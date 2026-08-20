# 0005 — Defining the active site, which is the propagation source

**Status:** accepted · 2026-08-20

## Context

The challenge asks for residues ranked by "dynamic connectivity to an active site"
(`CHALLENGE.md` §4.1). The active site is therefore the source term of the propagation, and
the choice of source drives the ranking more than most method knobs do. It must be defined
**from the apo structure only** (C1), and it must be stated before any method is run.

Two families of rule are available, and the targets do not all admit the same one:

- The apo entry's own bound cofactor. `4OBE`/`4LDJ` hold GDP·Mg; `9GZ3`/`8ACT` hold ADP·Mg
  and phosphate; `8QYP` holds ADP·vanadate·Mg. All are the catalytic ligand at the
  catalytic site, present in the input file, so using them leaks nothing.
- Conserved catalytic motifs located by sequence. Needed where the apo entry has no
  cofactor *reachable by the rule* — `2G1T`'s own chain A holds only Mg; its ATP site is
  occupied by a bisubstrate conjugate carried on a different chain (component `112`, chain
  E, 2.74 Å from chain A's motif residues), which a chain-scoped ligand rule cannot see.

## Decision

**Rule, in order:**

1. If the apo entry contains its catalytic cofactor (nucleotide, metal, substrate analogue),
   the active site is the protein residues within 4.5 Å of that cofactor's heavy atoms.
2. Otherwise, the active site is the conserved catalytic motif residues located by sequence
   match in the apo chain. For the protein-kinase fold that is the β3 VAIK lysine, the HRD
   catalytic loop and the DFG magnesium-binding loop. **The motif is located by sequence in
   each entry, never written down as residue numbers** — the same motifs sit at auth 287–290
   / 380–383 / 400–402 in the ABL1b-numbered entries (`1OPL`, `2G2H`) and at 268–271 /
   361–364 / 381–383 in the ABL1a-numbered `2G1T`. A pinned list would be right for one
   convention and silently wrong for the other, which is the +19 hazard of ADR 0004.
3. An ATP-site inhibitor present in the apo file may define the site (it marks the pocket
   and it is apo-side data), but rule 2 is preferred where both apply, because a drug's
   footprint is a property of that drug and does not transfer to another target.
   **All three ABL1 arms use rule 2.** The first manifest used `P16`'s footprint for two of
   them, contradicting this rule and giving those arms a 21-residue source against the third
   arm's 11 — so the sensitivity arm varied the structure *and* the source at once. Corrected
   2026-08-20; the scoreable label sets were unaffected (20/20 and 18/18 either way).

**The manifest stores the rule, not the result.** `active_site: {from_ligands: [GDP, MG]}`
or `{from_motifs: [VAIK, HRD, DFG]}`; `derive()` computes the residues. A pinned residue list
would be compared against itself by `verify()`, which is no check at all — and the first
version of this manifest did exactly that, and carried `1OPL`'s active site under
`2G2H`'s entry for a day before the audit caught it.

## Consequences

- Every target has an explicit, apo-only, reproducible source set. No method may choose
  its own.
- **Known confound, recorded here because it will be argued about:** on KRAS, 5 of the 21
  ground-truth pocket residues (11, 12, 13, 16 and 34) *are* active-site residues — the Switch-II
  pocket abuts the nucleotide site, and sotorasib is anchored at Cys12. A score defined as
  connectivity to the active site will rank those residues top for trivial reasons. The
  evaluation therefore reports enrichment both over the full label set and over the
  **scoreable** label set with the active-site residues removed, and the scoreable
  figure is the one that answers the challenge's actual question. BCR-ABL1 (10.6 Å minimum on the
  mandated pair, 10.8 Å corrected and 10.8 Å sensitivity) and cardiac myosin (16.5 Å corrected, 13.3 Å on the X-ray
  sensitivity arm) have no such overlap.
- Rule 2 is fold-specific. Extending to an ASD target with a different fold needs a motif
  definition for that fold, or a cofactor-bearing apo entry.


---

**Amendment, 2026-08-20 (ADR 0007).** This ADR originally said the evaluation reports over a
**distal** label set "with the active-site-adjacent residues removed". Withdrawn on two
counts. The set is now the **scoreable** label set, and the rule is **set membership, not
distance**: a label is excluded exactly when it is itself a propagation-source residue, which
is AlloPred's published rule (doi:10.1186/s12859-015-0771-1) and costs no labels to a
threshold nobody in the allostery literature states. The earlier 5 Å version discarded KRAS
residues 10 and 58, neither of which is an active-site residue under this ADR's own rule — a
second, undeclared criterion operating silently. Proximity is handled in the evaluation layer
by a distance-matched null instead. The **decision** of this ADR — active site as a derived
rule, never a pinned list — is unaffected, and `benchmark.py` already implements the amended
form. Recorded here because ADR 0007 lists this ADR as "unchanged and explicitly still in
force", which was true of its decision and not of this paragraph.
