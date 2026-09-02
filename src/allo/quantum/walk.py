"""Quantum propagation observables on the residue graph (pipeline stage S5).

Every function takes a :class:`~allo.network.graph.ResidueGraph` and returns one float per
node, higher meaning *more likely allosteric*, exactly like `allo.classical.baselines`. That
symmetry is deliberate: the frozen harness scores both through one path, so a quantum number
and a classical number are comparable by construction rather than by argument.

**What is simulated, and what is claimed.** The encoding is one qubit per residue in the
single-excitation sector, so an N-residue graph is an N-dimensional Hilbert space and every
observable here is a statevector calculation on a dense N x N operator. That is the
classical simulation of the circuit `docs/method/review/08-hardware-viability.md` prices at
`N(N-1)/2` two-qubit gates at depth `N` on a linear chain. Nothing here claims a quantum
speed-up: the full deliverable runs in milliseconds. What the circuit buys is the hardware
demonstration (C3, C4), and what these observables have to earn is accuracy.

**Why this module exists at all, given a prior negative result.** `00-conventions.md` §5
records eleven quantum insertion points a teammate measured and closed. Those measurements
ran on a different benchmark, with a different graph and a different scoring rule. The
principal investigator's standing instruction is that a method is not closed until an
experiment on *this* frozen benchmark produces a number. Every observable below is therefore
implemented to be measured, including the ones that prior work expects to fail.

**One structural fact governs the design.** A single-excitation Hermitian walk on a real
symmetric graph carries no information beyond its transfer amplitudes, and its infinite-time
average is manifestly interference-free. Two of the constructions here deliberately break
that: `quantum_survival_time` adds a non-Hermitian sink at the active site, and
`dephased_transport` adds Lindblad dephasing. Both are physically motivated and neither
imports MD or holo data, so both stay inside C1, C2 and C6.

Prediction-path code. It never imports `allo.groundtruth` or `allo.scoring`.
"""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np
import scipy.sparse.linalg as spla
from scipy.linalg import eigh, solve_sylvester

from allo.network.graph import ResidueGraph

__all__ = ["SCORERS", "hamiltonian"]

_FLOOR = 1e-12
# Above this node count the dense Liouvillian solve stops being worth its wall clock, and
# the observable is reported as unavailable rather than approximated. Stated here so the
# ceiling is a declared limit rather than a crash.
#
# What the ceiling admits and refuses, because the asymmetry is a scalability claim and not
# an implementation detail. It admits every arm of the tuning tier -- mkp5 147, ptp1b 298,
# hiv_rt 543, ns5b 553. It refuses `cardiac_myosin_corrected` at 764, which is a *scored
# deliverable target*, and `p97_vcp` at 723 and `ecoli_cps` at 1058 in the generalisation
# tier. An observable selected on four arms that all fit, and unavailable on a target the
# submission has to deliver, must be reported as exactly that. It is not a reason to raise
# the constant: the cost is O(N^2) state with an O(N^3) matvec, so raising it moves the wall
# and does not remove it. Coarse-graining is the answer, and that is Phase 4.
DEPHASING_MAX_NODES = 620


def hamiltonian(graph: ResidueGraph, form: str) -> np.ndarray:
    """The single-excitation Hamiltonian.

    * `adjacency` — H = A. The XY hopping model. Its ground state is the Perron vector, so a
      walk on it is the construction that reproduces eigenvector centrality.
    * `laplacian` — H = L = D - A. Adds an on-site energy equal to the residue's degree,
      which is the term that makes a buried residue energetically distinct from an exposed
      one. Physically it is the harmonic-network Hamiltonian, so it is the form the elastic
      network hypothesis (C6) actually implies.
    * `normalised_laplacian` — H = I - D^-1/2 A D^-1/2. The degree-normalised form, which
      removes the burial gradient the plain Laplacian introduces.
    """
    if form == "adjacency":
        return graph.adjacency.copy()
    if form == "laplacian":
        return graph.laplacian
    if form == "normalised_laplacian":
        inverse_root = 1.0 / np.sqrt(np.maximum(graph.degree, _FLOOR))
        return np.eye(graph.n) - inverse_root[:, None] * graph.adjacency * inverse_root[None, :]
    raise ValueError(f"unknown Hamiltonian form {form!r}")


def _eigen(graph: ResidueGraph, form: str) -> tuple[np.ndarray, np.ndarray]:
    return graph.memo(f"h_eigen:{form}", lambda: eigh(hamiltonian(graph, form)))


def _time_grid(
    graph: ResidueGraph, form: str, steps: int, window: float = 50.0, scale: str = "range"
) -> np.ndarray:
    """A time grid set by the operator's own spectral width, not by a hand-picked constant.

    The fastest phase in `exp(-iHt)` turns at the spectral range, so `t = 2 pi / range` is
    one full revolution of it. Sampling out to `window` of those covers the slow modes on
    every arm without a per-target number, which keeps the grid a property of the graph
    rather than a hyperparameter.

    `window` is the exception, and it is exposed rather than hidden because the challenge
    asks for stability of the metric under limited coherence times (CHALLENGE.md §4.2).
    A coherence limit is a shortened window, so sweeping this parameter is how that
    requirement is measured. The default reproduces every result recorded before
    2026-08-26.

    `scale` chooses **which end of the spectrum sets the unit of time**, and the choice is not
    cosmetic. `range` divides by the spectral range, which is the fastest phase in the
    operator. `gap` divides by the gap next to the dominant eigenvalue, which is the slowest
    beat the walk can produce. On the four `development` arms the range varies by a factor of
    1.09 between proteins and the gap by a factor of 21.7, so a window fixed in units of the
    range is a **different physical experiment on every protein**: it covers 1.81 periods of
    the slowest mode on `mkp5` and 0.084 of one on `hiv_rt`. Setting `scale="gap"` makes the
    window a fixed number of slow-mode periods instead, which is a per-protein adaptation that
    reads only the graph's own spectrum and never a label.

    It is not free. A longer window converges toward the infinite-time average, and that
    average is exactly the classical answer for a zero-energy initial state
    (`allo.quantum.quantumness`). `gap` also needs more `steps` to avoid aliasing the fast
    modes: at least `2 * range / gap` samples, which is 342 on `hiv_rt` for one period.
    """
    values, _ = _eigen(graph, form)
    if scale == "range":
        unit = max(float(values.max() - values.min()), _FLOOR)
    elif scale == "gap":
        unit = max(float(abs(values[-1] - values[-2])), _FLOOR)
    else:
        raise ValueError(f"unknown scale {scale!r}; have 'range' and 'gap'")
    return np.linspace(0.0, float(window) * 2.0 * np.pi / unit, steps)


def _amplitudes(graph: ResidueGraph, form: str, times: np.ndarray) -> np.ndarray:
    """|<i|exp(-iHt)|s>|^2 summed over source residues s, shaped (len(times), N).

    The sum over source residues is incoherent: each active-site residue is treated as an
    independent injection point. `ctqw_coherent_source_contrast` measures what the coherent
    alternative changes, which is the only place in this module where the difference between
    the two is itself the observable.
    """
    values, vectors = _eigen(graph, form)
    source = vectors[graph.source_index, :]
    phases = np.exp(-1j * np.outer(times, values))
    out = np.zeros((len(times), graph.n))
    for row in range(source.shape[0]):
        amplitude = (vectors * source[row][None, :]) @ phases.T
        out += np.abs(amplitude.T) ** 2
    return out


def ctqw_average_transfer(
    graph: ResidueGraph,
    form: str = "adjacency",
    steps: int = 512,
    window: float = 50.0,
    scale: str = "range",
) -> np.ndarray:
    """Time-averaged transfer probability from the active site over a finite window.

    The candidate metric ADR 0002 lists first. Reported for the finite window rather than
    the infinite-time limit, because the infinite-time average has a closed form,
    `sum_k |<i|k>|^2 |<k|s>|^2`, in which every phase has cancelled — it is a spectral
    overlap and contains no interference at all. `ctqw_infinite_time_average` computes that
    limit separately, so the difference between the two is measurable rather than assumed.
    """
    times = _time_grid(graph, form, steps, window, scale)
    return _amplitudes(graph, form, times).mean(axis=0)


def ctqw_infinite_time_average(graph: ResidueGraph, form: str = "adjacency") -> np.ndarray:
    """The T -> infinity limit: sum_k |<i|k>|^2 |<k|s>|^2. Interference-free by construction.

    Included so the report can state, with a number rather than an argument, how much of the
    finite-window score is interference and how much is spectral overlap.
    """
    _, vectors = _eigen(graph, form)
    weight = (vectors[graph.source_index, :] ** 2).sum(axis=0)
    return (vectors**2) @ weight


def ctqw_peak_transfer(
    graph: ResidueGraph,
    form: str = "adjacency",
    steps: int = 512,
    window: float = 50.0,
    scale: str = "range",
) -> np.ndarray:
    """The maximum transfer probability reached at any sampled time.

    A residue that receives a large transient population is coupled to the source even if
    the population leaves again. The time average cannot see that; this can.
    """
    times = _time_grid(graph, form, steps, window, scale)
    return _amplitudes(graph, form, times).max(axis=0)


def ctqw_temporal_variance(
    graph: ResidueGraph,
    form: str = "adjacency",
    steps: int = 512,
    window: float = 50.0,
    scale: str = "range",
) -> np.ndarray:
    """Variance in time of the transfer probability, divided by its mean.

    A classical diffusion on the same graph relaxes monotonically to its stationary
    distribution, so its normalised temporal variance decays. A coherent walk keeps
    oscillating, and the amplitude of that oscillation is set by how many eigenmodes overlap
    both the source and the residue. This is therefore one of the few observables in the
    module that has no classical counterpart on the same operator.
    """
    times = _time_grid(graph, form, steps, window, scale)
    trace = _amplitudes(graph, form, times)
    mean = trace.mean(axis=0)
    return trace.var(axis=0) / np.maximum(mean, _FLOOR)


def ctqw_coherent_source_contrast(
    graph: ResidueGraph,
    form: str = "adjacency",
    steps: int = 512,
    window: float = 50.0,
    scale: str = "range",
) -> np.ndarray:
    """Coherent-source transfer minus incoherent-source transfer.

    Inject the excitation as an equal-amplitude superposition over the active-site residues
    rather than one residue at a time, and subtract the incoherent result. What survives is
    exactly the cross-term between source residues — a direct, isolated measurement of
    interference between propagation routes leaving the active site. If interference carries
    signal anywhere in this problem, it is visible here or nowhere.
    """
    values, vectors = _eigen(graph, form)
    times = _time_grid(graph, form, steps, window, scale)
    phases = np.exp(-1j * np.outer(times, values))
    weights = vectors[graph.source_index, :].sum(axis=0) / np.sqrt(len(graph.source_index))
    coherent = np.abs(((vectors * weights[None, :]) @ phases.T).T) ** 2
    incoherent = _amplitudes(graph, form, times) / len(graph.source_index)
    return (coherent - incoherent).mean(axis=0)


# A uniform background decay, as a fraction of the operator's own spectral width. Without it
# the sink Sylvester solve breaks down on a large graph, and it breaks down silently: on
# `hiv_rt` at 543 nodes it returned survival times of -4.6e13, which is not a small error but
# a sign error of thirteen orders of magnitude, and the first four records of the method sweep
# carried it. The cause is conditioning. `solve_sylvester` needs the spectra of `H_eff^dagger`
# and `H_eff` to be separated, and their separation is `2 Im(lambda)`, which for an eigenvector
# with negligible overlap on a nine-residue sink inside a 543-node graph is numerically zero.
#
# The repair is physical rather than numerical. A real excitation has a finite lifetime, so
# `H_eff = H - i(kappa/2) P_S - i(gamma_0/2) I` with a small uniform `gamma_0` is the more
# honest operator, and it floors every imaginary part at `gamma_0/2`. It does not cancel from
# the ranking: a residue that drains quickly loses less to the background than one that does
# not. Every solve is checked for positivity afterwards, because a survival time is an
# integral of a non-negative quantity and cannot be negative.
SURVIVAL_BACKGROUND = 1e-3


def _survival(graph: ResidueGraph, form: str, trapping: float) -> np.ndarray:
    """Mean survival time per residue with a sink on the source. Positive by construction."""
    h = hamiltonian(graph, form).astype(complex)
    width = float(np.ptp(eigh(h.real, eigvals_only=True)))
    background = SURVIVAL_BACKGROUND * max(width, _FLOOR)
    projector = np.zeros((graph.n, graph.n))
    projector[graph.source_index, graph.source_index] = 1.0
    effective = h - 0.5j * (trapping * projector + background * np.eye(graph.n))
    solution = solve_sylvester(effective.conj().T, -effective, 1j * np.eye(graph.n))
    survival = np.real(np.diag(solution))
    if not np.all(np.isfinite(survival)) or survival.min() <= 0.0:
        raise ArithmeticError(
            f"{graph.target}: the sink Sylvester solve is ill-conditioned at trapping "
            f"{trapping} (minimum survival {survival.min():.3e}); the observable is refused "
            "rather than reported"
        )
    return survival


def quantum_survival_time(
    graph: ResidueGraph, form: str = "adjacency", trapping: float = 1.0
) -> np.ndarray:
    """Negated mean survival time of an excitation started at i, with a sink on the source.

    This is the quantum analogue of the classical hitting time, and it is the one
    construction here that is genuinely non-Hermitian without importing anything the
    constraints forbid: the sink is the active site, which the input layer already names.

    The effective Hamiltonian is `H_eff = H - i (kappa/2) P_S`, with `P_S` the projector onto
    the active-site residues. The survival integral
    `tau_i = integral_0^inf <psi_i(t)|psi_i(t)> dt` is the i-th diagonal entry of the matrix
    `X` solving the Sylvester equation `H_eff^dagger X - X H_eff = i I`, which follows from
    differentiating `exp(i H_eff^dagger t) exp(-i H_eff t)` and integrating. One O(N^3) solve
    gives every residue at once, so the whole deliverable costs a single decomposition.

    Negated, so that a short survival time — a residue whose excitation reaches the active
    site quickly — scores high.
    """

    def build():
        return -_survival(graph, form, trapping)

    return graph.memo(f"survival:{form}:{trapping}", build)


def quantum_perturbation_response(
    graph: ResidueGraph,
    form: str = "adjacency",
    strength: float = 1.0,
    steps: int = 128,
    window: float = 50.0,
    scale: str = "range",
) -> np.ndarray:
    """How much perturbing residue i changes propagation from the active site.

    ADR 0002's metric 5, and the only candidate on that list that
    `docs/method/review/03-quantum-methods.md` did not eliminate. Add `strength` to the
    on-site energy of residue i, recompute the time-averaged transfer from the source to
    every *other* residue, and score i by the L1 change. A residue that gates communication
    changes the whole transfer profile when it is detuned; a peripheral residue does not.

    This is the quantum counterpart of perturbation-response scanning, so the two should be
    read side by side: `allo.classical.baselines.anm_perturbation_response` asks the same
    question of an elastic network.

    Cost is N re-diagonalisations. File 03 priced 300 of them at 8.1e9 flops, which is
    seconds; at N = 1058 it is minutes, and it is the most expensive observable here.
    """

    def build():
        base_h = hamiltonian(graph, form)
        times = _time_grid(graph, form, steps, window, scale)
        baseline = _amplitudes(graph, form, times).mean(axis=0)
        score = np.zeros(graph.n)
        source = set(graph.source_index.tolist())
        for i in range(graph.n):
            if i in source:
                continue
            perturbed = base_h.copy()
            perturbed[i, i] += strength
            values, vectors = eigh(perturbed)
            phases = np.exp(-1j * np.outer(times, values))
            transfer = np.zeros((len(times), graph.n))
            for row in graph.source_index:
                amplitude = (vectors * vectors[row][None, :]) @ phases.T
                transfer += np.abs(amplitude.T) ** 2
            changed = transfer.mean(axis=0)
            keep = np.ones(graph.n, dtype=bool)
            keep[i] = False
            score[i] = np.abs(changed[keep] - baseline[keep]).sum()
        return score

    # `steps` and `window` set the time grid inside `build`, so both belong in the key.
    # Without them a second call at a different window returns the first call's result.
    return graph.memo(f"perturbation:{form}:{strength}:{steps}:{window}:{scale}", build)


def dephased_transport(
    graph: ResidueGraph, form: str = "adjacency", dephasing: float = 1.0, trapping: float = 1.0
) -> np.ndarray:
    """Negated mean trapping time under Lindblad dephasing plus a sink on the active site.

    Environment-assisted quantum transport. The published ENAQT optimum is a maximum in the
    transfer *efficiency* as a function of dephasing rate, and it exists only when the system
    has both dephasing and an irreversible trap: a coherent walk localises on disorder, weak
    dephasing breaks the localisation, strong dephasing freezes the walk by the quantum Zeno
    effect. A dephasing sweep with no sink cannot show that optimum, which is why this
    observable carries both terms.

    Solved in the adjoint picture. The mean survival time from every starting residue is the
    diagonal of the operator `A` satisfying `L^dagger(A) = -I`, so one linear solve of
    dimension N^2 returns all N scores rather than N separate simulations.

    The solve is matrix-free. Assembling the superoperator explicitly and factorising it took
    108 s at N = 147 and would be hopeless at N = 553, because the fill-in of an N^2 x N^2 LU
    is what dominates. Applying `L^dagger` to an N x N matrix instead costs two dense
    matrix products, so a Krylov method runs in O(N^3) per iteration and never forms the
    superoperator at all. Above `DEPHASING_MAX_NODES` the solve is refused rather than
    approximated.
    """
    if graph.n > DEPHASING_MAX_NODES:
        raise MemoryError(
            f"{graph.target}: dephased transport needs an N^2 = {graph.n**2} solve; the "
            f"declared ceiling is {DEPHASING_MAX_NODES} nodes"
        )

    def build():
        n = graph.n
        h = hamiltonian(graph, form).astype(complex)
        sink = np.zeros(n)
        sink[graph.source_index] = trapping
        anticommutator = 0.5 * (sink[:, None] + sink[None, :])
        # Pure dephasing in the site basis damps every off-diagonal entry at `dephasing` and
        # leaves the diagonal untouched.
        damping = dephasing * (1.0 - np.eye(n)) + anticommutator

        def apply(flat: np.ndarray) -> np.ndarray:
            a = flat.reshape(n, n)
            return (1j * (h @ a - a @ h) - damping * a).ravel()

        operator = spla.LinearOperator((n * n, n * n), matvec=apply, dtype=complex)
        # The right-hand side is -vec(I), not -vec(ones). The functional being integrated is
        # Tr(rho) = <I, rho>, so the adjoint equation is driven by the identity matrix.
        # Driving it with an all-ones matrix instead gives a wrong answer that looks
        # plausible -- it was within 15 % of the integrated truth on the first arm tested,
        # which is why this is written down rather than left to the reader.
        solution, info = spla.lgmres(
            operator,
            -np.eye(n, dtype=complex).ravel(),
            rtol=1e-8,
            atol=0.0,
            maxiter=2000,
        )
        if info != 0:
            raise RuntimeError(
                f"{graph.target}: dephased transport solve did not converge ({info})"
            )
        return -np.real(np.diag(solution.reshape(n, n)))

    return graph.memo(f"dephased:{form}:{dephasing}:{trapping}", build)


def szegedy_quantum_pagerank(
    graph: ResidueGraph, restart: float = 0.15, steps: int = 200
) -> np.ndarray:
    """Time-averaged instantaneous quantum PageRank, seeded on the active site.

    Paparo & Martin-Delgado, doi:10.1038/srep00444, quantise a classical Markov chain as a
    Szegedy walk on the edge space and read the node's instantaneous probability
    `I(i, t) = <Psi_t| (|i><i| (x) I) |Psi_t>`. Their claim is that the quantum version lifts
    secondary hubs that the classical chain flattens.

    The chain here is the *personalised* one — it restarts on the active site rather than
    uniformly — so the walk is conditioned on the propagation source exactly as the challenge
    requires. The published construction is uniform and does not condition, so this is an
    adaptation, and the classical score it must be compared against is
    `allo.classical.baselines.personalised_pagerank` on the same chain.

    The walk operator is applied as sparse matrix products rather than built densely: the
    edge space has N^2 dimensions, which is 1.1 million at the largest arm.
    """

    def build():
        n = graph.n
        transition = graph.weight / graph.degree[:, None]
        seed = np.zeros(n)
        seed[graph.source_index] = 1.0 / len(graph.source_index)
        chain = (1 - restart) * transition + restart * np.tile(seed, (n, 1))
        root = np.sqrt(chain)

        # |psi_i> = |i> (x) sum_j sqrt(P_ij) |j>, stored as rows of `root`.
        state = np.zeros((n, n), dtype=complex)
        state[graph.source_index, :] = root[graph.source_index, :]
        state /= np.linalg.norm(state)

        total = np.zeros(n)
        for _ in range(steps):
            # Reflection through span{|psi_i>}: 2 Pi - I, block diagonal in the first index.
            overlap = (root * state).sum(axis=1)
            state = 2.0 * overlap[:, None] * root - state
            # Swap the two registers.
            state = state.T.copy()
            total += (np.abs(state) ** 2).sum(axis=1)
        return total / steps

    return graph.memo(f"szegedy:{restart}:{steps}", build)


# The opening strengths swept by the two scorers below. Logarithmic over five decades,
# because the optimum moves by orders of magnitude between systems and a linear grid
# resolves only one decade of it. On mkp5 the grid brackets the optimum with room on both
# sides: every non-source residue turns at Gamma = 4.64, and the eleven that do not are the
# eleven source residues, whose survival time is monotone in Gamma by construction.
TRAPPING_RATES = tuple(float(rate) for rate in np.logspace(-2.0, 3.0, 12))


def _survival_sweep(graph: ResidueGraph, form: str, rates: tuple[float, ...]) -> np.ndarray:
    """Survival time of every residue at every opening strength. Shape `(len(rates), n)`."""

    def build():
        rows = []
        for rate in rates:
            try:
                rows.append(_survival(graph, form, float(rate)))
            except ArithmeticError:
                # A rate the solve cannot resolve is dropped, not clamped. At the weak-coupling
                # end the survival time genuinely diverges, so a failure there is the physics
                # showing through the arithmetic and not a bug to paper over.
                continue
        if len(rows) < 2:
            raise ArithmeticError(
                f"{graph.target}: fewer than two opening strengths survive conditioning; "
                "the sweep is refused rather than reported"
            )
        return np.stack(rows)

    return graph.memo(f"sweep:{form}:{rates}", build)


def quantum_best_case_transfer(
    graph: ResidueGraph, form: str = "adjacency", rates: Sequence[float] = TRAPPING_RATES
) -> np.ndarray:
    """Negated survival time at each residue's own best opening strength.

    `quantum_survival_time` fixes the sink strength at one value. That is the wrong thing to
    fix. Opening a quantum system to a drain has an optimum: too weak and the excitation
    never leaves, too strong and the Zeno effect decouples the drain from the rest of the
    graph. The optimum is a property of the complex spectrum of `H - i (Gamma/2) P_S`, and it
    is not recoverable from any single-Gamma transfer amplitude
    (doi:10.1021/jp302627w, doi:10.1088/1751-8121/ae5d23).

    This scans `rates` and keeps each residue's minimum. It costs `len(rates)` Sylvester
    solves, which is `len(rates)` times one O(N^3) decomposition and nothing else, because
    one solve returns every residue at once.

    Negated, so that a residue that can be drained fastest scores high.
    """
    return -_survival_sweep(graph, form, tuple(rates)).min(axis=0)


def quantum_opening_gain(
    graph: ResidueGraph, form: str = "adjacency", rates: Sequence[float] = TRAPPING_RATES
) -> np.ndarray:
    """How much each residue gains from tuning the opening, in decades of survival time.

    `log10(tau_i(Gamma_min) / min_Gamma tau_i)`: the depth of the residue's own transfer
    optimum, measured against the weak-coupling limit. This is the environment-assisted
    quantity itself rather than a transfer amplitude — a residue whose drainage improves by
    three decades when the sink is tuned is coupled to the active site through a channel
    that weak coupling cannot see, and one that gains nothing is not coupled at all.

    It replaces the obvious observable. `argmin_Gamma tau_i` was built first and measured
    first, and it is degenerate: on mkp5 it takes two distinct values over 147 residues,
    because the turning point is set by the graph's own spectral width and not by the
    residue. The depth of the optimum varies residue by residue; its location does not.
    The negative result is kept here rather than deleted.

    Free once the sweep runs.
    """
    table = _survival_sweep(graph, form, tuple(rates))
    return np.log10(table[0] / np.maximum(table.min(axis=0), _FLOOR))


SCORERS = {
    "ctqw_average_transfer": ctqw_average_transfer,
    "ctqw_infinite_time_average": ctqw_infinite_time_average,
    "ctqw_peak_transfer": ctqw_peak_transfer,
    "ctqw_temporal_variance": ctqw_temporal_variance,
    "ctqw_coherent_source_contrast": ctqw_coherent_source_contrast,
    "quantum_survival_time": quantum_survival_time,
    "quantum_perturbation_response": quantum_perturbation_response,
    "dephased_transport": dephased_transport,
    "szegedy_quantum_pagerank": szegedy_quantum_pagerank,
    "quantum_best_case_transfer": quantum_best_case_transfer,
    "quantum_opening_gain": quantum_opening_gain,
}
