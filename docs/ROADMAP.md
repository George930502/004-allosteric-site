# Roadmap

Each phase has an explicit **exit criterion** — a check that either passes or does not. No
phase is done on vibes. Update this file and the status table in `README.md` when a phase
closes.

**Current phase: 1 (Classical foundation).** Sub-phase 1.0, the frozen **input** layer, is
**closed**. Sub-phase 1.6, the frozen **evaluation** layer, is the next unit of work and is
what now blocks Phase 2.

---

## Phase 0 — Repository and agent harness ✅

Repo, packaging, verification gate, CI, agent contract, experiment ledger.

**Exit:** `make check` passes on a clean clone; CI green.

---

## Phase 1 — Classical foundation, ground truth, scoring harness

Nothing quantum yet. This phase builds the substrate everything else is measured against.
Getting the ground truth and the statistics right here is what makes every later number
believable.

### 1.0 — Frozen input layer ✅ closed 2026-08-24

Five scoreable arms across the three disease areas in `CHALLENGE.md` Table 1: the
**mandated** pair exactly as specified and a **corrected** pair for the same protein and the
same site, for each of KRAS G12C, BCR-ABL1 and cardiac myosin. Everything a method receives —
structure bytes, chain, node set, active-site rule — and everything it is scored against —
label set, scoreable label set, candidate set — is pinned before any method exists.

All three mandated pairs are defective, and each defect was re-derived from the deposited
coordinate files and cross-checked against live RCSB records:

- **KRAS `4OBE`→`6OIM`** — the apo is wild-type KRAS. Residue 12 is `GLY` in both chains and
  RCSB reports zero mutations, while the holo's sotorasib is covalently bonded to `CYS12` at
  1.805 Å. One residue of 21 labels. Usable, and repaired by `4LDJ`.
- **BCR-ABL1 `1OPL`→`5MO4`** — the apo is **holo at the site it is asked to predict**.
  Myristate contacts 16 of the 20 labels at 3.29 Å, and those 16 are a strict subset of the
  asciminib footprint. Fails clause (iii). Repaired by `2G2H`.
- **Cardiac myosin `5TBY`→`6C1H`** — unusable in both directions. `6C1H` is rat
  unconventional myosin-Ib with actin and calmodulin, and contains no mavacamten. `5TBY` is a
  SWISS-MODEL homology model on a tarantula template, deposited at 20 Å with zero heteroatoms,
  so it supplies neither measured contact topology nor a ligand from which a propagation
  source can be derived. Repaired by `9GZ3`/`9GZ2`, which is the cleanest pair in the
  benchmark: same construct, same state, differing by mavacamten and nothing else.

**Exit (MET):** `make verify` exits 0 — `allo benchmark verify` re-derives every frozen value
from the deposited files, and the network tests re-download all eight pinned wwPDB versioned
artifacts and confirm byte identity — and `make check` passes. `make check` is offline by
design, so it does not re-derive the freeze; `make verify` is the command that does.

See `docs/benchmark/README.md` and ADRs 0003–0011, 0014, 0016, 0017.

**What closed it was a reduction, not more work.** The freeze had eleven arms across three
proteins, a `sensitivity` tier, a second myosin site, an answer-informed apo quarantine, and
the whole evaluation protocol pinned in the same manifest. Five blockers stood between it and
its exit criterion, and four of them belonged to a layer that had not started. Separating the
layers and cutting the benchmark back to the three mandated disease areas removed all of them
except the decoys and the null, which moved to 1.6 where they belong. Recorded here because
the instinct to answer an audit finding by adding an arm is what produced the eleven.

### 1.1 Structure ingest — partly done

Fetch apo PDBs, select the chain, drop waters and ligands, index residues canonically by
author numbering, preserved end to end so hit lists are chemist-readable. Fetch, parse and
ligand-contact selection are implemented. The node set is the whole modelled chain
(ADR 0010).

### 1.2 Network construction

Cα (and optionally side-chain centroid) contact graph. Cutoff and weighting as configurable
knobs. Verify connectivity and degree distribution per target.

### 1.3 Ground truth ✅

Implemented in `src/allo/groundtruth/labels.py`: ligand-contact residues at 4.5 Å, transferred
to apo numbering by sequence alignment, unmapped labels reported rather than dropped. Import
isolation enforced by `tests/test_no_leakage.py`. Frozen per target.

### 1.4 Classical baselines

GNM/ANM mode-based, perturbation-response scanning, random-walk / diffusion kernel,
betweenness centrality. These are the classical analogs the challenge asks us to compare
against, and the bar quantum must clear. **APOP is the published bar** — GNM, unsupervised, no
MD, no training data, satisfying C1, C2 and C6 exactly.

A **distance-only** and a **degree-only** control belong here too, not as an afterthought.
On KRAS the label set is one hop from the propagation source, so a distance-only score is
close to unbeatable by construction. A method that does not beat those controls has
demonstrated nothing.

### 1.6 — Frozen evaluation layer 🔜 **next, and it blocks Phase 2**

Drafted in `docs/benchmark/evaluation-protocol.md`; nothing in it is pinned yet. Three things
have to land:

1. **The scoring harness**, implemented once and called identically by every method. AUC-PR
   as the tested endpoint with AUC-ROC beside it as the effect size, both estimators and tie
   rules pinned; precision@5 and P(≥1 hit) against the exact hypergeometric baseline.
2. **The decoy set.** `CHALLENGE.md` §4.1 requires enrichment against non-functional surface
   pockets as well as random background. This needs a geometric pocket detector, and its
   version and full configuration must be frozen before any method is scored — chosen after,
   it is a hyperparameter.
3. **The matched-patch null, calibrated** (ADR 0018). Both ends of the gate: a type-I rate on
   a stochastic site-uninformative score, and a positive control that must reject.

**Exit:** an evaluation manifest with its own freeze date, a committed calibration experiment
reproducible from its config, and the harness scoring a trivial baseline end to end on all
five arms.

### 1.7 — ASD selection set

A development set of ASD targets, built and frozen **before** Phase 2. Every hyperparameter —
metric, Hamiltonian, cutoff, coarse-graining ratio — is chosen there and nowhere else. Without
it, Phase 2's ablations are selected on the frozen primary benchmark, which is test-set
fitting even with no holo import (`docs/FIELD.md` trap 4).

The set must be disjoint from every primary target on accession, family, homologous site and
residue overlap (ADR 0012). That is not a formality: ASD curates the myristoyl pocket twice,
lists `1OPL` as a related complex, and holds an HRAS record carrying 4 of 5 KRAS labels past
any identity dedup.

**Exit:** a frozen selection set with a `selection.json` recording every candidate considered
and the clause that decided it, and no primary-benchmark number used to build it.

**Phase 2 entry gate: NOT MET.** Blocked on 1.6 and 1.7. ADR 0016 separately blocks the
mandated 5TBY deliverables until the organisers answer question (a).

---

## Phase 2 — Quantum propagation metric (statevector)

**Blocked:** do not begin method or hyperparameter selection until the Phase 2 entry gate is
met.

Hamiltonian constructions from the network; continuous-time quantum walk from the active
site; candidate metrics (time-averaged transfer probability, peak transfer, integrated
coherence, quantum Fisher information). Produce the N × N connectivity matrix and top-5 hit
lists. Ablate which metric, which Hamiltonian, which active-site definition — **on the Phase
1.7 selection set**. The frozen primary benchmark is scored once, with the choice already
fixed.

**Exit:** at least one quantum metric beats the best classical baseline on the primary
criterion across targets, with the comparison run through the Phase 1.6 harness and the
mechanism — why interference helps here — argued rather than asserted.

---

## Phase 3 — Circuits, depth budget, noise resilience

Trotterised `exp(-iHt)` in the single-excitation sector. Gate counts, depth, qubit count and
connectivity reported per target (C3). Aer noise models sweeping gate error and decoherence;
stability of the **ranking**, not just the raw metric, since the ranking is the deliverable.
Execute a coarse-grained instance on AWS Braket or via Classiq synthesis.

**Exit:** resource table per target, ranking-stability curves against noise strength, and at
least one real-hardware or hardware-emulated run.

---

## Phase 4 — Coarse-graining and scalability

Compress the network (spectral, community or domain-based) so targets exceeding qubit capacity
remain tractable, and **prove the compression retains the essential topological signal** — the
challenge asks for proof, not assertion: spectral distance between full and coarse
propagators, rank correlation of residue scores, recovery of the known pocket at each
compression ratio.

The myosin arm is where this bites first at 764 nodes. The interacting-heads question also
lands here: `9YRG`/`9YR7` is the super-relaxed pair, and whether the network should be one
head or the whole IHM is a coarse-graining decision rather than an input-layer one.

**Exit:** compression-ratio sweep showing where the signal breaks, plus a rule for picking the
ratio for an unseen protein.

---

## Phase 5 — Interpretability, delivery, extra targets

3D visualisation of connectivity maps on the structure. c-Myc (`1NKP`) prediction — its input
and evaluation contract must be frozen before method design, not after (ADR 0020). Further
**held-out** ASD targets for generalisability, distinct from the Phase 1.7 selection set,
which has already been tuned on and cannot demonstrate generalisation. The methodological
report tying the quantum metric to the biology. Final artifact pass for all four minimum
targets.

Robustness arms removed from the input layer on 2026-08-24 are re-addable from git history
here, one at a time, each against a specific claim: a third ABL1 apo (`2G1T`), a strict-C5
trimmed ABL1 node set, the bovine myosin pair (`8QYP`/`8QYR`, 1.80 Å), the omecamtiv arm, the
IHM pair, and the aficamten second site.

**Exit:** all three required artifacts present for KRAS, BCR-ABL1, cardiac myosin and c-Myc,
plus the supporting-evidence set listed in `CHALLENGE.md` §8.
