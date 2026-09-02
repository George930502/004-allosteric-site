# Hybrid quantum + AI methods, and hybrid orchestration patterns

**Scope:** this file covers (A) quantum machine-learning models used as a *scorer* — kernels,
variational classifiers, quantum graph networks, quantum reservoirs, quantum generative models,
quantum-computed features — and (B) *orchestration*: which stage of a pipeline each of quantum
and AI has been shown to own. It deliberately excludes pure-quantum propagation observables on a
contact graph (settled by measurement, `00-conventions.md` §5), classical ENM and spectral
baselines, and supervised allosteric-site predictors that take MD as input.
**Sibling files:** the pure-quantum-observable and classical-baseline files in this directory;
`allosteric-benchmark/docs/quantum-observable-search.md` for the eleven closed quantum insertion
points; `allosteric-benchmark/docs/ai-model-landscape.md` for the AI model families.
**Retrieved:** 2026-08-25.

---

## 0. The one-paragraph answer

The division of labour that the literature supports is not the one the working thesis assumes.
Across every matched comparison retrieved this session, **AI earns its place before and after the
quantum stage — building and compressing the graph, and turning scores into a ranking — and the
quantum stage earns its place only where the object being simulated is itself quantum.** A
residue contact graph is not. The single strongest orchestration result found (Guided Graph
Compression, §B.2) is a hybrid pipeline where the entire measured gain came from the classical
compression stage and the quantum classifier merely tracked it. The one matched comparison where
a quantum model genuinely won (EQGNN, §A.3) did so on 3-node graphs with 2 million labels. Our
regime is 100–660 nodes with ~100 labels. Nothing found this session reverses that.

---

# HALF A — quantum machine learning as a scorer

## A.1 Quantum kernels: the branch is closed, and 2025–2026 did not reopen it

`00-conventions.md` §5 forbids re-deriving this. What follows is only what is **new** since that
closure, plus the one thing the closure did not state.

The mechanism is now unified with the variational side. Exponential concentration in quantum
kernels and barren plateaus in variational circuits are the same phenomenon:

> "a rigorous connection between barren plateaus (BP) in variational quantum algorithms and
> exponential concentration of quantum kernels for machine learning" — arXiv:2501.07433,
> *Phys. Rev. A* 114, 022417 (2026). `[VERIFIED-ABSTRACT]`

The four named sources of that concentration — expressivity of the data embedding, global
measurements, entanglement, and noise — each carry an analytic bound (Thanasilp et al.,
*Nat. Commun.* 15, 5200 (2024), doi:10.1038/s41467-024-49287-w). `[VERIFIED-ABSTRACT]`

**What this adds for us.** One variance measurement now settles two questions at once. A single
pre-screen on kernel off-diagonal mass tells you both whether the kernel can generalise and
whether a variational model on the same embedding can be trained. Our own gate 1 already ran the
measurement without knowing it answered both: off-diagonal mass fell from 0.718 at bandwidth 0.02
to 0.005 at bandwidth 1.0 (`allosteric-benchmark/hybrid/RESULTS.md`). `[VERIFIED-FULLTEXT]`

**The cost the closure did not price.** A quantum kernel carries a state-preparation cost of
Θ(M²) for an M-point Gram matrix, and that cost does not amortise:

> "quantum kernel methods carry a $\Theta(M^2)$ state-preparation cost for the Gram matrix that
> does not amortize" — arXiv:2608.08433 (2026-08-09). `[VERIFIED-ABSTRACT]`

No 2025–2026 result retrieved this session changes the verdict. The one that tries — trainable
kernels for symmetry-structured data, arXiv:2509.14337 — requires a symmetry group in the data to
build the embedding around. A residue contact graph has permutation symmetry over nodes and
nothing else. `[UNVERIFIED]` — the paper was retrieved by title and abstract only, and the mapping
to our setting is our inference, not the paper's claim.

## A.2 Variational classifiers, data re-uploading, and the trainability/simulability question

The honest statement in `quantum-observable-search.md` — that "trainable implies classically
simulable" is *not* a theorem — is confirmed by the source that made the argument famous, and
that source is now peer-reviewed:

> "We collect evidence-on a case-by-case basis-that many commonly used models whose loss
> landscapes avoid barren plateaus can also admit classical simulation, provided that one can
> collect some classical data from quantum devices during an initial data acquisition phase."
> — arXiv:2312.09121, *Nature Communications* 16, 7907 (2025), doi:10.1038/s41467-025-63099-6.
> `[VERIFIED-ABSTRACT]`

Note the escape clause the authors themselves flag: the argument is *average case*, and the paper
lists smart initialisation, out-of-assumption models and provable superpolynomial advantage as
caveats. This is evidence, not a theorem, and the file should say so.

Our own measurement sits exactly where the theory predicts. A 24-parameter data-reuploading VQC
on 44 protein-grouped targets scored a stratified AUC of 0.575 against 0.596 for logistic
regression on identical features, paired p = 0.39, and against **0.576 for unlearned ALPS** —
that is, 24 trained parameters bought nothing over one hand-designed score
(`allosteric-benchmark/hybrid/RESULTS.md`, gate 3b). `[VERIFIED-FULLTEXT]`

**What this changes:** nothing about our design. It means a second variational classifier is not
worth building. The first one already landed on the predicted number.

## A.3 Quantum graph neural networks and equivariant QNNs — the one place quantum won

This is the most important positive result in this file, and it must be read with its conditions
attached.

Gianelle et al. benchmarked four architectures on quark/gluon jet tagging with **matched
parameter counts and identical train/validation/test splits** — the fair-comparison design our
own hybrid folder insists on. Test AUC, from Table 1 (*Axioms* 13 (2024) 160,
doi:10.3390/axioms13030160, arXiv:2311.18672): `[VERIFIED-FULLTEXT]`

| model | trainable params | test AUC |
| --- | --- | --- |
| GNN | 5122 | 63.36 % |
| EGNN (SE(2)-equivariant, classical) | 5252 | 67.88 % |
| QGNN | 5156 | 61.43 % |
| **EQGNN (permutation-equivariant, quantum)** | 5140 | **75.17 %** |

Read the table, not the headline. **The plain quantum model lost to the plain classical model**
(61.43 against 63.36). Equivariance helped both families; it helped the quantum family more. The
paper's own summary: "the EGNN outperformed both the classical and quantum GNN; however, this
algorithm was outperformed by EQGNN with a 7.29% increase in AUC". `[VERIFIED-FULLTEXT]`

Three conditions make this inapplicable to us as it stands:

1. **Graph size.** "the size of the quantum state and the Hamiltonian scale as 2^n, where n is
   the number of qubits… jets with large particle multiplicity require prohibitively complex
   quantum networks. Thus, we limited ourselves to the case of n_α = 3 particles per jet."
   Three nodes. One qubit per node. Our smallest frozen arm is two orders of magnitude larger.
   `[VERIFIED-FULLTEXT]`
2. **Label supply.** N = 1,997,445 jets. We have ~100 labelled proteins. `[VERIFIED-FULLTEXT]`
3. **Statistics.** One training run per architecture, no seed variance, no significance test.
   `[UNVERIFIED]` — inferred from the absence of any error bar in Table 1.

A newer line pushes message-passing QGNNs into the Weisfeiler-Leman hierarchy
(arXiv:2606.26873) and a critical review names noise, decoherence and scalability as the standing
obstacles without demonstrating superiority (arXiv:2408.06524). `[VERIFIED-ABSTRACT]`

**What this changes for us.** It identifies the *only* structural lever with published evidence
behind it: **equivariance, not quantumness**. The classical EGNN gained +4.5 AUC points over the
plain GNN at matched parameter count. Our in-repo GNN is a plain message-passing model
(`allosteric-benchmark/gnn/RESULTS.md`, 14,161 parameters, stratified AUC 0.622/0.630 against
ALPS 0.592, paired p ≈ 0.14). `[VERIFIED-FULLTEXT]` An E(3)-equivariant classical GNN on Cβ
coordinates is a cheaper and better-evidenced next move than any quantum graph model.

## A.4 Quantum reservoir computing — the gap, characterised

This is the candidate `00-conventions.md` §5 names as never characterised. Here is the
characterisation.

**What QRC is.** A fixed, untrained quantum system is driven by a *sequence* of inputs; local
observables are measured at each step; only a classical linear readout is trained.

> "Quantum reservoir computing (QRC) uses the dynamics of a fixed or weakly tuned quantum system
> to transform **temporal and sequential inputs** into measured features, while training is
> typically confined to a classical readout." — arXiv:2607.18552 (2026-07-20), survey.
> `[VERIFIED-ABSTRACT]` (emphasis added)

**Does it run on a static graph?** No, not in the form the name suggests. The one paper whose
title joins the two — "Quantum reservoir computing on random regular graphs", *Phys. Rev. A* 112,
012622 (2025), arXiv:2409.03665 — uses the graph as the **reservoir's own internal spin-coupling
topology**, not as the data. The data is a time series. Its numbers: N = 8 spins, degree k swept,
N_transient = 600–800 steps discarded, **N_train = 1000–2000 time steps**, N_test = 100–200.
`[VERIFIED-FULLTEXT]` The tasks are memory capacity at delay τ and NARMA-style nonlinear temporal
regression. Nothing in it takes a graph as input or produces a per-node score.

**The static-input analogue exists and has a different name.** A quantum reservoir driven by a
single static input, with a trained linear readout, is a **quantum extreme learning machine**
(QELM). That is the object that could in principle score residues. Three results bound it:

- A QELM is *exactly* a single effective measurement. "they can be concisely described via single
  effective measurements, and provide an explicit characterisation of the information exactly
  retrievable with such protocols" — arXiv:2210.00780, *Commun. Phys.* 6, 118 (2023),
  doi:10.1038/s42005-023-01233-w. `[VERIFIED-ABSTRACT]` In plain terms: a fixed random feature map
  followed by ridge regression. The quantum part contributes the feature map and nothing else.
- The feature map is a linear transform of the Pauli features the *encoding* creates. The
  Pauli-transfer-matrix analysis yields "a nonlinear vector (auto-)regression model as an
  interpretable classical representation of a QELM", and finds that "structured Hamiltonians can
  reduce model expressivity, as reflected in a low readout rank" — arXiv:2602.18377.
  `[VERIFIED-ABSTRACT]` A contact-graph Hamiltonian is structured and symmetric.
- In the regime where it works, it is classically simulable. "the relevant evolution time is
  consistent with information exchange over short distances and, within the explored system
  sizes, does not show evidence of scaling with the full system size. This suggests that QELM
  performance in this regime relies only on limited entanglement and **remains compatible with
  efficient classical simulation**." — arXiv:2509.06873. `[VERIFIED-ABSTRACT]`

**Is there a published advantage?** No.

> "Current results do not establish a broad quantum advantage over well matched classical
> reservoirs." — arXiv:2607.18552, survey abstract. `[VERIFIED-ABSTRACT]`

**One further result that bites directly on our Hamiltonian.** For a reservoir whose measured
features evolve *linearly*, "Linear reservoir dynamics can therefore redistribute features, but
cannot create new fixed-delay expressive power on their own" — arXiv:2605.29071.
`[VERIFIED-ABSTRACT]` A single-excitation walk on a contact graph is precisely linear in that
sense. This is the reservoir-computing restatement of the mechanism already diagnosed in §5 of
the conventions, arrived at independently.

**What would make a quantum reservoir non-trivial**, per the two theory papers: nonstabilizerness
(magic) injected into the dynamics — a tunable fraction p of conditional-T gates moves the
reservoir "from classically tractable to maximally expressive quantum dynamics"
(arXiv:2510.18623, *Phys. Rev. A* 113, L060401 (2026)) `[VERIFIED-ABSTRACT]`; and non-Gaussian
operations in the continuous-variable case (arXiv:2605.29071). `[VERIFIED-ABSTRACT]` Neither is
supplied by a residue contact graph. Both would have to be added by hand, and adding them means
the dynamics no longer represents the protein.

**Verdict on QRC/QELM.** Not a gap worth filling with an implementation. It is a fixed random
feature map plus a linear readout, it is a temporal paradigm whose static analogue collapses to a
POVM, its useful regime is classically simulable at our size, and its published advantage over a
matched classical reservoir does not exist. The honest form of the finding is: **the corpus was
searched, full texts were landed, and the branch closes on the same mechanism as the other
eleven** — a linear, structured, low-magic dynamics carries no information a classical readout of
the same features does not already have.

## A.5 Quantum generative models

Three families, one relevant result each.

- **Quantum circuit Born machine (QCBM).** The KRAS study in §B.1 is the only wet-lab-validated
  deployment retrieved. It uses a QCBM as a *prior* for a classical LSTM.
- **Quantum Boltzmann machines.** The standard QRBM is untrainable in practice: "their
  non-commuting Hamiltonians make gradient evaluation computationally demanding, even on
  fault-tolerant quantum computers." The workable variant, the semi-quantum RBM, is explicitly a
  *classical-data* model, and its stated advantage is a constant factor in width: "to learn a
  given probability distribution, an RBM requires three times as many hidden units as an sqRBM,
  while both models have the same total number of parameters" — arXiv:2502.17562, published as
  *Commun. Phys.* (2025), doi:10.1038/s42005-025-02353-1. `[VERIFIED-FULLTEXT]` (abstract read
  verbatim from the arXiv record; the journal page was paywalled to this session). A 3× width
  factor at equal parameter count is not a reason to build a quantum sampler.
- **Quantum GANs.** BO-QGAN reports "a 2.27-fold higher Drug Candidate Score (DCS) than prior
  quantum-hybrid benchmarks and 2.21-fold higher than the classical baseline, while reducing
  parameter count by more than 60%", with the architectural finding that 3–4 shallow 4–8 qubit
  circuits in sequence beat one deep one — arXiv:2506.01177, PMLR 267 (2025).
  `[VERIFIED-ABSTRACT]` This is molecule generation, not residue scoring, and DCS is a composite
  heuristic score, not a held-out measurement.

**What this changes for us.** Nothing on the prediction path. We are not generating; we are
ranking a fixed node set. Generative quantum models have no stage to own in our pipeline.

## A.6 Quantum-enhanced feature extraction — the framing most likely to survive, and its price

The framing is: run a quantum dynamics simulation, measure observables, hand the numbers to a
classical model as features. It survives the trainability objections in §A.1–A.2 because nothing
in the quantum part is trained. It is also what our CTQW already is.

Two things price it honestly.

**It is what the pre-refuted list already tested.** Eleven quantum observables were computed on
73–101 targets and fed to a classical readout; all eleven lost to a classical spectral readout
(`00-conventions.md` §5). The framing does not rescue the observables.

**The input cost is the real bottleneck, and it is a counting theorem, not an engineering gap.**

> "the resulting $\Theta(N)$ bound is a counting theorem rather than an engineering limitation
> that improved hardware will remove. Measured gate counts for a representative loading task are
> reported: an optimal library implementation requires 247 CNOT gates at n=8 qubits and doubles
> with each additional qubit, while the classical preprocessing that produces the rotation angles
> requires reading the entire input vector." — arXiv:2608.08433. `[VERIFIED-ABSTRACT]`

And the trap that closes the loop:

> "the strong input models that make quantum algorithms fast on classical data also enable
> classical dequantization" — arXiv:2608.08433. `[VERIFIED-ABSTRACT]`

**What this changes for us — and it is a C3 obligation.** Any quantum stage we report must count
the gates that *load the graph*, not only the gates that propagate on it. At 247 CNOTs for 8
qubits and a doubling per qubit, amplitude-encoding a 300-residue adjacency row is not a
near-term circuit. The escape the same paper names is the only one open to us: **an efficiently
preparable state**. A single-excitation position basis state |i⟩ is one X gate. That is why the
CTQW formulation is the only encoding in this file that survives C3 — and it is also the one
already shown to be a proximity ranker.

---

# HALF B — orchestration: which stage does each own?

## B.1 Published hybrid pipelines, and what each side actually owned

Four pipelines were landed in full text or in a citable record. In each row, "quantum stage" is
what the paper put on a quantum device, and "claim" is what the paper measured.

**(1) KRAS inhibitor design — Nature Biotechnology 2025.**
doi:10.1038/s41587-024-02526-3, PMC12700792, arXiv:2402.08210. `[VERIFIED-FULLTEXT]`

- Quantum stage: a 16-qubit QCBM on IBM hardware generating a *prior distribution*.
- Classical/AI stages: 1.1 M-molecule training set; an LSTM generator; Chemistry42 for scoring
  and filtering; docking (QuickVina 2, SMINA); human expert selection down to 15 molecules.
- Control: "an LSTM model devoid of quantum priors (representing a fully classical architecture)".
- Claim: "the use of QCBM–LSTM… offered a 21.5% improvement in passing filters that assessed the
  synthesizability and stability of the generated molecules".
- **What did not improve:** "these molecules displayed comparably high docking scores as
  determined by QuickVina 2 and the PLI score". On the Tartarus benchmark the hybrid produced the
  best molecules for one target (PDB 4LDE) while "the docking scores for the remaining two
  targets were not as high as those produced by classical algorithms".
- The authors' own limit: "they stop short of definitively proving a 'quantum advantage',
  achieving results unattainable by classical methods within a reasonable time frame."
- **The fairness gap.** The four compared variants were QCBM(simulator), QCBM(hardware),
  MQCBM(simulator) and LSTM-with-no-prior. There is **no classical prior of matched dimension**
  in the comparison. The measured contrast is *prior versus no prior*, not *quantum prior versus
  classical prior*. `[UNVERIFIED]` — this reading is ours; the paper does not state it.

**(2) Protein structure prediction — J. Chem. Theory Comput. 2024, IBM Quantum + Cleveland Clinic.**
doi:10.1021/acs.jctc.4c00067, PMC11099973. `[VERIFIED-FULLTEXT]`

- Quantum stage: "The most computationally demanding part, finding a coarse-grain representation
  of the lowest energy conformation of the protein structure, is performed on a quantum
  computer." A variational algorithm on a tetrahedral lattice with Miyazawa–Jernigan contact
  energies.
- Classical stages: everything else — format conversion, all-atom reconstruction, refinement.
- The division-of-labour argument is explicit and is about **data, not physics**: deep learning
  wins where MSA depth is high; the quantum candidate niche is the subspace where MSAs are
  shallow and template-based learning degrades.
- Resource cost, which is the number that matters for C3: "for a protein sequence with 22 amino
  acids, the number of qubits needed is 118", and "there is a perfect quadratic relationship
  between the protein sequence length and the number of qubits required."
- Demonstrated instance: a **seven-residue** catalytic P-loop.

**(3) Guided Graph Compression for quantum GNNs — arXiv:2506.09862 (CERN/ETH/UPC).**
`[VERIFIED-FULLTEXT]` This is the most instructive row in the table.

- Classical/AI stage: a graph autoencoder that reduces both node count and node-feature
  dimensionality, with the reconstruction loss and the downstream classification loss optimised
  **jointly**, so the compression is guided by the task.
- Quantum stage: a small permutation-equivariant QGNN classifier with data re-uploading, reading
  out ⟨Z⟩ on the first qubit.
- Test ROC-AUC, jet tagging, 50 k train / 5 k val / 50 k test:

| pipeline | test ROC-AUC |
| --- | --- |
| Uncompressed classical GNN (reference) | 0.8051 ± 0.0041 |
| Unguided compression → classical GNN | 0.5797 ± 0.0049 |
| Unguided compression → QGNN2 | 0.7811 ± 0.0046 |
| **Guided compression → classical GNN** (MIAGAE) | **0.8645 ± 0.0033** |
| Guided compression → QGNN2 (MIAGAE) | 0.8406 ± 0.0039 |
| Guided compression → classical GNN (SAG) | 0.8697 ± 0.0033 |
| Guided compression → QGNN2 (SAG) | 0.8721 ± 0.0030 |

- **Read it as an ablation of the orchestration, not of the classifier.** Making the compression
  task-guided moved the classical GNN from 0.5797 to 0.8645 — +0.28 AUC. The quantum classifier
  moved with it. In the best quantum row the margin over the classical GNN is 0.0024 with ±0.003
  error bars: a tie. In the other autoencoder the classical GNN wins outright.
- The gain lives in the AI stage. The quantum classifier is a passenger.

**(4) QSyncFold — Briefings in Bioinformatics 2026.** doi:10.1093/bib/bbag234, PMC13221982.
`[VERIFIED-FULLTEXT]`

- Quantum stage: a hybrid QNN with continuous-coordinate encoding, reducing per-iteration qubits
  from O(N) to 3 + ⌈log₂ N⌉ by trading register size for iteration count.
- Claim: "a 5.25-fold improvement in the lDDT metric compared with the Variational Quantum
  Eigensolver baseline".
- **The control is another quantum method.** On the classical side the paper is explicit: "While
  using quantum baselines as the primary comparison, the method performance approaches AlphaFold2
  in the short peptide domain, with classical methods serving as background reference." Approaches,
  on short peptides. It does not beat a classical control.

## B.2 Where a quantum subroutine actually pays inside a classical loop

The pattern with the strongest evidence is **quantum proposal, classical accept/reject**.

Layden et al., *Nature* 619, 282–287 (2023), doi:10.1038/s41586-023-06095-4: `[VERIFIED-ABSTRACT]`

> "In experiments, our quantum algorithm converged in fewer iterations than common classical MCMC
> alternatives, suggesting unusual robustness to noise. In simulations, we observed a polynomial
> speedup between cubic and quartic over such alternatives."

The property that makes it work is structural, and it is worth naming because it is the design
rule for any quantum subroutine we might add: **the quantum device only proposes; correctness is
enforced classically, so the algorithm "provably converges to the correct distribution, despite
being hard to simulate classically."** A wrong quantum answer costs iterations, never validity.

The follow-up is the honest bound and must be reported with it: "there is no speedup over
classical sampling on a worst-case unstructured sampling problem", together with "an upper bound
to the Markov gap that rules out a speedup for any unital quantum proposal" — arXiv:2403.03087.
`[VERIFIED-ABSTRACT]`

Other directions retrieved, with what each owned:

- **Classical ML choosing the circuit's starting point.** CRiSP uses a Transformer policy with
  neural-guided Monte Carlo tree search, trained by self-play, to pick Clifford gates that
  initialise a VQA; it reports "3.17× (max 45.02×) in average energy accuracy" over
  state-of-the-art Clifford initialisation, at up to 22 qubits and 1,370 parameters —
  arXiv:2605.23138. `[VERIFIED-ABSTRACT]` AI owns *initialisation*, quantum owns the energy.
- **ML-based error mitigation.** "machine learning for quantum error mitigation (ML-QEM)
  drastically reduces the cost of mitigation… without sacrificing accuracy", demonstrated at up
  to 100 qubits with linear regression, random forests, MLPs and graph neural networks —
  arXiv:2309.17368, *Nature Machine Intelligence* 6, 1478–1486 (2024),
  doi:10.1038/s42256-024-00927-2. `[VERIFIED-ABSTRACT]` AI owns the *overhead*, not the answer.
- **ML compilation of circuits.** A large and mature literature — RL for compiler optimisation
  (arXiv:2212.04508), qubit routing, quantum architecture search (arXiv:2104.07715,
  arXiv:2103.16089). `[VERIFIED-ABSTRACT]` for titles and abstracts only; no numbers extracted,
  because none of it changes what a method computes.

## B.3 The reverse direction — AI preparing the input a quantum algorithm consumes

This is where the retrieved evidence is strongest and most directly usable.

- **Structure.** Every quantum protein pipeline found starts from a structure that a classical
  method produced. The JCTC perspective (B.1 row 2) frames deep learning and quantum simulation
  as *complementary regimes selected by MSA depth*, not as competitors on the same input.
- **Graph coarsening.** Guided Graph Compression (B.1 row 3) is the only published instance found
  of an AI model *learning* the coarse-graining that a quantum model then consumes, and it is
  precisely the challenge's secondary objective on coarse-graining (`CHALLENGE.md` §4.2). Its
  lesson is that **unguided compression destroys the signal** (0.5797) and **guided compression
  creates it** (0.8645). If we coarse-grain, the compression must be optimised against the
  downstream objective, not against reconstruction error alone.
- **State preparation.** Variationally learned loading and amortised preparation are two of the
  four escapes arXiv:2608.08433 names from the Θ(N) input bound. `[VERIFIED-ABSTRACT]`

**The C1/C2 warning that goes with this half.** Every AI stage listed above is *trained*. Guided
graph compression is trained on the downstream labels; that is what makes it work. Importing that
pattern here would mean training a coarsening on allosteric labels, which needs a training split
of proteins we do not have at useful size, and which must never see a holo-derived label for a
scored arm (C1). A learned coarsening trained on MD-derived flexibility would violate C2 outright.

## B.4 Amplitude and state preparation as the real bottleneck

Collected in one place because it is the number every hybrid design must clear first.

| encoding | qubits for n items | cost | usable here? |
| --- | --- | --- | --- |
| Basis / position basis, single excitation \|i⟩ | ⌈log₂ n⌉ or n | 1 X gate | **Yes.** This is the CTQW encoding. |
| Amplitude encoding of a general vector | ⌈log₂ n⌉ | Θ(N) gates; 247 CNOTs at n = 8 qubits, doubling per qubit | No, at protein size |
| Grover–Rudolph distribution loading | ⌈log₂ n⌉ | Θ(N), plus reading the whole input classically | No |
| Quantum kernel Gram matrix | per-pair | Θ(M²) preparations, non-amortising | No, at M ≈ 16 000 residues |
| Lattice PSP encoding (JCTC) | quadratic in sequence length | 118 qubits at 22 residues | No, at protein size |
| Iteration-traded PSP encoding (QSyncFold) | 3 + ⌈log₂ N⌉ per iteration | more iterations instead | Untested beyond short peptides |

Source for rows 2–4: arXiv:2608.08433 `[VERIFIED-ABSTRACT]`. Row 5: PMC11099973
`[VERIFIED-FULLTEXT]`. Row 6: PMC13221982 `[VERIFIED-FULLTEXT]`.

---

# The four questions

## (a) Has any hybrid quantum+AI pipeline beaten a fair matched all-classical control on a structural-biology task?

**No.** Not in anything retrieved this session. The four closest candidates and why each falls
short:

| candidate | matched control? | who won | why it does not answer the question |
| --- | --- | --- | --- |
| KRAS QCBM–LSTM, *Nat. Biotechnol.* 2025 | Partial — vanilla LSTM, no prior | Hybrid, +21.5 % filter pass rate | Molecule *generation*, not site prediction. Docking scores tied. No classical prior of matched dimension. Authors decline the advantage claim. |
| EQGNN, *Axioms* 2024 | **Yes** — matched params, identical splits | Quantum, +7.29 AUC points | High-energy physics, 3-node graphs, 2 M labels, single seed, no significance test. Plain QGNN *lost* to plain GNN. |
| Guided Graph Compression, arXiv:2506.09862 | **Yes** — same compression, swap classifier | Tie (0.8721 ± 0.0030 vs 0.8697 ± 0.0033); classical wins with the other autoencoder | The +0.28 AUC came from the classical compression stage. Also HEP. |
| QSyncFold, *Brief. Bioinform.* 2026 | No — control is a VQE | Quantum, 5.25× lDDT over VQE | "approaches AlphaFold2… with classical methods serving as background reference". |

Per ADR 0019 this is a statement about the recorded search, not about the world: **no such result
was retrieved by the searches recorded in the Method section below.**

## (b) Division of labour, stage by stage

Built from the evidence above, not from intuition. "Quantum helps" and "AI helps" mean a matched
comparison was found in which that side won; "no" means the matched comparison was found and that
side did not win; "no evidence" means none was retrieved.

| stage | does quantum help? | does AI help? | evidence |
| --- | --- | --- | --- |
| **0. Apo structure → coordinates** | No evidence at protein scale. Quantum PSP demonstrated at 7 residues, 118 qubits at 22 residues, quadratic scaling. | **Yes, decisively.** AlphaFold2/ESMFold are the input everything else consumes; the quantum niche is explicitly the shallow-MSA subspace. | PMC11099973 `[VERIFIED-FULLTEXT]` |
| **1. Structure → graph / coarse-graining** | No evidence. | **Yes.** Task-guided learned compression moved a downstream classifier from 0.5797 to 0.8645 AUC; unguided compression destroyed it. | arXiv:2506.09862 `[VERIFIED-FULLTEXT]` |
| **2. Graph → Hamiltonian / state preparation** | **No — this is where quantum loses.** Θ(N) loading is a counting theorem; strong input models enable dequantization; Θ(M²) for a kernel Gram matrix. Only an efficiently preparable state (single-excitation \|i⟩) survives. | **Cost only, not signal.** RL Clifford initialisation gives 3.17× mean energy accuracy; learned loading is one of four named escapes. | arXiv:2608.08433, arXiv:2605.23138 `[VERIFIED-ABSTRACT]` |
| **3. Hamiltonian → propagation** | **Native, but empty on this object.** A single-particle Hermitian walk on a contact graph is classically simulable and reduces to transfer amplitudes; published CTQW centrality reproduces eigenvector centrality on 150 proteins. Linear reservoir dynamics "cannot create new fixed-delay expressive power". | No evidence that survives C2. MD-trained surrogates are excluded by construction. | `00-conventions.md` §5; doi:10.1021/jacs.6c08053; arXiv:2605.29071 `[VERIFIED-ABSTRACT]` |
| **4. Propagation → residue score** | **No.** Quantum kernel 0.592 vs poly-4 0.600 (Δ −0.008, p = 0.20); VQC 0.575 vs logistic 0.596 (Δ −0.021, p = 0.39); VQC ties unlearned ALPS at 0.576. | **Marginally.** GNN 0.622/0.630 vs ALPS 0.592 across two seeds, but paired p ≈ 0.14, not significant at n = 96. Equivariance is the untested lever: classical EGNN beat plain GNN by +4.5 AUC points at matched parameters. | `allosteric-benchmark/hybrid/RESULTS.md`, `allosteric-benchmark/gnn/RESULTS.md` `[VERIFIED-FULLTEXT]`; *Axioms* 13 (2024) 160 `[VERIFIED-FULLTEXT]` |
| **5. Score → ranked site** | No evidence. | **No — AI actively hurts here.** The learned combiner raised AUC 0.606 → 0.668 while dropping top-5 hit rate 27.1 % → 18.6 %. Geometry owns localisation. | `allosteric-benchmark/docs/quantum-observable-search.md` `[VERIFIED-FULLTEXT]` |

**The shape of the answer.** AI owns the ends of the pipeline (stages 0–1 and, weakly, 4).
Quantum owns nothing on this object; the one stage where quantum is *native* (stage 3) is the one
where the object being simulated supplies no quantum structure. The stage everyone forgets —
stage 2 — is where quantum's cost is paid, and it is the stage most likely to sink a submission
that does not budget for it.

## (c) Quantum reservoir computing on graphs

Three answers, all from §A.4.

1. **Does it exist?** Not as a model that takes a graph as input. The only "QRC on graphs" paper
   uses the graph as the reservoir's internal spin-coupling topology and feeds it a time series
   (*Phys. Rev. A* 112, 012622 (2025)). The static-input analogue is the quantum extreme learning
   machine, which is a fixed random feature map plus a trained linear readout.
2. **Does it need training data we do not have?** Yes, twice over. The graph paper trains on
   1000–2000 time steps after discarding 600–800; we have no time axis at all, since C2 forbids
   trajectories. And the readout is supervised, so it needs labelled proteins — we have ~100,
   which §(e) shows affords a handful of trainable parameters.
3. **Is it classically simulable at our size?** In the useful regime, yes. QELM performance
   "relies only on limited entanglement and remains compatible with efficient classical
   simulation" (arXiv:2509.06873), a QELM is exactly one effective POVM (*Commun. Phys.* 6, 118
   (2023)), and structured Hamiltonians reduce its readout rank (arXiv:2602.18377). Making it
   non-simulable requires injected magic or non-Gaussianity that a contact graph does not supply.

**The gap in `00-conventions.md` §5 is now closed, negatively.** QRC is not a twelfth candidate
worth testing; it is the same mechanism under a different name.

## (d) The cheapest decisive pre-screens, before any hybrid circuit is written

Ordered by cost. The first four are minutes of CPU on data we already have.

| # | pre-screen | what it decides | source |
| --- | --- | --- | --- |
| 1 | **Generalisation budget**: compute T_max = ε²N with N = *proteins*, not residues | How many trainable parameters the label supply supports. If T_max < 10, no variational model of any kind. | *Nat. Commun.* 13, 4919 (2022) `[VERIFIED-ABSTRACT]` |
| 2 | **Input-cost count**: count the gates that load the data before the gates that process it | Kills amplitude encoding and kernel Gram matrices at our size, before design | arXiv:2608.08433 `[VERIFIED-ABSTRACT]` |
| 3 | **Non-linearity gap** (best RBF − linear AUC) and **kernel effective rank** | Whether any richer kernel has room. Already run: gap +0.076, so room exists | `allosteric-benchmark/hybrid/RESULTS.md` `[VERIFIED-FULLTEXT]` |
| 4 | **Geometric difference g vs √n**, swept over bandwidth, **reported beside off-diagonal mass** | One-directional: g ≪ √n proves classical matches or beats quantum. Already run; the off-diagonal mass is what stops g from being misread | same, and the repair note in §"Three repairs" |
| 5 | **Kernel concentration variance** — the four named sources: embedding expressivity, global measurement, entanglement, noise | Whether the kernel collapses to the identity. **Also settles barren plateaus**, by the proved equivalence | *Nat. Commun.* 15, 5200 (2024); *Phys. Rev. A* 114, 022417 (2026) `[VERIFIED-ABSTRACT]` |
| 6 | **Effective rank R_eff of the feature matrix**, plus the order-statistics expressivity score | The reservoir/QELM analogue of #3. Cost is independent of Hilbert-space dimension, so it runs at any size and on hardware | arXiv:2607.09445 `[VERIFIED-ABSTRACT]` |
| 7 | **Nonstabilizerness (magic) content** of the proposed dynamics | If the dynamics is near-Clifford, the model is classically tractable by construction | arXiv:2510.18623, *Phys. Rev. A* 113, L060401 (2026) `[VERIFIED-ABSTRACT]` |
| 8 | **Taylor / Pauli-path classical surrogate** of the loss landscape | If a near-Clifford classical surrogate reproduces the landscape, the circuit adds nothing | arXiv:2507.06344 `[VERIFIED-ABSTRACT]` |

Screens 1 and 2 are new relative to `quantum-observable-search.md`, and both are strictly cheaper
than the two it names. Screen 1 costs one multiplication.

## (e) Barren plateaus and the parameter budget at ~100–150 labelled proteins

The bound, with its source:

> "the generalization error of a quantum machine learning model with T trainable gates scales at
> worst as √(T/N). When only K ≪ T gates have undergone substantial change in the optimization
> process, we prove that the generalization error improves to √(K/N)."
> — Caro et al., *Nature Communications* 13, 4919 (2022), doi:10.1038/s41467-022-32550-3,
> arXiv:2111.05292. `[VERIFIED-ABSTRACT]`

Inverting, for a target generalisation error ε: **T ≤ ε²N**. With N = 150 labelled proteins:

| target ε | T_max (trainable gates) |
| --- | --- |
| 0.05 | 0 |
| 0.10 | 1 |
| 0.20 | 6 |
| 0.30 | 13 |

`[UNVERIFIED]` — the arithmetic is ours; the bound is the paper's.

**The load-bearing detail is what counts as N.** Under protein-grouped cross-validation — which
this project requires, because no residue of a test protein may be trained on — the independent
unit is the protein, so N ≈ 100–150, not the ~80 000 residues. Using the residue count would
inflate T_max by a factor of ~500 and is the single easiest way to justify a circuit that cannot
generalise.

**This is already confirmed on our data.** The in-repo VQC used **24 trainable parameters** on 44
grouped proteins — which is above T_max even at ε = 0.30 — and scored 0.575, statistically
indistinguishable from unlearned ALPS at 0.576. The bound predicted the outcome.
`[VERIFIED-FULLTEXT]`

**And barren plateaus are not the binding constraint at this size.** With a budget of ~10 gates,
no circuit is deep enough to have a plateau. The binding constraint is the reverse one: at that
depth with a local observable, the model is in exactly the regime that is classically simulable
(*Nat. Commun.* 16, 7907 (2025)). The label supply, not the optimiser, is what closes the door.

---

## What this changes for our pipeline

1. **Do not build a quantum scorer.** (Stage 4.) The quantum kernel and the VQC were both run
   in-repo on our own features with the classical side tuned, and both tied or lost. Nothing
   retrieved this session gives a reason to run a third.
2. **Do not implement quantum reservoir computing.** (Stage 3/4.) The §5 gap is closed
   negatively: QRC is temporal, its static analogue is one POVM, its useful regime is classically
   simulable, and its survey states no advantage over matched classical reservoirs.
3. **Build an equivariant classical GNN instead.** (Stage 4.) This is the only lever in the file
   with a published matched-comparison gain — +4.5 AUC points, classical EGNN over plain GNN at
   matched parameter count — and our in-repo GNN has not tried it. It costs no quantum resource
   and violates no constraint.
4. **If we coarse-grain, guide the compression with the downstream objective.** (Stage 1.)
   Unguided compression dropped a classifier to 0.5797; guided compression lifted the same
   classifier to 0.8645. Reconstruction error alone is the wrong loss. Note the C1/C2 cost: any
   learned coarsening needs labels, and those labels must be held out from every scored arm.
5. **Budget the parameters before designing anything trainable.** (Stage 4.) T ≤ ε²N with N =
   proteins. At 150 proteins and ε = 0.2 that is six gates. Write this number into the method
   design, not into the discussion after the fact.
6. **Count the input gates in every resource table.** (Stage 2, and C3 directly.) The challenge
   requires circuit depth and qubit count for every quantum method. A table that reports the
   propagation circuit and omits the state preparation understates the cost by the dominant term.
   Our single-excitation encoding is one X gate — that is a genuine strength, and it should be
   stated as one.
7. **If a quantum subroutine is used at all, use it as a proposal, not as an answer.** (Any
   stage.) The one pattern with a *Nature*-level positive result puts the quantum device inside a
   classical accept/reject loop, so a wrong quantum output costs iterations and never
   correctness. Report the bound alongside it: no speedup for a unital proposal on an
   unstructured problem.
8. **Frame the report's hybrid claim around stage ownership, not around a quantum win.** The
   defensible claim is that AI owns stages 0–1 and 4, geometry owns stage 5, and the quantum
   stage is a topology-driven propagation whose cost is one X gate — not that a quantum model
   scored higher. No retrieved paper supports the second claim on a structural-biology task.

---

## Method

**Databases.** arXiv API (`export.arxiv.org/api/query`), Europe PMC search and `fullTextXML`,
NCBI/PMC article pages, publisher pages via WebFetch, and WebSearch for citation resolution.
Semantic Scholar was not attempted (rate limited per `00-conventions.md` §3).

**Queries run (18 arXiv, 3 Europe PMC, 5 WebSearch, 12 WebFetch).**
arXiv: `"quantum reservoir computing" AND graph`; `"quantum reservoir" AND ("classically
simulable" OR dequantization)`; `abs:"quantum reservoir computing"` sorted by date (60 records);
`abs:"quantum graph neural network"`; `abs:"quantum extreme learning machine"`; `"barren plateau"
AND "classically simulable"`; `ti:"barren plateaus" AND abs:simulation`; `generalization AND
"quantum machine learning" AND bounds`; `"data re-uploading"`; `"drug discovery" AND "hybrid
quantum"`; `"quantum generative" AND molecul`; `"state preparation" AND "quantum machine
learning"`; `"machine learning" AND "error mitigation"`; `"reinforcement learning" AND ansatz`;
`"reinforcement learning" AND "quantum circuit" AND compilation`; `"coarse-graining" AND quantum
AND "machine learning"`.
Europe PMC: `TITLE:"KRAS" AND ABSTRACT:"quantum"`; `("quantum machine learning" OR "quantum
computing") AND ("binding site" OR allosteric OR "protein structure prediction")`; DOI lookups.

**Counts.** ~430 records returned across all queries; 41 screened in on title and abstract; **9
full texts landed** (KRAS *Nat. Biotechnol.* via Europe PMC XML; JCTC Perspective PMC11099973;
QSyncFold PMC13221982; EQGNN arXiv HTML; Guided Graph Compression arXiv HTML; QRC on random
regular graphs arXiv HTML; sqRBM arXiv abstract page verbatim; plus two in-repo results files,
`allosteric-benchmark/hybrid/RESULTS.md` and `allosteric-benchmark/gnn/RESULTS.md`, read in
full). 21 further papers are cited from abstract or metadata records only and are tagged
`[VERIFIED-ABSTRACT]`.

**Stopping rule.** Stopped when three consecutive queries in a sub-topic returned only records
already screened, and when both halves of question (b) had at least one matched-control source
per pipeline stage or a recorded absence.

**What could not be reached this session.**
- The arXiv API returned HTTP 429 after roughly 20 requests and stayed blocked; later abstracts
  were obtained through WebFetch on `arxiv.org/abs/` pages instead. Some abstracts therefore
  arrived as a model's rendering of the page rather than as raw XML; where the exact wording is
  load-bearing the quote was re-fetched verbatim from the arXiv abstract block (sqRBM) or from
  Europe PMC (Layden).
- *Axioms* is open access but `mdpi.com` returned HTTP 403; the numbers in §A.3 come from the
  arXiv v3 HTML of the same paper, which carries the same Table 1.
- *Communications Physics* (sqRBM) and *Nature* (Layden) article pages were behind an identity
  redirect; abstracts were obtained from arXiv and Europe PMC respectively.
- Supplementary Tables 1–2 of the KRAS paper, which hold the per-variant success rates behind the
  21.5 % figure, are not in the Europe PMC full text and were not retrieved. The 21.5 % is quoted
  from the body text.
- No search was run on quantum annealing hardware for site selection; the QUBO route is already
  closed by measurement (`00-conventions.md` §5, item 6).
