# Constraint audit of the eleven-stage pipeline, before anything is built

**Scope:** an adversarial audit of `11-pipeline-decomposition.md` against C1–C6 as stated in
`AGENTS.md`, plus the challenge-compliance question the constraints do not cover. It covers
every stage S0–S10 and the five data routes that bypass the import graph. It deliberately
excludes whether the method will *work* — no verdict here is about accuracy — and excludes the
evidence behind each stage, which lives in files 01–10a.
**Sibling files:** `11-pipeline-decomposition.md` for the proposal, `10a-fact-check.md` for the
corrections that bind it, `00-conventions.md` §4 and §7 for the constraint and leakage rules.
**Retrieved:** 2026-08-25.

---

## Verdict

**3 PASS, 7 RISK, 1 VIOLATION**, over eleven stages.

The violation is not leakage. It is that the proposal, read at its word, produces the required
deliverable classically and leaves no quantum circuit that outputs a ranking — which
`CHALLENGE.md` §4.1 states as a **must**.

No stage requires reading any of the five protected data routes, and no stage requires
`allo.inputs` to regain a capability it dropped. Both were traced, not assumed; the trace is in
§3.

| # | Stage | Verdict | One-line reason |
| --- | --- | --- | --- |
| S0 | Structure ingest | **PASS** | `apo_input` is hash-pinned, takes no manifest, and `_prediction_structure` raises on any non-protein atom (`src/allo/inputs.py:237`) |
| S1 | Graph construction | **RISK** | Hydrogens are absent from `ApoInput.structure` by construction; edge-class weight values have no declared provenance; the strongest cited evidence is two-state and therefore C1-forbidden |
| S2 | Source definition | **PASS** | `active_site` reads the apo entry only, and the cofactor is a locator that never becomes a node (`src/allo/inputs.py:161-181`) |
| S3 | Operator construction | **PASS** | Laplacian or adjacency from contact topology is squarely inside C6 and is analytic, not MD. The unmade choice is charged to S5, not here |
| S4 | Perturbation | **RISK** | The on-site shift magnitude is a free scalar with no declared selection venue |
| S5 | Propagation and readout | **VIOLATION** | The readout is assigned to classical and left unnamed, so no circuit produces the ranking (`CHALLENGE.md` §4.1) and the S8 proof and the S9 circuit require different operators |
| S6 | Confound removal | **RISK** | "Fit `k` without labels" is asserted, not specified: no functional form, no fit universe in code, no test that would catch a leaky fit |
| S7 | Site assembly | **RISK** | The diversification radius is a free parameter, and the number motivating it comes from a set no ADR has vetted for overlap with the primary targets |
| S8 | Coarse-graining | **RISK** | The node-retention rule is never stated, and the proposal's own falsifier selects the ratio by recall of the known site |
| S9 | Circuit synthesis | **RISK** | C3 is met per circuit and not per deliverable: the perturbation formulation needs N circuits and the N×N matrix needs O(N²) estimates, at an unreported shot budget |
| S10 | Evaluation | **RISK** | The stage is labelled frozen and then changed, and "visible before a method runs" invites conditioning design on arm difficulty |

---

## 1. The violation

### S5 — the readout is not chosen, and both downstream stages assume a different one

**Constraint:** `CHALLENGE.md` §4.1 and §5 output 1. Against C1–C6 this is at worst a C4 risk;
against the challenge's primary objective it is a failure, and the challenge is the spec.

`CHALLENGE.md` §4.1 is unambiguous: "Participants **must build a quantum circuit that simulates
signal propagation through the protein structure**" and "The circuit must output a **ranking of
residues** based on their dynamic connectivity". §5 output 1 requires the N × N matrix entries
to be "the **calculated quantum connectivity strength** between residue i and residue j".

The proposal assigns S5 to classical outright — "Owner: classical. Quantum enters at S9 as a
hardware map, not here as a scorer" (line 74) — and reports the whole N × N deliverable at 6.0 ms
and 82 ms on a laptop (line 86). Taken at its word, nothing in the pipeline is a circuit that
outputs the ranking. `docs/ROADMAP.md` Phase 2's exit criterion says the same thing from the
other side: "at least one **quantum metric** beats the best classical baseline".

The deeper problem is that S5's readout is left unnamed while S8 and S9 each already assume one,
and they assume different ones:

- **If S5 is the perturbed CTQW transfer** (ADR 0002 metric 5, which the proposal says survives),
  then S9's Givens network is a genuine hardware map of the scored quantity and C4 is satisfied —
  but S8's exactness result does not apply. `10a-fact-check.md` claim 10 confirms Kron reduction
  preserves effective resistance and states plainly that it "does not extend to eigenvalues,
  eigenvectors, or a propagator". The proposal repeats this caveat at line 162 and then composes
  the two anyway.
- **If S5 is effective resistance to the source** (file 05's "best-fitting observable"), then S8's
  proof lands exactly — and S9's circuit computes a quantity the deliverable never uses. File 07
  itself already gates this: line 558 says report the resistance invariance "**if and only if the
  propagator readout is resistance-like**", and line 736 says Kron is "a second arm to run *only*
  where the readout is resistance-like".

So exactly one of S8's proof and S9's circuit is off-method, whichever way S5 goes, and the
proposal does not say which. That is not a detail to settle later: S8 and S9 are the two
deliverables the proposal calls "defensible" in §3.

**Repair.** Name S5's readout before S8 or S9 is built, and require both to be derived from that
one operator. Concretely, the honest configuration that satisfies §4.1 is:

1. S5 = the single-excitation propagator `exp(-iHt)` on the weighted graph, with the metric-5
   perturbation. It is quantum-inspired, classically simulated at full N.
2. S9 = the Givens network for **that same** unitary, which makes C4's "state how it maps to
   hardware" a construction rather than a claim, and lets the circuit reproduce the ranking at
   N ≈ 20 as a demonstration.
3. S8 keeps Kron + effective resistance only if effective resistance is *also* computed and
   reported, as a **classical baseline** under the Phase 1.4 list — not as the deliverable. Its
   exactness proof is then a proof about a baseline, stated as such.
4. If instead effective resistance is chosen as the deliverable, the report must say in its own
   voice that the submission does not meet §4.1's primary requirement, and argue why. That is a
   defensible negative result. Silently shipping it is not.

The unitary-coarsening gap the proposal names at line 169–172 is the fourth option, and it is the
only one that makes S8 and S9 the same object. It is real work and it should be costed before it
is planned against.

---

## 2. The risks

### S1 — three separate mechanisms, and the first is a factual error in the proposal

**C6, C2, C1.**

**(a) The stated input is wrong.** Line 55 says `allo.inputs.ApoInput.structure` carries "**every
protein atom** of the modelled chain". It does not. `Structure.protein` is
`in_polymer & _heavy` (`src/allo/structure/pdb.py:68-80`), and `_prediction_structure` copies
`apo.protein` (`src/allo/inputs.py:195`), so the prediction structure holds **heavy atoms only**
— hydrogens and deuteriums are removed whether or not the deposited entry has them. M3L's three
methyl carbons are removed too (`src/allo/inputs.py:200-202`).

This lands directly on the hydrogen-bond edge class. There are no hydrogens to assign one from,
and the two repairs are not equally safe:

- **Safe.** A heavy-atom geometric criterion — donor/acceptor element and atom-name typing from
  `structure.element` and `structure.atom`, a donor–acceptor distance cut, and an angle from
  backbone geometry where the amide H position is determined by it. This is a classification of
  the contact graph and stays inside C6, which the challenge words as "the topology of the contact
  network is the primary driver ... allowing us to abstract away specific atomic force fields".
  File 06 line 585 reaches the same verdict for edge weighting generally.
- **Not safe.** Protonating with `reduce`, `pdb2pqr` or an OpenMM/AMBER pipeline to obtain H
  positions. That imports a force field and a protonation model, which is the thing C6 abstracts
  away, and an OpenMM route puts an MD engine on the prediction path within reach of C2. Adding
  hydrogens would also require changing `Structure._heavy`, which is shared with the
  ground-truth side — a C1-boundary module — so the blast radius is not local.

**(b) The weight values have no provenance.** The proposal names three edge classes and a 1/d²
contact rate but never says where the *numbers* come from. Two published sources are C2 traps and
both are one search away: a Hinsen-style distance-dependent force-constant curve is fitted to an
all-atom force field, and HBAlloMap — which file 06 line 583 lists — derives its H-bond
fluctuation correlations from MD and is marked there as a "**C2 violation as published**; the
H-bond graph itself is reusable". The graph is reusable; the weights are not.

**Repair.** State in the stage spec that class weights are either (i) free parameters fitted on
the `development` tier, or (ii) fixed a priori and declared with the reasoning, per ADR 0012
("'We used the usual value' is a declaration; 'we tried a few' is not"). No weight may be
inherited from a source whose value was fitted to a force field or to a trajectory.

**(c) The strongest cited evidence is C1-forbidden in its strong form.** The Src side-chain result
the proposal leans on (PMC12893324) classifies residues by their contacts in **active and
inactive** structures — "active-only", "inactive-only", "swapping". File 06 line 579 already draws
the conclusion for us: contact dynamics "needs two structures — **holo-derived, so C1-forbidden
for us**". The single-structure classification (is there a salt bridge in the apo entry) is
apo-computable and legal; the state-swap classification is not. The proposal cites the evidence
without carrying the restriction.

**Repair.** S1 implements single-apo-structure class assignment only, and the report states that
it is implementing the weaker, legal form of a result measured in the stronger form.

**Two correctness notes, not constraint findings.** "Minimum heavy-atom **side-chain** distance"
is undefined for glycine and needs a stated fallback. And `altloc` is carried through unfiltered
(`src/allo/inputs.py:223`), so a minimum-distance edge length will pick the closest alternate
conformer and can manufacture contacts that no single conformer has.

### S4 — the perturbation magnitude has no declared venue

**C1, via hyperparameter selection.** Metric 5 shifts an on-site energy at the candidate residue.
That shift is a scalar, it changes the ranking, and the proposal names no venue for choosing it.
The governance sentence that exists (line 69–70) is scoped to S1's edge classes only. Repair: the
shared one, §2.7 below.

### S6 — "fit `k` without labels" is asserted and not specified

**C1.** This is the stage the brief asked to be audited hardest, and the finding is that caution 2
(line 118) is correct and unimplementable as written. "Fit it per-target on the candidate set's
own score-versus-distance trend, never on the positives" is a sentence, not a procedure. Four
things are missing, and each is a distinct way for a label to get in without a holo file opening.

**(a) The fit universe.** "The candidate set" is an evaluation-layer term. Its authority is
`frozen.json`, which the prediction path may not read (`tests/test_no_leakage.py:23-47` and
`:385-397`). It happens to be apo-reconstructible today: `evaluation_graph` builds
`candidates=tuple(r for r in order if r not in set(source))` (`src/allo/scoring/nulls.py:119`),
and ADR 0011's 2026-08-24 amendment records that on the current freeze
`excluded_from_scoring == active_site` and `n_candidates == n_residues - len(active_site)`.

That equality is a *fact about the current freeze*, not an invariant. ADR 0011 clause 1 lists a
second ground for exclusion, and clause 4 says adding one is "a manifest change plus a re-freeze".
If a later re-freeze uses it, a prediction stage that fitted on `residues - active_site` diverges
silently — and the tempting fix, reading `n_candidates` from the freeze to check, is C1 leakage.

**Repair.** S6 computes its fit universe as `set(apo.residues) - set(apo.active_site)` from
`ApoInput` and from nothing else, with a comment saying the equality with `n_candidates` is
coincidental and must never be verified against the freeze.

**(b) The functional form and estimator.** Unspecified. Repair: fit `log(score) ~ a - k·d` by
ordinary least squares over the whole fit universe, per target, with `d` the minimum heavy-atom
distance to the propagation source (file 06's observable 1 requires that metric, not Cα). Every
candidate enters, positives included and unlabelled. That is what makes it label-free, and the
physics supports it: `10a-fact-check.md` lines 306–307 record that the 7.45 Å fit is over **all
252** residues of the kinase domain while 18.24 Å is over the **42 selected** sites, so a fit over
everything is dominated by the background — which is exactly the null S6 wants.

**(c) The literature-coefficient trap.** Hard-coding `k` from 7.45 Å or 18.24 Å would import a
coefficient fitted on a labelled set in another protein. The 18.24 Å figure is worse than a prior:
`10a-fact-check.md` line 326 records that the 42 sites "were selected for large effects", so the
number is conditioned on the answer. Using either as a fixed `k` is a hyperparameter chosen with
reference to labels, with no holo file opened, and it is the exact shape of leakage the audit
brief names. Repair: `k` is always fitted, never quoted.

**(d) The test that would catch a leaky fit.** Two, and they live on different sides of the
firewall.

- *Prediction-side*, in `tests/`: assert that S6's fit universe equals
  `set(residues) - set(active_site)` derived from `apo_input` alone, and that S6's module text
  contains none of `FROZEN_TOKENS`. The second is free — the existing guards
  (`tests/test_no_leakage.py:385` and `:400`) already cover it once the module exists.
- *Evaluation-side*, the one that actually proves it: a **label-permutation invariance test**.
  Draw a random permutation of the label assignment, re-run S6 end to end, and require the fitted
  `k` to be **bit-identical**. A label-free fit cannot see the permutation. Any fit that was tuned
  against enrichment — including a human sweeping `k` and keeping the value that ranked known
  sites higher — moves. This test needs labels, so it belongs beside the scoring tests, never in
  the prediction path.

**(e) One thing S6 gets right, recorded so it is not repaired away.** Caution 3 (line 120) is
correct and is the honest framing: S6 helps a method that is partly a proximity ranker and is a
no-op for one that is not. It is a confound remover, not a signal source, and the report should
not claim otherwise.

### S7 — a free radius, and a number from an unvetted set

**C1, via hyperparameter selection.**

The top-5 cut itself is clean. `k = 5` is mandated by `CHALLENGE.md` §5 output 2, and it is frozen
in the harness as `settings["endpoints"]["top_k"]` (`src/allo/scoring/harness.py:207`), so it is
not a knob anyone can turn toward a pocket size. That is a PASS on the specific worry the brief
raised, and it is worth stating.

The diversification is not clean. "Spatial diversification raised top-5 from 24.4 % to 35.6 %"
(line 140) implies a spatial radius or a redundancy penalty, and that is a free parameter with no
declared venue. Worse, the number comes from the teammate's `allosteric-benchmark/` set of 73–101
targets. `rg` over `docs/adr/` returns **no ADR mentioning that repository**: it has never been
through ADR 0012's four disjointness clauses, so its overlap with the primary targets is unknown,
not zero. ADR 0012 exists precisely because the obvious tuning set turned out to contain the
answers to two of three primary arms.

**Repair.** Any value carried over from `allosteric-benchmark/` is re-derived on the
`development` tier or declared a priori. Its published numbers are legitimate as *motivation*;
they are not legitimate as *parameter values*. The same rule applies to any contact cutoff or
weight the proposal inherits from there.

### S8 — the retention rule is missing, and the falsifier selects on labels

**C1 and C3.**

**(a) Which nodes are retained is never stated.** Kron reduction is a Schur complement with
respect to a chosen interior; the choice of what survives *is* the coarse-graining decision. The
proposal specifies the ratio (~35×, from hardware) and the theorem, and not the rule.

The good news first, because the brief asked and the answer is clean: the target size is **not**
label-derived. It comes from the coherent gate budget — 200 two-qubit gates at Braket's 99.5 %
median fidelity, giving N ≈ 20 (line 190–192), which is consistent with N(N−1)/2 = 190 at N = 20.
That is a hardware derivation, traced to file 08, and nothing about it references a pocket size.

**(b) The falsifier does select on labels.** Line 174–177: "Sweep the compression ratio and report
... **recall@5 of the known site** at each ratio. If recall@5 survives to 35× on `development`,
S8 is solved." Choosing a ratio by recall of the known site is label-driven selection. On
`development` that is legal and is what the tier is for. It becomes a C1 violation the moment the
same sweep is run on a primary arm, and the proposal does not say it must not be.

`docs/ROADMAP.md` Phase 4's exit criterion already demands the right thing — "a rule for picking
the ratio for an **unseen protein**" — and the same demand applies to *which nodes*, not only how
many.

**Repair.** State the retention rule as a function of apo topology alone, fixed before any arm is
scored: retain the propagation-source set plus a topology criterion (degree, betweenness, or
local-variation contraction as file 07 recommends at line 735), with the ratio set by the hardware
budget and confirmed — not chosen — on `development`. Record it in an ADR, because reversing a
coarse-graining choice after a primary arm is scored is exactly the expensive kind of reversal
ADR 0001 asks for a record of.

**(c) The demonstration cannot emit the deliverable.** At ~20 supernodes over a 300–764-residue
chain each supernode spans roughly 15–38 residues, so a coarse instance ranks supernodes and
cannot produce a residue-level top-5. That is fine — the deliverable is produced at full
resolution — but it means S9's hardware run demonstrates an object that never produces a
deliverable, which feeds straight back into §1. The report must say this rather than let the
resource table imply the hardware run produced the hit list.

**(d) The densification cost is correctly flagged and must survive to the report.** Line 163: Kron
"densifies the reduced graph toward cliques, which is a direct C3 connectivity cost". Note the
tension with S9's "linear connectivity only" (line 186): a Givens network on a dense
single-particle Hamiltonian is still linear-connectivity, so the two are compatible — but the
gate count is the dense one, N(N−1)/2, and the report must not quote a sparse-graph figure.

### S9 — C3 is met per circuit and not per deliverable

**C3, C4.**

What is met, and it is more than most entrants will have: one qubit per residue, single-excitation
sector, N(N−1)/2 Givens rotations at depth **2N−3**, linear connectivity, zero Trotter error. The
depth is stated as a function of N, which is what the audit playbook asks for, and it carries
`10a-fact-check.md` claim 4's correction — the "exactly N depth" figure belongs to a fermionic
swap network for a different algorithm, and using it would have understated depth by about 2×.

What is not met is the per-deliverable accounting, and C3 says "**Every** quantum claim needs a
stated resource cost":

1. **Metric 5 is N re-simulations.** File 03's own costing is "300 re-diagonalisations". Each is a
   circuit. The quantum resource for one target's ranking is therefore N circuits at depth 2N−3,
   not one circuit at depth 2N−3.
2. **The N × N matrix is O(N²) amplitude estimates**, each needing its own shot budget.
3. **The noise claim has no number.** "Global depolarising noise provably preserves rank order ...
   the deliverable degrades only through a `1/λ²` shot budget" (line 200–202) is a quantum claim.
   Its cost is the shot count, given only as a scaling. C3 needs shots per target at the stated
   error rate.
4. **The long-time direction has no number at all.** S5 keeps open "long-time dynamics" as the one
   place a theorem declines to close the door (line 87–91). Long `t` is precisely where depth
   grows, and "deep, unoptimised circuits ... will be penalised" is `CHALLENGE.md` §5 constraint 2.
   If that direction is pursued it needs its own depth-versus-`t` table before it is planned
   against.

**Repair.** The resource table is per *target deliverable*, not per circuit: qubits, depth,
two-qubit gate count, circuit count, shots, and total shot-seconds, at both N ≈ 20 (demonstrated)
and full N (extrapolated), with the extrapolation labelled as such.

**One C4 note, in the proposal's favour.** A Givens network implements a quadratic, free-fermion
unitary, which is classically simulable by construction. The proposal already refuses to claim
advantage (§3, "Not defensible"), so this is consistent rather than contradictory — but the report
should state it outright, because a reviewer will notice that the exact encoding chosen for its
zero Trotter error is also the encoding that cannot be hard to simulate.

### S10 — labelled frozen, then changed

**Process, and a soft-leakage invitation.**

`AGENTS.md` says of the evaluation layer: "Nothing in it may change once a method has been
scored", and the layer was re-frozen as protocol version 2 on 2026-08-25 after its own audit
reopened it. The proposal marks S10 "**frozen**" in the table and then proposes adding a printed
critical AUC "beside every p-value" (line 214–216).

The statistics are sound. `R̄ = AUC·(n−m) + (m+1)/2` needs `m = |labels|`, and the record already
discloses that as `prevalence` (`src/allo/scoring/harness.py:269`), so the new field adds no label
information that a scored record does not already carry.

The problem is the stated purpose: "printing it beside every p-value makes each arm's difficulty
visible **before a method runs**". Arm difficulty visible before a method runs is an invitation to
condition method design on which arms are winnable.

**Repair.** Two lines. (i) The change goes through a re-freeze and `uv run allo evaluate verify`,
not an ad-hoc print — it is an evaluation-layer change however small. (ii) The critical value is
emitted **into the scored record at scoring time**, and not into any pre-run briefing, so it
documents a result rather than shapes a design.

### 2.7 The shared repair: one governance sentence, pipeline-wide

The proposal's hyperparameter rule exists but is stage-local. Line 69–70 says "Every one of them
is chosen on `development` and nowhere else", inside S1's Risk paragraph. §5's preamble says the
same for the five named experiments. Neither covers S4's perturbation magnitude, S6's fit
specification, S7's diversification radius, or S8's retention rule.

**Repair.** Promote it to a pipeline-level clause and enumerate what it binds:

> Every free parameter of S1–S8 — edge-class weights, contact cutoff, perturbation magnitude,
> propagation time, decay-fit specification, diversification radius, retention rule and
> compression ratio — is chosen on the `development` tier or fixed a priori with its reasoning
> declared, and is frozen before any primary arm is scored. No value is inherited from
> `allosteric-benchmark/`, which no ADR has vetted against ADR 0012's four clauses.

And the check that makes it more than a sentence: an experiment config committed **before** the
primary run, holding every one of those values, such that the primary run is a replay. That is
already the working agreement's determinism rule ("a rerun of a committed experiment must
reproduce its metrics bit-for-bit, or the config is incomplete") applied at the right moment.

---

## 3. The two checks the brief asked for by name

**Does any stage require reading one of the five protected data routes?** No. Traced per stage
against `PROTECTED_PATHS` and `FROZEN_TOKENS` in `tests/test_no_leakage.py:23-47` and `:610-624`.

- S0, S2 need the redacted manifest, which `allo.inputs.load` already supplies through two
  allow-lists (`src/allo/inputs.py:100-154`).
- S1, S3, S4, S5, S7, S8, S9 need only `ApoInput.structure`, `residues` and `active_site`.
- S6 needs the candidate set, which is reconstructible from `ApoInput` — see §2, S6(a). This is
  the only stage where a protected route is *tempting*, and the repair is to make the
  reconstruction explicit in code so nobody later "verifies" it against the freeze.
- S10 reads `frozen.json` and the evaluation manifest, and it is allowed to: `allo.scoring` is
  allow-listed (`tests/test_no_leakage.py:61-67`) and is the evaluation side of the firewall.

Nothing in the proposal needs `selection.json`, `extension-candidates.md`, or anything under
`docs/benchmark/evaluation/`.

**Does the proposal require `allo.inputs` to regain a dropped capability?** No. Checked against
the three capabilities the module deliberately dropped: the `manifest` parameter on `apo_input`
(`src/allo/inputs.py:262-271`), the `site` display string (`:132-140`), and the re-exported
`read_manifest` (`tests/test_no_leakage.py:558`). No stage needs any of them.

One adjacent change is worth naming because it is not a `allo.inputs` change and would be easy to
propose as a small one: S1's hydrogens would require altering `Structure._heavy`
(`src/allo/structure/pdb.py:68-70`), which is shared with the ground-truth side. It is a
C1-boundary module and a change there is not local. The repair in §2, S1(a) avoids needing it.

---

## What this changes for our pipeline

- **S5 is blocking, not open.** Naming the readout is a prerequisite for S8 and S9, not a Phase 2
  deliverable that can follow them. Until it is named, one of the proposal's two "defensible"
  claims is guaranteed to be about the wrong operator. Settle it with §5's experiment 1 (the
  effective-resistance contradiction), which is already the cheapest run in the list.
- **S6 needs a written specification before it is coded**, not after: fit universe from
  `ApoInput`, OLS on `log(score)` against minimum heavy-atom distance to the source, `k` always
  fitted and never quoted from literature. Plus the label-permutation invariance test, on the
  evaluation side.
- **S1's stage spec must correct the input statement** — heavy atoms, not every atom — and must
  state the apo-only hydrogen-bond criterion and the provenance rule for weight values. The
  proposal's factual error here would otherwise be inherited by whoever implements it.
- **S8 gains a retention rule in an ADR**, stated as a function of apo topology, before the ratio
  sweep runs. `docs/ROADMAP.md` Phase 4 already asks for the ratio half of this.
- **S9's resource table is per deliverable**, with circuit count and shots, at demonstrated and
  extrapolated N.
- **The hyperparameter governance clause moves out of S1's Risk paragraph** and becomes
  pipeline-level, enumerating all eight parameters and naming `allosteric-benchmark/` as an
  unvetted source.
- **S10 is not touched without a re-freeze**, and the critical AUC is emitted into records rather
  than into pre-run briefings.
- **ADR 0002 should be superseded with the readout named**, which the proposal already
  recommends — and the supersession is where the S5 decision belongs, because it is expensive to
  reverse.

## Method

No retrieval. This is a static audit of `11-pipeline-decomposition.md` against `AGENTS.md` C1–C6,
`docs/playbooks/constraint-audit.md`, and `CHALLENGE.md` §4.1, §5 and §6.

Traced in the repository: `src/allo/inputs.py` (whole file, for what `ApoInput` carries and what
`load` redacts), `src/allo/structure/pdb.py` (`Structure`, `_heavy`, `protein`, `contacts`,
`fetch_mmcif`), `src/allo/scoring/harness.py` (`_positives`, `score_arm`, `top_k`, `prevalence`),
`src/allo/scoring/nulls.py` (`evaluation_graph`, candidate construction),
`tests/test_no_leakage.py` (whole file, for `PROTECTED_PATHS`, `FROZEN_TOKENS`,
`MAY_IMPORT_GROUND_TRUTH` and the runner gate), ADR 0002, 0005, 0011, 0012, 0021, 0025, and
`docs/ROADMAP.md` Phases 2–5. Cross-read in the review: file 05 §STEP-3(a) and its pipeline
section, file 06 §5 and its observables table, file 07 §1.3 and its recommendations, and
`10a-fact-check.md` claims 4, 6 and 10.

Two `rg` searches decided findings rather than illustrating them: `allosteric-benchmark` over
`docs/adr/` returned nothing, which is what makes the teammate set unvetted under ADR 0012; and
`altloc` over `src/allo/` returned three sites, none of them a filter.

**Not opened, by `00-conventions.md` §7:** `docs/benchmark/primary/frozen.json`,
`docs/benchmark/secondary/frozen.json`, `selection.json`, either `manifest.yaml`,
`extension-candidates.md`, and everything under `docs/benchmark/evaluation/`. Every statement
above about the candidate set, `n_candidates` and the evaluation protocol is derived from code and
from ADRs, not from a freeze artifact. No label residue is named in this file.

**Stopping rule:** every stage S0–S10 given a verdict against all six constraints plus the two
named cross-checks; stopped when each stage had either a traced PASS with the file that proves it
or a stated mechanism and repair.
