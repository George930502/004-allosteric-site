# Roadmap

> **THE METHOD LAYER LEFT `main` ON 2026-09-02 (ADR 0037).** `main` now holds the frozen
> benchmark, the frozen evaluation protocol, the evidence behind both, and the nine controls
> the protocol requires. It holds no candidate method. Everything removed is on the branch
> `method-layer-archive`, which is the only copy and is never deleted. **Phase 2 sections
> below describe work that no longer exists on this branch.** They are kept as the record of
> what was tried and what it measured. Challenge deliverable 1, the N x N connectivity
> matrix, returns to **not built**; `docs/report/conformance.md` records that regression.

Each phase has an explicit **exit criterion** — a check that either passes or does not. No
phase is done on vibes. Update this file and the status table in `README.md` when a phase
closes.

**Current phase: 1 (Classical foundation).** Sub-phase 1.0, the frozen **input** layer, and
sub-phase 1.6, the frozen **evaluation** layer, are both **closed**. 1.6 was closed on
2026-08-25, reopened the same day by its own audit
(`docs/benchmark/evaluation/AUDIT.md`), and closed again as **protocol version 2**. It is at
**protocol version 4** today.

> **A FOURTH PASS RAN ON 2026-09-03 and opened protocol version 4.** Read
> [`docs/benchmark/review/27-fourth-pass-synthesis.md`](benchmark/review/27-fourth-pass-synthesis.md).
> It is the current ranked list and it supersedes `26`.
>
> Three findings would have invalidated a result. The claim family counted a rejection in the
> wrong direction, so a method significantly **worse** than `cavity_volume` cleared the family
> that licenses "the method beats the reference". The C1 package scans globbed `src/allo`
> while the runner scan exempted the whole of `src/`, so a second package at `src/predict/`
> was read by neither and recovered the positive count for all fifteen arms with the suite
> green. And negative class (b) did not measure the deliverable: a shift of four standard
> deviations on every label residue gives power **0** on KRAS and on cardiac myosin, because
> the statistic ranks the detector's pocket lining and the myosin labels sit inside a
> 295-residue lining, a small fraction of it. ADR 0039 adds the label-set form beside it, with power 0.875 and 1.000
> where the shipped form has none.
>
> **ADR 0039 was amended the same day, against its own first measurement.** It claimed the
> label form is "conservative, never anti-conservative" from one null family. Measured over
> four generators in `experiments/2026-09-03-endpoint-b/`, its size reaches **0.0548** with a
> 95 % interval of [0.0516, 0.0580], entirely above alpha, under a blocky distance-monotone
> field -- the shape every distance-correlated baseline here has. So it ships as a
> **descriptive percentile and not a p-value**, and the shipped `p` holds on all four.
>
> **"Clearing a family" had no definition**, and the frozen layer held both readings in
> documents that cite each other. ADR 0038 freezes the disjunction, in code. Under it,
> `cavity_volume` **clears** family 1 on one arm of three. The line below and
> `evaluation/README.md` §13 record that same measurement as a failure, which was the wording
> and not the arithmetic.
>
> The data-route list held eleven routes and two payload notes and called itself thirteen.
> Two real routes were added on 2026-09-03 — `docs/adr/`, and a protected file's former name
> after a rename — so the count is **fourteen**. The path resolver was replaced as the primary
> defence by a segment-cover backstop, because a whitelist of spellings had lost four times.
>
> **A third and a fourth adversarial round followed, and the input layer was re-frozen
> once.** Round 3 found that the size run measured three null laws while reporting four:
> `smooth_t` divided a Gaussian field by one chi-square per replicate, which is monotone
> within the column, so its ranks equalled `smooth_gaussian`'s. **A rank test cannot see a
> marginal distribution**, so only the copula matters. The run was repeated with a
> different copula and every conclusion survived. It also found a public bypass of the
> sealed tier, a mutable `decision.alpha`, and a former-path ledger already stale because a
> JSON-to-Markdown conversion is a delete and not a rename. All repaired: ADR 0043.
>
> **ADR 0044 re-froze the INPUT layer, and no number moved.** A scoped literature review
> found no published three-class occupant scheme, and found that every roster naming
> glycerol or sulfate puts them on the additive side. Both were recorded here as
> catalytic-state components. The larger finding is that the annotation was never the
> gate: clauses (iii) and (x) count every non-water heteroatom through a name-blind mask,
> stricter than any roster. Twenty-one leaves moved across both freezes, **all inside the
> annotation and none outside it**. The same review found the `ptp1b` WPD-loop strings
> backwards, confirmed by measurement: apo 6.52 angstrom against its own holo at 12.62.
>
> **Round 4 returned four findings, and three are defects in round 3's own repairs.** The
> replacement generator was scored with **ordinal ranks**, not midranks, and it is the only
> one of the four that ties anything: it is piecewise constant, a column of 80 residues holds
> a median of 3 distinct values, and every tie was broken by residue index, which runs along
> the chain. Repeated at the same seed, only that row moved and the other three are
> bit-identical. **Conformance was a deny-list** binding 6 of 74 manifest leaves; inverted to
> an allow-list plus a digest, it now binds 55 and the 19 survivors are exactly the declared
> prose set. **`docs/evidence/method-landscape/` reproduces positive counts** and was
> unprotected, so the count of data routes is **fourteen**; a standing sweep now fails on any
> unprotected file that puts an arm, its count and a cue word in one window. And **pinning a
> release did not make the values that release**: the recorded Pfam lists were RCSB
> per-entity assignments, a strict subset of the accession sets clause (xii) resolves on.
> Both manifests carry the accession-derived sets now and **the verdict holds at that full
> width**. No frozen value moved.

> **A second audit pass ran on 2026-09-02, audited the first one, and its findings were
> repaired the same day. Read
> [`docs/benchmark/review/25-second-pass-synthesis.md`](benchmark/review/25-second-pass-synthesis.md)
> for the evidence behind each item.** `make check` and `uv run allo evaluate verify --detect`
> both exit 0 after the repairs.
>
> **Closed — three new C1 leaks.** A sweep of every tracked `.md`, `.yaml`, `.json` and `.txt`
> outside the seven protected trees, looking for a run of label residues inside one
> 400-character window, found three files that cleared the coincidence floor.
> `docs/benchmark/primary/audit/` reproduces the complete KRAS label set and the complete
> BCR-ABL1 one; `docs/benchmark/evidence/` prints the KRAS distal label set as prose;
> `experiments/` persists the true site's radius of gyration for the six primary arms and all
> five sealed `generalisation` arms. All three are now guarded, taking the count of data
> routes from seven to ten. A `src.`-prefixed import that walked past every C1 import guard is
> closed in the same commit.
>
> **Withdrawn on the same day by the third pass — `docs/targets.md` IS a leak, and the
> refutation was a detector failure.** This box said it holds none of the cardiac myosin
> label residues. It holds the complete set, written in three-letter codes. The
> sweep matched bare integers on a word boundary, so a three-letter code never matched its
> own number. Re-run with the codes normalised, `docs/targets.md` holds the **complete** label
> set for both myosin arms and is the only new complete-set file in the tree. Two more routes came with
> it — both benchmark READMEs publish the positive count, the holo entry and the effector
> for every arm including the five sealed ones — and the count is now **thirteen**. See
> [`docs/benchmark/review/26-third-pass-synthesis.md`](benchmark/review/26-third-pass-synthesis.md).
>
> **Closed — the decoy-pocket p-value.** It compared the whole label set's mean midrank against
> the decoy pocket linings'. ADR 0030 writes the test on the **site pocket's** lining, and the
> type-I simulation behind it drew the site's number from the same unit-variance law as the
> decoys'. The code now matches both, and a test pins the identity
> `p = site_pocket_rank / (1 + n_decoys)`.
>
> **Closed — three stale or false statements in the frozen documents.** `cavity_volume` was
> re-measured under protocol version 3 at `p_calibrated` 0.0046 / 0.0715 / 0.3236, and Holm
> rejects **one arm of three**, not three of three. This paragraph read that as "no longer
> clears the confirmatory family" until 2026-09-03, when ADR 0038 froze the disjunction: one
> arm of three **is** clearing. The measurement stands; the reading of it was the error. The claim that the detector re-freeze selected on a label-free criterion was false —
> `n_decoys` depends on the labels — and the criterion of record is now `n_detected`, which
> picks the identical setting on all five arms with no tie, so no frozen value moved. Three
> counts were wrong: 36 ADRs not 33, fifteen arms not sixteen, ten data routes not seven.
>
> **Closed — two correctness defects outside the protocol.** The infinite-time connectivity
> matrix summed over eigenvectors rather than spectral projectors, so on a degenerate spectrum
> its value depended on an arbitrary LAPACK basis choice. The reported top-5 hit list broke
> ties using the answer key, which made the deliverable itself a function of the labels.
>
> **Corrected, not closed — the Faccin diagnosis under Phase 2 below.** It applies the theorem
> to the adjacency matrix, a site-basis state and the top eigengap. The paper is about
> `D^(-1/2) L D^(-1/2)`, its degree-weighted ground state, and the smallest non-zero
> eigenvalue. Measured on KRAS: `(H_Q)_ii = 1.0` at every node, `Δ = 0.056` against the code's
> 1.438, and a site-basis source sits at quantumness 0.994 rather than at the classical point.
> The module now says so and the two levers are demoted to measured heuristics. **The
> empirical sweep result stands; its explanation does not, and nothing below this box has been
> rewritten for it.**
>
> **A third pass audited those repairs on the same day, because nobody had.**
> [`26-third-pass-synthesis.md`](benchmark/review/26-third-pass-synthesis.md) is its ranked
> list. Four things it closed, beyond the withdrawal above:
>
> - **The path guard could be walked past with `.joinpath`.** A module in `allo.network`
>   recovered every arm's positive count from the protected matched-patch cache and all 34
>   leakage tests passed. `os.path.dirname` had the same hole. Both are closed and probed.
>   Third instance of one failure mode: the guard reads the text correctly and the
>   interpreter accepts a form the text does not model.
> - **The frozen decision rule had no implementation.** `decision.alpha`,
>   `decision.confirmatory_family` and `decision.correction` had no reader in `src/` or
>   `experiments/`, and `holm` had no caller outside the tests. The only Holm actually run
>   corrects over a different family. `allo.scoring.confirmatory_verdict` now reads the
>   frozen block and refuses a family that is not the declared one.
> - **The matched-patch cache key was blind to the contact cutoff**, under a comment saying
>   it was not. Identical digest at 4.5, 6.0 and 8.0 Å while the mean degree ran 9.531,
>   13.398, 24.262. Fixed; every pool was re-drawn and the freeze re-verifies unchanged.
> - **Five documents stated a refuted or stale fact**, including ADR 0030's decision 5 and
>   `scoring/decoys.py`, which still said `cavity_volume` clears the confirmatory family.
> - **It measured what protocol version 3 moved in the committed sweeps**, rather than
>   asserting it. Every record in the three 2026-08-26 experiments carries
>   `protocol_frozen_on: 2026-08-25`. Re-scoring 216 of them through the current harness moves
>   every decoy column and `auc_roc_vs_decoy_linings`, moves `dcc_angstrom` on 6 of 216, and
>   moves `auc_roc`, `mean_rank`, `auc_pr`, `precision_at_5`, `hits_at_5`, `recall_at_5` and
>   the matched-patch p-value on **none**. The screening statistic is unmoved, so the variant
>   selection stands and no re-run was needed. The three `notes.md` say so. The same
>   measurement found **15 of the 69 registered scorers have never been screened**.
>
> **Twenty-one items are open** and §5 of that document ranks them, each naming the ADR it
> needs. The largest are the undisclosed myosin B-factor defects, a claim-family arm scored
> against a truncated label set, and C3 — 14 of 25 quantum scorers have no resource account.
>
> **Open — one item, and it is the user's call.** The whole frozen state is uncommitted. A
> clean clone cannot reproduce what these documents call frozen.

**The organisers answered four questions on 2026-09-02, and a multi-axis audit of all three
frozen sets closed the same day. `docs/benchmark/review/` is the record; `11-synthesis.md` is
the ranked list.** Five items blocked scoring on the primary arms. **All five are now decided,
by ADRs 0029 to 0036, and the primary input layer is re-frozen at six arms.** What each one
was, and what settled it:

1. **The BCR-ABL1 chain — settled by ADR 0029: report chain B, non-confirmatory.** The organisers direct teams to `1OPL` chain **B**; the frozen arm
   uses chain A. Measured: chain B empties the myristoyl pocket and deletes the mechanism —
   no SH3 modelled, SH2 docked on the N-lobe instead of the C-lobe, 22.89 A from the holo,
   and coordinates the depositors state were rigid-body placed with three group B-factors.
   An exhaustive PDB survey finds **no myristate-free assembled ABL1 exists**: the clamp
   docks only when the pocket is filled, five entries for five.
2. **Negative class (b) has no valid per-arm test — settled by ADR 0030: keep the pocket-rank
   test descriptive, add a Fisher combination across the confirmatory family, re-freeze the
   detector on `n_detected` alone. This opens protocol version 3.** Three constructions measured against the
   ADR 0018 gate: the frozen pocket permutation needs an effect of 2.49 SD at any decoy
   count; a residue-level test has a measured size of 0.13-0.38; a size-matched patch cannot
   be drawn, because on both KRAS arms no decoy pocket is as large as the label set. A Fisher
   or Stouffer combination across arms reaches a floor of 0.021 and is the available answer.
3. **ADR 0016 is superseded by the organisers' answer — done, by ADR 0031. The arm is exposed,
   non-confirmatory, with both defects printed.** `9GZ2` is sanctioned, and all twelve
   labels transfer onto `5TBY`. Both input blockers stand and are now measured: no unique
   fold-general source rule, and a `5TBY` long-range contact graph agreeing with the measured
   structure at Jaccard **0.471**.
4. **The claim threshold and the confirmatory family disagree** (ADR 0025 against
   `evaluation/README.md` §8) — **settled by ADR 0032: the claim threshold becomes its own
   confirmatory family, a paired `compare_methods` against `cavity_volume` on the same three
   arms, Holm over three, two-sided.**
5. **Seven of fourteen arms locate the active site from a ligand the input strips.** The
   organisers' "uniformly stripped" instruction does not say whether that is permitted.
   **Settled by ADR 0033: the narrow reading — stripping scopes the node set, and the source
   rule is reported rather than re-frozen.** A measurement changed the design: the P-loop motif
   span was believed to sit inside the frozen ligand source, and it does not. Residue 10 is a
   **scoreable label**, so a motif source would move it out of the positive class, 16 to 15.
   No new frozen arm; a descriptive matched comparison on the 15-residue intersection instead.

**Three more ADRs came out of the same audit.** 0034 protects `docs/benchmark/review/` as an
answer key and exempts its own tools by an import-based rule. 0035 fixes conservation as the
fourth confounder column and rejects coevolution as a category error. 0036 makes c-Myc a
reported deliverable scored against NMR segments, superseding ADR 0020.

**The one open C1 hole is closed.** `docs/benchmark/review/` carries per-arm positive counts
and five real KRAS label residues, and it was not in `PROTECTED_PATHS`. C1 names the residue
count directly. The naive fix fails, because `data/fetch_structure_evidence.py` writes into the
protected tree and the runner gate then flags the script's own output. **ADR 0034 exempts the
tree's own tools by a rule instead of a name list**: a file is a review tool when it is tracked
inside the tree **and** imports nothing from `allo`. The leakage suite passes with the tree
protected, and two new tests pin the rule. It is the **seventh** guarded data route.

**One number the report has to carry: geometry alone is a strong baseline.** Both distance
directions are declared baselines. Taking the better one per arm gives a median AUC of
**0.666** over fourteen arms, 0.932 on `hiv_rt` and 0.804 on `ecoli_cps`. No other apo-only
descriptor separates the labels benchmark-wide — burial, B-factor, hydrophobicity, degree
and composition all sit at chance when pooled, which is a design strength worth stating.
Measured in `docs/benchmark/review/12-dataset-eda.md`.

**One correction that changes a recorded justification: ASD is reachable.** Twelve release
archives downloaded over plain HTTP on 2026-09-02. The 2026-08-24 conclusion was a method
failure, not a fact about the server. It supplies 34 new leads, 13 of them with physiological
effectors — the gap the secondary set names — and **zero** new admissible arms, because none
has been through clause (ii). The re-freeze decision stays in Phase 5.

**Phase 2 is open and starts from an empty method package.** On 2026-09-02 the method
layer was removed from `main` and preserved on the branch `method-layer-archive` (ADR 0037):
`src/allo/{network,classical,quantum}`, `tests/test_method.py`, `docs/method/exploration/`,
and the nine experiment directories dated 2026-08-26 and 2026-08-27. Nothing below this
paragraph that cites one of those paths is runnable on `main`. Two things moved rather than
left, because the frozen evaluation protocol requires them: the graph builder is now
`allo.structure.graph`, and the eight required baselines are now `allo.scoring.baselines`,
verified against the archived sweep at 32 scorer-arm pairs and 0 mismatches.

**Both per-target blockers are cleared, and both layers are frozen again.**
ADR 0031 supersedes 0016 and ADR 0036 supersedes 0020, so **all four minimum targets now have a
contract**. The conformance gap the audit called largest is closed. The input layer is
re-frozen at **six** primary arms and the evaluation layer at **protocol version 3**, over
fifteen arms — version 4 followed on 2026-09-03, and section 0a of
`docs/benchmark/evaluation/README.md` lists what it changed; `uv run allo benchmark verify --set all` and `uv run allo evaluate verify
--detect` both exit 0. The recalibration reproduced thirteen of fifteen arms' thresholds to six
decimals and moved only the two arms the re-freeze changed.

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

See `docs/benchmark/primary/README.md` and ADRs 0003–0011, 0014, 0016, 0017.

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
(`docs/benchmark/primary/README.md` §4). Eigenvector centrality is the control the published CTQW
result makes mandatory (ADR 0002). A method that does not beat those three controls has
demonstrated nothing.

### 1.6 — Frozen evaluation layer — CLOSED 2026-08-25 at protocol version 2, re-frozen 2026-09-02 at version 3 and 2026-09-03 at version 4

Frozen in `docs/benchmark/evaluation/`: `manifest.yaml` holds every pinned choice with its
reason, `frozen.json` holds the consequences for all 15 arms, and `README.md` is the argument.
`uv run allo evaluate verify` re-derives the freeze and exits 0 only if nothing moved.

**Version 3, 2026-09-02.** It opened because the **input** layer moved under it, not because a
defect was found here. Six changes, each with the ADR that decided it, in that `README.md` §0.
The recalibration reproduced thirteen of fifteen arms' thresholds to six decimals.

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

**Exit met.** `make check` and `make verify` both exit 0, at protocol version 3 on the day
this was written and at **version 4** since 2026-09-03 —
the latter re-derives both freezes, re-runs the pocket detector and runs the network tests. The
calibration experiment is reproducible from its committed config on all 15 arms, and the
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
and, in §7, the sixteen limitations a reviewer would otherwise find.

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
sub-phase 1.6, met again once 1.6 closed at protocol version 2, and **withdrawn again on
2026-09-02** when the organisers' answers moved the input layer under it.

**Both per-target blockers are cleared, and one new gate condition replaces them.**

- **ADR 0016 is superseded by ADR 0031.** The mandated 5TBY arm is frozen, exposed and
  non-confirmatory, with both input defects measured and printed.
- **ADR 0020 is superseded by ADR 0036.** The c-Myc contract is frozen: `1NKP` chain A in
  author numbering, 82 native residues at auth 900–981, scored against NMR chemical-shift
  segments with a hypergeometric null, source-free metric, **declared non-blind**, in no Holm
  family. All four minimum targets now have a contract.
- **The new gate condition was met on 2026-09-02: protocol version 3 is frozen.** The primary
  input layer was re-frozen at six arms, so two arms' calibrated thresholds were stale and one
  had none at all. `experiments/2026-09-02-null-recalibration/` re-ran all fifteen gate arms.
  Thirteen reproduced their 2026-08-25 `size_ratio` and `alpha_star` to six decimals;
  `bcr_abl1_mandated` moved to 1.2073 / 0.0277 on chain B and `cardiac_myosin_mandated` came in
  at 1.0509 / 0.0485. `uv run allo evaluate verify --detect` exits 0 over fifteen arms and 777
  decoy pockets. **A threshold measured after a method is scored is a hyperparameter**, which
  is why the order was this way round and not the convenient one.

---

## Phase 2 — Quantum propagation metric (statevector)

**Open. The substrate is built and the first four experiments have run.** Every hyperparameter
is chosen on the secondary set's `development` tier, and every number is produced by
`allo.scoring.score_arm` and no other path.

**Built on 2026-08-26.** `allo.network` (stage S1), `allo.classical` (S3–S7, three registries:
`baselines`, `coupling`, `mechanism`) and `allo.quantum` (S5). Sixty-nine scorers in total, none
of which existed when `docs/evidence/method-landscape/` was compiled.

**Extended later the same day**, after four further literature sweeps returned
(`docs/evidence/method-landscape/13` to `16`). `allo.quantum` gained three families: `interference` (the exact
separation of the interference term from the phase-cancelled overlap term), `connectivity` (the
**N × N matrix `CHALLENGE.md` §5 requires**, plus four source-free scorers) and `quantumness` (the
source-state energy lever and the symmetry route). `allo.classical.coupling` gained
`gnm_transfer_entropy_net`, and `allo.network.build` gained `min_seq_sep` and the `ohm`
weighting.

**Measured on 2026-08-26**, all on the `development` tier and nowhere else:

| Experiment                           | What it settled                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| ------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `2026-08-26-selection-power`         | **The screen's ceiling is an interval, and the screen sits on its upper edge.** 1620 variants hold only **8.86–10.58** independent directions, so the label-blind p95 runs from 0.707 (effective V) to 0.810 (raw V). The minimum detectable effect starts at 0.794. The **confound-removal axis** buys 3.8 independent directions; the **graph axis** buys 0.6                                                                                                                                                                                                                                                                                                                                     |
| `2026-08-26-method-sweep`            | 6480 records, 1620 complete variants. Best mean AUC **0.810** (`eigenvector_centrality`), **0 reject the null on all four arms**, the graph axis spans only 0.031 AUC, and quantum loses **30 of 30** paired cells to classical by +0.196 AUC. `docs/method/exploration/results/40-method-sweep.md`                                                                                                                                                                                                                                                                                                                                                                                                 |
| `2026-08-26-mechanism-probe`         | Three cross-system mechanism signatures. The published soft-corridor prediction is refuted; its inverse reaches mean AUC 0.714 with rank correlation −0.12 against distance, and still rejects no null                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| `2026-08-26-fusion-probe`            | Label-blind consensus, spatial smoothing and the top-5 assembly rule. Best mean AUC 0.765, below the label-blind median of 0.771. Sign alignment is the one knob worth its cost                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `2026-08-26-source-choice`           | **The propagation source does not have to be the active site, and often should not be.** Six label-blind size-matched sources. `degree` reaches mean AUC 0.705 with a worst arm of 0.608; `catalytic` reaches 0.564 with a worst arm of 0.323 and the largest between-arm spread of any source (0.486). Source conditioning still carries information: catalytic beats random on rejections, 0.118 against 0.076                                                                                                                                                                                                                                                                                    |
| `2026-08-26-beats-distance`          | **The central negative.** 69 scorers through the frozen paired test. **7 of 272** beat distance at uncorrected p ≤ 0.05 where chance gives 6.8, and **0 of 272** beat `eigenvector_centrality`. Also records that Holm **cannot reject on `ptp1b` or `ns5b` at any data**, because the permutation floor (0.001080) exceeds Holm's first step                                                                                                                                                                                                                                                                                                                                                       |
| `2026-08-26-stability-and-source`    | **The §4.2 noise-resilience evidence.** Coordinate noise, edge loss, source loss and a shortened coherence window, over 30 scorers and all four arms. At 1.0 Å the mean rank stability is **0.908 classical against 0.629 quantum**, and the **twenty** least stable scorers are all quantum. **The top-5 list is far less stable than the endpoint for every method** — geometry holds ρ 0.978 with Jaccard **0.46**, and `connectivity_strength` reaches AUC 0.625 with Jaccard **0.05**. Stability tracks the distance component inside the quantum family at Spearman **+0.874** (p < 0.0001, n = 22), so escaping the confound costs stability — though `degree` shows the trade is not forced |
| `2026-08-26-ensemble-stabilisation`  | **The remedy for the quantum instability, and it is not dephasing.** A rank mean over 16 jittered structures lifts held-out stability from 0.33–0.80 to 0.82–0.98, which is the classical range, at a cost in AUC of between −0.055 and +0.035                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `2026-08-26-timescale-normalisation` | **Tuning the clock does not work, and the measurement rules out the class.** Two spectral clocks × 8 windows × 4 finite-window observables. The `gap` clock halves window sensitivity (0.079 → 0.045) and leaves the between-arm AUC spread at **0.5627 → 0.5516**, a 2 % reduction. Between-arm variance is **1.3× to 14.5×** the within-arm window variance, and **0 of 32 settings** put all four arms above 0.5                                                                                                                                                                                                                                                                                 |

**ADR 0026 changed the entry conditions.** The eleven quantum insertion points that
`docs/evidence/method-landscape/00-conventions.md` §5 recorded as closed rested on a benchmark containing
all three primary targets in its own evaluation sets. Eight are re-opened and were measured
here. Three stay closed on mathematics.

**What Phase 2 still owes.** One frozen method — one graph, one scorer, one confound-removal
form, one assembly rule, written into an ADR — plus a pre-registered prediction, before the
`generalisation` tier is opened. The design is
`docs/method/exploration/results/42-threats-and-confirmation.md` §4.

**Four conformance gaps found on 2026-08-26 that no score fixes.** `docs/report/conformance.md`
re-reads the challenge PDF requirement by requirement. The N × N connectivity matrix did not
exist and now does; **no circuit has been compiled**, nothing has run on **Braket or Classiq**,
and **c-Myc has no arm** although §8.2 counts it among the minimum four targets. Items two and
three belong to Phase 3 and item four blocks method design under ADR 0020.

**One diagnosis that changes what Phase 2 means.** Faccin et al. (Phys Rev X 3, 041007) prove a
time-averaged quantum walk equals the classical degree ranking **exactly at zero initial-state
energy**. Our source state had energy exactly zero, because a site-basis state has
`⟨i|A|i⟩ = 0`. The bound on the deviation is `E/Δ`, and `Δ` varies **21.7×** across the four
`development` arms while the spectral range varies 1.09×. That is the reason the walk
observables behaved classically. It is **not** a lever: `2026-08-26-timescale-normalisation`
normalised the time grid by `Δ` on every arm and the cross-protein spread did not move.

**Per-protein adaptation was investigated on 2026-08-27 and is closed by ADR 0028.** The
direction was to adapt the pipeline to the input protein. **The effect it aims at is real.**
Blocked on scorer and permuted 200 000 times, the arm level effect gives classical
p = **0.00007** over 42 scorers, with a median per-scorer arm spread of **0.338**. What closes
the route is the sample, not the phenomenon. At four arms the minimum attainable two-sided
Spearman p is **0.083**, so a rank test over proteins has power **exactly zero at any effect
size**, and a screen of 30 apo-only descriptors returned **1** perfect ordering against
**2.50** expected by chance. The held-out `generalisation` tier is **5** arms, not ten — the
primary set is the confirmatory family and cannot also be a tuning surface — and at n = 5 the
power against a true rank correlation of 0.90 is **0.25**. So: **there is definitely something
to adapt to, and the benchmark definitively cannot tell us what it is.** No fitted adaptation
rule may enter the pipeline. The headroom is in **source geometry**: the graph side has no
between-protein spread to normalise, measured twice
(`docs/method/exploration/results/52-derived-cutoff-prescreen.md`), and neither does the clock.
`docs/method/exploration/results/48-adaptation-feasibility.md`.

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

Trotterised `exp(-iHt)` in the single-excitation sector — **or the exact Givens network, which
`docs/method/exploration/results/43-quantum-resources.md` prices as 3 to 8 times shallower on
every arm and cheaper on four of five. Phase 3 must state which it uses and why.** Gate counts, depth, qubit count and
connectivity reported per target (C3). Aer noise models sweeping gate error and decoherence;
stability of the **ranking**, not just the raw metric, since the ranking is the deliverable.
Execute a coarse-grained instance on AWS Braket or via Classiq synthesis.

**Exit:** resource table per target, ranking-stability curves against noise strength, and at
least one real-hardware or hardware-emulated run.

**Two things Phase 2 found that Phase 3 must carry.** The depolarizing order-preservation
guarantee does **not** reach `ctqw_temporal_variance` or `quantum_opening_gain`, because both
are ratios and the noise offset does not divide out of the denominator — those two need
per-correlation-length calibration. And the dominant hardware cost is the circuit **count**,
not the gate count: every continuous-time observable needs `512 x |S|` circuits, which is
5632 on `mkp5` and 10752 on cardiac myosin.

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

**The compression Phase 4 must achieve is now a number per arm.** A 20-node coarse-grained
graph is the ceiling that current hardware fidelity supports, so the factors are mkp5 7.3x,
ptp1b 14.9x, hiv_rt 27.1x, ns5b 27.6x, `cardiac_myosin_corrected` 38.2x. **The open question
is not the compression.** No file yet says how a ranking over 20 super-nodes becomes a
residue-level top-5, and the top-5 list is the mandated deliverable.

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
