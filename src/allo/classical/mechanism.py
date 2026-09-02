"""Three constructions read off the cross-system mechanism review, not off a method paper.

`baselines.py` holds the standard battery and `coupling.py` holds the source-conditioned
transport measures. This module holds the scores that came out of asking a different
question: across the seven systems whose allosteric mechanism is described in atomic detail
in the literature, what *structural signature* recurs, and which of those signatures is
visible in an apo structure alone? `docs/method/exploration/lit/26-system-mechanisms.md`
ranks eight of them by how many independent systems support each. Three are both
apo-observable and not already in the repo, and they are here.

* **Module boundary** (8 systems). Allosteric sites sit where two quasi-rigid domains meet:
  the haemoglobin dimer interface, the two kinase lobes, the myosin subdomain junctions, the
  glucokinase hinge. `module_boundary` scores a residue by how many distinct slow-mode
  domains it touches. It is the only signature in that review with an allosteric-specific
  effect size attached (PPV 0.65 at sensitivity 0.22 over 91 proteins,
  doi:10.1186/1471-2105-13-273).
* **Soft corridor** (6 systems). Evolved elastic networks develop a *less* constrained
  channel between coupled sites, not a stiffer one (doi:10.1073/pnas.1615536114), and about
  one per cent of bonds is enough to carry the coupling (doi:10.1073/pnas.1612139114).
  `soft_corridor_to_source` finds the route to the active site whose tightest residue is as
  loose as possible. It is the one score here that is not monotone in distance, so it is the
  one that can beat the negated-distance control for a reason rather than by accident.
* **Strain against diffusion** (5 systems). A random walk sums conductance over parallel
  routes; a mechanical signal takes the single stiffest chain and is limited by its weakest
  link. `strain_versus_diffusion` scores the difference, so a residue only ranks high if it
  is mechanically well connected *and* diffusively remote — which is what a distal allosteric
  residue is.

These are constructions, not reimplementations. Signature 8 of that review — the residues
whose contacts change between two functional states — is the single most predictive class in
the field and is forbidden by C1, because the second state is the holo structure. It is
recorded there as a named limitation and is deliberately absent here.

Every score runs on the apo graph alone. Prediction-path code: no `allo.groundtruth`, no
`allo.scoring`.
"""

from __future__ import annotations

import numpy as np

from allo.classical.baselines import spectrum
from allo.network.graph import ResidueGraph

__all__ = ["SCORERS"]

_FLOOR = 1e-12


def module_boundary(graph: ResidueGraph, modes: int = 3) -> np.ndarray:
    """How many distinct slow-mode domains a residue's own contacts belong to.

    The domain partition is the sign word of the lowest `modes` non-trivial Gaussian network
    modes. A slow mode changes sign exactly at the hinge that separates the two blocks it
    moves against each other, which is the classical GNM hinge definition (Bahar,
    doi:10.1016/S1359-0278(97)00024-2), so the joint sign pattern over the lowest few modes
    labels each residue with the quasi-rigid block it belongs to. A residue is on a boundary
    when its neighbours carry more than one label.

    The sign word is used rather than k-means on the eigenvectors because it is
    deterministic. Spectral clustering would need a seed and would put a stochastic step in
    the middle of a score that has no reason to have one.

    Zero to `modes` is the full range of the raw count, so the count is weighted by the
    residue's own slow-mode amplitude. A residue at a boundary that barely moves is not a
    hinge, and the amplitude is what separates the two.
    """

    def build():
        values, vectors = spectrum(graph, "laplacian")
        keep = vectors[:, 1 : 1 + modes]
        label = np.zeros(graph.n, dtype=np.int64)
        for column in range(keep.shape[1]):
            label = label * 2 + (keep[:, column] > 0).astype(np.int64)
        contacts = graph.adjacency > 0
        distinct = np.array(
            [len(np.unique(label[contacts[i]])) - 1 for i in range(graph.n)], dtype=float
        )
        amplitude = (keep**2 / np.maximum(values[1 : 1 + modes], _FLOOR)).sum(axis=1)
        return distinct * np.sqrt(amplitude)

    return graph.memo(f"module_boundary:{modes}", build)


def soft_corridor_to_source(graph: ResidueGraph, steepness: float = 1.0) -> np.ndarray:
    """The looseness of the tightest residue on the loosest route to the active site.

    Two steps. First a coordination deficit: the weighted contact number
    `w(i) = sum_j 1 / d_ij^2` measures how tightly residue i is packed, and it is z-scored
    inside deciles of the residue's distance to the chain centroid, so the score says "looser
    than its own depth predicts" rather than "near the surface". Depth is already in the
    frozen matched-patch null, and a score that only repeats it cannot reject that null.

    Second a widest-path search. Each residue is given a capacity
    `c(i) = 1 / (1 + exp(steepness * z(i)))`, and the score is the maximum over all routes to
    the active site of the minimum capacity along the route. This is a max-min, not a sum, so
    a single tight residue closes a corridor no matter how many loose residues surround it.

    The construction follows the two measurements the mechanism review reports: an evolved
    allosteric network develops a *less* constrained trumpet between its two sites
    (doi:10.1073/pnas.1615536114), and roughly one per cent of the bonds carries the coupling
    (doi:10.1073/pnas.1612139114). Both say the corridor is defined by what it lacks.
    """

    def build():
        separation = np.linalg.norm(graph.coord[:, None, :] - graph.coord[None, :, :], axis=-1)
        np.fill_diagonal(separation, np.inf)
        packing = (1.0 / np.maximum(separation, _FLOOR) ** 2).sum(axis=1)

        depth = np.linalg.norm(graph.coord - graph.coord.mean(axis=0), axis=1)
        deficit = np.zeros(graph.n)
        edges = np.quantile(depth, np.linspace(0.0, 1.0, 11))
        for low, high in zip(edges[:-1], edges[1:], strict=True):
            inside = (depth >= low) & (depth <= high)
            if inside.sum() < 3:
                continue
            block = packing[inside]
            spread = block.std()
            deficit[inside] = (block - block.mean()) / spread if spread > 0 else 0.0

        capacity = 1.0 / (1.0 + np.exp(steepness * deficit))
        # Widest path by a Prim sweep from the contracted source, carrying the minimum node
        # capacity rather than the minimum edge weight.
        best = np.full(graph.n, -np.inf)
        best[graph.source_index] = np.inf
        settled = np.zeros(graph.n, dtype=bool)
        for _ in range(graph.n):
            available = np.where(settled, -np.inf, best)
            node = int(np.argmax(available))
            if available[node] == -np.inf:
                break
            settled[node] = True
            reachable = (graph.weight[node] > 0) & ~settled
            through = np.minimum(best[node], capacity)
            best = np.where(reachable & (through > best), through, best)
        finite = best[np.isfinite(best)]
        return np.where(np.isfinite(best), best, finite.min() if len(finite) else 0.0)

    return graph.memo(f"soft_corridor:{steepness}", build)


def strain_versus_diffusion(graph: ResidueGraph, time: float = 1.0) -> np.ndarray:
    """Mechanical connection to the active site, with diffusive proximity removed.

    A random walk on a contact graph adds conductance over every parallel route, so a residue
    surrounded by many weak contacts scores as well as one on a single stiff chain. A
    mechanical signal does not work that way: it follows one load path and is limited by that
    path's weakest link. The mechanism review makes this its sharpest methodological point,
    and the two quantities are separable, so the difference is a score.

    `midrank(bottleneck) - midrank(heat kernel)`. The bottleneck term is the max-min path
    capacity to the active site; the diffusive term is `exp(-L t)` from the active site,
    which is the field the bottleneck must be read against. Both are converted to midranks
    first, so the difference does not depend on either one's units or on the shape of its
    tail.

    A residue ranks high only when it is mechanically well connected *and* diffusively
    remote. That combination is what distinguishes a distal allosteric residue from a
    neighbour of the active site, which scores high on both and therefore nets to zero.
    """

    def build():
        capacity = np.full(graph.n, -np.inf)
        capacity[graph.source_index] = np.inf
        settled = np.zeros(graph.n, dtype=bool)
        for _ in range(graph.n):
            available = np.where(settled, -np.inf, capacity)
            node = int(np.argmax(available))
            if available[node] == -np.inf:
                break
            settled[node] = True
            reachable = (graph.weight[node] > 0) & ~settled
            through = np.minimum(capacity[node], graph.weight[node])
            capacity = np.where(reachable & (through > capacity), through, capacity)
        finite = capacity[np.isfinite(capacity)]
        strain = np.where(np.isfinite(capacity), capacity, finite.min() if len(finite) else 0.0)

        values, vectors = spectrum(graph, "laplacian")
        kernel = (vectors * np.exp(-time * values)) @ vectors.T
        diffusion = kernel[:, graph.source_index].max(axis=1)
        return _midrank(strain) - _midrank(diffusion)

    return graph.memo(f"strain_vs_diffusion:{time}", build)


def _midrank(values: np.ndarray) -> np.ndarray:
    """Average rank of tied values, scaled to [0, 1]. Local copy: `postprocess` is stage S6."""
    order = np.argsort(values, kind="stable")
    ranks = np.empty(len(values), dtype=float)
    ranks[order] = np.arange(len(values), dtype=float)
    for value in np.unique(values):
        tied = values == value
        ranks[tied] = ranks[tied].mean()
    return ranks / max(len(values) - 1, 1)


def stiff_corridor_to_source(graph: ResidueGraph, steepness: float = 1.0) -> np.ndarray:
    """`soft_corridor_to_source` with the sign reversed: the tightest corridor, not the loosest.

    The sign is a free parameter, and this is where it was fixed. The soft direction is the
    published prediction — an evolved allosteric network develops a *less* constrained
    channel between its two sites (doi:10.1073/pnas.1615536114) — and it was built and
    measured first. On the four `development` arms it runs the wrong way, at mean AUC 0.31
    to 0.35 in every one of five confound-removal forms and on all three graphs, with a rank
    correlation of only 0.05 against the negated distance to the active site. A score that
    weak on distance and that consistent across arms is not measuring proximity and is not
    measuring noise. It is measuring constraint, with the opposite sign to the hypothesis.

    So the observation is that the residues our label sets contain sit on the *constrained*
    side of the coordination-deficit axis. Fixing the sign here is exactly what the
    `development` tier is for (ADR 0021): the choice is made on four arms that are never
    scored again, and the primary benchmark sees it already frozen.

    Reported as a refuted prediction, not as a discovery. What was tested is whether the
    evolved-network softness result transfers to crystallographic allosteric sites in real
    proteins, and on this benchmark it does not.
    """
    return -soft_corridor_to_source(graph, steepness=steepness)


SCORERS = {
    "module_boundary": module_boundary,
    "soft_corridor_to_source": soft_corridor_to_source,
    "stiff_corridor_to_source": stiff_corridor_to_source,
    "strain_versus_diffusion": strain_versus_diffusion,
}
