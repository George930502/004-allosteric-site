# The Phase-2 literature sweep

Seven reviews, compiled 2026-08-26. `../../review/` covered the field the challenge names:
allosteric-site prediction, classical and AI and quantum. This sweep covers the fields it
does **not** name, because a method that only reads its own literature can only rebuild what
that literature already built.

The instruction these seven answer:

> For the method development, we need to do the broad review on different topics. In frontier
> research it is very often to utilize the similar topic research findings as the inspiration
> to develop on the existing pipeline, do the modifications or do the fusion of different
> methods.

Same conventions as `../../review/`: `[VERIFIED-FULLTEXT]`, `[VERIFIED-ABSTRACT]` and
`[UNVERIFIED]` on every claim, a DOI or arXiv identifier on every source, and a recorded
"not retrieved" where a search came back empty (ADR 0019).

---

## The seven

| File                                                                   | Field mined                                              | The one thing to take from it                                                                                                                                              |
| ---------------------------------------------------------------------- | -------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`20-ppi-hotspot-transfer.md`](20-ppi-hotspot-transfer.md)             | Protein–protein interface hot spots                      | A hot spot is defined by an energetic criterion we cannot compute, and every structural proxy for it reduces to burial                                                     |
| [`21-structure-to-residue-score.md`](21-structure-to-residue-score.md) | Six adjacent structure-in / score-out tasks              | Performance falls monotonically as the positive class moves away from the orthosteric pocket: 0.749 → 0.680 → 0.363 → 0.077. Our class is the last one                     |
| [`22-transport-formalisms.md`](22-transport-formalisms.md)             | Transport on graphs and elastic networks                 | Nearly every propagation score is a function of the same operator read at the same source column, so most of them are one measurement wearing different names              |
| [`23-quantum-node-ranking.md`](23-quantum-node-ranking.md)             | Quantum node ranking on a classical graph                | Eight constructions that are genuinely new rather than transforms of the single-particle amplitude, each priced in flops at N = 272 and N = 1058                           |
| [`24-residue-descriptors.md`](24-residue-descriptors.md)               | Per-residue physicochemical and evolutionary descriptors | Do not add packing descriptors. Voronoi volume, weighted contact number, occluded surface, residue depth, DPX and CX are one axis, and the frozen null already controls it |
| [`25-md-free-fluctuation.md`](25-md-free-fluctuation.md)               | Predicting fluctuation without MD                        | The C2 verdicts, model by model — and the finding that the deposited B-factor is the whole route's oracle, so one line of code closes or opens it                          |
| [`26-system-mechanisms.md`](26-system-mechanisms.md)                   | How allostery works in seven mapped systems              | Eight recurring structural signatures ranked by how many independent systems support each. Three are apo-observable and were not in the repo                               |

---

## What the sweep changed in the code

Every item below exists because one of these seven files argued for it, and each names the
file it came from.

| Added                                                            | From | Module                                  |
| ---------------------------------------------------------------- | ---- | --------------------------------------- |
| Nine source-conditioned coupling measures                        | `22` | `allo.classical.coupling`               |
| Three cross-system mechanism signatures                          | `26` | `allo.classical.mechanism`              |
| Opening-strength sweep with a trap, and the depth of its optimum | `23` | `allo.quantum.walk`                     |
| Deposited B-factor as the fluctuation route's oracle             | `25` | `allo.classical.baselines.mean_bfactor` |
| Distance to chain centroid, local contact order                  | `24` | `allo.classical.baselines`              |

## What the sweep stopped

Also results. Each of these prevented work rather than creating it.

- **Packing descriptors** (`24`). Six candidate columns, one axis, already in the null.
- **Fluctuation ranking as a deliverable** (`25`). `CHALLENGE.md` §4.1 asks for a ranking by
  dynamic connectivity and §5 for an N × N matrix. A per-residue fluctuation vector is
  neither, and Yang and Bahar put catalytic sites at global-hinge _minima_ in over 70 % of 98
  enzymes, so a naive fluctuation ranking returns the negative class.
- **Boltz-2, idpGAN, ProTDyn, PHASE, ENSEMBITS, LD-FPG, GeoGraph, PEGASUS** (`25`). All
  trained on MD trajectories. C2 forbids them, and Boltz-2's own text says so — which
  corrects the natural assumption that the Boltz family is PDB-only.
- **Quantum reservoir computing** (`23`). A supervised linear readout on holo-derived labels
  with a hundred-protein budget, and a contact-graph reservoir is 2^N.
- **PDBFlex for our targets** (`25`). It clusters at 95 % identity, so the cluster contains
  the holo entries. An answer key wearing a database URL.

---

## How these relate to the earlier reviews

`../../review/00-conventions.md` §5 lists eleven quantum insertion points as closed. **ADR
0026** re-opens them: the benchmark that closed them contains all three of our primary
targets in its own evaluation sets, so its negative results are prior and not verdict. File
`23` is the re-derivation that follows, and it separates what is genuinely new from what is a
transform of an observable we already compute.

Three of the eleven survive re-opening on mathematics rather than on measurement, and stay
closed: the OTOC and Krylov collapse to `C(r,t) = 4 g²(r,t)`, the Lieb-Robinson bound
collapsing to the same transfer amplitude, and a real symmetric contact graph having neither
non-reciprocal hopping nor gain and loss. Those are identities. No benchmark can change them.
