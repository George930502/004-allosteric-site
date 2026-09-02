# The screen: every graph, every scorer, every confound-removal form

**Ran 2026-08-26** on the secondary set's `development` tier and nowhere else (ADR 0012,
ADR 0021). Three runners, 7 692 scored records, 1 923 variants complete on all four arms.

**Read [`42-threats-and-confirmation.md`](42-threats-and-confirmation.md) first**, and
[`41-selection-and-power.md`](41-selection-and-power.md) before you quote any number below.
This file is the numbers. The other two are what the numbers mean.

**This is a screen. It selects. It does not confirm.**

---

## 1. What ran

Every record is one call to `allo.scoring.score_arm`. No runner computes its own AUC, its
own null or its own p-value.

| Runner                            | Design                                                         | Records | Complete variants |
| --------------------------------- | -------------------------------------------------------------- | ------- | ----------------- |
| `2026-08-26-method-sweep`         | 8 graphs × 54 scorers × 3–5 confound-removal forms              | 6 480   | 1 620             |
| `2026-08-26-fusion-probe`         | label-blind consensus × smoothing × top-5 assembly              | 972     | 243               |
| `2026-08-26-mechanism-probe`      | 4 cross-system mechanism signatures × 3 graphs × 5 forms        | 240     | 60                |
| **Total**                         |                                                                 | **7 692** | **1 923**       |

The 54 scorers divide into four registries: 30 `baselines`, 9 `coupling`, 4 `mechanism`,
11 `quantum`. Every scorer completed on all four arms. Nothing was refused for size,
because the largest development arm holds 553 residues and the dephasing solve admits 620.

The four arms and their chance lines, re-derived by the harness on every record:

| Arm      | Candidates | Positives | Prevalence | Chance recall@5 | Chance DCC (Å) |
| -------- | ---------- | --------- | ---------- | --------------- | -------------- |
| `mkp5`   | 136        | 11        | 0.081      | 0.0368          | 11.96          |
| `ptp1b`  | 287        | 11        | 0.038      | 0.0174          | 17.65          |
| `hiv_rt` | 534        | 16        | 0.030      | 0.0094          | 24.98          |
| `ns5b`   | 550        | 16        | 0.029      | 0.0091          | 23.38          |

---

## 2. The result that governs every other number here

**Zero of 1 923 complete variants reject the matched-patch null on all four arms.** Not at
α = 0.05, and not at the Holm-corrected 0.05/4.

The full distribution over the 1 923 complete variants, at α = 0.05:

| Arms rejecting | 0     | 1   | 2  | 3     | 4     |
| -------------- | ----- | --- | -- | ----- | ----- |
| Variants       | 1 338 | 492 | 93 | **0** | **0** |

At the Holm-corrected 0.05/4 the counts fall to 8 variants at two arms and none above.

This is the single most important line in the file. A method that rejects on two arms and
fails on two has not shown that it generalises. It has shown that two arms are easier than
two other arms, which the chance table above already says.

---

## 3. Leaders by mean AUC

Twenty of 1 923, ranked by the mean of `auc_roc` over the four arms. `rej` counts arms that
reject the matched-patch null at 0.05. `|ρ|` is the mean absolute rank correlation against
`distance_from_source_negated`.

| Graph                  | Scorer                    | Detrend           | mean AUC | min AUC | hits@5 | rej | min p  | \|ρ\| | DCC (Å) |
| ---------------------- | ------------------------- | ----------------- | -------- | ------- | ------ | --- | ------ | ----- | ------- |
| `evaluation_default`   | `eigenvector_centrality`  | `binned_median`   | **0.810** | 0.703  | 2      | 2   | 0.0137 | 0.00  | 18.7    |
| `evaluation_default`   | `eigenvector_centrality`  | `binned_rank`     | 0.805    | 0.701   | 3      | 2   | 0.0285 | 0.00  | 18.5    |
| `evaluation_default`   | `eigenvector_centrality`  | `gaussian_kernel` | 0.786    | 0.676   | 3      | 0   | 0.0568 | 0.00  | 14.8    |
| `heavy_exponential`    | `eigenvector_centrality`  | `binned_rank`     | 0.779    | 0.663   | **6**  | 1   | 0.0041 | 0.06  | 13.2    |
| `heavy_inverse_square` | `gnm_fluctuation`         | `binned_rank`     | 0.778    | 0.581   | 5      | 2   | 0.0034 | 0.06  | 13.9    |
| `heavy_inverse_square` | `gnm_fluctuation`         | `gaussian_kernel` | 0.776    | 0.724   | 3      | 1   | 0.0321 | 0.35  | 16.3    |
| `heavy_edge_class`     | `gnm_fluctuation`         | `binned_rank`     | 0.772    | 0.655   | 3      | 2   | 0.0121 | 0.04  | 14.6    |
| `heavy_exponential`    | `gnm_fluctuation`         | `binned_rank`     | 0.770    | 0.615   | 4      | 2   | 0.0081 | 0.05  | 15.0    |
| `evaluation_default`   | `gnm_fluctuation`         | `binned_rank`     | 0.767    | 0.625   | 4      | 2   | 0.0094 | 0.00  | 14.8    |
| `heavy_inverse_square` | consensus, cut 0.5, `pc1` | raw, no smoothing | 0.765    | 0.586   | 5      | 0   | 0.0625 | 0.58  | 14.6    |

**Read the top row against the ceiling, not against 0.5.** The label-blind ceiling is an
interval, because the screen's effective size is not its raw size
([`41-selection-and-power.md`](41-selection-and-power.md) §4). Measured on the finished screen,
1 620 variants hold **8.86 independent directions on `mkp5` and 10.58 on `ptp1b`**. At that
effective V the ceiling is p95 = 0.707. At the raw count it is p95 = 0.810.

**The leader reaches 0.810, which sits above the lower ceiling and on the upper one.** The
participation ratio is a variance measure applied to a tail statistic, so it is a lower bound
on the effective V and the raw count is an upper bound. The honest statement is that the
leader clears the ceiling on the optimistic reading and equals it on the pessimistic one.

**That ambiguity does not rescue the screen**, because §2 does not depend on it. Zero variants
reject the null on all four arms, and that is a statement about calibrated p-values rather than
about where the AUC sits.

---

## 4. The leader arm by arm, and why the mean hides the story

`evaluation_default` × `eigenvector_centrality` × `binned_median`:

| Arm      | AUC   | calibrated p | hits@5 | recall@5 (chance) | DCC Å (chance) |
| -------- | ----- | ------------ | ------ | ----------------- | -------------- |
| `ns5b`   | 0.944 | 0.0137       | 1      | 0.062 (0.009)     | 11.9 (23.4)    |
| `ptp1b`  | 0.887 | 0.0204       | 1      | 0.091 (0.017)     | 21.0 (17.6)    |
| `hiv_rt` | 0.707 | 0.2404       | 0      | 0.000 (0.009)     | 31.1 (25.0)    |
| `mkp5`   | 0.703 | 0.5802       | 0      | 0.000 (0.037)     | 10.9 (12.0)    |

A mean of 0.810 is built from 0.944 and 0.703. The spread across arms is larger than the
gap between the first and the fiftieth variant in the table above. **Four arms cannot
resolve the ordering the ranking is built on** (threat T6).

On two arms the predicted centre is farther from the site than a random five-residue list.
The AUC and the deliverable disagree, which is threat T5 appearing again.

**The best variant for the deliverable is a different one.** `heavy_exponential` ×
`eigenvector_centrality` × `binned_rank` takes 6 hits at 5 and a mean DCC of 13.2 Å, at a
mean AUC of 0.779. On `ptp1b` it places 4 of 5 predicted residues inside the site and its
predicted centre lands 1.7 Å from the site centre against a chance line of 17.6 Å. On
`hiv_rt` it takes zero hits. The same method, two arms, opposite outcomes.

---

## 5. What each axis is worth

Means over complete `method-sweep` variants only. These are the axes the design crosses, so
these means answer "does this knob matter", not "which setting wins".

**Graph (stage S1).** Eight variants of the contact definition.

| Graph                  | n   | mean AUC | p90   | max   |
| ---------------------- | --- | -------- | ----- | ----- |
| `heavy_inverse_square` | 270 | 0.532    | 0.702 | 0.778 |
| `cb_10`                | 270 | 0.531    | 0.707 | 0.762 |
| `evaluation_default`   | 270 | 0.527    | 0.712 | **0.810** |
| `heavy_wide`           | 162 | 0.527    | 0.682 | 0.737 |
| `heavy_contact_count`  | 162 | 0.523    | 0.688 | 0.738 |
| `heavy_exponential`    | 162 | 0.522    | 0.708 | 0.779 |
| `heavy_edge_class`     | 162 | 0.519    | 0.694 | 0.772 |
| `ca_8`                 | 162 | 0.501    | 0.659 | 0.703 |

**This graph axis is flat, and the axis is narrower than it looks.** The spread from best
to worst mean is 0.031 AUC, and seven of eight graphs sit inside 0.013 of each other. The
one clear loser is `ca_8`, the Cα-only contact map at 8 Å, which is the coarsest definition
in the set.

**Read the scope before reading the number.** All eight graphs are residue-level
distance-threshold contact graphs. What varies across them is the cutoff (4.5, 6.0, 8 and
10 Å), the atom set that the contact test uses (all heavy atoms, Cβ only, Cα only), and the
edge weight (unit, contact count, inverse square, exponential decay, five-class chemical
type). What does **not** vary is the node scale, the rule that makes an edge, and the node
features. Every graph here has one node per residue, an edge wherever two residues are close,
and no node attributes. A family that fixes all three is a family in which the graphs are
near-duplicates of one another, so a flat result inside it is close to expected.

The claim this result supports is therefore narrow: **within residue-level distance-threshold
contact graphs, the cutoff, the atom set and the edge weight are low-leverage.** It does not
support a claim about graph construction in general.

**And the metric decides how flat it looks.** Chen, Lupo Pasini and Hauck sweep a contact
cutoff over 8 to 24 Å and report AUROC flat to within 0.03 while AUPRC falls from 0.70 to
0.36 (doi:10.1101/2025.08.25.672254). That is our own number on their AUROC axis and a
collapse on the other one, so the finding was worth re-running here. It reproduces. Restricted
to the 648 (arm, scorer, detrend) cells that exist on all eight graphs, so the comparison is
fully paired:

| Metric | Best graph | Worst graph | Spread | Relative spread |
| --- | --- | --- | --- | --- |
| AUC-ROC | `heavy_inverse_square` 0.5314 | `ca_8` 0.5014 | 0.0299 | **5.7 %** |
| AUC-PR | `heavy_exponential` 0.0928 | `ca_8` 0.0756 | 0.0172 | **19.9 %** |

**The graph axis moves precision-recall about three and a half times as far, in relative
terms, as it moves AUC-ROC.** A paired Wilcoxon over the 648 cells rejects on both axes
(p = 1.5e-7 on AUC-PR, 6.6e-6 on AUC-ROC), but the median cell difference is 0.0000 and
`heavy_exponential` wins only 307 of 648. The effect lives in the tail, not in the typical
variant. So the honest statement is narrower still: the typical variant does not care which
of these eight graphs it runs on, the label-rich tail does, and AUC-ROC is the axis least
able to see it. The prevalence on these arms runs 0.029 to 0.081, which is exactly the
low-prevalence regime where the two metrics are known to diverge. Delaunay or Voronoi contacts, typed
interaction edges, energy-weighted edges, an elastic-network Hessian, atom-level or
multi-node-per-residue scales, and any graph carrying node features are all untested here.
ADR 0028 records the wider sweep, and `docs/method/review/13-graph-construction.md` is the
evidence base for it. The
edge-class weighting, which was built specifically to carry hydrogen bonds and salt bridges
into the topology, ranks seventh of eight.

**Confound removal (stage S6).** Five forms, `raw` as the control.

| Detrend           | n   | mean AUC | p90   | max   |
| ----------------- | --- | -------- | ----- | ----- |
| `raw`             | 432 | 0.552    | 0.692 | 0.765 |
| `gaussian_kernel` | 162 | 0.539    | 0.715 | 0.786 |
| `binned_median`   | 162 | 0.521    | 0.700 | **0.810** |
| `binned_rank`     | 432 | 0.518    | 0.700 | 0.805 |
| `exponential`     | 432 | 0.497    | 0.699 | 0.761 |

**Detrending lowers the mean and raises the maximum.** `raw` has the highest mean and the
lowest maximum. Every detrended form has a lower mean and a higher p90 or maximum.

That pattern has one reading. Detrending removes the distance component. Most scorers lose
their AUC when it goes, because the distance component was carrying it. A few scorers keep
their AUC, and those are the ones worth taking forward. The mean drop is the confound
leaving. The maximum rise is what survives without it.

---

## 6. Quantum against classical, measured

The principal investigator's standing instruction is that no method is called unhelpful
until an experiment says so. All eleven quantum observables ran on all four arms, on all
eight graphs, in every applicable confound-removal form: 1 320 records, 330 complete
variants.

**Best variant per family, taken over all graphs and all detrend forms:**

| Family      | Scorers | mean of family bests | median | best  | worst |
| ----------- | ------- | -------------------- | ------ | ----- | ----- |
| `baselines` | 30      | 0.614                | 0.673  | **0.810** | 0.358 |
| `coupling`  | 9       | 0.608                | 0.598  | 0.735 | 0.387 |
| `quantum`   | 11      | 0.571                | 0.570  | **0.619** | 0.484 |
| `mechanism` | 4       | 0.570                | 0.609  | 0.714 | 0.346 |

**Paired inside each cell.** For each of the 30 (graph, detrend) cells, take the best
quantum scorer and the best classical scorer in that same cell. This holds the graph and the
confound-removal form fixed, so only the scorer differs.

- Classical wins **30 of 30 cells**.
- Mean difference **+0.196 AUC**, bootstrap 95 % CI **[+0.181, +0.212]**, 9 999 resamples,
  seed 0.
- Wilcoxon signed-rank across cells: W = 0.0, p = 1.9 × 10⁻⁹. Sign test: p = 1.9 × 10⁻⁹.

**Size-matched control, because the comparison is otherwise unfair.** The classical family
holds 43 scorers and the quantum family holds 11, so the classical maximum is drawn from
four times as many attempts. Draw 11 classical scorers at random, 2 000 times, and repeat
the comparison:

| Statistic                          | Quantum (11) | Classical (random 11 of 43) |
| ---------------------------------- | ------------ | --------------------------- |
| per-cell best, averaged over cells | 0.555        | 0.718 mean, p05 0.692       |
| global best                        | 0.619        | 0.758 mean, p05 0.715       |

**A size-matched classical set beats the quantum set in 1 999 of 2 000 draws**, on both the
average and the maximum. The family-size objection does not rescue the result.

**Whole-distribution comparison, which no maximum can bias.** Over all 330 quantum and
1 290 classical complete variants: quantum median 0.455, classical median 0.571.
Mann-Whitney U = 296 029, p = 2.7 × 10⁻²⁸, rank-biserial r = **+0.391**.

### What this does and does not establish

**Established.** The eleven quantum observables **as constructed here** — a continuous-time
quantum walk on the residue contact graph, with the active site as the source, and the
Hamiltonian set to the adjacency or the Laplacian — rank the ground-truth labels worse than
the classical graph scorers on this benchmark. This holds on every graph, in every
confound-removal form, and under a size-matched control. It is a measured result, not an
argument.

**The mechanism is visible in the same table.** Nine of the eleven quantum observables carry
a mean |ρ| against negated distance between **0.726 and 0.822**. The two exceptions are
`ctqw_coherent_source_contrast` at 0.062 and `ctqw_temporal_variance` at 0.322, and they are
the two lowest scorers of the eleven by mean AUC in most cells. A ballistic walk from a source spreads
by hop count. On an unweighted contact graph the hop count is the distance. The quantum
observables measure distance from the active site with extra steps, and the matched-patch
null is matched on geometry, so it absorbs exactly that.

**Not established, and stated as unknown.** This is not a result about quantum walks in
general. Three things were held fixed and never varied:

1. **The source.** Every observable starts at the active site. A walk started elsewhere, or
   a two-sided construction, was not measured.
2. **The Hamiltonian.** `adjacency` and `laplacian` only. No chemistry-weighted, no
   mass-weighted, no anisotropic Hamiltonian was tried.
3. **The observable.** All eleven read a transfer amplitude, a survival time, or a
   stationary distribution. None reads a spectral or interference feature.

**One measurement argues against a blanket verdict.** `ctqw_infinite_time_average` on
`cb_10` reaches **AUC 0.824 on `hiv_rt`**, where the overall classical leader reaches 0.707
on the same arm. The same variant reaches 0.377 on `ns5b`. The quantum family is not
uniformly worse. It is far more variable across arms, and its variance is what sinks its
mean. High variance across four arms is not evidence of a signal, but it is not evidence of
its absence either.

**The resource account is a separate document.** Qubit counts, depths, gate counts and
connectivity for all eleven observables are in
[`43-quantum-resources.md`](43-quantum-resources.md), which is what C3 and C4 require. That
account stands whatever this section says about accuracy.

---

## 7. Distance orthogonality

1 349 of 1 923 complete variants hold a mean |ρ| against negated distance below 0.30. The
top of that subset is the same top as the full table: `eigenvector_centrality` on
`evaluation_default` reports ρ = 0.00 exactly.

**This is the one encouraging structural fact in the file.** The leaders are not distance
scores. `eigenvector_centrality` after a binned detrend has no measurable correlation with
distance to the active site and still reaches 0.810. Whatever it measures, it is not the
confound that explains most published allosteric-site results.

The counter-example sits in the same tables. The consensus in `fusion-probe` reaches 0.765
with ρ = +0.58, and it rejects on zero arms. High AUC with high ρ and a high p-value is the
signature of the null working as designed.

---

## 8. What is refuted

Negative results, each with the measurement that produced it.

| Claim                                                              | Measured                                                                        | Status                                                                                                   |
| ------------------------------------------------------------------ | ------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| Cutoff, atom set and edge weight are high-leverage choices          | 0.031 AUC spread across eight graphs; seven inside 0.013                        | **refuted on this benchmark**, within residue-level distance-threshold graphs only — scale, edge rule and node features were not varied |
| Edge-class weighting carries chemistry that unit weighting loses   | seventh of eight graphs by mean AUC                                             | **no measurable gain**                                                                                   |
| Evolved elastic networks route signal down a **soft** corridor     | `soft_corridor_to_source` mean AUC 0.309–0.346 over its 15 variants, worst arm 0.207 | **refuted**; the inverse reaches 0.714 and is kept as `stiff_corridor_to_source`                         |
| Domain-boundary residues mark allosteric sites                     | `module_boundary` mean AUC 0.440–0.522 over its 15 variants                     | **at chance**                                                                                            |
| Quantum walk observables beat classical graph scorers here         | classical wins 30 of 30 paired cells, +0.196 AUC, size-matched control holds    | **refuted for the eleven constructions tested**; see §6 for what stays open                              |
| B-factor predicts allosteric sites                                 | `mean_bfactor` best mean AUC 0.435                                              | **below chance**, consistently                                                                           |
| The screen can produce a confirmable method                        | 0 of 1 923 variants reject on four arms; ceiling p95 0.810 equals the best AUC  | **the screen cannot confirm**; [`41`](41-selection-and-power.md) has the power calculation               |

`alps_spectral_response`, the reimplementation of the prior work's best method, reaches a
mean AUC of 0.713 and rejects on zero arms. It is an **optimistic** bar, because its
published constants were tuned on labels that include arms related to ours (threat T10,
ADR 0026). It is a comparator and never a candidate.

---

## 9. What the screen hands to the next phase

The screen's job is to pick one method to freeze. It cannot certify one. It can rank, and
this is the ranking with its caveats attached.

**Two candidates, and they are not the same candidate.**

- **For the confirmatory endpoint:** `evaluation_default` × `eigenvector_centrality` ×
  `binned_median`. Mean AUC 0.810, ρ = 0.00, rejects on 2 of 4 arms, 2 hits at 5.
- **For the deliverable:** `heavy_exponential` × `eigenvector_centrality` × `binned_rank`.
  Mean AUC 0.779, ρ = 0.06, rejects on 1 of 4 arms, 6 hits at 5, mean DCC 13.2 Å.

Both are `eigenvector_centrality`. The graph and the detrend form differ, and the two
choices trade the endpoint against the five-residue list, exactly as threat T5 predicts.
**That choice must be made once and written into an ADR before the `generalisation` tier
opens.**

**What has to be true for either to be a result.** The confirmatory design is step by step
in [`42-threats-and-confirmation.md`](42-threats-and-confirmation.md) §4. In one line: freeze
one method, pre-register the expected AUC and the abandonment threshold, then open the
`generalisation` tier once.

**What would abandon the route.** If the frozen method's AUC on the `generalisation` tier
falls inside the label-blind ceiling at the V this screen ran, then the screen selected
noise. That outcome is planned for. The write-up in that case is a negative result with the
ceiling as its evidence, and the ceiling is already measured.

---

## 10. Reproducing this

```bash
uv run python experiments/2026-08-26-method-sweep/run.py
uv run python experiments/2026-08-26-mechanism-probe/run.py
uv run python experiments/2026-08-26-fusion-probe/run.py
```

Each runner is resumable on a record key and writes `records.jsonl` plus `metrics.json`.
Each `config.yaml` carries every knob that affects a number, the seed included. A rerun of a
committed config must reproduce its metrics exactly.

The `method-sweep` runner takes about 44 minutes on one machine. `fusion-probe` and
`mechanism-probe` take under 10 minutes each.
