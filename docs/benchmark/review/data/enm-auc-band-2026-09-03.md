# Verification of the "AUC 0.75–0.82" band for the ENM / network-communication family

**Scope:** verifies the two data points the band rests on, then widens the search to any
elastic-network, normal-mode, perturbation-response-scanning, network-centrality or
communication-pathway method for allosteric site/residue prediction that reports AUC-ROC.
Excludes: MD-based cryptic-site methods, pathogenicity/variant predictors, and pure
sequence/pLM methods except where needed as contrast.
**Retrieved:** 2026-09-03.
**Evidence tags:** `[VERIFIED-FULLTEXT]`, `[VERIFIED-ABSTRACT]`, `[UNVERIFIED]`.

---

## 1. Verdict on the two data points

### 1.1 ZHMolEReP — **CONFIRMED (abstract), with one unresolved qualifier**

**Citation.** Ke X, Liu H, Wang J, Guo W, Feng H, Zhao Y. _ZHMolEReP: An Energy Response
Strategy for Protein Allosteric Site Prediction._ J Chem Inf Model. 2026 May 25;66(10):
6181–6195. doi:10.1021/acs.jcim.6c00141. PMID 42102115. `[VERIFIED-ABSTRACT]`

**DOI resolves.** Yes. The DOI, journal, volume, issue and page range are as claimed.
Record retrieved via NCBI E-utilities `efetch`. `[VERIFIED-ABSTRACT]`

**The numbers.** All three claimed figures are verbatim in the published abstract:

> On the ASBench benchmark data set, ZHMolEReP outperforms existing methods, achieving a
> recall of 0.7037, an AUC of 0.7858, and successfully identifying allosteric sites in 33 out
> of 40 proteins, representing increases of 141.8%, 35.4%, and 26.9% over baseline methods.

AUC 0.7858 — confirmed. Recall 0.7037 — confirmed. 33 of 40 proteins — confirmed.
Benchmark ASBench — confirmed. `[VERIFIED-ABSTRACT]`

**Endpoint.** Residue-level, not pocket-level. The abstract calls it "a residue-level
allosteric site prediction tool". `[VERIFIED-ABSTRACT]`

**Unresolved: is it AUC-ROC or area under a precision–recall curve?** The abstract says only
"an AUC of 0.7858". **The full text is paywalled** — `pubs.acs.org/doi/10.1021/acs.jcim.6c00141`
and the `article-abstract` landing page both returned HTTP 403. No open version, preprint or
PMC deposit was located. `[UNVERIFIED]`

_Inference, not evidence:_ the abstract's own "+35.4%" implies a baseline of 0.7858/1.354 ≈ 0.58.
A ~0.58 baseline is a characteristic weak-but-above-random **ROC** value; under a
precision–recall AUC on a residue task with a few per cent positives, a 0.58 baseline would be
implausible. This makes ROC the strong reading, but it is arithmetic on the abstract, not a
sentence anyone read. Do not promote it to `[VERIFIED]`.

**Family caveat — this matters more than the number.** ZHMolEReP is _not_ an elastic-network
propagation method whose observable is scored. It is a **supervised machine-learning
classifier** over "a concise and physically grounded seven-feature representation" that
"integrates perturbation response scanning (PRS) with free energy response approximation",
tuned with ablation and SHAP analysis. PRS is an ENM technique, so the method is ENM-_derived_;
the AUC is the classifier's, not an ENM observable's. `[VERIFIED-ABSTRACT]`

### 1.2 "Coupling dynamics and evolutionary information…" (AR-Pred) — **CONFIRMED, with a material correction to what the number means**

**Full citation and DOI (the task asked for these).** Mishra SK, Kandoi G, Jernigan RL.
_Coupling dynamics and evolutionary information with structure to identify protein regulatory
and functional binding sites._ Proteins. 2019 Oct;87(10):850–868. **doi:10.1002/prot.25749**.
PMID 31141211. PMCID PMC6718341. Method name: **AR-Pred** (Active and Regulatory site
Prediction). `[VERIFIED-ABSTRACT]`

**The number.** Confirmed verbatim in the abstract:

> Our models for active site prediction yield a median area under the curve (AUC) of 91% and
> Matthews correlation coefficient (MCC) of 0.68, whereas the less well-defined allosteric
> sites are predicted at a lower level with a median AUC of 80% and MCC of 0.48.

So median AUC = 80% for allosteric sites. The claimed "about 0.80" is right. `[VERIFIED-ABSTRACT]`

**What it is an AUC of — three qualifications, all load-bearing.**

1. **ROC, and over residues.** It is a ROC AUC over residues (allosteric vs non-allosteric),
   not over pockets. `[VERIFIED-FULLTEXT]`
2. **It is a _validation-set_ median, on _balanced_ sets — not an independent-test number.**
   The paper builds "10 balanced training and validation sets" per prediction class and reports
   the median of the ten models. The natural class ratio is far from balanced: the paper's own
   residue counts are "167 allosteric, 6607 non-allosteric". A balanced-set AUC is not
   comparable to an AUC computed on a whole protein at natural prevalence — which is what this
   project's harness computes. `[VERIFIED-FULLTEXT]`
3. **The independent test set carries no AUC at all.** On the independent set (15 proteins for
   allosteric), the paper reports percentages of proteins where AR-Pred matched or beat other
   methods on true positives at various thresholds — no AUC. `[VERIFIED-FULLTEXT]`

**Family caveat.** As with ZHMolEReP: AR-Pred is a **random-forest classifier**. Its dynamics
features come from "the Anisotropic Network Model (ANM), a type of Elastic Network Model
(ENM)" — mean-squared fluctuations, a dynamic flexibility index, and a shortest dynamically
correlated path to the active site — but they sit alongside geometric, evolutionary and
physicochemical features. "ENM-adjacent" is fair; "elastic-network method" is not.
`[VERIFIED-FULLTEXT]`

---

## 2. Task 2 — does the rest of the family report AUC?

### 2.1 The repository's claim is correct. Verified method by method.

Every method named in the repo's claim was checked in **full text** for the strings "AUC",
"ROC" and "area under". None reports one.

| Method                                         | Family                      | AUC?     | What it reports instead                                                                                                                                     | Source                                     | Grade                 |
| ---------------------------------------------- | --------------------------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------ | --------------------- |
| **AlloPred** (Greener & Sternberg 2015)        | NMA/ENM pocket perturbation | **None** | "AlloPred ranked an allosteric pocket top for 23 out of 40 known allosteric proteins"; 28/40 in top 2. Test set 40 proteins from ASBench-derived set of 119 | doi:10.1186/s12859-015-0771-1, PMC4619270  | `[VERIFIED-FULLTEXT]` |
| **PARS** precursor (Panjkovich & Daura 2012)   | NMA flexibility             | **None** | PPV/sensitivity: best set c1FS = 65% PPV, 0.22 sensitivity; 58 proteins                                                                                     | doi:10.1186/1471-2105-13-273, PMC3562710   | `[VERIFIED-FULLTEXT]` |
| **Ohm** (Wang et al. 2020)                     | network communication       | **None** | Average TPR 0.57, PPV 0.72 on 20 proteins (vs Amor 0.23 / 0.48)                                                                                             | doi:10.1038/s41467-020-17618-2, PMC7395124 | `[VERIFIED-FULLTEXT]` |
| **Bond-to-bond propensity** (Amor et al. 2016) | network propensity          | **None** | Quantile scores + Wilcoxon p-values; site detected by ≥1 of 4 measures in 19/20 proteins, by ≥3 of 4 in 15/20                                               | doi:10.1038/ncomms12477, PMC5007447        | `[VERIFIED-FULLTEXT]` |
| **ESSA** (Kaynak, Bahar, Doruker 2020)         | ENM essential-site scanning | **None** | z-scores + success rate: 10/14 holo, **7/14 apo**; 14 sites across 12 proteins                                                                              | doi:10.1016/j.csbj.2020.06.020, PMC7330491 | `[VERIFIED-FULLTEXT]` |
| **STRESS** (Clarke et al. 2016)                | binding leverage / dynamics | **None** | 55.6% average identification of known binding sites over 12 canonical proteins; ConSurf conservation contrasts with Wilcoxon p-values                       | doi:10.1016/j.str.2016.03.008, PMC4883016  | `[VERIFIED-FULLTEXT]` |

**The strongest single piece of evidence is the family's own comparative benchmark.**
Wu N, Strömich L, Yaliraki SN. _Prediction of allosteric sites and signaling: insights from
benchmarking datasets._ Patterns. 2021;3(1):100408. doi:10.1016/j.patter.2021.100408,
PMC8767309. It benchmarks **five** methods of exactly this family — bond-to-bond propensity,
AllositePro, AlloPred, PARS and SBSMMA — across ASBench (118 structures / 113 proteins) and
CASBench (314 structures / 33 proteins), 432 structures from 146 proteins combined. It reports
**no AUC or ROC anywhere**; it uses six quantile-score statistics and success-rate percentages.
`[VERIFIED-FULLTEXT]`

Also checked, no AUC in abstract: **AllositePro** (Song et al. 2017, doi:10.1021/acs.jcim.7b00014,
PMID 28825477 — abstract states only "superior to that of the other currently available methods",
no numbers); **SBSMMA** (Guarnera & Berezovsky 2016, doi:10.1371/journal.pcbi.1004678);
**AlloSigMA 2** (Tan et al. 2020, doi:10.1093/nar/gkaa338). `[VERIFIED-ABSTRACT]`

### 2.2 Every AUC I could verify for allosteric site/residue prediction

| #   | Method                              | AUC                             | Over what    | Benchmark & size                                                                        | ENM / network content?                                | DOI                                  | Grade                                                             |
| --- | ----------------------------------- | ------------------------------- | ------------ | --------------------------------------------------------------------------------------- | ----------------------------------------------------- | ------------------------------------ | ----------------------------------------------------------------- |
| 1   | **ZHMolEReP**                       | **0.7858**                      | residues     | ASBench, 40 proteins                                                                    | PRS features inside a 7-feature supervised model      | 10.1021/acs.jcim.6c00141             | `[VERIFIED-ABSTRACT]` (full text paywalled, ROC vs PR unresolved) |
| 2   | **AR-Pred**, allosteric             | **0.80** (median)               | residues     | 10 **balanced** validation sets; 167 pos / 6607 neg residues; 144 monomers total        | ANM/ENM features inside a random forest               | 10.1002/prot.25749                   | `[VERIFIED-FULLTEXT]`                                             |
| 3   | AR-Pred, **active site** (contrast) | **0.91** (median)               | residues     | same balanced-set protocol                                                              | same                                                  | 10.1002/prot.25749                   | `[VERIFIED-ABSTRACT]`                                             |
| 4   | **MEF-AlloSite**                    | **0.82**, 0.80, 0.803 (3 tests) | **pockets**  | Test1 56 prot/1510 pockets; Test2 56 prot/2471; Test3 122 prot/6384                     | **None** — Fpocket + physicochemical descriptors only | 10.1186/s13321-024-00882-5           | `[VERIFIED-FULLTEXT]`                                             |
| 5   | **AlloPED-pocket**                  | **0.920**                       | **pockets**  | train ASBench 146 proteins; test AllositePro set, 24 proteins, 53 pos / 745 neg pockets | **None** — ensemble ML on physicochemical features    | 10.1101/2025.03.28.645953 (preprint) | `[VERIFIED-FULLTEXT]` (preprint)                                  |
| 6   | **AlloPED-site**                    | **0.563**                       | **residues** | same 24-protein test set, 555 allosteric residues in 53 pockets                         | ProtT5 pLM embeddings + structure                     | 10.1101/2025.03.28.645953 (preprint) | `[VERIFIED-FULLTEXT]` (preprint)                                  |

**Row 5 vs row 6 is the most important finding in this table.** They are the _same paper_, the
_same test set_, the _same authors_. Pocket-level AUC 0.920; residue-level AUC 0.563. An AUC in
this field is close to meaningless without its endpoint attached. Any comparison that mixes
pocket-level and residue-level AUCs is measuring the endpoint, not the method.

### 2.3 Near-misses, recorded so they are not re-searched

- **AllosES** (Hu et al. 2024, doi:10.1021/acs.jcim.4c00544, PMID 39075972) — transfer-entropy
  dynamics + evolutionary info, ensemble ML. **Reports no AUC in its abstract**: MCC 0.556 on
  independent test set D24, and top-3 ranking for 83.3%/89.3% of proteins on D24/D28.
  `[VERIFIED-ABSTRACT]`
  **Correction to a live error:** a search-result summary attributed "AUC 0.920, MCC 0.544" to
  AllosES. That is wrong. The primary record gives AllosES MCC **0.556**; the 0.920/0.544 pair
  belongs to **AlloPED-pocket** (row 5). This is the same failure mode that produced the
  unverified band — do not propagate it.
- **AlloEF** (Zhang et al. 2026, J Phys Chem B 130(19):4970–4981,
  doi:10.1021/acs.jpcb.6c00242, PMID 42053346) — transfer entropy + energetic frustration +
  network topology features, soft-voting ensemble. **No AUC**: F1 0.630, MCC 0.609.
  `[VERIFIED-ABSTRACT]`
- **STINGAllo** (Omage et al. 2025, doi:10.1093/bib/bbaf424, PMC12368853) — **no AUC**;
  78% DCC success, F1 0.64, MCC 0.64. No ENM/NMA content. `[VERIFIED-FULLTEXT]`
- **CrypTothML** (doi:10.3390/ijms26104710) reports AUC-ROC 0.88, but it is a **cryptic-site**
  method built on mixed-solvent MD. Wrong endpoint (cryptic ≠ allosteric) and it violates C2.
  `[VERIFIED-ABSTRACT]`
- ENM-based predictors _do_ routinely report AUC for a **different endpoint** — missense-variant
  pathogenicity (e.g. Ponzoni & Bahar, doi:10.1073/pnas.1715896115). Not allosteric site
  prediction; excluded.

### 2.4 A negative result about the search itself

Two Europe PMC `FULL_TEXT:` queries returned zero hits. **Those nulls are worthless**: a control
query, `FULL_TEXT:"allosteric site" AND FULL_TEXT:"AUC"`, also returned `hitCount: 0`, which
cannot be true. The `FULL_TEXT:` field is not functioning on that REST endpoint. No
absence-of-prior-art conclusion may be drawn from those two searches, and none is drawn here.
Coverage of the family rests on the per-paper full-text reads in §2.1, not on a negative search.

---

## 3. What the band actually is

**The band's two endpoints are real. Its label is wrong.**

1. **Both data points verify.** 0.7858 and 0.80 are correctly transcribed from the primary
   sources. Neither is a fabrication and neither needs correcting. To that extent the band
   "0.75–0.82" is honestly derived from its two inputs.

2. **But neither data point belongs to the family the sentence names.** The claim says
   "the elastic-network and network-communication family". Both points are **supervised machine
   learning classifiers that consume ENM-derived features among others** — a random forest
   (AR-Pred) and a seven-feature model with SHAP-analysed ablations (ZHMolEReP). **Zero** of the
   two are unsupervised elastic-network or network-communication methods of the kind this
   project builds. The correct label is: _"supervised residue-level classifiers with
   dynamics-derived features report AUC ≈ 0.79–0.80."_

3. **The actual ENM / network-communication family does not report AUC.** Six canonical methods
   — AlloPred, PARS, Ohm, bond-to-bond propensity, ESSA, STRESS — report none, verified in full
   text. The family's own five-method comparative benchmark across 432 structures reports none.
   The repository's statement that this family reports top-N, TPR/PPV, quantile scores and
   z-score enrichment instead is **confirmed on every method named**.

4. **How many independent data points support the band as written: two — and they are not
   independent in the way that matters.** Both are supervised classifiers, both residue-level,
   both trained on ASBench-family data, and one of the two (AR-Pred's 0.80) is a **median over
   balanced validation sets**, not a test-set number at natural prevalence. AR-Pred's
   independent test set carries no AUC at all. So the band rests on **one** paywalled
   test-set-like AUC of uncertain type (ROC or PR), plus **one** balanced-validation median.

5. **Widening does not produce a band, it produces a spread governed by the endpoint.** Verified
   allosteric AUCs run 0.563 to 0.920. That range is not explained by method quality: it is
   explained by whether you score residues (0.563, 0.7858, 0.80) or pockets (0.80–0.82, 0.920).

**The honest statement.** _The elastic-network and network-communication family does not report
AUC often enough to define a band. Six canonical methods and the family's own five-method
benchmark report no AUC at all. The two numbers behind "0.75–0.82" are both correct, but both
come from supervised ML classifiers that merely use ENM-derived features, and one of the two is
a balanced-validation median rather than a test-set score. Any conclusion that requires "the
ENM family scores 0.75–0.82" is resting on a two-point band drawn from outside that family._

If a defensible statement is needed, this one is supportable: _residue-level supervised
predictors that include dynamics-derived features report AUC ≈ 0.79–0.80 on ASBench-derived
sets (n = 2, one paywalled, one balanced-validation);_ and separately, _unsupervised
elastic-network and network-communication methods report no AUC, so no published AUC baseline
for that family exists._

The second half of that is a **useful** result for this project: with no published AUC in the
family, a measured AUC on a frozen benchmark is not a number to be compared against literature
— it has to be compared against the project's own controls. That is what the repo's own bar
(`−distance` at AUC 0.617; best classical spectral readout 0.757) already does. Note those two
are unsupervised, natural-prevalence, whole-protein residue rankings and are therefore **not**
comparable to either band data point; do not difference them.

---

## 4. One-line answer

**Does an ordinary published result in this family reach AUC 0.86–0.95?**

**No.** No elastic-network, normal-mode, PRS, network-centrality or communication-pathway method
was found reporting _any_ AUC-ROC, let alone one ≥ 0.86; the single verified AUC ≥ 0.86
(AlloPED-pocket, 0.920) is **pocket-level** and contains **no** elastic-network content, and the
same paper's **residue-level** AUC is **0.563**.

---

## 5. Method

**Databases and routes.** NCBI E-utilities `efetch` (db=pubmed, rettype=abstract) — the only
reliable PubMed route, since `pubmed.ncbi.nlm.nih.gov` HTML is cookie-walled and returns no
content to a fetcher. Europe PMC REST `search` with `resultType=core` (works). Europe PMC
`fullTextXML` (intermittent: 404 for PMC6718341 and PMC4883016, worked for PMC7395124,
PMC5007447, PMC3562710, PMC7330491). PMC article pages at `pmc.ncbi.nlm.nih.gov` — note
`www.ncbi.nlm.nih.gov/pmc/` 301-redirects and the redirect must be followed manually.
biorxiv.org `.full`. General web search.

**Retrieval per claim.** Data point 1: abstract retrieved verbatim via E-utilities; full text
attempted twice against two distinct ACS URLs, both HTTP 403. Data point 2: abstract via
E-utilities, full text via the PMC article page, queried twice with different targeted prompts
to separate the validation-set median from the independent-test result. Section 2.1: each of
six methods fetched individually in full text and asked for verbatim "AUC"/"ROC"/"area under"
sentences, with an explicit instruction to state "no AUC reported" rather than infer.

**Counts.** 2 data points verified. 6 family methods checked in full text for AUC, 6 negative.
1 five-method comparative benchmark checked in full text, negative. 6 AUC values located and
graded. 5 near-miss methods recorded. 1 propagated attribution error found and corrected
(AllosES / AlloPED-pocket).

**Stopping rule.** For the two data points: stop once the exact number is returned from the
primary record and its endpoint, benchmark and evaluation split are established, or the full
text is confirmed unreachable. For the widening: stop once every method named in the repo's
claim has been checked in full text and the family's own comparative benchmark has been checked,
since that benchmark covers five methods at once and is the strongest available evidence on
whether the family uses AUC.

**What could not be reached.**

- ZHMolEReP full text — HTTP 403 at `pubs.acs.org/doi/10.1021/acs.jcim.6c00141` and at the
  `jcisd8/article-abstract` landing page. No preprint or PMC deposit located. Therefore
  **ROC vs precision–recall for the 0.7858 figure is unresolved**, as is whether its evaluation
  used balanced or natural class ratios.
- AllositePro (doi:10.1021/acs.jcim.7b00014) full text not retrieved; its abstract contains no
  performance numbers at all. Its no-AUC status is established only indirectly, via the Patterns
  benchmark that includes it.
- AR-Pred's positive:negative ratio inside its 10 balanced sets was not stated in the retrieved
  text; only the count of sets (10) and the global residue counts (167 / 6607) were recovered.
- Europe PMC `FULL_TEXT:` field is non-functional on the REST endpoint (control query returned
  hitCount 0). No negative conclusion rests on it.
