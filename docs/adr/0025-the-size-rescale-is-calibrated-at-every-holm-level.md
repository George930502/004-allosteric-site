# 0025 — The size rescale is calibrated at every Holm level, and clearing the null is a low bar

**Status:** accepted · 2026-08-25 · supersedes the rescale and the explanation in
[ADR 0023](0023-matched-patch-null-is-calibrated-not-fully-matched.md) · reopens Phase 1.6

## Context

Sub-phase 1.6 froze the evaluation layer on 2026-08-25 and its own audit reopened it the same
day (`docs/benchmark/evaluation/AUDIT.md`). Eight audits ran against the frozen manifest,
freeze, harness, ADRs, evidence file and calibration experiment. Two findings block scoring
and one changes what the protocol may claim.

### The confirmatory procedure was not FWER-controlled

ADR 0023 froze `alpha_star` per arm — the nominal p at which the measured size equals α — and
rescaled linearly, `p_calibrated = min(1, p × α / alpha_star)`.

That rescale is size-exact **at α and nowhere else**. The null's tail is convex, so at Holm's
tighter steps a linearly rescaled test runs above nominal. Holm presents α/3 and α/2 to two of
the three confirmatory arms whenever the first rejects, so the composed procedure was larger
than 0.05.

The calibration re-run measures it directly. `size_ratio` is the smallest factor that makes the
test conservative at a given level, and fitting it at α alone against fitting it at every level
gives different answers:

| Arm                        | needed at α | needed at α/2 | needed at α/3 | frozen ratio |
| -------------------------- | ----------: | ------------: | ------------: | -----------: |
| `kras_g12c_corrected`      |      1.0421 |        1.0642 |    **1.0827** |       1.0827 |
| `bcr_abl1_corrected`       |  **1.0970** |        1.0735 |        1.0951 |       1.0970 |
| `cardiac_myosin_corrected` |      1.0000 |        1.0000 |        1.0000 |       1.0000 |

Each cell is the maximum over the four correlation lengths. KRAS is the leak: calibrating at α
gives 1.0421 and α/3 needs 1.0827, so the frozen version-1 threshold was about half the
tightening the tightest Holm step required. BCR-ABL1 happens to bind at α, and myosin is
conservative everywhere, which is why the version-1 error showed on one arm and not on three.

Which level binds is not predictable in advance — `p97_vcp` (1.2487) and `chk1` (1.1832) both
bind at α/2 — so taking the maximum is the only rule that needs no case analysis.

### A trivial geometric baseline clears the whole confirmatory family

Score each residue by the volume of the largest pyKVFinder cavity that lines it. It is
label-blind, apo-only, zero-parameter, and it uses the detector the freeze already pins. Run
through `score_arm` under protocol version 2:

| Arm                        | AUC-ROC | recall@5 | `p_calibrated` | Holm threshold | reject  |
| -------------------------- | ------: | -------: | -------------: | -------------: | ------- |
| `cardiac_myosin_corrected` |   0.977 |     0.00 |         0.0001 |         0.0167 | **yes** |
| `bcr_abl1_corrected`       |   0.795 |     0.00 |         0.0003 |         0.0250 | **yes** |
| `kras_g12c_corrected`      |   0.830 |     0.00 |         0.0073 |         0.0500 | **yes** |

Three rejections out of three, at AUC-ROC inside the 0.75–0.82 band the protocol cites for the
published elastic-network literature. The tighter version-2 calibration does not save it.

This is not a defect in the null. The null controls patch size, compactness and burial. It does
not control cavity volume and it is not asked to. What the result shows is that **clearing the
confirmatory null is a low bar**. The same finding arrived independently from the literature
review: "rank by detector score alone" is the reference baseline both PASSer2.0
(doi:10.1093/nar/gkad303) and DeepAllo (doi:10.1093/bioinformatics/btaf294) report against.

The recall@5 column is the other half of it. All three rejections come with **zero** label
residues in the top five. The confirmatory test and the challenge's scored artifact are not the
same question, and a report that prints only the first is misleading.

### The explanation for the null's residual was falsified

ADR 0023 explained the residual by the percentile of the observed patch's variance factor
inside its own pool. `experiments/2026-08-25-null-repairs/` tests that directly by moving the
percentile. Across 12 arm-by-λ cells the two correlate at Spearman ρ = 0.821. Under
intervention, moving the percentile by 18 points moves the type-I rate by 0.001, and the
frozen relation predicts a mean type-I of 0.0407 where 0.0500 is measured. Both new repairs
also fail to close the residual, bringing the count to four.

## Decision

**1. Freeze a `size_ratio` per arm and rescale on the probit scale.**

```
p_calibrated = max(p, sf(isf(p) / size_ratio))
```

`size_ratio` is the maximum, over four correlation lengths **and** over every Holm level
α/3, α/2, α, of `z(q_t) / z(t)`, floored at 1. The rescale is conservative at level `t`
exactly when the ratio is at least `z(q_t) / z(t)`, so a maximum over all of them is
conservative at all of them by construction. `alpha_star` stays frozen and reported for
disclosure.

The `max(p, ...)` clamp exists because above p = 0.5 the probit rescale would lower p —
correctly under the model, since a wider null puts less mass above a point already below the
null mean. No decision threshold lies above 0.5, so the clamp costs nothing and keeps
"calibration may tighten and may never loosen" true as written.

**2. Add `cavity_volume` as a required baseline, first in the list.** The report's claim
threshold is **beating this baseline**, not rejecting the null. `allo.scoring.decoys.cavity_volume_score`
implements it, so the number is reproducible rather than quoted.

**3. Report recall@5 and the site pocket's rank beside every confirmatory p-value.** Both were
declared in prose and computed by nothing. A p-value printed without them invites the reading
the row above shows to be wrong.

**4. Re-freeze as protocol version 2 and reopen Phase 1.6** until `make check`,
`uv run allo evaluate verify` and both baseline runs pass.

## Consequences

**FWER is controlled at every Holm step**, by construction rather than by a model that happens
to fit at one threshold.

**It costs power, and the cost is measured.** The sensitivity analysis runs at the effective
threshold `sf(size_ratio × z(α))`, not at the nominal α, so the published minimum detectable
effect is the one the procedure delivers. Taking a maximum over twelve noisy quantiles instead
of four biases the ratio upward. That direction is one-sided and the magnitude is not zero.

**The bar moved, and it moved in the honest direction.** Before this ADR, "rejects the
confirmatory null on all three arms" was the headline a method could claim. After it, that
sentence describes a baseline that knows nothing about allostery. A quantum result has to beat
`cavity_volume`, and it has to put label residues in the top five.

**ADR 0023's decision stands and its explanation does not.** Calibrating the threshold is now
better supported — four repairs tried, none works — and the mechanism story is withdrawn. A
protocol may not claim a mechanism that direct intervention refutes.

**The design this protocol should be measured against is named, not hidden.** Variogram-matched
surrogates (Burt et al. 2020, doi:10.1016/j.neuroimage.2020.117038) resample the score map
rather than the patch and need no λ in advance. They are declined because they make the null a
property of the method, and the protocol's purpose is that every method faces the identical
null sample. This is the first thing to try if the calibration ever has to move.

## Amendment, same day — the deferral was wrong, and both items are now frozen

This ADR first deferred DCC and the four confounder columns to Phase 3, on the reason that
"they need a method to correlate against". That reason is false for DCC and only half true for
the confounders.

**DCC needs no method.** It is a function of the top-5 list, the label set and coordinates —
the same shape as precision@5, which was implemented and frozen before any method existed.
Deferring it would have meant adding an endpoint after methods were scored, which is precisely
what this manifest forbids. It is now `endpoints.reported.dcc_angstrom`, with a seeded Monte
Carlo chance line frozen per arm.

**The real complication was different, and it is handled.** Our own evidence file records that
the 4 Å threshold is contested for centre-to-centre distance: LIGYSIS-bench measured it and
states that 10–12 Å is the figure comparable to DCA = 4 Å. Freezing a threshold would take a
side, so the continuous distance is frozen and both conventions print beside it.

**Adding it immediately paid for itself.** On `bcr_abl1_corrected` the cavity-volume baseline
rejects the confirmatory null at `p_calibrated` 0.0003 while its predicted centre sits farther
from the true site than a random five-residue list: **DCC 26.5 Å against a chance line of
17.7 Å**. Without this column the report would have printed a decisive rejection with nothing
to contradict it. That is the clearest available evidence that a p-value and a usable hit list
are different claims.

**For the confounders, the computation needs a method but the declaration does not** — and the
declaration is the part that must be frozen before any method exists. The manifest already
works this way for `classical_comparison`, which lists eight baselines Phase 3 implements.
`confounders` is now declared the same way, and three of the four property vectors turned out
to need no new dependency:

| Property | Source |
| --- | --- |
| Relative solvent accessibility | Shrake-Rupley implemented in `allo.scoring.properties`, cross-checked against biopython at Spearman > 0.99 |
| Normalised B-factor | the deposited isotropic B, now carried through the parser, z-scored within the chain |
| Kyte–Doolittle hydrophobicity | doi:10.1016/0022-2836(82)90515-0, a 20-entry table |
| Conservation | **absent.** Needs an external alignment the offline gate cannot carry. Reads `null` |

They earn their place on first use: `distance_from_source_negated` correlates with normalised
B-factor at **ρ = −0.79** on cardiac myosin, so a score of that shape is largely re-measuring
crystallographic disorder. `cavity_volume` correlates with all three at |ρ| ≤ 0.22, so its
rejections are a cavity-size signal rather than a burial artefact.

**Still deferred, and now the reason is the true one.** Sequence conservation needs a network
fetch. It is recorded as unknown under R3 rather than approximated, and a reviewer will ask
for it.

## Amendment 2 — three more findings closed before the protocol was delivered

**"Beat the baseline" had no test.** The manifest required a method to beat its classical
baselines and defined no rule for it, so the comparison would have been chosen with results in
hand. `harness.compare_methods` is that rule: paired on the residue, tested against the same
matched-patch pool, two-sided because between two methods there is no defensible prior on the
winner. It is not a formality — `cavity_volume` beats `distance_from_source_negated` by AUC-ROC
**+0.24** on `kras_g12c_corrected` at **p = 0.60**, so a gap that size is inside what patch
geometry produces on that arm. Comparing two AUC values would have called it a win.

**The sensitivity was quoted at the wrong threshold.** Holm presents α/3 to the first of three
arms and α/2 to the second, and which arm draws which is decided by the results. The published
band was measured at α alone. The power stage now runs at every level: the band is 0.762–0.936
at α and **0.799–0.961** at α/3, so a method aiming at λ = 12–20 Å needs 0.89–0.96 rather than
the 0.86–0.94 the earlier draft implied.

**Four limitations were measured by the audit and stated nowhere.** All four are now in the
README: the decoy null's size mismatch (linings smaller than the label set on 14/14 arms,
median ratio 0.55, making it 2.3–5.3× conservative), its unreachable floor (7 of 14 arms, two
of them confirmatory, cannot reach p ≤ 0.05 at any effect size), the frozen ratio's sampling
error, and the pool's off-centre draw. None changes a decision. All four change what the report
may claim, which is why a protocol that hides them is not neutral.
