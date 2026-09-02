# mechanism-probe

**Date:** 2026-08-26 · **Config:** `config.yaml` · **Records:** 240 · **Metrics:** `metrics.json`

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

Across the seven systems whose allosteric mechanism is mapped residue by residue in the
primary literature, three structural signatures recur, are visible in an apo structure alone,
and were not in this repository. Do any of them rank the label set on the `development` tier?

The three are stated in `docs/method/exploration/lit/26-system-mechanisms.md` and implemented
in `src/allo/classical/mechanism.py`.

## Setup

Four `development` arms, three graphs, five confound-removal forms, four scorers. Every
number comes from `allo.scoring.score_arm`, the same call the method sweep makes, so the two
experiments' records are directly comparable.

The fourth scorer was added after the first pass. `soft_corridor_to_source` implements the
published prediction; `stiff_corridor_to_source` is the same score with the sign reversed.

## Result

| Scorer                     | Best mean AUC                                   | Min AUC over arms | Hits@5 | Arms rejecting the matched-patch null | Best rho vs negated distance |
| -------------------------- | ----------------------------------------------- | ----------------- | ------ | ------------------------------------- | ---------------------------- |
| `stiff_corridor_to_source` | **0.714** (`evaluation_default`, `exponential`) | 0.605             | 2      | **0 of 4**                            | −0.12                        |
| `strain_versus_diffusion`  | 0.669 (`cb_10`, `binned_median`)                | 0.443             | 1      | 0 of 4                                | −0.85 raw                    |
| `module_boundary`          | 0.522 (`heavy_inverse_square`, `raw`)           | 0.343             | 2      | 0 of 4                                | +0.23                        |
| `soft_corridor_to_source`  | 0.346                                           | 0.207             | 1      | 0 of 4                                | +0.05                        |

Per arm, `stiff_corridor_to_source` on the default graph, raw: mkp5 0.650, ptp1b 0.676,
hiv_rt 0.652, ns5b 0.756. Calibrated p from the matched-patch null: 0.345 to 0.411.

DCC against its own chance line, same variant: mkp5 12.0 against 12.0, ptp1b 26.5 against
17.6, hiv_rt 38.0 against 25.0, ns5b 17.2 against 23.4.

## Interpretation

**Three findings, and none of them is a method.**

**1. The soft-corridor prediction is refuted, and its inverse carries the signal.** An evolved
elastic network develops a _less_ constrained channel between two coupled sites
(doi:10.1073/pnas.1615536114). Measured here, the score runs the wrong way: mean AUC 0.31 to
0.35 in every one of five confound-removal forms and on all three graphs. The rank
correlation against negated distance to the active site is **0.05**, so this is not the
distance confound wearing a new name, and the consistency across four unrelated proteins is
not noise. The residues in these label sets sit on the _constrained_ side of the
coordination-deficit axis.

The sign is a free parameter, and this tier is where a free parameter is fixed (ADR 0021).
It is now fixed. What must not happen is quoting 0.714 as a discovery: it is one minus a
number that was measured first, and the report has to print both.

**2. The best score in this experiment still rejects nothing.** `stiff_corridor_to_source`
beats chance on all four arms and is nearly orthogonal to distance, which is more than most
of the standard battery manages. It does not come close to the frozen minimum detectable
effect, which is AUC 0.762 to 0.936 at α and 0.799 to 0.961 at α/3
(`experiments/REGISTRY.md`, 2026-08-25). Calibrated p runs 0.22 to 0.62. On three of four
arms its five-residue centre is _farther_ from the site than a random five would be.

**3. The module-boundary hypothesis does not transfer.** It has the most independent systems
behind it — eight — and the only allosteric-specific published effect size of the three
(PPV 0.65 at sensitivity 0.22, doi:10.1186/1471-2105-13-273). On these four arms it sits at
chance, 0.44 to 0.52, in every combination. Recorded as a negative result, not deleted.

**What would change these conclusions.** For finding 1: a graph or a depth-binning rule under
which the soft direction scores above 0.5 on more than one arm. The construction bins the
coordination deficit inside deciles of distance to the chain centroid, and a different burial
definition is a real alternative that was not swept. For finding 3: `module_boundary` uses the
sign word of the lowest three Laplacian modes; a partition from a different mode count, or
from spectral clustering rather than sign words, is untested.

**What this does not settle.** Nothing about the primary benchmark, which is not touched by a
screen. Four arms cannot separate 0.65 from 0.70, and
`docs/method/exploration/results/41-selection-and-power.md` says by how much.
