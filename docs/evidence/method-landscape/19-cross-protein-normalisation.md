# Cross-protein normalisation: derived, zero-parameter rules that make a hyperparameter mean the same physical thing on every protein

**Scope:** the single question of what makes a structural-network quantity _comparable between
proteins_. Contact-cutoff rules that are derived rather than fitted, the known N-scaling of graph
observables and their standard normalisations, source-geometry normalisation, the ENM/GNM/ANM
parameter conventions and their provenance, how network biology and graph signal processing make a
spectral quantity comparable across graphs, and the cases where a proposed normalisation has been
shown not to help. Every rule is classified by whether it has fitted parameters, because our tuning
set is four arms and a fitted rule is unfalsifiable at that size. It deliberately excludes which
edge rule is more physical, which is `13-graph-construction.md` §Q1–Q2; the cancellation of a radial
trend _within one protein_, which is `14-distance-confound.md` §Q4; and anything learned or
pretrained, which is `15-ai-preprocessing.md`.
**Sibling files:** `13-graph-construction.md` (the graph as a modelling choice),
`14-distance-confound.md` (within-protein detrending and matched nulls),
`15-ai-preprocessing.md` (learned front ends), `07-coarse-graining-scalability.md` (compression),
`../exploration/data/30-frozen-graph-profile.md` (the measured spread this file has to close),
`../exploration/results/44-stability-and-noise.md` §6 (the one normalisation we already falsified),
`../exploration/results/45-source-choice.md` (size-matched sources, already implemented),
`00-conventions.md` (evidence rules).
**Retrieved:** 2026-08-27.

**Databases searched:** PubMed E-utilities (`esearch.fcgi`, `efetch.fcgi`), PMC article pages,
arXiv API (`export.arxiv.org/api/query`), ar5iv HTML, Crossref REST (`api.crossref.org/works`),
publisher pages (PNAS, OUP), and general web search until the session's search budget was
exhausted after two queries. Europe PMC was not attempted: `14-distance-confound.md` recorded it
returning empty on ten consecutive attempts through this fetch route on 2026-08-26. Full query list
in §Method.

---

## 0. The one-paragraph answer

**Three of the six questions are largely moot for our endpoint, and the reason is one line of
arithmetic.** AUC is invariant under any strictly increasing transform of a score vector, so any
normalisation that multiplies or shifts _every residue of one protein by the same amount_ — divide
by N, divide by `λ_max`, divide by the mean — changes nothing that `score_arm` reports. The same
holds for the top-5 deliverable, which is also rank-based. Only three classes of rule can move a
per-protein rank endpoint: (a) rules that change the **operator or its hyperparameter**, (b) rules
that are **non-uniform across residues**, and (c) rules that change the **evaluation strata**. That
screen kills most of the size-normalisation literature as a _method_ change while leaving it fully
relevant to _reporting_ and to any pooled or thresholded step. Of what survives, our own measurement
already decides the ordering: `44-stability-and-noise.md` §6 normalised the walk's clock by the
spectral gap, cut the within-protein window sensitivity of `ctqw_average_transfer` almost in half
(0.079 → 0.045 AUC) and moved the between-arm spread by 0.011 out of 0.5627, which is 2 % of itself.
The rule worked exactly as designed and did not help, because between-protein variance is not routed
through the time scale. `30-frozen-graph-profile.md` says where it _is_ routed: the graphs are
near-universal as graphs (mean contact number 8.9–10.3, clustering 0.460–0.515, adjacency `λ₁`
10.40–11.80 across a 7.2× size range) while the source geometry varies 20× in size and 3× in
candidate-to-source distance. So the ranked candidate list in §7 leads with **source-geometry**
normalisations — a per-residue z-score against a size- and degree-matched random-source ensemble
(the construction Guney et al. use for drug–disease proximity, doi:10.1038/ncomms10331), and
radial-_quantile_ stratification of the endpoint rather than fixed-Å stratification — and places
spectral and cutoff rules below them, with the gap clock recorded as falsified. On cutoffs the
literature's own answer is unflattering to per-protein tuning: the two derived criteria that were
retrieved either produce a **universal constant** (minimum mutual information at 5 Å across distinct
proteins, doi:10.1002/prot.26154) or a per-protein value that is itself **size-confounded**
(percolation of the giant component, whose critical threshold "is generally higher for bigger
proteins", doi:10.1529/biophysj.105.064485), and the ENM field's own best-known per-protein fit —
cutoff optimised against B-factors — is undercut by two papers showing B-factors are the wrong
target (doi:10.1021/ct400399x, doi:10.1093/bioinformatics/btm625).

---

## 1. The two screens a candidate must pass before it is worth running

Both are derived here from arithmetic we already hold. They cost nothing and they eliminate most
proposals.

### 1.1 The rank-invariance screen

`score_arm`'s endpoint is an AUC over midranks and the deliverable is a top-5 list. Both are
invariant under a strictly increasing map applied to the whole score vector of one protein. Let
`s ∈ ℝ^N` be the scores on protein _p_ and let a proposed normalisation be `s ↦ φ_p(s)`.

- If `φ_p` is a scalar affine or monotone map (`s/N`, `s/λ_max`, `(s − mean)/sd`, `log s`), then
  every AUC, every rank correlation and every top-5 list is unchanged. **The rule is a no-op for the
  primary endpoint.** It still matters for reporting, for pooling scores across proteins into one
  figure, for score-space (not rank-space) ensembling, and for any absolute threshold.
- If `φ_p` acts differently on different residues (subtract a per-residue expectation; divide by a
  per-residue standard deviation), it is not monotone in `s` and it _can_ move the endpoint.
- If the rule instead changes the operator, the cutoff, the clock or the evaluation strata, it can
  move the endpoint by construction.

[UNVERIFIED — derived here.] This screen is why §Q2 below is short relative to its literature: the
analytic scaling forms are real and well established, and almost none of them touch our number.

### 1.2 The sensitivity bound

Let `A(p, θ)` be the endpoint on protein _p_ at hyperparameter `θ`, and let a derived rule replace a
fixed `θ₀` with `θ*(p)` read off _p_'s own structure. Write `R_within = max_p sup_θ |A(p,θ) −
A(p,θ₀)|` over the range of `θ` the rule can reach. Any spread statistic across proteins — range,
standard deviation, worst-case — can move by at most about `2·R_within`, because the rule only ever
slides each protein along its own `θ` curve.

**The gap clock is the worked example and it validates the bound.** `R_within` for
`ctqw_average_transfer` under the `range` clock is 0.079 AUC; the between-arm spread is 0.668. The
bound permits at most ≈ 0.16 of spread reduction; the measured reduction was 0.011
[VERIFIED-FULLTEXT, `../exploration/results/44-stability-and-noise.md` §6]. The ratio of between- to
within-variance got **worse**, 8.5× → 14.5×, precisely because the clock shrank the denominator
without touching the numerator [ibid.].

**The operational form.** Before implementing any derived rule, measure two numbers: (a) the
between-protein spread of the _quantity the rule equalises_, and (b) `R_within`, the endpoint's
sensitivity to that quantity inside one protein. A rule needs both to be large. The gap clock had
(a) = 21.7× and (b) small; the spectral-range clock has (a) = 1.09× and is therefore a no-op by
construction. This is a one-afternoon pre-screen and it is the cheapest thing in this file.

### 1.3 The four-tier taxonomy used throughout

| Tier      | Meaning                                                                                                                                                                                             | Admissible for us                                                  |
| --------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| **(i)**   | Derived from theory. No free constant at all (Maxwell counting; `0 ≤ λ(L_sym) ≤ 2`; `H/log N`)                                                                                                      | Yes                                                                |
| **(ii)**  | Derived from the protein's own structure. A constant exists but the protein sets it (percolation threshold of _this_ graph; isostatic cutoff of _this_ graph; the protein's own distance quantiles) | Yes                                                                |
| **(iii)** | Fitted once, globally, and then frozen (GNM's 7.0 Å; ANM's 15–24 Å; the 5 Å mutual-information optimum)                                                                                             | Usable as an inherited constant, but it is a constant, not a rule  |
| **(iv)**  | Fitted per protein against an external target (cutoff optimised against that protein's B-factors)                                                                                                   | No. Four arms cannot falsify it, and §Q6 shows the target is wrong |

**The trap the brief names, restated.** "Hold the mean degree constant" is tier (iii) — a fitted
constant in disguise — _unless_ the target degree is itself derived. Maxwell counting supplies one
derived target and §Q1.2 gives it.

---

## Q1 — Contact-cutoff rules that are derived rather than tuned

### Q1.1 Percolation of the giant component (tier ii, size-confounded)

The one large study retrieved that sets the threshold from the structure itself is Brinda and
Vishveshwara's protein structure graph. Edges are weighted by an interaction strength `I_ij`, "the
number of distinct atom pairs between the side chains of amino acid residues i and j, which come
within a distance of 4.5 Å, normalized by factors N_i and N_j specific to each residue type"
[VERIFIED-FULLTEXT, doi:10.1529/biophysj.105.064485, PMC1366981]. Sweeping the strength cutoff
`I_min` produces a percolation-like transition in the size of the largest cluster, and the
transition value `I_critical` is read off per protein.

Two numbers from the same paper decide how useful this is to us. Across 232 proteins, "the standard
deviation of I_critical is 0.9 around a mean of ∼3.9" and ">85% of the proteins have an I_critical
varying between 3.0 and 5.0" [VERIFIED-FULLTEXT, ibid.]. But: "I_critical is a function of the size
of the protein and is generally higher for bigger proteins", with bin means rising from ≈ 3.25 % at
100–200 residues to > 4.25 % at 400–1300 residues [VERIFIED-FULLTEXT, ibid.].

**Read those two together and the criterion is half a normalisation.** It is genuinely derived and
genuinely per-protein, and it removes most of the between-protein variation in edge density — but
it leaves a systematic residual trend _with N_, which is the exact axis a cross-protein rule is
supposed to close. The abstract-level summary of the same paper says the transition occurs "within a
narrow cutoff range regardless of protein size" [VERIFIED-ABSTRACT, PMID 16150969]; the full text
qualifies it. Where the two differ, the full text binds.

A weaker but strictly zero-parameter cousin of the same idea is the **connectivity threshold**: the
smallest cutoff at which the graph has one component. On our fourteen frozen apo graphs this is
already satisfied — "Every graph is connected. One component on all fourteen" and "No isolated
residue exists at the frozen cutoff" [VERIFIED-FULLTEXT,
`../exploration/data/30-frozen-graph-profile.md` §4]. So the connectivity threshold lies _below_
4.5 Å on every arm, and adopting it would move every arm's cutoff down by an unknown and
protein-specific amount. That is a measurable, cheap experiment and it is in §7.

### Q1.2 Rigidity and isostatic counting (tier i for the target, tier ii for the cutoff)

This is the only route retrieved that yields a _derived mean degree_, which is what a
constant-mean-degree rule needs in order not to be a fitted constant.

**Maxwell counting.** A network of N point sites in d = 3 with central-force springs has 3N degrees
of freedom and `N⟨k⟩/2` scalar constraints. Setting constraints equal to 3N − 6 gives
`⟨k⟩ = 6 − 12/N → 6`. The isostatic mean coordination for a central-force network in d dimensions is
`z = 2d` [UNVERIFIED — derived here]. The bond-bending analogue used for network glasses percolates
at a different and lower value: Micoulaut and Phillips give a "percolative transition at the mean
coordination number r̄ = 2.4" [VERIFIED-ABSTRACT, arXiv:cond-mat/0210100, Phys Rev B 67:104204].

**Our graphs against that target.** Mean contact number spans 8.9 to 10.3 at the frozen 4.5 Å
heavy-atom rule [VERIFIED-FULLTEXT, `30-frozen-graph-profile.md` §3.3]. The constraint ratio
`⟨k⟩/6` is therefore 1.48 to 1.72: our networks are 48–72 % overconstrained relative to
isostaticity, and uniformly so — which is another statement of "the graphs are near-universal as
graphs" [UNVERIFIED — arithmetic derived here from that file's table].

**The honest limitation, and it downgrades the rule for us.** Maxwell counting is a statement about
a _vector_ network — 3 degrees of freedom per node. Our propagation operator is a scalar adjacency
or Laplacian, 1 degree of freedom per node, for which the same counting gives `⟨k⟩ = 2`: a tree.
That is degenerate and useless. So the isostatic cutoff rule is only physically meaningful if the
observable is the vector ENM (ANM/PRS), not the scalar walk [UNVERIFIED — derived here]. It stays on
the list because `anm_perturbation_response` is in our battery, and because the rule is a genuinely
zero-parameter per-protein cutoff, but it should not be applied to a CTQW.

**The pebble game and the sweep-and-find-the-transition idea.** Jacobs, Rader, Kuhn and Thorpe's
FIRST applies graph theory to the protein's covalent, hydrogen-bond and salt-bridge constraint
network, counting degrees of freedom and identifying rigid and flexible substructures
[VERIFIED-ABSTRACT via web search result and Wiley DOI record, doi:10.1002/prot.1081, Proteins
44(2):150–165, PMID 11391777]. The rule that matters here is how the hydrogen-bond energy threshold
is chosen: Rader, Hespenheide, Kuhn and Thorpe locate the unfolding transition at "the inflection
point in the change in the number of independent bond-rotational degrees of freedom (floppy modes)"
as atomic coordination decreases [VERIFIED-ABSTRACT, doi:10.1073/pnas.062492699, PNAS 99:3540–5].
**That is a tier (ii) rule in exactly the form we want:** sweep the threshold, take a derivative,
pick the inflection, no fitted constant. It transfers to a distance cutoff directly — sweep the
cutoff, count floppy modes by Maxwell counting, take the inflection.

**The evidence it improves cross-protein comparability is absent, and there is evidence against
robustness.** No paper was retrieved that measures a rigidity-derived cutoff against a fixed cutoff
on a cross-protein prediction task. Wells, Jiménez-Roldán and Römer applied pebble-game rigidity
analysis to multiple crystal structures of each of several proteins and concluded that "rigidity
analysis is best used as a comparative tool to highlight the effects of structural variation"
[VERIFIED-ABSTRACT, arXiv:0810.1833, doi:10.1088/1478-3975/6/4/046005, Phys Biol 6:046005]. An apo
crystal structure is exactly a structure with variation of that kind, and our own measurement puts a
number on the same worry: rebuilding the graph after 1.0 Å coordinate noise leaves classical scorers
at ρ ≈ 0.91 and quantum scorers at ρ ≈ 0.63 [VERIFIED-FULLTEXT,
`../exploration/results/44-stability-and-noise.md` §1]. A rule that reads a derivative off a swept
curve is more perturbation-sensitive than the curve, not less.

### Q1.3 Information-theoretic cutoff selection (tier iii in practice, and C2-encumbered)

Sobieraj and Setny swept residue distance cutoff and contact-formation probability and minimised
mutual information — least redundancy — across the resulting protein structure networks. "We found
that the minimum in mutual information is universally achieved at the cutoff length of 5 Å,
irrespective of the applied contact formation probability threshold in all considered, distinct
proteins" [VERIFIED-ABSTRACT, doi:10.1002/prot.26154, Proteins 89:1333–1339].

**Two things follow, and they point in opposite directions.** The criterion is derived, which is
what we asked for; but its answer is the _same on every protein_, which means it is not a
cross-protein normalisation at all — it is a principled derivation of a universal constant, and
adopting it would change our cutoff once and equally everywhere. Second, the construction takes
contact-formation probabilities from atomistic MD, so running the criterion ourselves is a **C2
violation**. Inheriting the constant is not. `13-graph-construction.md` §Q2 already cites this paper
for the edge-definition question; the use here is different and the C2 note is new.

### Q1.4 The first minimum of the radial distribution function (tier ii, unsourced)

The standard physical-chemistry rule for defining a coordination shell is the first minimum of the
pair radial distribution function, which is read off the sample itself and has no fitted constant.
Applied per protein to the inter-residue distance histogram it is a tier (ii) cutoff rule. **No
paper applying this specific criterion to protein residue contact networks was retrieved by the
recorded search** [UNVERIFIED — derived here]. It is cheap enough to measure directly on our own
fourteen graphs and is in §7 for that reason.

### Q1.5 What the field actually uses, so the baseline is stated

The retrieved values are constants, and different groups fit different ones: ≤ 7.0 Å for Cα pairs in
the original GNM [VERIFIED-ABSTRACT, doi:10.1016/S1359-0278(97)00024-2]; 7.5 Å in Yang's
rotation-penalty ENM [VERIFIED-ABSTRACT, doi:10.1016/j.bpj.2011.02.033]; "a physically realistic
cutoff distance, R(c) approximately 8 Å" in Zheng's unification [VERIFIED-ABSTRACT,
doi:10.1529/biophysj.107.125831]; a swept range of 7.3–15 Å over 1250 proteins in oGNM
[VERIFIED-ABSTRACT, doi:10.1093/nar/gkl084]; 15–24 Å for the ANM [VERIFIED-ABSTRACT,
doi:10.1093/bioinformatics/btl448 — record confirmed from the OUP article page, DOI not
independently re-derived, see §Method]. **The spread of the field's own constants is larger than the
spread our own eight-graph sweep moved the answer by (0.031 mean AUC,
`13-graph-construction.md`).** That is the argument that the cutoff is not where the between-protein
problem lives.

---

## Q2 — Size and scale normalisation for network observables

Read §1.1 first: for a per-protein rank endpoint these are no-ops. They are stated because they
govern reporting, pooling, and any step with an absolute threshold — and because getting the
analytic form right is what lets us _say_ a quantity is intensive rather than assume it.

| Observable                 | Raw scaling with N                                                                           | Standard normalisation                                            | Range after             | Provenance                                                                                                                                                                                                       |
| -------------------------- | -------------------------------------------------------------------------------------------- | ----------------------------------------------------------------- | ----------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Betweenness `g_i`          | `Σ_i g_i ≈ (N²/2)·⟨ℓ⟩`, so mean `g ≈ (N/2)·⟨ℓ⟩`                                              | `ĝ = 2g/((N−1)(N−2))`                                             | `[0,1]`, mean ≈ `⟨ℓ⟩/N` | derived here; pair count is combinatorial                                                                                                                                                                        |
| Betweenness vs degree      | `g ~ k^η`                                                                                    | none; report `η`                                                  | —                       | `η = 2` for trees or low loop density, `η < 2` with more loops [VERIFIED-ABSTRACT, doi:10.1140/epjb/e2004-00111-4]                                                                                               |
| Closeness                  | `Σ_j d_ij` grows with N                                                                      | `(N−1)/Σ_j d_ij`                                                  | intensive               | derived here                                                                                                                                                                                                     |
| Participation ratio        | `PR = 1/Σ_i p_i² ∈ [1,N]`                                                                    | `PR/N`                                                            | `(0,1]`                 | derived here; the ENM field's "degree of collectivity" is the entropy form of the same idea [bibliographic record confirmed via Crossref, doi:10.1063/1.469213; formula UNVERIFIED — not retrieved this session] |
| Shannon entropy            | `H ∈ [0, log N]`                                                                             | `H/log N`                                                         | `[0,1]`                 | derived here; used as `S/log₂N` for network comparison [VERIFIED-FULLTEXT, doi:10.1103/PhysRevX.6.041062]                                                                                                        |
| Laplacian spectrum         | `λ(L)` unbounded above, scales with degree                                                   | use `L_sym = I − D^{-1/2}AD^{-1/2}`                               | `0 ≤ λ ≤ 2` exactly     | [VERIFIED-FULLTEXT, arXiv:1805.10712]                                                                                                                                                                            |
| Heat-kernel trace          | `h_t = Σ_j e^{−tλ_j}`; its Taylor expansion "contains information about the number of nodes" | `h_t/n` (empty-graph) or `h_t/(1 + (n−1)e^{−t})` (complete-graph) | size-invariant          | [VERIFIED-FULLTEXT, arXiv:1805.10712]                                                                                                                                                                            |
| Total effective resistance | `Kf = N Σ_{k≥2} 1/λ_k`, so mean pairwise `R = 2Σ_k(1/λ_k)/(N−1)`                             | divide a source resistance by the protein's own mean pairwise `R` | intensive               | derived here                                                                                                                                                                                                     |
| Filter/clock scale         | any `f(tL)` depends on `t·λ_max`                                                             | rescale the spectrum by `λ_max`                                   | `[−1,1]`                | the standard Chebyshev construction in graph signal processing [VERIFIED-ABSTRACT, arXiv:0912.3848]                                                                                                              |

**Two consequences worth stating.**

_First, our default clock is already the field's standard normalisation._ `_time_grid`'s
`scale="range"` divides by the spectral range, which is the `λ_max` rescaling that graph signal
processing uses for Chebyshev filters. The range varies by 1.09× across the four development arms,
so this normalisation is, on our inputs, indistinguishable from a wall clock
[VERIFIED-FULLTEXT, `44-stability-and-noise.md` §6]. That is not a defect of the rule; it is a
measurement that the quantity it equalises is already equal.

_Second, the `⟨ℓ⟩ ~ N^{1/3}` assumption behind "normalised betweenness is intensive" fails
specifically on our elongated arms._ For a compact three-dimensional object the diameter should
scale as `N^{1/3}`. Taking diameter ÷ `N^{1/3}` from the frozen profile: `mkp5` 7/5.28 = 1.33,
`kras_g12c_mandated` 8/5.53 = 1.45, `bcr_abl1_corrected` 10/6.48 = 1.54, `ptp1b` 10/6.68 = 1.50,
`ns5b` 12/8.21 = 1.46, `bcr_abl1_mandated` 13/7.67 = 1.69 — against `hiv_rt` 22/8.16 = 2.70 and
`cardiac_myosin_corrected` 22/9.14 = 2.41 [UNVERIFIED — arithmetic derived here from
`30-frozen-graph-profile.md` §2]. The globular arms cluster inside a 1.3–1.7 band and the two
elongated multi-domain arms sit at 2.4–2.7. **Any normalisation that assumes compactness is wrong by
about a factor of two on exactly the arms whose Laplacian condition number is worst** (`λ_max/λ₂`
spans 33 to 920, largest on the elongated chains [VERIFIED-FULLTEXT, ibid. §4]).

---

## Q3 — Source-geometry normalisation

This is where the headroom is. Source size spans 3 residues (`ns5b`) to 61, a 20× range; the median
candidate-to-source distance spans 7.6 Å to 23.9 Å (`hiv_rt`); the fraction of candidates within
10 Å of the source spans 0.12 (`ns5b`) to 0.69; the source's own mean relative solvent accessibility
spans 0.017 (`ptp1b`) to 0.268 [VERIFIED-FULLTEXT, `30-frozen-graph-profile.md` §3.3]. And the
endpoint is measurably sensitive to the source: the catalytic source has the largest between-arm AUC
spread of any source tested, 0.486, against 0.109 for a size-matched random source
[VERIFIED-FULLTEXT, `../exploration/results/45-source-choice.md` §3]. Both conditions of the §1.2
pre-screen are satisfied here and nowhere else in this file.

### Q3.1 Size- and degree-matched reference sets, converted to a z-score (tier ii)

The construction exists in network biology and is fully specified. Guney, Menche, Vidal and Barabási
define a closest-proximity measure between a drug's target set S and a disease's protein set T,

> `d_c(S,T) = (1/|T|) · Σ_{t∈T} min_{s∈S} d(s,t)`

and then normalise it against a matched reference ensemble,

> `z = (d(S,T) − μ_d(S,T)) / σ_d(S,T)`

where μ and σ come from "calculating the proximity between these two randomly selected groups, a
procedure repeated 1,000 times". Degree matching is by binning: "nodes within a certain degree
interval were grouped together such that there were at least 100 nodes in the bin. Accordingly, each
bin `B_{i,j}` was defined as `B_{i,j} = {u ∈ V | i ≤ k_u < j}` containing the nodes with degrees i to
minimum possible j such that `||B_{i,j}|| ≥ 100`". The stated reason is that drug targets are
systematically higher-degree than the network average — mean degree 28.6 against 21.2 — so an
unmatched reference would report proximity that is really hubness [VERIFIED-FULLTEXT,
doi:10.1038/ncomms10331, PMC4740350].

**Why this is the right shape for us and how it differs from what we already do.** Our
`45-source-choice.md` builds size-matched random sources and uses them as _alternative sources_, to
ask whether the catalytic site carries information. Guney's construction uses the matched ensemble
as a _reference distribution_ for the observed score. Applied per residue — `z_i = (s_i − μ_i)/σ_i`
with μ_i, σ_i estimated over M matched random sources on the same protein — it is **not** a monotone
transform of `s`, so it passes the §1.1 screen, and it subtracts exactly the part of a residue's
score that any source of that size and degree profile would have produced. It reads no label and
introduces no fitted parameter; M and the bin population are Monte-Carlo nuisance constants, and
their effect is measurable by varying them.

_Two honest caveats._ Our sources are 3 to 61 residues, far smaller than the ≥ 100-node bins Guney's
interactome supports, so degree matching on our graphs must use a different bin rule and the choice
must be reported. And the per-residue μ_i is a burial/centrality surrogate, so subtracting it will
also remove part of the distance confound — which `14-distance-confound.md` warns can over-match,
because real allosteric sites _are_ somewhat distal and distance is partly on the causal path. Report
matched and unmatched together.

**Counter-evidence that the same idea can be pushed too far, and a case where it helped.** Barel and
Herwig's NetCore replaces node degree with node coreness in the random-walk-with-restart, and reports
"improved re-ranking of genes after propagation" and "improved performance compared to the standard
degree-based network propagation using cross-validation" across 11 GWAS traits [VERIFIED-ABSTRACT,
doi:10.1093/nar/gkaa639, NAR 48:e98]. That is a _positive_ result for degree-bias correction, on a
scale-free interactome. Our contact graphs are not scale-free and their degree spread is small, so
the mechanism that makes NetCore work is much weaker here. Cite it as the reason to test, not as
evidence it will transfer.

### Q3.2 Subtracting the sets' own internal spread (tier i)

Menche et al. define the network-based separation of two node sets as

> `s_AB ≡ ⟨d_AB⟩ − (⟨d_AA⟩ + ⟨d_BB⟩)/2`

[VERIFIED-FULLTEXT, doi:10.1126/science.1257601, PMC4435741]. The subtraction makes a between-set
distance comparable across sets of different size and internal diameter, because each set's own
cohesion is removed before the comparison. For us the natural transfer is at the **site** level, not
the residue level: our deliverable is a top-5 hit list that is assembled into sites (stage S7), and
a predicted site and the active site are two node sets of different sizes. A 3-residue source and a
61-residue source have very different `⟨d_SS⟩`, and any raw source-to-patch distance inherits that
difference. This is one line of code on quantities we already compute [UNVERIFIED — transfer derived
here; no paper applying `s_AB` to a protein residue graph was retrieved].

### Q3.3 Radial-quantile stratification of the endpoint (tier ii)

The statistical machinery is covariate-adjusted ROC analysis. Janes and Pepe: "the authors
demonstrate the need for covariate adjustment in studies of classification accuracy, discuss methods
for adjusting for covariates, and distinguish covariate adjustment from several other related, but
fundamentally different, uses for covariates" [VERIFIED-ABSTRACT, doi:10.1093/aje/kwn099, Am J
Epidemiol 168:89–97]; the companion implementation paper describes "three different ways of using
covariate information", including asking "how much discriminatory accuracy improves with the
addition of the marker to the covariates (incremental value)" [VERIFIED-ABSTRACT, Stata J 9:17–39].

**The new content relative to `14-distance-confound.md` §Q4 is the stratum boundary, and it is the
whole point.** Prior work in this repository and in the teammate benchmark stratifies by distance in
**fixed 2 Å bins** (`00-conventions.md` §5). A fixed-Å bin is not the same object on two proteins
whose median candidate-to-source distance differs by 3×: on the closest arm most candidates fall in
the first few bins and on the farthest arm most fall beyond them. **Bins set by the deciles of _that
protein's own_ candidate-to-source distribution are, by construction, equally populated on every
protein**, so the within-stratum AUCs are comparable and their unweighted mean is a between-protein
comparable endpoint. Zero fitted parameters; the decile count is a resolution choice whose effect is
measurable [UNVERIFIED — derived here].

### Q3.4 A clock set by the source geometry rather than by the spectrum (tier ii)

The gap clock failed because it equalised a spectral quantity the endpoint does not depend on
(§1.2). The source-geometry analogue equalises a quantity the endpoint demonstrably does depend on:
set the propagation window so that the walk front reaches the protein's own median
candidate-to-source distance `d̃` a fixed number of times, rather than so that it completes a fixed
number of spectral periods. Both the number of hops to `d̃` and the front speed are read off the
graph. On our arms `d̃` spans 7.6 to 23.9 Å, a 3.1× range that a wall clock and the spectral-range
clock both ignore [VERIFIED-FULLTEXT, `30-frozen-graph-profile.md` §3.3]. **This is the one
remaining clock proposal that the §1.2 pre-screen does not immediately kill**, and the pre-screen
itself is the first thing to run on it.

### Q3.5 What the ENM literature offers here

Very little that is source-conditioned. `01-classical-baselines.md` already records that only four
classical methods condition on a named active site at all. No ENM paper was retrieved that
normalises a perturbation-response or a mode-projection for the _size or depth of the perturbed
site_, which is the quantity that varies 20× on our set. **Record this as a gap, not as an absence:**
"not retrieved by the recorded search" (ADR 0019).

---

## Q4 — Elastic-network parameter conventions: derived or empirical?

### Q4.1 The parameterisation papers and what they actually fit

| Model                              | Cutoff                                                                 | Spring constant                                                                           | Provenance                                                                                                                      | Tier                            |
| ---------------------------------- | ---------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- | ------------------------------- |
| GNM (Bahar, Atilgan & Erman 1997)  | "interactions between closely (≤ 7.0 Å) located alpha-carbon pairs"    | "A single-parameter harmonic potential is adopted"; one generic γ for all pairs           | validated against Cα temperature factors of 12 X-ray structures, 41–633 residues                                                | (iii)                           |
| ANM (Eyal, Yang & Bahar 2006)      | 15–24 Å, "quite robust to the cutoff distance in the range of 15–24 Å" | distance-weighting exponent p = 2.5                                                       | optimised for highest correlation with B-factors over 176 PDB structures at < 2.5 Å resolution, R < 0.3, no missing coordinates | (iii), fitted against B-factors |
| pfANM (Yang, Song & Jernigan 2009) | **none** — removed                                                     | inverse-square of the equilibrium distance; inverse 6th–7th power for larger deformations | motivated by the observation that "optimal cutoff values can differ somewhat from protein to protein"                           | (i) once the exponent is fixed  |
| oGNM (Yang et al. 2006)            | swept 7.3–15 Å                                                         | single γ                                                                                  | 1250 proteins                                                                                                                   | (iii)                           |

Citations: doi:10.1016/S1359-0278(97)00024-2 [VERIFIED-ABSTRACT, PMID 9218955];
doi:10.1093/bioinformatics/btl448, Bioinformatics 22(21):2619 [VERIFIED-ABSTRACT via the OUP article
page; DOI not independently re-derived]; doi:10.1073/pnas.0902159106, PNAS 106:12347–52
[VERIFIED-ABSTRACT, PMID 19617554]; doi:10.1093/nar/gkl084 [VERIFIED-ABSTRACT].

**The answer to the brief's question is that they are empirical, and the field says so.** The only
paper retrieved that argues _from_ the per-protein variation is pfANM, and its response is not to
tune per protein but to **delete the parameter**: replace the hard cutoff with an inverse-power
weight so that no threshold is needed at all. That is the cleanest zero-parameter move in the ENM
literature and it is directly implementable on our graph — it produces a dense weighted adjacency
rather than a sparse one, at a real cost in circuit depth under C3, and `13-graph-construction.md`
records that our own inverse-square weighting variant was already inside the family whose members
moved mean AUC by 0.031.

### Q4.2 Is there evidence that a per-protein choice beats a universal one?

**Not in the retrieved corpus, and the strongest evidence points the other way.** Three findings, in
increasing order of how much they hurt tier (iv):

1. Eyal et al.'s own robustness claim: the ANM "is quite robust to the cutoff distance in the range
   of 15–24 Å" [VERIFIED-ABSTRACT, OUP article page]. A 9 Å plateau leaves nothing for a per-protein
   rule to gain.
2. Fuglebakk, Reuter and Hinsen compared a representative selection of coarse-grained ENMs against
   MD-predicted covariance structure and report "large and consistent differences between proposed
   models"; crucially, "the models that agree best with B-factors model collective motions less
   reliably" and they "recommend against using B-factors as a benchmark" [VERIFIED-ABSTRACT,
   doi:10.1021/ct400399x, JCTC 9:5618–28, PMID 26592296].
3. Hinsen shows why: "thermal fluctuations are not the dominant contribution to crystallographic
   Debye-Waller factors" and "crystal packing modifies the atomic fluctuations considerably"
   [VERIFIED-ABSTRACT, doi:10.1093/bioinformatics/btm625, Bioinformatics 24:521–8, PMID 18089618].

**Together these close tier (iv) for us.** A cutoff fitted per protein against that protein's
B-factors is fitting the crystal environment, and the resulting model is measurably _worse_ at the
collective motions an allosteric signal would travel on. Note the C2 caveat on item 2: its reference
is an MD covariance, so the paper's own criterion is not one we may run — but its _negative_ result
about B-factors is a statement about B-factors and survives independently of the MD reference.

---

## Q5 — Cross-protein comparability in network biology and graph signal processing

### Q5.1 Which Laplacian

Three normalisations, and the choice is decided by what has to be comparable.

- **Combinatorial** `L = D − A`. Eigenvalues scale with degree; `λ_max` is bounded below by the
  maximum degree. Not comparable across graphs of different density without rescaling.
- **Symmetric normalised** `L_sym = I − D^{-1/2} A D^{-1/2}`. Its spectrum is bounded: "The
  Normalized Laplacian ... has a bounded spectrum, `0 ≤ λ_i ≤ 2`" [VERIFIED-FULLTEXT,
  arXiv:1805.10712]. This is the only one of the three whose spectrum is comparable across graphs
  _by construction rather than by rescaling_, and it is tier (i).
- **Random-walk** `L_rw = I − D^{-1}A`. Similar to `L_sym` via `D^{1/2}`, hence identical spectrum;
  the eigenvectors differ by a `D^{1/2}` factor [UNVERIFIED — derived here]. Choose between them on
  what the eigenvector means, not on the spectrum.

For us this is a genuine, cheap operator change that passes the §1.1 screen — `L_sym` reweights each
residue by `1/√k_i`, which is not a uniform transform. Our mean contact number varies only 8.9–10.3
between proteins, so the _between-protein_ gain is expected to be small; the _within-protein_ effect
of down-weighting high-degree buried residues is not small and is worth measuring on its own terms.

### Q5.2 Making a spectral quantity comparable across sizes

NetLSD is the cleanest statement of the problem and the fix. It is described as "the first, to our
knowledge, permutation- and size-invariant, scale-adaptive, and efficiently computable graph
representation method", and the requirement is that graph comparison be "invariant to the order of
nodes and the sizes of compared graphs, adaptive to the scale of graph patterns, and scalable"
[VERIFIED-FULLTEXT, arXiv:1805.10712]. The signature is the heat trace `h_t = tr(H_t) = Σ_j e^{−tλ_j}`,
and the reason raw traces are not comparable is explicit: the Taylor expansion shows "`h_t(G)`
contains information about the number of nodes", so signatures of differently sized graphs are not
on the same footing. The two normalisations are against neutral reference graphs of the same order —
the empty graph, `h_t(G)/h_t(K̄_n)` with `h_t(K̄_n) = 1/n`, and the complete graph,
`h_t(G)/h_t(K_n)` with `h_t(K_n) = 1 + (n−1)e^{−t}` [all VERIFIED-FULLTEXT, ibid.].

The information-theoretic route builds a density matrix directly from the Laplacian:
`ρ = e^{−βL}/Z`, `Z = Tr e^{−βL}`, with von Neumann entropy `S(ρ) = −Tr(ρ log₂ ρ) = −Σ λ_i log₂ λ_i`
and the equivalent form `S(G) = log₂ Z + β Tr[Lρ]` [VERIFIED-FULLTEXT, doi:10.1103/PhysRevX.6.041062,
arXiv:1609.01214]. Two details matter for us. First, `β` is not derived: the authors choose it so
that "the entropy normalized to its maximum value ... gets a specific real value c(β*) between 0 and
1" and recommend "the region close to the critical point — where entropy changes from 0 to positive
— provides the most performant range", exploring multiple values rather than fixing one
[VERIFIED-FULLTEXT, ibid.]. So the diffusion time is a swept parameter there too, and the
normalisation is of the _entropy_, `S/log₂N`, not of `β`. Second, this construction is a heat kernel
on the graph Laplacian written as a Gibbs state — the same object our `heat_kernel_from_source`
scorer computes — so adopting it is a reporting change, not a new observable.

De Lange, de Reus and van den Heuvel use the normalised-Laplacian spectrum precisely because "the
eigenvalue spectrum of the normalized Laplacian describes a network's structure directly at a
systems level, without referring to individual nodes or connections", and compare the macaque, cat
and _C. elegans_ networks — spanning macroscopic to microscopic scales — on that basis
[VERIFIED-ABSTRACT, doi:10.3389/fncom.2013.00189, Front Comput Neurosci 7:189]. That is the closest
published analogue to what we would be doing: comparing spectra of networks of very different size
and origin, using boundedness rather than rescaling to make it legitimate.

Tantardini, Ieva, Tajoli and Piccardi survey the wider space and split it by whether node
correspondence is known — DeltaCon and Cut Distance require it; alignment-based, graphlet-based and
spectral methods, Portrait Divergence and NetLSD do not [VERIFIED-ABSTRACT,
doi:10.1038/s41598-019-53708-y, Sci Rep 9:17557]. **For us node correspondence between two different
proteins does not exist**, so only the second class is available, and that is why the spectral route
is the one this literature offers us at all.

---

## Q6 — Negative evidence: where a normalisation has been shown not to help

This section is the one the brief most wants and it is the one with the most in-house evidence.

**N1. The spectral-gap clock. Ours, measured, decisive.** Setting the walk's time unit from the gap
next to the dominant eigenvalue instead of from the spectral range removes a real 117× disparity in
how many slow periods each arm covers, and reduces the between-arm AUC spread from 0.5627 to 0.5516
— 0.011, or 2 % of itself. The variance decomposition explains it: within-arm window sensitivity for
`ctqw_average_transfer` falls 0.079 → 0.045 while between-arm spread stays 0.668 → 0.650, so the
between/within ratio **worsens** from 8.5× to 14.5×. "The `gap` clock works exactly as designed and
that is why it fails" [all VERIFIED-FULLTEXT, `44-stability-and-noise.md` §6]. Of 32 combinations of
clock, window and observable, zero place all four development arms above 0.5 [ibid.].

**N2. B-factors as the fitting target for an ENM parameter.** Fuglebakk, Reuter and Hinsen:
"the models that agree best with B-factors model collective motions less reliably", with an explicit
recommendation "against using B-factors as a benchmark" [VERIFIED-ABSTRACT, doi:10.1021/ct400399x].
Hinsen supplies the mechanism: "thermal fluctuations are not the dominant contribution to
crystallographic Debye-Waller factors" and "crystal packing modifies the atomic fluctuations
considerably" [VERIFIED-ABSTRACT, doi:10.1093/bioinformatics/btm625]. **Any per-protein
normalisation validated against B-factors is validated against the crystal.**

**N3. The percolation-derived cutoff does not remove the size dependence.** `I_critical` "is a
function of the size of the protein and is generally higher for bigger proteins", rising from
≈ 3.25 % to > 4.25 % across the size range [VERIFIED-FULLTEXT, doi:10.1529/biophysj.105.064485]. A
rule adopted to make proteins comparable that itself varies systematically with N has not finished
the job.

**N4. A derived cutoff criterion can produce a universal constant, leaving nothing to normalise.**
The mutual-information minimum is "universally achieved at the cutoff length of 5 Å ... in all
considered, distinct proteins" [VERIFIED-ABSTRACT, doi:10.1002/prot.26154]. This is a success for
the criterion and a null result for cross-protein adaptivity.

**N5. A wide robustness plateau means per-protein tuning has no room.** The ANM is "quite robust to
the cutoff distance in the range of 15–24 Å" [VERIFIED-ABSTRACT, OUP article page]. Nine Ångström of
indifference.

**N6. Rigidity-derived thresholds are structure-sensitive.** "Rigidity analysis is best used as a
comparative tool to highlight the effects of structural variation" [VERIFIED-ABSTRACT,
arXiv:0810.1833]. A rule that reads a derivative off a swept curve inherits that sensitivity and
amplifies it.

**N7. Our own graph parameters are already near-equal, so no graph-side rule has headroom.** Mean
contact number 8.9–10.3, clustering 0.460–0.515, `λ₁` 10.40–11.80 across a 7.2× size range
[VERIFIED-FULLTEXT, `30-frozen-graph-profile.md` §3.3]. "A residue contact graph at a fixed cutoff is
a near-universal object" [ibid.]. This is the general form of N1: a normalisation of a quantity whose
between-protein spread is 1.1× cannot repair a between-protein endpoint spread of 0.49.

**N8. The counter-case, recorded so the section is not one-sided.** NetCore's coreness-based
correction of degree bias _did_ improve re-ranking after propagation, on 11 GWAS traits and
pan-cancer data [VERIFIED-ABSTRACT, doi:10.1093/nar/gkaa639]. The setting is a scale-free
interactome with heavy-tailed degree; ours is a near-regular geometric graph. The transfer argument
is weak in exactly the direction that matters, and this is the reason §7 ranks the degree-matched
z-score on its _source_-size component rather than on its degree component.

**One internal fact-check, recorded because a later reader will hit it.** The 21.7× figure for the
gap comes from `47-quantum-constructions.md` §1, whose table gives gaps 0.0748 to 1.6244 — ratio
21.72, which checks. `44-stability-and-noise.md` §6 quotes the same 21.7× while its own separate gap
column runs 0.01766 to 2.47385, ratio 140. The two tables report the gap of different operators.
Both documents also state the spectral range varies by 1.09× while `44`'s own table gives 17.968 to
21.631, ratio 1.20. Neither discrepancy changes any conclusion here — small either way — but quote
the figure with its source attached [VERIFIED-FULLTEXT for both tables; the reconciliation is
UNVERIFIED and is not attempted here].

---

## 7. Ranked candidate list

Ranked by the §1.2 pre-screen: a candidate scores well when the quantity it equalises varies a lot
between proteins **and** the endpoint is sensitive to that quantity within one protein. Every entry
is tier (i) or (ii). Tier (iii) constants and tier (iv) per-protein fits are excluded by
construction.

**The falsifier is the same for all of them, and it is the gap clock's own test.** Apply the rule
per arm → score through `allo.scoring.score_arm` on the four `development` arms → report (a) the
between-arm AUC spread, (b) the within-arm/between-arm variance decomposition, against the
unnormalised control. **The bar is the gap clock: a 2 % spread reduction with a worsened variance
ratio is failure.** A candidate passes only if it reduces the between-arm spread by materially more
than 0.011 without inflating the ratio.

| #   | Rule                                                                                                                      | What it equalises                                                               | Zero-parameter source of the setting                | Between-protein spread of that quantity              | Passes §1.1?                                                                         |
| --- | ------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- | --------------------------------------------------- | ---------------------------------------------------- | ------------------------------------------------------------------------------------ |
| 1   | Per-residue z-score against a size- and degree-matched random-source ensemble on the same protein (Guney construction)    | the score a residue would get from _any_ source of this size and degree profile | the protein's own graph plus the frozen source size | source size 20×                                      | Yes — per-residue, not monotone                                                      |
| 2   | Radial-**quantile** stratified AUC: deciles of the protein's own candidate-to-source distance                             | the candidate-to-source distance _distribution_                                 | the protein's own distance quantiles                | median distance 3.1×; fraction within 10 Å 0.12–0.69 | Yes — changes the strata                                                             |
| 3   | Geometry-derived clock: window set by hops to the protein's own median candidate-to-source distance                       | how far the walk has actually travelled relative to the distance it must cross  | `d̃` and the front speed, both read off the graph    | 3.1×                                                 | Yes — changes the hyperparameter                                                     |
| 4   | Intensive effective resistance: divide resistance-to-source by the protein's mean pairwise resistance `2Σ_k(1/λ_k)/(N−1)` | the graph's overall resistive scale                                             | Laplacian spectrum of this graph                    | unmeasured — measure first                           | **No for AUC alone**; yes for pooled or thresholded use                              |
| 5   | Source-spread subtraction at site level: `⟨d_SP⟩ − (⟨d_SS⟩+⟨d_PP⟩)/2` (Menche `s_AB`)                                     | the source's own internal diameter                                              | the two node sets                                   | source size 20×                                      | Yes — acts on the S7 site score                                                      |
| 6   | Operator swap to `L_sym`, spectrum bounded in `[0,2]`                                                                     | degree-driven spectral scale                                                    | theory; no constant at all                          | `⟨k⟩` only 8.9–10.3 → little                         | Yes — `1/√k_i` reweighting is not uniform                                            |
| 7   | Isostatic cutoff: per-protein `r*` with `⟨k⟩(r*) = 2d = 6`                                                                | constraint density relative to rigidity                                         | Maxwell counting on this structure                  | current `⟨k⟩/6` = 1.48–1.72, near-uniform            | Yes — changes the graph. **Only meaningful for the vector ENM, not the scalar walk** |
| 8   | Connectivity-threshold cutoff: smallest `r` with one component                                                            | the graph's own percolation point                                               | this structure                                      | unmeasured; all fourteen already connected at 4.5 Å  | Yes                                                                                  |
| 9   | RDF first-minimum cutoff, per protein                                                                                     | the first coordination shell                                                    | this structure's distance histogram                 | unmeasured                                           | Yes                                                                                  |
| 10  | pfANM: delete the cutoff, inverse-square weights                                                                          | the existence of the parameter                                                  | theory, once the exponent is fixed                  | —                                                    | Yes, but inside the family our sweep already moved 0.031                             |
| 11  | Reporting normalisations: `ĝ = 2g/((N−1)(N−2))`, `PR/N`, `H/log N`, `h_t/n`                                               | the observable's N-scaling                                                      | closed forms in §Q2                                 | 7.2× in N                                            | **No** — no-ops for AUC. Adopt for the report and for any pooled figure              |
| —   | **Spectral-gap clock**                                                                                                    | the number of slow periods covered                                              | graph spectrum                                      | 21.7×                                                | **Falsified. Do not re-propose** (`44` §6)                                           |

**Per-candidate falsifier, beyond the shared one.**

1. _Source z-score._ Falsified if the between-arm AUC spread does not fall by > 0.05, or if the mean
   |ρ| to negated distance rises above the unnormalised control's — which would mean the ensemble
   mean it subtracts was carrying the signal, not the artefact. Run the M-sweep (M ∈ {25, 100, 400})
   to show the result is not a Monte-Carlo artefact.
2. _Quantile stratification._ Falsified if the decile-stratified mean AUC has a between-arm spread no
   smaller than the fixed-2 Å-stratified version. This is a pure re-scoring of existing runs and
   costs no new propagation.
3. _Geometry clock._ Run §1.2 first: measure `R_within` for the geometry clock on one arm. If
   `R_within < 0.05` AUC, stop — the bound says it cannot recover the 0.49 spread and the full sweep
   is wasted.
4. _Intensive resistance._ Falsified for the primary endpoint by §1.1 before it is run; test it only
   where scores are pooled or thresholded. `effective_resistance_to_source` already scores best
   0.721 in the battery, so the pooled question is worth asking.
5. _`s_AB` at site level._ Falsified if the between-arm spread of the S7 site-level metric does not
   fall, or if hits@5 drops.
6. _`L_sym`._ Falsified if AUC and between-arm spread are both unchanged within noise. Cheap: one
   flag in `network.build`'s operator.
7. _Isostatic cutoff._ Falsified if `r*` solving `⟨k⟩(r*) = 6` varies by less than ~0.3 Å across the
   arms — that would mean the rule is a global constant in disguise (N4's failure mode) — or if the
   resulting graphs score worse than the frozen 4.5 Å graph on `anm_perturbation_response`.
   8–9. _Connectivity and RDF cutoffs._ Falsified the same way as 7: measure the spread of `r*` across
   arms **before** scoring anything. If the derived cutoffs are all within 0.3 Å of each other, the
   rule is a constant and there is nothing to normalise.
8. _pfANM._ Falsified if mean AUC stays inside the 0.031 band the eight-graph sweep already covered,
   which would place it inside the family `13-graph-construction.md` has closed. Report the C3 cost:
   a dense weighted adjacency multiplies the Trotter depth by `N/⟨k⟩`.

**What the list deliberately does not contain.** Any rule that fits a constant on four arms; any
rule normalised against B-factors (N2); any rule requiring MD to evaluate the criterion (C2); and
any further spectral clock (N1).

---

## What this changes for our pipeline

- **S1, the graph.** Three derived cutoff rules are now specified well enough to run — isostatic
  `⟨k⟩ = 6`, connectivity threshold, RDF first minimum — and all three should be _measured for their
  spread across arms before any of them is scored_. If the derived `r*` is near-constant across the
  benchmark, the rule is a global constant and the experiment stops there. This is the cheapest test
  in the file and it directly answers whether a cutoff rule can help at all. It is also consistent
  with `30-frozen-graph-profile.md` §5's existing conclusion that raw topology is near-constant and a
  graph variant can only help through weights.
- **S3, the operator.** `L_sym` is a one-flag change with a tier (i) justification — bounded spectrum
  — and it is not a monotone rescaling, so it can move the endpoint. Add it as an operator option
  beside the adjacency and the combinatorial Laplacian.
- **S5, the propagation observable.** Do not propose another spectral clock. The remaining clock
  worth testing is the geometry clock of §Q3.4, and §1.2's pre-screen decides whether even that is
  worth a full sweep.
- **S6, confound removal.** The per-residue matched-source z-score of §Q3.1 belongs here, not in S5:
  it is a confound-removal step that happens to be derived from the source rather than from distance.
  It must be applied at the same point in the chain as the existing detrend — after pocket smoothing,
  never before (`14-distance-confound.md` §Q4(f)) — and both the matched and unmatched numbers must
  be reported, because over-matching discards genuine signal.
- **S7, site assembly.** `s_AB` gives a size-corrected site-to-source distance for the assembled
  top-5 sites, which is the level at which our 20× source-size range does the most damage.
- **S9, the evaluation report.** Radial-quantile strata replace fixed-Å strata for any _between_-arm
  comparison. Fixed-Å strata remain correct for a within-arm statement. The two must not be mixed in
  one table.
- **S10, reporting.** The §Q2 normalisations are no-ops for AUC and are mandatory for any figure that
  puts two proteins on the same axis: `ĝ`, `PR/N`, `H/log N`, `h_t/n`. Also report `⟨k⟩/6`, the
  constraint ratio, per target: it is one number that says how far each graph sits from isostaticity
  and it costs nothing.
- **Method-selection policy.** §1.1 and §1.2 should be applied to every future normalisation proposal
  before it is implemented. Between them they would have rejected the gap clock on paper.

---

## Method

**Retrieved 2026-08-27.** Routes used, in order of yield: PubMed E-utilities `esearch.fcgi` and
`efetch.fcgi` (bibliographic records and abstracts); PMC article pages
(`pmc.ncbi.nlm.nih.gov/articles/{PMCID}/`) for full text; the arXiv API
(`export.arxiv.org/api/query`, both `search_query` and `id_list`); ar5iv HTML
(`ar5iv.labs.arxiv.org/html/{id}`) for arXiv full text, which succeeded where the raw PDF route
failed; Crossref REST (`api.crossref.org/works`) for bibliographic confirmation; and two publisher
pages. Europe PMC was not attempted, per `14-distance-confound.md`'s recorded outage on this route.

**Queries run.** Web search (2, then the session budget was exhausted): `Gaussian network model
Bahar Atilgan Erman 1997 cutoff 7.0 Angstrom single force constant B-factors`; `parameter-free
anisotropic network model Yang Song Jernigan inverse power distance spring constant cutoff`.
PubMed `esearch`: `Brinda Vishveshwara network representation protein structures stability`;
`Fuglebakk elastic network model collective motions evaluation`; `"degree bias" AND "network
propagation"`; `"Gaussian network model" AND cutoff`; `network propagation universal amplifier
genetic associations Cowen`; `Guney network-based in silico drug efficacy screening proximity`;
`Menche uncovering disease-disease relationships incomplete interactome`; `Hinsen structural
flexibility proteins impact crystal environment`; `Janes Pepe covariate adjustment ROC curves
diagnostic marker`; `Rader Hespenheide Kuhn Thorpe protein unfolding rigidity lost`; `entropy
distance cutoff protein contact network`; `Tantardini comparing methods for comparing networks`;
`Bruschweiler collective protein dynamics nuclear spin relaxation degree of collectivity`; and two
queries that returned zero because PubMed ANDs every term (`degree bias network propagation random
walk restart correction`; `Gaussian network model optimal cutoff distance protein size B-factor
correlation`) — recorded because the zero is a property of the query, not of the literature.
arXiv API: `all:"rigidity percolation" AND all:protein`; `ti:"Betweenness centrality in large complex
networks"`; `all:"NetLSD" OR ti:"hearing the shape of a graph"`; `abs:"mean coordination" AND
abs:"rigidity" AND abs:"isostatic"`; `ti:"Spectral entropies as information-theoretic tools for
complex network comparison"`; `ti:"Wavelets on Graphs via Spectral Graph Theory"`; `abs:"protein
contact network" AND abs:"percolation"` (0 results); `id_list=0810.1833`. Crossref: one bibliographic
query for Brüschweiler 1995.

**Counts.** Approximately 26 distinct retrievals. Records screened in and cited: 22. Full text
landed for 5 (Brinda & Vishveshwara via PMC; Guney et al. via PMC; Menche et al. via PMC; NetLSD via
ar5iv; De Domenico & Biamonte via ar5iv) plus 4 internal repository documents. The remainder are
abstract- or metadata-level.

**What could not be reached.** The PNAS full text of Yang, Song & Jernigan 2009 returned HTTP 403;
its abstract was taken from PubMed instead. The arXiv PDF route returned undecodable binary for
`1805.10712`; ar5iv succeeded. The Jacobs, Rader, Kuhn & Thorpe 2001 record came from a web search
result plus the Wiley DOI URL and the ASU repository listing, not from a direct record fetch — its
tag is `[VERIFIED-ABSTRACT]` with that provenance stated inline. The Eyal, Yang & Bahar 2006 DOI was
not independently re-derived; the volume, issue, page, parameter values and the 176-structure
optimisation set all come from the OUP article page fetched this session. The Brüschweiler
collectivity **formula** was not retrieved; only its bibliographic record was confirmed, via
Crossref, and the claim is tagged accordingly. Hammond, Vandergheynst & Gribonval's journal
reference and DOI were not returned by the arXiv API, so only the arXiv ID is cited, and the
specific claim that wavelet scales are set from `λ_max` is marked `[UNVERIFIED]` because it was not
retrieved from the full text this session.

**Stopping rule.** Stopped when each of the six questions had at least one tier (i) or (ii) rule with
a retrieved source and at least one retrieved negative, and when three consecutive retrievals
returned only material already covered by `13-graph-construction.md` or `14-distance-confound.md`.

**Leakage.** No file under `docs/benchmark/evaluation/`, neither manifest, neither `frozen.json`,
`selection.json`, nor `extension-candidates.md` was opened. No result for any `generalisation`-tier
arm is reported: per-arm numbers here name only `development` arms (`mkp5`, `ptp1b`, `hiv_rt`,
`ns5b`) and primary arms. Aggregate ranges over the fourteen frozen apo graphs are quoted from
`../exploration/data/30-frozen-graph-profile.md`, which is label-free and apo-only.
