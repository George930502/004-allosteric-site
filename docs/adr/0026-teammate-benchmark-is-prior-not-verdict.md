# 0026 — The teammate benchmark fails ADR 0012's disjointness test, so it is prior and not verdict

**Status:** accepted · 2026-08-26

## Context

`allosteric-benchmark/` is a separate repository vendored inside this one. It is the source
of a great deal of what `docs/evidence/method-landscape/` treats as settled: eleven closed quantum
insertion points, the distance-confound measurements, the diversification number behind
stage S7, the learned-combiner result, and most of `review/00-conventions.md` §5.

`docs/evidence/method-landscape/11-pipeline-decomposition.md` §4a searched for an ADR vetting that
repository against ADR 0012's four disjointness clauses and found none. It recommended
writing one **before experiment 1**. This is that ADR.

**The check was run on 2026-08-26 and the disjointness does not hold.** All three primary
targets are present in that repository's own evaluation sets, at both site and family level.

| Primary target | Where it appears in `allosteric-benchmark/`                                                                                                                                                                                          |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| KRAS G12C      | `data/qasc_targets/kras_g12c.npz`, scored in `data/results_qasc3.json`; `data/targets_b/4EPV_A.npz` (UniProt P01116, KRAS); `data/targets_b/4EPT_A.npz` (same switch-II covalent series); `data/targets_b/3L8Y_A.npz` (HRAS, P01112) |
| BCR-ABL1       | `data/qasc_targets/bcr_abl1.npz`; `data/targets_curated/3K5V.npz` and `3PYY.npz`, both ABL1 **myristoyl pocket** — the same site our benchmark asks a method to predict                                                              |
| Cardiac myosin | `data/qasc_targets/cardiac_myosin.npz`; `data/targets_curated/2JHR.npz` and `3BZ7.npz`, Myosin-2 heavy chain, blebbistatin-site                                                                                                      |

Two qualifications, so the finding is not overstated. The curated myosins are Myosin-2
heavy chain rather than human MYH7 — the same fold and the same pocket class, a different
gene. And the vendored `external/allobench-pipeline/metadata/manifest.json` names KRAS,
ABL1 and MYH7 but was never built; it is an identifier list, not a result.

The mechanism ADR 0012 exists to prevent arrives here by a route no test watches. The guard
in `tests/test_no_leakage.py` follows the import graph and the file-read paths of _this_
repository. A sibling directory that a human reads and then acts on is neither.

**`3PYY` also fails clause 1 outright.** ADR 0012 rejects any record naming an accession
this benchmark uses in any arm, and the `3PYY` record lists `1OPL` — our mandated BCR-ABL1
apo — as a related complex.

## Decision

**Every result in `allosteric-benchmark/` is prior, not verdict.** Three rules follow, and
the third is the one that costs work.

1. **A negative result there does not close a method here.** The eleven quantum insertion
   points in `review/00-conventions.md` §5 are re-opened. They were measured on a different
   node representation (Cβ at 10 Å, unit weight), a different positive class, a different
   candidate pool (≥ 8 Å from every anchor), a different estimator and a different null.
   A method is closed for this project when an experiment on **this** frozen benchmark, run
   through `allo.scoring.score_arm`, produces a number.

2. **No hyperparameter may be set by reading that repository.** Not the cutoff, not the
   weighting, not a stiffening constant, not a diversification radius. Every knob is chosen
   on the secondary set's `development` tier and nowhere else (ADR 0021). Where their work
   supplies a _value_, this repository treats it as one point in a sweep and never as a
   default.

3. **Their methods are reimplemented rather than cited.** `ALPS` is reimplemented in
   `alps_spectral_response` from their source, so it runs on our graph, our labels and our
   null. That reimplementation left `main` with the method layer on 2026-09-02 and is on the
   branch `method-layer-archive` (ADR 0037); the rule that a rival method is reimplemented
   rather than cited is unaffected. A number computed under their protocol and quoted beside
   a number computed under ours is not a comparison
   (`docs/playbooks/experiment.md`, comparison hygiene).

**What survives unchanged.** Their _algebraic_ eliminations do not depend on any benchmark.
`review/00-conventions.md` §5 items 9, 10 and 11 — OTOC/Krylov collapsing to
`C(r,t) = 4 g²(r,t)`, Lieb-Robinson collapsing to the same transfer amplitude, and a real
symmetric contact graph having neither non-reciprocal hopping nor gain and loss — are
identities, not measurements. They stay closed on the mathematics.

**What their map changes for us, positively.** The same audit established that six specific
constructions were **never tested there**, which makes each of them genuinely open rather
than a repeat:

- effective resistance to the source (they compute `L⁺` but never form `R_ij`),
- a non-Hermitian sink at the active site, and the survival time it defines,
- Lindblad dephasing **with a trapping term** — their `enaqt_transfer` is pure dephasing
  with no sink, which is the canonical ENAQT figure of merit minus the term that creates
  its optimum,
- Szegedy / quantum PageRank (their `qpr` is "quantum perturbation response", a name
  collision),
- edge-class-weighted graphs; their arrays carry no residue identity at all, so hydrogen
  bonds and salt bridges are not derivable from their shipped data,
- anisotropic (ANM) perturbation-response scanning; their `prs` is the scalar GNM form.

## Consequences

- **`docs/evidence/method-landscape/00-conventions.md` §5 must be read with this ADR beside it.** Its
  eleven items are a prior over what is likely to fail, and they are informative — but the
  heading "do not re-derive it" no longer binds. It is amended rather than rewritten,
  because the measurements it reports are real measurements of something.
- **The Phase-2 sweep is larger than it would otherwise have been**, because closed items
  had to be re-opened. That cost is accepted. The alternative is a submission whose
  eliminations rest on a benchmark that contains its own test set.
- **The report must state this.** A reviewer who finds the sibling directory will ask the
  question, and the answer has to be already written down.
- Depends on ADR 0012 for the disjointness clauses and on ADR 0021 for where tuning is
  allowed. Does not supersede either.
- **Not a criticism of that work.** It was built for a different question, with its own
  benchmark, and it says so. The failure is that nobody checked its overlap with ours
  before treating its conclusions as ours — which is the failure this ADR closes.
