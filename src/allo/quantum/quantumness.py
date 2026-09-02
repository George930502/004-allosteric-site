"""Observables built on the two mechanisms by which a quantum walk provably differs from diffusion.

Stage S5. This module exists because of one theorem and one measurement that agree.

**The theorem.** Faccin, Johnson, Biamonte, Kais and Migdal show that the long-time occupation
of a classical walk on a graph is exactly the degree distribution, `d_i / sum_j d_j`; that the
long-time average of a *quantum* walk equals it **exactly when the initial state has zero
energy**; and that the deviation between the two is bounded by `E / Delta`, the initial state's
energy over the spectral gap (Phys Rev X 3, 041007, 2013, arXiv:1305.6078).

**WITHDRAWN 2026-09-02: the paragraph that stood here read the theorem onto the wrong
operator, and its conclusion was the reverse of the truth.** It argued that a site-basis
source `|i>` has energy `<i|A|i> = 0` on the zero-diagonal adjacency, so "our source state sat
exactly on the theorem's classical point". Faccin's operator is not the adjacency. It is the
symmetric normalised Laplacian `H_Q = D^(-1/2) L D^(-1/2)`, whose diagonal is **1 at every
node**: measured on `kras_g12c_mandated`, `(H_Q)_ii` runs 1.000000 to 1.000000 over all 169
residues. The zero-energy state is the degree-weighted `|phi_0> = D^(1/2)|1>`, at
`<phi_0|H_Q|phi_0> = 0` to machine precision. A site-basis source sits at energy 1.0 and at
quantumness `eps = 1 - |<phi_0|i>|^2 = 0.994`. Far from the classical point, it is nearly as
far from it as a state can be.

`Delta` is wrong for the same reason. The paper's gap is the smallest **non-zero** eigenvalue
of `H_Q`, which is 0.056004 on that arm. `spectral_gap` below returns the gap next to the
dominant eigenvalue of the **adjacency**, which is 1.4383 -- a different number from a
different spectrum, a factor of 26 apart.

**What survives.** The bound is `E / Delta`, as stated. Nothing else in the paragraph does.
The two levers below are kept because the sweep measured them, not because this theorem
motivates them: read them as heuristics with a measurement behind them and no derivation.
`source_energy` and `spectral_gap` compute what their bodies say they compute, on the
adjacency, and they must not be quoted as the theorem's `E` and `Delta` until someone rebuilds
them on `H_Q`. Derivation and the reproduction script: review 25 of the 2026-09-02 audit,
section 2.5.

Two levers follow, and this module implements both.

1. **Energy.** Among states supported on the active site, take the one that maximises
   `<psi|H|psi>`. It is the top eigenvector of `H` restricted to the active-site block, and it is
   a *signed* combination -- the unsigned uniform state is the near-classical one. Same
   Hamiltonian, same graph, same averaging, same circuit: only the state preparation changes.
2. **Symmetry.** Local symmetry produces degenerate and null eigenspaces, and a walk can be
   trapped in them in a way no classical walk can be -- graph automorphisms give a quantum walk
   infinite hitting times, while a classical walk on a finite connected graph always has finite
   ones (Krovi and Brun, Phys Rev A 73, 032341, 2006). Overlap with those subspaces is a
   property of the graph's symmetry, which is not a function of distance to any source.

`docs/method/review/16-quantum-algorithm-survey.md` §Candidate constructions C1 and C2 are the
evidence base, and both name the classical control each observable has to be read against.
"""

from __future__ import annotations

import numpy as np

from allo.network import ResidueGraph
from allo.quantum.walk import _FLOOR, _eigen, _time_grid, hamiltonian


def _extreme_source_state(graph: ResidueGraph, form: str, high: bool) -> np.ndarray:
    """The state on the active site with the largest or smallest energy, as a full N-vector.

    A state supported only on the source has `<psi|H|psi> = c^T H_SS c`, so the extremal choices
    are the extremal eigenvectors of the source block. With a single source residue the block is
    1 x 1 and both reduce to that residue, which is the zero-energy case the theorem describes.
    """
    index = graph.source_index
    block = hamiltonian(graph, form)[np.ix_(index, index)]
    values, vectors = np.linalg.eigh(block)
    chosen = vectors[:, -1] if high else vectors[:, 0]
    state = np.zeros(graph.n)
    state[index] = chosen
    return state / max(float(np.linalg.norm(state)), _FLOOR)


def source_energy(graph: ResidueGraph, form: str = "adjacency", high: bool = True) -> float:
    """`<psi|H|psi>` for the extremal active-site state. The numerator of the theorem's bound."""
    state = _extreme_source_state(graph, form, high)
    return float(state @ hamiltonian(graph, form) @ state)


def spectral_gap(graph: ResidueGraph, form: str = "adjacency") -> float:
    """`Delta`, the gap next to the dominant eigenvalue. The denominator of the bound."""
    values, _ = _eigen(graph, form)
    return float(abs(values[-1] - values[-2]))


def quantumness_bound(graph: ResidueGraph, form: str = "adjacency") -> dict:
    """`E / Delta` for both extremal source states, plus the pieces it is built from.

    Diagnostic rather than a scorer. It is the quantity to report per target alongside any
    claim that a walk observable is not a classical one, because the theorem says a small value
    makes that claim untenable however the observable is defined.
    """
    gap = max(spectral_gap(graph, form), _FLOOR)
    high, low = source_energy(graph, form, True), source_energy(graph, form, False)
    return {
        "spectral_gap": round(gap, 6),
        "energy_high": round(high, 6),
        "energy_low": round(low, 6),
        "bound_high": round(abs(high) / gap, 4),
        "bound_low": round(abs(low) / gap, 4),
        "n_source": len(graph.source_index),
    }


def _transfer_from(graph: ResidueGraph, form: str, state: np.ndarray, steps: int, window: float):
    """Time-averaged occupation of every residue, starting from one prepared state."""
    values, vectors = _eigen(graph, form)
    times = _time_grid(graph, form, steps, window)
    amplitude = vectors.T @ state
    phases = np.exp(-1j * np.outer(times, values))
    evolved = (vectors * amplitude[None, :]) @ phases.T
    return (np.abs(evolved.T) ** 2).mean(axis=0)


def high_energy_transfer(
    graph: ResidueGraph, form: str = "adjacency", steps: int = 512, window: float = 50.0
) -> np.ndarray:
    """Time-averaged transfer from the highest-energy active-site state.

    The construction the survey ranks first, and the only one in the repository with a theorem
    stating the mechanism by which it must differ from diffusion. Read it against
    `walk.ctqw_average_transfer`, which is the same measurement from the zero-energy state: if
    the two rankings agree, the observable carries no quantum content, and that is then a
    measured fact rather than a suspicion.
    """
    return _transfer_from(graph, form, _extreme_source_state(graph, form, True), steps, window)


def low_energy_transfer(
    graph: ResidueGraph, form: str = "adjacency", steps: int = 512, window: float = 50.0
) -> np.ndarray:
    """Time-averaged transfer from the lowest-energy active-site state.

    The other extreme of the same lever. It is not a control for `high_energy_transfer` -- a
    large negative energy is just as far from the classical point as a large positive one -- but
    the pair brackets what the source-state choice can do, and their difference is the contrast
    below.
    """
    return _transfer_from(graph, form, _extreme_source_state(graph, form, False), steps, window)


def energy_contrast(
    graph: ResidueGraph, form: str = "adjacency", steps: int = 512, window: float = 50.0
) -> np.ndarray:
    """High-energy transfer minus low-energy transfer.

    Both states live on the same residues and both propagate through the same operator, so the
    radial envelope that makes every transfer probability a distance ranking is common to the
    two and cancels in the difference. What is left is the part of the propagation that depends
    on the *phase pattern* of the injected state, which has no classical counterpart at all: a
    classical walk has no phases to pattern.
    """
    high = _transfer_from(graph, form, _extreme_source_state(graph, form, True), steps, window)
    low = _transfer_from(graph, form, _extreme_source_state(graph, form, False), steps, window)
    return high - low


def symmetry_dark_overlap(
    graph: ResidueGraph, form: str = "adjacency", tolerance: float = 1e-8
) -> np.ndarray:
    """Weight of each residue in the null eigenspace of the operator.

    Local symmetry -- a repeated motif, a pair of interchangeable side chains, a duplicated loop
    -- produces exact zero eigenvalues of the adjacency, and the eigenvectors that span them are
    localised on the symmetric motif. A walk started elsewhere never reaches those components,
    which is the mechanism behind a quantum walk's infinite hitting times.

    Source-free, so it runs on a target with no catalytic site, and independent of distance to
    any source by construction: an automorphism is a property of the graph's labelling, not of
    its embedding in space.
    """
    values, vectors = _eigen(graph, form)
    scale = max(float(np.abs(values).max()), 1.0)
    dark = np.abs(values) <= tolerance * scale
    if not dark.any():
        return np.zeros(graph.n)
    return (vectors[:, dark] ** 2).sum(axis=1)


def degenerate_mixing_weight(
    graph: ResidueGraph, form: str = "adjacency", tolerance: float = 1e-6
) -> np.ndarray:
    """Source-conditioned overlap through degenerate eigenspaces only.

    The average mixing matrix of a continuous-time quantum walk is
    `M_ij = sum_r (E_r)_ij^2` over the spectral idempotents `E_r`. Restricting the sum to the
    `r` with `dim E_r > 1` keeps exactly the part that degeneracy -- and therefore symmetry --
    contributes, and discards the part any non-degenerate spectrum would also produce.

    Returns zero everywhere on a graph with a simple spectrum. That is the correct answer and
    not a failure: with no degeneracy there is no symmetry contribution to isolate.
    """
    values, vectors = _eigen(graph, form)
    scale = max(float(np.abs(values).max()), 1.0)
    score = np.zeros(graph.n)
    start = 0
    for stop in range(1, len(values) + 1):
        if stop == len(values) or values[stop] - values[start] > tolerance * scale:
            if stop - start > 1:
                block = vectors[:, start:stop]
                idempotent = block @ block.T
                score += (idempotent[:, graph.source_index] ** 2).sum(axis=1)
            start = stop
    return score


SCORERS = {
    "high_energy_transfer": high_energy_transfer,
    "low_energy_transfer": low_energy_transfer,
    "energy_contrast": energy_contrast,
    "symmetry_dark_overlap": symmetry_dark_overlap,
    "degenerate_mixing_weight": degenerate_mixing_weight,
}
