"""The evaluation graph, the matched-patch null, and the fields used to calibrate it.

**The graph in this module is not the method's graph.** It is fixed at the input layer's
frozen `contact_cutoff_angstrom`, heavy-atom minimum distance, and it never moves. A
method is free to choose its own cutoff, weighting and node representation -- that is a
hyperparameter, chosen on the secondary set's `development` tier. Scoring both methods
against one fixed graph is what makes their p-values comparable.

Why a matched patch and not a random draw of residues: an allosteric label set is a
spatially contiguous, partly buried patch, and any connectivity score favours contiguous
buried residues. Drawing m residues uniformly asks "are these m residues higher than m
random ones", which a method answers correctly by finding *any* buried blob. On residue
contact graphs specifically, nulls that ignore spatial embedding "tend to identify as
significantly (under-) over-represented almost all analyzed subgraphs"
(Milenkovic, Filippis, Lappe & Przulj, doi:10.1371/journal.pone.0005967). And the confound
is measured in this method's own family: elastic-network perturbation-response residues are
enriched in heavy-atom contact by 3.56-3.69x over random across 502 structure pairs
(Zheng & Tekpinar, doi:10.1186/1472-6807-9-45).
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path

import numpy as np
from scipy.spatial import cKDTree

from allo.inputs import ROOT, ApoInput

__all__ = [
    "PATCH_CACHE",
    "EvaluationGraph",
    "MatchedPoolUnavailable",
    "component_sizes",
    "evaluation_graph",
    "field_factor",
    "matched_patches",
    "permutation_p",
    "sample_matched_patches",
    "smooth_field",
]


class MatchedPoolUnavailable(RuntimeError):
    """The matched-patch pool cannot be drawn at the requested tolerance and attempt budget.

    Raised, not returned, because a short pool is never a usable null: the replicate count
    sets the p-value floor, so quietly returning fewer patches would move a number.

    It is a distinct type because the callers must tell "this graph cannot supply a matched
    pool at this tolerance" apart from any other RuntimeError. **No caller may answer it by
    widening the tolerance for the arm that failed.** The scoring tolerance is frozen at
    0.10 by the ADR 0023 sweep, and a per-arm tolerance chosen after an arm failed is a
    per-arm hyperparameter, which is the one thing this protocol exists to prevent.

    Where it fires, and where it does not. On 2026-09-02 it fired on
    `cardiac_myosin_mandated` -- the 20 A homology model ADR 0031 exposes as defective --
    on the **0.05 rung of the calibration sweep**, at 822 of 999 patches in 3 996 000
    attempts. It does **not** fire on that arm at the frozen 0.10, where 999 patches draw at
    an acceptance rate of 0.000884. So the sweep records the rung as undrawable and the
    scored arm keeps its null. A caller that runs at the frozen tolerance and still sees
    this exception has an arm whose graph is unlike every graph the protocol was calibrated
    on, and must report that arm without a matched-patch null rather than retune it.
    """

    def __init__(
        self,
        message: str,
        *,
        target: str,
        drawn: int,
        wanted: int,
        attempts: int,
        rejected: dict[str, int],
        observed: dict,
    ) -> None:
        super().__init__(message)
        self.target = target
        self.drawn = drawn
        self.wanted = wanted
        self.attempts = attempts
        self.rejected = rejected
        # The properties the draw was matching on. They are what a reader needs to see why
        # no patch matched, and carrying them keeps the record the same shape as a
        # successful draw's.
        self.observed = observed

    def diagnostics(self) -> dict:
        return {
            "available": False,
            "reason": "matched pool undrawable at the frozen tolerance",
            "drawn": self.drawn,
            "wanted": self.wanted,
            "attempts": self.attempts,
            "acceptance_rate": round(self.drawn / self.attempts, 8) if self.attempts else 0.0,
            "rejected": self.rejected,
            **self.observed,
        }


@dataclass(frozen=True)
class EvaluationGraph:
    """Residue contact graph of one frozen apo input, plus the geometry the null matches on.

    `order` is the canonical residue ordering for every array in this package: the frozen
    node set, ascending by author number. A score vector is only interpretable against it.
    """

    target: str
    order: tuple[int, ...]
    adjacency: tuple[frozenset[int], ...]
    degree: np.ndarray
    ca_coord: np.ndarray
    candidates: tuple[int, ...]
    source: tuple[int, ...]
    position: dict[int, int]

    def index(self, residues) -> np.ndarray:
        """Boolean mask over `order` for a residue-number collection."""
        wanted = set(residues)
        return np.array([r in wanted for r in self.order], dtype=bool)

    def neighbours(self, residue: int) -> frozenset[int]:
        return self.adjacency[self.position[residue]]

    def radius_of_gyration(self, residues) -> float:
        """Root mean square Ca distance from the patch centroid.

        This is the property that sets the variance of a patch mean under a spatially
        autocorrelated score, so it is the property a matched null has to match. Measured
        on the frozen arms, unmatched frontier growth misses it badly: the myosin label set
        has Rg 8.9 A against 21.1 +/- 6.7 A for size-and-component-matched patches, because
        its two lobes are adjacent while two freely grown lobes land anywhere in a
        764-residue chain.
        """
        coords = self.ca_coord[[self.position[r] for r in residues]]
        return float(np.sqrt(((coords - coords.mean(0)) ** 2).sum(1).mean()))


def evaluation_graph(apo: ApoInput) -> EvaluationGraph:
    """Build the fixed evaluation graph from what a method receives, and nothing else.

    Heavy-atom minimum distance at the frozen cutoff. Uses a KD-tree because the myosin arm
    is 764 residues and the dense atom-pair matrix for it is 288 MB.
    """
    structure = apo.structure
    heavy = structure.protein
    seq = structure.seq_id[heavy]
    coord = structure.coord[heavy]
    order = tuple(sorted(set(int(r) for r in seq)))
    position = {r: i for i, r in enumerate(order)}

    tree = cKDTree(coord)
    linked: list[set[int]] = [set() for _ in order]
    for i, j in tree.query_pairs(apo.cutoff):
        a, b = int(seq[i]), int(seq[j])
        if a != b:
            linked[position[a]].add(b)
            linked[position[b]].add(a)

    ca = structure.atom[heavy] == "CA"
    ca_by_residue = {int(r): c for r, c in zip(seq[ca], coord[ca], strict=True)}
    missing = [r for r in order if r not in ca_by_residue]
    if missing:
        raise ValueError(f"{apo.target}: residues {missing} have no CA atom")

    source = tuple(sorted(apo.active_site))
    return EvaluationGraph(
        target=apo.target,
        order=order,
        adjacency=tuple(frozenset(s) for s in linked),
        degree=np.array([len(s) for s in linked], dtype=float),
        ca_coord=np.array([ca_by_residue[r] for r in order]),
        candidates=tuple(r for r in order if r not in set(source)),
        source=source,
        position=position,
    )


def component_sizes(graph: EvaluationGraph, residues) -> tuple[int, ...]:
    """Sizes of the connected components of the subgraph induced on `residues`, descending.

    The null matches this multiset rather than requiring one connected blob. Two of the
    five frozen primary label sets are disconnected -- `bcr_abl1_corrected` is [17, 1] and
    `cardiac_myosin_corrected` is [8, 4] -- so sampling connected blobs against a two-lobed
    observation would impose a property the observation lacks, which is anti-conservative.
    """
    remaining = set(residues)
    sizes = []
    while remaining:
        stack = [remaining.pop()]
        size = 0
        while stack:
            node = stack.pop()
            size += 1
            for neighbour in graph.neighbours(node):
                if neighbour in remaining:
                    remaining.discard(neighbour)
                    stack.append(neighbour)
        sizes.append(size)
    return tuple(sorted(sizes, reverse=True))


def _grow(graph: EvaluationGraph, size: int, pool: set[int], rng: np.random.Generator):
    """Grow one component of `size` residues inside `pool` by uniform contact frontier."""
    patch = {int(rng.choice(sorted(pool)))}
    while len(patch) < size:
        frontier = sorted({n for r in patch for n in graph.neighbours(r) if n in pool} - patch)
        if not frontier:
            return None
        patch.add(int(rng.choice(frontier)))
    return patch


def sample_matched_patches(
    graph: EvaluationGraph,
    observed,
    *,
    n_patches: int,
    tolerance: float,
    seed: int,
    match_distance: bool = False,
    max_attempts_per_patch: int = 4000,
) -> tuple[np.ndarray, dict]:
    """Draw `n_patches` residue sets matched to `observed` on size, components and burial.

    Matching, in full:

    * **size** -- the same number of residues,
    * **components** -- the same component-size multiset, with the components mutually
      non-adjacent so a sampled two-lobed patch really is two-lobed,
    * **burial** -- patch mean contact degree, which is the confound that makes an
      unmatched null useless for a connectivity score,
    * **compactness** -- patch radius of gyration, which is what sets the variance of a
      patch mean under a spatially autocorrelated score, and is therefore what decides
      whether the test holds its size at all,
    * **distance to the propagation source** -- optional and off by default. Matching it
      asks the narrower question "does propagation add anything beyond geometry"; it is
      pre-registered as a secondary null, not as the confirmatory one, because the
      confirmatory question the challenge poses is enrichment against background. This
      sub-field's name for the confound is "distance bias"
      (ProteinLens, doi:10.1093/nar/gkab350), and the one lineage that controls it does so
      by quantile regression rather than by matching
      (Amor et al., doi:10.1038/ncomms12477).

    `tolerance` is one relative bound applied to both burial and compactness. It is not a
    free choice: it is fixed by the calibration gate in :mod:`allo.scoring.calibration` and
    pinned in the evaluation manifest (ADR 0018).

    Returns the patches as a boolean matrix over `graph.order`, and a diagnostics dict.
    Raises if the requested number cannot be drawn -- a silent short draw would make the
    p-value's denominator a lie.
    """
    rng = np.random.default_rng(seed)
    observed = sorted(set(observed))
    pool = set(graph.candidates)
    if not set(observed) <= pool:
        raise ValueError(f"{graph.target}: observed patch leaves the candidate set")

    wanted_components = component_sizes(graph, observed)
    mask = graph.index(observed)
    wanted_degree = float(graph.degree[mask].mean())
    source_mask = graph.index(graph.source)
    to_source = np.linalg.norm(
        graph.ca_coord[:, None, :] - graph.ca_coord[None, source_mask, :], axis=-1
    ).min(axis=1)
    wanted_distance = float(np.median(to_source[mask]))
    wanted_rg = graph.radius_of_gyration(observed)
    observed_geometry = {
        "observed_components": list(wanted_components),
        "observed_mean_degree": round(wanted_degree, 4),
        "observed_radius_of_gyration": round(wanted_rg, 4),
        "observed_median_distance_to_source": round(wanted_distance, 4),
    }

    patches = np.zeros((n_patches, len(graph.order)), dtype=bool)
    rejected = {"frontier": 0, "adjacent": 0, "degree": 0, "compactness": 0, "distance": 0}
    drawn = 0
    attempts = 0
    budget = n_patches * max_attempts_per_patch
    while drawn < n_patches and attempts < budget:
        attempts += 1
        residues: set[int] = set()
        blocked: set[int] = set()
        for size in wanted_components:
            grown = _grow(graph, size, pool - residues - blocked, rng)
            if grown is None:
                residues = set()
                rejected["frontier"] += 1
                break
            residues |= grown
            # Keep the components apart, or [17, 1] silently becomes [18].
            blocked |= {n for r in grown for n in graph.neighbours(r)}
        if not residues:
            continue
        candidate_mask = graph.index(residues)
        if component_sizes(graph, residues) != wanted_components:
            rejected["adjacent"] += 1
            continue
        if abs(graph.degree[candidate_mask].mean() - wanted_degree) > tolerance * wanted_degree:
            rejected["degree"] += 1
            continue
        if abs(graph.radius_of_gyration(residues) - wanted_rg) > tolerance * wanted_rg:
            rejected["compactness"] += 1
            continue
        if (
            match_distance
            and abs(np.median(to_source[candidate_mask]) - wanted_distance)
            > tolerance * wanted_distance
        ):
            rejected["distance"] += 1
            continue
        patches[drawn] = candidate_mask
        drawn += 1

    if drawn < n_patches:
        raise MatchedPoolUnavailable(
            f"{graph.target}: drew {drawn} of {n_patches} matched patches in {attempts} "
            f"attempts (rejections {rejected}). Widen the tolerance deliberately and "
            f"re-freeze; do not shrink the replicate count.",
            target=graph.target,
            drawn=drawn,
            wanted=n_patches,
            attempts=attempts,
            rejected=dict(rejected),
            observed=observed_geometry,
        )
    diagnostics = {
        "attempts": attempts,
        "acceptance_rate": round(n_patches / attempts, 6),
        "rejected": rejected,
        **observed_geometry,
        "sampled_mean_degree": round(float((patches @ graph.degree / patches.sum(1)).mean()), 4),
        "sampled_radius_of_gyration": round(
            float(
                np.mean(
                    [
                        graph.radius_of_gyration(
                            [r for r, on in zip(graph.order, row, strict=True) if on]
                        )
                        for row in patches
                    ]
                )
            ),
            4,
        ),
    }
    return patches, diagnostics


def permutation_p(observed: float, null: np.ndarray) -> float:
    """Upper-tail p with the plus-one correction: (1 + #{null >= observed}) / (1 + B).

    One-sided by design and not by convenience. A method that ranks allosteric residues
    *below* background is a broken method, not a competing finding.
    """
    return float((1 + int((null >= observed).sum())) / (1 + len(null)))


def field_factor(ca_coord: np.ndarray, length_scale: float) -> np.ndarray:
    """Cholesky factor of the exponential covariance exp(-d / lambda) over Ca distances.

    Takes coordinates rather than a graph so that the calibration can factorise the
    covariance of the *candidate* subset directly. Restricting a factor of the full
    covariance is not the same matrix as the factor of the restricted covariance, and the
    difference is not small.

    Split from the draw because the myosin arm is 764 nodes and the calibration takes a
    thousand draws per arm: the factor is computed once, each draw is one matrix-vector
    product.
    """
    distance = np.linalg.norm(ca_coord[:, None, :] - ca_coord[None, :, :], axis=-1)
    covariance = np.exp(-distance / length_scale)
    covariance[np.diag_indices_from(covariance)] += 1e-8
    return np.linalg.cholesky(covariance)


def smooth_field(factor: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """One draw of a site-uninformative Gaussian field from :func:`field_factor`.

    This is the calibration instrument, not a baseline. It knows nothing about the label
    set, so under any correctly sized test its rejection rate must equal alpha; it is
    spatially autocorrelated, so it reproduces the property that makes an unmatched
    rank-sum test reject far too often.
    """
    return factor @ rng.standard_normal(len(factor))


PATCH_CACHE = ROOT / "data" / "patches"


def matched_patches(
    graph: EvaluationGraph,
    observed,
    *,
    n_patches: int,
    tolerance: float,
    seed: int,
    match_distance: bool = False,
    cache: Path | None = PATCH_CACHE,
) -> tuple[np.ndarray, dict]:
    """:func:`sample_matched_patches`, memoised on disk.

    The pool depends on the arm and the protocol, never on the method being scored. Caching
    it is not only a speed fix: it means every method is tested against the **identical**
    null sample, so a difference between two methods cannot be sampler noise. The cache is
    gitignored and fully reproducible from the frozen seed, so deleting it costs time and
    nothing else.
    """
    if cache is None:
        return sample_matched_patches(
            graph,
            observed,
            n_patches=n_patches,
            tolerance=tolerance,
            seed=seed,
            match_distance=match_distance,
        )
    # The key must cover everything the sample depends on, not only the knobs. It also
    # depends on the observed patch and on the graph, and leaving those out meant a changed
    # label set or contact cutoff returned stale patches and `allo evaluate verify` still
    # exited 0 -- a false green in exactly the case verification exists to catch.
    # The digest covers every input the sampler reads, which until 2026-09-02 it did not.
    # `order` and `source` do not move with the contact cutoff, so the digest was identical
    # at cutoffs 4.5, 6.0 and 8.0 on `cardiac_myosin_corrected` while the mean degree ran
    # 9.531, 13.398, 24.262 -- and the pool is matched on `mean_degree` and
    # `radius_of_gyration`. A cutoff change returned a pool matched to the wrong geometry
    # and `allo evaluate verify` still exited 0, because `_derive_arm` writes the cached
    # diagnostics into the freeze and the comparison was stale against stale.
    #
    # `adjacency` and not just `degree`, because the sampler grows patches and counts
    # components from the neighbour sets, so an edge rewiring at unchanged degree is a
    # different sampler. `ca_coord` because `radius_of_gyration` and the distance match read
    # coordinates directly. The cutoff had never moved, so no recorded number was affected.
    digest = sha256(
        repr(
            (
                sorted(set(observed)),
                graph.order,
                tuple(sorted(graph.source)),
                tuple(tuple(sorted(s)) for s in graph.adjacency),
                np.ascontiguousarray(graph.ca_coord, dtype=np.float64).tobytes(),
            )
        ).encode()
    ).hexdigest()[:12]
    key = f"{graph.target}-n{n_patches}-t{tolerance}-s{seed}-d{int(match_distance)}-{digest}.npz"
    path = cache / key
    if path.exists():
        stored = np.load(path, allow_pickle=False)
        patches = np.zeros((n_patches, len(graph.order)), dtype=bool)
        np.put_along_axis(patches, stored["members"], True, axis=1)
        return patches, json.loads(str(stored["diagnostics"]))
    patches, diagnostics = sample_matched_patches(
        graph,
        observed,
        n_patches=n_patches,
        tolerance=tolerance,
        seed=seed,
        match_distance=match_distance,
    )
    cache.mkdir(parents=True, exist_ok=True)
    members = np.array([np.flatnonzero(row) for row in patches], dtype=np.int32)
    np.savez_compressed(path, members=members, diagnostics=json.dumps(diagnostics))
    return patches, diagnostics
