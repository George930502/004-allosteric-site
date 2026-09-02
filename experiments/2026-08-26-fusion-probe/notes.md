# fusion-probe

**Date:** 2026-08-26 · **Config:** `config.yaml` · **Records:** 972 (regenerated after the sink-solve repair, see below) · **Metrics:** `metrics.json`

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

The method sweep asks which single score is best. This asks three further questions. Does
combining several beat any of them? Does spatial smoothing help, given that a site is a patch
and not a residue? And does the top-5 assembly rule change the deliverable?

## Setup

Four `development` arms, three graphs, three confound-removal forms, three
correlation-clustering cuts, four smoothing radii, two member orientations, and three
non-zero exclusion radii for the assembly pass.

**Consensus membership is chosen without a label.** The scorers are clustered by the absolute
rank correlation of their own score vectors, and a scorer joins unless it duplicates one
already kept. Picking members by their AUC would be selection on the outcome. Picking them by
their mutual correlation is not, because the correlation matrix never sees a label. Membership
runs from 9 to 13 scorers depending on the arm and the cut.

**The `pc1` orientation is the same idea applied to signs.** A rank average assumes every
member points the same way, and two members of this pool do not. Aligning each member to the
leading eigenvector of the members' own correlation matrix fixes that and reads no label.
`none` is the control.

## Result

Best by mean AUC over all four arms — `heavy_inverse_square`, raw, cut 0.5, no smoothing,
`pc1`:

| Arm | AUC | hits@5 | recall@5 (chance) | DCC Å (chance) | calibrated p | rho vs negated distance |
| --- | --- | --- | --- | --- | --- | --- |
| `hiv_rt` | 0.857 | 3 | 0.188 (0.009) | 6.8 (25.0) | 0.146 | +0.55 |
| `mkp5` | 0.826 | 2 | 0.182 (0.037) | 8.4 (12.0) | 0.063 | +0.50 |
| `ptp1b` | 0.791 | 0 | 0.000 (0.017) | 13.5 (17.6) | 0.110 | +0.47 |
| `ns5b` | 0.586 | 0 | 0.000 (0.009) | 29.5 (23.4) | 0.529 | +0.79 |

**Mean AUC 0.765, minimum 0.586, five hits at 5, and zero arms rejecting the null.**

| Comparison | mean AUC | min AUC | hits@5 | arms rejecting | mean DCC Å |
| --- | --- | --- | --- | --- | --- |
| `pc1`, no smoothing | **0.765** | 0.586 | 5 | 0 | 14.6 |
| `pc1`, smoothing 9.0 Å | 0.735 | 0.495 | **6** | 0 | **14.2** |
| `none`, no smoothing | 0.741 | 0.566 | 3 | 1 | 19.5 |

**These numbers were regenerated.** The first pass included three sink-based quantum
observables as consensus members, and those were numerically broken on `hiv_rt` — the
Sylvester solve returned survival times of the wrong sign and 1e13 in magnitude. The scorers
were repaired with a uniform background decay and a positivity check, and every record here
was recomputed. The first pass reported mean AUC 0.775; the corrected figure is 0.765. The
qualitative conclusions below did not change, which is itself worth recording.

## Interpretation

**Sign alignment is worth more than any other knob here, and it costs nothing.** It raises the
mean AUC from 0.741 to 0.765, the worst arm from 0.566 to 0.586, and the mean DCC from 19.5 A
to 14.6 A. The clearest single case is `ptp1b`: 0.566 unoriented against 0.791 aligned, because
two members run backwards and cancel the rest. The fix reads no label.

**Spatial smoothing trades the endpoint for the deliverable, and the trade is measurable.**
At 9.0 Å the mean AUC falls 0.765 → 0.735 while hits at 5 rise 5 → 6 and mean DCC falls
14.6 Å → 14.2 Å. On `hiv_rt` recall@5 goes 0.188 → 0.250 against a chance line of 0.009.
The confirmatory endpoint and the five-residue list are different claims, and this is the
clearest measurement of that in the repository after the `cavity_volume` example. **A method
frozen for the challenge should smooth. A method frozen for the confirmatory test should
not.** That choice has to be made once and written into an ADR.

**The assembly rule changes almost nothing.** A diversified top-5 at 6 Å and at 8 Å gives the
same AUC and the same hits as a plain cut, and at 12 Å it loses one hit. On this benchmark the
consensus does not put five residues in one pocket often enough for the exclusion to bite.

**And now the caveat that outranks all three.** The consensus correlates with negated distance
to the active site at **+0.47 to +0.79**. It is largely a distance score. That is why the AUC
looks strong and the calibrated p does not: the matched-patch null is matched on geometry, so
it absorbs exactly this. The best variant rejects on **zero of four arms**. The best _any_
consensus variant manages is one arm, and the variant that manages it — unoriented, `mkp5`,
p = 0.0132 — is at AUC 0.566 on `ptp1b`.

**Read against the ceiling, not against 0.5.** A label-blind screen of this size reaches a
median mean AUC of 0.771 (`2026-08-26-selection-power`). The best fusion variant reaches 0.765.
**The best result in this experiment is below the median of what noise produces at this screen
size.**

**What would change the conclusion.** A consensus whose rank correlation against negated
distance is below 0.3 and whose calibrated p clears 0.05/4 on all four arms. The member pool
already excludes five distance-like scorers; excluding more, or detrending each member before
averaging rather than after, is the untested variant that could produce one. The detrended
members were swept — `exponential` and `binned_median` — and they rank below `raw`, which is
itself evidence that the distance component is carrying the AUC.
