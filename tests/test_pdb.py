import numpy as np
import pytest

from allo.structure.pdb import Structure, contacts, parse_mmcif_text

MINIMAL_CIF = """\
data_TEST
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
ATOM 2 C CA . 2 . GLY A 2 4.000 0.000 0.000 1
ATOM 3 C CA . 3 . SER A 3 9.000 0.000 0.000 1
HETATM 4 O O1 . . . LIG A 99 1.000 0.000 0.000 1
HETATM 5 O O . . . HOH A 98 1.500 0.000 0.000 1
ATOM 6 C CA . 4 . TRP A 4 50.00 0.000 0.000 2
"""


@pytest.fixture
def structure() -> Structure:
    return parse_mmcif_text(MINIMAL_CIF, "TEST")


def test_parse_keeps_first_model_only(structure):
    assert "TRP" not in structure.resname
    assert len(structure) == 5


def test_protein_and_ligand_masks_exclude_water(structure):
    assert structure.residues(structure.protein) == [
        ("A", 1, "ALA"),
        ("A", 2, "GLY"),
        ("A", 3, "SER"),
    ]
    assert structure.residues(structure.ligand) == [("A", 99, "LIG")]


def test_contacts_are_heavy_atom_minimum_distance(structure):
    assert contacts(structure, structure.ligand, structure.protein, 4.5) == [
        ("A", 1, "ALA"),
        ("A", 2, "GLY"),
    ]
    assert contacts(structure, structure.ligand, structure.protein, 1.5) == [("A", 1, "ALA")]


def test_contacts_with_empty_selection_is_empty(structure):
    assert contacts(structure, np.zeros(len(structure), bool), structure.protein, 4.5) == []
