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

| #   | Rule                                                                                                                                                                                                                                                                                                                      |
| --- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| C1  | **Apo input only.** Holo structures are used _exclusively_ to build ground-truth labels for scoring. No holo-derived information may enter the prediction path — not coordinates, not pocket residues, not even the residue count.                                                                                        |
| C2  | **No classical MD trajectories as input.** Dynamics must be predicted _ab initio_ from topology. No GROMACS/AMBER/OpenMM trajectories and no MD-derived covariance matrices, ever. MD-**trained** weights are a separate tier: admissible, disclosed, and never load-bearing for the primary result (ADR 0027, accepted). |
| C3  | **Near-term hardware viability.** Circuit depth, qubit count, and connectivity must be reported for every quantum method. Deep unoptimised circuits are explicitly penalised. Every quantum claim needs a stated resource cost.                                                                                           |
| C4  | **Credible quantum execution path.** Gate-based, quantum-inspired, and hybrid are all allowed, but a quantum-inspired method must state how it maps to hardware.                                                                                                                                                          |
| C5  | **Scope:** catalytic domains only. Waters, co-factors and PTMs excluded unless modelled as simple nodes. Read as scoping the _system_, not as trimming a chain — the node set is every modelled residue of the frozen chain (ADR 0010, accepted).                                                                         |
| C6  | **Elastic network hypothesis** is the modelling assumption: contact topology drives propagation; atomic force fields are abstracted away.                                                                                                                                                                                 |

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
All three mandated apo/holo pairs are defective and are scored in tiers. **All four now have a
contract**, since the organisers answered on 2026-09-02: the BCR-ABL1 input is `1OPL` chain
**B**, the cardiac-myosin holo is **`9GZ2`** in place of `6C1H`, and c-Myc is scored against
NMR segments and declared non-blind (ADRs 0029, 0031, 0036). Both mandated arms that moved are
**non-confirmatory** and print their measured defects. Every departure from `CHALLENGE.md`
Table 1 is on one page: `docs/report/substitutions.md`. See
`docs/benchmark/primary/README.md` before using any of these accessions:

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

| Open this                             | When                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| ------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `docs/ROADMAP.md`                     | Always, first. Which phase is current and what its exit criterion is                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| `experiments/REGISTRY.md`             | Always, second. What has been tried, and what failed — do not re-run a dead end                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| `CONTEXT.md`                          | Writing the word "site", "pocket", "target" or "pair" anywhere. The settled vocabulary — cryptic and allosteric are **not** synonyms and the difference decides what we are scored on                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| `docs/playbooks/phase-work.md`        | Starting or finishing any unit of work. `/phase` in Claude Code                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| `docs/playbooks/experiment.md`        | About to produce a number worth comparing to another number. `/exp`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| `docs/playbooks/constraint-audit.md`  | Diff touches the prediction path, ground truth, or a quantum method. `/audit`, or the `constraint-auditor` subagent                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| `docs/FIELD.md`                       | Choosing or defending a method; writing anything for the report                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| `docs/PRINCIPLES.md`                  | The one-liners above are not enough to settle a call                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| `docs/benchmark/README.md`            | Not sure which of the three frozen sets answers your question. One page, five rows, then go straight to the set. Shared literature evidence lives beside it in `evidence/`, because all three rest on it                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `docs/benchmark/primary/README.md`    | Any question about **what** a method receives and **what** it is scored against. `frozen.json` is the authority for every residue count, label set and active site — never quote one from prose. `n_residues` is what a method **receives**; `n_candidates` is what it is **scored against**, and they are not the same number (ADR 0011)                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| `docs/benchmark/secondary/README.md`  | Any question about the **generalisability or scalability** claim. Nine further targets, frozen 2026-08-24, in two tiers. `development` is where every hyperparameter is chosen; `generalisation` is not opened until the method is frozen. Same eight clauses plus four selection clauses (ADR 0021). §6 states what the achieved N supports and what it does not; §7 lists sixteen limitations                                                                                                                                                                                                                                                                                                                                                                                                  |
| `docs/benchmark/evaluation/README.md` | Any question about **how** a score is computed — endpoint, estimator, null, decoys, multiplicity. **Protocol version 4**, frozen 2026-09-03 alongside `manifest.yaml` and `frozen.json` there; `uv run allo evaluate verify` re-derives it. Read **§0 first**: it lists the six things version 3 changes and why each is not a hyperparameter. Version 3 opened because the _input_ layer moved, not because a defect was found. Version 1 was frozen and reopened the same day by `AUDIT.md`, which audits version 2 and is the record of what was wrong — read it before trusting any number a pre-audit document quotes. Every method calls `allo.scoring.score_arm` and no other path. Nothing in it may change once a method has been scored. Do not merge it back into the input manifest |
| `docs/benchmark/review/README.md`     | Quoting **any** number from a frozen set, or asking whether one is still right. The 2026-09-02 audit of all three frozen layers, opened when the organisers answered four questions. **`00-official-reply.md` holds their answers verbatim and outranks `CHALLENGE.md` where the two disagree.** `27-fourth-pass-synthesis.md` is the ranked list of what must change; `11`, `25` and `26` are the earlier passes, kept unedited. Corrections live here, not edited into the freezes                                                                                                                                                                                                                                                                                                                                                                                   |
| `docs/evidence/method-landscape/` | Choosing or defending a **method**, in Phase 2 or later. A scoped literature survey of how the field predicts allosteric sites, 23 documents, every claim carrying a DOI. It holds no code and no scored number. `11-pipeline-decomposition.md` assigns each of the eleven pipeline stages to classical, AI or quantum. Read `10a-fact-check.md` before quoting any number from it, and **ADR 0026** before treating `00-conventions.md` §5 as closed. What happened when experiments actually ran is **not here** — it left `main` with the method layer on 2026-09-02 and is on the branch `method-layer-archive` (ADR 0037) |
| `docs/targets.md`                     | Touching a specific protein, its chains, or its ground-truth labels                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| `docs/adr/`                           | Before choosing between credible alternatives; write one when the choice would be expensive to reverse. `README.md` there gives the format **and indexes all 45 by topic**. ADRs 0029-0037, nine of them, were written on 2026-09-02 and two supersede blockers; 0038-0044 came from the 2026-09-03 fourth and fifth passes and opened protocol v4; 0045 came from the sixth and changed nothing on purpose                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `experiments/README.md`               | Setting up a run directory                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `docs/agents/`                        | An installed engineering skill needs the issue tracker, triage labels, or domain-doc layout                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `CHALLENGE.md`                        | Any question about what the challenge actually requires. It is the spec; do not answer from memory                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| `CONTRIBUTING.md`                     | Writing anything a human contributor reads, or changing setup, the gates, the PR checklist or the experiment procedure. It states the same rules for people that this file states for agents — keep the two in step, and do not duplicate one into the other                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |

Not in context and not worth loading: `docs/Cleveland-Clinic-Challenge-Statement-vF.pdf`
(4.2 MB — `CHALLENGE.md` is the complete restatement), and anything under `data/raw/`
(parse it with code and print a summary; never read a PDB into context).

---

## Package layout

`src/allo/` is organised by pipeline stage, not by abstraction. Add a module when a stage
needs one, not before.

**What exists today.** Phase 1 built the substrate; Phase 2 built the method layer on top
of it.

```
structure/    apo-only, and every module here is on the prediction path.
              `pdb` fetch/parse -> coordinates, residue indexing.
              `properties` the three apo-only score confounders -- here, not in `scoring/`,
                so that an apo-only caller does not execute `allo/scoring/__init__.py`.
              `graph` `build(apo, contact=, cutoff=, weighting=)` returns a ResidueGraph
                carrying residue identity, coordinates, deposited B-factor and the source
                set. The default build reproduces the evaluation graph exactly, and a test
                says so. Here rather than in `scoring/` because a future prediction package
                needs it and may not import the evaluation layer (ADR 0037)
scoring/      the frozen evaluation harness: `score_arm` and `compare_methods` are the
              only paths a number may take; also nulls, decoys, metrics, calibration.
              `baselines` holds eight of the nine controls the frozen protocol requires,
                keyed by manifest name as `REQUIRED_BASELINES`. The ninth, `cavity_volume`,
                is in `decoys`. These are controls a method must beat, never candidates
groundtruth/  holo-derived labels ONLY -- never imported by prediction code (C1)
inputs.py     the one prediction-path module that opens the manifest
benchmark.py  the freeze and its verification -- evaluation side
experiment.py the run-directory scaffold behind `allo new-experiment`
cli.py        `allo <stage> ...` entry point
```

**There is no method layer on `main`.** `network/`, `classical/` and `quantum/` were removed
on 2026-09-02 and are preserved whole on the branch `method-layer-archive` (ADR 0037). Phase
2 restarts from an empty package against a frozen substrate. Two things moved rather than
left, because the frozen evaluation protocol requires them: the graph builder is now
`structure/graph.py`, and the eight required baselines are now `scoring/baselines.py`.

Every scorer takes a `ResidueGraph` and returns one array in the graph's own residue order.
`graph.as_scores(values)` is what turns that array into the residue-keyed mapping
`score_arm` requires. **No prediction-path module imports `allo.groundtruth` or
`allo.scoring`.** The prediction path is `allo.structure`, `allo.inputs` and
`allo.experiment`, and `test_the_prediction_path_is_the_set_this_contract_names` pins that
set, so a new prediction package is a decision rather than a side effect.

**The names still reserved.** Do not create one until its stage needs it.

```
viz/          2D plots and 3D structure rendering                             (Phase 5)
```

**`groundtruth/` is a sink.** Nothing imports from it except scoring and reporting. This is
C1 expressed in the import graph: holo structures, ligand contacts and label sets enter the
repo only through it. If anything on the prediction path imports it — directly or
transitively — the blind prediction is compromised and the submission is invalid.

**Nineteen data routes bypass the import graph, and each is guarded separately.**

1. **The freezes, and the trees around them.** `docs/benchmark/primary/` and
   `docs/benchmark/secondary/` are protected **whole**, not file by file. `frozen.json` was
   guarded on the first day and its own siblings were not, which is how route 12 below
   survived nine days. A file added to either tree is now protected by default.
2. **The manifests.** `docs/benchmark/primary/manifest.yaml` holds the holo accessions, the effector
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
6. **The matched-patch cache.** `data/patches/` is derived from the label set and announces
   it in its own array shapes: `members` has width equal to the arm's positive count, for
   all fifteen arms — including the five `generalisation` arms that are not open yet. C1
   names this exact case, "not even the residue count". Its `diagnostics` string carries the
   true site's own geometry as `observed_median_distance_to_source`,
   `observed_radius_of_gyration` and `observed_mean_degree`. `allo.scoring` writes and reads
   it under the constant `PATCH_CACHE`; nothing on the prediction path may. Added 2026-08-27
   by a design-stage constraint audit, which found the directory unprotected.

7. **The multi-axis review.** `docs/benchmark/review/` carries per-arm positive counts, five
   real KRAS label residues in `03-kras-mask.md`, and a candidate ledger with holo accessions
   and effector component IDs. C1 names the residue count directly, and
   `extension-candidates.md` is already protected as a Markdown answer key on the identical
   argument. Protected whole, so a file added there later is protected by default. Its **own**
   tools are exempt, by a rule rather than a name list: a tracked file inside the tree that
   imports no `allo` module may name paths **inside that tree only**. A prediction runner has
   to import the package, so a file that does not cannot be one. Added 2026-09-02 by ADR 0034.

8. **The per-target input audits.** `docs/benchmark/primary/audit/` derives its ligand-contact
   tables from the holo structure, so it reproduces the label sets outright: the **complete**
   set for both KRAS arms in `kras-g12c.md`, and for both BCR-ABL1 arms in `bcr-abl1.md`.
   Protected
   whole. Found 2026-09-02 by sweeping every tracked `.md`, `.yaml`, `.json` and `.txt`
   outside the seven trees above for a run of label residues inside one 400-character window.

9. **The shared literature evidence.** `docs/benchmark/evidence/` prints the KRAS distal label
   set as running prose in `allosteric-prediction-prior-art.md`, to make a point about how
   little of it the ASD covers. Protected whole, on the `evaluation/` argument. Same sweep.

10. **The experiment record.** Every `metrics.json` and `records.jsonl` a scoring run writes
    carries the matched-patch sampler diagnostics, and `observed_radius_of_gyration` is the
    true site's own geometry — 65 such fields in the 2026-09-02 recalibration alone, naming
    all five sealed `generalisation` arms. `data/patches/` was protected for exactly this
    content in August; the copy beside the runner was not. The tree cannot be protected
    outright, because the runners write into it, so the rule is narrower and is the one thing
    here that is not a path: **no file may name a record it did not write.** A run script may
    name the two records beside it. A `config.yaml` is not a record, which is why one runner
    legitimately reads another run's config. Added 2026-09-02. The tree **is** in
    `PROTECTED_PATHS`; `allowed_experiment_path` is the exemption on top of it, not a
    replacement for it.
11. **The target dossier.** `docs/targets.md` prints the cardiac myosin site in three-letter
    codes, which is the **complete** `label_residues` set for both myosin arms, plus the minimum
    label-to-source distance per arm. The sweep that cleared this file on 2026-09-02 matched
    bare integers on a word boundary, so a three-letter code never matched its own number and
    a true finding was recorded as refuted. **Re-run any label sweep with three-letter codes
    normalised.** Protecting the file does not change how you read it: `PROTECTED_PATHS` binds
    prediction modules, not agents.

    This entry quoted the residues until 2026-09-03, and so did the matching comment in
    `tests/test_no_leakage.py`. Neither file is protected and neither is scanned, so the note
    explaining the route was itself the route. **Describe an answer key by its shape and its
    location. Never by its contents.**
12. **The two benchmark READMEs.** `primary/README.md` and `secondary/README.md` tabulate a
    `Scoreable` column that **is** the positive count, beside the holo accession, the holo
    chain and the effector component ID — for all five sealed `generalisation` arms as well.
    That is the payload routes 3 and 6 are protected for, sitting next to the file protected
    first. Covered by the whole-tree protection in route 1, and kept as its own entry because
    it records what the 2026-09-02 sweep found. The per-target input audits, `primary/audit/`,
    were listed a second time below it until 2026-09-03; that entry duplicated route 8 and the
    count said thirteen when eleven routes and two payload notes were listed.
13. **The decision record.** `docs/adr/` was found on 2026-09-03 by re-running the sweep of
    route 11 over the trees that sweep had cleared.
    `0031-cardiac-myosin-holo-substitution.md:22` argues the `9GZ2` substitution from the
    contact shell, so it prints the contact shell: the complete `label_residues` set for both
    myosin arms, in the same three-letter spelling that hid `docs/targets.md` from the first sweep.
    An ADR argues from evidence, and the evidence lands in it. Protected whole, so ADR 0038
    is protected the day it is written.
14. **A former name, and a former place.** A protected path is protected by its name, and a
    rename gives the same bytes a second name no entry covers.
    `docs/benchmark/audit/kras-g12c.md` became `docs/benchmark/primary/audit/kras-g12c.md` on
    2026-08-31, and `git show <sha>:docs/benchmark/audit/kras-g12c.md` still returns the whole
    KRAS contact shell, from `main`, with no network. Two of the five renames carried a frozen
    token in the file name and were backstopped; the three audit files carried none.
    **`tests/former_protected_paths.json` is the authority, not git** (ADR 0043). A first fix
    derived the list at import time and was weakest exactly where a release is verified: a
    shallow clone, a `git archive` export and a machine with no `git` binary all give the empty
    set. Git now cross-checks the ledger and never replaces it. The filter is `RD`, because a
    format conversion is a delete plus an add and not a rename, and **a directory that lost any
    file to a protected tree is itself a former protected tree** — which is the rule rather than
    the three names it was found by. Regenerating the ledger is a deliberate act.
15. **The method-landscape survey.** `docs/evidence/method-landscape/` prints a per-arm
    scoreable count in a power table and more of them in a variance note. C1 names the count as
    plainly as it names the identities. Protected whole on 2026-09-03 by the round-4 audit. A
    standing sweep now fails on any tracked unprotected file that puts a name for an arm, the
    arm's exact count and a word that reads as a count inside one window — the arm identifier
    was not enough, because prose says "both myosin arms" and never says
    `cardiac_myosin_corrected`.

16. **The report tree.** `docs/report/substitutions.md` argues each departure from
    `CHALLENGE.md` Table 1 from the evidence, so it prints the evidence: the effector chemical
    component ID, then every entry containing it, which includes the holo accession.
    `allo.inputs.load`'s own docstring is the argument — "naming the effector is naming where
    the pocket is, to anyone with a search engine" — which is why `effector` is redacted from
    the prediction manifest. The page is a required deliverable and keeps saying what it says.
    Protected whole on 2026-09-03, so `conformance.md` and anything added later is covered.

17. **A data file shipped beside prediction code.** A module that never spells a path can read
    one a sidecar names. A probe added a `.json` next to `structure/graph.py` holding a
    protected path as a value, read the sidecar by an innocuous resolvable path, and opened
    what it named. The segment cover fires on that sidecar's text when it is called on it, and
    nothing ever pointed it there: `.json` is not a runner suffix, `src/` is exempt from the
    runner scan because the package scan covers it, and the package scan globs `*.py`. Every
    non-Python file under `src/` is now scanned, from the filesystem rather than from
    `git ls-files`, because an untracked sidecar imports exactly as readily as a tracked one.
    Added 2026-09-03 by round 6.
18. **A module with no source.** Every scan in the guard keys on `rglob("*.py")`. A probe
    compiled a `.pyc` with no `.py` beside it, imported the ground-truth package from it, and
    the import-graph fixture — which builds its edges by reading source — recorded no edge at
    all. A compiled extension is the committable version: `.so` and `.pyd` are importable and
    are ignored by nothing. The rule is that the module set the interpreter can import must
    equal the module set the guard can read. Added 2026-09-03 by round 6.
19. **A process, and specifically git.** `git -C <root> grep -l <field name> HEAD` performs the
    path lookup at run time, so the source holds only bare words: no protected component, no
    separator, no path expression. All six mechanisms return nothing and a probe recovered a
    per-arm count for every arm in both freezes. `git cat-file --batch-all-objects --batch` is
    wider still — it names no path, no revision and no object id — so it defeats route 14
    outright, since a ledger of former **names** cannot protect content reached without a name,
    and it returns superseded freezes that the working tree no longer holds. The residual this
    file used to declare said "a subprocess whose command is itself computed", which claimed a
    constant command was covered. It was not. The ingredient is removed the way `importlib`
    already was: **no prediction module starts a process, and none names `.git`.** Added
    2026-09-03 by round 6.

All nineteen are enforced by `tests/test_no_leakage.py`, which names them in
`PROTECTED_PATHS`, in `FROZEN_TOKENS` and — for route 10 — in `allowed_experiment_path`. An
import trace cannot see a file-read route, so the file-read and content tests are what does.

**Protecting a path the detector cannot resolve protects nothing.** On 2026-09-02 a module in
`allo.network` read the whole matched-patch cache — every arm's positive count, the sealed
tier included — by writing `Path("data").joinpath("patches")`. The guard modelled the `/`
operator and not its method spelling, and `patches` is not a frozen token, so all 34 tests
passed. `os.path.dirname` had the same hole. Both are closed and probed. This is one failure
mode: **the guard reads the text correctly and the interpreter accepts a form the text does not
model.** It has now recurred four times, and the fourth was `Path("data") / Path("patches")`,
where a `Path` on the right of `/` made the whole expression evaluate to None.

**A whitelist of spellings loses this race, so the guard no longer relies on one.** An
adversarial pass on 2026-09-03 listed 26 spellings the resolver does not model, and three of
them ran together in one tracked runner and read the matched-patch cache, the per-target input
audits and the sealed tier's positive counts with all 37 tests green.
`segment_cover_violations` asks the question the other way round: not "which path does this
expression build", which needs the whole language, but "does this file hold every component of
a protected path", which needs no evaluation at all. The interpreter must still get the
characters from somewhere. The resolver stays as the primary, because it names the concrete
path a reader can act on, and 22 permanent probes hold the backstop. Add a new spelling to
`test_the_segment_cover_backstop_catches_assembled_paths`, and a new resolver form to
`test_constant_path_guard_catches_composition_and_quote_variants`, before trusting a new route.

The race has a second track, and it is the import statement rather than the call. `from os
import walk as traverse` leaves the call site a bare name, so the capability scan — which
reads a `Name`, an `Attribute` and a string — saw no traversal word anywhere. A codex pass ran
it as a live module on 2026-09-03: all four guard helpers returned empty and it read a
protected label-count field for all fifteen arms. The scan now reads `ast.alias` as well.
**A guard that models how a name is used must also model how it is bound.**

**A guard that scans the wrong tree scans nothing.** The package scans globbed `src/allo`
while `NON_RUNNER_TREES` exempted the whole of `src/` on the ground that those scans covered
it. A second package at `src/predict/` was therefore read by neither, and the editable install
puts it on `sys.path` the day it is written. `.github/workflows/ci.yml` and `pyproject.toml`
had the same shape: no suffix in `RUNNER_SUFFIXES` and no first path part in
`NON_RUNNER_TREES`. Both holes were closed on 2026-09-03. Before adding an exemption, name the
scan that covers what it excludes, and check that the scan actually looks there.

**A submodule import executes its parent packages, and the import graph now says so.**
`from allo.scoring.properties import residue_properties` names a module whose own imports are
`numpy`, `scipy` and `allo.inputs`. Reading the source it is clean. Running it, the
interpreter executes `allo/scoring/__init__.py` first and `allo.groundtruth` is in the
process — with no protected path, no frozen token and no `groundtruth` anywhere in the text.
The graph fixture in `tests/test_no_leakage.py` adds the parent edges Python adds, and a
second test states the rule this file has always promised: **no prediction-path module
imports `allo.scoring` by any route.** Both were unchecked until 2026-08-27. The rule named
three packages until 2026-09-02, when they were removed and it started passing over an empty
set.

Dependencies point inward toward the graph and propagation logic, never outward toward
I/O, cloud backends or plotting. `structure/graph.py` must be callable without a PDB fetch,
and a future quantum package must be callable without Braket credentials. Pass the
capability in.

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
- **If the diff can change what an apo structure contains, run `make verify` too.** `make
  check` and `allo evaluate verify` are offline, and offline **skips the pocket detector** —
  the verifier says so, in its own output line. On 2026-09-03 a one-residue input correction
  was reported as moving no frozen value on the strength of an offline run, and it had moved a
  decoy cavity volume. **A verifier that skips a stage cannot certify that stage.**
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
