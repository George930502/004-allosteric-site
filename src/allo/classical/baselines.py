"""Classical residue scores: the analogs the challenge asks us to compare against.

Every function here takes a :class:`~allo.network.graph.ResidueGraph` and returns one float
per node, in `graph.order`, higher meaning *more likely allosteric*. Sign conventions are
applied inside each function, so a caller never has to remember which way a distance runs.

The battery splits in two, and the split is the discriminator that matters.

* **Source-blind** scores rank a residue by an intrinsic property of its position in the
  graph. They cannot express "connected to the active site", which is what
  `CHALLENGE.md` §4.1 asks for. They are here as controls: a propagation score that does
  not beat them has measured burial, not communication.
* **Source-conditioned** scores rank a residue by a relation to the frozen propagation
  source. Only four published classical allosteric methods do this
  (`docs/method/review/01-classical-baselines.md`), which is why most of this list had to
  be written rather than cited.

Three of these are mandatory by earlier decision. `distance_from_source_negated` and
`eigenvector_centrality` are required by ADR 0002 and `docs/ROADMAP.md` §1.4;
`cavity_volume` is required by ADR 0025 and lives with the detector in
`allo.scoring.decoys`, because that is where the pinned detector version is asserted.

Prediction-path code: no import of `allo.groundtruth` or `allo.scoring` appears here.
"""

from __future__ import annotations

import numpy as np
from scipy.linalg import eigh, pinvh
from scipy.sparse.csgraph import shortest_path

from allo.network.graph import ResidueGraph

__all__ = ["SOURCE_BLIND", "SOURCE_CONDITIONED", "SCORERS", "spectrum", "laplacian_pinv"]

_EIGEN_FLOOR = 1e-10


# --------------------------------------------------------------------------------------
# Shared decompositions. Memoised on the graph so a sweep pays for each one once.
# --------------------------------------------------------------------------------------


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


def _transition(graph: ResidueGraph) -> np.ndarray:
    """Row-stochastic random-walk transition matrix P = D^-1 W."""
    return graph.memo("transition", lambda: graph.weight / graph.degree[:, None])


# --------------------------------------------------------------------------------------
# Source-blind controls
# --------------------------------------------------------------------------------------


def degree(graph: ResidueGraph) -> np.ndarray:
    """Weighted degree. The burial proxy every connectivity score has to beat."""
    return graph.degree


def contact_number(graph: ResidueGraph) -> np.ndarray:
    """Unweighted contact count. Weighting-independent burial."""
    return (graph.weight > 0).sum(axis=1).astype(float)


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


def katz_centrality(graph: ResidueGraph, attenuation: float = 0.5) -> np.ndarray:
    """Sum of attenuated walks of every length: (I - a/lambda1 A)^-1 1.

    The attenuation is expressed as a fraction of the inverse spectral radius so that the
    series converges on every graph without a per-target constant.
    """
    values, _ = spectrum(graph, "adjacency")
    alpha = attenuation / max(values[-1], _EIGEN_FLOOR)
    return np.linalg.solve(np.eye(graph.n) - alpha * graph.adjacency, np.ones(graph.n))


def subgraph_centrality(graph: ResidueGraph) -> np.ndarray:
    """Diagonal of exp(A): the weighted count of closed walks through each node.

    Estrada & Rodriguez-Velazquez, doi:10.1103/PhysRevE.71.056103. The scaled adjacency
    keeps the exponential finite on a 1000-node graph; scaling is monotone in the spectrum
    and so does not change the ranking's construction, only its numerical range.
    """
    values, vectors = spectrum(graph, "adjacency")
    scaled = values / max(np.abs(values).max(), _EIGEN_FLOOR)
    return (vectors**2 @ np.exp(scaled)).ravel()


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


def clustering_coefficient(graph: ResidueGraph) -> np.ndarray:
    """Local clustering. High clustering marks a packed core, low marks a hinge."""
    binary = (graph.weight > 0).astype(float)
    triangles = np.einsum("ij,jk,ki->i", binary, binary, binary)
    k = binary.sum(axis=1)
    pairs = k * (k - 1)
    return np.where(pairs > 0, triangles / np.maximum(pairs, _EIGEN_FLOOR), 0.0)


def core_number(graph: ResidueGraph) -> np.ndarray:
    """k-core index by repeated peeling of the lowest-degree node."""
    binary = (graph.weight > 0).astype(int)
    remaining = np.ones(graph.n, dtype=bool)
    live_degree = binary.sum(axis=1).astype(float)
    core = np.zeros(graph.n)
    level = 0
    while remaining.any():
        candidates = np.where(remaining, live_degree, np.inf)
        node = int(np.argmin(candidates))
        level = max(level, int(candidates[node]))
        core[node] = level
        remaining[node] = False
        live_degree -= binary[node]
        live_degree[node] = 0
    return core


def gnm_fluctuation(graph: ResidueGraph) -> np.ndarray:
    """Gaussian network model mean-square fluctuation: the diagonal of the Kirchhoff pinv.

    Erman, doi:10.1529/biophysj.106.090803. Source-blind, and therefore a flexibility
    control rather than a communication score. Negated, because a rigid residue -- not a
    floppy one -- is the one an allosteric signal can travel through
    (`docs/method/review/06-signal-propagation-physics.md`).
    """
    return -np.diag(laplacian_pinv(graph))


def fiedler_amplitude(graph: ResidueGraph) -> np.ndarray:
    """Absolute amplitude in the second-lowest Laplacian eigenvector.

    The slowest non-trivial collective mode. The elastic-network literature's standard
    claim is that low-frequency modes carry function; this is the smallest test of it.
    """
    values, vectors = spectrum(graph, "laplacian")
    return np.abs(vectors[:, 1])


def slow_mode_participation(graph: ResidueGraph, modes: int = 10) -> np.ndarray:
    """Fluctuation carried by the ten slowest non-trivial Laplacian modes.

    The GNM fluctuation restricted to the low-frequency subspace, which is where the
    elastic-network literature places functional motion.
    """
    values, vectors = spectrum(graph, "laplacian")
    keep = slice(1, 1 + modes)
    inverse = 1.0 / np.maximum(values[keep], _EIGEN_FLOOR)
    return (vectors[:, keep] ** 2) @ inverse


# --------------------------------------------------------------------------------------
# Source-conditioned scores
# --------------------------------------------------------------------------------------


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


def hop_distance_from_source_negated(graph: ResidueGraph) -> np.ndarray:
    """Negated graph-hop distance to the nearest source residue.

    The topological twin of the control above. Where the two disagree, the graph has
    encoded something the coordinates alone do not.
    """
    hops = _hops(graph)
    return -_source_column(hops, graph, reduce=np.min)


def sequence_distance_from_source_negated(graph: ResidueGraph) -> np.ndarray:
    """Negated residue-number distance to the nearest source residue.

    The weakest possible baseline: it uses no structure at all. It is here because it is
    not weak in practice on some arms, and a method must be reported against it.
    """
    numbers = np.array(graph.order, dtype=float)
    source = numbers[graph.source_index]
    return -np.abs(numbers[:, None] - source[None, :]).min(axis=1)


def effective_resistance_to_source(graph: ResidueGraph) -> np.ndarray:
    """Negated effective resistance to the source, with the source shorted to one node.

    Omega(i, S) = L+_ii + L+_SS - 2 L+_iS, computed on the Laplacian of the graph in which
    every source residue is merged into a single node. Merging rather than averaging is the
    physically correct treatment: the active site is one terminal of the circuit, so its
    residues are at one potential.

    `docs/method/review/11-pipeline-decomposition.md` calls this the review's strongest new
    candidate and also its cheapest decisive test, because Kron reduction preserves it
    exactly under coarse-graining (Dorfler & Bullo, arXiv:1102.2950). Negated so that a low
    resistance -- strong coupling -- scores high.
    """

    def build():
        source = set(graph.source_index.tolist())
        rest = [i for i in range(graph.n) if i not in source]
        merged = np.zeros((len(rest) + 1, len(rest) + 1))
        merged[: len(rest), : len(rest)] = graph.weight[np.ix_(rest, rest)]
        merged[: len(rest), -1] = graph.weight[np.ix_(rest, sorted(source))].sum(axis=1)
        merged[-1, : len(rest)] = merged[: len(rest), -1]
        laplacian = np.diag(merged.sum(axis=1)) - merged
        pinv = pinvh(laplacian)
        resistance = np.full(graph.n, 0.0)
        for position, node in enumerate(rest):
            resistance[node] = pinv[position, position] + pinv[-1, -1] - 2 * pinv[position, -1]
        return -resistance

    return graph.memo("effective_resistance", build)


def hitting_time_to_source_negated(graph: ResidueGraph) -> np.ndarray:
    """Negated expected number of random-walk steps from a residue to the source set.

    Solves (I - P_cc) h = 1 over the non-source nodes, which is the absorbing-walk
    formulation. Unlike commute time this is not symmetric and not a monotone transform of
    effective resistance, so it is a separate observable rather than a rescaling.
    """

    def build():
        transition = _transition(graph)
        source = set(graph.source_index.tolist())
        rest = [i for i in range(graph.n) if i not in source]
        block = transition[np.ix_(rest, rest)]
        hitting = np.linalg.solve(np.eye(len(rest)) - block, np.ones(len(rest)))
        out = np.zeros(graph.n)
        out[rest] = hitting
        return -out

    return graph.memo("hitting_time", build)


def personalised_pagerank(graph: ResidueGraph, restart: float = 0.15) -> np.ndarray:
    """Stationary distribution of a random walk that restarts on the source set.

    pi = restart * (I - (1 - restart) P^T)^-1 v, with v uniform over the source. This is
    random-walk-with-restart under its other name, and it is the classical diffusive model
    the challenge asks the quantum walk to beat.
    """
    transition = _transition(graph)
    seed = np.zeros(graph.n)
    seed[graph.source_index] = 1.0 / len(graph.source_index)
    return restart * np.linalg.solve(np.eye(graph.n) - (1 - restart) * transition.T, seed)


def heat_kernel_from_source(graph: ResidueGraph, time: float = 1.0) -> np.ndarray:
    """[exp(-t L)]_{i,S}: classical diffusion from the source at diffusion time t.

    The direct classical analog of the quantum propagator. Where a continuous-time quantum
    walk uses exp(-i H t) on the same operator, this uses exp(-t L); comparing the two on
    one graph is the cleanest statement of "does interference help here".
    """
    values, vectors = spectrum(graph, "laplacian")
    kernel = (vectors * np.exp(-time * values)) @ vectors.T
    return _source_column(kernel, graph, reduce=np.max)


def regularised_laplacian_kernel(graph: ResidueGraph, sigma: float = 1.0) -> np.ndarray:
    """[(I + sigma^2 L)^-1]_{i,S}: the diffusion kernel's resolvent form.

    Different weighting of the same eigenbasis as the heat kernel: 1/(1 + sigma^2 lambda)
    instead of exp(-t lambda). It decays polynomially rather than exponentially in the
    eigenvalue, so it keeps more weight on fast modes.
    """
    kernel = np.linalg.inv(np.eye(graph.n) + sigma**2 * graph.laplacian)
    return _source_column(kernel, graph, reduce=np.max)


def communicability_from_source(graph: ResidueGraph) -> np.ndarray:
    """[exp(A)]_{i,S}: Estrada communicability, the walk-weighted coupling to the source.

    Estrada & Hatano, doi:10.1103/PhysRevE.77.036111. Structurally the closest classical
    object to a quantum transfer amplitude -- a sum over all walks with factorial damping --
    and therefore the classical score a quantum walk most needs to be shown to beat.
    """
    values, vectors = spectrum(graph, "adjacency")
    scaled = values / max(np.abs(values).max(), _EIGEN_FLOOR)
    kernel = (vectors * np.exp(scaled)) @ vectors.T
    return _source_column(kernel, graph, reduce=np.max)


def gnm_cross_correlation(graph: ResidueGraph) -> np.ndarray:
    """Normalised GNM cross-correlation of each residue with the source.

    C_ij / sqrt(C_ii C_jj) from the Kirchhoff pseudoinverse, the standard elastic-network
    measure of dynamic coupling (Chennubhotla & Bahar, doi:10.1371/journal.pcbi.0030172).
    The absolute value is taken: anticorrelated motion is coupling, not decoupling.
    """
    pinv = laplacian_pinv(graph)
    scale = np.sqrt(np.maximum(np.diag(pinv), _EIGEN_FLOOR))
    normalised = np.abs(pinv / np.outer(scale, scale))
    return _source_column(normalised, graph, reduce=np.max)


def source_conditioned_betweenness(graph: ResidueGraph) -> np.ndarray:
    """Fraction of shortest paths *from the source* that pass through each residue.

    Plain betweenness asks which residue lies on many paths. This asks which residue lies
    on many paths *out of the active site*, which is the question the challenge poses. It
    needs the same Brandes machinery restricted to the source rows.
    """

    def build():
        neighbours = [np.flatnonzero(row).tolist() for row in graph.weight > 0]
        score = np.zeros(graph.n)
        for start in graph.source_index.tolist():
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
        return score

    return graph.memo("source_betweenness", build)


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


def protrusion_index(graph: ResidueGraph) -> np.ndarray:
    """How far each residue sits outside the protein's own inertial ellipsoid.

    ElliPro's construction (doi:10.1186/1471-2105-9-514): diagonalise the coordinate
    covariance, express each residue in the principal frame, and take the ellipsoid radius
    that just contains it. A residue on a bulge scores high, one in the core scores low.

    Zero parameters, and decorrelated from cavity volume by construction: a cavity is a
    concavity and a protrusion is a convexity. It belongs here as a *geometric* control
    alongside `cavity_volume`, not as a propagation score.
    """
    centred = graph.coord - graph.coord.mean(axis=0)
    covariance = centred.T @ centred / len(centred)
    weights, axes = eigh(covariance)
    projected = centred @ axes
    return np.sqrt((projected**2 / np.maximum(weights, _EIGEN_FLOOR)).sum(axis=1))


def essa_perturbation(graph: ResidueGraph, modes: int = 10) -> np.ndarray:
    """Essential site scanning: the relative shift of the slow modes when residue i stiffens.

    ESSA (doi:10.1016/j.csbj.2020.06.020) adds mass or stiffness at one residue and measures
    how far the slow eigenvalues move. It is one of the four bars
    `docs/method/review/00-conventions.md` §6 makes mandatory, and it had not been built.

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


def alps_spectral_response(
    graph: ResidueGraph, radius: float = 10.0, stiffening: float = 1.0, modes: int = 3
) -> np.ndarray:
    """The teammate benchmark's own best method, reimplemented exactly.

    `allosteric-benchmark/methods/alps.py`: stiffen every edge inside residue i's `radius`
    neighbourhood by `1 + stiffening`, and score i by the relative shift of the lowest
    `modes` non-zero Kirchhoff eigenvalues,
    `sum_k |lambda_k(H_i) - lambda_k(H_0)| / lambda_k(H_0)`.

    It is here for three reasons. It is the only method in that repository that survives
    Bonferroni correction on its own curated set. It is a *local stiffening* response rather
    than a single-residue perturbation, which is a different object from
    `essa_perturbation`. And re-implementing it means the comparison runs on our frozen
    graph, our frozen labels and our frozen null, so the number is comparable to everything
    else here rather than to a number computed under a different protocol.

    **Its published constants are label-tuned on a set that contains our own arms, so this
    is a comparator and not a candidate.** `allosteric-benchmark/methods/alps.py` states in
    its own comment that `radius = 12.0`, `stiffening = 2.0` and `modes = 3` were "re-tuned
    on curated labels with the distance-stratified metric". That curated set includes `3K5V`
    and `3PYY` (the ABL1 myristoyl pocket, which is what `bcr_abl1_mandated` asks a method to
    predict), `1T49` (PTP1B with an allosteric inhibitor from the same series as the
    `ptp1b` development arm's holo entry), and `2JHR` and `3BZ7` (the myosin blebbistatin
    site). Those three numbers are therefore functions of holo-derived labels for pockets
    this benchmark scores against, and ADR 0026 clause 2 forbids them as defaults by name.

    Two consequences, both binding.

    1. **The defaults here are deliberately not theirs.** `radius = 10.0` and
       `stiffening = 1.0` are round numbers with no tuning behind them. The published triple
       is one point in a sweep, never a default (ADR 0026 clause 2).
    2. **This score is never eligible to be selected as our method.** It is reported as a
       bar, and it is an *optimistic* bar: it was tuned with an advantage no candidate here
       has. Beating it means something. Losing to it does not.

    Their published score applies a distance-conditional Gaussian-kernel z-score afterwards.
    That is a stage-S6 detrend, not part of the score, so it lives in
    `postprocess.fit_decay(form="gaussian_kernel")` and the sweep varies it like any other
    detrend. Their own measurement is that removing the active site from the score entirely
    costs nothing (0.591 against 0.591), so this stage is source-blind by construction and
    is filed accordingly.

    N re-diagonalisations of a sparse-ish matrix, done densely. It is the second most
    expensive score in the module after `essa_perturbation`'s exact counterpart.
    """

    def build():
        separation = np.linalg.norm(graph.coord[:, None, :] - graph.coord[None, :, :], axis=-1)
        base_values = np.sort(eigh(graph.laplacian, eigvals_only=True))
        base = base_values[base_values > _EIGEN_FLOOR * max(base_values.max(), 1.0)][:modes]
        score = np.zeros(graph.n)
        for i in range(graph.n):
            near = separation[i] <= radius
            scale = np.ones((graph.n, graph.n))
            scale[np.ix_(near, near)] = 1.0 + stiffening
            weight = graph.weight * scale
            laplacian = np.diag(weight.sum(axis=1)) - weight
            values = np.sort(eigh(laplacian, eigvals_only=True))
            shifted = values[values > _EIGEN_FLOOR * max(values.max(), 1.0)][:modes]
            score[i] = float((np.abs(shifted - base) / base).sum())
        return score

    return graph.memo(f"alps:{radius}:{stiffening}:{modes}", build)


def distance_to_centroid_negated(graph: ResidueGraph) -> np.ndarray:
    """Negated distance from each residue to the centroid of the modelled chain.

    One line of geometry, and a control rather than a method. STINGAllo's SHAP attribution
    over 54 descriptors names it the single most influential feature, mean |SHAP| > 0.4
    (doi:10.1016/j.csbj.2024.10.036). It is added here because a screen has to know whether
    its winner beats "how close is this residue to the middle of the protein", and because
    the frozen matched-patch null already controls burial -- which is what this measures.

    Negated so that a central residue scores high, matching the sign of every other score.
    """
    return -np.linalg.norm(graph.coord - graph.coord.mean(axis=0), axis=1)


def local_contact_order(graph: ResidueGraph) -> np.ndarray:
    """Mean sequence separation of a residue's own contacts.

    The per-residue form of Plaxco's contact order (doi:10.1006/jmbi.1998.1645). A residue
    whose contacts are all sequence-local sits in a helix or a turn; one whose contacts span
    the chain closes a long-range loop and is a candidate hinge.

    It is the only cheap descriptor in this module that is orthogonal to burial by
    construction: it divides by the contact count, so packing density cancels. That makes it
    the one geometric column the matched-patch null cannot absorb in advance.
    """
    numbers = np.array(graph.order, dtype=float)
    separation = np.abs(numbers[:, None] - numbers[None, :])
    contacts = graph.adjacency
    count = np.maximum(contacts.sum(axis=1), 1.0)
    return (contacts * separation).sum(axis=1) / count


def mean_bfactor(graph: ResidueGraph) -> np.ndarray:
    """The chain z-scored deposited B-factor. The fluctuation route's own oracle.

    Every method that predicts per-residue flexibility from topology is trying to reproduce
    this number, and the best of them reach only r ~ 0.59-0.64 against it (Halle,
    doi:10.1073/pnas.032522499). So this is the ceiling of the whole route: if the measured
    fluctuation does not separate the label set, no predicted fluctuation will, and the
    route closes for one line of code rather than for a modelling programme.

    Read it against `gnm_fluctuation` in the same run. `gnm_fluctuation` is the topological
    prediction of this quantity, so the pair separates "flexibility does not work here" from
    "our elastic model does not capture flexibility here".

    C1 and C2 both pass -- it is deposited apo metadata, not a simulation. It is a
    measurement of one crystal, with an error of about 9 A^2 at ambient temperature and 6
    A^2 under cryo conditions (Carugo, doi:10.1186/s12859-018-2083-8), and a correlation
    with it must never be reported as a correlation with dynamics.
    """
    return graph.bfactor


SOURCE_BLIND = {
    "degree": degree,
    "contact_number": contact_number,
    "eigenvector_centrality": eigenvector_centrality,
    "katz_centrality": katz_centrality,
    "subgraph_centrality": subgraph_centrality,
    "closeness_centrality": closeness_centrality,
    "betweenness_centrality": betweenness_centrality,
    "clustering_coefficient": clustering_coefficient,
    "core_number": core_number,
    "gnm_fluctuation": gnm_fluctuation,
    "fiedler_amplitude": fiedler_amplitude,
    "slow_mode_participation": slow_mode_participation,
    "protrusion_index": protrusion_index,
    "essa_perturbation": essa_perturbation,
    "alps_spectral_response": alps_spectral_response,
    "distance_to_centroid_negated": distance_to_centroid_negated,
    "local_contact_order": local_contact_order,
    "mean_bfactor": mean_bfactor,
}

SOURCE_CONDITIONED = {
    "distance_from_source_negated": distance_from_source_negated,
    "hop_distance_from_source_negated": hop_distance_from_source_negated,
    "sequence_distance_from_source_negated": sequence_distance_from_source_negated,
    "effective_resistance_to_source": effective_resistance_to_source,
    "hitting_time_to_source_negated": hitting_time_to_source_negated,
    "personalised_pagerank": personalised_pagerank,
    "heat_kernel_from_source": heat_kernel_from_source,
    "regularised_laplacian_kernel": regularised_laplacian_kernel,
    "communicability_from_source": communicability_from_source,
    "gnm_cross_correlation": gnm_cross_correlation,
    "source_conditioned_betweenness": source_conditioned_betweenness,
    "anm_perturbation_response": anm_perturbation_response,
}

SCORERS = SOURCE_BLIND | SOURCE_CONDITIONED
