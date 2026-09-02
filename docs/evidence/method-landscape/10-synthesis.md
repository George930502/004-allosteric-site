# Cross-cutting synthesis of the nine-part method review

**Scope:** only what becomes visible when files 01–09 are read together — claims that three or
more files reached by different routes, places where two files disagree, the causal chain that
makes most of the findings dependent rather than independent, the routes nothing has touched,
the decision the evidence forces, and the pre-mortem for the surviving candidate. It
deliberately excludes any restatement of a single file's contents; every file's own summary is
in that file.
**Sibling files:** `00-conventions.md` (rules, hard constraints, the eleven closed insertion
points) and `01`–`09`, all of which this file cites rather than reproduces.

---

> ## Read `10a-fact-check.md` before you act on this file
>
> This synthesis was written at the same time as the fact-check, so it could not see it.
> The fact-check overturns four claims that appear below. Apply these corrections as you read:
>
> 1. **The geometric-locality theorem does not close the observable space.** It holds only for
>    **short-time** dynamics, `t = polylog(N)`. The same paper's third result "suggests a
>    super-polynomial time advantage" for **long-time** dynamics in polynomial space. A contact
>    matrix is geometrically local only under spatial indexing, and at N ≈ 300 there is no
>    asymptotic regime for the theorem to reach. Convergent finding 1 is therefore five routes
>    plus one over-read citation, and **long-time propagation is open**.
> 2. **The parameter-budget ceiling is a misapplication.** Caro's bound is a worst-case upper
>    bound on generalisation error, not a ceiling on gate count, and its `N` counts training
>    examples rather than proteins. Convergent finding 7 loses this route and keeps the other two.
> 3. **The zero-shot protein-language-model result (15/24) could not be retrieved.** Treat it as
>    unsourced, not as evidence.
> 4. **The exact-circuit depth is 2N−3, not N.** The gate count `N(N−1)/2` stands.
>
> Two qualifications that do not change a conclusion but must travel with their numbers: the
> 18.24 Å half-distance is fitted over 42 sites **selected for large effects**, and Kron
> reduction is exact for **effective resistance only**, not for eigenvalues or propagators.

---
**Retrieved:** 2026-08-25. No new literature search was run; two claims were re-checked against
their originating files only.

---

## 1. Convergent findings

Ranked by the number of **independent routes** that reach the same conclusion. "Independent"
means a different kind of argument — a theorem, a wet-lab measurement, a computation on our own
data, a field reappraisal — not two files citing the same paper.

### 1.1 A single-particle Hermitian walk on this graph carries no information beyond its transfer amplitudes — **six routes**

| #   | Route                                         | File        | The evidence                                                                                                                                                                                                                                                                                                                                              |
| --- | --------------------------------------------- | ----------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Complexity theory                             | 03 §1       | Sakamoto & Fujii, _Quantum_ **10**, 2182 (2026), doi:10.22331/q-2026-08-03-2182: for an $(r_0,\mathcal{N}(r_0))$-geometrically local matrix, short-time ($t=\mathrm{polylog}(N)$) dynamics "does not yield any exponential quantum advantage in both time and space complexities", and their Theorem 3 closes the sampling loophole `[VERIFIED-FULLTEXT]` |
| 2   | Photonics                                     | 03 §8       | Oh, Liu, Alexeev, Fefferman & Jiang, _PRX Quantum_ **5**, 020341 (2024): a graph's adjacency matrix is "nonnegative, which does not necessitate quantum interference", so GBS-on-graphs is dequantized `[VERIFIED-ABSTRACT]`                                                                                                                              |
| 3   | Continuous-variable simulability              | 03 §6.4     | An elastic network is quadratic, hence Gaussian, hence poly-time classical — Bartlett, Sanders, Braunstein & Nemoto, _PRL_ **88**, 097904 (2002) `[VERIFIED-ABSTRACT]`                                                                                                                                                                                    |
| 4   | Reservoir-computing theory                    | 04 §A.4     | "Linear reservoir dynamics can therefore redistribute features, but cannot create new fixed-delay expressive power on their own" (arXiv:2605.29071); a QELM is exactly one effective POVM (_Commun. Phys._ **6**, 118 (2023)); its useful regime "remains compatible with efficient classical simulation" (arXiv:2509.06873) `[VERIFIED-ABSTRACT]`        |
| 5   | Direct spectral measurement on our own graphs | 09 §1.3–1.4 | Over **501** contact graphs: adjacent-gap ratio ⟨r⟩ median **0.5267** (IQR 0.5163–0.5369) against a computed GOE value of **0.5317 ± 0.0154** and Poisson **0.3894 ± 0.0147**; median near-degenerate adjacency pairs within 1 % of mean level spacing = **0 of N**; (λ₁ − λ₂)/mean spacing median **25.6**, 79 % of graphs above 10                      |
| 6   | Classical wall-clock                          | 08 §10      | The entire mandated `N × N` deliverable at N = 764 takes **81.74 ms** on a laptop (`eigh` 38.79 ms + propagator 42.95 ms); N = 2000 takes 1.10 s. No crossover at N ≤ 2000                                                                                                                                                                                |

**What the convergence buys that no single route did.** Route 5 supplies the _mechanism_ the
teammate's eleven empirical closures never had: the spectrum is GOE, so there is nothing for
interference to act on, and λ₁ is isolated by 25 mean spacings, so a coherent walk collapses onto
eigenvector centrality by construction. Route 1 supplies the _theorem_ that says the eleven
closures were not a run of bad luck — geometric locality plus bounded evolution time is
_sufficient_ to remove exponential advantage whatever observable is read. Routes 2–4 show the
same wall re-deriving itself in the three branches nobody in the project had examined (bosonic CV
encodings, GBS-on-graphs, quantum reservoirs). Any one route leaves the reply "then try a
different observable" open. Together they close the observable **space**, not a list of
observables. This is the strongest result in the review.

### 1.2 The ground truth is exponentially distance-decaying, and every leaderboard number inherits it — **five routes**

| #   | Route                                                 | File          | The evidence                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| --- | ----------------------------------------------------- | ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Wet-lab deep mutational scanning                      | 06 §8         | Allosteric maps fit $y = a e^{bx}$ with $x$ = **minimum heavy-atom side-chain distance to the ligand** (not Cα–Cα). Half-distance $d_{1/2}$: GB1 **5.6 Å**, PDZ domains (median of 7 interactions) **6.9 Å**, Src kinase domain all 252 sites **7.45 Å** ($k = -0.063 \pm 0.008$ Å⁻¹), Src re-fit **8.3 Å**, KRAS (median over six binding partners) **9.50 Å**, GRB2-SH3 **13.6 Å** `[VERIFIED-FULLTEXT via publisher page, doi:10.1101/2025.06.20.660748; PMC12893324]` |
| 2   | Per-residue rank-variance decomposition on our corpus | 09 §2.1       | On 23 `targets_curated_small` structures, median $R^2 = \rho^2$ of score against minimum distance inside the candidate pool: `qfi` **0.915**, `btb_raw` **0.859**, `qasc_normlap` 0.531, `ctqw_only` **0.423**, `apop` 0.026, **`ALPS` 0.003**                                                                                                                                                                                                                            |
| 3   | Per-target plain→stratified collapse                  | 09 §2.2       | Fraction of the margin over 0.5 lost when distance is spent (curated 72–73,                                                                                                                                                                                                                                                                                                                                                                                               | Δd  | ≤ 2 Å): `qasc_baseline` **97.3 %** (p = 0.0006), `btb_raw` **91.5 %** (p = 0.0019), `ctqw_only` **84.3 %** (p = 0.0007), `ALPS` **0 %** (p = 0.906) |
| 4   | The field's own leakage-controlled reappraisal        | 01 §7         | AlloBench (Maity & Qiao 2025, _ACS Omega_ **10**, 17973, doi:10.1021/acsomega.5c01263) reports a **strong correlation between Jaccard-Index success and the inverse distance** from the predicted centroid to the known site's centroid `[VERIFIED-FULLTEXT]`                                                                                                                                                                                                             |
| 5   | Learned-model ablation, two model families            | 02 §11, 09 §9 | Handing the in-repo GNN a distance-to-anchor feature makes it **worse**: stratified AUC 0.622 → **0.595**, collapsing its margin over `ALPS` to +0.003. The learned combiner raises plain AUC 0.606 → 0.668 while top-5 hit rate **falls** 27.1 % → 18.6 % `[VERIFIED-FULLTEXT]`                                                                                                                                                                                          |

**What the convergence buys.** Route 2/3 alone say "our metric is confounded" — a defect.
Route 1 says the confound is the biology: the ground truth genuinely decays with distance, so
`ctrl_closeness` reaching plain AUC **0.6166** on curated 72 is a correct measurement of a real
law, not an artefact to be engineered away. Read together, the correct response inverts: **do not
try to beat distance with a better proximity ranker; fit the decay as the null and score the
residual.** Route 1 also supplies the number that makes that reframe viable rather than empty —
in Src, restricting the fit to _major allosteric sites only_ gives $k = -0.038 \pm 0.005$ Å⁻¹,
$d_{1/2} =$ **18.24 Å**, against 7.45 Å for all sites. Real sites decay at roughly half the
background rate. That ratio is the entire separable signal, and it is invisible from any of
routes 2–5.

### 1.3 The right observable is a perturbation of the fluctuation spectrum, not an arrival amplitude — **five routes**

| #   | Route                                                        | File        | The evidence                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| --- | ------------------------------------------------------------ | ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1   | Biophysics of dynamic allostery                              | 06 §1–2, §9 | Cooper & Dryden (doi:10.1007/BF00276625): cooperative free energies of several kJ·mol⁻¹ from changes in _frequencies and amplitudes_ of thermal fluctuations "even in the absence of a macromolecular conformational change". CAP binds its first cAMP with "no effect on the conformation of the other subunit" (doi:10.1038/nsmb1132). **A metric that ranks residues by displacement cannot see CAP-type coupling at all**                                                                                                                                                                    |
| 2   | Elimination inside ADR 0002                                  | 03 §11(c)   | Metric 5 is the only ADR 0002 candidate that is neither a proximity ranker (metrics 1–2), nor degeneracy-limited (metric 3), nor blocked by absent non-Hermitian structure (metric 4). Its cost objection is void: 300 stiffened re-diagonalisations = $8.1\times10^9$ flops, seconds                                                                                                                                                                                                                                                                                                            |
| 3   | Independent naming in the 2026 quantum-algorithms literature | 03 §6.2     | Kolotouros et al., arXiv:2601.05161 (QENM), unprompted: "by applying a small perturbation to the force constants at a given network node and analyzing the resulting shift in the eigenvalue spectrum, one can assess which residues most strongly influence the global dynamics… Those nodes whose perturbation produces the largest spectral response are identified as the most likely allosteric mediators" `[VERIFIED-FULLTEXT]`. That paragraph describes ALPS, in a quantum paper, as the classical thing the quantum algorithm is motivated by — and their algorithm does not deliver it |
| 4   | Measured ranking on our corpus                               | 09 §4, §5   | `ALPS` and `ALPS_noresid` are the only methods with mean margin over random above **+0.10** (+0.1154 and +0.1086); they take **110 of 156** subgroup contrasts across four label-bearing sets, against 7 of 156 for the entire quantum family. `ALPS` is flat across the whole tolerance sweep (0.574 → 0.570 from 0.5 Å to ∞) while `ctqw_only` and `qfi` rise with the window                                                                                                                                                                                                                  |
| 5   | Compression robustness                                       | 07 §9       | Five independent lines agree that the low-frequency modes are the robust part: Loukas Thm 3.3 is tighter for smaller eigenvalues; the MSM bound $E(\delta) \le \lambda_1(m-1)\delta^2$ is stated for the _dominant_ eigenvalues and is quadratic in projection error; 5–6 lowest Tirion modes suffice for the all-atom CHARMM slow modes; global modes retained at correlation **0.99** across a **380×** node reduction (GroEL–GroES 8015 → 21, Chennubhotla & Bahar, _Mol Syst Biol_ **2**:36); slowest mode correlation > 0.95 at N/40 (Doruker 2002)                                         |

**What the convergence buys.** File 09 alone says ALPS wins empirically, but at stratified AUC
0.5786 on curated 72 that is a thin result. File 06 says _why_ this family should be right and
why the alternative family is physically blind. File 07 says it is the mode range that survives
the compression the hardware demands. File 03 says the quantum-algorithms literature arrived at
the same readout independently and could not deliver it, which converts our classical
implementation from a fallback into the thing a 2026 quantum paper wanted. Only a cross-read
produces a metric with a physical warrant, an empirical lead, a compression-survival argument,
and a hardware story at the same time.

### 1.4 Every quantum route dies at read-in, not at propagation — **four routes**

| #   | Route                                                    | File    | The evidence                                                                                                                                                                                                                                                                                                                                                                                       |
| --- | -------------------------------------------------------- | ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Protein-specific incompressibility proof                 | 03 §6.3 | Liu, Li, Wang & Liu, arXiv:2411.03972: protein structure information "has high information entropy and cannot be compressed with a ratio better than a constant value… the matrix A is **incompressibly determined by the coordinates of N atoms**, and since the number of atoms is N, we need to load Ω(N) bits" `[VERIFIED-FULLTEXT]`                                                           |
| 2   | General counting theorem for amplitude encoding          | 04 §A.6 | arXiv:2608.08433: "the resulting Θ(N) bound is a counting theorem rather than an engineering limitation that improved hardware will remove"; 247 CNOTs at n = 8 qubits, doubling per qubit; and "the strong input models that make quantum algorithms fast on classical data also enable classical dequantization" `[VERIFIED-ABSTRACT]`                                                           |
| 3   | Generic-unitary synthesis, instantiated on our graphs    | 08 §2.3 | Shende, Bullock & Markov (arXiv:quant-ph/0406176) bounds give, at N = 300 on ⌈log₂N⌉ = 9 qubits, **124,844** CNOTs upper / **65,529** generic lower — against **44,850** for the _uncompressed_ exact Givens network. The compressed encoding is worse in gate count at every size                                                                                                                 |
| 4   | The graphene contrast, stated by the people who did both | 03 §6.2 | Kolotouros et al. chose graphene "**due to it exhibiting a periodic structure**"; their cm-scale sheet in ~160 logical qubits is bought entirely by the lattice rule. Aaronson's condition for the electrical-network algorithm is the same: it needs a network whose description "can be quickly loaded… for example, because the network has a regular pattern" (08 §2.3, `[VERIFIED-FULLTEXT]`) |

**What the convergence buys.** Each route alone reads as "wait for better hardware." Together
they say the barrier is a counting/entropy argument that hardware cannot remove — and file 04
closes the loop nobody else does: the _one_ encoding that escapes the Θ(N) bound is an
efficiently preparable state, i.e. the single-excitation position basis |i⟩, one X gate. That is
exactly the encoding whose observable §1.1 already emptied. The affordable encoding and the
informative encoding are disjoint sets.

### 1.5 Published leaderboard numbers are inflated, and the ranking itself inverts with the label convention — **four routes**

| #   | Route                                       | File        | The evidence                                                                                                                                                                                                                                                                                                                                                             |
| --- | ------------------------------------------- | ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1   | Leakage-controlled re-test                  | 01 §7       | AlloBench, 100 leakage-controlled proteins (UniRef50-declustered), 8 tools, top-1 by Jaccard Index: "**None of these programs could achieve an accuracy of more than 60 %, even with a very low JI cutoff of approximately zero**." At JI > 0.5: PASSer (Ensemble) **18 %**, APOP **15 %**, PASSer (AutoML) **13 %** `[VERIFIED-FULLTEXT, doi:10.1021/acsomega.5c01263]` |
| 2   | Apo-vs-holo split                           | 01 §7       | CAPASP (doi:10.1007/s10822-026-00831-4): PASSer and APOP lead on both subsets but "performed better with the CAPASP-General subset than with the CAPASP-Unbound subset" — i.e. both degrade on apo, the exact axis `CHALLENGE.md` scores `[VERIFIED-ABSTRACT; exact values paywalled]`                                                                                   |
| 3   | Untrained baseline inside a published paper | 02 §11      | PASSer2.0's own numbers, 204-protein test set: the **untrained** FPocket-rank geometric baseline places a true positive pocket in the top three for **84.3 %** of proteins; the trained AutoML model, **82.7 %** `[VERIFIED-ABSTRACT, doi:10.3389/fmolb.2022.879251]`                                                                                                    |
| 4   | Label-convention sign flip, measured        | 09 §2.4, §4 | On curated expert labels `ctrl_closeness` reaches plain AUC **0.6166** (72 targets); on the 4 Å-to-modulator proxy tier-B set the **opposite** control wins, `ctrl_dist` at **0.6136** (90 targets). `btb_raw` is rank 1 of 22 on curated73 plain AUC and rank 21 of 22 on tier-B plain AUC                                                                              |

**What the convergence buys.** Routes 1–3 say the numbers are too high. Route 4 says something
strictly stronger and only visible on our own data: the _ordering_ of methods inverts between two
label conventions applied to the same task, by 0.23 AUC on the same one-line geometric feature.
That means a published leaderboard cannot even be used as a prior about which method family
works. Combined with §1.2 route 1, file 06 breaks the tie: all wet-lab allosteric maps decay
_away_ from the active site, so the curated convention (sites closer than background) is the
biologically faithful one and the 4 Å-to-modulator proxy is the artefact.

### 1.6 The labelled-data supply caps a trainable model at roughly ten parameters — **three routes**

This is the shape the task brief named as an example, and it occurs exactly.

| #   | Route                                | File    | The evidence                                                                                                                                                                                                                                                                                                                          |
| --- | ------------------------------------ | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Quantum learning theory              | 04 §(e) | Caro et al., _Nat. Commun._ **13**, 4919 (2022), doi:10.1038/s41467-022-32550-3: generalisation error of a model with T trainable gates scales at worst as √(T/N). Inverting, $T \le \varepsilon^2 N$ with **N = proteins** under protein-grouped CV: at N = 150, T_max = **0** (ε = 0.05), **1** (0.10), **6** (0.20), **13** (0.30) |
| 2   | Counting the labels                  | 02 §2   | Four independent counts: ASD **1,949** allosteric protein entries / ~3,000 sites; ASBench **235** Core / **147** Core-Diversity; CASBench **91** enzymes; AlloBench **2,141** sites over **418** unique chains. Evaluable positive prevalence 1.3–2.6 % pool-wide. Conclusion: "tens of trainable gates, not thousands"               |
| 3   | Effective rank of the feature matrix | 09 §3   | `hybrid/features.npz`, 44 curated targets, 16,063 pooled residues: **8** nominal features carry effective rank **2.618** (trace/‖S‖) to **5.393** (spectral entropy). `data/combiner_features.npz`, 59 tier-B targets: 7 features, 2.645 to 5.413                                                                                     |

**What the convergence buys.** Each route is individually contestable — the bound is loose,
prevalence is not capacity, effective rank is not intrinsic dimension. Together they bracket the
same regime from theory, from data volume and from data geometry, and the measurement lands
exactly where all three predict: the in-repo VQC with **24 trainable parameters** on 44
protein-grouped targets scored stratified AUC **0.575**, against logistic regression **0.596** on
identical features (paired p = 0.39) and against **0.576** for unlearned `ALPS`. Twenty-four
parameters bought nothing over one hand-designed score. File 04 adds the corollary that surprises:
**barren plateaus are not the binding constraint** — at a ~10-gate budget no circuit is deep
enough to have one. The label supply, not the optimiser, closes the door.

### 1.7 Ranking and localisation dissociate, and nothing localises — **four routes**

| #   | Route                                                 | File   | The evidence                                                                                                                                                                                                                                                                                                    |
| --- | ----------------------------------------------------- | ------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | In-repo, learned combiner                             | 02 §11 | Plain AUC 0.606 → **0.668** while top-5 hit rate **falls** 27.1 % → 18.6 % (proxy-label protocol); corrected re-run 0.576 → 0.603, +0.027, p = 0.72                                                                                                                                                             |
| 2   | Published, different lab and model family             | 02 §11 | PASSer2.0: precision/recall/F1 all improve over the untrained rule, but top-3 localisation does not lead (84.3 % untrained vs 82.7 % trained)                                                                                                                                                                   |
| 3   | Localisation metrics measured across the whole corpus | 09 §6  | Curated 73, top-5 hit rate: best is `apop` **0.132**, then `ALPS_noresid`/`btb_raw` 0.123, `ALPS` 0.082, `ctrl_random` 0.041. **DCC** (top-5 centroid to true-site centroid): best median **22.1 Å** (`ctqw_only`) against `ctrl_random` **23.3 Å**; fraction meeting ≤ 4 Å is **0.000–0.019 for every method** |
| 4   | Same trap on a zero-parameter geometric detector      | 02 §12 | Our own `cavity_volume` baseline rejects the statistical null at p = 0.0003 on one arm while `recall@5` is **0.00 on all five primary arms**, and on that same arm the predicted centre was farther from the true site than a random five-residue list                                                          |

**What the convergence buys.** Route 4 reframes the whole thing: the dissociation is not an AI
pathology, it is structural to a task with 1.3–8 % positive prevalence. And routes 1–3 together
say the metric the challenge actually scores — `CHALLENGE.md` §5's top-5 hit list — is the metric
on which **no method anywhere in this review, classical, AI or quantum, has been shown to beat a
baseline**. Every method file argues about AUC. The deliverable is not AUC.

### 1.8 The coarse-graining ratio is fixed by hardware, not by methodology — **three routes**

| #   | Route                                   | File             | The evidence                                                                                                                                                                                                                                                                                                                     |
| --- | --------------------------------------- | ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Device calibration arithmetic           | 08 §5.3          | At the 99.5 % median two-qubit fidelity Braket's IQM Emerald/Garnet and Rigetti Ankaa-3 (fSim) deliver, the coherent budget is $G^\* = 1/p = 200$ two-qubit gates; the exact Givens network costs $N(N-1)/2$, so $N \approx$ **20** (22 on IonQ Forte at 99.6 %, 15 on Rigetti Cepheus at 99.1 %)                                |
| 2   | Two independent published hardware runs | 08 §5.3, 03 §3   | The largest published quantum walk on a complex graph: **17 nodes, 20 edges, 40 qubits**, Hellinger fidelity > 0.87 over 7 steps (arXiv:2602.24053). The only published CTQW residue-centrality hardware run: a **9-residue** peptide (oxytocin, 1XY1) on 4 qubits, with the 150-protein study simulator-only (arXiv:2604.17486) |
| 3   | Our own measured sizes                  | 08 §1.1, 09 §1.1 | Frozen arms at an 8 Å Cβ cutoff: KRAS 169, BCR-ABL1 272/451, cardiac myosin **764**. Across 501 graphs, median N = 405, range 118–2072, mean degree 17.95 at a 10 Å cutoff                                                                                                                                                       |

**What the convergence buys.** File 07 was choosing a compression ratio on methodological
grounds — an SSE-level map at roughly 10–20×, which it calls "the defensible starting ratio."
File 08 says the hardware requires **~35×** for myosin (764 → 20). File 07's own cited evidence
measures $\varepsilon < 1$ only at $r \le 70\,\%$ (roughly 3×), with the eigenvalue error jumping
"by almost an order of magnitude whenever $r$ increases by 20 %". Neither file states the
resulting constraint: **the compression the hardware demands sits roughly an order of magnitude
beyond where the retention literature has measured anything, and no coarsening benchmark
retrieved includes a residue contact graph at all.**

### 1.9 The remaining legal information is in the graph's edges, not in the propagator — **three routes**

| #   | Route                                                    | File       | The evidence                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| --- | -------------------------------------------------------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Two orthogonal experimental classes agree on the carrier | 06 §5, §12 | Vibrational energy transfer with a placed injector and sensor on a Trp-zipper β-hairpin: "even if cutting short backbone stretches of only 3 to 4 amino acids in a protein, **hydrogen bonds are the dominant VET pathway**" `[VERIFIED-FULLTEXT, PMC8172543]`. Independently, the complete allosteric map of a small GTPase finds propagation "more efficient across the sheet than along the backbone within a strand" `[VERIFIED-FULLTEXT, PMC10866706]`. Contact transfer rates scale as 1/(contact distance)², validated on PDZ3 (doi:10.1063/1.5140070) |
| 2   | C2 compliance turns on the edge weight, not the metric   | 01 §3      | Sethi 2009's dynamical network analysis is a **C2 violation as published** because its correlation matrix is MD-derived; the identical recipe is clean with ENM covariance $\propto \Gamma^{-1}$ — "the MD vs. ENM choice of edge weight is what decides C2 compliance, not the centrality metric itself"                                                                                                                                                                                                                                                     |
| 3   | Legal ways to enrich the graph exist and are unused      | 05 §3, §6  | MD-free ensemble generators (Str2Str, ENM/NMA-guided sampling, AF2 MSA-subsampling) convert one binary contact map into a fluctuation-aware weighted graph — "a strictly larger input for the same C1/C2 budget". GNM-analytic transfer entropy supplies **directed, asymmetric** edge weights in closed form, with no trajectory                                                                                                                                                                                                                             |

**What the convergence buys.** Files 03, 08 and 09 independently conclude the propagator is
exhausted. Files 01, 05 and 06 independently point at the _graph_ as where legal information
remains. Read together they relocate the Phase 2 decision from "which propagator" to "which
graph" — and file 06 adds that this stays inside C6, because assigning a class weight to a
contact is a refinement within the elastic-network hypothesis, not a departure from it.

---

## 2. Contradictions

Stated with both positions and the evidence that would settle each. Not averaged.

### 2.1 File 01 contradicts the conventions' own "already known" section on the apo/holo ENM bar

- **Conventions §6, as originally written.** ESSA's apo top-3 of **7/14 = 50 %** (Dataset II, 24
  structures / 12 proteins at ≥ 90 % sequence identity, doi:10.1016/j.csbj.2020.06.020) is the
  field's clean apo-versus-holo comparison.
- **File 01 §2, §8(a).** APOP reports, on what its own text describes as essentially the same
  matched set, apo top-3 of **11/15 = 73 %**, restated elsewhere in the same paper as **86 %
  = 11/14**, with holo at 15/15 = 100 % (doi:10.1093/bioinformatics/btad275)
  `[VERIFIED-FULLTEXT]`. Markedly higher than ESSA on a similar unsupervised GNM-plus-pocket
  recipe.
- **Status.** Conventions §6 already carries the correction, dated 2026-08-25. But file 01 flags
  that APOP's own paper is internally inconsistent — the 15-vs-14 denominator discrepancy "is
  exactly as extracted and was not resolved against the primary PDF this session."
- **What would settle it.** Fetch the APOP primary PDF and resolve the denominator. **Low
  stakes**: AlloBench re-tests APOP at **15 %** at JI > 0.5 on 100 leakage-controlled proteins, so
  neither the 73 % nor the 86 % survives as a bar. Do not quote either in the report.

### 2.2 Two incompatible definitions of the bar the method must clear — conventions §6 versus file 09 §8

- **Conventions §6.** The bar is four comparative numbers: `−distance` at AUC 0.617,
  `cavity_volume`, eigenvector centrality, and the APOP/ESSA unsupervised-ENM bar.
- **File 09 §8.** Our own frozen protocol's matched-patch permutation test reaches 80 % power only
  at Cohen's d between **0.80 and 1.89** (median 0.88) over 60 arm × λ × Holm-level cells,
  corresponding to an achieved **AUC of 0.762 to 0.961** (median 0.879). The best confound-free
  number measured anywhere in the corpus is **0.59**.
- **The disagreement.** These are different objects: §6 is _comparative_ (beat these methods),
  file 09 is _absolute_ (reject the null with our own frozen test). A method can clear all four of
  §6's numbers and still fail to reject at any conventional level, and on the current evidence
  that is the expected outcome.
- **What would settle it.** Nothing empirical — it is a reporting decision, and it must be made
  before a number is produced. File 09's recommendation is the defensible one: **state the
  sensitivity band before stating a result**, and plan the report around an honest non-rejection.
  Averaging the two bars would produce a number that answers neither question.

### 2.3 Three files assign three different confidence levels to the same published quantum precedent

- **Conventions §5.** "A published quantum result already exists" — Mohtashim, Sajjan & Kais,
  _JACS_ 2026, doi:10.1021/jacs.6c08053: CTQW centrality on residue interaction networks over 150
  proteins showing "consistently strong agreement with classical eigenvector centrality."
- **File 03 §11(d).** "Its validation is anecdotal, not a benchmark": biological relevance
  confirmed through recovery of functional residues in **protein kinase A and oxytocin** — "Two
  proteins, functional residues, no allosteric labels, no AUC, no null. ADR 0002's reading stands
  and is if anything understated."
- **File 08 §5.4.** Reports Spearman ρ 0.582–1.000 (median ~0.964) and Kendall τ 0.491–1.000
  (median ~0.867) against classical eigenvector centrality — "**But that agreement is
  simulator-versus-classical.** They report **no** Kendall τ between the simulator ranking and the
  hardware ranking, no noise model, and no error rate. The hardware demonstration is one
  9-residue peptide at 1024 shots."
- **File 09 §1.4.** Tags the paper's own numbers `[UNVERIFIED]` because the full text was not
  retrieved, while supplying the isolation statistic (λ₁ − λ₂ = 25.6 mean spacings) that explains
  the agreement mechanistically.
- **What would settle it.** Retrieve the _JACS_ full text (not open access in any session). Until
  then the report must say what files 03 and 08 say, not what conventions §5 says: the precedent
  exists, agrees with a one-line classical quantity, and has never been scored against allosteric
  labels with a null.

### 2.4 Is ENAQT closed, or was it tested under conditions where the mechanism cannot appear?

- **Conventions §5 item 3, and file 09.** Closed by measurement: no optimum over γ from 0 to
  3·J_max. File 09 §2.1 measures `enaqt` at ρ = +0.009 against distance (R² 0.002), plain AUC
  0.517, stratified 0.508 — uncorrelated with distance and uninformative.
- **File 03 §5.** The measurement stands but the _mechanism_ explains it away: ENAQT requires
  site-energy disorder **and** a source–sink gradient. Zerah-Harush & Dubi, arXiv:1801.06799:
  "we find a **geometric condition on the network** for the appearance of ENAQT", and decisively,
  "So far as the symmetric linear chain is considered, **no ENAQT is observed**"
  `[VERIFIED-FULLTEXT]`. Our C6 Hamiltonian has uniform on-site energies and no sink. "The flat
  γ curve was not a null result about proteins; it was the predicted behaviour of a model with no
  density gradient and no disorder."
- **File 06 §11, and its observable 5.** Goes further and names the untested variant: "ENAQT was
  tested as a _tunable_ γ and failed, but the **ballistic fraction** as an effector-response
  readout was not tested." Motivation is a direct measurement: in bovine serum albumin, without the
  effector the ballistic (10 ps) and diffusive (29 ps) phases are "of nearly equal amplitude", but
  with sodium myristate bound at the distal site the decay is "**dominated (75 %) by the ballistic
  (10 ps) component**" `[VERIFIED-FULLTEXT, PMC3949117, doi:10.1038/ncomms4100]`.
- **The disagreement.** File 03 says the branch is mis-tested but un-reopenable, because adding a
  sink or disorder requires chemistry C6 excludes. File 06 says one specific apo-versus-clamped
  ratio is both untested and physically motivated, and needs no added chemistry.
- **What would settle it.** One extra column: define the ballistic fraction on the residue graph
  as the ratio of unitary to diffusive transfer at matched time, compute it apo and site-clamped
  on the curated set, score it under distance-stratified AUC. Note that file 09's `enaqt` result
  is **not** evidence against this, because it measured a different quantity (γ-swept efficiency,
  not an apo/clamped ratio). Cheap, and it is the only place the eleven closures leave room.

### 2.5 Files 02 and 05 give opposite verdicts on the protein-language-model route

- **File 05 §5, and conventions §5.** Closed. "Already tried and already failed here: conventions
  §5 records that protein language models collapse on allosteric sites (AUPR 0.64–0.76 on
  orthosteric vs **0.06** on allosteric in the same proteins)." File 05's pipeline list says
  explicitly: "do not re-benchmark protein-language-model mutational sensitivity as an allostery
  baseline."
- **File 02 §4, §9, §10.** The zero-shot attention route is "the cleanest C1/C2 survivor in the
  whole review" and "ready to prototype today at effectively zero labelled-data cost": ESM-1b beat
  a random null in **15/24** proteins (p < 0.05 by permutation) on a curated benchmark, against
  Ohm at **7/24** and EVcouplings at **5/24**, with EVcouplings additionally failing outright on
  8/24 for MSA depth `[VERIFIED-ABSTRACT, bioRxiv 2024.10.03.616547]`. File 02 also challenges the
  scope reading: "nothing in the six hard constraints bans using a protein's own apo **sequence**."
- **Partial resolution, and what remains.** The two files are largely discussing different objects
  — file 05/conventions means _mutational-sensitivity scoring_ (ESM-1v log-odds aggregated per
  residue); file 02's route 1 means _attention maps_ with zero fine-tuning. But the disagreement is
  not fully dissolved, because the numbers are not comparable and the review's own rule says so:
  AUPR 0.06 was measured on allosteric sites at < 3 % prevalence, while 15/24 is "beats a random
  null by permutation" on a different 24-protein set with a different criterion.
- **What would settle it.** Run the ESM-1b attention-head route on the _same_ label set that
  produced the AUPR 0.06, and report AUPR against its own prevalence line, top-5 hit rate and DCC
  (file 02 §12's own reporting standard). No training, one inference pass.

### 2.6 Is effective resistance a new candidate or closed item 1 under another name?

- **File 05 §(a).** Effective resistance to a named source,
  $\Omega(s,i) = L^+_{ss} + L^+_{ii} - 2L^+_{si}$, is "the strongest fit" and "the strongest
  candidate in the whole file": a source-to-every-node ranking by construction, equal up to
  graph-volume normalisation to random-walk commute time, needing only contact topology and edge
  weights. File 05 flags its own caveat: "some quantum-walk literature ties CTQW hitting times to
  resistance distance directly, which would collapse it back into item 1."
- **File 03.** Does not name it, but its table closes quantum communicability
  $(e^{-iHt})_{ij}$ as "same matrix function as item 1", and the Sakamoto & Fujii theorem covers
  any geometrically local linear dynamics on this matrix.
- **File 07 §1.3.** Supplies the fact that makes it attractive independently of any quantum
  reading: Kron reduction preserves effective resistance between retained nodes **exactly** (Dörfler
  & Bullo Thm 8) — the only exact preservation theorem in the whole coarsening review — and commute
  time is $2m$ times effective resistance, which is Chennubhotla & Bahar's own propagation measure.
- **File 09.** Does not measure it. There is no resistance row in the §2.1 confound table or the
  §4 ranking.
- **What would settle it, and it is the cheapest decisive test in the review.** One pseudo-inverse
  of the Laplacian, one column, the existing harness. If $\Omega(\text{active site}, i)$ lands near
  `ctqw_only`'s stratified 0.5154 it is item 1 in disguise; if it lands near `ALPS`'s 0.5782 it is
  not. Hours of work, and it resolves a live disagreement between three files.

### 2.7 File 09 corrects the conventions' wording on multimer degeneracy

- **Conventions §5 item 7.** "Degeneracy readouts on symmetric multimers — symmetry enriches
  degeneracy, the readout still loses."
- **File 09 §1.3.** The benchmark's own degeneracy statistic is **scale-dependent**:
  `multimer_ablation.py::degeneracy` takes the 20 lowest non-zero Kirchhoff eigenvalues and counts
  relative gaps $s_i/\lambda_i < 1\,\%$. Reproduced exactly (3.63 % tier B against the README's
  3.6 %; 4.61 % multimers) — but near the top of the spectrum λ ≈ 34 and s ≈ 0.05, so $s/\lambda$
  is small for reasons unrelated to degeneracy, and the same rule over the whole spectrum returns
  **79–91 %**. Read scale-free, the near-degeneracy fraction is **0.06 % in all three groups,
  monomer and multimer alike**.
- **Status.** The verdict survives; the wording does not. "Symmetry enriches degeneracy" is true
  only of the low-mode end under a scale-dependent statistic, and it is exactly the sentence
  someone will quote as a reason to retry a degeneracy readout. File 09 §7.3 confirms the ordering
  independently: on 60 multimer targets the plain eigenvalue shift `dlam` (ALPS's own observable)
  leads at mean AUC 0.694, above `dpart` 0.671, `dgap` 0.656 and `dipr` 0.639 — though that file
  carries no random or geometric control, so only the ordering is interpretable.
- **What would settle it.** Nothing further is needed. Amend the wording in conventions §5 item 7
  to "symmetry enriches the low-mode gap statistic; the spectrum remains GOE and the readout still
  loses."

### 2.8 File 07 disagrees with itself about how far compression can go, and file 08 forces the question

- **Optimistic position (07 §3.5, §9).** Global modes retained at correlation **0.99** across a
  380× node reduction; B-factor correlation **improving** from 0.68 (full 8015 residues) to 0.89
  at level 3 (c = 133); five independent lines that low-frequency modes are the robust part.
- **Cautious position (07 §4, §9, §11).** Loukas measures $\varepsilon < 1$ only at $r \le 70\,\%$,
  with mean relative eigenvalue error on the 10 lowest eigenvalues going 0.003 / 0.034 / **0.406**
  at $r = 30/50/70\,\%$ on a 1458-node yeast PPI graph; Kron reduction shows "numerical instability
  above $r = 50\,\%$"; **no coarsening benchmark retrieved includes a residue contact graph**; and
  **no retention theorem is stated for a unitary propagator** at all.
- **File 08 §5.3** requires $r \approx 97\,\%$ for myosin.
- **What would settle it.** File 07 §8 already names both instruments and neither has been run:
  the Loukas $\varepsilon$ on $R = U_k$, and — the one that actually proves retention of the
  _answer_ rather than the _operator_ — recall@5 at each ratio. Sweep at $r$ = 50/70/90/95/97 % on
  our own arms, densely, and do not assume monotone decay (07 §9 records a protein case where
  coarse-graining improved agreement with experiment).

---

## 3. The causal chain

Most of the nine files' findings are not independent. Below, root causes first; each subsequent
level is entailed by the one above. Fixing a root moves everything under it; fixing a consequence
moves nothing.

### 3.1 The root layer — five facts, none downstream of any other

**R0. A folded protein's contact graph is generic three-dimensional geometry — not a designed
system, not a periodic one.** This is the deepest fact, and it has two independent faces that
between them cause most of the review.

> **R1 (algebraic face).** The matrix is real, symmetric, non-negative, sparse (mean degree
> 17.95, density 0.0435 at a 10 Å Cβ cutoff), geometrically local, harmonic under C6, with a
> GOE spectrum (⟨r⟩ 0.5267) and a top eigenvalue isolated by a median of 25.6 mean spacings.
> `[09 §1.1–1.4, measured on 501 graphs]`
>
> **R2 (informational face).** The matrix's entries are _data_, not a rule: "incompressibly
> determined by the coordinates of N atoms", requiring Ω(N) bits to load.
> `[03 §6.3, arXiv:2411.03972, VERIFIED-FULLTEXT]`

**R3. The biological ground truth decays exponentially with distance from the active site**,
$d_{1/2}$ = 5.6–13.6 Å across five systems, and 18.24 Å versus 7.45 Å for major sites versus
background in Src. `[06 §8]`

**R4. The field's labelled supply is 90–265 unique proteins at 1.3–3.8 % positive prevalence.**
`[02 §2; 09 §1.6]`

**R5. Two-qubit fidelity on the provided platform is 99.0–99.6 %.** `[08 §5.3]`

### 3.2 What R1 causes, on its own

R1 → no interference structure available → **conventions §5 items 2, 4, 5, 7 are all one
finding**: time-averaged transfer, level-spacing degeneracy, eigenvector content/IPR, and the
multimer degeneracy ablation are four measurements of the same absent property.

R1 → λ₁ isolated → a coherent walk's long-time and time-averaged amplitudes are dominated by the
principal eigenvector → **conventions §5 item 1 (CTQW is a proximity ranker) and the published
Mohtashim result (CTQW reproduces eigenvector centrality) are the same fact, not a finding and its
independent validation.** This link is stated in none of the nine files as a single sentence, and
it changes how the precedent should be cited: the published quantum result is a **diagnosis of our
substrate**, not a validation of the method.

R1 (non-negativity) → GBS-on-graphs dequantized `[03 §8]`.
R1 (symmetry) → no non-reciprocal hopping, no gain/loss → conventions §5 item 11 `[03 §2]`.
R1 (couplings fixed by geometry) → the entire perfect/pretty-good state-transfer literature is
inapplicable, because every result there is a _design_ theorem whose input is a target fidelity
and whose output is a coupling pattern `[03 §4]`.
R1 (harmonic, from C6) → Gaussian → CV/bosonic encoding classically simulable `[03 §6.4]`.
R1 (linear, structured, low-magic) → QRC/QELM collapses to a fixed random feature map plus ridge
regression `[04 §A.4]`.
R1 (geometric locality + bounded time) → Sakamoto & Fujii `[03 §1]`.
R1 (no two-body term available under C6) → the only genuinely hard row in file 03's simulability
table is the one nothing in the physics supplies `[03 §11(a)]`.

**R1 alone explains eight of the eleven previously closed insertion points plus four branches
newly closed in this review.**

### 3.3 What R2 causes, on its own

R2 → the ⌈log₂N⌉ encoding is a generic SU(2ⁿ) element → 124,844 CNOTs against a 65,529 generic
lower bound at N = 300, worse than the uncompressed 44,850 `[08 §2.3]`.
R2 → every oracle-based result (qubitisation, QSP, sparse Hamiltonian simulation, Babbush's
coupled oscillators) is query-optimal but not gate-optimal, because the query is the expensive
object `[08 §3.4; 03 §7]`.
R2 → amplitude encoding is a Θ(N) counting theorem, and the same strong input models enable
dequantization `[04 §A.6]`.
R2 → once Ω(N) is paid, more has been spent than the $O(N^3) = 2.7\times10^7$ flops of
diagonalising the 300 × 300 Kirchhoff matrix outright `[03 §6.3]`.

**R1 ∧ R2 is a pincer, and it is the whole quantum negative result in two facts.** R2 says the
only affordable encoding is the single-excitation position basis |i⟩ (one X gate). R1 says that
encoding's observable is empty. The affordable encoding and the informative encoding are disjoint
sets. Neither file 03, 04 nor 08 states this in one place; each holds one jaw.

### 3.4 What R3 causes

R3 → `ctrl_closeness` at plain AUC 0.6166 is a correct measurement of a real law `[09 §2.4]`.
R3 → any monotone-in-distance score lands on the distance control `[06 §9]`.
R3 → the plain/stratified collapse: btb_raw loses 91.5 %, ctqw_only 84.3 %, qasc_baseline 97.3 %
of their margin `[09 §2.2]`.
R3 → AlloBench's JI correlates with inverse distance, so the field's own benchmark inherits the
same confound `[01 §7]`.
R3 → a learned model handed a distance channel latches onto it and generalises worse
(GNN 0.622 → 0.595) `[02 §11; 09 §9]`.
R3 → plain AUC is not a usable endpoint, and the sign of the confound depends on the label
convention `[09 §2.4]`.

### 3.5 What R4 causes

R4 → $T \le \varepsilon^2 N$ = 6 gates at N = 150, ε = 0.2 → the 24-parameter VQC's 0.575 was
predicted, not discovered `[04 §(e), §A.2]`.
R4 → barren plateaus are **not** the binding constraint; at ~10 gates no circuit is deep enough
`[04 §(e)]`.
R4 → any learned coarsening (the Guided Graph Compression pattern, which moved a classifier from
0.5797 to 0.8645 by making compression task-guided) is unaffordable here **and** would risk C1
`[04 §B.3]`.
R4 → every large-model route must be frozen-backbone-plus-tiny-head or zero-shot `[02 §6, §9]`.
R4 → accuracy is a useless metric at this prevalence; the hybrid folder records 0.967 for two
classifiers both predicting all-negative `[09 §1.6]`.

### 3.6 What R5 causes

R5 → coherent budget 100–250 two-qubit gates → $N(N-1)/2 \le 200$ → N ≈ 20 `[08 §5.3]`.
R5 → myosin needs ~~35× compression, so **file 07's ratio is set by file 08, not by
methodology** `[§1.8 above]`.
R5 → no full-N hardware run on any axis: qubit count (Braket's largest gate-based device is 108
against a smallest arm of 169), fidelity, Ankaa-3's fixed 20,000-gate ceiling, or cost (~~$33,000
for myosin at N circuits × 1e5 shots on the cheapest device) `[08 §7.1]`.
R5 ∧ the mitigation lower bounds (Takagi et al., _PRL_ **131**, 210602 (2023); Quek et al.,
_Nature Physics_ **20**, 1648 (2024)) → sampling overhead is exponential in depth **by theorem**,
so error mitigation "does not buy back the factor of 8–38 in N" `[08 §5.5]`.

### 3.7 The smallest set that explains the most

**{R1, R2, R3}.** Between them:

- R1 accounts for essentially all of files 03 and 04 — every closed observable, every closed
  branch, and the reason the published quantum precedent agrees with a one-line classical
  quantity.
- R2 accounts for file 08 §2–§3 and file 04 §B.4 — every encoding failure and every
  "query-optimal is not gate-optimal" result.
- R3 accounts for most of files 01, 02 §11–§12 and 09 §2 — every leaderboard number, the
  plain/stratified collapse, the GNN ablation, AlloBench's JI-vs-distance correlation, and the
  label-convention sign flip.

R4 and R5 are genuine roots but govern narrower subtrees (the learned arms; the hardware demo
size).

**The actionability asymmetry, which is the point of building the chain.** R1 cannot be fixed
without leaving C6 — every escape (a two-body term, non-Hermitian structure, site-energy disorder)
requires physics the challenge's own modelling assumption excludes. R2 cannot be fixed at all; it
is a counting theorem. R5 can only be worked around by compression whose retention nobody has
bounded for a unitary propagator. R4 can be sidestepped only by refusing to train.

**R3 is the only root with an actionable downstream**, and the action is not "beat distance" but
"fit the decay as the null and score the residual" — with file 06's Src ratio (18.24 Å versus
7.45 Å) as the evidence that something is in the residual to find. That, plus §1.9's relocation of
the remaining information into the edge weights, is the entire constructive content of nine files.

---

## 4. What is genuinely unexplored

Every route flagged as not retrieved, not attempted, or without published precedent. Judged for
_why_ — and the honest majority verdict is that the network-science block is unexplored because
the mathematics has nothing to discriminate with on this substrate.

### 4.1 The measurement that should make you sceptical of most of this section

File 09 §1.5, over 240 labelled targets: **67.9 % of labelled targets have a label residue within
2 hops of the active site, and 87.9 % within 3.** In Euclidean terms (328 targets) the median
distance from the active site to the nearest label residue is **13.8 Å**. On a graph of mean degree
18 and diameter 10, a two-hop neighbourhood is already a large fraction of the protein.

> **There is no long-range transport problem here for a propagator to solve.**

That single number, present in file 09 and in none of the files proposing transport-flavoured
routes, is the reason to be sceptical of target control, source localisation, spectral graph
wavelets and phonon-mode classification _all at once_. Any method whose selling point is transport
distance, path structure or control reachability has essentially no path to work with.

### 4.2 Survives the scepticism — worth a cheap decisive test

| Route                                                                                                                                                                                                                                                                      | Flagged by                                                                                                                                                                          | Why unexplored                                                                                                                                                                                                  | Cheapest decisive test                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Influence maximization** as the construction of the top-5 list (Kempe, Kleinberg & Tardos, KDD 2003) — a submodular seed set maximising _joint_ expected influence, instead of five independently top-scoring residues that may be five neighbours reporting one channel | 05 §7, "not retrieved as applied to protein allostery, and not retrieved as a reframing of any top-k allosteric hit list"                                                           | **Nobody happened to try it.** It comes from social-network science and nobody has connected it to a hit-list deliverable                                                                                       | Re-derive the top-5 from an existing score (`ALPS`) by greedy submodular selection with a redundancy penalty; rescore recall@5 and DCC on curated 73 against the current top-5-by-score cut. **Hours.** Highest expected value in the review: it attacks the deliverable's _construction_, and §1.7 says the deliverable is where every method fails (best recall@5 = 0.132; DCC ≤ 4 Å on 0.000–0.019 of targets)                                                                                                                                                                                           |
| **GNM-analytic transfer entropy** as a source of _directed_ edge weights (doi:10.1021/acs.jpclett.3c00366; bioRxiv:084764, "calculation times… in seconds")                                                                                                                | 05 §6 and 06 §10, independently                                                                                                                                                     | **Nobody happened to try it here.** The method is published; nobody connected it to conventions §5 item 11                                                                                                      | Compute TE(active site → i) and TE(i → active site) on curated 73 as two stratified-AUC columns, and report their correlation with the existing Γ⁻¹-derived columns. **The only route in the review that could legally reopen a closed branch**: conventions §5 item 11 says a real symmetric graph has "neither non-reciprocal hopping nor gain and loss", and this supplies the first without MD. Physical warrant is strong — file 06 §10 measures a ≥ **sixfold** difference in Src decay rates by direction ($d_{1/2}$ 19.80 Å toward helix αC versus **3.22 Å** toward the regulatory-domain surface) |
| **Effective resistance to the active site**, $\Omega(s,i)$, as a named baseline                                                                                                                                                                                            | 05 §(a), "not retrieved as a stated baseline anywhere in this search"                                                                                                               | **Nobody happened.** The mathematics is latent inside GNM's Γ⁻¹ and inside PRS, so nobody named it                                                                                                              | One Laplacian pseudo-inverse, one column. Resolves contradiction §2.6. **Hours.** Be sceptical: file 05 flags its own collapse risk to conventions §5 item 1                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| **Edge weighting by hydrogen-bond / side-chain-contact class, with contact rates ∝ 1/d²**                                                                                                                                                                                  | 06 §12, called "the highest-value change identified in this review"                                                                                                                 | **Nobody happened.** The ENM tradition uses uniform springs — that is Tirion's whole point                                                                                                                      | Rebuild the contact graph with class weights and 1/d² rates, rerun the existing arms. Sceptical note: because it departs from Tirion's demonstrated sufficiency, it must be **shown** to beat the uniform-spring graph on the same endpoint                                                                                                                                                                                                                                                                                                                                                                 |
| **Ballistic fraction as an apo-versus-clamped readout**                                                                                                                                                                                                                    | 06 §11 observable 5, "the one place where the eleven closed insertion points leave room"                                                                                            | **Nobody happened.** ENAQT was swept as a tunable γ, not read as an apo/clamped ratio                                                                                                                           | One extra column, existing harness. See contradiction §2.4                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| **Equivariant classical GNN** at matched parameter count                                                                                                                                                                                                                   | 04 §A.3, "the _only_ structural lever with published evidence behind it: **equivariance, not quantumness**"                                                                         | **Nobody happened here.** The evidence is from high-energy physics                                                                                                                                              | Swap the in-repo GNN's message-passing layer for an E(3)-equivariant one at matched parameters, same 96 protein-grouped folds. Published matched-comparison margin: classical EGNN **+4.5 AUC points** over plain GNN (Axioms **13** (2024) 160, arXiv:2311.18672, Table 1: GNN 5122 params / 63.36 %, EGNN 5252 / 67.88 %)                                                                                                                                                                                                                                                                                 |
| **A retention theorem for a unitary propagator**                                                                                                                                                                                                                           | 07 §11, "**None of them is stated for a unitary propagator** exp(−iHt)"                                                                                                             | **Nobody happened.** The coarsening literature is classical; the quantum literature does not coarse-grain                                                                                                       | It is a _derivation_, not an experiment: one page of continuity argument from Loukas Theorem 3.3 to our metric with explicit t-dependence. Note the asymmetry that argues for the metric choice — the derivation is easy for a spectral-shift readout and hard for a long-time arrival-amplitude one, where "small eigenvalue errors compound as exp(−i δλ t)". Directly answers `CHALLENGE.md` §4.2's "prove" clause where the literature has nothing                                                                                                                                                      |
| **Rank-order stability of graph-node scores under gate-level hardware noise**                                                                                                                                                                                              | 08 §5.4: "there is no established literature." Explicit negatives: arXiv `abs:"PageRank" AND abs:"decoherence"` → **0** results; `abs:"Kendall" AND abs:"quantum computer"` → **0** | **Nobody happened.** It falls between quantum computing and network science                                                                                                                                     | **The measurements already exist** (08 §5.1 shot-versus-λ table tracking 1/λ²; §6.1 shot budgets). Register them under `docs/playbooks/experiment.md`. A contribution for the cost of paperwork                                                                                                                                                                                                                                                                                                                                                                                                             |
| **The ASD/ASBench/CASBench target-overlap check** for KRAS G12C, BCR-ABL1, cardiac myosin, c-Myc and the nine secondary targets                                                                                                                                            | 02 §3, "the single highest-value follow-up this file did not complete"                                                                                                              | **Blocked by a search quota**, not by difficulty                                                                                                                                                                | One query against ASD's protein list. **Hours.** Gates whether _any_ external pretrained artifact is usable; until it is done, every "Legal\*" row in file 02 §3 is a reasoned risk, not a checked fact                                                                                                                                                                                                                                                                                                                                                                                                     |
| **Loukas ε and recall@5 on a residue contact graph at high compression**                                                                                                                                                                                                   | 07 §4: "**No residue contact graph appears in any coarsening benchmark retrieved by this search**"; 07 §11: no coarse-graining designed for quantum hardware retrieved              | **Nobody happened.** The coarsening literature benchmarks meshes, infrastructure and PPI graphs                                                                                                                 | Run local-variation (neighbourhood) contraction on our own arms at r = 50/70/90/95/97 %, report ε, mean relative eigenvalue error at k = 10 and k = 30, eigenspace angle ‖sin Θ‖_F, **and recall@5**                                                                                                                                                                                                                                                                                                                                                                                                        |
| **Mode composition of the chosen metric**                                                                                                                                                                                                                                  | 07's own pipeline note 5: "Cheap to run, expensive to skip"                                                                                                                         | **Nobody happened**                                                                                                                                                                                             | Decompose the metric over the eigenspectrum on one target. If it is not slow-mode dominated, every retention guarantee in file 07 §1 becomes inapplicable and the coarse-graining plan needs rebuilding                                                                                                                                                                                                                                                                                                                                                                                                     |
| **Binary/Gray-code synthesis depth for a real contact graph**, and **Classiq synthesis wall-clock at our sizes**                                                                                                                                                           | 08 §9.1 `unknown` cells: "Cheap to do; not done here"                                                                                                                               | **Nobody happened.** For Classiq, arguably **hard for the vendor** — a Classiq co-authored paper (arXiv:2603.05479) reports its engine "could not reliably generate circuits beyond N = 16" coupled oscillators | One `transpile`/`synthesize` run at 8–10 qubits and one at our coarse-grained size, recording wall-clock, width and depth                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| **PRS and Chennubhotla–Bahar hit/commute time** as active-site-conditioned classical baselines; **Markov-transient analysis from the active site** (Amor 2014, caspase-1)                                                                                                  | 01 §8(b) and 07's pipeline note 7                                                                                                                                                   | **Nobody happened here.** All are published, all satisfy C1/C2/C6, none is in the Phase 1.4 list                                                                                                                | Add as columns. File 01 §8(b) identifies these plus bond-to-bond propensity and Ohm as the only four published classical methods sharing our task shape — **the correct comparison class for a source-conditioned walk**, not the global scanners the field benchmarks against each other                                                                                                                                                                                                                                                                                                                   |

### 4.3 Unexplored, and probably for a reason — do not budget

| Route                                                                                                                                        | Flagged by                                                                                                                                                      | The sceptical verdict                                                                                                                                                                                                                                                                                                                                                    |
| -------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Target control / control centrality** at residue resolution (Gao et al., _Nat. Commun._ **5**, 5415; Liu et al., _PLoS ONE_ **7**, e44459) | 05 §7, §(c) — "not retrieved as applied to protein allostery"                                                                                                   | **Nobody happened**, but §4.1 explains why nobody would: maximum matching on an undirected, unweighted, degree-18 graph that is 99.2 % single-component and "close to a fixed local motif repeated at different sizes" (09 §1.1) has little to discriminate with, and the target is 2 hops away. Cheap enough (minutes) to run as one column purely to record a negative |
| **Source localization MLE** (Pinto, Thiran & Vetterli)                                                                                       | 05 §7                                                                                                                                                           | **Unexplored because the input does not exist here.** The method needs observed arrival times at sparse observers; an apo structure supplies none. Not worth a test                                                                                                                                                                                                      |
| **Spectral graph wavelets**, source-anchored                                                                                                 | 05 §7                                                                                                                                                           | **Partly uninteresting.** It is a spectrally filtered version of the same Laplacian propagator R1 already emptied, and file 05 flags its own caution that it "may collapse to tested diffusion family at heat-kernel limit"                                                                                                                                              |
| **Phonon-transport classification** (propagon/diffuson/locon) of the protein's own ANM modes                                                 | 05 §8                                                                                                                                                           | **Likely a relabelling of a closed readout.** File 05 itself notes the overlap with conventions §5 item 5 (eigenvector content / mode IPR, measured at 63.6 % and 36.4 %), and file 09 §1.3 says the spectrum is GOE with no localisation structure to classify. Check by correlating against the already-computed `mode_ipr_dipr` column before building anything       |
| **Katz / communicability**, source-anchored                                                                                                  | 05 §7                                                                                                                                                           | File 05's own note: converges to eigenvector centrality at large α, which is already a mandatory control. "Limited expected headroom"                                                                                                                                                                                                                                    |
| **Targeted rigidity percolation**                                                                                                            | 05 §8                                                                                                                                                           | **Probably not well posed on our input.** FIRST-style constraint counting needs hydrogen bonds and salt bridges (07 §3.4), which an 8–10 Å Cβ contact graph does not carry. And file 05 §(e) found rigidity _has_ been used for allosteric-site prediction, with no comparable AUC — "write unknown"                                                                     |
| **Tensor-network tree-width on protein contact graphs**                                                                                      | 03 §9, tagged `[UNVERIFIED]`, no full text landed                                                                                                               | **Uninteresting because the answer is obvious**: 7.7–8.3 independent cycles per residue is close to the worst case for MPS. Tensor networks are the classical _checker_ for a many-body proposal, not a scorer                                                                                                                                                           |
| **Long-time dynamics at fixed polynomial space** — the one regime Sakamoto & Fujii leave open                                                | 03 §1                                                                                                                                                           | **Hard, and closed from the other side.** File 08's $\lambda = (1-p)^G$ means long time = more gates = zero fidelity. State it so nobody reaches for it                                                                                                                                                                                                                  |
| **COREX/BEST and energetic frustration** as site rankers                                                                                     | 01 §6, "no top-N hit-rate number… retrieved. Negative result, recorded"                                                                                         | **Uninteresting to the field** as ranking predictors; they are used as mechanistic/explanatory signals. One paragraph to correlate an existing frustration output against curated labels, no more                                                                                                                                                                        |
| **A topology-only invariant independent of degree, burial and distance**                                                                     | 06's Method: "No source was retrieved that reports a topology-only invariant, independent of degree, burial and distance, correlating with allosteric coupling" | **Hard**, and file 06 §12 explains why: the best candidate (local packing density) is "close kin to degree and burial." Any claim here needs a **degree-preserving null** (configuration-model rewiring), which is not in the current harness and should be added before any such claim is made                                                                          |

---

## 5. The decision the evidence forces

### 5.1 Build this

1. **A classical, unlearned, spectral perturbation-response metric on a physically weighted contact
   graph, scored as a residual against a fitted exponential distance decay.** Concretely: keep
   ALPS's readout (stiffen a residue's neighbourhood, read the shift in the lowest Kirchhoff
   eigenvalues) and change two things — give the graph hydrogen-bond and side-chain-contact edge
   classes with contact rates ∝ 1/d² (§1.9), and report the residual above a fitted $\exp(-kd)$
   with $d$ = **minimum heavy-atom distance** (06 §8), alongside the frozen protocol's score.
   _Evidence:_ five independent routes converge on the observable (§1.3); it is the only method in
   the corpus with essentially no distance content ($R^2$ 0.003) and the only family above +0.10
   mean margin over random, taking 110 of 156 subgroup contrasts; it is the mode range that
   survives compression; and a 2026 quantum-algorithms paper names it verbatim as the ENM
   allosteric readout that its own algorithm cannot deliver.

2. **The quantum arm as a one-hot single-excitation Givens-rotation network at ~20 coarse nodes,
   with file 08 §9's resource table filled, presented as a C4 hardware map for a metric chosen on
   classical grounds — explicitly not as a source of advantage.** _Evidence:_ restricted to the
   single-excitation sector, exp(−iHt) _is_ an N × N unitary and decomposes exactly into $N(N-1)/2$
   two-qubit gates at depth N **on a line** (Clements et al., _Optica_ **3**, 1460; Kivlichan et
   al., _PRL_ **120**, 110501), so connectivity stops being a cost. At N = 272 that is 36,856 gates
   at depth 272 with **zero** Trotter error, against 80,832 gates at depth 1,024 for the r = 64
   Trotter step that first reproduces the top-5 — **2.2× cheaper in gates, 3.8× shallower, exact**.
   And QPE on the block-encoded Kirchhoff matrix _is_ ALPS executed quantum-mechanically (03 §7),
   which is a defensible hardware story and not a speedup claim.

3. **The two first-of-kind measurements, both already ~80 % done.** (i) No published quantum method
   has been scored against allosteric labels with a stated null (03 §11(d)); our frozen evaluation
   layer makes us the first, and the claim holds for a **negative** result, which `docs/FIELD.md`
   already commits us to reporting. (ii) No literature exists on rank-order stability of graph-node
   scores under gate-level noise (08 §5.4, with two zero-result arXiv queries on record); file 08
   §5.1 and §6.1 already have the shape of the missing result.

4. **The unitary-propagator retention argument** (07 §11) — a one-page continuity derivation from
   Loukas Theorem 3.3 to our metric with explicit t-dependence. It answers `CHALLENGE.md` §4.2's
   "prove" clause in a setting where the literature has nothing, and it is _easy_ precisely because
   our metric is a spectral shift rather than a long-time phase accumulation.

### 5.2 Stop considering this

- **Any new single-particle quantum observable on the contact graph.** §1.1, six routes.
  Sakamoto & Fujii converts eleven empirical closures into a theorem; the four branches this review
  newly examined all closed on the same mechanism.
- **Quantum kernels, variational classifiers, quantum reservoirs, quantum graph networks as
  scorers.** §1.6. $T \le \varepsilon^2 N$ gives six gates at 150 proteins; the in-repo VQC landed
  exactly where the bound predicted. File 04's verdict on QRC closes the one gap conventions §5
  left open, negatively: "it is the same mechanism under a different name."
- **The ⌈log₂N⌉ compressed encoding for an arbitrary contact graph.** §1.4. 124,844 CNOTs against
  a 65,529 generic lower bound at N = 300.
- **Jordan-Wigner and Bravyi-Kitaev.** C6 supplies no antisymmetry to enforce, and 34–40 % of our
  contacts would carry a Z-string, running to |i−j| = 156 (KRAS), 362 (BCR-ABL1) and **645**
  (myosin) `[08 §2.4]`.
- **QuEra Aquila as a propagation platform.** Its Hamiltonian is diagonal in the interaction term,
  its register is 2-D, and arbitrary connectivity costs ≤ 4N² atoms — **N ≤ 8** on 256 atoms
  `[08 §8.1]`.
- **Any full-N hardware run.** Fails on qubit count, on fidelity, on Ankaa-3's fixed 20,000-gate
  ceiling, and on cost (~$33,000 for myosin on the cheapest device) `[08 §7.1]`.
- **Louvain / Leiden / Infomap communities as supernodes.** A published mechanism — the
  field-of-view limit — predicts over-partitioning on geometrically embedded graphs, demonstrated
  on a 214-residue protein: 69 communities (modularity) and 421 (Infomap) `[07 §5]`.
- **Every MD-trained or MD-run artifact**, however compliant its inference looks: PocketMiner,
  CryptoSite, BioEmu, the MD-finetuned AlphaFlow/ESMFlow checkpoint, SWISH, CrypToth, and
  MD-covariance dynamical network analysis `[02 §7–§8, 05 §(d)]`. "Fast, single-structure inference"
  is not evidence of C2 compliance; training provenance is.
- **Two-state ANM/PATH and AlloPathFinder** — structurally unusable as blind apo-only predictors
  (one needs a second conformer, the other needs the answer as input) `[01 §8(b)]`.
- **Re-running** the ENAQT γ sweep, GBS site selection, the cooperative QUBO (classical annealing
  matches the exhaustive optimum to 5.9 × 10⁻¹⁶ on **100 of 100** instances), the multimer
  degeneracy ablation, or the protein-level false-positive experiment as designed (it measures
  protein size: `ctrl_dist` max 0.859, radius of gyration 0.813, protein size 0.783, all above the
  best real method) `[09 §7]`.

### 5.3 Genuinely balanced — the missing measurement, named

1. **Does the residual-scoring reframe find anything?** _For:_ Src's major sites decay at half the
   background rate ($d_{1/2}$ 18.24 versus 7.45 Å), so a residual exists in principle, and ALPS
   already lives there ($R^2$ 0.003 against distance). _Against:_ ALPS closes only **19.0 %** of the
   stratified headroom on curated 72 and **0.3 %** of the plain-AUC headroom, and file 09 §8 says
   the frozen protocol needs AUC 0.762–0.961 for 80 % power against a best-anywhere of 0.59.
   **Missing measurement:** run the explicit $\exp(-kd)$-residual endpoint with $d$ = minimum
   heavy-atom distance (the harness currently uses Cα–Cα) on curated 73, and report whether it
   separates ALPS from the decay null by more than the +0.0989 [+0.027, +0.168] it currently gets
   against `ctrl_closeness`.
2. **Does an equivariant classical GNN beat the plain one here?** _For:_ +4.5 AUC points at matched
   parameter count in the one published matched comparison. _Against:_ that was 3-node graphs with
   1,997,445 labels; our regime is 100–660 nodes with ~100 proteins, and the plain in-repo GNN at
   14,161 parameters already ties ALPS at p ≈ 0.14. **Missing measurement:** the swap, at matched
   parameters, on the same 96 protein-grouped folds, reporting stratified AUC **and** recall@5
   **and** DCC.
3. **Does injected direction reopen anything?** _For:_ ≥ sixfold anisotropy in Src decay rates by
   direction, and inhibitory versus activating mutations obey different laws ($k = -0.078 \pm 0.004$
   versus $+0.011 \pm 0.003$ Å⁻¹) — direction is real signal; and conventions §5 item 11 names
   non-reciprocal hopping as exactly the missing ingredient. _Against:_ the site is 2 hops away, so
   there may be no direction to resolve, and it is unclear whether a directed edge set built from
   Γ⁻¹ carries information Γ⁻¹ does not. **Missing measurement:** two GNM transfer-entropy columns
   and their correlation with the existing Γ⁻¹-derived features.
4. **Does ~35× compression retain the answer?** Balanced-to-negative (§2.8). **Missing
   measurement:** Loukas ε _and_ recall@5 across a dense r sweep on our own arms.

### 5.4 What the evidence does not support, and must not be claimed

**There is no quantum advantage on this problem at this size on this hardware, and the review
measures the gap rather than arguing it.** The whole mandated deliverable for our largest arm takes
**81.74 ms** on a laptop; the best quantum route needs 291,466 two-qubit gates on 764 qubits at a
fidelity three orders of magnitude beyond the best published two-qubit error rate. The honest
submission is a classical method with a stated, costed, _executed_ quantum hardware map at a
coarse-grained size, plus two first-of-kind measurements and one novel derivation. Claiming a
speedup would be false and a judge would find it in one question.

---

## 6. What would have to be true

Pre-mortem for the strongest remaining candidate: **spectral perturbation-response (ALPS-family) on
a physically weighted contact graph, scored as a residual against a fitted exponential distance
decay, with a one-hot single-excitation Givens circuit at ~20 coarse nodes as the stated hardware
map.**

| #       | Assumption                                                                                                                   | Verdict                                                           | Evidence                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| ------- | ---------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **A1**  | Contact topology alone sets the mode spectrum well enough that a spring-stiffening perturbation is meaningful                | **Confirmed**                                                     | Tirion 1996, doi:10.1103/PhysRevLett.77.1905: a uniform harmonic spring within a cutoff reproduces experimental B-factors as well as a full atomistic force field. C6 states it as an assumption; Tirion states it as a tested claim `[01 §2]`                                                                                                                                                                                                                     |
| **A2**  | The allosteric signal lives in the slow modes                                                                                | **Confirmed for the spectrum; open for _our_ metric**             | Five independent lines in 07 §9 (Loukas Thm 3.3 tighter at small eigenvalues; MSM bound $E(\delta) \le \lambda_1(m-1)\delta^2$ over the _dominant_ eigenvalues; 5–6 lowest Tirion modes suffice for all-atom CHARMM slow modes; 0.99 global-mode correlation at 380×; the central-limit mechanism). But **the mode composition of our metric has never been decomposed over the eigenspectrum** (07's own note 5)                                                  |
| **A3**  | A material fraction of allosteric coupling is entropic, so a spectrum-change readout sees what a displacement readout cannot | **Partly confirmed; the fraction is unknown**                     | Wand's entropy meter over 28 protein–ligand complexes: "for about one-quarter of these complexes, the absence of conformational entropy would render the resulting affinity biologically meaningless" `[VERIFIED-FULLTEXT, PMC5488930]`; CAP shows cooperativity with no conformational change in the other subunit (doi:10.1038/nsmb1132). File 06's own honest summary: "'unknown' is the correct answer to 'what fraction of allostery in general is entropic'" |
| **A4**  | The residual above an exponential distance decay contains separable signal                                                   | **Open — and load-bearing**                                       | Supported by exactly one system: in Src, major allosteric sites decay at $k = -0.038 \pm 0.005$ Å⁻¹ ($d_{1/2}$ 18.24 Å) against $-0.063 \pm 0.008$ Å⁻¹ (7.45 Å) for all 252 sites `[PMC12893324]`. One protein, one lab. File 09 §6 says ALPS closes 19.0 % of the stratified headroom                                                                                                                                                                             |
| **A5**  | H-bond/side-chain edge classes and 1/d² contact rates add information over uniform springs                                   | **Open**                                                          | Physically supported by three independent techniques (06 §5, §12) and a scaling rule validated on PDZ3. Argued _against_ by A1 itself: Tirion's result is that uniform springs already suffice. Must be **shown** on the same endpoint, not asserted                                                                                                                                                                                                               |
| **A6**  | Coarse-graining to ~20 nodes retains the answer, not just the operator                                                       | **Refuted at the required ratio, or at best unmeasured**          | Retention theorems exist for the classical Laplacian spectrum and for Kron's exact resistance invariance, and 380× worked on GroEL. But Loukas measured $\varepsilon < 1$ only at $r \le 70\,\%$, the error "jumps by almost an order of magnitude whenever $r$ increases by 20 %", no coarsening benchmark includes a residue contact graph, **no theorem covers a unitary propagator**, and file 08 requires $r \approx 97\,\%$ for myosin                       |
| **A7**  | A hard-partition lifting still produces a usable per-residue top-5                                                           | **Refuted as stated; a fix exists, untested**                     | 07 §10: hard lifting "cannot rank within a supernode and therefore caps the achievable ratio at supernodes of about five residues." At 764 → 20 the supernodes are ~38 residues. Fix: Chennubhotla & Bahar's soft-ownership R/K operator pair (_Mol Syst Biol_ **2**:36), whose intermediate-ownership "messenger" residues are themselves an allosteric readout — an unusually clean fit, and untested here                                                       |
| **A8**  | Global depolarising noise degrades resolution, not rank order                                                                | **Confirmed, with a precondition that constrains the observable** | The map $p_i \to \lambda p_i + (1-\lambda)/2^n$ is affine and strictly increasing, published in that form (Micklitz, arXiv:2510.13026). Measured shot budget tracks $1/\lambda^2$. **Precondition:** every residue score must come from _one_ noisy state with _one_ common λ. The single-circuit computational-basis readout satisfies it; a per-residue observable-by-observable scheme does not `[08 §5.1, §5.4]`                                               |
| **A9**  | The N × N deliverable costs N circuits, not N²                                                                               | **Confirmed**                                                     | Prepare $                                                                                                                                                                                                                                                                                                                                                                                                                                                          | e_i\rangle$ (one X gate), run the fixed Givens network, sample the computational basis: each shot returns an index j and M shots estimate the whole column. H real symmetric so $ | U_{ij} | =   | U_{ji} | $. For ranking alone, only the 11–23 active-site source columns are needed `[08 §6.2]` |
| **A10** | No holo information reaches the prediction path                                                                              | **Confirmed by construction; one live gap**                       | C1, `tests/test_no_leakage.py`, five guarded paths. **But**: file 02 §3's "Legal\*" caveat is unresolved — ASD is comprehensive enough that it very likely contains KRAS, BCR-ABL1 and cardiac myosin, so any ASD-derived pretrained artifact would leak through the weights. The per-target overlap check was **blocked by a search quota and not completed**                                                                                                     |
| **A11** | The frozen protocol can detect an effect of the size we expect                                                               | **Refuted for the expected effect size**                          | 80 % power at Cohen's d 0.80–1.89 (median 0.88) → achieved AUC **0.762–0.961** (median 0.879), against a best confound-free number of **0.59** `[09 §8]`. The correct response is not a fix but a disclosure: state the sensitivity band before stating a result                                                                                                                                                                                                   |

### The pre-mortem answer

If this fails in six months, the assumption that was wrong is, in order of likelihood:

1. **A4 — there is no separable signal in the distance residual.** Then the method is a
   well-engineered instrument measuring nothing, and A11 says we already lack the power to tell the
   difference between that and a small real effect. This is the _methodological_ failure, it is the
   most likely, and it rests on a decay-rate ratio measured in one protein by one lab.
2. **A6 — compression to the size the hardware holds does not retain the answer.** Then the
   classical result may stand but the C3/C4 hardware demonstration, a scored secondary objective,
   has nothing to show. This is the _deliverable_ failure, and it is the one where the gap between
   what is required (97 %) and what is measured (70 %) is largest.
3. **A10's open half — a benchmark target sits in ASD and an external artifact touched it.** Then
   the submission is invalid regardless of every number above. This is the _validity_ failure, it is
   the least likely, and it is the only one whose prevention costs hours rather than months.

---

## What this changes for our pipeline

- **`network/` (Phase 1.2/4) is now the highest-value stage, not `quantum/`.** §1.9 and §3.7:
  the propagator is exhausted by three independent literatures and one measurement; the remaining
  legal information is in edge weights (H-bond/side-chain classes, 1/d² rates) and in directed
  edges (GNM transfer entropy). Both stay inside C6. Emit the greedy edge colouring alongside the
  adjacency matrix (16–17 classes at every N) — it is the parallel-gate schedule and costs one pass.
- **`quantum/` (Phase 2/3): implement the one-hot single-excitation encoding with a Givens network,
  not a Trotteriser.** Exact, 2.2× cheaper in gates, 3.8× shallower, and it needs only a line.
  Trotter survives only as a deliberate noise-resilience knob.
- **`scoring/` reporting (frozen protocol unchanged):** every method reports AUPR against its own
  prevalence line, top-5 hit rate, DCC, and the distance-stratified endpoint — plus, new from this
  synthesis, the residual against a fitted $\exp(-kd)$ with $d$ = minimum heavy-atom distance. And
  the sensitivity band (AUC 0.762–0.961 for 80 % power) is stated **before** any number.
- **Phase 1.4 gains four classical baselines this review surfaced and the roadmap lacks:** PRS,
  Chennubhotla–Bahar hit/commute time, Markov-transient analysis from the active site, and effective
  resistance to the active site. The first three are the published methods that share our task
  shape; the fourth resolves a live disagreement for the cost of one pseudo-inverse.
- **Phase 4's compression ratio is an input from file 08, not a choice.** ~35× for myosin. Sweep
  densely, report Loukas ε and recall@5 at every ratio, use soft ownership for the reverse map, and
  write the unitary-propagator continuity argument.
- **Before any external pretrained artifact is adopted: run the ASD/ASBench/CASBench target-overlap
  check.** It is hours of work and it gates C1 validity for the whole AI comparison arm.
- **Two experiments should be registered now**, because they are contributions rather than
  diligence: the noise rank-stability measurement (08 §5.1, §6.1) and the first scoring of a quantum
  method against allosteric labels with a stated null.
- **One wording fix in `00-conventions.md` §5 item 7:** "symmetry enriches degeneracy" should read
  "symmetry enriches the low-mode gap statistic; the spectrum remains GOE and the readout still
  loses" (§2.7).

---

## Method

**Databases hit: none.** This file runs no literature search. Its inputs are
`00-conventions.md` and files `01`–`09` in this directory, read in full in this session. Per the
task brief, WebSearch and WebFetch were reserved for resolving a specific contested citation and
were **not needed** — the two candidates (the APOP 15-vs-14 denominator, §2.1; the Mohtashim
_JACS_ full text, §2.3) are both recorded by their originating files as unreachable this session,
and re-attempting them would not have changed a verdict in this file. Both are left flagged.

**Screening rule.** A claim entered §1 only if three or more files reached it by arguments of
different _kinds_ (theorem / wet-lab measurement / computation on our own data / field
reappraisal), not merely by citing the same source. Two candidate convergences were rejected under
that rule: "equivariance is the untested lever" (file 04 only, promoted to §4.2 instead) and
"published pocket-level and residue-level metrics measure different things" (files 01 and 02 only,
folded into §1.7).

**Number handling.** Every figure is quoted verbatim from its originating file with its dataset,
denominator and criterion attached, per conventions §2. No number from two different benchmarks is
compared without saying so — in particular the ESSA/APOP top-3 numbers (N = 14–15, matched pairs)
are never set against AlloBench's JI figures (N = 100, leakage-controlled), and file 02's ESM-1b
15/24 permutation result is never set against the AUPR 0.06 collapse (§2.5).

**Evidence tags.** Carried through unchanged from the originating file. Where this synthesis draws
an inference the source files do not state — the R1 ∧ R2 pincer (§3.3), the identification of
conventions §5 item 1 with the published CTQW-equals-eigenvector-centrality result (§3.2), the
observation that §4.1's two-hop measurement undercuts file 05's transport-flavoured routes, and
the constraint in §1.8 that the required compression exceeds the measured range — that inference is
marked as such in the text and carries no tag, because it is reasoning over sourced claims rather
than a new retrieval.

**Stopping rule.** Stopped when every one of the six required sections was populated from at least
three files, when every "not retrieved / not attempted / no precedent" flag across the nine files
had been placed in §4.2 or §4.3 with a stated reason and a test, and when each contradiction in §2
had both positions quoted and a named settling measurement.

**What this file could not do.** It cannot resolve any contradiction that requires a retrieval its
source files failed (§2.1, §2.3). It cannot check the leakage-guarded paths and therefore cannot
verify A10 (conventions §7). And it inherits every gap its sources recorded — most consequentially
the paywalled CAPASP apo-versus-holo numeric values (01), the AlloDyn before/after F1 values (01),
ZHMolEReP's learned-weight status (02), and the absence of any live `GetDevice` reading behind file
08 §5.3's device fidelities, which are the numbers the entire N ≈ 20 conclusion rests on.
