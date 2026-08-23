"""Prediction-safe structure parsing and selection. Knows nothing about ground truth (C1)."""

from allo.structure.pdb import Structure, contacts, parse_mmcif_text

__all__ = ["Structure", "contacts", "parse_mmcif_text"]
