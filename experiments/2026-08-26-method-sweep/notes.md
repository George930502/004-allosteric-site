# method-sweep-on-the-development-tier

**Date:** 2026-08-26 · **Config:** `config.yaml` · **Records:** 6 480 · **Metrics:** `metrics.json`

Full write-up, with the fusion and mechanism probes beside it:
`docs/method/exploration/results/40-method-sweep.md`.

> **STALE COLUMNS — measured 2026-09-02, third audit pass.** Every record here carries
> `protocol_frozen_on: 2026-08-25`. The evaluation protocol is **version 3**, frozen
> 2026-09-02, and its decoy detector was re-frozen with it (ADR 0030). 216 records were
> re-scored through the current `score_arm` — all 54 swept scorers on all four `development`
> arms. What that measured:
>
> | field                                                            | moved   |
> | ---------------------------------------------------------------- | ------- |
> | every `nulls.decoy_pockets` field, and `auc_roc_vs_decoy_linings` | ~all    |
> | `dcc_angstrom`                                                   | 6 / 216 |
> | `mean_rank`, `auc_roc`, `auc_pr`, `precision_at_5`, `hits_at_5`, `recall_at_5` | 0 / 216 |
> | `nulls.matched_patch.p_calibrated`                               | 0 / 216 |
>
> **Read the decoy columns and `auc_roc_vs_decoy_linings` as version-1 numbers.** Everything
> else below still reproduces. The screening statistic is `mean_auc_roc`, which did not move,
> so the selection this run made stands.
>
> The six `dcc_angstrom` moves are all on `hiv_rt` and all downward: `degree` and
> `contact_number` 32.530 -> 21.655, `clustering_coefficient` 30.006 -> 18.212,
> `sequence_distance_from_source_negated` 13.014 -> 9.164, `hop_distance_from_source_negated`
> and `ohm_path_probability` 11.788 -> 10.654. Cause is the 2026-09-02 `top_k_indices` repair,
> which stopped breaking ties with the answer key. The old rule sorted positives last inside a
> tie, so it reported the site as further away than it was.
>
> **Not re-run, deliberately.** A refresh costs about 2.4 hours and would change no number that
> decided anything. It also cannot be done in place: the resume key is
> `arm|graph|scorer|detrend` and does not carry the protocol version, so a re-run appends
> nothing until `records.jsonl` is deleted. See
> `docs/benchmark/review/26-third-pass-synthesis.md` items 5.18 and 5.21.

## Question

Across every graph, scorer and confound-removal form we can build from the frozen apo input
alone, which combinations rank the ground truth above the frozen nulls, and by how much?

## Setup

Eight graphs × 54 scorers × 3–5 confound-removal forms, on the four `development` arms and
nowhere else. Every number comes from one call to `allo.scoring.score_arm`. See
`config.yaml` for the knobs. The two extra detrend forms run on three graphs rather than
eight, which `config.yaml` states and `40-method-sweep.md` §5 tests.

The 54 scorers are 30 `baselines`, 9 `coupling`, 4 `mechanism` and 11 `quantum`. All 54
completed on all four arms. Nothing was refused for size: the largest development arm holds
553 residues and the dephasing solve admits 620.

## Result

**Zero of 1 620 complete variants reject the matched-patch null on all four arms**, at 0.05
or at 0.05/4. The distribution is 1 338 / 492 / 93 / 0 / 0 across the three runners' 1 923
variants.

| Leader                                                   | mean AUC | min AUC | hits@5 | rej | \|ρ\| |
| -------------------------------------------------------- | -------- | ------- | ------ | --- | ----- |
| `evaluation_default` `eigenvector_centrality` `binned_median` | **0.810** | 0.703 | 2 | 2 | 0.00 |
| `heavy_exponential` `eigenvector_centrality` `binned_rank`    | 0.779 | 0.663 | **6** | 1 | 0.06 |

Per-axis means. Graph: 0.501 to 0.532, a spread of 0.031, with seven of eight inside 0.013.
Detrend: `raw` highest mean at 0.552 and lowest maximum at 0.765, every detrended form lower
in the mean and higher at the top.

Quantum against classical, paired inside each of the 30 (graph, detrend) cells: classical
wins **30 of 30**, mean difference **+0.196** AUC, bootstrap 95 % CI [+0.181, +0.212]. A
size-matched control drawing 11 classical scorers at random 2 000 times beats the quantum
set in **1 999 of 2 000** draws.

## Interpretation

**The screen cannot confirm a method, and the leader sits at the noise ceiling.** A
label-blind screen of this size produces a 95th-percentile best-of-3000 mean AUC of 0.810
(`2026-08-26-selection-power`). The best variant here reaches 0.810. Read every number in
this run against that ceiling and never against 0.5.

**The graph axis is flat, which refutes a working assumption of the Phase-2 plan.** The
contact definition was expected to be high-leverage. It is worth 0.031 AUC across eight
variants, and the edge-class weighting built to carry hydrogen bonds and salt bridges ranks
seventh of eight.

**Detrending lowers the mean and raises the maximum, and that pattern is the finding.** Most
scorers lose their AUC when the distance component goes, because the distance component was
carrying it. The few that keep it are the ones worth taking forward.

**The quantum result is measured, and it is narrower than it looks.** Eleven observables, one
source definition, two Hamiltonians. Nine of the eleven correlate with negated distance at
|ρ| 0.726 to 0.822, so they measure hop count from the active site. What stays open is a
different source, a chemistry-weighted Hamiltonian, and an observable that reads a spectral
rather than a transport feature. `ctqw_infinite_time_average` reaches AUC 0.824 on `hiv_rt`,
above the classical leader on that arm, and 0.377 on `ns5b`. The family is not uniformly
worse. It is more variable, and the variance is what sinks the mean.

**What would stop us believing this.** A variant that rejects the matched-patch null on all
four arms at 0.05/4, with |ρ| against negated distance below 0.30. None of 1 923 does.
