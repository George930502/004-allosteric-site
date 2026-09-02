# Quantum and quantum-inspired node ranking on a classical graph, conditioned on a source set

**Scope:** algorithms whose output is a **score per vertex of a fixed classical graph**, where the
score may be conditioned on a named set of source vertices. Covers quantum PageRank and the Szegedy
family, open quantum walks and quantum stochastic walks, environment-assisted transport with a trap,
discrete-time coined and Grover walks, Ising/QUBO node-subset selection, tensor networks on graphs,
quantum reservoir computing, admissible routes to non-Hermitian and many-body structure, and the
long-time regime left open by the geometric-locality dequantization theorem. It deliberately excludes
quantum chemistry, VQE for molecules, bosonic/vibrational encodings of the elastic network, quantum
linear algebra, and everything with a trained readout other than reservoir computing.
**Sibling files:** `03-quantum-methods.md` (choice of propagation observable, bosonic encodings,
quantum linear algebra, GBS); `08-hardware-viability.md` (encodings, gate counts, Braket devices,
noise); `04-hybrid-quantum-ai.md` (trained models); `01-classical-baselines.md` (the classical bar).
**Retrieved:** 2026-08-26.

---

## 0. How to read this file against `00-conventions.md` §5

§5 lists eleven quantum insertion points measured and closed on a **different** repository's
benchmark. The principal investigator's standing instruction is that those closures are **prior, not
verdict**: a claim that a method "will not work" is withdrawn unless a real experiment on **our**
frozen benchmark produced a real number. This file therefore does three things and says which is
which:

1. **Names variants of the eleven that were not tested.** Three of them are load-bearing: item 3's
   dephasing sweep had no sink (§3); item 11's "no non-Hermitian structure" holds for the operator we
   chose to build, not for every operator the apo structure admits (§8); item 5's quantum-centrality
   closure was for a **graph-global** centrality, and personalisation is a one-line change (§2.3).
2. **Characterises quantum reservoir computing**, which §5 records as "the one candidate that
   appeared in the corpus and was never characterised" (§7). File 03 §11(e) dismisses it by deferral
   to file 04. That deferral rests on "a static contact graph is not a time series", which is correct
   for QRC and **wrong for its static sibling**, the quantum extreme learning machine. The dismissal
   still stands, but for a different and better reason: the supervision budget (§7.3).
3. **Brings the many-body / non-Hermitian question to a decision** (§8). §5's diagnosis says "a
   residue contact graph supplies neither". This file finds two constructions that supply one each,
   from apo coordinates only, with no MD and no holo.

Nothing here re-reports one of the eleven as new.

---

## 1. The frame: ranking is not centrality, and source-conditioning is the whole point

Our deliverable is a score per residue **relative to a named active site** (`CHALLENGE.md` §4.1). The
quantum-walk-on-graphs literature almost never computes that. It computes one of two things:

- **A graph-global centrality** — one number per vertex, no source argument. Quantum PageRank
  (doi:10.1038/srep00444), CTQW centrality (doi:10.1103/PhysRevA.95.032318), CTQW hub/authority
  scores (arXiv:2210.13379), and the protein application doi:10.1021/jacs.6c08053 are all of this
  type. `00-conventions.md` §5 item 5 and ADR 0002 already close this class: a graph-global
  centrality on a residue network reproduces eigenvector centrality.
- **A source-to-sink transport efficiency** — a scalar for one (source, sink) pair, from the
  transport/light-harvesting literature. This _is_ source-conditioned, and it is the branch this file
  argues has been under-read (§3, §8).

Classical **personalised** PageRank is source-conditionable by construction: the teleportation vector
is a free parameter. The quantum literature retrieved this session does not use that freedom (§2.3).
That is the single largest gap this file found in the ranking branch, and it is cheap to close.

Working sizes throughout: **N = 147–1058 residues**, mean contact degree ≈ 9.4, |E| = 809–3589,
measured in `08-hardware-viability.md` §1.1. All flop and dimension figures below were computed in
this session by elementary arithmetic, not recalled.

---

## 2. Quantum PageRank and the Szegedy family

### 2.1 The construction

**Paparo & Martin-Delgado**, "Google in a Quantum Network", _Sci. Rep._ **2**, 444 (2012),
doi:10.1038/srep00444 (arXiv:1112.2079). Read via `ar5iv` this session.

The classical input is the Google matrix

> **G := αE + (1−α)/N · 𝟙** `[VERIFIED-FULLTEXT]`

with E the column-stochastic hyperlink matrix, α the damping parameter, and 𝟙 the all-ones matrix.
The teleportation vector is **uniform, 1/N per page** `[VERIFIED-FULLTEXT]`.

The quantization is Szegedy's. The walk lives on the doubled space ℋ = ℂ^N ⊗ ℂ^N — one basis vector
per directed edge — with

> **|ψⱼ⟩ := |j⟩₁ ⊗ Σₖ √(Gₖⱼ) |k⟩₂**, **Π := Σⱼ |ψⱼ⟩⟨ψⱼ|**, **U := S(2Π − 𝟙)** `[VERIFIED-FULLTEXT]`

and the walk operator used in the algorithm is U². The readout is the **instantaneous quantum
PageRank**

> **I_q(Pᵢ, m) = ‖ Σ_μ μ^(2m) ₂⟨i|μ⟩⟨μ|ψ(0)⟩ ‖²** `[VERIFIED-FULLTEXT]`

and its time average

> **⟨I_q(Pᵢ)⟩ := (1/M) Σ\_{m=0}^{M−1} I_q(Pᵢ, m)** `[VERIFIED-FULLTEXT]`

The underlying discrete-time walk from a Markov chain is **Szegedy**, FOCS 2004,
doi:10.1109/focs.2004.53 `[UNVERIFIED — DOI carried from file 03; not re-verified this session]`.

### 2.2 What it is claimed to detect that classical PageRank does not

Three published claims, all on synthetic or WWW graphs, none on a molecular network.

- **Secondary hubs.** Paparo, Müller, Comellas & Martin-Delgado, "Quantum Google in a Complex
  Network", _Sci. Rep._ **3**, 2773 (2013), doi:10.1038/srep02773 (arXiv:1303.3891): the algorithm
  "is capable to clearly highlight the structure of secondary hubs of the network, and to partially
  resolve the degeneracy in importance of the low lying part of the list of rankings, which
  represents a typical shortcoming of the classical PageRank algorithm" `[VERIFIED-ABSTRACT]`. Same
  paper: "the quantum PageRank algorithm generically leads to changes in the hierarchy of nodes"
  `[VERIFIED-ABSTRACT]`.
- **Degeneracy lifting among peripheral nodes.** Loke, Tang, Rodriguez, Small & Wang, "Comparing
  classical and quantum PageRanks", _QIP_ **16**, 25 (2017), arXiv:1511.04823: "the quantum measures
  better highlight secondary hubs and resolve ranking degeneracy among peripheral nodes for the
  networks we studied" `[VERIFIED-ABSTRACT]`. They also report that "the required time of evolution
  does not scale significantly with increasing network size" `[VERIFIED-ABSTRACT]`.
- **Not all detected secondary hubs are real.** Ortega & Martin-Delgado, _Phys. Rev. Research_ **5**,
  013061 (2023), doi:10.1103/PhysRevResearch.5.013061 (arXiv:2209.13451): "the original quantum
  PageRank is able to break the degeneracy of the residual nodes and detect secondary hubs that the
  classical algorithm suppresses. Nevertheless, **not all of the detected secondary hubs are real
  according to the PageRank's definition.** Some APR schemes can overcome this problem"
  `[VERIFIED-ABSTRACT]` (emphasis ours). This is a **false-positive warning from inside the method's
  own literature** and it must be quoted in any report section that leans on the secondary-hub claim.

Related variants retrieved: arbitrary-phase-rotation clustering behaviour, Zhang et al.
arXiv:2411.13114 `[VERIFIED-ABSTRACT]`; graph-phased Szegedy walks with link phases and local APR,
Ortega & Martin-Delgado, _Phys. Rev. A_ **111**, 032216 (2025), doi:10.1103/PhysRevA.111.032216 —
"local APR phases emerge as powerful tools for marking graph nodes, optimizing quantum searches
**without altering graph structure**" `[VERIFIED-ABSTRACT]`; a discrete-time **open** quantum walk
PageRank, Dutta, _Phys. Rev. E_ **111**, 034312 (2025), doi:10.1103/PhysRevE.111.034312
`[VERIFIED-ABSTRACT]`; a directed-DTQW ranking, Chawla, Mangal & Chandrashekar arXiv:1905.06575, which
notes explicitly that "for non-trivial cyclic networks, the hierarchy of quantum ranks do not exactly
match to the hierarchy of the classical rank" `[VERIFIED-ABSTRACT]` — our graphs have 7.7–8.3 cycles
per residue (`00-conventions.md` §5 item 8), so this is the regime we would be in.

**Why the secondary-hub claim is the one worth our attention.** Our failure mode is precisely a
degenerate low-lying tail: distal candidate residues that classical centrality cannot separate, all
scoring near the graph-periphery floor. The published claim is about exactly that part of the list.
It has never been tested on a residue network with allosteric labels.

### 2.3 Is quantum PageRank conditionable on a source set? Yes, and nobody has done it

The damping term is the only place the source could enter, and in every construction retrieved this
session it is **uniform**. Classical PageRank's personalisation replaces (1−α)/N·𝟙 with
(1−α)·**v**·𝟙ᵀ for an arbitrary probability vector **v**. Nothing in the Szegedy quantization touches
that choice: G stays column-stochastic, |ψⱼ⟩ stays normalised, U stays unitary. Setting **v** to the
uniform distribution over the active-site residues yields a **personalised quantum PageRank**, a
source-conditioned per-residue score.

Searches for a published personalised or topic-sensitive quantum PageRank returned nothing (see
Method). Per ADR 0019 this is **not** an absence-of-prior-art claim; it is the outcome of the
recorded queries. `[UNVERIFIED — the construction is ours; the two ingredients (the G definition and
the Szegedy quantization) are `[VERIFIED-FULLTEXT]` above]`

Two properties make this worth building even though the unpersonalised version is inside §5 item 5's
closure:

- The score becomes a function of the active site, so it is no longer a graph-global centrality and
  §5 item 5 does not cover it.
- The **classical** personalised PageRank from the same **v** is a one-line control that must be run
  beside it. If the quantum version's only content is the classical personalised vector, the
  comparison says so immediately and cheaply — and personalised PageRank from the active site is
  itself a baseline we do not currently have.

**A caution that should be recorded before, not after, the run.** Personalised PageRank from a source
set concentrates on nodes near the source in graph distance. `00-conventions.md` §5 records that
`ctrl_closeness = −distance` already reaches AUC 0.617. A personalised ranking is at high risk of
being a proximity ranker in a new costume. The stratified evaluation in the frozen protocol is what
would catch that, and it must be applied.

### 2.4 Resources (C3) and hardware path (C4)

Two encodings, both instantiated at our sizes. Arithmetic ours.

| Encoding                            | Qubits at N = 147 / 272 / 1058 | Two-qubit gates **per walk step**                  | Depth          | Connectivity   |
| ----------------------------------- | ------------------------------ | -------------------------------------------------- | -------------- | -------------- |
| Binary, doubled register (2⌈log₂N⌉) | 16 / 18 / 22                   | ≈ 2·N_pad² = 131,072 / 524,288 / 8,388,608         | same order     | any            |
| One-hot, doubled register (2N)      | 294 / 544 / 2116               | O(N²) ≈ 2·N(N−1)/2 per controlled reflection block | O(N) per block | line per block |

The binary figure is a **multiplexed state-preparation** count: the reflection 2Π−𝟙 needs the isometry
|j⟩|0⟩ ↦ |ψⱼ⟩, which is N different n-qubit state preparations selected by an n-qubit address, at
≈2^{n+1} CNOTs each, giving ≈2·2^{2n} = 2·N_pad² with N_pad = 2^{⌈log₂N⌉}. `[UNVERIFIED — our
arithmetic; the generic state-preparation cost is the standard Shende–Bullock–Markov figure quoted in
`08-hardware-viability.md` §2.3]`

**There is no sparsity escape, and the reason is structural.** File 08 §2.3 shows the compressed
encoding is only viable when the matrix entries follow a rule. G is worse than an arbitrary sparse
matrix: the damping term **(1−α)/N** makes **every entry of G strictly positive**, so G is dense by
construction whatever the contact graph looks like. Loke & Wang, "Efficient quantum circuits for
Szegedy quantum walks", _Ann. Phys._ **382**, 64 (2017), doi:10.1016/j.aop.2017.04.006, give efficient
circuits only for chains "possessing **transformational symmetry in the columns of the transition
matrix**", instantiated on "cyclic permutations and complete bipartite graphs"
`[VERIFIED-ABSTRACT]` (emphasis ours). A residue contact graph has neither.

**Comparison that decides it.** File 08's exact Givens network for a single-excitation CTQW at N = 272
costs 36,856 two-qubit gates at depth 272 on 272 qubits. Quantum PageRank at the same N costs
≈524,288 two-qubit gates **per step**, and the time average needs M steps. That is a factor of ≈14
per step before the average, on 18 qubits that must all survive it. **C3 verdict: quantum PageRank is
not a near-term circuit at our sizes.** Its honest C4 path is fault-tolerant, and the report should
say so rather than citing the 2012 headline.

**But the classical simulation is trivial**, which is what makes it worth testing. Ortega &
Martin-Delgado's SQUWALS simulator "scales as O(N²) in both time and memory resources",
doi:10.1002/qute.202400022 (arXiv:2307.14314) `[VERIFIED-ABSTRACT]`; the successor SQWLib reaches
"optimal O(N²) complexity for dense graphs" and "scales linearly with the number of edges" for sparse
graphs (arXiv:2606.14226) `[VERIFIED-ABSTRACT]`. At N = 1058 the Szegedy state has N² = 1,119,364
complex amplitudes = 17.1 MiB; a step is ≈10⁶ operations. A 1000-step time average is ≈10⁹
operations. Seconds.

An earlier and much worse classical route exists and should be avoided: Tang et al. arXiv:2003.04930
report that the Lindblad formulation "needs to solve the Kronecker products of an O(N⁴) dimension and
requires severely large memory and time when the number of nodes N in a network increases above 150"
`[VERIFIED-ABSTRACT]`. At N = 1058, N⁴ = 1.25×10¹². Use the Szegedy formulation, not the Lindblad
one.

---

## 3. Open quantum walks, quantum stochastic walks, and the ENAQT term the sweep did not have

### 3.1 The interpolation

**Whitfield, Rodríguez-Rosario & Aspuru-Guzik**, _Phys. Rev. A_ **81**, 022323 (2010),
doi:10.1103/PhysRevA.81.022323 (arXiv:0905.2942): the quantum stochastic walk "determines the
evolution of generalized quantum mechanical walk on a graph that obeys a quantum stochastic equation
of motion … the family of possible QSWs encompasses both the classical random walk (CRW) and the
quantum walk (QW) as special cases, but also includes more general probability distributions"
`[VERIFIED-ABSTRACT]`. The interpolation parameter multiplies the Lindblad dissipator against the
coherent term.

**Attal, Petruccione & Sinayskiy**, "Open Quantum Walks on Graphs", arXiv:1401.3305: OQWs "are
formulated as quantum Markov chains on graphs" and are "exclusively driven by the interaction with
the external environment" `[VERIFIED-ABSTRACT]`. The OQW limit is fully incoherent; the QSW spans the
range.

Two facts constrain any QSW proposal and both come from inside the field:

- **Physical realizability is not free.** Taketani, Govia & Wilhelm, arXiv:1603.03699: "general
  implementations would require the complete solution of the underlying unitary dynamics, and
  sophisticated reservoir engineering, thus **weakening the benefits of experimental investigation**"
  `[VERIFIED-ABSTRACT]` (emphasis ours). A QSW is not automatically a hardware-viable object.
- **Naive QSWs on directed graphs corrupt the topology.** Domino, Głos & Ostaszewski,
  arXiv:1701.04624: the global-environment QSW produces "additional amplitude transitions … hence
  graph topology is changed into **moral graph**. Because of that we call the effect a spontaneous
  moralization" `[VERIFIED-ABSTRACT]`. They give a correction scheme. Anyone building §8.2's directed
  walk as a QSW must apply it.

Classical simulator that removes the tooling excuse: QSW_MPI, Matwiejew & Wang, arXiv:2003.02450,
"scalable to massively parallel computers, which makes possible the simulation of a wide range of walk
dynamics on directed and undirected graphs of arbitrary complexity" `[VERIFIED-ABSTRACT]`.

### 3.2 The ENAQT optimum needs a trap, and the closed sweep did not have one

File 03 §5 already establishes, from Zerah-Harush & Dubi (arXiv:1801.06799), that ENAQT arises from
"the tendency of dephasing to make the exciton population uniform, and **the formation of an exciton
density gradient, defined by the source and the sink**" `[VERIFIED-FULLTEXT, quoted in file 03]`.
This file adds the confirming independent line and, more importantly, a **different control
parameter**.

The sink is not a detail. It converts the Hamiltonian into a non-Hermitian effective operator, and the
transport optimum lives in **that** parameter, not in the dephasing rate.

**Celardo, Borgonovi, Merkli, Tsifrinovich & Berman**, "Superradiance Transition in Photosynthetic
Light-Harvesting Complexes", _J. Phys. Chem. C_ **116**, 22105 (2012), doi:10.1021/jp302627w
(arXiv:1111.5443):

> "The excitation energy transfer due to the coupling of the light harvesting complex to the reaction
> center ('sink') is analyzed using an **effective non-Hermitian Hamiltonian**. We show that, **as the
> coupling to the reaction center is varied, maximal efficiency in energy transport is achieved in the
> vicinity of the superradiance transition**, characterized by a segregation of the imaginary parts of
> the eigenvalues of the effective non-Hermitian Hamiltonian. Our results demonstrate that the presence
> of the sink (which provides a quasi-continuum in the energy spectrum) **is the dominant effect in the
> energy transfer which takes place even in absence of a thermal bath.**" `[VERIFIED-ABSTRACT]`
> (emphasis ours)

The general transport statement is **Celardo & Kaplan**, _Phys. Rev. B_ **79**, 155108 (2009),
doi:10.1103/PhysRevB.79.155108: "a transition to a superradiant regime is shown to occur … **transport
properties undergo a strong change at the superradiance transition, where the transmission is
maximized** and a drastic change in the structure of resonances is demonstrated" `[VERIFIED-ABSTRACT]`.

**This is the precise statement that `00-conventions.md` §5 item 3's γ sweep could not reach.** A
sweep over the dephasing rate γ with no sink has no absorbed population to maximise. The published
non-monotonicity is in the **opening strength Γ** — the coupling to the drain — and it exists "even in
absence of a thermal bath". `[UNVERIFIED — our reading; the two quoted sentences are
`[VERIFIED-ABSTRACT]`]`

### 3.3 The Bethe-lattice result: the optimum is an exceptional point, and the setup is ours

**Hatano, Katsura & Kawabata**, "Quantum transport on Bethe lattices with non-Hermitian sources and a
drain", _J. Phys. A: Math. Theor._ **59**, 175002 (2026), doi:10.1088/1751-8121/ae5d23
(arXiv:2409.01873). This is the closest published construction to what we would build.

> "We consider quantum transport in a tight-binding model on the Bethe lattice of finite generation,
> which we expect to be the first step toward analyzing electronic transport in a light-harvesting
> molecule." `[VERIFIED-ABSTRACT]`

> "As a new feature for analyzing quantum transport, we add **complex potentials for sources at
> peripheral sites and a drain at the central site, and solve a non-Hermitian eigenvalue problem,
> instead of simulating an initial-value problem.**" `[VERIFIED-ABSTRACT]` (emphasis ours)

> "**The current has a maximum with respect to the strengths of the sources and the drain.** The
> current decreases as we increase the strengths beyond the maximum and vanishes in the limit of
> infinite strength." `[VERIFIED-ABSTRACT]`

> "the current takes the maximum value **at the exceptional point where two eigenstates coalesce to a
> zero mode**, which emerges because of the non-Hermiticity due to the PT-symmetric complex
> potentials." `[VERIFIED-ABSTRACT]`

Three things follow.

1. The **method** is an eigenvalue problem on an N×N non-Hermitian matrix, not a time propagation.
   Cost is what we already pay for ALPS.
2. The **source set is named** and the **drain is named**. That is our problem statement.
3. The observable — the argmax over Γ, and the exceptional-point condition at it — is a property of
   the complex spectrum of H − i(Γ/2)|d⟩⟨d|. It is **not** a function of |⟨d|e^{−iHt}|s⟩| alone.

They also report the honest degradation: "By introducing randomness either into the hopping amplitude
or the number of links in each generation of the tree … the current reaches its maximum not exactly,
but approximately, for a zero mode, although **it is no longer located at an exceptional point in
general**" `[VERIFIED-ABSTRACT]`. A protein contact graph is far more irregular than a
random-hopping Bethe lattice. Expect the exceptional point to be approximate at best, and expect the
argmax in Γ to survive as the usable quantity.

### 3.4 Supporting and cautionary results in this branch

- **Transport efficiency of a CTQW with a single trap, on graphs of varying topology.** Razzoli, Paris
  & Bordone, _Entropy_ **23**, 85 (2021), doi:10.3390/e23010085 (arXiv:2011.13794): they "assume a
  single trap vertex accountable for the loss processes" and "for each graph, analytically determine
  the subspace of states having maximum transport efficiency". Their conclusion is the one that makes
  this interesting for allostery: "**connectivity is a poor indicator for transport efficiency**"
  `[VERIFIED-ABSTRACT]` (emphasis ours). Degree and burial are exactly the confound ADR 0002 names
  under Known risks; here is a published statement that trapped-CTQW efficiency is not that.
- **ENAQT and mobility edges.** Dwiputra & Zen, _Phys. Rev. A_ **104**, 022205 (2021),
  doi:10.1103/PhysRevA.104.022205: ENAQT "increases by orders of magnitude and depends on the number
  of localized eigenstates and disorder strength nonmonotonically … the result of the cooperation
  between population uniformization and localization" `[VERIFIED-ABSTRACT]`.
- **Interactions hurt.** Zerah-Harush & Dubi, arXiv:2005.04462: "repulsive interactions are
  detrimental to ENAQT, and lead to an environment-hampered quantum transport"
  `[VERIFIED-ABSTRACT]`. Relevant to §8.3 — do not expect ENAQT and the many-body route to compound.
- **It has been observed on hardware.** Maier et al., _Phys. Rev. Lett._ **122**, 050501 (2019),
  doi:10.1103/PhysRevLett.122.050501: ENAQT in a 10-qubit trapped-ion spin network "subject to
  engineered static disorder and temporally varying dephasing noise", showing "a crossover from
  coherent dynamics and Anderson localization to ENAQT and finally a suppression of transport due to
  the quantum Zeno effect" `[VERIFIED-ABSTRACT]`. Note both ingredients present: **engineered
  disorder** and a defined transfer endpoint.
- **The size-dependence caveat.** Skalkin, Unanyan & Fleischhauer, arXiv:2502.10854, on a 2D lossy
  lattice: "for **system sizes below a characteristic scale** it can be substantially enhanced by
  adding small dephasing noise" `[VERIFIED-ABSTRACT]` (emphasis ours). Whether N = 147–1058 is below
  that scale for a contact graph is unknown and would have to be measured.

### 3.5 Resources for the trapped/open branch

**Classical.** The single-excitation non-Hermitian generator is an N×N complex matrix. One
eigendecomposition is O(N³): 3.18×10⁶ (N=147), 2.01×10⁷ (N=272), 1.18×10⁹ (N=1058) flops. Sweeping the
drain over all N residues at G values of Γ costs G·N·O(N³) in the worst case — 1.25×10¹² at N=1058,
G=1, which is hours. The cheap route is a **steady-state linear solve** with the factorisation reused
across drains: G·[O(N³) + N·O(N²)] ≈ 2G·N³, i.e. 8.0×10⁸ flops at N=272 with G=20. Seconds. Use the
linear solve; reserve the eigendecomposition for the exceptional-point diagnostic.

Full Lindblad (dephasing plus trap) is N² density-matrix entries — 1,119,364 complex = 17.1 MiB at
N=1058 — with a sparse Liouvillian; Krylov integration avoids forming the N⁴ dense object (1.25×10¹²
entries).

**Quantum (C3/C4).** This is the cheapest hardware story in the file, and it is the reason the branch
is worth the effort. Take file 08 §2.1's one-hot single-excitation encoding and its exact Givens
network — N qubits, N(N−1)/2 two-qubit gates, depth N, line connectivity. A drain at residue d is
**one extra qubit** plus, per absorption step, **one two-qubit partial-SWAP between qubit d and the
ancilla followed by a mid-circuit reset of the ancilla**. Over r absorption steps that is r extra
two-qubit gates and r resets, and the observable — total absorbed population — is read directly from
the ancilla's cumulative reset outcomes.

|    N | qubits | 2q gates (Givens) | + sink at r = 32 |     depth | connectivity |
| ---: | -----: | ----------------: | ---------------: | --------: | ------------ |
|  147 |    148 |            10,731 |           10,763 |  147 + 32 | line         |
|  272 |    273 |            36,856 |           36,888 |  272 + 32 | line         |
| 1058 |   1059 |           559,153 |          559,185 | 1058 + 32 | line         |

`[UNVERIFIED — our construction and arithmetic; the Givens ingredient is `[VERIFIED-FULLTEXT]` in file
08 §2.1 from doi:10.1364/OPTICA.3.001460 and arXiv:1711.04789]`

The sink costs **0.3 % of the gate budget** at N = 147. The binding constraint is unchanged from file
08 §5.3: at 99.5 % two-qubit fidelity the coherent budget is ≈200 two-qubit gates, so a hardware run
is N ≈ 20 coarse-grained nodes. Mid-circuit reset availability on the Braket devices was **not checked
this session** and is flagged as an open item for file 08.

---

## 4. Discrete-time walks: coined, Grover, Szegedy — trapping, localisation, percolation

### 4.1 Asymptotic trapping: a source-and-sink observable with no continuous-time analogue

**Mareš, Novotný, Štefaňák & Jex**, "Key graph properties affecting transport efficiency of flip-flop
Grover percolated quantum walks", _Phys. Rev. A_ **105**, 062417 (2022),
doi:10.1103/PhysRevA.105.062417 (arXiv:2202.09582):

> "Quantum walks exhibit properties without classical analogues. One of those is the phenomenon of
> **asymptotic trapping** — there can be non-zero probability of the quantum walker being localised in
> a finite part of the underlying graph indefinitely even though locally all directions of movement are
> assigned non-zero amplitudes at each step." `[VERIFIED-ABSTRACT]`

> "we provide a recipe for the construction of a complete basis of the subspace of trapped states
> allowing to determine the asymptotic probability of trapping **for arbitrary finite connected simple
> graphs** … We show how **the position of the source and sink** together with the graph geometry and
> its modifications affect the excitation transport. This gives us a deep insight into processes where
> **elongation or addition of dead-end subgraphs may surprisingly result in enhanced transport**."
> `[VERIFIED-ABSTRACT]` (emphasis ours)

Four properties make this a real candidate rather than a curiosity:

1. It is defined **for arbitrary finite connected simple graphs**, not a designed family. Almost
   nothing else in the discrete-time literature is.
2. It takes a **source and a sink** as arguments.
3. The observable is the **asymptotic** trapping probability — a t → ∞ quantity computed from a
   subspace, not from a propagator at a chosen time. It therefore does not inherit the
   time-hyperparameter fragility that `00-conventions.md` §5 item 8 records for chiral walks.
4. "Dead-end subgraphs enhance transport" is an **anti-correlation with degree**. Our documented
   failure mode is scores collapsing onto burial and degree. This observable's published behaviour
   runs the other way.

The precondition is that the walk has a coin register, so the object lives on directed edges: dimension
2|E| = 1618 (KRAS, |E|=809) to 7178 (myosin, |E|=3589). The trapped subspace is a null-space
computation, worst case O(|E|³) = 5.3×10⁸ at |E|=809 and 4.6×10¹⁰ at |E|=3589. Minutes on a
workstation.

Predecessor results, for the report's citation chain: Kollár, Novotný, Kiss & Jex, arXiv:1204.6149,
give the analytic method for coined percolated walks and find "a rich variety of asymptotic evolutions
… not only the fully mixed state, but other stationary states; stable periodic and quasiperiodic
oscillations can emerge, depending on the coin operator, the initial state, and the topology"
`[VERIFIED-ABSTRACT]`; Mareš, Novotný & Jex, arXiv:1812.02519, extend the shift operator to graphs of
varying degree and connect the non-stationary asymptotics to the existence of an **edge-3-colouring**
`[VERIFIED-ABSTRACT]` — file 08 §1.1 measures our greedy edge colouring at 16–17 classes at every
size, so that specific criterion does not apply and the general recipe of arXiv:2202.09582 must be
used instead.

### 4.2 Localisation from clustering, and the dynamical IPR

`00-conventions.md` §5 item 5 closed "eigenvector content and mode IPR" at 63.6 % and 36.4 %. Two 2025–26
results identify a **different** IPR that was not in that test.

**Böttcher & Porter**, "Clustering-induced localization of quantum walks on networks", _Phys. Rev. E_
**112**, L062301 (2025), doi:10.1103/pp6q-n7mx (arXiv:2412.04325): "we demonstrate how localization
emerges in highly clustered networks … and we derive an analytical expression for the **long-time
inverse participation ratio** that depends on products of eigenvectors of the quantum-walk
Hamiltonian … **local clustering, which is a key structural feature of networks, can induce
localization of quantum walks**" `[VERIFIED-ABSTRACT]` (emphasis ours).

**Dhamapurkar & Subrahmanyam**, "Localization Without Disorder: Quantum Walks on Structured Graphs",
arXiv:2603.05643 (2026-03-05): "**the dynamical IPR can exceed expectations based solely on eigenstate
IPRs**, demonstrating that coherent superposition within degenerate eigenspaces enhances confinement.
By connecting IPR values to the effective number of vertices visited, we provide a structural
diagnostic for predicting quantum transport outcomes in modular networks, establishing that
connectivity alone can determine where and how strongly a quantum walk localizes"
`[VERIFIED-ABSTRACT]` (emphasis ours).

The distinction matters and is precise: **eigenstate IPR** is a property of H's eigenvectors, and it
is closed. **Dynamical IPR** of a wavepacket launched from the active site is a property of the
evolved state, is source-conditioned, and is sensitive to coherent superposition within degenerate
subspaces — which is exactly the structure `00-conventions.md` §5 item 4 measured to exist (3.6 % of
low gaps below 1 %) and then discarded. That said, the dynamical IPR is built from the same propagator
as item 1, so the honest prior is that it is a **transform of the transfer amplitudes, not
independent of them**. It is listed in §10 accordingly.

### 4.3 The robustness caveat that should temper the whole DTQW branch

**Duda, Ivaki, Sahlberg, Pöyhönen & Ojanen**, _Phys. Rev. Research_ **5**, 023150 (2023),
doi:10.1103/PhysRevResearch.5.023150 (arXiv:2210.05310), on percolation-generated 2D random lattices:

> "even **arbitrarily weak concentrations of randomly removed lattice sites give rise to a complete
> breakdown of the superdiffusive quantum speed-up**, reducing the motion to ordinary diffusion. By
> increasing the randomness, quantum walks eventually stop spreading due to Anderson localization …
> **The fragility of quantum speed-up implies dramatic limitations for quantum information
> applications of quantum walks on random geometries and graphs.**" `[VERIFIED-ABSTRACT]` (emphasis
> ours)

A protein contact graph is a random irregular geometry by any reasonable reading. This is the single
strongest published reason to expect the DTQW branch's _speed_ advantage to be absent on our input. It
says nothing about the _information content_ of the trapping observable in §4.1, which is not a
speed claim — and that distinction is what makes §4.1 survivable while the "quadratically faster
hitting" framing does not.

### 4.4 Published node-ranking uses of DTQWs, and one structural-anomaly result

- Chawla, Mangal & Chandrashekar, arXiv:1905.06575 — directed DTQW node ranking, applicable to "all
  directed networks"; the authors themselves suggest applying it "to model the dynamics on networks
  mimicking the chemical complexes and rank active centers in order of reactivities"
  `[VERIFIED-ABSTRACT]`. That is the closest published statement of intent to our problem.
- Dutta, doi:10.1103/PhysRevE.111.034312 — discrete-time **open** quantum walk PageRank with Weyl
  Kraus operators, compared across scale-free, Erdős–Rényi, Watts–Strogatz and spatial networks
  `[VERIFIED-ABSTRACT]`.
- Hillery, Zheng, Feldman, Reitzner & Bužek, _Phys. Rev. A_ **85**, 062325 (2012),
  doi:10.1103/PhysRevA.85.062325: quantum walks "to find structural anomalies in graphs … under some
  circumstances, a quantum walk can be used to **find where the connectivity of a network changes**"
  `[VERIFIED-ABSTRACT]`. Framed as search, but the underlying object — a walk that is sensitive to a
  local topological anomaly — is conceptually close to a perturbation-response metric, and the speedup
  is O(√N) on star-like graphs only.
- The hardware ceiling for this whole branch is already in file 08 §5.3: the largest published DTQW on
  a complex graph is **17 nodes, 20 edges, 40 qubits, 287 entangling layers** (arXiv:2602.24053).

### 4.5 Resources

| Object | Classical dimension at |E| = 809 / 3589 | Classical cost | Qubits (one directed-edge sector) |
| --- | --- | --- | --: |
| Grover flip-flop DTQW state | 1,618 / 7,178 | O(\|E\|) per step | 2\|E\| = 1,618 / 7,178 |
| Trapped subspace basis | same | O(\|E\|³) = 5.3×10⁸ / 4.6×10¹⁰ | n/a (classical only) |
| Dynamical IPR of a CTQW | N | one O(N³) `eigh`, then O(N²) per t | N (Givens network, file 08) |

The 2|E| qubit requirement is the reason arXiv:2602.24053 needed 40 qubits for 17 nodes. For a
continuous-time walk we need only N (file 08 §2.3), a further ≈9.5× saving. **If a discrete-time
observable is chosen, the qubit budget is ~9.5× worse than the continuous-time one at the same N**,
and file 08's N ≈ 20 ceiling becomes N ≈ 2–3. Discrete-time observables are therefore
classical-simulation-only candidates for us; their C4 story is fault-tolerant.

---

## 5. Annealing, QUBO and Ising for node-subset selection

`00-conventions.md` §5 item 6 closed cooperative site selection as a QUBO because classical annealing
hit the exhaustive optimum at every size up to C(34,7) = 5,379,616 (computed this session). The brief
asks whether any published formulation is hard enough that this would not happen.

### 5.1 The mechanism behind item 6, named

The likely reason the classical solver was exact is **submodularity**, not luck. Lynn & Lee,
"Maximizing Activity in Ising Networks via the TAP Approximation", arXiv:1803.00110: "In the discrete
setting where one chooses a small set of influential nodes, the problem is equivalent to the famous
influence maximization problem in social networks … we provide **sufficient conditions for when the
objective is submodular, allowing a greedy algorithm to achieve an approximation ratio of 1−1/e**"
`[VERIFIED-ABSTRACT]` (emphasis ours). A submodular set function of small cardinality on 34 candidates
is exactly the regime where greedy and annealing meet the optimum. `[UNVERIFIED — our attribution of
item 6's behaviour to submodularity; the theorem is `[VERIFIED-ABSTRACT]`]`

Recording this converts item 6 from "annealing was good enough" into "the objective we chose was
easy". That is a stronger and more useful statement for the report.

### 5.2 The non-submodular candidates, and why they still fail

The natural escape is a **non-submodular** node-subset objective. Densest-k-subgraph is the canonical
one and it has an established quantum framing — Gaussian boson sampling, Arrazola & Bromley, _Phys.
Rev. Lett._ **121**, 030503 (2018), doi:10.1103/PhysRevLett.121.030503 `[VERIFIED-ABSTRACT]`. File 03
§8 already closes this on the non-negativity argument (doi:10.1103/PRXQuantum.5.020341). Two 2025–26
results retrieved this session **strengthen** that closure rather than weaken it:

- Zhang et al., arXiv:2505.02445: a double-loop Glauber dynamics whose stationary distribution matches
  the GBS distribution, proved to "mix in polynomial time for dense graphs", improving random search
  and simulated annealing "for the max-Hafnian and densest k-subgraph problems **up to 10×**" on
  256-vertex unweighted graphs `[VERIFIED-ABSTRACT]`.
- Raghuraman, Patwardhan & La Cour, arXiv:2507.17567: a **classical** threshold-based GBS simulator
  that "provides better solutions in a comparable amount of samples for graphs with up to **2000
  nodes**" `[VERIFIED-ABSTRACT]`.

A classical sampler matching GBS on 2000-node graphs is larger than our largest arm. This branch is
closed on measurement by third parties, at our scale.

### 5.3 The fault-tolerant resource verdict, which is the number to quote

Even where a Szegedy walk does provide the quadratic speedup it is designed for, the compilation is
known. **Sanders, Berry, Costa, Tessler, Wiebe, Gidney, Neven & Babbush**, "Compilation of
Fault-Tolerant Quantum Heuristics for Combinatorial Optimization", arXiv:2007.07391:

> "Our results **discourage the notion that any quantum optimization heuristic realizing only a
> quadratic speedup will achieve an advantage over classical algorithms** on modest superconducting
> qubit surface code processors … our analysis suggests that quantum accelerated simulated annealing
> would require **roughly a day and a million physical qubits** to optimize spin glasses that could be
> solved by classical simulated annealing in about **four CPU-minutes**." `[VERIFIED-ABSTRACT]`
> (emphasis ours)

They compile "quantum accelerated simulated annealing including those using qubitization or **Szegedy
walks** to quantize classical Markov chains" `[VERIFIED-ABSTRACT]`. This is the same primitive as
quantum PageRank in §2. **C3/C4 verdict for the whole optimisation branch: no near-term path, and the
fault-tolerant path is quantified and unfavourable.**

**Quantum submodular minimisation** exists — Hamoudi, Rebentrost, Rosmanis & Santha, _QIC_ **19**,
1325 (2019), arXiv:1907.05378, at Õ(n^{5/4}/ε^{5/2}·EO) queries against a classical Õ(n^{3/2}/ε²·EO)
`[VERIFIED-ABSTRACT]` — a polynomial improvement in the query model only, with the same oracle-cost
objection file 08 §3.4 raises for every oracle result. It does not change the picture.

---

## 6. Quantum-inspired tensor networks on graphs

File 03 §9 states the tree-width argument and tags the protein-specific claim `[UNVERIFIED]`. This
file supplies the sourcing and does not overturn the conclusion.

The governing result is **Markov & Shi**, _SIAM J. Comput._ **38**, 963 (2008), doi:10.1137/050644756;
the operational restatement is **Dumitrescu, Fisher, Goodrich, Humble, Sullivan & Wright**,
arXiv:1807.04599: "**optimal contraction sequences correspond to optimal (minimum width) tree
decompositions of a tensor network's line graph** … computing optimal contraction sequences in general
is known to be a computationally difficult (NP-complete) task" `[VERIFIED-ABSTRACT]` (emphasis ours).
O'Gorman, arXiv:1906.00013, sharpens the correspondence: "the edge congestion of a graph is almost
equal to the branchwidth of its line graph" `[VERIFIED-ABSTRACT]`.

Two practical routes exist for graphs that are not tree-like:

- **Hyper-optimised approximate contraction.** Gray & Chan, arXiv:2206.07044: contraction "through
  bond compression on arbitrary graphs", with "a hyper-optimization over the compression and
  contraction strategy itself", demonstrated on "random regular graphs" and "graphs with many
  thousands of tensors" `[VERIFIED-ABSTRACT]`.
- **Tensor-network message passing.** Wang, Zhang, Pan & Zhang, arXiv:2305.01874: combines "the
  strengths of tensor networks in contracting small sub-graphs with many short loops and the strengths
  of message-passing methods in globally sparse graphs"; it is "**exact for systems that are globally
  tree-like and locally dense-connected**" `[VERIFIED-ABSTRACT]` (emphasis ours). A residue contact
  graph is locally dense (degree 9–16) but **not** globally tree-like — it has 7.7–8.3 independent
  cycles per residue. The stated exactness condition fails.

**Verdict, unchanged from file 03 and now sourced.** Tensor networks are not a scorer here. They are
the **classical simulator that would check** a many-body proposal (§8.3) at sizes where exact
diagonalisation runs out — and for our two- and three-excitation sectors exact sparse Krylov is
already enough (§8.3), so we would not need them. Their role in this project is as a reference
implementation, not a method.

One relevant negative datum on the quantum-inspired framing generally: Morais, Osaba, Pastor & Oregui,
arXiv:2504.05989, benchmark DMRG against a genetic algorithm and a GNN on weighted Max-Cut at 10–250
nodes and find the tensor-network approach "consistently yields high approximation ratios and
efficient execution on larger graphs, **albeit with increased memory consumption**"
`[VERIFIED-ABSTRACT]`. It is competitive, not dominant.

---

## 7. Quantum reservoir computing — the characterisation `00-conventions.md` §5 asks for

§5 records QRC as "the one candidate that appeared in the corpus and was never characterised". Here it
is characterised. File 03 §11(e) defers to file 04 and concludes "a static contact graph is not a time
series". That reason is **partly wrong** — the static sibling exists — and the correct blocker is
different and firmer.

### 7.1 What the reservoir is

**Fujii & Nakajima**, "Harnessing disordered quantum dynamics for machine learning", _Phys. Rev.
Applied_ **8**, 024030 (2017), doi:10.1103/PhysRevApplied.8.024030 (arXiv:1602.08159). Read via
`ar5iv` this session.

The reservoir is a **fully connected transverse-field Ising model** on n qubits with disordered
couplings: "coupling strengths are randomly chosen such that J_ij is distributed randomly from −J/2 to
J/2" `[VERIFIED-FULLTEXT]`. The disorder is the point — it removes the need to tune anything. Nothing
about the reservoir encodes the problem instance; the reservoir is fixed and generic.

### 7.2 What the readout is, and how the input enters

Input injection is a **state replacement on one qubit per timestep**: at step k the first qubit is
replaced with ρ_{s_k} = |ψ_{s_k}⟩⟨ψ_{s_k}|, where |ψ_{s_k}⟩ := √(1−s_k)|0⟩ + √(s_k)|1⟩
`[VERIFIED-FULLTEXT]`.

The readout is **⟨Z_i⟩ on each qubit** `[VERIFIED-FULLTEXT]`, expanded by **temporal multiplexing**:
"the time interval τ is divided into V subdivided timesteps. At each subdivided timestep the signals
are sampled" `[VERIFIED-FULLTEXT]`, giving nV features from n qubits.

The trained object is a **linear** map on those features:
O_trained ≡ Σ w_i^{LR}(I + Z_i)/2 + bias, with the weights "determined by the Moore-Penrose
pseudo-inverse" of the observed signal matrix `[VERIFIED-FULLTEXT]`. Nothing inside the quantum system
is trained.

### 7.3 Does it need training data? Yes — and that is the blocker, not the time series

**It is supervised.** The linear readout is fitted by least squares against labelled targets. There is
no unsupervised QRC in the retrieved corpus.

For us this collides with two things at once:

- **C1.** Our allosteric labels are holo-derived. A readout fitted on them is a prediction-path
  component trained on holo information. Under strict protein-level hold-out across a ~100-protein
  set it is defensible; under anything less it is leakage. The frozen evaluation layer would have to
  arbitrate, and the arbitration is not free.
- **The supervision budget.** ~100 labelled proteins against nV features. Fujii & Nakajima's own
  configurations use V ≫ 1 to reach hundreds of features. Fitting hundreds of features to ~100
  examples is a variance problem before it is a physics problem. Note also that C2 is **not**
  violated — no MD trajectory is involved — so the objection is C1 plus statistics, not C2.

`00-conventions.md` §6 already records that the field's own leakage-controlled reappraisal (AlloBench,
doi:10.1021/acsomega.5c01263) finds no tool above 60 % accuracy. A supervised readout is the exact
mechanism that reappraisal was designed to expose.

### 7.4 Published task performance

All temporal, all synthetic or classical-data, none on graphs with node labels.

- Fujii & Nakajima: "**5–7 qubits possess computational capabilities comparable to conventional
  recurrent neural networks of 100–500 nodes**"; a 5-qubit reservoir on NARMA sits "in between … ESN
  with N=50 and N=100" nodes; a 6-qubit timer task embeds delays "up to ~500 timesteps"
  `[VERIFIED-FULLTEXT]`.
- Hou et al., arXiv:2508.12383: a correlated-spin experimental QRC "reducing prediction error by 1 to
  2 orders of magnitude compared to previous quantum reservoir experiments"; "in long-term weather
  forecasting, our **9-spin quantum reservoir** delivers greater prediction accuracy than classical
  reservoirs with thousands of nodes" `[VERIFIED-ABSTRACT]`.
- Dao et al., arXiv:2603.13005: a QELM "employing up to **124 qubits** and circuits with more than
  **5,000 two-qubit gates** on IBM Quantum computers", competitive with classical baselines on
  time-series forecasting and satellite image classification `[VERIFIED-ABSTRACT]`. This is the
  largest hardware QRC/QELM number retrieved.
- Nokkala, Martínez-Peña, Giorgi, Parigi, Soriano & Zambrini, _Commun. Phys._ **4**, 53 (2021),
  doi:10.1038/s42005-021-00556-w: a **quantum harmonic network** reservoir; "we prove that unlike
  universal quantum computing, **universal reservoir computing can be achieved without non-Gaussian
  resources**" `[VERIFIED-ABSTRACT]`. Worth noting because a harmonic network is the closest object in
  the QRC corpus to an elastic network — and the result is that the Gaussian (hence classically
  simulable, file 03 §6.4) case already suffices.

### 7.5 The static sibling, and the two theorems that bound it

The **quantum extreme learning machine** is QRC without the temporal loop: a single fixed evolution,
a fixed measurement, a trained linear readout. Mujal, Martínez-Peña, Nokkala, García-Beni, Giorgi,
Soriano & Zambrini, _Adv. Quantum Technol._ **4**, 2100027 (2021), doi:10.1002/qute.202100027, is the
review `[VERIFIED-ABSTRACT]`. A static contact graph **is** a legitimate QELM input, so file 03
§11(e)'s stated reason does not close the door. Two results do bound it:

- **Innocenti, Lorenzo, Palmisano, Ferraro, Paternostro & Palma**, _Commun. Phys._ **6**, 118 (2023),
  doi:10.1038/s42005-023-01233-w: QRCs and QELMs "**can be concisely described via single effective
  measurements**", with "an explicit characterisation of the information exactly retrievable with such
  protocols" `[VERIFIED-ABSTRACT]` (emphasis ours). The reservoir plus readout collapses to one POVM.
  Whatever the reservoir does, the model's expressivity is that of a single effective measurement
  followed by linear regression.
- **Xiong, Facelli, Sahebi, Agnel, Chotibut, Thanasilp & Holmes**, _Quantum Mach. Intell._ **7**, 20
  (2025), doi:10.1007/s42484-025-00239-7: "we identify **four sources that can lead to the exponential
  concentration of the observables as the system size grows (randomness, hardware noise, entanglement,
  and global measurements)** and show how this can turn QELMs into **useless input-agnostic
  oracles** … our result on the reservoir-induced concentration strongly indicates that **quantum
  reservoirs drawn from a highly random ensemble make QELM models unscalable**" `[VERIFIED-ABSTRACT]`
  (emphasis ours). Fujii & Nakajima's reservoir is drawn from exactly such an ensemble.

Corroborating from the other direction: De Lorenzis et al., arXiv:2509.06873, find that QELM
performance saturates at an evolution time "consistent with information exchange over short distances"
and that this "remains compatible with efficient classical simulation" `[VERIFIED-ABSTRACT]`.

### 7.6 Could our contact graph _be_ the reservoir?

This is the one QRC variant that is not obviously covered by the above, and it has a published
precedent. **Ivaki, Lazarides & Ala-Nissila**, "Quantum reservoir computing on random regular graphs",
_Phys. Rev. A_ **112**, 012622 (2025), doi:10.1103/gq9r-d5q8 (arXiv:2409.03665): "we introduce a
strongly interacting spin model on **random regular graphs** as the quantum component and investigate
the interplay between static disorder, interactions, and **graph connectivity**, revealing their
critical impact on quantum memory capacity and learnability accuracy … we **uncover the role of
previously overlooked network connectivity**" `[VERIFIED-ABSTRACT]` (emphasis ours). See also Kora,
Zadeh-Haghighi, Stewart, Heshami & Simon, arXiv:2403.08998, on spin-network QRC, which reports that
"the strength of the entanglement advantage depends on the frequency of the input signal"
`[VERIFIED-ABSTRACT]`.

The idea would be: reservoir = the residue contact graph itself; input = a drive on the active site;
readout = per-qubit observables, which are per-residue. That is structurally the right shape. It fails
on arithmetic, not on principle: a one-qubit-per-residue **interacting** spin reservoir has dimension
2^N. At N = 20 that is 1,048,576 amplitudes (trivial); at N = 30, 1.07×10⁹ (8.6 GiB, hard); at
N = 147 it is 1.8×10⁴⁴. So the reservoir is classically unsimulable above ≈30 residues **and**
unrunnable on hardware above file 08's ≈20-node ceiling. The two limits meet in the same place and
leave no window.

### 7.7 Resources

| Variant                          |                             Qubits | Two-qubit gates                       | Depth                          | Classical sim        | Needs labels |
| -------------------------------- | ---------------------------------: | ------------------------------------- | ------------------------------ | -------------------- | ------------ |
| Fujii–Nakajima QRC, n-qubit TFIM |                      5–7 published | n(n−1)/2 ZZ per Trotter step, × steps | ×V multiplex                   | 2ⁿ; trivial to n≈25  | **yes**      |
| QELM, static input               | 4–124 (hardware, arXiv:2603.13005) | >5,000 reported on 124 qubits         | not stated                     | 2ⁿ                   | **yes**      |
| Contact graph as reservoir       |                       N = 147–1058 | ≥\|E\| = 809–3589 ZZ per step         | ≥17 layers/step (file 08 §1.1) | 2^N — **impossible** | **yes**      |

### 7.8 Verdict

**QRC is characterised and it is not a candidate.** The blocker is not "a graph is not a time series"
— the QELM variant removes that. The blockers are, in order: (i) it is supervised, and our labels are
holo-derived with a ~100-protein budget; (ii) the model collapses to a single effective measurement
(doi:10.1038/s42005-023-01233-w), so it is a feature map plus linear regression, which is the same
object `00-conventions.md` §5 already records as pre-refuted for quantum kernels at our feature
dimension; (iii) the one variant with the right shape — contact graph as reservoir — is neither
classically simulable nor hardware-runnable at our N. The §5 gap is now closed **by characterisation**
rather than by deferral, and file 03 §11(e)'s conclusion stands with a corrected reason.

No application of QRC or QELM to protein residues, residue networks or allosteric sites was retrieved
(Europe PMC, 5 results, none on topic — see Method). Per ADR 0019, recorded as a search outcome, not
as an absence claim.

---

## 8. Admissible non-Hermitian and many-body structure — the crux

`00-conventions.md` §5's diagnosis: "Every genuinely quantum observable found needs many-body
interactions or non-Hermitian structure, and a residue contact graph supplies neither." Item 11 states
it operationally: "a real symmetric contact graph has neither non-reciprocal hopping nor gain and
loss."

Both halves are true **of the operator that was built**. Neither is forced by the apo structure. Three
constructions follow. Each is checked against C1 (no holo), C2 (no MD, no MD-trained weights), C5
(catalytic domain, residues as nodes) and C6 (contact topology drives propagation).

### 8.1 Non-Hermitian route 1: open the system at the active site

Add a complex on-site potential −iΓ/2 at a drain residue. The generator becomes
H_eff = H − i(Γ/2)|d⟩⟨d|, which is non-Hermitian with **loss but no gain** — the "opening" of the
open-quantum-systems literature (§3.2, §3.3).

- **C1:** the drain position ranges over every residue in turn; the source is the active site, which
  is apo-side input. No holo information enters. **Clean.**
- **C2:** no trajectory, no trained weight. **Clean.**
- **C6:** the coupling constants are still the contact topology; Γ is a single global scalar swept, not
  a per-residue parameter fitted to anything. **Clean.** Note this is materially different from the
  "heterogeneous on-site energies" that file 03 §5 correctly rules out: **one** scalar for the whole
  model, not N chemistry-derived numbers.
- **C3/C4:** one ancilla qubit, r extra two-qubit gates, r mid-circuit resets (§3.5).

This is the construction Hatano, Katsura & Kawabata use (doi:10.1088/1751-8121/ae5d23), and the one
Celardo et al. use for FMO (doi:10.1021/jp302627w). **`00-conventions.md` §5 item 11 is about a closed
system. It does not cover an opened one, and opening is legal.**

### 8.2 Non-Hermitian route 2: stop symmetrising the contact graph

A directed contact graph gives non-reciprocal hopping directly. The question is whether any asymmetric
edge quantity is computable from apo coordinates alone.

Candidates, ordered by how defensible they are under C6:

1. **Degree-gradient weighting.** Weight the directed edge i→j by a function of deg(j)/deg(i). Pure
   topology, zero chemistry, zero extra data. Fully C1/C2/C6-clean. Its weakness is that it is
   **explicitly a degree quantity**, and degree is the confound ADR 0002 names under Known risks. Low
   expected value.
2. **Side-chain orientation.** Weight i→j by whether residue i's Cα→Cβ vector points toward residue j
   (e.g. by the cosine of the angle). This is **apo geometry**, not a force field: it uses coordinates
   already in the input structure. C1 and C2 clean. Under C6 it is a judgement call — the challenge
   says contact topology drives propagation and atomic force fields are abstracted away; a side-chain
   direction is neither a force field nor pure adjacency. **State the tension in the report rather than
   assuming the answer.** Practical caveat: glycine has no Cβ and needs an explicit rule.
3. **Burial or solvent-accessibility asymmetry.** Computable from apo coordinates, but it is closest to
   the "chemistry C6 tells us to abstract away" line and it is strongly degree-correlated. Not
   recommended.

Given a directed graph, the published machinery exists and it is cheap. **Izaac, Wang, Abbott & Ma**,
_Phys. Rev. A_ **96**, 032305 (2017), doi:10.1103/PhysRevA.96.032305 (arXiv:1607.02673):

> "issues arise when working with directed graphs — **the resulting non-Hermitian Hamiltonian leads to
> non-unitary dynamics**, and the total probability of the quantum walker is no longer conserved. In
> this paper, we discuss a method for simulating directed graphs using **PT-symmetric quantum walks**,
> allowing probability conserving non-unitary evolution. This method is equivalent to mapping the
> directed graph to an undirected, yet weighted, complete graph over the same vertex set … using the
> PT-symmetric framework, we extend these centrality algorithms to directed graphs **with a
> significantly reduced Hilbert space compared to previous proposals**. In certain cases, this
> centrality measure provides an advantage over classical algorithms used in network analysis, **for
> example by breaking vertex rank degeneracy**." `[VERIFIED-ABSTRACT]` (emphasis ours)

It has been run on hardware, at small size: Wu, Izaac et al., arXiv:1912.08411, realise PT-symmetric
centrality ranking on **three- and four-vertex** directed graphs in photonics, and "demonstrate the
advantage of QW approach experimentally by breaking the vertex rank degeneracy in a four-vertex graph"
`[VERIFIED-ABSTRACT]`. Four vertices. That is the state of the hardware art for this construction; the
C4 story is fault-tolerant or quantum-inspired-classical.

**File 03 §3 says of this exact construction: "That last one is the only route that adds structure a
contact graph lacks, and it needs a directed graph we do not have."** The correction this file offers
is narrow and specific: we do not _have_ a directed graph, but we can _build_ one from apo coordinates
without touching MD or holo. Whether we _should_, under C6, is an ADR-sized question, not a
literature question.

### 8.3 Many-body route: the hard-core constraint is already in the encoding

This is the finding with the highest value-to-cost ratio in the file.

File 08 §2.1 fixes the encoding: one qubit per residue, XY coupling, single-excitation sector. File 03
§11(a) then splits the k-excitation sector into "non-interacting" (free-fermion, classically easy,
equivalent to item 1) and "interacting" (hard, but "**no physical basis from Cβ coordinates**").

**That split is not exhaustive, and the missing case is the one we already have.** The XY model on
qubits describes **hard-core bosons**: at most one excitation per site. The hard-core exclusion **is**
an interaction. The mapping to free fermions requires a Jordan–Wigner ordering whose strings cancel,
which happens in one dimension; on a general graph they do not. The strongest published evidence that
the resulting model is genuinely many-body is:

**Childs, Gosset & Webb**, "The Bose-Hubbard model is QMA-complete", ICALP 2014,
doi:10.1007/978-3-662-43948-7_26 (arXiv:1311.3297):

> "We prove that approximating the ground energy of the Bose-Hubbard model on a graph at fixed particle
> number is **QMA-complete**. In our QMA-hardness proof, we encode the history of an n-qubit computation
> in the subspace with **at most one particle per site (i.e., hard-core bosons)**. This feature, along
> with the well-known mapping between hard-core bosons and spin systems, lets us prove a related result
> for a class of **2-local Hamiltonians defined by graphs that generalizes the XY model**."
> `[VERIFIED-ABSTRACT]` (emphasis ours)

If the multi-excitation XY model on an arbitrary graph were equivalent to free fermions, its ground
energy would be computable in polynomial time and could not be QMA-complete. It is not free.

Independent, and directly about transfer amplitudes rather than ground energy: **Large, Underwood &
Feder**, _Phys. Rev. A_ **91**, 032319 (2015), doi:10.1103/PhysRevA.91.032319 (arXiv:1412.1022):

> "We show that **if** single-particle PST occurs on one-dimensional weighted path graphs, then systems
> of hard-core bosons undergoing quantum walks on these paths also undergo PST … The results suggest
> that **hard-core bosons do not generically undergo PST, even on graphs which exhibit single-particle
> PST.**" `[VERIFIED-ABSTRACT]` (emphasis ours)

The one-dimensional case is where they can prove equivalence; off it, the multi-particle transfer
amplitude is **not** determined by the single-particle one. That is exactly the property we need.

**What it costs us: nothing.**

- **C1/C2/C6:** identical Hamiltonian, identical graph, identical couplings. Only the initial state
  changes. **Clean by construction.**
- **C3:** identical circuit. The XY Hamiltonian conserves excitation number, so the same exact Givens
  network of file 08 §2.1 propagates a two-excitation state with **the same** N(N−1)/2 two-qubit gates
  at **the same** depth N on **the same** line connectivity. The only change is one extra X gate in
  state preparation. Symmetry-verification postselection (file 08 §5.6) simply accepts Hamming
  weight 2 instead of 1.
- **Classical cost:** the k-excitation hard-core sector has dimension C(N,k), which is **polynomial**
  at fixed k. Computed this session:

|   k | dim at N=147 | dim at N=272 | dim at N=1058 |  sparse nnz at N=1058 |
| --: | -----------: | -----------: | ------------: | --------------------: |
|   1 |          147 |          272 |         1,058 |                  ≈10⁴ |
|   2 |       10,731 |       36,856 |       559,153 |             ≈1.06×10⁷ |
|   3 |      518,665 |    3,317,040 |   196,821,856 | ≈5.5×10⁹ (borderline) |

At k = 2 the Hamiltonian has ≈2×9.4 ≈ 19 nonzeros per row, so a sparse Krylov propagation at N = 1058
costs ≈10⁷ flops per matrix-vector product. **Trivial.** At k = 3 it is feasible to N ≈ 272
(3.3×10⁶ states, ≈9.3×10⁷ nonzeros) and borderline at N = 1058.

**So the many-body sector is simultaneously (a) genuinely interacting, (b) free on hardware, and (c)
cheap to check classically at k = 2 before any circuit is built.** That combination does not occur
anywhere else in this file.

**The honest limitation, stated plainly.** Classical simulability at fixed k means there is **no
quantum advantage** here — C(N,2) is polynomial. What there is, is a **new observable**: the two-body
transfer amplitude and its deviation from the free product. The claim is informational, not
computational, and the report must not conflate them. `docs/FIELD.md` trap 1 binds us on this.

Two concrete observables:

- **g₂(i,j,t) = |⟨{i,j}|e^{−iHt}|{s₁,s₂}⟩|**, with the two source excitations on two active-site
  residues; rank residue i by max_j or by the marginal Σ_j g₂.
- **Interaction excess** Δ(i,j,t) = g₂(i,j,t) − g₁(i,t)·g₁(j,t), where g₁ is the single-particle
  amplitude. Δ is **identically zero if the sector were free**, so it is a direct measurement of
  whether the hard-core constraint carries any signal on our graphs. That is a clean, falsifiable
  pre-registered test with a stated null.

Caution from §3.4: Zerah-Harush & Dubi (arXiv:2005.04462) find "repulsive interactions are detrimental
to ENAQT". Do not expect §8.1 and §8.3 to compound; test them separately.

### 8.4 What this does to `00-conventions.md` §5

| §5 item                                                 | Status after this file                                                                                                                                                                                                                                                                                                                              |
| ------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 3 — ENAQT/dephasing sweep, no optimum                   | **Variant not tested.** The published optimum is in the **opening strength Γ** at a trap, not the dephasing rate γ (doi:10.1021/jp302627w, doi:10.1088/1751-8121/ae5d23). The measurement stands; it did not test this.                                                                                                                             |
| 5 — eigenvector content and mode IPR                    | **Variant not tested.** Eigenstate IPR was measured; **dynamical** IPR from a named source is a different number (arXiv:2603.05643, doi:10.1103/pp6q-n7mx). Probable transform of the propagator — low priority.                                                                                                                                    |
| 6 — QUBO, classical annealing hit the optimum           | **Mechanism identified**, closure strengthened. Submodularity (arXiv:1803.00110) explains it; the non-submodular alternative (densest-k-subgraph via GBS) is dequantized at 2000 nodes (arXiv:2507.17567).                                                                                                                                          |
| 9, 10 — OTOC/Krylov, Lieb-Robinson collapse to 4g²(r,t) | **Premise conditional.** The collapse is the free-particle algebra. In the k ≥ 2 hard-core sector the model is not free (doi:10.1007/978-3-662-43948-7_26), so the collapse argument does not go through unchanged. Not a claim that these observables work — a claim that the reason given for closing them does not apply to a sector nobody ran. |
| 11 — no non-Hermitian structure                         | **Premise is about a closed, symmetrised system.** Opening it at a drain supplies loss (§8.1); refusing to symmetrise supplies non-reciprocity (§8.2). Both from apo coordinates only.                                                                                                                                                              |
| 1, 2, 4, 7, 8                                           | Unaffected. Nothing here revisits them.                                                                                                                                                                                                                                                                                                             |

---

## 9. Long-time dynamics: what the dequantization theorem leaves open

**Sakamoto & Fujii**, _Quantum_ **10**, 2182 (2026), doi:10.22331/q-2026-08-03-2182 (arXiv:2505.10445).
Abstract retrieved this session from both the journal page and the arXiv record:

> "First, we **dequantize the quantum algorithm for simulating short-time (polynomial-time) dynamics**
> of such systems. This implies that the problem of simulating this dynamics does not yield any
> exponential quantum advantage. Second, we show that simulating short-time dynamics is at least as
> hard as polynomial-time and linear-space probabilistic classical computation. Third, we show that
> **the computational complexity of simulating long-time (exponential-time) dynamics is captured by
> exponential-time and polynomial-space quantum computation.**" `[VERIFIED-ABSTRACT]` — both sources.

The arXiv v4 abstract carries one further sentence the journal landing page omits:

> "**This suggests a super-polynomial time advantage when restricting the computation to
> polynomial-space, or an exponential space advantage otherwise.**" `[VERIFIED-ABSTRACT]`

File 03 §1 quotes the short-time results from full text and states the three escape routes. This file
adds only the precise reading of the third result and what would test it.

**What the theorem does and does not license.**

- The short-time regime is dequantized. File 03 §1 quotes the paper's own polylog(N) framing from full
  text. Any observable read out at short time on a contact graph is covered.
- The long-time regime is characterised as **EXPTIME with poly space on a quantum machine**. The
  advantage that survives is a **space** advantage, or a time advantage only under a polynomial-space
  restriction. It is **not** a claim that long-time dynamics on a specific graph carries more
  information than short-time dynamics. It is a complexity-class statement.
- **At N ≤ 1058, n = ⌈log₂ N⌉ = 11, and "exponential in n" is a constant.** No asymptotic separation
  is testable at our sizes. Anyone writing that this result supports a quantum advantage for our
  pipeline is overreading it, and the report must not.

**What is testable, and it is cheap.** The information-theoretic version of the question: does the
ranking's content depend on the evolution horizon at all? Concretely — one O(N³) eigendecomposition
(1.18×10⁹ flops at N = 1058), then for a logarithmic grid of horizons t spanning 10⁰ to 10³ in units of
1/J_max, compute the ranking, and report (i) Kendall τ between the ranking at t and the t → ∞
time-averaged ranking, and (ii) the arm's evaluation score at each t against the frozen null. If the
score is flat in t, the horizon carries nothing and the branch is closed empirically. If it peaks at
long t, that is a finding worth reporting **as an information statement, not a complexity one**.

Cost: one `eigh` plus O(N²) per horizon. Under a minute at every arm size. This is the cheapest item
in §10 and also the lowest expected information — it is the same propagator at a different argument,
so it is at best a re-parameterisation of `00-conventions.md` §5 item 1.

---

## What this changes for our pipeline

Each row names a concrete observable computable on a residue graph of N = 147–1058 with a named source
set, its classical-simulation cost, whether it is a monotone transform of the single-particle transfer
amplitude (already measured and closed as §5 item 1), and the pipeline stage it touches. Ranked by
expected information gained per unit implementation cost.

|   # | Observable                                                                                                                                                               | Source-conditioned | New, or transform of g₁?                                                                                                                                                               | Classical cost at N=272 / 1058                                                                           | Stage                  |
| --: | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :----------------: | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- | ---------------------- |
|   1 | **Two-excitation hard-core transfer** g₂(i,j,t) = \|⟨{i,j}\|e^{−iHt}\|{s₁,s₂}⟩\|, source pair on the active site; rank residue i by the marginal over j                  |        yes         | **New.** Not free-fermion on a non-1D graph (doi:10.1007/978-3-662-43948-7_26); multi-particle transfer is not determined by single-particle transfer (doi:10.1103/PhysRevA.91.032319) | dim C(N,2) = 36,856 / 559,153; ≈19 nnz per row; sparse Krylov ≈7×10⁵ / 1.1×10⁷ flops per matvec          | `quantum/`             |
|   2 | **Interaction excess** Δ(i,j,t) = g₂ − g₁(i,t)·g₁(j,t)                                                                                                                   |        yes         | **New, and it is the null test for #1** — identically zero if the sector were free                                                                                                     | same as #1 plus one O(N³) `eigh`                                                                         | `quantum/`             |
|   3 | **Opening sweep**: absorbed population at a drain on residue i, source = active site, maximised over the opening strength Γ                                              |        yes         | **New.** A property of the complex spectrum of H − i(Γ/2)\|i⟩⟨i\| (doi:10.1021/jp302627w, doi:10.1088/1751-8121/ae5d23), not of \|⟨i\|e^{−iHt}\|s⟩\|                                   | G·[O(N³) + N·O(N²)] ≈ 8×10⁸ / 5×10¹⁰ flops at G=20 via shared factorisation                              | `quantum/`             |
|   4 | **Γ\*(i)**, the argmax location itself, plus the imaginary-part segregation ratio of the eigenvalues of H_eff at Γ\* (superradiance diagnostic)                          |        yes         | **New.** Purely non-Hermitian-spectral                                                                                                                                                 | N complex eigendecompositions per Γ: N·O(N³) = 5.5×10⁹ / 1.25×10¹² — run at G=1 first                    | `quantum/`             |
|   5 | **Personalised quantum PageRank**: Szegedy walk on G = αE + (1−α)·**v**·𝟙ᵀ with **v** supported on the active site; score = time-averaged instantaneous quantum PageRank |        yes         | **New as a construction.** A discrete Szegedy walk on the doubled space, not e^{−iHt}. Must be run beside classical personalised PageRank as the control                               | O(N²) per step (doi:10.1002/qute.202400022); N² = 73,984 / 1,119,364 amplitudes; ≈10⁹ ops for 1000 steps | `quantum/`             |
|   6 | **Low-tail degeneracy break**: number of distinct quantum-PageRank values among distal residues, against the classical personalised-PageRank tail                        |        yes         | **New**, and it targets our documented failure mode directly (doi:10.1038/srep02773). Carries a published false-positive warning (doi:10.1103/PhysRevResearch.5.013061)                | free once #5 runs                                                                                        | `scoring/`             |
|   7 | **Directed-graph PT-symmetric CTQW centrality**, edges directed by the Cα→Cβ orientation, source = active site                                                           |        yes         | **New.** Non-Hermitian generator (doi:10.1103/PhysRevA.96.032305). Blocked pending an ADR on whether side-chain orientation survives C6                                                | O(N³) = 2.0×10⁷ / 1.2×10⁹ once                                                                           | `network/`, `quantum/` |
|   8 | **Asymptotic trapping probability** of the flip-flop Grover DTQW, source = active site, sink = residue i                                                                 |        yes         | **New.** A coin-space t→∞ subspace quantity with no continuous-time analogue (doi:10.1103/PhysRevA.105.062417)                                                                         | dim 2\|E\| = 2,526 / 7,178; trapped-subspace null space O(\|E\|³) ≈ 2×10⁹ / 4.6×10¹⁰                     | `quantum/`             |
|   9 | **QSW interpolation sweep with a trap**: transport efficiency at the optimal Lindblad-versus-coherent mixing, with an absorbing active site                              |        yes         | **New relative to §5 item 3** (that sweep had no sink), but largely subsumed by #3. Run only if #3 shows structure                                                                     | Lindblad, ρ = N² = 73,984 / 1,119,364 entries, sparse Liouvillian                                        | `quantum/`             |
|  10 | **Dynamical IPR** of the wavepacket launched from the active site, per-residue contribution                                                                              |        yes         | **Probable transform of g₁** — built from the same propagator, though over degenerate subspaces (arXiv:2603.05643)                                                                     | one O(N³) `eigh`, then O(N²) per t                                                                       | `quantum/`             |
|  11 | **Time-horizon sweep** of any ranking, τ vs the t→∞ average, motivated by doi:10.22331/q-2026-08-03-2182                                                                 |        yes         | **Transform.** Same operator, different argument. Cheapest and least informative                                                                                                       | one `eigh` + O(N²) per horizon                                                                           | `scoring/`             |

**Decisions this supports.**

- **Build #1 and #2 first.** They reuse file 08 §2.1's circuit unchanged, need one extra X gate, cost
  nothing new in qubits or depth, are classically checkable at k=2 for every arm, and they test the
  exact premise `00-conventions.md` §5 rests on. #2 has a built-in null.
- **Build #3 next.** It is the variant §5 item 3 could not have seen, its cost is the ALPS cost, and
  its C3 line is +1 qubit and +r gates over the circuit we were already going to build.
- **Do not build #5–#6 before #1–#3.** They are cheap but they are a different operator on a different
  space, and the false-positive warning inside their own literature (doi:10.1103/PhysRevResearch.5.013061)
  plus the proximity-ranker risk (§2.3) means the classical personalised-PageRank control must exist
  first. The control is one line and we do not currently have it — **add classical personalised
  PageRank from the active site to `classical/` as a baseline regardless of whether the quantum version
  is ever built.**
- **#7 needs an ADR before code.** Directing the contact graph by side-chain orientation is the only
  retrieved route to non-reciprocal hopping that is C1- and C2-clean, and it is a genuine C6 judgement
  call. Write the ADR; do not decide it in a literature file.
- **Do not build a quantum PageRank circuit.** C3 blocks it: ≈524,288 two-qubit gates per step at
  N=272 against 36,856 for the whole exact CTQW, on a matrix the damping term makes dense, with no
  column symmetry (doi:10.1016/j.aop.2017.04.006). Simulate it classically at O(N²) and report the
  resource line as the reason.
- **Do not build any Ising/QUBO node-selection method.** §5 item 6 is now explained rather than merely
  observed, and the fault-tolerant resource estimate for the Szegedy-walk-accelerated version is a day
  and a million physical qubits against four classical CPU-minutes (arXiv:2007.07391).
- **Close QRC by characterisation, in the report.** §7 supplies what `00-conventions.md` §5 says was
  never done. The write-up should state the supervised-readout blocker, the single-effective-measurement
  theorem and the exponential-concentration result, and should correct file 03 §11(e)'s stated reason.
- **Report §"noise resilience":** #1 and #2 inherit file 08 §5.6's symmetry verification for free,
  with the postselection window moved from Hamming weight 1 to 2. Note that the retained-shot fraction
  will be lower, since two-excitation bitstrings are a larger but sparser target.
- **Report §"quantum biology motivation":** doi:10.1021/jp302627w's finding that the sink "is the
  dominant effect in the energy transfer which takes place even in absence of a thermal bath" is the
  correct citation for why an open-system framing is physical, and it is compatible with file 03 §10's
  retraction of the long-lived-coherence premise. Structured dissipation, not coherence.
- **Open item for file 08:** mid-circuit reset availability and fidelity on the Braket devices, which
  #3's sink circuit needs and which was not checked this session.

**What this does not support.** Nothing here is evidence that any of these observables beats
`−distance` at AUC 0.617, `cavity_volume`, eigenvector centrality or APOP/ESSA
(`00-conventions.md` §6). Every entry above is a hypothesis with a cheap classical test attached, and
the frozen protocol with its stated null and multiplicity correction is what decides them. Three of
the eleven §5 closures now have untested variants; that is a reason to run three experiments, not a
reason to expect three positives.

---

## Method

**Databases.** arXiv API (`export.arxiv.org/api/query`), including `id_list` batch metadata queries
used to extract publisher DOIs and journal references for 40 preprints in two calls; arXiv abstract
pages; `ar5iv.labs.arxiv.org` HTML full text; Crossref (`api.crossref.org/works`, bibliographic query,
used only to confirm DOI/journal/volume/year); Europe PMC REST search; the Quantum journal article
page; WebSearch for one gap-filling query. Semantic Scholar was not attempted (rate limited per
`00-conventions.md` §3). `nature.com` returned an authentication redirect and was replaced by the
arXiv/`ar5iv` route.

**Queries run (17 structured + 1 web).** arXiv `search_query`: `all:"quantum PageRank"`;
`abs:"quantum reservoir computing"`; `all:"quantum stochastic walk" OR all:"open quantum walk"`;
`abs:"environment-assisted quantum transport" OR abs:"superradiance transition"`;
`abs:"quantum extreme learning machine"`; `abs:"quantum walk" AND abs:"centrality"`;
`abs:"influence maximization" AND (abs:"quantum" OR abs:"QUBO" OR abs:"annealing")`;
`abs:"tensor network" AND abs:"graph" AND (abs:"combinatorial optimization" OR abs:"treewidth" OR
abs:"contraction")`; `abs:"hard-core bosons" AND abs:"graph"`;
`(abs:"densest k-subgraph" OR abs:"maximum vertex cover" OR abs:"submodular") AND (abs:"quantum" OR
abs:"QUBO" OR abs:"Ising")`; `abs:"exceptional point" AND (abs:"network" OR abs:"graph" OR
abs:"transport")`; `abs:"quantum walk" AND (abs:"percolation" OR abs:"localization") AND
abs:"graph"`; `abs:"Szegedy" AND (abs:"circuit" OR abs:"implementation" OR abs:"resource")`;
`(abs:"quantum reservoir" OR abs:"quantum extreme learning") AND (abs:"graph" OR abs:"node
classification" OR abs:"network")`; plus `all:2505.10445` and two `id_list` metadata batches. Europe
PMC: `("quantum reservoir" OR "quantum extreme learning") AND (protein OR residue OR allosteric)`.
Crossref: two bibliographic lookups for the 2012/2013 quantum-PageRank pair. WebSearch: `quantum
personalized PageRank Szegedy walk source node teleportation vector arXiv`.

**Counts.** ≈310 records returned across all queries. **47 screened in** on title and abstract.
**Two full texts landed and read** via `ar5iv` — arXiv:1112.2079 (Paparo & Martin-Delgado 2012) and
arXiv:1602.08159 (Fujii & Nakajima 2017) — plus the Quantum journal landing page for
doi:10.22331/q-2026-08-03-2182. **40 DOIs and journal references verified this session** against arXiv
publisher metadata; 3 further verified against Crossref. All dimensions, flop counts, gate counts and
binomial coefficients above were computed in this session by elementary arithmetic and are marked as
ours where the construction is ours.

**Stopping rule.** Stopped when (i) the source-conditioning question had a definite answer in both
directions — no published personalised quantum PageRank, but a published source-and-drain
non-Hermitian eigenvalue formulation and a published source-and-sink DTQW trapping formulation; (ii)
the two candidate routes to structure `00-conventions.md` §5 says the graph lacks had each been traced
to a primary source with a hardness or non-equivalence theorem attached
(doi:10.1007/978-3-662-43948-7_26 for many-body, doi:10.1021/jp302627w and
doi:10.1088/1751-8121/ae5d23 for non-Hermitian); and (iii) the QRC characterisation reached a blocker
that three independent results agree on.

**Could not be reached.**
(i) Sakamoto & Fujii's formal theorem statements for the long-time result — arXiv and the Quantum
landing page returned only the abstract this session; file 03 §1 holds the short-time statements from
full text.
(ii) Full text of Celardo et al. 2012 (_J. Phys. Chem. C_, paywalled); the superradiance-transition
claims here are `[VERIFIED-ABSTRACT]` only, and the segregation criterion in §10 row 4 is our
operationalisation of the abstract's wording.
(iii) Full text of Hatano, Katsura & Kawabata; the abstract was read twice (arXiv listing and abstract
page) but the 47-page body was not, so the explicit form of the complex potentials and the current
definition are not quoted.
(iv) Full text of Mareš et al. (_Phys. Rev. A_ 105, 062417), so the trapped-subspace construction
recipe is cited but not reproduced; the O(|E|³) cost figure in §4.5 is ours, not theirs.
(v) Full text of Sanders et al. arXiv:2007.07391 — the day/million-qubit figure is
`[VERIFIED-ABSTRACT]`.
(vi) `nature.com` full text for doi:10.1038/srep00444 and doi:10.1038/srep02773 (authentication
redirect); the 2012 construction was recovered from `ar5iv`, the 2013 claims are
`[VERIFIED-ABSTRACT]`.
(vii) No search was run on whether mid-circuit reset is available and characterised on the AWS Braket
devices, which §3.5 and §10 row 3 depend on. Flagged for file 08.
(viii) No quantum or quantum-inspired node-ranking method scored against allosteric labels with a
stated null was retrieved, and no QRC or QELM application to protein residues was retrieved. Per
ADR 0019 both are recorded as outcomes of the queries listed above, not as absence-of-prior-art claims.
