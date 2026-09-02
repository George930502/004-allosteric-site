# Fact-check of the ten load-bearing claims

**Scope:** independent retrieval and verification of the ten claims in files 01–09 that carry
the most weight for the Phase 2 method choice. It checks the source, the quote and the
numbers. It deliberately excludes claims that no decision rests on, and it does not re-argue
any method's merit — only whether the cited evidence says what the review says it says.
**Sibling files:** `00-conventions.md` for the evidence tags and the file format; files 01–09
for the claims themselves and the reasoning built on them.
**Retrieved:** 2026-08-25.

---

## 1. Verdict summary

| #   | Claim (short)                                                        | Source                                                        | Tag                   | Verdict                                                                                                       |
| --- | -------------------------------------------------------------------- | ------------------------------------------------------------- | --------------------- | ------------------------------------------------------------------------------------------------------------- |
| 1   | Geometric locality kills exponential quantum advantage               | Sakamoto & Fujii, Quantum 10, 2182 (2026); arXiv:2505.10445v4 | `[VERIFIED-FULLTEXT]` | **CONFIRMED WITH QUALIFICATION**                                                                              |
| 2   | Protein connectivity matrix read-in is Ω(N)                          | arXiv:2411.03972                                              | `[VERIFIED-FULLTEXT]` | **CONFIRMED WITH QUALIFICATION**                                                                              |
| 3   | Parameter budget T ≤ ε²·N                                            | Caro et al., Nat Commun 13:4919; arXiv:2111.05292             | `[VERIFIED-FULLTEXT]` | **NOT CONFIRMED** (misapplication)                                                                            |
| 4   | Givens network: exactly N depth, N²/2 gates                          | Kivlichan et al., PRL 120, 110501; arXiv:1711.04789           | `[VERIFIED-FULLTEXT]` | **NOT CONFIRMED** (quote misattributed)                                                                       |
| 5   | Classiq synthesis fails beyond N = 16                                | arXiv:2603.05479v1                                            | `[VERIFIED-FULLTEXT]` | **CONFIRMED**                                                                                                 |
| 6   | Src allosteric decay, d½ = 18.24 Å vs 7.45 Å                         | Beltran et al., Sci Adv 12(7):eaea2726; PMC12893324           | `[VERIFIED-FULLTEXT]` | **CONFIRMED WITH QUALIFICATION** (two of three cited sources do not contain the numbers)                      |
| 7   | ESM-1b attention beats random on 15/24 vs Ohm 7/24, EVcouplings 5/24 | none given                                                    | `[UNVERIFIED]`        | **COULD NOT RETRIEVE**                                                                                        |
| 8   | AlloBench: no tool above 60 % accuracy; APOP 15 % at JI > 0.5        | doi:10.1021/acsomega.5c01263; PMC12059942                     | `[VERIFIED-FULLTEXT]` | **CONFIRMED**                                                                                                 |
| 9   | APOP apo top-3 = 11/15 = 73 % and 86 % = 11/14                       | doi:10.1093/bioinformatics/btad275; PMC10185404               | `[VERIFIED-FULLTEXT]` | **CONFIRMED WITH QUALIFICATION** (the review quotes the paper correctly; the paper's own arithmetic is wrong) |
| 10  | Effective resistance exactly preserved under Kron reduction          | Dörfler & Bullo, arXiv:1102.2950                              | `[VERIFIED-FULLTEXT]` | **CONFIRMED**                                                                                                 |

Three claims (3, 4, 7) do not survive as written. Four more (1, 2, 6, 9) need a qualification
before anything is built on them.

---

## 2. Claim-by-claim detail

### Claim 1 — the geometric-locality theorem

**Source.** Kazuki Sakamoto and Keisuke Fujii, _On the quantum computational complexity of
classical linear dynamics with geometrically local interactions: Dequantization and
universality_, Quantum 10, 2182 (2026), doi:10.22331/q-2026-08-03-2182, arXiv:2505.10445v4.
Title and authors confirmed.

**Verdict: CONFIRMED WITH QUALIFICATION.** The result is real, and the sampling route is
covered. But the review's use of it — closing an entire class of approaches — is wider than
the theorem, on three separate grounds.

**Retrieved quote (published abstract).**

> First, we dequantize the quantum algorithm for simulating short-time (polynomial-time)
> dynamics of such systems. This implies that the problem of simulating this dynamics does
> not yield any exponential quantum advantage.

The review's quoted string extends this to "...does not yield any exponential quantum
advantage **in both time and space complexities**." The four-word extension did not come back
in the abstract or in the retrieved body text. Treat the shorter sentence as the quotable one.

**Exact definition of geometrically local (Definition 5, verbatim).**

> Consider the finite-volume lattice with sites labeled as i={1,…,N}, where the structure of
> the lattice is determined by some set of bonds. Let d(i,j) be the distance between the sites
> i and j, and 𝒩(·)∈ℝ₊→ℕ be a locality function defined as: 𝒩(r)≔max_{i={1,…,N}}|{j|d(i,j)≤r}|

A matrix is (r₀, 𝒩(r₀))-geometrically local if `A_ij = 0 for d(i,j) > r₀` and `𝒩(r) = poly(r)`
for any r. For a D-dimensional system, `𝒩(r₀) = O(r₀^D)`.

**Does a residue contact matrix satisfy it?** Yes, on the property the proofs actually use, and
only under one indexing. If the index set is residues embedded in R³ and d is Euclidean
distance between residue centroids, then `A_ij = 0` beyond the contact cutoff holds _by
construction_, and 𝒩(r) = O(r³) because protein packing density is bounded — so the definition
is met with D = 3. A protein is not a lattice, but the polynomial ball-growth condition is what
the classical algorithm exploits, and a protein satisfies it. The definition is **not** met if
the index is the sequence position: long-range tertiary contacts have large |i − j|, and a
contact matrix in sequence indexing is not geometrically local at all. Any argument that
invokes this theorem must say which indexing it assumes.

**What "short-time" means, quantitatively (verbatim).**

> Throughout this work, we refer to the regime t=polylog(N)=poly(n) as short-time evolution,
> and t=poly(N)=exp(n) as long-time evolution.

with N = 2ⁿ. This is the qualification that matters most. **N is the matrix dimension and
n = log₂N is the qubit count.** The dequantization covers evolution times polynomial in the
_number of qubits_, i.e. polylogarithmic in the matrix dimension.

**Further stated conditions.** Eigenvalues of A have non-positive real parts; ‖A‖ = poly(n);
‖e^{At}x(0)‖ ≥ 1/poly(n). The last is not free — it requires the solution not to decay
super-polynomially, which a dissipative propagator on a contact graph can violate.

**Classical runtime.** Theorem 1 estimates v†P(A)u to within ε; Theorem 3 is titled
"Classical sampling simulation of short-time dynamics", so the sampling loophole is closed as
the review says. The dimension dependence is explicit:

> Emphasizing the dependence on t, ε and δ, given the spatial dimension D, Õ(t^{2+D}log(1/δ)/ε²).

Polynomial, but the exponent grows with D. At D = 3 this is t⁵.

**Three conditions our problem does not meet, in order of importance.**

1. **The theorem is short-time only, and the same paper's third result points the other way.**
   The abstract's third finding — long-time (t = poly(N) = exp(n)) dynamics is captured by
   exponential-time, polynomial-space quantum computation — "suggests a super-polynomial time
   advantage when restricting the computation to polynomial-space, or an exponential space
   advantage otherwise." Citing this paper to close _all_ propagation methods reverses half of
   what it says. A method whose claim rests on long-time propagation is untouched by it.
2. **Our N is far too small for the asymptotic regime to have content.** A catalytic domain is
   ~200–500 residues, so n ≈ 8–9 qubits. "polylog(N) versus poly(N)" is not a distinction that
   exists at N = 300. The honest statement for our pipeline is simpler and stronger than the
   theorem: at a few hundred nodes there is no asymptotic separation to be had by anyone.
3. **It bounds exponential advantage only.** It says nothing about polynomial speedups, and
   nothing about whether a quantum _observable_ is more informative — which is the axis our own
   benchmark actually failed on (`00-conventions.md` §5).

**What changes if this is wrong.** If the review keeps the claim as written, it closes methods
the paper leaves open — specifically anything relying on long-time propagation. That is a
false negative on a whole branch, and it is the expensive direction of error. Rewrite the claim
to name the short-time restriction and the small-N argument separately.

---

### Claim 2 — the protein read-in bound

**Source.** Zhenning Liu, Xiantao Li, Chunhao Wang, Jin-Peng Liu, _Toward end-to-end quantum
simulation for protein dynamics_, arXiv:2411.03972.

**Verdict: CONFIRMED WITH QUALIFICATION.** The quote is real. The use made of it inverts the
authors' own conclusion.

**Retrieved quote (verbatim).**

> the matrix K is incompressibly determined by the coordinates of Cα atoms, and since the
> number of atoms is O(N), we need to load O(N) bits

Supporting sentence:

> the protein structure information has high information entropy and cannot be compressed with
> a ratio better than a constant value

**Paraphrase drift.** The review writes "coordinates of N atoms"; the paper writes "coordinates
of Cα atoms", with the count separately stated as O(N). Substantively the same, but the
paper is specific that the object is a coarse-grained Cα network — which is exactly our
setting, so the correction is in our favour and worth making.

**The qualification, which is the real finding.** The authors state the Ω(N) bound and then
argue past it:

> A sparse data access oracle to K can be implemented in O(log N) depth using O(N log N) gates

Their position is that O(N) _total gate count_ is acceptable because the _depth_ is
polylogarithmic, which they compare to classical ROM access and present as compatible with
exponential speedup in a fault-tolerant setting. The paper is a pro-quantum paper. Citing it as
evidence that read-in defeats quantum advantage reports its lemma and drops its conclusion.

**What changes if this is wrong.** If the review uses this to rule out amplitude-encoded
methods on read-in cost alone, a reader who opens the source finds the opposite argument, and
the review loses credibility on the surrounding section. The defensible version: read-in costs
Ω(N) gates; whether that matters depends on whether depth or gate count is the binding
resource, and at N ≈ 300 neither is.

---

### Claim 3 — the parameter budget

**Source.** Matthias C. Caro et al., _Generalization in quantum machine learning from few
training data_, Nat Commun 13:4919, arXiv:2111.05292.

**Verdict: NOT CONFIRMED.** The bound exists; the form quoted is wrong and the direction of
inference is wrong.

**Retrieved quote (Theorem 1, verbatim).**

> For a QMLM with T parameterized local quantum channels, with high probability over training
> data of size N, we have that gen(α∗)∈O(√(T log T/N))

> For any ε>0, we can, with high success probability, guarantee that gen(α∗)⩽ε, already with
> training data of size N∼T log T/ε²

**What the symbols count.** T = number of trainable local quantum gates/channels. N = **training
dataset size**, i.e. the number of training examples. The error term is `gen(α*)`, the
generalisation gap. The paper also gives a refinement to O(√(K log K/N)) when only K ≪ T gates
change substantially during training.

**Three errors in the review's version.**

1. **The log factor is dropped.** Inverting the paper's own sufficiency statement gives
   `T log T ≲ ε²N`, not `T ≤ ε²N`. At N = 150 and ε = 0.2, ε²N = 6, so `T log T ≲ 6` gives
   T ≈ 3–4, not 6. The review's arithmetic is not conservative — it is optimistic by roughly a
   factor of two.
2. **The O(·) hides an unspecified constant.** Both statements are asymptotic. No exact integer
   gate budget can be extracted from them at all. "Six trainable gates" has a false precision
   that the source does not support at any N.
3. **The direction of inference is reversed, and this is the serious one.** The theorem is a
   worst-case _upper bound_ on the generalisation gap — a sufficient condition for good
   generalisation. It says: with T gates, N ∼ T log T/ε² data _guarantees_ ε. It does **not**
   say that T above the budget will fail. The paper itself notes the bounds are "highly
   general" and hold "at worst", and that its own QFT-compilation experiments generalise better
   than the theory predicts. Reading it as a hard ceiling is a category error.

**One more thing to settle before using it.** N counts training _examples_. "150 proteins"
gives N = 150 only if the training unit is a whole protein. If the model is trained on
per-residue labels, N is ~10⁴–10⁵ and the budget moves by two orders of magnitude. The review
must state its training unit before quoting any budget.

**What changes if this is wrong.** As written, the claim rules out any variational method with
more than six gates. That is a hard architectural constraint derived from a misread bound, and
it would shape three months of work. The correct statement is far weaker: with ~150 whole-protein
training examples, worst-case generalisation guarantees are vacuous for any non-trivial circuit,
so a variational arm cannot be justified by this bound — but neither is it forbidden by it. The
argument against a supervised variational arm has to be made on other grounds.

---

### Claim 4 — the exact-circuit result

**Source.** Ian D. Kivlichan et al., _Quantum simulation of electronic structure with linear
depth and connectivity_, PRL 120, 110501 (2018), arXiv:1711.04789.

**Verdict: NOT CONFIRMED.** The quoted string is verbatim from the paper, but it describes a
different result from the one the review attaches it to.

**Retrieved quote (abstract, verbatim).**

> We show that by using an arrangement of gates that we term the fermionic swap network, we can
> simulate a Trotter step of the electronic structure Hamiltonian in exactly N depth and with
> N²/2 two-qubit entangling gates, and prepare arbitrary Slater determinants in at most N/2
> depth, all assuming only a minimal, linearly connected architecture.

"Exactly N depth and with N²/2 two-qubit entangling gates" is the **fermionic swap network for a
Trotter step of the electronic structure Hamiltonian**. It is not the Givens-rotation network,
and it is not a statement about a single-particle basis rotation.

**What the paper actually says about an arbitrary single-particle unitary (verbatim).**

> There are (N choose 2) elements below the diagonal, the number of Givens rotation required is
> (N choose 2)

> gate depth of 2N−3 is sufficient to implement the basis change

**Corrected numbers.** An arbitrary N × N single-particle basis rotation on a linear
nearest-neighbour array takes N(N−1)/2 Givens rotations at depth **2N − 3**, not N. The N/2
figure in the abstract is for preparing an arbitrary Slater determinant, a strictly easier task.

**What survives.** The substance the review wants does hold: the construction implements an
arbitrary N × N unitary, not a special case, and restricted to the single-excitation sector it
realises that unitary directly. Depth is still linear in N and connectivity is still linear
nearest-neighbour. Only the constant is wrong — by a factor of about two — and the quote is
attached to the wrong theorem.

**What changes if this is wrong.** C3 requires reporting circuit depth for every quantum method.
A depth figure that is low by 2× and sourced to a quote about a different algorithm will not
survive a reviewer who opens the reference. Replace the quote and use 2N − 3.

---

### Claim 5 — the Classiq risk

**Source.** Viraj Dsouza, Weronika Golletz, Dimitrios Kranas, Bakhao Dioum, Vardaan Sahgal,
Eden Schirman, _Quantum Simulation of Coupled Harmonic Oscillators: From Theory to
Implementation_, arXiv:2603.05479v1, submitted 2026-03-05.

**Verdict: CONFIRMED.** Retrieved twice, identically.

**Retrieved quote (verbatim).**

> The synthesis of deeper circuits becomes computationally demanding for larger N, and the
> synthesis engine could not reliably generate circuits beyond N=16 within reasonable classical
> runtime and memory limits.

A second, independent statement covers the oracle/QSVT implementation:

> For larger system sizes (N>16), the synthesis engine was unable to generate the corresponding
> quantum circuits within practical classical computational limits.

So the ceiling is not an artefact of one implementation — it recurs across two of the three
realisations the paper builds. Resource estimates are quoted up to N = 256 for initial state
preparation alone; the end-to-end synthesis for Hamiltonian simulation stops at N = 16.

**One qualification on "Classiq co-authored".** One author of six, Weronika Golletz, is at
Classiq Technologies; the other five are at the Washington Institute for STEM Entrepreneurship
and Research. The paper is not a Classiq publication in the sense the phrase implies. This
makes the finding _stronger_, not weaker — a mostly-external group reporting the ceiling is
better evidence than the vendor reporting it, but the review should describe the authorship
accurately.

**What changes if this is wrong.** This is the one fact named as decisive for tooling. It is
confirmed, so the tooling decision stands: do not plan a Classiq-synthesised end-to-end circuit
above N = 16 without first reproducing the synthesis at our target size.

---

### Claim 6 — the allosteric decay law

**Source (corrected).** Antoni Beltran, Mohsin M. Naqvi, Andre J. Faure, Ben Lehner, _The
allosteric landscape of the Src kinase_, Science Advances 12(7):eaea2726, 11 February 2026,
PMC12893324.

**Verdict: CONFIRMED WITH QUALIFICATION.** The number pair is exactly right. The citation
bundle is not.

**Retrieved quotes (verbatim).**

> corresponding to a 50% reduction of allosteric effects over a distance d₁/₂ = 7.45 Å

> the distance dependence when only considering the major allosteric sites is much weaker
> (k = −0.038 ± 0.005 Å⁻¹, d₁/₂ = 18.24 Å)

**What was fitted.** Average per-site mutation-effect magnitude (|ΔΔG_a|) against minimum heavy
atom distance to the active site, fitted as an exponential y = a·e^{bx}. The 7.45 Å fit is over
all 252 residues of the kinase domain. The 18.24 Å fit is over the 42 major allosteric sites
only (7 in the N lobe, 35 in the C lobe). The distance is to the nucleotide, the catalytic D389
or the phosphosite.

**Citation correction — two of the three sources given do not contain these numbers.**

- doi:10.1101/2025.10.20.683418 is _TF-MAPS: fast high-resolution functional and allosteric
  mapping of DNA-binding proteins_ (Li & Lehner), on HNF1A, FOXG1 and FOXP1. It supports the
  general statement that allostery is "distance-dependent, anisotropic" but contains neither
  18.24 nor 7.45.
- doi:10.1101/2025.06.20.660748 is _The evolution of allostery in a protein family_
  (Martí-Aranda & Lehner), on five homologous human proteins. It supports "conserved
  distant-dependent allosteric decay across the protein core" but contains neither number.

Only PMC12893324 carries the pair. Cite it alone for the numbers, and cite the other two for
the general law if that is what they are for.

**Two qualifications before building a method on this.**

1. **The 18.24 Å figure is conditioned on a selection.** The 42 "major allosteric sites" were
   _chosen_ for being enriched in activity-modulating mutations. Fitting decay over a set
   selected for having large effects will flatten the distance dependence relative to the
   background by construction. The contrast between 18.24 and 7.45 is therefore partly a
   selection artefact and cannot be read as "allosteric signal travels 2.4× further" without a
   separate argument.
2. **One protein, one domain, measured not predicted.** Both numbers come from deep mutational
   scanning of a single kinase domain. Using 18.24 Å as a calibrated prior for other targets is
   an extrapolation across ~250 residues of one protein. It does not violate C1 or C2 — the
   numbers are experimental, not holo-derived and not MD-derived — but any hyperparameter taken
   from it must be chosen on the `development` tier of the secondary set, not asserted.

**What changes if this is wrong.** A proposed method is built on this. The number survives; the
selection conditioning means it must not be used as a fixed length scale without tuning, and
the two spurious citations must be dropped from the numeric claim.

---

### Claim 7 — the zero-shot PLM result

**Verdict: COULD NOT RETRIEVE.** No source was supplied with the claim, and six independent
searches did not find one.

Searches run, all on 2026-08-25:

| Query                                                                          | Database             | Hits | Relevant |
| ------------------------------------------------------------------------------ | -------------------- | ---- | -------- |
| `"allosteric" AND "ESM-1b" AND "attention"`                                    | Europe PMC, core     | 21   | 0        |
| `"allosteric" AND "zero-shot" AND ("protein language model" OR "ESM")`         | Europe PMC, core     | 43   | 0        |
| `"EVcouplings" AND "Ohm"`                                                      | Europe PMC           | 0    | 0        |
| `FULL_TEXT:"EVcouplings" AND FULL_TEXT:"allosteric" AND FULL_TEXT:"attention"` | Europe PMC           | 0    | 0        |
| `"allosteric" AND "attention map"`                                             | Europe PMC, core     | 13   | 0        |
| `"allosteric site" AND "language model" AND SRC:"PPR"`                         | Europe PMC preprints | 2    | 0        |
| `abs:"allosteric" AND abs:"attention" AND abs:"protein language model"`        | arXiv                | 1    | 0        |
| `abs:"allosteric" AND abs:"zero-shot"`                                         | arXiv                | 1    | 0        |
| `all:"allosteric" AND all:"attention maps"`                                    | arXiv                | 0    | 0        |

The two preprints that came closest — Allo-PED (doi:10.1101/2025.03.28.645953) and DeepAllo
(doi:10.1101/2024.10.09.617427) — are supervised pLM allosteric-site predictors, not zero-shot
attention-map readouts, and neither benchmarks against Ohm or EVcouplings.

Per `00-conventions.md` §2 this is recorded as **not retrieved by the recorded search**, not as
false. The claim may rest on an internal analysis or a source not indexed by Europe PMC or
arXiv. It must carry `[UNVERIFIED]` until a DOI is supplied.

**What changes if this is wrong.** A zero-shot pLM baseline that beats Ohm and EVcouplings with
zero allosteric labels would be a strong C1/C2-compliant comparator and would raise the bar our
method must clear. If it does not exist, the bar in `00-conventions.md` §6 is unchanged. Do not
add it to the bar list until sourced.

---

### Claim 8 — the AlloBench collapse

**Source.** Dibyajyoti Maity and Baofu Qiao, _AlloBench: A Data Set Pipeline for the Development
and Benchmarking of Allosteric Site Prediction Tools_, ACS Omega, doi:10.1021/acsomega.5c01263,
PMC12059942.

**Verdict: CONFIRMED.** Both the sentence and the APOP number.

**Retrieved quote (verbatim).**

> Surprisingly, none of these programs could achieve an accuracy of more than 60%, even with a
> very low JI cutoff of approximately zero.

**Retrieved quote on the leakage control (verbatim).**

> The UniRef50 cluster IDs (UniProt reference clusters with at least 50% sequence identity) were
> obtained for the 268 unique UniProt IDs of these proteins. AlloBench proteins with these
> UniRef50 cluster IDs were dropped to remove any related proteins in addition to the proteins
> of the training sets.

**APOP at Jaccard > 0.5:** 15 %, second best behind PASSer (Ensemble) at 18 %. Confirmed.

**Definition of "accuracy", which must travel with the number.** "the percentage of proteins in
their top predictions with JI larger than a varying threshold", evaluated at cutoffs 0, 0.1,
0.2, 0.3, 0.4 and 0.5. This is a Jaccard-overlap criterion on predicted versus annotated pocket
residue sets, and it is a much harder criterion than APOP's own "known pocket within top 3
rank". The two numbers in claims 8 and 9 are **not** measuring the same thing and must never be
differenced.

**One small correction.** `00-conventions.md` §6 says "no tool of eight". The paper benchmarks
APOP, Ohm, ALLO, Allosite, AllositePro, STRESS, AlloPred and three PASSer variants — ten table
entries across eight distinct non-PASSer-variant tools. Say "ten configurations" or list them.

**What changes if this is wrong.** This claim sets the realism of every published number in the
review. It is confirmed, so the deflation stands.

---

### Claim 9 — the APOP apo number

**Source.** Ambuj Kumar, Burak T. Kaynak, Karin S. Dorman, Pemra Doruker, Robert L. Jernigan,
_Predicting allosteric pockets in protein biological assemblages_, Bioinformatics 2023,
doi:10.1093/bioinformatics/btad275, PMID 37115636, PMC10185404.

**Verdict: CONFIRMED WITH QUALIFICATION.** The review transcribes the paper faithfully. The
paper contradicts itself.

**Retrieved quotes (verbatim, both).**

> APOP successfully predicts allosteric pockets in all holo-structures (15/15) and 11 out of 15
> pockets in apo structures in this set within the top 3 rank.

> Although conformational rearrangements seem to affect the success rate of our predictions for
> apo structures, we still achieve a satisfactory prediction rate of 86% (11/14), excluding one
> cryptic pocket (PDB ID: 1ZG4).

**Resolution — what each denominator means.**

- **15** is the full matched apo/holo set. 11 of 15 apo top-3 successes = **73.3 %**.
- **14** is the same set with one case, the cryptic pocket in PDB 1ZG4, removed.

**The red flag is real, and it is the paper's, not the review's.** 11/14 = **78.6 %**, not 86 %.
86 % corresponds to 12/14. The two figures in that sentence cannot both be right. Removing one
failed case from a set of 15 with 11 successes gives 11/14 = 78.6 %; there is no reading under
which the stated fraction yields the stated percentage.

**Which number to use.** **11/15 = 73 %.** It is the unconditioned figure, it is stated plainly,
and its arithmetic checks. The 86 % figure is doubly unusable: it is internally inconsistent,
and it is produced by dropping a case _after_ seeing that it failed — which for our purposes is
exactly the wrong exclusion, since a cryptic pocket in an apo structure is precisely the regime
the challenge scores on (C1, `CONTEXT.md` on cryptic versus allosteric).

Note also for comparability: 15/15 holo versus 11/15 apo is the apo-versus-holo degradation the
review wants, and it is on the same set, so that comparison is sound.

**What changes if this is wrong.** The APOP bar in `00-conventions.md` §6 quotes 73 %. That
number is correct and should stay. Delete the 86 % figure from the review rather than reporting
both, and add one line saying the source's own arithmetic for it does not check.

---

### Claim 10 — the Kron reduction theorem

**Source.** Florian Dörfler and Francesco Bullo, _Kron Reduction of Graphs with Applications to
Electrical Networks_, arXiv:1102.2950.

**Verdict: CONFIRMED.** Exact equality, not an approximation.

**Retrieved quote (verbatim).**

> the effective resistance among boundary nodes is invariant under the Kron reduction process

**Definition used.**

> R_ij ≜ (e_i−e_j)ᵀQ†(e_i−e_j) = Q†_ii + Q†_jj − 2Q†_ij

with Q† the Moore–Penrose pseudoinverse.

**Stated conditions.**

1. Q ∈ R^{n×n} is a symmetric, irreducible loopy Laplacian.
2. The underlying graph is undirected, connected and weighted.
3. The retained (boundary) set α ⊊ I_n satisfies |α| ≥ 2.
4. Q(α,α) is non-singular — guaranteed by irreducibility.

A residue contact network with non-negative edge weights and a single connected component
satisfies all four. Weight signs matter: a Laplacian with negative edge weights is not covered.

**The caveat that matters for coarse-graining.** What is preserved is _effective resistance
between retained nodes_, exactly. Kron reduction does **not** preserve the Laplacian's
eigenvalues, its eigenvectors, or a propagator built from them. If the coarse-graining
validation (Phase 4) rests on anything other than an effective-resistance readout — a normal
mode, an eigenvector centrality, a walk amplitude — the exactness does not transfer and has to
be argued or measured separately.

**What changes if this is wrong.** It is not wrong. The usable consequence is narrower than
"coarse-graining is exact": it is "coarse-graining is exact for one specific readout". A
coarse-graining claim in the report must name the readout.

---

## 3. What this changes for our pipeline

- **Method selection (Phase 2).** Claim 1 as written closes more than the theorem supports.
  Reopen any long-time-propagation method the review closed on it. The correct grounds for
  scepticism about our problem are the small N (~8–9 qubits' worth of dimension) and the
  measured failure of eleven quantum observables in `00-conventions.md` §5 — not this theorem.
- **Method selection (Phase 2), variational arm.** Claim 3 does not support a six-gate ceiling.
  If a supervised variational arm is to be excluded, exclude it on the training-unit and
  label-scarcity argument, stated explicitly, and state N in training examples not proteins.
- **Circuit resource reporting (C3, Phase 3).** Use depth 2N − 3 and N(N−1)/2 Givens rotations
  on a linear array for an arbitrary single-particle basis rotation. Retire the "exactly N
  depth" quote, which belongs to a Trotter-step result.
- **Tooling (Phase 3).** Claim 5 is confirmed. Treat N = 16 as the demonstrated end-to-end
  synthesis ceiling for that toolchain and reproduce synthesis at our target size before
  committing.
- **Proposed decay-prior method.** Claim 6's numbers hold but are selection-conditioned and
  come from one kinase domain. Any length-scale hyperparameter derived from them is chosen on
  the `development` tier of the secondary set, never asserted.
- **The bar in `00-conventions.md` §6.** APOP stays at 11/15 = 73 %; drop the 86 % figure and
  note the source's arithmetic. AlloBench's 60 % ceiling and APOP's 15 % at JI > 0.5 stand,
  with the Jaccard criterion stated beside them so they are never differenced against top-3
  numbers. Do not add the zero-shot pLM comparator to the bar until claim 7 has a DOI.
- **Coarse-graining validation (Phase 4).** Kron reduction is exact for effective resistance
  only. Name the readout in any exactness claim.

## 4. Method

**Databases.** arXiv (`export.arxiv.org/api/query`, `arxiv.org/abs`, `arxiv.org/html`,
`ar5iv.labs.arxiv.org`), Europe PMC search and `fullTextXML`, PMC article pages,
quantum-journal.org, biorxiv.org, nature.com.

**Retrieval per claim.** Claims 1, 2, 3, 4, 5, 6, 8, 9, 10 — full text or a published abstract
retrieved and quoted directly. Claim 5 was retrieved twice from independent prompts against the
same document to confirm the wording character-for-character, and claim 9's two conflicting
sentences were re-retrieved with an explicit verbatim-transcription request to rule out a
transcription artefact.

**Counts.** Ten claims screened in. Nine sources retrieved, one not found. Nine claim-7 search
queries run across three databases (table in §7 above), 81 results screened, 0 relevant.

**Stopping rule.** For claims 1–6 and 8–10: stop once the exact quoted string is returned from
the primary source and its stated conditions are recorded. For claim 7: stop after nine queries
across arXiv, Europe PMC abstracts, Europe PMC full text and Europe PMC preprints returned
nothing matching the reported design (ESM-1b attention, 24 proteins, Ohm and EVcouplings
comparators).

**What could not be reached.**

- `pubs.acs.org/doi/10.1021/acsomega.5c01263` returned HTTP 403; the open-access copy at
  PMC12059942 was used instead and carries the full text under CC BY.
- `nature.com/articles/s41467-022-32550-3` redirected to an authentication endpoint; the arXiv
  version 2111.05292 was used, which is the same work.
- `arxiv.org/html/2411.03972v3` returned HTTP 404; ar5iv served the full text.
- The four-word extension "in both time and space complexities" in the claim-1 quote was not
  returned by any retrieval of the abstract or body.
- The full verbatim statement of Theorem 3 in arXiv:2505.10445v4 was truncated in retrieval; its
  title and subject ("Classical sampling simulation of short-time dynamics") were confirmed, so
  the sampling claim is recorded as verified at theorem-statement level, not at proof level.
- No source at all was located for claim 7.
- WebSearch was unavailable for this session (budget exhausted); all retrieval was by direct
  fetch against the endpoints listed in `00-conventions.md` §3.
