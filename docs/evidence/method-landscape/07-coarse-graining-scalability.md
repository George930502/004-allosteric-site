# Network coarse-graining, graph compression, and the proof that compression preserves signal

**Scope:** how to shrink a 300–1000-node residue network so it fits a device, and what formal
guarantee exists that the shrunk network still carries the allosteric signal. Covers
elastic-network coarse-graining, graph coarsening and sparsification theory, community and
modular decomposition, Markov lumping theory, renormalisation on networks, and structure-aware
protein mappings. **Excludes** circuit synthesis, gate counts and qubit costs — that is file 08.
It also excludes the choice of propagation metric itself, which is the earlier method files.
**Sibling files:** `08-*` (circuit synthesis and hardware resources), `00-conventions.md`.
**Retrieved:** 2026-08-25.

---

## 0. Why this file exists, and what the challenge actually asks

`CHALLENGE.md` §4.2 makes coarse-graining a **named secondary objective**, worded as a two-part
demand: "demonstrate a method for coarse-graining the protein structure" **and** "prove that this
compression retains the essential topological signal". §7 repeats it as a scored secondary
criterion. The word is _prove_. Most entrants will coarse-grain and then assert retention by
showing one picture. The content below exists so that we can instead name a theorem, state its
error bound, and report the quantity the theorem bounds.

Our sizes make this concrete rather than academic. The cardiac myosin arm is 764 nodes and the
secondary benchmark spans 147–1058 modelled residues (`docs/ROADMAP.md`, Phase 1.7 and Phase 4).
A one-qubit-per-residue encoding puts myosin and the largest secondary arms out of reach of a
near-term device, so the compression is required, not optional.

There is a structural point to fix before the survey. **Two different reductions are commonly
conflated, and only one of them buys qubits.**

- **Coarsening** merges nodes. `N → n`. This is what reduces a qubit count.
- **Sparsification** removes edges while keeping all `N` nodes. This reduces _interaction terms_,
  i.e. gate count and depth — a file-08 concern — and buys no qubits at all.

Spielman and Srivastava's sparsifiers keep the vertex set `V` unchanged and return a subgraph
`H = (V, Ẽ, w̃)` with `|Ẽ| = O(n log n / ε²)` edges [VERIFIED-FULLTEXT, arXiv:0803.0929]. That is
the wrong axis for a qubit budget and the right axis for a depth budget. Both are useful to us;
they must not be reported as the same result.

---

## 1. The proof: four families of guarantee, and what each one actually bounds

This is question (a), and it is the most valuable section in the file. Four distinct kinds of
theorem exist. They are not interchangeable — they bound different objects, and only two of them
bound anything an allosteric ranking depends on.

### 1.1 Eigenvalue interlacing — free, general, and weak

For any coarsening matrix `P` of full row rank, mapping an `N × N` PSD Laplacian `L` to an
`n × n` coarse Laplacian `L_c = P^∓ L P⁺`:

> `γ₁ λ_k ≤ λ̃_k ≤ γ₂ λ_{k+N−n}` for `k = 1, …, n`, with `γ₁ = λ₁((PP^⊤)^{-1})` and
> `γ₂ = λ_n((PP^⊤)^{-1})`

[VERIFIED-FULLTEXT, Loukas 2019, Theorem 2.3, arXiv:1808.10650, JMLR 20(116)]. For Laplacian
_consistent_ coarsening (each coarse node is a contraction set of fine nodes, weights summed over
the sets), the constants become the smallest and largest contraction-set sizes:
`γ₁ = min_i |V₀^{φ(i)}| ≥ 1` and `γ₂ = max_i |V₀^{φ(i)}|` [VERIFIED-FULLTEXT, ibid., Property 2.6
and the eigenvalue-interlacing paragraph of §2].

The identical structure appears independently in three places, which is a sign it is the generic
statement rather than a method-specific one:

- Normalised Laplacian, coarsening by node merging: `λ(i) ≤ λ_c(i) ≤ λ(i + N − n)` for
  `i = 1, …, n` [VERIFIED-FULLTEXT, Jin, Loukas & JaJa, Property 4.1, arXiv:1802.04447].
- Kron reduction (Schur complement on the loopy Laplacian):
  `λ_r(Q) ≤ λ_r(Q_red) ≤ λ_r(Q[α,α]) ≤ λ_{r+n−|α|}(Q)` [VERIFIED-FULLTEXT, Dörfler & Bullo,
  Theorem 7.1, arXiv:1102.2950].

**What this buys us, honestly:** almost nothing on its own. Loukas states plainly that
"Theorem 2.3 is particularly pessimistic as it has to hold for every possible `P` and `L`"
[VERIFIED-FULLTEXT]. The upper bound is `λ_{k+N−n}`, and at 70 % compression `N − n` is most of
the spectrum, so the window is vacuous. Interlacing is a sanity floor — it tells us the coarse
spectrum cannot _escape_ the fine one — not a proof of retention. Reporting only interlacing
would be the assertion dressed as a theorem that the challenge is inviting.

### 1.2 Restricted spectral approximation — the strongest general coarsening guarantee retrieved

Loukas's contribution is to give up on approximating the whole spectrum (impossible once the
dimension changes: satisfying `(1±ε)‖x‖_L` for every `x ∈ ℝ^N` forces `ε = 1` by a rank argument
[VERIFIED-FULLTEXT]) and instead approximate the action of `L` on a chosen subspace.

> **Definition 3.1 (Restricted spectral approximation).** `L_c` and `L` are `(R, ε)`-similar if
> `‖x − x̃‖_L ≤ ε ‖x‖_L` for all `x ∈ R`, where `x̃ = P⁺Px`.

[VERIFIED-FULLTEXT, Loukas 2019]. Take `R = U_k = span(u₁, …, u_k)`, the _k lowest_ Laplacian
eigenvectors. Three consequences follow, and they are the theorems to cite:

> **Theorem 3.3 (Eigenvalue approximation).** If `L_c` and `L` are `(U_k, ε_k)`-similar then
> `γ₁ λ_k ≤ λ̃_k ≤ γ₂ (1+ε_k)² / (1 − ε_k²(λ_k/λ₂)) · λ_k`, whenever `ε_k² < λ₂/λ_k`.

> **Theorem 3.4 (Eigenspace approximation).**
> `‖sin Θ(U_k, P^⊤Ũ_k)‖_F² ≤ (1/(λ_{k+1} − λ_k)) · ( Σ_{i≤k} λ_i((1+ε_i)²/γ₁ − 1) + λ_k Σ_{i≤k} ε_i )`.

> **Theorem 3.5.** For `2 ≤ k ≤ ⌊n/2⌋`, `φ_k(G) ≤ φ_k(G_c) = O( √( γ₂(1+ε_{2k})² ξ_k(G) /
(1 − ε_{2k}²(μ_{2k}/μ₂)) · φ_k(G) ) )` — the `k`-way conductance of the coarse graph is
> controlled by that of the fine graph.

[all three VERIFIED-FULLTEXT, Loukas 2019]. Three things matter for us.

1. **The bound depends on `λ_k`, not `λ_{k+N−n}`.** That is what makes it non-vacuous where
   interlacing is vacuous.
2. **It is tighter for the slow modes.** Loukas: "Noticing that `ε_k ≤ ε_{k'}` whenever `k < k'`,
   one also deduces that it is stronger for smaller eigenvalues" [VERIFIED-FULLTEXT]. For `k = 2`
   the bound collapses to `γ₁λ₂ ≤ λ̃₂ ≤ γ₂ (1+ε₂)²/(1−ε₂²) · λ₂`. This is the single most
   important sentence in this file for our use, and §11 develops it.
3. **The eigenspace bound is inversely proportional to the spectral gap `λ_{k+1} − λ_k`.** A
   near-degenerate protein spectrum at the cut `k` makes the guarantee blow up even when the
   eigenvalues themselves are fine. This is a real and checkable failure condition, not a
   theoretical caveat.

Loukas is explicit about the limits: there is no known polynomial-time algorithm that provably
approximates the minimal achievable `ε`, and no rigorous way to say in advance how much reduction
a given graph tolerates [VERIFIED-FULLTEXT, §6 Conclusions]. **The guarantee is a posteriori: you
compute `ε` for the coarsening you produced. You cannot promise it before you coarsen.** For our
purposes that is fine — a measured `ε` per target per ratio is exactly the "proof" artifact the
challenge asks for.

### 1.3 Exact invariants — Kron reduction preserves effective resistance exactly

Kron reduction takes the Schur complement of the loopy Laplacian `Q` with respect to the interior
nodes, retaining a chosen boundary set `α`. Dörfler and Bullo prove (arXiv:1102.2950, all
[VERIFIED-FULLTEXT]):

- **Closure.** The class of loopy Laplacians (and of connected undirected graphs) is closed under
  Kron reduction; iterative one-node elimination equals the one-step Schur complement.
- **Exact resistance invariance.** "The effective resistance `R_ij` between any two boundary
  nodes `i, j ∈ α` is equal when computed from `Q` or `Q_red`." This is an _equality_, not a bound
  — the only exact preservation theorem retrieved in this review.
- **Spectral interlacing**, as quoted in §1.1.
- **Densification (Theorem 6).** "Two nodes `i, j ∈ α` are connected by an edge in `G_red` if and
  only if there is a path from `i` to `j` in `G` whose nodes all belong to `{i,j} ∪ (I_n \ α)`",
  and if the eliminated interior nodes `β` form a connected subgraph then the boundary nodes
  adjacent to `β` "form a clique in `G_red`". Consequently algebraic connectivity rises: in their
  worked example `λ₂(L) = 0.30 ≤ λ₂(L_red) = 0.45`.

**Read for us:** Kron reduction is the one method that exactly preserves a _pairwise
communication distance_ between the nodes we keep. Since commute time on a graph is `2m` times the
effective resistance, and since commute time is the very quantity Chennubhotla and Bahar use as
the protein signal-propagation measure (§3.5), this is the tightest match between a coarsening
theorem and our physics that the search found. The cost is severe and must be stated: the reduced
graph becomes dense to complete, which converts a sparse residue contact graph into an all-to-all
interaction Hamiltonian. That is a direct hit on C3 hardware connectivity and belongs in the
file-08 trade study, not hidden here. Loukas's empirical finding is the second caveat: Kron
reduction "is an effective way to half the graph size but can result in poor approximation
otherwise", with numerical instability above `r = 50 %` [VERIFIED-FULLTEXT, Loukas 2019 §5.1].

### 1.4 Lumping theory — bounds on the coarse _propagator_, not just the spectrum

This is the family that bounds what we actually compute, because our deliverable is a propagator
readout, not an eigenvalue list.

**Exact lumpability.** For a row-stochastic `P` and a partition of the state space into classes
`L_k`, a necessary and sufficient condition for the partition to be a lumping is

> `Σ_{j ∈ L_l} P_ij` is constant for all `i ∈ L_k`,

and the aggregated chain is then `P̃_kl = Σ_{j∈L_l} P_ij` for any `i ∈ L_k`
[VERIFIED-FULLTEXT, Nilsson Jacobi, arXiv:0810.1127, Eqs. (1) and (3), citing Kemeny & Snell].
**Approximate lumpability** is defined by `P = (1−ε)A + εB` with `A` exactly lumpable, giving
aggregated transition probabilities constant to `O(ε)` [VERIFIED-FULLTEXT, ibid., Eq. (4)]. The
formal treatment of exact versus ordinary lumpability is Buchholz, _J Appl Prob_ 31:59–75 (1994),
doi:10.2307/3215235 — bibliographic record verified via Crossref, content not retrieved this
session [UNVERIFIED].

The condition has a direct structural reading for a contact graph: **nodes may be merged when they
have the same normalised connection profile to the rest of the graph.** Jin, Loukas and JaJa reach
the identical criterion from the spectral side. Their Proposition 4.1: if every node in a
partition has the same normalised edge weights, `w(i)/d(i) = w(j)/d(j)`, then the full and partial
spectral distances are exactly zero. Their Proposition 4.2: merging one pair with
`‖w(a)/d(a) − w(b)/d(b)‖₁ ≤ ε` gives `SD_full ≤ Nε` and `SD_part ≤ nε`
[both VERIFIED-FULLTEXT, arXiv:1802.04447]. Two independent literatures converge on the same
merge rule. That convergence is itself worth reporting.

**The Galerkin-projection bounds.** The Markov-state-model literature supplies the sharpest
statements. Write `Q` for the orthogonal projection onto the span of the (measure-normalised)
block indicator functions `χ_{A_i}/μ(A_i)`; the coarse propagator is `P = QTQ`. The projection
"keeps the measure on the sets `A₁,…,A_n`, but on each of the sets the ensemble will be
redistributed according to the invariant measure and the detailed information about the
distribution inside of a set `A_i` is lost" [VERIFIED-FULLTEXT, Sarich, Noé & Schütte,
_Multiscale Model Simul_ 8:1154–1177 (2010), preprint].

> **Eigenvalue bound.** Let `1 = λ₀ > λ₁ > … > λ_{m−1}` be the `m` dominant eigenvalues of `T`
> with eigenvectors `u_i`, `D` the coarse subspace with `1 ∈ D`, `dim(D) = n ≥ m`, and `Q` the
> orthogonal projection onto `D`. Then
> `E(δ) = max_{i=1..m−1} |λ_i − λ̂_i| ≤ λ₁ (m − 1) δ²`, where `δ = max_i ‖Q^⊥ u_i‖`.

[VERIFIED-FULLTEXT, Djurdjevac, Sarich & Schütte, Theorem 4.2, _Multiscale Model Simul_
10(1):61–81 (2012), preprint]. A generator version (Theorem 4.3) bounds the _relative_ error by
`(1+ε)(m−1) δ_A²` [VERIFIED-FULLTEXT, ibid.].

> **Propagator bound.** `E(k) = ‖QT^k Q − P^k‖ ≤ min(2 ; C(δ(A), η(τ), k)) · λ₁^k`, with
> `C(δ, η, k) = (mδ + η) C_sets(δ,k) + C_spec(η,k)`, `C_sets(δ,k) = m^{1/2}(k−1)δ` and
> `η = exp(−τΔ)` set by the spectral gap `Δ`.

[VERIFIED-FULLTEXT, Sarich, Noé & Schütte, Theorem 3.1].

**Why this is the family that matters for us.** The eigenvalue error is **quadratic** in the
projection error `δ` of the _dominant_ (slowest) eigenvectors onto the coarse space. A coarse
partition whose indicator functions capture the slow eigenvectors to 10 % gives 1 % eigenvalue
error. That is a strong, computable, reportable statement about exactly the modes allostery uses.
`δ` is measurable on our own network with no holo information and no MD, so it satisfies C1 and
C2 by construction.

Two related classical results are named here for completeness but were **not** retrieved in full
text this session: nearly-completely-decomposable aggregation via stochastic complementation
(Meyer, _SIAM Review_ 31:240–272, 1989, doi:10.1137/1031050) and robust Perron cluster analysis
(Deuflhard & Weber, _Linear Algebra Appl_ 398:161–184, 2005, doi:10.1016/j.laa.2004.10.026). Both
bibliographic records verified via Crossref. PCCA+ "always delivers an optimal fuzzy clustering
for nearly uncoupled, not necessarily reversible, Markov chains with transition states"
[VERIFIED-ABSTRACT, retrieved via search of the ScienceDirect record].

---

## 2. Master table — method, guarantee, demonstrated compression, applicability

Compression is stated as the paper states it. `r` is the fraction of nodes removed
(`r = 1 − n/N`) where the source uses that convention.

| Method                                                                                  | What it preserves                                                                                               | Formal guarantee?                                                                                                               | Compression demonstrated                                                                                                                                                          | Applicable to a residue contact graph?                                                                                                         |
| --------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| **Loukas local-variation coarsening** (arXiv:1808.10650)                                | action of `L` on the `k` lowest eigenvectors; hence low eigenvalues, principal eigenspaces, `k`-way conductance | **Yes** — restricted spectral approximation; Thms 2.3, 3.3, 3.4, 3.5; `ε` measured a posteriori                                 | `r` up to 70 % with `ε < 1` on all four test graphs; on the yeast PPI graph (`N`=1458) mean relative error on the 10 lowest eigenvalues 0.003 / 0.034 / 0.406 at `r` = 30/50/70 % | **Yes.** Nearly-linear time, keeps sparsity, needs only the Laplacian. Yeast PPI is the nearest published analogue to a residue network        |
| **Kron reduction / Schur complement** (arXiv:1102.2950)                                 | effective resistance between retained nodes **exactly**; Laplacian class; interlacing                           | **Yes** — exact invariance + interlacing (Thms 6, 7, 8)                                                                         | Halves the graph reliably; Loukas reports poor approximation and numerical instability at `r` > 50 %                                                                              | **Yes but expensive.** Reduced graph becomes dense/complete → all-to-all Hamiltonian, a C3 cost. Best where retained nodes are few and fixed   |
| **Spectral-distance coarsening** (Jin, Loukas & JaJa, arXiv:1802.04447)                 | normalised-Laplacian eigenvalues via the _lifted_ graph                                                         | **Yes** — Props 4.1 (`SD = 0` under equal normalised edge weights), 4.2 (`SD_full ≤ Nε`)                                        | Graph classification at coarsening ratio 1/5 matches full-graph accuracy on NCI1, NCI109                                                                                          | **Yes.** Gives the merge criterion directly: merge nodes with similar normalised connection profiles                                           |
| **Markov Stability multiscale partitioning** (PNAS 2010; PLoS ONE 2012)                 | community structure at every Markov time; no imposed scale                                                      | Partial — dynamical objective with proven limits of modularity/Infomap as its `t=1` special cases; no `ε`-bound on a propagator | Adenylate kinase atomistic graph: robust partitions at 206 → 8 → 3 communities (214 amino acids)                                                                                  | **Yes, and the best-validated on proteins.** Recovers residue, secondary-structure and domain levels from one sweep                            |
| **Chennubhotla–Bahar hierarchical Markov decomposition** (Mol Syst Biol 2006)           | signal-propagation stochastics; stationary distribution; global modes                                           | No error bound; **empirical fidelity test** with reconstruction                                                                 | GroEL–GroES `n` = 8015 → 1316, 483, 133, 35, 21 (levels 1–5). Global modes retained at `r`(correlation) = 0.99 at **all** levels                                                  | **Yes — this is the closest published prior art to our task.** Soft (probabilistic) ownership, explicit reduction and expansion operators      |
| **RTB / block normal modes** (Tama et al. 2000)                                         | low-frequency normal modes                                                                                      | No bound; empirical                                                                                                             | 6 residues per block "almost as accurate as with a single amino-acid per block"; `3N×3N` → `n×n`                                                                                  | **Yes**, in its ENM form. Contiguous-sequence blocks are trivially computable from apo coordinates                                             |
| **Density-cluster RTB** (Demerdash & Mitchell 2012)                                     | low-frequency modes; B-factors                                                                                  | No bound; empirical                                                                                                             | 85–90 % reduction in degrees of freedom vs standard blocking; ~100× speedup                                                                                                       | **Yes.** Clustering on atomic density gradients; superior B-factor correlation to fixed 1–4-residue blocks                                     |
| **Hierarchical ENM coarse-graining** (Doruker, Jernigan & Bahar 2002)                   | slowest collective mode                                                                                         | No bound; empirical                                                                                                             | Influenza HA `N` = 1509 → `N/2, N/10, N/20, N/40`; correlation > 0.95 for the slowest mode; reconstructed all-residue mode at 1/40 correlates 0.73                                | **Yes.** Backbone-subset selection; ~3 orders of magnitude speedup                                                                             |
| **Rigid-cluster decomposition (FIRST / RCNMA)** (Jacobs et al. 2001; Ahmed et al. 2010) | rigid/flexible partition; essential dynamics subspace                                                           | No bound; empirical, but large-scale                                                                                            | RCNMA matches ENM against MD essential dynamics on 335 proteins "despite a higher level of coarse graining"                                                                       | **Yes**, but the constraint network needs hydrogen bonds and salt bridges, i.e. more than Cα contacts                                          |
| **Spectral sparsification** (Spielman & Srivastava, arXiv:0803.0929)                    | Laplacian quadratic form to `(1±ε)`; approximately, all effective resistances                                   | **Yes** — Theorem 1, `O(n log n / ε²)` edges                                                                                    | Edges only                                                                                                                                                                        | **Wrong axis.** Keeps all `N` nodes → buys depth, not qubits. Belongs in file 08                                                               |
| **Graph pooling in GNNs** (DiffPool arXiv:1806.08804; MinCutPool arXiv:1907.00481)      | task-relevant embedding; a relaxed normalised min-cut                                                           | **No formal preservation guarantee** in either abstract                                                                         | DiffPool: 5–10 % average accuracy gain on graph classification                                                                                                                    | **No.** Both learn assignments from labelled data. Trained weights on the prediction path risk C2, and there is no retention theorem to report |
| **Laplacian renormalisation group** (Villegas et al., _Nat Phys_ 19:445–450, 2023)      | diffusion/information flow across scales; "Kadanoff supernodes"                                                 | Not retrieved                                                                                                                   | Not retrieved                                                                                                                                                                     | Plausible but unproven here. Its heterogeneous-network target is not obviously a geometric protein graph                                       |

---

## 3. Coarse-graining in the elastic-network tradition

This is the tradition C6 puts us in, so its results carry more weight for us than the generic
graph-theory ones.

### 3.1 RTB / block normal modes

Durand, Trinquier and Sanejouand introduced the rotations-translations-of-blocks projection;
Tama, Gadea, Marques and Sanejouand tested it across 46–858 residues. The finding:

> "with six amino-acids per block, the normal modes are almost as accurate as with a single
> amino-acid per block. In this case, for a protein of `n` residues and `N` atoms, the RTB method
> requires the diagonalization of an `n × n` matrix, whereas standard procedures require the
> diagonalization of a `3N × 3N` matrix"

[VERIFIED-ABSTRACT, _Proteins_ 41:1–7 (2000), doi:10.1002/1097-0134(20001001)41:1<1::aid-prot10>3.0.co;2-p].
The second half of that sentence is the one to keep: **the quality of the modes "depends very
little on the way the polypeptidic chain is split into blocks"** [VERIFIED-ABSTRACT, ibid.]. If
that transfers to our propagator, the choice of partition matters far less than the choice of
ratio — which is a testable claim on our own benchmark and a cheap one to run.

Demerdash and Mitchell's Density-Cluster RTB replaces sequence-contiguous blocks with
hierarchical clustering of atomic density gradients, reducing degrees of freedom by 85–90 %
relative to standard blocking with "good agreement" to standard RTB and "superior correlation
with B-factors compared with 1-4 residue per block RTB" [VERIFIED-ABSTRACT, _Proteins_ 80:1766–79
(2012), doi:10.1002/prot.24072].

### 3.2 Hierarchical and mixed coarse-graining

Doruker, Jernigan and Bahar coarse-grained influenza hemagglutinin (`N` = 1509) to `N/2`, `N/10`,
`N/20` and `N/40` along the backbone:

> "High correlations (>0.95) between residue fluctuations are obtained for the first dominant
> (slowest) mode of motion between the original model and the coarse-grained models… the dominant
> motions of protein structures are robust enough to be captured at extremely high levels of
> coarse-graining."

[VERIFIED-ABSTRACT, _J Comput Chem_ 23:119–27 (2002), doi:10.1002/jcc.1160]. At 1/40 the
reconstruction step (§12) recovers the all-residue first-mode shape at correlation 0.73, with
computation reduced "by about three orders of magnitude" [VERIFIED-ABSTRACT, ibid.].

Mixed-level coarse-graining — full resolution in a region of interest, coarse elsewhere — is
Kurkcuoglu, Jernigan and Doruker, _Polymer_ 45:649–657 (2004),
doi:10.1016/j.polymer.2003.10.071, titled "Mixed levels of coarse-graining of large proteins using
elastic network model succeeds in extracting the slowest motions". Bibliographic record verified
via Crossref; **no abstract or full text was retrieved this session**, so the supporting numbers
are [UNVERIFIED]. The idea is directly usable for us — keep the active site and its neighbourhood
at residue resolution and coarsen the distal bulk — but we would be adopting it on the title
alone unless the paper is landed.

### 3.3 Domain decomposition

Hinsen showed that low-frequency modes "are independent of force field details and can be
obtained with simplified mechanical models" and that these models "provide a useful measure for
rigidity in proteins, allowing the identification of quasi-rigid domains", validated on crambin,
lysozyme and ATCase [VERIFIED-ABSTRACT, _Proteins_ 33:417–29 (1998),
doi:10.1002/(sici)1097-0134(19981115)33:3<417::aid-prot10>3.0.co;2-8].

### 3.4 Rigid-cluster decomposition

FIRST counts degrees of freedom in a constraint network of covalent bonds, hydrogen bonds and
salt bridges and identifies rigid and flexible substructures from a single static structure,
"approximately a million times faster than molecular dynamics simulations"
[VERIFIED-ABSTRACT, Jacobs, Rader, Kuhn & Thorpe, _Proteins_ 44:150–65 (2001), doi:10.1002/prot.1081].

The large-scale validation is Ahmed, Villinger and Gohlke on 335 proteins: low-frequency ENM
modes "correlate very well" with MD essential-dynamics modes, and "a similar performance was
found if normal modes from RCNMA were used, despite a higher level of coarse graining". Quantitatively,
"the space spanned by the first quarter of ENM modes describes 84 % of the space spanned by the
five ED modes" [VERIFIED-ABSTRACT, _Proteins_ 78:3341–52 (2010), doi:10.1002/prot.22841]. Note
for C2: this is a _validation_ study that uses MD as the reference; nothing MD-derived enters the
coarse-graining itself, so citing it does not put MD on our prediction path.

### 3.5 Bahar's Markovian hierarchical decomposition — the closest prior art we have

Chennubhotla and Bahar's two papers are the most directly relevant work retrieved, and one of
them is `CHALLENGE.md` reference [8].

**The 2007 paper** (`CHALLENGE.md` ref 8, _PLoS Comput Biol_ 3:1716–26,
doi:10.1371/journal.pcbi.0030172, PMC1988854) is not itself a coarse-graining method — it is the
propagation metric. It measures communication by hit and commute times of a discrete Markov
process on the elastic network and proves those times "have physical origins directly relevant to
the equilibrium fluctuations of residues predicted by EN models" [VERIFIED-FULLTEXT]. Two of its
findings bear on coarse-graining:

- **Secondary structural elements emerge as efficient mediators of communication**
  [VERIFIED-FULLTEXT]. The hitting-time distributions were computed over 49,929 / 64,732 / 79,444
  residue pairs terminating on helices / strands / loops across five enzymes, and helical and
  strand residues communicate faster than coil residues [VERIFIED-FULLTEXT]. This is the physical
  argument for SSE-level coarse-graining (§7), and it comes from within our own tradition.
- Domains matter: in adenylate kinase "the communication between residue pairs belonging to
  different domains are usually slower than that between pairs in the same domain"
  [VERIFIED-FULLTEXT]. That is the physical argument for domain-level coarse-graining.

**The 2006 paper** (_Mol Syst Biol_ 2:36, doi:10.1038/msb4100075, PMC1681507) _is_ a
coarse-graining method for signal propagation, and it should be read as the baseline we must beat
or adopt. Its numbers, all [VERIFIED-FULLTEXT]:

- GroEL–GroES(ADP)₇, `n` = 8015 residues, mapped to `c` = 1316, 483, 133, 35, 21 nodes at levels
  `L` = 1–5. The coarsest level is a 380× node reduction.
- "The dimension of the reduced model, `c`, is automatically defined during the kernel selection
  at each level of the hierarchy. The method thus avoids the arbitrary choices of sampling
  density and interaction cutoff distances at different hierarchical levels."
- **Fidelity of the global modes: "the global modes are also verified to be maintained with a
  correlation coefficient of 0.99 at all levels 0 ⩽ `L` ⩽ 5 of the hierarchy."**
- **Coarse-graining improved agreement with experiment:** B-factor correlation was 0.68 at the
  full 8015-residue representation and 0.89 at level 3 (`c` = 133). "Interestingly, the full
  residue representation (with 8015 residues) yields a correlation coefficient of 0.68 that is
  lower than coarse-grained representation."

That last result is the strongest single piece of evidence in this review that low-frequency
protein dynamics is not merely _tolerant_ of coarse-graining but can be _improved_ by it — the
coarse operator averages out the high-frequency local noise that the full network carries. It
also means a compression sweep on our benchmark may show a non-monotone curve with an interior
optimum, and we should not assume monotone degradation when we design the sweep.

---

## 4. Graph coarsening and sparsification in graph theory and machine learning

Section 1 gave the theorems. This section records what the algorithms are and how they rank.

**The taxonomy.** Loukas benchmarks six families on four graphs — heavy-edge matching, local
variation (edge-based), local variation (neighbourhood-based), algebraic distance, affinity, and
Kron reduction [VERIFIED-FULLTEXT, arXiv:1808.10650 §5]. The finding: "local variation methods
outperform other coarsening methods in almost every problem instance. The gap is particularly
prominent for large reductions… Neighborhood-based contraction yields the best result overall."
At the maximum ratio the best local-variation method is "on average 3.9× better than the leading
state-of-the-art coarsening method" [VERIFIED-FULLTEXT].

**Heavy-edge matching** is the classical multigrid/METIS heuristic and is the weakest in that
comparison — on yeast at `r` = 70 %, mean relative eigenvalue error 3.390 (`k` = 10) against
0.406 for local variation (neighbourhood) [VERIFIED-FULLTEXT, Table 1]. It is fast and trivially
implementable, which makes it a legitimate _baseline_ for our sweep, not a method to ship.

**Algebraic multigrid** is the ancestor of the whole family; Loukas traces graph reduction "back
to the multigrid literature, that targets the acceleration of finite-element methods using cycles
of multi-level coarsening, lifting and refinement" [VERIFIED-FULLTEXT].

**Graclus / multilevel weighted graph cuts** is Dhillon, Guan & Kulis, _IEEE TPAMI_ 29:1944–1957
(2007), doi:10.1109/tpami.2007.1115, "Weighted Graph Cuts without Eigenvectors: A Multilevel
Approach". Bibliographic record verified via Crossref; content not retrieved this session
[UNVERIFIED]. The relevance is that it removes the eigendecomposition from the coarsening step,
which matters at our sizes only marginally (a 1000×1000 eigendecomposition is free).

**Graph pooling in GNNs.** DiffPool "learns a differentiable soft cluster assignment for nodes at
each layer" and reports "an average improvement of 5-10 % accuracy on graph classification
benchmarks"; **no formal guarantee about preserving graph structure is claimed**
[VERIFIED-ABSTRACT, arXiv:1806.08804]. MinCutPool trains a GNN to minimise a continuous relaxation
of the normalised min-cut, avoiding the spectral decomposition and generalising to out-of-sample
graphs [VERIFIED-ABSTRACT, arXiv:1907.00481]. Both are supervised or task-driven. Two objections
apply to us and both are disqualifying as stated: they carry no retention theorem, so they cannot
satisfy the challenge's "prove" clause; and any weights trained on dynamics data would put a
learned prior on the prediction path, which is where C2 bites. They belong in this review as
surveyed-and-rejected, which is a result.

**One honest limitation of this whole literature for us.** Every benchmark graph in Loukas's
comparison is either a mesh (airfoil, bunny), an infrastructure graph (minnesota) or a PPI network
(yeast, `N` = 1458, `M` = 1948, diameter 19, degrees 1–56) [VERIFIED-FULLTEXT]. **No residue
contact graph appears in any coarsening benchmark retrieved by this search.** The yeast PPI graph
is the nearest analogue and it is much sparser than a residue contact network at an 8–12 Å cutoff.
Numbers from that table are indicative for us, not transferable. Measuring `ε` on our own targets
is not optional.

---

## 5. Community detection and modular decomposition on protein networks

Modularity-based partitioning is the obvious way to coarse-grain a protein into "communities", and
the literature says it is the wrong way. This is a genuinely useful negative result.

**The methods.** Girvan & Newman, _PNAS_ 99:7821–7826 (2002), doi:10.1073/pnas.122653799;
Louvain — Blondel, Guillaume, Lambiotte & Lefebvre, _JSTAT_ 2008:P10008,
doi:10.1088/1742-5468/2008/10/p10008; Leiden — Traag, Waltman & van Eck, _Sci Rep_ 9 (2019),
doi:10.1038/s41598-019-41695-z (bibliographic records verified via Crossref; content
[UNVERIFIED]).

**The failure.** Schaub, Delvenne, Yaliraki & Barahona identify a **field-of-view limit**: an
_upper_ bound on the effective diameter of the communities a one-step method can see, distinct
from and additional to the known modularity resolution limit, which is a _lower_ bound on size.
"This field-of-view limit affects both modularity and Infomap." The cause is stated mechanically:
"one-step methods (such as modularity and Infomap) cannot detect communities with large effective
diameter, since these communities cannot be properly explored within one-step transitions"
[all VERIFIED-FULLTEXT, _PLoS ONE_ 7(2):e32210, doi:10.1371/journal.pone.0032210, PMC3288079].

**The protein evidence.** They run it on the atomistic structural graph of adenylate kinase
(214 amino acids):

| Method                               | Communities found                                                                         |
| ------------------------------------ | ----------------------------------------------------------------------------------------- |
| Modularity                           | 69                                                                                        |
| Infomap                              | 421                                                                                       |
| Hierarchical Infomap (highest level) | 58                                                                                        |
| Markov Stability, short `t`          | 206 — "the communities capture the amino acids of the protein (214 amino acids)"          |
| Markov Stability, medium `t`         | 8 — "correspond approximately to secondary structure of the protein"                      |
| Markov Stability, long `t`           | 3 — "correspond to the functional domains of the protein that operate at slow timescales" |

[VERIFIED-FULLTEXT, ibid., Figure 3 and accompanying text]. Their verdict on the one-step methods:
"The structural and geometric origin of the graph leads to a non clique-like community structure.
Again, this causes overpartitioning for both Infomap and modularity… even the highest level in
hierarchical Infomap is overpartitioned and **does not provide an appropriate coarse graining in
this case**" [VERIFIED-FULLTEXT, emphasis added].

**Why this generalises to us and not just to AdK.** The mechanism is geometric embedding. A
residue contact graph built from 3D coordinates with a distance cutoff is exactly the class of
graph the paper describes: "networks that emerge from geometric constraints can have natural non
clique-like substructures with large effective diameters" [VERIFIED-FULLTEXT]. Our graphs are that
class by construction under C6. **Running Louvain or Leiden on the residue network and using the
communities as supernodes is predicted, by a published mechanism, to over-partition.**

**Markov Stability** is the alternative. Delvenne, Yaliraki & Barahona define partition quality by
the clustered autocovariance of a Markov process on the network; "the Markov time acts effectively
as an intrinsic resolution parameter that establishes a hierarchy of increasingly coarser
communities", and it "provides a unifying framework for several standard partitioning measures:
modularity and normalized cut size can be interpreted as one-step time measures, whereas Fiedler's
spectral clustering emerges at long times". They "use it to obtain reduced descriptions for
atomic-level protein structures over different time scales" [VERIFIED-ABSTRACT, _PNAS_
107:12755–60 (2010), doi:10.1073/pnas.0903215107].

Two protein applications complete the case:

- Delmotte, Tate, Yaliraki & Barahona apply multiscale graph partitioning plus a robustness measure
  built from "biochemically-motivated surrogate random graph models" to four conformations of
  myosin tail interacting protein, recovering the closing mechanism, conserved clusters, and key
  binding residues by computational mutation [VERIFIED-ABSTRACT, _Phys Biol_ 8:055010 (2011),
  doi:10.1088/1478-3975/8/5/055010]. This is the myosin family, which is one of our arms.
- Amor, Yaliraki, Woscholski & Barahona use Markov Stability plus Markov _transients_ on the
  atomistic graph of caspase-1: the multiscale analysis shows "the active conformation has a
  weaker, less compartmentalised large-scale structure compared to the inactive conformation,
  resulting in greater intra-protein coherence and signal propagation", and the transient analysis
  from the active site "predict[s] the location of a known allosteric site in this protein"
  [VERIFIED-ABSTRACT, _Mol Biosyst_ 10:2247–58 (2014), doi:10.1039/c4mb00088a].

**Note the constraint status of that last one.** It is fully atomistic, unsupervised, uses only a
static structure, and needs no MD. It therefore satisfies C1, C2 and C6 exactly, and it is a
random-walk propagator on a graph — i.e. a _classical_ method squarely inside the space
`00-conventions.md` §5 says has already beaten every quantum readout we tried. It should be added
to the classical baseline list in §6 of the conventions rather than treated as a coarse-graining
method only.

Stochastic block models were sought and **no protein-domain application was retrieved by the
recorded search**; the multiscale-community tooling that did surface for biology is CDAPS,
which targets PPI networks rather than residue networks [VERIFIED-ABSTRACT, _PLoS Comput Biol_
17: e1008239 (2021), doi:10.1371/journal.pcbi.1008239].

---

## 6. Renormalisation-group and multiscale approaches on networks

The Laplacian renormalisation group defines a diffusion-based Kadanoff supernode construction and
a momentum-space RG "à la Wilson" for complex networks, replacing earlier approaches "based on
hidden geometries hypotheses" [VERIFIED-ABSTRACT, Villegas, Gili, Caldarelli & Gabrielli,
_Nat Phys_ 19:445–450 (2023), doi:10.1038/s41567-022-01866-8; preprint arXiv:2203.07230]. A
tutorial treatment exists (Caldarelli, Gabrielli, Gili & Villegas, _JSTAT_ 2024:084002,
doi:10.1088/1742-5468/ad57b1), as do follow-ups on equilibrium-preserving variants
(arXiv:2507.04977), Laplacian coarse graining in complex networks (arXiv:2302.07093), and
higher-order Laplacian renormalisation (arXiv:2401.11298) [all titles VERIFIED-ABSTRACT via the
arXiv listing].

**Assessment for us.** The construction is attractive because it coarse-grains by _diffusion_,
which is the same operator family our propagation metric lives in, and because it does so with a
principled scale parameter rather than a target node count. But no error bound on a preserved
observable was retrieved, no protein application was retrieved, and the motivating problem —
heterogeneous, scale-free degree distributions — is not the problem a residue contact graph
presents (degrees are bounded by packing). Real-space RG on graphs via box-covering
self-similarity was sought and **not retrieved in a form that gives a retention guarantee**.
Recorded as surveyed, not adopted [UNVERIFIED as to applicability].

---

## 7. Structure-aware protein coarse-graining

Three mappings are structure-derived rather than graph-derived, which makes them cheap, apo-only,
and interpretable to a medicinal chemist — the last being its own scored secondary objective
(`CHALLENGE.md` §4.2).

**Secondary-structure elements as nodes.** The physical justification is Chennubhotla & Bahar 2007
(§3.5): SSEs are the efficient mediators of communication, with faster hitting times for helix and
strand residues than for coil, measured over ~194k residue pairs across five enzymes
[VERIFIED-FULLTEXT]. Markov Stability recovers the SSE level _automatically_ on AdK as the
8-community robust partition [VERIFIED-FULLTEXT, §5]. Two independent lines therefore point at the
same intermediate resolution. For a 764-node myosin arm, an SSE-level map is roughly a 10–20×
reduction, which is the right order for a near-term device.

**Martini-style bead mappings.** Marrink, Risselada, Yefimov, Tieleman & de Vries, "The MARTINI
force field: coarse grained model for biomolecular simulations", _J Phys Chem B_ 111:7812–7824
(2007), doi:10.1021/jp071097f (bibliographic record verified; content [UNVERIFIED]). The elastic
network hybrid is ELNEDIN — Periole, Cavalli, Marrink & Ceruso, "Combining an Elastic Network With
a Coarse-Grained Molecular Force Field: Structure, Dynamics, and Intermolecular Recognition",
_J Chem Theory Comput_ (2009), doi:10.1021/ct9002114 [VERIFIED-ABSTRACT, via Europe PMC record].
**These map atoms to beads, i.e. they coarse-grain _below_ the residue.** Our node set is already
one node per modelled residue (ADR 0010), so Martini offers us nothing on the axis we need. Recorded
so that nobody re-searches it.

**Residue-to-fragment mappings** are the ENM hierarchical schemes already covered in §3.2 —
`N/2` … `N/40` backbone subsets (Doruker 2002) and contiguous residue blocks (RTB).

**One method from `CHALLENGE.md`'s own reference list.** Zheng's allosteric-site predictor samples
conformations "along each of the lowest 30 modes" solved from an ENM, then reconstructs atomistic
backbone and sidechains and runs a pocket finder, taking "1-2 h for an average-size protein of
~400 residues" and applied to GluR2, GroEL, a GPCR and **myosin**
[VERIFIED-ABSTRACT, _J Chem Phys_ 158:124127 (2023), doi:10.1063/5.0141630, PMC10066797]. This is
`CHALLENGE.md` reference [1]. It is a coarse-grained-mode method that predicts allosteric sites
under C1, C2 and C6, and it uses the _lowest 30 modes_ — a concrete, published answer to "how many
slow modes carry the site signal", which is the number our compression must preserve.

---

## 8. Question (b): what to report to demonstrate retention

The candidate measures, ranked by how well the literature validates them.

| Measure                                                                                    | Validated where                                                                                                                              | Verdict for our report                                                                                                                                                      |
| ------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Restricted spectral approximation constant `ε`** on `R = U_k`                            | Loukas 2019, computed per graph per ratio; `ε < 1` at `r` ≤ 70 % on all four test graphs                                                     | **Report it.** It is the quantity the theorems bound. It is the single number that turns "we coarse-grained" into "we proved"                                               |
| **Mean relative eigenvalue error** `(1/k) Σ                                                | λ̃_i − λ_i                                                                                                                                    | / λ_i`over the lowest`k`                                                                                                                                                    | Loukas 2019 Tables 1–2, `k` = 10, 40, 80 | **Report it.** Cheap, standard, and directly comparable to a published table. Use `k` = 10 and `k` = 30 (the latter matching Zheng's mode count) |
| **Spectral distance** `SD_full`, `SD_part` via the lifted graph                            | Jin, Loukas & JaJa; bounded by merge-profile discrepancy (Props 4.1, 4.2)                                                                    | **Report `SD_part`.** It needs only `n` eigenvalues of the fine graph, not `N`                                                                                              |
| **Rank correlation of residue scores** (Spearman / Kendall), fine vs projected-back coarse | Not validated as a coarsening metric in any retrieved paper; **it is the endpoint-relevant one for us** because our deliverable is a ranking | **Report it, and label it as our own endpoint measure, not a borrowed one.** Kendall τ-b for ties                                                                           |
| **Recovery of the known site at each ratio** (recall@5, DCC)                               | This is the challenge's own primary criterion applied per ratio                                                                              | **Report it — it is the actual proof of "retains the essential _signal_".** Everything above proves retention of the _operator_; only this proves retention of the _answer_ |
| **Correlation of the slowest mode / fluctuation profile**, fine vs reconstructed           | Doruker 2002 (>0.95 at `N/2`…`N/40`, 0.73 reconstructed at 1/40); Chennubhotla & Bahar 2006 (0.99 global modes at all levels)                | **Report it.** Two independent protein papers use exactly this, so our numbers are comparable to theirs                                                                     |
| **Effective-resistance / commute-time distortion** between retained node pairs             | Kron: exact invariance (Dörfler & Bullo Thm 8). Sparsifiers: approximately preserved (Spielman & Srivastava)                                 | **Report it if and only if the propagator readout is resistance-like.** For Kron it is a proof by equality and costs nothing                                                |
| **Eigenvalue interlacing gaps** `λ̃_k − λ_k` and `λ_{k+N−n} − λ̃_k`                          | Loukas Thm 2.3; Jin Prop 4.1; Dörfler & Bullo Thm 7                                                                                          | **Report as a sanity check only.** A violation means a bug. Satisfaction proves nothing                                                                                     |

**One measure the literature validates that we should also carry:** the eigenspace angle
`‖sin Θ(U_k, P^⊤Ũ_k)‖_F`, bounded by Loukas Theorem 3.4. It is the measure that fails first when
the spectral gap `λ_{k+1} − λ_k` closes, and it is the early-warning signal for §11's failure mode.

**Statement of comparability, per convention §2.** All the published numbers above are on
different graphs with different densities. `0.406` mean relative eigenvalue error at `r` = 70 % on
a 1458-node PPI network does not predict the same number on a 764-node residue contact network.
The published tables set our _format_; only our own sweep sets our numbers.

---

## 9. Question (c): what breaks first, and are the low-frequency modes robust or fragile?

**Answer: the low-frequency modes are the robust part, and this is the strongest and most
consistently replicated finding in the file.** Five independent lines agree.

1. **Theory.** Loukas Theorem 3.3's bound is tighter for smaller eigenvalues — "one also deduces
   that it is stronger for smaller eigenvalues", collapsing at `k` = 2 to
   `γ₁λ₂ ≤ λ̃₂ ≤ γ₂(1+ε₂)²/(1−ε₂²) λ₂` [VERIFIED-FULLTEXT, arXiv:1808.10650].
2. **Theory.** The MSM eigenvalue bound `E(δ) ≤ λ₁(m−1)δ²` is stated for the `m` **dominant**
   (slowest) eigenvalues, and is quadratic in the projection error
   [VERIFIED-FULLTEXT, Djurdjevac, Sarich & Schütte Thm 4.2]. Coarse-graining is designed around
   the slow subspace, not in spite of it.
3. **Protein empirics.** "Slow modes rather than fast modes are robust" is a section heading in
   the ENM review: 5–6 lowest Tirion elastic-network modes suffice to describe the slow modes of
   the all-atom CHARMM potential; the same 5–6-dimensional invariant subspace survives the
   cross-check over two further CG-EN models including ANM; and "similar slowest (1st) modes can
   be obtained through a hierarchy of coarse-grained (HCA) schemes for a given EN model"
   [VERIFIED-FULLTEXT, Yang & Chng, _Bioinform Biol Insights_ 2:25–45 (2008),
   doi:10.4137/bbi.s460, PMC2735964, summarising Nicolay & Sanejouand 2006 and Doruker 2002].
4. **Protein empirics.** Global modes retained at correlation 0.99 across a 380× node reduction
   [VERIFIED-FULLTEXT, Chennubhotla & Bahar 2006]; slowest mode at correlation > 0.95 at `N/40`
   [VERIFIED-ABSTRACT, Doruker 2002].
5. **Mechanism.** The review gives the reason rather than the observation: "The insensitivity to
   minor structural changes is understood to stem from the collective nature of the low-frequency
   modes. The collective oscillation is a joint effect of many interacting pairs, summed up to
   approach a universal form that is governed by the central limit theorem, regardless of the
   details of pair positions or potentials" [VERIFIED-FULLTEXT, ibid.].

**So what does break first?** Four things, in this order.

- **The fast modes.** They go first, by all five lines above. For allostery this is a feature, not
  a loss — but only if our metric is genuinely slow-mode-dominated. If our propagator readout
  turns out to depend on short-time / high-frequency structure, the entire argument above inverts
  and coarse-graining becomes hostile. **This must be checked before the sweep is designed, not
  after**, by decomposing the metric over the mode spectrum.
- **The rate is steep and it is a cliff, not a slope.** "For most cases the eigenvalue error jumps
  by almost an order of magnitude whenever `r` increases by 20 %" [VERIFIED-FULLTEXT, Loukas 2019
  §5.2]. On yeast at `k` = 10 the best method goes 0.003 → 0.034 → 0.406 across `r` = 30 → 50 →
  70 %. Our sweep must therefore be dense in `r`, not three points, and it must be expected to
  find a knee.
- **Near-degeneracy at the truncation point.** Loukas Theorem 3.4 has `1/(λ_{k+1} − λ_k)` in
  front. If the protein's spectrum is near-degenerate at `k`, the eigenspace guarantee blows up
  even while the eigenvalues stay accurate — the modes _mix_ rather than shift. A ranking built on
  mode content would then be wrong while every eigenvalue diagnostic looks healthy. This is the
  subtle failure and the eigenspace-angle measure of §8 is the only one that catches it.
- **Sparsity, for Kron reduction specifically.** Densification to a clique (Dörfler & Bullo Thm 6)
  preserves resistance perfectly and destroys the hardware-friendly topology. Signal retained,
  device lost.

**One counterintuitive finding worth carrying into the report.** Coarse-graining improved the
B-factor correlation from 0.68 to 0.89 on GroEL–GroES [VERIFIED-FULLTEXT, Chennubhotla & Bahar
2006]. Degradation with `r` is **not guaranteed monotone**. A sweep designed on the assumption of
monotone decay could miss an interior optimum and report the wrong recommended ratio.

---

## 10. Question (d): the reverse map — projecting a coarse score back to residues

Our deliverable is a per-residue top-5 hit list in author numbering (`CLAUDE.md`, Conventions).
A coarse score must therefore be lifted back. Four published mechanisms exist, and they differ in
whether they invent resolution.

**1. Linear lifting / prolongation (the multigrid inheritance).** Loukas's framework carries
`P` (reduction) and `P⁺` (lifting) as a matched pair, with `x̃ = P⁺Px`. Restricted spectral
approximation is _defined_ on the lifting error `‖x − x̃‖_L` [VERIFIED-FULLTEXT, Def 3.1]. Two
structural properties matter: the nullspace is preserved in both directions, `P 1_N = 1_n` and
`P⁺ 1_n = 1_N` (Property 2.8), and for any `x` in the range of `Π = P⁺P`, `x̃ = x` exactly
(Property 2.4) [both VERIFIED-FULLTEXT]. Jin, Loukas & JaJa make the lifted graph the _definition_
of their spectral distance, and prove the lifted eigenvectors `u_l = C u_c` are eigenvectors of
the lifted Laplacian (Property 4.3) [VERIFIED-FULLTEXT].

**This is honest and it is flat.** A hard-partition lifting assigns every residue in a supernode
the same score. It invents no resolution — and it also cannot rank within a supernode. If a
supernode is 20 residues, we can return the supernode but not a top-5 residue list from inside it.
**That is a hard constraint on how coarse we may go: the final supernodes must be small enough
that a supernode is a usable answer for a medicinal chemist.**

**2. Soft ownership (Chennubhotla & Bahar 2006) — the best answer retrieved.** Their reduction
operator `R` and expansion operator `K` are probabilistic, not deterministic. `K` is an `n × c`
non-negative kernel matrix whose columns are latent probability distributions each summing to 1;
`R_ij` is the "ownership of node `i` in the high-resolution representation by a node `j` in the
low resolution", with `Σ_{j=1}^{c} R_ij = 1`. Propagation runs coarse (`q^{k+1} = M̃ q^k`) and
expands to fine by `p^k = K q^k`. Multi-level composition is `R^{(0,L)} = Π_{l=0}^{L−1} R^{(l,l+1)}`
[all VERIFIED-FULLTEXT, _Mol Syst Biol_ 2:36]. Because ownership is fractional, **two residues in
the same coarse cluster receive different fine-scale scores** — the resolution comes from the
ownership weights, which were derived from the fine graph, not invented. Their fidelity test is
exactly the round trip we need: coarse-grain, do the GNM analysis in the reduced space,
reconstruct, compare — giving the 0.99 global-mode correlation and the improved B-factor
correlation quoted above.

Note also that the residues with _intermediate_ ownership are precisely their "messengers", the
high-communication-entropy residues they nominate as sites of high allosteric potential
[VERIFIED-FULLTEXT]. The reverse map and the allosteric readout are the same object in their
formulation. That is an unusually clean fit to our problem and it should be tested directly.

**3. Sliding-subset reconstruction (Doruker, Jernigan & Bahar 2002).** At coarse-graining 1/40
they reconstruct the mode shape "for all residues by successively selecting different subsets of
residues, shifting one residue at a time"; the reconstructed first mode correlates 0.73 with the
all-residue case [VERIFIED-ABSTRACT, _J Comput Chem_ 23:119–27]. This is an ensemble-of-coarsenings
answer: run `m` distinct coarse models with offset node selections and average per residue. It
gives genuine per-residue resolution at the cost of `m` runs — and `m` runs of a small circuit may
be cheaper on hardware than one run of a large one, which makes it more attractive for us than it
was for them.

**4. Local refinement (multigrid V-cycle).** Coarsen, solve, lift, then relax on the fine graph.
Named in Loukas's framing of the multigrid inheritance ("cycles of multi-level coarsening, lifting
and refinement") [VERIFIED-FULLTEXT] but **no protein application and no retention bound for the
refined solution was retrieved by this search**. Recorded as an option, not a recommendation.

---

## 11. Question (e): is there a published coarse-graining specifically for fitting a protein network onto quantum hardware?

**No such method was retrieved by the recorded search.** Per ADR 0019 and convention §2 this is a
statement about our search, not about the world.

What the search did return, and why each falls short:

- **arXiv:2608.05491**, "A Quantum Circuit Framework for Protein Ensemble-Level Energetics"
  (Patil, Bonde & Choubey, 2026). Residue-level gate-based framework, one two-state qubit per
  amino acid, with "a structure-informed entanglement block" for the interaction network. It is
  _residue-level_, i.e. it coarse-grains atoms to residues — the resolution we already start at.
  It does **not** reduce node count below one-per-residue, reports no compression ratio, and makes
  no claim of topological or spectral preservation. Test systems are Trp-cage miniproteins
  (1L2Y, 9GDL) at ~20 residues, i.e. two orders of magnitude below where the problem appears
  [VERIFIED-ABSTRACT, via the arXiv abstract page].
- **arXiv:2604.17486**, "Continuous-time quantum-walk centrality for protein residue interaction
  networks" (2026) — this is the preprint corresponding to the CTQW result already recorded in
  `00-conventions.md` §5. It maps the weighted adjacency matrix to a Hamiltonian and runs on IBM
  superconducting hardware, and it contains **no coarse-graining or network-reduction step at all**
  [VERIFIED-ABSTRACT, via the arXiv abstract page].

**The gap is real and it is ours to fill.** Every retention theorem in §1 was proved for a
classical Laplacian or a classical Markov propagator. **None of them is stated for a unitary
propagator `exp(-iHt)`.** Whether `‖x − x̃‖_L ≤ ε‖x‖_L` on the `k` slowest eigenvectors implies a
bound on a coherent transfer amplitude between two coarse nodes is, on this search, an open
question. Two positions are defensible and we must pick one explicitly:

- **Adequate.** If our Hamiltonian is `H = L` or `H = A` and our readout is a function of the
  eigen-decomposition, then a bound on the eigenvalues and eigenspaces bounds the readout by
  continuity, and the constant can be written down per metric. This is the cheap path and it is
  probably sufficient, but it must be _derived_ per metric and not waved at.
- **Insufficient.** If the readout depends on phase accumulation over long times, small eigenvalue
  errors compound as `exp(-i δλ t)` and the guarantee decays with `t`. A `δλ/λ` of 0.4 at `r` = 70 %
  would destroy any long-time interference readout while leaving every spectral diagnostic looking
  acceptable.

Deriving the unitary-propagator counterpart of Theorem 3.3 for our specific metric — even as a
one-page continuity argument with an explicit `t`-dependence — would be a genuinely novel
contribution to the submission and directly answers the challenge's "prove" clause in the quantum
setting where the existing literature does not.

---

## What this changes for our pipeline

1. **Phase 4 — adopt restricted spectral approximation as the primary proof instrument.**
   `docs/ROADMAP.md` Phase 4 already names spectral distance, rank correlation and pocket recovery.
   Add the Loukas `ε` on `R = U_k` as the fourth and lead number, because it is the only one with a
   theorem attached. Report `ε`, the mean relative eigenvalue error over the lowest `k`, and the
   eigenspace angle `‖sin Θ‖_F`, at every ratio, per target.
2. **Phase 4 — the coarsening algorithm should be local-variation (neighbourhood) contraction,
   with heavy-edge matching as the baseline.** Both are in the published comparison, the ranking
   between them is measured (3.9× at high ratio), and both keep the graph sparse — which matters
   for the Phase 3 depth budget. Kron reduction is a second arm to run _only_ where the readout is
   resistance-like, and its densification cost must be reported alongside its exact-invariance
   guarantee. Touches: a new `network/` coarsening module.
3. **Phase 4 — do not use Louvain, Leiden or Infomap communities as supernodes.** A published
   mechanism (the field-of-view limit) predicts over-partitioning on geometrically embedded graphs,
   and it was demonstrated on an atomistic protein graph — 69 and 421 communities on a 214-residue
   protein. If a community-based arm is run, it must be Markov Stability with a Markov-time sweep,
   which recovers the residue, secondary-structure and domain levels on the same protein.
4. **Phase 4 — the compression-ratio sweep must be dense and must not assume monotone decay.**
   Published behaviour is an order-of-magnitude jump per 20 % of ratio, and one protein result shows
   coarse-graining _improving_ agreement with experiment. Sweep at 10 % steps and look for both the
   knee and a possible interior optimum. This changes the exit criterion's shape, not its content.
5. **Phase 2 — check the mode composition of the chosen metric before Phase 4 starts.** The entire
   retention argument rests on the metric being slow-mode dominated. Decompose the metric over the
   eigenspectrum on one target. If it is not slow-mode dominated, every guarantee in §1 becomes
   inapplicable and the coarse-graining plan needs rebuilding. Cheap to run, expensive to skip.
6. **Phase 4 — the reverse map should be soft ownership, not hard partition assignment.** Hard
   lifting cannot rank within a supernode and therefore caps the achievable ratio at supernodes of
   about five residues. Chennubhotla & Bahar's `R`/`K` operator pair gives fractional per-residue
   scores from fine-graph information, and its "messenger" residues are themselves an allosteric
   readout. Sliding-subset reconstruction (Doruker) is the fallback if soft ownership underperforms.
7. **Phase 1.4 / conventions §6 — add two classical baselines that this review surfaced.**
   Markov-transient analysis from the active site (Amor 2014, caspase-1) and hierarchical Markov
   propagation (Chennubhotla & Bahar 2006) are unsupervised, apo-only, MD-free, contact-topology
   methods that predict allosteric sites. They satisfy C1, C2 and C6 exactly and are therefore in
   the same bar-setting class as APOP and ESSA. They are not in `00-conventions.md` §6 and should be.
8. **Phase 3 — record that sparsification and coarsening are different levers.** Spectral
   sparsification with an `(1±ε)` quadratic-form guarantee reduces the interaction-term count at
   fixed `N`. It buys depth, not qubits. That belongs in file 08's budget, and the two must not be
   reported as one compression number.
9. **Phase 3/4 — a derivation is owed.** No retrieved theorem covers a unitary propagator. Write
   the continuity argument from Theorem 3.3 to our specific metric, with explicit `t`-dependence,
   or state in the report that the retention proof covers the operator spectrum and not the
   long-time coherent readout. Either is defensible; silence is not.
10. **Myosin sizing.** At 764 nodes an SSE-level map is roughly 10–20× and lands in the range where
    both Loukas's `ε` and Chennubhotla & Bahar's fidelity results are comfortable. That, not a
    round number of qubits, is the defensible starting ratio for the sweep.

---

## Method

**Databases and routes.** arXiv API (`export.arxiv.org`), arXiv search UI and abstract pages via
WebFetch, ar5iv HTML full text (`ar5iv.labs.arxiv.org`), Europe PMC search and `fullTextXML`,
NCBI E-utilities `esearch`/`efetch`, PMC article pages, Crossref `api.crossref.org` (used for
bibliographic verification only, where Europe PMC had no record), and direct PDF retrieval plus
local `pdftotext` for two Freie Universität Berlin preprints.

**Queries run.** arXiv: `all:"graph coarsening" AND all:"spectral"` (17); `all:"restricted spectral
approximation"` (3); `ti:"Graph reduction with spectral and cut guarantees"` (1);
`all:"spectrally approximating large graphs"` (1); `all:"graph sparsification by effective
resistances"` (4); `all:"Kron reduction"` (8). arXiv search UI: `Laplacian renormalization group`;
`coarse-graining protein network quantum computer qubit allosteric`; `"elastic network"
coarse-graining qubit quantum algorithm protein` (0 results); `protein allosteric quantum walk
coarse-grained network reduce qubits` (0 results); `"quantum walk" protein residue network`;
`spectral coarsening geometric operators low frequency eigenvalues` (0 results). Europe PMC:
`TITLE:"coarse-grained" AND TITLE:"normal mode" AND ABSTRACT:protein` (8);
`TITLE:"Markov propagation" AND ABSTRACT:allosteric` (1); community-detection/protein/allosteric
combinations (1); `TITLE:"Markov transient"` / `multiscale community detection` (3); six exact-title
lookups for ENM coarse-graining papers (1 each); `ABSTRACT:"quantum" AND ABSTRACT:"coarse-grain*"
AND ABSTRACT:"protein" AND (ABSTRACT:"qubit" OR ABSTRACT:"quantum computer")` (0);
`ABSTRACT:"quantum" AND ABSTRACT:"allosteric" AND (ABSTRACT:"network" OR ABSTRACT:"graph")`,
2018–2026 (11, none relevant). E-utilities `efetch` on 18 PMIDs for author/volume/page verification.
Crossref bibliographic lookups: 12.

**Screening.** Roughly 130 records surfaced; 41 screened in; **11 read in full text**
(Loukas 2019; Dörfler & Bullo 2013; Spielman & Srivastava 2008; Jin, Loukas & JaJa 2018;
Chennubhotla & Bahar 2006; Chennubhotla & Bahar 2007; Schaub et al. 2012; Yang & Chng 2008;
Sarich, Noé & Schütte 2010; Djurdjevac, Sarich & Schütte 2012; Nilsson Jacobi 2010).

**Stopping rule.** Stopped when each of the six mandated topic areas had at least one source read
in full text or, failing that, an explicit record that it had not been reached; and when the
question-(a) theorem set had stopped growing across three consecutive query families.

**What could not be reached.**

- The arXiv API returned HTTP 429 repeatedly through the second half of the session; roughly a
  third of intended arXiv queries were rerouted through the arXiv search UI and abstract pages via
  WebFetch, which returns less structure. Some arXiv-only work may have been missed.
- The WebSearch budget for the session (200 calls) was exhausted by earlier files, so no general
  web search was available. Crossref and WebFetch substituted for it.
- **Paywalled, bibliographic record only, content [UNVERIFIED]:** Kurkcuoglu, Jernigan & Doruker
  (_Polymer_ 2004, mixed coarse-graining); Dhillon, Guan & Kulis (_TPAMI_ 2007, Graclus);
  Buchholz (_J Appl Prob_ 1994, lumpability); Meyer (_SIAM Review_ 1989, stochastic
  complementation); Marrink et al. (_J Phys Chem B_ 2007, Martini); Liu et al. (_ACM TOG_ 2019,
  spectral coarsening of geometric operators — ACM returned HTTP 403); Villegas et al.
  (_Nat Phys_ 2023 — nature.com requires authentication; abstract obtained from the arXiv listing
  instead). Deuflhard & Weber (PCCA+) content came from a search-engine rendering of the
  ScienceDirect abstract, tagged [VERIFIED-ABSTRACT].
- **Not retrieved:** any stochastic-block-model application to protein domain decomposition; any
  real-space box-covering RG on graphs with a retention guarantee; any coarsening benchmark that
  includes a residue contact graph; any retention theorem stated for a unitary propagator; and any
  coarse-graining method designed specifically to fit a protein network onto quantum hardware.
