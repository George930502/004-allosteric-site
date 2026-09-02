# 0035 — Conservation is the fourth confounder column, computed as JSD on pinned Pfam alignments

**Status:** accepted · 2026-09-02 · part of evaluation **protocol version 3** · fills the
`null` that [ADR 0025](0025-the-size-rescale-is-calibrated-at-every-holm-level.md) left

## Context

`evaluation/README.md` §11 prints three apo-only confounders beside every score — relative
solvent accessibility, hydrophobicity and deposited B-factor — and names conservation as the
fourth. It reads `null`, because no external alignment exists in the repository.

**The objection this leaves unanswered is the first one a reviewer raises:** "your allosteric
hits are just the conserved residues." The repository currently cannot answer it with a number.

**The evidence says the relationship is mixed, and the split is definitional.**

- Cimermancic 2016 (doi:10.1016/j.jmb.2016.01.029): "Cryptic site residues are significantly
  more conserved than the rest of a protein (P = 3.4 × 10⁻⁶⁷)". This is the only retrieved
  measurement against a background, and the population it measures is the one this benchmark's
  label sets belong to.
- Leander 2020 (doi:10.1073/pnas.2002613117): "Residues critical for allosteric signaling are
  surprisingly poorly conserved while those required for structural integrity are highly
  conserved."

Both can hold. A pocket lining and a signalling pathway are different residue sets. A
confounder column does not need the sign settled in advance — it needs to be measured.

**Nothing in the literature reports a conservation-only baseline for allosteric-site
prediction.** Computing this column produces a number nobody has published.

**One number in circulation is misquoted and must not enter the report.** CryptoSite's
"conservation AUC = 0.74" is not conservation's standalone AUC. The sentence reads: "The second
feature added to the subset of the 3 features by the greedy-forward approach was sequence
conservation (AUC = 0.74)" — that is the growing subset's AUC at that step. Conservation's
standalone AUC is unknown from the retrieved text.

Full review, with the candidate statistics and alignment sources compared:
[`../benchmark/evidence/conservation-confounder.md`](../benchmark/evidence/conservation-confounder.md).

## Decision

**1. The statistic is per-column Jensen–Shannon divergence, in the Capra & Singh
parameterisation** (doi:10.1093/bioinformatics/btm270): BLOSUM62 background distribution,
Henikoff–Henikoff sequence weights, λ = 1/2. Column name `jsd_conservation`, higher meaning
more conserved, so the objection corresponds to a **positive** Spearman ρ against the method.

**Why JSD and not rate4site.** Capra & Singh measured JSD at AUC₁ 0.9440 against Shannon
entropy's 0.9235, and found JSD and rate4site "not significantly outperformed by any other
method". The two are equivalent on accuracy. JSD needs an alignment and nothing else;
rate4site needs a phylogenetic tree, which is a second inference step to freeze and defend.

**2. The ±3-residue window heuristic is switched off.** Capra & Singh's window improves their
benchmark. Here it would inject sequence-local autocorrelation into a covariate whose entire
job is to correlate against a spatially autocorrelated score, which manufactures the
correlation the column exists to detect. This is a first-principles departure from the source
and it is recorded as one.

**3. The alignment source is Pfam full alignments, pinned to release 38.2**, fetched per family
through the InterPro API and mirrored as gzipped Stockholm. Every arm already carries its Pfam
accessions in the input manifest, so no new annotation is needed.

**The pinned artifact is the alignment itself, not a recipe for building one.** There is no
aligner to reproduce years from now, so determinism is exact by construction. That is the same
argument that made the decoy sets committed rather than re-derived.

Rejected sources, with the measurement that rejected each: **ConSurf-DB** is unreachable —
`ECONNREFUSED` on three attempts to three paths — and is rebuilt annually with no archived
releases, so it is unpinnable even when it answers. **UniRef** is reachable and pinnable but
30 GB. **UniClust for HHblits** is 75–103 GB. **`Pfam-A.full.gz`** whole is 22 GB; per family
through InterPro it is megabytes.

**4. Coevolution is not added, and the reason is a category error rather than absent
evidence.** A confounder column asks "is your score re-measuring a property of the residue?"
Coupling-to-the-source is not a residue property. It is a source-conditioned transport score
computed from sequence instead of from a contact graph — structurally the same object as
`allo.classical.coupling` (a module that left `main` on 2026-09-02, ADR 0037). Putting it in §11 would let a rival method masquerade as a control.

It is C1-clean and C2-clean, so nothing forbids it. It is blocked on evidence weight: the
supporting work is one group, one paper, N = 25 sites, pocket-level, compared against SCA and
never against conservation, while Teşileanu 2015 reports that SCA's top sector carries nothing
beyond single-site statistics and Chi 2008 found by double-mutant cycles that statistical
coupling does not report energetic coupling. **If it is ever added, it belongs beside
`cavity_volume` in the required baselines, not in §11.**

## Consequences

> **DECIDED, NOT BUILT.** Every bullet below is written in the present tense and none of it
> exists yet. `allo.structure.properties` returns three columns, `score_arm` still writes
> `confounders.conservation = None`, and `evaluation/manifest.yaml` carries the entry with
> `source: unknown`. Read the list as the work this ADR authorises, not as a description of
> the repository. Two findings from review 24 of the 2026-09-02 audit bear on it: the
> artifact-size objection dissolves, because 1.11 GB of Pfam alignments reduce to about
> **163 KiB** of content -- and that content is **untracked** today, under
> `../benchmark/review/data/conservation/`. Review 24 says 172 KB and an earlier draft of
> this box said "196 KB committed"; both were wrong, the second one twice, because 196 is
> the `du` figure including an ignored `__pycache__`; and coverage, not size, is the real blocker, with four arms below 0.55
> and `ns5b` at zero. `score_arm` rejects a partial column, so the ADR still owes an
> imputation rule it does not state.

- `evaluation/manifest.yaml` §11 names `jsd_conservation`, its parameterisation, the disabled
  window and the pinned Pfam release. Protocol version 3.
- `allo.structure.properties` gains the column. It stays on the **apo-only** side: the input is
  sequence, so C1 and C2 are both clear, and the module keeps its existing placement outside
  `allo/scoring/` so an apo-only caller does not execute the scoring package.
- The mirrored alignments are committed, one gzipped Stockholm file per Pfam family, and the
  release number is pinned beside them.
- **Two costs are stated rather than discovered later.** Pfam covers the domain envelope and
  not the whole chain, so some residues have no aligned column and read `null` — a specific
  risk on the 764-residue myosin arm. And the residue-to-column mapping is its own step with
  its own failure mode, so it carries its own test.
- The report gains one sentence it could not previously write: the rank correlation between
  every method's score and residue conservation, per arm.

## Alternatives rejected

**A protein-language-model proxy** — masked-token entropy or pseudo-log-likelihood from ESM.
Recorded as the fallback, not the recommendation: measured against ConSurf at Spearman
R = −0.374 (Marquet 2022), which is too weak to answer a conservation objection without
inviting a second objection about the proxy.

**Shannon entropy on the same alignments.** Cheaper and worse: AUC₁ 0.9235 against 0.9440, and
it ignores the background distribution, so a column of alanines scores as conserved as a column
of tryptophans.

**Leaving the column `null` and answering the objection in prose.** Rejected: R3 puts a
repository measurement above an argument, and the measurement is available.
