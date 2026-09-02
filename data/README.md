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
  - `external/asd/` — the **Allosteric Database** 2023 bulk release, all 12 archives, fetched
    2026-09-01T20:58Z from `http://mdl.shsmu.edu.cn/ASD2023Common/static_file/archive_2023/`.
    Release 5.1, newest file dated 2023-09-20. Per-file sizes and sha256 are in
    `docs/benchmark/review/data/extension-candidates-2026-09.json` under `_asd_provenance`, and
    the retrieval recipe is in `docs/benchmark/review/09-extension-sweep.md` §1.3.
    **Licence: research use only, and ASD forbids redistribution to a third party.** Never
    commit a verbatim ASD file. A derived candidate list — names, accessions, DOIs — is fine.
    ASD is a **recall device only**: its evidence bar sits on the protein, not the site, and its
    2023 release mixes 3102 curated sites with 66,589 machine-predicted ones (ADR 0021).

Every derived artifact records the code version and config that produced it. If you
cannot say which config produced a file, delete it and regenerate.
