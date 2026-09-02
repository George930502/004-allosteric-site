"""Does the propagation source have to be the catalytic site, and does it have to be right?

Reads `config.yaml` beside this file, writes `records.jsonl` incrementally and `metrics.json`
at the end. Resumable: a key already in `records.jsonl` is not recomputed.

Every source is size-matched to that arm's frozen active site and derived from the apo entry
alone. `random` is the null the whole experiment turns on: if a random size-matched source
scores like the catalytic one, then source conditioning carries no information and every
"propagation from the active site" claim in the report is decoration.

`degree` is carried as an invariance check. It does not read the source, so its score must be
identical in every row of an arm. A difference means the source is leaking somewhere it
should not.
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
from allo.classical.baselines import protrusion_index
from allo.inputs import apo_input
from allo.quantum import SCORERS as QUANTUM
from allo.scoring.harness import score_arm

HERE = Path(__file__).resolve().parent
CONFIG = yaml.safe_load((HERE / "config.yaml").read_text())
RECORDS = HERE / "records.jsonl"


def scorers() -> dict:
    keep = {name: QUANTUM[name] for name in CONFIG["scorers"]["quantum"]}
    keep |= {name: CLASSICAL[name] for name in CONFIG["scorers"]["classical"]}
    return keep


def spearman(a: np.ndarray, b: np.ndarray) -> float:
    ra, rb = rankdata(a), rankdata(b)
    if ra.std() == 0 or rb.std() == 0:
        return float("nan")
    return float(np.corrcoef(ra, rb)[0, 1])


def top_k(values: np.ndarray, order: tuple[int, ...], k: int) -> tuple[int, ...]:
    return tuple(sorted(int(order[i]) for i in np.argsort(-np.asarray(values))[:k]))


def source_sets(graph, k: int) -> dict[str, tuple[int, ...]]:
    """Every alternative source, all size `k`, all derived from the apo entry alone."""
    out: dict[str, tuple[int, ...]] = {"catalytic": tuple(sorted(graph.source))}
    out["eigenvector_centrality"] = top_k(
        CLASSICAL["eigenvector_centrality"](graph), graph.order, k
    )
    out["degree"] = top_k(graph.degree, graph.order, k)
    # Protrusion is a convexity measure, so the most buried residues are its smallest values.
    out["buried"] = top_k(-protrusion_index(graph), graph.order, k)
    fiedler = np.linalg.eigh(graph.laplacian)[1][:, 1]
    out["fiedler"] = top_k(np.abs(fiedler), graph.order, k)
    for seed in CONFIG["sources"]["random"]["seeds"]:
        rng = np.random.default_rng(seed)
        picked = rng.choice(graph.n, size=k, replace=False)
        out[f"random|{seed}"] = tuple(sorted(int(graph.order[i]) for i in picked))
    return out


def main() -> int:
    done = set()
    if RECORDS.exists():
        for line in RECORDS.read_text().splitlines():
            if line.strip():
                done.add(json.loads(line)["key"])

    pool = scorers()
    started = time.time()

    with RECORDS.open("a") as sink:
        for arm in CONFIG["arms"]:
            apo = apo_input(arm)
            base = network.build(apo, **CONFIG["graph"])
            catalytic_distance = np.asarray(
                [network.min_heavy_distance_to(apo, apo.active_site)[r] for r in base.order],
                dtype=float,
            )
            sources = source_sets(base, len(base.source))

            for label, residues in sources.items():
                graph = dataclasses.replace(base, source=residues, cache={})
                own_distance = np.asarray(
                    [network.min_heavy_distance_to(apo, residues)[r] for r in base.order],
                    dtype=float,
                )
                overlap = len(set(residues) & set(base.source)) / len(residues)

                for name, fn in pool.items():
                    key = f"{arm}|{label}|{name}"
                    if key in done:
                        continue
                    try:
                        values = np.asarray(fn(graph), dtype=float)
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
                                "source": label.split("|")[0],
                                "source_label": label,
                                "source_overlap_with_catalytic": round(overlap, 4),
                                "n_source": len(residues),
                                "auc_roc": record["endpoints"]["auc_roc"],
                                "hits_at_5": record["endpoints"]["hits_at_5"],
                                "dcc_angstrom": record["endpoints"]["dcc_angstrom"],
                                "p_calibrated": record["nulls"]["matched_patch"]["p_calibrated"],
                                "rho_to_own_source_distance": spearman(values, -own_distance),
                                "rho_to_catalytic_distance": spearman(values, -catalytic_distance),
                                "score_checksum": round(float(np.sum(rankdata(values))), 3),
                            }
                        )
                        + "\n"
                    )
                    sink.flush()
                print(f"{arm}/{label}: {time.time() - started:.0f}s", flush=True)

    rows = [json.loads(line) for line in RECORDS.read_text().splitlines() if line.strip()]
    (HERE / "metrics.json").write_text(json.dumps(summarise(rows), indent=2, default=str) + "\n")
    print(f"{len(rows)} records, {time.time() - started:.0f}s")
    return 0


def summarise(rows: list[dict]) -> dict:
    """Per (scorer, source): mean AUC over arms, and the gap to the catalytic control."""
    by: dict[tuple[str, str], list[dict]] = {}
    for row in rows:
        by.setdefault((row["scorer"], row["source"]), []).append(row)

    catalytic = {
        scorer: float(np.mean([r["auc_roc"] for r in group]))
        for (scorer, source), group in by.items()
        if source == "catalytic"
    }

    table = []
    for (scorer, source), group in sorted(by.items()):
        auc = [r["auc_roc"] for r in group]
        table.append(
            {
                "scorer": scorer,
                "family": group[0]["family"],
                "source": source,
                "n": len(group),
                "mean_auc_roc": round(float(np.mean(auc)), 4),
                "min_auc_roc": round(float(np.min(auc)), 4),
                "gap_to_catalytic": round(
                    float(np.mean(auc)) - catalytic.get(scorer, float("nan")), 4
                ),
                "total_hits_at_5": int(sum(r["hits_at_5"] for r in group)),
                "n_reject_uncorrected": sum(r["p_calibrated"] <= 0.05 for r in group),
                "mean_rho_to_own_source_distance": round(
                    float(np.mean([r["rho_to_own_source_distance"] for r in group])), 4
                ),
                "mean_source_overlap": round(
                    float(np.mean([r["source_overlap_with_catalytic"] for r in group])), 4
                ),
            }
        )

    # The invariance check. `degree` ignores the source, so one checksum per arm is expected.
    invariance = {}
    for arm in CONFIG["arms"]:
        sums = {r["score_checksum"] for r in rows if r["arm"] == arm and r["scorer"] == "degree"}
        invariance[arm] = {"distinct_degree_checksums": len(sums), "expected": 1}

    return {
        "config": CONFIG,
        "n_records": len(rows),
        "invariance_check": invariance,
        "by_source_and_scorer": sorted(table, key=lambda r: (r["scorer"], -r["mean_auc_roc"])),
    }


if __name__ == "__main__":
    sys.exit(main())
