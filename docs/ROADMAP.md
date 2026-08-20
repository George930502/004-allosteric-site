# Roadmap

Each phase has an explicit **exit criterion** — a check that either passes or does
not. No phase is "done" on vibes. Update the status table in `README.md` and this
file when a phase closes.

**Current phase: 1 (Classical foundation).** Sub-phase 1.0 is frozen and every ADR it
depends on is accepted (0006, 0013, 0014, 0015 decided 2026-08-20). Phase **1.8** — apo-only
re-selection of the `8QYP` arms — is booked and is the one thing standing between the
myosin arms and confirmatory status.

---

## Phase 0 — Repository and agent harness ✅

Repo, packaging, verification gate, CI, agent contract, experiment ledger.

**Exit:** `make check` passes on a clean clone; CI green.

---

## Phase 1 — Classical foundation, ground truth, scoring harness

Nothing quantum yet. This phase builds the substrate everything else is measured
against. Getting the ground truth and the statistics right here is what makes every
later number believable.

0. **Frozen benchmark — input layer and positives closed 2026-08-20; negatives still open**
   — the input layer is fixed before any method exists, so method comparisons are honest. An audit of the challenge's own
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
   (labels minus propagation-source residues, this repo's anti-circularity policy, with
   AlloPred only a methodological analogy) with no distance threshold;
   every target now carries `allosteric_evidence`, `state` and `blind` fields enforced by
   `tests/test_benchmark.py`; and myosin gained a second **target** (Site 2, aficamten) plus
   a Site 1 sensitivity arm, 11 targets at that freeze. Round 3 later added the trimmed ABL1
   sensitivity arm. **No** arm in the primary benchmark is blind (corrected 2026-08-20; myosin Site 1 was
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
   ASD set and not the hand-specified primary arms) and **ADR 0010, accepted** (the node set is
   the modelled chain, not a trimmed catalytic domain; the strict C5 reading would have shrunk
   the mandated ABL1 arm by ~40 % and deleted the SH3–SH2 clamp the myristoyl pocket acts
   through, and is declined — now guarded by a test tying `apo_input` to `n_residues`). One
   real C1 leak *surface* was closed: `manifest.yaml` carries label residue numbers in prose,
   so `allo.inputs.load()` now redacts the holo half by allow-list and two new tests hold it
   there.

   **Codex adversarial review 2026-08-20 (`gpt-5.6-sol`, xhigh).** An independent model was
   pointed at the whole branch precisely because everything above was produced in one
   self-consistent session. Nine findings, eight of which held; the four that mattered were
   ones no amount of re-reading by the same author would have surfaced, because each is a
   contradiction between two paragraphs that were individually right.
   - **ADR 0011 — the scoring universe.** Propagation-source residues had been removed from
     the positives and left in the negatives. That is a **44–62 % AUC-PR penalty aimed at
     connectivity methods and at nothing else** — i.e. at the method class the challenge asks
     for. They now leave both classes, along with sibling functional sites on the same apo
     chain. Every chance line in §5 moved.
   - **The C1 hole next to the one we closed.** `allo.inputs.read_manifest` returned the
     manifest verbatim from a *prediction-path* module, and no guard saw it — the import trace
     watches `allo.groundtruth`, the file-read test greps for `manifest.yaml`. Moved to
     `allo.groundtruth.manifest`, so the existing guard covers it.
   - **ADR 0012 — the tuning set contained the answers.** §5 sent hyperparameter selection to
     ASD; §7 records that ASD curates the myristoyl pocket twice, lists `1OPL` as a related
     complex, and holds an HRAS record carrying 4 of 5 KRAS labels past any identity dedup.
     Selection now requires disjointness on accession, family, homologous site and residue
     overlap.
   - **The null promised distance matching it did not do**, which is anti-conservative on
     exactly our proximal arms. §5 now matches on distance-to-source and requires a
     distance-only and degree-only calibration to fail before any p-value is quotable.
   Also: clause (iii)'s text now matches what `derive()` checks; §5 declares one confirmatory
   decision rule instead of two primary metrics and a Holm sentence; `apo_input` fails closed
   on the apo file's sha256; and the header no longer claims "identical negatives", because
   the decoy detector does not exist yet and choosing it later would make it a hyperparameter.

   **Codex adversarial review round 2 (`gpt-5.6-sol`, xhigh).** The same model re-checked its
   own nine findings rather than trusting the commit that claimed to close them, and audited
   the files round 1 never opened. It accepted the candidate-denominator arithmetic, the
   clause (iii) wording and the parser/label outputs; eight findings stood, three of them
   defects the *repair* introduced.
   - **The sibling mask keyed on free text.** `_exclude_sibling_sites` compared the display
     string `site`, and Site 1's two arms read "mavacamten site" and "mavacamten/omecamtiv
     pocket (Site 1)" — so the two halves of one pocket masked each other and both candidate
     counts were wrong (47/44 excluded, should be 42/42). Now keyed on a canonical `site_id`,
     with a test for the converse case that broke.
   - **The hash check was caller-bypassable.** `apo_input(target, manifest=...)` verified
     caller-supplied bytes against caller-supplied metadata: hand it a manifest mapping
     `kras_g12c_mandated` to `4LDJ` and it returned `4LDJ`, every guard green. The parameter is
     gone; the manifest is always the repository-pinned one.
   - **The confirmatory family was hand-counted as three** — counting proteins, when a target
     is a protein *plus a site* (ADR 0008). Four corrected arms exist, so Site 2 was being
     dropped or the FWER under-corrected. The family is derived by `allo benchmark stats` now.
   - **Run scripts kept a route to the answer key.** The `experiments/` guard grepped for
     `frozen.json`/`groundtruth`; `from allo import benchmark` then `benchmark.load()` contains
     neither string and is outside the import graph. The AST guard now walks `experiments/` and
     `scripts/` and rejects `allo.benchmark` as well as `allo.groundtruth`.
   - **A promise written in the present tense.** §7 said a trimmed-domain ABL1 arm "is run".
     It does not exist, and the kinase-only arms are different structures, so they cannot
     isolate trimming. Corrected to what is true, with the arm specified (`bcr_abl1_trimmed`,
     same `1OPL`:A, explicit `residue_range`, boundary from a version-pinned UniProt/Pfam
     assignment) and marked blocking.
   Also: the null now matches the **scoreable** set (matching the full set is impossible — it
   contains 0 Å source residues absent from the candidate set) and freezes its knobs in the
   manifest with a stated [0.02, 0.08] type-I acceptance band; ADR 0012 gained operational
   metrics and a required `selection.json` artifact instead of four unenforceable sentences;
   and the manifest move had broken the audit reproduction script in
   `evidence/allosteric-pair-audit.md`, which also still carried pre-ADR-0008 arm IDs — repaired,
   with the index claim corrected from "every frozen arm" to "eight of the ten".

   **Codex adversarial review round 3 repair 2026-08-20.** The ten reported findings were
   rechecked against executable regressions. The prediction boundary now supplies an
   immutable, ligand-free, single-chain structure with exactly the frozen nodes; the
   UniProtKB 2026_02-backed `bcr_abl1_trimmed` arm freezes the same 1OPL coordinates over
   deposited residues 261–512; catalytic-state matching uses contacting manifest vocabulary
   components and records additives separately; null and multiplicity choices are
   schema-guarded; real shell/Make/notebook runners are covered by the C1 gate; and the
   structural audit was rerun over `sorted(frozen)`. The prior round's claimed manifest null
   did not in fact exist, and its ad hoc type-I band is replaced by the exact binomial
   prediction interval.

   A fourth round then closed the policy questions and four defects the third round's repair
   had introduced or left. `load()` was a deny-list with no top-level filter at all, so the
   whole null model and the orthosteric vocabulary reached prediction code; it is now built
   from two allow-lists. Prediction-side arrays cleared the WRITEABLE flag, which NumPy lets
   the owner set back — they are `bytes`-backed and un-unfreezable now. The runner gate could
   not see a wrapped import. The cut-label test passed on a freeze with every cut erased, and
   is replaced by an accounting identity across arms sharing a pocket. Decisions taken:
   **ADR 0006 accepted** (a reversible node-set policy is not a frozen input layer);
   **ADR 0013 accepted, option 2** — the three `8QYP` arms are quarantined from claims, so the
   claim-bearing family is three, one arm per protein; **ADR 0014 corrected and accepted,
   option 1** — all 15 pinned mmCIF are byte-identical to their wwPDB versioned artifacts;
   exact URLs and version labels are in the manifest, while all 17 entries remain as a
   5.21 MiB offline mirror partitioned under `structures/apo` and `structures/holo`. The
   earlier rejection tested the wrong hosts. **ADR 0015 amended** — explicit per-protein
   functional-site registries, carried across entries by alignment, define exclusions;
   adding an arm cannot move another arm's universe.

   **Still open before any method may be scored:** decoy artifacts committed, the patch null
   calibrated, ADR 0012's `selection.json` built, two questions put to the organisers
   (`6C1H`, and how C5 is to be read), and Phase 1.8's apo-only re-selection.

1. **Structure ingest** — fetch apo PDBs, select catalytic domain / chain, drop
   waters, co-factors and PTMs (C5), index residues canonically (auth numbering,
   preserved end to end so hit lists are chemist-readable). _Partly done: fetch/parse and
   ligand-contact selection and explicit authority-backed residue ranges are implemented;
   the default remains the whole modelled chain under ADR 0010._
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

8. **Apo-only re-selection of the `8QYP` arms (ADR 0013, option 1).** `8QYP` was chosen by
   comparing apo candidates against holo-defined pocket geometry, so the three arms built on
   it are answer-informed in the anti-conservative direction and are quarantined from every
   claim until this lands. Enumerate MYH7 apo candidates and rank them on **apo-only**
   criteria pinned before any holo is opened — construct compatibility, method, resolution,
   model completeness, apo catalytic-state annotation — with the site-apo occupancy check
   applied as pass/fail admission and never as a closeness objective. Re-freeze every arm
   whose apo changes. If no candidate passes, the quarantine stands rather than relaxes.

   **Exit:** `claim_bearing_family()` returns four arms again, and `selection.json`-style
   provenance records every candidate considered with the clause that decided it.

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
