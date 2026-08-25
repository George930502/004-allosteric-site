"""The one scoring path. Every method -- classical, quantum, AI, hybrid -- goes through it.

A method hands in a score per candidate residue and gets back a record. It never sees the
label set, and it cannot choose an estimator, a tie rule, a null or a replicate count: all
of those come from the frozen evaluation manifest. That is the whole point. A quantum
number that beats a classical number computed differently is not evidence
(`docs/playbooks/experiment.md`).

This module is evaluation-side. It reads the answer key, so no prediction module may
import it (`tests/test_no_leakage.py`).
"""

from __future__ import annotations

import json
from collections.abc import Mapping
from pathlib import Path

import numpy as np
from scipy.stats import norm, spearmanr

from allo.benchmark import deep_diff
from allo.groundtruth.manifest import read_manifest
from allo.inputs import ROOT, apo_input
from allo.scoring import metrics, properties
from allo.scoring.nulls import (
    EvaluationGraph,
    evaluation_graph,
    matched_patches,
    permutation_p,
)

EVALUATION = ROOT / "docs" / "benchmark" / "evaluation"
EVALUATION_MANIFEST = EVALUATION / "manifest.yaml"
EVALUATION_FROZEN = EVALUATION / "frozen.json"
INPUT_FROZEN = ROOT / "docs" / "benchmark" / "primary" / "frozen.json"
SECONDARY_INPUT_FROZEN = ROOT / "docs" / "benchmark" / "secondary" / "frozen.json"

__all__ = [
    "calibrated_p",
    "compare_methods",
    "freeze_evaluation",
    "holm",
    "protocol",
    "score_arm",
    "verify_evaluation",
]


def protocol(path: Path = EVALUATION_MANIFEST) -> dict:
    """The frozen evaluation manifest, read verbatim.

    Unlike the input manifest there is no redaction, because there is no prediction-side
    reader: this file is evaluation-only by placement, and `tests/test_no_leakage.py`
    protects the directory.
    """
    return read_manifest(path)


def _positives(target: str) -> tuple[list[int], int]:
    for path in (INPUT_FROZEN, SECONDARY_INPUT_FROZEN):
        if not path.exists():
            continue
        frozen = json.loads(path.read_text())["targets"]
        if target in frozen:
            record = frozen[target]
            return list(record["scoreable_label_residues"]), int(record["n_candidates"])
    raise KeyError(f"{target!r} is not a frozen target")


def _spearman(left: np.ndarray, right: np.ndarray) -> float | None:
    """Spearman rho, or `None` where it is undefined rather than `nan`.

    A method that scores every candidate alike has no rank correlation with anything. SciPy
    returns `nan` and warns; `nan` is not valid JSON, so the record would be unreadable. The
    honest value is "undefined", which is what the conservation column already reads.
    """
    if len(np.unique(left)) < 2 or len(np.unique(right)) < 2:
        return None
    return round(float(spearmanr(left, right).statistic), 4)


def _aligned(graph: EvaluationGraph, scores: Mapping[int, float]) -> np.ndarray:
    """Score vector over the candidate set, in `graph.candidates` order.

    A method must score every candidate. Filling a gap with a constant would make the
    missing residues rank identically and quietly change the AUC, so this refuses instead.
    """
    missing = sorted(set(graph.candidates) - set(scores))
    if missing:
        raise ValueError(f"{graph.target}: no score for candidate residues {missing}")
    extra = sorted(set(scores) - set(graph.order))
    if extra:
        raise ValueError(f"{graph.target}: scores given for non-node residues {extra}")
    return np.array([float(scores[r]) for r in graph.candidates])


def _gate(target: str, settings: dict) -> dict:
    """The arm's calibration record, read from the committed calibration experiment.

    Matching size, components, burial and compactness is not enough on every arm. Radius of
    gyration is the second moment of the patch about its centroid, and what actually sets
    the variance of a patch mean under a spatially autocorrelated score is the whole
    within-patch distance distribution. The residual shows up as a measured type-I rate of
    0.059-0.075 on the two BCR-ABL1 arms and 0.034-0.037 on cardiac myosin, against a
    nominal 0.05. No moment tested closes it, and matching the variance factor itself is
    impossible in advance because it depends on the *method's* correlation length.

    So the threshold is calibrated instead of the null being matched further. `size_ratio`
    is the factor by which the observed statistic's null is wider than the pool members',
    taken as the maximum across correlation lengths and across every Holm level, and
    floored at 1. Calibration may tighten a test and may never loosen one. `alpha_star` is
    reported beside it for disclosure: it is the nominal p at which the measured size is
    alpha, and it is what the earlier linear rescale used.

    Four repairs to the matching have now been tested and none closes the residual: the two
    in ADR 0023, plus centring the patch pool on the observed radius of gyration and
    matching the whole within-patch pairwise-distance distribution (ADR 0025).
    """
    path = ROOT / str(settings["nulls"]["matched_patch"]["calibrated_by"]) / "metrics.json"
    gate = json.loads(path.read_text())["gate"]
    if target not in gate:
        raise KeyError(f"{target!r} has no calibrated threshold in {path}")
    return gate[target]


def calibrated_p(p: float, ratio: float) -> float:
    """`p` rescaled so the test holds its size at **every** Holm threshold, not only at alpha.

    The draft used the linear rescale `p * alpha / alpha_star`. It is exact at `alpha` and
    wrong everywhere else, because the null's tail is convex: at Holm's tighter steps a
    linearly rescaled test runs above nominal on the confirmatory arms, and the composed
    procedure is then not FWER-controlled (ADR 0025).

    The model is one parameter and needs no new kind of measurement. The observed
    statistic's null has standard deviation `ratio` times the pool members', so rescaling
    on the probit scale undoes it. What changed is where `ratio` is fitted: at every level
    Holm can present, `alpha/3 ... alpha`, taking the maximum. Fitting at `alpha` alone left
    the size above nominal at `alpha/3`; the maximum is conservative at all three by
    construction, because the rescale is conservative at level `t` exactly when
    `ratio >= z(q_t) / z(t)`.

    `ratio >= 1` by that construction. Above `p = 0.5` the rescale would nonetheless
    *lower* p -- correctly, under the model, because a wider null puts less mass above a
    point that already sits below the null mean -- so it is clamped. The clamp costs
    nothing: no threshold a decision ever uses lies above 0.5, exactness below 0.5 is
    untouched, and the composite stays monotone in `p`, which is what Holm needs. What it
    buys is that "calibration may tighten and may never loosen" holds as written.
    """
    ratio = max(float(ratio), 1.0)
    return float(min(1.0, max(p, norm.sf(norm.isf(p) / ratio))))


def _patch_null(graph, labels, settings, *, match_distance: bool):
    matched = settings["nulls"]["matched_patch"]
    replicates = int(
        settings["nulls"]["matched_patch_distance"]["replicates"]
        if match_distance
        else settings["nulls"]["replicates"]
    )
    patches, diagnostics = matched_patches(
        graph,
        labels,
        n_patches=replicates,
        tolerance=float(matched["tolerance"]),
        seed=int(settings["seed"]),
        match_distance=match_distance,
    )
    over_candidates = patches[:, graph.index(graph.candidates)].astype(np.float32)
    return over_candidates, diagnostics


def score_arm(
    target: str,
    scores: Mapping[int, float],
    *,
    method: str,
    against: Mapping[str, Mapping[int, float]] | None = None,
    config: dict | None = None,
) -> dict:
    """Score one method on one frozen arm under the frozen protocol.

    `scores` maps residue author number to a score, higher meaning more allosteric. Scores
    for source residues are accepted and ignored -- they leave both classes (ADR 0011).

    `against` optionally supplies baseline rankings for the same arm. Each gets a Spearman
    rank correlation against the method. This is not decoration: the only published quantum
    walk on protein residue networks reports "consistently strong agreement with classical
    eigenvector centrality" over about 150 proteins, per-protein Spearman rho running 0.582
    to 1.000, and declines the analysis that would separate the two
    (Mohtashim, Sajjan & Kais, JACS 2026;148(27):29206-29219, doi:10.1021/jacs.6c08053).
    A method that does not print this number has not answered the first question a reader
    of that paper will ask.
    """
    settings = config or protocol()
    frozen = json.loads(EVALUATION_FROZEN.read_text())["targets"][target]
    apo = apo_input(target)
    graph = evaluation_graph(apo)
    labels, n_candidates = _positives(target)
    if len(graph.candidates) != n_candidates:
        raise ValueError(
            f"{target}: evaluation graph has {len(graph.candidates)} candidates, freeze says "
            f"{n_candidates}"
        )
    values = _aligned(graph, scores)
    positive = np.array([r in set(labels) for r in graph.candidates], dtype=bool)
    k = int(settings["endpoints"]["top_k"])
    replicates = int(settings["nulls"]["replicates"])
    rng = np.random.default_rng(int(settings["seed"]))

    # The confirmatory statistic: the mean midrank of the scoreable label set. Computed on
    # the same float32 ranks the nulls use, so the observed value and its null share a
    # summation precision -- see the patch-size assert below for why that is exact.
    ranks = metrics.rank_vector(values).astype(np.float32)
    if int(positive.sum()) != len(labels):
        raise ValueError(
            f"{target}: {int(positive.sum())} positives found, freeze says {len(labels)}"
        )
    observed = float(ranks[positive].mean())

    # Null (a) as CHALLENGE.md section 4.1 words it: random background residues. Reported
    # because the challenge asks for it, and labelled anti-conservative because label sets
    # are contiguous patches and this null's replicates are not.
    background = np.array([rng.permutation(ranks)[: len(labels)].mean() for _ in range(replicates)])
    # Null (a) in the form that holds its size, and the same null with distance to the
    # propagation source added -- "distance bias" is this sub-field's published name for
    # the confound (doi:10.1093/nar/gkab350).
    geometry, diagnostics = _patch_null(graph, labels, settings, match_distance=False)
    distance, distance_diagnostics = _patch_null(graph, labels, settings, match_distance=True)

    # Null (b): non-functional surface pockets. One p-value per decoy pocket lining, so the
    # comparison is patch against patch with no synthetic sampling at all.
    decoy_linings = [p["lining"] for p in frozen["decoys"]["pockets"].values()]
    at = {residue: i for i, residue in enumerate(graph.candidates)}
    decoy_ranks = np.array([ranks[[at[r] for r in lining]].mean() for lining in decoy_linings])
    # Derived, not stored: the union of the decoy linings was 2064 lines of `frozen.json`
    # -- 30 % of the file -- carrying no information the linings do not already carry.
    decoy_residues = {r for lining in decoy_linings for r in lining}
    decoy_mask = np.array([r in decoy_residues for r in graph.candidates], dtype=bool)

    # The field's own convention, and the one number in this record a reader can put beside
    # PASSer, APOP or DeepAllo: rank every detected pocket by the mean midrank of its lining
    # and report where the site pocket lands. APOP states the convention as "If this pocket
    # is among the top-ranked three predicted pockets, we count it as a success"
    # (doi:10.1093/bioinformatics/btad275). Ties take the pessimistic rank, so a method that
    # scores every pocket equally reports last place rather than first.
    site_lining = frozen["decoys"]["site_pocket"]["lining"]
    site_pocket_rank = None
    if site_lining:
        site_score = float(ranks[[at[r] for r in site_lining]].mean())
        site_pocket_rank = 1 + int((decoy_ranks >= site_score).sum())

    gate = _gate(target, settings)
    # Every matched patch holds exactly `len(labels)` residues, so every row of the matmul
    # divides by the same constant. That is what makes the float32 accumulation safe: the
    # comparison in `permutation_p` is order-preserving under it. Assert the invariant
    # rather than rely on it silently.
    patch_sizes = geometry.sum(1)
    if not np.all(patch_sizes == len(labels)):
        raise ValueError(f"{target}: matched patches are not all size {len(labels)}")
    matched_p = permutation_p(observed, (geometry @ ranks) / patch_sizes)

    record = {
        "target": target,
        "method": method,
        "protocol_frozen_on": str(settings["frozen_on"]),
        "n_candidates": n_candidates,
        "n_positive": len(labels),
        "prevalence": round(len(labels) / n_candidates, 6),
        "endpoints": {
            "mean_rank": round(observed, 4),
            "auc_roc": round(metrics.auc_roc(values, positive), 4),
            "auc_pr": round(metrics.auc_pr(values, positive), 4),
            f"precision_at_{k}": round(metrics.precision_at_k(values, positive, k), 4),
            f"hits_at_{k}": int(round(metrics.precision_at_k(values, positive, k) * k)),
            # One division from hits@k, and the number this field reads first. Of 22 tools
            # surveyed, 17 report a recall-style top-N success rate and none reports
            # precision@k alone. Printed because a reader will otherwise compute it.
            f"recall_at_{k}": round(
                metrics.precision_at_k(values, positive, k) * k / len(labels), 4
            ),
            # The one published criterion built for a residue list rather than a pocket.
            # A distance, not a success rate: the 4 A threshold is contested for
            # centre-to-centre use, so both conventions print beside it (ADR 0025).
            "dcc_angstrom": round(
                metrics.dcc(
                    graph.ca_coord[graph.index(graph.candidates)],
                    metrics.top_k_indices(values, positive, k),
                    positive,
                ),
                3,
            ),
            "auc_roc_vs_decoy_linings": (
                round(
                    metrics.auc_roc(values[positive | decoy_mask], positive[positive | decoy_mask]),
                    4,
                )
                if decoy_mask.any()
                else None
            ),
        },
        "chance": frozen["chance"],
        "nulls": {
            "background_residues": {
                "p": permutation_p(observed, background),
                "replicates": replicates,
                "caveat": "anti-conservative: replicates are not contiguous patches",
            },
            "matched_patch": {
                "p": matched_p,
                # The number the decision uses, and the number Holm runs on. Calibrated at
                # every Holm level rather than only at alpha, which is what the linear
                # rescale of the draft was and why the composed procedure leaked FWER.
                "p_calibrated": round(calibrated_p(matched_p, gate["size_ratio"]), 6),
                "size_ratio": gate["size_ratio"],
                "alpha_star": gate["alpha_star"],
                "replicates": replicates,
                "confirmatory": True,
                "diagnostics": diagnostics,
            },
            "matched_patch_distance": {
                "p": permutation_p(observed, (distance @ ranks) / distance.sum(1)),
                "replicates": distance.shape[0],
                "confirmatory": False,
                "diagnostics": distance_diagnostics,
            },
            "decoy_pockets": {
                "p": permutation_p(observed, decoy_ranks) if len(decoy_ranks) else None,
                "n_decoys": len(decoy_ranks),
                "minimum_attainable_p": frozen["decoys"]["minimum_attainable_p"],
                # Pocket-level, reported never tested. It shares its p-value with the row
                # above, and the detector -- not the method -- fixes how many pockets there
                # are, so it cannot carry a decision. It exists for comparability.
                "site_pocket_rank": site_pocket_rank,
                "n_pockets_ranked": len(decoy_ranks) + (1 if site_lining else 0),
                "site_pocket_label_coverage": frozen["decoys"]["site_pocket"]["label_coverage"],
            },
        },
    }
    # The four confounders every propagation score is read against. Three are computable
    # from the apo structure alone; conservation needs an external alignment and is absent,
    # recorded as unknown rather than approximated (ADR 0025).
    record["confounders"] = {
        name: _spearman(values, _aligned(graph, column))
        for name, column in properties.residue_properties(apo).items()
    }
    record["confounders"]["conservation"] = None

    if against:
        record["rank_correlation"] = {
            name: _spearman(values, _aligned(graph, baseline)) for name, baseline in against.items()
        }
    return record


def holm(pvalues: Mapping[str, float], alpha: float = 0.05) -> dict[str, dict]:
    """Holm-Bonferroni over a declared family. Step-down, so it is uniformly more powerful
    than Bonferroni and needs no independence assumption -- which matters here, because two
    arms of the same disease area are not independent.
    """
    ordered = sorted(pvalues.items(), key=lambda kv: kv[1])
    m = len(ordered)
    verdict: dict[str, dict] = {}
    still_rejecting = True
    for i, (name, p) in enumerate(ordered):
        threshold = alpha / (m - i)
        still_rejecting = still_rejecting and p <= threshold
        verdict[name] = {"p": p, "threshold": round(threshold, 6), "reject": still_rejecting}
    return verdict


def _derive_arm(target: str, settings: dict, *, detect: bool) -> dict:
    """Everything the evaluation layer pins for one arm, re-derived from the frozen files."""
    from allo.scoring import decoys as decoy_module

    graph = evaluation_graph(apo_input(target))
    labels, n_candidates = _positives(target)
    k = int(settings["endpoints"]["top_k"])
    matched = settings["nulls"]["matched_patch"]
    _, diagnostics = matched_patches(
        graph,
        labels,
        n_patches=int(matched["freeze_probe_patches"]),
        tolerance=float(matched["tolerance"]),
        seed=int(settings["seed"]),
    )
    record = {
        "n_candidates": n_candidates,
        "n_positive": len(labels),
        "prevalence": round(len(labels) / n_candidates, 6),
        "chance": {
            f"precision_at_{k}": round(
                metrics.expected_precision_at_k(len(labels), n_candidates, k), 6
            ),
            # Under a uniform draw of k residues the expected number of hits is k * L / N,
            # so expected recall is k / N and does not depend on the label-set size.
            f"recall_at_{k}": round(k / n_candidates, 6),
            # No closed form for a distance, so a seeded Monte Carlo median, frozen per arm.
            "dcc_angstrom": round(
                metrics.chance_dcc(
                    graph.ca_coord[graph.index(graph.candidates)],
                    np.array([r in set(labels) for r in graph.candidates], dtype=bool),
                    k,
                    seed=int(settings["seed"]),
                ),
                3,
            ),
            f"p_at_least_one_hit_at_{k}": round(
                metrics.p_at_least_one_hit(len(labels), n_candidates, k), 6
            ),
        },
        "matched_patch": {
            "size_ratio": _gate(target, settings)["size_ratio"],
            "alpha_star": _gate(target, settings)["alpha_star"],
            "components": diagnostics["observed_components"],
            "mean_degree": diagnostics["observed_mean_degree"],
            "radius_of_gyration": diagnostics["observed_radius_of_gyration"],
            "median_distance_to_source": diagnostics["observed_median_distance_to_source"],
            "acceptance_rate": diagnostics["acceptance_rate"],
        },
    }
    if not detect:
        return record
    ca = {r: graph.ca_coord[graph.position[r]] for r in graph.order}
    detected = decoy_module.detect_pockets(
        apo_input(target), **settings["decoys"]["detector_settings"]
    )
    split = decoy_module.classify(
        detected,
        labels=labels,
        candidates=graph.candidates,
        ca_coord=ca,
        halo_angstrom=float(settings["decoys"]["halo_angstrom"]),
    )
    record["decoys"] = {
        "n_detected": split["n_detected"],
        "n_scoreable": split["n_scoreable"],
        "site_pocket": split["site_pocket"],
        "pockets": split["decoys"],
        "excluded_by_halo": sorted(split["excluded_by_halo"]),
        "minimum_attainable_p": split["minimum_attainable_p"],
    }
    return record


def compare_methods(
    target: str,
    scores: Mapping[int, float],
    against: Mapping[int, float],
    *,
    names: tuple[str, str] = ("method", "baseline"),
    config: dict | None = None,
) -> dict:
    """Paired test: does one score rank the label set higher than another, on the same arm?

    `manifest.yaml` requires a method to beat its classical baselines, and until this existed
    the protocol defined no test for "beat". A comparison rule chosen after seeing which
    method won is a hyperparameter, exactly like a threshold, so it is frozen here before any
    method exists (ADR 0025).

    **Paired on the residue, and geometry-matched like everything else.** Take the difference
    of the two midrank vectors, `d = rank(scores) - rank(against)`, and ask whether its mean
    over the label patch is extreme against its mean over the same matched-patch pool the
    confirmatory test uses. Both methods see the identical pool, so a difference between them
    cannot be sampler noise. Pairing removes every property of the arm that acts on both
    scores alike -- size, prevalence, patch compactness -- which is why it is far more
    sensitive than comparing two separate p-values.

    **Two-sided, unlike the confirmatory test, and deliberately.** The confirmatory test is
    one-sided because a method ranking allosteric residues below background is broken rather
    than competing. Here there is no such asymmetry: the question is which of two scores is
    better, and a prior on the answer would be exactly the bias this protocol exists to
    prevent. The null is centred on its own median before the tails are counted, because the
    pool's patch means need not be centred at zero.

    The arm's `size_ratio` is applied unchanged. It was calibrated for a single score's field
    and the difference of two fields has its own autocorrelation, so this is an approximation
    -- but it only ever tightens, so the direction is the safe one.
    """
    settings = config or protocol()
    apo = apo_input(target)
    graph = evaluation_graph(apo)
    labels, _ = _positives(target)
    positive = np.array([r in set(labels) for r in graph.candidates], dtype=bool)

    left, right = _aligned(graph, scores), _aligned(graph, against)
    delta = (metrics.rank_vector(left) - metrics.rank_vector(right)).astype(np.float32)
    observed = float(delta[positive].mean())

    geometry, diagnostics = _patch_null(graph, labels, settings, match_distance=False)
    null = (geometry @ delta) / geometry.sum(1)
    centre = float(np.median(null))
    extreme = int((np.abs(null - centre) >= abs(observed - centre)).sum())
    raw = (1 + extreme) / (1 + len(null))
    ratio = _gate(target, settings)["size_ratio"]

    return {
        "target": target,
        "comparison": f"{names[0]} against {names[1]}",
        "mean_rank_difference": round(observed, 4),
        "auc_roc_difference": round(
            metrics.auc_roc(left, positive) - metrics.auc_roc(right, positive), 4
        ),
        "leader": names[0] if observed > centre else names[1],
        "p": round(raw, 6),
        "p_calibrated": round(calibrated_p(raw, ratio), 6),
        "size_ratio": ratio,
        "sided": "two",
        "replicates": int(geometry.shape[0]),
        "null_centre": round(centre, 4),
        "diagnostics": diagnostics,
    }


def freeze_evaluation(settings: dict | None = None) -> dict:
    """Derive everything the evaluation layer pins, for every frozen arm.

    Needs the `eval` extra, because deriving the decoy pockets runs the detector. Scoring
    does not: it reads the committed result.
    """
    settings = settings or protocol()
    targets = sorted(json.loads(INPUT_FROZEN.read_text())["targets"])
    if SECONDARY_INPUT_FROZEN.exists():
        targets += sorted(json.loads(SECONDARY_INPUT_FROZEN.read_text())["targets"])
    return {
        "frozen_on": str(settings["frozen_on"]),
        "protocol_version": settings["version"],
        "targets": {t: _derive_arm(t, settings, detect=True) for t in targets},
    }


def verify_evaluation(detect: bool = False) -> list[str]:
    """Differences between the recorded evaluation freeze and what re-derives today.

    `detect=False` is the offline check: it re-derives the chance lines and the matched-patch
    geometry from the committed apo bytes and skips the pockets, so `make check` stays
    offline and free of the `eval` extra. `make verify` runs it with `detect=True`.
    """
    settings = protocol()
    frozen = json.loads(EVALUATION_FROZEN.read_text())
    problems: list[str] = []
    if str(frozen["frozen_on"]) != str(settings["frozen_on"]):
        problems.append(
            f"frozen_on: freeze {frozen['frozen_on']} != manifest {settings['frozen_on']}"
        )
    for target, recorded in frozen["targets"].items():
        current = _derive_arm(target, settings, detect=detect)
        if not detect:
            recorded = {key: value for key, value in recorded.items() if key != "decoys"}
        deep_diff(recorded, current, target, problems)
    return problems
