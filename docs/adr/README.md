# Architecture / research decision records

One file per decision that is expensive to reverse or that a future reader would
otherwise re-litigate. Format: `NNNN-short-slug.md`, statuses `proposed` /
`accepted` / `superseded by NNNN`.

Write one when: a modelling choice constrains later phases, a method is chosen over a
credible alternative, or a constraint interpretation is settled. Do not write one for
routine implementation details.

Statuses also include `withdrawn`, for a decision whose subject matter no longer exists. A
withdrawn ADR keeps the rule it established, in case it becomes live again, and says why it
stopped binding. It is never deleted.

## The record

Twenty-five decisions, grouped by what each one settles. Read the group that covers the
layer you touch. Every entry is one file, and no file is ever deleted.

### How we work

| # | Decision | Status |
| --- | --- | --- |
| [0001](0001-record-decisions.md) | Record research decisions as ADRs | accepted |
| [0019](0019-prior-art-review-is-scoped-not-systematic.md) | Prior-art review is scoped, not systematic | accepted |

### The input layer — what a method receives

| # | Decision | Status |
| --- | --- | --- |
| [0004](0004-residue-identity-and-label-transfer.md) | Residue identity, numbering conventions, and label transfer by alignment | accepted |
| [0005](0005-active-site-definition.md) | Defining the active site, which is the propagation source | accepted |
| [0006](0006-cofactors-and-modified-residues-as-nodes.md) | Cofactors, and modified residues, as network nodes | accepted |
| [0009](0009-structure-admission-rule.md) | Structure admission: resolution binds only where we select | accepted |
| [0010](0010-node-set-is-the-modelled-chain.md) | The frozen node set is the modelled chain, not a trimmed catalytic domain | accepted |
| [0014](0014-retain-exact-benchmark-structure-bytes.md) | Pin versioned structure provenance and retain an offline mirror | accepted |
| [0017](0017-normative-pair-definition-and-comparator-blindness.md) | One normative pair definition. Blindness belongs to evaluation | accepted |

### The ground truth — what a method is scored against

| # | Decision | Status |
| --- | --- | --- |
| [0007](0007-ground-truth-is-the-allosteric-site.md) | Ground truth is the allosteric site. Crypticity is a difficulty axis | accepted |
| [0011](0011-scoring-universe-is-the-candidate-set.md) | Residues that score by construction leave both classes, not only the positives | accepted |
| [0008](0008-one-target-per-allosteric-site.md) | One benchmark target per allosteric site | withdrawn |
| [0015](0015-same-site-labels-leave-the-background.md) | Per-protein functional-site registry | withdrawn |

### Which targets, and why those

| # | Decision | Status |
| --- | --- | --- |
| [0003](0003-frozen-benchmark-and-defective-pairs.md) | Freeze the benchmark, and answer the challenge's defective pairs with tiers | accepted |
| [0012](0012-selection-set-is-disjoint-from-the-primary-targets.md) | The tuning set must be family-disjoint and site-disjoint from every primary target | accepted |
| [0013](0013-answer-informed-apo-selection.md) | Do not select an apo structure by comparison against holo geometry | withdrawn as a live blocker, the rule stands |
| [0016](0016-do-not-expose-5tby-without-a-defensible-source.md) | Do not expose 5TBY as a propagation input without a defensible source | accepted, **blocks Phase 2 for that arm** |
| [0020](0020-cmyc-contract-must-precede-method-design.md) | Freeze the c-Myc contract before method design | accepted, **blocks Phase 2 for c-Myc** |
| [0021](0021-secondary-benchmark-is-two-disjoint-sets.md) | The secondary benchmark is two disjoint sets, and its frame is RCSB | accepted |

### The evaluation layer — how a score is computed

| # | Decision | Status |
| --- | --- | --- |
| [0018](0018-null-calibration-is-unmet.md) | Matched-patch null calibration is unmet | accepted, cleared by 0023 |
| [0022](0022-confirmatory-endpoint-is-the-mean-midrank.md) | The confirmatory endpoint is the mean midrank, not AUC-PR | accepted |
| [0023](0023-matched-patch-null-is-calibrated-not-fully-matched.md) | The matched-patch null is calibrated, not fully matched | accepted, mechanism claim withdrawn by 0025 |
| [0024](0024-decoy-pockets-are-detector-defined.md) | Decoy pockets: pyKVFinder at its defaults, zero halo, power floor disclosed | accepted |
| [0025](0025-the-size-rescale-is-calibrated-at-every-holm-level.md) | The size rescale is calibrated at every Holm level, and clearing the null is a low bar | accepted |

### The method

| # | Decision | Status |
| --- | --- | --- |
| [0002](0002-quantum-metric-hypothesis.md) | Working hypothesis for the quantum metric | proposed, Phase 2 accepts or supersedes it |

---

## Reading ADRs written before 2026-08-24

On 2026-08-24 the benchmark was reduced from eleven arms to five, and the evaluation protocol
was separated from the input layer. Earlier ADRs therefore refer to things that have moved:

| An older ADR says | It now lives at |
| --- | --- |
| `docs/benchmark/README.md` §5 | `docs/benchmark/evaluation/README.md` (frozen 2026-08-25) |
| `cardiac_myosin_site1_*` | `cardiac_myosin_*` — there is one myosin site |
| `bcr_abl1_sensitivity`, `bcr_abl1_trimmed`, `cardiac_myosin_site2_corrected`, the `8QYP`, `9YRG` and `2G1T` arms | removed; recoverable from git at `363633c` and listed in `docs/ROADMAP.md` Phase 5 |
| `docs/benchmark/audit/*.json` | deleted — they were self-declared duplicates of the `.md` and nothing loaded them |

The reasoning in those ADRs is unchanged. Only the names are stale.
