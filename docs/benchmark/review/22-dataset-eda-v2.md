# 22 — What the fifteen label sets look like, at six primary arms

> **SUBJECT PARTLY DELETED — 2026-09-02.** This document cites files in the method layer:
> `src/allo/{network,classical,quantum}`, `docs/method/exploration/`, `tests/test_method.py`,
> or an experiment directory dated 2026-08-26 or 2026-08-27. All of those left `main` on
> 2026-09-02 (ADR 0037) and are preserved whole on the branch `method-layer-archive`.
> Findings whose subject is one of those files are **not re-runnable on `main`**. They stay
> here unedited, because a record of what an audit found is worth keeping even when the
> subject is gone. To re-run one, check out that branch. Two things moved rather than left:
> `allo.network.graph` is now `allo.structure.graph`, and the nine required baselines are now
> `allo.scoring.baselines`.

**Status.** Measured 2026-09-02, after the primary input layer was re-frozen at six arms.
Apo-only descriptors, computed against the frozen label sets. Nothing here changes a freeze.

This supersedes [`12-dataset-eda.md`](12-dataset-eda.md), which measured **five** descriptors
on **fourteen** arms while the primary set still had five. The primary set now has six:
`bcr_abl1_mandated` moved from `1OPL` chain A to chain **B** (ADR 0029) and
`cardiac_myosin_mandated` is frozen for the first time against `9GZ2` (ADR 0031). Fifteen arms,
**224 label residues against 6659 background residues**.

Two things changed in the conclusion, and only one of them is the new arms' doing.

1. `12`'s headline — "no descriptor is a benchmark-wide shortcut" — is **true of the five
   descriptors it measured and false of the benchmark**. A sixth apo-only descriptor,
   `cavity_volume`, reaches a median AUC-ROC of **0.795** and is the only column that rejects
   chance. It was omitted, not refuted: `12` measured what `residue_properties` returns plus
   two graph quantities, and the detector score lives elsewhere.
2. The two changed arms move almost nothing in the pooled numbers and a great deal in the
   graph. Both carry a descriptor that is not the physical quantity its name says.

---

## 0. Validation — this probe agrees with three frozen artifacts

Nothing below is worth reading unless the measurement pipeline reproduces numbers the
repository already pinned. It reproduces all four, independently derived:

| Check | Pinned where | Result |
| --- | --- | --- |
| Five original descriptor columns on the thirteen arms that did not change | [`12-dataset-eda.md`](12-dataset-eda.md) §2 | **13 of 14 rows identical to three decimals.** The only row that moved is `bcr_abl1_mandated`, which changed chain |
| Distance baseline, all six primary arms | [`../primary/README.md`](../primary/README.md) §4 — 0.589, 0.588, 0.385, 0.215, 0.442, 0.335 | reproduced exactly, as 1 − 0.411, 1 − 0.412, 1 − 0.615, 1 − 0.785, 1 − 0.558, 1 − 0.665 |
| `cavity_volume` AUC on the confirmatory family | [`../evaluation/README.md`](../evaluation/README.md) §8 — 0.830 / 0.795 / 0.977 | reproduced exactly, **at the detector's published defaults** (§4 below) |
| Site-pocket label coverage, v2 defaults → v3 settings | `../evaluation/manifest.yaml`, ADR 0030 — median 0.750 → 0.917 | measured 0.750 → 0.920, and all three per-arm figures the comment names |

---

## 1. What was measured

Seven apo-only descriptors per candidate residue. Labels are used only to **score** a
descriptor, never to build one. No holo coordinate enters the descriptor side.

| Descriptor | Source | New at this pass |
| --- | --- | --- |
| `relative_solvent_accessibility` | Shrake-Rupley SASA over Tien et al. maxima, doi:10.1371/journal.pone.0080635 | |
| `normalised_b_factor` | Deposited B-factor column, z-scored within the chain | |
| `hydrophobicity` | Kyte-Doolittle, doi:10.1016/0022-2836(82)90515-0 | |
| `degree` | Degree in the frozen 4.5 Å contact graph, `allo.network.build(apo)` at its defaults | |
| `distance_to_source` | Minimum Cα distance to any active-site residue | |
| `cavity_volume` | Volume of the largest pyKVFinder cavity lining the residue, `allo.scoring.decoys` | **yes** |
| residue composition | Kyte-Doolittle already carries the hydropathy axis; the identity axis is tested separately in §6 | **yes** |

The statistic is the Mann-Whitney AUC of the descriptor read as a standalone predictor: the
probability that a label residue outranks a background residue. 0.5 is chance, and a value far
from 0.5 in **either** direction means the descriptor alone separates the label set. Positives
are `scoreable_label_residues`; the background is `residue_ids` minus `excluded_from_scoring`,
which is the candidate set `score_arm` uses.

`cavity_volume` is reported at two detector settings, because the protocol pins one and the
package documents another, and they do not agree. See §4.

---

## 2. The result table

| arm | n+ | n- |   RSA |  norm B | hydro | degree |  dist | cavity | cavity v3 |
| --- | --: | --: | ----: | ------: | ----: | -----: | ----: | -----: | --------: |
| `kras_g12c_mandated` | 16 | 130 | 0.485 | 0.260 | 0.504 | 0.419 | 0.411 | 0.835 | 0.784 |
| `kras_g12c_corrected` | 16 | 132 | 0.487 | 0.491 | 0.500 | 0.425 | 0.412 | 0.830 | 0.843 |
| **`bcr_abl1_mandated`** | 17 | 337 | 0.493 | 0.234 | 0.651 | 0.534 | 0.615 | 0.752 | 0.739 |
| `bcr_abl1_corrected` | 18 | 243 | 0.500 | 0.388 | 0.667 | 0.542 | 0.785 | 0.795 | 0.563 |
| **`cardiac_myosin_mandated`** | 12 | 920 | 0.425 | 0.287 | 0.410 | 0.552 | 0.558 | 0.804 | 0.609 |
| `cardiac_myosin_corrected` | 12 | 731 | 0.569 | 0.563 | 0.389 | 0.486 | 0.665 | 0.977 | 0.806 |
| `mkp5` | 11 | 125 | 0.264 | 0.242 | 0.644 | 0.751 | 0.201 | 0.465 | 0.516 |
| `chk1` | 12 | 249 | 0.511 | 0.451 | 0.491 | 0.494 | 0.550 | 0.699 | 0.415 |
| `ptp1b` | 11 | 276 | 0.407 | 0.606 | 0.549 | 0.664 | 0.667 | 0.568 | 0.517 |
| `smyd3` | 12 | 396 | 0.567 | 0.612 | 0.562 | 0.526 | 0.719 | 0.871 | 0.696 |
| `glucokinase` | 19 | 419 | 0.575 | 0.674 | 0.607 | 0.531 | 0.365 | 0.870 | 0.809 |
| `hiv_rt` | 16 | 518 | 0.431 | 0.487 | 0.565 | 0.584 | 0.068 | 0.876 | 0.723 |
| `ns5b` | 16 | 534 | 0.232 | 0.404 | 0.645 | 0.770 | 0.739 | 0.457 | 0.364 |
| `p97_vcp` | 17 | 671 | 0.427 | 0.238 | 0.525 | 0.530 | 0.565 | 0.678 | 0.413 |
| `ecoli_cps` | 19 | 978 | 0.571 | 0.759 | 0.422 | 0.426 | 0.804 | 0.719 | 0.876 |

Column summary over the fifteen arms. **Pooled** is one Mann-Whitney over all 224 positives and
6659 negatives after converting each descriptor to its within-arm percentile rank, so an arm
with 1058 residues does not dominate one with 147. **Best-direction median** takes
max(AUC, 1 − AUC) per arm, which is the honest ceiling for a baseline allowed to choose its sign.

| descriptor | mean | median | best-direction median | pooled | Wilcoxon p |
| --- | ---: | ---: | ---: | ---: | ---: |
| RSA | 0.463 | 0.487 | 0.569 | 0.469 | 0.177 |
| norm B | 0.446 | 0.451 | 0.612 | 0.453 | 0.244 |
| hydro | 0.542 | 0.549 | 0.578 | 0.550 | 0.109 |
| degree | 0.549 | 0.531 | 0.552 | 0.543 | 0.135 |
| dist | 0.542 | 0.565 | **0.665** | 0.546 | 0.389 |
| **cavity** | **0.746** | **0.795** | **0.795** | **0.771** | **0.0003** |
| cavity, v3 settings | 0.645 | 0.696 | 0.696 | 0.669 | 0.010 |

Holm over the seven tests puts the threshold for the smallest p at 0.05/7 = 0.0071.
`cavity_volume` clears it at both detector settings. Nothing else comes close.

---

## 3. Finding 1 — the five original columns are confirmed, and the distance median holds

`12` §3 said no descriptor is a benchmark-wide shortcut and §5 gave the better distance
direction a median AUC of 0.666 over fourteen arms. Both survive the two new arms:

- All five original mean AUCs stay between **0.446 and 0.549**, and no Wilcoxon p reaches 0.10.
- Best-direction distance median is **0.665** at fifteen arms, against 0.666 at fourteen. The
  two extremes `12` quotes are untouched: `hiv_rt` 0.932 and `ecoli_cps` 0.804.
- Nine of fifteen arms favour "far" and six favour "near", against nine and five before.
  `bcr_abl1_mandated` stays a "far" arm, and `cardiac_myosin_mandated` joins as one.

`12` §4's sign-flip finding is also unchanged and now has one more instance: `ns5b` labels are
buried and high-degree (RSA 0.232, degree 0.770), `mkp5` labels are buried, high-degree and
close (0.264, 0.751, 0.201), `ecoli_cps` labels are exposed, floppy and far (0.571, 0.759,
0.804). The direction is a property of each protein's architecture, not of allosteric sites.

**So the disposition items `12` left open are unaffected by the re-freeze.** Item 3 —
declare the distance direction or spend a multiplicity level — is still open and still costs
the same.

---

## 4. Finding 2 — the shortcut `12` missed, and it is the protocol's own claim threshold

`cavity_volume` scores each candidate by the volume of the largest detected cavity that lines
it. It is label-blind, apo-only and zero-parameter. At fifteen arms it gives median AUC-ROC
**0.795**, pooled **0.771**, and a Wilcoxon p of **0.0003** — the only descriptor here that
rejects chance. It reaches 0.87 or better on four arms and 0.977 on `cardiac_myosin_corrected`.

This is not news to the evaluation layer. ADR 0025 already made "beat `cavity_volume`" the
claim threshold and protocol v3 gave it its own confirmatory family (ADR 0032). It is news to
this page, which concluded the opposite from a descriptor list that did not contain it. **The
correction is to `12`, not to the freeze.**

Read as the field reads it, the same detection run ranks pockets by volume and asks where the
site pocket lands — the convention APOP states as "if this pocket is among the top-ranked three
predicted pockets, we count it as a success" (doi:10.1093/bioinformatics/btad275). The site
pocket is the detected pocket covering the most label residues, exactly as `decoys.classify`
defines it.

| arm | pockets | site rank | Jaccard | label recall | pockets v3 | site rank v3 | Jaccard v3 | recall v3 |
| --- | ------: | --------: | ------: | -----------: | ---------: | -----------: | ---------: | --------: |
| `kras_g12c_mandated` | 5 | 2 | 0.667 | 0.75 | 16 | 1 | 0.325 | 0.81 |
| `kras_g12c_corrected` | 4 | 1 | 0.545 | 0.75 | 21 | 1 | 0.333 | 0.94 |
| **`bcr_abl1_mandated`** | 18 | 3 | 0.611 | 0.65 | 48 | 2 | 0.37 | 1.0 |
| `bcr_abl1_corrected` | 12 | 3 | 0.632 | 0.67 | 35 | 2 | 0.37 | 0.94 |
| **`cardiac_myosin_mandated`** | 65 | 2 | 0.169 | 0.92 | 144 | 1 | 0.017 | 0.92 |
| `cardiac_myosin_corrected` | 42 | 1 | 0.267 | 1.0 | 85 | 1 | 0.041 | 1.0 |
| `mkp5` | 4 | 2 | 0.059 | 0.09 | 19 | 1 | 0.132 | 0.45 |
| `chk1` | 11 | 6 | 0.833 | 0.83 | 47 | 9 | 0.647 | 0.92 |
| `ptp1b` | 13 | 3 | 0.267 | 0.36 | 41 | 1 | 0.059 | 0.36 |
| `smyd3` | 13 | 2 | 0.632 | 1.0 | 35 | 1 | 0.047 | 1.0 |
| `glucokinase` | 23 | 2 | 0.68 | 0.89 | 56 | 2 | 0.475 | 1.0 |
| `hiv_rt` | 28 | 5 | 0.5 | 0.62 | 72 | 1 | 0.066 | 0.62 |
| `ns5b` | 22 | 20 | 0.143 | 0.19 | 54 | 1 | 0.017 | 0.31 |
| `p97_vcp` | 44 | 15 | 0.556 | 0.59 | 71 | 13 | 0.6 | 0.71 |
| `ecoli_cps` | 47 | 9 | 0.652 | 0.79 | 100 | 1 | 0.074 | 0.95 |

### 4a. The bar moves with the detector setting, and the protocol pins it in only one place

`../evaluation/manifest.yaml` pins `decoys.detector_settings` — `probe_out` 8.0,
`removal_distance` 1.2, `volume_cutoff` 1.0, re-frozen on `n_decoys` alone at v3 (ADR 0030).
`allo.scoring.decoys.DETECTOR_DEFAULTS` is the package's documented defaults —
`probe_out` 4.0, `removal_distance` 2.4, `volume_cutoff` 5.0. The harness passes the frozen
settings when it builds the **decoy split**. Nothing states which settings the
`cavity_volume` **baseline** runs at, and `manifest.yaml: classical_comparison` names the
baseline without naming a setting.

The two settings do not give the same baseline:

| Quantity, over fifteen arms | package defaults | v3 frozen settings |
| --- | ---: | ---: |
| median `cavity_volume` AUC-ROC | **0.795** | **0.696** |
| pooled AUC-ROC | 0.771 | 0.669 |
| site pocket in the top 3 by volume | 10 of 15 | **13 of 15** |
| median site-pocket rank | 3 | **1** |
| median site-pocket label coverage | 0.750 | **0.920** |
| median site-pocket Jaccard against the label set | **0.556** | 0.132 |

They move in opposite directions, and the mechanism is visible in the last two rows. The v3
settings roll a larger probe with less removal, so pockets merge: the site pocket now almost
always contains the whole label set and is far too big, which improves the **pocket-level**
rank and degrades the **residue-level** score that a merged cavity assigns to everything it
touches. ADR 0030 selected on `n_decoys`, which is label-free and cannot shape the negative
class with the answer key. That argument is untouched. What was not measured is that the same
choice moves the claim threshold by **0.099 median AUC**, downward.

**And the number already in print is the defaults one.**
[`../evaluation/README.md`](../evaluation/README.md) §8 gives `cavity_volume` as
0.830 / 0.795 / 0.977 on the confirmatory family. This probe returns exactly that triple at
the package defaults and **0.843 / 0.563 / 0.806** at the v3 `detector_settings`. Trimming a
lining to the candidate set cannot explain the gap, because `cavity_volume_score` already
scores only candidates. So the claim threshold a v3 document prints was measured at a setting
v3 does not pin. Whether that was intended is not established here.

**What this forces.** `evaluation/manifest.yaml` should name the settings the
`cavity_volume` baseline runs at, in the same way it names them for the decoy split. Until it
does, a method that reports "we beat `cavity_volume`" has not said which `cavity_volume`.
Recorded here; it needs an ADR, and this page does not make it.

---

## 5. Finding 3 — the two changed arms each carry a descriptor that is not what its name says

Neither new arm moves a pooled number much. Both break a descriptor.

### 5a. `bcr_abl1_mandated`: the B-factor column has three values

`1OPL` chain B was rigid-body placed and refined with group B-factors. The whole 365-residue
chain carries exactly **three distinct B values**, raw 160.84 to 198.13 Å², constant within
each residue. Z-scored, the descriptor takes the values −0.61, −0.59 and +1.65.

`normalised_b_factor` on this arm is therefore not a flexibility proxy at all. It is a
three-level indicator of **which rigid body a residue was placed in**, and its AUC of 0.234
says the labels sit in the low-B group. Read best-direction, **0.766 is the arm's strongest
apo-only descriptor** — a refinement artefact outscoring every geometric quantity on it. Any
per-arm result on this arm that correlates with `normalised_b_factor` is reporting the
refinement protocol.

The other descriptors barely move from `bcr_abl1_corrected`, and that is itself informative:
RSA mean 0.252 against 0.250, buried fraction (RSA < 0.2) 0.504 against 0.504, mean degree
9.28 against 9.36. **Local packing in chain B is normal.** The five original columns did move
against the old chain-A row — RSA 0.378 → 0.493, hydro 0.698 → 0.651, degree 0.628 → 0.534,
dist 0.519 → 0.615 — because the label set changed from 20 residues to 17 and the candidate
set from 440 to 354, not because the protein is packed differently.

What is not normal is the global topology, and the missing SH3 domain is exactly where it
shows. Measured on the frozen graph: **0 residues modelled in 84–138**, and the 91-node SH2
domain attaches to the 265-node kinase domain through **17 edges**. The consequences:

| | `bcr_abl1_mandated` (`1OPL`:B) | `bcr_abl1_corrected` (`2G2H`:A) |
| --- | ---: | ---: |
| spectral gap | **0.0625** | 0.1936 |
| diameter, hops | **15** | 10 |
| mean shortest path | 5.91 | 4.50 |
| relative contact order | 0.0483 | 0.0696 |
| edges across the Fiedler cut | 51 | 80 |

A 3.1× smaller spectral gap on a graph with 34 % more nodes is the quantitative form of "the
clamp is not assembled" ([`01-bcr-abl1-chain.md`](01-bcr-abl1-chain.md) §3.2). Any propagation
score with a global time or length scale will behave differently here for a reason that is
about the deposition, not about ABL1.

### 5b. `cardiac_myosin_mandated`: the model is under-packed, and its B column is not a B-factor

`5TBY` is a SWISS-MODEL homology model on a tarantula template, rigid-body fitted, deposited
at 20 Å with no `refine` block. Two measurements say what that costs, both against
`cardiac_myosin_corrected`, which is the **same protein** solved at 3.4 Å.

**The B column is not an atomic displacement parameter.** Its raw range is **0.00 to 6.25**,
constant within each residue. `9GZ3`'s is 16.82 to 108.47, also per-residue constant, which is
an ordinary grouped cryo-EM refinement. A quantity bounded by 6.25 in a file with no
refinement block cannot be a thermal B-factor; what it is instead is **unknown** and is not
inferred here. `normalised_b_factor` on this arm z-scores that unknown quantity and returns
AUC 0.287.

**The contact graph is systematically looser.** At the same 4.5 Å cutoff and the same builder:

| | `cardiac_myosin_mandated` (`5TBY`:A, 20 Å model) | `cardiac_myosin_corrected` (`9GZ3`:A, 3.4 Å) |
| --- | ---: | ---: |
| nodes | 954 | 764 |
| mean degree | **8.27** — the lowest in the benchmark | 9.53 |
| buried fraction, RSA < 0.2 | **0.343** | 0.514 |
| mean RSA | 0.328 | 0.234 |
| fraction of nodes with degree ≤ 6 | 0.225 | 0.166 |
| diameter, hops | **35** — the largest in the benchmark | 22 |
| mean shortest path | **11.11** | 7.19 |
| spectral gap | **0.0063** — the smallest in the benchmark, by 3.2× | 0.0527 |
| edges across the Fiedler cut | 14 | 118 |

Half the residues that are buried in the measured structure are not buried in the model. That
is one number for "the contact topology is largely invented"
([`02-cardiac-myosin.md`](02-cardiac-myosin.md) §3), computed on the object C6 makes the
method rest on.

**One caution against overreading the bottleneck.** A 14-edge Fiedler cut sounds unique and is
not: `p97_vcp` has **8**, on a measured 1.9 Å structure, because a two-domain AAA+ ATPase
genuinely is two lobes. The distinctive myosin numbers are the **packing** ones — mean degree
8.27 and buried fraction 0.343 — which have no counterpart anywhere else in the set.

**What survives.** `cavity_volume` still reaches 0.804 on this arm and the site pocket still
ranks 2 of 65. A detector finds the mavacamten pocket in the model. That is consistent with
ADR 0031 admitting the arm as non-confirmatory: the labels are real, the topology is not.

---

## 6. Finding 4 — composition is still not a route in

Pooled over fifteen arms: 224 label residues against 6659 background residues.

| residue | label n | label % | background % | odds ratio | Fisher p |
| --- | ---: | ---: | ---: | ---: | ---: |
| TYR | 16 | 7.1 | 3.4 | 2.20 | 0.008 |
| HIS | 10 | 4.5 | 1.9 | 2.44 | 0.012 |
| SER | 5 | 2.2 | 5.2 | 0.42 | 0.060 |
| ASP | 6 | 2.7 | 5.5 | 0.47 | 0.070 |
| LYS | 9 | 4.0 | 7.2 | 0.54 | 0.083 |

Twenty tests, five shown. The smallest p is 0.008 against a Holm threshold of 0.05/20 =
**0.0025**. Nothing survives correction, as at fourteen arms — but note that the TYR and HIS
p-values fell from 0.023 and 0.038 to 0.008 and 0.012 on nine extra label residues. The trend
is the same one `12` recorded and declined to claim, and it is recorded and declined again.

`12` reported a Fisher table and no AUC, so composition had no number comparable to the other
columns. It has one now. Score each residue by a log-odds prior fitted on the **other fourteen
arms'** label and background composition, then score that prior on the held-out arm:

median AUC **0.591**, mean 0.557, Wilcoxon p 0.030 — not significant under Holm over the
descriptor family, where the correction stops after `cavity_volume`: the next-smallest p is
0.010 and its threshold is 0.05/6 = 0.0083. Per arm it ranges from 0.410 on `ecoli_cps` to
0.749 on `glucokinase`.

Two cautions on that number. It is **not apo-only in the sense the other six are**: it is
fitted on fourteen other arms' answers, so it is a transfer baseline, not a descriptor. And a
20-parameter prior fitted on 224 positives is at the edge of what the data supports. The
finding is unchanged: **a composition-only predictor cannot score on this benchmark**, which
removes a whole class of trivial baseline.

---

## 7. The multi-scale picture, and what it costs a single setting

| arm | nodes | edges | mean deg | max deg | diameter | mean path | clustering | spectral gap | comps | rel. contact order | Fiedler cut |
| --- | ----: | ----: | -------: | ------: | -------: | --------: | ---------: | -----------: | ----: | -----------------: | ----------: |
| `kras_g12c_mandated` | 169 | 795 | 9.41 | 16 | 8 | 3.7 | 0.511 | 0.48 | 1 | 0.1232 | 77 |
| `kras_g12c_corrected` | 170 | 803 | 9.45 | 16 | 8 | 3.67 | 0.507 | 0.4967 | 1 | 0.1203 | 77 |
| **`bcr_abl1_mandated`** | 365 | 1694 | 9.28 | 19 | 15 | 5.91 | 0.501 | 0.0625 | 1 | 0.0483 | 51 |
| `bcr_abl1_corrected` | 272 | 1273 | 9.36 | 19 | 10 | 4.5 | 0.502 | 0.1936 | 1 | 0.0696 | 80 |
| **`cardiac_myosin_mandated`** | 954 | 3947 | 8.27 | 15 | 35 | 11.11 | 0.516 | 0.0063 | 1 | 0.0366 | 14 |
| `cardiac_myosin_corrected` | 764 | 3641 | 9.53 | 18 | 22 | 7.19 | 0.481 | 0.0527 | 1 | 0.0602 | 118 |
| `mkp5` | 147 | 718 | 9.77 | 16 | 7 | 3.4 | 0.515 | 0.5475 | 1 | 0.1228 | 76 |
| `chk1` | 272 | 1255 | 9.23 | 20 | 13 | 4.75 | 0.502 | 0.1391 | 1 | 0.0663 | 59 |
| `ptp1b` | 298 | 1481 | 9.94 | 20 | 10 | 4.36 | 0.488 | 0.3181 | 1 | 0.1025 | 106 |
| `smyd3` | 425 | 2089 | 9.83 | 20 | 12 | 5.33 | 0.496 | 0.1506 | 1 | 0.0618 | 99 |
| `glucokinase` | 453 | 2270 | 10.02 | 17 | 14 | 5.4 | 0.48 | 0.1267 | 1 | 0.0894 | 98 |
| `hiv_rt` | 543 | 2403 | 8.85 | 16 | 22 | 8.45 | 0.499 | 0.0247 | 1 | 0.0414 | 41 |
| `ns5b` | 553 | 2720 | 9.84 | 18 | 12 | 5.85 | 0.477 | 0.12 | 1 | 0.0764 | 84 |
| `p97_vcp` | 723 | 3241 | 8.97 | 17 | 18 | 7.81 | 0.482 | 0.0203 | 1 | 0.0341 | 8 |
| `ecoli_cps` | 1058 | 5433 | 10.27 | 18 | 15 | 6.8 | 0.46 | 0.0952 | 1 | 0.045 | 180 |

| arm | prevalence | n+ | dist min / median / max, A | label R_g, A | R_g / chain R_g | label mean degree | centroid to source, A |
| --- | ---------: | -: | ------------------------: | -----------: | --------------: | ----------------: | --------------------: |
| `kras_g12c_mandated` | 10.96 % | 16 | 3.8 / 10.6 / 18.3 | 7.97 | 0.541 | 8.75 | 16.9 |
| `kras_g12c_corrected` | 10.81 % | 16 | 3.8 / 10.7 / 18.2 | 7.86 | 0.53 | 8.81 | 16.7 |
| **`bcr_abl1_mandated`** | 4.80 % | 17 | 10.6 / 17.3 / 23.9 | 7.83 | 0.306 | 9.59 | 24.0 |
| `bcr_abl1_corrected` | 6.90 % | 18 | 10.8 / 17.5 / 30.1 | 8.69 | 0.456 | 9.67 | 24.1 |
| **`cardiac_myosin_mandated`** | 1.29 % | 12 | 16.8 / 27.9 / 41.1 | 9.34 | 0.223 | 8.75 | 34.6 |
| `cardiac_myosin_corrected` | 1.62 % | 12 | 16.5 / 27.6 / 35.6 | 8.9 | 0.293 | 9.42 | 32.2 |
| `mkp5` | 8.09 % | 11 | 3.8 / 6.2 / 12.5 | 6.29 | 0.437 | 12.09 | 10.4 |
| `chk1` | 4.60 % | 12 | 7.1 / 15.3 / 19.0 | 6.76 | 0.342 | 9.08 | 18.8 |
| `ptp1b` | 3.83 % | 11 | 13.5 / 16.7 / 21.5 | 7.02 | 0.371 | 11.45 | 20.2 |
| `smyd3` | 2.94 % | 12 | 18.2 / 25.4 / 34.5 | 8.08 | 0.364 | 10.17 | 33.5 |
| `glucokinase` | 4.34 % | 19 | 6.3 / 12.8 / 18.6 | 8.27 | 0.362 | 10.21 | 18.5 |
| `hiv_rt` | 3.00 % | 16 | 4.4 / 10.4 / 16.5 | 7.97 | 0.239 | 9.69 | 12.5 |
| `ns5b` | 2.91 % | 16 | 22.3 / 28.5 / 36.8 | 8.21 | 0.342 | 12.38 | 28.7 |
| `p97_vcp` | 2.47 % | 17 | 14.1 / 16.5 / 23.1 | 7.1 | 0.229 | 9.18 | 19.8 |
| `ecoli_cps` | 1.91 % | 19 | 12.5 / 18.9 / 28.7 | 8.05 | 0.283 | 9.68 | 29.8 |

**Local structure is nearly constant; global structure varies by two orders of magnitude.**

| Quantity | Range over fifteen arms | Ratio |
| --- | --- | ---: |
| mean degree | 8.27 (`cardiac_myosin_mandated`) – 10.27 (`ecoli_cps`) | **1.24×** |
| average clustering coefficient | 0.460 (`ecoli_cps`) – 0.516 (`cardiac_myosin_mandated`) | 1.12× |
| max degree | 15 – 20 | 1.33× |
| connected components | 1 everywhere | — |
| nodes | 147 (`mkp5`) – 1058 (`ecoli_cps`) | 7.2× |
| diameter, hops | 7 (`mkp5`) – 35 (`cardiac_myosin_mandated`) | 5.0× |
| mean shortest path | 3.40 – 11.11 | 3.3× |
| relative contact order | 0.0341 (`p97_vcp`) – 0.1232 (`kras_g12c_mandated`) | 3.6× |
| **spectral gap** | **0.0063** (`cardiac_myosin_mandated`) – **0.5475** (`mkp5`) | **87×** |

**What this means for a method that must run on all fifteen with one setting.** The contact
graph is locally the same object everywhere: about nine or ten neighbours, clustering near
0.49, one component, no isolated node. A parameter defined **locally** — the contact rule, the
cutoff, an edge weighting, a neighbourhood radius in hops — transfers across the set for free,
because the quantity it acts on barely moves.

A parameter defined **globally** does not. Diffusion and quantum-walk mixing times scale with
the inverse spectral gap, and that runs 1.83 on `mkp5` to 159 on `cardiac_myosin_mandated` — a
factor of **87**. One propagation time cannot be simultaneously long enough to cross a
954-node myosin model of diameter 35 and short enough not to equilibrate a 147-node phosphatase
of diameter 7. A method whose only free parameter is a global time or decay length is therefore
choosing which half of the benchmark to work on, and it must either (i) normalise the parameter
by a graph quantity computed from the apo input alone — the spectral gap and the diameter are
both apo-only and both legal — or (ii) report the sweep and take the multiplicity hit. **Option
(i) is not per-arm tuning**, provided the normalising quantity is a fixed function of the input
and is fixed before any arm is scored.

**Label geometry is the quiet invariant.** Across fifteen arms of 147 to 1058 residues, the
label set's radius of gyration runs only **6.29 to 9.34 Å** (1.5×) and its mean degree
**8.75 to 12.38**. Allosteric sites are the same size everywhere; what changes is the protein
around them. That is why prevalence falls from 10.96 % to 1.29 % mainly because N grows and not
because label sets shrink — the label count runs only 11 to 19 across all fifteen arms — and it
is why `R_g` / chain `R_g` — 0.223 to 0.541 — is a cleaner compactness statement than `R_g`.
It also means a fixed k = 5 top-list is a harder target on a big protein for a reason that has
nothing to do with allostery.

---

## 8. Which arm is hardest, which is easiest

The three defensible measures disagree, and naming which one decides is part of the answer.

| arm | strongest apo-only descriptor | best-direction AUC | prevalence | expected hits in top 5 at chance |
| --- | --- | ----: | ---------: | ----: |
| `ptp1b` | `distance_to_source` | 0.667 | 3.83 % | 0.192 |
| `chk1` | `cavity_volume` | 0.699 | 4.60 % | 0.230 |
| `p97_vcp` | `normalised_b_factor` | 0.762 | 2.47 % | 0.123 |
| **`bcr_abl1_mandated`** | `normalised_b_factor` | 0.766 | 4.80 % | 0.240 |
| `ns5b` | `degree` | 0.770 | 2.91 % | 0.146 |
| `bcr_abl1_corrected` | `cavity_volume` | 0.795 | 6.90 % | 0.345 |
| `mkp5` | `distance_to_source` | 0.799 | 8.09 % | 0.404 |
| **`cardiac_myosin_mandated`** | `cavity_volume` | 0.804 | 1.29 % | 0.065 |
| `kras_g12c_mandated` | `cavity_volume` | 0.835 | 10.96 % | 0.548 |
| `kras_g12c_corrected` | `cavity_volume_v3` | 0.843 | 10.81 % | 0.540 |
| `glucokinase` | `cavity_volume` | 0.870 | 4.34 % | 0.217 |
| `smyd3` | `cavity_volume` | 0.871 | 2.94 % | 0.147 |
| `ecoli_cps` | `cavity_volume_v3` | 0.876 | 1.91 % | 0.096 |
| `hiv_rt` | `distance_to_source` | 0.932 | 3.00 % | 0.150 |
| `cardiac_myosin_corrected` | `cavity_volume` | 0.977 | 1.62 % | 0.081 |

**By free signal — the measure that decides.** The strongest apo-only descriptor available on
an arm is the bar a method must clear there before it has demonstrated anything.

- **Hardest: `ptp1b`, at 0.667.** No apo-only descriptor exceeds AUC 0.667 on it — the lowest
  ceiling in the benchmark. Its cavity signal is weak in both settings (0.568 / 0.517) and the
  detector recovers only **36 %** of its label residues in the site pocket at either setting,
  so the pocket route is half-blind there. The next-hardest is `chk1` at 0.699.
- **Easiest: `cardiac_myosin_corrected`, at 0.977.** `cavity_volume` alone nearly separates
  its label set, the site pocket ranks **1** of 42 by volume at the defaults and 1 of 85 at the
  v3 settings, and the detector recovers **100 %** of its labels. A zero-parameter geometric
  baseline gets 0.977 for free on an arm with the second-lowest prevalence in the set.

**By base rate, the answer flips, and this is the trap.** `cardiac_myosin_mandated` has
prevalence **1.29 %** and expects **0.065** hits in a top-5 list at chance, against
`kras_g12c_mandated`'s 10.96 % and 0.548 — a factor of **8.4**. So the arm with the least
signal per candidate is a myosin arm and the arm with the most free signal is also a myosin
arm. Prevalence measures how thin the positives are; it does not measure how hard they are to
find. **Quote the free-signal number when the claim is about a method, and the prevalence
number when the claim is about a metric's chance line.**

**By pocket-detector failure, a third answer.** `mkp5` is the arm where the detector is worst:
its site pocket covers **9 %** of the label set at the defaults and 45 % at the v3 settings.
`mkp5` is nonetheless easy by distance (0.799) and degree (0.751). A detector failure and a
hard arm are different things, and the benchmark contains one of each.

**The single number.** A method must beat **median AUC-ROC 0.795** — `cavity_volume` over
fifteen arms, at the detector's published defaults; **0.696** at the protocol's v3 settings;
and on the three confirmatory arms specifically, **0.830 / 0.795 / 0.977**, which ADR 0025
already fixed as the claim threshold. The next-strongest descriptor is `distance_to_source`
at a best-direction median of **0.665**, and that one has to declare its direction post hoc.

---

## 9. Disposition

| # | Finding | Action |
| - | --- | --- |
| 1 | `12` §3's "no descriptor is a shortcut" holds for its five columns and not for the benchmark | **Correct `12` here, not in the freeze.** `cavity_volume` is the sixth column and it is a shortcut |
| 2 | Best-direction distance median is 0.665 at fifteen arms, against 0.666 at fourteen | `12` disposition item 3 is unaffected and still open |
| 3 | The `cavity_volume` baseline's detector settings are not pinned, and the two candidate settings differ by 0.099 median AUC | Needs an ADR. `evaluation/manifest.yaml` pins settings for the decoy split and not for the baseline |
| 4 | `normalised_b_factor` is a three-level rigid-body indicator on `bcr_abl1_mandated` and an unidentified quantity on `cardiac_myosin_mandated` | Print it as **not applicable** on those two arms rather than as a flexibility confounder. ADR 0025's display rule assumes a refined B-factor |
| 5 | The `5TBY` graph is under-packed: mean degree 8.27 against 9.53, buried fraction 0.343 against 0.514 | Record beside ADR 0031's Jaccard 0.471. Same conclusion, a second measurement |
| 6 | Spectral gap spans 87× across the set; local packing spans 1.24× | A global propagation time must be normalised by an apo-only graph quantity, or swept and corrected for |
| 7 | Composition still does not survive Holm; the leave-one-arm-out prior gives median 0.591, p = 0.030 | Closed. No composition baseline needed |

Items 3 and 4 are the ones that change what a document must print. Item 6 is the one that
changes what a method may do.

---

## 10. Reproduction

The probe cannot be committed, for the reason [`12-dataset-eda.md`](12-dataset-eda.md) §7
gives and ADR 0034 settled: `tests/test_no_leakage.py` fails any tracked script naming
`frozen.json`, and a review tool inside this tree is exempt only if it imports nothing from
`allo`. This one imports four `allo` modules, so it lives in the session scratchpad and its
source is reproduced here in full. Write it outside the repository and run it from the
repository root with `uv run python`.

Requires the optional `eval` extra (pyKVFinder 0.9.3, version-asserted by
`detect_pockets`) and `networkx`. Runtime is a few minutes, dominated by two pyKVFinder
passes over fifteen structures.

```python
"""Apo-only descriptor and structure EDA over all fifteen frozen arms.

Read-only. No holo coordinates. Labels are used only to score a descriptor, never to
build one. Run from the repository root with `uv run python`.
"""

import json
from collections import Counter
from pathlib import Path

import networkx as nx
import numpy as np
from scipy import stats
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components, shortest_path

from allo.inputs import apo_input
from allo.network import build
from allo.scoring.decoys import cavity_volume_score, detect_pockets
from allo.structure.properties import residue_properties

SETS = ("docs/benchmark/primary/frozen.json", "docs/benchmark/secondary/frozen.json")
OUT = "/tmp/eda.json"  # never inside the repository: a tracked file naming frozen.json fails the leakage gate

# The two pyKVFinder settings that matter. DEFAULTS is `decoys.DETECTOR_DEFAULTS`, the
# package's documented defaults. V3 is `evaluation/manifest.yaml: decoys.detector_settings`,
# re-frozen 2026-09-02 on `n_decoys` alone (ADR 0030). Written out here so this script opens
# only the two input freezes.
V3_SETTINGS = {
    "step": 0.6,
    "probe_in": 1.4,
    "probe_out": 8.0,
    "removal_distance": 1.2,
    "volume_cutoff": 1.0,
}
COLS = (
    "relative_solvent_accessibility",
    "normalised_b_factor",
    "hydrophobicity",
    "degree",
    "distance_to_source",
    "cavity_volume",
    "cavity_volume_v3",
)


def auc(pos, neg):
    """Mann-Whitney AUC of a descriptor read as a standalone predictor. 0.5 is chance."""
    pos, neg = np.asarray(pos, float), np.asarray(neg, float)
    if not len(pos) or not len(neg) or np.ptp(np.concatenate([pos, neg])) == 0:
        return 0.5
    return stats.mannwhitneyu(pos, neg, alternative="two-sided")[0] / (len(pos) * len(neg))


def rg(points):
    return float(np.sqrt(((points - points.mean(0)) ** 2).sum(1).mean()))


arms, pooled = {}, {c: ([], []) for c in COLS}
for path in SETS:
    frozen = json.loads(Path(path).read_text())
    for arm, spec in frozen["targets"].items():
        apo = apo_input(arm)
        graph = build(apo)  # default build == the evaluation graph
        props = residue_properties(apo)

        excluded = set(spec["excluded_from_scoring"])
        candidates = [r for r in spec["residue_ids"] if r not in excluded]
        labels = set(spec["scoreable_label_residues"])
        source = set(spec["active_site"])

        s = apo.structure
        ca = {
            int(r): np.asarray(x, float)
            for r, a, x in zip(s.seq_id, s.atom, s.coord, strict=True)
            if a == "CA"
        }
        resname = {int(r): str(n) for r, n in zip(s.seq_id, s.resname, strict=True)}
        source_xyz = np.array([ca[r] for r in sorted(source) if r in ca])
        degree = dict(zip(graph.order, graph.degree, strict=True))
        distance = {r: float(np.linalg.norm(source_xyz - ca[r], axis=1).min()) for r in ca}

        pockets = detect_pockets(apo)  # apo-only, no label enters
        pockets_v3 = detect_pockets(apo, **V3_SETTINGS)
        columns = dict(props)
        columns["degree"] = {r: float(degree[r]) for r in candidates}
        columns["distance_to_source"] = {r: distance[r] for r in candidates if r in ca}
        columns["cavity_volume"] = cavity_volume_score(pockets, candidates)
        columns["cavity_volume_v3"] = cavity_volume_score(pockets_v3, candidates)

        scores = {}
        for name in COLS:
            values = {r: v for r, v in columns[name].items() if r in set(candidates)}
            pos = [v for r, v in values.items() if r in labels]
            neg = [v for r, v in values.items() if r not in labels]
            scores[name] = round(auc(pos, neg), 3)
            rank = stats.rankdata(list(values.values())) / len(values)
            for (r, _), q in zip(values.items(), rank):
                pooled[name][0 if r in labels else 1].append(q)

        # graph properties, unweighted: the default build is unit-weighted
        adj = (graph.weight > 0).astype(np.int8)
        deg = adj.sum(1)
        hops = shortest_path(csr_matrix(adj), method="D", unweighted=True)
        order = np.asarray(graph.order, int)
        ii, jj = np.nonzero(np.triu(adj, 1))
        eigval, eigvec = np.linalg.eigh(np.diag(deg) - adj.astype(float))
        side = eigvec[:, 1] > 0  # Fiedler bipartition
        small = side if side.sum() < graph.n / 2 else ~side

        lab = np.array([ca[r] for r in sorted(labels)])
        cand_xyz = np.array([ca[r] for r in candidates])
        lab_dist = np.array([distance[r] for r in sorted(labels)])

        # pocket ranking, the field's own convention (APOP, doi:10.1093/bioinformatics/btad275).
        # The label enters only to say WHICH detected pocket is the site, exactly as
        # `decoys.classify` does. It does not enter the ranking.
        def rank_pockets(found):
            lin = [
                (float(p["volume"]), set(map(int, p["lining"])) & set(candidates))
                for p in found.values()
            ]
            lin = [(v, s) for v, s in lin if s]
            lin.sort(key=lambda r: -r[0])
            # `decoys.classify` calls the site pocket the one covering the MOST label
            # residues, so this does too. Ranking by Jaccard instead picks a different
            # pocket and a different rank on four arms.
            b = int(np.argmax([len(s & labels) for _, s in lin]))
            cover = lin[b][1] & labels
            return (
                b + 1,
                len(lin),
                round(len(cover) / len(lin[b][1] | labels), 3),
                round(len(cover) / len(labels), 2),
            )

        rank, n_pockets, jaccard, recall = rank_pockets(pockets)
        rank_v3 = rank_pockets(pockets_v3)

        arms[arm] = {
            "set": "primary" if "primary" in path else "secondary",
            "n_residues": spec["n_residues"],
            "n_candidates": spec["n_candidates"],
            "n_labels": len(labels),
            "prevalence": round(len(labels) / spec["n_candidates"], 4),
            "descriptors": scores,
            "graph": {
                "n_edges": int(adj.sum() // 2),
                "mean_degree": round(float(deg.mean()), 2),
                "max_degree": int(deg.max()),
                "diameter": int(hops[np.isfinite(hops)].max()),
                "mean_path": round(float(hops[np.isfinite(hops)].mean()), 2),
                "clustering": round(nx.average_clustering(nx.from_numpy_array(adj)), 3),
                "spectral_gap": round(float(eigval[1]), 4),
                "components": int(connected_components(csr_matrix(adj), directed=False)[0]),
                "rel_contact_order": round(
                    float(np.abs(order[ii] - order[jj]).mean() / graph.n), 4
                ),
                "fiedler_cut_edges": int(adj[np.ix_(side, ~side)].sum()),
                "fiedler_small_side": f"{order[small].min()}-{order[small].max()}",
                "b_factor_distinct": len({round(float(v), 3) for v in graph.bfactor}),
            },
            "labels": {
                "dist_min": round(float(lab_dist.min()), 1),
                "dist_median": round(float(np.median(lab_dist)), 1),
                "dist_max": round(float(lab_dist.max()), 1),
                "rg": round(rg(lab), 2),
                "rg_over_chain": round(rg(lab) / rg(cand_xyz), 3),
                "mean_degree": round(float(np.mean([degree[r] for r in labels])), 2),
                "centroid_to_source": round(
                    float(np.linalg.norm(lab.mean(0) - source_xyz.mean(0))), 1
                ),
            },
            "pocket_rank": rank,
            "n_pockets": n_pockets,
            "pocket_jaccard": jaccard,
            "pocket_recall": recall,
            "pocket_v3": rank_v3,
            "composition": dict(Counter(resname[r] for r in sorted(labels))),
            "background": dict(Counter(resname[r] for r in candidates if r not in labels)),
        }

Path(OUT).write_text(json.dumps(arms, indent=1, default=float))
for arm, v in arms.items():
    print(
        arm,
        v["descriptors"],
        v["graph"],
        v["labels"],
        v["pocket_rank"],
        v["n_pockets"],
        v["pocket_jaccard"],
        v["pocket_recall"],
        v["pocket_v3"],
    )

print("\ndescriptor | mean | median | best-direction median | pooled | Wilcoxon p")
for c in COLS:
    a = np.array([v["descriptors"][c] for v in arms.values()])
    b = np.maximum(a, 1 - a)
    p = stats.mannwhitneyu(pooled[c][0], pooled[c][1])[0] / (len(pooled[c][0]) * len(pooled[c][1]))
    print(
        f"{c} | {a.mean():.3f} | {np.median(a):.3f} | {np.median(b):.3f} | {p:.3f} | "
        f"{stats.wilcoxon(a - 0.5)[1]:.4f}"
    )

for key, label in (("pocket_rank", "defaults"), ("pocket_v3", "v3 settings")):
    rank = np.array([v[key] if key == "pocket_rank" else v[key][0] for v in arms.values()])
    print(
        f"pocket volume ranking, {label}: top-1 {np.mean(rank == 1):.2f}  "
        f"top-3 {np.mean(rank <= 3):.2f}  top-5 {np.mean(rank <= 5):.2f}  "
        f"median rank {np.median(rank):.0f}"
    )

lab, bg = Counter(), Counter()
for v in arms.values():
    lab.update(v["composition"])
    bg.update(v["background"])
nl, nb = sum(lab.values()), sum(bg.values())
print(f"\ncomposition: {nl} label vs {nb} background residues; Holm threshold {0.05 / 20:.4f}")
rows = []
for aa in sorted(set(lab) | set(bg)):
    odds, p = stats.fisher_exact([[lab[aa], nl - lab[aa]], [bg[aa], nb - bg[aa]]])
    rows.append((p, aa, odds))
for p, aa, odds in sorted(rows)[:5]:
    print(
        f"{aa} | {lab[aa]} | {100 * lab[aa] / nl:.1f} | {100 * bg[aa] / nb:.1f} | {odds:.2f} | {p:.3f}"
    )

loo = []
for held in arms:
    tl, tb = Counter(), Counter()
    for arm, v in arms.items():
        if arm != held:
            tl.update(v["composition"])
            tb.update(v["background"])
    n1, n0 = sum(tl.values()), sum(tb.values())
    prior = {
        a: np.log((tl[a] + 0.5) / (n1 + 10)) - np.log((tb[a] + 0.5) / (n0 + 10))
        for a in set(tl) | set(tb)
    }
    v = arms[held]
    expand = lambda d: [prior.get(a, 0.0) for a, n in d.items() for _ in range(n)]
    loo.append(auc(expand(v["composition"]), expand(v["background"])))
loo = np.array(loo)
print(
    f"\ncomposition prior, leave-one-arm-out: mean {loo.mean():.3f} median {np.median(loo):.3f} "
    f"Wilcoxon p {stats.wilcoxon(loo - 0.5)[1]:.3f}"
)
```

`graph.order` and `graph.degree` are the correct field names; `ResidueGraph` has no `residues`
attribute and `adjacency` is an alias for `weight`. `apo.pdb_id`, not `apo.entry`.
