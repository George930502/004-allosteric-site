import pytest

from allo.groundtruth.labels import align_numbering, pocket_residues, transfer_labels
from allo.structure.pdb import parse_mmcif_text

# Two tiny entries of the same three-residue protein under different author
# numbering, with a ligand touching the middle residue in the "holo" one. The
# numbering offset of 100 is the ABL1 1a/1b hazard in miniature.
APO = """\
data_APO
loop_
_atom_site.group_PDB
_atom_site.id
_atom_site.type_symbol
_atom_site.label_atom_id
_atom_site.label_alt_id
_atom_site.label_seq_id
_atom_site.pdbx_PDB_ins_code
_atom_site.auth_comp_id
_atom_site.auth_asym_id
_atom_site.auth_seq_id
_atom_site.Cartn_x
_atom_site.Cartn_y
_atom_site.Cartn_z
_atom_site.pdbx_PDB_model_num
ATOM 1 C CA . 1 . ALA A 1 0.000 0.000 0.000 1
ATOM 2 C CA . 2 . TRP A 2 6.000 0.000 0.000 1
ATOM 3 C CA . 3 . SER A 3 12.00 0.000 0.000 1
"""
HOLO = """\
data_HOLO
loop_
_atom_site.group_PDB
_atom_site.id
_atom_site.type_symbol
_atom_site.label_atom_id
_atom_site.label_alt_id
_atom_site.label_seq_id
_atom_site.pdbx_PDB_ins_code
_atom_site.auth_comp_id
_atom_site.auth_asym_id
_atom_site.auth_seq_id
_atom_site.Cartn_x
_atom_site.Cartn_y
_atom_site.Cartn_z
_atom_site.pdbx_PDB_model_num
ATOM 1 C CA . 101 . ALA B 101 0.000 0.000 0.000 1
ATOM 2 C CA . 102 . TRP B 102 6.000 0.000 0.000 1
ATOM 3 C CA . 103 . SER B 103 12.00 0.000 0.000 1
HETATM 4 C C1 . . . DRG B 201 6.000 2.000 0.000 1
"""


@pytest.fixture
def pair():
    return parse_mmcif_text(APO, "APO"), parse_mmcif_text(HOLO, "HOLO")


def test_pocket_residues_uses_the_cutoff(pair):
    _, holo = pair
    assert pocket_residues(holo, "DRG", 4.5) == [("B", 102, "TRP")]
    assert pocket_residues(holo, "DRG", 1.0) == []


def test_missing_ligand_is_an_error_not_an_empty_label_set(pair):
    _, holo = pair
    with pytest.raises(ValueError, match="ABSENT"):
        pocket_residues(holo, "ABSENT")


def test_align_numbering_recovers_the_offset(pair):
    apo, holo = pair
    assert align_numbering(holo, apo, "B", "A") == {101: 1, 102: 2, 103: 3}


def test_transfer_labels_reports_in_apo_numbering(pair):
    apo, holo = pair
    labels = transfer_labels(holo, apo, "DRG", holo_chain="B", apo_chain="A")
    assert labels.apo_residues == [("A", 2, "TRP")]
    assert labels.holo_residues == [("B", 102, "TRP")]
    assert labels.unmapped == []
