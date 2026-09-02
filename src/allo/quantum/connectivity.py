"""The N x N connectivity matrix, and the source-free observables it makes available.

`CHALLENGE.md` §5 requires an **N x N matrix whose entry (i, j) is the quantum connectivity
strength between residue i and residue j**. Every observable in `allo.quantum.walk` returns
an N-vector of connectivity *to the source*, which is one column of that matrix summed over
the source residues. The matrix is therefore already implicit in the walk, and this module
makes it explicit so that the required artifact and the ranked hit list come from the same
object rather than from two constructions that happen to agree.

    C(i, j) = mean over t in [0, T] of |<i|exp(-iHt)|j>|^2

Symmetric, because H is real symmetric. Row-stochastic in the limit of a complete time
average, so a row is a distribution over partners and the usual functionals of a distribution
apply to it. The infinite-time limit sums over spectral **projectors**, not over eigenvectors,
which is what makes that true on a degenerate spectrum as well as a simple one.

**Why source-free observables belong here.** §4.1 asks for connectivity "in most cases" to an
active site. The hedge is the organisers' own, and it has to be: c-Myc, which §8 counts among
the minimum four targets, is a transcription factor with no catalytic site. A score read off
the matrix without choosing a source runs on such a target unchanged. The four below do that,
and none of them takes the source as an argument.
"""

from __future__ import annotations

import numpy as np

from allo.network import ResidueGraph
from allo.quantum.walk import _FLOOR, _eigen, _time_grid


def connectivity_matrix(
    graph: ResidueGraph,
    form: str = "adjacency",
    steps: int = 128,
    window: float = 50.0,
    mode: str = "finite",
) -> np.ndarray:
    """`C(i, j)`, the time-averaged transfer probability between every pair of residues.

    `mode="infinite"` returns the T -> infinity limit `sum_k |<i|k>|^2 |<k|j>|^2`, in which
    every phase has cancelled. It costs one matrix product instead of `steps` of them, and it
    contains no interference at all, which makes it the honest control for the finite window
    rather than a cheaper approximation to it.

    `steps` is lower here than in `walk`, at 128 against 512, because the cost is `steps` N x N
    products rather than `steps` matrix-vector products. On a 553-residue arm that is the
    difference between a minute and eight.
    """
    values, vectors = _eigen(graph, form)
    if mode == "infinite":
        # sum_k |<i|k>|^2 |<k|j>|^2 is the T -> infinity limit only when every eigenvalue is
        # simple. Time-averaging kills the cross term between two eigenvectors exactly when
        # their phases differ, so a degenerate pair leaves its cross term standing and the
        # limit is `sum_m |<i|P_m|j>|^2` over the spectral projector of each distinct
        # eigenvalue. What the naive form really costs is well-posedness: inside a
        # degenerate eigenspace the eigenvectors are an arbitrary LAPACK choice, so its
        # answer depends on that choice. Rotating the degenerate pair of the triangle K3
        # by 0.7 rad moves the naive matrix by up to 0.216 per entry and moves the
        # projector form by 0.0. K3's exact projector values are 5/9 on the diagonal and
        # 2/9 off it.
        # ponytail: a fixed relative tolerance, not a perturbative degeneracy analysis. It
        # is set two orders below the smallest gap any frozen arm actually shows, so it
        # separates the exactly-degenerate case from every near-degenerate one. Widen it
        # only with a measured gap distribution in hand.
        scale = max(1.0, float(np.abs(values).max()))
        blocks = np.split(
            np.arange(len(values)), np.flatnonzero(np.diff(values) > 1e-9 * scale) + 1
        )
        total = np.zeros((graph.n, graph.n))
        for block in blocks:
            projector = vectors[:, block] @ vectors[:, block].T
            total += projector**2
        return total
    if mode != "finite":
        raise ValueError(f"unknown mode {mode!r}; have 'finite' and 'infinite'")

    times = _time_grid(graph, form, steps, window)
    total = np.zeros((graph.n, graph.n))
    for t in times:
        propagator = (vectors * np.exp(-1j * values * t)[None, :]) @ vectors.T
        total += np.abs(propagator) ** 2
    return total / len(times)


def _rows(graph: ResidueGraph, form: str, steps: int, window: float) -> np.ndarray:
    """`C` with each row normalised to a distribution over partners, memoised on the graph."""

    def build() -> np.ndarray:
        matrix = connectivity_matrix(graph, form, steps, window)
        np.fill_diagonal(matrix, 0.0)
        return matrix / np.maximum(matrix.sum(axis=1, keepdims=True), _FLOOR)

    return graph.memo(f"connectivity_rows|{form}|{steps}|{window}", build)


def connectivity_entropy(
    graph: ResidueGraph, form: str = "adjacency", steps: int = 128, window: float = 50.0
) -> np.ndarray:
    """Shannon entropy of a residue's connectivity distribution, in nats.

    High entropy means the residue exchanges amplitude with many partners at comparable
    strength; low entropy means it is coupled to a few. This is a shape statistic of the row
    and not a magnitude, so scaling a whole row leaves it unchanged -- and the magnitude is
    where the dependence on distance to any particular site lives.

    Source-free, so it runs on a target with no catalytic site.
    """
    rows = _rows(graph, form, steps, window)
    return -(rows * np.log(np.maximum(rows, _FLOOR))).sum(axis=1)


def connectivity_participation(
    graph: ResidueGraph, form: str = "adjacency", steps: int = 128, window: float = 50.0
) -> np.ndarray:
    """The effective number of partners a residue is connected to, `1 / sum_j p_ij^2`.

    The participation ratio of the same distribution `connectivity_entropy` takes the entropy
    of. It answers the same question in units of a count rather than of information, and the
    two disagree when the distribution has a long tail, so both are carried.

    Source-free.
    """
    rows = _rows(graph, form, steps, window)
    return 1.0 / np.maximum((rows**2).sum(axis=1), _FLOOR)


def connectivity_strength(
    graph: ResidueGraph, form: str = "adjacency", steps: int = 128, window: float = 50.0
) -> np.ndarray:
    """Total connectivity of a residue to all others, the un-normalised row sum.

    The magnitude control for the two scorers above. It is expected to track degree, and it is
    here so that a gain from entropy or participation can be shown to be a gain from the
    *shape* of the distribution rather than from its size.

    Source-free.
    """
    matrix = connectivity_matrix(graph, form, steps, window)
    np.fill_diagonal(matrix, 0.0)
    return matrix.sum(axis=1)


def connectivity_eigencentrality(
    graph: ResidueGraph, form: str = "adjacency", steps: int = 128, window: float = 50.0
) -> np.ndarray:
    """Leading eigenvector of `C`: connectivity to residues that are themselves well connected.

    Eigenvector centrality computed on the quantum connectivity matrix rather than on the
    contact adjacency. The difference between this and `classical.eigenvector_centrality` is
    exactly what the walk adds to the topology it started from, so the pair is read together.

    Source-free.
    """
    matrix = connectivity_matrix(graph, form, steps, window)
    np.fill_diagonal(matrix, 0.0)
    vector = np.linalg.eigh(matrix)[1][:, -1]
    return np.abs(vector)


SCORERS = {
    "connectivity_entropy": connectivity_entropy,
    "connectivity_participation": connectivity_participation,
    "connectivity_strength": connectivity_strength,
    "connectivity_eigencentrality": connectivity_eigencentrality,
}
