# Roadmap

Each phase has an explicit **exit criterion** — a check that either passes or does not. No
phase is done on vibes. Update this file and the status table in `README.md` when a phase
closes.

**Current phase: 1 (Classical foundation).** Sub-phase 1.0, the frozen **input** layer, and
sub-phase 1.6, the frozen **evaluation** layer, are both **closed**. 1.6 was closed on
2026-08-25, reopened the same day by its own audit
(`docs/benchmark/evaluation/AUDIT.md`), and closed again as **protocol version 2**.

Phase 2 is unblocked except for ADR 0016, which holds the mandated 5TBY deliverables until the
organisers answer question (a).

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

A **distance-only**, a **degree-only** and an **eigenvector-centrality** control belong here
too, not as an afterthought. On KRAS the scoreable label set starts 3.8 Å from the propagation
source, and a distance-only score still reaches only AUC 0.589 there and sits below chance on
three of five arms, so these are controls to beat rather than walkovers
(`docs/benchmark/README.md` §4). Eigenvector centrality is the control the published CTQW
result makes mandatory (ADR 0002). A method that does not beat those three controls has
demonstrated nothing.

### 1.6 — Frozen evaluation layer — CLOSED 2026-08-25 at protocol version 2

Frozen in `docs/benchmark/evaluation/`: `manifest.yaml` holds every pinned choice with its
reason, `frozen.json` holds the consequences for all 14 arms, and `README.md` is the argument.
`uv run allo evaluate verify` re-derives the freeze and exits 0 only if nothing moved.

**Delivered.**

1. **The scoring harness.** `allo.scoring.score_arm` is the one path; no method chooses an
   estimator, a tie rule, a null or a replicate count. The confirmatory endpoint changed from
   AUC-PR to the mean midrank (ADR 0022), which under a size-preserving null is a strictly
   increasing function of AUC-ROC. AUC-PR stays as a reported endpoint against its prevalence
   chance line. Every top-5 number prints against its exact hypergeometric baseline.
2. **The decoy set** (ADR 0024). pyKVFinder 0.9.3 at its published defaults, version and full
   configuration frozen before any method ran. The per-arm power floor is disclosed rather
   than discovered later: with three decoy pockets the smallest attainable p is 0.25, so the
   challenge's negative class (b) cannot reject at α = 0.05 on three of five primary arms.
3. **The matched-patch null, calibrated** (ADR 0023, which clears ADR 0018). The gate found
   what the draft did not anticipate. The matched null holds its size on KRAS, runs
   conservative on myosin and runs **anti-conservative on both BCR-ABL1 arms**, and a tighter
   tolerance makes that worse. The mechanism was measured: radius of gyration is only the
   second moment of the patch about its centroid, and the patch-mean variance is a functional
   of the whole within-patch distance distribution. **Four** repairs have now been tested and
   none closes it, and the fourth falsified that mechanism story (ADR 0025). The remedy is a
   per-arm calibration of the threshold, frozen before any method exists, one-sided so it can
   only tighten a test and never loosen one.

**Reopened 2026-08-25 by `docs/benchmark/evaluation/AUDIT.md`.** Eight audits ran against the
frozen layer. Two blockers:

- **The confirmatory procedure was not FWER-controlled.** The linear rescale
  `p × α / alpha_star` is size-exact at α and larger than nominal at Holm's tighter steps.
  Fixed by calibrating a `size_ratio` at every Holm level and rescaling on the probit scale
  (ADR 0025).
- **A trivial geometric baseline cleared the whole confirmatory family.** Rank each residue
  by the volume of the largest cavity that lines it — label-blind, apo-only, zero-parameter —
  and it rejects on all three confirmatory arms. Clearing the null is therefore a low bar.
  `cavity_volume` is now a required baseline, and the report's claim threshold is **beating
  it**, not rejecting the null (ADR 0025).

Also repaired: the patch cache key, a leakage route through `harness._positives`, the
unenforced detector version and `--detect` gate, seven wrong numbers and fourteen citations.
2 075 lines deleted. `docs/benchmark/evaluation/AUDIT.md` is the record.

**Two endpoints were added before closing, not deferred.** The audit first pushed
residue-centroid DCC and the four confounder columns to Phase 3. That was wrong for DCC: it is
a function of the top-5 list, the labels and coordinates, so it needed no method, and deferring
it would have meant adding an endpoint after methods were scored — the exact move the manifest
forbids. It paid for itself on first use. On `bcr_abl1_corrected` the cavity-volume baseline
rejects at `p_calibrated` 0.0003 while its predicted centre sits **farther from the site than a
random five-residue list** (DCC 26.5 Å against a chance line of 17.7 Å). Three of the four
confounder columns are now computed too; conservation needs an external alignment and reads
`null` (ADR 0025 amendment).

**Exit met.** `make check` and `make verify` both exit 0 at protocol version 2 —
the latter re-derives both freezes, re-runs the pocket detector and runs the network tests. The
calibration experiment is reproducible from its committed config on all 14 arms, and the
`null-repairs` experiment likewise. Both required controls run end to end on all five primary
arms: `distance_from_source_negated` rejects nothing, and `cavity_volume` rejects on all three
confirmatory arms with its recall@5 and DCC recorded rather than hidden.

**Two things the report must say before its numbers, not after them.** The distance-only
baseline is below chance on three of five arms, so its inversion is the strong control there.
And a geometric pocket detector misses the site entirely on 3 of 14 arms — the challenge's own
premise, quantified on our benchmark before any method existed.

### 1.7 — Secondary benchmark — CLOSED 2026-08-24

A second frozen input layer, built and frozen **before** Phase 2, in two disjoint tiers
(ADR 0021). `development` carries every hyperparameter — metric, Hamiltonian, cutoff,
coarse-graining ratio — and `generalisation` carries the Phase 5 claim and is not looked at
until the method is frozen. Without the first tier, Phase 2's ablations are selected on the
frozen primary benchmark, which is test-set fitting even with no holo import
(`docs/FIELD.md` trap 4). Without the second, there is no set that can demonstrate
generalisation, because the tuning set is burned by construction (ADR 0012).

The frame is RCSB rather than the Allosteric Database. No database certifies allostery per
record, per site, per structure; ASD is unreachable and unlicensed; AHoJ-DB's apo call
returns the pair this repo's own audit rejected. Evidence: `docs/benchmark/secondary/evidence/databases.md`.

**Delivered.** 9 targets from 97 candidates, 147–1058 modelled residues, 133 scoreable
labels. Four extra admission clauses beyond the eight — single-chain lining, apo occupant
classification, structure admission, within-set Pfam redundancy — each with a test.
Tier split is seeded and size-stratified, and `allo.benchmark.size_stratified_split`
reproduces it. `docs/benchmark/secondary/README.md` reports what the achieved N supports
and, in §7, the eleven limitations a reviewer would otherwise find.

**Exit met:** `allo benchmark verify --set all` is clean, `selection.json` records all 97
candidates, 73 of them with the clause that decided each, and no primary-benchmark number
was used to build it.

**The 24 `pending` rows were screened on 2026-08-24**, together with a wider sweep of two
independent frames, and the freeze was left unchanged. Five further arms are admissible, which
takes N from 9 to 14 and the `generalisation` tier from 5 to about 7 or 8 — the minimum
attainable one-sided p moves from 0.031 to 0.0078 or 0.0039. Adding them re-runs the seeded
split and so changes every existing tier assignment, which is a re-freeze rather than a repair.
The screening record is `docs/benchmark/secondary/evidence/extension-candidates.md`. It is an
answer key and `tests/test_no_leakage.py` guards it.

**What the sweep settled.** Clause (ix), single-chain lining, is the binding supply constraint
at a 72 % kill rate on physiological-effector holo entries, not clause (xii) at 12-14 %. The
design target of 28 is not reachable from this frame. No new admissible target is below 272
residues, because small catalytic domains are overwhelmingly obligate oligomers and so fail
clause (ix) before size is the question. **The decision to re-freeze is open and belongs to
Phase 5, not to Phase 1.**

**Phase 2 entry gate: met on 2026-08-25**, withdrawn the same day when the audit reopened
sub-phase 1.6, and met again once 1.6 closed at protocol version 2.

**Two per-target blockers remain, and neither is cleared by 1.6.**

- **ADR 0016** holds the mandated 5TBY deliverables until the organisers answer question (a).
- **ADR 0020** holds the c-Myc (`1NKP`) deliverables. Its contract is still unmet: no chain or
  copy is chosen, no propagation source or explicitly source-free metric contract is frozen,
  and no answer-independent consensus or docking evaluation exists. `1NKP` is one of the four
  minimum deliverables in `CHALLENGE.md`, and it has **no arm in the evaluation freeze**. The
  version-2 audit found this recorded nowhere on this page (`AUDIT.md` M15) and it is recorded
  here now. Phase 2 may proceed on the other three targets; it may not produce c-Myc artifacts
  until an ADR supersedes 0020.

---

## Phase 2 — Quantum propagation metric (statevector)

**Open.** Every hyperparameter is chosen on the secondary set's `development` tier, and every
number is produced by `allo.scoring.score_arm` and no other path.

Hamiltonian constructions from the network; continuous-time quantum walk from the active
site; candidate metrics (time-averaged transfer probability, peak transfer, integrated
coherence, quantum Fisher information). Produce the N × N connectivity matrix and top-5 hit
lists. Ablate which metric, which Hamiltonian, which active-site definition — **on the secondary
set's `development` tier and nowhere else**. The frozen primary benchmark is scored once,
with the choice already fixed, and the `generalisation` tier is not opened until Phase 5.

**The quantum bar is published, and it is not friendly.** Mohtashim 2026, _JACS_,
doi:10.1021/jacs.6c08053, ran CTQW centrality on protein residue-interaction networks on IBM
hardware over 150 proteins and found "consistently strong agreement with classical eigenvector
centrality". Our differences from that work — active-site conditioning, apo/holo scoring, and
the perturbation metric — are what Phase 2 has to demonstrate, not assume (ADR 0002).
**Eigenvector centrality is therefore a mandatory baseline in 1.4**, beside GNM/APOP,
distance-only and degree-only.

**Exit:** at least one quantum metric beats the best classical baseline on the primary
criterion across targets, with the comparison run through the Phase 1.6 harness and the
mechanism — why interference helps here — argued rather than asserted. A metric that ties with
eigenvector centrality has reproduced Mohtashim 2026 and has not cleared the bar.

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
and evaluation contract must be frozen before method design, not after (ADR 0020). The generalisability and
scalability numbers come from the secondary set's `generalisation` tier (N = 5, frozen
2026-08-24) and from nowhere else. It is opened here for the first time; the `development`
tier has already been tuned on and cannot demonstrate generalisation. The methodological
report tying the quantum metric to the biology. Final artifact pass for all four minimum
targets.

Robustness arms removed from the input layer on 2026-08-24 are re-addable from git history
here, one at a time, each against a specific claim: a third ABL1 apo (`2G1T`), a strict-C5
trimmed ABL1 node set, the bovine myosin pair (`8QYP`/`8QYR`, 1.80 Å), the omecamtiv arm, the
IHM pair, and the aficamten second site.

**Exit:** all three required artifacts present for KRAS, BCR-ABL1, cardiac myosin and c-Myc,
plus the supporting-evidence set listed in `CHALLENGE.md` §8.
