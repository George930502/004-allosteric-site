# Prior prediction attempts on the benchmark pockets — scoped evidence review

Retrieved 2026-08-20 via Europe PMC REST (`/search`, `/{PMCID}/fullTextXML`). Nothing in this
document comes from model memory; every PDB ID, residue number and metric traces to a source
retrieved in that session and cited inline.

This is **not a systematic review**: it has no registered protocol, multi-database search,
screening flow, eligibility ledger, duplicate review, or risk-of-bias assessment, and its
extraction-model output was not checked against every raw paper. “Nothing found” below means
only “not found by the recorded scoped retrieval”; it cannot establish absence of prior art
or a genuine research gap (ADR 0019).

## Tag key

| Tag                   | Meaning                                                                        |
| --------------------- | ------------------------------------------------------------------------------ |
| `[VERIFIED-FULLTEXT]` | Quote came back from `/{PMCID}/fullTextXML` for the cited paper                |
| `[VERIFIED-ABSTRACT]` | Quote came back from the `/search?resultType=core` abstract or metadata record |
| `[UNVERIFIED]`        | My inference, or a claim I could not source this session                       |

## Provenance caveat — read before quoting any of this in `docs/report/`

Europe PMC payloads were passed through an extraction model before reaching me. Sentences
marked verbatim were returned as verbatim by that pipeline; I did not read the raw bytes.
Before any quote here is used in the submission, re-pull the source and confirm the sentence.
The five highest-stakes quotes to re-check are flagged **[RE-CHECK]** inline.

---

# 1. Prior prediction attempts on these exact pockets

## 1.1 KRAS switch-II pocket (S-IIP) — attempted, and partly anticipated before its discovery

### Grant BJ, Lukman S, Hocker HJ, Sayyah J, Brown JH, McCammon JA, Gorfe AA (2011)

_Novel allosteric sites on Ras for lead generation._ PLoS ONE 6(10):e25711.
doi:10.1371/journal.pone.0025711. PMID 22046245. PMCID PMC3201956. Open access.

The most consequential precedent found. Published **two years before** Ostrem 2013 discovered
the S-IIP experimentally.

`[VERIFIED-FULLTEXT]` Starting structure: _"Simulations of K-Ras were carried out with bound
Mg2+GTP and Mg2+GDP, both modeled from a high-resolution crystal structure of K-Ras (PDB code
**2PMX**)."_

`[VERIFIED-FULLTEXT]` Method: _"Three independent 20 ns production runs with different initial
velocities were carried out on each system resulting in a cumulative simulation time of 120 ns."_
Pocket detection by three schemes on the resulting ensemble — FTMAP (fragment), AutoLigand
(grid), BlindDock (ligand).

`[VERIFIED-FULLTEXT]` Table 1 residue compositions, exactly as printed:

| Pocket | Residues                           | Location      | Mean volume (Å³) |
| ------ | ---------------------------------- | ------------- | ---------------- |
| p1     | `5–7,39,54–56, 67, 70–75`          | β1–3 and α2   | 112              |
| p2     | `61–65, 90–99`                     | L2, α2 and α3 | 143.6            |
| p3     | `97,101,107–111, 136–140, 161–166` | lobe2         | 173              |
| p3b    | `75–78,104,106–110, 162–166`       | —             | 36               |
| p4     | `24–40, 17, 21, 57`                | —             | 139.9            |

`[VERIFIED-FULLTEXT]` _"Residues from α2 and β-strands 1–3 (in lobe1) line p1, whilst p2 lies
between helices α2 and α3 at the interface between the two lobes."_

`[VERIFIED-FULLTEXT]` _"This includes pockets p1 and p2 that reside on either side of the highly
mobile helix α2."_

`[VERIFIED-FULLTEXT]` _"These nucleotide-associated displacements effectively link the
conformations of p1 and p2 to that of the nucleotide-binding site."_

`[VERIFIED-FULLTEXT]` _"However, pocket p3 is observed in all ensemble conformers in contrast to
pockets p1 and p2 that are inaccessible in some members of the ensemble."_

`[VERIFIED-FULLTEXT]` _"The most distal non active site pocket, p3, resides in lobe2
approximately 25 Å from the nucleotide-binding site."_

**Why this matters, and the trap.** `[UNVERIFIED]` p2's residue set (61–65 covers E62/E63/Y64/S65;
90–99 covers H95/Y96/Q99) overlaps the region later named the switch-II pocket. The paper never
uses the phrase "switch-II pocket" — the name did not exist yet. **Do not claim Grant 2011
"predicted the S-IIP" in the report without first computing the coordinate overlap between p2 as
printed above and our own holo-derived S-IIP label set.** If the overlap is high, this is the
single strongest cautionary tale in the benchmark: a 120 ns classical MD run with off-the-shelf
pocket finders already reached the answer, and our method must clear that bar without MD (C2).
If the overlap is low, p2 is a different pocket and the precedent weakens.

**[RE-CHECK]** The Table 1 residue strings above.

### Vithani N, Zhang S, Thompson JP, et al., LeBard DN (2024)

_Exploration of Cryptic Pockets Using Enhanced Sampling Along Normal Modes: A Case Study of
KRAS G12D._ J Chem Inf Model. doi:10.1021/acs.jcim.4c01435. PMID 39419500. PMCID PMC11558672.
Open access.

`[VERIFIED-FULLTEXT]` **Starting structure is 4OBE, and they use it as the wild-type structure**:
_"We chose the KRASWT structure from PDB ID: **4OBE**"_ and _"The crystal structure of the
KRASWT:GDP complex (Protein Data Bank (PDB) ID: **4OBE**) is shown"_.

This independently corroborates the repo's structural audit finding that `4OBE` is **wild-type
KRAS, not G12C** (`docs/targets.md`). The field treats 4OBE as the canonical WT:GDP reference.

`[VERIFIED-FULLTEXT]` Reference/holo structures: `7RPZ` (_"KRASG12D:GDP complex ... with
MRTX1133 bound at the Switch-II pocket"_), `7RT1` (_"bound to an analog of MRTX1133 (Compound 15)
in the Switch-I/II pocket"_), `5XCO` (_"KRASG12D-peptide inhibitor complex"_).

`[VERIFIED-FULLTEXT]` Method: weighted-ensemble MD using anisotropic network model normal modes
as progress coordinate — _"the ANM is constructed from all Cα atoms ... using ProDy, from which a
set of normal modes can be derived from the Hessian matrix"_, projecting _"the top one or two most
collective of the slowest normal modes as a progress coordinate in our WE simulations"_ (ANM modes
14 and 15). Cumulative sampling >400 μs (per Zhang & Bowman 2026, below).

`[VERIFIED-FULLTEXT]` Result: _"One of the sites identified by the exposon methodology is lined
with residues that form the **Switch-II cryptic pocket** where MRTX1133 [binds]"_, and
_"Xenon-binding cluster-1 overlaps with C7-naphthyl group of MRTX1133 and Adagrasib, both of
which occupy a deep hydrophobic subpocket in the Switch-II binding site."_

`[VERIFIED-FULLTEXT]` **No benchmark comparison.** The extraction found no comparison against
PocketMiner, CryptoSite, fpocket or P2Rank. So this is a positive control with no reported
rank, AUC or enrichment number — it says "we found it", not "we found it at rank _k_".

**Status: positive control, no scoreable metric.**

### Buhrman G, O'Connor C, Zerbe B, et al., Vajda S, Kozakov D, Kovrigin EL, Mattos C (2011)

_Analysis of binding site hot spots on the surface of Ras GTPase._ J Mol Biol 413(4):773–789.
doi:10.1016/j.jmb.2011.09.011. PMID 21945529.

`[VERIFIED-ABSTRACT]` Multiple-solvent crystal structures plus computational mapping:
_"Thirteen sites are revealed, expanding possible target sites for ligand binding well beyond the
active site."_ No per-site rank retrieved; no statement that any of the 13 is the S-IIP.

### Mansoor S, Baek M, Park H, Lee GR, Baker D (2024)

_Protein Ensemble Generation Through Variational Autoencoder Latent Space Sampling._
J Chem Theory Comput. doi:10.1021/acs.jctc.3c01057. PMID 38547871. PMCID PMC11008089.

`[VERIFIED-ABSTRACT]` VAE trained on K-Ras crystal structures and MD snapshots; sampling accurate
_"within 1 Å of withheld structures, successfully recapitulating cryptic pockets for molecular
docking."_ Note this trains on MD — out of bounds for our prediction path under C2, but a valid
external bar.

### Zhang S, Bowman GR (2026)

_Decrypting cryptic pockets with physics-based simulations and artificial intelligence._
Curr Opin Struct Biol 90:103215. doi:10.1016/j.sbi.2025.103215. PMID 41604887. PMCID PMC12959236.
Open access.

`[VERIFIED-FULLTEXT]` _"the discovery of a hidden switch-II pocket in KRAS G12C led to the
development of two Food and Drug Administration—approved covalent inhibitors, AMG 510 and
MRTX849"_ and _"These compounds selectively bind to cysteine 12 within a cryptic site."_

`[VERIFIED-FULLTEXT]` _"Leveraging over 400 μs of simulation data, the authors conducted
comprehensive analyses of cryptic pockets in both KRAS and its G12D mutant."_

`[VERIFIED-FULLTEXT]` Method benchmarks quoted: PocketMiner _"achieves slightly higher accuracy,
as measured by the area under the receiver operating characteristic curve (ROC-AUC: 0.87 vs.
0.85), while offering over 1000-fold faster prediction speed"_ vs CryptoSite, which requires
_"approximately one day per input structure"_. BioEmu _"successfully recovered 86 % of holo
structures"_ but _"only 56 % accurately predicted"_ apo conformations.

### What was NOT found for KRAS

Searched and found **no** paper that reports a rank, score or AUC for the switch-II pocket from a
general-purpose predictor. Specifically:

- **PocketMiner** (Meller 2023, PMC9977097): `[VERIFIED-FULLTEXT]` extraction found **no mention
  of KRAS, Ras, ABL, Abl kinase, myosin or mavacamten** anywhere in the paper.
- **CryptoBench** (Škrhák 2024, PMC11725321): `[VERIFIED-FULLTEXT]` _"No mentions found of KRAS,
  RAS, ABL, myosin, or specific kinase targets."_
- **CrypToth** (Koseki 2025, PMC12152933): `[VERIFIED-FULLTEXT]` its nine targets are TIE-2
  (1FVR/2OO8), Exodeoxyribonuclease I (1FXX/3HL8), TEM β-lactamase (1JWP/1PZO), NPC2 (1NEP/2HKA),
  androgen receptor (2AM9/2PIQ), DHFR Tn4003 (2W9T/2W9S), ferulic acid decarboxylase (3NX1/3NX2),
  fascin (3P53/6I11), anti-methotrexate VHH (3QXW/3QXV). **KRAS, Ras, ABL and myosin absent.**
- **CryptoSite** (Cimermancic 2016, PMC4794384): full-text XML returned **HTTP 404**; could not
  check its dataset for KRAS.

## 1.2 ABL1 myristoyl pocket — no blind prediction attempt found. This is a real gap.

**I searched for, and did not find, any published attempt to _discover_ the ABL1 myristoyl pocket
from a myristate-free structure.** Queries run:

- `"allosteric site" AND prediction AND "Abl" AND (myristoyl OR myristate)` — 45 hits, none is a
  blind-prediction study on this pocket
- `(myristate OR myristoyl) AND pocket AND Abl AND ("C-lobe" OR "alphaI" OR "helix I")` — 159 hits,
  all mechanism/pharmacology
- `"myristoyl pocket" AND (cryptic OR "induced fit" OR preformed OR "pre-formed")` — 24 hits, none
  reports prediction
- `"GNF-2" OR "GNF-5" AND Bcr-Abl allosteric myristate` — 62 hits, all discovery-by-screening

The pocket was found **experimentally**, by crystallography of the myristoylated protein
(Nagar 2003) and by cell-based screening (Zhang 2010), not by prediction. Absence of prior art here
is itself a result: **target 2 has never been used as a prediction benchmark.**

The nearest published bar is a class-level number, not a target-level one:

### Riedlová K, Škrhák V, Gatlin WG, et al., Hoksza D, Verkhivker GM (2026)

_Predicting and Decoding Allosteric Binding Sites Using Protein Language Models and Structure-Based
Machine Learning: An Energy Landscape-Guided Explainable AI Framework._ J Chem Theory Comput.
doi:10.1021/acs.jctc.6c00427. PMID 42093179. PMCID PMC13217555. Open access.

`[VERIFIED-FULLTEXT]` Benchmark: _"we benchmarked this fine-tuned PLM alongside the structure-based
method P2Rank for the detection of orthosteric and allosteric sites in protein kinases using
Kinase Conformation Resource (KinCoRe)"_ — fine-tuned ESM2-650M vs P2Rank v2.5, 453 human kinases,
10,301 complexes.

`[VERIFIED-FULLTEXT]` The myristoyl pocket is the **Type IV** class: _"the well-characterized
myristoyl pocket in the C-lobe (Type IV)"_.

`[VERIFIED-FULLTEXT]` Performance by class:

| Site class                                              | AUROC     | AUPR                            |
| ------------------------------------------------------- | --------- | ------------------------------- |
| Type I (orthosteric)                                    | 0.968     | 0.629–0.749 (orthosteric range) |
| Type I.5 (orthosteric)                                  | 0.975     | ”                               |
| Type II (orthosteric)                                   | 0.941     | ”                               |
| Type III (allosteric)                                   | 0.910     | 0.363                           |
| **Type IV / ALLO (allosteric, incl. myristoyl pocket)** | **0.676** | **0.077**                       |

`[VERIFIED-ABSTRACT]` _"Orthosteric pockets are located in minimally frustrated basins that
generate strong evolutionary and structural signatures, whereas allosteric pockets occupy
predominantly neutrally frustrated zones associated with conformational plasticity and reduced
evolutionary constraint."_ Abstract also: _"allosteric sites are detected with substantially lower
confidence"_.

**Bar for target 2: AUPR 0.077 for the myristoyl-pocket class.** `[VERIFIED-FULLTEXT]` the paper
gives no per-target ABL1 number.

**Leakage warning for any ML baseline on target 2.** `[VERIFIED-FULLTEXT]` ASD (Liu 2020 NAR)
curates the BCR-ABL myristoyl site: _"single point mutations (A337V, P465S, V468F, and I502L) at
the allosteric myristoyl binding site in the C-lobe of BCR-ABL kinase cause insensitivity to the
allosteric inhibitor ABL001 in chronic myeloid leukemia."_ PASSer / PASSer2.0 / PASSerRank are
trained and evaluated on ASD. **A PASSer-family baseline is not blind on this target** and any
comparison must say so.

## 1.3 Mavacamten site — no prediction attempt found; the one AI study deliberately started holo

**No published attempt to predict this site from an apo structure was found.** Queries:
`"mavacamten" AND (docking OR "virtual screening" OR "binding site prediction")` (50 hits);
`"mavacamten" AND "binding pocket" AND (Tyr164 OR His666 OR "transducer")` (16 hits);
`mavacamten AND (crystal structure OR cryo-EM) AND (binding site OR residues)` (54 hits).

### Parijat P, et al. (2023) — the closest thing, and a cautionary tale

_Discovery of a novel cardiac-specific myosin modulator using artificial intelligence-based virtual
screening._ Nat Commun 14:7692. doi:10.1038/s41467-023-43538-y. PMID 38001148. PMCID PMC10673995.
Open access.

`[VERIFIED-FULLTEXT]` Site chosen, not predicted: _"The OM-binding site is solvent accessible and
at sufficient distance to both the ATP- and actin-binding sites, making it an ideal target for the
AI-based virtual screen for an allosteric effector."_

`[VERIFIED-FULLTEXT]` **They used a holo template on purpose**: they _"chose the nucleotide
free-structure of human β-cardiac myosin bound to Omecamtiv Mecarbil (OM; PDB entry **4PA0**) as
the starting template"_ because _"Holo-structures of protein-ligand complexes are preferred targets
over protein apo structures."_

This is direct evidence that practitioners working on this exact pocket did not consider an apo
structure usable. It supports the crypticity finding in §3.3 and it is the clearest statement in
the retrieved literature that the mavacamten/OM site is hard from apo.

`[VERIFIED-FULLTEXT]` Their docking-grid residues: _"A91, M92, T94, L96, S118, G119, F121, F489,
M493, E497, V698, G701, I702, C705, P710, N711, and R712"_.

### Meller A, Lotthammer JM, Smith LG, et al., Greenberg MJ, Bowman GR (2023)

_Drug specificity and affinity are encoded in the probability of cryptic pocket opening in myosin
motor domains._ eLife 12:e83602. doi:10.7554/eLife.83602. PMID 36705568. PMCID PMC9995120.

The only cryptic-pocket study of myosin motor domains — **and it is about the blebbistatin pocket,
not the mavacamten pocket.**

`[VERIFIED-FULLTEXT]` _"Recently, the myosin inhibitor, mavacamten, received FDA approval for the
treatment of symptomatic obstructive hypertrophic cardiomyopathy."_ — the only mavacamten mention.
Extraction: _"No binding site or mechanism for mavacamten is discussed."_

`[VERIFIED-FULLTEXT]` _"It has previously been suggested that blebbistatin binds at a 'cryptic'
pocket that is usually closed in crystal structures of myosins without a bound blebbistatin."_ and
_"All known blebbistatin-free experimental structures of the myosin motor domain have a closed
blebbistatin pocket."_ Blebbistatin pocket residues named: Y269, L270, F657.
`[VERIFIED-ABSTRACT]` Markov state models; docking against MSMs predicted affinities with R²=0.82;
blind prediction for Myh7b agreed with experimental IC50.

Isoforms covered: MYH2, **MYH7**, MYH9, MYH11, myosin-V, myosin-Ib, myosin-X, Myh7b. Structures
cited: 1YV3, 5N6A, 1BR2, 5I0H, 5I4E, 6FSA, 3MJX, 3BZ8, 3BZ7, 3BZ9, 3MYK, 3MYH, 6Z7U, 6YSY.

**Implication for us:** the Bowman group has already demonstrated MSM-based cryptic pocket
prediction on MYH7 — for a _different_ pocket. That is both a methodological precedent and an
opportunity: the mavacamten pocket on MYH7 is unclaimed.

## 1.4 Classical baselines the submission must report against

These are the numbers a reviewer will hold us to. None of them was measured on our three targets,
which is itself worth saying in the report.

| Method                                                                                | Reference                                                                                                                                                                                                                                                                                                          | Reported performance                                                                                                                                                                                            | Tag                   |
| ------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------- |
| **Ohm** — structure-based allosteric pathway network, **no simulation required**      | Wang J, Jain A, McDonald LR, Gambogi C, Lee AL, Dokholyan NV. Nat Commun 2020;11:3862. doi:10.1038/s41467-020-17618-2. PMID 32737291                                                                                                                                                                               | _"a structure-based network approach for identifying allosteric communication pathways without simulations, validated against experimentally confirmed allosteric proteins and NMR data"_                       | `[VERIFIED-ABSTRACT]` |
| **Bond-to-bond propensity** — atomistic energy-weighted graph, active-site-referenced | Amor BR, Schaub MT, Yaliraki SN, Barahona M. Nat Commun 2016;7:12477. doi:10.1038/ncomms12477. PMID 27561351. PMC5007447                                                                                                                                                                                           | _"The allosteric site is detected significantly by at least one of the four measures in 19 out of 20 proteins in the test set, and is detected by three or more of the four measures in 15 out of 20 proteins"_ | `[VERIFIED-FULLTEXT]` |
| **APOP** — ENM pocket stiffening                                                      | Kumar A, Kaynak BT, Dorman KS, Doruker P, Jernigan RL. Bioinformatics 2023;39(5):btad275. doi:10.1093/bioinformatics/btad275. PMID 37115636                                                                                                                                                                        | _"Out of the 104 test cases, APOP predicts known allosteric pockets for 92 within the top 3"_ (88 % top-3)                                                                                                      | `[VERIFIED-ABSTRACT]` |
| **ESSA** — essential site scanning, ENM                                               | Kaynak BT, Bahar I, Doruker P. CSBJ 2020;18:1577. doi:10.1016/j.csbj.2020.06.020. PMID 32637054                                                                                                                                                                                                                    | enrichment among allosteric sites, hinge regions, binding pockets; no headline number retrieved                                                                                                                 | `[VERIFIED-ABSTRACT]` |
| **PRS** — perturbation-response scanning                                              | Atilgan C, Gerek ZN, Ozkan SB, Atilgan AR. Biophys J 2010;99:933. doi:10.1016/j.bpj.2010.05.020. PMID 20682272 (25 proteins); Gerek ZN, Ozkan SB. PLoS Comput Biol 2011;7:e1002154. doi:10.1371/journal.pcbi.1002154                                                                                               | no headline number retrieved                                                                                                                                                                                    | `[VERIFIED-ABSTRACT]` |
| **Reversed allosteric communication**                                                 | Ni D, Wei J, He X, et al., Zhang J. Chem Sci 2020. doi:10.1039/d0sc05131d. PMID 34163609                                                                                                                                                                                                                           | MD + MSM + mutagenesis; novel cryptic allosteric sites in Sirt6                                                                                                                                                 | `[VERIFIED-ABSTRACT]` |
| **Reverse perturbation (Berezovsky)**                                                 | Tee WV, Guarnera E, Berezovsky IN. PLoS Comput Biol 2018;14:e1006228. doi:10.1371/journal.pcbi.1006228. PMID 29912863                                                                                                                                                                                              | reveals known and latent regulatory regions                                                                                                                                                                     | `[VERIFIED-ABSTRACT]` |
| **PASSer**                                                                            | Tian H, Jiang X, Tao P. Mach Learn Sci Technol 2021;2:035015. doi:10.1088/2632-2153/abe6d6. PMID 34396127                                                                                                                                                                                                          | 84.9 % top-3                                                                                                                                                                                                    | `[VERIFIED-ABSTRACT]` |
| **PASSer2.0**                                                                         | Xiao S, Tian H, Tao P. Front Mol Biosci 2022;9:879251. doi:10.3389/fmolb.2022.879251. PMID 35898310                                                                                                                                                                                                                | _"82.7% of allosteric pockets appearing among the top three positions"_                                                                                                                                         | `[VERIFIED-ABSTRACT]` |
| **PASSerRank**                                                                        | Tian H, Xiao S, Jiang X, Tao P. J Comput Chem 2023. doi:10.1002/jcc.27193. PMID 37561047                                                                                                                                                                                                                           | 83.6 % top-3 on ASD                                                                                                                                                                                             | `[VERIFIED-ABSTRACT]` |
| **CryptoSite**                                                                        | Cimermancic P, Weinkam P, Rettenmaier TJ, et al. J Mol Biol 2016;428:709. doi:10.1016/j.jmb.2016.01.029. PMID 26854760                                                                                                                                                                                             | 73 % TPR / 29 % FPR; ROC-AUC 0.85 (per Zhang & Bowman 2026); _"increases the size of the potentially druggable human proteome from ~40% to ~78% of disease-associated proteins"_                                | `[VERIFIED-ABSTRACT]` |
| **PocketMiner**                                                                       | Meller A, Ward M, Borowsky J, et al., Bowman GR. Nat Commun 2023;14:1177. doi:10.1038/s41467-023-36699-3. PMID 36859488. PMC9977097                                                                                                                                                                                | _"ROC AUC: 0.87"_; vs CryptoSite _"0.87 for PocketMiner vs. 0.85 for CryptoSite"_; >1000× faster                                                                                                                | `[VERIFIED-FULLTEXT]` |
| **On CryptoBench** (the honest numbers)                                               | Škrhák V, Novotný M, Feidakis CP, Krivák R, Hoksza D. Bioinformatics 2024;40:btae745. doi:10.1093/bioinformatics/btae745. PMID 39693053. PMC11725321                                                                                                                                                               | PocketMiner AUC 0.76 / **AUPRC 0.19**; P2Rank-apo AUC 0.81 / **AUPRC 0.21**; P2Rank-holo AUC 0.89 / **AUPRC 0.34**                                                                                              | `[VERIFIED-FULLTEXT]` |
| **SWISH** — Hamiltonian replica exchange + probes                                     | Oleinikovas V, Saladino G, Cossins BP, Gervasio FL. JACS 2016;138:14257. doi:10.1021/jacs.6b05425. PMID 27726386; Comitani F, Gervasio FL. JCTC 2018. doi:10.1021/acs.jctc.8b00263. PMID 29768914; SWISH-X: Borsatto A, Gianquinto E, Rizzi V, Gervasio FL. JCTC 2024. doi:10.1021/acs.jctc.3c01318. PMID 38563746 | SWISH targets: NPC2, p38α, LfrR, hPNMT. **KRAS, ABL, myosin not among them**                                                                                                                                    | `[VERIFIED-ABSTRACT]` |
| **CrypToth** — mixed-solvent MD + topological data analysis                           | Koseki J, Motono C, Yanagisawa K, et al. JCIM 2025. doi:10.1021/acs.jcim.4c02111. PMID 40404166. PMC12152933                                                                                                                                                                                                       | _"In seven of nine cases, hotspots associated with cryptic sites were ranked the highest"_; _"CrypToth outperformed PocketMiner"_; PocketMiner top-3 in only 5/9, rank-1 in 2/9                                 | `[VERIFIED-FULLTEXT]` |
| **AlphaFold for cryptic pockets**                                                     | Meller A, Bhakat S, Solieva S, Bowman GR. JCTC 2023. doi:10.1021/acs.jctc.2c01189. PMID 36948209                                                                                                                                                                                                                   | _"AlphaFold samples open cryptic pocket states in 6 of 10 cases"_                                                                                                                                               | `[VERIFIED-ABSTRACT]` |

**The AUPRC column is the number that matters.** On a properly constructed apo/holo cryptic-site
benchmark, the best published methods sit at AUPRC 0.19–0.34. Anyone claiming cryptic-site
prediction is "solved classically" is quoting ROC-AUC on an easier split.

---

# 2. Which apo and holo structures the field actually uses

Checked against the specific IDs requested. "Not found" means: not present in any abstract or
full text retrieved in this session. It does not mean the ID is unused in the wider literature —
it means I have no session-sourced evidence for it and must not assert one.

## KRAS

| PDB        | Status                                                                                                                     | Evidence                                                                  |
| ---------- | -------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| **4OBE**   | **Recurs as the canonical WT:GDP reference.** Used as the MD starting structure by Vithani 2024                            | `[VERIFIED-FULLTEXT]` _"We chose the KRASWT structure from PDB ID: 4OBE"_ |
| **4LDJ**   | **NOT FOUND.** Ostrem 2013 full text (PMC4274051) returned HTTP 404, so I could not confirm which IDs that paper deposited | —                                                                         |
| **6OIM**   | **NOT FOUND** in any retrieved abstract or full text                                                                       | —                                                                         |
| 2PMX       | Grant 2011 MD starting structure                                                                                           | `[VERIFIED-FULLTEXT]`                                                     |
| 7RPZ       | G12D + MRTX1133, **Switch-II pocket**                                                                                      | `[VERIFIED-FULLTEXT]` (Vithani)                                           |
| 7RT1       | G12D + MRTX1133 analog, **Switch-I/II pocket**                                                                             | `[VERIFIED-FULLTEXT]` (Vithani)                                           |
| 5XCO       | G12D + peptide inhibitor                                                                                                   | `[VERIFIED-FULLTEXT]` (Vithani)                                           |
| 5US4, 7EW9 | screening template / pharmacophore reference in the quantum KRAS paper                                                     | `[VERIFIED-FULLTEXT]` (Ghazi Vakili 2025)                                 |
| 3K8Y       | h-Ras + substrate + allosteric activator, used by Amor 2016                                                                | `[VERIFIED-FULLTEXT]`                                                     |

## ABL1

| PDB                | Status                                                                                                                                                                              | Evidence                                                                                                                                                                                                     |
| ------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **1OPL**           | **NOT FOUND** in any retrieved full text. Nagar 2003 (PMID 12654251, Cell) is the autoinhibited c-Abl structure paper but is not open access and I could not retrieve its full text | `[VERIFIED-ABSTRACT]` for the paper: _"The N-terminal myristoyl modification of c-Abl 1b binds to the kinase domain and induces conformational changes that allow the SH2 and SH3 domains to dock onto it."_ |
| **1M52**           | **Recurs as the canonical myristate-free kinase domain.** Directly corroborates the repo audit's corrected-apo suggestion                                                           | `[VERIFIED-FULLTEXT]` Paladini 2024: _"Crystal structures of the isolated Abl kinase domain with an empty myristoyl binding pocket (PDB 1M52)"_                                                              |
| **2G2H**, **2G1T** | **NOT FOUND** in any retrieved text                                                                                                                                                 | —                                                                                                                                                                                                            |
| **5MO4**           | **NOT FOUND** in any retrieved text. Wylie 2017 (PMID 28329763) is the asciminib paper but has no PMCID and is not open access                                                      | —                                                                                                                                                                                                            |
| 2FO0               | myristoylated Abl 1b, residues 2–531                                                                                                                                                | `[VERIFIED-FULLTEXT]` Paladini: _"Crystal structure of the N-terminally myristoylated Abl 1b isoform (residues 2–531, PDB 2FO0)"_                                                                            |
| 2HYY               | A-loop inactive conformation reference                                                                                                                                              | `[VERIFIED-FULLTEXT]` Paladini                                                                                                                                                                               |

**Numbering convention, confirmed independently of the repo audit.** `[VERIFIED-FULLTEXT]`
Paladini et al. 2024 state flatly: _"Abl 1b numbering used throughout"_. The corpus does not share
a convention; it is declared per paper. This is exactly the hazard `docs/targets.md` recorded, and
it is now literature-backed.

## Cardiac myosin / MYH7

| PDB                                     | Status                                                                                                                                                                                                | Evidence                                                                                                                                            |
| --------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| **8ACT**                                | **Confirmed twice** as the experimental human β-cardiac myosin folded-back / IHM reference                                                                                                            | `[VERIFIED-FULLTEXT]` Somavarapu 2026: _"8ACT: WT human β-cardiac myosin IHM"_; McMillan 2026: _"PDB 8ACT ... folded-back state (IHM)"_, EMDB 15353 |
| **9GZ1**                                | IHM + mavacamten, EMD-51719. Deposited by McMillan 2026                                                                                                                                               | `[VERIFIED-FULLTEXT]`                                                                                                                               |
| **9GZ2**                                | motor domain + mavacamten (`MD_mava`), EMD-51720                                                                                                                                                      | `[VERIFIED-FULLTEXT]`                                                                                                                               |
| **9GZ3**                                | motor domain, **no mavacamten** (`MD`), EMD-51721                                                                                                                                                     | `[VERIFIED-FULLTEXT]`                                                                                                                               |
| **8QYP**, **8QYR**                      | **NOT FOUND** by ID. The deposition paper (Auguin 2024, PMID 38849353, doi:10.1038/s41467-024-47587-9) is not open access in Europe PMC; its bioRxiv preprint full text (PPR760230) returned HTTP 404 | `[VERIFIED-ABSTRACT]` only: _"both drugs target the same pocket and stabilize a pre-stroke structural state, with only few local differences"_      |
| 8QYQ                                    | bovine S1 cardiac myosin + mavacamten                                                                                                                                                                 | `[VERIFIED-FULLTEXT]` McMillan 2026                                                                                                                 |
| **5TBY**, **6C1H**                      | **NOT FOUND ANYWHERE.** Neither appears in any of the four myosin structure papers retrieved                                                                                                          | —                                                                                                                                                   |
| 9YOP / 9YRG / 9YP9 / 9YR7 / 9YP4 / 9YRH | Somavarapu 2026 depositions: WT docked/undocked, +mavacamten docked/undocked, +OM docked/undocked (EMD-73268/73367/73288/73362/73283/73368)                                                           | `[VERIFIED-FULLTEXT]`                                                                                                                               |
| **5N6A**                                | **`APO-MD-PPS` — drug-free pre-powerstroke motor domain.** New candidate apo reference, see §3.3                                                                                                      | `[VERIFIED-FULLTEXT]` Planelles-Herrero 2017                                                                                                        |
| 5N69                                    | `OM-S1-PPS`, OM-bound, same study as 5N6A                                                                                                                                                             | `[VERIFIED-FULLTEXT]`                                                                                                                               |
| 4PA0                                    | human β-cardiac myosin + OM, nucleotide-free (Winkelmann 2015)                                                                                                                                        | `[VERIFIED-FULLTEXT]` Parijat 2023                                                                                                                  |

**Findings that change the benchmark.**

1. `9GZ3 → 9GZ2` and `8ACT → 9GZ1` are confirmed by the depositing paper itself as
   same-construct pairs differing only by mavacamten. The repo's corrected pairing is
   literature-backed, not just coordinate-derived.
2. **`5N6A` is a genuine drug-free structure of the same pocket** (pre-powerstroke motor domain,
   solved alongside the OM-bound 5N69 by the same authors). It is a stronger apo candidate for a
   _cryptic_-pocket test than 9GZ3, because Planelles-Herrero explicitly report the pocket is
   incompletely formed in it (§3.3). Worth adding as a sensitivity arm. The tradeoff: 5N6A is not
   the mavacamten complex's own apo, so a label-transfer step is needed.
3. **The challenge's assigned myosin pair (`5TBY` → `6C1H`) has no literature footprint at all.**
   Zero retrieved papers mention either ID. That is consistent with, and independent of, the repo
   audit's conclusion that the pair is unscoreable.

---

# 3. Crypticity status of each pocket

## 3.1 KRAS switch-II pocket — cryptic, unambiguously, and stated in the discovery paper

**Ostrem JM, Peters U, Sos ML, Wells JA, Shokat KM (2013)** _K-Ras(G12C) inhibitors allosterically
control GTP affinity and effector interactions._ Nature 503:548–551. doi:10.1038/nature12796.
PMID 24256730. Cited 1970×.

`[VERIFIED-ABSTRACT]`, verbatim from the abstract retrieved this session:

> _"Efforts to target this oncogene directly have faced difficulties owing to its picomolar
> affinity for GTP/GDP and **the absence of known allosteric regulatory sites**."_

> _"Crystallographic studies reveal **the formation of a new pocket that is not apparent in
> previous structures of Ras**, beneath the effector binding switch-II region."_

> _"Our data provide structure-based validation of a **new allosteric regulatory site** on Ras that
> is targetable in a mutant-specific manner."_

Corroborating:

- `[VERIFIED-FULLTEXT]` Vithani 2024: _"the presence of an **allosteric cryptic pocket** in
  KRASG12C near the Switch-II region"_; _"A breakthrough occurred from a covalent fragment
  screening study conducted by the Shokat lab in 2013, which suggested the **presence of an
  allosteric cryptic pocket** in KRASG12C"_; _"the **Switch-II cryptic pocket**"_.
- `[VERIFIED-FULLTEXT]` Zhang & Bowman 2026: _"a **hidden** switch-II pocket in KRAS G12C"_;
  _"within a **cryptic site**"_.
- `[VERIFIED-ABSTRACT]` Mao Z, et al. Cell Discov 2022;8:5. doi:10.1038/s41421-021-00368-w.
  PMID 35075146: _"**inhibitor binding-induced** switch-II pocket in KRAS(G12D)"_.

**Verdict: genuinely cryptic. Target 1 is a valid cryptic-pocket discovery test.** This matches
the repo's own transplant test (`MOV` into the apo frame: 14 of 41 atoms clashing below 2.5 Å).

## 3.2 ABL1 myristoyl pocket — pre-formed. No source calls it cryptic.

**No retrieved source describes the ABL1 myristoyl pocket as cryptic, induced-fit, or hidden.**
A dedicated search (`"myristoyl pocket" AND (cryptic OR "induced fit" OR preformed OR
"pre-formed")`, 24 hits) returned nothing where those adjectives attach to this pocket.

Positive evidence that it is pre-formed:

- `[VERIFIED-FULLTEXT]` Paladini J, Maier A, Habazettl JM, Hertel I, Sonti R, Grzesiek S. eLife
  2024;13:e92324. doi:10.7554/eLife.92324. PMID 38588001. PMC11001296:
  _"Crystal structures of the isolated Abl kinase domain with an **empty myristoyl binding pocket**
  (PDB 1M52)"_ and _"The docking of the N-terminal myristoyl into **a hydrophobic cleft** at the
  bottom of the KD C-lobe."_
  The pocket is described as a cleft that exists and is empty — not one that forms on binding.
- `[VERIFIED-ABSTRACT]` Wylie AA, et al. Nature 2017;543:733. doi:10.1038/nature21702.
  PMID 28329763: _"ABL001 **binds to the myristoyl pocket** of ABL1 and **induces the formation of
  an inactive kinase conformation**."_ The induced change is to the **kinase conformation**, not to
  the pocket. Ligand binding reorganises the SH3/SH2/KD module; it does not open the cavity.
- `[VERIFIED-ABSTRACT]` Zhang J, Adrián FJ, Jahnke W, et al., Gray NS. Nature 2010;463:501.
  doi:10.1038/nature08675. PMID 20072125: _"GNF-2 binds to the **myristate-binding site** of Abl,
  leading to changes in the structural dynamics of the ATP-binding site."_
- `[VERIFIED-FULLTEXT]` Riedlová 2026 calls it _"the **well-characterized** myristoyl pocket in the
  C-lobe (Type IV)"_.
- `[VERIFIED-ABSTRACT]` Xie T, Saleh T, Rossi P, Miller D, Kalodimos CG. J Mol Biol
  2022;434:167349. doi:10.1016/j.jmb.2021.167349. PMID 34774565: _"Imatinib binds to a secondary,
  allosteric site located in the **myristoyl pocket** of Abl to function as an activator of kinase
  activity."_ A second, chemically unrelated ligand occupying the same cavity is further evidence
  the cavity is constitutively available.

**Verdict: allosteric but pre-formed. Target 2 tests allosteric-site ranking, not cryptic-pocket
discovery.** The report must state which of the two it is claiming.

**The decisive quantitative argument, now literature-backed.** `[VERIFIED-FULLTEXT]` CryptoBench's
published crypticity criterion is: _"A significant change is defined as a difference of at least
**2 Å RMSD** between the binding residues in the apo and holo forms."_ The repo's structural audit
measured **0.50 Å** Cα RMSD across the pocket lining for `1OPL` → `5MO4`. **By the field's own
published threshold, that pair does not qualify as a cryptic binding site — it misses by a factor
of four.** This is the cleanest citation available for the audit's conclusion.

## 3.3 Mavacamten site — "not completely formed" in the drug-free structure. Partially cryptic.

The decisive source is not a mavacamten paper. It is the omecamtiv mecarbil paper that solved both
the drug-bound and drug-free forms of the same pocket.

**Planelles-Herrero VJ, Hartman JJ, Robert-Paganin J, Malik FI, Houdusse A (2017)** _Mechanistic and
structural basis for activation of cardiac myosin force production by omecamtiv mecarbil._
Nat Commun 8:190. doi:10.1038/s41467-017-00176-5. PMID 28775348. PMC5543065. Open access.

`[VERIFIED-FULLTEXT]` Structures deposited: **5N69** (`OM-S1-PPS`) and **5N6A** (`APO-MD-PPS`).

`[VERIFIED-FULLTEXT]` **[RE-CHECK]** The key sentence:

> _"Comparison of the structures with and without drug bound reveals that **the OM-binding pocket
> is actually not completely formed in the APO-MD-PPS structure**"_

`[VERIFIED-FULLTEXT]` And on novelty:

> _"OM binds in a **previously unseen pocket** of the motor, which we call the 'PPS' allosteric
> site ... OM is at the center of a network of interactions between the N terminus, the relay
> helix, and the converter domain"_

Same pocket as mavacamten: `[VERIFIED-ABSTRACT]` Auguin D, Robert-Paganin J, Réty S, et al.,
Houdusse A. Nat Commun 2024;15:2903. doi:10.1038/s41467-024-47587-9. PMID 38849353 — title:
_"Omecamtiv mecarbil and Mavacamten target the same myosin pocket despite opposite effects in
heart contraction"_; abstract: _"both drugs **target the same pocket** and stabilize a pre-stroke
structural state, with only few local differences."_

Indirect corroboration: `[VERIFIED-FULLTEXT]` Parijat 2023 chose a holo template because
_"Holo-structures of protein-ligand complexes are preferred targets over protein apo structures."_

Negative finding worth recording: `[VERIFIED-FULLTEXT]` **neither** McMillan 2026 **nor**
Somavarapu 2026 — the two 2026 cryo-EM papers that define the mavacamten site — makes any
statement about the pocket being pre-formed, cryptic, or induced. The crypticity claim rests
entirely on Planelles-Herrero 2017.

**Verdict: partially cryptic ("not completely formed" in apo), with a single primary source.**
Target 3 is a weaker cryptic-pocket test than target 1 and a stronger one than target 2. State
this explicitly rather than lumping all three together.

---

# 4. Published allosteric-site residue definitions — as stated, not harmonised

## 4.1 KRAS switch-II pocket

**No primary-literature residue list was retrieved this session.** Ostrem 2013's full text was not
retrievable (PMC4274051 → HTTP 404). What was retrieved:

- `[VERIFIED-ABSTRACT]` Ostrem 2013 locates it only qualitatively: _"beneath the effector binding
  switch-II region"_, and states binding _"disrupts both switch-I and switch-II"_.
- `[VERIFIED-FULLTEXT]` Grant 2011 pocket p2, the only complete enumeration retrieved for that
  region, printed exactly as: **`61–65, 90–99`**, location `L2, α2 and α3`. **The paper does not
  call this the switch-II pocket.**
- `[VERIFIED-ABSTRACT]` Awad MM, Liu S, Rybkin II, et al. N Engl J Med 2021;384:2382.
  doi:10.1056/NEJMoa2105281. PMID 34161704 — resistance positions implicating the pocket:
  _"Acquired KRAS alterations included G12D/R/V/W, G13D, Q61H, R68S, **H95D/Q/R**, **Y96C**, and
  high-level amplification of the KRASG12C allele."_
- `[VERIFIED-ABSTRACT]` Tanaka N, Lin JJ, Li C, et al. Cancer Discov 2021;11:1913.
  doi:10.1158/2159-8290.CD-21-0365. PMID 33824136 — _"a novel **Y96D** mutation affecting the
  switch-II pocket that impairs drug binding"_.

**Action:** the S-IIP label set must come from coordinates (holo transplant + 4.5 Å cutoff), as
`docs/targets.md` already mandates. There is no clean published list to cross-check against.
Grant's `61–65, 90–99` and the resistance positions H95/Y96 are the only external anchors.

## 4.2 ABL1 myristoyl pocket

**No residue list retrieved this session.** The only residue numbers found:

- `[VERIFIED-FULLTEXT]` ASD (Liu X, Lu S, Song K, et al. Nucleic Acids Res 2020;48:D394.
  doi:10.1093/nar/gkz958. PMID 31665428): _"single point mutations (**A337V, P465S, V468F, and
  I502L**) at the allosteric myristoyl binding site in the C-lobe of BCR-ABL kinase cause
  insensitivity to the allosteric inhibitor ABL001 in chronic myeloid leukemia."_
  **The numbering convention is not stated in that sentence.** This is precisely the 1a/1b hazard
  the repo flagged — a residue list published without its convention is unusable.
- `[VERIFIED-ABSTRACT]` Batar P, Mezei G, Illes A. Curr Oncol 2025;32:97.
  doi:10.3390/curroncol32020097. PMID 39996897 — **A337V** as a treatment-emergent
  myristoyl-binding-pocket mutation.
- `[VERIFIED-FULLTEXT]` Paladini 2024 names **E528** (αI-helix, explicitly Abl 1b numbering) and
  **R479** as a salt-bridge pair — these are αI-helix residues, **not** pocket lining.

**Action:** derive from coordinates. Do not adopt A337V/P465S/V468F/I502L into any label set until
the convention is resolved per entry.

## 4.3 MYH7 mavacamten site — three independent lists, reported exactly as published

**(a) Somavarapu AK, Ge J, Yengo CM, Craig R, Padron R (2026)** _Cryo-EM reveals how cardiomyopathy
therapeutic drugs modulate the myosin motors of the heart._ Sci Adv. doi:10.1126/sciadv.aed6472.
PMID 42054467. PMC13127576.

`[VERIFIED-FULLTEXT]`

> _"Within 4 Å of each ligand, key interacting residues included **N711, R712, I713, L770, E774,
> R721, Y722, T167, D168, Y164, and H666**."_

> _"Among these, the side chains of D168 (negatively charged) and N711 (polar), along with the
> backbone amide nitrogen of R712, formed direct hydrogen bonds with both ligands."_

> _"The more elongated OM extended to reach **H492** and **E497** on the relay helix at one end and
> **K146** at the other end."_

Pocket location: _"located between the converter region and the upper 50-kDa domain"_;
_"predominantly hydrophobic, engaging broadly conserved residues with nonpolar side chains"_.

**(b) McMillan SN, Pitts JRT, Barua B, Winkelmann DA, Scarff CA (2026)** _Mavacamten inhibits myosin
activity by stabilizing the myosin interacting-heads motif and stalling motor force generation._
Sci Adv. doi:10.1126/sciadv.aea9335. PMID 42054462. PMC13127578.

`[VERIFIED-FULLTEXT]`

> _"The mavacamten-protein interactions are predominantly hydrophobic, formed by the sidechain
> backbones of residues **Arg721, Leu770 (L770), and Iso713** on the converter with isopropyl
> pyrimidinedione, methylethyl ester, and phenyl moieties of mavacamten ... as well as **His666**
> on the L50 subdomain and **Thr67** on the U50 subdomain with the isopropyl pyrimidinedione and
> phenyl moieties."_

> _"These hydrophobic contacts are supported by an ionic interaction between **Tyr164** (Y164) on
> the U50 subdomain and the isopropyl pyrimidinedione moiety and hydrogen bonding between
> **Asn711** (N711), the backbone of **Arg712** (R712) from the converter, and **Asp168** from the
> U50 subdomain to the isopropyl pyrimidinedione and methylethyl ester moieties."_

> _"This allows formation of a salt bridge between **Asp778** (D778) and **Lys146** (K146),
> creating additional communication between the lever and U50 subdomain."_

**Disagreement, recorded not fixed:** McMillan prints **"Thr67 on the U50 subdomain"** where
Somavarapu and Planelles-Herrero both print **T167**. Almost certainly a typesetting error for
Thr167, but reported here as published. **Resolve from coordinates, never from the paper.**

**(c) Planelles-Herrero et al. (2017)** — same pocket, omecamtiv mecarbil.

`[VERIFIED-FULLTEXT]`

> _"In the PPS state, OM binding involves extensive interactions with the N-terminal subdomain
> (**K146, R147, N160, Q163, Y164, T167, and D168**), the relay helix (**H492**), the extremity of
> the third beta-strand of the transducer (**H666**), and the converter (**P710, N711, R712, I713,
> R721, Y722, F765, L770, and E774**)"_

**(d) Parijat et al. (2023)** — docking grid for the OM pocket.

`[VERIFIED-FULLTEXT]` _"**A91, M92, T94, L96, S118, G119, F121, F489, M493, E497, V698, G701, I702,
C705, P710, N711, and R712**"_

### Cross-study agreement and disagreement

**Named by all three structural studies (a), (b), (c):** Y164, T167 (printed "Thr67" in (b)), D168,
H666, N711, R712, I713, R721, Y722, L770, E774 — **eleven residues.**

This matches the repo's coordinate-derived set (Tyr164, Thr167, Asp168, His666, Pro710, Asn711,
Arg712, Ile713, Glu774, plus Arg721, Tyr722, Leu770) with one difference: **Pro710** appears in
(c) and (d) but is not named among mavacamten contacts in (a) or (b).

**Disagreements, all real and all worth preserving:**

1. (c) and (d) include N-terminal-subdomain residues (K146, R147, N160, Q163 / A91, M92, T94, L96,
   S118, G119, F121) that (a) and (b) do not name for mavacamten.
2. (a) explicitly attributes K146, H492 and E497 to **OM's greater length**, not to mavacamten.
3. **The OM footprint is therefore larger than the mavacamten footprint in the same pocket.** A
   benchmark that scores against "the OM/mavacamten pocket" as one set will over-count for
   mavacamten. Use the mavacamten ligand for mavacamten labels.

---

# 5. Active-site definitions and pocket-to-active-site distances

## KRAS

Active site: the guanine nucleotide (GDP/GTP · Mg²⁺) site.

**No published S-IIP-to-nucleotide distance was retrieved.** The only Ras distance found:
`[VERIFIED-FULLTEXT]` Grant 2011: _"The most distal non active site pocket, p3, resides in lobe2
approximately **25 Å** from the nucleotide-binding site."_ — and p3 is **not** the S-IIP.

`[VERIFIED-ABSTRACT]` Ostrem 2013 places the pocket _"beneath the effector binding switch-II
region"_ and reports that binding _"disrupts both switch-I and switch-II"_.

**Consequence for our method, and it is not a small one.** The S-IIP is adjacent to and
conformationally coupled with the nucleotide site — switch I and switch II _are_ the nucleotide
sensor. `[VERIFIED-FULLTEXT]` Grant 2011 says the same of p1 and p2: _"These nucleotide-associated
displacements effectively link the conformations of p1 and p2 to that of the nucleotide-binding
site."_ **The S-IIP is a near-active-site allosteric pocket, not a distal one.** Any scoring rule
that rewards _distal_ dynamic connectivity will behave differently on target 1 than on targets 2
and 3. Report per-target distance distributions before interpreting any cross-target comparison.

## ABL1

Active site: the ATP site in the cleft between kinase N- and C-lobes.

**No published myristoyl-pocket-to-ATP-site distance was retrieved.** Functional coupling is
well documented:

- `[VERIFIED-ABSTRACT]` Zhang 2010: _"GNF-2 binds to the myristate-binding site of Abl, leading to
  changes in the structural dynamics of the ATP-binding site."_
- `[VERIFIED-ABSTRACT]` Skora L, Mestan J, Fabbro D, Jahnke W, Grzesiek S. PNAS 2013;110:E4437.
  doi:10.1073/pnas.1314712110. PMID 24191057 — _"NMR reveals the allosteric opening and closing of
  Abelson tyrosine kinase by ATP-site and myristoyl pocket inhibitors"_; _"The combination of
  imatinib with the allosteric inhibitor GNF-5 restores the closed, inactivated state."_
- `[VERIFIED-FULLTEXT]` Riedlová 2026 classifies it as **Type IV**, i.e. outside the ATP cleft.

## MYH7

Active site(s): the ATPase/nucleotide site, and the actin-binding cleft.

**No numeric distance retrieved from any of the four myosin structure papers.** The only
geometric statement: `[VERIFIED-FULLTEXT]` Parijat 2023 — _"The OM-binding site is solvent
accessible and at **sufficient distance to both the ATP- and actin-binding sites**, making it an
ideal target for the AI-based virtual screen for an allosteric effector."_

`[VERIFIED-ABSTRACT]` McMillan 2026 describes the mechanism as _"reducing motor dynamics required
for actin-binding cleft closure"_ and _"stabilizing ADP.Pi binding"_ — coupled to both, distance
unstated.

**All three targets: the published record gives qualitative coupling, not distances. Our own
computed distances are the primary source and should be presented as such.**

---

# 6. Quantum approaches — the prior art is closer than comfortable

## 6.1 The one that matters

**Mohtashim SI, Sajjan M, Kais S (2026)** _Continuous-Time Quantum-Walk Centrality for Protein
Residue Interaction Networks._ J Am Chem Soc 148(27):29206–29219. doi:10.1021/jacs.6c08053.
PMID 42361045. **Not open access.**

`[VERIFIED-ABSTRACT]` Full abstract, verbatim:

> _"We present a quantum-dynamical framework for identifying structurally and functionally
> important residues in proteins based on continuous-time quantum walks (CTQWs) on weighted
> residue-interaction networks constructed from experimentally resolved structures. By mapping the
> weighted adjacency matrix to a Hamiltonian, residue importance emerges from the long-time
> averaged occupation probability, confirmed analytically through its spectral decomposition.
> Across a data set of 150 proteins spanning diverse structural and functional classes, CTQW
> centrality exhibits consistently strong agreement with classical eigenvector centrality in
> identifying central residues, while extending beyond it through incorporating signatures of
> quantum interference. Analyzing the time-averaged quantum transition matrix reveals consistently
> larger spectral gaps than the classical random-walk operator. Furthermore, biological relevance
> is confirmed through recovery of experimentally established functional residues in proteins
> kinase A and oxytocin. CTQW-derived centrality rankings are accessible on near-term intermediate-
> scale quantum hardware, as we demonstrate through a proof-of-principle implementation on IBM
> superconducting quantum hardware. These results establish continuous-time quantum walks as a
> computationally tractable framework for protein network analysis, that connects network
> theoretical treatments of protein structural biology to continuous-time quantum walk dynamics."_

**This is, in method class, the challenge's own proposal — already published in JACS.** What is
_not_ claimed, and where our contribution has to live:

| They did                                                                   | They did not do                                                                        |
| -------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| CTQW on weighted residue-interaction networks from experimental structures | Rank residues **relative to a named active site** — theirs is unconditioned centrality |
| Validate on PKA and oxytocin, 150-protein set                              | Any apo/holo cryptic-pocket benchmark                                                  |
| Demonstrate on IBM superconducting hardware                                | KRAS, ABL1, myosin, or any allosteric-site prediction task                             |
| Report spectral-gap advantage over the classical random walk               | Show the ranking beats a classical baseline on a downstream task                       |

**The line that must be answered in our report:** _"CTQW centrality exhibits consistently strong
agreement with classical eigenvector centrality."_ By the authors' own account, on 150 proteins
the quantum method largely reproduces a cheap classical baseline. Our submission needs a stated,
tested regime where it does not — otherwise it is a reimplementation with a harder runtime.

They have also already set the C3/C4 bar by running on hardware. Reporting circuit depth, qubit
count and connectivity is now table stakes, not a differentiator.

## 6.2 Quantum + one of our targets, already published

**Ghazi Vakili M, Gorgulla C, Snider J, et al. (2025)** _Quantum-computing-enhanced algorithm
unveils potential KRAS inhibitors._ Nat Biotechnol. doi:10.1038/s41587-024-02526-3. PMID 39843581.
PMC12700792. Open access.

`[VERIFIED-FULLTEXT]`

- Target: **the switch II pocket** — _"binding mode within the switch II pocket"_.
- Structures: **5US4** (virtual screen) and **7EW9** (pharmacophore analysis).
- Hardware: _"16-qubit IBM quantum processor"_, Guadalupe, _"Falcon r4P processor type"_.
  Quantum circuit Born machine; **circuit depth not reported**.
- **No site prediction was performed.** Extraction: _"No allosteric site prediction performed. The
  site was treated as given."_
- Their own caveat, verbatim: _"While these findings are encouraging, they stop short of
  definitively proving a 'quantum advantage', achieving results unattainable by classical methods
  within a reasonable time frame."_

**So quantum + KRAS switch-II pocket is already in Nature Biotechnology — but on the _ligand
design_ side of a known pocket. The _discovery_ side is open.** That is a clean, defensible
statement of our contribution, and the sentence above is the one to cite for it.

## 6.3 Other quantum prior art

| Work                                                                                               | Reference                                                                                                                                                  | Relevance                                                                                                                                                                                                                                                                                                                                       | Tag                   |
| -------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------- |
| CTQW on a structure-derived redox network (mitochondrial complex I)                                | Sung J, Cheong J. bioRxiv 2026. doi:10.64898/2026.05.28.728423                                                                                             | _"we formulate electron transport as a continuous-time quantum walk on a structure-derived redox network"_ — same machinery, different biology                                                                                                                                                                                                  | `[VERIFIED-ABSTRACT]` |
| **Coherent Ising machine incl. allosteric site detection**                                         | Wen K, Zha J, Chen S, et al. bioRxiv 2026. doi:10.64898/2026.02.09.704961                                                                                  | _"QBoson-CPQC-3Gen"_; explicitly includes _"**allosteric site detection**, protein-peptide docking and intermolecular similarity calculation"_, _"performance exceeding traditional heuristic approaches"_. **The only retrieved prior art claiming quantum allosteric-site detection.** Preprint, not peer reviewed, target list not retrieved | `[VERIFIED-ABSTRACT]` |
| CTQW for disease gene prioritisation on PPI networks                                               | Saarinen H, Goldsmith M, Wang RS, Loscalzo J, Maniscalco S. Bioinformatics 2024;40:btae513. doi:10.1093/bioinformatics/btae513. PMID 39171848. PMC11361815 | _"a new algorithm for disease gene prioritization based on continuous-time quantum walks using the adjacency matrix of a protein–protein interaction (PPI) network"_ — network level, not residue level                                                                                                                                         | `[VERIFIED-ABSTRACT]` |
| CTQW link prediction on PPI networks                                                               | Goldsmith M, Saarinen H, García-Pérez G, Malmi J, Rossi MAC, Maniscalco S. Entropy 2023;25:730. doi:10.3390/e25050730. PMID 37238485                       | same group, same machinery                                                                                                                                                                                                                                                                                                                      | `[VERIFIED-ABSTRACT]` |
| **Quantum navigation and ranking in complex networks** — the foundational quantum-centrality paper | Sánchez-Burillo E, Duch J, Gómez-Gardeñes J, Zueco D. Sci Rep 2012;2:605. doi:10.1038/srep00605. PMID 22930671                                             | _"quantum coherence unveils new hierarchical features"_ — the general precedent for quantum-walk centrality/PageRank                                                                                                                                                                                                                            | `[VERIFIED-ABSTRACT]` |
| Quantum-inspired discrete-walk node influence                                                      | Liang W, Wang Y, Liu Q, Zhang W. Entropy 2025;27:634. doi:10.3390/e27060634. PMID 40566221                                                                 | quantum-inspired centrality at O(N⟨k⟩) — a cheap quantum-inspired baseline                                                                                                                                                                                                                                                                      | `[VERIFIED-ABSTRACT]` |
| Quantum-augmented graph differential geometry for PPI                                              | Karthick V, et al. Sci Rep 2026. doi:10.1038/s41598-026-41325-5. PMID 41760787                                                                             | 96.7 % accuracy claim on PPI prediction                                                                                                                                                                                                                                                                                                         | `[VERIFIED-ABSTRACT]` |
| Quantum computing for protein structure prediction                                                 | Doga H, Raubenolt B, Cumbo F, et al. JCTC 2024. doi:10.1021/acs.jctc.4c00067. PMID 38703105                                                                | _"framework for systematically selecting protein structure problems amenable for quantum advantage"_ — useful template for our C3/C4 resource section                                                                                                                                                                                           | `[VERIFIED-ABSTRACT]` |
| State of the art, quantum for drug discovery                                                       | Blunt NS, Camps J, Crawford O, et al. JCTC 2022. doi:10.1021/acs.jctc.2c00574. PMID 36355616                                                               | resource estimates for pharmaceutical simulation                                                                                                                                                                                                                                                                                                | `[VERIFIED-ABSTRACT]` |

## 6.4 Leads not found in the scoped retrieval

The recorded searches **did not retrieve**:

- No retrieved paper uses the Cleveland Clinic challenge target set (`4OBE`/`6OIM`, `1OPL`/`5MO4`,
  `5TBY`/`6C1H`, `1NKP`). The challenge itself is documented only in trade press — The Quantum
  Insider, 2026-04-16 and 2026-06-15; Cleveland Clinic newsroom, 2026-06-15 — not in the
  peer-reviewed literature `[VERIFIED-ABSTRACT via web search]`.
- No retrieved quantum method was applied to ABL1 or to cardiac myosin.
- No retrieved quantum walk ranked allosteric sites conditioned on an active site.
  Mohtashim 2026 does unconditioned centrality; Amor 2016 does active-site-conditioned propagation
  but classically. The scoped search did not cover the intersection; it does not establish
  that the intersection is unoccupied.
- Query `"quantum walk" AND "allosteric"` returned **hitCount 1**, and the single hit
  (Otaki, BioTech 2024, PMID 39846550) is a peptide inhibitor assay with no quantum content.

---

# 7. Scoped searches with no retrieved result

These are retrieval outcomes, not evidence that prior art is absent.

| Question                                                     | Query run                                                 | Result                                                                                      |
| ------------------------------------------------------------ | --------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| Blind prediction of the **ABL1 myristoyl pocket**            | 4 distinct queries (§1.2)                                 | **Nothing.** Pocket was found by crystallography and cell screening, never predicted        |
| Blind prediction of the **mavacamten site**                  | 3 distinct queries (§1.3)                                 | **Nothing.** The one AI study deliberately started from holo                                |
| Rank/score for the **KRAS S-IIP** from any general predictor | PocketMiner, CryptoBench, CrypToth, CryptoSite full texts | **Nothing.** PocketMiner and CryptoBench never mention Ras; CrypToth's 9 targets exclude it |
| `4LDJ`, `6OIM`, `5MO4`, `2G2H`, `2G1T` in the literature     | direct ID search + all target full texts                  | **Not found in any retrieved source**                                                       |
| `5TBY`, `6C1H` in the literature                             | all four myosin structure papers                          | **Not found anywhere.** No literature footprint at all                                      |
| `8QYP` / `8QYR`                                              | direct ID search; Auguin 2024 not OA; preprint XML 404    | **Not found.** Only `8QYQ` was confirmed                                                    |
| Published S-IIP → nucleotide-site **distance**               | §5                                                        | **Nothing**                                                                                 |
| Published myristoyl → ATP-site **distance**                  | §5                                                        | **Nothing**                                                                                 |
| Published mavacamten → ATPase/actin **distance**             | §5                                                        | **Nothing** (qualitative only)                                                              |
| Published **residue list** for the S-IIP                     | §4.1                                                      | **Nothing** (Ostrem full text 404)                                                          |
| Published **residue list** for the myristoyl pocket          | §4.2                                                      | **Nothing** (only 4 resistance mutations, convention unstated)                              |
| Anything describing the **myristoyl pocket as cryptic**      | dedicated query, 24 hits                                  | **Nothing**                                                                                 |
| **Quantum** + ABL1, myosin, or allosteric-site ranking       | §6.4                                                      | **Nothing**                                                                                 |
| Any paper using the **challenge target set**                 | §6.4                                                      | **Nothing**                                                                                 |

Sources that could not be retrieved and remain open:
`PMC4274051` (Ostrem 2013) → 404 · `PMC2901986` (Zhang 2010) → 404 · `PMC4794384` (CryptoSite 2016) → 404 · `PPR760230` (Auguin preprint) → 404 · Wylie 2017 and Nagar 2003 have no PMCID.
Six of the most load-bearing primary sources are paywalled or unavailable as XML; the abstracts
were retrieved for all of them.

---

# 8. What this changes

1. **Target 1 (KRAS) is a valid cryptic-pocket test** — Ostrem's own words, plus three
   independent corroborations. `4OBE` is confirmed by Vithani 2024 as the field's WT:GDP reference,
   confirming the repo audit's finding that it is not G12C.
2. **Target 2 (ABL1) is not a cryptic-pocket test.** No source calls the myristoyl pocket cryptic;
   Paladini calls it an _empty pocket_ in a myristate-free crystal. And CryptoBench's published
   ≥ 2 Å criterion, against the audit's measured 0.50 Å, disqualifies the `1OPL` → `5MO4` pair on
   the field's own terms. Cite CryptoBench for this — it is far stronger than an internal
   measurement alone.
3. **Target 3 (myosin) is partially cryptic on a single source.** Planelles-Herrero 2017:
   _"the OM-binding pocket is actually not completely formed in the APO-MD-PPS structure."_
   `5N6A` is a real drug-free structure of that pocket and deserves consideration as a sensitivity
   arm alongside `9GZ3`. The repo's corrected pairs `9GZ3` → `9GZ2` and `8ACT` → `9GZ1` are
   confirmed by the depositing paper.
4. **The classical bar is Grant 2011 for KRAS, and it is uncomfortably close.** 120 ns of MD with
   FTMap/AutoLigand found a pocket at residues `61–65, 90–99` two years before the S-IIP was
   discovered. Compute the overlap against our label set before claiming novelty.
5. **The quantum bar is Mohtashim 2026 (JACS).** CTQW on protein residue networks, on IBM
   hardware, published. Our differentiators are: conditioning on the active site, apo-only input,
   and an apo/holo scored benchmark — none of which they do. Their own finding that CTQW agrees
   closely with classical eigenvector centrality is the result we have to beat or explain.
6. **Report AUPRC, not just ROC-AUC.** Published cryptic-site methods sit at AUPRC 0.19–0.34 on
   CryptoBench while showing ROC-AUC 0.76–0.89. Reporting only ROC-AUC would flatter us the same
   way and a reviewer who knows CryptoBench will notice.
