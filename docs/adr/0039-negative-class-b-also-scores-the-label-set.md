# 0039 — Negative class (b) also scores the label set, beside the site pocket

**Status:** accepted · 2026-09-03 · opens evaluation **protocol version 4** · extends
[ADR 0030](0030-negative-class-b-is-tested-by-combination-across-arms.md) and answers the
question left open by `../benchmark/review/25-second-pass-synthesis.md` §1.4

## Context

`CHALLENGE.md` §4.1 requires enrichment against two negative classes. The second is
**non-functional surface pockets**. The frozen protocol tests it by ranking every detected
pocket by the mean midrank of its lining, and asking where the site pocket lands.

Until 2026-09-02 the code put the **label set's** mean midrank on the positive side. Review 25
§1.4 closed against that form and the code was changed to the site pocket's lining, on two
grounds: ADR 0030 writes the test with the site's number drawn from the same law as a decoy's,
and a label statistic's sampling variance goes as one over the label count while a decoy's
goes as one over its lining size. Both halves have to be a pocket lining for that
exchangeability to hold. The stated reason for rejecting the label form was that **no measured
type-I rate covered it.** That was true on 2026-09-02.

## What the 2026-09-03 audit measured

Instrument: the site-uninformative Gaussian field the frozen calibration itself uses,
`nulls.smooth_field`, over the real Cα coordinates, with the real site and decoy linings read
from the freeze. Seeds are printed per cell. Script and raw output:
`../benchmark/review/data/endpoint-b-2026-09-03/s34_sim.py` and `s4b_label_endpoint.py`.

**The shipped statistic has no power against the deliverable.** Power at correlation length 8,
20 000 fields per cell, with δ added to a residue set before ranking:

| arm | δ on the label set | δ on the site lining |
| --- | --- | --- |
| `kras_g12c_corrected` | 0 at every δ | 0 at every δ |
| `bcr_abl1_corrected` | 0.037 at δ = 4 | 0.999 at δ = 4 |
| `cardiac_myosin_corrected` | 0 at δ = 4 | 0.989 at δ = 4 |

The dilution is mechanical. Twelve myosin labels sit inside a 295-residue lining, so a perfect
signal on all twelve moves the lining mean by 12/295 of δ. And δ = 2 already means a mean
per-arm AUC of 0.930, so δ = 4 is past any realistic method. The shipped statistic measures
whether the **detector's pocket** ranks high, not whether the **allosteric residues** do.

**The label statistic is conservative, not inflated.** Same instrument, 20 000 fields per arm
per correlation length, four correlation lengths:

| arm | size at α = 0.05 | 95 % interval | power at δ = 2 | power at δ = 4 |
| --- | --- | --- | --- | --- |
| `kras_g12c_corrected` | 0.0000 | [0, 0.00018] | 0 | 0 |
| `bcr_abl1_corrected` | 0.0083 | [0.0071, 0.0097] | 0.751 | 0.999 |
| `cardiac_myosin_corrected` | 0.0094 | [0.0081, 0.0108] | 0.866 | 1.000 |

Combined across the three arms, Fisher size is 0.0016 to 0.0067 across correlation lengths 4
to 20, against a nominal 0.05.

The exchangeability objection is correct as physics and its consequence is measured: unequal
set sizes make the test **conservative**, never anti-conservative, on every arm and every
correlation length tested. `kras_g12c_corrected` cannot reject on either form, because 18
decoys floor the attainable p at 1/19 = 0.0526. That is the detector's pocket count, not the
statistic.

## Decision

**Report both.** `score_arm` writes `nulls.decoy_pockets.label_p` beside the existing `p`.

- `p` is unchanged. It is the ADR 0030 statistic, exactly as review 25 §1.4 left it, and it
  answers "does the method rank the true pocket above decoy pockets".
- `label_p` uses the same decoy linings and the same permutation, with the label set as the
  positive. It answers "does the method rank the allosteric residues above non-functional
  pockets", which is the question §4.1 is about.
- **Both stay descriptive.** Neither enters a confirmatory family. ADR 0030's per-arm floor
  argument is untouched.
- The licence `label_p` carries is asymmetric, because its measured behaviour is asymmetric: a
  rejection is real, and a non-rejection is weak evidence rather than evidence of absence.

This is an addition and not a reversal. Review 25 §1.4 removed a statistic that had no
measured type-I rate. This restores it beside the other one, with the measurement it lacked,
and without giving it a decision to make.

## Consequences

- Evaluation **protocol version 4**. `manifest.yaml` gains one reported endpoint and
  `frozen.json` gains no pinned value: the number is computed per method at score time. `allo
  evaluate verify` re-derives clean.
- The report can state the §4.1 result honestly for the first time. Under version 3 it could
  only have said "the site pocket outranks decoy pockets", and on two of three arms not even
  that.
- `test_the_decoy_p_value_is_built_from_the_site_pocket_and_not_the_label_set` still passes
  and still pins `p`. `test_negative_class_b_reports_the_label_set_beside_the_site_pocket`
  pins that both are present and that neither is confirmatory.
- No number produced under version 3 moves, because no method has been scored on `main`: the
  method layer left on 2026-09-02 (ADR 0037). Opening version 4 is cheap today and would be
  impossible after the first scored run.
