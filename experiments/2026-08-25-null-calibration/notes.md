# Null calibration — the matched-patch permutation test

> **Amended 2026-08-25 by the version-2 audit.** This experiment was re-run after
> `docs/benchmark/evaluation/AUDIT.md` found two defects that changed what it must measure.
> The `gate` stage now reports a **`size_ratio`** calibrated at every Holm level, not only an
> `alpha_star` calibrated at alpha, because a one-parameter rescale fitted at one threshold
> leaks FWER at the others. The `power` stage now runs at **every** Holm level for the same
> reason. `alpha_star` is still reported for disclosure and nothing computes with it. The
> type-I measurements below are unchanged and reproduce bit-for-bit. ADR 0025.

**Question.** At what matching tolerance does the matched-patch permutation test hold its
size on the frozen arms, does it still reject when the score knows the answer, and what
effect size can it then detect?

ADR 0018 blocks scoring until the first two are measured. The third replaces the two
closed-form power columns the draft protocol withdrew.

```bash
uv run allo evaluate calibrate experiments/2026-08-25-null-calibration/config.yaml
```

Seed 0. Everything that moves a number is in `config.yaml`. Raw output is `metrics.json`.

## Setup

Three stages, answering different questions.

1. **search** — sweep the tolerance at 999 replicates. Where the tolerance is *chosen*.
2. **gate** — run the chosen tolerance at 9999 replicates, the count scoring uses, on all 14
   frozen arms. Where the tolerance is *verified* and each arm's `alpha_star` is measured.
3. **power** — bisect on an added effect until the real test reaches 80 % power, at each
   arm's calibrated threshold.

**The data-generating model for the null** is a Gaussian field over the candidate residues
with covariance `exp(-d/λ)` on Cα distances, drawn by Cholesky factorisation. It is
site-uninformative by construction: nothing in it knows where the label set is. Any rejection
rate above α is therefore the test failing to hold its size, and any rate below it is the test
throwing away power. λ runs 4, 8, 12 and 20 Å — about one contact shell up to a smooth
gradient across a small domain — because the type-I rate depends on λ and a gate at one value
would prove nothing about the others.

**The positive control** is minus the distance to the nearest scoreable label. It is
evaluation-side only and never touches the prediction path. A null that rejects nothing passes
a type-I band perfectly, so this end of the gate is what makes the other end meaningful.

## Result 1 — the unmatched null is unusable, and that is why the matched one exists

Measured type-I rate of the plain background permutation: **0.10 to 0.32**, rising
monotonically with λ on all 14 arms. The draft protocol claimed 0.16–0.18 from an uncommitted
session. The committed measurement is worse.

An allosteric label set is a spatially contiguous, partly buried patch. Any connectivity score
favours contiguous buried residues. Drawing m residues uniformly asks whether these m beat m
random ones, and a method answers that correctly by finding any buried blob.

## Result 2 — the matched null does not hold its size everywhere either

At the frozen tolerance 0.10 and 9999 replicates, against the exact central binomial
prediction interval **[0.037, 0.064]** at n = 1000 fields:

- **In band, 7 arms:** both KRAS arms, `ecoli_cps`, `hiv_rt`, `ns5b`, `ptp1b`, `smyd3`.
- **Above band, 6 arms:** both BCR-ABL1 arms (0.059–0.075), `chk1`, `glucokinase`, `mkp5`,
  `p97_vcp` (up to 0.077).
- **Below band, 1 arm:** `cardiac_myosin_corrected` (0.034–0.037).

This is systematic, not a property of one protein. Tightening the tolerance to 0.05 makes
BCR-ABL1 **worse** (0.066–0.089) and drops the sampler's acceptance rate on myosin to 0.0027.
Loosening it to 0.20 is worse again.

**The positive control passes decisively.** The oracle score returns p = 0.0001 on all 14
arms, the smallest value 9999 replicates can produce.

## Result 3 — why, measured rather than guessed

The variance of a patch mean under a spatially autocorrelated score is

```
Var = m^-2 * sum_ij exp(-d_ij / lambda)
```

a functional of the **entire** within-patch distance distribution. Radius of gyration is only
its second moment about the centroid. Two patches with equal size and equal radius of gyration
can differ in that sum.

The observed patch's own value of that sum, expressed as a percentile inside its matched pool,
orders the arms exactly as the type-I rate does (λ = 8 Å):

| Arm | percentile | measured type-I |
| --- | ---: | ---: |
| `cardiac_myosin_corrected` | 32.5 % | 0.034 |
| `kras_g12c_mandated` | 55.6 % | 0.048 |
| `kras_g12c_corrected` | 57.3 % | 0.055 |
| `bcr_abl1_mandated` | 70.1 % | 0.066 |
| `bcr_abl1_corrected` | 76.7 % | 0.067 |

Above the median, the null's members have systematically lower variance than the observed
statistic and the test over-rejects. Below it, the test under-rejects.

**Two repairs were tested and both failed.**

- Adding mean within-patch pairwise Cα distance changes nothing: 97–99 % of the pool already
  satisfies it within ±10 %, and the percentiles move by at most one point.
- Internal contact count correlates with the variance factor at only ρ ≈ 0.6–0.8, and it does
  not order the arms correctly.

Matching the variance factor itself is not available in advance, because λ is a property of
the **method's** score field and not of the benchmark.

## Result 4 — what the calibrated test can detect

Bisection on a constant shift added to the label residues, 300 fields per evaluation, at each
arm's `alpha_star` rather than at the nominal α. The field has unit marginal variance, so the
shift reads as Cohen's d. The AUC is the median actually achieved at that shift.

| Arm | λ = 4 Å | λ = 8 Å | λ = 12 Å | λ = 20 Å |
| --- | --- | --- | --- | --- |
| `kras_g12c_mandated`       | 1.00 / 0.774 | 1.17 / 0.833 | 1.20 / 0.858 | 1.15 / 0.883 |
| `kras_g12c_corrected`      | 1.02 / 0.778 | 1.21 / 0.836 | 1.25 / 0.863 | 1.20 / 0.887 |
| `bcr_abl1_mandated`        | 0.95 / 0.773 | 1.22 / 0.835 | 1.35 / 0.867 | 1.43 / 0.913 |
| `bcr_abl1_corrected`       | 1.00 / 0.762 | 1.31 / 0.850 | 1.38 / 0.880 | 1.36 / 0.908 |
| `cardiac_myosin_corrected` | 1.02 / 0.769 | 1.37 / 0.850 | 1.52 / 0.897 | 1.63 / 0.936 |

**The answer is a band, AUC-ROC 0.76 to 0.96, and it has two axes: λ, and which Holm step the
arm draws.** At alpha the band is 0.762-0.936; at alpha/3 it is 0.799-0.961. A method whose
score field varies on a 4 Å scale is detected at AUC ≈ 0.77. The same method with a 20 Å field
needs AUC ≈ 0.90. That is a real property of a patch-based test and the draft's single number
hid it.

At fixed λ the band is flat across arms to within 0.06, although prevalence spans 6.79× and
candidate counts span 5×. **Label patch geometry, not arm size, sets the sensitivity.**

Published AUC in the elastic-network and network-communication family sits around 0.75–0.82
where it is reported at all. That overlaps only the short-correlation end. **An ordinary
publishable result in this sub-field can fail on this benchmark**, and the report has to say
so before its numbers rather than after them.

## Interpretation, and the decision

Calibrate the threshold rather than match the null further (ADR 0023). Each arm carries
`size_ratio`, the factor by which the observed statistic's null is wider than the pool
members', taken as the maximum across Holm levels and across
the four correlation lengths and capped at α. `score_arm` reports
`p_calibrated = max(p, sf(isf(p) / size_ratio))`, rescaled on the probit scale. The linear
form this first used is size-exact at alpha and wrong at every other threshold (ADR 0025).

Two properties are worth stating plainly. `p_calibrated` is exact at the decision boundary and
only approximate away from it, so it is a decision rule and not a calibrated p-value. And the
Monte Carlo error in a 5th-percentile estimate from 1000 draws is real, which — together with
the extremum over four λ and three levels — biases the ratio upward. Only the second is
one-sided: the sampling error in a single tail quantile is symmetric and can land either way.
"Both push toward a smaller test" was wrong as written. The extremum pushes toward a smaller
test, which
is the direction that cannot manufacture a result.

**Negative result worth keeping.** The tolerance sweep found no value at which every arm holds
its size. 0.05, 0.10 and 0.20 all fail, and they fail on different arms. A future attempt at
a fully matched null must add a property that captures the short-distance part of the patch's
own distance distribution, and must show that the property is λ-free.

**Disclosed limitation, carried from ADR 0018.** The patch pool is drawn once per arm and
shared across field draws, so replicates are conditionally independent given the pool rather
than independent, and the binomial interval is a screen and not a proof. Sharing the pool has
one benefit worth stating: every method faces the identical null sample, so a difference
between two methods cannot be sampler noise.
