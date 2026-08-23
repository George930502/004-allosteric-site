# 0015 — Per-protein functional-site registry

**Status:** withdrawn · 2026-08-24 (accepted 2026-08-20)

## What it decided

[ADR 0011](0011-scoring-universe-is-the-candidate-set.md) removes the propagation source from
both the positive and the negative class. ADR 0015 extended that to **sibling functional
sites**: a residue this benchmark labels in one arm must not be a negative in another arm of
the same protein. It implemented the extension as an explicit `functional_sites` registry in
the manifest, carried between entries by sequence alignment, so that adding an arm could not
move another arm's candidate universe.

## Why it is withdrawn

The mechanism was built for a benchmark with two myosin sites and four myosin arms. After the
2026-08-24 reduction each protein carries one site, and the registry became a measured no-op:
on all five frozen arms `excluded_from_scoring` equals the derived active site exactly, and
`n_candidates == n_residues - len(active_site)`. The registry, its alignment transfer and its
three regression tests were removed rather than kept as machinery that guards nothing.

Removing it also **returned 27 residues to the myosin candidate set** (716 → 743) that were
excluded only on account of arms this benchmark no longer runs. That is the fairer number.

The ADR's own honest note is worth carrying forward: the registry was verified to equal the
union of that protein's frozen labels, which means it never achieved the arm-independence it
claimed. Any future version must derive the registry from an external source — UniProt
binding-site annotations, ASD records, M-CSA — and not from the benchmark's own arms.

Reinstate together with [ADR 0008](0008-one-target-per-allosteric-site.md) if a protein ever
carries two benchmarked sites.
