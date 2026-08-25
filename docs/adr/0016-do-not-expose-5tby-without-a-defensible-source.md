# 0016 — Do not expose 5TBY as a propagation input without a defensible source

**Status:** accepted · 2026-08-21

## Context

`CHALLENGE.md` Table 1 mandates `5TBY` as the cardiac-myosin input, independently of
whether the assigned `6C1H` validation structure can be scored. The current manifest arm is
`status: excluded`. That status must not decide which apo inputs a method receives: an
invalid holo label set is not, by itself, a reason to delete a mandated apo input.

The repository artifacts establish two separate input-side blockers. Decompressing the
tracked `structures/apo/5TBY.cif.gz` and parsing it with
the evaluation-side `allo.groundtruth.structures.parse_mmcif` yields 954 modelled residues on chain A and zero
heteroatoms. Accordingly, the manifest rule
`active_site: {from_ligands: []}` has no ligand from which `allo.inputs.active_site()` can
derive a propagation source. `docs/benchmark/primary/frozen.json` contains no
`cardiac_myosin_mandated` record, so neither a node set nor a source is currently
frozen for prediction.

The coordinate file itself reports electron microscopy at 20 Å, and its deposited title and
Alamo et al. identify it as a SWISS-MODEL homology model built on tarantula `3JBH` and
rigid-body fitted to the low-resolution envelope (doi:10.7554/eLife.24634; evidence review in
`docs/benchmark/evidence/claim-verification.md` §C3). At that resolution the residue-level
side-chain contacts are properties of the modelling and fitting protocol, not measured
contact topology. Treating them as the elastic network would therefore make C6's topology
hypothesis rest on invented residue contacts.

## Decision

Choose option (b): **do not expose `5TBY` through the frozen prediction interface now.** Its
labels and scoring remain unavailable because `6C1H` is the wrong protein and contains no
mavacamten, but that is not the input-side reason. The input remains unavailable because no
apo-derived propagation source exists under the accepted general rules in ADR 0005, and the
20 Å homology model cannot defensibly supply residue-level contact topology under C6.

Do not repair the missing source with a written residue list or a myosin-only motif added for
this arm. The former violates ADR 0005's derived-rule requirement; the latter would be a
per-arm modelling choice introduced only to force a mandated accession through the
interface. No such rule has been independently specified or validated in this repository.

## Consequences

- `cardiac_myosin_mandated` remains absent from `allo.inputs.load()` and
  `docs/benchmark/primary/frozen.json`. This is explicitly option (b), an unmet input requirement,
  not a completed repair. The manifest records the independent apo-admission decision as
  `prediction_status: blocked` and pins the tracked 5TBY bytes; `load()` no longer consults
  evaluation `status` when admitting inputs.
- Phase 2 is blocked while a challenge-mandated input cannot produce its required matrix and
  hit list. The cost is delayed method selection rather than a source chosen after seeing the
  target-specific problem.
- Exposure may be reconsidered if the organisers supply an experimental apo cardiac-myosin
  structure with a catalytic cofactor, or if the project pre-registers and independently
  validates a fold-general apo-sequence rule for myosin catalytic sources **and** supplies
  experimental coordinates adequate for residue-contact topology.
- An organiser-supplied correct holo structure would make labels scoreable but would not, by
  itself, cure the two input-side blockers above.
