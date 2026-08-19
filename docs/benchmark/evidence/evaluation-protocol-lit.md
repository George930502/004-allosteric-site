# Evaluation protocol — literature evidence

Retrieved 2026-08-20. Purpose: stress-test the pre-registered scoring protocol for the
allosteric-residue benchmark before any method exists (`docs/benchmark/manifest.yaml`,
Phase 1.6 of `docs/ROADMAP.md`).

## Evidence rules applied here

Every claim carries a DOI and a verification tag:

- `[VERIFIED-FULLTEXT]` — I read the open-access full text this session via
  `https://www.ebi.ac.uk/europepmc/webservices/rest/<PMCID>/fullTextXML`.
- `[VERIFIED-ABSTRACT]` — I read only the Europe PMC `core` record (title + abstract).
  The paper is closed-access or I did not spend a fetch on it.
- `[UNVERIFIED]` — reasoning or arithmetic of mine, not taken from a retrieved source.
  Treat as a hypothesis to check in-repo, not as evidence.

Nothing in this file is recalled from memory. Where a number was wanted and could not be
retrieved, it appears in §5 "Not established" instead of being reconstructed.

---

## 0. Summary of the refutation attempt

| Our provisional choice                    | Verdict from retrieved literature                                                                                                                                                                                   |
| ----------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| AUC-ROC as effect size                    | **Weakened.** Same-predictor, same-data pairs in this exact domain show ROC-AUC 0.86 with AUPRC 0.36, and 0.83 with PR-AUC 0.44. Report both.                                                                       |
| Mann-Whitney U as the ranking test        | **Coherent but not independent** of AUC-ROC — it is the same statistic rescaled. The protocol currently has one view of the ranking, not two.                                                                       |
| Exact hypergeometric null for precision@5 | **No precedent found** in this field, for or against. Not refuted; also not standard.                                                                                                                               |
| Matched connected-patch null              | **Supported by adjacent fields, unprecedented in this one.** Strongest support is the protein-structure-network null-model literature: non-geometric nulls declare nearly everything significant on residue graphs. |
| Holm across compared methods              | **More conservative than any precedent found.** The one allosteric paper that ran significance tests ran many uncorrected t-tests.                                                                                  |
| No pooled cross-target p-value            | **Supported, but the field does something different**: it pools _residues/pockets_ across all targets into one AUC. That is data pooling, and it is the norm.                                                       |

---

## 1. Metrics the field actually reports

### 1.1 Residue-level classification metrics

**PocketMiner** reports both ROC-AUC and PR-AUC for residue-level cryptic-pocket
prediction: "Across the 5 splits, the best GVP-GNN model achieves an average test PR-AUC
of 0.44 ± 0.12 (average ROC-AUC: 0.83 ± 0.04)"; the 3D-CNN comparator gives "PR-AUC: 0.41
± 0.05; ROC-AUC: 0.79 ± 0.02". On the held-out experimental set it reports "ROC-AUC: 0.87"
(10.1038/s41467-023-36699-3) `[VERIFIED-FULLTEXT]`

**CryptoBench** defines and reports AUC, AUPRC, accuracy, TPR, FPR, MCC and F1 at the
residue level. Its pLM-NN model on the CB-full test set: AUC 0.86, AUPRC 0.36, ACC 0.93,
FPR 0.05, TPR 0.48, MCC 0.39, F1 0.92 (10.1093/bioinformatics/btae745)
`[VERIFIED-FULLTEXT]`

**MEF-AlloSite** reports Average Precision (i.e. AUC-PR) and ROC AUC at the pocket level,
plus precision / recall / F1 at top-1 (10.1186/s13321-024-00882-5) `[VERIFIED-FULLTEXT]`

**DeepAllo** reports F1, precision and recall only, and explicitly declines to lead with
accuracy: "As the dataset is highly imbalanced, the performance was evaluated using F1
score mainly but also keeping in mind Precision and Recall." No AUC-ROC or AUC-PR is
reported at all (10.1093/bioinformatics/btaf294) `[VERIFIED-FULLTEXT]`

### 1.2 Rank-cutoff / success-rate metrics (the dominant convention for site prediction)

**P2Rank** defines the standard protocol: "We use Top-n and Top-(n+2) rank cutoffs where n
is the number of relevant ligands in the evaluated target protein structure (for proteins
with only one ligand this corresponds to the usual Top-1 and Top-3 cutoffs)."
(10.1186/s13321-018-0285-8) `[VERIFIED-FULLTEXT]`

**PASSer**: "84.9% of allosteric pockets in the test set appeared in the top 3 positions"
(10.1088/2632-2153/abe6d6) `[VERIFIED-ABSTRACT]`
**PASSer2.0**: "82.7% of allosteric pockets appearing among the top three positions"
(10.3389/fmolb.2022.879251) `[VERIFIED-ABSTRACT]`
**PASSer** (web-server update, NAR 2023): 10.1093/nar/gkad303 `[VERIFIED-ABSTRACT]`
**DeepAllo**: "90.5% of allosteric pockets in the top 3 positions", and "90% of positive
or predicted allosteric pockets ... are ranked in top 10% of the results"
(10.1093/bioinformatics/btaf294) `[VERIFIED-FULLTEXT]`

This is the closest analogue in the literature to our precision@5. Note it is a _pocket_
rank cutoff, not a residue rank cutoff.

### 1.3 DCC

**P2Rank** uses "DCC (distance between the center of the pocket and any ligand atom)
pocket identification criterion with 4 Å threshold" (10.1186/s13321-018-0285-8)
`[VERIFIED-FULLTEXT]` — **caveat**: the retrieved text labels this DCC while describing a
centre-to-_any-ligand-atom_ distance, which is conventionally DCA. Do not copy this
definition into our harness without re-reading the source. See §5.

A 2024 allosteric-site ML paper reports "78% DCC success rate, 60% overall DCC, 64% F1
score and 64% MCC" (10.1016/j.csbj.2024.10.036) `[VERIFIED-ABSTRACT, attribution
uncertain]` — the same numeric string was mis-attributed to CryptoBench by one search
summariser; CryptoBench's own full text reports entirely different values (§1.1), so the
numbers belong to the CSBJ paper. Confirm before citing.

### 1.4 True/false positive rate pairs

**CryptoSite**: "for our benchmark, the true positive and false positive rates are 73% and
29%, respectively" (10.1016/j.jmb.2016.01.029) `[VERIFIED-ABSTRACT]` — paper is not open
access; nothing beyond the abstract is reachable.

**Ohm** reports TPR and PPV only: "The average TPR of Ohm is 0.57, compared to 0.23 of
Amor's method"; "The PPV of Ohm is 0.72, compared to 0.48 of Amor's method"
(10.1038/s41467-020-17618-2) `[VERIFIED-FULLTEXT]`

### 1.5 Enrichment factor

**Not found** in any allosteric- or cryptic-site paper I retrieved. The only enrichment
language I saw was virtual-screening enrichment against decoy _ligands_ in DUD-E
(10.1021/jm300687e) `[VERIFIED-ABSTRACT]`, which is a different quantity. See §5.

---

## 2. Null models — what each paper compares against

**This is the headline finding: the allosteric- and cryptic-site prediction literature I
read does not use a statistical null model at all.** Not a matched one, not a uniform
random one. Methods are compared to other methods, point estimate against point estimate.

| Paper                                        | Negative set                                                              | Statistical null / test                   | Spatial autocorrelation addressed?  |
| -------------------------------------------- | ------------------------------------------------------------------------- | ----------------------------------------- | ----------------------------------- |
| PocketMiner (10.1038/s41467-023-36699-3)     | Curated _hard negatives_                                                  | None                                      | No                                  |
| CryptoBench (10.1093/bioinformatics/btae745) | All non-binding residues                                                  | None                                      | No (only sequence-homology leakage) |
| DeepAllo (10.1093/bioinformatics/btaf294)    | All non-allosteric FPocket pockets (definition not stated)                | None                                      | No                                  |
| MEF-AlloSite (10.1186/s13321-024-00882-5)    | Pockets with no allosteric-modulator-binding residue, undersampled to 1:5 | Student's t-test + Cohen's d, uncorrected | No                                  |
| Ohm (10.1038/s41467-020-17618-2)             | n/a                                                                       | None                                      | No                                  |
| P2Rank (10.1186/s13321-018-0285-8)           | n/a                                                                       | None                                      | No                                  |

Supporting quotes:

- PocketMiner's negatives are curated, not random and not matched: "we only used residues
  from proteins known to be extremely rigid or extremely stable or residues from proteins
  that have been put through extensive drug screens"; they additionally "identified
  proteins that had been the subjects of extensive drug screens and pulled out residues
  where ligands did not bind" and "removed any residues that were the sites of cryptic
  pocket opening in simulation". No statistical tests, p-values, permutation tests or null
  models are reported anywhere in the paper. (10.1038/s41467-023-36699-3)
  `[VERIFIED-FULLTEXT]`
- CryptoBench: negatives are simply all non-binding residues; "binding residues only
  correspond to less than 5% of all residues in the whole protein". No significance
  testing. Its only leakage control is sequence-based: "To mitigate the risk of including
  homologous proteins in different splits, causing information leakage, we conducted
  another round of clustering on the dataset ... a threshold of 10% sequence identity."
  (10.1093/bioinformatics/btae745) `[VERIFIED-FULLTEXT]`
- MEF-AlloSite is the _only_ retrieved allosteric paper running a significance test:
  "Student's t test and Cohen's D value have been used to evaluate the average precision
  and ROC AUC score distribution", one-sided, α = 0.05, with **no correction for multiple
  comparisons**. (10.1186/s13321-024-00882-5) `[VERIFIED-FULLTEXT]`
- Ohm compares only to other published methods; "No p-values, permutation tests, or formal
  statistical significance statements are reported." (10.1038/s41467-020-17618-2)
  `[VERIFIED-FULLTEXT]`

**Consequence for us:** our matched-patch null has no precedent in this literature to copy
and no precedent to contradict it. If we ship it, it is more rigorous than every method
paper cited above. It also means we cannot calibrate our expected p-values against
anything published — there is nothing to calibrate against.

### 2.1 Spatial autocorrelation — the two sources that do address it

Neither is from the allosteric field, and both support the patch null.

**Guharoy & Chakrabarti 2010, BMC Bioinformatics** (10.1186/1471-2105-11-286)
`[VERIFIED-FULLTEXT]` — the direct empirical measurement of the effect we are worried
about.

- Surface patches defined by nearest-neighbour growth in space: "Each surface residue
  (represented by its center of mass) was taken in turn and all the other surface residues
  within a fixed radius were selected" — 15 Å for complexes, 22 Å for homodimers, chosen
  as half the average maximum interface dimension (30 Å / 44 Å). A refinement adds "vector
  constraints ... to avoid generating surface patches that include residues from 'opposite
  sides' of a protein molecule."
- Null construction: "subsets of residues (of the same size as the number of conserved
  residues) were selected randomly" from the same interface, with "average (and SD) of the
  M_s values calculated for 1000 random subsets".
- Result — the magnitude of the spatial-clustering effect: "In 96.7% (117/121)
  homodimeric and 87.7% (341/389) protein complex interfaces, randomly selected groups of
  residues were indeed less clustered" (P < 0.01). Overall significance by **Mann-Whitney
  U** (non-parametric): homodimers P = 1.57e-04, complexes P = 9.64e-14.
- Prediction performance, top 10% of ranked patches: 65/121 (53.7%) homodimers, 189/389
  (48.6%) complexes, 77/114 (67.5%) enzyme-inhibitor complexes. Almost 60% of experimental
  hot-spot residues (ΔΔG > 2 kcal/mol) fall in conserved clusters.

Read carefully: their _size-matched random subset_ null is exactly the null our patch null
is designed to replace, and their finding is that functionally labelled residues beat it
in ~90% of cases **by virtue of being clustered**. That is the confound quantified. They
used clustering as the signal; we would be treating it as the nuisance. Same phenomenon.

**Przulj et al., "Optimized null model for protein structure networks", PLoS ONE**
(10.1371/journal.pone.0005967) `[VERIFIED-FULLTEXT]` — the theoretical argument.

- Models compared on residue interaction graphs (RIGs): "Erdös-Rényi random graphs ('ER'),
  random graphs with same degree distribution as the RIGs ('ER-DD'), Barabási-Albert type
  scale free networks ('SF-BA'), and stickiness-index based networks ('STICKY')" versus 3D
  geometric random graphs.
- Result: "geometric random graphs, that model spatial relationships between objects,
  provide the best fit to RIGs", because "two objects that are close enough in space will
  interact, whereas two distant objects will not ... they are expected to mimic well the
  underlying nature of packed residues in a protein". GDD-agreement up to 0.85 for the
  largest protein (3eca), ~0.7 for smaller ones. "GEO-3D is the best-fitting null model
  for almost all RIGs with respect to all network properties."
- **The load-bearing quote for our design decision:** "all non-geometric models ... tend to
  identify as significantly (under-) over-represented almost all analyzed subgraphs",
  whereas "GEO-3D model exhibits the highest 'specificity' ... only 5–11 out of 29
  subgraphs ... are identified as (anti-)motifs". Conclusion: "The choice of a well-fitting
  null model is crucial."

This is the strongest published support for our matched-patch null that I retrieved: on
residue-contact graphs specifically, a null that ignores spatial embedding inflates
significance across the board. Our concern is not speculative.

---

## 3. Reported effect sizes and the sample sizes behind them

Use these to judge whether N = 3 targets can detect anything comparable.

| Source                                                             | Metric                  | Value                                                               | Sample size behind the number                                                                                                                                                     |
| ------------------------------------------------------------------ | ----------------------- | ------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| PocketMiner (10.1038/s41467-023-36699-3) `[VERIFIED-FULLTEXT]`     | ROC-AUC                 | 0.87                                                                | 38 apo-holo pairs / 39 cryptic pockets; test set = **563 positive residues, 1283 negative residues** from 24 apo structures + 4 hyper-rigid + 7 screened proteins                 |
| PocketMiner, same                                                  | ROC-AUC vs CryptoSite   | 0.87 vs 0.85                                                        | same set — a 0.02 head-to-head margin                                                                                                                                             |
| PocketMiner, cross-validation                                      | ROC-AUC / PR-AUC        | 0.83 ± 0.04 / 0.44 ± 0.12                                           | 5 splits; 37 proteins, 2400 MD simulations, 941,650 unique training examples                                                                                                      |
| CryptoBench (10.1093/bioinformatics/btae745) `[VERIFIED-FULLTEXT]` | AUC / AUPRC             | 0.86 / 0.36                                                         | 1107 structures (885 train / 222 test); 1361 cryptic pockets; 16.60 ± 7.22 binding residues per protein; positives < 5% of residues                                               |
| MEF-AlloSite (10.1186/s13321-024-00882-5) `[VERIFIED-FULLTEXT]`    | Average Precision       | 0.620 / 0.509 / 0.452                                               | Test 1: 56 proteins, 1510 pockets, 87 allosteric (5.762%). Test 2: 56 proteins, 2471 pockets, 88 allosteric (3.561%). Test 3: 122 proteins, 6384 pockets, 202 allosteric (3.164%) |
| MEF-AlloSite, same                                                 | ROC AUC                 | 0.803 vs 0.798                                                      | Tests 2 & 3; margin of 0.005 declared significant                                                                                                                                 |
| MEF-AlloSite, same                                                 | vs PASSer2.0, Test 1    | AP p = 3.43e-25, Cohen's d = 2.759; ROC AUC p = 1.16e-11, d = 1.512 | distribution over repeated runs, **not** over proteins — see caveat below                                                                                                         |
| DeepAllo (10.1093/bioinformatics/btaf294) `[VERIFIED-FULLTEXT]`    | F1 / precision / recall | 0.897 / 0.923 / 0.881                                               | 207 proteins, 4223 pockets total; test 42 proteins / 848 pockets / 15,567 residues; positives 304 pockets = 7.76%, **5.12% of residues**                                          |
| DeepAllo, same                                                     | top-3                   | 90.5%                                                               | same test set                                                                                                                                                                     |
| Ohm (10.1038/s41467-020-17618-2) `[VERIFIED-FULLTEXT]`             | TPR / PPV               | 0.57 / 0.72 (vs 0.23 / 0.48)                                        | **20 known allosteric proteins**; 147–3311 residues each                                                                                                                          |
| P2Rank (10.1186/s13321-018-0285-8) `[VERIFIED-FULLTEXT]`           | Top-n / Top-(n+2)       | 72.0% / 78.3%                                                       | COACH420, 420 single-chain structures                                                                                                                                             |
| P2Rank, same                                                       | Top-n / Top-(n+2)       | 68.6% / 74.0%                                                       | HOLO4K                                                                                                                                                                            |
| PASSer (10.1088/2632-2153/abe6d6) `[VERIFIED-ABSTRACT]`            | top-3                   | 84.9%                                                               | test-set size unknown                                                                                                                                                             |
| CryptoSite (10.1016/j.jmb.2016.01.029) `[VERIFIED-ABSTRACT]`       | TPR / FPR               | 73% / 29%                                                           | benchmark size unknown from abstract                                                                                                                                              |

Reference benchmark sizes: ASBench = "a core set with 235 different allosteric sites and
... a core-diversity set with 147 structurally varied allosteric sites"; ASD = "1949 target
entries" (10.1186/s13321-024-00882-5) `[VERIFIED-FULLTEXT]`

### 3.1 Power caveats a reader should not miss

- **The Cohen's d values above are not between-target effect sizes.** MEF-AlloSite's
  d = 2.759 is computed over a distribution of repeated runs on a fixed dataset, so its
  denominator is run-to-run variance, not protein-to-protein variance. It cannot be
  transferred to an N = 3 target design. `[VERIFIED-FULLTEXT]` for the method, `[UNVERIFIED]`
  for the inference.
- **PR-AUC is roughly 3x noisier than ROC-AUC** in the one paper that reports both with
  dispersion: ±0.12 vs ±0.04 across 5 splits (10.1038/s41467-023-36699-3)
  `[VERIFIED-FULLTEXT]`. If we adopt AUC-PR as a co-primary at N = 3, expect a wide
  interval.
- **Published head-to-head margins are small**: 0.02 ROC-AUC (PocketMiner vs CryptoSite),
  0.005 ROC AUC (MEF-AlloSite vs its own ablation). Detecting margins of that size across
  3 targets is arithmetically hopeless; our comparisons will need to be within-target.
  `[UNVERIFIED]` — inference from the two verified numbers.
- **At N = 3 no across-target paired non-parametric test can reach p < 0.05.** A two-sided
  sign test on 3 paired differences has minimum attainable p = 2/2^3 = 0.25. This is
  arithmetic, not a citation. `[UNVERIFIED — verify in-repo]` It independently supports the
  decision not to pool a cross-target p-value, but it also means the _only_ place inference
  can live is the within-target nulls. Those nulls therefore have to be right.

---

## 4. Evidence that CONTRADICTS our provisional choices

### 4.1 AUC-ROC as the effect size — contradicted, with in-domain examples

**General argument.** Saito & Rehmsmeier (10.1371/journal.pone.0118432) `[VERIFIED-FULLTEXT]`:

- Concrete paired numbers: MiRFinder on dataset T2 has ROC AUC 0.772 but PRC AUC 0.106;
  RNAmicro has ROC AUC 0.886 (the best ROC score in the comparison) but PRC AUC 0.054.
  "the ROC plot makes an innocent impression, the PRC plot reveals the bitter truth".
- Mechanism, stated in terms of the FPR denominator: "The point for the balanced case
  represents 160 FPs and 500 TPs ... In contrast, the same point for the imbalanced case
  represents 1,600 FPs and 500 TPs, and [ROC] fails to explicitly show this performance
  difference." Because FPR = FP/(TN+FP), inflating the negative class shrinks FPR for the
  same absolute number of false positives.
- Recommendation: PRC plots as "the most informative visual analysis tool" for imbalanced
  data, and PRC "can be useful in revealing the early-retrieval performance" — which is
  precisely the regime our precision@5 lives in.

**In-domain instances of the same gap, same predictor, same data:**

- CryptoBench: AUC 0.86 alongside AUPRC 0.36 (10.1093/bioinformatics/btae745)
  `[VERIFIED-FULLTEXT]`. It also spells out the operational consequence: "the high FPR
  combined with the imbalance between binding and non-binding residues could cause the
  number of false positives to significantly outnumber the true positives."
- PocketMiner: ROC-AUC 0.83 ± 0.04 alongside PR-AUC 0.44 ± 0.12
  (10.1038/s41467-023-36699-3) `[VERIFIED-FULLTEXT]`.

Our positive fraction will be in the same regime these papers describe — CryptoBench
"less than 5% of all residues", DeepAllo "5.12% positive labels"
(10.1093/bioinformatics/btae745, 10.1093/bioinformatics/btaf294) `[VERIFIED-FULLTEXT]`.

**Stronger form of the critique.** Chicco & Jurman argue ROC AUC should be replaced
outright: it "is generated including predictions that obtained insufficient sensitivity and
specificity" and "does not say anything about positive predictive value ... potentially
generating inflated overoptimistic results" (10.1186/s13040-023-00322-4)
`[VERIFIED-ABSTRACT]`. See also 10.1186/s13040-021-00244-z `[VERIFIED-ABSTRACT]`.

**Recommendation:** keep AUC-ROC (it is what the field reports, so it is what makes us
comparable) but demote it from sole effect size. Report AUC-PR alongside it, with the
positive-class prevalence stated per target, since AUC-PR's baseline is the prevalence and
is therefore not comparable across targets of different size.

### 4.2 Residue-level AUC as the framing — contradicted by P2Rank

P2Rank explicitly rejects residue-level classification metrics for binding-site prediction
in favour of a pocket-centric view: "We believe that pocket-centric point of view better
represents a common sense associated with LBS prediction, and as an evaluation methodology
awards those methods that fail to predict the least amount of potentially interesting
binding sites." The authors argue residue-level MCC/AUC/F-measure set up conflicting
objectives and penalise a correctly sized pocket that happens to contain non-contact
residues (10.1186/s13321-018-0285-8) `[VERIFIED-FULLTEXT]`.

This is a real challenge to our whole framing, not just to one metric. The entire
PASSer / DeepAllo / MEF-AlloSite line evaluates at pocket rank, not residue rank
(10.1088/2632-2153/abe6d6, 10.1093/bioinformatics/btaf294, 10.1186/s13321-024-00882-5).
Our deliverable is a _residue_ hit list, so residue-level scoring is the honest match to
the artifact — but we should state that choice and its cost explicitly rather than let a
reviewer find it.

### 4.3 AUC-ROC and Mann-Whitney U are not two pieces of evidence

The normalised Mann-Whitney U statistic equals the AUC-ROC. Using one as the test and the
other as the effect size gives a single view of the ranking, not a corroborated one.
`[UNVERIFIED — no DOI retrieved for this identity; confirm by simulation in-repo, it is a
five-line check.]` If a second, independent view is wanted, it must come from a different
functional (e.g. a top-heavy statistic such as precision@5 under the patch null, which the
protocol already has).

### 4.4 Pooling across targets — the field does pool, just not p-values

Every multi-protein evaluation retrieved computes one AUC/AP over residues or pockets
**pooled across all proteins**: MEF-AlloSite's AP over 1510–6384 pockets from 56–122
proteins (10.1186/s13321-024-00882-5), CryptoBench's AUC over 222 test structures
(10.1093/bioinformatics/btae745), PocketMiner's ROC-AUC over 563 + 1283 residues from 35
structures (10.1038/s41467-023-36699-3). All `[VERIFIED-FULLTEXT]`. None reports a
per-protein distribution as the primary result. I found **no paper that pools p-values**
across targets and no paper that justifies a small-N design. So our "no pooled p-value" is
not contradicted; what is contradicted is the implied premise that the field avoids
pooling. It pools the data, which is a stronger and less examined move (larger proteins
dominate the pooled AUC; MEF-AlloSite even notices the size effect — "The presence of more
negative samples in larger proteins within the dataset guarantees an imbalanced
representation of different protein sizes" `[VERIFIED-FULLTEXT]`).

### 4.5 Holm correction — no support, no opposition, and we would be ahead of the field

MEF-AlloSite runs multiple one-sided t-tests across three test sets and several
competitors with no multiple-comparison correction (10.1186/s13321-024-00882-5)
`[VERIFIED-FULLTEXT]`. No retrieved paper applies Holm, Bonferroni or FDR to method
comparison in this domain. Nothing refutes our choice; nothing supports it either.

---

## 5. Not established — questions I could not answer from a source I read

Each entry names the specific number wanted and why it is unreachable.

1. ~~**CryptoSite per-feature AUC values.**~~ **CLOSED** -- see the addendum at the end of
   this file. Full text was retrieved by a route not tried here (NCBI `efetch` over `db=pmc`,
   which serves PMC full text even when Europe PMC reports `isOpenAccess: N`).
2. ~~**CryptoSite benchmark size.**~~ **CLOSED** -- see the addendum.
3. **Whether any allosteric- or cryptic-site paper uses a spatially matched / contiguous
   patch null.** I found none across six full texts and five Europe PMC searches. Absence
   of evidence, not evidence of absence — I cannot claim the field has never done it.
4. **Enrichment factor for allosteric residue prediction.** Wanted: a definition and a
   reported EF value with its baseline. Found EF only in ligand virtual-screening contexts
   (10.1021/jm300687e, abstract only). No residue-level EF retrieved.
5. **Precedent for an exact hypergeometric null on precision@k in structural
   bioinformatics.** Searched, none retrieved. Unknown whether this is standard, novel, or
   quietly avoided for a reason.
6. **Precedent for pooling p-values across targets at small N, and any justification.**
   None retrieved.
7. **Between-target variance of AUC for allosteric prediction.** Wanted: SD of per-protein
   AUC across a benchmark, which is the number that actually sets our power at N = 3.
   PocketMiner's ±0.04 is across cross-validation splits, not across targets
   (10.1038/s41467-023-36699-3). No paper retrieved reports a per-protein AUC distribution.
   **This is the single most important missing number for our design.**
8. **Exact DCC definition and threshold used by CryptoBench** for its DCC success rate.
   The full-text extraction gave AUC/AUPRC/MCC/F1 but no DCC threshold.
9. **DCC vs DCA in P2Rank.** The retrieved text labels a centre-to-any-ligand-atom
   distance as "DCC" with a 4 Å threshold. Conventionally that is DCA. Which the paper
   actually means was not resolved; re-read 10.1186/s13321-018-0285-8 before implementing.
10. **DeepAllo's negative-pocket definition.** The full text states ~20 FPocket pockets per
    protein but never says whether negatives are all non-allosteric pockets, a random
    subset, or size-matched (10.1093/bioinformatics/btaf294).
11. **PASSer test-set size.** The 84.9% top-3 figure has no denominator in the abstract and
    the paper is not open access (10.1088/2632-2153/abe6d6).
12. **Attribution of the "78% DCC / 60% / 64% F1 / 64% MCC" figures.** Almost certainly
    10.1016/j.csbj.2024.10.036, but one search summariser attached them to CryptoBench,
    whose full text disagrees. Not read in full text; treat as provisional.
13. **Whether AUC-PR has been argued as preferable specifically for allosteric residue
    prediction.** The arguments retrieved are general (10.1371/journal.pone.0118432,
    10.1186/s13040-023-00322-4) or domain-adjacent (10.1093/bioinformatics/btae745). No
    allosteric-specific argument found.
14. **A DOI-backed precedent for random-surface-patch nulls in binding-site prediction.** A
    web search surfaced strong hints (random surface patches as controls; score reshuffling
    over residues before patch extraction) but returned no attributable source I could
    retrieve — the one candidate, Nucleic Acids Research 10.1093/nar/gkl454, redirects to a
    token-gated PDF host. Recorded as a lead, not as evidence.

---

## Bibliography

Sorted by verification level.

**Full text read this session:**

- Meller A. et al. Predicting locations of cryptic pockets from single protein structures
  using the PocketMiner graph neural network. _Nat Commun_ 2023. doi:10.1038/s41467-023-36699-3
- Vít Škrhák et al. CryptoBench: cryptic protein-ligand binding sites dataset and benchmark.
  _Bioinformatics_ 2024. doi:10.1093/bioinformatics/btae745
- DeepAllo: allosteric site prediction using protein language model with multitask learning.
  _Bioinformatics_ 2025. doi:10.1093/bioinformatics/btaf294
- MEF-AlloSite: an accurate and robust Multimodel Ensemble Feature selection for the
  Allosteric Site identification model. _J Cheminform_ 2024. doi:10.1186/s13321-024-00882-5
- Wang J. et al. Mapping allosteric communications within individual proteins (Ohm).
  _Nat Commun_ 2020. doi:10.1038/s41467-020-17618-2
- Krivák R., Hoksza D. P2Rank: machine learning based tool for rapid and accurate prediction
  of ligand binding sites from protein structure. _J Cheminform_ 2018. doi:10.1186/s13321-018-0285-8
- Optimized null model for protein structure networks. _PLoS ONE_ 2009. doi:10.1371/journal.pone.0005967
- Guharoy M., Chakrabarti P. Conserved residue clusters at protein-protein interfaces and
  their use in binding site identification. _BMC Bioinformatics_ 2010;11:286.
  doi:10.1186/1471-2105-11-286
- Saito T., Rehmsmeier M. The precision-recall plot is more informative than the ROC plot
  when evaluating binary classifiers on imbalanced datasets. _PLoS ONE_ 2015.
  doi:10.1371/journal.pone.0118432

**Abstract only:**

- Cimermancic P. et al. CryptoSite. _J Mol Biol_ 2016. doi:10.1016/j.jmb.2016.01.029 (closed)
- PASSer: Prediction of Allosteric Sites Server. _Mach Learn Sci Technol_ 2021.
  doi:10.1088/2632-2153/abe6d6 (closed)
- PASSer2.0. _Front Mol Biosci_ 2022. doi:10.3389/fmolb.2022.879251
- PASSer: fast and accurate prediction of protein allosteric sites. _NAR_ 2023. doi:10.1093/nar/gkad303
- Protein allosteric site identification using machine learning and per amino acid residue
  reported internal protein nanoenvironment descriptors. _CSBJ_ 2024. doi:10.1016/j.csbj.2024.10.036
- Chicco D., Jurman G. The Matthews correlation coefficient (MCC) should replace the ROC AUC
  as the standard metric. _BioData Min_ 2023. doi:10.1186/s13040-023-00322-4
- Chicco D. et al. MCC more reliable than balanced accuracy. _BioData Min_ 2021. doi:10.1186/s13040-021-00244-z
- Mysinger M. et al. DUD-E. _J Med Chem_ 2012. doi:10.1021/jm300687e


---

## Addendum — CryptoSite full text retrieved (closes unknowns 1 and 2)

Retrieved after this review was written, via `efetch.fcgi?db=pmc&id=4794384&retmode=xml`,
which returns the complete author manuscript (111 kB) even though Europe PMC reports
`isOpenAccess: N` and its `fullTextXML` endpoint 404s. The Europe PMC OA flag describes the
bulk-download licence subset, not PMC availability. All values below are
`[VERIFIED-FULLTEXT]` from that retrieval.

### The AUC ladder (unknown 1)

| Configuration | AUC |
|---|---:|
| MD-derived average pocket score, best single feature | 0.73 |
| 30 crystal-structure features combined | 0.74 |
| + sequence conservation (2nd selected feature) | 0.74 |
| + small-molecule fragment-binding likelihood (3rd) | 0.77 |
| Full SVM model (quadratic kernel, 3 selected features) | **0.83** |
| MD-free fast variant, ~1000x speedup | **0.74** |

Two readings matter for this repo. First, **a single MD-derived feature (0.73) is worth about
as much as thirty crystal-structure features combined (0.74)** -- the dynamics carry
information the static structure does not, which is the premise our own method depends on.
Second, **dropping MD entirely costs 0.83 -> 0.74**. C2 forbids MD outright, so 0.74 is the
honest reference point for what a strong non-MD method achieves on cryptic-site localisation,
and 0.83 is a ceiling we are constitutionally barred from reaching by their route.

### Dataset composition (unknown 2)

84 cryptic binding sites, 92 binding pockets and **705 concave surface patches**, from the PDB
and Binding MOAD. Training used leave-one-out cross-validation over the 84 cryptic sites
(79 proteins); the held-out test set is **14 apo structures**. Recall 96 % at sensitivity
> 33 %, 88 % at sensitivity > 50 %.

### Correction to section 2 of this file

This review reported that no allosteric/cryptic-site paper uses a matched patch comparison.
That was true of the six full texts it could read, but **CryptoSite is a counterexample it
could not reach**: the 705 concave surface patches are exactly such a matched class, compared
against cryptic sites and binding pockets with p-values (pocket score 0.07 vs 0.42,
P = 1.7e-31; protruding atoms 170 vs 183, P = 8.0e-3; convexity 2.4 vs 1.9, P = 0.8), and the
paper also states a random-residue baseline (19 residues tested at random to find one true
cryptic residue). The narrower claim survives and is the one now in `../README.md` section 5:
patches are used there to characterise what cryptic sites *are*, not as a permutation null
calibrating what a predictor *scores*.

### An internal inconsistency in the paper

The abstract reports "true positive and false positive rates are 73 % and 29 %"; the body
reports "79 % and 29 % at the residue score threshold of 0.05". Both quoted verbatim. Cite the
body figure with its threshold, or the abstract figure as the abstract's -- but not
interchangeably.

### Still unreachable

The SI Text, which holds the ligand size floor, the ion policy, the resolution cutoff and the
definition of the 705 concave patches. PMC now gates supplementary binaries behind a
JavaScript proof-of-work challenge (`pow-*.js`), which a plain HTTP client cannot satisfy;
Europe PMC's `supplementaryFiles` endpoint refuses with "not open access"; the Sali lab site
and `github.com/salilab/cryptosite` publish the predictor and its fragment set, not the pair
list. Ligand policy is nonetheless partly recoverable, because the Methods name **Binding
MOAD** as the ligand source -- see `apo-holo-definition.md`.
