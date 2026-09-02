# 0042 — Clause (xii) is Pfam family plus PANTHER narrowing, and the clan sentence is withdrawn

**Status:** accepted · 2026-09-03 · corrects the operational sentence of
[ADR 0012](0012-selection-set-is-disjoint-from-the-primary-targets.md) clause 2 · no freeze
moves

## Context

ADR 0012 clause 2 states the disjointness rule twice and the two statements disagree.

The **headline** names three biological groups: "no RAS superfamily GTPase, no ABL/SRC-family
tyrosine kinase, no myosin of any class."

The **operational** sentence says: "reject if the candidate's UniProt accession maps, via
InterPro/Pfam at a release pinned and recorded in the artifact, to any **clan** containing
`PF00071` (Ras), `PF07714` (PK_Tyr_Ser-Thr) narrowed to the ABL/SRC branch by its
InterPro/PANTHER family assignment, or `PF00063` (Myosin_head)."

What ships is neither. `tests/test_secondary.py:84` compares Pfam **family** strings, and no
release is pinned anywhere in the repository.

## What was measured

Live against the InterPro API on 2026-09-03, and re-verified independently the same day.
Releases: **InterPro 109.0** (2026-06-11), **Pfam 38.2** (2026-03-26), **PANTHER 19.0**
(2024-06-20).

**The two anchor clans collapse to two, and one of them is enormous.**

| anchor | clan | clan members |
| --- | --- | --- |
| `PF00071` Ras | **CL0023** P-loop_NTPase | **316 Pfam families** |
| `PF00063` Myosin_head | **CL0023**, the same clan | — |
| `PF07714` PK_Tyr_Ser-Thr | CL0016 PKinase | 48 |

Rejecting everything in CL0023 removes 316 Pfam families: effectively every P-loop
NTP-binding enzyme, which covers kinases, ATPases, GTPases and helicases, and is most of the
druggable enzyme universe. That is far more than "no RAS superfamily GTPase".

**The operational sentence rejects an arm the headline admits.** `p97_vcp` carries `PF00004`
(AAA), which is in CL0023 — it is that clan's first member. p97/VCP is not a RAS GTPase, not an
ABL/SRC kinase and not a myosin. PANTHER separates all three:

| protein | UniProt | PANTHER family |
| --- | --- | --- |
| p97/VCP | P55072 | PTHR23077 AAA ATPase domain-containing protein |
| KRAS | P01116 | PTHR24070 RAS/DI-RAS/RHEB |
| MYH7 | P12883 | PTHR45615 Myosin ATPase superfamily |
| CHK1 | O14757 | PTHR24346 MAP/microtubule affinity-regulating kinase |
| ABL1 | P00519 | PTHR24418 non-receptor tyrosine kinases |

**Strict clan application would destroy the across-target claim.** Dropping `p97_vcp` takes the
`generalisation` tier from 5 arms to 4 and breaks
`test_the_generalisation_tier_is_large_enough_to_reject`, whose floor is N greater than or
equal to 5 because 2⁻⁴ = 0.0625 is above alpha. Applied within the secondary set it would also
collide `hiv_rt` with `ns5b` (CL0027) and `mkp5` with `ptp1b` (CL0031), taking `development`
from 4 to 2.

**And it cannot bind the primary set at all.** KRAS and cardiac myosin are both in CL0023, and
`bcr_abl1_mandated` shares CL0010 with myosin. `CHALLENGE.md` Table 1 mandates all three
proteins, so the primary set is not clan-disjoint from itself and cannot be made so. A rule
that binds one set and cannot bind the other is asymmetric by construction.

## Decision

**Clause (xii) is Pfam family disjointness, narrowed by PANTHER family where two arms share a
family.** The clan sentence in ADR 0012 clause 2 is withdrawn. The headline sentence stands and
is what the rule means.

**PANTHER is the narrowing instrument and cannot be the primary one.** Measured over all
fifteen arms: fourteen carry exactly one PANTHER family and all fourteen are distinct, but
`ns5b` (P26663, the HCV polyprotein) has **no PANTHER assignment at all** — the API answers
that accession with an empty body. A rule resting on PANTHER alone would be silent on one arm.
Pfam families do the work, and PANTHER resolves the one collision that matters, `chk1` against
the two ABL1 arms in CL0016. The full per-arm assignment is
`../benchmark/review/data/clause-xii-2026-09-03.json`.

Three consequences follow from that:

1. **Pin the releases** — **DONE 2026-09-03.** `interpro_release: 109.0`,
   `pfam_release: 38.2` and `panther_release: 19.0` are in both manifests. A rule that resolves against a moving database and records no version is not
   frozen. Note that every `pfam` value in both manifests came from RCSB, whose annotations
   carry `assignment_version: "34.0"`, so the manifests are pinned to Pfam 34.0 in fact and to
   nothing in writing, while any lookup today resolves against Pfam 38.2.
2. **Add `uniprot:` per target** — **DONE 2026-09-03**, all fifteen arms, so the clause
   derives from an accession rather than from a hand-typed family list. `ns5b`'s `pfam` value cannot have come from RCSB, which carries no
   Pfam annotation for either of that arm's entries; the value is right but its stated
   provenance is not, and it is the sole input to the disjointness test for that arm.
3. **Say what the guarantee is** — **DONE 2026-09-03** in `secondary/README.md`, directly
   under the clause text: family level, plus PANTHER where families collide. Neither document mentions clans today,
   so the shipped text is already right and only the ADR was wrong.

## Consequences

- No freeze moves and no arm changes tier. `p97_vcp` stays admitted, on the headline reading
  that always admitted it.
- Four of the fifteen arms carry a Pfam family that belongs to no clan at all, so a clan rule
  is silently a no-op on part of every such arm. That is a property of the rule the ADR never
  mentioned and a second reason not to state the guarantee at clan level.
- A generalisability claim may say the secondary arms share no Pfam family with a primary
  target and sit in different PANTHER families. It may not say they are clan-disjoint. They
  are not, and the primary set is not clan-disjoint from itself either.
- Items 1 and 2 are work, not decisions. They are tracked in
  `../benchmark/review/27-fourth-pass-synthesis.md` §3.2.
