# src/allo — package index

Read before adding or moving a module.

`src/allo/` is organised by pipeline stage, not by abstraction:

```
structure/    PDB fetch/parse -> coordinates, residue indexing
network/      contact graph / elastic network construction, coarse-graining
quantum/      Hamiltonians, propagation metrics, circuits, noise models
classical/    baselines (GNM/ANM, random walk, betweenness, perturbation response)
scoring/      ranking, enrichment statistics, decoy generation
groundtruth/  holo-derived labels ONLY — never imported by prediction code (C1)
viz/          2D plots and 3D structure rendering
cli.py        `allo <stage> ...` entry point
```

Add a module when a stage needs one, not before. No interface with one
implementation, no config knob for a value that never changes.

## Dependency direction

One invariant, and it is the code-level expression of hard constraint **C1**
(apo-only input) from the root `AGENTS.md`:

**`groundtruth/` is a sink. Nothing imports from it except scoring and reporting.**

Holo structures, ligand contacts and label sets enter the repo only through
`groundtruth/`. If `structure/`, `network/`, `quantum/`, `classical/` or anything else
on the prediction path imports it — directly or transitively — the blind prediction is
compromised and the submission is invalid. `tests/test_no_leakage.py` enforces this.

The general form: dependencies point inward toward the network/propagation logic, never
outward toward I/O, cloud backends or plotting. `quantum/` must be callable without
Braket credentials, `network/` without a PDB fetch. Pass the capability in.

## Conventions

- Residue identity is **author numbering plus chain ID**, preserved end to end. A hit
  list indexed by matrix row is not readable by a medicinal chemist and is not a
  deliverable (`docs/FIELD.md` — report in the units chemists use).
- Every stochastic function takes an explicit `seed`.
- Any function that returns a residue score returns it alongside the residue identity,
  never as a bare array whose ordering the caller must reconstruct.
