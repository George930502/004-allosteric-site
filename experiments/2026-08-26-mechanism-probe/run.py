"""Score the three cross-system mechanism signatures on the `development` tier.

Reads `config.yaml` beside this file, writes `records.jsonl` incrementally and
`metrics.json` at the end. Resumable on the same key rule as the method sweep.

Every number comes from `allo.scoring.score_arm`, the same call the method sweep makes, so
the two experiments' records are directly comparable and the comparison does not depend on
either script.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import yaml

from allo import network
from allo.classical import mechanism, postprocess
from allo.inputs import apo_input
from allo.scoring.harness import score_arm

HERE = Path(__file__).resolve().parent
CONFIG = yaml.safe_load((HERE / "config.yaml").read_text())
RECORDS = HERE / "records.jsonl"

# The same three controls the method sweep reports against, computed on the same graph, so
# a signature cannot look strong by being measured against a weaker reference.
CONTROLS = ("distance_from_source_negated", "eigenvector_centrality", "degree")


def build_graph(apo, name: str):
    spec = dict(CONFIG["graphs"][name])
    return network.build(
        apo,
        contact=spec["contact"],
        cutoff=float(spec["cutoff"]),
        weighting=spec["weighting"],
    )


def detrended(scores, distance, source, mode):
    if mode == "raw":
        return scores, {}
    bins = (
        float(CONFIG["gaussian_bandwidth"])
        if mode == "gaussian_kernel"
        else int(CONFIG["binned_rank_bins"])
    )
    return postprocess.decay_residual(scores, distance, source, form=mode, bins=bins)


def main() -> int:
    from allo.classical import baselines

    done = set()
    if RECORDS.exists():
        for line in RECORDS.read_text().splitlines():
            if line.strip():
                done.add(json.loads(line)["key"])

    started = time.time()
    with RECORDS.open("a") as sink:
        for arm in CONFIG["arms"]:
            apo = apo_input(arm)
            distance = network.min_heavy_distance_to(apo, apo.active_site)
            for graph_name in CONFIG["graphs"]:
                graph = build_graph(apo, graph_name)
                reference = {
                    name: graph.as_scores(baselines.SCORERS[name](graph)) for name in CONTROLS
                }
                for scorer_name, scorer in mechanism.SCORERS.items():
                    params = dict(CONFIG["scorer_params"].get(scorer_name, {}))
                    raw = graph.as_scores(scorer(graph, **params))
                    for mode in CONFIG["detrend"]:
                        key = f"{arm}|{graph_name}|{scorer_name}|{mode}"
                        if key in done:
                            continue
                        scores, fit = detrended(raw, distance, apo.active_site, mode)
                        record = score_arm(
                            arm,
                            scores,
                            method=f"{scorer_name}[{graph_name}][{mode}]",
                            against=reference,
                        )
                        record |= {
                            "key": key,
                            "arm": arm,
                            "graph": graph_name,
                            "scorer": scorer_name,
                            "detrend": mode,
                            "decay_fit": fit,
                            "scorer_params": params,
                        }
                        sink.write(json.dumps(record) + "\n")
                        sink.flush()
                print(f"{arm}/{graph_name}: {time.time() - started:.0f}s", flush=True)

    rows = [json.loads(line) for line in RECORDS.read_text().splitlines() if line.strip()]
    (HERE / "metrics.json").write_text(json.dumps(summarise(rows), indent=2, default=str) + "\n")
    print(f"{len(rows)} records, {time.time() - started:.0f}s")
    return 0


def summarise(rows: list[dict]) -> dict:
    by_variant: dict[str, list[dict]] = {}
    for row in rows:
        by_variant.setdefault(f"{row['graph']}|{row['scorer']}|{row['detrend']}", []).append(row)

    table = []
    for variant, group in sorted(by_variant.items()):
        graph_name, scorer, mode = variant.split("|")
        table.append(
            {
                "graph": graph_name,
                "scorer": scorer,
                "detrend": mode,
                "n_arms": len(group),
                "mean_auc_roc": round(
                    float(np.mean([r["endpoints"]["auc_roc"] for r in group])), 4
                ),
                "min_auc_roc": round(float(np.min([r["endpoints"]["auc_roc"] for r in group])), 4),
                "total_hits_at_5": int(sum(r["endpoints"]["hits_at_5"] for r in group)),
                "mean_dcc_angstrom": round(
                    float(np.mean([r["endpoints"]["dcc_angstrom"] for r in group])), 3
                ),
                "n_reject_matched_patch_uncorrected": sum(
                    r["nulls"]["matched_patch"]["p_calibrated"] <= 0.05 for r in group
                ),
                "arms": {r["arm"]: r["endpoints"]["auc_roc"] for r in group},
            }
        )
    table.sort(key=lambda r: -r["mean_auc_roc"])
    return {"config": CONFIG, "n_records": len(rows), "n_variants": len(table), "ranking": table}


if __name__ == "__main__":
    sys.exit(main())
