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

## 3. Research principles

Standing instructions from the principal investigator. They govern *how* the research
is conducted, in the same way §2 governs what the result is allowed to be. They apply
to every task, not only to the ones that look scientific.

### R1 — First-principles thinking

Reason from the physics and the biology, not from what a similar repo did. Before
adopting any method, be able to state: what physical quantity it computes, what
assumption makes that quantity meaningful here, and what would make it break. If a
step exists only because it is conventional, it is not yet justified.

Practically: derive before you cite; when a paper's result is used, state the mechanism
in one sentence in your own terms. If you cannot, you do not yet understand it well
enough to build on it. "This is standard practice" is not a reason.

### R2 — Decompose into executable phases

Every unit of work reduces to phases with an **exit criterion that a command can
check**. Never start a task whose success condition is a feeling. If a task cannot be
decomposed that way, that is the finding — say so and reduce scope until it can be.

The project-level decomposition lives in `docs/ROADMAP.md`; the task-level version is
step 5 of `docs/playbooks/phase-work.md`. Both are load-bearing, not paperwork.

### R3 — Ground every claim in evidence

Four admissible kinds, in the order we prefer them when they conflict:

1. **Quantitative experimental results** produced in this repo, reproducible from a
   committed config (`experiments/`).
2. **Statistical analysis** of those results: effect size against a stated null model,
   with the test named. A ranking without a null is not evidence.
3. **Literature** with a DOI, read rather than recalled. Its claim is reported with its
   conditions — the protein class, the system size, the regime it was shown in.
4. **Observational / empirical** notes on structures and data — what the PDB file
   actually contains, what the network actually looks like. Recorded as observations,
   with the code path that produced them.

Not admissible as evidence: an LLM's recollection of a residue number, a plausible
mechanism nobody measured, or a number whose provenance cannot be named. When there is
no evidence yet, write "unknown" — an honest gap is cheaper than a confident guess that
someone later builds on.

### R4 — Work like a frontier researcher in this field

The field is defined explicitly in [`docs/FIELD.md`](docs/FIELD.md): protein allostery
and ensemble dynamics, elastic-network biophysics, and quantum transport on graphs,
applied to early-stage target validation. Read it before non-trivial work — it also
lists the known intellectual traps in this specific challenge, including the ones that
produce an impressive-looking but hollow submission.

Expert behaviour that is expected here: build the null model before the method; treat
the classical baselines as serious opponents rather than strawmen; distinguish pocket
from allosteric site from communication pathway; report in the units a medicinal
chemist uses; state the limits of a claim in the same breath as the claim.

Searching for best practice is encouraged — and it means finding what expert groups in
*these* fields actually do and why, then judging it, not copying the first tutorial
that runs. An adopted practice that cannot be justified under R1 is not adopted.

## 4. Required deliverables (what "done" means for the project)

Per target — KRAS G12C `4OBE`, BCR-ABL1 `1OPL`, cardiac myosin `5TBY`, c-Myc `1NKP`:

1. **N x N connectivity matrix** (`results/<target>/connectivity.npz`)
2. **Top-5 ranked allosteric residue hit list** (`results/<target>/hits.csv`)
3. Contribution to the **methodological report** (`docs/report/`)

Plus, project-wide: statistical enrichment vs. random and decoy residues, noise
resilience study, coarse-graining validation, 3D visualisations, classical-baseline
comparison, circuit-resource analysis.

---

## 5. Repo map

```
CHALLENGE.md            the spec — verbatim challenge statement
AGENTS.md / CLAUDE.md   this file
docs/FIELD.md           definition of the field, expert practice, known traps (R4)
docs/ROADMAP.md         phase plan; check current phase before starting work
docs/decisions/         ADRs — one file per irreversible or contested choice
docs/targets.md         validation targets, pockets, ground-truth policy
docs/playbooks/         shared procedures for both Claude Code and Codex
src/allo/               the package (see §5 for layout rules)
tests/                  fast by default; mark slow/network tests
experiments/            one dir per run: config + metrics + notes (§7)
results/<target>/       the scored deliverable artifacts
data/raw/               downloaded PDB files (gitignored, reproducible)
data/processed/         derived networks/labels (gitignored)
scripts/check.sh        the verification gate
```

## 6. Package layout rules

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

## 7. Working agreement

The mechanics that make §3 enforceable.

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

## 8. Experiment protocol

Any run that produces a number worth comparing goes through `experiments/`:

```
uv run allo new-experiment "ctqw time-averaged transfer"
# -> experiments/<date>-ctqw-time-averaged-transfer/{config.yaml,notes.md}
```

Fill `config.yaml` (all knobs, incl. seed), run it, write `metrics.json`, then add one
line to `experiments/REGISTRY.md`. The registry is the project's memory: an agent
starting fresh reads it to learn what has already been tried and what failed.

## 9. Context discipline for agents

- Start a task by reading: `docs/ROADMAP.md` (current phase) then
  `experiments/REGISTRY.md` (what has been tried). Both are short by design. Add
  `docs/FIELD.md` for anything methodological — it is where R1 and R4 get concrete.
- Prefer `rg`/`grep` over reading whole files. Never read `data/raw/*.pdb` into
  context — parse it with code and print a summary.
- The challenge PDF is 4.2 MB. Read `CHALLENGE.md` instead; it is complete.
- When you finish a phase, update `docs/ROADMAP.md` and write an ADR for any choice
  that would be expensive to reverse.

## 10. Environment

```
make setup      # uv sync --extra dev  -> .venv, Python >= 3.11
make check      # format + lint + fast tests
make test       # fast tests only
```

Cloud backends (AWS Braket, Classiq) are optional extras: `uv sync --extra hw`.
Credentials come from environment variables listed in `env.example` — never commit
secrets, never print them.

## 11. The harness

Shared playbooks live in `docs/playbooks/` so both tools follow the same procedure:

| Playbook | Claude Code | Codex |
|---|---|---|
| `phase-work.md` — start and finish a unit of phase work | `/phase <task>` | "follow the phase-work playbook" |
| `experiment.md` — run something that produces a comparable number | `/exp <question>` | "follow the experiment playbook" |
| `constraint-audit.md` — check a diff against C1–C6 | `/audit` or the `constraint-auditor` subagent | "run the constraint audit playbook" |
| handoff (section of `phase-work.md`) | `/handoff` | "do the handoff checklist" |

Claude Code additionally has a `PostToolUse` hook (`scripts/format-hook.sh`) that runs
`ruff format` on Python files as they are written, so the check gate never fails on
whitespace. Codex users get the same effect from `make fmt`.
