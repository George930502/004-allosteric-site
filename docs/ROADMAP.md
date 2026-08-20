# Roadmap

Each phase has an explicit **exit criterion** — a check that either passes or does
not. No phase is "done" on vibes. Update the status table in `README.md` and this
file when a phase closes.

**Current phase: 1 (Classical foundation).** Sub-phase 1.0 (frozen benchmark) closed 2026-08-20.

---

## Phase 0 — Repository and agent harness ✅

Repo, packaging, verification gate, CI, agent contract, experiment ledger.

**Exit:** `make check` passes on a clean clone; CI green.

---

## Phase 1 — Classical foundation, ground truth, scoring harness

Nothing quantum yet. This phase builds the substrate everything else is measured
against. Getting the ground truth and the statistics right here is what makes every
later number believable.

0. **Frozen benchmark ✅ (closed 2026-08-20)** — the input layer is fixed before any
   method exists, so method comparisons are honest. An audit of the challenge's own
   apo/holo assignments found all three defective, one fatally (`6C1H` contains neither
   mavacamten nor cardiac myosin). Response is tiered — mandated / corrected /
   sensitivity — and pre-registered in `docs/benchmark/manifest.yaml`.
   **Exit (met):** `make verify` (`allo benchmark verify` plus the network-marked tests)
   exits 0; `make check` passes. `make check` is offline by design, so it does _not_
   re-derive the freeze — `make verify` is the command that does, and it needs network.
   See `docs/benchmark/README.md`, ADRs 0003–0005.

   **Re-anchored 2026-08-20 (ADR 0007, ADR 0008).** The benchmark had been assembled with
   the cryptic-pocket literature as its definitional backbone; the challenge asks for
   **allosteric sites**, which is a functional property, not a structural one. The pairs,
   coordinates and label sets did not change — the entry criterion and the framing did.
   Concretely: the apo/holo definition is now the allostery field's nine clauses; crypticity
   is a reported difficulty axis with no pass/fail; the label set is the scoreable set
   (labels minus propagation-source residues, AlloPred's rule) with no distance threshold;
   every target now carries `allosteric_evidence`, `state` and `blind` fields enforced by
   `tests/test_benchmark.py`; and myosin gained a second **target** (Site 2, aficamten) plus
   a Site 1 sensitivity arm, 11 targets in total. **No** arm in the primary benchmark is blind (corrected 2026-08-20; myosin Site 1 was
   wrongly recorded as blind until challenge reference [1] was re-read to its second site). See `CONTEXT.md` for the settled vocabulary.

   **Adversarial re-verification 2026-08-20.** Five independent agents re-checked the freeze
   against RCSB, the primary literature and the C1–C6 constraints. All 11 structural claims
   held, including the two the tiering rests on (`6C1H` contains no mavacamten; `1OPL` is holo
   at the site). What did not hold was the citation and prose layer: three DOIs pointed at
   unrelated papers, one paper title was attributed to a DOI seven years too early, the
   aficamten paper was cited under the wrong first author, README §1's occupancy table had
   gone stale against the code, and §5's AUC line no longer regenerated. All corrected, and
   each class now has a test or a derived field behind it rather than a promise. Two decisions
   were forced out into the open: **ADR 0009** (resolution is a selection rule, so it binds the
   ASD set and not the hand-specified primary arms) and **ADR 0010, proposed** (the node set is
   the modelled chain, not a trimmed catalytic domain — worth the PI's explicit call, since the
   strict C5 reading would shrink the mandated ABL1 arm by ~40 %). One real C1 leak *surface*
   was closed: `manifest.yaml` carries label residue numbers in prose, so `allo.inputs.load()`
   now redacts the holo half by allow-list and two new tests hold it there.

1. **Structure ingest** — fetch apo PDBs, select catalytic domain / chain, drop
   waters, co-factors and PTMs (C5), index residues canonically (auth numbering,
   preserved end to end so hit lists are chemist-readable). _Partly done: fetch/parse and
   ligand-contact selection are in `src/allo/structure/`; domain trimming is open._
2. **Network construction** — Cα (and optionally side-chain centroid) contact graph;
   cutoff and weighting scheme as configurable knobs; verify connectivity and degree
   distribution per target.
3. **Ground truth ✅** — implemented in `src/allo/groundtruth/labels.py`: ligand-contact
   residues at 4.5 Å, transferred to apo numbering by sequence alignment, unmapped labels
   reported. Import isolation enforced by `tests/test_no_leakage.py`. Frozen per target.
4. **Negative sets** — random background residues, and non-functional surface pockets
   (the challenge scores against both). Surface-pocket decoys need a geometric pocket
   detector or a documented substitute.
5. **Classical baselines** — GNM/ANM mode-based, perturbation-response scanning,
   random-walk / diffusion kernel, betweenness centrality. These are the "classical
   analogs" the challenge asks us to compare against, and the bar quantum must clear.
6. **Scoring harness** — the protocol pre-registered in `docs/benchmark/README.md` §5,
   implemented once and called identically by every method: **AUC-ROC and AUC-PR**
   co-primary (the Mann-Whitney U statistic _is_ AUC-ROC rescaled — one procedure, not
   two), precision@5 and P(≥1 hit) against the exact hypergeometric baseline, and the
   **matched connected-patch permutation null** against both negative sets.
7. **Selection set (ASD).** A development set of ASD targets, built and frozen _before_
   Phase 2. Every hyperparameter — metric, Hamiltonian, cutoff, coarse-graining ratio —
   is chosen here and nowhere else. Without it, Phase 2's ablations would be selected on
   the frozen primary benchmark, which is test-set fitting even with no holo import
   (`docs/benchmark/README.md` §5, `docs/FIELD.md` trap 4). This is why the ASD set is a
   Phase 1 deliverable and not the Phase 5 nicety an earlier draft made it.

**Exit:** for all three validation targets, a committed baseline experiment reporting
enrichment statistics for every classical method, reproducible from its config, with
a leakage test proving no holo-derived data reaches the prediction path — and a frozen
selection set that no primary-benchmark number was used to build.

---

## Phase 2 — Quantum propagation metric (statevector)

Hamiltonian constructions from the network; continuous-time quantum walk from the
active site; candidate metrics (time-averaged transfer probability, peak transfer,
integrated coherence, quantum Fisher information). Produce the N x N connectivity
matrix and top-5 hit lists. Ablate: which metric, which Hamiltonian, which active-site
definition — **on the Phase 1.7 selection set**. The frozen primary benchmark is scored
once, with the choice already fixed.

**Exit:** at least one quantum metric beats the best classical baseline on the primary
criterion across targets, with the comparison run through the Phase 1 harness and the
mechanism (why interference helps here) argued, not just asserted.

---

## Phase 3 — Circuits, depth budget, noise resilience

Trotterised `exp(-iHt)` in the single-excitation sector; gate counts, depth, qubit
count and connectivity requirements reported per target (C3). Aer noise models sweeping
gate error and decoherence; stability of the _ranking_, not just the raw metric, since
the ranking is the deliverable. Execute a coarse-grained instance on AWS Braket and/or
via Classiq synthesis.

**Exit:** resource table per target, ranking-stability curves vs. noise strength, and
at least one real-hardware or hardware-emulated run.

---

## Phase 4 — Coarse-graining and scalability

Compress the network (spectral / community / domain-based) so targets exceeding qubit
capacity remain tractable, and **prove the compression retains the essential
topological signal** — the challenge asks for proof, not assertion: spectral distance
between full and coarse propagators, rank correlation of residue scores, recovery of
the known pocket at each compression ratio.

**Exit:** compression-ratio sweep showing where the signal breaks, plus a rule for
picking the ratio for an unseen protein.

---

## Phase 5 — Interpretability, delivery, extra targets

3D visualisation of connectivity maps on the structure; c-Myc (`1NKP`) prediction;
further **held-out** ASD targets for generalisability (distinct from the Phase 1.7
selection set, which has already been tuned on and cannot demonstrate generalisation); the methodological report tying the
quantum metric to the biology; final artifact pass for all four minimum targets.

**Exit:** all three required artifacts present for KRAS, BCR-ABL1, cardiac myosin and
c-Myc, plus the supporting-evidence set listed in `CHALLENGE.md` §8.
