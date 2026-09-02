"""The evaluation layer: metrics, the matched-patch null, and the freeze that pins them.

Offline throughout. Where a test needs the harness end to end it overrides the replicate
count, because the frozen 9999 is a scoring setting and not a test setting.
"""

from __future__ import annotations

import copy
import json

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
    (ADR 0029), 17 labels in 354 candidates against 20 in 440, and `cardiac_myosin_mandated`
    is a new arm (ADR 0031). The other three must not move.
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

    `cardiac_myosin_mandated` is the most fragmented at (7, 4, 1), against (8, 4) for the same
    twelve residues on the measured `9GZ3` structure. The label sets are identical, so the
    difference is entirely the homology model's contact graph — the same defect ADR 0031
    measures as a long-range contact Jaccard of 0.471, seen here from the label set's own side.
    """
    expected = {
        "kras_g12c_mandated": (16,),
        "kras_g12c_corrected": (16,),
        "bcr_abl1_mandated": (17,),
        "bcr_abl1_corrected": (17, 1),
        "cardiac_myosin_mandated": (7, 4, 1),
        "cardiac_myosin_corrected": (8, 4),
    }
    assert set(expected) == set(PRIMARY), "every frozen arm needs a pinned component structure"
    for target, sizes in expected.items():
        graph = evaluation_graph(apo_input(target))
        assert component_sizes(graph, PRIMARY[target]["scoreable_label_residues"]) == sizes


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
    for target, record in EVALUATION.items():
        star = record["matched_patch"]["alpha_star"]
        assert 0 < star <= alpha, f"{target}: alpha_star {star} is not a tightening of {alpha}"
        ratio = record["matched_patch"]["size_ratio"]
        assert ratio >= 1.0, f"{target}: size_ratio {ratio} would loosen the test"


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
    for target, record in EVALUATION.items():
        assert record["matched_patch"]["alpha_star"] == pytest.approx(gate[target]["alpha_star"])
        assert record["matched_patch"]["size_ratio"] == pytest.approx(gate[target]["size_ratio"])


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
    for target, record in EVALUATION.items():
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
    """
    floors = {"a": 0.25, "b": 0.1, "c": 0.04}
    combined = harness.combine_arms(floors)
    assert combined["p"] < min(floors.values()), "combination must beat every per-arm floor"
    assert combined["tests"] == "intersection null: no arm has signal"
    assert combined["arms"] == sorted(floors)
    assert combined["p_per_arm"] == floors
    # Identical inputs, both directions: a uniform p-vector must not reject.
    assert harness.combine_arms(dict.fromkeys("abc", 0.5))["p"] > 0.05


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
    with pytest.raises(ValueError, match="family_2 must be exactly"):
        harness.confirmatory_verdict(
            dict.fromkeys(declared, 0.01), dict.fromkeys(declared[:1], 0.01)
        )
    both = harness.confirmatory_verdict(
        dict.fromkeys(declared, 0.01), dict.fromkeys(list(claim["arms"]), 0.01)
    )
    assert both["family_2"]["reference"] == "cavity_volume"
    assert both["family_2"]["sided"] == "two"
