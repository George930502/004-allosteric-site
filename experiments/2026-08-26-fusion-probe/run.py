"""Does combining scores beat the best single score, and does site assembly change the list?

Reads `config.yaml` beside this file, writes `records.jsonl` incrementally and `metrics.json`
at the end. Resumable on the same key rule as the other two runners.

Consensus membership is chosen from the scorers' mutual rank correlation and never from
their AUC. The correlation matrix is label-blind, so choosing a diverse subset from it adds
no selection on the outcome; choosing the highest-scoring subset would.

Every number comes from `allo.scoring.score_arm`.
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
from allo.classical import baselines, postprocess
from allo.inputs import apo_input
from allo.quantum import SCORERS as QUANTUM
from allo.scoring.harness import score_arm

HERE = Path(__file__).resolve().parent
CONFIG = yaml.safe_load((HERE / "config.yaml").read_text())
RECORDS = HERE / "records.jsonl"

SCORERS = {
    name: fn
    for name, fn in (CLASSICAL | QUANTUM).items()
    if name not in set(CONFIG["skip_scorers"])
}
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
        return scores
    bins = (
        float(CONFIG["gaussian_bandwidth"])
        if mode == "gaussian_kernel"
        else int(CONFIG["binned_rank_bins"])
    )
    return postprocess.decay_residual(scores, distance, source, form=mode, bins=bins)[0]


def diverse_members(columns: dict[str, np.ndarray], cut: float) -> list[str]:
    """Greedy medoid-free cover: keep a scorer unless it duplicates one already kept.

    Deterministic and label-blind. Names are visited in sorted order, so the result depends
    on the score vectors and on nothing else.
    """
    ranked = {name: postprocess.midrank(values) for name, values in columns.items()}
    kept: list[str] = []
    for name in sorted(ranked):
        vector = ranked[name]
        duplicate = False
        for chosen in kept:
            other = ranked[chosen]
            correlation = np.corrcoef(vector, other)[0, 1]
            if np.isfinite(correlation) and abs(correlation) >= cut:
                duplicate = True
                break
        if not duplicate:
            kept.append(name)
    return kept


def oriented(columns: dict[str, np.ndarray], members: list[str]) -> list[dict]:
    """Sign-align members to the leading eigenvector of their own correlation matrix.

    A rank average assumes every member points the same way, and nothing guarantees that. Two
    members of the pool are known to run backwards: `soft_corridor_to_source` by measurement,
    and `anm_perturbation_response` by its own sign convention. Averaging them in unflipped
    subtracts signal.

    The fix stays label-blind. The leading eigenvector of the members' rank-correlation matrix
    is the direction they most agree on, and its loadings give each member a sign. No label is
    read, so this adds no selection on the outcome — it only removes an arbitrary convention.
    """
    matrix = np.stack([postprocess.midrank(columns[name]) for name in members])
    correlation = np.nan_to_num(np.corrcoef(matrix), nan=0.0)
    _, vectors = np.linalg.eigh(correlation)
    loading = vectors[:, -1]
    if loading.sum() < 0:
        loading = -loading
    return [row if sign >= 0 else -row for row, sign in zip(matrix, loading, strict=True)]


def main() -> int:
    done = set()
    if RECORDS.exists():
        for line in RECORDS.read_text().splitlines():
            if line.strip():
                done.add(json.loads(line)["key"])

    started = time.time()
    excluded = set(CONFIG["consensus_exclude"])
    with RECORDS.open("a") as sink:

        def emit(record: dict, key: str, **fields) -> None:
            record |= {"key": key, **fields}
            sink.write(json.dumps(record) + "\n")
            sink.flush()

        for arm in CONFIG["arms"]:
            apo = apo_input(arm)
            distance = network.min_heavy_distance_to(apo, apo.active_site)
            for graph_name in CONFIG["graphs"]:
                graph = build_graph(apo, graph_name)
                reference = {
                    name: graph.as_scores(baselines.SCORERS[name](graph)) for name in CONTROLS
                }
                coord = {residue: graph.coord[i] for i, residue in enumerate(graph.order)}

                for mode in CONFIG["detrend"]:
                    columns = {}
                    for name, scorer in SCORERS.items():
                        if name in excluded:
                            continue
                        values = detrended(
                            graph.as_scores(scorer(graph)), distance, apo.active_site, mode
                        )
                        columns[name] = np.array([values[r] for r in graph.order], dtype=float)

                    for cut in CONFIG["consensus_cut"]:
                        members = diverse_members(columns, float(cut))
                        blended = postprocess.consensus(
                            *[
                                dict(zip(graph.order, columns[name].tolist(), strict=True))
                                for name in members
                            ]
                        )
                        aligned = postprocess.consensus(
                            *[
                                dict(zip(graph.order, row.tolist(), strict=True))
                                for row in oriented(columns, members)
                            ]
                        )
                        for orient, base in (("none", blended), ("pc1", aligned)):
                            for radius in CONFIG["smoothing_radius"]:
                                scores = (
                                    base
                                    if radius == 0
                                    else postprocess.spatial_smoothing(
                                        base, coord, radius=float(radius)
                                    )
                                )
                                key = f"{arm}|{graph_name}|{mode}|cut{cut}|smooth{radius}"
                                if orient != "none":
                                    key += f"|{orient}"
                                if key in done:
                                    continue
                                record = score_arm(
                                    arm,
                                    scores,
                                    method=(
                                        f"consensus[{graph_name}][{mode}]"
                                        f"[cut{cut}][r{radius}][{orient}]"
                                    ),
                                    against=reference,
                                )
                                emit(
                                    record,
                                    key,
                                    arm=arm,
                                    graph=graph_name,
                                    detrend=mode,
                                    consensus_cut=float(cut),
                                    smoothing_radius=float(radius),
                                    orient=orient,
                                    n_members=len(members),
                                    members=members,
                                    assembly="top5",
                                )
                    # Pass 3. The assembly rule changes only the five residues at the top,
                    # so it is applied as a score transform: the diversified five are lifted
                    # above every other residue, keeping their order among themselves.
                    default_cut = float(CONFIG["consensus_cut"][1])
                    members = diverse_members(columns, default_cut)
                    blended = postprocess.consensus(
                        *[
                            dict(zip(graph.order, columns[name].tolist(), strict=True))
                            for name in members
                        ]
                    )
                    for exclusion in CONFIG["exclusion_radius"]:
                        if exclusion == 0:
                            continue
                        key = f"{arm}|{graph_name}|{mode}|assembly{exclusion}"
                        if key in done:
                            continue
                        chosen = postprocess.diversified_top_k(
                            blended,
                            coord,
                            k=5,
                            exclusion_radius=float(exclusion),
                            exclude=graph.source,
                        )
                        top = max(blended.values())
                        lifted = dict(blended)
                        for rank, residue in enumerate(chosen):
                            lifted[residue] = top + len(chosen) - rank
                        record = score_arm(
                            arm,
                            lifted,
                            method=f"consensus[{graph_name}][{mode}][diversified{exclusion}]",
                            against=reference,
                        )
                        emit(
                            record,
                            key,
                            arm=arm,
                            graph=graph_name,
                            detrend=mode,
                            consensus_cut=default_cut,
                            smoothing_radius=0.0,
                            n_members=len(members),
                            members=members,
                            orient="none",
                            assembly=f"diversified{exclusion}",
                        )

                print(f"{arm}/{graph_name}: {time.time() - started:.0f}s", flush=True)

    rows = [json.loads(line) for line in RECORDS.read_text().splitlines() if line.strip()]
    (HERE / "metrics.json").write_text(json.dumps(summarise(rows), indent=2, default=str) + "\n")
    print(f"{len(rows)} records, {time.time() - started:.0f}s")
    return 0


def summarise(rows: list[dict]) -> dict:
    by_variant: dict[str, list[dict]] = {}
    for row in rows:
        label = (
            f"{row['graph']}|{row['detrend']}|cut{row['consensus_cut']}"
            f"|r{row['smoothing_radius']}|{row.get('orient', 'none')}|{row['assembly']}"
        )
        by_variant.setdefault(label, []).append(row)

    table = []
    for label, group in sorted(by_variant.items()):
        graph_name, mode, cut, radius, orient, assembly = label.split("|")
        table.append(
            {
                "graph": graph_name,
                "detrend": mode,
                "consensus_cut": cut,
                "smoothing_radius": radius,
                "orient": orient,
                "assembly": assembly,
                "n_arms": len(group),
                "mean_members": round(float(np.mean([r["n_members"] for r in group])), 1),
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
