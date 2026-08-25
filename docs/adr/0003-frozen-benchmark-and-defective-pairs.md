# 0003 — Freeze the benchmark, and answer the challenge's defective pairs with tiers

**Status:** accepted · 2026-08-20

## Context

The challenge fixes the apo/holo pairs (`CHALLENGE.md` §6, Table 1). A forensic audit of
the deposited files (`docs/benchmark/primary/audit/`) found every one of the three defective:

- **KRAS `4OBE` → `6OIM`** — the apo input is **wild-type** KRAS. It does not carry the
  G12C cysteine that the holo inhibitor is covalently bonded to.
- **BCR-ABL1 `1OPL` → `5MO4`** — the apo input carries myristate **in the pocket we are
  asked to blind-predict**, plus an ATP-site inhibitor. Myristate contacts 16 of the 20
  label residues at 3.29 Å — the apo input already *is* holo at the site to be predicted.
- **Cardiac myosin `5TBY` → `6C1H`** — `6C1H` is rat unconventional myosin-Ib bound to
  actin and calmodulin, with no mavacamten and no cardiac myosin in it. `5TBY` is a 20 Å
  homology model built on a tarantula template. **No ground truth can be derived at all.**

Two bad options present themselves. Use the mandated pairs as given, and report numbers
computed against a ground truth that in one case does not exist. Or substitute better
structures, and be scored on a benchmark the organisers did not specify.

## Decision

Neither. The benchmark is **frozen** in `docs/benchmark/primary/manifest.yaml` with three tiers,
and every tier is reported:

- **`mandated`** — exactly the entries in Table 1. Reported because the challenge requires
  them. Each carries a `defect:` field naming what is wrong with it. Cardiac myosin is
  marked `status: excluded`, because "unscoreable" is the honest result, not a number.
- **`corrected`** — the defensible pair for the same biological target, chosen on
  structural grounds recorded in the audit. This is where the method comparison happens.
  For ABL1 the audit's own first choice was the NMR ensemble `6XR7` (the only ABL1 kinase
  domain with *both* pockets empty); `2G2H` was taken instead because it is X-ray, uses the
  holo's ABL1b numbering, and has the myristoyl pocket free — at the cost of an ATP-site
  inhibitor and an engineered H415P. `6XR6`/`6XR7`/`6XRG` remain the ligand-free
  alternative and are recorded here rather than silently dropped.
- **`sensitivity`** — an alternative structure of the same target, to show whether a
  conclusion survives a different input.

Everything is fixed **before any method is run**, which is what makes the choice
pre-registration rather than result-tuning. `uv run allo benchmark verify` re-derives every
pinned quantity from the deposited files and fails on any drift, including RCSB
re-versioning an entry.

## Consequences

- Method comparisons are honest: every method sees identical inputs and labels. **Not yet
  negatives** — the second negative class the challenge requires (non-functional surface
  pockets) is unbuilt, and until it is committed no method may be scored here. This bullet
  said "and negatives" from the start, which was aspirational rather than true; the header of
  `docs/benchmark/primary/README.md` states the scoring gate that governs.
- We report more numbers than asked for, and must explain the tiers in the report. That
  explanation is an asset — it demonstrates the target validation the challenge is about.
- The cardiac myosin correction is not a judgement call but a factual error in the
  challenge statement, and is worth reporting upstream (`docs/benchmark/primary/README.md`).
- Adding a target later means editing the manifest and re-running `benchmark freeze`, so
  the cost of the ASD generalisability set in Phase 5 is small.
- Risk accepted: if the organisers score only the mandated tier, our best numbers sit in a
  tier they may not read. Mitigation is to lead with the mandated tier and its defects.

---

**Amendment, 2026-08-20 (ADR 0007).** The BCR-ABL1 bullet originally carried a second
reason: that apo and holo differ by 1.00 Å core and 0.50 Å across the pocket lining, so
"there is no conformational change to find". That reason is withdrawn. Under an allosteric
ground truth a pre-formed pocket is not a defect — the ABL1 myristoyl pocket is the field's
canonical *allosteric but not cryptic* site, and what remains to be predicted is which of
the many pre-formed pockets is the coupled one. The ligand-occupancy reason above is
sufficient on its own and is the one that actually bears on C1. The **decision** of this
ADR — three tiers, freeze before any method runs, report all three — is unaffected.

---

**Amendment, 2026-08-24 — two tiers, not three.** The `sensitivity` tier is removed. It had
grown to six arms across three proteins: a third ABL1 apo, a strict-C5 trimmed ABL1 node set,
two extra myosin structures, a second myosin drug, and a second myosin site. None of them is
an input-layer question. Whether a conclusion survives a different structure, a different
node-set scope or a different effector is a **robustness question about a method**, and it
cannot be asked before a method exists. Those arms are re-addable from git history in Phase 2,
one at a time, against a specific claim.

The decision that remains is the one this ADR made: **`mandated` and `corrected`, both frozen
before any method runs, both reported.** Five scoreable arms, one mandated-but-unscoreable
record. The benchmark now maps one-to-one onto the three disease areas in Table 1.
