"""Build the weighted residue graph a method propagates on (pipeline stage S1).

`docs/method/review/11-pipeline-decomposition.md` names S1 the highest-leverage open stage:
better edge weighting matters more than a better propagator, and weighting stays inside C6.
This module makes that testable. It supplies one graph builder with three orthogonal knobs --
node representation, contact rule, edge weighting -- so that "the graph is the leverage
point" becomes an experiment rather than an opinion.

Three rules hold everywhere in this file.

* **Apo only.** The single input is an `ApoInput`. Nothing here opens a manifest, a freeze,
  or a holo structure.
* **No force field.** C6 abstracts atomic force fields away, and C2 forbids MD-derived
  parameters. Every weight below is a function of measured geometry and of the deposited
  element and atom names. No Hinsen constant, no Amber charge, no MD-fitted spring.
* **Heavy atoms only.** `ApoInput.structure` is `in_polymer & _heavy`, so hydrogens are
  absent. Hydrogen-bond and salt-bridge assignment is therefore heavy-atom geometric, with
  no angle term, and the docstrings say so where it matters.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from scipy.spatial import cKDTree

from allo.inputs import ApoInput

__all__ = [
    "CONTACT_RULES",
    "WEIGHTINGS",
    "ResidueGraph",
    "build",
    "min_heavy_distance_to",
    "residue_atom_index",
]

# Heavy atoms that can donate or accept a hydrogen bond. Sulfur is included: it is a weak
# but real acceptor, and excluding it would silently drop every CYS and MET contact.
HBOND_ELEMENTS = frozenset({"N", "O", "S"})
HBOND_CUTOFF = 3.5

# Formally charged side-chain groups at pH 7. HIS is listed because it titrates near
# physiological pH, so leaving it out is as much a choice as putting it in; it carries the
# positive set and its contribution is separable by turning the salt-bridge class off.
POSITIVE_ATOMS = {
    ("ARG", "NE"), ("ARG", "NH1"), ("ARG", "NH2"),
    ("LYS", "NZ"),
    ("HIS", "ND1"), ("HIS", "NE2"),
}  # fmt: skip
NEGATIVE_ATOMS = {
    ("ASP", "OD1"), ("ASP", "OD2"),
    ("GLU", "OE1"), ("GLU", "OE2"),
}  # fmt: skip
SALT_BRIDGE_CUTOFF = 4.0

# Barlow & Thornton, doi:10.1016/S0022-2836(83)80079-5, use 4 A between charged-group
# centroids. 4.0 A between any charged heavy-atom pair is the atom-pair form of the same
# threshold and is what a heavy-atom-only structure can measure.

DISULFIDE_CUTOFF = 2.5

BACKBONE_ATOMS = frozenset({"N", "CA", "C", "O", "OXT"})

CONTACT_RULES = ("heavy_min", "ca", "cb", "sidechain_centroid")
WEIGHTINGS = ("unit", "contact_count", "inverse_square", "exponential", "edge_class", "ohm")


def residue_atom_index(apo: ApoInput) -> tuple[tuple[int, ...], dict[int, int], np.ndarray]:
    """Canonical residue order, its position map, and the per-atom residue index.

    The residue order is ascending author number, which is the ordering every array in this
    package and in `allo.scoring` uses. Returning the per-atom index alongside it means no
    caller has to rebuild the mapping and risk building a different one.
    """
    structure = apo.structure
    heavy = structure.protein
    seq = np.asarray(structure.seq_id[heavy], dtype=int)
    order = tuple(sorted({int(r) for r in seq}))
    position = {r: i for i, r in enumerate(order)}
    return order, position, np.array([position[int(r)] for r in seq], dtype=int)


def _representative(apo: ApoInput, rule: str) -> np.ndarray:
    """One point per residue, for the node representations that use a single point.

    `cb` falls back to CA for glycine, which has no CB. `sidechain_centroid` falls back to
    CA for glycine for the same reason, and never to the whole-residue centroid: a
    whole-residue centroid for glycine and a side-chain centroid for everything else would
    be two different quantities under one name.
    """
    structure = apo.structure
    heavy = structure.protein
    order, position, atom_residue = residue_atom_index(apo)
    coord = np.asarray(structure.coord[heavy], dtype=float)
    atom = np.asarray(structure.atom[heavy])

    points = np.full((len(order), 3), np.nan)
    ca = atom == "CA"
    points[atom_residue[ca]] = coord[ca]
    if rule == "ca":
        return points

    if rule == "cb":
        cb = atom == "CB"
        points[atom_residue[cb]] = coord[cb]
        return points

    side = ~np.isin(atom, list(BACKBONE_ATOMS))
    for index in np.unique(atom_residue[side]):
        chosen = side & (atom_residue == index)
        points[index] = coord[chosen].mean(axis=0)
    return points


def min_heavy_distance_to(apo: ApoInput, residues) -> dict[int, float]:
    """Minimum heavy-atom distance from every residue to a residue set.

    `docs/method/review/06-signal-propagation-physics.md` identifies minimum side-chain
    heavy-atom distance, not Ca distance, as the variable the biological decay law is
    exponential in. This is the whole-residue form of it: it needs no side-chain fallback
    for glycine, and stage S6 fits its decay against exactly this vector.

    A residue in the set has distance 0 by construction, which is correct and which the
    S6 fit must therefore exclude -- it does, because its fit universe removes the source.
    """
    structure = apo.structure
    heavy = structure.protein
    order, position, atom_residue = residue_atom_index(apo)
    coord = np.asarray(structure.coord[heavy], dtype=float)

    wanted = {int(r) for r in residues}
    target = np.array([order[i] in wanted for i in atom_residue])
    if not target.any():
        raise ValueError("distance target set is empty on this structure")

    tree = cKDTree(coord[target])
    distance, _ = tree.query(coord, k=1)
    best = np.full(len(order), np.inf)
    np.minimum.at(best, atom_residue, distance)
    return {residue: float(best[i]) for i, residue in enumerate(order)}


def _edge_geometry(apo: ApoInput, cutoff: float) -> dict[tuple[int, int], dict]:
    """Every residue pair with a heavy-atom contact, with the geometry the weights need.

    One KD-tree pass supplies all of it: the minimum heavy-atom distance, the number of
    contacting atom pairs, and the class flags. Computing them separately would mean three
    passes over the same pairs and three chances for the pair sets to disagree.
    """
    structure = apo.structure
    heavy = structure.protein
    order, position, atom_residue = residue_atom_index(apo)
    coord = np.asarray(structure.coord[heavy], dtype=float)
    atom = np.asarray(structure.atom[heavy])
    element = np.asarray(structure.element[heavy])
    resname = np.asarray(structure.resname[heavy])

    is_hbond_atom = np.isin(element, list(HBOND_ELEMENTS))
    keys = list(zip(resname.tolist(), atom.tolist(), strict=True))
    is_positive = np.array([k in POSITIVE_ATOMS for k in keys])
    is_negative = np.array([k in NEGATIVE_ATOMS for k in keys])
    is_carbon = element == "C"
    is_sulfur = (element == "S") & (atom == "SG")

    tree = cKDTree(coord)
    edges: dict[tuple[int, int], dict] = {}
    for i, j in tree.query_pairs(cutoff):
        a, b = atom_residue[i], atom_residue[j]
        if a == b:
            continue
        key = (a, b) if a < b else (b, a)
        distance = float(np.linalg.norm(coord[i] - coord[j]))
        record = edges.get(key)
        if record is None:
            record = edges[key] = {
                "distance": distance,
                "pairs": 0,
                "hbond": 0,
                "salt_bridge": 0,
                "packing": 0,
                "disulfide": 0,
            }
        record["pairs"] += 1
        record["distance"] = min(record["distance"], distance)
        # No angle term is available: the deposited file carries no hydrogens, and adding
        # them needs a protonation model, which is a force field (C6) or an MD engine (C2).
        if distance <= HBOND_CUTOFF and is_hbond_atom[i] and is_hbond_atom[j]:
            record["hbond"] += 1
        if distance <= SALT_BRIDGE_CUTOFF and (
            (is_positive[i] and is_negative[j]) or (is_negative[i] and is_positive[j])
        ):
            record["salt_bridge"] += 1
        if is_carbon[i] and is_carbon[j]:
            record["packing"] += 1
        if distance <= DISULFIDE_CUTOFF and is_sulfur[i] and is_sulfur[j]:
            record["disulfide"] += 1
    return edges


@dataclass(frozen=True)
class ResidueGraph:
    """A weighted residue graph, plus the geometry and provenance a scorer needs.

    `order` is ascending author number and is the ordering of every array here. `weight` is
    symmetric with a zero diagonal. `source` is the propagation source in residue numbers,
    carried on the graph so that a source-conditioned scorer cannot be handed the wrong one.

    `cache` exists so that an expensive decomposition -- an eigenbasis, a Laplacian
    pseudoinverse, an anisotropic Hessian -- is computed once per graph rather than once per
    scorer. It is deliberately not part of the graph's identity.
    """

    target: str
    order: tuple[int, ...]
    position: dict[int, int]
    weight: np.ndarray
    coord: np.ndarray
    bfactor: np.ndarray
    source: tuple[int, ...]
    config: dict
    cache: dict = field(default_factory=dict, compare=False, repr=False)

    @property
    def n(self) -> int:
        return len(self.order)

    @property
    def adjacency(self) -> np.ndarray:
        return self.weight

    @property
    def degree(self) -> np.ndarray:
        return self.weight.sum(axis=1)

    @property
    def laplacian(self) -> np.ndarray:
        return np.diag(self.degree) - self.weight

    @property
    def source_index(self) -> np.ndarray:
        return np.array([self.position[r] for r in self.source], dtype=int)

    def index(self, residues) -> np.ndarray:
        return np.array([self.position[int(r)] for r in residues], dtype=int)

    def as_scores(self, values: np.ndarray) -> dict[int, float]:
        """Attach residue identity to a score vector.

        Every function returning a residue score returns it with the identity, never as a
        bare array whose ordering the caller must reconstruct (AGENTS.md, Conventions).
        """
        values = np.asarray(values, dtype=float)
        if values.shape != (self.n,):
            raise ValueError(f"{self.target}: expected {self.n} scores, got {values.shape}")
        return {residue: float(v) for residue, v in zip(self.order, values, strict=True)}

    def memo(self, key: str, build_value):
        if key not in self.cache:
            self.cache[key] = build_value()
        return self.cache[key]


def _mean_bfactor(apo) -> np.ndarray:
    """Per-residue mean deposited B-factor over heavy atoms, z-scored across the chain.

    The chain z-score is the right normalisation: an absolute B-factor is not comparable
    between two crystals, because it absorbs the resolution, the refinement protocol and the
    overall scale of the data set (Carugo, doi:10.1186/s12859-018-2083-8).

    It is apo-only and it is not a simulation, so C1 and C2 both pass. It is a *measurement*
    of the crystal, not a prediction of dynamics, and it must never be reported as one.
    """
    structure = apo.structure
    order, _, atom_residue = residue_atom_index(apo)
    values = np.asarray(structure.bfactor[structure.protein], dtype=float)
    total = np.bincount(atom_residue, weights=values, minlength=len(order))
    count = np.bincount(atom_residue, minlength=len(order))
    per_residue = np.where(count > 0, total / np.maximum(count, 1), np.nan)
    filled = np.where(np.isnan(per_residue), np.nanmean(per_residue), per_residue)
    spread = filled.std()
    return (filled - filled.mean()) / spread if spread > 0 else filled - filled.mean()


def build(
    apo: ApoInput,
    *,
    cutoff: float | None = None,
    contact: str = "heavy_min",
    weighting: str = "unit",
    decay_length: float = 4.0,
    class_weights: dict[str, float] | None = None,
    min_seq_sep: int = 0,
) -> ResidueGraph:
    """Build one residue graph from one apo input.

    `cutoff` defaults to the input layer's frozen contact cutoff, which makes the default
    graph the same object the evaluation uses -- the honest starting point for an ablation
    that wants to show a different graph is better.

    `contact` chooses what a distance between two residues means:

    * `heavy_min` -- minimum heavy-atom distance. The evaluation layer's rule.
    * `ca`, `cb` -- single-point distance between alpha or beta carbons. `cb` at 8-10 A is
      the field's most common convention and is what the teammate's benchmark used.
    * `sidechain_centroid` -- centroid of the non-backbone heavy atoms, CA for glycine.

    `weighting` chooses the edge weight:

    * `unit` -- 1 for every contact. The elastic-network default.
    * `contact_count` -- the number of contacting heavy-atom pairs, which is the atom-count
      form of "contact rate" and needs no parameter.
    * `inverse_square` -- 1/d^2 in the contact distance.
    * `exponential` -- exp(-d / `decay_length`).
    * `edge_class` -- a base packing weight plus a bonus per detected hydrogen bond, salt
      bridge and disulfide. `class_weights` sets the bonuses and every value is a free
      parameter, so it is fitted on `development` and never quoted from an MD-parameterised
      source (`docs/method/review/11-pipeline-decomposition.md`, S1 risk).

    * `ohm` -- a saturating contact weight, `1 - exp(-3 N_ij / (a_i a_j))`, where `N_ij` is
      the number of contacting heavy-atom pairs and `a_i` the heavy-atom count of residue i.
      Normalising by the atom counts removes the residue-size artefact that makes a
      tryptophan a hub for no reason other than having more atoms, and the exponential
      saturates so a 12-pair contact and a 20-pair contact are nearly equal. It is the only
      published construction that de-biases residue size explicitly, and it is meant to be
      built at a tighter cutoff than the default -- 3.4 A in its source
      (`docs/method/review/13-graph-construction.md` Q2).

    `min_seq_sep` deletes every edge between residues closer than `min_seq_sep` in author
    numbering. The polymer backbone is a path whose graph distance is proportional to
    sequence separation and therefore, for a folded chain, to Euclidean separation, so it is
    the most distance-faithful part of any contact graph. Removing it forces propagation
    through tertiary packing. The default of 0 keeps every edge and reproduces every graph
    built before 2026-08-26.

    Raises rather than returns a disconnected graph silently: a scorer that inverts a
    Laplacian on a graph with two components returns a number that means nothing, and the
    caller should decide what to do about it.
    """
    if contact not in CONTACT_RULES:
        raise ValueError(f"unknown contact rule {contact!r}; have {CONTACT_RULES}")
    if weighting not in WEIGHTINGS:
        raise ValueError(f"unknown weighting {weighting!r}; have {WEIGHTINGS}")
    cutoff = float(apo.cutoff if cutoff is None else cutoff)
    order, position, owner = residue_atom_index(apo)
    n = len(order)
    weight = np.zeros((n, n))

    if contact == "heavy_min":
        edges = _edge_geometry(apo, cutoff)
        atoms = np.bincount(owner, minlength=n).astype(float)
        bonus = {"hbond": 1.0, "salt_bridge": 1.0, "disulfide": 2.0} | (class_weights or {})
        for (a, b), record in edges.items():
            distance = max(record["distance"], 1e-6)
            if weighting == "unit":
                value = 1.0
            elif weighting == "contact_count":
                value = float(record["pairs"])
            elif weighting == "inverse_square":
                value = 1.0 / distance**2
            elif weighting == "exponential":
                value = float(np.exp(-distance / decay_length))
            elif weighting == "ohm":
                pairs = float(record["pairs"]) / max(atoms[a] * atoms[b], 1)
                value = float(1.0 - np.exp(-3.0 * pairs))
            else:
                value = 1.0
                for name, scale in bonus.items():
                    if record[name]:
                        value += scale
            weight[a, b] = weight[b, a] = value
    else:
        points = _representative(apo, contact)
        if np.isnan(points).any():
            missing = [order[i] for i in np.flatnonzero(np.isnan(points).any(axis=1))]
            raise ValueError(f"{apo.target}: residues {missing} have no {contact} point")
        distance = np.linalg.norm(points[:, None, :] - points[None, :, :], axis=-1)
        contacting = (distance <= cutoff) & ~np.eye(n, dtype=bool)
        safe = np.where(contacting, np.maximum(distance, 1e-6), 1.0)
        if weighting == "unit":
            weight = contacting.astype(float)
        elif weighting == "inverse_square":
            weight = np.where(contacting, 1.0 / safe**2, 0.0)
        elif weighting == "exponential":
            weight = np.where(contacting, np.exp(-safe / decay_length), 0.0)
        else:
            raise ValueError(f"{weighting!r} needs heavy-atom contacts; use contact='heavy_min'")

    if min_seq_sep > 0:
        numbers = np.asarray(order, dtype=int)
        near = np.abs(numbers[:, None] - numbers[None, :]) < min_seq_sep
        weight = np.where(near, 0.0, weight)

    graph = ResidueGraph(
        target=apo.target,
        order=order,
        position=position,
        weight=weight,
        coord=_representative(apo, "ca"),
        bfactor=_mean_bfactor(apo),
        source=tuple(sorted(apo.active_site)),
        config={
            "cutoff_angstrom": cutoff,
            "contact": contact,
            "weighting": weighting,
            "min_seq_sep": min_seq_sep,
            "decay_length": decay_length if weighting == "exponential" else None,
            "class_weights": (
                {"hbond": 1.0, "salt_bridge": 1.0, "disulfide": 2.0} | (class_weights or {})
                if weighting == "edge_class"
                else None
            ),
        },
    )
    isolated = [order[i] for i in np.flatnonzero(graph.degree == 0)]
    if isolated:
        raise ValueError(
            f"{apo.target}: residues {isolated} have no contact at cutoff {cutoff}; a "
            "propagation score on a graph with isolated nodes is undefined"
        )
    return graph
