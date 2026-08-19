"""Structure ingest: fetch, parse, select. Knows nothing about ground truth (C1)."""

from allo.structure.pdb import Structure, contacts, fetch_mmcif, parse_mmcif

__all__ = ["Structure", "contacts", "fetch_mmcif", "parse_mmcif"]
