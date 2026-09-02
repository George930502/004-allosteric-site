# Classical, Unsupervised, Physics-Based Baselines for Allosteric-Site Prediction

**Scope:** every classical method that ranks residues or pockets by dynamic or geometric
connectivity to a binding site using apo topology alone, with no MD trajectory and no
training data — the elastic-network lineage, graph/network-propagation methods,
allostery-specific unsupervised predictors, pocket-geometry detectors, and
trajectory-free statistical-mechanics routes. Deliberately excludes: quantum and
quantum-inspired methods, MD-trained or MD-run AI predictors (PocketMiner, CrypToth,
protein-language-model allostery predictors), circuit/hardware/noise literature, and
coarse-graining algorithms as a topic in their own right.
**Sibling files:** the quantum, quantum-inspired and hybrid methods (CTQW, ENAQT,
quantum kernels, quantum reservoir computing), circuit-resource and noise-resilience
literature, and coarse-graining/scalability literature are covered elsewhere in this
nine-part review. Supervised or MD-trained predictors (AlloSite, AlloPred, PASSer,
AllositePro, STINGAllo) are named here only where needed to interpret a reappraisal
(§7) or to contrast against the training-free methods that are this file's actual
subject; they are not evaluated here as candidates in their own right.
**Retrieved:** 2026-08-25.

---

## 1. Framing

`CHALLENGE.md` §4.2 requires a classical-analog comparison, and §6 conventions already
fixes four numbers our method must clear together: `−distance`, `cavity_volume`,
eigenvector centrality, and the APOP/ESSA unsupervised-ENM bar. This file is the
evidence base for that comparison. It does not re-run any of the eleven quantum
insertion points already closed (conventions §5) and it does not re-derive the four
numbers in conventions §6 — it supplies everything upstream and around them: what each
classical method actually computes, what it needs as input, whether it satisfies C1/C2,
and what its published number really measures once the field's own 2025–2026
reappraisals are taken into account.

Two structural facts organize everything below and are stated once here rather than
repeated per method:

- **Global scanners vs. source-conditioned methods.** `CHALLENGE.md` §4.1 asks for
  "connectivity ... in most cases, to an active site" — a **source-conditioned** score.
  Most classical allostery predictors (ESSA, APOP, GNM/ANM raw fluctuations, PARS,
  AlloSite, AlloPred, fpocket/pyKVFinder/CASTp) are **global scanners**: they rank every
  residue or pocket by an intrinsic property (mode-frequency shift, hydrophobicity,
  volume) with no reference to a named active site. A source-conditioned CTQW is not
  directly comparable to these in task shape. Only a small set of classical methods
  share the task shape — see §8(b).
- **"Training-free" is not what several of the papers commonly cited as training-free
  actually are.** AlloSite and AlloPred are SVM classifiers fit on labeled allosteric
  pockets. That is supervised learning, not a training-free physical computation, even
  though neither uses an MD trajectory. Flagged per method below.

---

## 2. The elastic-network lineage

**Tirion 1996** [VERIFIED-ABSTRACT] introduced the single-parameter elastic potential
that removes atomic force-field detail from normal-mode analysis: a uniform harmonic
spring between every pair of atoms within a cutoff reproduces experimental B-factors as
well as a full atomistic force field does. _Phys Rev Lett_ 77:1905–1908,
doi:10.1103/PhysRevLett.77.1905. This is C6 (the elastic network hypothesis) stated as a
testable claim, seven years before `CHALLENGE.md` cites it as an assumption. Input: Cα
(or all-atom) coordinates only. No training, no MD, no holo information — satisfies
C1/C2/C6 exactly.

**GNM — Bahar, Atilgan & Erman 1997** [VERIFIED-ABSTRACT]. "Direct evaluation of
thermal fluctuations in proteins using a single-parameter harmonic potential." _Folding
Des._ 2:173–181, doi:10.1016/S1359-0278(97)00024-2. Builds Tirion's potential on a Cα
contact graph at ~7 Å cutoff (the Kirchhoff/Laplacian matrix Γ) and predicts isotropic
residue fluctuations from Γ⁻¹. Same input/compliance profile as Tirion. This is the
substrate every ENM-based method below (ESSA, APOP, PRS, Chennubhotla–Bahar, STRESS)
builds on. `CHALLENGE.md` ref 16 (Erman 2006, _Biophys J_ 91:3589–3599,
doi:10.1529/biophysj.106.090803) is a GNM application review the challenge itself
already cites; not independently re-verified here.

**ANM — Atilgan et al. 2001** [VERIFIED-ABSTRACT]. "Anisotropy of Fluctuation Dynamics
of Proteins with an Elastic Network Model." _Biophys J_ 80:505–515,
doi:10.1016/S0006-3495(01)76033-X. Extends GNM to directional (3N×3N Hessian) motion.
Same compliance profile. GNM and ANM together are "the published bar" the roadmap
already names for Phase 1.4.

**Two-state ANM / PATH — Das, Gur, Cheng, Jo, Bahar & Roux 2014** [VERIFIED-ABSTRACT].
_PLoS Comput Biol_ 10:e1003521, doi:10.1371/journal.pcbi.1003521 (`CHALLENGE.md` ref
15). Builds a mixed two-well energy function with minima at **two given end-state
structures** and searches for the highest-energy structure the transition path most
likely visits. **This needs both conformers as input.** For a blind apo-only prediction
this is a hard C1 problem: the second "state" is either the unknown target conformation
(unavailable) or a holo-adjacent structure (a C1 violation to use). It is a
transition-path tool between two _known_ states, not a site predictor from one state,
and it is not usable as an apo-only baseline in this project. Flagged, not implemented.

**Perturbation-response scanning (PRS) — Atilgan & Atilgan 2009** [VERIFIED-ABSTRACT].
"Perturbation-Response Scanning Reveals Ligand Entry-Exit Mechanisms of Ferric Binding
Protein." _PLoS Comput Biol_ 5:e1000544, doi:10.1371/journal.pcbi.1000544. Perturbs each
residue in turn (a directed force in the ANM Hessian) and records the displacement
response of every other residue, producing an **N×N response matrix** — structurally the
closest classical analog to `CHALLENGE.md`'s required N×N connectivity-matrix output.
Reading a single row/column of that matrix (response of residue _i_ to a perturbation at
the active site, or vice versa) is exactly a source-conditioned score. Input: apo Cα
coordinates only, no training. Satisfies C1/C2/C6 exactly, and is compliant in task shape
with our own pipeline (§8b).

**ESSA — Kaynak, Bahar & Doruker 2020** [VERIFIED-FULLTEXT]. "Essential site scanning
analysis: A new approach for detecting sites that modulate the dispersion of protein
global motions." _Comput Struct Biotechnol J_ 18:1577–1586,
doi:10.1016/j.csbj.2020.06.020. Adds each residue's heavy atoms as extra ENM nodes (to
mimic ligand-induced crowding) and scores it by the resulting shift in global-mode
eigenvalues (a z-score). Input: apo Cα-only structure, default ProDy GNM/ANM parameters.
No training. **Dataset II** is 24 structures, "mainly the bound and unbound forms of 12
proteins" with ≥90% sequence identity, giving **14** matched allosteric-site
comparisons: apo top-3 success **7/14 = 50%**, holo top-3 success **10/14 ≈ 71%**
[VERIFIED-FULLTEXT]. This is the number conventions §6 already treats as the apo/holo
ENM bar; not re-derived here, only sourced.

**APOP — Bioinformatics 2023** [VERIFIED-FULLTEXT]. "Predicting allosteric pockets in
protein biological assemblages." doi:10.1093/bioinformatics/btad275. Detects pockets
with Fpocket, then stiffens the GNM springs across each pocket's lining residues (γ=1.0
baseline, perturbed γ=10.0 — fixed, not fitted) to emulate ligand binding, and ranks
pockets by the resulting global-mode frequency shift plus local hydrophobicity. Input:
Cα coordinates with ligands stripped ("holo-structures formed simply by removing any
ligand(s)"), i.e., apo-equivalent. No training, no cross-validation, no MD.
Three reported numbers, at three different scopes, and they must not be conflated:

- **92/104 (88.5%)** top-3 success on the full 104-protein set (61 monomers + 43
  multimers, pooled from the AlloPred test set, the ESSA apo/holo set, and additional
  literature cases) — **mixed apo and holo structures pooled together**
  [VERIFIED-FULLTEXT].
- **42/50 (84%)** top-3 on a 50-structure holo subset, against AlloPred's 68% and
  PASSer's 76% on the same subset [VERIFIED-FULLTEXT].
- The apo-restricted number, on what the fetched text describes as the same matched
  set ESSA uses: **holo 15/15 (100%)**, **apo 11/15 (73%)**, restated elsewhere in the
  paper as **86% (11/14)** [VERIFIED-FULLTEXT]. The 15-vs-14 denominator discrepancy
  is exactly as extracted and was not resolved against the primary PDF this session —
  flagged, not silently fixed.

APOP's apo-restricted top-3 (73–86%, on essentially ESSA's own 14-protein matched set)
is markedly higher than ESSA's 50% on the same kind of comparison, using a similar
unsupervised GNM-plus-pocket recipe. **This is new evidence against conventions §6's
framing of ESSA's 50% as the field's best clean apo/holo number** — see §8(a) for why it
does not survive the 2025–2026 reappraisals regardless.

**Zheng 2023 — coarse-grained normal-mode-guided conformational sampling**
[VERIFIED-ABSTRACT]. _J Chem Phys_ 158:124127, doi:10.1063/5.0141630 (`CHALLENGE.md`
ref 1). Samples along the lowest 30 ENM normal modes, reconstructs atomistic
backbone/side chains along each sampled displacement, and runs a pocket finder
(Concavity) on the resulting ensemble of conformers to expose pockets that are closed in
the static structure. Applied to four classical cryptic/allosteric cases (GluR2, GroEL,
a GPCR, myosin) as demonstrations, not a benchmarked hit rate against a labeled set — no
top-N number was retrieved this session. Input: single apo structure, ENM only, no
training. Satisfies C1/C2/C6. Directly relevant to the coarse-graining/scalability
sibling file, not re-covered there.

---

## 3. Network and graph analysis on the residue contact graph

**Dynamical network analysis — Sethi, Eargle, Black & Luthey-Schulten 2009**
[VERIFIED-ABSTRACT]. "Dynamical networks in tRNA:protein complexes." _PNAS_
106:6620–6625, doi:10.1073/pnas.0810961106. Builds a residue graph weighted by
generalized (dynamical) cross-correlation, finds communities (Girvan–Newman) and
shortest paths between a specified source and target. **The correlation matrix in the
original paper is derived from an MD trajectory** ("community network analysis derived
from molecular dynamics simulations") — a direct **C2 violation** if used as published.
The same recipe (weighted graph → community/shortest-path readout) is C1/C2-clean if the
correlation matrix is replaced by the ENM covariance Cov ∝ Γ⁻¹ or the ANM Hessian
inverse instead of an MD trajectory — which is exactly what Chennubhotla & Bahar (below)
and STRESS's interior module (below) do. Sethi 2009 itself is flagged unusable; the
graph-community idea it popularized is usable once decoupled from MD.

**Chennubhotla & Bahar 2007** [VERIFIED-ABSTRACT]. "Signal propagation in proteins and
relation to equilibrium fluctuations." _PLoS Comput Biol_ 3:1716–1726,
doi:10.1371/journal.pcbi.0030172 (`CHALLENGE.md` ref 8, the paper that motivates C6 in
the challenge text itself). Treats the GNM-derived residue network as a discrete-time
Markov chain and computes hit times and commute times between residue pairs — the
number of steps, on average, for a fluctuation to travel from one residue to another.
Functionally important residues have short hit times. Because hit/commute time is
naturally read from a fixed source residue to every other residue, this is
**source-conditioned by construction** and satisfies C1/C2/C6 exactly (built entirely
from the GNM Kirchhoff matrix, no MD, no training). No single top-N benchmark number
was retrieved this session; the paper is a mechanistic/case-study paper (case studies
included), not a benchmarked predictor — recorded as a negative result, not an omission.

**del Sol, Fujihashi, Amoros & Nussinov 2006** [VERIFIED-ABSTRACT]. "Residue centrality,
functionally important residues, and active site shape." _Protein Sci_ 15:2120–2128,
doi:10.1110/ps.062249106. Closeness centrality on the residue contact graph, tested
across 46 protein families (29 enzyme, 17 non-enzyme). Of the highest-centrality
residues, **80% overall**, **91% for enzyme families**, and **48% for non-enzyme
families** were the active site or in direct contact with it. This is the opposite
framing from ours (predicting the _active_ site from global centrality, not scoring
distal residues _relative to_ a known active site) but it is the founding result behind
using centrality as a functional-site signal, and it is the reason eigenvector
centrality is a mandatory control (conventions §6, ROADMAP Phase 2). Global scanner, no
active-site conditioning, no training.

**Bond-to-bond propensity — Amor, Schaub, Yaliraki & Barahona 2016**
[VERIFIED-ABSTRACT]. "Prediction of allosteric sites and mediating interactions through
bond-to-bond propensities." _Nat Commun_ 7:12477, doi:10.1038/ncomms12477. Builds an
energy-weighted atomistic graph (covalent + weak/non-covalent bonds) and computes how a
fluctuation at a defined **source** (typically the active site) propagates,
bond-by-bond, to every other bond in the structure — explicitly **source-conditioned**,
and explicitly framed by its authors as finding "communication pathways strongly coupled
to the active site... without prior information of their [distal-site] location." Case
studies on caspase-1, CheY and h-Ras; this is the method Ohm (below) benchmarks against
directly. Structure-only, no training, satisfies C1/C2/C6. Whether it needs full
all-atom (not Cα-only) topology was not independently re-verified this session.

**Ohm — Wang, Jain, McDonald, Gambogi, Lee & Dokholyan 2020** [VERIFIED-FULLTEXT].
"Mapping allosteric communications within individual proteins." _Nat Commun_ 11:3862,
doi:10.1038/s41467-020-17618-2. Network-based allosteric-coupling-index (ACI)
propagation on a single static structure — the authors state explicitly, "Unlike
previously developed simulation-based approaches, Ohm relies solely on the structure of
the protein of interest," and separately: **"If the position of the active site is
known, the perturbation propagation algorithm calculates ACIs of all residues relative
to the active site."** This is the cleanest example found this session of a classical
method that literally does what our pipeline is asked to do — **condition on a named
active site and score every other residue's dynamic connectivity to it** — without MD
and without training. On a 20-protein known-allosteric-protein test set: **TPR 0.57,
PPV 0.72** for Ohm vs. **TPR 0.23, PPV 0.48** for the bond-to-bond-propensity comparator
[VERIFIED-FULLTEXT] — a head-to-head win for the source-conditioned ENM/network
approach over the source-conditioned atomistic-graph approach, on the same set. A CheY
case study against NMR CHESCA data reaches 47.6% TPR on the top-20 predicted residue
pairs. Whether the 20-protein set used apo or holo input structures was not stated in
the retrieved text — **apo-only status: unconfirmed**, flagged rather than assumed.

**Current-flow (random-walk) betweenness centrality.** Introduced to protein allosteric
networks as an electrical-current analog of betweenness — it sums contributions from
_all_ paths between two nodes, weighted by conductance, not just the shortest path
[VERIFIED-ABSTRACT, bioRxiv 10.1101/259572]. Actively maintained today in **AlloViz**
(2024) [VERIFIED-ABSTRACT, https://pubmed.ncbi.nlm.nih.gov/38736696/], a tool that
computes current-flow betweenness (among other network metrics) on protein structures
for GPCRs and PTP1B case studies. Structure-based, source/target-conditioned when read
between two chosen nodes, no MD requirement if the edge weights come from ENM
correlation rather than MD correlation (as with dynamical network analysis, the MD vs.
ENM choice of edge weight is what decides C2 compliance, not the centrality metric
itself).

**Community detection (Girvan–Newman) on protein structure networks.** The general
method removes the highest-edge-betweenness edge iteratively and tracks the resulting
modularity-optimal partition [VERIFIED-ABSTRACT]. Applied to protein structure/dynamics
networks to find "modules" whose boundary residues mediate inter-module signaling —
e.g. "Modular architecture of protein structures and allosteric communications" (_Genome
Biol_ 2007;8:R92) [VERIFIED-ABSTRACT, title/venue only, authors not independently
confirmed this session]. This is the community-detection half of Sethi 2009's toolkit,
usable independently of the MD-derived edge weights that make Sethi's full pipeline
C2-non-compliant.

**STRESS — Clarke, Sethi, Li, Kumar, Chang, Chen & Gerstein 2016** [VERIFIED-ABSTRACT].
"Identifying Allosteric Hotspots with Dynamics: Application to Inter- and Intra-species
Conservation." _Structure_ 24:826–837, doi:10.1016/j.str.2016.03.019 (DOI pattern-matched
from the article's ScienceDirect PII, not independently confirmed by a direct DOI
resolver hit this session). Two independent modules: a **surface** module (Monte Carlo
ligand-probe simulation over the protein surface, following the "binding leverage"
concept of Mitternacht & Berezovsky 2011) and an **interior** module that represents the
structure as a network and identifies communication "bottleneck" residues, using **ANM
normal modes, not an MD trajectory**, to encode conformational change — i.e., this is a
structural descendant of Sethi's dynamical-network idea with the MD covariance replaced
by ENM covariance, which is exactly the substitution that makes it C1/C2-clean. No
isolated STRESS accuracy number was retrieved this session outside of its inclusion as
one of the eight tools in the AlloBench reappraisal (§7).

---

## 4. Allostery-specific predictors: training-free vs. secretly supervised

**PARS — Panjkovich & Daura 2014** [VERIFIED-ABSTRACT]. "PARS: a web server for the
prediction of Protein Allosteric and Regulatory Sites." _Bioinformatics_ 30:1314–1315,
https://academic.oup.com/bioinformatics/article/30/9/1314/235500. Combines a normal-mode
fluctuation/mobility score with structural-conservation-across-homologs scoring per
candidate pocket. No SVM, no fitted weights on a labeled allosteric-site set — the
conservation term needs a homolog alignment (an external database lookup, not a
trajectory and not training in the ML sense). Reasonably classed as training-free.
No independent apo-blind benchmark number was retrieved this session; PARS was
**excluded from the AlloBench (§7) re-evaluation** because its implementation is
reported unavailable/defunct — a negative result, not evidence it fails.

**AlloSite — Huang, Lu, Huang, Liu, Mou, Luo, Zhao, Liu, Chen, Hou & Zhang 2013**
[VERIFIED-ABSTRACT]. _Bioinformatics_ 29:2357–2359, doi:10.1093/bioinformatics/btt399.
**This is an SVM classifier trained on labeled pocket descriptors, not a training-free
physical computation** — it does not belong in a "no training needed" list despite
being commonly grouped with PARS and AlloPathFinder in review articles. Reports "~95%
accuracy" on its own test set [VERIFIED-ABSTRACT]; criterion, exact denominator and
whether the test set is apo or holo were not stated in the retrieved abstract-level
text. Included in the AlloBench and CAPASP re-evaluations (§7), where it does not
retain anything close to 95%.

**AlloPred — Greener & Sternberg 2015** [VERIFIED-ABSTRACT]. _BMC Bioinformatics_
16:335, doi:10.1186/s12859-015-0771-1. **Also an SVM**, trained with leave-one-out
cross-validation over a 79-protein training set (grid search over C and γ), combining
normal-mode perturbation features with Fpocket pocket descriptors. On 40 known
allosteric proteins: top-1 success **23/40 (57.5%)**, top-1-or-2 **28/40 (70%)**
[VERIFIED-ABSTRACT]. Flagged supervised, not training-free.

**AlloPathFinder — Tang, Liao, Dunn, Altman, Spudich & Schmidt 2007**
[VERIFIED-ABSTRACT]. "Predicting allosteric communication in myosin via a pathway of
conserved residues." _J Mol Biol_ 373:1361–1373, PMID 17900617,
https://pmc.ncbi.nlm.nih.gov/articles/PMC2128046/. Dijkstra shortest-path search on the
residue contact graph, with edge weights favoring high sequence conservation, **between
a given active site and a given allosteric/regulatory site**. **This needs both
endpoints as input.** It explains or validates a pathway between two already-known
sites; it is not a tool for discovering an unknown distal site from the active site
alone, which is the task this project has. Not usable as a blind site predictor;
usable, in principle, only after a candidate site is already proposed by another
method — out of scope as a primary baseline.

**SPACER — Goncearenco, Mitternacht, Yin, Bhaskara, Rezende, Palmberg, Trellet, Reed &
Berezovsky 2013** [VERIFIED-ABSTRACT, author list from the retrieved journal page not
independently cross-checked in full]. "SPACER: server for predicting allosteric
communication and effects of regulation." _Nucleic Acids Res_ 41:W266–W272,
doi:10.1093/nar/gkt460. Structure-based statistical-mechanical model (the precursor to
Guarnera & Berezovsky's 2016 SBSMMA, _PLoS Comput Biol_ 12:e1004678,
doi:10.1371/journal.pcbi.1004678, which formalizes the causal, per-residue free-energy
version of the same idea). Computes the mean work exerted on each residue by ligand
binding at a defined site, from ENM normal modes of the bound vs. unbound system —
structure-only, no training, and explicitly source-conditioned (the ligand/binding site
is the perturbation origin). Satisfies C1/C2/C6. No top-N hit-rate number against a
labeled allosteric-site benchmark was retrieved this session for SPACER itself; STRESS
(§3) is its closer structural relative that does appear in a benchmark (§7).

**Contrast — supervised/ML methods named only because the reappraisals in §7 test
them.** PASSer / PASSer2.0 (AutoML/ensemble, _Mach Learn Sci Technol_ 2021,
doi:10.1088/2632-2153/abe6d6), AllositePro, and STINGAllo (2025, 54 hand-engineered
"nanoenvironment" descriptors into a residue-level ML model, _Brief Bioinform_,
doi:10.1093/bib/bbaf424, reporting ~78% success vs. 21–24% for "contemporary
pocket-based predictors" on its own benchmark [VERIFIED-ABSTRACT]) are all trained
predictors. None is training-free; none is evaluated here as a candidate. They appear
only in §7 because the field's own reappraisals test them alongside the unsupervised
methods this file is actually about, and the gap between their in-paper numbers and
their reappraised numbers is part of the evidence for §8(c).

---

## 5. Pocket-geometry detectors used as the ranking substrate

These do not themselves output an "allosteric" label — they find and score candidate
cavities, which several methods above (APOP, AlloPred, PARS) then re-rank with a
dynamics term, and which our own frozen evaluation layer uses for the `cavity_volume`
control and decoy set (conventions §5–§6; not re-derived here, only connected).

- **fpocket — Le Guilloux, Schmidtke & Tuffery 2009** [VERIFIED-ABSTRACT]. _BMC
  Bioinformatics_ 10:168, doi:10.1186/1471-2105-10-168. Voronoi tessellation + alpha
  spheres. Open source, C, no training. The pocket detector APOP itself uses.
- **pyKVFinder — Guerra, Ribeiro-Filho, Jara, Bortot, Pereira & Lopes-de-Oliveira 2021**
  [VERIFIED-ABSTRACT]. _BMC Bioinformatics_ 22:607, doi:10.1186/s12859-021-04519-4.
  Grid-based cavity detection (volume, area, depth, hydropathy). This is the detector
  version and configuration our own frozen evaluation layer pins for the decoy set
  (conventions §5, ADR 0024 — value not re-opened here).
- **CASTp 3.0 — Tian, Chen, Chan, Golemis & Wu 2018** [VERIFIED-ABSTRACT]. _Nucleic
  Acids Res_ 46:W363–W367, doi:10.1093/nar/gky473. Alpha-shape-based pocket/cavity/
  channel atlas, web-server oriented.
- **P2Rank — Krivák & Hoksza 2018** [VERIFIED-ABSTRACT]. _J Cheminform_ 10:39,
  doi:10.1186/s13321-018-0285-8. ML-trained (random forest on local chemical/geometric
  descriptors per solvent-exposed point), so out of the training-free scope by itself,
  but its **evaluation-methodology argument matters directly to us**: a
  pocket-centric method that correctly finds a pocket is still penalized under a
  naive residue-level AUC/classification metric, because every residue near — but not
  part of — the correctly identified pocket counts as a false positive under
  residue-level scoring even when the pocket-level prediction is exactly right
  [VERIFIED-ABSTRACT]. A 2024 independent comparative-evaluation paper restates the
  same tension explicitly: pocket-level metrics (DCC/top-N) "don't reward excessive
  overprediction," while residue-level AUC "treats all false positives equally
  regardless of whether they contribute to successful pocket detection" (_J
  Cheminform_ 2024, doi:10.1186/s13321-024-00923-z; full text paywalled this session,
  claim sourced from the retrieved abstract/summary) [VERIFIED-ABSTRACT]. This is the
  "P2Rank's argument against residue-level AUC" named in the task brief — relevant to
  how our own residue-ranked hit list should be read, not a reason to alter the frozen
  evaluation harness.

---

## 6. Statistical-mechanics routes that need no trajectory

**COREX/BEST — Hilser & Freire 1996** [VERIFIED-ABSTRACT]. "Structure-based calculation
of the equilibrium folding pathway of proteins. Correlation with hydrogen exchange
protection factors." _J Mol Biol_ 262:756–772, doi:10.1006/jmbi.1996.0550. Enumerates a
combinatorial set of partially-folded microstates from one static structure and
Boltzmann-weights them with a parameterized (but not ML-trained; physically
parameterized from surface-area/entropy terms) energy function, giving a per-residue
stability constant without any conformational-ensemble simulation. This is the
computational engine behind "the ensemble nature of allostery" (`CHALLENGE.md` ref 4,
Motlagh, Wrabl, Li & Hilser 2014, _Nature_ 508:331–339, already in the challenge's own
bibliography — not re-verified here). Structure-only, no MD, no training. No top-N
allosteric-site hit-rate number against a labeled benchmark was retrieved this session
— COREX/BEST is used for regional-stability and cooperativity case studies, not as a
site-ranking predictor with a published leaderboard entry. Negative result, recorded.

**Elastic/energetic frustration — Ferreiro, Hegler, Komives & Wolynes 2007 and 2011**
[VERIFIED-ABSTRACT]. "Localizing frustration in native proteins and protein
assemblies." _PNAS_ 104:19819–19824, doi:10.1073/pnas.0709915104. "On the role of
frustration in the energy landscapes of allosteric proteins." _PNAS_ 108:3499–3503,
doi:10.1073/pnas.1018980108. Scores each native contact by how favorable it is relative
to the ensemble of possible sequence/register substitutions at that geometry ("locally
frustrated" contacts are close to marginal). The 2011 paper's finding: regions that
undergo conformational change during allosteric transitions are enriched in highly
frustrated contacts, consistent with these regions acting as hinges. Structure-only
(needs a contact map and a substitution/decoy statistic, computable from sequence +
structure, no MD, no training data beyond a standard statistical potential). No top-N
hit-rate number against a labeled allosteric-site benchmark was retrieved this session —
frustration is used as a mechanistic/explanatory signal (where hinges are), not as a
benchmarked site-ranking predictor. Negative result, recorded.

---

## 7. The field's own reappraisals — what they actually report

**AlloBench — Maity & Qiao 2025** [VERIFIED-FULLTEXT]. "AlloBench: A Data Set Pipeline
for the Development and Benchmarking of Allosteric Site Prediction Tools." _ACS Omega_
10:17973–17982, doi:10.1021/acsomega.5c01263. Builds a 2141-allosteric-site,
2034-structure, 418-unique-chain pipeline from ASD/ASBench/CASBench sources, then
removes every protein sharing a UniRef50 cluster with any protein in the training sets
of the tools it re-tests, leaving **100 leakage-controlled test proteins**. Re-evaluates
**eight tools**: PASSer (Ensemble, AutoML and Rank variants), APOP, ALLO, AlloPred,
AlloSite, AllositePro, STRESS and Ohm, by Jaccard Index (JI) of predicted vs. known
allosteric-site residues, top-1 prediction only. Headline finding, quoted exactly:
**"None of these programs could achieve an accuracy of more than 60%, even with a very
low JI cutoff of approximately zero."** At the stricter JI > 0.5 threshold: PASSer
(Ensemble) 18%, APOP 15%, PASSer (AutoML) 13% [VERIFIED-FULLTEXT]. PARS and ESSA were
**excluded** for unavailable/defunct implementations — negative result, not evidence of
failure. The paper also reports a **strong correlation between JI and the inverse
distance** from the predicted centroid to the known site's centroid, i.e., success on
this benchmark is substantially explained by proximity to the true site
[VERIFIED-FULLTEXT] — independent, convergent evidence for the same proximity confound
our own repo already diagnosed (conventions §5, `ctrl_closeness` at AUC 0.617).

**CAPASP — 2026** [VERIFIED-ABSTRACT; full text behind a Springer login wall this
session]. "A systematic evaluation of protein allosteric site prediction tools with
independent datasets." _J Comput Aided Mol Des_, doi:10.1007/s10822-026-00831-4.
Builds two **independent** datasets: **CAPASP-General** (holo-state allosteric
proteins) and **CAPASP-Unbound** (apo-state allosteric proteins), and scores five
tools (only two resolved from the retrieved abstract/snippets: **PASSer and APOP**) on
sensitivity, specificity, F1, MCC and ranking. Finding, as retrieved: PASSer and APOP
"achieved the highest success rate in sensitivity prediction and also lead in average
F1-score and MCC value," but **"these models performed better with the CAPASP-General
subset than with the CAPASP-Unbound subset"** [VERIFIED-ABSTRACT] — i.e., the two
best-performing classical/ML-hybrid tools both degrade when the input is switched from
holo to apo, which is exactly the setting `CHALLENGE.md` mandates. Exact numeric
sensitivity/F1/MCC values for the apo vs. holo split were **not retrieved this
session** (paywalled) — recorded as a gap, not filled with a recalled number.

**AlloDyn — Pryakhin, Smail-Tabbone & Karami 2026** [VERIFIED-FULLTEXT]. "Benchmark
Bias and Conformational Dynamics in Allosteric Site Prediction." bioRxiv,
doi:10.64898/2026.05.22.727284. Re-evaluates APOP, PASSer (ensemble/AutoML/ranking
variants), AllosES and fpocket on existing benchmarks (D24, ASD2023), and shows that
"models trained on the biased dataset achieve substantially higher F1 scores than those
trained on the unbiased dataset" [VERIFIED-FULLTEXT] — exact before/after percentages
were not resolved from the fetched summary this session (gap recorded, not filled).
AlloDyn is the name of the **method** the paper introduces (a static+dynamic feature
fusion framework), not a new benchmark dataset — a correction to how the task brief
names it. The paper does not report a comparison of classical methods against a
simple distance-to-modulator control [VERIFIED-FULLTEXT] — see §8(d).

---

## 8. The four questions

**(a) Strongest MD-free, training-free, apo-only classical result as of 2026, with its
number and criterion.** On the original publication's own terms, it is **APOP's
apo-restricted top-3 success of 11/15 (73%), reported elsewhere in the same paper as
86% (11/14)**, on a matched apo/holo allosteric-pocket subset largely drawn from ESSA's
own dataset (Bioinformatics 2023, doi:10.1093/bioinformatics/btad275) — higher than
ESSA's own 7/14 (50%) on essentially the same comparison, using a similar unsupervised
GNM-plus-pocket-perturbation recipe. **This number does not survive the field's own
2025–2026 reappraisal.** AlloBench's larger, leakage-controlled re-test puts APOP at
15% at JI > 0.5 and states flatly that no tool clears 60% even at a near-zero JI cutoff
(doi:10.1021/acsomega.5c01263). CAPASP's independent apo-vs-holo split finds APOP (with
PASSer) specifically **degrades** on apo (CAPASP-Unbound) relative to holo
(CAPASP-General) input (doi:10.1007/s10822-026-00831-4). The honest answer is:
**the field's original best apo number (APOP, ~73–86% on N=14–15) is real but built on
a small, non-leakage-controlled set; the field's 2025–2026 rigorous, larger-N,
leakage-and-apo-controlled bar is under 60% and falls further on apo input** — which is
consistent with, and now more specific than, conventions §6's "no tool exceeded 60%
accuracy even at a very low Jaccard cutoff."

**(b) Which classical methods condition on a named active site, as ours must, rather
than scoring the graph globally?** A small set, and it is exactly the set that shares
our pipeline's task shape: **PRS** (read one row/column of its N×N response matrix),
**Chennubhotla & Bahar's Markov hit/commute times** (fixed source, all-residue readout),
**bond-to-bond propensity** (explicitly source-conditioned on the active site), and
**Ohm** (explicitly: "calculates ACIs of all residues relative to the active site," and
the only one of these four with a head-to-head published number against another
source-conditioned method — Ohm's TPR 0.57/PPV 0.72 vs. bond-to-bond propensity's TPR
0.23/PPV 0.48 on the same 20-protein set). AlloPathFinder also conditions on a source
but needs the _target_ too, which makes it a pathway explainer, not a site predictor.
Dynamical network analysis (Sethi 2009) and its descendants condition on a source/target
pair as well, but the original MD-covariance formulation is C2-non-compliant. Everything
else surveyed here — GNM/ANM raw fluctuations, ESSA, APOP, PARS, AlloSite, AlloPred,
fpocket/pyKVFinder/CASTp, COREX/BEST, frustration — is a **global scanner** with no
active-site input at all. This four-method set (PRS, Chennubhotla–Bahar, bond-to-bond
propensity, Ohm) is the right comparison class for a source-conditioned quantum walk,
not the global scanners the field usually benchmarks against each other.

**(c) The field's own reappraisals.** Covered in full in §7. Net effect: AlloBench
deflates every retested tool below 60% (most far below) on a leakage-controlled set;
CAPASP shows the two strongest tools (PASSer, APOP) specifically weaken on apo relative
to holo input, which is the exact axis `CHALLENGE.md` scores on; AlloDyn shows F1 is
"substantially higher" on the biased version of a benchmark than the debiased version,
without giving this session a resolved before/after number. All three converge on the
same conclusion conventions §6 already states in different words: **published leaderboard
numbers for this task are inflated, and the deflation is large enough to change which
method looks best.**

**(d) Is there a published classical method that beats a plain distance-to-active-site
control under a proximity-matched or distance-stratified evaluation?** **Not retrieved
by the recorded search this session.** None of the three reappraisals runs that specific
analysis; AlloBench comes closest, and what it finds points the other way — a **strong
correlation between its own JI success metric and inverse distance to the true site**,
meaning success on the published benchmark is substantially explained by proximity, not
mechanism. That is convergent, independent evidence for the same confound our own repo
already measured (`ctrl_closeness` = AUC 0.617). Per ADR 0019, this is reported as
"not retrieved," not as "does not exist" — the search was not exhaustive over every
2020–2026 allostery paper, only over the routes in conventions §3.

---

## 9. Comparison table — every quoted metric, with dataset and criterion

| Method                                                         | Year | Dataset (N)                                             | Input                             | Criterion                                         | Number                                                                                      | Active-site-conditioned?                   | Source                             |
| -------------------------------------------------------------- | ---- | ------------------------------------------------------- | --------------------------------- | ------------------------------------------------- | ------------------------------------------------------------------------------------------- | ------------------------------------------ | ---------------------------------- |
| APOP                                                           | 2023 | 104 proteins (61 mono + 43 multi), pooled apo+holo      | apo-equivalent (ligand stripped)  | top-3 pocket rank                                 | 92/104 = 88.5%                                                                              | No (global)                                | doi:10.1093/bioinformatics/btad275 |
| APOP                                                           | 2023 | 50-structure holo subset                                | holo                              | top-3                                             | 42/50 = 84% (vs. AlloPred 68%, PASSer 76%)                                                  | No                                         | same                               |
| APOP                                                           | 2023 | matched apo/holo subset, ~14–15 pairs                   | apo vs. holo                      | top-3                                             | apo 11/15=73% (also stated 86%=11/14); holo 15/15=100%                                      | No                                         | same                               |
| ESSA                                                           | 2020 | Dataset II, 14 matched pairs (12 proteins)              | apo vs. holo                      | top-3                                             | apo 7/14=50%; holo 10/14≈71%                                                                | No                                         | doi:10.1016/j.csbj.2020.06.020     |
| AlloPred (SVM)                                                 | 2015 | 40 known allosteric proteins                            | not stated                        | top-1 / top-1-or-2                                | 23/40=57.5% / 28/40=70%                                                                     | No                                         | doi:10.1186/s12859-015-0771-1      |
| AlloSite (SVM)                                                 | 2013 | undisclosed test set                                    | not stated                        | "accuracy"                                        | ~95%                                                                                        | No                                         | doi:10.1093/bioinformatics/btt399  |
| Ohm                                                            | 2020 | 20 known allosteric proteins                            | not stated (unconfirmed apo/holo) | TPR / PPV vs. bond-to-bond-propensity comparator  | Ohm TPR 0.57, PPV 0.72; comparator TPR 0.23, PPV 0.48                                       | **Yes**                                    | doi:10.1038/s41467-020-17618-2     |
| Ohm (CheY case)                                                | 2020 | 1 protein, NMR CHESCA                                   | not stated                        | top-20 residue pairs, TPR                         | 47.6%                                                                                       | Yes                                        | same                               |
| del Sol closeness centrality                                   | 2006 | 46 families (29 enzyme, 17 non-enzyme)                  | holo/family-based                 | % top-centrality residues at/adjacent active site | 80% overall; 91% enzyme; 48% non-enzyme                                                     | No (predicts active site, not distal site) | doi:10.1110/ps.062249106           |
| STINGAllo (ML, contrast)                                       | 2025 | its own benchmark                                       | not stated                        | success rate                                      | ~78% (vs. 21–24% pocket-based baselines; 60.2% overall claim)                               | No                                         | doi:10.1093/bib/bbaf424            |
| AlloBench reappraisal                                          | 2025 | 100 leakage-controlled proteins, 8 tools                | mixed                             | JI ≈ 0 cutoff; JI > 0.5                           | all tools <60% at JI≈0; at JI>0.5: PASSer-Ens 18%, APOP 15%, PASSer-AutoML 13%              | n/a (evaluation study)                     | doi:10.1021/acsomega.5c01263       |
| CAPASP reappraisal                                             | 2026 | CAPASP-General (holo) vs. CAPASP-Unbound (apo), 5 tools | apo vs. holo, split               | sensitivity/F1/MCC                                | PASSer & APOP lead both, both degrade apo vs. holo (exact values not retrieved — paywalled) | n/a                                        | doi:10.1007/s10822-026-00831-4     |
| AlloDyn reappraisal                                            | 2026 | D24 / ASD2023                                           | mixed                             | F1, biased vs. unbiased dataset                   | biased-dataset F1 "substantially higher" (exact values not retrieved)                       | n/a                                        | doi:10.64898/2026.05.22.727284     |
| `ctrl_closeness` (this repo, cross-referenced, not re-derived) | —    | 73 curated targets                                      | apo                               | AUC                                               | 0.617                                                                                       | Yes (by definition)                        | conventions §5 (internal)          |

---

## What this changes for our pipeline

- **Phase 1.4 (classical baselines) should add PRS and Chennubhotla–Bahar hit/commute
  time as explicit active-site-conditioned baselines**, alongside the GNM/ANM/APOP/
  distance/degree/eigenvector-centrality controls already planned. They are the closest
  published classical analogs to a source-conditioned CTQW (§8b) and are currently
  absent from the roadmap's Phase 1.4 list. Ohm's published numbers (TPR 0.57/PPV 0.72
  vs. bond-to-bond propensity's 0.23/0.48, doi:10.1038/s41467-020-17618-2) give a
  concrete external number to reproduce or beat if Ohm-style ACI propagation is
  implemented as a control.
- **Two published methods are structurally unusable as blind apo-only baselines and
  should not be budgeted:** two-state ANM/PATH (Das 2014, needs a second known
  conformer — C1 risk) and AlloPathFinder (Tang 2007, needs the allosteric site as an
  input, not an output). Recorded here so no future phase spends effort implementing
  either as a predictor.
- **Any classical dynamical-network-analysis baseline must use ENM covariance, never
  MD covariance**, to stay C2-compliant — Sethi 2009's original formulation is
  MD-derived and is flagged unusable as published; Chennubhotla–Bahar and STRESS's
  interior module show the ENM-covariance substitution is already established practice
  in the literature.
- **The report's "bar to beat" language (Phase 5, `docs/report/`) should cite
  AlloBench's <60%-at-JI≈0 ceiling and CAPASP's apo-degradation finding, not APOP's
  original 73–88.5% headline numbers**, when characterizing the classical state of the
  art. This file adds a specific, sourced mechanism (small N, apparent apo/holo dataset
  overlap with the source paper's own development set, no leakage control) to the
  general caution conventions §6 already states, and adds a second, apo-specific
  deflation axis (CAPASP) that was not previously in evidence.
- **No published classical method is known, from this session's search, to beat
  `−distance` under a distance-stratified or proximity-matched control (§8d).**
  AlloBench's own JI-vs-inverse-distance correlation is convergent external evidence
  for the same proximity confound already measured in this repo. This supports keeping
  the conventions §6 four-number bar as the target rather than any single external
  leaderboard number.
- **P2Rank's residue-vs-pocket-level AUC argument (§5) is relevant context for the
  methodological report's limitations section** when discussing how the residue-ranked
  hit list should be read — it does not imply any change to the frozen Phase 1.6
  evaluation harness, which this file did not open and does not question.

---

## Method

**Databases hit:** general web search (primary route this session), Europe PMC REST
search API (one query, for the AlloDyn/benchmark-bias preprint), PMC, Oxford Academic
(Bioinformatics, NAR), BioMed Central (BMC Bioinformatics, J Cheminform), PLOS Comput
Biol, Nature Communications, PNAS, Cell Press (Structure, Biophysical Journal), ACS
Omega, bioRxiv, arXiv (indirectly, via search snippets only — no arXiv API query was
needed since no candidate method in scope for this file was arXiv-only). Semantic
Scholar was not queried (conventions §3: rate-limited).

**Representative queries run:** Tirion 1996 PRL; Bahar/Atilgan/Erman 1997 GNM; Atilgan
2001 ANM; Atilgan & Atilgan 2009 PRS; ESSA essential site scanning; APOP allosteric
pocket prediction; Sethi 2009 dynamical networks; Amor/Barahona bond-to-bond
propensity; PARS Panjkovich Daura; AlloSite Huang; AlloPred BMC Bioinformatics SVM;
AlloPathFinder Tang myosin; SPACER Berezovsky; Ohm Dokholyan Nature Communications;
STRESS Gerstein Clarke; del Sol 2006 residue centrality; COREX BEST Hilser Freire;
Ferreiro Wolynes localizing frustration; fpocket Le Guilloux; pyKVFinder Guerra; CASTp
Tian 2018; P2Rank residue-level AUC criticism; AlloBench 2025 ACS Omega leakage; CAPASP
2026 JCAMD; AlloDyn/benchmark-bias bioRxiv 2026; distance-to-active-site proximity bias
allosteric benchmark; current-flow betweenness protein allostery; Girvan-Newman
community detection protein network allostery; Zheng 2023 coarse-grained normal modes;
Chennubhotla Bahar 2007 Markov propagation; Das 2014 two-state ANM. Roughly 35 distinct
queries, ~10 targeted WebFetch full-text/abstract retrievals.

**Counts:** ~33 distinct methods/tools screened in with at least one full-text- or
abstract-verified claim; 3 field reappraisals fully screened; 2 candidate methods
(two-state ANM/PATH, AlloPathFinder) screened in specifically to be flagged as
structurally unusable, not as candidates.

**Stopping rule:** stopped once every method category listed in the assignment brief
had at least one sourced, dated entry with a DOI/URL retrieved this session, and all
four named questions (§8) had either a direct sourced answer or a documented negative
result satisfying ADR 0019's wording.

**Could not be reached this session:** CAPASP full text (Springer login redirect;
abstract/snippet-level claims only, flagged); P2Rank J Cheminform 2018 full-text PDF
(Springer login redirect; claim sourced from search-snippet paraphrase instead); Ohm
paper via nature.com directly (login redirect; recovered via its PMC mirror,
PMC7395124); GNM's original 1997 Folding & Design text (pre-open-access era; title,
journal, volume/page and DOI confirmed via secondary sources, content description is a
standard/uncontested characterization of GNM, not an independently fetched quote);
exact numeric CAPASP-General vs. CAPASP-Unbound sensitivity/F1/MCC values (paywalled);
exact before/after F1 values in AlloDyn's bias analysis (summarized by the fetch tool
without the underlying table); a primary citation independently confirming the full
author list of the Genome Biology 2007 community-detection paper.
