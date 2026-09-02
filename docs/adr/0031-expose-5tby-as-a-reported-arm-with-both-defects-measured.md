# 0031 — Expose 5TBY as a reported cardiac-myosin arm, with both input defects measured beside it

**Status:** accepted · 2026-09-02 · **supersedes**
[ADR 0016](0016-do-not-expose-5tby-without-a-defensible-source.md) · clears the Phase 2
blocker on that arm

## Context

ADR 0016 blocked the mandated cardiac-myosin arm on three grounds: no label set could be
derived, no apo-derived propagation source existed, and a 20 Å homology model cannot supply
residue-level contact topology under C6. Its blocking condition was "the organisers answer
question (a)". That has occurred.

The organisers answered on 2026-09-02:

> "To better represent the human MYH7-mavacamten complex for this challenge, you may
> substitute 9GZ2 for 6C1H. Please always document the substitution you make and explain
> rational of why you did it."

**The label blocker is gone, completely.** `transfer_labels(9GZ2:A, 5TBY:A, XB2, 4.5 Å)`
returns all twelve mavacamten-contact residues, none unmapped, all inside the `5TBY` chain A
node set: 164, 167, 168, 666, 710, 711, 712, 713, 721, 722, 770 and 774. That is the same
twelve residues as the frozen `cardiac_myosin_corrected` label set, because `5TBY` and `9GZ3`
use the same author numbering.

**Both input blockers stand, and both are now measured rather than argued**
([`../benchmark/review/02-cardiac-myosin.md`](../benchmark/review/02-cardiac-myosin.md)).

**Blocker 1 — no unique fold-general source rule.** PROSITE PS00016 matches once in KRAS and
**twice** in MYH7, at 61–68 and 178–185, so `allo.inputs.active_site` raises on uniqueness.
Forced through by taking both matches, the source centroid lands 13.50 Å from the
ligand-derived centroid.

A **family-level** motif triple does work. `GESGAGKT` (P-loop), `N..SSRFG` (switch I) and
`DI.GFE` (switch II) each match exactly once in MYH7 and zero times in KRAS, ABL1 or the two
ABL1 apo entries. Validated against the ligand-derived source where that truth exists:

| Entry    | ligand source | motif source | overlap | Jaccard | centroid offset |
| -------- | ------------: | -----------: | ------: | ------: | --------------: |
| `9GZ3:A` |            21 |           22 |      14 |   0.483 |          5.96 Å |
| `9GZ2:A` |            25 |           22 |      16 |   0.516 |          5.92 Å |

**ADR 0016's prohibition was stricter than the repository's own precedent.** It forbids "a
myosin-only motif", but every entry already in `CATALYTIC_MOTIFS` is a family motif: `PTP` is
PROSITE PS00383, `POLA` and `YXDD` are Poch 1989 polymerase motifs, `GDD` is motif C in an
RdRp. None is fold-general either.

**Blocker 2 — the contact topology is largely invented, and here is the number.** Against the
3.4 Å cryo-EM `9GZ3`, aligned by sequence over 761 shared residues, at the frozen 4.5 Å
heavy-atom cutoff:

| minimum sequence separation | `5TBY` edges | `9GZ3` edges | shared |   Jaccard |    recall |
| --------------------------- | -----------: | -----------: | -----: | --------: | --------: |
| 1                           |         3226 |         3626 |   2862 |     0.717 |     0.789 |
| 3                           |         1783 |         2166 |   1447 |     0.578 |     0.668 |
| **5 (long-range)**          |         1103 |         1419 |    807 | **0.471** | **0.569** |

Pairwise Cα distances agree at Spearman **0.9724**, median absolute difference 2.08 Å.

An independent re-derivation over the same 289 180 pairs returns **0.9742** and **1.95 Å**
([`../benchmark/review/15-blocking-measurement-recheck.md`](../benchmark/review/15-blocking-measurement-recheck.md)).
The cause of the difference was not isolated, and it changes nothing: both readings say the
same thing, which is that the fold agrees closely while the contact graph does not. The Jaccard,
the edge counts, the recall and the degree correlation all reproduce exactly. Quote the range
rather than either endpoint.

**The fold is right and the graph is not.** A method reading global shape would be fine on
`5TBY`. A method reading the contact graph — which is what C6 mandates — receives a graph in
which 43 % of the measured long-range contacts are missing and 27 % of the contacts present
were never measured. Those are the edges that carry allosteric signal.

**The same defect shows from the label set's own side, and it is the sharpest form of it.**
The two myosin arms carry the **identical** twelve label residues, because `5TBY` and `9GZ3`
use the same author numbering. In the evaluation graph those twelve residues form **(8, 4)**
components on the measured `9GZ3` and **(7, 4, 1)** on the homology model. One residue that the
measured structure puts in contact with the rest of the site is isolated in `5TBY`. Nothing
about the label set changed; only the edges did. Pinned by
`tests/test_scoring.py::test_label_component_structure_is_what_the_protocol_claims`.

## Decision

**1. Supersede ADR 0016.** Its blocking condition has occurred and its label-side premise is
false. Its input-side reasoning survives as a disclosure, not as a block.

**2. Keep `cardiac_myosin_corrected` (`9GZ3:A`→`9GZ2:A`) as the scored, confirmatory arm.**
It is the only cardiac-myosin pair with measured contact topology and a ligand-derived source,
and it is the cleanest pair in the benchmark: same construct, same state, differing by
mavacamten and nothing else.

**3. Expose `5TBY:A`→`9GZ2:A` as `cardiac_myosin_mandated`, non-confirmatory, with both
measured defects printed beside every number.** The arm is the challenge's literal apo input,
a valid label set now exists, and "unscoreable" was the honest answer only while no label set
could be derived. A disclosed defective number beats a missing one: a judge reading
`CHALLENGE.md` Table 1 will look for the accession.

Print with it, always: source Jaccard 0.48–0.52 against the ligand-derived source with a
5.9 Å centroid offset, and long-range contact Jaccard 0.471 against the measured structure.

**4. Add the myosin family motif triple to `CATALYTIC_MOTIFS`**, with its citation and with
the validation table above committed as a test.

**5. Write the submission-facing substitution page.** The organisers' final sentence is
general: document every substitution and give the reason. Four exist — `6C1H`→`9GZ2`,
`5TBY`→`9GZ3`, `4OBE`→`4LDJ`, `1OPL`→`2G2H` — each documented in a different file. A judge
will look for one page.

## Consequences

- `cardiac_myosin_mandated` loses `status: excluded` and `prediction_status: blocked`, gains
  `holo: {pdb: 9GZ2, chain: A, ligand: XB2}` and `active_site: {from_motifs: [...]}`, and
  enters `primary/frozen.json` with a node set, a label set and a candidate set.
- The holo accession in that arm is **no longer the one `CHALLENGE.md` Table 1 names**. That
  is the substitution the organisers sanctioned, and it is documented as one.
- The confirmatory family is unchanged at three `corrected` arms.
- `CATALYTIC_MOTIFS` gains three entries. A test pins the validation numbers, so a later
  change to the motif set fails the suite rather than moving a source silently.
- **The cost is that any number this arm produces measures the homology model as much as the
  method.** That is why it is non-confirmatory and why both agreement numbers print beside it.
- Phase 2 may now produce the mandated cardiac-myosin deliverables. The ADR 0016 blocker on
  that arm is cleared. The c-Myc blocker is cleared separately, by ADR 0036.
- **Scoring parity across teams is not guaranteed on this target.** The organisers declined to
  designate one replacement for all teams. A cross-team comparison on cardiac myosin is not
  like-for-like, and the report says so.

## Alternatives rejected

**Leave `5TBY` unexposed.** Rejected by the decision recorded on 2026-09-02: two of the four
minimum targets would then have no connectivity matrix and no top-5 list, which is the largest
open conformance gap. The input defects are disclosable; a missing deliverable is not.

**Use the motif triple on the corrected arm too.** Rejected: the corrected arm has a
ligand-derived source that the motif triple only agrees with at Jaccard 0.5. Replacing a
measured source with a 6 Å-offset approximation on the arm that carries the confirmatory
decision would weaken the arm that matters to make two arms look alike.

**Substitute `8QYR` or `9GZ1`.** Rejected: the organisers name `9GZ2` as preferred, the
repository already froze it, and no label set moves.
