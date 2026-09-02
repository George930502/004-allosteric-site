"""Source-conditioned coupling measures drawn from the exploration literature sweep.

`baselines.py` holds the standard battery -- the centralities, kernels and elastic-network
scores any reviewer would expect. This module holds the candidates that came out of the
Phase-2 exploration sweep in `docs/method/exploration/lit/`, each of which answers a question
the standard battery cannot:

* **Which residues lie on a high-probability communication path to the active site**
  (`ohm_path_probability`), rather than merely close to it.
* **Which residues carry current when the active site is driven** (`current_flow_to_source`),
  which counts every parallel route rather than only the shortest.
* **Which residues, if removed, would change the active site's own fluctuation**
  (`gnm_entropy_response`, `node_deletion_response`). These are the only scores in the repo
  that are *interventional*: they ask what a residue does, not where it sits.
* **How much of the graph has to be cut to separate a residue from the active site**
  (`min_vertex_cut_to_source`), which is not a function of the adjacency spectrum at all and
  so cannot collapse onto eigenvector centrality.
* **Directional coupling** (`gnm_transfer_entropy`), which a symmetric propagator cannot
  express and which a unitary walk on a real symmetric graph cannot express either.

Every one runs on the apo graph alone. Prediction-path code: no `allo.groundtruth`, no
`allo.scoring`.
"""

from __future__ import annotations

import numpy as np
from scipy.linalg import eigh, pinvh
from scipy.sparse.csgraph import dijkstra

from allo.network.graph import ResidueGraph

__all__ = ["SCORERS"]

_FLOOR = 1e-12
# Ohm's published contact-to-probability conversion, doi:10.1038/s41467-020-17618-2. The
# constant is theirs and is fitted to normalised heavy-atom contact counts, not to any MD
# quantity, so it carries no C2 problem: their own text is that Ohm "relies solely on the
# structure of the protein of interest".
#
# Two caveats, both material. Their `N_ij` is a contact count divided by the two residues'
# atom counts; the implementation below uses the graph edge weight divided by the graph's
# mean edge weight. Once the normalisation changes, 3.0 is no longer the paper's constant --
# it is a round number of the right order. And the method sweep pins it at one value rather
# than varying it, so this is a fixed choice and not a swept one. Both are stated here
# because a constant that looks cited and is not is worse than one that looks arbitrary.
OHM_SCALE = 3.0


def _source_reduce(matrix: np.ndarray, graph: ResidueGraph, reduce=np.max) -> np.ndarray:
    return reduce(matrix[:, graph.source_index], axis=1)


def ohm_path_probability(graph: ResidueGraph, scale: float = OHM_SCALE) -> np.ndarray:
    """Probability of the most likely communication path from the active site to each residue.

    Ohm converts a normalised residue contact count into a per-edge communication
    probability, `P_ij = 1 - exp(-scale * N_ij)`, then estimates each residue's coupling to a
    named site by Monte Carlo over paths. The maximum-probability path is the same object
    computed exactly: taking `-log P` as an edge length turns "most probable path" into
    "shortest path", so one multi-source Dijkstra replaces ten thousand random draws and
    removes the seed from the method entirely.

    `N_ij` here is the edge weight normalised by the graph's mean edge weight, so the
    construction works on every weighting the sweep builds rather than only on a contact
    count.
    """

    def build():
        weight = graph.weight
        positive = weight[weight > 0]
        normalised = np.where(weight > 0, weight / max(positive.mean(), _FLOOR), 0.0)
        probability = np.where(weight > 0, 1.0 - np.exp(-scale * normalised), 0.0)
        # A probability of exactly 1 gives a zero-length edge, which is correct but which
        # makes the log infinite in the other direction; clip just below.
        probability = np.clip(probability, _FLOOR, 1.0 - 1e-9)
        length = np.where(weight > 0, -np.log(probability), np.inf)
        cost = dijkstra(length, directed=False, indices=graph.source_index).min(axis=0)
        return np.exp(-cost)

    return graph.memo(f"ohm:{scale}", build)


def current_flow_to_source(graph: ResidueGraph) -> np.ndarray:
    """Electrical current through each residue when the active site is driven against ground.

    Inject unit current at the shorted active site, extract it uniformly over every other
    residue, and read the total absolute current on the edges touching residue i. Where
    shortest-path betweenness counts one route, this counts every parallel route weighted by
    its conductance, which is what a contact network with many redundant paths actually has.

    Potentials come from the Laplacian pseudoinverse, so this costs one decomposition that
    `effective_resistance_to_source` has already paid for.
    """

    def build():
        pinv = pinvh(graph.laplacian)
        injection = np.zeros(graph.n)
        injection[graph.source_index] = 1.0 / len(graph.source_index)
        injection -= 1.0 / graph.n
        potential = pinv @ injection
        difference = potential[:, None] - potential[None, :]
        return (np.abs(difference) * graph.weight).sum(axis=1) / 2.0

    return graph.memo("current_flow", build)


def node_deletion_response(graph: ResidueGraph) -> np.ndarray:
    """Change in the active site's own mean-square fluctuation when residue i is removed.

    An interventional score rather than a positional one. Delete node i from the Kirchhoff
    matrix, recompute the source residues' diagonal of the pseudoinverse, and report the
    total absolute change. A residue whose removal leaves the active site unchanged is not
    coupled to it, however central it is in the graph.

    N pseudoinverses of an (N-1) x (N-1) matrix. At N = 1058 that is minutes, which is the
    same order as `quantum_perturbation_response` and is the price of an interventional
    measure.
    """

    def build():
        source = set(graph.source_index.tolist())
        base = np.diag(pinvh(graph.laplacian))[graph.source_index]
        score = np.zeros(graph.n)
        for i in range(graph.n):
            if i in source:
                continue
            keep = np.ones(graph.n, dtype=bool)
            keep[i] = False
            reduced = graph.weight[np.ix_(keep, keep)]
            laplacian = np.diag(reduced.sum(axis=1)) - reduced
            index = np.array([j - (j > i) for j in graph.source_index])
            score[i] = np.abs(np.diag(pinvh(laplacian))[index] - base).sum()
        return score

    return graph.memo("node_deletion", build)


def gnm_entropy_response(graph: ResidueGraph) -> np.ndarray:
    """Change in the network's conformational entropy when residue i is constrained.

    The Gaussian network model's configurational entropy is `-0.5 * log det' Gamma` up to
    additive constants, where `det'` is the product of the non-zero Kirchhoff eigenvalues --
    which by the matrix-tree theorem is the graph's spanning-tree count. Constraining residue
    i changes it, and the change is a global, thermodynamic statement about that residue
    rather than a local one.

    Reported as the *source-weighted* form: the entropy change is multiplied by the residue's
    normalised GNM correlation with the active site, so a residue that stiffens a region the
    active site does not feel scores low. Without that weighting the score is source-blind
    and belongs in `baselines.py`.
    """

    def build():
        values, _ = eigh(graph.laplacian)
        non_zero = values[values > _FLOOR * max(values.max(), 1.0)]
        base = float(np.log(non_zero).sum())
        pinv = pinvh(graph.laplacian)
        scale = np.sqrt(np.maximum(np.diag(pinv), _FLOOR))
        correlation = _source_reduce(np.abs(pinv / np.outer(scale, scale)), graph)

        source = set(graph.source_index.tolist())
        entropy_change = np.zeros(graph.n)
        for i in range(graph.n):
            if i in source:
                continue
            keep = np.ones(graph.n, dtype=bool)
            keep[i] = False
            reduced = graph.weight[np.ix_(keep, keep)]
            laplacian = np.diag(reduced.sum(axis=1)) - reduced
            reduced_values, _ = eigh(laplacian)
            alive = reduced_values[reduced_values > _FLOOR * max(reduced_values.max(), 1.0)]
            entropy_change[i] = abs(base - float(np.log(alive).sum()))
        return entropy_change * correlation

    return graph.memo("gnm_entropy_response", build)


def min_vertex_cut_to_source(graph: ResidueGraph) -> np.ndarray:
    """Negated minimum cut separating each residue from the active site.

    By Menger's theorem the minimum cut equals the maximum number of edge-disjoint paths, so
    this counts *route redundancy* rather than route length. It is the one score in the repo
    that is not a function of the adjacency spectrum, which matters because every spectral
    readout on a protein graph collapses toward eigenvector centrality
    (`docs/method/review/09-data-analysis.md`).

    Negated so that a residue that is hard to separate from the active site -- many disjoint
    routes -- scores high. Capacities are the edge weights, and the max-flow is computed by
    the standard augmenting-path method on the dense matrix, which is affordable because the
    source side is contracted to one node.
    """

    def build():
        source = sorted(set(graph.source_index.tolist()))
        rest = [i for i in range(graph.n) if i not in set(source)]
        size = len(rest) + 1
        capacity = np.zeros((size, size))
        capacity[: len(rest), : len(rest)] = graph.weight[np.ix_(rest, rest)]
        merged = graph.weight[np.ix_(rest, source)].sum(axis=1)
        capacity[: len(rest), -1] = merged
        capacity[-1, : len(rest)] = merged

        score = np.zeros(graph.n)
        for position, node in enumerate(rest):
            score[node] = -_max_flow(capacity, size - 1, position)
        return score

    return graph.memo("min_cut", build)


def _max_flow(capacity: np.ndarray, start: int, sink: int) -> float:
    """Edmonds-Karp maximum flow on a dense symmetric capacity matrix."""
    residual = capacity.copy()
    total = 0.0
    while True:
        parent = np.full(len(residual), -1)
        parent[start] = start
        queue = [start]
        head = 0
        while head < len(queue) and parent[sink] < 0:
            node = queue[head]
            head += 1
            for other in np.flatnonzero(residual[node] > _FLOOR):
                if parent[other] < 0:
                    parent[other] = node
                    queue.append(int(other))
        if parent[sink] < 0:
            return total
        bottleneck = np.inf
        node = sink
        while node != start:
            bottleneck = min(bottleneck, residual[parent[node], node])
            node = parent[node]
        node = sink
        while node != start:
            residual[parent[node], node] -= bottleneck
            residual[node, parent[node]] += bottleneck
            node = parent[node]
        total += bottleneck


def gnm_transfer_entropy(graph: ResidueGraph, lag: float = 1.0) -> np.ndarray:
    """Directional information transfer from each residue to the active site.

    A symmetric propagator on a symmetric graph cannot say which of two coupled residues
    drives the other, and neither can a unitary walk. Linearised Langevin dynamics on the
    Kirchhoff matrix can: the time-lagged covariance `C(tau) = exp(-Gamma tau) Gamma^+` is not
    symmetric once the degrees differ, and the Gaussian transfer entropy built from it is
    directional.

    For jointly Gaussian variables the transfer entropy from i to p reduces to a ratio of
    conditional variances, which is a closed form in the covariance blocks and needs no
    trajectory. Reported as the maximum over active-site residues of the transfer from i
    into the source.
    """

    def build():
        values, vectors = eigh(graph.laplacian)
        alive = values > _FLOOR * max(values.max(), 1.0)
        static = (vectors[:, alive] / values[alive]) @ vectors[:, alive].T
        lagged = (vectors[:, alive] * np.exp(-values[alive] * lag) / values[alive]) @ vectors[
            :, alive
        ].T

        variance = np.maximum(np.diag(static), _FLOOR)
        score = np.zeros(graph.n)
        for p in graph.source_index:
            # Variance of p at time t+lag given its own past.
            own = variance[p] * (1.0 - lagged[p, p] ** 2 / (variance[p] * variance[p]))
            # ... and given its own past plus residue i's past.
            past = np.stack(
                [
                    np.full(graph.n, lagged[p, p]),
                    lagged[p, :],
                ],
                axis=1,
            )
            cross = np.stack(
                [
                    np.stack([np.full(graph.n, variance[p]), static[p, :]], axis=1),
                    np.stack([static[p, :], variance], axis=1),
                ],
                axis=1,
            )
            determinant = cross[:, 0, 0] * cross[:, 1, 1] - cross[:, 0, 1] * cross[:, 1, 0]
            safe = np.where(np.abs(determinant) > _FLOOR, determinant, np.inf)
            solved = np.stack(
                [
                    (cross[:, 1, 1] * past[:, 0] - cross[:, 0, 1] * past[:, 1]) / safe,
                    (-cross[:, 1, 0] * past[:, 0] + cross[:, 0, 0] * past[:, 1]) / safe,
                ],
                axis=1,
            )
            joint = variance[p] - (past * solved).sum(axis=1)
            ratio = np.maximum(own, _FLOOR) / np.maximum(joint, _FLOOR)
            score = np.maximum(score, 0.5 * np.log(np.maximum(ratio, 1.0)))
        return score

    return graph.memo(f"transfer_entropy:{lag}", build)


def _gaussian_transfer(
    predicted: np.ndarray,
    predicted_lag: np.ndarray,
    driver: np.ndarray,
    cross_static: np.ndarray,
    cross_lagged: np.ndarray,
) -> np.ndarray:
    """Gaussian transfer entropy into `predicted`, driven by `driver`, vectorised over pairs.

    Every argument is a vector over the pairs being evaluated. `predicted` is the equal-time
    variance of the predicted variable, `predicted_lag` its own lagged autocovariance,
    `driver` the equal-time variance of the driver, and the two `cross` vectors the
    equal-time and lagged covariance between them.

    Split out of `gnm_transfer_entropy` so that both directions of the same pair can be
    evaluated from one decomposition. The two directions differ only in which variable
    supplies the diagonal terms, which is where the asymmetry of the Kirchhoff dynamics
    lives.
    """
    own = predicted - predicted_lag**2 / np.maximum(predicted, _FLOOR)
    determinant = predicted * driver - cross_static**2
    safe = np.where(np.abs(determinant) > _FLOOR, determinant, np.inf)
    first = (driver * predicted_lag - cross_static * cross_lagged) / safe
    second = (-cross_static * predicted_lag + predicted * cross_lagged) / safe
    joint = predicted - (predicted_lag * first + cross_lagged * second)
    ratio = np.maximum(own, _FLOOR) / np.maximum(joint, _FLOOR)
    return 0.5 * np.log(np.maximum(ratio, 1.0))


def gnm_transfer_entropy_net(graph: ResidueGraph, lag: float = 1.0) -> np.ndarray:
    """Net directional transfer between each residue and the active site.

    `gnm_transfer_entropy` reports the transfer **into** the source and nothing else, so a
    residue that is merely well coupled scores highly whichever way the information runs. The
    net form subtracts the reverse direction:

        net(i) = mean over source p of [ T(i -> p) - T(p -> i) ]

    **The subtraction is why this is here.** Both directions are computed from the same
    covariance blocks, and every term that depends only on the pair -- the equal-time
    covariance `static[i, p]` and the lagged covariance `lagged[i, p]`, which are the two
    quantities that carry the inter-residue distance -- appears identically in both. What
    survives the difference is the asymmetry between the two residues' own diagonals, and a
    diagonal is a local property rather than a separation. So the construction cancels the
    distance dependence by algebra rather than by fitting a decay and subtracting it
    (Hacisuleyman and Erman, doi:10.1371/journal.pcbi.1005319).

    Positive means the residue drives the active site; negative means it listens to it. A
    driver is the allosteric direction, so the score is reported unsigned-positive as it
    stands.
    """

    def build():
        values, vectors = eigh(graph.laplacian)
        alive = values > _FLOOR * max(values.max(), 1.0)
        static = (vectors[:, alive] / values[alive]) @ vectors[:, alive].T
        lagged = (vectors[:, alive] * np.exp(-values[alive] * lag) / values[alive]) @ vectors[
            :, alive
        ].T
        variance = np.maximum(np.diag(static), _FLOOR)
        auto = np.diag(lagged)

        total = np.zeros(graph.n)
        for p in graph.source_index:
            forward = _gaussian_transfer(
                predicted=np.full(graph.n, variance[p]),
                predicted_lag=np.full(graph.n, auto[p]),
                driver=variance,
                cross_static=static[p, :],
                cross_lagged=lagged[p, :],
            )
            reverse = _gaussian_transfer(
                predicted=variance,
                predicted_lag=auto,
                driver=np.full(graph.n, variance[p]),
                cross_static=static[p, :],
                cross_lagged=lagged[p, :],
            )
            total += forward - reverse
        return total / max(len(graph.source_index), 1)

    return graph.memo(f"transfer_entropy_net:{lag}", build)


def multiscale_heat_kernel(graph: ResidueGraph, scales: int = 6) -> np.ndarray:
    """Geometric mean of the heat kernel from the active site over a spread of diffusion times.

    A single diffusion time is a hyperparameter and the sweep showed the choice matters. The
    heat-kernel-signature literature answers this by never picking one: sample `t` on a
    logarithmic grid spanning the operator's own spectral range and combine. The geometric
    mean is used rather than the arithmetic one because the kernel spans orders of magnitude
    across scales and an arithmetic mean would be the largest scale alone.
    """

    def build():
        values, vectors = eigh(graph.laplacian)
        positive = values[values > _FLOOR * max(values.max(), 1.0)]
        low, high = positive.min(), positive.max()
        times = np.logspace(np.log10(1.0 / high), np.log10(4.0 / low), scales)
        total = np.zeros(graph.n)
        for time in times:
            kernel = (vectors * np.exp(-time * values)) @ vectors.T
            total += np.log(np.maximum(_source_reduce(kernel, graph), _FLOOR))
        return total / scales

    return graph.memo(f"multiscale_heat:{scales}", build)


def normalised_anm_response(graph: ResidueGraph, cutoff: float = 13.0) -> np.ndarray:
    """Dynamic coupling index: ANM response at the active site, divided by the response anywhere.

    Perturbation-response scanning ranks a residue partly by how flexible it is, because a
    floppy residue moves a lot whatever you do to it. Dividing the mean response at the
    active site by the mean response over the whole chain cancels that term, which is the
    normalisation `entropy 22:6:667` (doi:10.3390/e22060667) introduces and calls the dynamic
    coupling index.

    That normalisation is the reason to compute this alongside
    `baselines.anm_perturbation_response` rather than instead of it: burial and flexibility
    are already controlled inside the frozen null, so a score that removes them at source
    should behave differently under that null, and the pair measures how much.
    """

    def build():
        coord = graph.coord
        separation = coord[:, None, :] - coord[None, :, :]
        distance = np.linalg.norm(separation, axis=-1)
        connected = (distance <= cutoff) & ~np.eye(graph.n, dtype=bool)
        hessian = np.zeros((3 * graph.n, 3 * graph.n))
        for i, j in zip(*np.nonzero(connected), strict=True):
            if i >= j:
                continue
            outer = np.outer(separation[i, j], separation[i, j]) / distance[i, j] ** 2
            hessian[3 * i : 3 * i + 3, 3 * j : 3 * j + 3] = -outer
            hessian[3 * j : 3 * j + 3, 3 * i : 3 * i + 3] = -outer
            hessian[3 * i : 3 * i + 3, 3 * i : 3 * i + 3] += outer
            hessian[3 * j : 3 * j + 3, 3 * j : 3 * j + 3] += outer
        values, vectors = eigh(hessian)
        keep = values > _FLOOR * max(values.max(), 1.0)
        inverse = (vectors[:, keep] / values[keep]) @ vectors[:, keep].T
        response = np.linalg.norm(inverse.reshape(graph.n, 3, graph.n, 3), axis=(1, 3))
        at_source = response[:, graph.source_index].mean(axis=1)
        everywhere = np.maximum(response.mean(axis=1), _FLOOR)
        return at_source / everywhere

    return graph.memo(f"dci:{cutoff}", build)


def bottleneck_to_source(graph: ResidueGraph) -> np.ndarray:
    """The weakest contact on the strongest path from each residue to the active site.

    Constraint network analysis ranks a residue by the rigidity of the weakest link on its
    best route to a named site, rather than by the length of that route
    (doi:10.1371/journal.pcbi.1004754). The quantity is the minimax path capacity, and it
    lies on the maximum spanning tree of the contact graph, so one Prim pass computes it for
    every residue at once.

    It is not distance (a sum along a path) and not effective resistance (a sum over parallel
    paths). It is a minimum along one path, which makes it the only score in the repo that
    saturates: adding a second route changes nothing unless that route is stronger. That is
    the property worth testing, because allosteric coupling is usually argued to travel a
    pathway rather than a field.
    """

    def build():
        # Prim from the contracted source, keeping the bottleneck rather than the total.
        capacity = np.full(graph.n, -np.inf)
        capacity[graph.source_index] = np.inf
        settled = np.zeros(graph.n, dtype=bool)
        for _ in range(graph.n):
            available = np.where(settled, -np.inf, capacity)
            node = int(np.argmax(available))
            if not np.isfinite(available[node]) and available[node] < 0:
                break
            settled[node] = True
            reachable = (graph.weight[node] > 0) & ~settled
            through = np.minimum(capacity[node], graph.weight[node])
            capacity = np.where(reachable & (through > capacity), through, capacity)
        finite = capacity[np.isfinite(capacity)]
        floor = finite.min() if len(finite) else 0.0
        return np.where(np.isfinite(capacity), capacity, floor)

    return graph.memo("bottleneck", build)


SCORERS = {
    "ohm_path_probability": ohm_path_probability,
    "current_flow_to_source": current_flow_to_source,
    "node_deletion_response": node_deletion_response,
    "gnm_entropy_response": gnm_entropy_response,
    "min_vertex_cut_to_source": min_vertex_cut_to_source,
    "gnm_transfer_entropy": gnm_transfer_entropy,
    "gnm_transfer_entropy_net": gnm_transfer_entropy_net,
    "multiscale_heat_kernel": multiscale_heat_kernel,
    "normalised_anm_response": normalised_anm_response,
    "bottleneck_to_source": bottleneck_to_source,
}
