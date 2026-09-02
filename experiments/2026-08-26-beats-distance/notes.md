# beats-distance

**Date:** 2026-08-26 · **Config:** `config.yaml` · **Records:** 276 · **Metrics:** `metrics.json`

## Question

Every result in `docs/method/exploration/results/` carries the same caveat: the score correlates
0.65 to 0.85 with Euclidean distance to the active site. Does anything in the battery add signal
**over** that baseline?

## Setup

Sixty-nine scorers — 44 classical and 25 quantum, including the three families added on
2026-08-26 — on four `development` arms, on the evaluation-default graph. Each is put through two
frozen tests: `score_arm` for the confirmatory endpoint, and `compare_methods` paired against
`distance_from_source_negated` and against `eigenvector_centrality`. No statistic is invented
here; `compare_methods` was frozen before any method existed (ADR 0025).

## Result

| Comparison | Paired tests | Scorer leads | Wins at uncorrected p ≤ 0.05 | Expected by chance |
| --- | --- | --- | --- | --- |
| vs distance | 272 | 125 | 7 | 6.8 |
| vs eigenvector centrality | 272 | 100 | 0 | 6.8 |

Holm over the battery rejects nothing on any arm.

**The Holm result is uninterpretable on two arms and the experiment says so.** The smallest
calibrated p anywhere in the 272 tests is 0.001080, because `compare_methods` reads its p from a
permutation pool. Holm's first step needs `0.05 / m`:

| Arm | m | Needs | Floor | Can reject? |
| --- | --- | --- | --- | --- |
| `hiv_rt` | 2 | 0.025000 | 0.001080 | yes |
| `mkp5` | 12 | 0.004167 | 0.001080 | yes |
| `ptp1b` | 55 | 0.000909 | 0.001080 | no, at any data |
| `ns5b` | 56 | 0.000893 | 0.001080 | no, at any data |

The useful quadrant — mean AUC above 0.55 and mean absolute rho against distance below 0.35 —
holds four scorers, all classical: `gnm_entropy_response` (0.704 / 0.257),
`stiff_corridor_to_source` (0.684 / **0.057**), `gnm_transfer_entropy` (0.584 / 0.207),
`core_number` (0.575 / 0.279). No quantum observable enters it.

## Interpretation

**Nothing in the battery beats distance more often than chance, and nothing beats eigenvector
centrality at all.** Seven of 272 against 6.8 expected is not a signal.

**The quantum layer is caught in a trade.** Its accurate observables are accurate because they
are distance (rho 0.66 to 0.85). Its distance-orthogonal observables sit at chance (AUC 0.36 to
0.53). None is both.

**This does not refute the approach; it locates the limit.** Every scorer here is a function of
one contact graph and its geometry, and `docs/method/review/13-graph-construction.md` shows that
class inherits distance by construction. The descriptors that survive the confound in the
literature — local energetic frustration, cavity geometry, contact area rather than contact
distance — are not in this battery because they are not functions of the contact graph. That is
the next experiment.

**Two fixes for the resolution problem, and they are different decisions.** Enlarge the
permutation pool, at linear compute cost and no protocol change. Or pre-register a small
candidate set so the family is small, which is what the `development` tier exists to allow. The
second is better: a battery of 69 is a screen and a screen was never meant to carry a corrected
claim.

Full write-up: `docs/method/exploration/results/46-beats-distance.md`.
