"""Residue properties every propagation score is read against.

The first question asked of any distal-site score is whether it is a burial proxy or a
flexibility proxy in disguise. `docs/benchmark/evaluation/README.md` section 11 controls
burial *inside* the null, which is the stronger treatment, but it leaves the reader with no
number. These are that number: one Spearman correlation per property, printed beside every
result, so the question is answered before it is asked (ADR 0025).

**All three run on the apo input alone and touch no label.** They are confounders of the
score, not of the benchmark, so they are computed at score time rather than frozen. A frozen
value would be identical for every method and would say nothing about any of them.

Conservation is the fourth confounder the audit named and it is absent, because it needs a
multiple-sequence alignment against an external database. That is a network dependency the
offline gate cannot carry. Recorded as unknown rather than approximated.
"""

from __future__ import annotations

import numpy as np
from scipy.spatial import cKDTree

from allo.inputs import ApoInput

__all__ = ["KYTE_DOOLITTLE", "MAX_ACCESSIBLE_AREA", "residue_properties", "solvent_accessibility"]

# Kyte & Doolittle hydropathy, doi:10.1016/0022-2836(82)90515-0, table I.
KYTE_DOOLITTLE = {
    "ILE": 4.5, "VAL": 4.2, "LEU": 3.8, "PHE": 2.8, "CYS": 2.5,
    "MET": 1.9, "ALA": 1.8, "GLY": -0.4, "THR": -0.7, "SER": -0.8,
    "TRP": -0.9, "TYR": -1.3, "PRO": -1.6, "HIS": -3.2, "GLU": -3.5,
    "GLN": -3.5, "ASP": -3.5, "ASN": -3.5, "LYS": -3.9, "ARG": -4.5,
}  # fmt: skip

# Theoretical maximum accessible surface area per residue, Tien et al. 2013,
# doi:10.1371/journal.pone.0080635, table 1 "Theoretical" column. The denominator that turns
# absolute SASA into RSA. Theoretical rather than empirical because it is a fixed constant
# and not a value measured on some other protein set.
MAX_ACCESSIBLE_AREA = {
    "ALA": 129.0, "ARG": 274.0, "ASN": 195.0, "ASP": 193.0, "CYS": 167.0,
    "GLN": 225.0, "GLU": 223.0, "GLY": 104.0, "HIS": 224.0, "ILE": 197.0,
    "LEU": 201.0, "LYS": 236.0, "MET": 224.0, "PHE": 240.0, "PRO": 159.0,
    "SER": 155.0, "THR": 172.0, "TRP": 285.0, "TYR": 263.0, "VAL": 174.0,
}  # fmt: skip

# Bondi van der Waals radii, doi:10.1021/j100785a001, for the elements a protein chain has.
BONDI_RADII = {"C": 1.70, "N": 1.55, "O": 1.52, "S": 1.80}
PROBE_RADIUS = 1.4


def _sphere_points(count: int) -> np.ndarray:
    """`count` near-uniform points on the unit sphere, by the golden-angle spiral.

    Deterministic by construction. Shrake & Rupley's original numerical integration used a
    random or icosahedral set; the spiral needs no seed, which matters because every
    stochastic step in this repo has to take one.
    """
    index = np.arange(count) + 0.5
    z = 1.0 - 2.0 * index / count
    radius = np.sqrt(np.maximum(0.0, 1.0 - z * z))
    angle = np.pi * (1.0 + 5.0**0.5) * index
    return np.column_stack([radius * np.cos(angle), radius * np.sin(angle), z])


def solvent_accessibility(apo: ApoInput, *, points: int = 92) -> dict[int, float]:
    """Relative solvent accessibility per residue, by Shrake-Rupley numerical integration.

    Shrake & Rupley 1973, doi:10.1016/0022-2836(73)90011-9: roll a probe of radius 1.4 A over
    the van der Waals surface and integrate the reachable area. Implemented here rather than
    taken from a library because the input is a set of parallel arrays, not an object tree,
    and the conversion costs more code than the algorithm.

    Returns absolute SASA divided by the residue's theoretical maximum, so 0 is fully buried
    and about 1 is fully exposed. A value can exceed 1 for a terminal or strained residue;
    it is not clipped, because clipping would hide that.
    """
    structure = apo.structure
    mask = structure.protein
    coords = np.asarray(structure.coord[mask], dtype=float)
    radii = np.array([BONDI_RADII.get(str(element), 1.70) for element in structure.element[mask]])
    seq_id = np.asarray(structure.seq_id[mask])
    resname = np.asarray(structure.resname[mask])

    inflated = radii + PROBE_RADIUS
    unit = _sphere_points(points)
    tree = cKDTree(coords)
    # Any atom that can occlude atom i lies within its inflated radius plus the largest one.
    neighbours = tree.query_ball_point(coords, inflated + inflated.max())

    area = np.empty(len(coords))
    for i, near in enumerate(neighbours):
        other = np.array([j for j in near if j != i], dtype=int)
        shell = coords[i] + inflated[i] * unit
        if len(other):
            distance = np.linalg.norm(shell[:, None, :] - coords[other][None, :, :], axis=-1)
            exposed = np.all(distance >= inflated[other][None, :], axis=1)
        else:
            exposed = np.ones(points, dtype=bool)
        area[i] = 4.0 * np.pi * inflated[i] ** 2 * exposed.mean()

    absolute: dict[int, float] = {}
    reference: dict[int, str] = {}
    for residue, name, value in zip(seq_id, resname, area, strict=True):
        absolute[int(residue)] = absolute.get(int(residue), 0.0) + float(value)
        reference[int(residue)] = str(name)
    return {
        residue: total / MAX_ACCESSIBLE_AREA.get(reference[residue], 200.0)
        for residue, total in absolute.items()
    }


def residue_properties(apo: ApoInput) -> dict[str, dict[int, float]]:
    """The three confounders computable from the apo structure alone.

    Normalised B-factor is the chain's own z-score, so it is comparable across arms that were
    refined at different resolutions. It is the crystallographic flexibility proxy, and C2
    permits it because it is a measured property of the deposited structure and not a
    simulated trajectory.
    """
    structure = apo.structure
    mask = structure.protein
    seq_id = np.asarray(structure.seq_id[mask])
    bfactor = np.asarray(structure.bfactor[mask], dtype=float)

    per_residue: dict[int, list[float]] = {}
    resname: dict[int, str] = {}
    for residue, name, value in zip(seq_id, structure.resname[mask], bfactor, strict=True):
        per_residue.setdefault(int(residue), []).append(float(value))
        resname[int(residue)] = str(name)
    mean_b = {residue: float(np.nanmean(values)) for residue, values in per_residue.items()}
    values = np.array(list(mean_b.values()))
    spread = float(np.nanstd(values))
    centre = float(np.nanmean(values))
    normalised = {
        residue: (value - centre) / spread if spread > 0 else 0.0
        for residue, value in mean_b.items()
    }
    return {
        "relative_solvent_accessibility": solvent_accessibility(apo),
        "normalised_b_factor": normalised,
        "hydrophobicity": {
            residue: KYTE_DOOLITTLE.get(name, 0.0) for residue, name in resname.items()
        },
    }
