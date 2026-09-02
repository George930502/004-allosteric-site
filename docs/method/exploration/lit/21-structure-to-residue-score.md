# Structure in, per-residue score out

**Scope:** The machinery six adjacent structural-biology tasks use to turn one static structure
into a ranked residue list — catalytic-residue prediction, cryptic-pocket propensity, ligand-site
and druggability ranking, epitope prediction, protein-language-model and inverse-folding zero-shot
scoring, and rigidity theory. Mined for the **score construction** (what function of the input
produces the number), not for the biology. Deliberately excludes every allosteric-site predictor —
those are files 01 and 02 — and excludes the graph-theoretic observables already screened in
file 05 (effective resistance, target control, influence maximisation, spectral wavelets).
**Sibling files:** `00-conventions.md` (evidence rules, C1–C6, the eleven closed quantum insertion
points, the leakage guard); `02-ai-methods.md` (supervised allosteric-site predictors, the
supervision ceiling, the AUROC/AUPR trap); `05-adjacent-task-transfer.md` (frameworks built for
other problems, screened for whether the mathematics ports).
**Retrieved:** 2026-08-26.

---

## 0. How to read this file, and the one result that reframes the rest

Every method below answers a question of the form "given one structure, which residues matter?"
Our question is different in exactly one way: **we are told where the active site is, and we are
asked which residues are coupled to it.** Sections 1, 3 and 4 review tasks that rank residues by
being _at_ a functional site. Sections 2, 5 and 6 review tasks that rank residues by a property
(openability, evolutionary constraint, rigidity) that is not anchored to any named source.

That asymmetry has a consequence which is the most decision-relevant thing in this file, so it is
stated first rather than at the end.

**Global centrality on a residue-interaction network is an orthosteric-site finder.** Amitai et al.
transformed 178 representative structures into residue interaction graphs and reported that
combining closeness centrality with surface accessibility "identified active site residues in 70%"
of them [VERIFIED-ABSTRACT, doi:10.1016/j.jmb.2004.10.055]. Chea & Livesay re-tested the same
readout on 283 SCOP-superfamily-unique proteins from the Catalytic Site Atlas (844 catalytic
against 96,280 non-catalytic residues) and found, over the top five closeness scores, a
true-to-false-positive ratio of **6.8:1**, rising to **15.3:1** with a ≥9.0 Å² solvent-accessibility
filter and **26.3:1** with an added residue-identity filter, against a 0.9% random baseline
accuracy [VERIFIED-FULLTEXT, doi:10.1186/1471-2105-8-153].

Now chain that against what `00-conventions.md` §5 already records. A CTQW centrality on residue
interaction networks shows "consistently strong agreement with classical eigenvector centrality"
(Mohtashim, Sajjan & Kais, _JACS_ 2026). The same first author's follow-up, RinQ, formulates
centrality detection on residue interaction networks as a QUBO and solves it with D-Wave simulated
annealing, reporting that it "consistently identifies central residues that closely align with
classical benchmarks" [VERIFIED-ABSTRACT, arXiv:2508.01501]. So: quantum walk centrality ≈ classical
eigenvector centrality ≈ closeness centrality ≈ **the active site**, which the challenge hands us
for free.

**This is a mechanistic explanation for the eleven closed insertion points, not a new one.**
Conventions §5 diagnoses their failure as "a single-particle Hermitian walk carries no information
beyond its transfer amplitudes." The adjacent-task literature adds the complementary half: whatever
information those amplitudes _do_ carry is centrality, and centrality is a validated detector of
the residue set we are not being scored on. The implication is not "try harder" — it is that a
centrality-flavoured score should enter our pipeline as a **subtraction**, not as a predictor
(§7, item 5).

**On C6.** C6 is the modelling assumption for the _propagation_ stage: contact topology drives the
signal. It does not forbid an auxiliary per-residue feature computed some other way. Below, a C6
verdict of PASS means the score is a function of contact topology; FAIL means it is not and could
not become the propagation core; CONDITIONAL means it is legal as an auxiliary feature but must not
displace the topology-driven core.

---

## 1. Catalytic-residue prediction from structure alone

This is the mirror image of our task. Six generations of method, and the trend across them is the
single most useful thing here: **the field moved from global centrality to local network
properties, and the local score won by a factor of three on precision.**

### 1.1 Global centrality — Amitai 2004, Chea & Livesay 2007

Network: Cα nodes, edges at an **8.5 Å** cutoff, unweighted. Score:

```
CC_i = N_p / Σ_j L_ij        # L_ij = shortest-path hop count, N_p = number of vertices
```

[VERIFIED-FULLTEXT, doi:10.1186/1471-2105-8-153]. Numbers in §0. Statistical significance was
established against a binomial null, p from 2.7 × 10⁻⁹ to below 8.8 × 10⁻¹³⁴ [VERIFIED-FULLTEXT,
same].

Amitai et al. additionally note, from detailed structural analysis rather than benchmark statistics,
that high-closeness residues in their set include "the regions whose structural changes activate
MAP kinase and glycogen phosphorylase" [VERIFIED-ABSTRACT, doi:10.1016/j.jmb.2004.10.055]. That is
an allostery-adjacent observation from a pure centrality readout, but it is anecdotal in the source
— no hit rate, no null. Do not quote it as evidence that closeness finds allosteric sites.

**Verdict.** C1 PASS (single apo structure, no ligand). C2 PASS (no MD, no fitted weights).
C6 PASS (pure contact topology).

### 1.2 Local network properties — Slama, Filippis & Lappe 2008

Contacts defined at **4.2 Å** between non-covalently-connected heavy atoms; a second graph uses
side-chain-only atoms. The published ranking function is:

```
S_i = Dg3_i^3 · exp( 0.25 · (Dg1SC_i − ⟨Dg1SC⟩_type) ) · [ 1 + 50 · (D_type − med(D_type)) ]
```

where `Dg3_i` is the number of residues at exactly **three** graph steps from i, `Dg1SC_i` is the
side-chain contact count normalised by the residue-type average, and `D_type` is the percentage of
that residue type among known catalytic residues [VERIFIED-FULLTEXT, doi:10.1186/1471-2105-9-517].

On 226 CSA proteins (62,083 residues, 777 catalytic) it reaches **precision 28.1% at coverage
9.91%**, against **precision 8.22% at coverage 31.66%** for the closeness-centrality-plus-surface-
accessibility baseline of §1.1 — "a more than three-fold increase" in precision [VERIFIED-FULLTEXT,
same]. On an 8-protein validation set precision is 45.5% for strictly catalytic residues and
**72.7%** when substrate-binding residues are also counted positive [VERIFIED-FULLTEXT, same].

The transferable content is the shape of the score, not the constants: a **cubed third-shell
count** times an exponential in local side-chain contact density. Both terms are local. Neither is
a global centrality. This is the only head-to-head comparison retrieved this session in which a
local topological score beats a global one on the same dataset and the same positive class.

**Verdict.** C1 PASS. C2 PASS — the `D_type` prior is a frequency table over CSA catalytic
residues, not MD, but it _is_ fitted to an external label set (546 proteins, 1,478 catalytic
residues), so a strict reading makes the third factor CONDITIONAL and the first two factors
unconditionally clean. C6 PASS.

### 1.3 Electrostatics — THEMATICS and POOL

THEMATICS solves Poisson–Boltzmann, runs Monte Carlo protonation sampling, and flags ionisable
residues whose theoretical microscopic titration curves deviate from Henderson–Hasselbalch shape.
On 169 CatRes enzymes: recall **41.1 / 50.4 / 54.2%** at Z-score cutoffs 1.00 / 0.99 / 0.98, with
precision **19.4 / 17.9 / 16.4%**, and false-positive rates 1.95 / 2.60 / 3.12% on a 75-protein set
[VERIFIED-ABSTRACT, doi:10.1186/1471-2105-8-119].

POOL turns that into a ranked list. Its per-residue feature vector is small and explicit: the
**third and fourth central moments** of the titration curve (μ₃, μ₄), the same two moments averaged
over a **9 Å** environment (μ₃ᵉⁿᵛ, μ₄ᵉⁿᵛ), the CASTp cleft-size rank, and a ConSurf conservation
score. Non-ionisable residues get only the two environment features. Ties break on Manhattan
distance from the origin in THEMATICS space. On a 160-protein set with 10-fold cross-validation,
POOL(T)×POOL(G)×POOL(C) reaches **recall 88.6%** at a 10% filtration-ratio cutoff, mean average
specificity **0.925**; the structure-only variant POOL(T)×POOL(G) reaches **85.2% recall at 91.0%
accuracy** [VERIFIED-FULLTEXT, doi:10.1371/journal.pcbi.1000266]. Server: Somarowthu & Ondrechen
2012 [VERIFIED-ABSTRACT, doi:10.1093/bioinformatics/bts321].

Two constructions transfer. First, **environment-averaged moments**: take any per-residue scalar,
compute its 3rd and 4th central moments over a fixed-radius shell, and use those as features. This
is a cheap way to convert a noisy point estimate into a spatially smoothed one that still
distinguishes tail behaviour from mean behaviour. Second, **multiplying independent rankers**
(POOL(T) × POOL(G) × POOL(C)) rather than summing them — a product is a conjunction, and it is why
POOL's precision holds up while recall climbs.

**Verdict.** C1 PASS. C2 PASS (no MD; ConSurf is an MSA product). C6 CONDITIONAL — electrostatics
is not contact topology, so this is an auxiliary feature, not a propagation core.

### 1.4 Geometry plus conservation — ConCavity

ConCavity integrates evolutionary sequence conservation with structure-based cavity detection and
reports state-of-the-art performance on both 3D pocket and individual ligand-binding-residue
prediction, including catalytic sites [VERIFIED-ABSTRACT, doi:10.1371/journal.pcbi.1000585]. The
paper's own framing is the useful part: it performs "one of the first direct comparisons of
conservation-based and structure-based methods" and finds "the two approaches provide largely
complementary information." Exact per-residue numbers were not retrieved from the abstract.

**Verdict.** C1 PASS. C2 PASS. C6 CONDITIONAL.

### 1.5 2022–2026 deep methods

| method                                   | input                | per-residue score construction                                                                                                                                                                                                                                        | numbers                                                                                                                                               | dataset / criterion                                                                                                                                                                                                                     |
| ---------------------------------------- | -------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **AEGAN** (Shen et al. 2023)             | sequence + structure | adaptive edge-gated graph attention network, binary head                                                                                                                                                                                                              | sensitivity **0.9659**, accuracy **0.9226**, AUPRC **0.9241**; F1 ~4× the best prior model                                                            | independent test set; positive class and prevalence **not retrieved** — treat the AUPRC as uncomparable until the prevalence is known (`02` §12) [VERIFIED-ABSTRACT, doi:10.1021/acs.jcim.3c00273]                                      |
| **SCREEN** (Pan et al. 2025)             | structure + sequence | 3-layer GCN on a residue graph, then MLP → 2-vector propensity; features = PSSM (n×20) + HMM (n×30) + ProtT5 (1024-d) + B-factor, SASA, atom type, atomic mass, H-bond capacity, vdW radius                                                                           | precision **61.0–69.3%**, recall **61.2–82.0%**, F1 **61.5–74.1**                                                                                     | five test sets, 1,055-enzyme training corpus (M-CSA + EF) clustered at 40% identity; **no MD anywhere** [VERIFIED-FULLTEXT, doi:10.1093/gpbjnl/qzae094]                                                                                 |
| **Squidly** (Rieger et al. 2025)         | **sequence only**    | ESM2 (3B/15B) per-token embeddings → contrastive MLP → 128-d → BiLSTM → 5-model ensemble mean, threshold 0.6                                                                                                                                                          | precision **0.81–0.86**, recall **0.52–0.61**, F1 **0.66–0.69** on the low-identity set; F1 > 0.85 on six standard benchmarks; BLAST baseline F1 0.37 | CataloDB, 232 sequences at **<30% sequence and structural identity** to training [VERIFIED-FULLTEXT, doi:10.1101/2025.06.13.659624]                                                                                                     |
| **PARSE** (Derry, Tartici & Altman 2025) | structure            | COLLAPSE local-environment embeddings; rank all reference-database residues by max cosine similarity to any query residue; running **Kolmogorov–Smirnov** statistic down that ranked list = enrichment score per function; map contributors back by nearest neighbour | **58.7%** of predictions at precision > 0.9 _and_ recall > 0.5; beats DeepFRI on 584/599 test proteins                                                | rare enzymes (<100 SwissProt examples); reference DB = CSA, 26,157 residues / 939 functions; active site defined as catalytic residues plus neighbours within 3.5 Å; pLDDT ≥ 70 filter [VERIFIED-FULLTEXT, doi:10.1073/pnas.2513219122] |

Squidly's benchmark is the one worth copying. It reports separately on a set filtered to **<30%
sequence _and structural_ identity** to training, and the F1 drops from >0.85 to 0.66–0.69 when it
does. That is the same leakage-controlled reappraisal that AlloBench applied to allosteric
predictors (`00-conventions.md` §6), performed by the authors themselves, and it is the reporting
standard our own method files should meet.

PARSE is the most transferable construction in the table because it is **effectively zero-shot**:
one reference example per function suffices, and the score is a rank-enrichment statistic rather
than a fitted classifier. The §2 supervision ceiling in `02-ai-methods.md` does not bind it.

**Verdicts.** All four: C1 PASS (single structure or sequence at inference), C2 PASS (no MD in
training or inference for any of them). C6: FAIL for Squidly (sequence only) and PARSE (embedding
similarity, not topology); CONDITIONAL for AEGAN and SCREEN (graph over residues, but the graph is
a carrier for learned features rather than the propagating medium). All four inherit the `02` §3
"Legal\*" caveat: none may be used as a pretrained artifact on our benchmark targets until its
training split is checked.

### 1.6 What section 1 changes

Three things. (i) Closeness/eigenvector centrality is an orthosteric detector — use it as an
anti-feature (§7, item 5). (ii) A **local third-shell** score beat a global centrality 3.4× on
precision on the mirror task; nothing in `00-conventions.md` §5's eleven closed points is a local
shell statistic. (iii) POOL's environment-averaged central moments and multiplicative combination
are free upgrades to any per-residue score we produce.

---

## 2. Cryptic-pocket and conformational-change propensity from one apo structure, without MD

The brief asks for what survives when PocketMiner is removed. Four routes survive, one of them
cleanly.

### 2.1 CryptoSite's feature set, and exactly what is left after deleting the MD

CryptoSite trains an **SVM with a quadratic kernel** on 84 known cryptic sites, 92 binding pockets
and 705 concave surface patches, and reports overall **AUC 0.83** with **TPR 79% / FPR 29%** at a
residue-score threshold of 0.05 on a held-out 14-protein apo test set [VERIFIED-FULLTEXT,
doi:10.1016/j.jmb.2016.01.029]. The feature set partitions as **30 structure-only** features
(fpocket and ConCavity pocket scores, surface convexity, hydrophobicity, B-factors, geometry
descriptors) plus **28 AllosMod MD-derived** features, 58 total [VERIFIED-FULLTEXT, same].

The ablation is the number that matters. Greedy-forward selection picks three features, and the
single most informative one is "average pocket score from the molecular dynamics simulations"
at **AUC 0.73 alone**; the crystal-structure features combined reach **AUC 0.74**
[VERIFIED-FULLTEXT, same]. So one MD feature carries as much signal as thirty static ones — which
also means **the price of C2 compliance on this task is roughly 0.83 → 0.74 AUC**, not a collapse.
_Caveat, flagged rather than resolved:_ the retrieved text also reports a three-feature final model
at AUC 0.77, which does not sit cleanly beside the headline 0.83; the difference is presumably
training-set versus test-set evaluation, but the retrieval this session did not settle it. Quote
0.83 and 0.74 with that caveat attached.

**Verdict.** C1 FAIL and C2 FAIL — new MD is required at inference, not just at training. Already
established in `02` §8 and `05` §2; repeated here only because the 30/28 partition is the
quantitative basis for §2.2.

### 2.2 The C2-legal twin — normal-mode-guided conformational sampling (Zheng 2021)

This is the survivor `02` and `05` did not retrieve, and it matters because it was benchmarked
against CryptoSite on CryptoSite's own data.

Procedure: solve the lowest **30** normal modes of a coarse-grained elastic network, sample along
each mode, refine the backbone atomistically, repack side chains, then run **fpocket or ConCavity**
on the restructured conformers and take the enhanced pocket score. On the **same** 84-site training
set and 14-protein test set, it reaches "area under the receiver operating characteristic curve

> 0.8 … comparable to the CryptoSite server," at **1–2 hours** per average-size protein
> [VERIFIED-ABSTRACT, doi:10.1002/prot.26027].

Two secondary findings from the same abstract are load-bearing. First, "simply sampling along each
of the lowest 30 modes is near optimal" — no tuning of which modes. Second, the authors "trained
machine-learning protocols to optimize the combination of the sampling-enhanced pocket scores with
other dynamic and conservation scores, which only slightly improved the performance." That is a
third independent instance of the `02` §11 pattern: the unlearned geometric readout is already
where the signal is.

**Verdict.** C1 PASS (single apo structure). C2 PASS (elastic network, no trajectory, no
MD-trained weights). C6 PASS (the modes come from the contact-derived Hessian). This is the only
method in section 2 that is unconditionally clean on all three.

### 2.3 ESSA — a per-residue score straight out of the ENM spectrum

Already named as a bar in `00-conventions.md` §6; retrieved here for its score construction, which
that file does not give. Build a Cα GNM (cutoff 10 Å) or ANM (15 Å). For each residue i, add its
heavy atoms as extra network nodes to mimic the crowding a bound ligand would cause, and measure
the fractional shift in the softest mode frequencies:

```
Δλ_k(i)%  =  (λ_k(i) − λ_k) / λ_k × 100                    (Eq. 2.2.1)
essa_i     =  ⟨Δλ_1–10(i)⟩                                   # mean over the softest ten modes
z_i        =  (essa_i − μ) / σ                               (Eq. 2.2.2)
```

[VERIFIED-FULLTEXT, doi:10.1016/j.csbj.2020.06.020]. Datasets: 25 monomers carrying 28 allosteric
and 26 orthosteric sites (Dataset I); 24 structures of 12 proteins in both apo and holo form
(Dataset II). On Dataset II, integrating the ESSA profile with fpocket pockets and local
hydrophobic density places the allosteric site in the **top 3 pockets** for **10 of 14** sites from
holo structures and **7 of 14** from apo [VERIFIED-FULLTEXT, same].

That 10/14 → 7/14 apo penalty on the _same twelve proteins_ is the cleanest matched apo-versus-holo
degradation retrieved in this session, and it is on the exact axis the challenge scores.

**Verdict.** C1 PASS, C2 PASS, C6 PASS.

### 2.4 Hinges without MD — PACKMAN

Compute alpha shapes (a subset of the Delaunay tessellation) of the structure, convert to a graph,
and take the **network eccentricity of each backbone atom** as the per-atom score; hinge calls are
validated by a permutation test on B-factors. On **167 open/closed protein pairs**, PACKMAN
"is able to predict hinge regions equally well from either the open or the closed forms"
[VERIFIED-ABSTRACT, doi:10.1016/j.jmb.2019.11.018].

Two transferable pieces. (i) **Eccentricity** — max shortest-path distance from a node — is a
global topological statistic that is _not_ closeness and _not_ eigenvector centrality, and it was
not among the observables screened in `00-conventions.md` §5. (ii) The **permutation test against
B-factors** is a ready-made, C1-clean null for any per-residue score: permute the score labels,
recompute its association with the observed B-factor profile, and report the empirical p.

**Verdict.** C1 PASS, C2 PASS, C6 PASS (alpha shapes are a geometric-topological construction on
coordinates alone).

### 2.5 The sequence route — CryptoBank

Cryptic-site labels are derived by applying a machine-learning model to ligand-induced
conformational change across **more than 6 million apo/holo structural alignments** in the PDB, and
a protein language model is then fine-tuned to predict cryptic sites from sequence
[VERIFIED-ABSTRACT, doi:10.1126/sciadv.ady6364]. The preprint reports **PR AUC 0.8** when the query
shares >20% identity with a CryptoBank entry [VERIFIED-ABSTRACT, bioRxiv 2025.04.23.650184]; the
published record retrieved this session did not restate that figure, so treat it as preprint-level.

**Verdict.** C2 **PASS** — the labels come from crystallographic apo/holo pairs, not from
trajectories; MD appears only in the paper's downstream validation of four predictions, which is
not in the prediction path. C1 **CONDITIONAL and serious**: the label generator is defined by
holo structures, and with >6 M alignments the training corpus is close to exhaustive over the PDB.
Using the released weights on any of our targets almost certainly puts that target's own holo
conformational change into the prediction path through the weights. This is a stronger version of
the `02` §3 "Legal\*" risk, and it cannot be discharged without the training-chain list. C6 FAIL
(sequence only).

### 2.6 The 2026 reappraisal — all of these are qualitative

Zhang, Miller & Bowman benchmarked AlphaFlow, BioEmu, PocketMiner and CryptoBank against
FAST/seeded MD and against thiol-labelling experiments on Ebola VP35 and TEM β-lactamase plus
mutants, with pocket openness defined by a 1.0 nm Cα–Cα threshold [VERIFIED-FULLTEXT,
doi:10.64898/2026.01.21.700870]. For VP35 wild type, experiment gives **28.6 ± 0.5% open**; BioEmu
predicts **10.4%**, AlphaFlow **<1%**, FAST+seeding MD **31.8%**. PocketMiner and CryptoBank
captured the direction of the F239A and I303A increases but both missed the A291P decrease. The
authors' conclusion, verbatim:

> "Multiple methods are remarkably successful at predicting whether a mutation will increase or
> decrease the probability of cryptic pocket opening. However, none can reliably predict the
> absolute probability of pocket opening."

and

> "At present, the speed of AI-based methods makes them appealing for triaging large numbers of
> proteins."

Read that beside `02` §12: this is a fourth independent instance of a method being right on
_ranking_ and wrong on the _quantity the deliverable needs_.

**Verdict.** Not a method — a benchmark. C1/C2 not applicable. It is evidence against adopting any
AI cryptic-pocket score as more than a triage feature.

---

## 3. Ligand-binding-site and druggability ranking from apo structure

### 3.1 fpocket — the alpha-sphere baseline, and the apo number

Voronoi tessellation via Qhull, alpha spheres of varying radius, clustered into pockets. Detection:
**94% (holo) and 92% (apo)** of true pockets within the best three ranked pockets
[VERIFIED-ABSTRACT, doi:10.1186/1471-2105-10-168]. Note the near-absence of an apo penalty for
_detection_, which contrasts sharply with the ESSA apo penalty for _allosteric ranking_ (§2.3) —
finding a cavity in an apo structure is easy; deciding which cavity matters is not.

The per-pocket descriptor list, verbatim from the tool's own documentation, is the transferable
part [VERIFIED-FULLTEXT, `Discngine/fpocket` `doc/GETTINGSTARTED.md`]:

```
Score · Druggability Score · Number of Alpha Spheres · Total SASA · Polar SASA · Apolar SASA ·
Volume · Mean local hydrophobic density · Mean alpha sphere radius · Mean alp. sph. solvent access ·
Apolar alpha sphere proportion · Hydrophobicity score
```

Our own `cavity_volume` baseline (`00-conventions.md` §6) is a zero-parameter instance of exactly
one of these twelve. **Mean local hydrophobic density** and **apolar alpha-sphere proportion** are
the two that are cheapest to add and least correlated with volume.

**Verdict.** C1 PASS, C2 PASS, C6 CONDITIONAL (geometry of coordinates, not contact topology).

### 3.2 Druggability — fpocket's logistic score and PockDrug

Schmidtke & Barril fit a **logistic regression** on fpocket descriptors over a curated druggable/
non-druggable cavity set and report that "polar groups in druggable binding sites have properties
that enable them to play a decisive role in ligand recognition" [VERIFIED-ABSTRACT,
doi:10.1021/jm100574m]. No accuracy figure appears in the retrieved abstract.

PockDrug is a **consensus of seven linear discriminant analysis models** over three property
classes: hydrophobicity combined with volume, aromaticity, and hydroxyl-group composition. On the
NRDLD holo set, accuracy >83% up to 94.6% and MCC >0.650 up to 0.885. On the **Apo139** set,
average accuracy **92.5%** but average MCC only **0.48** — and its two configurations score
accuracy 91.4% / MCC 0.45 (on fpocket pockets) and 93.5% / MCC 0.515 (on DoGSite pockets), against
the **fpocket score at 47.5% accuracy / MCC 0.198** and DoGSiteScorer at 79.1% / 0.328
[VERIFIED-FULLTEXT, doi:10.1093/nar/gkv462].

The accuracy/MCC divergence on Apo139 (92.5% vs 0.48) is the same imbalance artefact `02` §12
documents. It is a reminder that **on apo input, a druggability score's headline accuracy is
carried by the negative class.**

**Verdict.** C1 PASS (apo pockets are explicitly supported). C2 PASS. C6 FAIL (physicochemical
descriptors, not topology).

### 3.3 P2Rank — the feature vector and the aggregation formula

Generate regularly spaced points on the solvent-accessible surface; describe each point by a
**35-dimensional** feature vector of physico-chemical properties projected from neighbouring
protein atoms; predict a per-point ligandability with a random forest; cluster high-scoring points;
rank clusters by

```
pocket_score = Σ_{p ∈ cluster} ligandability(p)²
```

[VERIFIED-FULLTEXT, doi:10.1186/s13321-018-0285-8]. The single most important feature, by the
paper's own analysis, is **protrusion**: "a number of protein atoms within a sphere of 10 Å around
a SAS point" [VERIFIED-FULLTEXT, same].

DCA success at a 4 Å threshold, Top-n / Top-(n+2):

| method         | COACH420 Top-n | COACH420 Top-(n+2) | HOLO4K Top-n | HOLO4K Top-(n+2) |
| -------------- | -------------- | ------------------ | ------------ | ---------------- |
| P2Rank         | **72.0%**      | **78.3%**          | **68.6%**    | **74.0%**        |
| MetaPocket 2.0 | 63.4%          | 74.6%              | 57.9%        | 68.6%            |
| fpocket        | 56.4%          | 68.9%              | 52.4%        | 63.1%            |
| DeepSite       | 56.4%          | 63.4%              | 45.6%        | 48.2%            |
| SiteHound      | 53.0%          | 69.3%              | 50.1%        | 62.1%            |

[VERIFIED-FULLTEXT, same]. CHEN11 = 251 proteins / 476 ligands; COACH420 = 420 single-chain
structures.

Two constructions transfer. (i) **Sum of squared per-point scores** as the cluster aggregator —
squaring rewards a few confident points over many mediocre ones, which is the opposite of what a
mean does, and is directly applicable to turning our per-residue propagation scores into a pocket-
level or region-level score for the top-5 hit list. (ii) **Protrusion** as a one-line per-residue
feature: an atom count in a 10 Å ball. Cheaper than any pocket detector and it is the top feature
in the best general pocket ranker in the table.

**Verdict.** C1 PASS, C2 PASS, C6 FAIL (surface geometry). "Legal\*" for the trained random forest,
per `02` §3.

### 3.4 Pure-geometry detectors and the apo penalty

Modern re-benchmark of eight geometric detectors on the 48-protein PocketPicker set, hit criterion
= the ligand's solvent-accessible surface lies entirely inside the extruded pocket volume
[VERIFIED-FULLTEXT, doi:10.1016/j.csbj.2025.07.054]:

| method       | Top-1 unbound | Top-1 bound | Top-3 unbound | Top-3 bound |
| ------------ | ------------- | ----------- | ------------- | ----------- |
| fpocket      | 69%           | 83%         | **94%**       | 92%         |
| pyCAST       | 60%           | 83%         | 90%           | 89%         |
| PocketPicker | 69%           | 72%         | 85%           | 85%         |
| LIGSITEcs    | 60%           | 69%         | 77%           | 87%         |
| LIGSITE      | 58%           | 69%         | 75%           | 87%         |
| CAST         | 58%           | 67%         | 75%           | 83%         |
| PASS         | 60%           | 63%         | 71%           | 81%         |
| SURFNET      | 52%           | 54%         | 75%           | 78%         |

The original LIGSITEcsc report gives 71% / 75% on its own 48-unbound and 210-bound sets
[VERIFIED-ABSTRACT, doi:10.1186/1472-6807-6-19].

Two observations. First, **the unbound Top-1 numbers are 52–69% for every zero-parameter geometric
detector** — the apo penalty in this task is 10–20 points, and it lands on rank-1 far harder than
on top-3. Second, LIGSITEcsc's own conclusion was that "the use of the Connolly surface leads to
slight improvements, the prediction **re-ranking by conservation** to significant improvements"
[VERIFIED-ABSTRACT, same]. Re-ranking a geometric candidate list by an orthogonal signal is the
oldest working pattern in this literature, and it is structurally identical to what our pipeline
does when it re-ranks pockets by propagation score.

**Verdict.** All eight: C1 PASS, C2 PASS, C6 FAIL.

---

## 4. Epitope and functional-site prediction — mined only for score construction

### 4.1 ElliPro — a zero-parameter geometric per-residue score

Approximate the protein as an ellipsoid that can be inflated to enclose any percentage of its
atoms. For each residue, the **protrusion index** is "percentage of the protein atoms enclosed in
the ellipsoid at which the residue first becomes lying outside the ellipsoid," using the residue's
centre of mass rather than its Cα [VERIFIED-FULLTEXT, doi:10.1186/1471-2105-9-514]. Residues are
then clustered in three recursive passes (single residues + neighbours within R → clusters sharing
≥3 centres of mass within R → clusters sharing residues), and "the score for each epitope is
defined as a PI value averaged over epitope residues" [VERIFIED-FULLTEXT, same].

On 39 epitopes in 39 structures, ElliPro reaches **AUC 0.732**, against DOT 0.693, PatchDock 0.656,
DiscoTope 0.601, ProMate 0.589, CEP 0.544, PPI-PRED 0.528 [VERIFIED-FULLTEXT, same].

This is the best value-per-line score in the whole file: a covariance eigendecomposition of the
coordinate cloud plus a rank, no parameters, no training, no external data. It measures _shape
extremity_, which is orthogonal to both distance-from-active-site and cavity volume.

**Verdict.** C1 PASS, C2 PASS, C6 FAIL (shape, not topology) — but as an auxiliary feature it is
unconditionally clean.

### 4.2 DiscoTope-3.0 — inverse-folding latents, and a calibration trick worth stealing

Per-residue input is **535 dimensions**: ESM-IF1 inverse-folding embedding (512) + one-hot residue
(20) + antigen length (1) + pLDDT (1) + relative surface accessibility via Shrake–Rupley (1). Model
is an ensemble of 100 XGBoost regressors (max_depth 4, subsample 0.50, n_estimators 200); the score
is the ensemble mean [VERIFIED-FULLTEXT, doi:10.3389/fimmu.2024.1322712].

The calibration step is the transferable piece:

```
calibrated_score_i = (score_i − μ̂) / σ̂
# μ̂, σ̂ come from generalized additive models fitted on
#   (antigen length, mean surface-residue score)
```

[VERIFIED-FULLTEXT, same]. This makes scores comparable **across proteins of different size and
different overall score level** — which is precisely the problem our evaluation layer faces when
pooling four primary and nine secondary arms.

Numbers, positive class = "any antigen residue containing at least 1 heavy atom within 4 Å of an
antibody heavy atom", external test set of 24 antigens filtered to ≤20% similarity to training:
AUC-PR **0.232 ± 0.02** (AlphaFold structures) and **0.223 ± 0.02** (solved), AUC-ROC 0.783 / 0.795,
against BepiPred-3.0 0.177 ± 0.02, SEMA 0.185 ± 0.02, ScanNet 0.127 ± 0.011 (predicted) and
0.157 ± 0.012 (solved) [VERIFIED-FULLTEXT, same]. Structure-derived representations beat
sequence-derived ones by a small margin: AUC-ROC **0.767 ± 0.003 vs 0.751 ± 0.003**
[VERIFIED-ABSTRACT, same].

Two things follow. First, this is a well-run 2024 tool on a well-defined task and **its AUC-PR is
0.22–0.23**. That is the honest magnitude for a hard, imbalanced per-residue ranking problem, and
it is a far more useful reference point than the 0.9-something AUPRCs in §1.5. Second, structure
adds only ~0.016 AUC-ROC over sequence here — evidence against assuming a structural
representation is automatically the stronger one.

**Verdict.** C1 PASS (single structure at inference). C2 PASS (no MD). C6 FAIL. "Legal\*" for the
trained weights.

### 4.3 SEMA — a graded regression target instead of a binary label

SEMA fine-tunes **ESM-1v** (SEMA-1D, sequence) and **ESM-IF1** (SEMA-3D, structure) to predict, per
residue, "the log-scaled expected number of contacts with antibody residues" — a continuous,
interpretable target rather than an epitope/non-epitope bit. ROC AUC **0.76** on an independent
test set; ESM-1v 0.70 / 0.67 and ESM-IF1 0.75 / 0.73 on "masked" and "unmasked" test sets
[VERIFIED-ABSTRACT, doi:10.3389/fimmu.2022.960985].

The construction is what matters: **replace the binary label with a graded contact count.** Our own
label sets are binary residue memberships. A graded target — for instance, number of effector heavy
atoms within a cutoff, or fractional burial by the effector — would carry strictly more information
per positive at a task where positives are scarce (1.3–8% prevalence, `02` §2). This is a change to
the _evaluation_ layer, which is frozen (`00-conventions.md` §7, ADR on the evaluation freeze), so
it is recorded here as an observation for a future protocol version, not a proposal to reopen one.

**Verdict.** C1 PASS, C2 PASS, C6 FAIL.

---

## 5. Protein language model and inverse-folding zero-shot residue scoring

This section matters more than the others because it is the only family in the file that is
C1/C2-legal from **sequence and backbone alone** — no ligand, no trajectory, no allosteric label.
`02-ai-methods.md` §4 and §9 already argue that sequence is legal input. What follows is the score
construction and, critically, the **source of the AUPR 0.06 claim** that `00-conventions.md` §5
records without a citation.

### 5.1 The four score constructions

From Meier et al.'s zero-shot variant-effect work, all four are per-position functions of a masked
language model with **no fitted parameters** [VERIFIED-FULLTEXT for the entropy claim,
VERIFIED-ABSTRACT for the score definitions, doi:10.1101/2021.07.09.450648]:

1. **Masked marginal** (best performing): mask position i, read `log p(a | x_\i)`, score a
   substitution as `log p(mut) − log p(wt)`.
2. **Wild-type marginal**: one forward pass on the unmasked sequence, same log-odds.
3. **Mutant marginal**: pass the mutated sequence.
4. **Pseudo-log-likelihood**: `PLL(x) = Σ_i log p(x_i | x_\i)`.

The exact equations sit in the paper's Appendix A and were **not** retrieved this session; the four
names and the log-odds form were.

Two more, from the structure side:

5. **Inverse-folding log-odds.** ProteinMPNN gives `p(a | backbone)` at every position; native
   sequence recovery is **52.4%** against Rosetta's 32.9% [VERIFIED-ABSTRACT,
   doi:10.1126/science.add2187]. ESM-IF1 reaches **51%** overall and **72% for buried residues**
   after training on 12 M AlphaFold2-predicted structures [VERIFIED-ABSTRACT,
   doi:10.1101/2022.04.10.487779].
6. **Entropy of the designed-residue distribution.** `H_i = −Σ_a p(a|·) log p(a|·)` at position i,
   from either model.

### 5.2 Published evidence that these mark functional sites

- **Entropy is lowest at the active site.** Meier et al., Figure 5: "Low-entropy positions cluster
  in the active site," with "side chains for the top 10 positions with lowest prediction entropy
  shown in blue" for DNA methylase HaeIII (PDB 1DCT) [VERIFIED-FULLTEXT,
  doi:10.1101/2021.07.09.450648]. This is a single-protein figure, not a benchmark. It is the
  source of the widely repeated claim; treat it as an existence proof, not a measured hit rate.
- **Attention targets binding sites.** Vig et al. report that attention in protein transformers
  "targets binding sites, a key functional component of proteins," consistently across BERT, ALBERT
  and XLNet and two datasets [VERIFIED-ABSTRACT, arXiv:2006.15222].
- **Unsupervised recovery of 52.13% of the binding site.** A reaction-SMILES-plus-sequence language
  model recovers, "with no supervision, 52.13% of the binding site when considering co-crystallized
  substrate-enzyme structures as ground truth, vastly outperforming other attention-based models"
  [VERIFIED-ABSTRACT, doi:10.1016/j.csbj.2024.04.012]. Needs the substrate SMILES, so C1 is
  CONDITIONAL for us (the natural substrate is not the target's holo structure, but it is
  ligand information).
- **Embeddings reproduce MSA conservation without an MSA.** Linear/ridge/LASSO/elastic-net
  regression from **ESM2-3B** embeddings onto Jensen–Shannon divergence against a BLOSUM62
  background reaches Pearson **0.71** per residue and 0.74 per sequence, and — the useful part —
  assigns a score to _every_ residue including unaligned regions where MSA methods cannot
  [VERIFIED-FULLTEXT, doi:10.1093/bib/bbac599].
- **Zero-shot segmentation.** ProtT5-XL-U50 embeddings plus change-point detection (RBF-kernel cost,
  window 30, comparing 15 residues to the next 15) with **no parameters trained** puts 40–50% of
  predicted boundaries within 10 residues of a known UniProt boundary, average IoU 0.525
  [VERIFIED-FULLTEXT, doi:10.1371/journal.pcbi.1012929].
- **Supervised, for contrast.** An ESM-2 MLP head trained on per-residue ligand-contact labels over
  96,000 binding sites from 68,000 PDB structures reaches AUC >0.92 on a random split and **0.81 on
  the hardest tree-based split** [VERIFIED-FULLTEXT, doi:10.1093/bioinformatics/btaf284].

### 5.3 The source of the "AUPR 0.06" claim — found

`00-conventions.md` §5 records, unsourced, that "protein language models collapse on allosteric
sites. AUPR 0.64–0.76 on orthosteric against **0.06** on allosteric in the same proteins, with
AUROC still 0.70." **This session located the primary source.**

> Riedlová K, Škrhák V, Gatlin WG, Ludwick M, Turano L, Novotný M, Hoksza D, Verkhivker GM.
> "Predicting and Decoding Allosteric Binding Sites Using Protein Language Models and
> Structure-Based Machine Learning: An Energy Landscape-Guided Explainable AI Framework."
> _J Chem Theory Comput_ 22(10):5326, 2026. **doi:10.1021/acs.jctc.6c00427**, PMID 42093179,
> PMCID PMC13217555. Preprint: bioRxiv **doi:10.64898/2026.01.05.697819**.

The preprint abstract carries the exact quoted sentence: "both methods achieve high precision-recall
(AUPR = 0.64–0.76) on orthosteric sites, PLM performance collapses on allosteric sites
(AUPR = 0.06), despite retaining moderate ranking ability (AUROC = 0.70)" [VERIFIED-ABSTRACT,
bioRxiv 10.64898/2026.01.05.697819]. The published version's own table gives the same result at
slightly different precision [VERIFIED-FULLTEXT, doi:10.1021/acs.jctc.6c00427]:

| inhibitor class                        | positive-residue definition             | prevalence | AUROC     | AUPR      |
| -------------------------------------- | --------------------------------------- | ---------- | --------- | --------- |
| Type I (orthosteric)                   | within 4 Å of an ATP-competitive ligand | 4.75%      | 0.968     | 0.629     |
| Type I.5 (orthosteric)                 | "                                       | 6.15%      | 0.975     | 0.749     |
| Type II (orthosteric)                  | "                                       | 6.67%      | 0.941     | 0.680     |
| Type III (allosteric-proximal)         | >6.0 Å from the hinge                   | 5.40%      | 0.910     | 0.363     |
| **Type IV / ALLO (allosteric-distal)** | **>6.5 Å from hinge and C-helix**       | **3.22%**  | **0.676** | **0.077** |

**Four corrections to how `00-conventions.md` §5 states this claim, all material.**

1. **The model is supervised, not zero-shot.** The PLM is **ESM2-650M** with the head replaced by a
   linear layer `W ∈ ℝ^{1280×1}` plus sigmoid, producing `p_i = σ(W h_i + b)`, _trained_ on
   binding-site labels [VERIFIED-FULLTEXT, doi:10.1021/acs.jctc.6c00427]. The collapse therefore
   says nothing directly about masked-marginal entropy, pseudo-log-likelihood, or inverse-folding
   log-odds. Those remain untested on allosteric sites by this paper.
2. **The comparator is P2Rank v2.5**, aggregated to residues by taking, for each residue, "the
   maximum probability over all predicted pockets that contained that residue" ("ANY-pocket"
   aggregation) [VERIFIED-FULLTEXT, same]. So the §3 machinery and the §5 machinery were compared
   head to head on the same labels — and both fall on allosteric sites.
3. **The published Type-IV numbers are AUROC 0.676 / AUPR 0.077**, not 0.70 / 0.06; the 0.70/0.06
   pair is the preprint's abstract rounding. Both are real; cite the published pair.
4. **The corpus is kinases only** — 453 human kinases, 10,301 KinCoRe complexes, with leakage
   controlled by "removing all evaluation chains whose sequences overlapped with those used for PLM
   training" [VERIFIED-FULLTEXT, same]. It is a strong result _within kinase domains_. It is not a
   demonstration that PLMs collapse on allosteric sites in general, and BCR-ABL1 is a kinase, so
   the finding is directly on-target for at least one of our arms.

The gradient across the five rows is itself the finding: AUPR falls monotonically as the positive
class moves away from the orthosteric pocket — 0.749 → 0.680 → 0.363 → 0.077. **A binding-site
scorer's accuracy is a function of distance from the orthosteric site**, which is the same confound
`00-conventions.md` §5 already records for our own `−distance` baseline, seen from the other side.

### 5.4 Why — the stability–function trade-off, and frustration

The mechanism is old and independently established. Shoichet, Baase, Kuroki & Matthews mutated
functionally important residues in T4 lysozyme: six mutations at two catalytic residues "abolished
or reduced enzymatic activity but increased thermal stability by 0.7–1.7 kcal·mol⁻¹," and nine at
two substrate-binding residues "increased stability by 1.2–2.0 kcal·mol⁻¹, again at the cost of
reduced activity" [VERIFIED-ABSTRACT, doi:10.1073/pnas.92.2.452]. Functional residues are not
stability-optimal.

That is exactly the quantity an inverse-folding model computes. ProteinMPNN and ESM-IF1 are trained
to predict the residue that _fits the backbone_; where the native residue is present for function
rather than for fold, the model should disagree with it. The disagreement is a functional-site
signal that costs one forward pass and no training.

The frustration literature says the same thing with an energy function. The Frustratometer's
authors state that "sites of high local frustration often correlate with functional regions such as
binding sites and regions involved in allosteric transitions" [VERIFIED-ABSTRACT,
doi:10.1093/nar/gkw304]. And Riedlová et al. sharpen it into a **discriminating** claim: computing,
for each residue, how many of its ≤5 Å Cα–Cα contacts are minimally frustrated (Z > 0.78), highly
frustrated (Z < −1.0) or neutral, they find "orthosteric sites display a pronounced shift toward
minimal frustration … whereas allosteric sites show predominant neutral local frustration and an
elevated population of highly frustrated residues" [VERIFIED-FULLTEXT,
doi:10.1021/acs.jctc.6c00427].

**That is a band-pass, not a threshold, and it is the single most actionable mechanistic statement
retrieved in this session.** Orthosteric = low frustration. Allosteric = _middle_. Irrelevant
surface = high. Every monotone score in the literature — conservation, centrality, PLM
log-likelihood, binding-site probability — is a _monotone_ readout, and a monotone readout cannot
select a middle band. This is a plausible unified explanation for why every predictor in this file
that works on orthosteric sites fails on allosteric ones, and it is directly implementable (§7,
item 2).

_Caveat:_ the band-pass reading is my inference from Riedlová's frustration distributions, not a
claim their paper makes in that form. Tagged [UNVERIFIED] and it must be measured on our own labels
before it is relied on.

**Verdicts for section 5.** Zero-shot PLL / masked marginal / entropy: C1 PASS, C2 PASS, C6 FAIL
(sequence only, auxiliary feature). ProteinMPNN and ESM-IF1 log-odds and entropy: C1 PASS
(backbone only — no ligand, no holo), C2 PASS (PDB and AlphaFold2 structures, no MD), C6 FAIL.
Supervised PLM heads (Riedlová's, Oruç's, SEMA, DiscoTope): C1 PASS at inference, C2 PASS, C6 FAIL,
plus the `02` §3 "Legal\*" training-split check. Reaction-SMILES attention (Teukam et al.): C1
CONDITIONAL — requires substrate identity.

---

## 6. Rigidity theory and constraint counting

Topology-only, no energy minimisation, no dynamics, no fitted weights. This family is C1/C2/C6-clean
by construction, which is why it is worth the space even though its published record is
qualitative. `05-adjacent-task-transfer.md` §8 and (e) established that rigidity has already been
used for allosteric-site prediction and that "no comparable AUC" exists. This section supplies what
that file could not: the **exact per-residue indices**.

### 6.1 The pebble game and the flexibility index — FIRST

Represent the protein as a bar-and-joint framework: covalent bonds, hydrogen bonds and salt bridges
are distance constraints, dihedral rotations are the degrees of freedom. The pebble game counts
degrees of freedom against constraints and decomposes the network into rigid clusters,
overconstrained regions and underconstrained (flexible) regions. "The number of extra constraints
or remaining degrees of bond-rotational freedom within a substructure quantifies its relative
rigidity/flexibility and **provides a flexibility index for each bond in the structure**." The
procedure is "approximately a million times faster than molecular dynamics simulations and captures
the essential conformational flexibility of the protein main and side-chains **from analysis of a
single, static three-dimensional structure**" [VERIFIED-ABSTRACT, doi:10.1002/prot.1081]. Validated
on HIV protease, adenylate kinase and dihydrofolate reductase. ProFlex is the Kuhn-lab distribution
of the same algorithm.

### 6.2 Constraint dilution — the three indices worth copying

Constraint Network Analysis (Gohlke lab) simulates thermal unfolding by "successively removing
non-covalent constraints from the network," sweeping the hydrogen-bond energy cutoff `E_cut` from
−0.1 to −6.0 kcal/mol. Three indices, all verbatim [VERIFIED-FULLTEXT,
doi:10.1371/journal.pcbi.1004754]:

- **Rigidity index `r_i`** — "defined for each covalent bond i between two atoms as the `E_cut`
  value during the thermal unfolding simulation at which the bond changes from rigid to flexible."
- **Stability map `rc_ij`** — "a two-dimensional itemization of `r_i` … indicates for all residue
  pairs the `E_cut` value at which a rigid contact between the two residues i, j is lost, i.e. when
  the two residues stop belonging to the same rigid cluster."
- **Neighbour stability map** — "the stability map `rc_ij` … filtered such that only rigid contacts
  between residues that are at most 5 Å apart from each other are considered."

Structural weak spots are "residues in the neighborhood of the largest rigid cluster from which
they segregate" at a major phase transition. The software is CNA [VERIFIED-ABSTRACT,
doi:10.1021/ci400044m]; the field review is Hermans et al. [VERIFIED-ABSTRACT,
doi:10.1002/wcms.1311].

**`rc_ij` restricted to j ∈ active site is a source-anchored per-residue score, and it is the exact
rigidity analogue of what our pipeline is asked to compute.** `05` §8 flagged "targeted rigidity
percolation" as not retrieved for protein allostery; this is the index it would be built on. §7
item 1 gives a cheap surrogate.

### 6.3 FRODA — motion without dynamics

Determine the rigid regions, replace them by ghost templates, then move atoms by random steps that
keep all covalent, hydrophobic and hydrogen-bond constraints satisfied and avoid van der Waals
overlaps. "The available conformational phase space of a 100 residue protein can be well explored
in approximately 10–100 minutes … using a single processor," with barnase results "showing good
agreement with nuclear magnetic resonance experiments" [VERIFIED-ABSTRACT,
doi:10.1088/1478-3975/2/4/S07]. This is a third C2-legal ensemble generator to set beside Str2Str
and ENM-mode sampling in `05` §3, and the only one whose moves are guaranteed to respect the
contact network exactly.

### 6.4 Rigidity-based perturbation for allostery — Pfleger et al. 2017

Integrates an ensemble-based perturbation approach with rigidity/flexibility analysis. The model
"by definition, excludes the possibility of conformational changes, evaluates static, not dynamic,
properties of molecular systems, and describes allosteric effects due to ligand binding in terms of
a novel free-energy measure." Validated on eglin c, PTP1B and the LFA-1 I domain; "in all cases, it
successfully identified key residues for signal transmission in very good agreement with the
experiment," and it "correctly and quantitatively discriminated between positively or negatively
cooperative effects for one of the systems" [VERIFIED-ABSTRACT, doi:10.1021/acs.jctc.7b00529].

No AUC, no top-k hit rate, no stated null. **Write "unknown" for the quantitative comparison
against our four bars** — this is `05`'s conclusion, re-confirmed with the primary citation now
pinned.

**Verdicts for section 6.** FIRST/pebble game, CNA indices, FRODA, Pfleger perturbation: C1 PASS,
C2 PASS, C6 PASS — all four. This is the only family in the file that is unconditionally clean on
all three constraints and has a source-anchored readout.

---

## 7. What this changes for our pipeline

Six implementable items and two prohibitions. Every score below is computable from **only** a
residue contact graph with heavy-atom minimum distances, Cα/heavy-atom coordinates, the one-letter
sequence, per-atom B-factors, and the named active-site residue set. Ranked by expected information
gained per unit of implementation cost.

---

**1. Bottleneck (minimax-path) contact strength to the active site — `classical/`, Phase 1.4.**

The cheap surrogate for CNA's `rc_iA` (§6.2): replace "stop sharing a rigid cluster" with "stop
sharing a connected component under edge dilution." It is not `−distance` (a sum along a path) and
not effective resistance (`05` §STEP-3a, a parallel-path sum); it is the _weakest link_ on the best
path, which is what a percolation threshold measures.

```python
W[i, j] = 1.0 / max(dmin[i, j], 1e-9)  # heavy-atom minimum distance -> contact strength
T = maximum_spanning_tree(W)  # scipy: -minimum_spanning_tree(-W)
# bottleneck(i, A) = the minimum edge weight on the unique T-path from i to the nearest anchor
score[i] = min(w for w in tree_path(T, i, nearest_anchor(i, A)))
```

Equivalent one-pass form: sort edges by descending weight, union-find, and record for each residue
the weight at which it first joins the active site's component. Cost: one MST plus N tree walks,
~15 lines. Expected information: high — it is source-anchored by construction, it is a
rigidity-percolation observable rather than a centrality, and neither `00-conventions.md` §5's
eleven closed points nor `05`'s transfer table contains it. **Verify:** Spearman against
`ctrl_closeness = −distance` must be well below 1 or the item is dead.

---

**2. Neutral-frustration band-pass from inverse-folding entropy — `classical/`, Phase 1.4.**

Operationalises the strongest mechanistic finding in this file (§5.4) without implementing AWSEM.
The designed-residue distribution from a stability-optimising inverse-folding model is a per-residue
frustration proxy: minimally frustrated positions have a peaked distribution, neutrally frustrated
ones a flat-but-not-random one.

```python
p = proteinmpnn(backbone_coords).per_position_distribution()  # N x 20, pretrained, no training
H = -(p * np.log(p + 1e-12)).sum(axis=1)  # entropy per residue
# Riedlova 2026: orthosteric -> minimally frustrated (low H); allosteric -> NEUTRAL (mid H)
neutral = np.exp(-((H - np.median(H)) ** 2) / (2 * mad(H) ** 2))  # band-pass, not a threshold
score = neutral * surface_exposed  # exclude the buried core
```

Cost: one pretrained forward pass, ~15 lines. Expected information: high, and it is the only item
here that is _designed to be non-monotone_ — every other score in the literature is monotone and
therefore structurally unable to select a middle band (§5.4). **Verify before trusting:** measure
the H distribution for known-orthosteric versus known-allosteric residues on the curated external
corpus (not our frozen arms), and confirm the band-pass shape empirically. The band-pass reading is
[UNVERIFIED] inference, not a retrieved result. **C1 note:** ProteinMPNN's weights are fitted on PDB
backbones with no allosteric or ligand label, so the `02` §3 "Legal\*" risk is lower here than for
any ASD-trained tool — but it is not zero and should be recorded.

---

**3. ESSA essentiality via first-order perturbation — `classical/`, Phase 1.4.**

`00-conventions.md` §6 names ESSA as one of the four bars we must clear, and it is not implemented.
Its published form re-diagonalises the network once per residue, which is O(N) eigen-solves. First-
order Rayleigh–Schrödinger removes all but one.

```python
G = kirchhoff(ca_coords, cutoff=10.0)  # GNM
lam, U = np.linalg.eigh(G)  # once
for i in residues:
    dG = crowding_perturbation(i)  # +k on G_ii and its contact entries,
    # k = number of heavy atoms in residue i
    dlam = np.einsum("k,kl,l->", ...)  # dlam_k = u_k^T dG u_k, k = 1..10
    essa[i] = np.mean(dlam[1:11] / lam[1:11])
z = (essa - essa.mean()) / essa.std()
```

Cost: one eigendecomposition plus N × 10 quadratic forms, ~25 lines. Expected information: it _is_
one of the four bars, so the information is not new — but not having it is a hole in the comparison
table. **Verify:** re-diagonalise fully for 20 random residues and check the first-order
approximation reproduces the ranking; if it does not, fall back to the exact loop (N ≈ 300 makes it
affordable anyway).

---

**4. Ellipsoidal protrusion index — `network/` or `classical/`, cheap feature.**

ElliPro's PI (§4.1), zero parameters, decorrelated from both cavity volume and distance.

```python
X = heavy_atom_coords - heavy_atom_coords.mean(0)
w, V = np.linalg.eigh(np.cov(X.T))
r = np.sqrt(((X @ V) ** 2 / w).sum(axis=1))  # ellipsoidal radius per atom
pi_atom = rankdata(r) / len(r) * 100  # % of atoms enclosed when this atom exits
PI[i] = pi_atom[atoms_of_residue(i)].mean()
```

Cost: ~8 lines. Expected information: moderate — 0.732 AUC on epitopes with no training
(doi:10.1186/1471-2105-9-514), and it measures shape extremity, which no current baseline of ours
does. Use it as a covariate and as a decoy-pocket generator distinct from `cavity_volume`.

---

**5. Orthosteric anti-filter — `scoring/` composition, and a framing change.**

§0 and §5.3 together say that centrality-like and binding-site-like scores find the orthosteric
site. We are given the orthosteric site. So the correct use of such a score is subtraction:

```python
ortho[i] = shell3[i] ** 3 * np.exp(0.25 * (sc_degree[i] - mean_sc_degree_of_type(seq[i])))
ortho = (ortho - ortho.min()) / (ortho.max() - ortho.min())  # Slama 2008, type prior dropped
final[i] = propagation[i] * (1.0 - ortho[i])
```

where `shell3[i] = |{j : graph_distance(i, j) == 3}|` on the 4.2 Å side-chain contact graph. Cost:
one BFS plus ~10 lines. Note the **type prior is deliberately dropped** so that the score is
zero-parameter and cannot leak an external label set — that costs some of Slama's 28.1% precision
but keeps the item unconditionally C1/C2-clean. Expected information: moderate-to-high and
_orthogonal_ — this changes the composition of the final score rather than adding a competing one,
and it is the direct pipeline consequence of the file's headline result.

---

**6. Cross-arm calibration — `scoring/`, before any pooling.**

DiscoTope-3's trick (§4.2). Not new signal; a precondition for comparing numbers across arms of
different size.

```python
mu_hat, sd_hat = fit(target=score_mean, features=[n_residues, mean(score[surface])])
score_cal = (score - mu_hat) / sd_hat
```

Cost: ~6 lines. Expected information: zero new signal, near-zero cost, and it removes a size
confound from every pooled statistic the evaluation layer computes. Note: the evaluation protocol
is frozen (`00-conventions.md` §7), so this belongs on the _method_ side of the boundary — calibrate
the method's output before it is handed to `allo.scoring.score_arm`, do not change the harness.

---

**Do not build — two items, both of which look attractive.**

- **A supervised PLM head for allosteric-site prediction.** Refuted at the exact granularity we
  need: AUROC 0.676, **AUPR 0.077 at 3.22% prevalence**, on 453 kinases with sequence-overlap
  leakage control (§5.3, doi:10.1021/acs.jctc.6c00427). P2Rank on the same labels also fails. This
  is now a sourced closure of `00-conventions.md` §5's last bullet, and it should be recorded as
  such — with the correction that the finding does **not** cover zero-shot entropy, masked
  marginals, or inverse-folding log-odds, which item 2 above uses.
- **Any pretrained cryptic-pocket predictor.** CryptoSite fails C1 and C2 (MD at inference).
  PocketMiner fails C2. CryptoBank passes C2 but its labels are generated from >6 M apo/holo
  alignments across the PDB, which is a C1 hazard we cannot discharge without the training-chain
  list (§2.5). And the 2026 benchmark (§2.6) shows all four AI methods get the direction right and
  the magnitude wrong. If cryptic-pocket propensity is wanted, build it from the C2-legal twin:
  ENM-mode sampling plus a geometric detector, at AUC >0.8 (§2.2, doi:10.1002/prot.26027).

---

## Method

**Databases and routes.** All four routes named in `00-conventions.md` §3 were used: Europe PMC
search and full-text (`/search?query=...&format=json&resultType=core` and PMC article pages), the
arXiv API (`export.arxiv.org/api/query`), PubMed-indexed general web search, and direct WebFetch
against bioRxiv, PLOS, Frontiers, Springer, OUP and ScienceDirect. Semantic Scholar was not used
(rate-limited, per §3). No file under `docs/benchmark/` was opened (§7 leakage guard).

**Counts.** 34 WebSearch queries run, all returned results. 57 WebFetch calls; 50 returned usable
content. Seven failures: Springer `link.springer.com` 303-redirected to an authentication IdP
(P2Rank); ScienceDirect returned HTTP 403 (Teukam et al., recovered via Europe PMC metadata); two
PDFs returned unparsable binary (the Gohlke-lab paper mirror, and the fpocket v2 manual); the
Europe PMC supplementary-file endpoint returned HTTP 520 (P2Rank feature table); and three arXiv API
queries returned `totalResults=0` (`"protein language model" + "active site" + entropy`;
`ti:"Learning inverse folding from millions of predicted structures"`; `abs:"inverse folding" +
abs:"functional sites"`) — the last two were recovered through Europe PMC.

**Sources screened in: 47**, distributed as 13 for §1, 8 for §2, 8 for §3, 3 for §4, 9 for §5, 6 for
§6.

**Representative queries.** §1: `catalytic residue prediction closeness centrality residue
interaction network`; `THEMATICS POOL electrostatics catalytic residue prediction`; `catalytic
residue prediction graph neural network 2023 2024 2025 benchmark MCC`; title lookups for Amitai,
Slama, Wei, Capra. §2: `cryptic pocket prediction single static apo structure without molecular
dynamics normal mode elastic network`; `Zheng normal mode analysis cryptic pocket`; `Essential Site
Scanning Analysis ESSA`; `CryptoBank`; `cryptic pocket prediction 2025 2026 without molecular
dynamics benchmark`; `PACKMAN hinge prediction alpha shape`. §3: `P2Rank feature vector DCA success
rate COACH420 HOLO4K`; `fpocket Voronoi alpha sphere druggability PockDrug`; `LIGSITE CASTp
Concavity PASS success rate top 1 top 3`. §4: `DiscoTope-3.0 ESM-IF per-residue score`;
`ElliPro protrusion index`; `SEMA epitope prediction ESM-2`. §5: `protein language model fails
allosteric sites AUPR orthosteric AUROC frustration kinase 2026`; `masked language model entropy per
residue identifies binding site pseudo-log-likelihood`; `ProteinMPNN log probability functional
site`; `inverse folding stability function trade-off`; `BERTology meets biology`. §6: `FIRST pebble
game rigid cluster decomposition flexibility index`; `Constraint Network Analysis Gohlke rigidity
allosteric`; `FRODA constrained geometric simulation`; `"neighbor stability map"`.

**Stopping rule.** Each of the six sections stopped when (a) every named method in the brief had a
retrieved citation with a DOI or arXiv ID, a stated score construction, and a C1/C2/C6 verdict, and
(b) three consecutive new queries in that section returned no method not already screened in. The
§5 search additionally did not stop until the AUPR 0.06 claim was traced to a primary source, which
was the one explicitly assigned open question.

**Not reached this session.**

1. **CatSite.** A tool by that exact name was **not retrieved** by the recorded search — three
   queries (Europe PMC `"CatSite" AND catalytic`; two web searches naming the journal and the
   task) returned only CatSId (a template-matching enzyme-function tool, doi:10.1371/journal.pone.0062535)
   and unrelated cathepsin papers. Per ADR 0019 and `00-conventions.md` §2 this is recorded as
   "not retrieved by the recorded search", **not** as an absence claim. The 2022–2026 deep
   catalytic-residue slot is filled by AEGAN, SCREEN, Squidly and PARSE instead.
2. **P2Rank's complete 35-feature list.** The supplementary file returned HTTP 520 and the Springer
   article page redirected to an authentication endpoint. Only the count (35), the single most
   important feature (protrusion, atom count in a 10 Å ball) and the cluster-aggregation formula
   (sum of squared per-point ligandabilities) were recovered.
3. **The functional form of fpocket's `Score` and `Druggability Score`.** The v2 manual PDF was
   unparsable binary and the _J Med Chem_ full text is paywalled. Only the descriptor names (from
   the tool's own repository documentation) and the model class (logistic regression) were
   recovered.
4. **CryptoSite's 0.83-versus-0.77 internal tension.** The retrieved full text reports an overall
   AUC of 0.83 and a three-feature final model at 0.77; which evaluation each refers to was not
   settled. Both are flagged in §2.1 rather than silently reconciled.
5. **CNA's own primary paper** (doi:10.1021/ci400044m, ACS). The index definitions in §6.2 come
   from the open-access Rathi et al. 2016 (doi:10.1371/journal.pcbi.1004754) instead, which states
   them verbatim.
6. **Any quantitative benchmark for rigidity-based allosteric-site prediction.** §6.4 confirms
   `05`'s finding: the record is qualitative. Written as "unknown", not inferred.
