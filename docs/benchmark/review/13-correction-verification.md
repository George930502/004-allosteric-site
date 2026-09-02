# Independent verification of ten proposed corrections

**Date: 2026-09-02.**

**Scope.** Ten claims drawn from [`11-synthesis.md`](11-synthesis.md) §2 that are queued to be written
into, or against, a frozen benchmark layer. Each was re-checked against a primary source in this
session — publisher page, Crossref, Europe PMC, PMC, RCSB, PDBe, or the live ASD host — without
relying on [`06-definition-audit.md`](06-definition-audit.md),
[`07-metrics-audit.md`](07-metrics-audit.md), [`07a-metrics-fact-check.md`](07a-metrics-fact-check.md),
[`08-structure-evidence.md`](08-structure-evidence.md) or
[`09-extension-sweep.md`](09-extension-sweep.md) for the fact. Those five were read first, so that
what was already claimed is known, and then set aside.

**Headline. Five of the ten stand exactly as written. Four need a narrower statement. One is
refuted, and the correction it proposes would put a wrong number into a freeze.**

This file names no allosteric-site residue and no per-arm label count, for the reason
[`09-extension-sweep.md`](09-extension-sweep.md) gives: at the time of writing this directory
was not in `tests/test_no_leakage.py`'s `PROTECTED_PATHS`. It is now (ADR 0034), and the
redaction is kept as defence in depth.

---

## Verdict table

|   # | Claim                                                                                                                                    | Verdict                 | Primary source                                           | Correction needed                                                                                                                 |
| --: | ---------------------------------------------------------------------------------------------------------------------------------------- | ----------------------- | -------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
|   1 | ASD is reachable; 12 archives, ~143.7 MB over plain HTTP; expired TLS certificate; list is a JavaScript array; research-use-only licence | **PARTIALLY CONFIRMED** | `mdl.shsmu.edu.cn` via reader proxy; direct HTTPS probes | Drop or tag the 143.7 MB figure — not verifiable here. Narrow the `<a href>` clause                                               |
|   2 | Kincore defines Type IV by minimum distances > 6.5 Å from hinge and C-helix-Glu(+4)                                                      | **CONFIRMED**           | doi:10.1093/nar/gkab920, PMC8728253                      | —                                                                                                                                 |
|   3 | CryptoBank applies a global entry-level apo filter over ~6 M alignments                                                                  | **CONFIRMED**           | doi:10.1126/sciadv.ady6364, PMC13267282                  | —                                                                                                                                 |
|   4 | Variogram surrogates 29.2–36.3 % FPR, worse than the spin test; eigenmode rotation 5.2–5.3 %                                             | **CONFIRMED**           | doi:10.1162/IMAG.a.71, PMC12330862                       | —                                                                                                                                 |
|   5 | RCSB serves RSRZ 6.50 % / 24.6th percentile for `1OPL`; PDBe serves 22.18 % / 0.4th; the two partners serve different validation runs    | **PARTIALLY CONFIRMED** | RCSB data API; PDBe validation XML and PDBe REST API     | All four numbers are right. The stated cause is wrong: PDBe serves the _same_ report as RCSB. Only one PDBe API endpoint is stale |
|   6 | Vajda's Table 1 has 20 rows, so the "8 of 19" denominator must be re-checked                                                             | **REFUTED**             | doi:10.1016/j.cbpa.2018.05.003, PMC6088748               | Table 1 has **19** data rows. The repo's existing "8 of 19" is correct and must not be changed                                    |
|   7 | `max MCC ≈ sqrt(5/m)` overstates; exact form gives 0.491–0.642, not 0.50–0.67                                                            | **PARTIALLY CONFIRMED** | Derived independently from the MCC definition            | Closed form and direction of error confirmed. The "0.50–0.67" comparator is scope-mismatched                                      |
|  8a | doi:10.1002/advs.202513641 is 2025, not 2026                                                                                             | **REFUTED**             | Crossref; Europe PMC                                     | Online 2025-11-28; version of record _Adv Sci_ **2026**;13(12):e13641. The existing "2026" is defensible; do not flip it to 2025  |
|  8b | `07-metrics-audit.md` §4.1 says "nine papers" above a ten-row table                                                                      | **CONFIRMED**           | The file itself, lines 437–452                           | —                                                                                                                                 |
|   9 | AUROC 0.95 is an Appendix-A baseline's, not Allo-Allo's; the Bonferroni adjusts attention-head selection, not the AlphaMissense test     | **CONFIRMED**           | doi:10.1101/2024.09.28.615583                            | —                                                                                                                                 |
|  10 | doi:10.64898/2026.01.28.702257 is real and describes a Pocket Fragmentation Index                                                        | **CONFIRMED**           | Crossref; bioRxiv full text                              | —                                                                                                                                 |

---

## 1. ASD reachability — PARTIALLY CONFIRMED

**Reachable: yes.** `http://mdl.shsmu.edu.cn/ASD/module/download/js/download.js` and
`http://mdl.shsmu.edu.cn/ASD/js/util/localcomponent.js` were both retrieved today and returned
their source. **Disclosure of method, because it bears on the verdict:** this environment's fetch
tool rewrites `http://` to `https://`, so the plain-HTTP retrieval went through the `r.jina.ai`
reader proxy. That is one trust hop more than `curl`. Direct HTTPS attempts against
`https://mdl.shsmu.edu.cn/ASD/`, `.../download.js` and `.../download.jsp?tabIndex=1` all failed
with `certificate has expired`, three times, on three different paths.

**Confirmed exactly.** `dataRecord2023` is a literal JavaScript array of **twelve** objects, each
with `fileName`, `fileDescrip`, `fileType`, `versionNum`, `dateCreate`. The newest is
`ASD_Release_202309_AS.tar.gz`, Release 5.1, dated 2023-09-20; `ASD_Release_202306_XF.tar.gz` is
present at Release 5.01. `localcomponent.js` defines
`asd2015_static_file_root = "https://mdl.shsmu.edu.cn/ASD2023Common/static_file/"` and
`apo_holo_pse_gz_path` derived from it. The licence sentence is verbatim, and appears twice in the
file: **"ASD contains data for research use only. Users will not be allowed to distribute the data
to a third party."** The deployed TLS certificate is expired.

**Not verified, and it should not be asserted.** The **143.7 MB total** could not be checked: the
proxy refuses binary payloads (HTTP 422 on the `.tar.gz`), and nothing here downloaded an archive.
Report it as a figure measured by `curl` on 2026-09-02 in
[`09-extension-sweep.md`](09-extension-sweep.md), not as re-verified.

**Two clauses need narrowing.** First, the download list _is_ emitted as `<a href>` elements — but
only inside the `loginDownloadHtml` branch, which an unauthenticated fetch never reaches; the
anonymous branch prints file names without anchors. The audit's conclusion (an `href` scrape of the
rendered anonymous page finds nothing) is right; the statement "not `<a href>` elements" is not
literally true of the file. Second, an incidental finding against
[`09-extension-sweep.md`](09-extension-sweep.md) §1 headline 2, which says the certificate "has not
been renewed": Certificate Transparency logs list two current `*.shsmu.edu.cn` certificates —
SHECA OV Server CA G5, valid 2025-11-10 to 2026-11-10, and RapidSSL TLS RSA CA G1, valid 2025-11-28
to 2026-12-29. Certificates were renewed at the certificate authority; they are not deployed on
this host. The expiry date 2025-12-28 was not confirmed.

## 2. Kincore Type IV — CONFIRMED

Retrieved twice by independent routes, PMC HTML and the Europe PMC full-text XML, with identical
wording. Modi V, Dunbrack RL, _Nucleic Acids Res_ 2022;50(D1):D654–D664, doi:10.1093/nar/gkab920,
PMC8728253:

> "Allosteric: Any small molecule in the asymmetric unit whose minimum distances from the hinge
> region and C-helix-Glu(+4) residues are both >6.5 Å."

Every element of the claim holds. The number is **6.5 Å**. There are **two** landmarks, the hinge
region and C-helix-Glu(+4). It is a **minimum distance** and it runs **ligand to landmark residue**,
not site to site. The adjacent Type 3 rule corroborates the form of the convention: "minimum
distance from the hinge >6 Å and at least three contacts in the back pocket". The class holds 220
unique ligands. The four qualifications
[`06-definition-audit.md`](06-definition-audit.md) §3.2 attaches — kinase-specific, ligand-to-landmark,
purely geometric, and therefore in tension with clause (ii) — all survive this check and must travel
with the citation.

## 3. CryptoBank apo filter — CONFIRMED

Febrer Martinez P, Fröhlking T, Borsatto A, Gervasio FL, _Sci Adv_ 2026, doi:10.1126/sciadv.ady6364,
PMC13267282. The DOI resolves to a real paper of that name. Verbatim: the apo filter is "an apo
structure filter selecting entries with no nonpolymer entities", against "a preliminary holo
structure filter selecting entries with at least one nonpolymer entity". The scale figure is
verbatim: "This produced 6 million unique apo-holo-ligand combinations." The filter is **entry-level**
— it tests the whole PDB entry's `nonpolymer_entity_count`, not the neighbourhood of a binding
site — with a later refinement against a curated exclusion list of ions, solvents and low-mass
compounds. The proposed narrowing of `primary/README.md` §1, to "the majority among resources that
annotate apo/holo per binding site", is supported.

## 4. Variogram-matched surrogates — CONFIRMED

Koussis NC et al., _Imaging Neuroscience_ 3, 2025, doi:10.1162/IMAG.a.71, PMC12330862. Every digit
is in the published text, and the direction of the comparison is stated by the authors, not
inferred:

> "The BrainSMASH method shows higher FPR than both the Spin Test and eigenstrapping, reaching
> 29.2% at α = 2.0 and 36.3% at α = 3.0."

> "the Spin Test yields higher than expected FPR across all SA regimes, ranging from 5.7% at
> α = 0.0, increasing to 6.8% (α = 1.0), 7.4% (α = 2.0), to a maximum of 12.3% (α = 3.0)."

> "Eigenstrapping yields an FPR near or below the expected 5% for α = 0.0–2.5, with 5.3%
> (α = 0.0), 2.1% (α = 0.5), 3.5% (α = 1.0), 5.6% (α = 1.5), 5.0% (α = 2.0), 5.2% (α = 2.5), and
> 5.2% (α = 3.0)."

The 5.2–5.3 % pair for eigenmode rotation, the 29.2–36.3 % pair for the variogram method, and
"worse than the spin test" are all the paper's. The presentational caveat
[`07a-metrics-fact-check.md`](07a-metrics-fact-check.md) §1 raises stands: the α values are not
matched across those three quotations, and the α-matched row at α = 3.0 — 5.2 %, 12.3 %, 36.3 % —
is the one to print. Two further caveats already recorded there must travel with the citation: the
measurements are on simulated Gaussian random fields on a cortical surface, and the bioRxiv v2
preprint of the same work carries different numbers.

## 5. `1OPL` validation percentiles — PARTIALLY CONFIRMED, and the stated cause is wrong

All four numbers are right. The inference drawn from them is not.

RCSB's data API for `1OPL` gives `pdbx_vrpt_summary_diffraction.percent_RSRZ_outliers = 6.5`,
`pdbx_vrpt_summary_geometry.clashscore = 11.29`, and
`pdbx_vrpt_summary.report_creation_date = "2026-03-20T17:53:00.000+00:00"`. PDBe's REST endpoint
`validation/global-percentiles/entry/1opl` returns 22.18 % at the 0.4th absolute and 0.6th relative
percentile.

**But PDBe's own validation report says 6.50 %.** The wwPDB report PDBe serves at
`https://www.ebi.ac.uk/pdbe/entry-files/download/1opl_validation.xml` carries
`percent-RSRZ-outliers="6.50"`, `absolute-percentile-percent-RSRZ-outliers="24.6"`,
`relative-percentile-percent-RSRZ-outliers="19.3"`, `clashscore="11.29"`,
`PDB-revision-number="5"`, `XMLcreationDate="Mar 20, 2026 -- 05:53 PM UTC"`. That creation
timestamp is identical to RCSB's to the minute. **The two partners serve the same validation run.**
The 24.6th-percentile figure in the claim is confirmed — and it is confirmed from PDBe, not from
RCSB.

The discrepancy is real but narrower than stated: **one PDBe REST endpoint is stale relative to the
report PDBe itself distributes.** Write that, not "the two wwPDB partners are serving different
validation runs", which a reviewer can disprove in one fetch. The operative correction to
`docs/targets.md` is unaffected: 22.18 % / 0.4th percentile is superseded by 6.50 % / 24.6th
percentile in the current report, and the source of the stale number is a percentile API, not a
partner disagreement.

## 6. Vajda cryptic/allosteric denominator — REFUTED

Vajda S, Beglov D, Wakefield AE, Egbert M, Whitty A, _Curr Opin Chem Biol_ 2018;44:1–8,
doi:10.1016/j.cbpa.2018.05.003, PMC6088748. The sentence is verbatim as reported: **"Eight of the
sites shown in Table 1 are allosteric."**

The denominator claim is wrong. Table 1 — captioned "Proteins in the CryptoSite set with validated
high affinity cryptic sites" — has **19** data rows, not 20. Three independent retrievals (the PMC
article page and two reads of the Europe PMC full-text XML) enumerate the identical 19 rows, in the
same order, ending at Bcl-xL. Two of the three retrieval summaries reported a count of 18 while
listing 19 items; the enumeration, not the summary count, is the evidence, and no retrieval produced
a twentieth row.

The internal check settles it. Exactly **8** of the 19 rows carry `Type = Allo`, which is precisely
the number the sentence states. 9 are `Ortho` and 2 are `PPI`. The repo's existing "8 of 19" in
`evaluation/README.md` §3.3 is correct as it stands.

**One qualification to record beside it, not a correction:** the 19 rows are 19 _sites_, not 19
proteins. Hepatitis C virus polymerase appears twice, unbound `3CJ0A` against holo `2BRLA` and
`3FQKB`, so the table covers 18 distinct proteins. The paper's own sentence says "sites", so 19 is
the denominator the sentence licenses. Item 2.13 of [`11-synthesis.md`](11-synthesis.md) should be
struck and the number left alone.

## 7. max-MCC closed form — PARTIALLY CONFIRMED

Derived here from the definition, not read from the audit. Take a candidate set of size `n`, `p`
positives, and a predictor that names exactly `k` residues, of which `t` are true. Then
`TP = t`, `FP = k − t`, `FN = p − t`, `TN = n − k − p + t`.

The numerator collapses:
`TP·TN − FP·FN = t(n − k − p + t) − (k − t)(p − t) = tn − kp`.

The four marginals are free of `t`: `TP + FP = k`, `TP + FN = p`, `TN + FP = n − p`,
`TN + FN = n − k`. So

```
MCC(t) = (t·n − k·p) / sqrt(k · p · (n − p) · (n − k))
```

which is **linear and increasing in `t`**, the denominator being constant. The maximum is therefore
at `t = min(k, p)`, and at `p ≥ k` it is `t = k`, giving

```
max MCC = k(n − p) / sqrt(k·p·(n − p)·(n − k)) = sqrt( k(n − p) / (p(n − k)) )
```

At `k = 5` that is `sqrt(5(n − p) / (p(n − 5)))`, character for character the form
[`07-metrics-audit.md`](07-metrics-audit.md) §3.2 gives. **CONFIRMED by independent derivation.**

**The shorthand always overstates, and by exactly how much is closed-form too.** The exact value
divided by `sqrt(5/p)` is `sqrt((n − p)/(n − 5))`, which is strictly below 1 whenever `p > 5`. So
`sqrt(5/m)` is an upper bound that is never attained, and the relative overstatement is
`sqrt((n − 5)/(n − p)) − 1`. The direction in the claim is right, and it runs against the audit's own
argument, so replacing the shorthand strengthens it. Per-arm values were not re-derived — they need
the frozen label sets, and this directory is unprotected — but the arithmetic in
[`07a-metrics-fact-check.md`](07a-metrics-fact-check.md) §8 reproduces exactly from the `m` and `n`
that table states, to every printed digit, including the 0.5 % and 4.1 % endpoints.

**One defect in the claim's presentation.** "True range 0.491–0.642, not 0.50–0.67" compares two
different sets of arms. `0.67 ≈ sqrt(5/11)` requires a label set of 11, which is a secondary arm;
the exact range 0.491–0.642 is over the five primary arms. Computed over those same five arms the
shorthand runs 0.500 to 0.645, so the honest statement of the overstatement is "up to 4.1 %", not a
gap between 0.642 and 0.67. Fix the comparator or state both scopes.

## 8. The two clerical items — 8a REFUTED, 8b CONFIRMED

**(a) The year is not simply 2025, and flipping it would be a new error.** Crossref for
doi:10.1002/advs.202513641 gives `published-online` and `issued` = 2025-11-28, `created` 2025-11-29,
`published-print` February 2026, volume 13, issue 12, article e13641. Europe PMC assigns
`pubYear = 2026`, with `firstPublicationDate` and `electronicPublicationDate` of 2025-11-28 and a
journal issue date of February 2026. So the version of record is **_Adv Sci_ 2026;13(12):e13641**,
first published online 2025-11-28. The bibliography's existing "2026" matches the journal, the issue
and the indexing databases. Item 2.17 of [`11-synthesis.md`](11-synthesis.md) is wrong to call this
a clerical error; if anything is missing it is the volume, issue and online date, and the fix is to
add them, not to change the year. This is the one item where adopting the proposed correction would
put a worse citation into the repository than the one already there.

**(b) Confirmed by direct count.** The table under
[`07-metrics-audit.md`](07-metrics-audit.md) §4.1 has **ten** data rows — AlloPred, PocketMiner,
APOP, Allo-Allo, CryptoBench, DeepAllo, STINGAllo, Allo-PED, Eccleston & Furnham, Kinase pLM
framework. The prose above it says "nine papers"; the conclusion below it says "8 of 10". The
prose is the error, exactly as claimed.

## 9. Allo-Allo AUROC and Bonferroni — CONFIRMED

Dong T, Kan C, Devkota K, Singh R, bioRxiv 2024, doi:10.1101/2024.09.28.615583, full text read at
biorxiv.org. Both halves hold.

**(a)** The 0.95 belongs to the Appendix-A prediction-head baseline: "The Prediction-Head approach
achieved an AUPRC of 0.68 and an AUROC of 0.95 on the test set." Allo-Allo's own headline number is
AUPRC 0.77. Attributing 0.95 to Allo-Allo credits the method with a competitor's score, and on the
metric where that competitor wins.

**(b)** The Bonferroni sentence — "Bonferroni correction was applied to adjust the p-values for
multiple hypothesis testing" — sits under the methods heading "Selecting attention heads with
highest allosteric sensitivity", adjusting the per-head t-tests used to build the model. The
AlphaMissense analysis is a separate section, uses a Welch's t-test, and contains no mention of
Bonferroni. The correction is right, and the reason matters: a multiplicity correction applied to
feature selection is further from a performance claim than a downstream validation would be, so the
restatement of `evaluation-metrics.md` §3.5 gets stronger, not weaker.

## 10. Seq2Pocket Pocket Fragmentation Index — CONFIRMED

doi:10.64898/2026.01.28.702257 resolves in Crossref to a registered openRxiv/bioRxiv preprint,
"Seq2Pocket: Augmenting protein language models for spatially consistent binding site prediction",
Škrhák V, Polák L, Novotný M, Hoksza D, posted 2026-01-31, resource URL
`http://biorxiv.org/lookup/doi/10.64898/2026.01.28.702257`. The `10.64898` prefix is bioRxiv's
current one and is not an error.

The metric exists and the paper's own wording is:

> "To evaluate the effectiveness of the clustering method, we suggest a measure called Pocket
> Fragmentation Index (PFI), which measures the average number of predicted clusters assigned to
> each ground-truth pocket"

> "An ideal clustering strategy achieves a one-to-one mapping, resulting in a PFI of 1.0."

> "By monitoring this index, we can identify excessive clustering fragmentation, where a single
> biological binding site is incorrectly partitioned into multiple predicted regions."

Use those three. The separate warning in
[`07a-metrics-fact-check.md`](07a-metrics-fact-check.md) §2 is unaffected and still applies: the
"incomplete pockets… often achieve high statistical scores" sentence in
[`07-metrics-audit.md`](07-metrics-audit.md) §1.2 is not the paper's wording and must not be carried
inside quotation marks.

---

## Method and its limits

Every source above was fetched in this session. Nothing is confirmed from memory. Where two
retrievals of the same document disagreed, both are reported and the disagreement is resolved by
enumeration rather than by a summary count (item 6).

Three limits, stated because they bound what this file establishes.

1. **No shell.** This session had no command execution, so nothing was `curl`ed, no certificate was
   inspected with `openssl`, and no archive was downloaded. The ASD plain-HTTP result went through a
   third-party reader proxy and is one trust hop weaker than the `curl` evidence in
   [`09-extension-sweep.md`](09-extension-sweep.md). It corroborates that record; it does not
   replace it.
2. **Retrieval is one step removed from the raw file.** Pages were fetched and summarised by a
   tool. Quoted strings are as that tool returned them. Anything load-bearing in `docs/report/`
   should be re-quoted from the raw source, as
   [`06-definition-audit.md`](06-definition-audit.md) already warns.
3. **`data/structure-evidence.json` was not re-derived.** Item 5 was checked against the live RCSB
   and PDBe services, not against the cached responses under `data/rcsb-raw/`.

## Direct sources

- <https://pmc.ncbi.nlm.nih.gov/articles/PMC8728253/> and
  <https://www.ebi.ac.uk/europepmc/webservices/rest/PMC8728253/fullTextXML> (Kincore)
- <https://pmc.ncbi.nlm.nih.gov/articles/PMC13267282/> (CryptoBank)
- <https://pmc.ncbi.nlm.nih.gov/articles/PMC12330862/> (eigenstrapping)
- <https://pmc.ncbi.nlm.nih.gov/articles/PMC6088748/> and
  <https://www.ebi.ac.uk/europepmc/webservices/rest/PMC6088748/fullTextXML> (Vajda 2018, Table 1)
- <https://data.rcsb.org/rest/v1/core/entry/1OPL>
- <https://www.ebi.ac.uk/pdbe/entry-files/download/1opl_validation.xml>
- <https://www.ebi.ac.uk/pdbe/api/validation/global-percentiles/entry/1opl> and
  <https://www.ebi.ac.uk/pdbe/api/validation/summary_quality_scores/entry/1opl>
- <https://api.crossref.org/works/10.1002/advs.202513641> and Europe PMC search for the same DOI
- <https://api.crossref.org/works/10.64898/2026.01.28.702257> and
  <https://www.biorxiv.org/content/10.64898/2026.01.28.702257v1.full>
- <https://www.biorxiv.org/content/10.1101/2024.09.28.615583v1.full>
- `http://mdl.shsmu.edu.cn/ASD/module/download/js/download.js` and
  `http://mdl.shsmu.edu.cn/ASD/js/util/localcomponent.js`, via reader proxy
- <https://api.certspotter.com/v1/issuances?domain=shsmu.edu.cn&include_subdomains=true>
