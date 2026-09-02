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


**These are the recorded outputs, not a re-runnable script.** The simulations import
`allo.inputs` and `allo.scoring`, and a tracked file inside the review tree may import no
`allo` module (ADR 0034), so the scripts could not live beside their output and
`experiments/` could not hold them either. Each JSON carries the seed, the sample size, the
arm and the interval, which is enough to check the arithmetic and to rebuild the run, and it
is less than the repository asks for elsewhere. `../benchmark/review/data/endpoint-b-2026-09-03/README.md`
states the rule that produced the gap. The endpoint-b measurement was afterwards moved into
`allo.scoring.simulate` and re-run as a tracked experiment; the FWER and budget simulations
were not, and that is recorded here rather than claimed away.

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
`../benchmark/review/data/endpoint-b-2026-09-03/s1_fwer.json`, `s1_lfc.json`.

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

   > **The 0.2631 is not in the cited records and the other five numbers are.** Found
   > 2026-09-03 by the round-5 audit. `s1_fwer.json` holds 0.2465 and 0.87175 at λ = 8 and
   > δ = 1.0, `s1_lfc.json` holds 0.04025, and both hold the closed form 0.049171. Neither
   > records an uncorrected run, and this ADR says above that these are recorded outputs
   > rather than a re-runnable script, so the number cannot be re-derived. What the records
   > do support is the direction: Holm rejecting all three implies every raw p is at or below
   > α, so the uncorrected conjunction is **at least 0.2465** and the ratio to 0.8718 stands
   > whatever its exact value. Read 0.2631 as `[UNVERIFIED]`.

## Consequences

- `docs/ROADMAP.md` and `evaluation/README.md` §13 stated the conjunctive reading. Under this
  ADR, `cavity_volume` **clears family 1** on one arm of three, which is what those two
  documents record as a failure. The measurement stands; the wording was the error.
- A method that clears both families may say "at least one confirmatory arm separates the
  site, and the method beats `cavity_volume` on at least one arm". It may not say the method
  works on all three, unless all three reject and the statement names them.
- Nothing about a per-arm p-value changes. This ADR fixes the reading, not the arithmetic.
