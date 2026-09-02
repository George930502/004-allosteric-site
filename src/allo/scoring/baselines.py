"""The nine baselines the frozen evaluation protocol requires.

`docs/benchmark/evaluation/manifest.yaml` freezes `required_baselines`, and section 8 of the
layer README states that a method's result is not reportable until it is compared against
every one of them. This module is the only implementation of eight of the nine. The ninth,
`cavity_volume`, is a property of the detector and lives in `allo.scoring.decoys`.

**These are controls, not candidate methods.** A candidate method is something the project
proposes and wants scored. A required baseline is something the protocol mandates as the
reference a candidate has to beat. The distinction decides where the code lives: a control
belongs to the evaluation layer, which is frozen, and a candidate belongs to the method
layer, which is not.

**Added here on 2026-09-02**, when the method layer was removed from `main`. Eight of the
thirty scorers in `allo.classical.baselines` were the required baselines, and deleting that
module would have left the frozen protocol mandating numbers no code could produce. The
twelve functions below are those eight plus their transitive helpers, extracted unchanged.
The other twenty-two scorers were candidate methods and are preserved on the branch
`method-layer-archive`. See ADR 0037.

Every function takes a `ResidueGraph` and returns one array in the graph's own residue
order. `graph.as_scores(values)` turns that into the residue-keyed mapping `score_arm`
requires.
"""

from __future__ import annotations

import numpy as np
from scipy.linalg import eigh, pinvh
from scipy.sparse.csgraph import shortest_path

from allo.structure.graph import ResidueGraph

#: Eigenvalues below this fraction of the largest are treated as the null space. Rigid-body
#: modes sit there, and dividing by one of them turns a numerical zero into a large score.
_EIGEN_FLOOR = 1e-10


def spectrum(graph: ResidueGraph, operator: str) -> tuple[np.ndarray, np.ndarray]:
    """Ascending eigenvalues and eigenvectors of the adjacency or the Laplacian."""

    def build():
        matrix = graph.adjacency if operator == "adjacency" else graph.laplacian
        return eigh(matrix)

    return graph.memo(f"spectrum:{operator}", build)


def laplacian_pinv(graph: ResidueGraph) -> np.ndarray:
    """Moore-Penrose pseudoinverse of the graph Laplacian.

    Every resistance-like quantity in this module is one line off this matrix, so it is
    computed once. `pinvh` rather than `pinv` because the Laplacian is symmetric positive
    semidefinite and the symmetric routine keeps the result symmetric to machine precision,
    which matters when the next step subtracts two nearly equal entries.
    """
    return graph.memo("laplacian_pinv", lambda: pinvh(graph.laplacian))


def _hops(graph: ResidueGraph) -> np.ndarray:
    """All-pairs shortest-path hop counts on the unweighted contact graph."""
    return graph.memo("hops", lambda: shortest_path(graph.weight > 0, method="D", unweighted=True))


def degree(graph: ResidueGraph) -> np.ndarray:
    """Weighted degree. The burial proxy every connectivity score has to beat."""
    return graph.degree


def eigenvector_centrality(graph: ResidueGraph) -> np.ndarray:
    """Perron eigenvector of the adjacency matrix.

    Mandatory (ADR 0002). Mohtashim, Sajjan & Kais report that a continuous-time quantum
    walk on residue interaction networks agrees "consistently strongly" with this score
    over about 150 proteins (doi:10.1021/jacs.6c08053). A quantum metric that ties with
    this has reproduced that paper and has cleared nothing.
    """
    values, vectors = spectrum(graph, "adjacency")
    principal = vectors[:, -1]
    return np.abs(principal)


def closeness_centrality(graph: ResidueGraph) -> np.ndarray:
    """Reciprocal mean hop distance to every other residue."""
    hops = _hops(graph)
    finite = np.where(np.isfinite(hops), hops, 0.0)
    return (graph.n - 1) / np.maximum(finite.sum(axis=1), _EIGEN_FLOOR)


def betweenness_centrality(graph: ResidueGraph) -> np.ndarray:
    """Brandes betweenness on the unweighted contact graph.

    Implemented here rather than pulled from networkx: the package is not a dependency and
    the algorithm is twenty lines. Unweighted because the published protein applications of
    residue betweenness use hop counts.
    """

    def build():
        neighbours = [np.flatnonzero(row).tolist() for row in graph.weight > 0]
        score = np.zeros(graph.n)
        for start in range(graph.n):
            stack: list[int] = []
            predecessors: list[list[int]] = [[] for _ in range(graph.n)]
            paths = np.zeros(graph.n)
            paths[start] = 1.0
            distance = np.full(graph.n, -1)
            distance[start] = 0
            queue = [start]
            head = 0
            while head < len(queue):
                node = queue[head]
                head += 1
                stack.append(node)
                for other in neighbours[node]:
                    if distance[other] < 0:
                        distance[other] = distance[node] + 1
                        queue.append(other)
                    if distance[other] == distance[node] + 1:
                        paths[other] += paths[node]
                        predecessors[other].append(node)
            dependency = np.zeros(graph.n)
            while stack:
                node = stack.pop()
                for previous in predecessors[node]:
                    dependency[previous] += (paths[previous] / paths[node]) * (1 + dependency[node])
                if node != start:
                    score[node] += dependency[node]
        return score / 2.0

    return graph.memo("betweenness", build)


def gnm_fluctuation(graph: ResidueGraph) -> np.ndarray:
    """Gaussian network model mean-square fluctuation: the diagonal of the Kirchhoff pinv.

    Erman, doi:10.1529/biophysj.106.090803. Source-blind, and therefore a flexibility
    control rather than a communication score. Negated, because a rigid residue -- not a
    floppy one -- is the one an allosteric signal can travel through
    (`docs/evidence/method-landscape/06-signal-propagation-physics.md`).
    """
    return -np.diag(laplacian_pinv(graph))


def _source_column(matrix: np.ndarray, graph: ResidueGraph, reduce=np.max) -> np.ndarray:
    """Collapse the source columns of a pairwise matrix to one vector.

    `max` rather than `mean` by default: the source is a set of contacting residues, and a
    signal reaching any one of them has reached the active site. Averaging would penalise
    a residue coupled strongly to one source residue and weakly to the rest.
    """
    return reduce(matrix[:, graph.source_index], axis=1)


def distance_from_source_negated(graph: ResidueGraph) -> np.ndarray:
    """Negated Euclidean distance from the nearest source residue. The required control.

    `docs/ROADMAP.md` §1.4 makes this mandatory and says why it is not a walkover: it sits
    below chance on three of five primary arms, so its *inversion* is the strong control
    there. A propagation score that correlates with it above about 0.9 is a proximity
    ranker with extra steps.
    """
    distance = np.linalg.norm(
        graph.coord[:, None, :] - graph.coord[None, graph.source_index, :], axis=-1
    ).min(axis=1)
    return -distance


def anm_perturbation_response(graph: ResidueGraph, cutoff: float = 13.0) -> np.ndarray:
    """Perturbation-response scanning: displacement at the source per unit force at i.

    Build the 3N x 3N anisotropic network model Hessian from the same node set, invert it in
    the space orthogonal to the six rigid-body modes, then read the Frobenius norm of the
    3 x 3 block coupling residue i to each source residue. This is the elastic-network
    method that most directly computes "dynamic connectivity to the active site", and it is
    the published bar this project has to clear (Atilgan & Atilgan,
    doi:10.1371/journal.pcbi.1000544).

    The ANM cutoff is a separate hyperparameter from the contact graph's: the anisotropic
    model needs a longer range than a heavy-atom contact rule to be stable, and 13 A is the
    value the original ANM paper uses for Ca networks. It is tuned on `development` like
    every other knob.
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
        keep = values > _EIGEN_FLOOR * max(values.max(), 1.0)
        inverse = (vectors[:, keep] / values[keep]) @ vectors[:, keep].T
        blocks = inverse.reshape(graph.n, 3, graph.n, 3)
        response = np.linalg.norm(blocks, axis=(1, 3))
        return _source_column(response, graph, reduce=np.max)

    return graph.memo(f"anm_prs:{cutoff}", build)


def essa_perturbation(graph: ResidueGraph, modes: int = 10) -> np.ndarray:
    """Essential site scanning: the relative shift of the slow modes when residue i stiffens.

    ESSA (doi:10.1016/j.csbj.2020.06.020) adds mass or stiffness at one residue and measures
    how far the slow eigenvalues move. It is one of the four bars section 6 of
    `docs/evidence/method-landscape/00-conventions.md` makes mandatory.

    First-order perturbation theory replaces the N re-diagonalisations of the published
    implementation with one: for a symmetric operator, `dlambda_k = u_k^T dGamma u_k`, and
    stiffening residue i by its own contacts gives `dGamma(i)` with support only on row and
    column i. The whole score is then a contraction over the stored eigenvectors. The result
    is z-scored across residues, as the published score is.
    """

    def build():
        values, vectors = spectrum(graph, "laplacian")
        keep = slice(1, 1 + modes)
        amplitude = vectors[:, keep] ** 2
        # Stiffening residue i scales every edge at i, so dGamma acts as 2 * degree_i on the
        # squared amplitude at i, minus the cross terms with its neighbours.
        cross = graph.weight @ (vectors[:, keep] ** 2)
        shift = (graph.degree[:, None] * amplitude - cross) / np.maximum(
            values[keep][None, :], _EIGEN_FLOOR
        )
        score = shift.mean(axis=1)
        spread = score.std()
        return (score - score.mean()) / spread if spread > 0 else score

    return graph.memo(f"essa:{modes}", build)


def distance_from_source(graph: ResidueGraph) -> np.ndarray:
    """The un-negated form, which the manifest requires beside the negated one.

    Both directions are required baselines. On four of six primary arms the *inverted*
    distance ranker is the strong one, so reporting only one direction would understate the
    control (`experiments/REGISTRY.md`, 2026-09-02).
    """
    return -distance_from_source_negated(graph)


#: The manifest's nine `required_baselines`, keyed by the name the manifest uses.
#: `gnm_or_essa` offers two admissible constructions and `cavity_volume` is not here,
#: because it is a detector property computed by `allo.scoring.decoys.cavity_volume_score`.
REQUIRED_BASELINES = {
    "distance_from_source_negated": distance_from_source_negated,
    "distance_from_source": distance_from_source,
    "eigenvector_centrality": eigenvector_centrality,
    "degree": degree,
    "closeness": closeness_centrality,
    "betweenness": betweenness_centrality,
    "gnm_or_essa": gnm_fluctuation,
    "perturbation_response_scanning": anm_perturbation_response,
}

#: The second admissible reading of `gnm_or_essa`.
ESSA_ALTERNATIVE = {"gnm_or_essa": essa_perturbation}

__all__ = [
    "ESSA_ALTERNATIVE",
    "REQUIRED_BASELINES",
    "anm_perturbation_response",
    "betweenness_centrality",
    "closeness_centrality",
    "degree",
    "distance_from_source",
    "distance_from_source_negated",
    "eigenvector_centrality",
    "essa_perturbation",
    "gnm_fluctuation",
    "laplacian_pinv",
    "spectrum",
]
