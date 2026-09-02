# 0027 — C2 is three tiers of provenance, not a single ban, and the primary result stands on tier A

**Status:** accepted · 2026-08-26

## Context

`AGENTS.md` C2 states:

> **No classical MD trajectories as input.** Dynamics must be predicted _ab initio_ from
> topology. No GROMACS/AMBER/OpenMM trajectories, no MD-derived covariance matrices, no
> MD-trained ML weights in the prediction path.

`CHALLENGE.md` §5 restates the official constraint verbatim, and it is shorter:

> 3. **No Classical MD:** The solution **cannot rely on classical MD trajectories as
>    inputs**. The goal is to **predict the dynamics _ab initio_ from topology**.

The last clause of C2 — **no MD-trained ML weights** — is ours. It is not in the challenge
statement. It was written in Phase 0 as a conservative reading and never revisited.

That clause now blocks work the principal investigator has asked for. Phase 2 measured that
between-protein variance dominates every other effect: one fixed pipeline that is good on a
phosphatase is poor on a polymerase. The direction given is to add an AI preprocessing stage
that characterises the input protein and adapts the pipeline to it. Several of the obvious
candidates — PocketMiner, AlphaFlow, BioEmu, learned flexibility predictors — were trained
on MD trajectories. Under C2 as written, all of them are excluded. The competition is titled
"Global Quantum + **AI** Challenge 2026", so a blanket exclusion of learned components is
also hard to defend on intent.

**The principal investigator's argument, and where it is right and where it stops.** The
argument is that a frozen input layer and a frozen evaluation layer put every method under
identical conditions, so the comparison stays fair. That is correct about **internal
comparability**: `allo.scoring.score_arm` is the only path a number may take, and it does
not care what produced the score. It is not an argument about **external admissibility**.
Whether a component is allowed is set by the organisers, not by the fairness of our own
harness. The two questions are separate and this ADR answers only the second.

## Decision

**Replace the single ban with three provenance tiers.** Every component on the prediction
path is assigned a tier, and the tier is disclosed in the report.

| Tier | Provenance | Status |
| --- | --- | --- |
| **A** | No training, or trained only on static structures and sequences. GNM/ANM and normal modes, geometric pocket detectors, conservation and coupling from alignments, protein language models trained on sequence, foldseek, AlphaFold pLDDT and PAE. | **Admissible without qualification.** |
| **B** | Trained on MD trajectories. The trajectory shaped the weights; it is not an input at inference time. | **Admissible, disclosed, and reported separately.** Never load-bearing for the primary result. |
| **C** | An MD trajectory or an MD-derived covariance matrix passed as an input at inference. Anything trained on this benchmark's holo structures or label sets. | **Forbidden.** Unchanged. |

**The primary result must stand on tier A alone.** A tier B component enters only as a
labelled ablation that reports what it buys, alongside the tier A number it is compared
against. The submission is then correct under either reading of Constraint 3, and the
question of what learned preprocessing is worth still gets an answer.

**Every tier B use states its training set and cites it.** "Training data not determined"
disqualifies a component from use, because an undetermined provenance cannot be placed in a
tier.

## Consequences

**What this unblocks.** A front-end stage may compute learned per-residue features and may
adapt downstream hyperparameters to the input protein, provided the components are tier A.
The label-free adaptation route — choosing a parameter by a criterion that never sees a
label — is tier A by construction and is preferred for that reason.

**What does not change.** C1 is untouched. Holo structures still enter only through
`allo.groundtruth/`, the five protected data routes still hold, and `tests/test_no_leakage.py`
still enforces both. The `no MD-derived covariance matrices` clause of C2 is kept verbatim in
tier C, because a covariance matrix is a trajectory in compressed form and using one is
relying on a trajectory as an input.

**The disclosure that has no clean fix.** A model pretrained on the whole PDB has seen holo
entries that appear in our label sets. There is no way to unsee them retroactively, and
date-based holdout cannot be applied to weights already trained. This is disclosed in the
report rather than argued away. It is one more reason the primary result stands on tier A,
where the strongest members — GNM, ANM, geometric detectors, alignment statistics — involve
no training at all.

**Cost if this is wrong.** If a judge reads Constraint 3 the strict way, a tier B ablation is
a labelled appendix and the primary result is unaffected. That asymmetry is the whole reason
for the tier split.

## Alternatives rejected

**Keep C2 as written.** Safe, and it forecloses the direction the principal investigator
asked for, on a clause the challenge does not contain.

**Delete the clause outright.** This is what the instruction taken literally asks for. It
loses the distinction between a component that never touched MD and one that is a regression
on MD, and that distinction is exactly what a reviewer will ask about.

**Decide per component as each arises.** No standing rule, so the decision drifts and the
report cannot state one policy. Rejected on R2.

## References

- `CHALLENGE.md` §4.1, §5 Constraints, §6 Critical rule
- ADR 0012 (tier discipline), ADR 0021 (secondary set selection clauses)
- `docs/evidence/method-landscape/15-ai-preprocessing.md` — the admissibility table this ADR's tiers are applied to
