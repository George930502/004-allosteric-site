# Does negative class (b) measure the deliverable, and is the label form calibrated?

**Run:** `uv run python experiments/2026-09-03-endpoint-b/run.py` · seed 0 ·
`metrics.json` beside this file. **Decided ADR 0039**, and then amended it the same day.

## Question

`CHALLENGE.md` §4.1 asks for enrichment against non-functional surface pockets. The frozen
test ranks pockets by the mean midrank of their linings and asks where the positive set lands.
Which set goes on the positive side is the whole question:

- `site` — the detector's site-pocket lining. The ADR 0030 statistic, reported as `p`.
- `label` — the label set. The deliverable, reported as `label_p`.

## Result 1 — `p` cannot see the deliverable

Power at correlation length 8, shift on the **label set** in both columns:

| arm | δ | `site` | `label` |
| --- | ---: | ---: | ---: |
| `bcr_abl1_corrected` | 2.0 | 0.028 | **0.754** |
| `bcr_abl1_corrected` | 4.0 | 0.034 | **0.999** |
| `cardiac_myosin_corrected` | 2.0 | 0.000 | **0.875** |
| `cardiac_myosin_corrected` | 4.0 | 0.000 | **1.000** |
| `kras_g12c_corrected` | any | 0.000 | 0.000 |

The dilution is mechanical: 12 myosin labels inside a 295-residue lining move that mean by
12/295 of δ. And δ = 2 already means a mean per-arm AUC of 0.93, so this is not a small-effect
artefact. `kras_g12c_corrected` cannot reject on either form, because 18 decoys floor the
attainable p at 1/19 = 0.0526.

## Result 2 — and `label_p` is not a p-value

The two sides have different set sizes and are not exchangeable, so the size of `label_p` is a
property of the score field rather than a distribution-free guarantee. Four generators, worst
size over four correlation lengths, 20 000 fields per cell:

| generator | `site` | `label` |
| --- | ---: | ---: |
| `white_noise` | 0.0001 | 0.0086 |
| `smooth_gaussian` | 0.0049 | 0.0154 |
| `smooth_t` | 0.0047 | 0.0137 |
| `distance_shell` | 0.0237 | **0.0548** |

On `bcr_abl1_corrected` under `distance_shell` the label form runs 0.0513 to 0.0548 across all
four correlation lengths, and the worst cell's 95 % interval, [0.0516, 0.0580], is entirely
above α. `distance_shell` is negated distance to a random residue: the shape every
distance-correlated baseline in this repository has, and the adversarial case for a test whose
two sides differ in size.

**So `label_p` is reported as a descriptive percentile and carries no rejection**, and review
25 §1.4's exchangeability argument is vindicated by measurement rather than by principle.

## What this run does not establish

- Four generators are four, not all. A score field unlike all four could behave differently.
  The claim is "measured on these four", never "distribution-free".
- Power is measured at one correlation length, 8. The size table covers four.
- Nothing here is a method. Every field is site-uninformative by construction.

## Provenance

The first version of this measurement lived in an untracked script, and ADR 0039 was written
from it. An adversarial pass made two findings the same day: the evidence was not reproducible,
and the size claim rested on one null family. Both are why the simulation is now
`allo.scoring.simulate` and why the table above has four rows.
