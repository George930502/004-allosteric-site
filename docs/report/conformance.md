# What the challenge asks for, and where we stand

**Source:** `CHALLENGE.md`, the verbatim restatement of
`docs/Cleveland-Clinic-Challenge-Statement-vF.pdf`. Re-read against the PDF on 2026-08-26.
**Status of this page:** it tracks conformance, not quality. A row marked "done" means the
artifact exists, not that the number in it is good.

Every row cites the clause it comes from. Where our repository is stricter than the
challenge, or where the challenge contradicts itself, the row says so, because those are the
two places a reader gets misled.

---

## 1. The three required outputs (§5)

| # | Required output | Clause | Status |
| --- | --- | --- | --- |
| 1 | **N × N connectivity matrix**, entry (i, j) = quantum connectivity strength between residue i and residue j | §5, §8.2 | **built, not exported.** `allo.quantum.connectivity.connectivity_matrix(graph, form=, mode=)` returns it. Verified on `mkp5`: shape (147, 147), symmetric to 2e-17, rows sum to 1, all finite, in both `laplacian` and `adjacency` form and both `finite` and `infinite` mode. No `results/<target>/connectivity.npz` is written yet |
| 2 | **Top-5 ranked allosteric residue hit list** per target | §5, §8.2 | **not exported.** `hits_at_5` and `recall_at_5` are computed inside the scoring harness for every arm, so the ranking exists; no `hits.csv` is written |
| 3 | **Methodological report** — the quantum metric and why it proxies biological signal transmission | §5, §8.3 | **in progress.** `docs/report/` is the home; this page is the first section |

**Row 1 was the largest single gap. The definition is now settled and the export is not.**
A CTQW transfer probability `|<i|exp(-iHt)|j>|^2` is naturally an N × N object, and the
vector we score is one column of it summed over the source residues. `connectivity_matrix`
takes that object as *the* matrix and normalises each row to a probability, so the reported
matrix and the reported hit list come from one construction. Several observables —
`quantum_opening_gain`, `protrusion_index` — have no N × N form at all, so they cannot be
the headline metric. What remains is the exporter and the choice of `form` and `mode`, which
is a freeze decision rather than a definition problem.

---

## 2. Primary objective (§4.1)

| Requirement | Clause | Status |
| --- | --- | --- |
| Build a **quantum circuit** that simulates signal propagation | §4.1, §8.1 | **not built.** The quantum layer is exact statevector linear algebra in NumPy. No circuit, no gate count, no transpilation. `docs/method/exploration/results/43-quantum-resources.md` prices circuits on paper; nothing is compiled |
| Output a **ranking of residues by dynamic connectivity**, in most cases to an active site | §4.1 | **done.** Every scorer returns a residue-keyed ranking through `allo.scoring.score_arm` |
| Score **significantly higher** on known distal regulatory residues than on **random background residues** | §4.1 | **done and measured.** This is the matched-patch null in the frozen evaluation layer |
| …and than on **non-functional surface pockets** | §4.1 | **done and measured.** This is the decoy-pocket class, detector-defined (ADR 0024) |

**The success criterion in §4.1 matches our frozen evaluation layer clause for clause.** The
challenge names two negative classes — random background and non-functional surface pockets
— and the evaluation layer implements exactly those two. This was not designed backwards
from the challenge text, so the agreement is worth recording.

**"In most cases, to an active site" is the organisers' own hedge, and it is load-bearing.**
c-Myc, which §8 lists among the minimum four targets, is a transcription factor with no
catalytic site. A pipeline that requires a catalytic source cannot run on it.
`experiments/2026-08-26-source-choice` measures what happens when the source is something
else.

---

## 3. Secondary objectives (§4.2)

| Objective | Clause | Status |
| --- | --- | --- |
| **Noise resilience** — stability of the metric despite gate errors and limited coherence times | §4.2 | **partly measured.** `experiments/2026-08-26-stability-and-source` sweeps the coherence window and two input-perturbation families. Gate error is not yet modelled, because there is no circuit to put gate errors on |
| **Scalability / coarse-graining**, with a **proof that compression retains the essential topological signal** | §4.2, §8.4 | **not started.** Phase 4. The word "prove" is the organisers'; a measured correlation between coarse and fine rankings is not what the clause asks for |
| **Interpretability** for medicinal chemists without extensive training | §4.2 | **partly done by construction.** Residue identity is author numbering plus chain ID end to end, so a hit list is readable. No chemist-facing artifact exists |
| **Actionable output** — 3D visualisation of the connectivity maps, prioritised | §4.2, §8.4 | **not started.** Phase 5. `viz/` is reserved and empty |
| **Classical comparison**, where relevant | §4.2, §8.4 | **done and measured.** 43 classical scorers against 11 quantum, every one through the same harness |
| **Statistical enrichment vs random and decoy residues** | §8.4 | **done and measured.** The frozen protocol, version 2 |
| **Near-term hardware feasibility / circuit depth analysis** | §8.4 | **on paper only.** Resource estimates exist; no compiled circuit backs them |

---

## 4. Constraints (§5) and the checklist (§9)

| Constraint | What the challenge says | What we enforce | Gap |
| --- | --- | --- | --- |
| Apo input only | "must use the **unbound (apo) structure as input** and **blind-predict**" (§6) | C1, an import guard, thirteen protected file routes, `tests/test_no_leakage.py` | none. We are stricter, deliberately |
| No classical MD | "cannot rely on classical MD **trajectories as inputs**" (§5.3) | C2, now three provenance tiers (ADR 0027) | we were stricter than the text and have said so explicitly rather than silently |
| Catalytic domains only; no water, co-factors or PTMs unless simple nodes | §5 Scope | C5, read as scoping the system rather than trimming a chain (ADR 0010) | none |
| Elastic network hypothesis | §5 Assumption | C6 | none |
| Circuit depth aware, near-term viable | §5.2 | C3 | **open** — no compiled circuit |
| Credible hardware execution path | §5.1 | C4 | **open** — the statevector layer needs a stated mapping |
| **Uses AWS Braket and/or Classiq** | §5.4, §9 | — | **open.** `pyproject.toml` carries the `hw` extra. Nothing has been run on either service |
| **Open-source frameworks, for example Qiskit** | §6, §9 | — | **open.** The quantum layer is NumPy. It is reproducible and open source, but it is not a circuit framework |
| All three artifacts per target | §9 | — | **open**, see §1 above |
| **Minimum four targets** | §9, §8.2 | five primary arms | **open on identity, not on count** — see below |

---

## 5. The target list, and a contradiction in the source document

§6 Table 1 names three validation targets and calls c-Myc a **stretch target**. §8.2 then
requires "4 minimum: KRAS G12C 4OBE, BCR-ABL1 1OPL, Cardiac Myosin 5TBY, c-Myc 1NKP",
which counts c-Myc among the minimum. The two clauses disagree, and the safe reading is the
stricter one: **produce artifacts for all four, c-Myc included.**

| Target | Mandated apo | Our arm | Note |
| --- | --- | --- | --- |
| KRAS G12C | 4OBE | `kras_g12c_mandated`, plus `kras_g12c_corrected` (4LDJ) | both scored, tiered |
| BCR-ABL1 | 1OPL | `bcr_abl1_mandated`, plus `bcr_abl1_corrected` (2G2H) | both scored, tiered |
| Cardiac myosin | 5TBY | `cardiac_myosin_corrected` (9GZ3) | **the mandated pair is unscoreable as assigned.** A method must still emit the three artifacts for 5TBY, because §8.2 asks for artifacts and not for a score |
| c-Myc | 1NKP | **none** | **no arm exists.** ADR 0020 requires the c-Myc contract before method design, and it is unwritten |

Why the substitutions exist is in `docs/benchmark/primary/README.md`. The distinction that
matters here: a defective pair blocks **scoring**, not **output**. Deliverable rows 1 and 2
are artifacts, and they can be produced for 4OBE, 1OPL, 5TBY and 1NKP whether or not a
ground truth exists to score them against.

---

## 6. What this page changes about the plan

Four items are conformance gaps rather than quality gaps, and none of them is answered by a
better score:

1. **Export the N × N connectivity matrix.** The construction exists and is verified. What is
   left is a writer for `results/<target>/connectivity.npz` and a frozen choice of `form` and
   `mode`. The choice constrains which observable can be the headline metric.
2. **Compile a circuit.** §4.1 says "must build a quantum circuit". A statevector simulation
   of a Hamiltonian is not one, however faithful. Braket or Classiq or Qiskit, with a gate
   count and a depth, on at least one target.
3. **Give c-Myc a contract**, or state in the report why the target is excluded. ADR 0020
   already says this blocks method design.
4. **Emit artifacts for the mandated accessions**, including the ones our benchmark cannot
   score, so that the deliverable list is complete on its own terms.

Nothing here contradicts the current phase order. It says which Phase 3 to Phase 5 items are
**required** rather than desirable, and item 1 is earlier than the roadmap has it.
