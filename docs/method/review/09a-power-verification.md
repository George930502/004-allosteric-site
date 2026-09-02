# Independent verification of the power claim in file 09

**Scope:** reproduces or refutes one number — the claim in `09-data-analysis.md` §8 and its
pipeline item 5 that "our frozen protocol needs AUC 0.76 to 0.96 for 80 % power" while "the
best confound-free number in this field is 0.59". It covers the confirmatory endpoint, the
two reported endpoints beside it, the Holm family, and whether the two numbers are on one
scale. It deliberately excludes every other number in file 09, which is not re-checked here.
**Sibling files:** `09-data-analysis.md` (the file under test), `00-conventions.md` §6 (the
four numbers a method must clear).
**Retrieved:** 2026-08-25.

---

## Verdict — PARTLY CONFIRMED

**The arithmetic is right and the conclusion drawn from it is wrong.** An independent
simulation, written from the protocol text rather than from `allo.scoring.calibration`,
reproduces the published minimum-detectable-effect table to within ±0.016 AUC in every one of
40 cells (median absolute difference 0.004, Monte-Carlo s.e. of an interpolated cell 0.004).
The band **0.76–0.96 is real**. But three things break the inference. First, the band is a
property of the _assumed smoothness of the method's own score field_, not of the benchmark:
the experiment swept correlation lengths 4–20 Å and never tried the short-correlation limit,
where the same simulation gives **0.669–0.760**. Second, the "0.59" is a **mean over 72–96
targets of a distance-stratified AUC on a different candidate pool with different labels**,
and our band is a **per-arm threshold on plain AUC over our own candidate set** — two
different estimands, two different sampling units, not comparable. Third, and decisively, the
question is already settled by measurement on our own arms: `cavity_volume`, a zero-parameter
geometric baseline, scores plain AUC **0.830 / 0.795 / 0.977** on the three confirmatory arms
and rejects all three at Holm-corrected `p_calibrated` 0.0073 / 0.0003 / 0.0001. A benchmark
on which a trivial baseline already rejects on 3 of 3 arms is not a benchmark on which
"a genuinely good method will fail to reject". **Phase 2 does not need replanning. It needs
one line added to the report template** — see the pipeline section. The part of the alarm
that survives is narrower and still worth carrying: the _claim threshold is beating
`cavity_volume` at 0.80–0.98 plain AUC_, not clearing 0.59.

---

## 1. What was claimed, and what produced it

File 09 §8 quotes the power line from `experiments/2026-08-25-null-calibration/metrics.json`
via `10_own_experiments.py`. That script does no computation: it walks the `power` block,
selects every path whose key matches `auc`, and prints min / median / max. It is a correct
read of the file. The number therefore comes from
`allo.scoring.calibration.detectable_effect`, and that is what is verified below.

Two things the source script assumed without checking, both material:

- **That the 60 cells span the reachable range.** They span 5 arms × 4 correlation lengths ×
  3 Holm levels. Correlation length is a property of the _method_, not of the benchmark, and
  the grid starts at 4 Å. Nothing below that was measured.
- **That AUC is the quantity to compare.** `auc_roc` in the `power` block is a _reported
  consequence_ of the simulated shift under one data-generating model, not the tested
  statistic and not an input.

---

## 2. The protocol, read from source

From `docs/benchmark/evaluation/manifest.yaml` via `allo.scoring.harness.protocol()`, from
`harness.score_arm`, and from `docs/benchmark/primary/README.md` §3, which already publishes
every count below.

| Setting                  | Value                                                                                   |
| ------------------------ | --------------------------------------------------------------------------------------- |
| Confirmatory endpoint    | `mean_rank` — mean midrank of the scoreable label set (ADR 0022)                        |
| Null                     | matched-patch permutation, tolerance 0.10, 9999 replicates, upper tail, plus-one        |
| Calibration              | per-arm probit rescale `size_ratio`, max over 4 λ and over all 3 Holm levels (ADR 0025) |
| α, correction, sidedness | 0.05, Holm step-down, one-sided upper                                                   |
| Confirmatory family      | the three `corrected` arms                                                              |
| Power simulation         | 300 field draws, bisection to 80 %, at the _calibrated_ threshold                       |

| Arm                        | m (scoreable labels) | n (candidates) | prevalence | `size_ratio` | raw p threshold at α / (α/3) |
| -------------------------- | -------------------: | -------------: | ---------: | -----------: | ---------------------------- |
| `kras_g12c_corrected`      |                   16 |            148 |     10.8 % |       1.0827 | 0.0375 / 0.0106              |
| `bcr_abl1_corrected`       |                   18 |            261 |      6.9 % |       1.0970 | 0.0356 / 0.0098              |
| `cardiac_myosin_corrected` |                   12 |            743 |      1.6 % |       1.0000 | 0.0500 / 0.0167              |

---

## 3. The algebra, verified: the endpoint _is_ AUC, and the test is a threshold on it

The README asserts that mean midrank is "a strictly increasing function of AUC-ROC" under a
size-preserving null. It is stronger than that — the relation is **exact and affine**:

```
U  = Σ_{i∈P} R_i − m(m+1)/2      (Mann-Whitney)
AUC = U / (m (n−m))
⇒   R̄ = AUC · (n − m) + (m + 1)/2          and       AUC = (R̄ − (m+1)/2) / (n − m)
```

with `m` the label-set size, `n` the candidate count, `R̄` the mean midrank. Slope `(n−m) > 0`,
so strictly increasing. Verified numerically against `allo.scoring.metrics.auc_roc` and
`rank_vector` to floating-point equality, including under heavy ties (midranks make it exact).

**The consequence the README does not draw.** Every matched patch holds exactly `m` residues
(`score_arm` asserts it), so the _same_ affine map converts every null replicate. The
confirmatory decision is therefore, exactly:

> reject iff the score's plain AUC-ROC exceeds the (1 − α\*) quantile of the AUCs that the
> 9999 matched patches achieve **under that same score vector**.

The critical value is data-dependent — it is a property of the method's own score field, not
a constant — and it is computable at scoring time with no simulation and no correlation
length. Measured under the calibration field, at α:

| Arm                        | s.d. of null AUC → |   iid |   λ=4 |   λ=8 |  λ=12 |  λ=20 |
| -------------------------- | ------------------ | ----: | ----: | ----: | ----: | ----: |
| `kras_g12c_corrected`      | critical AUC       | 0.627 | 0.679 | 0.728 | 0.753 | 0.778 |
| `bcr_abl1_corrected`       | critical AUC       | 0.625 | 0.680 | 0.738 | 0.767 | 0.795 |
| `cardiac_myosin_corrected` | critical AUC       | 0.637 | 0.687 | 0.748 | 0.783 | 0.815 |

The iid column is a closed-form check: under a white-noise score the null AUC has s.d.
`√((n+1)/(12 m (n−m)))` = 0.0767 / 0.0707 / 0.0841, and `0.5 + z(α*)·s.d.` reproduces the
simulated column to three decimals. **12–18 positives is what sets this**, not the candidate
count.

---

## 4. Reproduction of the published table

Own simulation, 2000 field draws per cell (the experiment used 300), common random numbers
across shifts, power interpolated on a 13-point shift grid. First, the implementation is
validated against a number I did not compute: replaying the repo's own draw order and seed on
`kras_g12c_corrected` at λ = 8 returns a type-I rate of **0.0550**, against the 0.055 printed
in the evaluation README §6.1. Twelve independent seeds give 0.0453 ± 0.0053, so the published
cell is a one-seed estimate with real Monte-Carlo width — worth knowing, and not the subject
here.

MDE in median achieved AUC-ROC. `mine v published (difference)`:

**At α**

| Arm                        | λ=4                    | λ=8                    | λ=12                   | λ=20                   |
| -------------------------- | ---------------------- | ---------------------- | ---------------------- | ---------------------- |
| `kras_g12c_corrected`      | 0.785 v 0.786 (−0.001) | 0.842 v 0.842 (0.000)  | 0.870 v 0.868 (+0.002) | 0.893 v 0.895 (−0.002) |
| `bcr_abl1_corrected`       | 0.762 v 0.762 (0.000)  | 0.841 v 0.850 (−0.009) | 0.876 v 0.880 (−0.004) | 0.903 v 0.908 (−0.005) |
| `cardiac_myosin_corrected` | 0.772 v 0.769 (+0.003) | 0.853 v 0.850 (+0.003) | 0.893 v 0.897 (−0.004) | 0.925 v 0.936 (−0.011) |
| `kras_g12c_mandated`       | 0.772 v 0.776 (−0.004) | 0.836 v 0.841 (−0.005) | 0.865 v 0.860 (+0.005) | 0.889 v 0.888 (+0.001) |
| `bcr_abl1_mandated`        | 0.757 v 0.773 (−0.016) | 0.848 v 0.835 (+0.013) | 0.883 v 0.867 (+0.016) | 0.911 v 0.913 (−0.002) |

**At α/3**

| Arm                        | λ=4                    | λ=8                    | λ=12                   | λ=20                   |
| -------------------------- | ---------------------- | ---------------------- | ---------------------- | ---------------------- |
| `kras_g12c_corrected`      | 0.822 v 0.827 (−0.005) | 0.874 v 0.881 (−0.007) | 0.898 v 0.891 (+0.007) | 0.918 v 0.914 (+0.004) |
| `bcr_abl1_corrected`       | 0.802 v 0.799 (+0.003) | 0.872 v 0.883 (−0.011) | 0.903 v 0.911 (−0.008) | 0.925 v 0.933 (−0.008) |
| `cardiac_myosin_corrected` | 0.815 v 0.810 (+0.005) | 0.890 v 0.892 (−0.002) | 0.927 v 0.931 (−0.004) | 0.952 v 0.961 (−0.009) |
| `kras_g12c_mandated`       | 0.811 v 0.813 (−0.002) | 0.870 v 0.871 (−0.001) | 0.893 v 0.891 (+0.002) | 0.914 v 0.908 (+0.006) |
| `bcr_abl1_mandated`        | 0.794 v 0.804 (−0.010) | 0.877 v 0.875 (+0.002) | 0.909 v 0.900 (+0.009) | 0.933 v 0.931 (+0.002) |

Over the 40 cells: min 0.757, median 0.875, max 0.952, against the published 0.762 / 0.879 /
0.961. **The published band is reproduced.** Every difference is inside 2.5 s.e. of the
interpolation (local slope dPower/dAUC is 2.2–4.5, so s.e.(MDE) ≈ 0.004).

## 4.1 The lower edge is not a floor

The experiment's grid starts at λ = 4 Å. Adding the λ → 0 limit — a score with no spatial
autocorrelation, which is the most favourable score field the test can be handed:

| Arm                        | MDE at α | MDE at α/3 |
| -------------------------- | -------: | ---------: |
| `kras_g12c_corrected`      |    0.717 |      0.760 |
| `bcr_abl1_corrected`       |    0.687 |      0.722 |
| `cardiac_myosin_corrected` |    0.708 |      0.746 |
| `kras_g12c_mandated`       |    0.711 |      0.753 |
| `bcr_abl1_mandated`        |    0.669 |      0.703 |

**Per-arm MDE, correctly stated: AUC 0.67 to 0.95, and which end an arm sits at is chosen by
the method, not by the benchmark.** The 0.76 edge is what a method whose score varies on a
4 Å scale needs. A residue-level score with little spatial smoothing needs 0.67–0.76.

The mechanism is in §3: a smooth score inflates the observed AUC and the null's AUC by the
same amount, so smoothness buys no evidence. AUC alone is not a sufficient statistic for the
decision, which is why the same AUC means different things on different score fields.

---

## 5. The Holm family

Paired draws — one independent field per arm per replicate, common shift, `p_calibrated` per
arm, step-down Holm at α = 0.05 across the three `corrected` arms.

|   λ | d for P(≥1 arm rejects) = 0.80 | AUC there | d for P(all 3 reject) = 0.80 | AUC there |
| --: | -----------------------------: | --------: | ---------------------------: | --------: |
| iid |                           0.58 | **0.663** |                         0.95 | **0.752** |
|   4 |                           0.77 |     0.717 |                         1.28 |     0.830 |
|   8 |                           0.89 |     0.761 |                         1.63 |     0.904 |
|  12 |                           0.91 |     0.782 |                         1.77 |     0.935 |
|  20 |                           0.87 |     0.800 |                         1.82 |     0.963 |

Two readings, and the report must not confuse them. Under §8 of the evaluation README a
Fisher or Stouffer combination licenses only the **intersection-null** claim — _at least one
arm has signal_ — and that reading needs **AUC 0.66–0.80**. A per-arm claim on all three
needs 0.75–0.96. **File 09 quotes the harder of the two without saying which claim it
supports.**

Measured size at shift 0 across all 15 arm × λ cells: 0.036–0.050 at α (nominal 0.05, exact
central 95 % band at n = 2000 is [0.041, 0.060]). The calibrated test is at or slightly below
nominal everywhere, as ADR 0025 intends.

---

## 6. The other two endpoints (step 4)

The frozen protocol _tests_ one endpoint and _prints_ two more. Both were simulated under the
identical DGM. AUC-PR was given the same matched-patch permutation null (1999 replicates) at
the **nominal** threshold, with no size calibration — which flatters it. hits@5 was tested
against its exact hypergeometric chance line at the same level.

MDE expressed as the shift each endpoint needs, at α:

| Arm                        |   λ | mean midrank | AUC-PR | hits@5 | hits needed | AUC-PR at the MDE | prevalence |
| -------------------------- | --: | -----------: | -----: | -----: | ----------: | ----------------: | ---------: |
| `kras_g12c_corrected`      |   4 |         1.06 |   1.08 |   1.55 |      3 of 5 |             0.423 |      0.108 |
| `kras_g12c_corrected`      |  20 |         1.17 |   1.13 |   1.41 |      3 of 5 |             0.593 |      0.108 |
| `bcr_abl1_corrected`       |   4 |         0.96 |   1.01 |   1.33 |      2 of 5 |             0.255 |      0.069 |
| `bcr_abl1_corrected`       |  20 |         1.33 |   1.31 |   1.40 |      2 of 5 |             0.530 |      0.069 |
| `cardiac_myosin_corrected` |   4 |         1.00 |   1.19 |   1.97 |      2 of 5 |             0.082 |      0.016 |
| `cardiac_myosin_corrected` |  20 |         1.54 |   1.57 |   2.07 |      2 of 5 |             0.302 |      0.016 |

**No endpoint rescues the other.** AUC-PR ties the frozen endpoint within ±0.05 in d on the
two higher-prevalence arms and is **worse by 0.19–0.25 d on the 1.6 %-prevalence myosin arm**,
which is exactly the direction the README predicted from McDermott et al. (arXiv:2401.06091)
and the PocketMiner dispersion. Since it is quoted uncalibrated while the frozen endpoint is
tightened, its true gap is larger than shown. **hits@5 is decisively the worst**: it needs
0.3–0.9 more d everywhere, and on myosin its measured size at nominal α is 0.002–0.006,
because the discreteness of a 5-element list against 12 labels in 743 candidates leaves almost
no attainable rejection region. Choosing the mean midrank as the confirmatory statistic was
the right call and this verification supports it.

---

## 7. Are the two numbers on the same scale? No (step 5)

They are not, on five independent axes. `stratified_auc` is
`allosteric-benchmark/scripts/partial_auc.py`; the pool is `methods/common.py::distal_nonanchor_mask`.

|                        | our band                                                                    | the "0.59"                                                           |
| ---------------------- | --------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| **estimand**           | plain AUC-ROC                                                               | AUC restricted to (pos, neg) pairs with \|Δd to active site\| ≤ 2 Å  |
| **candidate pool**     | every modelled residue of the frozen chain minus the active site (ADR 0011) | residues ≥ 8 Å from the nearest active-site residue                  |
| **labels**             | our frozen scoreable label sets, `m` = 12–18                                | expert-curated annotation, and see file 09 §2.4 on label conventions |
| **sampling unit**      | one arm; a threshold each arm must individually clear                       | the **mean over 72–96 targets**                                      |
| **role of the number** | a critical value                                                            | a point estimate of a population mean                                |

Comparing a cross-target mean to a per-arm critical value is a category error, and the size of
the error is measurable. On the same 72 curated targets the per-target distribution behind the
0.59 has **s.d. 0.224**, with **23.6 % of targets at or above 0.76** and 8.3 % at or above
0.88 (`ctrl_random` for scale: s.d. 0.118, 2.8 % above 0.76). A method with that per-target
distribution has roughly a one-in-four chance of clearing 0.76 on any single arm — not the
"will fail to reject" the mean implies.

Two smaller corrections to the same sentence. **0.59 is not the best confound-free number in
the teammate's repository**: `gnn/RESULTS.md` records distance-stratified AUC **0.622 and
0.630** on 96 curated targets, which file 09 §9 itself reports. And the sign of the geometric
confound flips between label conventions (file 09 §2.4), so a stratified number from curated
labels does not transfer to our labels at all.

**The correct comparison, if one is wanted**, is one of two things, and neither is available
from `allosteric-benchmark`: either (a) recompute our critical AUC under the teammate's
stratified estimand and pool, which changes the protocol and is frozen shut; or (b) run the
teammate's _methods_ through `allo.scoring.score_arm` on our three arms and read the plain AUC
they achieve there. (b) is cheap, legal under C1/C2, and is the only apples-to-apples route.

---

## 8. The measurement that settles it

Both required controls have already been run through `score_arm` on all five primary arms
(evaluation README §13, `docs/ROADMAP.md` §1.6). They are on **exactly** our scale:

| baseline                       | plain AUC on the three confirmatory arms | Holm `p_calibrated`      | verdict           |
| ------------------------------ | ---------------------------------------- | ------------------------ | ----------------- |
| `cavity_volume`                | **0.830 / 0.795 / 0.977**                | 0.0073 / 0.0003 / 0.0001 | rejects on 3 of 3 |
| `distance_from_source_negated` | 0.588 / 0.215 / 0.335                    | 0.286 / 0.920 / 0.656    | rejects on 0 of 3 |

Every `cavity_volume` value clears its arm's λ = 8 critical AUC (0.728 / 0.738 / 0.748) and
each rejection lands where the simulation says it should. The framework is empirically
validated by two real methods, and the alarm's premise is false: this benchmark is not one on
which nothing can reject.

Note the coincidence and do not read it as agreement — the negative control's plain AUC on
`kras_g12c_corrected` is **0.588**. A method that scored 0.59 _on our scale, on our arms_
would indeed not reject. It would also be at the level of a control that the protocol requires
to fail. That is the residual grain of truth in the alarm, and it is a statement about a bad
method, not about an underpowered benchmark.

---

## What this changes for our pipeline

1. **Phase 2 proceeds as written.** The premise "a genuinely good method will fail to reject
   on our own benchmark" is refuted by a measurement already in the repository:
   `cavity_volume` rejects on 3 of 3 confirmatory arms. No replan is warranted.
2. **Correct the sensitivity band before the report quotes it.** The honest per-arm statement
   is **AUC 0.67–0.95 at 80 % power**, with the position inside that band set by the
   correlation length of the method's own score field. Withdraw the "0.76–0.96" phrasing from
   file 09 §8 and pipeline item 5; it is the λ ≥ 4 Å sub-band. The evaluation README §7.1 is
   frozen and must not change — this is a correction to the _review_, not to the protocol.
3. **Report the critical AUC beside every p-value (Phase 2, scoring).** §3 shows it is one
   quantile of the null-statistic vector `score_arm` already computes, needs no simulation and
   no correlation length, and turns an abstract band into the exact number that arm's score had
   to beat. This is a reporting addition, not a protocol change.
4. **Say which claim the sensitivity supports.** "At least one arm has signal" needs AUC
   0.66–0.80; "all three arms reject" needs 0.75–0.96. File 09 quotes the second and reads it
   as if it were the first.
5. **The bar stays where `00-conventions.md` §6 puts it: beating `cavity_volume`.** On our
   scale that is plain AUC 0.80–0.98 with recall@5 above 0.00 and a DCC inside its chance
   line — a harder target than clearing the null, and the one that matters.
6. **Never compare a cross-target mean against a per-arm critical value again.** The rule
   already exists (`00-conventions.md` §2, "numbers must be comparable before they are
   compared"); this is the case that shows what it costs. If a comparison to
   `allosteric-benchmark` is wanted, run its methods through `score_arm` on our arms.
7. **The confirmatory endpoint choice is confirmed, not merely inherited.** Mean midrank
   dominates AUC-PR on the low-prevalence arm and dominates hits@5 everywhere. Do not
   re-litigate it.

---

## Method

**Databases and searches:** none. Every number here is computed in-session from files on
disk or read from a committed repository document; no literature was retrieved, so the three
evidence tags of `00-conventions.md` §2 do not apply to any line above. The two DOIs mentioned
(arXiv:2401.06091, doi:10.1038/s41467-023-36699-3) are carried over from the evaluation
README's own citations for direction of agreement only and were not retrieved this session.

**Read.** `docs/method/review/09-data-analysis.md`; the session scratchpad's
`10_own_experiments.py`; `docs/benchmark/evaluation/README.md`, `manifest.yaml` and `AUDIT.md`;
`docs/benchmark/primary/README.md`; all of `src/allo/scoring/`;
`experiments/2026-08-25-null-calibration/{config.yaml,metrics.json}`; `docs/ROADMAP.md` §1.6;
`allosteric-benchmark/scripts/partial_auc.py`, `methods/common.py`,
`data/results_partial_auc.json`, `gnn/RESULTS.md`; `tests/test_no_leakage.py`.
`selection.json` and `extension-candidates.md` were not opened.

**Scripts** (session scratchpad, none written into the repository):

| script            | produces                                                                                                                                                                                                              |
| ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `v1_power_sim.py` | `power_grid.csv`, `pvectors.npz` — 5 arms × 5 λ × 13 shifts × 2000 field draws; per cell the power of all three endpoints at all three Holm levels, the achieved AUC / AUC-PR / hits@5, and the null AUC distribution |
| `v2_analyse.py`   | the reproduction table (§4), the critical-AUC table (§3), the endpoint comparison (§6), the Holm family curves (§5)                                                                                                   |
| `v3_addendum.py`  | family MDE both readings, measured size per endpoint, the mean-midrank scale, the baseline placement (§8)                                                                                                             |

The simulation reimplements ranking, the permutation p, the probit calibration, Holm, and the
power loop. It reuses only the frozen objects under test: `evaluation_graph`,
`matched_patches` (the identical cached 9999-patch pool `score_arm` uses) and the frozen label
sets. `allo.scoring.calibration.detectable_effect` was read but never called.

**Precision.** 2000 draws per cell, so a power estimate has Monte-Carlo s.e. ≤ 0.0112. The
local slope of power against AUC at the 0.80 crossing is 2.2–4.5, so an interpolated MDE has
s.e. ≈ 0.004. Every difference reported in §4 is inside 2.5 of those.

**Leakage.** No residue number, label residue, decoy lining or site identity appears in this
file. The only frozen quantities quoted are counts (`m`, `n_candidates`, prevalence) and
protocol settings, all of which `docs/benchmark/primary/README.md` §3 already publishes.
`docs/` is outside the runner scan in `tests/test_no_leakage.py`, and the scripts live in the
scratchpad, so nothing here enters the prediction path.

**Stopping rule.** Stop when the published table is reproduced or refuted cell by cell, the
two other printed endpoints have a power number, the family has a joint number, and the scale
question has an answer that names the estimand on both sides. Reached.

**What could not be reached.** Three things.

1. **The 0.59 could not be recomputed on our scale**, because doing so means running the
   teammate's methods through `score_arm` on our arms, which is Phase 2 work. §7 states the
   comparison that would be valid instead of making one that is not.
2. **The alternative is one data-generating model.** A constant shift on the label patch
   inside a stationary exponential-covariance Gaussian field. Real score fields are neither
   stationary nor Gaussian. §3's critical-AUC framing is the model-free part of this file and
   is the number to prefer where the two disagree.
3. **The published type-I cells carry one-seed Monte-Carlo width** (0.055 reproduced exactly;
   12 further seeds give 0.045 ± 0.005). The evaluation README §6.3 already discloses that
   `size_ratio` is an estimate frozen forever. This file does not reopen it and neither should
   anything else.
