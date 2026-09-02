# 0024 — Decoy pockets: pyKVFinder at its defaults, zero halo, power floor disclosed

**Status:** accepted · 2026-08-25 · **superseded on the detector settings by
[`0030`](0030-negative-class-b-is-tested-by-combination-across-arms.md)**, which re-froze
pyKVFinder away from its defaults and demoted the pocket test to descriptive. The two
decisions this ADR still owns are the zero halo and the disclosure of the power floor.

## Context

`CHALLENGE.md` §4.1 requires enrichment against **two** negative classes: random background
residues, and **non-functional surface pockets**. The second needs a pocket detector, and
every choice around it moves the endpoint. Chosen after seeing a result, each becomes a
hyperparameter. All of them are frozen here.

Three sub-decisions, and the third is forced by arithmetic rather than by preference.

## Decision

**Detector: pyKVFinder 0.9.3** (doi:10.1186/s12859-021-04519-4) at its published defaults —
step 0.6 Å, probe_in 1.4 Å, probe_out 4.0 Å, removal_distance 2.4 Å, volume_cutoff 5.0 Å³ —
run on the apo input alone.

It is purely geometric, so it raises no C2 question, and it is versioned and installable, so
this configuration is reproducible. Choosing the defaults is the choice not to tune a
detector on the benchmark it will score. It is an optional `eval` extra: the decoy sets are
derived once and committed, so `make check` verifies them offline.

**Membership: a pocket is a decoy only if its lining, restricted to the candidate set, shares
no residue with the label set.** The restriction comes first, because a residue that scores
by construction leaves both classes (ADR 0011), and a pocket lining is no exception.

**Halo: 0 Å, with 5 Å pinned as a pre-registered sensitivity analysis.** Excluding pockets
near the site is the better idea in principle — without it a method is penalised for being
nearly right — but the measurement forbids it here. At 5 Å `kras_g12c_mandated` keeps **zero**
decoys, and at 8 Å both KRAS arms do.

## Consequences

**The challenge's negative class (b) cannot reject at α = 0.05 on three of five arms.** With
three decoy pockets the smallest attainable p-value is 0.25.

| Arm | detected | decoys | min attainable p |
| --- | ---: | ---: | ---: |
| `kras_g12c_mandated` | 5 | 3 | **0.25** |
| `kras_g12c_corrected` | 5 | 3 | **0.25** |
| `bcr_abl1_mandated` | 27 | 24 | 0.040 |
| `bcr_abl1_corrected` | 12 | 9 | **0.10** |
| `cardiac_myosin_corrected` | 42 | 41 | 0.024 |

This is arithmetic about small proteins, not a defect in the method or in the detector. It is
disclosed in `docs/benchmark/evaluation/README.md` §5 and carried in `frozen.json` per arm, so
a null result on that endpoint cannot later be read as a method failure.

**The detector misses the site entirely on some secondary arms.** Coverage of the label set by
the best detected pocket is 0.09 on `mkp5`, 0.19 on `ns5b` and 0.36 on `ptp1b`. That is the
challenge's own premise — static pocket detection fails on exactly these targets — measured on
our benchmark before any method existed. It is a difficulty axis and never a selection rule.

**The objection this invites, and the answer.** SiteFerret states that a detector-derived
negative set "is method-specific" and that "false negatives cannot be ruled out". Both are
true and unavoidable: a pocket labelled non-functional here is a pocket with no *known*
function. The mitigation available is version discipline, and it is applied in full. Of the
allosteric-prediction papers surveyed for this protocol, exactly one states a detector
version.
