# 0014 — Pin versioned structure provenance and retain an offline mirror

**Status:** accepted · 2026-08-20 — option 1 is the provenance authority; partitioned bytes retained

## Correction of the accepted record

The previous accepted decision said wwPDB option 1 was unavailable. That claim was false: it
tested the wrong hosts and paths. `east.wwpdb.org` is a documentation endpoint, and
`files.wwpdb.org/pub/pdb_versioned/` is not the versioned archive. The live archive is
`https://files-versioned.wwpdb.org/pdb_versioned/`, mirrored by PDBe under
`https://ftp.ebi.ac.uk/pub/databases/pdb_versioned/`. This correction is substantive, not a
footnote, because the original decision rejected its own preferred option using invalid
evidence.

The pre-registered acceptance rule was: choose option 1 only if **every decompressed
versioned artifact matches the existing manifest hash**. That rule is met. All 15 pinned
entries match byte-for-byte:

- `1OPL` v1-4, `2G1T` v1-4, `2G2H` v1-4, `4LDJ` v1-3, `4OBE` v1-2;
- `5MO4` v1-2, `6OIM` v1-4, `8QYP` v1-0, `8QYR` v1-1, `8QYU` v1-0;
- `9F6C` v1-1, `9GZ2` v1-1, `9GZ3` v1-0, `9YR7` v1-1, `9YRG` v1-1.

`test_versioned_archive_reproduces_every_pinned_structure` re-fetches all 15 URLs,
decompresses them and checks the SHA-256 recorded in `manifest.yaml:structure_provenance`.
This converts the measured result into an executable R3 check.

## Decision

**Adopt option 1 as the provenance record.** The manifest pins the exact major/minor label,
canonical wwPDB versioned URL and decompressed SHA-256 for each entry contributing to the
freeze. Evaluation-side recovery prefers the local cache, then the tracked mirror, then the
pinned versioned URL. A current unversioned RCSB download is only a fallback for the two
excluded structures, which do not contribute to `frozen.json`.

**Retain the committed bytes as an offline reproduction mirror.** The versioned archive now
provides independent provenance, but remote availability is not the same property as offline
reproduction. The 17 deterministic `.cif.gz` files total 5,465,227 bytes (5.21 MiB), small
enough that removing them would trade a working offline gate for negligible repository
savings. This is evidence-based redundancy: archive URLs establish origin; tracked bytes
make `make check` and `allo benchmark verify` independent of network state.

## C1 partition

The mirror is partitioned by role:

- `structures/apo/` contains the nine apo-side entries;
- `structures/holo/` contains the eight holo-side entries, including the excluded `6C1H`.

Free-form accession resolution no longer exists on the prediction path. A method receives a
target-bound, hash-checked apo structure only through `allo.inputs.apo_input`; holo-capable
resolution lives behind `allo.groundtruth.structures`. The regression tries all reported holo
accessions and requires prediction-side resolution to refuse them.

## Consequences

- The freeze has two independent recovery routes: pinned wwPDB versions and tracked bytes.
- Hashes remain over decompressed mmCIF bytes, independent of gzip serialization.
- The store also retains `5TBY` and `6C1H`, so the evidence for the excluded mandated arm is
  reproducible even though those files contribute no frozen target.
- Adding or revising a scoreable entry requires a manifest version label, URL and hash, a
  partitioned offline artifact, archive verification, and a deliberate re-freeze.
