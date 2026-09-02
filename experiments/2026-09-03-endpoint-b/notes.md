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
| `cluster_blocks` | 0.0046 | 0.0163 |
| `distance_shell` | 0.0237 | **0.0548** |

On `bcr_abl1_corrected` under `distance_shell` the label form runs 0.0513 to 0.0548 across all
four correlation lengths, and the worst cell's 95 % interval, [0.0516, 0.0580], is entirely
above α. `distance_shell` is negated distance to a random residue: the shape every
distance-correlated baseline in this repository has, and the adversarial case for a test whose
two sides differ in size.

**So `label_p` is reported as a descriptive percentile and carries no rejection**, and review
25 §1.4's exchangeability argument is vindicated by measurement rather than by principle.

### Re-run the same day, because the third generator was not a third law

The table's third row read `smooth_t`, at 0.0047 and 0.0137. An adversarial pass found that
generator divided a Gaussian field by one chi-square draw per replicate, which is monotone
within the column. Every statistic here is a midrank, so its ranks were bit-identical to
`smooth_gaussian`'s at the same seed and this run measured three laws while reporting four.

**A rank test cannot see a marginal distribution.** Heavy tails, log-normal marginals and
rescaling are all the same null, so only the copula moves the answer. `cluster_blocks`
replaces it with a genuinely different dependence structure: each residue takes the value of
its nearest of `n // 25` random centres, so the field is piecewise constant with hard
boundaries. Blockiness is the direction that made `distance_shell` the worst case, so the
replacement is adversarial rather than convenient.

The whole run was repeated at the same seed and the table above is the repeat. Nothing
changed but that row: 0.0163 instead of 0.0137, still far below α and still not the worst
case. `distance_shell` is still worst at 0.0548 with the same interval, and `site` still
holds at 0.0237.

## What this run does not establish

- Four generators are four, not all. A score field unlike all four could behave differently.
  The claim is "measured on these four", never "distribution-free". They are four distinct
  RANK laws, which a test pins, and that is the only kind of distinctness this test can see.
- Power is measured at one correlation length, 8. The size table covers four.
- Nothing here is a method. Every field is site-uninformative by construction.

## Provenance

The first version of this measurement lived in an untracked script, and ADR 0039 was written
from it. An adversarial pass made two findings the same day: the evidence was not reproducible,
and the size claim rested on one null family. Both are why the simulation is now
`allo.scoring.simulate` and why the table above has four rows.
