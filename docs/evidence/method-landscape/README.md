# The method landscape — literature evidence, no method

A scoped survey of how the field predicts allosteric sites, compiled 2026-08-25. Twenty-three
documents, every claim carrying a DOI.

**This directory holds no code, no scored number and no selected variant.** It was written
before any method existed in this repository, and it survived the removal of the method layer
on 2026-09-02 for that reason. It is evidence under principle R3, not a proposal.

## Why it is here and not under `docs/benchmark/evidence/`

`docs/benchmark/evidence/` is protected against reads from the prediction path, because it
prints label residues. This directory prints none, so it carries no such guard. Keeping the
two apart stops a future reader from assuming that everything under `evidence/` is an answer
key.

## What cites it

Two accepted ADRs rest on these documents, and both bind the frozen layer.

| ADR    | What it takes from here                                                            |
| ------ | ------------------------------------------------------------------------------------ |
| `0026` | `11-pipeline-decomposition.md`, and `00-conventions.md` section 5                    |
| `0027` | `15-ai-preprocessing.md`, the admissibility table the three C2 tiers are applied to |

## Read this first

`10a-fact-check.md` audits the numbers in the other documents. Read it before quoting any of
them. `20-fact-check-17-19.md` does the same for documents 17 to 19.

## What was removed with the method layer

`docs/method/exploration/` held what happened when the experiments ran on 2026-08-26. Those
runs, the nine experiment directories beside them, and the code that produced them were
removed from `main` on 2026-09-02. They are preserved whole on the branch
`method-layer-archive`. A document here that points into `exploration/` points at that branch.
