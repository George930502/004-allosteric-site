# stability-and-source

**Date:** 2026-08-26 · **Config:** `config.yaml` · **Records:** 5222 · **Metrics:** `metrics.json`

## Question

`CHALLENGE.md` §4.2 asks for a noise-resilience study. The method sweep left a second question
open: the quantum observables move a long way between arms and between runs, and nothing so far
says how much of that is the input and how much is the observable.

Four perturbations answer both. Three disturb the input and one disturbs the algorithm.

## Setup

Four `development` arms, the evaluation-default graph, and the frozen scoring harness.

- **Coordinate noise.** Gaussian displacement of every atom at sigma in {0.25, 0.50, 1.00}
  Angstrom, five seeds each. The graph is rebuilt after the displacement, so contacts near the
  cutoff appear and disappear. This is the physical question: does a different crystal of the
  same protein give the same answer?
- **Edge dropout.** Removal of a fraction f in {0.02, 0.05, 0.10} of contacts, five seeds each.
  The geometry is held fixed, which separates "sensitive to coordinates" from "sensitive to
  which contacts exist".
- **Source dropout.** One active-site residue removed, once per residue, capped at 11.
- **Coherence window.** The walk's time window shortened to {5, 10, 25, 100} against a baseline
  of 50. A device with a short T2 cannot run the long window.

Four readouts per record: `rho_to_baseline` for rank stability, `delta_auc` for endpoint
stability, `top5_jaccard` for stability of the deliverable, and `rho_to_distance` so that a
scorer cannot look stable merely by being a distance ranking.

## Result

**Mean `rho` over four arms, 20 perturbed graphs per cell:**

| Family | coord 0.25 | coord 0.50 | coord 1.00 | edge 0.02 | edge 0.05 | edge 0.10 |
| --- | --- | --- | --- | --- | --- | --- |
| classical (8) | 0.962 | 0.946 | **0.908** | 0.987 | 0.978 | 0.955 |
| quantum (22) | 0.711 | 0.666 | **0.629** | 0.783 | 0.724 | 0.680 |

**The twenty least stable scorers in the battery are all quantum**, from 0.164 to 0.795 at 1.00
Angstrom. The first classical entry appears at 0.827. `distance_from_source_negated` is the most
stable scorer at 0.978 and `energy_contrast` the least at 0.164.

`symmetry_dark_overlap` and `degenerate_mixing_weight` return a constant on every arm, which
leaves the rank correlation undefined. They are dropped from every table here. That is the
symmetry branch of document 47 confirmed on four arms rather than argued.

**The top-5 list is far less stable than the ranking, for every method.** At 0.50 Angstrom,
`distance_from_source_negated` holds `rho` = 0.993 and a top-5 Jaccard of **0.46**.
`eigenvector_centrality`, the best classical scorer in the method sweep at AUC 0.759, holds a
Jaccard of 0.38. The confirmatory endpoint is stable and the deliverable is not, and this is not
a quantum problem.

**For the newer quantum families the top-5 list is gone.** `spectral_participation_ratio` holds
a Jaccard of **0.01**, `connectivity_strength` **0.05** and `connectivity_eigencentrality` 0.07.
`connectivity_strength` reaches mean AUC 0.625, among the better quantum figures in the
repository, and one residue in twenty survives from its top-5 list to that of a copy of the same
protein displaced by half an Angstrom.

**Two scorers are exactly invariant under edge dropout**, `distance_from_source_negated` and
`anm_perturbation_response`, because neither reads the edge set. That is the control behaving
as designed rather than a result.

**Source loss is mild on average and severe on one arm.** The quantum mean is `rho` = 0.947
against 0.997 classical, with a worst quantum cell of 0.163 and a largest AUC change of −0.221.
The frozen active sites are not the same size: 11 residues on `mkp5` and `ptp1b`, 9 on `hiv_rt`
and **3 on `ns5b`**. Leave-one-out therefore removes a third of the source on `ns5b`, and every
one of the five worst cells is on `ns5b` or on `energy_contrast`. Restricted to the three arms
with nine or more source residues, the quantum mean rises to 0.973 and the worst cell to 0.508.

## Interpretation

**Stability tracks the distance component, within each family.** Spearman correlation between a
scorer's stability at 1.00 Angstrom and its absolute `rho` to negated distance: **+0.874** over
22 quantum scorers (p < 0.0001) and **+0.690** over 8 classical ones (p = 0.058). Pooled it is
+0.571 over 30 (p = 0.0010), weaker than either family, because the two sit on different
offsets.

This is exploratory. The hypothesis followed the data and the p values are uncorrected. It is
recorded because it explains the rest of the table: distance is a smooth function of the
coordinates, an interference term is a sum of phases set by a spectrum that moves under the same
perturbation, and a score built to cancel the distance component gives up the smoothness with
it.

**`degree` shows the trade is not forced.** Stability 0.878, absolute `rho` to distance 0.376,
mean AUC 0.692. No quantum observable reaches that quadrant. Seven quantum scorers sit below
`rho` 0.45 and the most stable of them reaches 0.569. The best of the seven on AUC is
`connectivity_strength` at 0.625, whose top-5 Jaccard is 0.05.

**`dephased_transport` is the most stable quantum scorer at 0.964, and that is the warning.** It
reaches that number because it drives the walk toward its classical limit. Its AUC is 0.479.

## Two corrections recorded rather than hidden

**The window rows for `quantum_perturbation_response` were wrong on the first pass, and were
recomputed.** The memo key in `allo.quantum.walk` omitted `window`, so the second and later
calls at a different window returned the first call's cached result. The signature was `rho` to
baseline of exactly 1.0000 at every window, which cannot be right. The key now carries `steps`
and `window`. Only the window sweep was affected — every other experiment used the default
window, so no earlier number changes. The stale rows were deleted and re-run.

**A second pass extended the scorer pool.** The first pass loaded `allo.quantum.SCORERS` before
the interference, connectivity and quantumness modules were added to it, so it covered 11
quantum observables over 3010 records. The re-run for the window repair picked up all 25 and
took the file to 5222. The tables above cover the 30 scorers whose coverage is complete on all
four arms, so no partial cell enters a mean. The extension changed the conclusions: the quantum
family mean fell from 0.717 to 0.629 and the stability-against-distance correlation rose from
+0.648 to +0.874.

## What would change the conclusion

A quantum observable at stability above 0.85 with absolute `rho` to distance below 0.45 and an
AUC above chance. Nothing in the current battery is within reach of it, and section 7 of
`docs/method/exploration/results/44-stability-and-noise.md` explains why the two requirements
pull against each other.
