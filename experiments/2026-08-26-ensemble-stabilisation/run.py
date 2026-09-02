"""Does averaging a coherent observable over structural uncertainty stabilise it?

Reads `config.yaml` beside this file, writes `records.jsonl` incrementally and `metrics.json`
at the end. Resumable: a key already in `records.jsonl` is not recomputed.

The estimator under test is the **rank mean over K jittered structures**. Ranks rather than
raw values, because the observables differ by orders of magnitude between residues and an
arithmetic mean would be dominated by whichever structure happened to produce the largest
numbers. A rank mean asks only that the K structures agree on the ordering, which is the
thing the downstream ranking uses.

Two readouts, and both are needed for a verdict:

* **stability** -- the rank correlation between the estimator computed on the reference
  structure and the same estimator computed on a *held-out* jittered structure. The held-out
  seeds are disjoint from the ensemble seeds, so an ensemble cannot score well by having
  already seen the test perturbation.
* **accuracy** -- AUC and the matched-patch p through the frozen harness.

An ensemble that raises stability and lowers accuracy has bought nothing, so a size is only
worth adopting if it moves the first without moving the second.
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
SCORERS = CLASSICAL | QUANTUM


def spearman(a: np.ndarray, b: np.ndarray) -> float:
    ra, rb = rankdata(a), rankdata(b)
    if ra.std() == 0 or rb.std() == 0:
        return float("nan")
    return float(np.corrcoef(ra, rb)[0, 1])


def jitter(apo, sigma: float, seed: int):
    rng = np.random.default_rng(seed)
    coord = apo.structure.coord + rng.normal(0.0, sigma, apo.structure.coord.shape)
    return dataclasses.replace(apo, structure=dataclasses.replace(apo.structure, coord=coord))


def per_seed_ranks(apo, names: list[str], sigma: float, seeds: list[int]) -> dict[str, list]:
    """Midrank vector of every named scorer, once per jittered structure.

    The ensemble sizes are nested -- K = 4 is the first four seeds of K = 16 -- so each seed is
    scored once here and the sizes are prefix means of the result. Recomputing K = 4 separately
    would cost four times as much and would also let the two sizes disagree, which they must
    not.
    """
    out: dict[str, list] = {name: [] for name in names}
    for seed in seeds:
        moved = jitter(apo, sigma, seed) if sigma > 0 else apo
        try:
            graph = network.build(moved, **CONFIG["graph"])
        except (ValueError, MemoryError, ArithmeticError) as refused:
            print(f"  skip build seed {seed}: {refused}", flush=True)
            continue
        for name in names:
            try:
                values = np.asarray(SCORERS[name](graph), dtype=float)
            except (MemoryError, ArithmeticError, ValueError):
                continue
            if np.isfinite(values).all():
                out[name].append(rankdata(values))
    return out


def prefix_mean(ranks: list, size: int) -> np.ndarray | None:
    """The K = `size` ensemble estimate: the mean of the first `size` rank vectors."""
    if len(ranks) < size:
        return None
    return np.mean(np.stack(ranks[:size]), axis=0)


def main() -> int:
    done = set()
    if RECORDS.exists():
        for line in RECORDS.read_text().splitlines():
            if line.strip():
                done.add(json.loads(line)["key"])

    names = list(CONFIG["scorers"])
    started = time.time()

    with RECORDS.open("a") as sink:
        for arm in CONFIG["arms"]:
            apo = apo_input(arm)
            base_graph = network.build(apo, **CONFIG["graph"])
            distance = np.asarray(
                [network.min_heavy_distance_to(apo, apo.active_site)[r] for r in base_graph.order],
                dtype=float,
            )
            seeds = CONFIG["ensemble"]["build_seeds"]
            test_seeds = CONFIG["test"]["seeds"]
            test_sigma = CONFIG["test"]["sigma"]

            for sigma in CONFIG["ensemble"]["sigma"]:
                # K = 1 is the unperturbed structure, which is the estimator every earlier
                # experiment used. Every K > 1 is the ensemble around it.
                single = per_seed_ranks(apo, names, 0.0, [0])
                many = per_seed_ranks(apo, names, sigma, seeds)
                held = [
                    (
                        per_seed_ranks(jitter(apo, test_sigma, t), names, 0.0, [0]),
                        per_seed_ranks(jitter(apo, test_sigma, t), names, sigma, seeds),
                    )
                    for t in test_seeds
                ]
                print(f"{arm}/sigma={sigma}: built, {time.time() - started:.0f}s", flush=True)

                for size in CONFIG["ensemble"]["sizes"]:
                    for name in names:
                        key = f"{arm}|{sigma}|{size}|{name}"
                        if key in done:
                            continue
                        source = single if size == 1 else many
                        values = prefix_mean(source[name], 1 if size == 1 else size)
                        if values is None:
                            continue
                        stability = []
                        for one, pool in held:
                            other = prefix_mean(
                                (one if size == 1 else pool)[name], 1 if size == 1 else size
                            )
                            if other is not None:
                                stability.append(spearman(values, other))
                        record = score_arm(
                            arm, base_graph.as_scores(values), method=f"{name}[ens{size}]"
                        )
                        sink.write(
                            json.dumps(
                                {
                                    "key": key,
                                    "arm": arm,
                                    "scorer": name,
                                    "family": "quantum" if name in QUANTUM else "classical",
                                    "sigma": sigma,
                                    "size": size,
                                    "auc_roc": record["endpoints"]["auc_roc"],
                                    "hits_at_5": record["endpoints"]["hits_at_5"],
                                    "p_calibrated": record["nulls"]["matched_patch"][
                                        "p_calibrated"
                                    ],
                                    "held_out_stability": round(float(np.mean(stability)), 4)
                                    if stability
                                    else None,
                                    "rho_to_distance": round(spearman(values, -distance), 4),
                                }
                            )
                            + "\n"
                        )
                        sink.flush()
                    print(f"{arm}/sigma={sigma}/K={size}: {time.time() - started:.0f}s", flush=True)

    rows = [json.loads(line) for line in RECORDS.read_text().splitlines() if line.strip()]
    (HERE / "metrics.json").write_text(json.dumps(summarise(rows), indent=2, default=str) + "\n")
    print(f"{len(rows)} records, {time.time() - started:.0f}s")
    return 0


def summarise(rows: list[dict]) -> dict:
    by: dict[tuple[str, float, int], list[dict]] = {}
    for row in rows:
        by.setdefault((row["scorer"], row["sigma"], row["size"]), []).append(row)

    table = []
    for (scorer, sigma, size), group in sorted(by.items()):
        stability = [r["held_out_stability"] for r in group if r["held_out_stability"] is not None]
        table.append(
            {
                "scorer": scorer,
                "family": group[0]["family"],
                "sigma": sigma,
                "size": size,
                "n_arms": len(group),
                "mean_held_out_stability": round(float(np.mean(stability)), 4)
                if stability
                else None,
                "mean_auc_roc": round(float(np.mean([r["auc_roc"] for r in group])), 4),
                "min_auc_roc": round(float(np.min([r["auc_roc"] for r in group])), 4),
                "total_hits_at_5": int(sum(r["hits_at_5"] for r in group)),
                "n_reject_uncorrected": sum(r["p_calibrated"] <= 0.05 for r in group),
                "mean_abs_rho_to_distance": round(
                    float(np.mean([abs(r["rho_to_distance"]) for r in group])), 4
                ),
            }
        )

    # The verdict table: what K = 16 buys over K = 1, per scorer.
    gains = []
    for scorer in sorted({r["scorer"] for r in rows}):
        for sigma in sorted({r["sigma"] for r in rows}):
            one = [
                r for r in table if r["scorer"] == scorer and r["size"] == 1 and r["sigma"] == sigma
            ]
            many = [
                r
                for r in table
                if r["scorer"] == scorer and r["size"] == 16 and r["sigma"] == sigma
            ]
            if one and many and one[0]["mean_held_out_stability"] is not None:
                gains.append(
                    {
                        "scorer": scorer,
                        "sigma": sigma,
                        "stability_1": one[0]["mean_held_out_stability"],
                        "stability_16": many[0]["mean_held_out_stability"],
                        "stability_gain": round(
                            many[0]["mean_held_out_stability"] - one[0]["mean_held_out_stability"],
                            4,
                        ),
                        "auc_1": one[0]["mean_auc_roc"],
                        "auc_16": many[0]["mean_auc_roc"],
                        "auc_change": round(many[0]["mean_auc_roc"] - one[0]["mean_auc_roc"], 4),
                    }
                )

    return {
        "config": CONFIG,
        "n_records": len(rows),
        "gain_at_16": sorted(gains, key=lambda r: -r["stability_gain"]),
        "sweep": table,
    }


if __name__ == "__main__":
    sys.exit(main())
