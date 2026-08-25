# Null repairs — two more, and a test of the explanation

**Date:** 2026-08-25 · **Config:** `config.yaml` · **Run:** `uv run allo evaluate repairs config.yaml`

The measurement code is `allo.scoring.calibration.run_repairs`, not a script in this
directory: `experiments/` is scanned by the runner leakage gate and this code calls
`_positives`. Same split as the calibration experiment.

## Question

The matched-patch null holds its size on most frozen arms and misses on three. ADR 0023
records two repairs that failed, and explains the residual this way: the observed patch's
variance factor, as a percentile of its own matched pool, sets the type-I rate.

Two questions, one run.

1. Do two further repairs close the residual? Repair **C** centres the acceptance window on
   the observed radius of gyration. Repair **D** matches the whole within-patch
   pairwise-distance distribution instead of its second moment.
2. Is the percentile the **mechanism**, or only a correlate? Both repairs move the percentile
   directly, so the answer is measurable rather than arguable.

## Setup

Three confirmatory arms, four correlation lengths, 1000 site-uninformative field draws each,
against the 9999-member pool that scoring actually uses. Each repair post-stratifies that pool
and keeps the closest half.

**Limitation, stated because it bounds the conclusion.** Neither repair redraws the pool at
full size. The surviving pool is half as large and less diverse, so a full re-draw under either
rule is an open question, not a closed one. What the run does establish is the direction of the
percentile-to-type-I relation under direct intervention, and that does not depend on pool size.

## Result 1 — both repairs fail

| Arm                        | frozen type-I (λ = 4–20) | after C       | after D       |
| -------------------------- | ------------------------ | ------------- | ------------- |
| `kras_g12c_corrected`      | 0.050 – 0.055            | 0.045 – 0.056 | 0.047 – 0.055 |
| `bcr_abl1_corrected`       | 0.060 – 0.068            | 0.061 – 0.065 | 0.061 – 0.067 |
| `cardiac_myosin_corrected` | 0.034 – 0.037            | 0.034 – 0.037 | 0.035 – 0.036 |

Nominal is 0.05 and the exact binomial band at n = 1000 is [0.037, 0.064]. BCR-ABL1 stays
above the band under both repairs. Cardiac myosin stays below it under both. **Four repairs
have now been tested and none closes the residual.**

## Result 2 — the explanation is falsified

Across the 12 arm-by-λ cells, percentile and type-I rate correlate at Spearman **ρ = 0.821**.
That is the observation ADR 0023 was built on, and it is real.

Under direct intervention it does not hold.

| Repair | mean move in percentile | mean move in type-I | ρ of the two moves |
| ------ | ----------------------- | ------------------- | ------------------ |
| C      | **−18.1 points**        | −0.0012             | −0.193             |
| D      | −4.8 points             | −0.0011             | +0.049             |

Repair C moves the percentile by 18 points on average and up to 26, and the type-I rate moves
by about one thousandth. Fitted on the frozen cells, the percentile-to-type-I relation predicts
a mean type-I of **0.0407** after repair C. The measured value is **0.0500**.

The sharpest single cell: repair C takes `kras_g12c_corrected` at λ = 8 from percentile 57.3 to
**31.0** — below the 32.5 that cardiac myosin sat at when the protocol read that percentile as
the reason myosin under-rejects. KRAS's type-I rate goes 0.055 to 0.056.

**Interpretation.** The percentile is a **correlate across arms, not a cause**. Something that
varies between arms drives both, and the percentile is a marker for it. Matching the marker
does not move the outcome, which is why four repairs aimed at the marker have all failed.

## What this changes

ADR 0023's **decision** — freeze the tolerance and calibrate the threshold — stands, and is
better supported now than when written: four repairs have been tried and none works, so
calibrating the threshold is not a shortcut past an unexplored fix.

ADR 0023's **explanation** does not stand and is corrected there and in
`docs/benchmark/evaluation/README.md` section 6.2. A protocol may not claim a mechanism that
direct intervention refutes.

**What would settle it.** Resample the score **map** rather than the patch: variogram-matched
surrogates (Burt et al. 2020, doi:10.1016/j.neuroimage.2020.117038) estimate the
autocorrelation from the field a method actually produced. That design sidesteps the marker
entirely. It is not adopted here because it makes the null a property of the method, and the
protocol's purpose is that every method faces the identical null. See README section 12.4.
