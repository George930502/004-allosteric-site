# 0023 — The matched-patch null is calibrated, not fully matched

**Status:** accepted, decision stands · 2026-08-25 · clears
[ADR 0018](0018-null-calibration-is-unmet.md) · **rescale and explanation superseded by
[ADR 0025](0025-the-size-rescale-is-calibrated-at-every-holm-level.md)**

> **What ADR 0025 changes here.** The *decision* — freeze the tolerance and calibrate the
> threshold — stands, and it is better supported now than when this was written: four
> matching repairs have been tested and none closes the residual. Two things below are
> wrong and are corrected inline: the linear rescale formula, and the claim that the
> variance-factor percentile explains the residual. The second was falsified by direct
> intervention.

## Context

ADR 0018 withdrew the matched-patch tolerance and attempt budget because they rested on
session observations with no generator, config, seed or metrics. It blocked scoring until a
committed experiment regenerated them. `experiments/2026-08-25-null-calibration/` is that
experiment. It has a question, a versioned config, a seed, an implementation, raw and derived
metrics, and notes, and it produced a result the earlier draft did not anticipate.

**The two-ended gate.** Draw a site-uninformative, spatially autocorrelated score. Test the
true label patch against the matched-patch null. Repeat 1000 times at each of four
correlation lengths. The rejection rate must sit inside the exact central binomial prediction
interval, **[0.037, 0.064]** at n = 1000 and α = 0.05. Separately, a score built from the
answer must reject on every arm.

**The unmatched null fails badly, which is the finding that justifies the construction.**
Measured type-I rate 0.10 to 0.32 across all 14 arms, rising monotonically with correlation
length on every one.

**The matched null does not pass everywhere either, and the failure is systematic.** At the
frozen tolerance 0.10 and 9999 replicates, **6 of 14 arms sit above the band and 1 sits
below it**. It holds its size on both KRAS arms and on `ecoli_cps`, `hiv_rt`, `ns5b`, `ptp1b`
and `smyd3`; it runs conservative on cardiac myosin (0.034–0.037); and it runs
anti-conservative on both BCR-ABL1 arms (0.059–0.075) and on `chk1`, `glucokinase`, `mkp5`
and `p97_vcp` (up to 0.077). Tightening the tolerance to 0.05 makes BCR-ABL1 worse, not
better (0.066–0.089), and drops the sampler's acceptance rate on myosin to 0.0027.

**The positive control passes decisively**, so the null is not inert: a score built from the
answer returns p = 0.0001 on all 14 arms, the smallest value 9999 replicates can produce.

**The mechanism was measured, not guessed.** The variance of a patch mean under a spatially
autocorrelated score is `m⁻² Σᵢⱼ exp(−dᵢⱼ/λ)`, a functional of the entire within-patch
distance distribution. Radius of gyration is only its second moment about the centroid. The
observed patch's percentile on that sum, inside its own matched pool, orders the arms exactly
as the type-I rate does: myosin 32.5 %, KRAS 55.6 / 57.3 %, BCR-ABL1 70.1 / 76.7 % at λ = 8.

Four repairs have now been tried and none works. Mean within-patch pairwise Cα distance is
already satisfied by almost all of the pool, so adding it barely moves the percentiles.
Internal contact count correlates with the variance factor only weakly and orders the arms
wrongly. Centring the acceptance window on the observed radius of gyration leaves cardiac
myosin where it was. Matching the whole within-patch pairwise-distance distribution fixes
myosin and makes both BCR-ABL1 arms **worse**. Matching the variance factor itself is
impossible in advance: λ is a property of the **method's** score field, not of the benchmark.

**The fourth repair falsified the explanation above.** See
[ADR 0025](0025-the-size-rescale-is-calibrated-at-every-holm-level.md) and
`experiments/2026-08-25-null-repairs/`. Distribution matching drove BCR-ABL1's
variance-factor percentile to the centre of its pool and the type-I rate got worse. If the
percentile were the mechanism, that could not happen. It is a correlation across arms, not a
cause, and the paragraph above must be read as a description and never as an explanation.

## Decision

Freeze the tolerance at **0.10** and calibrate the **threshold** rather than match the null
further.

Each arm carries a frozen calibration measured on a site-uninformative score. `score_arm`
reports `p_calibrated` from it, and that is what the decision and the Holm step-down use.

**Superseded in form, not in substance.** This ADR froze `alpha_star`, the nominal p at which
the measured size equals α, and the linear rescale `p_calibrated = min(1, p × α / alpha_star)`.
That rescale is size-exact at α and wrong at Holm's tighter steps, so the composed procedure
was not FWER-controlled. ADR 0025 replaces it with `size_ratio`, calibrated at every Holm
level. `alpha_star` is still frozen and reported, for disclosure.

Two one-sided choices, both toward a smaller test:

- `alpha_star` is the **minimum across the four correlation lengths**, so it is valid for any
  method whose score field falls in that range.
- `alpha_star` is **capped at α**. Calibration may tighten a test and may never loosen one.
  Cardiac myosin keeps the nominal threshold instead of buying power back.

The gate runs on all 14 frozen arms, not only the five in the tolerance sweep. A threshold
measured after a method is scored is a hyperparameter, and the secondary set is where
hyperparameters are chosen.

## Consequences

ADR 0018's blocker clears and Phase 2 is unblocked on this axis.

**`p_calibrated` is a decision rule, not a calibrated p-value.** It is exact at the boundary
and only approximate away from it. Do not read it as a uniform p under the null.

**It costs power, and the cost is measured rather than assumed.** The sensitivity analysis in
the same experiment runs at `alpha_star` and not at the nominal α, so the published number is
the one the procedure delivers. At 80 % power the minimum detectable effect is AUC-ROC
**0.76 to 0.94**, and the spread across that band is the correlation length of the method's
own score field, not arm-to-arm variation. `alpha_star` runs from **0.025** (`p97_vcp`) to
**0.050** (`kras_g12c_mandated`, `cardiac_myosin_corrected`, `smyd3`).

**The residual is a modelling limitation, and it is disclosed.** Two sources of Monte Carlo
error remain. Taking an extremum over four correlation lengths biases the estimate toward a
smaller test. The noise in a single tail-quantile estimate from 1000 draws does **not**: it is
symmetric, so it can land either way. "Both push toward a smaller test" was wrong as written.
Under the frozen scheme the chance that an arm's threshold is looser than the truth was about
0.27 per arm, and about 0.61 that at least one of the three confirmatory arms is. ADR 0025
takes a maximum over twelve estimates instead of four, which shrinks that chance further and
costs more power. The direction is one-sided and disclosed; the magnitude is not zero.

> **MEASURED 2026-09-03, and the last claim is refuted.** Maximising over twelve estimates
> does **not** shrink that chance: `../benchmark/review/21-protocol-v3-statistics.md` §1.4,
> finding S4, draws 40 independent 1000-field blocks per arm against a 40 000-field reference
> and reads **0.275 to 0.300**, which is the same 0.27 the four-estimate scheme carried. The
> twelve cells are quantiles of the same 1000 p-values at three nearby levels, so they are
> almost perfectly correlated and the maximum over twelve is close to the maximum over four.
> The correct disclosure is "the design carries a chance of about 0.3 per arm of
> under-tightening; on these arms it did not", since both frozen ratios above 1 sit above the
> out-of-sample reference. The frozen values do not move for this.

**ADR 0018's second disclosed limitation stands.** The patch pool is drawn once per arm and
shared across field draws, so replicates are conditionally independent given the pool rather
than independent, and the binomial interval is a screen and not a proof. Sharing the pool has
one benefit worth stating: every method faces the identical null sample, so a difference
between two methods cannot be sampler noise.
