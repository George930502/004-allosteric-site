"""The manifest with its holo half intact. A sink, for the same reason labels are.

`manifest.yaml` is not an index of apo entries. It names every holo accession and
effector component ID, and three of its prose fields spell out label residues outright:
`blind.why` names KRAS 68/95/96/99, `defect` says myristate contacts "16 of the 20"
labels, and Site 2's `note` gives the whole label-to-active-site distribution. Reading it
verbatim is reading the answer key.

This used to live in `allo.inputs` as a public `read_manifest`, one import away from
every prediction module, and no guard caught it: the import-graph test only watches
`allo.groundtruth`, and the file-read test greps for `manifest.yaml`/`MANIFEST` — neither
string appears in `from allo.inputs import read_manifest`. Moving it here does not add a
special case; it puts the function behind the guard that already exists, so a prediction
module that reaches for it fails `test_prediction_path_never_reaches_ground_truth`.

The redacted view a method is allowed is `allo.inputs.load`.
"""

from __future__ import annotations

from pathlib import Path

import yaml

from allo.inputs import MANIFEST


def read_manifest(path: Path = MANIFEST) -> dict:
    """The manifest verbatim, holo half included. Evaluation path only."""
    return yaml.safe_load(path.read_text())
