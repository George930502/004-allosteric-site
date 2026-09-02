# Fact-check of files 17, 18 and 19

**Scope:** independent retrieval and verification of the load-bearing claims in
`17-generalisation-variance.md`, `18-selection-sample-complexity.md` and
`19-cross-protein-normalisation.md`. It checks the source, the quoted string, the numbers, the
internal repository cross-references, and — for the two results in file 19 that are mathematics
rather than citation — the reasoning. It deliberately excludes any re-argument of a method's merit,
and it does not check claims on which no decision rests.
**Sibling files:** `00-conventions.md` for the evidence tags and the file format;
`10a-fact-check.md`, the equivalent pass over files 01–09, whose format and severity conventions
this file follows; files 17, 18 and 19 for the claims themselves.
**Retrieved:** 2026-08-27.

---

## 1. Verdict summary

Sixty-five claims checked. **Fifty-one CONFIRMED, nine OVERSTATED, two WRONG, three UNVERIFIABLE.**
By file: 17 is 14 / 5 / 1 / 2 over 22 claims; 18 is 22 / 2 / 1 / 0 over 25; 19 is 15 / 2 / 0 / 1 over 18.

### File 17 — between-target variance

| #     | Claim (short)                                                                         | Source                                  | Tag in doc            | Verdict          |
| ----- | ------------------------------------------------------------------------------------- | --------------------------------------- | --------------------- | ---------------- |
| 17.1  | No retrieved paper reports a between-target **standard deviation** of AUC             | negative result of recorded search      | negative result       | **CONFIRMED**    |
| 17.2  | Kinase PLM is "the only retrieved instance" treating dispersion as reportable         | doi:10.1021/acs.jctc.6c00427            | `[VERIFIED-FULLTEXT]` | **OVERSTATED**   |
| 17.3  | §6: "nobody publishes a between-target AUC standard deviation for this task"          | none                                    | untagged assertion    | **OVERSTATED**   |
| 17.4  | PocketMiner 0.87 pooled over 563 + 1283 residues, 35 structures, no per-structure AUC | doi:10.1038/s41467-023-36699-3          | `[VERIFIED-FULLTEXT]` | **CONFIRMED**    |
| 17.5  | PocketMiner 0.87 → AUC 0.76 / AUPRC 0.19 on CryptoBench, pre-trained                  | doi:10.1093/bioinformatics/btae745      | `[VERIFIED-FULLTEXT]` | **CONFIRMED**    |
| 17.6  | CASP10 per-target median MCC ≈ −0.05 to ≈ 0.6 over 13 targets                         | doi:10.1002/prot.24495                  | `[VERIFIED-FULLTEXT]` | **CONFIRMED**    |
| 17.7  | CryptoSite per-protein sensitivity 0 % to 100 %, all nine named values                | doi:10.1016/j.jmb.2016.01.029           | `[VERIFIED-FULLTEXT]` | **CONFIRMED**    |
| 17.8  | CryptoSite "79-protein LOO training set"                                              | doi:10.1016/j.jmb.2016.01.029           | `[VERIFIED-FULLTEXT]` | **UNVERIFIABLE** |
| 17.9  | P2Rank HOLO4K 68.6 % vs 81.2 % on HOLO4K(Mlig+); COACH420 72.0 → 74.9                 | doi:10.1186/s13321-018-0285-8 + 3c01698 | `[VERIFIED-FULLTEXT]` | **CONFIRMED**    |
| 17.10 | AlloBench puts the best of eight tools at 18 % at JI > 0.5                            | doi:10.1021/acsomega.5c01263            | `[VERIFIED-FULLTEXT]` | **CONFIRMED**    |
| 17.11 | DeepSite −10.8 points; ties Fpocket on COACH420, 6.8 behind on HOLO4K                 | doi:10.1186/s13321-018-0285-8           | `[VERIFIED-FULLTEXT]` | **CONFIRMED**    |
| 17.12 | Kinase PLM 0.968/0.629 Type I, 0.676/0.077 Type IV, max 0.975/0.749                   | doi:10.1021/acs.jctc.6c00427            | `[VERIFIED-FULLTEXT]` | **CONFIRMED**    |
| 17.13 | Executive item 7 calls 0.292 / 0.552 "the largest single-model spread retrieved"      | same paper                              | `[VERIFIED-FULLTEXT]` | **OVERSTATED**   |
| 17.14 | CASP9: "similar spectrum of results…"; "highly target specific, or…random"            | doi:10.1002/prot.23174                  | `[VERIFIED-FULLTEXT]` | **OVERSTATED**   |
| 17.15 | CASP9 best-per-target averaged 0.84; T0604 best 0.56, average 0.29                    | doi:10.1002/prot.23174                  | `[VERIFIED-FULLTEXT]` | **CONFIRMED**    |
| 17.16 | Q3 table sources the T0659 template quote to "CASP9"                                  | doi:10.1002/prot.24495                  | `[VERIFIED-FULLTEXT]` | **WRONG**        |
| 17.17 | GrASP Mlig+ re-filtering, quoted string                                               | doi:10.1021/acs.jcim.3c01698            | `[VERIFIED-FULLTEXT]` | **OVERSTATED**   |
| 17.18 | CryptoBench sizes: PocketMiner 38, CryptoSite 93, CryptoBench 1107                    | doi:10.1093/bioinformatics/btae745      | `[VERIFIED-FULLTEXT]` | **CONFIRMED**    |
| 17.19 | §6 Hanley–McNeil arithmetic: SE 0.091/0.090/0.074/0.074, mean 0.082, d₂ = 2.059       | doi:10.1148/radiology.143.1.7063747     | `[UNVERIFIED]`        | **CONFIRMED**    |
| 17.20 | The arm sizes 11/136, 11/287, 16/534, 16/550                                          | `40-method-sweep.md` §1                 | repo                  | **CONFIRMED**    |
| 17.21 | **The spreads 0.175 (classical) and 0.361 (quantum)**                                 | attributed to `40-method-sweep.md`      | repo                  | **UNVERIFIABLE** |
| 17.22 | Repo quotes 0.810 / 0.944 / 0.703; 0.824 / 0.377; quantum median 0.455                | `40-method-sweep.md` §4, §6             | repo                  | **CONFIRMED**    |

### File 18 — selection sample complexity

| #     | Claim (short)                                                                                     | Source                                  | Tag in doc            | Verdict        |
| ----- | ------------------------------------------------------------------------------------------------- | --------------------------------------- | --------------------- | -------------- |
| 18.1  | `OPENML-WEKA-2017`: 30 algorithms, 105 instances, 103 features, Quality, VBS/SBS 1.02             | doi:10.1016/j.artint.2018.10.004 Tab. 2 | `[VERIFIED-FULLTEXT]` | **CONFIRMED**  |
| 18.2  | "six out of eight submissions performed almost equal to or worse than the SBS"                    | ibid. §5.7                              | `[VERIFIED-FULLTEXT]` | **CONFIRMED**  |
| 18.3  | Table E.9: 0.950, 0.950, 0.787, 0.877, 1.000, 1.000, 3.798, 7.233                                 | ibid. Table E.9                         | `[VERIFIED-FULLTEXT]` | **CONFIRMED**  |
| 18.4  | Best of eight closed 21 % of a gap of factor 1.02                                                 | ibid. Tables 2, E.9                     | `[VERIFIED-FULLTEXT]` | **CONFIRMED**  |
| 18.5  | SATzilla07: 4 811 instances = 2 300 + 1 490 + 1 021; split 40:30:30; 7 solvers; 48 features       | arXiv:1111.2249 §3.1–3.3                | `[VERIFIED-FULLTEXT]` | **CONFIRMED**  |
| 18.6  | Therefore 40 % of 1 021 ≈ 408 and 40 % of 4 811 ≈ 1 924 **instances trained on**                  | derived from the above                  | `[VERIFIED-FULLTEXT]` | **OVERSTATED** |
| 18.7  | Gupta & Roughgarden Thm 3.2 `m ≥ c(H/ε)²(d_ℋ + ln(1/δ))`; Cor 3.4; Thm 3.6; Thm 3.19              | arXiv:1511.07147 §3                     | `[VERIFIED-FULLTEXT]` | **CONFIRMED**  |
| 18.8  | The bound is vacuous at m = 4: ε ≈ 1.00; ε = 0.10 needs 400; ε = 0.05 needs 1 600                 | derived on the verified formula         | `[UNVERIFIED]`        | **CONFIRMED**  |
| 18.9  | Balcan, Sandholm & Vitercik: three channels; "overfitting is inevitable…"                         | arXiv:2012.13315 abstract               | `[VERIFIED-ABSTRACT]` | **CONFIRMED**  |
| 18.10 | **The two papers use opposite sign orientations**                                                 | artint eq. (2) vs PMLR 79 eq. (2)       | `[VERIFIED-FULLTEXT]` | **CONFIRMED**  |
| 18.11 | 2015 best 0.366 (zilla); 2017 best 0.38 (ASAP.v2); 2017 VBSel 0.29                                | ibid. Tables 3, 4, §5.3                 | `[VERIFIED-FULLTEXT]` | **CONFIRMED**  |
| 18.12 | The 13 ASlib 2015 scenario rows, every count and factor                                           | ibid. Table 1                           | `[VERIFIED-FULLTEXT]` | **CONFIRMED**  |
| 18.13 | The six quoted 2017 scenario rows, every count and factor                                         | ibid. Table 2                           | `[VERIFIED-FULLTEXT]` | **CONFIRMED**  |
| 18.14 | "5–31 algorithms and 100–9720 instances"; participants got 2/3 train, 1/3 test                    | PMLR 79:1–7 §§2–3                       | `[VERIFIED-FULLTEXT]` | **CONFIRMED**  |
| 18.15 | Demšar: Friedman "N > 10 and k > 5"                                                               | JMLR 7:1–30 §3.2.2                      | `[VERIFIED-FULLTEXT]` | **CONFIRMED**  |
| 18.16 | Demšar: paired t-test needs ∼30 data sets; the "small samples" passage                            | ibid. §3.1.2                            | `[VERIFIED-FULLTEXT]` | **CONFIRMED**  |
| 18.17 | Demšar Table 3 begins at N = 5 and needs all five wins; no N = 4 column                           | ibid. Table 3                           | `[VERIFIED-FULLTEXT]` | **CONFIRMED**  |
| 18.18 | 2015: no significant difference between any of the submissions (Friedman/Nemenyi)                 | doi:10.1016/j.artint.2018.10.004 §4.1   | `[VERIFIED-FULLTEXT]` | **CONFIRMED**  |
| 18.19 | The random-forest baseline: 100 holdout sets, 18 %, 67.5 % vs 78 %                                | ibid. §5.7                              | `[VERIFIED-FULLTEXT]` | **CONFIRMED**  |
| 18.20 | ASAP.v2's lucky seed: score 0.025 has probability 0.466 % over 1 500 seeds                        | ibid. §5.4                              | `[VERIFIED-FULLTEXT]` | **CONFIRMED**  |
| 18.21 | Every combinatorial floor: 2/n!, 2/2ⁿ, E = 2.500, P(≥1) = 0.9265, Poisson 0.287, Bonferroni n ≥ 7 | derived                                 | `[UNVERIFIED]`        | **CONFIRMED**  |
| 18.22 | **`1 − (11/12)¹⁰ = 0.5793`**                                                                      | derived                                 | `[UNVERIFIED]`        | **WRONG**      |
| 18.23 | "static (instance-features free) pre-solving schedules…"                                          | ibid. §2.3                              | `[VERIFIED-FULLTEXT]` | **OVERSTATED** |
| 18.24 | Fast Downward Stone Soup won an IPC-2011 track; auto-sklearn won two challenges                   | ibid. §2.1                              | `[VERIFIED-FULLTEXT]` | **CONFIRMED**  |
| 18.25 | Repo cross-references: 1 923 variants, 69 scorers, 8.86/10.58, 0.794–0.955, `44` §§3,4,6          | repo                                    | repo                  | **CONFIRMED**  |

### File 19 — cross-protein normalisation

| #     | Claim (short)                                                                                 | Source                            | Tag in doc            | Verdict          |
| ----- | --------------------------------------------------------------------------------------------- | --------------------------------- | --------------------- | ---------------- |
| 19.1  | Brinda & Vishveshwara: 232 proteins; SD 0.9 around mean ∼3.9; > 85 % in 3.0–5.0               | doi:10.1529/biophysj.105.064485   | `[VERIFIED-FULLTEXT]` | **CONFIRMED**    |
| 19.2  | "I_critical … is generally higher for bigger proteins"; bins ≈ 3.25 % → > 4.25 %              | ibid.                             | `[VERIFIED-FULLTEXT]` | **CONFIRMED**    |
| 19.3  | The abstract says "within a narrow cutoff range regardless of protein size"                   | ibid., abstract                   | `[VERIFIED-ABSTRACT]` | **OVERSTATED**   |
| 19.4  | Maxwell counting gives ⟨k⟩ = 6 − 12/N → 6, and z = 2d                                         | derived here                      | `[UNVERIFIED]`        | **CONFIRMED**    |
| 19.5  | The scalar analogue gives ⟨k⟩ = 2, a tree, so the rule suits the vector ENM only              | derived here                      | `[UNVERIFIED]`        | **CONFIRMED**    |
| 19.6  | Our ⟨k⟩/6 = 1.48–1.72                                                                         | `30-frozen-graph-profile.md` §3.3 | `[UNVERIFIED]`        | **CONFIRMED**    |
| 19.7  | GNM: ≤ 7.0 Å Cα pairs; single-parameter harmonic potential; 12 structures, 41–633             | doi:10.1016/S1359-0278(97)00024-2 | `[VERIFIED-ABSTRACT]` | **CONFIRMED**    |
| 19.8  | ANM: "quite robust … in the range of 15–24 Å"; p = 2.5; 176 structures                        | doi:10.1093/bioinformatics/btl448 | `[VERIFIED-ABSTRACT]` | **CONFIRMED**    |
| 19.9  | Fuglebakk: "large and consistent differences…"; "recommend against using B-factors"           | doi:10.1021/ct400399x             | `[VERIFIED-ABSTRACT]` | **CONFIRMED**    |
| 19.10 | Hinsen: Debye-Waller / crystal-packing sentences                                              | doi:10.1093/bioinformatics/btm625 | `[VERIFIED-ABSTRACT]` | **CONFIRMED**    |
| 19.11 | Guney: `d_c`, the z-score, 1 000 repetitions, ≥ 100-node bins, 28.6 vs 21.2                   | doi:10.1038/ncomms10331           | `[VERIFIED-FULLTEXT]` | **CONFIRMED**    |
| 19.12 | Sobieraj & Setny: MI minimum universally at 5 Å; construction is MD-based (C2)                | doi:10.1002/prot.26154            | `[VERIFIED-ABSTRACT]` | **CONFIRMED**    |
| 19.13 | **Derived (a): AUC is rank-invariant, so a uniform rescaling is a no-op**                     | derived here                      | `[UNVERIFIED]`        | **CONFIRMED**    |
| 19.14 | **Derived (b): a θ-sliding rule moves any spread statistic by at most ≈ 2·R_within**          | derived here                      | `[UNVERIFIED]`        | **CONFIRMED**    |
| 19.15 | The §1.2 worked example (R_within 0.079, spread 0.668, bound 0.16, measured 0.011)            | `44-stability-and-noise.md` §6    | `[VERIFIED-FULLTEXT]` | **OVERSTATED**   |
| 19.16 | The §6 internal fact-check: ratios 21.72, 140, 1.20                                           | `47` §1, `44` §6                  | `[VERIFIED-FULLTEXT]` | **CONFIRMED**    |
| 19.17 | Repo quotes: 8.9–10.3, 0.460–0.515, 10.40–11.80, 7.2×; the diameter/N^⅓ table; 0.486 vs 0.109 | repo                              | mixed                 | **CONFIRMED**    |
| 19.18 | "`effective_resistance_to_source` already scores best 0.721 in the battery"                   | no file named                     | untagged              | **UNVERIFIABLE** |

---

## 2. Claim-by-claim detail

### 2.1 File 17

#### 17.1 — the negative claim, and whether the searches were adequate

**Verdict: CONFIRMED, with a named retrieval gap that does not overturn it.**

The claim as written in §Q2 is correctly hedged: "**No paper retrieved** reports a between-target
standard deviation of AUC for allosteric or cryptic-site prediction … Record that as a negative
result of the recorded search, not as an absence." That is exactly what ADR 0019 requires.

Four Europe PMC searches were run this session that file 17 did not run, chosen to be the queries
most likely to surface a counter-example. Eighty-two records screened, none reporting a
between-target standard deviation of AUC for allosteric-, cryptic- or pocket-prediction:

| Query                                                                                                                                                                                                                        | Hits | Counter-examples |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---- | ---------------- |
| `("per-protein AUC" OR "per-target AUC" OR "per-structure AUC" OR "per-chain AUC")` — **unconjoined**                                                                                                                        | 8    | 0                |
| `"mean AUC" AND "standard deviation" AND ("binding site prediction" OR "pocket prediction" OR "allosteric site" OR "cryptic pocket")`                                                                                        | 22   | 0                |
| `("allosteric site" OR "cryptic pocket" OR "cryptic site") AND "AUC" AND ("across proteins" OR "between proteins" OR "protein-to-protein variability" OR "varied across targets")`                                           | 35   | 0                |
| `("allosteric site prediction" OR "cryptic pocket prediction" OR "binding site prediction") AND ("per-protein AUC" OR "AUC per protein" OR "AUC for each protein" OR "AUC values across proteins" OR "distribution of AUC")` | 17   | 0                |

Two near misses were followed to full text and neither is a counter-example:

- **MEF-AlloSite** (Ugurlu, McDonald & He, _J Cheminform_ 2024, doi:10.1186/s13321-024-00882-5,
  PMC11515501) reports ROC-AUC **distributions**, but the distribution is over **51 different splits
  of the training set** on three test cases — a between-split dispersion, not a between-target one.
  The distinction matters and file 17 never draws it; a cross-validation standard deviation answers a
  different question from a between-protein one.
- **Utgés & Barton** (_J Cheminform_ 2024, doi:10.1186/s13321-024-00923-z, PMC11552181) reports
  **mean ROC-AUC only in the main text**, with no ± SD. The literal claim therefore survives.

**But Utgés & Barton is a retrieval gap that must be recorded**, because two other statements in
file 17 do not survive it (17.2, 17.3), and because of what the paper is. It benchmarks 13 ligand
binding-site predictors spanning 30 years against LIGYSIS, and it is the most recent large-scale
comparative evaluation in this literature. Two properties bear directly on file 17's subject:

> Mean ROC and PR curves are calculated by averaging the curves of the 2775 LIGYSIS protein chains.

That is a **macro estimator over 2 775 targets** — the same estimator file 17 says only one paper
uses. And its Supplementary Figures 10–11 show the "variation in ROC and AUC across LIGYSIS protein
chains", which is a **published between-target AUC distribution for binding-site prediction at
N = 2 775**. It publishes the distribution and not the summary statistic.

The sharpest form of the gap: file 17 cites the kinase PLM paper (doi:10.1021/acs.jctc.6c00427) and
correctly records that its training set is **LIGYSIS** with a 30 % identity filter — but never
retrieves the LIGYSIS benchmark paper itself. The recorded stopping rule ("stop when three
independently retrieved sources agree that per-target reporting is absent from the modal method
paper") stopped the search before a paper that reports per-target dispersion at N = 2 775 was found.

#### 17.2 — "the only retrieved instance"

**Verdict: OVERSTATED.** §Q1 closes with "That is the only retrieved instance of a site-prediction
paper treating between-target dispersion as a reportable property of a method", and the
"What the literature does NOT support" list repeats it as "Only the kinase PLM study
(doi:10.1021/acs.jctc.6c00427) reports both." Utgés & Barton reports both estimators and publishes
the per-chain dispersion. Delete "only" and add the second citation.

The direction of this error is favourable to file 17's own recommendation 1 — a second, far larger
precedent for macro-averaging strengthens the case for keeping the per-arm table primary — so the
fix is an addition, not a retraction.

#### 17.3 — "nobody publishes"

**Verdict: OVERSTATED.** §6 states: "The literature alone cannot answer it, for the reason in §2:
**nobody publishes** a between-target AUC standard deviation for this task." That is an
absence-of-prior-art claim from a scoped search, which ADR 0019 forbids and which file 17's own §Q2
explicitly disclaims two pages earlier. The executive summary carries the same slippage ("no
retrieved paper" is correct there; "nobody publishes" is not). One word, but §6's calibration
verdict is built on it.

#### 17.4, 17.5, 17.18 — PocketMiner and CryptoBench

**Verdict: CONFIRMED**, all three, verbatim.

> We find that our final model, referred to as PocketMiner, achieves very good performance at
> discriminating residues that form cryptic pockets from those that do not (ROC AUC: 0.87).

> In total, there were 563 residues that form cryptic pockets and 1283 residues that do not form
> cryptic pockets in our test set.

The 35 structures decompose as "a total of 24 _apo_ structures that form ligand-binding cryptic
pockets, 4 hyper-rigid proteins, and 7 proteins that were the subjects of extensive ligand
screening". **No per-structure or per-protein AUC appears anywhere in the paper**, confirmed on a
direct question. File 17's structural observation is sound.

CryptoBench Table 5: PocketMiner **AUC 0.76, AUPRC 0.19**. Pre-trained without retraining, verbatim:

> We used the model available on the project GitHub page for PocketMiner without any retraining or
> fine-tuning, as the repository does not provide a documented way of retraining/tuning the model on
> new structures and labels.

Sizes 38 / 93 / 1107 confirmed. **One caveat file 17 does not carry:** "PocketMiner encountered
prediction errors for 22 structures from the test subset, leading to their exclusion from the
evaluation." The −0.11 delta is still the cleanest AUC-to-AUC cross-benchmark comparison in this
literature, but the away number is computed on a subset with 22 structures dropped for a reason
correlated with the method. Say so wherever −0.11 is quoted. For scale, the same table puts P2Rank
at AUC 0.81 on its own apo subset of CryptoBench.

#### 17.6 — CASP10

**Verdict: CONFIRMED.** The long quotation is verbatim:

> On most targets the predictors achieved on average a good performance around an MCC of 0.6, except
> in three cases, where in two (T0657 and T0659) the median scores were around zero and in one
> (T0720) was around 0.2.

Thirteen targets confirmed; the lowest per-target median MCC is **−0.05**, on T0657.

**One qualification on the derived spread.** File 17 records "Spread ≈ 0.65 MCC" from "about −0.05
to about 0.6". The 0.6 is the paper's _typical_ value ("on most targets… around an MCC of 0.6"), not
the maximum, so 0.65 is a lower bound on the true per-target range rather than an estimate of it.
The direction is conservative, which is the safe direction here.

#### 17.7 and 17.8 — CryptoSite

**Verdict on the sensitivities: CONFIRMED**, all nine values exactly as file 17 prints them —
HCV RNA polymerase 0 %, Ca-ATPase 6 %, kynurenine aminotransferase II 17 %, PTP1B allosteric site
29 %, biotin carboxylase 56 %, exportin 1 68 %, β-lactoglobulin 89 %, acyl-CoA binding site 98 %,
GluR2 100 %. AUC 0.83 with "respective true positive and false positive rates of 79% and 29% at the
residue score threshold of 0.05" confirmed.

**Verdict on the training-set size: UNVERIFIABLE as stated.** File 17's Q1 table says "14 held-out
apo structures; **79-protein** LOO training set". The retrieved text gives leave-one-out
cross-validation over **84** proteins in the training set containing cryptic sites. A verbatim
sentence for either number was not returned this session. Resolve it before the number is quoted
again; nothing in file 17's argument depends on which is right.

The failure-mode quotations "large conformational changes" and "partial sites that require binding
to another protein chain" came back; **"large and hydrophobic ligand binds to a cryptic site" did
not** and is recorded as not re-retrieved, not as false. The FTFlex comparison came back as
"CryptoSite is more accurate than FTFlex when a cryptic site is buried or resides in a large
protein"; file 17's version ("when a cryptic site was fully buried or when it resided in a large
protein") is tagged `[VERIFIED-ABSTRACT]` and the tense difference is consistent with an abstract
source.

#### 17.9, 17.11 — P2Rank, GrASP, DeepSite

**Verdict: CONFIRMED**, every number. P2Rank Table 3: COACH420 **72.0**, HOLO4K **68.6**. DeepSite
**56.4** and **45.6**. Fpocket **56.4** and **52.4** — so "DeepSite ties Fpocket on COACH420 and is
6.8 points behind it on HOLO4K" is exact (52.4 − 45.6 = 6.8). GrASP Table III puts P2Rank at
**81.2 %** on HOLO4K(Mlig+) and Table II at **74.9 %** on COACH420(Mlig+); GrASP's own figures are
85.3 / 77.5 / 81.3. The two derived moves check: 81.2 − 68.6 = **12.6**, 74.9 − 72.0 = **2.9**.

The dataset-difference quotation is verbatim: "HOLO4K contains mainly multimers and COACH420 only
single-chain proteins."

#### 17.10 — AlloBench

**Verdict: CONFIRMED**, and the "eight" is defensible.

> The top three programs are PASSer (Ensemble), APOP, and PASSer (AutoML), with an accuracy of 18,
> 15, and 13%, respectively.

> None of these programs could achieve an accuracy of more than 60%, even with a very low JI cutoff.

Dataset: "2141 allosteric sites from 2034 PDB structures containing 418 unique UniProt chains" —
exact. Supporting Information Table S3 "contains the Jaccard index values for each program's top
prediction across all 100 test proteins", which confirms file 17's "Yes, in Supporting Information
Table S3" and puts a number on the per-target table it lists as not reached: **100 test proteins**,
not 418.

**A note against `10a-fact-check.md` claim 8.** That file corrected `00-conventions.md`'s "no tool of
eight" to "ten configurations across eight distinct non-PASSer-variant tools". The retrieved list is
PASSer (Ensemble, AutoML, Rank), APOP, Ohm, ALLO, AllositePro, STRESS, AlloPred and Allosite — ten
configurations of **eight distinct tools**, PASSer being one of the eight. File 17's "best of eight
tools" is therefore correct as written, and the earlier correction was itself slightly off. Worth
recording so the count does not oscillate again.

#### 17.12, 17.13 — the kinase PLM

**Verdict on the numbers: CONFIRMED.** Type I AUROC 0.968 / AUPR 0.629; Type IV allosteric AUROC
0.676 / AUPR 0.077; maxima AUROC **0.975** and AUPR **0.749**, both on Type I.5. KinCoRe "10,301
complexes spanning 453 human kinases". Both micro- and macro-averaged metrics reported. The 30 %
identity filter confirmed ("MMseqs2 was used to cluster training proteins … any training sequence
with >30% sequence identity was identified" and removed). The IQR quotation is verbatim:

> the PLM exhibited narrower interquartile ranges across families, indicating more consistent
> performance and reduced variance relative to P2Rank

**Verdict on "the largest single-model spread retrieved": OVERSTATED.** Executive item 7 gives
"An AUROC spread of **0.292** and an AUPR spread of **0.552**" — which is Type I against Type IV, and
arithmetically right (0.968 − 0.676; 0.629 − 0.077). But §Q2 of the same file records **0.299** and
**0.672** for the same model, max against min over five site classes, and §6 uses 0.299. The
executive summary therefore understates its own §Q2 while calling its number the largest retrieved.
Use one convention and state which.

#### 17.14, 17.15, 17.16 — CASP9

**Verdict on 17.15: CONFIRMED.** Thirty targets; best-per-target averaged 0.84; T0604 best 0.56 with
average 0.29. Note that file 17's "Spread in best-per-target ≈ 0.28" is 0.84 − 0.56, a
mean-minus-minimum, not a maximum-minus-minimum. The number is right; the label "spread" is not.

**Verdict on 17.14: OVERSTATED, because the quotation is truncated at the point where it changes
meaning.** The first quotation is verbatim. The second is not complete. The paper reads:

> either the performance of the different methods is highly target specific, or there is a
> considerable random component in the prediction process **in combination with a strong influence
> by the small and biased target data set.**

File 17 cuts the sentence at "prediction process" in §Q3, in the executive summary, and in
"What the literature does NOT support" ("CASP9 … attributes it to the targets or to chance"). The
dropped clause names a **third** explanation — a small, biased target set — and it is the one that
cuts against the use file 17 makes of the sentence. §Q3 introduces the quote as "the field, in a
formal assessment, reporting that the target explains more of the variance than the method does";
the complete sentence declines to say that, offering target specificity, chance, **and** dataset
artefact as alternatives it does not separate. Restore the clause. The point that survives — that a
formal assessment saw the same spread among the best groups in the field and could not attribute it
— is still worth making, but it is a weaker point than the truncated version implies.

**Verdict on 17.16: WRONG (citation).** The Q3 descriptor table's first row sources
"Easily detectable homologous structures of this protein did not contain any ligand, which explains
the overall weak performance" to **CASP9**, with a parenthetical "(CASP10, T0659)". The sentence is
from **CASP10**, doi:10.1002/prot.24495, retrieved verbatim there this session. The parenthetical is
right and the source column is wrong; fix the column.

#### 17.17 — the GrASP re-filtering quotation

**Verdict: OVERSTATED.** §Q5 puts in quotation marks that GrASP's authors modified the P2Rank test
sets "to ensure ligands were both bound and biologically or pharmacologically relevant". The
retrieved text reads "We apply both sets of criteria to these sets to ensure both bound and relevant
ligands", with biological/pharmacological relevance established through Binding MOAD. The substance
is confirmed; the quoted string is a paraphrase and should lose its quotation marks. The sequence-
identity quotation is verbatim apart from a typo in the source ("sequence identify"), which file 17
silently corrects — acceptable, but flag it with `[sic]` or a note.

#### 17.19, 17.20, 17.22 — the arithmetic and the repository quotations

**Verdict: CONFIRMED.** Every step of §6 was recomputed by hand.

Arm sizes match `40-method-sweep.md` §1 exactly: `mkp5` 11 of 136, `ptp1b` 11 of 287, `hiv_rt` 16 of
534, `ns5b` 16 of 550.

Hanley–McNeil at A = 0.70, with Q₁ = A/(2−A) = 0.538462 and Q₂ = 2A²/(1+A) = 0.576471:

| Arm      | n₁  | n₂  | SE(A)   | file 17 |
| -------- | --- | --- | ------- | ------- |
| `mkp5`   | 11  | 125 | 0.09112 | 0.091   |
| `ptp1b`  | 11  | 276 | 0.08978 | 0.090   |
| `hiv_rt` | 16  | 518 | 0.07421 | 0.074   |
| `ns5b`   | 16  | 534 | 0.07419 | 0.074   |

Mean 0.08233 → 0.082. At A = 0.55 the mean recomputes to 0.08359 → 0.084, as stated. The range
constant d₂ = 2.059 is the standard control-chart value for subgroup size 4. 2.059 × 0.082 = 0.1688
→ 0.169. The ratios 0.175/0.169 = 1.035 and 0.361/0.169 = 2.136 round to the stated 1.04 and 2.14.

Repository quotations all check: mean 0.810 built from 0.944 and 0.703 (`40` §4);
`ctqw_infinite_time_average` on `cb_10` at 0.824 on `hiv_rt` and 0.377 on `ns5b`, quantum
whole-distribution median 0.455 (`40` §6).

#### 17.21 — the two numbers §6 is built on

**Verdict: UNVERIFIABLE. This is the most consequential finding in file 17.**

§6's entire calibration verdict rests on two numbers: a between-target spread of **0.175** for the
classical family and **0.361** for the quantum family. File 17's Method section states that "The only
repository numbers quoted are arm sizes and family-level AUC statistics already published in
`../exploration/results/40-method-sweep.md`."

**Neither number appears in `40-method-sweep.md`.** The file was read end to end. Its family table
(§6) gives, per family, the mean of family bests, the median, the best and the worst — 0.614 / 0.673
/ 0.810 / 0.358 for `baselines` and 0.571 / 0.570 / 0.619 / 0.484 for `quantum`. Neither 0.175 nor
0.361 is derivable from any table in that file, and neither appears in `41`, `44`, `45`, `46` or `47`
either.

Two consequences, and the second is the serious one.

1. **Provenance.** As it stands the two numbers have no traceable source, which violates the
   working agreement's "numbers come from code, never from memory". Either name the file and section
   that publishes them, or compute them in a runner and register it.
2. **Whether the null is the right null.** If 0.175 and 0.361 are spreads of a _family-aggregate_
   AUC — a mean over many scorers within a family, evaluated per arm — then the Hanley–McNeil noise
   floor is the wrong comparator, and wrong in the direction that flatters the verdict. Hanley–McNeil
   gives the sampling error of **one** AUC estimate at those class counts. A mean over dozens of
   correlated scorers has a _smaller_ estimator standard error than any single scorer, so a floor of
   0.169 is too wide, the ratio 1.04 is too small, and "0.175 is typical, and it is weaker evidence
   of a target effect than it looks" is optimistic by an unknown factor. If instead the two numbers
   are single-scorer per-arm spreads, the comparison is sound. **Which of the two it is cannot be
   determined from the document**, and the verdict changes with the answer.

File 17's own recommendation 2 already names the fix — run the matched-patch null draws that
`allo.scoring.score_arm` already generates and record the distribution of the max−min AUC spread over
the four arms. That replaces an analytic floor of uncertain applicability with a
benchmark-specific one, and it should be done before §6's verdict is carried into `docs/report/`.

The classical/quantum ordering §6 argues for does not obviously depend on the floor: the quantum
verdict leans on the below-chance median of 0.455 and the sign-flipping behaviour, both confirmed
independently. It is the _classical_ verdict — "0.175 is typical … nothing is pathological about it"
— that is exposed.

---

### 2.2 File 18

File 18 is the strongest of the three. Every load-bearing citation was retrieved and every quoted
string came back character-for-character. Twenty-one of twenty-five claims are CONFIRMED, one is a
fourth-decimal arithmetic slip with no consequence, and two are qualifications.

#### 18.1–18.4 — the `OPENML-WEKA-2017` scenario

**Verdict: CONFIRMED, every number.** This is described in the brief as the single most decisive
citation in the investigation, so it was checked exhaustively.

Table 2 row, verbatim: `OPENML-WEKA-2017 | Oberon | 30 | 105 | 103 | Quality | 1.02`. The comparison
row is also exact: `CSP-Minizinc-Obj-2016 | Camilla | 8 | 100 | 95 | Quality | 1.7`.

§5.7, verbatim:

> `OPENML-WEKA-2017` was a new scenario in the 2017 competition and appeared to be very challenging,
> as six out of eight submissions performed almost equal to or worse than the single best solver
> (≥95% remaining gap).

Table E.9 on that scenario, all eight values as file 18 prints them: ASAP.v2 0.950, ASAP.v3 0.950,
Sunny-fkvar 0.787, Sunny-autok 0.877, `*Zilla` 1.000, `*Zilla(dyn)` 1.000, `AS-RF` 3.798, `AS-ASL`
7.233. The derived "the best of eight closed 21 %" follows: 1 − 0.787 = 0.213.

**One structural note worth carrying.** The PMLR version of the same table (Table 1 there) marks the
VBS-over-SBS column **`n/a`** for all three quality scenarios and defines it in the caption as
applying "for runtime scenarios" only. The 1.02, 1.04 and 1.7 figures come from the journal version's
Table 2. Both are legitimate; quote the journal version when the quality factors are used, as file 18
does.

#### 18.5, 18.6 — SATzilla07

**Verdict on the counts: CONFIRMED, verbatim**, from §3.1:

> Overall, there were 4 811 instances: 2 300 instances in category `RANDOM`, 1 490 in category
> `HANDMADE` and 1 021 in category `INDUSTRIAL`; of course, category `ALL` included all of these
> instances.

> We randomly split our data set into training, validation and test sets at a ratio of 40:30:30.

Seven component solvers (Table 1) and 48 raw features (§3.3, Figure 2) confirmed.

**Verdict on the derived training-set sizes: OVERSTATED.** File 18 reports "40 % of 4 811 ≈ **1 924**"
and "40 % of 1 021 ≈ **408**" as instance counts trained on. The same paragraph of the source says:

> About 68% of the instances were solved within 1 200 CPU seconds on our reference machine by at
> least one of the seven solvers we used … All instances that were not solved by any of these
> solvers were dropped from our data set.

So the 40:30:30 split is over the data set **after** that drop, roughly 0.68 × 4 811 ≈ 3 270. The
real training sets are about a third smaller than file 18's figures — roughly 1 300 and, for
`INDUSTRIAL`, correspondingly fewer. This changes nothing: the gap to n = 4 remains two orders of
magnitude, and §7's "empirical floor" stands. But the numbers are printed in a table as if exact, so
they should carry the qualification.

#### 18.7, 18.8 — Gupta & Roughgarden

**Verdict: CONFIRMED.** Theorem 3.2 came back with the condition exactly as file 18 quotes it:

> if m ≥ c(H/ϵ)²(d_ℋ + ln(1/δ)) for a suitable constant c (independent of all other parameters)

Corollary 3.4 ("any ERM algorithm (2ϵ,δ)-learns the optimal algorithm in 𝒜 from m samples"),
Theorem 3.6 (`O(log(κβn))`) and Theorem 3.19 (`m = Õ(H³/ϵ²)`) all confirmed. The abstract sentence is
verbatim.

The arithmetic recomputes: ln(1/0.05) = 2.9957 ≈ 3.00; m ≥ 4/ε²; ε = 1.00 at m = 4; m = 400 at
ε = 0.10; m = 1 600 at ε = 0.05.

**The reading is sound and worth defending explicitly**, because it is the kind of argument that
usually goes wrong. File 18 pushes every free quantity in the direction that makes the requirement
_smallest_ (d_ℋ = 1, H = 1, c = 1) and finds the guarantee still vacuous. That is the correct
direction of argument for a "cannot be done" conclusion — an unfavourable reading would prove
nothing. H = 1 is right for a bounded endpoint. The `c ≥ 1` assumption is stated in the document as
an assumption and the sensitivity to it is stated correctly ("raising `c`, `d_ℋ` or `H` can only make
the requirement larger"). The `[UNVERIFIED]` tag on the arithmetic is honest.

#### 18.9 — Balcan, Sandholm & Vitercik

**Verdict: CONFIRMED, verbatim from the abstract**, which is what the `[VERIFIED-ABSTRACT]` tag
claims. All three quoted strings came back exactly:

> we provide the first provable guarantees for portfolio-based algorithm selection

> 1. the learning-theoretic complexity of the algorithm selector, 2) the size of the portfolio, and
> 2. the learning-theoretic complexity of the algorithm's performance as a function of its parameters

> We prove that if the portfolio is large, overfitting is inevitable, even with an extremely simple
> algorithm selector.

> as we increase the portfolio size, we can hope to include a well-suited parameter setting for
> every possible problem instance, but it becomes impossible to avoid overfitting

File 18's own "Could not be reached" section already records that the theorem's dependence on
portfolio size k was not retrieved and that only the qualitative claim is verified. That remains the
correct state.

#### 18.10 — the opposite sign orientations

**Verdict: CONFIRMED, decisively. The claim is right and getting it backwards would indeed invert a
conclusion.**

_Artificial Intelligence_ 272 (2019), §2.4, equation (2):

> m̂_s = (m_s − m_VBS) / (m_SBS − m_VBS) … where 0 corresponds to perfect performance, equivalent to
> the VBS, and 1 corresponds to the performance of the SBS.

PMLR 79:1–7, §2, equation (2) — read directly from the paper's own page:

> (m_SBS − m_s) / (m_SBS − m_VBS)

> In this metric, 1.0 corresponds to a perfect score (i.e. the algorithm selection system always
> selects the best algorithm for each instance and does not generate overhead due to instance feature
> computation) and 0.0 corresponds to the baseline (i.e. the single best solver). A value of less
> than 0.0 indicates that the algorithm selection system is worse than the single best solver, i.e.
> chooses algorithms that perform worse than it.

The numerators are reversed, and both papers are by the same three authors on the same competition.
File 18's §Q3 table transcribes both orientations correctly, including the sign of "worse than SBS"
in each. The instruction to carry the orientation with any quoted number is well founded.

#### 18.11–18.14, 18.18–18.20, 18.24 — the rest of the competitions paper

**Verdict: CONFIRMED, without exception.** All thirteen 2015 scenario rows (Table 1) match file 18's
table on algorithms, instances, features and VBS/SBS factor. All six quoted 2017 rows match Table 2.
Best 2015 system 0.366; best 2017 system 0.38. The PMLR sentences "ranging across different numbers
of algorithms (5-31) and instances (100-9720)" and "the participants had access to performance and
feature data on training instances (2/3), and only the instance features for the test instances
(1/3)" are verbatim, so the derived "smallest training set in the whole competition is about 67
instances" follows.

The three §5 observations that make the scenario a cautionary tale all came back: the plain
random-forest baseline "on 100 randomly sampled 33% holdout sets" that "performed worse than the SBS"
in 18 % of them while achieving 67.5 % remaining gap on the competition split; ASAP.v2's
"actual obtained score (0.025) has a probability of 0.466%" over 1 500 seeds; and the 2015 Friedman
with post-hoc Nemenyi result, verbatim: "there is no statistically significant difference between any
of the submissions". The Fast Downward Stone Soup and auto-sklearn sentences are verbatim.

#### 18.15–18.17 — Demšar

**Verdict: CONFIRMED**, read from the paper's own pages.

§3.2.2, verbatim: "is distributed according to χ²_F with k − 1 degrees of freedom, when N and k are
big enough (as a rule of a thumb, **N > 10 and k > 5**)."

§3.1.2, verbatim: "The second problem with the t-test is that unless the sample size is large enough
(∼ 30 data sets), the paired t-test requires that the differences between the two random variables
compared are distributed normally." and "Therefore, for using the t-test we need normal distributions
because we have small samples, but the small samples also prohibit us from checking the distribution
shape."

Table 3 begins at `#data sets = 5` with `w_0.05 = 5` — a clean sweep — and there is **no column for
N = 4**. File 18's note that this is mildly liberal is also right: the exact two-sided binomial at
5/5 gives 2/2⁵ = 0.0625, above 0.05.

#### 18.21, 18.22 — the derived combinatorics

**Verdict: CONFIRMED except one value.** Recomputed by hand: 2/3! = 0.3333; 2/4! = 0.08333;
2/5! = 0.016667; 2/6! = 0.0027778; 2/7! = 0.00039683. 2/2³ = 0.25; 2/2⁴ = 0.125; 2/2⁵ = 0.0625;
2/2⁶ = 0.03125; 2/2⁷ = 0.015625. E[perfect] = 30 × 2/24 = **2.500**. P(≥1) = 1 − (11/12)³⁰ =
1 − 0.073527 = **0.92647**. Poisson P(X ≤ 1 | λ = 2.5) = e^{−2.5}(1 + 2.5) = 0.082085 × 3.5 =
**0.28720**. Bonferroni: 0.05/30 = 0.0016667, needs n! ≥ 1 200, and 6! = 720 fails while
7! = 5 040 passes, so **n ≥ 7**. Every one of these is correct.

**18.22, WRONG:** `1 − (11/12)¹⁰`. File 18 states **0.5793** in §Q5 and repeats it in the Method
section's list of derived numbers. The correct value is **0.58108**. Worked: (11/12)¹⁰ = 0.4189192,
so 1 − 0.4189192 = 0.5810808. File 18 rounds it to 0.579 in the sentence body, which is also wrong at
the third decimal. The consequence is nil — the point being made is that a smaller effective K lowers
P(≥1) without moving the per-descriptor floor, and 0.581 makes it identically well — but the number
should be corrected in both places.

#### 18.23 — the pre-solving schedule quotation

**Verdict: OVERSTATED.** File 18 quotes §2.3 as "One variant of algorithm schedules are static
(**instance-features free**) pre-solving schedules which are applied before any instance features are
computed". The retrieved text reads "static (**instance-independent**) pre-solving schedules which are
applied before any instance features are computed (Xu et al., 2008)." The substance — static
schedules that need nothing per-instance — is confirmed and is the load-bearing part. The parenthetical
as quoted did not come back. Either it is a version difference between the arXiv and journal texts or
a transcription slip; retrieve it once more before the string is quoted in `docs/report/`.

#### 18.25 — the repository cross-references

**Verdict: CONFIRMED**, all of them, against the files themselves: 1 923 complete variants and 1 620
in the method sweep (`40` §1); 69 scorers (`46` header); 8.86 and 10.58 effective independent
directions over 1 620 variants (`41` §4), which file 18 rounds to "~8.9–10.6"; the minimum detectable
band 0.794–0.955 (`41` §5); the window sweep moving one observable 0.304 → 0.686 on one arm and
0.605 → 0.177 on another (`44` §3); the ensemble raising held-out stability 0.581 → 0.888 at K = 16
with ΔAUC −0.015 and distance correlation 0.496 → 0.613 (`44` §4); the gap clock's 0.079 → 0.045,
0.011 spread move, 8.5× → 14.5× ratio, and zero of 32 settings clearing 0.5 with the best worst-arm
at 0.375 (`44` §6).

---

### 2.3 File 19

#### 19.1, 19.2, 19.3 — Brinda & Vishveshwara

**Verdict on the numbers: CONFIRMED, verbatim.** 232 proteins. "The standard deviation of I_critical
is 0.9 around a mean of ∼3.9". ">85% of the proteins have an I_critical varying between 3.0 and 5.0".
And the size dependence, which is the one file 19 builds an argument on:

> I_critical is a function of the size of the protein and is generally higher for bigger proteins …
> mean I_critical is ∼3.25% in proteins with 100–200 residues, 3.75% in those with 200–300 residues,
> 4.25% in those with 300–400 residues, and >4.25% in those with 400–1300 residues

File 19's "bin means rising from ≈ 3.25 % at 100–200 residues to > 4.25 % at 400–1300 residues" is
exact, and the two intermediate bins it omits are monotone, so the summary is faithful. **The N3
argument holds: a per-protein criterion that itself trends with N has not finished the job.**

**Verdict on the abstract quotation: OVERSTATED.** §Q1.1 puts in quotation marks that the abstract
says the transition occurs "within a narrow cutoff range regardless of protein size". The abstract
reads:

> this transition occurs within a narrow range of interaction cutoff for all the proteins,
> irrespective of the size or the fold topology

The paraphrase is faithful in substance and the point file 19 makes — that the abstract and the full
text pull in opposite directions, and the full text binds — is confirmed and is a good catch. But the
string is not verbatim and carries quotation marks, so it should be re-quoted or unquoted.

#### 19.4, 19.5, 19.6 — Maxwell counting

**Verdict: CONFIRMED as mathematics.** Checked independently rather than sourced, which is the right
treatment for a counting argument.

In d = 3 a network of N point sites has 3N degrees of freedom and, with central-force springs, one
scalar constraint per bond, i.e. N⟨k⟩/2 constraints. Setting these equal to the non-trivial degrees
of freedom 3N − 6 gives ⟨k⟩ = 6 − 12/N, which tends to 6. Dropping the six rigid-body motions gives
the general isostatic coordination z = 2d directly, and z = 6 at d = 3. Both statements in §Q1.2 are
correct.

**The limitation file 19 states is also correct and is the more useful half.** For a scalar operator
there is one degree of freedom per node, so the same counting gives N⟨k⟩/2 = N − 1, i.e.
⟨k⟩ = 2 − 2/N — a tree, exactly as stated, and z = 2d = 2 at d = 1. So an isostatic cutoff rule is
meaningful for a vector ENM and degenerate for a scalar walk. **This is the correct conclusion and it
is derived, not asserted.** Ranking the rule at #7 with "Only meaningful for the vector ENM, not the
scalar walk" is the right treatment.

⟨k⟩/6 recomputes to 1.483–1.717 from the profile's 8.9–10.3, matching the stated 1.48–1.72.

The Micoulaut & Phillips r̄ = 2.4 comparison was not re-retrieved this session and is recorded as
not checked; it is a contrast, not a load-bearing number, and file 19 describes its role correctly
(a bond-bending analogue at a different and lower value).

#### 19.7, 19.8 — GNM and ANM

**Verdict: CONFIRMED, verbatim, and one open flag can now be closed.**

GNM (Bahar, Atilgan & Erman 1997): "≤ 7.0 Å" for alpha-carbon pairs; "A single-parameter harmonic
potential is adopted"; validation on "12 X-ray structures, ranging from a 41 residue subunit to a
633 residue dimer". File 19's table row is faithful on all three.

ANM (Eyal, Yang & Bahar 2006), read from the article page:

> The model that is quite robust to the cutoff distance in the range of 15–24 Å, with a CC between
> experiments and theory of ∼0.54.

> Weighting the interactions improves the correlation gradually up to 0.58 at _P_ = 2.5, approximately.

> The final set includes 176 proteins … all crystal structures with resolution better than 2.5 Å,
> R-factor <0.3 Å and no missing coordinates.

All three numbers file 19 quotes — the 15–24 Å plateau, p = 2.5, and the 176-structure set with its
selection criteria — are confirmed, and the correlation being optimised is against experimental
temperature factors, so the tier (iii) classification "fitted against B-factors" is right.

**File 19's own caveat can be retired.** It records twice that "the Eyal, Yang & Bahar 2006 DOI was
not independently re-derived". It was re-derived this session: `api.crossref.org` returns
doi:10.1093/bioinformatics/btl448 as Eran Eyal, Lee-Wei Yang, Ivet Bahar, "Anisotropic network model:
systematic evaluation and a new web interface", _Bioinformatics_ 22(21):2619–2627, 2006. The DOI
resolves to the paper file 19 cites.

#### 19.9, 19.10 — the B-factor negatives

**Verdict: CONFIRMED, both verbatim.** Fuglebakk, Reuter & Hinsen (doi:10.1021/ct400399x):

> we report large and consistent differences between proposed models

> we find that the models that agree best with B-factors model collective motions less reliably and
> recommend against using B-factors as a benchmark

Hinsen (doi:10.1093/bioinformatics/btm625):

> (1) crystal packing modifies the atomic fluctuations considerably and (2) thermal fluctuations are
> not the dominant contribution to crystallographic Debye-Waller factors

File 19's C2 note on the first is correct and worth keeping: the paper's own reference standard is an
MD covariance, which we may not run, but its negative result _about B-factors_ is a statement about
B-factors and survives the constraint. N2 and the tier (iv) closure both stand.

#### 19.11 — the Guney construction

**Verdict: CONFIRMED, verbatim.** The closest-proximity measure `d_c(S,T) = (1/|T|) Σ_t min_s d(s,t)`,
the z-score `z = (d(S,T) − μ_d(S,T))/σ_d(S,T)`, the reference distribution built by "calculating the
proximity between these two randomly selected groups, a procedure repeated 1,000 times", and the
degree-binning rule, verbatim:

> each bin B_{i,j} was defined as B_{i,j}={u∈V|i≤k_u<j} containing the nodes with degrees i to
> minimum possible j such that ||B_{i,j}||≥100.

The motivating numbers are confirmed: "The mean degree of the targets is k_target=28.6, larger than
the interactome's average degree k=21.2".

**One inference to label as ours, not theirs.** File 19 gives the _reason_ for degree matching as "an
unmatched reference would report proximity that is really hubness". The paper attributes the elevated
target degree to literature bias toward well-characterised drug targets and does not phrase the
consequence that way. The inference is sound and is the right reason to adopt the construction here,
but it is an inference and should be tagged as one rather than folded into the `[VERIFIED-FULLTEXT]`
sentence. The two caveats file 19 already attaches — that our sources are far smaller than a
100-node bin supports, and that the per-residue mean is a burial surrogate that will remove part of
the distance signal — are the right ones.

#### 19.12 — the mutual-information cutoff

**Verdict: CONFIRMED.** doi:10.1002/prot.26154 resolves to Sobieraj & Setny, "Entropy-based distance
cutoff for protein internal contact networks", _Proteins_ 89:1333–1339, 2021. The retrieved record
confirms both halves of file 19's use: that "mutual information reaches its minimum universally at a
5 Å cutoff length across all tested proteins, independent of the probability threshold applied", and
that the contact-formation probabilities come from molecular dynamics simulations — so the C2 note in
§Q1.3 ("running the criterion ourselves is a C2 violation; inheriting the constant is not") is
correct and is a real addition over `13-graph-construction.md`'s use of the same paper.

#### 19.13 — derived result (a): rank invariance

**Verdict: CONFIRMED as mathematics, under two conditions the document states more loosely than it
should.**

The result holds. AUC-ROC is a functional of the ranking alone: it is the Mann–Whitney statistic,
`P(s⁺ > s⁻) + ½·P(s⁺ = s⁻)`. A **strictly increasing** map applied to the whole score vector of one
protein preserves both the strict ordering and the tie pattern, so the AUC is unchanged exactly, not
approximately. Rank correlations and the top-k set follow for the same reason. The three-way
classification in §1.1 — uniform monotone maps are no-ops, per-residue maps are not, operator/strata
changes are not — is correct, and the observation that the screen "kills most of the size-normalisation
literature as a _method_ change while leaving it fully relevant to _reporting_" is the right
consequence. §Q2's table and the S10 recommendation follow correctly from it.

**Condition 1 — "affine" must mean "affine with positive slope".** §1.1 says "If `φ_p` is a scalar
affine or monotone map". An affine map with negative slope is scalar and affine and it sends AUC to
**1 − AUC**. This is not hypothetical in this repository: `47-quantum-constructions.md` §4 discusses
negating `energy_contrast`, whose AUC of 0.360 would read 0.640 — and correctly refuses it as a
sign chosen after seeing labels. The screen as worded would classify that negation as a no-op. Say
"strictly increasing" throughout, as the opening sentence of §1.1 in fact does, and drop "affine".

**Condition 2 — `log s` needs s > 0.** It is listed as an example. Our scores are not all positive:
every detrended score in the sweep is a residual, and `40-method-sweep.md` §5 makes detrending the
highest-leverage stage in the pipeline. On a signed vector `log s` is undefined, not monotone. Replace
the example or restrict it.

**Condition 3 — weakly monotone maps.** Any map that is constant on an interval (rounding, clipping,
quantisation) creates ties, and ties move AUC by ½ per tied pair and can change the top-5 set. Not a
realistic normalisation here, but the screen should say "strictly" for the same reason as condition 1.

None of these three overturns any conclusion in file 19. All three are cases the screen as written
would wave through.

#### 19.14 — derived result (b): the sensitivity bound

**Verdict: CONFIRMED. The bound is correct, and it is tight for the range statistic.**

Restated: let `A(p,θ)` be the endpoint on protein p at hyperparameter θ, let a derived rule replace a
fixed θ₀ with θ*(p), and let `R = max_p sup_θ |A(p,θ) − A(p,θ₀)|` over the reachable θ. Then any
spread statistic moves by at most about 2R.

Proof for the **range** `S = max_p A(p,·) − min_p A(p,·)`. For every p, `A(p,θ*(p))` lies within R of
`A(p,θ₀)`. Hence `max_p A(p,θ*) ∈ [max_p A(p,θ₀) − R, max_p A(p,θ₀) + R]` and likewise for the
minimum. Subtracting, `S* ∈ [S₀ − 2R, S₀ + 2R]`, so `|S* − S₀| ≤ 2R`. The bound is attained when the
rule pushes the maximum arm down by R and the minimum arm up by R, so it is **tight**, not merely
sufficient. "At most about 2·R_within" is right, and the hedge "about" is not needed.

Two extensions worth recording because they strengthen the screen:

- **For the standard deviation the constant is R, not 2R.** The sample SD is `‖x − x̄1‖₂/√P`, and by
  the reverse triangle inequality `|sd(x) − sd(y)| ≤ ‖x − y‖₂/√P ≤ ‖x − y‖_∞ = R`. So the bound
  quoted covers SD with a factor of two to spare.
- **For the worst-arm endpoint the constant is also R**, directly.
- _*The bound holds for any selection rule θ*(p), including an oracle that reads the labels._* Nothing
  in the argument uses how θ* is chosen. That is the strongest form of the result and file 19 does not
  say it: even a perfect per-protein clock, chosen with full knowledge of the answer, cannot reduce
  the between-arm range by more than 2·R_within. That is a much sharper pre-screen than "a derived
  rule cannot".

**One condition that does bind, and it is about the number rather than the theorem.** R is defined as
a supremum over the reachable θ. The value plugged in, `R_within = 0.079` for `ctqw_average_transfer`,
is the maximum over the **five sampled windows** {5, 10, 25, 50, 100} in `44-stability-and-noise.md`
§3, not over the continuum. A maximum over a five-point grid is a **lower bound** on the supremum, so
`2R ≈ 0.16` is an estimate of the ceiling and not a proven one. The direction of the error is against
the argument: the true ceiling may be higher than 0.16. It is still nowhere near the 0.49–0.67 spread
the rule would have to close, so the conclusion is safe by a wide margin — but §1.2's operational
instruction ("measure R_within") should say _over the reachable range, densely enough that the grid
is not the binding constraint_.

The other stated condition is correct and important: the bound applies only to rules that slide θ.
§1.1's other two classes — per-residue maps and strata changes — are outside it by construction, which
is exactly why candidates 1, 2 and 5 in the §7 ranking are not covered by it.

#### 19.15 — the worked example

**Verdict: OVERSTATED, on scope rather than on arithmetic.** §1.2 reads: "`R_within` for
`ctqw_average_transfer` under the `range` clock is 0.079 AUC; the between-arm spread is 0.668. The
bound permits at most ≈ 0.16 of spread reduction; the measured reduction was 0.011."

Three numbers, two statistics. The 0.079 and 0.668 are both specific to `ctqw_average_transfer`
(`44` §6's variance-decomposition table). The 0.011 is the **mean between-arm AUC spread across all
four observables** (0.5627 → 0.5516, `44` §6's clock table). The observable-specific reduction from
the same table is 0.668 → 0.650, i.e. **0.018**. Both 0.011 and 0.018 sit far inside the 0.16 bound,
so the example validates the bound whichever is used — but the sentence should not mix them, and N1
in §Q6 mixes them the same way.

`2 × 0.079 = 0.158 ≈ 0.16` is correct.

#### 19.16 — the internal fact-check

**Verdict: CONFIRMED, and it is the right thing to have done.** §Q6's closing paragraph flags that the
21.7× gap figure comes from `47` §1 while `44` §6's own gap column implies a different ratio.
Recomputed: `47` §1 gives gaps 1.6244 and 0.0748, ratio **21.72**; `44` §6 gives 2.47385 and 0.01766,
ratio **140.1**; `44` §6's spectral-range column gives 21.631 and 17.968, ratio **1.204** against the
1.09 quoted in prose. All three of file 19's arithmetic statements are right, the diagnosis (the two
tables report the gap of different operators) is plausible, and declining to reconcile them while
recording the discrepancy is the correct call. No conclusion in file 19 turns on which is used.

#### 19.17 — the repository quotations

**Verdict: CONFIRMED**, all recomputed from `30-frozen-graph-profile.md`, `44` and `45`.

The near-universality figures are exact: mean contact number 8.9–10.3, clustering 0.460–0.515, λ₁
10.40–11.80, across a 7.2× size range, and the quoted sentence "A residue contact graph at a fixed
cutoff is a near-universal object". The connectivity facts are verbatim: "Every graph is connected.
One component on all fourteen" and "No isolated residue exists at the frozen cutoff". The
source-geometry ranges are exact: source size 3 to 61 (20×), median candidate-to-source distance
7.6 Å to 23.9 Å (3.1×), fraction within 10 Å 0.12 to 0.69, source mean relative solvent accessibility
0.017 to 0.268. The Laplacian condition number range 33 to 920 is exact.

The §Q2 diameter ÷ N^{1/3} table was recomputed cell by cell and every one of the eight values is
right to two decimals: 1.33, 1.45, 1.54, 1.50, 1.46, 1.69, 2.70, 2.41. The compactness conclusion —
globular arms in a 1.3–1.7 band, elongated multi-domain arms at 2.4–2.7 — follows.

The `45-source-choice.md` figures are exact: the catalytic source has the largest between-arm AUC
spread of any source tested at 0.486, against 0.109 for a size-matched random source.

**One inferential step to label.** §Q3.4 argues that a source-geometry clock "equalises a quantity the
endpoint demonstrably does depend on", citing the 0.486-vs-0.109 result. That result shows the
endpoint depends on **which residues** form the source; it does not by itself show the endpoint
depends on the **median candidate-to-source distance** `d̃`, which is the quantity the proposed clock
would equalise. The gap between those two is exactly what §1.2's own pre-screen exists to measure, and
§7's falsifier for candidate 3 correctly says to run the pre-screen first. The claim is adequately
hedged in §7 and slightly over-stated in §Q3.4.

#### 19.18 — the effective-resistance figure

**Verdict: UNVERIFIABLE.** §7's per-candidate falsifier 4 states "`effective_resistance_to_source`
already scores best 0.721 in the battery". No file is named. The figure does not appear in
`40-method-sweep.md`, `41-selection-and-power.md`, `44-stability-and-noise.md`,
`45-source-choice.md`, `46-beats-distance.md` or `47-quantum-constructions.md`. Name the source or
drop the number; nothing in the ranking depends on it, since candidate 4 is already excluded from the
primary endpoint by the §1.1 screen.

---

## 3. What this changes for our pipeline

- **File 17, §6 and the report (stage S8/S10) — blocked until 17.21 is resolved.** The two spread
  figures 0.175 and 0.361 have no traceable source, and whether the Hanley–McNeil floor is the right
  null depends on which statistic they are. Do not carry §6's "0.175 is typical" verdict into
  `docs/report/` until either (a) the numbers are traced to a published table, or (b) file 17's own
  recommendation 2 is executed — record the distribution of the max−min AUC spread over the four arms
  from the matched-patch null draws `score_arm` already generates, and calibrate against that. The
  quantum verdict is not exposed in the same way; it rests on the below-chance median of 0.455 and the
  sign-flipping behaviour, both independently confirmed.
- **File 17, §Q1 and the "does NOT support" list.** Add Utgés & Barton
  (doi:10.1186/s13321-024-00923-z) and delete "only" from both places. It is a second and much larger
  precedent for macro-averaging per target — 2 775 chains — which strengthens recommendation 1 rather
  than weakening it. Add the LIGYSIS benchmark to the comparator vocabulary in `docs/report/`.
- **File 17, §6, one word.** "Nobody publishes" must become "not retrieved by the recorded search",
  per ADR 0019 and per file 17's own §Q2.
- **File 17, the CASP9 quotation.** Restore "in combination with a strong influence by the small and
  biased target data set". It changes what the assessment is being cited for, and a reviewer who opens
  the reference will find the clause.
- **File 18 — no change required to any conclusion.** The four floors in §7 are each independently
  confirmed at the source. Fix `1 − (11/12)¹⁰` to 0.5811 in two places, add the "unsolved instances
  were dropped" qualification to the SATzilla row, and re-retrieve the pre-solving-schedule
  parenthetical before it is quoted in the report. §7's verdict — no fitted per-protein selector at
  n = 4 — stands as written.
- **File 18's cheapest experiment stands and should be run first.** Compute SBS, VBS and the
  normalised gap on the four `development` arms. The orientation trap is real and now verified at both
  sources; whichever equation is adopted, state it beside the number.
- **File 19, §1.1 — tighten the screen before it is used as policy.** It is proposed as a standing
  filter on every future normalisation ("Method-selection policy"). As worded it would pass an affine
  map with negative slope, which reverses the AUC, and it lists `log s` on score vectors that are
  signed after detrending. Say "strictly increasing" and drop "affine".
- **File 19, §1.2 — the bound is stronger than stated and should be quoted that way.** It holds for
  any θ-selection rule including an oracle, and the constant is R rather than 2R for the standard
  deviation and for the worst-arm endpoint. State the oracle form: it turns the pre-screen from
  "a derived rule cannot recover the spread" into "no clock can", which closes candidate 3 far more
  cheaply if `R_within` is small. When measuring `R_within`, sample θ densely enough that the grid is
  not the binding constraint — the 0.079 currently used is a five-point maximum, hence a lower bound.
- **File 19 — one caveat can be retired and one added.** The Eyal, Yang & Bahar DOI is confirmed to
  resolve to the cited paper, so the "not independently re-derived" flag can go. The Guney rationale
  ("proximity that is really hubness") is our inference and should be tagged as one.
- **All three files.** Nine quoted strings across the three files are paraphrases carrying quotation
  marks (17.17, 18.23, 19.3 and the Guney rationale among them). None changes a conclusion. The
  pattern is worth naming because `00-conventions.md` §2's tags are read as a promise that a quoted
  string came back verbatim, and a reader who opens one reference and finds a paraphrase will discount
  the rest.

---

## 4. Method

**Databases and routes.** ar5iv (`ar5iv.labs.arxiv.org/html/{id}`); the arXiv API
(`export.arxiv.org/api/query?id_list=`); PMC article pages
(`pmc.ncbi.nlm.nih.gov/articles/{PMCID}/`); PubMed E-utilities `efetch.fcgi` and `esearch.fcgi`;
Europe PMC REST search (`www.ebi.ac.uk/europepmc/webservices/rest/search`, `format=json`, with and
without `resultType=core`); Crossref REST (`api.crossref.org/works/{DOI}`); PMLR
(`proceedings.mlr.press`); JMLR (`www.jmlr.org`); OUP (`academic.oup.com`).

**WebSearch was unavailable for this session** — the 200-call budget was already exhausted when the
pass began — so every retrieval went through the direct-fetch endpoints listed in
`00-conventions.md` §3, exactly as `10a-fact-check.md` had to. Europe PMC REST search worked
throughout, contrary to the outage `14-distance-confound.md` records.

**PDF handling, which is what made this pass possible where `18-selection-sample-complexity.md` had to
work around it.** Three PDFs — PMLR 79:1–7, arXiv:1111.2249 and Demšar's JMLR paper — returned
unusable text through the HTML converter, the same failure file 18's Method section records for all
eight of its PDFs. Each fetch nonetheless writes the binary to a local path, and reading that file
with an explicit page range renders the pages directly. All three were read that way: PMLR pages 1–7,
SATzilla pages 9–14 (§§3.1–3.8), Demšar pages 5–12 (§§3.1–3.2, Tables 3–5). **Record this route as
working**; it removes the constraint that produced file 18's three dropped sources.

**Independent searches for the file 17 negative claim.** Four Europe PMC queries, chosen to be
different from the twelve file 17 records, and specifically aimed at finding a counter-example rather
than confirming the absence. Listed with hit counts in §2.1 under 17.1. 82 records screened, 0
counter-examples, 2 near misses followed to full text.

**Counts.** 65 claims screened in. 31 document fetches. 3 PDFs read page-by-page over 3 page-range
reads. 8 repository files read in full (`30-frozen-graph-profile.md`, `40-method-sweep.md`,
`41-selection-and-power.md`, `44-stability-and-noise.md`, `45-source-choice.md`,
`46-beats-distance.md`, `47-quantum-constructions.md`, plus `00-conventions.md` and
`10a-fact-check.md`). 4 Europe PMC searches, 82 records screened. 2 DOIs resolved through Crossref,
both returning the cited work.

**Arithmetic performed by hand and stated so it can be re-checked.** The four Hanley–McNeil standard
errors at A = 0.70 and at A = 0.55 and their means; 2.059 × 0.082; the two ratios 1.035 and 2.136;
(11/12)³⁰ and (11/12)¹⁰ by repeated squaring; e^{−2.5}(1 + 2.5); 2/n! and 2/2ⁿ for n = 3…7; the
Bonferroni threshold and the n! it requires; 4/ε² at ε ∈ {1, 0.10, 0.05}; the eight diameter ÷ N^{1/3}
values; 8.9/6 and 10.3/6; 1.6244/0.0748, 2.47385/0.01766 and 21.631/17.968; 23.9/7.6; 81.2 − 68.6,
74.9 − 72.0, 52.4 − 45.6, 0.975 − 0.676, 0.749 − 0.077, 0.968 − 0.676, 0.629 − 0.077; 1 − 0.787;
0.4 × 1 021 and 0.4 × 4 811.

**Proofs performed rather than retrieved.** The rank-invariance of the Mann–Whitney form of AUC under
a strictly increasing map, and the three conditions under which it fails (negative slope, non-positive
domain, tie creation). The `2·R_within` range bound and its tightness, the `R` bound for the standard
deviation via the reverse triangle inequality on `‖x − x̄1‖₂/√P`, the `R` bound for the worst-arm
endpoint, and the observation that none of the three uses how θ* is selected. Maxwell counting at
d = 3 and d = 1.

**What could not be reached.**

- `nature.com` and `link.springer.com` were not attempted; every needed article was on PMC.
- The verbatim CryptoSite sentence giving the leave-one-out training-set size. One retrieval returns
  84; file 17 states 79. Unresolved (17.8).
- The CryptoSite quotation "large and hydrophobic ligand binds to a cryptic site" did not come back
  from the PMC full text this session. Recorded as not re-retrieved, not as false.
- The exact parenthetical in the pre-solving-schedule sentence, `doi:10.1016/j.artint.2018.10.004`
  §2.3. The retrieved text reads "(instance-independent)" where file 18 quotes "(instance-features
  free)". One more retrieval against the journal version would settle whether this is a version
  difference (18.23).
- Micoulaut & Phillips, arXiv:cond-mat/0210100 — the r̄ = 2.4 figure was not re-retrieved. It is a
  contrast in file 19, not load-bearing.
- Several file 17 sources cited for numbers no decision rests on were not re-retrieved: AlloPred
  (doi:10.1186/s12859-015-0771-1), Ohm (doi:10.1038/s41467-020-17618-2), PASSer
  (doi:10.1093/nar/gkad303), PASSerRank (doi:10.1002/jcc.27193), STINGAllo (doi:10.1093/bib/bbaf424),
  bond-to-bond propensity (doi:10.1016/j.patter.2021.100408), AlloDyn
  (doi:10.64898/2026.05.22.727284), CryptoBank (doi:10.1126/sciadv.ady6364). Their internal arithmetic
  was checked where file 17 prints both a fraction and a percentage (92/104 = 88.5 %, 10/40 = 25 %,
  23/40 − 10/40 = 32.5 points) and all of it holds.
- File 19's rigidity sources (doi:10.1002/prot.1081, doi:10.1073/pnas.062492699, arXiv:0810.1833) were
  not re-retrieved; file 19 already flags the provenance of the first.

**Stopping rule.** For each priority claim: stop once the quoted string or the numeric table cell came
back from the primary source and its stated conditions were recorded. For the two derived results in
file 19: stop once the statement was proved or a counter-example was constructed. For the file 17
negative claim: stop after four independent queries across Europe PMC returned no paper reporting a
between-target standard deviation of AUC, and after the two nearest candidates had been followed to
full text and characterised.

**Leakage guard.** No file under `docs/benchmark/evaluation/` was opened. Neither `frozen.json`,
neither `manifest.yaml`, not `selection.json`, not `extension-candidates.md`. No result for any
`generalisation`-tier arm is reported anywhere in this file: the only per-arm repository numbers
quoted are for `mkp5`, `ptp1b`, `hiv_rt`, `ns5b` and the primary arms, and the fourteen-graph
aggregates are quoted only as aggregates, from `30-frozen-graph-profile.md`, which is label-free and
apo-only. No real label residue is named.
