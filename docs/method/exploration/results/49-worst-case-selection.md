# 49 — Selecting for generalisation, not for the average

**Re-analysis, no new scoring.** Reads `experiments/2026-08-26-beats-distance/records.jsonl`
(276 records · 69 scorers × 4 `development` arms),
`experiments/2026-08-26-method-sweep/records.jsonl`
(6 480 records), `experiments/2026-08-26-stability-and-source/records.jsonl` (5 222 records)
and `docs/method/exploration/data/frozen-graph-profile.json`. Four arms: `mkp5`, `ptp1b`,
`hiv_rt`, `ns5b`. **Everything here is exploratory.** Nothing in it is a confirmatory claim.

Every earlier document in this directory selects on **mean AUC over four arms**. For a
generalisation claim that is the wrong loss. A scorer at 0.90 and 0.50 has the mean of a scorer
at 0.70 twice, and only the second generalises. This document re-ranks the whole battery under
worst-case objectives and asks what changes.

---

## 1. The result

**Three scorers, and only three, are Pareto-optimal in (mean AUC, worst-arm AUC).**

| Scorer | Family | Mean AUC | Worst arm | Which arm | Spread | mean \|ρ\| to distance |
| --- | --- | --- | --- | --- | --- | --- |
| `eigenvector_centrality` | classical | **0.7593** | 0.5639 | `ptp1b` | 0.334 | 0.431 |
| `gnm_fluctuation` | classical | 0.7505 | 0.6390 | `ptp1b` | 0.205 | 0.589 |
| `betweenness_centrality` | classical | 0.6938 | **0.6509** | `ns5b` | **0.068** | 0.505 |

**The trade is cheap in one direction and expensive in the other.** Moving from
`eigenvector_centrality` to `gnm_fluctuation` costs **0.0089** of mean AUC and buys **0.0751**
of worst-arm AUC — an 8:1 exchange. Moving on to `betweenness_centrality` costs a further
0.0566 of mean and buys only 0.0119 more of the floor.

**So the answer to "which scorer wins under generalisation" is `gnm_fluctuation`, and the
answer changes the winner** — the repository's incumbent by mean AUC is `eigenvector_centrality`,
which has the *tenth* worst-arm score in the battery.

**And the honest caveat is bigger than the finding.** Section 4 puts the switch through a
leave-one-arm-out test. **Selecting on the worst arm does not improve the held-out worst arm**
(0.5632 against 0.5639) and costs 0.058 of held-out mean. At n = 4 the worst-case objective is
estimated from a single number per scorer, and that number does not transfer.

---

## 2. Four objectives, four rankings

`spread` is max − min; `max regret` is, per arm, the best AUC any of the 69 scorers reached on
that arm minus this scorer's, taken at its worst arm. Top 15 by each, with the other three
columns carried along.

**By mean AUC** (the incumbent objective)

| # | Scorer | Mean | Min | Spread | Max regret |
| --- | --- | --- | --- | --- | --- |
| 1 | `eigenvector_centrality` | **0.759** | 0.564 | 0.334 | 0.251 |
| 2 | `gnm_fluctuation` | 0.750 | 0.639 | 0.205 | **0.176** |
| 3 | `effective_resistance_to_source` | 0.715 | 0.579 | 0.311 | 0.312 |
| 4 | `source_conditioned_betweenness` | 0.709 | 0.608 | 0.191 | 0.291 |
| 5 | `katz_centrality` | 0.708 | 0.592 | 0.220 | 0.340 |
| 6 | `gnm_entropy_response` | 0.704 | 0.542 | 0.316 | 0.304 |
| 7 | `alps_spectral_response` | 0.697 | 0.592 | 0.221 | 0.223 |
| 8 | `betweenness_centrality` | 0.694 | **0.651** | **0.068** | 0.247 |
| 9 | `subgraph_centrality` | 0.694 | 0.563 | 0.217 | 0.369 |
| 10 | `degree` ≡ `contact_number` | 0.692 | 0.584 | 0.186 | 0.349 |
| 12 | `sequence_distance_from_source_negated` | 0.690 | 0.518 | 0.341 | 0.380 |
| 13 | `stiff_corridor_to_source` | 0.684 | 0.651 | 0.105 | 0.280 |
| 14 | `gnm_cross_correlation` | 0.680 | 0.471 | 0.372 | 0.344 |
| 15 | `closeness_centrality` | 0.678 | 0.555 | 0.341 | 0.343 |

**By worst-arm AUC**

| # | Scorer | Min | Mean | Rank by mean |
| --- | --- | --- | --- | --- |
| 1 | `betweenness_centrality` | **0.6509** | 0.694 | 8 |
| 2 | `stiff_corridor_to_source` | 0.6505 | 0.684 | 13 |
| 3 | `gnm_fluctuation` | 0.6390 | 0.750 | 2 |
| 4 | `source_conditioned_betweenness` | 0.6076 | 0.709 | 4 |
| 5 | `alps_spectral_response` | 0.5919 | 0.697 | 7 |
| 6 | `katz_centrality` | 0.5917 | 0.708 | 5 |
| 7 | `degree` ≡ `contact_number` | 0.5836 | 0.692 | 10 |
| 9 | `effective_resistance_to_source` | 0.5791 | 0.715 | 3 |
| 10 | `eigenvector_centrality` | 0.5639 | **0.759** | **1** |
| 11 | `subgraph_centrality` | 0.5632 | 0.694 | 9 |
| 12 | `core_number` | 0.5560 | 0.575 | 30 |
| 13 | `closeness_centrality` | 0.5552 | 0.678 | 15 |
| 14 | `local_contact_order` | 0.5458 | 0.670 | 18 |
| 15 | `gnm_entropy_response` | 0.5415 | 0.704 | 6 |

**By minimax regret** (lower is better)

| # | Scorer | Max regret | Mean | Min |
| --- | --- | --- | --- | --- |
| 1 | `gnm_fluctuation` | **0.176** | 0.750 | 0.639 |
| 2 | `alps_spectral_response` | 0.223 | 0.697 | 0.592 |
| 3 | `betweenness_centrality` | 0.247 | 0.694 | 0.651 |
| 4 | `eigenvector_centrality` | 0.251 | 0.759 | 0.564 |
| 5 | `stiff_corridor_to_source` | 0.280 | 0.684 | 0.651 |
| 6 | `source_conditioned_betweenness` | 0.291 | 0.709 | 0.608 |
| 7 | `gnm_entropy_response` | 0.304 | 0.704 | 0.542 |
| 8 | `local_contact_order` | 0.304 | 0.670 | 0.546 |
| 9 | `effective_resistance_to_source` | 0.312 | 0.715 | 0.579 |
| 10 | `katz_centrality` | 0.340 | 0.708 | 0.592 |
| 11 | `closeness_centrality` | 0.343 | 0.678 | 0.555 |
| 12 | `gnm_cross_correlation` | 0.344 | 0.680 | 0.471 |
| 13 | `contact_number` | 0.349 | 0.692 | 0.584 |
| 14 | `degree` | 0.349 | 0.692 | 0.584 |
| 15 | `core_number` | 0.356 | 0.575 | 0.556 |

**By smallest between-arm spread** — listed in full because it is a deliverable, and read with
the caveat under it, not without

| # | Scorer | Spread | Mean | Min |
| --- | --- | --- | --- | --- |
| 1 | `bottleneck_to_source` | **0.0000** | 0.500 | 0.500 |
| 2 | `symmetry_dark_overlap` | **0.0000** | 0.500 | 0.500 |
| 3 | `core_number` | 0.0491 | 0.575 | 0.556 |
| 4 | `betweenness_centrality` | 0.0680 | 0.694 | 0.651 |
| 5 | `degenerate_mixing_weight` | 0.0744 | 0.481 | 0.426 |
| 6 | `essa_perturbation` | 0.1005 | 0.294 | 0.248 |
| 7 | `soft_corridor_to_source` | 0.1052 | 0.316 | 0.244 |
| 8 | `stiff_corridor_to_source` | 0.1052 | 0.684 | 0.651 |
| 9 | `protrusion_index` | 0.1453 | 0.347 | 0.266 |
| 10 | `clustering_coefficient` | 0.1647 | 0.334 | 0.279 |
| 11 | `connectivity_eigencentrality` | 0.1842 | 0.578 | 0.472 |
| 12 | `min_vertex_cut_to_source` | 0.1862 | 0.308 | 0.230 |
| 13 | `contact_number` | 0.1862 | 0.692 | 0.584 |
| 14 | `degree` | 0.1862 | 0.692 | 0.584 |
| 15 | `source_conditioned_betweenness` | 0.1909 | 0.709 | 0.608 |

**Ten of those fifteen have a mean AUC at or below 0.58, and the objective must not be used
alone.** The two smallest spreads are exactly 0.0000 and belong to `bottleneck_to_source` and
`symmetry_dark_overlap`, both of which return a **constant** score and therefore AUC 0.5000 on
all four arms. `degenerate_mixing_weight` is third at 0.0744 and
is constant on three arms. This is document 45's `random`-source lesson in a second setting:
**low between-arm variance is a symptom of carrying no signal as often as it is a symptom of
carrying robust signal.** Spread is readable only jointly with level, and it is reported here
for completeness, not as a selection rule.

The same degeneracy contaminates the min-AUC ranking more quietly: a constant scorer sits at
**rank 18 of 69** by worst arm. It is not on the Pareto frontier — `betweenness_centrality`
dominates it at (0.694, 0.651) — which is the argument for reading the frontier rather than
the min-AUC column.

### Rank disagreement

Kendall τ‑b over all 69 scorers, every objective oriented so that higher is better:

| | mean | min | −spread | −regret |
| --- | --- | --- | --- | --- |
| **mean** | 1 | **+0.574** | +0.113 | +0.627 |
| **min** | | 1 | +0.510 | **+0.853** |
| **−spread** | | | 1 | +0.397 |
| **−regret** | | | | 1 |

**Mean and min agree at the top and disagree in the middle.** The top-15 sets share 13 of 15
members, but the median absolute rank change across the whole battery is **9 positions** and the
maximum is 35. Minimax regret is very nearly the min-AUC ranking (τ = 0.853) and adds little.

The large movers are informative. Switching from mean to min **demotes** the scorers that are
excellent somewhere and broken somewhere else — `normalised_anm_response` 34 → 65 (mean 0.554,
min 0.117), `gnm_transfer_entropy_net` 43 → 66 (0.528, 0.117), `regularised_laplacian_kernel`
37 → 59, `szegedy_quantum_pagerank` 31 → 53 — and **promotes** the scorers that are uniformly
mediocre, including the constants. That asymmetry is the objective working as designed; it is
also why it needs a level floor.

**No interval is quoted on any of these rankings.** A bootstrap over four arms resamples four
numbers, and the resulting interval on a minimum would be a statement about which of four arms
was drawn, not about the scorer. The rank order is reported as a point estimate and read as
exploratory.

---

## 3. The Pareto frontier

Frontier size is **3 of 69**. The full list is §1. Two facts about it:

- **All three are classical.** No quantum observable is Pareto-optimal on either axis. The best
  quantum scorer by worst arm is `connectivity_eigencentrality` at 0.472, below chance-adjacent
  and 0.179 under the frontier.
- **The frontier is short because the two axes are strongly aligned in this battery**
  (τ = 0.574). The interesting scorers are the ones that break the alignment, and there are
  three of them.

`stiff_corridor_to_source` (0.684, 0.6505) is worth naming even though it misses the frontier
by 0.0004 of worst-arm AUC against `betweenness_centrality`. It is the scorer document 46 puts
in the distance-orthogonal quadrant at |ρ| = 0.057, and on the three-axis reading of §8 it is
the only candidate that is simultaneously high-floor and not a distance score.

---

## 4. Does selecting on the worst case actually generalise? Measured, and no

The four objectives above are all computed on the same four arms they rank. That is selection
on the test set. The cheap correction available at n = 4 is leave-one-arm-out: choose the
scorer that maximises the objective on three arms, then read its AUC on the fourth.

| Held out | Chosen by mean-of-3 | AUC | Chosen by min-of-3 | AUC | Chosen by regret-of-3 | AUC |
| --- | --- | --- | --- | --- | --- | --- |
| `mkp5` | `gnm_fluctuation` | 0.7549 | `stiff_corridor_to_source` | 0.6505 | `gnm_fluctuation` | 0.7549 |
| `ptp1b` | `eigenvector_centrality` | 0.5639 | `eigenvector_centrality` | 0.5639 | `gnm_fluctuation` | 0.6390 |
| `hiv_rt` | `eigenvector_centrality` | 0.7558 | `subgraph_centrality` | 0.5632 | `subgraph_centrality` | 0.5632 |
| `ns5b` | `effective_resistance_to_source` | 0.5864 | `betweenness_centrality` | 0.6509 | `source_conditioned_betweenness` | 0.6076 |

| Selection objective | Held-out mean | Held-out worst |
| --- | --- | --- |
| mean-of-3 | **0.6653** | 0.5639 |
| min-of-3 | 0.6071 | 0.5632 |
| regret-of-3 | 0.6412 | 0.5632 |

**Selecting on the worst arm buys nothing on the held-out worst arm** — 0.5632 against 0.5639,
a difference of 0.0007 in the wrong direction — and it costs **0.058** of held-out mean.
Minimax regret is intermediate on both and dominated by neither.

**Why, mechanically.** With four arms the min-of-3 criterion is the minimum of three numbers, so
it is decided by a single arm and inherits that arm's noise entirely. The mean-of-3 criterion
averages three. The worst-case objective is the right objective and it is the *least* estimable
one from this many arms; those two statements are not in conflict, and only the second is a
statement about our data.

**Four folds is four.** This table is the most decision-relevant thing in the document and it
rests on four selections. It is a warning, not a refutation of worst-case selection in general.

---

## 5. Where the variance in the sweep actually lives

**Method.** Exact orthogonal sums-of-squares on the **balanced sub-design** of the method sweep:
8 graphs × 54 scorers × 3 core confound-removal forms × 4 arms = **5 184** of the 6 480 records.
The two extra forms (`binned_median`, `gaussian_kernel`) ran on 3 graphs only, so the full set
is unbalanced in graph × detrend and its sums of squares would be order-dependent. On the
balanced block every main effect and interaction is orthogonal and the shares are unambiguous.

**Why sums of squares and not a random-effects fit.** There is exactly one observation per cell,
so there is no pure-error term. A variance-components fit would be identified only by assuming
the highest-order interaction away — assuming, rather than measuring, the very quantity in
question. The SS decomposition assumes nothing; the four-way interaction is the residual and is
reported as a component.

`SS_total` = 249.302 over 5 184 cells; var(AUC) = 0.0481, sd = 0.219.

| Component | SS | Share | df | Mean square |
| --- | --- | --- | --- | --- |
| `scorer` | 84.617 | **33.94 %** | 53 | 1.597 |
| `arm × scorer` | 67.947 | **27.26 %** | 159 | 0.427 |
| `arm × scorer × detrend` | 34.581 | 13.87 % | 318 | 0.109 |
| `arm × detrend` | 28.085 | 11.27 % | 6 | **4.681** |
| `arm × scorer × graph` | 13.032 | 5.23 % | 1 113 | 0.012 |
| `scorer × detrend` | 6.727 | 2.70 % | 106 | 0.063 |
| `scorer × graph` | 4.245 | 1.70 % | 371 | 0.011 |
| **`arm`** | **2.873** | **1.15 %** | 3 | 0.958 |
| `detrend` | 2.648 | 1.06 % | 2 | 1.324 |
| `arm × scorer × graph × detrend` (residual) | 2.174 | 0.87 % | 2 226 | 0.001 |
| `arm × graph` | 1.316 | 0.53 % | 21 | 0.063 |
| `scorer × graph × detrend` | 0.442 | 0.18 % | 742 | 0.001 |
| **`graph`** | **0.417** | **0.17 %** | 7 | 0.060 |
| `arm × graph × detrend` | 0.167 | 0.07 % | 42 | 0.004 |
| `graph × detrend` | 0.031 | 0.01 % | 14 | 0.002 |

**The stated hypothesis is half right, and the half that is wrong is the interesting half.**

- **As a main effect the arm is nearly absent: 1.15 %.** The four arms have almost the same
  *average* AUC over the battery — 0.554, 0.531, 0.517, 0.489.
- **Every arm-linked term together is 60.3 % of the variance**, against 39.7 % for all
  method-choice terms that do not involve the arm. So the arm dominates, but it does so
  **entirely through interactions**, not through a level shift.
- **`arm × scorer` alone is 27.3 %, which is 160 × the graph main effect.** Which scorer is good
  is a property of the arm, not of the battery. This is §6 in ANOVA form, and the two views
  agree.
- **By mean square the largest effect in the whole design is `arm × detrend` at 4.68**, three
  times the scorer main effect, on 6 degrees of freedom.

**That last row has a mechanism, and it explains the small arm main effect.** Per-arm mean AUC
over the 54 scorers, by confound-removal form:

| Detrend | `mkp5` | `ptp1b` | `hiv_rt` | `ns5b` |
| --- | --- | --- | --- | --- |
| `raw` | 0.635 | 0.453 | **0.674** | 0.446 |
| `exponential` | 0.489 | **0.596** | 0.372 | 0.532 |
| `binned_rank` | 0.538 | 0.543 | 0.504 | 0.488 |

**The ordering of the arms reverses under detrending.** On raw scores `mkp5` and `hiv_rt` are
the easy arms; remove the distance trend and they become the hard ones and `ptp1b` and `ns5b`
become the easy ones. Averaging over the three forms cancels most of the arm main effect into
the interaction, which is why the `arm` row reads 1.15 %.

The cause is visible in one line of the battery. `distance_from_source_negated` scores
**0.7985 / 0.3333 / 0.9321 / 0.2608** on the four arms. On `mkp5` and `hiv_rt` the labelled site
sits near the active site and any score carrying distance wins; on `ptp1b` and `ns5b` it sits
far and the *inverted* distance is the strong control (document 40's finding, and the same
inversion the primary set shows in `experiments/REGISTRY.md`).

**Sensitivity, full 6 480 records**, main-effects OLS with sequential SS in the order arm,
scorer, graph, detrend: arm 1.32 %, scorer 35.27 %, graph 0.16 %, detrend 0.89 %, residual
62.36 % — the residual there holds every interaction, including the two large arm terms above.
The shares agree with the balanced block to within a percentage point.

---

## 6. Is difficulty a property of the arm, or of the arm–scorer pair?

Spearman correlation of the 69 scorers' AUC between each pair of arms.

| | `mkp5` | `ptp1b` | `hiv_rt` | `ns5b` |
| --- | --- | --- | --- | --- |
| **`mkp5`** | 1.000 | −0.123 | **+0.597** | +0.024 |
| **`ptp1b`** | −0.123 | 1.000 | −0.319 | **+0.678** |
| **`hiv_rt`** | +0.597 | −0.319 | 1.000 | **−0.428** |
| **`ns5b`** | +0.024 | +0.678 | −0.428 | 1.000 |

Mean off-diagonal **+0.071**, range **−0.428 to +0.678**.

**The orderings differ, so per-protein adaptation is worth something in principle.** But the
structure is not noise: the four arms fall into **two clusters of two**, `{mkp5, hiv_rt}` at
+0.597 and `{ptp1b, ns5b}` at +0.678, with a mean **between**-cluster correlation of **−0.212**.
Within a cluster the same scorers work; across clusters they anti-correlate.

**The clusters are the near/far split of §5.** `{mkp5, hiv_rt}` are the arms where the distance
baseline reads 0.80 and 0.93; `{ptp1b, ns5b}` are the arms where it reads 0.33 and 0.26. Two
clusters from four arms could arise by chance, but this one has an independent explanation and
it is the same explanation the detrend interaction has.

**Powered, but not by as much as 69 suggests.** These correlations are over 69 scorers, not over
4 arms, so the n = 4 significance floor does not apply and the p values are real: `ptp1b`–`ns5b`
p = 1.6 × 10⁻¹⁰, `mkp5`–`hiv_rt` p = 6.3 × 10⁻⁸, `hiv_rt`–`ns5b` p = 2.4 × 10⁻⁴. The 69
scorers
are **not** independent: only **66 distinct four-arm profiles** exist among them
(`degree` ≡ `contact_number`, `hop_distance_from_source_negated` ≡ `ohm_path_probability`,
`bottleneck_to_source` ≡ `symmetry_dark_overlap`, both constant), and the battery contains whole
families of near-duplicates that document 41 prices at **8.86–10.58 effective directions** for
the sweep. Read the p values as ordering evidence, not as calibrated tail probabilities. The
4 × 4 arm correlation matrix has eigenvalues 2.015, 1.365, 0.452, 0.168 — a participation ratio
of **2.60**, so the four arms span about two and a half independent directions of scorer
preference, consistent with the two clusters.

**Conclusion: difficulty is a property of the pair, and the pair term is structured.** Not "each
protein needs its own method" but "there appear to be two regimes, and which regime a protein is
in is defined by where its site sits relative to the active site — which is exactly the thing a
blind method does not know."

---

## 7. What a perfect oracle would be worth

The virtual best picks the best of the 69 scorers separately on each arm. The single best picks
one scorer by mean and uses it everywhere. The gap is the maximum possible payoff from
per-protein adaptation.

| Pool | Oracle mean AUC | Single best by mean | Gap | Oracle worst arm |
| --- | --- | --- | --- | --- |
| all 69 | **0.8757** | 0.7593 (`eigenvector_centrality`) | **+0.1164** | 0.8152 |
| mean \|ρ to distance\| < 0.45 (26 scorers) | 0.8348 | 0.7593 (`eigenvector_centrality`) | **+0.0755** | 0.7245 |
| max \|ρ to distance\| < 0.45 (11 scorers) | 0.7435 | 0.7038 (`gnm_entropy_response`) | +0.0397 | 0.6525 |

The filter convention is document 46's: the mean over arms of |ρ to negated distance|. The
per-arm-maximum variant is the stricter sensitivity in the third row. Constant scorers have an
undefined ρ and are excluded by both.

Per-arm winners, unfiltered:

| Arm | Winner | AUC | Its mean AUC | Label-blind p95 / p99 (doc 41) |
| --- | --- | --- | --- | --- |
| `mkp5` | `gnm_entropy_response` | 0.8575 | 0.704 | 0.780 / 0.845 |
| `ptp1b` | `strain_versus_diffusion` | 0.8152 | **0.481** | 0.773 / 0.871 |
| `hiv_rt` | `distance_from_source_negated` | 0.9321 | 0.581 | 0.794 / 0.852 |
| `ns5b` | `eigenvector_centrality` | 0.8981 | 0.759 | 0.731 / 0.798 |

**Read the gap as an upper bound that is mostly selection noise, not as a payoff.** The virtual
best is a per-arm best-of-69 chosen after seeing the labels, which is precisely the quantity
`41-selection-and-power.md` exists to price — **but not by its best-of-V rows**, which select one
variant by its *mean* over arms. A per-arm oracle is a different and larger selection quantity:
under the label-blind null it is the mean of four independent per-arm maxima, and the median of a
maximum of V draws sits at quantile 0.5^(1/V) of the per-arm distribution. At face value V = 69
that is about the per-arm p99, whose mean over the four arms is **0.84**; at document 41's
measured effective V ≈ 10 it is about p93, giving roughly **0.76**. **So the oracle's own null is
an interval, 0.76 to 0.84, and the observed 0.876 sits just above its top.** Headroom over the
selection-inflated null is on the order of **+0.03**, not +0.116.

Three of the four per-arm winners do clear their own arm's label-blind p99, so the gap is not
*entirely* selection noise. But no part of it is available to a blind method, and the correct
summary is "at most +0.116 against a fixed choice, about +0.03 against a null that selects the
same way, and unreachable either way".

**Two of the four winners disqualify themselves on inspection.** `hiv_rt`'s winner is
`distance_from_source_negated` — the geometry-only control, at ρ = 0.994 to itself. `ptp1b`'s
winner is `strain_versus_diffusion`, which scores 0.279 on `mkp5` and 0.115 on `hiv_rt`: it is
close to an anti-distance score, and it wins on `ptp1b` for the same reason the distance score
wins on `hiv_rt`. **The oracle's gain is mostly the gain from knowing, per protein, whether to
use distance or its inverse — and that is the one bit of information a blind method cannot
have.** Restricting to decorrelated scorers costs 35 % of the gap (0.116 → 0.076) and the strict
restriction costs 66 % (→ 0.040), which quantifies the same statement.

---

## 8. Three axes: accuracy floor, distance orthogonality, stability

Stability is the mean `rho_to_baseline` over every `coord|1.0|*` record — 1.0 Å isotropic
coordinate jitter, 5 seeds × 4 arms — which is document 44's convention and reproduces its
quoted values (`degree` 0.878, `eigenvector_centrality` 0.827,
`distance_from_source_negated` 0.978). `jacc` is the top-5 Jaccard under the same perturbation.

**Coverage is 33 of 69 scorers**, because `2026-08-26-stability-and-source` ran the 30-scorer
complete-coverage subset plus three others; **32 of those 33 have a defined stability value**,
because one constant scorer's rank correlation to its own baseline is undefined. Rows
without a record read `not measured` and are
neither dropped nor imputed. Per-arm record counts differ (`mkp5` 1 388, `ptp1b` 1 388,
`hiv_rt` 1 322, `ns5b` 1 124) because `ns5b`'s three-residue source truncates its source
leave-one-out arm.

Top 20 by worst-arm AUC:

| Scorer | Family | Mean | Min | mean \|ρ\| | Stability @1.0 Å | Top-5 Jaccard |
| --- | --- | --- | --- | --- | --- | --- |
| `betweenness_centrality` | classical | 0.694 | **0.651** | 0.505 | 0.829 | 0.264 |
| `stiff_corridor_to_source` | classical | 0.684 | 0.651 | **0.057** | not measured | — |
| `gnm_fluctuation` | classical | 0.750 | 0.639 | 0.589 | **0.921** | 0.304 |
| `source_conditioned_betweenness` | classical | 0.709 | 0.608 | 0.574 | not measured | — |
| `alps_spectral_response` | classical | 0.697 | 0.592 | 0.615 | not measured | — |
| `katz_centrality` | classical | 0.708 | 0.592 | 0.425 | not measured | — |
| `contact_number` | classical | 0.692 | 0.584 | 0.376 | not measured | — |
| `degree` | classical | 0.692 | 0.584 | 0.376 | 0.878 | 0.188 |
| `effective_resistance_to_source` | classical | 0.715 | 0.579 | 0.790 | not measured | — |
| `eigenvector_centrality` | classical | **0.759** | 0.564 | 0.431 | 0.827 | 0.211 |
| `subgraph_centrality` | classical | 0.694 | 0.563 | 0.361 | not measured | — |
| `core_number` | classical | 0.575 | 0.556 | 0.279 | not measured | — |
| `closeness_centrality` | classical | 0.678 | 0.555 | 0.732 | not measured | — |
| `local_contact_order` | classical | 0.670 | 0.546 | 0.406 | not measured | — |
| `gnm_entropy_response` | classical | 0.704 | 0.542 | 0.257 | not measured | — |
| `distance_to_centroid_negated` | classical | 0.610 | 0.520 | 0.714 | not measured | — |
| `sequence_distance_from_source_negated` | classical | 0.690 | 0.518 | 0.422 | not measured | — |
| `bottleneck_to_source` | classical | 0.500 | 0.500 | constant | not measured | — |
| `symmetry_dark_overlap` | quantum | 0.500 | 0.500 | constant | not measured | 1.000 |
| `connectivity_eigencentrality` | quantum | 0.578 | 0.472 | 0.452 | 0.569 | 0.039 |

**Seventeen of the top twenty are classical, and the three that are not are the two constants
and one quantum scorer below chance on its worst arm.**

**No scorer is good on all three axes.** Requiring min AUC ≥ 0.60, mean |ρ| < 0.45 and stability
≥ 0.80 returns **zero** of the 32 measurable scorers. Relaxing the floor to min AUC ≥ 0.55
returns exactly two, `degree` (0.692 / 0.584 / 0.376 / 0.878) and `eigenvector_centrality`
(0.759 / 0.564 / 0.431 / 0.827), and neither has a worst arm above 0.60.

**The coupling document 44 found is confirmed here on a wider set and refined.** Over the 32
scorers with both measurements, Spearman(stability, mean |ρ| to distance) = **+0.599**
(p = 2.9 × 10⁻⁴); within the 24 quantum scorers **+0.881** (p = 1.3 × 10⁻⁸); within the 8
classical **+0.690** (p = 0.058). These are over scorers, not arms, so the significance floor of
§9 does not apply — but the hypothesis followed the data in document 44 and the p values are
uncorrected, so they are exploratory.

**The new number is the one that is near zero.** Spearman(stability, worst-arm AUC) = **−0.007**
(p = 0.97), against Spearman(stability, mean AUC) = **+0.354** (p = 0.047). **Stability predicts
average accuracy weakly and worst-case accuracy not at all.** A stable score is a smooth
function of coordinates; smoothness is what distance has; and distance is exactly the component
that is excellent on two arms and inverted on the other two. So the axis that document 44 treats
as a proxy for robustness is silent about the robustness this document is asking for.

---

## 9. Can an apo-only descriptor tell us which arm is hard?

If it could, the two-cluster structure of §6 would be detectable without a label and the oracle
gap of §7 would be partly reachable. **Screened and null.**

K = **37** numeric descriptors from `frozen-graph-profile.json`, each Spearman-correlated over
the four arms against arm difficulty (mean AUC over the 69 scorers: `mkp5` 0.626, `ptp1b` 0.464,
`hiv_rt` 0.659, `ns5b` 0.463).

**Expected number of perfect orderings by chance = K × 2/24 = 3.08. Observed = 1**
(`confounders.mean_relative_solvent_accessibility`, ρ = +1). Fewer than chance would give.

**With n = 4 the minimum attainable two-sided Spearman p is 0.083, so no descriptor in this
screen can reach significance at any effect size.** The screen is reported to show that it was
run and came back empty, not because it found anything. It also does not exclude a two-group
separator, which n = 4 cannot distinguish from a monotone ordering.

---

## 10. What is supported and what is not

**Supported by the numbers here.**

- The Pareto frontier of (mean, worst) contains exactly three scorers and the mean-optimal
  choice is not on the worst-case end of it.
- The mean → worst switch is cheap once (0.0089 for 0.0751) and expensive after that.
- The arm accounts for 60.3 % of the sweep's AUC variance through interactions and 1.15 % as a
  main effect; the graph accounts for 0.17 %.
- Scorer orderings differ between arms and cluster into two groups that coincide with the sign
  of the distance baseline.
- A per-arm oracle would gain at most +0.116 mean AUC, and at most +0.076 among scorers that
  are not distance.
- Nothing in the measurable battery is simultaneously high-floor, distance-orthogonal and
  stable.

**Not supported, and stated as such.**

- **That switching the selection objective to the worst case improves generalisation.** §4
  measures it and finds it does not, on four folds.
- **That `gnm_fluctuation` is better than `eigenvector_centrality`.** It is better on this
  benchmark under this objective, chosen after seeing all four arms. Neither rejects the
  matched-patch null on more than one arm (`40-method-sweep.md`), and `46-beats-distance.md`
  shows nothing in this battery beats the distance baseline more often than chance. **A better
  ranking among methods that do not clear their null is a better ranking among methods that do
  not clear their null.**
- **Any p value on a quantity computed over four arms.** The floor is 0.083.
- **That the two clusters are real.** Two clusters from four arms, with a post-hoc mechanism.
  It is a hypothesis for the `generalisation` tier to test, and it is the single most
  falsifiable statement in this document.

**Everything above is exploratory.** No hypothesis here was pre-registered, the objectives were
compared after the records existed, and the multiplicity of comparing four objectives over 69
scorers is not corrected anywhere.

---

## 11. Reproducing this

Every number is a re-analysis of committed records; no scoring was re-run and no frozen value
was touched. The four development arms only. **No script is committed for this document**,
because it added no experiment — each section instead names the file, the field and the
aggregation it used (§5 the balanced 5 184-record block, §8 the mean `rho_to_baseline` over
`coord|1.0|*`, §7 the mean-over-arms |ρ| filter), which is what a reader needs to rebuild
it. The two anchors quoted in the brief reproduce
exactly from `experiments/2026-08-26-beats-distance/records.jsonl`:
`eigenvector_centrality` mean 0.7593 / min 0.5639, `betweenness_centrality` 0.6938 / 0.6509,
which is the gate this analysis was run behind.

---

## 12. What this changes

1. **Report the worst arm next to the mean, everywhere.** It costs one column and it is the
   column a generalisation claim is actually about. Documents 40 and 45 already carry a
   worst-arm column; documents that quote a mean without one should gain it.

2. **Do not switch the selection rule to the worst arm.** §4 is the reason: at n = 4 the
   worst-case objective is estimated from one number per scorer and does not transfer, and it
   costs 0.058 of held-out mean. The defensible position is to **select on the mean and report
   the minimum**, then treat any scorer with a worst arm below ~0.60 as unproven rather than
   as a winner.

3. **If a single scorer has to be frozen for a generalisation claim, `gnm_fluctuation` is the
   better-argued choice than `eigenvector_centrality`** — 8:1 in the trade, and it is the
   minimax-regret leader as well. This is an argument for an ADR, not a decision this document
   may take. Under ADR 0012 a hyperparameter chosen on `development` is frozen before the
   `generalisation` tier opens, and this comparison is a hyperparameter choice.

4. **Stop treating stability as evidence for robustness.** Spearman(stability, worst-arm AUC) =
   −0.007. Document 44's §7 tension is sharper than it looked: stability tracks the distance
   component (+0.599 pooled, +0.881 within quantum) and the distance component is precisely what
   reverses between the two arm clusters. Stability belongs in the §4.2 noise-resilience
   deliverable, where it answers the question that was asked; it does not belong in an argument
   about generalisation.

5. **The graph axis can be closed as a source of variance.** 0.17 % of the sweep's AUC variance
   on 7 degrees of freedom, against 27.3 % for `arm × scorer`. Effort spent on graph
   construction is effort spent on the smallest term in the design. (Scope: AUC-ROC. The
   registry records that on AUC-PR the graph axis moves 3.5× further in relative terms.)

6. **The next experiment is not another scorer.** §6 and §7 together say the reachable ceiling
   is set by a single unknown bit per protein — whether the labelled site is near the active
   site or far from it. A label-blind estimator of that bit would convert part of the +0.116
   oracle gap into a real gain, and nothing in `docs/method/review/14-distance-confound.md`'s
   surviving descriptor list has been tested for it. That is a sharper target than adding a
   70th scorer to the battery.
