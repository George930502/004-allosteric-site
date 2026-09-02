# null-recalibration — 2026-09-02

**Question.** Does the matched-patch permutation test hold its size on the two arms the
2026-09-02 input re-freeze changed, and what threshold does each need?

**Why it exists.** Identical to `2026-08-25-null-calibration` except for the arm list. The
re-freeze changed two arms:

- `bcr_abl1_mandated` moved from `1OPL` chain A to chain B (ADR 0029). Node set 451 -> 365,
  scoreable labels 20 -> 17, 3 unmapped.
- `cardiac_myosin_mandated` was exposed for the first time (ADR 0031). It had no calibrated
  threshold, so `allo.scoring.harness._gate` raised on it and the arm could not be scored.

A threshold measured after a method has been scored is a hyperparameter. Both are calibrated
here, before any method runs on either arm.

**Pre-registered expectation.** The twelve unchanged arms reproduce their 2026-08-25 values
exactly. The seed, the tolerance and the replicate counts are identical, and nothing those
arms depend on moved. An unchanged arm that differs is a finding about determinism, not a
rounding difference.

**One thing happened during the first attempt, and it is a result rather than a fault.**
The run aborted on `cardiac_myosin_mandated` at the **0.05 rung of the tolerance sweep**:
822 of 999 patches in 3 996 000 attempts, rejections `{frontier: 704, adjacent: 0, degree:
2670539, compactness: 1323935, distance: 0}`. The frozen scoring tolerance is **0.10**, not
0.05, and at 0.10 the same arm draws all 999 patches at an acceptance rate of **0.000884**
(measured directly: 0.10 → 0.000884, 0.15 → 0.002212, 0.20 → 0.004260, 0.30 → 0.010698).

So the failure is confined to a rung the sweep is *testing*, and the scored arm keeps its null.
Two changes followed, and neither touches a threshold:

1. `allo.scoring.nulls.MatchedPoolUnavailable` is a distinct exception type, carrying the draw
   diagnostics and the observed patch geometry. `allo.scoring.calibration.calibrate_arm`
   records the rung as `available: false` and the sweep continues; the power stage skips any
   arm with no gate.
2. `allo.scoring.harness` handles the same exception on the scoring path, so an arm whose
   graph cannot supply a pool **at the frozen tolerance** would be reported without a
   matched-patch null instead of aborting the freeze. No arm is in that state today.

**No arm's tolerance was widened.** A per-arm tolerance chosen after that arm failed is the
per-arm hyperparameter this protocol exists to prevent, and the exception's docstring says so
at the raise site.

## Result

**The pre-registered expectation held exactly.** Thirteen of the fifteen gate arms reproduce
their 2026-08-25 `size_ratio` and `alpha_star` to six decimal places. The two that moved are
the two that were supposed to move.

| Arm | `size_ratio` | `alpha_star` | Against 2026-08-25 |
| --- | ---: | ---: | --- |
| `bcr_abl1_mandated` | **1.2073** | **0.0277** | was 1.0960 / 0.0357 on chain A. **The organisers' chain B needs more tightening than chain A did** |
| `cardiac_myosin_mandated` | **1.0509** | **0.0485** | new arm, no prior value |
| every other arm | unchanged | unchanged | bit-for-bit |

**The one undrawable rung is the predicted one.** `cardiac_myosin_mandated` at tolerance
**0.05**: 822 of 999 patches in 3 996 000 attempts, acceptance 0.000206. Recorded as
`available: false`; the sweep continued. At the frozen 0.10 the same arm drew all 9999 gate
patches in 11 390 541 attempts at acceptance **0.000878** — within 1 % of the 0.000884 the
standalone probe measured, which is the determinism check.

**The homology-model arm is the best-calibrated arm in the set, and that is worth stating
because it is counter-intuitive.** `cardiac_myosin_mandated` sits inside the binomial band
[0.0370, 0.0640] at all four correlation lengths (0.051 / 0.048 / 0.046 / 0.054). The measured
`cardiac_myosin_corrected` sits **below** the band at two of them. A well-calibrated null on
this arm says nothing about whether the arm's graph is right — it says the matched-patch
construction works on it. The arm's defect is the contact graph (long-range Jaccard 0.471
against `9GZ3`), and no null calibration can see that.

**`bcr_abl1_mandated` got worse, and the gate absorbed it.** Chain B's type-I rate is
0.054 / 0.071 / 0.069 / 0.079 against chain A's 0.059-0.075, so three of four length scales sit
above the band. That is what `size_ratio` 1.2073 is for. Calibration may tighten and may never
loosen, so the arm is testable at a stricter threshold rather than at a wrong one.

**The positive control is 0.0001 on all fifteen arms**, the smallest value 9999 replicates can
produce. The nulls are not passing their type-I band by rejecting nothing.

Full record: `metrics.json`. Protocol: `docs/benchmark/evaluation/README.md`.
