# Evaluation metrics — literature basis for the frozen protocol

Compiled 2026-08-25 from five independent specialist literature reviews (A–E) run
2026-08-24/25, merged against the earlier, narrower review in
`evaluation-protocol-lit.md` (2026-08-20).

This file is the evidence base for `docs/benchmark/evaluation/README.md` and for the
`manifest.yaml` beside it. Every protocol decision traces to a row here. It contains **no recommendations**. Decisions
live in the protocol document and in `docs/adr/`.

---

## 0. What this file is, and its evidence rules

### 0.1 The rule

Every claim below carries a DOI or an explicit **unknown**. No number is recalled from
memory. Where a number was wanted and could not be retrieved, it appears in §9 rather than
being reconstructed. Where two reports give different values for the same quantity, both are
recorded with their sources (§8); none is silently preferred.

### 0.2 Verification tags

The three-level convention from `evaluation-protocol-lit.md` is carried over and applied to
every row:

| Tag                   | Meaning                                                                                                                      |
| --------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| `[VERIFIED-FULLTEXT]` | A reviewer opened the source document and the quoted wording came out of that retrieval.                                     |
| `[VERIFIED-ABSTRACT]` | Only the abstract or structured metadata record was read. The paper is closed-access or was not fetched in full.             |
| `[UNVERIFIED]`        | Search-engine summary only, reviewer inference, arithmetic, or a paraphrase returned by a fetch tool instead of a quotation. |

The five reports used five different tag vocabularies. They map as follows, and the original
tag is preserved in brackets where it carries extra information:

| Report | Its tag                                       | Maps to               |
| ------ | --------------------------------------------- | --------------------- |
| A      | verbatim quote from a fetched page            | `[VERIFIED-FULLTEXT]` |
| A      | `[paraphrase returned, not verbatim]`         | `[UNVERIFIED]`        |
| A      | `[my inference]`                              | `[UNVERIFIED]`        |
| A      | number from a search-result summary (ACS 403) | `[UNVERIFIED]`        |
| B      | `[F]`                                         | `[VERIFIED-FULLTEXT]` |
| B      | `[S]`                                         | `[UNVERIFIED]`        |
| C      | fetched in session (default)                  | `[VERIFIED-FULLTEXT]` |
| C      | `UNVERIFIED`                                  | `[UNVERIFIED]`        |
| D      | `[F]`                                         | `[VERIFIED-FULLTEXT]` |
| D      | `[S]`, `[U]`                                  | `[UNVERIFIED]`        |
| E      | `[FT]`                                        | `[VERIFIED-FULLTEXT]` |
| E      | `[ABS]`                                       | `[VERIFIED-ABSTRACT]` |
| E      | `[SNIP]`, `[GAP]`                             | `[UNVERIFIED]`        |

A tag downgrade is never reversed here. If a report marked something unverified, it stays
unverified in this file, even where a second report verified the same fact — in that case
both are recorded and the row carries the higher tag with the lower one named.

Two exceptions, both citation metadata rather than substantive values, were resolved by
direct retrieval during this merge and are marked `[VERIFIED-FULLTEXT, resolved at merge]`.
They are the only new retrievals in this file. Both are in §8.

### 0.3 How the five reports were produced

All five were search-first systematic reviews, not recall. Each recorded its queries
verbatim, its hit counts where the interface exposed them, its screening decisions, and an
explicit list of sources it could not reach. None is a PRISMA-conformant systematic review in
the Cochrane sense and report E says so outright; they are targeted, auditable reviews.

| Report | Scope                                                        | Primary interfaces used                                             |
| ------ | ------------------------------------------------------------ | ------------------------------------------------------------------- |
| **A**  | Metrics used in allosteric-site prediction                   | PubMed E-utilities, web search, direct publisher/PMC fetch          |
| **B**  | Benchmarks, negative classes, decoys, statistical procedures | PubMed E-utilities, arXiv export API, Semantic Scholar, web, GitHub |
| **C**  | Hit criteria and top-N conventions                           | Europe PMC REST, web search, author-hosted copies                   |
| **D**  | How network and dynamics methods validate themselves         | PubMed E-utilities, Semantic Scholar, web search                    |
| **E**  | Biology and pharma stratification factors                    | Web search, PMC, NCBI E-utilities, Semantic Scholar Graph API       |

Four of the five (B, C, D, E) exhausted a 200-call session search budget and each names the
queries it could not run. Those unrun queries are recorded in §9 as bounded gaps, because an
unrun query weakens a negative finding.

### 0.4 Combined query and screening counts

**Queries with exposed hit counts.**

| Interface                  | Queries | Reports                      | Notes                                                                                                         |
| -------------------------- | ------: | ---------------------------- | ------------------------------------------------------------------------------------------------------------- |
| PubMed `esearch` (boolean) |      22 | A 7, B 8, D 7                | Counts are the API `count` field. PubMed silently expands unquoted terms; B flags this.                       |
| arXiv export API           |       2 | B                            | `all:"allosteric site prediction"` → 1; `all:"decoy pocket"` → 0.                                             |
| Europe PMC REST            |      17 | C                            | Mix of DOI lookups and full-text boolean queries.                                                             |
| Semantic Scholar Graph API |       4 | B 2, D 2                     | **3 of 4 failed with HTTP 429.** The one success returned a relevance envelope (16,516), not a boolean count. |
| Web / Google-backed search |     175 | A 40, B 23, C 18, D 33, E 61 | The interface exposes no counts. Recorded as queries run.                                                     |

**The PubMed counts that matter most**, because they bound how large the relevant literature
is. All `[VERIFIED-FULLTEXT]` (API responses read directly):

| Query (as sent)                                                                                 |  Count | Report |
| ----------------------------------------------------------------------------------------------- | -----: | ------ |
| `"allosteric site prediction"` (phrase)                                                         |     25 | A      |
| `"allosteric pocket prediction"` (phrase)                                                       |      1 | A      |
| `"allosteric residue" AND prediction`                                                           |      3 | A      |
| `allosteric AND (benchmark OR benchmarking) AND (prediction)`                                   |     53 | A      |
| `"allosteric site" AND prediction`                                                              |    591 | A      |
| `("cryptic pocket" OR "cryptic site" OR "cryptic binding site") AND prediction`                 |     68 | A      |
| `"allosteric communication" AND (prediction OR predicting)`                                     |    107 | A      |
| `allosteric site prediction benchmark`                                                          |     23 | B      |
| `"decoy pocket"`                                                                                |     92 | B      |
| `"allosteric" AND "negative dataset"`                                                           |  **0** | B      |
| `allosteric AND "permutation test"`                                                             |  **1** | B      |
| `protein AND "spatial autocorrelation" AND residue`                                             |  **1** | B      |
| `"cryptic pocket" OR "cryptic binding site"`                                                    |    193 | B      |
| `"allosteric" AND ("null model" OR "null distribution")`                                        |  **1** | B      |
| `"allosteric" AND "bootstrap" AND "confidence interval"`                                        |  **0** | B      |
| `"perturbation response scanning"`                                                              |     63 | D      |
| `allosteric[Title] AND (prediction OR predict)[Title] AND (network OR "elastic network")[Tiab]` |     15 | D      |
| `("residue interaction network" OR "protein contact network")[Tiab] AND alloster*[Tiab]`        |     54 | D      |
| `("gaussian network model" OR "anisotropic network model")[Tiab] AND alloster*[Tiab]`           |     75 | D      |
| `alloster*[Tiab] AND (betweenness OR centrality)[Tiab]`                                         |     85 | D      |
| `("quantum walk" OR "quantum walks")[Tiab] AND protein[Tiab]`                                   | **11** | D      |

**Screening.**

| Report | Records inspected at title/abstract | Retrieved in full or substantial part | Included                                   | Excluded, with reason                                                           |
| ------ | ----------------------------------: | ------------------------------------: | ------------------------------------------ | ------------------------------------------------------------------------------- |
| A      |     ≈95 (approximate, self-flagged) |                                   ≈34 | 28 method/benchmark + 6 metric authorities | 7 server/case-study papers with no cohort metric; 2 dataset papers; 1 not found |
| B      |                                ≈140 |                                    31 | 21                                         | 10 (5 no negative-class content, 3 paywalls, 2 mis-resolved PMC IDs)            |
| C      |             not exposed by the tool |       30 of 33 in its reference table | 33 cited                                   | 3 unreachable primaries                                                         |
| D      |                                ≈180 |                                    23 | 20 in the method-validation table          | not itemised                                                                    |
| E      |                    ≈470 result rows |                             58 opened | 31 cited at full text or abstract          | 10 unreachable, itemised                                                        |

Records inspected, summed over the four reports that report a denominator: **≈885**. C's
search interface exposes no counts, so no total including C is computable.

**No union count is given, and none should be inferred.** The five source sets overlap
heavily: AlloBench, APOP, CryptoBench, PocketMiner, CryptoSite, the Patterns/Barahona
benchmarking paper, ESSA, Ohm and the PASSer family each appear in four or five of the five
reviews. The overlap was not de-duplicated at the item level by any reviewer.

### 0.5 Convergent findings, and what convergence buys

Where two or more reports reached the same finding from independent searches with different
query sets, the finding is stronger than either report alone. Those cases are marked inline
as `(convergent: A, C)` and so on. The set:

| Finding                                                                                          | Reports                       | Section |
| ------------------------------------------------------------------------------------------------ | ----------------------------- | ------- |
| Ohm's "TPR" is precision and its "PPV" is recall — names inverted vs standard usage              | A, C                          | §1, §2  |
| PASSer2.0 uses two mutually inconsistent pocket-labelling rules within one paper                 | A, B, C                       | §2      |
| Jaccard > 0.5 is mathematically unreachable for a top-5 residue list against a 10–20-residue set | A, C                          | §1, §2  |
| Top-N residue (as opposed to top-N pocket) has no established convention in this field           | A, C                          | §1, §2  |
| The field's negative class is method-generated; there is no reusable decoy-pocket set            | B, D                          | §3      |
| Most papers claim a working method with no stated statistical test at all                        | B (13/18), D (≈15/17)         | §3, §4  |
| The Barahona/Yaliraki surrogate-site null is the field's only geometry-matched null              | B, D, E                       | §3, §4  |
| No paper in the network/ENM family controls for burial or solvent accessibility                  | D (searched), B (none found)  | §4      |
| Apo performance is materially worse than holo, and the field routinely evaluates on pseudo-apo   | A, B, D, E                    | §5      |
| ASD and ASBench hosts are unreachable (expired certificate, same host)                           | B (twice), A (403s elsewhere) | §9      |
| AlloBench's independent JI results contradict the field's self-reported top-3 rates              | A, D, E                       | §5, §8  |
| The 4 Å contact cutoff is not a field-wide convention; 3.5/4.0/4.5/5.0 Å all appear              | B, C, E                       | §2, §8  |

---

## 1. What the field measures

The metric census, merged and de-duplicated across reports A and C. "Independent groups" is
counted by research group, not by paper, because the PASSer family alone contributes four
papers from one group. Level is the unit actually scored.

### 1.1 The census

| Rank | Metric                                             | Definition **as first stated**                                                                                                                                                                                                                                                                                                                                                                                                                                  | Primary DOI                                                                                                                             |                                                    Independent groups | Level                                | Tag                                                                                         |
| ---: | -------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------: | ------------------------------------ | ------------------------------------------------------------------------------------------- |
|    1 | **Top-N rank success**                             | PASS 2000: "the top-ranked ASP hits the binding site in 12 trials, and one of the top three ASPs is a hit in 16 trials". APOP restates the modern form: "If this pocket is among the top-ranked three predicted pockets, we count it as a success."                                                                                                                                                                                                             | `10.1023/A:1008124202956` (PASS); `10.1093/bioinformatics/btad275` (APOP)                                                               |                                                                    ≈6 | **Pocket**                           | `[VERIFIED-FULLTEXT]`                                                                       |
|    2 | **Precision / recall / F1**                        | PASSer v1: "Precision: TP / (TP + FP)"; "Recall/Sensitivity: TP / (TP + FN)"; "F1 Score: 2 × precision × recall / (precision + recall)". PASSer-NAR: "F1 Score: the harmonic mean of precision and recall".                                                                                                                                                                                                                                                     | `10.1088/2632-2153/abe6d6`; `10.1093/nar/gkad303`                                                                                       |                                                                   ≥10 | Both                                 | `[VERIFIED-FULLTEXT]`                                                                       |
|    3 | **ROC AUC**                                        | Tee, Guarnera & Berezovsky, the fullest statement in the allosteric literature: "The receiver operating characteristic (ROC) curve is used here to quantify the proportion of true positive (those that belong to a known allosteric site) and false positive (those not belonging to a known allosteric site) among residues with a large free energy change."                                                                                                 | `10.1371/journal.pcbi.1006228`                                                                                                          |                                                                    ≥8 | **Residue** natively                 | `[VERIFIED-FULLTEXT]`                                                                       |
|    4 | **MCC**                                            | Allo-PED: "MCC = (TP·TN − FP·FN) / √[(TP+FP)(TP+FN)(TN+FP)(TN+FN)]". CASP10 adds the interpretation: "A MCC of 0 corresponds to random prediction"; "MCC is a useful measure when the two classes … are of very different sizes."                                                                                                                                                                                                                               | `10.1101/2025.03.28.645953`; `10.1002/prot.24495`                                                                                       |                                                                    ≥5 | Both                                 | `[VERIFIED-FULLTEXT]`                                                                       |
|    5 | **AUPRC / average precision**                      | CryptoBench: "area under the precision-recall curve (AUPRC)", computed "from probability outputs". MEF-AlloSite calls it average precision: "The weighted mean of precision values at each threshold is used to determine average precision".                                                                                                                                                                                                                   | `10.1093/bioinformatics/btae745`; `10.1186/s13321-024-00882-5`                                                                          |                                                 5, **all since 2023** | **Residue** (pocket in MEF-AlloSite) | `[VERIFIED-FULLTEXT]`                                                                       |
|    6 | **DCA / DCC (distance hit criterion)**             | See §2. DCA: centre of prediction to nearest ligand heavy atom. DCC: centre-to-centre. **The two names are used inconsistently across the literature.**                                                                                                                                                                                                                                                                                                         | `10.1023/A:1008124202956` (4 Å origin); `10.1093/bioinformatics/btx350` (DCC as centre-to-centre)                                       |     1 in allosteric (STINGAllo); ubiquitous in ligand-site prediction | Pocket                               | `[VERIFIED-FULLTEXT]`                                                                       |
|    7 | **Jaccard index over residue sets**                | AlloBench: "JI = \|K ∩ P\| / \|K ∪ P\|, where K and P are the sets of residues in the known and predicted allosteric sites… It is 0 if there are no residues in common between K and P and is 1 if K and P are identical."                                                                                                                                                                                                                                      | `10.1021/acsomega.5c01263`                                                                                                              |                                                                 **1** | Residue sets, compared at site level | `[VERIFIED-FULLTEXT]`                                                                       |
|    8 | **DVO (discretised volume overlap)**               | DeepSite: "we discretize protein space into 1 × 1 × 1 Å³ voxels, and consider the convex hulls determined by both the real and predicted-binding site volume. We then compute a Jaccard Index." DeepSite cites no prior source; it is their contribution.                                                                                                                                                                                                       | `10.1093/bioinformatics/btx350`                                                                                                         | 3 (DeepSite, Kalasanty, PUResNet) report it; **only 1 thresholds it** | Volume                               | `[VERIFIED-FULLTEXT]`                                                                       |
|    9 | **BDT (binding-site distance test)**               | Roche, Tetchner & McGuffin: `S_ij = exp(−(d_ij/d0)²)` on Cα–Cα distances, `BDT = Σ_i max_j S_ij / max(N_p, N_o)`, d0 = 1–3 Å recommended. Motivation: "An incorrectly predicted site that is nevertheless close to the observed binding site will obtain an identical score to the same number of non-binding residues predicted at random" (with MCC).                                                                                                         | `10.1093/bioinformatics/btq543`                                                                                                         |                                                              1 + CASP | **Residue**, graded                  | `[VERIFIED-FULLTEXT]`                                                                       |
|   10 | **Mutual overlap criterion (MOc)**                 | fpocket: a pocket succeeds if "at least 50% of the ligand atoms lies within 3 Å of at least one alpha sphere, AND if at least 20% of the pocket alpha spheres lie within 3 Å of the ligand".                                                                                                                                                                                                                                                                    | `10.1186/1471-2105-10-168`                                                                                                              |                                                                     1 | Alpha-sphere / pocket                | `[VERIFIED-FULLTEXT]`                                                                       |
|   11 | **Relative intersection I_rel**                    | LIGYSIS-bench: "Relative intersection, I_rel, … quantifies how similar these fingerprints are. Subtracting I_rel from 1 gives a distance, D, which takes the value of 0 when A and B share all the binding residues and 1 when they share none." **Not** the Jaccard union — it is a max-possible-intersection normalisation.                                                                                                                                   | `10.1186/s13321-024-00923-z`                                                                                                            |                                                                     1 | Residue sets                         | `[UNVERIFIED]` for the exact denominator; `[VERIFIED-FULLTEXT]` for the quoted sentence     |
|   12 | **AULC / AULC-ratio**                              | Zhang, Ghadermarzi & Kurgan: "quantifies the area under the ROC curve where the number of putative PBRs ≤ number of native PBRs", justified as "arguably the key part of ROC curve"; plus a ratio normalised by the random predictor's AULC.                                                                                                                                                                                                                    | `10.1093/bioinformatics/btaa573`                                                                                                        |                                                    1 (adjacent field) | **Residue**, partial ROC             | `[VERIFIED-FULLTEXT]`                                                                       |
|   13 | **Group-specific scores used as their own metric** | ACI (Ohm): "The frequency with which each residue is affected by a perturbation… we call this frequency the allosteric coupling intensity". Quantile score QS, 6 variants (Barahona/Yaliraki). Z-score of pocket coupling (KeyAlloSite): "Z-score_cavity_m = (ECS_cavity_m − μ_cavity) / σ_cavity". Z-score of soft-mode frequency shift (ESSA): "z_i = ⟨Δλ₁₋₁₀(i)⟩ − μ / σ", scored by top-quartile membership. Binding leverage / leverage coupling (SPACER). | `10.1038/s41467-020-17618-2`; `10.1016/j.patter.2021.100408`; `10.7554/eLife.81850`; `10.1016/j.csbj.2020.06.020`; `10.1093/nar/gkt460` |                                                                1 each | Residue → site                       | `[VERIFIED-FULLTEXT]`                                                                       |
|    — | **EF / RIE / BEDROC**                              | Compound-ranking early-recognition metrics. `EF@f = (actives in top f·N) / (n · f)`. BEDROC α = 20 "dictates that 80% of the maximum contribution to BEDROC comes from the top 8% of the ranked list."                                                                                                                                                                                                                                                          | `10.1021/ci600426e` (primary **unreachable**); α attribution via `10.3389/fchem.2019.00701`                                             |                                              **0 in site prediction** | Ranked list                          | `[UNVERIFIED]` — normalisation constants taken from the RDKit implementation, not the paper |
|    — | **Accuracy**                                       | PASSer v1: "Accuracy: (TP + TN) / (TP + FP + FN + TN)".                                                                                                                                                                                                                                                                                                                                                                                                         | `10.1088/2632-2153/abe6d6`                                                                                                              |                                                               several | Both                                 | `[VERIFIED-FULLTEXT]`                                                                       |

### 1.2 What a reviewer expects, and what is ad hoc

Stated plainly, from A §4 and C §4.1, which agree.

**Expected. A reviewer will ask why if these are missing:**

1. **A top-N ranked-list number.** Rank 1 by independent-group count and the field's default
   since PASS 2000. Report A: "If you publish an allosteric-site method and do not report a
   top-N rate, a reviewer will ask why."
2. **A threshold-free discrimination number over residues.** ROC AUC is the safe choice
   (≥8 groups); AUPRC beside it is normal as of 2023 and is the convention in the
   cryptic-pocket and pLM-residue wings.
3. **A stated chance or null baseline.** Every paper that claims significance states one:
   PARS "Wilcoxon–Mann–Whitney's P ≤ 0.05"; APOP "The P-value of 0.00088 obtained from the
   one-sided Wilcoxon signed-rank"; MEF-AlloSite p-values and Cohen's d.
4. **Precision / recall / F1** if the method has a classifier head. Not expected of a pure
   network or dynamics method — Ohm, ESSA, bond-to-bond propensity and Tee 2018 all skip it.

**Ad hoc. Each would read as an instrument chosen after the result:**

- Any metric derived from the method's own propagation score, presented as the evaluation
  rather than as the prediction. Scoring a method with its own score is circular. Every
  entry in row 13 above is idiosyncratic by construction.
- **Jaccard against a short list.** One group, one paper. Structurally unusable below.
- **Accuracy at any threshold** at 2–11 % prevalence. PASSer v1 reports accuracy 0.974 at a
  positive rate of 119/2246 = 5.3 %, where the always-negative classifier scores 0.947
  `[VERIFIED-FULLTEXT]`. Allo-Allo's "Imb. Acc." column reads 0.91–0.98 for every method
  including one at AUPRC 0.07 `[VERIFIED-FULLTEXT]`.
- **A bespoke composite index.** No paper in the 28-paper included set has one.
- **BEDROC or EF.** Report C read the evaluation sections of PASS, LIGSITEcsc, PocketPicker,
  Q-SiteFinder, fpocket, P2Rank, DeepSite, Kalasanty, PUResNet, COACH, CASP10, CryptoSite,
  CryptoBench, PocketMiner, LIGYSIS-bench, AlloBench, APOP, PASSer2.0, DeepAllo, STINGAllo,
  Ohm and Amor 2016. **None reports EF, RIE or BEDROC** `[VERIFIED-FULLTEXT]`. Further,
  α = 20 encodes "the top 8 % matters", which for a 300-residue chain is 24 residues — not a
  top-5 list.

### 1.3 Three structural facts about the census

**(a) The metric names are not comparable across levels.** ROC AUC, AUPRC, F1 and MCC are all
computed at pocket level by some groups and residue level by others, under the same name.
Prevalence changes from ~5 % of residues to ~5 % of pockets and the numbers are not the same
object. Allo-PED's MCC 0.544 is pocket-level, STINGAllo's 0.64 is per-residue, CryptoBench's
is per-residue over a different label definition. A cross-paper MCC comparison in this field
is not well-defined `[VERIFIED-FULLTEXT]`.

**(b) The pocket detector is a hidden hyperparameter of every pocket-level metric.** Papers
get from residue scores to pockets by aggregating over an externally detected pocket set,
almost always fpocket (AlloPred, APOP, PASSer family, ESSA, Allo-PED) or CAVITY
(KeyAlloSite). STINGAllo's own honest split is direct evidence of the size of the effect:
DCC success "~78 %" on the subset where its predicted residues fall inside an fpocket pocket,
against **60.2 % overall** `[VERIFIED-FULLTEXT]`.

**(c) Top-N residue has no convention.** (convergent: A, C.) A found no allosteric paper
using "precision@N" as a named metric; the query
`"precision@" OR "hit rate" top-5 residue ranked list allosteric prediction evaluation protein`
returned no allosteric paper using the term. C found the same: "All of these are top-N
pockets. Top-N residues has no established convention in this field." The nearest objects are
DeepAllo's fractional top-k % (still over pockets: "Allosteric pockets were ranked in
different top positions namely, Top 1 %, Top 3 %, Top 5 %, and Top 10 %") and STINGAllo's DCC
on a predicted residue set, which is a geometric hit rather than a rank
`[VERIFIED-FULLTEXT]`.

The closest published template for a short ranked **residue** list from a network model is
outside the allosteric-prediction literature proper: the PNAS 2024 global-hinge-site paper,
`10.1073/pnas.2414333121`, which takes `h` GNM hinge residues, counts the overlap `s` with
`b` drug-binding residues out of `N`, and reports an exact hypergeometric p-value
`[VERIFIED-FULLTEXT]`. See §3.4.

---

## 2. What counts as a hit

Merged from C, with the label-cutoff evidence cross-checked against B and E.

### 2.1 The 4 Å criterion and its true primary source

This is the most-quoted number in the field. The chain is real and has one broken link.

**Primary — PASS, 2000.** Brady GP Jr & Stouten PFW, _J Comput Aided Mol Des_ 14:383–401,
`10.1023/A:1008124202956`, fetched from the author-hosted copy at ccl.net
`[VERIFIED-FULLTEXT]`:

> "Any ASP with DNear <= 4Å is considered a binding site 'hit.'"

where `DNear` is the distance from an Active Site Point to the **nearest ligand atom** — i.e.
centre-to-atom. PASS also originates the top-1/top-3 convention in the same paper.

**Restatement 1 — LIGSITEcsc, 2006**, `10.1186/1472-6807-6-19` `[VERIFIED-FULLTEXT]`:
"A prediction is a hit if it is within 4 Å to any atom of the ligand." LIGSITEcsc attributes
this to its reference [16] = Laurie & Jackson 2005 (Q-SiteFinder).

**The broken link.** Laurie ATR & Jackson RM 2005, `10.1093/bioinformatics/bti315`, fetched
`[VERIFIED-FULLTEXT]`, states **no 4 Å criterion**. Its criterion is a different quantity
entirely:

> "The term 'precision' used here defines the percentage of probe sites in a single cluster
> that are within 1.6 Å of a ligand atom."
> "A threshold of 25% precision was used to define success in all the results presented here."

with the rationale that "a method that includes the entire protein surface in a single
'pocket' will be 100% successful unless such a precision threshold is used."

**So: the 4 Å criterion traces to PASS (2000), not to Q-SiteFinder. LIGSITEcsc's citation is
a misattribution that has been propagated onward.** This is itself a finding — a repeated
number that traces to nothing is a defect in the field's citation graph, not a convention.

**Restatement 2 — PocketPicker, 2007**, `10.1186/1752-153X-1-7` `[VERIFIED-FULLTEXT]`: "we
define a prediction to be a hit, if the geometric center of the presumed pocket lies within
4 Å to any atom of the ligand"; "Correct predictions were termed 'TOP1-hits' whereas
'TOP3-hits' are predictions where the respective ligand is found within the three largest
predicted pockets." Attributed to PASS and to Huang & Schröder.

**Restatement 3 — fpocket names it PPc, 2009**, `10.1186/1471-2105-10-168`
`[VERIFIED-FULLTEXT]`: "PocketPicker criterion (PPc)… If the position of this centre is
within 4 Å from any atom of the ligand, the binding site is considered correctly identified."

**Restatement 4 — P2Rank, 2018**, `10.1186/s13321-018-0285-8` `[VERIFIED-FULLTEXT]`:
"methodology based on ligand-centric counting and DCC (distance between the center of the
pocket and any ligand atom) pocket identification criterion with 4 Å threshold."

### 2.2 DCA against DCC — a naming collision, not a threshold disagreement

**P2Rank calls centre-to-nearest-ligand-atom "DCC".** Everywhere else — DeepSite, Kalasanty,
PUResNet, LIGYSIS-bench, the 2025 membrane benchmark — **DCC means centre-to-centre** and the
centre-to-atom quantity is called **DCA**. The same acronym denotes two different distances
across the literature `[VERIFIED-FULLTEXT]`.

**DCC as centre-to-centre, definitional source.** DeepSite, `10.1093/bioinformatics/btx350`
`[VERIFIED-FULLTEXT]`:

> "This metric considers a prediction successful if a point prediction of the pocket is
> closer than a given distance threshold to the geometric center of the real-binding site."
> "Values ranging between 4 and 20 Å are typically used for success rate plots."

DeepSite credits the practice to Chen et al. 2011, `10.1016/j.str.2011.02.015`, whose primary
text is **paywalled and was not verified at source** — so the DCC lineage has an unverified
root as well `[UNVERIFIED]`.

Corroborating uses of DCC ≤ 4 Å: Kalasanty `10.1038/s41598-020-61860-z`, "the distance
between the predicted and the actual center of the pocket", DCC < 4 Å headline;
PUResNet `10.1186/s13321-021-00547-7`, "If the distance is ≤ 4 Å, then it is determined to be
correctly predicted site"; the 2025 membrane benchmark `10.1021/acs.jcim.5c00336`,
"Predictions with DCC values of less than 4.0 Å were considered to be successful" and "4 Å is
the established cutoff value" for DCC. All `[VERIFIED-FULLTEXT]`.

**And the most recent independent evaluation rejects that.** Utgés & Barton 2024,
`10.1186/s13321-024-00923-z` `[VERIFIED-FULLTEXT]`:

> "It is clear from our results that a DCC threshold of 4 Å is too conservative, and a more
> flexible DCC threshold of 10–12 Å should be used for comparable performance with DCA = 4 Å."
> "Reported recall is obtained using DCC = 12 Å"

**Consequence.** DCA = 4 Å and DCC = 4 Å are not interchangeable; for centre-to-centre the
equivalent strictness is 10–12 Å. Papers quoting "DCC 4 Å" are, on Utgés & Barton's evidence,
applying a criterion roughly three times stricter than the convention they believe they are
following. Any protocol that uses either acronym must define it rather than cite it.

### 2.3 Residue-overlap criteria — six mutually inconsistent rules

| Rule                              | Exact wording                                                                                                                                                       | Source             | DOI                          | Tag                                  |
| --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------ | ---------------------------- | ------------------------------------ |
| **Mutual overlap (MOc)**          | "at least 50% of the ligand atoms lies within 3 Å of at least one alpha sphere, AND if at least 20% of the pocket alpha spheres lie within 3 Å of the ligand"       | fpocket 2009       | `10.1186/1471-2105-10-168`   | `[VERIFIED-FULLTEXT]`                |
| **Jaccard over residue sets**     | "JI = \|K ∩ P\| / \|K ∪ P\|"; success at "JI > 0.5"; swept over {0, 0.1, 0.2, 0.3, 0.4, 0.5}                                                                        | AlloBench 2025     | `10.1021/acsomega.5c01263`   | `[VERIFIED-FULLTEXT]`                |
| **Relative intersection I_rel**   | "takes the value of 0 when A and B share all the binding residues and 1 when they share none"; sites merged by "cutting the tree at D = 0.5"                        | LIGYSIS-bench 2024 | `10.1186/s13321-024-00923-z` | `[UNVERIFIED]` for the normalisation |
| **≥1 shared residue**             | "A pocket is labeled as either 1 (positive) if it contains at least one residue identified as binding to allosteric modulators or 0 (negative)" — ASD arm           | PASSer2.0 2022     | `10.3389/fmolb.2022.879251`  | `[VERIFIED-FULLTEXT]`                |
| **Closest centroid**              | "A pocket is labeled as 1 (positive) only if its centroid is the closest to that of the allosteric modulator, otherwise 0 (negative)" — ASBench arm, **same paper** | PASSer2.0 2022     | `10.3389/fmolb.2022.879251`  | `[VERIFIED-FULLTEXT]`                |
| **≥25 % residue overlap**         | "labeled positive if ≥ 25 % of its residues overlapped with the true allosteric site; otherwise negative"                                                           | Allo-PED 2025      | `10.1101/2025.03.28.645953`  | `[VERIFIED-FULLTEXT]`                |
| **≥1/3 coverage of the true set** | "We define a prediction of a cryptic site to be accurate when at least one third of its residues are identified (sensitivity > 33%)."                               | CryptoSite 2016    | `10.1016/j.jmb.2016.01.029`  | `[VERIFIED-FULLTEXT]`                |

**PASSer2.0 uses two incompatible rules on its two datasets inside one paper**
(convergent: A, B, C — three reviewers found this independently from different queries). The
consequence is visible in its own class balance: ASD arm 2,123 pockets / 133 positive;
ASBench arm 3,708 pockets; combined **4.87 % (251 of 5,155)** `[VERIFIED-FULLTEXT]`.

**The ceiling nobody states.** With a ground-truth allosteric set of |K| ≈ 10–20 residues
(CryptoBench: 16.60 ± 7.22 binding residues per protein, `10.1093/bioinformatics/btae745`
`[VERIFIED-FULLTEXT]`) and a 5-residue prediction, max Jaccard ≈ 5/16 ≈ 0.31. AlloBench's own
headline success threshold, JI > 0.5, is **unreachable by construction** for a top-5 list
(convergent: A, C). AlloBench also discards all ranking information by design: "The
probabilities reported by ALLO, Allosite, PASSer (AutoML), and PASSer (Ensemble) or the
scores by AllositePro, APOP, and PASSer (Rank) were also not utilized here."
`[VERIFIED-FULLTEXT]`

### 2.4 The contact cutoff that builds the label set — no single convention

(convergent: B, C, E — all three built this table independently and none found a field-wide
standard.)

| Cutoff                  | What it is applied to                                                                                                     | Source                     | DOI                                 | Tag                                                                                      |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------- | -------------------------- | ----------------------------------- | ---------------------------------------------------------------------------------------- |
| **2.5 Å** heavy atom    | to a projected ligand                                                                                                     | COACH                      | `10.1093/bioinformatics/btt447`     | `[VERIFIED-FULLTEXT]`                                                                    |
| **3.5 Å** heavy atom    | caspase-1 allosteric residues                                                                                             | Amor et al. 2016           | `10.1038/ncomms12477`               | `[VERIFIED-FULLTEXT]`                                                                    |
| **4.0 Å**               | "allosteric sites were obtained by locating the residues within 4 Å of the allosteric modulator in the PDB structures"    | AlloBench                  | `10.1021/acsomega.5c01263`          | `[VERIFIED-FULLTEXT]`                                                                    |
| **4.0 Å**               | "residues within 4 Å from the allosteric ligand" — the ASBench-lineage number, as used by the Patterns benchmarking paper | Wu/Strömich/Yaliraki       | `10.1016/j.patter.2021.100408`      | `[VERIFIED-FULLTEXT]`                                                                    |
| **4.5 Å**               | binding-site radius                                                                                                       | CryptoBench                | `10.1093/bioinformatics/btae745`    | `[VERIFIED-FULLTEXT]`                                                                    |
| **4.5 Å**               | effector atoms → allosteric site membership                                                                               | Tee, Guarnera & Berezovsky | `10.1371/journal.pcbi.1006228`      | `[VERIFIED-FULLTEXT]`                                                                    |
| **5.0 Å** any atom      | "residues with at least one atom within 5 Å from any atom of a ligand"                                                    | CryptoSite                 | `10.1016/j.jmb.2016.01.029`         | `[VERIFIED-FULLTEXT]`                                                                    |
| **5.0 Å**               | "All residues located within 5 Å of the selected ligand" — **same rule for catalytic and allosteric sites**               | CASBench                   | `10.32607/20758251-2019-11-1-74-80` | `[VERIFIED-FULLTEXT]`                                                                    |
| **6 Å**                 | ASBench, as rendered in the **bioRxiv preprint** of the Patterns paper                                                    | —                          | `10.1101/2021.08.16.456251`         | `[UNVERIFIED]` — B judges it most likely an extraction artefact and could not confirm it |
| **6 Å**                 | ASD v2                                                                                                                    | —                          | —                                   | `[UNVERIFIED]` (E, `[SNIP]`)                                                             |
| **Σ VdW radii + 0.5 Å** | "at least one heavy atom of a biologically relevant ligand within 0.5 Å distance of the sum of the Van der Waals radii"   | CASP10                     | `10.1002/prot.24495`                | `[VERIFIED-FULLTEXT]`                                                                    |

**ASD and ASBench themselves state no explicit distance cutoff** in the text B fetched
`[VERIFIED-FULLTEXT]`. The 4 Å figure that everyone attributes to ASBench comes from
downstream users, not from the ASBench paper. That is a second orphaned number.

The field says so itself. Patterns 2021/2022, `10.1016/j.patter.2021.100408`
`[VERIFIED-FULLTEXT]`:

> "the definition of orthosteric and allosteric residues, which would significantly affect
> the size and residues involved, plays an essential part when evaluating allosteric site
> prediction methods."

i.e. the field's own diagnosis is that label definition, not metric choice, dominates the
variance.

### 2.5 Misattributions and undefined criteria the reports found

A repeated number that traces to nothing is itself a finding. The full list:

1. **4 Å → Q-SiteFinder.** LIGSITEcsc's attribution is wrong; Q-SiteFinder states a 25 %
   precision threshold at 1.6 Å instead. Real primary: PASS 2000,
   `10.1023/A:1008124202956`. `[VERIFIED-FULLTEXT]` (C).
2. **DCC vs DCA.** P2Rank's "DCC" is everyone else's DCA. `[VERIFIED-FULLTEXT]` (C); flagged
   independently as unresolved in `evaluation-protocol-lit.md` §5 item 9 and now **closed**.
3. **Ohm's TPR and PPV are swapped relative to standard usage.** (convergent: A, C.) Ohm,
   `10.1038/s41467-020-17618-2` `[VERIFIED-FULLTEXT]`: TPR = "the ratio of the number of true
   hotspots to the total number of predicted hotspots" — **that is precision**; PPV = "the
   ratio of the number of identified allosteric site residues to the total number of all
   allosteric site residues" — **that is recall**. Do not copy Ohm's metric names.
4. **Ohm defines no "true hotspot".** C: "There is **no quantitative definition of a 'true
   hotspot'** anywhere in the paper — the match to a known allosteric site is asserted, not
   defined." `[VERIFIED-FULLTEXT]`
5. **APOP defines no spatial overlap rule.** "For each structure, we report the
   highest-ranked pocket that is known to have bound allosteric ligand(s)" — the step from
   ligand to pocket identity is not specified. `[VERIFIED-FULLTEXT]`
6. **Allosite's cutoff and pocket-labelling threshold live in the SI**, not the article body,
   and were not retrieved. **unknown** at source. `10.1093/bioinformatics/btt399`.
7. **DVO has no canonical threshold.** The only thresholded use found is 0.2, in a single
   2025 benchmark that says outright: "There exists no clear recommendation for the DVO
   cutoff value in the scientific literature" `10.1021/acs.jcim.5c00336`
   `[VERIFIED-FULLTEXT]`. A "DVO > 0.5 high quality" framing appears in a Kalasanty fetch
   summary and is `[UNVERIFIED]`. Anyone quoting a canonical DVO threshold is quoting
   nothing.
8. **BEDROC's normalisation constants and the α = 20 convention are unverified at primary.**
   Truchon & Bayly `10.1021/ci600426e` returned ACS 403 and a PubMed cookie wall. C's
   formulas come from the RDKit reference implementation and the α = 20 attribution from a
   secondary, `10.3389/fchem.2019.00701`. The sign in the `RIE_min` denominator did not
   render consistently across fetches. `[UNVERIFIED]`
9. **RIE is attributed by RDKit to Sheridan et al. 2001**, _J Chem Inf Comput Sci_
   41:1395–1406 — **DOI unverified**. `[UNVERIFIED]`
10. **"78 % DCC / 60 % / 64 % F1 / 64 % MCC" belongs to STINGAllo, not CryptoBench and not
    the CSBJ precursor.** `evaluation-protocol-lit.md` §5 item 12 recorded these figures as
    "almost certainly `10.1016/j.csbj.2024.10.036`" after a search summariser attached them
    to CryptoBench. Reports A and C independently read STINGAllo and both attribute them
    there: `10.1093/bib/bbaf424`, "DCC success ~78 % on the subset where AFRs fall in an
    fpocket pocket; 60.2 % overall… per-residue F1 0.64, MCC 0.64" `[VERIFIED-FULLTEXT]`.
    Mariano et al. `10.1016/j.csbj.2024.10.036` is STINGAllo's precursor and reports
    Kolmogorov–Smirnov tests on feature distributions **with no p-values in the text**
    `[VERIFIED-FULLTEXT]` (B). **The earlier file's provisional attribution is corrected.**

### 2.6 Near-misses: the field has no residue-level tolerance shell

A Europe PMC full-text query for
`"binding site residues" AND "shell" AND "tolerance" AND "prediction"` returned **47 records,
none of which defines a tolerance shell around a residue label set** `[VERIFIED-FULLTEXT]`.
Residue-level papers — CASP10, PocketMiner, CryptoBench, CryptoSite, COACH, DeepAllo — all
use a hard binary label from one ligand distance cutoff, and a residue outside it is a false
positive regardless of proximity.

Tolerance enters in three other ways:

1. **At pocket level, via the distance criterion itself.** DCA ≤ 4 Å and DCC ≤ 4–12 Å _are_
   the tolerance. This is why the field prefers pockets: the tolerance is inside the metric.
2. **At residue level, via BDT's graded score.** `10.1093/bioinformatics/btq543` is the
   field's only sanctioned near-miss device, and its answer is "partial credit, weighted by
   distance". CASP10 used BDT alongside MCC and found results "very similar to the MCC
   averages" `[VERIFIED-FULLTEXT]`.
3. **By widening the label set at construction** — the 2.5/3.5/4.0/4.5/5.0 Å spread in §2.4
   is an unlabelled tolerance parameter.

### 2.7 There is no allosteric-specific hit criterion

C, plainly: "the allosteric field reuses the orthosteric machinery, and does so less
rigorously." AlloBench is the only allosteric benchmark that pins a criterion explicitly and
sweeps its threshold. PASSer labels inconsistently between datasets; APOP omits the overlap
definition; Ohm leaves "true hotspot" undefined; Allosite's rule is in unretrieved SI.
STINGAllo is the only paper reporting **both** levels — residue F1 = 0.64 and MCC = 0.64
alongside a pocket-level 4 Å DCC success rate — and it defines allosteric-site-forming
residues by **loss of accessible surface area on modulator binding, not by a distance
cutoff**, which is a seventh label convention. `[VERIFIED-FULLTEXT]`

---

## 3. Negative classes and null models

Merged from B and D. The sponsor's success criterion under test is, verbatim:
_"statistically significantly higher scores to known distal regulatory residues compared to:
random background residues, and non-functional surface pockets."_ B's finding, stated
plainly: **that criterion is met in full by no published paper in either review.** The
Barahona lineage meets the random-background half. Nobody meets both halves with a stated
test.

### 3.1 How "non-functional surface pocket" is built in practice

Three families exist. Every one of them is method-generated.

**(a) Complement-of-positive within the same protein. The dominant construction.**

| Paper        | Exact wording                                                                                                                | Scale                                                                          | DOI                              | Tag                   |
| ------------ | ---------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ | -------------------------------- | --------------------- |
| AlloPred     | "We treated pockets without known allosteric binding residues as negative examples during machine learning."                 | 2,201 pockets, 389 (18 %) allosteric ⇒ ~1,812 negatives                        | `10.1186/s12859-015-0771-1`      | `[VERIFIED-FULLTEXT]` |
| PASSer2.0    | two inconsistent rules, §2.3                                                                                                 | 5,155 pockets, 251 positive = **4.87 %**                                       | `10.3389/fmolb.2022.879251`      | `[VERIFIED-FULLTEXT]` |
| Allo-PED     | "A pocket was labeled positive if ≥25 % of its residues overlapped with the true allosteric site"                            | **185 positive vs 4,571 negative** in training; 745 test negatives             | `10.1101/2025.03.28.645953`      | `[VERIFIED-FULLTEXT]` |
| DeepAllo     | "Each residue in an allosteric pocket was labeled as allosteric."                                                            | positive pockets **304 of 4,223 (7.76 %)**; residue-level positives **5.12 %** | `10.1093/bioinformatics/btaf294` | `[VERIFIED-FULLTEXT]` |
| PASSer (NAR) | "the pocket nearest to the modulator as the allosteric site"; "all other pockets as non-allosteric sites"                    | ASD 207 proteins; CASBench 1049                                                | `10.1093/nar/gkad303`            | `[VERIFIED-FULLTEXT]` |
| MEF-AlloSite | pocket with no residue binding an allosteric modulator, **undersampled to 1:5 pos:neg**                                      | Core 235 sites, Core-Diversity 147 sites                                       | `10.1186/s13321-024-00882-5`     | `[VERIFIED-FULLTEXT]` |
| Allo-Allo    | "residues not labeled as allosteric sites within these proteins were treated as negative examples" — whole-protein negatives | ASD 2422 → 653 proteins                                                        | `10.1101/2024.09.28.615583`      | `[VERIFIED-FULLTEXT]` |
| CryptoBench  | residue level: **no formal definition** — everything not within 4.5 Å of a ligand                                            | 1,107 apo structures                                                           | `10.1093/bioinformatics/btae745` | `[VERIFIED-FULLTEXT]` |

**(b) Absence of any bound ligand across the whole PDB, then falsified by simulation. Only
PocketMiner.** `10.1038/s41467-023-36699-3`, preprint `10.1101/2022.06.28.497399`
`[VERIFIED-FULLTEXT]`:

> "The residues of the USEARCH cluster centroid which were not found within 5 Å of any valid
> MOAD ligand were taken as candidate negative examples"

then

> "To build further confidence in negative labels, we also conducted simulations of these
> proteins … we eliminated any residues that had an assigned LIGSITE pocket volume greater
> than 20 Å³"

**This is the only negative-class construction in either review that actively tries to
falsify its own negative labels.** Its second stage requires MD.

**(c) Algorithm-generated decoys in regions where no binding was observed. DogSiteScorer.**
Quoted verbatim from SiteFerret's critique, `10.1021/acs.jctc.2c01306` / arXiv:2212.11888
`[VERIFIED-FULLTEXT]`:

> "To populate the negative dataset in the DogSiteScorer algorithm, so-called decoys are
> added to the dataset. This choice, however, is conceptually unsatisfactory since: i) it is
> method-specific (every method will return differently shaped putative pockets); ii) false
> negatives cannot be ruled out"

SiteFerret's own response is to abandon negatives entirely: "we approached the problem of
scoring putative pockets as a one-class discrimination problem. Namely, we assumed that we
only hold samples of the positive class" — Isolation Forest anomaly detection.

**Two constructions the field does _not_ use.** Nobody labels a pocket non-functional by
"absence from ASD" — no paper B fetched uses that rule. Nobody uses a ranking threshold as a
label definition either; top-1/top-3 and DCC/DCA are _evaluation_ criteria, not labels.
`[VERIFIED-FULLTEXT]` for the first, `[UNVERIFIED]` for the second.

### 3.2 Is there a reusable decoy-pocket set? No

(convergent: B, D.) **Every paper rolls its own, regenerated from whichever pocket detector
that paper happens to run.** There is no allosteric equivalent of DUD-E. arXiv
`all:"decoy pocket"` returns **0** `[VERIFIED-FULLTEXT]`.

The three nearest things, and why none of them is that:

| Candidate                                    | What it is                                                                                                                                                                                                                               | Why it is not an allosteric decoy set                                             | DOI                              | Tag                   |
| -------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- | -------------------------------- | --------------------- |
| **NRDLD / DrugPred**                         | 71 druggable + 44 "less druggable" proteins                                                                                                                                                                                              | the axis is druggability, not allostery, and it is protein-level not pocket-level | `10.1021/ci200266d`              | `[UNVERIFIED]`        |
| **CryptoSite's 705 concave surface patches** | third class beside 84 cryptic sites and 92 binding pockets                                                                                                                                                                               | bound to one 2016 apo–holo pair list and to fpocket/ConCavity scoring of that era | `10.1016/j.jmb.2016.01.029`      | `[VERIFIED-FULLTEXT]` |
| **CryptoBench's 1,445 non-cryptic pockets**  | largest and most recent, MIT-licensed                                                                                                                                                                                                    | axis is crypticity (pocket RMSD < 2 Å), not allostery                             | `10.1093/bioinformatics/btae745` | `[VERIFIED-FULLTEXT]` |
| **DUD-E** (for contrast)                     | 102 targets, 22,886 ligands, **50 property-matched decoys per ligand**; matched on MW, miLogP, rotatable bonds, HBA, HBD, net charge; FCFP_6 Tanimoto filter; only 692/805,136 (**0.086 %**) decoy scaffolds overlapped ligand scaffolds | ligand-side, not site-side                                                        | `10.1021/jm300687e`              | `[UNVERIFIED]`        |

Because the negative class is method-generated, **two papers' "non-functional pockets" are
not the same objects** — SiteFerret's point (i). A cross-paper comparison of specificity in
this field is not well-defined.

**AlloBench is titled a benchmarking pipeline and supplies no negative class at all.** B's
targeted extraction: "The document does not explicitly define how non-allosteric pockets or
decoy sites are generated." `[VERIFIED-FULLTEXT]` A benchmark for a discrimination task with
only a positive class is not a benchmark for discrimination.

### 3.3 Which detector, at which version, with which parameters

| Method                                                  | Detector                              | Version stated?          | Parameters stated?                                                                                                                                               |
| ------------------------------------------------------- | ------------------------------------- | ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| AlloPred `10.1186/s12859-015-0771-1`                    | fpocket                               | **Yes — "Fpocket v2.0"** | "default parameters used in the Fpocket calculation produced pockets that were large enough to place most (average 86 %) allosteric binding residues in pockets" |
| PASSer2.0 `10.3389/fmolb.2022.879251`                   | fpocket                               | No                       | No                                                                                                                                                               |
| DeepAllo `10.1093/bioinformatics/btaf294`               | fpocket                               | No                       | No                                                                                                                                                               |
| Allo-PED `10.1101/2025.03.28.645953`                    | fpocket                               | No                       | "default settings"                                                                                                                                               |
| APOP `10.1093/bioinformatics/btad275`                   | fpocket                               | No                       | "the default parameters of Fpocket"; GNM cutoff **10 Å**                                                                                                         |
| ESSA `10.1016/j.csbj.2020.06.020`                       | fpocket                               | No                       | "Fpocket with its default parameters"                                                                                                                            |
| CryptoSite `10.1016/j.jmb.2016.01.029`                  | fpocket **+ ConCavity**               | No                       | Not stated                                                                                                                                                       |
| PocketMiner `10.1101/2022.06.28.497399`                 | **LIGSITE** (enspara impl.) + fpocket | impl. named              | **Yes, fully**: "we used a min rank of 7, a grid spacing of 0.7 Å, a probe radius of 1.4 Å, and a minimum cluster size of 3 grid points"                         |
| CryptoBench evaluation `10.1093/bioinformatics/btae745` | P2Rank                                | No                       | Not stated                                                                                                                                                       |
| SiteFerret `10.1021/acs.jctc.2c01306`                   | own NS-based                          | —                        | one-class, no negatives                                                                                                                                          |

All rows `[VERIFIED-FULLTEXT]`.

**fpocket is the de-facto standard and exactly one paper states a version** (AlloPred, v2.0,
2015). PocketMiner is the only paper in either review that states a fully reproducible
detector configuration. "Default parameters" is not reproducible across the 1.0 → 4.x line.

Release state, checked via the GitHub API 2026-08-24 `[VERIFIED-FULLTEXT]`:
**fpocket 4.2.3**, published **2026-03-09**, MIT licence; **P2Rank 2.5.1**, published
**2025-08-07**.

fpocket 1.0 published defaults, `10.1186/1471-2105-10-168` `[VERIFIED-FULLTEXT]`:
alpha-sphere min radius **3.0 Å**, max radius **6.0 Å**, three clustering steps at
**1.73 / 2.5 / 4.0 Å**, minimum **35** alpha spheres per pocket. Whether the 4.2.3 defaults
are still these numbers is **unknown** — no reviewer read them off the binary.

### 3.4 How "random background residues" is built

Five distinct constructions, weakest first.

**(1) Uniform over all residues — implicit, and by far the most common.** Every residue-level
classifier does this by default without calling it a null. Visible in the reported balances:
DeepAllo **5.12 %** positive residues, "A huge class imbalance was detected", handled with
weighted cross-entropy and `scale_pos_weight`; Mariano et al. (STINGAllo precursor) "To
accommodate class imbalance (1:21), the model was initialized with a scale_pos_weight
parameter" `10.1016/j.csbj.2024.10.036`. Both `[VERIFIED-FULLTEXT]`. A 2026 kinase pLM study
reports allosteric sites have "the lowest fraction of positive residues (3.22 %), with 15,185
positives and 456,117 negatives" `[UNVERIFIED]`.

**(2) Surface-only random residues.** KeyAlloSite, `10.7554/eLife.81850`
`[VERIFIED-FULLTEXT]`: "For each protein in the data set, two residues that are not part of
the orthosteric and allosteric sites were randomly selected from the surface residues."

**(3) Size-matched contiguous patches grown around a random surface centre.** The strongest
geometry in the field, in exactly one paper. KeyAlloSite `[VERIFIED-FULLTEXT]`:

> "One was taken as the first center, and the residues around it with the same number as the
> residues in orthosteric pocket were selected as patch1; and the other residue was taken as
> the second center, and the residues around it with the same number as the residues in
> allosteric pocket were selected as patch2."

Compared with a Student's t-test. **But repeated only four times**: "The process was repeated
four times, and the mean and standard deviation of the evolutionary coupling strength were
calculated." Four draws cannot support a p-value at useful resolution.

**(4) Size- and diameter-matched "surrogate sites", 1,000 per protein — the Barahona/Yaliraki
lineage.** `10.1038/ncomms12477`, restated in `10.1016/j.patter.2021.100408` and ProteinLens
`10.1093/nar/gkab350` `[VERIFIED-FULLTEXT]`. Surrogate sites satisfy

> "(1) the number of residues is equal to the number of residues in the allosteric site, and
> (2) the diameter (maximum distance between any two atoms in the site) is smaller than that
> of the allosteric site. For each protein, 1,000 surrogate sites are generated."

D's fetch of Amor 2016 renders clause (2) as "their diameter…is **not larger than** that of
the allosteric site" — a wording difference that does not change the direction. Both are
one-sided.

**Note the diameter constraint is one-sided and therefore biased** (B, stated as a stated
weakness rather than a finding about the result): requiring surrogate diameter to be smaller
than the real site's makes surrogates more compact than the positive class, and whether that
inflates or deflates the comparison depends on whether the score is itself
compactness-correlated. The paper does not check. `[UNVERIFIED]` for the direction of the
bias; `[VERIFIED-FULLTEXT]` for the one-sidedness.

**(5) Distance-matched — exists, but only as a regression control inside one method.** Amor
et al., `10.1038/ncomms12477` `[VERIFIED-FULLTEXT]`:

> "the quantile score of a bond p_b is a measure of how high the propensity Π_b is relative
> to other bonds in the sample which are at a similar distance from the active site."

Quantile regression is fitted at p = 0.1 … 0.9, with Q0.90 as the working cutoff and Q0.99
for stringent detection. **This is the field's only systematic control for the
distance-from-active-site confound.** See §4.

**The one published chance-baseline formula for a short residue list.** PNAS 2024,
`10.1073/pnas.2414333121` `[VERIFIED-FULLTEXT]`:

> "For each ensemble, we evaluated the overlap, s = b ∩ h, between the b drug-binding
> residues and h global hinge residues."
> "p(s, N, h, b) = 1 − Σ_{i=0}^{s−1} [C(b,i) · C(N−b, h−i)] / C(N,h)"
> "The reciprocal 1/P provides a measure of enhancement compared to random, and a
> hypergeometric score of P ≤ 0.05 is usually considered significant."

Reported: average P = 4.547 × 10⁻³, average enrichment **4.13×** over random,
"32.53 ± 10.39 % of drug-binding sites colocalize with hinge regions".

The other three verified baseline constructions:

- **Surrogate/decoy sites** — Amor 2016, above, with "a 95% confidence interval for the
  average from a bootstrap with 10,000 resamples". `[VERIFIED-FULLTEXT]`
- **Expected number of residues to test** — CryptoSite `[VERIFIED-FULLTEXT]`: "on average
  7.6, 5.9, and 4.9 residues with the predicted residues score higher than 0.05, 0.1, and
  0.15, respectively, would need to be tested to find at least one true cryptic site residue
  – a significant improvement over the need to test 19 randomly chosen residues for the same
  outcome".
- **Positive-class proportion as the precision baseline** — LIGYSIS-bench
  `[VERIFIED-FULLTEXT]`: "Dashed line represents the baseline, i.e., proportion of observed
  binding residues = 0.1".

**And the absence.** Europe PMC `"allosteric site prediction" AND "random" AND "top 3"`
returned 6 relevant papers, **none reporting a chance baseline**;
`"binding site prediction" AND "random baseline"` returned 11 records, all off-topic
`[VERIFIED-FULLTEXT]`. APOP, PASSer, PASSerRank, AlloBench, fpocket, P2Rank, LIGSITEcsc,
PocketPicker, DeepSite, Kalasanty and PUResNet all report top-N success rates without stating
what a random ranker would achieve — even though APOP itself notes the candidate pocket count
"ranges from 10 to 242", which makes the random top-3 rate vary by more than an order of
magnitude inside its own benchmark.

### 3.5 Which papers state a test at all, and the count that do not

B's table over 18 allosteric/cryptic prediction papers and benchmarks:

| Paper                                 | DOI                              | Test                                                                                                                                             | Stated null                                          | α            | Multiplicity                                                     | Sided                  |
| ------------------------------------- | -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------- | ------------ | ---------------------------------------------------------------- | ---------------------- |
| Amor et al.                           | `10.1038/ncomms12477`            | quantile regression conditioned on distance + structural bootstrap vs 1,000 surrogates, 10,000 resamples → 95 % CI                               | **not formally stated**                              | none         | **none**                                                         | effectively one-sided  |
| Patterns benchmarking                 | `10.1016/j.patter.2021.100408`   | same; "If the average quantile score … is above the upper bound of the 95 % confidence interval, the allosteric site is assumed to be detected." | "does not explicitly state a formal null hypothesis" | none         | **none**                                                         | one-sided              |
| ProteinLens                           | `10.1093/nar/gkab350`            | same; 1,000 surrogates; bootstrap 95 % CI                                                                                                        | implicit                                             | none         | none                                                             | one-sided              |
| APOP                                  | `10.1093/bioinformatics/btad275` | **one-sided Wilcoxon signed-rank, P = 0.00088** vs AlloPred                                                                                      | paired ranking comparison                            | not stated   | **none**                                                         | **one-sided**          |
| CryptoSite                            | `10.1016/j.jmb.2016.01.029`      | **two-sample Kolmogorov–Smirnov**, e.g. P = 1.4 × 10⁻³; AUC 0.83; LOO CV                                                                         | feature distributions equal                          | not stated   | **none**                                                         | two-sided              |
| KeyAlloSite                           | `10.7554/eLife.81850`            | **Student's t-test, α = 0.05** vs two size-matched random surface patches (4 repeats)                                                            | means equal                                          | **0.05**     | **none** ("Bonferroni" does not appear in the text — B searched) | two-sided              |
| Guharoy & Chakrabarti (PPI, adjacent) | `10.1186/1471-2105-11-286`       | **Mann-Whitney U** on an inverse-distance clustering statistic vs 1,000 equal-size random subsets from the same interface; Z > 1.64              | observed clustering = random-subset clustering       | **P < 0.01** | **none** across 513 interfaces                                   | one-sided in practice  |
| ESSA                                  | `10.1016/j.csbj.2020.06.020`     | **No test.** z-score over all residues; "those lying in the top quartile (top 25%, z_i > 0.59)"                                                  | —                                                    | —            | —                                                                | —                      |
| Thayer et al.                         | `10.1371/journal.pone.0188616`   | **No test.** Success rates + sd from random 20 % residue subsets                                                                                 | —                                                    | —            | —                                                                | —                      |
| AlloPred                              | `10.1186/s12859-015-0771-1`      | **No test.** LOO + 20 random splits                                                                                                              | —                                                    | —            | —                                                                | —                      |
| PASSer2.0                             | `10.3389/fmolb.2022.879251`      | **No test.**                                                                                                                                     | —                                                    | —            | —                                                                | —                      |
| PocketMiner                           | `10.1038/s41467-023-36699-3`     | **No test, no CI.**                                                                                                                              | —                                                    | —            | —                                                                | —                      |
| CryptoBench                           | `10.1093/bioinformatics/btae745` | **No test.** "no formal statistical testing or null distribution analysis"                                                                       | —                                                    | —            | —                                                                | —                      |
| AlloBench                             | `10.1021/acsomega.5c01263`       | **No test.** "No formal statistical significance testing or null distribution analysis is reported."                                             | —                                                    | —            | —                                                                | —                      |
| DeepAllo                              | `10.1093/bioinformatics/btaf294` | **No test.**                                                                                                                                     | —                                                    | —            | —                                                                | —                      |
| Allo-PED                              | `10.1101/2025.03.28.645953`      | **No test.** mRMR + ROC with Youden's index                                                                                                      | —                                                    | —            | —                                                                | —                      |
| STINGAllo                             | `10.1093/bib/bbaf424`            | **No test, no CI, no correction.**                                                                                                               | —                                                    | —            | —                                                                | —                      |
| Mariano et al.                        | `10.1016/j.csbj.2024.10.036`     | **Kolmogorov–Smirnov** on feature distributions; **no p-values reported in text**                                                                | —                                                    | —            | —                                                                | —                      |
| Kovačev-Nikolić et al.                | `10.1515/sagmb-2015-0057`        | permutation test on persistence landscapes, open vs closed MBP conformer groups                                                                  | groups exchangeable                                  | unknown      | unknown                                                          | unknown `[UNVERIFIED]` |

All rows `[VERIFIED-FULLTEXT]` except the last.

**Tally, verbatim from B:**

- **5** state an actual inferential procedure (the Amor lineage ×3 counted as one family; APOP;
  CryptoSite; KeyAlloSite; plus Guharoy & Chakrabarti from the adjacent PPI literature).
- **13 claim their method works with no stated statistical test at all** — they report AUC,
  F1, MCC, top-1/top-3, or DCC/DCA hit rate, and stop.
- **0** apply any multiplicity correction. Not one.
- **0** state a null hypothesis in words.
- **1** states sidedness explicitly (APOP).

**D reached the same count from a different corpus and different queries** (convergent: B, D).
Of D's 17 method rows: one lineage (Barahona–Yaliraki) has a genuine distance-aware,
geometry-matched null; one (APOP) runs a paired significance test, but on a _between-methods_
comparison rather than method-vs-null; "everything else validates by showing that known
residues appear near the top of a ranking, with no null distribution at all."

**Confidence intervals: none on any AUC.** PubMed
`"allosteric" AND "bootstrap" AND "confidence interval"` → **0 hits** `[VERIFIED-FULLTEXT]`.
Not one of the 18 papers reports a DeLong, Hanley–McNeil or bootstrap CI on an AUC.
PocketMiner reports a 5-fold-CV mean ROC-AUC with no CI and no spread; CryptoBench reports a
seven-metric table with no CI on any cell; STINGAllo reports F1/MCC with no CI. The only
bootstrap CIs anywhere in this literature are on the **site-score statistic**: "A 95%
confidence interval is obtained for each protein to assess the statistical significance by
using bootstrap with 10,000 resamples with replacement" `10.1016/j.patter.2021.100408`
`[VERIFIED-FULLTEXT]`.

DeLong is the field-standard parametric AUC CI, exploiting the AUC/Mann-Whitney-U identity
`[UNVERIFIED]` — B's source is pROC documentation, not a paper. The documented caveat, same
source, `[UNVERIFIED]`: "DeLong assumes asymptotic normality of the AUC sampling
distribution; it can give narrow, anti-conservative intervals at very small sample sizes
(under 30 per class). Additionally, the variance formula assumes independence of
observations; for clustered data use cluster-bootstrap CIs."

**Effect sizes: essentially never reported.** No paper in either review reports Cliff's delta,
rank-biserial correlation, or a standardised enrichment. MEF-AlloSite reports Cohen's d, but
over a distribution of repeated runs on a fixed dataset, so its denominator is run-to-run
variance, not protein-to-protein variance (`evaluation-protocol-lit.md` §3.1,
`[VERIFIED-FULLTEXT]` for the method, `[UNVERIFIED]` for the inference). One
effect-size-adjacent statement surfaced — enrichment factor 254 %, p = 0.0155, for PTMs at
allosteric hotspots — and B marks it **do not cite**, source not fetched `[UNVERIFIED]`.

### 3.6 Spatial autocorrelation and residue non-independence

The allosteric label set is a spatially contiguous patch. Residue-wise sampling therefore
overstates the number of independent observations. **B searched hard for anyone
acknowledging this and can quantify the absence.**

Evidence of absence, all `[VERIFIED-FULLTEXT]` for the counts:

- PubMed `allosteric AND "permutation test"` → **1 hit**. That hit — Kovačev-Nikolić et al.
  2016, `10.1515/sagmb-2015-0057` — permutes **groups of protein structures** (open vs closed
  maltose-binding protein) to test a persistence-landscape statistic. It is a two-sample test
  between conformational ensembles and **does not address residue-level contiguity at all**
  `[UNVERIFIED]` for the content.
- PubMed `"allosteric" AND ("null model" OR "null distribution")` → **1 hit**: Thayer et al.
  2017, `10.1371/journal.pone.0188616`, which builds a null by selecting "20% of the protein
  residues … at random" while fixing endpoints and asks how often a contiguous pathway
  appears. Reported as success rates with standard deviations — PDZ 51 % (sd 0.12), p53 30 %
  (sd 0.078), MutS 3 % (sd 0.11) — and **no p-values at all**. B's targeted extraction on the
  independence question: "This critical issue is NOT discussed. The authors make no
  acknowledgment that spatially contiguous residue selections violate statistical
  independence assumptions."
- PubMed `protein AND "spatial autocorrelation" AND residue` → **1 hit**, and it is about
  amino-acid replacement rates in a receptor family (Marsh 2009,
  `10.1007/s00239-008-9183-4`), not binding sites.
- arXiv `all:"decoy pocket"` → **0**.
- The two most-cited benchmarking papers explicitly do not discuss it. Targeted extraction of
  the Patterns paper: "No explicit discussion of residue non-independence or spatial
  autocorrelation concerns appears in the provided text." Allo-PED: "Not mentioned."

**Partial credit where due.** KeyAlloSite's random patches are genuinely contiguous by
construction — the correct null geometry, undermined by n = 4 repetitions. The Barahona
surrogate sites are diameter-bounded, which is a _partial_ contiguity constraint: a residue
set with bounded diameter is compact but not necessarily connected. Both
`[VERIFIED-FULLTEXT]`.

**Adjacent machinery that exists and has not crossed into this field:**

| Machinery                                                         | What it does                                                                                                                                                                                                                                                                                                                                                             | Source                                                                          | Tag                          |
| ----------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------- | ---------------------------- |
| **Inverse-distance clustering statistic with 1,000 permutations** | Mann-Whitney U comparing observed clustering against "random subsets of equivalent size from the same interface", 1,000 permutations per interface, P < 0.01, Z > 1.64, **no multiple-testing correction across 513 interfaces**. The correct shape of test — matched-size random subsets from the same object — applied to PPI interfaces rather than allosteric sites. | Guharoy & Chakrabarti 2010, `10.1186/1471-2105-11-286`                          | `[VERIFIED-FULLTEXT]`        |
| **Local Moran's I on protein structures**                         | Applied to conservation scores using Cβ atoms as nodes and residue contacts as edges; Moran scatterplot shows positive spatial autocorrelation of conservation.                                                                                                                                                                                                          | PMC3533907                                                                      | `[UNVERIFIED]` — not fetched |
| **Spatial-autocorrelation-preserving nulls (neuroimaging)**       | "spin tests" and generative surrogate maps that randomise topography while preserving autocorrelation structure. Stated motivation transfers exactly: "The assumptions built into the null hypotheses of permutation testing are strongly violated by … spatial autocorrelation". A mature solution to this problem in a neighbouring field.                             | neuromaps null-models docs; Burt et al., _NeuroImage_ 2020 — **DOI unverified** | `[UNVERIFIED]`               |

**The magnitude of the effect, measured on protein structures.** This is the strongest
quantitative evidence and it comes from `evaluation-protocol-lit.md` §2.1, retrieved
2026-08-20, `[VERIFIED-FULLTEXT]`. Guharoy & Chakrabarti 2010, `10.1186/1471-2105-11-286`:
surface patches defined by nearest-neighbour growth (15 Å radius for complexes, 22 Å for
homodimers); null = "subsets of residues (of the same size as the number of conserved
residues) … selected randomly" from the same interface, 1,000 random subsets. Result:

> "In 96.7% (117/121) homodimeric and 87.7% (341/389) protein complex interfaces, randomly
> selected groups of residues were indeed less clustered" (P < 0.01)

Overall significance by Mann-Whitney U: homodimers P = 1.57e-04, complexes P = 9.64e-14.
**Functionally labelled residues beat a size-matched random-subset null in roughly 90 % of
cases by virtue of being clustered.** They used clustering as signal; a propagation-method
evaluation must treat it as nuisance. Same phenomenon.

**The theoretical argument.** Milenkovic, Filippis, Lappe & Przulj, "Optimized null model for protein structure
networks", `10.1371/journal.pone.0005967` `[VERIFIED-FULLTEXT]`, compared Erdős–Rényi,
degree-preserving, Barabási–Albert and stickiness-index models against 3D geometric random
graphs on residue interaction graphs. The load-bearing sentence:

> "all non-geometric models … tend to identify as significantly (under-) over-represented
> almost all analyzed subgraphs"

whereas "GEO-3D model exhibits the highest 'specificity' … only 5–11 out of 29 subgraphs …
are identified as (anti-)motifs". Conclusion: "The choice of a well-fitting null model is
crucial."

**B's bottom line, recorded as its reasoning rather than as a retrieved number**
`[UNVERIFIED]`: for a 250-residue protein with a 15-residue contiguous allosteric patch, the
effective number of independent observations is closer to the number of independent surface
patches (order 15–25) than to 250; every p-value in this literature computed under
residue-wise exchangeability is anticonservative by roughly an order of magnitude in
effective n; and nobody says so.

---

## 4. How the network and elastic-network family validates itself

From D. This is the sub-family the project's own method belongs to, so its validation
conventions are the ones a reviewer will apply.

### 4.1 The method-validation table

| #   | Method                                       | Year      | DOI                                                | Network definition                                                                                                                                                                                                                           | Propagated quantity                                                                                                                                                             | Baselines compared against                                                                                                                                           | Statistical test                                                                                                                                       | N proteins                                        |
| --- | -------------------------------------------- | --------- | -------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------- |
| 1   | **Chennubhotla & Bahar**                     | 2007      | `10.1371/journal.pcbi.0030172`                     | residue nodes, **4 Å** atom–atom contact; `a_ij = N_ij/(N_i × N_j)`                                                                                                                                                                          | discrete-time Markov chain; **hitting time** "the expected number of steps it takes to send information from residue v_i to residue v_j"; commute time `C(i,j) = H(i,j)+H(j,i)` | **none explicitly stated**                                                                                                                                           | mean hit times ± s.d. only. **No formal test**                                                                                                         | **5** enzymes                                     |
| 2   | **Amor, Schaub, Yaliraki & Barahona**        | 2016      | `10.1038/ncomms12477`                              | **atomistic**; atoms = nodes, covalent + non-covalent bonds weighted by bond energies; **no distance cutoff** — "since there is no cutoff distance for interactions, both weak and long-range interactions within a protein can be captured" | edge-to-edge transfer matrix; residue propensity                                                                                                                                | prior methods cited, **no head-to-head numbers**                                                                                                                     | quantile regression on distance from the active site; structural bootstrap vs 1,000 surrogates; reference set of 100 SCOP proteins, 465,409 weak bonds | **20**                                            |
| 3   | **ProteinLens**                              | 2021      | `10.1093/nar/gkab350`                              | same atomistic graph                                                                                                                                                                                                                         | propensity + Markov transient half-times                                                                                                                                        | none                                                                                                                                                                 | same as row 2                                                                                                                                          | 113 proteins / 118 sites                          |
| 4   | **Wu, Strömich & Yaliraki**                  | 2021/22   | `10.1016/j.patter.2021.100408`                     | same                                                                                                                                                                                                                                         | same + two site-level statistics                                                                                                                                                | none head-to-head                                                                                                                                                    | structural bootstrap; added `P(p_R,allosteric site > 0.95)` and a SCOP-reference measure                                                               | **146** proteins / **432** structures             |
| 5   | **ESSA**                                     | 2020      | `10.1016/j.csbj.2020.06.020`                       | Cα ENM + heavy atoms as extra nodes; **GNM 10 Å, ANM 15 Å**, γ = 1                                                                                                                                                                           | z-scored shift in soft-mode eigenvalues, "the mean over the softest ten modes"                                                                                                  | **PARS, AllositePro**                                                                                                                                                | **none reported**                                                                                                                                      | 25 monomers; 24 structures / 12 proteins apo+holo |
| 6   | **APOP**                                     | 2023      | `10.1093/bioinformatics/btad275`                   | Cα GNM, **10 Å**, γ = 1.0; pocket springs stiffened to γ = 10.0                                                                                                                                                                              | shift in global mode frequencies, 50/50 with fpocket hydrophobic density                                                                                                        | **AlloPred, PASSer**                                                                                                                                                 | **one-sided Wilcoxon signed-rank, p = 0.00088**                                                                                                        | **104**                                           |
| 7   | **Ohm**                                      | 2020      | `10.1038/s41467-020-17618-2`                       | residue nodes; contact = any two atoms within **3.4 Å**; `P_ij = 1 − e^(−α·N_ij)`, α = 3.0                                                                                                                                                   | **ACI** = frequency a residue is reached over **10,000** stochastic rounds seeded at the active site                                                                            | **Amor et al., PRS, hitting time, shortest paths, native contacts**; negative control = non-allosteric four-helix bundle **1MFT**                                    | convergence analysis only. "No formal null-model or permutation test reported"                                                                         | **20**                                            |
| 8   | **SPACER**                                   | 2013      | `10.1093/nar/gkt460`                               | residue interaction graph                                                                                                                                                                                                                    | local closeness; binding leverage; leverage coupling                                                                                                                            | **none**                                                                                                                                                             | "No formal dataset, baseline comparisons, or statistical significance testing are reported."                                                           | **1** case study                                  |
| 9   | **STRESS**                                   | 2016      | `10.1016/j.str.2016.03.008` (DOI unverified in D)  | all-atom Monte Carlo surface probing; ANM modes                                                                                                                                                                                              | binding leverage → surface-critical residues                                                                                                                                    | **unknown**                                                                                                                                                          | **unknown**                                                                                                                                            | **unknown**                                       |
| 10  | **PARS**                                     | 2014      | `10.1093/bioinformatics/btu002`                    | fpocket pockets on an NMA/ENM backbone                                                                                                                                                                                                       | flexibility change on pocket occupancy + structural conservation                                                                                                                | unknown in the original; externally measured at 2/14 apo and holo by ESSA                                                                                            | unknown                                                                                                                                                | unknown                                           |
| 11  | **AlloPred**                                 | 2015      | `10.1186/s12859-015-0771-1`                        | ENM with stiffened pocket springs                                                                                                                                                                                                            | perturbation effect **at the active site**, then SVM over pocket features                                                                                                       | unknown in the original; externally measured at 68 % (34/50) by APOP                                                                                                 | SVM cross-validation                                                                                                                                   | unknown                                           |
| 12  | **MCPath**                                   | 2013      | `10.1093/nar/gkt284` (DOI unverified in D)         | residue network, atomistic potential                                                                                                                                                                                                         | ensemble of maximum-probability Monte Carlo paths                                                                                                                               | **none**                                                                                                                                                             | unknown                                                                                                                                                | **2** case studies                                |
| 13  | **AlloSigMA / AlloSigMA 2**                  | 2017/2020 | DOI unverified                                     | SBSMMA, per-residue                                                                                                                                                                                                                          | allosteric free energy per residue                                                                                                                                              | unknown                                                                                                                                                              | unknown                                                                                                                                                | unknown                                           |
| 14  | **Sethi et al., dynamical network analysis** | 2009      | `10.1073/pnas.0810961106`                          | dynamic contact map **from an MD trajectory**; correlation-weighted edges; Girvan–Newman                                                                                                                                                     | communities + optimal/suboptimal paths                                                                                                                                          | none                                                                                                                                                                 | unknown                                                                                                                                                | **2** complexes                                   |
| 15  | **CTQW centrality for protein RINs**         | 2026      | `10.1021/jacs.6c08053` (preprint arXiv:2604.17486) | **Cα nodes**; "two residues i and j were considered connected if the Euclidean distance between their C-α atoms … satisfied the cutoff criterion d_ij < 8 Å"; weight "w_ij = 1/(d_ij)^2"                                                     | long-time-average occupation probability of a CTQW with **H = A**, from a **uniform superposition** initial state                                                               | **eigenvector centrality** (primary); classical random walk (spectral gap only)                                                                                      | Spearman ρ, Kendall τ, Overlap@k, Jaccard as **agreement** statistics. **No null model, no permutation test, no AUC**                                  | **~150**                                          |
| 16  | **Erman, GNM for KRAS allostery**            | 2026      | `10.1088/1478-3975/ae3e49`                         | GNM Kirchhoff matrix; cutoff sensitivity examined                                                                                                                                                                                            | dynamic distance `R_ij`; edge centrality `w_ij·R_ij`; entropy sensitivity `∂S/∂δ`                                                                                               | argues **against** degree — "local measures such as degree are insufficient to capture long-range allosteric coupling" — but **"no formal quantitative comparison"** | B-factor correlation; cutoff-sensitivity slope **0.013 ± 0.034 (95 % CI)** beyond 7.8 Å                                                                | **1** (KRAS)                                      |
| 17  | **ZHMolEReP**                                | 2026      | `10.1021/acs.jcim.6c00141`                         | PRS on an ENM; seven-feature representation                                                                                                                                                                                                  | PRS + free-energy response                                                                                                                                                      | unknown                                                                                                                                                              | unknown                                                                                                                                                | **40** `[UNVERIFIED]`                             |

Rows 1–8, 15, 16 `[VERIFIED-FULLTEXT]`; rows 9–14, 17 `[UNVERIFIED]` in whole or in part as
noted.

### 4.2 The baseline question — who compares against plain graph geometry

| Baseline                                                | Papers that include it                                                                                                                                                                                     | Papers that do not                                                                                                  |
| ------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Euclidean distance from the active site**             | **Amor 2016** — regressed out via quantile regression, **not compared as a rival ranker**; **ProteinLens 2021** — same; **Wu 2022** — inherits it; **AlloBench 2025** indirectly and damningly (see below) | Ohm ("Distance control: Not explicitly stated"), ESSA, APOP, SPACER, PARS, AlloPred, MCPath, CTQW, Erman — **none** |
| **Degree centrality / contact number**                  | **Erman 2026** argues against it qualitatively, runs **no quantitative comparison**; **Malik 2018** measures it descriptively                                                                              | Amor 2016, ProteinLens, Wu 2022, Ohm, ESSA, APOP, SPACER, PARS, AlloPred, CTQW — **none**                           |
| **Eigenvector centrality**                              | **CTQW 2026** — the _only_ paper in this family that makes it the primary named baseline                                                                                                                   | all others                                                                                                          |
| **Betweenness centrality**                              | **Malik 2018** descriptively. Widely used _as a method_ (85 PubMed records) but rarely _as a control against a propagation score_                                                                          | Amor 2016, Ohm, ESSA, APOP, CTQW                                                                                    |
| **Closeness centrality**                                | **SPACER 2013** uses "local closeness" as one of its own predictors, so it exists as a _method_; **Malik 2018** descriptively                                                                              | all propagation papers                                                                                              |
| **Classical random walk / diffusion on the same graph** | **Ohm 2020** compares ACI against **hitting time**, shortest paths and native contacts; **CTQW 2026** compares classical vs quantum _spectral gap_ only, not classical vs quantum _ranking_                | Amor 2016, ESSA, APOP, SPACER, PARS, AlloPred, Erman                                                                |

All `[VERIFIED-FULLTEXT]` except the AlloBench correlation claim, below.

**Does anyone criticise the omission in print?** Partially, and less directly than would be
useful. What D found:

1. AlloBench criticises the field's _benchmarking_ practice — "a systematic study
   quantitatively comparing the performance of the available allosteric site prediction tools
   on a common test set has yet to be performed" `[VERIFIED-FULLTEXT]` — but that is about
   sample size and common test sets, not missing geometric baselines.
2. AlloBench then makes an admission that functions as a criticism: that "the strong
   correlation between the JI and inverse distance indicates that the JI is a robust
   estimator of the proximity of the known and predicted allosteric site". **In other words
   the field's newest common metric is, by its own authors' description, substantially a
   distance measure.** D marks this `[UNVERIFIED]`; E fetched the same sentence at full text
   `[VERIFIED-FULLTEXT]`, so the sentence is verified, and E adds a caution: it describes the
   distance between _predicted_ and _known_ site, and says nothing about accuracy as a
   function of distance from the _active_ site. Do not cite it for the latter.
3. **ProteinLens names the confound and treats it as a defect requiring correction**
   `[VERIFIED-FULLTEXT]`: "The distribution of bond-to-bond propensities declines with
   distance from the chosen source, whereas Markov Transient half-times increase with
   distance… To account for this distance bias, we use quantile regression into our
   workflow", adding that this is "especially important for long-range effects like
   allostery".
4. Ohm implicitly criticises pure-topology scores by including shortest paths and native
   contacts as baselines and beating them. It does not name the confound.
5. Betweenness-specific criticism exists but is about path enumeration, not confounding:
   "edges and nodes that lie 'near to' but not exactly on the shortest path may provide
   relevant contributions [and] will be ignored by a standard betweenness centrality
   computation" and "betweenness centrality may contain contributions from paths that are not
   relevant to transmitting a signal between the domains of interest" `[UNVERIFIED]`. That
   cuts the other way: betweenness is a weak baseline, so beating it proves less.

**What D did not find, and how hard it looked.** Three targeted searches plus one on the
burial variant. **No paper says, in so many words, that a method's reported enrichment is not
shown to exceed a centrality or distance baseline and that this invalidates the claim.** The
one query designed to find exactly that phrasing **was not run** because the search budget ran
out. The negative finding should be read as strongly suggested by four converging searches,
**not exhaustively established**.

### 4.3 The published name for the distance confound

**"Distance bias."** One name, and it is narrow. ProteinLens, `10.1093/nar/gkab350`
`[VERIFIED-FULLTEXT]`, uses exactly that phrase for the distance-decay component: "To account
for this distance bias, we use quantile regression into our workflow."

There is **no established name for the broader confound** — that a propagation score is
approximately a centrality. The CTQW paper describes it without naming it. D's conclusion: do
not invent a term; use "distance bias" for the distance component with ProteinLens as the
citation, and describe the centrality component in plain words.

**The functional form is published; the magnitude is not.** Amor 2016 `[VERIFIED-FULLTEXT]`:
"the observed exponential decay of Π with d", hence `log(Π_b) ∝ β₀ + β₁·d_b` as the
quantile-regression model. But:

> **Variance in a propagation score explained by distance alone (R², or AUC of a
> distance-only ranker): no published value exists.** D searched and found none.

The literature has _named_ the confound, _modelled_ it as log-linear decay, and _corrected_
for it — and has never _quantified_ it.

### 4.4 The quantum-walk-against-eigenvector-centrality result

The single published quantum-walk-on-protein-networks paper: `10.1021/jacs.6c08053`, preprint
arXiv:2604.17486, 2026. All `[VERIFIED-FULLTEXT]`.

| Measurement                                                                                          | Value                                                                                                                                                                                                                        |
| ---------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Rank correlation between CTQW centrality and **eigenvector centrality** across ~150 proteins         | **Spearman ρ mean ≈ 0.94, range 0.58–1.00, median ≈ 0.96**; **Kendall τ mean ≈ 0.84, range 0.49–1.00, median ≈ 0.87**                                                                                                        |
| Top-_k_ set overlap, CTQW vs eigenvector, on PKA (336 residues)                                      | **18 of top 20 shared; 23 of top 26 shared**                                                                                                                                                                                 |
| The paper's own headline functional-recovery metric on PKA ("key score")                             | **CTQW 16.75 %, eigenvector 15.21 %, random 8 %**                                                                                                                                                                            |
| Functional-residue recovery on PKA                                                                   | 8 of top-26 (≈31 %) vs 8 % random                                                                                                                                                                                            |
| Partial correlation controlling for degree, or a direct CTQW-vs-degree / CTQW-vs-distance comparison | **Not done.** The paper's own limitation statement: "The paper does not report partial correlation (CTQW score vs. eigenvector, controlling for degree) or compare CTQW vs. degree centrality directly on the same dataset." |

**Read the third row carefully.** The quantum method's margin over the classical baseline is
**1.54 percentage points**, against an 8.75-point margin over random — roughly **85 % of the
above-random signal is shared with eigenvector centrality**.

**Caveat that bounds the transfer.** The CTQW initial state is a **uniform superposition**,
not a localised active-site source. So this measures how much of _global_ quantum-walk
centrality is classical spectral centrality; it does not directly bound the source-localised
case.

The paper's own open question, verbatim `[VERIFIED-FULLTEXT]`: "This leaves open whether
quantum walk benefits over classical methods arise purely from multi-eigenmode contributions
or are driven by underlying degree/distance structure shared across all methods."

**The cautionary precedent for the classical-propagator comparison.** Ohm ran a classical
walk on the same graph from the same source and found a **dead tie**: on CheY top-20 residue
pairs, Ohm 47.6 %, **hitting time 47.6 %**, native contacts 38.1 %, shortest paths 33.3 %,
PRS 33.3 % `[VERIFIED-FULLTEXT]`.

### 4.5 What nobody controls for

**Burial and solvent accessibility: nobody, in this family.** D's finding, stated as
requested:

> _No method in the network-propagation or elastic-network family of allosteric-site
> predictors controls for solvent accessibility or burial when claiming that known allosteric
> residues score above background. Patch contiguity is controlled by one research group
> (Barahona/Yaliraki, via a size- and diameter-matched structural bootstrap) and by nobody
> else. The remaining methods either restrict the candidate set to geometric pockets — an
> implicit and unstated control — or apply no control at all._

How hard D looked: two dedicated searches plus one targeting partial correlation on burial
depth / RSA / contact number. All three returned general protein-bioinformatics literature on
_predicting_ RSA and nothing on using RSA as a control in allosteric-site enrichment. Direct
inspection of the methods sections of Amor 2016, Wu 2022, ESSA and APOP: burial appears as a
_feature_ — APOP uses fpocket local hydrophobic density as half its score — but never as a
_covariate to be held fixed_. APOP's limitation stated flatly by the source: **"No explicit
controls for pocket size or burial depth reported."** `[VERIFIED-FULLTEXT]`

What exists instead, and why it is not a substitute: Malik 2018 reports descriptively that
hydrophobic residues in allosteric communication sub-systems have significantly higher
thermal fluctuations than in the non-ACSS part `[VERIFIED-FULLTEXT]`; and the RIN literature
records "a positive correlation between node degree and hydrophobicity, implying that hub
nodes in protein contact networks tend to be hydrophobic, with hydrophobic residues generally
lying in the core" `[UNVERIFIED]`. So burial → degree → connectivity score is a documented
chain with no documented control anywhere along it.

**One structural nuance that changes who needs the control.** APOP, PARS, AlloPred, PASSer and
ESSA+fpocket all score **fpocket-detected pockets**, not free residue sets. Their candidate
set is already restricted to objects that are contiguous and cavity-like **by construction**.
That is an _implicit_ contiguity control living in the candidate set rather than in the
statistics — and a residue-level method does not get it for free. `[VERIFIED-FULLTEXT]` for
the detector use; `[UNVERIFIED]` for the inference.

### 4.6 Coarse-graining: three validation traditions that prove different things

| Tradition                                                           | What it measures                                                                                                                                                                                                                                                                                                                                                                                                                                        | Primary source                                                                                           | Tag                   |
| ------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- | --------------------- |
| **(a) Mode overlap / cumulative overlap** — the dominant convention | overlap between a normal mode and a reference displacement vector, usually an experimentally observed apo→holo conformational change; cumulative overlap "gives a number between 0 and 1 describing how well the best combination of the specified modes can describe the conformational change"; reported CG-vs-atomistic overlaps reach **0.97**                                                                                                      | usually attributed to Marques & Sanejouand 1995, _Proteins_ 23:557–560 — **DOI unverified, not fetched** | `[UNVERIFIED]`        |
| **(b) Spectral preservation**                                       | Gfeller & De Los Rios, verbatim abstract: "we use random walks to design a coarse-graining scheme for complex networks. By construction the coarse-graining preserves the slow modes of the walk, while reducing significantly the size and the complexity of the network… keeping most of their relevant spectral properties." **The specific error measure used inside the paper was not recoverable from the abstract page.**                        | `10.1103/PhysRevLett.99.038701`                                                                          | `[VERIFIED-ABSTRACT]` |
| **(c) Exact-integration consistency**                               | Diggins et al.: cost function is "a simple measure of the consistency between the harmonic approximation of an elastic network model and the harmonic model obtained through exact integration of the discarded degrees of freedom". Headline: "Our analysis quantifies the substantial impact that an algorithm-driven selection of coarse-grained sites can have on a model's properties" — i.e. **which** nodes you keep matters, not just how many. | `10.1021/acs.jctc.8b00654`                                                                               | `[VERIFIED-FULLTEXT]` |
| **(d) Mixed coarse-graining**                                       | high resolution at the functional site, low elsewhere; validated by showing the slowest modes survive                                                                                                                                                                                                                                                                                                                                                   | Kurkcuoglu, Jernigan & Doruker, _Polymer_ 2004 — **DOI unverified**                                      | `[UNVERIFIED]`        |

**Tradition (a) requires a holo structure.** Overlap is conventionally computed against an
apo→holo displacement vector. That makes the field's dominant coarse-graining validation
unavailable as a prediction-side check under an apo-only constraint; it can only ever be
evaluation-side.

### 4.7 Cutoff robustness, noise, and ranking stability

**Cutoff.** Dubanevics & McLeish 2022, `10.1016/j.jmb.2022.167696`, verbatim abstract
`[VERIFIED-ABSTRACT]`:

> "(1) balancing B-factor and dispersion-relation predictions, a near-universal optimal value
> of 8.5 Å is advisable for ENMs; (2) inhomogeneity in elasticity brings the first mode
> containing spatial structure not well-resolved by the ENM typically within the first 20;
> (3) the BENM only affects modes in the upper third of the distribution… (4) BENM does not
> typically affect fluctuation-allostery"

Three proteins: CAP, GST, SARS-CoV-2 Mpro. Note **8.5 Å is a Cα cutoff**, a different object
from a heavy-atom contact cutoff; the two are not comparable.

Erman 2026 reports the only cutoff-sensitivity _statistic_ D found: slope
**0.013 ± 0.034 (95 % CI)** beyond 7.8 Å on KRAS `[VERIFIED-FULLTEXT]`. **The CI straddles
zero** — a null result presented as robustness, which is a legitimate but weak form of the
claim.

**Coordinate noise.** D found **no paper in the allosteric-prediction family that perturbs
input coordinates and measures ranking degradation.** The nearest things are ENM parameter
sweeps and general network-science work on centrality stability under edge removal
`[UNVERIFIED]`.

**Ranking stability statistics.** No convention inside the sub-field, because almost nobody
measures it. The single closest precedent is CTQW 2026, which reports **four** agreement
statistics side by side when comparing two rankings on the same protein set
`[VERIFIED-FULLTEXT]`: Spearman ρ ("Mean ~0.94 (range 0.58–1.00); tight clustering near
unity"), Kendall τ ("Mean ~0.84 (range 0.49–1.00); broader spread reflecting pairwise
discrepancies"), Overlap@k, and Jaccard ("Strong agreement, broader spread due to stricter
normalisation"). From the wider network-science literature `[UNVERIFIED]`: Kendall τ is "the
standard measure" for comparing centrality rankings between an original and a perturbed
network, and Rank-Biased Overlap is the top-weighted alternative — "unlike traditional metrics
like Kendall Tau, RBO is weighted, giving more importance to higher-ranked items"; primary
reference Webber, Moffat & Zobel, ACM TOIS 28(4), 2010, **DOI not verified**. **D found zero
use of RBO anywhere in the protein-allostery literature.**

### 4.8 Two premise-level disagreements inside this family

**Are allosteric residues network hubs?** Two findings point in opposite directions and D
records both without resolving them.

- The centrality-confound argument assumes yes; the RIN literature supports the
  burial→degree chain `[UNVERIFIED]`.
- **Malik, Banerji, Kouza, Buhimschi & Kloczkowski 2018**, arXiv:1802.10207,
  `10.48550/arXiv.1802.10207` `[VERIFIED-FULLTEXT]`, analysed allosteric communication
  sub-systems across four ASD protein classes and found **low degree centrality and low
  closeness centrality** in ACSS residues across all groups, betweenness showing "nonuniform
  behavior", and most ACSSs **not** small-world. Control: the non-ACSS part of the same
  protein.
- **Erman 2026** agrees directionally: "local measures such as degree are insufficient to
  capture long-range allosteric coupling" `[VERIFIED-FULLTEXT]`.

D's own note on a possible reconciliation, marked as a category distinction rather than a
resolution: Malik studies _pathway_ residues (ACSS), which are a different object from
_allosteric site_ residues, so the two findings may be about different residue classes.

**Do allosteric communication pathways exist at all?** The entire pathway-prediction
literature assumes yes. **Stock & Hamm 2018**, `10.1098/rstb.2017.0187`, used time-resolved
IR plus non-equilibrium MD on a photoswitchable PDZ2 and found "the absence of well-defined
communication pathways", concluding that "allosteric communication shares some properties
with downhill folding, except that it is an 'order-order' transition"
`[VERIFIED-FULLTEXT]`/`[UNVERIFIED]` — D tags this row F/S. This is a direct experimental
challenge to the premise of every pathway method in §4.1.

---

## 5. Performance bands, and what "good" is here

Merged from A, D and E, with the earlier file's §3 folded in. This section exists so a reader
can judge whether a given result is publishable in this sub-field.

### 5.1 Self-reported top-N band (pocket level)

| Paper                              | Definition used                                | Reported                                                                                                                                                                                | DOI                              |
| ---------------------------------- | ---------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------- |
| PARS 2014                          | position of first matching cavity              | **44 % top-1, 73 % top-3** of 102 proteins                                                                                                                                              | `10.1093/bioinformatics/btu002`  |
| AlloPred 2015                      | raw counts, top-1 and top-2                    | **23/40** and **28/40**; CV mean 23.6/40. AlloSite 21/40, PARS 10/40 on the same set. **No AUC, accuracy, sensitivity, specificity or MCC reported**                                    | `10.1186/s12859-015-0771-1`      |
| PASSer 2021                        | top-1 / top-3 %                                | **60.7 % / 84.9 %**; accuracy 0.974, recall 0.847, precision 0.726, F1 0.782, ROC AUC 0.914                                                                                             | `10.1088/2632-2153/abe6d6`       |
| PASSer2.0 2022                     | top-1 / top-3 %                                | **65.1 % / 82.7 %**; precision 0.850, recall 0.616, F1 0.701                                                                                                                            | `10.3389/fmolb.2022.879251`      |
| PASSerRank 2023                    | top-3 %                                        | **83.6 %** (ASD), **80.5 %** (CASBench)                                                                                                                                                 | `10.48550/arXiv.2302.01117`      |
| APOP 2023                          | top-3 success count                            | **92/104 = 88.5 %**; **84 % (42/50)** on the holo subset vs AlloPred 68 % (34/50) and PASSer 76 % (38/50); P = 0.00088 one-sided Wilcoxon vs AlloPred                                   | `10.1093/bioinformatics/btad275` |
| KeyAlloSite 2023                   | top-1/2/3 by z-score                           | **56.0 % / 76.0 % / 96.0 %**; recall 0.92 (23/25 with Z > 0.5)                                                                                                                          | `10.7554/eLife.81850`            |
| DeepAllo 2025                      | **top 1 %, 3 %, 5 %, 10 %** of the ranked list | **90.5 %** of allosteric pockets in top-3; best F1 89.66 %, precision 92.3 %, recall 88.14 %                                                                                            | `10.1093/bioinformatics/btaf294` |
| ESSA 2020                          | x/14 sites recovered                           | **holo 10/14, apo 7/14**                                                                                                                                                                | `10.1016/j.csbj.2020.06.020`     |
| Bond-to-bond propensity 2016       | site detected by ≥1 of 4 measures              | **19/20 (95 %)**; by ≥3 of 4: **15/20 (75 %)**                                                                                                                                          | `10.1038/ncomms12477`            |
| Bond-to-bond propensity, scaled up | ASBench, with allosteric ligand present        | **106/118 structures (89.8 %)**; ≥3 measures **81/118 (68.6 %)**                                                                                                                        | `10.1016/j.patter.2021.100408`   |
| Bond-to-bond propensity            | ASBench, ligand removed                        | **99/118 (83.9 %)**; ≥3 measures **69/118 (58.5 %)**                                                                                                                                    | same                             |
| Bond-to-bond propensity            | CASBench, orthosteric **ligand** as source     | **308/314 structures (98.1 %)**, 32/33 proteins                                                                                                                                         | same                             |
| Bond-to-bond propensity            | CASBench, orthosteric **residues** as source   | **304/314 (96.8 %)**, 32/33 proteins                                                                                                                                                    | same                             |
| Ohm 2020                           | TPR / PPV (see §2.5 — names inverted)          | **Ohm 0.57 / 0.72; Amor 0.23 / 0.48** over 20 proteins                                                                                                                                  | `10.1038/s41467-020-17618-2`     |
| STINGAllo 2025                     | DCC success rate                               | **60.2 % overall**, ~78 % on the fpocket subset, vs 21.1–24.2 % for pocket-based predictors; residue F1 0.64, MCC 0.64. Comparators: PASSer Ensemble 47.4 %, AutoML 45.0 %, Rank 55.0 % | `10.1093/bib/bbaf424`            |
| P2Rank 2018                        | Top-n / Top-(n+2)                              | **72.0 % / 78.3 %** (COACH420); **68.6 % / 74.0 %** (HOLO4K)                                                                                                                            | `10.1186/s13321-018-0285-8`      |

All `[VERIFIED-FULLTEXT]` except PASSer 2021's numbers, which A verified at full text and the
earlier file had only `[VERIFIED-ABSTRACT]`.

**The chance rate for these numbers is almost never stated.** PASSer states there are
typically "more than ten pockets while there is only one positive" per protein
`[VERIFIED-FULLTEXT]`, so top-1 chance ≈ 10 % and top-3 chance ≈ 30 %; state of the art
(65 % top-1) is then ≈6.5× chance and top-3 (85 %) ≈2.8× chance. **That ratio is D's
arithmetic from PASSer's own statement, not a published number** `[UNVERIFIED]`.

### 5.2 The independent band, and the gap

AlloBench 2025, `10.1021/acsomega.5c01263`, ran ten tools on a 100-protein test set
**explicitly filtered against the tools' own training sets** — "The test set employed here was
created such that proteins in or related to those in the training sets of allosteric site
prediction tools were excluded" — and scored residue-set Jaccard on the **top prediction
only**. All `[VERIFIED-FULLTEXT]`.

| Tool              | Median JI | Mean JI | Accuracy at JI > 0.5 |
| ----------------- | --------: | ------: | -------------------: |
| PASSer (Ensemble) | **0.060** |   0.197 |             **18 %** |
| PASSer (AutoML)   |     0.046 |       — |             **13 %** |
| APOP              |     0.040 |       — |             **15 %** |
| ALLO              |     0.025 |       — |                    — |
| Allosite          |     0.011 |       — |                    — |
| AlloPred          |     **0** |   0.130 |                    — |
| PASSer (Rank)     |     **0** |   0.117 |                    — |
| AllositePro       |     **0** |   0.084 |                    — |
| STRESS            |     **0** |   0.062 |                    — |
| Ohm               |     **0** |   0.014 |                    — |

Verbatim: _"Suppose we consider correct predictions to be those with a JI > 0.5. The top three
programs are PASSer (Ensemble), APOP, and PASSer (AutoML), with an accuracy of 18, 15, and
13 %, respectively."_ And: _"Surprisingly, most predictions from the programs had no overlap
with the known allosteric site, as evidenced by the high frequency of JI = 0."_ And:
_"none of these programs could achieve an accuracy of more than 60%, even with a very low JI
cutoff of approximately zero."_

Why top-1 only, in their words: _"Only the topmost prediction from each program was considered
to keep the comparison uniform, as Allosite, AllositePro, and STRESS returned less than three
predictions for some proteins."_

**This is the single most important calibration number in the merged review** (convergent:
A, D, E — all three independently identified it as such). Six of ten published tools have a
**median Jaccard of exactly zero** against an independently curated label set. The field's
self-reported top-3 rates of 83–90 % and the independent JI-based accuracies of 13–18 % are
not measuring the same thing, and the gap is about a factor of five. See §8 for the three
drivers of that gap.

### 5.3 The residue-level AUC band

| Method                                                   | Family                     |                                                                                                        ROC AUC |           AUPRC / PR-AUC | Prevalence                            | DOI                                  | Tag                                                  |
| -------------------------------------------------------- | -------------------------- | -------------------------------------------------------------------------------------------------------------: | -----------------------: | ------------------------------------- | ------------------------------------ | ---------------------------------------------------- |
| Allo-Allo                                                | sequence pLM               |                                                                                                       **0.96** |                 **0.77** | ASD-derived                           | `10.1101/2024.09.28.615583`          | `[VERIFIED-FULLTEXT]`                                |
| Allo-Allo ablation (embedding + head)                    | pLM                        |                                                                                                           0.95 |                     0.68 | same                                  | same                                 | `[VERIFIED-FULLTEXT]`                                |
| PocketMiner, experimental cryptic-pocket task            | GNN, apo                   |                                                                                                       **0.87** |                        — | ≈30 % positives in test               | `10.1038/s41467-023-36699-3`         | `[VERIFIED-FULLTEXT]`                                |
| PocketMiner, simulation task, 5-fold                     | GNN                        |                                                                                                    0.83 ± 0.04 |          **0.44 ± 0.12** | ≈10 %                                 | same                                 | `[VERIFIED-FULLTEXT]`                                |
| PocketMiner 3D-CNN comparator                            | CNN                        |                                                                                                    0.79 ± 0.02 |              0.41 ± 0.05 | same                                  | same                                 | `[VERIFIED-FULLTEXT]`                                |
| CryptoSite                                               | apo, MD feature            | **0.83** (full SVM); **0.74** MD-free variant; 0.73 best single feature; 0.74 for 30 crystal features combined |                        — | 84 cryptic sites                      | `10.1016/j.jmb.2016.01.029`          | `[VERIFIED-FULLTEXT]`                                |
| CryptoSite vs PocketMiner head-to-head                   | —                          |                                                                                                   0.85 vs 0.87 |                        — | same test set                         | `10.1038/s41467-023-36699-3`         | `[VERIFIED-FULLTEXT]`                                |
| CryptoBench pLM-NN, CB-full                              | apo                        |                                                                                                       **0.86** |                 **0.36** | <5 % of residues                      | `10.1093/bioinformatics/btae745`     | `[VERIFIED-FULLTEXT]`                                |
| P2Rank on **holo**                                       | trained                    |                                                                                                           0.89 |                     0.34 | —                                     | `10.1093/bioinformatics/btae745`     | `[VERIFIED-FULLTEXT]`                                |
| P2Rank on **apo**                                        | trained                    |                                                                                                       **0.81** |                 **0.21** | —                                     | same                                 | `[VERIFIED-FULLTEXT]`                                |
| PASSerRank                                               | pocket ranking             |                                                                                                           0.82 |                     0.46 | ASD residue-level re-run              | `10.1101/2024.09.28.615583`          | `[VERIFIED-FULLTEXT]`                                |
| PASSer                                                   | pocket ranking             |                                                                                                           0.82 |                     0.30 | same                                  | same                                 | `[VERIFIED-FULLTEXT]`                                |
| PASSer2.0                                                | pocket ranking             |                                                                                                           0.83 |                     0.28 | same                                  | same                                 | `[VERIFIED-FULLTEXT]`                                |
| AllositePro                                              | pocket                     |                                                                                                       **0.68** |                 **0.07** | same                                  | same                                 | `[VERIFIED-FULLTEXT]`                                |
| MEF-AlloSite                                             | pocket                     |                                                                                   0.803 vs 0.798 (Tests 2 & 3) | AP 0.620 / 0.509 / 0.452 | 5.76 % / 3.56 % / 3.16 %              | `10.1186/s13321-024-00882-5`         | `[VERIFIED-FULLTEXT]`                                |
| Allo-PED-pocket                                          | structure + pLM            |                                                                            0.920 (MCC 0.544, precision 47.1 %) |                        — | 185 pos / 4,571 neg                   | `10.1101/2025.03.28.645953`          | `[VERIFIED-FULLTEXT]`                                |
| Allo-PED-site (residue)                                  | same                       |                                                                                **0.563**; best window **0.72** |     best window **0.67** | —                                     | same                                 | `[VERIFIED-FULLTEXT]`                                |
| ZHMolEReP                                                | **supervised, PRS features** |                                                                    **0.7858**, recall 0.7037, 33/40 proteins |                        — | ASBench, 40 proteins                  | `10.1021/acs.jcim.6c00141`           | `[VERIFIED-ABSTRACT]` 2026-09-03; DOI and PMID 42102115 resolve. **ROC or PR is unresolved** — full text paywalled |
| AR-Pred, "Coupling dynamics and evolutionary information…" | **supervised, ANM features** |                                                                              **0.80 median**, ROC, residues |                        — | median over **10 balanced train/validation sets**; the independent test of 15 proteins reports no AUC | `10.1002/prot.25749` (PMID 31141211, PMC6718341) | `[VERIFIED-FULLTEXT]` 2026-09-03 |
| 2026 kinase pLM study                                    | pLM                        |                                                                                                          0.676 |                **0.077** | **3.22 %** (15,185 pos / 456,117 neg) | bioRxiv `10.64898/2026.01.05.697819` | `[UNVERIFIED]`                                       |
| CASP9 top-10 groups, orthosteric ligand-binding residues | community blind assessment |                                                                                                              — |                        — | —                                     | `10.1002/prot.24495`                 | MCC ≈ **0.62** `[VERIFIED-FULLTEXT]`                 |

**WITHDRAWN 2026-09-03. There is no band, because the family does not report the statistic.**
This paragraph said the network/ENM family reports roughly 0.75–0.82 and flagged the evidence
as two `[UNVERIFIED]` points. Both were verified on 2026-09-03 and **neither is an
elastic-network method**: ZHMolEReP is a supervised model with PRS features and AR-Pred is a
random forest with ANM features, whose 0.80 is a median over balanced validation sets rather
than a test score. The rest of the observation holds and is now the whole finding: **PARS,
Ohm, ESSA, bond-to-bond propensity, STRESS and AlloPred report no AUC at all**, confirmed in
full text on each, and the family's own five-method benchmark over 432 structures
(doi:10.1016/j.patter.2021.100408) reports none either. Record:
`../review/data/enm-auc-band-2026-09-03.md`.

**The AUROC/AUPRC divergence is real and in-domain.** Allo-Allo Table 1 above is the cleanest
same-data, same-split comparison in the allosteric literature: read the AUROC column and
AllositePro (0.68) looks weak-but-working while PASSer and PASSerRank (0.82–0.83) look
interchangeable; read the AUPRC column and AllositePro is at or near the chance line while
PASSerRank is 1.5× PASSer2.0. **The two columns give different orderings and very different
magnitudes on the same predictions.** CryptoBench shows the same divergence independently
(0.86 / 0.36), as does the earlier file's §4.1.

Also note Allo-Allo's "Imb. Acc." column: **0.91–0.98 for every method including the one at
AUPRC 0.07** `[VERIFIED-FULLTEXT]`.

**PR-AUC is roughly 3× noisier than ROC-AUC** in the one paper reporting both with
dispersion: ±0.12 vs ±0.04 across 5 splits `10.1038/s41467-023-36699-3`
`[VERIFIED-FULLTEXT]`.

**Published head-to-head margins are small.** 0.02 ROC-AUC (PocketMiner vs CryptoSite); 0.005
ROC AUC (MEF-AlloSite vs its own ablation, declared significant); 1.54 percentage points
(CTQW vs eigenvector centrality). All `[VERIFIED-FULLTEXT]`.

### 5.4 The apo-versus-holo penalty

The number that matters most for any apo-only method.

| Method                                              | Holo                                     | Apo                                          | Drop                                                                                                                                                                   | Source                           | Tag                                                               |
| --------------------------------------------------- | ---------------------------------------- | -------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------- | ----------------------------------------------------------------- |
| ESSA + fpocket                                      | 10/14                                    | **7/14**                                     | **−21 pp**                                                                                                                                                             | `10.1016/j.csbj.2020.06.020`     | `[VERIFIED-FULLTEXT]`                                             |
| AllositePro                                         | 8/14                                     | **2/14**                                     | **−43 pp**                                                                                                                                                             | same                             | `[VERIFIED-FULLTEXT]`                                             |
| PARS                                                | 2/14                                     | 2/14                                         | 0 (already at floor)                                                                                                                                                   | same                             | `[VERIFIED-FULLTEXT]`                                             |
| P2Rank, same proteins                               | AUC 0.89, AUPRC 0.34, TPR 0.84, MCC 0.38 | **AUC 0.81, AUPRC 0.21, TPR 0.62, MCC 0.27** | −0.08 AUC, −0.13 AUPRC                                                                                                                                                 | `10.1093/bioinformatics/btae745` | `[VERIFIED-FULLTEXT]`                                             |
| Bond-to-bond propensity, ligand **removed** not apo | 89.8 % (≥1 measure), 68.6 % (≥3)         | 83.9 %, 58.5 %                               | −5.9 pp, −10.1 pp                                                                                                                                                      | `10.1016/j.patter.2021.100408`   | `[VERIFIED-FULLTEXT]`                                             |
| CAPASP 2026, five tools, dedicated apo subset       | —                                        | —                                            | qualitative only: "these models performed better with the holo state dataset than the apo state dataset, indicating that prediction models require further refinement" | `10.1007/s10822-026-00831-4`     | `[VERIFIED-ABSTRACT]`; **per-tool numbers paywalled and unknown** |

CryptoBench's own summary sentence `[VERIFIED-FULLTEXT]`: "P2Rank performs better on holo
structures than on apo structures, a trend also observed in the aforementioned studies."

**Two caveats that change how these numbers may be used.**

1. **The ligand-removal delta is a lower bound, not the apo penalty.** E states it plainly:
   removing a ligand from a holo structure is not an apo structure — the backbone and side
   chains remain in the bound conformation. So 5.9 and 10.1 percentage points bound the true
   apo penalty from below. **Nobody has published the true apo-vs-holo delta for the same
   method on the same sites.**
2. **A large part of the "apo performance" literature is measured on ligand-stripped holo.**
   APOP evaluates on "holo-structures formed simply by removing any ligand(s)"
   `[VERIFIED-FULLTEXT]`. B calls this a leakage-adjacent shortcut the field takes routinely,
   and it inflates apo performance.

**Honest comparator band for apo-only structure-based prediction in the network/ENM family:
ESSA+fpocket at 7/14 = 50 % top-ranked success** (D). Any holo-derived comparator quoted
against an apo method is inflated by 20–43 percentage points on this evidence.

**A contradiction in the same territory.** fpocket 1.0 apo-vs-holo detection rates: B's direct
fetch returns holo **83 % rank-1 / 92 % top-3**, apo **69 % rank-1 / 94 % top-3**
`[VERIFIED-FULLTEXT]`; a search-result summary of the same abstract returns "94 % and 92 % of
the pockets within the best three ranked pockets from the holo and apo proteins respectively"
`[UNVERIFIED]`. These disagree, and the fetched apo top-3 (94 %) exceeding holo top-3 (92 %)
is implausible. **B's instruction: do not quote either number without re-reading the paper.**

### 5.5 Class prevalence — the chance lines these bands sit on

| Source                | Positive fraction                                                                                                                       | Level   | DOI                                  | Tag                   |
| --------------------- | --------------------------------------------------------------------------------------------------------------------------------------- | ------- | ------------------------------------ | --------------------- |
| CryptoBench 2025      | "binding residues only correspond to less than 5% of all residues"; 16.60 ± 7.22 binding residues per protein over 1,107 apo structures | residue | `10.1093/bioinformatics/btae745`     | `[VERIFIED-FULLTEXT]` |
| DeepAllo 2025         | **5.12 %** residues; **7.76 %** pockets (304 of 4,223)                                                                                  | both    | `10.1093/bioinformatics/btaf294`     | `[VERIFIED-FULLTEXT]` |
| PocketMiner 2023      | "∼10% of all residues were labeled as positives"                                                                                        | residue | `10.1038/s41467-023-36699-3`         | `[VERIFIED-FULLTEXT]` |
| LIGYSIS-bench 2024    | "proportion of observed binding residues = 0.1" as the plotted precision baseline                                                       | residue | `10.1186/s13321-024-00923-z`         | `[VERIFIED-FULLTEXT]` |
| PASSer2.0 2022        | **4.87 %** (251/5,155)                                                                                                                  | pocket  | `10.3389/fmolb.2022.879251`          | `[VERIFIED-FULLTEXT]` |
| PASSer v1 2021        | 119/2,246 = **5.3 %**                                                                                                                   | pocket  | `10.1088/2632-2153/abe6d6`           | `[VERIFIED-FULLTEXT]` |
| STINGAllo precursor   | class imbalance **1:21**                                                                                                                | residue | `10.1016/j.csbj.2024.10.036`         | `[VERIFIED-FULLTEXT]` |
| 2026 kinase pLM study | **3.22 %**                                                                                                                              | residue | bioRxiv `10.64898/2026.01.05.697819` | `[UNVERIFIED]`        |

Only one paper in either review states an AUPRC chance line beside an AUPRC value: Allo-Allo,
"an AUPRC of 0.59 …, substantially better than random (= 0.44)" `[VERIFIED-FULLTEXT]`.

### 5.6 What the downstream value of a correct answer looks like

One target, one group, and it is not the comparison it is often taken for. Kampen, Rodríguez,
Jørgensen et al. 2022, mGlu5, `10.1021/acschembio.2c00234`, all `[VERIFIED-FULLTEXT]`:

| Campaign                                         | Library / N       |                            Actives |                   Hit rate |
| ------------------------------------------------ | ----------------- | ---------------------------------: | -------------------------: |
| Functional HTS (Rodriguez et al.)                | 160,000 compounds |                           345 NAMs |                  **0.2 %** |
| Radioligand fragment screen (Christopher et al.) | 3,600 fragments   | 178 (>30 % displacement at 300 µM) |                    **5 %** |
| Structure-based docking, fragment subset         | 59 tested         |                                  4 | **7 %** (affinity < 10 µM) |
| Structure-based docking, lead-like subset        | 59 tested         |                                  7 |                   **12 %** |
| Structure-based docking, combined                | 118 tested        |                                 11 |                    **9 %** |

**Read honestly.** Both arms target the same allosteric site. The 0.2 % → 9 % jump is a
**structure-guided versus blind** comparison, not allosteric versus orthosteric. It is the
strongest published argument that knowing where the allosteric site is is worth roughly
**45-fold in hit rate** on this target — an existence proof from one target, retrospectively
compared against a literature HTS number, not a population estimate.

Crystallographic fragment screening for context, `[UNVERIFIED]` unless noted: XChem, >150
campaigns, hit rates 1–30 %, typical 5–10 %; PanDDA re-analysis of one campaign raised a hit
rate from 0.9 % to 10.6 %; one recent campaign reported 39 %. Krojer 2020
`[VERIFIED-FULLTEXT]`: "less than 10% of all collected datasets of a screening campaign have
fragments bound", and campaigns "tend to focus on hits found in well-characterised,
orthosteric sites".

**No paper found reports a matched allosteric-versus-orthosteric hit rate across multiple
targets.** unknown.

---

## 6. Difficulty factors and stratification

From E, ranked by strength of evidence. The four-level labelling is E's:
**established** = two or more independent measurements on this task; **single-paper** = one
source, no replication; **folklore** = widely assumed, no measurement found; **unknown** = no
study found at all.

### 6.1 The ranked table

| #   | Factor                                                  | Status                                                                               | Best evidence                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | DOI                                                                                                                     | Tag                                                                                             |
| --- | ------------------------------------------------------- | ------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| 1   | **Crypticity of the site in the apo structure**         | **ESTABLISHED** — direction unambiguous, magnitude poorly pinned                     | CAPASP 2026, five tools better on holo than apo; Wu 2021 ligand-removal 89.8→83.9 % and 68.6→58.5 %; CryptoSite names the failure mode: predictors "failed to predict most cryptic sites that undergo large conformational changes … and partial sites that require binding to another protein chain"                                                                                                                                                                                                                                                                               | `10.1007/s10822-026-00831-4`; `10.1016/j.patter.2021.100408`; `10.1016/j.jmb.2016.01.029`                               | `[VERIFIED-ABSTRACT]` / `[VERIFIED-FULLTEXT]`                                                   |
| 2   | **Burial / solvent exposure of the site**               | **ESTABLISHED — strongest quantitative effect in the whole review**                  | Utgés et al. 2024, 37 fragment-screening experiments, 1,309 structures, 1,601 ligands, **293 unique sites**, K-means on RSA profiles: "A site in C1 is ≈28-fold more likely to be functional than one in C4." C1 n = 46, ≈0.68 of residues at RSA < 25 %, missense-depleted (MES −0.17); C4 n = 29, ≈0.10, missense-enriched (MES +0.06), **0/29 known functional sites**                                                                                                                                                                                                           | `10.1038/s42003-024-05970-8`                                                                                            | `[VERIFIED-FULLTEXT]`                                                                           |
| 3   | **Proximity to the active site**                        | **ESTABLISHED, but with the sign inverted from the naive expectation**               | CASBench: "In 30% of cases, the catalytic and allosteric sites either overlap or share a common border; in 70% of entries, both sites reside at a considerable distance". Wu 2021 explains a **miss** by a site "being in close proximity to the orthosteric site where direct interactions, instead of long-range coupling, occur between the two sites", and states that direct interaction "is out of scope" of the method                                                                                                                                                       | `10.32607/20758251-2019-11-1-74-80`; `10.1016/j.patter.2021.100408`                                                     | `[VERIFIED-FULLTEXT]`                                                                           |
| 4   | **Interface / oligomeric site**                         | **ESTABLISHED as a population fact; single source**                                  | CASBench, n = 91 enzymes: "In 5% of entries, both sites are formed within the intersubunit contact; in 22% of cases, only one site is located between the subunits and 73% of entries correspond to both sites being formed within the subunits" — so **27 % have at least one site at an intersubunit contact**. Also "In 70% of cases, the annotations describe monomeric proteins". CryptoSite independently names "partial sites that require binding to another protein chain" as a failure class                                                                              | `10.32607/20758251-2019-11-1-74-80`; `10.1016/j.jmb.2016.01.029`                                                        | `[VERIFIED-FULLTEXT]`                                                                           |
| 5   | **Conservation of site residues**                       | **ESTABLISHED against orthosteric sites; CONTESTED as an absolute property**         | Panjkovich & Daura: "allosteric sites tend to be under lower sequence-conservation pressure than active sites"; measured trade-off, flexibility alone matched 27 % of 117 candidate pockets, adding a ≥50 % structural-conservation filter raised **PPV to 0.42** on 36 pockets, strictest set **PPV 0.65 at sensitivity 0.22**. Wu 2021 and Eccleston & Furnham agree in direction. **Contradicted in detail** by Utgés 2024's C1 being most conserved and most missense-depleted                                                                                                  | `10.1186/1471-2105-13-273`; `10.1101/2025.06.27.662060`; `10.1038/s42003-024-05970-8`                                   | `[VERIFIED-FULLTEXT]`                                                                           |
| 6   | **Modulator type (activator vs inhibitor)**             | **ESTABLISHED that a topology-only method should not be expected to differ by sign** | Motlagh, Wrabl, Li & Hilser: "the actual sign of the coupling can change, transforming an activator into a repressor, or vice versa"; "the signs of the interaction energies are the key parameters". Empirically, an NMDAR PAM/NAM series shares one site and is interconverted by methyl groups; at mGlu5 PAMs and NAMs bind the same pocket                                                                                                                                                                                                                                             | `10.1038/nature13001`; `10.7554/eLife.34711`                                                                            | `[VERIFIED-FULLTEXT]` / `[UNVERIFIED]` for the two empirical cases                              |
| 7   | **Conformational-change magnitude (apo→holo RMSD)**     | **CONFOUNDED; duplicates #1**                                                        | CryptoBench uses pocket-atom RMSD > 2 Å as its _definition_ of crypticity, so stratifying on both is stratifying on the same thing twice. Theoretical objection, Motlagh 2014: "allostery can indeed be manifested essentially without structural change"; Tsai & Nussinov: "an allosteric event such as ligand binding does not create a new conformational state; it only shifts the population among existing states." Measurement objection, Wankowicz Rule 8: match "resolutions within 0.3 Å, identical space groups, and unit cell dimensions differing by no more than 10%" | `10.1093/bioinformatics/btae745`; `10.1038/nature13001`; `10.1371/journal.pcbi.1003394`; `10.1371/journal.pcbi.1013094` | `[UNVERIFIED]` for the CryptoBench criterion as quoted by E; `[VERIFIED-FULLTEXT]` for the rest |
| 8   | **Protein size / residue count**                        | **FOLKLORE as a direct difficulty axis; ESTABLISHED as a normalisation requirement** | APOP: "The number of pockets in this set ranges from 10 to 242"; fructose-1,6-bisphosphatase gives 84 pockets in `3IFA` and 69 in `1KZ8`. The ranking denominator grows with the protein and the numerator does not. APOP does **not** quantify a difficulty–size correlation, and **no paper found reports accuracy stratified by residue count**                                                                                                                                                                                                                                  | `10.1093/bioinformatics/btad275`                                                                                        | `[VERIFIED-FULLTEXT]`                                                                           |
| 9   | **Lipid-facing site**                                   | **SINGLE WEAK SOURCE**                                                               | FTMap and FTSite reported to fail at hydrophobic sites at the protein–membrane interface (glucagon receptor as the example); a transmembrane ligand must first partition into the membrane                                                                                                                                                                                                                                                                                                                                                                                          | —                                                                                                                       | `[UNVERIFIED]`                                                                                  |
| 10  | **Secondary-structure context (helix / strand / loop)** | **UNKNOWN**                                                                          | No study found reporting accuracy or prevalence stratified by secondary structure. Two qualitative statements point at loops without quantifying: Vajda 2018, "allosteric modulators frequently bind at flexible regions without pre-formed pockets"; Eccleston & Furnham, allosteric sites "exhibit more ambiguous, non-pocket-like geometries"                                                                                                                                                                                                                                    | `10.1016/j.cbpa.2018.05.003`; `10.1101/2025.06.27.662060`                                                               | `[VERIFIED-FULLTEXT]` for the two quotes                                                        |
| 11  | **Mechanical / lever-arm / motor sites**                | **UNKNOWN**                                                                          | No published statistics found                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | —                                                                                                                       | unknown                                                                                         |

### 6.2 Crypticity has three incompatible definitions

This matters because §6.1 row 1 is the strongest factor and the definition is not settled.

1. **Pocket score, apo vs holo.** CryptoSite `[VERIFIED-FULLTEXT]`: "Binding sites with bad
   pocket scores in the unbound conformation and good pocket scores in the bound conformation
   were defined as cryptic sites, whereas those with good pocket scores in both conformations
   were defined as binding pockets." Vajda 2018 renders the numeric form: "an average pocket
   score of less than 0.1 in the unbound form of the protein and greater than 0.4 in the
   bound form" `[VERIFIED-FULLTEXT]`.
2. **Pocket-atom RMSD ≥ 2 Å.** CryptoBench: "The pocket is marked as cryptic if there exists
   a conformation where the RMSD of the pocket atoms between ligand-bound state (holo) and
   the ligand-free state (apo) exceeds 2 Å" `[UNVERIFIED]` in E's retrieval;
   `[VERIFIED-FULLTEXT]` in B's, which renders it as "a difference of at least 2 Å RMSD
   between the binding residues in the apo and holo forms".
3. **Transplant clash count.** No published precedent found; a repo construction, and E
   requires it be labelled as one.

**(1) and (2) measure different things.** (1) is about pocket _detectability_; (2) is about
pocket-atom _motion_. A site can move 2 Å and remain detectable in the apo, and a sub-2 Å
side-chain rotation can occlude a pocket entirely. Which convention was used must be stated
at first use.

The definitional base is Vajda, Beglov, Wakefield, Egbert & Whitty 2018,
`10.1016/j.cbpa.2018.05.003` `[VERIFIED-FULLTEXT]`: "A cryptic site can therefore be defined
as a site that forms a pocket in a ligand-bound structure, but not in the unbound protein
structure."

### 6.3 Cryptic against allosteric — two numbers that do not agree

| Statement                                                                        | Value                                                                                                                                                                          | Source                                   | Tag                   |
| -------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------- | --------------------- |
| Of 19 validated cryptic sites with ligands below 300 nM, how many are allosteric | "Eight of the sites shown in Table 1 are allosteric" → **8/19 = 42 %**                                                                                                         | Vajda 2018, `10.1016/j.cbpa.2018.05.003` | `[VERIFIED-FULLTEXT]` |
| Of 58 cryptic sites, how many are effector-binding sites                         | "24 of the 58 cryptic sites are found in proteins that are known to be allosterically regulated, with **17 of the 24** annotated as effector binding sites" → **17/58 = 29 %** | CryptoSite, `10.1016/j.jmb.2016.01.029`  | `[VERIFIED-FULLTEXT]` |

**The denominators differ** — Vajda restricts to validated high-affinity sites — so the two
are not strictly contradictory. Neither supports "most cryptic sites are allosteric", and
neither answers the converse. **The converse fraction, what proportion of _allosteric_ sites
are cryptic, is not reported anywhere.** E checked again against CryptoBench, CryptoBank and
Gašparíková 2025 and did not close it.

The sentence that limits inference in the other direction, Vajda 2018 `[VERIFIED-FULLTEXT]`:
"Since molecular mechanisms of allosteric communication are rooted in the dynamic nature of
proteins, allosteric modulators frequently bind at flexible regions without pre-formed
pockets."

### 6.4 Why "distal is harder" is folklore for a propagation method

E's finding, and it inverts the naive expectation. **No published curve of accuracy versus
distance from the active site exists** — a genuine gap. What exists instead:

- 30 % of curated allosteric enzymes have sites that overlap or border the catalytic site
  (CASBench). A distance filter on a label set therefore discards about a third of curated
  allosteric sites.
- **Proximity is a documented _failure_ mode for propagation methods, not an advantage**
  (Wu 2021, above): near the orthosteric site, direct interaction rather than long-range
  coupling occurs, and the method declares it out of scope.
- The AlloBench JI-vs-inverse-distance correlation is a **metric artefact, not a difficulty
  finding**: it says JI tracks the distance between _predicted_ and _known_ site, and says
  nothing about accuracy as a function of the site's distance from the _active_ site
  (`10.1021/acsomega.5c01263`, `[VERIFIED-FULLTEXT]`). Do not cite it for the latter.

So the documented mechanism is that _proximal_ sites are contaminated by direct interaction
and are trivially recoverable by a distance proxy. That is a different problem, not an easier
version of the same one.

### 6.5 Which factors can carry a stratified comparison at small N

E's own constraint, stated as arithmetic rather than as a citation: the minimum attainable
one-sided p of a sign-type test is 2⁻ᴺ — 0.031 at N = 5, 0.0625 at N = 4, 0.125 at N = 3,
0.25 at N = 2 `[UNVERIFIED — arithmetic]`. Every two-way stratification of a 14-arm panel
produces cells at or below N = 5.

E's classification of what a factor can be used for:

| Factor                       | Measure?                                               | Can it be a stratum?                                                                                                      |
| ---------------------------- | ------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------- |
| Crypticity                   | yes                                                    | **yes** — the only factor with a measured effect on this exact task, a published definition, and a pre-method measurement |
| Proximity to the source      | yes                                                    | **yes, but only with the distance-only baseline printed beside it**                                                       |
| Burial / RSA of label set    | yes                                                    | no — property of the ground truth, not the input; too few arms                                                            |
| Conservation                 | yes, as covariate                                      | no — not on an apo-only prediction path; literature contradicts itself on sign                                            |
| Protein size N               | yes                                                    | **covariate, not stratum** — collinear with prevalence                                                                    |
| Apo–holo pocket RMSD         | yes, as disclosure                                     | no — duplicates crypticity; confounded by Δresolution                                                                     |
| Oligomeric state / interface | record as zero-variance where excluded by construction | no                                                                                                                        |
| Modulator type               | record as constant                                     | no — theoretically unmotivated and constant                                                                               |
| Secondary structure          | optional                                               | no — **no published evidence exists**                                                                                     |
| Lipid-facing                 | no                                                     | no                                                                                                                        |

---

## 7. Reporting standards and published criticisms

From A and E.

### 7.1 Is there a TRIPOD or CONSORT analogue for structure-based site prediction?

**No.** E searched for it specifically (four queries) and found three partial standards and no
unified one.

**1. Wankowicz, "Ten rules for a structural bioinformatic analysis", _PLoS Comput Biol_
2025;21(10):e1013094, `10.1371/journal.pcbi.1013094`** `[VERIFIED-FULLTEXT]`. The closest
thing to a checklist: recent, community-facing, and directly about analyses built on PDB
entries.

| Rule | Title                                                               | Recommendation as retrieved                                                                                                               |
| ---- | ------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| 1    | Define your biological selection criteria                           | state the inclusion frame; de-redundify by clustering or alignment                                                                        |
| 2    | Determine how you will quality control your data                    | method, resolution, R-values, Ramachandran, stereochemistry                                                                               |
| 3    | Re-processing structural model data                                 | "Where possible, it is recommended to use X-ray structural models from PDB-REDO"                                                          |
| 4    | The PDB and structural models are weird and biased                  | PDB over-represents small globular proteins; distinguish ASU from biological assembly; "approximately 20% of assemblies may be incorrect" |
| 5    | Consider sample size, statistics, overfitting and uncertainty       | paired tests for paired comparisons; resampling; cross-validation                                                                         |
| 6    | Determine and apply the correct controls                            | "**Controls must directly address the null hypothesis you wish to reject.**"                                                              |
| 7    | Understand how metrics are compared across your structures          | normalise RMSD by length; normalise B-factors within structures                                                                           |
| 8    | Appropriately connect and compare structures                        | "**Match crystallographic parameters**" — resolutions within **0.3 Å**, identical space groups, unit cells within 10 %                    |
| 9    | Connect your analysis to other databases or prospective experiments | UniProt, Pfam, SCOP via SIFTS                                                                                                             |
| 10   | Visualize everything!                                               | PyMOL/Chimera as quality control before reporting                                                                                         |

**2. DOME** — Walsh, Fishman, Garcia-Gasulla et al., _Nat Methods_ 2021;18:1122–1127,
`10.1038/s41592-021-01205-4` `[UNVERIFIED]`. Four-axis reporting standard (Data,
Optimization, Model, Evaluation) explicitly scoped to **supervised** ML, so only partly
applicable to an unsupervised propagation method; the Data and Evaluation axes transfer.

**3. CASP function-prediction (FN) assessment** `[VERIFIED-FULLTEXT]` for the CASP10 paper.
Ligand-binding-residue prediction is assessed at residue level using MCC and BDT
(`10.1002/prot.24495`; BDT primary `10.1093/bioinformatics/btq543`). CASP9's ten top groups
averaged **MCC 0.62**; CASP10 had 17 groups on 13 targets. The field's only community-run
blind assessment of binding-site prediction — but it targets orthosteric ligand-binding
residues, not allosteric ones.

### 7.2 Field-specific conventions a reviewer will expect

From E §4.2, cross-checked against A §4:

- **A success criterion stated in advance.** Top-1 / top-3 pocket rank is the dominant
  convention.
- **Jaccard against the label set at several cutoffs**, per AlloBench.
- **A stated label radius.** 4 Å (AlloBench, ASBench-lineage), 4.5 Å (CryptoBench), 5 Å
  (CASBench, CryptoSite, PocketMiner), 6 Å (ASD v2). "A number computed at one radius is not
  comparable to a number computed at another; say which you used, at first use."
- **A matched null**, if any significance is claimed. The field's only well-specified one is
  the Barahona/Yaliraki surrogate-site construction.
- **A comparison on a common test set, not self-reported numbers.**
- **Redundancy control between any training or tuning data and the test set, with the
  threshold stated.** UniRef50 cluster removal (AlloBench); MMseqs2 at 30 % identity
  (DeepAllo, Eccleston & Furnham); 40 % clustering (CryptoBench `[UNVERIFIED]`); 10 %
  sequence identity for the second clustering round (CryptoBench, `[VERIFIED-FULLTEXT]` in
  the earlier file).
- **Author numbering and chain ID on every reported residue.**

### 7.3 The nine documented criticisms an evaluation like this attracts

Each quoted from a source that makes it, so a rebuttal can be written against the actual
wording.

| #      | Criticism                                                                   | The wording                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | DOI                                                                                                                      | Tag                                               |
| ------ | --------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------- |
| **T1** | **Evaluating on holo, or on ligand-stripped holo, instead of apo**          | CAPASP: five tools "performed better with the holo state dataset than the apo state dataset". Wu 2021: "the presence of the allosteric ligand strengthens the coupling to the orthosteric site and makes the result biased towards successful detection." APOP evaluates on "holo-structures formed simply by removing any ligand(s)"                                                                                                                                                                                                                                                                                                       | `10.1007/s10822-026-00831-4`; `10.1016/j.patter.2021.100408`; `10.1093/bioinformatics/btad275`; `10.1093/bioadv/vbaf156` | `[VERIFIED-ABSTRACT]` / `[VERIFIED-FULLTEXT]`     |
| **T2** | **Homology leakage between training/tuning data and the test set**          | AlloBench: "The UniRef50 cluster IDs … were obtained for the 268 unique UniProt IDs of these proteins. AlloBench proteins with these UniRef50 cluster IDs were dropped to remove any related proteins in addition to the proteins of the training sets." The consequence when it is done: "none of these programs could achieve an accuracy of more than 60%, even with a very low JI cutoff of approximately zero", best tool 18 % at JI > 0.5 — against self-reported figures such as Allosite's ">95 %"                                                                                                                                  | `10.1021/acsomega.5c01263`                                                                                               | `[VERIFIED-FULLTEXT]`                             |
| **T3** | **Self-evaluation**                                                         | AlloBench: "a systematic study quantitatively comparing the performance of the available allosteric site prediction tools on a common test set has yet to be performed"                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | `10.1021/acsomega.5c01263`                                                                                               | `[VERIFIED-FULLTEXT]`                             |
| **T4** | **Ground truth that is wrong**                                              | Zlobin 2019: "The ASD database is an important resource on allosteric proteins but contains redundant (duplicated) data and low-quality annotations; so, only a small part of this collection can be used in practice." Wu 2021 found it concretely: "the orthosteric residues of three structures … reported in the ASD database are incorrect (that is they do not form a binding site) and those of one further structure do not match with the data in ASBench." ASD2023 mixes 3,102 curated sites with **66,589 machine-predicted** ones; AlloBench adds that in ASD 2023 "only 46% of entries have annotations for orthosteric sites" | `10.32607/20758251-2019-11-1-74-80`; `10.1016/j.patter.2021.100408`; `10.1093/nar/gkad915`; `10.1021/acsomega.5c01263`   | `[VERIFIED-FULLTEXT]`, ASD2023 mix `[UNVERIFIED]` |
| **T5** | **No negative control and no null**                                         | Wankowicz Rule 6: "Controls must directly address the null hypothesis you wish to reject." §3.5 above quantifies the field's compliance: 13 of 18 papers state no test at all                                                                                                                                                                                                                                                                                                                                                                                                                                                               | `10.1371/journal.pcbi.1013094`                                                                                           | `[VERIFIED-FULLTEXT]`                             |
| **T6** | **Retrospective, cherry-picked evaluation with no prospective test**        | Chen & Zhang 2025: "It is important to acknowledge that this retrospective docking study is biased by past results." Gašparíková 2025 on the cryptic-site ML field: "to date, there is limited evidence of any truly novel ligands being discovered as a result of cryptic binding site detection using one of the ML-methods summarized above."                                                                                                                                                                                                                                                                                            | `10.1021/acs.jcim.5c00331`; `10.1093/bioadv/vbaf156`                                                                     | `[VERIFIED-FULLTEXT]`                             |
| **T7** | **Training-distribution bias that looks like a method result**              | Chen & Zhang: "There are fewer allosterically bound kinase structures and binding data points compared with their orthosteric counterparts", so "diffusion-based generative models trained on this data would be more likely to sample the high-density regions and dock ligands to the orthosteric site." Measured: on CDK2 Type III (allosteric) poses, DiffDock alone succeeded **~0 %** against ~75 % on orthosteric                                                                                                                                                                                                                    | `10.1021/acs.jcim.5c00331`                                                                                               | `[VERIFIED-FULLTEXT]`                             |
| **T8** | **Definitional drift between "cryptic" and "allosteric"**                   | §6.2, §6.3 above                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | —                                                                                                                        | —                                                 |
| **T9** | **Uncontrolled crystallographic parameters behind any apo–holo difference** | Wankowicz Rule 8, resolutions within 0.3 Å, identical space groups, unit cells within 10 %                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | `10.1371/journal.pcbi.1013094`                                                                                           | `[VERIFIED-FULLTEXT]`                             |

**Plus, from the fragment-screening side, applying to any "we found a new site" claim.**
Krojer, Fraser & von Delft 2020, `10.1016/j.sbi.2020.08.004` `[VERIFIED-FULLTEXT]`:

> "even though the function of almost every protein can be influenced by allostery, it remains
> a challenge to discover, rationalise and validate putative allosteric binding pockets"
> "The self-evident power of structure-based mapping of protein surfaces is tempered by the
> remaining challenge of assessment biochemical or biological relevance of these pockets."
> "to consider a site truly allosteric requires orthogonal experiments to establish whether
> modulating them has measureable biochemical effects."
> "In this case, the difficulty remains establishing whether these are merely baseline
> structural fluctuations, or instead the result of true allosteric signalling."
> "Developing high-affinity small molecule ligands is even more difficult for these pockets
> than for orthosteric sites."
> "Disulphide tethering and mutational studies are established methods for functional
> validation of putative allosteric pockets"

Utgés 2024 quantifies the prior against an unprioritised surface pocket: **0 of 29** sites in
the most solvent-exposed cluster had a known function `[VERIFIED-FULLTEXT]`.

### 7.4 The two standing methodological objections to a residue-level, threshold-free protocol

**Objection 1 — residue-level metrics are the wrong unit.** Utgés & Barton 2024,
`10.1186/s13321-024-00923-z`, 13 methods + 15 variants, 2,775 protein chains, >10 metrics
`[VERIFIED-FULLTEXT]`:

> "the usefulness of residue-level metrics as F1 score or MCC is limited"
> because "methods that precisely and correctly predict the clearest sites … perform better on
> these metrics, whilst methods that predict more pockets … will obtain worse results.
> Pocket-level metrics, particularly recall, are more representative."

and their positive recommendation:

> "Recall (% of sites that are correctly predicted) is more informative than precision (% of
> predictions that are correct), particularly, recall considering top-N+2 ranked predictions"
> "we propose top-N+2 recall as the universal benchmark metric for ligand binding site
> prediction and urge authors to share not only the source code of their methods, but also of
> their benchmark."

P2Rank makes the same objection from the other direction `[VERIFIED-FULLTEXT]`: "We believe
that pocket-centric point of view better represents a common sense associated with LBS
prediction, and as an evaluation methodology awards those methods that fail to predict the
least amount of potentially interesting binding sites."

**Objection 2 — AUPRC is not generally better under imbalance.** McDermott MB, Zhang H,
Hansen L, Angelotti G, Gallifant J (2024), "A Closer Look at AUROC and AUPRC under Class
Imbalance", NeurIPS 2024, **arXiv:2401.06091** `[VERIFIED-FULLTEXT]` for the wording. They

> "theoretically characterize the behavior of AUROC and AUPRC in the presence of model
> mistakes, establishing that AUPRC is not generally superior in cases of class imbalance"

argue AUPRC

> "can be a harmful metric as it can unduly favor model improvements in subpopulations with
> more frequent positive labels"

and report a survey of over 1.5 million papers finding the "AUPRC is better under imbalance"
claim

> "is often made without citation, misattributed to papers that do not argue this point, and
> aggressively over-generalized from source arguments."

The pro-AUPRC position it argues against is Saito & Rehmsmeier 2015,
`10.1371/journal.pone.0118432` `[VERIFIED-FULLTEXT]`, framed for life-science data: "The
rapid expansion in high-throughput biological experiments produces a number of large-sized
datasets, and the majority of such datasets can be expected to be imbalanced", with the
retrieval argument "it is practical to check the performance of the early retrievals, which
only examines a limited number of top-scoring instances", and the reported observation that
66.7 % of the binary-SVM studies on imbalanced data they surveyed used ROC. Their concrete
paired numbers: MiRFinder ROC AUC 0.772 / PRC AUC 0.106; RNAmicro ROC AUC 0.886 (best ROC in
the comparison) / PRC AUC 0.054 — "the ROC plot makes an innocent impression, the PRC plot
reveals the bitter truth".

**And the frequently over-cited third party.** Davis J & Goadrich M (2006), "The Relationship
between Precision-Recall and ROC Curves", ICML '06 pp. 233–240, `10.1145/1143844.1143874`.
It establishes the one-to-one point correspondence between ROC and PR space and the
non-linear-interpolation result. **It is about interpolation and dominance, not about which
metric to prefer.** `evaluation-protocol-lit.md` already records correcting a mis-citation of
exactly this kind.

**A stronger anti-AUROC position also exists.** Chicco & Jurman, `10.1186/s13040-023-00322-4`
`[VERIFIED-ABSTRACT]`: ROC AUC "is generated including predictions that obtained insufficient
sensitivity and specificity" and "does not say anything about positive predictive value …
potentially generating inflated overoptimistic results"; see also
`10.1186/s13040-021-00244-z`.

### 7.5 What the field itself says a residue ranking does not deliver

Kozakov, Hall, Napoleon, Yueh, Whitty & Vajda 2015, `10.1021/acs.jmedchem.5b00586`
`[VERIFIED-FULLTEXT]`, define druggability as "the likelihood of being able to identify a
druglike small ligand that can modulate the activity of the target" and give the operational
geometric bar:

| Criterion                                              | Threshold                                            |
| ------------------------------------------------------ | ---------------------------------------------------- |
| Strength `S` of the primary hot spot                   | **≥ 16 FTMap probe clusters**                        |
| Connectivity `CD` (centre-to-centre between hot spots) | **< 8 Å**                                            |
| Size `MD` (maximum dimension)                          | **≥ 10 Å**                                           |
| Borderline druggable                                   | 13 ≤ S < 16, predicted "at most micromolar affinity" |

Vajda 2018 applies the same bar to cryptic and allosteric sites and adds the cost-side facts
`[VERIFIED-FULLTEXT]`: "Druggable cryptic sites almost invariably have a strong binding energy
hot spot close by"; "the number of such strong hot spots on any given protein never exceeded
four"; "It is likely therefore that very few of the dozens of transient pockets seen in some
Markov state simulations provide viable drug targets."

**The published druggability scores are biased against allosteric pockets by construction**,
and nobody has measured by how much. Every one of SiteMap Dscore (`10.1021/ci800324m`),
fpocket druggability (`10.1021/jm100574m`) and DoGSiteScorer
(`10.1093/bioinformatics/bts310`) is a size- and enclosure-weighted function, while two
independent statements say allosteric pockets are systematically smaller and less pocket-like
than orthosteric ones. **All three primaries are paywalled and their numeric thresholds are
`[UNVERIFIED]`; see §8 for the Dscore threshold contradiction.**

### 7.6 What the field optimises, on the evidence of its own metric choices

E's argument, from evidence rather than opinion:

1. **Every allosteric-site benchmark scores precision at small k, and none scores recall.**
   APOP counts a top-3 hit; PASSer2.0 reports top-1/2/3; AlloBench scores only the topmost
   prediction. "A field that cared about recall would report a curve, not a top-k count."
2. **The virtual-screening literature made the early-recognition argument twenty years ago**
   (Truchon & Bayly, `10.1021/ci600426e`, `[UNVERIFIED]` — primary unreachable).
3. **The cost of a false positive is one experimental campaign**, and the campaign is the
   expensive step (Krojer 2020).
4. **The base rate for an unprioritised surface pocket is near zero** (Utgés 2024, 0/29).
5. **Attrition data put target validation first** — the AstraZeneca 5R framework,
   `10.1038/nrd4309`, with target validation "the most essential priority and the one
   currently responsible for the most project attrition" `[UNVERIFIED]`.

---

## 8. Contradictions between sources

Every place two sources disagree. Neither side is resolved by preference. Each entry states
both positions and what would settle it.

### C1 — Is AUPRC the right metric under class imbalance?

| Position                                  | Claim                                                                                                                                                                                                                                                                                                     | Sources                                                                       |
| ----------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| **Pro**                                   | "The Precision-Recall Plot Is More Informative than the ROC Plot When Evaluating Binary Classifiers on Imbalanced Datasets"; concrete paired numbers ROC 0.772 / PRC 0.106 and ROC 0.886 / PRC 0.054                                                                                                      | Saito & Rehmsmeier 2015, `10.1371/journal.pone.0118432` `[VERIFIED-FULLTEXT]` |
| **Anti**                                  | "AUPRC is not generally superior in cases of class imbalance"; it "can unduly favor model improvements in subpopulations with more frequent positive labels"; and the pro-claim "is often made without citation, misattributed to papers that do not argue this point, and aggressively over-generalized" | McDermott et al. 2024, arXiv:2401.06091 `[VERIFIED-FULLTEXT]`                 |
| **Neither**                               | Davis & Goadrich 2006 establishes point correspondence and non-linear interpolation, **not** metric preference — and is the paper McDermott names as the most-misattributed                                                                                                                               | `10.1145/1143844.1143874`                                                     |
| **In-domain evidence for the divergence** | Allo-Allo Table 1: AUROC and AUPRC give different orderings on the same predictions. CryptoBench 0.86/0.36. P2Rank apo 0.81/0.21                                                                                                                                                                          | §5.3                                                                          |

**What would settle it:** nothing in the literature; the two arguments are about different
things. Saito & Rehmsmeier argue AUPRC is more _informative_ about early retrieval; McDermott
argues it is not _uniformly better_ and is _comparison-distorting across subpopulations of
different prevalence_. Both can be true. The empirically decidable part is whether raw AUPRC
reorders arms of differing prevalence in a given dataset, which is a measurement, not a
citation.

### C2 — DCC at 4 Å or at 10–12 Å, and is "DCC" even the same quantity?

| Position                              | Claim                                                                                                                                               | Sources                                                                                                                                                             |
| ------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **4 Å is the established DCC cutoff** | "Predictions with DCC values of less than 4.0 Å were considered to be successful"; "4 Å is the established cutoff value" for DCC                    | JCIM 2025 membrane benchmark, `10.1021/acs.jcim.5c00336`; Kalasanty `10.1038/s41598-020-61860-z`; PUResNet `10.1186/s13321-021-00547-7` — all `[VERIFIED-FULLTEXT]` |
| **4 Å is too conservative for DCC**   | "a DCC threshold of 4 Å is too conservative, and a more flexible DCC threshold of 10–12 Å should be used for comparable performance with DCA = 4 Å" | Utgés & Barton 2024, `10.1186/s13321-024-00923-z` `[VERIFIED-FULLTEXT]`                                                                                             |
| **The acronym itself is contested**   | P2Rank: "DCC (distance between the center of the pocket and any ligand atom)". Everywhere else DCC = centre-to-centre and centre-to-atom = DCA      | `10.1186/s13321-018-0285-8` vs `10.1093/bioinformatics/btx350` — both `[VERIFIED-FULLTEXT]`                                                                         |

**What would settle it:** nothing about a threshold; it is a naming failure, not a
disagreement about geometry. Any use must define the quantity rather than cite the acronym.
Utgés & Barton's 10–12 Å figure is an empirical equivalence to DCA = 4 Å measured on 2,775
chains, so it settles the _equivalence_ question and not the _right threshold_ question.

### C3 — The ligand-contact cutoff that defines the label set

Seven values in current use: 2.5 Å (COACH), 3.5 Å (Amor 2016), 4.0 Å (AlloBench,
ASBench-lineage), 4.5 Å (CryptoBench, Tee 2018), 5.0 Å (CryptoSite, CASBench), 6 Å (ASD v2
`[UNVERIFIED]`), ΣVdW + 0.5 Å (CASP10). Full table at §2.4.

**What would settle it:** nothing — there is no fact of the matter, only a convention. The
field's own diagnosis (Patterns 2021/2022) is that this choice, not metric choice, dominates
evaluation variance. The empirically decidable part is a sensitivity sweep.

### C4 — The ASBench cutoff: 4 Å or 6 Å in the same paper's two versions

B's fetch of the **published PMC version** of the Patterns benchmarking paper returns
"residues within 4 Å from the allosteric ligand" for ASBench; B's fetch of the **bioRxiv
preprint of the same paper** returns "within 6 Å" `[VERIFIED-FULLTEXT]` for both retrievals.
AlloBench independently uses 4 Å.

**B's own reading:** treat 4 Å as the ASBench-lineage number; "the 6 Å reading is most likely
an extraction artefact from the preprint and I could not confirm it."
**What would settle it:** re-reading the preprint PDF directly rather than through an
extractor.

### C5 — fpocket's apo-versus-holo detection rates

| Source                                                               | Holo                     | Apo                          |
| -------------------------------------------------------------------- | ------------------------ | ---------------------------- |
| B's direct fetch of `10.1186/1471-2105-10-168` `[VERIFIED-FULLTEXT]` | 83 % rank-1 / 92 % top-3 | 69 % rank-1 / **94 % top-3** |
| Search-result summary of the same abstract `[UNVERIFIED]`            | 94 % top-3               | 92 % top-3                   |

The fetched apo top-3 (94 %) exceeding the fetched holo top-3 (92 %) is implausible.
**B's instruction: do not quote either without re-reading the paper.**
**What would settle it:** reading the fpocket 2009 results table directly.

### C6 — Are allosteric residues network hubs?

| Position              | Claim                                                                                                                                                                                                               | Sources                                                              |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| **Yes, implicitly**   | The centrality-confound argument, and the RIN literature's documented burial→hydrophobicity→degree chain                                                                                                            | `[UNVERIFIED]`                                                       |
| **No**                | ACSS residues show **low degree centrality and low closeness centrality** across all four ASD protein classes; betweenness "nonuniform"; most ACSSs not small-world. Control: the non-ACSS part of the same protein | Malik et al. 2018, `10.48550/arXiv.1802.10207` `[VERIFIED-FULLTEXT]` |
| **No, directionally** | "local measures such as degree are insufficient to capture long-range allosteric coupling" — but **no quantitative comparison run**                                                                                 | Erman 2026, `10.1088/1478-3975/ae3e49` `[VERIFIED-FULLTEXT]`         |

**What would settle it:** the two literatures may be describing different residue classes —
_pathway_ residues (Malik's ACSS) versus _site_ residues. A single study computing degree and
closeness separately for annotated allosteric-**site** residues and for pathway residues, on
the same structures, would settle it. None exists.

### C7 — Do allosteric communication pathways exist?

The entire pathway-prediction literature (rows 1, 7, 12, 14 of §4.1) assumes yes.
**Stock & Hamm 2018**, `10.1098/rstb.2017.0187`, time-resolved IR plus non-equilibrium MD on
a photoswitchable PDZ2, found "the absence of well-defined communication pathways", concluding
that "allosteric communication shares some properties with downhill folding, except that it is
an 'order-order' transition."

**What would settle it:** more experiments of the Stock & Hamm design on more systems. n = 1
system against an entire assumed literature.

### C8 — 85 % top-3 against a median Jaccard of 0.06

The field simultaneously reports 83–90 % top-3 pocket-ranking success (§5.1) and, for the same
tools on an independently curated leakage-filtered set, a **median residue-overlap Jaccard of
0.06 and accuracies of 13–18 % at JI > 0.5** (§5.2). Both `[VERIFIED-FULLTEXT]`.

D names three drivers and notes **nobody has decomposed them**:

1. **Metric.** "Is the right pocket in the top 3 of ~10 pockets" is a far easier question than
   "what fraction of the true residue set did you recover".
2. **Leakage.** AlloBench filtered training-set relatives; the self-reported numbers largely
   did not.
3. **Candidate set.** Pocket-ranking methods get contiguity and cavity-ness for free; residue
   scoring does not.

**What would settle it:** running the same tools on the same proteins under both metrics with
and without the leakage filter — a 2 × 2 decomposition nobody has published.

### C9 — Are allosteric sites conserved?

| Position                                          | Claim                                                                                                                                                                                                                                                                                               | Sources                                                                                                                                                                 |
| ------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Less conserved than orthosteric sites**         | "allosteric sites tend to be under lower sequence-conservation pressure than active sites"; "Low evolutionary pressure for allosteric sites to accommodate an endogenous substrate compared with the well-conserved orthosteric sites"; "Allosteric sites tend to be less evolutionarily conserved" | Panjkovich & Daura 2012 `10.1186/1471-2105-13-273`; Wu 2021 `10.1016/j.patter.2021.100408`; Eccleston & Furnham `10.1101/2025.06.27.662060` — all `[VERIFIED-FULLTEXT]` |
| **Functional pockets are the _most_ conserved**   | Utgés 2024's C1 cluster is the most buried, **most conserved and most missense-depleted** (MES −0.17), and is the cluster enriched in known functional sites                                                                                                                                        | `10.1038/s42003-024-05970-8` `[VERIFIED-FULLTEXT]`                                                                                                                      |
| **Coevolution carries allosteric signal**         | statistical coupling analysis finds coevolving "sectors" physically connecting active sites to distal allosteric sites                                                                                                                                                                              | `[UNVERIFIED]`                                                                                                                                                          |
| **Deep mutational scanning, the other way again** | residues critical for allosteric control are poorly conserved while residues critical for structural stability are highly conserved                                                                                                                                                                 | `[UNVERIFIED]`                                                                                                                                                          |
| **And yet conservation carries signal**           | CryptoSite retains "sequence conservation" as one of three features in its reduced model                                                                                                                                                                                                            | `10.1016/j.jmb.2016.01.029` `[VERIFIED-FULLTEXT]`                                                                                                                       |

**What would settle it:** the reference class. The comparisons are not the same comparison —
allosteric-vs-orthosteric is not functional-vs-non-functional. E's stated synthesis, marked as
a reading rather than a retrieved claim: "allosteric sites are less conserved than orthosteric
sites, but functional pockets in general are more conserved than non-functional ones, and the
two comparisons have different reference classes." A single study reporting both contrasts on
one dataset would settle it.

### C10 — Which crypticity definition

Pocket-score rule (CryptoSite / Vajda: apo < 0.1, holo > 0.4) against pocket-atom RMSD ≥ 2 Å
(CryptoBench). Both `[VERIFIED-FULLTEXT]` in at least one report.

**What would settle it:** nothing — they measure different physical quantities
(_detectability_ against _motion_) and can disagree on the same site in both directions. The
decidable part is reporting both for every arm.

### C11 — What fraction of cryptic sites are allosteric

8/19 = 42 % (Vajda 2018) against 17/58 = 29 % (CryptoSite). Both `[VERIFIED-FULLTEXT]`.
**What would settle it:** the denominators differ (Vajda restricts to validated sites with
sub-300 nM ligands), so the two are not strictly contradictory. A single curation applying one
inclusion rule would settle it.

### C12 — SiteMap Dscore thresholds

Two secondary sources give incompatible thresholds, both `[UNVERIFIED]`:

- "typical Dscores for druggable protein pockets are above 1.108 while Dscores below 0.871
  suggest a difficult to drug protein"
- "≤ 0.7 difficult-to-drug, 0.7–0.8 intermediate, > 0.8 highly druggable"

E's assessment: these "almost certainly conflate SiteScore with Dscore, or a different
normalisation." The primary, Halgren 2009 `10.1021/ci800324m`, is paywalled and was not read.
**E's instruction: do not quote any Dscore threshold.**
**What would settle it:** reading Halgren 2009.

### C13 — The BDT DOI — **resolved at merge**

Report C gives `10.1093/bioinformatics/btq543`; report E gives
`10.1093/bioinformatics/btq551`.

**Resolved by direct retrieval during this merge** `[VERIFIED-FULLTEXT, resolved at merge]`:

- `10.1093/bioinformatics/btq543` = Roche DB, **Tetchner SJ**, McGuffin LJ, "The binding site
  distance test score: a robust method for the assessment of predicted protein binding sites",
  _Bioinformatics_ 26(22):2920–2921, 2010. **This is BDT.** Note that C's author list gives
  the middle author as "Buenavista MT"; the correct middle author is **Stuart J. Tetchner**.
- `10.1093/bioinformatics/btq551` = Magnan CN et al., "High-throughput prediction of protein
  antigenicity using protein microarray data", _Bioinformatics_ 26(23):2936–2943, 2010. **An
  unrelated paper.** E's DOI is wrong.

### C14 — Authorship of `10.1186/1471-2105-11-286` — **resolved at merge**

Report B attributes it to "Ma B et al."; `evaluation-protocol-lit.md` attributes it to
"Guharoy M., Chakrabarti P."

**Resolved by direct retrieval during this merge** `[VERIFIED-FULLTEXT, resolved at merge]`:
**Guharoy M, Chakrabarti P**, "Conserved residue clusters at protein-protein interfaces and
their use in binding site identification", _BMC Bioinformatics_ 2010;11:286. The earlier repo
file is correct; report B's attribution is wrong. The DOI, the content and the statistics B
extracted from it are unaffected.

### C15 — Attribution of the "78 % DCC / 60 % / 64 % F1 / 64 % MCC" figures

`evaluation-protocol-lit.md` §5 item 12 recorded them as "almost certainly
`10.1016/j.csbj.2024.10.036`", after a search summariser had attached them to CryptoBench,
whose own full text disagrees.

**Reports A and C both read STINGAllo directly and both attribute them to
`10.1093/bib/bbaf424`** `[VERIFIED-FULLTEXT]` (convergent: A, C). Mariano et al.
`10.1016/j.csbj.2024.10.036` is STINGAllo's precursor and reports KS tests on feature
distributions with no p-values in the text.

**What would settle it:** it is settled. Two independent full-text reads against one search
summary. The earlier file's provisional attribution is superseded.

### C16 — Ohm's metric names against standard usage

Ohm's "TPR" is precision and its "PPV" is recall (§2.5, convergent: A, C). This is a
terminological collision with the rest of the field, not a disagreement about a value. Ohm's
reported numbers (TPR 0.57, PPV 0.72 against Amor's 0.23 / 0.48) are internally consistent
with Ohm's own definitions.
**What would settle it:** nothing to settle. Do not copy the names; state which quantity is
meant.

### C17 — PASSer2.0's two labelling rules

"≥1 shared residue" on the ASD arm and "closest centroid" on the ASBench arm, in one paper
(convergent: A, B, C). Not a disagreement between sources but a disagreement inside one
source, which makes its 4.87 % positive rate a mixture of two label definitions.
**What would settle it:** re-labelling both arms under one rule and re-reporting.

### C18 — Residue level or pocket level

| Position               | Sources                                                                                                                                                                                                                                                                                              |
| ---------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Pocket**             | P2Rank `10.1186/s13321-018-0285-8`; Utgés & Barton `10.1186/s13321-024-00923-z` (§7.4)                                                                                                                                                                                                               |
| **Residue**            | CASP FN category since CASP8 `10.1002/prot.24495`; PocketMiner `10.1038/s41467-023-36699-3`; CryptoSite `10.1016/j.jmb.2016.01.029`; CryptoBench `10.1093/bioinformatics/btae745`; COACH `10.1093/bioinformatics/btt447`; DeepAllo `10.1093/bioinformatics/btaf294`; STINGAllo `10.1093/bib/bbaf424` |
| **Both, in one paper** | STINGAllo; LIGYSIS-bench                                                                                                                                                                                                                                                                             |

C's own qualification, which narrows the disagreement: Utgés & Barton's objection is
specifically about **thresholded** residue metrics (F1, MCC) penalising methods that nominate
more sites, and does not obviously extend to threshold-free AUROC/AUPRC.
**What would settle it:** the deliverable. The unit scored should be the unit shipped; both
sides agree on that and disagree about what is shipped.

### C19 — Does the allosteric literature use a statistical null at all?

`evaluation-protocol-lit.md` §2, headline finding: "the allosteric- and cryptic-site
prediction literature I read does not use a statistical null model at all. Not a matched one,
not a uniform random one."

**Contradicted in its strong form by B and D**, which both reached the Barahona/Yaliraki
lineage the earlier review did not: 1,000 size- and diameter-matched surrogate sites per
protein, distance-conditioned quantile regression, and a 10,000-resample bootstrap 95 % CI
(`10.1038/ncomms12477`, `10.1093/nar/gkab350`, `10.1016/j.patter.2021.100408`) — plus
KeyAlloSite's contiguous size-matched surface patches (`10.7554/eLife.81850`).

**Confirmed in its weak form**: 13 of 18 papers state no test at all (B), ≈15 of 17 method
rows have no null (D), 0 of 18 apply any multiplicity correction, 0 state a null in words.
The earlier file's own addendum had already flagged CryptoSite's 705 concave surface patches
as a counterexample it could not reach.

**What would settle it:** it is settled. The earlier claim was true of the six full texts that
review could read and false of the field.

### C20 — CryptoSite's TPR

Three renderings of the same number:

- abstract: "the true positive and false positive rates are 73% and 29%"
  (`evaluation-protocol-lit.md`, `[VERIFIED-ABSTRACT]`)
- body: "79 % and 29 % at the residue score threshold of 0.05"
  (`evaluation-protocol-lit.md` addendum, `[VERIFIED-FULLTEXT]`)
- report A: "TPR 73 % / FPR 29 % at residue-score threshold 0.05" — the abstract's value
  paired with the body's threshold `[VERIFIED-FULLTEXT]` for the retrieval, but the pairing
  is not in either place in the paper

**What would settle it:** it is an internal inconsistency in the paper itself. Cite the body
figure with its threshold, or the abstract figure as the abstract's — not interchangeably, and
not crossed.

### C21 — The Amor surrogate diameter clause

D's fetch of Amor 2016: surrogates' "diameter…is **not larger than** that of the allosteric
site". B's fetch of the Patterns restatement: "the diameter … is **smaller than** that of the
allosteric site". Both `[VERIFIED-FULLTEXT]`. The difference is whether equality is admitted;
the one-sidedness, which is the load-bearing property, is identical in both.
**What would settle it:** the Amor 2016 methods section, which both reviewers reached — the
difference is between the original and its restatement, not between two readings of one text.

### C22 — Publication year of the Patterns benchmarking paper

A dates `10.1016/j.patter.2021.100408` to 2022; B and E date it 2021; D marks the journal DOI
unverified and cites the bioRxiv preprint `10.1101/2021.08.16.456251`. Volume 3(1) is the
January 2022 issue with 2021 online publication. **What would settle it:** the publisher's
issue record. The DOI is the same in all four and is `[VERIFIED-FULLTEXT]` in A, B and E,
which also closes D's "journal DOI unverified" flag.

---

## 9. What is not established

The merged unknown list from all five reports plus `evaluation-protocol-lit.md` §5. Each
entry names the specific number wanted and why it is unreachable.

### 9.1 Status of the earlier file's §5 list

| #   | Earlier entry                                                                                           | Status after the five reports                                                                                                                                                                                                                                                                                                                                                                                              |
| --- | ------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | CryptoSite per-feature AUC values                                                                       | **CLOSED** already, in the earlier file's own addendum                                                                                                                                                                                                                                                                                                                                                                     |
| 2   | CryptoSite benchmark size                                                                               | **CLOSED** already, in the addendum                                                                                                                                                                                                                                                                                                                                                                                        |
| 3   | Whether any allosteric/cryptic paper uses a spatially matched or contiguous patch null                  | **CLOSED** (convergent: B, D). Yes: KeyAlloSite grows contiguous size-matched patches around random surface centres, `10.7554/eLife.81850`; the Barahona/Yaliraki lineage uses 1,000 size- and diameter-matched surrogate sites per protein, `10.1038/ncomms12477`, `10.1093/nar/gkab350`, `10.1016/j.patter.2021.100408`. **The earlier file's absence claim was true of what it could read and false of the field**      |
| 4   | Enrichment factor for allosteric residue prediction                                                     | **CLOSED as a negative.** C read the evaluation sections of 22 site-prediction papers and **none reports EF, RIE or BEDROC**. The enrichment idea survives in this field as a hypergeometric (`10.1073/pnas.2414333121`) or a surrogate-site bootstrap (`10.1038/ncomms12477`), not as EF                                                                                                                                  |
| 5   | Precedent for an exact hypergeometric null on precision@k in structural bioinformatics                  | **CLOSED.** PNAS 2024 global-hinge-site paper, `10.1073/pnas.2414333121`, gives the exact formula, reports average P = 4.547 × 10⁻³ and average enrichment 4.13× over random, from the group that founded the ENM field, on a residue-level score from an elastic network                                                                                                                                                  |
| 6   | Precedent for pooling p-values across targets at small N, and any justification                         | **STILL OPEN.** None of the five reports found one. B proposes Fisher/Stouffer and cites **no in-field precedent**                                                                                                                                                                                                                                                                                                         |
| 7   | Between-target variance of AUC for allosteric prediction — the SD of per-protein AUC across a benchmark | **STILL OPEN, and still the single most important missing number.** No report found a paper publishing a per-protein AUC distribution. CTQW 2026 publishes per-protein ρ and τ distributions but not AUC                                                                                                                                                                                                                   |
| 8   | Exact DCC definition and threshold used by CryptoBench                                                  | **STILL OPEN.** C's retrieval gives CryptoBench's metric list as "TPR, FPR, F1, ACC, MCC" plus AUC/AUPRC from probabilities, with per-method thresholds chosen by F1 (e.g. 0.95 for their pLM-NN). No DCC threshold surfaced                                                                                                                                                                                               |
| 9   | DCC vs DCA in P2Rank                                                                                    | **CLOSED.** The naming collision is real and documented (§2.2). P2Rank's "DCC" is the field's DCA. The 4 Å threshold's true primary is PASS 2000, `10.1023/A:1008124202956`, and DCC at equivalent strictness is 10–12 Å per `10.1186/s13321-024-00923-z`                                                                                                                                                                  |
| 10  | DeepAllo's negative-pocket definition                                                                   | **PARTLY CLOSED.** A and B both retrieved it: positives are pockets containing allosteric-modulator residues, 304 of 4,223 = 7.76 %; residue-level positives 5.12 %; "Every residue not in an allosteric pocket" is negative. **Still unstated: whether any undersampling or size matching was applied**                                                                                                                   |
| 11  | PASSer test-set size                                                                                    | **CLOSED.** PASSer v1: 90 proteins from ASD, 2,246 pockets, 119 allosteric / 2,127 non-allosteric. PASSer-NAR: ASD 207 proteins, CASBench 1,049. PASSer2.0: 204 proteins, 5,155 pockets                                                                                                                                                                                                                                    |
| 12  | Attribution of "78 % DCC / 60 % / 64 % F1 / 64 % MCC"                                                   | **CLOSED, and the earlier provisional attribution is corrected.** They are STINGAllo's, `10.1093/bib/bbaf424` (convergent: A, C). See §8 C15                                                                                                                                                                                                                                                                               |
| 13  | Whether AUC-PR has been argued as preferable specifically for allosteric residue prediction             | **PARTLY CLOSED.** Allo-Allo makes AUPRC its leading column and headline abstract claim ("a 67 % higher AUPRC than state-of-the-art methods"), `10.1101/2024.09.28.615583`. A 2026 kinase pLM study argues average precision is the appropriate headline under this imbalance, `[UNVERIFIED]`. **No allosteric-specific methodological argument paper exists**, and McDermott et al. 2024 argues against the general claim |
| 14  | A DOI-backed precedent for random-surface-patch nulls in binding-site prediction                        | **CLOSED.** KeyAlloSite `10.7554/eLife.81850` (surface-seeded, size-matched, contiguous, Student's t-test, **4 repeats**); Amor/ProteinLens/Patterns surrogate sites; Guharoy & Chakrabarti `10.1186/1471-2105-11-286` (1,000 equal-size random subsets from the same interface, Mann-Whitney U)                                                                                                                           |

**Nine of fourteen closed or partly closed; five still open.**

### 9.2 Numbers wanted and not obtainable

| #   | The number wanted                                                                                                                                                                                  | Why it is unreachable                                                                                                                                                                                                                                                                                                  | Reports            |
| --- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------ |
| 1   | **SD of per-protein AUC across an allosteric benchmark.** The quantity that sets power at small N                                                                                                  | No paper publishes a per-protein AUC distribution. PocketMiner's ±0.04 is across CV splits, not across targets                                                                                                                                                                                                         | earlier file, A, D |
| 2   | **The true apo-versus-holo penalty for the same method on the same sites.** ESSA's 21 pp and AllositePro's 43 pp are on 14 sites; Wu's 5.9–10.1 pp is a **ligand-removal** delta, not an apo delta | CAPASP 2026 has the right design (CAPASP-General holo vs CAPASP-Unbound apo) but its per-tool numbers and dataset sizes are behind a Springer paywall. `10.1007/s10822-026-00831-4`                                                                                                                                    | A, C, D, E         |
| 3   | **Variance in a network-propagation score explained by distance from the source alone** (R², or AUC of a distance-only ranker)                                                                     | Nobody has published it. The literature named the confound ("distance bias", `10.1093/nar/gkab350`), modelled it (`log Π ∝ β₀ + β₁d`, `10.1038/ncomms12477`) and corrected for it, but never quantified it                                                                                                             | D                  |
| 4   | **Accuracy as a function of the allosteric site's distance from the active site**                                                                                                                  | No published curve exists                                                                                                                                                                                                                                                                                              | E                  |
| 5   | **Accuracy as a function of protein size or residue count**                                                                                                                                        | No published relation. APOP has the data (10–242 pockets per protein, 104 proteins) and did not analyse it                                                                                                                                                                                                             | E                  |
| 6   | **The fraction of _allosteric_ sites that are cryptic**                                                                                                                                            | Unreported. Checked against CryptoBench, CryptoBank and Gašparíková 2025                                                                                                                                                                                                                                               | E                  |
| 7   | **Quantified bias of pocket-based druggability scores against allosteric pockets**                                                                                                                 | Two sources assert allosteric pockets are smaller and less pocket-like; nobody has measured what that does to Dscore or DoGSiteScorer                                                                                                                                                                                  | E                  |
| 8   | **A matched allosteric-versus-orthosteric hit rate across multiple targets**                                                                                                                       | The mGlu5 comparison is one target and is structure-guided-versus-blind, not allosteric-versus-orthosteric                                                                                                                                                                                                             | E                  |
| 9   | **Per-tool numbers and dataset sizes from CAPASP 2026** — the only modern independent evaluation with a dedicated apo subset                                                                       | Springer IdP redirect; abstract recovered via PubMed efetch (PMID 42126486), body not reached. **The most valuable single missing item across all five reviews**                                                                                                                                                       | A, C, D, E         |
| 10  | **Whether allosteric-site labels' spatial contiguity has ever been acknowledged as a statistical-independence problem in this field**                                                              | Bounded by counts, not by exhaustion: PubMed returns 1 allostery paper with "permutation test", 1 with "null model"/"null distribution", 1 protein-residue paper with "spatial autocorrelation", 0 with bootstrap CIs, and arXiv 0 for "decoy pocket". Absence of evidence at this density is strong, but is not proof | B                  |
| 11  | **Whether anyone has criticised the missing centrality/distance baseline in print**                                                                                                                | D ran four converging searches and found no such statement, but **the one query designed to find exactly that phrasing was not run** (budget exhausted). Read as strongly suggested, not established                                                                                                                   | D                  |

### 9.3 Sources that exist and could not be read

| Source                                                                                            | DOI                                                      | Barrier                                                                                                                              |
| ------------------------------------------------------------------------------------------------- | -------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| **AllositePro** (Song et al. 2017) — its own headline numbers                                     | `10.1021/acs.jcim.7b00014`                               | ACS HTTP 403 on `/doi/` and `/doi/abs/`; PubMed cookie wall. Only third-party re-runs available                                      |
| **STRESS** (Clarke et al. 2016) — its own headline numbers, validation dataset size, success rate | `10.1016/j.str.2016.03.008` (DOI itself unverified in D) | ScienceDirect 403; PMC4883016 exists but metrics not extracted                                                                       |
| **ZHMolEReP** — AUC 0.7858, recall 0.7037, 33/40                                                  | `10.1021/acs.jcim.6c00141`                               | ACS 403. **All three numbers come from a search-result summary in both A and D. One of only two AUC data points for the ENM family** |
| **Allofusion** — all metrics                                                                      | `10.1021/acs.jcim.5c01033`                               | ACS 403                                                                                                                              |
| **AllosES / transfer-entropy ensemble** — all metrics                                             | `10.1021/acs.jcim.4c00544`                               | ACS 403; abstract-level mention of class-imbalance handling only                                                                     |
| **Truchon & Bayly 2007** — BEDROC/RIE normalisation constants, the α = 20 rationale               | `10.1021/ci600426e`                                      | ACS 403 + PubMed cookie wall. Formulas taken from the RDKit implementation; `RIE_min` sign did not render consistently               |
| **Chen et al. 2011** — the DCC lineage's root                                                     | `10.1016/j.str.2011.02.015`                              | Paywalled, no PMCID. Known only via citing papers                                                                                    |
| **Allosite 2013** — the distance cutoff and pocket-labelling threshold                            | `10.1093/bioinformatics/btt399`                          | Criteria are in the SI, not the article body; SI not retrieved                                                                       |
| **Halgren 2009** — the SiteMap Dscore thresholds                                                  | `10.1021/ci800324m`                                      | Paywalled; abstract elided. See §8 C12                                                                                               |
| **Schmidtke & Barril 2010** — fpocket druggability thresholds                                     | `10.1021/jm100574m`                                      | Abstract elided                                                                                                                      |
| **Beglov et al. 2018** — structural origins of cryptic sites                                      | `10.1073/pnas.1711490115`                                | PNAS HTTP 403                                                                                                                        |
| **Ludlow et al. 2015** — how common secondary binding sites are                                   | `10.1073/pnas.1518946112`                                | PNAS 403 / navigation shell only                                                                                                     |
| **Wodak et al. 2019** — "Allostery in Its Many Disguises"                                         | `10.1016/j.str.2019.01.003`                              | Binary PDF with no text layer                                                                                                        |
| **Zheng 2023** — named in `docs/FIELD.md` and `CHALLENGE.md`                                      | `10.1063/5.0141630`                                      | Abstract page located; method and validation numbers not fetched                                                                     |
| **Gfeller & De Los Rios 2007** — the specific coarse-graining error metric                        | `10.1103/PhysRevLett.99.038701`                          | Abstract only; PRL full text not reached                                                                                             |
| **P2Rank 2018** — the exact DCA/DCC defining sentences                                            | `10.1186/s13321-018-0285-8`                              | Springer redirect returned a lossy extraction twice in A; C reached the partial quote via Europe PMC                                 |
| **Schmidtke et al. 2010**, four-algorithm binding-site comparison                                 | —                                                        | Not fetched; MOc known only via fpocket 2009                                                                                         |
| **JMB 2025, "Sequence and Structure-based Prediction of Allosteric Sites"**                       | PII S0022283625003717                                    | ScienceDirect 403                                                                                                                    |
| **Drug Discovery Today review 2025**                                                              | `10.1016/j.drudis.2025.104466`                           | Paywalled; abstract only                                                                                                             |
| **PASSerRank** full text                                                                          | `10.48550/arXiv.2302.01117`                              | arXiv PDF returned undecoded binary; PMC ID 404'd on Europe PMC                                                                      |

### 9.4 Infrastructure that is down, and what that costs

| Resource                                                | Status 2026-08-24                                                                                                     | Consequence                                                                |
| ------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| **ASD (Allosteric Database)**, `mdl.shsmu.edu.cn/ASD/`  | **certificate has expired** — fetch fails on http and https                                                           | The canonical allosteric label source is unreachable                       |
| **ASBench**, `mdl.shsmu.edu.cn/asbench`                 | **certificate has expired** — same host, same failure                                                                 | The canonical benchmark set is unreachable                                 |
| **sc-PDB**                                              | `connect ECONNREFUSED 130.79.85.37:443`                                                                               | —                                                                          |
| **Binding MOAD**                                        | HTTP 403, consistent with the published sunset notice ("available online at BindingMOAD.org through June 31st, 2024") | PocketMiner's negative-class construction cannot be reproduced from source |
| **Semantic Scholar Graph API**                          | HTTP 429 on 3 of 4 attempts across two reports                                                                        | —                                                                          |
| **CASBench**, `biokinet.belozersky.msu.ru/casbench`     | **loads**                                                                                                             | Reachable label source                                                     |
| **AlloBench**, `github.com/djmaity/allobench` (MIT)     | **loads**                                                                                                             | Reachable label source                                                     |
| **CryptoBench**, `github.com/skrhakv/CryptoBench` (MIT) | GitHub loads; OSF page is a JS shell, contents not enumerable by fetch                                                | Partly reachable                                                           |

**Both canonical allosteric label sources are down, on the same expired-certificate host, and
this was confirmed twice** `[VERIFIED-FULLTEXT]`. Any label set derived from them cannot
currently be re-derived by a reader from the source.

### 9.5 Things that do not exist

- **"AlloseeIt"** — report A ran every query it could and found **no matching tool in any
  index**. Either it is misnamed or it is not indexed. Recorded as a gap, not guessed at.
- **"ALLO" as a distinct benchmark** — B found no such benchmark under that name.
  "AlloBench", "AlloRep", "AlloMAPS", "Allo-Allo" and "Allo-PED" are all distinct things.
  (Note: AlloBench's comparison table does include a tool called **ALLO**, median JI 0.025 —
  that is a predictor, not a benchmark.)
- **A named "precision@N" metric in the allosteric literature** — A's targeted query returned
  no allosteric paper using the term. A real negative result, not a failure to find.
- **A residue-level spatial tolerance shell** — 47 Europe PMC full-text hits, none defining
  one.
- **An allosteric-specific hit criterion** — the field reuses orthosteric machinery (§2.7).
- **A TRIPOD/CONSORT analogue for structure-based site prediction** — three partial standards,
  no unified one (§7.1).
- **Any use of Rank-Biased Overlap in the protein-allostery literature** — zero.
- **Any paper in the allosteric-prediction family that perturbs input coordinates and measures
  ranking degradation** — none found.

### 9.6 Unrun queries that bound the negative findings

- **D, query designed to find published statements that allosteric predictors perform "no
  better than a simple geometric baseline"** — not run, budget exhausted. This is the query
  most directly relevant to §4.2's negative finding.
- **B, P2Rank primary text and the ALLO database** — planned, dropped at 200 cumulative
  calls. COACH420/HOLO4K construction details are therefore `[UNVERIFIED]`.
- **E, three queries** — `Krojer von Delft Fraser 2020 allosteric fragment screening review
abstract "secondary sites" percentage functional relevance` (recovered by direct fetch);
  `allosteric activator versus inhibitor binding site differences network communication
asymmetry prediction` (**gap**); `"apo" versus "holo" structure allosteric site prediction
performance drop measured percentage ESSA APOP` (**gap** — and this is the query that would
  have addressed §9.2 item 2).

### 9.7 Cross-closures between the five reports

Gaps one report could not close and another did. These are recorded because they show where a
single review would have under-reported:

| Gap                                                                                   | Report that could not close it                                             | Report that closed it                                                      |
| ------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| **Amor et al. 2016 full text** — the matched-surrogate null's originating description | E (`[GAP]`, cited via Wu 2021)                                             | **B and D both fetched it** `[VERIFIED-FULLTEXT]`                          |
| **CASBench DOI**                                                                      | B ("DOI unknown, not stated in PMC text; PMID 31024751, PMCID PMC6475866") | **E**: `10.32607/20758251-2019-11-1-74-80` `[VERIFIED-FULLTEXT]`           |
| **Patterns benchmarking paper, journal DOI**                                          | D ("journal DOI unverified")                                               | **A, B and E** all carry `10.1016/j.patter.2021.100408` from fetched pages |
| **PASSer v1's dataset size and full metric set**                                      | earlier file (`[VERIFIED-ABSTRACT]`, "test-set size unknown")              | **A** `[VERIFIED-FULLTEXT]`                                                |
| **AlloBench's JI-vs-inverse-distance sentence**                                       | D (`[UNVERIFIED]`, and it carries weight in D §3.2)                        | **E** fetched it at full text `[VERIFIED-FULLTEXT]`                        |
| **The "78 % DCC" attribution**                                                        | earlier file (provisional, wrong)                                          | **A and C**, independently `[VERIFIED-FULLTEXT]`                           |

---

## 10. Bibliography

Every DOI cited above, once, with title and venue. DOI strings are preserved exactly as the
source reports carry them. The tag is the **highest** verification level any of the six source
documents reached for that item; where reports disagreed on the level, the lower one is named
in the note.

### 10.1 Allosteric-site prediction methods

| DOI                              | Short name               | Title                                                                                                                                                                | Venue, year                                   | Tag                                                               |
| -------------------------------- | ------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------- | ----------------------------------------------------------------- |
| `10.1093/bioinformatics/btt399`  | Allosite                 | Allosite: a method for predicting allosteric sites                                                                                                                   | Bioinformatics 29(18):2357–2359, 2013         | `[VERIFIED-FULLTEXT]` — criteria in unretrieved SI                |
| `10.1093/bioinformatics/btu002`  | PARS                     | PARS: a web server for the prediction of Protein Allosteric and Regulatory Sites                                                                                     | Bioinformatics 30(9):1314–1315, 2014          | `[VERIFIED-FULLTEXT]`                                             |
| `10.1186/1471-2105-13-273`       | Panjkovich & Daura 2012  | Exploiting protein flexibility to predict the location of allosteric sites                                                                                           | BMC Bioinformatics 13:273, 2012               | `[VERIFIED-FULLTEXT]`                                             |
| `10.1186/s12859-015-0771-1`      | AlloPred                 | AlloPred: prediction of allosteric pockets on proteins using normal mode perturbation analysis                                                                       | BMC Bioinformatics 16:335, 2015               | `[VERIFIED-FULLTEXT]`                                             |
| `10.1021/acs.jcim.7b00014`       | AllositePro              | Improved Method for the Identification and Validation of Allosteric Sites                                                                                            | J Chem Inf Model 57(9):2358–2363, 2017        | **unreachable (ACS 403)**                                         |
| `10.1016/j.str.2016.03.008`      | STRESS                   | Identifying Allosteric Hotspots with Dynamics                                                                                                                        | Structure 24(5):826–837, 2016                 | **unreachable (403); DOI itself unverified in D**                 |
| `10.1016/j.csbj.2020.06.020`     | ESSA                     | Essential site scanning analysis: a new approach for detecting sites that modulate the dispersion of protein global motions                                          | Comput Struct Biotechnol J 18:1577–1586, 2020 | `[VERIFIED-FULLTEXT]`                                             |
| `10.1038/s41467-020-17618-2`     | Ohm                      | Mapping allosteric communications within individual proteins                                                                                                         | Nat Commun 11:3862, 2020                      | `[VERIFIED-FULLTEXT]`                                             |
| `10.1088/2632-2153/abe6d6`       | PASSer v1                | PASSer: prediction of allosteric sites server                                                                                                                        | Mach Learn Sci Technol 2(3):035015, 2021      | `[VERIFIED-FULLTEXT]`                                             |
| `10.3389/fmolb.2022.879251`      | PASSer2.0                | PASSer2.0: accurate prediction of protein allosteric sites through automated machine learning                                                                        | Front Mol Biosci 9:879251, 2022               | `[VERIFIED-FULLTEXT]`                                             |
| `10.48550/arXiv.2302.01117`      | PASSerRank               | PASSerRank: Prediction of Allosteric Sites with Learning to Rank                                                                                                     | J Comput Chem 44(28):2223–2229, 2023          | `[VERIFIED-ABSTRACT]` — PDF unparseable                           |
| `10.1093/nar/gkad303`            | PASSer (NAR)             | PASSer: fast and accurate prediction of protein allosteric sites                                                                                                     | Nucleic Acids Res 51(W1):W427–W431, 2023      | `[VERIFIED-FULLTEXT]`                                             |
| `10.1093/bioinformatics/btad275` | APOP                     | Predicting allosteric pockets in protein biological assemblages                                                                                                      | Bioinformatics 39(5):btad275, 2023            | `[VERIFIED-FULLTEXT]`                                             |
| `10.7554/eLife.81850`            | KeyAlloSite              | Coevolution-based prediction of key allosteric residues for protein function regulation                                                                              | eLife 12:e81850, 2023                         | `[VERIFIED-FULLTEXT]`                                             |
| `10.1186/s13321-024-00882-5`     | MEF-AlloSite             | MEF-AlloSite: an accurate and robust Multimodel Ensemble Feature selection for the Allosteric Site identification model                                              | J Cheminform 16, 2024                         | `[VERIFIED-FULLTEXT]`                                             |
| `10.1101/2024.09.28.615583`      | Allo-Allo                | Allo-Allo: Data-efficient prediction of allosteric sites                                                                                                             | bioRxiv, 2024                                 | `[VERIFIED-FULLTEXT]`                                             |
| `10.1093/bioinformatics/btaf294` | DeepAllo                 | DeepAllo: allosteric site prediction using protein language model with multitask learning                                                                            | Bioinformatics 41(6):btaf294, 2025            | `[VERIFIED-FULLTEXT]`                                             |
| `10.1101/2025.03.28.645953`      | Allo-PED                 | Allo-PED / AlloPED                                                                                                                                                   | bioRxiv, 2025                                 | `[VERIFIED-FULLTEXT]`                                             |
| `10.1093/bib/bbaf424`            | STINGAllo                | STINGAllo                                                                                                                                                            | Brief Bioinform 26(4):bbaf424, 2025           | `[VERIFIED-FULLTEXT]`                                             |
| `10.1016/j.csbj.2024.10.036`     | Mariano et al.           | Protein allosteric site identification using machine learning and per amino acid residue reported internal protein nanoenvironment descriptors (STINGAllo precursor) | Comput Struct Biotechnol J, 2024              | `[VERIFIED-FULLTEXT]`                                             |
| `10.1021/acs.jcim.6c00141`       | ZHMolEReP                | ZHMolEReP                                                                                                                                                            | J Chem Inf Model 66(10):6181–6195, 2026       | **unreachable (ACS 403); numbers `[UNVERIFIED]`**                 |
| `10.1021/acs.jcim.5c01033`       | Allofusion               | Allofusion                                                                                                                                                           | J Chem Inf Model 65(16):8858–8870, 2025       | **unreachable (ACS 403)**                                         |
| `10.1021/acs.jcim.4c00544`       | AllosES                  | Prediction of Protein Allosteric Sites with Transfer Entropy                                                                                                         | J Chem Inf Model 64(15):6197–6204, 2024       | **unreachable (ACS 403)**                                         |
| `10.1101/2025.06.27.662060`      | Eccleston & Furnham      | Allosteric Site Prediction Using Protein Language Models and Orthosteric Conditioning                                                                                | bioRxiv, 2025                                 | `[VERIFIED-FULLTEXT]`                                             |
| `10.1371/journal.pcbi.1000531`   | Demerdash et al.         | Structure-Based Predictive Models for Allosteric Hot Spots                                                                                                           | PLoS Comput Biol 5(10):e1000531, 2009         | `[VERIFIED-FULLTEXT]`                                             |
| `10.1371/journal.pcbi.1006228`   | Tee et al. (SBSMMA)      | Reversing allosteric communication: from detecting allosteric sites to inducing and tuning targeted allosteric response                                              | PLoS Comput Biol 14(6):e1006228, 2018         | `[VERIFIED-FULLTEXT]`                                             |
| `10.1093/nar/gkt284`             | MCPath                   | MCPath: Monte Carlo path generation approach to predict likely allosteric pathways and functional residues                                                           | Nucleic Acids Res 41:W249–W255, 2013          | `[UNVERIFIED]` — DOI unverified in D; no cohort benchmark located |
| `10.1093/nar/gkt460`             | SPACER                   | SPACER: server for predicting allosteric communication and effects of regulation                                                                                     | Nucleic Acids Res 41:W266–W272, 2013          | `[VERIFIED-FULLTEXT]`                                             |
| `10.1093/bioinformatics/btac380` | Haliloglu et al.         | Prediction of allosteric communication pathways in proteins                                                                                                          | Bioinformatics 38(14):3590–3599, 2022         | `[VERIFIED-ABSTRACT]` — six case studies, no cohort metric        |
| `10.1371/journal.pcbi.1002148`   | Mitternacht & Berezovsky | Binding leverage as a molecular basis for allosteric regulation                                                                                                      | PLoS Comput Biol, 2011                        | `[UNVERIFIED]`                                                    |
| `10.1088/1478-3975/ae3e49`       | Erman 2026               | GNM framework for allostery in KRAS                                                                                                                                  | Phys Biol, 2026                               | `[VERIFIED-FULLTEXT]`                                             |

### 10.2 Network, elastic-network and propagation methods

| DOI                             | Short name              | Title                                                                                                              | Venue, year                           | Tag                                                 |
| ------------------------------- | ----------------------- | ------------------------------------------------------------------------------------------------------------------ | ------------------------------------- | --------------------------------------------------- |
| `10.1371/journal.pcbi.0030172`  | Chennubhotla & Bahar    | Signal Propagation in Proteins and Relation to Equilibrium Fluctuations                                            | PLoS Comput Biol 3(9):e172, 2007      | `[VERIFIED-FULLTEXT]`                               |
| `10.1038/ncomms12477`           | Amor et al. 2016        | Prediction of allosteric sites and mediating interactions through bond-to-bond propensities                        | Nat Commun 7:12477, 2016              | `[VERIFIED-FULLTEXT]`                               |
| `10.1039/c4mb00088a`            | Amor et al. 2014        | (bond-to-bond precursor)                                                                                           | Mol Biosyst, 2014                     | `[UNVERIFIED]`                                      |
| `10.1093/nar/gkab350`           | ProteinLens             | ProteinLens: a web-based application for the analysis of allosteric signalling on atomistic graphs of biomolecules | Nucleic Acids Res 49(W1):W551, 2021   | `[VERIFIED-FULLTEXT]`                               |
| `10.1016/j.patter.2021.100408`  | Wu, Strömich & Yaliraki | Prediction of allosteric sites and signaling: Insights from benchmarking datasets                                  | Patterns 3(1):100408, 2021/2022       | `[VERIFIED-FULLTEXT]`; year disputed, §8 C22        |
| `10.1101/2021.08.16.456251`     | same, preprint          | (bioRxiv preprint of the above)                                                                                    | bioRxiv, 2021                         | `[VERIFIED-FULLTEXT]`                               |
| `10.1021/jacs.6c08053`          | CTQW 2026               | Continuous-time quantum walk centrality for protein residue interaction networks (preprint arXiv:2604.17486)       | J Am Chem Soc 2026;148(27):29206-29219 | `[VERIFIED-FULLTEXT]`; Mohtashim SI, Sajjan M, Kais S |
| `10.1073/pnas.0810961106`       | Sethi et al.            | Dynamical networks in tRNA:protein complexes                                                                       | PNAS 106:6620–6625, 2009              | `[UNVERIFIED]`; **MD-derived**                      |
| `10.48550/arXiv.1802.10207`     | Malik et al. 2018       | Analysis of allosteric communication sub-systems                                                                   | arXiv:1802.10207, 2018                | `[VERIFIED-FULLTEXT]`                               |
| `10.1098/rstb.2017.0187`        | Stock & Hamm            | A non-equilibrium approach to allosteric communication                                                             | Phil Trans R Soc B 373:20170187, 2018 | `[VERIFIED-FULLTEXT]`/`[UNVERIFIED]` — D tags F/S   |
| `10.1103/PhysRevLett.99.038701` | Gfeller & De Los Rios   | Spectral coarse graining of complex networks                                                                       | Phys Rev Lett 99:038701, 2007         | `[VERIFIED-ABSTRACT]`                               |
| `10.1021/acs.jctc.8b00654`      | Diggins et al.          | Optimal coarse-grained site selection in elastic network models of biomolecules                                    | J Chem Theory Comput, 2018            | `[VERIFIED-FULLTEXT]`                               |
| `10.1016/j.jmb.2022.167696`     | Dubanevics & McLeish    | Optimising elastic network models for protein dynamics and allostery                                               | J Mol Biol, 2022                      | `[VERIFIED-ABSTRACT]`                               |
| `10.1063/5.0141630`             | Zheng 2023              | (named in `CHALLENGE.md` and `docs/FIELD.md`)                                                                      | J Chem Phys 158:124127, 2023          | **not fetched; details unknown**                    |
| `10.3389/fbinf.2021.684970`     | Brysbaert & Lensink     | (residue interaction network analysis)                                                                             | Front Bioinform 1:684970, 2021        | `[VERIFIED-FULLTEXT]`                               |

### 10.3 Cryptic-pocket prediction

| DOI                              | Short name           | Title                                                                                                             | Venue, year                        | Tag                   |
| -------------------------------- | -------------------- | ----------------------------------------------------------------------------------------------------------------- | ---------------------------------- | --------------------- |
| `10.1016/j.jmb.2016.01.029`      | CryptoSite           | Cryptic Binding Sites on Proteins: Definition, Detection, and Druggability                                        | J Mol Biol 428(4):709–719, 2016    | `[VERIFIED-FULLTEXT]` |
| `10.1038/s41467-023-36699-3`     | PocketMiner          | Predicting locations of cryptic pockets from single protein structures using the PocketMiner graph neural network | Nat Commun 14:1177, 2023           | `[VERIFIED-FULLTEXT]` |
| `10.1101/2022.06.28.497399`      | PocketMiner preprint | (bioRxiv preprint of the above)                                                                                   | bioRxiv, 2022                      | `[VERIFIED-FULLTEXT]` |
| `10.1093/bioinformatics/btae745` | CryptoBench          | CryptoBench: cryptic protein–ligand binding sites dataset and benchmark                                           | Bioinformatics 41(1):btae745, 2025 | `[VERIFIED-FULLTEXT]` |
| `10.1016/j.cbpa.2018.05.003`     | Vajda et al. 2018    | Cryptic binding sites on proteins: definition, detection, and druggability                                        | Curr Opin Chem Biol 44:1–8, 2018   | `[VERIFIED-FULLTEXT]` |
| `10.1093/bioadv/vbaf156`         | Gašparíková et al.   | Recent computational advances in the identification of cryptic binding sites for drug discovery                   | Bioinform Adv 5(1):vbaf156, 2025   | `[VERIFIED-FULLTEXT]` |
| `10.1073/pnas.1711490115`        | Beglov et al.        | Exploring the structural origins of cryptic sites on proteins                                                     | PNAS, 2018                         | **unreachable (403)** |

### 10.4 Benchmarks, datasets and independent evaluations

| DOI                                 | Short name          | Title                                                                                                                      | Venue, year                           | Tag                                                 |
| ----------------------------------- | ------------------- | -------------------------------------------------------------------------------------------------------------------------- | ------------------------------------- | --------------------------------------------------- |
| `10.1093/bioinformatics/btv169`     | ASBench             | ASBench: benchmarking sets for allosteric discovery                                                                        | Bioinformatics 31(15):2598–2600, 2015 | `[VERIFIED-FULLTEXT]`; **host unreachable**         |
| `10.32607/20758251-2019-11-1-74-80` | CASBench            | CASBench: a benchmarking set of proteins with annotated catalytic and allosteric sites in their structures                 | Acta Naturae 11(1):74–80, 2019        | `[VERIFIED-FULLTEXT]`                               |
| `10.1093/nar/gkv902`                | ASD v3.0            | ASD v3.0: unravelling allosteric regulation with structural mechanisms and biological networks                             | Nucleic Acids Res 44:D527, 2016       | `[VERIFIED-FULLTEXT]`; **host unreachable**         |
| `10.1093/nar/gkad915`               | ASD2023             | ASD2023: towards the integrating landscapes of allosteric knowledgebase                                                    | Nucleic Acids Res 52:D376, 2024       | `[VERIFIED-FULLTEXT]`; **host unreachable**         |
| `10.1021/acsomega.5c01263`          | AlloBench           | AlloBench: A Data Set Pipeline for the Development and Benchmarking of Allosteric Site Prediction Tools                    | ACS Omega 10(17):17973–17982, 2025    | `[VERIFIED-FULLTEXT]`                               |
| `10.1007/s10822-026-00831-4`        | CAPASP              | A systematic evaluation of protein allosteric site prediction tools with independent datasets                              | J Comput Aided Mol Des, 2026          | `[VERIFIED-ABSTRACT]`; **per-tool numbers unknown** |
| `10.1016/j.jmb.2015.09.001`         | AlloRep             | AlloRep: a repository of sequence, structural and mutagenesis data for the LacI/GalR transcription regulators              | J Mol Biol, 2015                      | `[UNVERIFIED]` — DOI unverified                     |
| `10.1021/jm300687e`                 | DUD-E               | Directory of Useful Decoys, Enhanced (DUD-E): better ligands and decoys for better benchmarking                            | J Med Chem 55(14):6582, 2012          | `[UNVERIFIED]`                                      |
| `10.1021/ci200266d`                 | DrugPred / NRDLD    | Structure-Based Predictions of Activity Cliffs / druggability prediction with a non-redundant druggable/less-druggable set | J Chem Inf Model 51(11):2829, 2011    | `[UNVERIFIED]`                                      |
| `10.1038/s41598-023-29996-w`        | Binding MOAD sunset | Sunsetting Binding MOAD with its last data update                                                                          | Sci Rep, 2023                         | `[UNVERIFIED]`                                      |
| —                                   | sc-PDB              | sc-PDB: a 3D-database of ligandable binding sites — 10 years on                                                            | Nucleic Acids Res 43:D465, 2015       | **DOI unknown**; server refuses connections         |

### 10.5 Ligand-binding-site prediction — where the hit criteria come from

| DOI                             | Short name         | Title                                                                                                                               | Venue, year                             | Tag                                                                               |
| ------------------------------- | ------------------ | ----------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------- | --------------------------------------------------------------------------------- |
| `10.1023/A:1008124202956`       | PASS               | Fast prediction and visualization of protein binding pockets with PASS                                                              | J Comput Aided Mol Des 14:383–401, 2000 | `[VERIFIED-FULLTEXT]` — **the true primary for the 4 Å criterion**                |
| `10.1093/bioinformatics/bti315` | Q-SiteFinder       | Q-SiteFinder: an energy-based method for the prediction of protein–ligand binding sites                                             | Bioinformatics 21:1908–1916, 2005       | `[VERIFIED-FULLTEXT]` — **states no 4 Å criterion**                               |
| `10.1186/1472-6807-6-19`        | LIGSITEcsc         | LIGSITEcsc: predicting ligand binding sites using the Connolly surface and degree of conservation                                   | BMC Struct Biol 6:19, 2006              | `[VERIFIED-FULLTEXT]` — misattributes the 4 Å criterion                           |
| `10.1186/1752-153X-1-7`         | PocketPicker       | PocketPicker: analysis of ligand binding-sites with shape descriptors                                                               | Chem Cent J 1:7, 2007                   | `[VERIFIED-FULLTEXT]`                                                             |
| `10.1186/1471-2105-10-168`      | fpocket            | Fpocket: an open source platform for ligand pocket detection                                                                        | BMC Bioinformatics 10:168, 2009         | `[VERIFIED-FULLTEXT]`                                                             |
| `10.1093/bioinformatics/btq543` | BDT                | The binding site distance test score: a robust method for the assessment of predicted protein binding sites                         | Bioinformatics 26(22):2920–2921, 2010   | `[VERIFIED-FULLTEXT, resolved at merge]` — Roche DB, **Tetchner SJ**, McGuffin LJ |
| `10.1016/j.str.2011.02.015`     | Chen et al. 2011   | A critical comparative assessment of predictions of protein-binding sites for biologically relevant organic compounds               | Structure 19:613–621, 2011              | **paywalled, no PMCID**                                                           |
| `10.1002/prot.24495`            | CASP10 assessment  | Assessment of ligand binding site predictions in CASP10                                                                             | Proteins 82(S2):154–163, 2014           | `[VERIFIED-FULLTEXT]`                                                             |
| `10.1093/bioinformatics/btt447` | COACH              | Protein-ligand binding site recognition using complementary binding-specific substructure comparison and sequence profile alignment | Bioinformatics 29:2588–2595, 2013       | `[VERIFIED-FULLTEXT]`                                                             |
| `10.1093/bioinformatics/btx350` | DeepSite           | DeepSite: protein-binding site predictor using 3D-convolutional neural networks                                                     | Bioinformatics 33:3036–3042, 2017       | `[VERIFIED-FULLTEXT]` — **DVO's origin**                                          |
| `10.1186/s13321-018-0285-8`     | P2Rank             | P2Rank: machine learning based tool for rapid and accurate prediction of ligand binding sites from protein structure                | J Cheminform 10:39, 2018                | `[VERIFIED-FULLTEXT]`; exact DCA/DCC sentences `[UNVERIFIED]`                     |
| `10.1038/s41598-020-61860-z`    | Kalasanty          | Improving detection of protein-ligand binding sites with 3D segmentation                                                            | Sci Rep 10:5035, 2020                   | `[VERIFIED-FULLTEXT]`                                                             |
| `10.1186/s13321-021-00547-7`    | PUResNet           | PUResNet: prediction of protein-ligand binding sites using deep residual neural network                                             | J Cheminform 13:65, 2021                | `[VERIFIED-FULLTEXT]`                                                             |
| `10.1186/s13321-024-00923-z`    | LIGYSIS-bench      | Comparative evaluation of methods for the prediction of protein–ligand binding sites                                                | J Cheminform 16:126, 2024               | `[VERIFIED-FULLTEXT]`                                                             |
| `10.1021/acs.jcim.5c00336`      | Membrane benchmark | (benchmark of binding-site prediction on membrane proteins)                                                                         | J Chem Inf Model, 2025                  | `[VERIFIED-FULLTEXT]`                                                             |
| `10.1021/acs.jctc.2c01306`      | SiteFerret         | SiteFerret: beyond simple pocket identification in proteins (arXiv:2212.11888)                                                      | J Chem Theory Comput 19(15):5242, 2023  | `[VERIFIED-FULLTEXT]`                                                             |
| `10.1093/bioinformatics/bts310` | DoGSiteScorer      | DoGSiteScorer: a web server for automatic binding site prediction, analysis and druggability assessment                             | Bioinformatics 28(15):2074–2075, 2012   | `[VERIFIED-ABSTRACT]`; thresholds `[UNVERIFIED]`                                  |

### 10.6 Metric theory, statistics and null models

| DOI                              | Short name                     | Title                                                                                                                                       | Venue, year                              | Tag                                                      |
| -------------------------------- | ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------- | -------------------------------------------------------- |
| `10.1145/1143844.1143874`        | Davis & Goadrich               | The Relationship between Precision-Recall and ROC Curves                                                                                    | ICML '06, pp. 233–240, 2006              | `[VERIFIED-ABSTRACT]`                                    |
| `10.1371/journal.pone.0118432`   | Saito & Rehmsmeier             | The Precision-Recall Plot Is More Informative than the ROC Plot When Evaluating Binary Classifiers on Imbalanced Datasets                   | PLoS ONE 10(3):e0118432, 2015            | `[VERIFIED-FULLTEXT]`                                    |
| arXiv:2401.06091                 | McDermott et al.               | A Closer Look at AUROC and AUPRC under Class Imbalance                                                                                      | NeurIPS 2024                             | `[VERIFIED-FULLTEXT]`                                    |
| `10.1093/bioinformatics/btaa573` | Zhang, Ghadermarzi & Kurgan    | Prediction of protein-binding residues: dichotomy of sequence-based methods developed using structured complexes versus disordered proteins | Bioinformatics 36(18):4729–4738, 2020    | `[VERIFIED-FULLTEXT]` — **AULC's origin**                |
| `10.1186/s13040-023-00322-4`     | Chicco & Jurman 2023           | The Matthews correlation coefficient (MCC) should replace the ROC AUC as the standard metric                                                | BioData Min, 2023                        | `[VERIFIED-ABSTRACT]`                                    |
| `10.1186/s13040-021-00244-z`     | Chicco et al. 2021             | The Matthews correlation coefficient (MCC) is more reliable than balanced accuracy                                                          | BioData Min, 2021                        | `[VERIFIED-ABSTRACT]`                                    |
| `10.1021/ci600426e`              | Truchon & Bayly                | Evaluating Virtual Screening Methods: Good and Bad Metrics for the "Early Recognition" Problem                                              | J Chem Inf Model 47(2):488–508, 2007     | **unreachable**; constants `[UNVERIFIED]`                |
| `10.3389/fchem.2019.00701`       | Front Chem 2019                | Teaching an Old Dog New Tricks: (the α = 20 attribution)                                                                                    | Front Chem 7:701, 2019                   | `[VERIFIED-FULLTEXT]`                                    |
| `10.1073/pnas.2414333121`        | PNAS hinge sites               | Global hinge sites of proteins as target sites for drug binding                                                                             | PNAS 121, 2024                           | `[VERIFIED-FULLTEXT]` — **the hypergeometric precedent** |
| `10.1186/1471-2105-11-286`       | Guharoy & Chakrabarti          | Conserved residue clusters at protein-protein interfaces and their use in binding site identification                                       | BMC Bioinformatics 11:286, 2010          | `[VERIFIED-FULLTEXT, resolved at merge]`                 |
| `10.1371/journal.pone.0005967`   | Milenkovic, Filippis, Lappe & Przulj | Optimized null model for protein structure networks                                                                                         | PLoS ONE, 2009                           | `[VERIFIED-FULLTEXT]`                                    |
| `10.1371/journal.pone.0188616`   | Thayer et al.                  | Dependence of prevalence of contiguous pathways in proteins on structural complexity                                                        | PLoS One 12(12):e0188616, 2017           | `[VERIFIED-FULLTEXT]`                                    |
| `10.1515/sagmb-2015-0057`        | Kovačev-Nikolić et al.         | Using persistent homology and dynamical distances to analyze protein binding                                                                | Stat Appl Genet Mol Biol, 2016           | `[UNVERIFIED]`                                           |
| `10.1007/s00239-008-9183-4`      | Marsh 2009                     | Spatial autocorrelation of amino acid replacement rates in the vasopressin receptor family                                                  | J Mol Evol, 2009                         | `[VERIFIED-ABSTRACT]`                                    |
| —                                | Burt et al. 2020               | Generative modeling of brain maps with spatial autocorrelation                                                                              | NeuroImage, 2020                         | **DOI unverified**                                       |
| —                                | Webber, Moffat & Zobel         | A Similarity Measure for Indefinite Rankings (RBO)                                                                                          | ACM TOIS 28(4), 2010                     | **DOI unverified**                                       |
| —                                | Marques & Sanejouand 1995      | (mode overlap)                                                                                                                              | Proteins 23:557–560, 1995                | **DOI unverified, not fetched**                          |
| —                                | Kurkcuoglu, Jernigan & Doruker | Mixed levels of coarse-graining of large proteins using elastic network model succeeds in extracting the slowest motions                    | Polymer 45, 2004                         | **DOI unverified**                                       |
| —                                | Sheridan et al. 2001           | (RIE, as attributed by the RDKit implementation)                                                                                            | J Chem Inf Comput Sci 41:1395–1406, 2001 | **DOI unverified**                                       |

### 10.7 Allostery theory, pharma and reporting standards

| DOI                                  | Short name            | Title                                                                                                 | Venue, year                                      | Tag                                                           |
| ------------------------------------ | --------------------- | ----------------------------------------------------------------------------------------------------- | ------------------------------------------------ | ------------------------------------------------------------- |
| `10.1038/nature13001`                | Motlagh et al.        | The ensemble nature of allostery                                                                      | Nature 508(7496):331–339, 2014                   | `[VERIFIED-FULLTEXT]`                                         |
| `10.1371/journal.pcbi.1003394`       | Tsai & Nussinov       | A Unified View of "How Allostery Works"                                                               | PLoS Comput Biol 10(2):e1003394, 2014            | `[VERIFIED-FULLTEXT]`                                         |
| `10.1016/j.cell.2013.03.034`         | Nussinov & Tsai 2013  | Allostery in disease and in drug discovery                                                            | Cell 153:293–305, 2013                           | `[UNVERIFIED]` — abstract elided by publisher                 |
| `10.1016/j.tips.2014.03.006`         | Nussinov & Tsai 2014  | Unravelling structural mechanisms of allosteric drug action                                           | Trends Pharmacol Sci 35(5):256–264, 2014         | `[UNVERIFIED]`                                                |
| `10.1016/j.str.2019.01.003`          | Wodak et al.          | Allostery in Its Many Disguises: From Theory to Applications                                          | Structure, 2019                                  | **not readable (PDF with no text layer)**                     |
| `10.1002/med.21317`                  | Lu, Li & Zhang        | Recent computational advances in the identification of allosteric sites in proteins                   | Med Res Rev, 2014                                | `[UNVERIFIED]` — closed access                                |
| `10.1016/j.drudis.2025.104466`       | Huang et al. 2025     | Recent advances in computational strategies for allosteric site prediction                            | Drug Discov Today 30(10):104466, 2025            | `[VERIFIED-ABSTRACT]`                                         |
| `10.1016/j.sbi.2020.08.004`          | Krojer et al.         | Discovery of allosteric binding sites by crystallographic fragment screening                          | Curr Opin Struct Biol 65:209–216, 2020           | `[VERIFIED-FULLTEXT]`                                         |
| `10.1021/acs.jmedchem.5b00586`       | Kozakov et al.        | New Frontiers in Druggability                                                                         | J Med Chem 58(23):9063–9088, 2015                | `[VERIFIED-FULLTEXT]`                                         |
| `10.1021/ci800324m`                  | Halgren 2009          | Identifying and characterizing binding sites and assessing druggability                               | J Chem Inf Model 49(2):377–389, 2009             | `[VERIFIED-ABSTRACT]` — metadata only; **thresholds unknown** |
| `10.1021/jm100574m`                  | Schmidtke & Barril    | Understanding and Predicting Druggability                                                             | J Med Chem 53(15):5858–5867, 2010                | `[VERIFIED-ABSTRACT]` — metadata only                         |
| `10.1371/journal.pone.0010109`       | Huang & Jacobson      | Binding-site assessment by virtual fragment screening                                                 | PLoS ONE 5(4):e10109, 2010                       | `[UNVERIFIED]`                                                |
| `10.1021/acschembio.2c00234`         | Kampen et al.         | Structure-Based Discovery of Negative Allosteric Modulators of mGlu5                                  | ACS Chem Biol 17(10):2744–2752, 2022             | `[VERIFIED-FULLTEXT]`                                         |
| `10.1038/s42003-024-05970-8`         | Utgés et al. 2024     | Classification of likely functional class for ligand binding sites identified from fragment screening | Commun Biol 7:320, 2024                          | `[VERIFIED-FULLTEXT]`                                         |
| `10.1073/pnas.1518946112`            | Ludlow et al.         | Detection of secondary binding sites in proteins using fragment screening                             | PNAS, 2015                                       | **unreachable (403)**                                         |
| `10.1038/nrd4309`                    | Cook et al.           | Lessons learned from the fate of AstraZeneca's drug pipeline: a five-dimensional framework            | Nat Rev Drug Discov 13:419–431, 2014             | `[UNVERIFIED]`                                                |
| `10.1021/acs.jcim.5c00331`           | Chen & Zhang          | Can Deep Learning Blind Docking Methods be Used to Predict Allosteric Compounds?                      | J Chem Inf Model 65(7):3737–3748, 2025           | `[VERIFIED-FULLTEXT]`                                         |
| `10.1371/journal.pcbi.1013094`       | Wankowicz 2025        | Ten rules for a structural bioinformatic analysis                                                     | PLoS Comput Biol 21(10):e1013094, 2025           | `[VERIFIED-FULLTEXT]`                                         |
| `10.1038/s41592-021-01205-4`         | DOME                  | DOME: recommendations for supervised machine learning validation in biology                           | Nat Methods 18:1122–1127, 2021                   | `[UNVERIFIED]`                                                |
| `10.7554/eLife.34711`                | NMDAR PAM/NAM series  | (PAM/NAM interconversion at a shared site)                                                            | eLife, 2018                                      | `[UNVERIFIED]`                                                |
| bioRxiv `10.64898/2026.01.05.697819` | 2026 kinase pLM study | Protein language models and structure-based ML for allosteric binding sites in kinases                | J Chem Theory Comput 22(10):5326 / bioRxiv, 2026 | `[UNVERIFIED]`                                                |

### 10.8 Software releases cited as evidence

| Item                          | Version and date      | Licence | Source                                    | Tag                                                                     |
| ----------------------------- | --------------------- | ------- | ----------------------------------------- | ----------------------------------------------------------------------- |
| fpocket                       | **4.2.3**, 2026-03-09 | MIT     | GitHub releases API                       | `[VERIFIED-FULLTEXT]`                                                   |
| P2Rank                        | **2.5.1**, 2025-08-07 | —       | GitHub releases API                       | `[VERIFIED-FULLTEXT]`                                                   |
| RDKit `ML/Scoring/Scoring.py` | —                     | BSD     | raw.githubusercontent.com                 | `[VERIFIED-FULLTEXT]` — source of the BEDROC/RIE/EF formulas used in §1 |
| allobench                     | —                     | MIT     | GitHub                                    | `[VERIFIED-FULLTEXT]`                                                   |
| CryptoBench                   | —                     | MIT     | GitHub; OSF `osf.io/pz4a9/` is a JS shell | `[VERIFIED-FULLTEXT]`                                                   |

### 10.9 Source documents merged into this file

| File                         | Date       | Scope                                                                                   |
| ---------------------------- | ---------- | --------------------------------------------------------------------------------------- |
| `evaluation-protocol-lit.md` | 2026-08-20 | The earlier, narrower review. Confirmed, extended and contradicted as marked throughout |
| lit-A-metrics.md             | 2026-08-24 | Metrics used in allosteric-site prediction                                              |
| lit-B-negatives.md           | 2026-08-24 | Benchmarks, negative classes, decoys, statistical procedures                            |
| lit-C-hitcriteria.md         | 2026-08-25 | Hit criteria and top-N conventions                                                      |
| lit-D-network.md             | 2026-08-24 | How network and dynamics methods validate themselves                                    |
| lit-E-strata.md              | 2026-08-24 | Biology and pharma stratification factors                                               |

Reports A–E were working files in a session scratchpad and are not committed. Their content is
merged here in full for every claim that carries a DOI or an explicit unknown; their
recommendation sections are deliberately **not** merged, because this file is evidence and
decisions live in `docs/benchmark/evaluation/` (`README.md` and `manifest.yaml`) and in
`docs/adr/`.
