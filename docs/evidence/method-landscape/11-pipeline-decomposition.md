# The pipeline, stage by stage: who owns what, and what would prove it wrong

**Scope:** the decision file. It decomposes the end-to-end method into eleven stages, assigns
each stage to classical, AI or quantum on the evidence in files 01–10a, and states for every
assignment the observation that would overturn it. It deliberately excludes the evidence
itself, which lives in the numbered files, and it excludes any number not traceable to one of
them.
**Sibling files:** `10-synthesis.md` for the cross-cutting argument, `10a-fact-check.md` for
the corrections that bind this file, `00-conventions.md` for the constraints.
**Retrieved:** 2026-08-25.
**Audited:** 2026-08-25 by `12-constraint-audit.md` — **3 PASS, 7 RISK, 1 VIOLATION**. The
violation was in S5 and is repaired below. Every RISK is marked at its stage. Read the audit
before implementing any stage; it carries repairs this file only summarises.

---

## 0. Why decompose at all

The challenge asks for one artifact: a ranked residue list per target. It is easy to read that
as one algorithm. It is not one algorithm. It is a chain of eleven transformations, and the
evidence says the classes differ in quality by stage, not overall.

The mistake this file exists to prevent is picking a method for the **pipeline** when the
question is which method suits each **stage**. Nine independent reviews converged on a shape:
AI is strong at the two ends, geometry is strong in the middle, and quantum is strong at
none of them on this object. That is not a reason to abandon quantum. It is a reason to put
quantum where it is honest, and to stop paying for it where it is not.

---

## 1. The eleven stages

`S0`–`S2` are closed by Phase 1 and frozen. `S3`–`S10` are Phase 2 and later.

| # | Stage | In → out | Owner | Status |
| --- | --- | --- | --- | --- |
| S0 | Structure ingest | apo mmCIF → atoms of the modelled chain | classical | **frozen** |
| S1 | Graph construction | atoms → weighted residue graph | **classical, physics-weighted** | **open, highest leverage** |
| S2 | Source definition | structure → propagation source | classical, rule-based | **frozen** (ADR 0005) |
| S3 | Operator construction | graph → Kirchhoff / Hamiltonian | classical | open |
| S4 | Perturbation | operator + candidate → perturbed operator | classical | open |
| S5 | Propagation and readout | perturbed operator → response | **must be one named operator; quantum owns the circuit** | **open — settles S8 and S9** |
| S6 | Confound removal | raw score → decay residual | **classical, and the decisive stage** | **open, untested** |
| S7 | Site assembly | residue scores → top-5 list | classical, set-valued | open |
| S8 | Coarse-graining | full graph → ~20 nodes, and back | classical, with a proof | open |
| S9 | Circuit synthesis | coarse operator → circuit, depth, noise | quantum | open |
| S10 | Evaluation | scores → p, AUC, recall@5, DCC | **frozen** | **frozen** |

### S1 — Graph construction. The stage the evidence says matters most

**Owner: classical, physically weighted.** File 06 answers question (d) directly: better edge
weighting matters more than a better propagator, and it stays inside C6. Two orthogonal
experimental techniques agree that a hydrogen-bond shortcut is worth 3–4 backbone residues,
and that across-sheet transfer beats along-strand. File 09's convergent finding 9 states the
same conclusion from the data side: the information lives in the edges, not the propagator.

**What changes from current practice.** The teammate's benchmark used Cβ coordinates at a
10 Å cutoff, because that was the input it defined. `allo.inputs.ApoInput.structure` carries
**every heavy protein atom of the modelled chain** — `Structure.protein` is
`in_polymer & _heavy`, so **hydrogens are stripped** *(corrected 2026-08-25; this file first
said "every protein atom", which is wrong and matters)*. Hydrogen-bond assignment must
therefore be **heavy-atom geometric**. Protonating with pdb2pqr or OpenMM would import a force
field, which C6 abstracts away, and an MD engine, which C2 forbids. With that constraint
stated, this pipeline can still build a graph the earlier work could not:

- edge length as **minimum heavy-atom side-chain distance**, which file 06 identifies as the
  variable the biological decay law is actually exponential in — not Cα distance;
- edge classes for hydrogen bond, salt bridge, and side-chain packing contact;
- contact rate weighting as 1/d².

**Falsifier.** Build three graphs — Cβ-10 Å, heavy-atom, heavy-atom plus edge classes — hold
S3–S7 fixed, and score all three on the secondary set's `development` tier. If the weighted
graphs do not separate from Cβ-10 Å, this stage is not the leverage point and S6 becomes the
only remaining one.

**Risk — RISK verdict in `12-constraint-audit.md`, three parts.** Edge classes add free
parameters, and every one is chosen on `development` and nowhere else, or the primary benchmark
is burned (`docs/FIELD.md` trap 4). Two further findings from the audit bind harder:

- **The edge-class weight values have no admissible provenance.** Hinsen-style constants and
  HBAlloMap are both C2 traps, and file 06 already marks HBAlloMap C2-violating. A weight must
  be fitted on `development` or derived from geometry, never quoted from an MD-parameterised
  source.
- **The Src side-chain evidence cannot justify this stage.** It is a two-state classification,
  and file 06 records it as holo-derived — **C1-forbidden for us**. The mechanism claim for
  edge weighting must rest on the remaining apo-admissible evidence, or the stage is motivated
  by something we are not allowed to use.

### S3–S5 — Operator, perturbation, propagation

**Owner: one named operator, and quantum owns its circuit.** *(Repaired 2026-08-25. The
first version of this file assigned S5 to classical outright and put quantum at S9 as a
hardware map. `12-constraint-audit.md` recorded that as a VIOLATION and it is right twice
over.)*

**Why it was wrong.** `CHALLENGE.md` §4.1 requires that participants "must build a quantum
circuit that simulates signal propagation" and that "the circuit must output a ranking". A
quantum stage bolted on after the ranking is produced does not satisfy the primary objective,
whatever it satisfies about C3 and C4. Assigning S5 to classical outright fails the challenge
on its own terms.

**The second error is internal, and worse.** The first version left S5's readout unnamed while
S8 and S9 each silently assumed a **different** one. S8's proof is Kron reduction plus
effective resistance — a resistance-like readout, and `10a-fact-check.md` claim 10 confirms the
exactness does **not** extend to a propagator. S9's circuit is a Givens network, which is a
propagator. Exactly one of the two headline claims in §3 is off-method whichever way S5 is
later settled, and the first version could not see that because it never named the operator.

**The repair: name S5 first, and derive S8 and S9 from it.** Two coherent pipelines exist, and
they are not mixable.

| | Option A — resistance-like | Option B — propagator |
| --- | --- | --- |
| S5 readout | effective resistance / commute time to the source | `exp(−iHt)` transfer, perturbed |
| S8 proof | **exists and is exact** (Kron) | **does not exist** — must be derived |
| S9 circuit | must be a resistance or spectral estimator, not a Givens network | **exists and is exact** (Givens, `N(N−1)/2` gates, depth 2N−3) |
| Challenge §4.1 | circuit must still simulate propagation — needs an argument | satisfied directly |
| Main risk | may be insertion point 1 in disguise (pre-mortem row 3) | S8 gap is real work, and file 09 says the observable is empty on our spectra |

**Experiment 1 settles this**, and it is already first in §5 for an unrelated reason. It should
now be understood as the stage-defining experiment, not a tidy-up.

The rest of this section stands as written.

File 03 eliminated the ADR 0002 candidate list down to metric 5, the perturbation formulation,
and file 09 explains why the others fail on our own graphs rather than in principle: the
adjacency spectrum is GOE with a median of **zero** near-degenerate pairs, and λ₁ is isolated
by **25.6 mean spacings**. A continuous-time quantum walk on a spectrum shaped like that must
collapse onto eigenvector centrality. That is the mechanism behind the published agreement in
Mohtashim et al., measured on 501 of our own graphs rather than argued.

The stated cost objection to metric 5 is void. File 03 computes 300 re-diagonalisations at
8.1 × 10⁹ flops — seconds. File 08 measures the entire N × N deliverable at **6.0 ms** for
N = 300 and **82 ms** for N = 764.

**One quantum direction remains open, and only one.** File 10a corrected the reading of
Sakamoto & Fujii: the no-advantage result holds for **short-time** dynamics, `t = polylog(N)`,
and the same paper's third result "suggests a super-polynomial time advantage when restricting
the computation to polynomial-space" for **long-time** dynamics. Nothing in this review tested
a long-time observable. It is the one place a published theorem declines to close the door.

**Falsifier for the whole classical assignment.** Compute the Spearman correlation between the
chosen readout and eigenvector centrality on every arm, and print it. `score_arm` already
accepts this through its `against` parameter, and its docstring already demands it. A readout
that correlates above about 0.9 with eigenvector centrality has reproduced Mohtashim et al.
and has not cleared the bar (ADR 0002).

### S6 — Confound removal. The decisive stage, and it is untested

**Owner: classical. This is the single most valuable open experiment in the review.**

Five independent routes agree that the ground truth decays exponentially with distance from
the active site (file 10, convergent finding 2). Everyone in the field, ourselves included,
has treated that as a confound to stratify away. File 06 shows it is a physical law with a
fitted form, and that **real sites decay more slowly than background**: Src's major allosteric
sites fit a half-distance of 18.24 Å against 7.45 Å for all sites.

If that holds, the correct estimator is not "beat distance". It is: **fit `exp(−k·d)` as the
null, and score the residual.** No method in any of the nine files does this.

**Three cautions, all load-bearing.**

1. **The 18.24 Å figure is fitted over 42 sites selected for large effects** (`10a-fact-check.md`,
   claim 6). That is a selection effect sitting directly under the proposed method. The
   mechanism may be real and the coefficient inflated.
2. `k` must be fitted **without labels**, or S6 is leakage wearing a physics costume. Fit it
   per-target on the candidate set's own score-versus-distance trend, never on the positives.
3. Removing distance can remove signal. File 06 says distance carries real biophysics; file 09
   measures that ALPS already has R² 0.003 on distance, so for that method there is nothing to
   remove and S6 is a no-op. S6 helps a method that is partly a proximity ranker and does
   nothing for one that is not.

**The spec, because "fit k without labels" is not implementable as prose.**
`12-constraint-audit.md` called the first version of this stage unimplementable, and named it
the top C1 repair. It is specified here rather than left to the implementer:

- **Fit universe:** the residues of `ApoInput.residues` minus `ApoInput.active_site`, derived
  from `ApoInput` alone. It is *not* the evaluation layer's candidate set. The two coincide on
  the current freeze, but `n_candidates == n_residues − len(active_site)` is a fact about this
  freeze and not an invariant (ADR 0011, amended), so naming the evaluation term here would
  couple the prediction path to the evaluation layer.
- **Functional form:** ordinary least squares of `log(score)` on minimum heavy-atom side-chain
  distance to the source, one fit per target.
- **Rule:** `k` is always fitted, never quoted, and never carried between targets.
- **Test:** an evaluation-side label-permutation test. Permute the labels, refit, and require
  `k` to be **bit-identical**. If it moves, the fit saw the answer key and the stage is C1
  leakage wearing a physics costume.

**Falsifier.** Apply S6 to every baseline and to the candidate method on `development`. If the
residual scores do not beat the raw scores, the decay-residual hypothesis is wrong and the
review's central recommendation fails.

### S7 — Site assembly

**Owner: classical, and set-valued rather than top-k.**

Four routes converge on the same failure: **ranking improves while localisation degrades**
(file 10, convergent finding 6). The teammate's learned combiner raised AUC 0.606 → 0.668 while
dropping top-5 hit rate 27.1 % → 18.6 %. PASSer2.0's own published numbers show an untrained
baseline at 84.3 % top-3 against a trained AutoML at 82.7 %. Our deliverable is a **top-5 list**,
so this is the metric that decides the submission.

File 05 proposes the reframing: **influence maximisation**. Treat the top-5 as a submodular
non-redundant *set* selection rather than a cut through a ranked score. Five residues from one
pocket is one prediction, not five. The teammate measured a related effect: spatial
diversification raised top-5 from 24.4 % to 35.6 %.

**Falsifier.** Compare a plain score cut against diversified selection on `development`, on
recall@5 and DCC. If diversification does not help, keep the score cut, which is simpler.

### S8 — Coarse-graining. The stage where the proof lives

**Owner: classical, and it must ship a theorem rather than a correlation.**

The challenge asks participants to "prove that this compression retains the essential
topological signal". Most entrants will assert. File 07 found three methods that carry real
guarantees, and file 05's strongest candidate composes with one of them exactly.

**The composition.** File 05 names effective resistance to the source as the best-fitting
observable. File 07 finds Kron reduction preserves effective resistance between retained nodes
**exactly** — an equality, not a bound (Dörfler & Bullo, arXiv:1102.2950). For that pairing the
challenge's requested proof is available in closed form.

Three conditions travel with it and none may be dropped:

- **The exactness is for effective resistance only** (`10a-fact-check.md`, claim 10). It does
  not extend to eigenvalues, eigenvectors, or a propagator.
- Kron reduction **densifies the reduced graph toward cliques**, which is a direct C3
  connectivity cost and must be reported, not hidden.
- File 07 measured instability above 50 % reduction, and file 08 requires about **35×** for
  myosin. The two files disagree at the ratio the hardware demands, and that disagreement is
  unresolved.

**The gap worth filling.** No retention theorem exists for a **unitary** propagator under
coarsening. Every guarantee found is for a Laplacian or a Markov operator. Deriving the
equivalent bound for `exp(−iHt)` is real, provable work that satisfies a named secondary
objective without requiring a quantum advantage to exist.

**Falsifier.** Sweep the compression ratio and report Loukas ε on the low eigenspace, Kendall τ
of fine-versus-lifted residue scores, and recall@5 of the known site at each ratio. If recall@5
survives to 35× on `development`, S8 is solved. If it collapses at 50 %, the hardware
demonstration is capped below myosin and the report must say so.

### S9 — Circuit synthesis. Where quantum is honest

**Owner: quantum. It is a C3 and C4 deliverable, and it is not an accuracy claim.**

The encoding is settled and exact: one qubit per residue, single-excitation sector, XY hopping,
implemented by a **Givens-rotation network** in `N(N−1)/2` two-qubit gates at depth **2N−3**
(`10a-fact-check.md`, claim 4, correcting the depth). Zero Trotter error, zero SWAP overhead,
linear connectivity only.

Three facts bound the demonstration:

- At Braket's 99.5 % median two-qubit fidelity the coherent budget is about 200 two-qubit
  gates, giving **N ≈ 20**. The largest published quantum walk on a complex graph ran at 17
  nodes; the only CTQW residue-centrality hardware run used a 9-residue peptide.
- The log₂ N compression is published and does **not** help: 9 qubits at N = 300, but
  124,844 CNOTs against a 65,529 generic lower bound.
- Classiq gives a measured 2.68× CX reduction on plain Trotter, and a Classiq co-authored paper
  states twice that its engine "could not reliably generate circuits beyond N = 16" **on
  coupled harmonic oscillators**, which is our structure (`10a-fact-check.md`, claim 5,
  confirmed verbatim). Budget for hand-written Qiskit as the fallback.

**A free contribution.** Global depolarising noise provably preserves rank order, because it is
an affine monotone map; the deliverable degrades only through a `1/λ²` shot budget. No
retrieved paper reports Kendall τ or top-k overlap between ideal and noisy node rankings
against error rate. The challenge names noise resilience as a secondary objective, and the
ranking — not the raw metric — is our artifact. That measurement is cheap, unoccupied, and
directly on a scored criterion.

### S10 — Evaluation. Frozen, and now legible

`allo.scoring.score_arm` and no other path. Nothing here may change (ADR 0025).

`09a-power-verification.md` adds one result that should be used from the first run. Mean
midrank is **exactly affine in AUC**: `R̄ = AUC·(n−m) + (m+1)/2`, and every matched patch has
size m. So the confirmatory test *is* a threshold on plain AUC — reject iff AUC exceeds the
(1−α\*) quantile of the matched patches. That critical value is computable at scoring time with
no simulation, and printing it beside every p-value makes each arm's difficulty visible before
a method runs.

---

## 2. Where AI sits, and why it is not in the table above

File 02's supervision ceiling and file 04's orchestration table agree: AI owns the ends of the
pipeline, not the middle. In this project the ends are already built or already excluded.

- **S0 is done.** Structures are frozen and hashed. No AI needed.
- **A learned scorer at S5 is out of budget.** File 02 counts the labelled allosteric data —
  ASD ~3,000 sites, ASBench 235 core, CASBench 91 — and file 09 measures the effective rank of
  the teammate's 7-feature space at **2.65**. Two independent routes bound the learnable
  component near the 14,161 parameters their GNN already used. The third route, the quantum
  parameter budget, was **withdrawn** as a misapplication (`10a-fact-check.md`, claim 3), so
  this conclusion rests on two routes, not three.
- **A learned combiner at S7 actively hurts the deliverable.** It trades top-5 for AUC, and
  top-5 is what is scored.
- **The one AI route with a clean constraint verdict is unsourced.** File 02's zero-shot
  protein-language-model result could not be retrieved by the fact-checker (claim 7). It is not
  refuted; it is unevidenced. If a DOI is found, sequence is available from
  `allo.inputs.one_letter()` and the route is legal under C1 and C2. Until then it cannot be
  planned against.

**The honest statement for the report.** This is a hybrid submission in the sense the challenge
permits, but the division of labour is decided by evidence rather than by symmetry. Naming a
stage "AI" to make the architecture diagram balanced would be the same error as naming a stage
"quantum" for the same reason.

---

## 3. What we can claim, and what we cannot

Stated now, before any method runs, so that the claims are not tuned to the numbers.

**Defensible.**

1. **A first.** No published quantum method has been scored against an allosteric ground truth
   with a null. Mohtashim et al. validate on two proteins with no labels and no null. Our
   frozen evaluation layer makes this the first such measurement, whichever way it comes out.
2. **A proof, not an assertion.** Kron reduction plus effective resistance gives exact
   retention under compression, where the challenge asks for proof.
3. **A resource budget that is real.** Exact circuit, exact gate count, exact depth, honest
   ceiling at N ≈ 20, and the cost stated rather than implied.
4. **Noise resilience measured on the ranking**, which is the artifact, and which nothing
   retrieved has measured.

**Not defensible, and the report must say so in its own voice.**

1. **Quantum advantage in accuracy.** File 09's spectral measurements explain why a walk
   collapses to eigenvector centrality on protein graphs. Claiming otherwise contradicts our
   own data.
2. **Quantum advantage in cost.** The full deliverable is 6 ms on a laptop.
3. **Coherence as a biological mechanism.** `docs/FIELD.md` trap 2 and trap 3 already commit us
   to this, and file 06 supplies the measurement: at 310 K trajectories are mutually incoherent,
   so phase relations between routes are not physical. The quantum walk is a **mathematical
   propagator with different path-summation properties**, and nothing more.

---

## 4. Pre-mortem: if this fails in six months, which assumption was wrong

Ranked by the product of how load-bearing each assumption is and how weak its current support
is.

| # | Assumption | Support today | If wrong |
| --- | --- | --- | --- |
| 1 | The decay residual carries signal (S6) | **Untested anywhere.** Rests on one selected-sample fit | The review's central recommendation fails, and S1 is the only leverage left |
| 2 | Physical edge weighting beats Cβ-10 Å (S1) | Two experimental techniques agree on the mechanism; no direct test on this task | We are left with S6 alone, and the method is ALPS with a different graph |
| 3 | Effective resistance is not insertion point 1 in disguise | **Files 05 and 00 disagree.** Cheapest decisive test in the review | The strongest new candidate is a closed one, retired in an afternoon |
| 4 | Coarse-graining survives to 35× | Files 07 and 08 disagree at exactly this ratio | Hardware demonstration capped below myosin; report says so |
| 5 | Beating `cavity_volume` is achievable | It scores 0.830 / 0.795 / 0.977 and rejects on all three arms | The submission reports a negative result against a geometric baseline |
| 6 | Long-time propagation is genuinely open | One paper's third result, untested by anyone here | The last open quantum direction closes, and S9 is purely a hardware map |

Assumptions 1, 2 and 3 are each answerable on the `development` tier in days, not weeks. They
should be answered before anything else is built.

---

## 4a. One finding that sits above the pipeline

`12-constraint-audit.md` searched for it and found nothing: **no ADR has ever vetted
`allosteric-benchmark/` against ADR 0012's four clauses.** That repository is the source of the
distance-confound measurements, the eleven closed insertion points, the diversification number
behind S7, and much of `00-conventions.md` §5.

ADR 0012 requires the tuning set to be family-disjoint and site-disjoint from every primary
target. The teammate's curated sets draw from ASD and ASBench, and ASD very likely contains
KRAS, BCR-ABL1 and cardiac myosin. If it does, then any hyperparameter this project chooses by
reading their results has been chosen with knowledge of our primary targets — which is exactly
the failure ADR 0012 exists to prevent, arriving through a route no test watches because it is
a sibling directory rather than an import.

**This does not invalidate their negative results.** A closed insertion point stays closed; a
measured confound stays measured. It bears on **tuning**, not on **elimination**. But every
number this review takes from that repository as a *design input* rather than as a *dead end*
needs the disjointness checked first, and a decision recorded.

**Recommended:** write the ADR before experiment 1, not after. It is a half-day of set
intersection and it protects every number Phase 2 will produce.

---

## 5. What to run first

Ordered by information gained per day, not by pipeline order. Every one runs on the secondary
set's `development` tier and nowhere else.

1. **Resolve the effective-resistance contradiction.** Compute Ω(source, i) and its Spearman
   correlation against the closed CTQW transfer amplitude and against eigenvector centrality.
   One afternoon. It promotes or retires the review's strongest new candidate.
2. **Test the decay residual.** Fit `exp(−k·d)` label-free per target, score the residual for
   every baseline, and compare. This tests the central recommendation directly.
3. **Test physical edge weighting.** Three graphs, S3–S7 held fixed.
4. **Print the eigenvector-centrality correlation and the critical AUC** on every arm from the
   first run onward. Both are one line and both are demanded by existing decisions.
5. **Sweep the compression ratio** with recall@5 at each step, to find where S8 breaks before
   S9 depends on it.

---

## What this changes for our pipeline

- **S1 and S6 are the two open stages that carry the method's value.** Both are classical, both
  are cheap, and neither has been tested. Phase 2 should start there rather than at S5.
- **ADR 0002 needs superseding, not accepting.** Its metric 5 survives; metrics 1–4 are closed
  by measurement. Its stated cost risk is void. Its risk list should gain the long-time
  regime as the one open direction.
- **Phase 1.4's baseline list is incomplete.** Add **Ohm**, which conditions on the active site
  as our method must, and **effective resistance to the source**, pending experiment 1. Correct
  the entry that groups AlloSite and AlloPred with training-free methods: both are SVMs.
- **Phase 4 is not a later phase.** File 08 sets the coarse-graining ratio from hardware, so S8
  gates S9. The roadmap orders them the other way.
- **The report gains two sections it can write before any method runs:** the resource budget,
  and the honest statement of what quantum cannot claim here.

## Method

No retrieval. This file is a decision built from files 01–10a, `09a-power-verification.md`, and
the repository's frozen interfaces in `src/allo/inputs.py` and `src/allo/scoring/harness.py`.
Every number traces to one of those, and every claim inherits the evidence tag it carried
there. Where two files disagree, the disagreement is recorded rather than averaged, and a
settling experiment is named. Claims corrected by `10a-fact-check.md` are marked at the point
of use.
