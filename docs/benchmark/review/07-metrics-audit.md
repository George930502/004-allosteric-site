# Independent re-audit of the frozen metrics and workflow

> **SUPERSEDED — 2026-09-02.** [`17-definition-and-metrics-standard.md`](17-definition-and-metrics-standard.md) is the second, independent pass at the metrics question, and [`21-protocol-v3-statistics.md`](21-protocol-v3-statistics.md) audits the protocol version that replaced the version 2 audited here. This document stays unedited as the record of this pass.

> **SUBJECT PARTLY DELETED — 2026-09-02.** This document cites files in the method layer:
> `src/allo/{network,classical,quantum}`, `docs/method/exploration/`, `tests/test_method.py`,
> or an experiment directory dated 2026-08-26 or 2026-08-27. All of those left `main` on
> 2026-09-02 (ADR 0037) and are preserved whole on the branch `method-layer-archive`.
> Findings whose subject is one of those files are **not re-runnable on `main`**. They stay
> here unedited, because a record of what an audit found is worth keeping even when the
> subject is gone. To re-run one, check out that branch. Two things moved rather than left:
> `allo.network.graph` is now `allo.structure.graph`, and the required baselines are now
> `allo.scoring.baselines` -- eight of the nine, with `cavity_volume` in `allo.scoring.decoys`.

**Date: 2026-09-02. Scope: `docs/benchmark/evaluation/` protocol version 2, its manifest, its
evidence base, and `src/allo/scoring/harness.py`. Adversarial, independent, search-first.**

Provenance tags used below:

| Tag                 | Meaning                                                                                                     |
| ------------------- | ----------------------------------------------------------------------------------------------------------- |
| `[FT]`              | I fetched the source or the publisher/Crossref record **in this session** and read it.                      |
| `[repo]`            | The claim is carried by `../evidence/evaluation-metrics.md` at the tag recorded there. I did not re-verify. |
| `[CODE]`            | Verified by reading a committed file in this repository this session.                                       |
| `[NOT ESTABLISHED]` | I searched and found no source. Not "false" — unmeasured.                                                   |

Arithmetic derived here is marked **[derived]** and shows its formula so it can be checked.

---

## Headline verdict

**The metric layer is sound and, on statistics, well ahead of this field. It has one
challenge-compliance hole, one internal inconsistency about what the claim actually is, one
frozen file that still carries three rationales its own audit withdrew, and one forward-looking
recommendation that the 2025 literature refutes. None of these is a reason to rebuild. All four
are cheap to fix, and three of them must be fixed before any method is scored.**

Specifically:

1. **Negative class (b) — half of the sponsor's dominant criterion — has no usable significance
   test.** `[CODE]` The only decoy p-value is a permutation over `n_decoys` pocket means, which
   floors at 0.25 on both KRAS arms and 0.10 on `bcr_abl1_corrected`. The residue-level
   `auc_roc_vs_decoy_linings` is computed and reported with **no null and no p at all**. The
   challenge asks for statistical significance against non-functional surface pockets. As
   frozen, the protocol cannot deliver it on two of three confirmatory arms. This is the most
   serious finding.
2. **The claim threshold and the confirmatory family disagree.** ADR 0025 and README §13 make
   "beat `cavity_volume`" the claim. README §8 and `manifest.yaml` make everything except the
   three matched-patch tests descriptive and FWER-unprotected. The load-bearing comparison is
   therefore the one with no multiplicity control, across nine required baselines and an
   unbounded number of methods. `[CODE]`
3. **`manifest.yaml` still carries the pre-audit omission rationales.** `AUDIT.md` §4 corrected
   the MCC/F1, Jaccard and DVO reasons; `README.md` was updated and the manifest was not. The
   manifest's DVO clause is the one the audit withdrew as **false**, and its Jaccard ceiling
   (0.31) is the number the audit corrected (0.4545). `[CODE]`
4. **README §12.4 recommends the wrong repair.** It names variogram-matched surrogates (Burt et
   al. 2020) as "the right design" and "the first thing to try if the calibration ever has to
   move". The most recent head-to-head measurement puts that method at **29.2 % and 36.3 %
   false-positive rate** at high spatial autocorrelation — worse than the spin test — while
   eigenmode-rotation surrogates hold 5.2–5.3 % (doi:10.1162/IMAG.a.71) `[FT]`.

Two further gaps that are additions rather than corrections: nothing measures whether the top-5
is **spatially contiguous**, and nothing computes F1, MCC or IoU on the **assembled site**, which
is where the field's own numbers live.

The currency risk is small. The evidence base was compiled eight days before this audit. What
changed is not the calendar; it is that four 2025–2026 sources bear directly on choices the
protocol froze, and three of them were not in the evidence base.

---

## 1. Currency check

The evidence base is dated 2026-08-25. This audit is 2026-09-02. Calendar drift is not the risk.
The risk is 2025–2026 material that existed at compile time and was missed, plus items recorded
as paywalled. I found seven items that change something and three that close an open flag.

### 1.1 New, and it changes a frozen recommendation

**Eigenstrapping — geometric-eigenmode surrogate maps.** Koussis NC, Pang JC, Phogat R,
Jeganathan J, Paton B, Fornito A, Robinson PA, Misic B, Breakspear M. _Imaging Neuroscience_
3, 2025, doi:10.1162/IMAG.a.71 `[FT]`. Measured false-positive rates against a nominal 5 %:

| Null                                | FPR at low autocorrelation | FPR at high autocorrelation |
| ----------------------------------- | -------------------------: | --------------------------: |
| Eigenstrapping                      |                      5.3 % |                       5.2 % |
| Spin test                           |                          — |                      12.3 % |
| BrainSMASH (variogram, Burt et al.) |           29.2 % (α = 2.0) |            36.3 % (α = 3.0) |

Verbatim from the paper: eigenstrapping "eschews the need for parametric assumptions about the
nature of a map's SA" and has "only one free parameter (the number of modes used for
decomposition)" `[FT]`.

This matters for three reasons.

- README §12.4 names variogram-matched surrogates as the design the protocol should have used and
  the first repair to try. On this measurement that method is the **worst** of the three tested.
  The rebuttal as written would hand a reviewer the weapon.
- The property README §6.2 says is unobtainable — a null that needs no λ in advance — is exactly
  what eigenstrapping provides, and it provides it without the parametric variogram fit that
  BrainSMASH needs.
- The construction transfers in principle: rotate within the eigenspaces of the contact-graph
  Laplacian, which `allo.network` already builds. **Whether eigenstrapping transfers to a residue
  contact graph has not been demonstrated by anyone. [NOT ESTABLISHED]** It is defined on smooth
  2-manifolds using Laplace–Beltrami eigenmodes; the graph-Laplacian analogue is obvious but
  unpublished for proteins.

**The spin test's own failure mode, and a transferable remedy.** Bazinet V, Liu Z-Q, Misic B,
"The effect of spherical projection on spin tests for brain maps", _Imaging Neuroscience_ 3,
2025, doi:10.1162/imag.a.118 `[FT]`. Spherical projection "distorts distance relationships
between vertices", producing surrogates that imperfectly preserve autocorrelation and inflated
FPR; the proposed remedy is **removing individual spins exhibiting high distortion**. That is a
screen-and-discard post-stratification of the surrogate pool. `AUDIT.md` M14 proposed
post-stratification, the repo tested _re-centring_ the acceptance window (repair C), it failed,
and the idea was dropped. Screen-and-discard is a different operation from re-centring and has
not been tried here. `[CODE]`

### 1.2 New, and it names a metric the protocol does not have

**Seq2Pocket.** Škrhák V, Polák L, Novotný M, Hoksza D. bioRxiv 2026,
doi:10.64898/2026.01.28.702257 `[FT]`. Introduces the **Pocket Fragmentation Index (PFI)**, which
"measures the average number of predicted clusters assigned to each ground-truth pocket", where
"an ideal clustering strategy achieves a one-to-one mapping, resulting in a PFI of 1.0". The
paper's motivating claim, verbatim: protein language models produce "incomplete pockets:
residue-wise predictions that often achieve high statistical scores but fail to form continuous
binding regions", and "while residue-level metrics might look promising... the pocket-level
metrics could be disappointing" `[FT]`.

The repo predicts a top-5 residue list and measures no contiguity property of it. A top 5 spread
over five unrelated surface patches is not a druggable site, is not what CHALLENGE §4.2 calls an
"actionable output", and would score identically to a compact five-residue patch on every frozen
endpoint except DCC. DCC is a centroid distance, and a centroid can sit in the middle of five
scattered residues.

Seq2Pocket also uses **DCC at 12 Å**, adopting Utgés & Barton's recommendation
(doi:10.1186/s13321-024-00923-z) rather than the 4 Å convention `[FT]`. That is a second
independent group choosing 12 Å over 4 Å, which strengthens the repo's decision to freeze the
continuous distance and print both conventions.

### 1.3 New, and it reopens the Jaccard question

**UniSite.** NeurIPS 2025 spotlight, arXiv:2506.03237, doi:10.48550/arXiv.2506.03237 `[FT]`.
Verbatim criticisms of the metrics the repo reports:

> "approximately 20% of proteins are subject to double-counting during evaluation"
>
> "the measured mean ground truth DCC (2.15 Å, 92.65% < 4 Å) and DCA (1.57 Å, 98.88% < 4 Å)
> exhibit a significant deviation from the ideal value of 0"
>
> "They completely disregard the structural properties such as shape, size, and residue
> composition of binding sites"

Its replacement is **residue-mask Average Precision at an IoU threshold**:
`IoU(m_A, m_B) = sum(m_A & m_B) / sum(m_A | m_B)`, with one-to-one matching and AP reported at
IoU 0.3 and 0.5 `[FT]`. Residue-mask IoU is Jaccard. A NeurIPS spotlight is promoting the metric
the repo dropped. The repo's reason survives (see §3), but only because the repo predicts a fixed
five and UniSite predicts variable-size sets.

### 1.4 CAPASP is now readable at the abstract, and CASP has dropped the category

**CAPASP.** Ai Y, Li H, Huang X, Liu S. _J Comput Aided Mol Des_ 40(1):122, 2026,
doi:10.1007/s10822-026-00831-4 `[FT]`, abstract retrieved verbatim via Europe PMC. It evaluates
five tools on two purpose-built independent sets, "a CAPASP-General subset comprising holo state
allosteric proteins and a CAPASP-Unbound subset comprising apo state allosteric proteins", across
"five dimensions: sensitivity, specificity, F1-score, MCC value and ranking capability". PASSer
and APOP lead. "However, these models performed better with the CAPASP-General subset than with
the CAPASP-Unbound subset". **Per-tool numbers and dataset sizes remain behind the Springer
paywall. [NOT ESTABLISHED]** The repo's §9.2 item 9 stays open, but the citation is now complete.

**CASP16 (2024) has no function-prediction category.** The category list retrieved from
predictioncenter.org this session is: Single Proteins and Domains; Protein Complexes; Accuracy
Estimation; Nucleic acid structures and complexes; Protein–organic ligand complexes;
Macromolecular conformational ensembles; Integrative modeling `[FT]`. There is no FN category and
no ligand-binding-residue category. The last community blind assessment of binding-site residues
is CASP10, doi:10.1002/prot.24495 `[repo]`. The CASP16 ligand category assesses **poses and
affinities**, scored by LDDT-PLI and Kendall's τ, doi:10.1002/prot.70061 `[FT]` — a different
task. Consequence: CAPASP 2026 is now the field's only current independent assessment, which
raises the cost of not reporting its five dimensions.

### 1.5 New tools since the compile

| Tool                                    | Citation                                                                                                                                                                     | What it adds                                                                                                                                                                                                                                                                                                         |
| --------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **AlloEF**                              | Zhang J, Sun X, Wu Z, Su J, Zhang X, Li C. _J Phys Chem B_ 130(19):4970–4981, 2026, doi:10.1021/acs.jpcb.6c00242 `[FT]`                                                      | Soft-voting ensemble on transfer entropy plus energetic frustration. F1 0.630, MCC 0.609 on an independent test set (search-summary figures, **not** read at full text — treat as `[UNVERIFIED]`). Note for C2: whether its transfer entropy comes from MD or from an elastic network is **[NOT ESTABLISHED]** here. |
| **Kinase pLM framework, now published** | Riedlová K, Škrhák V, Gatlin WG, Ludwick M, Turano L, Novotný M, Hoksza D, Verkhivker GM. _J Chem Theory Comput_ 22(10):5326–5347, 2026, doi:10.1021/acs.jctc.6c00427 `[FT]` | Full text of the preprint gives, for the allosteric ("ALLO") class: **AUROC 0.705, AUPR 0.061, prevalence 2.96 % (8,140 positives / 267,118 negatives)**, with negatives defined as "residues not satisfying the 4 Å distance criterion" and **no statistical test, confidence interval or null** `[FT]`.            |
| **LIGYSIS-web**                         | _Nucleic Acids Res_ 53(W1):W351, 2025, doi:10.1093/nar/gkaf411 `[FT]`                                                                                                        | 65,000 binding sites over 25,000 proteins. Not in the repo bibliography.                                                                                                                                                                                                                                             |
| **Seq2Pocket, UniSite**                 | above                                                                                                                                                                        | above                                                                                                                                                                                                                                                                                                                |

**The repo's kinase-pLM row is wrong.** `evaluation-metrics.md` §5.3 carries "0.676 / 0.077 /
3.22 % (15,185 pos / 456,117 neg)" tagged `[UNVERIFIED]` `[repo]`. Full-text retrieval this
session gives 0.705 / 0.061 / 2.96 % (8,140 / 267,118) `[FT]`. I cannot reconcile the two — they
may be different table rows or different inhibitor classes. Replace with the retrieved values and
the published DOI, or mark the discrepancy.

### 1.6 Flags this audit closes

- **RBO has a DOI.** Webber W, Moffat A, Zobel J, _ACM TOIS_ 28(4):20, 2010,
  doi:10.1145/1852102.1852106 `[FT]`. The evidence file records it as "DOI unverified".
- **Burt et al. 2020 has a verified DOI.** doi:10.1016/j.neuroimage.2020.117038, Crossref record
  retrieved `[FT]`. The evidence file records it as "DOI unverified"; the README already uses it.
- **DOME has a verified DOI.** Walsh I, Fishman D, Garcia-Gasulla D, Titma T, Pollastri G, ELIXIR
  ML Focus Group. _Nat Methods_ 18:1122–1127, 2021, doi:10.1038/s41592-021-01205-4 `[FT]`. The
  evidence file tags it `[UNVERIFIED]`.

### 1.7 What did _not_ change

- **No new AUROC/AUPRC critique supersedes McDermott et al. 2024** (arXiv:2401.06091). Searches
  for 2025–2026 work returned only that paper and its NeurIPS/ACM versions `[FT]`. The repo's
  treatment stands.
- **ASD is still at ASD2023.** No 2026 release found `[FT]`.
- **No TRIPOD/CONSORT analogue for structure-based site prediction has appeared.** A fresh search
  returned only the same three partial standards the repo already names `[FT]`.
- **PASSer has no post-2023 release** that I could find `[FT]`.

---

## 2. Is the frozen endpoint set the one the field recognises?

### 2.1 The census

Thirty-six tools and assessments. "Unit" is what is actually scored. "Negative class" is what the
positives are compared against. Rows marked `[FT]` were read at source this session; rows marked
`[repo]` are carried from the repo's evidence base at the tag recorded there.

|   # | Tool / assessment          |    Year | DOI                            | Metrics reported                                                                                               | Unit                  | Negative class                                                   | Src                       |
| --: | -------------------------- | ------: | ------------------------------ | -------------------------------------------------------------------------------------------------------------- | --------------------- | ---------------------------------------------------------------- | ------------------------- |
|   1 | PASS                       |    2000 | 10.1023/A:1008124202956        | top-1 / top-3 hit rate; DCA ≤ 4 Å                                                                              | pocket                | other ASPs on the same protein                                   | `[repo]`                  |
|   2 | Q-SiteFinder               |    2005 | 10.1093/bioinformatics/bti315  | precision at 1.6 Å, 25 % threshold                                                                             | pocket                | other probe clusters                                             | `[repo]`                  |
|   3 | LIGSITEcsc                 |    2006 | 10.1186/1472-6807-6-19         | hit rate at 4 Å                                                                                                | pocket                | other pockets                                                    | `[repo]`                  |
|   4 | PocketPicker               |    2007 | 10.1186/1752-153X-1-7          | TOP1 / TOP3 hits                                                                                               | pocket                | other pockets                                                    | `[repo]`                  |
|   5 | fpocket                    |    2009 | 10.1186/1471-2105-10-168       | MOc; rank-1 / top-3                                                                                            | pocket / alpha-sphere | other pockets                                                    | `[repo]`                  |
|   6 | BDT (assessment metric)    |    2010 | 10.1093/bioinformatics/btq543  | graded distance score                                                                                          | residue               | non-binding residues                                             | `[repo]`                  |
|   7 | Panjkovich & Daura         |    2012 | 10.1186/1471-2105-13-273       | PPV, sensitivity                                                                                               | pocket                | non-allosteric pockets                                           | `[repo]`                  |
|   8 | Allosite                   |    2013 | 10.1093/bioinformatics/btt399  | criteria in unretrieved SI                                                                                     | pocket                | unstated in body                                                 | `[repo]`                  |
|   9 | SPACER                     |    2013 | 10.1093/nar/gkt460             | none (case study)                                                                                              | residue → site        | none                                                             | `[repo]`                  |
|  10 | COACH                      |    2013 | 10.1093/bioinformatics/btt447  | MCC; 2.5 Å label                                                                                               | residue               | non-binding residues                                             | `[repo]`                  |
|  11 | PARS                       |    2014 | 10.1093/bioinformatics/btu002  | 44 % top-1, 73 % top-3                                                                                         | pocket                | other cavities                                                   | `[repo]`                  |
|  12 | CASP10 assessment          |    2014 | 10.1002/prot.24495             | MCC, BDT                                                                                                       | residue               | non-binding residues                                             | `[repo]`                  |
|  13 | AlloPred                   |    2015 | 10.1186/s12859-015-0771-1      | 23/40 top-1, 28/40 top-2; **no test**                                                                          | pocket                | "pockets without known allosteric binding residues"              | `[FT]`                    |
|  14 | CryptoSite                 |    2016 | 10.1016/j.jmb.2016.01.029      | AUC 0.83; TPR/FPR; KS test                                                                                     | residue               | 705 concave surface patches + non-binding residues               | `[repo]`                  |
|  15 | Amor et al.                |    2016 | 10.1038/ncomms12477            | quantile score; 1,000 surrogate sites; bootstrap 95 % CI                                                       | bond → residue → site | size- and diameter-matched surrogate sites                       | `[repo]`                  |
|  16 | DeepSite                   |    2017 | 10.1093/bioinformatics/btx350  | DCC, **DVO**                                                                                                   | pocket / volume       | other predicted volumes                                          | `[repo]`                  |
|  17 | AllositePro                |    2017 | 10.1021/acs.jcim.7b00014       | **unreachable (ACS 403)**                                                                                      | pocket                | unknown                                                          | `[repo]`                  |
|  18 | P2Rank                     |    2018 | 10.1186/s13321-018-0285-8      | top-n / top-(n+2), "DCC" = DCA 4 Å                                                                             | pocket                | other pockets                                                    | `[repo]`                  |
|  19 | Tee, Guarnera & Berezovsky |    2018 | 10.1371/journal.pcbi.1006228   | ROC AUC                                                                                                        | residue               | non-site residues                                                | `[repo]`                  |
|  20 | Ohm                        |    2020 | 10.1038/s41467-020-17618-2     | "TPR"/"PPV" (names inverted); no null                                                                          | residue               | 1MFT negative control protein                                    | `[repo]`                  |
|  21 | ESSA                       |    2020 | 10.1016/j.csbj.2020.06.020     | 10/14 holo, 7/14 apo; **no test**                                                                              | pocket                | other fpocket pockets                                            | `[repo]`                  |
|  22 | Kalasanty                  |    2020 | 10.1038/s41598-020-61860-z     | DCC < 4 Å, DVO                                                                                                 | pocket / volume       | other volumes                                                    | `[repo]`                  |
|  23 | PASSer v1                  |    2021 | 10.1088/2632-2153/abe6d6       | top-1 60.7 %, top-3 84.9 %; accuracy 0.974, recall, precision, F1, ROC AUC                                     | pocket                | 2,127 non-allosteric pockets                                     | `[repo]`                  |
|  24 | ProteinLens                |    2021 | 10.1093/nar/gkab350            | quantile score; surrogates; bootstrap CI; quantile regression on distance                                      | bond → residue        | surrogate sites                                                  | `[repo]`                  |
|  25 | Wu, Strömich & Yaliraki    |    2021 | 10.1016/j.patter.2021.100408   | detection rates; bootstrap 95 % CI                                                                             | site                  | surrogate sites                                                  | `[repo]`                  |
|  26 | PUResNet                   |    2021 | 10.1186/s13321-021-00547-7     | DCC ≤ 4 Å                                                                                                      | pocket                | other volumes                                                    | `[repo]`                  |
|  27 | PASSer2.0                  |    2022 | 10.3389/fmolb.2022.879251      | top-1/2/3; precision, recall, F1; **no test**                                                                  | pocket                | 4,904 non-allosteric pockets (two incompatible label rules)      | `[repo]`                  |
|  28 | APOP                       |    2023 | 10.1093/bioinformatics/btad275 | top-3 success 92/104; **one-sided Wilcoxon signed-rank, P = 0.00088** vs AlloPred                              | pocket                | other fpocket pockets                                            | `[FT]`                    |
|  29 | KeyAlloSite                |    2023 | 10.7554/eLife.81850            | top-1/2/3 56/76/96 %; Student's t vs 2 size-matched surface patches, 4 repeats                                 | pocket / residue      | contiguous size-matched random surface patches                   | `[repo]`                  |
|  30 | PocketMiner                |    2023 | 10.1038/s41467-023-36699-3     | ROC-AUC 0.83 ± 0.04, PR-AUC 0.44 ± 0.12; ROC-AUC 0.87 on the experimental task; **no test**                    | residue               | MOAD-absence residues, falsified by simulation                   | `[FT]`                    |
|  31 | SiteFerret                 |    2023 | 10.1021/acs.jctc.2c01306       | one-class ranking                                                                                              | pocket                | **none by design**                                               | `[repo]`                  |
|  32 | MEF-AlloSite               |    2024 | 10.1186/s13321-024-00882-5     | ROC AUC 0.803; average precision; Cohen's d                                                                    | pocket                | non-modulator pockets, undersampled 1:5                          | `[repo]`                  |
|  33 | LIGYSIS-bench              |    2024 | 10.1186/s13321-024-00923-z     | >10 metrics; **recommends top-N+2 recall**; DCC 10–12 Å                                                        | pocket + residue      | non-binding residues / pockets                                   | `[repo]`                  |
|  34 | Mariano et al.             |    2024 | 10.1016/j.csbj.2024.10.036     | KS tests on features, **no p-values in text**                                                                  | residue               | 1:21 imbalance                                                   | `[repo]`                  |
|  35 | Allo-Allo                  |    2024 | 10.1101/2024.09.28.615583      | AUPRC 0.77 / AUROC 0.95; **Welch's t-test with Bonferroni** on a downstream AlphaMissense validation           | residue               | "residues not labeled as allosteric sites within these proteins" | `[FT]`                    |
|  36 | CryptoBench                |    2025 | 10.1093/bioinformatics/btae745 | AUC, AUPRC, ACC, TPR, FPR, MCC, F1; **no test**                                                                | residue               | residues beyond 4.5 Å of the ligand                              | `[FT]`                    |
|  37 | AlloBench                  |    2025 | 10.1021/acsomega.5c01263       | **Jaccard index only**, swept 0–0.5; **no test**                                                               | residue sets          | **none defined**                                                 | `[repo]`                  |
|  38 | DeepAllo                   |    2025 | 10.1093/bioinformatics/btaf294 | F1 89.66 %, precision, recall; top 1/3/5/10 %; **no test**                                                     | pocket                | fpocket pockets with no allosteric residue                       | `[FT]`                    |
|  39 | STINGAllo                  |    2025 | 10.1093/bib/bbaf424            | **DCC success 78 % / 60.2 % at a 4 Å centre-to-centre threshold**; per-residue F1 0.64, MCC 0.64; **no test**  | residue + pocket      | not explicitly described                                         | `[FT]`                    |
|  40 | Allo-PED / AlloPED         | 2025–26 | 10.1101/2025.03.28.645953      | pocket AUC 0.920, MCC 0.544, precision 47.1 %; site AUC 0.563, AUPRC 0.67, F1 0.59; **no test on performance** | pocket + residue      | pockets with < 25 % overlap; 4,571 neg vs 185 pos                | `[FT]`                    |
|  41 | Eccleston & Furnham        |    2025 | 10.1101/2025.06.27.662060      | accuracy, precision, recall, F1, AUC-ROC, average precision; **no test**                                       | residue               | residues outside the allosteric site (~6 % positive)             | `[FT]`                    |
|  42 | UniSite                    |    2025 | 10.48550/arXiv.2506.03237      | **AP at IoU 0.3 and 0.5**; critiques DCC/DCA                                                                   | site (residue mask)   | unmatched ground-truth sites                                     | `[FT]`                    |
|  43 | ZHMolEReP                  |    2026 | 10.1021/acs.jcim.6c00141       | recall 0.7037, AUC 0.7858, 33/40 proteins                                                                      | residue               | unknown (ACS 403)                                                | `[repo]`                  |
|  44 | AlloEF                     |    2026 | 10.1021/acs.jpcb.6c00242       | F1 0.630, MCC 0.609                                                                                            | residue               | SVM-SMOTE-balanced training set                                  | `[FT]`/unverified numbers |
|  45 | Kinase pLM framework       |    2026 | 10.1021/acs.jctc.6c00427       | AUROC 0.705, AUPR 0.061 (ALLO class), micro-MCC, micro-accuracy; **no test**                                   | residue               | residues beyond 4 Å of the ligand                                | `[FT]`                    |
|  46 | Seq2Pocket                 |    2026 | 10.64898/2026.01.28.702257     | **DCC at 12 Å**, DCC top-N / top-(N+2) / MAX, RRO, **PFI**; MCC, AUC, AUPRC, F1, accuracy                      | residue → pocket      | non-binding residues                                             | `[FT]`                    |
|  47 | CAPASP (assessment)        |    2026 | 10.1007/s10822-026-00831-4     | **sensitivity, specificity, F1, MCC, ranking capability**                                                      | pocket (5 tools)      | two purpose-built independent sets                               | `[FT]`                    |
|  48 | CTQW centrality            |    2026 | 10.1021/jacs.6c08053           | Spearman ρ, Kendall τ, overlap@k, Jaccard, as _agreement_; **no null, no AUC**                                 | residue               | none                                                             | `[repo]`                  |

### 2.2 What the census says

Counting over the 48 rows above:

- **A top-N rank success rate appears in 15 rows** (1, 3, 4, 5, 11, 13, 18, 21, 23, 27, 28, 29, 33, 38, 46). In **every one of them the unit ranked is a pocket, not a residue.** **[derived from the table]**
- **A threshold-free discrimination number (ROC AUC and/or AUPRC) appears in 12 rows** (14, 19, 23,
  30, 32, 35, 36, 40, 41, 43, 45, 46). Rows 33 and 44 report large metric panels whose AUC content
  I did not verify, and are excluded. All the residue-level ones are 2016 or later and most are
  2023 or later. **[derived]**
- **A stated statistical test appears in 7 of the 48 rows** (14, 15, 24, 25, 28, 29, 35),
  representing **5 independent constructions**: CryptoSite (KS on feature distributions);
  Amor / ProteinLens / Wu (one lineage, surrogate-site bootstrap); APOP (Wilcoxon, between
  methods, not against a null); KeyAlloSite (t-test, n = 4); Allo-Allo (Welch's t with Bonferroni,
  on a downstream validation rather than on performance). **[derived]**
- **Top-N _residue_ still has no convention.** The two 2026 papers that come closest — Seq2Pocket and UniSite — both convert residue scores into **sites or pockets before scoring**. Neither scores a bare ranked residue list. `[FT]`

### 2.3 Verdict on the endpoint set

**The repo's threshold-free half matches the field. Its top-k half does not, and cannot, because
the field has no top-k residue convention to match. The divergence is defensible. Three
justifications for it are weaker than they read.**

**Defensible.** CHALLENGE §5 makes the scored artifact a top-5 residue list. Scoring a pocket
when the deliverable is residues would be the same category error the field commits in reverse.
The confirmatory statistic (mean midrank) appears in no paper in the census, but it is a strictly
monotone re-parameterisation of AUC-ROC under a size-fixed null, so it introduces no new
behaviour, and the repo prints AUC-ROC beside it. That is honest.

**Weakness 1 — the recall@5 justification is a category error.** `harness.py` carries the comment
"Of 22 tools surveyed, 17 report a recall-style top-N success rate" `[CODE]`, and README §3.2
repeats it. The field's top-N number is a **per-protein binary: did the true pocket land in the
top 3 of ~10 detected pockets**. The repo's recall@5 is **the fraction of a 11–20 residue label
set recovered in 5 picks**. These are different quantities with different chance lines. Printing
recall@5 is still right — a reader will compute it otherwise — but the stated reason should be
that, not a claimed field convention it does not share.

**Weakness 2 — the deliverable's own wording is ambiguous and the protocol does not say which
reading it took.** CHALLENGE §5 says "a ranked list of the **top 5 predicted allosteric sites
(residue indices)**". §8 of the same file (our restatement) says "Top-5 ranked allosteric
**residue** hit list". Under the first reading the deliverable is five _sites_, each named by one
residue index, and precision@5 against a single site's label set is the wrong statistic — a
perfect answer would put one residue in the true site and four elsewhere, scoring precision@5 =
0.2. Under the second it is five residues from one site. The repo took the second. It should say
so, in one sentence, with the reason. Under the first reading the untested `site_pocket_rank` is
closer to the required artifact than any tested endpoint.

**Weakness 3 — the pocket-level number is reported and never tested, and that is now the field's
only independent yardstick.** CAPASP's fifth dimension is "ranking capability"
(doi:10.1007/s10822-026-00831-4) `[FT]`, and the modal metric across the census is top-3 pocket
rank. `score_arm` computes `site_pocket_rank` out of `n_pockets_ranked` and refuses to test it,
for a stated and correct reason (the detector, not the method, fixes the denominator). Fine. But
the report must pre-declare how that number will be read, or a reader will read it as the
headline and the repo will have no pre-registered statement about it.

---

## 3. The omissions, attacked

Eight declared omissions. **Six reasons are correct. Two need to change. One further omission is
undocumented, and one metric class is absent from the whole design.**

### 3.1 Accuracy — reason correct, nothing compels it

At 1.6–11 % prevalence the all-negative classifier scores 0.89–0.98. That is arithmetic. No source
compels reporting it. In-field corroboration: PASSer v1 reports accuracy 0.974 at a 5.3 % positive
rate, doi:10.1088/2632-2153/abe6d6 `[repo]`; the kinase pLM framework reports micro-accuracy
0.94–0.96 alongside AUPR 0.061, doi:10.1021/acs.jctc.6c00427 `[FT]`. **Both illustrations are now
verified at full text, which lets the repo drop the unverified bitmap-read Allo-Allo illustration
it currently flags.**

### 3.2 MCC and F1 — reason correct at k = 5, and the manifest states the wrong reason

The arithmetic. With a fixed prediction of k = 5, perfect precision, a label set of size m and a
candidate set of size n:

- max F1 = 2·1·(5/m) / (1 + 5/m) = **10/(m + 5)**. For m = 11 that is **0.625**; for m = 20,
  **0.400**. **[derived]**
- max MCC (FP = 0) = sqrt(5(n − m) / (m(n − 5))) ≈ **sqrt(5/m)**. For m = 11, **0.674**; for
  m = 20, **0.500**. **[derived]**

STINGAllo reports per-residue F1 0.64 and MCC 0.64, doi:10.1093/bib/bbaf424 `[FT]`. **A perfect
top-5 answer on the repo's larger arms cannot reach STINGAllo's F1 and can barely reach its MCC.**
The repo's "k = 5 is too small" argument is therefore correct and now has a number behind it. Put
that number in the document.

**Is there a source that compels inclusion?** Yes, conditionally. CAPASP 2026 names F1 and MCC
among its five evaluation dimensions `[FT]`; STINGAllo, CryptoBench, Allo-PED, AlloEF and the
kinase pLM framework all report both at residue level `[FT]`. **The condition is a variable-size
prediction.** Every one of those papers predicts a variable-size residue set, not a fixed five.

**And the repo has a variable-size prediction available.** `src/allo/classical/postprocess` holds
stage S7 site assembly `[CODE]`. Once a site is assembled, F1, MCC, Jaccard and UniSite's
IoU-based AP are all computable and directly comparable to the field's own numbers. Reporting them
on the assembled site — descriptive, never confirmatory — costs nothing, breaks no freeze, and
removes the single loudest objection a reviewer from this field will raise. **This is the strongest
argument against the omission and the protocol does not address it.**

**The manifest states the reason the audit withdrew.** `manifest.yaml` says MCC and F1 "need a
decision threshold, and no threshold can be chosen blind", and quotes Utgés & Barton as the
argument `[CODE]`. `AUDIT.md` §4 corrected exactly this: "The Utgés & Barton quote is about
prediction-set size, not thresholds. At fixed k = 5 it does not apply, because every method
predicts the same number." README §3.3 was updated. The manifest was not.

### 3.3 Jaccard — reason correct at fixed k, and the manifest's number is wrong

Ceiling = 5/m: **0.25 to 0.4545 across the 14 arms** (README, correct). `manifest.yaml` says
"caps at about 0.31, below AlloBench's 0.5 reporting threshold" `[CODE]`. Both clauses are the
ones `AUDIT.md` §3 and §4 corrected: 0.31 is the KRAS value, not the ceiling, and AlloBench
tabulates JI values of 0.1–0.4 which those ceilings reach, so "below the reporting threshold" is
not the reason.

**And the pressure has increased since the freeze.** UniSite (NeurIPS 2025) makes residue-mask
IoU — Jaccard — its recommended metric, with AP at IoU 0.3 and 0.5, doi:10.48550/arXiv.2506.03237
`[FT]`. AlloBench already scores nothing else, doi:10.1021/acsomega.5c01263 `[repo]`. The repo's
decline survives **only** for the fixed-five list. On an assembled site it does not survive, and
the fix is the same as §3.2.

### 3.4 DVO — reason correct, and the manifest carries a claim its own audit called false

"No volume is predicted" is decisive on its own. `manifest.yaml` adds "and no standard threshold
for it exists" `[CODE]`. `AUDIT.md` §4: that is **false**; `DVO > 0.2` is stated verbatim in
doi:10.1021/acs.jcim.5c00336 `[repo]`. README withdrew the clause. The manifest did not.

### 3.5 Bootstrap confidence interval — the reason is right about the wrong bootstrap

The repo declines a **residue-level** nonparametric bootstrap because the label set is a
contiguous, spatially autocorrelated patch, so residues are not exchangeable, and resampling
moves the prevalence the null conditions on. **That reasoning is correct and I found no source
that overturns it.** DeLong's parametric AUC interval (doi:10.2307/2531595 `[FT]`) fails on the
same assumption — it treats observations as independent — so declining it is also right. But the
protocol never names DeLong and declines it, which it should.

**The hole: the repo declined the residue bootstrap and never considered a patch-level one.** The
field's only confidence intervals are bootstraps over the **surrogate-site pool**, not over
residues — "a 95 % confidence interval is obtained for each protein... by using bootstrap with
10,000 resamples with replacement", doi:10.1016/j.patter.2021.100408 `[repo]`, and the same in
Amor et al., doi:10.1038/ncomms12477 `[repo]`. The repo already draws 9,999 matched patches per
arm `[CODE]`. A percentile interval on `observed − null_mean` computed by resampling **patches**
assumes only that the patches are exchangeable draws from the pool, which is exactly what the
sampler constructs. It does not assume residue exchangeability and it does not move the
prevalence. It costs one line.

**Caveat, and it must be stated if this is adopted:** the pool is drawn once per arm and shared
(ADR 0018), so the patches are conditionally independent given the pool rather than independent,
and the interval is a screen, not a proof — the same disclosure the protocol already makes for the
p-value.

### 3.6 Enrichment factor, BEDROC, RIE — reason correct

Two independent literature sweeps found zero use in site prediction `[repo]`, and my census of 48
rows found none either **[derived]**. BEDROC's α = 20 encodes "the top 8 % matters", which is
meaningless at k = 5. α is nominally tunable, but a tuned α is a hyperparameter and there is no
precedent to anchor it. **Nothing compels inclusion.**

### 3.7 One undocumented omission and one absent metric class

- **Specificity is not reported and not declined.** CAPASP names it as one of five dimensions
  `[FT]`. At k = 5 it is (n − m − FP)/(n − m) ≈ 1 for every method, so it is as uninformative as
  accuracy — but §3.3 of the README does not say so. Add one line. (Sensitivity **is** covered:
  recall@5 is sensitivity at k = 5.)
- **Nothing measures whether the top-5 is one place or five places.** See §1.2. A PFI-style
  statistic — the number of connected components the top-5 forms in the evaluation graph, or its
  radius of gyration against the chance line the repo already computes for DCC — is a two-line
  addition and closes a hole that the newest work in the field is explicitly about
  (doi:10.64898/2026.01.28.702257) `[FT]`.

---

## 4. Null models

### 4.1 Independent verification of the "13 of 18 state no test" claim

I re-checked nine papers at source this session, without consulting the repo's table first,
asking one question: does the paper state a statistical test, null model, permutation test or
confidence interval **on its performance claim**?

| Paper                | Year | Test on the performance claim?                                                                                       | Src    |
| -------------------- | ---: | -------------------------------------------------------------------------------------------------------------------- | ------ |
| AlloPred             | 2015 | No                                                                                                                   | `[FT]` |
| PocketMiner          | 2023 | No. Standard deviations across CV folds only.                                                                        | `[FT]` |
| APOP                 | 2023 | **Yes** — "A one-sided Wilcoxon signed-rank test... P-value of 0.00088", but between two methods, not against a null | `[FT]` |
| Allo-Allo            | 2024 | Not on performance. **Welch's t-test with Bonferroni** on a downstream AlphaMissense validation                      | `[FT]` |
| CryptoBench          | 2025 | No                                                                                                                   | `[FT]` |
| DeepAllo             | 2025 | No                                                                                                                   | `[FT]` |
| STINGAllo            | 2025 | No                                                                                                                   | `[FT]` |
| Allo-PED             | 2025 | No on performance; one p-value on a conservation comparison                                                          | `[FT]` |
| Eccleston & Furnham  | 2025 | No                                                                                                                   | `[FT]` |
| Kinase pLM framework | 2026 | No                                                                                                                   | `[FT]` |

**Result: 8 of 10 state no test at all on performance; 1 states a between-method test; 1 states a
test on something else.** The repo's 13/18 is 72 %; my independent, partly non-overlapping and
more recent sample gives 80–90 %. **The claim is corroborated in direction and magnitude.**

**One correction.** `evaluation-metrics.md` §3.5 states "**0** apply any multiplicity correction.
Not one." `[repo]` That is false as literally worded: Allo-Allo says verbatim "Bonferroni
correction was applied to adjust the p-values" `[FT]`. Allo-Allo is not in the repo's 18-paper
frame, so the tally is not wrong within its frame — but the sentence reads as a claim about the
field. The defensible restatement: **no paper applies a multiplicity correction to a performance
claim.** This is the same class of defect as `AUDIT.md` B3 and should be fixed the same way.

### 4.2 What the field's nulls actually are

Three constructions exist, and only one is geometry-matched.

1. **Size- and diameter-matched surrogate sites, 1,000 per protein, one-sided on diameter.**
   Amor et al. doi:10.1038/ncomms12477; ProteinLens doi:10.1093/nar/gkab350; Wu et al.
   doi:10.1016/j.patter.2021.100408 `[repo]`. One group, one construction, dropped in that group's
   own later web server.
2. **Contiguous size-matched random surface patches, 4 repeats, Student's t.** KeyAlloSite
   doi:10.7554/eLife.81850 `[repo]`. Correct geometry, unusable n.
3. **Equal-size random subsets from the same region, 1,000 permutations, Mann-Whitney.** Guharoy
   & Chakrabarti doi:10.1186/1471-2105-11-286 `[repo]`, from the PPI literature.

The repo's matched patch is stricter than all three: it matches size, component-size multiset,
mean contact degree and radius of gyration, two-sided, at 9,999 replicates, and it **calibrates
its own type-I rate**, which no paper in this field does. That is not merely "ahead"; it is a
different standard.

### 4.3 Nulls the repo has not considered

| Construction                                                     | Source                                                                                                                                                                 | Why it matters here                                                                                                                                                                                                                                                                      |
| ---------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Eigenmode-rotation surrogates (eigenstrapping)**               | doi:10.1162/IMAG.a.71 `[FT]`                                                                                                                                           | Best measured FPR of the three spatial nulls tested (5.2–5.3 % vs 12.3 % spin, 29.2–36.3 % variogram). Needs no λ. One free parameter. Rotating within eigenspaces of the contact-graph Laplacian is the direct protein analogue. **No protein demonstration exists. [NOT ESTABLISHED]** |
| **Screen-and-discard post-stratification of the surrogate pool** | doi:10.1162/imag.a.118 `[FT]`                                                                                                                                          | Removes the surrogates whose realised autocorrelation deviates most from the target, rather than re-centring the acceptance window. Distinct from repair C, which the repo tested and which failed.                                                                                      |
| **Tailor-made decoy sets with a controlled property**            | ProSPECCTs, Ehrt C, Brinkjost T, Koch O, _PLOS Comput Biol_ 14(11), 2018, doi:10.1371/journal.pcbi.1006483 `[FT]` — **title and metadata only; not read at full text** | A precedent for constructing negative sets to isolate one property rather than accepting whatever a detector emits. Relevant to the decoy-lining size mismatch the repo discloses (median ratio 0.55 on 14/14 arms).                                                                     |
| **Local Moran's I on residue contact graphs**                    | PMC3533907, `[UNVERIFIED]` in the repo's own evidence file                                                                                                             | The standard spatial-statistics diagnostic for the exact property the calibration gate is fighting. Would give a per-method, per-arm autocorrelation number in place of the assumed λ grid.                                                                                              |

Burt et al. 2020, Markello & Misic 2021, Milenković et al. 2009 and Amor et al. 2016 are all
already cited. The eigenstrapping result **inverts the repo's ranking of the first of them**.

---

## 5. Cross-method comparability

The challenge requires an honest comparison of classical, quantum, AI and hybrid methods. The
methods-comparison literature — not the allostery literature — states five requirements. The repo
meets three cleanly, meets one by accident, and does not meet the fifth.

### 5.1 The named standards

| Standard                                                       | Citation                                                                                                                                                                                                                                                                     | What it requires that bears here                                                                                                                                                                                                         |
| -------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Essential guidelines for computational method benchmarking** | Weber LM, Saelens W, Cannoodt R, et al. _Genome Biol_ 20:125, 2019, doi:10.1186/s13059-019-1738-8 `[FT]`                                                                                                                                                                     | The closest thing to a checklist for exactly what this repo is doing: designing and running a benchmark. **Not cited anywhere in the repo's evidence base.**                                                                             |
| **A plea for neutral comparison studies**                      | Boulesteix A-L, Lauer S, Eugster MJA. _PLoS ONE_ 8(4):e61562, 2013, doi:10.1371/journal.pone.0061562 `[FT]`                                                                                                                                                                  | A comparison run by the authors of one of the compared methods is not neutral. This project proposes a quantum method **and** runs the benchmark. Freezing first is the mitigation; the report must name the problem and the mitigation. |
| **Over-optimism from design and analysis multiplicity**        | Nießl C, Herrmann M, Wiedemann C, Casalicchio G, Boulesteix A-L. _WIREs Data Min Knowl Discov_ 12, 2021/2022, doi:10.1002/widm.1441 `[FT]`; Buchka S, Hapfelmeier A, Gardner PP, Wilson R, Boulesteix A-L. _Genome Biol_ 22:152, 2021, doi:10.1186/s13059-021-02365-4 `[FT]` | Newly introduced methods look better in their own papers. Quantifies the effect the freeze exists to prevent.                                                                                                                            |
| **Leakage taxonomy**                                           | Kapoor S, Narayanan A. _Patterns_ 4, 2023, doi:10.1016/j.patter.2023.100804 `[FT]`                                                                                                                                                                                           | 294 papers across 17 fields, eight leakage types. The repo's C1 machinery is a leakage control; naming the taxonomy makes it legible to a general reviewer.                                                                              |
| **DOME**                                                       | Walsh I, Fishman D, Garcia-Gasulla D, et al. _Nat Methods_ 18:1122–1127, 2021, doi:10.1038/s41592-021-01205-4 `[FT]`; **DOME Registry**, Attafi OA, Clementel D, Kyritsis K, et al. _GigaScience_ 13, 2024, doi:10.1093/gigascience/giae094 `[FT]`                           | Four-axis report (Data, Optimization, Model, Evaluation). Scoped to supervised ML, so the Data and Evaluation axes transfer and the Optimization axis does not.                                                                          |
| **TRIPOD+AI**                                                  | Collins GS, Moons KGM, Dhiman P, et al. _BMJ_ 385:e078378, 2024, doi:10.1136/bmj-2023-078378 `[FT]`                                                                                                                                                                          | Pre-specification of the analysis, reporting of **all** metrics computed, and open-science items. Clinical in scope; the pre-specification and complete-reporting items transfer directly.                                               |
| **AIMe registry**                                              | _Nat Methods_ 18:1128–1131, 2021, doi:10.1038/s41592-021-01241-0 `[FT]`                                                                                                                                                                                                      | A public, citable pre-registration route if the project wants one.                                                                                                                                                                       |
| **Ten rules for a structural bioinformatic analysis**          | Wankowicz SA. _PLoS Comput Biol_ 21(10):e1013094, 2025, doi:10.1371/journal.pcbi.1013094 `[repo]`                                                                                                                                                                            | Already cited by the repo. Rule 6 ("Controls must directly address the null hypothesis you wish to reject") is the one that binds here.                                                                                                  |

### 5.2 Paired tests and multiplicity — the one real hole

**Paired, same-instance testing: met, and met well.** `compare_methods` differences the two midrank
vectors and tests the difference's patch mean against the same matched-patch pool `[CODE]`. That
is stronger than Demšar's recommendation for two methods (Wilcoxon signed-rank over datasets;
Demšar J, _J Mach Learn Res_ 7:1–30, 2006 — **JMLR mints no DOI**, stable URL
`jmlr.org/papers/v7/demsar06a.html`), because it is paired within an instance rather than across
instances.

**Effect size beside the p: met.** `compare_methods` returns `mean_rank_difference` and
`auc_roc_difference` alongside `p` and `p_calibrated` `[CODE]`. The objection I expected to make
does not hold.

**Multiplicity across methods: not met, and this is the hole.** `holm()` exists and is wired only
to the three confirmatory arms `[CODE]`. `manifest.yaml` lists **nine** required baselines, and
`classical.SCORERS` plus `quantum.walk.SCORERS` will supply many methods. That is a large family
of two-sided paired tests with no declared correction. README §8 disposes of this by declaring
everything except the matched-patch family "descriptive". **But ADR 0025 and README §13 make
"beating `cavity_volume`" the claim threshold.** The claim therefore rests entirely on a family
the protocol declares unprotected. That is an internal inconsistency, and it is the kind a
reviewer finds in five minutes.

The fix is small and does not require rebuilding anything: declare a **second confirmatory
family** — the paired comparison against the single pre-declared reference `cavity_volume`, on the
same three `corrected` arms, Holm over three, two-sided as already frozen — and declare every
other baseline comparison descriptive. The reference is already pre-declared, so this adds no
freedom.

For K > 2 methods, Demšar's Friedman test with a post-hoc correction is the standard route; the
caution against mean-rank post-hoc tests is Benavoli G, Corani G, Mangili F, "Should we really use
post-hoc tests based on mean-ranks?", _J Mach Learn Res_ 17:1–10, 2016, arXiv:1505.02288,
doi:10.48550/arXiv.1505.02288 `[FT]`. At 14 arms and a handful of methods, Holm against one
pre-declared reference is simpler and stronger than Friedman, and it is what I recommend.

**Clustered, shared-instance evaluation.** A 2026 treatment of exactly this design — K methods
scored on the same instances, with instances clustered — is Mandujano Reyes JF, "Statistical
Methods for Multiple Language Model Comparison on a Shared Evaluation", arXiv:2608.22659 `[FT]`:
a random-effects model with methods as fixed effects and questions or clusters as random effects,
which "recover[s] Miller's paired and clustered estimators for K = 2" and extends to any K. The
residue-within-arm structure here is the same shape. Offered as a pointer, not a requirement —
the paper is two weeks old and the permutation route is exact.

**Paired AUC comparison.** DeLong ER, DeLong DM, Clarke-Pearson DL, _Biometrics_ 44(3):837, 1988,
doi:10.2307/2531595 `[FT]` is the standard test for two AUCs on the same cases. Its independence
assumption fails on a contiguous label patch, so declining it is right — name it and decline it.

### 5.3 Ranking stability

The noise-resilience statistics (Spearman ρ, Kendall τ, overlap@5, Jaccard@5) are the four the
CTQW paper reports, chosen by precedent `[CODE]`. R1 says "it is standard practice" is not a
reason. **Rank-biased overlap is top-weighted and the others are not**, which matters when the
deliverable is a top-5: Webber W, Moffat A, Zobel J, _ACM TOIS_ 28(4):20, 2010,
doi:10.1145/1852102.1852106 `[FT]`. The repo omits it because it "has no use in this literature".
That is a popularity argument. The correct statement is that overlap@5 already captures
top-weighting at the exact k that is shipped, so RBO adds little — which is a first-principles
reason and should replace the current one.

---

## 6. What "success" means per the challenge, clause by clause

### 6.1 CHALLENGE §4.1

| Clause (verbatim)                                                                                                          | Does the frozen protocol test it?                                                                                                                                                                                                                                                                                                          |
| -------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| "Participants **must build a quantum circuit** that simulates signal propagation through the protein structure"            | **No, and correctly not** — this is a method requirement, not an endpoint. But the scoring record carries `method` as a free-text string and **no method-class field and no circuit-resource fields** `[CODE]`. Nothing in the evaluation layer prevents a classical number and a quantum number being tabulated without their provenance. |
| "The circuit must output a **ranking of residues** based on their dynamic connectivity"                                    | **Yes.** The contract is one score per candidate residue, and `_aligned` refuses a partial scoring `[CODE]`.                                                                                                                                                                                                                               |
| "statistically significantly higher scores to known distal regulatory residues compared to **random background residues**" | **Yes, and on a stricter null than asked.** The confirmatory null is the matched patch, not the literal uniform draw. The literal null is reported with its measured 0.096–0.323 type-I rate. **This must be stated in the report as a deliberate deviation**: the sponsor asked for one test and the protocol decides on a harder one.    |
| "...and **non-functional surface pockets**"                                                                                | **No, not on two of the three confirmatory arms.** See §6.2. **This is the compliance failure.**                                                                                                                                                                                                                                           |
| "Participants are free to hypothesize and define the specific quantum metric"                                              | **Yes.** No constraint on the score's construction.                                                                                                                                                                                                                                                                                        |

### 6.2 The negative-class-(b) failure, in detail

Verified in code `[CODE]`:

- `nulls.decoy_pockets` is a `pocket_rank_permutation`: `permutation_p(observed, decoy_ranks)`
  where `decoy_ranks` has one entry per decoy pocket. With 3 decoys the minimum attainable p is
  1/4 = **0.25**; the frozen per-arm floors are 0.25 / 0.25 / 0.040 / 0.10 / 0.024.
- `auc_roc_vs_decoy_linings` is a residue-level AUC-ROC over label residues against the **union of
  decoy-lining residues** (23–291 residues per arm). It is reported. **It has no null, no
  permutation and no p-value anywhere in the manifest or the harness.**

So negative class (b) has an effect size with no test and a test that cannot reject. README §5.3
says "The challenge's negative class (b) cannot reject at α = 0.05 on three of five primary arms".
**That sentence is true of the pocket-rank test and is over-general as a claim about the class.**
A residue-pooled permutation over the same two groups has a floor of `1/C(m+d, m)`, which is
negligible at m = 11–20 and d = 23–291 **[derived]**.

The size-mismatch objection in §5.3 does **not** transfer to the pooled test. That objection is
about the variance of a **per-pocket mean**, which scales with the reciprocal of the pocket's
size. A pooled residue-level rank test never averages within a pocket, so the 0.55 median size
ratio does not bias it in that way. A different caution does apply and must be stated: the decoy
linings are not geometry-matched to the label patch, so the pooled test measures what the
challenge literally words — labels against pocket linings — and not a compactness-controlled
contrast.

**The tension this creates.** Adding a declared test to a frozen protocol is a protocol change,
and the protocol forbids changes once a method is scored. Two controls have been scored
(`cavity_volume`, `distance_from_source_negated`), and ADR 0025 already amended the protocol after
that. The choice is between a documented, pre-method version-3 amendment and shipping a submission
that fails half the sponsor's dominant criterion on two of three mandated disease areas. **The
amendment is the lesser evil, and it must be made before any quantum, AI or hybrid method is
scored, with an ADR recording that the amendment was made blind to any such result.**

### 6.3 CHALLENGE §7

| Clause                                                                                                                | Status                                                                                                                                                                                                                                                                                       |
| --------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| "Statistically significant enrichment... AND non-functional surface pockets"                                          | See §6.2.                                                                                                                                                                                                                                                                                    |
| "Blind prediction on **apo input**, scored against the **holo ground truth** for KRAS G12C, BCR-ABL1, Cardiac Myosin" | **Met in substance, with a presentational risk.** The confirmatory family is the three **corrected** arms, not the mandated accessions, because all three mandated pairs are defective. Both are reported. The report must lead with that substitution rather than let a reader discover it. |
| "**Top-5 ranked hit list per target** is the scored artifact"                                                         | **Met under one of two readings.** See §2.3, weakness 2.                                                                                                                                                                                                                                     |
| Noise resilience                                                                                                      | **Endpoint declared** (four rank-stability statistics at k = 5).                                                                                                                                                                                                                             |
| Coarse-graining, with proof that compression retains the topological signal                                           | **Endpoint declared** (spectral distance, rank correlation, label recovery at k = 5).                                                                                                                                                                                                        |
| "Interpretability / low entry barrier" so medicinal chemists can use it                                               | **No endpoint anywhere, and no statement that there is none.**                                                                                                                                                                                                                               |
| "3D visualization of the quantum connectivity maps"                                                                   | Deferred to Phase 5. Not an endpoint. Acceptable, but say so.                                                                                                                                                                                                                                |
| "Clear logic linking the chosen quantum metric to the biological phenomenon"                                          | **No endpoint anywhere, and no statement that there is none.**                                                                                                                                                                                                                               |
| "Comparison to classical analogs"                                                                                     | **Endpoint declared**, nine baselines and a frozen paired test — but see §5.2 on multiplicity.                                                                                                                                                                                               |
| "Generalizability/scalability shown on extra targets"                                                                 | One across-target decision on the `generalisation` tier, Phase 5.                                                                                                                                                                                                                            |
| "Deep, unoptimized circuits... will be penalized"                                                                     | **The evaluation layer records no circuit resources.** C3 requires depth, qubit count and connectivity for every quantum method. Nothing binds a quantum p-value to its cost.                                                                                                                |
| c-Myc `1NKP`, part of the "MINIMUM set required for submission"                                                       | **No arm exists in any freeze.** `AUDIT.md` M15 records this as live. A required deliverable has no scoring path.                                                                                                                                                                            |

Two of the five §4.2 rows have no endpoint and no declared reason for having none. In a document
whose stated purpose is that "chosen after seeing a result, each becomes a hyperparameter", the
right entry is "no endpoint; judged qualitatively by the sponsor" — not silence.

---

## What must change in the repo

Ranked by severity. Items 1–4 must land before any quantum, AI or hybrid method is scored.

1. **[CRITICAL] Give negative class (b) a test that can reject.** Add a permutation or exact
   Mann-Whitney p for the existing residue-level `auc_roc_vs_decoy_linings` endpoint: label
   residues against the pooled decoy-lining residues, one-sided upper, reported per arm. Record it
   as a **version-3 protocol amendment** in a new ADR, made blind to any method result, and state
   in that ADR that the pocket-rank permutation remains reported and untested. Correct README §5.3
   so the "cannot reject" sentence is scoped to the pocket-rank test. _Files:_
   `docs/benchmark/evaluation/manifest.yaml`, `README.md` §4 and §5.3,
   `src/allo/scoring/harness.py`, `docs/adr/`.

2. **[CRITICAL] Resolve the claim-threshold inconsistency.** Declare a second confirmatory family:
   the paired `compare_methods` test against `cavity_volume`, on the three `corrected` arms, Holm
   over three. Declare every other baseline comparison descriptive. Without this, the claim the
   project intends to make (ADR 0025: "beating `cavity_volume`, not rejecting the null") rests on
   a family README §8 declares unprotected. _Files:_ `manifest.yaml` `decision:`, README §8 and
   §13, `docs/adr/`.

3. **[HIGH] Bring `manifest.yaml`'s omission rationales into line with `AUDIT.md` §4.** Three of
   five are the withdrawn versions: `mcc_and_f1` quotes Utgés & Barton as the argument when the
   audit ruled it inapplicable at fixed k; `jaccard` states a ceiling of 0.31 when the audit
   measured 0.4545 and rejected the "below the reporting threshold" reason; `dvo` carries the
   clause the audit withdrew as **false**. Replace with the README text. Add the derived ceilings
   as numbers: max F1 = 10/(m+5) = 0.40–0.625, max MCC ≈ sqrt(5/m) = 0.50–0.67, max Jaccard = 5/m
   = 0.25–0.4545. Also collapse the `arXiv:2604.17486` citation to `doi:10.1021/jacs.6c08053` per
   `AUDIT.md` §4. _File:_ `docs/benchmark/evaluation/manifest.yaml`.

4. **[HIGH] Rewrite README §12.4.** Variogram-matched surrogates are no longer "the right design".
   Measured FPR: eigenstrapping 5.2–5.3 %, spin test up to 12.3 %, BrainSMASH 29.2–36.3 %
   (doi:10.1162/IMAG.a.71). Name eigenmode-rotation surrogates as the current best-measured
   spatially constrained null, state that no protein demonstration exists **[NOT ESTABLISHED]**,
   and keep the existing reason for not adopting a method-specific null (every method must face
   the identical null sample). Add the screen-and-discard post-stratification pointer
   (doi:10.1162/imag.a.118) as the untried variant of `AUDIT.md` M14.

5. **[HIGH] Report F1, MCC and residue-set IoU on the assembled site (stage S7), descriptive
   only.** This restores comparability with CAPASP's five dimensions
   (doi:10.1007/s10822-026-00831-4), STINGAllo (doi:10.1093/bib/bbaf424), AlloBench
   (doi:10.1021/acsomega.5c01263) and UniSite's AP@IoU (doi:10.48550/arXiv.2506.03237) without
   touching the frozen confirmatory design. Keep them out of the top-5 record; put them in the
   report's comparability table.

6. **[HIGH] Measure whether the top-5 is one place or five.** Add a fragmentation statistic — the
   number of connected components the top-5 forms in the evaluation graph, and its radius of
   gyration against the chance line already computed for DCC. Motivated by the Pocket Fragmentation
   Index (doi:10.64898/2026.01.28.702257) and required by CHALLENGE §4.2's "actionable output".

7. **[MEDIUM] Add a patch-level percentile interval on the effect size.** Resample the 9,999
   matched patches, not the residues. The residue bootstrap is correctly declined; the patch
   bootstrap is what the field's own confidence intervals do (doi:10.1038/ncomms12477,
   doi:10.1016/j.patter.2021.100408), it assumes only patch exchangeability, and it does not move
   the prevalence. Disclose that the shared pool makes the patches conditionally independent, so
   the interval is a screen. Also name and decline DeLong (doi:10.2307/2531595) with its reason.

8. **[MEDIUM] Carry method class and circuit resources through the report.** Add
   `method_class` (classical / quantum / AI / hybrid) and, for quantum methods, circuit depth,
   qubit count and connectivity, to the **report template** rather than to the frozen record, so a
   quantum p-value cannot be quoted without its C3 cost.

9. **[MEDIUM] Fix two claims about the field.** (a) `evaluation-metrics.md` §3.5 "0 apply any
   multiplicity correction. Not one." → "no paper applies a multiplicity correction to a
   performance claim"; Allo-Allo applies Bonferroni to a downstream validation
   (doi:10.1101/2024.09.28.615583). (b) `harness.py` line ~278 and README §3.2: the field's
   "recall-style top-N success rate" is a per-protein pocket-rank hit rate, not residue recall.
   Print recall@5 because a reader will compute it, not because the field reports the same
   quantity.

10. **[MEDIUM] Declare the two §4.2 rows that have no endpoint.** Add to README §10:
    interpretability / low entry barrier, and the metric-to-biology logical link, are judged
    qualitatively and carry no frozen endpoint. Silence in a pre-registration document reads as an
    oversight.

11. **[MEDIUM] State the top-5 reading.** One sentence in README §1: CHALLENGE §5 says "top 5
    predicted allosteric **sites** (residue indices)"; the protocol reads that as five residues
    from one site, per CHALLENGE §8; under the other reading `site_pocket_rank` is the closer
    artifact. Add specificity to §3.3's omission list with the k = 5 reason.

12. **[MEDIUM] Adopt a named benchmarking standard in the report.** Weber et al.
    (doi:10.1186/s13059-019-1738-8) is the on-point checklist and is absent from the evidence
    base. Add Boulesteix et al. on neutrality (doi:10.1371/journal.pone.0061562), Nießl et al. on
    design multiplicity (doi:10.1002/widm.1441), Kapoor & Narayanan on leakage
    (doi:10.1016/j.patter.2023.100804), and the DOME Data/Evaluation axes
    (doi:10.1038/s41592-021-01205-4, doi:10.1093/gigascience/giae094).

13. **[LOW] Update the evidence base.** Replace the kinase-pLM row with the published values
    (doi:10.1021/acs.jctc.6c00427: ALLO AUROC 0.705, AUPR 0.061, prevalence 2.96 %, 8,140 /
    267,118) and flag the discrepancy with the previously recorded 0.676 / 0.077 / 3.22 %. Close
    three DOI flags: RBO doi:10.1145/1852102.1852106, Burt et al. doi:10.1016/j.neuroimage.2020.117038,
    DOME doi:10.1038/s41592-021-01205-4. Add CAPASP's full citation and verbatim abstract, and the
    six new 2025–2026 sources in §1.

14. **[LOW] Record that CASP dropped the category.** CASP16 (2024) has no function-prediction
    category; the last community blind assessment of binding-site residues is CASP10 (2014,
    doi:10.1002/prot.24495). This strengthens §12's rebuttal 1 and raises CAPASP's weight.

15. **[LOW] Replace the RBO omission reason.** "No use in this literature" is a popularity
    argument and violates R1. The first-principles reason is that overlap@5 already delivers
    top-weighting at the shipped k (doi:10.1145/1852102.1852106).

16. **[LOW] c-Myc.** `1NKP` is 1 of the 4 minimum deliverables and has no arm in any freeze.
    Either write the ADR that supersedes ADR 0020, or state in the report that the target is
    delivered without a scored endpoint because no ground-truth structure exists (CHALLENGE §6
    says it is judged by consensus and docking viability).

**Not recommended, and why.** Do not add accuracy, DVO, BEDROC, RIE or enrichment factor: the
stated reasons hold and no source compels them. Do not add a residue-level bootstrap: the
exchangeability objection is correct. Do not replace the matched-patch null: four repairs have
been tested and the calibration is disclosed, and swapping in an undemonstrated construction after
the freeze would be a larger fault than the residual it fixes.

---

## Bibliography

Every DOI below resolved or was fetched in this session unless marked otherwise.

### Retrieved this session

- Ai Y, Li H, Huang X, Liu S. A systematic evaluation of protein allosteric site prediction tools
  with independent datasets. _J Comput Aided Mol Des_ 40(1):122, 2026.
  doi:10.1007/s10822-026-00831-4
- Bazinet V, Liu Z-Q, Misic B. The effect of spherical projection on spin tests for brain maps.
  _Imaging Neuroscience_ 3, 2025. doi:10.1162/imag.a.118
- Benavoli A, Corani G, Mangili F. Should we really use post-hoc tests based on mean-ranks?
  _J Mach Learn Res_ 17:1–10, 2016. arXiv:1505.02288, doi:10.48550/arXiv.1505.02288
- Boulesteix A-L, Lauer S, Eugster MJA. A plea for neutral comparison studies in computational
  sciences. _PLoS ONE_ 8(4):e61562, 2013. doi:10.1371/journal.pone.0061562
- Buchka S, Hapfelmeier A, Gardner PP, Wilson R, Boulesteix A-L. On the optimistic performance
  evaluation of newly introduced bioinformatic methods. _Genome Biol_ 22:152, 2021.
  doi:10.1186/s13059-021-02365-4
- Burt JB, Helmer M, Shinn M, Anticevic A, Murray JD. Generative modeling of brain maps with
  spatial autocorrelation. _NeuroImage_ 220, 2020. doi:10.1016/j.neuroimage.2020.117038
- Collins GS, Moons KGM, Dhiman P, et al. TRIPOD+AI statement: updated guidance for reporting
  clinical prediction models that use regression or machine learning methods. _BMJ_ 385:e078378, 2024. doi:10.1136/bmj-2023-078378
- DeLong ER, DeLong DM, Clarke-Pearson DL. Comparing the areas under two or more correlated
  receiver operating characteristic curves: a nonparametric approach. _Biometrics_ 44(3):837–845, 1988. doi:10.2307/2531595
- Demšar J. Statistical comparisons of classifiers over multiple data sets. _J Mach Learn Res_
  7:1–30, 2006. **[NO DOI — JMLR does not mint DOIs]**; `jmlr.org/papers/v7/demsar06a.html`
- Ehrt C, Brinkjost T, Koch O. A benchmark driven guide to binding site comparison: an exhaustive
  evaluation using tailor-made data sets (ProSPECCTs). _PLOS Comput Biol_ 14(11), 2018.
  doi:10.1371/journal.pcbi.1006483 **[metadata only; not read at full text]**
- Kapoor S, Narayanan A. Leakage and the reproducibility crisis in machine-learning-based science.
  _Patterns_ 4, 2023. doi:10.1016/j.patter.2023.100804
- Koussis NC, Pang JC, Phogat R, Jeganathan J, Paton B, Fornito A, Robinson PA, Misic B,
  Breakspear M. Generation of surrogate brain maps preserving spatial autocorrelation through
  random rotation of geometric eigenmodes. _Imaging Neuroscience_ 3, 2025. doi:10.1162/IMAG.a.71
- Mandujano Reyes JF. Statistical methods for multiple language model comparison on a shared
  evaluation. arXiv:2608.22659, 2026.
- Markello RD, Misic B. Comparing spatial null models for brain maps. _NeuroImage_ 236, 2021.
  doi:10.1016/j.neuroimage.2021.118052
- Nießl C, Herrmann M, Wiedemann C, Casalicchio G, Boulesteix A-L. Over-optimism in benchmark
  studies and the multiplicity of design and analysis options when interpreting their results.
  _WIREs Data Min Knowl Discov_ 12, 2021/2022. doi:10.1002/widm.1441
- Riedlová K, Škrhák V, Gatlin WG, Ludwick M, Turano L, Novotný M, Hoksza D, Verkhivker GM.
  Predicting and decoding allosteric binding sites using protein language models and
  structure-based machine learning. _J Chem Theory Comput_ 22(10):5326–5347, 2026.
  doi:10.1021/acs.jctc.6c00427; preprint doi:10.64898/2026.01.05.697819
- Škrhák V, Polák L, Novotný M, Hoksza D. Seq2Pocket: augmenting protein language models for
  spatially consistent binding site prediction. bioRxiv, 2026. doi:10.64898/2026.01.28.702257
- Attafi OA, Clementel D, Kyritsis K, et al. DOME Registry: implementing community-wide
  recommendations for reporting supervised machine learning in biology. _GigaScience_ 13, 2024.
  doi:10.1093/gigascience/giae094
- UniSite: the first cross-structure dataset and learning framework for end-to-end ligand binding
  site detection. NeurIPS 2025. arXiv:2506.03237, doi:10.48550/arXiv.2506.03237
- Walsh I, Fishman D, Garcia-Gasulla D, Titma T, Pollastri G, ELIXIR ML Focus Group. DOME:
  recommendations for supervised machine learning validation in biology. _Nat Methods_
  18:1122–1127, 2021. doi:10.1038/s41592-021-01205-4
- Weber LM, Saelens W, Cannoodt R, et al. Essential guidelines for computational method
  benchmarking. _Genome Biol_ 20:125, 2019. doi:10.1186/s13059-019-1738-8
- Webber W, Moffat A, Zobel J. A similarity measure for indefinite rankings. _ACM Trans Inf Syst_
  28(4):20, 2010. doi:10.1145/1852102.1852106
- Zhang J, Sun X, Wu Z, Su J, Zhang X, Li C. AlloEF: an ensemble model for protein allosteric site
  identification based on transfer entropy and energetic frustration. _J Phys Chem B_
  130(19):4970–4981, 2026. doi:10.1021/acs.jpcb.6c00242
- The AIMe registry for artificial intelligence in biomedical research. _Nat Methods_
  18:1128–1131, 2021. doi:10.1038/s41592-021-01241-0
- LIGYSIS-web: a resource for the analysis of protein-ligand binding sites. _Nucleic Acids Res_
  53(W1):W351, 2025. doi:10.1093/nar/gkaf411
- Assessment of pharmaceutical protein–ligand pose and affinity predictions in CASP16.
  _Proteins_, 2025. doi:10.1002/prot.70061
- A quantum framework for protein binding-site structure prediction on utility-level quantum
  processors. _Adv Sci_, 2026. doi:10.1002/advs.202513641; preprint arXiv:2506.22677
  **[metadata only; not read at full text]**

### Verified at source this session (allosteric / cryptic prediction)

- AlloPred. doi:10.1186/s12859-015-0771-1
- APOP. doi:10.1093/bioinformatics/btad275
- PocketMiner. doi:10.1038/s41467-023-36699-3
- CryptoBench. doi:10.1093/bioinformatics/btae745
- DeepAllo. doi:10.1093/bioinformatics/btaf294
- STINGAllo. doi:10.1093/bib/bbaf424
- Allo-PED / AlloPED. doi:10.1101/2025.03.28.645953
- Allo-Allo. doi:10.1101/2024.09.28.615583
- Eccleston & Furnham. doi:10.1101/2025.06.27.662060

### Carried from `../evidence/evaluation-metrics.md` at the tag recorded there

PASS `10.1023/A:1008124202956`; Q-SiteFinder `10.1093/bioinformatics/bti315`; LIGSITEcsc
`10.1186/1472-6807-6-19`; PocketPicker `10.1186/1752-153X-1-7`; fpocket `10.1186/1471-2105-10-168`;
BDT `10.1093/bioinformatics/btq543`; Panjkovich & Daura `10.1186/1471-2105-13-273`; Allosite
`10.1093/bioinformatics/btt399`; SPACER `10.1093/nar/gkt460`; COACH `10.1093/bioinformatics/btt447`;
PARS `10.1093/bioinformatics/btu002`; CASP10 `10.1002/prot.24495`; CryptoSite
`10.1016/j.jmb.2016.01.029`; Amor et al. `10.1038/ncomms12477`; DeepSite
`10.1093/bioinformatics/btx350`; AllositePro `10.1021/acs.jcim.7b00014`; STRESS
`10.1016/j.str.2016.03.008`; P2Rank `10.1186/s13321-018-0285-8`; Tee et al.
`10.1371/journal.pcbi.1006228`; Ohm `10.1038/s41467-020-17618-2`; ESSA `10.1016/j.csbj.2020.06.020`;
Kalasanty `10.1038/s41598-020-61860-z`; PASSer v1 `10.1088/2632-2153/abe6d6`; ProteinLens
`10.1093/nar/gkab350`; Wu et al. `10.1016/j.patter.2021.100408`; PUResNet
`10.1186/s13321-021-00547-7`; PASSer2.0 `10.3389/fmolb.2022.879251`; PASSer (NAR)
`10.1093/nar/gkad303`; PASSerRank `10.48550/arXiv.2302.01117`; KeyAlloSite `10.7554/eLife.81850`;
SiteFerret `10.1021/acs.jctc.2c01306`; MEF-AlloSite `10.1186/s13321-024-00882-5`; LIGYSIS-bench
`10.1186/s13321-024-00923-z`; Mariano et al. `10.1016/j.csbj.2024.10.036`; AlloBench
`10.1021/acsomega.5c01263`; ZHMolEReP `10.1021/acs.jcim.6c00141`; AllosES
`10.1021/acs.jcim.4c00544`; Allofusion `10.1021/acs.jcim.5c01033`; CTQW `10.1021/jacs.6c08053`;
Erman `10.1088/1478-3975/ae3e49`; Guharoy & Chakrabarti `10.1186/1471-2105-11-286`; Milenković
et al. `10.1371/journal.pone.0005967`; Thayer et al. `10.1371/journal.pone.0188616`; Saito &
Rehmsmeier `10.1371/journal.pone.0118432`; McDermott et al. `arXiv:2401.06091`; Davis & Goadrich
`10.1145/1143844.1143874`; Chicco & Jurman `10.1186/s13040-023-00322-4`; PNAS hinge sites
`10.1073/pnas.2414333121`; Utgés et al. `10.1038/s42003-024-05970-8`; Wankowicz
`10.1371/journal.pcbi.1013094`; membrane benchmark `10.1021/acs.jcim.5c00336`; pyKVFinder
`10.1186/s12859-021-04519-4`; Gfeller & De Los Rios `10.1103/PhysRevLett.99.038701`; Zheng &
Tekpinar `10.1186/1472-6807-9-45`; Motlagh et al. `10.1038/nature13001`; Krojer et al.
`10.1016/j.sbi.2020.08.004`; Kozakov et al. `10.1021/acs.jmedchem.5b00586`; Vajda et al.
`10.1016/j.cbpa.2018.05.003`; Gašparíková et al. `10.1093/bioadv/vbaf156`; apo/holo detector
comparison `10.1038/s41598-020-72906-7`.

### Explicitly not established

- Whether eigenmode-rotation surrogates transfer to a residue contact graph. No protein
  demonstration found. **[NOT ESTABLISHED]**
- CAPASP's per-tool numbers and dataset sizes. Springer paywall. **[NOT ESTABLISHED]**
- Whether AlloEF's transfer entropy derives from MD trajectories or from an elastic network
  model — relevant to C2. ACS 403. **[NOT ESTABLISHED]**
- A published convention for scoring a bare top-N **residue** list in allosteric-site prediction.
  Both 2026 candidates convert residues to sites first. **[NOT ESTABLISHED]**
- Whether CASP formally retired the FN category or merely did not run it in CASP16. The CASP16
  category list contains no FN entry; no retirement statement was found. **[NOT ESTABLISHED]**
