# Quantum and quantum-inspired algorithms as the propagation engine

**Scope:** this file covers the algorithms that could _be_ the propagation step or the scoring
metric — walks on graphs, state transfer on spin networks, open-system transport, bosonic and
vibrational simulation, quantum linear algebra, quantum optimisation, and quantum-inspired
classical methods. Its question is: **what quantum object could carry the allosteric signal?**
It deliberately excludes quantum machine learning, quantum kernels and quantum reservoirs
(trained models, file 04), and circuit depth, qubit counts and hardware costing (file 08).
**Sibling files:** `04-hybrid-quantum-ai.md` for anything with a trained readout;
`01-classical-baselines.md` for the ENM and spectral bar this must clear; the hardware-resource
file for every depth and qubit number quoted here in passing;
`allosteric-benchmark/docs/quantum-observable-search.md` for the eleven closed insertion points.
**Retrieved:** 2026-08-25.

---

## 1. The structural fact that organises the whole field

`00-conventions.md` §5 states the diagnosis a teammate reached by measurement:

> A single-particle Hermitian walk on a graph is classically simulable and carries no
> information beyond its transfer amplitudes.

This review found that the diagnosis is **stronger and more general than the repository states**,
and that it now has a peer-reviewed complexity-theoretic form. The relevant theorem is not about
quantum walks at all. It is about _any_ linear dynamical system whose matrix vanishes beyond a
geometric cutoff — which is the exact definition of a residue contact graph.

**Sakamoto & Fujii**, _Quantum_ **10**, 2182 (2026), doi:10.22331/q-2026-08-03-2182
(arXiv:2505.10445), Definition 5:

> Consider the finite-volume lattice with sites labeled as $i=\{1,\dots,N\}$ … we say that
> $A\in\mathbb{C}^{N\times N}$ is an $(r_0,\mathcal{N}(r_0))$-geometrically local matrix if
> there exists a value $r_0\in\mathbb{R}_+$ such that $A_{ij}=0$ for $d(i,j)>r_0$.
> `[VERIFIED-FULLTEXT]`

A Kirchhoff matrix built with a Cβ contact cutoff is an $(r_0,\mathcal{N}(r_0))$-geometrically
local matrix, with $r_0$ the cutoff and $\mathcal{N}(r_0)$ the maximum contact degree.
`[UNVERIFIED — our reading of the definition, not a claim in the paper]`

Their result:

> This result implies that simulating the short-time ($t=\mathrm{polylog}(N)$) dynamics with
> geometrically local interactions does not yield any exponential quantum advantage in both time
> and space complexities. … our results imply that no exponential quantum advantage exists for
> short-time evolution. This is a nontrivial finding that rules out the exponential quantum
> speedup or space advantage in the form discussed in many prior works. `[VERIFIED-FULLTEXT]`

They also close the sampling loophole — sampling from a short-time evolved state under a
geometrically local matrix is classically easy too (their Theorem 3) `[VERIFIED-FULLTEXT]` —
and they show that the _long_-time regime ($t=\mathrm{poly}(N)$) is equivalent to
$\mathrm{poly}(N)$-time, $O(n)$-space quantum computation, so the advantage that survives is a
**space** advantage, or a time advantage only under a polynomial-space restriction
`[VERIFIED-FULLTEXT]`.

**What this changes.** The teammate closed eleven observables one at a time by measurement. This
theorem says the closure was not a run of bad luck: geometric locality plus short evolution time
is _sufficient_ to remove exponential advantage, whatever observable you read out. Any proposal
in this file that keeps the contact graph, keeps the dynamics linear, and reads out at short
times is refuted before it is coded. The only escape routes are the three the theorem does not
cover: long-time dynamics at fixed polynomial space, a non-linear or many-body Hamiltonian, or
a different object than the contact graph.

---

## 2. Candidate quantum observables — the table

`sim@300` is the cost of the honest classical computation at our working size, N ≈ 300 residues.
All dimension and flop figures in this column were computed in this session with `math.comb` and
elementary counting, not recalled.

| Observable                                                                    | What it needs from H                                            | Does a real symmetric contact graph supply it?                 | Classically simulable at N=300?                                                                                 | Already closed                                                                             |
| ----------------------------------------------------------------------------- | --------------------------------------------------------------- | -------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| CTQW transfer amplitude $\lvert\langle j\rvert e^{-iHt}\lvert i\rangle\rvert$ | Hermitian H, one excitation                                     | Yes                                                            | **Yes.** Dense `expm` is $O(N^3)=2.7\times10^7$ flops                                                           | **Closed** (§5 item 1)                                                                     |
| Time-averaged transfer $C_{ij}$                                               | Eigenvalue non-degeneracy for interference                      | **No** — 3.6 % of low gaps below 1 %                           | Yes, same cost                                                                                                  | **Closed** (items 1, 4)                                                                    |
| Quantum PageRank / Szegedy walk centrality                                    | A stochastic matrix + a coin register                           | Yes (row-normalise)                                            | **Yes.** Szegedy walk is a $2N^2$ unitary; $O(N^6)$ worst case, still trivial                                   | **Closed in substance** — a graph-global centrality (item 5, and doi:10.1021/jacs.6c08053) |
| Quantum communicability $(e^{-iHt})_{ij}$ vs. $(e^{Ht})_{ij}$                 | Nothing extra                                                   | Yes                                                            | Yes                                                                                                             | **Closed** — same matrix function as item 1                                                |
| Perfect / pretty-good state transfer fidelity                                 | **Engineered** couplings or spectral integrality                | **No** — couplings are fixed by geometry, not designable       | Yes                                                                                                             | Not tested; ruled out by construction (§4)                                                 |
| ENAQT efficiency vs. dephasing rate γ                                         | Site-energy disorder **and** a source–sink gradient             | **No** — uniform on-site energies, no trap                     | Yes; $\rho$ is 90 000 entries = 1.4 MiB                                                                         | **Closed** (item 3), but for a reason the γ sweep could not see (§5)                       |
| Quantum stochastic walk interpolation parameter                               | A Lindbladian with non-trivial jump operators                   | Only if we invent them                                         | Yes                                                                                                             | Same family as item 3                                                                      |
| OTOC / Krylov complexity / operator growth                                    | **Many-body interactions**                                      | **No**                                                         | Yes — collapses to $4g^2(r,t)$                                                                                  | **Closed** (item 9)                                                                        |
| Lieb–Robinson velocity                                                        | Bounded-range H                                                 | Yes, but the bounded object is the propagator                  | Yes                                                                                                             | **Closed** (item 10)                                                                       |
| Non-Hermitian / exceptional-point sensitivity                                 | Non-reciprocity or gain/loss                                    | **No**                                                         | Yes                                                                                                             | **Closed** (item 11)                                                                       |
| Chiral-walk directional asymmetry                                             | Cycles (E − N + 1)                                              | **Yes**, 7.7–8.3 cycles per residue                            | Yes                                                                                                             | **Closed by measurement** (item 8) — precondition held, observable failed                  |
| k-excitation sector amplitudes, **non-interacting**                           | k excitations, no interaction term                              | Yes trivially                                                  | **Yes.** Free fermions/matchgates are poly-time (doi:10.1137/s0097539700377025; doi:10.1103/physreva.65.032325) | Not tested; equivalent to item 1                                                           |
| k-excitation sector amplitudes, **interacting**                               | A genuine two-body term on the graph                            | **No physical basis from Cβ coordinates**                      | **No** — C(300,5)=1.96×10¹⁰ (292 GiB), C(300,10)=1.40×10¹⁸                                                      | Not tested; unmotivated (§8)                                                               |
| Kinetic/potential energy of an oscillator subset (Babbush encoding)           | Sparse-access oracle to the spring matrix, polylog-time queries | **No** — the matrix is incompressible in N (§6)                | Yes; the classical problem is $O(N^3)$                                                                          | **New here.** Blocked on read-in, not read-out                                             |
| ENM normal modes via a quantum ENM                                            | Same, plus a mode extraction the encoding does not have         | **No** — "Extracting such normal modes is not … possible" (§6) | Yes                                                                                                             | **New here**                                                                               |
| Gaussian-state moments of a bosonic ENM (CV encoding)                         | Non-Gaussianity somewhere                                       | **No** — a harmonic network is exactly Gaussian                | **Yes** — Gaussian in, Gaussian out is poly-time (doi:10.1103/physrevlett.88.097904)                            | **New here**                                                                               |
| GBS photon patterns on the adjacency matrix (dense subgraph, max clique)      | An adjacency matrix with **sign structure** for interference    | **No** — a contact adjacency matrix is non-negative            | **Yes in practice** — quantum-inspired sampler matches it (doi:10.1103/prxquantum.5.020341)                     | **New here**; a different framing from the closed QUBO, and it also fails                  |
| Low-lying eigenvalue shift under a local stiffening (ADR 0002 metric 5)       | Nothing quantum. A Hermitian matrix and a diagonalisation       | Yes                                                            | **Yes** — 300 × $O(N^3)$ = 8.1×10⁹ flops, seconds                                                               | **This is ALPS.** Already the repo's best method, and classical                            |
| Quantum phase estimation of the shifted spectrum                              | Block-encoded $\sqrt{A}$, a QROM oracle                         | Buildable, at $\tilde O(N)$ gates                              | Yes (the classical answer is the above)                                                                         | **New here** — a hardware route to a number we already compute cheaply                     |

---

## 3. Walks on graphs — where the exponential speedup actually lives

The foundational results are sound and are being misread across this problem domain, so state
them precisely.

- **Farhi & Gutmann**, _Phys. Rev. A_ **58**, 915 (1998), doi:10.1103/physreva.58.915 — the
  continuous-time walk as $e^{-iHt}$ with H the graph adjacency matrix. `[VERIFIED-ABSTRACT]`
- **Childs, Cleve, Deotto, Farhi, Gutmann & Spielman**, STOC 2003,
  doi:10.1145/780542.780552 — "Exponential algorithmic speedup by a quantum walk", the glued-trees
  problem. `[VERIFIED-ABSTRACT]`
- **Childs**, _Phys. Rev. Lett._ **102**, 180501 (2009), doi:10.1103/physrevlett.102.180501 —
  universal computation by a **single-particle** continuous-time walk. `[VERIFIED-ABSTRACT]`
- **Childs, Gosset & Webb**, _Science_ **339**, 791 (2013), doi:10.1126/science.1229957 —
  universal computation by **multiparticle** walk. `[VERIFIED-ABSTRACT]`
- **Szegedy**, FOCS 2004, doi:10.1109/focs.2004.53 — the discrete-time walk from a Markov chain,
  quadratic speedup in hitting time. `[VERIFIED-ABSTRACT]`

**The trap.** Childs 2009 proves a single-particle walk is universal. That is a statement about
walks on _exponentially large, implicitly specified_ graphs whose structure encodes a circuit.
It says nothing about a walk on an explicitly stored 300 × 300 matrix. The same applies to the
glued-trees speedup: it is an **oracle** separation on a graph with $2^n$ vertices. Our graph has
N vertices, all of them in memory, and $e^{-iHt}$ costs $O(N^3)$.

**Quantum PageRank and quantum centrality.** Discrete- and continuous-time variants were compared
in arXiv:1511.04823 `[VERIFIED-ABSTRACT]`, and generalised with arbitrary phase rotations in
arXiv:2209.13451 `[VERIFIED-ABSTRACT]`. A PT-symmetric construction exists specifically to handle
_directed_ graphs, where the resulting Hamiltonian is non-Hermitian (arXiv:1607.02673)
`[VERIFIED-ABSTRACT]`. That last one is the only route that adds structure a contact graph lacks,
and it needs a directed graph we do not have. Everything else in this family is a graph-global
centrality — the exact object doi:10.1021/jacs.6c08053 showed reproduces classical eigenvector
centrality on ~150 proteins, and which ADR 0002 already names as a mandatory control.

**Quantum communicability.** Estrada & Hatano's communicability, _Phys. Rev. E_ **77**, 036111
(2008), doi:10.1103/physreve.77.036111, is $(e^{A})_{ij}$ `[VERIFIED-ABSTRACT]`. The "quantum"
version replaces $e^{A}$ with $e^{-iAt}$. That is item 1 in `00-conventions.md` §5 under a
different name, and Mülken & Blumen's review, _Phys. Rep._ **502**, 37 (2011),
doi:10.1016/j.physrep.2011.01.002, is the standard reference for that equivalence
`[VERIFIED-ABSTRACT]`.

**Only new fact in this branch.** Discrete-time quantum walks on biological graphs have now been
run on superconducting hardware using a **symmetry-sector encoding** that trades depth for
qubits, reaching "complex graphs containing up to 17 nodes and 20 edges … utilizing 40 qubits …
with the Hellinger fidelity exceeding 87% throughout 7 steps" (arXiv:2602.24053, 2026-02-27)
`[VERIFIED-ABSTRACT]`. The encoding idea is a method choice and belongs here; the 17-node ceiling
against our 147–1058-residue benchmark is a hardware fact and belongs in file 08.

---

## 4. State transfer and spin networks — ruled out by construction, not by measurement

- **Bose**, _Phys. Rev. Lett._ **91**, 207901 (2003), doi:10.1103/physrevlett.91.207901 —
  transfer through an _unmodulated_ chain. `[VERIFIED-ABSTRACT]`
- **Christandl, Datta, Ekert & Landahl**, _Phys. Rev. Lett._ **92**, 187902 (2004),
  doi:10.1103/physrevlett.92.187902 — perfect state transfer, but only for a designed class of
  networks: "We propose a class of qubit networks that admit perfect transfer of any quantum state
  in a fixed period of time." `[VERIFIED-ABSTRACT]`
- **Pretty-good state transfer** relaxes perfection to arbitrarily-close fidelity, and the
  literature is a catalogue of graph families that admit it: double stars (arXiv:1206.0082),
  circulant graphs (arXiv:1607.03598), paths on $2^t p - 1$ vertices under the XY Hamiltonian
  (arXiv:1611.09836), graphs with an involution _given a choice of on-site potential_
  (arXiv:1702.07000). All `[VERIFIED-ABSTRACT]`.

**Why this branch is closed before it starts.** Every result here is a _design_ theorem. The
input is a target fidelity and the output is a coupling pattern — mirror-symmetric couplings,
transcendental on-site potentials, integral spectra, an isospectral reduction
(arXiv:1908.02046) `[VERIFIED-ABSTRACT]`. Our couplings are not free variables. They are fixed by
the Cβ geometry of an apo structure, and C6 says exactly that: contact topology drives
propagation. Engineering the couplings to obtain high transfer fidelity would be inventing the
answer. A protein contact graph is a generic irregular graph, and the state-transfer literature's
whole content is that generic graphs do not transfer well.

**One thing worth keeping.** The XY Hamiltonian restricted to the single-excitation sector is
exactly the CTQW generator (this is the standard equivalence, e.g. arXiv:1611.09836's model)
`[VERIFIED-ABSTRACT]`. ADR 0002's "one qubit per node, XY coupling, single-excitation sector"
framing is therefore _not_ a separate physical model from the walk — it is the same operator with
a hardware story attached. That is worth saying plainly in the report rather than presenting the
spin encoding as if it added physics.

---

## 5. Open systems — what a plain γ sweep could not have shown

`00-conventions.md` §5 item 3 records that dephasing-assisted transport had no optimum over γ from
0 to 3·J_max. That is a correct measurement and this review does not overturn it. It does supply
the **mechanism**, which the sweep could not.

**ENAQT has a precondition, and it is not the dephasing rate.** Zerah-Harush & Dubi, "Universal
Origin for Environment-Assisted Quantum Transport in Exciton Transfer Networks"
(arXiv:1801.06799):

> We show that ENAQT appears due to two competing processes, namely the tendency of dephasing to
> make the exciton population uniform, and the formation of an exciton density gradient, defined
> by **the source and the sink**. Furthermore, we find a **geometric condition on the network**
> for the appearance of ENAQT. `[VERIFIED-FULLTEXT]` (emphasis added)

and, decisively:

> So far as the symmetric linear chain is considered, **no ENAQT is observed.** However, it
> appears upon a slight modification of the system. `[VERIFIED-FULLTEXT]`

> if disorder, asymmetry or a dephasing environment are unavoidably present (which seems to be
> the case for natural photo-synthetic complexes), the intermediate coherent-dephasing regime
> delivers better performance. `[VERIFIED-FULLTEXT]`

Independently, strong ENAQT has been tied to the presence of a **mobility edge** — that is, to
localisation induced by site-energy disorder (arXiv:2012.09337) `[VERIFIED-ABSTRACT]`, and to
interactions and disorder jointly (arXiv:2005.04462) `[VERIFIED-ABSTRACT]`.

**The consequence for us.** A C6-compliant contact-graph Hamiltonian has _uniform_ on-site
energies (the diagonal is degree or zero, not a disordered site energy), and our metric has no
sink — the excitation is not absorbed anywhere. Both ingredients the mechanism requires are
absent by construction. The flat γ curve was not a null result about proteins; it was the
predicted behaviour of a model with no density gradient and no disorder. **Re-running the sweep
with a trap at the active site and heterogeneous on-site energies would test something different**
— but the on-site energies would have to come from somewhere, and the only honest sources
(residue type, burial, mass) are chemistry that C6 tells us to abstract away, or are already
captured by the contact degree.

The foundational papers, for the report: Plenio & Huelga, _New J. Phys._ **10**, 113019 (2008),
doi:10.1088/1367-2630/10/11/113019; Mohseni, Rebentrost, Lloyd & Aspuru-Guzik, _J. Chem. Phys._
**129**, 174106 (2008), doi:10.1063/1.3002335; Rebentrost, Mohseni, Kassal, Lloyd & Aspuru-Guzik,
_New J. Phys._ **11**, 033003 (2009), doi:10.1088/1367-2630/11/3/033003; Whitfield,
Rodríguez-Rosario & Aspuru-Guzik (quantum stochastic walks), _Phys. Rev. A_ **81**, 022323 (2010),
doi:10.1103/physreva.81.022323. All `[VERIFIED-ABSTRACT]` (Crossref metadata this session).

**Cost note.** Open-system dynamics is not where the classical wall is either. At N = 300 the
site-basis density matrix is 90 000 entries (1.4 MiB). A _dense_ vectorised Liouvillian would be
$N^4 = 8.1\times10^9$ entries (121 GiB), which is the only genuinely large object in this section —
and it is sparse, so Krylov integration avoids forming it. Computed this session.

---

## 6. Bosonic and vibrational encodings — question (b), answered

**Yes, this work is published, and it is recent.** This is the least-explored direction in the
repository and it is the best-matched to C6, so it gets the longest treatment.

### 6.1 The enabling algorithm

**Babbush, Berry, Kothari, Somma & Wiebe**, "Exponential Quantum Speedup in Simulating Coupled
Classical Oscillators", _Phys. Rev. X_ **13**, 041041 (2023), doi:10.1103/physrevx.13.041041
(arXiv:2303.13012). It maps Newton's equations for $2^n$ masses-and-springs onto a Schrödinger
equation generated by $\sqrt{\mathbf{A}}$, encoding displacements and momenta in the _amplitudes_
of an n-qubit state. `[VERIFIED-FULLTEXT]`

Its own stated limits are the load-bearing part:

> While providing a large quantum advantage in certain contexts, these techniques also have
> significant limitations. For example, the approach is **only efficient for computing
> particularly large or global properties** and when masses and spring constants can be computed
> in **time polylogarithmic in system size**. Another feature of our algorithm is that its
> complexity is (almost) linear in the evolution time $t$ … being efficient **only if $t$ is also
> polylogarithmic in system size**. `[VERIFIED-FULLTEXT]` (emphasis added)

Three conditions. A residue network fails all three, as shown next.

### 6.2 It has already been applied to an elastic network — a graphene sheet

**Kolotouros, Sireesh, Ferguson, Thrasher, Wallden & Michel**, "Quantum Elastic Network Models and
their Application to Graphene", arXiv:2601.05161 (v2, 2026-06-16). They name the object
**QENM** and build it on Babbush et al. `[VERIFIED-FULLTEXT]`

They are explicit that this is the natural home of protein ENMs, and they name our exact metric:

> ENMs also provide a natural framework for studying allosteric signaling; by applying a small
> perturbation to the force constants at a given network node and analyzing the resulting shift in
> the eigenvalue spectrum, one can assess which residues most strongly influence the global
> dynamics of the system. Those nodes whose perturbation produces the largest spectral response
> are identified as the most likely allosteric mediators. `[VERIFIED-FULLTEXT]`
> (their ref. [24] is Feher, Durrant, Van Wart & Amaro, _Curr. Opin. Struct. Biol._ **25**, 98
> (2014), doi:10.1016/j.sbi.2014.02.004, `[VERIFIED-ABSTRACT]`)

That paragraph describes ALPS. It is in a 2026 quantum-algorithms paper, described as the
classical thing the quantum algorithm is _motivated by_ — and the quantum algorithm does not
deliver it. Two barriers, both stated by the authors:

**Barrier 1 — the readout does not contain normal modes.**

> Traditionally, ENMs output a set of low-frequency normal modes that describe the functional
> motion of a given molecular assembly. **Extracting such normal modes is not, however, possible
> in our current description of QENM.** This necessitates exploration of alternative outputs …
> Of course, this short supply of measurable quantities — along with limitations on initial state
> preparation — means that careful experimental design is required. `[VERIFIED-FULLTEXT]`

The available observables are subset kinetic and potential energies and displacement statistics.
Our deliverable is an N × N connectivity matrix and a per-residue ranking. Those are $N$ local
numbers, i.e. exactly the "not large or global" case Babbush et al. exclude.

**Barrier 2 — they chose graphene because it is periodic.**

> In the case where atoms are structured in a **grid or a chain**, constructing this oracle
> requires simple quantum arithmetic and a small overhead in qubits, while in other cases it can
> be more complicated. In the next section, we choose graphene **due to it exhibiting a periodic
> structure**. `[VERIFIED-FULLTEXT]` (emphasis added)

Their headline number — a cm-scale graphene sheet in ~160 logical qubits — is bought entirely by
the lattice rule. A protein has no such rule.

They are also candid that the advantage largely evaporates:

> although exponential advantage is in practice unlikely, high order polynomial and
> super-polynomial advantages still have vast potential for utility in fault-tolerant quantum
> computing. `[VERIFIED-FULLTEXT]`

and that the exponential advantage in their heat-transfer application "only provides an
exponential advantage at very low temperature" `[VERIFIED-FULLTEXT]`.

### 6.3 It has already been applied to proteins — and the blocker is proved, not conjectured

**Liu, Li, Wang & Liu**, "Toward end-to-end quantum simulation for protein dynamics",
arXiv:2411.03972 (v2, 2025-04-16). This is the closest published work to our pipeline: GNM and
all-atom normal-mode models, with read-in, dynamics and read-out costed end to end.
`[VERIFIED-FULLTEXT]`

The read-out list is almost our deliverable list:

> our algorithms estimate a range of classical observables, including energy, **low-frequency
> vibrational modes**, density of states, **displacement correlations**, and optimal control
> parameters. `[VERIFIED-FULLTEXT]`

But the read-in is proved impossible in polylog:

> Coordinates of Cα atoms partially determine the molecular structure, which is usually obtained
> by structural biology research **instead of being generated by an efficient computer program**.
> Therefore, the protein structure information has **high information entropy and cannot be
> compressed with a ratio better than a constant value.** … In conclusion, the matrix A is
> **incompressibly determined by the coordinates of N atoms**, and since the number of atoms is
> N, we need to load Ω(N) bits. `[VERIFIED-FULLTEXT]`

Their workaround is QROM at $\tilde O(N)$ gates and polylog _depth_, and they are honest about
what that costs:

> we notice that our QROM and ROM share the same architecture and both require $\tilde O(N)$
> gates, but the cost of querying a ROM is generally considered as negligible in classical
> computer science research. `[VERIFIED-FULLTEXT]`

**This is the decisive asymmetry between graphene and a protein, stated by the people who did
both.** Graphene's connectivity is a _rule_, so the oracle is arithmetic. A protein's
connectivity is _data_, so the oracle is a table with Ω(N) entries — and once you have paid Ω(N)
to build the table you have already paid more than the $O(N^3) = 2.7\times10^7$ flops that
diagonalising the 300 × 300 Kirchhoff matrix costs outright.

### 6.4 The deeper problem: harmonic means Gaussian, and Gaussian means classical

Even setting read-in aside, a true continuous-variable encoding — one qumode per residue, which is
the physically honest bosonic map for C6 — hits a different wall. An elastic network is a system
of _coupled harmonic oscillators_. Its Hamiltonian is quadratic, so its evolution is a Gaussian
(symplectic) operation, and a Gaussian state under Gaussian operations with Gaussian measurements
is efficiently classically simulable: **Bartlett, Sanders, Braunstein & Nemoto**, _Phys. Rev.
Lett._ **88**, 097904 (2002), doi:10.1103/physrevlett.88.097904 `[VERIFIED-ABSTRACT]`.

The Hilbert-space size argument is a mirage here. A Fock-truncated bosonic register for N = 300
modes has dimension $d^{300}$ — $10^{90}$ at $d=2$, $10^{143}$ at $d=3$, $10^{181}$ at $d=4$
(computed this session). None of that is reachable by the dynamics, because a Gaussian state on
300 modes is fully specified by a 600 × 600 covariance matrix and a 600-vector of means. The
dimension is large and the manifold is small.

**Where bosonic encodings do win, and why it does not help us.** They win on **anharmonic**
vibrational Hamiltonians. The oscillator-qubit route reports cost $O(MN\log(1/\varepsilon))$ per
Trotter step for M vibrational modes and N electronic states — linear in modes — against classical
MCTDH which is "typically restricted in practice to systems with on the order of 10–15 vibrational
modes" (_Chem. Sci._ 2026, doi:10.1039/d5sc09606e) `[VERIFIED-FULLTEXT via WebFetch]`. The
advantage is created by the anharmonic terms. **C6 removes exactly those terms**: "the topology of
the contact network is the primary driver of signal propagation, allowing us to abstract away
specific atomic force fields" (`CHALLENGE.md` §5). The QENM authors independently flag the same
gap — "the unphysical nature of the harmonic approximation, which excludes fundamental anharmonic
terms" `[VERIFIED-FULLTEXT]`.

So the bosonic direction is a genuine dilemma, and it should be written up as one: the encoding
that fits C6's physics is the encoding C6's own simplification renders classical.

### 6.5 Boson sampling for vibronic spectra — the one hard bosonic object, and its fate

The exception to "Gaussian is easy" is _sampling_. **Huh, Guerreschi, Peropadre, McClean &
Aspuru-Guzik**, "Boson sampling for molecular vibronic spectra", _Nat. Photonics_ **9**, 615
(2015), doi:10.1038/nphoton.2015.153 `[VERIFIED-ABSTRACT]`, maps a molecule's Franck–Condon
profile onto a Gaussian boson sampler; **Hamilton et al.**, _Phys. Rev. Lett._ **119**, 170501
(2017), doi:10.1103/physrevlett.119.170501 `[VERIFIED-ABSTRACT]` is the GBS model itself. Sampling
photon-number patterns from a Gaussian state involves hafnians and is not efficiently simulable in
general (exact simulation costs exponential time in the _photon number_, arXiv:1908.08068)
`[VERIFIED-ABSTRACT]`.

Two facts close this as a route for us:

1. **It has been dequantized for the chemistry application.** Oh et al.,
   "Quantum-inspired classical algorithms for molecular vibronic spectra", _Nat. Phys._ **20**, 225
   (2024), doi:10.1038/s41567-023-02308-9 `[VERIFIED-ABSTRACT]`; see also arXiv:2507.19442, which
   asks directly "whether an actual GBS approach is required" `[VERIFIED-ABSTRACT]`.
2. **The object it computes is a vibronic transition spectrum**, not a per-residue connectivity.
   A Franck–Condon profile between two electronic surfaces has no analogue in an apo elastic
   network — there is no second surface, because C1 forbids the holo structure that would define
   one.

---

## 7. Quantum linear algebra — a hardware route to a number we already have

The challenge's own reference [11] is **Oh, Krogmeier, Schlimgen & Head-Marsden**, "Singular Value
Decomposition Quantum Algorithm for Quantum Biology", _ACS Phys. Chem. Au_ **4**, 393 (2024),
doi:10.1021/acsphyschemau.4c00018 (arXiv:2309.17391). Read in full this session.
`[VERIFIED-FULLTEXT]`

What it actually does: it takes the _classically computed_ SVD of a Lindblad propagator, dilates
the diagonal singular-value matrix into a unitary with one ancilla, and runs it. Applied to FMO
(3-site and full 7-site, "which becomes a 9 level system when a sink and a ground state are
included", using 8 qubits) and to the avian radical pair. `[VERIFIED-FULLTEXT]`

Its costs, verbatim:

> the singular value decomposition is computed classically with a complexity $\mathcal{O}(r^3)$
> where $r$ is the size of the decomposed operator. `[VERIFIED-FULLTEXT]`

> This involves transitioning from a Hilbert space of size $r$ to the Liouville space of size
> $r^2$ which also spans a larger qubit space. `[VERIFIED-FULLTEXT]`

> The total gate complexity of the SVD algorithm is therefore $\mathcal{O}(d^{2}2^{2d-1})$.
> `[VERIFIED-FULLTEXT]`

> it should be noted that the systems studied are beyond the scope of possible implementation on
> current NISQ computers. `[VERIFIED-FULLTEXT]`

**Reading.** The challenge cites this as evidence that quantum simulation helps biology. It is
better read as a warning: the algorithm's non-unitary content is obtained _classically_ at
$O(r^3)$ — the same $O(N^3)$ we would pay anyway — and the quantum part is a replay. At N = 300
the Liouville space is $r^2 = 9\times10^4$, needing $d = \lceil\log_2 9\times10^4\rceil + 1 = 18$
qubits and $O(d^2 2^{2d-1})$ ≈ $10^{13}$ gates, which is not a near-term circuit (C3). Computed
this session from their formula.

The rest of the family is the same shape:

- **HHL**, Harrow, Hassidim & Lloyd, _Phys. Rev. Lett._ **103**, 150502 (2009),
  doi:10.1103/physrevlett.103.150502 `[VERIFIED-ABSTRACT]` — returns a _state_, not a vector; the
  per-residue readout costs N measurements, which erases the speedup.
- **Quantum PCA**, Lloyd, Mohseni & Rebentrost, _Nat. Phys._ **10**, 631 (2014),
  doi:10.1038/nphys3029 `[VERIFIED-ABSTRACT]` — needs the matrix as a _density operator_ and is
  dequantized for low rank (Tang, STOC 2019, doi:10.1145/3313276.3316310) `[VERIFIED-ABSTRACT]`.
- **Sparse Hamiltonian simulation**, Berry, Ahokas, Cleve & Sanders, _Commun. Math. Phys._ **270**,
  359 (2006), doi:10.1007/s00220-006-0150-x `[VERIFIED-ABSTRACT]` — the primitive QENM and Liu et
  al. both call. Sound, but its input is the oracle §6.3 shows costs Ω(N) to build.
- **Quantum phase estimation of $\sqrt{\mathbf{A}}$** is explicitly available in the Babbush
  construction: "It is possible … to do Hamiltonian simulation with $-\sqrt{\mathbf{A}}$ given
  oracle access to $\mathbf{A}$ using quantum phase estimation … but that is less efficient than
  what we describe here." `[VERIFIED-FULLTEXT]`

**The one honest quantum framing this leaves.** QPE on the block-encoded Kirchhoff matrix returns
low-lying eigenvalues. Doing that once for $H_0$ and once per candidate residue for the stiffened
$H_i$ _is_ ALPS, executed quantum-mechanically. It computes the same number by a more expensive
route. That is a defensible **C4 hardware story for a metric chosen on classical grounds**, and it
should be presented as exactly that — not as a source of advantage.

---

## 8. Quantum optimisation — a different combinatorial framing, and it also fails

`00-conventions.md` §5 item 6 closed cooperative site selection as a QUBO: classical annealing hit
the exhaustive optimum at every size up to C(34,7). The brief asked for a _different_ framing.
There is one, it is not an energy minimiser, and it is already dequantized.

**The framing.** Gaussian boson sampling encodes a graph's adjacency matrix into a Gaussian state
so that photon-click patterns are drawn with hafnian-weighted probability, biased toward **dense
subgraphs** (Arrazola & Bromley, _Phys. Rev. Lett._ **121**, 030503 (2018),
doi:10.1103/physrevlett.121.030503) `[VERIFIED-ABSTRACT]` and **maximum weight cliques**, which is
how Banchi, Fingerhuth, Babej, Ing & Arrazola cast molecular docking, _Sci. Adv._ **6**, eaax1950
(2020), doi:10.1126/sciadv.aax1950 `[VERIFIED-ABSTRACT]`. There is also a graph-similarity feature
map, Schuld, Bromley, Banchi & Killoran, _Phys. Rev. A_ **101**, 032314 (2020),
doi:10.1103/physreva.101.032314 `[VERIFIED-ABSTRACT]`. This is genuinely a different object from a
QUBO: a sampler over subgraphs, not a minimiser over bitstrings, and it consumes the adjacency
matrix that C6 hands us.

**Why it fails, and the reason is the same one that closed the other eleven.** Oh, Liu, Alexeev,
Fefferman & Jiang, "Quantum-Inspired Classical Algorithm for Graph Problems by Gaussian Boson
Sampling", _PRX Quantum_ **5**, 020341 (2024), doi:10.1103/prxquantum.5.020341 (arXiv:2302.00536):

> The main observation from Gaussian boson samplers is that a given graph's adjacency matrix to be
> encoded in a Gaussian boson sampler is **nonnegative, which does not necessitate quantum
> interference.** … we … show that **the advantage from Gaussian boson samplers is not significant
> in general.** `[VERIFIED-ABSTRACT]` (emphasis added)

A residue contact adjacency matrix is non-negative by construction. The property that dequantizes
GBS-on-graphs is a property our input has, unavoidably. Note the mechanism is the _same_ one the
teammate diagnosed — no sign structure means no interference — arriving from photonics rather than
from spin walks. That convergence is itself worth reporting.

**And the object is wrong anyway.** A densest-k-subgraph on a contact graph is "the most tightly
packed cluster of residues". That is burial and degree, which is the failure mode ADR 0002 already
names under Known risks, and which the eigenvector-centrality collapse already demonstrated.

QAOA (Farhi, Goldstone & Gutmann) and quantum annealing (Kadowaki & Nishimori, _Phys. Rev. E_
**58**, 5355 (1998), doi:10.1103/physreve.58.5355 `[VERIFIED-ABSTRACT]`) are the standard
alternatives; both consume an Ising/QUBO objective and are therefore inside the framing item 6
already closed. Max-clique GBS remains under active development (arXiv:2605.27522, 2026-05-26,
displaced GBS for max-clique) `[VERIFIED-ABSTRACT]`, so the door is not nailed shut — but nothing
retrieved suggests the non-negativity obstruction is being removed.

---

## 9. Quantum-inspired classical methods — allowed by C4, and the strongest branch

C4 permits a quantum-inspired method that states its hardware map. Two families qualify, and one
of them is already what we do.

**Dequantization (Tang and successors).** Tang, STOC 2019, doi:10.1145/3313276.3316310
`[VERIFIED-ABSTRACT]`, and the singular-value-transformation generalisation
(arXiv:1910.05699) `[VERIFIED-ABSTRACT]`. Chia et al.'s practical study is the one to quote in the
report: the algorithms have "an exponential asymptotic speedup … but with complexity bounds that
exhibit a hefty polynomial overhead" (arXiv:1905.10415) `[VERIFIED-ABSTRACT]`. In this project
dequantization is not a method we would adopt; it is the tool that has removed the advantage from
four separate branches above (§1, §6.5, §8, and the quantum-kernel result already in
`00-conventions.md` §5).

**Tensor networks.** MPS/DMRG cost is governed by the graph's tree-width — Markov & Shi, _SIAM J.
Comput._ **38**, 963 (2008), doi:10.1137/050644756 `[VERIFIED-ABSTRACT]`. A protein contact graph
has high tree-width and 7.7–8.3 independent cycles per residue (`00-conventions.md` §5 item 8), so
it is close to the worst case for MPS. Tree-tensor-network and belief-propagation extensions to
arbitrary graphs exist but introduce uncontrolled error away from locally tree-like structure
`[UNVERIFIED — from search-result summaries, no full text landed]`. Tensor networks are not a
scorer here; they are the classical simulator that would be used to _check_ any many-body proposal.

**Coherent Ising machines and simulated bifurcation.** McMahon et al., _Science_ **354**, 614
(2016), doi:10.1126/science.aah5178 `[VERIFIED-ABSTRACT]`; Goto, Tatsumura & Dixon, _Sci. Adv._
**5**, eaav2372 (2019), doi:10.1126/sciadv.aav2372 `[VERIFIED-ABSTRACT]`. Both are physical or
algorithmic Ising solvers with a clean hardware map, which satisfies C4 cleanly. Both consume an
Ising objective, so they inherit item 6's closure.

**The branch that actually works is already in the repository.** ALPS — stiffen a residue's
neighbourhood, read the shift in the three lowest Kirchhoff eigenvalues — is a quantum-inspired
classical method by the strictest reading of C4, because the Kirchhoff matrix _is_ the CTQW
generator and the low-lying eigenvalues _are_ the walk's slowest coherent frequencies. Its
hardware map is §7's QPE route. That is a legitimate C4 story, and it is the only one in this file
backed by a measured result on our own targets.

---

## 10. Quantum biology precedent — reported honestly

`CHALLENGE.md` §2 asserts that "Quantum computers offer a unique advantage in simulating non-local
correlations and interference effects, which are analogous to how biological signals propagate."
The premise behind that sentence has been retracted by the field it came from, and the report must
say so rather than lean on it.

**Cao et al.**, "Quantum biology revisited", _Sci. Adv._ **6**, eaaz4888 (2020),
doi:10.1126/sciadv.aaz4888, read in full this session:

> This Review discusses recent work reexamining these claims and demonstrates that **interexciton
> coherences are too short lived to have any functional significance** in photosynthetic energy
> transfer. Instead, the observed long-lived coherences **originate from impulsively excited
> vibrations**. `[VERIFIED-FULLTEXT]`

> detailed analysis of the exemplar system in quantum biology — the FMO complex — shows
> **unambiguously the absence of long-lived interexciton coherence** on relevant time scales in
> this system, both at cryogenic and physiological temperatures. `[VERIFIED-FULLTEXT]`

> in a secular approximation (justified for the FMO protein …), the evolution of interexciton
> coherences **is independent of the evolution of populations**, obviously excluding a direct
> functional influence of these coherences. `[VERIFIED-FULLTEXT]`

They also close the specific escape hatch a protein-network proposal would reach for:

> no quantum mechanics/molecular mechanics based dynamic studies of the FMO protein could identify
> correlations in site energy fluctuations … it has to be concluded that correlations in site
> energy fluctuations, which would allow for long-lived interexciton coherences **are detrimental
> for the light-harvesting function**. `[VERIFIED-FULLTEXT]`

**What survives, and it is the interesting part:**

> Nature, rather than trying to avoid dissipation, **exploits it via engineering of exciton-bath
> interaction** to create efficient energy flow. `[VERIFIED-FULLTEXT]`

The lesson biology teaches is not "coherence propagates the signal". It is "structured
dissipation shapes the flow". Our C6 model has no bath and no structured dissipation, so it does
not inherit even that lesson without adding physics C6 excludes. The report should state the FMO
correction explicitly; citing 2007-era coherence claims in 2026 is a credibility risk
(`docs/FIELD.md`).

---

## 11. The five questions, answered directly

### (a) The classical-simulability trap

$e^{-iHt}$ on a 300 × 300 matrix costs $O(N^3) = 2.7\times10^7$ flops. Here is where each proposed
escape actually lands. Dimensions computed this session.

| Regime                             | Object size at N = 300                                                               | Genuinely hard?                                                        | Source                                                                                                                                            |
| ---------------------------------- | ------------------------------------------------------------------------------------ | ---------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| Single excitation, unitary         | 300-vector; $O(N^3)$ expm                                                            | **No**                                                                 | Elementary; and no exponential advantage exists for geometrically local short-time dynamics, doi:10.22331/q-2026-08-03-2182 `[VERIFIED-FULLTEXT]` |
| k excitations, **non-interacting** | Free-fermion covariance, $O(N^3)$                                                    | **No** — matchgate/Gaussian-fermion simulability                       | doi:10.1137/s0097539700377025; doi:10.1103/physreva.65.032325 `[VERIFIED-ABSTRACT]`                                                               |
| k excitations, **interacting**     | C(300,2)=4.5×10⁴; C(300,5)=1.96×10¹⁰ (292 GiB); C(300,10)=1.40×10¹⁸                  | **Yes from k ≈ 5** — and multiparticle interacting walks are universal | doi:10.1126/science.1229957 `[VERIFIED-ABSTRACT]`; dimensions computed                                                                            |
| Open system, Markovian             | ρ = 9×10⁴ entries (1.4 MiB); dense Liouvillian $N^4$ = 8.1×10⁹ (121 GiB), but sparse | **No** in practice                                                     | Computed                                                                                                                                          |
| Non-Markovian / structured bath    | Adds bath modes; cost is in the bath, not the graph                                  | Depends on bath size, not on N                                         | `[UNVERIFIED]`                                                                                                                                    |
| Disorder / ensemble averaging      | M independent runs of the above                                                      | **No** — embarrassingly parallel, linear in M                          | Elementary                                                                                                                                        |
| Bosonic, **harmonic** (Gaussian)   | 600 × 600 covariance matrix                                                          | **No** — Gaussian in/out is poly-time                                  | doi:10.1103/physrevlett.88.097904 `[VERIFIED-ABSTRACT]`                                                                                           |
| Bosonic, **anharmonic**            | $d^{300}$: 10⁹⁰ (d=2) to 10¹⁸¹ (d=4)                                                 | **Yes** — but C6 removes the anharmonicity                             | doi:10.1039/d5sc09606e `[VERIFIED-FULLTEXT via WebFetch]`; dimensions computed                                                                    |
| GBS photon-pattern sampling        | Hafnians; exact sim exponential in photon number                                     | **Formally yes, practically no** on a non-negative adjacency matrix    | arXiv:1908.08068 `[VERIFIED-ABSTRACT]`; doi:10.1103/prxquantum.5.020341 `[VERIFIED-ABSTRACT]`                                                     |
| All-atom node count (N ≈ 10⁴)      | $O(N^3)$ = 10¹² flops; Hessian 3N × 3N = 9×10⁸ entries                               | **No** — hours on a workstation, and sparse solvers do better          | Computed                                                                                                                                          |

**The one column that is genuinely hard is the one with a two-body interaction term, and nothing
in C6 supplies one.** That is the same conclusion `00-conventions.md` §5 reached; this table gives
it a number per row and a citation per row.

### (b) The bosonic question

**Answered above, §6. Yes, the work exists, and it is not encouraging.**

- The enabling algorithm is Babbush et al., _PRX_ **13**, 041041 (2023).
- It has been applied to an elastic network — arXiv:2601.05161, "Quantum Elastic Network Models",
  on a **graphene** sheet, ~160 logical qubits at cm scale, and the authors chose graphene
  explicitly "due to it exhibiting a periodic structure".
- It has been applied to **proteins** — arXiv:2411.03972, GNM and all-atom normal modes, end to
  end — and that paper _proves_ the read-in blocker: a protein's connectivity matrix "is
  incompressibly determined by the coordinates of N atoms", so loading it costs Ω(N) bits.
- The QENM paper states that normal modes cannot be extracted from the encoding at all.
- A true CV encoding is Gaussian, hence classically simulable (doi:10.1103/physrevlett.88.097904).
  Bosonic hardware wins on **anharmonic** vibrational Hamiltonians, and C6 removes the
  anharmonicity by assumption.

The direction was worth the search — it is the best physical match to C6 in the whole file, and no
one in this project had looked — but it closes on a read-in theorem and a Gaussian-simulability
theorem rather than on a benchmark.

### (c) Perturbation as the observable

Our ADR 0002 metric 5 is **not** linear response, and getting this distinction right matters.

- **First-order linear response** on a graph is the retarded Green's function
  $\chi_{ij}(t) = -i\theta(t)\langle[A_i(t),A_j(0)]\rangle$. Quantum algorithms for it exist
  (Rall, _Phys. Rev. A_ **102**, 022408 (2020), doi:10.1103/physreva.102.022408, block-encoding
  based, covering "n-time correlation functions … and dynamical linear response functions"
  `[VERIFIED-ABSTRACT]`; also arXiv:2404.01454 for n-th order susceptibilities
  `[VERIFIED-ABSTRACT]`). **For a non-interacting hopping Hamiltonian this collapses to the
  propagator**, by the same algebra that collapsed the OTOC to $4g^2(r,t)$ (item 9). Building it
  would re-derive a known negative. `[UNVERIFIED — our inference from item 9's algebra, applied to
the single-particle Green's function]`
- **ADR 0002 metric 5 is a finite change to H's parameters**, not an operator insertion: stiffen
  the edges in a residue's neighbourhood and re-diagonalise. The published home of that idea is
  the ENM literature, not the quantum literature — Feher et al., doi:10.1016/j.sbi.2014.02.004
  `[VERIFIED-ABSTRACT]`; essential site scanning, Kaynak & Bahar, _CSBJ_ **18**, 1577 (2020),
  doi:10.1016/j.csbj.2020.06.020 `[VERIFIED-ABSTRACT]`; perturbation-response scanning, e.g.
  doi:10.1021/acs.jcim.6b00775 `[VERIFIED-ABSTRACT]`. And a 2026 quantum-algorithms paper
  describes it as the natural ENM allosteric readout, verbatim in §6.2.
- **Cost.** 300 stiffened re-diagonalisations = $300 \times O(N^3) = 8.1\times10^9$ flops. Seconds
  on a laptop. Computed this session. The "cost of N re-simulations" that ADR 0002 flags as a risk
  is not a real cost at our size.

**Verdict:** metric 5 is the right observable and it is already implemented, classically, as ALPS.
No published _quantum_ perturbation-response observable was retrieved that is not either (i) the
propagator in disguise, or (ii) quantum Fisher information, which item 3 of the observable search
already closed for lack of non-Hermitian structure.

### (d) Has any quantum method been scored against an allosteric ground truth?

**Not retrieved by the recorded search.** Per ADR 0019 this is not an absence-of-prior-art claim;
it is the outcome of the queries in §12. What was found:

- **Mohtashim, Sajjan & Kais**, doi:10.1021/jacs.6c08053 (arXiv:2604.17486). ~150 proteins. Its
  validation is anecdotal, not a benchmark: "biological relevance is confirmed through recovery of
  experimentally established functional residues in **proteins kinase A and oxytocin**"
  `[VERIFIED-ABSTRACT]`. Two proteins, functional residues, no allosteric labels, no AUC, no null.
  ADR 0002's reading stands and is if anything understated.
- **Quantum transport in mitochondrial complex I** (preprint, doi:10.64898/2026.05.28.728423,
  2026): a CTQW on a structure-derived **redox-centre** network, reading pathway-level electron
  flux, validated against a conserved structural bottleneck across species `[VERIFIED-ABSTRACT]`.
  Closest thing to a quantum walk scored against a structural ground truth — but ~10 redox nodes,
  not residues, electron transfer not allostery, and not peer-reviewed.
- **DTQW on a protein–protein-interaction network** for disease-gene prioritisation
  (arXiv:2602.24053) `[VERIFIED-ABSTRACT]` — a different network and a different label set.
- **VQE for active-site _structure_** on IBM–Cleveland Clinic hardware (arXiv:2506.22677,
  _Adv. Sci._ 2026, doi:10.1002/advs.202513641): predicts peptide-fragment backbone geometry
  against RMSD, not site location, and uses no allosteric labels `[VERIFIED-FULLTEXT via
WebFetch]`.

**This is the single most important strategic fact in the file.** The field has produced no
quantum method scored against allosteric labels with a stated null. Our frozen evaluation layer
would make us the first to do so — including for a _negative_ result, which
`docs/FIELD.md` already commits us to reporting.

### (e) Quantum reservoir computing

**It needs training, and file 04 has already closed it.** QRC drives a fixed quantum system with a
_sequence_ of inputs and trains a classical linear readout; `04-hybrid-quantum-ai.md` §(c)
characterises it and concludes "QRC is not a twelfth candidate worth testing; it is the same
mechanism under a different name." Everything retrieved here agrees: the QRC corpus is temporal
machine learning — turbulence forecasting (doi:10.1063/5.0334540), entanglement witnessing
(doi:10.1126/sciadv.ady7987), NARMA-style benchmarks, and a survey framing it as a successor to
quantum feature maps (doi:10.1098/rsta.2025.0085). All `[VERIFIED-ABSTRACT]`. A static contact
graph is not a time series, and we have ~100 labelled proteins. **Nothing further is owed here;
the gap in `00-conventions.md` §5 is closed by file 04, not by this one.**

---

## What this changes for our pipeline

1. **Propagation engine — do not build a new single-particle observable.** doi:10.22331/q-2026-08-03-2182
   proves no exponential advantage exists for geometrically local short-time linear dynamics, which
   is what a contact graph plus a bounded evolution time is. This upgrades the teammate's empirical
   closure to a theorem and should be cited in the report as the reason the search stopped.
2. **ADR 0002 — accept metric 5, and record why the alternatives are closed.** Metric 5 is the only
   candidate in ADR 0002 that is neither a proximity ranker (metrics 1–2), nor degeneracy-limited
   (metric 3), nor blocked by the absence of non-Hermitian structure (metric 4). Its cost objection
   is void: 300 re-diagonalisations are 8.1×10⁹ flops. Metrics 1–4 should be demoted to ablations
   with this file cited.
3. **Report §"quantum metric" — the honest framing is quantum-inspired under C4, not quantum
   advantage.** The Kirchhoff matrix is simultaneously the CTQW generator and the GNM operator.
   Present the metric as a spectral response of the walk generator, with §7's QPE-on-block-encoded-
   Kirchhoff as the stated hardware map. Do not claim speedup. `docs/FIELD.md` trap 1 already binds
   us to this.
4. **Bosonic branch — write it up as a closed direction, with the two theorems.** This is the most
   valuable new material in the file and the only branch nobody in the project had examined. State
   the Ω(N) read-in incompressibility (arXiv:2411.03972) and Gaussian simulability
   (doi:10.1103/physrevlett.88.097904). It converts "we did not try bosonic encodings" into "we
   examined bosonic encodings and here is why they cannot work under C6" — a stronger section of the
   report than any positive result we could fabricate.
5. **Do not run an ENAQT γ sweep again without adding a sink and site-energy disorder** — and note
   that adding either requires physics C6 excludes. The flat γ curve is explained, not merely
   observed (arXiv:1801.06799).
6. **Do not implement GBS site selection.** It is a genuinely different framing from the closed
   QUBO, and it is dequantized precisely because our adjacency matrix is non-negative
   (doi:10.1103/prxquantum.5.020341).
7. **Report §"quantum biology motivation" — cite the correction.** Cao et al. 2020 retract the
   long-lived-electronic-coherence premise that `CHALLENGE.md` §2 leans on. Restating the 2007
   claim in 2026 is a scoring risk.
8. **Evaluation — claim the first-mover position.** No published quantum method has been scored
   against allosteric ground truth with a stated null. Our frozen evaluation layer makes that
   claimable, and it is claimable whether the result is positive or negative.
9. **File 08 owes three numbers this file surfaced:** the 17-node / 40-qubit DTQW hardware ceiling
   (arXiv:2602.24053); the $\tilde O(N)$-gate QROM oracle for a protein connectivity matrix
   (arXiv:2411.03972); and the $O(d^2 2^{2d-1})$ gate count of the SVD algorithm at Liouville
   dimension $N^2$ (doi:10.1021/acsphyschemau.4c00018).

---

## Method

**Databases.** arXiv API (`export.arxiv.org/api/query`), Europe PMC search and `fullTextXML`,
Crossref (`api.crossref.org/works`, used only to verify DOIs, journals, volumes and years),
arXiv HTML full text (`arxiv.org/html/`, `ar5iv.labs.arxiv.org`), PMC article pages, and
WebSearch/WebFetch for gap filling. Semantic Scholar was not attempted (rate limited per
`00-conventions.md` §3).

**Queries run (28).** arXiv: `"Gaussian boson sampling" AND "vibronic"`; `"normal mode" AND
"quantum computer" AND protein`; `"elastic network" AND quantum`; `"coupled harmonic oscillators"
AND "quantum algorithm"`; `"communicability" AND quantum AND network`; `"quantum PageRank" OR
"quantum centrality"`; `"quantum reservoir computing"`; `"linear response" AND "quantum algorithm"
AND "response function"`; `"quantum-inspired" AND "low-rank"`; `"singular value decomposition" AND
"quantum biology"`; `"Lindblad" AND "quantum algorithm"`; `"pretty good state transfer"`;
`"perfect state transfer" AND spin`; `"vibrationally assisted" AND "energy transfer"`;
`"environment-assisted quantum transport"`; `"quantum walk" AND protein`; `"Gaussian boson
sampling" AND (dequantiz OR "classical algorithm") AND graph`. Europe PMC: `"quantum walk" AND
(protein OR residue)`; `"quantum computing" AND ("normal mode" OR "elastic network" OR "Gaussian
network model")`; `allosteric AND ("quantum walk" OR "quantum algorithm" OR "quantum computing")`;
`("quantum walk" OR "quantum simulation" OR "quantum circuit") AND ("allosteric site" OR
"allosteric residue" OR "allosteric pocket")`; `"oscillator-qubit" OR ("continuous-variable" AND
vibrational AND "quantum simulation")`; `TITLE:"quantum reservoir computing"`; `"long-lived" AND
coherence AND photosynthetic AND vibrational`; `("quantum phase estimation" OR "quantum algorithm")
AND ("perturbation response" OR "spectral response" OR "eigenvalue shift")`; plus two title lookups.
WebSearch: 6 queries (budget exhausted at 200/200 for the session).

**Counts.** ~230 records returned across all queries; 41 screened in on title/abstract; **9 full
texts landed and read** — arXiv:2601.05161, arXiv:2411.03972, arXiv:2303.13012, arXiv:2505.10445,
arXiv:2309.17391, arXiv:1801.06799, PMC7124948 (Cao 2020), PMC13158693 (via WebFetch),
arXiv:2506.22677 (via WebFetch). 26 DOIs verified against Crossref this session. All Hilbert-space
dimensions, memory figures and flop counts were computed in this session with `math.comb` and
elementary counting, never recalled.

**Stopping rule.** Stopped when three independent branches (geometrically local dynamics, bosonic
CV encodings, GBS on graphs) converged on the _same_ mechanism already recorded in
`00-conventions.md` §5 — that a real, non-negative, single-particle operator supplies no
interference structure — and when no query returned a quantum method scored against allosteric
labels.

**Could not be reached.** (i) The Sakamoto & Fujii runtime constants for the dequantized algorithm:
Definition 5 and the three main results were read in full, the explicit polynomial in Theorem 1 was
not extracted. (ii) The QENM supplementary complexity tables. (iii) Full text of the mitochondrial
complex I preprint (not open access). (iv) Full text of Mohtashim et al. (_JACS_, not open access);
the arXiv preprint abstract was used. (v) Tensor-network tree-width behaviour on protein contact
graphs specifically — no full text landed, and the claim in §9 is tagged `[UNVERIFIED]`.
(vi) arXiv rate-limited (HTTP 429) for roughly 20 minutes mid-session; 12 planned arXiv queries
were dropped and replaced by Europe PMC and Crossref equivalents.
