# How many instances per-instance algorithm selection needs, and what four buys you

**Scope:** Whether a **fitted per-protein selector** — a rule that reads descriptors of an apo
protein and chooses which pipeline arm to run on it — can be learned and validated from a tuning
set of **four** proteins. Covers the learning-theoretic sample complexity of algorithm selection,
the instance counts the successful empirical selectors actually used, the single-best-solver and
virtual-best-solver reference points and the fraction of the gap between them that real systems
close, the small-sample regime, the multiple-comparisons failure mode in descriptor screening,
and the alternatives the literature recommends when a selector cannot be fitted. Deliberately
excludes the _architecture_ of a selector (Rice's formalisation, SATzilla's four blocks,
Kerschke's survey — all in `15-ai-preprocessing.md` §Q3), the choice of graph
(`13-graph-construction.md`) and the distance confound (`14-distance-confound.md`).
**Sibling files:** `00-conventions.md` (evidence tags, C1–C6, the leakage guard),
`15-ai-preprocessing.md` §Q3 (what per-instance selection _is_, the meta-feature criteria, the
label-free adaptation candidates, and the n·log₂(m) capacity argument),
`09a-power-verification.md` and `../exploration/results/41-selection-and-power.md` (what four
arms resolve), `../exploration/results/44-stability-and-noise.md` (the measured between-arm
spread that motivates wanting adaptation at all, and the one derived adaptation rule we tried).
**Retrieved:** 2026-08-27.

**No experiment has run behind this file.** Nothing here opens any path under
`docs/benchmark/`, and no real label residue is named. Every arithmetic derivation below is
stated so it can be re-checked by hand.

---

## Executive summary — the six numbers that decide it

1. **A perfect descriptor cannot be significant at n = 4.** Under the exact permutation null, a
   descriptor that orders four proteins exactly right (or exactly backwards) has two-sided
   p = 2/4! = **0.083**. That is above α = 0.05 _before any correction for multiplicity_. The
   multiple-comparisons correction is therefore not the binding constraint; the granularity of
   the null is. [derived below, §5]
2. **The repo's own screening arithmetic checks out and points the other way from "we found
   something".** With n = 4 and K = 30 descriptors, E[perfect orderings] = 30·2/24 = **2.500**
   and P(≥1) = 1 − (11/12)³⁰ = **0.9265**. One observed perfect ordering is _below_ the null
   expectation of 2.5. [derived below, §5; reproduces the stated 2.50 / 0.93 / observed 1]
3. **The theory's bound is vacuous at m = 4.** Gupta & Roughgarden's uniform-convergence
   condition is m ≥ c(H/ε)²(d_ℋ + ln(1/δ)). At the smallest non-trivial pseudo-dimension d = 1,
   δ = 0.05, H = 1 (AUC is bounded) and c = 1, m = 4 buys ε ≈ 1 — the whole range of the metric.
   ε = 0.05 needs m ≈ **1 600**. [§1]
4. **The empirical selectors used hundreds to thousands.** SATzilla07 drew on **4 811** SAT
   instances, split 40:30:30, with 7 candidate solvers and 48 features. The smallest scenario ever
   admitted to an algorithm-selection competition has **100** instances; participants trained on
   two thirds of them. [§2]
5. **Real selectors close roughly 60–70 % of the SBS→VBS gap — and fail exactly where our
   problem lives.** Best 2015 system: 0.366 remaining gap. Best 2017 system: 0.38. But on
   `OPENML-WEKA-2017` — 105 instances, 30 candidate algorithms, a **bounded quality metric**, and
   a VBS that beats the SBS by a factor of only **1.02** — "six out of eight submissions performed
   almost equal to or worse than the single best solver". [§3]
6. **Nobody attempts this below ~100 instances, and the field's own reference says N > 10.**
   Demšar's rule of thumb for comparing algorithms across data sets is **N > 10 and k > 5**; his
   table of sign-test critical values begins at N = 5. No study of per-instance algorithm
   selection with fewer than ~20 training instances was retrieved by the recorded search — a
   negative result under ADR 0019, not an absence claim. [§4]

**Verdict, stated once here and defended in §7: at n = 4 a fitted per-protein selector is not
defensible, and no correction, resampling scheme or Bayesian reframing repairs it.**

---

## Q1. Sample complexity of algorithm selection — what the theory says

### Synthesis

**The problem was given a PAC formulation in 2016, and the answer has the standard shape.**
Gupta & Roughgarden "adapt concepts from statistical and online learning theory to reason about
application-specific algorithm selection", modelling algorithm selection as a statistical learning
problem in which "dimension notions from statistical learning theory, historically used to measure
the complexity of classes of binary- and real-valued functions, are relevant in a much broader
algorithmic context" [VERIFIED-ABSTRACT, arXiv:1511.07147; ITCS 2016 doi:10.1145/2840728.2840766;
SIAM J. Comput. 46(3):992–1017, doi:10.1137/15M1050276].

The load-bearing statement is their uniform-convergence theorem. Theorem 3.2 gives the condition

> "if m ≥ c(H/ϵ)²(d_ℋ + ln(1/δ)) for a suitable constant c (independent of all other parameters)"

and Corollary 3.4 concludes that "any ERM algorithm (2ϵ, δ)-learns the optimal algorithm in 𝒜 from
m samples" [VERIFIED-FULLTEXT, ar5iv rendering of arXiv:1511.07147, §3].

**What the bound depends on, in plain terms.** Three quantities, and only one of them is under our
control.

| Symbol | Meaning                                                                                | Our value                                   |
| ------ | -------------------------------------------------------------------------------------- | ------------------------------------------- |
| `H`    | the range of the cost/performance function                                             | 1 — AUC is bounded in [0,1]                 |
| `d_ℋ`  | the pseudo-dimension of the class of algorithms (or of selection rules) being searched | ≥ 1, and much larger for any real portfolio |
| `ε`    | the accuracy you want the learned choice to have against the best in class             | the effect we care about, ~0.02–0.05 AUC    |
| `δ`    | failure probability                                                                    | 0.05                                        |
| `c`    | an unspecified absolute constant                                                       | ≥ 1, unknown                                |

Gupta & Roughgarden then bound `d_ℋ` for concrete families: `O(log(κβn))` for a class of greedy
heuristics (κ the crossing number of the scoring rules, β a bound on attribute changes), and for
gradient-descent step-size selection "there is a learning algorithm that (1+ϵ, δ)-learns the optimal
algorithm … using m = Õ(H³/ϵ²) samples" [VERIFIED-FULLTEXT, ibid., Theorems 3.6 and 3.19].

**The arithmetic at m = 4.** Take the most favourable possible reading: d_ℋ = 1 (one binary
decision), H = 1, δ = 0.05 so ln(1/δ) = 3.00, and c = 1. Then m ≥ (1/ε)²·(1 + 3.00) = 4/ε². Solving
for ε at m = 4 gives ε = 1.00 — the entire range of AUC, which is no guarantee at all. ε = 0.10
needs m = 400; ε = 0.05 needs m = 1 600. [UNVERIFIED — arithmetic performed in this document on
the verified formula. `c ≥ 1` is an assumption; the theorem leaves `c` unspecified, so this is an
order-of-magnitude reading, not a theorem application. The direction, however, is not in doubt:
raising `c`, `d_ℋ` or `H` can only make the requirement larger.]

**Balcan's programme generalises the bound and gives it a name.** "How much data is sufficient to
learn high-performing algorithms? Generalization guarantees for data-driven algorithm design"
develops bounds for the case where "for many types of algorithms, performance is a volatile function
of the parameters: slightly perturbing the parameters can cause large changes in behavior", covering
piecewise-constant, piecewise-linear and more generally piecewise-structured performance functions,
and unifying earlier case-specific analyses [VERIFIED-ABSTRACT, arXiv:1908.02894; STOC 2021].
**The volatility clause is ours.** `../exploration/results/44-stability-and-noise.md` §3 measures
the same observable rising from AUC 0.304 to 0.686 with the coherence window on one arm and falling
from 0.605 to 0.177 on another — a piecewise-volatile performance function in exactly the sense the
bound is written for, which is the regime where the pseudo-dimension is _largest_.

**The result that speaks directly to a portfolio of the size we screened.** Balcan, Sandholm &
Vitercik provide "the first provable guarantees for portfolio-based algorithm selection", analysing
"how large the training set should be to ensure that the resulting algorithm selector's average
performance over the training set is close to its future (expected) performance", through three
channels: "1) the learning-theoretic complexity of the algorithm selector, 2) the size of the
portfolio, and 3) the learning-theoretic complexity of the algorithm's performance as a function of
its parameters." Their conclusion is unambiguous:

> "We prove that if the portfolio is large, overfitting is inevitable, even with an extremely
> simple algorithm selector."

and they describe the resulting tension: "as we increase the portfolio size, we can hope to include
a well-suited parameter setting for every possible problem instance, but it becomes impossible to
avoid overfitting" [VERIFIED-ABSTRACT, AAAI 35(14):12225–12232, doi:10.1609/aaai.v35i14.17451;
arXiv:2012.13315].

**Read that beside our own portfolio.** `../exploration/results/40-method-sweep.md` scored 1 923
complete variants and `46-beats-distance.md` compares 69 scorers. That is a large portfolio by any
reading, and the theorem says overfitting is inevitable for a large portfolio _even with an
extremely simple selector_ — which is the design we would be forced into at n = 4.

**One distinction the literature is careful about and we should be too.** Most of Gupta &
Roughgarden's and Balcan's bounds are for learning a **single** configuration that is good in
expectation over the instance distribution. That is the _SBS-like_ task, and it is the easier one.
A per-instance selector is a map from features to algorithms, a strictly richer hypothesis class, so
its sample complexity is bounded below by the single-configuration case. **Every bound quoted here
is a floor for what we want, not a ceiling.** [UNVERIFIED — inference from the definitions in the
cited abstracts; the containment is standard but was not retrieved as a stated theorem.]

### Table

| Source                                                | Year      | What it establishes                                                                    | The bound, and what it turns on                                                                            | Verification                                                    |
| ----------------------------------------------------- | --------- | -------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------- |
| Gupta & Roughgarden, ITCS/SICOMP                      | 2016/2017 | PAC framework for application-specific algorithm selection                             | `m ≥ c(H/ε)²(d_ℋ + ln(1/δ))`; pseudo-dimension of the algorithm class, range of the cost, accuracy squared | [VERIFIED-FULLTEXT] arXiv:1511.07147 §3; doi:10.1137/15M1050276 |
| Gupta & Roughgarden, Thm 3.6                          | 2016      | pseudo-dimension of a greedy-heuristic family                                          | `O(log(κβn))`                                                                                              | [VERIFIED-FULLTEXT] same                                        |
| Gupta & Roughgarden, Thm 3.19                         | 2016      | step-size selection for gradient descent                                               | `m = Õ(H³/ε²)`                                                                                             | [VERIFIED-FULLTEXT] same                                        |
| Balcan, DeBlasio, Dick, Kingsford, Sandholm, Vitercik | 2021      | generalisation for data-driven algorithm design under piecewise-structured performance | bounds via the dual class structure; volatility of performance in the parameters is the driver             | [VERIFIED-ABSTRACT] arXiv:1908.02894, STOC 2021                 |
| Balcan, Sandholm & Vitercik                           | 2021      | first provable guarantees for **portfolio-based** selection                            | three channels; **large portfolio ⇒ overfitting inevitable, even with a trivial selector**                 | [VERIFIED-ABSTRACT] doi:10.1609/aaai.v35i14.17451               |
| Wolpert & Macready                                    | 1997      | no free lunch — why per-instance selection is attractive at all                        | averaged over all problems, no algorithm dominates                                                         | [VERIFIED-ABSTRACT metadata] doi:10.1109/4235.585893            |

**What it changes here.** Nothing in the theory forbids a _derived_ rule with no fitted parameters
(pseudo-dimension 0). Everything in it forbids a _fitted_ one at m = 4.

---

## Q2. What the successful selectors actually trained on

### Synthesis

**SATzilla07 — the canonical system, with the exact counts.** From the paper's own §3.1:

> "Overall, there were 4 811 instances: 2 300 instances in category `RANDOM`, 1 490 in category
> `HANDMADE` and 1 021 in category `INDUSTRIAL`; of course, category `ALL` included all of these
> instances."

and

> "We randomly split our data set into training, validation and test sets at a ratio of 40:30:30."

[VERIFIED-FULLTEXT, arXiv:1111.2249 §3.1; JAIR 32:565–606, doi:10.1613/jair.2490]. The portfolio
held **seven** component solvers and the model used **48** raw features [VERIFIED-FULLTEXT, ibid.
§3.2, §3.3]. So the _smallest_ single-distribution training set SATzilla07 ever used was
0.40 × 1 021 ≈ **408** instances, for 7 candidates and 48 features.

**ASlib and the two competitions fix the field's operating range.** The 2015 competition ran 13
scenarios; the instance counts are [VERIFIED-FULLTEXT, Lindauer, van Rijn & Kotthoff, _Artificial
Intelligence_ 272 (2019) 86–100, doi:10.1016/j.artint.2018.10.004, Table 1]:

| Scenario     | algorithms | instances | features | VBS/SBS factor |
| ------------ | ---------- | --------- | -------- | -------------- |
| ASP-POTASSCO | 11         | 1 294     | 138      | 25             |
| CSP-2010     | 2          | 2 024     | 17       | 10             |
| MAXSAT12-PMS | 6          | 876       | 37       | 53             |
| CPMP-2013    | 4          | 527       | 22       | 31             |
| PROTEUS-2014 | 22         | 4 021     | 198      | 413            |
| QBF-2011     | 5          | 1 368     | 46       | 96             |
| SAT11-HAND   | 15         | 296       | 115      | 37             |
| SAT11-INDU   | 18         | 300       | 115      | 22             |
| SAT11-RAND   | 9          | 600       | 115      | 66             |
| SAT12-ALL    | 31         | 1 614     | 115      | 30             |
| SAT12-HAND   | 31         | 1 167     | 138      | 35             |
| SAT12-INDU   | 31         | 767       | 138      | 15             |
| SAT12-RAND   | 31         | 1 167     | 138      | 12             |

The 2017 competition's eleven scenarios span "different numbers of algorithms (5–31) and instances
(**100**–9720)" [VERIFIED-FULLTEXT, Lindauer, van Rijn & Kotthoff, _Open Algorithm Selection
Challenge 2017: Setup and Scenarios_, PMLR 79:1–7, §3]. Its Table 2 gives the counts, and two rows
matter to us more than the other nine [VERIFIED-FULLTEXT, doi:10.1016/j.artint.2018.10.004, Table 2]:

| Scenario              | alias   | algorithms | instances | features | objective   | VBS/SBS factor |
| --------------------- | ------- | ---------- | --------- | -------- | ----------- | -------------- |
| CSP-Minizinc-Obj-2016 | Camilla | 8          | **100**   | 95       | **Quality** | **1.7**        |
| OPENML-WEKA-2017      | Oberon  | **30**     | **105**   | 103      | **Quality** | **1.02**       |
| TTP-2016              | Titus   | 22         | 9 720     | 50       | Quality     | 1.04           |
| MIP-2016              | Mira    | 5          | 218       | 143      | Time        | 11             |
| QBF-2016              | Qill    | 24         | 825       | 46       | Time        | 265            |
| SAT03-16_INDU         | Sora    | 10         | 2 000     | 483      | Time        | 13             |

Participants "had access to performance and feature data on training instances (2/3), and only the
instance features for the test instances (1/3)" [VERIFIED-FULLTEXT, PMLR 79:1–7, §2]. **So the
smallest training set in the whole competition is about 67 instances.**

**`OPENML-WEKA-2017` is the scenario built out of our exact problem shape, and it is worth reading
carefully.** It is machine-learning algorithm selection: datasets are the instances, 30 WEKA
learners are the candidates, 103 meta-features describe each dataset, and the objective is a
**bounded quality score**, not runtime. Our situation is the same shape — proteins as instances,
pipeline arms as candidates, structural descriptors as meta-features, AUC as a bounded quality
score. Its numbers are 105 instances and 30 candidates. Ours would be **4** instances and 30
descriptors. §3 reports what happened to it.

**Frugal algorithm selection is the field's own low-data frontier, and it is not close.** Kuş,
Akgün, Dang & Miguel address "the cost of training [that] can be prohibitively large due to running
candidate algorithms on a representative set of training instances" by "choosing a subset of the
training instances on which to train", using active learning, timeout predictors and progressively
increasing timeouts, evaluated "on six datasets from ASLib" [VERIFIED-ABSTRACT, arXiv:2405.11059,
CP 2024]. The headline result is

> "In several cases the training effort is reduced to 10% of the labelling cost of passive
> learning."

[VERIFIED-FULLTEXT, arXiv:2405.11059 §"Key findings"]. Note precisely what is reduced: **labelling
cost** (CPU time), on scenarios of 527–2 024 instances. Ten per cent of the labelling cost of
CSP-2010 is still a training set of hundreds. **The paper whose entire subject is spending less
still operates two to three orders of magnitude above n = 4.**

**AutoML/meta-learning does not rescue the count.** The competitions paper records that "the AutoML
system auto-sklearn uses algorithm selection to initialize its hyperparameter optimization and won
two AutoML challenges" [VERIFIED-FULLTEXT, doi:10.1016/j.artint.2018.10.004, §2.1]; the meta-learning
warm-start there is fitted over ~100 prior datasets (already recorded in `15-ai-preprocessing.md`
§Q3), and `OPENML-WEKA-2017` is that same family's ASlib representative at 105.

### Table

| System / benchmark                    | Year | Instances used for training                   | Candidates                           | Features                 | Verification                                                |
| ------------------------------------- | ---- | --------------------------------------------- | ------------------------------------ | ------------------------ | ----------------------------------------------------------- |
| SATzilla07 (`ALL`)                    | 2008 | 40 % of 4 811 ≈ **1 924**                     | 7                                    | 48                       | [VERIFIED-FULLTEXT] doi:10.1613/jair.2490                   |
| SATzilla07 (`INDUSTRIAL`)             | 2008 | 40 % of 1 021 ≈ **408**                       | 7                                    | 48                       | [VERIFIED-FULLTEXT] same                                    |
| ASlib / OASC 2015                     | 2015 | 296 – 4 021 per scenario, 10 bootstrap splits | 2 – 31                               | 17 – 198                 | [VERIFIED-FULLTEXT] doi:10.1016/j.artint.2018.10.004 Tab. 1 |
| ASlib / OASC 2017                     | 2017 | 2/3 of 100 – 9 720 per scenario               | 5 – 31                               | 37 – 483                 | [VERIFIED-FULLTEXT] ibid. Tab. 2; PMLR 79:1–7 §2            |
| `OPENML-WEKA-2017` (closest analogue) | 2017 | 2/3 of **105**                                | **30**                               | 103                      | [VERIFIED-FULLTEXT] ibid. Tab. 2                            |
| Frugal algorithm selection            | 2024 | six ASlib scenarios, ~10 % of labelling cost  | as ASlib                             | as ASlib                 | [VERIFIED-FULLTEXT] arXiv:2405.11059                        |
| **This project's tuning set**         | 2026 | **4**                                         | 69 scorers / 1 923 variants screened | ~30 descriptors proposed | repo, `../exploration/results/40-method-sweep.md`           |

**What it changes here.** The gap between our n and the field's smallest n is **not a factor of
two**. It is a factor of ~17 against the smallest scenario ever competed, and ~100 against the
smallest training set SATzilla ever used. No amount of methodological care closes a gap of that
size; only more proteins would, and C-side constraints plus ADR 0021 forbid adding them.

---

## Q3. The single best solver, the virtual best solver, and how much of the gap gets closed

### Synthesis

**The two reference points are standard and precisely defined.** From the competitions paper:

> "To be able to assess the performance gain of algorithm selection systems, two baselines are
> commonly compared against: (i) the performance of the individual algorithm performing best on all
> training instances (called _single best solver_ (SBS)), which denotes what can be achieved without
> algorithm selection; (ii) the performance of the _virtual best solver_ (VBS) (also called oracle
> performance), which makes perfect decisions and chooses the best-performing algorithm on each
> instance without any overhead. The VBS corresponds to the overhead-free parallel portfolio that
> runs all algorithms in parallel and terminates as soon as the first algorithm finishes."

[VERIFIED-FULLTEXT, doi:10.1016/j.artint.2018.10.004, §2.4]

**The normalisation is one equation, and its sign convention is a trap.** Equation (2) of the same
paper is

> m̂_s = (m_s − m_VBS) / (m_SBS − m_VBS)

"where 0 corresponds to perfect performance, equivalent to the VBS, and 1 corresponds to the
performance of the SBS. The performance of an algorithm selection system will usually be between 0
and 1; **if it is larger than 1 it means that simply always selecting the SBS is a better
strategy**" [VERIFIED-FULLTEXT, ibid., §2.4]. The 2017 challenge write-up states the same quantity
with the opposite orientation — "1.0 corresponds to a perfect score … and 0.0 corresponds to the
baseline (i.e. the single best solver). A value of less than 0.0 indicates that the algorithm
selection system is worse than the single best solver" [VERIFIED-FULLTEXT, PMLR 79:1–7, eq. (2)].
**Both papers report the same numbers on opposite scales.** Any number we quote from this literature
must carry its orientation, or it will be read backwards.

**How much gets closed, aggregated.** Using the "remaining gap" orientation (0 = VBS, 1 = SBS):

| Competition                                          | Best system | Avg. remaining gap         | Fraction of gap closed |
| ---------------------------------------------------- | ----------- | -------------------------- | ---------------------- |
| 2015                                                 | zilla       | 0.366 (All), 0.344 (PAR10) | ~63–66 %               |
| 2017                                                 | ASAP.v2     | 0.38 (PAR10)               | ~62 %                  |
| 2017, virtual best _selector_ over all 8 submissions | —           | 0.29                       | ~71 %                  |

[VERIFIED-FULLTEXT, doi:10.1016/j.artint.2018.10.004, Tables 3 and 4, and §5.3.] The authors' own
summary: "All systems perform well on average, closing more than half of the gap between virtual
and single best solver" (2015), and "the best systems had a remaining gap between the single best
and virtual best solver of only 38% in 2017" [VERIFIED-FULLTEXT, ibid., §4.1, §5.7]. Progress
between the two was "rather small" [ibid., §5.1].

**How much gets closed, disaggregated — and this is where it stops being encouraging.** The 2017
average gaps (Table 4, on the 0 = VBS / 1 = SBS scale) run: ASAP.v2 0.38, ASAP.v3 0.40, Sunny-fkvar
0.43, Sunny-autok 0.57, `*Zilla` 0.93, `*Zilla(dyn)` 0.96, `AS-RF` **2.10**, `AS-ASL` **2.51**. Two
of eight state-of-the-art submissions were **worse than simply always using the single best
algorithm**, by more than the whole size of the gap; two more sat within 7 % of it
[VERIFIED-FULLTEXT, ibid., Table 4 and Appendix E, Table E.9].

**On the scenario shaped like ours, per-instance selection essentially did not work.**

> "`OPENML-WEKA-2017` was a new scenario in the 2017 competition and appeared to be very
> challenging, as six out of eight submissions performed almost equal to or worse than the single
> best solver (≥ 95% remaining gap)."

[VERIFIED-FULLTEXT, ibid., §5.7]. Table E.9 gives the individual scores on that scenario: ASAP.v2
0.950, ASAP.v3 0.950, Sunny-fkvar 0.787, Sunny-autok 0.877, both `*Zilla` variants **1.000**,
`AS-RF` 3.798, `AS-ASL` 7.233. The best of eight closed 21 % of a gap whose total size was a factor
of **1.02** [VERIFIED-FULLTEXT, ibid., Tables 2 and E.9].

**Two further observations from the same scenario, both of which transfer directly.**

- _Split-to-split variance dominated the ranking at 105 instances._ The organisers ran a plain
  random-forest baseline "on 100 randomly sampled 33% holdout sets" and found that "on half of the
  sampled holdout sets, our baseline was unable to close the gap by more than 10%. In 18% of the
  holdout sets, the baseline performed worse than the SBS. However, our simple baseline achieved
  67.5% remaining gap on the holdout set used in the competition (compared to the best submission
  Sunny-fkvar with 78%)" [VERIFIED-FULLTEXT, ibid., §5.7 and Fig. 7]. A baseline that beat every
  competition entry on the competition split was worse than doing nothing on nearly one split in
  five. **At n = 105.**
- _The competition winner's headline result was a lucky seed._ On `CSP-Minizinc-Obj-2016` — the
  other 100-instance quality scenario — the organisers re-ran ASAP.v2 across 1 500 random seeds and
  found "the actual obtained score (0.025) has a probability of 0.466%"; with the median seed "it
  would have ranked in third place" [VERIFIED-FULLTEXT, ibid., §5.4 and Fig. 6].

**The prize itself is small when the metric is a bounded quality score.** The VBS/SBS improvement
factor is 11–265 on the runtime scenarios and **1.02, 1.04 and 1.7** on the three quality scenarios
[VERIFIED-FULLTEXT, ibid., Tables 1 and 2]. Runtime is unbounded above, so one instance where every
algorithm but one times out creates an enormous oracle gap; a bounded score cannot. **Our endpoint
is AUC, a bounded quality score.** [UNVERIFIED — the mechanism is our reading of the tables, not a
claim the papers make.]

**Consequence the literature makes obvious and we have not yet done.** Before any selector is
designed, compute the SBS and the VBS on the four `development` arms and report m̂ for the trivial
selectors. If the oracle gap on our own benchmark is of the order of the 1.02–1.7 seen on the
quality scenarios, the maximum possible prize from _perfect_ per-protein selection is smaller than
the minimum detectable effect `41-selection-and-power.md` §5 reports (0.794–0.955 AUC at 80 %
power), and the question closes without any selector being built. **This is the cheapest decisive
experiment available and it should precede everything else in this area.**

### Table

| Quantity                        | Definition / value                                                                                  | Verification                                              |
| ------------------------------- | --------------------------------------------------------------------------------------------------- | --------------------------------------------------------- |
| SBS                             | single algorithm best on all training instances; "what can be achieved without algorithm selection" | [VERIFIED-FULLTEXT] doi:10.1016/j.artint.2018.10.004 §2.4 |
| VBS                             | oracle; per-instance best, no overhead; = overhead-free parallel portfolio                          | [VERIFIED-FULLTEXT] ibid.                                 |
| Normalised score                | `(m_s − m_VBS)/(m_SBS − m_VBS)`, 0 = VBS, 1 = SBS, >1 = worse than SBS                              | [VERIFIED-FULLTEXT] ibid. eq. (2)                         |
| Closed gap (OASC orientation)   | `(m_SBS − m_s)/(m_SBS − m_VBS)`, 1 = VBS, 0 = SBS, <0 = worse than SBS                              | [VERIFIED-FULLTEXT] PMLR 79:1–7 eq. (2)                   |
| Typical closure, best system    | ~62–66 % (2015 and 2017)                                                                            | [VERIFIED-FULLTEXT] Tables 3, 4                           |
| Systems worse than SBS, 2017    | 2 of 8 overall; 6 of 8 on `OPENML-WEKA-2017`                                                        | [VERIFIED-FULLTEXT] Table E.9, §5.7                       |
| VBS/SBS factor, quality metrics | 1.02, 1.04, 1.7                                                                                     | [VERIFIED-FULLTEXT] Tables 1, 2                           |
| VBS/SBS factor, runtime metrics | 10 – 413                                                                                            | [VERIFIED-FULLTEXT] Tables 1, 2                           |

---

## Q4. Small-sample regimes — what happens below ~20 instances

### Synthesis

**Direct answer: the recorded search retrieved no study of per-instance algorithm selection with
fewer than roughly 20 training instances.** The closest the community comes is the 100-instance
`CSP-Minizinc` scenarios, of which two thirds are training. Recorded as a negative result under
ADR 0019 — "not retrieved by the recorded search", not "does not exist". §Method lists what was run.

**What does exist is the field's own small-sample failure, one level up.** The competitions treat
each _scenario_ as a sample when they compare selectors to each other, which gives N = 13 in 2015
and N = 11 in 2017. The outcome:

> "In the 2015 competition, none of the differences between the submitted systems were statistical
> significant, whereas in the 2017 competition only some differences where statistical significant.
> Failure to detect a significant difference does not imply that there is no such difference: the
> statistical tests are based on a relatively low number of samples and thus have limited power."

[VERIFIED-FULLTEXT, doi:10.1016/j.artint.2018.10.004, §5.2; the 2015 result is also stated in §4.1
as "According to the Friedman test with post-hoc Nemenyi test, there is no statistically significant
difference between any of the submissions"]. **Eight competing state-of-the-art selectors, thirteen
samples, and the standard test could not separate any of them.** We are proposing to separate
pipeline arms with four.

**The methodological reference the ML community uses says N > 10, in as many words.** Demšar's
recommended omnibus test for comparing k algorithms across N data sets is the Friedman test, whose
statistic "is distributed according to χ²_F with k − 1 degrees of freedom, **when N and k are big
enough (as a rule of a thumb, N > 10 and k > 5)**" [VERIFIED-FULLTEXT, Demšar, _JMLR_ 7:1–30 (2006),
§3.2.2]. His treatment of the paired t-test names the exact bind we are in:

> "The second problem with the t-test is that unless the sample size is large enough (∼ 30 data
> sets), the paired t-test requires that the differences between the two random variables compared
> are distributed normally. … Therefore, for using the t-test we need normal distributions because
> we have small samples, but the small samples also prohibit us from checking the distribution
> shape."

[VERIFIED-FULLTEXT, ibid., §3.1.2]. And his table of critical values for the two-tailed sign test
**begins at N = 5**, where it requires a clean sweep of all five wins; there is no column for N = 4
[VERIFIED-FULLTEXT, ibid., Table 3].

**The exact floors at small n, derived.** Three non-parametric tests, three floors. All are exact
combinatorial facts, not approximations, and all can be checked by hand.

| n     | Perfect rank ordering, two-sided (`2/n!`) | Clean sweep of paired wins, two-sided sign / Wilcoxon (`2/2ⁿ`) |
| ----- | ----------------------------------------- | -------------------------------------------------------------- |
| 3     | 0.333                                     | 0.250                                                          |
| **4** | **0.083**                                 | **0.125**                                                      |
| 5     | 0.017                                     | 0.063                                                          |
| 6     | 0.0028                                    | **0.031**                                                      |
| 7     | 0.00040                                   | 0.016                                                          |

[UNVERIFIED — elementary combinatorics performed in this document; each cell is `2/n!` or `2/2ⁿ`.
The Wilcoxon signed-rank statistic attains the same minimum as the sign test because both are
bounded by the 2ⁿ sign assignments. Demšar's Table 3 admits N = 5 with all five wins, which under
the exact two-sided binomial is p = 0.0625; that mild liberality is noted rather than glossed.]

Read the table for the two numbers that matter:

- **At n = 4, no result of any kind reaches α = 0.05.** Not a perfect descriptor (0.083), not a
  clean sweep of the selector over the SBS on every protein (0.125). The maximum evidence four
  proteins can produce is short of the conventional threshold by a factor of 1.7 to 2.5.
- **The smallest n at which a perfect ordering is significant uncorrected is 5; the smallest n at
  which a clean sweep of wins is significant is 6.**

**And the parametric floor agrees.** `15-ai-preprocessing.md` §Q3 derives the paired minimum
detectable effect at n = 4 as **2.08 · SD_diff** against 0.846 · SD_diff at n = 13, and the
capacity budget as 8 bits at n = 4, m = 4. Nothing in this file contradicts that; this file adds
that the non-parametric floors are hit _before_ the parametric ones, so the choice of test does not
rescue the design.

### Table

| Claim                                                                   | Value                                          | Verification                                                    |
| ----------------------------------------------------------------------- | ---------------------------------------------- | --------------------------------------------------------------- |
| Per-instance AS studies below ~20 instances                             | **none retrieved** by the recorded search      | negative result, ADR 0019                                       |
| Smallest competition scenario                                           | 100 instances (2/3 for training)               | [VERIFIED-FULLTEXT] PMLR 79:1–7 §3                              |
| Selectors compared across 13 scenarios (2015)                           | **no** significant difference between any of 8 | [VERIFIED-FULLTEXT] doi:10.1016/j.artint.2018.10.004 §4.1, §5.2 |
| Friedman-test rule of thumb                                             | **N > 10 and k > 5**                           | [VERIFIED-FULLTEXT] Demšar _JMLR_ 7:1–30 §3.2.2                 |
| Paired t-test needs ~30 data sets for the normality question to be moot | ∼30                                            | [VERIFIED-FULLTEXT] ibid. §3.1.2                                |
| Sign-test critical-value table                                          | starts at N = 5                                | [VERIFIED-FULLTEXT] ibid. Table 3                               |
| Minimum two-sided p, perfect ordering, n = 4                            | **0.083**                                      | [UNVERIFIED] `2/4!`, derived here                               |
| Minimum two-sided p, clean sweep, n = 4                                 | **0.125**                                      | [UNVERIFIED] `2/2⁴`, derived here                               |

---

## Q5. The multiple-comparisons trap in descriptor screening

### Synthesis

**The repo's arithmetic, re-derived independently.** Screen K candidate descriptors against a
target quantity on n instances, and admit a descriptor if it orders the instances exactly as the
target does or exactly backwards. Under the null that a descriptor carries no information, all `n!`
orderings are equally likely, so

- P(one descriptor is perfect, either sign) = `2/n!`
- E[number of perfect descriptors] = `2K/n!`
- P(at least one perfect descriptor) = `1 − (1 − 2/n!)^K`

At n = 4 and K = 30: `2/24 = 0.08333`; expectation `30 × 0.08333 = ` **2.500**; and
`1 − (11/12)³⁰ = 1 − 0.07353 = ` **0.9265**. These reproduce the stated 2.50 and 0.93 exactly.
[UNVERIFIED — combinatorics performed in this document; it agrees to four decimals with the value
the task brief reports, which is the check.]

**The most important reading of the observed count is the one that is easy to miss.** One perfect
ordering was observed where chance alone predicts 2.500. **The screen produced fewer perfect
descriptors than the null expects.** Under a Poisson approximation with mean 2.5, P(X ≤ 1) = 0.287,
so the observation is unremarkable in the _low_ direction. The screen result is not merely
"explainable by chance"; it is slightly below what chance would have delivered. [UNVERIFIED —
Poisson arithmetic performed here: e^{−2.5}(1 + 2.5) = 0.0821 × 3.5 = 0.287.]

**The correction that everyone reaches for does not apply, and the reason is structural.** The
conventional response to K = 30 comparisons is Bonferroni (α/K), Holm's step-down, or
Benjamini–Hochberg FDR control [VERIFIED-ABSTRACT metadata, Benjamini & Hochberg, _JRSS-B_
57:289–300, doi:10.1111/j.2517-6161.1995.tb02031.x; Storey & Tibshirani's q-value,
doi:10.1073/pnas.1530509100]. But at n = 4 the _uncorrected_ two-sided p of a perfect fit is 0.083,
already above 0.05. Bonferroni at K = 30 demands p ≤ 0.001667, which needs `2/n! ≤ 0.001667`, i.e.
`n! ≥ 1200`, i.e. **n ≥ 7** (6! = 720 gives 0.00278 and fails; 7! = 5040 gives 0.000397 and passes).
[UNVERIFIED — derived here.]

> **The multiplicity correction is not what breaks at n = 4. The null's granularity breaks first.**
> No correction can lower a p-value, and the smallest p available is 0.083.

This is the same phenomenon Phipson & Smyth analyse for permutation tests — that the attainable
p-value has a floor set by the number of distinguishable rearrangements, and reporting below that
floor is an artefact [VERIFIED-ABSTRACT metadata, _Stat. Appl. Genet. Mol. Biol._ 9(1),
doi:10.2202/1544-6115.1585]. Here the floor is set not by how many permutations we choose to draw
but by how many exist: `4! = 24`.

**The standard treatment of this failure mode in biomarker discovery, and the names to cite.** The
"p ≫ n, screen many markers, find a perfect one" pattern is the best-documented false-discovery
mechanism in computational biology.

- Simon, Radmacher, Dobbin & McShane, "Pitfalls in the use of DNA microarray data for diagnostic and
  prognostic classification", is the field's canonical warning about exactly this design
  [VERIFIED-ABSTRACT metadata, _JNCI_ 95(1):14–18, doi:10.1093/jnci/95.1.14; the abstract was not
  returned by the Europe PMC record retrieved this session — **the full text was not landed**].
- Ambroise & McLachlan give the measurement. Reported near-zero prediction errors from small gene
  subsets "suffered from a selection bias … because the rule is either tested on tissue samples that
  were used in the first instance to select the genes being used in the rule or because the
  cross-validation of the rule is not external to the selection process"; and once "correction is
  made for the selection bias, the cross-validated error is no longer zero for a subset of only a
  few genes" [VERIFIED-ABSTRACT, _PNAS_ 99(10):6562–6566, doi:10.1073/pnas.102102699].
- Ransohoff, "Bias as a threat to the validity of cancer molecular-marker research"
  [VERIFIED-ABSTRACT metadata, _Nat. Rev. Cancer_ 5:142–149, doi:10.1038/nrc1550].
- Ioannidis's general statement of the mechanism: the probability a claim is true "may depend on
  study power and bias, the number of other studies on the same question, and, importantly, the
  ratio of true to no relationships among the relationships probed in each scientific field", and
  false findings are more likely "when studies are smaller [and] when there is greater flexibility
  in designs, definitions, outcomes and analytical modes" [VERIFIED-ABSTRACT, _PLoS Med._ 2(8):e124,
  doi:10.1371/journal.pmed.0020124].
- Baggerly & Coombes's forensic reconstruction of a high-profile failure is the case study
  [VERIFIED-ABSTRACT metadata, _Ann. Appl. Stat._ 3, doi:10.1214/09-AOAS291].
- The analyst-degrees-of-freedom framing is Simmons, Nelson & Simonsohn, "False-positive psychology"
  [VERIFIED-ABSTRACT metadata, _Psych. Sci._ 22:1359–1366, doi:10.1177/0956797611417632].

**The conventional corrections, and which ones are appropriate here.**

| Correction                               | Controls                               | Applicable to our screen?                                                                                                                                                                                           |
| ---------------------------------------- | -------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Bonferroni / Holm                        | family-wise error                      | Yes in principle; **useless at n = 4** because the uncorrected floor already exceeds α. Already the repo's convention (`46-beats-distance.md` uses Holm)                                                            |
| Benjamini–Hochberg FDR / Storey q        | false discovery rate                   | Same objection. FDR is _more_ permissive than FWER, and even it cannot go below 0.083                                                                                                                               |
| Westfall–Young / permutation max-T       | FWER **under dependence**              | The right family when descriptors are correlated — and ours are: `41-selection-and-power.md` §4 measures ~8.9–10.6 effective independent directions among 1 620 variants. But it still cannot beat the `2/n!` floor |
| External / nested cross-validation       | selection bias in the error estimate   | Yes, and mandatory if anything is tuned (Ambroise & McLachlan; Varma & Simon and Cawley & Talbot, already in `15-ai-preprocessing.md` §Q3). At n = 4 it controls bias while leaving variance untouched              |
| Stability selection                      | false discoveries under subsampling    | Meinshausen & Bühlmann, doi:10.1111/j.1467-9868.2010.00740.x. Needs subsamples; at n = 4 there are 4 leave-one-out subsets, which is not a resampling distribution                                                  |
| Valid post-selection inference           | inference _after_ a data-driven choice | Berk et al., doi:10.1214/12-AOS1077; Taylor & Tibshirani, doi:10.1073/pnas.1507583112. Conceptually the right frame; the price is wider intervals, which n = 4 cannot afford                                        |
| Pre-registration + held-out confirmation | everything above, by construction      | **The only one that works at our n.** It is also what the competitions themselves do (2/3 train, 1/3 test) and what our `generalisation` tier is for                                                                |

[All rows: DOIs verified by Crossref metadata retrieval this session. The applicability judgements
are ours, marked UNVERIFIED as inference.]

**One caution about the effective K.** Bonferroni over K = 30 would be conservative if the 30
descriptors were as correlated as our 1 620 pipeline variants proved to be (~9–11 effective
directions, `41-selection-and-power.md` §4). But correlated descriptors make the null _narrower_,
not the floor lower: the `2/n!` bound is per-descriptor and does not move. Correlation changes
E[perfect] and P(≥1) — with K_eff = 10 instead of 30, E = 0.833 and P(≥1) = 0.579 — but the
individual p-value floor is unchanged. [UNVERIFIED — derived here: `1 − (11/12)¹⁰ = 0.5793`.]

---

## Q6. What the literature recommends when you cannot fit a selector

### Synthesis

Three families, in increasing order of how much they ask of the data. All three are compatible with
C1–C6.

**(a) Pick one algorithm, but pick it on the worst case rather than the mean.** The SBS as the
competitions define it is "the individual algorithm performing best on all training instances" —
a mean over the instance set [VERIFIED-FULLTEXT, doi:10.1016/j.artint.2018.10.004, §2.4]. A
minimax variant instead maximises the _minimum_ per-instance score. The hypothesis class is
identical in size (choose 1 of m), so nothing extra is being fitted, but the objective changes to
the one our deliverable actually needs: no protein on which the method collapses.

The algorithm-selection literature's own move in this direction is decision-theoretic and
risk-averse: Tornede et al.'s Run2Survive builds distributional runtime models and "advocate[s] a
risk-averse approach to algorithm selection, in which the avoidance of a timeout is given high
priority" [VERIFIED-ABSTRACT, arXiv:2007.02816]. The structural point transfers even though the
timeout does not: when the loss is asymmetric — and ours is, because one arm below chance
invalidates a per-target deliverable — expected performance is the wrong criterion.

Our repo already computes this quantity and it is already discriminating.
`../exploration/results/44-stability-and-noise.md` §6 reports that of 32 combinations of clock,
window and observable, **zero** place all four development arms above 0.5, and that the best of them
has a worst arm at 0.375. A worst-arm criterion separates candidates that a mean does not.

**Caveat, stated because it is real:** a minimum over four values is a high-variance statistic, and
its sampling distribution at n = 4 is wide. Minimax at n = 4 is _cheaper to justify_ than a fitted
selector, not _well estimated_. Report it as a screening criterion, not as an estimate.

**(b) Run the portfolio and combine, without selecting.** The literature's answer when the selector
cannot be trusted is a schedule or an ensemble.

- _Static, feature-free schedules win competitions._ "One variant of algorithm schedules are static
  (instance-features free) pre-solving schedules which are applied before any instance features are
  computed" [VERIFIED-FULLTEXT, doi:10.1016/j.artint.2018.10.004, §2.3], and "In AI planning, a
  simple static portfolio of planners (fast downward stone soup) won a track at the International
  Planning Competition (IPC) in 2011" [VERIFIED-FULLTEXT, ibid., §2.1 — the primary Helmert, Röger &
  Karpas workshop paper was not retrieved this session]. `aspeed` computes such schedules by answer
  set programming from benchmark data alone [VERIFIED-ABSTRACT, Hoos, Kaminski, Lindauer & Schaub,
  _TPLP_ 15:117–142, doi:10.1017/S1471068414000015]. The foundational statement of the idea is
  Gomes & Selman's "Algorithm portfolios" [VERIFIED-ABSTRACT metadata, _Artif. Intell._ 126:43–62,
  doi:10.1016/S0004-3702(00)00081-3].
- _Our field's own version is the consensus site predictor._ metaPocket combines four binding-site
  predictors and "improves the success rate from approximately 70 to 75% at the top 1 prediction"
  on 48 unbound/bound and 210 bound structures [VERIFIED-ABSTRACT, _OMICS_ 13:325–330,
  doi:10.1089/omi.2009.0045]. No per-protein selector; a fixed combination.
- _Our repo has already measured the analogue and it works on the axis it was aimed at._ Rank-mean
  ensembling over K jittered copies raises held-out stability from **0.581 to 0.888** at K = 16
  with a mean AUC change of −0.015, and the controls stay flat, which is what makes the result
  readable [`../exploration/results/44-stability-and-noise.md` §4]. Two costs are recorded there
  and must be carried: the correlation to distance rises from 0.496 to 0.613, which is the wrong
  direction against `46-beats-distance.md`, and K = 16 multiplies circuit executions by 16 under C3.
- _The decision rule between selecting and ensembling is already in the repo._
  `15-ai-preprocessing.md` §Q3 states it: selection beats ensembling when the selector's own error
  is small relative to the spread between candidates, and ensembling wins otherwise. At n = 4 the
  selector's error is large by construction. **This file's contribution is to give that rule a
  number: the selector's own error at n = 4 has a p-value floor of 0.125.**

**(c) Derive the adaptation rule instead of learning it — and check it has a mechanism.** A rule
with no fitted parameters has pseudo-dimension 0 and needs no validation set, which is why
`15-ai-preprocessing.md` §Q3 recommends the family (local scaling, eigengap, Markov stability,
stability selection). Not restated here. **What this file adds is that we have already run the
member of that family that most obviously applied, and it did not work.**

`../exploration/results/44-stability-and-noise.md` §6 tests a spectrally normalised clock: divide
the propagation time by the spectral gap, so that every protein covers the same number of periods
of its own slowest mode. It reads only the graph's own spectrum and never a label — a textbook
derived, parameter-free per-instance adaptation. The measured outcome:

- it worked **as designed**: within-arm window sensitivity for `ctqw_average_transfer` fell from
  0.079 to 0.045;
- it changed nothing that mattered: between-arm AUC spread moved by 0.011, which is 2 % of itself;
- the ratio it was meant to fix got **worse**, from 8.5× to 14.5×, because the denominator shrank;
- and zero of 32 settings put all four arms above chance.

> **A derived rule needs no validation set, but it still needs a mechanism.** Ours normalised a
> variance that was never the variance that mattered. "Parameter-free" buys statistical
> admissibility; it does not buy an effect.

**(d) The option the challenge already allows: do not adapt.** `CHALLENGE.md` requires a per-target
hit list and connectivity matrix. Reporting one fixed pipeline with its four per-protein numbers
visible, including the worst, is a complete deliverable. Adaptation is an optimisation on top of
it, not a requirement of it.

### Table

| Alternative                               | What it asks of the data                                       | Precedent                                                       | Repo status                                                                              | Verification                                                                                                         |
| ----------------------------------------- | -------------------------------------------------------------- | --------------------------------------------------------------- | ---------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| SBS on the mean                           | 1 choice among m; n instances to estimate m means              | the competitions' own baseline                                  | computable now                                                                           | [VERIFIED-FULLTEXT] doi:10.1016/j.artint.2018.10.004 §2.4                                                            |
| **SBS on the worst case (minimax)**       | 1 choice among m; high-variance at n = 4 but nothing fitted    | risk-averse AS, Run2Survive                                     | already discriminating (`44` §6: 0 of 32 clear all four arms)                            | [VERIFIED-ABSTRACT] arXiv:2007.02816                                                                                 |
| Static, feature-free schedule / portfolio | **nothing per-instance**                                       | Fast Downward Stone Soup won IPC-2011; `aspeed`; Gomes & Selman | not tried in this form                                                                   | [VERIFIED-FULLTEXT] §2.1, §2.3; [VERIFIED-ABSTRACT] doi:10.1017/S1471068414000015, doi:10.1016/S0004-3702(00)00081-3 |
| Consensus / rank aggregation              | **nothing per-instance**, no label                             | metaPocket 70 %→75 % top-1                                      | **measured**: stability 0.581→0.888, ΔAUC −0.015, distance ρ 0.496→0.613                 | [VERIFIED-ABSTRACT] doi:10.1089/omi.2009.0045; repo `44` §4                                                          |
| Derived, parameter-free adaptation        | nothing fitted; needs a mechanism                              | local scaling, eigengap, Markov stability (`15` §Q3)            | **tried and negative**: spectral-gap clock, spread −0.011 (2 %), 0 of 32 settings usable | repo `44` §6                                                                                                         |
| Fitted per-instance selector              | `m ≥ c(H/ε)²(d + ln(1/δ))`; hundreds to thousands of instances | SATzilla, ASAP, Sunny                                           | **not admissible at n = 4**                                                              | [VERIFIED-FULLTEXT] arXiv:1511.07147 §3                                                                              |

---

## Q7. Verdict — is a fitted per-protein selector defensible at n = 4?

**No.** Four independent floors block it, and they do not share a mechanism, so no single fix moves
more than one of them.

1. **Combinatorial floor.** The best possible descriptor at n = 4 has two-sided p = 2/4! = 0.083.
   No correction lowers a p-value, so the screen cannot produce a significant result at α = 0.05
   even in the limit of a perfect fit. [derived, §4–§5]
2. **Paired-comparison floor.** A selector that beats the fixed pipeline on all four proteins gives
   a two-sided sign-test or Wilcoxon p of 0.125. The parametric version is the same conclusion by a
   different route: MDE = 2.08 · SD_diff (`15-ai-preprocessing.md` §Q3). [derived, §4]
3. **Sample-complexity floor.** Gupta & Roughgarden's uniform-convergence condition at the most
   generous parameter values gives ε ≈ 1 at m = 4 — a vacuous guarantee — and Balcan, Sandholm &
   Vitercik prove that for a large portfolio "overfitting is inevitable, even with an extremely
   simple algorithm selector". Our portfolio is 69 scorers over 1 923 variants. [§1]
4. **Empirical floor.** The field's smallest competed instance count is 100, its smallest training
   set ~67, and on the one scenario shaped like ours — 105 instances, 30 candidates, a bounded
   quality metric, VBS/SBS = 1.02 — six of eight state-of-the-art selectors failed to beat the
   single best algorithm. [§2–§3]

**The smallest n at which it becomes defensible, by criterion.** Stated as a ladder because
different claims need different rungs.

| Claim you want to make                                                                  | Smallest n           | Source                     |
| --------------------------------------------------------------------------------------- | -------------------- | -------------------------- |
| "This descriptor orders the proteins better than chance" (one descriptor, uncorrected)  | **5**                | `2/5! = 0.017 ≤ 0.05`      |
| "The adapted pipeline beat the fixed one on every protein" (sign / Wilcoxon, two-sided) | **6**                | `2/2⁶ = 0.031 ≤ 0.05`      |
| "This descriptor survived a screen of 30" (Bonferroni)                                  | **7**                | `2/7! = 0.00040 ≤ 0.05/30` |
| "These k candidates differ across proteins" (Friedman + Nemenyi)                        | **> 10**, with k > 5 | Demšar's rule of thumb     |
| "This selector beats the SBS" with the field's own conventions                          | **≈ 100**            | smallest competed scenario |

**Our arithmetic against that ladder.** The tuning set is 4. The held-out `generalisation` tier is
5 and is closed until the method is frozen (ADR 0021), and opening it to raise n would spend the
only confirmation the project has — trading the thing being defended for the defence. Even a merged
4 + 5 = 9 sits below Demšar's N > 10, and would leave nothing held out. **There is no route from
this benchmark to a defensible fitted selector.**

**The honest alternatives, in the order they should be attempted.**

1. **Measure the prize before building the machine.** Compute the SBS and the VBS on the four
   `development` arms through `allo.scoring.score_arm` and report `(m_s − m_VBS)/(m_SBS − m_VBS)`.
   If the oracle gap is of the order the field sees on bounded quality metrics (1.02–1.7×), a
   _perfect_ selector would win less than `41-selection-and-power.md` §5's minimum detectable
   effect, and the question closes with one cheap experiment. This should precede everything else.
2. **Choose one arm on the worst case, not the mean.** Nothing is fitted; the criterion matches the
   per-target deliverable; and `44` §6 shows it already separates candidates that a mean does not.
   Report it as a screening rule with its variance acknowledged, not as an estimate.
3. **Aggregate rather than select.** Rank-mean over the portfolio is label-free, already
   implemented, and already measured (`44` §4). Report its two costs — the distance correlation
   rises and the C3 shot budget multiplies by K — in the same breath.
4. **If an adaptation rule is wanted, derive it and state its mechanism in advance.** A
   parameter-free rule needs no validation set. It does need a reason to work, and `44` §6 is the
   worked example of one that was correctly derived and had no effect. Pre-register the rule and
   the seed before scoring, per `15-ai-preprocessing.md` §Q5 item 6.
5. **Write the negative result up.** "We considered per-protein adaptation, computed the sample
   complexity, and found n = 4 cannot support it" is a stronger paragraph in `docs/report/` than a
   selector whose validation a reviewer can dismantle with `2/4! = 0.083`.

---

## What this changes for our pipeline

- **S0 / front end — blocked.** No fitted per-protein selector, no learned meta-model over
  descriptors, and no descriptor admitted on the strength of a screen at n = 4. The blocking
  argument is `2/n!`, and it is arithmetic, not judgement. This tightens
  `15-ai-preprocessing.md` §Q3's conclusion ("with 4–13 proteins a learned per-instance selector
  cannot be validated") from a power argument to an exact combinatorial one.
- **S0 / front end — the one descriptor result already in hand is not evidence.** One perfect
  ordering at n = 4, K = 30 sits _below_ the null expectation of 2.500. It must not be carried into
  `docs/report/` as a finding, and if it is mentioned it must be mentioned with 2.500 beside it.
- **New experiment, highest priority, cheap.** Compute SBS, VBS and the normalised gap on the four
  `development` arms. It bounds the maximum possible value of every adaptation idea in the project
  and it costs one pass over numbers we already have. Register it in `experiments/REGISTRY.md`.
- **S5 / propagation — the coherence-window question is settled by this file, not reopened.**
  `44` §5 says a per-protein window fails "because nothing selects it". This file says a fitted
  selector cannot be built at our n and a derived one was already measured as ineffective. The
  window should be fixed by a stated rule and reported as a limitation.
- **S7 / site assembly — prefer aggregation.** Rank-mean over the portfolio is the measured remedy
  and the literature's recommendation at small n. Carry its two costs explicitly.
- **Scoring and reporting.** Adopt the SBS/VBS vocabulary and equation (2) verbatim, with its
  orientation stated, wherever we compare a method to a fixed baseline. It is the field's standard
  and it makes "our method is better" a number rather than an adjective.
- **`docs/report/` — a limitation to state, not hide.** N = 4 for tuning and 5 for confirmation is
  below every threshold the algorithm-selection field uses. Saying so, with this ladder, is
  cheaper than having a reviewer find it.

---

## Method

**Databases and routes.** arXiv (abs pages, the `export.arxiv.org` API, and the ar5iv HTML
renderer), Crossref REST API (`api.crossref.org`), Europe PMC REST search
(`www.ebi.ac.uk/europepmc/webservices/rest/search`), JMLR, PMLR, AAAI OJS, and direct PDF retrieval
from publisher and author-hosted copies. **All eight PDFs attempted returned unusable text through
the HTML converter**; five were recovered by reading the retrieved file page-by-page, and three
(the AAAI camera copy of doi:10.1609/aaai.v35i14.17451, Roughgarden's author copy of the SICOMP
version, and the author-hosted copy of the competitions report) were dropped in favour of an
equivalent route. Any claim whose only source was a dropped PDF is marked as unreached below.

**Queries run.** `Gupta Roughgarden "A PAC approach to application-specific algorithm selection"
pseudo-dimension sample complexity bound`; `Balcan Sandholm Vitercik "Generalization in
portfolio-based algorithm selection" sample complexity lower bound`; `ASlib benchmark library
algorithm selection Bischl 2016 single best solver virtual best solver number of instances per
scenario`; `"OPENML-WEKA-2017" ASlib scenario 105 instances algorithm selection competition single
best solver`; `SATzilla portfolio-based algorithm selection Xu 2008 JAIR training instances
"empirical hardness models"`; `algorithm selection "training set size" learning curve "number of
instances" required to outperform single best solver`. arXiv API: `ti:"SATzilla"`;
`abs:"algorithm selection" AND abs:"cold start"`; `abs:"algorithm selection" AND abs:"small number
of instances"` (**0 results**); `abs:"algorithm selection" AND abs:"training instances"`;
`all:"algorithm selection" AND all:"how many instances"` (**0 results**). Europe PMC:
`TITLE:"Pitfalls in the use of DNA microarray data for diagnostic and prognostic classification"`;
`TITLE:"Selection bias in gene extraction on the basis of microarray gene-expression data"`;
`TITLE:"MetaPocket"`; `DOI:"10.1371/journal.pmed.0020124"`. Crossref: two batched `filter=doi:…`
queries covering 18 DOIs, plus one `query.bibliographic` lookup to establish
doi:10.1016/j.artint.2018.10.004.

**Counts.** Four web searches returned results and two were refused after the session's search
budget was exhausted at 200 calls, after which all retrieval went through the API and direct-URL
routes listed above. 32 document fetches were performed. Five PDFs were then read directly
page-by-page over 8 page-range reads (OASC-2017 setup; the competitions report ×3 ranges; SATzilla
×2 ranges; Frugal Algorithm Selection; Demšar). **23 distinct DOIs** were resolved through Crossref,
Europe PMC or a publisher record, and all 23 returned records. Roughly 45 candidate sources were
screened; 24 are cited.

**Full-text landed** (read from the paper's own pages this session): Gupta & Roughgarden
arXiv:1511.07147 §3 (via ar5iv); Lindauer, van Rijn & Kotthoff, _Artif. Intell._ 272 (2019) 86–100,
§§1–5 and Appendices B–E; Lindauer, van Rijn & Kotthoff, PMLR 79:1–7, §§1–3 and Table 1; Xu, Hutter,
Hoos & Leyton-Brown, arXiv:1111.2249 §§3.1–4.3; Demšar, _JMLR_ 7:1–30, §§3.1–3.2; Kuş et al.,
arXiv:2405.11059 §§4–6.

**Abstract-level only:** Balcan, Sandholm & Vitercik (doi:10.1609/aaai.v35i14.17451); Balcan et al.
(arXiv:1908.02894); Tornede et al. (arXiv:2007.02816); Ambroise & McLachlan
(doi:10.1073/pnas.102102699); Ioannidis (doi:10.1371/journal.pmed.0020124); Huang
(doi:10.1089/omi.2009.0045); Hoos et al. (doi:10.1017/S1471068414000015).

**Metadata-record only** (citation confirmed, abstract not retrieved): Benjamini & Hochberg; Storey
& Tibshirani; Simon et al.; Ransohoff; Baggerly & Coombes; Simmons et al.; Berk et al.; Taylor &
Tibshirani; Meinshausen & Bühlmann; Phipson & Smyth; Wolpert & Macready; Gomes & Selman; Bischl
et al.; Kerschke et al.

**Could not be reached.** (i) The abstract of Simon et al. 2003 — the Europe PMC record carries
bibliographic and indexing data but no abstract text, and the full text was not landed; the claim
is cited at metadata level only. (ii) Helmert, Röger & Karpas's Fast Downward Stone Soup workshop
paper — the IPC-2011 result is cited **as reported by** Lindauer et al. §2.1, not from the primary
source. (iii) Balcan, Sandholm & Vitercik's actual sample-complexity theorem and its dependence on
portfolio size _k_ — the AAAI PDF did not convert and the arXiv abstract does not state the scaling;
only the qualitative "large portfolio ⇒ inevitable overfitting" claim is verified. (iv) No paper
performing per-instance algorithm selection with fewer than ~20 training instances was retrieved by
any of the queries above.

**Stopping rule.** Retrieval stopped when the four floors in §7 were each supported by at least one
full-text-verified source and one independent derivation, and when three further queries aimed at
the sub-20-instance regime returned either zero results or the same 100-instance ASlib scenarios
already recorded. The negative result in §4 is reported as "not retrieved by the recorded search"
per ADR 0019 and is not an absence-of-prior-art claim.

**Numbers derived rather than retrieved, listed so they can be checked.** `2/4! = 0.0833`;
`30 × 2/24 = 2.500`; `1 − (11/12)³⁰ = 0.9265`; `1 − (11/12)¹⁰ = 0.5793`; Poisson `P(X ≤ 1 | λ=2.5)
= 0.287`; `2/2⁴ = 0.125`, `2/2⁵ = 0.0625`, `2/2⁶ = 0.03125`; `2/5! = 0.01667`, `2/6! = 0.002778`,
`2/7! = 0.000397`; and the Gupta–Roughgarden reading `m = 4/ε²` at `d = 1, H = 1, δ = 0.05, c = 1`
giving `ε = 1.00` at `m = 4`, `m = 400` at `ε = 0.10` and `m = 1600` at `ε = 0.05`. All are marked
[UNVERIFIED] at the point of use, in the sense of `00-conventions.md` §2: the formulae are verified,
the arithmetic on them is ours.
