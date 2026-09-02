# Pure AI and machine-learning methods

**Scope:** Every allosteric-site predictor, protein representation model, or generative
model with fitted or learned parameters — the comparison class a hybrid quantum+AI method
must beat. For each: what input it needs, whether it clears C1 (holo leakage) and C2 (MD
in training or inference), how much labelled data it took, and what its published number
actually measures. Deliberately excludes physics-only baselines with no fitted parameters
(ENM/GNM, bond-to-bond propensity, perturbation-response scanning, our own `ALPS`/`APOP`)
and quantum or hybrid-quantum architectures.
**Sibling files:** 00 (conventions, evidence rules, the eleven closed quantum insertion
points). The classical physics-only baselines and the quantum/hybrid-quantum methods are
covered elsewhere in this nine-file series; this file is bounded strictly to methods with
learned weights.
**Retrieved:** 2026-08-25.

---

## 1. Relation to `allosteric-benchmark/docs/ai-model-landscape.md`

That survey (2,536 papers, 27 verified cards) asked which AI model families can do
allosteric-site prediction and which run on one specific minimal input signature (Cβ
coordinates + active-site indices only — no sequence). This file asks the broader question
the challenge itself poses: which AI families exist for this task at all, and which survive
C1 and C2 on **any** apo-legal input, sequence included. Three relations to name explicitly.

**Confirmed, unchanged.** The PLM collapse on allosteric sites (AUPR 0.06 at AUROC 0.70),
the PASSer2.0 baseline-vs-AutoML tension (84.3% untrained vs 82.7% trained on top-3), the
class-imbalance trap, ESM-1b's zero-shot edge over Ohm/EVcouplings, and the field's small
training sets (90–235 proteins) all reproduce independently in this search and are used
below without re-deriving them.

**Extended.** Six things that survey did not have: (i) exact identification and citation
of the PLM-collapse source [§12]; (ii) nine additional named predictors from 2024–2026
(DeepAllo, MEF-AlloSite, Allo-PED, ZHMolEReP, Allo-Allo, AlloFusion, STINGAllo, AlloEF, and
the ALLO systematic-evaluation paper that supplies this repository's own curated labels);
(iii) a strict, method-by-method C1/C2 legality pass [§10]; (iv) an explicit count of the
field's total labelled-data ceiling [§2]; (v) a literature-confirmed second instance of the
ranking-vs-localisation split this repo already measured internally, in PASSer2.0's own
numbers [§11]; (vi) two double-checked C2 traps — BioEmu and MD-finetuned AlphaFlow — that
look ab-initio at inference but are not, because their weights were fit in part on MD [§7].

**Corrected in scope, not in fact.** The survey's family table concludes "on our input,
essentially one untried family: a residue-graph GNN … everything else needs an input we do
not have" (ai-model-landscape.md §6). That is correct for the specific Cβ-only input signature that sub-repo
chose, but it is not a C1/C2 finding — nothing in the six hard constraints bans using a
protein's own apo **sequence**. Sequence is not holo information and it is not MD. A
protein-language-model route is therefore not illegal; it is merely outside one
experiment's self-imposed input contract. If the prediction path admits sequence, the
entire PLM family in §4 opens up, and §9's zero-shot route becomes the cleanest C1/C2
survivor of anything reviewed here. This is a scope clarification, not a contradiction of
any number in the survey — worth stating loudly because it changes what "legal" means for
this file relative to that one. [UNVERIFIED — a reading of C1–C2 against the survey's own
table, not a new retrieval]

---

## 2. The supervision ceiling — how much labelled allosteric data actually exists

Four independent counts, all retrieved this session, converge on the same order of
magnitude.

| source                    | unique proteins / sites                                                                                                                                                                  | note                                                                                                                                                                                                                                                                     |
| ------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| ASD (2010→2023 releases)  | **1,949 allosteric protein entries**; **~3,000 allosteric sites** against ~14,000 general binding sites in the same release                                                              | [VERIFIED-FULLTEXT] Xiao, Verkhivker & Tao, _Trends Biochem Sci_ 2023, doi:10.1016/j.tibs.2022.11.001 (PMC10023316); site count corroborated independently by the 2025 pLM study's own ASD pull, "~3,000 allosteric sites" [VERIFIED-FULLTEXT] bioRxiv 2025.06.27.662060 |
| ASBench                   | **235** unique allosteric sites (Core set), **147** structurally non-redundant (Core-Diversity set)                                                                                      | [VERIFIED-ABSTRACT] Huang et al. 2015, _Bioinformatics_, doi:10.1093/bioinformatics/btv169                                                                                                                                                                               |
| CASBench                  | **91** enzymes with both catalytic and allosteric sites annotated                                                                                                                        | [VERIFIED-ABSTRACT] Zlobin et al. 2019, _Acta Naturae_, doi:10.32607/20758251-2019-11-1-74-80                                                                                                                                                                            |
| AlloBench (2025 pipeline) | **2,141** allosteric sites, **2,034** structures, **418** unique chains; a systematic re-benchmark of seven tools on a 100-protein subset found accuracy for every tool "well below 60%" | [VERIFIED-ABSTRACT] Maity & Qiao 2025, _ACS Omega_, doi:10.1021/acsomega.5c01263                                                                                                                                                                                         |
| ALLO (`allo_tableS2.csv`) | the curated table behind this repo's own 97-target set, plus 87 orthosteric-only negatives                                                                                               | [VERIFIED-FULLTEXT] read directly, `allosteric-benchmark/README.md` §1.3, §11; source paper Ai et al. 2026, _J Comput-Aided Mol Des_, doi:10.1007/s10822-026-00831-4, cited in the same repo's References                                                                |

Two numbers matter more than the protein counts: **prevalence** and **evaluable positives**
once a proximity mask is applied, because those are what bound model capacity, not the
protein count alone. This repo's own AlloBench integration measured it directly: 1,042
samples over 265 UniProt accessions survive its own filters, carrying **9,738 evaluable
positive residues** out of 369,988 candidate residues — a **2.6% pool-wide prevalence**
[VERIFIED-FULLTEXT] `allosteric-benchmark/README.md` §1.6. The curated 96-target set carries
**1,050** evaluable positives out of 78,509 (1.3%) [VERIFIED-FULLTEXT] `gnn/RESULTS.md`. The
44-target hybrid subset carries 386 positives out of 16,063 pooled residues (2.4%)
[VERIFIED-FULLTEXT] `hybrid/RESULTS.md`. Independently, the kinase-frustration PLM study
reports allosteric residues at **under 3%** of the kinase domain on its own 453-kinase
corpus [VERIFIED-FULLTEXT] bioRxiv 10.64898/2026.01.05.697819.

**What that capacity supports.** Generalisation error for a fitted model scales as
√(trainable-parameters / effective-N); with ~90–265 unique proteins and a few hundred to
low-thousands of positive residues at 1.3–6% prevalence, this repo's own GNN work stream
put the practical ceiling at "tens of trainable gates, not thousands" for a quantum model,
and independently chose ~15k parameters for a classical GNN as "already generous for ~90
proteins" [VERIFIED-FULLTEXT] `gnn/README.md`, `hybrid/README.md`. That is two orders of
magnitude below DeepSite's regime — >7,000 general-pocket proteins support a voxel CNN with
millions of parameters, but that architecture cannot be legitimately fit on allosteric
labels alone [VERIFIED-ABSTRACT — teammate's card P10-c3, confirmed by this session's search
on the same paper]. The consequence is architectural, not just statistical: **the field's
own capacity ceiling rules out training a large network end-to-end on allosteric labels**
and rules in exactly two patterns — (i) a small model (≤ ~15k parameters: logistic
regression, SVM, shallow GNN, gradient-boosted ensemble) fit directly on the 90–265-protein
corpus, or (ii) a small head fit on top of a large representation pretrained on an
unrelated, richly-supervised task (contacts, structure, general binding, B-factors) with no
allosteric label anywhere in the large model's own training. §6 and §9 both instantiate the
second pattern; §10's survivor table is built on this distinction.

**→ Pipeline implication.** Any learned component in the prediction path should sit at or
below the ~15k-parameter band unless it is a frozen-representation-plus-light-head design.
This bounds §5–§6's architecture choice before a single circuit or network is written.

---

## 3. Named allosteric-site predictors with learning — the master table

Columns as specified. "C1 verdict" and "C2 verdict" are about the **method itself** — its
published training procedure and its inference-time input. A second, separate risk applies
to every ASD/ASBench/CASBench-trained tool in this table and is **not** repeated in every
row: ASD is comprehensive enough that it very likely already contains entries for KRAS,
BCR-ABL1, and cardiac myosin — all three are landmark, heavily published allosteric
targets, and Sotorasib's Switch-II pocket alone has been described in the literature since
2013 (`CHALLENGE.md` ref. 18). Using a pretrained ASD-derived classifier on our own
benchmark targets **without confirming those targets are excluded from its training split**
would leak the answer through the weights, the same failure mode AlloBench's own
UniRef50-declustering exercise was built to catch (conventions §6; AlloBench above). This
is marked "Legal\*" in the table and explained once here rather than four times below.
[UNVERIFIED — a reasoned risk from ASD's known comprehensiveness, not a per-target lookup;
checking it would require opening `docs/benchmark/*/manifest.yaml`, which this file may not
do]

| Method                                         | Input required                                                                                                                                         | C1                                                                                                | C2                                                                                                                               | Training data                                                                                                                                                               | Published number                                                                                                                                                                      | Dataset                                               | Criterion                                                                                                                                                                                                           |
| ---------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| AlloPred (Greener & Sternberg 2015)            | Cα coords, single structure; SVM on 7 NMA+Fpocket features                                                                                             | Legal\*                                                                                           | **Legal** — NMA on one static structure, no MD                                                                                   | 79 train / 40 test (119 total)                                                                                                                                              | 23/40 top-ranked, 28/40 top-1-or-2                                                                                                                                                    | ASBench Core-Diversity                                | pocket rank vs. annotated allosteric pocket [VERIFIED-FULLTEXT, doi:10.1186/s12859-015-0771-1]                                                                                                                      |
| AllositePro (Song et al. 2017)                 | single structure, pocket features + perturbation                                                                                                       | Legal\*                                                                                           | Legal — perturbation, not MD                                                                                                     | not retrieved                                                                                                                                                               | superior to AlloSite/AlloPred (qualitative); novel CDK2 site confirmed by mutagenesis                                                                                                 | ASD-derived                                           | pocket rank / experimental validation [VERIFIED-ABSTRACT, doi:10.1021/acs.jcim.7b00014]                                                                                                                             |
| PASSer (Tian et al. 2023a)                     | Fpocket geometric descriptors                                                                                                                          | Legal\*                                                                                           | Legal                                                                                                                            | 204-protein test set                                                                                                                                                        | untrained FPocket-rank baseline: **accuracy 0.968**; top-3 70.6–84.3% depending on denominator                                                                                        | ASD-derived                                           | accuracy/precision/recall/F1; top-3 rank [VERIFIED-ABSTRACT, doi:10.1093/nar/gkad303; numbers cross-checked against teammate's card P48]                                                                            |
| PASSer2.0 (Xiao, Tian & Tao 2022)              | pocket descriptors, AutoML                                                                                                                             | Legal\*                                                                                           | Legal                                                                                                                            | 90 proteins train                                                                                                                                                           | precision 0.850, recall 0.616, F1 0.701; **82.7% top-3**                                                                                                                              | 204-protein test set                                  | precision/recall/F1; top-3 rank [VERIFIED-ABSTRACT, doi:10.3389/fmolb.2022.879251]                                                                                                                                  |
| PASSerRank (Tian et al. 2023b)                 | pocket descriptors, learning-to-rank                                                                                                                   | Legal\*                                                                                           | Legal                                                                                                                            | trained/validated on ASD and CASBench                                                                                                                                       | F1 0.662 (ASD) / 0.608 (CASBench); **top-3 83.6% / 80.5%**                                                                                                                            | ASD, CASBench                                         | F1; top-3 rank [VERIFIED-ABSTRACT, doi:10.1002/jcc.27193, arXiv:2302.01117]                                                                                                                                         |
| DeepAllo (2024/2025)                           | sequence only, fine-tuned ProtBERT-BFD, multitask (allostery + secondary structure)                                                                    | Legal\*, sequence-only                                                                            | Legal                                                                                                                            | ASD fine-tuning split (exact n not retrieved)                                                                                                                               | F1 **89.66%**; top-3 **90.5%**                                                                                                                                                        | ASD                                                   | F1; top-3 pocket rank [VERIFIED-ABSTRACT, doi:10.1093/bioinformatics/btaf294; PMC12145174]                                                                                                                          |
| MEF-AlloSite (2024)                            | 9,460 structure+sequence pocket features, multimodel ensemble selection                                                                                | Legal\*                                                                                           | Legal                                                                                                                            | **90 proteins**, 51 resplits                                                                                                                                                | beats PASSer2.0/PASSerRank, paired t-test p < 0.05, Cohen's D > 0.8                                                                                                                   | 3 held-out test cases                                 | precision/AUC distribution, paired significance [VERIFIED-ABSTRACT, doi:10.1186/s13321-024-00882-5]                                                                                                                 |
| Allo-PED / AlloPED (2025)                      | AlloPED-pocket: physicochemical pocket features (ensemble); AlloPED-site: ProtT5 embeddings + dilated CNN + attention                                  | Legal\*                                                                                           | Legal                                                                                                                            | not fully retrieved                                                                                                                                                         | pocket-level **MCC 0.544, AUC 0.920**; residue-level **precision 0.601, recall 0.422**                                                                                                | benchmark not fully specified in retrieved text       | MCC/AUC (pocket) vs. precision/recall (residue) — **the gap between these two rows is itself the ranking-vs-localisation split, §11** [VERIFIED-ABSTRACT, bioRxiv 2025.03.28.645953; confirms teammate's card P536] |
| ZHMolEReP (2026)                               | single structure; GNM + mutual-information-corrected Kirchhoff matrix                                                                                  | Legal\*                                                                                           | Legal — info-theoretic correction from an MSA, not MD                                                                            | fit against ASBench; **whether it has any gradient-fitted weight, vs. being a closed-form correction, could not be confirmed — full text was paywalled (403) this session** | recall 0.7037, AUC 0.7858, **33/40** proteins hit                                                                                                                                     | ASBench (40 proteins)                                 | recall; AUC; protein hit-count [VERIFIED-ABSTRACT only — see caveat above, doi:10.1021/acs.jcim.6c00141]                                                                                                            |
| Allo-Allo (Dong et al. 2024)                   | single apo sequence; **ESM-2 attention heads only, no fine-tuning of the backbone**                                                                    | Legal, sequence-only, cleanest overlap risk (§9)                                                  | Legal                                                                                                                            | data-efficient by design; exact n not retrieved this session                                                                                                                | **67% higher AUPRC** than the SOTA PLM baselines it compares against                                                                                                                  | not fully specified in the retrieved abstract         | AUPRC [VERIFIED-ABSTRACT, doi:10.1101/2024.09.28.615583]                                                                                                                                                            |
| AlloFusion (Huang et al. 2025)                 | sequence: pLM embedding + PSSM (evolutionary) + biochemical descriptors                                                                                | Legal\*, sequence-only                                                                            | Legal                                                                                                                            | not retrieved                                                                                                                                                               | not retrieved this session                                                                                                                                                            | not retrieved                                         | not retrieved [VERIFIED-ABSTRACT (existence and architecture only), doi:10.1021/acs.jcim.5c01033]                                                                                                                   |
| STINGAllo (Omage et al. 2025)                  | single structure; 54 "nanoenvironment" descriptors (hydrophobic network, local density, graph connectivity, "sponge effect")                           | Legal\*                                                                                           | Legal                                                                                                                            | residue-centric ML, n not retrieved                                                                                                                                         | **~78%** success on sites outside surface pockets vs. **21.1–24.2%** for pocket-based predictors; ~60.2% overall vs ~21–24% baselines                                                 | in-house benchmark                                    | success rate [VERIFIED-ABSTRACT, doi:10.1093/bib/bbaf424]                                                                                                                                                           |
| AlloEF (Zhang et al. 2026)                     | sequence + structure + network-topology features; soft-voting ensemble (LightGBM + Random Forest + XGBoost) + transfer entropy + energetic frustration | Legal\*                                                                                           | Legal                                                                                                                            | not retrieved                                                                                                                                                               | **F1 0.630, MCC 0.609**                                                                                                                                                               | independent test set, not fully specified             | F1; MCC [VERIFIED-ABSTRACT, doi:10.1021/acs.jpcb.6c00242]                                                                                                                                                           |
| Our repo — residue-graph GNN (`gnn/`)          | **Cβ coords + active-site indices only** — no sequence, no MD, no holo                                                                                 | Legal\* (external training corpus; not our own 4+9 frozen targets)                                | Legal                                                                                                                            | 96 curated targets (protein-grouped 5-fold CV), 1,050 evaluable positives, **14,161 parameters**                                                                            | stratified AUC **0.622 / 0.630** (seed 0/1); ties `ALPS` (0.592), paired p = 0.14/0.15                                                                                                | 97-target curated set (ASBench/ASD via ALLO Table S2) | distance-stratified AUC vs. paired classical baseline [VERIFIED-FULLTEXT, `gnn/README.md`, `gnn/RESULTS.md`]                                                                                                        |
| Our repo — hybrid learned combiner (`hybrid/`) | same 7–8 hand-engineered structural features as `ALPS`                                                                                                 | Legal\*                                                                                           | Legal                                                                                                                            | 44 curated targets, 16,063 pooled residues, 386 positives                                                                                                                   | proxy/plain-AUC protocol: **0.606 → 0.668** AUC, **27.1% → 18.6%** top-5 hit rate; curated/stratified re-run (Gate 0): 0.576 (`ALPS`) → 0.603 (logistic regression), +0.027, p = 0.72 | curated 44-target subset, two protocols               | stratified AUC + top-5 hit rate [VERIFIED-FULLTEXT, `hybrid/README.md`, `hybrid/RESULTS.md`]                                                                                                                        |
| CryptoSite (Cimermancic et al. 2016)           | single structure at deployment, but **new MD run required at inference**                                                                               | **Illegal** — MD required even at deployment time, not just training                              | **Illegal** — 28 of 58 training features are AllosMod MD outputs; MD-free ablation exists (30 features) at AUC 0.74 vs 0.83 full | 84 cryptic sites / 92 pockets / 705 surface patches                                                                                                                         | AUC 0.83 (full), TPR 79%/FPR 29%; **MD-free variant AUC 0.74**                                                                                                                        | own 14-protein apo test set                           | AUC; TPR/FPR [VERIFIED-FULLTEXT, doi:10.1016/j.jmb.2016.01.029, PMC4794384; MD-free number cross-checked in `experiments/REGISTRY.md` line 76–77]                                                                   |
| PocketMiner (Meller et al. 2023)               | single structure at inference; **MD-derived labels at training**                                                                                       | Legal input at inference                                                                          | **Illegal** — weights trained to predict an MD-simulated event; conventions §4 already names this                                | 2,400 MD simulations across 35 proteins                                                                                                                                     | ROC-AUC **0.87**                                                                                                                                                                      | 39 experimentally-confirmed cryptic pockets           | ROC-AUC [VERIFIED-ABSTRACT, doi:10.1038/s41467-023-36699-3]                                                                                                                                                         |
| AF2BIND (2023/2026)                            | sequence + AF2 pair representation (frozen); no true ligand needed                                                                                     | Legal\* — corpus is general small-molecule PDB, not ASD, so overlap risk is lower but not zero    | Legal                                                                                                                            | 1,902 proteins / 2,110 ligands, logistic-regression head only                                                                                                               | **66%** binding-residue recovery (AF2-pair alone); **69%** combined with ESM2 + ESM1-IF                                                                                               | held-out curated PDB set                              | binding-residue recovery [VERIFIED-FULLTEXT, bioRxiv 2023.10.15.562410]                                                                                                                                             |
| DeepSite (2017)                                | all-atom voxel grid                                                                                                                                    | Legal but **allostery-agnostic** — detects any druggable pocket, not specifically allosteric ones | Legal                                                                                                                            | >7,000 general-pocket proteins                                                                                                                                              | not allostery-specific; general pocket "ligandability" score                                                                                                                          | scPDB-derived                                         | ligandability [VERIFIED-ABSTRACT, doi:10.1093/bioinformatics/btx285]                                                                                                                                                |
| VN-EGNN (2024)                                 | Cα graph + virtual nodes, E(3)/SE(3)-equivariant message passing                                                                                       | Legal but allostery-agnostic                                                                      | Legal                                                                                                                            | COACH420 / HOLO4K / PDBbind2020                                                                                                                                             | state-of-the-art DCC/DCA success rate (exact % not retrieved this session)                                                                                                            | COACH420, HOLO4K, PDBbind2020                         | DCC/DCA success rate [VERIFIED-ABSTRACT, doi:10.1186/s13321-025-01127-9]                                                                                                                                            |
| MaSIF / dMaSIF / ScanNet                       | molecular surface mesh or raw atoms; geometric deep learning                                                                                           | Legal but allostery-agnostic (protein–protein interfaces / general pockets)                       | Legal                                                                                                                            | general PPI/pocket corpora                                                                                                                                                  | ScanNet: DockQ ≥ 0.23 in **67%** of heteromeric interfaces, DockQ ≥ 0.8 in 23%                                                                                                        | PPI benchmark sets                                    | DockQ success rate [VERIFIED-ABSTRACT, doi:10.1038/s41592-022-01490-7 (ScanNet); doi:10.1038/s41592-019-0666-6 (MaSIF)]                                                                                             |
| BioEmu (2025)                                  | sequence (outputs a structure ensemble)                                                                                                                | Legal at inference                                                                                | **Illegal** — weights fit in part on ~200 ms aggregate MD, plus AFDB and stability data                                          | AlphaFold DB + MD + ~500k experimental stability measurements                                                                                                               | free-energy accuracy ~1 kcal/mol vs. ms-scale MD                                                                                                                                      | internal MD/experimental comparison                   | free-energy RMSE [VERIFIED-ABSTRACT, doi:10.1038/s41592-025-02874-1]                                                                                                                                                |
| AlphaFlow — PDB variant (2024)                 | sequence                                                                                                                                               | Legal                                                                                             | **Legal** — trained only on deposited PDB structures, no MD                                                                      | PDB structures                                                                                                                                                              | ensemble precision/diversity exceeds AlphaFold+MSA-subsampling                                                                                                                        | PDB                                                   | precision–diversity trade-off [VERIFIED-ABSTRACT, arXiv:2402.04845]                                                                                                                                                 |
| AlphaFlow — MD-finetuned variant               | sequence                                                                                                                                               | Legal at inference                                                                                | **Illegal** — finetuned on all-atom MD ensembles                                                                                 | + MD ensemble data                                                                                                                                                          | captures flexibility and higher-order ensemble observables                                                                                                                            | held-out MD sets                                      | ensemble-observable match [VERIFIED-ABSTRACT, arXiv:2402.04845]                                                                                                                                                     |
| B-factor Bi-LSTM (Pandey et al. 2023)          | sequence + Cα coords + secondary structure; **no allosteric label anywhere**                                                                           | Legal                                                                                             | Legal — trained on experimental B-factors, not MD                                                                                | 56k train / 2.4k val / 2.4k test PDB structures                                                                                                                             | Pearson r = **0.80**; 0.70 vs. 0.54 baseline on a held-out comparison (**~30% relative gain**)                                                                                        | 2,442-protein test set                                | Pearson correlation to experimental B-factor — **untested for allostery, §9** [VERIFIED-FULLTEXT, PMC10499862]                                                                                                      |

**→ Pipeline implication.** Fourteen of the twenty-two rows above are conditionally C1/C2
legal; three are unconditionally illegal (CryptoSite, PocketMiner, BioEmu, plus one illegal
variant of AlphaFlow — four illegal entries total). None of the legal, allostery-specific
rows can be adopted as a pretrained black box without first confirming our benchmark
targets are absent from its training split.

---

## 4. Protein language models — three formulations, one clean route

Three distinct PLM usages appear in this search, and they behave very differently.

**Zero-shot, attention-only.** ESM-1b/ESM-2's self-attention maps carry contact information
after nothing but masked-language-model pretraining on UniRef — no structure, no allostery,
ever, in the loss function [VERIFIED-FULLTEXT] Rao et al., "Transformer protein language
models are unsupervised structure learners," bioRxiv 2020.12.15.422761. Reused with zero
additional training on a 24-protein curated benchmark: **ESM-1b beat a random null in 15/24
proteins** (p < 0.05 by permutation), against Ohm (network model) 7/24 and EVcouplings
(coevolution) 5/24 — and EVcouplings additionally failed outright on 8/24 proteins for want
of MSA depth [VERIFIED-ABSTRACT, bioRxiv 2024.10.03.616547 — this is the exact paper behind
the teammate's card P685]. This is the cleanest C1/C2 survivor in the whole review: the
representation never sees an allosteric label, an MD trajectory, or a holo structure, at
any stage.

**Active-site-conditioned fine-tuning.** A 2025 study fine-tunes pLMs with the orthosteric
site given as an extra input, testing whether "where does the known active site sit"
narrows the search for the unknown allosteric one [VERIFIED-FULLTEXT] bioRxiv
2025.06.27.662060. Fixed-embedding classifiers on ~2,400 ASD examples: Ankh Large AUC-ROC
0.843 / APS 0.490; ProtT5 XL + focal loss AUC-ROC 0.884 / APS 0.553. Conditioning on the
orthosteric site and fine-tuning ESM-2 3B on ~1,520 orthosteric-labelled examples raises
AUC-ROC to **0.948**, APS to 0.614 — but on the paper's own benchmark this ranks **3rd in
accuracy and 4th in recall** against PASSer (accuracy 0.97, recall 0.85, the best model in
that comparison). This nuances the teammate's card, which read the result as "comparable to
the leading structure-based" method [P89-c8]: on the numbers retrieved in full text here,
conditioning closes most but not all of the gap, and a purely structural pocket detector
(PASSer) still leads on this benchmark. Not a contradiction of the card — an elaboration of
the same paper's own comparison table.

**General-purpose fine-tuning without conditioning.** DeepAllo fine-tunes ProtBERT-BFD on
ASD directly (multitask: allostery + secondary structure), reaching F1 89.66% / top-3 90.5%
— but reports no untrained-baseline ablation, so whether the fine-tuning is doing anything
beyond what geometry alone would give is not answerable from the retrieved text. This gap
in the DeepAllo paper's own reporting is exactly what §11 is about.

**ESM-C, Ankh, and general zero-shot mutation scoring.** ESM-C (EvolutionaryScale's newest
representation model, ~2.8B training sequences) exists but was **not found applied to
allosteric or binding-site prediction by the recorded search** — a negative result, not an
absence claim (conventions §2, ADR 0019). The same applies to ESM zero-shot variant-effect
scoring (mutation log-likelihood, itself a pure self-supervised MLM output): it is a
plausible route to a distal-residue functional-importance signal, but no paper in this
search applies it to allostery specifically. [UNVERIFIED — this is a scope note, not a
finding]

**→ Pipeline implication.** If sequence enters the prediction path, §9's zero-shot
attention route is the strongest candidate to prototype first: zero labelled examples,
already validated against two classical baselines on a held-out benchmark, and immune to
every C1/C2 concern raised anywhere else in this file.

---

## 5. Structure-based geometric deep learning

Two sub-classes, and neither one currently has an allostery-specific application in the
literature retrieved this session — this repo's own GNN (§3 table) is the only residue-level
allosteric result found or produced anywhere in this search.

**Equivariant/message-passing GNNs.** VN-EGNN adds virtual nodes to an E(3)/SE(3)-equivariant
message-passing network and sets a new state of the art for **general** binding-site centre
location on COACH420/HOLO4K/PDBbind2020 [VERIFIED-ABSTRACT, doi:10.1186/s13321-025-01127-9].
GVP (Geometric Vector Perceptron) is the underlying equivariant building block used across
protein-design and structure-learning tasks generally [VERIFIED-ABSTRACT — GitHub/paper
metadata only, no allostery application found]. e3nn-family architectures were not found
applied to any allosteric or binding-site task by the recorded search. None of these three
needs MD; all need more than Cβ (side-chain or all-atom geometry, in most published
configurations) — legal, but off-target for allostery until someone runs one on ASD/ASBench
labels the way this repo ran a plainer message-passing GNN.

**Voxel and surface methods.** DeepSite (3D CNN on a voxel grid) and the MaSIF family
(mesh-based, then point-cloud `dMaSIF`) both predict **general** ligandability or
protein–protein interface propensity, not allostery specifically. MaSIF's headline
applications are ligand-class prediction, PPI-site prediction, and ultrafast surface
matching [VERIFIED-ABSTRACT, doi:10.1038/s41592-019-0666-6]; dMaSIF removes MaSIF's
precomputed-mesh bottleneck with an on-the-fly point-cloud convolution
[VERIFIED-ABSTRACT, CVPR 2021]. ScanNet adds MSA-derived evolutionary features to a
geometric deep-learning interface predictor and reaches DockQ ≥ 0.23 on 67% of heteromeric
interfaces [VERIFIED-ABSTRACT, doi:10.1038/s41592-022-01490-7]. All three are C1/C2-legal
in isolation (no MD, no holo of the target) but answer "is there a pocket/interface here at
all," not "is this pocket allosteric." Pairing one with a distance-from-active-site filter
would reproduce, not beat, the `−distance` classical bar already established at AUC 0.617
(conventions §6).

**→ Pipeline implication.** The literature gap this section documents is the same one the
teammate's survey found and this repo's own `gnn/` folder closed for one architecture family
(plain message-passing GNN, Cβ-only). Equivariant and voxel/surface architectures remain
open — untried on allostery, not ruled out.

---

## 6. Foundation models as frozen feature extractors

AF2BIND is the clean exemplar of the pattern Step 3 asks about: **AlphaFold2 itself is never
retrained**; only a logistic-regression head on its pair representation is fit, on 1,902
proteins and 2,110 ligands, reaching 66% binding-residue recovery (69% stacked with ESM2 and
ESM1-IF) [VERIFIED-FULLTEXT, bioRxiv 2023.10.15.562410]. The authors themselves note that
"direct comparison of AF2BIND to other ligand-binding-site predictors is challenging because
most published train/test data-splits contain significant amounts of data leakage" — an
independent confirmation, from inside the foundation-model literature, of exactly the
overlap risk flagged for every ASD-trained tool in §3.

This pattern — large model frozen, small head fit on the target task — is the only way to
reconcile §2's ~15k-parameter capacity ceiling with a large representation: the large model's
own training used a task with orders of magnitude more supervision (AF2's training set, or
UniRef for a PLM), and the allostery-specific fitting touches only a few hundred parameters.
No paper in this search runs this pattern with an **allostery-specific** head on AF2, AF3,
ESMFold, Boltz, or Chai features — only on general binding-site recovery (AF2BIND) or general
structure prediction (ESMFold/Boltz/Chai, none binding-site-specific). This is a second gap,
not a finding: a light allostery-specific classifier on frozen AF2/AF3/ESMFold pair or
structure-module features has not been reported, and is a legal, low-cost design to try
before a deeper architecture. [UNVERIFIED — a design implication, not a retrieved result]

**→ Pipeline implication.** If a foundation-model feature extractor enters the prediction
path, the AF2BIND pattern (frozen backbone, tiny head, general pretraining corpus rather
than an ASD-derived one) is the lowest-leakage-risk way to do it, precisely because its
1,902-protein training corpus is a general PDB pull rather than an allostery-curated set.

---

## 7. Generative and conformational-ensemble models

AlphaFlow and BioEmu both promise exactly what the challenge asks for on paper — "predict
the dynamics ab initio from topology" — and both require care about which **variant** is
being used, because the two variants of AlphaFlow sit on opposite sides of C2.

AlphaFlow fine-tunes AlphaFold/ESMFold under a flow-matching objective. The **PDB-only
variant** (diversity induced by MSA subsampling against deposited structures) is C2-legal:
no MD anywhere in its training. A **second variant, further fine-tuned on all-atom MD
ensembles**, captures flexibility and higher-order observables more accurately — and is C2
**illegal**, because its weights were fit in part on MD trajectories, even though a single
forward pass at inference needs only a sequence [VERIFIED-ABSTRACT, arXiv:2402.04845]. BioEmu
is the same trap in a more dangerous form: it "runs up to 100,000× faster than traditional
simulations" and needs only a sequence at inference, which reads as compliant with "no MD
trajectories as input" — but its weights were fit on ~200 ms of **aggregate MD** simulation
alongside the AlphaFold database and experimental stability data
[VERIFIED-ABSTRACT, doi:10.1038/s41592-025-02874-1]. **Neither method's fast, single-sequence
inference makes it C2-legal** — conventions §4 states this exactly for PocketMiner, and it
applies identically here: "no MD-trained weights in the prediction path," full stop,
regardless of inference cost.

**→ Pipeline implication.** Any conformational-ensemble generator considered for this
pipeline needs its training provenance checked variant-by-variant, not model-by-model.
"Ab-initio-looking at inference" is not the same claim as "C2-legal," and this family is
where that gap is most likely to be missed.

---

## 8. Cryptic-pocket learners

CryptoSite and PocketMiner are the two named in the conventions file, and both fail C2, but
differently — the difference matters for how much of each method survives.

**CryptoSite** fails at both stages. 28 of its 58 training features come from AllosMod MD
simulations, and **new MD simulations are required at inference for every new protein**
("1–2 days on our webserver") — this is not a training-only violation
[VERIFIED-FULLTEXT, doi:10.1016/j.jmb.2016.01.029]. The one salvageable fact: an MD-free
30-feature ablation still reaches AUC 0.74, against 0.83 for the full model — one dynamics
feature (the MD pocket-opening score, AUC 0.73 alone) carries roughly as much signal as the
other thirty static features combined [VERIFIED-FULLTEXT, cross-checked in
`experiments/REGISTRY.md` line 76–77]. That 0.74 is not a certified C2-legal variant — the
ablation was measured on a model whose feature-selection procedure still touched MD data —
but it bounds how much is lost by refusing MD outright on this specific cryptic-pocket task.

**PocketMiner** fails only at training. Inference is a single-structure GNN forward pass,
but the labels it was trained on ("will this residue's pocket open during a short MD run")
are MD-simulated events, over 2,400 simulations across 35 proteins, reaching ROC-AUC 0.87 on
a 39-protein experimentally-confirmed test set [VERIFIED-ABSTRACT, doi:10.1038/s41467-023-36699-3].
Conventions §4 already closes this one; this session's search confirms the exact numbers
behind that closure and adds the CryptoSite MD-free ablation as the field's own measurement
of the cost of compliance.

**→ Pipeline implication.** Neither method can be used as a pretrained black box. If cryptic-
pocket detection is wanted on the prediction path, it must be retrained from a C2-legal
label source — static-structure ensembles from crystallography (multiple deposited
conformers of the same protein) or from an ENM-perturbation proxy, not MD.

---

## 9. Self-supervised and physics-supervised routes needing no allosteric label at all — (c)

This is the most decision-relevant section in this file, because every method above needs
between several hundred and several thousand allosteric labels, and §2 already shows that
ceiling is real and low. Four routes were found, ranked by how far they have already been
validated on allostery specifically.

**1. PLM attention maps, already validated zero-shot (§4).** Masked-language-model
pretraining on UniRef, with zero allosteric labels anywhere in the loss, reused with no
fine-tuning to beat two classical baselines on 15/24 curated proteins
[VERIFIED-ABSTRACT, bioRxiv 2024.10.03.616547]. The only "supervised" step in the whole
chain is a sparse logistic regression fit on ~20 **structures** to pick which attention
heads track contacts [VERIFIED-FULLTEXT, Rao et al. 2020] — a physics label (contact),
not an allostery label, and two orders of magnitude fewer examples than any allostery-
specific tool in §3 needed.

**2. Inverse-folding embeddings, validated for general binding, not yet for allostery.**
ESM-IF1 is trained self-supervised to recover sequence from backbone structure — no MD, no
allostery. AF2BIND's own ablation shows stacking ESM-IF with AF2-pair features moves general
binding-residue recovery from 66% to 69% [VERIFIED-FULLTEXT, bioRxiv 2023.10.15.562410]. Not
tested on allostery specifically by any paper in this search.

**3. Experimental-B-factor prediction, untested for allostery.** A sequence-plus-coordinate
Bi-LSTM trained on 56k/2.4k/2.4k PDB structures' **experimental B-factors** — no MD, no
allostery label — reaches Pearson r = 0.80 and explicitly names "identifying active regions
… for pharmaceutical applications" as a motivating future use, without testing it
[VERIFIED-FULLTEXT, PMC10499862]. Flexibility is mechanistically close to allostery (the
elastic-network hypothesis, C6, is exactly the claim that fluctuation encodes function), so
this is a plausible untried route, not a validated one.

**4. ENM parameters fit to B-factors, then reused via perturbation response.** This is what
`ALPS`, `APOP`, AlloPred and ZHMolEReP already do: an elastic-network model's spring
constants are physics, not fit to any protein-specific data, but the network's ability to
reproduce experimental fluctuations is itself a form of physics-supervision against an
abundant, non-allosteric label (crystallographic B-factors broadly). This is why conventions
§6 names APOP/ESSA as the C1/C2/C6-clean bar already in production — it is the field's
existing answer to this question, just not usually described as "self-supervised."

**→ Pipeline implication.** Route 1 is ready to prototype today at effectively zero labelled-
data cost. Routes 2–4 are legal but unvalidated for allostery specifically — each is a
one-paragraph experiment (fit nothing new, just correlate an existing frozen output against
this repo's curated labels) before any larger model is built.

---

## 10. Which AI methods are legal under C1 and C2, exactly as written — (b)

Applying both constraints strictly, at both training and inference, per method:

**Unconditionally illegal — do not use, even as a pretrained artifact:**

- **PocketMiner** — MD-trained weights (conventions §4 already states this; confirmed here).
- **CryptoSite** — MD-trained weights **and** MD required at inference; the more severe case.
- **BioEmu** — weights fit in part on ~200 ms aggregate MD, despite single-sequence, fast
  inference. Looks compliant; is not.
- **AlphaFlow, MD-finetuned variant** — same trap as BioEmu, one variant only.

**Conditionally legal — legal architecture and training procedure, but every row needs its
training split checked against our benchmark targets before use (§3's "Legal\*"):**
PASSer/PASSer2.0/PASSerRank, DeepAllo, MEF-AlloSite, Allo-PED, AlloPred, AllositePro,
Allo-Allo, AlloFusion, STINGAllo, AlloEF, ZHMolEReP (pending the learned-weights question),
AF2BIND (lower risk — general PDB corpus, not ASD), and this repo's own GNN and hybrid
combiner (lowest risk — trained on a 96/44-target external curated set, not the frozen 4+9
benchmark targets).

**Unconditionally legal, and allostery-agnostic (need pairing with a distance filter to
become relevant, which reproduces rather than beats the classical `−distance` bar):**
DeepSite, VN-EGNN, MaSIF/dMaSIF/ScanNet, AlphaFlow PDB-only variant.

**Unconditionally legal and the cleanest in the entire review:** the §9 zero-shot PLM
attention route (no allosteric label, no MD, no holo, anywhere in the pipeline) and the §9
B-factor Bi-LSTM (same properties, untested for allostery).

**→ Pipeline implication.** The practical shortlist for a legal AI comparison arm is short:
this repo's own GNN and hybrid combiner (already measured, §3), the zero-shot PLM attention
route (not yet run on this repo's targets), and — if a target-overlap check clears it —
AF2BIND's frozen-feature-plus-light-head pattern applied to a new, allostery-specific head.
Everything ASD/ASBench-trained needs that check before it can be called legal rather than
merely legal-shaped.

---

## 11. Where learning helps and where it hurts — ranking vs. localisation — (d)

This repo already measured the split the task asks about, twice, in two model families, and
the literature confirms the same pattern a third time.

**This repo, learned combiner, proxy labels / plain AUC (the number this file was asked to
check):** AUC 0.606 (`ALPS` alone) → **0.668** with a classical learned combiner — but top-5
hit rate **falls** 27.1% → 18.6% [VERIFIED-FULLTEXT, `hybrid/README.md`]. Read this number
beside its protocol: it predates the curated-label correction (conventions §5's "eleven
insertion points"), and was measured on the confounded proxy-label, plain-AUC protocol this
repo's own §10 later showed reverses rankings. The **corrected** re-run (curated labels,
distance-stratified AUC, Gate 0) shows a much smaller and non-significant gap: logistic
regression 0.603 vs. unlearned `ALPS` 0.576, **+0.027, p = 0.72** — and does not re-report a
top-5 hit-rate split at all [VERIFIED-FULLTEXT, `hybrid/RESULTS.md`]. Both numbers are real;
they answer different questions, and the corrected one is the one to trust for magnitude.
The direction — ranking gain, localisation-metric stagnation-or-loss — reproduces in both.

**This repo, residue-graph GNN, curated labels / stratified AUC (a second, independent model
family):** the GNN ties `ALPS` on ranking (0.622–0.630 vs. 0.592, not significant at n = 96)
— but the sharper result is the ablation. Handing the model a distance-to-anchor feature
makes it **worse**, 0.622 → 0.595, collapsing its margin over `ALPS` to nothing
[VERIFIED-FULLTEXT, `gnn/README.md`, `gnn/RESULTS.md`]. This is not identical to the
AUC/hit-rate split above — it is "learning latches onto the easy confound and generalises
worse when denied it" rather than "ranking improves while localisation degrades" — but both
are instances of the same underlying fact: a model that is allowed to exploit distance-to-
active-site will, and doing so does not help it find the actual site.

**Literature, PASSer2.0's own numbers (the clearest external confirmation found):** the
untrained FPocket-rank geometric baseline places a true positive pocket in the top three for
**84.3%** of test proteins; PASSer2.0's trained AutoML model does it for **82.7%**
[VERIFIED-ABSTRACT, doi:10.3389/fmolb.2022.879251 — cross-checked against teammate's card
P48]. The learned model clearly improves precision/recall/F1 over the same untrained rule,
but on the exact top-3 localisation metric the challenge's own Hit List deliverable maps to
most closely, it does not lead. This is an independently published instance of the same
ranking-improves/localisation-does-not(-or-worsens) pattern, in a different lab, a different
protein set, and a different model family than either of this repo's own results — three
independent confirmations now, not one repo's quirk.

**A fourth, weaker instance:** Allo-PED's own reported numbers show pocket-level AUC 0.920
against residue-level precision 0.601/recall 0.422 on the same method — a granularity-driven
version of the same divergence, flagged as unexplained in the teammate's survey (§7 there)
and now connected explicitly to this theme.

**→ Pipeline implication.** Any AI component added to this pipeline must be evaluated on
both a ranking metric and a localisation metric (top-K hit rate or DCC) before being called
an improvement. A ranking-only report — which is what most of §3's table rows provide — is
not sufficient evidence that learning helped the deliverable the challenge actually scores
(`CHALLENGE.md` §5, the top-5 Hit List).

---

## 12. The AUROC/AUPR trap — how widespread, and what to report instead — (e)

Three independent sources, at three different severities, all on allosteric-site tasks:

| source                                                                 | AUROC       | AUPR / APS                                                                    | prevalence                   | note                                                                                                                                                                            |
| ---------------------------------------------------------------------- | ----------- | ----------------------------------------------------------------------------- | ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Riedlová et al. 2026 (kinase frustration)                              | 0.70        | **0.06** (orthosteric 0.64–0.76 on the same proteins)                         | < 3%                         | mechanistic, not imbalance-only: allosteric residues show "neutral mutational frustration," orthosteric residues do not [VERIFIED-FULLTEXT, bioRxiv 10.64898/2026.01.05.697819] |
| Orthosteric-conditioning study, best pLM                               | 0.843–0.948 | 0.490–0.614                                                                   | ASD pool, not stated exactly | a smaller but still large gap — 0.25–0.4 absolute — at a milder imbalance [VERIFIED-FULLTEXT, bioRxiv 2025.06.27.662060]                                                        |
| This repo's own evaluation harness, geometric `cavity_volume` baseline | 0.48–0.59   | **0.012–0.162**, three of five arms at/below their own prevalence chance line | 1.9–8.1% (primary arms)      | not an AI method at all — same trap on a zero-parameter geometric detector [VERIFIED-FULLTEXT, `experiments/REGISTRY.md`, "Evaluation layer" table]                             |

The third row is the one that reframes the question: **the AUROC/AUPR gap is not an AI-
specific failure.** It is a structural consequence of this task's severe class imbalance
(1.3–8% positive prevalence, consistent across every dataset counted in §2) combined with
AUROC's insensitivity to prevalence. AI methods are simply the most visible victims because
published papers report AUROC and rarely report AUPR against its own prevalence baseline —
exactly the trap the teammate's card [P89-c1,c2,c3] already names in general terms; this
session adds the mechanistic explanation and a same-repo, non-AI confirmation that the trap
is task-structural rather than model-specific.

**What the field should report instead**, in order of how directly each maps to the
challenge's own scored artifact (`CHALLENGE.md` §5, §7):

1. **AUPR beside its own prevalence chance line**, not beside 0.5 — a raw AUPR of 0.15 on a
   task with 2% positives is well above chance; the same 0.15 on a 50%-positive task is not.
2. **Top-K hit rate at the exact K the deliverable requires** (top-5) — this repo's own
   `recall@5 of that same cavity-volume baseline: 0.00 on all five primary arms` is the
   single clearest instance in the whole project of a method rejecting the statistical null
   while producing a useless hit list [VERIFIED-FULLTEXT, `experiments/REGISTRY.md`].
3. **DCC (distance from the predicted centroid to the nearest true site)** as a localisation
   metric distinct from any ranking metric — this repo measured a case where the predicted
   centre was farther from the true site than a random five-residue list, on the same arm
   where the ranking metric rejected the null at p = 0.0003 [VERIFIED-FULLTEXT,
   `experiments/REGISTRY.md`].
4. **Distance-stratified or proximity-matched AUC**, because plain AUC on this task is
   dominated by proximity to the active site on every label set this repo has checked
   (conventions §5).

**→ Pipeline implication.** Any number this project reports for an AI (or quantum) method
must be accompanied by an AUPR-vs-prevalence figure and a top-5/DCC figure, not AUROC alone.
This is now enforceable against three independent sources, not asserted from one.

---

## What this changes for our pipeline

- **Architecture stage.** The ~15k-parameter capacity ceiling (§2) and the two validated
  in-repo results (GNN 0.622–0.630, learned combiner 0.576→0.603 under the corrected
  protocol) mean a learned classical or hybrid component, if added, should be small and
  should not be handed a distance-to-active-site feature — denying it measurably helped in
  the one architecture tested (§11).
- **Legality gate, before any external model is adopted.** No ASD/ASBench/CASBench-trained
  tool in §3 may be used as a pretrained artifact until its training split is confirmed to
  exclude KRAS G12C, BCR-ABL1, cardiac myosin, c-Myc, and the nine secondary targets (§3, §10).
  This is a concrete, checkable pre-condition, not a vague caveat.
- **Prototyping order, if a legal AI arm is wanted.** Try the zero-shot PLM attention route
  first (§9, route 1) — zero labelled examples, already validated against two classical
  baselines externally. Only then consider fine-tuning anything.
- **Excluded outright, and why it matters that they looked compliant.** PocketMiner,
  CryptoSite, BioEmu, and MD-finetuned AlphaFlow are all disqualified by C2 even though three
  of the four need only a single sequence or structure at inference (§7, §8). "Fast,
  single-structure inference" is not evidence of C2 compliance; training provenance is.
- **Reporting standard for every future method file in this series, AI or quantum.** Report
  AUPR against its own prevalence line, top-5 hit rate, and DCC alongside any AUROC number
  (§12) — three independent sources in this file show AUROC alone is misleading at this
  task's prevalence, and this repo's own evaluation harness reproduces the same trap on a
  non-AI baseline.
- **Comparison target for a hybrid quantum+AI method.** Not `ALPS` (0.592–0.606 depending on
  protocol) alone. The bar is whichever number in §3's table is highest **on the metric the
  deliverable actually needs** — for ranking, the GNN's 0.622–0.630 (tied with `ALPS`, not
  beating it); for localisation, no learned method in this file has been shown to beat the
  classical baselines on top-5 or DCC.

---

## Method

**Databases and routes used:** WebSearch (34 queries, 33 returned results — the ASD/KRAS
overlap-risk query was blocked by the session's search quota and not run), WebFetch against
bioRxiv full-text and abstract pages, PMC full-text articles, PubMed/Europe PMC metadata,
and ACS/ScienceDirect/Nature abstract pages; plus direct `Read` of this repository's own
`experiments/REGISTRY.md` and the `allosteric-benchmark/` sub-repository's `README.md`,
`hybrid/README.md`, `hybrid/RESULTS.md`, `gnn/README.md`, and `gnn/RESULTS.md`, which turned
out to hold the primary evidence for §11's headline finding.

**Queries (representative, not exhaustive — 34 total):** for each named method in Step 2's
list, `"<method name>" allosteric site prediction`; `ASBench`/`CASBench`/`AlloBench`/`ASD`
dataset-size queries; `ESM-2`/`ESM-1b`/`ESM-C`/`ProtT5`/`Ankh` × `allosteric OR binding site`;
`MaSIF`/`dMaSIF`/`ScanNet`/`VN-EGNN`/`GVP` × `binding site prediction`; `AF2BIND`;
`AlphaFlow`/`BioEmu` × `conformational ensemble`; `CryptoSite`/`PocketMiner` × `cryptic
pocket`; `B-factor prediction sequence-based deep learning`; `PLM attention map contact
prediction unsupervised`.

**Counts:** 34 WebSearch queries run, 33 returned usable results (1 blocked by quota). 16
WebFetch calls, 10 returned usable full or near-full text, 6 failed (4× HTTP 403 —
ScienceDirect ×2, ACS ×2; 1× corrupted/binary PDF response ×2 counted once each for
PASSerRank and the kinase-frustration paper's PDF route, recovered via the HTML route for
the latter; 1× empty response). 8 internal `Read` calls against this repository's own
experiment records.

**Stopping rule:** every named method in Step 2's minimum list was located and at least
minimally characterised (AllositePro and AlloFusion have the thinnest retrieved detail — see
their table rows for exactly what is missing). The search stopped when three consecutive new
queries (EGNN/e3nn-for-allostery, ESM-C-for-allostery, ALLO-tool-specific Table S2 detail)
returned no new allostery-specific result, each logged above as a negative result rather than
omitted.

**Not reached this session:** ZHMolEReP's full text (JCIM, 403) — its C1/C2 verdict is
recorded but its "does it have a learned weight" question is open. AllositePro's and
AlloFusion's exact numeric results (both behind ACS paywalls that returned 403). A per-target
check of whether KRAS G12C, BCR-ABL1, cardiac myosin, or any secondary-set target appears in
ASD/ASBench/CASBench's own protein lists — this would resolve §3's "Legal\*" caveat from a
reasoned risk into a checked fact, and is the single highest-value follow-up this file did
not complete.
