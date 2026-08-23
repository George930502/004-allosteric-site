# 0013 — Do not select an apo structure by comparing candidates against holo geometry

**Status:** withdrawn as a live blocker · 2026-08-24 (accepted 2026-08-20). **The rule stands.**

## The rule

An apo input must be chosen on **apo-only** criteria, pinned before any holo file is opened:
construct compatibility, experimental method, resolution, model completeness, and annotated
catalytic state. A site-occupancy check is admission pass/fail and never a closeness
objective. Choosing the apo whose pocket most resembles the holo pocket is selection on the
answer, and it biases every downstream number in the anti-conservative direction.

## Why the blocker is gone

`8QYP` was selected by comparing apo candidates against holo-defined pocket geometry, so the
three arms built on it were quarantined and a Phase 1.8 apo-only re-selection was scheduled.
All three arms — `cardiac_myosin_site1_sensitivity_xray`, `cardiac_myosin_site1_omecamtiv`
and `cardiac_myosin_site2_corrected` — were removed on 2026-08-24. The cardiac-myosin arm is
now `9GZ3`/`9GZ2`, which needs no such re-selection: `9GZ3` is the deposited apo partner of
`9GZ2` from the same study, same construct, same state, same modelled range. There was no
candidate ranking to bias.

## Consequences

Phase 1.8 is deleted. No arm in the benchmark is quarantined, and the `quarantine` field is
gone from the manifest and the freeze. The rule above binds the Phase 1.7 ASD selection set,
where candidate ranking *is* how structures get chosen — see
[ADR 0012](0012-selection-set-is-disjoint-from-the-primary-targets.md) and
[ADR 0009](0009-structure-admission-rule.md).
