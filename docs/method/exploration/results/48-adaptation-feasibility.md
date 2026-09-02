# 48 — Per-protein adaptation: what four proteins can and cannot establish

**Analysis, not an experiment.** Every number below comes from records already in
`experiments/`, from `docs/method/exploration/data/frozen-graph-profile.json`, or from an
exact permutation calculation. No new scoring ran.

The question this session opens is: adapt the pipeline to each protein, so that it
generalises. Before choosing a route, one thing has to be settled. **Per-protein adaptation
is a model with parameters, and it has to be fitted on something.** This document establishes
what our tuning set can support. The answer bounds every route in documents 17, 18, 19 and
49, so it belongs first.

---

## 1. The per-protein effect is real, and the first version of this section said it was not

> **Corrected 2026-08-27.** The first version of this section applied a Hanley-McNeil
> standard error for a **single** AUC to the spread of a **44-scorer family mean**, concluded
> that the classical spread of 0.175 was 1.04x the noise floor at P = 0.43, and titled itself
> "the variance is not real". Two independent reviews flagged the same error, the deflation
> factor was then measured, and the conclusion reverses. The corrected analysis is below. The
> superseded table is kept at the end of this section, because the mistake is instructive and
> because three other documents quote its numbers.

Per-arm mean AUC over the 69 scorers of `2026-08-26-beats-distance`:

| Arm | N | All 69 | Classical (44) | Quantum (25) |
| --- | --- | --- | --- | --- |
| `mkp5` | 147 | 0.626 | 0.638 | 0.604 |
| `ptp1b` | 298 | 0.464 | 0.463 | 0.465 |
| `hiv_rt` | 543 | 0.659 | 0.632 | **0.708** |
| `ns5b` | 553 | 0.463 | 0.528 | **0.347** |
| **Spread** | | **0.196** | **0.175** | **0.361** |

### 1.1 Why the first null was the wrong null

A Hanley-McNeil standard error describes **one** AUC estimated against 11 to 16 positives. It
is 0.071 to 0.093 on our arms. Applying it to the spread of a family **mean** assumes the
scorers in the family are perfectly correlated, so that averaging 44 of them removes no noise
at all. That assumption was never stated and it is false.

The mean pairwise Spearman correlation inside the classical family, measured on the
evaluation-default graph over each arm's candidate pool, is **+0.128** across the four arms.
It is not near 1. For an equicorrelated family the mean's standard error is

`SE(mean) = SE(single) * sqrt(rho_bar + (1 - rho_bar) / K)`

which at `rho_bar = 0.128` and `K = 43` gives **0.385**. **The floor used in the first version
was about 2.6 times too wide**, so the P = 0.43 it produced was an upper bound on a p-value
and not a p-value. The direction of the error ran against the conclusion drawn from it.

### 1.2 The right test keeps the pairing, and it has an exact null

The deeper problem is not the size of the floor. It is that collapsing 44 scorers into one
mean per arm throws away the design. **Every scorer is measured on every arm**, so the arm
effect is testable by a blocked test that never needs an analytic standard error at all.

Permute the four arm labels **within each scorer**, 200 000 times, and ask how often the
spread of the resulting family means reaches the observed one. The null is exactly "the arm
carries no level effect". On the `evaluation_default` graph with `raw` scores:

| Family | K | Family-mean spread | Blocked permutation p | Friedman chi2 (df 3) | p |
| --- | --- | --- | --- | --- | --- |
| classical | 42 | 0.190 | **0.00007** | 14.37 | **0.0024** |
| quantum | 11 | 0.541 | **< 0.000005** | 24.71 | 1.8e-05 |
| all | 53 | 0.237 | **< 0.000005** | 26.68 | 6.9e-06 |

**The arm level effect is real for the classical family, and the evidence is strong.** Mean
within-scorer arm rank puts `hiv_rt` at 2.88 and `ptp1b` at 1.90 out of 4: the ordering is
consistent scorer by scorer, which is what the blocked test detects and what a family mean
against an inflated floor could not.

The per-scorer arm spread has median **0.338** in the classical family. That is not a small
effect hidden by noise. It is a large effect that the first analysis mismeasured.

### 1.3 What reverses, and what does not

**Reverses.** The claim that there is no per-protein effect for the family that predicts.
There is one, at p = 0.00007.

**Does not reverse — and this is the point of the document.** Sections 2 and 3 never used
this section's result. Detecting **that** arms differ is a blocked test with 42 scorers of
replication. Predicting **which** arm is which from an apo descriptor is a rank correlation
over four points, and §2 shows it has power exactly zero. The two questions have different
sample sizes because they have different units of replication: the scorer for the first, the
protein for the second.

So the conclusion is not weakened. It is sharpened, and it is worth stating in its corrected
form because it is a better sentence than the one it replaces:

> **There is definitely something to adapt to, and four proteins definitively cannot tell us
> what it is.**

That is a statement about the sample, not about the phenomenon. It makes the sample size the
binding constraint and it makes §4's arithmetic the operative result of the document.

### 1.4 Where the effect is not

It is **not fold family.** `mkp5` and `ptp1b` are both phosphatases and land on opposite
sides. `hiv_rt` and `ns5b` are both viral polymerases and land on opposite sides. Whatever
separates easy from hard, it crosses both families in our set.

It is **not the graph**, and this is now measured twice. `30-frozen-graph-profile.md` §3.3
found that across a 7.2-fold size range the mean contact number spans 8.9 to 10.3 and mean
clustering 0.460 to 0.515. `52-derived-cutoff-prescreen.md` then solved three derived contact
cutoffs on nine arms and found the one genuinely derived rule returns 3.85 to 4.15 Angstrom on
every protein, a standard deviation of 0.092 Angstrom. **The graph side has no between-protein
spread to normalise.**

The **source geometry** is what varies: active-site size 3 to 61 residues, median
candidate-to-source distance 7.6 to 23.9 Angstrom, and a between-arm AUC spread of 0.486 for
the catalytic source against 0.109 for a size-matched random one (`45-source-choice.md` §3).
That is where §6 sends the remaining effort.

### 1.5 The superseded analysis, kept

Three other documents quote these numbers, so they are recorded rather than deleted. **Do not
cite them.** The floor is about 2.6x too wide because it assumes perfectly correlated scorers.

| Family | Observed spread | Multiple of the too-wide floor | P under one common AUC |
| --- | --- | --- | --- |
| classical (44) | 0.175 | 1.04x | 0.43 |
| all 69 | 0.196 | 1.17x | 0.33 |
| quantum (25) | 0.361 | 2.15x | 0.011 |

The per-arm Hanley-McNeil standard errors themselves are correct and remain useful for any
statement about a **single** scorer's AUC on a **single** arm: `mkp5` 0.0934, `ptp1b` 0.0866,
`hiv_rt` 0.0755, `ns5b` 0.0713.

---

## 2. At four proteins the test cannot reject, at any effect size

A per-protein adaptation rule maps a structural descriptor to a method choice. To establish
one, a descriptor has to be shown to track difficulty. That is a rank correlation over arms,
and at four arms it has an exact null with 24 permutations.

| Arms | Permutations | Smallest attainable two-sided p |
| --- | --- | --- |
| 4 | 24 | **0.0833** |
| 5 | 120 | 0.0167 |
| 6 | 720 | 0.00278 |
| 7 | 5040 | 0.000397 |
| 8 | 40320 | 0.0000496 |

**At four arms the smallest p any descriptor can produce is 0.083.** A perfect ordering of
all four proteins does not reach 0.05. The power of the test is therefore **exactly zero**,
and it is zero for a true rank correlation of 0.95 as surely as for one of 0.20. This is not
a small-sample weakness to be noted and worked around. It is an arithmetic ceiling.

---

## 3. We ran the screen anyway, and it produced exactly what noise produces

30 apo-only descriptors from `frozen-graph-profile.json` have four distinct values across the
development arms. Each was correlated against per-arm mean AUC.

**One descriptor ordered all four arms perfectly:** whole-protein mean relative solvent
accessibility, at 0.275 (`hiv_rt`) > 0.250 (`mkp5`) > 0.222 (`ptp1b`) > 0.220 (`ns5b`),
against difficulty 0.659 > 0.626 > 0.464 > 0.463.

It is tempting. It is also nothing:

| Quantity | Value |
| --- | --- |
| Descriptors screened | 30 |
| Perfect orderings observed | **1** |
| Perfect orderings expected by chance | **2.50** |
| P(at least one perfect, all null) | **0.93** |

Under the null, each descriptor has probability 2/24 = 0.083 of ordering four arms perfectly.
Over 30 descriptors the expected count is 2.50. **We observed fewer perfect orderings than
chance produces**, and a Poisson tail at that rate puts P(one or fewer) at 0.287. The screen is
not weak evidence for the solvent-accessibility descriptor. It is evidence that the screen is
uninformative.

Document 49 ran the same screen over a wider descriptor set, K = 37, and reached the same
place: 3.08 perfect orderings expected, one observed.

Note also that the descriptors are not independent — many are functions of size or density —
so the effective number of tests is below 30 and the expectation above is an upper bound on
how much correction is needed. That direction does not help. It means the screen resolves
even less than the table implies.

---

## 4. The sample size that settles it

Power to detect a descriptor-difficulty rank correlation, by exact permutation test up to
n = 8 and by the asymptotic test above it. Two regimes, and the difference between them is
the whole design decision.

**Regime A — screen many descriptors, correct for it.** Bonferroni over 30 candidates:

| True rank correlation | Proteins needed for 80% power |
| --- | --- |
| 0.95 | 10 |
| 0.90 | 13 |
| 0.80 | 19 |
| 0.70 | **28** |

**Regime B — pre-register one descriptor, test it once.** No correction needed:

| True rank correlation | Proteins needed for 80% power |
| --- | --- |
| 0.95 | **6** |
| 0.90 | **8** |
| 0.80 | 11 |
| 0.70 | 15 |

**The gap between the two tables is the cost of looking.** A single descriptor named in
advance needs 8 proteins to establish a strong relationship. The same relationship found by
screening 30 needs 13. We have 4 for tuning.

---

## 5. What the benchmark can actually supply

> **Corrected 2026-08-27.** The first version of this section summed the primary five into a
> "held-out total" of ten, one row after its own table called them "never a tuning surface".
> Both statements cannot hold. The constraint audit
> (`51-adaptation-constraint-audit.md`, P3) named the contradiction and the arithmetic is
> restated below at the honest N.

| Set | Arms | Status for this question |
| --- | --- | --- |
| `secondary/development` | 4 | The tuning set. Burned by construction (ADR 0012) |
| `secondary/generalisation` | 5 | Closed until the method is frozen. **The only genuinely available surface** |
| `primary` | 5 | The confirmatory family, and not a tuning surface at any point. Spending it on a descriptor question spends the submission's own result |

**So the number is 5, not 10.** The primary set cannot be both the confirmatory endpoint and
the sample that decides a hyperparameter question. The evaluation protocol admits exactly one
across-target decision at full alpha, and that decision is already committed.

**And five is not enough.** Exact permutation power for one pre-registered descriptor against
per-arm difficulty, 20 000 replicates per cell, two-sided at 0.05:

| n | Minimum attainable p | rho = 0.95 | rho = 0.90 | rho = 0.80 | rho = 0.70 |
| --- | --- | --- | --- | --- | --- |
| 4 | 0.0833 | **0.000** | **0.000** | **0.000** | **0.000** |
| 5 | 0.0167 | 0.378 | **0.251** | 0.140 | 0.095 |
| 6 | 0.0028 | 0.702 | 0.533 | 0.332 | 0.220 |
| 7 | 0.0004 | 0.888 | 0.753 | 0.519 | 0.366 |
| 8 | 0.0000 | 0.951 | **0.850** | 0.621 | 0.433 |
| 10 | 0.0000 | 0.990 | 0.947 | 0.782 | 0.592 |

**At the five arms actually available, power is 0.25 against a true rank correlation of 0.90
and 0.10 against 0.70.** Reaching 80 % needs **eight** arms at 0.90, and the benchmark does
not hold eight arms that are free to spend.

Read against §4 this is not a bleak result. It is a design, and the design has a gap.

**Regime A is unavailable and will stay unavailable.** Screening descriptors on four arms
cannot establish anything, and no amount of care changes the arithmetic. A rule found that
way is a rule fitted to four points.

**Regime B is available once and is underpowered when it is spent.** Five held-out arms give
a one-in-four chance of detecting a rank correlation of 0.90, which is a strong effect. A
negative result from that experiment would carry almost no information, and a positive one
would rest on a perfect or near-perfect ordering of five points. **This is the finding that
decides the recommendation**: the pre-registered route is not a cheap fallback, it is a
low-power experiment that consumes an irreplaceable resource.

---

## 6. What this rules out, and what it leaves

**Ruled out on arithmetic, not on taste.**

- A fitted per-protein selector — a model that reads descriptors and picks a method or a
  hyperparameter. It needs a training set and we do not have one. Document 18 gives the
  literature's own instance counts for comparison.
- Any adaptation rule whose parameters were chosen by looking at which choice scores better
  across the four development arms. That is selection on the outcome with four points, and
  `2026-08-26-selection-power` already measured what selection produces at this scale.
- Reporting the solvent-accessibility ordering as a finding. It is below chance.

**Left open, and each is testable.**

1. **Derived normalisation with zero fitted parameters.** A rule that makes a hyperparameter
   mean the same physical thing on every protein, taken from theory rather than from our four
   arms. Document 19 surveys the candidates and ranks eleven of them. These are admissible
   because they add no free parameters, so §4 does not bind them.

   Document 19 also supplies two screens that cost nothing and remove most of the field:

   - **Rank invariance.** Our endpoint is an AUC over midranks and our deliverable is a top-5
     list. Both are unchanged by any strictly increasing map applied to one protein's whole
     score vector. So `s/N`, `s/λ_max` and a per-protein z-score of the vector are **no-ops
     for the primary endpoint**. Only three classes of rule can move it: a rule that changes
     the operator or its hyperparameter, a rule that acts differently on different residues,
     and a rule that changes the evaluation strata. The size-normalisation literature is
     mostly the first class, and it stays relevant to reporting and to pooled figures, not to
     the score.
   - **The sensitivity bound.** A rule that only slides a hyperparameter `θ` moves each
     protein along its own `A(p, θ)` curve. So it can change any between-protein spread
     statistic by at most about `2·R_within`, where `R_within` is the endpoint's largest
     within-protein swing over the reachable `θ`. Measure `R_within` and the between-protein
     spread of the quantity the rule equalises **before** scoring anything. A rule needs both
     to be large.

   The bound is not retrospective bookkeeping: it predicts the one failure we already have.
   The gap-scaled clock in `2026-08-26-timescale-normalisation` equalises a quantity that
   varies 21.7x between arms, but `R_within` for `ctqw_average_transfer` is 0.079 AUC against
   a between-arm spread of 0.668. The bound permits at most about 0.16 of spread reduction.
   The measured reduction was 0.011, and the between-to-within variance ratio got worse, 8.5x
   to 14.5x, because the clock shrank the denominator and left the numerator alone. **The
   pre-screen would have cost one afternoon and saved the sweep.** It is now the entry gate
   for every rule in this class.
2. **Adaptation avoidance.** Instead of adapting to the protein, choose the observable whose
   between-arm variance is lowest to begin with. This needs no fitting at all and it is
   measurable on data we already have. Document 49 does that measurement.
3. **One pre-registered rule, tested once on the held-out ten.** The only route in §4's
   Regime B. The rule and the endpoint go into an ADR before the tier opens.

**Where the headroom is, if it is anywhere.** The two screens point at the same place. The
graphs are near-universal objects across a 7.2-fold size range — mean contact number 8.9 to
10.3, clustering 0.460 to 0.515 (`30-frozen-graph-profile.md` §3.3) — so a rule that
normalises the graph has almost nothing to equalise. The **source geometry** varies 20-fold
in size and 3.1-fold in median candidate-to-source distance, and `45-source-choice.md` §3
measured the consequence: the catalytic source has a between-arm AUC spread of 0.486, the
largest of six source families, against 0.109 for a size-matched random source. Document 19's
top two candidates both act there. A per-residue z-score against a size- and degree-matched
random-source ensemble passes the rank-invariance screen because it is per-residue.
Radial-quantile stratification passes it because it changes the strata. Neither is run yet.

**And one measurement suggests the prize is too small to chase.** Document 49 computes the
oracle: a selector that picks the best scorer for each arm reaches mean AUC 0.876 against
0.759 for the single best scorer, a gap of **+0.116**. Restricted to scorers that are not
distance rankings, the gap falls to **+0.040**, and against a null that selects the same way
it is about **+0.03**. Document 41 §5 puts the minimum detectable AUC on this benchmark at
0.794 to 0.955. **A perfect per-protein selector wins an amount comparable to what we cannot
measure.** Document 18 finds the same shape in the algorithm-selection literature: on bounded
quality metrics the virtual-best to single-best ratio is 1.02 to 1.7, against 11 to 265 for
runtime metrics, and in the one scenario shaped like ours — 105 instances, 30 candidates, a
bounded metric — six of eight submitted selectors did no better than the single best.

**One question that decides how much any of this can work.** If per-arm difficulty is a
property of the apo→holo transition rather than of the apo structure, then no apo-only
descriptor can predict it. We cannot test this. Such a test opens the holo structures on the
prediction side, which C1 forbids. It is recorded here as the assumption every adaptation
route rests on, and it is currently **unknown**.

---

## 7. What this document supports and what it does not

**Supported.**

- The between-arm spread is 0.196 over all scorers, 0.175 classical and 0.361 quantum, and
  it does not follow fold family in our set.
- **There is a real per-protein level effect**, blocked on scorer: classical permutation
  p = 0.00007 over 42 scorers, Friedman p = 0.0024. The median per-scorer arm spread is 0.338.
- The mean pairwise Spearman inside the classical family is +0.128, so a family mean's
  standard error is 0.385 of a single scorer's, not equal to it.
- At four arms a rank test over proteins has power exactly zero, because its minimum
  attainable p is 0.083.
- The 30-descriptor screen produced 1 perfect ordering against 2.50 expected by chance.
- A single pre-registered descriptor needs **8** proteins for 80 % power at a true rank
  correlation of 0.90. A screen of 30 needs about 13. **At the 5 arms actually available the
  power is 0.25** at 0.90 and 0.10 at 0.70.
- Any normalisation that applies one strictly increasing map to a protein's whole score
  vector cannot change our AUC or our top-5 list. This is arithmetic, not a measurement.
- A rule that only slides a hyperparameter cannot reduce between-protein spread by more than
  about twice the within-protein endpoint range over the reachable settings. The gap clock
  obeys the bound: permitted 0.16, delivered 0.011.

**Not supported.**

- No claim that mean relative solvent accessibility predicts difficulty. The screen that
  produced it is uninformative by its own multiplicity arithmetic.
- **No claim that the per-protein effect is absent.** §1 said that until 2026-08-27 and it
  was wrong. The effect is real; what is absent is any way to learn its rule from four
  proteins.
- No claim about what the per-protein effect *is*. The blocked test says the arms differ in
  level. It says nothing about which apo property that difference tracks.
- No claim about which route in §6 will work. This document bounds the design space and
  ranks nothing inside it.
- No claim that ten held-out arms are enough. They are enough for a true rank correlation
  near 0.90 and not for one near 0.70, and we do not know which regime we are in.
- The power figures for n above 8 use the asymptotic Spearman test rather than exact
  enumeration, because 9! permutations per replicate is not affordable. They are simulation
  estimates with a Monte Carlo error of roughly one point at 2500 replicates.
