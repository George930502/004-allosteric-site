# Quantum algorithms for site prediction, graph optimisation and elastic-network spectra — a survey against the measured distance confound

**Scope:** six questions asked of the primary literature: (Q1) quantum computing applied to protein
site prediction of any kind; (Q2) QAOA and annealing formulations on protein graphs; (Q3) quantum
eigensolvers and phase estimation on elastic-network Hessians; (Q4) the two references the challenge
organisers cite, plus the Schlimgen/Head-Marsden non-unitary-simulation line behind them; (Q5) where a
graph observable is genuinely non-classical, reported with its dequantizations; (Q6) how the field
stabilises a quantum-walk observable. It deliberately excludes classical allosteric-site predictors
(file `01`), trained models (file `02`, file `04`), and gate-count costing beyond the figures quoted
inline (file `08`, `../exploration/results/43-quantum-resources.md`).
**Sibling files:** `03-quantum-methods.md` — the propagation-observable choice, bosonic encodings and
quantum linear algebra; `../exploration/lit/23-quantum-node-ranking.md` — node ranking on a fixed
classical graph, and the eight constructions it priced; `00-conventions.md` §5 with **ADR 0026** for
what is closed and on what evidence.
**Retrieved:** 2026-08-26.

> **Filename note.** `12-constraint-audit.md` already occupies the `12-` prefix in this directory.
> This file was written to the path the task specified. If the numbering is to be unique, rename this
> to `13-quantum-algorithm-survey.md` and update `../README.md`.

---

## Scope statement and search record

Searched **2026-08-26** across the arXiv API (`export.arxiv.org/api/query`, both `search_query` and
`id_list` forms), arXiv and `ar5iv` HTML full text, PubMed and PMC article pages, PLOS ONE, the
Quantum journal article pages, and general web search. Europe PMC's REST endpoint returned only
`{"version":"6.9"}` through the available fetch route on three attempts and was replaced by
PubMed/PMC page reads. Semantic Scholar was not attempted (rate-limited per `00-conventions.md` §3).
Query strings are listed verbatim in **Method** at the foot of this file. Roughly **340 records** were
returned across 17 structured queries and 8 web queries; **71 were screened in**; **44 records had
their title, authors, journal reference, DOI and full abstract re-retrieved from a primary index this
session**; **two full texts were read** (`ar5iv` for arXiv:1305.6078; the PMC article page for
PMC12228596). Every arithmetic figure below was computed in this session; none is recalled.

**The problem this survey is answering.** Our implemented quantum scorers — CTQW transfer, a
non-Hermitian sink with an opening sweep, Lindblad dephasing with a trap, Szegedy quantum PageRank —
correlate 0.65–0.85 with Euclidean distance to the active site and collapse under detrending
(`../exploration/README.md`; `../exploration/results/40-method-sweep.md`). The survey is therefore
organised around one filter: **does the observable have a mechanism that makes it something other
than a re-parameterised diffusion?** Section Q6 turns out to supply the theorem that explains why our
observables behave this way, and it is the most load-bearing finding in the file.

---

## Q1. Quantum algorithms applied to protein site prediction

**Synthesis.** The field exists but it is thin, young, and almost entirely aimed at problems adjacent
to ours rather than at ours. Seven distinct lines were retrieved. Ranked by proximity to "locate a
site on a protein structure":

1. **Grover-type search over a lattice interaction space.** Liliopoulos et al. [1] extend the protein
   lattice model to protein–ligand interaction sites, label each site with two qubits (one for
   hydrophobic character, one for hydrogen bonding), and run a modified Grover search for docking
   sites. Executed on three IBM 127-qubit devices (`ibm_brisbane`, `ibm_osaka`, `ibm_kyoto`) plus
   simulators, on 4-, 10- and 27-site lattices with 1-, 2- and 3-site ligands. Success probability
   degrades from an expected 0.918 under noise, partially recovered with XX dynamical decoupling. **No
   classical baseline is reported.** `[VERIFIED-FULLTEXT — PMC12228596 article page]`
2. **Hydration-site placement as a QUBO.** Loco et al. [2] couple classical 3D-RISM to a quantum
   optimiser and run hardware experiments **up to 123 qubits**, "matching the precision of classical
   approaches" on real protein–ligand complexes. This is the largest genuinely site-located quantum
   result retrieved, and its honest reading is _parity with classical, at 123 qubits, on a
   sub-problem_. `[VERIFIED-ABSTRACT]`
3. **Residue centrality as a QUBO.** RinQ [3] models protein structures as residue interaction
   networks and casts centrality detection as a QUBO, solved with **D-Wave's simulated annealing**
   (i.e. a classical solver from the D-Wave stack, not the QPU). Result: "consistently identifies
   central residues that closely align with classical benchmarks". That is agreement with the
   classical answer, not improvement on it. `[VERIFIED-ABSTRACT]`
4. **Active-site _structure_ by VQE.** Zhang et al. [4] formulate binding-site structure prediction as
   ground-state energy minimisation on a tetrahedral lattice, on utility-level IBM processors. The
   endpoint is peptide-fragment backbone geometry against RMSD, **not site location**.
   `[VERIFIED-ABSTRACT]`
5. **Quantum ML on protein graphs.** Giusto et al. [6] compute a Quantum Evolution Kernel on the
   PROTEINS dataset on the **256-qubit Aquila** neutral-atom machine, obtaining "slightly better
   performance" than classical kernels on whole-graph classification; Vercellino et al. [7] report
   that only **76 %** of protein graphs could be embedded as unit-disk graphs on the same register.
   Both are graph-level classification, not residue-level localisation. Li et al. [5] state binding
   pocket classification with a quantum CNN in a four-technique suite, with no dataset, metric or
   baseline in the abstract. `[VERIFIED-ABSTRACT]`
6. **Hot spots.** Roosan et al. [8] classify hotspot _mutations_ with a QNN plus VQE on the Qiskit
   simulator for two genes. The positive class is a mutation, not a surface patch, and no benchmark or
   null is stated. `[VERIFIED-ABSTRACT]`
7. **Ensemble energetics with an allostery claim.** Patil et al. [9] give one qubit per residue (a
   two-state solvation variable), entangle along the residue-interaction network, and sample ~10⁶
   shots to recover residue-level couplings on Trp-cage 1L2Y and a chimera 9GDL. Allosteric pathway
   identification appears in the abstract as a **prospective application**, not a result.
   `[VERIFIED-ABSTRACT]`

**The negative result, recorded explicitly.** An arXiv query for `(allosteric OR "cryptic site" OR
"cryptic pocket") AND quantum` returned 7 on-topic-looking records, of which **zero** use a quantum
computing algorithm to predict an allosteric-site or cryptic-pocket location; every one uses "quantum"
in the quantum-chemistry, QM/MM or quantum-biology sense. Combined with a PubMed sweep that surfaced
only classical predictors (ZHMolEReP, STINGAllo, Allo-PED) alongside the docking-site paper [1], **no
quantum method scored against allosteric ground truth with a stated null was retrieved.** Per ADR 0019
this is the outcome of the recorded queries, not an absence-of-prior-art claim. It independently
reproduces `03-quantum-methods.md` §11(d) from a different query set and a different database.

| Citation               | Year | What it does                                                        | Encoding / qubit count                                                                                 | Result                                                                                   | Relevance to us                                                                                                                                               |
| ---------------------- | ---- | ------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Liliopoulos et al. [1] | 2025 | Grover search for protein–ligand docking sites on a lattice         | 2 qubits per interaction site (hydrophobic, H-bond); 4/10/27-site lattices                             | Works on simulator; degrades on IBM 127-qubit hardware; **no classical baseline**        | The only Grover-type _site-location_ result retrieved. Lattice model, not a contact graph. Shows the hardware ceiling for oracle-based search on this problem |
| Loco et al. [2]        | 2026 | Protein-pocket hydration-site prediction as QUBO + 3D-RISM          | Binary occupancy per grid point; **up to 123 qubits** on NISQ hardware                                 | Matches classical precision on real complexes; claims accuracy improves with qubit count | Largest site-located quantum run found. Parity, not advantage. Its honesty about "matching" is the register we should adopt                                   |
| Mohtashim (RinQ) [3]   | 2025 | Residue centrality on RINs as QUBO                                  | Binary per residue; solved with D-Wave **simulated** annealing                                         | Agrees with classical centrality benchmarks                                              | Closest published object to a residue ranking. Its own success criterion is agreement with classical centrality — the confound ADR 0002 names                 |
| Zhang et al. [4]       | 2026 | Binding-site _structure_ prediction via VQE                         | Tetrahedral-lattice turn encoding; utility-scale IBM processors                                        | Backbone geometry vs RMSD                                                                | Not site location. Cite only to show the challenge sponsor's own quantum line targets geometry                                                                |
| Li et al. [5]          | 2021 | QGAN/QCNN/QVAE suite; one task is "classify binding pockets"        | Not stated in abstract                                                                                 | Not stated                                                                               | Weak. Record it so the field's coverage is not overstated                                                                                                     |
| Giusto et al. [6]      | 2024 | Quantum Evolution Kernel for graph classification, PROTEINS dataset | **256-qubit** Aquila neutral atom register, one atom per node                                          | "Slightly better" than classical kernels                                                 | Whole-graph label, not residue ranking. Establishes that 256-node protein graphs _can_ be laid out on analogue hardware                                       |
| Vercellino et al. [7]  | 2024 | Embedding protein graphs as unit-disk graphs on neutral-atom QPUs   | One atom per node; Aquila and Orion Alpha                                                              | **76 %** of protein graphs embeddable                                                    | A hard, quotable C3 number for the analogue route: a quarter of protein graphs do not fit the register geometry at all                                        |
| Roosan et al. [8]      | 2025 | Hotspot _mutation_ classification, QNN + VQE                        | Qiskit simulator; qubit count not stated                                                               | High reported accuracy, no benchmark or null                                             | Hot-spot in name only. Not a structural site predictor                                                                                                        |
| Patil et al. [9]       | 2026 | Residue-level ensemble energetics on a gate circuit                 | **One qubit per residue** (two-state solvation), entangling block from the contact network; ~10⁶ shots | Folding-funnel-like energy distribution on Trp-cage; residue couplings                   | Same qubit budget as our one-hot CTQW encoding, on the same graph. Allostery is aspirational in it — a gap we could fill                                      |
| Li et al. [12]         | 2018 | Quantum annealing vs classical ML for transcription-factor binding  | D-Wave; binary classifier weights                                                                      | "Slight advantage" in classification, comparable ranking                                 | The field's own most careful head-to-head. Slight, not decisive — the calibration to keep                                                                     |
| Santagati et al. [10]  | 2024 | Perspective: drug design on quantum computers                       | n/a                                                                                                    | Resource-realistic outlook                                                               | The reference to cite when framing expectations honestly                                                                                                      |

---

## Q2. QAOA and quantum annealing on protein graphs

**Synthesis.** Two facts govern this branch and they pull in opposite directions.

**Fact one: protein _structure_ networks have been cast as QUBOs, repeatedly, and the objectives all
reduce to a small family.** Molecular docking as weighted subgraph isomorphism on D-Wave [16];
docking as maximum-weight vertex clique solved by digitised-counterdiabatic QAOA on IBM Eagle, one
qubit per interaction anchor, **6-qubit solvability confirmed on hardware, exact optimum recovered on
8 of 11 targets at 10 qubits** [17]; docking as max-weight clique sampled by Gaussian boson sampling
[18]; residue centrality as QUBO [3]; lattice folding as an Ising ground state on D-Wave [20, 21, 22]
and on gate hardware with **22 qubits for a 10-residue Angiotensin and 9 qubits for a 7-residue
neuropeptide** [19]. The encoding is always one binary variable per (residue, position) or per
(anchor, match) pair, and the objective is always a contact energy or a matching score.

**Fact two: the graph-combinatorial formulations that are genuinely proxies for "the sub-graph most
dynamically coupled to a source" already exist — and they are classical, they are good, and nobody has
quantised them.** The Barahona group's line is the relevant one and it is not in this repository's
review files:

- **Multiscale community detection on an atomistic protein graph** with Markov Stability, using random
  walk transients to extract signalling pathways in caspase-1 [23]. `[VERIFIED-ABSTRACT]`
- **Bond-to-bond propensities** [24], which quantify how an instantaneous bond fluctuation propagates
  non-locally, with significance assessed by quantile regression against a background — this is
  structurally the same idea as our matched-patch null, published in 2016.
- **Paths of optimised propensity** linking the orthosteric site to identified allosteric sites [25].
- **Graph partitioning plus robustness analysis** to find binding-relevant residues [26].
- **Relative dimension with respect to a diffusive source** [27]: "the relative dimension with respect
  to the active site uncovers regions involved in allosteric communication". `[VERIFIED-ABSTRACT]`

All five take structure only — no MD trajectory — so all five satisfy C1, C2 and C6. **[27] in
particular is a source-conditioned, scale-resolved classical measure that we do not have and that is a
strictly stronger baseline than `−distance`.** Any quantum community-detection or partitioning
proposal must be scored against it, not against a random floor.

**The quantum side of community detection is mature enough to instantiate but its verdict is already
in.** Modularity maximisation as a QUBO with one-hot per-node encoding runs on D-Wave 2X/2000Q at a
34-node ceiling on the QPU [13]; the hybrid solver reaches brain connectomes and reports **higher
modularity than Louvain** [14]. Faccin et al. [15] define community detection _for a quantum walk_,
using quantum transport probability and state fidelity as the closeness measure, and demonstrate it on
the LHCII light-harvesting complex, claiming "quantum effects undetectable by classical network
tools". That is the one construction in this branch whose object is not available classically by
construction — and it is source-conditionable, because transport probability takes a source argument.

**Why the branch nonetheless does not rescue us.** Three independent reasons, each sourced:

1. `00-conventions.md` §5 item 6: classical annealing hit the exhaustive optimum at every size up to
   C(34,7) on the cooperative-selection QUBO, and `../exploration/lit/23-quantum-node-ranking.md` §5.1
   attributes that to submodularity.
2. The fault-tolerant resource estimate for Szegedy-walk-accelerated annealing is a day and a million
   physical qubits against four classical CPU-minutes [28]. `[VERIFIED-ABSTRACT in file 23; not
re-retrieved here]`
3. The GBS route to dense subgraphs and max-clique is dequantized precisely because a contact adjacency
   matrix is non-negative [29]. `[VERIFIED-ABSTRACT in file 03; not re-retrieved here]`

**No literature was retrieved casting an allosteric pathway as a Steiner tree or a minimum cut and
solving it with a quantum method.** Classical Steiner-tree and min-cut work on biomolecules exists
(Euclidean Steiner trees for macromolecular stability, arXiv:math-ph/0512043; max-flow/min-cut for
protein titration states, doi:10.1021/acs.jpcb.6b02059) but neither is an allosteric-pathway
formulation and neither is quantum. Recorded as a search outcome under ADR 0019.

| Citation                                         | Year | What it does                                                                                                        | Encoding / qubit count                                                                                              | Result                                                                                                     | Relevance to us                                                                                                                                                    |
| ------------------------------------------------ | ---- | ------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Negre, Ushijima-Mwesigwa, Mniszewski [13]        | 2020 | Multi-community detection as QUBO on D-Wave                                                                         | **k binary vars per node** (one-hot over k communities); D-Wave 2X (46 vars) / 2000Q (64 vars)                      | Karate club, 34 nodes, 78 edges on hardware; baseline is D-Wave's classical annealer                       | The canonical QUBO community-detection formulation. **The 34-node hardware ceiling is the number to quote against our N = 147–1058**                               |
| Wierzbiński, Falcó-Roget, Crimi [14]             | 2023 | Modularity maximisation on brain connectomes as a Discrete Quadratic Model                                          | Leap hybrid solver                                                                                                  | Higher modularity index than Louvain                                                                       | The closest published biological-network analogue. Note "hybrid solver" — the classical part does most of the work                                                 |
| Faccin, Migdał, Johnson, Bergholm, Biamonte [15] | 2014 | **Community detection defined for a quantum walk**; closeness from quantum transport probability and state fidelity | CTQW on the network; LHCII                                                                                          | Claims communities invisible to classical tools                                                            | **The one formulation in this branch whose object has no classical counterpart, and it is source-conditionable.** Candidate C4 below                               |
| Triuzzi et al. [16]                              | 2025 | Docking as weighted subgraph isomorphism, QUBO                                                                      | Binary per (ligand atom, pocket grid cell)                                                                          | Compared against classical simulated annealing                                                             | The pocket grid is the object, not the residue graph. Shows QUBO docking is a matching problem, not a propagation problem                                          |
| Zheng et al. (Q-Score) [17]                      | 2026 | Docking score as max-weight vertex clique via DC-QAOA                                                               | **One qubit per interaction anchor**; exact optimum on 8/11 targets at 10 qubits; **6-qubit circuits on IBM Eagle** | Spearman ρ 0.05 vs classical scoring — deliberately orthogonal                                             | The clearest recent max-clique-on-a-protein-graph instantiation with real hardware numbers, and it is honest that orthogonality to classical scoring is the _goal_ |
| Banchi et al. [18]                               | 2020 | Docking as max-weight clique sampled by GBS                                                                         | Photonic modes on the adjacency matrix                                                                              | Proof of principle                                                                                         | Dequantized by [29] for non-negative adjacency matrices, which ours is                                                                                             |
| Robert, Barkoutsos, Woerner, Tavernelli [19]     | 2021 | Lattice protein folding, variational, O(N⁴) Hamiltonian                                                             | **22 qubits for 10 residues; 9 qubits for 7 residues**; IBM 20-qubit device                                         | Folds model peptides                                                                                       | The canonical qubit-per-residue scaling number for lattice encodings. At 300 residues this encoding is out of reach by orders of magnitude                         |
| Perdomo-Ortiz et al. [20]                        | 2012 | First lattice folding on a quantum annealer                                                                         | Up to **81 qubits**, MJ and HP models                                                                               | Benchmark implementation                                                                                   | Historical anchor. Fourteen years later the size has not moved much                                                                                                |
| Irbäck et al. [21]                               | 2022 | HP lattice folding, distributed spin encoding, D-Wave Advantage                                                     | No auxiliary variables; chains to **N = 64**                                                                        | 100 % hit rate for N ≤ 30                                                                                  | The best-engineered annealing result in the family, and still a lattice                                                                                            |
| Outeiral et al. [22]                             | 2021 | Numerical study of annealing on protein lattice problems                                                            | D-Wave                                                                                                              | "Limited" speedup, conditional on Hamiltonian engineering                                                  | The field's own sober assessment. Title contains the word "limited"                                                                                                |
| Amor, Yaliraki, Woscholski, Barahona [23]        | 2014 | Markov Stability multiscale community detection for allosteric pathways                                             | Classical, atomistic graph, **structure only**                                                                      | Signalling pathways in caspase-1                                                                           | **The classical target a QAOA community-detection proposal must beat.** C1/C2/C6-clean                                                                             |
| Amor, Schaub, Yaliraki, Barahona [24]            | 2016 | Bond-to-bond propensity, with quantile-regression significance                                                      | Classical, energy-weighted atomistic graph                                                                          | Allosteric sites in caspase-1, CheY, h-Ras                                                                 | Structurally our matched-patch null, ten years earlier. Must be cited in the report                                                                                |
| Wu, Yaliraki, Barahona [25]                      | 2022 | Paths of optimised propensity from orthosteric to allosteric site                                                   | Classical, structure only                                                                                           | Pathways and functional residues                                                                           | Source-conditioned by construction — rare in this literature                                                                                                       |
| Delmotte, Tate, Yaliraki, Barahona [26]          | 2011 | Multi-scale graph partitioning + robustness on protein graphs                                                       | Classical                                                                                                           | Key binding residues on myosin tails                                                                       | The partition-quality object a QAOA max-cut proposal would consume                                                                                                 |
| Peach, Arnaudon, Barahona [27]                   | 2022 | **Relative dimension with respect to a diffusive source**                                                           | Classical, structure only                                                                                           | "Relative dimension with respect to the active site uncovers regions involved in allosteric communication" | **The strongest missing classical baseline in this survey.** Source-conditioned, scale-resolved, C1/C2/C6-clean, one diffusion solve                               |

---

## Q3. QPE and VQE on the elastic-network Hessian

**Synthesis.** The mapping the task asks about is real, is precisely locatable, and is
**Babbush, Berry, Kothari, Somma & Wiebe, _Phys. Rev. X_ 13, 041041 (2023)**, arXiv:2303.13012 [30].
Verified this session directly from the arXiv metadata record: the author list, the journal reference
`Phys. Rev. X 13, 041041 (2023)` and `DOI 10.1103/PhysRevX.13.041041` all match.

**The encoding, from the abstract verbatim** `[VERIFIED-ABSTRACT]`:

> "We present a quantum algorithm for simulating the classical dynamics of $2^n$ coupled oscillators
> (e.g., $2^n$ masses coupled by springs). Our approach leverages a mapping between the Schrödinger
> equation and Newton's equation for harmonic potentials such that the amplitudes of the evolved
> quantum state encode the momenta and displacements of the classical oscillators."

So: **displacements and momenta live in the amplitudes of an n-qubit state**, with $N = 2^n$
oscillators, and the generator is built from $\sqrt{\mathbf{A}}$ where $\mathbf{A}$ is the
spring-constant matrix. The complexity is "polynomial in $n$, almost linear in the evolution time, and
sublinear in the sparsity", conditional on two oracles: efficient _query_ access to individual masses
and spring constants, and efficient initial-state preparation. The hardness claim is sharp and worth
quoting because it is what makes the paper a _speedup_ result rather than a heuristic: estimating the
kinetic energy of an oscillator is **BQP-complete** when the oracles are instantiated by efficient
quantum circuits, and any classical algorithm must make $2^{\Omega(n)}$ oracle queries
`[VERIFIED-ABSTRACT]`.

**Is the observable different in kind from classical NMA? No — and three independent papers say so.**

- **The readout is a global energy, not a mode.** Babbush et al.'s stated example application is "the
  kinetic energy of an oscillator at any time" — a scalar. Kolotouros et al. [33] build Quantum Elastic
  Network Models directly on [30] and state that extracting normal modes "is not, however, possible in
  our current description of QENM" `[VERIFIED-FULLTEXT in file 03 §6.2; abstract re-verified here]`.
  Their headline figure — a centimetre-scale graphene sheet in **~160 logical qubits** — is bought by
  graphene's periodicity, which supplies the spring-constant oracle as arithmetic.
- **The read-in is provably Ω(N) for a protein.** Liu, Li, Wang & Liu [32] cost GNM and all-atom
  normal-mode simulation end to end and prove that the connectivity matrix "is incompressibly
  determined by the coordinates of N atoms" `[VERIFIED-FULLTEXT in file 03 §6.3; abstract re-verified
here]`. Their own read-out list — "energy, low-frequency vibrational modes, density of states,
  displacement correlations, and optimal control parameters" — is almost our deliverable list, which is
  why the read-in bound is the binding constraint rather than a technicality.
- **Modal analysis by QPE exists as a standalone construction.** Lee & Kanno [31] apply quantum phase
  estimation to coupled classical oscillators using **qubitization on the sparse structure of the
  matrix**, "explicitly construct block-encoding oracles", propose an initial-state preparation, and
  give "rough estimates of the necessary number of physical qubits and actual runtime" for a
  fault-tolerant machine `[VERIFIED-ABSTRACT]`. This is the cleanest published statement that
  natural-frequency extraction by QPE is a legitimate object. **It was not in `03-quantum-methods.md`.**

**The quantum-linear-systems route is worse, not better.** HHL [37] returns the solution as a _state_,
not as a vector; extracting a per-residue score costs $N$ measurements, which erases the speedup. That
objection is generic to the family and applies to any proposal that inverts the Kirchhoff matrix on
hardware and then asks for a ranking. It is why [31]'s eigenvalue-only readout is the honest quantum
object here: an eigenvalue is one number, and QPE returns one number.

**The general structural-mechanics picture is polynomial, not exponential.** Montanaro & Pallister [34]
compare a quantum FEM solver against conjugate gradient and find a "polynomial speedup" that grows
with the PDE's spatial dimension, with evidence ruling out super-polynomial speedup at fixed dimension
for smooth solutions `[VERIFIED-ABSTRACT]`. Deiml & Peterseim [35] recover optimal $\mathrm{tol}^{-1}$
complexity with a BPX preconditioner, obtaining quantum advantage in two dimensions where earlier work
needed four. Hölscher et al. [36] give an end-to-end fault-tolerant topology-optimisation algorithm
with a block-encoded stiffness matrix and QSVT inversion, and the speedup is **quadratic**, from
Grover. None of these is an exponential separation on a fixed finite mesh.

**One retrieved paper does exactly the wrong thing for us, and is worth naming as a trap.** Reilly [38]
encodes a protein as a "mechanical harmonics graph" whose nodes are vibrational modes and whose edges
are harmonic couplings, then runs Kuramoto entrainment described as "directly compatible with quantum
annealing hardware". It is an elegant frequency-space representation — and its nodes are **"vibrational
modes derived from molecular dynamics"** `[VERIFIED-ABSTRACT]`. That is a C2 violation on the face of
the abstract. Do not import it.

| Citation                                       | Year    | What it does                                                                                                                                 | Encoding / qubit count                                                                                                                           | Result                                                                                                      | Relevance to us                                                                                                                                                                                                                   |
| ---------------------------------------------- | ------- | -------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Babbush, Berry, Kothari, Somma, Wiebe [30]** | 2023    | **The mapping the task asks for.** Newton's equations for $2^n$ coupled oscillators → Schrödinger evolution generated by $\sqrt{\mathbf{A}}$ | **Displacements and momenta in the amplitudes of an $n$-qubit state**; $N = 2^n$ oscillators, so N = 300 needs **n = 9** system qubits           | Exponential speedup; kinetic-energy estimation is **BQP-complete**; classical needs $2^{\Omega(n)}$ queries | Verified precisely: _Phys. Rev. X_ **13**, 041041 (2023), doi:10.1103/PhysRevX.13.041041, arXiv:2303.13012. The speedup is conditional on polylog-time oracles for masses and springs — which [32] proves a protein does not have |
| Lee & Kanno [31]                               | 2023    | **QPE for natural frequencies and normal modes** of coupled classical oscillators, via qubitization                                          | Explicit block-encoding oracles exploiting matrix sparsity; physical-qubit and runtime estimates for a fault-tolerant machine                    | Demonstrated on simple oscillator systems                                                                   | **The missing reference in `03-quantum-methods.md`.** It is the honest hardware story for the ALPS eigenvalue readout, and it says out loud that this is a fault-tolerant proposition                                             |
| Liu, Li, Wang, Liu [32]                        | 2024–25 | End-to-end quantum simulation of protein dynamics with GNM and all-atom NMA                                                                  | State prep, first efficient loading of a protein connectivity matrix, read-out of energy / low-frequency modes / DOS / displacement correlations | Read-in proved incompressible: Ω(N) bits                                                                    | The single most relevant paper in the survey. Its read-out list is our deliverable list; its read-in theorem is why the exponential speedup does not transfer                                                                     |
| Kolotouros et al. (QENM) [33]                  | 2026    | Babbush algorithm applied to a 2D elastic network                                                                                            | ~**160 logical qubits** for a cm-scale graphene sheet                                                                                            | Heat transfer and out-of-plane rippling                                                                     | Graphene is periodic; a protein is not. Authors state normal modes cannot be extracted from the encoding                                                                                                                          |
| Montanaro & Pallister [34]                     | 2016    | Quantum FEM vs conjugate gradient                                                                                                            | Quantum linear-systems solver on the FEM stiffness matrix                                                                                        | **Polynomial** speedup growing with PDE dimension; super-polynomial ruled out at fixed dimension            | The general ceiling for "quantum linear algebra on a mechanical operator". Cite it before claiming any FEM-style advantage                                                                                                        |
| Deiml & Peterseim [35]                         | 2024    | Quantum FEM with BPX preconditioning                                                                                                         | Cartesian-grid discretisation                                                                                                                    | Optimal $\mathrm{tol}^{-1}$ complexity; advantage from 2D rather than 4D                                    | Shows the polynomial ceiling is being tightened, not broken                                                                                                                                                                       |
| Hölscher et al. [36]                           | 2025    | End-to-end topology optimisation in structural mechanics                                                                                     | Block-encoded stiffness matrix, QSVT inversion, Grover over the design space                                                                     | **Quadratic** speedup, fault-tolerant                                                                       | The end-to-end costing template. Quadratic, and fault-tolerant, is the honest shape of this branch                                                                                                                                |
| Reilly [38]                                    | 2026    | Protein as a mechanical-harmonics graph, Kuramoto entrainment framed for annealers                                                           | Nodes are **MD-derived vibrational modes**; GNN readout on 5,238 SwissProt proteins                                                              | GO function prediction; 7.5× signal amplification on CLIC1                                                  | **C2 violation on the face of the abstract.** Named here so nobody imports it                                                                                                                                                     |
| Bartlett, Sanders, Braunstein, Nemoto [39]     | 2002    | Gaussian states under Gaussian operations are classically simulable                                                                          | n/a                                                                                                                                              | Efficient classical simulation                                                                              | The theorem that closes the continuous-variable route for a _harmonic_ network. C6 removes the anharmonicity that would reopen it                                                                                                 |

**Answer to Q3's third bullet, stated plainly.** The observable a quantum algorithm gives you on an
elastic network is **not different in kind** from classical NMA — it is a _subset_. Classical NMA
returns the full eigenbasis at $O(N^3) = 2.7\times10^7$ flops for N = 300. The Babbush encoding
returns global quadratic functionals (kinetic energy, total energy, subset energies) and cannot return
the modes [33]. The one place a quantum algorithm computes something classical NMA does not hand you
cheaply is **an eigenvalue to high precision without the eigenvector**, via QPE [31] — and our
best-performing classical metric, ALPS, needs exactly that and nothing more. That is a real C4 story
and it is a _hardware story for a classically chosen metric_, not a source of advantage.

---

## Q4. The two references the challenge organisers cite

### Q4.1 Oh, Krogmeier, Schlimgen & Head-Marsden (2024) [40]

**The problem it solves.** Non-unitary (Lindblad) dynamics on a unitary-gate machine. The algorithm
takes the propagator, computes its **singular value decomposition classically**, dilates the diagonal
singular-value matrix into a unitary with one ancilla, and runs the resulting circuit. Applied to two
canonical quantum-biology benchmarks: excitonic transport in the Fenna–Matthews–Olson complex and the
radical-pair mechanism for avian magnetoreception. Abstract verbatim `[VERIFIED-ABSTRACT this session
from arXiv:2309.17391]`: it "demonstrate[s] that the singular value decomposition algorithm is capable
of capturing accurate short- and long-time dynamics for these systems **through implementation on a
quantum simulator**" (emphasis ours — this is simulation, not hardware).

**The quantum resource cost**, from the full text as recorded in `03-quantum-methods.md` §7
`[VERIFIED-FULLTEXT there; not re-retrieved here]`: the SVD is classical at $\mathcal{O}(r^3)$; the
Hilbert space of size $r$ becomes a Liouville space of size $r^2$; the total gate complexity is
$\mathcal{O}(d^2 2^{2d-1})$ for $d$ qubits; and the authors state the systems studied "are beyond the
scope of possible implementation on current NISQ computers."

**What it would let us compute on a residue contact graph that a classical method cannot compute as
cheaply: nothing.** The argument is arithmetic. At N = 300 the Liouville dimension is
$r^2 = 9\times10^4$, requiring $d = \lceil \log_2 9\times10^4 \rceil + 1 = 18$ qubits and
$\mathcal{O}(d^2 2^{2d-1}) \approx 10^{13}$ gates (computed this session from their formula). The
classical step the algorithm _begins with_ — an $\mathcal{O}(N^3) = 2.7\times10^7$-flop decomposition
— is already the whole cost of the classical answer. **The challenge cites this paper as evidence that
quantum simulation helps biology; read carefully it is evidence that the non-unitary content is
obtained classically and the quantum part is a replay.** That reading should appear in the report,
politely and with the numbers.

### Q4.2 Mitarai & Fujii (2021) [41]

**The problem it solves.** Simulating a **non-local** (two-qubit) channel using only **local**
channels, by decomposing the non-local channel into a quasiprobability-weighted linear combination of
local ones and Monte-Carlo sampling the decomposition. Abstract verbatim `[VERIFIED-ABSTRACT from both
the Quantum journal page and arXiv:2006.11174]`: it defines a quantity called the "**channel
robustness of non-locality**, which quantifies the cost for the decomposition", and gives "an upper
bound for a general two-qubit unitary channel by providing an explicit decomposition".

**The quantum resource cost, with the number.** The predecessor paper by the same authors [42] states
it exactly `[VERIFIED-ABSTRACT this session]`: "The required number of sampling to get an expectation
value of a target observable within an error of $\varepsilon$ is roughly $O(9^k/\varepsilon^2)$, where
$k$ is the number of 'cuts' performed." Piveteau & Sutter [43] later reduce this to $O(4^n)$ for $n$
non-local CNOTs **if classical communication between the fragments is allowed**
`[VERIFIED-ABSTRACT]`. The parent idea — simulating a large circuit on a small machine — is Peng,
Harrow, Ozols & Wu [44], at $2^{O(K)}$ for $K$ qubits of inter-cluster communication
`[VERIFIED-ABSTRACT]`.

**What it would let us compute on a residue contact graph — and the honest answer is a computed
"no".** This is the one genuinely actionable thing in the challenge's second reference, and it
deserves the arithmetic rather than a hand-wave. Our one-hot single-excitation CTQW encoding needs one
qubit per residue (file `08` §2.1); the repository's measured coherent budget at 99.5 % two-qubit
fidelity is roughly 200 two-qubit gates, i.e. **N ≈ 20 nodes on hardware**
(`../exploration/results/43-quantum-resources.md`). Circuit cutting is exactly the technique that
would break that ceiling: partition the residue graph into ~20-qubit blocks and cut every two-qubit
gate that crosses a boundary. The cost is $9^k$ samples for $k$ cuts. Computed this session:

| cuts $k$ | samples $\approx 9^k$ | verdict                    |
| -------: | --------------------: | -------------------------- |
|        5 |     $5.9\times10^{4}$ | fine                       |
|       10 |     $3.5\times10^{9}$ | a long but conceivable run |
|       20 |    $1.2\times10^{19}$ | out of reach               |
|      127 |            $10^{121}$ | absurd                     |

A balanced partition of a residue contact graph with mean degree ≈ 9.4 into 20-residue blocks cuts on
the order of the graph's edge boundary — tens to hundreds of edges at N = 147, and more at N = 300.
**So circuit cutting does not rescue the encoding, and the reason is a computable property of the
input rather than an engineering shortfall.** Reporting that, with the table, is a stronger C3 section
than any optimistic projection. It also converts the organisers' second reference from a decorative
citation into a quantitative bound.

### Q4.3 The Schlimgen / Head-Marsden non-unitary-simulation line

The SVD paper [40] sits on a four-paper programme, all retrieved and verified this session from arXiv
metadata. This is directly relevant to our sink scorer and our Lindblad-with-trap scorer, because both
are non-unitary generators that a gate machine cannot execute natively.

- **Linear combination of unitaries** [45]: "any quantum operator can be **exactly decomposed as a
  linear combination of at most four unitary operators**" `[VERIFIED-ABSTRACT]`. Demonstrated on a
  two-level system in zero- and finite-temperature amplitude damping channels. This is the cheapest
  primitive of the family and it is the right one for a **single** non-Hermitian step.
- **Dilation with one ancilla via SVD** [46]: decompose a general operator into two unitaries and a
  diagonal non-unitary, and implement the diagonal part as a diagonal unitary in a **1-qubit dilated
  space**, which has known circuit decompositions. Used to prepare sub-normalised two-level states and
  to run dephasing and amplitude-damping dynamics **on a device** `[VERIFIED-ABSTRACT]`. This is the
  exact primitive our complex-absorbing-potential sink would compile to.
- **Density-matrix purification** [47]: recast the $d\times d$ density matrix as a $d^2$ wavefunction
  evolved unitarily; the advantage stated is that "the wavefunction requires only an $n$-qubit,
  compared to $2n$-qubit, bath for an $n$-qubit system" `[VERIFIED-ABSTRACT]`. Demonstrated on a
  two-site quantum Ising model on an experimental device.
- **The review** [48] is the single citation to use when the report needs one reference for the whole
  open-system-on-quantum-hardware area.
- **PT-symmetric two-level systems via Hermitian equivalents** [49] is the same group's route to
  non-Hermitian dynamics through similarity transformation — relevant if we pursue the directed-graph
  PT-symmetric construction that `../exploration/lit/23-quantum-node-ranking.md` §8.2 leaves open
  pending an ADR.

| Citation                                               | Year | What it does                                                                                                                                               | Encoding / qubit count                                                 | Result                                                                         | Relevance to us                                                                                                                       |
| ------------------------------------------------------ | ---- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------- |
| Oh, Krogmeier, Schlimgen, Head-Marsden [40]            | 2024 | Non-unitary Lindblad dynamics via a **classically computed** SVD, dilated with one ancilla                                                                 | Liouville space $r^2$; FMO 7-site becomes a 9-level system on 8 qubits | Accurate short- and long-time FMO and radical-pair dynamics **on a simulator** | Challenge reference [11]. At N = 300 it needs 18 qubits and ~$10^{13}$ gates. The classical $O(r^3)$ step is the whole classical cost |
| Mitarai & Fujii [41]                                   | 2021 | Defines **channel robustness of non-locality**; upper-bounds the quasiprobability decomposition of a general two-qubit unitary channel into local channels | Framework, not a circuit                                               | Explicit decomposition and bound                                               | The technique that would let a 20-qubit-coherent device address a 300-residue graph — and the $9^k$ cost says it cannot               |
| Mitarai & Fujii [42]                                   | 2021 | The predecessor: virtual two-qubit gate from single-qubit operations                                                                                       | Pauli measurement + $\pi/2$ rotations                                  | **$O(9^k/\varepsilon^2)$ samples for $k$ cuts**                                | The quotable overhead number. Use this, not the Quantum paper, when stating the cost                                                  |
| Piveteau & Sutter [43]                                 | 2023 | Circuit knitting with classical communication                                                                                                              | $n$ non-local CNOTs                                                    | Overhead $O(9^n) \to O(4^n)$                                                   | The best available constant. Even $4^{20} = 1.1\times10^{12}$ is out of reach                                                         |
| Peng, Harrow, Ozols, Wu [44]                           | 2020 | Simulate a large circuit on a small machine by clustering                                                                                                  | $(K,d)$-clustered circuits, $d$-qubit machine                          | Time $2^{O(K)}$; BeH₂ VQE on half the qubits                                   | The framing paper. "Weak interactions among clusters" is the precondition, and a contact graph does not have it                       |
| Schlimgen, Head-Marsden, Sager, Narang, Mazziotti [45] | 2021 | **LCU: any operator = a linear combination of at most four unitaries**                                                                                     | Two-level system, amplitude damping                                    | Agreement with classical calculation                                           | The cheapest compilation route for our sink Hamiltonian                                                                               |
| Schlimgen et al. [46]                                  | 2022 | Dilation via SVD with **one ancilla**; the dilated operator is diagonal                                                                                    | 1 ancilla; sub-normalised two-level states **on a device**             | Dephasing and amplitude damping on hardware                                    | The exact primitive a complex absorbing potential compiles to. Cite it in the C4 section for the sink scorer                          |
| Schlimgen et al. [47]                                  | 2022 | Density-matrix purification: $d\times d$ density matrix as a $d^2$ wavefunction                                                                            | **$n$-qubit** bath instead of $2n$                                     | Two-site Ising on an experimental device                                       | Halves the register for our Lindblad-with-trap scorer. The relevant C3 saving                                                         |
| Delgado-Granados et al. [48]                           | 2024 | Review of quantum algorithms for open quantum systems                                                                                                      | n/a                                                                    | Survey                                                                         | One citation for the whole area                                                                                                       |
| Abbasi, Aydogan, Schlimgen, Head-Marsden [49]          | 2025 | PT-symmetric non-unitary systems simulated via Hermitian equivalents                                                                                       | Two-level                                                              | Similarity-transformation route                                                | The compilation route for a directed-graph PT-symmetric walk, should ADR permit one                                                   |

---

## Q5. Where is quantum genuinely non-classical on a graph?

**Synthesis, and it is the analytical core of this file.** The literature converges on an answer that
is narrower and more useful than "interference and non-local correlations". Four candidate sources of
genuine non-classicality were examined. Three are real; one is a trap; and the three that are real all
have the **same** underlying cause.

**(a) Particle number, not interference, is what buys graph-discrimination power.** Gamble, Friesen,
Zhou, Joynt & Coppersmith [50] tested quantum walks against strongly regular graphs — the standard
hard case for graph isomorphism — and found that walks of **two non-interacting particles cannot
distinguish** certain non-isomorphic SRG pairs, while **two interacting bosons distinguish every pair
examined**, across more than 500 million comparisons `[VERIFIED-ABSTRACT]`. Kasture, Acheche, Henriet
& Henry [51] sharpen this into a theorem: a $k$-particle quantum walk with superposition inputs
distinguishes $k$-CFI graphs that the $k$-dimensional Weisfeiler–Leman test cannot `[VERIFIED-ABSTRACT]`.
**This is independent confirmation, from graph theory rather than from spin physics, of exactly the
conclusion `00-conventions.md` §5 reached by measurement and `23-quantum-node-ranking.md` §8.3 reached
by the QMA-completeness of the Bose–Hubbard model at fixed particle number [71]: the single-particle
sector carries no structural
information beyond its transfer amplitudes, and the hard-core two-excitation sector does.** Three
independent routes to the same statement is as close to settled as this survey gets.

**(b) The phenomena with no classical diffusion analogue are all symmetry phenomena.** Three results,
from three literatures, describing one mechanism:

- **Infinite hitting times.** Krovi & Brun [52] prove that quantum walks can have infinite hitting
  times for certain initial states, with sufficient conditions "based on evolution operator degeneracy
  and **graph automorphism groups**" `[VERIFIED-ABSTRACT]`. Varbanov, Krovi & Brun [53] extend this to
  continuous time: "continuous-time quantum walks, like discrete-time quantum walks but **unlike
  classical random walks**, can have infinite hitting times", and connect it to graph symmetry
  `[VERIFIED-ABSTRACT]`. A classical random walk on a connected graph has finite hitting time to every
  vertex, always. This is a qualitative, not quantitative, separation.
- **Null-eigenvalue localisation.** Bueno & Hatano [54] report that "the adjacency matrices of
  real-world complex networks systematically have **null eigenspaces with much higher dimensions than
  that of random networks**", caused by "duplication mechanisms leading to structures with local
  symmetries", and that the associated eigenvectors are "strongly localized". They then show the
  localisation directly in the spread of a CTQW, and distinguish it sharply from Anderson
  localisation: the eigenvalues sit at the **centre** of the density of states rather than at the
  edges, and the eigenstates "do not decay exponentially and do not leak out of the symmetric
  structures" — closer to a bound state in the continuum `[VERIFIED-ABSTRACT]`.
- **Average mixing matrix rank.** Coutinho, Godsil, Guo & Zhan [56] show the average mixing matrix
  $\hat{M} = \lim_{C\to\infty} C^{-1}\int_0^C H(t)\circ H(-t)\,dt$ "is the matrix of transformation of
  the orthogonal projection onto the **commutant algebra** of the adjacency matrix, restricted to
  diagonal matrices", and find "connections between its **rank and automorphisms of the graph**"
  `[VERIFIED-ABSTRACT]`. Godsil [55] establishes it is positive semidefinite with rational entries,
  and Godsil, Guo & Sobchuk [57] confirm it "**is a graph invariant**; it is the sum of the Schur
  squares of spectral idempotents of the Hamiltonian" `[VERIFIED-ABSTRACT]`.

**The unifying statement, and it is the one to build on.** A classical random walk on a connected
graph converges to a degree-proportional stationary distribution and has finite hitting times,
_regardless of the graph's automorphisms_. A quantum walk does not: degeneracy induced by local
symmetry creates dark subspaces the walker cannot leave and cannot enter, which shows up as infinite
hitting times [52, 53], as null-eigenvector localisation on duplicated motifs [54], and as rank
deficiency in a graph invariant [56, 57]. **Local symmetry is the one graph property that a quantum
walk sees and classical diffusion is blind to.** It is also, conveniently, uncorrelated with Euclidean
distance to the active site by construction — which is precisely the property our measured scorers
lack.

**(c) The exponential separations are structural, not generic.** The glued-trees speedup is an
**oracle** separation on a graph with $2^n$ vertices [61], and the universality result that is often
quoted alongside it is about a **multiparticle** walk on an implicitly specified graph encoding a
circuit [70], not about a 300×300 matrix in memory. Balasubramanian, Li & Harrow [58] generalise
it to random hierarchical graphs and tie it explicitly to "zero-mode localization in disordered
tight-binding models" `[VERIFIED-ABSTRACT]`, which is the same symmetry/degeneracy mechanism again but
now requiring a hierarchical construction we do not have.

**(d) The negative findings, reported honestly — this is the part the report must not skip.**

- **Dequantization.** Tang's review [59] is the canonical citation: quantum machine-learning speedups
  that assume low-rank input with sampling access can be matched classically, and the review's whole
  purpose is to say which claimed advantages survive. Chia, Gilyén, Li, Lin, Tang & Wang [60] give the
  general singular-value-transformation framework. **Do not claim an exponential advantage for any
  linear-algebraic readout of a 300×300 Kirchhoff matrix.**
- **Geometric locality dequantizes short-time dynamics.** Sakamoto & Fujii [62] prove there is no
  exponential quantum advantage — in time _or_ space — for simulating short-time dynamics of
  geometrically local matrices, and close the sampling loophole too. A contact-cutoff Kirchhoff matrix
  is geometrically local by definition. `[VERIFIED-FULLTEXT in file 03 §1; not re-retrieved here]`
- **Mixing-time advantage may be an artefact of the comparison class.** Dervovic [63] constructs, for
  every quantum walk, a **classical lifted Markov chain with faster mixing time**, bounded by the graph
  diameter `[VERIFIED-ABSTRACT]`. If we ever claim a mixing or spreading advantage, this is the paper
  that will be quoted back at us.
- **GBS-on-graphs is dequantized where the adjacency matrix is non-negative** [29], which ours is.
- **Quantum kernels collapse to RBF at our feature dimension** (`00-conventions.md` §5). The quantum
  graph-kernel line [64, 65] builds classifiers from the average mixing matrix and quantum
  Jensen–Shannon-type entropies; these are legitimate _classical_ features derived from a quantum
  object, and should be described that way rather than as quantum computation.

| Citation                                                 | Year    | What it does                                                          | Encoding / qubit count                                   | Result                                                                                                                                                          | Relevance to us                                                                                                                                                         |
| -------------------------------------------------------- | ------- | --------------------------------------------------------------------- | -------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Gamble, Friesen, Zhou, Joynt, Coppersmith [50]           | 2010    | Tests 2-particle walks on strongly regular graphs                     | 2 particles on an $N$-vertex graph; classical simulation | **Non-interacting pairs fail**; **interacting bosons succeed** on >5×10⁸ SRG pairs                                                                              | Independent, graph-theoretic confirmation that interaction — not coherence — is what carries structural information. Directly supports the k = 2 hard-core construction |
| Kasture, Acheche, Henriet, Henry [51]                    | 2025    | Proves $k$-particle walks distinguish $k$-CFI graphs beyond $k$-WL    | $k$ particles, superposition inputs                      | Provable separation from the WL hierarchy                                                                                                                       | Turns [50]'s empirical finding into a theorem. The strongest available justification for a multi-excitation observable                                                  |
| Krovi & Brun [52]                                        | 2006    | **Infinite hitting times** in quantum walks                           | Discrete-time coined walk                                | Sufficient conditions from evolution-operator degeneracy and **graph automorphisms**                                                                            | A qualitative separation from classical walks. The observable is a symmetry property, not a transport rate                                                              |
| Varbanov, Krovi, Brun [53]                               | 2008    | Hitting time for the **continuous-time** walk                         | CTQW with Poisson-distributed measurement                | Infinite hitting times persist in continuous time; tied to symmetry                                                                                             | Extends [52] to our generator. Defines a hitting time our pipeline could actually compute                                                                               |
| Bueno & Hatano [54]                                      | 2020    | **Null-eigenvalue localisation** of CTQWs on real-world networks      | CTQW on adjacency matrices of empirical networks         | Real networks have anomalously large null eigenspaces from duplication/local symmetry; eigenvectors strongly localised; **distinct from Anderson localisation** | The most directly transferable new finding in Q5. A residue graph is a real-world network with duplicated local motifs, and this observable is orthogonal to distance   |
| Godsil [55]                                              | 2011    | Defines the **average mixing matrix** of a CTQW                       | $\hat M = \lim C^{-1}\int_0^C H(t)\circ H(-t)dt$         | Doubly stochastic, positive semidefinite, **rational entries**                                                                                                  | Our required deliverable — an N×N connectivity matrix — _is_ this object. Worth saying in the report                                                                    |
| Coutinho, Godsil, Guo, Zhan [56]                         | 2017    | Reinterprets $\hat M$ as projection onto the commutant algebra        | n/a                                                      | **Rank of $\hat M$ ↔ graph automorphisms**                                                                                                                      | The bridge between the average mixing matrix and symmetry. Makes the symmetry observable computable from a single eigendecomposition                                    |
| Godsil, Guo, Sobchuk [57]                                | 2019    | Diagonal entries of $\hat M$                                          | n/a                                                      | $\hat M$ **is a graph invariant**, the sum of Schur squares of spectral idempotents                                                                             | $\hat M_{ii}$ is a per-residue, source-free localisation score at zero extra cost                                                                                       |
| Balasubramanian, Li, Harrow [58]                         | 2025    | Exponential walk speedups on random hierarchical graphs               | Welded-tree generalisation                               | Superpolynomial-to-exponential, tied to **zero-mode localisation**                                                                                              | Confirms the mechanism, and confirms it needs hierarchy. Do not claim it for a contact graph                                                                            |
| Tang [59]                                                | 2022    | Review of dequantization                                              | n/a                                                      | Which QML advantages survive                                                                                                                                    | The mandatory citation before any linear-algebra advantage claim                                                                                                        |
| Chia, Gilyén, Li, Lin, Tang, Wang [60]                   | 2019    | Sampling-based sublinear framework for dequantizing QML               | n/a                                                      | General singular-value-transformation dequantization                                                                                                            | The technical form of [59]                                                                                                                                              |
| Sakamoto & Fujii [62]                                    | 2026    | Dequantizes short-time dynamics of geometrically local matrices       | n/a                                                      | No exponential advantage in time or space; sampling loophole closed                                                                                             | Our Kirchhoff matrix is geometrically local. This is the theorem that bounds the whole propagation branch                                                               |
| Dervovic [63]                                            | 2017    | Classical lifted Markov chains matching quantum walk mixing           | n/a                                                      | For every quantum walk, a **faster-mixing** lifted classical chain exists                                                                                       | The counterargument to any mixing-speed claim we might make                                                                                                             |
| Bai, Cui, Hancock [64]; Cui, Li, Wang, Bai, Hancock [65] | 2022–23 | Graph kernels built from the CTQW average mixing matrix and entropies | Classical computation of a quantum object                | Competitive graph classification                                                                                                                                | Shows the average mixing matrix is already a usable machine-learning feature — classically                                                                              |

---

## Q6. Reducing the instability of quantum observables on graphs

**Synthesis. The standard stabilisation is time-averaging, and the field has a theorem saying that
time-averaging is exactly what turns a quantum walk into a degree ranking.** This is the finding that
explains our measured problem, and it was not in the repository.

**Faccin, Johnson, Biamonte, Kais & Migdał, _Phys. Rev. X_ 3, 041007 (2013)** [66], read via `ar5iv`
this session. They relate the long-time-average quantum distribution to the classical one
`[VERIFIED-FULLTEXT via ar5iv]`:

- The classical long-time distribution is degree: $(P_C)_i = d_i / \sum_j d_j$ (their Eq. 1), and "the
  probability of finding the walker at any node $i$ is given purely by the importance of the degree
  $d_i$ of that node".
- The quantum long-time average is
  $(P_Q)_i = \lim_{T\to\infty} \frac{1}{T}\int_0^T dt\, \langle i|U(t)\rho(0)U^\dagger(t)|i\rangle$
  (their Eq. 2).
- The deviation they call _quantumness_ is $\varepsilon = 1 - \langle\phi_0|\rho(0)|\phi_0\rangle$
  (their Eq. 6), with $|\phi_0\rangle$ the zero-energy state, and it is **bounded by the energy of the
  initial state relative to the spectral gap**, $E/\Delta \ge \varepsilon$.
- From the abstract `[VERIFIED-ABSTRACT]`: "The quantum distribution becomes **exactly equal to the
  classical distribution when the walk has zero energy** and at higher energies the difference, the
  so-called quantumness, is bounded by the energy of the initial state."

**Read this against our measurement.** Our time-averaged CTQW observables correlate 0.65–0.85 with
distance and collapse under detrending. [66] says the time-averaged distribution of a low-energy
initial state on a graph **is** the degree distribution, with the deviation bounded above by
$E/\Delta$. Time-averaging is not a neutral stabiliser; it is a projection onto the classical answer.
The parameter that controls how much quantum content survives is the **energy of the initial state**,
and nothing in our pipeline currently sets it deliberately.

**The rest of the stabilisation literature, in the order of usefulness:**

1. **Time-averaging / the average mixing matrix** is the field's default, and it converges to a
   _rational_ graph invariant [55, 57]. It is stable by construction — and by [66], stably classical
   unless the initial state carries energy.
2. **Averaging is limited from below by degeneracy.** Agliari, Blumen & Mülken [72] examine "the lower
   bound of long time averages" and show that substrate topology and finiteness jointly determine it;
   Mülken & Blumen's review [77] is the standard reference for the identity that the long-time average
   is a sum over degenerate eigenvalue subspaces. Degeneracy therefore sets a floor no amount of
   averaging removes — which is also, per Q5, where the non-classical content lives.
3. **Spectral-gap dependence is quantified.** Chakraborty, Luh & Roland [67] prove upper bounds on
   quantum mixing time for nearly all networks via random matrix theory, obtaining
   $O(n^{3/2+o(1)})$ for dense random networks `[VERIFIED-ABSTRACT]`. Faccin et al.'s bound $E/\Delta
   \ge \varepsilon$ makes the gap $\Delta$ appear directly in the quantumness budget.
4. **Perturbation sensitivity has been computed exactly, once.** Giordano & Martin-Delgado [68] give a
   rigorous perturbative analysis of **single-link removal** in a Szegedy walk: the transition-matrix
   perturbation has spectral norm $\Theta(1/n)$, the gap eigenvalue shift is $\Theta(1/n^2)$, the
   eigenphase shift is $\Theta(1/n^2)$, and the change in success probability is bounded by
   $O(1/\sqrt{n})$, **dominated by geometric misalignment of the effective subspace rather than by the
   spectral shift** `[VERIFIED-ABSTRACT]`. The setting is a complete graph, so the constants do not
   transfer — but the diagnosis does: the fragile part is the _subspace alignment_, not the spectrum.
   Stabilisation should therefore project onto a subspace, not smooth a spectrum.
5. **Degree normalisation is a real and under-used knob.** Malmi, Rossi, García-Pérez & Maniscalco [69]
   find that CTQW spatial-search performance on renormalised Internet networks "strongly depends on the
   degree of the nodes" `[VERIFIED-ABSTRACT]`; Adithya, Hegde & Meena [73] find degree heterogeneity
   plus postselection preferentially traps excitations at **low-degree** nodes `[VERIFIED-ABSTRACT]`;
   Ide & Konno [74] show CTQW localisation at the starting point on scale-free graphs where the
   classical walker spreads uniformly `[VERIFIED-ABSTRACT]`. The concrete lever is the choice of
   generator: adjacency $A$, combinatorial Laplacian $L = D - A$, and normalised Laplacian
   $D^{-1/2}LD^{-1/2}$ give different degree dependence, and [66]'s zero-energy state is the
   degree-weighted one.
6. **Structural disorder degrades transport in a way that is well documented.** Anishchenko, Blumen &
   Mülken [75] find strong eigenstate localisation on random 2D structures "in geometries where
   classical transport succeeds"; Tsomokos [76] finds that under link failure "the reconfiguration of
   the quantum walk is determined by the **community structure** of the network"; Duda et al. [78]
   report that "arbitrarily weak concentrations of randomly removed lattice sites give rise to a
   complete breakdown of the superdiffusive quantum speed-up". Our graphs are irregular random
   geometries. Expect the _speed_ claims to fail and design the observable so it does not depend on
   them.
7. **Connectivity is a poor predictor of trapped-walk efficiency.** Razzoli, Paris & Bordone [79]
   determine analytically the maximum-transport-efficiency subspace for a CTQW with a single trap and
   conclude that "connectivity is a poor indicator for transport efficiency". That is a published
   reason to expect a trapped-walk observable _not_ to collapse onto degree — the one encouraging
   result in this section. `[VERIFIED-ABSTRACT in file 23; not re-retrieved here]`

**The recommended stabilisation protocol, assembled from the above.** (i) Report the time-averaged
observable, because it is a rational graph invariant [55, 57] and therefore hyperparameter-free.
(ii) Report the **initial-state energy** $E$ and the spectral gap $\Delta$ alongside it, and treat
$E/\Delta$ as the ceiling on how much non-classical content the number can possibly contain [66].
(iii) Choose the generator explicitly and report which one, because adjacency and Laplacian differ in
their degree dependence. (iv) Do not report a single-time observable without a horizon sweep, and
report Kendall $\tau$ between horizons as a stability statistic. (v) Where the observable is a
projection (a trapped subspace, a null eigenspace), report subspace alignment rather than eigenvalue
shift, because [68] shows alignment is the fragile quantity.

| Citation                                         | Year | What it does                                                                         | Encoding / qubit count                    | Result                                                                                                                                  | Relevance to us                                                                                                                                                          |
| ------------------------------------------------ | ---- | ------------------------------------------------------------------------------------ | ----------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Faccin, Johnson, Biamonte, Kais, Migdał [66]** | 2013 | Relates the CTQW long-time-average distribution to the classical degree distribution | CTQW on complex networks; analytic        | $(P_C)_i \propto d_i$; **$P_Q = P_C$ exactly at zero energy**; quantumness $\varepsilon \le E/\Delta$                                   | **The theorem that explains our measured failure.** Time-averaging projects toward degree; the initial-state energy is the only lever. Not previously in this repository |
| Chakraborty, Luh, Roland [67]                    | 2020 | Upper bounds on quantum mixing time for nearly all networks                          | Random matrix theory                      | $O(n^{3/2+o(1)})$ for dense random networks                                                                                             | Makes the spectral gap explicit in the stabilisation budget                                                                                                              |
| Giordano & Martin-Delgado [68]                   | 2026 | Exact perturbation analysis of **single-link removal** in a Szegedy walk             | Complete graph, $n$ nodes, $m$ marked     | Norm $\Theta(1/n)$; eigenphase shift $\Theta(1/n^2)$; success-probability change $O(1/\sqrt n)$, **dominated by subspace misalignment** | The only quantitative edge-perturbation result retrieved. Says to stabilise the subspace, not the spectrum                                                               |
| Malmi, Rossi, García-Pérez, Maniscalco [69]      | 2022 | CTQW spatial search on renormalised real Internet networks                           | CTQW                                      | Performance "strongly depends on the degree of the nodes"; better than $O(N)$, worse than $O(\sqrt N)$                                  | Degree dependence is measured, not assumed, on real irregular networks                                                                                                   |
| Agliari, Blumen, Mülken [72]                     | 2008 | Long-time averages in restricted geometries                                          | CTQW on finite discrete structures        | Derives the **lower bound** of long-time averages from topology and finiteness                                                          | The floor that averaging cannot remove — and it is the degeneracy floor                                                                                                  |
| Adithya, Hegde, Meena [73]                       | 2026 | Postselection-induced localisation on heterogeneous networks                         | Quantum stochastic walk with dephasing    | Degree heterogeneity + postselection traps excitations at **low-degree** nodes                                                          | An explicitly anti-degree mechanism. Rare, and directly targets our confound                                                                                             |
| Ide & Konno [74]                                 | 2010 | CTQW on scale-free threshold networks                                                | CTQW                                      | Quantum walker **localises at the start**; classical spreads uniformly                                                                  | Localisation at the source is the failure mode a source-conditioned quantum ranking risks                                                                                |
| Anishchenko, Blumen, Mülken [75]                 | 2013 | CTQW on random 2D structures                                                         | Long-time-average survival probability    | Strong eigenstate localisation "where classical transport succeeds"                                                                     | Our graphs are random geometries. Sets expectations                                                                                                                      |
| Tsomokos [76]                                    | 2011 | CTQW under connection instabilities                                                  | CTQW on networks with community structure | Reconfiguration "determined by the community structure"                                                                                 | Links robustness to modularity — the Q2 object                                                                                                                           |
| Mülken & Blumen [77]                             | 2011 | The standard CTQW review                                                             | n/a                                       | Long-time average as a sum over degenerate subspaces                                                                                    | The identity behind the averaging floor                                                                                                                                  |
| Duda, Ivaki, Sahlberg, Pöyhönen, Ojanen [78]     | 2023 | Percolation-generated 2D random lattices                                             | DTQW                                      | "Arbitrarily weak" site removal destroys superdiffusive speed-up                                                                        | The strongest reason not to make a speed claim                                                                                                                           |
| Razzoli, Paris, Bordone [79]                     | 2021 | CTQW with a single trap, across topologies                                           | Analytic maximum-efficiency subspace      | "**Connectivity is a poor indicator for transport efficiency**"                                                                         | The one published result predicting a trapped-walk observable is _not_ a degree proxy                                                                                    |

---

## Candidate constructions for this project

Ranked by expected information per unit implementation cost. Every one is (i) not already implemented
in `allo.quantum` or `allo.classical`, (ii) C1/C2/C6-clean, and (iii) accompanied by the classical
control that would expose it as a distance proxy. Qubit and depth figures are for **N = 300**, using
the repository's established one-hot single-excitation encoding (file `08` §2.1): $N$ qubits,
$N(N-1)/2 = 44{,}850$ two-qubit Givens gates, depth $N = 300$, line connectivity. All arithmetic
computed this session.

Nothing below is evidence that any of it beats `−distance` at AUC 0.617, `cavity_volume`, eigenvector
centrality, or APOP/ESSA. Each is a hypothesis with a cheap classical test attached.

---

**C1. High-energy initial state on the active site (the quantumness lever).**

- **(a) What it computes.** The same time-averaged CTQW occupation we already compute, but from an
  initial state deliberately chosen to maximise $\varepsilon \le E/\Delta$ [66] instead of the
  site-basis state $|s\rangle$, which is low-energy and therefore near-classical. Concretely: among
  superpositions supported on the active-site residues, choose the one maximising
  $\langle\psi|H|\psi\rangle$ (the top eigenvector of $H$ restricted to the active-site subspace, i.e.
  a **signed** combination of active-site amplitudes), and report both the ranking and the achieved
  $E/\Delta$.
- **(b) Classical fallback / honest baseline.** The same ranking from the unsigned uniform active-site
  state, which by [66] approaches the degree distribution. The pair is a matched comparison: same
  operator, same graph, same averaging, one number different. If the two rankings agree, the
  observable has no quantum content and we have proved it rather than suspected it.
- **(c) Resources at N = 300.** 300 qubits, 44,850 two-qubit gates, depth 300 — **identical to the
  circuit we already have**; the change is in state preparation only (a $|A|$-qubit preparation over
  the active-site support, negligible). Classically: one $O(N^3) = 2.7\times10^7$-flop `eigh`.
- **(d) Why it is not a distance proxy.** Because [66] proves the _low_-energy limit is the degree
  distribution and bounds the deviation by $E/\Delta$. This construction maximises exactly that bound.
  It is the only candidate here with a theorem stating the mechanism by which it differs from
  diffusion. **Build this first — it is a few lines and it directly tests the diagnosis.**

---

**C2. Symmetry-dark-state overlap from the active site.**

- **(a) What it computes.** For each residue $i$, the weight of $|i\rangle$ in the localised
  null/degenerate eigenspaces that local symmetry creates [54, 52, 56]. Two concrete forms: the
  null-space projection $\|P_0|i\rangle\|^2$ where $P_0$ projects onto the 0-eigenspace of $A$; and the
  source-conditioned form $\sum_{r:\ \dim E_r>1} (E_r)_{is}^2$, restricting the average mixing matrix
  column to degenerate spectral idempotents.
- **(b) Classical fallback.** Two controls, both required. (i) Graph automorphism orbits computed with
  a classical isomorphism tool — if the quantum score is a relabelling of orbit size, it is classical
  graph theory in costume. (ii) The full average mixing matrix column, which is the observable we
  already compute; the degenerate part must add information beyond it.
- **(c) Resources at N = 300.** One $O(N^3)$ `eigh` at $2.7\times10^7$ flops, seconds. On hardware
  there is no circuit — this is a spectral post-processing step, so its C4 story is the QPE route [31]
  applied to the degenerate block, and it should be presented as quantum-inspired under C4.
- **(d) Why it is not a distance proxy.** The null-eigenspace weight is a function of **local
  duplication motifs** [54], with no dependence on the source and therefore no distance ordering built
  in. Bueno & Hatano show explicitly that this localisation is _not_ Anderson localisation — the
  eigenvalues sit at the centre of the density of states, not at the edges — so it is not a disorder
  effect either. Its risk is the opposite one: being uninformative rather than being a proxy.

---

**C3. Two-excitation hard-core transfer and the interaction excess.**

- **(a) What it computes.** $g_2(i,j,t) = |\langle\{i,j\}|e^{-iHt}|\{s_1,s_2\}\rangle|$ with both
  source excitations on active-site residues, ranked by the marginal over $j$; and the **interaction
  excess** $\Delta(i,j,t) = g_2 - g_1(i,t)g_1(j,t)$, which is identically zero if the sector were free.
- **(b) Classical fallback.** $\Delta \equiv 0$ _is_ the fallback — it is a built-in null. The free
  product $g_1 g_1$ is computable from the single-particle propagator we already have.
- **(c) Resources at N = 300.** Circuit: **identical** — the XY Hamiltonian conserves excitation
  number, so the same 44,850-gate, depth-300, line-connectivity Givens network propagates a
  two-excitation state; the only change is one extra X gate in state preparation. Classical:
  $\binom{300}{2} = 44{,}850$ basis states with ≈19 nonzeros per row ($\approx 8.5\times10^5$
  nonzeros), so a sparse Krylov matvec is ~$10^6$ flops. Trivial.
- **(d) Why it is not a distance proxy.** Two independent theorem-level supports, from different
  literatures: the Bose–Hubbard model on a graph at fixed particle number is QMA-complete in the
  hard-core sector [71] (`23-quantum-node-ranking.md` §8.3), and **non-interacting two-particle walks
  provably fail to distinguish graph pairs that interacting bosons distinguish** [50], with the
  separation from the WL hierarchy proved in [51]. This is the construction with the strongest
  literature support in the whole survey.
- **Note.** This is already argued in `23-quantum-node-ranking.md` §8.3 as items 1–2. It is repeated
  here because Q5 supplies **new, independent** graph-theoretic evidence for it. If the priority list
  in that file has not yet been executed, this survey raises rather than lowers its priority.

---

**C4. Quantum-transport community detection, source-anchored.**

- **(a) What it computes.** Faccin et al.'s quantum community detection [15], with the closeness
  measure being the CTQW transport probability from the active site, then modularity maximisation over
  that closeness matrix. The output is the community containing the active site and, more usefully,
  the _second_ community with the highest inter-community transport — the candidate allosteric module.
- **(b) Classical fallback.** Markov Stability multiscale community detection on the same graph [23],
  which is the published classical method for exactly this task and is C1/C2/C6-clean. Also the
  classical modularity partition of the plain contact graph. If the quantum closeness matrix yields
  the same partition, the construction is closed in one run.
- **(c) Resources at N = 300.** Classical: one $O(N^3)$ `eigh` plus a modularity optimisation on a
  dense $300\times300$ closeness matrix — seconds. On hardware: the closeness matrix needs $N$ transport
  probabilities, i.e. $N$ runs of the 44,850-gate circuit, so 300 circuit executions at depth 300. That
  is a fault-tolerant proposition, and the honest C3 line says so.
- **(d) Why it is not a distance proxy.** The output is a **partition**, not a per-residue scalar
  derived from a propagator column, so it cannot be a monotone function of distance. The risk is
  different and should be stated: modularity on a spatially embedded graph tends to recover spatial
  domains, so the partition may be a _domain_ detector rather than an allostery detector. The Markov
  Stability control [23] is what distinguishes the two.

---

**C5. Relative dimension with respect to the active site (classical, and it should exist regardless).**

- **(a) What it computes.** Peach, Arnaudon & Barahona's relative dimension [27]: a scale-dependent
  dimension assigned to each node relative to a diffusive source, whose published application is
  precisely "regions involved in allosteric communication" relative to the active site.
- **(b) Classical fallback.** It _is_ classical. Its own control is `−distance` and the matched-patch
  null.
- **(c) Resources at N = 300.** One diffusion solve per scale over a logarithmic grid of ~30 scales:
  $30 \times O(N^2)$ with a reused factorisation, well under a second.
- **(d) Why it is not a distance proxy.** It is scale-_resolved_: a node's relative dimension is a
  curve over diffusion time, not a scalar, and the published claim is that the curve's shape (not its
  level) marks allosteric regions. The level is likely a distance proxy; the shape is what to test.
- **Note.** This is not a quantum construction. It is in this list because it is the strongest
  source-conditioned classical baseline the survey found, we do not have it, and **no quantum result on
  this problem is credible until it has been compared against it.** One implementation, in
  `classical/coupling`.

---

**C6. Average-mixing-matrix invariants as the N×N deliverable.**

- **(a) What it computes.** The full average mixing matrix $\hat M$ [55, 56, 57] as the required N×N
  connectivity deliverable, plus three cheap invariants derived from it: its rank (which tracks graph
  automorphisms [56]), its trace (the walk's "laziness"), and its diagonal $\hat M_{ii}$ (per-residue
  long-time return probability, a localisation score).
- **(b) Classical fallback.** The classical random-walk return probability and the degree vector. By
  [66], $\hat M$'s row sums approach the degree distribution in the low-energy limit, so the degree
  control is mandatory and must be reported beside it.
- **(c) Resources at N = 300.** One $O(N^3)$ `eigh`, then $\hat M_{ij} = \sum_r (E_r)_{ij}^2$ formed in
  $O(N^3)$ — $2.7\times10^7$ flops, seconds. No circuit; C4 story is [31].
- **(d) Why it is not a distance proxy.** The _column_ from the source is a proxy, and we should say so
  — it is the time-averaged transfer we already measured. The **rank and diagonal** are not: they are
  source-free symmetry quantities [56, 57]. The value here is partly presentational and it is real:
  our required deliverable already is a named, published graph invariant with proven rationality and
  positive semidefiniteness, which is a stronger thing to write in a report than "an N×N matrix we
  defined".

---

**C7. Infinite-hitting-time / dark-subspace diagnostic.**

- **(a) What it computes.** For a walk launched at the active site, the fraction of the initial state
  lying in subspaces from which residue $i$ is unreachable — operationally, $1 - \sum_t$ (detected
  probability at $i$) in the Varbanov–Krovi–Brun continuous-time hitting-time formalism [53], with the
  measurement-rate parameter swept.
- **(b) Classical fallback.** The classical random-walk hitting time from the active site to residue
  $i$, which is finite for every $i$ on a connected graph and computable in $O(N^3)$ from the Laplacian
  pseudo-inverse — which we already form for effective resistance.
- **(c) Resources at N = 300.** One $O(N^3)$ `eigh` plus $O(N^2)$ per measurement rate; a 20-point
  sweep is ~$10^8$ flops. On hardware: the existing circuit plus one ancilla and $r$ mid-circuit
  resets, i.e. $+r$ two-qubit gates over 44,850 — under 0.1 % of the budget at $r = 32$.
- **(d) Why it is not a distance proxy.** The classical comparison quantity is _provably always finite_
  and the quantum one is _provably sometimes infinite_ [52, 53], and the difference is caused by
  automorphisms, not by geometry. The gap between the classical and quantum hitting times is therefore
  a clean symmetry observable with an exactly-zero null for a graph with trivial automorphism group.
- **Caveat.** Real protein contact graphs are unlikely to have exact automorphisms. The observable will
  have to be relaxed to near-degeneracy with a tolerance, which reintroduces a hyperparameter — choose
  it on `development` only.

---

**C8. Modularity-QUBO site selection, run once as a resource-honest negative.**

- **(a) What it computes.** The community-detection QUBO of [13] on the residue contact graph with the
  active site fixed to one community, solved classically, with the D-Wave-style one-hot encoding costed
  but not run.
- **(b) Classical fallback.** Louvain and Markov Stability [23], both of which [14] concedes the
  quantum route only matches or slightly exceeds.
- **(c) Resources at N = 300.** With $k$ communities the QUBO has $kN$ binary variables: at $k = 8$
  that is **2,400 logical variables**, against a hardware ceiling demonstrated at **34 nodes** [13].
  Minor-embedding overhead on a Chimera/Pegasus topology multiplies this further.
- **(d) Why it is not a distance proxy.** A partition is not a scalar ranking. But the honest
  expectation is failure: `00-conventions.md` §5 item 6 plus the submodularity diagnosis, plus the
  fault-tolerant estimate of a day and a million physical qubits against four CPU-minutes [28].
  **Recommended only as a costed C3 section, not as a method.** Its value to the submission is the
  2,400-variables-against-34-nodes comparison, which is a concrete near-term-viability statement.

---

**Priority.** Build **C1** first (a few lines, a theorem behind it, and it directly tests why our
existing scorers fail). Then **C5**, because it is classical, cheap and no quantum claim is credible
without it. Then **C3**, which reuses the existing circuit unchanged and has the strongest hardness
argument. Then **C2** and **C7**, which are the two symmetry observables and share an eigendecomposition.
**C4** and **C6** are cheap add-ons to work already done. **C8** is a resource paragraph, not an
experiment.

---

## What the literature does NOT support

Claims to avoid, each with the source that would be quoted back at us.

1. **"Quantum walks give an exponential speedup for signal propagation on a protein contact graph."**
   The glued-trees separation is an _oracle_ separation on a $2^n$-vertex implicitly specified graph
   [61]; Sakamoto & Fujii [62] prove no exponential advantage exists in time or space for short-time
   dynamics of geometrically local matrices, which a contact-cutoff Kirchhoff matrix is.
2. **"Quantum computers uniquely capture non-local correlations and interference in biological signal
   propagation."** The single-particle sector on a real, non-negative, symmetric adjacency matrix has
   no sign structure to interfere with [29], and the photosynthesis premise behind the analogy has been
   retracted by its own field (Cao et al. 2020, `03-quantum-methods.md` §10).
3. **"Our quantum ranking beats classical centrality."** Not without the personalised-PageRank,
   degree, `−distance` and relative-dimension [27] controls run beside it. Faccin et al. [66] prove the
   time-averaged distribution tends to degree; RinQ's own success criterion is agreement with classical
   centrality [3]; and the published CTQW-on-RIN result reports strong agreement with classical
   eigenvector centrality (`00-conventions.md` §5).
4. **"Elastic network models get an exponential quantum speedup."** Babbush et al.'s speedup is
   conditional on polylog-time query access to masses and spring constants [30]; Liu et al. [32] prove
   a protein's connectivity matrix is incompressible and needs $\Omega(N)$ bits; Kolotouros et al. [33]
   state normal modes cannot be extracted from the encoding at all. The general structural-mechanics
   result is polynomial [34, 35] or quadratic [36].
5. **"Quantum optimisation finds better allosteric sub-graphs."** Community-detection QUBOs are
   demonstrated on 34 nodes on hardware [13]; the hybrid results that scale are dominated by their
   classical component [14]; the fault-tolerant estimate for the Szegedy-accelerated version is a day
   and a million physical qubits against four CPU-minutes [28]; and GBS-on-graphs is dequantized for
   non-negative adjacency matrices [29].
6. **"Quantum machine learning on protein structures outperforms classical."** The strongest retrieved
   claim is "slightly better performance" on graph-level classification with a 256-qubit analogue
   simulator [6], on a task that is not ours, with 24 % of protein graphs unembeddable [7]. Quantum
   kernels are pre-refuted at our feature dimension (`00-conventions.md` §5).
7. **"Circuit cutting lets us run the full-size graph on near-term hardware."** $O(9^k/\varepsilon^2)$
   samples for $k$ cuts [42], $O(4^n)$ at best with classical communication [43]. Twenty cuts is
   $1.2\times10^{19}$ samples; a balanced partition of our graph needs far more than twenty.
8. **"A quantum walk mixes or spreads faster, therefore it finds allosteric sites faster."** For every
   quantum walk there is a classical lifted Markov chain that mixes faster [63], and superdiffusive
   spreading collapses under arbitrarily weak site disorder [78]. Speed is the wrong axis; information
   content is the right one.
9. **"We are the first to apply quantum computing to protein site prediction."** We are not: Grover
   search for docking sites on IBM hardware [1], hydration-site QUBO on 123 qubits [2], residue
   centrality as a QUBO [3], binding-site structure by VQE [4]. **What was not retrieved is a quantum
   method scored against allosteric ground truth with a stated null** — that is the claimable
   first, and it is claimable for a negative result too.
10. **"Time-averaging stabilises the observable without cost."** It stabilises it by converging to a
    degree ranking [66]. Report $E/\Delta$ beside any time-averaged number.

---

## What this changes for our pipeline

1. **Stage S5 — set the initial-state energy deliberately, and report it.** [66] gives the mechanism
   for our measured distance/degree collapse and names the lever. Add $E$ and $\Delta$ to every
   quantum arm's recorded metadata, and add candidate **C1** as a scorer variant. This is the highest
   value-per-line item in the file.
2. **Stage S3 — implement relative dimension with respect to the active site [27] as a classical
   baseline.** It is C1/C2/C6-clean, source-conditioned, published on protein graphs for this exact
   task, and we do not have it. Until it is in `classical.coupling`, no quantum arm has an honest bar.
3. **Report §"quantum metric" — the symmetry framing replaces the interference framing.** Q5 finds
   that the only graph properties a quantum walk sees and classical diffusion does not are symmetry
   properties: infinite hitting times from automorphisms [52, 53], null-eigenvector localisation on
   duplicated motifs [54], and average-mixing-matrix rank [56]. That is a defensible, sourced,
   non-hand-waving answer to the challenge's "non-local correlations and interference" claim, and it is
   a better one than the challenge's own.
4. **Report §"deliverables" — name the N×N matrix.** The average mixing matrix is a published graph
   invariant with proven rationality and positive semidefiniteness [55, 57]. Say so.
5. **Report §"circuit resources" — use the $9^k$ table.** The organisers' own second reference [41, 42]
   supplies a quantitative bound showing circuit cutting cannot bridge our N ≈ 20 coherence ceiling to
   N = 300. Presenting their reference as a computed constraint rather than a citation is the strongest
   available demonstration that C3 was taken seriously.
6. **Report §"quantum biology" — cite [46] and [47] as the compilation route for the sink and Lindblad
   scorers.** One ancilla for the dilated diagonal operator [46]; an $n$-qubit rather than $2n$-qubit
   register via density-matrix purification [47]. Both are demonstrated on devices. This turns our two
   non-unitary scorers from "simulated classically" into "simulated classically, with a named,
   hardware-demonstrated compilation".
7. **Prioritise the k = 2 hard-core sector.** Q5 supplies independent graph-theoretic evidence [50, 51]
   for the same conclusion `23-quantum-node-ranking.md` §8.3 reached from QMA-completeness. Three
   independent routes agree, the circuit cost is zero, and the classical check is $10^6$ flops.
8. **Do not build a QUBO node-selection method,** and do write the 2,400-variables-against-34-nodes
   comparison [13] into the C3 section as a resource result.
9. **Open item.** No literature was retrieved casting an allosteric pathway as a Steiner tree or
   minimum cut and solving it quantumly, and none casting a residue graph as a QAOA max-cut. Both are
   recorded as search outcomes under ADR 0019, not as absence-of-prior-art claims.

---

## Method

**Databases.** arXiv API `export.arxiv.org/api/query` (both `search_query` and `id_list` forms);
arXiv abstract pages; `ar5iv.labs.arxiv.org` HTML full text; PubMed and PMC article pages; PLOS ONE
article page; `quantum-journal.org` article page; general web search. **Europe PMC's REST search
endpoint returned only `{"version":"6.9"}` on three attempts through the available fetch route and
could not be used**; PubMed and PMC pages were substituted. Semantic Scholar was not attempted
(rate-limited per `00-conventions.md` §3). `pubmed.ncbi.nlm.nih.gov` article pages returned a cookie
wall; `pmc.ncbi.nlm.nih.gov` worked after following a 301 from `www.ncbi.nlm.nih.gov/pmc/`.

**Queries run (17 structured + 8 web).**

arXiv `search_query`:
`all:"Exponential quantum speedup in simulating coupled classical oscillators"`;
`au:"Schlimgen" AND cat:quant-ph`;
`abs:"binding site" AND (abs:"quantum computing" OR abs:"quantum algorithm" OR abs:"quantum machine learning" OR abs:"quantum annealing")`;
`(abs:"quantum annealing" OR abs:"QAOA" OR abs:"QUBO") AND (abs:"protein" OR abs:"residue network" OR abs:"protein structure")`;
`(abs:"finite element" OR abs:"normal mode" OR abs:"vibrational analysis" OR abs:"structural dynamics" OR abs:"eigenvalue problem") AND (abs:"quantum algorithm" OR abs:"quantum phase estimation")`;
`abs:"graph isomorphism" AND abs:"quantum walk"`;
`abs:"quantum walk" AND (abs:"robustness" OR abs:"perturbation" OR abs:"disorder" OR abs:"static noise") AND (abs:"graph" OR abs:"network")`;
`(abs:"continuous-time quantum walk" OR abs:"quantum transport") AND (abs:"complex network" OR abs:"degree distribution" OR abs:"long-time average" OR abs:"limiting distribution")`;
`(abs:"quantum kernel" OR abs:"quantum support vector" OR abs:"quantum neural network" OR abs:"quantum machine learning") AND (abs:"protein" OR abs:"residue" OR abs:"druggab" OR abs:"hot spot")`;
`(abs:"maximum clique" OR abs:"Steiner tree" OR abs:"minimum cut" OR abs:"max-cut" OR abs:"graph partitioning") AND (abs:"protein" OR abs:"allosteric" OR abs:"residue")`;
`(abs:"allosteric" OR abs:"allostery") AND (abs:"network" OR abs:"graph") AND (abs:"pathway" OR abs:"community" OR abs:"partition" OR abs:"flow")`;
`(abs:"allosteric" OR abs:"cryptic site" OR abs:"cryptic pocket") AND abs:"quantum"`;
`(abs:"hitting time" OR abs:"mixing time") AND abs:"quantum walk" AND (abs:"exponential" OR abs:"speedup" OR abs:"classical random walk")`;
`abs:"average mixing matrix"`.
Plus four `id_list` metadata batches covering 21 identifiers:
`2106.12588,2205.02826,2207.07112,2406.05219,2309.17391`;
`2508.01501,2512.08390,2607.09737,2405.06657,2605.13899`;
`2104.00746,2605.04737,2605.03503,2607.19129,2507.00072`;
`1305.6078,2411.03972,1103.2578,1709.03591,2106.05368`; `1909.07534,2205.00016,1904.00102`;
`1310.6638,2001.06305`.

Web: `Schlimgen Head-Marsden Sager Mazziotti "quantum simulation of open quantum systems" unitary
decomposition of operators PRL 2021`; `quantum computing protein binding site prediction quantum
machine learning pocket detection arXiv 2024 2025`; `"community detection" QUBO quantum annealing
D-Wave modularity maximization Negre Ushijima-Mwesigwa Mniszewski`; `Ewin Tang dequantization quantum
machine learning ... limitations 2022`; `Amor Schaub Yaliraki Barahona "bond-to-bond propensities"
allosteric sites Nature Communications 2016`; `Santagati "Drug design on quantum computers" Nature
Physics 2024`; `Robert Barkoutsos Woerner Tavernelli "Resource-efficient quantum algorithm for protein
folding" npj Quantum Information 2021 qubits`; `"brain connectomes" hybrid quantum computing community
detection Scientific Reports 2023 QUBO modularity`; `"Quantum algorithm for protein-ligand docking
sites identification in the interaction space" 2025 authors journal DOI qubits`; `pubmed quantum
computing algorithm allosteric site prediction protein residue interaction network benchmark AUC`
(domain-restricted to PubMed/PMC/Nature/ACS/OUP); `"Degree Distribution in Quantum Walks on Complex
Networks" Faccin ... abstract stationary state degree`.

**Counts.** ≈340 records returned; **71 screened in** on title and abstract; **44 records had title,
authors, journal reference, DOI and full abstract re-retrieved from a primary index this session**;
**two full texts landed and read** — `ar5iv` for arXiv:1305.6078 (Faccin et al.), and the PMC article
page for PMC12228596 (Liliopoulos et al.). All flop counts, sample counts, binomial coefficients and
qubit/gate figures were computed this session by elementary arithmetic.

**Stopping rule.** Stopped when (i) three independent literatures — multi-particle graph
discrimination [50, 51], quantum-walk hitting times [52, 53], and algebraic graph theory of the
average mixing matrix [56, 57] — converged on the same mechanism (local symmetry as the sole
non-classical graph property visible to a walk); (ii) Q6 produced a theorem [66] that explains the
project's measured failure mode and names its control parameter; and (iii) the Q1 sweep for a quantum
method scored against allosteric labels returned nothing across arXiv and PubMed, reproducing
`03-quantum-methods.md` §11(d) from an independent query set.

**Could not be reached.**
(i) Europe PMC REST — endpoint returned only a version string; three attempts.
(ii) Full text of Mitarai & Fujii, _Quantum_ **5**, 388 — the `ar5iv` conversion of arXiv:2006.11174
failed with a fatal error, so the explicit channel-robustness bound for a general two-qubit unitary is
`[VERIFIED-ABSTRACT]` only. The $9^k$ figure quoted comes from the predecessor paper [42], whose
abstract states it verbatim.
(iii) Full text of Babbush et al. [30] — abstract and metadata re-verified this session; the
limitation quotes in `03-quantum-methods.md` §6.1 were not re-retrieved.
(iv) Full text of Faccin et al. [66] beyond the four extracted items — the definition of
$|\phi_0\rangle$ as the zero-energy state, and the exact generator convention (adjacency versus
Laplacian) under which $(P_C)_i \propto d_i$ holds, were read from the `ar5iv` extraction but the
surrounding derivation was not. **Our reading that this makes the Laplacian generator with a
low-energy source state a guaranteed degree ranking is `[UNVERIFIED]` inference and must be confirmed
against the full text before it reaches `docs/report/`.**
(v) Qubit counts and runtime figures from Lee & Kanno [31] — the abstract states such estimates are
given; the numbers themselves are in the body, which was not retrieved.
(vi) The article number for Wierzbiński et al. [14]; the DOI is verified, the volume/page is not.
(vii) DOIs for several 2012–2022 items ([20], [21], [22], [12], [52], [53]) were not re-verified
against Crossref this session; the arXiv identifiers given are the resolvable ones and should be
preferred.
(viii) The DOI reported by arXiv metadata for [7] (`10.1109/QCE60285.2024.10281`) does not match the
format of its sibling [6] and may be malformed; cite the arXiv identifier.

---

## References

1. Liliopoulos I, Varsamis GD, Karamanidou T, Papalitsas C, Koulouras G, Pantazopoulos V, Stavropoulos TG, Karafyllidis IG. Quantum algorithm for protein-ligand docking sites identification in the interaction space. J Comput Aided Mol Des. 2025;39(1):40. doi:10.1007/s10822-025-00620-5
2. Loco D, Barkemeyer K, Carvalho ARR, Piquemal J-P. Practical protein-pocket hydration-site prediction for drug discovery on a quantum computer. Phys Rev Research. 2026. doi:10.1103/gyqr-mv1h. arXiv:2512.08390
3. Mohtashim SI. RinQ: Towards predicting central sites in proteins on current quantum computers. Mater Today Quantum. 2025;7:100053. doi:10.1016/j.mtquan.2025.100053. arXiv:2508.01501
4. Zhang et al. A quantum framework for protein binding-site structure prediction on utility-level quantum processors. Adv Sci. 2026. doi:10.1002/advs.202513641. arXiv:2506.22677
5. Li J, Alam M, Sha CM, Wang J, Dokholyan NV, Ghosh S. Drug discovery approaches using quantum machine learning. arXiv:2104.00746
6. Giusto E, Iurlaro G, Montrucchio B, Scionti A, Terzo O, Vercellino C, Vitali G, Viviani P. Harnessing a 256-qubit neutral atom simulator for graph classification. In: IEEE QCE 2024. p. 296–305. doi:10.1109/QCE60285.2024.00043. arXiv:2605.04737
7. Vercellino C, Vitali G, Viviani P, Scionti A, Terzo O, Montrucchio B. Harnessing DEN models for quantum computing tasks on neutral atom QPUs. In: IEEE QCE 2024. p. 217–222. arXiv:2605.03503
8. Roosan D, Khan R, Nirzhor S, Khou T, Hai F. Classifying hotspots mutations for biosimulation with quantum neural networks and variational quantum eigensolver. arXiv:2507.00072
9. Patil P, Bonde B, Choubey B. A quantum circuit framework for protein ensemble-level energetics. arXiv:2608.05491
10. Santagati R, Aspuru-Guzik A, Babbush R, Degroote M, González L, Kyoseva E, et al. Drug design on quantum computers. Nat Phys. 2024;20:549–557. doi:10.1038/s41567-024-02411-5. arXiv:2301.04114
11. Mohtashim SI, Sajjan M, Kais S. Continuous-time quantum-walk centrality for protein residue interaction networks. arXiv:2604.17486. Published version doi:10.1021/jacs.6c08053
12. Li RY, Di Felice R, Rohs R, Lidar DA. Quantum annealing versus classical machine learning applied to a simplified computational biology problem. npj Quantum Inf. 2018;4:14. arXiv:1803.00135
13. Negre CFA, Ushijima-Mwesigwa H, Mniszewski SM. Detecting multiple communities using quantum annealing on the D-Wave system. PLoS ONE. 2020;15(2):e0227538. doi:10.1371/journal.pone.0227538
14. Wierzbiński M, Falcó-Roget J, Crimi A. Community detection in brain connectomes with hybrid quantum computing. Sci Rep. 2023;13. doi:10.1038/s41598-023-30579-y
15. Faccin M, Migdał P, Johnson TH, Bergholm V, Biamonte JD. Community detection in quantum complex networks. Phys Rev X. 2014;4:041012. doi:10.1103/PhysRevX.4.041012. arXiv:1310.6638
16. Triuzzi E, Mengoni R, Micucci F, Bonanni D, Ottaviani D, Beccari A, Palermo G. Molecular docking via weighted subgraph isomorphism on quantum annealers. Quantum Sci Technol. 2025. doi:10.1088/2058-9565/ae0890. arXiv:2405.06657
17. Zheng K, Zhou Y, Li R, Ding Z, Liang Z, Li S. Q-Score: a quantum-native scoring function for molecular docking. arXiv:2607.09737
18. Banchi L, Fingerhuth M, Babej T, Ing C, Arrazola JM. Molecular docking with Gaussian boson sampling. Sci Adv. 2020;6:eaax1950. doi:10.1126/sciadv.aax1950
19. Robert A, Barkoutsos PK, Woerner S, Tavernelli I. Resource-efficient quantum algorithm for protein folding. npj Quantum Inf. 2021;7:38. doi:10.1038/s41534-021-00368-4
20. Perdomo-Ortiz A, Dickson N, Drew-Brook M, Rose G, Aspuru-Guzik A. Finding low-energy conformations of lattice protein models by quantum annealing. arXiv:1204.5485
21. Irbäck A, Knuthson L, Mohanty S, Peterson C. Folding lattice proteins with quantum annealing. Phys Rev Research. 2022;4:043013. arXiv:2205.06084
22. Outeiral C, Morris GM, Shi J, Strahm M, Benjamin SC, Deane CM. Investigating the potential for a limited quantum speedup on protein lattice problems. New J Phys. 2021;23:023012. arXiv:2004.01118
23. Amor B, Yaliraki SN, Woscholski R, Barahona M. Uncovering allosteric pathways in caspase-1 using Markov transient analysis and multiscale community detection. Mol Biosyst. 2014;10(8):2247–58. doi:10.1039/c4mb00088a. arXiv:1411.2847
24. Amor BRC, Schaub MT, Yaliraki SN, Barahona M. Prediction of allosteric sites and mediating interactions through bond-to-bond propensities. Nat Commun. 2016;7:12477. doi:10.1038/ncomms12477. arXiv:1605.09710
25. Wu N, Yaliraki SN, Barahona M. Prediction of protein allosteric signalling pathways and functional residues through paths of optimised propensity. arXiv:2207.07202
26. Delmotte A, Tate EW, Yaliraki SN, Barahona M. Protein multi-scale organization through graph partitioning and robustness analysis. Phys Biol. 2011;8(5):055010. doi:10.1088/1478-3975/8/5/055010. arXiv:1109.4232
27. Peach RL, Arnaudon A, Barahona M. Relative, local and global dimension in complex networks. Nat Commun. 2022;13:1869. doi:10.1038/s41467-022-30705-w. arXiv:2106.05368
28. Sanders YR, Berry DW, Costa PCS, Tessler LW, Wiebe N, Gidney C, Neven H, Babbush R. Compilation of fault-tolerant quantum heuristics for combinatorial optimization. arXiv:2007.07391
29. Oh C, Liu M, Alexeev Y, Fefferman B, Jiang L. Quantum-inspired classical algorithm for graph problems by Gaussian boson sampling. PRX Quantum. 2024;5:020341. doi:10.1103/PRXQuantum.5.020341. arXiv:2302.00536
30. Babbush R, Berry DW, Kothari R, Somma RD, Wiebe N. Exponential quantum speedup in simulating coupled classical oscillators. Phys Rev X. 2023;13:041041. doi:10.1103/PhysRevX.13.041041. arXiv:2303.13012
31. Lee Y, Kanno K. Modal analysis on quantum computers via qubitization. arXiv:2307.07478
32. Liu Z, Li X, Wang C, Liu J-P. Toward end-to-end quantum simulation for protein dynamics. arXiv:2411.03972
33. Kolotouros I, Sireesh A, Ferguson S, Thrasher S, Wallden P, Michel J. Quantum elastic network models and their application to graphene. arXiv:2601.05161
34. Montanaro A, Pallister S. Quantum algorithms and the finite element method. Phys Rev A. 2016;93:032324. doi:10.1103/PhysRevA.93.032324. arXiv:1512.05903
35. Deiml M, Peterseim D. Quantum realization of the finite element method. Math Comp. doi:10.1090/mcom/4137. arXiv:2403.19512
36. Hölscher L, Ahrend O, Karch L, L'Estocq C, Marfany Andreu M, Stollenwerk T, Wilhelm FK, Kowalski J. End-to-end quantum algorithm for topology optimization in structural mechanics. Quantum Sci Technol. doi:10.1088/2058-9565/ae4cfe. arXiv:2510.07280
37. Harrow AW, Hassidim A, Lloyd S. Quantum algorithm for linear systems of equations. Phys Rev Lett. 2009;103:150502. doi:10.1103/PhysRevLett.103.150502
38. Reilly CB. Frequency-space mechanics: a sequence and coordinate-free representation for protein function prediction. arXiv:2605.13899
39. Bartlett SD, Sanders BC, Braunstein SL, Nemoto K. Efficient classical simulation of continuous variable quantum information processes. Phys Rev Lett. 2002;88:097904. doi:10.1103/PhysRevLett.88.097904
40. Oh EK, Krogmeier TJ, Schlimgen AW, Head-Marsden K. Singular value decomposition quantum algorithm for quantum biology. ACS Phys Chem Au. 2024;4(4):393–399. doi:10.1021/acsphyschemau.4c00018. arXiv:2309.17391
41. Mitarai K, Fujii K. Overhead for simulating a non-local channel with local channels by quasiprobability sampling. Quantum. 2021;5:388. doi:10.22331/q-2021-01-28-388. arXiv:2006.11174
42. Mitarai K, Fujii K. Constructing a virtual two-qubit gate by sampling single-qubit operations. New J Phys. 2021;23:023021. doi:10.1088/1367-2630/abd7bc. arXiv:1909.07534
43. Piveteau C, Sutter D. Circuit knitting with classical communication. IEEE Trans Inf Theory. 2023. doi:10.1109/TIT.2023.3310797. arXiv:2205.00016
44. Peng T, Harrow A, Ozols M, Wu X. Simulating large quantum circuits on a small quantum computer. Phys Rev Lett. 2020;125:150504. doi:10.1103/PhysRevLett.125.150504. arXiv:1904.00102
45. Schlimgen AW, Head-Marsden K, Sager LM, Narang P, Mazziotti DA. Quantum simulation of open quantum systems using a unitary decomposition of operators. Phys Rev Lett. 2021;127:270503. doi:10.1103/PhysRevLett.127.270503. arXiv:2106.12588
46. Schlimgen AW, Head-Marsden K, Sager-Smith LM, Narang P, Mazziotti DA. Quantum state preparation and nonunitary evolution with diagonal operators. Phys Rev A. 2022;106:022414. doi:10.1103/PhysRevA.106.022414. arXiv:2205.02826
47. Schlimgen AW, Head-Marsden K, Sager-Smith LM, Narang P, Mazziotti DA. Quantum simulation of open quantum systems using density-matrix purification. arXiv:2207.07112
48. Delgado-Granados LH, Krogmeier TJ, Sager-Smith LM, Avdic I, Hu Z, Sajjan M, Abbasi M, Smart SE, Narang P, Kais S, Schlimgen AW, Head-Marsden K, Mazziotti DA. Quantum algorithms and applications for open quantum systems. arXiv:2406.05219
49. Abbasi M, Aydogan K, Schlimgen AW, Head-Marsden K. Quantum simulation of two-level PT-symmetric systems using Hermitian Hamiltonians. doi:10.1103/gwbz-mbfw. arXiv:2507.08129
50. Gamble JK, Friesen M, Zhou D, Joynt R, Coppersmith SN. Two-particle quantum walks applied to the graph isomorphism problem. Phys Rev A. 2010;81:052313. arXiv:1002.3003
51. Kasture S, Acheche S, Henriet L, Henry L-P. Multiparticle quantum walks for distinguishing hard graphs. arXiv:2501.03683
52. Krovi H, Brun TA. Quantum walks with infinite hitting times. Phys Rev A. 2006;74:042334. arXiv:quant-ph/0606094
53. Varbanov M, Krovi H, Brun TA. Hitting time for the continuous quantum walk. Phys Rev A. 2008;78:022324. arXiv:0803.3446
54. Bueno R, Hatano N. Null-eigenvalue localization of quantum walks on real-world complex networks. Phys Rev Research. 2020;2:033185. doi:10.1103/PhysRevResearch.2.033185. arXiv:2007.00129
55. Godsil C. Average mixing of continuous quantum walks. arXiv:1103.2578
56. Coutinho G, Godsil C, Guo K, Zhan H. A new perspective on the average mixing matrix. arXiv:1709.03591
57. Godsil C, Guo K, Sobchuk M. Diagonal entries of the average mixing matrix. arXiv:1910.02039
58. Balasubramanian S, Li T, Harrow A. Exponential speedups for quantum walks in random hierarchical graphs. Commun Math Phys. 2025;406:209. arXiv:2307.15062
59. Tang E. Dequantizing algorithms to understand quantum advantage in machine learning. Nat Rev Phys. 2022;4:692–702. doi:10.1038/s42254-022-00511-w
60. Chia N-H, Gilyén A, Li T, Lin H-H, Tang E, Wang C. Sampling-based sublinear low-rank matrix arithmetic framework for dequantizing quantum machine learning. arXiv:1910.06151
61. Childs AM, Cleve R, Deotto E, Farhi E, Gutmann S, Spielman DA. Exponential algorithmic speedup by a quantum walk. In: STOC 2003. doi:10.1145/780542.780552
62. Sakamoto K, Fujii K. [Dequantization of short-time dynamics of geometrically local matrices.] Quantum. 2026;10:2182. doi:10.22331/q-2026-08-03-2182. arXiv:2505.10445
63. Dervovic D. For every quantum walk there is a (classical) lifted Markov chain with faster mixing time. arXiv:1712.02318
64. Bai L, Cui L, Hancock ER. QESK: quantum-based entropic subtree kernels for graph classification. arXiv:2212.05228
65. Cui L, Li M, Wang Y, Bai L, Hancock ER. AERK: aligned entropic reproducing kernels through continuous-time quantum walks. arXiv:2303.03396
66. Faccin M, Johnson T, Biamonte J, Kais S, Migdał P. Degree distribution in quantum walks on complex networks. Phys Rev X. 2013;3:041007. doi:10.1103/PhysRevX.3.041007. arXiv:1305.6078
67. Chakraborty S, Luh K, Roland J. How fast do quantum walks mix? Phys Rev Lett. 2020;124:050501. doi:10.1103/PhysRevLett.124.050501. arXiv:2001.06305
68. Giordano S, Martin-Delgado MA. Single link removal perturbation in Szegedy quantum walk: from graph completeness testing to integrity monitoring. arXiv:2607.19129
69. Malmi J, Rossi MAC, García-Pérez G, Maniscalco S. Spatial search by continuous-time quantum walks on renormalized Internet networks. Phys Rev Research. 2022;4:043185. arXiv:2205.02137
70. Childs AM, Gosset D, Webb Z. Universal computation by multiparticle quantum walk. Science. 2013;339:791. doi:10.1126/science.1229957
71. Childs AM, Gosset D, Webb Z. The Bose-Hubbard model is QMA-complete. In: ICALP 2014. doi:10.1007/978-3-662-43948-7_26. arXiv:1311.3297
72. Agliari E, Blumen A, Mülken O. Dynamics of continuous-time quantum walks in restricted geometries. J Phys A. 2008;41:445301. arXiv:0810.1184
73. Adithya LJ, Hegde SS, Meena C. Postselection induced localization and coherence in quantum walks on heterogeneous networks. arXiv:2603.17629
74. Ide Y, Konno N. Continuous-time quantum walks on the threshold network model. Math Struct Comput Sci. 2010;20:1079–1090. arXiv:1003.0055
75. Anishchenko A, Blumen A, Mülken O. Geometrical aspects of quantum walks on random two-dimensional structures. Phys Rev E. 2013;88:062126. arXiv:1309.2827
76. Tsomokos DI. Quantum walks on complex networks with connection instabilities and community structure. Phys Rev A. 2011;83:052315. arXiv:1012.2405
77. Mülken O, Blumen A. Continuous-time quantum walks: models for coherent transport on complex networks. Phys Rep. 2011;502:37. doi:10.1016/j.physrep.2011.01.002
78. Duda M, Ivaki MN, Sahlberg I, Pöyhönen K, Ojanen T. Quantum walks on random lattices: diffusion, localization, and the absence of parametric quantum speedup. Phys Rev Research. 2023;5:023150. arXiv:2210.05310
79. Razzoli L, Paris MGA, Bordone P. Transport efficiency of continuous-time quantum walks on graphs. Entropy. 2021;23:85. doi:10.3390/e23010085. arXiv:2011.13794
</content>

</invoke>
