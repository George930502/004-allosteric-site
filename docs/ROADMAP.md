# Roadmap

Each phase has an explicit **exit criterion** — a check that either passes or does
not. No phase is "done" on vibes. Update the status table in `README.md` and this
file when a phase closes.

**Current phase: 1 (Classical foundation).**

---

## Phase 0 — Repository and agent harness ✅

Repo, packaging, verification gate, CI, agent contract, experiment ledger.

**Exit:** `make check` passes on a clean clone; CI green.

---

## Phase 1 — Classical foundation, ground truth, scoring harness

Nothing quantum yet. This phase builds the substrate everything else is measured
against. Getting the ground truth and the statistics right here is what makes every
later number believable.

1. **Structure ingest** — fetch apo PDBs, select catalytic domain / chain, drop
   waters, co-factors and PTMs (C5), index residues canonically (auth numbering,
   preserved end to end so hit lists are chemist-readable).
2. **Network construction** — Cα (and optionally side-chain centroid) contact graph;
   cutoff and weighting scheme as configurable knobs; verify connectivity and degree
   distribution per target.
3. **Ground truth** — derive allosteric pocket residues *programmatically* from the
   holo structure: ligand heavy atoms within a distance cutoff of protein heavy atoms,
   mapped onto apo residue numbering by sequence alignment. Never hand-typed (see
   `docs/targets.md`). Lives in `src/allo/groundtruth/`, import-isolated from the
   prediction path.
4. **Negative sets** — random background residues, and non-functional surface pockets
   (the challenge scores against both). Surface-pocket decoys need a geometric pocket
   detector or a documented substitute.
5. **Classical baselines** — GNM/ANM mode-based, perturbation-response scanning,
   random-walk / diffusion kernel, betweenness centrality. These are the "classical
   analogs" the challenge asks us to compare against, and the bar quantum must clear.
6. **Scoring harness** — enrichment statistics (AUC, precision@5, Mann-Whitney U vs.
   both negative sets, permutation null), one function called identically by every
   method.

**Exit:** for all three validation targets, a committed baseline experiment reporting
enrichment statistics for every classical method, reproducible from its config, with
a leakage test proving no holo-derived data reaches the prediction path.

---

## Phase 2 — Quantum propagation metric (statevector)

Hamiltonian constructions from the network; continuous-time quantum walk from the
active site; candidate metrics (time-averaged transfer probability, peak transfer,
integrated coherence, quantum Fisher information). Produce the N x N connectivity
matrix and top-5 hit lists. Ablate: which metric, which Hamiltonian, which active-site
definition.

**Exit:** at least one quantum metric beats the best classical baseline on the primary
criterion across targets, with the comparison run through the Phase 1 harness and the
mechanism (why interference helps here) argued, not just asserted.

---

## Phase 3 — Circuits, depth budget, noise resilience

Trotterised `exp(-iHt)` in the single-excitation sector; gate counts, depth, qubit
count and connectivity requirements reported per target (C3). Aer noise models sweeping
gate error and decoherence; stability of the *ranking*, not just the raw metric, since
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
additional ASD targets for generalisability; the methodological report tying the
quantum metric to the biology; final artifact pass for all four minimum targets.

**Exit:** all three required artifacts present for KRAS, BCR-ABL1, cardiac myosin and
c-Myc, plus the supporting-evidence set listed in `CHALLENGE.md` §8.
