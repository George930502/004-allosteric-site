"""The evaluation layer: metrics, the matched-patch null, and the freeze that pins them.

Offline throughout. Where a test needs the harness end to end it overrides the replicate
count, because the frozen 9999 is a scoring setting and not a test setting.
"""

from __future__ import annotations

import copy
import json
import re

import numpy as np
import pytest
from scipy.stats import spearmanr

from allo.inputs import ROOT, apo_input
from allo.scoring import harness, metrics
from allo.scoring.calibration import binomial_band
from allo.scoring.harness import _positives
from allo.scoring.nulls import (
    component_sizes,
    evaluation_graph,
    field_factor,
    matched_patches,
    permutation_p,
    smooth_field,
)

PRIMARY = json.loads(harness.INPUT_FROZEN.read_text())["targets"]
EVALUATION = json.loads(harness.EVALUATION_FROZEN.read_text())["targets"]


def fast_protocol(replicates: int = 199) -> dict:
    settings = copy.deepcopy(harness.protocol())
    settings["nulls"]["replicates"] = replicates
    settings["nulls"]["matched_patch_distance"]["replicates"] = replicates
    return settings


# --------------------------------------------------------------------------------------
# Metrics, against values computed by hand rather than against another implementation.
# --------------------------------------------------------------------------------------


def test_metrics_match_hand_computed_values():
    scores = np.array([5.0, 4.0, 3.0, 2.0, 1.0])
    positive = np.array([True, False, True, False, False])
    # Positives {5, 3} beat negatives {4, 2, 1} in 5 of 6 pairs.
    assert metrics.auc_roc(scores, positive) == pytest.approx(5 / 6)
    # Operating points: (P=1, R=0.5) then (P=2/3, R=1).
    assert metrics.auc_pr(scores, positive) == pytest.approx(0.5 * 1 + 0.5 * (2 / 3))
    assert metrics.precision_at_k(scores, positive, 2) == pytest.approx(0.5)


def test_ties_are_midranked_and_broken_pessimistically():
    flat = np.ones(5)
    positive = np.array([True, False, True, False, False])
    assert metrics.auc_roc(flat, positive) == pytest.approx(0.5)
    assert metrics.auc_pr(flat, positive) == pytest.approx(0.4)
    # A method emitting one constant must not collect the top-k by array order.
    assert metrics.precision_at_k(flat, positive, 2) == 0.0


def test_auc_roc_equals_normalised_mann_whitney():
    rng = np.random.default_rng(0)
    scores = rng.integers(0, 4, 200).astype(float)  # heavy ties, where the identity bites
    positive = rng.random(200) < 0.1
    ranks = metrics.rank_vector(scores)
    n_pos = int(positive.sum())
    u = ranks[positive].sum() - n_pos * (n_pos + 1) / 2
    assert metrics.auc_roc(scores, positive) == pytest.approx(u / (n_pos * (200 - n_pos)))


def test_chance_lines_reproduce_the_recorded_benchmark_numbers():
    """`experiments/REGISTRY.md` recorded these before this harness existed.

    Two moved on 2026-09-02 and neither is a drift. `bcr_abl1_mandated` is a different chain
    (ADR 0029) with a different label and candidate count, and `cardiac_myosin_mandated` is a
    new arm (ADR 0031). Both counts were printed here until 2026-09-03 and are redacted: C1
    names the residue count, and a comment is as readable as a table. The other three must not move.
    """
    recorded = {
        "kras_g12c_mandated": 0.445,
        "kras_g12c_corrected": 0.440,
        "bcr_abl1_mandated": 0.219,
        "bcr_abl1_corrected": 0.302,
        "cardiac_myosin_mandated": 0.063,
        "cardiac_myosin_corrected": 0.078,
    }
    assert set(recorded) == set(PRIMARY), "every frozen arm needs a pinned chance line"
    for target, expected in recorded.items():
        frozen = PRIMARY[target]
        got = metrics.p_at_least_one_hit(
            len(frozen["scoreable_label_residues"]), frozen["n_candidates"], 5
        )
        assert got == pytest.approx(expected, abs=5e-4), target


def test_chance_precision_is_the_prevalence():
    assert metrics.expected_precision_at_k(16, 146, 5) == pytest.approx(16 / 146)


def test_precision_at_k_rejects_k_outside_the_ranking():
    scores, positive = np.ones(3), np.array([True, False, False])
    with pytest.raises(ValueError):
        metrics.precision_at_k(scores, positive, 4)


# --------------------------------------------------------------------------------------
# The evaluation graph. It must agree with the input freeze, or the two layers disagree
# about what is being scored.
# --------------------------------------------------------------------------------------


@pytest.mark.parametrize("target", sorted(PRIMARY))
def test_evaluation_graph_agrees_with_the_input_freeze(target):
    graph = evaluation_graph(apo_input(target))
    frozen = PRIMARY[target]
    assert len(graph.order) == frozen["n_residues"]
    assert len(graph.candidates) == frozen["n_candidates"]
    assert sorted(graph.source) == sorted(frozen["excluded_from_scoring"])
    assert set(frozen["scoreable_label_residues"]) <= set(graph.candidates)


def test_label_component_structure_is_what_the_protocol_claims():
    """Three of six label sets are disconnected. A null sampling connected blobs against
    them would impose a property the observation lacks.

    `cardiac_myosin_mandated` is the most fragmented, and its two arms carry the SAME label
    set on structures that disagree — the homology model splits one lobe the measured `9GZ3`
    keeps whole. So the difference is entirely the contact graph, which is the defect ADR 0031
    measures as a long-range contact Jaccard of 0.471, seen from the label set's own side.

    Everything here is DERIVED from the freeze at run time. It used to hold a hard-coded table
    of component sizes per arm, which sums to the positive count — the quantity C1 names when
    it says "not even the residue count" — in a file no path guard covers. A test may read the
    answer key; it may not restate it as a literal. Redacted 2026-09-03.
    """
    sizes = {
        target: component_sizes(
            evaluation_graph(apo_input(target)), PRIMARY[target]["scoreable_label_residues"]
        )
        for target in PRIMARY
    }
    assert len(sizes) == len(PRIMARY), "every frozen arm needs a pinned component structure"

    for target, parts in sizes.items():
        assert sum(parts) == len(PRIMARY[target]["scoreable_label_residues"]), target
        assert list(parts) == sorted(parts, reverse=True), f"{target}: not descending"

    disconnected = {target for target, parts in sizes.items() if len(parts) > 1}
    assert disconnected == {
        "bcr_abl1_corrected",
        "cardiac_myosin_mandated",
        "cardiac_myosin_corrected",
    }, f"the set of fragmented arms moved: {sorted(disconnected)}"

    mandated, corrected = sizes["cardiac_myosin_mandated"], sizes["cardiac_myosin_corrected"]
    assert set(PRIMARY["cardiac_myosin_mandated"]["scoreable_label_residues"]) == set(
        PRIMARY["cardiac_myosin_corrected"]["scoreable_label_residues"]
    ), "the two myosin arms are supposed to share one label set"
    assert len(mandated) > len(corrected), (
        "the homology model is supposed to be the more fragmented of the two, which is what "
        "makes the difference a property of the contact graph and not of the labels"
    )


# --------------------------------------------------------------------------------------
# The matched-patch null.
# --------------------------------------------------------------------------------------


@pytest.mark.parametrize("target", ["kras_g12c_mandated", "bcr_abl1_corrected"])
def test_sampled_patches_really_are_matched(target):
    graph = evaluation_graph(apo_input(target))
    labels = PRIMARY[target]["scoreable_label_residues"]
    tolerance = float(harness.protocol()["nulls"]["matched_patch"]["tolerance"])
    patches, _ = matched_patches(
        graph, labels, n_patches=100, tolerance=tolerance, seed=0, cache=None
    )
    wanted_components = component_sizes(graph, labels)
    mask = graph.index(labels)
    wanted_degree = graph.degree[mask].mean()
    wanted_rg = graph.radius_of_gyration(labels)
    candidates = set(graph.candidates)
    for row in patches:
        residues = [r for r, on in zip(graph.order, row, strict=True) if on]
        assert len(residues) == len(labels)
        assert set(residues) <= candidates
        assert component_sizes(graph, residues) == wanted_components
        assert abs(graph.degree[row].mean() - wanted_degree) <= tolerance * wanted_degree
        assert abs(graph.radius_of_gyration(residues) - wanted_rg) <= tolerance * wanted_rg


def test_the_sampler_refuses_to_short_draw():
    """A silent short draw makes the p-value's denominator a lie."""
    graph = evaluation_graph(apo_input("kras_g12c_mandated"))
    labels = PRIMARY["kras_g12c_mandated"]["scoreable_label_residues"]
    with pytest.raises(RuntimeError, match="matched patches"):
        matched_patches(graph, labels, n_patches=5, tolerance=1e-9, seed=0, cache=None)


def test_patch_cache_returns_the_same_pool():
    graph = evaluation_graph(apo_input("kras_g12c_mandated"))
    labels = PRIMARY["kras_g12c_mandated"]["scoreable_label_residues"]
    first, _ = matched_patches(graph, labels, n_patches=50, tolerance=0.1, seed=0, cache=None)
    second, _ = matched_patches(graph, labels, n_patches=50, tolerance=0.1, seed=0, cache=None)
    assert np.array_equal(first, second)


def test_permutation_p_is_bounded_and_plus_one_corrected():
    null = np.zeros(99)
    assert permutation_p(1.0, null) == pytest.approx(1 / 100)  # nothing beats it
    assert permutation_p(-1.0, null) == pytest.approx(1.0)  # everything does
    assert permutation_p(1.0, np.zeros(0)) == 1.0  # no replicates, no evidence


def test_smooth_field_is_spatially_autocorrelated():
    """The calibration instrument has to have the property it is there to test."""
    graph = evaluation_graph(apo_input("kras_g12c_mandated"))
    coords = graph.ca_coord
    factor = field_factor(coords, 8.0)
    rng = np.random.default_rng(0)
    draws = np.array([smooth_field(factor, rng) for _ in range(200)])
    distance = np.linalg.norm(coords[:, None, :] - coords[None, :, :], axis=-1)
    empirical = np.corrcoef(draws.T)
    close = (distance > 0) & (distance < 6)
    far = distance > 25
    assert empirical[close].mean() > 0.5
    assert empirical[far].mean() < empirical[close].mean()


def test_binomial_band_brackets_alpha():
    low, high = binomial_band(1000, 0.05)
    assert low < 0.05 < high
    assert (low, high) == pytest.approx((0.037, 0.064), abs=1e-3)


# --------------------------------------------------------------------------------------
# The harness contract.
# --------------------------------------------------------------------------------------


def test_score_arm_refuses_an_incomplete_ranking():
    graph = evaluation_graph(apo_input("kras_g12c_mandated"))
    scores = {r: 0.0 for r in graph.candidates[:-1]}
    with pytest.raises(ValueError, match="no score for candidate residues"):
        harness.score_arm("kras_g12c_mandated", scores, method="incomplete", config=fast_protocol())


def test_score_arm_refuses_scores_for_residues_outside_the_node_set():
    graph = evaluation_graph(apo_input("kras_g12c_mandated"))
    scores = {r: 0.0 for r in graph.candidates} | {999_999: 1.0}
    with pytest.raises(ValueError, match="non-node residues"):
        harness.score_arm("kras_g12c_mandated", scores, method="stray", config=fast_protocol())


def test_score_arm_runs_end_to_end_and_reports_every_declared_endpoint():
    target = "kras_g12c_mandated"
    graph = evaluation_graph(apo_input(target))
    source = graph.index(graph.source)
    distance = np.linalg.norm(
        graph.ca_coord[:, None, :] - graph.ca_coord[None, source, :], axis=-1
    ).min(axis=1)
    scores = {r: -float(distance[graph.position[r]]) for r in graph.order}

    record = harness.score_arm(
        target, scores, method="distance_from_source_negated", config=fast_protocol()
    )
    # The repo measured this baseline before the harness existed; it must reproduce.
    assert record["endpoints"]["auc_roc"] == pytest.approx(0.589, abs=1e-3)
    assert set(record["nulls"]) == {
        "background_residues",
        "matched_patch",
        "matched_patch_distance",
        "decoy_pockets",
    }
    assert record["nulls"]["matched_patch"]["confirmatory"] is True
    assert record["chance"] == EVALUATION[target]["chance"]
    # A geometry-only control must not clear a geometry-matched null.
    assert record["nulls"]["matched_patch"]["p"] > 0.05


def test_stricter_nulls_give_larger_p_values():
    """The ladder has to be monotone, or the three nulls are not nested in strictness."""
    target = "kras_g12c_mandated"
    graph = evaluation_graph(apo_input(target))
    source = graph.index(graph.source)
    distance = np.linalg.norm(
        graph.ca_coord[:, None, :] - graph.ca_coord[None, source, :], axis=-1
    ).min(axis=1)
    scores = {r: -float(distance[graph.position[r]]) for r in graph.order}
    nulls = harness.score_arm(target, scores, method="distance", config=fast_protocol(999))["nulls"]
    assert (
        nulls["background_residues"]["p"]
        <= nulls["matched_patch"]["p"]
        <= nulls["matched_patch_distance"]["p"]
    )


def test_holm_is_step_down_and_stops_at_the_first_failure():
    verdict = harness.holm({"a": 0.001, "b": 0.03, "c": 0.9}, alpha=0.05)
    assert verdict["a"]["threshold"] == pytest.approx(0.05 / 3, abs=1e-6)
    assert verdict["a"]["reject"] is True
    assert verdict["b"]["threshold"] == pytest.approx(0.05 / 2, abs=1e-6)
    assert verdict["b"]["reject"] is False  # 0.03 > 0.025
    assert verdict["c"]["reject"] is False  # and nothing after it can reject


# --------------------------------------------------------------------------------------
# The freeze.
# --------------------------------------------------------------------------------------


def test_evaluation_freeze_verifies_offline():
    """Everything except the pockets re-derives from the committed apo bytes."""
    assert harness.verify_evaluation(detect=False) == []


def test_every_frozen_arm_carries_a_decoy_record():
    for target, record in EVALUATION.items():
        assert "decoys" in record, target
        assert record["decoys"]["n_detected"] >= record["decoys"]["n_scoreable"]
        decoy_residues = {r for p in record["decoys"]["pockets"].values() for r in p["lining"]}
        assert decoy_residues.isdisjoint(
            json.loads(harness.INPUT_FROZEN.read_text())["targets"]
            .get(target, {})
            .get("scoreable_label_residues", [])
        ), f"{target}: a decoy lining contains a label"


def test_decoy_power_floor_is_recorded_where_it_bites():
    """KRAS has five detectable pockets, so the pocket criterion cannot reach 0.05 there.
    That is arithmetic about a 169-residue protein, and it is disclosed, not hidden."""
    kras = EVALUATION["kras_g12c_mandated"]["decoys"]
    assert kras["minimum_attainable_p"] > 0.05
    myosin = EVALUATION["cardiac_myosin_corrected"]["decoys"]
    assert myosin["minimum_attainable_p"] < 0.05


def test_protocol_declares_one_confirmatory_family_of_three():
    decision = harness.protocol()["decision"]
    assert len(decision["confirmatory_family"]) == 3
    assert set(decision["confirmatory_family"]).isdisjoint(decision["supportive_only"])
    assert decision["sided"] == "upper"


def test_every_primary_arm_has_exactly_one_declared_reporting_role():
    """Disjointness is not enough; an arm can be in neither list and be scored anyway.

    `cardiac_myosin_mandated` was in neither between the ADR 0031 re-freeze and 2026-09-02.
    It was fully scored, at 932 candidates and 139 decoys, with its role declared only in
    its own input-manifest block and not in the decision rule -- a free parameter in the one
    file that exists to have none.
    """
    decision = harness.protocol()["decision"]
    frozen = set(json.loads(harness.INPUT_FROZEN.read_text())["targets"])
    declared = list(decision["confirmatory_family"]) + list(decision["supportive_only"])

    assert len(declared) == len(set(declared)), f"an arm has two roles: {declared}"
    assert set(declared) == frozen, (
        f"every primary arm needs exactly one role. missing: {sorted(frozen - set(declared))}; "
        f"unknown: {sorted(set(declared) - frozen)}"
    )


# --------------------------------------------------------------------------------------
# The size calibration (ADR 0023, rescale corrected by ADR 0025). Matching size, components,
# burial and compactness is not enough on every arm, so the threshold is calibrated instead of
# the null matched further -- at every Holm level, not only at alpha.
# --------------------------------------------------------------------------------------


def test_every_frozen_arm_carries_a_calibrated_threshold_that_only_tightens():
    settings = harness.protocol()
    alpha = float(settings["decision"]["alpha"])
    # Counted: every assertion is inside the loop, so a filter that matched everything
    # or an emptied source would make this pass by asserting nothing. Round 6.
    checked = 0
    for target, record in EVALUATION.items():
        checked += 1
        star = record["matched_patch"]["alpha_star"]
        assert 0 < star <= alpha, f"{target}: alpha_star {star} is not a tightening of {alpha}"
        ratio = record["matched_patch"]["size_ratio"]
        assert ratio >= 1.0, f"{target}: size_ratio {ratio} would loosen the test"
    assert checked, "the evaluation freeze carried no arm, so this asserted nothing"


def test_the_calibration_is_conservative_at_every_holm_level_not_only_at_alpha():
    """The version-1 defect: a ratio fitted at alpha alone leaks FWER at Holm's tighter steps.

    The rescale is conservative at level `t` exactly when the ratio is at least
    `z(q_t) / z(t)`, so the frozen ratio must dominate the ratio each level needs. Checking it
    at alpha only would pass the version-1 freeze, which was not FWER-controlled.
    """
    settings = harness.protocol()
    family = len(settings["decision"]["confirmatory_family"])
    alpha = float(settings["decision"]["alpha"])
    gate = json.loads(
        (
            ROOT / str(settings["nulls"]["matched_patch"]["calibrated_by"]) / "metrics.json"
        ).read_text()
    )["gate"]
    for target, record in EVALUATION.items():
        frozen_ratio = record["matched_patch"]["size_ratio"]
        assert gate[target]["family_size"] == family
        for length_scale, rates in gate[target]["type_one_rate"].items():
            assert len(rates["step_ratio"]) == family, f"{target}: not every Holm level measured"
            for level, needed in rates["step_ratio"].items():
                assert frozen_ratio >= needed, (
                    f"{target} at lambda {length_scale}, level {level}: frozen ratio "
                    f"{frozen_ratio} is below the {needed} that level needs"
                )
        tightest = min(float(level) for level in rates["step_ratio"])
        assert tightest == pytest.approx(alpha / family, abs=1e-5), (
            "tightest Holm level not measured"
        )


def test_the_freeze_quotes_the_calibration_experiment_and_does_not_restate_it():
    settings = harness.protocol()
    gate = json.loads(
        (
            ROOT / str(settings["nulls"]["matched_patch"]["calibrated_by"]) / "metrics.json"
        ).read_text()
    )["gate"]
    # Counted: every assertion is inside the loop, so a filter that matched everything
    # or an emptied source would make this pass by asserting nothing. Round 6.
    checked = 0
    for target, record in EVALUATION.items():
        checked += 1
        assert record["matched_patch"]["alpha_star"] == pytest.approx(gate[target]["alpha_star"])
        assert record["matched_patch"]["size_ratio"] == pytest.approx(gate[target]["size_ratio"])
    assert checked, "the evaluation freeze carried no arm, so this asserted nothing"


def test_the_calibrated_p_is_never_smaller_than_the_raw_one():
    """Calibration may tighten a test and may never loosen one."""
    target = "bcr_abl1_corrected"
    graph = evaluation_graph(apo_input(target))
    source = graph.index(graph.source)
    distance = np.linalg.norm(
        graph.ca_coord[:, None, :] - graph.ca_coord[None, source, :], axis=-1
    ).min(axis=1)
    scores = {r: -float(distance[graph.position[r]]) for r in graph.order}
    matched = harness.score_arm(target, scores, method="distance", config=fast_protocol(999))[
        "nulls"
    ]["matched_patch"]
    assert matched["p_calibrated"] >= matched["p"]
    assert matched["size_ratio"] > 1.0, "this arm is the one the gate found anti-conservative"


def test_the_rescale_never_loosens_anywhere_on_the_unit_interval():
    """The clamp. Above p = 0.5 the probit rescale would lower p, which the docs forbid."""
    for ratio in (1.0, 1.05, 1.25, 2.0):
        previous = 0.0
        for step in range(1, 1000):
            p = step / 1000
            calibrated = harness.calibrated_p(p, ratio)
            assert calibrated >= p, f"ratio {ratio} loosened p={p}"
            assert calibrated >= previous, f"ratio {ratio} is not monotone at p={p}"
            previous = calibrated
    # A ratio of 1 is the identity, so an already-conservative arm is untouched.
    assert harness.calibrated_p(0.031, 1.0) == pytest.approx(0.031)


# --------------------------------------------------------------------------------------
# The cavity-volume baseline (ADR 0025). It clears the confirmatory family on all three
# arms, so "rejects the null" is not evidence a method learned anything about allostery.
# --------------------------------------------------------------------------------------


def test_cavity_volume_takes_the_largest_lining_cavity_and_ignores_non_candidates():
    from allo.scoring.decoys import cavity_volume_score

    pockets = {
        "KAA": {"lining": [10, 11], "volume": 120.0},
        "KAB": {"lining": [11, 12], "volume": 340.0},
        "KAC": {"lining": [99], "volume": 999.0},  # residue outside the candidate set
    }
    score = cavity_volume_score(pockets, [10, 11, 12, 13])
    assert score == {10: 120.0, 11: 340.0, 12: 340.0, 13: 0.0}
    assert 99 not in score, "a residue outside the candidate set must not gain a score"


def test_the_site_pocket_rank_is_pessimistic_under_ties():
    """A method scoring every pocket alike must report last place, never first."""
    target = "cardiac_myosin_corrected"
    graph = evaluation_graph(apo_input(target))
    flat = dict.fromkeys(graph.order, 1.0)
    decoy = harness.score_arm(target, flat, method="flat", config=fast_protocol(199))["nulls"][
        "decoy_pockets"
    ]
    assert decoy["site_pocket_rank"] == decoy["n_pockets_ranked"]


def test_the_decoy_p_value_is_built_from_the_site_pocket_and_not_the_label_set():
    """ADR 0030 writes this test as `(1 + #{decoy_rank >= site_rank}) / (1 + n_decoys)`.

    Its type-I simulation drew the site's number from the same unit-variance law as the
    decoys', which holds only while both halves are a pocket lining. Passing the label
    set's own mean midrank instead compares a mean over `|labels|` draws with a mean over
    `|lining|` draws. That statistic is not exchangeable with the decoys and no measured
    type-I rate in `decoy-typeI.json` covers it. The code did exactly that until
    2026-09-02, so the identity below is the regression check.
    """
    target = "cardiac_myosin_corrected"
    graph = evaluation_graph(apo_input(target))
    # Deterministic, non-flat and label-blind: a flat score makes both statistics equal
    # and would pass whichever one the code used.
    scores = {residue: float(residue) for residue in graph.order}
    decoy = harness.score_arm(target, scores, method="residue-number", config=fast_protocol(199))[
        "nulls"
    ]["decoy_pockets"]
    assert decoy["p"] == pytest.approx(decoy["site_pocket_rank"] / decoy["n_pockets_ranked"]), (
        "the reported p and the reported rank are no longer the same statistic"
    )


# --------------------------------------------------------------------------------------
# The residue-list criterion and the confounder columns (ADR 0025). Both were declared in
# prose and computed by nothing until the version-2 audit.
# --------------------------------------------------------------------------------------


def test_dcc_measures_centre_to_centre_and_falls_to_zero_on_a_perfect_list():
    from allo.scoring.metrics import chance_dcc, dcc, top_k_indices

    # Two clusters 10 A apart on the x axis; the labels are the right-hand one.
    left = np.array([[0.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])
    right = left + np.array([10.0, 0.0, 0.0])
    coords = np.vstack([left, right])
    labels = np.array([False, False, False, True, True, True])

    assert dcc(coords, np.array([3, 4, 5]), labels) == pytest.approx(0.0)
    assert dcc(coords, np.array([0, 1, 2]), labels) == pytest.approx(10.0)
    # A score that ranks the labels first must give exactly the perfect list.
    scores = np.array([0.0, 0.0, 0.0, 1.0, 1.0, 1.0])
    assert dcc(coords, top_k_indices(scores, 3), labels) == pytest.approx(0.0)
    # And the list is a function of the scores alone: flipping the labels cannot move it.
    assert list(top_k_indices(scores, 3)) == list(top_k_indices(scores, 3))
    assert set(top_k_indices(np.array([1.0] * 6), 3)) == {0, 1, 2}, (
        "a flat score must give the first three candidates, not the three negatives"
    )
    # The chance line sits between the two, and it is deterministic.
    chance = chance_dcc(coords, labels, 3)
    assert 0.0 < chance < 10.0
    assert chance == chance_dcc(coords, labels, 3)


def test_the_frozen_chance_dcc_is_reproducible_from_the_committed_seed():
    from allo.scoring.metrics import chance_dcc

    settings = harness.protocol()
    # Counted: every assertion is inside the loop, so a filter that matched everything
    # or an emptied source would make this pass by asserting nothing. Round 6.
    checked = 0
    for target, record in EVALUATION.items():
        checked += 1
        graph = evaluation_graph(apo_input(target))
        labels, _ = _positives(target)
        mask = np.array([r in set(labels) for r in graph.candidates], dtype=bool)
        again = chance_dcc(
            graph.ca_coord[graph.index(graph.candidates)],
            mask,
            int(settings["endpoints"]["top_k"]),
            seed=int(settings["seed"]),
        )
        assert record["chance"]["dcc_angstrom"] == pytest.approx(again, abs=5e-4), target
    assert checked, "the evaluation freeze carried no arm, so this asserted nothing"


def test_solvent_accessibility_agrees_with_an_independent_implementation():
    """Shrake-Rupley is implemented here, so it is checked against biopython's.

    Ours integrates over 92 sphere points and biopython's over 960, so exact equality is not
    expected. What must hold is that the two rank residues by burial the same way, because a
    Spearman column is what the confounder is used for.
    """
    import io
    import warnings

    from Bio.PDB import PDBParser
    from Bio.PDB.SASA import ShrakeRupley

    from allo.structure.properties import MAX_ACCESSIBLE_AREA, solvent_accessibility

    apo = apo_input("kras_g12c_corrected")
    structure = apo.structure
    mask = structure.protein
    lines = []
    for i, (chain, seq, resname, atom, element, xyz) in enumerate(
        zip(
            structure.chain[mask],
            structure.seq_id[mask],
            structure.resname[mask],
            structure.atom[mask],
            structure.element[mask],
            structure.coord[mask],
            strict=True,
        )
    ):
        # Columns 13-16 atom name, 17 altLoc, 18-20 resName, 22 chain, 23-26 resSeq. Getting
        # the altLoc column wrong truncates the residue name and silently changes the answer.
        name = atom if len(atom) >= 4 else f" {atom:<3s}"
        lines.append(
            f"ATOM  {i + 1:5d} {name:<4s} {resname:>3s} {chain}{int(seq):4d}    "
            f"{xyz[0]:8.3f}{xyz[1]:8.3f}{xyz[2]:8.3f}  1.00  0.00          {element:>2s}"
        )
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        parsed = PDBParser(QUIET=True).get_structure("x", io.StringIO("\n".join(lines) + "\nEND"))
    chain = next(next(parsed.get_models()).get_chains())
    assert all(len(residue.get_resname()) == 3 for residue in chain), "resname column is wrong"
    ShrakeRupley(n_points=960).compute(chain, level="R")
    theirs = {
        residue.id[1]: residue.sasa / MAX_ACCESSIBLE_AREA[residue.get_resname()]
        for residue in chain
    }

    mine = solvent_accessibility(apo)
    shared = sorted(set(mine) & set(theirs))
    ours = np.array([mine[r] for r in shared])
    reference = np.array([theirs[r] for r in shared])
    assert float(spearmanr(ours, reference).statistic) > 0.99
    assert float(np.abs(ours - reference).max()) < 0.10


def test_every_scored_record_carries_every_declared_confounder_column():
    from allo.structure.properties import residue_properties

    target = "kras_g12c_corrected"
    graph = evaluation_graph(apo_input(target))
    record = harness.score_arm(
        target,
        dict.fromkeys(graph.order, 1.0),
        method="flat",
        config=fast_protocol(199),
    )
    declared = set(harness.protocol()["confounders"]) - {"statistic"}
    assert set(record["confounders"]) == declared
    assert record["confounders"]["conservation"] is None, "conservation must read as unknown"
    # A flat score has no rank correlation with anything. It must read undefined, never NaN,
    # because NaN is not valid JSON and the record would not survive a round trip.
    assert all(value is None for value in record["confounders"].values())
    assert json.loads(json.dumps(record))["confounders"] == record["confounders"]

    source = graph.index(graph.source)
    distance = np.linalg.norm(
        graph.ca_coord[:, None, :] - graph.ca_coord[None, source, :], axis=-1
    ).min(axis=1)
    real = harness.score_arm(
        target,
        {r: -float(distance[graph.position[r]]) for r in graph.order},
        method="distance",
        config=fast_protocol(199),
    )
    for name in residue_properties(apo_input(target)):
        assert real["confounders"][name] is not None


def test_a_paired_comparison_of_a_score_with_itself_cannot_separate():
    """The floor case. Identical scores must give zero effect and the largest possible p."""
    target = "kras_g12c_corrected"
    graph = evaluation_graph(apo_input(target))
    source = graph.index(graph.source)
    distance = np.linalg.norm(
        graph.ca_coord[:, None, :] - graph.ca_coord[None, source, :], axis=-1
    ).min(axis=1)
    scores = {r: -float(distance[graph.position[r]]) for r in graph.order}
    result = harness.compare_methods(
        target, scores, dict(scores), names=("a", "copy"), config=fast_protocol(499)
    )
    assert result["auc_roc_difference"] == pytest.approx(0.0)
    assert result["mean_rank_difference"] == pytest.approx(0.0)
    assert result["p"] == pytest.approx(1.0)
    assert result["sided"] == "two", "a method-versus-method test must not assume a winner"


def test_the_paired_comparison_is_symmetric_in_its_two_arguments():
    """Swapping the arguments must flip the leader and leave the evidence unchanged."""
    target = "kras_g12c_corrected"
    graph = evaluation_graph(apo_input(target))
    source = graph.index(graph.source)
    distance = np.linalg.norm(
        graph.ca_coord[:, None, :] - graph.ca_coord[None, source, :], axis=-1
    ).min(axis=1)
    near = {r: -float(distance[graph.position[r]]) for r in graph.order}
    far = {r: float(distance[graph.position[r]]) for r in graph.order}
    forward = harness.compare_methods(
        target, near, far, names=("near", "far"), config=fast_protocol(499)
    )
    backward = harness.compare_methods(
        target, far, near, names=("far", "near"), config=fast_protocol(499)
    )
    assert forward["p"] == pytest.approx(backward["p"])
    assert forward["auc_roc_difference"] == pytest.approx(-backward["auc_roc_difference"])
    assert forward["leader"] == backward["leader"], "the winner must not depend on argument order"


def test_top_k_components_counts_places_not_residues():
    """One pocket must read 1 and a scattered list must read k.

    The endpoint exists to separate "five residues a chemist can design against" from "five
    residues in five places" (`CHALLENGE.md` §4.2). A count that cannot tell those apart is
    worse than no count, so both ends are pinned here rather than trusted.
    """
    graph = evaluation_graph(apo_input("kras_g12c_corrected"))
    k = 5
    inside = set(graph.candidates)

    # One place: a residue and four of its own graph neighbours, all inside the candidate set.
    seed = next(r for r in graph.candidates if len(graph.neighbours(r) & inside) >= 4)
    clique = [seed, *sorted(graph.neighbours(seed) & inside)[:4]]
    top = {r: (1.0 if r in set(clique) else 0.0) for r in graph.candidates}
    values = np.array([top[r] for r in graph.candidates])
    assert harness.top_k_components(graph, values, k) == 1

    # Five places: five residues no two of which are adjacent.
    scattered: list[int] = []
    for residue in graph.candidates:
        if len(scattered) == k:
            break
        if all(residue not in graph.neighbours(other) for other in scattered):
            scattered.append(residue)
    assert len(scattered) == k, "the arm is too small to hold five mutually non-adjacent residues"
    spread = {r: (1.0 if r in set(scattered) else 0.0) for r in graph.candidates}
    values = np.array([spread[r] for r in graph.candidates])
    assert harness.top_k_components(graph, values, k) == k


def test_combining_arms_tests_the_intersection_null_and_is_labelled_as_such():
    """Fisher and Stouffer escape the per-arm floor, and the record must say what they test.

    A rejection here licenses "at least one arm separates the site from non-functional surface
    pockets" and nothing stronger. The label is the point of the test (ADR 0030).

    The arm names are the FROZEN family from 2026-09-03. The manifest declares this
    combination `over: confirmatory_family` and nothing enforced it, so this test used three
    made-up names and passed. A combination over a set chosen after seeing the numbers is a
    different test from the one the protocol froze.
    """
    family = sorted(harness.protocol()["decision"]["confirmatory_family"])
    floors = dict(zip(family, (0.25, 0.1, 0.04), strict=True))
    combined = harness.combine_arms(floors)
    assert combined["p"] < min(floors.values()), "combination must beat every per-arm floor"
    assert combined["tests"] == "intersection null: no arm has signal"
    assert combined["arms"] == family
    assert combined["p_per_arm"] == floors
    # Identical inputs, both directions: a uniform p-vector must not reject.
    assert harness.combine_arms(dict.fromkeys(family, 0.5))["p"] > 0.05

    # And a set that is not the family is refused, which is the whole repair.
    for wrong in ({family[0]: 0.01, family[1]: 0.01}, {"a": 0.01, "b": 0.01, "c": 0.01}):
        with pytest.raises(ValueError, match="confirmatory family"):
            harness.combine_arms(wrong)


def test_the_frozen_decision_rule_reads_the_frozen_family():
    """The manifest froze a confirmatory family and until 2026-09-02 no code read it.

    `decision.alpha`, `decision.confirmatory_family` and `decision.correction` had no reader
    in `src/` or `experiments/`, and `holm` had no caller outside this file. Nothing would
    have noticed a fourth arm entering the family or Holm running over six.
    """
    settings = harness.protocol()
    declared = list(settings["decision"]["confirmatory_family"])
    assert len(declared) == 3

    verdict = harness.confirmatory_verdict(dict.fromkeys(declared, 0.001))
    assert verdict["alpha"] == 0.05
    assert verdict["correction"] == "holm"
    assert verdict["family_1"]["n_reject"] == 3
    # Holm over three: the smallest p is tested at alpha/3.
    assert verdict["family_1"]["arms"][declared[0]]["threshold"] == pytest.approx(
        0.05 / 3, abs=5e-7
    )

    # Step-down stops at the first failure, and the count reflects it.
    ps = dict(zip(declared, [0.001, 0.9, 0.002], strict=True))
    assert harness.confirmatory_verdict(ps)["family_1"]["n_reject"] == 2


def test_the_decision_rule_refuses_a_family_that_is_not_the_declared_one():
    """Correcting over the wrong m is the failure this guard exists to make loud."""
    settings = harness.protocol()
    declared = list(settings["decision"]["confirmatory_family"])

    with pytest.raises(ValueError, match="family_1 must be exactly"):
        harness.confirmatory_verdict(dict.fromkeys([*declared, "kras_g12c_mandated"], 0.01))
    with pytest.raises(ValueError, match="family_1 must be exactly"):
        harness.confirmatory_verdict(dict.fromkeys(declared[:2], 0.01))

    claim = settings["decision"]["claim_family"]
    reference = claim["reference"]

    def won(p=0.01):
        return {"comparison": f"ctqw against {reference}", "leader": "ctqw", "p_calibrated": p}

    with pytest.raises(ValueError, match="family_2 must be exactly"):
        harness.confirmatory_verdict(dict.fromkeys(declared, 0.01), {declared[0]: won()})
    both = harness.confirmatory_verdict(
        dict.fromkeys(declared, 0.01), {arm: won() for arm in claim["arms"]}
    )
    assert both["family_2"]["reference"] == "cavity_volume"
    assert both["family_2"]["sided"] == "two"


def test_the_claim_family_counts_a_rejection_only_when_the_method_wins():
    """ADR 0032 licenses "the method beats the reference"; the test that licenses it is two-sided.

    The first implementation took bare p-values, so a method significantly WORSE than
    `cavity_volume` cleared the claim family: Holm rejects either tail and the direction was
    discarded. Two records with identical p-values and opposite leaders must give opposite
    verdicts, or the family does not test what the ADR says it tests.
    """
    settings = harness.protocol()
    family_1 = dict.fromkeys(settings["decision"]["confirmatory_family"], 1e-6)
    claim = settings["decision"]["claim_family"]
    arms, reference = list(claim["arms"]), claim["reference"]

    def record(leader):
        return {
            "comparison": f"ctqw against {reference}",
            "leader": leader,
            "p_calibrated": 1e-6,
        }

    wins = harness.confirmatory_verdict(family_1, {a: record("ctqw") for a in arms})
    loses = harness.confirmatory_verdict(family_1, {a: record(reference) for a in arms})
    assert wins["family_2"]["n_reject"] == 3
    assert loses["family_2"]["n_reject"] == 0
    assert all(a["leads"] for a in wins["family_2"]["arms"].values())
    assert not any(a["leads"] for a in loses["family_2"]["arms"].values())

    # A bare p-value carries no direction, so it is refused rather than assumed favourable.
    with pytest.raises(TypeError, match="compare_methods record"):
        harness.confirmatory_verdict(family_1, dict.fromkeys(arms, 1e-6))
    # Swapping the two arguments of `compare_methods` would reverse the direction silently.
    with pytest.raises(ValueError, match="the frozen reference is"):
        harness.confirmatory_verdict(
            family_1,
            {
                a: {"comparison": "ctqw against degree", "leader": "ctqw", "p_calibrated": 1e-6}
                for a in arms
            },
        )


def test_a_family_is_cleared_when_holm_rejects_at_least_one_arm():
    """ADR 0038 freezes the disjunction, and the frozen layer used to hold both readings.

    README section 8 and ADR 0030 read the combination test disjunctively; `docs/ROADMAP.md`
    and section 13 printed one-of-three as a failure. The rule now lives in code, so a reader
    cannot pick the reading that suits the result.

    The composite needs BOTH families, which is what the manifest has always said. One arm in
    each is enough, and no arm in either is not.
    """
    settings = harness.protocol()
    family = list(settings["decision"]["confirmatory_family"])
    claim = settings["decision"]["claim_family"]
    reference = claim["reference"]

    def record(leader, p):
        return {"comparison": f"ctqw against {reference}", "leader": leader, "p_calibrated": p}

    one = {family[0]: 1e-6, family[1]: 0.9, family[2]: 0.9}
    none = dict.fromkeys(family, 0.9)
    wins_one = {claim["arms"][0]: record("ctqw", 1e-6)} | {
        a: record("ctqw", 0.9) for a in claim["arms"][1:]
    }
    loses_all = {a: record("ctqw", 0.9) for a in claim["arms"]}

    assert harness.confirmatory_verdict(one, wins_one)["cleared"]
    assert not harness.confirmatory_verdict(none, wins_one)["cleared"]
    assert not harness.confirmatory_verdict(one, loses_all)["cleared"]
    # A rejection in the wrong direction is not a rejection, so it cannot clear either.
    reversed_claim = {a: record(reference, 1e-6) for a in claim["arms"]}
    assert not harness.confirmatory_verdict(one, reversed_claim)["cleared"]
    # Family 1 alone is not a composite verdict. The field is present and False, because
    # absent is not the same as unmet and a caller must not have to tell them apart.
    alone = harness.confirmatory_verdict(one)
    assert alone["family_1"]["cleared"]
    assert alone["cleared"] is False
    assert "both families" in alone["licence"]


def test_negative_class_b_reports_the_label_set_beside_the_site_pocket():
    """ADR 0039, protocol v4. `p` ranks the site POCKET; `label_p` ranks the label RESIDUES.

    The two are different questions and the difference is measurable: a delta = 4 shift on
    every label residue leaves `p` at power 0 on two of three confirmatory arms, while
    `label_p` reaches 0.999 and 1.000. Both must be present, and on an arm whose site lining
    is not the label set they must be free to differ.
    """
    arm = "cardiac_myosin_corrected"
    frozen = json.loads(harness.EVALUATION_FROZEN.read_text())["targets"][arm]
    lining = set(frozen["decoys"]["site_pocket"]["lining"])
    labels = set(harness._positives(arm)[0])
    assert lining and labels and lining != labels, "this arm must separate the two sets"

    graph = evaluation_graph(apo_input(arm))
    scores = {r: float(i) for i, r in enumerate(graph.order)}
    record = harness.score_arm(arm, scores, method="probe", config=fast_protocol(99))["nulls"][
        "decoy_pockets"
    ]
    assert record["p"] is not None and record["label_p"] is not None
    assert record["confirmatory"] is False, "both forms stay descriptive"


def test_the_sealed_tier_cannot_be_scored_without_saying_so():
    """ADR 0041. The rule lived in a manifest comment and was broken in 23 tracked files.

    A rule a document states and no test holds is a promise. This one was broken in the very
    commit that wrote it, so the tier was never sealed against storage. Scoring is what the
    seal can still protect, so scoring is what is guarded.
    """
    graph = evaluation_graph(apo_input("mkp5"))
    scores = {r: float(i) for i, r in enumerate(graph.order)}
    with pytest.raises(PermissionError, match="sealed `generalisation` tier"):
        harness.score_arm("chk1", scores, method="probe", config=fast_protocol(99))
    # A development arm is not sealed and needs no token.
    harness.score_arm("mkp5", scores, method="probe", config=fast_protocol(99))


def test_every_public_scoring_entry_point_carries_the_generalisation_seal():
    """ADR 0041's seal, pinned at the boundary rather than in one caller. Added 2026-09-03.

    The seal was written inside `score_arm`. `compare_methods` was exported beside it, takes
    the same two things -- an arm name and a method's scores -- reads the same frozen labels,
    and had no check, so a caller could score a sealed arm through the paired test and get a
    complete record with calibrated p-values. Same shape as every other guard defect here:
    the rule sat in one caller instead of at the boundary.

    So this asserts on the SET, not on the two functions. A future public scorer that takes
    an arm and a score map must call `_require_unseal`, and this fails until it does.

    The seal is deliberately NOT in `_positives`, the shared read. Calibration and the size
    simulation read every arm's labels by design -- the August calibration derived all
    fifteen arms' thresholds -- so a check on the read would break the freeze it protects.
    ADR 0041 says the seal covers scoring, and scoring is what these functions do.
    """
    import inspect

    from allo import scoring
    from allo.scoring import harness

    sealed = "chk1"  # a `generalisation` arm; `_tier` reads it from the secondary freeze
    assert harness._tier(sealed) == "generalisation", f"{sealed} left the sealed tier"

    entry_points = []
    for name in scoring.__all__:
        function = getattr(scoring, name)
        parameters = inspect.signature(function).parameters
        # An entry point is anything taking an arm name AND a residue-keyed score map.
        if "target" in parameters and "scores" in parameters:
            entry_points.append((name, function, parameters))

    assert {name for name, _, _ in entry_points} == {"score_arm", "compare_methods"}, (
        f"the public scoring surface changed: {sorted(n for n, _, _ in entry_points)}. Add the "
        "new entry point's seal call, then update this set"
    )

    for name, function, parameters in entry_points:
        assert "unseal" in parameters, f"{name} takes an arm and scores but has no unseal"
        arguments = {"scores": {1: 0.0}}
        if "against" in parameters:
            arguments["against"] = {1: 0.0}
        if "method" in parameters:
            arguments["method"] = "probe"
        with pytest.raises(PermissionError, match="sealed"):
            function(sealed, **arguments)
        # And the token must actually open it: a guard that never opens is a broken gate,
        # not a strong one. Anything raised past this point is the arm's own scoring.
        with pytest.raises(Exception) as raised:
            function(sealed, unseal="phase-5", **arguments)
        assert not isinstance(raised.value, PermissionError), (
            f"{name}: unseal='phase-5' was refused, so the seal cannot be opened in Phase 5"
        )


def test_the_size_simulation_draws_four_distinct_rank_laws():
    """Every statistic in `allo.scoring.simulate` is a midrank, so a generator that differs
    from another only by an elementwise monotone map is not a second null. Added 2026-09-03.

    This is not hypothetical. `smooth_t` built a multivariate t by dividing a Gaussian field
    by ONE chi-square draw per replicate. Dividing a column by a positive scalar is monotone
    within that column, so its ranks were bit-identical to `smooth_gaussian`'s at the same
    seed, and the run behind ADR 0039 measured three laws while claiming four.

    **Checked on the law, not on the byte.** The first version of this test asserted only that
    two generators give different rank arrays at the same seed. That catches the exact bug
    above and nothing else: two generators drawing the SAME law while consuming the random
    stream differently would also differ, and would pass. So the comparison is a signature of
    the dependence structure -- the mean between-residue rank correlation at short and at long
    spatial separation -- because the copula is the only thing a rank test can see. A monotone
    duplicate scores exactly 0 on it. The four generators' closest pair is about 0.16 apart, so
    the 0.05 floor below has three times the margin it needs.
    """
    import itertools

    import numpy as np

    from allo.scoring.nulls import field_factor
    from allo.scoring.simulate import GENERATORS, _draw, _ranks

    assert len(GENERATORS) == 4, GENERATORS
    n, replicates = 100, 1200
    coordinates = np.random.default_rng(11).standard_normal((n, 3)) * 12
    factor = field_factor(coordinates, 8.0)
    pairs = np.triu_indices(n, 1)
    separation = np.linalg.norm(coordinates[:, None, :] - coordinates[None, :, :], axis=-1)[pairs]
    near = separation <= np.quantile(separation, 0.15)
    far = separation >= np.quantile(separation, 0.85)

    signature = {}
    for name in GENERATORS:
        ranks = _ranks(
            _draw(name, factor, coordinates, np.random.default_rng(5), replicates)
        ).astype(np.float64)
        ranks = (ranks - ranks.mean(0)) / ranks.std(0)
        correlation = ((ranks @ ranks.T) / replicates)[pairs]
        signature[name] = (float(correlation[near].mean()), float(correlation[far].mean()))

    for left, right in itertools.combinations(GENERATORS, 2):
        gap = max(abs(a - b) for a, b in zip(signature[left], signature[right], strict=True))
        assert gap > 0.05, (
            f"{left} and {right} have the same rank-correlation signature, {gap:.4f} apart. "
            "They are one law under a rank statistic, so the run measures one fewer null than "
            f"it reports. Signatures: {signature}"
        )


def test_every_normative_manifest_leaf_is_bound_by_conformance():
    """Mutate each of the evaluation manifest's leaves in turn and require a problem, unless
    the leaf is declared prose. Added 2026-09-03.

    The history is the argument for the shape. `_conformance_problems` began as a
    hand-maintained list of what to check, and a sweep found **6 of 74** leaves bound. Three
    adversarial passes then found four more, one at a time -- `decision.sided`,
    `decision.claim_family.sided`, `decision.alpha`, `nulls.replicates` -- each of which moves
    a number while `allo evaluate verify` exits 0. Closing an instance per pass is not closing
    a class.

    So the allow-list is inverted. `DECLARATIVE_SETTINGS` names the leaves that may be
    reworded, `NORMATIVE_DIGEST` covers everything else, and a leaf added later is normative
    by default. That is the same argument `allo.inputs.load` makes for redaction.

    This test is the proof of coverage, and it is exact: the set that survives mutation must
    equal the declared set, neither larger nor smaller. Smaller would mean a prose leaf is
    being treated as normative and a rewording would fail the gate for no reason.
    """
    import copy

    from allo.scoring import harness
    from allo.scoring.harness import DECLARATIVE_SETTINGS, _settings_leaves

    def mutated(value):
        if isinstance(value, bool):
            return not value
        if isinstance(value, (int, float)):
            return value + 1
        if isinstance(value, str):
            return value + "_MUTATED"
        if isinstance(value, list):
            return [*value, "MUTATED"]
        return "MUTATED"

    settings = harness.protocol()
    assert not harness._conformance_problems(settings), "the tracked manifest is not conformant"

    survived = set()
    for path, value in _settings_leaves(settings):
        probe = copy.deepcopy(settings)
        node, keys = probe, path.split(".")
        for key in keys[:-1]:
            node = node[key]
        node[keys[-1]] = mutated(value)
        if not harness._conformance_problems(probe):
            survived.add(path)

    assert survived == set(DECLARATIVE_SETTINGS), (
        "leaves that drift unnoticed but are not declared prose: "
        f"{sorted(survived - set(DECLARATIVE_SETTINGS))}; declared prose that is nonetheless "
        f"bound: {sorted(set(DECLARATIVE_SETTINGS) - survived)}"
    )


def test_the_protocol_readme_states_the_frozen_detector_settings():
    """§5.1 is where a reader looks up the detector, so it must not hold withdrawn values.

    Added 2026-09-03. ADR 0030 re-froze the detector on 2026-09-02 and §0 and §5.3 of the
    protocol README were updated. §5.1 kept the package's version-0.9.3 defaults and read as
    current for a day. Derived from the manifest here rather than retyped.
    """
    from allo.inputs import ROOT
    from allo.scoring.harness import protocol

    detector = protocol()["decoys"]["detector_settings"]
    section = (ROOT / "docs/benchmark/evaluation/README.md").read_text()
    section = section[section.index("### 5.1 The detector") :].split("### 5.2")[0]
    for field in ("step", "probe_in", "probe_out", "removal_distance", "volume_cutoff"):
        value = detector[field]
        assert f"{field} {value}" in section or f"**{field} {value}" in section, (
            f"§5.1 does not state the frozen {field} of {value}"
        )


def _readme_rows(section: str) -> dict[str, list[str]]:
    """Every `| `arm` | ... |` row in one README section, keyed by arm."""
    rows = {}
    for line in section.splitlines():
        match = re.match(r"^\|\s*`(\w+)`\s*\|(.*)\|\s*$", line)
        if match:
            rows[match.group(1)] = [
                cell.replace("*", "").strip() for cell in match.group(2).split("|")
            ]
    return rows


def test_the_protocol_readme_quotes_the_numbers_its_own_sources_hold():
    """Four tables in the protocol README restate a freeze or an experiment. Derive them.

    Added 2026-09-03 by the round-5 audit, which found three separate drifts in these four
    tables and no test that could see any of them:

    - §5.3's `detected` column held `decoys + 1` on all fifteen rows, not `n_detected`.
    - §6.1 quoted `alpha_star` 0.02771 for `bcr_abl1_mandated` against the freeze's 0.02774.
    - §7.1's three tables still held the version 2 chain-A row for `bcr_abl1_mandated` and
      omitted `cardiac_myosin_mandated` entirely.

    Each was a hand-typed restatement of a machine-written number. One parser closes all four,
    and a fifth table added later is not covered until it is named here.
    """
    from allo.inputs import ROOT
    from allo.scoring.harness import EVALUATION_FROZEN

    readme = (ROOT / "docs/benchmark/evaluation/README.md").read_text()
    targets = json.loads(EVALUATION_FROZEN.read_text())["targets"]

    def section(start: str, end: str) -> str:
        return readme[readme.index(start) :].split(end)[0]

    decoys = _readme_rows(section("### 5.3 What the detector found", "At the version-2"))
    assert len(decoys) == len(targets), "§5.3 must carry every frozen arm"
    for arm, cells in decoys.items():
        frozen = targets[arm]["decoys"]
        pockets, halo = frozen["pockets"], frozen["excluded_by_halo"]
        lining = len({residue for pocket in pockets.values() for residue in pocket["lining"]})
        expected = [
            str(frozen["n_detected"]),
            str(len(halo)),
            str(len(pockets)),
            str(lining),
            f"{frozen['site_pocket']['label_coverage']:.4f}",
            f"{frozen['minimum_attainable_p']:.6f}",
        ]
        assert cells == expected, f"§5.3 row {arm}: README {cells}, freeze {expected}"

    gate = _readme_rows(section("### 6.1 The gate failed", "**Re-measured at protocol"))
    assert len(gate) == len(targets), "§6.1 must carry every frozen arm"
    for arm, cells in gate.items():
        patch = targets[arm]["matched_patch"]
        assert cells[-2:] == [f"{patch['alpha_star']:.5f}", f"{patch['size_ratio']:.4f}"], (
            f"§6.1 row {arm} does not quote the frozen calibration"
        )

    measured = json.loads(
        (ROOT / "experiments/2026-09-02-null-recalibration/metrics.json").read_text()
    )["power"]
    for start, end, level in (
        ("**At α, the loosest threshold", "**At α/3, the tightest.**", "alpha"),
        ("**At α/3, the tightest.**", "The effective raw-p threshold", "alpha/3"),
    ):
        rows = _readme_rows(section(start, end))
        assert set(rows) == set(measured), f"§7.1 at {level} must carry every measured arm"
        for arm, cells in rows.items():
            scale = measured[arm][level]["by_length_scale"]
            expected = [
                f"{scale[s]['shift']:.2f} / {scale[s]['auc_roc']:.3f}"
                for s in ("4.0", "8.0", "12.0", "20.0")
            ]
            assert cells == expected, f"§7.1 {level} row {arm}: README {cells}, run {expected}"

    thresholds = _readme_rows(section("The effective raw-p threshold behind", "**Read it as"))
    assert set(thresholds) == set(measured), "the threshold table must carry every measured arm"
    for arm, cells in thresholds.items():
        expected = [
            f"{measured[arm][level]['alpha']:.4f}" for level in ("alpha", "alpha/2", "alpha/3")
        ]
        assert cells == expected, f"threshold row {arm}: README {cells}, run {expected}"


def test_every_endpoint_the_record_writes_is_declared_in_the_manifest():
    """`endpoints.reported` is a declaration, and until round 6 nothing checked it.

    `score_arm` wrote `top_5_components` into every record from ADR 0030 onward, the omission
    rationale for `top_5_fragmentation` said "added, see `reported` above", and `reported` did
    not hold it. A reported endpoint that no declaration names is the mirror of the rule the
    list exists to enforce, so this derives the written set from the source rather than
    restating it.

    One direction only, and the reason is stated rather than excepted away: two declared names
    -- `auc_roc_vs_decoy_linings` is not one of them, it is written here -- live under `nulls`
    and not in this block. `label_rank_vs_decoy_linings` is written as `nulls.decoy_pockets.
    label_p`, which the manifest now says beside the entry. Checking that direction by name
    would need a second map, and a map is the thing this test exists to avoid.
    """
    import ast
    import inspect

    from allo.scoring import harness

    tree = ast.parse(inspect.getsource(harness))
    k = harness.protocol()["endpoints"]["top_k"]

    def resolved(node: ast.expr) -> str | None:
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            return node.value
        if isinstance(node, ast.JoinedStr):
            parts = []
            for piece in node.values:
                if isinstance(piece, ast.Constant):
                    parts.append(str(piece.value))
                elif isinstance(piece, ast.FormattedValue) and _is_k(piece.value):
                    parts.append(str(k))
                else:
                    return None
            return "".join(parts)
        return None

    def _is_k(node: ast.expr) -> bool:
        return isinstance(node, ast.Name) and node.id == "k"

    written: set[str] = set()
    for function in ast.walk(tree):
        if not (isinstance(function, ast.FunctionDef) and function.name == "score_arm"):
            continue
        for node in ast.walk(function):
            if not (isinstance(node, ast.Dict) and node is not None):
                continue
            for key, value in zip(node.keys, node.values, strict=True):
                if resolved(key) == "endpoints" and isinstance(value, ast.Dict):
                    written = {resolved(inner) for inner in value.keys}
    assert written and None not in written, f"the endpoints block did not parse: {written}"

    settings = harness.protocol()
    declared = {settings["endpoints"]["confirmatory"], *settings["endpoints"]["reported"]}
    assert written <= declared, (
        f"endpoints the record writes that no declaration names: {sorted(written - declared)}"
    )


def test_the_simulation_ranks_agree_with_the_shipped_statistic():
    """`simulate._ranks` names this test and it did not exist until round 6.

    The docstring at `src/allo/scoring/simulate.py` says the simulation's ranking "is the same
    call" as `metrics.rank_vector` and that this test "pins that they agree". Nothing checked
    it, and the reason to check it is that the simulation already got this wrong once: it
    assigned ordinal ranks by stable sort until 2026-09-03, so `cluster_blocks` -- whose whole
    construction is tied blocks -- had every tie broken by residue index, which runs along the
    chain and therefore correlates with space. The published cells were not the statistic they
    claimed to be.

    Ties are the whole point, so the fixture is built to have them.
    """
    import numpy as np

    from allo.scoring.metrics import rank_vector
    from allo.scoring.simulate import _ranks

    rng = np.random.default_rng(0)
    fields = np.round(rng.normal(size=(64, 7)) * 2).astype(float)
    distinct = [len(np.unique(column)) for column in fields.T]
    assert max(distinct) < 64, "the fixture has no ties, so it cannot see the defect"

    simulated = _ranks(fields)
    for column in range(fields.shape[1]):
        shipped = rank_vector(fields[:, column])
        assert np.allclose(simulated[:, column], shipped), (
            f"column {column}: the simulation's ranks are not the shipped statistic's"
        )

    # And the defect itself: ordinal ranks would pass a shape check and fail this one.
    from scipy.stats import rankdata

    ordinal = rankdata(fields, method="ordinal", axis=0).astype(np.float32)
    assert not np.allclose(ordinal, simulated), "the fixture cannot distinguish the two methods"


def test_no_decision_function_accepts_a_non_finite_p_value():
    """Round 6, from a codex adversarial pass. `nan <= 0` and `nan > 1` are both false.

    So `np.any((values <= 0) | (values > 1))` let a NaN through, and the consequence is not
    only a record that serialises as bare `NaN`, which is not JSON. `holm` sorts the NaN
    FIRST, gives it the tightest threshold, fails to reject it, and the step-down then stops:
    measured on the frozen confirmatory family, one NaN turned two rejections at p = 0.01 into
    none.

    `_aligned` was given the identical guard earlier in this round, for the identical reason,
    and the multiplicity path was left with the hole. That is the root-cause lesson here, so
    the check lives in one function that all four entry points call.
    """
    import math

    from allo.scoring.harness import calibrated_p, combine_arms, holm, protocol

    family = sorted(protocol()["decision"]["confirmatory_family"])
    for bad in (math.nan, math.inf, -math.inf, 0.0, -0.5, 1.5):
        pvalues = dict.fromkeys(family, 0.01)
        pvalues[family[0]] = bad
        with pytest.raises(ValueError, match="finite"):
            combine_arms(pvalues)
        with pytest.raises(ValueError, match="finite"):
            holm(pvalues, alpha=0.05)
    for bad in (math.nan, math.inf, 0.0, 1.5):
        with pytest.raises(ValueError, match="finite"):
            calibrated_p(bad, 1.2)

    # The SIZE RATIO needed the same guard and did not have it, one argument over. A NaN there
    # is the dangerous direction: `norm.sf(nan)` is nan, `max(p, nan)` returns p, so the
    # calibration silently disappears and the raw p-value reaches Holm untightened. A ratio
    # below 1 was clamped up, which hid a broken gate instead of reporting it.
    for bad in (math.nan, math.inf, -math.inf, 0.0, -3.0, 0.5):
        with pytest.raises(ValueError, match="size ratio"):
            calibrated_p(0.01, bad)

    # And the family still works, so the guard is a filter and not a wall.
    valid = dict.fromkeys(family, 0.01)
    assert all(row["reject"] for row in holm(valid, alpha=0.05).values())
    assert combine_arms(valid)["p"] < 0.05
    assert calibrated_p(0.01, 1.2) >= 0.01


def test_the_verdict_applies_the_frozen_decision_rule_and_no_other():
    """Round 6, from a codex adversarial pass. `settings` was a way to supply your own test.

    It exists so that a test can run a cheap protocol -- fewer replicates, a smaller sampler
    budget. It also let a caller replace the DECISION block, and
    `settings["decision"]["alpha"] = 2.0` makes every Holm threshold exceed 1, so three
    p-values at 0.6 clear both families with every guard green. Measured before the fix.

    This is the argument `apo_input` makes for having no `manifest` parameter: "every method
    saw identical inputs" has to be true by construction, and so does "every method faced the
    same decision rule". `holm` is public and callable directly, so it checks alpha itself.
    """
    import copy
    import math

    from allo.scoring.harness import confirmatory_verdict, holm, protocol

    family = sorted(protocol()["decision"]["confirmatory_family"])
    claim = {
        arm: {
            "comparison": "mine against cavity_volume",
            "leader": "mine",
            "p_calibrated": 0.6,
        }
        for arm in family
    }

    for field, value in (
        ("alpha", 2.0),
        ("alpha", 0.5),
        ("correction", "bonferroni"),
        ("sided", "two"),
    ):
        settings = copy.deepcopy(protocol())
        settings["decision"][field] = value
        with pytest.raises(ValueError, match="FROZEN decision rule"):
            confirmatory_verdict(dict.fromkeys(family, 0.6), claim, settings=settings)

    for alpha in (2.0, 0.0, 1.0, -0.1, math.nan, math.inf):
        with pytest.raises(ValueError, match="significance level"):
            holm(dict.fromkeys(family, 0.01), alpha=alpha)

    # A cheaper NULL is still allowed, which is what the parameter is for.
    cheap = copy.deepcopy(protocol())
    cheap["nulls"]["replicates"] = 199
    assert confirmatory_verdict(dict.fromkeys(family, 0.001), settings=cheap)["family_1"][
        "n_reject"
    ] == len(family)
