# The evaluation protocol — DRAFT, not frozen

**Status: draft. Phase 1.6. Nothing here is pinned, and no method may be scored under it
yet.** This document holds the design that was written while the input layer was being built.
It lived inside `README.md` and inside `manifest.yaml` until 2026-08-24. That coupling meant
an unfinished null model blocked a finished input layer, so the two were separated.

The input layer answers **what** is scored: which structures, which residues, which labels,
which candidate set. It is frozen — see [`README.md`](README.md). This document answers
**how**. When it is finished it gets its own manifest and its own freeze date, and the
config below moves out of prose and into that file.

**Do not merge this back into the input manifest.** The two layers move at different rates.
The last time they shared one file, the freeze could not close.

---

## 1. What the challenge asks for

`CHALLENGE.md` §4.1: known distal regulatory residues must score **statistically
significantly higher** than (a) **random background residues** and (b) **non-functional
surface pockets**. Both negative classes are required. Only the first exists today.

The scored artifact is a **top-5 ranked residue list per target** (§5). The N × N
connectivity matrix is a deliverable but is not what accuracy is measured on.

## 2. Primary endpoint

**AUC-PR is the tested endpoint. AUC-ROC is reported beside it as the effect size.**

Prevalence on the frozen arms runs 1.6 % to 11.0 %, a 6.9× span within five arms. AUC-ROC is
prevalence-invariant and AUC-PR is not, so at this prevalence they answer different questions
and reporting only one hides the harder arms. Measured on the eleven-arm benchmark with
synthetic signal at fixed effect (d = 0.8, seed 0): ROC landed near 0.714 on all three
claim-bearing arms while PR spanned 0.290 / 0.208 / 0.069. The ROC number would let the
myosin arm look like the KRAS arm. Regenerate on the current five arms when the harness
exists; the conclusion follows from the prevalence span and does not depend on the values.

Testing both would count one experiment twice: the Mann-Whitney U statistic **is** AUC-ROC
rescaled, so it is one procedure and not two. Declare one confirmatory decision rule.

Two things move an AUC without any protocol appearing to change, so both must be pinned:

| Metric  | Estimator                                           | Tie rule                                |
| ------- | --------------------------------------------------- | --------------------------------------- |
| AUC-PR  | `average_precision_step` — AP = Σᵢ (Rᵢ − Rᵢ₋₁) · Pᵢ | evaluated only at distinct score values |
| AUC-ROC | rank-based Mann-Whitney                             | midrank                                 |

Trapezoidal interpolation of the PR curve is optimistically biased in PR space
(Davis & Goadrich 2006, doi:10.1145/1143844.1143874), and this prevalence range is exactly
where that bias lives. Grouping at distinct thresholds means no within-tie ordering is ever
used: without it, a method emitting coarse or integer-valued scores gets ranked by tie order
rather than by score. Midrank ROC ties are what makes `U / (n_pos · n_neg) == AUC-ROC` exact.

**Positive class:** `scoreable_label_residues`. **Negative class:** the candidate set minus
the positives. Neither is the whole chain.

## 3. Secondary endpoints

- **Precision@5** and **P(≥1 hit in top 5)**, both against the exact hypergeometric baseline
  on the candidate set. A top-5 list has to clear that bar before it means anything.
- The chance lines are recomputed from the freeze, never quoted from prose.

## 4. The null — matched-patch permutation

The rank-sum null is the wrong opponent. It asks "are these 16 residues higher than 130
random ones", and a connectivity method scores a contiguous buried patch highly whether or
not that patch is the site. The null must sample **patches that look like the observation**
and ask whether the true one stands out.

Draft matching rules, all of which need a calibration run before they may be used:

| Property   | Rule                                                                                        |
| ---------- | ------------------------------------------------------------------------------------------- |
| graph      | heavy atom, 4.5 Å — the same graph the input layer freezes                                  |
| size       | same number of residues as the scoreable set                                                |
| components | **match the observed component-size multiset**, not "connected"                             |
| exposure   | seed drawn below the median contact-degree quantile, plus a 20 % bound on patch mean degree |
| distance   | median, minimum and lower-quartile Cα distance to the source, each within 1.0 Å             |
| growth     | uniform contact frontier                                                                    |
| p-value    | upper tail, plus-one correction                                                             |

**Why components and not connectivity.** Measured on the current five arms, 4.5 Å heavy-atom
graph:

| Arm                        | component sizes |              |
| -------------------------- | --------------- | ------------ |
| `kras_g12c_mandated`       | [16]            | connected    |
| `kras_g12c_corrected`      | [16]            | connected    |
| `bcr_abl1_mandated`        | [20]            | connected    |
| `bcr_abl1_corrected`       | **[17, 1]**     | disconnected |
| `cardiac_myosin_corrected` | **[8, 4]**      | disconnected |

Two of five, and one of them is the myosin arm — the one with the least evidence to spare.
Sampling connected blobs against a two-lobed observation imposes a property the observation
lacks, which is anti-conservative. `bcr_abl1_corrected`'s singleton is `A:ILE521`. The myosin
split is not a stray residue: it is 8 residues in the 710–774 lobe against 4 in the 164–168
plus 666 lobe, so that arm is genuinely two-patch.

**Why the exposure bound.** Matching exposure at the seed alone left the burial confound half
controlled — measured 14.2 % median degree miss on KRAS.

### The calibration gate

A null that rejects nothing passes a type-I band perfectly, so the gate needs both ends:

1. **Type-I rate.** 1000 replicates of a **stochastic, site-uninformative, spatially
   autocorrelated** score at α = 0.05. Accept inside the exact central 95 % binomial
   prediction interval, [0.037, 0.064].
2. **Positive control.** A score built from the answer must **reject on every claim-bearing
   arm**. It is evaluation-side only and never touches the prediction path.

Distance-only and degree-only scores are **diagnostics on the matching, not the gate**: the
distance statistics match them by construction, and each yields one p-value per arm, which
cannot separate 0.05 from 0.15.

**Known limitation to disclose, not hide.** Drawing a fresh patch pool per replicate is
prohibitive, so the pool is drawn once per arm and shared. The replicates are therefore
conditionally independent given the pool, not independent, and the binomial interval is a
screen rather than a proof (ADR 0018).

## 5. The second negative class

Non-functional surface pockets need a geometric pocket detector. None is installed. Choosing
one after seeing method results would make it a hyperparameter — which detector, what surface
definition, how pockets merge, what is excluded — so the choice, its version and its full
configuration go into the evaluation manifest **before** any method is scored.

## 6. Power, honestly

A priori sensitivity analysis at the fixed n the input layer already froze. This is not
observed power: nothing has been measured yet.

| Arm                        | n pos | n neg | MDE AUC, residues independent | MDE AUC, one effective patch |
| -------------------------- | ----: | ----: | ----------------------------: | ---------------------------: |
| `kras_g12c_mandated`       |    16 |   130 |                         0.690 |                        0.970 |
| `kras_g12c_corrected`      |    16 |   132 |                         0.690 |                        0.970 |
| `bcr_abl1_mandated`        |    20 |   420 |                         0.664 |                        0.959 |
| `bcr_abl1_corrected`       |    18 |   243 |                         0.675 |                        0.963 |
| `cardiac_myosin_corrected` |    12 |   731 |                         0.709 |                        0.958 |

80 % power, one-sided α = 0.05. One-sided is justified by design and not by convenience: §4
declares the decision rule upper-tail, and a method ranking allosteric residues _below_
background is a broken method rather than a competing finding.

**The two columns are the whole problem.** The left one uses Noether's rank-sum formula and
counts a spatially contiguous label patch as 12 to 20 independent observations, which it is
not. It is an **upper bound on the evidence available**. The right one is the exact
single-observation case: under H0 one positive's rank is uniform on 1..n+1, so the number of
negatives scoring above it is Binomial(n, 1 − theta). It is the **floor**.

The truth sits between them, at the number of independent lobes in the label set. On myosin
the MDE runs 1.218 / 1.008 / 0.915 / 0.860 / 0.794 / 0.709 at 1 / 2 / 3 / 4 / 6 / 12 effective
observations. **Measure that number before quoting either column.** Note that Noether at one
observation returns 1.218 — above the range an AUC can take, and independent of n — which is
the formula evaluated outside its domain, saying nothing about these targets.

Consequence, and state it in the report before the numbers rather than after them: on the
pessimistic reading this benchmark detects only a near-perfect ranking, and three targets is
a small family. **A negative result here is weak evidence of absence.**

## 7. Multiplicity, and what generalises

Three arms carry claims (one corrected arm per disease area). Declare **one** confirmatory
decision rule across that family, corrected at α/3, and derive the family from the freeze
rather than counting by hand.

A stratified permutation test across three targets generalises to **three targets**. It does
not generalise to proteins, to families, or to allostery. Say so in the report.

**Where a generalisation claim can come from instead.** Three arms cannot make one at any α:
the minimum attainable one-sided p of a distribution-free one-sample test over N targets is
2^-N, and 2^-3 = 0.125. The secondary set's `generalisation` tier exists for this and holds
N = 5 (`secondary/README.md`). **Open item for Phase 1.6:** ADR 0021 argues that the
across-target test there should be declared at k = 1 and full α, because the per-target
tests are inputs to it rather than N confirmatory decisions. That is a change to the rule
above and is not settled here.

## 8. No tuning on this benchmark

Every hyperparameter — metric, Hamiltonian, cutoff, coarse-graining ratio — is chosen on the
secondary set's **`development`** tier and nowhere else (frozen 2026-08-24, N = 4). The
`generalisation` tier is not opened until the method is frozen, and the primary set is
scored once. That set must be disjoint from every primary target on accession, family,
homologous site and residue overlap (ADR 0012). Clause (xii) tests the first two of those
four; ADR 0021 §3 records why the other two are not tests and what was run by hand instead.
The frame is RCSB rather than the Allosteric Database, for reasons recorded in
`secondary/evidence/databases.md`. ASD curates the
myristoyl pocket twice, lists `1OPL` as a related complex, and holds an HRAS record carrying
4 of 5 KRAS labels past any identity dedup, so the disjointness has to be enforced rather
than assumed.

The frozen primary benchmark is scored **once**, with every choice already fixed.

## 9. Gate before any number is quotable

All three, together:

1. `allo benchmark verify` clean.
2. Decoy artifacts committed and their detector configuration frozen.
3. The patch null calibrated — type-I band **and** positive control.
