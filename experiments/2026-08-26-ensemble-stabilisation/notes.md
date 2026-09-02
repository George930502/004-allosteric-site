# ensemble-stabilisation

**Date:** 2026-08-26 · **Config:** `config.yaml` · **Records:** 352 · **Metrics:** `metrics.json`

## Question

`2026-08-26-stability-and-source` found that coherent walk observables lose their ranking under
coordinate noise while classical ones keep theirs, and that dephasing buys stability only by
giving up the coherence. Is there a remedy that keeps the coherence?

A deposited structure is one sample from a conformational ensemble. So the expectation of an
observable over that uncertainty is a more honest estimator than its value at one point. Does
that estimator hold its ranking, and does it keep its accuracy?

## Setup

Four `development` arms. The estimator is the **rank mean over K jittered structures**, K in
{1, 4, 8, 16}, jitter sigma in {0.25, 0.5} Å. Ranks rather than raw values, because the
observables span orders of magnitude between residues and an arithmetic mean would be whichever
structure produced the largest numbers.

**The test perturbation is held out.** Stability is the rank correlation between the estimator on
the reference structure and the same estimator on a structure displaced by 0.5 Å, using three
test seeds drawn from a range disjoint from the sixteen ensemble seeds. Averaging over the same
noise the estimator is tested on would measure nothing.

Sizes are nested, so each seed is scored once and the sizes are prefix means of the result.
`dephased_transport` and `connectivity_entropy` are excluded on cost, which `config.yaml` records:
both run about ten seconds per structure on the two large arms, and neither has anything to gain.

## Result

Held-out stability and mean AUC, K = 1 against K = 16, at sigma 0.5:

| Scorer | Stability K=1 | Stability K=16 | Gain | AUC K=1 | AUC K=16 | ΔAUC |
| --- | --- | --- | --- | --- | --- | --- |
| `spectral_participation_ratio` | 0.332 | **0.816** | **+0.484** | 0.489 | 0.517 | +0.028 |
| `ctqw_temporal_variance` | 0.495 | 0.834 | +0.340 | 0.520 | 0.491 | −0.029 |
| `oscillation_ratio` | 0.544 | 0.872 | +0.328 | 0.507 | 0.453 | −0.055 |
| `coherent_source_ratio` | 0.535 | 0.855 | +0.320 | 0.533 | **0.552** | **+0.019** |
| `ctqw_coherent_source_contrast` | 0.516 | 0.832 | +0.315 | 0.526 | 0.524 | −0.002 |
| `interference_excess` | 0.644 | 0.926 | +0.282 | 0.517 | 0.477 | −0.040 |
| `ctqw_peak_transfer` | 0.690 | 0.948 | +0.258 | 0.541 | 0.534 | −0.007 |
| `ctqw_average_transfer` | 0.799 | 0.977 | +0.177 | 0.524 | 0.512 | −0.011 |
| `anm_perturbation_response` (control) | 0.969 | 0.982 | +0.013 | 0.289 | 0.287 | −0.002 |
| `distance_from_source_negated` (control) | 0.994 | 0.994 | +0.000 | 0.581 | 0.583 | +0.002 |

## Interpretation

**Structural ensembling closes almost the whole stability gap, and it is nearly free.** The eight
coherent observables move from 0.33–0.80 to 0.82–0.98, which is the range the classical controls
already occupied. The controls do not move, which is the check that the gain is real: an
estimator that was already stable has nothing to average away.

**Accuracy is essentially unchanged.** Every ΔAUC lies between −0.055 and +0.035. Two scorers
improve on both axes at once: `coherent_source_ratio` gains 0.320 stability and 0.019 AUC, and
`spectral_participation_ratio` gains 0.484 stability and 0.028 AUC.

**So the answer to "how do we lower the instability" is neither dephasing nor hyperparameter
tuning.** It is to stop treating one deposited structure as the input. The cost is a factor of K
in compute and nothing else, and K = 16 is enough: the gain from 8 to 16 is small compared with
the gain from 1 to 4.

**What this does not fix.** Stability is not accuracy. Every scorer in the table above except the
distance control sits between 0.45 and 0.57 AUC after ensembling, which is chance. A stable
estimate of an uninformative quantity is still uninformative. Read this alongside
`docs/method/exploration/results/46-beats-distance.md`, which is where the accuracy verdict lives.

**Sigma barely matters.** The 0.25 Å and 0.5 Å rows differ by less than 0.05 in stability gain
everywhere. The mechanism is averaging over an ensemble, not the width of the ensemble.

Full write-up: `docs/method/exploration/results/44-stability-and-noise.md`.
