# 0003 — Freeze the benchmark, and answer the challenge's defective pairs with tiers

**Status:** accepted · 2026-08-20

## Context

The challenge fixes the apo/holo pairs (`CHALLENGE.md` §6, Table 1). A forensic audit of
the deposited files (`docs/benchmark/audit/`) found every one of the three defective:

- **KRAS `4OBE` → `6OIM`** — the apo input is **wild-type** KRAS. It does not carry the
  G12C cysteine that the holo inhibitor is covalently bonded to.
- **BCR-ABL1 `1OPL` → `5MO4`** — the apo input carries myristate **in the pocket we are
  asked to blind-predict**, plus an ATP-site inhibitor. Apo and holo differ by 1.00 Å
  over 409 paired residues and 0.50 Å across the pocket lining: there is no conformational
  change to find.
- **Cardiac myosin `5TBY` → `6C1H`** — `6C1H` is rat unconventional myosin-Ib bound to
  actin and calmodulin, with no mavacamten and no cardiac myosin in it. `5TBY` is a 20 Å
  homology model built on a tarantula template. **No ground truth can be derived at all.**

Two bad options present themselves. Use the mandated pairs as given, and report numbers
computed against a ground truth that in one case does not exist. Or substitute better
structures, and be scored on a benchmark the organisers did not specify.

## Decision

Neither. The benchmark is **frozen** in `docs/benchmark/manifest.yaml` with three tiers,
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

- Method comparisons are honest: every method sees identical inputs, labels and negatives.
- We report more numbers than asked for, and must explain the tiers in the report. That
  explanation is an asset — it demonstrates the target validation the challenge is about.
- The cardiac myosin correction is not a judgement call but a factual error in the
  challenge statement, and is worth reporting upstream (`docs/benchmark/README.md`).
- Adding a target later means editing the manifest and re-running `benchmark freeze`, so
  the cost of the ASD generalisability set in Phase 5 is small.
- Risk accepted: if the organisers score only the mandated tier, our best numbers sit in a
  tier they may not read. Mitigation is to lead with the mandated tier and its defects.
