"""Derive allosteric-site labels from a holo structure and carry them onto the apo.

Two steps, kept separate because they fail differently:

1. `pocket_residues` — which holo residues line the bound ligand. A geometric
   fact about one file.
2. `align_numbering` / `transfer_labels` — which apo residue is the same physical
   residue. Author numbering is *not* a reliable key across entries: the same
   protein is deposited under different isoform conventions (ABL1 1a vs 1b differ
   by 19), so the mapping is derived by aligning the modelled sequences and
   unmapped labels are reported rather than silently dropped.
"""

from __future__ import annotations

from dataclasses import dataclass

from Bio.Align import PairwiseAligner, substitution_matrices

from allo.inputs import one_letter
from allo.structure.pdb import Structure

Residue = tuple[str, int, str]


def pocket_residues(
    holo: Structure, ligand_comp: str, cutoff: float = 4.5, chain: str | None = None
) -> list[Residue]:
    """Protein residues with a heavy atom within `cutoff` A of `ligand_comp`.

    `chain` scopes which *copy* of the ligand defines the pocket. Without it, an entry
    holding the same drug in two chains defines one pocket from both copies, and a
    residue near the other protomer's ligand is labelled across the interface. No
    frozen target is affected today (checked); a homodimer in the ASD set would be.
    """
    from allo.structure.pdb import contacts

    ligand = holo.ligand & (holo.resname == ligand_comp)
    if chain is not None:
        ligand = ligand & (holo.chain == chain)
    if not ligand.any():
        where = f" in chain {chain}" if chain else ""
        raise ValueError(f"{holo.pdb_id} contains no component {ligand_comp!r}{where}")
    return contacts(holo, ligand, holo.protein, cutoff)


def _aligner() -> PairwiseAligner:
    aligner = PairwiseAligner(mode="global")
    aligner.substitution_matrix = substitution_matrices.load("BLOSUM62")
    aligner.open_gap_score = -11
    aligner.extend_gap_score = -1
    return aligner


def align_numbering(
    holo: Structure, apo: Structure, holo_chain: str, apo_chain: str
) -> dict[int, int]:
    """Map holo author numbering -> apo author numbering for one chain each.

    Aligns the *modelled* residues of both chains, so a residue absent from either
    model simply has no entry — which is the honest answer, since an unmodelled
    residue has no coordinates to score against.
    """
    holo_res = [r for r in holo.residues() if r[0] == holo_chain]
    apo_res = [r for r in apo.residues() if r[0] == apo_chain]
    alignment = _aligner().align(one_letter(holo_res), one_letter(apo_res))[0]
    mapping: dict[int, int] = {}
    for (h0, h1), (a0, _) in zip(*alignment.aligned, strict=True):
        for step in range(h1 - h0):
            mapping[holo_res[h0 + step][1]] = apo_res[a0 + step][1]
    return mapping


@dataclass(frozen=True)
class Labels:
    """A label set is only interpretable together with how it was made."""

    apo_residues: list[Residue]
    holo_residues: list[Residue]
    unmapped: list[Residue]
    ligand_comp: str
    cutoff: float
    apo_chain: str
    holo_chain: str


def transfer_labels(
    holo: Structure,
    apo: Structure,
    ligand_comp: str,
    holo_chain: str,
    apo_chain: str,
    cutoff: float = 4.5,
) -> Labels:
    """Pocket residues of `ligand_comp` in the holo entry, in apo author numbering."""
    pocket = [
        r for r in pocket_residues(holo, ligand_comp, cutoff, holo_chain) if r[0] == holo_chain
    ]
    mapping = align_numbering(holo, apo, holo_chain, apo_chain)
    by_number = {number: name for chain, number, name in apo.residues() if chain == apo_chain}
    mapped, unmapped = [], []
    for residue in pocket:
        apo_number = mapping.get(residue[1])
        if apo_number is None:
            unmapped.append(residue)
        else:
            mapped.append((apo_chain, apo_number, by_number[apo_number]))
    return Labels(
        apo_residues=sorted(mapped, key=lambda r: r[1]),
        holo_residues=pocket,
        unmapped=unmapped,
        ligand_comp=ligand_comp,
        cutoff=cutoff,
        apo_chain=apo_chain,
        holo_chain=holo_chain,
    )
