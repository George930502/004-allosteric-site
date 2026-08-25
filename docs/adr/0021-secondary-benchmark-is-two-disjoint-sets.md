# 0021 — The secondary benchmark is two disjoint sets, and its frame is RCSB

**Status:** accepted · 2026-08-24

## Context

`CHALLENGE.md` §6 asks participants to "test robustness on additional targets of their choice
to demonstrate **generalizability and scalability**", and points at the Allosteric Database
for them. Two earlier decisions constrain how that is done:

- **ADR 0012** requires the tuning set to be family- and site-disjoint from every primary
  target, and says plainly that "the generalisability claim needs a set this one cannot
  serve. The selection set is burned by construction — hyperparameters were chosen on it."
- **ADR 0009** applies a resolution ceiling wherever there is a _pool_ to select from, and
  no ceiling where a target is hand-specified.

`CONTEXT.md` defined the secondary benchmark as one set "used for hyperparameter selection
**and** for generalisability". That is the contradiction ADR 0012 already named, written
into the vocabulary. This ADR settles it.

Three facts, established this phase, decide the rest.

**Fact 1 — no database certifies allostery per record, per site, per structure.** ASD
certifies _proteins_, not sites ("336 **proteins** … verified as **allosteric proteins**");
ASD v3.0/2019/2023 publish no inclusion criteria at all and mix curated records with 66,589
machine-_predicted_ AlloSitePro sites; ASBench's rules are behind a paywall and its licence
forbids redistribution outright; CASBench adds no independent allostery test and unions its
site over every deposited structure of the protein; AlloBench is the most explicit protocol
in the field and still has no apo step. Binding MOAD is sunset. PDBbind+ is paywalled.
AHoJ-DB publishes apo/holo pairs but no licence, and its apo call is not our clause (iii):
queried for `AY7` it returns `1opl`, the pair our own audit rejected for myristate contacting
16 of 20 labels at 3.29 Å. Full survey: `docs/benchmark/secondary/evidence/databases.md`.

**Fact 2 — the interface problem is large and is ours, not the field's.** ADR 0010 fixes the
node set to one modelled chain. `transfer_labels` keeps only same-chain lining residues, so
an effector on a subunit interface loses part of its positive class **in silence**. In
CASBench's 91 curated enzymes, 27 % of entries have at least one of the two annotated sites
formed at an intersubunit contact — 5 % both sites, 22 % one (doi:10.32607/20758251-2019-11-1-74-80,
quoted in full in the evidence note; the fraction whose _allosteric_ site is at an interface
is bounded at 5–27 %, not known). **Rate corrected after the freeze**, because the number
first written here was an estimate the ledger cannot reproduce. Derived from
`selection.json`: 11 of the 73 screened candidates were rejected on clause (ix), which is
15 %; counting only the 58 rows that record both an apo and a holo, it is 10 of 58, or 17 %.
Either way the rate on our own candidates sits inside CASBench's 5–27 % bound rather than
above it.

**Fact 3 — three targets cannot reject.** Any distribution-free one-sample test over N
targets has a minimum attainable one-sided p of 2⁻ᴺ. At N = 3 that is 0.125. The primary
benchmark's three claim-bearing arms are not underpowered for a cross-target claim; they are
_unable_ to make one at α = 0.05. N ≥ 5 is a hard floor and N ≥ 6 under any correction.
This is why a secondary set is a statistical necessity and not a nicety.

## Decision

### 1. Two sets, disjoint, frozen together, used at different times

| Set              | Tier             | Purpose                                                   | When it may be looked at                |
| ---------------- | ---------------- | --------------------------------------------------------- | --------------------------------------- |
| `development`    | `development`    | every hyperparameter — metric, Hamiltonian, cutoff, ratio | Phase 2 onward. Burned by construction  |
| `generalisation` | `generalisation` | the generalisability and scalability claims               | Phase 5, **after the method is frozen** |

Both freeze now, from one manifest, through the same `derive()` the primary set uses. Freezing
them together is what makes them comparable; using them at different times is what makes the
second one worth anything. Assignment between the two is a **seeded split stratified by size**,
not a judgement — see decision 5.

### 2. The candidate frame is RCSB, not ASD

The frame is a recorded full-text query over RCSB for entries whose own annotation names an
allosteric site, filtered to experimental structures at the ADR 0009 resolution ceiling. It
is reproducible, needs no licence, has no expired certificate in front of it, and is the
source `CHALLENGE.md` §6 names for structures. The curated databases are **cross-checks on
the allostery claim**, never the claim itself.

This does not weaken clause (ii). It cannot: by Fact 1 no database satisfies clause (ii)
either. The functional-evidence DOI is re-established per target from primary literature,
exactly as the three primary arms already do. That is the expensive part of a secondary set,
and no choice of frame avoids it.

### 3. Four admission clauses beyond the eight

Clauses (i)–(viii) in `docs/benchmark/primary/README.md` §1 are unchanged and bind both sets. These
four bind the secondary set, because they are **selection** rules and a selection only exists
where there is a pool (ADR 0009's reasoning, applied again).

> **(ix) Single-chain lining [REPOSITORY POLICY].** Every protein residue lining the effector
> at the declared radius must lie in the modelled chain. Measured, not assumed. An interface
> site is rejected, with the in-chain fraction recorded.
>
> **(x) Apo occupant classification [REPOSITORY POLICY].** No apo component may contact a
> **scoreable** label. A component may contact a label only where that label is itself an
> active-site residue, which clause (vii) has already removed from the scoring universe.
> Clause (iii) alone is not enough: a sibling fragment of the same series, in the same
> pocket, passes a scoreable-set contact check by half an angstrom.
>
> **(xi) Structure admission.** ADR 0009 clause 2, unchanged: X-ray ≤ 2.5 Å or cryo-EM
> ≤ 4.0 Å, experimental only.
>
> **(xii) Within-set redundancy [REPOSITORY POLICY].** No two secondary targets may share a
> UniProt accession, and none may share a Pfam family with another secondary target or with
> any primary target. Per-pair clauses say nothing about a set that is eight copies of one
> fold, and this is the set hyperparameters are chosen on.

**Clause (x) was narrowed after the freeze, and this is the record.** It first read "every
non-polymer component of the apo entry is classified ... a second-site occupant must contact
**no** residue of the full label set". Both halves overstated what the freeze holds.

- The freeze classifies only the components that contact the active site, into
  `orthosteric_state.apo.state_components` and `.additives`. Components elsewhere in the entry
  are recorded in `apo_site_occupancy.entry_components` and are not sorted into a third bucket.
  Six of the fourteen arms across both sets carry such a component, so an exhaustive
  classification assertion would fail today on `MYR`, `EDO`, `TRS`, `ZN`, `K`, `NET` and `ORN`.
- "Contact no residue of the full label set" was already untrue of an admitted arm when it was
  written: `mkp5` records `labels_contacted: 1`, a sulfate 2.9 Å from label 413, and 413 is an
  active-site residue under the `PTP` motif rule.

The narrowed wording is what `tests/test_secondary.py` enforces, and it is falsifiable: the
primary set's `bcr_abl1_mandated` arm fails it outright, with myristate contacting 16 of 20
labels and no active-site overlap at all. That arm is admitted because the challenge mandates
it and its defect is disclosed. An arm selected from a pool gets no such licence.

**What clause (xii) is tested on, recorded after an audit asked.**
`tests/test_secondary.py` checks the Pfam half, both within the set and against the primary
set. It does not check the UniProt half separately, and it does not need to: two arms sharing
a UniProt accession share every Pfam family, so the Pfam assertion fails first. The manifest
carries no `uniprot` field for that reason.

ADR 0012 names two further disjointness clauses that are **not** implemented as tests, and
this is the record of why. Its clause 3 (structural superposition and chemotype) has no
threshold anyone has published for this use. Its clause 4 — a secondary site whose residues
transfer onto two or more of a primary arm's frozen labels — was run by hand during the audit,
over every secondary apo chain against every primary apo chain. It flagged five pairs, and all
five are artefacts: a global BLOSUM62 alignment between non-homologous chains returns 22–42 %
"identity" by chance, and a carbamoyl-phosphate synthetase is not homologous to a kinase.
A test that fires on every non-homologous pair tests nothing. The genuine near-miss the clause
was written for is `chk1` (PF00069) against `bcr_abl1` (PF07714): the same protein-kinase
fold in two Pfam families. The Pfam test passes it and the manifest note discloses it, which
is the honest outcome and not a hidden one.

Clause (ix) is the expensive one and its cost is stated rather than hidden: it removes a
class of allosteric site that the MWC picture makes central — the subunit-interface site.
Extending the node set to more than one chain is a Phase 4 coarse-graining question, not an
input-layer one, and it is recorded there.

### 4. Clause (ii) needs an active site to be derivable, and that selects

A pair whose apo entry admits no `{from_ligands: …}` or `{from_motifs: …}` rule is
unusable, because the active site is the propagation source. Two consequences, both declared:
nuclear receptors and other non-catalytic targets are out of scope for this benchmark
entirely, and the admitted set leans toward cofactor-bearing enzymes.

Every motif added to `allo.inputs.CATALYTIC_MOTIFS` carries a citation, and is verified to
match **exactly once** on the apo chain that uses it. **Amended 2026-08-24, before any motif
was added:** the original wording required a PROSITE accession for every motif. PROSITE
covers three of the families we need by **profile** only — reverse transcriptase, positive-
strand RdRp, and coronavirus 3CL protease — and a profile is not a regular expression. Where
PROSITE publishes a `PA` **pattern**, the regex is converted from that pattern mechanically
and carries the accession. Where it publishes only a profile, the motif carries a
primary-literature citation instead. The accession is provenance for the pattern; the
guarantee is the exactly-once match, which `active_site` already enforces at freeze time and
which caught a dead active site (`6CMP`, the catalytically dead SHP2 C459E mutant) during
screening.

The recorded escape hatch, if a later set is too thin: derive the active site from pinned
UniProt `ACT_SITE` features transferred by alignment. Not built, because nothing admitted here
needs it.

### 5. The split is seeded, stratified and reproducible

Targets are ordered by `n_residues`, assigned to size strata, and split within each stratum by
`random.Random(0).shuffle`. The seed and the resulting assignment are frozen. Nobody chooses
which targets carry the generalisation claim, so nobody can put the easy ones there.

### 6. ADR 0012's byte-for-byte ledger requirement is amended

ADR 0012 requires `selection.json` to reproduce byte-for-byte on re-run. **That is not
achievable for any live-database frame** and was not achievable when it was written: RCSB
gains entries every week, so the same query returns a superset later. Replaced by what is
actually checkable:

- the ledger records the frame query, its retrieval date, every candidate considered, and the
  clause that decided it;
- **admitted** rows are re-derived from the deposited files by `allo benchmark verify --set secondary`;
- **rejected** rows are re-checkable by re-running the recorded screen, which is a network test;
- a candidate absent from the ledger still cannot enter the set, and a test holds that.

No `allo select` command is added. The screening reuses `benchmark.derive` unchanged, which is
the point — a candidate is judged by the same code that freezes an arm.

## Consequences

- `CONTEXT.md`'s "secondary benchmark" entry splits into two terms. The word "selection set"
  is retired in favour of `development`.
- The secondary set lives in `docs/benchmark/secondary/`, with its own manifest and its own
  freeze date. The primary freeze is a closed artifact and is not rewritten.
- Phase 1.7 closes when the secondary freeze verifies. Phase 5's generalisability number comes
  from the `generalisation` tier and from nowhere else.
- **Risk accepted, and it is the main one.** Clause (ix) plus the apo-availability constraint
  admit far fewer targets than the power analysis asks for. The set is therefore reported with
  the claim its achieved N supports, and the shortfall is named in
  `docs/benchmark/secondary/README.md` §7 rather than absorbed. **Outcome, recorded after
  the freeze:** 97 candidates considered, 73 screened to a deciding clause, 9 admitted,
  split 4 development and 5 generalisation. A set this size supports a
  generalisability statement about a per-target success rate near 0.9, not near 0.8.
- **Risk accepted.** The frame is a depositor's own use of the word "allosteric" in a title or
  abstract. That is a claim, not curation. It is a recall device only: clause (ii) still
  decides, from primary literature, per target.
- Depends on ADR 0007 (allosteric ground truth), ADR 0009 (structure admission), ADR 0010
  (node set), ADR 0012 (disjointness, amended here), ADR 0013 (apo-only selection, which binds
  the ranking used here).
