# AGENTS.md — operating contract for coding agents

Read this before touching anything. It is the single source of truth for both
Claude Code and Codex (`CLAUDE.md` is a symlink to this file).

---

## 1. What this repo is

A research codebase for the **Global Quantum + AI Challenge 2026 — Cleveland Clinic**
statement: *"Unlocking undruggable targets: quantum simulation of allosteric signal
propagation."*

We take an **apo** protein structure, build a residue-level elastic/contact network,
simulate **quantum** signal propagation on that network, and rank residues by dynamic
connectivity to the active site. High-ranking distal residues are the predicted
allosteric sites.

Full challenge text: `CHALLENGE.md` (verbatim restatement of the official PDF).
Read it once at the start of any non-trivial task. It is the spec.

---

## 2. Hard constraints — violating any of these invalidates the submission

These come from the challenge statement, not from us. Never trade them away for
convenience, and flag it loudly if a task appears to require breaking one.

| # | Rule |
|---|------|
| C1 | **Apo input only.** Holo structures are used *exclusively* to build ground-truth labels for scoring. No holo-derived information may enter the prediction path — not coordinates, not pocket residues, not even the residue count. |
| C2 | **No classical MD trajectories as input.** Dynamics must be predicted *ab initio* from topology. No GROMACS/AMBER/OpenMM trajectories, no MD-derived covariance matrices, no MD-trained ML weights in the prediction path. |
| C3 | **Near-term hardware viability.** Circuit depth, qubit count, and connectivity must be reported for every quantum method. Deep unoptimised circuits are explicitly penalised. Every quantum claim needs a stated resource cost. |
| C4 | **Credible quantum execution path.** Gate-based, quantum-inspired, and hybrid are all allowed, but a quantum-inspired method must state how it maps to hardware. |
| C5 | **Scope:** catalytic domains only. Waters, co-factors and PTMs excluded unless modelled as simple nodes. |
| C6 | **Elastic network hypothesis** is the modelling assumption: contact topology drives propagation; atomic force fields are abstracted away. |

Leakage from C1 is the easiest mistake to make and the hardest to notice. Any code
that loads a holo PDB lives under `src/allo/groundtruth/` and is never imported by
prediction code. Enforced by a test (`tests/test_no_leakage.py`, added in Phase 1).

---

## 3. Required deliverables (what "done" means for the project)

Per target — KRAS G12C `4OBE`, BCR-ABL1 `1OPL`, cardiac myosin `5TBY`, c-Myc `1NKP`:

1. **N x N connectivity matrix** (`results/<target>/connectivity.npz`)
2. **Top-5 ranked allosteric residue hit list** (`results/<target>/hits.csv`)
3. Contribution to the **methodological report** (`docs/report/`)

Plus, project-wide: statistical enrichment vs. random and decoy residues, noise
resilience study, coarse-graining validation, 3D visualisations, classical-baseline
comparison, circuit-resource analysis.

---

## 4. Repo map

```
CHALLENGE.md            the spec — verbatim challenge statement
AGENTS.md / CLAUDE.md   this file
docs/ROADMAP.md         phase plan; check current phase before starting work
docs/decisions/         ADRs — one file per irreversible or contested choice
docs/targets.md         validation targets, pockets, ground-truth policy
src/allo/               the package (see §5 for layout rules)
tests/                  fast by default; mark slow/network tests
experiments/            one dir per run: config + metrics + notes (§7)
results/<target>/       the scored deliverable artifacts
data/raw/               downloaded PDB files (gitignored, reproducible)
data/processed/         derived networks/labels (gitignored)
scripts/check.sh        the verification gate
```

## 5. Package layout rules

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

## 6. Working agreement

- **Run `make check` before reporting any task complete.** It is fast, offline, and
  is the same gate CI runs. "It should work" is not a status.
- **State assumptions up front.** If two readings of a task give materially different
  work, ask before building.
- **Surgical diffs.** Every changed line traces to the request. Don't reformat or
  "improve" adjacent code.
- **Determinism.** Every stochastic step takes an explicit `seed`. Default seed `0`.
  A rerun of a committed experiment must reproduce its metrics bit-for-bit on the
  same machine, or the config is incomplete.
- **Numbers come from code, never from memory.** Residue indices, pocket definitions,
  PDB chain IDs and literature values are derived programmatically or cited to a
  source in `docs/`. Do not hand-type a residue list you "know".
- **Cite when you claim.** Any biological or algorithmic claim in docs carries a DOI
  or a `CHALLENGE.md` reference number.
- **Negative results are results.** A method that underperforms gets written up in
  its experiment notes, not deleted.

## 7. Experiment protocol

Any run that produces a number worth comparing goes through `experiments/`:

```
uv run allo new-experiment "ctqw time-averaged transfer"
# -> experiments/<date>-ctqw-time-averaged-transfer/{config.yaml,notes.md}
```

Fill `config.yaml` (all knobs, incl. seed), run it, write `metrics.json`, then add one
line to `experiments/REGISTRY.md`. The registry is the project's memory: an agent
starting fresh reads it to learn what has already been tried and what failed.

## 8. Context discipline for agents

- Start a task by reading: `docs/ROADMAP.md` (current phase) then
  `experiments/REGISTRY.md` (what has been tried). Both are short by design.
- Prefer `rg`/`grep` over reading whole files. Never read `data/raw/*.pdb` into
  context — parse it with code and print a summary.
- The challenge PDF is 4.2 MB. Read `CHALLENGE.md` instead; it is complete.
- When you finish a phase, update `docs/ROADMAP.md` and write an ADR for any choice
  that would be expensive to reverse.

## 9. Environment

```
make setup      # uv sync --extra dev  -> .venv, Python >= 3.11
make check      # format + lint + fast tests
make test       # fast tests only
```

Cloud backends (AWS Braket, Classiq) are optional extras: `uv sync --extra hw`.
Credentials come from environment variables listed in `env.example` — never commit
secrets, never print them.
