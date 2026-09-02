# The Phase-2 exploration

**Opened 2026-08-26.** `../review/` is the evidence base compiled on 2026-08-25: nine
literature reviews, a synthesis, two verification passes and a decision file. It ends with
the sentence "No experiment has run."

This directory is what happened when they ran.

---

## Why it exists, and what changed

The principal investigator's standing instruction for this phase:

> Withdraw the previous claim about which methods may possibly work or not, unless you have
> done the real experiments and verified with the real number, not by guessing.

`../review/00-conventions.md` §5 lists eleven quantum insertion points under the heading
"do not re-derive it". Every one was closed by measurement — on a **different** benchmark,
with a different graph, a different positive class, a different candidate pool, a different
estimator and a different null. On 2026-08-26 that benchmark was audited against ADR 0012's
disjointness clauses for the first time, and it **fails**: KRAS, ABL1's myristoyl pocket and
myosin are all in its own evaluation sets. **ADR 0026** records the finding and the rule that
follows — those results are prior, not verdict, and a method is closed for this project only
when an experiment on _this_ frozen benchmark produces a number.

So the eleven were re-opened, together with everything else, and measured here.

---

## Read in this order

| Open this                                                                | When                                                                                                                                                             |
| ------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`results/42-threats-and-confirmation.md`](results/42-threats-and-confirmation.md)               | **Start here.** Ten ways the winner could be spurious, each with its control, and the confirmatory design that turns a screen into a result                                                               |
| [`results/40-method-sweep.md`](results/40-method-sweep.md)               | You want the numbers. 7 692 records, 1 923 complete variants, and the measured quantum-against-classical comparison. **0 of 1 923 reject the null on all four arms** |
| [`results/41-selection-and-power.md`](results/41-selection-and-power.md) | **Before quoting any number from `40`.** What a screen of this size produces by chance, how many of its variants are independent, and what four arms can resolve |
| [`results/43-quantum-resources.md`](results/43-quantum-resources.md) | Any C3 or C4 claim. Qubit count, depth, gate count and connectivity for all eleven quantum observables, the coarse-graining factor each arm needs, and the one circuit worth running on hardware |
| [`results/46-beats-distance.md`](results/46-beats-distance.md) | **The central negative.** 69 scorers against the distance baseline through the frozen paired test. 7 wins of 272 where chance gives 6.8, and 0 of 272 against eigenvector centrality. Also records why the Holm correction cannot reject on two of the four arms |
| [`results/45-source-choice.md`](results/45-source-choice.md) | Anything about **where propagation starts**. Six label-blind sources, size-matched. The catalytic site is fourth of six and has the largest between-arm spread of any source tested |
| [`results/47-quantum-constructions.md`](results/47-quantum-constructions.md) | The three quantum families added 2026-08-26, and the theorem behind them. Our source state had **energy exactly zero**, which is the classical point. Also closes the symmetry branch with a measurement |
| [`results/44-stability-and-noise.md`](results/44-stability-and-noise.md) | **The §4.2 noise-resilience evidence, and the instability question.** How far each ranking survives coordinate noise, edge loss, source loss and a shortened coherence window. The top-5 list is far less stable than the endpoint **for every method, including pure geometry**, and for the newer quantum families it is gone (`connectivity_strength`: AUC 0.625, top-5 Jaccard **0.05**). Rank-mean ensembling is the one measured remedy (stability 0.581 → 0.888). A spectrally normalised clock is **not**, and §6 says why. §7 shows stability and the distance confound are close to one quantity (**+0.874** inside the quantum family) |
| [`results/48-adaptation-feasibility.md`](results/48-adaptation-feasibility.md) | **Before proposing anything that adapts the pipeline to the protein.** The feasibility bound, and it is arithmetic rather than opinion. **The per-protein effect is real** — blocked on scorer, classical permutation p = **0.00007** over 42 scorers, median per-scorer arm spread **0.338**. §1 said the opposite until 2026-08-27 and records why it was wrong. What closes the route is the sample: at four arms the minimum attainable two-sided Spearman p is **0.083**, so a rank test over proteins has power **exactly zero at any effect size**. A 30-descriptor screen returned **1** perfect ordering against **2.50** expected. 80 % power needs **8** proteins for one pre-registered descriptor and **13** for a screen of 30, while the held-out tier holds **5** and delivers power **0.25**. Also carries the two zero-cost screens from review 19: AUC rank-invariance, and the sensitivity bound that predicted the gap clock's failure |
| [`results/49-worst-case-selection.md`](results/49-worst-case-selection.md) | **Selecting for generalisation rather than for the average.** The 69-scorer battery re-ranked by worst-arm AUC, between-arm spread and minimax regret. The (mean, worst) Pareto frontier holds **three** scorers; `gnm_fluctuation` buys **+0.075** of worst arm for **0.009** of mean over `eigenvector_centrality`. **But leave-one-arm-out says selecting on the worst arm does not improve the held-out worst arm** (0.5632 vs 0.5639) and costs 0.058 of held-out mean. Variance decomposition: the arm is **1.15 %** as a main effect and **60.3 %** through interactions, the graph **0.17 %**. The oracle gap is **+0.116**, and most of it is knowing whether to use distance or its inverse |
| [`results/50-adaptation-evidence-map.md`](results/50-adaptation-evidence-map.md) | **The map, once five documents disagree.** Eight convergences with their independence labelled — four are one fact counted several times — and **eight named conflicts, none averaged away**. The central one: "no per-protein effect" and "the arm is 60.3 % of the variance" measure **level** against **interaction**, both true, and which one a route aims at decides whether it has anything to fix. Ten routes, each with a kill condition and an inversion recipe. Ends with eight open questions and no answers |
| [`results/51-adaptation-constraint-audit.md`](results/51-adaptation-constraint-audit.md) | **Before implementing any adaptation route.** A design-stage ruling on seven proposals against C1, C2 and the frozen protocol. Worst-arm AUC as a **reported column** is admissible; as a **promoted endpoint** it is **forbidden**, because the re-freeze window shut when the first method was scored. It also found two live leakage routes that the guard could not see, both since closed: the matched-patch cache was unprotected, and a submodule import executes its parent package |
| [`results/52-derived-cutoff-prescreen.md`](results/52-derived-cutoff-prescreen.md) | **Before proposing a derived graph rule.** The cheap half of review 19's pre-screen, run on nine arms across a 5.2-fold size range. All three derived cutoff rules fail, in two different ways: Maxwell counting returns **3.85 to 4.15 A** (SD 0.092) and is a global constant in disguise, while the two that do vary track **protein size** (Spearman +0.72 and **+0.85**). The graph side has no spread to normalise |
| [`data/30-frozen-graph-profile.md`](data/30-frozen-graph-profile.md)     | Any question about the inputs themselves. It overturns one of the two spectral facts the Phase-2 plan was built on                                               |
| [`lit/`](lit/README.md)                                                  | You want the evidence behind a candidate. Seven new sweeps over fields `../review/` did not cover                                                                |

---

## What is here that was not here before

**Code.** Three new packages on the prediction path, none of which existed on 2026-08-25:

```
src/allo/network/     stage S1 -- the residue graph, with three orthogonal knobs
src/allo/classical/   stages S3-S7 -- the baseline battery, the coupling measures,
                      and the confound-removal and site-assembly stages
src/allo/quantum/     stage S5 -- Hamiltonians and propagation observables
```

**Experiments.** Four, all on the secondary set's `development` tier and nowhere else
(ADR 0012, ADR 0021):

```
experiments/2026-08-26-method-sweep/       the screen -- 8 graphs x 54 scorers x 3-5 detrends
experiments/2026-08-26-mechanism-probe/    three signatures read off the mechanism literature
experiments/2026-08-26-fusion-probe/       label-blind consensus, smoothing, top-5 assembly
experiments/2026-08-26-selection-power/    what the screen's best number means
```

**Six constructions the prior work never tested.** Established by the audit behind ADR 0026,
and each implemented here:

Each row now carries what it measured. `best` is the best mean AUC over the four arms across
all graphs and confound-removal forms. `rej` counts arms that reject the matched-patch null at
0.05, out of four. **None of the six reaches three.**

| Construction                               | Why it was open                                                                                                    | Where                                                | Measured                       |
| ------------------------------------------ | ------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------- | ------------------------------ |
| Effective resistance to the source         | The prior work computes `L⁺` but never forms `R_ij`                                                                | `classical.baselines.effective_resistance_to_source` | best **0.721**, rej 1, ρ 0.74 |
| A non-Hermitian sink at the active site    | Ruled out on structural grounds, never measured                                                                    | `quantum.walk.quantum_survival_time`                 | best 0.572, rej 0, ρ 0.81 |
| Lindblad dephasing **with a trap**         | Their ENAQT is pure dephasing with no sink — the canonical figure of merit minus the term that creates its optimum | `quantum.walk.dephased_transport`                    | best 0.484, rej 0, ρ 0.80 |
| Szegedy / quantum PageRank                 | Their `qpr` is "quantum perturbation response", a name collision                                                   | `quantum.walk.szegedy_quantum_pagerank`              | best 0.617, rej 0, ρ 0.76 |
| Edge-class-weighted graphs                 | Their arrays carry no residue identity, so hydrogen bonds and salt bridges are not derivable from them             | `network.build(weighting="edge_class")`              | best 0.772, **7th of 8 graphs** |
| Anisotropic perturbation-response scanning | Their `prs` is the scalar GNM form                                                                                 | `classical.baselines.anm_perturbation_response`      | best 0.358, **below chance** |

**The verdict on all six is the same.** Each was open, each was measured, and none produces a
method. Five are largely distance scores — the mean |ρ| against negated distance runs from
0.74 to 0.81 for four of them — and the matched-patch null absorbs exactly that. The two that
are not distance scores, `anm_perturbation_response` and the edge-class graph, do not beat the
plainer constructions they were meant to improve on.

**That is a result, not a disappointment.** Each was an open question that the prior work's
own evidence could not close (ADR 0026), and each is now closed by a number on this benchmark.
The numbers live in [`results/40-method-sweep.md`](results/40-method-sweep.md); the resource
account for the quantum three is in
[`results/43-quantum-resources.md`](results/43-quantum-resources.md).

---

## The rules this directory works under

Unchanged from `../review/00-conventions.md`, and repeated because they bind every file here.

- **Every number comes from `allo.scoring.score_arm`.** No experiment computes its own AUC,
  its own null or its own p-value. A quantum number that beats a classical number computed
  differently is not evidence.
- **Every hyperparameter is chosen on `development` and nowhere else.** The primary benchmark
  is scored once, with the choice already fixed, and the `generalisation` tier is not opened
  until the method is frozen (Phase 5).
- **A screen is a screen.** Selecting the best of several thousand variants on four arms is
  selection, and `results/41-selection-and-power.md` measures how much. No file here calls a
  screen result a finding.
- **Evidence tags are load-bearing.** `[VERIFIED-FULLTEXT]`, `[VERIFIED-ABSTRACT]`,
  `[UNVERIFIED]`, exactly as `../review/00-conventions.md` §2 defines them.
- **The five leakage paths stay closed.** Nothing here opens `docs/benchmark/*/frozen.json`,
  either manifest, `selection.json`, `extension-candidates.md`, or anything under
  `docs/benchmark/evaluation/`.
