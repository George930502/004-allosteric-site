# Exploratory data analysis of the measured results

**Scope:** what the numbers already in this repository and in `allosteric-benchmark/` say
about which method families work, what the residue graphs actually look like, and how much
of every published score is proximity to the active site. It deliberately excludes the
literature — no paper is reviewed here, and no method is proposed. Sibling files argue from
the field; this one argues from the data.
**Sibling files:** `01-classical-baselines.md`, `02-ai-methods.md`, `03-quantum-methods.md`,
`04-hybrid-quantum-ai.md`, `05-adjacent-task-transfer.md`, `06-signal-propagation-physics.md`.
**Retrieved:** 2026-08-25.

---

## 0. How to read the numbers in this file

Every number below was computed in this session from a file on disk. None is quoted from
prose, and none is recalled. Each section names the script that produced it; the scripts are
in the session scratchpad (`.../ce5997e3-.../scratchpad/`) and are listed in the Method
section at the end. Project rule R3 ranks a repo experiment above a literature value, so a
computed number carries its script name where a literature claim would carry a DOI. The
three evidence tags are used only where this file touches a literature claim.

Two conventions are inherited from the benchmark's own code (`methods/common.py`) and are
used everywhere below:

- The **contact graph** is unit-weighted on Cβ coordinates with a 10 Å cutoff, no self-loops.
- The **candidate pool** is every residue at least 8 Å from the nearest active-site residue,
  excluding the active site itself. Every AUC is computed inside that pool.

A caution that applies to the whole file. Two label conventions are mixed across the
benchmark's target sets, and they disagree about geometry. The **curated** sets use expert
annotation. The **tier-A/tier-B** sets use a 4 Å-to-modulator proxy. On curated labels the
true site sits *closer* to the active site than the distal background; on the proxy sets it
sits *farther*. Numbers from the two families are not interchangeable and are never pooled
here.

---

## 1. What the graphs look like — the substrate any propagator has to work with

`02_graph_profile.py` profiled **501** contact graphs across all eight target directories.
`02c_spectral_extra.py` added the hop-depth and eigenvalue-isolation statistics.
`09b_lowmode_degeneracy.py` reproduced the benchmark's own degeneracy statistic and set a
scale-free one beside it.

### 1.1 Size, degree, density

| statistic | 5 % | 25 % | median | 75 % | 95 % | range |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| N (residues) | 186 | 305 | **405** | 641 | 1170 | 118 – 2072 |
| mean degree | 16.17 | 17.03 | **17.95** | 18.85 | 20.21 | 11.83 – 21.24 |
| degree s.d. | 5.13 | 5.57 | 5.90 | 6.27 | 6.79 | 3.53 – 7.15 |
| min degree | 2 | 4 | 4 | 5 | 6 | 1 – 7 |
| max degree | 27 | 30 | 32 | 33 | 37 | 21 – 41 |
| density | 0.0152 | 0.0295 | **0.0435** | 0.0571 | 0.0917 | 0.0096 – 0.1143 |
| cycle rank / residue | 7.09 | 7.52 | **7.97** | 8.43 | 9.11 | 4.92 – 9.62 |
| diameter (hops) | 7 | 9 | **10** | 12 | 16 | 6 – 26 |
| characteristic path (hops) | 3.11 | 3.63 | 4.16 | 4.90 | 6.49 | 2.70 – 9.92 |
| mean clustering coefficient | 0.5114 | 0.5234 | **0.5352** | 0.5464 | 0.5669 | 0.4930 – 0.6044 |

The distributions are narrow where it matters. Mean degree spans a factor of 1.8 across a
17-fold span in N, and clustering spans 0.49 to 0.60 across the whole corpus. A 10 Å Cβ
contact graph is close to a fixed local motif repeated at different sizes.

**Cycle rank per residue is not an independent variable.** For a connected graph
`cycle_rank/N = (m − N + 1)/N = mean_degree/2 − 1 + 1/N`, and the measured Spearman
correlation between the two over 501 graphs is **1.00**. Any precondition stated in terms of
"cycles per residue" is a statement about mean degree with a different name on it. This
matters directly: the chiral-walk precondition recorded in `00-conventions.md` §5 item 8
("7.7–8.3 cycles per residue") is the statement that mean degree is about 17.5, which is true
of essentially every protein at a 10 Å cutoff.

Connectivity is not an issue: 99.2 % of graphs are a single connected component and the worst
case is two.

### 1.2 Scaling with N

Log-log regressions over the 501 graphs (`02b_graph_report.py`, `02c_spectral_extra.py`):

| quantity | slope in log N | s.e. | r² |
| --- | ---: | ---: | ---: |
| algebraic connectivity λ₂(L) | **−0.977** | 0.054 | 0.399 |
| adjacency top gap λ₁ − λ₂ | −1.525 | 0.078 | 0.435 |
| diameter | +0.387 | 0.013 | 0.650 |
| mean degree | +0.079 | 0.005 | 0.331 |

λ₂ decays as 1/N. The classical diffusive mixing time therefore grows linearly with the
number of residues, and the top of the adjacency spectrum flattens faster still. Median
λ₂ = 0.3545; 10.2 % of graphs sit below 0.1 and 3.2 % below 0.05.

### 1.3 The spectrum has no degeneracy to exploit

This is the structural fact that decides the fate of every interference-based readout, and it
needs a scale-free statistic to see. The adjacent-gap ratio
`r_i = min(s_i, s_{i+1}) / max(s_i, s_{i+1})` needs no unfolding.

Reference values computed in-session by sampling, not cited (`12_goe_reference.py`, 40
matrices of size 500):

- GOE ⟨r⟩ = **0.5317 ± 0.0154** (level repulsion, no degeneracy)
- Poisson ⟨r⟩ = **0.3894 ± 0.0147**, against the analytic `2 ln 2 − 1 = 0.3863`

Measured over the 501 contact graphs: adjacency ⟨r⟩ median **0.5267**, IQR
[0.5163, 0.5369]. On the Kirchhoff matrix, ⟨r⟩ = 0.522 (tier B), 0.517 (curated), 0.513
(multimers). **A residue contact graph is a GOE-like spectrum.** Its levels repel. Exact
degeneracies are absent (median fraction of gaps below 1e-8 is 0.0000), and near-degeneracies
are absent too: the median count of adjacency eigenvalue pairs within 1 % of the mean level
spacing is **0 of N**, and within an absolute 1e-3 it is **1 of N**.

**The benchmark's own degeneracy statistic measures something else.**
`scripts/multimer_ablation.py::degeneracy` takes the 20 lowest non-zero Kirchhoff eigenvalues
and counts relative gaps `s_i/λ_i < 1 %`. Reproduced exactly here: 3.63 % on tier B (the
README reports 3.6 %) and 4.61 % on the multimer set. The statistic is scale-dependent — near
the top of the spectrum λ ≈ 34 and s ≈ 0.05, so `s/λ` is small for reasons that have nothing
to do with degeneracy, and applying the same rule to the whole spectrum returns 79–91 %. Read
scale-free, the near-degeneracy fraction is **0.06 % in all three groups, monomer and
multimer alike**. Symmetry does enrich the low-mode end, and that part of the benchmark's
finding survives. It does not create degeneracy anywhere else, and it does not move the
spectrum away from GOE.

### 1.4 The principal eigenvalue is isolated, which is why a walk collapses to centrality

The ratio (λ₁ − λ₂) / mean level spacing has median **25.6**; 79 % of graphs exceed 10 and
98 % exceed 1. The top adjacency eigenvalue is separated from the rest of the spectrum by
tens of mean spacings.

A continuous-time quantum walk propagator is `exp(−iAt)`. When one eigenvalue is isolated by
that margin, the long-time and time-averaged transfer amplitudes are dominated by its
eigenvector, which is the eigenvector centrality. This is the measured mechanism behind the
published result recorded in `00-conventions.md` §5 — CTQW centrality agreeing with classical
eigenvector centrality (Mohtashim, Sajjan & Kais, *JACS* 2026, doi:10.1021/jacs.6c08053)
`[UNVERIFIED]` for the paper's own numbers, which were not retrieved this session; the
isolation statistic that explains it is computed here.

### 1.5 The site is two hops away

`02c_spectral_extra.py`, over 240 labelled targets:

| hop count from the active-site anchor set | median | 5 % | 95 % |
| --- | ---: | ---: | ---: |
| to the **nearest** label residue | **2** | 1 | 4 |
| to the **median** label residue | 3 | 1 | 5 |
| to the median pool residue | 3 | 2 | 6 |
| to the farthest pool residue | 6 | 4 | 12 |

**67.9 %** of labelled targets have a label residue within **2 hops** of the active site, and
**87.9 %** within 3. In Euclidean terms (328 labelled targets) the median distance from the
active site to the nearest label residue is **13.8 Å**, and 41.5 % of targets have one inside
12 Å.

This is the single most consequential structural fact in the file. On a graph of mean degree
18 and diameter 10, a two-hop neighbourhood is already a large fraction of the protein. There
is no long-range transport problem here for a propagator to solve. Whatever separates a true
site from the background, it is not distance travelled through the network.

### 1.6 Label geometry

Over 328 labelled targets: median 21 anchor residues, median 12 label residues, median pool
size 388, median prevalence inside the pool **2.8 %** (mean 3.1 %). Positive prevalence
between 1 % and 4 % is the operating regime for every metric below, and it is why accuracy is
useless here — the hybrid folder records a first attempt that reported 0.967 for two
classifiers that were both predicting all-negative (`hybrid/RESULTS.md`).

### 1.7 What helps and what hurts a quantum propagator

| structural fact | effect |
| --- | --- |
| GOE level statistics, ⟨r⟩ = 0.527 | **Hurts.** Interference readouts need degenerate or near-degenerate levels. There are none. |
| λ₁ isolated by 25× the mean spacing | **Hurts.** A coherent walk collapses onto eigenvector centrality, a one-line classical quantity. |
| Site is 2 hops from the active site | **Hurts.** No transport distance to exploit; a 2-step classical diffusion reaches the same residues. |
| λ₂ ∝ 1/N, so classical mixing time ∝ N | **Helps, in principle.** This is the one place where a coherent walk's ballistic spread could beat diffusion. But it only matters over long paths, and §1.5 says the relevant paths are 2–3 hops. |
| Single connected component, 99.2 % | Neutral. Removes a class of pathologies. |
| Mean degree 18 at N up to 2072 | **Hurts hardware.** A qubit-per-residue encoding needs 118–2072 qubits with degree-18 connectivity, on hardware with nearest-neighbour or heavy-hex coupling (C3). |
| Real symmetric graph, no gain/loss | **Hurts.** No non-Hermitian structure, as `00-conventions.md` §5 item 11 already records. |

---

## 2. How much of every method is distance to the active site

Two independent measurements, one per-residue and one per-target.

### 2.1 Per-residue: correlate the score against distance directly

`04_distance_confound.py` recomputed the raw per-residue score of every implemented method on
the 24 `targets_curated_small` structures (N 248–499; 23 pass the pool filter), applied the
benchmark's own rank-percentile and pocket-smoothing post-processing, and took the Spearman
correlation with the minimum distance to the active site **inside the candidate pool**. R² is
ρ², the share of the score's rank variance that distance alone accounts for.

| method | median ρ vs distance | **median R²** | mean plain AUC | mean stratified AUC |
| --- | ---: | ---: | ---: | ---: |
| `ctrl_dist` / `ctrl_closeness` | ±0.991 | 0.981 | 0.473 / 0.527 | 0.520 / 0.480 |
| **`qfi`** (quantum Fisher information) | −0.956 | **0.915** | 0.500 | 0.445 |
| `btb_raw` (bond-to-bond, uncorrected) | −0.927 | **0.859** | 0.526 | 0.508 |
| `qasc_normlap` | −0.728 | 0.531 | 0.444 | 0.396 |
| `qasc_degseed` | −0.691 | 0.477 | 0.447 | 0.388 |
| `qasc_baseline` | −0.690 | 0.477 | 0.448 | 0.392 |
| **`ctqw_only`** | −0.651 | **0.423** | 0.466 | 0.413 |
| `qasc+btb` | −0.600 | 0.360 | 0.458 | 0.424 |
| `ctrl_burial` | −0.430 | 0.185 | 0.477 | 0.469 |
| `qpr_coherent` | −0.408 | 0.166 | 0.442 | 0.422 |
| `prs` | +0.396 | 0.157 | 0.485 | 0.460 |
| `corrsite` | −0.327 | 0.107 | 0.570 | 0.554 |
| `eigvec_dpart` | −0.306 | 0.093 | 0.563 | 0.562 |
| `chiral_asym` | −0.269 | 0.072 | 0.513 | 0.505 |
| `ALPS_noresid` | −0.260 | 0.068 | 0.623 | 0.655 |
| `degeneracy_dgap` | −0.167 | 0.055 | 0.554 | 0.534 |
| `mode_ipr_dipr` | −0.122 | 0.038 | 0.547 | 0.558 |
| `apop` | −0.112 | 0.026 | 0.558 | 0.547 |
| **`ALPS`** | −0.045 | **0.003** | 0.641 | 0.654 |
| `btb` (distance-corrected) | −0.016 | 0.002 | 0.494 | 0.511 |
| `enaqt` | +0.009 | 0.002 | 0.517 | 0.508 |

**The answer to "distance explains X %" is a spread, and the quantum family sits at the wrong
end of it.** Quantum Fisher information is 92 % distance. The coherent-walk family (`ctqw`,
the three `qasc` variants) is 42–53 % distance. `ALPS`, which residualises against distance
by construction, is 0.3 %.

### 2.2 Per-target: the plain-to-stratified collapse

`05_confound_and_headroom.py` pairs `results_curated_full.json` (plain AUC, 73 targets)
against `results_partial_auc.json` (distance-stratified AUC, |Δd| ≤ 2 Å, 72 targets) target by
target. `frac lost` is the share of the method's margin over 0.5 that disappears when
distance is spent.

| method | plain AUC | stratified AUC | drop | frac lost | paired p |
| --- | ---: | ---: | ---: | ---: | ---: |
| `btb_raw` | 0.6176 | 0.5100 | 0.1076 | **91.5 %** | 0.0019 |
| `ctqw_only` | 0.5981 | 0.5154 | 0.0827 | **84.3 %** | 0.0007 |
| `qasc_baseline` | 0.5899 | 0.5025 | 0.0875 | **97.3 %** | 0.0006 |
| `corrsite` | 0.5952 | 0.5259 | 0.0693 | 72.8 % | 0.0008 |
| `ALPS_noresid` | 0.5976 | 0.5786 | 0.0190 | 19.5 % | 0.207 |
| `apop` | 0.5544 | 0.5414 | 0.0130 | 23.9 % | 0.311 |
| `btb` | 0.5321 | 0.5183 | 0.0138 | 43.0 % | 0.295 |
| **`ALPS`** | 0.5773 | 0.5782 | **−0.0009** | **0 %** | 0.906 |
| `ctrl_random` | 0.5259 | 0.5227 | 0.0032 | 12.2 % | 0.578 |

The between-target version says the same thing. Regressing each method's per-target AUC on
the closeness control's per-target AUC across the same 72 targets:

| method | Pearson r | **R²** |
| --- | ---: | ---: |
| `btb_raw` | +0.959 | **0.919** |
| `qasc_baseline` | +0.815 | 0.664 |
| `ctqw_only` | +0.775 | 0.601 |
| `corrsite` | +0.482 | 0.233 |
| `ctrl_burial` | +0.336 | 0.113 |
| `btb` | +0.224 | 0.050 |
| `ALPS_noresid` | +0.200 | 0.040 |
| `ALPS` | −0.031 | 0.001 |
| `apop` | −0.026 | 0.001 |

Three independent estimators agree: `btb_raw` is 86–92 % geometry, the coherent-walk family
is 42–66 %, and the two ENM spectral readouts are under 4 %.

### 2.3 The stratified metric does what it claims

`08_extra_sets.py` reads the tolerance sweep. The diagnostic is `ctrl_closeness`: it must
collapse to 0.5 once distance is properly controlled.

| tolerance (Å) | 0.5 | 1.0 | 1.5 | **2.0** | 3.0 | 4.0 | 6.0 | ∞ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `ctrl_closeness` | 0.489 | 0.489 | 0.489 | **0.494** | 0.503 | 0.510 | 0.523 | 0.573 |
| `ALPS` | 0.574 | 0.583 | 0.580 | **0.578** | 0.579 | 0.576 | 0.576 | 0.570 |
| `ctqw_only` | 0.478 | 0.481 | 0.483 | **0.481** | 0.486 | 0.491 | 0.498 | 0.540 |
| `qfi` | 0.456 | 0.456 | 0.455 | **0.460** | 0.469 | 0.475 | 0.493 | 0.553 |
| median matched pairs | 104 | 209 | 320 | **406** | 600 | 754 | 1113 | 2448 |

The 2 Å choice is validated by data, not by taste: closeness sits at 0.494 there and rises
monotonically as the window opens. `ALPS` is flat across the whole sweep — its score genuinely
contains no distance. `ctqw_only` and `qfi` rise with the window, which is what a
distance-loaded score does.

### 2.4 The sign of the confound is a property of the labels, not of allostery

On curated expert labels, closeness wins: `ctrl_closeness` reaches plain AUC **0.6166** on 72
targets, and no method separates from it (§4). On the proxy-labelled tier-B set, the opposite
control wins: `ctrl_dist` reaches **0.6136** on 90 targets, the best score there. The two sets
disagree by 0.23 AUC on the same one-line geometric feature.

This is not a subtlety to note in passing. It means the direction and size of the geometric
confound must be **measured on our own frozen benchmark** before any method result from it is
interpreted, and it means a method tuned to one label convention can invert on the other.

---

## 3. Effective dimensionality of the feature space

`03_features.py`, over the two committed feature caches. Both are rank-percentile columns, so
a Pearson correlation on them is already a rank statistic.

| | `hybrid/features.npz` | `data/combiner_features.npz` |
| --- | --- | --- |
| targets | 44 curated | 59 tier B |
| pooled pool residues | 16 063 | 14 816 |
| positives in pool | 386 (**2.40 %**) | 567 (**3.83 %**) |
| nominal features | **8** | **7** |
| effective rank, tr S / ‖S‖ | **2.618** | **2.645** |
| effective rank, spectral entropy | **5.393** | **5.413** |
| PCs for 90 % / 95 % variance | 6 / 6 | 5 / 6 |
| explained variance ratio | .382 .223 .151 .078 .063 .058 .038 .007 | .378 .183 .160 .120 .069 .054 .037 |

**The learned combiner's 7 features carry between 2.6 and 5.4 independent directions.** The
two effective-rank definitions bracket the answer: the trace-over-max ratio weights the top
eigenvalue heavily and returns 2.6; the spectral-entropy version returns 5.4. Neither is 7.

Pairwise correlation, hybrid matrix (8 features):

| | alps | apop | corrsite | prs | btb | ctqw | dist | burial |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| alps | 1.000 | **0.733** | 0.039 | −0.179 | 0.118 | 0.096 | −0.098 | **0.557** |
| apop | 0.733 | 1.000 | 0.058 | −0.204 | 0.209 | 0.161 | −0.213 | **0.589** |
| corrsite | 0.039 | 0.058 | 1.000 | 0.244 | 0.352 | 0.210 | −0.320 | 0.096 |
| prs | −0.179 | −0.204 | 0.244 | 1.000 | −0.279 | −0.199 | 0.256 | −0.176 |
| btb | 0.118 | 0.209 | 0.352 | −0.279 | 1.000 | 0.502 | **−0.918** | 0.218 |
| ctqw | 0.096 | 0.161 | 0.210 | −0.199 | 0.502 | 1.000 | **−0.488** | 0.258 |
| dist | −0.098 | −0.213 | −0.320 | 0.256 | −0.918 | −0.488 | 1.000 | −0.293 |
| burial | 0.557 | 0.589 | 0.096 | −0.176 | 0.218 | 0.258 | −0.293 | 1.000 |

Collinearity with distance, expressed as the variance-inflation factor from regressing each
feature on all the others: `btb` 7.3, `dist` 7.0, `apop` 2.5, `alps` 2.4, `burial` 1.8,
`ctqw` 1.4, `corrsite` 1.4, `prs` 1.3. `btb` and `dist` are one direction with two names,
and they are the pair that the smallest principal component (0.7 % of variance) separates.
The combiner matrix uses the distance-corrected `btb` instead, and its collinearity with
distance falls to r = −0.010, VIF 1.1 — the residualisation works.

Univariate discrimination inside the pool, pooled over targets:

| feature | hybrid (44 curated) | combiner (59 tier B) |
| --- | ---: | ---: |
| `alps` | **0.579** | **0.644** |
| `corrsite` | 0.557 | 0.449 |
| `apop` | 0.544 | 0.560 |
| `btb` | 0.538 | 0.453 |
| `ctqw` | 0.521 | — |
| `burial` | 0.486 | 0.521 |
| `dist` | 0.474 | 0.555 |
| `prs` | 0.435 | 0.452 |

The sign flip on `dist` between the two panels is §2.4 again, in one column.

**Consequence for any quantum feature map.** `hybrid/RESULTS.md` records a variational
classifier on 8 qubits, 3 layers, 24 trainable parameters, encoding these 8 features. It is
encoding a matrix whose effective rank is 2.6. The regime where a quantum kernel's larger
feature space could pay for itself is far above this dimensionality, and the measured result
matches: VQC 0.575 against logistic regression 0.596 on identical features, Δ = −0.021,
paired p = 0.39. The same file records the kernel arm: quantum kernel at bandwidth 0.02
reaches 0.592 against `poly-4` at 0.600, Δ = −0.008, paired p = 0.20, with the quantum
kernel's ranking landing immediately below the polynomial kernel it was predicted to
approximate.

---

## 4. Method ranking, and how it moves with the metric

`01_tidy_results.py` builds one tidy table across every result file in
`allosteric-benchmark/data`: **24 306 rows**, 20 target-set labels, 8 distinct file schemas.
`11_overall_ranking.py` collapses it.

Mean AUC by set. The first three columns are plain AUC; the last three are distance-stratified
AUC. Only methods scored on five or more sets are shown.

| method | tierA (11) | tierB (90) | curated73 | strat curated (72) | expanded (96) | mean margin over random |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| **`ALPS`** | **0.7575** | **0.6026** | 0.5773 | 0.5782 | 0.5906 | **+0.1154** |
| **`ALPS_noresid`** | 0.7215 | 0.5838 | 0.5976 | **0.5786** | **0.5906** | **+0.1086** |
| `apop` | 0.7334 | 0.5641 | 0.5544 | 0.5414 | 0.5325 | +0.0794 |
| `corrsite` | 0.5338 | 0.4422 | 0.5952 | 0.5259 | 0.5115 | +0.0159 |
| `ctrl_burial` | 0.6134 | 0.4661 | 0.5136 | 0.4967 | 0.4978 | +0.0117 |
| `ctrl_dist` | 0.5833 | **0.6136** | 0.3834 | 0.5206 | 0.5275 | +0.0199 |
| `ctrl_random` | 0.4888 | 0.4729 | 0.5259 | 0.5227 | 0.5185 | 0 |
| `btb` | 0.4456 | 0.4653 | 0.5321 | 0.5183 | — | −0.0123 |
| `ctqw_only` | 0.4652 | 0.4162 | **0.5981** | 0.5154 | 0.5191 | −0.0146 |
| `btb_raw` | 0.4248 | 0.3940 | **0.6176** | 0.5100 | 0.5045 | −0.0156 |
| `qasc_baseline` | 0.4125 | 0.4157 | 0.5899 | 0.5025 | 0.5064 | −0.0300 |
| `qfi` | — | — | — | 0.4639 | 0.4649 | −0.0562 |
| `qasc_normlap` | 0.3692 | 0.3891 | — | — | — | −0.0977 |
| `qpr_coherent` | 0.3580 | 0.3999 | — | — | — | −0.0930 |

Three readings.

1. **Every quantum readout has a negative mean margin over the random control.** The best is
   `mode_ipr_dipr` at +0.0098 on one set only. The two ENM spectral readouts, `ALPS` and
   `ALPS_noresid`, are the only methods above +0.10.
2. **`btb_raw` and `ctqw_only` top the curated73 column and are near the bottom everywhere
   else.** That is §2 in one row: their curated-set rank is bought with distance, and the
   curated set is the one where closeness helps.
3. **The metric decides the ranking.** `btb_raw` is rank 1 on curated73 plain AUC and rank 21
   of 22 on tier-B plain AUC.

A note on the quantum-recheck file. `results_quantum_recheck.json` contains only quantum
readouts plus `cpr_classical` and `ctrl_random`, so the "best classical" inside it is a weak
comparator. `07_recheck_vs_alps.py` joins it to `results_partial_auc.json` on the 70 shared
targets, identical metric and tolerance. The ranking on that shared subset:

`ALPS_noresid` 0.6052 · `ALPS` 0.6036 · `eigvec_dpart` 0.5469 · `mode_ipr_dipr` 0.5468 ·
`cpr_classical` 0.5432 · `corrsite` 0.5404 · `apop` 0.5374 · `degeneracy_dgap` 0.5281 ·
`ctrl_dist` 0.5237 · `chiral_asym` 0.4805 · `ctrl_closeness` 0.4765 · `qpr_coherent` 0.4464 ·
`ctqw_only` 0.4396 · `qasc_baseline` 0.4257.

---

## 5. Is there a subgroup where a quantum or spectral method wins?

`06_subgroups.py` ran **195** subgroup contrasts: 5 result sets × 13 slicing variables × 3
tertiles. Slicing variables are N, mean degree, density, cycles per residue, λ₂(L), adjacency
top gap, principal-eigenvalue isolation, diameter, clustering, active-site-to-label distance,
label-set size, pool prevalence, and anchor-set size. Bonferroni α over 195 tests is
**2.6 × 10⁻⁴**. `07_recheck_vs_alps.py` reran the 39 contrasts on the quantum-recheck subset
against the real classical bar.

**No quantum readout beats the classical bar in any subgroup at Bonferroni.**

The one candidate worth naming, with all its caveats:

> **`eigvec_dpart` on targets with 23–26 active-site residues.** Distance-stratified AUC
> **0.6264** against `ALPS_noresid` **0.5568** and `ALPS` 0.5579, on **n = 19** targets.
> Δ = +0.0696, paired p = **0.0356**. Against 0.5 it is unambiguous: one-sample p = 0.0023.

Against the classical bar it is not. The family it sits in has 39 tests, so its threshold is
1.3 × 10⁻³ and 0.0356 misses by a factor of 27. The slicing variable is also the wrong kind:
**anchor-set size is a property of how the active site was annotated, not of the protein**.
A subgroup defined by an annotation artefact is the shape a multiple-comparisons false
positive takes. The benchmark's own record contains two instances of exactly this pattern —
`dgap` leading at n = 4 symmetric multimers and reversing at n = 29, and the cooperative-QUBO
hit rate falling from 0.455 at n = 11 to 0.236 at n = 89 (§7 below).

The nearest structurally meaningful subgroup is the low mean-degree tertile (16.18–17.05,
n = 25): `eigvec_dpart` 0.6642, `ALPS` 0.6457, `ALPS_noresid` 0.6438. It clears 0.5 decisively
(p < 10⁻⁴) and does not clear ALPS (Δ = +0.020, p = 0.36).

The other direction is where the significant results are. Across the four label-bearing sets
the classical side wins **149 of 156** contrasts, and the largest margins clear Bonferroni
comfortably:
`ALPS_noresid` over `ctqw_only` by 0.217 on the high-anchor-count tertile (n = 22,
p = 0.0002); `ALPS` over `qfi` by 0.217 on the high-density tertile (n = 20, p < 10⁻⁴);
`ALPS` over `ctqw_only` by 0.204 on the high-anchor-count tertile of the expanded set (n = 32,
p = 0.0001).

Counting outright subgroup winners across the **156** subgroups on the four label-bearing sets
(13 slicing variables x 3 tertiles x 4 sets): `ALPS` **62** and `ALPS_noresid` **48**, so the
ALPS family takes **110 of 156**; `apop` or `apop+dist` 15; `btb_raw` 13; `corrsite` 7;
`ctqw_only` **4**; `btb` 2; `cpr_classical` 2; `qasc_baseline` 2; `enaqt` 1. The whole quantum
family wins 7 of 156.

**Conclusion for (d): the honest answer is no.** One candidate exists, it is defined by an
annotation artefact, and it does not survive multiplicity.

---

## 6. Headroom

`05_confound_and_headroom.py`. "Best" is the best non-control method on that set; the gap to a
perfect ranker is 1.000 − best. Confidence intervals are 20 000-resample paired bootstraps
over targets.

| set | metric | best method | best | −distance control | random | gap to perfect | best − control | 95 % CI | paired p |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- | ---: |
| curated 73 | plain AUC | `btb_raw` | 0.6176 | **0.6166** | 0.5259 | **0.382** | **+0.0010** | [−0.017, +0.019] | 0.909 |
| curated 72 | stratified | `ALPS_noresid` | 0.5786 | 0.4796 | 0.5227 | 0.421 | +0.0989 | [+0.027, +0.168] | 0.0083 |
| expanded 96 | stratified, r = 12 Å | `ALPS_noresid` | 0.5906 | 0.4727 | 0.5185 | 0.409 | +0.1180 | [+0.056, +0.178] | 0.0003 |
| tier A 11 | plain AUC | `ALPS` | 0.7541 | 0.3886 | 0.4881 | 0.246 | +0.3655 | [+0.175, +0.516] | 0.0033 |
| tier B 90 | plain AUC | `ALPS` | 0.6004 | 0.3795 | 0.4745 | 0.400 | +0.2210 | [+0.160, +0.280] | 1.6e−10 |
| recheck 37 | stratified, quantum only | `mode_ipr_dipr` | 0.5411 | — | 0.5313 | 0.459 | +0.0098 | [−0.069, +0.085] | 0.806 |

Expressed as a share of the distance that still separates the control from a perfect ranker,
the best method closes:

- **0.3 %** on curated plain AUC — the confounded metric, where nothing beats geometry;
- **19.0 %** on curated stratified AUC;
- **22.4 %** on the expanded set's stratified AUC;
- **35.6 %** on tier-B plain AUC and **59.8 %** on tier-A, where the control is
  anti-correlated with the labels and therefore easy to beat.

Two further headroom measures, both on curated 73 and both worse than the AUC picture:

**Top-5 hit rate** (the deliverable this project actually has to produce). Best: `apop`
0.132, `ALPS_noresid` and `btb_raw` 0.123, `ALPS` 0.082, `ctrl_random` 0.041. Headroom to a
perfect ranker is **0.868**. The best method finds a true label residue in its top five on
one target in eight.

**DCC** (distance from the top-5 centroid to the true site centroid; STINGAllo's success
criterion is ≤ 4 Å). Best median 22.1 Å (`ctqw_only`), against `ctrl_random` at 23.3 Å. The
fraction of targets meeting ≤ 4 Å is **0.000–0.019 for every method**. Nothing localises.

---

## 7. Four sub-experiments the main table flattens

`08_extra_sets.py`.

**7.1 Nobody can say "no site here."** 55 positive proteins against 90 negatives, protein-level
Mann-Whitney AUC over four summary statistics per method. The top four discriminators are all
controls: `ctrl_dist` max **0.859**, radius of gyration **0.813**, protein size **0.783**,
`ctrl_random` top-5 mean **0.742**. The best real method is `qasc_baseline`, at 0.732 on its top-5 mean and 0.734 on
kurtosis in the reversed direction — below the size control either way. 13 of 34 tests clear Bonferroni (α = 1.5 × 10⁻³) and the strongest are
confounds. **This experiment measures protein size and shape, not allostery.**

**7.2 Cooperative selection as a QUBO is not hard.** Candidate pool fixed at 26 residues,
choose a subset. Median |J| / mean h = 0.19 (tier A) and 0.21 (tier B); 39–42 % of couplings
are negative, so there is genuine frustration, and 72–74 % exceed 10 % of the mean field.
Classical simulated annealing matches the exhaustive optimum to **5.9 × 10⁻¹⁶** on **all 100**
targets. Greedy does not — it reaches the optimum on 9.1 % (tier A) and 6.7 % (tier B), with a
worst-case gap of 0.31. The instance class is therefore non-trivial for greedy and trivial for
classical annealing, which is the wrong side of the line for a quantum optimiser. Downstream
the result evaporates anyway: top-5 hit rate 0.455 at n = 11 falls to 0.236 at n = 89, below
its own random control at 0.257.

**7.3 Symmetric multimers.** 60 targets. Mean AUC: `dlam` (eigenvalue shift, ALPS's own
observable) **0.694**, `dpart` 0.671, `dgap` 0.656, `dipr` 0.639; permutation-significant on
68 %, 65 %, 60 %, 55 % of targets. The plain eigenvalue shift leads all three
degeneracy-sensitive readouts. The file carries no random or geometric control, so the
absolute level is not interpretable from it — only the ordering is. Combined with §1.3, the
ordering has a mechanism: symmetry enriches the low-mode gap statistic and leaves the spectrum
GOE, so there is no degeneracy for `dgap` to read.

**7.4 The tolerance sweep** is in §2.3.

---

## 8. This repository's own two experiments

`10_own_experiments.py` re-derives every number below from `metrics.json`, not from the notes.
All reproduce the committed prose exactly.

**`experiments/2026-08-25-null-calibration`.** The question is whether the matched-patch
permutation test holds its size.

- The **unmatched** background permutation has a measured type-I rate of **0.096 to 0.323**
  across 14 arms × 4 correlation lengths, median 0.234, at a nominal 0.05. It is unusable, and
  that is why the matched null exists.
- The **matched** null at tolerance 0.10 and 9999 replicates holds its size on **7 of 14
  arms** at all four correlation lengths, against the exact binomial band [0.037, 0.064] at
  n = 1000. Six arms sit above (worst `mkp5` at 0.077, `p97_vcp` at 0.072, both BCR-ABL1 arms
  0.059–0.075); one sits below (`cardiac_myosin_corrected`, 0.034–0.037).
- The **positive control** returns p = 1 × 10⁻⁴ — the smallest value 9999 replicates can
  produce — on all 14 arms at all four correlation lengths. The test rejects when it should.
- The **calibration factor** `size_ratio` runs 1.0000 to **1.2487** across arms, median 1.081.
- **Sensitivity.** 80 % power is reached at Cohen's d between **0.80 and 1.89** (median 0.88)
  over 60 arm × λ × Holm-level cells, corresponding to an achieved **AUC of 0.762 to 0.961**,
  median 0.879.

That last line is the one that binds this whole file together. **Our own frozen protocol needs
AUC 0.76 to 0.96 to reject at 80 % power.** The best method measured anywhere in
`allosteric-benchmark` on a confound-free metric is 0.59.

**`experiments/2026-08-25-null-repairs`.** Two further repairs, and a direct test of the
protocol's explanation for the residual.

- Across the 12 frozen arm × λ cells, the observed patch's variance-factor percentile and the
  type-I rate correlate at Spearman **ρ = 0.821** (p = 0.0011).
- Under intervention the relation vanishes. Repair C moves the percentile by **−18.12 points**
  on average and the type-I rate by **−0.00117**; the correlation between the two movements is
  **−0.193**. Repair D moves the percentile by −4.82 points, the type-I rate by −0.00108, and
  the movements correlate at **+0.049**.
- Both repairs leave BCR-ABL1 above the band and cardiac myosin below it. Four repairs have now
  been tried and none closes the residual.

The percentile is a correlate across arms and not a cause. The experiment is a clean example
of what this file is for: an observed ρ = 0.82 that direct intervention refutes.

---

## 9. The learned models, read from their own result files

Not recomputed here — `gnn/RESULTS.md` and `hybrid/RESULTS.md` are the source, and the model
weights are not committed.

**GNN** (`gnn/RESULTS.md`): 96 curated targets, 86 794 residues, 78 509 in the distal pool,
1 050 evaluable positives (1.3 %), 14 161 parameters, protein-grouped 5-fold CV,
distance-stratified AUC. Seed 0 → **0.622**, seed 1 → **0.630**, against `ALPS` at 0.592 and
the 25-seed random floor at 0.4963 ± 0.0157. GNN − ALPS = +0.030 and +0.038, paired p = 0.136
and 0.151 at n = 96. **Handing the model the distance channel makes it worse: 0.622 → 0.595**,
and collapses its margin over ALPS to +0.003.

That ablation is the most informative single measurement in the teammate's repository, and §2
explains it. Distance is not a useful input on curated labels once the metric controls for it;
given the channel, the network spends capacity reproducing a feature the metric has already
neutralised. The same behaviour appears in a completely different model family (the learned
combiner), which makes it a property of the task.

**Hybrid** (`hybrid/RESULTS.md`): 44 curated targets, 16 063 pooled residues, 386 positives.
Logistic regression on the 8 features 0.603, unlearned ALPS 0.576, learner − ALPS = +0.027,
p = 0.72. Quantum kernel 0.592 (bandwidth 0.02) against `poly-4` 0.600, Δ = −0.008, p = 0.20.
VQC with 24 parameters 0.575 against logistic 0.596, Δ = −0.021, p = 0.39. The quantum kernel
collapses to the identity for bandwidth ≥ 0.25 (off-diagonal mass 0.032 falling to 0.005), so
only bandwidth ≲ 0.1 is usable at all.

**The learned ceiling on curated labels is 0.62–0.63, and no learned model separates from a
one-line spectral readout at n = 44 to 96.**

---

## What this changes for our pipeline

1. **Network construction (Phase 1.2).** Fix and report the contact definition, then measure
   the spectrum, not assume it. Any method whose mechanism needs level degeneracy is
   pre-refuted on this substrate: ⟨r⟩ = 0.527 against a computed GOE value of 0.5317, and a
   median of zero near-degenerate pairs per graph. Do not adopt "cycles per residue" as an
   independent precondition — it is mean degree, Spearman 1.00.
2. **Quantum method choice (Phase 2).** A coherent single-particle walk on this graph is
   dominated by an eigenvector that is isolated by 25 mean spacings, and the resulting score
   is 42–53 % distance by rank variance. Neither is a bug to fix; both are properties of the
   substrate. Any Phase 2 candidate must state, before it is run, why it is not one of these
   two things.
3. **Propagation depth (Phase 2).** 68 % of labelled targets have a label residue within two
   hops of the active site. A method whose selling point is long-range or ballistic transport
   has no distance to travel here. Measure the hop depth on our own frozen arms before
   choosing a propagation time or circuit depth (C3).
4. **Evaluation (frozen; do not change).** Report the distance-stratified endpoint alongside
   whatever the protocol specifies, and report the sign and size of the geometric confound on
   our own labels. The sign flips between label conventions — closeness AUC 0.617 on curated,
   distance AUC 0.614 on proxy — so it must be measured, not inherited.
5. **The bar, restated in our own units.** Our frozen protocol needs AUC 0.76 to 0.96 for
   80 % power. The best confound-free number in the teammate's repository is 0.59, and the
   best top-5 hit rate is 0.132 with no method ever reaching DCC ≤ 4 Å on more than 1.9 % of
   targets. Phase 2 should plan for a result that is honest about not rejecting, and the
   report has to state the sensitivity band before it states a number.
6. **Feature-based and learned arms (Phase 1.4, and any hybrid arm).** Seven or eight
   hand-designed scores carry 2.6 to 5.4 independent directions. Adding another ENM readout to
   that stack buys almost nothing, and a quantum feature map over it is encoding a rank-2.6
   matrix. If a hybrid arm is built, it needs a feature that is demonstrably orthogonal to
   distance, burial and the ALPS/apop pair — the measured correlations say the existing ones
   are not.
7. **Statistics.** Never compare a method against a single random draw: two seeds of the same
   control differ by 0.042 and bracket the 25-seed floor. Fix the multiplicity family before
   slicing — 195 subgroup tests produced exactly one nominal quantum win, on a subgroup
   defined by an annotation artefact.
8. **Do not re-run.** Cooperative selection as a QUBO (classical annealing is exact to 6e−16
   on 100/100 instances), the multimer degeneracy ablation, the protein-level false-positive
   experiment as designed (it measures size), and CTQW/QASC/ENAQT/QFI as ranking readouts.
   All are closed by measurement above.

---

## Method

**Databases and searches:** none. This file is an analysis of files on disk and runs no
literature search. The one external reference it touches (doi:10.1021/jacs.6c08053) is carried
over from `00-conventions.md` §5 and is tagged `[UNVERIFIED]` because its full text was not
retrieved this session. The GOE and Poisson reference values for ⟨r⟩ were **computed by
sampling** rather than cited, so no retrieval was needed.

**Data read.** `allosteric-benchmark/data/*.json` — 14 result files of the 22 JSON files there,
the rest being manifests, candidate-id lists and a tuning cache; 8 distinct schemas, 24 306
tidy rows; `allosteric-benchmark/data/targets*/`, `matched_pos/`, `matched_neg/`
(501 `.npz` structures); `allosteric-benchmark/hybrid/features.npz` and
`data/combiner_features.npz`; `allosteric-benchmark/gnn/RESULTS.md` and `hybrid/RESULTS.md`;
`experiments/2026-08-25-null-calibration/{config.yaml,metrics.json,notes.md}` and
`experiments/2026-08-25-null-repairs/{config.yaml,metrics.json,notes.md}`;
`allosteric-benchmark/scripts/*.py` and `methods/*.py` for the definitions behind every
column name.

**Everything loaded.** No data file failed to load. Two schema traps were found and are
recorded because a naive reader hits both:
`results_expanded.json` holds **distance-stratified** AUC at a 12 Å contact radius, not plain
AUC (`scripts/eval_expanded.py` line 73); and `multimer_readouts.json` stores
`[permutation p, AUC]`, so taking element 0 as the AUC inverts the result.

**Scripts** (in the session scratchpad, none written into the repository):

| script | produces |
| --- | --- |
| `01_tidy_results.py` | `tidy_results.csv` — one tidy table over all 14 result files |
| `02_graph_profile.py` | `graph_profile.csv` — 501 graphs × 25 structural columns |
| `02b_graph_report.py` | distributions, cross-correlations, scaling laws |
| `02c_spectral_extra.py` | `hop_depth.csv`, principal-eigenvalue isolation |
| `03_features.py` | effective rank, correlations, VIF, univariate AUC |
| `04_distance_confound.py` | `distance_confound.csv` — per-residue ρ vs distance, 23 targets, 28 methods |
| `05_confound_and_headroom.py` | `plain_vs_strat.csv`, `target_level_closeness.csv`, headroom |
| `06_subgroups.py` | `subgroups.csv` — 195 subgroup contrasts |
| `07_recheck_vs_alps.py` | `recheck_vs_alps.csv` — quantum readouts against the real classical bar |
| `08_extra_sets.py` | `false_positive_protein_auc.csv`, QUBO, multimer, tolerance sweep |
| `09_laplacian_degeneracy.py` | `laplacian_degeneracy.csv` |
| `09b_lowmode_degeneracy.py` | `lowmode_degeneracy.csv` — the benchmark's own statistic, reproduced |
| `10_own_experiments.py` | this repository's two experiments, re-derived from `metrics.json` |
| `11_overall_ranking.py` | `overall_ranking.csv` |
| `12_goe_reference.py` | GOE and Poisson ⟨r⟩ by sampling |

**Stopping rule.** Stop when every result file in `allosteric-benchmark/data` has been loaded
and placed in the tidy table, every target directory has been profiled, and each of the five
questions in the brief has a number attached. Reached.

**What could not be reached.** Five things, each a real limit on what is above.

1. **The five leakage-guarded paths were not opened** (`00-conventions.md` §7). Nothing in
   this file is derived from our own frozen label sets, so every AUC quoted is the teammate's
   benchmark and not ours. The `experiments/` numbers are type-I rates and power, which are
   label-free by construction.
2. **The per-residue distance-confound table (§2.1) covers 23 targets, not 73.** Recomputing
   raw scores needs `apop`'s N eigensolves and `qpr`'s per-residue eigenvectors, so it was run
   on `targets_curated_small` (N 248–499). The per-target confirmations in §2.2 cover 72
   targets and agree, so the conclusion does not rest on the small set alone.
3. **GNN and hybrid numbers are read, not recomputed.** `graphs.npz` is 72 MB and not
   committed, and the trained weights are not in the repository.
4. **`multimer_readouts.json` has no control column**, so §7.3 reports the ordering of the
   four readouts and not their absolute level.
5. **No causal claim is made from any subgroup.** §5 reports one nominal win and rejects it on
   multiplicity and on the nature of the slicing variable. The null-repairs experiment in §8
   is the reason that caution is not rhetorical: it is a measured case in this repository where
   ρ = 0.82 survived four attempts and failed under intervention.
