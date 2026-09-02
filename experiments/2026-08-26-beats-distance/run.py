"""Which scorers beat the distance baseline on its own terms?

Reads `config.yaml` beside this file, writes `records.jsonl` incrementally and `metrics.json`
at the end. Resumable: a key already in `records.jsonl` is not recomputed.

For every scorer in the battery and every `development` arm, this runs two frozen tests:

* `score_arm` -- the confirmatory endpoint against the matched-patch null, which asks whether
  the scorer ranks the label patch above geometry-matched background.
* `compare_methods` -- the paired test against `distance_from_source_negated`, which asks
  whether it does so **better than distance alone**.

The second is the one that matters here. A scorer can pass the first because distance passes
it, and the paired test removes exactly that: both scores see the identical matched-patch
pool, the difference of their midrank vectors is the statistic, and every property of the arm
that acts on both alike cancels.

Nothing here is a result until a chosen scorer is frozen and run once on the primary
benchmark. This is a screen over 59 scorers on 4 arms, and the multiplicity that implies is
the reason `docs/method/exploration/results/41-selection-and-power.md` exists.
"""

from __future__ import annotations

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
from allo.scoring.harness import compare_methods, score_arm

HERE = Path(__file__).resolve().parent
CONFIG = yaml.safe_load((HERE / "config.yaml").read_text())
RECORDS = HERE / "records.jsonl"
SCORERS = CLASSICAL | QUANTUM


def spearman(a: np.ndarray, b: np.ndarray) -> float:
    ra, rb = rankdata(a), rankdata(b)
    if ra.std() == 0 or rb.std() == 0:
        return float("nan")
    return float(np.corrcoef(ra, rb)[0, 1])


def holm(pairs: list[tuple[str, float]], alpha: float = 0.05) -> dict[str, bool]:
    """Holm-Bonferroni over one family. Returns which members reject."""
    ordered = sorted(pairs, key=lambda kv: kv[1])
    reject: dict[str, bool] = {}
    still = True
    for i, (name, p) in enumerate(ordered):
        still = still and p <= alpha / (len(ordered) - i)
        reject[name] = still
    return reject


def main() -> int:
    done = set()
    if RECORDS.exists():
        for line in RECORDS.read_text().splitlines():
            if line.strip():
                done.add(json.loads(line)["key"])

    started = time.time()
    with RECORDS.open("a") as sink:
        for arm in CONFIG["arms"]:
            apo = apo_input(arm)
            graph = network.build(apo, **CONFIG["graph"])
            distance = np.asarray(
                [network.min_heavy_distance_to(apo, apo.active_site)[r] for r in graph.order],
                dtype=float,
            )
            baselines = {
                name: graph.as_scores(np.asarray(SCORERS[name](graph), dtype=float))
                for name in (CONFIG["baseline"], CONFIG["second_baseline"])
            }

            for name, fn in SCORERS.items():
                key = f"{arm}|{name}"
                if key in done:
                    continue
                try:
                    values = np.asarray(fn(graph), dtype=float)
                except (MemoryError, ArithmeticError, ValueError) as refused:
                    print(f"  skip {key}: {refused}", flush=True)
                    continue
                if not np.isfinite(values).all():
                    print(f"  skip {key}: non-finite scores", flush=True)
                    continue

                scores = graph.as_scores(values)
                record = score_arm(arm, scores, method=name)
                row = {
                    "key": key,
                    "arm": arm,
                    "scorer": name,
                    "family": "quantum" if name in QUANTUM else "classical",
                    "auc_roc": record["endpoints"]["auc_roc"],
                    "hits_at_5": record["endpoints"]["hits_at_5"],
                    "dcc_angstrom": record["endpoints"]["dcc_angstrom"],
                    "p_calibrated": record["nulls"]["matched_patch"]["p_calibrated"],
                    "rho_to_distance": round(spearman(values, -distance), 4),
                }
                for label, baseline in baselines.items():
                    if name == label:
                        continue
                    beat = compare_methods(arm, scores, baseline, names=(name, label))
                    row[f"vs_{label}"] = {
                        "auc_difference": beat["auc_roc_difference"],
                        "mean_rank_difference": beat["mean_rank_difference"],
                        "leader": beat["leader"],
                        "p_calibrated": beat["p_calibrated"],
                    }
                sink.write(json.dumps(row) + "\n")
                sink.flush()
            print(f"{arm}: {time.time() - started:.0f}s", flush=True)

    rows = [json.loads(line) for line in RECORDS.read_text().splitlines() if line.strip()]
    (HERE / "metrics.json").write_text(json.dumps(summarise(rows), indent=2, default=str) + "\n")
    print(f"{len(rows)} records, {time.time() - started:.0f}s")
    return 0


def summarise(rows: list[dict]) -> dict:
    by: dict[str, list[dict]] = {}
    for row in rows:
        by.setdefault(row["scorer"], []).append(row)

    table = []
    for scorer, group in sorted(by.items()):
        entry = {
            "scorer": scorer,
            "family": group[0]["family"],
            "n_arms": len(group),
            "mean_auc_roc": round(float(np.mean([r["auc_roc"] for r in group])), 4),
            "min_auc_roc": round(float(np.min([r["auc_roc"] for r in group])), 4),
            "mean_abs_rho_to_distance": round(
                float(np.mean([abs(r["rho_to_distance"]) for r in group])), 4
            ),
            "total_hits_at_5": int(sum(r["hits_at_5"] for r in group)),
            "n_reject_confirmatory": sum(r["p_calibrated"] <= 0.05 for r in group),
        }
        for label in (CONFIG["baseline"], CONFIG["second_baseline"]):
            field = f"vs_{label}"
            beats = [r[field] for r in group if field in r]
            if beats:
                entry[field] = {
                    "n_arms_leading": sum(b["leader"] == scorer for b in beats),
                    "n_arms_beating_at_05": sum(
                        b["leader"] == scorer and b["p_calibrated"] <= 0.05 for b in beats
                    ),
                    "mean_auc_difference": round(
                        float(np.mean([b["auc_difference"] for b in beats])), 4
                    ),
                    "min_p_calibrated": round(float(np.min([b["p_calibrated"] for b in beats])), 6),
                }
        table.append(entry)

    # Holm over the whole battery, per arm, on the "beats distance" p-values. This is the
    # multiplicity the screen actually incurs, and reporting the uncorrected count without it
    # would be the exact error `41-selection-and-power.md` was written to prevent.
    corrected = {}
    field = f"vs_{CONFIG['baseline']}"
    for arm in CONFIG["arms"]:
        pairs = [
            (r["scorer"], r[field]["p_calibrated"])
            for r in rows
            if r["arm"] == arm and field in r and r[field]["leader"] == r["scorer"]
        ]
        if pairs:
            reject = holm(pairs)
            corrected[arm] = {
                "n_tested": len(pairs),
                "n_reject_holm": sum(reject.values()),
                "survivors": sorted(name for name, ok in reject.items() if ok),
            }

    return {
        "config": CONFIG,
        "n_records": len(rows),
        "beats_distance_holm_per_arm": corrected,
        "ranking": sorted(table, key=lambda r: -r["mean_auc_roc"]),
    }


if __name__ == "__main__":
    sys.exit(main())
