# 45 — The propagation source: does it have to be the active site, and does it have to be right?

**Experiment:** `experiments/2026-08-26-source-choice` · 760 records · 4 `development` arms ·
6 source families · 19 source-conditioned scorers · evaluation-default graph.

`CHALLENGE.md` §4.1 requires a ranking of residues by dynamic connectivity, "in most cases" to
an active site. The hedge is the organisers' own. It has to be: c-Myc, which §8.2 counts among
the minimum four targets, is a transcription factor with no catalytic site. So the question is
not academic, and it splits in two. Does a label-blind alternative source do as well? And does
a **random** source do as well, which would mean the source carries nothing?

Every source below is derived from the apo entry alone and is size-matched to that arm's frozen
active site. None reads a label.

---

## 1. The result in one table

| Source | Records | Mean AUC | Worst AUC | Reject rate | Hits@5 per record | Mean DCC Å | Overlap with catalytic |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `degree` | 76 | **0.705** | **0.425** | **0.171** | 0.395 | 18.08 | 0.045 |
| `eigenvector_centrality` | 76 | 0.687 | 0.181 | 0.066 | **0.592** | **16.06** | 0.136 |
| `buried` | 76 | 0.600 | 0.277 | 0.013 | 0.421 | 18.00 | 0.210 |
| `catalytic` | 76 | 0.564 | 0.129 | 0.118 | 0.526 | 18.94 | 1.000 |
| `random` | 380 | 0.543 | 0.085 | 0.076 | 0.182 | 21.85 | 0.023 |
| `fiedler` | 76 | 0.527 | 0.230 | 0.026 | 0.026 | 30.99 | 0.000 |

**The catalytic active site is the fourth-best source of six.** It sits 0.141 AUC below the
eleven highest-degree residues and 0.021 above a random size-matched set.

`degree` is the best source for 13 of the 19 scorers. The catalytic site is best for none.

**The invariance check passed on all four arms.** `degree` as a *scorer* ignores the source, so
its score has to be identical in every row of an arm. It is: one distinct checksum per arm,
four of four. A source is therefore not leaking anywhere it should not.

---

## 2. Source conditioning does carry information, and less than expected

The `random` row is the floor and it is the row the experiment was built around. If a random
size-matched source scored like the catalytic one, then "propagation from the active site" would
be decoration and every claim in the report resting on it would be void.

It does not. Catalytic beats random on the confirmatory endpoint, 0.118 against 0.076, and on
the deliverable, 0.526 hits at 5 per record against 0.182. **The framing survives.**

But the margin on AUC is 0.021, and three label-blind alternatives beat the catalytic site on
that axis. The honest statement is that the source matters, and that the active site is not the
best answer to what the source ought to be.

---

## 3. Where the variance actually lives

Mean AUC per arm, over all 19 source-conditioned scorers:

| Source | `mkp5` | `ptp1b` | `hiv_rt` | `ns5b` | Spread |
| --- | --- | --- | --- | --- | --- |
| `catalytic` | 0.723 | 0.399 | **0.809** | 0.323 | **0.486** |
| `eigenvector_centrality` | 0.762 | 0.463 | 0.664 | 0.857 | 0.394 |
| `fiedler` | 0.422 | 0.456 | 0.461 | 0.770 | 0.348 |
| `buried` | 0.712 | 0.471 | 0.743 | 0.476 | 0.272 |
| `degree` | 0.685 | 0.608 | 0.683 | 0.845 | **0.237** |
| `random` | 0.588 | 0.555 | 0.479 | 0.550 | **0.109** |

**This is the finding that matters, and it is not the mean.** The catalytic source has the
largest between-arm spread of any source tested. It is the best source on `hiv_rt` at 0.809 and
close to the worst on `ns5b` at 0.323. The degree source is never excellent and never broken:
its floor is 0.608 where the catalytic floor is 0.323.

So the active site is the right source for some proteins and the wrong source for others.
**Which of the two a given protein is cannot be known without a label**, and that is the same
per-protein heterogeneity the method sweep found and could not name. This experiment names one
of its causes.

The `random` row confirms the reading rather than weakening it. A random source has the smallest
spread of all, because averaging over five arbitrary seeds averages the protein-specific
structure away. Low variance here is a symptom of carrying no signal, not of carrying robust
signal. Read the two columns together or not at all.

---

## 4. The two endpoints disagree again, and they disagree by source

`degree` wins mean AUC (0.705) and the reject rate (0.171). `eigenvector_centrality` wins the
deliverable: 0.592 hits at 5 per record and the closest predicted centre at 16.06 Å.
`catalytic` is second on hits at 5 with 0.526 and fourth on AUC.

This is the third independent place in the repository where the confirmatory endpoint and the
five-residue hit list rank the same options differently. The first was the `cavity_volume`
baseline, the second was spatial smoothing in `2026-08-26-fusion-probe`. A method frozen for the
challenge and a method frozen for the confirmatory test are not the same method, and the choice
has to be made once, deliberately, and written into an ADR.

`fiedler` is the clearest failure in the experiment. It puts the source on the two lobes of the
slowest Laplacian mode, which are by construction on opposite sides of the protein, and it
produces 2 hits at 5 across 76 records with a mean DCC of 31 Å. A source split across the
structure predicts the centre of the structure, which is nowhere in particular.

---

## 5. Quantum and classical respond to the source the same way

| Family | `catalytic` | `eigenvector` | `degree` | `buried` | `fiedler` | `random` |
| --- | --- | --- | --- | --- | --- | --- |
| classical | 0.613 | 0.705 | 0.722 | 0.625 | 0.581 | 0.588 |
| quantum | 0.527 | 0.673 | 0.693 | 0.582 | 0.488 | 0.511 |

The ordering is identical in both rows and the classical row is above the quantum row at every
source. The source choice is therefore a property of the pipeline stage, not of the quantum
layer, and it can be settled once for both.

---

## 6. What this hands forward

1. **A source rule that runs on c-Myc.** `degree` and `eigenvector_centrality` need no catalytic
   site, no cognate ligand and no sequence motif. They are computable on any modelled chain. The
   c-Myc contract that ADR 0020 requires now has a source rule that does not depend on a
   catalytic site existing.
2. **A candidate remedy for cross-protein variance.** Replacing the catalytic source with the
   degree source cuts the between-arm AUC spread from 0.486 to 0.237.
3. **A question the challenge text leaves open, answered with a number.** "In most cases, to an
   active site" is compatible with what we measure. It is not compatible with a claim that the
   active site is the best source, and no such claim should appear in the report.

---

## 7. What would overturn this, and what it is not yet

**This is a screen, not a result.** Six source families were compared on four arms and the best
was selected afterwards. That is selection over six options with the same multiplicity cost
`41-selection-and-power.md` prices for every other axis. A source rule is a hyperparameter, and
under ADR 0012 it is chosen on `development` and then frozen and scored once.

Three specific threats:

- **`degree` and `eigenvector_centrality` may be winning for a reason unrelated to allostery.**
  Both put the source in the packed core. A score propagating from the core is close to a global
  centrality, and centrality is a known confound. `46-beats-distance.md` is where that is tested.
- **The catalytic sets differ in size between arms**, from 3 residues on `ns5b` to 11 on `mkp5`
  and `ptp1b`. Every alternative is size-matched per arm, so the comparison within an arm is
  clean, but a between-arm comparison still carries the source size.
- **Four arms is four.** The spread column is computed from four numbers and is an estimate with
  a wide interval. It orders the sources; it does not measure the ordering precisely.

**What would change the conclusion.** A source rule whose worst-arm AUC clears 0.65 and whose
calibrated p clears 0.05 on three of four arms, holding on the `generalisation` tier after the
method is frozen. Nothing here reaches that yet: the best reject rate in the table is 0.171,
which is 13 of 76.

---

## 8. Reproducing this

```bash
uv run python experiments/2026-08-26-source-choice/run.py
```

Resumable. `records.jsonl` is keyed by `arm|source|scorer` and an existing key is not recomputed.
Every number above is derived from `records.jsonl` by `summarise` in the same file.
