# Fact-check of `07-metrics-audit.md`

**Date: 2026-09-02. Scope: the NEW citations and NEW numbers introduced by
`07-metrics-audit.md`. Every source below was fetched this session. Nothing here is
confirmed from memory.**

Why this file exists: `07-metrics-audit.md` recommends changes to a frozen evaluation
protocol. R3 says a recalled number is not evidence. Four of its recommendations
(items 3, 4, 6 and 9 of its "What must change" list) rest on citations that did not exist
in the evidence base. Those citations are checked here before they drive an edit.

**Headline.** The audit's load-bearing claim — the one that reverses README §12.4 — is
**correct in every digit**. Two smaller defects are real and must not be copied into the
repo: the audit misattributes what Allo-Allo's Bonferroni correction was applied to, and
it presents a non-verbatim sentence as a verbatim Seq2Pocket quote. One arithmetic
shorthand (`max MCC ≈ sqrt(5/m)`) overstates the true ceiling and should be replaced with
the exact form the audit itself derives two paragraphs earlier.

---

## Verdict table

|   # | Claim under check                                                     | Verdict                 | What is wrong, if anything                                                                                   |
| --: | --------------------------------------------------------------------- | ----------------------- | ------------------------------------------------------------------------------------------------------------ |
|   1 | doi:10.1162/IMAG.a.71 and its five FPR numbers                        | **CONFIRMED**           | All five digits exact. One presentational caveat: the audit's two table columns are not matched on α         |
|   2 | doi:10.64898/2026.01.28.702257 is Seq2Pocket, source of the PFI       | **PARTIALLY CONFIRMED** | DOI, paper, PFI and 12 Å DCC all real. One quoted-as-verbatim sentence is not the paper's wording            |
|   3 | doi:10.1007/s10822-026-00831-4 is CAPASP, five evaluation dimensions  | **CONFIRMED**           | —                                                                                                            |
|   4 | doi:10.48550/arXiv.2506.03237 is UniSite with an AP@IoU metric        | **CONFIRMED**           | —                                                                                                            |
|   5 | doi:10.1162/imag.a.118 is the spin-distortion paper with a screen fix | **CONFIRMED**           | "Screen-and-discard post-stratification" is the audit's own gloss, correctly marked as such                  |
|   6 | "Allo-Allo applies Bonferroni"                                        | **PARTIALLY CONFIRMED** | The Bonferroni is real. It adjusts the **attention-head selection** t-tests, **not** the AlphaMissense check |
|   7 | "8 of 10 papers I read at source state no significance test"          | **CONFIRMED**           | Substance holds on four spot-checks. The prose says "nine papers" above a ten-row table                      |
|   8 | Derived ceilings: F1 = 10/(m+5), MCC ≈ sqrt(5/m), Jaccard = 5/m       | **PARTIALLY CONFIRMED** | F1 and Jaccard are exact. The MCC shorthand overstates the ceiling by 0.5–4.1 % on the five primary arms     |
|   9 | "CASP has dropped the category"                                       | **CONFIRMED**           | Last edition was **CASP10**. The audit's own `[NOT ESTABLISHED]` flag on retirement can now be **closed**    |
|  10 | Eight further "Retrieved this session" DOIs                           | **CONFIRMED**           | One year error: doi:10.1002/advs.202513641 is **2025**, not 2026                                             |
|  11 | (found in passing) Census row 35: Allo-Allo "AUROC 0.95"              | **REFUTED**             | 0.95 is an Appendix-A **baseline** AUROC, not Allo-Allo's own                                                |

---

## 1. doi:10.1162/IMAG.a.71 — eigenstrapping. CONFIRMED.

**Verdict: CONFIRMED.** DOI resolves, journal and authors match, and all five numbers
appear in the published paper with the meaning the audit gives them.

**Metadata** (Crossref record, `api.crossref.org/works/10.1162/IMAG.a.71`):

- Title: "Generation of surrogate brain maps preserving spatial autocorrelation through
  random rotation of geometric eigenmodes"
- Authors: Nikitas C. Koussis, James C. Pang, Richa Phogat, Jayson Jeganathan, Bryan Paton,
  Alex Fornito, P.A. Robinson, Bratislav Misic, Michael Breakspear
- _Imaging Neuroscience_ 3, 2025, MIT Press. PMID 40800970, PMCID PMC12330862, open access.

Every field matches the audit's citation exactly.

**The five numbers.** Read at `https://pmc.ncbi.nlm.nih.gov/articles/PMC12330862/`. All
three quotations below are verbatim from the published version.

> "Eigenstrapping yields an FPR near or below the expected 5% for α = 0.0–2.5, with 5.3%
> (α = 0.0), 2.1% (α = 0.5), 3.5% (α = 1.0), 5.6% (α = 1.5), 5.0% (α = 2.0), 5.2%
> (α = 2.5), and 5.2% (α = 3.0)."

> "the Spin Test yields higher than expected FPR across all SA regimes, ranging from 5.7%
> at α = 0.0, increasing to 6.8% (α = 1.0), 7.4% (α = 2.0), to a maximum of 12.3%
> (α = 3.0)."

> "The BrainSMASH method shows higher FPR than both the Spin Test and eigenstrapping,
> reaching 29.2% at α = 2.0 and 36.3% at α = 3.0."

So: 29.2 % ✓, 36.3 % ✓, 12.3 % ✓, 5.2 % ✓, 5.3 % ✓. All five carry the meaning the audit
assigns. The two characterisation quotes are also verbatim: "eschews the need for
parametric assumptions about the nature of a map's SA" and "eigenstrapping only having one
free parameter (the number of modes used for decomposition)".

**Measurement conditions, which the audit does not state.** The FPRs come from simulated
Gaussian random fields on a cortical surface, Figure 3, nominal test level 5 %. α is the
smoothness parameter of the simulated field, from α = 0.0 (no autocorrelation) to α = 3.0
(high). The endpoint is a map-to-map correlation, not a set-enrichment test.

**One caveat on the audit's table, and it is presentational only.** The audit prints two
columns, "FPR at low autocorrelation" and "FPR at high autocorrelation", and the columns
are not matched on α. Eigenstrapping's 5.3 % is at α = 0.0; BrainSMASH's 29.2 % is at
α = 2.0. The audit also leaves the spin test's low-SA cell blank, which hides that the spin
test is already above nominal at α = 0.0 (5.7 %). The α-matched head-to-head at α = 3.0 is
cleaner and supports the same conclusion more directly:

| Null           | FPR at α = 3.0 |
| -------------- | -------------: |
| Eigenstrapping |          5.2 % |
| Spin test      |         12.3 % |
| BrainSMASH     |         36.3 % |

**Correction to make when README §12.4 is rewritten:** print the α-matched row, not the
mixed-α table.

**A trap that this check caught.** The bioRxiv v2 preprint
(doi:10.1101/2024.02.07.579070) reports **different** numbers: eigenstrapping "12.3%
(α = 3.5)", BrainSMASH "29.2% at α = 2.0 and 38.4% at α = 4.0", and no per-α spin-test
figures. Under the preprint, 12.3 % belongs to **eigenstrapping**, not the spin test, and
36.3 % does not appear. The numbers were revised between preprint and publication. Anyone
re-checking this must use the published version. Citing the preprint would produce a
verdict of REFUTED on the same claim.

**Bottom line.** Recommendation 4 of the audit stands. Variogram-matched surrogates
(BrainSMASH) measure worse than the spin test at every autocorrelation level tested, and
README §12.4's "the right design" is refuted by the source the audit names. The
`[NOT ESTABLISHED]` caveat the audit attaches — no protein-contact-graph demonstration
exists — remains correct and must travel with the citation.

---

## 2. doi:10.64898/2026.01.28.702257 — Seq2Pocket. PARTIALLY CONFIRMED.

**Verdict: PARTIALLY CONFIRMED.** The DOI resolves, the paper is Seq2Pocket, and the
Pocket Fragmentation Index is real and defined as the audit says. One sentence the audit
presents as verbatim is not the paper's wording.

**The prefix is not an error.** `10.64898` is the current DOI prefix for bioRxiv
preprints. Crossref returns publisher **openRxiv** and resource URL
`http://biorxiv.org/lookup/doi/10.64898/2026.01.28.702257`. A second, unrelated 2026
bioRxiv preprint surfaced during search under the same prefix
(`10.64898/2026.03.08.710410`), which corroborates it. bioRxiv moved from `10.1101` to
`10.64898` under openRxiv; both prefixes are live.

**Metadata** (Crossref):

- Title: "Seq2Pocket: Augmenting protein language models for spatially consistent binding
  site prediction"
- Authors: Vít Škrhák, Lukáš Polák, Marian Novotný, David Hoksza
- Preprint, posted 2026-01-31, openRxiv / bioRxiv.
- Canonical link: <https://www.biorxiv.org/content/10.64898/2026.01.28.702257v1>

**PFI: CONFIRMED.** Read at
`https://www.biorxiv.org/content/10.64898/2026.01.28.702257v1.full`. The paper states that
PFI "measures the average number of predicted clusters assigned to each ground-truth
pocket", and that "an ideal clustering strategy achieves a one-to-one mapping, resulting in
a PFI of 1.0". Both fragments the audit quotes are the paper's.

**DCC at 12 Å: CONFIRMED.** Verbatim: "We define a successful prediction as a 'hit' if the
DCC is below a 12 Å threshold [51]." Reference [51] is "Javier Utgés and Geoffrey Barton.
Comparative evaluation of methods for the prediction of protein–ligand binding sites.
Journal of Cheminformatics, 16, 11 2024" — that is doi:10.1186/s13321-024-00923-z, the
paper the audit names. The audit's second-independent-group argument holds.

**The defect. The "incomplete pockets" quote is not verbatim.** The audit §1.2 writes:

> protein language models produce "incomplete pockets: residue-wise predictions that often
> achieve high statistical scores but fail to form continuous binding regions"

The paper says:

> "In this study, we address the tendency of pLMs to produce what we define as **incomplete
> pockets**: residue-wise predictions that fail to form full, continuous binding regions"

The clause "often achieve high statistical scores but" does not appear. The word "full" was
dropped. The phrase "high statistical scores" does not occur anywhere in the paper. The
audit also quotes "while residue-level metrics might look promising... the pocket-level
metrics could be disappointing"; the paper's wording uses "mappings", not "metrics", in the
first clause. The audit's substantive point survives — the paper is explicitly about
residue-level success not implying pocket-level success, and it makes that point with a
worked example ("if a protein has three distinct binding pockets and a predictor only finds
the largest one, its pocket-level recall is only 33%, even if its residue-level scores are
high") — but the quotation marks are not earned.

**Correction.** If recommendation 6 is adopted, cite the PFI definition and the worked
example. Do not carry the "incomplete pockets" sentence as a quotation in its audit form.

---

## 3. doi:10.1007/s10822-026-00831-4 — CAPASP. CONFIRMED.

**Verdict: CONFIRMED.** Every element checks out.

**Metadata** (Crossref plus Europe PMC record, PMID 42126486):

- Title: "A systematic evaluation of protein allosteric site prediction tools with
  independent datasets"
- Authors: Yuanbao Ai, Haixiao Li, Xuemei Huang, Sen Liu
- _Journal of Computer-Aided Molecular Design_ 40(1):122, 2026. Springer.
- Crossref publication date 2026-05-13.

The audit's citation "Ai Y, Li H, Huang X, Liu S. _J Comput Aided Mol Des_ 40(1):122, 2026"
is exact.

**The five dimensions: CONFIRMED, verbatim from the abstract.**

> "We then systematically evaluated the accuracy of five allosteric site prediction tools
> across five dimensions: sensitivity, specificity, F1-score, MCC value and ranking
> capability."

The audit's other two abstract quotes are also verbatim:

> "a CAPASP-General subset comprising holo state allosteric proteins and a CAPASP-Unbound
> subset comprising apo state allosteric proteins"

> "However, these models performed better with the CAPASP-General subset than with the
> CAPASP-Unbound subset"

And the PASSer/APOP lead: "the machine learning models PASSer and APOP, which are based on
protein physicochemical properties, not only achieved the highest success rate in
sensitivity prediction but also lead in average F1-score and MCC value."

The audit's `[NOT ESTABLISHED]` on per-tool numbers and dataset sizes is not disturbed;
the abstract carries none, and the full text sits behind the Springer paywall. Not
attempted here, because the audit already discloses it.

---

## 4. doi:10.48550/arXiv.2506.03237 — UniSite. CONFIRMED.

**Verdict: CONFIRMED.**

Read at <https://arxiv.org/abs/2506.03237>.

- Title: "UniSite: The First Cross-Structure Dataset and Learning Framework for End-to-End
  Ligand Binding Site Detection"
- Authors: Jigang Fan, Quanlin Wu, Shengjie Luo, Liwei Wang
- Submitted 3 June 2025. NeurIPS 2025, Spotlight.

**The metric: CONFIRMED, verbatim from the abstract.**

> "In addition, we introduce Average Precision based on Intersection over Union (IoU) as a
> more accurate evaluation metric for ligand binding site prediction."

The abstract also states the metric critique the audit relies on:

> "(3) traditional evaluation metrics do not adequately reflect the actual performance of
> different binding site prediction methods."

The audit's three block quotes in §1.3 (the 20 % double-counting figure, the ground-truth
DCC/DCA deviation, and "They completely disregard the structural properties such as shape,
size, and residue composition of binding sites") come from the body, not the abstract, and
were not individually re-checked here. The metric claim — which is what recommendations 5
and the §3.3 Jaccard argument depend on — is confirmed at the abstract.

**Note for the repo's own use.** UniSite's IoU is over **residue masks**, and it is scored
with one-to-one bijective matching between predicted and ground-truth sites. The audit's
observation that "residue-mask IoU is Jaccard" is correct, and so is its reason for why the
repo's decline still survives at fixed k = 5.

---

## 5. doi:10.1162/imag.a.118 — spherical-projection distortion. CONFIRMED.

**Verdict: CONFIRMED.**

**Metadata** (Crossref plus Europe PMC, PMID 40860578, PMCID PMC12371478, open access):

- Title: "The effect of spherical projection on spin tests for brain maps"
- Authors: Vincent Bazinet, Zhen-Qi Liu, Bratislav Misic
- _Imaging Neuroscience_ 3, 2025, MIT Press.

Exact match to the audit's citation.

**The method: CONFIRMED, verbatim from the abstract.**

> "Here we show that a key component of the procedure—projecting brain maps to a spherical
> surface—distorts distance relationships between vertices. These distortions result in
> surrogate maps that imperfectly preserve spatial autocorrelation, yielding inflated false
> positive rates. We then confirm that targeted removal of individual spins with high
> distortion reduces false positive rates."

Every clause the audit attributes to this paper is in that passage: distance distortion,
imperfect autocorrelation preservation, inflated FPR, and the remedy of removing individual
high-distortion spins.

**One label to keep straight.** "Screen-and-discard post-stratification" is the audit's own
term, not the paper's. The paper says "targeted removal of individual spins with high
distortion". The audit marks the gloss as its own, so this is correct as written. Keep the
gloss and the paper's phrase together in any README text, so a reader can find the source.

---

## 6. "Allo-Allo applies Bonferroni". PARTIALLY CONFIRMED.

**Verdict: PARTIALLY CONFIRMED. The correction the audit asks the repo to make is right.
The reason it gives for it is wrong, and must not be copied.**

**Paper identity: CONFIRMED.** Europe PMC record for doi:10.1101/2024.09.28.615583:
"Allo-Allo: Data-efficient prediction of allosteric sites", Tianze Dong, Christopher Kan,
Kapil Devkota, Rohit Singh, bioRxiv 2024, PPR917773.
Full text read at <https://www.biorxiv.org/content/10.1101/2024.09.28.615583v1.full>.

**Bonferroni exists: CONFIRMED.** Verbatim:

> "Bonferroni correction was applied to adjust the _p_-values for multiple hypothesis
> testing."

So `evaluation-metrics.md` §3.5's "**0** apply any multiplicity correction. Not one." **is**
false as literally worded, and the audit is right that it must change.

**What the audit gets wrong.** The audit says, in three separate places (headline §4.1
table, census row 35, and recommendation 9a), that this is a "Welch's t-test with
Bonferroni on a downstream AlphaMissense validation". It is not. The Bonferroni sentence
sits under the section heading **"Selecting attention heads with highest allosteric
sensitivity"**, in this paragraph:

> "In the second step, we applied the Student's t-test to each _P_ℓ,h set, with the null
> hypothesis implying a µ0 equal to the average _p_-score across all training samples and
> attention heads. Bonferroni correction was applied to adjust the _p_-values for multiple
> hypothesis testing. Finally, the attention heads that rejected the null hypothesis were
> ranked based on their Signal-to-Noise Ratios (SNRs)..."

That is a **Student's** t-test used for **feature selection inside model construction**. It
is not Welch's, and it has nothing to do with AlphaMissense.

The AlphaMissense analysis is a separate, later section, and it uses Welch's t-test with
**no** Bonferroni:

> "We marked Allo-Allo predictions above the 99-th percentile as positive, the rest as
> negative, and compared the distribution of AlphaMissense risk-scores between the two
> sets. Through a Welch's t-test, we found that the Allo-Allo predictions had significantly
> higher scores in the average (_t_ = 9.46), max (_t_ = 9.01), and weighted risk-score
> (_t_ = 8.86); _p_ < 10⁻⁵ in all cases."

The word "Bonferroni" does not appear in that section.

**Effect on the audit's conclusion: it strengthens it.** The audit's proposed restatement —
"no paper applies a multiplicity correction to a performance claim" — is not merely
preserved but improved. Allo-Allo's Bonferroni protects a **model-building** step, which is
further from a performance claim than a downstream validation is.

**Corrections required before recommendation 9a is applied.**

- `07-metrics-audit.md` §4.1 table, Allo-Allo row: replace "Welch's t-test with Bonferroni
  on a downstream AlphaMissense validation" with "No test on performance. Bonferroni on the
  attention-head selection t-tests (model construction); an uncorrected Welch's t-test on a
  downstream AlphaMissense validation."
- §2.1 census row 35: same replacement.
- Recommendation 9a: the replacement text for `evaluation-metrics.md` must say Allo-Allo
  applies Bonferroni to **attention-head selection**, not to a downstream validation.

---

## 7. "8 of 10 papers I read at source state no significance test". CONFIRMED.

**Verdict: CONFIRMED on the substance. One internal inconsistency in the file.**

**The ten papers.** Section 4.1's table names, in order: AlloPred (2015), PocketMiner
(2023), APOP (2023), Allo-Allo (2024), CryptoBench (2025), DeepAllo (2025), STINGAllo
(2025), Allo-PED (2025), Eccleston & Furnham (2025), Kinase pLM framework (2026).

**Inconsistency.** The prose above the table says "I re-checked **nine** papers at source
this session". The table has **ten** rows and the conclusion says "8 of **10**". The
arithmetic of the conclusion is internally consistent (8 "No" + 1 between-method + 1
other = 10); the word "nine" is the error. Fix the prose, not the table.

**Spot-checks. Four done, not three. All four hold.**

**APOP (2023), doi:10.1093/bioinformatics/btad275 — CONFIRMED exactly.** PMCID PMC10185404,
"Predicting allosteric pockets in protein biological assemblages", Kumar A, Kaynak BT,
Dorman KS, Doruker P, Jernigan RL, _Bioinformatics_ 2023. Verbatim:

> "A one-sided Wilcoxon signed-rank test ... was applied to test if there is a significant
> difference between known allosteric pocket ranking performance between APOP and Allopred."

> "Furthermore, the _P_-value of 0.00088 obtained from the one-sided Wilcoxon signed-rank
> ... results indicate the ranking of known allosteric pocket obtained with APOP to be
> significantly better than with Allopred."

The audit's characterisation is precise: a test, one-sided Wilcoxon signed-rank,
P = 0.00088, **between two methods, not against a null**. The abstract also confirms the
audit's census figure: "Out of the 104 test cases, APOP predicts known allosteric pockets
for 92 within the top 3 rank."

**PocketMiner (2023), doi:10.1038/s41467-023-36699-3 — CONFIRMED.** PMCID PMC9977097,
"Predicting locations of cryptic pockets from single protein structures using the
PocketMiner graph neural network", Meller A et al., _Nat Commun_ 2023. No p-value, no
permutation test, no null model, no confidence interval and no bootstrap is applied to any
performance claim. The reported "ROC-AUC 0.83 ± 0.04" and "PR-AUC 0.44" carry
cross-validation standard deviations across 5 folds — exactly what the audit's row says
("Standard deviations across CV folds only"). The held-out experimental task reports
ROC-AUC 0.87 with no uncertainty, and the comparison against CryptoSite (0.87 vs 0.85) has
no test.

**CryptoBench (2025), doi:10.1093/bioinformatics/btae745 — CONFIRMED.** PMCID PMC11725321,
Škrhák V, Novotný M, Feidakis CP, Krivák R, Hoksza D. No p-values, permutation tests, null
models, confidence intervals or bootstraps anywhere. The metric panel is AUC, AUPRC, ACC,
TPR, FPR, MCC and F1 — exactly the audit's census row 36 — reported as point estimates in
Table 5. **Minor citation note:** Europe PMC dates this 2024 (PMID 39693053, December
2024). The audit lists it as 2025, which matches the journal issue rather than the
publication date. Not worth changing.

**Allo-Allo (2024) — see item 6.** The row's verdict ("Not on performance") is right; the
row's description of what the test was is wrong.

**Conclusion.** The audit's independent corroboration of the repo's "13 of 18" claim holds.
Four of four spot-checks match the audit's verdict column.

---

## 8. The derived ceilings. PARTIALLY CONFIRMED.

**Verdict: PARTIALLY CONFIRMED. Two of three are exact. The MCC shorthand is loose and
should be replaced.**

Setup: fixed prediction of k = 5, perfect precision, label set of size m, candidate set of
size n. Then TP = 5, FP = 0, FN = m − 5, TN = n − m.

**max F1 = 10/(m + 5). CONFIRMED, and it is exact.**

F1 = 2·TP / (2·TP + FP + FN). Substituting FP + FN = (k − TP) + (m − TP) gives
2·TP + FP + FN = k + m, so F1 = 2·TP/(k + m) identically. At TP = k = 5 this is
10/(m + 5), with no dependence on n. For m = 11 that is 0.625; for m = 20, 0.400. Both
digits check.

**max Jaccard = 5/m. CONFIRMED, and it is exact.**

Jaccard = TP/(TP + FP + FN) = TP/(k + m − TP) = 5/m at TP = 5. For m = 11, 0.4545; for
m = 20, 0.25. Both check.

**max MCC. The audit's closed form is exact. The `≈ sqrt(5/m)` shorthand is not.**

MCC = (TP·TN − FP·FN) / sqrt((TP+FP)(TP+FN)(TN+FP)(TN+FN)). With FP = 0:

- numerator = 5(n − m)
- denominator = sqrt(5 · m · (n − m) · (n − 5))
- MCC = 5(n − m)/sqrt(5m(n − m)(n − 5)) = **sqrt(5(n − m) / (m(n − 5)))**

That is the audit's §3.2 formula, character for character. **CONFIRMED.**

The shorthand drops the factor sqrt((n − m)/(n − 5)), which is strictly less than 1 whenever
m > 5. So `sqrt(5/m)` always **overstates** the ceiling. Computed against the frozen primary
arms (`docs/benchmark/primary/README.md` §3, m = scoreable labels, n = candidates):

| Arm                        |   m |   n | exact max MCC | sqrt(5/m) | shorthand overstates by |
| -------------------------- | --: | --: | ------------: | --------: | ----------------------: |
| `kras_g12c_mandated`       |  16 | 146 |     **0.537** |     0.559 |                   4.1 % |
| `kras_g12c_corrected`      |  16 | 148 |     **0.537** |     0.559 |                   4.1 % |
| `bcr_abl1_mandated`        |  20 | 440 |     **0.491** |     0.500 |                   1.8 % |
| `bcr_abl1_corrected`       |  18 | 261 |     **0.513** |     0.527 |                   2.6 % |
| `cardiac_myosin_corrected` |  12 | 743 |     **0.642** |     0.645 |                   0.5 % |

The error is small but it always runs one way, and it runs **against the audit's own
argument**. The audit uses these ceilings to show that a perfect top-5 answer cannot match
STINGAllo's per-residue F1 = 0.64 and MCC = 0.64. Using the exact form makes that argument
stronger: on the primary arms, only `cardiac_myosin_corrected` reaches MCC 0.64 at all, and
it clears it by 0.002. Every other primary arm caps at 0.49–0.54.

The F1 half of the claim is unconditionally true: max F1 on the primary arms runs
0.400–0.588, so **no** primary arm can reach STINGAllo's F1 of 0.64 even with a perfect
answer. The audit's "on the repo's larger arms" is an understatement.

**Correction to recommendation 3.** The manifest text should read:

- `max F1 = 10/(m + 5)` — exact, n-independent
- `max Jaccard = 5/m` — exact, n-independent
- `max MCC = sqrt(5(n − m) / (m(n − 5)))` — exact; **do not** write `≈ sqrt(5/m)`, which
  overstates by up to 4.1 % on the frozen arms

The audit's stated ranges (F1 0.40–0.625, Jaccard 0.25–0.4545) span all 14 arms, so they
imply m runs 11 to 20 across primary and secondary. The primary-only ranges are F1
0.400–0.588, Jaccard 0.25–0.4167, exact MCC 0.491–0.642. The secondary-set values were not
re-derived here.

---

## 9. "CASP has dropped the category". CONFIRMED.

**Verdict: CONFIRMED. And the audit's own `[NOT ESTABLISHED]` flag on this can be closed.**

**CASP16 has no FN category.** The category list at
<https://predictioncenter.org/casp16/index.cgi> is: Single Proteins and Domains; Protein
Complexes; Accuracy Estimation; Nucleic acid structures and complexes; Protein–organic
ligand complexes; Macromolecular conformational ensembles; Integrative modeling. No
function-prediction and no binding-residue category. That reproduces the audit's list
exactly.

**CASP11 has no FN category either.** <https://predictioncenter.org/casp11/index.cgi>
lists Tertiary Structure (TBM, FM, refinement, contact-assisted, alignment-assisted),
Residue-Residue Contacts, Disordered Regions and Quality Assessment. No FN.

**The last edition was CASP10, and CASP said so at the time.** The audit marks
"[whether] CASP formally retired the FN category or merely did not run it in CASP16" as
`[NOT ESTABLISHED]`, saying no retirement statement was found. The statement exists, and
it is in the CASP10 assessment paper the audit already cites. Gallo Cassarino T, Bordoli L,
Schwede T, "Assessment of ligand binding site predictions in CASP10", _Proteins_
82(S2):154–163, 2014, doi:10.1002/prot.24495, read at
<https://pmc.ncbi.nlm.nih.gov/articles/PMC4495912/>:

> "prediction methods in the FN category in future editions of CASP will no longer be
> evaluated based on the regular set of CASP target proteins. Instead, ligand binding site
> prediction servers will be evaluated continuously using an automated system called
> Continuous Automated Model Evaluation (CAMEO)"

CASP10's FN round assessed 17 groups on 13 targets carrying biologically relevant ligands.

**The precise statement the repo should carry.** CASP10 (assessed 2014) was the last CASP
edition to run a ligand-binding-site prediction category on regular CASP targets. The
category was **moved to CAMEO for continuous automated evaluation**, not abolished
outright. That distinction matters for the audit's own §12 rebuttal: "no community blind
assessment exists" is too strong. "No episodic community blind assessment on CASP targets
has run since CASP10; continuous automated evaluation moved to CAMEO" is what the source
supports.

**The CASP16 ligand category is a different task: CONFIRMED.** doi:10.1002/prot.70061 is
"Assessment of Pharmaceutical Protein–Ligand Pose and Affinity Predictions in CASP16",
Gilson MK, Eberhardt J, Škrinjar P, Durairaj J, Robin X, Kryshtafovych A, _Proteins_
94(1):249–266. Poses and affinities, not binding-site residues, exactly as the audit says.

---

## 10. Eight further bibliography DOIs. CONFIRMED.

All eight resolve. Titles and authors match what the audit claims. Checked via
`api.crossref.org/works/<doi>`.

| DOI                        | Resolves to                                                                                                                                                                                                                                                                                                         | Matches audit?                                                                             |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| 10.1021/acs.jctc.6c00427   | "Predicting and Decoding Allosteric Binding Sites Using Protein Language Models and Structure-Based Machine Learning: An Energy Landscape-Guided Explainable AI Framework". Riedlová K, Škrhák V, Gatlin WG, Ludwick M, Turano L, Novotný M, Hoksza D, Verkhivker GM. _J Chem Theory Comput_ 22(10):5326–5347, 2026 | Yes. Authors, journal, volume, issue and pages all exact. The audit truncates the subtitle |
| 10.1021/acs.jpcb.6c00242   | "AlloEF: An Ensemble Model for Protein Allosteric Site Identification Based on Transfer Entropy and Energetic Frustration". Zhang J, Sun X, Wu Z, Su J, Zhang X, Li C. _J Phys Chem B_ 130(19):4970–4981, 2026                                                                                                      | Yes, exactly                                                                               |
| 10.64898/2026.01.05.697819 | "Protein Language Models and Structure-Based Machine Learning for Prediction of Allosteric Binding Sites in Protein Kinases: An Explainable AI Framework Grounded in Energy Landscape-Encoded Frustration". Same author group. openRxiv preprint, posted 2026-01-06                                                 | Yes. Preprint of the row above; title changed on publication, which is normal              |
| 10.1002/prot.70061         | "Assessment of Pharmaceutical Protein–Ligand Pose and Affinity Predictions in CASP16". Gilson MK et al. _Proteins_ 94(1):249–266                                                                                                                                                                                    | Yes                                                                                        |
| 10.1093/nar/gkaf411        | "LIGYSIS-web: a resource for the analysis of protein-ligand binding sites". Utgés JS, MacGowan SA, Barton GJ. _Nucleic Acids Res_ 53(W1):W351–W360, 2025                                                                                                                                                            | Yes                                                                                        |
| 10.1145/1852102.1852106    | "A similarity measure for indefinite rankings". Webber W, Moffat A, Zobel J. _ACM Trans Inf Syst_ 28(4), 2010                                                                                                                                                                                                       | Yes. The RBO DOI flag can be closed                                                        |
| 10.1186/s13059-019-1738-8  | "Essential guidelines for computational method benchmarking". Weber LM, Saelens W, Cannoodt R, Soneson C, Hapfelmeier A, Gardner PP, Boulesteix A-L, Saeys Y, Robinson MD. _Genome Biol_ 20:125, 2019                                                                                                               | Yes                                                                                        |
| 10.1002/advs.202513641     | "A Quantum Framework for Protein Binding-Site Structure Prediction on Utility-Level Quantum Processors". Zhang Y, Yang Y, Martin W, Lin K, Wang Z, Lu C-C, Jiang W, Nussinov R, Loscalzo J, Guan Q, Cheng F. _Advanced Science_ 13:e13641                                                                           | Title and authors yes. **Year is 2025**, not 2026 — Crossref publication date 2025-11-28   |

**One correction: the _Adv Sci_ entry is 2025, not 2026.** Cosmetic, but it is in a
bibliography whose stated standard is that every DOI resolved this session.

Also checked, because it is the one entry in the audit with no DOI at all:
**arXiv:2608.22659 exists.** "Statistical Methods for Multiple Language Model Comparison on
a Shared Evaluation", Juan Francisco Mandujano Reyes, submitted 23 August 2026. The audit
describes it as "two weeks old", which is right to the day. Its stated validation is six
models on 1,497 MMLU-Pro questions across 14 subject clusters, with models as fixed effects
and questions as random effects. That matches the audit's description.

---

## 11. Found in passing: census row 35 is wrong about Allo-Allo's AUROC. REFUTED.

The audit's §2.1 census row 35 reports Allo-Allo as "AUPRC 0.77 / AUROC 0.95".

**AUPRC 0.77 is correct.** From the abstract: Allo-Allo "achieves an AUPRC of 0.77 on
allosteric site prediction, compared to the current best AUPRC of 0.46 (PASSerRank)".

**AUROC 0.95 is not Allo-Allo's.** It belongs to the prediction-head MLP **baseline** in
Appendix A, which "achieved an AUPRC of 0.68 and an AUROC of 0.95 on the test set". That
baseline is the alternative architecture Allo-Allo is argued to beat, and it beats it on
AUPRC, not AUROC. Quoting 0.95 as Allo-Allo's number attributes a competitor's score to the
method.

This is the same failure mode the repo's own evidence base already flags as `AUDIT.md` B3:
a number carried across a row boundary. Correct row 35 to "AUPRC 0.77; no AUROC reported
for Allo-Allo itself" before the census is cited anywhere.

---

## What could not be checked, and why

- **CAPASP per-tool numbers and dataset sizes.** Springer paywall. Abstract retrieved via
  Europe PMC; full text not attempted, because the audit already marks this
  `[NOT ESTABLISHED]` and nothing here depends on it.
- **UniSite's three body quotes** (20 % double-counting, ground-truth DCC/DCA deviation,
  "completely disregard the structural properties"). The metric claim was confirmed at the
  abstract; the body quotes were not individually located. The recommendations that depend
  on UniSite depend only on the metric claim.
- **AlloEF's F1 0.630 / MCC 0.609 and the provenance of its transfer entropy.** ACS returns
  403 to automated fetches. The DOI, title, authors, journal, volume and pages are
  confirmed; the numbers are not. The audit already tags them `[UNVERIFIED]`, and the C2
  question ("MD or elastic network?") stays `[NOT ESTABLISHED]`.
- **The eigenstrapping FPRs on empirical (non-simulated) maps.** Only the Gaussian
  random-field results were checked, because those are the ones the audit quotes.
- **The secondary set's m and n values**, needed to give the exact MCC ceiling on the
  m = 11 arm. Only the five primary arms were re-derived. The formula is exact for all 14.

## Direct sources

- <https://api.crossref.org/works/10.1162/IMAG.a.71>
- <https://pmc.ncbi.nlm.nih.gov/articles/PMC12330862/>
- <https://www.biorxiv.org/content/10.1101/2024.02.07.579070v2.full> (preprint, different numbers)
- <https://api.crossref.org/works/10.64898/2026.01.28.702257>, <https://www.biorxiv.org/content/10.64898/2026.01.28.702257v1.full>
- <https://api.crossref.org/works/10.1007/s10822-026-00831-4>, Europe PMC PMID 42126486
- <https://arxiv.org/abs/2506.03237>
- <https://api.crossref.org/works/10.1162/imag.a.118>, Europe PMC PMID 40860578
- <https://www.biorxiv.org/content/10.1101/2024.09.28.615583v1.full>
- <https://pmc.ncbi.nlm.nih.gov/articles/PMC10185404/> (APOP)
- <https://pmc.ncbi.nlm.nih.gov/articles/PMC9977097/> (PocketMiner)
- <https://pmc.ncbi.nlm.nih.gov/articles/PMC11725321/> (CryptoBench)
- <https://predictioncenter.org/casp16/index.cgi>, <https://predictioncenter.org/casp11/index.cgi>
- <https://pmc.ncbi.nlm.nih.gov/articles/PMC4495912/> (CASP10 FN assessment)
- <https://arxiv.org/abs/2608.22659>
- Crossref records for the eight DOIs in item 10
