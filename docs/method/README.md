# The method layer

Phase 2 and later. The input layer and the evaluation layer are frozen and live under
`docs/benchmark/`; this directory holds the choice of **method** and the evidence behind it.

Phase 1 built a substrate that can measure a method. Nothing here changes it. Every number
this layer produces goes through `allo.scoring.score_arm` and no other path.

---

## Two directories, and the order they were written in

`review/` is the evidence base, compiled 2026-08-25, and it ends with the sentence "No
experiment has run." `exploration/` is what happened when they ran, on 2026-08-26.

| Open this                                                           | When                                                                                                                                                                                                                           |
| ------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [`exploration/`](exploration/README.md)                             | **Start here for anything Phase 2 onward.** Three experiments on the `development` tier, seven further literature sweeps over adjacent fields, an EDA of the frozen inputs, and the threat list a screen result has to survive |
| [`review/`](#review--the-phase-2-evidence-base-compiled-2026-08-25) | You want the argument a candidate came from, or the constraint audit behind a stage                                                                                                                                            |

**One thing in `review/` was overturned rather than extended.** Its §5 list of eleven closed
quantum insertion points rested on a benchmark that contains all three of our primary targets
in its own evaluation sets. **ADR 0026** re-opens eight of the eleven — three survive on
mathematics — and `review/00-conventions.md` §5 now carries the amendment at its head.

---

## `review/` — the Phase 2 evidence base, compiled 2026-08-25

Eighteen files. Fourteen independent literature and data reviews, one cross-cutting synthesis,
two verification passes, and one decision file. They were written by agents that could not see
each other's work, which is what makes the convergences in `10-synthesis.md` meaningful.

**Four were added on 2026-08-26** and they are numbered `13` to `16`. They answer questions the
first nine did not ask, and three of them overturn something the first nine concluded. Open them
before trusting a Phase-2 conclusion about the graph, the distance confound, or where a quantum
advantage lives. `12-constraint-audit.md` keeps its number; the quantum survey is `16` because
`12` was already taken.

**Read in this order if you are new.** `11` is the decision. `10` is the argument. `10a` and
`09a` are the corrections that bind both. Everything else is depth you open when you need it.

| Open this                             | When                                                                                                                                                                                                                                                                           |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `review/11-pipeline-decomposition.md` | **Start here.** The eleven pipeline stages, who owns each, what would prove each assignment wrong, and what to run first                                                                                                                                                       |
| `review/10-synthesis.md`              | You want the argument rather than the conclusion. Convergent findings ranked by independent routes, eight contradictions with their settling tests, and the causal chain that makes most findings dependent rather than independent. **Carries a correction banner — read it** |
| `review/10a-fact-check.md`            | **Before quoting any number from `10` or below.** Ten load-bearing claims re-retrieved from source. Three failed, four needed qualification. It overturns a theorem reading, a parameter bound, a circuit depth and an unsourced result                                        |
| `review/09a-power-verification.md`    | Anyone claims our benchmark is underpowered. An independent re-derivation: the arithmetic held, the inference did not. Also proves mean midrank is exactly affine in AUC, which makes every arm's critical value computable at scoring time                                    |
| `review/00-conventions.md`            | Writing or extending any file here. Evidence tags, retrieval routes, the six hard constraints, the leakage guard, and the eleven quantum insertion points already closed by measurement                                                                                        |

### The nine dimensions

| Open this                                  | When                                                                                                                                                                                                   |
| ------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `review/01-classical-baselines.md`         | Choosing or defending a baseline. ~33 methods with their datasets and hit criteria. **Only four classical methods condition on a named active site, as ours must**                                     |
| `review/02-ai-methods.md`                  | Asking whether a learned component is legal or affordable. Carries the supervision ceiling and the per-method C1/C2 verdict. Four methods are illegal in a way that is easy to miss                    |
| `review/03-quantum-methods.md`             | Choosing a quantum observable. The candidate space, what each needs from the Hamiltonian, and why a real symmetric contact graph supplies almost none of it                                            |
| `review/04-hybrid-quantum-ai.md`           | Designing the division of labour. Stage-by-stage evidence on what quantum and AI each own, and the quantum-reservoir-computing branch closed                                                           |
| `review/05-adjacent-task-transfer.md`      | Looking for a framework from a neighbouring field. Effective resistance, mechanical metamaterials, network controllability, MD-free ensemble generation                                                |
| `review/06-signal-propagation-physics.md`  | **Before defending any observable.** What physically carries an allosteric signal, whether allostery is pathway-like or ensemble-like, and the exponential decay law the whole leaderboard is built on |
| `review/07-coarse-graining-scalability.md` | Compressing the network. Three methods with real guarantees, the measures that prove retention, and the failure mode that hides behind healthy-looking eigenvalues                                     |
| `review/08-hardware-viability.md`          | Any C3 or C4 claim. Encodings, exact gate counts, the N ≈ 20 coherence ceiling, Braket devices and costs, and the Classiq synthesis risk                                                               |
| `review/09-data-analysis.md`               | Asking what the measured numbers already say. 501 contact graphs profiled, every method's distance R², and no subgroup surviving multiplicity                                                          |
| `review/12-constraint-audit.md`            | Before implementing any stage. The proposal audited against C1–C6 stage by stage                                                                                                                       |

### The four added 2026-08-26

| Open this                               | When                                                                                                                                                                                                                                                                                                                                                                                              |
| --------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `review/13-graph-construction.md`       | Choosing or defending the **graph**. Node scale, edge rule, node features, and what the allosteric field actually builds. Carries the one-question test for whether a construction can escape the distance confound at all, and the finding that a cutoff sweep leaves AUROC flat while AUPRC collapses — which is why `exploration/results/40-method-sweep.md` now states its graph result twice |
| `review/14-distance-confound.md`        | Anyone claims a score adds signal **over distance**. The transferable nulls, the descriptors that are genuinely distance-orthogonal, and the nested-spline likelihood-ratio test that is the right way to ask. It also retires SCA sectors as a candidate and reports that no published allosteric-site predictor was found running a distance-only control                                       |
| `review/15-ai-preprocessing.md`         | Before adding any learned component. The admissibility table under ADR 0027's tiers, with training-data provenance cited per model. PocketMiner, PEGASUS, CrypticScout and DiG all fail or cannot be determined. The recommended front end is label-free adaptation, and the arithmetic for why a trained selector cannot be validated at n = 13                                                  |
| `review/16-quantum-algorithm-survey.md` | **Before any claim about where quantum helps.** QAOA, QPE, VQE, annealing and quantum kernels for site prediction; the challenge's own two references read and priced; and the theorem that a time-averaged walk from a zero-energy state _is_ the classical degree ranking, which is what our source state was                                                                                   |

### The three added 2026-08-27

| Open this                              | When                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| -------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `review/17-generalisation-variance.md` | **Anyone reads a between-arm spread as a verdict.** How far site-prediction performance moves between targets and between benchmarks in the published field, why most method papers cannot show it (pooled residue-level estimators), the four same-method-two-benchmark deltas that are the only admissible external comparators, and the calibration: our classical spread of 0.175 over four arms is within 4 % of the Hanley–McNeil noise floor |
| `review/18-selection-sample-complexity.md` | **Before proposing anything that picks a method per protein.** How many instances the algorithm-selection field needs to fit a selector, why the Gupta–Roughgarden bound is vacuous at m = 4, the exact permutation floor that gives a four-arm rank test power exactly zero, and the OPENML-WEKA-2017 scenario — 105 instances, 30 candidates, a bounded metric, and six of eight submitted selectors no better than the single best solver |
| `review/19-cross-protein-normalisation.md` | **Before implementing any normalisation, and before proposing another clock.** Eleven ranked tier-(i) and tier-(ii) rules, plus the two screens that cost nothing and remove most of them: AUC is rank-invariant, so a uniform per-protein rescaling is a **no-op** for our endpoint; and a rule that only slides a hyperparameter can reduce between-protein spread by at most about twice the within-protein endpoint range, which predicted the gap clock's 2 % failure on paper |

---

## How to read a number from this directory

Three rules, inherited from `docs/benchmark/evidence/README.md` and not relaxed here.

- **Tags are load-bearing.** `[VERIFIED-FULLTEXT]` means the quote came back from the paper's
  full text in that session. `[UNVERIFIED]` means it did not, and the claim must not reach
  `docs/report/` without retrieving it first.
- **`10a-fact-check.md` wins.** Where it corrects a file, the correction binds. Three of ten
  load-bearing claims did not survive re-retrieval, and one of those was being used to close an
  entire class of approaches.
- **Check the file's verification depth before you lean on it.** The nine reviews differ, and
  the difference is not cosmetic. `08` carries 61 full-text-verified claims, `07` 49, `06` 45.
  **`05` carries one.** Its 44 remaining sources were verified at abstract level only — and
  `05` is where the review's strongest new candidate, effective resistance to the source, comes
  from. That candidate is worth testing precisely because testing it is cheap; it is not worth
  trusting on the strength of its sourcing.
- **Numbers from different benchmarks are not comparable.** Every file states the dataset, the
  positive class, the negative class and the hit criterion beside its metrics, because the
  field's own criteria differ and the differences are large. `09a-power-verification.md` records
  what happens when that rule is broken: a five-axis category error that produced a false alarm.

## What is not here

**A result.** Three experiments have run and their numbers are in `exploration/results/`, but
a screen selects and does not confirm. Nothing in either directory has been scored on the
`generalisation` tier or on the primary benchmark, and the confirmatory design that would
change that is `exploration/results/42-threats-and-confirmation.md` §4.
