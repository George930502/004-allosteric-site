# 0004 — Residue identity, numbering conventions, and label transfer by alignment

**Status:** accepted · 2026-08-20

## Context

Ground-truth labels are pocket residues observed in a holo entry, scored against
predictions made on an apo entry. That only works if "the same residue" is well defined
across two files — and it frequently is not:

- **ABL1** is deposited under two numbering conventions. `1OPL` and `5MO4` both use isoform
  1b, but `1M52`, `2G1T`, `2HYY` and `4WA9` use 1a, which is 19 lower for the same residue.
- **`1OPL`'s own `_struct_ref_seq` record is wrong.** It claims author numbering equals
  UniProt P00519 numbering; SIFTS shows a +19 offset. Normalising through the deposited
  record would shift every label by 19 and quietly destroy the ground truth.
- **`1NKP`** gives its two Myc copies arbitrary and *different* offsets (chains A and D,
  auth 897–984 and 499–581, both UniProt 353–434).
- Constructs differ: expression tags at negative numbers, cloning artefacts, chimeric
  fusions, residues modelled in one entry and disordered in the other.

## Decision

1. **Residue identity is `(author chain, author residue number)` of the entry it came
   from.** It is the unit a medicinal chemist reads and the unit hit lists are reported in.
2. **Correspondence between two entries is derived by aligning their modelled sequences**
   (`allo.groundtruth.labels.align_numbering`), never by assuming author numbers match and
   never by routing through UniProt. Alignment is robust to both the isoform split and the
   wrong `_struct_ref_seq` record; UniProt normalisation is robust to neither.
3. **Labels that do not map are reported, not dropped.** `Labels.unmapped` names them. A
   residue disordered in the apo model has no coordinates and cannot be scored; hiding that
   would inflate every metric.
4. **The pocket is the set of protein residues with any heavy atom within 4.5 Å of any
   heavy atom of the named ligand**, identified by chemical component ID read from the file.
   4.0 Å and 5.0 Å are run as a reported sensitivity, never as a selection criterion.
5. **Any geometric comparison between two entries is fitted through the same alignment**,
   and locally — on the shell within 20 Å of the pocket centroid, excluding the pocket
   itself. A whole-chain fit on a multi-domain protein is dominated by inter-domain motion;
   on the myosin interacting-heads pair a global fit gave 8.5 Å RMSD and manufactured a
   clash that the local fit shows does not exist.

## Consequences

- Adding a target never requires hand-checking a numbering convention; the failure mode
  becomes a visible `unmapped` list instead of a silent shift.
- Alignment cost is negligible at these sizes and is done once per pair at freeze time.
- Limitation: alignment assumes the two entries are the same protein. It will happily align
  39 %-identical sequences and return nonsense, which is exactly what the mandated cardiac
  myosin pair would produce. Sequence identity is therefore recorded per pair in the audit,
  and a pair below a sane threshold is excluded rather than mapped (ADR 0003).
