# Negative class (b): the decoy-pocket test cannot work, and the reason is not the detector

**Question.** The organisers make the decoy set each team's own responsibility. The frozen
protocol discloses a power floor of 0.25 on two of three confirmatory arms. Can a better
decoy set fix it?

**Answer.** No. The floor is a symptom. The test itself has a power ceiling of
`1 - Phi(z_(1-alpha) - delta)`, so it needs a pocket-level effect of **delta >= 2.49
standard deviations** for 80 % power at any decoy count whatever. The fix is a different
statistic, not more pockets.

`CHALLENGE.md` §4.1 names this negative class as half of the success criterion, so a test
that cannot reject is a conformance problem and not only a statistical one.

---

## 1. The test, and its structural ceiling

`allo.scoring.harness` gives every detected pocket one number — the mean midrank of its
lining — and compares the site pocket against the decoys:

```
p = (1 + #{decoy_rank >= site_rank}) / (1 + n_decoys)
```

Exact, one-sided, no sampling. Two consequences follow from the form alone.

**A hard floor.** The smallest value the numerator can take is 1, so `p >= 1 / (1 + n_decoys)`.

| threshold | decoys needed before the test can reject at all |
| --- | ---: |
| alpha = 0.05 | **19** |
| alpha/2 = 0.025 | **39** |
| alpha/3 = 0.0167 | **59** |

**A ceiling that more decoys do not lift.** The statistic is *one draw per pocket*. Whatever
the lining size, all within-pocket information is discarded. As `n_decoys` grows the floor
falls, but the site must out-rank proportionally more competitors, and the power tends to

```
P(reject) -> 1 - Phi(z_(1-alpha) - delta)
```

where `delta` is the site pocket's separation from the decoy pocket score distribution, in
standard deviations. Setting that to 0.80 gives

```
delta >= z_(1-alpha) + z_0.80 = 1.645 + 0.842 = 2.487
```

**No decoy count changes this number.** A pocket-level effect of 2.5 standard deviations is
very large.

---

## 2. Simulated power at every attainable decoy count

20 000 Monte-Carlo replicates per cell. Site score drawn `N(delta, 1)`, each decoy `N(0, 1)`,
then the exact test above. Script: `data/decoy_power_sim.py`.

**At alpha = 0.05.**

| arm / detector setting | n decoys | d=0.5 | d=1.0 | d=1.5 | d=2.0 | d=3.0 | floor |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `kras_g12c_corrected` frozen | 3 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.250 |
| `kras_g12c_corrected` loosest tried | 18 | **0.000** | **0.000** | **0.000** | **0.000** | **0.000** | 0.053 |
| `bcr_abl1_corrected` frozen | 9 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.100 |
| `bcr_abl1_corrected` loosest tried | 31 | 0.076 | 0.173 | 0.313 | 0.483 | 0.802 | 0.031 |
| `cardiac_myosin_corrected` frozen | 41 | 0.115 | 0.239 | 0.403 | 0.591 | 0.875 | 0.024 |
| `cardiac_myosin_corrected` loosest tried | 84 | 0.114 | 0.240 | 0.422 | 0.605 | 0.894 | 0.012 |

**At Holm's tightest step, alpha/3.** Every arm reads 0.000 except cardiac myosin at the two
loosest settings, which reaches 0.19 at d = 1.5.

**Decoys needed for 80 % power at alpha = 0.05:** d = 3.0 needs 19; d = 2.5 needs **289**;
d <= 2.0 is unreachable at 400.

The Gaussian model is **optimistic**. Real pocket linings differ in size, so their mean
midranks are heteroscedastic, and lining residues are spatially autocorrelated. Both widen
the decoy distribution relative to the model.

---

## 3. Can a detector setting reach 19 decoys? Measured

Nine pyKVFinder settings on the five primary arms. `n_decoys` and, in brackets, the number of
distinct decoy-lining residues.

| setting | kras mand. | kras corr. | abl1 mand. | abl1 corr. | myosin |
| --- | ---: | ---: | ---: | ---: | ---: |
| **frozen** (defaults) | 3 [23] | **3 [25]** | 24 [197] | **9 [73]** | **41 [291]** |
| `volume_cutoff 1.0` | 4 [29] | 5 [26] | 27 [201] | 16 [94] | 52 [318] |
| `probe_out 8.0` | 5 [36] | 3 [29] | 11 [138] | 15 [129] | 42 [405] |
| `removal_distance 1.2` | 6 [41] | 7 [41] | 30 [237] | 22 [144] | 71 [458] |
| `probe_out 8, rd 1.2, vol 1` | 13 [76] | **18 [64]** | 41 [222] | **31 [198]** | **84 [464]** |

**KRAS never reaches 19.** Its best is 18, a floor of 0.0526, still above alpha. A
169-residue protein does not carry 19 non-functional surface pockets. Negative class (b) is
therefore untestable on `kras_g12c_corrected` under this statistic, at every detector setting
tried, at every effect size. That is arithmetic about small proteins.

**One thing the sweep found that is worth having on its own merits.** Site coverage — the
fraction of label residues the detected "site pocket" actually covers — improves sharply:

| arm | frozen | loosest |
| --- | ---: | ---: |
| `kras_g12c_corrected` | 0.75 | **0.9375** |
| `bcr_abl1_corrected` | **0.6667** | **0.9444** |
| `bcr_abl1_mandated` | 0.85 | 1.00 |
| `cardiac_myosin_corrected` | 1.00 | 1.00 |

Under the frozen setting the pocket the protocol calls "the site" on `bcr_abl1_corrected`
covers **two thirds** of the label set. The published pocket-rank convention (APOP's top-3
rule) is being applied to a pocket that is only partly the site. That is a reporting defect
independent of the power question.

**Selection rule, stated so it cannot be mistaken for tuning.** If the detector settings are
re-frozen, select on `n_decoys` alone. That quantity is label-free and is a sample-size
criterion. Report site coverage as a consequence, never as the selection target — choosing a
setting because it covers more labels would shape the negative class with the answer key.

---

## 4. What to do instead

The statistic wastes the data. Each pocket contributes one number regardless of whether its
lining holds 5 residues or 40.

**Recommended: a size-matched patch-resampling null over the decoy-lining union.** Draw many
contiguous patches restricted to the union of decoy linings, matched to the observed label
patch on size, component structure, burial and compactness — the machinery
`allo.scoring.nulls` already has — and compare the observed mean midrank against that
distribution.

| | frozen pocket test | proposed decoy-patch null |
| --- | --- | --- |
| replicates | `n_decoys` (3 to 84) | as many as drawn (9999) |
| floor on p | `1/(1 + n_decoys)` | `1/(1 + B)` |
| unit | one pocket | one size-matched patch |
| uses lining size | no | yes |
| answers | "does the site out-rank the other pockets?" | "does the site out-rank a comparable patch of non-functional pocket surface?" |

Both readings are legitimate. The second is closer to the challenge's wording — "higher
scores ... compared to non-functional surface pockets" is a comparison of scores, not a rank
among pockets — and it is the only one with usable power.

**It needs the same two things the matched-patch null needed**: a type-I calibration gate on
a site-uninformative field, and a supply of decoy-lining residues large enough to draw from.
Supply, measured: `kras_g12c_corrected` has 25 decoy residues at the frozen setting against a
16-residue label set, which is too few. At the loosest setting it has 64. **The detector
change and the statistic change have to happen together or neither works.**

---

## 4a. Three constructions were tried. All three fail on the confirmatory family

Section 4 proposed a replacement. It was measured before being recommended, through the same
gate ADR 0018 applies to the matched-patch null: draw a stochastic, site-uninformative,
spatially autocorrelated field, run the test, repeat 1000 times, and read the rejection rate
against the exact central 95 % binomial band, which at 1000 draws and alpha = 0.05 is
**[0.037, 0.064]**.

| construction | what it compares | measured type-I rate | verdict |
| --- | --- | --- | --- |
| **A** current: pocket permutation | label patch against the `n_decoys` pocket-lining means | **0.000-0.032** | below the band on every arm and every correlation length — **conservative**, consistent with the floor |
| **B** residue-level | label patch against `m` residues drawn uniformly from the pooled decoy linings | **0.132-0.384** | far above the band everywhere, rising with correlation length — **anti-conservative by 3x to 8x** |
| **C** patch resampling inside the decoy union | label patch against size-matched contiguous patches drawn from decoy linings | **not computable** | no feasible draw exists on three of five arms |

**Construction B, per arm, at each correlation length.**

| arm | lambda=4 | lambda=8 | lambda=12 | lambda=20 |
| --- | ---: | ---: | ---: | ---: |
| `kras_g12c_mandated` | 0.314 | 0.354 | 0.366 | 0.383 |
| `kras_g12c_corrected` | 0.317 | 0.353 | 0.368 | **0.384** |
| `bcr_abl1_mandated` | 0.172 | 0.261 | 0.292 | 0.306 |
| `bcr_abl1_corrected` | 0.228 | 0.301 | 0.327 | 0.348 |
| `cardiac_myosin_corrected` | 0.132 | 0.219 | 0.254 | 0.295 |

**This is worse than the unmatched background null**, which `evaluation/README.md` §4.1
measures at 0.10-0.32 and calls unusable. Under a score field that knows nothing about the
site, construction B rejects **38 %** of the time on KRAS.

The mechanism is the same one §4.1 names. The observed label set is one contiguous blob. A
uniform draw of `m` residues from a pool spread over 3 to 41 discrete pockets scatters them,
so the null draws have far less variance than the observation and the upper tail is too thin.
The decoy pool being small and clumped makes it worse here than against the whole chain.

**Construction C is infeasible on the arms that need it.** A size-matched patch has to fit
inside a decoy pocket.

| arm | label set size `m` | decoy pockets | pooled residues | largest lining | pockets with at least `m` residues |
| --- | ---: | ---: | ---: | ---: | ---: |
| `kras_g12c_mandated` | 16 | 3 | 23 | 10 | **0** |
| `kras_g12c_corrected` | 16 | 3 | 25 | 11 | **0** |
| `bcr_abl1_mandated` | 20 | 24 | 197 | 33 | 1 |
| `bcr_abl1_corrected` | 18 | 9 | 73 | 18 | **1** |
| `cardiac_myosin_corrected` | 12 | 41 | 291 | 35 | 8 |

On both KRAS arms **no decoy pocket is even as large as the label set**. On
`bcr_abl1_corrected` exactly one is, which floors that construction at 1/2.

**The conclusion is a negative result, and it is a clean one.** On two of the three
confirmatory arms, negative class (b) admits no valid significance test: A is powerless, B
does not hold its size, and C cannot be drawn. The binding constraint is decoy supply, and it
is worst on the smallest protein — the same arm the challenge mandates.

This is why a delegated recommendation is measured before it is adopted. An independent audit
of the metric layer proposed construction B as a critical fix. Installed unmeasured, it would
have given the report a headline test with a true size near 0.35.

---

## 4b. What can still be claimed, and it is not nothing

Per-arm p-values are floored. A **combination across arms is not**, because Fisher and
Stouffer are unbounded below even when each input is bounded. Computed from the frozen floors:

| family | per-arm floors | Fisher minimum attainable p | Stouffer |
| --- | --- | ---: | ---: |
| three confirmatory arms, frozen detector | 0.25, 0.10, 0.024 | **0.0214** | **0.0115** |
| three confirmatory arms, loosest detector tried | 0.053, 0.031, 0.012 | 0.0014 | 0.00045 |
| all five primary arms, frozen detector | 0.25, 0.25, 0.040, 0.10, 0.024 | 0.0074 | 0.0022 |

**So the challenge's negative class (b) is testable at the family level at alpha = 0.05, on
the frozen detector, with no change to the input layer.** Label it correctly: Fisher and
Stouffer test the intersection null — no arm has signal — so a rejection licenses "at least
one arm distinguishes the site from non-functional surface pockets". That is exactly the
claim `evaluation/README.md` §8 already scopes for the confirmatory arms, and it is a real
answer to a criterion the protocol currently reports as untestable.

---

## 5. Disposition

1. **Keep the pocket-rank test and keep reporting it.** It is the field's own convention and
   it is what a reader compares to APOP and PASSer. It is descriptive, never a decision.
2. **Stop describing the problem as a floor of 0.25 on some arms.** The honest statement is
   stronger: the test needs `delta >= 2.49` for 80 % power at any decoy count, so on the whole
   confirmatory family it is descriptive whatever the detector does.
3. **Do not add a residue-level decoy test.** Its measured size is 0.13 to 0.38 (§4a). This
   supersedes the recommendation in `07-metrics-audit.md` item 1, which was made before the
   calibration ran.
4. **Add a Fisher or Stouffer combination across the confirmatory arms** as the tested form of
   negative class (b), declared before any method is scored, and labelled as an
   intersection-null test (§4b). It reaches a minimum attainable p of 0.021 on the frozen
   detector and needs no input-layer change.
5. **Re-freeze the detector settings**, selecting on `n_decoys`, and report the site-coverage
   improvement as a consequence. This lowers the family floor from 0.021 to 0.0014 and fixes
   the `bcr_abl1_corrected` site pocket that currently covers two thirds of its label set.
6. **Do all of it before any candidate method is scored on the primary arms**, and record it
   as protocol version 3 with an ADR. The organisers' answer to Q4 is new information that
   arrived after the version-2 freeze, which is the same kind of event that reopened version 1.
7. **Document the decoy construction in the submission.** The organisers require it
   explicitly, and no other team's negative class will be comparable to ours.

---

## 6. Reproduction

```
data/decoy_power_sim.py             the Monte-Carlo power calculation
data/decoy-typeI.json               type-I rates of constructions A and B, all five arms
scratchpad/probe/decoy_typeI.py     the calibration run behind them
data/decoy-power-sweep.json         the nine-setting detector sweep, all five primary arms
scratchpad/probe/decoy_power.py     the script that produced the sweep
```
