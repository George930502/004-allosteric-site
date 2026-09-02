# 0028 — Per-protein adaptation is not testable at four arms, and no fitted rule enters the pipeline

**Status:** accepted · 2026-08-27

## Context

Phase 2 measured that a single fixed pipeline is good on one protein and poor on another.
The principal investigator's direction was to adapt the pipeline to the input protein, and to
consider an AI preprocessing stage that reads the structure and selects the method or the
hyperparameter. ADR 0027 already removed the constraint objection: a tier A component is
admissible without qualification.

The remaining objection is not a constraint. It is arithmetic, and it is decisive.

**Four measurements settle it, and the first is not the one this ADR was drafted around.**
The effect adaptation aims at is real. What fails is our ability to learn its rule. All four
are on the four `development` arms and all use `allo.scoring.score_arm`.

1. **The per-protein effect is real, and that is not what closes the route.** Every scorer is
   measured on every arm, so the arm effect is testable by permuting arm labels within each
   scorer. Over 200 000 permutations on the `evaluation_default` graph the classical family
   gives p = **0.00007** across 42 scorers, Friedman p = 0.0024, with a median per-scorer arm
   spread of **0.338**. The arms differ, and they differ consistently scorer by scorer.
   [`docs/method/exploration/results/48-adaptation-feasibility.md` §1.2]

   An earlier version of that section concluded the opposite, by applying a single-AUC
   Hanley-McNeil standard error to a 44-scorer family mean. The mean pairwise Spearman inside
   that family is **+0.128**, so the family mean's standard error is **0.385** of a single
   scorer's and the floor used was about 2.6 times too wide. The error is recorded in §1.5 of
   that document rather than deleted, because three other files quote its numbers.

2. **At four arms a rank test over proteins has power exactly zero.** Four arms give 24
   permutations, so the minimum attainable two-sided Spearman p is **0.0833**. No effect size
   reaches 0.05. The floor falls below 0.05 only at n = 5, and below a Bonferroni threshold
   for 30 descriptors only at n = 7.
   [`48-adaptation-feasibility.md` §2, `docs/method/review/18-selection-sample-complexity.md`
   §5]

3. **The screen ran anyway, and returned less than chance.** Thirty apo-only descriptors were
   correlated against per-arm difficulty. One produced a perfect ordering. The chance
   expectation over 30 descriptors is **2.50**, and P(at least one) = **0.93**.
   [`48-adaptation-feasibility.md` §3]

**The field reports the same shape.** In the one algorithm-selection scenario shaped like
ours — `OPENML-WEKA-2017`, 105 instances, 30 candidates, a bounded quality metric — the
virtual-best to single-best ratio is **1.02**, and six of eight submitted selectors did no
better than the single best solver. The Gupta-Roughgarden sample-complexity bound is vacuous
at m = 4: it buys an error of about the whole range of the metric.
[`18-selection-sample-complexity.md` §§2, 4]

4. **The held-out tier is five arms, and five arms are underpowered.** The primary set is the
   confirmatory family and cannot also be the sample that settles a hyperparameter question,
   so the only genuinely available surface is `secondary/generalisation`. Exact permutation
   power for one pre-registered descriptor at n = 5 is **0.25** against a true rank
   correlation of 0.90 and **0.10** against 0.70. Reaching 80 % needs **eight** arms at 0.90.
   [`48-adaptation-feasibility.md` §5, corrected after `51-adaptation-constraint-audit.md` P3]

**And the prize is small.** A per-arm oracle reaches mean AUC 0.876 against 0.759 for the
single best scorer, a gap of **+0.116**. Restricted to scorers that are not distance
rankings, the gap falls to about **+0.03**. The minimum detectable AUC on this benchmark is
0.794 to 0.955. A perfect selector wins an amount comparable to what the benchmark cannot
measure.
[`docs/method/exploration/results/49-worst-case-selection.md` §6,
`docs/method/exploration/results/41-selection-and-power.md` §5]

## Decision

**No fitted adaptation rule enters the pipeline.** A rule is fitted if any of its parameters,
thresholds, descriptor choices or method assignments was selected by comparing scores across
the `development` arms. Such a rule cannot be validated at n = 4, and this project will not
report one.

**Three routes stay open, and each has a stated gate.**

| Route | What it is | Gate before it runs |
| --- | --- | --- |
| **Derived normalisation** | A rule that fixes a hyperparameter from theory or from the protein's own structure, with zero free constants. Tier (i) and tier (ii) of `19-cross-protein-normalisation.md` §1.3 | Both screens in §1 of that review. See below |
| **Adaptation avoidance** | Choose the observable with the lowest between-arm variance instead of adapting to the protein. No fitting at all | None. It is a selection over the existing battery and is priced by `41-selection-and-power.md` |
| **One pre-registered rule** | A single rule and a single endpoint, written into an ADR, then tested once on the `generalisation` tier | The ADR exists and is accepted **before** the tier opens. `docs/benchmark/secondary/README.md` keeps the tier closed until the method is frozen. **Note the power: 0.25 at rho = 0.90 over five arms.** This route spends an irreplaceable resource on a low-power test, and a negative result from it carries almost no information |

**Every derived normalisation must pass two screens before it is implemented.** Both are
zero-cost and both come from `19-cross-protein-normalisation.md` §1.

- **Rank invariance.** Our endpoint is an AUC over midranks and our deliverable is a top-5
  list. A strictly increasing map applied to one protein's whole score vector changes
  neither. A rule of the form `s/N`, `s/λ_max` or a per-protein z-score of the vector is a
  **no-op for the primary endpoint**. Such a rule is admissible for reporting and for pooled
  figures, and it must not be proposed as a method change.
- **The sensitivity bound.** A rule that only slides a hyperparameter `θ` moves each protein
  along its own `A(p, θ)` curve. It can change any between-protein spread statistic by at
  most about `2·R_within`, where `R_within` is the endpoint's largest within-protein swing
  over the reachable `θ`. Measure `R_within` and the between-protein spread of the quantity
  the rule equalises **before** scoring anything.

**The gap clock is the worked example and it is the bar.** It equalises a quantity that varies
21.7x between arms, but `R_within` for `ctqw_average_transfer` is 0.079 AUC against a
between-arm spread of 0.668. The bound permits at most about 0.16 of spread reduction. The
measured reduction was **0.011**, and the between-to-within variance ratio worsened from 8.5x
to 14.5x. The pre-screen predicts that failure on paper. Do not re-propose a spectral clock.
[`docs/method/exploration/results/44-stability-and-noise.md` §6]

**Where the headroom is.** The graphs are near-universal across a 7.2-fold size range: mean
contact number 8.9 to 10.3, clustering 0.460 to 0.515. A rule that normalises the graph has
almost nothing to equalise. The **source geometry** varies 20-fold in size and 3.1-fold in
median candidate-to-source distance, and the catalytic source has the largest between-arm AUC
spread of six source families, 0.486 against 0.109 for a size-matched random source. A
derived rule must act on source geometry, or state why it does not.
[`docs/method/exploration/data/30-frozen-graph-profile.md` §3.3,
`docs/method/exploration/results/45-source-choice.md` §3]

## Consequences

**What this blocks.** Any learned per-protein selector, any descriptor-driven method switch,
and any hyperparameter rule tuned by comparing arms. ADR 0027 admits tier A and tier B
components on provenance grounds. This ADR blocks a subset of them on statistical grounds,
and the two are independent tests. A component must pass both.

**What this does not block.** A learned component that computes a **feature** used identically
on every protein. That is not adaptation. It is one more fixed pipeline, and it is scored the
same way as any other.

**What the report must say.** The between-protein variance is reported as a **real and
measured effect**, with the blocked permutation p beside it, and immediately followed by the
statement that no rule for it can be learned from this benchmark. The report must not claim
that any descriptor predicts difficulty, and it must not claim the variance is noise.

**One methodological rule follows from how this ADR was nearly wrong.** A statistic computed
over a family of scorers must not be tested against a standard error derived for one scorer.
Where the design is paired — every scorer on every arm — the blocked test is the correct one
and it needs no analytic standard error at all. This binds every between-arm claim in the
project.

**What would reopen this.** Eight scored proteins for a single pre-registered descriptor, or
thirteen for a screen of 30, at a true rank correlation of 0.90. At 0.70 the counts are 15
and 28. The `generalisation` tier supplies **five** and the primary set is not available for
the question. That is not enough for a screen, and not enough for a well-powered single test
either. Reopening this needs **new arms**, admitted under ADR 0021's clauses. A re-analysis
of what we hold cannot do it.

**One assumption is untestable and is recorded as unknown.** If per-arm difficulty is a
property of the apo-to-holo transition rather than of the apo structure, then no apo-only
descriptor can predict it. Testing that opens the holo structures on the prediction side,
which C1 forbids. Every adaptation route rests on this assumption. It is **unknown**.
