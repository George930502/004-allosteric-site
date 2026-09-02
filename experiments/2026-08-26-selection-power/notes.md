# selection-power

**Date:** 2026-08-26 · **Config:** `config.yaml` · **Metrics:** `metrics.json`
**Write-up:** `docs/method/exploration/results/41-selection-and-power.md`

## Question

The method sweep screens thousands of variants on four arms and reports the best. How much of
that best is selection, how many of those variants are independent, and what effect can four
arms resolve?

## Setup

Three passes, all on the `development` tier, all through the frozen harness.

1. **`null_auc`** — 125 label-blind spatially autocorrelated fields at each of four
   correlation lengths, per arm, scored by `score_arm`. Not a uniform random score: a uniform
   score has no spatial autocorrelation and every real method has some.
2. **`effective_dimension`** — participation ratio of the eigenvalue spectrum of the
   variant-by-variant rank correlation matrix, 150 variants on `mkp5`.
3. **`detectable_effect`** — the frozen calibration module's own sensitivity pass at
   α = 0.0167 and 80 % power, which the committed calibration ran only on the primary five.

The first pass also feeds a best-of-V simulation, 20000 draws, at V from 1 to 10000.

## Result

| Quantity                                   | Value             |
| ------------------------------------------ | ----------------- |
| Label-blind AUC, median per arm            | 0.495 – 0.528     |
| Label-blind AUC, p95 per arm               | 0.731 – 0.794     |
| Best-of-3000 mean AUC, median              | **0.771**         |
| Best-of-3000 mean AUC, p95                 | 0.810             |
| Effective independent variants, 150-variant subset | 3.88 (2.6 %) — **superseded**, see below |
| Effective independent variants, full 1620-variant screen | **8.86** (`mkp5`) · **10.58** (`ptp1b`) |
| Share of variance in the leading direction | 0.228 · 0.213     |
| Median absolute pairwise correlation       | 0.238 · 0.184     |
| Minimum detectable AUC at α/3, 80 % power  | **0.794 – 0.955** |

## Interpretation

**This experiment's own falsifier fired, and the headline moved.** The first pass measured the
participation ratio on a 150-variant subset and scaled it linearly to the full sweep. The notes
below named that extrapolation as the thing to test. It was tested on the finished
1620-variant screen and it was **wrong by more than an order of magnitude**: the effective V is
about 10, not 155. The participation ratio does not scale with the variant count, because added
variants are mostly copies of directions already present.

**The ceiling is therefore an interval, not a number.** At the measured effective V ≈ 10 the
label-blind p95 is 0.707. At the raw count it is 0.810. The participation ratio is a variance
measure used on a tail statistic, so it is a **lower** bound on the effective V and the raw
count is an **upper** bound.

**The screen's best variant reaches 0.810** — above the lower ceiling, on the upper one, and
above the 0.794 floor of the detectable band. **It is still not a result**, for a reason that
needs neither boundary: **0 of 1923 variants reject the matched-patch null on all four arms**.
Only a pre-specified test on unseen arms can produce one, which is what
`docs/method/exploration/results/42-threats-and-confirmation.md` §4 lays out.

**Which axis buys independence, measured on `mkp5`.** 54 scorers on one graph with no
detrending hold 3.45 directions. Adding all eight graphs takes that to 4.08. Adding all five
confound-removal forms on one graph takes it to 7.22. **The graph axis buys 0.6 directions for
eight times the compute. The confound-removal axis buys 3.8.** The 54-scorer battery holding
only 3.45 directions is the algebra of
`docs/method/exploration/lit/22-transport-formalisms.md` — most propagation scores are one
operator read at one source column — arriving as a measured number.

**Read the calibrated p, not the AUC.** The matched-patch null is matched on size, components,
mean degree and radius of gyration, so it already absorbs the spatial structure that produces
the ceiling. The AUC is a description. The calibrated p is the test.

**A defect was found and fixed while making this number reproducible.** The dimension pass
ranked its score vectors with `np.argsort(np.argsort(values))`, which gives ordinal ranks.
Spearman is defined on midranks. Several scorers tie heavily — `degree`, `core_number`,
`hop_distance_from_source_negated` — so ordinal ranks broke those ties by residue position.
That made the correlation matrix depend on array order and **overstated how independent two
scorers are**. The helper now calls `scipy.stats.rankdata`.

The defect is contained. It lived only in this pass, never in `allo.scoring`, so no AUC, no
p-value and no record in any `records.jsonl` depends on it. The uncorrected run reported 9.15
and 10.72 where the corrected run reports 8.86 and 10.58, and every axis slice moved the same
way. The direction was predictable: inflated independence, therefore an inflated effective V,
therefore an inflated noise ceiling. The correction moves the ceiling down, which favours the
screen rather than the reverse.

**What would change this.** The effective dimension is now measured on two arms of four, over
the full screen. `mkp5` gives 8.86 and `ptp1b` gives 10.58, so the quantity replicates within
two directions. `hiv_rt` and `ns5b` were not measured, because the solve costs about 20 minutes
per arm at 550 residues and the two measured arms agree. A materially different ratio on a
third arm would move the lower ceiling. Narrowing the interval between the two ceilings needs a
direct best-of-V simulation over the screen's own correlation structure, and that was not
run.

**Falsifier for the headline.** If a method's calibrated p from the matched-patch null clears
0.05/4 on every one of the four arms, then the ceiling argument does not apply to it: the
matched null is not the AUC, and clearing it four times independently is not what a
best-of-3000 draw produces. The check is one query over the three `records.jsonl` files, and
its result is in `docs/method/exploration/results/40-method-sweep.md` §2: **zero of 1923**, at
0.05 and at 0.05/4.
