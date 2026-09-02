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

import hashlib
import json
from collections.abc import Iterator, Mapping
from pathlib import Path

import numpy as np
from scipy.stats import chi2, norm, spearmanr

from allo.benchmark import deep_diff
from allo.groundtruth.manifest import read_manifest
from allo.inputs import ROOT, apo_input
from allo.scoring import metrics
from allo.scoring.nulls import (
    EvaluationGraph,
    MatchedPoolUnavailable,
    evaluation_graph,
    matched_patches,
    permutation_p,
)
from allo.structure import properties

EVALUATION = ROOT / "docs" / "benchmark" / "evaluation"
EVALUATION_MANIFEST = EVALUATION / "manifest.yaml"
EVALUATION_FROZEN = EVALUATION / "frozen.json"
INPUT_FROZEN = ROOT / "docs" / "benchmark" / "primary" / "frozen.json"
SECONDARY_INPUT_FROZEN = ROOT / "docs" / "benchmark" / "secondary" / "frozen.json"

__all__ = [
    "calibrated_p",
    "combine_arms",
    "compare_methods",
    "freeze_evaluation",
    "holm",
    "protocol",
    "score_arm",
    "top_k_components",
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


def _require_unseal(target: str, unseal: str | None) -> None:
    """The `generalisation` seal. Every PUBLIC scoring entry point calls this, and one test
    pins that set so a new entry point cannot forget.

    It is NOT in `_positives`, though that is the shared read. Calibration and the size
    simulation legitimately read every arm's labels -- the August calibration derived the
    per-arm thresholds for all fifteen -- and ADR 0041 records that the seal covers SCORING
    rather than reading. Putting the check on the read would break the freeze it protects.

    Added 2026-09-03. The guard was written inside `score_arm` and `compare_methods` was
    exported beside it with no check at all, so a caller could score a sealed arm through the
    paired test and get a complete record. That is the same shape as every other guard defect
    in this repository: the rule was placed in one caller instead of at the boundary.
    """
    if _tier(target) == "generalisation" and unseal != "phase-5":
        raise PermissionError(
            f"{target} is in the sealed `generalisation` tier. It carries the generalisability "
            "claim and is not scored until the method is frozen (Phase 5, ADR 0021). Pass "
            'unseal="phase-5" to score it, and say in the run notes why the method is frozen.'
        )


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
    try:
        patches, diagnostics = matched_patches(
            graph,
            labels,
            n_patches=replicates,
            tolerance=float(matched["tolerance"]),
            seed=int(settings["seed"]),
            match_distance=match_distance,
        )
    except MatchedPoolUnavailable as unavailable:
        # The pool is a property of the graph, not of the method. An arm whose graph
        # cannot supply one at the frozen tolerance is reported without this null, with the
        # failure printed. Widening the tolerance for the one arm that failed is the
        # per-arm hyperparameter the frozen protocol exists to prevent.
        return None, unavailable.diagnostics()
    over_candidates = patches[:, graph.index(graph.candidates)].astype(np.float32)
    return over_candidates, diagnostics


def score_arm(
    target: str,
    scores: Mapping[int, float],
    *,
    method: str,
    against: Mapping[str, Mapping[int, float]] | None = None,
    config: dict | None = None,
    unseal: str | None = None,
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

    `unseal` must be `"phase-5"` to score an arm in the secondary set's `generalisation`
    tier. That tier carries the generalisability claim and is not opened until the method is
    frozen, and until 2026-09-03 the rule lived only in a manifest comment. ADR 0041 makes it
    a check, on the argument the file-read routes are enforced on: a rule a document states
    and no test holds is a promise, and this one was broken in 23 tracked files before it was
    a day old. What the seal can still protect is scoring, so scoring is what is guarded.
    """
    _require_unseal(target, unseal)
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
    site_score = None
    if site_lining:
        site_score = float(ranks[[at[r] for r in site_lining]].mean())
        site_pocket_rank = 1 + int((decoy_ranks >= site_score).sum())

    # The same permutation with the LABEL SET as the positive, added at v4 by ADR 0039. It
    # answers the question the deliverable is about -- do the allosteric residues outrank
    # non-functional pockets -- which the site-lining statistic above cannot: a method that
    # ranks every myosin label perfectly still moves a 295-residue lining mean by only the
    # label fraction of the effect, and the measured power of a delta = 4 shift is 0 on kras and
    # on myosin. On the same instrument this statistic reaches 0.87 and 1.00.
    label_score = float(ranks[[at[r] for r in labels]].mean()) if labels else None

    if geometry is None:
        # No pool, so no calibrated threshold either: `alpha_star` and `size_ratio` are
        # measured *from* the pool. The arm reports the failure and cannot be confirmatory.
        matched_record = {
            "available": False,
            "p": None,
            "p_calibrated": None,
            "size_ratio": None,
            "alpha_star": None,
            "replicates": 0,
            "confirmatory": False,
            "diagnostics": diagnostics,
        }
    else:
        gate = _gate(target, settings)
        # Every matched patch holds exactly `len(labels)` residues, so every row of the
        # matmul divides by the same constant. That is what makes the float32 accumulation
        # safe: the comparison in `permutation_p` is order-preserving under it. Assert the
        # invariant rather than rely on it silently.
        patch_sizes = geometry.sum(1)
        if not np.all(patch_sizes == len(labels)):
            raise ValueError(f"{target}: matched patches are not all size {len(labels)}")
        matched_p = permutation_p(observed, (geometry @ ranks) / patch_sizes)
        matched_record = {
            "available": True,
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
        }

    # `config` exists so that a test can run a 199-replicate protocol, and until 2026-09-03
    # the record it produced was stamped with the frozen date and said nothing else. A
    # top-1, 199-replicate calculation could therefore identify itself as the frozen
    # protocol. Round 6. The record now says which top-level sections it ran under that the
    # frozen manifest does not have, so a reader never has to trust the date alone.
    frozen_settings = protocol()
    deviations = sorted(
        key
        for key in set(frozen_settings) | set(settings)
        if frozen_settings.get(key) != settings.get(key)
    )

    record = {
        "target": target,
        "method": method,
        "protocol_frozen_on": str(settings["frozen_on"]),
        "protocol_is_frozen": not deviations,
        "protocol_deviations": deviations,
        "n_candidates": n_candidates,
        "n_positive": len(labels),
        "prevalence": round(len(labels) / n_candidates, 6),
        "endpoints": {
            "mean_rank": round(observed, 4),
            "auc_roc": round(metrics.auc_roc(values, positive), 4),
            "auc_pr": round(metrics.auc_pr(values, positive), 4),
            f"precision_at_{k}": round(metrics.precision_at_k(values, positive, k), 4),
            f"hits_at_{k}": int(round(metrics.precision_at_k(values, positive, k) * k)),
            # One division from hits@k. Printed because a reader will otherwise compute it,
            # and will compute it wrongly. CORRECTED 2026-09-03: this comment used to justify
            # it as a field convention, citing 17 of 22 surveyed tools reporting a
            # recall-style top-N rate. Review 07 of the 2026-09-02 audit shows that is a
            # category error. The field's top-N is a per-protein binary -- did the true
            # pocket land in the top three of the pockets a detector found -- while this is
            # the fraction of a multi-residue label set recovered in k picks. Different
            # quantities, different chance lines. The reason to print it is that it is one
            # division away, not that the field reports the same thing.
            f"recall_at_{k}": round(
                metrics.precision_at_k(values, positive, k) * k / len(labels), 4
            ),
            # The one published criterion built for a residue list rather than a pocket.
            # A distance, not a success rate: the 4 A threshold is contested for
            # centre-to-centre use, so both conventions print beside it (ADR 0025).
            "dcc_angstrom": round(
                metrics.dcc(
                    graph.ca_coord[graph.index(graph.candidates)],
                    metrics.top_k_indices(values, k),
                    positive,
                ),
                3,
            ),
            # How many places the top-k list lands in. 1 is one site a chemist can design
            # against; k is scatter. CHALLENGE.md section 4.2 asks for actionable output and
            # nothing else here measures it. Reported, never tested (ADR 0030 disposition,
            # precedent doi:10.64898/2026.01.28.702257).
            f"top_{k}_components": top_k_components(graph, values, k),
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
            "matched_patch": matched_record,
            "matched_patch_distance": {
                "p": (
                    permutation_p(observed, (distance @ ranks) / distance.sum(1))
                    if distance is not None
                    else None
                ),
                "available": distance is not None,
                "replicates": 0 if distance is None else distance.shape[0],
                "confirmatory": False,
                "diagnostics": distance_diagnostics,
            },
            "decoy_pockets": {
                # ADR 0030 writes this test as `(1 + #{decoy_rank >= site_rank}) / (1 + n)`,
                # and the type-I simulation behind it drew the site's number from the same
                # unit-variance law as the decoys'. Both halves have to be a pocket lining
                # for that exchangeability to hold. Until 2026-09-02 the code passed the
                # label set's own mean midrank here instead, whose sampling variance goes as
                # 1/|labels| while a decoy's goes as 1/|lining| -- a statistic no type-I
                # rate in `decoy-typeI.json` was ever measured for.
                "p": (
                    permutation_p(site_score, decoy_ranks)
                    if len(decoy_ranks) and site_score is not None
                    else None
                ),
                # ADR 0039, protocol v4. A DESCRIPTIVE PERCENTILE, not a p-value: the rank
                # of the label set's mean midrank among the decoy linings' means. Reported
                # beside `p`, never in place of it. `p` is the ADR 0030 statistic and stays
                # exactly as review 25 section 1.4 left it.
                #
                # It exists because `p` cannot see the deliverable. `p` ranks the detector's
                # site-pocket lining, and a shift of four standard deviations on every label
                # residue leaves its power at 0 on kras and on cardiac myosin: the myosin
                # labels sit inside a 295-residue lining, so they move that mean by only a
                # small fraction of the effect. This quantity reaches 0.875 and 1.000 on
                # the same fields.
                #
                # It carries NO rejection, and the reason is measured rather than cautious.
                # The two sides have different set sizes and are not exchangeable, so its size
                # is a property of the score field. Over four null generators in
                # `experiments/2026-09-03-endpoint-b/` it runs 0.0000 to 0.0548, and the worst
                # cell -- `bcr_abl1_corrected` under a blocky distance-monotone field, which is
                # the shape every distance-correlated baseline here has -- has a 95 % interval
                # of [0.0516, 0.0580], entirely above alpha. Quote it as "the label set
                # outranks N of M detected pockets" and never as a p-value. `allo.scoring.simulate`.
                "label_p": (
                    permutation_p(label_score, decoy_ranks)
                    if len(decoy_ranks) and label_score is not None
                    else None
                ),
                "n_decoys": len(decoy_ranks),
                "minimum_attainable_p": frozen["decoys"]["minimum_attainable_p"],
                # Pocket-level, reported never tested. It is the same quantity the p-value
                # above is built from -- `p` is exactly `site_pocket_rank / (1 + n_decoys)`
                # -- and the detector, not the method, fixes how many pockets there are, so
                # it cannot carry a decision. It exists for comparability.
                "site_pocket_rank": site_pocket_rank,
                "n_pockets_ranked": len(decoy_ranks) + (1 if site_lining else 0),
                "site_pocket_label_coverage": frozen["decoys"]["site_pocket"]["label_coverage"],
                # Per-arm, this is descriptive and cannot be otherwise. The statistic gives
                # one draw per pocket, so its power tends to 1 - Phi(z_(1-alpha) - delta) and
                # needs delta >= 2.49 for 80 % power at ANY decoy count. The tested form of
                # negative class (b) is `combine_arms` over the confirmatory family, which is
                # not floored. ADR 0030.
                "confirmatory": False,
                "tested_form": "combine_arms over the confirmatory family",
            },
        },
    }
    # The confounders every propagation score is read against. Three are computable from the
    # apo structure alone; conservation needs an external alignment and is absent, recorded
    # as unknown rather than approximated (ADR 0025, ADR 0035).
    record["confounders"] = {
        name: _spearman(values, _aligned(graph, column))
        for name, column in properties.residue_properties(apo).items()
    }
    record["confounders"]["conservation"] = None
    # Two more, added at protocol v3, and free: the evaluation graph already holds both. They
    # are here because they separate label from background about as strongly as the three
    # above -- degree reaches AUC 0.770 on `ns5b`, distance 0.932 on `hiv_rt` in its better
    # direction -- so "your hits are just the well-connected residues near the source" is an
    # objection the record has to be able to answer. Apo-only and label-free, so C1 and C2
    # are untouched. Reported, never tested.
    source_coord = graph.ca_coord[[graph.position[r] for r in graph.source]]
    gaps = graph.ca_coord[:, None, :] - source_coord[None, :, :]
    to_source = np.linalg.norm(gaps, axis=2).min(axis=1)
    on_candidates = graph.index(graph.candidates)
    record["confounders"]["degree"] = _spearman(values, graph.degree[on_candidates])
    record["confounders"]["distance_to_source"] = _spearman(values, to_source[on_candidates])

    # The manifest MANDATES a correlation against every baseline
    # (`secondary_objectives.classical_comparison.also_report`). The key used to be omitted
    # when no baselines were supplied, which made a non-conforming record indistinguishable
    # from a conforming one. It is always present now, and `None` says the caller supplied
    # nothing, so a reader of the record can tell. Found 2026-09-03.
    record["rank_correlation"] = (
        {name: _spearman(values, _aligned(graph, baseline)) for name, baseline in against.items()}
        if against
        else None
    )
    # And the manifest mandates NINE of them by name, so a record that carries one
    # correlation and a record that carries all nine were the same shape. Added 2026-09-03
    # after round 6 showed that `against={"degree": ...}` produces a conforming-looking
    # record. The key is always present and empty only when nothing is missing.
    required = set(settings["secondary_objectives"]["classical_comparison"]["required_baselines"])
    record["required_baselines_missing"] = sorted(required - set(against or {}))
    return record


def combine_arms(pvalues: Mapping[str, float], *, method: str = "fisher") -> dict:
    """Combine per-arm p-values across a declared family (ADR 0030).

    Negative class (b) -- non-functional surface pockets -- has no valid per-arm test. The
    pocket-rank statistic gives one draw per pocket, so its power tends to
    `1 - Phi(z_(1-alpha) - delta)` and needs a pocket-level effect of 2.49 standard
    deviations for 80 % power **at any decoy count**.

    CORRECTED 2026-09-02. 2.487 is the `n -> infinity` normal-quantile limit, not the power
    of the discrete rank test this code runs. Integrating the exact binomial mixture at
    alpha = 0.05 gives power 0.7173 at 19 decoys, 0.6530 at 31, 0.7718 at 84, 0.7888 at 139
    and only 0.7959 at 400 -- and rejection is impossible at 18 or fewer, where the floor
    exceeds alpha. The direction is that the test is WEAKER than 2.487 implies at every
    frozen decoy count, so the disclosed requirement understates the effect it needs.

    A residue-level replacement was
    measured at a type-I rate of 0.132-0.384, and a size-matched patch cannot be drawn
    inside the decoy union on either KRAS arm, where no decoy pocket is as large as the
    label set.

    A combination across arms is not floored, because Fisher and Stouffer are unbounded
    below even when every input is bounded. On the three confirmatory arms the minimum
    attainable p is 0.00137 by Fisher and 0.000453 by Stouffer at the v3 detector settings,
    against 0.0214 and 0.0115 at the v2 settings.

    **This tests the INTERSECTION null -- no arm has signal.** A rejection licenses "at
    least one arm distinguishes the site from non-functional surface pockets". It is not a
    generalisation claim, and it must be labelled that way wherever it is quoted.
    """
    # The manifest declares this combination `over: confirmatory_family`, and until
    # 2026-09-03 nothing enforced it: two arms, or three that are not the family, were
    # accepted without complaint while `confirmatory_verdict` next door checked its own.
    # A combination over a set chosen after seeing the numbers is a different test from the
    # one the protocol froze, so the family is checked here on the same argument.
    declared = sorted(protocol()["decision"]["confirmatory_family"])
    if sorted(pvalues) != declared:
        raise ValueError(
            f"combine_arms is declared over the confirmatory family, which is {declared}; "
            f"got {sorted(pvalues)}. Combining a set chosen after the fact is a different test"
        )
    names = sorted(pvalues)
    values = np.array([float(pvalues[n]) for n in names], dtype=float)
    if not values.size:
        raise ValueError("combine_arms needs at least one arm")
    if np.any((values <= 0) | (values > 1)):
        raise ValueError(f"p-values outside (0, 1]: {dict(zip(names, values, strict=True))}")
    if method == "fisher":
        statistic = float(-2 * np.log(values).sum())
        p = float(chi2.sf(statistic, 2 * values.size))
    elif method == "stouffer":
        statistic = float(norm.isf(values).sum() / np.sqrt(values.size))
        p = float(norm.sf(statistic))
    else:
        raise ValueError(f"unknown combination method {method!r}")
    return {
        "method": method,
        "arms": names,
        "p_per_arm": {n: float(pvalues[n]) for n in names},
        "statistic": round(statistic, 6),
        "p": round(p, 8),
        "tests": "intersection null: no arm has signal",
        "licenses": "at least one arm separates the site from non-functional surface pockets",
    }


def top_k_components(graph, values: np.ndarray, k: int) -> int:
    """How many connected pieces the top-k list breaks into, in the evaluation graph.

    `CHALLENGE.md` section 4.2 asks for actionable output. Five residues in one place are a
    pocket a chemist can design against; five residues in five places are not, and no
    endpoint in the protocol separated the two. Published precedent for the quantity is
    Seq2Pocket's Pocket Fragmentation Index (doi:10.64898/2026.01.28.702257), which
    "measures the average number of predicted clusters assigned to each ground-truth
    pocket", ideal 1.0. Ours is the component count directly: 1 is one site, k is scatter.

    Reported, never tested. It is a property of the hit list, not evidence about it.
    """
    chosen = [graph.candidates[i] for i in metrics.top_k_indices(values, k)]
    unseen, components = set(chosen), 0
    while unseen:
        stack, components = [unseen.pop()], components + 1
        while stack:
            for neighbour in graph.neighbours(stack.pop()) & unseen:
                unseen.discard(neighbour)
                stack.append(neighbour)
    return components


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


def confirmatory_verdict(
    family_1: Mapping[str, float],
    family_2: Mapping[str, Mapping] | None = None,
    *,
    settings: dict | None = None,
) -> dict:
    """Apply the frozen decision rule to one method's per-arm p-values.

    Until 2026-09-02 the manifest froze a decision rule that no code read. `decision.alpha`,
    `decision.confirmatory_family` and `decision.correction` had no reader anywhere in `src/`
    or `experiments/`, and `holm` had no caller outside the tests. The one Holm actually run
    in the repository was in an experiment runner that predates ADR 0032, and it corrected
    over the whole scorer battery *within* an arm -- a different family from the one the
    protocol declares. That runner left `main` with the method layer on 2026-09-02 and is on
    the branch `method-layer-archive` (ADR 0037). A frozen rule that every caller
    re-implements is not frozen, which is the same argument that makes `score_arm` the only
    scoring path.

    `family_1` is the matched-patch `p_calibrated` per arm, one-sided upper. `family_2` is
    the whole `compare_methods` record per arm, against `cavity_volume`, two-sided (ADR 0032).
    Both are corrected by Holm over three at the frozen alpha, and the arms supplied must be
    exactly the declared family -- passing four arms, or the wrong three, raises rather than
    silently correcting over the wrong m.

    **Family 2 takes records, not bare p-values, because the test is two-sided and the claim
    is directional.** ADR 0032's own table says a family-2 rejection licenses "the method
    beats the pre-declared reference on that arm". A two-sided p-value cannot say which
    method won, so the first implementation counted a method that was significantly WORSE
    than `cavity_volume` as clearing the claim family. Requiring the record makes the
    direction available: an arm rejects only when Holm rejects AND `leader` is not the
    reference. A record whose `comparison` is not against the frozen reference raises, so a
    caller cannot reverse the direction by swapping the two arguments of `compare_methods`.
    Found 2026-09-03 by an adversarial pass.

    **A family is cleared when Holm rejects at least one arm, and ADR 0038 is why.** Until
    2026-09-03 neither the ADR nor README section 8 said whether clearing meant one arm or all
    three, and the frozen layer held both readings in documents that cite each other: section
    8 and ADR 0030 read the combination test disjunctively, while `docs/ROADMAP.md` and
    section 13 read one-of-three as a failure. Choosing after seeing a result is the
    hyperparameter this layer exists to prevent, so the rule is frozen here.

    The disjunction is what Holm controls and what this function already computed. Its
    measured global-null familywise error is 0.0416 to 0.0457 against a nominal 0.05, and the
    closed form is 0.049171. The conjunction is an intersection-union test, which is level
    alpha with NO multiplicity step at all, so freezing Holm implies the disjunction was
    intended; run under Holm it spends 1 event in 20 000 at the global null while still
    reaching 0.04025 at its least-favourable configuration, and it costs 3.5 times the
    family-level power at a realistic effect. Neither reading protects an individual arm
    better: the chance that a null arm is rejected is 0.0408 to 0.0457 either way, which is a
    property of Holm.

    The licence is per arm and is printed per arm. "Rejects on all three" is a separate,
    optional consistency statement that carries no extra protection, and a generalisation
    claim needs the secondary `generalisation` tier rather than a conjunction of three.
    """
    settings = settings or protocol()
    decision = settings["decision"]
    alpha = float(decision["alpha"])
    if decision["correction"] != "holm":
        raise ValueError(f"unsupported correction {decision['correction']!r}")

    def _check(supplied: Mapping[str, float], declared: list[str], label: str) -> dict:
        if set(supplied) != set(declared):
            raise ValueError(f"{label} must be exactly {sorted(declared)}; got {sorted(supplied)}")
        return holm(supplied, alpha=alpha)

    verdict = {
        "alpha": alpha,
        "correction": "holm",
        "family_1": {
            "test": "matched_patch",
            "sided": decision["sided"],
            "arms": _check(family_1, list(decision["confirmatory_family"]), "family_1"),
        },
    }
    verdict["family_1"]["n_reject"] = sum(a["reject"] for a in verdict["family_1"]["arms"].values())
    verdict["family_1"]["cleared"] = verdict["family_1"]["n_reject"] >= 1
    if family_2 is None:
        # ADR 0038 requires BOTH families, so a verdict without family 2 is not cleared. It
        # used to omit the field, which left a caller unable to tell "not cleared" from a
        # record written before the field existed. Absent is not the same as unmet.
        verdict["cleared"] = False
        verdict["licence"] = (
            "no claim: the claim family was not supplied, and ADR 0038 requires both families"
        )
        return verdict
    claim = decision["claim_family"]
    reference = str(claim["reference"])
    leads: dict[str, bool] = {}
    pvalues: dict[str, float] = {}
    for arm, record in family_2.items():
        if not isinstance(record, Mapping) or "leader" not in record:
            raise TypeError(
                f"family_2[{arm!r}] must be a compare_methods record, not a bare p-value: "
                "a two-sided p cannot say which method won, and ADR 0032 licenses "
                f"'the method beats {reference}'"
            )
        comparison = str(record.get("comparison", ""))
        if not comparison.endswith(f" against {reference}"):
            raise ValueError(
                f"family_2[{arm!r}] compares {comparison!r}; the frozen reference is "
                f"{reference!r} and it must be the second argument to compare_methods"
            )
        pvalues[arm] = float(record["p_calibrated"])
        leads[arm] = str(record["leader"]) != reference
    arms = _check(pvalues, list(claim["arms"]), "family_2")
    for arm, outcome in arms.items():
        # Holm rejects a two-sided test in either direction. Only one of them is the claim.
        outcome["leads"] = leads[arm]
        outcome["reject"] = bool(outcome["reject"] and leads[arm])
    verdict["family_2"] = {
        "test": claim["test"],
        "reference": reference,
        "sided": claim["sided"],
        "arms": arms,
    }
    verdict["family_2"]["n_reject"] = sum(a["reject"] for a in arms.values())
    verdict["family_2"]["cleared"] = verdict["family_2"]["n_reject"] >= 1
    verdict["cleared"] = verdict["family_1"]["cleared"] and verdict["family_2"]["cleared"]
    verdict["licence"] = (
        "at least one confirmatory arm separates the site AND beats "
        f"{reference} on at least one arm; see the per-arm records for which"
        if verdict["cleared"]
        else "no claim: both families must clear"
    )
    return verdict


def _derive_arm(target: str, settings: dict, *, detect: bool) -> dict:
    """Everything the evaluation layer pins for one arm, re-derived from the frozen files."""
    from allo.scoring import decoys as decoy_module

    graph = evaluation_graph(apo_input(target))
    labels, n_candidates = _positives(target)
    k = int(settings["endpoints"]["top_k"])
    matched = settings["nulls"]["matched_patch"]
    try:
        _, diagnostics = matched_patches(
            graph,
            labels,
            n_patches=int(matched["freeze_probe_patches"]),
            tolerance=float(matched["tolerance"]),
            seed=int(settings["seed"]),
        )
        gate = _gate(target, settings)
    except MatchedPoolUnavailable as unavailable:
        diagnostics, gate = unavailable.diagnostics(), None
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
            "available": gate is not None,
            "size_ratio": None if gate is None else gate["size_ratio"],
            "alpha_star": None if gate is None else gate["alpha_star"],
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
    unseal: str | None = None,
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

    **`calibrated_p` is a one-sided rescale and the raw p here is two-sided.** On paper that
    is a type mismatch: rescaling the upper tail of a two-sided p understates the inflation a
    wider null deserves. It is left alone because the question it raises was answered by
    measurement rather than by algebra. Review 21 of the 2026-09-02 audit, finding S8, draws
    the null field out of sample and reads this family's size at **0.041 to 0.047
    against alpha = 0.05**, and 3.7x conservative at alpha on `kras_g12c_corrected`. The
    composite already holds its size, so switching to the two-sided rescale would buy no
    validity and would cost power a family this conservative cannot spare. Revisit if the
    measured size ever reaches alpha.
    """
    _require_unseal(target, unseal)
    settings = config or protocol()
    apo = apo_input(target)
    graph = evaluation_graph(apo)
    labels, _ = _positives(target)
    positive = np.array([r in set(labels) for r in graph.candidates], dtype=bool)

    left, right = _aligned(graph, scores), _aligned(graph, against)
    delta = (metrics.rank_vector(left) - metrics.rank_vector(right)).astype(np.float32)
    observed = float(delta[positive].mean())

    geometry, diagnostics = _patch_null(graph, labels, settings, match_distance=False)
    if geometry is None:
        # Same rule as `score_arm`: the pool is a property of the graph, so an arm that cannot
        # supply one is reported without the test rather than given a different one. The
        # difference in AUC still prints, because it needs no null.
        return {
            "target": target,
            "comparison": f"{names[0]} against {names[1]}",
            "available": False,
            "mean_rank_difference": round(observed, 4),
            "auc_roc_difference": round(
                metrics.auc_roc(left, positive) - metrics.auc_roc(right, positive), 4
            ),
            "leader": None,
            "p": None,
            "p_calibrated": None,
            "size_ratio": None,
            "sided": "two",
            "replicates": 0,
            "null_centre": None,
            "diagnostics": diagnostics,
        }
    null = (geometry @ delta) / geometry.sum(1)
    centre = float(np.median(null))
    extreme = int((np.abs(null - centre) >= abs(observed - centre)).sum())
    raw = (1 + extreme) / (1 + len(null))
    ratio = _gate(target, settings)["size_ratio"]

    return {
        "target": target,
        "comparison": f"{names[0]} against {names[1]}",
        "available": True,
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
    return {
        "frozen_on": str(settings["frozen_on"]),
        "protocol_version": settings["version"],
        "targets": {t: _derive_arm(t, settings, detect=True) for t in _arms_from_the_input_layer()},
    }


def _tier(target: str) -> str | None:
    """The secondary tier an arm belongs to, or None for a primary arm.

    Read from the secondary input freeze rather than from its manifest, because the freeze is
    what `allo.benchmark.size_stratified_split` reproduces and a test already holds that the
    recorded tiers are what that function returns.
    """
    if not SECONDARY_INPUT_FROZEN.exists():
        return None
    record = json.loads(SECONDARY_INPUT_FROZEN.read_text())["targets"].get(target)
    return None if record is None else record.get("tier")


def _arms_from_the_input_layer() -> list[str]:
    """Every arm the evaluation layer must cover, taken from the two INPUT freezes.

    The authority for *which* arms exist is the input layer, never the evaluation freeze
    itself. `verify_evaluation` used to iterate the arms recorded in `frozen.json`, so an arm
    deleted from that file was simply not checked and the verifier exited 0 over fourteen
    arms. Both the freeze and the verification now derive the list here, so the two cannot
    disagree about the set they cover.
    """
    targets = sorted(json.loads(INPUT_FROZEN.read_text())["targets"])
    if SECONDARY_INPUT_FROZEN.exists():
        targets += sorted(json.loads(SECONDARY_INPUT_FROZEN.read_text())["targets"])
    return targets


def verify_evaluation(detect: bool = False) -> list[str]:
    """Differences between the recorded evaluation freeze and what re-derives today.

    `detect=False` is the offline check: it re-derives the chance lines and the matched-patch
    geometry from the committed apo bytes and skips the pockets, so `make check` stays
    offline and free of the `eval` extra. `make verify` runs it with `detect=True`.

    **The whole root is diffed, not the arms one at a time.** Until 2026-09-03 this function
    compared `frozen_on` and then looped over whichever arms `frozen.json` happened to hold.
    Deleting an arm from that file and setting `protocol_version` to 999 left it exiting 0.
    Both are release-gate failures: `README.md` advertises this command as the check that
    "re-derives every pinned value and exits 0 only if nothing moved". `deep_diff` already
    reports a key present on one side and absent on the other, so building the derived root
    exactly as `freeze_evaluation` does and diffing once closes the arm set, the protocol
    version and the freeze date together.
    """
    settings = protocol()
    frozen = json.loads(EVALUATION_FROZEN.read_text())
    current = {
        "frozen_on": str(settings["frozen_on"]),
        "protocol_version": settings["version"],
        "targets": {
            t: _derive_arm(t, settings, detect=detect) for t in _arms_from_the_input_layer()
        },
    }
    if not detect:
        # The pockets are the one part the offline check cannot re-derive, so drop them from
        # both sides rather than reporting every arm as changed.
        frozen = dict(frozen)
        frozen["targets"] = {
            target: {key: value for key, value in record.items() if key != "decoys"}
            for target, record in frozen["targets"].items()
        }
    problems: list[str] = []
    deep_diff(frozen, current, "", problems)
    problems += _conformance_problems(settings)
    return problems


# The 18 leaves of the evaluation manifest that are DECLARATIVE: a rationale, a source note,
# or a statement of why an endpoint was omitted. They may be reworded without changing a
# number. Everything else is normative, and `NORMATIVE_DIGEST` below pins it.
#
# The list is an allow-list on purpose, and it is the same argument `allo.inputs.load` makes
# for redaction: a leaf added later is NORMATIVE by default and fails until someone reviews
# it. The earlier design was the other way round -- a hand-maintained list of what to check --
# so a leaf nobody listed drifted silently. Three did: `nulls.replicates`,
# `nulls.matched_patch_distance.replicates` and `nulls.matched_patch.tolerance`, each of which
# moves a p-value, and `decision.alpha`, which moves every decision. Found by two adversarial
# passes on 2026-09-03, one leaf at a time, which is what closing an instance instead of a
# class looks like.
DECLARATIVE_SETTINGS = frozenset(
    {
        # Rationale prose, and nothing else. Each says WHY a choice was made or why an
        # endpoint is absent. None of them states what the code computes, so none can move a
        # number by disagreeing with the implementation.
        #
        # SHRUNK from 19 to 10 on 2026-09-03. The first cut called a leaf declarative when it
        # read like prose, and nine of them were operational: `pairwise_test` is the frozen
        # definition of "beat", `also_report` mandates a correlation against every baseline,
        # `confounders.statistic` names the estimator, five `source` and `normalised_by`
        # fields name the exact quantity the code derives, and `frozen_on` dates the freeze.
        # An adversarial pass moved `pairwise_test` to a Wilcoxon signed-rank test and
        # `verify_evaluation` returned no problems. Prose is what a reviewer reads; a rule is
        # what the code obeys, and the test for the difference is whether the implementation
        # could contradict it.
        "confounders.conservation.note",
        "confounders.distance_to_source.note",
        "confounders.normalised_b_factor.note",
        "endpoints.omitted.accuracy",
        "endpoints.omitted.dvo",
        "endpoints.omitted.enrichment_factor_bedroc_rie",
        "endpoints.omitted.jaccard",
        "endpoints.omitted.mcc_and_f1",
        "endpoints.omitted.top_5_fragmentation",
        "source",
    }
)

# sha256 over the 64 normative leaves, canonical JSON, sorted keys. Recomputed deliberately
# when the protocol version moves, never to make a failure go away: a mismatch means the
# manifest and the code disagree, and the manifest is not the authority on what the code does.
_MISSING = object()

NORMATIVE_DIGEST = "b26ecd7ee94db1d1ee1c864afa0822e38fdd7d1d9b36797fc3e5f4df49a318d2"


def _settings_leaves(node: object, path: str = "") -> Iterator[tuple[str, object]]:
    """Every leaf of the settings tree, as a dotted path. Lists are leaves, not branches."""
    if isinstance(node, dict):
        for key, value in sorted(node.items()):
            yield from _settings_leaves(value, f"{path}.{key}" if path else key)
    else:
        yield path, node


def normative_settings(settings: dict) -> dict[str, object]:
    """The settings with the declarative leaves removed. What `NORMATIVE_DIGEST` covers."""
    return {
        path: value
        for path, value in _settings_leaves(settings)
        if path not in DECLARATIVE_SETTINGS
    }


def _conformance_problems(settings: dict) -> list[str]:
    """Manifest fields that describe implemented behaviour, checked against the code.

    A mutation sweep on 2026-09-03 changed one manifest leaf at a time and asked whether
    `verify_evaluation` noticed. Six of seventy-four leaves moved a derived value; the rest
    could be edited freely with the verifier still exiting 0. Most of the rest are declarative
    prose -- the omission rationales, the confounder sources, the Phase 3 and 4 endpoint
    declarations -- and prose is what they are meant to be.

    The ones below are different. Each is a NORMATIVE claim about what the code does, so a
    divergence between the manifest and the implementation would change a number while the
    release gate stayed green. They are checked here rather than folded into `frozen.json`,
    because a freeze records what was derived and this records what was implemented. Adding
    them to the freeze would move it, and this moves nothing.
    """
    from allo.scoring import decoys as decoy_module
    from allo.scoring.nulls import IMPLEMENTED_GRAPH_RULE

    implemented = {
        "graph": IMPLEMENTED_GRAPH_RULE,
        "endpoints.confirmatory": "mean_rank",
        "decoys.detector": "pyKVFinder",
        "decoys.detector_version": decoy_module.DETECTOR_VERSION,
        "decision.correction": "holm",
        "decision.claim_family.correction": "holm",
        # Added 2026-09-03. A mutation probe removed the v4 endpoint and flipped both
        # sidedness declarations, and all three left this function silent. `sided` is not
        # decoration: `holm` applies it, and turning `decision.sided` from `upper` to `two`
        # halves every confirmatory p-value's tail without moving one pinned value.
        "decision.sided": "upper",
        "decision.claim_family.sided": "two",
        # Added 2026-09-03. `confirmatory_verdict` reads `decision.alpha` straight from the
        # manifest and no frozen value records it, so a probe moved it from 0.05 to 0.90 and
        # every decision changed while `verify_evaluation` still returned no problems. The
        # calibration invariant below binds it from BELOW, and this literal binds it from
        # above. Both are needed: the invariant cannot see alpha being raised.
        "decision.alpha": 0.05,
    }
    problems: list[str] = []
    # The digest first, because it covers every normative leaf and the named checks below
    # cover nine. A mismatch names the leaves rather than only the hash, so the message is
    # actionable; the named checks then say WHY those nine matter.
    view = normative_settings(settings)
    if (
        hashlib.sha256(json.dumps(view, sort_keys=True, default=str).encode()).hexdigest()
        != NORMATIVE_DIGEST
    ):
        reference = normative_settings(protocol())
        moved = sorted(
            path
            for path in set(view) | set(reference)
            if view.get(path, _MISSING) != reference.get(path, _MISSING)
        )
        changed = moved or ["(none: the tracked manifest itself moved)"]
        problems.append(
            "conformance settings digest: the normative leaves do not match "
            f"NORMATIVE_DIGEST. Changed against the tracked manifest: {changed}"
        )
    # The calibration invariant, from `alpha_star`: "calibration may tighten a test and may
    # never loosen one", so no arm's calibrated threshold may exceed the decision level. This
    # is derived rather than declared, and it is what would catch alpha being LOWERED under a
    # freeze whose thresholds were calibrated at the old value.
    alpha = settings.get("decision", {}).get("alpha")
    if isinstance(alpha, (int, float)) and EVALUATION_FROZEN.exists():
        starred = [
            arm["matched_patch"]["alpha_star"]
            for arm in json.loads(EVALUATION_FROZEN.read_text())["targets"].values()
            if arm.get("matched_patch", {}).get("alpha_star") is not None
        ]
        if starred and max(starred) > float(alpha):
            problems.append(
                f"conformance decision.alpha: {alpha} is below the largest calibrated "
                f"threshold {max(starred)}, so the freeze was calibrated at a different level"
            )
    # `endpoints.reported` is a list, so it is checked for membership rather than equality:
    # the manifest may report more than the code writes, and it may not report less.
    reported = settings.get("endpoints", {}).get("reported") or []
    for name in ("auc_roc_vs_decoy_linings", "label_rank_vs_decoy_linings"):
        if name not in reported:
            problems.append(f"conformance endpoints.reported: {name} is written but not declared")
    for key, expected in implemented.items():
        node: object = settings
        for part in key.split("."):
            node = node[part] if isinstance(node, dict) and part in node else None
            if node is None:
                break
        if node != expected:
            problems.append(f"conformance {key}: manifest {node!r} != implemented {expected!r}")
    return problems
