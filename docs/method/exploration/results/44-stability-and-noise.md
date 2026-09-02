# 44 — Instability: how large it is, where it comes from, and what reduces it

**Experiments:** `experiments/2026-08-26-stability-and-source` (coordinate noise, edge dropout,
source leave-one-out, coherence window), `experiments/2026-08-26-ensemble-stabilisation` (the
remedy that works) and `experiments/2026-08-26-timescale-normalisation` (the one that does
not). All three use the `development` tier and the evaluation-default graph.

`CHALLENGE.md` §4.2 asks for a noise-resilience study. This document is that study. It also
answers the separate question the principal investigator raised: the quantum observables are
unstable, so what reduces the instability?

The two questions share one measurement, so they share one document. Every number below comes
from `allo.scoring.score_arm`. The stability readout is the Spearman correlation between the
perturbed midrank vector and the unperturbed one, written `rho`. The second readout is the
Jaccard overlap of the two top-5 lists.

---

## 1. How unstable, exactly

Three perturbations, applied to the frozen apo input and not to the evaluation:

- **Coordinate noise.** Independent Gaussian displacement of every atom, sigma in {0.25, 0.50,
  1.00} Angstrom, five seeds each. The graph is rebuilt after the displacement, so contacts
  near the cutoff can appear and disappear.
- **Edge dropout.** Random removal of a fraction f in {0.02, 0.05, 0.10} of contacts, five
  seeds each.
- **Source loss.** One residue removed from the frozen active site, once per residue.

Mean `rho` over all four `development` arms, 20 perturbed graphs per cell, for the 30 scorers
whose coverage is complete:

| Family | coord 0.25 | coord 0.50 | coord 1.00 | edge 0.02 | edge 0.05 | edge 0.10 |
| --- | --- | --- | --- | --- | --- | --- |
| classical (8 scorers) | 0.962 | 0.946 | **0.908** | 0.987 | 0.978 | 0.955 |
| quantum (22 scorers) | 0.711 | 0.666 | **0.629** | 0.783 | 0.724 | 0.680 |

**The gap is large and it is one-sided.** At 1.00 Angstrom the **twenty** least stable scorers
in the battery are all quantum, from 0.164 to 0.795. The first classical entry appears at 0.827.
The worst is `energy_contrast` at 0.164, which keeps almost none of its rank order under a
displacement smaller than the coordinate error of a good crystal structure.

Two scorers were dropped from every table here because they return the same value on every
residue, which leaves the rank correlation undefined: `symmetry_dark_overlap` and
`degenerate_mixing_weight`. That is the symmetry branch of document 47 confirmed on all four
arms rather than argued.

Three scorers inside the quantum family break the pattern, and each break is informative:

| Scorer | coord 1.00 `rho` | Note |
| --- | --- | --- |
| `dephased_transport` | **0.964** | The most stable quantum scorer. Section 5 explains why this is not good news |
| `szegedy_quantum_pagerank` | 0.839 | Discrete-time walk. More stable than every continuous-time observable |
| `quantum_best_case_transfer` | 0.795 | The most stable continuous-time observable |
| `spectral_participation_ratio` | 0.307 | Second least stable |
| `energy_contrast` | **0.164** | Least stable in the battery |

For scale at the other end, `distance_from_source_negated` sits at **0.978** and
`heat_kernel_from_source` at 0.956. Section 7 shows that this is not a coincidence.

**Source loss is mild on average and severe on one arm, and the reason is the arm.** The
removal of one active-site residue moves the quantum rankings by `rho` = 0.947 on average
against 0.997 classical. The worst quantum cell is 0.163, and the largest AUC change is −0.221.

The frozen active sites are not the same size:

| Arm | Residues in the active site | Fraction removed by leave-one-out |
| --- | --- | --- |
| `mkp5` | 11 | 9% |
| `ptp1b` | 11 | 9% |
| `hiv_rt` | 9 | 11% |
| `ns5b` | **3** | **33%** |

Every one of the five worst cells is on `ns5b` or on `energy_contrast`, and three are on both.
On a three-residue source, leave-one-out is not a small perturbation. Restricted to the three
arms with nine or more source residues, the quantum mean rises to `rho` = 0.973, the worst cell
to 0.508 and the largest AUC change to −0.151.

The active-site definition therefore does not have to be exactly right for the ranking to hold,
as long as the site is not tiny. This matters, because §4.1 says "in most cases" an active site,
and document 45 shows the source can be replaced entirely.

---

## 2. The top-5 list is far less stable than the ranking, for every method

The two readouts disagree, and the disagreement is the most practical finding here.

| Scorer | coord 1.00 `rho` | coord 0.50 Jaccard | Mean AUC |
| --- | --- | --- | --- |
| `distance_from_source_negated` | 0.978 | **0.46** | 0.581 |
| `heat_kernel_from_source` | 0.956 | **0.35** | 0.520 |
| `degree` | 0.878 | 0.35 | 0.692 |
| `eigenvector_centrality` | 0.827 | 0.38 | 0.759 |
| `gnm_fluctuation` | 0.921 | 0.41 | 0.750 |
| `anm_perturbation_response` | 0.929 | 0.82 | 0.289 |

A pure geometric control keeps 98% of its rank order under one-Angstrom noise and still
replaces two or three of its five reported residues at half an Angstrom. `eigenvector_centrality`,
the best classical scorer in the sweep at AUC 0.759, replaces three of its five. The
confirmatory endpoint is stable. **The deliverable is not.** This is not a quantum problem. It
is a property of the top-5 cut. The leading values of a continuous score sit close together.

**For the newer quantum families the top-5 list is not merely unstable. It is gone.**

| Scorer | coord 0.50 Jaccard | Mean AUC |
| --- | --- | --- |
| `spectral_participation_ratio` | **0.01** | 0.489 |
| `connectivity_strength` | **0.05** | 0.625 |
| `connectivity_eigencentrality` | 0.07 | 0.578 |
| `coherent_source_ratio` | 0.10 | 0.533 |
| `energy_contrast` | 0.12 | 0.360 |
| `connectivity_participation` | 0.15 | 0.608 |
| `connectivity_entropy` | 0.20 | 0.596 |

Read `connectivity_strength` carefully. It reaches mean AUC 0.625, which is among the better
quantum figures in the repository, and **one residue in twenty survives** from its top-5 list to
the top-5 list of a copy of the same protein displaced by half an Angstrom. A score can rank the
whole protein usefully and still name five different residues every time it is asked.

Two scorers return `rho` = 1.000 and Jaccard = 1.00 under every edge dropout level:
`distance_from_source_negated` and `anm_perturbation_response`. Neither reads the edge set, so
this is the control that behaves correctly rather than a result.

**Consequence for the submission.** Report the hit list with the top-5 Jaccard under
half-Angstrom noise beside it. A top-5 list quoted without that number overstates what the
method delivers, whatever produced the list.

---

## 3. Where the quantum instability comes from: the coherence window

The continuous-time walk needs a time grid, and the grid needs an upper limit. That limit is a
free hyperparameter. The sweep runs it over {5, 10, 25, 100} in units where the baseline is 50.

Four arms, five windows, AUC of the same scorer. These figures come from
`experiments/2026-08-26-timescale-normalisation`, which re-measured the curve at step counts
that satisfy Nyquist (see section 6):

| Scorer | Arm | w=5 | w=10 | w=25 | w=50 | w=100 |
| --- | --- | --- | --- | --- | --- | --- |
| `ctqw_coherent_source_contrast` | `mkp5` | 0.304 | 0.375 | 0.601 | **0.686** | 0.671 |
| `ctqw_coherent_source_contrast` | `ptp1b` | **0.763** | 0.688 | 0.563 | 0.623 | 0.603 |
| `ctqw_coherent_source_contrast` | `hiv_rt` | **0.605** | 0.383 | 0.177 | 0.260 | 0.269 |
| `ctqw_coherent_source_contrast` | `ns5b` | 0.440 | 0.376 | **0.565** | 0.537 | 0.460 |
| `ctqw_average_transfer` | `mkp5` | 0.756 | 0.740 | **0.779** | 0.722 | 0.690 |
| `ctqw_average_transfer` | `ptp1b` | 0.291 | 0.328 | **0.352** | 0.289 | 0.267 |
| `ctqw_average_transfer` | `hiv_rt` | **0.911** | 0.894 | 0.885 | 0.885 | 0.871 |
| `ctqw_average_transfer` | `ns5b` | 0.258 | 0.235 | 0.157 | 0.199 | **0.254** |

**Read the first three rows together.** The same observable rises with the window on `mkp5`
from 0.304 to 0.686 and falls on `hiv_rt` from 0.605 to 0.177. The window is not a
hyperparameter with a wrong setting and a right setting. It has opposite optima on two proteins
of the same benchmark tier, and its four optima sit at four different windows.

**Read the last four rows for the size of the effect.** The window moves `ctqw_average_transfer`
by about 0.09 within any one arm. The arm moves it by 0.65. Section 6 turns that observation
into the measurement that closes the question.

The rank correlation to the baseline window confirms the size of the effect. At w=5 the ranking
agrees with the w=50 ranking at `rho` between 0.26 and 0.83. The exact value depends on the
scorer and the arm.

**This is the mechanism behind section 1.** Coordinate noise perturbs the spectrum, and the
spectrum sets the phases on the time grid. A scorer whose value depends strongly on where the
grid ends is therefore a scorer that the spectrum can move. Document 47 gives the spectral
measurement: the gap varies by a factor of 21.7 across the four arms while the spectral range
varies by 1.09. A single wall-clock window therefore lands in a different physical regime on
each protein.

---

## 4. What reduces it: ensembling over perturbed structures

If a single structure gives an unstable ranking, average the ranking over a set of structures
that the input is equally consistent with. The construction reads no label:

1. Build K jittered copies of the apo structure, one per build seed.
2. Score each copy and convert each score to midranks.
3. Report the mean midrank.

**Held-out stability is measured on test seeds disjoint from the build seeds.** Without that
separation the measurement rewards the ensemble because it already saw the perturbation.

Mean over the 9 quantum scorers, test noise 0.50 Angstrom:

| K | Held-out stability | Mean AUC | Mean abs `rho` to distance |
| --- | --- | --- | --- |
| 1 | 0.581 | 0.519 | 0.496 |
| 4 | 0.760 | 0.524 | 0.564 |
| 8 | 0.829 | 0.501 | 0.594 |
| 16 | **0.888** | 0.504 | **0.613** |

**Stability rises by 0.31 and the endpoint does not move.** The mean AUC change from K=1 to
K=16 is −0.015, and the per-scorer changes run from −0.055 to +0.035. The largest single gain
is `spectral_participation_ratio`, from 0.332 to 0.816, with AUC up 0.028.

**The controls stay flat, which is what makes the result readable.**
`distance_from_source_negated` sits at 0.994 at K=1 and 0.994 at K=16.
`anm_perturbation_response` goes 0.969 to 0.982. Neither has instability to remove, so neither
gains. The ensemble acts on the quantum observables and not on the harness.

**Two costs, both of which must be reported.**

- **The distance correlation rises**, from 0.496 to 0.613. The ensemble buys stability partly
  because it moves each observable toward the consensus of its own jittered copies. That
  consensus is more distance-like than any single copy. Against document 46 this is the wrong
  direction.
- **K=16 means 16 times the circuit executions.** Under constraint C3 that multiplies the
  reported resource cost by 16 with no depth reduction. The trade is stability for shots.

---

## 5. What does not reduce it

**Dephasing does not, in any useful sense.** `dephased_transport` is the most stable quantum
scorer in the battery at `rho` = 0.957 under 1.00 Angstrom noise. It reaches that stability
because it drives the walk toward its classical limit, and its AUC sits near chance across the
tier. The observation generalises: within the quantum family, stability and quantum character
trade against each other along the dephasing axis. A fully dephased walk is stable because it is
no longer a quantum measurement.

**A per-protein window does not, because nothing selects it.** Section 3 shows the
optima are opposite on two arms. Any rule that picks the window must read something, and every
label-blind quantity tested so far fails to predict which direction the optimum lies.

**And a spectrally normalised clock does not either.** Section 6 measures it.

---

## 6. The timescale is not the sensitive factor

**Experiment:** `experiments/2026-08-26-timescale-normalisation` · 128 records · 4 arms ·
4 finite-window observables · 2 clocks · 8 windows.

Section 3 leaves an obvious remedy on the table. If the window means a different thing on each
protein, set the unit of time from a spectral quantity that tracks the difference.
`_time_grid` therefore accepts two clocks:

- `scale="range"` divides by the spectral range, the fastest phase in the operator. The range
  varies by 1.09 across the four arms, so this clock is close to a fixed wall clock.
- `scale="gap"` divides by the gap next to the dominant eigenvalue, the slowest beat the walk
  can produce. The gap varies by 21.7, so this clock adapts per protein. It reads only the
  graph's own spectrum and never a label.

**The disparity is real and now has a number.** At a nominal window of 50 under the `range`
clock, the four arms cover these many periods of their own slowest mode:

| Arm | Spectral range | Spectral gap | Slow periods at w=50 |
| --- | --- | --- | --- |
| `mkp5` | 18.094 | 0.23692 | 0.655 |
| `ptp1b` | 21.631 | 2.47385 | **5.718** |
| `hiv_rt` | 17.968 | 0.01766 | **0.049** |
| `ns5b` | 19.418 | 0.85700 | 2.207 |

A factor of 117 between `ptp1b` and `hiv_rt`. The `gap` clock removes it by construction: at
window w, every arm covers exactly w slow periods.

**It removes the disparity and it does not help.**

| Clock | Mean between-arm AUC spread | Best min-AUC over all settings |
| --- | --- | --- |
| `range` (5 windows) | 0.5627 | 0.375 |
| `gap` (3 windows) | **0.5516** | 0.355 |

The spread falls by 0.011, which is 2% of itself.

**The reason is a variance decomposition, and it is decisive.** For each observable and clock,
compare how much the window moves the AUC within one arm against how much the arm moves it at
one window:

| Clock | Observable | Within-arm (window) | Between-arm (protein) | Ratio |
| --- | --- | --- | --- | --- |
| `range` | `ctqw_average_transfer` | 0.079 | 0.668 | **8.5x** |
| `range` | `ctqw_peak_transfer` | 0.099 | 0.637 | 6.4x |
| `range` | `ctqw_temporal_variance` | 0.169 | 0.541 | 3.2x |
| `range` | `ctqw_coherent_source_contrast` | 0.300 | 0.405 | 1.3x |
| `gap` | `ctqw_average_transfer` | 0.045 | 0.650 | **14.5x** |
| `gap` | `ctqw_peak_transfer` | 0.059 | 0.602 | 10.2x |
| `gap` | `ctqw_temporal_variance` | 0.176 | 0.528 | 3.0x |
| `gap` | `ctqw_coherent_source_contrast` | 0.101 | 0.427 | 4.2x |

**The `gap` clock works exactly as designed and that is why it fails.** It cuts the window
sensitivity of `ctqw_average_transfer` almost in half, from 0.079 to 0.045, so the clock is a
correct normalisation. The between-arm spread does not move, so the variance it normalises away
was never the variance that matters. The ratio gets **worse**, not better, because the
denominator shrank.

**No setting is usable across the tier.** Of the 32 combinations of clock, window and
observable, **zero** place all four development arms above 0.5. The best is `range` at w=10 with
`ctqw_coherent_source_contrast`, whose worst arm sits at 0.375. Three of its four arms are below
chance and one is at 0.688.

`hiv_rt` scores 0.87 to 0.91 on `ctqw_average_transfer` at every window and under both clocks.
`ns5b` scores 0.16 to 0.26 on the same observable under the same conditions. No choice of clock
closes that.

**What this rules out.** Point 6 asked whether the instability yields to hyperparameter tuning.
For the time grid the answer is no, and the answer is not close. The observable's cross-protein
variance is a property of the protein and the observable, not of the clock. Section 4's ensemble
remains the only measured remedy, and it treats a different problem: it stabilises one protein
against perturbation, and it does nothing for the spread between proteins.

**One robustness check, and it passed.** The earlier window sweep used the default 128 steps.
A window of 100 needs at least 200 samples to satisfy Nyquist on the fastest phase, so those
rows were re-measured here with a derived step count. Across all 48 shared cells the largest
change in AUC is 0.002. The earlier numbers stand.

---

## 7. Stability and the distance confound are close to the same quantity

**Exploratory.** The hypothesis below follows section 1. It did not precede the data. The
pool is 30 scorers, the tests are not corrected for multiplicity, and nothing here is a
confirmatory claim. It is recorded because it explains section 5 and because it constrains what
a remedy can look like.

Section 1 ranks scorers by stability. Document 46 ranks the same scorers by their rank
correlation to distance from the source. The two orderings are close to the same ordering.

Spearman correlation between a scorer's mean stability at 1.00 Angstrom and its mean
absolute `rho` to negated distance, over all four arms:

| Family | n | Spearman | p |
| --- | --- | --- | --- |
| quantum | 22 | **+0.874** | < 0.0001 |
| classical | 8 | **+0.690** | 0.058 |
| pooled | 30 | +0.571 | 0.0010 |

**Inside the quantum family the two orderings are nearly the same ordering.** A rank correlation
of 0.874 over 22 scorers is not a tendency. Measure how much of a quantum score is distance,
and you have measured most of what decides its stability. The pooled figure is
weaker than either family alone, because the two families sit on different offsets.

**The mechanism is not subtle.** Distance from the source is a smooth function of the
coordinates. Perturb every atom by half an Angstrom and the distance ranking barely moves. An
interference term is a sum of oscillating phases whose frequencies come from the spectrum, and
the spectrum moves under the same perturbation. Any score that carries a large distance
component inherits the smoothness of distance. Any score built to cancel that component gives
the smoothness up with it.

**The endpoints of the table make the point on their own.**

| Scorer | Stability | abs `rho` to distance | Mean AUC |
| --- | --- | --- | --- |
| `distance_from_source_negated` | **0.978** | **0.978** | 0.581 |
| `dephased_transport` | 0.964 | 0.852 | 0.479 |
| `heat_kernel_from_source` | 0.956 | 0.847 | 0.520 |
| `quantum_best_case_transfer` | 0.795 | 0.783 | 0.528 |
| `ctqw_peak_transfer` | 0.669 | 0.718 | 0.541 |
| `connectivity_strength` | 0.529 | 0.427 | 0.625 |
| `ctqw_coherent_source_contrast` | 0.413 | 0.241 | 0.526 |
| `spectral_participation_ratio` | 0.307 | 0.345 | 0.489 |
| `energy_contrast` | **0.164** | **0.213** | 0.360 |

**This is the direct tension between two of the questions this session set out to answer.**
Reduce the distance dependence and the ranking becomes unstable. Stabilise the ranking and the
distance dependence comes back. Section 4 measures exactly that: the ensemble raises stability
from 0.581 to 0.888 and raises the distance correlation from 0.496 to 0.613 at the same time.
The two are not independent knobs.

**The trade is not forced, and the counter-example is classical.** `degree` sits at stability
0.878, absolute `rho` to distance 0.376 and mean AUC 0.692. It is stable, decorrelated and
predictive at once. `anm_perturbation_response` reaches stability 0.929 at `rho` 0.210, though
its AUC of 0.289 means it is anti-correlated with the labels and is not a candidate.

**No quantum observable reaches that quadrant.** Seven quantum scorers sit below `rho` 0.45,
and the most stable of them is `connectivity_eigencentrality` at 0.569. The rest run from 0.529
down to 0.164. The best of the seven on AUC is `connectivity_strength` at 0.625, and its top-5
Jaccard is 0.05. The quantum family currently buys decorrelation with instability, and where it
does buy some accuracy the deliverable does not survive the purchase.

**What this means for the pipeline.** Any candidate must be reported on three axes together:
AUC, absolute `rho` to distance, and stability at half an Angstrom. A method that reports the
first two and omits the third can pass for a distance-free advance and still be a coin flip on
the next crystal structure of the same protein.

---

## 8. What this section supports and what it does not

**Supported.**

- The §4.2 noise-resilience requirement is answered with a measurement over three perturbation
  types, three magnitudes and five seeds.
- The quantum observables are less stable than the classical battery by a wide and consistent
  margin, and the coherence window is a demonstrated mechanism for that.
- Rank-mean ensembling raises held-out stability from 0.581 to 0.888 with no change to the
  endpoint, and the controls confirm that it acts on the unstable scorers only.
- Source loss is not a significant instability. The method tolerates an imperfect active site.
- The time grid is not the sensitive factor. Between-arm variance is 1.3 to 14.5 times the
  within-arm window variance, and a spectrally adapted clock does not reduce it.
- Within each family, stability and the distance component rise together (Spearman +0.874
  quantum over 22 scorers, +0.690 classical over 8). `degree` shows the trade is not forced,
  and no quantum observable matches it.

**Not supported.**

- No claim that the stabilised quantum scorers beat the distance baseline. They do not, and the
  ensemble makes them more distance-like rather than less. Document 46 is the authority.
- **Section 7 is exploratory, not confirmatory.** The hypothesis followed the data and the p
  values are uncorrected. The quantum figure is strong (+0.874 over 22 scorers) and the
  classical one is not (+0.690 over 8, p = 0.058). It explains a pattern. It does not
  establish one.
- No claim that source loss is mild on a small active site. On `ns5b` the frozen site has
  three residues, so leave-one-out removes a third of the source, and the worst quantum cell
  falls to `rho` = 0.163.
- No claim that 16 copies is the right K. The sweep stops at 16 because the curve flattens
  there, not because 16 was shown to be optimal.
