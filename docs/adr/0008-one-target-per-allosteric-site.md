# 0008 — One benchmark target per allosteric site

**Status:** withdrawn · 2026-08-24 (accepted 2026-08-20)

## The rule, which still holds

One benchmark instance is one protein **plus one allosteric site**. The scored artifact is a
ranked residue list per target, so a protein with two validated allosteric sites needs two
ranked lists and therefore contributes two targets.

## Why it is withdrawn as a decision

The rule was written to settle a live question: cardiac myosin carried both the mavacamten
site and the aficamten site, so `protein` was ambiguous as a unit of counting. Both aficamten
arms were removed on 2026-08-24 as scope the challenge never asked for, and every remaining
protein carries exactly one site. Nothing now depends on this choice, so it is a convention
rather than a decision.

Reinstate it as an accepted ADR if a second site is ever added for the same protein. At that
point the sibling-site question in [ADR 0011](0011-scoring-universe-is-the-candidate-set.md)
becomes live again too, and the two must be settled together.
