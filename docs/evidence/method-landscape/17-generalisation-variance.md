# Between-target variance: how much site-prediction performance moves from protein to protein, and what the field reports about it

**Scope:** the observed dispersion of allosteric-, cryptic- and binding-site prediction performance
_across targets_ and _across benchmarks_ — whether published methods report per-target results at
all, what spread they show when they do, whether a documented easy/hard target phenomenon exists,
what generalisation gaps are measured when a method moves to a new set, and how much of the field's
reported variance is attributable to benchmark composition. It deliberately excludes methods for
_reducing_ that variance: graph construction (`13-graph-construction.md`), distance detrending and
radial normalisation (`14-distance-confound.md`), and pretrained front ends, algorithm selection and
meta-features (`15-ai-preprocessing.md`).
**Sibling files:** `13-graph-construction.md`, `14-distance-confound.md`, `15-ai-preprocessing.md`
(the three files this one must not duplicate), `09a-power-verification.md` and
`../exploration/results/41-selection-and-power.md` (what four arms resolve),
`../exploration/results/40-method-sweep.md` (the numbers being calibrated),
`../exploration/results/44-stability-and-noise.md` (within-target stability, which is a different
axis), `00-conventions.md` (evidence tags, C1–C6, the leakage guard).
**Retrieved:** 2026-08-27.

---

## 0. Executive summary — the sentences that matter

**The verdict first, because it is the question asked.** A between-target spread in mean AUC-ROC of
**0.175 across four proteins is typical, and on the evidence below it is not even distinguishable
from the sampling error of AUC at our arm sizes**. A spread of **0.361 is large — roughly 2.1× what
estimator noise alone would produce — but it is not off-scale for this field**, and it is the
signature of an uninformative score rather than of a broken pipeline. The literature cannot settle
this by itself, because no retrieved paper reports a between-target standard deviation of AUC for
allosteric or cryptic-site prediction. The arithmetic that does settle it is ours, and it is in §6.

Seven findings, each with its section.

1. **Pooled reporting is the norm; per-target tables are the exception.** PocketMiner's headline
   ROC-AUC of 0.87 is computed over 563 positive and 1283 negative residues pooled across 35
   structures, and no per-structure AUC appears anywhere in the paper
   (doi:10.1038/s41467-023-36699-3) [VERIFIED-FULLTEXT]. PASSer, AlloPred, Ohm and STINGAllo report
   aggregate rates only. **Between-target variance is invisible by construction in most of this
   literature.** §1.

2. **The one part of the field that does report per target reports enormous spread.** In CASP10's
   binding-site category, per-target median MCC runs from about **−0.05 to about 0.6** over 13
   targets (doi:10.1002/prot.24495) [VERIFIED-FULLTEXT]. CryptoSite's per-protein sensitivities run
   from **0 % (HCV RNA polymerase) to 100 % (GluR2)** on a 14-protein held-out set
   (doi:10.1016/j.jmb.2016.01.029) [VERIFIED-FULLTEXT]. §2.

3. **The field has stated, in print, that target effects exceed method effects.** The CASP9
   assessors wrote that the 12 top-performing groups "show overall a similar spectrum of results,
   with a few nearly perfectly predicted targets and some poorly predicted targets" and concluded
   that "either the performance of the different methods is highly target specific, or there is a
   considerable random component in the prediction process" (doi:10.1002/prot.23174)
   [VERIFIED-FULLTEXT]. §3.

4. **Difficulty descriptors have been proposed and none has been validated on held-out targets.**
   Template availability, magnitude of apo→holo conformational change, ligand size and
   hydrophobicity, burial, multimeric complexity, proximity to the orthosteric site, and binding-site
   class have all been named. Every one is post-hoc failure analysis. No fitted, held-out-tested
   difficulty model was retrieved by the recorded search. §4.

5. **Cross-benchmark drops are real but modest when the criterion is held fixed, and catastrophic
   when leakage is removed.** PocketMiner drops from 0.87 on its own test set to **AUC 0.76,
   AUPRC 0.19** on CryptoBench (doi:10.1093/bioinformatics/btae745) [VERIFIED-FULLTEXT]. PASSerRank
   drops 3.2 points top-1 from ASD to CASBench (doi:10.1002/jcc.27193) [VERIFIED-FULLTEXT]. But
   AlloBench, which drops every test protein sharing a UniRef50 cluster with a training protein,
   puts the best of eight tools at **18 %** (doi:10.1021/acsomega.5c01263) [VERIFIED-FULLTEXT]
   against the 80–85 % top-3 those tools report for themselves — under a different hit criterion. §5.

6. **Benchmark identity is not benchmark composition.** P2Rank scores 68.6 % DCA Top-n on HOLO4K as
   curated in 2018 (doi:10.1186/s13321-018-0285-8) and **81.2 % on "HOLO4K(Mlig+)"**, the same named
   set re-filtered for bound and relevant ligands (doi:10.1021/acs.jcim.3c01698) [both
   VERIFIED-FULLTEXT]. A 12.6-point move from a curation decision, with the method unchanged. §5.

7. **The largest single-model spread retrieved is between binding-site classes inside one protein
   family.** A fine-tuned protein language model on kinases scores AUROC **0.968 / AUPR 0.629** on
   Type I orthosteric sites and AUROC **0.676 / AUPR 0.077** on Type IV allosteric sites — same
   model, same proteins (doi:10.1021/acs.jctc.6c00427) [VERIFIED-FULLTEXT]. An AUROC spread of
   **0.292** and an AUPR spread of **0.552**. §2.

---

## Q1 — Do published methods report per-target results, or only pooled?

Mostly pooled. The table below records what each paper actually prints. "Per-target table" means a
row per protein in the paper or its supplement with a numeric score, not a case study.

| Method / assessment                   | Source                                         | Per-target results?                                                  | Headline number and criterion                                                | Evaluation set                                                                            |
| ------------------------------------- | ---------------------------------------------- | -------------------------------------------------------------------- | ---------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| **PARS**                              | doi:10.1186/1471-2105-13-273                   | Not in the abstract; main text not retrieved                         | 65 % positive predictive value for identifying allosteric sites              | 91 non-redundant allosteric proteins [VERIFIED-ABSTRACT]                                  |
| **AlloSite**                          | not retrieved this session                     | unknown                                                              | —                                                                            | —                                                                                         |
| **AlloPred**                          | doi:10.1186/s12859-015-0771-1                  | **No** ("no per-protein results table is provided")                  | 23/40 proteins with an allosteric pocket ranked top; 28/40 top-2             | 40 test proteins from ASBench Core-Diversity [VERIFIED-FULLTEXT]                          |
| **CryptoSite**                        | doi:10.1016/j.jmb.2016.01.029                  | **Yes** — per-protein sensitivities for training and test proteins   | AUC 0.83; TPR 79 % / FPR 29 % at threshold 0.05                              | 14 held-out apo structures; 79-protein LOO training set [VERIFIED-FULLTEXT]               |
| **Ohm**                               | doi:10.1038/s41467-020-17618-2                 | **No** — aggregate plus five named exemplars                         | mean TPR 0.57, PPV 0.72 (vs 0.23 / 0.48 for the comparator)                  | 20 allosterically regulated proteins, 147–3311 residues [VERIFIED-FULLTEXT]               |
| **PASSer** (Ensemble / AutoML / Rank) | doi:10.1093/nar/gkad303                        | **No**                                                               | top-1 60.7 / 65.1 / 59.5 %; top-3 84.9 / 82.7 / 83.6 %                       | ASD test split; models trained on 90 / 204 / 207 proteins [VERIFIED-FULLTEXT]             |
| **PASSerRank, external**              | doi:10.1002/jcc.27193                          | **No**                                                               | top-1 56.3 %, top-2 73.7 %, top-3 80.5 %                                     | CASBench, ASD training proteins removed [VERIFIED-FULLTEXT]                               |
| **APOP**                              | doi:10.1093/bioinformatics/btad275             | Not retrieved                                                        | 92 of 104 test cases with a known allosteric pocket in the top 3             | 104 allosteric proteins, monomers and assemblages [VERIFIED-ABSTRACT]                     |
| **PocketMiner**                       | doi:10.1038/s41467-023-36699-3                 | **No** — residue-level pooled                                        | ROC-AUC 0.87 over 563 cryptic-pocket residues and 1283 non-pocket residues   | 24 apo + 4 hyper-rigid + 7 screened structures [VERIFIED-FULLTEXT]                        |
| **STINGAllo**                         | doi:10.1093/bib/bbaf424                        | **No**                                                               | DCC success 78 %; per-residue F1 0.64, MCC 0.64, pooled                      | 91 ASBench chains held out of training [VERIFIED-FULLTEXT]                                |
| **P2Rank**                            | doi:10.1186/s13321-018-0285-8                  | Per-**dataset**, not per-target                                      | DCA Top-n 72.0 % (COACH420), 68.6 % (HOLO4K)                                 | COACH420, HOLO4K [VERIFIED-FULLTEXT]                                                      |
| **GrASP**                             | doi:10.1021/acs.jcim.3c01698                   | Per-**dataset**                                                      | DCA Top-n 85.3 % (sc-PDB CV), 77.5 % (COACH420 Mlig+), 81.3 % (HOLO4K Mlig+) | three sets [VERIFIED-FULLTEXT]                                                            |
| **AlloBench**                         | doi:10.1021/acsomega.5c01263                   | **Yes**, in Supporting Information Table S3                          | best of eight tools 18 % at Jaccard > 0.5                                    | 2141 allosteric sites, 2034 PDB structures, 418 unique UniProt chains [VERIFIED-FULLTEXT] |
| **Bond-to-bond propensity**           | doi:10.1016/j.patter.2021.100408               | Per-**structure** counts of how many of six measures detect the site | 83.9 % (ASBench, 118 structures); 96.8 % (CASBench, 314 structures)          | two benchmarks [VERIFIED-FULLTEXT]                                                        |
| **PLM on kinase site classes**        | doi:10.1021/acs.jctc.6c00427                   | Micro- **and** macro-averaged, with interquartile ranges by family   | AUROC 0.968 (Type I) to 0.676 (Type IV allosteric)                           | KinCoRe, 10 301 complexes, 453 kinases [VERIFIED-FULLTEXT]                                |
| **CASP FN category**                  | doi:10.1002/prot.24495, doi:10.1002/prot.23174 | **Yes — routinely, per target**                                      | see §2                                                                       | 13 targets (CASP10), 30 targets (CASP9) [VERIFIED-FULLTEXT]                               |

**The structural observation is the finding.** PocketMiner's estimator pools every residue of every
test structure into one ROC curve. Under that estimator a method that scores 0.99 on half the
proteins and 0.55 on the other half prints a single number near 0.87, and the reader cannot tell
which world they are in. Our own harness averages a per-arm AUC, which is a macro estimator, and the
per-arm numbers survive. **The comparison "our 0.810 versus PocketMiner's 0.87" is not a comparison
at all**, and not only for the usual reasons of dataset and positive class. The two numbers are
different statistics.

**One paper in the retrieved set reports both estimators.** The kinase PLM study prints micro- and
macro-averaged MCC separately and notes that the PLM "exhibited narrower interquartile ranges across
families, indicating more consistent performance and reduced variance relative to P2Rank"
(doi:10.1021/acs.jctc.6c00427) [VERIFIED-FULLTEXT]. That is the only retrieved instance of a
site-prediction paper treating between-target dispersion as a reportable property of a method.

---

## Q2 — What is the reported between-target spread of the headline metric?

**No paper retrieved reports a between-target standard deviation of AUC for allosteric or
cryptic-site prediction.** A Europe PMC full-text search for `"per-target AUC" OR "per-structure
AUC" OR "per-protein AUC"` conjoined with `pocket OR "binding site" OR allosteric` returned two
records, neither in this task (§Method). Record that as a negative result of the recorded search,
not as an absence.

What the field does report, converted where possible into a spread:

| Source                                                                 | Unit of variation                                     | Metric                                      | Observed spread                                                                                                                                                                                                                                                                                        |
| ---------------------------------------------------------------------- | ----------------------------------------------------- | ------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| CASP10, doi:10.1002/prot.24495                                         | 13 targets                                            | per-target **median** MCC across all groups | "On most targets the predictors achieved on average a good performance around an MCC of 0.6, except in three cases, where in two (T0657 and T0659) the median scores were around zero and in one (T0720) was around 0.2." Worst target median MCC **−0.05**. Spread ≈ **0.65 MCC** [VERIFIED-FULLTEXT] |
| CASP9, doi:10.1002/prot.23174                                          | 30 targets                                            | best-prediction MCC per target              | best prediction per target averaged **0.84**; on the hardest target, T0604, the best prediction reached **0.56** and the average was **0.29**. Spread in best-per-target ≈ **0.28** [VERIFIED-FULLTEXT]                                                                                                |
| CryptoSite, doi:10.1016/j.jmb.2016.01.029                              | individual proteins                                   | per-protein sensitivity                     | **0 %** (HCV RNA polymerase), 6 % (Ca-ATPase), 17 % (kynurenine aminotransferase II), 29 % (PTP1B allosteric site), 56 % (biotin carboxylase), 68 % (exportin 1), 89 % (β-lactoglobulin), 98 % (acyl-CoA binding site), 100 % (GluR2). Spread **0–100 %** [VERIFIED-FULLTEXT]                          |
| Kinase PLM, doi:10.1021/acs.jctc.6c00427                               | 5 binding-site classes, one protein family, one model | AUROC / AUPR                                | AUROC **0.676 → 0.975** (spread **0.299**); AUPR **0.077 → 0.749** (spread **0.672**) [VERIFIED-FULLTEXT]                                                                                                                                                                                              |
| Bond-to-bond propensity, doi:10.1016/j.patter.2021.100408              | 2 benchmarks                                          | detection rate                              | **83.9 % → 96.8 %** (spread 12.9 points) [VERIFIED-FULLTEXT]                                                                                                                                                                                                                                           |
| AlloPred / AlloSite / PARS head to head, doi:10.1186/s12859-015-0771-1 | 3 methods, 1 set of 40 proteins                       | top-1 hit rate                              | **10/40, 21/40, 23/40** — a 32.5-point method spread on a fixed target set, with AlloPred making "4 correct predictions that neither of the other methods do" [VERIFIED-FULLTEXT]                                                                                                                      |
| STINGAllo, doi:10.1093/bib/bbaf424                                     | method class, 1 benchmark                             | success rate                                | **60.2 %** versus **21.1–24.2 %** for "contemporary pocket-based predictors" on the same 91-chain test set [VERIFIED-FULLTEXT]                                                                                                                                                                         |

**Two things follow.** First, where per-target numbers exist they span most of the available range of
the metric — 0 to 1 in sensitivity, roughly −0.05 to 0.7 in MCC. Second, the AUROC-specific spreads
are smaller than the spreads in precision-style metrics, which is the same asymmetry
`13-graph-construction.md` records for the cutoff sweep: AUROC is the axis least able to see
composition change. The kinase PLM shows it cleanly — AUROC moves 0.299 between site classes while
AUPR moves 0.672.

---

## Q3 — Is there a documented easy-target / hard-target phenomenon?

Yes, and in the assessment literature it is stated explicitly rather than inferred.

**The strongest statement is CASP9's.** After comparing the 12 top-performing groups the assessors
wrote [VERIFIED-FULLTEXT, doi:10.1002/prot.23174]:

> the 12 top performing groups show overall a similar spectrum of results, with a few nearly
> perfectly predicted targets and some poorly predicted targets

and concluded

> either the performance of the different methods is highly target specific, or there is a
> considerable random component in the prediction process

That is the field, in a formal assessment, reporting that the target explains more of the variance
than the method does, and declining to distinguish "target effect" from "noise". **Our four-arm
spread is the same observation at n = 4.**

**CASP10 repeats the pattern at target level** [VERIFIED-FULLTEXT, doi:10.1002/prot.24495]: most
targets sit near median MCC 0.6, two sit near zero, one near 0.2. The distribution is not
unimodal-with-scatter; it is a bulk plus a failure mode.

**Descriptors proposed for what makes a target easy.** Each is listed with the source and with what
would count as validation.

| Descriptor                                       | Source                                                                                                                                                                        | Direction                  | Validated on held-out targets?                                                                                                             |
| ------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| Homologous holo template available               | CASP9 [VERIFIED-FULLTEXT] — "Easily detectable homologous structures of this protein did not contain any ligand, which explains the overall weak performance" (CASP10, T0659) | template present → easier  | **No.** Post-hoc explanation of two named failures                                                                                         |
| Magnitude of apo→holo conformational change      | CryptoSite [VERIFIED-FULLTEXT] — failures occur with "large conformational changes"                                                                                           | small change → easier      | **No.** Post-hoc                                                                                                                           |
| Ligand size and hydrophobicity                   | CryptoSite [VERIFIED-FULLTEXT] — best results where "large and hydrophobic ligand binds to a cryptic site"                                                                    | large hydrophobic → easier | **No.** Post-hoc                                                                                                                           |
| Site completed by a second chain                 | CryptoSite [VERIFIED-FULLTEXT] — "partial sites that require binding to another protein chain" fail                                                                           | single-chain site → easier | **No.** Post-hoc                                                                                                                           |
| Buried versus exposed site, protein size         | CryptoSite [VERIFIED-ABSTRACT] — more accurate than FTFlex "when a cryptic site was fully buried or when it resided in a large protein"                                       | method-dependent           | **No.** Pairwise comparison on 14 proteins                                                                                                 |
| Multimeric complexity and cooperativity          | Wu et al. [VERIFIED-FULLTEXT] — difficult cases were "large and complex multimeric proteins"                                                                                  | monomer → easier           | **No.** Post-hoc                                                                                                                           |
| Proximity of allosteric to orthosteric site      | Wu et al. [VERIFIED-FULLTEXT] — sites "in close proximity" confound direct interaction with allosteric coupling                                                               | far → cleaner, not easier  | **No.** This is the distance confound, and `14-distance-confound.md` owns it                                                               |
| Binding-site class (orthosteric vs allosteric)   | Kinase PLM [VERIFIED-FULLTEXT] — allosteric sites "lack discriminative sequence signatures"                                                                                   | orthosteric → far easier   | **Partly.** Split by class with a 30 % sequence-identity filter between train and test; but class is not a per-target difficulty predictor |
| Multi-chain / larger structures in the benchmark | P2Rank [VERIFIED-FULLTEXT] — "HOLO4K contains mainly multimers and COACH420 only single-chain proteins"                                                                       | single-chain → easier      | **No.** Offered as an explanation of a dataset-level gap                                                                                   |

**The honest summary of Q3: the phenomenon is documented, the descriptors are folklore.** Every
proposed descriptor in the retrieved corpus is a narrative attached to observed failures after the
fact. No paper retrieved fits a difficulty model on one set of targets and tests its predictions on
another. The one adjacent framework that would formalise this — Rice's algorithm-selection problem
and its meta-feature machinery — is surveyed in `15-ai-preprocessing.md`, which also gives the
arithmetic for why such a selector cannot be validated at our N.

---

## Q4 — Generalisation gaps when a method moves to a new set

Quantified where numbers exist. **Read the "criterion" column before comparing rows**; the field's
hit criteria differ and the differences are larger than most of the gaps.

| Method                | Home number                                                                                   | Away number                                                                                                                   | Gap                    | Criterion held fixed?                                                                                                                                                                                                                                        |
| --------------------- | --------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- | ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **PocketMiner**       | ROC-AUC **0.87**, own 35-structure test set, residues pooled (doi:10.1038/s41467-023-36699-3) | ROC-AUC **0.76**, AUPRC **0.19**, CryptoBench test set, pre-trained model, no retraining (doi:10.1093/bioinformatics/btae745) | **−0.11 AUC**          | Both residue-level ROC-AUC. Closest thing to a clean cross-benchmark AUC delta in this field [VERIFIED-FULLTEXT]                                                                                                                                             |
| **PASSerRank**        | top-1 **59.5 %**, top-3 **83.6 %**, ASD 20 % test split                                       | top-1 **56.3 %**, top-3 **80.5 %**, CASBench with ASD training proteins removed                                               | **−3.2 / −3.1 points** | Yes, same top-k pocket criterion. The authors call it "decreased but within an acceptable range" [VERIFIED-FULLTEXT]                                                                                                                                         |
| **P2Rank**            | DCA Top-n **72.0 %**, COACH420                                                                | DCA Top-n **68.6 %**, HOLO4K                                                                                                  | **−3.4 points**        | Yes [VERIFIED-FULLTEXT]                                                                                                                                                                                                                                      |
| **DeepSite**          | DCA Top-n **56.4 %**, COACH420                                                                | DCA Top-n **45.6 %**, HOLO4K                                                                                                  | **−10.8 points**       | Yes. Note this **reorders** the leaderboard: DeepSite ties Fpocket on COACH420 and is 6.8 points behind it on HOLO4K [VERIFIED-FULLTEXT]                                                                                                                     |
| **GrASP**             | DCA Top-n **85.3 %**, sc-PDB 10-fold CV                                                       | **77.5 %** COACH420(Mlig+), **81.3 %** HOLO4K(Mlig+)                                                                          | **−7.8 / −4.0**        | Yes, but CV→held-out is a different comparison from benchmark→benchmark [VERIFIED-FULLTEXT]                                                                                                                                                                  |
| **PARS**              | **65 %** PPV on 91 allosteric proteins, own paper                                             | **10/40 = 25 %** top-1 in AlloPred's re-run on ASBench Core-Diversity                                                         | not comparable         | **No.** PPV versus top-1 rank. Reported here to show how large a criterion change looks [VERIFIED-ABSTRACT / VERIFIED-FULLTEXT]                                                                                                                              |
| **APOP**              | **92/104 = 88.5 %** top-3, own paper                                                          | **15 %** at Jaccard > 0.5 in AlloBench, UniRef50 relatives of training data dropped                                           | not comparable         | **No.** Top-3 pocket rank versus Jaccard overlap threshold [VERIFIED-ABSTRACT / VERIFIED-FULLTEXT]                                                                                                                                                           |
| **PASSer (Ensemble)** | top-3 **84.9 %**, ASD                                                                         | **18 %** at Jaccard > 0.5, AlloBench                                                                                          | not comparable         | **No**, same reason [VERIFIED-FULLTEXT]                                                                                                                                                                                                                      |
| **PASSer, APOP**      | holo input                                                                                    | apo input                                                                                                                     | direction only         | CAPASP reports both tools "showed better results with holo state proteins than apo state proteins" over two independent datasets (CAPASP-General, CAPASP-Unbound). **No numbers retrieved** — paywalled (doi:10.1007/s10822-026-00831-4) [VERIFIED-ABSTRACT] |

**Two regimes, and they must not be conflated.** When the hit criterion is held fixed, cross-benchmark
gaps in this field run **3 to 11 points**, or about **0.11 AUC** in the one AUC-to-AUC case
available. When the criterion is changed and homologues of the training set are removed, published
80–85 % figures become 13–18 %. The second number is not "the true generalisation gap"; it is the
sum of a generalisation gap and a criterion change, and no retrieved paper separates them.

**Cross-family generalisation was not measured in the retrieved corpus.** The nearest thing is the
kinase PLM's 30 % sequence-identity filter between LIGYSIS training sequences and the KinCoRe test
set, which is a within-family, sequence-controlled split rather than a cross-family transfer
(doi:10.1021/acs.jctc.6c00427) [VERIFIED-FULLTEXT]. GrASP reports "very small variance with respect
to sequence identity for all bins with sufficient data (above 20 % identity)"
(doi:10.1021/acs.jcim.3c01698) [VERIFIED-FULLTEXT], which is a claim of no gap rather than a
measurement of one.

---

## Q5 — How much of the reported variance is benchmark composition?

A large fraction, and at least three distinct mechanisms are documented.

**1. Re-curating a named benchmark moves a fixed method by more than most method improvements.**
P2Rank on HOLO4K: **68.6 %** DCA Top-n under the 2018 curation
(doi:10.1186/s13321-018-0285-8), **81.2 %** under "HOLO4K(Mlig+)", where GrASP's authors modified
the P2Rank test sets "to ensure ligands were both bound and biologically or pharmacologically
relevant" (doi:10.1021/acs.jcim.3c01698). Same tool, same benchmark name, **12.6 points**. On
COACH420 the same re-curation moves P2Rank from 72.0 % to 74.9 %, **2.9 points**, in the opposite
direction relative to its own size. [both VERIFIED-FULLTEXT]

**2. One method, two allosteric benchmarks: 12.9 points.** Bond-to-bond propensity detects the
allosteric site in **99 of 118 (83.9 %)** ASBench structures and **304 of 314 (96.8 %)** CASBench
structures — and the two runs also differ in the perturbation source, which the authors identify as
load-bearing: "the allosteric site of a protein structure can be identified with more statistical
measures when choosing the orthosteric ligand as the perturbation source"
(doi:10.1016/j.patter.2021.100408) [VERIFIED-FULLTEXT]. The comparison is therefore
benchmark **and** protocol, not benchmark alone — which is itself the point. The same authors write
that the "definition of orthosteric and allosteric residues … plays an essential part when
evaluating allosteric site prediction methods."

**3. Benchmark construction can leak, and the leak inflates everyone.** A 2026 preprint reports "a
systematic bias in current benchmarking practices, showing that applying fpocket to holo structures
without removing bound allosteric modulators introduces data leakage and leads to artificially
inflated performance estimates" (doi:10.64898/2026.05.22.727284) [VERIFIED-ABSTRACT]. This is the
same failure mode our C1 forbids, found independently in the benchmark-construction step rather than
in the prediction step.

**4. Benchmark sizes differ by an order of magnitude, and small ones cannot resolve variance.**
Apo structures per cryptic-site benchmark: **PocketMiner 38, CryptoSite 93, CryptoBench 1107**
(doi:10.1093/bioinformatics/btae745) [VERIFIED-FULLTEXT]; CryptoBank claims ~5151 unique cryptic
sites across 3643 protein clusters (doi:10.1126/sciadv.ady6364) [VERIFIED-FULLTEXT]. On the
allosteric side: Ohm 20, AlloPred 40 test, CASBench 33 proteins / 314 structures, ASD 207 proteins,
APOP 104, STINGAllo 91 chains, AlloBench 418 unique UniProt chains. **Our four development arms are
small even by this field's standards, and the field's own 14-to-40-protein sets are themselves too
small to estimate a between-target variance.**

**5. Has anyone re-run one method across two benchmarks and reported both?** Yes, four times in the
retrieved corpus: PASSerRank (ASD, CASBench), P2Rank and every tool in its table (COACH420, HOLO4K),
GrASP (sc-PDB CV, COACH420 Mlig+, HOLO4K Mlig+), and CryptoBench's re-run of pre-trained PocketMiner
and P2Rank. **None of the four reports a per-target breakdown alongside the per-benchmark numbers**,
so in no case can the between-benchmark gap be decomposed into "different targets" and "different
labelling". PASSer's own web-server paper states the constraint plainly: "performance is not
directly comparable across models due to differences in the training and test datasets used"
(doi:10.1093/nar/gkad303) [VERIFIED-FULLTEXT].

---

## 6. Calibration verdict

The question is whether **0.175 (classical)** and **0.361 (quantum)** between-target spread in mean
AUC-ROC over four proteins is typical, good or bad. The literature alone cannot answer it, for the
reason in §2: nobody publishes a between-target AUC standard deviation for this task. So the answer
has to come from a null, and the null is computable from numbers already in the repo.

**Step 1 — what spread does estimator noise alone produce on our four arms?** The arm sizes are in
`../exploration/results/40-method-sweep.md` §1: `mkp5` 11 positives of 136 candidates, `ptp1b` 11 of
287, `hiv_rt` 16 of 534, `ns5b` 16 of 550. The Hanley–McNeil standard error of an AUC estimate
(doi:10.1148/radiology.143.1.7063747) is

```
SE(A)² = [ A(1−A) + (n₁−1)(Q₁ − A²) + (n₂−1)(Q₂ − A²) ] / (n₁ n₂)
Q₁ = A/(2−A),   Q₂ = 2A²/(1+A)
```

At A = 0.70 this gives SE = 0.091 (`mkp5`), 0.090 (`ptp1b`), 0.074 (`hiv_rt`), 0.074 (`ns5b`); mean
**0.082**. At A = 0.55 the mean is 0.084, so the value is insensitive to where on the scale we
evaluate it. [UNVERIFIED — this is our arithmetic from a published formula, not a literature claim.]

**Step 2 — convert a standard error into an expected range.** For four independent draws from a
normal distribution with standard deviation σ, the expected range is d₂σ with d₂ = 2.059. So under a
null of **no target effect at all** — one true AUC, four noisy estimates of it — the expected
observed spread across our four arms is

```
2.059 × 0.082 ≈ 0.169
```

**Step 3 — read our numbers against that.**

| Family            | Observed between-arm spread | Expected under no-target-effect null | Ratio    |
| ----------------- | --------------------------- | ------------------------------------ | -------- |
| Classical scorers | **0.175**                   | 0.169                                | **1.04** |
| Quantum scorers   | **0.361**                   | 0.169                                | **2.14** |

**Verdict, classical: 0.175 is typical, and it is weaker evidence of a target effect than it looks.**
It is within 4 % of what four AUC estimates at our positive counts would scatter by if every arm had
exactly the same true AUC. It is also far smaller than every per-target spread the field reports
where per-target numbers exist (§2), smaller than the 0.299 AUROC spread one model shows between
site classes in a single protein family, and comparable to the single clean cross-benchmark AUC
delta in the literature (PocketMiner, −0.11). **Nothing is pathological about it.**

**Verdict, quantum: 0.361 is large — about 2.1× the noise floor — but it is not off-scale for this
field, and it is not evidence of a signal.** It exceeds the largest single-model spread retrieved
(0.299 AUROC between binding-site classes on kinases) but sits well inside the per-target MCC range
CASP reports. The direction matters more than the magnitude. `40-method-sweep.md` §6 already records
the mechanism: `ctqw_infinite_time_average` on `cb_10` reaches AUC 0.824 on `hiv_rt` and 0.377 on
`ns5b`, and the quantum family's whole-distribution median is **0.455**, below chance. A score with a
below-chance median and a large arm-to-arm swing is behaving like an uninformative score whose sign
flips with the geometry, not like a target-specific detector. **Large spread with a low mean is the
signature of noise, and the literature offers no counter-example in which large between-target
variance was later shown to be a genuine per-target competence.**

**What the literature genuinely cannot answer, stated plainly.** No retrieved paper reports a
between-target standard deviation of AUC for allosteric-, cryptic- or binding-site prediction. No
retrieved paper reports the same method's per-target AUC on two benchmarks. So "is 0.361 normal for a
quantum walk on a residue graph" has no published comparator and will not acquire one from this
literature. The comparator that exists is ours to compute, and §"What this changes" names it.

---

## What the literature does NOT support

- **It does not support a published between-target standard deviation for this task.** The recorded
  search found none for AUC, AUPRC or top-N in allosteric- or cryptic-site prediction. Not
  retrieved is not non-existent.
- **It does not support comparing our mean AUC to a published mean AUC.** Beyond the usual dataset
  and positive-class mismatch, the estimators differ in kind: PocketMiner and STINGAllo pool residues
  across proteins, our harness macro-averages per arm. Only the kinase PLM study
  (doi:10.1021/acs.jctc.6c00427) reports both.
- **It does not support any validated difficulty descriptor.** Nine descriptors were retrieved and
  every one is post-hoc. None was fitted on one target set and tested on another.
- **It does not support the inference "large between-target spread ⇒ broken method".** CASP9 reports
  the same spread for the best groups in the field and attributes it to the targets or to chance
  (doi:10.1002/prot.23174).
- **It does not support the inference "small between-target spread ⇒ generalisation".** At our arm
  sizes a spread of 0.17 is what pure estimator noise delivers, so a small spread carries almost no
  information about the target effect.
- **It does not support treating a benchmark name as a fixed quantity.** HOLO4K under two curations
  moved a fixed method by 12.6 points (doi:10.1186/s13321-018-0285-8 versus
  doi:10.1021/acs.jcim.3c01698).
- **It does not support a claim about cross-family transfer in this task.** No cross-family transfer
  experiment was retrieved for allosteric- or cryptic-site prediction.
- **It does not support quoting AlloBench's 13–18 % as "the generalisation gap".** That number
  changes the hit criterion at the same time as it removes homologues, and no retrieved source
  separates the two.

---

## What this changes for our pipeline

1. **Stage S8 / reporting (`allo.scoring`).** Keep the per-arm table as the primary presentation and
   the mean as secondary, and say in `docs/report/` why. The field's modal estimator — residues
   pooled across proteins — would have concealed the entire result in
   `../exploration/results/40-method-sweep.md` §4, where a mean of 0.810 is built from 0.944 and
   0.703. This is a defensible methodological choice with a citation behind it
   (doi:10.1021/acs.jctc.6c00427 is the only retrieved paper that does the same).

2. **Compute the between-arm spread of the null, not just of the method.** §6 uses an analytic
   Hanley–McNeil noise floor because it is cheap. The repo already owns a better one: the
   matched-patch null inside `allo.scoring.score_arm`. Running the existing null draws and recording
   the **distribution of the max-min AUC spread across the four arms** gives a calibrated,
   benchmark-specific answer to "is 0.361 anomalous". It costs one pass over draws that are already
   generated, and it is the only route to an answer the literature cannot supply. Add it as a
   reported statistic before the `generalisation` tier opens.

3. **Add worst-arm AUC as a pre-registered secondary endpoint.** `40-method-sweep.md` already prints
   `min AUC`; promote it. Under a mean-only endpoint a method that wins on two arms and loses on two
   is indistinguishable from one that is uniformly mediocre, and §2 of that file already states that
   the first case is what we have. CASP9's finding — target effects rivalling method effects — is the
   external argument for why a worst-case endpoint is the honest one.

4. **Blocks any "our method generalises" claim from four arms.** With a per-arm SE near 0.082, the
   standard error of a four-arm mean is about 0.041, and the 95 % interval on a mean AUC is roughly
   ±0.08. Two methods whose four-arm means differ by less than 0.08 are not separated. This is an
   independent route to the same conclusion as
   `../exploration/results/41-selection-and-power.md` and `09a-power-verification.md`, and it
   strengthens rather than replaces them.

5. **Fixes the comparator set for `docs/report/`.** The admissible external comparators are
   same-method-two-benchmark deltas (PocketMiner −0.11 AUC; PASSerRank −3.2 points top-1; P2Rank
   −3.4 points; DeepSite −10.8 points), not headline numbers. Any table in the report that puts our
   AUC next to a published AUC must carry the estimator, the positive class, the candidate pool and
   the criterion in the same row, per `00-conventions.md` §2.

6. **Does not change stage S1, S5 or S6.** Nothing here bears on graph construction, on the choice
   of observable, or on detrending. Those are `13`, `03`/`16` and `14` respectively.

---

## Method

**Retrieved 2026-08-27.**

**Databases and routes.** Europe PMC REST search (`/europepmc/webservices/rest/search`, `resultType`
`lite` and `core`) — **working this session**, contrary to the outage recorded in
`14-distance-confound.md`; PMC article pages (`pmc.ncbi.nlm.nih.gov/articles/{PMCID}/`); the PMC ID
converter (`pmc.ncbi.nlm.nih.gov/tools/idconv/api/v1/articles/`); Crossref REST
(`api.crossref.org/works/{DOI}` and `?query.bibliographic=`); arXiv API
(`export.arxiv.org/api/query`); general web search (four queries only — the tool then reported the
session's web-search budget exhausted, and **all** subsequent retrieval went through the REST routes
above).

**Europe PMC `fullTextXML` returned HTTP 404 for every PMCID attempted** (PMC4794384, PMC4495912).
The PMC article page returned full text for the same IDs. Record `fullTextXML` as down for this
route and the article page as the working substitute, which is what `00-conventions.md` §3 already
advises.

**Publisher pages that could not be reached.** `nature.com` and `link.springer.com` both returned
303 redirects to an identity provider for the PocketMiner and P2Rank articles; both were recovered
from PMC. `biorxiv.org` returned HTTP 403 for the AlloDyn preprint full text; its abstract was
recovered from the Europe PMC `core` record. The CAPASP paper
(doi:10.1007/s10822-026-00831-4) has no PMC deposit and is paywalled — **abstract only, no numbers**.

**Queries run, in order.** `CASP assessment of ligand binding site predictions per-target MCC easy
hard targets Gallo Cassarino Schwede`; `CryptoSite Cimermancic 2016 cryptic binding site prediction
AUC per-target performance variability`; `PocketMiner Meller 2023 cryptic pocket AUC 0.87 comparison
CryptoSite held-out test set per-protein`; `PASSer allosteric site prediction top-1 top-3 accuracy
ASBench ASD test set per-protein results` (web search, four calls, budget exhausted). Then via
Europe PMC: `"allosteric site prediction" AND benchmark`; `("binding site prediction" OR "pocket
prediction") AND ("sequence identity" AND (generalisation OR generalization OR leakage))`;
`"per-target" AND "AUC" AND ("variance" OR "variability") AND (protein OR docking OR "virtual
screening")`; `("allosteric site" OR "cryptic site" OR "cryptic pocket") AND ("apo" AND "holo") AND
("performance drop" OR degrade OR degradation OR decrease)`; `("binding site prediction" OR "pocket
detection") AND "target difficulty"`; `("per-protein AUC" OR "per-target AUC" OR "per-structure
AUC") AND (pocket OR "binding site" OR allosteric)`; `"allosteric site prediction" AND ("independent
dataset" OR "systematic evaluation" OR "comparative assessment")`;
`TITLE:"Benchmark Bias and Conformational Dynamics in Allosteric Site Prediction"`;
`TITLE:"Exploiting protein flexibility to predict the location of allosteric sites"`;
`DOI:"10.1007/s10822-026-00831-4"`; `DOI:"10.1093/bioinformatics/btad275"`. Crossref DOI-direct for
`10.1148/radiology.143.1.7063747`, `10.1016/j.jmb.2016.01.029`, `10.1007/s10822-026-00831-4`.

**Counts.** Approximately 165 bibliographic records surfaced across the searches; 26 screened in as
potentially carrying per-target, cross-benchmark or difficulty evidence; **17 full texts retrieved**
and read this session; 6 further records used at abstract or metadata level only. Two searches
returned nothing on task and are recorded as negatives in §2 and §Q4.

**Stopping rule.** Stop when three independently retrieved sources agree that per-target reporting is
absent from the modal method paper, and when at least four distinct same-method-two-benchmark
comparisons have been located with numbers on both sides. Both conditions were met; the search was
stopped at that point rather than extended to method papers unlikely to change either conclusion.

**Not reached, and named so a later pass can close it.** AlloSite / AlloSitePro (Huang et al. 2013;
Song et al. 2017) — not retrieved this session, so the only number for it here is AlloPred's re-run.
CAPASP's per-tool, per-dataset numbers — paywalled. AlloBench Supporting Information Table S3, which
is the one per-protein table located but not opened, and which would supply the field's only
large-N per-target distribution for allosteric-site prediction. CASP8's assessment
(doi:10.1002/prot.22557) — the retrieved article for that PMCID was the CASP9 paper. The CASP11–15
binding-site assessments, if the category persisted.

**Leakage guard.** No file under `docs/benchmark/evaluation/`, no `frozen.json`, no `manifest.yaml`,
no `selection.json` and no `extension-candidates.md` was opened. No `generalisation`-tier arm was
looked up in this repository or in the literature. The only repository numbers quoted are arm sizes
and family-level AUC statistics already published in
`../exploration/results/40-method-sweep.md`.

---

## References

Ordered by first appearance.

1. Gallo Cassarino T, Bordoli L, Schwede T. **Assessment of ligand binding site predictions in
   CASP10.** _Proteins_ 2014;82(S2):154–163. doi:10.1002/prot.24495. PMC4495912. [VERIFIED-FULLTEXT]
2. Schmidt T, Haas J, Gallo Cassarino T, Schwede T. **Assessment of ligand-binding residue
   predictions in CASP9.** _Proteins_ 2011. doi:10.1002/prot.23174. PMC5628505. [VERIFIED-FULLTEXT]
3. Cimermancic P, Weinkam P, Rettenmaier TJ, Bichmann L, Keedy DA, Woldeyes RA, Schneidman-Duhovny D,
   Demerdash ON, Mitchell JC, Wells JA, Fraser JS, Sali A. **CryptoSite: Expanding the Druggable
   Proteome by Characterization and Prediction of Cryptic Binding Sites.** _J Mol Biol_
   2016;428:709–719. doi:10.1016/j.jmb.2016.01.029. PMC4794384. [VERIFIED-FULLTEXT]
4. Meller A, Ward M, Borowsky J, Kshirsagar M, Lotthammer JM, Oviedo F, Ferres JL, Bowman GR.
   **Predicting locations of cryptic pockets from single protein structures using the PocketMiner
   graph neural network.** _Nat Commun_ 2023;14:1177. doi:10.1038/s41467-023-36699-3. PMC9977097.
   [VERIFIED-FULLTEXT]
5. Škrhák V, et al. **CryptoBench: cryptic protein–ligand binding sites dataset and benchmark.**
   _Bioinformatics_ 2025;41(1):btae745. doi:10.1093/bioinformatics/btae745. PMC11725321.
   [VERIFIED-FULLTEXT]
6. Tian H, Xiao S, Jiang X, Tao P. **PASSerRank: Prediction of allosteric sites with learning to
   rank.** _J Comput Chem_ 2023. doi:10.1002/jcc.27193. PMC9915737. [VERIFIED-FULLTEXT]
7. Tian H, Xiao S, Jiang X, Tao P. **PASSer: fast and accurate prediction of protein allosteric
   sites.** _Nucleic Acids Res_ 2023;51(W1):W427. doi:10.1093/nar/gkad303. PMC10320119.
   [VERIFIED-FULLTEXT]
8. Maity D, Qiao B. **AlloBench: A Data Set Pipeline for the Development and Benchmarking of
   Allosteric Site Prediction Tools.** _ACS Omega_ 2025. doi:10.1021/acsomega.5c01263. PMC12059942.
   [VERIFIED-FULLTEXT]
9. Greener JG, Sternberg MJE. **AlloPred: prediction of allosteric pockets on proteins using normal
   mode perturbation analysis.** _BMC Bioinformatics_ 2015;16:335. doi:10.1186/s12859-015-0771-1.
   PMC4619270. [VERIFIED-FULLTEXT]
10. Wang J, Jain A, McDonald LR, Gambogi C, Lee AL, Dokholyan NV. **Mapping allosteric communications
    within individual proteins.** _Nat Commun_ 2020;11:3862. doi:10.1038/s41467-020-17618-2.
    PMC7395124. [VERIFIED-FULLTEXT]
11. Krivák R, Hoksza D. **P2Rank: machine learning based tool for rapid and accurate prediction of
    ligand binding sites from protein structure.** _J Cheminform_ 2018;10:39.
    doi:10.1186/s13321-018-0285-8. PMC6091426. [VERIFIED-FULLTEXT]
12. Smith Z, et al. **Graph Attention Site Prediction (GrASP): Identifying
    Druggable Binding Sites Using Graph Neural Networks.** _J Chem Inf Model_ 2024.
    doi:10.1021/acs.jcim.3c01698. PMC11182664. [VERIFIED-FULLTEXT]
13. Wu N, Strömich L, Yaliraki SN. **Prediction of allosteric sites and signaling: Insights from
    benchmarking datasets.** _Patterns_ 2022;3(1):100408. doi:10.1016/j.patter.2021.100408.
    PMC8767309. [VERIFIED-FULLTEXT]
14. Riedlová K, Škrhák V, Gatlin WG, Ludwick M, Turano L, Novotný M, Hoksza D, Verkhivker GM.
    **Predicting and Decoding Allosteric Binding Sites Using Protein Language Models and
    Structure-Based Machine Learning: An Energy Landscape-Guided Explainable AI Framework.**
    _J Chem Theory Comput_ 2026. doi:10.1021/acs.jctc.6c00427. PMC13217555. [VERIFIED-FULLTEXT]
15. Omage FB, Salim JA, Mazoni I, Yano IH, Hernández González JE, Giachetto PF, Tasic L, Arni RK,
    Neshich G. **STINGAllo: a web server for high-throughput prediction of allosteric site-forming
    residues using internal protein nanoenvironment descriptors.** _Brief Bioinform_ 2025.
    doi:10.1093/bib/bbaf424. PMC12368853. [VERIFIED-FULLTEXT]
16. Panjkovich A, Daura X. **Exploiting protein flexibility to predict the location of allosteric
    sites.** _BMC Bioinformatics_ 2012;13:273. doi:10.1186/1471-2105-13-273. PMC3562710.
    [VERIFIED-ABSTRACT]
17. Kumar A, Kaynak BT, Dorman KS, Doruker P, Jernigan RL. **Predicting allosteric pockets in protein
    biological assemblages** (APOP). _Bioinformatics_ 2023. doi:10.1093/bioinformatics/btad275.
    PMC10185404. [VERIFIED-ABSTRACT] — the matched-apo subset figure of 11/15 top-3 is recorded in
    `00-conventions.md` §6 and was **not** re-retrieved this session.
18. Ai Y, Li H, Huang X, Liu S. **A systematic evaluation of protein allosteric site prediction tools
    with independent datasets** (CAPASP). _J Comput Aided Mol Des_ 2026.
    doi:10.1007/s10822-026-00831-4. PMID 42126486. [VERIFIED-ABSTRACT] — paywalled, no numbers.
19. Pryakhin V, Smail-Tabbone M, Karami Y. **Benchmark Bias and Conformational Dynamics in Allosteric
    Site Prediction** (AlloDyn). _bioRxiv_ 2026. doi:10.64898/2026.05.22.727284. PPR1240387.
    [VERIFIED-ABSTRACT]
20. Febrer Martinez P, Fröhlking T, Borsatto A, Gervasio FL. **CryptoBank: A resource for the
    identification and prediction of cryptic sites in proteins.** _Sci Adv_ 2026.
    doi:10.1126/sciadv.ady6364. PMC13267282. [VERIFIED-FULLTEXT]
21. Zlobin A, Suplatov D, Kopylov K, Švedas V. **CASBench: A Benchmarking Set of Proteins with
    Annotated Catalytic and Allosteric Sites in Their Structures.** _Acta Naturae_ 2019;11(1):74–80.
    doi:10.32607/20758251-2019-11-1-74-80. PMC6475866. [VERIFIED-ABSTRACT — metadata only]
22. Hanley JA, McNeil BJ. **The meaning and use of the area under a receiver operating characteristic
    (ROC) curve.** _Radiology_ 1982;143(1):29–36. doi:10.1148/radiology.143.1.7063747.
    [VERIFIED-ABSTRACT — bibliographic record confirmed via Crossref; the variance formula used in §6
    is the standard published form and was **not** re-read from the paper this session.]
23. Bouthillier X, Delaunay P, Bronzi M, Trofimov A, Nichyporuk B, Szeto J, Sepah N, Raff E, Madan K,
    Voleti V, Ebrahimi Kahou S, Michalski V, Serdyuk D, Arbel T, Pal C, Varoquaux G, Vincent P.
    **Accounting for Variance in Machine Learning Benchmarks.** arXiv:2103.03098.
    [VERIFIED-ABSTRACT] — cited only for the general principle that a benchmark score carries
    variance from sources the headline number hides.
24. Bioinformatics Advances review of cryptic-site methods, 2025;5(1):vbaf156.
    doi:10.1093/bioadv/vbaf156. [VERIFIED-FULLTEXT] — cited for "Across different cases, CryptoSite's
    accuracy varied depending on the protein system", and for the absence of any unified
    cross-method benchmark in that literature.
