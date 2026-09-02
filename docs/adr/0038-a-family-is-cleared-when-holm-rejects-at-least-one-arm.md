# 0038 — A confirmatory family is cleared when Holm rejects at least one arm

**Status:** accepted · 2026-09-03 · part of evaluation **protocol version 4** · completes
[ADR 0032](0032-the-claim-threshold-is-its-own-confirmatory-family.md) and
[ADR 0030](0030-negative-class-b-is-tested-by-combination-across-arms.md)

## Context

The frozen protocol declares two confirmatory families, corrects each by Holm over three
arms, and says a method must clear both. It never says what clearing one is.

That gap is not academic. The frozen layer holds **both** readings, in documents that cite
each other:

| Where | Reading |
| --- | --- |
| `evaluation/README.md` §8, on the combination test | rejecting says "at least one arm has signal" — **disjunction** |
| `evaluation/README.md` §0, row 3, quoting ADR 0030 | "at least one arm separates the site" — **disjunction** |
| `evaluation/README.md` §13 | "the positive control rejects on **one of three**", printed as an adverse finding — **conjunction** |
| `docs/ROADMAP.md` | "`cavity_volume` no longer clears the confirmatory family … Holm rejects one arm of three, not three of three" — **conjunction** |
| `harness.confirmatory_verdict` | reported `n_reject` and declined to choose |

Choosing after seeing a result is the hyperparameter this layer exists to prevent. One
control makes the stakes concrete: `cavity_volume` clears family 1 under the disjunction and
fails it under the conjunction, so the two readings disagree about the repository's own
declared reference method.

## Decision

**A family is cleared when Holm rejects at least one of its arms.** The composite verdict
requires both families. The licence is per arm and is printed per arm.

`harness.confirmatory_verdict` now returns `cleared` on each family and on the verdict, so
the rule is executed rather than restated.

"Rejects on all three arms" stays available as an optional consistency statement. It carries
no extra error protection and licenses no generalisation claim. A generalisation claim needs
the secondary `generalisation` tier.

## Why the disjunction and not the conjunction

Measured, not argued. Scripts and raw output:
`../benchmark/review/data/endpoint-b-2026-09-03/s1_fwer.py`, `s1_lfc.py`.

1. **Holm controls the disjunction, and only the disjunction.** Measured global-null
   familywise error is 0.0416 to 0.0457 against a nominal 0.05, and the closed form is
   0.049171. That is the error rate the frozen correction was chosen to hold.
2. **The conjunction is an intersection-union test, and Holm is the wrong machinery for it.**
   An IUT is level alpha with **no multiplicity step at all**, so freezing Holm is itself
   evidence that the disjunction was intended. Run under Holm the conjunction spends 1 event
   in 20 000 at the global null — at least 180 times below the alpha it advertises — while
   still reaching **0.04025** at its least-favourable configuration. It advertises a
   protection it does not deliver where it matters.
3. **Neither reading protects an individual arm better.** The chance that a null arm is
   rejected is 0.0408 to 0.0457 under both. That is a property of Holm, not of the rule.
4. **The conjunction costs 3.5 times the family-level power** at a realistic effect: 0.2465
   against 0.8718 at a mean per-arm AUC of 0.77. Dropping Holm does not recover it (0.2631).

## Consequences

- `docs/ROADMAP.md` and `evaluation/README.md` §13 stated the conjunctive reading. Under this
  ADR, `cavity_volume` **clears family 1** on one arm of three, which is what those two
  documents record as a failure. The measurement stands; the wording was the error.
- A method that clears both families may say "at least one confirmatory arm separates the
  site, and the method beats `cavity_volume` on at least one arm". It may not say the method
  works on all three, unless all three reject and the statement names them.
- Nothing about a per-arm p-value changes. This ADR fixes the reading, not the arithmetic.
