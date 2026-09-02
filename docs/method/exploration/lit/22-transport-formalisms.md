# Transport and propagation formalisms on graphs and elastic networks

**Scope:** the mathematics of moving something across a weighted graph — heat, current,
probability, mass, information — mined for **observables computable on a residue contact
graph**. Each formalism is given as a formula, with what it demands of the operator, its
cost at N = 150–1100 nodes, and whatever published evidence exists that it marks a
functional site in a protein. It deliberately excludes the _phenomenon_ of allostery (what
physically carries the signal, pathway-versus-ensemble, the exponential decay law) and it
excludes circuit construction, hardware mapping and evaluation protocol.
**Sibling files:** `../../review/00-conventions.md` (rules, the six constraints, the eleven
quantum insertion points already closed by measurement, the four bars a method must clear);
`../../review/06-signal-propagation-physics.md` (the physics this file is instrumented for —
read it first, this file is the toolbox and that one is the specification).
**Retrieved:** 2026-08-26.

---

## 0. The discriminator, stated once

Our problem is not "rank residues by importance". It is **"rank residues by dynamic
connectivity to a named source set S"**, where S is the apo active site and is given to us
(`CHALLENGE.md` §4.1). That single clause eliminates most of the graph-theory literature
before any of it is evaluated, because most graph observables are **source-free**: they are
a property of node _i_ alone, so they return the same ranking whatever question is asked of
the protein. Degree, betweenness, closeness, k-core index, eigenvector centrality, subgraph
centrality, the heat-kernel signature, both Ricci curvatures and the von Neumann entropy are
all source-free in their published form.

A source-free observable can still be useful — as a node weight, as a prior, as a control —
but it cannot be the primary readout, because it does not know where the active site is.
Every formalism below is tagged **source-conditioned** or **source-free**, and where a
source-free quantity has a natural source-conditioned relative, that relative is named.

A second discriminator runs underneath the first. Most of what follows is a **matrix
function of the operator, read at a source column**:

| Object                                       | Walk-length weight                 | Read at    |
| -------------------------------------------- | ---------------------------------- | ---------- |
| Heat kernel `exp(−tL)`                       | Poisson, `t^k e^{−t}/k!`           | `[·]_{Si}` |
| Communicability `exp(A)`                     | `1/k!`                             | `[·]_{Si}` |
| Katz / personalised PageRank `(I − cA)^{−1}` | geometric, `c^k`                   | `[·]_{Si}` |
| Resolvent Green's function `(zI − H)^{−1}`   | geometric                          | `[·]_{Si}` |
| CTQW `exp(−iHt)`                             | Poisson with a phase, `(−it)^k/k!` | `[·]_{Si}` |

They differ only in how they weight walks of length k. The last row is the transfer
amplitude that `00-conventions.md` §5 records as closed by measurement — a proximity ranker
correlating −0.60 to −0.71 with distance. **Any new member of this family inherits that
result.** Adding another `f(A)` is not a new observable; it is a reweighting. This file
therefore separates, at every step, the reweightings from the genuinely different
constructions: hitting-time asymmetry, min-cut, rigidity, spectral-determinant response, and
local conductance. Those five are the only things here that are not `f(A)_{Si}`.

**A cost note that applies to everything below and is stated once.** A dense symmetric
eigendecomposition, a dense matrix exponential, a dense pseudoinverse and a dense Cholesky
are all O(N³). At N = 1100 that is ≈ 1.3 × 10⁹ flops, well under a second in LAPACK; at
N = 150 it is instantaneous. **Nothing in this file is compute-limited at our sizes.** Where
the literature warns that a method is expensive (repeatedly, for Ollivier-Ricci curvature),
the warning is calibrated to N ≳ 10⁵ and does not transfer to us. The binding constraint on
every choice below is _information_, never _cost_. That is worth saying plainly in the
report, because C3 requires a resource statement for quantum methods and the honest
comparison is that the classical side of this problem costs nothing.

---

## 1. Heat kernel and diffusion on graphs

### 1.1 The heat kernel

**Definition.** For a weighted graph with adjacency `A`, degree `D = diag(A1)` and
combinatorial Laplacian `L = D − A`, the heat kernel is

```
H_t = exp(−tL) = Σ_k e^(−λ_k t) φ_k φ_kᵀ ,      L φ_k = λ_k φ_k
```

`[H_t]_{ij}` is the amount of heat at j at time t after a unit impulse at i. It solves
`∂u/∂t = −Lu`. The normalised variant uses `𝓛 = I − D^(−1/2) A D^(−1/2)`.

**Operator requirement.** `L` symmetric positive semidefinite. Any symmetric non-negative
`A` gives one. `H_t` is row-substochastic for the random-walk Laplacian and doubly
non-negative for the combinatorial one; **all entries are non-negative**, which is the
structural difference from `exp(−iHt)`, whose entries carry a sign and therefore interfere.

**Cost.** One eigendecomposition, O(N³), then any t is free. Or `expm_multiply` on a sparse
`L` for a single column: O(|E| · s) with s the number of Krylov steps. At N ≤ 1100, free.

**Source-conditioned?** Yes, when read as `Σ_{p∈S} [H_t]_{pi}` — "heat arriving at i from the
active site by time t". This is a legitimate source-conditioned observable and it is the
diffusive sibling of the CTQW transfer amplitude.

**C1 / C2 / C6.** C1-OK, C2-OK, C6-OK — topology only.

### 1.2 The auto-diffusivity function and the heat-kernel signature (HKS)

**Definition.** The auto-diffusivity function is the **diagonal** of the heat kernel:

```
k_t(i,i) = [exp(−tL)]_{ii} = Σ_k e^(−λ_k t) φ_k(i)²
```

The HKS of Sun, Ovsjanikov & Guibas is the vector `{k_t(i,i)}` sampled over a logarithmic
grid of t. The paper proves that "under certain mild assumptions, HKS captures all of the
information contained in the heat kernel and characterizes the shape up to isometry"
[VERIFIED-ABSTRACT] (doi:10.1111/j.1467-8659.2009.01515.x). Small t probes local geometry
(on a manifold, `k_t(i,i)` expands in the scalar curvature); large t is dominated by the
Fiedler mode.

**Operator requirement.** Same as §1.1.

**Cost.** Free once eigenvectors are in hand. Practically 10–20 time samples per residue.

**Source-conditioned?** **No — it is a diagonal.** HKS is the shape-analysis analogue of
"how central and how buried is this residue", and its large-t limit is `φ_1(i)²`, i.e.
squared eigenvector centrality. That is bar #3 in `00-conventions.md` §6 and a CTQW already
reproduces it.

**Published protein evidence.** One direct application retrieved: a "ten-point heat-kernel
signature" combined with Laplace–Beltrami eigenvalues on **ligand-aware** protein surfaces
predicted binding affinity comparably to docking [VERIFIED-ABSTRACT]
(doi:10.3390/molecules31111899, PMC13258241). "Ligand-aware" makes that construction
**C1-FAIL as published** — the surface is defined using the ligand. The descriptor itself is
reusable on an apo surface. Two studies from one group applied heat-kernel analyses to
protein energetic networks to study allostery in p53-DBD and in PDZ [VERIFIED-ABSTRACT]
(doi:10.3390/ijms26146884, PMC12295982; doi:10.1021/acs.jpcb.2c06546, PMC9884075), but both
build the network from MD-derived energetics, so both are **C2-FAIL as published**; the heat
kernel itself is not.

**Limitation, from the shape literature and directly relevant here.** HKS and the wave-kernel
signature "exhibit sensitivity to mesh connectivity, sampling patterns, and topological
noise" [VERIFIED-ABSTRACT] (arXiv:2503.03907). A residue contact graph built with a cutoff
is exactly a connectivity-sensitive discretisation. A retrieval audit found that for these
descriptors "short scales dominate retrieval performance while long scales are harmful"
[VERIFIED-ABSTRACT] (arXiv:2606.07791) — i.e. the informative content is local, which is the
regime where degree and burial already live.

### 1.3 Diffusion distance and diffusion maps

**Definition.** With the random-walk operator `P = D^{−1}A` having right eigenvectors `ψ_k`
and eigenvalues `μ_k`, the diffusion distance at scale t is

```
D_t(i,j)² = Σ_{k≥2} μ_k^(2t) (ψ_k(i) − ψ_k(j))²
```

Coifman & Lafon prove this **is a metric**, equal to the Euclidean distance in the diffusion
coordinates `Ψ_t(i) = (μ_2^t ψ_2(i), μ_3^t ψ_3(i), …)`, and that it aggregates all paths
between two points rather than one shortest path [VERIFIED-ABSTRACT]
(doi:10.1016/j.acha.2006.04.006). The heat-kernel version substitutes `e^{−λ_k t}` for
`μ_k^t`.

**Operator requirement.** `P` row-stochastic, reversible (guaranteed by symmetric `A`),
non-negative.

**Cost.** One eigendecomposition; all t and all pairs then free. O(N³) once.

**Source-conditioned?** Yes, as `min_{p∈S} D_t(p,i)` or `D_t(S̄, i)` with `S̄` the source
centroid in diffusion coordinates. This is a **metric on the graph that is not graph
distance** — the one property that makes it worth testing against the `−distance` control,
because it is the only member of the family with a triangle inequality and a scale parameter
at the same time.

**C1 / C2 / C6.** C1-OK, C2-OK, C6-OK.

**Published protein evidence.** Not retrieved by the recorded search for residue-level
allosteric-site prediction. Recorded as "not retrieved", not as absent (ADR 0019).

### 1.4 The wave-kernel signature (WKS)

**Definition.** WKS replaces the heat semigroup with the Schrödinger propagator. For a
log-normal energy filter `f_e` centred on log-energy e,

```
WKS(i, e) = C_e Σ_k φ_k(i)² f_e(λ_k)²
```

It is band-pass in the spectrum where HKS is low-pass. Both are members of the parametric
spectral-descriptor family formalised by Bronstein [VERIFIED-ABSTRACT] (arXiv:1110.5015);
"HKS and WKS exhibit distinct scale dependence patterns" [VERIFIED-ABSTRACT]
(arXiv:2606.07791).

**Verdict for us — negative, and it matters.** `Σ_k φ_k(i)² f(λ_k)` is a **filtered inverse
participation ratio**. `00-conventions.md` §5 item 5 records eigenvector content and mode IPR
already measured at 63.6 % and 36.4 % against a 90.9 % bar. WKS is the same object with a
smoother window. Source-free. **Do not build it.** C1-OK, C2-OK, C6-OK, but pre-refuted.

---

## 2. Effective resistance, commute time, hitting time, random walk with restart

Let `L⁺` be the Moore–Penrose pseudoinverse of `L`, `d_i` the weighted degree, and
`vol(G) = Σ_i d_i`.

### 2.1 Effective resistance (resistance distance)

```
R_eff(i,j) = L⁺_ii + L⁺_jj − 2 L⁺_ij
```

Klein & Randić established that if fixed resistors are assigned to each edge of a connected
graph, "the effective resistance between pairs of vertices is a graphical distance", and
proved theorems about this distance function [VERIFIED-ABSTRACT] (doi:10.1007/BF01164627).
**It is a metric.** On a distance-regular network it is a strictly increasing function of
shortest-path distance [VERIFIED-ABSTRACT] (arXiv:0705.2480) — a warning that on a
near-lattice graph it will collapse onto the `−distance` control.

**Operator requirement.** `L` symmetric PSD, graph connected (else use per-component `L⁺`).
Non-negative edge weights required for the electrical interpretation.

**Cost.** One pseudoinverse, O(N³). All pairs then free.

**Source-conditioned?** Yes, as `R_eff(S, i)` with the source set shorted into a single node
(the electrical operation is literally shorting: merge the rows and columns of S). Shorting
is exact and is one line of index arithmetic.

**C1 / C2 / C6.** C1-OK, C2-OK, C6-OK.

**Quantum hook, honestly sized.** A benchmark of the "full and reduced effective resistance
kernel for molecular classification" reports a "quadratic improvement in time complexity over
classical approaches" for kernel calculation on a quantum device [VERIFIED-ABSTRACT]
(arXiv:2501.19352, doi:10.1109/qCCL65142.2025.11158790). A quadratic speedup on an O(N³)
operation that already takes under a second at N = 1100 buys nothing. Record it as a C4
mapping that exists, not as a reason to use it.

### 2.2 Commute time

```
C(i,j) = H(i→j) + H(j→i) = vol(G) · R_eff(i,j)
```

Chandra, Raghavan, Ruzzo, Smolensky & Tiwari proved the identity `C(u,v) = 2m·R_uv` for
unweighted graphs with m edges, and bounded the cover time by `mR < cover < O(mR log n)`
[VERIFIED-ABSTRACT] (doi:10.1007/BF01270385). Commute time **is a metric** — it is `vol(G)`
times a metric.

**Verdict.** Commute time carries **exactly the information in effective resistance** and no
more. Reporting both is reporting one thing twice.

### 2.3 Hitting time — the asymmetric one

```
H(i→j) = Σ_k d_k ( L⁺_ik − L⁺_ij − L⁺_jk + L⁺_jj )
```

[UNVERIFIED] for the exact index form — this is standard algebra, and it was checked here by
summing `H(i→j) + H(j→i)`, in which the `L⁺_ik` and `L⁺_jk` terms cancel and the remainder is
`vol(G)(L⁺_ii + L⁺_jj − 2L⁺_ij) = vol(G)·R_eff(i,j)`, reproducing §2.2. Laplacian
pseudoinverses are confirmed as the standard route to "the hitting/commuting times for a
Markov chain" [VERIFIED-ABSTRACT] (arXiv:2109.14587).

**Hitting time is not a metric and not symmetric.** `H(i→j) ≠ H(j→i)` on an undirected graph,
because the walk's stationary measure `π_i ∝ d_i` weights the two directions differently. The
asymmetry comes from **degree heterogeneity, not from non-reciprocal hopping.**

**This is the single most consequential finding in this file.** `06-signal-propagation-physics.md`
§10 and `00-conventions.md` §5 item 11 both record that a unitary walk on a real symmetric
contact graph cannot be directional, and that our required N×N connectivity matrix is
therefore symmetric while the biology is anisotropic by at least sixfold. A **random-walk
hitting time on the same symmetric graph is directional at no extra cost and with no extra
assumption.** It does not need a lag parameter, a source/sink pair, or an entropy production
term.

**Practical form for us.** Absorb at the whole source set. Delete the rows and columns of S
from the row-stochastic `W = D⁻¹A` to get `W_R`, then

```
h(i → S) = [ (I − W_R)^(−1) 𝟙 ]_i
```

One dense solve, O(N³). Ten lines of code.

**Published protein evidence — strong, and with a numerical trap in it.** Chennubhotla &
Bahar built a discrete-time Markov process on a residue affinity network with
`m_ij = a_ij / d_j`, `d_j = Σ_i a_ij`, and inter-residue affinities from atom–atom contacts
at a 4 Å cutoff normalised by residue size; they measured communication by hit and commute
times and found that "functionally active residues are found to possess enhanced
communication propensities, evidenced by their short hit times", with catalytic residues
sitting in communication minima across five enzymes (1bk9, 1a30, 1br6, 1cqq, 1bvv), and
α-helices acting as efficient mediators [VERIFIED-FULLTEXT] (PMC1988854,
doi:10.1371/journal.pcbi.0030172).

The trap, and it is decision-relevant. For phospholipase A2 they report broadcast hitting
times `⟨H_b(i)⟩ = 340.3 ± 1.5` against receive times `⟨H_r(j)⟩ = 340.3 ± 124.8`
[VERIFIED-FULLTEXT] (PMC1988854). **Same mean, variance eighty times larger in one
direction.** The near-constancy of the broadcast mean is Kemeny's constant: the expected
hitting time from any start node to a target drawn from the stationary distribution is
independent of the start node, and equals `Σ 1/λ_i` over the non-zero Laplacian eigenvalues
[VERIFIED-ABSTRACT via retrieved summaries of arXiv:2412.11160 and arXiv:2409.05471];
[UNVERIFIED] for the identification of Bahar's ±1.5 with Kemeny's constant, which is
inference. The operational consequence is unambiguous: **rank by `h(i → S)`, never by
`h(S → i)`.** The broadcast direction is a constant plus noise by a theorem.

**C1 / C2 / C6.** C1-OK, C2-OK, C6-OK. **Source-conditioned: yes, and directionally.**

### 2.4 Random walk with restart / personalised PageRank

**Definition.** With restart probability α and personalisation vector `s` (uniform on the
named source set S),

```
p = α ( I − (1−α) A D^(−1) )^(−1) s
```

equivalently the fixed point of `p = α s + (1−α) A D⁻¹ p`. This is a **resolvent**, i.e. the
geometric-weighted walk sum; the heat-kernel PageRank of Chung is the Poisson-weighted
counterpart, `exp(−t(I − W))` seeded at S [VERIFIED-ABSTRACT] (doi:10.1073/pnas.0708838104).

**Operator requirement.** `W` column- or row-stochastic, non-negative. Not Hermitian, but
similar to a symmetric matrix under `D^{1/2}` for reversible chains.

**Cost.** One sparse solve or ~50 power iterations. Milliseconds.

**Source-conditioned?** **Yes, by construction — this is the cleanest source-conditioned
member of the whole family.** `s` _is_ the active site.

**Not a metric.** `p_i` is a probability mass, asymmetric in the same degree-driven way as
hitting time.

**C1 / C2 / C6.** C1-OK, C2-OK, C6-OK.

**Published protein evidence.** Retrieved applications of PPR/RWR in biology are at the
level of drug–protein heterogeneous graphs [VERIFIED-ABSTRACT] (arXiv:2204.08206), not
residue graphs. Residue-level RWR seeded on an active site was **not retrieved by the
recorded search**. Note that a unified randomised algorithm exists computing PPR, heat-kernel
PageRank and Katz under one bounded-error guarantee [VERIFIED-ABSTRACT]
(arXiv:2106.03058, doi:10.1145/3447548.3467243) — useful if we want the three walk-weightings
as a family sweep rather than three implementations.

### 2.5 Current-flow (random-walk) betweenness

Newman's measure scores a node by the total electrical current through it when unit current
is injected and extracted over all source–sink pairs [VERIFIED-ABSTRACT]
(doi:10.1016/j.socnet.2004.11.009). Source-free **as published**, because it averages over
all pairs. The source-conditioned restriction — inject at S, extract at i, score the
intermediate residues — is a one-line change and is the correct form for us. It is a
`L⁺`-based quantity, so it costs one pseudoinverse. C1-OK, C2-OK, C6-OK.

Betweenness in its shortest-path form is already the field's default: an RIN package reports
"degree, closeness, and betweenness", with the highest-betweenness residues taken as putative
allosteric sites [VERIFIED-ABSTRACT] (doi:10.1021/acs.jcim.6c00004); a machine-learning study
of DNA-binding protein drug sites found "binding sites with high betweenness value and high
closeness value are more likely to interact with drugs" [VERIFIED-ABSTRACT]
(doi:10.3389/fbioe.2022.822392, PMC9065339). Both are source-free and both are the "buried
and central" detector that `docs/FIELD.md` §3 warns is what most methods actually find.

---

## 3. Discrete curvature on graphs

### 3.1 Ollivier-Ricci curvature

**Definition.** For an edge (x,y), with `m_x` the one-step (optionally lazy) random-walk
measure at x and `W₁` the 1-Wasserstein / earth-mover distance,

```
κ(x,y) = 1 − W₁(m_x, m_y) / d(x,y)
```

Ollivier defines coarse Ricci curvature "in terms of how much small balls are closer (in
Wasserstein transportation distance) than their centers are", as "a local contraction
coefficient of the random walk acting on the space of probability measures"
[VERIFIED-ABSTRACT] (doi:10.1016/j.jfa.2008.11.001). Node curvature is the weighted mean over
incident edges. Each edge requires solving one optimal-transport linear programme
[VERIFIED-ABSTRACT] (arXiv:1909.12156).

**Operator requirement.** A non-negative stochastic kernel and a base metric `d`. Not
Hermitian, not a Laplacian — this is genuinely outside the `f(A)` family.

**Cost — and the literature's warning does not apply to us.** Multiple papers call
Ollivier-Ricci "prohibitively high computational complexity" and propose cheaper surrogates:
a Jaccard-metric approximation [VERIFIED-ABSTRACT] (arXiv:1710.01724), an "Effective
Resistance Curvature" that "significantly outperforms Ollivier-Ricci curvature in
computational efficiency" [VERIFIED-ABSTRACT] (arXiv:2511.01443), and a Lower Ricci Curvature
with "linear computational complexity" [VERIFIED-ABSTRACT] (PMC13021251). Those are
calibrated to N ≳ 10⁵. A residue graph at an 8 Å Cα cutoff has |E| ≈ 8N ≈ 8 800 edges at
N = 1100 and mean degree ≈ 15, so each LP is a ~15 × 15 transport problem. Total: seconds.
[UNVERIFIED] — this is an arithmetic estimate from the retrieved degree statistics, not a
benchmark.

**Interpretation, and why it is the right shape of idea.** Negative curvature marks a
bottleneck. In graph neural networks, "positive graph curvature" correlates with
over-smoothing and "negative graph curvature" correlates with **over-squashing** — the
failure mode in which information from a large neighbourhood must funnel through a narrow
edge [VERIFIED-ABSTRACT] (arXiv:2211.15779). Bounded-degree graphs with non-negative
Ollivier-Ricci curvature have subexponential growth and a **diffusive** rather than
super-diffusive random walk [VERIFIED-ABSTRACT] (arXiv:2512.03968). Lower curvature bounds
constrain the normalised Laplacian spectrum [VERIFIED-ABSTRACT] (arXiv:1105.3803). So
curvature is not independent of the spectral quantities in §7 — it bounds them.

**Source-conditioned?** **No.** Curvature is an edge or node property. The source-conditioned
relative is "the minimum edge curvature along the S→i flow", which is a construction of ours,
not a published observable.

**Published protein evidence.** Direct and recent: discrete Ricci curvature on Cα contact
graphs as a fold descriptor. A 22-dimensional feature from summary statistics and quantiles of
Ollivier-Ricci and Forman-Ricci edge-curvature distributions "already outperforms mean-pooled
ESM-2 on both datasets" (CATH top-10 topology, ASTRAL-40 % SCOPe top-10 fold), using "3.4 % of
the ESM-2 baseline dimensionality", reaching macro-F1 0.71 (CATH) and 0.68 (SCOPe) when
combined with persistent homology at 112 dimensions [VERIFIED-ABSTRACT] (arXiv:2607.16553).
That is **fold classification, not site prediction** — it shows the descriptor carries protein
structural information, not that it localises function. Ollivier persistent Ricci curvature has
been used for protein–ligand binding-affinity featurisation on PDBbind [VERIFIED-ABSTRACT]
(arXiv:2011.10281), and a curvature-enhanced GCN reached state-of-the-art on 13 of 14
biomolecular interaction datasets [VERIFIED-ABSTRACT] (doi:10.1016/j.csbj.2024.02.006,
PMC10904164) — both supervised and both trained on complexes, hence **C1-FAIL as published**
for our use, though the curvature feature itself is C1-clean. In omics networks, an
open-source Ollivier-Ricci tool is explicitly framed as measuring **robustness**
[VERIFIED-ABSTRACT] (doi:10.1093/bioinformatics/btaf093, PMC11893153), and curvature residuals
"reveal bridge nodes between communities" [VERIFIED-ABSTRACT]
(doi:10.1038/s41598-026-42823-2, PMC13077092).

**No application of Ollivier-Ricci curvature to allosteric-site prediction on a residue
contact graph was retrieved by the recorded search.** Per ADR 0019, recorded as not
retrieved.

**C1 / C2 / C6.** C1-OK, C2-OK, C6-OK. Source-free.

### 3.2 Forman-Ricci curvature — and a decisive negative result

**Definition.** Forman's discretisation, adapted to networks by Sreejith, Mohanraj, Jost,
Saucan & Samal for undirected weighted and unweighted graphs, weights the edge and its two
endpoint nodes and subtracts a sum over parallel edges [VERIFIED-ABSTRACT]
(doi:10.1088/1742-5468/2016/06/063206, arXiv:1603.00386).

**On an unweighted graph it reduces to**

```
F(e = uv) = 4 − deg(u) − deg(v)
```

[UNVERIFIED] — this is the standard reduction with unit node and edge weights; the general
weighted formula is the verified one. **If the reduction holds, Forman curvature on an
unweighted contact graph is a pure function of two degrees and adds nothing whatsoever
beyond degree.** That is a clean and cheap thing for us to check in code before spending any
effort on it, and it is the reason Forman is ranked below Ollivier here despite being ~1000×
cheaper.

On a **weighted** graph it becomes degree-plus-weights, which is slightly more than degree but
still local. Forman curvature has been used as an attention weight in a drug–target affinity
GNN with a claimed 22.5 % reduction in cold-start prediction error [VERIFIED-ABSTRACT]
(doi:10.1016/j.jmgm.2025.109170, PMID 40966797), and in SIR models where "scale-free and
clustered networks exhibit strongly negative curvature around hubs" [VERIFIED-ABSTRACT]
(doi:10.20944/preprints202509.1630.v1) — note that this last sentence is itself the statement
that Forman curvature is a hub detector.

**C1 / C2 / C6.** C1-OK, C2-OK, C6-OK. Source-free. **Low priority.**

---

## 4. Non-equilibrium and anomalous transport

This is the section where the C2 verdict actually separates methods, so each entry states it
explicitly.

### 4.1 Energy-exchange networks and CURP — **C2-FAIL as published**

Ishikura, Iwata, Hatano & Yamato built CURP ("CURrent calculation for proteins") for "the flow
analysis of physical quantities within thermally fluctuating protein media", and applied it to
the PDZ domain of PSD-95, finding that structural elements essential for binding remain
critical to the energy-exchange network despite minimal structural change [VERIFIED-ABSTRACT]
(doi:10.1002/jcc.23989). The observable is an inter-residue energy current computed from the
**instantaneous forces and velocities along an MD trajectory**. Leitner & Yamato's review
frames the energy-exchange network as a way to identify "residues and protein regions involved
in the allosteric transition" [VERIFIED-ABSTRACT] (doi:10.1007/s12551-020-00661-0, PMC7242592).

**Verdict: C2-FAIL.** It needs a trajectory. C1-OK, C6-partially (it uses the force field, not
just topology). Source-conditioned: yes — the current is defined between a source and the rest.
**What survives without the trajectory is §4.2.**

### 4.2 The harmonic communication map — **C2-OK, and this is the one to take**

Yamato & Laprévote state that the communication map is built from "the harmonic approximation
of the heat current operator", formulated on the Hessian obtained by energy minimisation, and
that the method requires **only a structure and force constants, not an MD trajectory**;
crucially, "energy transport pathways observed in PYP by the communication map analysis were in
good agreement with those obtained via the Green–Kubo formalism with equilibrium MD
simulation" [VERIFIED-FULLTEXT] (PMC6976091, doi:10.2142/biophysico.16.0_322).

That single sentence is the licence for the whole approach: **a harmonic, topology-plus-force-
constant calculation reproduces the trajectory-derived energy-transport map on at least one
allosteric protein.** It is the C2-clean route to a quantity the trajectory methods compute the
expensive way. The retrieved text does not give the explicit inter-residue conductivity formula
[VERIFIED-FULLTEXT, formula not present], which is a gap: we would need the primary Leitner
reference to implement it exactly.

**C1-OK, C2-OK, C6-OK** (force constants inside the elastic-network hypothesis). **Source-
conditioned: yes.**

### 4.3 Non-equilibrium propagation on an elastic network — **C2-OK, directly usable**

Wang et al. propose exactly the construction we need. Excite one named residue with a unit
displacement, integrate the ENM equation of motion

```
d²(ΔR)/dt² = −(γ/m) Γ ΔR ,   solved in normal-mode space as
ΔR(t) = Σ_k U_k (U_kᵀ ΔR(0)) cos(ω_k t) ,   ω_k = √(γ Λ_kk / m)
```

and record which residues cross a fluctuation-amplitude threshold and when. **No MD is
required**; the method is "non-equilibrium dynamics in the normal modes space of ENM"
[VERIFIED-FULLTEXT] (PMC6015066, doi:10.1038/s41598-018-27745-y).

Results: myosin (680 residues, 1MMA) excited at Asn127 in the ATP site gives 56 energy-excited
residues in 11 clusters along two pathways — ATP site → 50 kDa cleft via the transducer, and
ATP site → converter via the lever-arm interface. PDZ3 (97 residues, 1BE9) excited at His372
gives 32 residues in 5 clusters along `His372 → βB → βE-α2 loop → βC → βD`
[VERIFIED-FULLTEXT] (PMC6015066).

**Three things make this the most directly transplantable method in this file.** (i) It is
source-conditioned on a **named binding-site residue**, exactly our input contract. (ii) It is
C1-OK provided the named source is the _active_ site, which we are given; naming a
ligand-derived allosteric site instead would be C1-FAIL. (iii) It is the **conservative
(undamped) limit**, which `06-signal-propagation-physics.md` §3–§4 says is the _wrong_ regime —
protein VET at 310 K is diffusive, `⟨x²(t)⟩ ∝ t`. Adding a damping term to the same equation
interpolates between this and §1.1's heat kernel, and that interpolation is a one-parameter
family we can sweep. **Note the warning in `00-conventions.md` §5 item 3: a dephasing sweep
γ ∈ [0, 3J_max] has already been tested and showed no optimum.** The distinction is that ENAQT
was swept on a _unitary_ propagator's transfer amplitude; this is a sweep on a _displacement-
threshold arrival time_, which is a different readout. Weak distinction. Flag as a hypothesis.

**C1-OK (with the source-set caveat), C2-OK, C6-OK. Source-conditioned: yes.**

### 4.4 Fourier law versus anomalous diffusion — proteins are subdiffusive, and it is computable

**Proteins are fractal-like and their vibrational dynamics are anomalous, and this follows from
the elastic network alone.** Reuveni, Granek & Klafter solved a master equation for random
walkers on the protein fold across **512 PDB structures** and report that "for most proteins
d_s < 2", so that the return probability `P₀(t)` "decays much slower than one would have
naively expected", with `P₀(t) ~ t^(−(3−d_s)/2)` at intermediate times; they state that "the
only information required to implement the method is the knowledge of the native structure
obtained from the PDB" [VERIFIED-FULLTEXT] (PMC2922288, doi:10.1073/pnas.1002018107). **No MD.
Gaussian network model on the native structure.**

Independently, Morita & Takano characterised residue contact networks in native structures as
fractal rather than small-world, reporting "universally" `D_c ≈ 1.9`, `D_f ≈ 2.5` and
`d_s ≈ 1.3`, and concluding that "the residue contact networks in the protein native structures
belong to the universality class of three dimensional percolation cluster"
[VERIFIED-ABSTRACT] (arXiv:0809.4876, doi:10.1103/PhysRevE.79.020901). Burioni, Cassi, Cecconi
& Vulpiani computed the GNM harmonic spectrum and its spectral dimension and found a strong
correlation with protein length [VERIFIED-ABSTRACT] (arXiv:q-bio/0405010). Granek & Klafter
showed that fractons — the vibrational excitations of a fractal — make distance
autocorrelations decay anomalously, crossing over from near-stretched-exponential to a slow
algebraic decay [VERIFIED-ABSTRACT] (doi:10.1103/PhysRevLett.95.098106).

**What this gives us as an observable.** `d_s` is read off the log-log slope of the
auto-diffusivity `k_t(i,i)` (§1.2), because `Σ_k e^{−λ_k t} ∼ t^{−d_s/2}` when
`g(ω) ∼ ω^{d_s−1}`. A **local** spectral dimension `d_s(i)`, fitted from the slope at residue
i, is therefore a free by-product of the heat kernel and measures how anomalous the transport
is _at that residue_. It is a slope, not a value, so it is not a monotone transform of the
transfer amplitude. Source-free; the source-conditioned relative is the slope of
`Σ_{p∈S}[H_t]_{pi}` in t.

A formal machinery exists for putting sub- and superdiffusion on a graph directly: Diaz-Diaz &
Estrada's generalised diffusion equation uses "fractional-time derivatives and transformed
d-path Laplacian operators on graphs/networks", solved analytically, and "covers the regimes of
normal, sub- and superdiffusion as a function of the two parameters of the model"
[VERIFIED-ABSTRACT] (arXiv:2202.00318, doi:10.1016/j.chaos.2022.111791). Two parameters, closed
form, computable from `L`. That is a defensible way to make the propagator match the measured
transport class instead of asserting it.

**C1-OK, C2-OK, C6-OK throughout §4.4.**

### 4.5 Bottlenecks in energy transport — a published, protein-specific claim

Poudel, Wales & Leitner mapped the vibrational energy landscape of β₂AR with disconnectivity
graphs and identified "prolines and glycines ... as bottlenecks to energy transport", with
alternative pathways emerging via noncovalent contacts, and found first-passage-time
distributions differing strikingly between active and inactive states [VERIFIED-ABSTRACT]
(doi:10.1021/acs.jpcb.4c04513). Reid & Leitner report that in hemoglobin, "channels for facile
energy transport ... lie along pathways that experiments reveal are important in allosteric
processes" [VERIFIED-ABSTRACT] (doi:10.1007/978-1-0716-1154-8_4).

Both are MD-based — **C2-FAIL as published** — but the _claim_ they support is the one §3 and
§6 are trying to instrument: **energy transport in proteins has identifiable bottlenecks, and
the bottlenecks are chemically specific (Pro, Gly) rather than purely topological.** That is an
argument for weighting edges by residue class, which
`06-signal-propagation-physics.md` §12 already ranks as the highest-value change to the graph.

---

## 5. Master-equation / Markov propagation on an elastic network

### 5.1 Chennubhotla-Bahar Markov propagation

Covered in §2.3 for its hitting-time content; the framing matters separately. The model is "a
discrete-time, discrete-state Markov process of information transfer across the network of
residues", with the transition matrix built as `m_ij = a_ij/d_j` from atom–atom contact
affinities at 4 Å normalised by residue size [VERIFIED-FULLTEXT] (PMC1988854). Its companion
work connects "global dynamics and signal transduction pathways", arguing that "allosteric
communication is facilitated by the intrinsic ability of biomolecules to undergo collective
changes in structure" [VERIFIED-ABSTRACT] (doi:10.1039/b717819k). Dutta & Bahar applied the
same signal-transduction readout to metal-binding sites and found them "remarkably efficient
and precise", through participation in hinge sites controlling soft modes plus central
positioning with minimal solvent exposure [VERIFIED-ABSTRACT]
(doi:10.1016/j.str.2010.06.013, PMC2937013).

Read that last sentence as a warning as much as a result: "central position, low solvent
exposure, hinge participation" is the composite that `docs/FIELD.md` §3 says every method
finds. Any claim built on hit times has to be tested against a burial + degree null.

**C1-OK, C2-OK, C6-OK. Source-conditioned: yes. Cost: one O(N³) solve.**

### 5.2 Perturbation-response and essential-site scanning — the incumbent bar

The incumbent unsupervised ENM family is dense and is the bar we must clear
(`00-conventions.md` §6 item 4). Retrieved this session: Perturbation Response Scanning
extended to simultaneous multi-residue perturbation [VERIFIED-ABSTRACT]
(doi:10.21769/bioprotoc.5718; doi:10.1016/j.jmb.2025.169234); PRS fused with a free-energy
response approximation for residue-level allosteric-site prediction [VERIFIED-ABSTRACT]
(doi:10.1021/acs.jcim.6c00141); RIN plus mixed coarse-grained ANM reporting "up to 80.0 %
sensitivity" for drug-binding sites on SARS-CoV-2 M^pro [VERIFIED-ABSTRACT]
(doi:10.1002/prot.70122); RIN plus SILCS reporting 77.8 % sensitivity for **orthosteric**
sites in class A GPCRs [VERIFIED-ABSTRACT] (doi:10.1021/acsomega.4c06172, PMC11425613).

**Numbers not comparable to ours.** Different targets, different positive class, different hit
criterion, no leakage control. `00-conventions.md` §6 already records what happens to this
family under a leakage-controlled reappraisal: APOP retests at 15 % at Jaccard > 0.5. Quote
these as context, never as a bar.

---

## 6. Percolation, rigidity and network robustness

### 6.1 The residue network sits at a percolation critical point

Morita & Takano's result (§4.4) is the load-bearing one: residue contact networks are in the
**universality class of the three-dimensional critical percolation cluster**, with criticality
"relevant to the ambivalent nature of the protein native structures, i.e. the coexistence of
stability and instability" [VERIFIED-ABSTRACT] (doi:10.1103/PhysRevE.79.020901). A network at
its percolation threshold is one where local edge removal _does_ propagate globally. That is
the precondition under which a bond-percolation or min-cut readout can be informative at all,
and it is measured rather than assumed.

### 6.2 Rigidity percolation and the pebble game

The mechanical analogue is better developed than the connectivity one. Constraint Network
Analysis on **apo** EGFR reveals "a well-defined rigidity percolation transition in apo EGFR",
with ligand binding producing localised rigidification rather than large-scale reorganisation
[VERIFIED-ABSTRACT] (doi:10.64898/2026.01.19.700489, preprint). The pebble-game algorithm for
identifying rigid components is packaged and maintained [VERIFIED-ABSTRACT]
(doi:10.1186/s12859-025-06300-3, PMC12570563). An equivalence has been proposed between the
normal-mode formalism and anisotropic rigidity theory, using "the pebble game algorithm to
identify independent edges" to produce filtered residue interaction networks that improve
prediction of local flexibility and conformational change [VERIFIED-ABSTRACT]
(doi:10.21203/rs.3.rs-7983512/v1, preprint).

**Cost.** The 3D (6,6) pebble game is roughly O(N²) and is trivial at our sizes.
**C1-OK, C2-OK, C6-OK.** Source-free as published; the source-conditioned form is "is residue
i in the same rigid cluster as the active site, and at what constraint density do they
separate?" — which is a **rigidity-percolation dilution curve conditioned on S**, and is a
genuinely different observable from anything in the `f(A)` family.

**Caveat.** Rigidity is chemistry-sensitive: the standard pebble game uses hydrogen bonds
ranked by an energy function, not a distance cutoff. Building it on a bare 8 Å Cα graph would
discard the thing that makes it work.

### 6.3 Articulation points, bridges, k-core

**Definitions and cost.** Articulation points and bridges: Tarjan's DFS, O(N + |E|), instant.
k-core: repeated degree pruning, O(|E|), instant.

**Expected verdict, stated in advance so the negative result is a result.** A Cα contact graph
at 6.5–8 Å in a globular domain is dense and three-dimensional; single-vertex cuts should be
very rare, and the k-core index should track degree and burial closely. Both are source-free.
**The construction that survives is the source-conditioned generalisation:** by Menger's
theorem, the minimum S–i vertex cut equals the maximum number of vertex-disjoint S→i paths.
With unit vertex capacities and one max-flow per residue, cost O(N · |E|√N) ≈ 3 × 10⁸
operations at N = 1100 — seconds. With capacities set to the contact weight (e.g. 1/d² per
`06-signal-propagation-physics.md` §12), the cut value becomes a **transport bottleneck rather
than a degree statistic**, which is the whole point.

**No published application of minimum S–i vertex cut or bond-percolation threshold to
allosteric-site ranking on a residue contact graph was retrieved by the recorded search**,
including a dedicated query on percolation and robustness in protein structure networks that
returned 305 records and no on-topic hit. Recorded as not retrieved (ADR 0019).

### 6.4 Vulnerability descriptors that have been tried

The protein-contact-network community's robustness descriptor of choice is the **participation
coefficient**: across a set of protein–protein interfaces, "the participation coefficient P ...
was the key descriptor of PCN vulnerability of all structures", identifying residues critical
for stability [VERIFIED-ABSTRACT] (doi:10.3389/fbioe.2015.00170, PMC4626657). The programme is
laid out in Di Paola & Giuliani's "Protein contact network topology: a natural language for
allostery", where "network descriptors, capturing network signaling efficiency, explain
allostery in terms of signal transmission" [VERIFIED-ABSTRACT] (doi:10.1016/j.sbi.2015.03.001),
and in the earlier review [VERIFIED-ABSTRACT] (doi:10.1021/cr3002356, PMID 23186336). All
source-free; all C1-OK, C2-OK, C6-OK.

---

## 7. Spectral graph theory beyond eigenvector centrality

### 7.1 The Fiedler vector and algebraic connectivity — with the identity that matters

`L φ_2 = λ_2 φ_2` with `λ_2` the smallest non-zero eigenvalue. `λ_2` is the algebraic
connectivity; `φ_2` is the Fiedler vector; its sign pattern is the standard spectral bipartition.

**The identity to state explicitly in the report:** the GNM Kirchhoff matrix **is** the graph
Laplacian of the contact network, so the **GNM slowest mode is the Fiedler vector** and GNM
hinge sites are its zero-crossings. This is not an analogy. Zhang, Gur & Bahar define hinges
operationally from exactly this: "Hinge residues in mode k were deduced from the kth mode
profile (normalized displacement of residues along the kth mode axis) as those lying at the
crossover between negative and positive motions", using "up to three slowest modes, 1 ≤ k ≤ 3,
... to ensure a cumulative variance σ of ≥ 1/3" [VERIFIED-FULLTEXT] (PMC11626116,
doi:10.1073/pnas.2414333121).

**Their quantitative result, and its C1 problem.** Across "7,754 proteins that have been
structurally resolved in drug-bound forms" over 20 families, "a striking 32.53 ± 10.39 % of
drug-binding sites colocalize with hinge regions", with hinges "enriched by a factor of 4.13
within drug-binding sites, compared to other sites", average hypergeometric
`⟨P⟩ = 4.547 × 10⁻³`, individual P from 1.566 × 10⁻⁶ (MAPK) to 2.603 × 10⁻² (AKR1C3)
[VERIFIED-FULLTEXT] (PMC11626116). **The method as executed uses an ensemble of drug-bound
structural homologs to identify hinges and drug-binding residues together — C1-FAIL as
evidence for us.** Computing `φ_2` on the apo structure alone is C1-OK; their _number_ is not
transferable to the apo setting, and `00-conventions.md` §6 records the CAPASP finding that
this whole family degrades specifically on apo input. Quote the identity, not the 32.53 %.

The same paper is useful for vocabulary: "Essential sites comprise three groups: (1)
chemically active (e.g., catalytic), (2) allosteric, and (3) mechanically sensitive (e.g.,
hinge-bending) sites" [VERIFIED-FULLTEXT] (PMC11626116). Hinges are a _third_ category, not a
synonym for allosteric — consistent with `CONTEXT.md`'s insistence that these words are not
interchangeable.

**Source-conditioned?** No. `φ_2` is a global mode. **Cost:** one eigendecomposition.
**C1-OK, C2-OK, C6-OK** for the apo-only computation.

### 7.2 Mode subsets and the "low-frequency modes are functional" claim

The ENM claim is that soft modes carry function. The most careful retrieved form does not use
the softest mode alone: Altintel, Acar, Erman & Haliloglu show that "dissection of dynamic
information into subsets of slow dynamic modes discloses different layers of multi-directional
allosteric pathways", and that within those subsets the collectivity of information transfer
(their TECol score) identifies residues "associated with known active and allosteric sites"
across ATCase, Na⁺/K⁺-ATPase, TRPM2 and a 20-protein set [VERIFIED-ABSTRACT]
(doi:10.1016/j.jmb.2022.167644).

**Honest counterweight.** `00-conventions.md` §6 records that no tool of eight exceeded 60 %
accuracy in AlloBench's leakage-controlled reappraisal even at a very low Jaccard cutoff, and
that APOP retests at 15 %. The "low modes are functional" claim is real as a correlation and
weak as a predictor.

### 7.3 Localisation and the inverse participation ratio

```
IPR(k) = Σ_i φ_k(i)^4 / ( Σ_i φ_k(i)² )²
```

High IPR = a mode localised on few residues. **Already closed by measurement in our own
corpus** at 63.6 % and 36.4 % against a 90.9 % bar (`00-conventions.md` §5 item 5). Retrieved
protein IPR work is about Anderson-transition criticality of _electronic_ states — proteins
with efficient electron transport are found to be "self-organized into the critical state of
the Anderson transition" with multifractal wavefunctions [VERIFIED-ABSTRACT]
(doi:10.1016/j.csbj.2025.05.049, PMC12167833) — which is a different physics and does not
speak to catalytic-site localisation. **No source was retrieved showing that localised
high-frequency ENM modes mark catalytic sites.** Recorded as not retrieved.

**Do not rebuild IPR.** Source-free and pre-refuted.

### 7.4 Cheeger cuts and local conductance — the useful one

**Cheeger's inequality.** With conductance `h(G) = min_S |∂S| / min(vol S, vol S̄)`,

```
λ_2 / 2  ≤  h(G)  ≤  √(2 λ_2)
```

The spectral gap bounds the sparsest cut in both directions. Globally this is a scalar, not a
ranker.

**The local, source-seeded version is what we want.** Chung's heat-kernel PageRank result:
for a subset S with Cheeger ratio h, "at least a quarter of the vertices in S can serve as
seeds for heat kernel pagerank which lead to local cuts with Cheeger ratio at most O(√h)",
improving the previous bound by `√log|S|` [VERIFIED-ABSTRACT] (doi:10.1073/pnas.0708838104).

**Read that as an algorithm for us.** Seed at the active site, diffuse, sort residues by
`p_i/d_i`, sweep the prefix, take the cut of minimum conductance. The output is a **set**: the
minimum-conductance region containing the active site. Its boundary residues are the ones that
gate the site — a defensible allosteric hypothesis that is not a per-residue score and
therefore not a monotone transform of an amplitude. Cost: one `expm_multiply` plus a sort,
O(|E|·s + N log N). Twenty lines.

**Source-conditioned: yes. C1-OK, C2-OK, C6-OK.** No protein application retrieved.

---

## 8. Information theory on graphs

### 8.1 Communicability — the direct classical analogue of a quantum propagator

**Definition.** Estrada & Hatano:

```
G_pq = [ exp(A) ]_pq = Σ_{k=0}^∞ (A^k)_pq / k!
```

with the temperature-parameterised form `[exp(βA)]_pq`. Estrada's protein-network paper gives
all the variants verbatim on a Cα contact network at `r_C = 7.0 Å`: average communicability
`⟨G_pq⟩ = (2/n(n−1)) Σ_{p<q} G_pq`; communicability angle
`θ_pq = cos⁻¹( G_pq / √(G_pp G_qq) )`, which "describes how efficiently a network transmits
information between its pairs of nodes"; and a long-range variant
`Z = Σ_k A^k / k!!` using the double factorial "to less penalize longer walks"
[VERIFIED-FULLTEXT] (PMC7286701, doi:10.1063/5.0013029). The communicability distance
`ξ_pq = √(G_pp + G_qq − 2G_pq)` is a Euclidean metric, "an angle between position vectors of
the nodes in an Euclidean communicability space" being the associated angle
[VERIFIED-ABSTRACT] (arXiv:1507.05881, doi:10.1103/PhysRevE.92.052809).

The motivation is exactly ours: "most of the transport on the network flows along the shortest
paths ... the consideration of the shortest paths only does not account for the global
communicability", so communicability is "a broad generalization of the concept of the shortest
path" [VERIFIED-ABSTRACT] (arXiv:0707.0756, doi:10.1103/PhysRevE.77.036111).

**The quantum connection is explicit in the literature and we should cite it rather than
invent it.** Estrada, Hatano & Benzi model the network as a system of oscillators and derive
"physical interpretations, both classical and quantum-mechanical, of various communicability
functions", noting that the matrix argument may be either `A` or `L`, and that the functions
of interest are the exponential, the resolvent and the hyperbolic functions
[VERIFIED-ABSTRACT] (arXiv:1109.2950, doi:10.1016/j.physrep.2012.01.006). Sharper still:
Alalwan, Arenas & Estrada "show that the communicability function plays the role of the
**thermal Green's function** of a network of harmonic oscillators", and prove "the existence of
a universal phase transition in the communicability structure of every simple graph" resembling
melting; at the local level "the main driver for node melting is the eigenvector centrality of
the corresponding node, particularly when the critical value of the inverse temperature
approaches zero" [VERIFIED-FULLTEXT abstract] (arXiv:1802.07809).

**The last clause is the honest verdict.** Spectrally,
`[exp(βA)]_pq = Σ_k φ_k(p)φ_k(q) e^{βμ_k}`, so as β grows this converges to
`e^{βμ_1} φ_1(p)φ_1(q)` — it **factorises into eigenvector centrality**. As β → 0 it converges
to `I + βA`, the adjacency matrix. [UNVERIFIED] as a derivation, but it is elementary and
Estrada's own melting result names eigenvector centrality as the β-limit driver. Since
`00-conventions.md` §5 records that published CTQW centrality on residue interaction networks
"shows consistently strong agreement with classical eigenvector centrality" over 150 proteins
(doi:10.1021/jacs.6c08053), and eigenvector centrality is bar #3, **communicability at its
natural β = 1 is somewhere on a path between two things we already have.** Its value to us is
as an interpolating control with one knob, not as a new observable.

**Published protein evidence — the strongest single result in this section.** Estrada found
that in SARS-CoV-2 M^pro, "the largest sensitivity of M^pro to structural perturbations is
located exactly around the catalytic site Cys-145 and coincides with the binding site of strong
inhibitors", measured by long-range subgraph centrality: "the 22 amino acids displaying the
largest change in this centrality form a connected subgraph of the PRN" containing Cys-145
[VERIFIED-FULLTEXT] (PMC7286701). Note the observable there is a **perturbation response of a
communicability-derived centrality**, not communicability itself — which is the same shape of
readout that `06-signal-propagation-physics.md` recommends. The communicability angle
"correlates very well with the experimentally measured value of the relative packing efficiency
of proteins that are represented as residue networks" [VERIFIED-ABSTRACT] (arXiv:1412.7388) —
useful, and also a warning that it is measuring packing. Two MD-based studies use the
communicability matrix to visualise allostery: in the SARS-CoV-2 RBD "the communicability
matrix could serve as a tool to visualize the effects of allostery, as the pairs of amino acids
or secondary structures with high communicability could pinpoint the possible sites" for signal
transfer [VERIFIED-ABSTRACT] (doi:10.1021/acsomega.3c07947, PMC10831861), and in M^pro variants
communicability matrices of PRNs were compared across mutants [VERIFIED-ABSTRACT]
(doi:10.1021/acs.jpcb.2c08312). Both build the network from MD ensembles — **C2-FAIL as
published**, C2-OK on a single apo structure.

**Operator requirement.** Symmetric non-negative `A`. **Cost:** one `expm`, O(N³), under a
second. **Source-conditioned:** yes, as `Σ_{p∈S} G_pi`. **C1-OK, C2-OK, C6-OK.** **New
observable: no — it is a reweighting of the same walk sum.**

### 8.2 Transfer entropy without a trajectory — yes, it is possible

The question posed is answerable and the answer is yes, with a caveat about which paper.

**The C2-clean route.** Hacisuleyman & Erman present "a fast and approximate method of
generating allosteric communication landscapes in proteins ... by using Schreiber's entropy
transfer concept in combination with the Gaussian Network Model", concluding that "information
transfer in proteins does not necessarily take place along a single path, but an ensemble of
pathways is possible", and that "knowledge of entropy only is not sufficient ... additional
information based on **time delayed correlations** should be introduced, which leads to the
presence of causality in proteins"; applied to ubiquitin, pyruvate kinase and PDZ
[VERIFIED-ABSTRACT] (doi:10.1002/prot.25272). The confirmation that this needs only a
structure comes from an independent group: "The GNM provides reasonable approximations of
long-range information exchange as a minimalist network model **based on a single crystal
structure**" [VERIFIED-ABSTRACT] (doi:10.1093/bioinformatics/btae076, PMC10898342).

**The C2-dirty companion, which is the more cited one.** The same authors' PLoS Comput Biol
paper uses "600 nanosecond molecular dynamics trajectories for Ubiquitin" [VERIFIED-ABSTRACT]
(doi:10.1371/journal.pcbi.1005319, PMC5283753). **C2-FAIL.** Citing the wrong one of these two
would misstate our own compliance, so the distinction must be kept.

**Where the directionality comes from — the same place as §2.3.** The GNM Kirchhoff matrix is
symmetric, yet `TE_{i→j} ≠ TE_{j→i}`, because under Langevin relaxation each mode decays at its
own rate `∝ λ_k` and the time-lagged cross-correlation `C_ij(τ)` inherits an asymmetric
weighting of modes at the two residues. Direction is injected by the **dynamics**, not by the
graph. [UNVERIFIED] as a derivation; consistent with the two papers above.

**Downstream GNM-TE work retrieved.** AlloPath combines GNM transfer entropy with an HMM to
predict directional routes "from allosteric site to active site" on hPTP1E PDZ2, Caspase-1 and
CheY, explicitly "without requiring costly MD simulations" [VERIFIED-ABSTRACT]
(doi:10.1016/j.ijbiomac.2026.151961) — note the source there is the _allosteric_ site, which
would be C1-FAIL as an input for us; run in reverse from the active site it is C1-OK. A
2549-mutation, 190-protein GNM-TE study found "pathogenic mutations significantly coincide with
key information sources or sinks within collective information flow" [VERIFIED-ABSTRACT]
(doi:10.1016/j.jmb.2025.169326). GNM-TE has been applied to CFTR [VERIFIED-ABSTRACT]
(doi:10.7554/eLife.88659, PMC10727502) and to Mn ABC transporters [VERIFIED-ABSTRACT]
(doi:10.1002/pro.70039, PMC11779740). A methodological caution from a direct comparison of
correlation, response function and transfer entropy on GNM ubiquitin: use all three, because
"correlation analysis is validated by the two other indicators" and correlation alone confuses
spurious with causal dependence [VERIFIED-ABSTRACT] (doi:10.1088/1478-3975/ace1c5).

**C1-OK (with source-direction caveat), C2-OK for the GNM form, C6-OK. Source-conditioned:
yes, and directionally. Cost:** one eigendecomposition plus O(N²) pair loops.

### 8.3 Von Neumann entropy of ρ = L / tr(L) — and why the GNM entropy is the right one

**Definition.** Braunstein, Ghosh & Severini treat the normalised Laplacian as a density
matrix; the BGS entropy of a network is the von Neumann entropy of that density matrix
[VERIFIED-ABSTRACT] (doi:10.1007/s00026-006-0289-3, arXiv:quant-ph/0406165):

```
ρ = L / tr(L) ,     S(ρ) = − Σ_k (λ_k / tr L) log (λ_k / tr L)
```

`tr(L) = vol(G) = 2m` for an unweighted graph, so `ρ` is PSD with unit trace by construction.

**Operator requirement.** `L` PSD. Any symmetric non-negative `A`.

**Cost.** Eigenvalues only — cheaper than everything else here.

**Biological application retrieved.** The VECTOR framework uses the von Neumann entropy of a
normalised Hi-C contact-map Laplacian across scales of 10²–10⁷ bp, finding that "short-range
entropy systematically decreases at topological associating domain (TAD) boundaries"
[VERIFIED-ABSTRACT] (doi:10.1021/acs.jpcb.5c08112; preprint doi:10.1101/2025.09.24.678266).
That is the right shape of use — entropy as a **boundary detector** on a contact map — and it
is the only retrieved biological precedent. No protein-residue application retrieved.

**The R1 correction, and it is important.** `S(ρ)` is the Shannon entropy of the _normalised
spectrum_. It is **not** the protein's conformational entropy. Under the GNM the configurational
entropy of the Gaussian fluctuation ensemble is, up to additive constants,

```
S_GNM  ∝  − ½ Σ_{k>0} ln λ_k   =  − ½ ln det′(Γ)
```

a different function of the same eigenvalues, and the thermodynamically correct one.
[UNVERIFIED] as a derivation; it is the standard Gaussian entropy `½ ln det(2πe Σ)` with
`Σ ∝ Γ⁻¹`. Two consequences follow immediately.

1. By the Matrix-Tree theorem, `det′(Γ)` is `N` times the weighted spanning-tree count of the
   contact graph. So **the GNM entropy is a log spanning-tree count**, and the entropy change
   on removing residue i is `ln( T(G) / T(G−i) )` up to a constant. That is an exact,
   parameter-free, purely combinatorial quantity. [UNVERIFIED] as stated; the Matrix-Tree
   theorem is textbook and was not retrieved this session.
2. `06-signal-propagation-physics.md`'s ranked Observable #2 — "change in the fluctuation
   spectrum of the network when a site is clamped" — has an exact formula, and it is this one,
   not the von Neumann entropy.

**Source-conditioned?** Both are source-free as scalars. The source-conditioned form is the
one to build: **clamp residue i and measure the change in the active site's mean-square
fluctuation**, `Δ_i = Σ_{p∈S} ( [Γ⁻¹]_pp − [(Γ^{(i)})⁻¹]_pp )`, where `Γ^{(i)}` deletes residue
i and its edges. That reads out the source set specifically, is C1/C2/C6-clean, and is one
Woodbury update per residue.

**C1-OK, C2-OK, C6-OK.**

### 8.4 Graph entropy variants

Structural/graph entropies based on degree or partition distributions are source-free and are
degree statistics in disguise. Retrieved entropy-based centralities use continuous-time random
walks and are explicitly compared to "total f-communicability centralities, of which Katz
centrality and total communicability are particular cases" [VERIFIED-ABSTRACT]
(arXiv:2108.09248) — i.e. they land back in the `f(A)` family of §0. Not pursued.

---

## 9. Summary table

`SC` = conditions on a named source set. `New` = not a monotone transform of a transfer
amplitude / walk sum.

| #   | Formalism                                          | Formula                                                                         | Operator needs              | Cost, N ≤ 1100   | Protein evidence                                                            | C1        | C2                        | C6      | SC                        | New                                   |
| --- | -------------------------------------------------- | ------------------------------------------------------------------------------- | --------------------------- | ---------------- | --------------------------------------------------------------------------- | --------- | ------------------------- | ------- | ------------------------- | ------------------------------------- |
| 1   | Heat kernel                                        | `exp(−tL)`                                                                      | `L` sym PSD                 | O(N³) once       | indirect                                                                    | OK        | OK                        | OK      | yes                       | no                                    |
| 2   | Auto-diffusivity / HKS                             | `Σ_k e^{−λ_k t}φ_k(i)²`                                                         | `L` sym PSD                 | free             | pocket surfaces, C1-FAIL as published                                       | OK        | OK                        | OK      | **no**                    | no                                    |
| 3   | Diffusion distance                                 | `Σ_k μ_k^{2t}(ψ_k(i)−ψ_k(j))²`, **metric**                                      | `P` stochastic reversible   | O(N³) once       | none retrieved                                                              | OK        | OK                        | OK      | yes                       | no                                    |
| 4   | Wave-kernel signature                              | `Σ_k φ_k(i)² f_e(λ_k)²`                                                         | `L` sym PSD                 | free             | none                                                                        | OK        | OK                        | OK      | **no**                    | no — kin to mode IPR, closed          |
| 5   | Effective resistance                               | `L⁺_ii+L⁺_jj−2L⁺_ij`, **metric**                                                | `L` sym PSD, connected      | O(N³)            | none retrieved                                                              | OK        | OK                        | OK      | yes (short S)             | no                                    |
| 6   | Commute time                                       | `vol(G)·R_eff`, **metric**                                                      | as above                    | O(N³)            | Bahar 2007                                                                  | OK        | OK                        | OK      | yes                       | no — same as #5                       |
| 7   | **Hitting time**                                   | `Σ_k d_k(L⁺_ik−L⁺_ij−L⁺_jk+L⁺_jj)`, **not** a metric, **asymmetric**            | `P` stochastic              | O(N³)            | catalytic residues in hit-time minima, 5 enzymes                            | OK        | OK                        | OK      | **yes, directional**      | **yes — the asymmetry is**            |
| 8   | RWR / personalised PageRank                        | `α(I−(1−α)AD⁻¹)⁻¹s`                                                             | `W` stochastic              | ms               | not at residue level                                                        | OK        | OK                        | OK      | **yes**                   | no                                    |
| 9   | Current-flow betweenness                           | current through i, S→j                                                          | `L⁺`                        | O(N³)            | betweenness is field default                                                | OK        | OK                        | OK      | yes if restricted         | no                                    |
| 10  | Ollivier-Ricci                                     | `1 − W₁(m_x,m_y)/d(x,y)`                                                        | stochastic kernel + metric  | seconds          | fold classification, F1 0.71/0.68                                           | OK        | OK                        | OK      | **no**                    | **yes**                               |
| 11  | Forman-Ricci                                       | `4 − deg(u) − deg(v)` unweighted                                                | degrees                     | instant          | DTA attention weights                                                       | OK        | OK                        | OK      | **no**                    | **no — it is degree**                 |
| 12  | CURP / energy-exchange net                         | inter-residue energy current                                                    | MD forces+velocities        | high             | PDZ, FixL, β₂AR                                                             | OK        | **FAIL**                  | partial | yes                       | yes                                   |
| 13  | Harmonic communication map                         | heat-current operator on Hessian                                                | structure + force constants | O(N³)            | PYP, matches Green-Kubo MD                                                  | OK        | OK                        | OK      | yes                       | **yes**                               |
| 14  | Non-equilibrium ENM propagation                    | `d²ΔR/dt² = −(γ/m)ΓΔR`, mode sum                                                | `Γ` sym PSD                 | O(N³)            | myosin 680 res, PDZ3 97 res                                                 | OK*       | OK                        | OK      | **yes**                   | partly                                |
| 15  | Local spectral dimension                           | slope of `k_t(i,i) ∼ t^{−d_s/2}`                                                | `L` sym PSD                 | free             | `d_s<2` over 512 PDB, GNM only                                              | OK        | OK                        | OK      | no (yes if seeded)        | **yes — a slope**                     |
| 16  | Fractional GDE on graphs                           | Caputo-time + `d`-path Laplacian, 2 params                                      | `L`                         | O(N³)            | protein–DNA sliding/hopping                                                 | OK        | OK                        | OK      | yes                       | **yes**                               |
| 17  | Rigidity percolation / pebble game                 | (6,6) pebble game on constraint net                                             | constraint graph            | O(N²)            | rigidity transition in **apo** EGFR                                         | OK        | OK                        | OK      | no (yes if S-conditioned) | **yes**                               |
| 18  | Articulation points / bridges / k-core             | Tarjan; degree peeling                                                          | any graph                   | O(N+E)           | none for allostery                                                          | OK        | OK                        | OK      | **no**                    | no                                    |
| 19  | **Min S–i vertex cut (max-flow)**                  | Menger; unit or 1/d² vertex capacities                                          | any graph                   | seconds          | **none retrieved**                                                          | OK        | OK                        | OK      | **yes**                   | **yes**                               |
| 20  | Fiedler vector / algebraic connectivity            | `Lφ₂=λ₂φ₂`; hinges = sign changes                                               | `L` sym PSD                 | O(N³)            | 32.53±10.39 % drug-site overlap, enrich 4.13 — **holo-derived**             | OK on apo | OK                        | OK      | **no**                    | no                                    |
| 21  | Spectral gap `λ₂`                                  | scalar                                                                          | `L`                         | free             | —                                                                           | OK        | OK                        | OK      | no                        | no                                    |
| 22  | Inverse participation ratio                        | `Σφ_k(i)⁴/(Σφ_k(i)²)²`                                                          | `L`                         | free             | Anderson criticality, not sites                                             | OK        | OK                        | OK      | **no**                    | **no — closed at 36.4 %**             |
| 23  | **Local Cheeger cut (heat-kernel PageRank sweep)** | seed S, sweep `p_i/d_i`, cut of min conductance; `O(√h)` guarantee              | `L`, `W`                    | O(E·s + N log N) | none retrieved                                                              | OK        | OK                        | OK      | **yes**                   | **yes — set-valued**                  |
| 24  | Communicability                                    | `G_pq=[exp(βA)]_pq`; angle `arccos(G_pq/√(G_ppG_qq))`; distance is a **metric** | `A` sym non-neg             | O(N³)            | **M^pro: max perturbation response at Cys-145**; angle ↔ packing efficiency | OK        | OK                        | OK      | yes                       | no — β→∞ gives eigenvector centrality |
| 25  | GNM transfer entropy                               | Schreiber TE on time-lagged GNM/Langevin correlations                           | `Γ` sym PSD                 | O(N³)+O(N²)      | ubiquitin, PDZ, PK, CFTR, 190 proteins                                      | OK*       | **OK** (MD version FAILs) | OK      | **yes, directional**      | **yes**                               |
| 26  | Von Neumann entropy                                | `S(L/tr L)`                                                                     | `L` PSD                     | eigenvalues only | Hi-C TAD boundaries                                                         | OK        | OK                        | OK      | **no**                    | yes but wrong physics                 |
| 27  | **GNM entropy response**                           | `−½ln det′Γ`; `Δ_i = Σ_{p∈S}([Γ⁻¹]_pp − [(Γ^{(i)})⁻¹]_pp)`                      | `Γ` sym PSD                 | Woodbury per i   | this is file 06's Observable #2                                             | OK        | OK                        | OK      | **yes**                   | **yes**                               |

\* C1-OK only if the named source is the **active** site. Seeding from a known allosteric site,
as AlloPath and several PRS papers do, is C1-FAIL for us.

---

## What this changes for our pipeline

Ranked by expected information gained per unit of implementation cost. Every item is
computable from a weighted residue graph (`A`, `D`, `L`), Cα or heavy-atom coordinates, and the
named active-site residue numbers — nothing else.

**1. Directional hitting time to the active site. `network/` + a new propagation readout.
NEW observable (the asymmetry is; the value is not).**

```
W = D⁻¹A ;  delete rows/cols of S → W_R ;  h(i→S) = [ (I − W_R)⁻¹ 𝟙 ]_i
score(i) = −h(i→S)
```

One dense solve, ten lines. This is the highest-ratio item in the file for a reason that is
structural, not empirical: `00-conventions.md` §5 item 11 and
`06-signal-propagation-physics.md` §10 both record that a unitary walk on a symmetric contact
graph **cannot** be directional, and that our deliverable N×N matrix is therefore symmetric
while the measured biology is anisotropic by ≥6-fold. A random walk on the _same_ symmetric
graph is directional for free, because `π_i ∝ d_i` breaks the symmetry. Rank by `h(i→S)`
(receiving), never `h(S→i)` (broadcasting): Chennubhotla & Bahar measured
`⟨H_b⟩ = 340.3 ± 1.5` against `⟨H_r⟩ = 340.3 ± 124.8` on phospholipase A2, and the
near-constant broadcast mean is Kemeny's constant, i.e. a theorem, not a signal.

**2. Minimum S–i vertex cut with 1/d² capacities. `network/`. NEW — not a matrix function of
`A` at all.**

```
capacity(u,v) = w_uv = 1/d_uv²  (per file 06 §12);  vertex capacity = Σ incident w
cut(i) = max-flow value from the merged source node S to residue i
score(i) = 1/cut(i)   [a bottleneck score, high = funnelled]
```

N max-flow calls, `networkx.maximum_flow`, seconds at N = 1100. This is the only item that
answers "where does the signal funnel" combinatorially rather than spectrally, and **no
published application of it to allosteric-site ranking was retrieved**. It is orthogonal to
every walk sum by construction. Risk, stated up front: an 8 Å contact graph is dense and the
cut may reduce to `min(deg)`; the 1/d² capacity is what is supposed to prevent that, and if it
does not, the negative result is publishable in the experiment notes.

**3. GNM entropy response of the active site to clamping residue i. `classical/` + `network/`.
NEW — a spectral-determinant response, not an amplitude.**

```
Γ = L (Kirchhoff = graph Laplacian) ;  Γ^(i) = Γ with residue i and its edges deleted
Δ_i = Σ_{p∈S} ( [Γ⁻¹]_pp − [(Γ^(i))⁻¹]_pp )        # source-conditioned form
S_GNM = −½ Σ_{k>0} ln λ_k = −½ ln det′(Γ)          # global form, = log spanning-tree count
```

This is `06-signal-propagation-physics.md`'s ranked Observable #2 with an exact formula
attached, and §8.3 above supplies the correction that matters: use the **GNM Gaussian entropy**
`−½ Σ ln λ_k`, not the von Neumann entropy of `L/tr(L)`. They are different functions of the
same spectrum and only the first is the conformational entropy. Cost: one Woodbury update per
residue on a cached `Γ⁻¹`.

**4. Local Cheeger cut seeded at the active site. `network/`. NEW — set-valued.**

```
p = heat-kernel PageRank: expm_multiply( −t(I − D⁻¹A), s_S )
sort residues by p_i / d_i ;  sweep prefixes ;  take the prefix of minimum conductance
report the boundary residues of that cut
```

Chung's guarantee: conductance `O(√h)` from a seed inside the target set. Twenty lines using
`scipy.sparse.linalg.expm_multiply`. The per-residue _ordering_ it uses is a heat-kernel
vector, hence a monotone transform of a diffusive amplitude; the **cut threshold** is not, and
the deliverable is the boundary set. This gives a hypothesis of a different type from a ranked
list, which is worth having when the ranked-list bar (`−distance`, AUC 0.617) is so hard.

**5. Ollivier-Ricci curvature of edges, and its minimum along the S→i max-flow bundle.
`network/`. NEW as a node quantity, constructed as a source-conditioned one.**

```
κ(u,v) = 1 − W₁(m_u, m_v) / d(u,v)     # one small LP per edge, seconds total at N ≤ 1100
score(i) = − min{ κ(e) : e on the S→i flow support }
```

Contradict the literature's cost warnings explicitly in the report: they are calibrated to
N ≳ 10⁵, our LPs are ~15 × 15, and the whole computation is seconds. Negative curvature is the
published signature of a transport bottleneck (over-squashing, arXiv:2211.15779) and of
non-diffusive walk behaviour (arXiv:2512.03968). **Check Forman-Ricci first and cheaply**: if
`F(e) = 4 − deg(u) − deg(v)` on our unweighted graph, Forman is degree and can be dropped in
one line of code rather than one week of work.

**6. Local spectral dimension from the heat-kernel diagonal. `quantum/` or `classical/`.
NEW — it is a slope, not a value.**

```
d_s(i) = −2 · d log k_t(i,i) / d log t ,   fitted over an intermediate-t window
```

Free once the eigendecomposition exists. Justified by a measured protein fact: `d_s < 2` over
512 PDB structures from the GNM alone (PMC2922288), and `d_s ≈ 1.3` with 3D-critical-percolation
universality (doi:10.1103/PhysRevE.79.020901). A residue whose local slope departs from the
protein's global `d_s` sits at a topological anomaly. Source-free as written; the
source-conditioned version fits the slope of `Σ_{p∈S}[exp(−tL)]_{pi}` instead. Low rank because
it is close kin to burial and must be tested against a burial null.

**7. Rigidity-percolation dilution curve conditioned on the active site. `network/`. NEW.**

Run the pebble game while diluting the constraint set, and record the dilution level at which
residue i separates from the active site's rigid cluster. Precondition is met and measured:
apo EGFR shows a well-defined rigidity percolation transition
(doi:10.64898/2026.01.19.700489). Ranked here rather than higher because it needs a _hydrogen-
bond constraint network with energies_, not a Cα cutoff graph — a real amount of new
infrastructure — and because the same edge-weighting work is already item 2 of
`06-signal-propagation-physics.md`'s pipeline list.

**8. Controls to run, not methods to build.** Compute and report, but do not claim:
communicability `Σ_{p∈S}[exp(βA)]_{pi}` with β swept (it interpolates between adjacency and
eigenvector centrality, both of which are already bars); effective resistance `R_eff(S,i)`
(a metric, but strictly increasing in distance on near-lattice graphs); RWR seeded at S. Each
is one line and each is a **monotone transform of a walk sum**, so each is expected to land
near `ctrl_closeness`. `06-signal-propagation-physics.md` §9 predicts exactly this, and a
method landing there is diagnosed, not lucky.

**9. Do not build.** Wave-kernel signature and inverse participation ratio (§1.4, §7.3) — kin
to mode-IPR, closed at 36.4 % in our own corpus. Forman-Ricci on an unweighted graph (§3.2) —
a degree statistic. Commute time alongside effective resistance (§2.2) — the same number twice.
Von Neumann entropy of `L/tr(L)` as a proxy for conformational entropy (§8.3) — wrong function
of the right spectrum. CURP-style energy-exchange networks (§4.1) — C2-FAIL.

**10. Two statements the report must carry, because a referee in this field will supply them
if we do not.** (i) Communicability `exp(A)` is a **thermal Green's function** of a harmonic
network and `exp(−iHt)` is its Wick rotation — the literature says so explicitly
(arXiv:1802.07809; arXiv:1109.2950), so our quantum propagator has a named classical twin and
we should present it that way rather than be shown it. (ii) At N ≤ 1100 **every classical
observable in this file costs under a second**, so the C3 resource comparison is not
"quantum is faster" — it never will be here — but "quantum is a different weighting of the
same walk sum, tested empirically". That is the framing already fixed in
`06-signal-propagation-physics.md` §11 and this file is consistent with it.

---

## Method

**Databases.** arXiv API (`export.arxiv.org/api/query`), Europe PMC REST search
(`resultType=core`) and full text (`fullTextXML`), PMC article pages as fallback when
`fullTextXML` returned HTTP 404 (used once, successfully, for PMC2922288), and general web
search for four items whose canonical venue is a non-indexed proceedings or a pre-2000
journal (SGP/Computer Graphics Forum, J. Math. Chem., Social Networks, STOC/Comput. Complex.).
Semantic Scholar not attempted (rate limited, conventions §3).

**Queries run** — 12 batches, 30 distinct queries.
_arXiv:_ `"heat kernel signature"`; `"wave kernel signature"`;
`abs:"effective resistance" AND abs:"commute time"`; `abs:communicability AND abs:network`;
`abs:"communicability angle" OR abs:"communicability distance"`;
`abs:Ollivier AND abs:curvature AND abs:graph`;
`(abs:"Ricci curvature" OR abs:"Forman curvature") AND (abs:protein OR abs:"amino acid" OR abs:residue)`;
`abs:"personalized PageRank" OR abs:"random walk with restart"`;
`abs:"diffusion maps" AND abs:"diffusion distance"`; `abs:"spectral dimension" AND abs:protein`;
`(abs:"anomalous diffusion" OR abs:fracton OR abs:subdiffusion) AND abs:protein`; and four
single-ID lookups (`1109.2950`, `0809.4876`, `1802.07809`, `2202.00318`, `0707.0756`, `2607.16553`).
_Europe PMC:_ Chennubhotla+Bahar+Markov/propagation/signal; communicability AND
protein/residue/allosteric; Ricci/Ollivier/Forman AND protein/network; energy exchange network
/ CURP / inter-residue energy; rigidity percolation / pebble game / percolation / k-core /
articulation AND protein network; `"von Neumann entropy" AND (graph OR network)`; transfer
entropy AND (GNM OR elastic network OR allosteric); entropy/information transfer AND GNM AND
AUTH:Erman; inverse participation ratio / mode localization AND protein; Fiedler / algebraic
connectivity / spectral partitioning AND protein; GNM AND slowest mode/hinge AND catalytic;
perturbation response scanning / essential site scanning / random walk AND allosteric residue;
energy/thermal transport AND protein AND normal mode/elastic network/communication maps;
Leitner AND energy transport AND allosteric/communication map; k-core/cut vertex/articulation/
betweenness AND protein contact network; network robustness / node removal / percolation AND
residue network; protein contact network AND percolation/robustness/small world/topology;
heat kernel / heat diffusion / graph diffusion AND protein AND allosteric/binding site/residue.
_Web search:_ Sun-Ovsjanikov-Guibas HKS DOI; Klein-Randić resistance distance DOI; Newman
current-flow betweenness DOI; Chandra et al. commute-time identity DOI; Ollivier 2009 DOI;
Sreejith et al. Forman curvature DOI; Coifman-Lafon diffusion maps DOI; Chung heat-kernel
PageRank DOI; Braunstein-Ghosh-Severini DOI; Granek-Klafter fractons DOI; Di Paola et al.
Chem. Rev. DOI; Kemeny's constant definition.

**Counts.** Approximately 240 records returned across all queries. **57 screened in** on title
and abstract and cited in this file. **Five full texts retrieved and read this session:**
PMC1988854 (Chennubhotla & Bahar, hit/commute times), PMC7286701 (Estrada, M^pro
communicability), PMC6015066 (Wang et al., non-equilibrium ENM propagation), PMC11626116
(Zhang/Gur/Bahar, global hinge sites), PMC6976091 (Yamato & Laprévote, harmonic communication
map) — plus PMC2922288 (Reuveni/Granek/Klafter) read via the PMC article page after
`fullTextXML` returned 404.

**Stopping rule.** Stop when each of the eight mandated topics has (a) at least one formula
with a retrieved DOI or arXiv ID, (b) a stated operator requirement, and (c) either a protein
application or an explicit "not retrieved" record; and when a further query on that topic
returns no record that changes a verdict. Reached for all eight. Topic 8 (communicability) was
additionally cross-checked across four independent Estrada-group sources plus two independent
protein applications, because the brief flagged it as mandatory.

**What could not be reached.**

- **The explicit inter-residue energy-conductivity formula** for the harmonic communication
  map. PMC6976091 describes the method and its agreement with Green–Kubo MD but does not print
  the heat-current-operator formula; the primary Leitner reference was not retrieved. This is
  the single largest gap for implementing item 13 of the summary table.
- **Sun, Ovsjanikov & Guibas (2009)** full text. Only the abstract and the DOI were retrieved
  (doi:10.1111/j.1467-8659.2009.01515.x, plus dl.acm.org/doi/10.5555/1735603.1735621). The HKS
  and auto-diffusivity formulas as written here are standard and are tagged accordingly.
- **Klein & Randić (1993), Chandra et al. (1997), Ollivier (2009), Sreejith et al. (2016),
  Coifman & Lafon (2006), Chung (2007), Braunstein/Ghosh/Severini (2006), Newman (2005),
  Granek & Klafter (2005)** — abstracts, DOIs and the specific claims quoted were retrieved via
  web search this session; full texts were not opened. Tagged `[VERIFIED-ABSTRACT]`.
- **The exact hitting-time index form** (§2.3) and **the Forman reduction to `4 − deg − deg`**
  (§3.2) could not be sourced verbatim. Both are tagged `[UNVERIFIED]`; the first was checked
  by verifying that it sums to the verified commute-time identity, the second is a one-line
  code check we should run before relying on it.
- **No source was retrieved** applying (a) diffusion distance / diffusion maps, (b) minimum
  source–target vertex cut or bond-percolation threshold, (c) a local Cheeger sweep, or (d)
  Ollivier-Ricci curvature, to **allosteric-site ranking on a residue contact graph**. Per
  ADR 0019 these are recorded as "not retrieved by the recorded search", never as an absence of
  prior art. They are also, for the same reason, where the four highest-ranked items in the
  section above come from.
