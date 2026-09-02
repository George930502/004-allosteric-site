# 21 — Statistical audit of evaluation protocol version 3

> **SUBJECT PARTLY DELETED — 2026-09-02.** This document cites files in the method layer:
> `src/allo/{network,classical,quantum}`, `docs/method/exploration/`, `tests/test_method.py`,
> or an experiment directory dated 2026-08-26 or 2026-08-27. All of those left `main` on
> 2026-09-02 (ADR 0037) and are preserved whole on the branch `method-layer-archive`.
> Findings whose subject is one of those files are **not re-runnable on `main`**. They stay
> here unedited, because a record of what an audit found is worth keeping even when the
> subject is gone. To re-run one, check out that branch. Two things moved rather than left:
> `allo.network.graph` is now `allo.structure.graph`, and the nine required baselines are now
> `allo.scoring.baselines`.

**Date: 2026-09-02. Scope: `docs/benchmark/evaluation/` at protocol version 3, and the code
that implements it — `src/allo/scoring/calibration.py`, `harness.py`, `nulls.py`,
`metrics.py`, `decoys.py`.**

Read-only on every frozen artifact. Nothing in `manifest.yaml`, `frozen.json` or any
`metrics.json` was edited. Every number below is either re-derived from a committed file or
measured by a script reproduced verbatim in **Appendix A**. Scripts were run with
`uv run python` from a scratch directory outside the repository, because a tracked script
naming `frozen.json` fails `tests/test_no_leakage.py`.

**Verdict.** The core of the procedure is sound and better than the field's practice: the
probit rescale is calibrated at exactly the levels Holm's proof requires, and an
out-of-sample simulation confirms FWER control. The defects are all in the **layer around
it** — in the negative-class-(b) test, in the pre-declared claim reference, and in numbers
the documents state that no longer re-derive.

| # | Finding | Severity | Kind |
| --- | --- | --- | --- |
| **S1** | `cavity_volume`, the pre-declared reference of confirmatory family 2, no longer clears family 1 under v3. Measured `p_calibrated` **0.0715 / 0.3236 / 0.0046** — Holm rejects **1 of 3**, not 3 of 3. The v3 manifest and ADRs 0025/0032 still assert 3 of 3 | **blocker for the documents** | stale fact |
| **S2** | The **tested** form of negative class (b) is cleared by a label-blind cavity ruler: Fisher **p = 0.01537**, Stouffer **0.00904**, empirical p under the field null **0.0002–0.0003**. No "beat the baseline" threshold exists for this endpoint | **high** | design gap |
| **S3** | The combined negative-class-(b) test's measured size at nominal 0.05 is **0.0014–0.0066** (Fisher) and **0.0051–0.0141** (Stouffer). It was never gated. It escapes the arithmetic floor but is 7.6× to 36× conservative | **high** | undisclosed |
| **S4** | The frozen `size_ratio` is a 1000-field estimate whose 12-cell maximum falls below a 40 000-field reference **27.5–30.0 %** of the time. ADR 0025's "shrinks that chance further" than ADR 0023's 0.27 is not supported | medium | unsupported claim |
| **S5** | The "permutation floor of 0.001080" in `ROADMAP.md`, `REGISTRY.md` and `46-beats-distance.md` is **not a floor**. It is the smallest calibrated p in one 272-test battery. "Holm cannot reject on `ptp1b`/`ns5b` at any data" is **false** | medium | arithmetic error |
| **S6** | AUC-PR's stated chance line (prevalence) understates the null mean of the step estimator by **26–51 %**, and no AUC-PR chance line is frozen in `frozen.json` | medium | wrong chance line |
| **S7** | Three separate α = 0.05 decisions — family 1, family 2, `decoy_pockets_combined` — with no correction across them. Sound as a conjunction, ≤ 0.15 study-wise if reported as three findings | low-medium | multiplicity |
| **S8** | Confirmatory family 2 (`compare_methods`) had **never** had its size measured. Measured here: it holds, 0.041–0.047 at α | low (confirmed) | gap now closed |
| **C1–C10** | Ten claims confirmed by measurement, including FWER control, the one-sided rescale, the midrank↔AUC identity, Fisher's independence, and every minimum-attainable p | — | confirmation |

---

## 1. Is the probit-scale rescale at every Holm level valid?

### 1.1 The procedure, from the code

Three functions, in this order.

**`calibration.calibrate_arm` (`calibration.py:142–171`) fits the ratio.** For each
correlation length λ ∈ {4, 8, 12, 20} Å it draws `n_fields = 1000` site-uninformative
Gaussian fields from the exponential covariance `exp(−d/λ)` over the candidate Cα
coordinates, ranks each field, takes the label patch's mean midrank, and computes the raw
upper-tail permutation p against the **cached 9999-patch matched pool**. Then, for every
level Holm can present,

```text
levels = [alpha / k for k in range(family_size, 0, -1)]     # [α/3, α/2, α]
...
for level in levels:
    q = float(np.quantile(matched_p, level))
    step_ratio[round(level, 5)] = round(float(norm.isf(min(q, level)) / norm.isf(level)), 4)
```

and the frozen number is `"size_ratio": round(max(ratios), 4)` — the maximum over **12
cells** (4 λ × 3 levels), floored at 1 by the `min(q, level)` cap.

**`harness.calibrated_p` (`harness.py:131–157`) applies it.**

```text
ratio = max(float(ratio), 1.0)
return float(min(1.0, max(p, norm.sf(norm.isf(p) / ratio))))
```

**`harness.holm` (`harness.py:480–494`) composes it.** Step-down, `threshold = alpha / (m - i)`
on the ascending order, `still_rejecting = still_rejecting and p <= threshold`.

### 1.2 The algebra is exactly right, and it is right for a reason the ADRs do not state

Rejecting at level `t` means `sf(isf(p)/r) ≤ t`, i.e. `p ≤ sf(r·z(t))`. Writing `F` for the
null CDF of the raw p and `q_t = F⁻¹(t)`, the calibrated test's size at level `t` is
`F(sf(r·z(t)))`, which is `≤ t` exactly when `r ≥ z(q_t)/z(t)`. That is the code's
condition, and taking the maximum over levels makes it hold at all of them. Confirmed.

**What makes this sufficient rather than merely plausible is the structure of Holm's proof,
which neither ADR 0025 nor the README states.** Let `I` be the true nulls, `m₀ = |I|`. If any
true null is rejected, the first true null in sorted order sits at position `j ≤ m − m₀`,
so its p satisfies `p ≤ α/(m−j) ≤ α/m₀`. Hence

```
FWER ≤ P(min_{i∈I} p_i ≤ α/m₀) ≤ Σ_{i∈I} P(p_i ≤ α/m₀) = m₀ · (α/m₀) = α
```

The union bound needs validity of each p **at the single level α/m₀ only**. With `m = 3`,
`m₀ ∈ {1, 2, 3}`, so the levels that matter are exactly `{α, α/2, α/3}` — precisely the set
`calibrate_arm` fits. The design is not "calibrate at a few levels and hope"; it is the
minimal sufficient set. **Confirmed (C1).**

### 1.3 Measured, out of sample

`q12_fwer.py` (Appendix A.2) re-runs the whole procedure at a **different seed** from the
frozen calibration (20260902 against the frozen 0), 20 000 fields per cell, using the same
cached pools, the same `calibrated_p` and the same `holm`.

| λ (Å) | raw size at α, KRAS / BCR-ABL1 / myosin | calibrated size at α/3 | at α/2 | at α | **FWER, Holm, 3 true nulls** |
| ---: | --- | --- | --- | --- | ---: |
| 4 | 0.0466 / 0.0554 / 0.0449 | 0.0123 / 0.0116 / 0.0145 | 0.0175 / 0.0185 / 0.0227 | 0.0355 / 0.0387 / 0.0450 | **0.0376** |
| 8 | 0.0468 / 0.0583 / 0.0434 | 0.0138 / 0.0147 / 0.0145 | 0.0211 / 0.0224 / 0.0218 | 0.0372 / 0.0428 / 0.0434 | **0.0422** |
| 12 | 0.0461 / 0.0604 / 0.0433 | 0.0143 / 0.0165 / 0.0149 | 0.0201 / 0.0235 / 0.0213 | 0.0376 / 0.0448 / 0.0434 | **0.0452** |
| 20 | 0.0452 / 0.0637 / 0.0391 | 0.0144 / 0.0162 / 0.0152 | 0.0206 / 0.0235 / 0.0205 | 0.0365 / 0.0461 / 0.0391 | **0.0450** |
| **40** | 0.0434 / 0.0644 / 0.0353 | 0.0142 / 0.0158 / 0.0131 | 0.0200 / 0.0224 / 0.0183 | 0.0349 / 0.0463 / 0.0353 | **0.0424** |
| **100** | 0.0404 / 0.0642 / 0.0307 | 0.0136 / 0.0163 / 0.0106 | 0.0187 / 0.0234 / 0.0151 | 0.0331 / 0.0465 / 0.0308 | **0.0400** |

Nominal levels are 0.016667, 0.025, 0.05. **No cell exceeds its nominal level, at any λ**,
and the FWER runs 0.0376–0.0452 against 0.05. Monte-Carlo SE at 20 000 draws is 0.0015 at a
rate of 0.045, so the largest reading, 0.0452 ± 0.0029, is below 0.05.

**Answer to question 1: the family-wise error rate is controlled at 0.05, and the procedure
is mildly conservative — measured FWER 0.038–0.045 rather than 0.05.** The rows in bold are
the important ones: λ = 40 and 100 Å lie **outside** the range the calibration was fitted on,
and the calibrated size still does not exceed nominal. The raw (uncalibrated) size on
`bcr_abl1_corrected` rises from 0.0554 at λ = 4 to 0.0644 at λ = 40 and then plateaus, which
is why the extrapolation is safe: the anti-conservatism saturates inside the calibrated band.

### 1.4 Where the residual risk actually is

Not in the algebra — in the 1000 fields the quantile is estimated from. `q12c_focus.py`
(Appendix A.4) draws 40 independent 1000-field blocks per arm, reproducing the frozen
design's structure (the same innovations reused across λ, as `calibrate_arm` does by
resetting `field_rng` inside the λ loop), and compares each block's 12-cell maximum against
a 40 000-field reference.

| Arm | frozen `size_ratio` | 40 000-field reference | 1000-field max: mean (sd) | **P(block max < reference)** |
| --- | ---: | ---: | --- | ---: |
| `kras_g12c_corrected` | 1.0827 | 1.0475 | 1.0781 (0.0472) | **0.300** |
| `bcr_abl1_corrected` | 1.0970 | 1.0818 | 1.1061 (0.0438) | **0.275** |
| `cardiac_myosin_corrected` | 1.0000 | 1.0000 | 1.0213 (0.0280) | 0.000 |

**S4.** ADR 0023 disclosed "about 0.27 per arm" for the 4-estimate scheme and ADR 0025
asserts that maximising over twelve estimates instead of four "shrinks that chance further".
**Measured, it does not: 0.275–0.300 (40 blocks, SE ≈ 0.07).** The extra cells are highly
correlated — they are quantiles of the same 1000 p-values at three nearby levels — so the
maximum over 12 is close to the maximum over 4.

This is a defect in a stated claim, not in the frozen values. Both frozen ratios happen to
sit **above** the out-of-sample reference (1.0827 > 1.0475; 1.0970 > 1.0818), which is why
§1.3 comes in under nominal everywhere. The correct disclosure is "the design carries a ≈0.3
per-arm chance of under-tightening; on these three arms it did not."

### 1.5 A field class the calibration never saw

The calibration instrument is an exponential-covariance Gaussian field in **Euclidean**
space. A CTQW observable, a GNM mode, a spectral centrality — the methods this project will
run — are band-limited in the **graph** spectrum instead. `q12c_focus.py` measures the
calibrated size under `score = Σ_{k=1..K} c_k φ_k`, the K lowest non-trivial eigenvectors of
the evaluation graph's combinatorial Laplacian with i.i.d. Gaussian coefficients, 20 000
draws per cell:

| Arm | K = 5 | K = 20 | K = 50 | K = 150 |
| --- | ---: | ---: | ---: | ---: |
| `kras_g12c_corrected` | 0.0024 | 0.0335 | 0.0299 | 0.0370 |
| `bcr_abl1_corrected` | 0.0115 | 0.0114 | 0.0253 | 0.0496 |
| `cardiac_myosin_corrected` | 0.0000 | 0.0083 | 0.0372 | 0.0425 |

(size at nominal α = 0.05.) **No anti-conservatism anywhere — the opposite.** For a strongly
band-limited score the test spends between 0 % and 23 % of its α. This is a power finding,
not a validity finding, and it is the one that matters most for this project: a smooth
spectral observable faces an effective α closer to 0.01 than to 0.05, on top of the
`size_ratio` tightening. It is unmeasured and unstated in the protocol.

---

## 2. Is there circularity between calibration and scoring?

**Does the calibration use label information? Yes — the label patch's geometry, and nothing
else.** `calibrate_arm` calls `harness._positives(target)`, which reads
`scoreable_label_residues` from the input freeze, and passes the residue list to
`matched_patches`. `nulls.sample_matched_patches` derives from it exactly four quantities:
the size, the component-size multiset, the patch mean contact degree, and the patch radius
of gyration (`nulls.py:263–271`). Those four define the pool the null is drawn from. There
is no route by which a **score** enters: the only score vectors `calibrate_arm` ever sees are
the synthetic Gaussian fields and the evaluation-side oracle (`−`distance to the nearest
label), and neither leaves the function.

That is not circularity — it is what a matched null *is*. The observed patch's geometry has
to enter the null or the null is not matched. The genuine C1 concern is a different one and
is already documented as leakage route 6: `data/patches/` stores `members` with width equal
to the arm's positive count and a `diagnostics` string carrying
`observed_median_distance_to_source`, `observed_radius_of_gyration` and
`observed_mean_degree`. That is the label geometry on disk, and
`tests/test_no_leakage.py` guards it. Nothing here changes that assessment.

**Is the rescale one-sided, as the ADRs claim? Yes, verified from the code.** `q2356.py`
(Appendix A.5) evaluates `calibrated_p(p, r) ≥ p` over 51 ratios × 600 p-values = **30 600
pairs; 0 violations**. The three mechanisms:

* `ratio = max(float(ratio), 1.0)` — a ratio below 1 (a conservative arm) is clamped, so
  calibration can never buy power back. `calibrated_p(0.01, 0.5) = 0.01`.
* For `p < 0.5`, `isf(p) > 0`, so dividing by `r ≥ 1` moves the probit toward 0 and
  `sf(·) ≥ p`.
* For `p ≥ 0.5` the transform would *lower* p, and the outer `max(p, ·)` blocks it.
  `calibrated_p(0.8, 1.25) = 0.8`.

**Can a method exploit the calibration? Two channels were tested and neither opens.**

1. *Correlation length.* A method could in principle emit a smoother score field than the
   λ ≤ 20 Å the calibration covers. §1.3 measures λ = 40 and 100 Å: calibrated size stays
   under nominal at every level. The exploit is closed empirically.
2. *Field class.* §1.5 measures band-limited graph-spectral fields, a class the calibration
   never saw. Conservative everywhere.

**The channel that is open is the one ADR 0025 already names, and it is not the
calibration's fault.** The null matches size, components, degree and compactness. It does
not match cavity volume, solvent accessibility, B-factor or distance to the source, so any
score correlated with an unmatched confounder clears the null without knowing anything about
allostery. That is a property of the null's matching set, not of the threshold rescale, and
the protocol's answer to it is confirmatory family 2 — which §3 shows has a stale reference.

---

## 3. Is the Fisher combination a valid test of the stated hypothesis?

### 3.1 The stated hypothesis and the minimum attainable p

`combine_arms` takes the three `nulls.decoy_pockets.p` values, each
`(1 + #{decoy lining mean rank ≥ label set mean rank}) / (1 + n_decoys)`, and returns
`chi2.sf(−2 Σ ln p, 2k)`. It tests the **intersection null**, and the manifest and ADR 0030
label it correctly.

Enumerated exactly over the discrete supports (`q345_exact.py`, Appendix A.1):

| Detector settings | `n_decoys` (KRAS / BCR-ABL1 / myosin) | per-arm floors | **Fisher min p** | **Stouffer min p** |
| --- | --- | --- | ---: | ---: |
| version 2 | 3 / 9 / 41 | 0.25, 0.10, 0.0238 | **0.0214306** | **0.0115158** |
| version 3 | 18 / 31 / 84 | 0.052632, 0.03125, 0.011765 | **0.0013689** | **0.000452975** |

**Answer: the claimed floor of 0.021 is right — for version 2.** ADR 0030's table reads
0.0214 and 0.0115, and both re-derive to six figures. Under the re-frozen v3 detector the
floor is 0.00137 / 0.000453, which the manifest also states correctly. Any document still
quoting 0.021 as *current* is quoting version 2. **Confirmed (C7).**

### 3.2 Dependence: measured, and it is not the problem

The question presumes positive dependence from shared structures, detector and code path.
`q3_fisher_size.py` (Appendix A.6) measures it directly: draw an independent
site-uninformative field on each arm, compute the three decoy p-values, and correlate their
probits, 20 000 replicates per λ.

| λ (Å) | ρ(KRAS, BCR-ABL1) | ρ(KRAS, myosin) | ρ(BCR-ABL1, myosin) |
| ---: | ---: | ---: | ---: |
| 4 | −0.010 | 0.008 | −0.007 |
| 8 | −0.004 | 0.002 | −0.001 |
| 12 | 0.000 | 0.010 | 0.000 |
| 20 | −0.001 | 0.004 | 0.006 |

**All |ρ| ≤ 0.010 against a standard error of 0.007. The three arms are empirically
independent under this null.** The reason is structural: the permutation randomness on arm
*i* is the pocket set of protein *i*, and the three proteins share no residue, no pocket and
no permutation. The shared detector and shared code path induce dependence in the
**alternative** — a good method wins on all three together — which raises power and does not
touch size. **Confirmed (C6).**

For completeness, the sensitivity if that were wrong. A Gaussian copula on the exact discrete
supports, 400 000 draws per ρ, and the Brown/Kost scaled-χ² approximation
(doi:10.2307/2529826; doi:10.1016/S0167-7152(02)00310-3) beside it:

| ρ | Fisher, true size at nominal 0.05 | Stouffer, true size |
| ---: | ---: | ---: |
| 0.0 | 0.0209 *(exact enumeration: 0.02055)* | 0.0317 *(exact: 0.03137)* |
| 0.1 | 0.0293 | 0.0447 |
| 0.2 | 0.0397 | **0.0597** |
| 0.3 | 0.0497 | 0.0743 |
| 0.5 | 0.0685 | 0.1012 |
| 0.7 | 0.0861 | 0.1252 |

Two things follow. First, **discreteness makes the nominal-0.05 Fisher test an actual-0.0206
test**, so it buys a dependence budget: Fisher does not exceed nominal until ρ ≈ 0.30.
Second, **Stouffer — which the protocol reports beside Fisher — exceeds nominal at ρ ≈ 0.15**
and reads 0.0597 at ρ = 0.2. Since the measured ρ is 0.00, neither bites here; the point is
that the two combiners have very different robustness and the protocol reports both without
saying so.

### 3.3 The real defect: the combination has never been gated, and it is 7.6–36× conservative

ADR 0030 ran the ADR-0018 type-I gate on the **per-arm** pocket test ("construction A,
0.000–0.032") and on the two rejected replacements. It never ran it on the construction it
adopted. `q3_fisher_size.py` runs it, 20 000 site-uninformative fields per λ:

| λ (Å) | per-arm size at 0.05: KRAS / BCR-ABL1 / myosin | **Fisher size at 0.05** | **Stouffer size at 0.05** |
| ---: | --- | ---: | ---: |
| 4 | 0.0000 / 0.0032 / 0.0072 | **0.0014** | **0.0051** |
| 8 | 0.0000 / 0.0077 / 0.0089 | **0.0032** | **0.0089** |
| 12 | 0.0000 / 0.0105 / 0.0113 | **0.0051** | **0.0121** |
| 20 | 0.0000 / 0.0138 / 0.0126 | **0.0066** | **0.0141** |

**S3.** The tested form of negative class (b) has a true size of 0.0014 to 0.0066 against a
nominal 0.05 — 7.6× to 36× conservative. ADR 0030's consequence "negative class (b) becomes
testable at α = 0.05, at the family level" is true about the *arithmetic floor* and false
about the *size*. Two mechanisms compound: the discreteness of §3.2 (0.05 → 0.0206), and the
size mismatch the README §5.3 already discloses — a decoy lining is smaller than the label
set on 15 of 15 arms, median ratio 0.412 (re-derived; the README's 0.412 is **correct**,
C10), so the decoy statistic is over-dispersed relative to the observed one. On
`kras_g12c_corrected` the per-arm size is **exactly 0**, because its floor of 0.052632
exceeds α: that arm contributes a p that can never be below 0.05, on any data.

### 3.4 S2 — a label-blind cavity ruler clears the tested form of negative class (b)

`q2356.py` computes `decoys.cavity_volume_score` under the frozen v3 detector settings and
pushes it through the same statistic `score_arm` uses.

| Arm | decoy-pocket p | floor | AUC-ROC | site cavity volume (Å³) | largest decoy | site's volume rank |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `kras_g12c_corrected` | **0.052632** | 0.052632 | 0.8430 | 1688.69 | 47.52 | **1** |
| `bcr_abl1_corrected` | 0.312500 | 0.03125 | 0.5626 | 1489.54 | 2814.91 | 2 |
| `cardiac_myosin_corrected` | **0.023529** | 0.011765 | 0.8064 | 7988.54 | 4579.63 | **1** |

```
combine_arms(fisher)   = 0.01537309
combine_arms(stouffer) = 0.00904173
```

Both reject at α = 0.05. Against the *empirical* null of §3.3 the result is stronger still:
`P(Fisher ≤ 0.015373)` under a site-uninformative field is **0.0000–0.0003** across λ.

**The mechanism is arithmetic, not biology: pyKVFinder's site pocket is the largest cavity in
the protein on two of the three arms.** Ranking residues by the volume of the cavity that
lines them therefore separates the site from non-functional pockets by construction, with no
model of allostery anywhere in it.

ADR 0025 met the identical situation on family 1 and answered it by declaring a claim
threshold: a method must **beat** `cavity_volume`, and ADR 0032 made that its own Holm-
corrected family. **No equivalent threshold exists for negative class (b).** A report can
print "Fisher p = 0.004, negative class (b) rejected" with nothing in the protocol to say
that a zero-parameter cavity ruler reaches 0.0154 on the same endpoint. That is the same
defect ADR 0025 called blocker B2, in the one place ADR 0025 did not look.

---

## 4. What is the actual power of the confirmatory family?

### 4.1 Minimum detectable effect, per arm

From `experiments/2026-09-02-null-recalibration/metrics.json`, the committed sensitivity
analysis, which simulates the real procedure at the **calibrated** threshold
`sf(size_ratio · z(level))` rather than at nominal α. Median AUC-ROC achieved at the shift
giving 80 % power:

| Arm | level | λ = 4 | λ = 8 | λ = 12 | λ = 20 |
| --- | --- | ---: | ---: | ---: | ---: |
| `kras_g12c_corrected` | α | 0.786 | 0.842 | 0.868 | 0.895 |
| | α/2 | 0.814 | 0.868 | 0.884 | 0.907 |
| | α/3 | 0.827 | 0.881 | 0.891 | 0.914 |
| `bcr_abl1_corrected` | α | 0.762 | 0.850 | 0.880 | 0.908 |
| | α/2 | 0.787 | 0.873 | 0.902 | 0.925 |
| | α/3 | 0.799 | 0.883 | 0.911 | 0.934 |
| `cardiac_myosin_corrected` | α | 0.769 | 0.850 | 0.897 | 0.937 |
| | α/2 | 0.796 | 0.878 | 0.921 | 0.953 |
| | α/3 | 0.810 | 0.892 | 0.932 | 0.961 |

**MDE band: AUC-ROC 0.762–0.937 at α, 0.799–0.961 at α/3.** This reproduces the ADR 0025
Amendment 2 figures (0.762–0.936 and 0.799–0.961) and my independent re-simulation agrees:
at λ = 8 and shift 1.2 I measure per-arm power 0.803 / 0.778 / 0.732 where the committed run
puts the 80 % shift at 1.2422 / 1.3125 / 1.3711. **Confirmed (C9).**

### 4.2 The number the repository does not have: family-level power

Every published MDE here is *per arm*. The deliverable is four targets, and ADR 0032 makes a
claim require rejection in two families. `q4_familypower.py` (Appendix A.7) runs Holm over
the three arms, 4000 replicates, same data-generating model:

**λ = 8 Å**

| shift (SD) | KRAS | BCR-ABL1 | myosin | median AUC | **P(all 3 reject)** | P(≥ 1 rejects) |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.00 | 0.684 | 0.666 | 0.596 | 0.785 | 0.259 | 0.878 |
| 1.20 | 0.803 | 0.778 | 0.732 | 0.829 | 0.445 | 0.959 |
| 1.40 | 0.888 | 0.874 | 0.833 | 0.866 | 0.637 | 0.987 |
| 1.60 | 0.941 | 0.930 | 0.904 | 0.898 | 0.785 | 0.998 |
| 1.80 | 0.972 | 0.965 | 0.944 | 0.925 | 0.883 | 1.000 |

**λ = 12 Å**: `P(all 3)` reaches 0.704 at shift 1.60 (AUC 0.916) and 0.815 at 1.80 (AUC 0.940).

**80 % power to reject on all three confirmatory arms needs a shift of ≈ 1.63 SD, median
AUC-ROC ≈ 0.90, at λ = 8 Å — and ≈ 1.77 SD, AUC ≈ 0.94, at λ = 12 Å.** Eighty per cent power
for *at least one* arm needs only AUC ≈ 0.75. The gap between "the protocol rejects
somewhere" and "the protocol rejects everywhere" is roughly 0.15 AUC, and only the second
supports a per-target deliverable. Published elastic-network AUCs sit at 0.75–0.82, which is
below the family-level bar on every arm.

### 4.3 The permutation floor, and the trap that is not there

Family 1 uses B = 9999, raw floor 1/10000. Family 2 (`compare_methods`) uses the same pool
and the same replicate count, so it has the same raw floor.

| Arm | `size_ratio` | **smallest attainable `p_calibrated`** | Holm step 1 (α/3) | headroom |
| --- | ---: | ---: | ---: | ---: |
| `kras_g12c_corrected` | 1.0827 | **0.000296** | 0.016667 | ×56 |
| `bcr_abl1_corrected` | 1.0970 | **0.000349** | 0.016667 | ×48 |
| `cardiac_myosin_corrected` | 1.0000 | **0.000100** | 0.016667 | ×167 |

**No trap on the primary confirmatory arms.**

**S5 — and the recorded trap on the secondary arms is an error.** `docs/ROADMAP.md:330`,
`experiments/REGISTRY.md:12`, `experiments/2026-08-26-beats-distance/notes.md` and
`docs/method/exploration/results/46-beats-distance.md` all state that a "permutation floor"
of 0.001080 exceeds Holm's first step on `ptp1b` and `ns5b`, so "Holm cannot reject at any
data". 0.001080 is not a floor. `notes.md` itself says it is "the smallest calibrated p
anywhere in these 272 tests", and inverting the rescale identifies its source exactly:
`sf(isf(0.001080) × 1.1541) = 2.00/10000` — one `hiv_rt` record whose observed statistic was
matched by exactly one of 9999 null replicates. The per-arm floors are:

| Arm | `size_ratio` | true floor | Holm step 1 | can Holm reject? |
| --- | ---: | ---: | ---: | --- |
| `hiv_rt` | 1.1541 | 0.000636 | 0.025000 (m=2) | yes, ×39 |
| `mkp5` | 1.1398 | 0.000551 | 0.004167 (m=12) | yes, ×7.6 |
| `ptp1b` | 1.0768 | **0.000276** | 0.000909 (m=55) | **yes, ×3.3** |
| `ns5b` | 1.0027 | **0.000104** | 0.000893 (m=56) | **yes, ×8.6** |

The correct statement is that the headroom on `ptp1b` is only 3.3×, so a rejection there
needs a p in the top 3 of 10 000 permutations — tight, but not impossible. "Uninterpretable
at any data" overstates it and should be corrected in all four documents.

### 4.4 Family 2's size, measured for the first time

`compare_methods` applies the arm's `size_ratio` — fitted for a **one-sided** test on a
**single** Gaussian field — to a **two-sided** test on the **difference of two rank fields**.
The docstring concedes the approximation and argues "it only ever tightens, so the direction
is the safe one". That conflates *tightening relative to the raw p* with *controlling size*,
and no gate was ever run. `q12c_focus.py` runs one: two independent fields, 60 000
replicates.

| Arm | λ method / baseline | size at α/3 [95 % CI] | at α/2 | at α |
| --- | --- | --- | --- | --- |
| `bcr_abl1_corrected` | 8 / 100 | 0.01637 [0.01535, 0.01738] | 0.02407 | 0.04707 [0.04537, 0.04876] |
| `bcr_abl1_corrected` | 20 / 4 | 0.01473 | 0.02232 | 0.04607 |
| `bcr_abl1_corrected` | 20 / 20 | 0.01583 | 0.02292 | 0.04523 |
| `bcr_abl1_corrected` | 4 / 4 | 0.01252 | 0.01933 | 0.04118 |
| `kras_g12c_corrected` | 8 / 100 | 0.00363 | 0.00585 | 0.01347 |
| `cardiac_myosin_corrected` | 8 / 100 | 0.01120 | 0.01695 | 0.03392 |

Family-2 FWER under Holm over three, 20 000 replicates, λ 4–100: **0.0293–0.0339**.

**S8 — the gap is now closed and the answer is favourable: family 2 holds its size** (worst
cell 0.01637 against 0.016667, CI overlapping but the point estimate under). Two caveats
stand. On `kras_g12c_corrected` it is 3.7× conservative at α, so family 2 has little power
there. And the null simulated is *exchangeable* — two i.i.d. fields — whereas the frozen
reference `cavity_volume` is a fixed, blocky, informative score. No simulation can make
"the method equals `cavity_volume`" a true null, so this measures the machinery, not the
declared comparison.

---

## 5. Is the mean midrank the right endpoint?

### 5.1 The identity, proved

With `n_p` positives and `n_n` negatives, the rank-based Mann-Whitney AUC is

```
AUC = (Σ_{i∈P} r_i − n_p(n_p+1)/2) / (n_p · n_n)
    = (mean_midrank − (n_p+1)/2) / n_n
```

an **affine, strictly increasing** map with slope `1/n_n > 0`. It holds exactly under ties,
because `rank_vector` uses midranks and midranks are what make `U/(n_p n_n) = AUC` exact.
So ADR 0022's claim is not merely true under a size-preserving null: it is an algebraic
identity for any fixed `(n_p, n_n)`.

### 5.2 Does it survive the matched-patch null? Yes, and the code enforces it

The concern in the question — that the matched null "is not size-preserving in the same
sense" — does not bite. Matching on components, degree and radius of gyration constrains
*which* residues a replicate holds; it does not change *how many*. `harness.score_arm`
asserts this rather than assuming it:

```text
patch_sizes = geometry.sum(1)
if not np.all(patch_sizes == len(labels)):
    raise ValueError(f"{target}: matched patches are not all size {len(labels)}")
```

Every replicate therefore has the same `n_p` and the same `n_n` as the observation, so the
affine map has identical constants for the observed value and every null value, and the
permutation p is invariant under it. Verified numerically on all three confirmatory arms, 20
random score vectors each with 30 % of entries forced to a tie:

| Arm | max \|AUC_direct − AUC_from_midrank\| | all pool sizes == n_p | permutation p identical |
| --- | ---: | --- | --- |
| `kras_g12c_corrected` | 0.00e+00 | True | True |
| `bcr_abl1_corrected` | 2.79e−08 | True | True |
| `cardiac_myosin_corrected` | 1.39e−08 | True | True |

Residuals are float32 rounding from `.astype(np.float32)` on the rank vector. **Confirmed
(C4).**

### 5.3 What the endpoint actually measures — a distinction the README blurs

The identity is *within one arm, between two statistics*. It is **not** an equivalence
between "the reported AUC-ROC" and "the p-value", and the two answer different questions:

* the reported `auc_roc` compares the label set against **all** candidates;
* the p-value compares the label set against **matched patches** — contiguous, equally
  buried, equally compact residue sets.

They can and do point in opposite directions. Under v3, `cavity_volume` on
`kras_g12c_corrected` reads AUC-ROC 0.843 — a strong-looking number — at `p_calibrated`
0.0715, no rejection: matched patches score nearly as well. Conversely `cardiac_myosin_
corrected` reads AUC 0.806 and rejects at 0.0046. **README §3.1's "the effect size reported
beside it is the metric this field actually uses" is true of the statistic and misleading
about the inference.** The AUC printed beside the p-value is not the effect size the p-value
tests; the effect size the p-value tests is the label patch's elevation *above matched
patches*, which the record never prints. A one-line addition — the observed mean midrank
against the pool's mean and sd — would fix it.

---

## 6. Prevalence and decoy coverage

### 6.1 What an 8.5× prevalence spread does to AUC-PR comparability

Prevalence runs 0.0129 (`cardiac_myosin_mandated`) to 0.1096 (`kras_g12c_mandated`), a
factor of **8.51**. `q2356.py` simulates the null distribution of the frozen step estimator
(`metrics.auc_pr`) at each arm's exact `(n_positive, n_candidates)`, 4000 uniformly random
rankings per arm:

| Arm | prevalence | null AP mean | ×prev | null AP p95 | ×prev |
| --- | ---: | ---: | ---: | ---: | ---: |
| `kras_g12c_mandated` | 0.1096 | 0.1377 | 1.26 | 0.2164 | 1.97 |
| `kras_g12c_corrected` | 0.1081 | 0.1366 | 1.26 | 0.2180 | 2.02 |
| `mkp5` | 0.0809 | 0.1114 | 1.38 | 0.2036 | 2.52 |
| `bcr_abl1_corrected` | 0.0690 | 0.0879 | 1.27 | 0.1452 | 2.10 |
| `bcr_abl1_mandated` | 0.0480 | 0.0631 | 1.31 | 0.1116 | 2.32 |
| `chk1` | 0.0460 | 0.0641 | 1.39 | 0.1252 | 2.72 |
| `glucokinase` | 0.0434 | 0.0555 | 1.28 | 0.0957 | 2.21 |
| `ptp1b` | 0.0383 | 0.0566 | **1.48** | 0.1245 | **3.25** |
| `hiv_rt` | 0.0300 | 0.0409 | 1.37 | 0.0762 | 2.54 |
| `smyd3` | 0.0294 | 0.0436 | 1.48 | 0.0900 | 3.06 |
| `ns5b` | 0.0291 | 0.0391 | 1.35 | 0.0722 | 2.48 |
| `p97_vcp` | 0.0247 | 0.0337 | 1.36 | 0.0638 | 2.58 |
| `ecoli_cps` | 0.0191 | 0.0253 | 1.33 | 0.0448 | 2.35 |
| `cardiac_myosin_corrected` | 0.0162 | 0.0243 | **1.50** | 0.0504 | **3.12** |
| `cardiac_myosin_mandated` | 0.0129 | 0.0194 | **1.51** | 0.0396 | 3.08 |

**S6, two distinct costs.**

*The stated chance line is wrong.* README §3.2 and ADR 0022 both say AUC-PR "must always be
printed against its chance line, which is the prevalence". The null **mean** of the frozen
step estimator is 1.26× to 1.51× prevalence — prevalence is the chance line for
*precision*, not for the step AP, which is upward-biased at small `n_positive`. The bias
itself varies by a factor of 1.20 across arms, so the error is not even a constant offset.
And `frozen.json.chance` carries `precision_at_5`, `recall_at_5`, `p_at_least_one_hit_at_5`
and `dcc_angstrom` — **no AUC-PR chance line is frozen at all**, so nothing re-derives it.
The fix costs one seeded Monte Carlo per arm, exactly as `chance_dcc` already does.

*Cross-arm comparison of a raw AP is meaningless.* AP = 0.10 sits **below** the null mean on
both KRAS arms (0.137) and **above the 95th percentile** on `cardiac_myosin_mandated`
(0.0396). The same number is worse-than-chance on one arm and significant on another. Any
table that ranks arms or methods by bare AP is reading noise; the comparable quantity is
AP/null-mean or a per-arm percentile, and neither is frozen.

### 6.2 What poor site coverage costs, endpoint by endpoint

`q6_decoys.py` re-runs the frozen v3 detector and `decoys.classify` on the three confirmatory
arms and the four low-coverage arms:

| Arm | n_pos | site coverage | labels in **any** detected pocket | labels in **no** pocket | n_decoys | decoy lining residues | floor |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `kras_g12c_corrected` | 16 | 0.9375 | 15 | 1 | 18 | 64 | 0.052632 |
| `bcr_abl1_corrected` | 18 | 0.9444 | 18 | 0 | 31 | 198 | 0.031250 |
| `cardiac_myosin_corrected` | 12 | 1.0000 | 12 | 0 | 84 | 464 | 0.011765 |
| `ns5b` | 16 | **0.3125** | 9 | **7** | 50 | 260 | 0.019608 |
| `ptp1b` | 11 | **0.3636** | 9 | 2 | 33 | 175 | 0.029412 |
| `mkp5` | 11 | **0.4545** | 6 | **5** | 14 | 66 | 0.066667 |
| `hiv_rt` | 16 | 0.6250 | 15 | 1 | 68 | 383 | 0.014493 |

**The first thing to establish is what coverage does *not* touch, because the natural fear is
wrong.** `score_arm` computes the decoy p-value from `observed`, the mean midrank of the
**full label set**, against `decoy_ranks`, the mean midranks of the **decoy** linings. The
site pocket appears in exactly one place, `site_pocket_rank`, which the manifest declares
descriptive. And `classify` guarantees a decoy lining shares no residue with the label set,
so uncovered label residues never migrate into the negative class. **Coverage does not enter
the decoy p-value, the Fisher combination, or `auc_roc_vs_decoy_linings`.** All four
low-coverage arms are secondary; site coverage on the confirmatory family is 0.94–1.00.

**What it does cost, in three parts:**

1. **`site_pocket_rank` measures the wrong object on four arms.** On `ns5b` "the site
   pocket" holds 5 of 16 label residues; on `ptp1b` 4 of 11; on `mkp5` 5 of 11. The APOP
   convention this endpoint exists to reproduce
   (doi:10.1093/bioinformatics/btad275) is being applied to a cavity that is a third of the
   site. The endpoint is descriptive, so no decision moves — but it is the number a reader
   compares to PASSer and APOP, and on those arms it is not comparable.
2. **The label set is fragmented across pockets, and the fragments leave the negative
   class.** On `ns5b`, 9 of 16 labels lie in *some* detected pocket but only 5 in the site
   pocket, so 4 sit in pockets `classify` pushes into `excluded_by_halo` because they touch
   a label. Those pockets are removed from the decoy set. The negative class is therefore
   depleted of exactly the pockets most similar to the site — the hardest negatives — which
   makes the pocket test easier and is one more contributor to the conservatism of §3.3
   being smaller than it should be.
3. **31–45 % of the label set is invisible to any pocket-shaped score.** On `mkp5` 5 of 11
   labels and on `ns5b` 7 of 16 lie in no detected cavity, so `cavity_volume` assigns them 0
   and ties them at the bottom. That is the challenge's own premise measured — static pocket
   detection fails on these targets — and it is a difficulty axis, correctly. It also means
   the baseline is arm-dependent in strength, which §7 shows matters.

---

## 7. S1 — the pre-declared claim reference no longer does what the documents say

`q_cavity_v3.py` scores `decoys.cavity_volume_score` through `score_arm` under the **frozen
v3 settings** and runs `holm` over the three confirmatory arms.

| Arm | AUC-ROC | AUC-PR | recall@5 | DCC (chance) | **`p_calibrated`** | Holm threshold | **reject** |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `cardiac_myosin_corrected` | 0.8064 | 0.0407 | 0.00 | 26.14 (28.73) | **0.0046** | 0.016667 | **yes** |
| `kras_g12c_corrected` | 0.8430 | 0.3264 | 0.00 | 13.30 (13.10) | **0.0715** | 0.025 | **no** |
| `bcr_abl1_corrected` | 0.5626 | 0.1298 | 0.00 | 26.74 (17.68) | **0.3236** | 0.05 | **no** |

Against the version-2 record in ADR 0025, AUDIT.md §B2 and `manifest.yaml`:

| Arm | AUC-ROC v2 | AUC-ROC v3 | `p_calibrated` v2 | `p_calibrated` v3 |
| --- | ---: | ---: | ---: | ---: |
| `kras_g12c_corrected` | 0.830 | 0.843 | 0.0047 – 0.0073 | **0.0715** |
| `bcr_abl1_corrected` | 0.795 | **0.563** | 0.0001 – 0.0003 | **0.3236** |
| `cardiac_myosin_corrected` | 0.977 | **0.806** | 0.0001 | 0.0046 |

**Three consequences, and none is recorded anywhere.**

1. **ADR 0025's founding measurement no longer reproduces.** "A trivial geometric baseline
   clears the whole confirmatory family" was the evidence that made "clearing the null is a
   low bar" a fact and made "beat `cavity_volume`" the claim threshold. Under v3 the
   baseline clears **one** arm of three. The decision ADR 0025 reached is still the right
   one — a stricter bar is never wrong — but the empirical support for it has moved and the
   ADR should say so.
2. **ADR 0032's non-redundancy illustration no longer holds.** It argues families 1 and 2 are
   not redundant because "on `bcr_abl1_corrected`, `cavity_volume` itself rejects family 1 at
   `p_calibrated` 0.0003 while its predicted centre sits farther from the site than a random
   five-residue list". Under v3 the DCC half survives (26.74 Å against a chance line of
   17.68 Å) and the rejection half does not (0.3236). A different arm now carries the point:
   `cardiac_myosin_corrected` rejects at 0.0046 with recall@5 = 0.00 and 0 hits in the top
   five.
3. **The claim bar fell, as a side effect of a change made for another reason.** ADR 0030
   re-froze the detector selecting on `n_decoys` alone. `n_decoys` is label-free, so this is
   not leakage and not tuning on the answer key — the audit finds no C1 problem. But
   `cavity_volume` is computed *from the same detector settings*, so re-freezing them also
   re-defined the pre-declared reference of confirmatory family 2, weakening it on two arms
   (AUC 0.795 → 0.563 on `bcr_abl1_corrected`). ADR 0030's consequence list does not mention
   it. A method now has a materially easier reference to beat than version 2 declared, and
   the manifest still quotes the version-1 numbers — `required_baselines` reads "it rejects
   on all three confirmatory arms under the frozen null and Holm (p_calibrated 0.0047,
   0.0001, 0.0001)", which is a v1 triple; ADR 0025 gives a third, different triple
   (0.0073, 0.0003, 0.0001). Three sets of numbers for one baseline, none of them current.

**Recommendation:** re-run `cavity_volume` through `score_arm` under v3, record the result in
`experiments/REGISTRY.md`, and amend ADR 0025, ADR 0032 and `manifest.yaml` to carry the v3
triple with its version stated. Nothing has been scored, so this is a documentation repair,
not a re-freeze — but it must happen before any method is scored, because a claim threshold
whose value nobody has measured is not a threshold.

---

## 8. S7 — three α = 0.05 decisions, no correction between them

Protocol version 3 declares **three** tested quantities, each at α = 0.05:

| | test | correction inside it |
| --- | --- | --- |
| family 1 | matched-patch permutation, 3 arms | Holm over 3 |
| family 2 | paired `compare_methods` against `cavity_volume`, 3 arms | Holm over 3 |
| negative class (b) | `decoy_pockets_combined`, Fisher over 3 arms | none — one test |

Nothing corrects across the three. Two readings, and they differ:

* **As a conjunction** — a claim requires family 1 **and** family 2, and the challenge
  requires both negative classes — this is an intersection-union test and needs no
  correction. Its type-I rate is bounded by the smallest of the three, so it is
  *conservative*, materially so given §3.3's 0.0014–0.0066 and §4.4's 0.029–0.034.
* **As three reported findings** — "we reject the matched-patch null", "we beat the
  baseline", "we separate the site from non-functional pockets" — the study-wise error is up
  to 0.15 by Bonferroni union.

The manifest says "a method must clear BOTH families to support a claim" and labels
`decoy_pockets_combined` the tested form of (b), which is the conjunctive reading. It never
says that the individual family-1 or negative-class-(b) rejections are **not** claims in
their own right. Given that §7 shows a cavity ruler rejects family 1 on one arm and negative
class (b) at the family level, the distinction is load-bearing and should be written into
§8 of the protocol README in one sentence.

---

## 9. Confirmed claims

| | Claim | Measured |
| --- | --- | --- |
| **C1** | The probit rescale composed with Holm controls FWER at 0.05 | out-of-sample FWER 0.0376–0.0452 over λ = 4–100 Å, 20 000 draws each |
| **C2** | Calibration "may tighten and may never loosen" | 0 violations of `calibrated_p(p, r) ≥ p` over 30 600 (p, ratio) pairs |
| **C3** | Calibrating at every Holm level is sufficient | Holm's proof needs validity at α/m₀ only, m₀ ∈ {1,2,3} — exactly the fitted set |
| **C4** | Mean midrank is a strictly increasing function of AUC-ROC, and the permutation p is unchanged | affine identity; max \|ΔAUC\| = 2.8e−8; p bit-identical on 60 score vectors; pool sizes all = n_p |
| **C5** | No Holm trap on the primary confirmatory arms | floors 0.000296 / 0.000349 / 0.000100 against α/3 = 0.016667 |
| **C6** | Fisher's independence assumption | cross-arm probit correlations \|ρ\| ≤ 0.010 at 20 000 replicates (SE 0.007) |
| **C7** | Minimum attainable combined p | Fisher/Stouffer 0.0214306 / 0.0115158 (v2) and 0.0013689 / 0.000452975 (v3), matching ADR 0030 and the manifest |
| **C8** | "13 of 15 arms reproduce their 2026-08-25 calibration" | 14 arms in both runs; exactly one moved (`bcr_abl1_mandated` 1.096 → 1.2073); `cardiac_myosin_mandated` is new |
| **C9** | The published MDE band | 0.762–0.937 at α, 0.799–0.961 at α/3; independent re-simulation agrees at λ = 8 |
| **C10** | README §5.3's decoy lining size disclosure | median lining/label ratio 0.412 under v3 on 15 of 15 arms, exactly as stated |

---

## 10. Unknowns

Three questions this audit could not settle, and what would settle each.

* **The true size of confirmatory family 2 as it will actually run.** §4.4 measures an
  exchangeable two-field null. The declared reference is a fixed, blocky, informative score,
  and no simulation can make "the method equals `cavity_volume`" a true null. **Unknown.**
  What would settle it: a permutation of the *pocket→volume* assignment, which preserves
  `cavity_volume`'s spatial structure while destroying its site information, run through
  `compare_methods` as the type-I gate ADR 0018 applies to every other null.
* **Whether the matched-patch calibration holds for a score field that is neither Gaussian-
  Euclidean nor band-limited-spectral.** Two classes were tested and both pass. A third — a
  heavy-tailed or bimodal score, which a sink-based non-Hermitian walk can produce — is
  **unknown**. What would settle it: add the actual `quantum.walk.SCORERS` observables,
  randomised over their own free parameters, to the calibration's field set.
* **Whether Fisher's measured independence survives a real method.** §3.2 measures ρ ≈ 0
  under synthetic fields drawn independently per arm. A single method applied to all three
  arms is one realisation, not a sample, so its cross-arm dependence is not estimable from
  the protocol's own data. **Unknown, and not estimable at three arms.** What would settle
  it: the `secondary/development` tier, where the same statistic can be computed across
  enough arms to estimate ρ empirically.

---

## Appendix A — scripts, verbatim

All scripts were run from the repository root with `uv run python`, and live outside the
repository. None is tracked. Every code fence in this document is `text` rather than
`python` on purpose: `ruff format --check` rewrites Python fenced in Markdown, and these
blocks must stay byte-identical to the source that was read or run.

### A.1 `q345_exact.py` — exact Fisher/Stouffer null, permutation floors

```text
"""Q3/Q4/Q5: exact enumeration of the Fisher null, permutation floors, midrank<->AUC."""
import itertools, json
import numpy as np
from scipy.stats import chi2, norm

ARMS = ["kras_g12c_corrected", "bcr_abl1_corrected", "cardiac_myosin_corrected"]
FROZEN = json.load(open("docs/benchmark/evaluation/frozen.json"))["targets"]

# ---- Q3a: exact null of Fisher / Stouffer on three discrete pocket-permutation p-values ----
# p_i = (1 + #{decoy >= site}) / (1 + n_i), so p_i is uniform on {1/(n+1), ..., (n+1)/(n+1)}
# under exchangeability of the label statistic with the n decoy statistics.
n = [len(FROZEN[a]["decoys"]["pockets"]) for a in ARMS]
print("n_decoys v3:", dict(zip(ARMS, n)))
supports = [np.arange(1, k + 2) / (k + 1) for k in n]

def combine(ps, how):
    ps = np.asarray(ps, float)
    if how == "fisher":
        return float(chi2.sf(-2 * np.log(ps).sum(), 2 * ps.size))
    return float(norm.sf(norm.isf(ps).sum() / np.sqrt(ps.size)))

def exact(supports, how):
    """Exact null distribution of the combined p over the product support."""
    grid = np.array(list(itertools.product(*supports)))
    if how == "fisher":
        stat = -2 * np.log(grid).sum(1)
        p = chi2.sf(stat, 2 * grid.shape[1])
    else:
        z = norm.isf(grid)
        p = norm.sf(z.sum(1) / np.sqrt(grid.shape[1]))
    return p

for how in ("fisher", "stouffer"):
    p_null = exact(supports, how)
    floor = combine([s[0] for s in supports], how)
    for a in (0.05, 0.025, 0.0167):
        print(f"{how:9s} exact size at nominal {a:<7}: {np.mean(p_null <= a):.5f}  (N={p_null.size})")
    print(f"{how:9s} minimum attainable p (v3): {floor:.6g}")

# v2 decoy counts from ADR 0024 / ADR 0030 table
n2 = [3, 9, 41]
sup2 = [np.arange(1, k + 2) / (k + 1) for k in n2]
for how in ("fisher", "stouffer"):
    print(f"{how:9s} minimum attainable p (v2, n_decoys={n2}): "
          f"{combine([s[0] for s in sup2], how):.6g}")
    p2 = exact(sup2, how)
    print(f"{how:9s} exact size at nominal 0.05 (v2): {np.mean(p2 <= 0.05):.5f}")

# ---- Q3b: what equicorrelation does to Fisher (Brown 1975 / Kost & McDermott 2002) ----
# cov(-2 ln p_i, -2 ln p_j) ~ 3.263 rho + 0.710 rho^2 + 0.027 rho^3 for p from correlated
# normal one-sided tests.  doi:10.1016/S0167-7152(02)00310-3
k = 3
print("\nBrown/Kost scaled-chi2 size of a nominal-0.05 Fisher test, k=3, equicorrelated:")
for rho in (0.0, 0.1, 0.2, 0.3, 0.5, 0.7, 0.9):
    cov = 3.263 * rho + 0.710 * rho**2 + 0.027 * rho**3
    var = 4 * k + 2 * k * (k - 1) * cov
    c = var / (2 * 2 * k)          # scale
    f = 2 * (2 * k) ** 2 / var     # effective df
    crit = chi2.isf(0.05, 2 * k)   # threshold the protocol actually uses
    size = chi2.sf(crit / c, f)
    print(f"  rho={rho:4.2f}  E=2k={2*k}  Var={var:7.3f}  df_eff={f:6.2f}  true size={size:.4f}")

# ---- Q4: permutation floors ----
print("\nQ4 floors, matched-patch family (B = 9999 replicates, raw floor 1e-4):")
B = 9999
raw_floor = 1 / (1 + B)
for a in ARMS:
    r = FROZEN[a]["matched_patch"]["size_ratio"]
    cal = float(min(1.0, max(raw_floor, norm.sf(norm.isf(raw_floor) / max(r, 1.0)))))
    print(f"  {a:26s} size_ratio={r:<7} floor p_cal={cal:.6f}  "
          f"Holm step1 = {0.05/3:.6f}  headroom x{0.05/3/cal:.1f}")

print("\nQ4 floors on the four development arms of 2026-08-26-beats-distance:")
ALL = json.load(open("docs/benchmark/evaluation/frozen.json"))["targets"]
for a, m in (("hiv_rt", 2), ("mkp5", 12), ("ptp1b", 55), ("ns5b", 56)):
    r = ALL[a]["matched_patch"]["size_ratio"]
    cal = float(norm.sf(norm.isf(raw_floor) / max(r, 1.0)))
    step1 = 0.05 / m
    print(f"  {a:8s} ratio={r:<7} true floor={cal:.6f}  Holm step1={step1:.6f}  "
          f"can reject? {'YES' if cal <= step1 else 'no'}")
# what raw p produces the 0.001080 the repo calls a floor
for a in ("hiv_rt", "mkp5", "ptp1b", "ns5b"):
    r = ALL[a]["matched_patch"]["size_ratio"]
    raw = float(norm.sf(norm.isf(0.001080) * r))
    print(f"  {a:8s}: p_cal 0.001080 <- raw p {raw:.6g} = {raw*10000:.2f}/10000")
```

### A.2 `q12_fwer.py` — out-of-sample size and FWER

```text
"""Q1/Q2: out-of-sample size of the calibrated matched-patch test, FWER of Holm over the
three confirmatory arms, and the size of `compare_methods` (family 2), which has no gate.

Everything runs through the repo's own primitives: the cached 9999-patch pools, the same
exponential-covariance field, the same midrank vector, the same permutation p, the same
`calibrated_p`.  Only the seed differs from the frozen calibration, so this is an honest
out-of-sample check of a ratio that was fitted on `seed + 1`.
"""
import json, sys, time
import numpy as np
from scipy.stats import norm, rankdata

from allo.inputs import apo_input
from allo.scoring.harness import _positives, calibrated_p, holm
from allo.scoring.nulls import evaluation_graph, field_factor, matched_patches

ARMS = ["kras_g12c_corrected", "bcr_abl1_corrected", "cardiac_myosin_corrected"]
FROZEN = json.load(open("docs/benchmark/evaluation/frozen.json"))["targets"]
ALPHA = 0.05
LEVELS = {"alpha/3": ALPHA / 3, "alpha/2": ALPHA / 2, "alpha": ALPHA}
LAMBDAS = [4.0, 8.0, 12.0, 20.0, 40.0, 100.0]
N_FIELDS = int(sys.argv[1]) if len(sys.argv) > 1 else 4000
SEED = 20260902           # NOT the frozen seed: out-of-sample by construction
CHUNK = 200


def arm_setup(target):
    graph = evaluation_graph(apo_input(target))
    labels, _ = _positives(target)
    mask = np.array([r in set(labels) for r in graph.candidates], dtype=bool)
    patches, _ = matched_patches(graph, labels, n_patches=9999, tolerance=0.10, seed=0)
    members = patches[:, graph.index(graph.candidates)].astype(np.float32)
    coords = graph.ca_coord[graph.index(graph.candidates)]
    return dict(mask=mask, members=members, sizes=members.sum(1), coords=coords,
                ratio=float(FROZEN[target]["matched_patch"]["size_ratio"]))


def raw_p_batch(members, sizes, mask, fields):
    """One raw upper-tail p per column of `fields`, against the shared matched pool."""
    ranks = rankdata(fields, axis=0, method="average").astype(np.float32)
    observed = ranks[mask].mean(0)                       # (n_fields,)
    null = (members @ ranks) / sizes[:, None]            # (9999, n_fields)
    return (1 + (null >= observed).sum(0)) / (1 + null.shape[0])


def two_sided_p_batch(members, sizes, mask, delta):
    ranks = delta.astype(np.float32)
    observed = ranks[mask].mean(0)
    null = (members @ ranks) / sizes[:, None]
    centre = np.median(null, axis=0)
    extreme = (np.abs(null - centre) >= np.abs(observed - centre)).sum(0)
    return (1 + extreme) / (1 + null.shape[0])


setups = {a: arm_setup(a) for a in ARMS}
for a in ARMS:
    print(f"{a}: {setups[a]['members'].shape[1]} candidates, "
          f"{int(setups[a]['mask'].sum())} positives, size_ratio {setups[a]['ratio']}")

out = {}
for lam in LAMBDAS:
    t0 = time.time()
    factors = {a: field_factor(setups[a]["coords"], lam) for a in ARMS}
    p_cal = {a: [] for a in ARMS}
    p_raw = {a: [] for a in ARMS}
    p_cmp = {a: [] for a in ARMS}
    for a in ARMS:
        s, f = setups[a], factors[a]
        rng = np.random.default_rng(SEED + 1000 * ARMS.index(a))
        done = 0
        while done < N_FIELDS:
            b = min(CHUNK, N_FIELDS - done)
            z = rng.standard_normal((f.shape[0], b))
            fields = f @ z
            r = raw_p_batch(s["members"], s["sizes"], s["mask"], fields)
            p_raw[a].extend(r.tolist())
            p_cal[a].extend([calibrated_p(float(x), s["ratio"]) for x in r])
            # family 2 under an exchangeable null: two independent uninformative scores
            other = f @ rng.standard_normal((f.shape[0], b))
            delta = (rankdata(fields, axis=0, method="average")
                     - rankdata(other, axis=0, method="average"))
            c = two_sided_p_batch(s["members"], s["sizes"], s["mask"], delta)
            p_cmp[a].extend([calibrated_p(float(x), s["ratio"]) for x in c])
            done += b
    P = {a: np.array(p_cal[a]) for a in ARMS}
    R = {a: np.array(p_raw[a]) for a in ARMS}
    C = {a: np.array(p_cmp[a]) for a in ARMS}
    row = {"lambda": lam, "per_arm": {}, "seconds": round(time.time() - t0, 1)}
    for a in ARMS:
        row["per_arm"][a] = {
            "raw_size_at_alpha": round(float((R[a] <= ALPHA).mean()), 4),
            "cal_size": {k: round(float((P[a] <= v).mean()), 5) for k, v in LEVELS.items()},
            "cmp_size": {k: round(float((C[a] <= v).mean()), 5) for k, v in LEVELS.items()},
        }
    # FWER of Holm over the three arms, all three nulls true.
    rejects = 0
    for i in range(N_FIELDS):
        v = holm({a: float(P[a][i]) for a in ARMS}, alpha=ALPHA)
        rejects += any(d["reject"] for d in v.values())
    row["fwer_holm_3_true_nulls"] = round(rejects / N_FIELDS, 5)
    # and family 2's FWER on the same construction
    rejects2 = 0
    for i in range(N_FIELDS):
        v = holm({a: float(C[a][i]) for a in ARMS}, alpha=ALPHA)
        rejects2 += any(d["reject"] for d in v.values())
    row["fwer_holm_family2"] = round(rejects2 / N_FIELDS, 5)
    out[str(lam)] = row
    print(json.dumps(row, indent=1))

json.dump({"n_fields": N_FIELDS, "seed": SEED, "results": out},
          open(sys.argv[2] if len(sys.argv) > 2 else "/tmp/q12.json", "w"), indent=1)
```

### A.3–A.4 `q12b_ratio.py` and `q12c_focus.py` — ratio error, crossed λ, band-limited fields

`q12b_ratio.py` was the exploratory pass; `q12c_focus.py` is the high-precision rerun whose
numbers appear above. Only the second is reproduced.

```text
"""High-precision follow-up: family-2 size on the worst cells, band-limited fields with the
mode count capped at n-1, and P(the frozen 1000-field max under-tightens)."""
import json, sys
import numpy as np
from scipy.stats import norm, rankdata

from allo.inputs import apo_input
from allo.scoring.harness import _positives, calibrated_p
from allo.scoring.nulls import evaluation_graph, field_factor, matched_patches

ARMS = ["kras_g12c_corrected", "bcr_abl1_corrected", "cardiac_myosin_corrected"]
FROZEN = json.load(open("docs/benchmark/evaluation/frozen.json"))["targets"]
ALPHA = 0.05
LEVELS = {"alpha/3": ALPHA / 3, "alpha/2": ALPHA / 2, "alpha": ALPHA}
SEED = 777001


def setup(target):
    g = evaluation_graph(apo_input(target))
    labels, _ = _positives(target)
    mask = np.array([r in set(labels) for r in g.candidates], dtype=bool)
    patches, _ = matched_patches(g, labels, n_patches=9999, tolerance=0.10, seed=0)
    members = patches[:, g.index(g.candidates)].astype(np.float32)
    n = len(g.order)
    A = np.zeros((n, n))
    for i, r in enumerate(g.order):
        for nb in g.neighbours(r):
            A[i, g.position[nb]] = 1.0
    w, V = np.linalg.eigh(np.diag(A.sum(1)) - A)
    return dict(mask=mask, members=members, sizes=members.sum(1),
                coords=g.ca_coord[g.index(g.candidates)],
                ratio=float(FROZEN[target]["matched_patch"]["size_ratio"]),
                V=V[g.index(g.candidates)], n=n)


def raw_p(s, fields):
    ranks = rankdata(fields, axis=0, method="average").astype(np.float32)
    obs = ranks[s["mask"]].mean(0)
    null = (s["members"] @ ranks) / s["sizes"][:, None]
    return (1 + (null >= obs).sum(0)) / (1 + null.shape[0])


def two_sided(s, delta):
    ranks = delta.astype(np.float32)
    obs = ranks[s["mask"]].mean(0)
    null = (s["members"] @ ranks) / s["sizes"][:, None]
    c = np.median(null, axis=0)
    return (1 + (np.abs(null - c) >= np.abs(obs - c)).sum(0)) / (1 + null.shape[0])


S = {a: setup(a) for a in ARMS}
CH, out = 250, {}

print("=== family 2 size, 60000 replicates, the cells that ran over ===")
for a, lm, lb in [("bcr_abl1_corrected", 8.0, 100.0), ("bcr_abl1_corrected", 20.0, 4.0),
                  ("bcr_abl1_corrected", 20.0, 20.0), ("bcr_abl1_corrected", 4.0, 4.0),
                  ("kras_g12c_corrected", 8.0, 100.0),
                  ("cardiac_myosin_corrected", 8.0, 100.0)]:
    s = S[a]
    fm, fb = field_factor(s["coords"], lm), field_factor(s["coords"], lb)
    rng = np.random.default_rng(SEED + int(lm * 13 + lb) + 977 * ARMS.index(a))
    M, ps = 60000, []
    while len(ps) < M:
        b = min(CH, M - len(ps))
        d = (rankdata(fm @ rng.standard_normal((fm.shape[0], b)), axis=0, method="average")
             - rankdata(fb @ rng.standard_normal((fb.shape[0], b)), axis=0, method="average"))
        ps.extend([calibrated_p(float(x), s["ratio"]) for x in two_sided(s, d)])
    ps = np.array(ps)
    row = {}
    for k, t in LEVELS.items():
        hat = float((ps <= t).mean())
        se = (hat * (1 - hat) / M) ** 0.5
        row[k] = [round(hat, 5), round(hat - 1.96 * se, 5), round(hat + 1.96 * se, 5), t]
    out[f"fam2|{a}|{lm}v{lb}"] = row
    over = [k for k, v in row.items() if v[1] > v[3]]
    print(f"  {a:26s} {lm:5}/{lb:6}: " +
          "  ".join(f"{k} {v[0]:.5f} [{v[1]:.5f},{v[2]:.5f}] vs {v[3]:.5f}" for k, v in row.items())
          + (f"   SIGNIFICANTLY OVER at {over}" if over else ""))

print("\n=== matched-patch size under band-limited Laplacian fields (K modes) ===")
for a in ARMS:
    s = S[a]
    for K in (5, 20, 50, 150):
        if K >= s["n"]:
            continue
        V = s["V"][:, 1:1 + K]
        rng = np.random.default_rng(SEED + 5 + K + 977 * ARMS.index(a))
        M, ps = 20000, []
        while len(ps) < M:
            b = min(CH, M - len(ps))
            ps.extend([calibrated_p(float(x), s["ratio"])
                       for x in raw_p(s, V @ rng.standard_normal((K, b)))])
        ps = np.array(ps)
        row = {k: round(float((np.array(ps) <= t).mean()), 5) for k, t in LEVELS.items()}
        out[f"bandlimited|{a}|K{K}"] = row
        print(f"  {a:26s} K={K:4d}: {row}")

print("\n=== P(the frozen 1000-field max over 12 cells under-tightens) ===")
# 40 independent 1000-field blocks per arm; within a block the SAME innovations are reused
# across lambda, exactly as `calibrate_arm` does (field_rng is reset inside the lambda loop).
LAM = [4.0, 8.0, 12.0, 20.0]
for a in ARMS:
    s = S[a]
    factors = {l: field_factor(s["coords"], l) for l in LAM}
    B, block, ests = 40, 1000, []
    rng = np.random.default_rng(SEED + 3 + 977 * ARMS.index(a))
    big = {l: [] for l in LAM}
    for _ in range(B):
        z = rng.standard_normal((s["coords"].shape[0], block))     # shared innovations
        per = {}
        for l in LAM:
            per[l] = raw_p(s, factors[l] @ z)
            big[l].extend(per[l].tolist())
        cells = [norm.isf(min(float(np.quantile(per[l], t)), t)) / norm.isf(t)
                 for l in LAM for t in LEVELS.values()]
        ests.append(max(1.0, max(cells)))
    ests = np.array(ests)
    truth = max(1.0, max(
        norm.isf(min(float(np.quantile(np.array(big[l]), t)), t)) / norm.isf(t)
        for l in LAM for t in LEVELS.values()))
    out[f"ratio_mc|{a}"] = {"frozen": s["ratio"], "reference_40000": round(float(truth), 4),
                            "block_mean": round(float(ests.mean()), 4),
                            "block_sd": round(float(ests.std()), 4),
                            "P_block_below_reference": round(float((ests < truth).mean()), 3),
                            "P_block_below_frozen": round(float((ests < s["ratio"]).mean()), 3)}
    print(f"  {a:26s} frozen {s['ratio']:<7} 40000-field reference {truth:.4f}  "
          f"1000-field max: mean {ests.mean():.4f} sd {ests.std():.4f}  "
          f"P(<reference) {(ests < truth).mean():.3f}  P(<frozen) {(ests < s['ratio']).mean():.3f}")

json.dump(out, open(sys.argv[1] if len(sys.argv) > 1 else "/tmp/q12c.json", "w"), indent=1)
```

### A.5 `q2356.py` — one-sidedness, copula dependence, cavity attack, identity, AP nulls

```text
"""Q2 one-sidedness, Q3 dependence + the cavity-volume attack on negative class (b),
Q5 the midrank<->AUC identity, Q6 prevalence and AP comparability."""
import itertools, json, sys
import numpy as np
from scipy.stats import chi2, norm, rankdata

from allo.inputs import apo_input
from allo.scoring import metrics
from allo.scoring.decoys import cavity_volume_score, detect_pockets
from allo.scoring.harness import _positives, calibrated_p, combine_arms, protocol
from allo.scoring.nulls import evaluation_graph, matched_patches, permutation_p

ARMS = ["kras_g12c_corrected", "bcr_abl1_corrected", "cardiac_myosin_corrected"]
FROZEN = json.load(open("docs/benchmark/evaluation/frozen.json"))["targets"]
out = {}

# ---------------- Q2: is the rescale one-sided? -------------------------------------
print("=== Q2  calibrated_p(p, r) >= p for every p, every r >= 1 ? ===")
bad = []
for r in np.linspace(1.0, 1.5, 51):
    for p in np.r_[np.logspace(-6, -0.31, 400), np.linspace(0.5, 1.0, 200)]:
        if calibrated_p(float(p), float(r)) < float(p) - 1e-15:
            bad.append((float(p), float(r)))
print(f"  violations over 30600 (p, ratio) pairs: {len(bad)}")
print(f"  r < 1 is clamped: calibrated_p(0.01, 0.5) = {calibrated_p(0.01, 0.5)} (== raw 0.01)")
print(f"  above 0.5 the clamp binds: calibrated_p(0.8, 1.25) = {calibrated_p(0.8, 1.25)}")
out["q2_violations"] = len(bad)

# ---------------- Q3a: dependence, exact discrete supports under a Gaussian copula ---
print("\n=== Q3  Fisher on the three discrete pocket p-values, equicorrelated copula ===")
n = [len(FROZEN[a]["decoys"]["pockets"]) for a in ARMS]
sup = [k + 1 for k in n]
rng = np.random.default_rng(4242)
M = 400000
res = {}
for rho in (0.0, 0.1, 0.2, 0.3, 0.5, 0.7):
    C = np.full((3, 3), rho); np.fill_diagonal(C, 1.0)
    z = rng.multivariate_normal(np.zeros(3), C, size=M)
    u = norm.cdf(z)
    # discretise each margin onto {1/(n+1), ..., 1}: exactly the permutation p support
    p = np.column_stack([np.ceil(u[:, i] * sup[i]) / sup[i] for i in range(3)])
    fis = chi2.sf(-2 * np.log(p).sum(1), 6)
    sto = norm.sf(norm.isf(p).sum(1) / np.sqrt(3))
    res[rho] = {"fisher_size@0.05": round(float((fis <= 0.05).mean()), 5),
                "stouffer_size@0.05": round(float((sto <= 0.05).mean()), 5)}
    print(f"  rho={rho:4.2f}  Fisher {res[rho]['fisher_size@0.05']:.5f}   "
          f"Stouffer {res[rho]['stouffer_size@0.05']:.5f}")
out["q3_copula"] = res

# ---------------- Q3b: does a label-blind cavity score reject negative class (b)? ----
print("\n=== Q3  cavity_volume against negative class (b): per-arm p and the combination ===")
settings = protocol()
per_arm, detail = {}, {}
for a in ARMS:
    apo = apo_input(a)
    g = evaluation_graph(apo)
    labels, _ = _positives(a)
    pockets = detect_pockets(apo, **{k: float(v) for k, v in settings["decoys"]["detector_settings"].items()})
    scores = cavity_volume_score(pockets, g.candidates)
    values = np.array([scores[r] for r in g.candidates])
    ranks = metrics.rank_vector(values).astype(np.float32)
    pos = np.array([r in set(labels) for r in g.candidates], dtype=bool)
    at = {r: i for i, r in enumerate(g.candidates)}
    linings = [q["lining"] for q in FROZEN[a]["decoys"]["pockets"].values()]
    decoy_ranks = np.array([ranks[[at[r] for r in L]].mean() for L in linings])
    obs = float(ranks[pos].mean())
    p = permutation_p(obs, decoy_ranks)
    per_arm[a] = p
    site = FROZEN[a]["decoys"]["site_pocket"]
    detail[a] = {"p_decoy_pockets": p, "floor": FROZEN[a]["decoys"]["minimum_attainable_p"],
                 "auc_roc": round(metrics.auc_roc(values, pos), 4),
                 "site_pocket_volume": site["volume"],
                 "max_decoy_volume": round(max(q["volume"] for q in FROZEN[a]["decoys"]["pockets"].values()), 2),
                 "site_volume_rank_of_all": 1 + sum(
                     q["volume"] >= site["volume"] for q in FROZEN[a]["decoys"]["pockets"].values())}
    print(f"  {a:26s} p={p:.6f} (floor {detail[a]['floor']}), AUC-ROC {detail[a]['auc_roc']}, "
          f"site cavity volume {site['volume']} vs largest decoy {detail[a]['max_decoy_volume']} "
          f"-> site pocket is #{detail[a]['site_volume_rank_of_all']} by volume")
for how in ("fisher", "stouffer"):
    c = combine_arms(per_arm, method=how)
    print(f"  combine_arms({how}) over the confirmatory family: p = {c['p']}")
    detail[f"combined_{how}"] = c["p"]
out["q3_cavity"] = detail

# ---------------- Q5: mean midrank is an affine function of AUC-ROC ------------------
print("\n=== Q5  mean midrank <-> AUC-ROC under the matched-patch null ===")
q5 = {}
for a in ARMS:
    g = evaluation_graph(apo_input(a))
    labels, ncand = _positives(a)
    pos = np.array([r in set(labels) for r in g.candidates], dtype=bool)
    patches, _ = matched_patches(g, labels, n_patches=9999, tolerance=0.10, seed=0)
    members = patches[:, g.index(g.candidates)].astype(np.float32)
    sizes = members.sum(1)
    npos, nneg = int(pos.sum()), int(len(pos) - pos.sum())
    rng2 = np.random.default_rng(11)
    worst = 0.0
    identical = True
    for _ in range(20):
        v = rng2.standard_normal(len(pos))
        v[rng2.random(len(pos)) < 0.3] = 0.0            # force heavy ties
        ranks = metrics.rank_vector(v).astype(np.float32)
        # affine identity: AUC = (mean_midrank - (npos+1)/2) / nneg
        auc_direct = metrics.auc_roc(v, pos)
        auc_affine = (float(ranks[pos].mean()) - (npos + 1) / 2) / nneg
        worst = max(worst, abs(auc_direct - auc_affine))
        null_rank = (members @ ranks) / sizes
        p_rank = permutation_p(float(ranks[pos].mean()), null_rank)
        p_auc = permutation_p((float(ranks[pos].mean()) - (npos + 1) / 2) / nneg,
                              (null_rank - (npos + 1) / 2) / nneg)
        identical &= (p_rank == p_auc)
    q5[a] = {"max|AUC_direct - AUC_from_midrank|": float(worst),
             "all_patch_sizes_equal_npos": bool(np.all(sizes == npos)),
             "permutation_p_identical": bool(identical),
             "n_pos": npos, "n_neg": nneg}
    print(f"  {a:26s} max|dAUC| = {worst:.3e}   pool sizes all == n_pos: "
          f"{bool(np.all(sizes == npos))}   permutation p identical: {identical}")
out["q5"] = q5

# ---------------- Q6: prevalence and AUC-PR comparability ---------------------------
print("\n=== Q6  null distribution of the step AP estimator, per arm ===")
rng3 = np.random.default_rng(9)
q6 = {}
for a in sorted(FROZEN):
    ncand, npos = FROZEN[a]["n_candidates"], FROZEN[a]["n_positive"]
    prev = npos / ncand
    aps = []
    for _ in range(4000):
        v = rng3.random(ncand)
        pos = np.zeros(ncand, bool); pos[rng3.choice(ncand, npos, replace=False)] = True
        aps.append(metrics.auc_pr(v, pos))
    aps = np.array(aps)
    q6[a] = {"prevalence": round(prev, 5), "null_AP_mean": round(float(aps.mean()), 5),
             "null_AP_p95": round(float(np.quantile(aps, 0.95)), 5),
             "bias_over_prevalence": round(float(aps.mean() / prev), 3),
             "p95_over_prevalence": round(float(np.quantile(aps, 0.95) / prev), 3)}
    print(f"  {a:26s} prev {prev:.4f}  null AP mean {aps.mean():.4f} "
          f"({aps.mean()/prev:.2f}x prev)  null AP p95 {np.quantile(aps,0.95):.4f} "
          f"({np.quantile(aps,0.95)/prev:.2f}x prev)")
out["q6_ap"] = q6

json.dump(out, open(sys.argv[1] if len(sys.argv) > 1 else "/tmp/q2356.json", "w"), indent=1)
```

### A.6 `q3_fisher_size.py` — the gate the combined negative-class test never had

```text
"""The one gate the repository never ran: the measured type-I rate of the TESTED form of
negative class (b) -- Fisher and Stouffer over the three confirmatory arms -- under the same
site-uninformative field the matched-patch gate uses."""
import json, sys
import numpy as np
from scipy.stats import chi2, norm, rankdata

from allo.inputs import apo_input
from allo.scoring.harness import _positives
from allo.scoring.nulls import evaluation_graph, field_factor

ARMS = ["kras_g12c_corrected", "bcr_abl1_corrected", "cardiac_myosin_corrected"]
FROZEN = json.load(open("docs/benchmark/evaluation/frozen.json"))["targets"]
N, SEED = 20000, 606060

S = {}
for a in ARMS:
    g = evaluation_graph(apo_input(a))
    labels, _ = _positives(a)
    at = {r: i for i, r in enumerate(g.candidates)}
    L = [np.array([at[r] for r in q["lining"]]) for q in FROZEN[a]["decoys"]["pockets"].values()]
    S[a] = dict(mask=np.array([r in set(labels) for r in g.candidates], bool),
                coords=g.ca_coord[g.index(g.candidates)], linings=L)

for lam in (4.0, 8.0, 12.0, 20.0):
    P = {}
    for a in ARMS:
        s = S[a]
        f = field_factor(s["coords"], lam)
        rng = np.random.default_rng(SEED + int(lam) + 100 * ARMS.index(a))
        ps = []
        while len(ps) < N:
            b = min(250, N - len(ps))
            ranks = rankdata(f @ rng.standard_normal((f.shape[0], b)), axis=0, method="average")
            obs = ranks[s["mask"]].mean(0)
            dec = np.array([ranks[ix].mean(0) for ix in s["linings"]])   # (n_dec, b)
            ps.extend(((1 + (dec >= obs).sum(0)) / (1 + len(s["linings"]))).tolist())
        P[a] = np.array(ps)
    mat = np.column_stack([P[a] for a in ARMS])
    fis = chi2.sf(-2 * np.log(mat).sum(1), 6)
    sto = norm.sf(norm.isf(mat).sum(1) / np.sqrt(3))
    per = {a: round(float((P[a] <= 0.05).mean()), 4) for a in ARMS}
    zz = norm.isf(np.clip(mat, 1e-6, 1 - 1e-6)); rho = np.corrcoef(zz.T)
    print(f"  P(Fisher <= 0.015373) = {float((fis <= 0.015373).mean()):.5f}   P(Stouffer <= 0.009042) = {float((sto <= 0.009042).mean()):.5f}")
    print(f"lambda {lam:5}: per-arm size@0.05 {per}  Fisher size {float((fis<=0.05).mean()):.4f}  "
          f"Stouffer size {float((sto<=0.05).mean()):.4f}  "
          f"z-correlations {rho[0,1]:.3f}/{rho[0,2]:.3f}/{rho[1,2]:.3f}")
```

### A.7 `q4_familypower.py` — family-level power

```text
"""Q4: family-level power of Holm over the three confirmatory arms, which the repository
reports only per arm.  Same data-generating model as `calibration.detectable_effect`:
a site-uninformative field with unit marginal variance plus a constant shift on the labels."""
import json, sys
import numpy as np
from scipy.stats import rankdata

from allo.inputs import apo_input
from allo.scoring.harness import _positives, calibrated_p, holm
from allo.scoring.nulls import evaluation_graph, field_factor, matched_patches

ARMS = ["kras_g12c_corrected", "bcr_abl1_corrected", "cardiac_myosin_corrected"]
FROZEN = json.load(open("docs/benchmark/evaluation/frozen.json"))["targets"]
N = 4000
SEED = 5150


def setup(t):
    g = evaluation_graph(apo_input(t))
    labels, _ = _positives(t)
    mask = np.array([r in set(labels) for r in g.candidates], dtype=bool)
    patches, _ = matched_patches(g, labels, n_patches=9999, tolerance=0.10, seed=0)
    m = patches[:, g.index(g.candidates)].astype(np.float32)
    return dict(mask=mask, members=m, sizes=m.sum(1),
                coords=g.ca_coord[g.index(g.candidates)],
                ratio=float(FROZEN[t]["matched_patch"]["size_ratio"]),
                npos=int(mask.sum()), nneg=int(len(mask) - mask.sum()))


S = {a: setup(a) for a in ARMS}
for lam in (8.0, 12.0):
    F = {a: field_factor(S[a]["coords"], lam) for a in ARMS}
    print(f"\n=== lambda = {lam} A, {N} replicates ===")
    print(f"{'shift':>6} " + " ".join(f"{a.split('_')[0]:>10}" for a in ARMS) +
          f" {'medAUC':>7} {'all3':>7} {'>=1':>7}")
    for shift in (0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.4):
        P, AUC = {}, {}
        for a in ARMS:
            s, f = S[a], F[a]
            rng = np.random.default_rng(SEED + ARMS.index(a))
            ps, aucs = [], []
            done = 0
            while done < N:
                b = min(250, N - done)
                fields = f @ rng.standard_normal((f.shape[0], b)) + shift * s["mask"][:, None]
                ranks = rankdata(fields, axis=0, method="average").astype(np.float32)
                obs = ranks[s["mask"]].mean(0)
                null = (s["members"] @ ranks) / s["sizes"][:, None]
                raw = (1 + (null >= obs).sum(0)) / (1 + null.shape[0])
                ps.extend([calibrated_p(float(x), s["ratio"]) for x in raw])
                aucs.extend(((ranks[s["mask"]].sum(0) - s["npos"] * (s["npos"] + 1) / 2)
                             / (s["npos"] * s["nneg"])).tolist())
                done += b
            P[a] = np.array(ps); AUC[a] = float(np.median(aucs))
        all3 = one = 0
        for i in range(N):
            v = holm({a: float(P[a][i]) for a in ARMS}, alpha=0.05)
            r = [d["reject"] for d in v.values()]
            all3 += all(r); one += any(r)
        marg = " ".join(f"{float((P[a] <= 0.05).mean()):>10.3f}" for a in ARMS)
        print(f"{shift:>6.2f} {marg} {np.median(list(AUC.values())):>7.3f} "
              f"{all3/N:>7.3f} {one/N:>7.3f}")
```

### A.8 `q6_decoys.py` and `q_cavity_v3.py` — coverage cost and the v3 reference

```text
"""Q6: what poor site coverage actually costs, endpoint by endpoint."""
import json, sys
import numpy as np
from allo.inputs import apo_input
from allo.scoring.decoys import classify, detect_pockets
from allo.scoring.harness import _positives, protocol
from allo.scoring.nulls import evaluation_graph

FROZEN = json.load(open("docs/benchmark/evaluation/frozen.json"))["targets"]
S = protocol()["decoys"]
ARMS = ["kras_g12c_corrected", "bcr_abl1_corrected", "cardiac_myosin_corrected",
        "ns5b", "ptp1b", "mkp5", "hiv_rt"]
print(f"{'arm':<26} {'npos':>4} {'site_cov':>8} {'in_any_pocket':>13} {'in_no_pocket':>12} "
      f"{'n_decoy':>7} {'decoy_lining_residues':>21} {'floor':>8}")
rows = {}
for a in ARMS:
    apo = apo_input(a)
    g = evaluation_graph(apo)
    labels, _ = _positives(a)
    pockets = detect_pockets(apo, **{k: float(v) for k, v in S["detector_settings"].items()})
    ca = {r: g.ca_coord[g.position[r]] for r in g.order}
    rec = classify(pockets, labels=labels, candidates=g.candidates, ca_coord=ca,
                   halo_angstrom=float(S["halo_angstrom"]))
    lined = set()
    for name, q in pockets.items():
        lined |= set(q["lining"]) & set(g.candidates)
    in_any = len(set(labels) & lined)
    dec_res = set()
    for q in rec["decoys"].values():
        dec_res |= set(q["lining"])
    rows[a] = {"n_positive": len(labels),
               "site_pocket_label_coverage": rec["site_pocket"]["label_coverage"],
               "labels_in_any_detected_pocket": in_any,
               "labels_in_no_detected_pocket": len(labels) - in_any,
               "n_decoys": len(rec["decoys"]),
               "decoy_lining_residues": len(dec_res),
               "decoy_lining_fraction_of_candidates": round(len(dec_res) / len(g.candidates), 4),
               "minimum_attainable_p": rec["minimum_attainable_p"],
               "n_excluded_by_overlap": len(rec["excluded_by_halo"])}
    r = rows[a]
    print(f"{a:<26} {r['n_positive']:>4} {r['site_pocket_label_coverage']:>8} "
          f"{in_any:>13} {r['labels_in_no_detected_pocket']:>12} {r['n_decoys']:>7} "
          f"{r['decoy_lining_residues']:>21} {r['minimum_attainable_p']:>8}")
json.dump(rows, open(sys.argv[1] if len(sys.argv) > 1 else "/tmp/q6d.json", "w"), indent=1)
```

```text
"""The pre-declared family-2 reference under the v3 detector, and the decoy lining sizes."""
import json, sys
import numpy as np
from allo.inputs import apo_input
from allo.scoring.decoys import cavity_volume_score, detect_pockets
from allo.scoring.harness import _positives, holm, protocol, score_arm
from allo.scoring.nulls import evaluation_graph

FROZEN = json.load(open("docs/benchmark/evaluation/frozen.json"))["targets"]
S = protocol()
ARMS = ["kras_g12c_corrected", "bcr_abl1_corrected", "cardiac_myosin_corrected"]
ps, out = {}, {}
for a in ARMS:
    apo = apo_input(a)
    g = evaluation_graph(apo)
    pockets = detect_pockets(apo, **{k: float(v) for k, v in S["decoys"]["detector_settings"].items()})
    rec = score_arm(a, cavity_volume_score(pockets, g.candidates), method="cavity_volume")
    mp = rec["nulls"]["matched_patch"]
    ps[a] = mp["p_calibrated"]
    out[a] = {"auc_roc": rec["endpoints"]["auc_roc"], "auc_pr": rec["endpoints"]["auc_pr"],
              "recall_at_5": rec["endpoints"]["recall_at_5"], "hits_at_5": rec["endpoints"]["hits_at_5"],
              "dcc": rec["endpoints"]["dcc_angstrom"], "chance_dcc": rec["chance"]["dcc_angstrom"],
              "p_raw": mp["p"], "p_calibrated": mp["p_calibrated"],
              "decoy_p": rec["nulls"]["decoy_pockets"]["p"],
              "site_pocket_rank": rec["nulls"]["decoy_pockets"]["site_pocket_rank"],
              "n_pockets_ranked": rec["nulls"]["decoy_pockets"]["n_pockets_ranked"],
              "auc_vs_decoy_linings": rec["endpoints"]["auc_roc_vs_decoy_linings"]}
    print(f"{a:26s} AUC {out[a]['auc_roc']:.4f}  AP {out[a]['auc_pr']:.4f}  recall@5 "
          f"{out[a]['recall_at_5']}  DCC {out[a]['dcc']} (chance {out[a]['chance_dcc']})  "
          f"p_cal {out[a]['p_calibrated']}  decoy p {out[a]['decoy_p']}  "
          f"site pocket rank {out[a]['site_pocket_rank']}/{out[a]['n_pockets_ranked']}")
print("\nfamily 1, Holm over three, for the pre-declared reference itself:")
for name, v in holm(ps, alpha=0.05).items():
    print(f"  {name:26s} p_cal {v['p']:.6f}  threshold {v['threshold']}  reject {v['reject']}")

print("\ndecoy lining size against the label-set size (README section 5.3 disclosure):")
for a in sorted(FROZEN):
    labels, _ = _positives(a)
    sizes = np.array([len(q["lining"]) for q in FROZEN[a]["decoys"]["pockets"].values()])
    print(f"  {a:26s} n_pos {len(labels):>3}  decoy lining median {np.median(sizes):>5.1f}  "
          f"ratio {np.median(sizes)/len(labels):.3f}  min {sizes.min()} max {sizes.max()}")

print("\nv2 -> v3 calibration drift check (README section 0.1 claims 13 of 15 unchanged):")
old = json.load(open("experiments/2026-08-25-null-calibration/metrics.json"))["gate"]
new = json.load(open("experiments/2026-09-02-null-recalibration/metrics.json"))["gate"]
moved = []
for a in sorted(set(old) & set(new)):
    if old[a]["size_ratio"] != new[a]["size_ratio"] or old[a]["alpha_star"] != new[a]["alpha_star"]:
        moved.append((a, old[a]["size_ratio"], new[a]["size_ratio"]))
print(f"  arms in both runs: {len(set(old) & set(new))}; only in v3: {sorted(set(new) - set(old))}")
print(f"  arms whose size_ratio or alpha_star moved: {moved}")
json.dump(out, open(sys.argv[1] if len(sys.argv) > 1 else "/tmp/cav.json", "w"), indent=1)
```

---

## Appendix B — references

* Brown, M. B. (1975). A method for combining non-independent, one-sided tests of
  significance. *Biometrics* 31, 987–992. doi:10.2307/2529826
* Kost, J. T. & McDermott, M. P. (2002). Combining dependent p-values.
  *Statistics & Probability Letters* 60, 183–190. doi:10.1016/S0167-7152(02)00310-3
* Holm, S. (1979). A simple sequentially rejective multiple test procedure.
  *Scandinavian Journal of Statistics* 6, 65–70.
* Guerra, V. et al. pyKVFinder. doi:10.1186/s12859-021-04519-4
* Xiao, S. et al. APOP. doi:10.1093/bioinformatics/btad275
* Meller, A. et al. PocketMiner. doi:10.1038/s41467-023-36699-3
