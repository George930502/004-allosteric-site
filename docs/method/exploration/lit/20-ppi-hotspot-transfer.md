# PPI Hot-Spot and Interface Science, Mined for Transfer

**Scope:** protein–protein interaction hot-spot theory, prediction and energetics, screened for what
transfers to "rank residues by dynamic connectivity to a named active site, from one apo structure."
Covers O-ring/hot-region theory, computational alanine scanning, the hot-spot prediction servers,
the interface-to-allostery mechanism literature, and every retrieved method that ranks residues by
**coupling to a second site** rather than by an intrinsic local property. Deliberately excludes:
interface-_site_ predictors that output a binding-surface probability without an energetic hot-spot
claim (ScanNet, MaSIF, PeSTo — file `review/05`), MD-free ensemble generation (`review/05` §3),
effective resistance and network-controllability (`review/05` §7), and the classical
allosteric-site predictor lineage itself (`review/01`).
**Sibling files:** `review/00-conventions.md` (the rules this file obeys),
`review/01-classical-baselines.md` (ENM lineage, Ohm's benchmark numbers, the field's reappraisals),
`review/05-adjacent-task-transfer.md` (interface-site deep learning, FTMap as a druggability probe,
DCA/SCA as an epistasis channel, effective resistance).
**Retrieved:** 2026-08-26.

---

## 1. Why this literature and not another

PPI hot-spot science is the only mature field that has spent thirty years answering a question with
our exact grammar: _given a structure and a named functional region, which residues carry the
energetic load?_ It has an experimental ground truth (alanine scanning), a curated database lineage
(ASEdb, BID, SKEMPI), a theory (O-ring, hot regions), and — crucially — a documented record of what
happens when its predictors meet a distribution they were not trained on. That record is the most
useful thing in it for us, and it is mostly negative.

Two structural facts organise everything below.

**Fact one: nearly every hot-spot predictor needs the complex.** A hot spot is defined by a ΔΔG of
binding, which requires two partners. For us the second partner is the holo-equivalent object. A
method that takes the complex as input is C1-forbidden in exactly the way a holo pocket definition
is. The exceptions are few and are named individually in §3.

**Fact two: the field's own transfer tests fail hard.** Section §6 collects four independent
instances where hot-spot or pathway machinery was moved off its training distribution and lost most
of its signal. None of these numbers is recalled; each has a DOI retrieved this session.

---

## 2. The theory: O-rings, hot regions, and what survives without the partner

**Bogan & Thorn 1998** [VERIFIED-ABSTRACT]. "Anatomy of hot spots in protein interfaces." _J Mol
Biol_ 280:1–9, doi:10.1006/jmbi.1998.1843, PMID 9653027. Analysis of **2,325 alanine mutants**.
Binding free energy is not spread over the interface; it concentrates in a small residue subset
enriched in **tryptophan, tyrosine and arginine**. The retrieved record states "there is little
correlation between buried surface area and free energy of binding" at the side-chain level, and
that hot spots are ringed by energetically unimportant residues that occlude solvent. The O-ring is
therefore a **geometric occlusion claim about the residue's neighbourhood**, and occlusion is
computable from a monomer.

_Verdict — C1 CONDITIONAL, C2 PASS, C6 CONDITIONAL._ The theory is a claim about interfaces, so the
ΔΔG it explains is a two-body quantity we cannot measure without the partner. What ports is the
occlusion geometry, which is monomer-computable. It is a packing statement, not a topology-driven
propagation statement, so C6 holds only in the weak sense that packing density is a contact-graph
degree.

**Keskin, Ma & Nussinov 2005** [VERIFIED-ABSTRACT]. "Hot regions in protein-protein interactions:
the organization and contribution of structurally conserved hot spot residues." _J Mol Biol_
345:1281–1294, doi:10.1016/j.jmb.2004.10.077, PMID 15644221. Structurally conserved interface
residues "correlate with the experimental alanine-scanning hot spots." Hot spots do not distribute
uniformly — they **cluster into densely packed hot regions**, and the retrieved record states that
within a cluster the contributions to stability are **cooperative**, while **separate clusters
contribute additively**.

This is the single most portable idea in the theory section, and it is portable because it is a
statement about the _score's spatial structure_, not about binding. If the functional signal is
carried by clusters, a per-residue ranker that treats residues independently is throwing away the
clustering. See §7 item 4.

**Keskin, Ma, Rogale, Gunasekaran & Nussinov 2005** [VERIFIED-ABSTRACT]. "Protein-protein
interactions: organization, cooperativity and mapping in a bottom-up Systems Biology approach."
_Phys Biol_ 2:S24, doi:10.1088/1478-3975/2/2/S03, PMID 16204846. States that hot spots "cluster
within densely packed 'hot regions'" forming cooperative networks, and — the C1-relevant part —
that the conserved residues are "**pre-organized**" in the **unbound** state.

**Rajamani, Thiel, Vajda & Camacho 2004** [VERIFIED-ABSTRACT]. "Anchor residues in protein-protein
interactions." _PNAS_ 101:11287–11292, doi:10.1073/pnas.0401942101, PMID 15269345. Across **39
protein complexes**, anchor side chains "are found in conformations similar to those observed in
the bound complex" without their partners present. This is the mechanistic licence for the whole
"predict from the unbound structure" programme: the binding-competent geometry is already in the
apo structure.

_Verdict for both pre-organisation results — C1 PASS, C2 PASS, C6 FAIL._ They justify apo-only
input. They say nothing about propagation, so they are a licence, not a method.

**Li & Liu 2009** [VERIFIED-ABSTRACT]. "'Double water exclusion': a hypothesis refining the O-ring
theory for the hot spots at protein interfaces." _Bioinformatics_ 25:743–750,
doi:10.1093/bioinformatics/btp058, PMID 19179356, PMCID PMC2654803. Sharpens O-ring: the hot region
is not merely solvent-shielded but internally **water-free**. Identified **1,293 non-redundant
biclique patterns** in PDB structures, checked against HotSprint and ASEdb.

_Verdict — C1 FAIL as published (bicliques are computed across the interface of a complex), C2 PASS,
C6 FAIL._

---

## 3. Prediction from a structure: what each method eats and what it emits

Ordered by how much of the complex the method needs. This is the C1 axis.

### 3a. Needs the complex — C1 FAIL for us

**HotPoint — Tuncbag, Keskin & Gursoy 2010** [VERIFIED-FULLTEXT]. _Nucleic Acids Res_ 38:W402–W406,
doi:10.1093/nar/gkq323, PMCID PMC2896123. The retrieved text is explicit: "The input to the HotPoint
server is a protein complex and two chain identifiers that form an interface," and "Server does not
work for PDB files containing only one chain and returns an error." The rule is two thresholds:
"If an individual interface residue is buried (its relative ASA **in complex state** is ≤20%) and
its total contact potential is **≥18.0**, this residue is flagged as a hot spot." Reported
**accuracy 0.70, precision 0.73, recall 0.59, specificity 0.79** on an independent test set of
**112 residues (54 hot spots, 58 non-hot spots)** from the Binding Interface Database. No MD
anywhere; the pair potentials are knowledge-based.

_Verdict — C1 FAIL (relative ASA is measured in the complex state; a monomer rASA is a different
number and the published threshold does not carry over), C2 PASS, C6 FAIL._ Output: a binary
per-residue label, not a score.

**KFC2 — Zhu & Mitchell 2011** [VERIFIED-ABSTRACT]. _Proteins_ 79:2671–2683, doi:10.1002/prot.23094,
PMID 21735484. Two SVMs (KFC2a, KFC2b) on **eight features** dominated by solvent accessibility and
local plasticity. **KFC2a TPR = 0.85** on the paper's balanced set.
_Verdict — C1 FAIL (interface solvation features), C2 PASS, C6 FAIL._

**SpotOn — Moreira, Koukos, Melo et al. 2017** [VERIFIED-ABSTRACT]. _Sci Rep_ 7:8007,
doi:10.1038/s41598-017-08321-2, PMCID PMC5556074. Ensemble ML on 3D-structure and sequence features
from **53 protein complexes**; reported **accuracy 0.95, sensitivity 0.98** on an independent test
set. Classifies interfacial residues as Hot-Spot or Null-Spot — i.e. it presupposes the interface.
_Verdict — C1 FAIL, C2 PASS, C6 FAIL._ Note the 0.95/0.98 against SPOTONE's fate in §6.

**HotRegion — Cukuroglu, Gursoy & Keskin 2012** [VERIFIED-ABSTRACT]. _Nucleic Acids Res_
40:D829–D833, doi:10.1093/nar/gkr929, PMCID PMC3245113. A database of predicted hot-spot _clusters_
with pair potentials, ASA, and the interactions among hot-spot residues. Useful only as an external
label source; it is derived from complexes.
_Verdict — C1 FAIL._

**DSSA-PPI 2026** [VERIFIED-ABSTRACT]. _Chem Sci_, doi:10.1039/d5sc08898d, PMCID PMC12758018.
PPIFormer + ESM-2, equivariant GNN, trained on SKEMPI v2 for ΔΔG-of-binding upon mutation. Needs the
bound complex.
_Verdict — C1 FAIL, C2 PASS (SKEMPI is experimental, not MD), C6 FAIL._

### 3b. Sequence only — C1 vacuously PASS, but see §6

**SPOTONE — Preto & Moreira 2020** [VERIFIED-ABSTRACT]. _Int J Mol Sci_ 21:7281,
doi:10.3390/ijms21197281, PMCID PMC7582262. "Only requiring the user to submit a FASTA file with one
or more protein sequences." Reported **accuracy 0.82, AUROC 0.83, precision 0.91, recall 0.82,
F1 0.85** on its own independent test set.
_Verdict — C1 PASS (a sequence carries no conformational state, so it cannot leak apo-vs-holo), C2
PASS, C6 FAIL (no topology at all)._ Its measured collapse is in §6.

**Embed-1dCNN — Zhang, Yao & Chen 2023** [VERIFIED-ABSTRACT]. _PLoS One_ 18:e0290899,
doi:10.1371/journal.pone.0290899, PMCID PMC10506709. Pre-trained sequence embedding + 1D CNN. Merged
ASEdb, BID, SKEMPI and dbMPIKT, and used SMOTE to expand the minority class; the retrieved
assessment records F1 = 0.82 with **no external validation**.
_Verdict — C1 PASS, C2 PASS, C6 FAIL. Not usable as evidence at that F1._

**Higa & Tozzi 2009** [VERIFIED-ABSTRACT]. _Genet Mol Biol_ 32:626–633,
doi:10.1590/s1415-47572009000300029, PMCID PMC3036045. Structural + evolutionary parameters,
**F-measure 60.4%**, and the retrieved record states this was achieved "without requiring complex
structure information." An early and honest calibration of what the single-structure ceiling looks
like.
_Verdict — C1 PASS, C2 PASS, C6 FAIL._

### 3c. Free (unbound) structure only — the C1-legal cases

**PPI-HotspotID — Chen, Sargsyan, Wright, Chen, Huang & Lim 2024** [VERIFIED-FULLTEXT]. _eLife_
13:RP96643, doi:10.7554/eLife.96643, PMCID PMC11405013. **This is the reference point for our
constraint set.** It takes "the free protein structure," runs "a conjugate gradients minimization
with constraints on the heavy atoms," and computes per-residue MM-PBSA energies. **No MD.** The
final model uses exactly four features, in importance order: **conservation score, residue type,
SASA, and ΔG_gas**.

Numbers, all from the fetched full text:

| Set                                   | N                                                           | Sens | Prec | Spec | F1               |
| ------------------------------------- | ----------------------------------------------------------- | ---- | ---- | ---- | ---------------- |
| PPI-Hotspot+PDB^BM(1.1)               | 158 nonredundant proteins; 414 hot spots, 504 non-hot spots | 0.67 | 0.76 | 0.83 | 0.71 (val. 0.66) |
| 48 complexes with unsolved structures | 90 hot spots, 45 non-hot spots                              | 0.58 | 0.77 | —    | 0.66             |

_Verdict — C1 PASS (free structure only; the AlphaFold-Multimer interface residues are an optional
add-on and would be the C1-questionable part if used), C2 PASS (minimisation is not a trajectory and
no MD-trained weights enter), C6 FAIL (energetics and conservation, not contact topology)._

**Sargsyan & Lim 2024** [VERIFIED-ABSTRACT]. "Using protein language models for protein interaction
hot spot prediction with limited data." _BMC Bioinformatics_ 25:115,
doi:10.1186/s12859-024-05737-2, PMCID PMC10943781. ESM-2 representations replacing the
structure-derived features on the same 414/504 set. Competitive with the structure-based features.
_Verdict — C1 PASS, C2 PASS, C6 FAIL._ Relevant chiefly because conventions §5 already records that
protein language models collapse on allosteric sites (AUPR 0.06). A PLM feature that works for PPI
hot spots is not evidence it will work for ours.

**Rosell & Fernández-Recio 2020** [VERIFIED-ABSTRACT]. _Comput Struct Biotechnol J_ 18:3750–3761,
doi:10.1016/j.csbj.2020.11.029, PMCID PMC7679229. pyDock energy-based docking scores hot spots "on
the unbound proteins, thus not requiring the complex structure," then couples that to MD-generated
transient cavities.
_Verdict — C1 PASS for the docking half; C2 **FAIL** for the cavity half (explicit MD); C6 FAIL._
The docking half survives, the pipeline as published does not.

### 3d. Physics-based ΔΔG engines (used as hot-spot surrogates)

**Kortemme & Baker 2002** [VERIFIED-ABSTRACT]. "A simple physical model for binding energy hot spots
in protein-protein complexes." _PNAS_ 99:14116–14121, doi:10.1073/pnas.202485799, PMCID PMC137846.
Mean absolute errors: **0.81 kcal/mol on 743 globular-protein mutations** and **1.06 kcal/mol on 233
mutations across 19 protein-protein interfaces**. This is the Robetta alanine-scanning lineage.
_Verdict — C1 FAIL for ΔΔG_bind (needs both partners); C1 PASS for ΔΔG_fold on a monomer; C2 PASS;
C6 FAIL._

**FoldX, revisited — Delgado, Reche, Cianferoni, Orlando, van der Kant, Rousseau, Schymkowitz &
Serrano 2025** [VERIFIED-ABSTRACT]. _Bioinformatics_ 41:btaf064, doi:10.1093/bioinformatics/btaf064,
PMCID PMC11879241. The improved force field reports **R = 0.706, RMSE = 1.252 kcal/mol** on its
validation set. The original 2005 FoldX web-server paper was **not retrieved by the recorded search**
this session; only the 2025 revision and downstream assessments came back.

**Barnes, Chi, Pandey, Ytreberg & Patel 2026** [VERIFIED-ABSTRACT]. "Leveraging Neural Networks to
Correct FoldX Free Energy Estimates." _ACS Omega_ 11:30003–30013, doi:10.1021/acsomega.6c01409,
PMCID PMC13216946. A learned correction lifts FoldX binding predictions from **correlation 0.37 to
0.61**. Read the 0.37 as the honest out-of-the-box number for FoldX ΔΔG_bind on that set.

**MM/GBSA computational alanine scanning** [VERIFIED-ABSTRACT]. Valdés-Tresanco, Valdés-Tresanco,
Moreno & Valiente 2023, _J Phys Chem B_ 127:944–954, doi:10.1021/acs.jpcb.2c07079: the internal
dielectric constant is the dominant parameter, and adding entropy or explicit water **decreased**
prediction quality. Liu, Xu, Duan & Zhang 2026, _Chem Sci_, doi:10.1039/d6sc04176k, PMID 42621395,
reviews the GBSA/interaction-entropy family.
_Verdict — C2 FAIL for the standard protocol._ The interaction-entropy term is defined from MD
fluctuations (Yan, Yang, Ji & Zhang 2017, _J Chem Inf Model_ 57:1112–1122,
doi:10.1021/acs.jcim.6b00734 [VERIFIED-ABSTRACT]). Single-snapshot MM/GBSA without the entropy term
is C2-legal; the version that carries the published accuracy is not.

**BAlaS/BudeAlaScan — Wood, Ibarra, Bartlett, Wilson, Woolfson & Sessions 2020**
[VERIFIED-ABSTRACT]. _Bioinformatics_ 36:2917–2919, doi:10.1093/bioinformatics/btaa026. Interactive
CAS, no MD. Needs the complex. _C1 FAIL, C2 PASS._

**Robin, Sato, Desplancq, Rochel, Weiss & Martineau 2014** [VERIFIED-ABSTRACT]. _J Mol Biol_
426:3729–3743, doi:10.1016/j.jmb.2014.08.013. CAS over **227 antibody-antigen complexes**: "as few
as 8 residues among 30 key positions" explain **80% of binding free energy**. A quantitative
statement of how sparse the energetic signal is — and therefore how small a true-positive set a
hit-list metric is chasing.

**HotspotPred — Hamdani, Cianferoni, Reche, Delgado & Serrano 2025** [VERIFIED-ABSTRACT]. _Protein
Sci_ 34:e70220, doi:10.1002/pro.70220, PMCID PMC12268110. Residue-triplet features, **accuracy 0.73
on 1,160 alanine mutants** (nanobody interfaces). _C1 FAIL, C2 PASS._

---

## 4. Interfaces coupled to active sites: the mechanism literature

This is the argument that a PPI interface and an internal active site are two ends of one network,
which is exactly the physical claim `CHALLENGE.md` §4.1 asks us to compute.

**Nussinov, Tsai & Csermely 2011** [VERIFIED-ABSTRACT]. "Allo-network drugs: harnessing allostery in
cellular networks." _Trends Pharmacol Sci_ 32:686–693, doi:10.1016/j.tips.2011.08.004, PMCID
PMC7380718. Proposes drugs "whose effects can propagate either **within a protein, or across
several proteins**." The intra-protein half of that sentence is our problem statement.

**Szilágyi, Nussinov & Csermely 2013** [VERIFIED-ABSTRACT]. "Allo-network drugs: extension of the
allosteric drug concept to protein-protein interaction and signaling networks." _Curr Top Med Chem_
13:64–77, doi:10.2174/1568026611313010007, PMID 23409766. Companion editorial: Csermely, Nussinov &
Szilágyi, _Curr Top Med Chem_ 13:2–4, doi:10.2174/1568026611313010002 [VERIFIED-ABSTRACT].

**Csermely, Korcsmáros, Kiss, London & Nussinov 2013** [VERIFIED-ABSTRACT]. _Pharmacol Ther_
138:333–408, doi:10.1016/j.pharmthera.2013.01.016, PMCID PMC3647006. Distinguishes a **"central hit
strategy"** (target hubs of a flexible network) from a **"network influence strategy"** (reconfigure
a rigid network from its periphery). That distinction maps directly onto our choice between ranking
by centrality — which conventions §6 already puts on the must-clear bar — and ranking by
source-conditioned influence, which is what the challenge actually asks for.

**Ma & Nussinov 2014** [VERIFIED-FULLTEXT]. "Druggable orthosteric and allosteric hot spots to
target protein-protein interactions." _Curr Pharm Des_ 20:1293–1301,
doi:10.2174/13816128113199990073, PMCID PMC6361532. Three quotes matter, all fetched:

- "The hot spots in protein-protein interactions are **coupled with conformational dynamics** of
  protein complexes."
- "Hot spot residues are often '**hub**'-like residues in protein complexes represented as
  small-world networks."
- "Hot spots and structurally conserved residues often locate in complemented pockets that
  **pre-organized in the unbound states**."

The paper distinguishes **orthosteric** hot spots ("at the protein-protein interaction site") from
**allosteric** hot spots ("elsewhere") but the fetched text gives no formal definition of either and
no quantitative comparison between them. Treat the shared-network-signature claim as **asserted, not
measured** [UNVERIFIED as a quantitative claim].

**Di Paola & Giuliani 2015** [VERIFIED-ABSTRACT]. "Protein contact network topology: a natural
language for allostery." _Curr Opin Struct Biol_ 31:43–48, doi:10.1016/j.sbi.2015.03.001, PMID 25796032. Positions contact-network formalism as the substrate for allo-network drug design. C6
stated as a research programme.

_Verdict for the whole section — C1 PASS, C2 PASS, C6 PASS._ These are conceptual papers with no
implementable score. Their value is that they license the transfer and give the report a sourced
narrative; they do not supply a number.

**Where the "shared network signature" claim actually has support.** Two independent, weak lines,
plus one strong counter-line.

- **Weak support A.** Sarica, Sungur & Kurkcuoglu 2026, "RinPy," _J Chem Inf Model_ 66,
  doi:10.1021/acs.jcim.6c00004, PMID 41940623 [VERIFIED-ABSTRACT]: computes "degree, closeness, and
  betweenness" on a residue interaction network, and "the nodes with the highest betweenness scores
  are used to suggest putative allosteric sites." No benchmark statistic retrieved.
- **Weak support B.** Inan, Yuce, MacKerell & Kurkcuoglu 2024, _ACS Omega_ 9,
  doi:10.1021/acsomega.4c06172, PMCID PMC11425613 [VERIFIED-ABSTRACT]: proposed GPCR sites "were
  located at the interfaces of highly interconnected residue clusters."
- **Strong counter-line.** §6 item 1 below. When allosteric hot spots were measured exhaustively by
  deep mutational scanning, they were "**distributed protein-wide rather than being restricted to
  'pathways' linking allosteric and active sites**," and sequence conservation did **not** separate
  them from non-hot-spots. Both facts contradict the naive reading of the shared-signature claim.

---

## 5. Ranking residues by coupling to a second site

This is the section that matters. Every method here conditions on a named site and emits a
per-residue score for every other residue — our exact output shape.

### 5a. Coevolution: coupled by sequence, not by structure

**Lockless & Ranganathan 1999** [VERIFIED-ABSTRACT]. "Evolutionarily conserved pathways of energetic
connectivity in protein families." _Science_ 286:295–299, doi:10.1126/science.286.5438.295, PMID 10514373. SCA measures statistical coupling between alignment positions, predicts long-range
couplings in the PDZ domain, and finds that coupled sets "form connected pathways through protein
structures."

**Is SCA admissible here? C1 PASS, C2 PASS, C6 FAIL — with one build-time guard.** The reasoning,
stated because the brief asks for it explicitly:

- **C1 (apo only).** An MSA is built from sequence databases. The apo and holo forms of a protein
  have the _same sequence_, so an MSA cannot encode which conformer was crystallised. It carries no
  holo geometry, no holo pocket, no holo residue count. C1 is satisfied on the merits, not by a
  technicality. The one live leakage route is procedural: if the homolog set, the alignment trimming
  or a structural template were chosen using knowledge of the answer, that choice leaks. That is a
  guard on our build script, not a property of SCA.
- **C2 (no MD).** SCA touches no trajectory and no MD-trained weight. Clean.
- **C6 (topology-driven).** SCA is explicitly _not_ a contact-topology method. It is a second,
  independent measurement channel for the same physical coupling. Using it would mean stepping
  outside the elastic-network hypothesis, which is allowed but must be declared.

**Two retrieved results argue against leaning on it.** Teşileanu, Colwell & Leibler 2015,
_PLoS Comput Biol_ 11:e1004091, doi:10.1371/journal.pcbi.1004091, PMCID PMC4344308
[VERIFIED-ABSTRACT], report that **conservation dominates the SCA result for single-sector
proteins** — i.e. much of what SCA finds is recoverable from a conservation score alone. And §6
item 1 records that conservation does not separate allosteric hot spots. Combined with the DCA
negative already recorded in `review/05` §5 (Bravi et al., doi:10.1371/journal.pcbi.1007630 — DCA
"fails to capture long-range epistasis" against a known mechanical ground truth), the coevolution
channel has now failed two independent checks at exactly the range that defines allostery.
**Recommendation: do not budget an SCA baseline.**

### 5b. Double-mutant cycles: the experimental definition of coupling

**Horovitz, Fleisher & Mondal 2019** [VERIFIED-ABSTRACT]. "Double-mutant cycles: new directions and
applications." _Curr Opin Struct Biol_ 58:10–17, doi:10.1016/j.sbi.2019.03.025, PMID 31029859.
**Pagano, Toto, Malagrinò, Visconti, Jemth & Gianni 2021** [VERIFIED-ABSTRACT]. "Double Mutant
Cycles as a Tool to Address Folding, Binding, and Allostery." _Int J Mol Sci_ 22:828,
doi:10.3390/ijms22020828, PMCID PMC7830974. **Sokolovski, Cveticanin, Hayoun, Korobko, Sharon &
Horovitz 2017** [VERIFIED-ABSTRACT]. _Nat Commun_ 8:212, doi:10.1038/s41467-017-00285-1, PMCID
PMC5550451 — pairwise interaction energies from a single native mass spectrum.

_Verdict — not a prediction method._ A double-mutant cycle is an **experimental ground-truth
generator**: ΔΔG_int(i,j) = ΔΔG(i) + ΔΔG(j) − ΔΔG(i,j). It defines what "coupling" means so that a
computed score can be validated against it. Recorded here so that no phase mistakes it for a
predictor. It is the operation the DMS papers in §6 industrialise.

### 5c. Structure-only coupling estimators — the transferable core

**Ohm — Wang, Jain, McDonald, Gambogi, Lee & Dokholyan 2020** [VERIFIED-FULLTEXT]. _Nat Commun_
11:3862, doi:10.1038/s41467-020-17618-2, PMCID PMC7395124. Fetched algorithm:

- Propagation probability between contacting residues: **P_ij = 1 − e^(−α·N_ij)**, where N_ij is a
  normalised contact count (contacts divided by atom counts), and **α = 3.0**.
- Stochastic propagation: "a random number between 0 and 1 is generated. If this random number is
  less than the perturbation propagation probability between residue i and residue j, P_ij, then we
  propagate this perturbation from i to j." The process "is repeated **10⁴ times**."
- **ACI** = "the frequency with which each residue is affected by a perturbation."
- Source: users "use all residues on the active site" as the perturbation origin.
- "Ohm relies solely on the structure of the protein of interest" — no MD in the method itself.

_Verdict — C1 PASS, C2 PASS, C6 PASS._ This is the cleanest structure-only, source-conditioned
coupling estimator retrieved, and it is computable from precisely our permitted inputs. Its
benchmark numbers (TPR 0.57 / PPV 0.72) are already in `review/01` §3 and are not restated here. Its
**failure** is in §6.

Note what Ohm actually is, stripped of biology: an **independent-cascade diffusion model** seeded at
the active site, with edge activation probabilities read off contact density, estimated by Monte
Carlo. That identification is not made in the paper [UNVERIFIED as the authors' framing] but it is
what the fetched equations say, and it matters because `review/05` §7 already flags influence
maximisation — the submodular optimisation _over_ independent-cascade models — as an untried
reframing of our top-5 deliverable. The two connect: Ohm supplies the cascade model that influence
maximisation would optimise over.

**Perturbation-response scanning and the Dynamic Coupling Index — Gerek & Ozkan 2011**
[VERIFIED-FULLTEXT]. _PLoS Comput Biol_ 7:e1002154, doi:10.1371/journal.pcbi.1002154, PMCID
PMC3188487. Fetched:

- Linear response: **ΔR = H⁻¹ · ΔF**, with H the ENM Hessian.
- Forces are applied in **7 directions per residue** (x, y, z, xy, xz, yz, xyz).
- The paper defines the **allosteric response ratio χ_j**: "the ratio of average fluctuation response
  of the residue j upon perturbations placed on **binding site residues** to average response of
  residue j upon perturbations on **all residues**."
- Input: Cα coordinates plus the identity of the binding-site residues. **No MD** in the core
  calculation.

**Campitelli & Ozkan 2020** [VERIFIED-FULLTEXT]. "Allostery and Epistasis: Emergent Properties of
Anisotropic Networks." _Entropy_ 22:667, doi:10.3390/e22060667, PMCID PMC7517209. Fetched equations:

- **[ΔR]_(3N×1) = [H]⁻¹_(3N×3N) [F]\_(3N×1)**
- **|ΔR^j|\_i = √⟨(ΔR)²⟩** — response magnitude at i to a perturbation at j.
- **DCI_ij = [ Σ_j |ΔR^j|_i / N_functional ] / [ Σ_(j=1..N) |ΔR^j|\_i / N ]**
- **DCI_asym = DCI_i − DCI_j**
- EpiScore: the %DCI at a functional position k under simultaneous perturbation at i and j, over the
  average of the individual perturbations.

_Verdict — C1 PASS, C2 PASS, C6 PASS._ DCI conditioned on the active site is, term for term, "rank
residues by dynamic connectivity to a named active site." It is the single best formula-level match
in this file. Related applications carrying the same machinery: Kazan, Mills & Ozkan 2023, _Protein
Sci_ 32:e4700, doi:10.1002/pro.4700 [VERIFIED-ABSTRACT]; Campitelli, Kazan, Hamilton & Ozkan 2025,
_J Mol Biol_ 437:169175, doi:10.1016/j.jmb.2025.169175 [VERIFIED-ABSTRACT]. Caution: Huynh, Kazan,
Lu, Kolbaba-Kartchner, Mills & Ozkan 2025, _PNAS_ 122:e2502444122, doi:10.1073/pnas.2502444122
[VERIFIED-ABSTRACT] wraps DCI_asym in a **trained** GNN — the wrapper is supervised and would need
its own C1/C2 audit; the bare DCI does not.

**SBSMMA / AlloSigMA — Guarnera & Berezovsky 2016** [VERIFIED-FULLTEXT]. _PLoS Comput Biol_
12:e1004678, doi:10.1371/journal.pcbi.1004678, PMCID PMC4777440. Fetched:

- Per-residue configurational work: **Δg_i(P→AP) = (½)k_B T Σ_μ ln[ ε^(AP)\_μ,i / ε^(P)\_μ,i ]**,
  comparing spring constants across low-frequency modes between the ligand-free (P) and
  ligand-bound (AP) harmonic systems.
- **The input is the apo structure only.** Fetched verbatim: "The ligand bound system AP is obtained
  from the free system P by **harmonic restraining of all the pairs of residues belonging to the
  allosteric binding site A**." No ligand coordinates and no holo structure are needed.
- The fetched text provides **no quantitative validation metrics** — results across seven test
  proteins are qualitative. Recorded as a gap, not filled.

_Verdict — C1 PASS (this is the strongest C1 result in the file: a ligand's effect is emulated by
restraining residue pairs in the apo ENM), C2 PASS, C6 PASS._ Servers and databases: AlloSigMA,
_Bioinformatics_ 33:3996–3998, doi:10.1093/bioinformatics/btx430; AlloSigMA 2, _Nucleic Acids Res_
48:W116–W124, doi:10.1093/nar/gkaa338, PMCID PMC7319554; AlloMAPS 2, _Nucleic Acids Res_
51:D345–D351, doi:10.1093/nar/gkac828 [all VERIFIED-ABSTRACT].

Note the family resemblance: SBSMMA's "restrain the site's residue pairs and read the mode-spectrum
shift" is the same operation as APOP's "stiffen the springs across the pocket lining and read the
global-mode frequency shift" (`review/01` §2). The difference is the readout — SBSMMA reads a
**per-residue** free energy relative to a **named second site**, APOP reads a **global** eigenvalue
shift. For our task shape, SBSMMA's readout is the right one and APOP's is not.

**Bond-to-bond propensity — Amor, Schaub, Yaliraki & Barahona 2016** [VERIFIED-FULLTEXT]. _Nat
Commun_ 7:12477, doi:10.1038/ncomms12477, PMCID PMC5007447. Fetched:

- Edge-to-edge transfer matrix **M = G·B·L†·Bᵀ·G**, with G = diag(w_b) the bond-energy diagonal, B
  the incidence matrix, and L† the Moore–Penrose pseudo-inverse of the Laplacian L = D − W.
- Per-bond propensity **Π_b = Σ\_(a ∈ active site) M_ba / E**; residue aggregation
  **Π_R = Σ\_(b ∈ residue R) Π_b**.
- **Quantile regression** against distance: "To identify bonds with high propensities relative to
  others at a **similar distance** from the active site, we use quantile regression."
- Results: caspase-1 E390–R286 salt bridges at 0.996 and 0.990 (experimentally, 230-fold and
  130-fold drops in catalytic efficiency); CheY's phosphorylation site D57 at p_R = 0.96, with
  allosteric residues averaging **p_R = 0.61 vs 0.43** for non-allosteric; h-Ras bonds ranked 1st
  and 3rd of 1,159 weak interactions. Test set: "**Nineteen out of 20** allosteric sites are
  identified by at least one measure, and **15 out of 20** by at least three of four measures."
- Scaling: "The computation time scales almost linearly in the number of edges."

_Verdict — C2 PASS, C6 PASS. C1 CONDITIONAL._ The fetched text says the source is specified "given
the location of the known active site," and the extraction read that as requiring the bound
structure to enumerate ligand–protein bonds. That reading is the **tool's convenience route**, not a
hard requirement: the CheY case takes a single residue (D57) as the source [VERIFIED-FULLTEXT], so a
residue-number-defined source is what the authors themselves use. For us the active site arrives as
residue numbers from the input manifest, which is a permitted input. **The C1-legal variant is: source
= active-site residue numbers; the C1-illegal variant is: source = the holo ligand's contacts.** This
distinction must be enforced in code, not assumed.

Note also that M is built from L†, the same pseudo-inverse that `review/05` §STEP-3(a) already
identifies as its top candidate (effective resistance). **The genuinely new ingredient here is not
the propensity — it is the quantile regression against distance.** See §7 item 1.

**ProteinLens — Mersmann, Strömich, Song, Wu, Vianello, Barahona & Yaliraki 2021**
[VERIFIED-FULLTEXT]. _Nucleic Acids Res_ 49:W551–W558, doi:10.1093/nar/gkab350, PMCID PMC8661402.
Web front end for bond-to-bond propensity and **Markov Transients**. Fetched: transients model "how
the perturbations propagate over the atomistic graph using a random walk formalism," tracking "the
probability of the random walker being at a certain node at any time point," with the readout "the
characteristic transient time **t₁/₂** of a node, defined as the time needed for the probability to
reach half its stationary value." The quantile score runs "from 0 to 1 ... based on the significance
of that atom or bond compared to all other atoms and bonds **equidistant from the source**, thereby
**account[ing] for this distance bias**." Input: one PDB identifier or one uploaded PDB file. The
paper does not reproduce the underlying equations; it refers to Amor et al.

_Verdict — C1 PASS (single structure; source is user-chosen), C2 PASS, C6 PASS._ The t₁/₂ readout
is a hitting-time quantity and therefore overlaps Chennubhotla & Bahar's hit/commute times, already
recorded in `review/01` §3 — not new. The distance-conditioned quantile score is the new part, and
it is the same idea as Amor's.

---

## 6. Negative evidence: four measured failures

Each of these is a case where hot-spot or coupling machinery met a distribution it was not fitted to.

**1. Ohm on experimentally measured allosteric hot spots: accuracy 0.08–0.40.** Leander, Liu, Cui &
Raman 2022, "Deep mutational scanning and machine learning reveal structural and molecular rules
governing allosteric hotspots," _eLife_ 11:e79932, doi:10.7554/eLife.79932, PMCID PMC9662819
[VERIFIED-FULLTEXT]. Four TetR-family allosteric transcription factors — TetR, TtgR, MphR, RolR —
each ~200 residues, single-site saturation mutagenesis giving "~3800 mutants per aTF (~200 residues
× 19 mutants/residue)." After excluding ligand-contacting residues, **41, 43, 29 and 51 hot spots**
respectively. The Ohm webserver, run on the same proteins, scored **accuracy 0.08 (TetR), 0.12
(TtgR), 0.31 (MphR), 0.40 (RolR)**.

This is the most important number in this file. Ohm is the closest published task-shape match to our
own pipeline (`review/01` §8b), it satisfies C1/C2/C6 exactly, and it reports TPR 0.57 / PPV 0.72 on
its own 20-protein set. Against exhaustive experimental ground truth on four proteins it retains
almost nothing. Two readings are available and this file cannot choose between them
[UNVERIFIED which is correct]: either source-conditioned pathway propagation is a much weaker signal
than its own benchmark suggests, or DMS-defined allosteric hot spots and ASD-style annotated
allosteric _sites_ are different positive classes and the comparison is not like-for-like. Both
readings are actionable. The first says the whole method family is in trouble; the second says our
frozen positive class determines what we can claim, which is a point `review/00` §2 already makes
about comparability.

Three further findings from the same paper, all [VERIFIED-FULLTEXT]:

- Hot spots are "**distributed protein-wide** rather than being restricted to 'pathways' linking
  allosteric and active sites."
- **Conservation does not work**: "allosteric hotspots [were] **not statistically higher** [in]
  sequence conservation in hotspots over non-hotspots."
- **Global beats local**: "global structural and dynamic properties [were] a stronger predictor of
  whether a residue is a hotspot than local and physicochemical properties," and "global features
  have the highest F scores" across all four proteins. Their own supervised model reached F1 **0.83
  (TetR), 0.54 (TtgR), 0.82 (MphR), 0.64 (RolR)** — i.e. it is protein-dependent and not
  transferable at the low end.

The 11 global features, fetched from the article page [VERIFIED-FULLTEXT]: motional correlation with
the DNA region; motional correlation with the ligand region; maximum correlation with other
residues; distance to DNA; distance to ligand; closeness centrality; distance to each of four
centrality peaks; and "sequence propagation" (largest sequence separation within a 5 Å contact).
Motional correlations were computed with an **elastic network model, not MD** — verbatim: "motional
covariance between a residue and the ligand/DNA-binding residues evaluated using an elastic network
model." That makes the entire global feature block C2-legal, and it is a near-exact enumeration of
what our own `network/` stage can produce.

**2. FTMap loses almost all sensitivity for hot spots on the free structure: 0.07.** From the
PPI-HotspotID full text [VERIFIED-FULLTEXT], head-to-head on the same 158-protein set:

| Method        | True positives | Sensitivity | Precision | F1   |
| ------------- | -------------- | ----------- | --------- | ---- |
| PPI-HotspotID | 278            | 0.67        | 0.76      | 0.71 |
| FTMap         | 30             | **0.07**    | 0.64      | 0.13 |
| SPOTONE       | 40             | **0.10**    | 0.64      | 0.17 |

SPOTONE's own paper reports accuracy 0.82 / AUROC 0.83 / recall 0.82 on its own test set
(doi:10.3390/ijms21197281). On an independent set assembled by another group it recovers **10%** of
the positives. The precision stays at 0.64 for both, which is the diagnostic: these methods are not
wrong about what they find, they find almost nothing. A hit-list deliverable is a
**sensitivity** deliverable, so this is the failure mode that would hurt us.

**3. FTMap on annotated allosteric sites: 15/24, and 21/39.** Two independent GPCR studies.

- Peter, Siragusa, Thomas, Palomba, Cross, O'Boyle, Bajusz, Ferenczy, Keserű, Bottegoni, Bender,
  Chen & de Graaf 2024, _J Chem Inf Model_, doi:10.1021/acs.jcim.4c00819, PMCID PMC11558664
  [VERIFIED-FULLTEXT]. Across **24 allosteric GPCR binding sites**: **BioGPS 22/24, SiteMap
  (default) 20/24, FTMap 15/24 (62%)**. Success criterion, verbatim: "The site detection is
  considered successful if the bound ligand is partially covered by the predicted pocket."
  The apo-degradation axis, fetched: of 33 unique receptor–site combinations, only **60% (inactive)
  and 56% (active)** were detected in the unliganded reference structures, and "the ligand-induced
  effect on the binding site formation is particularly pronounced with extrahelical sites from the
  active-state receptor, as **five out of six were not detected** among the Reference structures."
- Wakefield, Bajusz, Kozakov, Keserű & Vajda 2022, _J Chem Inf Model_, doi:10.1021/acs.jcim.2c00209,
  PMCID PMC9847135 [VERIFIED-FULLTEXT, via the PMC article page after `fullTextXML` returned 404].
  Of **39 GPCR X-ray structures with bound allosteric inhibitors, 21** had an FTMap druggable hot
  spot overlapping the ligand — **18 did not**. On AlphaFold2 models, only **17 of those 21**
  survived, with named failures at CRF1 (helix occlusion), mGlu5 (Trp side-chain obstruction) and
  PAR2 (Lys side-chain movement). Druggability threshold: **≥16 probe clusters**.

Both are consistent with Vajda, Beglov, Wakefield, Egbert & Whitty 2018, _Curr Opin Chem Biol_
44:1–8, doi:10.1016/j.cbpa.2018.05.003, PMCID PMC6088748 [VERIFIED-FULLTEXT], which reports the more
optimistic framing — "for **81%** of the proteins at least one of the unbound structures has hot
spots with 16 or more probe clusters within 5 Å of the cryptic site" — while immediately flagging
that "the condition that binding 16 probe clusters implies druggability was based on the analysis of
traditional drug targets, and **may over-predict druggability when applied to cryptic sites**." Note
that 81% is a _best-of-several-unbound-structures_ number and the 60%/56% above is a
single-reference-structure number; they are not comparable and must not be quoted side by side as if
they were.

**4. Hot-spot ΔΔG regressors do not survive a temporal holdout: PCC 0.80 → below 0.42.** Geng,
Vangone, Folkers, Xue & Bonvin 2019, "iSEE," _Proteins_ 87:110–119, doi:10.1002/prot.25630, PMCID
PMC6587874 [VERIFIED-ABSTRACT]. Trained on 1,102 mutations across 57 complexes, reported PCC 0.80.
Verbatim from the retrieved record: "Predictions for a new dataset of 487 mutations in 56 protein
complexes from the recently published SKEMPI 2.0 database reveals that **none of the current methods
perform well (PCC < 0.42)**, although their combination does improve the predictions." A companion
methodological warning: Chen, Kuhn & Raschka 2022, bioRxiv, doi:10.1101/2022.12.26.521948
[VERIFIED-ABSTRACT], uses "500-fold repartitioning of training and test sets" to show that standard
cross-validation masks overfitting in this exact task, and finds that the two most important
features are simply **wild-type residue accessible surface area and evolutionary conservation**.

**How these four sit against conventions §6.** They are the PPI field's version of the same
deflation that AlloBench and CAPASP delivered to the allostery field (`review/01` §7). Two fields,
independent datasets, same conclusion: published leaderboard numbers for residue-level functional-site
prediction do not survive a leakage-controlled or temporally separated retest, and the deflation is
large enough to reorder the methods.

---

## 7. What this changes for our pipeline

Six concrete score functions, each computable from **only** the permitted inputs: a residue contact
graph with heavy-atom minimum distances, Cα/heavy-atom coordinates, the one-letter sequence, and a
named set of active-site residue numbers. Ranked by (expected information gained) / (implementation
cost). Every one is C1 PASS, C2 PASS.

### 1. Distance-conditioned residual score. Stage: `scoring/`. Cost: ~15 lines.

The highest-value item in this file, and it is a **wrapper**, not a new method. Both Barahona-lab
tools normalise the propagation score against the distribution of scores at the _same distance from
the source_ (doi:10.1038/ncomms12477, doi:10.1093/nar/gkab350). Our repo has already measured why
this matters: `ctrl_closeness = −distance` reaches AUC 0.617 and beats most quantum observables
(conventions §5). Independently, Martí-Aranda & Lehner 2026, _Nat Commun_,
doi:10.1038/s41467-026-71005-x, PMCID PMC13284222 [VERIFIED-FULLTEXT], measured the decay directly
over **21,802 free-energy changes**: "the probability of a mutation causing a change in binding
energy decays with the distance from the binding interface, with a **50% reduction of energetic
effects over a median distance d₁/₂ = 6.9 Å**," per-protein 8.3 Å (SRC), 9.50 Å (KRAS), 5.6 Å (GB1),
13.6 Å (GRB2-SH3). And — the operative number — "a median of **14.4% of mutations have effects
larger than expected given the distance-dependent decay**."

That 14.4% _is_ the residual signal. Score it directly.

```
d[i]        = min over a in active_site of heavy_atom_min_dist(i, a)
raw[i]      = any source-conditioned score (items 2, 3 below)
# fit the conditional median of raw on d (quantile regression, tau=0.5,
# or simply bin d at 1 A and take the per-bin median)
resid[i]    = raw[i] - conditional_median(raw | d = d[i])
rank by resid[i]        # ties broken by raw[i]
```

Expected information: high. It converts every score in this file from one that competes with
`−distance` into one that is orthogonal to it by construction, which is the axis the frozen
evaluation layer stratifies on. Cost: near zero.

### 2. Ohm-style cascade reachability, computed deterministically. Stage: `classical/`. Cost: ~25 lines.

From doi:10.1038/s41467-020-17618-2 [VERIFIED-FULLTEXT]. The published estimator draws 10⁴ Monte
Carlo cascades. The cheap deterministic surrogate is the **most-probable path**, which is a Dijkstra
run on negative log weights and needs no sampling or seed:

```
N[i][j] = n_heavy_atom_contacts(i,j) / (n_atoms(i) * n_atoms(j))   # as published
P[i][j] = 1 - exp(-3.0 * N[i][j])                                   # alpha = 3.0, as published
w[i][j] = -log(P[i][j])
aci_path[i] = exp(-shortest_path_dist(active_site_set -> i, weights=w))   # multi-source Dijkstra
```

Report `aci_path` and, if the Monte Carlo version is also run, report both — they differ, because
the cascade counts all paths and the Dijkstra surrogate counts the best one. Expected information:
high, because we have a published head-to-head number to reproduce (`review/01` §3) **and** a
published failure to reproduce (§6 item 1). Reproducing the failure is as informative as reproducing
the win; it tells us whether our positive class behaves like ASD annotations or like DMS hot spots.

### 3. DCI conditioned on the active site. Stage: `classical/`. Cost: ~40 lines given an ANM Hessian.

From doi:10.3390/e22060667 [VERIFIED-FULLTEXT], term for term our task shape:

```
H        = ANM Hessian from Ca coordinates, cutoff 13 A (or the contact graph's own weights)
Hinv     = pseudo_inverse(H)                    # 3N x 3N, one call
for each source residue j:
    for each of 7 force directions f:
        dR = Hinv @ F(j, f)                     # F is zero except at j
    A[i][j] = mean over f of || dR[i] ||        # response magnitude at i to a kick at j
DCI[i]   = mean(A[i][j] for j in active_site) / mean(A[i][j] for j in all residues)
```

The denominator is what makes it a _coupling_ score rather than a _flexibility_ score: it divides out
residue i's intrinsic responsiveness. That is exactly the confound our repo needs controlled, and it
comes free. Expected information: high — this is the strongest published lineage for our exact
question and `review/01`'s Phase 1.4 list does not contain it (PRS is listed there; the
active-site-normalised DCI readout of PRS is not). Cost: moderate, dominated by one pseudo-inverse.

### 4. Hot-region smoothing of any per-residue score. Stage: `scoring/`. Cost: 3 lines.

From doi:10.1016/j.jmb.2004.10.077 [VERIFIED-ABSTRACT]: hot spots cluster into densely packed hot
regions, cooperative within a cluster and additive between clusters. Our ground truth is a pocket —
a spatial cluster — not an isolated residue, and `review/01` §5 already records P2Rank's argument
that residue-level metrics penalise a correct pocket call.

```
smooth[i] = mean(score[j] for j where heavy_atom_min_dist(i,j) <= 6.5)   # includes i
```

Expected information: moderate and cheap. It should raise any noisy per-residue score, and if it
does **not**, that is itself evidence that the score is not localising to a coherent region — worth
knowing before Phase 5. Run it as an ablation on every method, not as a default.

### 5. SBSMMA-style restraint response. Stage: `classical/` or `network/`. Cost: ~60 lines, and N ENM re-solves.

From doi:10.1371/journal.pcbi.1004678 [VERIFIED-FULLTEXT], and the only method in this file whose
published input is _literally_ "apo structure plus a named site":

```
eps_P    = ENM mode spectrum of the apo structure
for each candidate site S (a residue and its spatial neighbours within 6.5 A):
    eps_AP = ENM mode spectrum with all residue pairs in S harmonically restrained
    dg[S]  = 0.5 * kB*T * sum over low-frequency modes mu of
                 log( eps_AP[mu, active_site] / eps_P[mu, active_site] )
rank candidates by |dg[S]|
```

Note the direction: this perturbs the **candidate** and reads the **active site**, which is the
reverse of items 2 and 3. Running both directions gives an asymmetry — the DCI_asym idea
(doi:10.3390/e22060667) — which a symmetric contact graph cannot otherwise supply and which
`review/05` §6 identifies as the one structural ingredient a plain contact graph lacks. Expected
information: moderate-to-high. Cost: high, because it needs one eigendecomposition per candidate.
Do items 1–3 first; do this only if they clear the bar.

### 6. O-ring occlusion feature. Stage: `network/`. Cost: ~10 lines. **Ranked last, and probably skip.**

From doi:10.1006/jmbi.1998.1843 and doi:10.1093/nar/gkq323: burial plus a knowledge-based contact
potential. Computable from our inputs as `rASA_monomer[i]` plus a Miyazawa-Jernigan sum over contact
neighbours (we have the sequence and the graph). But three retrieved results argue against spending
the time: HotPoint's ≤20% threshold is defined on **complex-state** rASA and does not transfer
(§3a); Leander et al. found local physicochemical properties **lose to global ones** for allosteric
hot spots (§6 item 1); and conservation — PPI-HotspotID's single most important feature — **does not
separate** allosteric hot spots. Record the reasoning; do not implement.

### Three things not to spend time on

- **An SCA or coevolution baseline.** §5a. Two independent negatives at long range (Teşileanu
  doi:10.1371/journal.pcbi.1004091; Bravi doi:10.1371/journal.pcbi.1007630 via `review/05`), plus
  Leander's finding that conservation does not separate allosteric hot spots.
- **Any hot-spot predictor that ingests a complex.** HotPoint, KFC2, SpotOn, HotRegion, BAlaS,
  DSSA-PPI, iSEE. C1 FAIL, not negotiable.
- **MM/GBSA with the interaction-entropy term.** doi:10.1021/acs.jcim.6b00734 defines it from MD
  fluctuations. C2 FAIL. Single-snapshot MM/GBSA without entropy is legal but carries none of the
  published accuracy.

### One framing point for the report

`docs/report/` should state the four §6 failures alongside AlloBench and CAPASP (`review/01` §7).
They are independent fields reaching the same conclusion, and they set the honest expectation for
our own numbers. In particular, **Ohm at 0.08–0.40 against DMS ground truth** is the number that
should appear next to any claim we make about source-conditioned propagation, because Ohm is the
published method closest to what we are building.

---

## Method

**Databases and routes used** (conventions §3): Europe PMC REST search API (`/search?query=...`,
`resultType=core`) as the primary route; Europe PMC `fullTextXML` for full-text extraction; the PMC
article page (`pmc.ncbi.nlm.nih.gov/articles/{PMCID}/`) as the fallback when `fullTextXML` returned
404; the arXiv API (`export.arxiv.org/api/query`). PubMed E-utilities was not needed — every PubMed
record wanted was reachable through Europe PMC. Semantic Scholar was not queried (rate-limited,
conventions §3).

**Queries run — 18 Europe PMC searches:** O-ring + hot spot + PPI interface; `TITLE:"Anatomy of hot
spots in protein interfaces"`; `TITLE:"hot regions" AND TITLE:"protein interfaces"` (0 hits);
Keskin + Nussinov + hot region; `"Allo-network drugs"`; `TITLE:HotPoint|KFC2|SpotOn|HotRegion`;
`TITLE:"computational alanine scanning"`; hot spot + unbound structure + predict;
`TITLE:ProteinLens|AlloSigMA` + bond-to-bond propensity; `TITLE:FoldX`; Guarnera + statistical
mechanical; `TITLE:"double mutant cycle"|"statistical coupling analysis"`; allosteric + hot spot +
fail/poor (miss); Lockless & Ranganathan by exact title; hot spot + allosteric site + benchmark/AUC
(miss); residue interaction network + betweenness + interface + allosteric; ML hot-spot predictors
2022–2026; `TITLE:SPOTONE`; SKEMPI + generalization/leakage; `"allosteric hot spot" + interface`;
`TITLE:"anchor residues"`; Keskin hot regions cooperativity (0 hits); Nussinov + allostery +
interface + propagation; DCI/DFI/PRS coupling; Ozkan + PDZ + allosteric network; `TITLE:"Allostery
and Epistasis"`; DMS + allosteric + hotspot; FTMap + allosteric site; interface + active site +
allosteric communication + elastic network. **2 arXiv API queries:** hot spot + PPI + allosteric
(0 results); allosteric + residue network (0 results); one broader arXiv query (allosteric protein
network) returned 20 records of which 1 was on topic (arXiv:2608.23490, PHASE — an ensemble-encoding
method, out of scope for this file). **14 full-text extractions:** PMC11405013 (PPI-HotspotID),
PMC5007447 (bond-to-bond propensity), PMC4777440 (SBSMMA), PMC8661402 (ProteinLens), PMC7395124
(Ohm), PMC3188487 (PRS/PDZ), PMC7517209 (DCI/EpiScore), PMC9662819 (Leander DMS, twice — XML then
article page for the feature list), PMC13284222 (Lehner PDZ family), PMC11558664 (GPCR allosteric
site comparison), PMC9847135 (Wakefield FTMap — article page after XML 404), PMC6088748 (Vajda
cryptic sites), PMC6361532 (Ma & Nussinov — article page after XML 404), PMC2896123 (HotPoint),
PMC12729103 (HOTPocket).

**Counts.** Roughly 140 distinct records surfaced across the searches. **41 screened in** with at
least one abstract- or full-text-verified claim and an explicit C1/C2/C6 verdict. 15 of those carry
at least one full-text-verified equation or number. 4 negative results screened in specifically as
negative evidence (§6). 3 records screened in only to be flagged unusable (HotPoint, SpotOn, iSEE as
C1 failures with instructive numbers).

**Stopping rule.** Stopped screening a sub-topic once (a) every explicit item in the task brief had
at least one sourced citation with a stated C1/C2/C6 verdict, and (b) two further independent
queries in that sub-topic returned only records already screened or clearly out of scope. The
negative-evidence hunt (§6) was the exception and was pursued through five differently-worded
queries before the DMS route (§6 item 1) produced the numbers; the four direct queries for
"hot-spot machinery applied to allosteric sites and failed" all missed, and the usable negatives
came from papers that report the failure incidentally rather than as their subject.

**Could not be reached this session.**

1. **The original FoldX web-server paper** (Schymkowitz et al. 2005, _Nucleic Acids Res_ 33:W382).
   Not returned by two `TITLE:FoldX` searches; only the 2025 revision and downstream assessments
   came back. FoldX's baseline ΔΔG accuracy is therefore quoted from doi:10.1093/bioinformatics/btaf064
   (R = 0.706) and doi:10.1021/acsomega.6c01409 (0.37 uncorrected), not from the original.
2. **A quantitative comparison of PPI hot spots against allosteric residues in the same proteins.**
   Two direct queries returned nothing. Ma & Nussinov's shared-network-signature claim
   (doi:10.2174/13816128113199990073) is asserted in prose with no accompanying statistic in the
   fetched text. Recorded as "not retrieved by the recorded search," per ADR 0019 — not as absent.
3. **Whether Ohm's 0.08–0.40 failure is a method failure or a positive-class mismatch.** The Leander
   full text gives the accuracies but not a breakdown against ASD-style annotated sites for the same
   four proteins, so the two candidate explanations in §6 item 1 cannot be separated from the
   retrieved evidence. Flagged rather than resolved.

Minor gaps, flagged not filled: the exact ε-parameter definition in SBSMMA's equation 6 (the fetched
XML gives the equation but not the full derivation of ε from the harmonic model); ProteinLens's
Markov-transient equations (the paper defers to Amor et al. and the fetched text confirms this);
Keskin & Nussinov's hot-region _fraction_ statistics (the cooperativity claim came back, the
per-interface counts did not — one query returned 0 hits).
