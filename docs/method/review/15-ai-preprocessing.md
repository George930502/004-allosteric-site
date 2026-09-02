# AI preprocessing: characterising the input protein and adapting the pipeline to it

**Scope:** Whether an AI front-end stage can characterise an apo protein and adapt the
downstream graph-propagation pipeline to it, and what such a stage may legally be built from.
Covers pretrained representation models, MD-free flexibility and cryptic-pocket predictors,
the per-instance algorithm-selection literature, protein meta-features, contamination and
disclosure practice, and precedent for classical AI feeding a quantum stage. Deliberately
excludes allosteric-site predictors used as the _output_ of the pipeline (that is `02-ai-methods.md`),
the choice of quantum observable (`03`), and the classical baseline battery (`01`).
**Sibling files:** `00-conventions.md` (evidence tags, C1–C6, the leakage guard),
`02-ai-methods.md` (learned allosteric-site predictors and the supervision ceiling),
`04-hybrid-quantum-ai.md` (stage-by-stage division of labour),
`09a-power-verification.md` and `../exploration/results/41-selection-and-power.md` (what our N resolves).
**Retrieved:** 2026-08-26.

**Scope statement and search record.** All retrieval was performed on **2026-08-26** against
Google/Bing-backed web search, arXiv abstract pages, PubMed and PubMed Central, bioRxiv, Nature,
Science, Oxford Academic, IOPscience, PNAS, APS, MIT Press, JAIR, PMLR and NeurIPS proceedings
pages, and Hugging Face / GitHub model cards for licence text. Representative query strings, run
verbatim: `PocketMiner graph neural network cryptic pocket trained molecular dynamics simulations
Meller 2023`; `AlphaFlow ESMFlow flow matching protein conformational ensembles Jing 2024 PDB MD
ATLAS fine-tuned`; `BioEmu biomolecular emulator Lewis 2025 Science trained molecular dynamics 200
milliseconds`; `Distributional Graphormer DiG Zheng 2024 training data molecular dynamics`;
`AlphaFold2 pLDDT as intrinsic disorder predictor CAID assessment`; `AlphaFold2 predicted aligned
error PAE domain boundary definition inter-domain motion proxy`; `Merizo Chainsaw SWORD2 protein
domain segmentation AlphaFold models`; `ESM-IF1 Hsu learning inverse folding from millions of
predicted structures`; `SaProt structure-aware vocabulary Foldseek 3Di`; `ProstT5 bilingual
language model`; `ESM-C EvolutionaryScale Cambrian license`; `Rice 1976 The Algorithm Selection
Problem`; `SATzilla portfolio-based algorithm selection`; `Kerschke Hoos Neumann Trautmann
Automated Algorithm Selection Survey`; `Rivolli Meta-features for meta-learning`; `Zelnik-Manor
Perona Self-tuning spectral clustering`; `Delvenne Yaliraki Barahona Stability of graph communities
across time scales`; `Meinshausen Buhlmann Stability selection`; `Varoquaux Cross-validation
failure small sample sizes`; `Cawley Talbot over-fitting in model selection`; `Varma Simon Bias in
error estimation`; `Kapoor Narayanan Leakage and the reproducibility crisis`; `Park Marcotte Flaws
in evaluation schemes for pair-input computational predictions`; `A flaw in using pretrained
protein language models in protein-protein interaction inference models`; `Graph-Part homology
partitioning`; `Chen Hidden bias in the DUD-E dataset`; `Walsh DOME recommendations`; `Moussa
Calandra Dunjko To quantum or not to quantum algorithm selection`; `Schuld Killoran Is quantum
advantage the right goal`; `Bowles Ahmed Schuld Better than classical`; `Schreiber Eisert Meyer
Classical surrogates for quantum learning models`; `Mücke Feature selection on quantum computers`;
plus per-model queries for ESM-2, ESM-3, ProtTrans/ProtT5, Ankh, ProteinMPNN, GearNet, Foldseek,
MEDUSA, PEGASUS, DynaMine, flDPnn, PredyFlexy, IUPred3, GNM, ANM, ProDy, ESSA, APOP, SPECTRUS,
DEPTH, DSSP, CryptoBench, CrypticScout and CAMEO. Roughly 80 search queries and 9 direct document
fetches were run across two passes; one fetch failed outright (ScienceDirect HTTP 403, recovered
via an alternate route) and two returned redirects (one followed to the content, one confirming DOI
resolution only). **No experiment has run behind this file.** Nothing here opens any path under
`docs/benchmark/`, and no real label residue is named.

---

## Executive summary — the four sentences that matter

1. **A front-end that adapts the pipeline is legal and cheap, but almost nothing that is
   _learned_ is admissible.** The best MD-free flexibility signals in the literature — PocketMiner,
   BioEmu, AlphaFlow-MD, PEGASUS, CryptoSite — are all trained on molecular-dynamics trajectories
   and are therefore barred by C2, regardless of how fast their inference is.
2. **The two admissible learned families are self-supervised sequence/structure representations
   (ESM-2, ProtT5, ESM-IF, ProteinMPNN, Foldseek 3Di) and AlphaFold-family confidence heads
   (pLDDT, PAE)** — none of which ever saw an MD trajectory or an allosteric label. Their
   flexibility signal is weaker than the literature's enthusiasm suggests and must be reported
   with the counter-evidence.
3. **With 4–13 proteins, a _learned_ per-instance selector cannot be validated.** The paired
   minimum detectable effect at n = 13 is ≈ 0.85 × SD of the paired AUC difference; a selector
   choosing among m arms per protein has 13·log₂(m) bits of freedom and will memorise the set.
   The only defensible design is a **label-free, parameter-free adaptation rule** — spectral
   normalisation of the diffusion time, local-scaling of edge weights, stability-based arm
   retention — which needs no validation because it fits nothing.
4. **The accepted way to keep the quantum stage the contribution is an ablation, not an
   argument**: run the identical classical front end with the quantum stage replaced by its
   cheapest classical readout, and report the delta alongside the qubit/depth cost.

---

## Q1. Pretrained models that characterise a protein from an apo structure or sequence

### Synthesis

**Protein language models.** The self-supervised masked-language-model family (ESM-1b/ESM-2/ESM-3,
ProtTrans/ProtT5, ProstT5, Ankh) is trained on UniRef/BFD sequence corpora with no structural,
dynamical or functional label in the loss. Two independent lines establish that useful structural
information nevertheless falls out of the attention weights. Vig et al. showed that attention in
BERT/ALBERT/XLNet protein transformers "captures the folding structure of proteins by connecting
amino acids that are far apart in the underlying sequence but spatially close in the
three-dimensional structure", that attention "targets binding sites", and that it "focuses on
progressively more complex biophysical properties with increasing layer depth", consistently
across three architectures and two datasets [VERIFIED-ABSTRACT, ICLR 2021, arXiv:2006.15222].
Rao et al. showed that attention maps learn contacts from the unsupervised objective alone, with
the highest-capacity models outperforming state-of-the-art unsupervised contact predictors
[VERIFIED-ABSTRACT, bioRxiv 2020.12.15.422761 / ICLR 2021]. This is the mechanism our repo already
uses in `02-ai-methods.md` §9 route 1. **Read it beside the counter-evidence already recorded in
`00-conventions.md` §5: PLM signal collapses on allosteric sites specifically (AUPR 0.06 against
0.64–0.76 orthosteric in the same proteins).** Attention finds _binding_ sites; the allosteric
subclass is where it fails.

Licences differ sharply and this is a real constraint. ESM-2/ESMFold ship under MIT via
`facebookresearch/esm`; ESM-3 and ESM-C 600M ship under EvolutionaryScale's **Cambrian
Non-Commercial License**, with only ESM-C 300M under the more permissive Cambrian Open License
[VERIFIED-ABSTRACT, evolutionaryscale.ai licence pages and HF model cards]. ESM-C has **no
peer-reviewed paper or preprint DOI retrieved by the recorded search** — a negative result, not an
absence claim. ProstT5 is MIT [VERIFIED-ABSTRACT, GitHub `mheinzinger/ProstT5`].

**Structure-aware models.** ESM-IF1 is the cleanest structure-conditioned self-supervised
representation available: an autoregressive transformer with GVP geometric input layers, trained
to recover sequence from backbone coordinates on CATH **plus 12 M AlphaFold2-predicted structures**
[VERIFIED-ABSTRACT, PMLR v162 (ICML 2022)]. That training corpus matters twice over — it is
MD-free (admissible) but it is _predicted_ structure, so ESM-IF has effectively seen a
computational proxy for most of the PDB's fold space. ProteinMPNN is a message-passing inverse-folding
model trained on PDB backbones [VERIFIED-ABSTRACT, doi:10.1126/science.add2187]. GearNet is
pretrained by multiview contrast and self-prediction on **805 K AlphaFoldDB structures**
[VERIFIED-ABSTRACT, arXiv:2203.06125]. SaProt fuses amino-acid and Foldseek 3Di tokens into a
structure-aware vocabulary over ~40 M sequence–structure pairs [VERIFIED-ABSTRACT, ICLR 2024,
bioRxiv 2023.10.01.560349]. Foldseek's 3Di alphabet itself is not a learned protein model in the
same sense — it is a 20-state structural alphabet describing, for each residue, the geometric
conformation with its spatially closest partner, and it is GPLv3 free software
[VERIFIED-ABSTRACT, doi:10.1038/s41587-023-01773-0]. **For a meta-feature vector, 3Di is the
best value per unit of risk in this whole section: it is deterministic, licence-clean, needs no
GPU, and gives a fold-class descriptor directly from apo coordinates.**

**Structure predictors as flexibility proxies — the important and most-oversold claim.** The
attraction is obvious: pLDDT and PAE give a per-residue and per-pair uncertainty estimate with no
MD anywhere. The literature is genuinely split.

- _For._ Guo et al. report that "pLDDT scores are highly correlated with the root mean square
  fluctuations (RMSF) calculated from MD simulations", introduce reversed-pLDDT "AF2-scores"
  that are "highly consistent with the RMSF profiles from MD", and report that PAE maps show
  "highly consistent patterns" with MD distance-variation matrices, concluding "the PAE map from
  AF2 originates from the protein dynamics" [VERIFIED-FULLTEXT, doi:10.1038/s41598-022-14382-9].
  Independently, PAE is the operational basis of AlphaFold domain parsing: blocks of high PAE mark
  domain boundaries, and PAE is "a measure of the local packing of residues … as well as of the
  relative placement of domains" [VERIFIED-ABSTRACT, retrieved 2026-08-26 from the UCSF ChimeraX
  PAE documentation and the SPAED preprint].
- _Against._ pLDDT is a mediocre disorder predictor when measured properly. CAID round 2 found
  that AlphaFold-based methods "perform particularly well in the Disorder-PDB benchmark, but less
  well in the Disorder-NOX and are not in the top 10 when considering APS", and that neither
  pLDDT nor AF2-derived RSA "correctly prioritize disordered positions as defined in the
  Disorder-NOX reference" [VERIFIED-ABSTRACT, doi:10.1002/prot.26582]. A head-to-head against 20
  dedicated predictors puts AF2-based disorder at **AUC 0.77 versus ~0.80** for several modern
  predictors, a statistically significant loss [VERIFIED-ABSTRACT, doi:10.1016/j.csbj.2023.06.001].
  Piovesan et al. establish AF2DB-derived baselines using **pLDDT and RSA together**, with RSA
  carrying much of the signal [VERIFIED-ABSTRACT, doi:10.1002/pro.4466].

**Our reading.** pLDDT is a defensible _ordinal_ flexibility/disorder proxy for a meta-feature
(e.g. "what fraction of this chain is low-confidence"), and PAE is a defensible _domain-partition_
proxy. Neither is a substitute for a fluctuation calculation, and the Guo et al. RMSF correlation
should be quoted as one study's finding, not as an established equivalence. A GNM/ANM fluctuation
profile costs one eigendecomposition, needs no weights and no MD, and is the honest baseline
against which any pLDDT-derived flexibility feature must be shown to add something.

**Conformational-ensemble predictors — the C2 minefield.** Provenance must be checked
_variant-by-variant_, not model-by-model.

- **AF2 with reduced MSA depth / MSA subsampling.** Restricting MSA depth lets AlphaFold2 predict
  diverse conformational ensembles instead of a single static model [VERIFIED-ABSTRACT,
  doi:10.7554/eLife.75751]. **No MD anywhere** — it is a change to inference-time inputs on
  weights trained on the PDB. Fully C2-legal.
- **AF-Cluster (sequence clustering + AF2).** Same property, published in Nature
  [VERIFIED-ABSTRACT, doi:10.1038/s41586-023-06832-9] — but a Nature Matters Arising, "Sequence
  clustering confounds AlphaFold2", disputes the mechanism [VERIFIED-ABSTRACT,
  doi:10.1038/s41586-024-08267-2]. Legal, contested.
- **AlphaFlow / ESMFlow.** Two variants on opposite sides of C2. The PDB-trained variant is legal.
  The variant "further trained on ensembles from all-atom MD" is **not** [VERIFIED-ABSTRACT,
  arXiv:2402.04845; PMLR v235 (ICML 2024)].
- **Distributional Graphormer (DiG).** DiG "can be trained using flexible types of sources,
  including simulation data such as molecular dynamics trajectories, as well as the energy
  functions (force fields) of molecular systems" [VERIFIED-ABSTRACT, doi:10.1038/s42256-024-00837-3;
  arXiv:2306.05445]. The abstract retrieved this session does **not** state which source was used
  for the released protein-conformation checkpoint. **Training data not determined for the released
  protein weights** — and under C2 an undetermined provenance is a disqualification, not a licence.
- **BioEmu.** Trained by "combining training data from AlphaFold structural predictions,
  large-scale MD simulations, and extensive experimental measurements of protein stability",
  integrating **over 200 ms of MD** [VERIFIED-ABSTRACT, doi:10.1126/science.adv9817; Nature Methods
  research briefing doi:10.1038/s41592-025-02874-1]. Single-sequence inference; MD-trained weights.
  Illegal.

**Fold and domain classifiers.** Merizo is trained on CATH domains and fine-tuned on AF2 models by
self-distillation [VERIFIED-ABSTRACT, doi:10.1038/s41467-023-43934-4]. Chainsaw is a fully
convolutional network predicting the probability that each residue pair is in the same domain,
reported to beat Merizo and unsupervised parsers on held-out CATH and CASP annotations
[VERIFIED-ABSTRACT, doi:10.1093/bioinformatics/btae296]. SWORD2 decomposes a structure into
hierarchical "Protein Units" by iterative clustering of the contact probability map — **no learned
weights at all** [VERIFIED-ABSTRACT, doi:10.1093/nar/gkac370]. SPECTRUS obtains quasi-rigid
domains by spectral clustering of ENM-derived distance fluctuations, again with no training and no
MD [VERIFIED-ABSTRACT, doi:10.1016/j.str.2015.05.022]. **SWORD2 and SPECTRUS are strictly
preferable for us to Merizo/Chainsaw**: they give the same meta-feature (domain count and
boundaries) with zero training-provenance risk, and SPECTRUS is built out of exactly the elastic
network C6 already commits us to.

### Table

| Model or method           | Year    | Input                                  | Output                                              | Training data                                                                                  | MD-derived?        | Licence                                          | Relevance to us                                                              |
| ------------------------- | ------- | -------------------------------------- | --------------------------------------------------- | ---------------------------------------------------------------------------------------------- | ------------------ | ------------------------------------------------ | ---------------------------------------------------------------------------- |
| ESM-2 / ESMFold           | 2023    | sequence                               | per-residue embeddings, attention maps, structure   | UniRef; up to 15 B params                                                                      | No                 | MIT (`facebookresearch/esm`)                     | Meta-features + attention; PLM collapse on allosteric sites already measured |
| ESM-3                     | 2025    | sequence / structure / function tokens | multimodal embeddings, generation                   | evolutionary-scale multimodal corpus                                                           | No                 | Cambrian Non-Commercial (open weights, academic) | Licence blocks any commercial claim; no allostery-specific evidence          |
| ESM-C (300M/600M/6B)      | 2024    | sequence                               | per-residue embeddings                              | protein sequences (details not in a paper)                                                     | No                 | 300M: Cambrian Open; 600M: Non-Commercial        | **No paper DOI retrieved**; do not cite as literature                        |
| ProtT5 / ProtTrans        | 2022    | sequence                               | per-residue embeddings                              | UniRef + BFD, up to 393 B amino acids                                                          | No                 | code public (`agemagician/ProtTrans`)            | Strong per-residue embeddings without MSAs                                   |
| ProstT5                   | 2024    | sequence ↔ 3Di                         | translation between sequence and structure alphabet | ProtT5-XL-U50 finetuned on 17 M high-quality AFDB structures                                   | No                 | MIT                                              | 3Di from sequence alone; fold descriptor without coordinates                 |
| Ankh                      | 2023    | sequence                               | per-residue embeddings                              | protein sequence corpora; optimised, <10 % of SOTA pretraining cost                            | No                 | see `agemagician/Ankh` model card                | Cheapest strong PLM; licence not verified this session                       |
| ESM-IF1                   | 2022    | backbone coordinates                   | sequence logits, structure-conditioned embeddings   | CATH + **12 M AF2-predicted structures**                                                       | No                 | MIT (`facebookresearch/esm`)                     | Structure-conditioned features with no MD; already stacked in AF2BIND        |
| ProteinMPNN               | 2022    | backbone coordinates                   | sequence logits / embeddings                        | PDB backbones                                                                                  | No                 | code public, Baker lab                           | Per-residue structural context score, MD-free                                |
| GearNet                   | 2023    | residue graph                          | structure embeddings                                | 805 K AlphaFoldDB structures, self-supervised                                                  | No                 | code public (`DeepGraphLearning/GearNet`)        | Nearest architecture to our own residue graph                                |
| SaProt                    | 2024    | sequence + 3Di                         | structure-aware embeddings                          | ~40 M sequence–structure pairs                                                                 | No                 | code public                                      | Fold-aware embedding without a separate structure model                      |
| Foldseek 3Di              | 2024    | coordinates                            | 20-state structural alphabet, fold search           | alphabet learned on structure pairs (not a downstream task)                                    | No                 | **GPLv3**                                        | Best risk-adjusted fold/meta-feature source in this table                    |
| AlphaFold2 pLDDT          | 2021    | sequence (+MSA)                        | per-residue confidence                              | PDB + self-distillation, date-cutoff training                                                  | No                 | code Apache-2.0; AFDB entries CC-BY-4.0          | Disorder/flexibility proxy — AUC 0.77 vs ~0.80 for dedicated predictors      |
| AlphaFold2 PAE            | 2021    | sequence (+MSA)                        | pairwise expected alignment error                   | as above                                                                                       | No                 | as above                                         | Domain-boundary and inter-domain-rigidity proxy                              |
| AlphaFold3                | 2024    | sequence + ligands/ions                | structure, pLDDT, PAE                               | expanded biomolecular corpus                                                                   | No                 | **weights on request, non-commercial only**      | Licence makes it unusable as a reproducible pipeline component               |
| AF2 + MSA subsampling     | 2022    | sequence, reduced MSA depth            | conformational ensemble                             | none (inference-time change)                                                                   | **No**             | as AF2                                           | The one ensemble route that is unambiguously C2-legal                        |
| AF-Cluster                | 2024    | sequence, clustered MSA                | alternative conformations                           | none (inference-time change)                                                                   | **No**             | code public                                      | Legal but mechanism disputed by a Nature Matters Arising                     |
| AlphaFlow / ESMFlow (PDB) | 2024    | sequence                               | conformational ensemble                             | PDB only                                                                                       | **No**             | code public                                      | Legal ensemble generator                                                     |
| AlphaFlow (MD-finetuned)  | 2024    | sequence                               | conformational ensemble                             | + all-atom MD ensembles                                                                        | **Yes**            | code public                                      | **Barred by C2**                                                             |
| Distributional Graphormer | 2024    | graph or sequence                      | equilibrium distribution                            | MD trajectories _and/or_ force fields; released-checkpoint source not stated in retrieved text | **Not determined** | code public                                      | Barred pending provenance; undetermined ≠ admissible                         |
| BioEmu                    | 2025    | sequence                               | equilibrium structure ensemble                      | AFDB + **>200 ms MD** + ~experimental stability                                                | **Yes**            | code public                                      | **Barred by C2** despite MD-free inference                                   |
| Merizo                    | 2023    | structure                              | domain segmentation                                 | CATH domains + AF2 self-distillation                                                           | No                 | code public (`psipred/Merizo`)                   | Legal; superseded for us by SWORD2/SPECTRUS                                  |
| Chainsaw                  | 2024    | structure                              | domain segmentation                                 | CATH + CASP annotations                                                                        | No                 | code public                                      | Legal; same comment                                                          |
| SWORD2                    | 2022    | structure                              | hierarchical Protein Units                          | **no training**                                                                                | No                 | code public (`DSIMB/SWORD2`)                     | Zero-provenance-risk domain count                                            |
| SPECTRUS                  | 2015    | structure(s)                           | quasi-rigid dynamical domains                       | **no training**, ENM distance fluctuations                                                     | No                 | published algorithm                              | Domain count from the same elastic network C6 assumes                        |
| CATH / SCOP assignment    | ongoing | structure                              | fold class                                          | curated classification                                                                         | No                 | academic use                                     | Fold-class meta-feature; assignment latency is the practical cost            |

---

## Q2. Models that predict flexibility, dynamics or cryptic pockets without MD

### Synthesis

**PocketMiner — confirmed MD-trained, with the exact numbers.** The suspicion in the task brief is
correct and the details are worse than the summary suggests. From the paper's full text:
"This dataset included 37 proteins and 2400 independent MD simulations at least 40 ns in length";
"We generated labels for each residue in each 40 ns window's starting structure based on whether
that residue participates in a cryptic pocket at any point in the next 40 ns of simulation …
Altogether, this dataset included 941,650 unique examples"; a residue was positive "if at any point
in simulation the nearby pocket volume determined by the LIGSITE algorithm increased by more than
40 Å² relative to its assigned pocket volume in the starting structure"; final ROC-AUC 0.87 on a
test set of "24 apo structures that form ligand-binding cryptic pockets, 4 hyper-rigid proteins,
and 7 proteins that were the subjects of extensive ligand screening", all under 55 % sequence
identity to training [VERIFIED-FULLTEXT, doi:10.1038/s41467-023-36699-3, PMC9977097]. **The label
itself is an MD event.** Inference takes a single structure, which is exactly the trap
`02-ai-methods.md` §7 names: fast single-structure inference is not evidence of C2 compliance. This
also corrects the "35 proteins" figure in `02-ai-methods.md` §3 to **37**.

**CryptoSite and CrypticScout are worse, not better.** CryptoSite requires _new_ MD at inference
(already recorded in `02-ai-methods.md` §8). CrypticScout is a mixed-solvent MD workflow using
benzene as a hydrophobic probe, mapping "probe occupancy, residence time, and the benzene occupancy
reweighed by the residence time", tested on 18 systems plus 5 kinases and served through
PlayMolecule [VERIFIED-ABSTRACT, doi:10.1021/acs.jcim.9b01209]. It is an MD _method_, not merely
MD-trained: barred at inference under C2, without qualification. CrypToth and CrypTothML are the
same family [VERIFIED-ABSTRACT, doi:10.1021/acs.jcim.4c02111].

**The useful thing the cryptic-pocket literature gives us is not a model but a finding.** Beglov et
al. report that "cryptic sites in ligand-free structures generally have a strong binding energy hot
spot very close by", that "regions around cryptic sites exhibit above-average flexibility", and
that "close to 50 % of the proteins studied have unbound structures that could accommodate the
ligand without clashes" [VERIFIED-ABSTRACT, doi:10.1073/pnas.1711490115]. Two of those three are
computable from an apo structure with no learning at all — local flexibility from an ENM, and hot-spot
proximity from a geometric/energetic probe. **Note the vocabulary trap flagged in `CONTEXT.md`:
cryptic and allosteric are not synonyms.** These findings license a _flexibility_ meta-feature, not
an allosteric-site prediction.

CryptoBench is worth knowing about as a dataset-design precedent rather than a model: it is built
on apo–holo pairs "grouped by UniProtID, clustered by sequence identity, and filtered to contain
only structures with substantial structural change in the binding site", explicitly because
"holo-based assessment yields unrealistic performance expectations"
[VERIFIED-ABSTRACT, doi:10.1093/bioinformatics/btae745]. That is the same apo-vs-holo axis the
challenge scores on, arrived at independently.

**Sequence-based flexibility predictors split cleanly on training label.**

| label the model was fit to                  | admissible?                                         | examples                                                      |
| ------------------------------------------- | --------------------------------------------------- | ------------------------------------------------------------- |
| crystallographic B-factors                  | **Yes** — experimental observable, not a trajectory | MEDUSA, the B-factor Bi-LSTM already in `02-ai-methods.md` §9 |
| NMR-derived S² order parameters             | **Yes** — experimental observable                   | DynaMine                                                      |
| curated disorder annotations (DisProt/CAID) | **Yes**                                             | flDPnn, IUPred3                                               |
| **MD-derived RMSF / dihedral SD / LDDT**    | **No — C2**                                         | PEGASUS                                                       |

MEDUSA predicts a flexibility class per residue "in terms of the expected normalized B-factor value
range", trained on X-ray B-factors [VERIFIED-ABSTRACT, doi:10.1016/j.jmb.2021.166882]. DynaMine
predicts backbone N–H S² order parameters "directly estimated from experimentally determined NMR
chemical shifts" [VERIFIED-ABSTRACT, doi:10.1038/ncomms3741]. flDPnn predicts disorder and four
disorder functions and was assessed in CAID [VERIFIED-ABSTRACT, doi:10.1038/s41467-021-24773-7].
PredyFlexy predicts flexibility and local structure from sequence [VERIFIED-ABSTRACT,
doi:10.1093/nar/gks482]; **its exact training-label source was not established by the recorded
search — training data not determined.** PEGASUS, from the same group as MEDUSA, is the explicit
C2 violation in this family: it is "a sequence-based predictor of MD-derived information on protein
flexibility developed using the recently released ATLAS database", predicting RMSF, φ/ψ standard
deviations and mean LDDT from PLM embeddings [VERIFIED-ABSTRACT, doi:10.1002/pro.70221]. It is the
most accurate MD-free-at-inference flexibility predictor found this session, and we may not use it.

**The always-admissible baseline: elastic network normal modes.** GNM (Bahar, Atilgan & Erman 1997,
doi:10.1016/S1359-0278(97)00024-2) and ANM (Atilgan et al. 2001, doi:10.1016/S0006-3495(01)76033-X)
require **no training, no MD, and no labels**, and are implemented in ProDy
[VERIFIED-ABSTRACT, doi:10.1093/bioinformatics/btr168]. Their allostery-facing derivatives, ESSA
[VERIFIED-ABSTRACT, doi:10.1016/j.csbj.2020.06.020] and APOP
[VERIFIED-ABSTRACT, doi:10.1093/bioinformatics/btad275], are already our bar in
`00-conventions.md` §6. **Record the consequence for this file: every learned flexibility feature we
might add has to be shown to beat a GNM mode-weighted fluctuation profile computed on the same
graph, which is one eigendecomposition and costs nothing.** That is the control, not a nicety.

### Table

| Model or method  | Year | Input                               | Output                                         | Training data                                                        | MD-derived?    | Licence                                      | Relevance to us                                                                       |
| ---------------- | ---- | ----------------------------------- | ---------------------------------------------- | -------------------------------------------------------------------- | -------------- | -------------------------------------------- | ------------------------------------------------------------------------------------- |
| GNM              | 1997 | Cα coordinates                      | per-residue mean-square fluctuation, modes     | **none**                                                             | No             | algorithm; ProDy MIT                         | Always-admissible flexibility baseline; C6-native                                     |
| ANM              | 2001 | Cα coordinates                      | directional modes, fluctuations                | **none**                                                             | No             | algorithm; ProDy MIT                         | Directional flexibility; anisotropic PRS already measured (below chance)              |
| ProDy            | 2011 | structure                           | GNM/ANM/NMA toolkit                            | n/a                                                                  | No             | MIT                                          | Reference implementation                                                              |
| ESSA             | 2020 | structure                           | essential-site score from soft-mode shifts     | **none**                                                             | No             | ProDy                                        | Part of our stated bar                                                                |
| APOP             | 2023 | structure                           | ranked allosteric pockets                      | **none** (parameters fixed, not fitted)                              | No             | published method                             | Part of our stated bar; 92/104 top-3 self-reported, 15 % under AlloBench declustering |
| SPECTRUS         | 2015 | structure                           | quasi-rigid domains                            | **none**                                                             | No             | published method                             | Domain-count meta-feature from an ENM                                                 |
| MEDUSA           | 2021 | sequence                            | flexibility class (normalised B-factor bin)    | X-ray B-factors                                                      | No             | `DSIMB/MEDUSA`                               | Legal flexibility prior; untested on allostery                                        |
| DynaMine         | 2013 | sequence                            | backbone N–H S² order parameter                | NMR chemical shifts                                                  | No             | web server / bio2byte                        | Legal flexibility prior; experimental label                                           |
| flDPnn           | 2021 | sequence                            | disorder + 4 disorder functions                | DisProt/CAID annotations                                             | No             | web server                                   | Legal disorder-content meta-feature                                                   |
| IUPred3          | 2021 | sequence                            | disorder propensity                            | biophysical energy estimation + annotation                           | No             | academic use                                 | Legal, near-zero cost disorder meta-feature                                           |
| PredyFlexy       | 2012 | sequence                            | flexibility + local structure                  | **training data not determined**                                     | Unknown        | web server                                   | Do not use until provenance is established                                            |
| B-factor Bi-LSTM | 2023 | sequence + Cα + SS                  | predicted B-factor, r = 0.80                   | 56 k PDB structures' experimental B-factors                          | No             | see PMC10499862                              | Legal; already flagged untested for allostery                                         |
| **PEGASUS**      | 2025 | sequence (PLM embeddings)           | **MD-derived** RMSF, φ/ψ SD, mean LDDT         | ATLAS MD database                                                    | **Yes**        | `DSIMB/PEGASUS`                              | **Barred by C2** — the most tempting violation in this table                          |
| **PocketMiner**  | 2023 | single structure                    | per-residue cryptic-pocket-opening probability | 37 proteins, 2 400 MD runs ≥ 40 ns, 941 650 examples, LIGSITE labels | **Yes**        | code CC-BY-4.0 article; GitHub `Mickdub/gvp` | **Barred by C2**; labels are MD events                                                |
| **CryptoSite**   | 2016 | structure + **new MD at inference** | cryptic-site score                             | 84 cryptic sites; 28/58 features from AllosMod MD                    | **Yes, twice** | web server                                   | **Barred by C2** at training and inference                                            |
| **CrypticScout** | 2020 | structure + **mixed-solvent MD**    | probe hotspot map                              | n/a (physics workflow, MD is the method)                             | **Yes**        | PlayMolecule                                 | **Barred by C2** at inference                                                         |
| CryptoBench      | 2025 | apo–holo pairs                      | dataset + benchmark model                      | apo–holo pairs, UniProt-grouped, identity-clustered                  | No             | OSF / GitHub                                 | Dataset-design precedent for apo-based evaluation                                     |

---

## Q3. Per-input adaptation: the machine-learning pattern

### Synthesis

**The problem has a name and a 50-year-old formalisation.** Rice's algorithm selection problem is
exactly ours: find a mapping from a problem-instance space to a set of candidate algorithms, using
features of the instance [VERIFIED-ABSTRACT, Rice 1976, _Advances in Computers_ 15:65–118,
doi:10.1016/S0065-2458(08)60520-3 — DOI confirmed resolvable this session]. The canonical modern
instantiation is SATzilla, which builds "per-instance algorithm portfolios for SAT that use
empirical hardness models to choose among their constituent solvers"
[VERIFIED-ABSTRACT, doi:10.1613/jair.2490]. The standard architecture is four blocks and has not
changed materially since:

1. **Instance features** — cheap, computable before the expensive step runs.
2. **Presolvers / fallbacks** — a fixed cheap algorithm run first, so the selector never has to be
   right about easy instances.
3. **Empirical performance models** — one regressor per candidate algorithm, predicting its
   runtime/quality on an instance from its features.
4. **Selection rule** — argmax over predicted performance, with a backup.

Kerschke et al.'s survey is the modern reference and states the field's own scope: per-instance
algorithm selection "has been intensely studied over the past 15 years and has led to major
improvements in solving discrete combinatorial problems"
[VERIFIED-ABSTRACT, doi:10.1162/evco_a_00242]. **Note what that scope is not.** Every headline
success is on instance distributions with thousands to millions of instances. Nothing in that
literature validates a selector at n = 13.

**Meta-features.** Rivolli et al. give the field's systematic treatment: meta-features are
"characterizations … that describe properties of data that are predictive for the performance of
machine learning algorithms" [VERIFIED-ABSTRACT, doi:10.1016/j.knosys.2021.108101]. The properties
that make a meta-feature set good, extracted from that work and from the SATzilla design, are:
(i) **cheap** relative to the algorithm being selected; (ii) **deterministic**; (iii) **scale-
and size-invariant**, or explicitly normalised, so that a value means the same thing on a 150-residue
and a 900-residue protein; (iv) **discriminative** — it actually varies across the instance
population; (v) **low-dimensional relative to n**, because each meta-feature is a degree of freedom
the selector can overfit on.

**AutoML is the same pattern with the search made explicit.** auto-sklearn combines Bayesian
optimisation over a 15-classifier / 14-preprocessor space with two ideas that matter here:
**meta-learning warm-starts** (use performance on similar prior datasets to seed the search) and
**post-hoc ensemble construction** from the models evaluated during optimisation
[VERIFIED-ABSTRACT, NeurIPS 2015 proceedings]. The second is the more important lesson for us.

**Ensembling versus selection — when "run everything and combine" wins.** Stacking originates with
Wolpert (_Neural Networks_ 5:241–259, 1992) and was extended to regression by Breiman, who forms
"linear combinations of different predictors … using cross-validation data and least squares under
non-negativity constraints" [VERIFIED-ABSTRACT, doi:10.1007/BF00117832]. Caruana et al.'s ensemble
selection builds ensembles from libraries of thousands of models by forward stepwise selection
optimising the target metric directly [VERIFIED-ABSTRACT, doi:10.1145/1015330.1015432]. The
decision rule that falls out of this literature and applies directly to us:

> **Selection beats ensembling when the selector's own error is small relative to the spread
> between candidates. Ensembling beats selection when it is not.** With 13 instances the selector's
> error is large by construction. Therefore: ensemble.

Ensembling also has a second advantage under our constraints: a rank-aggregation ensemble across
arms can be computed **without any label**, whereas a selector cannot be _fitted_ without one.

**Label-free / self-tuning parameter choice — the branch we should actually take.** There is a
mature literature on choosing a graph-algorithm hyperparameter from the data itself.

- **Local scaling.** Zelnik-Manor & Perona set a _per-point_ affinity scale σᵢ from the distance to
  the k-th nearest neighbour, removing the global bandwidth hyperparameter and handling multi-scale
  data and cluttered backgrounds; they also infer the number of groups from eigenvector structure
  [VERIFIED-ABSTRACT, NeurIPS 17 (2004), proceedings entry
  `40173ea48d9567f1f393b20c855bb40b`; ACM DL 10.5555/2976040.2976241. **No Crossref DOI was issued
  for this paper** — recorded as a gap, not glossed over]. This maps onto our contact graph
  directly: replace a fixed Å cutoff or a fixed Gaussian width with a per-residue local scale.
- **Eigengap.** von Luxburg's tutorial states the heuristic precisely: choose k so that λ₁…λ_k are
  small and λ_{k+1} is relatively large [VERIFIED-ABSTRACT, arXiv:0711.0189, _Statistics and
  Computing_ 17(4)]. This gives a label-free estimate of the number of dynamical modules.
- **Markov stability / diffusion time.** Delvenne, Yaliraki & Barahona define the stability of a
  partition from "the clustered autocovariance of a dynamic Markov process taking place on the
  network", with "an intrinsic dependence on time scales of the graph", allowing partitions to be
  ranked at each time and the time spans over which each is optimal to be established
  [VERIFIED-ABSTRACT, doi:10.1073/pnas.0903215107]. **This is the single closest match in the entire
  survey to what we need**: a principled, label-free way to pick the propagation time of a walk on
  a graph. It has already been applied to proteins by the same group, using multi-scale graph
  partitioning plus robustness analysis to uncover organisation "across the full range of scales"
  [VERIFIED-ABSTRACT, doi:10.1088/1478-3975/8/5/055010, arXiv:1109.4232].
- **Stability-based model selection.** Meinshausen & Bühlmann's stability selection subsamples and
  keeps structures that recur, giving "finite sample control for some error rates of false
  discoveries and hence a transparent principle to choose a proper amount of regularization"
  [VERIFIED-ABSTRACT, doi:10.1111/j.1467-9868.2010.00740.x]. Applied to a ranking rather than a
  variable set, this becomes: perturb the graph, keep the residues whose high rank survives.

**Honest validation at n = 4–13.** Three results bound what is possible, and they are unanimous.

- Cross-validating a model that was itself tuned by cross-validation "gives a significantly biased
  estimate of the true error"; the remedy is nested cross-validation
  [VERIFIED-ABSTRACT, doi:10.1186/1471-2105-7-91].
- Cawley & Talbot show the mechanism: non-negligible **variance** in the model-selection criterion
  produces over-fitting _in the selection step itself_, independent of the model's own capacity;
  nested CV with separate inner and outer loops is the recommended remedy
  [VERIFIED-ABSTRACT, JMLR 11:2079–2107 (2010); no Crossref DOI — JMLR volume-11 record, ACM DL
  10.5555/1756006.1859921].
- Varoquaux quantifies the small-sample regime: sample sizes typical of neuroimaging "inherently
  lead to large error bars (e.g. ±10 % for 100 samples)", and "the standard error across folds
  strongly underestimates them" [VERIFIED-ABSTRACT, doi:10.1016/j.neuroimage.2017.06.061;
  arXiv:1706.07581].

**What 4–13 proteins can actually show — the arithmetic.** Two derivations, both stated so they can
be checked.

_Paired minimum detectable effect._ For a paired comparison (same protein, adapted pipeline vs
fixed pipeline) with n = 13, two-sided α = 0.05 and 80 % power, the minimum detectable mean
difference is (t₀.₀₂₅,₁₂ + t₀.₂₀,₁₂)·SD_diff/√13 = (2.179 + 0.873)·SD_diff/3.606 ≈ **0.846·SD_diff**.
At n = 4 (df = 3) the same expression gives (3.182 + 0.978)/2 ≈ **2.08·SD_diff**. So: if the paired
per-protein AUC difference has SD 0.05, adaptation must buy ≈ **0.042 AUC** to be detectable at
n = 13 and ≈ **0.104 AUC** at n = 4. If the paired SD is 0.10, those become 0.085 and 0.208.
[UNVERIFIED — standard paired-t power arithmetic performed in this document; the assumed SD_diff is
an assumption, and the real value must be measured, not guessed. The pairing is what makes this
tractable: between-protein variance, which the task brief says dominates, cancels in the difference.]

_Capacity budget._ A selector that picks one of m arms per protein has n·log₂(m) bits of freedom.
At n = 13, m = 4 that is 26 bits — enough to reproduce any assignment of 26 binary outcomes. At
n = 4, m = 4 it is 8 bits. **A per-instance selector with free parameters is not identifiable at
our N, and no cross-validation scheme repairs that**; nested LOO at n = 13 gives an outer loop of
13 estimates each built on 12 proteins, which controls the _bias_ Varma & Simon describe while
leaving the _variance_ Varoquaux describes untouched. [UNVERIFIED — an information-counting argument
stated here, consistent with the three cited results but not itself retrieved from one.]

### Table

| Model or method                              | Year        | Input                           | Output                                         | Training data                      | MD-derived? | Licence                            | Relevance to us                                                                           |
| -------------------------------------------- | ----------- | ------------------------------- | ---------------------------------------------- | ---------------------------------- | ----------- | ---------------------------------- | ----------------------------------------------------------------------------------------- |
| Rice algorithm-selection framework           | 1976        | instance features               | mapping instance → algorithm                   | n/a (formalism)                    | No          | n/a                                | Names our exact problem; nothing more                                                     |
| SATzilla                                     | 2008        | SAT instance features           | per-instance solver choice                     | thousands of SAT instances         | No          | academic                           | Canonical architecture: features + presolvers + performance models + argmax               |
| Automated Algorithm Selection survey         | 2019        | —                               | survey                                         | —                                  | No          | n/a                                | States the field's scope; every success is at large n                                     |
| auto-sklearn                                 | 2015        | tabular dataset + meta-features | pipeline + ensemble                            | 100+ prior datasets for warm-start | No          | BSD-3                              | Warm-start + post-hoc ensemble; the ensemble half transfers, the warm-start half does not |
| Meta-features for meta-learning              | 2022        | —                               | taxonomy of meta-features                      | —                                  | No          | n/a                                | Criteria for a good meta-feature set                                                      |
| Stacked generalisation / stacked regressions | 1992 / 1996 | base-model predictions          | combined prediction                            | CV folds                           | No          | n/a                                | Ensembling as the alternative to selection                                                |
| Ensemble selection from model libraries      | 2004        | model library                   | forward-selected ensemble                      | target metric on a hillclimb set   | No          | n/a                                | Optimise the metric you are scored on, directly                                           |
| Self-tuning spectral clustering              | 2004        | point set                       | clusters, k, local scales σᵢ                   | **none — label-free**              | No          | **no DOI issued**                  | Removes the global bandwidth hyperparameter; maps to our edge weights                     |
| Eigengap heuristic                           | 2007        | graph Laplacian spectrum        | number of clusters                             | **none — label-free**              | No          | arXiv                              | Label-free module count from our own graph                                                |
| Markov stability                             | 2010        | graph                           | partition quality as a function of Markov time | **none — label-free**              | No          | published method; `PyGenStability` | **Label-free selection of diffusion time** — the closest match to our problem             |
| Markov stability on proteins                 | 2011        | protein graph                   | multi-scale organisation + robustness          | **none**                           | No          | published method                   | Same idea already applied to protein structure graphs                                     |
| Stability selection                          | 2010        | data + selection algorithm      | recurrent structures with error control        | subsamples                         | No          | n/a                                | Perturb-and-keep-what-survives, as a ranking criterion                                    |
| Nested cross-validation                      | 2006        | data                            | unbiased error estimate                        | —                                  | No          | n/a                                | Required if anything at all is tuned                                                      |
| Over-fitting in model selection              | 2010        | —                               | variance of the selection criterion            | —                                  | No          | JMLR, **no Crossref DOI**          | Explains _why_ small-n selection inflates                                                 |
| CV failure at small n                        | 2018        | —                               | error-bar magnitude                            | —                                  | No          | arXiv:1706.07581                   | ±10 % at n = 100; our n is an order of magnitude smaller                                  |

---

## Q4. Protein descriptors for the meta-feature vector

### Synthesis

The task brief's own diagnosis — size, fold class, oligomeric state, surface-to-volume, domain
count, active-site burial, apo–holo conformational change — is a list of _candidate meta-features_.
Only some of them are computable from an apo structure, and one of them is not computable at all
without violating C1.

**Computable from apo coordinates, zero training, deterministic.**

- _Size and shape._ Residue count N; radius of gyration R_g; the ratio R_g/N^(1/3), which is
  dimensionless and separates compact from extended folds. Solvent-accessible surface area from
  Shrake–Rupley rolling-probe integration gives surface-to-volume directly.
- _Secondary-structure composition._ DSSP assigns secondary structure, geometric features and
  solvent exposure from coordinates alone [VERIFIED-ABSTRACT, doi:10.1002/bip.360221211].
- _Contact order._ Plaxco, Simons & Baker established that the average sequence separation between
  contacting residues in the native state correlates with folding rate and transition-state
  placement across non-homologous single-domain proteins, so that "proteins featuring primarily
  sequence-local contacts tend to fold more rapidly … than those characterized by more non-local
  interactions" [VERIFIED-ABSTRACT, doi:10.1006/jmbi.1998.1645]. **This is the field's canonical
  demonstration that a single scalar topology descriptor predicts a protein's kinetic behaviour.**
  It is the strongest precedent in the literature for the whole idea of this file, and it costs one
  pass over the contact map.
- _Burial depth of the active site._ Residue depth measures "the extent of atom/residue burial
  within a protein" and "correlates with properties such as protein stability, hydrogen exchange
  rate, protein–protein interaction hot spots, post-translational modification sites and sequence
  variability"; DEPTH also defines buried cavities as those lined by residues whose minimum depth
  exceeds 3.75 Å [VERIFIED-ABSTRACT, doi:10.1093/nar/gkt503]. Applied to the _given_ active site —
  which is an input, not a label — this is a legal and directly relevant meta-feature.
- _Domain count._ SWORD2 (contact-map peeling, no training) or SPECTRUS (spectral clustering of ENM
  distance fluctuations, no training), per Q1. PAE-based partition is the AI alternative.
- _Disorder content._ IUPred3 or flDPnn, per Q2. Both legal.
- _Fold class._ Foldseek 3Di search against a reference set, or a CATH/SCOP assignment.
- _Oligomeric state._ Readable from the deposited assembly of the apo entry. **Note C5 and ADR 0010:
  the node set is every modelled residue of the frozen chain, so oligomeric state enters as a
  descriptor, not as a change to the graph.**

**Spectral descriptors of the contact graph.** These are the meta-features most likely to _predict
which propagation parameter is right_, because they are properties of the very operator the
propagation runs on: algebraic connectivity λ₂ of the graph Laplacian; the spectral gap λ₂ − λ₁ and
the eigengap sequence; spectral radius; mean and variance of the degree distribution; the
eigenvalue-spectrum shape. Protein contact networks are known to be small-world — "regular packing
is preserved in short-range interactions, but short average path lengths are achieved through some
long-range contacts" — measured over 595 non-homologous proteins [VERIFIED-ABSTRACT,
doi:10.1016/S0006-3495(04)74086-2]. The GNM literature is in effect a fifty-paper demonstration
that the Kirchhoff-matrix spectrum of the contact graph predicts real fluctuation behaviour
[VERIFIED-ABSTRACT, doi:10.1016/S1359-0278(97)00024-2].

**The direct precedent for "descriptors predict which method will work" in structural biology** is
thinner than in AutoML and should not be oversold. The strongest instances retrieved this session
are indirect: contact order predicting folding rate (above); Beglov et al.'s finding that
cryptic-site regions have above-average flexibility and a nearby hot spot, i.e. that a structural
descriptor predicts a _behaviour_ [VERIFIED-ABSTRACT, doi:10.1073/pnas.1711490115]; and CryptoBench's
demonstration that apo-vs-holo input status alone changes measured performance enough to make
holo-based assessment "unrealistic" [VERIFIED-ABSTRACT, doi:10.1093/bioinformatics/btae745]. **A
paper that fits a meta-model predicting binding-site-predictor performance from protein descriptors
was not retrieved by the recorded search.** That is a negative result under ADR 0019, not an
absence claim — but it means our front end would be building on an analogy to AutoML, not on an
established structural-bioinformatics practice, and the write-up must say so.

**The one descriptor we must not use.** "How much conformational change separates apo from holo" is
in the task brief's own list of what distinguishes the proteins. **It is holo-derived and its use
anywhere on the prediction path violates C1.** It may appear only in post-hoc analysis of results
under `groundtruth/`, never as a meta-feature. Flagging this explicitly because it is the one item
on the brief's list that looks innocuous and is not.

### Table

| Model or method                           | Year | Input              | Output                                | Training data                       | MD-derived? | Licence                | Relevance to us                                                 |
| ----------------------------------------- | ---- | ------------------ | ------------------------------------- | ----------------------------------- | ----------- | ---------------------- | --------------------------------------------------------------- |
| Contact order                             | 1998 | contact map        | one scalar                            | **none**                            | No          | n/a                    | Canonical precedent: topology scalar predicts kinetic behaviour |
| DSSP                                      | 1983 | coordinates        | secondary structure, exposure         | **none**                            | No          | free for academic use  | SS composition meta-feature                                     |
| DEPTH residue depth                       | 2013 | coordinates        | per-residue depth, cavity detection   | **none**                            | No          | web server             | Active-site burial depth, legal (site is an input)              |
| Small-world analysis of contact networks  | 2004 | contact graph      | path length, clustering, degree stats | **none** (measured on 595 proteins) | No          | n/a                    | Justifies degree/path meta-features                             |
| GNM Kirchhoff spectrum                    | 1997 | contact graph      | eigenvalues, mode shapes              | **none**                            | No          | ProDy MIT              | λ₂, spectral gap, mode participation as meta-features           |
| SWORD2                                    | 2022 | coordinates        | domain count/boundaries               | **none**                            | No          | code public            | Domain-count meta-feature                                       |
| SPECTRUS                                  | 2015 | coordinates        | quasi-rigid domain count              | **none**                            | No          | published method       | Domain-count meta-feature, ENM-native                           |
| Foldseek 3Di                              | 2024 | coordinates        | fold descriptor / neighbours          | alphabet learned on structures      | No          | GPLv3                  | Fold-class meta-feature                                         |
| IUPred3                                   | 2021 | sequence           | disorder propensity                   | biophysics + annotation             | No          | academic use           | Disorder-content meta-feature                                   |
| flDPnn                                    | 2021 | sequence           | disorder + functions                  | DisProt/CAID                        | No          | web server             | Disorder-content meta-feature, CAID-assessed                    |
| AlphaFold PAE partition                   | 2021 | sequence           | inter-domain rigidity map             | PDB                                 | No          | Apache-2.0 / CC-BY-4.0 | AI alternative to SWORD2/SPECTRUS                               |
| **Apo–holo RMSD / conformational change** | —    | **holo structure** | magnitude of induced fit              | n/a                                 | No          | n/a                    | **C1 VIOLATION — never a meta-feature; analysis only**          |

---

## Q5. Leakage and fairness — how to do this defensibly

### Synthesis

**Contamination in structural-bioinformatics benchmarks is documented, quantified, and taxonomised.**
Kapoor & Narayanan surveyed 17 fields, found leakage affecting **294 papers**, "in some cases,
leading to wildly overoptimistic conclusions", and give a taxonomy of eight leakage types
[VERIFIED-ABSTRACT, doi:10.1016/j.patter.2023.100804]. In our own neighbourhood: random splitting of
sequence datasets leaves "evolutionarily related homologs of training sequences … in validation and
test data, causing predictive performance to be overestimated", which is precisely what GraphPart's
homology partitioning exists to prevent [VERIFIED-ABSTRACT, doi:10.1093/nargab/lqad088]. Park &
Marcotte show the pair-input version: random division "without regard to the partitioning of test
pairs into distinct classes … can therefore misrepresent overall predictive performance"
[VERIFIED-ABSTRACT, doi:10.1038/nmeth.2259]. In virtual screening, superior CNN enrichment on DUD-E
"can be attributed to the analogue and decoy bias hidden in the DUD-E dataset rather than successful
generalization of the pattern of protein–ligand interactions"
[VERIFIED-ABSTRACT, doi:10.1371/journal.pone.0220113]. Our own field's instance is already in
`00-conventions.md` §6: AlloBench's UniRef50 declustering drops every tool below 60 %
[VERIFIED-ABSTRACT, doi:10.1021/acsomega.5c01263].

**Is a model pretrained on the whole PDB/UniRef "leaked" against a PDB-drawn benchmark? The field
now has a direct empirical answer, and it is uncomfortable.** Szymborski & Emad demonstrate that
"existing pre-trained pLMs are a source of data leakage for the downstream PPI task", because "the
pre-training of pLMs is commonly conducted on datasets such as UniRef constructed without regard to
the evaluation of downstream tasks, with most proteins in the testing dataset of the downstream PPI
task certain to appear in the dataset used to pre-train pLMs", and they measure "measurable
inflation of testing scores" by comparing strict-vs-non-strict leakage controls
[VERIFIED-ABSTRACT, doi:10.1038/s42256-025-01176-7; preprint bioRxiv 2025.04.21.649858. **The
abstract does not give the numeric size of the inflation; the full text was not landed this
session.**]. From inside the foundation-model literature, AF2BIND's authors note that "direct
comparison of AF2BIND to other ligand-binding-site predictors is challenging because most published
train/test data-splits contain significant amounts of data leakage"
[VERIFIED-FULLTEXT, recorded in `02-ai-methods.md` §6, bioRxiv 2023.10.15.562410].

**How the field handles it in practice, and what actually resolves it for us.** The honest reading
is that "pretrained on a corpus containing my test protein" is a _spectrum_, and the relevant
question is not whether the structure was seen but whether **the label** was. Three positions:

1. _Structure seen, label never existed in the pretraining task._ ESM-2 saw our targets' sequences;
   AF2 saw their apo structures. Neither loss function contains an allosteric-site label, a holo
   pocket, or an MD trajectory. The pretraining task (masked-token recovery, structure prediction)
   is not our evaluation task (ranking distal residues by connectivity to a given active site).
   This is the weakest form of contamination and is, in our judgement, acceptable **if disclosed
   and ablated**.
2. _Label-bearing corpus._ Any ASD/ASBench/CASBench-trained tool. Already handled by
   `02-ai-methods.md` §10's "Legal\*" gate, and unchanged by this file.
3. _MD-bearing corpus._ Barred outright by C2, independent of any leakage argument.

The Szymborski & Emad result is a genuine complication for position 1 and should not be waved away.
Its mechanism, though, is specific: PPI inference asks a question **about the pairs of proteins in
the pretraining corpus**, so the pretrained representation can encode the answer. Our question is
about which residues within one protein are dynamically coupled to a given site — a property no
step of MLM or structure-prediction pretraining is optimised to represent. **That is an argument,
not a measurement.** The measurement that settles it is the ablation in the disclosure protocol
below, item 5.

**Temporal holdouts.** CASP established "fully blinded testing of structure prediction methods"
by predicting structures before their release [VERIFIED-ABSTRACT, doi:10.1002/prot.340230303].
CAMEO automates it: "fully automated blind prediction assessments based on the weekly pre-release
of sequences of those structures, which are going to be published in the next release of the PDB"
[VERIFIED-ABSTRACT, doi:10.1002/prot.25431]. AlphaFold-family training uses an explicit date cutoff
for the same reason. **A date-based holdout is not available to us**: our targets are long-published
landmark proteins, and every pretrained model's corpus postdates them. Saying so plainly is better
than implying a control we do not have.

**Reporting frameworks.** DOME gives "community-wide recommendations for reporting supervised
machine learning–based analyses applied to biological studies", structured as Data, Optimization,
Model, Evaluation, and is explicitly designed "to help both reviewers and readers to better
understand and assess the performance and limitations of a method"
[VERIFIED-ABSTRACT, doi:10.1038/s41592-021-01205-4]. We should adopt DOME's four headings verbatim
rather than invent our own.

### A concrete disclosure protocol we can adopt

Eight items. Each is checkable by a reviewer without trusting us.

1. **Pin every artifact.** For each pretrained component: package name, checkpoint identifier,
   parameter count, release date, download hash, and licence — in a machine-readable block committed
   beside the results, not in prose.
2. **State the pretraining corpus and its cutoff.** Name the corpus (UniRef50/90, PDB, AFDB, ATLAS,
   …), its size, and the date at which it was frozen. If unknown, write "not determined".
3. **Assert three negatives, and make one of them a test.** (a) No allosteric label anywhere in the
   component's training. (b) No holo structure of any benchmark target. (c) No MD trajectory.
   Negative (c) is the C2 gate and should be enforced the way `tests/test_no_leakage.py` already
   enforces the file-read routes: an allow-list of admitted checkpoints, with a test that fails when
   anything not on it is loaded on the prediction path.
4. **Disclose the contamination we cannot remove.** State explicitly that our targets' apo sequences
   and structures are in the PDB and UniRef and therefore in essentially every pretrained corpus;
   state that a date-based holdout is impossible for these targets; cite Szymborski & Emad as the
   known counter-argument rather than omitting it.
5. **Ship the substitution ablation.** Report the identical pipeline with each pretrained component
   replaced by a zero-training physics substitute — pLDDT-flexibility → GNM mean-square fluctuation;
   PAE-domains → SPECTRUS or SWORD2; PLM embedding → one-hot amino acid plus DSSP class. **The delta
   between the two is the only defensible statement of what the pretrained model contributed.** If
   the delta is inside the noise, say so and drop the component; that is a smaller, faster pipeline
   and a stronger paper.
6. **Pre-register the adaptation rule.** Freeze the meta-feature list, the adaptation function and
   the seed in a committed file _before_ scoring, and record the commit hash in the results. This
   converts "we chose the rule that worked" into a checkable claim.
7. **Publish the meta-feature vector per target.** One CSV. A reviewer can then re-derive the
   adaptation for any protein and check that the rule was applied as stated.
8. **Report under DOME's four headings** (Data, Optimization, Model, Evaluation), and report both a
   ranking metric and a localisation metric as `02-ai-methods.md` §12 already requires.

### Table

| Model or method                       | Year  | Input                  | Output                                       | Training data          | MD-derived? | Licence     | Relevance to us                                                                   |
| ------------------------------------- | ----- | ---------------------- | -------------------------------------------- | ---------------------- | ----------- | ----------- | --------------------------------------------------------------------------------- |
| Leakage taxonomy (Kapoor & Narayanan) | 2023  | —                      | 8-type leakage taxonomy; 294 affected papers | survey of 17 fields    | No          | n/a         | Vocabulary for the disclosure section                                             |
| GraphPart                             | 2023  | sequence set           | homology-aware partition                     | n/a (algorithm)        | No          | code public | How to split if we ever fit anything on external proteins                         |
| Pair-input evaluation flaws           | 2012  | —                      | evaluation-scheme critique                   | —                      | No          | n/a         | Why random splits overstate                                                       |
| DUD-E hidden bias                     | 2019  | —                      | decoy/analogue-bias demonstration            | DUD-E                  | No          | n/a         | Benchmark structure, not model quality, drove the numbers                         |
| pLM leakage in PPI inference          | 2026  | —                      | measured inflation from pretrained pLMs      | UniRef-pretrained pLMs | No          | n/a         | **The direct counter-argument to "pretrained ≠ leaked"; magnitude not retrieved** |
| AlloBench declustering                | 2025  | allosteric benchmark   | UniRef50-declustered re-benchmark            | ASD-derived            | No          | n/a         | Our field's own instance; every tool < 60 %                                       |
| CASP                                  | 1995– | pre-release targets    | blind assessment                             | n/a                    | No          | n/a         | Temporal-holdout gold standard we cannot use here                                 |
| CAMEO                                 | 2018  | weekly PDB pre-release | continuous blind assessment                  | n/a                    | No          | n/a         | Automated temporal holdout                                                        |
| DOME                                  | 2021  | —                      | reporting checklist                          | —                      | No          | n/a         | Adopt its four headings verbatim                                                  |

---

## Q6. Precedent for AI + quantum hybrid pipelines

### Synthesis

**Classical preprocessing to fit a problem onto few qubits is standard and uncontroversial — when
its cost is counted.** Three established forms:

- _Symmetry-based qubit reduction._ Bravyi et al.'s tapering exploits symmetries so that "encodings
  eliminat[e] redundant degrees of freedom in a way that preserves a simple structure of the system
  Hamiltonian enabling quantum simulations with fewer qubits"
  [VERIFIED-ABSTRACT, arXiv:1701.08213]. This is exact, not heuristic — the model is unchanged.
- _Coarse-graining before encoding._ The IBM protein-folding work places the chain on a
  coarse-grained tetrahedral lattice with restricted freedom of movement, giving an O(N⁴) model
  Hamiltonian and a variational algorithm on it
  [VERIFIED-ABSTRACT, doi:10.1038/s41534-021-00368-4]. The classical coarse-graining is what makes
  the quantum step possible, and the paper is judged on the quantum step. **This is the closest
  published template for our own S2 coarse-graining feeding S5.**
- _Feature selection to reduce the qubit count._ Mücke et al. formulate feature selection as a QUBO
  "based on their importance and redundancy", solved on classical hardware, a gate device and an
  annealer [VERIFIED-ABSTRACT, doi:10.1007/s42484-023-00099-z, arXiv:2203.13261]. Light-cone feature
  selection is a more recent variant tailored to the circuit's causal structure
  [VERIFIED-ABSTRACT, doi:10.1002/qute.202400647, arXiv:2403.18733]. The general practice — reduce
  dimensionality classically because "each qubit is associated with a feature" and NISQ qubit counts
  are small — is ubiquitous [VERIFIED-ABSTRACT, retrieved 2026-08-26 across the QML feature-selection
  literature].

**Classical models choosing a quantum algorithm's parameters is also established.** Verdon et al.
train classical neural networks to produce good initialisations for QAOA and VQE circuits,
addressing the fact that parameter initialisation determines "rapid and consistent convergence to
local minima of the parameterized quantum circuit landscape" [VERIFIED-ABSTRACT, arXiv:1907.05415].
Khairy et al. learn optimisation policies for variational circuits on combinatorial problems
[VERIFIED-ABSTRACT, doi:10.1609/aaai.v34i03.5616, arXiv:1911.11071]. **Most directly relevant to
this file: Moussa, Calandra & Dunjko explicitly import algorithm selection into quantum
optimisation**, studying "how to detect problem instances where QAOA is most likely to yield an
advantage over a conventional algorithm" [VERIFIED-ABSTRACT, doi:10.1088/2058-9565/abb8e5,
arXiv:2001.08271]. That paper is the single best citation for "an AI front end that decides how to
run the quantum stage" and it does exactly what the PI is asking for, in a different domain.

**Classical shadows** are the postprocessing counterpart: an approximate classical description of a
quantum state from few measurements, sufficient to predict M properties with O(log M) measurements
[VERIFIED-ABSTRACT, doi:10.1038/s41567-020-0932-7]. Relevant to us as an efficient readout if any
observable is ever measured on hardware.

**How to describe the division of labour so the quantum part is the contribution, not the
decoration.** The literature's answer is an ablation plus an accounting, not a narrative.

1. **Count the classical work in the end-to-end claim.** Aaronson's "Read the fine print" is the
   canonical statement that the caveats — state preparation, readout, and the classical work
   surrounding the quantum core — can consume the advertised speed-up
   [VERIFIED-ABSTRACT, doi:10.1038/nphys3272].
2. **Ablate the quantumness.** Bowles, Ahmed & Schuld benchmarked 12 QML models on 160 datasets and
   found that "out-of-the-box classical machine learning models outperform the quantum classifiers"
   and, decisively, that "removing entanglement from a quantum model often results in as good or
   better performance, suggesting that 'quantumness' may not be the crucial ingredient"
   [VERIFIED-ABSTRACT, arXiv:2403.07059]. **The operational lesson: report the same pipeline with
   the quantum stage's distinctively quantum feature removed.** For us that is a CTQW with coherence
   destroyed, or the quantum observable replaced by its classical transfer-amplitude equivalent —
   which is exactly the collapse `00-conventions.md` §5 items 9–11 already prove algebraically for
   three observables.
3. **Check for a classical surrogate.** Schreiber, Eisert & Meyer define "a classical model which
   can be efficiently obtained from a trained quantum learning model and reproduces its input–output
   relations" [VERIFIED-ABSTRACT, doi:10.1103/PhysRevLett.131.100803]. If our observable has a
   cheap classical surrogate, that must be stated, not discovered by a reviewer.
4. **Do not frame the contribution as "advantage".** Schuld & Killoran argue the field should ask
   better-posed questions than quantum advantage, given that ML is hard to study theoretically and
   quantum computing lacks realistic-scale benchmarks
   [VERIFIED-ABSTRACT, doi:10.1103/PRXQuantum.3.030101]. Combined with C3, the defensible framing is:
   _here is the observable, here is its qubit count / depth / connectivity, here is what it buys
   over the best classical readout on an identical input, and here is the ablation showing where
   the buy comes from._
5. **Be careful about kernel-style claims specifically.** Bandwidth is a hyperparameter that
   "controls the expressivity of the resulting model", with behaviour running from underfitting to
   overfitting as it varies [VERIFIED-ABSTRACT, doi:10.1103/PhysRevA.106.042407] — which is the
   published basis for `00-conventions.md` §5's statement that a bandwidth-tuned quantum kernel
   becomes indistinguishable from an RBF kernel.

**The division of labour this supports for us.** Classical/AI owns: input characterisation (S0),
graph construction and coarse-graining (S1–S2), confound removal and site assembly (S6–S7). Quantum
owns: propagation and the observable (S5). The AI front end is legitimate precisely because it does
not touch S5 — it chooses _how the graph is presented to_ S5, in the same way the tetrahedral
lattice chooses how the chain is presented to the IBM folding circuit. It becomes illegitimate the
moment it can be shown to produce the ranking on its own; hence ablation item 2.

### Table

| Model or method                       | Year | Input                          | Output                                             | Training data           | MD-derived? | Licence                | Relevance to us                                                                                |
| ------------------------------------- | ---- | ------------------------------ | -------------------------------------------------- | ----------------------- | ----------- | ---------------------- | ---------------------------------------------------------------------------------------------- |
| Qubit tapering (Z₂ symmetries)        | 2017 | Hamiltonian + symmetries       | reduced-qubit Hamiltonian                          | n/a                     | No          | n/a                    | Exact classical reduction; the gold standard for "preprocessing that costs nothing scientific" |
| Coarse-grained lattice folding VQE    | 2021 | sequence → tetrahedral lattice | folded conformation                                | n/a                     | No          | Qiskit                 | Template: classical coarse-graining enables the quantum step; quantum step is judged           |
| Feature selection as QUBO             | 2023 | feature set                    | selected subset                                    | dataset-specific        | No          | code public            | Precedent for classical selection reducing qubit count                                         |
| Light-cone feature selection          | 2025 | features + circuit structure   | selected subset                                    | dataset-specific        | No          | published method       | Selection tailored to the circuit's causal cone                                                |
| Learning-to-learn for VQC init        | 2019 | problem instance               | initial circuit parameters                         | QAOA/VQE instances      | No          | code public            | Classical NN chooses quantum parameters                                                        |
| RL optimiser for variational circuits | 2020 | problem instance               | optimisation policy                                | combinatorial instances | No          | code public            | Same pattern, learned control loop                                                             |
| **Algorithm selection for QAOA**      | 2020 | instance features              | run quantum or classical?                          | optimisation instances  | No          | published method       | **Closest precedent to the PI's proposal**                                                     |
| Classical shadows                     | 2020 | few measurements               | classical description of the state                 | n/a                     | No          | n/a                    | Efficient readout for a hardware run                                                           |
| Classical surrogates                  | 2023 | trained quantum model          | efficient classical equivalent                     | n/a                     | No          | n/a                    | The test our observable must survive                                                           |
| Kernel bandwidth in QML               | 2022 | quantum kernel + bandwidth     | expressivity control                               | benchmark datasets      | No          | n/a                    | Basis for the pre-refuted quantum-kernel branch                                                |
| Benchmarking QML honestly             | 2024 | 12 models × 160 datasets       | classical models win; entanglement often unhelpful | benchmark datasets      | No          | PennyLane, open source | Supplies the ablation standard we should adopt                                                 |
| "Read the fine print"                 | 2015 | —                              | caveat inventory                                   | —                       | No          | n/a                    | Count the classical work in the claim                                                          |
| Is quantum advantage the right goal?  | 2022 | —                              | reframing                                          | —                       | No          | n/a                    | How to state the contribution without an advantage claim                                       |

---

## Admissibility table

The single most important output. "Trained on holo structures?" is answered for the model's own
pretraining corpus; the separate per-target overlap check that `02-ai-methods.md` §3 calls "Legal\*"
still applies to anything trained on an allostery-curated set, and none of the rows below are.

| Model                                          | What it gives us                                       | Trained on MD?                                               | Trained on holo structures?                                         | Admissible under "no MD trajectories as input"?               | Our verdict                                                                                                                                                                                               |
| ---------------------------------------------- | ------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------------- | ------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **GNM / ANM (ProDy)**                          | per-residue fluctuation, modes, λ₂, mode participation | **No — no training at all**                                  | No                                                                  | **Yes**                                                       | **Adopt as the default flexibility feature.** Zero parameters, C6-native, and the control every learned alternative must beat.                                                                            |
| **SWORD2**                                     | domain count and boundaries                            | **No — no training**                                         | No                                                                  | **Yes**                                                       | **Adopt** for the domain meta-feature; nothing learned can be leaked through it.                                                                                                                          |
| **SPECTRUS**                                   | quasi-rigid domain count from ENM fluctuations         | **No — no training**                                         | No                                                                  | **Yes**                                                       | **Adopt** as the ENM-consistent alternative to SWORD2; agreement between the two is a free sanity check.                                                                                                  |
| **Foldseek 3Di**                               | fold-class descriptor, structural alphabet per residue | No                                                           | No (alphabet learned on structure pairs, not on ligand-bound state) | **Yes**                                                       | **Adopt.** GPLv3, deterministic, no GPU, best risk-adjusted meta-feature in the survey.                                                                                                                   |
| **DSSP / SASA / contact order / R_g**          | size, shape, SS composition, topology scalars          | **No — no training**                                         | No                                                                  | **Yes**                                                       | **Adopt.** These are arithmetic on the apo coordinates; there is nothing to leak.                                                                                                                         |
| **DEPTH (residue depth)**                      | burial depth of the _given_ active site                | **No — no training**                                         | No                                                                  | **Yes**                                                       | **Adopt.** The active site is an input under the challenge, not a label, so conditioning on it is legal.                                                                                                  |
| **IUPred3 / flDPnn**                           | disorder content                                       | No (biophysical energy estimation; DisProt/CAID annotations) | No                                                                  | **Yes**                                                       | **Adopt one, not both.** IUPred3 if we want zero dependencies; flDPnn if CAID-assessed accuracy matters.                                                                                                  |
| **AlphaFold2 pLDDT**                           | disorder / low-confidence fraction                     | No                                                           | No (PDB + self-distillation)                                        | **Yes**                                                       | **Admissible, use with a caveat and an ablation.** Its measured disorder AUC (0.77) is below dedicated predictors (~0.80) and it fails on the Disorder-NOX definition; report it against the GNM control. |
| **AlphaFold2 PAE**                             | inter-domain rigidity, domain partition                | No                                                           | No                                                                  | **Yes**                                                       | **Admissible but redundant.** SWORD2/SPECTRUS give the same meta-feature with no model dependency; use PAE only if the two disagree and we need a tiebreak.                                               |
| **ESM-2 / ProtT5 / Ankh embeddings**           | per-residue sequence context, attention                | No                                                           | No (UniRef/BFD sequences only)                                      | **Yes**                                                       | **Admissible, low expected value.** PLM signal is already measured to collapse on allosteric sites (AUPR 0.06). Use for meta-features, not for the ranking.                                               |
| **ESM-3 / ESM-C 600M**                         | multimodal embeddings                                  | No                                                           | No                                                                  | **Yes technically**                                           | **Reject on licence.** Cambrian Non-Commercial forecloses any commercial path and complicates a competition submission; ESM-2 (MIT) does the same job.                                                    |
| **ESM-IF1 / ProteinMPNN**                      | structure-conditioned per-residue features             | No                                                           | No (backbones; ESM-IF adds 12 M AF2-predicted structures)           | **Yes**                                                       | **Admissible, hold in reserve.** Legal and cheap, but no allostery-specific validation exists; try only after the physics features are exhausted.                                                         |
| **SaProt / GearNet / ProstT5**                 | fold-aware embeddings                                  | No                                                           | No (AFDB / sequence–structure pairs)                                | **Yes**                                                       | **Admissible, not recommended now.** Each adds a heavyweight dependency for a meta-feature Foldseek 3Di already supplies.                                                                                 |
| **AlphaFold3**                                 | structure, pLDDT, PAE                                  | No                                                           | No                                                                  | **Yes technically**                                           | **Reject on licence and reproducibility.** Weights on request, non-commercial only — an unreproducible pipeline component.                                                                                |
| **AF2 + MSA subsampling / AF-Cluster**         | apo conformational ensemble                            | **No**                                                       | No                                                                  | **Yes**                                                       | **Admissible; treat as an experiment, not a component.** It is the only legal ensemble route, but AF-Cluster's mechanism is contested in Nature and neither is validated for allostery.                   |
| **AlphaFlow (PDB variant)**                    | conformational ensemble                                | **No**                                                       | No                                                                  | **Yes**                                                       | **Admissible; same caveat.** Must be the PDB checkpoint, verified by hash, never the MD checkpoint.                                                                                                       |
| **AlphaFlow (MD-finetuned)**                   | conformational ensemble                                | **Yes**                                                      | No                                                                  | **No**                                                        | **Reject.** Weights fit on all-atom MD ensembles; single-sequence inference does not launder that.                                                                                                        |
| **Distributional Graphormer (DiG)**            | equilibrium distribution                               | **Not determined for the released protein checkpoint**       | No                                                                  | **No**                                                        | **Reject pending provenance.** C2 makes undetermined provenance a disqualification; revisit only if the checkpoint's training source is documented.                                                       |
| **BioEmu**                                     | equilibrium structure ensemble                         | **Yes — >200 ms aggregate MD**                               | No                                                                  | **No**                                                        | **Reject.** The most compliant-looking violation in the survey: sequence in, ensemble out, MD in the weights.                                                                                             |
| **PEGASUS**                                    | per-residue RMSF, φ/ψ SD, mean LDDT                    | **Yes — ATLAS MD database**                                  | No                                                                  | **No**                                                        | **Reject.** It predicts MD-derived quantities by construction; the target variable is the violation.                                                                                                      |
| **PocketMiner**                                | per-residue cryptic-pocket-opening probability         | **Yes — 2 400 MD runs, 37 proteins, LIGSITE labels**         | No                                                                  | **No**                                                        | **Reject.** Confirmed from full text; the label is literally "did a pocket open during MD".                                                                                                               |
| **CryptoSite**                                 | cryptic-site score                                     | **Yes — and new MD at inference**                            | Uses apo–holo pairs to define cryptic sites                         | **No**                                                        | **Reject twice over.** Barred at training and at inference.                                                                                                                                               |
| **CrypticScout / CrypToth**                    | probe hotspot map                                      | **Yes — mixed-solvent MD is the method**                     | No                                                                  | **No**                                                        | **Reject.** Not MD-trained but MD-_run_; the most direct C2 violation possible.                                                                                                                           |
| **MEDUSA / DynaMine / B-factor Bi-LSTM**       | predicted flexibility from sequence                    | **No** — X-ray B-factors / NMR S²                            | No                                                                  | **Yes**                                                       | **Admissible; use only as a comparator.** Legal, but a GNM profile on our own graph is cheaper and already inside the model class C6 commits us to.                                                       |
| **PredyFlexy**                                 | flexibility + local structure                          | **Training data not determined**                             | Unknown                                                             | **Unresolved**                                                | **Do not use** until the training label is established; an undetermined provenance is the same as a failed one under C2.                                                                                  |
| **Any ASD/ASBench/CASBench-trained predictor** | allosteric-site ranking                                | No                                                           | Yes, by construction of the label                                   | Legal on C2, **fails the `02-ai-methods.md` §3 overlap gate** | **Out of scope for this file** — that is an output model, not a front end, and it is already gated.                                                                                                       |
| **Apo–holo conformational-change descriptor**  | "how much induced fit this target shows"               | n/a                                                          | **Yes, by definition**                                              | **No — C1**                                                   | **Reject absolutely.** It is on the brief's own list of distinguishing properties and it is the one item there that is an answer key.                                                                     |

---

## Recommended preprocessing architecture

A concrete, implementable design. It is deliberately **not** a learned selector, because Q3's
arithmetic says a learned selector cannot be validated at our N. It is a **label-free adaptation
rule plus a stability-filtered ensemble**, which needs no validation set because it fits nothing.

### Stage S0 — `characterise`

A new module `src/allo/network/characterise.py` (it belongs in `network/` because it consumes a
`ResidueGraph` and emits numbers, and `network/` is already the stage that owns the graph). One
function:

```
characterise(graph) -> dict[str, float]
```

taking the `ResidueGraph` that `allo.network.build` already returns and the active-site residue set
that `allo.inputs` already supplies. It must not import `allo.groundtruth` or `allo.scoring`.

**Meta-features, all deterministic, all from apo coordinates.** Fourteen, grouped, each normalised
so a value means the same thing at N = 150 and N = 900:

_Size and shape (4)_ — `n_residues`; `rg_over_n_cbrt` = R_g / N^(1/3); `sasa_per_residue`;
`sphericity` from SASA and enclosed volume.

_Topology of the contact graph (4)_ — `mean_degree`; `degree_cv` (SD/mean, dimensionless);
`relative_contact_order` (Plaxco's normalised form); `mean_shortest_path / log N` (small-world
normalisation, per the 595-protein result).

_Spectrum of the graph Laplacian (3)_ — `lambda2_times_n` (algebraic connectivity, size-normalised);
`spectral_gap_ratio` = (λ₃ − λ₂)/λ₂; `n_modules_eigengap`, the eigengap-heuristic module count.

_Composition and site (3)_ — `helix_frac`, `strand_frac` from DSSP; `site_depth_z`, the mean residue
depth of the given active-site residues expressed as a z-score against the chain's own depth
distribution (self-normalising, so it does not need a cross-protein calibration).

Two more are computed but held **outside** the adaptation rule, for reporting only, because they add
a dependency the rule does not need: `disorder_frac` (IUPred3) and `n_domains_sword2`. Report them;
do not let them drive anything until an experiment shows they do.

**Every one of these is admissible with no model weights at all.** That is the point. The AI content
of the front end is the _pattern_ — instance characterisation driving per-instance configuration —
not a downloaded checkpoint. If the PI wants a pretrained model in the loop, the two lowest-risk
additions are Foldseek 3Di (fold class) and pLDDT (disorder fraction), each admitted only through
the disclosure protocol above and each shipped with its physics substitute for ablation (item 5).

### Stage S0b — `adapt`

Three adaptations, each justified by a specific published criterion, each with **zero free
parameters**.

1. **Diffusion / propagation time — spectral normalisation.** Replace any absolute time `t` with a
   dimensionless `τ`, and set `t = τ / λ₂`. Rationale: λ₂ is the slowest non-trivial relaxation rate
   of the graph Laplacian, so `t·λ₂` is the natural dimensionless time and is comparable across
   proteins of different size and connectivity. This alone should remove a large part of the
   between-protein variance the PI describes, because a fixed `t` is currently a _different physical
   scale_ on every protein. Where a single scale is not enough, scan `τ` on a log grid and select
   the scale by the Markov-stability criterion — the τ-range over which the induced partition is
   most robust (doi:10.1073/pnas.0903215107; protein application doi:10.1088/1478-3975/8/5/055010).
   **No label is consulted at any point.**
2. **Edge weights — local scaling.** Replace a fixed Å cutoff or fixed Gaussian width with a
   per-residue local scale σᵢ = distance to residue _i_'s k-th nearest Cβ neighbour, with edge weight
   exp(−dᵢⱼ²/(σᵢσⱼ)) (Zelnik-Manor & Perona). k is fixed once, globally, at a value that reproduces
   the current default graph's mean degree — so it is a re-parameterisation, not a new knob.
   Rationale: packing density varies by fold class, so a fixed cutoff produces systematically
   different graph density on a compact phosphatase and an extended polymerase, which is precisely
   the failure the brief describes.
3. **Number of modules / smoothing radius — eigengap.** Where a stage needs a module count or a
   spatial smoothing scale, take it from `n_modules_eigengap` rather than from a constant
   (arXiv:0711.0189). Cross-check against SWORD2/SPECTRUS; log disagreements rather than resolving
   them silently.

### Stage S0c — label-free arm retention, instead of arm selection

Run the whole small portfolio of scorers, then keep and combine, rather than pick:

1. **Perturb the graph** R times with an explicit seed: drop a fixed fraction of edges at random,
   and jitter coordinates by a magnitude read from the deposited B-factors the `ResidueGraph`
   already carries.
2. **Compute each arm's rank stability** as the mean Spearman ρ between its ranking on the
   unperturbed graph and on each perturbation. This is stability selection applied to a ranking
   (doi:10.1111/j.1467-9868.2010.00740.x).
3. **Drop arms below a fixed stability floor**, set once and never tuned.
4. **Aggregate the survivors by rank** (Borda / mean midrank). Mean midrank is exactly affine in AUC
   per `09a-power-verification.md`, so this composition is analysable rather than opaque.

**No label is used in steps 1–4.** That is what makes the whole design immune to the leakage question
the PI is trading against — and it means the fairness argument does not have to be made at all,
because there is nothing to be unfair with.

### How to validate this on 4–13 proteins without overfitting

Three tiers, and only the first two are supportable.

**Tier A — no fitting (this is the design above).** Nothing is chosen from data, so there is nothing
to cross-validate. The claim is "spectral normalisation of τ reduces between-protein variance", and
the test is a paired comparison of the adapted pipeline against the fixed-`t` pipeline on the same
arms and the same graphs, through `allo.scoring.score_arm` and no other path. Report the paired
difference with its SD, and report the MDE arithmetic beside it so the reader knows what the test
could and could not have detected. Pre-register the rule (disclosure item 6) before scoring.

**Tier B — at most one global parameter.** If a scan is unavoidable (e.g. the stability floor), fix
it on the `development` tier only, exactly as `../exploration/README.md` already requires, and report
the development number as _selection_, not as a result. One parameter chosen on ~4 development arms
is 2 bits of freedom against 13 arms of eventual evidence — defensible. Two parameters is not.

**Tier C — a learned per-instance selector. Not supportable. Do not build it.** At n = 13 with m = 4
arms the selector has 26 bits of freedom (Q3 capacity budget); nested LOO controls the Varma–Simon
bias but leaves the Varoquaux variance, so the resulting estimate is unbiased and uninformative at
once. If a reviewer asks why we did not build one, the answer is the paired MDE: at n = 13 we
cannot resolve an improvement below ≈ 0.85·SD_diff, and a selector's expected gain over a
well-normalised fixed rule is smaller than that.

**Two mandatory controls, whichever tier.**

- _The substitution ablation_ (disclosure item 5): the same pipeline with each adapted quantity
  reverted to its constant. This isolates what adaptation bought.
- _The quantumness ablation_ (Q6 item 2): the same front end with the quantum observable replaced by
  its classical transfer-amplitude equivalent. Without this, the front end could carry the result and
  the quantum stage would be decoration — the exact failure Bowles, Ahmed & Schuld measured across
  160 datasets.

---

## What the literature does NOT support

Stated so that none of these gets written into `docs/report/` by accident.

1. **It does not support using PocketMiner, CryptoSite, CrypticScout, BioEmu, PEGASUS or MD-finetuned
   AlphaFlow.** Every one is MD-derived. Three of them need only a single structure or sequence at
   inference, which is why they keep getting proposed. Inference cost is not provenance.
2. **It does not support treating pLDDT as an MD-free RMSF.** One study reports a high pLDDT–RMSF
   correlation (doi:10.1038/s41598-022-14382-9); CAID2 and a 20-predictor head-to-head both find
   pLDDT-based disorder below dedicated predictors and failing outright on one of the two reference
   definitions. Quote it as a proxy, with the counter-evidence, or not at all.
3. **It does not support a claim that "pretrained on the PDB is not leakage".** Szymborski & Emad
   measured inflation from exactly that mechanism in PPI inference. Our position — that the
   pretraining task does not contain our label — is an argument that must be backed by the
   substitution ablation, not a settled fact. **The magnitude of the inflation they measured was not
   retrieved this session**; do not quote a number for it.
4. **It does not support a learned per-instance selector at n = 4–13.** Every headline
   algorithm-selection success is on thousands of instances. Nothing in Rice, SATzilla, Kerschke or
   auto-sklearn validates the pattern at our scale, and the small-sample CV literature says
   explicitly that it will not.
5. **It does not supply a precedent for predicting binding-site-predictor performance from protein
   descriptors.** A paper doing this was **not retrieved by the recorded search**. Contact order and
   the cryptic-site structural-origins work are analogies, not precedents. Our front end is
   importing a pattern from AutoML into structural biology, and the write-up must say that plainly
   rather than implying a body of prior work that we did not find.
6. **It does not support using apo–holo conformational change as a meta-feature.** That is C1
   leakage, full stop, and it is on the brief's own list of properties that distinguish the targets.
7. **It does not support claiming a quantum contribution on the strength of a working pipeline.**
   Bowles, Ahmed & Schuld found entanglement removal often _improves_ QML models; Schreiber et al.
   show many quantum models have efficient classical surrogates; Aaronson's caveat says the
   classical work counts. Without both ablations, a good end-to-end number is evidence about the
   front end, not about the circuit.
8. **It does not license ESM-3, ESM-C 600M or AlphaFold3 for an unrestricted submission.** Two are
   non-commercial-only; AF3's weights are request-gated. This is a licence fact, not a scientific
   one, and it is the kind that surfaces late.

---

## What this changes for our pipeline

- **New stage S0, and it is classical.** `characterise` + `adapt` sit in front of S1. The design
  above uses **no model weights at all**, which means the entire fairness/leakage debate the PI has
  been prepared to have does not need to be had. If a pretrained component is added later, it enters
  through the eight-item disclosure protocol and carries its physics substitute for ablation.
- **The highest-value single change is dimensionless propagation time.** Replace absolute `t` with
  `t = τ/λ₂` everywhere in `allo.quantum.walk` and in any classical diffusion scorer. This is one
  line per scorer, costs nothing, and is the most direct attack on the between-protein variance the
  brief describes. It should be tested before anything else in this file.
- **Second-highest is local scaling of edge weights** in `allo.network.build` — a fourth orthogonal
  knob alongside the three that exist, and one that removes rather than adds a constant.
- **Selection is replaced by stability-filtered rank aggregation.** This slots into
  `allo.classical.postprocess` beside the existing S6/S7 stages and reuses the mean-midrank identity
  from `09a-power-verification.md`.
- **A C2 allow-list belongs in `tests/test_no_leakage.py`.** The file currently guards five file-read
  routes. Pretrained checkpoints are a sixth route, and an import trace cannot see a `from_pretrained`
  call any more than it can see a file read. An allow-list of admitted checkpoint identifiers, with a
  test that fails on anything else, is the same guard applied to the same class of gap.
- **Correction to a sibling file.** `02-ai-methods.md` §3 records PocketMiner as trained on "2,400 MD
  simulations across 35 proteins". The full text says **37 proteins**, 2 400 simulations of at least
  40 ns, 941 650 examples. The C2 verdict is unchanged; the number should be.
- **Two reporting obligations follow.** Every number from a pipeline containing S0 must carry (i) the
  substitution ablation against the constant-parameter pipeline, and (ii) the quantumness ablation
  against the classical readout, alongside the qubit/depth/connectivity account C3 already requires.
- **Nothing here has been measured.** Everything above is a design supported by literature. The first
  experiment is the paired τ-normalisation test on the `development` tier, through
  `allo.scoring.score_arm` and no other path.

---

## Method

**Databases and routes.** WebSearch (~80 queries across two passes) against Google/Bing-backed indices; WebFetch
against arXiv abstract pages, PubMed Central full text, bioRxiv, and doi.org resolution. Publisher
metadata pages consulted for Nature, Science, Cell Press, Oxford Academic, IOPscience, PNAS, APS,
Wiley, MIT Press, JAIR, PMLR, NeurIPS, AAAI and ACM DL. Model cards and licence text read from
Hugging Face and GitHub. Internal `Read` calls: `docs/method/README.md`,
`docs/method/review/00-conventions.md`, `docs/method/review/02-ai-methods.md`,
`docs/method/exploration/README.md`.

**Queries.** Listed in full in the scope statement above.

**Verification passes.** Two. The first established the DOI/arXiv ID for every entry. The second
re-checked the author lists, volumes and pages that the first pass had inferred rather than
retrieved; it corrected four entries (CrypticScout's authors, volume and pages; CrypToth's authors,
volume and pages; ESM-IF's author list and preprint DOI; CAID2's author list) and softened seven
others to a verified first author plus "et al." where the full list could not be retrieved. Any
reference carrying a bracketed note is one where a specific field is still unretrieved; the DOI or
arXiv ID in every entry was checked.

**Counts.** ~80 WebSearch queries, all returning usable results. 9 WebFetch calls: 6 returned usable
full or near-full text (PocketMiner PMC9977097; Guo et al. PMC9226352; arXiv:0711.0189;
arXiv:2306.05445; bioRxiv 2025.04.21.649858; bioRxiv 2022.04.10.487779), 1 returned a 301 redirect
that was followed successfully, 1 returned HTTP 403 (ScienceDirect, recovered via a search route
that supplied the DOI), 1 returned a 302 to a publisher linkinghub URL that confirmed DOI
resolution without content. 5 internal `Read` calls.

**Stopping rule.** Every model named in the six questions was located and characterised, or recorded
as not determined. Search stopped when three consecutive new queries (PredyFlexy training label;
DiG released-checkpoint provenance; a meta-model predicting binding-site-predictor performance from
protein descriptors) returned no new usable result — each logged above as a negative result rather
than omitted.

**Not reached this session.** (i) The numeric magnitude of the pLM-leakage inflation in
doi:10.1038/s42256-025-01176-7 — the abstract states the effect, not its size, and the full text was
not landed. (ii) The training-data source of the _released_ Distributional Graphormer protein
checkpoint. (iii) PredyFlexy's training label. (iv) Ankh's exact model-weight licence. (v) Whether
any of our benchmark targets appears in the ATLAS MD database — irrelevant while PEGASUS and
AlphaFlow-MD are rejected outright, but it would become the first question if that ever changed.
(vi) A Crossref DOI for Zelnik-Manor & Perona (2004) and for Cawley & Talbot (2010); neither was
issued one, and both are cited to their canonical proceedings/journal records instead.

---

## References

Vancouver style. Every entry carries a DOI, an arXiv ID, or — where none was issued — the canonical
proceedings record, explicitly marked.

1. Rice JR. The algorithm selection problem. Adv Comput. 1976;15:65–118. doi:10.1016/S0065-2458(08)60520-3
2. Kabsch W, Sander C. Dictionary of protein secondary structure: pattern recognition of hydrogen-bonded and geometrical features. Biopolymers. 1983;22(12):2577–637. doi:10.1002/bip.360221211
3. Wolpert DH. Stacked generalization. Neural Netw. 1992;5(2):241–59. doi:10.1016/S0893-6080(05)80023-1
4. Breiman L. Stacked regressions. Mach Learn. 1996;24(1):49–64. doi:10.1007/BF00117832
5. Moult J, Pedersen JT, Judson R, Fidelis K. A large-scale experiment to assess protein structure prediction methods. Proteins. 1995;23(3):ii–v. doi:10.1002/prot.340230303
6. Bahar I, Atilgan AR, Erman B. Direct evaluation of thermal fluctuations in proteins using a single-parameter harmonic potential. Fold Des. 1997;2(3):173–81. doi:10.1016/S1359-0278(97)00024-2
7. Plaxco KW, Simons KT, Baker D. Contact order, transition state placement and the refolding rates of single domain proteins. J Mol Biol. 1998;277(4):985–94. doi:10.1006/jmbi.1998.1645
8. Atilgan AR, Durell SR, Jernigan RL, Demirel MC, Keskin O, Bahar I. Anisotropy of fluctuation dynamics of proteins with an elastic network model. Biophys J. 2001;80(1):505–15. doi:10.1016/S0006-3495(01)76033-X
9. Atilgan AR, Akan P, Baysal C. Small-world communication of residues and significance for protein dynamics. Biophys J. 2004;86(1):85–91. doi:10.1016/S0006-3495(04)74086-2
10. Zelnik-Manor L, Perona P. Self-tuning spectral clustering. In: Advances in Neural Information Processing Systems 17 (NIPS 2004). Proceedings record 40173ea48d9567f1f393b20c855bb40b; ACM DL 10.5555/2976040.2976241. **No Crossref DOI issued.**
11. Caruana R, Niculescu-Mizil A, Crew G, Ksikes A. Ensemble selection from libraries of models. In: Proc 21st Int Conf Mach Learn (ICML '04). 2004:18. doi:10.1145/1015330.1015432
12. Varma S, Simon R. Bias in error estimation when using cross-validation for model selection. BMC Bioinformatics. 2006;7:91. doi:10.1186/1471-2105-7-91
13. von Luxburg U. A tutorial on spectral clustering. Stat Comput. 2007;17(4):395–416. arXiv:0711.0189
14. Xu L, Hutter F, Hoos HH, Leyton-Brown K. SATzilla: portfolio-based algorithm selection for SAT. J Artif Intell Res. 2008;32:565–606. doi:10.1613/jair.2490
15. Cawley GC, Talbot NLC. On over-fitting in model selection and subsequent selection bias in performance evaluation. J Mach Learn Res. 2010;11:2079–107. JMLR v11 record cawley10a; ACM DL 10.5555/1756006.1859921. **No Crossref DOI issued.**
16. Delvenne JC, Yaliraki SN, Barahona M. Stability of graph communities across time scales. Proc Natl Acad Sci USA. 2010;107(29):12755–60. doi:10.1073/pnas.0903215107
17. Meinshausen N, Bühlmann P. Stability selection. J R Stat Soc Series B. 2010;72(4):417–73. doi:10.1111/j.1467-9868.2010.00740.x
18. Bakan A, Meireles LM, Bahar I. ProDy: protein dynamics inferred from theory and experiments. Bioinformatics. 2011;27(11):1575–7. doi:10.1093/bioinformatics/btr168
19. Delmotte A, Tate EW, Yaliraki SN, Barahona M. Protein multi-scale organization through graph partitioning and robustness analysis: application to the myosin–myosin light chain interaction. Phys Biol. 2011;8(5):055010. doi:10.1088/1478-3975/8/5/055010; arXiv:1109.4232
20. de Brevern AG, Bornot A, Craveur P, Etchebest C, Gelly JC. PredyFlexy: flexibility and local structure prediction from sequence. Nucleic Acids Res. 2012;40(W1):W317–22. doi:10.1093/nar/gks482
21. Park Y, Marcotte EM. Flaws in evaluation schemes for pair-input computational predictions. Nat Methods. 2012;9(12):1134–6. doi:10.1038/nmeth.2259
22. Tan KP, Nguyen TB, Patel S, Varadarajan R, Madhusudhan MS. Depth: a web server to compute depth, cavity sizes, detect potential small-molecule ligand-binding cavities and predict the pKa of ionizable residues in proteins. Nucleic Acids Res. 2013;41(W1):W314–21. doi:10.1093/nar/gkt503
23. Cilia E, Pancsa R, Tompa P, Lenaerts T, Vranken WF. From protein sequence to dynamics and disorder with DynaMine. Nat Commun. 2013;4:2741. doi:10.1038/ncomms3741
24. Aaronson S. Read the fine print. Nat Phys. 2015;11(4):291–3. doi:10.1038/nphys3272
25. Feurer M, Klein A, Eggensperger K, Springenberg J, Blum M, Hutter F. Efficient and robust automated machine learning. In: Advances in Neural Information Processing Systems 28 (NeurIPS 2015). NeurIPS proceedings 11d0e6287202fced83f79975ec59a3a6; ACM DL 10.5555/2969442.2969547.
26. Ponzoni L, Polles G, Carnevale V, Micheletti C. SPECTRUS: a dimensionality reduction approach for identifying dynamical domains in protein complexes from limited structural datasets. Structure. 2015;23(8):1516–25. doi:10.1016/j.str.2015.05.022
27. Cimermancic P, Weinkam P, Rettenmaier TJ, et al. CryptoSite: expanding the druggable proteome by characterization and prediction of cryptic binding sites. J Mol Biol. 2016;428(4):709–19. doi:10.1016/j.jmb.2016.01.029
28. Bravyi S, Gambetta JM, Mezzacapo A, Temme K. Tapering off qubits to simulate fermionic Hamiltonians. arXiv:1701.08213
29. Beglov D, Hall DR, Wakefield AE, et al. Exploring the structural origins of cryptic sites on proteins. Proc Natl Acad Sci USA. 2018;115(15):E3416–25. doi:10.1073/pnas.1711490115
30. Haas J, et al. Continuous Automated Model EvaluatiOn (CAMEO) complementing the critical assessment of structure prediction in CASP12. Proteins. 2018;86(Suppl 1):387–98. doi:10.1002/prot.25431
31. Varoquaux G. Cross-validation failure: small sample sizes lead to large error bars. NeuroImage. 2018;180(Pt A):68–77. doi:10.1016/j.neuroimage.2017.06.061; arXiv:1706.07581
32. Kerschke P, Hoos HH, Neumann F, Trautmann H. Automated algorithm selection: survey and perspectives. Evol Comput. 2019;27(1):3–45. doi:10.1162/evco_a_00242
33. Chen L, Cruz A, Ramsey S, et al. Hidden bias in the DUD-E dataset leads to misleading performance of deep learning in structure-based virtual screening. PLoS One. 2019;14(8):e0220113. doi:10.1371/journal.pone.0220113
34. Verdon G, et al. Learning to learn with quantum neural networks via classical neural networks. arXiv:1907.05415
35. Khairy S, Shaydulin R, Cincio L, Alexeev Y, Balaprakash P. Learning to optimize variational quantum circuits to solve combinatorial problems. Proc AAAI Conf Artif Intell. 2020;34(3):2367–75. doi:10.1609/aaai.v34i03.5616; arXiv:1911.11071
36. Martínez-Rosell G, Lovera S, Sands ZA, De Fabritiis G. PlayMolecule CrypticScout: predicting protein cryptic sites using mixed-solvent molecular simulations. J Chem Inf Model. 2020;60(4):2314–24. doi:10.1021/acs.jcim.9b01209
37. Huang HY, Kueng R, Preskill J. Predicting many properties of a quantum system from very few measurements. Nat Phys. 2020;16(10):1050–7. doi:10.1038/s41567-020-0932-7
38. Kaynak BT, Bahar I, Doruker P. Essential site scanning analysis: a new approach for detecting sites that modulate the dispersion of protein global motions. Comput Struct Biotechnol J. 2020;18:1577–86. doi:10.1016/j.csbj.2020.06.020
39. Moussa C, Calandra H, Dunjko V. To quantum or not to quantum: towards algorithm selection in near-term quantum optimization. Quantum Sci Technol. 2020;5(4):044009. doi:10.1088/2058-9565/abb8e5; arXiv:2001.08271
40. Vig J, Madani A, Varshney LR, Xiong C, Socher R, Rajani NF. BERTology meets biology: interpreting attention in protein language models. In: Int Conf Learn Represent (ICLR 2021). arXiv:2006.15222
41. Rao R, Meier J, Sercu T, Ovchinnikov S, Rives A. Transformer protein language models are unsupervised structure learners. In: Int Conf Learn Represent (ICLR 2021). bioRxiv 2020.12.15.422761. doi:10.1101/2020.12.15.422761
42. Jumper J, Evans R, Pritzel A, et al. Highly accurate protein structure prediction with AlphaFold. Nature. 2021;596(7873):583–9. doi:10.1038/s41586-021-03819-2
43. Robert A, Barkoutsos PK, Woerner S, Tavernelli I. Resource-efficient quantum algorithm for protein folding. npj Quantum Inf. 2021;7:38. doi:10.1038/s41534-021-00368-4
44. Hu G, Katuwawala A, Wang K, et al. flDPnn: accurate intrinsic disorder prediction with putative propensities of disorder functions. Nat Commun. 2021;12:4438. doi:10.1038/s41467-021-24773-7
45. Erdős G, Pajkos M, Dosztányi Z. IUPred3: prediction of protein disorder enhanced with unambiguous experimental annotation and visualization of evolutionary conservation. Nucleic Acids Res. 2021;49(W1):W297–303. doi:10.1093/nar/gkab408
46. Vander Meersche Y, Cretin G, de Brevern AG, Gelly JC, Galochkina T. MEDUSA: prediction of protein flexibility from sequence. J Mol Biol. 2021;433(11):166882. doi:10.1016/j.jmb.2021.166882
47. Walsh I, Fishman D, Garcia-Gasulla D, et al. DOME: recommendations for supervised machine learning validation in biology. Nat Methods. 2021;18(10):1122–7. doi:10.1038/s41592-021-01205-4; arXiv:2006.16189
48. Elnaggar A, Heinzinger M, et al. ProtTrans: toward understanding the language of life through self-supervised learning. IEEE Trans Pattern Anal Mach Intell. 2022;44(10):7112–27. doi:10.1109/TPAMI.2021.3095381; arXiv:2007.06225
49. del Alamo D, Sala D, Mchaourab HS, Meiler J. Sampling alternative conformational states of transporters and receptors with AlphaFold2. eLife. 2022;11:e75751. doi:10.7554/eLife.75751
50. Hsu C, Verkuil R, Liu J, Lin Z, Hie B, Sercu T, Lerer A, Rives A. Learning inverse folding from millions of predicted structures. In: Proc 39th Int Conf Mach Learn (ICML 2022). PMLR 162:8946–70. Preprint: bioRxiv 2022.04.10.487779. doi:10.1101/2022.04.10.487779
51. Dauparas J, Anishchenko I, Bennett N, et al. Robust deep learning-based protein sequence design using ProteinMPNN. Science. 2022;378(6615):49–56. doi:10.1126/science.add2187
52. Piovesan D, Monzon AM, Tosatto SCE. Intrinsic protein disorder and conditional folding in AlphaFoldDB. Protein Sci. 2022;31(11):e4466. doi:10.1002/pro.4466
53. Guo HB, Perminov A, Bekele S, et al. AlphaFold2 models indicate that protein sequence determines both structure and dynamics. Sci Rep. 2022;12:10696. doi:10.1038/s41598-022-14382-9
54. Cretin G, Galochkina T, et al. SWORD2: hierarchical analysis of protein 3D structures. Nucleic Acids Res. 2022;50(W1):W732–8. doi:10.1093/nar/gkac370
55. Shaydulin R, Wild SM. Importance of kernel bandwidth in quantum machine learning. Phys Rev A. 2022;106(4):042407. doi:10.1103/PhysRevA.106.042407; arXiv:2111.05451
56. Schuld M, Killoran N. Is quantum advantage the right goal for quantum machine learning? PRX Quantum. 2022;3(3):030101. doi:10.1103/PRXQuantum.3.030101; arXiv:2203.01340
57. Zhang Z, et al. Protein representation learning by geometric structure pretraining. In: Int Conf Learn Represent (ICLR 2023). arXiv:2203.06125
58. Elnaggar A, et al. Ankh: optimized protein language model unlocks general-purpose modelling. arXiv:2301.06568
59. Meller A, Ward M, Borowsky J, et al. Predicting locations of cryptic pockets from single protein structures using the PocketMiner graph neural network. Nat Commun. 2023;14:1177. doi:10.1038/s41467-023-36699-3
60. Lin Z, Akin H, Rao R, et al. Evolutionary-scale prediction of atomic-level protein structure with a language model. Science. 2023;379(6637):1123–30. doi:10.1126/science.ade2574
61. Del Conte A, et al. Critical assessment of protein intrinsic disorder prediction (CAID) — results of round 2. Proteins. 2023;91(12):1925–34. doi:10.1002/prot.26582 [full author list not retrieved; first author and volume/pages verified]
62. Zhao B, Ghadermarzi S, Kurgan L. Comparative evaluation of AlphaFold2 and disorder predictors for prediction of intrinsic disorder, disorder content and fully disordered proteins. Comput Struct Biotechnol J. 2023;21:3248–58. doi:10.1016/j.csbj.2023.06.001
63. Lau AM, Kandathil SM, Jones DT. Merizo: a rapid and accurate protein domain segmentation method using invariant point attention. Nat Commun. 2023;14:8445. doi:10.1038/s41467-023-43934-4
64. Kumar A, Kaynak BT, Dorman KS, Doruker P, Jernigan RL. Predicting allosteric pockets in protein biological assemblages. Bioinformatics. 2023;39(5):btad275. doi:10.1093/bioinformatics/btad275
65. Kapoor S, Narayanan A. Leakage and the reproducibility crisis in machine-learning-based science. Patterns. 2023;4(9):100804. doi:10.1016/j.patter.2023.100804
66. Teufel F, Gíslason MH, Almagro Armenteros JJ, Johansen AR, Winther O, Nielsen H. GraphPart: homology partitioning for biological sequence analysis. NAR Genom Bioinform. 2023;5(4):lqad088. doi:10.1093/nargab/lqad088
67. Mücke S, Heese R, Müller S, Wolter M, Piatkowski N. Feature selection on quantum computers. Quantum Mach Intell. 2023;5:11. doi:10.1007/s42484-023-00099-z; arXiv:2203.13261
68. Schreiber FJ, Eisert J, Meyer JJ. Classical surrogates for quantum learning models. Phys Rev Lett. 2023;131(10):100803. doi:10.1103/PhysRevLett.131.100803; arXiv:2206.11740
69. van Kempen M, Kim SS, Tumescheit C, et al. Fast and accurate protein structure search with Foldseek. Nat Biotechnol. 2024;42(2):243–6. doi:10.1038/s41587-023-01773-0
70. Su J, et al. SaProt: protein language modeling with structure-aware vocabulary. In: Int Conf Learn Represent (ICLR 2024). bioRxiv 2023.10.01.560349. doi:10.1101/2023.10.01.560349
71. Heinzinger M, Weissenow K, Gomez Sanchez J, et al. Bilingual language model for protein sequence and structure. NAR Genom Bioinform. 2024;6(4):lqae150. doi:10.1093/nargab/lqae150
72. Jing B, Berger B, Jaakkola T. AlphaFold meets flow matching for generating protein ensembles. In: Proc 41st Int Conf Mach Learn (ICML 2024). PMLR 235. arXiv:2402.04845
73. Zheng S, et al. Predicting equilibrium distributions for molecular systems with deep learning. Nat Mach Intell. 2024;6:558–67. doi:10.1038/s42256-024-00837-3; arXiv:2306.05445
74. Wayment-Steele HK, Ojoawo A, et al. Predicting multiple conformations via sequence clustering and AlphaFold2. Nature. 2024;625(7996):832–9. doi:10.1038/s41586-023-06832-9
75. Schafer JW, Lee M, Chakravarty D, Chen EA, Porter LL. Sequence clustering confounds AlphaFold2. Nature. 2025;638(8049):E8–E12. doi:10.1038/s41586-024-08267-2
76. Abramson J, Adler J, Dunger J, et al. Accurate structure prediction of biomolecular interactions with AlphaFold 3. Nature. 2024;630(8016):493–500. doi:10.1038/s41586-024-07487-w
77. Wells J, Hawkins-Hooker A, et al. Chainsaw: protein domain segmentation with fully convolutional neural networks. Bioinformatics. 2024;40(5):btae296. doi:10.1093/bioinformatics/btae296
78. Rivolli A, Garcia LPF, Soares C, Vanschoren J, de Carvalho ACPLF. Meta-features for meta-learning. Knowl Based Syst. 2022;240:108101. doi:10.1016/j.knosys.2021.108101
79. Bowles J, Ahmed S, Schuld M. Better than classical? The subtle art of benchmarking quantum machine learning models. arXiv:2403.07059
80. Škrhák V, Novotný M, Feidakis CP, Krivák R, Hoksza D. CryptoBench: cryptic protein–ligand binding sites dataset and benchmark. Bioinformatics. 2025;41(1):btae745. doi:10.1093/bioinformatics/btae745
81. Hayes T, Rao R, Akin H, et al. Simulating 500 million years of evolution with a language model. Science. 2025. doi:10.1126/science.ads0018; preprint bioRxiv 2024.07.01.600583 [volume/pages not retrieved]
82. Lewis S, Hempel T, Jiménez-Luna J, et al. Scalable emulation of protein equilibrium ensembles with generative deep learning. Science. 2025. doi:10.1126/science.adv9817; preprint bioRxiv 2024.12.05.626885. Research briefing: BioEmu is a biomolecular emulator for sampling protein structure ensembles. Nat Methods. 2025. doi:10.1038/s41592-025-02874-1
83. Vander Meersche Y, et al. PEGASUS: prediction of MD-derived protein flexibility from sequence. Protein Sci. 2025;34(8):e70221. doi:10.1002/pro.70221 [full author list not retrieved]
84. Suzuki, et al. Light-cone feature selection for quantum machine learning. Adv Quantum Technol. 2025. doi:10.1002/qute.202400647; arXiv:2403.18733 [first author surname only; initials and full list not retrieved]
85. Szymborski J, Emad A. A flaw in using pretrained protein language models in protein–protein interaction inference models. Nat Mach Intell. 2026;8:197–208. doi:10.1038/s42256-025-01176-7; bioRxiv 2025.04.21.649858. doi:10.1101/2025.04.21.649858
86. Maity S, Qiao B. AlloBench: a data set pipeline for the development and benchmarking of allosteric site prediction tools. ACS Omega. 2025;10(17):17973–85. doi:10.1021/acsomega.5c01263
87. Koseki J, Motono C, Yanagisawa K, Kudo G, Yoshino R, Hirokawa T, Imai K. CrypToth: cryptic pocket detection through mixed-solvent molecular dynamics simulations-based topological data analysis. J Chem Inf Model. 2025;65:5567–75. doi:10.1021/acs.jcim.4c02111
