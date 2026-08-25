"""mmCIF fetch and parse.

Deliberately not Bio.PDB.Structure: we want author numbering, element symbols and
HETATM/ATOM provenance as flat arrays, because every downstream stage (contact
network, pocket labelling, coarse-graining) indexes residues rather than walking
an object tree. Reading the whole file into arrays once is also what makes the
benchmark freeze checkable — see docs/benchmark/README.md.
"""

from __future__ import annotations

import hashlib
import io
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from Bio.PDB.MMCIF2Dict import MMCIF2Dict


def fetch_mmcif(pdb_id: str, dest_dir: Path) -> Path:
    """Refuse free-form accession resolution on the prediction path.

    A method starts from :func:`allo.inputs.apo_input`, which binds the accession to a
    repository target and checks its hash. Accepting an arbitrary PDB id here let the same
    prediction-side module restore tracked holo coordinates without importing ground truth.
    Evaluation-side resolution lives in :mod:`allo.groundtruth.structures`.
    """
    del pdb_id, dest_dir
    raise PermissionError(
        "free-form structure resolution is unavailable; use allo.inputs.apo_input"
    )


def sha256(path: Path) -> str:
    """Hash of the file as downloaded — the thing a frozen benchmark actually pins."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


@dataclass(frozen=True)
class Structure:
    """First model of one mmCIF entry, as parallel per-atom arrays.

    `chain`/`seq_id` are *author* numbering: the units a medicinal chemist reads
    (AGENTS.md). `hetatm` marks non-polymer atoms, so ligands can be
    selected without a second parse.
    """

    pdb_id: str
    chain: np.ndarray
    seq_id: np.ndarray
    resname: np.ndarray
    atom: np.ndarray
    element: np.ndarray
    altloc: np.ndarray
    coord: np.ndarray
    # Crystallographic isotropic B. Kept because normalised B-factor is one of the four
    # confounders every propagation score is read against (ADR 0025). NaN where the entry
    # omits it, so a caller sees a missing value rather than a silent zero.
    bfactor: np.ndarray
    hetatm: np.ndarray
    in_polymer: np.ndarray

    def __len__(self) -> int:
        return len(self.seq_id)

    @property
    def _heavy(self) -> np.ndarray:
        return (self.element != "H") & (self.element != "D")

    @property
    def protein(self) -> np.ndarray:
        """Heavy atoms of polymer residues, *including* modified ones.

        Membership is decided by `label_seq_id`, not by the ATOM/HETATM flag.
        Modified residues in the chain — trimethyl-lysine, selenomethionine,
        phosphoserine — are deposited as HETATM but carry a polymer sequence number.
        Reading the flag instead would delete them from the chain, which silently
        changes residue counts, breaks the sequence alignment, and makes two entries
        of the same protein disagree about which residues exist.
        """
        return self.in_polymer & self._heavy

    @property
    def ligand(self) -> np.ndarray:
        """Heavy atoms of genuine non-polymer components, water excluded."""
        return ~self.in_polymer & (self.resname != "HOH") & self._heavy

    def residues(self, mask: np.ndarray | None = None) -> list[tuple[str, int, str]]:
        """Unique `(chain, author seq id, residue name)`, ordered by chain then number."""
        keep = self.protein if mask is None else mask
        seen = {
            (c, int(s)): n
            for c, s, n in zip(self.chain[keep], self.seq_id[keep], self.resname[keep], strict=True)
        }
        return [(c, s, seen[c, s]) for c, s in sorted(seen)]


def _column(data: dict, key: str) -> list[str]:
    value = data.get(key)
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


def _numeric(value: str) -> float:
    """mmCIF writes an absent value as `.` or `?`, which `float` cannot read."""
    try:
        return float(value)
    except ValueError:
        return float("nan")


def parse_mmcif_text(text: str, pdb_id: str) -> Structure:
    """Parse mmCIF text without opening a filesystem path.

    Prediction-safe shared code receives content only. Apo file opening is owned by
    :mod:`allo.inputs`; privileged evaluation file opening is owned by
    :mod:`allo.groundtruth.structures` (C1).
    """
    data = MMCIF2Dict(io.StringIO(text))
    model = np.array(_column(data, "_atom_site.pdbx_PDB_model_num"))
    first = model == model[0] if len(model) else np.zeros(0, dtype=bool)
    take = np.where(first)[0]
    coord = np.array(
        [[_column(data, f"_atom_site.Cartn_{axis}")[i] for axis in "xyz"] for i in take],
        dtype=float,
    )
    pick = lambda key: np.array([_column(data, key)[i] for i in take])  # noqa: E731

    # Insertion codes would make (chain, number) ambiguous and silently merge two
    # residues into one node. None of the frozen targets has any; refuse rather than
    # corrupt if one ever appears.
    icode = pick("_atom_site.pdbx_PDB_ins_code")
    present = sorted({c for c in icode.tolist() if c not in (".", "?", "")})
    if present:
        raise NotImplementedError(
            f"{pdb_id} uses insertion codes {present}; residue identity is not unique. "
            "Extend the residue key before using this entry."
        )

    label_seq = pick("_atom_site.label_seq_id")
    return Structure(
        pdb_id=pdb_id.upper(),
        chain=pick("_atom_site.auth_asym_id"),
        seq_id=pick("_atom_site.auth_seq_id").astype(int),
        resname=pick("_atom_site.auth_comp_id"),
        atom=pick("_atom_site.label_atom_id"),
        element=pick("_atom_site.type_symbol"),
        altloc=pick("_atom_site.label_alt_id"),
        coord=coord,
        bfactor=np.array(
            [_numeric(value) for value in pick("_atom_site.B_iso_or_equiv")], dtype=float
        )
        if _column(data, "_atom_site.B_iso_or_equiv")
        else np.full(len(take), np.nan),
        hetatm=pick("_atom_site.group_PDB") == "HETATM",
        in_polymer=~np.isin(label_seq, [".", "?", ""]),
    )


def contacts(
    structure: Structure,
    source: np.ndarray,
    target: np.ndarray,
    cutoff: float,
) -> list[tuple[str, int, str]]:
    """Residues in `target` with any atom within `cutoff` A of any atom in `source`.

    Heavy-atom minimum distance, which is the convention pocket definitions use;
    the cutoff is a knob because published values differ (docs/benchmark/README.md).
    """
    if not source.any() or not target.any():
        return []
    src = structure.coord[source]
    tgt = structure.coord[target]
    near = (np.linalg.norm(tgt[:, None, :] - src[None, :, :], axis=-1) <= cutoff).any(axis=1)
    hit = np.zeros(len(structure), dtype=bool)
    hit[np.where(target)[0][near]] = True
    return structure.residues(hit)
