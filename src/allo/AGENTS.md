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

**Two data routes bypass the import graph, and both are guarded separately.**
`docs/benchmark/frozen.json` holds the label sets, and no prediction-path module may name
it. `docs/benchmark/manifest.yaml` holds the holo accessions, the effector component IDs
and — in `blind.why`, `defect` and `note` — label residue numbers written out in prose.
`allo.inputs` is the **only** prediction-path module permitted to open it, and its `load()`
strips every holo-side field by allow-list, so a field added later is redacted by default.
The unredacted read is `allo.groundtruth.manifest.read_manifest`, so the import guard covers
it like any other holo data. It used to sit on `allo.inputs` beside `load()`, and every guard
stayed green for a prediction module that imported it: the import trace only watches
`groundtruth`, and the file-read test greps for `manifest.yaml`/`MANIFEST`, neither of which
appears in `from allo.inputs import read_manifest`. Found by adversarial review, closed by
moving the function rather than by adding a special case. **`allo.inputs` must never regain a
verbatim reader** — `test_no_prediction_module_can_reach_an_unredacted_manifest` holds it.

An import trace cannot see the `frozen.json` route; the file-read and content tests in
`tests/test_no_leakage.py` are what does.

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
