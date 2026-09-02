# timescale-normalisation

**Date:** 2026-08-26 · **Config:** `config.yaml` · **Records:** 128 · **Metrics:** `metrics.json`

## Question

The window sweep in `2026-08-26-stability-and-source` found that the continuous-time walk's
coherence window has opposite optima on two arms of the same tier. Document 47 measured a
candidate cause: the spectral gap varies by 21.7 across the four `development` arms while the
spectral range varies by 1.09, so a window fixed in units of the range is a different physical
experiment on each protein.

Does a clock set by the gap instead of the range make the window portable?

## Setup

Four arms, four finite-window observables, two clocks. `range` divides the unit of time by the
spectral range, `gap` divides it by the gap next to the dominant eigenvalue. Five windows for
`range` and three for `gap`, because one full slow period is already a long walk.

**The step count is derived, not fixed.** Over a grid spanning `window * 2 pi / unit` the
fastest phase turns `window * range / unit` times. Below two samples per turn the result
aliases, and the alias is invisible in the output. The runner sets four samples per turn, with
a floor of 256 and a cap of 8192. On `hiv_rt` under the `gap` clock this reaches 4071 steps.

## Result

**The gap clock removes the disparity it was built to remove, and the endpoint does not move.**

| Clock | Mean between-arm AUC spread | Best min-AUC over all settings |
| --- | --- | --- |
| `range` | 0.5627 | 0.375 |
| `gap` | **0.5516** | 0.355 |

The spread falls by 0.011, which is 2% of itself.

**Zero of 32 settings put all four arms above 0.5.** The best worst-arm figure over every
combination of clock, window and observable is 0.375.

**Variance decomposition, `range` clock then `gap` clock:**

| Observable | Within-arm (window) | Between-arm (protein) | Ratio |
| --- | --- | --- | --- |
| `ctqw_average_transfer` | 0.079 / 0.045 | 0.668 / 0.650 | 8.5x / **14.5x** |
| `ctqw_peak_transfer` | 0.099 / 0.059 | 0.637 / 0.602 | 6.4x / 10.2x |
| `ctqw_temporal_variance` | 0.169 / 0.176 | 0.541 / 0.528 | 3.2x / 3.0x |
| `ctqw_coherent_source_contrast` | 0.300 / 0.101 | 0.405 / 0.427 | 1.3x / 4.2x |

## Interpretation

**The clock is a correct normalisation and it normalises the wrong variance.** For
`ctqw_average_transfer` the gap clock nearly halves the window sensitivity, from 0.079 to 0.045.
That is the intended effect and it is measurable. The between-arm spread stays at 0.65. So the
ratio gets worse, not better, because the denominator shrank and the numerator did not.

**The protein dominates the hyperparameter by roughly an order of magnitude.** `hiv_rt` scores
0.87 to 0.91 on `ctqw_average_transfer` at every window under both clocks. `ns5b` scores 0.16 to
0.26 under the same conditions. The window moves each arm by about 0.08. Nothing in the time
grid closes a gap of 0.65.

**Negative result, and it rules out a whole class of remedy.** Tuning the time grid cannot make
these observables portable across proteins, because the time grid is not what makes them
unportable. Any future remedy has to act on the observable or on the graph, not on the clock.

**One robustness check passed, and it retires a caveat.** The earlier window sweep used the
default 128 steps, and a window of 100 needs at least 200 to satisfy Nyquist. Re-measured here
with a derived step count, the largest change across 48 shared cells is 0.002. The earlier
numbers stand.

## What would change the conclusion

A clock derived from a quantity that tracks the between-arm difference rather than the
within-arm one. Nothing tested so far predicts which of the four arms an observable will do well
on, so there is no candidate. `hiv_rt` being the easy arm for transfer observables and the hard
arm for `ctqw_coherent_source_contrast` (0.171 to 0.605) suggests the split is not a single
scalar property of the protein.
