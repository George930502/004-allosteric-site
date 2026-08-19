# Data

Nothing here is committed except this file and `.gitkeep` markers — every byte is
reproducibly re-fetchable or re-derivable, and PDB files are large.

- `raw/` — structures downloaded verbatim from RCSB PDB (rcsb.org). Never edited in
  place; a cleaned structure is a *derived* artifact.
- `interim/` — intermediate parses, alignments, caches.
- `processed/` — contact networks, label sets, and other inputs to scoring.
- `external/` — third-party datasets (e.g. Allosteric Database exports) with their
  provenance recorded here when added.

Every derived artifact records the code version and config that produced it. If you
cannot say which config produced a file, delete it and regenerate.
