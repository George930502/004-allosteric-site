# 0032 — The claim threshold is its own confirmatory family, corrected over three arms

**Status:** accepted · 2026-09-02 · part of evaluation **protocol version 3** · amends
[ADR 0025](0025-the-size-rescale-is-calibrated-at-every-holm-level.md)

## Context

ADR 0025 raised the bar for a claim. Clearing the matched-patch null is a low bar, because a
trivial geometric baseline clears it: rank each residue by the volume of the largest cavity
that lines it — label-blind, apo-only, zero-parameter — and `cavity_volume` rejects on all
three confirmatory arms. The claim threshold therefore became **beating `cavity_volume`**, and
`evaluation/README.md` §13 states it as the gate before any number is quotable.

`evaluation/README.md` §8 declares one confirmatory family: the three matched-patch tests on
the `corrected` arms, Holm-corrected at α = 0.05. It then declares **everything else
descriptive and not FWER-protected**, including every baseline comparison.

Those two statements contradict each other. The load-bearing comparison — the one that decides
whether a result may be claimed — sits in a family the protocol declares unprotected, across
nine required baselines and however many methods `classical.SCORERS` and `quantum.walk.SCORERS`
supply. A reviewer finds this in five minutes.

The machinery is already correct. `allo.scoring.harness.compare_methods` is paired on the
residue: it differences the two midrank vectors and tests the difference's patch mean against
the same matched-patch pool the confirmatory test uses. That is stronger than the field's
usual recommendation for two methods, because it is paired **within** an instance rather than
across instances. It returns `mean_rank_difference` and `auc_roc_difference` beside `p` and
`p_calibrated`, so an effect size already prints with the p-value. `holm()` exists. It is
wired to the matched-patch family only.

What is missing is a declaration, not an implementation.

## Decision

**Declare a second confirmatory family, and declare it now, before any method is scored.**

|                           | family 1                                                                | family 2                                                |
| ------------------------- | ----------------------------------------------------------------------- | ------------------------------------------------------- |
| test                      | matched-patch permutation against the null                              | paired `compare_methods` against `cavity_volume`        |
| arms                      | `kras_g12c_corrected`, `bcr_abl1_corrected`, `cardiac_myosin_corrected` | the same three                                          |
| correction                | Holm over 3                                                             | Holm over 3                                             |
| sided                     | upper, one-sided                                                        | two-sided, as already frozen                            |
| α                         | 0.05                                                                    | 0.05                                                    |
| what a rejection licenses | the arm has signal against matched background                           | the method beats the pre-declared reference on that arm |

The reference is `cavity_volume` and only `cavity_volume`. It was pre-declared in ADR 0025,
so this adds no freedom: the family size is fixed at three by the arms, not by the number of
methods a run happens to produce.

**Every other baseline comparison is descriptive.** The eight other required baselines, the
`mandated` arms, the distance-matched null, the decoy-pocket test and the whole `development`
tier all produce p-values and none is a decision. Label them that way in the report.

**Two-sided stays.** Between two methods there is no asymmetry to exploit. A prior on which
one wins is the bias this protocol exists to prevent. The one-sided rule in family 1 has an
argument that does not transfer: a method ranking allosteric residues below background is
broken, not competing.

**Name and decline the alternatives, rather than ignoring them.**

- **DeLong's test** for two AUCs on the same cases assumes independent cases. A contiguous
  label patch violates it. Declined, and named as declined.
- **Friedman with a post-hoc test** is the standard route for K > 2 methods. At three arms
  and one pre-declared reference, Holm over three is simpler and exact. Not needed.
- **Rank-biased overlap** is omitted from the noise-resilience statistics. The current reason
  — "it has no use in this literature" — is a popularity argument and R1 forbids it. The
  correct reason is that overlap@5 already carries top-weighting at exactly the k that ships,
  so RBO adds nothing here.

## Consequences

- `evaluation/manifest.yaml` gains a second entry under `decision`, with the same three arms,
  Holm over three, two-sided, reference `cavity_volume`. Protocol version 3.
- A method must now clear **two** Holm-corrected families to support a claim. That is a
  higher bar than version 2 stated, and it is the bar version 2 already implied.
- `p_calibrated` feeds both families. Holm never runs on a raw permutation p.
- The report prints, per arm: the family-1 p, the family-2 p, and the effect sizes beside
  each. A rejection in family 1 alone is not a claim.
- **One measurement shows the two families are not redundant.** On `bcr_abl1_corrected`,
  `cavity_volume` itself rejects family 1 at `p_calibrated` 0.0003 while its predicted centre
  sits farther from the site than a random five-residue list — DCC 26.5 Å against a chance
  line of 17.7 Å. Clearing a null and producing a useful hit list are different claims.
- The RBO omission reason is rewritten in the manifest and in §10 of the protocol README.

## Alternatives rejected

**Leave everything but family 1 descriptive, and drop the "beat `cavity_volume`" threshold.**
Rejected: the threshold exists because clearing the null is a low bar, measured. Dropping it
returns the project to a bar a zero-parameter geometric baseline clears.

**Correct across every baseline and every method.** Rejected: the family would grow with the
number of methods run, which makes the correction a function of exploration effort rather than
of the claim. One pre-declared reference keeps the family fixed at three.
