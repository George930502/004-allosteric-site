# AGENTS.md — operating contract for agents

Root index for both Claude Code and Codex (`CLAUDE.md` is a symlink to this file).
It is always in context, so it holds only what is needed **every** session; everything
else is one hop away and named below with the condition for opening it.

---

## What this repo is

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

## Hard constraints — violating any of these invalidates the submission

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
prediction code. Enforced by `tests/test_no_leakage.py` (added in Phase 1).

---

## Research principles

Standing instructions from the principal investigator. They govern *how* the research
is conducted, in the same way the constraints govern what the result may be.

- **R1 — First principles.** Reason from the physics and the biology, not from what a
  similar repo did. State what a method computes and what assumption makes it
  meaningful here. "It is standard practice" is not a reason.
- **R2 — Executable phases.** Every unit of work has an exit criterion a command can
  check. Never start a task whose success condition is a feeling.
- **R3 — Evidence.** Claims rest on repo experiments, statistics with a stated null,
  literature with a DOI, or recorded observation — in that order of preference. A
  recalled number is not evidence. Where evidence is absent, write "unknown".
- **R4 — Frontier expertise.** Work as an expert in this field would. Search for best
  practice, then judge it against R1 rather than copying it.

Full statements: `docs/PRINCIPLES.md`. What "this field" means, and the traps that
produce a confident but hollow submission: `docs/FIELD.md`. Enforcement checkpoints
`[R1]`–`[R4]` are marked inline in `docs/playbooks/phase-work.md`.

---

## Required deliverables (what "done" means for the project)

Per target — KRAS G12C `4OBE`, BCR-ABL1 `1OPL`, cardiac myosin `5TBY`, c-Myc `1NKP`:

1. **N x N connectivity matrix** (`results/<target>/connectivity.npz`)
2. **Top-5 ranked allosteric residue hit list** (`results/<target>/hits.csv`)
3. Contribution to the **methodological report** (`docs/report/`)

Plus, project-wide: statistical enrichment vs. random and decoy residues, noise
resilience study, coarse-graining validation, 3D visualisations, classical-baseline
comparison, circuit-resource analysis.

---

## Where things are, and when to open them

Start every task with the first two rows. The rest are on-demand — open one when its
condition fires, not to browse.

| Open this | When |
|---|---|
| `docs/ROADMAP.md` | Always, first. Which phase is current and what its exit criterion is |
| `experiments/REGISTRY.md` | Always, second. What has been tried, and what failed — do not re-run a dead end |
| `docs/playbooks/phase-work.md` | Starting or finishing any unit of work. `/phase` in Claude Code |
| `docs/playbooks/experiment.md` | About to produce a number worth comparing to another number. `/exp` |
| `docs/playbooks/constraint-audit.md` | Diff touches the prediction path, ground truth, or a quantum method. `/audit`, or the `constraint-auditor` subagent |
| `docs/FIELD.md` | Choosing or defending a method; writing anything for the report |
| `docs/PRINCIPLES.md` | The one-liners above are not enough to settle a call |
| `docs/targets.md` | Touching a specific protein, its chains, or its ground-truth labels |
| `docs/adr/` | Before choosing between credible alternatives; write one when the choice would be expensive to reverse. `README.md` there gives the format |
| `src/allo/AGENTS.md` | Adding or moving a module — package layout and the dependency rule that enforces C1 |
| `experiments/README.md` | Setting up a run directory |
| `docs/agents/` | An installed engineering skill needs the issue tracker, triage labels, or domain-doc layout |
| `CHALLENGE.md` | Any question about what the challenge actually requires. It is the spec; do not answer from memory |

Not in context and not worth loading: `Cleveland-Clinic-Challenge-Statement-vF.pdf`
(4.2 MB — `CHALLENGE.md` is the complete restatement), and anything under `data/raw/`
(parse it with code and print a summary; never read a PDB into context).

---

## Working agreement

The mechanics that make the principles enforceable.

- **Run `make check` before reporting any task complete.** Fast, offline, the same gate
  CI runs. "It should work" is not a status.
- **State assumptions up front.** If two readings of a task give materially different
  work, ask before building.
- **Surgical diffs.** Every changed line traces to the request. Don't reformat or
  "improve" adjacent code.
- **Determinism.** Every stochastic step takes an explicit `seed`, default `0`. A rerun
  of a committed experiment must reproduce its metrics bit-for-bit, or the config is
  incomplete.
- **Numbers come from code, never from memory.** Residue indices, pocket definitions,
  PDB chain IDs and literature values are derived programmatically or cited to a source
  in `docs/`. Do not hand-type a residue list you "know".
- **Cite when you claim.** Any biological or algorithmic claim in docs carries a DOI or
  a `CHALLENGE.md` reference number.
- **Negative results are results.** A method that underperforms is written up in its
  experiment notes, not deleted.
- **Leave the memory updated.** A new comparable number → `experiments/REGISTRY.md`. A
  decision that constrains later phases → an ADR. A phase closed → `docs/ROADMAP.md`.

---

## Environment

`make setup` once, `make check` before every handoff. Targets are defined in the
`Makefile` — read it rather than trusting a copy here. Python ≥ 3.11 via `uv`; cloud
backends are the optional `hw` extra. Credentials come from the environment variables
listed in `env.example`; never commit or print them.

---

## Agent skills

Per-repo configuration the installed engineering skills read.

### Issue tracker

GitHub Issues on `George930502/004-allosteric-site` via `gh`; external PRs are not a
request surface. See `docs/agents/issue-tracker.md`.

### Triage labels

The five canonical roles, label strings equal to their names. See
`docs/agents/triage-labels.md`.

### Domain docs

Single-context; `docs/adr/` is the decision record. See `docs/agents/domain.md`.
