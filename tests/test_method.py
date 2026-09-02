"""The method layer: graph construction, the classical battery, the quantum observables.

Two of these tests are not unit tests but derivation checks. `quantum_survival_time` and
`dephased_transport` each replace an N-fold time integration with one linear solve, and the
algebra behind each is short enough to get wrong silently — the dephasing solve was driven
by the wrong right-hand side on its first version and landed within 15 % of the truth, which
is exactly the error a plausible-looking number hides. Both are checked against direct
numerical integration of the equation they claim to solve.
"""

from __future__ import annotations

import numpy as np
import pytest
from scipy.integrate import solve_ivp

from allo import network
from allo.classical import baselines, postprocess
from allo.inputs import apo_input
from allo.quantum import connectivity, interference, quantumness, walk

TARGET = "mkp5"  # the smallest frozen arm, so every check here runs in seconds


@pytest.fixture(scope="module")
def apo():
    return apo_input(TARGET)


@pytest.fixture(scope="module")
def graph(apo):
    return network.build(apo)


def test_the_default_graph_is_the_evaluation_graph(apo, graph):
    """The method's default cutoff and contact rule reproduce the frozen evaluation graph.

    Not a coincidence to be preserved: it is what makes "our graph beats the default" an
    ablation with a meaningful zero point rather than a comparison of two arbitrary graphs.
    """
    from allo.scoring.nulls import evaluation_graph

    reference = evaluation_graph(apo)
    assert graph.order == reference.order
    assert graph.source == reference.source
    for residue, neighbours in zip(reference.order, reference.adjacency, strict=True):
        row = graph.weight[graph.position[residue]]
        assert set(np.array(graph.order)[row > 0].tolist()) == set(neighbours)


def test_every_scorer_returns_one_finite_score_per_node(graph):
    for name, scorer in (baselines.SCORERS | walk.SCORERS).items():
        values = scorer(graph)
        assert values.shape == (graph.n,), name
        assert np.all(np.isfinite(values)), name


def test_scores_carry_residue_identity(graph):
    scores = graph.as_scores(baselines.degree(graph))
    assert set(scores) == set(graph.order)
    with pytest.raises(ValueError):
        graph.as_scores(np.zeros(graph.n + 1))


def test_an_isolated_node_is_refused_rather_than_scored(apo):
    """A cutoff of 2.0 A is not enough to isolate anything: the peptide C-N bond is 1.33 A,
    so every residue keeps its sequence neighbours. 1.0 A empties the graph, which is the
    case the guard exists for."""
    with pytest.raises(ValueError, match="no contact"):
        network.build(apo, cutoff=1.0)


def test_coherent_survival_time_matches_direct_integration(graph):
    """One Sylvester solve against `int <psi|psi> dt` integrated node by node."""
    closed = -walk.quantum_survival_time(graph, "adjacency", trapping=1.0)
    hamiltonian = walk.hamiltonian(graph, "adjacency").astype(complex)
    projector = np.zeros((graph.n, graph.n))
    projector[graph.source_index, graph.source_index] = 1.0
    # The reference must carry the same uniform background decay the solve does. Without it
    # the Sylvester system is ill-conditioned on a large graph, and it fails silently: on
    # `hiv_rt` it returned survival times of the wrong sign and 1e13 in magnitude.
    from scipy.linalg import eigh as _eigh

    width = float(np.ptp(_eigh(hamiltonian.real, eigvals_only=True)))
    background = walk.SURVIVAL_BACKGROUND * width
    effective = hamiltonian - 0.5j * (projector + background * np.eye(graph.n))

    for node in (0, graph.n // 2, graph.n - 1):
        start = np.zeros(graph.n, dtype=complex)
        start[node] = 1.0
        solved = solve_ivp(
            lambda t, y: -1j * (effective @ y),
            [0.0, 400.0],
            start,
            method="DOP853",
            rtol=1e-9,
            atol=1e-11,
            dense_output=True,
        )
        grid = np.linspace(0.0, 400.0, 20001)
        integrated = np.trapezoid((np.abs(solved.sol(grid)) ** 2).sum(axis=0), grid)
        assert closed[node] == pytest.approx(integrated, rel=5e-3)


def test_dephased_transport_matches_direct_lindblad_integration(graph):
    """One Krylov solve against the Lindblad equation integrated node by node."""
    closed = -walk.dephased_transport(graph, "adjacency", dephasing=1.0, trapping=1.0)
    hamiltonian = walk.hamiltonian(graph, "adjacency").astype(complex)
    projector = np.zeros((graph.n, graph.n))
    projector[graph.source_index, graph.source_index] = 1.0

    def lindblad(t, flat):
        rho = flat.reshape(graph.n, graph.n)
        derivative = -1j * (hamiltonian @ rho - rho @ hamiltonian)
        derivative -= rho - np.diag(np.diag(rho))
        derivative -= 0.5 * (projector @ rho + rho @ projector)
        return derivative.ravel()

    for node in (0, graph.n - 1):
        start = np.zeros((graph.n, graph.n), dtype=complex)
        start[node, node] = 1.0
        solved = solve_ivp(
            lindblad,
            [0.0, 400.0],
            start.ravel(),
            method="DOP853",
            rtol=1e-8,
            atol=1e-10,
            dense_output=True,
        )
        grid = np.linspace(0.0, 400.0, 4001)
        trace = np.real(solved.sol(grid).reshape(graph.n, graph.n, -1).trace(axis1=0, axis2=1))
        assert closed[node] == pytest.approx(np.trapezoid(trace, grid), rel=5e-3)


def test_the_time_average_converges_to_the_phase_free_overlap(graph):
    """As the window grows, the time-averaged transfer converges to `sum_k |<i|k>|^2 |<k|s>|^2`.

    This is the claim the report rests on when it says the time-averaged transfer metric
    keeps no interference in the limit. It is checked rather than asserted, and it is worth
    checking because the *finite* window this module actually uses has not converged: the
    default 50-revolution window correlates about 0.92 with the limit, not 1.00. Both are
    therefore kept as separate observables.
    """
    values, vectors = walk._eigen(graph, "adjacency")
    limit = walk.ctqw_infinite_time_average(graph, "adjacency")
    previous = 0.0
    for span in (200.0, 2000.0, 20000.0):
        grid = np.linspace(0.0, span, 40001)
        correlation = np.corrcoef(walk._amplitudes(graph, "adjacency", grid).mean(axis=0), limit)[
            0, 1
        ]
        assert correlation > previous
        previous = correlation
    assert previous > 0.999

    default_window = walk.ctqw_average_transfer(graph, "adjacency")
    assert np.corrcoef(default_window, limit)[0, 1] < 0.99


def test_the_decay_fit_cannot_see_a_label(graph):
    """S6's C1 guarantee, checked the way the pipeline decomposition specifies it.

    Permuting a label set must leave `k` bit-identical. It does, because no function in
    `postprocess` accepts a label set at all — this test is what makes that structural fact
    an enforced one.
    """
    apo = apo_input(TARGET)
    distance = network.min_heavy_distance_to(apo, graph.source)
    scores = graph.as_scores(baselines.degree(graph))
    first, fit_a = postprocess.decay_residual(scores, distance, graph.source)

    shuffled = dict(reversed(list(scores.items())))
    second, fit_b = postprocess.decay_residual(shuffled, distance, graph.source)
    assert fit_a["k"] == fit_b["k"]
    assert first == second

    # And the stage takes no label argument at all, which is the structural half of the
    # guarantee: there is no route by which a label set could reach the fit.
    import inspect

    for name in ("fit_decay", "decay_residual"):
        parameters = set(inspect.signature(getattr(postprocess, name)).parameters)
        assert not parameters & {"labels", "positives", "truth", "site"}


def test_diversified_selection_reduces_to_the_plain_cut_at_radius_zero(graph):
    scores = graph.as_scores(baselines.degree(graph))
    coord = {r: graph.coord[i] for i, r in enumerate(graph.order)}
    plain = sorted(scores, key=lambda r: -scores[r])[:5]
    assert postprocess.diversified_top_k(scores, coord, k=5, exclusion_radius=0.0) == plain

    spread = postprocess.diversified_top_k(scores, coord, k=5, exclusion_radius=10.0)
    assert len(spread) == 5
    chosen = np.array([coord[r] for r in spread])
    separation = np.linalg.norm(chosen[:, None, :] - chosen[None, :, :], axis=-1)
    assert separation[np.triu_indices(5, 1)].min() > 10.0


def test_the_connectivity_matrix_is_symmetric_and_row_stochastic(graph):
    """The required N x N deliverable, checked against the two properties that define it.

    Entry (i, j) is a transfer probability, so each row is a distribution over destinations
    and the matrix is symmetric because `exp(-iHt)` is symmetric for symmetric `H`. Neither
    property survives an index transposition or a missing normalisation, which is exactly
    the class of error that produces a plausible-looking matrix.
    """
    for mode in ("finite", "infinite"):
        matrix = connectivity.connectivity_matrix(graph, mode=mode, steps=64)
        assert matrix.shape == (graph.n, graph.n)
        assert np.isfinite(matrix).all()
        assert np.abs(matrix - matrix.T).max() < 1e-12
        assert np.abs(matrix.sum(axis=1) - 1.0).max() < 1e-10


def test_the_interference_free_term_is_a_column_sum_of_the_infinite_time_matrix(graph):
    """`interference._overlap` and `connectivity_matrix(mode="infinite")` are one object.

    Both are the T -> infinity transfer probability, one summed over the source and one for
    every pair. If the two disagree, one of them has its indices the wrong way round, and
    the interference scorers subtract a term that is not their own classical limit. Since
    2026-09-02 `_overlap` calls the matrix rather than writing the formula out a second
    time, so this also pins that they cannot drift apart again.
    """
    overlap = interference._overlap(graph, "adjacency")
    matrix = connectivity.connectivity_matrix(graph, form="adjacency", mode="infinite")
    assert np.abs(overlap - matrix[:, graph.source_index].sum(axis=1)).max() < 1e-12


def test_the_infinite_time_matrix_ignores_the_degenerate_basis(graph):
    """The T -> infinity limit must be a property of the operator, not of LAPACK.

    Time-averaging `|<i|exp(-iHt)|j>|^2` cancels the cross term between two eigenvectors
    only when their phases differ, so a degenerate pair keeps its cross term and the limit
    is `sum_m |<i|P_m|j>|^2` over spectral projectors. The old code wrote
    `sum_k |<i|k>|^2 |<k|j>|^2`, which agrees on a simple spectrum and, on a degenerate
    one, returns whichever answer the arbitrary basis of the degenerate eigenspace gives.

    The degeneracy is forced rather than found, because no frozen arm is guaranteed to
    carry one and the property must hold whether or not today's arm does.
    """
    values, vectors = walk._eigen(graph, "adjacency")
    forced = values.copy()
    forced[1] = forced[0]
    theta = 0.7
    turn = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
    rotated = vectors.copy()
    rotated[:, :2] = vectors[:, :2] @ turn

    def matrix_from(basis: np.ndarray) -> np.ndarray:
        graph.cache["h_eigen:adjacency"] = (forced, basis)
        try:
            return connectivity.connectivity_matrix(graph, mode="infinite")
        finally:
            graph.cache.pop("h_eigen:adjacency", None)

    plain, turned = matrix_from(vectors), matrix_from(rotated)
    assert np.abs(plain - turned).max() < 1e-10, (
        "the infinite-time matrix moved when only the degenerate basis changed"
    )
    # A guard that cannot fail is not a guard: the old construction really does move.
    before = (vectors**2) @ (vectors**2).T
    after = (rotated**2) @ (rotated**2).T
    assert np.abs(before - after).max() > 1e-6, (
        "the forced degeneracy does not reach the old formula, so this proves nothing"
    )


def test_the_active_site_source_energy_brackets_zero_on_the_adjacency_form(graph):
    """The Faccin diagnosis, as an enforced fact rather than a recalled one.

    The adjacency matrix has no self-loops, so its diagonal is zero and the source block has
    zero trace. The block's eigenvalues therefore sum to zero, so the extremal source states
    bracket zero and a single-residue source sits exactly on it. That zero is why the
    time-averaged walk reproduced the classical degree ranking (`docs/method/exploration/
    results/47-quantum-constructions.md`), so a change here changes that conclusion.
    """
    matrix = walk.hamiltonian(graph, "adjacency")
    assert np.abs(np.diag(matrix)).max() == 0.0

    high = quantumness.source_energy(graph, "adjacency", high=True)
    low = quantumness.source_energy(graph, "adjacency", high=False)
    assert low <= 0.0 <= high

    # And the gap the bound divides by is non-zero, which is what makes `E / Delta` finite.
    assert quantumness.spectral_gap(graph, "adjacency") > 0.0
