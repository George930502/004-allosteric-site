# Document alignment audit — the whole tree against the 2026-09-02 re-freeze

**Run 2026-09-02, after the re-freeze, against the working tree (960 changed files, nothing
committed).** Scope: every tracked Markdown and YAML file under `docs/`, plus `README.md`,
`AGENTS.md`/`CLAUDE.md`, `CONTRIBUTING.md`, `CONTEXT.md`, `experiments/`, `src/` and
`tests/`. This is a **sweep**, not a deep read: it asks whether two documents disagree, not
whether either is right on the science.

**Nothing here is a decision and nothing here edits a freeze.** Same rule as the rest of this
directory: a correction is recorded here and moves only when an ADR or a maintainer says so.

**Authorities used.** Every "correct value" column was re-derived from an artifact, never from
prose:

| Fact | Value | Where it came from |
| --- | --- | --- |
| primary arms | **6** | `../primary/frozen.json` → `targets` |
| `bcr_abl1_mandated` | `1OPL`:**B**, **365** nodes, **17** labels, 17 scoreable, 354 candidates | `../primary/frozen.json`, `../primary/manifest.yaml` |
| `cardiac_myosin_mandated` | `5TBY`:A → **`9GZ2`**:A, 954 nodes, 12 labels | same |
| evaluation protocol | **version 3**, **15** arms | `../evaluation/frozen.json` → `protocol_version`, `targets` |
| decoy pockets | **777** over **15** arms | sum of `../evaluation/README.md` §5.3 table |
| ADRs | **36** (`0001`–`0036`) | `ls docs/adr/0*.md` |
| guarded data routes | **7** named; `PROTECTED_PATHS` holds **10** path entries | `AGENTS.md` §Package layout, `tests/test_no_leakage.py` |
| secondary limitations | **16** | `../secondary/README.md` §7 |

**Counts.** 34 contradictions · 18 broken references · 15 pieces of superseded text left
standing · 10 duplication pairs · 10 orphans/redundancies. The index contract holds for
`src/allo/` and fails in one place for the guarded routes.

---

## 1. Contradictions

Two documents stating different values for the same fact, or one document contradicting an
artifact. Ranked: **P1** a reader acts on it and is wrong; **P2** a reader quotes it and
misleads; **P3** cosmetic drift.

| # | P | File:line | Says | Correct value |
| --- | --- | --- | --- | --- |
| C1 | **P1** | `README.md:132-133` | "the candidate set for **5 primary arms**" | **6** |
| C2 | **P1** | `README.md:165` | "**five** file-read routes that no import trace can see are named and guarded" | **seven** (`AGENTS.md:168`) |
| C3 | **P1** | `CONTRIBUTING.md:58-59` | "**Five** file-read routes bypass the import graph. All five are named… If you add a **sixth**, add it there" | seven; the next one is an **eighth** |
| C4 | **P1** | `CONTRIBUTING.md:78` | `evaluation/frozen.json` "the evaluation layer, **protocol version 2**" | **version 3** |
| C5 | **P1** | `docs/benchmark/README.md:12` | "`primary/` … **5 arms**" | **6** |
| C6 | **P1** | `docs/benchmark/README.md:14` | "`evaluation/` … **Protocol version 2**" | **version 3** (line 66 of the same file says 3) |
| C7 | **P1** | `docs/benchmark/README.md:35` | "**Five** scoreable arms" | **six** |
| C8 | **P1** | `docs/benchmark/primary/README.md:3` | "**Status: frozen 2026-08-24. Five** scoreable arms" — the status banner of the input freeze | **re-frozen 2026-09-02; six** scoreable arms |
| C9 | **P1** | `docs/benchmark/review/README.md:26-27` | "Protocol version 3 is written and **not yet frozen**" | frozen 2026-09-02; `../evaluation/frozen.json` has `protocol_version: 3` and `uv run allo evaluate verify --detect` exits 0 |
| C10 | **P1** | `docs/benchmark/evaluation/README.md:423` | §5.3 "Re-derived at protocol version 3 … over **sixteen** arms" | **fifteen** — the table below it has 15 rows and its decoys sum to 777 |
| C11 | **P1** | `docs/benchmark/evaluation/README.md:451` | "The per-arm floor still binds, on three of **sixteen** arms" | three of **fifteen** |
| C12 | **P1** | `docs/benchmark/evaluation/README.md:463` | "the decoy count tracks the candidate count at ρ = +0.953 across the **sixteen** arms" | **fifteen** |
| C13 | **P1** | `docs/adr/README.md:17` | "**Thirty-three** decisions, grouped by what each one settles" | **thirty-six** |
| C14 | **P1** | `AGENTS.md:110` | "`README.md` there gives the format **and indexes all 33 by topic**" | **36** |
| C15 | **P1** | `CONTRIBUTING.md:154` | "The index in `docs/adr/README.md` groups **all 25** by topic" | **36** |
| C16 | **P1** | `README.md:244` | "`adr/` **25 decision records**, indexed by topic" | **36** |
| C17 | **P1** | `README.md:248` | "`evaluation/` how a score is computed. **Protocol version 2**" | **version 3** (line 203 of the same file says version 3 — README contradicts itself) |
| C18 | **P1** | `README.md:233-236` | `network/`, `classical/`, `quantum/` listed under "**reserved, created when the phase needs it**" | all three exist and are populated; **only `viz/` is reserved** (`AGENTS.md:158-161`) |
| C19 | **P2** | `AGENTS.md:192` | patch-cache `members` width "for **all fourteen** arms" | **fifteen** — `../evaluation/frozen.json` has 15 arms |
| C20 | **P2** | `tests/test_no_leakage.py:50` | same sentence, same "**all fourteen** arms" | **fifteen** |
| C21 | **P2** | `AGENTS.md:105` | "`secondary/README.md` … §7 lists **eleven** limitations" | **sixteen** (items 14–16 added 2026-08-24 and 2026-09-02) |
| C22 | **P2** | `docs/ROADMAP.md:259` | "and, in §7, the **eleven** limitations a reviewer would otherwise find" | **sixteen** |
| C23 | **P2** | `docs/benchmark/primary/README.md:262` | "`6C1H` is **bovine** myosin-Ib" | **rat** unconventional myosin-Ib, UniProt **Q05096** — as the same file says at :202, and `../../report/substitutions.md:37`, `docs/targets.md:62`, `experiments/REGISTRY.md:68` |
| C24 | **P2** | `docs/benchmark/primary/manifest.yaml:442` | "`6C1H` is **bovine cardiac myosin S1** with no mavacamten bound" | **rat myosin-Ib + rabbit actin + calmodulin.** Two wrong facts in one clause, inside a frozen manifest. It does not change the arm — the reason (no mavacamten, no label set) stands |
| C25 | **P2** | `docs/report/conformance.md:64` | statistical enrichment "The frozen protocol, **version 2**" | **version 3** |
| C26 | **P2** | `docs/report/conformance.md:73` | C1 enforced by "**five** protected file routes" | **seven** |
| C27 | **P2** | `docs/report/conformance.md:82` | "Minimum four targets … **five primary arms**" | **six** |
| C28 | **P2** | `docs/benchmark/evaluation/README.md:182, 207, 219, 327, 1009` | five present-tense "the five primary arms" / "three of five primary arms" statements inside the **version-3** freeze | six. `experiments/REGISTRY.md:192` already carries the six-arm re-measurement (AUC 0.589 / 0.588 / 0.385 / 0.215 / 0.442 / 0.335, **below chance on four of six**), so :1009's five-value list is superseded by a row in the registry |
| C29 | **P2** | `docs/benchmark/evaluation/README.md:445` | "At the version-2 defaults **the same five primary arms** read 3 / 3 / 24 / 9 / 41" | "the same" is now false — six primary arms exist; the v2 comparison covers five of them |
| C30 | **P2** | `docs/benchmark/secondary/README.md:502` | limitation 15, "and so do **all five primary arms**" | **six** |
| C31 | **P2** | `docs/method/README.md:30` | "`review/` — **Eighteen files.** Fourteen independent literature and data reviews, one synthesis, two verification passes, and one decision file" | **23 files** (`00`–`20` plus `09a`, `10a`) — 17 reviews, 1 synthesis, 3 verification passes (`09a`, `10a`, `20`), 1 decomposition, 1 conventions |
| C32 | **P2** | `docs/method/exploration/README.md:64` | "**Experiments.** Four, all on the secondary set's `development` tier" | nine ran on 2026-08-26, plus `2026-08-27-derived-cutoff-prescreen` and `2026-09-02-null-recalibration`. `docs/ROADMAP.md:324-333` lists nine |
| C33 | **P3** | `docs/benchmark/README.md:80` | "`evidence/README.md` indexes the **twelve** files" | **fourteen** files; the index table holds **13** rows |
| C34 | **P3** | `README.md:277` | "a number produced under protocol version 1 is not comparable to one produced under **version 2**" | version 3 is the current one; the sentence stops one version short |

**Not a contradiction, checked and cleared.** `docs/ROADMAP.md:326` ("6480 records, 1620
complete variants") against `docs/method/exploration/README.md:36` ("7 692 records, 1 923
complete variants") — the first is the `2026-08-26-method-sweep` runner alone, the second is
the three-runner total. `results/40-method-sweep.md:21-24` gives both, correctly scoped.
`docs/benchmark/evaluation/README.md:578-586` and `:1006` are explicitly labelled as
version-2 data. `docs/targets.md` carries a stale top table but repairs it at :66-73 with an
"what changed on 2026-09-02" table, so a reader cannot be misled. `docs/adr/0016` and
`docs/adr/0020` **both carry correct supersession headers** with a paragraph saying what
survives — nothing to fix there.

---

## 2. Broken and stale cross-references

Markdown link targets were checked mechanically: **every relative link in every `.md` file
under `docs/`, plus `README.md` and `AGENTS.md`, resolves.** The one reported miss,
`../secondary/evidence/extension-candidates.md:316` `[LIVM](2)`, is chemistry notation, not a
link. The failures below are `§`-pointers and backticked paths, which no tool checks.

| # | P | File:line | Points at | Problem |
| --- | --- | --- | --- | --- |
| R1 | **P1** | `docs/adr/0009-structure-admission-rule.md:7` | `../benchmark/primary/README.md` §7 | that file has **§1–§6**; the open items it means are now **§6** |
| R2 | **P1** | `docs/benchmark/evidence/allosteric-prediction-prior-art.md:28` | `primary/README.md` §7 | same — **§6** |
| R3 | **P1** | `docs/benchmark/evidence/allosteric-prediction-prior-art.md:139` | `primary/README.md` §7 | same — **§6** |
| R4 | **P1** | `docs/method/exploration/lit/24-residue-descriptors.md:773` | `src/allo/scoring/properties.py` | the module is `src/allo/structure/properties.py`. `AGENTS.md:131-133` states the move **and the reason** — reaching it through `scoring/` executes `allo/scoring/__init__.py` and pulls `allo.groundtruth` into the process |
| R5 | **P1** | `docs/method/exploration/results/51-adaptation-constraint-audit.md:382` | `src/allo/scoring/properties.py` | same |
| R6 | **P2** | `docs/method/review/15-ai-preprocessing.md:819` | `src/allo/network/characterise.py` | no such file; `network/` holds `graph.py` only |
| R7 | **P2** | `docs/ROADMAP.md:55` | `data/fetch_structure_evidence.py` | real path `docs/benchmark/review/data/fetch_structure_evidence.py`. Bare `data/` reads as the repo-root `data/`, which is a guarded tree |
| R8 | **P2** | `docs/adr/0034-…:26` | `data/fetch_structure_evidence.py` | same |
| R9 | **P2** | `docs/benchmark/secondary/README.md:234` | `docs/benchmark/README.md` §4 | that file has had **no numbered sections** since the 2026-08-25 split into three siblings |
| R10 | **P2** | `docs/benchmark/evidence/allosteric-pair-definition.md:1036` | `docs/benchmark/README.md` §1 | same |
| R11 | **P2** | `docs/benchmark/evidence/allosteric-pair-audit.md:161` | `docs/benchmark/evidence/README.md` §1 | that README has **no numbered sections** |
| R12 | **P2** | `docs/benchmark/evidence/allosteric-pair-definition.md:759` | `docs/benchmark/evidence/README.md` §5 | same |
| R13 | **P2** | `docs/benchmark/review/07-metrics-audit.md:653` | `./README.md` §4 | **this** directory's README has no numbered sections |
| R14 | **P2** | `docs/benchmark/review/11-synthesis.md:217` | `../evaluation/README.md` §12.4 | §12 exists and has **no subsections** |
| R15 | **P2** | `docs/method/exploration/README.md:42` | `results/44-stability-and-noise.md` §4.2 | that file has §1–§8 |
| R16 | **P2** | `docs/method/exploration/results/51-…:284` | `docs/playbooks/experiment.md` §13 | the playbook has two headings, neither numbered |
| R17 | **P2** | `docs/method/review/12-constraint-audit.md:424` | `docs/playbooks/constraint-audit.md` §4.1 | that playbook numbers nothing; its sections are `C1`–`C6` |
| R18 | **P3** | 20 sites in `09-extension-sweep.md`, `14-clause-ii-literature-pass.md`, `11-synthesis.md`, `../secondary/evidence/extension-candidates.md` | `secondary/README.md` §7.1–§7.10, `09-extension-sweep.md` §6.1–§6.8 | §7 and §6 are **numbered lists**, not numbered subsections, so `§7.10` means "limitation 10". The same synthesis file writes it both ways — `§7 limitation 14` at the disposition table and `§7.2` at :219. Pick one |

**Mislabelled link text** (the href is right, the label is not): `../evaluation/README.md:16`
renders "`../README.md`" over an href of `../primary/README.md`; `README.md:147` renders
"`README.md`" over `docs/benchmark/evaluation/README.md`; `../primary/README.md`'s file table
labels the row `evidence/` for a directory that is `../evidence/`.

**ADR numbers referenced in prose all exist**, `0001`–`0036`, with no dangling number.

---

## 3. Superseded text left standing

ADR 0031 supersedes 0016; ADR 0036 supersedes 0020. **Both superseded ADRs carry correct
headers**, so the defect is entirely in the documents that cite them.

| # | P | File:line | Asserts the superseded position | What is true now |
| --- | --- | --- | --- | --- |
| S1 | **P1** | `README.md:116` | Cardiac myosin mandated pair `5TBY` → `6C1H`, "**unscoreable**" | ADR 0031: the frozen arm is `5TBY`:A → **`9GZ2`**:A, scoreable, non-confirmatory, both defects printed. This is the front door of the repository |
| S2 | **P1** | `README.md:117` | c-Myc "`1NKP` \| **no ground truth; consensus-judged** \| —" | ADR 0036: a reported deliverable, `1NKP` chain A auth 900–981, scored against NMR chemical-shift segments with a hypergeometric null, **declared non-blind** |
| S3 | **P1** | `README.md:115` | BCR-ABL1 mandated status "apo has myristate **in the target pocket**, contacting 16 of 20 labels" | ADR 0029: the frozen input is `1OPL`:**B**, whose pocket is **empty** (nearest ligand atom 16.0 Å) and which carries **17** labels. The row describes a chain that is no longer the input |
| S4 | **P1** | `docs/report/conformance.md:97` | myosin row: our arm is `cardiac_myosin_corrected` (9GZ3); "the mandated pair is **unscoreable as assigned**" | `cardiac_myosin_mandated` is frozen and scored |
| S5 | **P1** | `docs/report/conformance.md:98` | c-Myc: "**no arm exists.** ADR 0020 requires the c-Myc contract before method design, and it is **unwritten**" | it is written — ADR 0036 |
| S6 | **P1** | `docs/report/conformance.md:118` | "Give c-Myc a contract … **ADR 0020 already says this blocks method design**" | done; the blocker is cleared |
| S7 | **P1** | `docs/benchmark/primary/README.md:445` | "**c-Myc (`1NKP`) is out of scope for this phase** (ADR 0020)" | in scope, contract frozen |
| S8 | **P2** | `docs/ROADMAP.md:348-349` | "**c-Myc has no arm** … item four blocks method design under **ADR 0020**" | the same file says the opposite at :51 and :288. ROADMAP contradicts itself |
| S9 | **P2** | `docs/ROADMAP.md:444` | Phase 5: c-Myc "input and evaluation contract must be frozen before method design, not after **(ADR 0020)**" | cite ADR 0036 and record it as met |
| S10 | **P2** | `CONTEXT.md:120-121` | "**Stretch target**: c-Myc, which has no characterised allosteric site and **therefore no ground truth**" | it has a scoring contract; "no *holo* label set" is the surviving half |
| S11 | **P2** | `src/allo/inputs.py:159` | comment: "**ADR 0016 records why 5TBY is blocked** without fabricating a propagation source" | 5TBY is a frozen, admitted arm with a motif-derived source (ADR 0031). The `prediction_status` mechanism the comment explains is still real; only the example is dead |
| S12 | **P2** | `docs/benchmark/primary/README.md:423-424` | Open items: "**Two questions for the organisers.** (a) `6C1H` is the wrong protein … **What was intended?**" | answered 2026-09-02 (`00-official-reply.md`). Both questions are closed |
| S13 | **P2** | `docs/benchmark/secondary/README.md:73` | cites **ADR 0016** as the precedent for "how a defective pair was repaired" | cite ADR 0031, or say "0016, superseded by 0031" |
| S14 | **P3** | `docs/report/conformance.md` (whole page) | re-read against the PDF **2026-08-26**; carries S4–S6 plus C25–C27 | it has no supersession banner. Every other stale page in this repo has one |
| S15 | **P3** | `docs/benchmark/evaluation/AUDIT.md:39,170` | M15: ADR 0020's blocker "is recorded now, and **it is still live**" | historical audit record, correctly framed as one — but it is the only "still live" in the frozen evaluation tree, so a one-line pointer to ADR 0036 would cost nothing |

---

## 4. Duplication that will drift

`AGENTS.md` states the rule at its own routing table: `CONTRIBUTING.md` "states the same
rules for people that this file states for agents — **keep the two in step, and do not
duplicate one into the other**." The rule is violated, and every violation has already
drifted.

| # | P | The fact | Stated in | Drift today |
| --- | --- | --- | --- | --- |
| D1 | **P1** | Number of guarded file-read routes | `AGENTS.md:168` (**seven**), `CONTRIBUTING.md:58` (five), `README.md:165` (five), `docs/report/conformance.md:73` (five) | **3 of 4 copies wrong.** Only `AGENTS.md` and `tests/test_no_leakage.py` should carry it; the rest should link |
| D2 | **P1** | Number of ADRs | `docs/adr/README.md:17` (**thirty-three**), `AGENTS.md:110` (33), `CONTRIBUTING.md:154` (25), `README.md:244` (25) | **4 of 4 wrong**, and they disagree with each other by 11. Only `docs/adr/README.md` should say a number |
| D3 | **P1** | Evaluation protocol version | `README.md:142` (3), `:203` (3), `:248` (**2**), `CONTRIBUTING.md:78` (**2**), `docs/benchmark/README.md:14` (**2**), `:66` (3), `AGENTS.md:106` (3), `docs/report/conformance.md:64` (**2**) | 4 of 8 wrong, and `README.md` and `docs/benchmark/README.md` each contradict themselves |
| D4 | **P1** | Primary arm count | `README.md:20` (six), `:132` (**5**), `docs/benchmark/README.md:12` (**5**), `:35` (**Five**), `../primary/README.md:3` (**Five**), `docs/ROADMAP.md:100` (Five, historical) | `docs/benchmark/README.md:108` itself says "**`frozen.json` is the authority.** Never quote a residue count, a label set or an active site from prose." The arm count deserves the same rule |
| D5 | **P2** | The patch-cache C1 argument | `AGENTS.md:189-196` and `tests/test_no_leakage.py:44-56` — near-verbatim, ~13 lines | Both carry the same stale "**fourteen arms**" (C19/C20). The test file is the one that can be checked; `AGENTS.md` should cite it |
| D6 | **P2** | `src/allo/` package layout | `AGENTS.md:126-161` (correct) and `README.md:220-236` (**stale**) | `README.md` still calls `network/`, `classical/` and `quantum/` reserved, and omits `structure/properties.py`. Its own header says "AGENTS.md fixes the names" — so it should stop restating them |
| D7 | **P2** | Code conventions | `CONTRIBUTING.md:184-189` reproduces `AGENTS.md:126-128` and `:222-224` almost word for word ("organised by **pipeline stage**, not by abstraction"; "Dependencies point inward … `quantum/` must be callable without Braket credentials, `network/` without a PDB fetch. Pass the capability in.") | The literal case the AGENTS.md rule forbids |
| D8 | **P2** | Count of `secondary/README.md` §7 limitations | `AGENTS.md:105` (eleven), `docs/ROADMAP.md:259` (eleven) | both wrong; sixteen. Neither needs a number at all |
| D9 | **P3** | `make check` / `make verify` semantics | `README.md:50-59`, `CONTRIBUTING.md:34-43`, `AGENTS.md` §Environment | `AGENTS.md` says "read the `Makefile` rather than trusting a copy here", then two other files keep copies. Currently consistent; three copies is three chances to drift |
| D10 | **P3** | The frozen-artifact list | `CONTRIBUTING.md:76-78`, `docs/benchmark/README.md:33-83`, `AGENTS.md:99-107` | `CONTRIBUTING.md`'s copy is the one carrying the stale version number (C4) |

---

## 5. Orphans and redundancy

| # | P | Path | Finding |
| --- | --- | --- | --- |
| O1 | **P2** | `docs/method/review/20-fact-check-17-19.md` | **True orphan.** No file in the repository names it. `docs/method/README.md` indexes `00`–`19` in three tables and stops; `20` verifies `17`–`19`, which is exactly the file a reader of `17`–`19` must be sent to (the same role `10a-fact-check.md` plays for `10`, and that one *is* indexed) |
| O2 | **P2** | `docs/benchmark/evidence/conservation-confounder.md` | Not in `../evidence/README.md`'s index table, which is the one thing that index exists to do. Named only by ADR 0035 |
| O3 | **P2** | `./data/` | The `data/` block in `./README.md:70-80` lists 8 of 15 entries. Missing: `extension-candidates-2026-09.json`, `structure-evidence-refresh.json`, `fetch_refresh_2026_09.py`, `extract_refresh_2026_09.py`, `fetch_structure_evidence.py`, `rcsb-2026-09-refresh/`, `rcsb-abl1/`. Two of those are the tools ADR 0034's exemption rule was written for |
| O4 | **P2** | `allosteric-benchmark/` (repo root) | A **nested git repository** — its own `.git`, its own `LICENSE`, an 85 KB `README.md`, `README.zh-TW.md`, and `data/`, `gnn/`, `hybrid/`, `methods/`, `scripts/`, `external/`. Untracked and ignored by the last line of `.gitignore` ("Separate upstream repo, cloned here for reference; not part of this project"). It is the **teammate benchmark** ADR 0026 rules on, and ADR 0026:19-23 cites paths inside it. Nothing in `src/`, `tests/` or the `Makefile` reads it. **It does not belong inside the working tree**: ADR 0026's finding is that a human reads it and acts on it by a route no test watches, and keeping it one `cd` away maximises that risk. `tests/test_no_leakage.py`'s `NON_RUNNER_TREES` does not exempt it — it is invisible to that scan only because it is untracked, so a stray `git add` would trip the runner gate |
| O5 | **P3** | `graphify-out/` | Ignored and untracked, yet exempted by name in `tests/test_no_leakage.py` `NON_RUNNER_TREES`. The exemption is unreachable while the ignore rule stands — harmless, but it reads as if the directory were tracked |
| O6 | **P3** | `scratch/` | 7 untracked, ignored files: `check_dephase.py`, `verify_quantum.py`, `warm_cache.py`, `eda_graphs.py`, `eda_graphs.json`, `eda_graphs_clean.json`, `eda_graphs.log`. Nothing references them and no document says the directory exists. `../review/README.md` "How to read a finding here" rule 2 says probes live in `scratchpad/probe/`, not `scratch/` — two names for one idea |
| O7 | **P3** | `data/processed/` | Exists and is empty. `data/README.md:22` documents it; nothing writes it |
| O8 | **P3** | `data/patches/` | 128 files, the **sixth guarded route** — and `data/README.md` does not mention it at all, while documenting `interim/`, `processed/` and `external/`. The one directory in `data/` with a C1 argument attached is the one its README omits |
| O9 | **P3** | `data/README.md:15` | "restored **all seven** holo entries into the shared cache" — a 2026-08-21 statement; there are now 3 primary + 9 secondary holo accessions |
| O10 | **P3** | `results/` | Holds `README.md` only. No `connectivity.npz` and no `hits.csv` for any target — deliverables 1 and 2. Already recorded in `../../report/conformance.md` §1, so this is a cross-check, not a new finding |

`.DS_Store` (6.0 KB) sits at the repository root; it is ignored, so this is housekeeping only.

---

## 6. The index contract

### 6.1 `src/allo/` — **PASS**

`AGENTS.md:129-149` names `structure/`, `scoring/`, `groundtruth/`, `network/`, `classical/`,
`quantum/`, `inputs.py`, `benchmark.py`, `experiment.py`, `cli.py`. All ten exist. Nothing
exists under `src/allo/` that `AGENTS.md` does not name. `viz/` is declared reserved at :160
and is absent, as promised. `classical/` holds exactly the four modules `AGENTS.md:140-143`
claims (`baselines`, `coupling`, `mechanism`, `postprocess`); `structure/properties.py` is
where :131 says it is.

`README.md:220-236` promises a **different** layout for the same directory and is wrong (C18,
D6).

### 6.2 The seven guarded routes vs `PROTECTED_PATHS` — **PASS with one gap**

| `AGENTS.md` route | Enforced by |
| --- | --- |
| 1 the freezes | `PROTECTED_PATHS` — `primary/frozen.json`, `secondary/frozen.json` ✔ |
| 2 the manifests | **not** in `PROTECTED_PATHS`. `FROZEN_TOKENS` carries `manifest.yaml` / `MANIFEST`, plus the allow-list in `allo.inputs.load` and `test_only_the_boundary_module_reads_the_manifest` ✔ |
| 3 the selection ledger | `PROTECTED_PATHS` ✔ |
| 4 the screening record | `PROTECTED_PATHS` ✔ |
| 5 the evaluation layer | `PROTECTED_PATHS` (whole tree) ✔ |
| 6 the matched-patch cache | `PROTECTED_PATHS` + `FROZEN_TOKENS` `PATCH_CACHE` ✔ |
| 7 the multi-axis review | `PROTECTED_PATHS` (whole tree) + `REVIEW_TOOLS` exemption rule ✔ |

**The gap is the other direction.** `PROTECTED_PATHS` holds **ten** path entries. Three —
`structures/holo`, `data/raw`, `data/raw/eval` — are not among the seven routes `AGENTS.md`
enumerates. They are covered by the prose above the list ("holo structures … enter the repo
only through `groundtruth/`") and by `data/README.md:6-19`, but a reader who counts
`PROTECTED_PATHS` and reads "seven" will not reconcile the two numbers. Say either "seven
*document* routes plus the three structure caches", or number all ten.

`AGENTS.md:200-202`'s claim — "All seven are enforced by `tests/test_no_leakage.py`, which
names them in `PROTECTED_PATHS` **and** in `FROZEN_TOKENS`" — is true as a disjunction and
false as a conjunction: route 2 is in `FROZEN_TOKENS` only, route 7 in `PROTECTED_PATHS` only.

---

## 7. The five worst, in order

1. **`README.md:115-117`** — the repository's front door still presents the mandated cardiac
   myosin pair as `6C1H`/"unscoreable" and c-Myc as having no ground truth, both superseded
   the same day by ADRs 0031 and 0036, and presents BCR-ABL1's chain-A defect as the mandated
   arm's status when the mandated arm is chain B. Three of four rows in the target table are
   wrong (S1, S2, S3).
2. **The ADR count, three files, three different numbers** — 25 / 33 / 33 against an actual
   36 (C13–C16, D2). The number is restated in four places and correct in none.
3. **The guarded-route count, four files, two different numbers** — five / seven against an
   actual seven (C2, C3, C26, D1), inside the C1 documentation, which is the constraint
   `AGENTS.md` itself calls "the easiest mistake to make and the hardest to notice". A
   contributor following `CONTRIBUTING.md:59` would add the eighth route as a sixth.
4. **`docs/benchmark/evaluation/README.md:423, 451, 463` — "sixteen arms"** — three
   present-tense statements inside the *frozen* protocol-version-3 document, contradicting
   the 15-row table directly beneath the first of them, `frozen.json`'s 15 arms, and the same
   file's own "fifteen" at :27, :62, :88, :535 (C10–C12).
5. **`docs/report/conformance.md`** — the page whose whole job is to say where the project
   stands against the challenge is a week stale in six places at once (C25, C26, C27, S4, S5,
   S6), including "no arm exists" for a target that has a frozen contract, and it carries no
   banner warning a reader of it.

---

## 8. What this audit did not check

- **Whether any number is scientifically right.** Only whether two documents agree.
- **`docs/method/review/` and `docs/method/exploration/` internal consistency** beyond index
  and count claims — `10a-fact-check.md` and `20-fact-check-17-19.md` own that.
- **Anchor fragments** (`#section-name`) in links; only the file half was resolved.
- **`CHALLENGE.md`**, which is a verbatim restatement and is not ours to align.
- **Prose inside `../` review files that records what was true at audit time.** By this
  directory's own rule those are unedited records, and stale values in them are the point.
  The one exception taken as a finding is `README.md:26-27`, which is a present-tense status
  claim rather than a record (C9).
