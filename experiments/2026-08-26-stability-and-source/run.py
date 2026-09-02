"""How stable is a residue score under perturbation, and how much does the source decide it?

Reads `config.yaml` beside this file, writes `records.jsonl` incrementally and `metrics.json`
at the end. Resumable: a key already in `records.jsonl` is not recomputed.

Three perturbation families disturb the input, one disturbs the algorithm:

* `coordinate_noise` jitters every atom and rebuilds the graph. This is the physical
  robustness question -- would a different crystal of the same protein give the same answer?
* `edge_dropout` removes edges from the built graph. This is the topological question, with
  the geometry held fixed, and it separates "sensitive to coordinates" from "sensitive to
  which contacts exist".
* `source_dropout` removes one active-site residue. `CHALLENGE.md` §4.1 says the ranking is
  of connectivity "in most cases" to an active site, so how much the exact source set
  matters is a question the challenge itself leaves open.
* `coherence_window` shortens the walk's time window. A device with a short T2 cannot run
  the long window, so this is the §4.2 noise-resilience axis measured in the observable's
  own units.

Four readouts per record. `rho_to_baseline` is rank stability, `delta_auc` is endpoint
stability, `top5_jaccard` is stability of the deliverable, and `rho_to_distance` is there so
a scorer cannot look stable merely by being a distance ranking, which is stable for a reason
that has nothing to do with the method.
"""

from __future__ import annotations

import dataclasses
import json
import sys
import time
from pathlib import Path

import numpy as np
import yaml
from scipy.stats import rankdata

from allo import network
from allo.classical import SCORERS as CLASSICAL
from allo.inputs import apo_input
from allo.quantum import SCORERS as QUANTUM
from allo.scoring.harness import score_arm

HERE = Path(__file__).resolve().parent
CONFIG = yaml.safe_load((HERE / "config.yaml").read_text())
RECORDS = HERE / "records.jsonl"

CTQW = {name for name in QUANTUM if name.startswith("ctqw_")} | {"quantum_perturbation_response"}
CTQW -= {"ctqw_infinite_time_average"}  # no finite window, so no coherence axis


def scorers() -> dict:
    keep = dict(QUANTUM)
    for name in CONFIG["classical_controls"]:
        keep[name] = CLASSICAL[name]
    return keep


def spearman(a: np.ndarray, b: np.ndarray) -> float:
    """Midranks, not ordinal ranks -- several controls tie heavily and `argsort` would break
    those ties by array position, making the answer depend on residue order."""
    ra, rb = rankdata(a), rankdata(b)
    if ra.std() == 0 or rb.std() == 0:
        return float("nan")
    return float(np.corrcoef(ra, rb)[0, 1])


def jaccard(a: np.ndarray, b: np.ndarray, k: int = 5) -> float:
    top_a = set(np.argsort(-a)[:k].tolist())
    top_b = set(np.argsort(-b)[:k].tolist())
    return len(top_a & top_b) / len(top_a | top_b)


def jitter(apo, sigma: float, seed: int):
    """A new apo input with every atom displaced by isotropic Gaussian noise."""
    rng = np.random.default_rng(seed)
    coord = apo.structure.coord + rng.normal(0.0, sigma, apo.structure.coord.shape)
    return dataclasses.replace(apo, structure=dataclasses.replace(apo.structure, coord=coord))


def drop_edges(graph, fraction: float, seed: int):
    """A copy of the graph with a random `fraction` of its edges removed."""
    rng = np.random.default_rng(seed)
    upper = np.argwhere(np.triu(graph.weight, 1) > 0)
    n_drop = int(round(fraction * len(upper)))
    if n_drop == 0:
        return graph
    chosen = upper[rng.choice(len(upper), size=n_drop, replace=False)]
    weight = graph.weight.copy()
    for a, b in chosen:
        weight[a, b] = weight[b, a] = 0.0
    return dataclasses.replace(graph, weight=weight, cache={})


def variants(apo, graph) -> list[tuple[str, dict]]:
    """Every perturbation to apply, as `(key, spec)`. `spec` is what `evaluate` consumes."""
    out: list[tuple[str, dict]] = [("baseline", {"kind": "baseline"})]
    noise = CONFIG["perturbations"]["coordinate_noise"]
    for sigma in noise["sigma"]:
        for seed in noise["seeds"]:
            out.append((f"coord|{sigma}|{seed}", {"kind": "coord", "sigma": sigma, "seed": seed}))
    drop = CONFIG["perturbations"]["edge_dropout"]
    for fraction in drop["fraction"]:
        for seed in drop["seeds"]:
            out.append(
                (f"edge|{fraction}|{seed}", {"kind": "edge", "fraction": fraction, "seed": seed})
            )
    limit = CONFIG["perturbations"]["source_dropout"]["max_variants"]
    for held in sorted(graph.source)[:limit]:
        out.append((f"source|{held}", {"kind": "source", "held": held}))
    for window in CONFIG["perturbations"]["coherence_window"]["window"]:
        out.append((f"window|{window}", {"kind": "window", "window": window}))
    return out


def perturbed_graph(apo, graph, spec: dict):
    """The graph a variant scores on. `window` perturbs the algorithm, not the graph."""
    if spec["kind"] == "coord":
        return network.build(jitter(apo, spec["sigma"], spec["seed"]), **CONFIG["graph"])
    if spec["kind"] == "edge":
        return drop_edges(graph, spec["fraction"], spec["seed"])
    if spec["kind"] == "source":
        keep = tuple(r for r in graph.source if r != spec["held"])
        return dataclasses.replace(graph, source=keep, cache={})
    return graph


def spectrum(graph) -> dict:
    """Graph properties that a stability difference might be explained by."""
    values = np.linalg.eigvalsh(graph.laplacian)
    return {
        "n": graph.n,
        "n_edges": int((graph.weight > 0).sum() // 2),
        "n_source": len(graph.source),
        "algebraic_connectivity": round(float(values[1]), 6),
        "spectral_range": round(float(values[-1] - values[0]), 4),
        "mean_degree": round(float(graph.degree.mean()), 3),
    }


def main() -> int:
    done = set()
    if RECORDS.exists():
        for line in RECORDS.read_text().splitlines():
            if line.strip():
                done.add(json.loads(line)["key"])

    pool = scorers()
    expensive = set(CONFIG["expensive_scorers"])
    expensive_seeds = set(CONFIG["expensive_seeds"])
    started = time.time()
    capped: list[str] = []

    with RECORDS.open("a") as sink:
        for arm in CONFIG["arms"]:
            apo = apo_input(arm)
            base_graph = network.build(apo, **CONFIG["graph"])
            context = spectrum(base_graph)
            distance = np.asarray(
                [network.min_heavy_distance_to(apo, apo.active_site)[r] for r in base_graph.order],
                dtype=float,
            )

            base_values: dict[str, np.ndarray] = {}
            for name, fn in pool.items():
                base_values[name] = np.asarray(fn(base_graph), dtype=float)

            for label, spec in variants(apo, base_graph):
                try:
                    graph = perturbed_graph(apo, base_graph, spec)
                except (ValueError, MemoryError, ArithmeticError) as refused:
                    print(f"  skip {arm}/{label}: {refused}", flush=True)
                    continue

                for name, fn in pool.items():
                    if spec["kind"] == "window" and name not in CTQW:
                        continue
                    if name in expensive and spec.get("seed", 0) not in expensive_seeds:
                        capped.append(f"{arm}|{label}|{name}")
                        continue
                    key = f"{arm}|{label}|{name}"
                    if key in done:
                        continue
                    kwargs = {"window": spec["window"]} if spec["kind"] == "window" else {}
                    try:
                        values = np.asarray(fn(graph, **kwargs), dtype=float)
                    except (MemoryError, ArithmeticError, ValueError) as refused:
                        print(f"  skip {key}: {refused}", flush=True)
                        continue

                    record = score_arm(arm, graph.as_scores(values), method=f"{name}[{label}]")
                    sink.write(
                        json.dumps(
                            {
                                "key": key,
                                "arm": arm,
                                "scorer": name,
                                "family": "quantum" if name in QUANTUM else "classical",
                                "variant": label,
                                "kind": spec["kind"],
                                "spec": spec,
                                "auc_roc": record["endpoints"]["auc_roc"],
                                "hits_at_5": record["endpoints"]["hits_at_5"],
                                "dcc_angstrom": record["endpoints"]["dcc_angstrom"],
                                "p_calibrated": record["nulls"]["matched_patch"]["p_calibrated"],
                                "rho_to_baseline": spearman(values, base_values[name]),
                                "top5_jaccard": jaccard(values, base_values[name]),
                                "rho_to_distance": spearman(values, -distance),
                                "context": context,
                            }
                        )
                        + "\n"
                    )
                    sink.flush()
                print(f"{arm}/{label}: {time.time() - started:.0f}s", flush=True)

    rows = [json.loads(line) for line in RECORDS.read_text().splitlines() if line.strip()]
    (HERE / "metrics.json").write_text(
        json.dumps(summarise(rows, capped), indent=2, default=str) + "\n"
    )
    print(f"{len(rows)} records, {len(capped)} capped, {time.time() - started:.0f}s")
    return 0


def summarise(rows: list[dict], capped: list[str]) -> dict:
    """Per scorer: how much of its ranking survives each perturbation family."""
    base = {(r["arm"], r["scorer"]): r for r in rows if r["kind"] == "baseline"}

    by_scorer: dict[tuple[str, str], list[dict]] = {}
    for row in rows:
        if row["kind"] == "baseline":
            continue
        by_scorer.setdefault((row["scorer"], row["kind"]), []).append(row)

    table = []
    for (scorer, kind), group in sorted(by_scorer.items()):
        rho = [r["rho_to_baseline"] for r in group if np.isfinite(r["rho_to_baseline"])]
        delta = [
            r["auc_roc"] - base[(r["arm"], r["scorer"])]["auc_roc"]
            for r in group
            if (r["arm"], r["scorer"]) in base
        ]
        table.append(
            {
                "scorer": scorer,
                "family": group[0]["family"],
                "perturbation": kind,
                "n": len(group),
                "mean_rho_to_baseline": round(float(np.mean(rho)), 4) if rho else None,
                "min_rho_to_baseline": round(float(np.min(rho)), 4) if rho else None,
                "mean_abs_delta_auc": round(float(np.mean(np.abs(delta))), 4) if delta else None,
                "max_abs_delta_auc": round(float(np.max(np.abs(delta))), 4) if delta else None,
                "mean_top5_jaccard": round(float(np.mean([r["top5_jaccard"] for r in group])), 4),
            }
        )

    baseline_table = [
        {
            "arm": arm,
            "scorer": scorer,
            "family": row["family"],
            "auc_roc": row["auc_roc"],
            "rho_to_distance": round(row["rho_to_distance"], 4),
            "p_calibrated": row["p_calibrated"],
        }
        for (arm, scorer), row in sorted(base.items())
    ]

    return {
        "config": CONFIG,
        "n_records": len(rows),
        "n_capped": len(capped),
        "capped": sorted(set(capped))[:50],
        "context": {r["arm"]: r["context"] for r in rows},
        "baseline": baseline_table,
        "stability": sorted(
            table, key=lambda r: (r["perturbation"], -(r["mean_rho_to_baseline"] or -9))
        ),
    }


if __name__ == "__main__":
    sys.exit(main())
