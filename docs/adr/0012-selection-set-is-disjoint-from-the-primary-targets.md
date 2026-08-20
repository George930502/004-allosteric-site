# 0012 — The tuning set must be family- and site-disjoint from every primary target

**Status:** accepted · 2026-08-20

## Context

`docs/benchmark/README.md` §5 says hyperparameters are selected on the ASD generalisability
set and frozen before the primary targets are touched, so that nothing is tuned on the
benchmark it is scored on.

The same document, §7, records what is in ASD:

- ASD curates the BCR-ABL1 myristoyl pocket **twice** (`AS001006501` / `3PYY`;
  `AS002023501` / `3K5V`), and the `3PYY` record lists `1OPL`/`MYR` as a related complex —
  **our mandated apo is itself an ASD entry.**
- ASBench curates HRAS (`AS001013301`, `4DLR`) with site residues R68, D92, Q95, Y96, Q99,
  **4 of which are in our frozen KRAS label set**, and "no predictor's 30–40 % identity
  dedup separates KRAS from HRAS".
- Zheng 2023 — challenge reference [1] — tests the myosin blebbistatin pocket, our Site 2.

So the set designated to hold the hyperparameters contains the answers to two of the three
primary targets and a near-answer to the third. Selecting on it is tuning on the test set by
a longer route. Both facts were already written down, in the same file, three hundred lines
apart; the contradiction was never drawn.

There is no mitigating blindness left to spend: §7 concludes "**no arm in the primary
benchmark is blind**". A leak into the selection set cannot be absorbed by a clean test set,
because there isn't one.

Found by an adversarial review (Codex, `gpt-5.6-sol`), not by us.

## Decision

**A candidate may enter the selection set only if it is disjoint from every primary target
on all four of the following.** Applied as a pre-filter, before any candidate's difficulty
is examined, and frozen as a list of accessions before a single hyperparameter is chosen.

1. **Accession.** No ASD/ASBench/CASBench record naming any accession this benchmark uses in
   any arm, as apo, holo, or "related complex". This alone removes the `3PYY` record.
2. **Protein family.** No member of a primary target's family, by Pfam clan and by
   UniProt-level orthology: no RAS superfamily GTPase (removes HRAS `4DLR` and NRAS), no
   ABL/SRC-family tyrosine kinase, no myosin of any class. Family, not sequence identity —
   a 30 % identity cut is what the field uses and it is exactly what fails to separate KRAS
   from HRAS.
3. **Homologous site.** No record whose curated site is the structural equivalent of a
   primary site in _any_ protein — no myristoyl/SH3-clamp pocket, no switch-II or
   helix-3/loop-7 pocket, no myosin N-terminal/converter or blebbistatin site — even in an
   unrelated fold.
4. **Residue overlap.** After 2 and 3, no candidate whose curated site residues transfer,
   through pairwise alignment to a primary apo chain, onto ≥ 2 of that arm's frozen labels.
   This is the check that caught HRAS and it is cheap to run; it is the backstop for a
   homology the first three clauses miss.

**Anything selected outside this set is fixed a priori and declared**, with the reasoning,
before the primary targets are run. "We used the usual value" is a declaration; "we tried a
few" is not.

**The generalisability claim needs a set this one cannot serve.** The selection set is
burned by construction — hyperparameters were chosen on it. Phase 5's generalisability
number comes from a further set, disjoint from both, selected under the same four clauses
and never looked at until the method is frozen.

## Consequences

- The selection set will be materially smaller than an unfiltered ASD pull, and clause 2
  removes the closest analogues of our targets — the candidates on which tuning would have
  been most informative. That is the cost, and it is the point.
- **Kinases are not banned wholesale**, only ABL/SRC-family ones. A CDK or a PKA allosteric
  record survives clauses 2 and 3, which keeps enough kinase biology in the set to tune on.
- Clause 4 needs the candidate's curated site residues, which ASD supplies unevenly and
  sometimes truncated with `,etc.`. Where the residue list is incomplete the candidate is
  **excluded**, not admitted on a partial check.
- This constrains Phase 1.7 (build the selection set) and Phase 2 (choose the quantum
  metric's parameters on it). Both must cite this ADR.
- **Risk accepted.** ASD2023 ran AlloSitePro over all 20,386 human proteins and predicted
  66,589 sites, MYH7 among them (§7). No exclusion rule can remove a _predicted_ pocketome
  from a method's training history. This ADR bounds curated leakage; it does not bound that,
  and the report must say so rather than claim a clean separation.
- Completes the tuning half of the protocol begun in ADR 0003. Depends on ADR 0007's
  ground-truth definition for what "the same site" means.
