# 50 — Per-protein adaptation: the evidence map and the option set

**Synthesis, no new scoring and no new retrieval.** Every number below is carried from one of five
documents written on 2026-08-26 and 2026-08-27, and every claim names the document and section it
came from. A claim with no source has been deleted rather than softened.

**The five:**
[`../../review/17-generalisation-variance.md`](../../review/17-generalisation-variance.md) (how far
performance moves between targets, in our data and in the field),
[`../../review/18-selection-sample-complexity.md`](../../review/18-selection-sample-complexity.md)
(how many instances a fitted per-instance selector needs),
[`../../review/19-cross-protein-normalisation.md`](../../review/19-cross-protein-normalisation.md)
(derived zero-parameter rules and the two screens that kill most of them),
[`48-adaptation-feasibility.md`](48-adaptation-feasibility.md) (what four tuning proteins can
establish), [`49-worst-case-selection.md`](49-worst-case-selection.md) (mean versus worst-case
objectives, the variance decomposition, the oracle gap).
Read against `../../../PRINCIPLES.md` R3 for the evidence standard and
[`42-threats-and-confirmation.md`](42-threats-and-confirmation.md) for the threat framing this
document extends rather than replaces.

**This document does not contain a recommendation.** §9 lists the open decisions as questions.

**Scope guard.** Only the four `development` arms — `mkp5`, `ptp1b`, `hiv_rt`, `ns5b` — and primary
arms are named. No `generalisation`-tier arm is named or scored anywhere below. No file under
`docs/benchmark/evaluation/`, no `selection.json` and no `extension-candidates.md` was opened.

---

## 0. The two sentences everything else qualifies

> **C2 was resolved by measurement on 2026-08-27, after this document was written, and the
> first of the two sentences below is now known to be wrong.** This document's §C2 flagged
> that `48` §1 applied a single-AUC Hanley-McNeil standard error to a 44-scorer family mean,
> and correctly reasoned that the error ran against the no-effect reading. The deflation
> factor was then measured: the mean pairwise Spearman inside the classical family is
> **+0.128**, so a family mean's standard error is **0.385** of a single scorer's and the
> floor used was about 2.6x too wide. Replacing the analytic floor with the blocked
> permutation the paired design allows — permute arm labels within each scorer, 200 000 times
> — gives classical **p = 0.00007** over 42 scorers, Friedman p = 0.0024. **The per-protein
> level effect is real.** `48` §1 is rewritten; its superseded numbers are kept in §1.5 there.
>
> **Nothing else in this document changes.** §C1's distinction between level and interaction
> still sorts the option set, and every route's kill condition stands. The corrected headline
> is: *there is definitely something to adapt to, and the benchmark definitively cannot tell
> us what it is.* Read the first sentence below as superseded and the second as intact.


**For the family that actually predicts anything, there is no demonstrated per-protein effect at the
level of the score.** The classical family's between-arm AUC spread is 0.175; the Hanley–McNeil noise
floor at 11–16 positives per arm gives an expected spread of 0.169 under a single common true AUC,
and P(spread this large) = **0.43** (`48` §1, calibrated in `17` §6).

**But the arm dominates the sweep through interaction, not through level.** Exact orthogonal
sums-of-squares on a balanced 5 184-record block put the arm at **1.15 %** as a main effect and
**27.26 %** as `arm × scorer`, with every arm-linked term summing to **60.3 %** (`49` §5).

These two sentences are both true and they are not in conflict. They are measurements of different
quantities, and **which of the two a route is aimed at decides whether it has anything to fix.**
Most of §2 is the consequence of people reading one as the other.

---

## 1. Where the five converge — and how independent each convergence is

Convergence is only evidence when the routes are independent. Four of the eight below are
independent; four are one fact cited several times, and are labelled as such.

| #      | The convergent claim                                                                                                                                                    | Documents                                                                                                                                                                                                                                                     | Independent?                                                                                                                                                                                                                                                                         |
| ------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **V1** | At n = 4 a rank test over proteins has power exactly zero: the smallest attainable two-sided p is `2/4! = 0.083`, and a clean sweep of paired wins gives `2/2⁴ = 0.125` | `18` §4–§5, `48` §2, `49` §9                                                                                                                                                                                                                                  | **No.** One combinatorial fact, derived three times. Its strength is that it is arithmetic, not that three files agree                                                                                                                                                               |
| **V2** | The apo-descriptor screen came back below the null                                                                                                                      | `48` §3 (K = 30, expected 2.50, observed 1), `49` §9 (K = 37, expected 3.08, observed 1), arithmetic re-derived in `18` §Q5                                                                                                                                   | **No, and this matters.** Both screens read the same `frozen-graph-profile.json`, K = 37 is a superset of K = 30, and the single perfect ordering is the same descriptor (mean relative solvent accessibility). This is **one** screen counted twice; it must not be reported as two |
| **V3** | A perfect per-protein oracle wins little, and most of what it wins is unreachable                                                                                       | `49` §7 (+0.1164 raw; +0.0755 at mean \|ρ\| < 0.45; +0.0397 at max \|ρ\| < 0.45; ≈ +0.03 against a selection-inflated null), `18` §Q3 (VBS/SBS factor **1.02, 1.04, 1.7** on the field's three bounded-quality scenarios against 10–413 on runtime scenarios) | **Yes.** One repo measurement and one literature regularity, arrived at independently. The strongest convergence in the set                                                                                                                                                          |
| **V4** | A fitted per-protein selector is not admissible at n = 4                                                                                                                | `18` §7 (four independent floors: combinatorial, paired-comparison, sample-complexity, empirical), `48` §6                                                                                                                                                    | **Partly.** `48` supplies repo arithmetic, `18` supplies theory (Gupta–Roughgarden ε ≈ 1.00 at m = 4) and field practice (smallest competed scenario 100 instances, smallest training set ≈ 67)                                                                                      |
| **V5** | The graph is not where the between-protein variance lives                                                                                                               | `19` N7 (mean contact number 8.9–10.3, clustering 0.460–0.515, adjacency λ₁ 10.40–11.80 across a 7.2× size range), `49` §5 (graph main effect **0.17 %** of sweep variance, on 7 df, against 27.26 % for `arm × scorer`)                                      | **Yes.** A structural profile and a variance decomposition, different data reductions, same conclusion                                                                                                                                                                               |
| **V6** | Source geometry is the thing that varies between our proteins                                                                                                           | `19` §Q3 (source size 3–61 residues, 20×; median candidate-to-source distance 7.6–23.9 Å, 3.1×; fraction of candidates within 10 Å 0.12–0.69; source mean RSA 0.017–0.268), `48` §1                                                                           | **No** — `48` quotes `19`'s source. The independent element is `45` §3, quoted by `19`: the catalytic source has the largest between-arm AUC spread of any source tested, **0.486** against **0.109** for a size-matched random source                                               |
| **V7** | A derived, zero-parameter rule needs a mechanism, not just statistical admissibility                                                                                    | `19` §1.2 and N1, `18` §Q6(c), `48` §6                                                                                                                                                                                                                        | **No.** All three trace to the single measurement in `44` §6: the spectral-gap clock cut within-arm window sensitivity 0.079 → 0.045, moved between-arm spread by **0.011** (2 % of itself), and made the between/within ratio **worse**, 8.5× → 14.5×                               |
| **V8** | The worst-case objective is the right objective and the least estimable one at n = 4                                                                                    | `18` §Q6(a) (predicted from theory: "a minimum over four values is a high-variance statistic"), `49` §4 (measured: leave-one-arm-out gives held-out worst 0.5632 against 0.5639 and costs **0.058** of held-out mean)                                         | **Yes, and in the strongest possible form.** `18` predicted the failure mode before `49` measured it. A prediction that survives its own test is worth more than two agreeing observations                                                                                           |

---

## 2. Where they conflict

Eight conflicts. None is averaged away below.

### C1 — "No per-protein effect" (`48` §1) against "the arm is 60.3 % of the variance" (`49` §5)

**The conflict as it will be quoted.** `48` §1: "For the family that actually predicts anything, we
cannot show [a per-protein effect]." `49` §5: "Every arm-linked term together is 60.3 % of the
variance." `49` §6: the arm-pair Spearman correlations reach p = 1.6 × 10⁻¹⁰.

**Resolution, and it holds.** The two measure different objects. `48` measures the spread of the
per-arm **mean AUC over a family of scorers** — a level. `49` measures the **interaction**: which
scorer is good on which arm. `49` §5 supplies the reconciliation itself — the arm main effect is
1.15 % and the per-arm means over the 54-scorer battery are 0.554, 0.531, 0.517, 0.489, a spread of
0.065. **The arm barely shifts the level and heavily reorders the methods.**

**What it decides.** Any route that equalises a per-protein _scalar_ has nothing to fix — there is
no level effect to remove. Any route that chooses a _different method per protein_ has a real target
and, by V1 and V4, no admissible way to aim at it. This single distinction sorts §3's option set into
two halves.

**Not resolved.** `49` §6's p-values are computed over 69 scorers, not over 4 arms, so the n = 4
floor does not apply to them — but the 69 scorers hold only 66 distinct four-arm profiles and about
8.86–10.58 effective directions (`49` §6, quoting `41` §4), and the arm-correlation matrix has a
participation ratio of **2.60**. `49` §6 says to read them as ordering evidence, not calibrated tail
probabilities. Nobody has computed what the effective-n correction does to p = 1.6 × 10⁻¹⁰.

### C2 — The noise floor is analytic, and it may be the wrong size for a family mean

**Both `17` §6 and `48` §1 apply a Hanley–McNeil standard error for a _single_ AUC estimate
(0.0934 / 0.0866 / 0.0755 / 0.0713, mean 0.082) to the spread of a per-arm mean over 69 scorers.**
`48` §1 simulates 200 000 times, but the simulation draws each arm's family mean from a normal with
that single-AUC SE.

**Why this is not obviously right.** All 69 scorers are evaluated against the same realised label set
on a given arm, so the label-draw component of the error is shared and does not average down — which
is the argument that makes the single-AUC SE approximately correct. But the scorer-specific component
_does_ average down, and the battery holds ~9–11 effective directions, not one. So 0.082 is an
**upper bound** on the SE of a family mean, the 0.169 expected spread is an upper bound on the noise
floor, and P = 0.43 is therefore a **lower bound on the extremeness** of the observed 0.175 — the
error is in the conservative direction for "no effect".

**This is not a new objection: `17` §"What this changes" item 2 already names the fix** — run the
matched-patch null draws already generated inside `allo.scoring.score_arm` and record the
**distribution of the max−min AUC spread across the four arms**. It costs one pass over existing
draws. `48` used the analytic floor instead. **The two have not been reconciled and the benchmark's
own null has never been read on this statistic.**

**Better grounded:** neither, yet. The analytic floor is exactly derived from a published formula
(doi:10.1148/radiology.143.1.7063747) under an assumption about the estimator that has not been
checked; the empirical floor would require no assumption and has not been computed.

### C3 — "Our spread is small by field standards" is partly a property of the metric

`17` §6 concludes that 0.175 "is far smaller than every per-target spread the field reports". `17`
§2 records what those field spreads are: CryptoSite per-protein **sensitivity** 0 %–100 %; CASP10
per-target **median MCC** −0.05 to 0.6. Neither is an AUC. And `17` §2 states the asymmetry itself:
the kinase PLM moves **AUROC 0.299** and **AUPR 0.672** between site classes on the same proteins,
and "AUROC is the axis least able to see composition change".

**So the field comparison compares our AUC spread to the field's non-AUC spreads on a metric the
same document says is the least sensitive one available.** `17` §2 also records the honest version:
no retrieved paper reports a between-target standard deviation of AUC for this task, so there is no
like-for-like comparator and will not be one from this literature.

**Resolution.** The only admissible external comparator `17` identifies is the single
AUC-to-AUC, same-method, two-benchmark delta: **PocketMiner 0.87 → 0.76, −0.11** (`17` §Q4). Our
0.175 spread over four arms and that −0.11 cross-benchmark drop are the two numbers that may sit in
the same sentence. Everything else in `17` §2 is context, not calibration.

### C4 — `49` measures worst-case selection failing, then recommends the worst-case winner

`49` §12 item 2: "Do not switch the selection rule to the worst arm." `49` §12 item 3: "If a single
scorer has to be frozen for a generalisation claim, `gnm_fluctuation` is the better-argued choice."
`gnm_fluctuation` is the scorer the worst-arm and minimax-regret objectives pick.

**Resolution, and it is real but narrow.** The recommendation is not a min-AUC argument. It costs
**0.0089** of mean AUC (0.7593 → 0.7505), which is a twentieth of the ±0.08 interval `17`
§"What this changes" item 4 puts on a four-arm mean, and it is simultaneously **#1 by minimax
regret** (0.176) and **#2 by mean** (`49` §1–§2). So it is nearly free under the incumbent objective
and best under a third. **A choice that is free under the objective you trust is not a switch of
objective.**

**Residual, stated because `49` §10 states it:** the choice was still made after seeing all four
arms, and neither `gnm_fluctuation` nor `eigenvector_centrality` rejects the matched-patch null on
more than one arm.

### C5 — `18` recommends ensembling on evidence `49` shows is silent about the objective

`18` §Q6(b) ranks "aggregate rather than select" third among its honest alternatives, and its repo
evidence is `44` §4: rank-mean ensembling over K = 16 jittered copies raises held-out **stability**
from 0.581 to 0.888 at a mean-AUC cost of −0.015.

`49` §8 measures **Spearman(stability, worst-arm AUC) = −0.007, p = 0.97**, against
Spearman(stability, mean AUC) = +0.354, p = 0.047. And it supplies the mechanism:
Spearman(stability, mean \|ρ\| to distance) = **+0.599** pooled and **+0.881** within the quantum
family — a stable score is a smooth function of coordinates, smoothness is what distance has, and
distance is precisely the component that **inverts** between the two arm clusters (`49` §5–§6).

**So the headline benefit of `18`'s third-ranked alternative is measured on an axis that is
uncorrelated with the objective this whole investigation is about.** `18` does carry the cost
honestly — the distance correlation rises 0.496 → 0.613 and K = 16 multiplies circuit executions
under C3 — but it does not know that the two are the same fact. **`49` §8 turns `18`'s caveat into
an objection.** This is the sharpest live conflict between two of the five documents.

**Unresolved and testable:** if ensembling buys stability by buying distance, and distance inverts
between clusters, the ensemble's **between-arm spread should rise**. Nobody has measured the K = 16
ensemble's four per-arm AUCs.

### C6 — `19`'s top-ranked candidate is not an adaptation rule

`19` §7 ranks the per-residue z-score against a size- and degree-matched random-source ensemble
first, because "both conditions of the §1.2 pre-screen are satisfied here and nowhere else". Its
supporting number is `45` §3's between-arm spread by source (0.486 catalytic against 0.109
size-matched random).

**But `19` §S6 says what the rule actually is:** "The per-residue matched-source z-score of §Q3.1
belongs [in S6], not in S5: it is a confound-removal step that happens to be derived from the source
rather than from distance."

**So the best-argued item on the normalisation list is a confound-removal step, and its correct
comparator is the paired test against the distance baseline (`46`), not the between-arm spread.** If
it is judged on between-arm spread it is being judged on the axis C1 says has no demonstrated effect.
`19`'s own falsifier for it is written both ways — "falsified if the between-arm AUC spread does not
fall by > 0.05, **or** if the mean \|ρ\| to negated distance rises above the unnormalised control's"
— and only the second clause tests what the rule is for.

### C7 — Ten held-out arms is not one sample of size ten

`48` §5 tabulates `secondary/generalisation` 5 + `primary` 5 = "**Held-out total 10**, available
once", and reads it against §4's Regime B power table (8 proteins for 80 % power at a true rank
correlation of 0.90).

**Three things break the arithmetic, and all three are recorded elsewhere in the repo.** `42` §4 step
4 scores the primary set with **Holm–Bonferroni across the three confirmatory arms** and with
`cavity_volume` as the required comparator rather than chance (ADR 0025) — a different test with a
different comparator from the generalisation tier's. The root operating contract records that all
three mandated apo/holo pairs are defective and are scored in tiers, and that **the cardiac myosin
pair is unscoreable as assigned**. And `48` §5 labels `primary` "Confirmatory. Never a tuning
surface" in the same table it adds into a power denominator.

**Resolution: `48` §5's "10" is an upper bound on a heterogeneous set, not an n for a Regime B power
calculation.** The number of arms that could carry a single pre-registered rank test under one
protocol is smaller than 10 and is not stated in any of the five documents.

### C8 — Numbers that disagree, or that name the same word for different objects

| Quantity                                 | Values in circulation                                                                                                                                                                                                                                                                                                                                                                        | Which is better grounded                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| ---------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| "between-arm spread"                     | **0.175 / 0.196 / 0.361** = spread of per-arm _family mean_ AUC (`48` §1); **0.334 / 0.205 / 0.068** = spread of _one scorer's_ per-arm AUC (`49` §1); **0.5627 → 0.5516** and **0.668 → 0.650** = spread over a _window sweep_ of one observable (`19` N1, quoting `44` §6); **0.486 / 0.109** = spread by _source choice_ (`19` §Q3, quoting `45` §3); **"0.49"** used loosely in `19` §N7 | All are correctly sourced; **none may be quoted against another**. Four distinct statistics share one phrase. The noise floor of 0.169 was computed for the first only                                                                                                                                                                                                                                                                                                                                                                    |
| Spectral gap ratio across arms           | **21.7×** (`19` §Q6, from `47` §1: gaps 0.0748–1.6244) against **140×** (`44` §6's own column, 0.01766–2.47385)                                                                                                                                                                                                                                                                              | Both `[VERIFIED-FULLTEXT]`; the tables report the gap of **different operators**. `19` records the discrepancy and does not reconcile it. Quote the figure with its operator attached or not at all                                                                                                                                                                                                                                                                                                                                       |
| Spectral range ratio                     | **1.09×** stated in both `19` §Q2 and `44` §6, against **1.20×** from `44`'s own table (17.968–21.631)                                                                                                                                                                                                                                                                                       | `19` flags it; the reconciliation is `[UNVERIFIED]`. Immaterial either way — both say the quantity the `range` clock equalises is already nearly equal                                                                                                                                                                                                                                                                                                                                                                                    |
| Arm size, "N"                            | `48` §1 prints N = 147 / 298 / 543 / 553; `17` §6 and `48` §1's second table use 136 / 287 / 534 / 550 candidates with 11 / 11 / 16 / 16 positives                                                                                                                                                                                                                                           | Both correct and both needed. Per ADR 0011 `n_residues` (what a method receives) ≠ `n_candidates` (what it is scored against); `48`'s first-table header "N" is the former. The SE arithmetic uses the latter, which is right                                                                                                                                                                                                                                                                                                             |
| The oracle reduction                     | The brief's "+0.116 falling to about +0.03 for scorers that are not distance rankings" merges two reductions that `49` §7 keeps apart: **+0.116 → +0.0755 → +0.0397** is a _distance-filter_ series over 69 → 26 → 11 scorers; **≈ +0.03** is a separate comparison of the observed 0.876 against a _selection-inflated label-blind null_ whose interval is 0.76–0.84                        | `49` §7 is better grounded because it keeps them separate. The two reductions have different mechanisms and **must not be composed**                                                                                                                                                                                                                                                                                                                                                                                                      |
| What the oracle gain is compared against | `48` §6 compares a **+0.03 gain** to the "minimum detectable AUC on this benchmark, 0.794 to 0.955" (`41` §5)                                                                                                                                                                                                                                                                                | This compares a _difference_ to an _absolute level_. `42` T6 states the same quantity as "the minimum detectable effect at 80 % power is AUC 0.762 to 0.936 at α" — the AUC a single method must **reach** to reject its null, not the difference between two correlated methods on shared arms. `46` runs a **paired** test whose minimum detectable _difference_ is a smaller and different number, and **no document in the set quotes it**. The rhetorical conclusion may well be right; the comparison as written is a category slip |

---

## 3. The option set

Ten routes. Six were named in the brief; four more are supported by the documents. Routes are
distinct when their failure modes are distinct, not when their implementations differ.

| #       | Route                                                                                                                                                                                | What it changes                                                          | The half of C1 it targets                                          | Load-bearing source                                                                                                                                                                                             |
| ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------ | ------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **R1**  | **Fitted per-protein selection.** Learn a map from apo descriptors to a method or a hyperparameter                                                                                   | The method, per protein                                                  | Interaction                                                        | `18` §7, `48` §6                                                                                                                                                                                                |
| **R2**  | **Derived zero-parameter normalisation.** A rule with no free constant that makes a hyperparameter mean the same physical thing everywhere                                           | A hyperparameter or an operator, per protein                             | Level (**R2a**, rank-invariant) or endpoint (**R2b**, non-uniform) | `19` §7, §1.1, §1.2                                                                                                                                                                                             |
| **R3**  | **Adaptation avoidance by low-variance observable.** Pick the observable whose between-arm variance is smallest to begin with                                                        | Nothing per protein; the choice of scorer                                | Neither — it declines the question                                 | `49` §2, `48` §6 item 2                                                                                                                                                                                         |
| **R4**  | **Source-geometry normalisation.** Per-residue z-score against a size- and degree-matched random-source ensemble; radial-**quantile** strata; a geometry clock; `s_AB` at site level | The score within each protein (R4 is four sub-rules with one motivation) | Interaction, via the confound                                      | `19` §Q3.1–Q3.4, §7 rows 1–3, 5                                                                                                                                                                                 |
| **R5**  | **Worst-case objective.** Optimise or report the minimum per-arm AUC rather than the mean                                                                                            | The selection rule, or the endpoint                                      | Neither — it changes the loss                                      | `49` §1–§4, `18` §Q6(a), `17` item 3                                                                                                                                                                            |
| **R6**  | **Do nothing; report the variance honestly.** One fixed pipeline, four per-protein numbers visible including the worst                                                               | Nothing                                                                  | Neither                                                            | `18` §Q6(d), `17` item 1, `42` §4                                                                                                                                                                               |
| **R7**  | **Aggregate rather than select.** Rank-mean over a portfolio; label-free, nothing per-instance                                                                                       | Nothing per protein; the score is a consensus                            | Interaction, by averaging over it                                  | `18` §Q6(b), `44` §4, metaPocket precedent                                                                                                                                                                      |
| **R8**  | **Estimate the near/far bit and route on it.** A label-blind estimator of whether the labelled site sits near or far from the active site, plus a two-branch router                  | The method, per protein — but with a 1-bit output space                  | Interaction, at its identified mechanism                           | `49` §6, §7, §12 item 6                                                                                                                                                                                         |
| **R9**  | **Spend the held-out arms once on one pre-registered rule.** Regime B: name the descriptor and the endpoint in an ADR before the tier opens                                          | Nothing now; it is the validation design for R1/R2/R4/R8                 | Whichever the rule targets                                         | `48` §4–§5, `42` §4                                                                                                                                                                                             |
| **R10** | **Enlarge the tuning set.** _Listed so it is not re-proposed._                                                                                                                       | The benchmark                                                            | —                                                                  | **Foreclosed.** `18` §7: merging 4 + 5 = 9 still sits below Demšar's N > 10 and leaves nothing held out; ADR 0021 forbids opening the tier to raise n. Doing so trades the thing being defended for the defence |

**Three structural facts about this set, before any of them is tested.**

1. **R3 and R5 are not distinct once a level floor is imposed.** `49` §2's smallest-spread table has
   `bottleneck_to_source` and `symmetry_dark_overlap` at spread **0.0000** — both return a constant
   score and therefore AUC **0.5000** on all four arms — with `degenerate_mixing_weight` third at
   0.0744 and constant on three arms. Ten of the top fifteen by spread have mean AUC at or below
   0.58. Spread alone selects degeneracy. With a floor, R3 collapses into R5's Pareto reading.
2. **R8 is R1 with a smaller output space, and R9 is R8's only admissible validation.** The router is
   trivial; the _estimator_ of the bit carries the capacity, and `18` §Q3's containment argument
   applies to it — a per-instance selector's sample complexity is bounded below by the
   single-configuration case. `18`'s ladder puts a clean sweep of paired wins at **n = 6**, above our 4. R8 validated on `development` is R1; R8 pre-registered and validated once on held-out arms is
   R9.
3. **R2 splits at `19` §1.1 and the split is decisive.** AUC and a top-5 list are invariant under any
   strictly increasing per-protein transform, so `s/N`, `s/λ_max`, `(s − mean)/sd` and `log s` are
   **provable no-ops** for the primary endpoint. Almost the whole size-normalisation literature `19`
   §Q2 catalogues is in this class. Only rules that are non-uniform across residues, or that change
   the operator, the hyperparameter or the evaluation strata, can move the number.

---

## 4. Adversarial test of each route

For each: the **kill condition**, then the **inversion** — what one would do to guarantee this route
wastes the remaining project time — then whether the route as proposed avoids that path.

### R1 — Fitted per-protein selection

**Kill condition.** Any fitting at all on four arms. `18` §7's four floors do not share a mechanism,
so no single fix moves more than one: the combinatorial floor (best possible p = 0.083), the
paired-comparison floor (0.125), the sample-complexity floor (Gupta–Roughgarden gives ε ≈ 1.00 at
m = 4; ε = 0.05 needs m ≈ 1 600), and the empirical floor (smallest competed scenario 100 instances;
on `OPENML-WEKA-2017` — 105 instances, 30 candidates, bounded quality metric, VBS/SBS **1.02** — six
of eight state-of-the-art selectors performed at or below the single best algorithm).

**Inversion — how to guarantee waste.** Screen 30 apo descriptors on four arms. Take the one that
orders them perfectly. Write it into an ADR as a "pre-registered" rule. Open the held-out tier to
confirm it, and claim Regime B power because the rule was named before the tier opened. **Cost: the
entire remaining confirmatory budget, spent on a descriptor that arrived below its own null
expectation of 2.50 (`48` §3), through the exact selection-bias mechanism Ambroise & McLachlan
measure (`18` §Q5) — cross-validation that is not external to the selection process.**

**Does the route avoid it?** No. Both `18` §7 and `48` §6 rule it out on arithmetic. The most
dangerous variant is the one that does not look fitted: `48` §6 names it — "any adaptation rule whose
parameters were chosen by looking at which choice scores better across the four development arms".
A rule can have zero _explicit_ parameters and still be fitted, if its **form** was chosen by
looking.

### R2 — Derived zero-parameter normalisation

**Kill condition.** The rule equalises a quantity the endpoint does not depend on. The worked example
is already in hand and is decisive: the spectral-gap clock removed a real 21.7× disparity, cut
within-arm window sensitivity 0.079 → 0.045, moved between-arm spread by **0.011** — and made the
between/within ratio **worse**, 8.5× → 14.5×, because it shrank the denominator without touching the
numerator (`19` N1, `18` §Q6(c), `44` §6). Zero of 32 clock × window × observable settings put all
four arms above 0.5.

**Inversion.** Choose a normalisation because it is theoretically clean. Implement it across all
fourteen frozen graphs. Sweep it. Never measure `R_within` first. **A second, cheaper inversion:
choose a rule that is a monotone per-protein rescaling — divide by N, by λ_max, by the mean — and
spend an afternoon implementing a provable no-op (`19` §1.1).**

**Does the route avoid it?** **Better than any other route in the set, and it is the only one that
arrives with its own falsifier.** `19` §1.1 screens out the no-ops on paper, §1.2 gives a two-number
pre-screen (between-protein spread of the equalised quantity × within-protein endpoint sensitivity)
that costs one afternoon and would have rejected the gap clock before implementation, and §7 sets a
numeric bar — a candidate passes only if it beats the gap clock's 0.011 by a material margin, with
candidate 1's own bar at > 0.05. **What `19` cannot supply is a reason to expect any candidate to
clear that bar**, because C1 says there is no level effect to remove, and `19` N7 states the general
form: "a normalisation of a quantity whose between-protein spread is 1.1× cannot repair a
between-protein endpoint spread of 0.49".

**One further adversarial reading of `19`'s own list.** Three of its eleven candidates — isostatic
cutoff, connectivity threshold, RDF first minimum — are cutoff rules, and `19` N4 records the
precedent: the one derived cutoff criterion in the literature produces a **universal constant**
(minimum mutual information at 5 Å across distinct proteins). `19` §7 falsifier 7 anticipates this
exactly — if the derived `r*` varies by less than ~0.3 Å across arms the rule is a global constant in
disguise. **That test costs no scoring at all and has not been run.**

### R3 — Adaptation avoidance by low-variance observable

**Kill condition.** Spread used without a level floor. Measured: the two smallest spreads in the
battery are exactly 0.0000 and belong to constant scorers at AUC 0.5000, and a constant scorer sits
at **rank 18 of 69** by worst arm (`49` §2). This is `45`'s random-source lesson in a second setting:
low between-arm variance is a symptom of carrying no signal as often as of carrying robust signal.

**Inversion.** Rank the battery by between-arm spread. Take the top. Report "our method generalises —
between-arm spread 0.00". **It would be arithmetically true and completely worthless, and it would
survive casual review because the number is a deliverable the challenge asks for.**

**Does the route avoid it?** Not as stated. `49` §2 explicitly reports the spread ranking "for
completeness, not as a selection rule", and says to read the Pareto frontier instead — which is R5.

**The deeper objection, which applies to R3, R5 and R7 alike.** Even the best-behaved low-spread
scorer, `betweenness_centrality` at spread 0.068 / mean 0.694 / min 0.651, has not cleared its own
null: `49` §10 records that nothing in this battery beats the distance baseline more often than
chance (`46`), and that the two frontier leaders reject the matched-patch null on at most one arm
each (`40`). **A better ranking among methods that do not clear their null is a better ranking among
methods that do not clear their null** (`49` §10). Every objective-switching route optimises the
between-arm behaviour of a quantity whose above-chance status is unestablished.

### R4 — Source-geometry normalisation

**Kill condition, and `19` names it.** The matched-source ensemble mean carries the **signal** rather
than the artefact. Real allosteric sites _are_ somewhat distal, distance is partly on the causal
path, and a per-residue expectation estimated over matched random sources is a burial/centrality
surrogate — so subtracting it removes part of what we are trying to detect (`19` §Q3.1, citing
`14`'s over-matching warning). The observable signature of the failure is stated: the mean \|ρ\| to
negated distance **rises** above the unnormalised control's.

**Inversion.** Implement the per-residue z-score at M = 1 000 matched sources on every arm — an M-fold
multiplication of propagations, which under C3 is a resource cost that must be declared — discover
that the between-arm spread barely moves, and report the unnormalised and normalised numbers only in
whichever direction is kinder. **A cheaper inversion: run it at M too small, and report a Monte-Carlo
artefact as a result.**

**Does the route avoid it?** Largely yes, and it is the best-instrumented route in the set. `19` §7
prescribes the M ∈ {25, 100, 400} sweep, requires matched and unmatched numbers reported together,
and fixes the insertion point (S6, after pocket smoothing, never before). **The unresolved problem is
C6: the route is filed under normalisation but is a confound-removal step, and it will be scored on
the wrong axis unless the lead says which axis is primary.** `19` §Q3's sibling rules differ in cost
and are worth separating — **radial-quantile stratification is a pure re-scoring of existing runs and
costs no new propagation at all**, which makes it the cheapest live experiment anywhere in this
document.

### R5 — Worst-case objective

**Kill condition.** Using it as a _selection rule_ at n = 4. Measured and unambiguous: leave-one-arm-out
selection on min-of-3 returns held-out worst **0.5632** against mean-of-3's **0.5639** — 0.0007 in the
wrong direction — and costs **0.058** of held-out mean (`49` §4). The mechanism is stated: the minimum
of three numbers is decided by a single arm and inherits that arm's noise entirely, while the mean
averages three.

**Inversion.** Adopt min-of-3 as the selection criterion, freeze the scorer it picks, and present the
result as an improved generalisation claim. **You would have paid 0.058 of held-out mean for 0.0007
in the wrong direction, and the failure would be invisible in the write-up because the objective's
name is exactly the property being claimed.**

**Does the route avoid it?** Only if endpoint and selection rule are kept apart — and both `17` and
`49` independently recommend the same split. `17` item 3 asks for worst-arm AUC as a **pre-registered
secondary endpoint** (reporting); `49` §12 item 1 asks for the worst arm to be reported next to the
mean everywhere (reporting), and item 2 forbids selecting on it. **Conflating "report the minimum"
with "select on the minimum" is the single most likely way this route goes wrong, and the two phrases
are one word apart.**

**Adversarial note on the evidence against it.** `49` §4 rests on four folds and four selections, and
`49` says so: "a warning, not a refutation of worst-case selection in general". The measurement that
would upgrade it does not exist at n = 4.

### R6 — Do nothing; report the variance honestly

**Kill condition.** The report claims generalisation from a four-arm mean, or presents pooled numbers.
`17` §Q1 makes the case concrete: the field's modal estimator pools every residue of every test
structure into one ROC curve, under which a method scoring 0.99 on half the proteins and 0.55 on the
other half prints ≈ 0.87 and the reader cannot tell which world they are in. Our own mean of 0.810 is
built from 0.944 and 0.703 (`17` item 1, quoting `40` §4).

**Inversion.** Two, and they are opposite. **(a)** Spend the remaining phase on adaptation, arrive at
submission with a method tuned on four arms, never confirmed, and no per-arm table. **(b)** Do
nothing _and say nothing_: report a mean, omit the worst arm, and let a reviewer find the spread.
`18` §7 prices (b) precisely — "we considered per-protein adaptation, computed the sample complexity,
and found n = 4 cannot support it" is a stronger paragraph in `docs/report/` than a selector a
reviewer can dismantle with `2/4! = 0.083`.

**Does the route avoid it?** Yes, and it is the only route whose cost has no variance. `18` §Q6(d)
records that `CHALLENGE.md` requires a per-target hit list and connectivity matrix, and that one
fixed pipeline with its four per-protein numbers visible is a **complete deliverable**; adaptation is
an optimisation on top of it, not a requirement of it. **Its risk is not technical. It is that a
negative result only counts if it is written as one** — and the four floors, the below-null screen and
the oracle arithmetic are the material for writing it.

**It is also the only route that does not consume the held-out arms.** Every route that ends in a
confirmatory claim spends them, and they are available once (`48` §5).

### R7 — Aggregate rather than select

**Kill condition, three of them.** (i) The stability gain is mistaken for a generalisation gain —
`49` §8: Spearman(stability, worst-arm AUC) = −0.007, p = 0.97. (ii) The distance correlation rises
0.496 → 0.613 (`18` §Q6(b), `44` §4), which is the wrong direction against `46`, and `49` §8 supplies
the mechanism that makes (i) and (ii) the same fact. (iii) K = 16 multiplies circuit executions by 16
under C3, and every quantum claim must carry its resource cost.

**Inversion.** Build a K = 16 rank-mean ensemble. Report the stability figure (0.581 → 0.888) as the
generalisation evidence. Ship a method whose circuit budget is 16×, whose distance correlation is
higher than the single scorer it replaced, and whose actual between-arm behaviour was never measured.
**Every number in that write-up would be real and the claim would be unsupported.**

**Does the route avoid it?** Partly. `18` §Q6(b) carries both costs in the same breath, so a careful
reader is warned — but `18` does not know (ii) and (i) are one mechanism, because `49` §8 had not been
written. **The measurement that decides R7 is one line: the K = 16 ensemble's four per-arm AUCs, its
spread and its worst arm.** The mechanism predicts the spread should rise. That prediction has never
been tested and is the cheapest way to close or open this route.

**In its favour, and it should not be lost:** R7 asks nothing per-instance, needs no label, is
already implemented, and is the algorithm-selection literature's own recommendation when the selector
cannot be trusted (`18` §Q6(b): static feature-free schedules winning IPC-2011; metaPocket raising
top-1 from ≈ 70 % to 75 % by fixed combination).

### R8 — Estimate the near/far bit and route on it

**What it is.** `49` §7: "The oracle's gain is mostly the gain from knowing, per protein, whether to
use distance or its inverse." `distance_from_source_negated` scores **0.7985 / 0.3333 / 0.9321 /
0.2608** across the four arms; the arms cluster into `{mkp5, hiv_rt}` at ρ = +0.597 and
`{ptp1b, ns5b}` at ρ = +0.678 with a mean between-cluster correlation of −0.212 (`49` §6); and the
arm ordering **reverses under confound removal** — raw `mkp5` 0.635 / `hiv_rt` 0.674 against
exponential-detrended 0.489 / 0.372 (`49` §5).

**Kill condition.** The bit is not estimable from the apo structure. There is a strong structural
reason to fear so: the bit _is_ a property of where the labelled site sits, which is the answer. And
`48` §6 states the version that cannot be tested at all — "if per-arm difficulty is a property of the
apo→holo transition rather than of the apo structure, then no apo-only descriptor can predict it. We
cannot test this. Such a test opens the holo structures on the prediction side, which C1 forbids."
**Currently unknown, and it is the assumption every adaptation route rests on.**

**Inversion.** Spend the remaining phase building an apo-only near/far classifier; validate it on
four arms where a monotone descriptor's floor is p = 0.083 and a clean sweep's is 0.125; carry it to
the held-out arms as a pre-registered rule. **Identical to R1's failure with a smaller output space,
and more seductive because the target has a named mechanism.**

**Does the route avoid it?** Only if the estimator is **derived** rather than fitted, and only if it
is registered before the tier opens — at which point it is R9. `49` §12 item 6 calls it "a sharper
target than adding a 70th scorer", and `49` §10 calls the two-cluster hypothesis "the single most
falsifiable statement in this document" — but also warns that two clusters from four arms with a
post-hoc mechanism is exactly the shape of a pattern found in noise, and that n = 4 cannot
distinguish a two-group separator from a monotone ordering (`49` §9).

**And the prize is bounded by V3.** Even a perfect router captures at most the oracle gap, which is
+0.116 raw, +0.0397 among scorers that are not distance rankings, and ≈ +0.03 against a null that
selects the same way. `17` item 4 puts the 95 % interval on a four-arm mean at roughly **±0.08**.
**A perfect router's honest headroom is smaller than the interval on the number it would improve.**

### R9 — Spend the held-out arms once, on one pre-registered rule

**Kill condition.** The rule that gets pre-registered is the one the four-arm screen produced. Then
Regime B's power table does not apply — the descriptor was chosen by looking, so the applicable row
is Regime A's (13 proteins at ρ = 0.90 against 8), and the held-out set is not enough (`48` §4).

**Second kill condition, from C7.** The held-out arms are not one homogeneous sample. `42` §4 scores
the primary set under Holm–Bonferroni across three confirmatory arms with `cavity_volume` as the
required comparator (ADR 0025); the root contract records that all three mandated pairs are defective
and tiered and that the cardiac myosin pair is unscoreable as assigned. **A single rank test over
"ten held-out proteins" does not exist as a design.**

**Inversion.** Screen on four, pre-register the winner, open the tier, claim Regime B power, and
spend the only confirmation the project has on a descriptor whose provenance is a screen that
returned below its null.

**Does the route avoid it?** Only under a provenance rule: the descriptor must come from mechanism,
stated in an ADR with the endpoint and the abandonment threshold, before anything is scored. That is
precisely `42` §4 steps 1–3 and `48` §5's Regime B. **The route is sound; what is missing is the
number of arms it actually has, which no document in the set states.**

### R10 — Enlarge the tuning set

Foreclosed above. Recorded so it does not consume a meeting.

---

## 5. Second-order effects

What each route makes more or less likely at the next phase and at submission. "Spends the tier"
means it consumes the once-only confirmation of `48` §5.

| Route                                | Spends the tier?                       | C3 cost                                                 | Makes more likely at the next phase                                                                       | Makes more likely at submission                                                                                   | Makes less likely                                                                              |
| ------------------------------------ | -------------------------------------- | ------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| **R1**                               | Yes, and wastes it                     | none directly                                           | A descriptor written into an ADR that four arms cannot support; pressure to reopen the tier when it fails | A reviewer closing the claim with `2/4! = 0.083`                                                                  | Any other use of the held-out arms                                                             |
| **R2a** (rank-invariant)             | No                                     | none                                                    | Implementation effort with a provable zero endpoint change                                                | A reporting section that is genuinely better (`19` S10: `ĝ`, `PR/N`, `H/log N`, `h_t/n`, plus `⟨k⟩/6` per target) | Nothing — it is free and small                                                                 |
| **R2b** (operator / strata / cutoff) | No, if run on `development`            | `L_sym` free; pfANM multiplies Trotter depth by `N/⟨k⟩` | A short, decisive negative: `19` §7 falsifier 7 closes the three cutoff rules with no scoring at all      | A methods section that shows derived rules were tried and priced                                                  | Re-proposal of a spectral clock (`19` says do not)                                             |
| **R3**                               | No                                     | none                                                    | Selection of a degenerate constant unless a level floor is imposed                                        | A "between-arm spread 0.00" line that a careful reviewer will invert                                              | Nothing — it collapses into R5                                                                 |
| **R4**                               | No, if run on `development`            | M-fold propagation multiplier, declarable under C3      | The cheapest live experiment in the set (radial-quantile strata: pure re-scoring, no new propagation)     | A defensible S6 stage with matched and unmatched numbers side by side                                             | R4's own claim, if it is scored on between-arm spread instead of against the distance baseline |
| **R5** (as endpoint)                 | No                                     | none                                                    | A worst-arm column everywhere, at a cost of one column                                                    | A generalisation claim that is about the number it names                                                          | An overclaim from a four-arm mean                                                              |
| **R5** (as selection rule)           | Indirectly — it fixes what gets frozen | none                                                    | Freezing a scorer chosen by a criterion measured not to transfer                                          | −0.058 of held-out mean, invisible in the write-up                                                                | A defensible freeze under ADR 0012                                                             |
| **R6**                               | **No**                                 | none                                                    | Time released for the confirmatory design of `42` §4 and for the C3/C4 resource account                   | A negative result written as one, with four floors and an oracle bound behind it                                  | Any positive adaptation claim, including a true one                                            |
| **R7**                               | No                                     | **×K circuit executions** — 16× at the measured K       | A single decisive measurement (the ensemble's four per-arm AUCs) that nobody has taken                    | A stability deliverable (§4.2) that is genuinely satisfied                                                        | A distance-orthogonality claim, since ρ rises 0.496 → 0.613                                    |
| **R8**                               | Only via R9                            | depends on the estimator                                | The most mechanistically motivated experiment available, and the one most likely to be R1 in disguise     | Either the project's only real per-protein result, or its most expensive null                                     | Adding a 70th scorer                                                                           |
| **R9**                               | **Yes, by construction, once**         | none                                                    | An ADR with a rule, an endpoint and an abandonment threshold, written before the tier opens               | A confirmatory claim, whichever way it lands                                                                      | A second attempt                                                                               |

**Two cross-cutting second-order effects worth naming separately.**

- **ADR 0012 binds every route that changes a hyperparameter.** A choice made on `development` must
  be frozen before the tier opens. R2b, R4, R5-as-selection and R8 are all hyperparameter choices in
  that sense; R6 and R2a are not. **The routes differ less in what they cost to run than in what they
  cost to freeze.**
- **Every route except R6 and R2a increases the number of things that must be true for the submission
  to hold.** `42` §2's ten threats are stated against a fixed pipeline; each adaptation route adds a
  new selection surface, and T1 (selection) and T9 (sign flips chosen after seeing the data) are the
  two threats that grow directly with the number of surfaces.

---

## 6. One cross-domain parallel: naive diversification in portfolio choice

**The parallel.** Mean–variance portfolio optimisation takes estimated expected returns for N assets
and produces optimal weights. The estimates are noisy; the optimiser is maximally sensitive to
exactly the directions in which they are noisiest; and the resulting "optimal" portfolio can perform
worse out of sample than the zero-parameter equal-weight `1/N` rule. DeMiguel, Garlappi and Uppal put
the question in their title — _Optimal Versus Naive Diversification: How Inefficient Is the 1/N
Portfolio Strategy?_, Review of Financial Studies 22(5):1915–1953, doi:10.1093/rfs/hhm075
[**bibliographic record confirmed via Crossref 2026-08-27; the paper's text was not retrieved this
session, so its own figures are not quoted here and the qualitative result below is UNVERIFIED and
must be re-retrieved before it reaches `docs/report/`**].

**Why it transfers, stated as a mapping rather than an analogy.**

| Portfolio choice                    | Here                                                  |
| ----------------------------------- | ----------------------------------------------------- |
| Assets                              | Scorers (69)                                          |
| Estimated expected return per asset | Per-arm AUC per scorer                                |
| Length of the estimation window     | Number of proteins (4)                                |
| The optimiser's input error         | Hanley–McNeil SE ≈ 0.082 per arm (`17` §6)            |
| The prize the optimiser chases      | The oracle gap, +0.116 raw / ≈ +0.03 honest (`49` §7) |
| `1/N` equal weighting               | Rank-mean ensembling over the portfolio — **R7**      |
| "Pick the best asset each period"   | Per-protein selection — **R1**, **R8**                |

**The transfer condition, and our numbers meet it.** The naive rule wins when the cross-sectional
spread of the true means is small relative to the estimation error of those means. Ours: a
between-arm spread of **0.175** against a per-arm estimation error of **0.082** — the same order.
This is the same statement C2 makes from a different direction, and it is why the portfolio result is
the right import rather than a decoration.

**What the parallel predicts that our own documents also say.** That a large _oracle_ gap does not
imply a capturable gap — there genuinely is a best asset every period, and the optimiser still cannot
find it. `49` §7 says the same thing in our units: "at most +0.116 against a fixed choice, about
+0.03 against a null that selects the same way, and unreachable either way". And `18` §Q3's
`OPENML-WEKA-2017` result is the algorithm-selection field's independent instance of it.

**Where the parallel breaks, and the break is instructive.** Finance has hundreds of periods and only
a short estimation window; we have four proteins and no time dimension at all, so we cannot buy our
way out by extending the window. And `1/N` works in finance because assets have broadly comparable
risk premia; here **ten of the fifteen lowest-spread scorers have mean AUC at or below 0.58 and two
are constants at 0.5000** (`49` §2). **So the transferred advice is not "equal-weight the battery" —
it is "equal-weight a level-floored subset", which is a different and smaller claim than R7 as
currently proposed.**

---

## 7. Confidence calibration

Every claim carried forward, with the **single** measurement that would change it. High = arithmetic
or an exact decomposition; Medium = a measurement resting on one identified assumption; Low =
four-fold, exploratory or post-hoc.

| #   | Claim                                                                                                                                                                                    | Conf.                                                                 | Source                                                                                                                                        | The one measurement that would change it                                                                                                                                                                                                       |
| --- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Classical between-arm spread is **0.175** and the Hanley–McNeil floor is **0.169**; ratio 1.04                                                                                           | **High**                                                              | `48` §1, `17` §6                                                                                                                              | Nothing — both are computed from committed records and a published formula                                                                                                                                                                     |
| 2   | Therefore there is **no demonstrated per-protein effect** for the classical family, P = 0.43                                                                                             | **Medium**                                                            | `48` §1                                                                                                                                       | The benchmark's own null: the distribution of max−min AUC spread across four arms from the matched-patch draws inside `score_arm` (`17` item 2). See C2 — the analytic floor is an upper bound, so the error runs against the claim            |
| 3   | Quantum spread **0.361**, P = 0.011, median AUC **0.455** — an uninformative score, not a target effect                                                                                  | **High**                                                              | `48` §1, `17` §6                                                                                                                              | A quantum family whose median clears 0.5 on the same four arms                                                                                                                                                                                 |
| 4   | At n = 4 the minimum two-sided Spearman p is **0.083**; power is exactly zero at any effect size                                                                                         | **High**                                                              | `48` §2, `18` §4                                                                                                                              | Nothing at n = 4. Only n ≥ 5 changes it                                                                                                                                                                                                        |
| 5   | The 30-descriptor screen produced **1** perfect ordering against **2.50** expected                                                                                                       | **High** for the arithmetic, **Medium** as evidence of absence        | `48` §3, `49` §9                                                                                                                              | A screen on a descriptor source disjoint from `frozen-graph-profile.json` at n ≥ 5. Note V2: the K = 37 screen is not a replication                                                                                                            |
| 6   | Variance decomposition: arm **1.15 %** main effect, `arm × scorer` **27.26 %**, graph **0.17 %**                                                                                         | **High**                                                              | `49` §5                                                                                                                                       | The same exact decomposition on held-out arms. It assumes nothing — one observation per cell, residual reported as a component                                                                                                                 |
| 7   | Arm difficulty **reverses** under confound removal; which arms are easy is not a property of the protein                                                                                 | **High**                                                              | `49` §5 (raw 0.635/0.453/0.674/0.446 against exponential 0.489/0.596/0.372/0.532; `distance_from_source_negated` 0.7985/0.3333/0.9321/0.2608) | The same detrend × arm table on held-out arms showing a stable ordering                                                                                                                                                                        |
| 8   | Oracle gap **+0.1164**, falling to **+0.0755** / **+0.0397** under the two distance filters                                                                                              | **High**                                                              | `49` §7                                                                                                                                       | Nothing — it is a maximum over committed records                                                                                                                                                                                               |
| 9   | Honest headroom against a selection-inflated null is **≈ +0.03** (observed 0.876 against a null interval 0.76–0.84)                                                                      | **Medium**                                                            | `49` §7                                                                                                                                       | The label-blind **per-arm** best-of-V distribution computed at the actual V, rather than inferred from a quantile argument. The effective-V estimate behind the interval was revised by more than an order of magnitude once already (`42` T2) |
| 10  | Selecting on the worst arm does not improve the held-out worst arm (0.5632 against 0.5639) and costs **0.058** of held-out mean                                                          | **Low–Medium**                                                        | `49` §4                                                                                                                                       | Repeated leave-one-out over more arms, or a resampling over scorers rather than arms. `49` calls it "a warning, not a refutation"; it rests on four selections                                                                                 |
| 11  | Stability does not predict worst-arm performance: **−0.007**, p 0.97                                                                                                                     | **Medium**                                                            | `49` §8                                                                                                                                       | Completing stability coverage from 32 to all 69 scorers. The relationship it replaces (stability ↔ distance, +0.599 pooled, +0.881 quantum) is post-hoc and uncorrected                                                                        |
| 12  | A fitted per-protein selector is inadmissible at n = 4 (four independent floors)                                                                                                         | **High**                                                              | `18` §7                                                                                                                                       | Only more proteins, which ADR 0021 forecloses                                                                                                                                                                                                  |
| 13  | Zero-parameter normalisation is statistically admissible but needs a mechanism; the gap clock moved spread **0.011** and worsened the variance ratio 8.5× → 14.5×                        | **High**                                                              | `19` N1, `44` §6                                                                                                                              | Nothing — it is measured. What is unknown is whether any _other_ derived rule clears the bar                                                                                                                                                   |
| 14  | Between-protein graph variation is too small for any graph-side rule to matter (⟨k⟩ 8.9–10.3, clustering 0.460–0.515, λ₁ 10.40–11.80 over a 7.2× size range; graph = 0.17 % of variance) | **High**                                                              | `19` N7, `49` §5                                                                                                                              | Scope note only: on AUC-PR the graph axis moves 3.5× further in relative terms (`49` §12 item 5, quoting the registry)                                                                                                                         |
| 15  | Source geometry varies where the graph does not (source size 20×, median candidate-to-source distance 3.1×, within-10 Å fraction 0.12–0.69)                                              | **High** for the variation, **Medium** for its relevance              | `19` §Q3                                                                                                                                      | `R_within`: the endpoint's sensitivity to source geometry inside one protein (`19` §1.2). Without it, condition (b) of the pre-screen is unmeasured for the top-ranked candidate                                                               |
| 16  | The near/far bit is the whole reachable ceiling, and the two arm clusters are `{mkp5, hiv_rt}` / `{ptp1b, ns5b}`                                                                         | **Low**                                                               | `49` §6, §7                                                                                                                                   | Whether the clustering reproduces on held-out arms. Two clusters from four arms with a post-hoc mechanism; `49` §10 lists it under "not supported"                                                                                             |
| 17  | Our spread is unremarkable by the field's standards                                                                                                                                      | **Low**                                                               | `17` §2, §6                                                                                                                                   | A published between-target **AUC** standard deviation for this task. None exists in the retrieved corpus, and the comparison currently runs across metrics (C3)                                                                                |
| 18  | Ensembling raises stability 0.581 → 0.888 at ΔAUC −0.015 and ρ-to-distance 0.496 → 0.613                                                                                                 | **High** for the numbers, **Low** for their bearing on generalisation | `18` §Q6(b), `44` §4, reinterpreted by `49` §8                                                                                                | The K = 16 ensemble's four per-arm AUCs, its spread and its worst arm — never measured (C5)                                                                                                                                                    |
| 19  | Held-out arms available: `48` §5 says 10                                                                                                                                                 | **Low**                                                               | `48` §5 against `42` §4 and the root contract                                                                                                 | A statement of how many arms can carry one rank test under one protocol, given tiering, defects and the primary set's separate comparator (C7)                                                                                                 |

---

## 8. Knowledge gaps

Ranked by how much each blocks a decision, not by cost.

1. **Whether per-arm difficulty is a property of the apo structure or of the apo→holo transition.**
   `48` §6: unknown, and **untestable under C1** — the test would open holo structures on the
   prediction side. Every adaptation route rests on this assumption and none of the five documents can
   discharge it.
2. **The minimum detectable _difference_ between two correlated scorers on one arm.** `42` T6 and
   `41` §5 state the minimum detectable **level** (AUC 0.762–0.936 at α; 0.794–0.955 at 80 % power);
   `46` runs a paired test whose resolvable difference is a smaller, different number that **no
   document quotes**. Without it, "the oracle gain is smaller than what we can measure" (`48` §6) is
   an unfinished comparison (C8).
3. **The benchmark's own max−min spread null.** Recommended by `17` item 2, never run, costs one pass
   over existing draws (C2).
4. **The K = 16 ensemble's four per-arm AUCs.** Decides R7 in one line, and the mechanism in `49` §8
   predicts the spread rises (C5).
5. **`R_within` for source geometry and for the geometry clock.** `19` §1.2 makes it the gate on its
   own top-ranked candidates; `19` §7 falsifier 3 says stop if it is below 0.05.
6. **The between-arm spread of the three derived cutoff rules' `r*`.** `19` S1: the cheapest test in
   that file, no scoring required, and it closes or opens three candidates at once.
7. **How many held-out arms can carry one pre-registered rank test.** C7.
8. **Cross-family generalisation in the published field.** `17` §Q4: no cross-family transfer
   experiment was retrieved for allosteric- or cryptic-site prediction. Recorded as a negative result
   of a recorded search (ADR 0019), not as an absence.

---

## 9. What the lead has to decide

Questions, with the evidence bearing on each. No answers.

**Q1 — Which half of C1 is the project trying to fix: the level, or the interaction?**
Bearing: `48` §1 (no demonstrated level effect for the classical family, P = 0.43) against `49` §5
(`arm × scorer` 27.26 %, arm main effect 1.15 %). R2a and most of `19` §Q2 target a level that does
not appear to exist; R1, R4, R7 and R8 target the interaction, which exists and which V1/V4 say
cannot be aimed at with four arms. **No route in §3 targets both.**

**Q2 — Is any adaptation route worth the held-out arms, given that even a perfect router wins less
than the interval on the number it would improve?**
Bearing: `49` §7 (+0.116 → +0.0397 → ≈ +0.03), `17` item 4 (95 % interval on a four-arm mean ≈ ±0.08),
`18` §Q3 (VBS/SBS 1.02–1.7 on bounded quality metrics; six of eight selectors at or below the single
best on the scenario shaped like ours). Against: gap 2 in §8 — the comparison has not been made on
the right statistic.

**Q3 — Is the worst arm an endpoint, a selection rule, or both?**
Bearing: `17` item 3 and `49` §12 item 1 both ask for it as a reported endpoint, at a cost of one
column. `49` §4 measures it failing as a selection rule (0.5632 against 0.5639; −0.058 of held-out
mean). `18` §Q6(a) predicted that failure from the variance of a minimum at n = 4. **The two uses
have opposite evidence and one name.**

**Q4 — Does `gnm_fluctuation` replace `eigenvector_centrality` as the frozen scorer, and on which
argument?**
Bearing: the trade is 0.0089 of mean for 0.0751 of worst arm, 8:1 (`49` §1); `gnm_fluctuation` is #1
by minimax regret and #2 by mean; the mean cost is a twentieth of the ±0.08 interval on a four-arm
mean. Against: the choice was made after seeing all four arms, and neither scorer rejects the
matched-patch null on more than one arm (`49` §10). ADR 0012 makes this a hyperparameter choice that
must be frozen before the tier opens.

**Q5 — Is the source z-score filed as normalisation (judged on between-arm spread) or as S6 confound
removal (judged against the distance baseline)?**
Bearing: `19` §7 ranks it first as a normalisation; `19` §S6 files it as confound removal; its own
falsifier is written both ways. C6. The answer decides which experiment is run and which null it is
scored against, and the two would give different verdicts on the same run.

**Q6 — Does the benchmark's own max−min null get computed before any spread number reaches
`docs/report/`?**
Bearing: `17` item 2 recommends it; `48` used the analytic floor instead; C2 shows the analytic floor
is an upper bound, so the direction of the error runs against the "no effect" reading. Cost: one pass
over draws that already exist.

**Q7 — Which single cheap measurement is run first?**
The candidates, with their costs. _(a)_ The max−min null — one pass over existing draws, and it
settles Q6 and claim 2. _(b)_ Radial-quantile stratified AUC — a pure re-scoring of existing runs,
no new propagation (`19` §7 falsifier 2). _(c)_ The spread of the three derived cutoffs' `r*` — no
scoring at all (`19` S1). _(d)_ The K = 16 ensemble's four per-arm AUCs — one pass, and it decides R7
(C5). _(e)_ `R_within` for source geometry on one arm — one sweep, and it gates `19`'s top two
candidates. **All five are cheaper than any route in §3, and none has been run.**

**Q8 — If nothing is adapted, is the negative result written as a result?**
Bearing: `18` §7 ("we considered per-protein adaptation, computed the sample complexity, and found
n = 4 cannot support it" is a stronger paragraph than a selector a reviewer can dismantle);
`18` §Q6(d) (`CHALLENGE.md` is satisfied by one fixed pipeline with its four per-protein numbers
visible); `17` item 1 (keep the per-arm table primary and the mean secondary, and say in
`docs/report/` why — the field's modal pooled estimator would have concealed the entire result);
`42` §4 (the confirmatory design that turns a screen into a result, whichever way it lands).
**R6 is the only route whose cost has no variance, and the only one that leaves the held-out arms
unspent.**
