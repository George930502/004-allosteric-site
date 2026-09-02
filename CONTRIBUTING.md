# Contributing

This is a research codebase, not a library. A change here is a claim about what is true, so
the process protects the claims. Read this page once before your first pull request.

Start with [`README.md`](README.md) for what the project does, and
[`AGENTS.md`](AGENTS.md) for the rules that govern every change.

---

## 1. Set up

```bash
git clone https://github.com/George930502/quantum-allostery
cd quantum-allostery
make setup      # uv sync --extra dev. Python >= 3.11, creates .venv
make check      # must pass on a clean clone
```

If `make check` fails on a clean clone, that is a bug. Open an issue.

Optional extras, installed only when you need them:

| Extra  | Command                | Needed for                               |
| ------ | ---------------------- | ---------------------------------------- |
| `eval` | `uv sync --extra eval` | re-derive the decoy pockets (pyKVFinder) |
| `hw`   | `uv sync --extra hw`   | AWS Braket and Classiq backends          |
| `viz`  | `uv sync --extra viz`  | 3D structure rendering                   |

---

## 2. The two gates

```bash
make check      # offline, seconds. Format, lint, and every test that needs no network
make verify     # network. Re-derives both freezes, re-runs the detector, byte-checks structures
```

Run `make check` before every commit. Run `make verify` before a merge to `main`. CI runs
`make check` on every pull request.

`make check` is offline **by design**. It therefore cannot re-derive a freeze from RCSB. If
your change touches a frozen artifact, run `make verify` yourself and paste the output.

---

## 3. Three rules that break silently

Most mistakes announce themselves. These three do not.

### 3.1 Constraint C1 — no holo data on the prediction path

Holo structures build the labels. They must never reach the code that makes a prediction. A
leak produces excellent results that mean nothing, and no test failure tells you.

- All holo-reading code lives in `src/allo/groundtruth/`. That package is a **sink**. Only
  scoring and reporting import it.
- **Fourteen** file-read routes bypass the import graph. All fourteen are named in
  [`tests/test_no_leakage.py`](tests/test_no_leakage.py) and listed in `AGENTS.md`. If you
  add a fifteenth, add it there. Two of them were found on 2026-09-02 by a sweep whose
  first version matched bare integers and so could not see `Tyr164`; **normalise
  three-letter residue codes before trusting any label sweep.**
- Leakage also has forms that no import reveals: a cutoff tuned until enrichment looked good,
  a `top_k` picked because it matched the known pocket size, a threshold chosen on the
  validation targets. The
  [constraint-audit playbook](docs/playbooks/constraint-audit.md) lists them.

Run the audit before you open a pull request that touches the prediction path:

```bash
uv run pytest -q tests/test_no_leakage.py
```

### 3.2 Never edit a frozen artifact

These files are closed. Nothing in them changes once a method has been scored against them.

```
docs/benchmark/primary/frozen.json              the primary input layer
docs/benchmark/secondary/frozen.json    the secondary input layer
docs/benchmark/evaluation/frozen.json   the evaluation layer, protocol version 4
```

Their manifests carry the choices, and `frozen.json` carries the consequences. `make verify`
fails if a derived value moves.

If a freeze is wrong, do not repair it in place. Write an ADR that supersedes the decision,
state what changes and why, and re-freeze under a new protocol version. A number produced
under one version is not comparable to a number produced under another.

### 3.3 Numbers come from code, never from memory

Residue indices, pocket definitions, chain IDs and literature values are derived
programmatically or cited to a source in `docs/`. Do not hand-type a residue list you know.
Do not quote a count from prose — `frozen.json` is the authority.

A recalled number is not evidence. Where evidence is absent, write "unknown".

---

## 4. How to add a prediction method

This is the Phase 2 workflow. Every method follows it.

**There is no method package on `main`.** It was removed on 2026-09-02 and is preserved on
the branch `method-layer-archive` (ADR 0037). Step 1 below therefore includes reading that
branch, so that a dead end is not re-run. Two things stayed, because the frozen evaluation
protocol requires them: the graph builder is `allo.structure.graph`, and the nine controls a
method must beat are `allo.scoring.baselines.REQUIRED_BASELINES` plus `cavity_volume`. Do not
copy a baseline into a new method package. Compute it from `scoring/` and pass it to
`score_arm` as `against=`.

1. **Read the contract.** [`docs/benchmark/README.md`](docs/benchmark/README.md) indexes the
   three frozen sets. `primary/` states what a method receives, `evaluation/` states how it is
   scored, and `secondary/development` is the only place a hyperparameter may be chosen.
2. **Take the input through `allo.inputs.apo_input`.** It is the one prediction-path module
   that opens the input manifest, and it redacts by default.
3. **Return residue identity with every score.** Author numbering plus chain ID, end to end. A
   hit list indexed by matrix row is not readable by a chemist and is not a deliverable.
4. **Take an explicit `seed`, default `0`,** in every stochastic function.
5. **Score through `allo.scoring.score_arm` and no other path.** A method never chooses an
   estimator, a tie rule, a null or a replicate count.
6. **Tune on the secondary set's `development` tier only.** The primary benchmark is scored
   once, with the choice already fixed. The `generalisation` tier stays closed until Phase 5.
7. **Beat a baseline, and prove it with the paired test.** `allo.scoring.compare_methods` is
   that test. An AUC gap is not a result: `cavity_volume` leads
   `distance_from_source_negated` by AUC-ROC +0.24 on KRAS at p = 0.60.
8. **Report the resource cost** for any quantum method: qubit count, circuit depth and
   connectivity (constraint C3).

---

## 5. How to run an experiment

An experiment is any run that produces a number worth comparing to another number.

```bash
uv run allo new-experiment "ctqw time-averaged transfer"
```

That creates `experiments/YYYY-MM-DD-slug/`. Fill it in:

| File           | Holds                                                   |
| -------------- | ------------------------------------------------------- |
| `config.yaml`  | every knob, the seed included. Complete enough to rerun |
| `metrics.json` | the numbers, written by the run                         |
| `notes.md`     | the question, the setup, the result, the interpretation |

Then add one line to [`experiments/REGISTRY.md`](experiments/REGISTRY.md). **Add it for a
negative result too.** The registry is how the next contributor avoids a dead end you already
walked. A rerun of a committed config must reproduce its metrics exactly. If it does not, the
config is incomplete.

Full procedure: [`docs/playbooks/experiment.md`](docs/playbooks/experiment.md).

---

## 6. When to write an ADR

Write one in [`docs/adr/`](docs/adr/README.md) when a choice is expensive to reverse:

- A modelling choice constrains later phases.
- A method is chosen over a credible alternative.
- A constraint interpretation is settled.

Do not write one for a routine implementation detail. The index in
[`docs/adr/README.md`](docs/adr/README.md) groups all 44 by topic, and the format is at the
top of that file. An ADR is never deleted. A decision that stops binding becomes
`withdrawn` and says why.

---

## 7. Pull requests

1. Branch from `main`. Name the branch after the phase or the experiment.
2. Keep the diff surgical. Every changed line traces to the request. Do not reformat adjacent
   code or "improve" what is not broken.
3. Run `make check`. Run `make verify` if you touched a freeze.
4. Fill in [`.github/PULL_REQUEST_TEMPLATE.md`](.github/PULL_REQUEST_TEMPLATE.md). The
   checkboxes are the constraint audit in short form.
5. Update the memory: a new number goes to `experiments/REGISTRY.md`, a binding decision to
   `docs/adr/`, a closed phase to `docs/ROADMAP.md` and the status table in `README.md`.

Issues live on GitHub. See [`docs/agents/issue-tracker.md`](docs/agents/issue-tracker.md) for
the conventions and [`docs/agents/triage-labels.md`](docs/agents/triage-labels.md) for the
labels.

---

## 8. Code conventions

- `src/allo/` is organised by **pipeline stage**, not by abstraction. Add a module when a
  stage needs one, not before.
- Dependencies point inward toward the graph and propagation logic, never outward toward
  I/O, cloud backends or plotting. `structure/graph.py` must be callable without a PDB fetch,
  and a future quantum package must be callable without Braket credentials. Pass the
  capability in.
- Ruff formats and lints. Line length 100. `make fmt` fixes what it can.
- Add a dependency only when something imports it today. Phase-ahead dependencies were
  removed once already.
- Never commit or print credentials. They come from the environment variables in
  [`env.example`](env.example).
- Never read a PDB file into a review or a document. Parse it with code and print a summary.

---

## 9. If you work with an AI agent

The repo is set up for Claude Code and Codex. [`AGENTS.md`](AGENTS.md) is the operating
contract, and `CLAUDE.md` is a symlink to it.

| Path                | Holds                                                               |
| ------------------- | ------------------------------------------------------------------- |
| `.claude/commands/` | slash commands: `/phase`, `/exp`, `/audit`, `/handoff`              |
| `.claude/agents/`   | subagents, including `constraint-auditor`                           |
| `.claude/skills/`   | domain skills: literature review, statistics, PDB and PubMed access |
| `docs/playbooks/`   | the procedures those commands follow                                |

An agent is held to the same rules as a person, and to four research principles stated in
[`docs/PRINCIPLES.md`](docs/PRINCIPLES.md): reason from first principles, give every unit of
work an exit criterion a command can check, ground every claim in evidence, and work as an
expert in the field would.

---

## 10. Vocabulary

[`CONTEXT.md`](CONTEXT.md) is the settled vocabulary. Read it before you write "site",
"pocket", "target" or "pair" in code or in a document. **Cryptic and allosteric are not
synonyms**, and the difference decides what this project is scored on.
