# 0041 — The `generalisation` tier was never sealed against storage, and scoring is what the seal now guards

**Status:** accepted · 2026-09-03 · amends
[ADR 0021](0021-secondary-set-is-two-disjoint-tiers.md) · no protocol version change

## Context

`docs/benchmark/secondary/manifest.yaml:19-20` states the rule:

> `generalisation` — the generalisability and scalability claims. Phase 5, and NOT BEFORE the
> method is frozen. Reading it early destroys the only thing it is for.

The rule was broken in **23 tracked files on `main`**, and the commit that states it already
published all five arms' positive counts, prevalences and label residue lists on the day it
was written. This is not a later reader breaking a rule.

Reproduced independently on 2026-09-03:

| Where | What it publishes for all five sealed arms |
| --- | --- |
| `docs/benchmark/evaluation/frozen.json` | `n_positive` 12, 12, 19, 17, 19 and the matching prevalence |
| `docs/benchmark/secondary/README.md:180-187` | the same counts and prevalences, in a table |
| `data/patches/*.npz` | `members` has width equal to the positive count, for every sealed arm |
| `docs/benchmark/secondary/manifest.yaml` | the label residue lists |

`docs/benchmark/secondary/frozen.json` is the one place that withholds it: `n_positive` is
`None` there for every sealed arm. Every other route publishes it.

`26-third-pass-synthesis.md` §4b calls this "the most important finding of the pass" and
carries no row for it in its own §5 tracker, which is the failure `26` §7 criticises in `25`.

## What the seal can and cannot still protect

Three things a sealed tier is normally for:

1. **Scoring secrecy** — no method has been scored on a sealed arm. Measured: `main` holds no
   method layer, and no tracked record scores one. **Intact.**
2. **Storage secrecy** — the answer key is not in the repository. **Never held.** It was
   published in the commit that wrote the rule.
3. **Reader secrecy** — nobody designing the method has seen the arms. **Lost**, because the
   counts and the label lists are readable by anyone who opens the repository. The
   `PROTECTED_PATHS` guard binds prediction modules, not people.

Rebuilding an unopened tier is not available. It would have to come from candidate leads whose
answer keys are already tracked in `secondary/evidence/extension-candidates.md`, which is a
protected answer key for exactly that reason, and the 2026-09-03 screen found 19 candidates
that clear every clause checkable without an answer key and **none with a paid clause (ii)**.

## Decision

**Amend the rule to what it can still deliver, and make that part a check.**

The `generalisation` tier is sealed **against scoring**, not against storage. `score_arm`
raises `PermissionError` on a `generalisation` arm unless the caller passes
`unseal="phase-5"`, and the run notes must say why the method is frozen.

This is the argument the file-read routes are enforced on: a rule a document states and no
test holds is a promise. The check is
`test_the_sealed_tier_cannot_be_scored_without_saying_so`.

## Consequences

- `secondary/manifest.yaml:19-20`, `secondary/README.md:54` and ADR 0021:60 state the old,
  wider rule. They are frozen artifacts and are not repaired in place. The correction is
  `../benchmark/review/27-fourth-pass-synthesis.md` §3.1 and this ADR.
- **Any generalisability claim must disclose that the tier's positive counts and label sets
  were readable in the repository throughout method design.** A reviewer who finds this
  themselves will not accept "sealed" afterwards. Disclosing it costs the strength of the
  claim and keeps its honesty, which is the trade this repository takes everywhere else.
- The calibration path is unaffected: it calls `nulls.matched_patches` directly and not
  `score_arm`, which is why the sealed arms have patch caches at all.
- Nothing about the tier assignment changes. It stays the seeded, size-stratified split, and
  the test that it reproduces from `n_residues` still holds.
