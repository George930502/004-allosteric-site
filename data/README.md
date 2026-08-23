# Data

Nothing here is committed except this file and `.gitkeep` markers — every byte is
reproducibly re-fetchable or re-derivable, and PDB files are large.

- `raw/` — structures restored verbatim from the tracked `structures/` mirror or from
  RCSB PDB (rcsb.org). Never edited in place; a cleaned structure is a _derived_ artifact.
  **Partitioned, and the partition is a C1 boundary, not housekeeping:**
  - `raw/apo/` — written only by `allo.inputs.apo_input`. Apo entries only. This is the
    one cache reachable from the prediction path.
  - `raw/eval/` — written only by `allo.groundtruth.structures.fetch_mmcif`. Holds both
    halves of every pair, so it is holo-bearing by design.

  They were one directory until 2026-08-21. `make check` is offline and unmarked, so it
  restored all seven holo entries into the shared cache on every clone — and `parse_mmcif`
  is public and takes a path, so a prediction module could read the answer key without
  importing ground truth or naming a guarded file.
  `tests/test_no_leakage.py::test_the_prediction_cache_never_holds_a_holo_structure`
  holds the partition.

- `interim/` — intermediate parses, alignments, caches.
- `processed/` — contact networks, label sets, and other inputs to scoring.
- `external/` — third-party datasets (e.g. Allosteric Database exports) with their
  provenance recorded here when added.

Every derived artifact records the code version and config that produced it. If you
cannot say which config produced a file, delete it and regenerate.
