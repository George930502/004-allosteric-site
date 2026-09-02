# Near-term hardware viability: encodings, circuit cost, noise, and the two provided platforms

**Scope:** what it costs to run a Hamiltonian on a residue graph — qubit encoding, gate count,
depth, connectivity, noise, shots, and what AWS Braket and Classiq actually give us. It
deliberately excludes **which observable to read out** and **why that observable is a proxy for
allostery**, and it excludes the **theory of coarse-graining** and any proof that compression
retains topological signal.
**Sibling files:** `03` (choice of observable), `07` (coarse-graining theory and validation),
`06-signal-propagation-physics.md` (the physics the Hamiltonian is meant to encode),
`01-classical-baselines.md` (what the classical bar is).
**Retrieved:** 2026-08-25.

---

## 0. The one-paragraph answer

Put the walker in the **single-excitation sector** and encode it **one qubit per residue**. Then
`exp(-iHt)` restricted to that sector is an N x N unitary, and an exact Givens-rotation network
implements it in **N(N-1)/2 two-qubit gates at depth N on a line** — no Trotter error, no SWAP
overhead, no all-to-all requirement. The `ceil(log2 N)`-qubit compression is real in qubit count
and, for an _arbitrary_ contact graph, catastrophic in gate count: 9 qubits for N = 300, but
~125,000 CNOTs against a proven generic lower bound of 65,529. The binding constraint is not qubit
count, it is **two-qubit fidelity**. At the 99.5 % median two-qubit fidelity Braket's best devices
deliver, the coherent gate budget is ~200 two-qubit gates, and `N(N-1)/2 <= 200` gives **N ~ 20**.
Not 169, not 108 — twenty. Two independent hardware results land in the same place: the largest
published quantum walk on a complex graph ran at **17 nodes**, and the only published CTQW
residue-centrality hardware run used a **9-residue** peptide. So the honest deliverable is a
**coarse-grained run of about twenty nodes** plus a full-N classical reference, and file 07 owns the
compression that gets us there.

---

## 1. What C3 and C4 actually demand of us

`CHALLENGE.md` §5 constraint 2: _"Proposals must demonstrate awareness of coherence time
limitations. Deep, unoptimized circuits that cannot run on near-term hardware will be penalized."_
Constraint 1: gate-based, quantum-inspired and hybrid are all allowed _"provided the proposal
demonstrates a credible path to execution on near-term or fault-tolerant quantum hardware"_.
§4.2 adds noise resilience — _"stability of the signal-propagation metric despite gate errors and
limited coherence times"_ — and scalability by coarse-graining, because _"many relevant protein
targets exceed the qubit capacity of current devices if mapped 1-to-1"_.

Read together, these say: **every quantum claim carries a resource line, and a resource line that
cannot run is a penalty rather than a neutral.** Section 9 is the template we fill for every method
the review recommends.

### 1.1 The graphs we are actually costing

Measured in this session from the frozen apo inputs, C-alpha contact graph at an 8 A cutoff
(`allo.inputs.apo_input`, no holo data touched). These are the real N and the real degree, and they
replace the "N = 300, degree 8" placeholder used in the brief:

| Arm                        |   N | \|E\| | mean degree | max degree | density D | greedy edge colours | max \|i-j\| |
| -------------------------- | --: | ----: | ----------: | ---------: | --------: | ------------------: | ----------: |
| `kras_g12c_mandated`       | 169 |   809 |        9.57 |         16 |    0.0570 |                  17 |         156 |
| `kras_g12c_corrected`      | 170 |   812 |        9.55 |         16 |    0.0565 |                   — |         156 |
| `bcr_abl1_corrected`       | 272 |  1263 |        9.29 |         15 |    0.0343 |                  16 |         163 |
| `bcr_abl1_mandated`        | 451 |  2099 |        9.31 |         15 |    0.0207 |                  16 |         362 |
| `cardiac_myosin_corrected` | 764 |  3589 |        9.40 |         16 |    0.0123 |                  16 |         645 |

Two numbers in that table do real work later. **Mean degree is ~9.4 and maximum degree is 15-16 at
every size** — the graph gets sparser, not denser, as the protein grows, and the _local_ structure
is size-independent. And the **greedy edge colouring is 16-17 layers at every size**, so one layer
of commuting two-qubit gates over the whole contact graph is ~17 parallel gate layers given
all-to-all connectivity, independent of N. That is the cheapest depth any edge-local scheme can
have. `[measured in this session; not a registered experiment]`

---

## 2. Encodings

This is the highest-leverage section, because the encoding fixes qubit count, gate count and
connectivity requirement before any algorithm choice is made.

### 2.1 One qubit per residue, in the single-excitation sector

Under C6 the propagating object is a single excitation hopping on the contact graph. The natural
qubit Hamiltonian is the XY (hard-core boson) model

```
H = sum_{(i,j) in E} J_ij (X_i X_j + Y_i Y_j) / 2
```

which **conserves excitation number**. Start in `|0...010...0>` — one excitation on the source
residue — and the state never leaves the N-dimensional single-excitation subspace. Residue identity
is the qubit index, which satisfies the repository's author-numbering convention for free.

The naive reading is "N qubits is wasteful, we are using N of 2^N basis states". The correct reading
is that **the wasted Hilbert space buys an exact, shallow, linearly-connected circuit**:

- Restricted to the single-excitation sector, `exp(-iHt)` **is** an N x N unitary. Any N x N unitary
  decomposes exactly into `N(N-1)/2` two-mode (Givens / XY) rotations. Clements, Humphreys, Metcalf,
  Kolthammer, Walmsley, _Optica_ 3, 1460 (2016), doi:10.1364/OPTICA.3.001460, give the mesh that
  achieves this at **depth N**, and state it _"requires half the optical depth of the Reck design"_.
  `[VERIFIED-ABSTRACT]`
- The qubit version, with the connectivity statement we need, is Kivlichan, McClean, Wiebe, Gidney,
  Aspuru-Guzik, Chan, Babbush, _PRL_ 120, 110501 (2018), arXiv:1711.04789. Verbatim: _"we can
  simulate a Trotter step of the electronic structure Hamiltonian in exactly N depth and with N^2/2
  two-qubit entangling gates, and prepare arbitrary Slater determinants in at most N/2 depth, all
  assuming only a minimal, linearly connected architecture."_ The basis rotation is _"a sequence of
  exactly (N choose 2) rotations of the form R_pq(theta)"_. `[VERIFIED-FULLTEXT]`

The consequence for us: **connectivity stops being a cost.** The requirement is a Hamiltonian path
through the qubits used. A square lattice has one, and an all-to-all ion trap has one trivially, so
the Givens network runs with no routing overhead on IQM Garnet/Emerald and on IonQ or AQT. For
Rigetti's multi-chip lattices the path should be confirmed against the live coupling map before it is
asserted. `[UNVERIFIED for Rigetti; the requirement itself is VERIFIED-FULLTEXT from Kivlichan et
al.]`

Concrete cost, computed from `N(N-1)/2` and depth `N`:

|   N | qubits | two-qubit gates | depth | connectivity |
| --: | -----: | --------------: | ----: | ------------ |
| 150 |    150 |          11,175 |   150 | line         |
| 169 |    169 |          14,196 |   169 | line         |
| 272 |    272 |          36,856 |   272 | line         |
| 300 |    300 |          44,850 |   300 | line         |
| 764 |    764 |         291,466 |   764 | line         |
| 800 |    800 |         319,600 |   800 | line         |

Historical note, because it looks like prior art and is not: Geller et al., _"Universal quantum
simulation with prethreshold superconducting qubits: Single-excitation subspace method"_,
arXiv:1505.04990, use the n-dimensional single-excitation subspace of n coupled qubits as an
_analog_ computational resource. They describe it themselves as _"a nonscalable special case of the
standard gate-based quantum computing model"_ (arXiv:1210.5260). `[VERIFIED-ABSTRACT]` It is the same
subspace, not the same construction.

### 2.2 The compact / binary / Gray-code encoding

Index the N residues by a bitstring: `ceil(log2 N)` qubits. For N = 300 that is **9 qubits**, for
N = 800 it is 10. The literature on this is real and the space saving is real:

- Di Matteo, McCoy, Gysbers, Miyagi, Woloshyn, Navratil, _"Improving Hamiltonian encodings with the
  Gray code"_, _PRA_ 103, 042405 (2021), arXiv:2008.05012: Gray-code ordering yields
  _"circuits for the evolution operators with reduced depth and roughly half the number of gates
  compared to a one-hot encoding"_ — at fixed Hilbert-space dimension, i.e. for a _structured_
  Hamiltonian on a small number of qubits. `[VERIFIED-ABSTRACT]`
- Sawaya, Menke, Kyaw, Johri, Aspuru-Guzik, Guerreschi, _npj Quantum Information_ 6, 49 (2020),
  arXiv:1909.12847, study qudit-to-qubit encodings and _"observ[e] desirable properties for
  approaches based on the Gray code"_, driven by _"the interplay between Hamming distances, sparsity
  patterns, bosonic truncation, and other properties of local operators"_. `[VERIFIED-ABSTRACT]`
- Plesch, Friak, Mohammad, _"Efficient implementation of single particle Hamiltonians in
  exponentially reduced qubit space"_, **Quantum 10, 2099 (2026)**, arXiv:2601.00247. This is the
  closest published work to the question. Verbatim: _"a logarithmic-qubit encoding that maps a system
  with N physical sites onto only ceil(log2 N) qubits while maintaining a clear correspondence with
  the underlying physical model"_, with _"a Gray-code-inspired measurement strategy whose number of
  global settings grows only logarithmically with system size"_, reducing space-time-sampling volume
  _"from N^2 to (logN)^3 for hardware efficient ansatz"_. `[VERIFIED-ABSTRACT]`

**Two caveats decide whether this is usable here, and both are stated by the authors.** First,
Plesch et al. is a **variational** construction with a hardware-efficient ansatz, not a circuit for
`exp(-iHt)`; the `(logN)^3` volume is the cost of a VQE loop, not of time evolution. Second, its
scope is _"structured solid-state Hamiltonians"_ — a lattice with translational symmetry. A residue
contact graph has neither symmetry nor a closed-form rule for its entries.

### 2.3 Question (a): what the log2 compression actually costs

**If the graph is arbitrary, the compression trades an exponential in space for an exponential in
time, and the exchange rate is bad.**

The mechanism is not subtle. On `n = ceil(log2 N)` qubits, `exp(-iHt)` is a generic element of
SU(2^n) — nothing in a protein contact graph makes it special. Generic unitary synthesis has known
tight bounds. Shende, Bullock, Markov, _"Synthesis of Quantum Logic Circuits"_, _IEEE TCAD_ 25(6),
1000-1010 (2006), arXiv:quant-ph/0406176, verbatim: _"An arbitrary n-qubit operator can be
implemented in a circuit containing no more than (23/48) x 4^n - (3/2) x 2^n + 4/3 CNOT gates"_, and
_"n-qubit operators generically require ceil[(1/4)(4^n - 3n - 1)] CNOTs"_. `[VERIFIED-FULLTEXT]`
The same paper notes _"restricting CNOT gates to nearest-neighbor interactions increases CNOT count
by at most a factor of nine."_ `[VERIFIED-FULLTEXT]`

Instantiated:

|   N | qubits `ceil(log2 N)` | QSD upper bound (CNOTs) | generic lower bound (CNOTs) |
| --: | --------------------: | ----------------------: | --------------------------: |
| 150 |                     8 |                  31,020 |                      16,378 |
| 300 |                     9 |                 124,844 |                      65,529 |
| 800 |                    10 |                 500,908 |                     262,137 |

Compare to the one-hot Givens network at the same N: 11,175 / 44,850 / 319,600 two-qubit gates. **The
compressed encoding is worse in gate count at every size**, and the lower bound says no cleverer
compiler fixes it. You save 291 qubits at N = 300 and pay 2.8x the two-qubit gates, on 9 qubits that
must all survive every one of them.

There is exactly one escape, and it is conditional. Jordan and Wocjan, _"Efficient quantum circuits
for arbitrary sparse unitaries"_, arXiv:0904.2211, show _"quantum circuits can efficiently implement
any unitary provided it has at most polynomially many nonzero entries in any row or column, **and
these entries are efficiently computable**"_ `[VERIFIED-ABSTRACT]` (emphasis ours). Our matrix is
sparse — degree 15-16 — but its entries are not computable from a formula; they are `O(N * d)` bits
of geometry read off a PDB file. Aaronson, _"Read the fine print"_, _Nature Physics_ 11, 291 (2015),
states the same barrier for the whole family: _"If the matrix A is sparse ... and if there's a
quantum RAM that conveniently stores, for each i, the locations and values of row i's nonzero
entries — then it's known that one can apply e^{-iAt} in an amount of time that grows nearly
linearly with s"_, and _"With each of them, one faces the problem of how to load a large amount of
classical data into a quantum computer (or else compute the data 'on-the-fly'), in a way that is
efficient enough to preserve the quantum speedup."_ `[VERIFIED-FULLTEXT]` He makes the condition
explicit for the closest analogue to our problem: an electrical-network algorithm gives an
exponential speedup _"only under special conditions: for example, that the electrical network has
small degree but a large amount of interconnectivity (technically, 'large expansion'); and that a
description of the electrical network can be quickly loaded into the quantum computer (for example,
because the network has a regular pattern)."_ `[VERIFIED-FULLTEXT]` A protein has no regular pattern.

**Is anyone doing exactly this?** The closest published hardware experiment goes the _opposite_ way
and says so. Dubovitskii, Filippov et al. (Algorithmiq + IBM Quantum), _"Experimental implementation
of a discrete-time quantum walk on biological networks"_, arXiv:2602.24053 (27 Feb 2026):

> _"Conventional dense encodings of graph structures require prohibitively deep circuits, making
> them incompatible with existing hardware. Here we introduce an algorithm that leverages
> symmetry-sector encoding and trades circuit depth for qubits, while integrating
> symmetry-respecting postselection as an effective noise-mitigation strategy."_ `[VERIFIED-FULLTEXT]`

Their measured comparison is the number this question wanted. Against the
`ceil(log2 N) + ceil(log2 |E|)` dense encoding: _"a 6-qubit implementation of a single DTQW step on
an 8-node, 8-edge graph with maximum degree 3 already decomposes into a circuit containing 1,218
entangling layers ... When the constraints of heavy-hex qubit connectivity are taken into account,
the number of entangling layers increases further, reaching 2,882."_ Their sector encoding instead
_"requires only 11 entangling layers in QPU with all-to-all connectivity and 28 entangling layers
under the heavy-hex connectivity, reducing the circuit depth by two orders of magnitude compared to
the aforementioned design."_ `[VERIFIED-FULLTEXT]` They also state the scaling rule that matches our
measured degree table: _"This reduction stems from the scaling properties of our method, in which
circuit depth grows primarily with the maximum node degree."_

Their encoding uses `2|E|` qubits (one per directed edge) because a _discrete_-time walk needs a coin
degree of freedom. For a **continuous**-time walk we need only `N`, which for our graphs is a further
9.5x saving: `2|E| = 1,618` versus `N = 169` on KRAS.

**Answer to (a), stated plainly.** The compression to `ceil(log2 N) = 9` qubits for N = 300 exists,
is published, and does not help us. It costs roughly 125,000 CNOTs against 44,850 for the
uncompressed exact circuit, with a proven generic lower bound of 65,529 that no compiler beats. It
becomes attractive only for a Hamiltonian whose entries follow a rule — a lattice, a circulant graph
(Loke and Wang, _"Efficient Quantum Walk on a Quantum Processor"_, arXiv:1510.08657, give explicit
efficient CTQW circuits _"on the circulant class of graphs"_ `[VERIFIED-ABSTRACT]`), or a
coarse-grained network we design to have that structure. **That last clause is the one live route,
and it belongs to file 07.**

### 2.4 Jordan-Wigner and Bravyi-Kitaev: a cost we should decline to pay

Both mappings exist to enforce **fermionic antisymmetry**. Nothing in the elastic-network hypothesis
makes the propagating excitation a fermion: residues are distinguishable sites, and C6 says only that
contact topology drives propagation. Modelled as a hard-core boson or spin excitation, the XY
Hamiltonian in §2.1 needs no string operator at all.

The cost of choosing otherwise is measurable on our own graphs. Under Jordan-Wigner with sequence
ordering, a hop between residues i and j carries a Z-string of length `|i - j|`. We measured the
sequence-separation distribution: **60-66% of contacts have |i-j| <= 4**, but the tail runs to
`|i-j| = 156` (KRAS), `362` (BCR-ABL1 `1OPL`) and `645` (myosin `9GZ3`). `[measured in this session]`
So a third of all edges carry a string, and the longest is nearly the whole chain — the tertiary
contacts, which are exactly the long-range couplings an allosteric-propagation model exists to
capture. Havlicek, Troyer, Whitfield, _"Operator Locality in Quantum Simulation of Fermionic
Models"_, _PRA_ 95, 032332 (2017), arXiv:1701.07072, state the general form: _"The simplest method
for this task, the Jordan-Wigner transformation, yields strings of Pauli operators acting on an
extensive number of qubits"_, and that _"a variant of the Bravyi-Kitaev transform provides the most
compact fermion-to-qubit mapping for Hubbard-like models"_. `[VERIFIED-ABSTRACT]`

**Recommendation: do not use JW or BK.** If a reviewer asks why the fermionic machinery is absent,
the answer is C6 plus the string cost above, not an oversight.

### 2.5 Bosonic, continuous-variable and photonic encodings

An elastic network model _is_ a set of coupled harmonic oscillators, so the strongest published
result in this whole file lives here.

Babbush, Berry, Kothari, Somma, Wiebe, _"Exponential quantum speedup in simulating coupled classical
oscillators"_, **PRX 13, 041041 (2023)**, arXiv:2303.13012:

> _"We present a quantum algorithm for simulating the classical dynamics of 2^n coupled oscillators
> (e.g., 2^n masses coupled by springs). Our approach leverages a mapping between the Schrodinger
> equation and Newton's equation for harmonic potentials such that the amplitudes of the evolved
> quantum state encode the momenta and displacements of the classical oscillators. When individual
> masses and spring constants can be efficiently queried, and when the initial state can be
> efficiently prepared, the complexity of our quantum algorithm is polynomial in n, almost linear in
> the evolution time, and sublinear in the sparsity."_ `[VERIFIED-ABSTRACT]`

The encoding is exactly the ENM one: `y = sqrt(M) x` turns `M x'' = -F x` into `y'' = -A y` with
`A = sqrt(M)^-1 F sqrt(M)^-1`, and the Hamiltonian is built from `B` with `B B^dagger = A` — `B` is
literally the square root of the mass-weighted Hessian. `2^n` oscillators need about
`2n + O(log(1/eps))` qubits. Theorem 1: `Q = O(tau + log(1/eps))` queries and
`G = O(Q log^2(N tau eps^-1 m_max/m_min))` two-qubit gates. Theorem 3: the decision version of
estimating a single oscillator's kinetic energy is **BQP-complete**. `[VERIFIED-FULLTEXT]`

And then the caveat that decides our case, verbatim from the same paper:

> _"Any algorithm that outputs the full vectors x(t) or x'(t) would necessarily have complexity at
> least linear in N."_ / _"Extracting the full configuration of the classical system would scale
> polynomially in the Hilbert space dimension, precluding a large quantum speedup."_
> `[VERIFIED-FULLTEXT]`

**Our first mandated deliverable is an N x N connectivity matrix — the full configuration.** The
exponential speedup is available only for a _subset energy_ readout, and `CHALLENGE.md` §5 asks for
the matrix. The speedup and the deliverable are, as written, incompatible.

The direct protein follow-up exists and reaches the same place: Liu, Li, Wang, Liu, _"Toward
end-to-end quantum simulation for protein dynamics"_, arXiv:2411.03972, simulate _"normal mode
models — such as Gaussian network models (GNM) and all-atom normal mode models"_ `[VERIFIED-ABSTRACT]`
using `n = O(log N)` qubits, and state that the stiffness matrix _"is incompressibly determined by
the coordinates"_, requiring `O(N)` bits to load, so that _"to achieve a full overall quantum
advantage, significant challenges remain."_ `[VERIFIED-FULLTEXT]`

**Qumode / photonic.** Gaussian boson sampling is the only platform in this review with a
zero-overhead encoding of an _arbitrary_ adjacency matrix. Bromley, Arrazola et al., _Quantum Sci.
Technol._ 5, 034010 (2020), arXiv:1912.07634: the adjacency matrix is Takagi-decomposed as
`A = U diag(lambda) U^T`, `U` programs the interferometer, squeezing is set by
`tanh(r_i) = c lambda_i` with `c < 1/lambda_max`, and _"An N-node graph requires exactly N optical
modes in the GBS device, with one mode per node."_ `[VERIFIED-FULLTEXT]` The sampled quantity is a
hafnian — Arrazola and Bromley, _PRL_ 121, 030503 (2018), doi:10.1103/PhysRevLett.121.030503:
_"a link between graph density and the number of perfect matchings — enumerated by the Hafnian —
which is the relevant quantity determining sampling probabilities in GBS."_ `[VERIFIED-ABSTRACT]`
That is a subgraph-density statistic, **not a propagator**, so it answers a different question than
"dynamic connectivity to the active site". And no photonic device is on Braket (§7.1).

### 2.6 Encoding summary at N = 300

| Encoding                           |           Qubits |        Two-qubit gates for `exp(-iHt)` |                      Depth | Connectivity                          | Verdict                                                           |
| ---------------------------------- | ---------------: | -------------------------------------: | -------------------------: | ------------------------------------- | ----------------------------------------------------------------- |
| One-hot, exact Givens network      |              300 |                                 44,850 |                        300 | line                                  | cheapest exact circuit; exceeds every Braket device's qubit count |
| One-hot, Trotter over edge colours |              300 |             809-3589 per step, r steps |                17 per step | all-to-all (or line via swap network) | dominated by Givens (§3.6)                                        |
| Directed-edge sector (Dubovitskii) |   2\|E\| ~ 2,800 |                       unknown for CTQW | ~11 layers/step all-to-all | any                                   | published on hardware, but for a DTQW and at 17 nodes             |
| Binary / Gray code                 |                9 |           124,844 (65,529 lower bound) |                ~same order | any (x9 on a line)                    | infeasible for an arbitrary graph                                 |
| Binary + sparse-oracle             |     9 + ancillas | unknown; oracle costs O(N d) per query |                    unknown | any                                   | data loading destroys the saving (§2.3)                           |
| Coupled-oscillator (Babbush)       | ~2 log2 N + anc. |      `O((tau + log 1/eps) log^2(...))` |                    unknown | any                                   | exponential speedup, but not for a full N x N readout             |
| GBS qumodes                        |        300 modes |                           n/a (analog) |                        n/a | n/a                                   | wrong observable; no device on Braket                             |
| Jordan-Wigner fermionic            |              300 |     44,850 x (string factor up to 645) |                      worse | line                                  | declined; C6 gives no reason to pay it                            |

---

## 3. Hamiltonian simulation cost

### 3.1 Trotter-Suzuki

Childs, Su, Tran, Wiebe, Zhu, _"Theory of Trotter Error with Commutator Scaling"_, **PRX 11, 011020
(2021)**, arXiv:1912.08854, is the current bound. Verbatim: their analysis _"directly exploits the
commutativity of operator summands, producing tighter error bounds"_, and they report that the
_"higher-order bound overestimates the complexity of simulating a one-dimensional Heisenberg model by
only a factor of 5."_ `[VERIFIED-ABSTRACT]` For our Hamiltonian the summands are the edge-colour
classes of §1.1; within a class the terms are disjoint and commute exactly, so the error is carried
entirely by the ~17 inter-class commutators.

### 3.2 Measured: how many Trotter steps a stable top-5 needs

The asymptotics do not tell us `r`. We measured it. First-order Trotter over the greedy edge-colour
classes, `t = 5/J`, score = mean transfer probability from the active-site source residues, compared
against the exact spectral propagator on the same graph:

| Arm                                |   r | 2q gates | 2q depth | top-5 overlap vs exact | Kendall tau |
| ---------------------------------- | --: | -------: | -------: | ---------------------- | ----------: |
| `kras_g12c_mandated` (N=169)       |  16 |   12,944 |      272 | 1/5                    |      +0.421 |
|                                    |  64 |   51,776 |    1,088 | 3/5                    |      +0.768 |
|                                    | 128 |  103,552 |    2,176 | 4/5                    |      +0.889 |
|                                    | 256 |  207,104 |    4,352 | 5/5                    |      +0.947 |
| `bcr_abl1_corrected` (N=272)       |  32 |   40,416 |      512 | 2/5                    |      +0.554 |
|                                    |  64 |   80,832 |    1,024 | 5/5                    |      +0.729 |
| `cardiac_myosin_corrected` (N=764) |  64 |  229,696 |    1,024 | 2/5                    |      +0.880 |
|                                    | 256 |  918,784 |    4,096 | 4/5                    |      +0.964 |

`[measured in this session; not a registered experiment]`

Two things to take from this. **Kendall tau is a misleading gate.** At `r = 64` on myosin the global
rank correlation is already +0.88 while only 2 of the top 5 are right; the top of the list converges
much later than the bulk. **And the resource cost is fatal.** A top-5 that matches the exact
propagator needs `r` in the low hundreds, i.e. **10^5 to 10^6 two-qubit gates and 2,000-4,400 layers
of two-qubit depth.** Rigetti's Ankaa-3 rejects any circuit above 20,000 gates outright (§7.1). This
is precisely the _"deep, unoptimized circuit"_ C3 penalises.

### 3.3 Randomised compiling and qDRIFT

Campbell, _"A random compiler for fast Hamiltonian simulation"_, **PRL 123, 070503 (2019)**,
arXiv:1811.08017: circuit size depends on `lambda` (the L1 norm of the Hamiltonian coefficients),
`t` and `eps`, and is _"independent of L"_, the number of terms. `[VERIFIED-ABSTRACT]`

That independence is the wrong lever for us. Our `L = |E|` is 809-3589, but `lambda = sum |J_ij| =
|E| * J`, and qDRIFT's gate count scales as `lambda^2 t^2 / eps`. Trading `L` for `lambda^2` on a
graph where `lambda` grows _with_ `L` is not a trade. Later work confirms the direction rather than
reversing it: qFLO (arXiv:2411.04240) reduces depth to `O(T^2 log(1/eps))`, still quadratic in time.
`[VERIFIED-ABSTRACT]`

### 3.4 LCU, qubitisation and quantum signal processing

- Childs and Wiebe, _"Hamiltonian Simulation Using Linear Combinations of Unitary Operations"_,
  _QIC_ 12, 901-924 (2012), arXiv:1202.5822 — the LCU primitive; _"scales better with the simulation
  error than any known Hamiltonian simulation technique"_ at the time. `[VERIFIED-ABSTRACT]`
- Low and Chuang, _"Hamiltonian Simulation by Qubitization"_, **Quantum 3, 163 (2019)**,
  arXiv:1610.06546 — query complexity _"O(t + log(1/eps)) to both oracles"_, described as
  _"optimal for all parameters"_, using _"at most two additional ancilla qubits"_. `[VERIFIED-ABSTRACT]`
- Berry, Childs, Cleve, Kothari, _"Exponential improvement in precision for simulating sparse
  Hamiltonians"_, arXiv:1312.1414 — a d-sparse H on n qubits simulated to precision eps with
  _"O(tau log(tau/eps)/log log(tau/eps)) queries and O(tau log^2(tau/eps)/log log(tau/eps) n)
  additional 2-qubit gates, where tau = d^2 ||H||\_max t"_. `[VERIFIED-ABSTRACT]`
  Berry, Childs, Kothari, FOCS 2015, doi:10.1109/FOCS.2015.54, achieve complexity _"optimal (up to
  log factors) as a function of all parameters of interest"_. `[VERIFIED-ABSTRACT]`

All four are **oracle** results. The oracle for our Hamiltonian is a lookup of the contact graph, and
building it costs `O(N d)` gates for an arbitrary graph — the §2.3 barrier again. Query optimality is
not gate optimality when the query itself is the expensive object.

### 3.5 The graph Laplacian or adjacency Hamiltonian specifically

Two results bound what can ever be gained.

Childs and Kothari, _"Limitations on the simulation of non-sparse Hamiltonians"_, arXiv:0908.4398:
_"The evolution of a sparse N x N Hamiltonian H for time t can be simulated using O(||Ht|| poly(log
N)) operations, which is essentially optimal due to a no-fast-forwarding theorem."_ They generalise
it, _"ruling out generic simulations taking time o(||Ht||)"_. `[VERIFIED-ABSTRACT]` So the runtime is
linear in `||H|| t` no matter what — you cannot jump to `t = infinity` to get a time-averaged
observable cheaply.

And the classical side is not hard. `exp(-iHt)` on an `N x N` symmetric matrix is one `eigh` call.
Section 10 gives the measured wall-clock.

### 3.6 Trotter is dominated here, and that is a finding

Put §2.1 and §3.2 side by side at N = 272:

| Method               | two-qubit gates | two-qubit depth | error                 |
| -------------------- | --------------: | --------------: | --------------------- |
| Exact Givens network |          36,856 |             272 | **zero**              |
| Trotter, r = 64      |          80,832 |           1,024 | 5/5 top-5, tau = 0.73 |
| Trotter, r = 256     |         323,328 |           4,096 | tau = 0.93            |

The exact circuit is **2.2x cheaper in gates, 3.8x shallower, and has no Trotter error at all.**
Trotterisation is the standard move for a many-body Hamiltonian precisely because the exact unitary
is not efficiently synthesisable; in the single-excitation sector it is. **Any method in this project
that Trotterises a single-particle graph Hamiltonian should justify why it is not using the Givens
network instead.** `[UNVERIFIED — this comparison is ours; the two ingredients are separately
sourced above]`

---

## 4. Circuit compilation and connectivity

### 4.1 What the provided platform actually offers

There is no heavy-hex device on Amazon Braket. The current provider list is **AQT, IonQ, IQM, QuEra
and Rigetti** (§7.1) — trapped-ion all-to-all, superconducting square lattice, and a neutral-atom
analog machine. IBM is not a Braket provider, so heavy-hex routing is an off-platform comparison for
us. It is worth costing anyway, because the one published hardware experiment on biological-network
quantum walks ran on heavy-hex.

### 4.2 SWAP overhead, with published formulas instantiated on our graphs

Weidenfeller, Clark, Johnson, Bishop, Rossi, Pistoia, _"Scaling of the quantum approximate
optimization algorithm on superconducting qubit based hardware"_, **Quantum 6, 870 (2022)**,
arXiv:2202.03459, gives closed-form swap-network costs for one layer of commuting two-qubit gates at
graph density `D` on `n` qubits (their Table 1, verbatim structure): `[VERIFIED-FULLTEXT]`

| Coupling map | swap layers `L_S` | CNOT layers `L_cx`   | total CNOTs                   | avg CNOTs/layer |
| ------------ | ----------------- | -------------------- | ----------------------------- | --------------- |
| Line         | `Dn`              | `3 L_S = 3Dn`        | `(3/2) n L_S = (3/2) D n^2`   | `n/2`           |
| 2D grid      | `(1/2) Dn`        | `7 L_S = (7/2) Dn`   | `(7/2) n L_S = (7/4) D n^2`   | `n/2`           |
| 3D grid      | `(1/4) Dn`        | `11 L_S = (11/4) Dn` | `(11/2) n L_S = (11/8) D n^2` | `11n/32`        |
| Heavy-hex    | `Dn`              | `9 L_S = 9Dn`        | `(8/5) n L_S = (8/5) D n^2`   | `8n/45`         |

They also state the depth ceiling under depolarising noise: _"the maximum depth of a QAOA circuit
with a fraction f1 of single-qubit gate layers and a fraction f2 of two-qubit gate layers with
depolarizing noise with probability p1 and p2 ... is bounded by L_max ~ ln(eps^-1) / (2(f1 p1 + f2
p2))"_, and assume _"CNOT gates lasting 400 ns"_. `[VERIFIED-FULLTEXT]`

Instantiated at our measured densities, for **one** layer of commuting gates over the contact graph:

| Arm                        |   N |      D | Line                   | 2D grid     | Heavy-hex   |
| -------------------------- | --: | -----: | ---------------------- | ----------- | ----------- |
| `kras_g12c_mandated`       | 169 | 0.0570 | 29 layers / 2,442 CNOT | 34 / 2,849  | 87 / 2,605  |
| `bcr_abl1_corrected`       | 272 | 0.0343 | 28 / 3,806             | 33 / 4,441  | 84 / 4,060  |
| `bcr_abl1_mandated`        | 451 | 0.0207 | 28 / 6,316             | 33 / 7,368  | 84 / 6,737  |
| `cardiac_myosin_corrected` | 764 | 0.0123 | 28 / 10,769            | 33 / 12,564 | 85 / 11,487 |

`[derived from the published formulas above and our measured D; arithmetic is ours]`

**Heavy-hex costs about 3x the two-qubit depth of a line for the same problem, at similar total gate
count.** The independent hardware measurement agrees on the magnitude: Dubovitskii et al. report
_"only 11 entangling layers in QPU with all-to-all connectivity and 28 entangling layers under the
heavy-hex connectivity"_ per DTQW step — a 2.5x penalty. `[VERIFIED-FULLTEXT]`

For an arbitrary-unitary circuit rather than a graph-local one, Shende et al.'s bound is the answer:
nearest-neighbour restriction costs _"at most a factor of nine"_ in CNOT count. `[VERIFIED-FULLTEXT]`

### 4.3 The Givens network needs only a line — so pay none of this

The routing analysis above applies to schemes that emit one gate per graph edge. The exact Givens
network does not: the swap network **is** the algorithm, and Kivlichan et al. already state its
depth-N cost _"assuming only a minimal, linearly connected architecture."_ On a line, on a square
lattice, or on an ion trap, the number is the same. This is the single strongest engineering argument
for the one-hot encoding and it should appear in the report.

---

## 5. Noise, and whether a ranking survives it

### 5.1 The structural fact: global depolarising noise cannot reorder a ranking

Under a global depolarising channel with parameter `lambda`, measured probabilities transform as
`p_i -> lambda p_i + (1 - lambda)/2^n`. That map is **affine and strictly increasing in `p_i`**, so it
preserves the order of `p_1, ..., p_N` **exactly**. Depolarising noise cannot, by itself, change a
top-5 list. It only compresses the gaps between scores by `lambda`, which means the _shot_ budget
needed to resolve those gaps grows as `1/lambda^2`.

We checked the scaling directly. KRAS (N = 169), exact propagator, global depolarising applied to the
score vector, then binomial sampling; the criterion is `P(top-5 overlap >= 4/5) >= 0.9`:

| `lambda` | shots `M` needed | `1/lambda^2` |
| -------: | ---------------: | -----------: |
|     1.00 |              1e4 |            1 |
|     0.50 |              1e4 |            4 |
|     0.20 |              1e5 |           25 |
|     0.10 |              1e5 |          100 |
|     0.05 |              1e6 |          400 |
|     0.02 |              1e7 |        2,500 |

`[measured in this session; not a registered experiment]` The observed budget tracks `1/lambda^2`
within the resolution of the decade grid.

**This is the honest framing of noise resilience for a ranking deliverable, and it is stronger than
"the metric is robust".** The failure mode is not rank inversion by decoherence; it is _loss of
resolution_, converted into an exponentially growing shot bill.

### 5.2 The depth at which the signal is lost

With two-qubit error `p` and `G` two-qubit gates, `lambda ~ (1 - p)^G`. For the exact Givens network
`G = N(N-1)/2`:

|   N |       G | p = 2e-3 | p = 1e-3 | p = 1e-4 | p = 1e-5 | p = 1e-6 |
| --: | ------: | -------: | -------: | -------: | -------: | -------: |
| 150 |  11,175 |  1.9e-10 |   1.4e-5 |    0.327 |    0.894 |    0.989 |
| 169 |  14,196 |  4.5e-13 |   6.8e-7 |    0.242 |    0.868 |    0.986 |
| 272 |  36,856 |  9.0e-33 |  9.7e-17 |    0.025 |    0.692 |    0.964 |
| 300 |  44,850 |  1.0e-39 |  3.3e-20 |    0.011 |    0.639 |    0.956 |
| 764 | 291,466 | 3.8e-254 | 2.3e-127 |  2.2e-13 |    0.054 |    0.747 |

The usable-signal condition is `G p <~ 1`:

|   N | required two-qubit error | required two-qubit fidelity |
| --: | -----------------------: | --------------------------- |
| 150 |                   8.9e-5 | 99.9910 %                   |
| 169 |                   7.0e-5 | 99.9930 %                   |
| 272 |                   2.7e-5 | 99.9973 %                   |
| 300 |                   2.2e-5 | 99.9978 %                   |
| 764 |                   3.4e-6 | 99.99966 %                  |

`[arithmetic ours, from the published gate count in §2.1]`

The rule `depth budget ~ 1/error` is not our invention. Cross, Bishop, Sheldon, Nation, Gambetta,
_PRA_ 100, 032328 (2019), arXiv:1811.12926, define quantum volume through exactly this relation:
`m * d(m) ~ 1/eps_eff(m)` with `eps_eff(m) = (a sqrt(m) + b) eps` and `eps` the two-qubit gate error.
`[VERIFIED-FULLTEXT]` The product form is the one measured on hardware: Arute et al., _Nature_ 574,
505 (2019), give circuit polarisation as a product over gates,
`p = prod_i [1 - e_p(i)/(1 - 1/D^2)]`. `[VERIFIED-FULLTEXT]` At scale, IBM's layer-fidelity metric
makes the same point with numbers — McKay, Hincks, Pritchett, Carroll, Govia, Merkel,
arXiv:2311.05933: `LF = prod_m LF_m`, `EPLG = 1 - LF^(1/n_2q)`, and on a 100-qubit chain
`ibm_sherbrooke` (Eagle) reaches `LF = 0.19` and `ibm_montecarlo` (Heron) `LF = 0.26`.
`[VERIFIED-FULLTEXT]`

### 5.3 What this means on the devices we are actually given

Published two-qubit error rates for the Braket QPUs, and the two-qubit gate budget
`G* = 1/p` at which `lambda` falls to `1/e`:

| Device                        | 2Q error `p`   | source                                                   | `G*` | largest N with `N(N-1)/2 <= G*` |
| ----------------------------- | -------------- | -------------------------------------------------------- | ---: | ------------------------------: |
| IonQ Forte-1 / Forte-Ent.     | 4.0e-3 (99.6%) | ionq.com/quantum-systems/compare `[VERIFIED-FULLTEXT]`   |  250 |                          **22** |
| IQM Garnet (20q)              | 5.0e-3 (99.5%) | arXiv:2408.12433 `[VERIFIED-ABSTRACT]`                   |  200 |                          **20** |
| IQM Emerald (54q)             | 5.0e-3 (99.5%) | AWS launch blog, 21 Jul 2025 `[VERIFIED-FULLTEXT]`       |  200 |                          **20** |
| Rigetti Ankaa-3 (84q), fSim   | 5.0e-3 (99.5%) | Rigetti PR, 23 Dec 2024 `[VERIFIED-FULLTEXT, secondary]` |  200 |                          **20** |
| Rigetti Ankaa-3, iSWAP        | 1.0e-2 (99.0%) | same                                                     |  100 |                          **14** |
| Rigetti Cepheus-1-108Q        | 9.0e-3 (99.1%) | AWS launch blog, 7 Apr 2026 `[VERIFIED-FULLTEXT]`        |  111 |                          **15** |
| AQT IBEX-Q1                   | unknown        | AWS docs state no number                                 |    — |                               — |
| _(off-platform)_ IBM Heron R3 | 1.7e-3         | Dubovitskii et al. `[VERIFIED-FULLTEXT]`                 |  588 |                              34 |

`[G* and N columns are our arithmetic from the cited error rates]`

**This is the sharpest number in the file.** On the best gate-based device Braket offers, the exact
Givens network stays coherent up to about **N = 20-22 nodes**. Not 169. Not 300. Twenty.

Two independent lines of evidence land in the same place. Dubovitskii et al. ran the largest
published quantum walk on a complex graph on superconducting hardware at **17 nodes and 20 edges**,
using 40 qubits and 287 entangling layers. `[VERIFIED-FULLTEXT]` And Mohtashim, Sajjan, Kais
(arXiv:2604.17486), running a CTQW residue-centrality calculation on `ibm_kingston`, chose a
**9-residue** peptide (oxytocin, `1XY1`) on 4 qubits for the hardware arm, while their 150-protein
study is simulator-only. `[VERIFIED-FULLTEXT]`

**Everything downstream follows from this.** File 07 does not get to pick a coarse-graining ratio for
methodological reasons alone; the hardware fixes the target at a few tens of nodes. A 764-residue
myosin chain must compress by a factor of ~35 to run at all.

Also note what the table does to §2.3's conclusion. At `N = 20` the compressed encoding needs
`ceil(log2 20) = 5` qubits and, by Shende et al., up to `(23/48) 4^5 - (3/2) 2^5 + 4/3 = 444` CNOTs
against the Givens network's **190**. The compressed encoding is still worse, but only by ~2.3x
rather than 2.8x — and at the _very_ small sizes where hardware demonstrations actually happen
(n = 4, N <= 16), the two converge and the compressed route becomes defensible. That is precisely the
size Mohtashim et al. used. `[arithmetic ours]`

### 5.4 Question (d): what the literature says about ranking stability — and the gap

**The honest finding: there is no established literature on the rank-order stability of graph-node
scores under gate-level hardware noise.** Recording that as an absence, per ADR 0019, rather than as
a claim about what exists.

What the search did return:

- **The order-preservation statement, explicitly.** Micklitz, arXiv:2510.13026, writes the noisy
  output distribution as `p_k(f) = f p_k + (1-f)/D` and observes that _"Probabilities larger than the
  uniform value 1/D ... are compressed by f<1, while those smaller ... are inflated toward it"_, with
  _"each rank shift[ing] differently, yet in a manner fully determined by the single fidelity
  parameter f"_. `[VERIFIED-FULLTEXT]` This is §5.1 in published form.
- **The closest domain precedent, and it is our own problem.** Mohtashim, Sajjan, Kais,
  _"Continuous-time quantum-walk centrality for protein residue interaction networks"_,
  arXiv:2604.17486 (19 Apr 2026) — the paper `00-conventions.md` §5 already names as the published
  quantum result. Its hardware arm reports: _"Despite noise in the device runs, the highest-ranked
  residues remain consistent, demonstrating that CTQW-derived centralities are experimentally
  accessible on current noisy intermediate-scale quantum hardware"_, with _"only minor permutations
  among the upper-rank residues"_ attributed to _"finite-shot sampling and two-qubit gate
  infidelities"_. `[VERIFIED-FULLTEXT]` Against classical eigenvector centrality they report Spearman
  rho 0.582-1.000 (median ~0.964) and Kendall tau 0.491-1.000 (median ~0.867) over ~150 proteins.
  **But that agreement is simulator-versus-classical.** They report **no** Kendall tau between the
  simulator ranking and the hardware ranking, no noise model, and no error rate. The hardware
  demonstration is one 9-residue peptide at 1024 shots.
- **A ranking surviving noise in an adjacent task.** Yang, arXiv:2507.18425, on quantum ML for
  binding free energies: _"Although noise slightly reduces accuracy, the ranking of ligand affinities
  remains largely unchanged."_ `[VERIFIED-ABSTRACT]`
- **Quantum PageRank robustness is about the wrong parameter.** Paparo, Muller, Comellas,
  Martin-Delgado, _Sci. Rep._ 3, 2773 (2013): _"the quantum PageRank is very robust with respect to
  variation of the parameter that controls the fraction of random hopping. It is much more robust
  than in the classical case"_, with minimum fidelity 0.91 against a classical drop below 0.4.
  `[VERIFIED-FULLTEXT]` The only noise sentence in that paper is a conjecture, verbatim: _"the
  quantum PageRank algorithm is expected to be robust with respect to random external noise."_
  Ortega and Martin-Delgado, _PRR_ 5, 013061 (2023), repeat the analysis with arbitrary phase
  rotations and again measure stability against the damping parameter, not against a channel.
  `[VERIFIED-FULLTEXT]` Loke, Tang, Rodriguez, Small, Wang, _QIP_ 16, 25 (2017), arXiv:1511.04823 —
  the paper usually cited here — contains **no** noise or hardware analysis at all.
  `[VERIFIED-ABSTRACT]`
- **The counterexample to over-confidence.** Fontana, Fitzpatrick, Munoz Ramo, Duncan, Rungger,
  _PRA_ 104, 022403 (2021): parameter _"degeneracy can be lifted in the presence of noise, with some
  states being significantly more resilient to noise than others"_. `[VERIFIED-ABSTRACT]` Noise can
  decide which configuration wins when the noiseless scores are close.

**And the caveat that constrains our design.** §5.1's order preservation is exact only if every
residue score is read off **the same noisy state with the same `lambda`**. If residue `i`'s score came
from a circuit with `G_i` two-qubit gates and residue `j`'s from a circuit with `G_j != G_i`, then
`lambda_i != lambda_j`, the map is no longer a common affine rescaling, and rank inversions become
possible between residues whose true scores differ by less than the `lambda` mismatch. **The
single-circuit, computational-basis readout of §6.2 satisfies the condition; a per-residue
observable-by-observable scheme does not.** This is a constraint on how the propagation metric is
defined, not a reporting detail. `[UNVERIFIED — our analysis; the affine-map ingredient is sourced
above]`

Explicit negatives from the recorded search: an arXiv full-text query
`abs:"PageRank" AND abs:"decoherence"` returned **0** results; `abs:"Kendall" AND abs:"quantum
computer"` returned **0**; no paper reporting Kendall tau or top-k overlap between a noiseless and a
QPU node ranking as a function of shot count or error rate was retrieved; no top-k recovery guarantee
under shot noise for graph centrality was retrieved. **The measurements in §5.1 and §6.1 have no
direct competitor in the retrieved literature, and turning them into a registered experiment is a
cheap, defensible contribution that answers `CHALLENGE.md` §4.2's noise-resilience objective
directly.**

### 5.5 Error mitigation, and what each costs in shots

Overhead formulas from the field review — Cai, Babbush, Benjamin, Endo, Huggins, Li, McClean,
O'Brien, _"Quantum Error Mitigation"_, **Rev. Mod. Phys. 95, 045005 (2023)**, arXiv:2210.00921,
all `[VERIFIED-FULLTEXT]`:

| Technique                        | Sampling overhead `C_em`                                                                      | What it costs us                                                                                                                                                                      |
| -------------------------------- | --------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Zero-noise extrapolation         | `~ (sum \|prod (lambda_k/(lambda_k - lambda_m))\|)^2`; `~ (2^M - 1)^2` for M equal-gap points | 9x at M=2, 49x at M=3 — cheap, and it also multiplies circuit depth by the noise-scaling factor                                                                                       |
| Probabilistic error cancellation | `prod (1+p)^2/(1-p)^2 ~ e^(4 M p) = e^(4 lambda)`                                             | exponential in noise-weighted circuit volume; at `M p = 1` already `e^4 = 55x`, at `M p = 5` `e^20 = 4.9e8`                                                                           |
| Readout / measurement mitigation | _"increase exponentially with the measurement faults rate"_                                   | the one cheap layer in practice; Nation, Kang, Sundaresan, Gambetta, _PRX Quantum_ 2, 040326 (2021), give a matrix-free method that _"converges in O(1) steps"_ `[VERIFIED-ABSTRACT]` |
| Symmetry verification            | `~ Tr[Pi rho]^(-1)` direct, `Tr[Pi rho]^(-2)` post-processed                                  | exactly our postselection ratio (§5.6); free in gates, paid in retained shots                                                                                                         |

The same review states the general limit verbatim: _"QEM cannot efficiently tackle noisy circuits
with large lambda on its own due to the exponential sampling overhead"_. `[VERIFIED-FULLTEXT]`

The lower bounds make this a theorem rather than an engineering observation. Takagi, Tajima, Gu,
_"Universal sampling lower bounds for quantum error mitigation"_, **PRL 131, 210602 (2023)**,
arXiv:2208.09178: _"the sampling cost required for a wide class of protocols to mitigate errors must
grow exponentially with the circuit depth for various noise models"_, and for layered circuits under
local depolarising noise their Theorem 3 gives
`N >= (1-2 eps)^2 / [2 ln(2) M (1-gamma)^(2L)]` — sample count growing as `(1-gamma)^(-2L)`,
exponential in depth `L`. `[VERIFIED-FULLTEXT]` Quek, Franca, Khatri, Meyer, Eisert, _Nature Physics_
20, 1648 (2024), arXiv:2210.11505, sharpen it: _"even at shallow circuit depths comparable to the
current experiments, a superpolynomial number of samples is needed in the worst case"_, and
_"scrambling due to noise can kick in at exponentially smaller depths than previously thought"_.
`[VERIFIED-ABSTRACT]`

**Conclusion for our plan: mitigation does not buy back the factor of 8-38 in N implied by §5.3.**
It buys resolution at a size the device already reaches. Use readout mitigation (cheap), symmetry
verification (§5.6), and at most two-point ZNE. Do not budget for PEC.

### 5.6 Symmetry verification is nearly free here, and we should use it

Number conservation gives a **built-in error-detection code**. Any measured bitstring with Hamming
weight != 1 is a detected error. Dubovitskii et al. use exactly this: _"It is the postselection of
measurement bitstrings from the single-excitation subspace that serves as an effective noise filter
and substantially improves fidelity"_, taking Hellinger fidelity _"above 0.87"_ over 7 steps on
graphs up to 17 nodes and 40 qubits. `[VERIFIED-FULLTEXT]` The honest costs, also from that paper:
_"The fraction of bitstrings retained in the postselection procedure ... typically decays
exponentially with the circuit depth and number of qubits"_, and _"multiple bit-flip errors may
remain undetectable by postselection if the total number of excitation is preserved."_
`[VERIFIED-FULLTEXT]`

So symmetry verification converts a fidelity problem into a shot problem — the same conversion as
§5.1, and it composes with it.

---

## 6. Measurement cost

### 6.1 Shots needed to order residues

Measured on the exact propagator, noiseless, criterion `P(top-5 overlap >= 4/5) >= 0.9`, shots per
source column:

| Arm                        |   N | M = 1e2 |  1e3 |  1e4 |  1e5 |
| -------------------------- | --: | ------: | ---: | ---: | ---: |
| `kras_g12c_mandated`       | 169 |    0.10 | 0.84 | 1.00 | 1.00 |
| `bcr_abl1_corrected`       | 272 |    0.01 | 0.77 | 1.00 | 1.00 |
| `cardiac_myosin_corrected` | 764 |    0.00 | 0.07 | 0.67 | 0.99 |

`[measured in this session; not a registered experiment]`

**~1e4 shots per column at N <= 272, ~1e5 at N = 764**, noiseless. Multiply by `1/lambda^2` from §5.1
for a real device. The N-dependence is the expected one: probability mass spreads over more residues,
so the gaps to resolve shrink.

The analytic form agrees. For an observable in `[-1, 1]` the standard error is at most `1/sqrt(M)`,
so separating two scores that differ by `delta` at 2 sigma needs `M >= 8/delta^2`, and ordering _all_
pairs among N residues costs a union-bound factor of `~2 ln N`:

| `delta` | `M` for one pair | `M` for all pairs at N = 300 |
| ------: | ---------------: | ---------------------------: |
|    0.10 |              800 |                        9,126 |
|    0.05 |            3,200 |                       36,504 |
|    0.03 |            8,889 |                      101,401 |
|    0.01 |           80,000 |                      912,605 |

`[UNVERIFIED — our derivation; no paper stating it for this setting was retrieved]` The published
statement that measurement counts are the practical bottleneck is Wecker, Hastings, Troyer, _PRA_ 92,
042303 (2015) — _"the required number of measurements is astronomically large for quantum chemistry
applications"_ `[VERIFIED-ABSTRACT]` — and the modern resource analysis is Gonthier et al., _PRR_ 4,
033154 (2022), arXiv:2012.04001. `[VERIFIED-ABSTRACT]`

**One hard vendor ceiling to note now:** QuEra Aquila's `shotsRange` is `(1, 1000)`.
`[VERIFIED-FULLTEXT]` A 1e4-shot column is 10 Aquila tasks; a 1e5-shot column is 100. That is a
resource line, not a footnote.

### 6.2 The N x N matrix does **not** need N^2 experiments

`CHALLENGE.md` §5 asks for an `N x N` matrix whose entry `(i,j)` is the connectivity between residues
i and j. Under the one-hot encoding this costs **N circuits, not N^2**:

1. Prepare `|e_i>` (one X gate).
2. Run the fixed Givens network for `exp(-iHt)`.
3. Measure in the computational basis. Each shot returns a single index `j`; `M` shots estimate the
   whole column `|<j|U|e_i>|^2` for every `j` at once.

The matrix is symmetric (`H` is real symmetric, so `|U_ij| = |U_ji|`), so N columns suffice, and the
circuit is identical across columns — only the one-qubit input state changes. On Braket this is one
batched task set, and under Hybrid Jobs the same compiled circuit is reused (_"parametric
compilation"_, §7.1).

For the **ranking** deliverable alone, fewer still: only the active-site source columns are needed —
11 to 23 on our arms.

### 6.3 Amplitude estimation and classical shadows

Amplitude estimation gives a quadratic improvement in shots, `M -> sqrt(M)`, but requires coherent
repetitions of the circuit inside a Grover operator — multiplying `G` by the number of iterations and
therefore multiplying the §5.2 fidelity requirement by the same factor. **At `lambda = (1-p)^G`
already near zero, spending depth to save shots is the wrong direction.** Sampling is correct here.

Classical shadows (Huang, Kueng, Preskill, _Nature Physics_ 16, 1050 (2020),
doi:10.1038/s41567-020-0932-7, arXiv:2002.08953) predict `M` observables from _"order log M
measurements"_, and the sample bound is `N >= O(log M) max_i ||O_i||_shadow^2 / eps^2`. For random
Pauli measurements and k-local observables `||O_i||_shadow^2 <= 4^k ||O_i||_inf^2` — **exponential in
locality, independent of the number of qubits**. `[VERIFIED-FULLTEXT]` A per-residue occupation
`n_i = (I - Z_i)/2` is 1-local, so shadows would give the whole N-residue score vector at cost
`~4 log(N)/eps^2`.

That is genuinely attractive, and we should still not use it here: §6.2 already gets the whole matrix
in `N` circuits by direct computational-basis sampling, because our observables are all diagonal in
the measurement basis and one shot updates every one of them. Shadows earn their keep when the
observables do not commute. Ours do. **Record shadows as the right tool if the chosen observable in
file 03 turns out to be non-diagonal.**

---

## 7. The two provided platforms

### 7.1 AWS Braket

All from `docs.aws.amazon.com/braket` and `aws.amazon.com/braket/pricing`, retrieved 2026-08-25.
`[VERIFIED-FULLTEXT]`

**Devices.**

| Provider | Device                      | Paradigm              |    Qubits | Topology                       | Native gates                      | 2Q fidelity                    | Region     |
| -------- | --------------------------- | --------------------- | --------: | ------------------------------ | --------------------------------- | ------------------------------ | ---------- |
| AQT      | IBEX-Q1                     | gate                  |   unknown | all-to-all (Ca-40 ion crystal) | `prx`, `xx`, `rz`                 | unknown                        | eu-north-1 |
| IonQ     | Forte-1, Forte-Enterprise-1 | gate                  |    **36** | all-to-all (Yb-171 chain)      | `gpi`, `gpi2`, `zz`               | **99.6 %** (GST 99.43 %)       | us-east-1  |
| IQM      | Garnet                      | gate                  |    **20** | square (crystal) lattice       | `cz`, `prx`                       | **99.5 %**                     | eu-north-1 |
| IQM      | Emerald                     | gate                  |    **54** | square (crystal) lattice       | `cz`, `prx`                       | **99.5 %** (1Q 99.93 %)        | eu-north-1 |
| Rigetti  | Ankaa-3                     | gate                  |    **84** | multi-chip lattice             | `rx`(+-pi/2, +-pi), `rz`, `iswap` | **99.5 %** fSim / 99.0 % iSWAP | us-west-1  |
| Rigetti  | Cepheus-1-108Q              | gate                  |   **108** | 12 x 9-qubit chiplets, 3x4     | as Ankaa-3                        | **99.1 %** (1Q 99.9 %)         | us-west-1  |
| QuEra    | Aquila                      | **analog (AHS only)** | 256 atoms | 2D neutral-atom register       | n/a — Rydberg Hamiltonian         | not published                  | us-east-1  |

Qubit counts and gate sets from AWS docs; IonQ's 36 qubits and 99.6 % / 99.98 % from
`ionq.com/quantum-systems/compare`; IQM Garnet's 99.5 % from Abdurakhimov et al., arXiv:2408.12433;
IQM Emerald's 99.5 % / 99.93 % from the AWS launch blog of 21 Jul 2025; Rigetti Cepheus's 99.1 % and
chiplet layout from the AWS launch blog of 7 Apr 2026; Ankaa-3's figures from Rigetti's launch
release of 23 Dec 2024. `[VERIFIED-FULLTEXT except IQM Garnet, VERIFIED-ABSTRACT]` **AWS documents no
qubit count and no calibration for AQT IBEX-Q1 or IonQ Forte** — the docs say to read them from the
console or the `GetDevice` API, and any load-bearing number must come from there.

**The largest gate-based device on the provided infrastructure is 108 qubits.** Our smallest target
is N = 169. A one-qubit-per-residue run at full N is impossible on Braket for every arm. And §5.3 is
the tighter constraint: at these fidelities the coherent two-qubit budget is 100-250 gates, so the
exact Givens network runs at **N ~ 20**, not at 108. File 07 owns the consequence.

**Hard limits that bite.** _"The Ankaa-3 device has a maximum limit of 20,000 gates per circuit.
Circuits that exceed this limit are rejected with a validation error. This is a fixed limit that
cannot be increased."_ At N = 169 the Givens network is 14,196 gates and fits; at N = 272 it is
36,856 and does not.

**Simulators.** SV1 (state vector, on-demand): _"up to 34 qubits"_, 6-hour max runtime, and _"a
34-qubit, dense, and square circuit (circuit depth = 34) ... approximately 1-2 hours"_. DM1 (density
matrix): _"up to 17 qubits"_, reduced density matrix _"up to max 8 qubits"_. Local: `braket_sv` _"up
to 25 qubits"_, `braket_dm` _"up to 12 qubits"_, `braket_ahs` _"up to 10-12 atoms"_. **TN1 is no
longer listed in the device table** although the pricing page still names it — treat TN1 as
unavailable until confirmed.

**Pricing.** $0.30 per task on every QPU, plus per shot: IonQ Forte **$0.08**, AQT IBEX-Q1 $0.0235,
QuEra Aquila $0.01, IQM Emerald $0.0016, IQM Garnet $0.00145, Rigetti Cepheus **$0.000425**.
Simulators $0.075 per minute, 3-second minimum. Hybrid Jobs: SageMaker instance pricing, default
`ml.m5.xlarge` at $0.23/hour, quantum tasks billed as above.

That per-shot spread is a **188x** cost difference between IonQ Forte and Rigetti Cepheus and it
dominates the budget. Applying §6.2 (N circuits) and §6.1 (M shots):

| Configuration | IonQ Forte | AQT IBEX-Q1 | QuEra Aquila | IQM Emerald | Rigetti Cepheus |
| ------------- | ---------: | ----------: | -----------: | ----------: | --------------: |
| N=169, M=1e4  |   $135,251 |     $39,766 |      $16,951 |      $2,755 |            $769 |
| N=272, M=1e4  |   $217,682 |     $64,002 |      $27,282 |      $4,434 |          $1,238 |
| N=764, M=1e5  | $6,112,229 |  $1,795,629 |     $764,229 |    $122,469 |         $32,699 |

`[arithmetic ours, from the published price list]` The challenge provides Braket _"at no cost"_
(`CHALLENGE.md` §5), but a six-figure shot bill is not a plan even when someone else pays it. **Any
full-N hardware run is out on cost alone, before qubit count and fidelity are considered.**

**Hybrid Jobs.** _"quantum tasks that are created from a hybrid job benefit from higher priority
queueing to the target QPU device"_; _"You can submit a circuit using free parameters and Braket
compiles the circuit once, without the need to recompile for subsequent parameter updates to the same
circuit"_; and _"only one hybrid job can run on a QPU at any given time."_ Parametric compilation is
directly useful to us: the Givens network is one circuit reused across all N source columns.

### 7.2 Classiq

**What the synthesis engine does.** Classiq separates **synthesis** from **transpilation**, verbatim:
_"Classiq synthesis returns an execution-ready quantum program ... However, it is not yet transpiled
to a specific backend's gate set or connectivity"_, while _"Transpilation is the process of
optimizing an already-synthesized quantum program and matching it to the desired hardware."_
`[VERIFIED-FULLTEXT]` Synthesis is a design-space search: _"a complete quantum algorithm can be
realized in multiple ways, utilizing different design choices such as function implementations,
placement, uncompute strategies, qubit management, and wirings. The platform sifts through the design
space and finds a best realization given your requirements and resource constraints."_
`[VERIFIED-FULLTEXT]` That is a genuine difference from a Qiskit pass, which rewrites a circuit whose
structure is already fixed.

**The knobs, read from the shipped `classiq` 1.26.0 wheel rather than the docs.** `Constraints` has
exactly two public fields: `max_width` and `optimization_parameter`.
`OptimizationParameter` is `WIDTH | DEPTH | NO_OPTIMIZATION`, and `optimization_parameter` also
accepts a basis-gate name (e.g. `"cx"`), which is how two-qubit-count optimisation is expressed.
**`max_depth` and `max_gate_count` are not fields of `Constraints` in 1.26.0** despite the docstring
and the rendered SDK reference saying otherwise; the only public depth _bound_ is
`ExponentiationConstraints.max_depth`, whose default objective is `MINIMIZE_DEPTH`.
`[VERIFIED-FULLTEXT]`

**Hamiltonian evolution is first-class.** The open library exposes `suzuki_trotter`, `qdrift`,
`exponentiate`, `single_pauli_exponent`, `commuting_paulis_exponent`, `multi_suzuki_trotter`,
`sequential_suzuki_trotter`, and (in the wheel, not yet in the rendered reference)
`suzuki_trotter_commuting_grouped`, `suzuki_trotter_parallel_scheduled`,
`suzuki_trotter_cancellation_scheduled`. Input is `SparsePauliOp` or a list of `PauliTerm`. LCU
(`lcu`, `lcu_pauli`, `prepare_select`), QSVT (`qsvt`, `qsvt_inversion`, `qsvt_lcu`, `gqsp`) and block
encoding are all present. `[VERIFIED-FULLTEXT]`

**Question (e): the measured depth reduction, and its baseline.** Classiq publishes two reproducible,
code-included head-to-head comparisons.

_Hamiltonian evolution_ (H2O/STO-3G, 551 Pauli terms, 12 qubits, basis `["cx","u"]`, Qiskit 1.0.0):

| Case                           | Classiq CX | Qiskit CX | ratio |
| ------------------------------ | ---------: | --------: | ----: |
| Suzuki-Trotter order 1, reps 6 |      9,402 |    25,164 | 2.68x |
| ST order 2, reps 4             |     12,458 |    33,508 | 2.69x |
| ST order 4, reps 1             |     15,570 |    41,882 | 2.69x |
| **controlled** ST1, reps 6     |     21,252 |   186,067 | 8.76x |
| **controlled** ST2, reps 4     |     28,270 |   248,232 | 8.78x |
| qDRIFT N=1000                  |      3,388 |     3,581 | 1.06x |
| qDRIFT N=2000                  |      6,712 |     7,404 | 1.10x |

`[VERIFIED-FULLTEXT]` — docs.classiq.io, `hamiltonian_evolution` tutorial.

_HHL_, matched at solution fidelity, is the only published head-to-head **depth** comparison: Classiq
1,063 -> 4,729 against Qiskit 1,921 -> 159,291 across precision 1-7, i.e. **1.81x rising to 33.7x**.
`[VERIFIED-FULLTEXT]`

**The caveat that must travel with those numbers.** Both notebooks run
`transpilation_options = {"classiq": "auto optimize", "qiskit": 1}`, with the
`{"classiq": "custom", "qiskit": 3}` line present but commented out and labelled _"uncomment this for
deeper comparison"_. **The Qiskit baseline is `optimization_level=1`, not Qiskit's best.**
`[VERIFIED-FULLTEXT]` The qDRIFT baseline is additionally hand-rolled by Classiq rather than Qiskit's
own. Read the shape rather than the headline: ~2.7x on plain Trotter, ~8.8x when a `control()`
wrapper is involved, ~1.06x on qDRIFT. Our workload is plain, uncontrolled evolution, so **~2.7x
against Qiskit O1 is the number to plan with, and it is an upper bound on what we would see against
Qiskit O3.**

**Independent verification: none found.** Full-text greps for "classiq" over Benchpress
(arXiv:2409.08844), Arline Benchmarks (arXiv:2202.14025), arXiv:2509.16205 and arXiv:2406.06836
return **zero hits** in all four. `[VERIFIED-FULLTEXT]` The structural reason is that those harnesses
require a locally installable open-source compiler and Classiq is a hosted, authenticated service.
Every quantitative Classiq-versus-Qiskit number in this file was produced by Classiq or by a
Classiq co-authored paper.

**The adoption risk, in Classiq's own co-authored words.** arXiv:2603.05479, _"Quantum Simulation of
Coupled Harmonic Oscillators: From Theory to Implementation"_ (WISER + Classiq, 5 Mar 2026),
implements the Babbush et al. coupled-oscillator algorithm on Classiq and reports:

> _"The synthesis of deeper circuits becomes computationally demanding for larger N, and the synthesis
> engine could not reliably generate circuits beyond N = 16 within reasonable classical runtime and
> memory limits."_ `[VERIFIED-FULLTEXT]`

**A Classiq-co-authored paper hitting a classical synthesis wall at 16 oscillators, on precisely the
coupled-oscillator structure an elastic network model has, is the headline risk of putting Classiq on
our critical path.** Synthesis cost is classical and it bites early. Measure it on our own network
sizes before building on it.

**Braket integration works, with friction.** _"The Classiq executor supports any available gate-based
Amazon Braket simulator and quantum hardware"_ — listed: Forte 1, Emerald, Ankaa-3, Garnet; SV1, TN1,
dm1. Execution needs _"an AWS account, and a role that Classiq can assume for execution"_, whose
parameters _"may differ between users. Contacting Classiq support is required!"_ By default a Classiq
circuit reaches Braket through a _"standard adapter from Qiskit to Braket"_; `emulate=True` selects
Classiq's device-aware path instead. `[VERIFIED-FULLTEXT]` **Budget lead time for the cross-account
IAM role if hardware execution is on the critical path.**

---

## 8. Analog and special-purpose hardware

### 8.1 Neutral atoms: QuEra Aquila and the unit-disk constraint

Aquila is on Braket and is the only analog device there. Specifications: **256 atoms**; field of view
**75 um x 76 um**; **minimum atom spacing 4 um**; Rabi frequency **0 to 2.5 x 2pi MHz**; global
detuning **-20 to +20 x 2pi MHz**; **C6 = 862,690 x 2pi MHz um^6**; maximum sequence duration 4 us;
**shots range (1, 1000)** at **$0.01/shot**. `[VERIFIED-FULLTEXT — quera.com/aquila and AWS docs]`
The register is **2-D only**, and the drive is global: _"Access to local detuning is an Experimental
capability and is available by request through Braket Direct"_, and enabling it means _"the device
experiences faster decoherence than the T2 time listed"_. `[VERIFIED-FULLTEXT]`

The blockade radius at maximum Rabi frequency is `R_b = (C6/Omega)^(1/6) = 8.4 um`, about 2.1x the
minimum spacing `[arithmetic ours]` — the same regime as Ebadi et al., _Science_ 376, 1209 (2022),
doi:10.1126/science.abo6587, whose graphs were _"deterministically prepared with vertices occupying
80% of an underlying square lattice, with the blockade extending across nearest and next-nearest
(diagonal) neighbors"_ at `R_b/a = 1.7`. `[VERIFIED-FULLTEXT]` That is a King's graph: **maximum
degree 8, in the plane.**

**The honest embedding statement.** A Rydberg array natively realises a **unit-disk graph in 2D** —
Pichler, Wang, Zhou, Choi, Lukin, arXiv:1808.10816: _"UD graphs are geometric graphs, where vertices
are placed in the 2D plane and connected if their pairwise distance is less than a unit length."_
`[VERIFIED-FULLTEXT]` A residue contact network is a **unit-ball graph in 3D**, which is a different
class. Two consequences:

1. You cannot simply lay the protein out. Breu and Kirkpatrick, _Computational Geometry_ 9(1-2),
   3-24 (1998), doi:10.1016/S0925-7721(97)00014-X: **unit-disk graph recognition is NP-hard.**
   `[VERIFIED-ABSTRACT]` Deciding whether our graph even _has_ a planar unit-disk realisation is not a
   pipeline stage we can run.
2. You can _encode_ rather than embed, at a stated cost. Nguyen, Liu, Wurtz, Lukin, Wang, Pichler,
   _"Quantum Optimization with Arbitrary Connectivity Using Rydberg Atom Arrays"_, **PRX Quantum 4,
   010316 (2023)**, doi:10.1103/PRXQuantum.4.010316, build crossing and copy gadgets and conclude
   _"this construction leads to a UDG with at most 4N^2 vertices, corresponding to the optimal
   quadratic overhead for arbitrary connectivity"_. `[VERIFIED-FULLTEXT]`

`4N^2 <= 256` gives **N <= 8 residues.** `[arithmetic ours]` An arbitrary-connectivity encoding of
even a 20-residue coarse-grained network needs ~1,600 atoms, over six times Aquila.

There is a partial escape the same paper names: _"For restricted connectivity, one may construct a
lower-overhead crossing lattice"_, and _"a restricted 2D QUBO problem can be mapped onto UDG-MWIS with
only a constant overhead."_ `[VERIFIED-FULLTEXT]` Whether a coarse-grained residue network falls in
that class is an open question for file 07, and must be **checked rather than assumed**.

One further mismatch, and it is fundamental rather than a scale problem: **Aquila runs an Ising
(Rydberg-blockade) Hamiltonian, not a hopping Hamiltonian.** `V_vdw = C6/d^6 n_i n_j` is diagonal;
it produces no transport. The natural Aquila problem is maximum weighted independent set, and node
weights need the experimental local-detuning feature. Aquila is a plausible platform for a
_combinatorial_ formulation of site selection; it is not a platform for signal propagation.

### 8.2 Quantum annealers

**D-Wave is not available on Amazon Braket.** AWS Quantum Technologies Blog, 17 November 2022:
_"Starting today, access to D-Wave products and services has fully transitioned to the AWS
Marketplace, and customers can no longer access the D-Wave 2000Q and Advantage systems via Amazon
Braket."_ `[VERIFIED-FULLTEXT]` An annealer is therefore outside the _"provided infrastructure"_ of
`CHALLENGE.md` §5 constraint 4, and using one is a separate procurement decision.

Minor-embedding cost is quadratic and remains so across generations. From Boothby, King, Roy,
arXiv:1507.04774, the Chimera clique embedding uses _"chains of size M+1"_ to give a `K_LM` minor in
`C_{M,M,L}`, which has `2LM^2` qubits — so embedding `K_n` costs `2n^2/L` physical qubits, i.e.
`n^2/2` at D-Wave's `L = 4`, reproducing the 2000Q's 2,048 qubits / `K_64` exactly. `[VERIFIED-FULLTEXT
for the theorem; arithmetic ours]` Pegasus improves the constant, not the exponent: Boothby, Bunyk,
Raymond, Roy, arXiv:2003.00133, give cliques _"of size at most a = 12(M-1)"_, i.e. `K_180` on an
Advantage P16. `[VERIFIED-FULLTEXT]`

A published annealer result computing **eigenvectors or eigenvalues of a graph Laplacian** — which is
what a GNM/ANM baseline needs — was **not retrieved by the recorded search**. What exists is
Laplacian-derived QUBO work: Ushijima-Mwesigwa, Negre, Mniszewski, _"Graph Partitioning using Quantum
Annealing on the D-Wave System"_, arXiv:1705.03082. `[VERIFIED-ABSTRACT]` Partitioning is a
combinatorial problem, not a spectral one, and the distinction matters for what an annealer could
contribute here.

### 8.3 Photonic Gaussian boson sampling

Covered as an encoding in §2.5. Three deployment facts: the encoding is
`A = U diag(lambda) U^T` with _"exactly N optical modes ... one mode per node"_
`[VERIFIED-FULLTEXT]`, which is the **only** zero-overhead encoding of an arbitrary adjacency matrix
in this review; the sampled quantity is a hafnian (perfect-matching count), so the observable is a
subgraph-density statistic and not a propagator; and **no photonic device appears in the Braket
device table retrieved 2026-08-25**. `[VERIFIED-FULLTEXT]` The nearest drug-discovery precedent,
Banchi, Fingerhuth, Babej, Ing, Arrazola, _Science Advances_ 6, eaax1950 (2020),
doi:10.1126/sciadv.aax1950, reduces docking to _"finding the maximum weighted clique in a graph"_ and
ran its benchmark on a **24-vertex** graph after subselecting 4 ligand and 6 receptor points from 11
and 243. `[VERIFIED-FULLTEXT]`

---

## 9. The resource table template — question (b)

**This is the table every quantum method in this project fills before it is accepted.** Fill every
cell or write `unknown` and name the experiment that would fill it. A blank is a failed C3 report.

Assumptions fixed for comparability: exact `exp(-iHt)` at `t = 5/J`; scoring = transfer probability
from the active-site source set; deliverable = full `N x N` matrix plus a top-5 list; "shots" is per
source column; runtime assumes a 400 ns two-qubit gate (Weidenfeller et al.) and ignores queue time.

### 9.1 Filled as far as the evidence allows

`lambda` is quoted at **p = 5e-3**, the median two-qubit error of IQM Emerald and Rigetti Ankaa-3
fSim (§5.3) — i.e. what the provided platform actually delivers, not an aspirational rate.
`N = 20` is included as the size §5.3 shows is reachable.

| Encoding                       |   N |                  Qubits |                       2q gates |                      2q depth | Connectivity       |        Shots/column | `lambda` at p=5e-3 | Est. runtime (coherent, per shot) | Runs on Braket?                |
| ------------------------------ | --: | ----------------------: | -----------------------------: | ----------------------------: | ------------------ | ------------------: | -----------------: | --------------------------------: | ------------------------------ |
| One-hot, exact Givens          |  20 |                      20 |                            190 |                            20 | line               |             unknown |           **0.39** |                            8.0 us | **yes**                        |
|                                | 150 |                     150 |                         11,175 |                           150 | line               |                 1e4 |            4.7e-25 |                             60 us | no (>108 qubits, and fidelity) |
|                                | 300 |                     300 |                         44,850 |                           300 | line               |            ~1e4-1e5 |            2.3e-98 |                            120 us | no                             |
|                                | 800 |                     800 |                        319,600 |                           800 | line               |                ~1e5 |                 ~0 |                            320 us | no                             |
| One-hot, Trotter r=64          |  20 |                      20 |                         ~3,200 |                        ~1,088 | all-to-all         |             unknown |             1.1e-7 |                            435 us | qubits yes, fidelity no        |
|                                | 150 |                     150 |                        ~45,000 |                        ~1,088 | all-to-all         |                 1e4 |              3e-98 |                            435 us | no                             |
|                                | 300 |                     300 |                        ~90,000 |                        ~1,088 | all-to-all         |            ~1e4-1e5 |           8.9e-196 |                            435 us | no                             |
|                                | 800 |                     800 |                       ~240,000 |                        ~1,088 | all-to-all         |                ~1e5 |                 ~0 |                            435 us | no                             |
| Binary / Gray, generic unitary |  20 |                       5 |                            444 |                       unknown | any (x9 on a line) |             unknown |               0.11 |                           unknown | yes                            |
|                                | 150 |                       8 |                         31,020 |                       unknown | any                |             unknown |              3e-68 |                           unknown | qubits yes, fidelity no        |
|                                | 300 |                       9 |                        124,844 |                       unknown | any                |             unknown |           1.7e-272 |                           unknown | qubits yes, fidelity no        |
|                                | 800 |                      10 |                        500,908 |                       unknown | any                |             unknown |                 ~0 |                           unknown | qubits yes, fidelity no        |
| Binary + sparse oracle         | any |            log2 N + anc | unknown (oracle `O(Nd)`/query) |                       unknown | any                |             unknown |            unknown |                           unknown | unknown                        |
| Coupled-oscillator (Babbush)   | 150 |               ~16 + anc |                        unknown |                       unknown | any                | n/a for full matrix |            unknown |                           unknown | unknown                        |
|                                | 300 |               ~18 + anc |                        unknown |                       unknown | any                |                 n/a |            unknown |                           unknown | unknown                        |
|                                | 800 |               ~20 + anc |                        unknown |                       unknown | any                |                 n/a |            unknown |                           unknown | unknown                        |
| Directed-edge sector (DTQW)    |  17 | 2\|E\| = 40 (published) |                        unknown |       287 layers over 7 steps | heavy-hex          |       5.3e5 x 1.1^t | Hellinger F > 0.87 |                           unknown | not on Braket (IBM)            |
|                                | 150 |         ~2\|E\| ~ 1,400 |                        unknown | ~11/step (a2a), ~28/step (hh) | any                |             unknown |            unknown |                           unknown | **no**                         |
| Neutral atom, arbitrary conn.  |   8 |        4N^2 = 256 atoms |                   n/a (analog) |                           n/a | 2D unit disk       |            <= 1,000 |                n/a |                          4 us max | **yes, at N = 8**              |
|                                | 150 |  <= 4N^2 = 90,000 atoms |                   n/a (analog) |                           n/a | 2D unit disk       |            <= 1,000 |                n/a |                          4 us max | **no** (256 atoms)             |
| GBS qumodes                    | 150 |               150 modes |                   n/a (analog) |                           n/a | n/a                |             unknown |                n/a |                               n/a | **no device**                  |
| Classical reference (`eigh`)   | 150 |                       0 |                              0 |                             0 | n/a                |                   0 |                  1 |                        **1.6 ms** | n/a                            |
|                                | 300 |                       0 |                              0 |                             0 | n/a                |                   0 |                  1 |                        **6.0 ms** | n/a                            |
|                                | 800 |                       0 |                              0 |                             0 | n/a                |                   0 |                  1 |                         **48 ms** | n/a                            |

Sources per column: qubits and gates from §2; depth from §2.1 and §3.2; connectivity from §4;
shots from §6.1; `lambda` from §5.2-§5.3; device error rates from §5.3; classical runtime measured in
§10. `unknown` cells are honest gaps, and each names the missing measurement:

- **Binary/Gray depth** — needs a synthesis run (Qiskit `transpile` or Classiq `synthesize`) on a real
  contact graph's `exp(-iHt)` at 8-10 qubits. Cheap to do; not done here.
- **Sparse-oracle cost** — needs a QROM gate count for our specific `N x d` adjacency table.
- **Coupled-oscillator cost** — Babbush et al. give complexity in oracle queries, not gate counts for
  a specific `A`. Needs the same QROM accounting.
- **Directed-edge CTQW cost** — Dubovitskii et al. publish it for a DTQW only.
- **Shot budgets for the compressed encodings** — the readout is not a computational-basis sample, so
  §6.1's measurement does not transfer.
- **Shots at N = 20** — §6.1 was measured at N = 169-764. The coarse-grained size has fewer residues
  to separate, so the budget should fall; measure it once file 07 fixes the size.

**Read the `N = 20` row against every other row.** It is the only row in the table with a `lambda`
above 0.1 on hardware Braket actually provides. That row, not the N = 300 row, is the hardware
demonstration this submission can make.

### 9.2 How to fill a row for a new method

1. Write the Hamiltonian and its encoding. State qubits as a formula in N.
2. Emit the circuit and count two-qubit gates and two-qubit depth from the **transpiled** circuit for
   a named device, not the logical one.
3. State the connectivity requirement, and if it is not "line", give the routing overhead using the
   §4.2 formulas for the actual target.
4. Compute `lambda = (1-p)^G` with `p` from that device's published calibration. If `lambda < 1e-3`,
   say so; do not report an expectation value as if it survived.
5. Measure shots by the §6.1 protocol — top-5 overlap against the exact classical propagator on the
   same graph, not by a variance heuristic.
6. Multiply the shot budget by `1/lambda^2` (§5.1) and price it against §7.1.
7. Report the classical wall-clock for the same output on the same machine.

---

## 10. Question (c): where does a device beat a laptop?

**Measured on this machine** (macOS arm64, numpy 2.5.2, single call to `numpy.linalg.eigh` plus the
full `N x N` propagator and its squared modulus — i.e. the entire mandated connectivity-matrix
deliverable):

|    N |   `eigh` | full `N x N` `exp(-iHt)` + `abs()^2` |        total |
| ---: | -------: | -----------------------------------: | -----------: |
|  150 |  1.30 ms |                              0.33 ms |  **1.63 ms** |
|  169 |  1.34 ms |                              0.31 ms |  **1.65 ms** |
|  300 |  4.59 ms |                              1.45 ms |  **6.04 ms** |
|  451 | 11.16 ms |                              7.07 ms | **18.23 ms** |
|  764 | 38.79 ms |                             42.95 ms | **81.74 ms** |
|  800 | 32.69 ms |                             15.25 ms | **47.93 ms** |
| 2000 |   527 ms |                               569 ms |   **1.10 s** |

`[measured in this session; not a registered experiment]`

**The blunt answer: nowhere, for this problem, at this size, on this hardware.** The whole
deliverable for our largest target takes 82 milliseconds classically. The best quantum route we have
found needs 291,466 two-qubit gates on 764 qubits, which no device on Braket can hold, at a fidelity
requirement three orders of magnitude beyond the best published two-qubit error rate, for a shot bill
of $33,000 on the cheapest device. There is no crossover at N <= 2,000.

Put the two numbers next to each other. The device is coherent for about **20 nodes**; the laptop
does **764 nodes in 82 ms** and 2,000 nodes in 1.1 s. The gap is not close, and it is not closing
from the direction we can push. A single-excitation walk on N nodes is an `N x N` linear-algebra
problem, and `N` is a protein's residue count — a number that is small by construction.

Three named regimes where the sign could flip, each with its blocking condition:

1. **Many-body dynamics.** A single-particle Hermitian walk on a graph is classically simulable in
   `O(N^3)`; the exponential-Hilbert-space argument only applies once the state has more than one
   excitation, or the evolution is non-Hermitian. `docs/evidence/method-landscape/00-conventions.md` §5 records
   that this was already measured and closed across eleven observables. **Blocked by physics, not by
   hardware.**
2. **`N` beyond classical eigendecomposition.** `eigh` is `O(N^3)`; at `N ~ 10^6` nodes it stops
   being a laptop operation. A protein has `10^2` to `10^4` residues. **Blocked by the problem
   size.** A whole-proteome interaction network would qualify — that is a different project, and it
   is what Dubovitskii et al.'s PPI case study is reaching for.
3. **A sub-linear readout that is genuinely all we need.** Babbush et al.'s exponential speedup is
   real for a _subset energy_, and BQP-complete at that. If the deliverable were "is the total
   fluctuation energy on this candidate pocket above threshold", `log N` qubits and `poly(log N)`
   gates would be the right resource line. `CHALLENGE.md` §5 asks for the full `N x N` matrix
   instead, and Babbush et al. state that outputting the full vector _"would necessarily have
   complexity at least linear in N."_ **Blocked by the deliverable specification** — and this is the
   one blocker that could be renegotiated with the organisers, since a top-5 list needs only a
   handful of subset energies.

The credible C4 story for this project is therefore not "the device is faster". It is: **an exact,
shallow, linearly-connected circuit exists; we run it at a coarse-grained size the hardware can hold;
we report the full resource line and the fidelity ceiling honestly; and we show the coarse-grained
ranking against the exact classical ranking at full N.** That is a demonstration of viability, and
`CHALLENGE.md` §4.2 asks for exactly that under "scalability / coarse-graining". Claiming a speedup
would be false and a judge would find it in one question.

---

## What this changes for our pipeline

1. **`quantum/` should implement the one-hot single-excitation encoding, and a Givens-rotation
   network, not a Trotteriser.** The exact circuit is 2.2x cheaper in gates and 3.8x shallower than
   the `r = 64` Trotter approximation that first reproduces the top-5, and has no Trotter error
   (§2.1, §3.2, §3.6). Trotter remains useful only as a knob for a deliberate noise-resilience study.
2. **Do not build a `ceil(log2 N)` compressed encoding for an arbitrary contact graph.** 124,844
   CNOTs against a 65,529 generic lower bound at N = 300 (§2.3). The one live route is a
   _coarse-grained_ network designed to have exploitable structure — a decision that belongs to
   file 07, and this file supplies the cost argument for why the structure has to be designed in
   rather than hoped for.
3. **Do not import Jordan-Wigner or Bravyi-Kitaev into `quantum/`.** C6 gives no antisymmetry to
   enforce, and 34-40% of our contacts would carry a Z-string up to 645 qubits long (§2.4).
4. **`network/` should emit the edge-colouring alongside the adjacency matrix.** It is 16-17 classes
   at every N, it is the parallel-gate schedule, and it costs one greedy pass (§1.1).
5. **The connectivity-matrix deliverable costs N circuits, not N^2** (§6.2). Build the artefact
   writer around one circuit and N input states, and use Braket's parametric compilation under Hybrid
   Jobs.
6. **The coarse-graining target is ~20 nodes, and hardware sets it, not methodology.** At Braket's
   published 99.5 % median two-qubit fidelity the coherent budget is ~200 two-qubit gates, so
   `N(N-1)/2 <= 200` gives **N ~ 20** (§5.3). This is a hard input to file 07, which must show that a
   35x compression of myosin retains the topological signal, not merely that some compression does.
7. **The noise-resilience study required by `CHALLENGE.md` §4.2 should be framed as resolution loss,
   not rank inversion.** Global depolarising noise provably preserves rank order; the deliverable
   degrades through the `1/lambda^2` shot budget (§5.1). Report `lambda`, the required shots, and the
   price, per device. **And keep the precondition**: all residue scores must come from one noisy
   state with one common `lambda`, which the §6.2 single-circuit readout satisfies and a per-residue
   observable scheme does not (§5.4). That is a constraint on the observable definition in file 03.
8. **Register the ranking-stability measurement as an experiment — it is a contribution, not just
   diligence.** No paper retrieved reports Kendall tau or top-k overlap between an ideal and a noisy
   node ranking as a function of error rate and shot count (§5.4). The closest precedent, the CTQW
   residue-centrality paper, reports only that top residues "remain consistent" on one 9-residue
   peptide. Our §5.1 and §6.1 measurements already have the shape of the missing result.
9. **Add symmetry-verification postselection to any hardware run.** Number conservation gives free
   error detection, published as effective at 40 qubits (§5.6). Report the retained fraction — it
   decays exponentially with depth and is itself a resource cost. Budget readout mitigation and
   at most two-point ZNE; do not budget for PEC, whose overhead is `e^(4 M p)` (§5.5).
10. **No full-N hardware run is affordable or possible.** Braket's largest gate-based device is 108
    qubits against a smallest target of N = 169, Ankaa-3 rejects circuits above 20,000 gates, Aquila
    caps at 1,000 shots per task, and the cheapest full-N shot bill for myosin is ~$33,000 (§6.1,
    §7.1). The hardware demonstration must be a coarse-grained one.
11. **Treat Classiq as a compiler with a measured ~2.7x CX advantage on plain Trotter against Qiskit
    `optimization_level=1`, and verify it ourselves.** No independent benchmark of Classiq exists in
    four full-text compiler-benchmark papers, and a Classiq co-authored paper reports its synthesis
    engine failing beyond **16 coupled oscillators** (§7.2). Before Classiq goes on the critical path,
    run one experiment: synthesise `exp(-iHt)` for a real contact graph at our coarse-grained size and
    record synthesis wall-clock, width and depth.
12. **QuEra Aquila is not a propagation platform.** Its Hamiltonian is diagonal in the interaction
    term, its register is 2-D, and arbitrary connectivity costs `<= 4N^2` atoms, i.e. **N <= 8** on
    256 atoms (§8.1). If a neutral-atom arm is attempted at all, it must be a combinatorial
    (independent-set) formulation, and it needs the experimental local-detuning feature for node
    weights.
13. **Every quantum arm fills the §9 table before it is accepted.** That is the operational form of
    C3, and the `unknown` cells in §9.1 are the backlog of measurements this review could not make.

---

## Method

**Databases and endpoints.** arXiv API (`export.arxiv.org/api/query`; returned HTTP 429 repeatedly
and was retried with exponential backoff and a User-Agent header), `arxiv.org/abs` and
`arxiv.org/pdf` pages, `ar5iv.labs.arxiv.org` for full text, `quantum-journal.org`,
`docs.aws.amazon.com/braket`, `aws.amazon.com/braket/pricing`, `aws.amazon.com/blogs/quantum-computing`,
`docs.classiq.io` (raw markdown twins indexed at `docs.classiq.io/llms.txt`), the `classiq` 1.26.0
wheel from PyPI, `quera.com/aquila`, `docs.dwavequantum.com`, `scottaaronson.com/papers/qml.pdf`.
PDFs were text-extracted locally with `pypdf` where a fetch returned binary.

**Queries run on arXiv.** `all:"Gray code" AND all:"Hamiltonian" AND cat:quant-ph`;
`all:"single-excitation subspace"`; `abs:"qubit-efficient" AND abs:"encoding"`;
`abs:"quantum walk" AND abs:"quantum circuit" AND abs:"efficient"`; `ti:"Theory of Trotter Error"`;
`abs:"qDRIFT"`; `ti:"Qubitization" OR ti:"Quantum Signal Processing"`;
`ti:"sparse Hamiltonian" AND abs:"simulation"`; `abs:"heavy-hex"`;
`abs:"qubit routing" AND abs:"overhead"`; `ti:"classical shadows" OR ti:"Predicting many properties
of a quantum system from very few measurements"`; `abs:"protein" AND abs:"quantum walk"`.
Roughly 8 records screened per query; ~35 screened in, ~25 cited.

**Delegated sub-searches.** Three parallel agents covered (i) device metrics, noise models, error
mitigation and ranking stability, (ii) Classiq documentation and benchmarks, (iii) analog and
special-purpose hardware. Their sources are cited inline above with the same tags. The shared
WebSearch budget (200 calls) was exhausted during (ii); the remaining work used direct fetches only.

**Stopping rule.** Stop when the encoding, simulation-cost, connectivity, noise, measurement,
platform and analog sections each carry at least one primary source with a number, and when questions
(a)-(e) each have either a sourced answer or an explicit `unknown` with a named experiment.

**Measurements made in this session** (scripts in the session scratchpad; none are registered
experiments, and any of these numbers that becomes load-bearing must be re-run under
`docs/playbooks/experiment.md` and recorded in `experiments/REGISTRY.md`):

- Contact-graph statistics for all five frozen arms (§1.1) — via `allo.inputs.apo_input`, C-alpha,
  8 A cutoff. No holo data touched.
- Greedy edge colouring of each contact graph (§1.1).
- First-order Trotter convergence of the top-5 against the exact spectral propagator (§3.2).
- Shot budget for top-5 stability, noiseless and under global depolarising noise (§5.1, §6.1).
- Classical wall-clock for the full deliverable (§10).
- Arithmetic instantiations of published formulas (Shende et al. CNOT counts, Weidenfeller et al.
  Table 1, `lambda = (1-p)^G`, Braket prices, Aquila blockade radius, `4N^2 <= 256`).

**Not retrieved by the recorded search.**

- A published construction implementing `exp(-iHt)` for an _arbitrary_ graph on `ceil(log2 N)` qubits
  with better than generic-unitary cost. Efficient constructions exist for circulant graphs
  (arXiv:1510.08657) and for structured solid-state lattices (arXiv:2601.00247); neither covers a
  protein contact graph.
- A gate-count (as opposed to query-count) resource estimate for a 300-node degree-9 graph under
  qubitisation or QSP with an explicit oracle construction.
- An M-dependent (edge-count-aware) refinement of the `4N^2` Rydberg overhead.
- An explicit theorem on 3D unit-ball to 2D unit-disk realisability.
- A published Zephyr clique-embedding formula.
- Annealer results on _spectral_ graph-Laplacian problems as opposed to Laplacian-derived QUBOs.
- A primary AWS announcement of the Xanadu Borealis retirement date.
- Any independent, non-Classiq benchmark of Classiq against Qiskit, tket or BQSKit.
- Classiq-side circuit _depths_ for the Hamiltonian-evolution comparison (only CX counts are printed).
- Official Classiq Coding Competition results with per-competitor depths.
- Qubit counts and calibration for AQT IBEX-Q1 from any primary source; and none for any Braket
  device from AWS documentation, which points to the console or the `GetDevice` API instead. IonQ's
  36 qubits and IQM's/Rigetti's fidelities came from vendor and AWS-blog pages, not the dev guide.
  **Use the live `GetDevice` API before any of §5.3's numbers becomes load-bearing.**
- Coherence times (T1, T2) for IQM Garnet or Emerald from a landable primary page. Values circulate
  in search summaries and conflict with each other.
- Any paper studying quantum PageRank under **decoherence**: an arXiv query
  `abs:"PageRank" AND abs:"decoherence"` returned 0 results, and `abs:"Kendall" AND abs:"quantum
computer"` returned 0.
- Any paper reporting Kendall tau or top-k overlap between a noiseless-simulator node ranking and a
  QPU node ranking as a function of shot count or error rate.
- A top-k recovery guarantee under shot noise for graph centrality.
- Any use of the phrase "noise-induced ranking inversion".
- A published statement of the `M >= 8/delta^2` shot bound for _ordering_ two quantum expectation
  values; §6.1's derivation is ours.
