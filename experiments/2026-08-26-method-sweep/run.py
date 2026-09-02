"""Screen every graph x scorer x detrend combination on the `development` tier.

Reads `config.yaml` beside this file, writes `records.jsonl` incrementally and
`metrics.json` at the end. Resumable: a record already present in `records.jsonl` for the
same key is not recomputed, so a killed run continues where it stopped.

This is a screen. Selecting the best of several hundred variants on four arms is exactly the
multiplicity the `development` tier exists to absorb, and the selected variant has to be
frozen and scored once on the primary benchmark before any of it is a result.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import yaml

from allo import network
from allo.classical import SCORERS as CLASSICAL
from allo.classical import postprocess
from allo.inputs import apo_input
from allo.quantum import SCORERS as QUANTUM
from allo.scoring.harness import score_arm

HERE = Path(__file__).resolve().parent
CONFIG = yaml.safe_load((HERE / "config.yaml").read_text())
RECORDS = HERE / "records.jsonl"

SCORERS = CLASSICAL | QUANTUM
# The three controls every result is reported against. They are computed on the evaluation
# default graph, so a method cannot beat them by changing the graph under them.
CONTROLS = (
    "distance_from_source_negated",
    "eigenvector_centrality",
    "degree",
)


def build_graph(apo, name: str):
    spec = dict(CONFIG["graphs"][name])
    kwargs = {
        "contact": spec["contact"],
        "cutoff": float(spec["cutoff"]),
        "weighting": spec["weighting"],
    }
    if "decay_length" in spec:
        kwargs["decay_length"] = float(spec["decay_length"])
    if spec["weighting"] == "edge_class":
        kwargs["class_weights"] = dict(CONFIG["edge_class_weights"])
    return network.build(apo, **kwargs)


def detrended(scores, distance, source, mode):
    """Stage S6. `mode` names a `postprocess` decay form, or `raw` for no detrending."""
    if mode == "raw":
        return scores, {}
    bins = (
        float(CONFIG["gaussian_bandwidth"])
        if mode == "gaussian_kernel"
        else int(CONFIG["binned_rank_bins"])
    )
    return postprocess.decay_residual(scores, distance, source, form=mode, bins=bins)


def modes_for(graph_name: str) -> list[str]:
    extra = CONFIG["detrend_extra"] if graph_name in CONFIG["detrend_extra_graphs"] else []
    return list(CONFIG["detrend"]) + list(extra)


def main() -> int:
    done = set()
    if RECORDS.exists():
        for line in RECORDS.read_text().splitlines():
            if line.strip():
                done.add(json.loads(line)["key"])

    started = time.time()
    written = 0
    with RECORDS.open("a") as sink:
        for arm in CONFIG["arms"]:
            apo = apo_input(arm)
            distance = network.min_heavy_distance_to(apo, apo.active_site)
            reference = {}
            for graph_name in CONFIG["graphs"]:
                graph = build_graph(apo, graph_name)
                for scorer_name, scorer in SCORERS.items():
                    params = dict(CONFIG["scorer_params"].get(scorer_name, {}))
                    try:
                        values = scorer(graph, **params)
                    except (MemoryError, ArithmeticError) as refused:
                        print(f"  skip {arm}/{graph_name}/{scorer_name}: {refused}", flush=True)
                        continue
                    raw = graph.as_scores(values)
                    if graph_name == "evaluation_default" and scorer_name in CONTROLS:
                        reference[scorer_name] = raw
                    for mode in modes_for(graph_name):
                        key = f"{arm}|{graph_name}|{scorer_name}|{mode}"
                        if key in done:
                            continue
                        scores, fit = detrended(raw, distance, apo.active_site, mode)
                        record = score_arm(
                            arm,
                            scores,
                            method=f"{scorer_name}[{graph_name}][{mode}]",
                            against=reference or None,
                        )
                        record["key"] = key
                        record["arm"] = arm
                        record["graph"] = graph_name
                        record["scorer"] = scorer_name
                        record["detrend"] = mode
                        record["decay_fit"] = fit
                        record["scorer_params"] = params
                        sink.write(json.dumps(record) + "\n")
                        sink.flush()
                        written += 1
                print(
                    f"{arm}/{graph_name}: {written} written, {time.time() - started:.0f}s",
                    flush=True,
                )

    rows = [json.loads(line) for line in RECORDS.read_text().splitlines() if line.strip()]
    summary = summarise(rows)
    (HERE / "metrics.json").write_text(json.dumps(summary, indent=2, default=str) + "\n")
    print(f"{len(rows)} records, {time.time() - started:.0f}s")
    return 0


def summarise(rows: list[dict]) -> dict:
    """Aggregate across arms. Mean AUC-ROC is the screening statistic, not the decision."""
    by_variant: dict[str, list[dict]] = {}
    for row in rows:
        by_variant.setdefault(f"{row['graph']}|{row['scorer']}|{row['detrend']}", []).append(row)

    table = []
    for variant, group in sorted(by_variant.items()):
        graph_name, scorer, mode = variant.split("|")
        auc = [r["endpoints"]["auc_roc"] for r in group]
        table.append(
            {
                "graph": graph_name,
                "scorer": scorer,
                "detrend": mode,
                "n_arms": len(group),
                "mean_auc_roc": round(float(np.mean(auc)), 4),
                "min_auc_roc": round(float(np.min(auc)), 4),
                "mean_recall_at_5": round(
                    float(np.mean([r["endpoints"]["recall_at_5"] for r in group])), 4
                ),
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
    return {
        "config": CONFIG,
        "n_records": len(rows),
        "n_variants": len(table),
        "chance_lines": {
            row["arm"]: {
                "prevalence": row["prevalence"],
                "recall_at_5": row["chance"]["recall_at_5"],
                "dcc_angstrom": row["chance"]["dcc_angstrom"],
            }
            for row in rows
        },
        "ranking": table,
    }


if __name__ == "__main__":
    sys.exit(main())
