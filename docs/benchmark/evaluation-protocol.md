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

Prevalence on the frozen arms runs 1.6 % to 11.0 %, a 6.79× span within five arms. AUC-ROC is
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

**The estimator stands; its stated reason does not, and the reason is corrected here.** This
paragraph used to justify the step estimator by Davis & Goadrich 2006
(doi:10.1145/1143844.1143874) on trapezoidal interpolation being optimistically biased in PR
space. That result is about **sparse operating points** and does not bite on continuous scores.
Measured against the population AUC-PR on these arms, the step estimator is the _more_
optimistically biased of the two — +18 % on KRAS to +64 % on myosin, against +10 % / +38 % for
the trapezoid. Keep `average_precision_step` because it is the scikit-learn convention and
because it never interpolates between thresholds a method did not produce, and **report the
bias rather than claiming the estimator removes it**. Both estimators are biased upward at this
prevalence; only a common estimator across methods makes the comparison fair, which is the
actual argument. Grouping at distinct thresholds means no within-tie ordering is ever
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

**Rewritten 2026-08-24 after the open item below was measured.** This section held two
columns, 0.66–0.71 and 0.96–0.97, and told the reader to measure the number between them
before quoting either. That number has now been measured and both columns are withdrawn.

| Arm                        | n pos | n neg | n_eff | **MDE AUC at n_eff** | withdrawn: Noether | withdrawn: one patch |
| -------------------------- | ----: | ----: | ----: | -------------------: | -----------------: | -------------------: |
| `kras_g12c_mandated`       |    16 |   130 |  4.88 |            **0.831** |              0.690 |                0.970 |
| `kras_g12c_corrected`      |    16 |   132 |  4.92 |            **0.830** |              0.690 |                0.970 |
| `bcr_abl1_mandated`        |    20 |   420 |  5.04 |            **0.822** |              0.664 |                0.959 |
| `bcr_abl1_corrected`       |    18 |   243 |  5.18 |            **0.819** |              0.675 |                0.963 |
| `cardiac_myosin_corrected` |    12 |   731 |  4.63 |            **0.835** |              0.709 |                0.958 |

80 % power, one-sided α = 0.05. One-sided is justified by design and not by convenience: §4
declares the decision rule upper-tail, and a method ranking allosteric residues _below_
background is a broken method rather than a competing finding.

The nine secondary arms measure n_eff 3.68–5.14 and MDE AUC **0.819–0.877**, so the answer is
the same across both sets: **this benchmark detects a strong ranking, AUC ≈ 0.85. Not a
near-perfect one at 0.96, and not a moderate one at 0.69.**

**Why both old columns were wrong.** The left one used Noether's rank-sum formula, which counts
a spatially contiguous label patch as 12 to 20 independent observations. It was labelled "an
upper bound on the evidence available", and that reading is not available: under the spatially
autocorrelated null §4 itself specifies, the unmatched rank-sum test's measured type-I rate is
**0.16–0.18**, not 0.05. A number from a test that does not hold its size is not a power
statement. The right column assumed one effective observation, and the repo's own suggested
way to check that — connected components of the label subgraph — returns 1 for **9 of the 14
label sets** across both benchmarks, so it cannot discriminate.

**How n_eff was measured, and why it is not a benchmark constant.** Variance inflation of
AUC-ROC itself: with iid scores `Var(AUC) = (n+ + n- + 1) / (12 n+ n-)`, so simulate the §4
null field on the frozen 4.5 Å contact graph, measure `Var(AUC)`, and solve for n_eff holding
n- fixed. The estimator returns the right answer on iid fields (16.29 for n+ = 16). Two
independent routes agree: graph heat-kernel smoothing of white noise gives n_eff 5.0–9.0 at
t = 1, and the size-corrected matched-null simulation of §4 lands at MDE AUC 0.79–0.84.

n_eff is **not** "the number of independent lobes in the label set", which is what this section
used to say. It is a joint property of the label geometry **and the correlation length of the
method's score field**, and on a fixed KRAS label set it moves 7.02 → 2.61 as λ runs 4 → 20 Å.
**Open item for the evaluation manifest:** ship the estimator (about 20 lines — Cholesky of
`exp(-d/λ)`, 4000 draws, one variance) and require every method to report its own λ and its own
n_eff beside its AUC. A single pinned n_eff would be a fiction.

**§6 and §4 are not the same procedure and must not be quoted for each other.** The table above
is a marginal rank-sum effect. §4's matched-patch test is a _partial_ effect given size,
topology, exposure and distance-to-source. Size-corrected to a common empirical 5 % level, the
matching costs 0.01–0.05 of MDE AUC (KRAS 0.792 → 0.841, ABL1 0.787 → 0.833, myosin
0.801 → 0.810). That is the price of asking "does propagation add something beyond geometry",
and it is the right question — but it is a different number from the one in this table.

Consequence, and state it in the report before the numbers rather than after them: three
targets is a small family, and **a negative result here is weak evidence of absence.**

## 7. Multiplicity, and what generalises

**Settled 2026-08-24. It is forced, not arguable.** The `generalisation` tier holds N = 5, so
its minimum attainable one-sided p is 2⁻⁵ = **0.03125**. Any correction to k ≥ 2 puts the
threshold at α/2 = 0.025 or below, and **0.03125 > 0.025**, so a corrected across-target test
could not reject at any effect size whatever. The project therefore admits **exactly one
confirmatory decision at full α**, and it is the across-target test on the `generalisation`
tier. The three primary arms are declared **supportive**, not confirmatory. ADR 0021 reached
the same place by a softer argument; this is the arithmetic that removes the choice.

A stratified permutation test across three targets generalises to **three targets**. It does
not generalise to proteins, to families, or to allostery. Say so in the report.

**What the primary set CAN claim, and the earlier text denied it one.** This section used to
say three arms "cannot make [a cross-target claim] at any α" because the minimum attainable
one-sided p over N targets is 2⁻ᴺ. The bound is right; the conclusion drawn from it was too
strong, and it is corrected here rather than left standing:

- The 2⁻ᴺ floor applies to a test **invariant to sign flips of N target-level effects** — the
  sign test — because its null distribution has 2ᴺ atoms. That is a property of that test.
- Combining the three per-arm matched-patch permutation p-values by **Fisher or Stouffer** is
  unbounded below: three arms at p = 0.05 each give Fisher 6.3e-3, Stouffer 2.2e-3. Power at
  N = 3 when each arm is a coin flip at α = 0.05 is 0.82 for Fisher, against **0.000** for the
  sign test at every effect size.
- What that licenses is narrower and must be labelled: Fisher and Stouffer test the
  **intersection null** — "no arm has signal" — so rejecting says _at least one_ arm has
  signal. It is **not** a generalisation claim. Report it as the global-null result it is.

**The threat that N does not fix.** Every generalisation reading assumes the targets are
exchangeable with a population. The three primary arms were **mandated** by the challenge. The
nine secondary arms survived twelve admission clauses over an RCSB full-text query, and
`secondary/README.md` §7 documents at length that the frame is non-random: interface sites
excluded by construction, non-catalytic targets excluded entirely, the frame a depositor's own
word. No N repairs a non-probability sampling frame. Generalisability here is at least as much
a **frame** problem as an N problem, and the report must say so beside the N argument.

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
