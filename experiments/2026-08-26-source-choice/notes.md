# source-choice

**Date:** 2026-08-26 · **Config:** `config.yaml` · **Records:** 760 · **Metrics:** `metrics.json`

## Question

`CHALLENGE.md` §4.1 asks for connectivity "in most cases" to an active site. Two questions
follow. Does a label-blind alternative source do as well as the frozen catalytic site? And does
a random size-matched source do as well, which would mean the source carries nothing?

## Setup

Four `development` arms, the evaluation-default graph, and six source families, each size-matched
to that arm's frozen active site and derived from the apo entry alone: `catalytic`,
`eigenvector_centrality`, `degree`, `buried` (lowest protrusion index), `fiedler` (largest
absolute Fiedler amplitude), and `random` at five seeds. Nineteen source-conditioned scorers,
plus `degree` as an invariance check — it ignores the source, so its score must be identical in
every row of an arm.

## Result

**The invariance check passed on all four arms**: one distinct `degree` checksum per arm.

| Source | Mean AUC | Worst AUC | Reject rate | Hits@5 per record | Between-arm spread |
| --- | --- | --- | --- | --- | --- |
| `degree` | 0.705 | 0.425 | 0.171 | 0.395 | 0.237 |
| `eigenvector_centrality` | 0.687 | 0.181 | 0.066 | 0.592 | 0.394 |
| `buried` | 0.600 | 0.277 | 0.013 | 0.421 | 0.272 |
| `catalytic` | 0.564 | 0.129 | 0.118 | 0.526 | 0.486 |
| `random` | 0.543 | 0.085 | 0.076 | 0.182 | 0.109 |
| `fiedler` | 0.527 | 0.230 | 0.026 | 0.026 | 0.348 |

The catalytic site is fourth of six on mean AUC and 0.021 above random. It is best for none of
the nineteen scorers; `degree` is best for thirteen.

## Interpretation

**Source conditioning carries information, and the active site is not the best use of it.**
Catalytic beats random on the confirmatory endpoint (0.118 against 0.076) and on the deliverable
(0.526 hits at 5 per record against 0.182), so the propagation framing is not decoration. But
three label-blind alternatives beat it on AUC.

**The variance is the finding, not the mean.** The catalytic source has the largest between-arm
spread of any source tested: 0.809 on `hiv_rt` and 0.323 on `ns5b`. The degree source never
reaches 0.809 and never falls below 0.608. So the active site is the right source for some
proteins and the wrong source for others, and which is which is not knowable without a label.
That is one named cause of the per-protein heterogeneity the method sweep could not explain.

**Quantum and classical respond identically.** The source ordering is the same in both families
and the classical row is above the quantum row at every source, so this is a pipeline-stage
decision and not a quantum-layer one.

**What this is not.** Six source families compared on four arms with the best chosen afterwards
is a screen, and it carries the multiplicity `41-selection-and-power.md` prices. A source rule is
a hyperparameter: chosen on `development`, then frozen and scored once.

Full write-up: `docs/method/exploration/results/45-source-choice.md`.
