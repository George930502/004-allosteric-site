# What one NaN did, at each of the twelve sites — measured 2026-09-03

Round 6 of the audit found the same defect twelve times: **a NaN makes every comparison
false, and false is the direction that helps a method.** Every site is guarded now. This
page records what each one did *before* its guard, so that the grade each finding was given
rests on a measurement rather than on the example that happened to be tried first.

Method: reproduce the pre-guard expression exactly as the code wrote it, then read the number
that comes out. No guard is removed. Every row is re-derivable from the expression in its own
"evidence" column.

| # | site | direction | evidence |
| - | ---- | --------- | -------- |
| 1 | `_aligned`, the score vector | **anti-conservative** | `rankdata([1, nan, 3])` returns `[nan, nan, nan]`, so the observed statistic is nan and `permutation_p` returns its floor `1/(1+B)` = **1.0e-04** at the frozen replicate count — under every Holm threshold in the family |
| 2 | `combine_arms`, the p-values | fail-safe, record corrupt | the Fisher statistic is nan, `chi2.sf(nan, 6)` is nan, and `nan < 0.05` is False. No rejection — but the record then serialises as bare `NaN`, which is not JSON |
| 3 | `holm`, the p-values | fail-safe | the NaN sorts **first**, takes the tightest threshold `0.05/3`, is not rejected, and the step-down stops. Two arms at p = 0.01 go from two rejections to **zero** |
| 4 | `holm`, alpha | fail-safe | `0.01 <= nan/3` is False, so no arm is ever rejected |
| 5 | `calibrated_p`, the p-value | fail-safe | `norm.isf(nan)` is nan, the composite is nan, every threshold comparison against it is False |
| 6 | `calibrated_p`, the size ratio | **anti-conservative** | `max(0.01, norm.sf(norm.isf(0.01)/nan))` returns **0.01**, the raw p-value. The rescale silently disappears. The correct ratio 1.2073 would have given **0.026996** |
| 7 | `_gate`, the settings side | fail-safe on the public path | `abs(nan - 0.10) > 1e-9` is False, so the gate passes. Measured through `score_arm`, the sampler then draws nothing and the arm reports `available: false` with no p-value |
| 8 | `_gate`, the calibration-record side | fail-safe on the public path | the same comparison, the other argument |
| 9 | `permutation_p` | **anti-conservative** | `(1 + #{null >= nan})/(1+3)` = **0.25**; at the frozen B this is **1.0e-04**, the minimum attainable p-value, manufactured out of a missing number |
| 10 | `sample_matched_patches`, the tolerance | **anti-conservative** | the three rejections read `diff > tolerance * wanted`, and `abs(5.0 - 4.0) > nan * 4.0` is False. Degree, compactness and distance are all skipped: **20 patches of the right size** come back and the pool still reports itself matched |
| 11 | `binomial_band` | fail-safe | `binom.ppf(0.025, 1000, nan)/1000` is nan, so `low <= rate <= high` is False both ways, which reads as a **failing** calibration |
| 12 | the exported metrics | **two of five anti-conservative** | see below |

## Row 12, which was graded wrong the first time

The seventh pass's finding was written up as robustness rather than validity, on the ground
that a NaN gives an unfavourable number here. **One example was tried, and it was not the
rule.**

`rank_vector` propagates a NaN to the whole vector, so `auc_roc` returns nan and that half is
fail-safe. `precision_at_k` does **not** propagate: `np.lexsort` sinks the NaN to the bottom
of the ranking. So a method that emits a NaN on its own worst false positive deletes that
false positive from the top of its own list.

| scores | positive | precision@2 |
| ------ | -------- | ----------: |
| `[1.0, 5.0, 2.0, 0.5]` | `[T, F, T, F]` | 0.50 |
| `[1.0, nan, 2.0, 0.5]` | `[T, F, T, F]` | **1.00** |

`top_k_indices` is the same expression and it is the deliverable itself: the top-5 residue
list a chemist is handed. `auc_pr` moves the same way, 1.0000 with the NaN on a negative and
0.7500 with it on a positive — the direction is decided by which class holds the NaN and by
array order, and nothing announces either.

Pinned by `test_no_exported_metric_ranks_a_non_finite_score`.

## The tally

**Four anti-conservative, seven fail-safe, one whose direction is decided by array order.**
Twelve sites, found across seven adversarial passes, each one only after the previous fix
shipped. The class was the finding, and it took seven passes to say so.

The guards now live one per layer: `_checked_pvalues` and `_checked_tolerance` in
`allo.scoring.harness`, `_finite_scores` in `allo.scoring.metrics`, and in-place checks in
`nulls` and `calibration`. The standing test
`test_no_raise_guard_compares_a_float_a_non_finite_value_would_slip_past` sweeps for the
shape, and it caught site 11's own new replicate-count guard on its first run.
