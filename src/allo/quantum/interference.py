"""Observables that isolate interference, and normalise it by its own interference-free part.

Stage S5, and the answer to two questions at once.

**The quantum question.** `CHALLENGE.md` §2 claims quantum offers "a unique advantage in
simulating non-local correlations and interference effects". Most observables in
`allo.quantum.walk` do not test that claim: a time-averaged transfer probability is a
spectral overlap plus an interference correction, and the overlap term is a classical
quantity that any diffusion kernel also produces. The two are separable exactly, so the
correction can be measured on its own rather than argued about.

Write the finite-window average as

    P_T(i) = mean over t in [0, T] of |<i|exp(-iHt)|s>|^2
           = sum_k |<i|k>|^2 |<k|s>|^2                              (the overlap term)
           + cross terms in exp(-i(E_k - E_l)t)                     (the interference term)

The first line is `walk.ctqw_infinite_time_average`, the T -> infinity limit in which every
phase has cancelled. Subtracting it from `P_T` leaves the interference and nothing else.

**The distance question.** The overlap term carries the magnitude, and the magnitude is what
correlates with distance to the source: a residue far from the source has small overlap with
every mode the source excites, whatever the mechanism. Dividing the interference term by the
overlap term therefore cancels the radial trend **by construction** rather than by fitting
and subtracting one afterwards. That is the difference between a ratio of two quantities
that share a confound and a regression residual, and it is why these are separate scorers
rather than a post-processing mode.

Every scorer here is a ratio or a difference of two quantities computed on the same operator,
the same time grid and the same source. Nothing is fitted and there is no free parameter
beyond the ones `walk` already exposes.
"""

from __future__ import annotations

import numpy as np

from allo.network import ResidueGraph
from allo.quantum.connectivity import connectivity_matrix
from allo.quantum.walk import _FLOOR, _amplitudes, _eigen, _time_grid


def _overlap(graph: ResidueGraph, form: str) -> np.ndarray:
    """The interference-free term: the T -> infinity transfer to the source, per residue.

    This used to write `sum_k |<i|k>|^2 |<k|s>|^2` out again. That form is the limit only on
    a simple spectrum, and on a degenerate one its value depends on which basis LAPACK
    happened to return for the degenerate eigenspace. It is now one column sum of the same
    matrix `connectivity` builds, so the two constructions cannot drift apart and the
    correction lands in both.
    """
    matrix = connectivity_matrix(graph, form, mode="infinite")
    return matrix[:, graph.source_index].sum(axis=1)


def interference_excess(
    graph: ResidueGraph, form: str = "adjacency", steps: int = 512, window: float = 50.0
) -> np.ndarray:
    """Finite-window transfer minus its own interference-free limit.

    The interference content of the walk, in absolute units. It keeps the magnitude, so it
    is the control against which the ratio forms below are read: if the ratio helps and this
    does not, the gain came from cancelling the magnitude and not from the interference.
    """
    times = _time_grid(graph, form, steps, window)
    return _amplitudes(graph, form, times).mean(axis=0) - _overlap(graph, form)


def interference_ratio(
    graph: ResidueGraph, form: str = "adjacency", steps: int = 512, window: float = 50.0
) -> np.ndarray:
    """Interference divided by the interference-free term.

    Scale-free by construction: multiply a residue's whole transfer profile by a constant and
    this does not move. Since the radial decay of transfer is close to such a constant per
    residue, the ratio is the natural distance-cancelled form of the same measurement.
    """
    times = _time_grid(graph, form, steps, window)
    overlap = _overlap(graph, form)
    finite = _amplitudes(graph, form, times).mean(axis=0)
    return finite / np.maximum(overlap, _FLOOR) - 1.0


def oscillation_ratio(
    graph: ResidueGraph, form: str = "adjacency", steps: int = 512, window: float = 50.0
) -> np.ndarray:
    """Root-mean-square temporal oscillation, in units of the interference-free transfer.

    A classical walk on the same operator relaxes monotonically, so its normalised
    oscillation decays to zero. A coherent walk keeps oscillating, with an amplitude set by
    how many eigenmodes overlap both the source and the residue. `walk.ctqw_temporal_variance`
    normalises by the observed mean, which still carries the magnitude; this normalises by the
    interference-free term, which is the quantity the magnitude actually lives in.
    """
    times = _time_grid(graph, form, steps, window)
    trace = _amplitudes(graph, form, times)
    overlap = np.maximum(_overlap(graph, form), _FLOOR)
    return np.sqrt(trace.var(axis=0)) / overlap


def coherent_source_ratio(
    graph: ResidueGraph, form: str = "adjacency", steps: int = 512, window: float = 50.0
) -> np.ndarray:
    """Coherent-source transfer divided by incoherent-source transfer, minus one.

    The ratio form of `walk.ctqw_coherent_source_contrast`. Injecting the excitation as an
    equal-amplitude superposition over the active-site residues, rather than one residue at a
    time, leaves exactly the cross-terms between source residues. Those cross-terms are
    interference between propagation routes leaving the active site, which is the most direct
    reading of the challenge's "non-local correlations" claim available on this graph.

    A single-residue source has no such cross-term and this returns zero everywhere. That is
    correct rather than a failure: with one injection point there is nothing to interfere.
    """
    if len(graph.source_index) < 2:
        return np.zeros(graph.n)
    values, vectors = _eigen(graph, form)
    times = _time_grid(graph, form, steps, window)
    phases = np.exp(-1j * np.outer(times, values))
    weights = vectors[graph.source_index, :].sum(axis=0) / np.sqrt(len(graph.source_index))
    coherent = (np.abs(((vectors * weights[None, :]) @ phases.T).T) ** 2).mean(axis=0)
    incoherent = (_amplitudes(graph, form, times) / len(graph.source_index)).mean(axis=0)
    return coherent / np.maximum(incoherent, _FLOOR) - 1.0


def spectral_participation_ratio(graph: ResidueGraph, form: str = "adjacency") -> np.ndarray:
    """How many eigenmodes carry a residue's coupling to the source.

    `1 / sum_k p_k^2` where `p_k` is the normalised contribution of mode k to that residue's
    overlap with the source. A residue coupled through one mode has a participation of 1; one
    coupled through many has a participation approaching N.

    This is the count of interfering routes rather than their sum, so it does not scale with
    the coupling strength, and the coupling strength is where the distance dependence lives.
    It needs no time grid and no window, which makes it the cheapest observable in the module
    and the only one with no coherence-time dependence at all.
    """
    _, vectors = _eigen(graph, form)
    weight = (vectors[graph.source_index, :] ** 2).sum(axis=0)
    contribution = (vectors**2) * weight[None, :]
    total = np.maximum(contribution.sum(axis=1, keepdims=True), _FLOOR)
    p = contribution / total
    return 1.0 / np.maximum((p**2).sum(axis=1), _FLOOR)


SCORERS = {
    "interference_excess": interference_excess,
    "interference_ratio": interference_ratio,
    "oscillation_ratio": oscillation_ratio,
    "coherent_source_ratio": coherent_source_ratio,
    "spectral_participation_ratio": spectral_participation_ratio,
}
