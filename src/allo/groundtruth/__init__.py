"""Holo-derived labels. A sink: nothing on the prediction path may import this (C1).

See src/allo/AGENTS.md for the dependency rule and tests/test_no_leakage.py for
its enforcement.
"""

from allo.groundtruth.labels import align_numbering, pocket_residues, transfer_labels
from allo.groundtruth.manifest import read_manifest

__all__ = ["align_numbering", "pocket_residues", "read_manifest", "transfer_labels"]
