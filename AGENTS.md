# AGENTS.md — operating contract for agents

Root index for both Claude Code and Codex (`CLAUDE.md` is a symlink to this file).
It is always in context, so it holds only what is needed **every** session; everything
else is one hop away and named below with the condition for opening it.

---

## What this repo is

A research codebase for the **Global Quantum + AI Challenge 2026 — Cleveland Clinic**
statement: _"Unlocking undruggable targets: quantum simulation of allosteric signal
propagation."_

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

| #   | Rule                                                                                                                                                                                                                               |
| --- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| C1  | **Apo input only.** Holo structures are used _exclusively_ to build ground-truth labels for scoring. No holo-derived information may enter the prediction path — not coordinates, not pocket residues, not even the residue count. |
| C2  | **No classical MD trajectories as input.** Dynamics must be predicted _ab initio_ from topology. No GROMACS/AMBER/OpenMM trajectories, no MD-derived covariance matrices, no MD-trained ML weights in the prediction path.         |
| C3  | **Near-term hardware viability.** Circuit depth, qubit count, and connectivity must be reported for every quantum method. Deep unoptimised circuits are explicitly penalised. Every quantum claim needs a stated resource cost.    |
| C4  | **Credible quantum execution path.** Gate-based, quantum-inspired, and hybrid are all allowed, but a quantum-inspired method must state how it maps to hardware.                                                                   |
| C5  | **Scope:** catalytic domains only. Waters, co-factors and PTMs excluded unless modelled as simple nodes. Read as scoping the _system_, not as trimming a chain — the node set is every modelled residue of the frozen chain (ADR 0010, accepted).                                                                                                                           |
| C6  | **Elastic network hypothesis** is the modelling assumption: contact topology drives propagation; atomic force fields are abstracted away.                                                                                          |

Leakage from C1 is the easiest mistake to make and the hardest to notice. Any code
that loads a holo PDB lives under `src/allo/groundtruth/` and is never imported by
prediction code. Enforced by `tests/test_no_leakage.py` (added in Phase 1).

---

## Research principles

Standing instructions from the principal investigator. They govern _how_ the research
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

Per target — KRAS G12C `4OBE`, BCR-ABL1 `1OPL`, cardiac myosin `5TBY`, c-Myc `1NKP`.
All three mandated apo/holo pairs are defective and are scored in tiers; the cardiac
myosin pair is unscoreable as assigned. See `docs/benchmark/README.md` before using any
of these accessions:

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

| Open this                            | When                                                                                                                                                                                  |
| ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `docs/ROADMAP.md`                    | Always, first. Which phase is current and what its exit criterion is                                                                                                                  |
| `experiments/REGISTRY.md`            | Always, second. What has been tried, and what failed — do not re-run a dead end                                                                                                       |
| `CONTEXT.md`                         | Writing the word "site", "pocket", "target" or "pair" anywhere. The settled vocabulary — cryptic and allosteric are **not** synonyms and the difference decides what we are scored on |
| `docs/playbooks/phase-work.md`       | Starting or finishing any unit of work. `/phase` in Claude Code                                                                                                                       |
| `docs/playbooks/experiment.md`       | About to produce a number worth comparing to another number. `/exp`                                                                                                                   |
| `docs/playbooks/constraint-audit.md` | Diff touches the prediction path, ground truth, or a quantum method. `/audit`, or the `constraint-auditor` subagent                                                                   |
| `docs/FIELD.md`                      | Choosing or defending a method; writing anything for the report                                                                                                                       |
| `docs/PRINCIPLES.md`                 | The one-liners above are not enough to settle a call                                                                                                                                  |
| `docs/benchmark/README.md`           | Any question about **what** a method receives and **what** it is scored against. `frozen.json` is the authority for every residue count, label set and active site — never quote one from prose. `n_residues` is what a method **receives**; `n_candidates` is what it is **scored against**, and they are not the same number (ADR 0011) |
| `docs/benchmark/secondary/README.md`  | Any question about the **generalisability or scalability** claim. Nine further targets, frozen 2026-08-24, in two tiers. `development` is where every hyperparameter is chosen; `generalisation` is not opened until the method is frozen. Same eight clauses plus four selection clauses (ADR 0021). §6 states what the achieved N supports and what it does not; §7 lists eleven limitations |
| `docs/benchmark/evaluation/README.md`  | Any question about **how** a score is computed — endpoint, estimator, null, decoys, multiplicity. **Protocol version 2**, frozen 2026-08-25 alongside `manifest.yaml` and `frozen.json` there; `uv run allo evaluate verify` re-derives it. Version 1 was frozen and reopened the same day by `AUDIT.md`, which is the record of what was wrong — read it before trusting any number a pre-audit document quotes. Every method calls `allo.scoring.score_arm` and no other path. Nothing in it may change once a method has been scored. Do not merge it back into the input manifest |
| `docs/targets.md`                    | Touching a specific protein, its chains, or its ground-truth labels                                                                                                                   |
| `docs/adr/`                          | Before choosing between credible alternatives; write one when the choice would be expensive to reverse. `README.md` there gives the format **and indexes all 25 by topic**            |
| `experiments/README.md`              | Setting up a run directory                                                                                                                                                            |
| `docs/agents/`                       | An installed engineering skill needs the issue tracker, triage labels, or domain-doc layout                                                                                           |
| `CHALLENGE.md`                       | Any question about what the challenge actually requires. It is the spec; do not answer from memory                                                                                    |
| `CONTRIBUTING.md`                    | Writing anything a human contributor reads, or changing setup, the gates, the PR checklist or the experiment procedure. It states the same rules for people that this file states for agents — keep the two in step, and do not duplicate one into the other |

Not in context and not worth loading: `docs/Cleveland-Clinic-Challenge-Statement-vF.pdf`
(4.2 MB — `CHALLENGE.md` is the complete restatement), and anything under `data/raw/`
(parse it with code and print a summary; never read a PDB into context).

---

## Package layout

`src/allo/` is organised by pipeline stage, not by abstraction. Add a module when a stage
needs one, not before.

**What exists today.** Phase 1 built the substrate. Nothing quantum is written yet.

```
structure/    PDB fetch/parse -> coordinates, residue indexing
scoring/      the frozen evaluation harness: `score_arm` and `compare_methods` are the
              only paths a number may take; also nulls, decoys, metrics, calibration
groundtruth/  holo-derived labels ONLY — never imported by prediction code (C1)
inputs.py     the one prediction-path module that opens the manifest
benchmark.py  the freeze and its verification — evaluation side
experiment.py the run-directory scaffold behind `allo new-experiment`
cli.py        `allo <stage> ...` entry point
```

**The names reserved for later phases.** Do not create one until its stage needs it. The
name is fixed here so that two agents do not invent two names for the same stage.

```
network/      contact graph / elastic network construction, coarse-graining   (Phase 1.2, 4)
quantum/      Hamiltonians, propagation metrics, circuits, noise models       (Phase 2, 3)
classical/    baselines (GNM/ANM, random walk, betweenness, eigenvector)      (Phase 1.4)
viz/          2D plots and 3D structure rendering                             (Phase 5)
```

**`groundtruth/` is a sink.** Nothing imports from it except scoring and reporting. This is
C1 expressed in the import graph: holo structures, ligand contacts and label sets enter the
repo only through it. If anything on the prediction path imports it — directly or
transitively — the blind prediction is compromised and the submission is invalid.

**Five data routes bypass the import graph, and each is guarded separately.**

1. **The freezes.** `docs/benchmark/frozen.json` and `docs/benchmark/secondary/frozen.json`
   hold the label sets. No prediction-path module may name either.
2. **The manifests.** `docs/benchmark/manifest.yaml` holds the holo accessions, the effector
   component IDs and — in `blind.why`, `defect` and `note` — label residue numbers written
   out in prose. The secondary set has its own manifest with the same shape. `allo.inputs` is
   the **only** prediction-path module permitted to open either, and `load()` rebuilds the
   result from two allow-lists, so a field added later is redacted by default. The unredacted
   read is `allo.groundtruth.manifest.read_manifest`, behind the import guard. `allo.inputs`
   must never regain a verbatim reader.
3. **The selection ledger.** `docs/benchmark/secondary/selection.json` is an answer key. For
   every admitted arm it carries `holo`, `holo_chain` and `effector` as structured fields, and
   its prose names real label residues. Nothing on the prediction path and no experiment
   runner may open it.
4. **The screening record.** `docs/benchmark/secondary/evidence/extension-candidates.md`
   names real label residues in apo numbering for candidate arms that were measured and
   **not** admitted, plus their holo accessions and effector component IDs. It is an answer
   key for arms that do not exist yet, and it is guarded on the same argument as the ledger.
5. **The evaluation layer.** The whole of `docs/benchmark/evaluation/` is protected by
   default, because `frozen.json` names the site pocket's lining residues and every decoy
   lining. `allo.scoring` reads it; nothing on the prediction path may.

All five are enforced by `tests/test_no_leakage.py`, which names them in `PROTECTED_PATHS`
and in `FROZEN_TOKENS`. An import trace cannot see a file-read route, so the file-read and
content tests are what does.

Dependencies point inward toward the network/propagation logic, never outward toward I/O,
cloud backends or plotting. `quantum/` must be callable without Braket credentials,
`network/` without a PDB fetch. Pass the capability in.

**Conventions.** Residue identity is **author numbering plus chain ID**, preserved end to
end — a hit list indexed by matrix row is not readable by a medicinal chemist and is not a
deliverable (`docs/FIELD.md`). Every stochastic function takes an explicit `seed`. Any
function returning a residue score returns it alongside the residue identity, never as a
bare array whose ordering the caller must reconstruct.

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

GitHub Issues on `George930502/quantum-allostery` via `gh`; external PRs are not a
request surface. See `docs/agents/issue-tracker.md`.

### Triage labels

The five canonical roles, label strings equal to their names. See
`docs/agents/triage-labels.md`.

### Domain docs

Single-context; `docs/adr/` is the decision record. See `docs/agents/domain.md`.
