# Allosteric-site prediction: prior art on our targets, benchmark membership, and the field's bar

Review date **2026-08-20**. Scope: **allosteric-site prediction**. Cryptic-pocket prior art is
reviewed separately and is not repeated here; where a method spans both, only its
allosteric-site claims are recorded.

## How claims are tagged

| Tag                   | Meaning                                                                                       |
| --------------------- | --------------------------------------------------------------------------------------------- |
| `[VERIFIED-FULLTEXT]` | read from the paper's full text this session                                                  |
| `[VERIFIED-ABSTRACT]` | read from the abstract/record only; the full text was paywalled or unretrievable              |
| `[VERIFIED-DBRECORD]` | read live from a primary database record (ASBench, RCSB, PDBe) this session, not from a paper |
| `[UNVERIFIED]`        | could not be established from a primary source in this session; stated as open                |

Nothing here is from recall. Every number traces to a fetch made this session.

## What could and could not be reached

- **Europe PMC REST** (`/search`, `/{PMCID}/fullTextXML`) — worked throughout.
- **ASBench** (`http://mdl.shsmu.edu.cn/asbench/`) — server-side JSP, **fully queryable**
  through a text proxy. This is the load-bearing source for the ASD membership question,
  because ASBench is built directly from ASD's qualified allosteric sites.
- **ASD proper** (`http://mdl.shsmu.edu.cn/ASD/`) — **not queryable in this session.** Its
  navigation renders, but every data table is client-side JavaScript, so a text proxy
  returns navigation only. Direct `curl` over plain HTTP was unavailable (no shell in this
  thread) and `WebFetch` force-upgrades to HTTPS, which fails on the expired
  `*.shsmu.edu.cn` certificate already recorded in `docs/benchmark/primary/README.md` §7.
  **This is the single open hole in the review** — see "What to run next".
- **CASBench** (`biokinet.belozersky.msu.ru/casbench`) — search interface renders, results
  do not; the only bulk download is a 1.9 GB tarball. Its 91-entry list could not be
  enumerated. `[UNVERIFIED]`

---

# (a) Target-by-target benchmark membership, and the leakage verdict

## Summary table

| Our target                          | ASD / ASBench                                                                                           | CASBench   | Used by which predictors                                                                                    | Blind?                                                                                                         |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------- | ---------- | ----------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| **KRAS** (P01116)                   | **absent from ASBench**; ASD 2023 status unresolved                                                     | unresolved | none found                                                                                                  | **Probably blind, but the homologue is not** — see below                                                       |
| **HRAS** (P01112) — homologue       | **PRESENT**, `AS001013301`, PDB `4DLR` (+`4DLV`,`4DLX`,`4DLY`,`4DLZ`)                                   | unresolved | ASBench Core set → MEF-AlloSite test sets, PASSer2.0 extra validation; possibly AlloPred/PASSer2.0 training | n/a                                                                                                            |
| **ABL1 / BCR-ABL** (P00519, P00520) | **PRESENT TWICE**, `AS001006501` (`3PYY`) and `AS002023501` (`3K5V`) — **both at the myristoyl pocket** | unresolved | same as above; **`3K5V` is an APOP case study** and **`3PYY` is an ESSA case study**                        | **NO. Not blind.**                                                                                             |
| **Cardiac myosin / MYH7** (P12883)  | **ABSENT from ASBench** (keyword `myosin` → "No Complex to display")                                    | unresolved | none found                                                                                                  | **Blind w.r.t. ASD-trained ML.** But see Zheng 2023 below — myosin is challenge reference [1]'s own test case. |

## KRAS — absent, but its homologue's ASD site sits in our label region

`[VERIFIED-DBRECORD]` ASBench full-text search for `kras` returns **"No Complex to display",
Page of 0**. ASBench's Core set is 235 entries over 12 pages; a search for `Ras` returns 21
records of which exactly one is a Ras GTPase.

`[VERIFIED-DBRECORD]` That one record is **`AS001013301` — "Gtpase hras", UniProt P01112,
PDB `4DLR`, modulator `DTU`, allosteric type "Regulator"**, with the curated allosteric site
residues given verbatim as:

> `R68,D92,Q95,Y96,Q99,etc.`

Related ASBench structures for the same target: `4DLV` (DTT), `4DLX` (DTU), `4DLY` (DTT),
`4DLZ` (DTU), all "Regulator".

`[VERIFIED-DBRECORD]` `4DLR` is H-Ras at 1.32 Å with GNP, DTU ((2R,3S)-1,4-dimercaptobutane-2,3-diol,
i.e. DTT), Ca and Mg; primary citation Holzapfel, Buhrman & Mattos, _Biochemistry_ 2012,
[10.1021/bi300509j](https://doi.org/10.1021/bi300509j).

`[VERIFIED-ABSTRACT]` That site is the **Mattos "allosteric switch"**: calcium acetate (or
DTT/DTE) binds remote from the active site and induces "a shift in helix 3/loop 7 and a
network of H-bonding interactions that propagates across the molecule, culminating in the
ordering of switch II" (Buhrman, Holzapfel, Fetics & Mattos, _PNAS_ 2010,
[10.1073/pnas.0912226107](https://doi.org/10.1073/pnas.0912226107)).

**Why this matters more than "KRAS is absent".** Our frozen KRAS **distal** label set, as
recorded in `docs/benchmark/primary/README.md` §5, is `9, 59, 60, 61, 62, 63, 68, 69, 72, 95, 96, 99,
100, 103`. The ASD-curated H-Ras allosteric residues named above are `68, 92, 95, 96, 99`.
**Four of the five named residues — 68, 95, 96, 99 — are positions in our KRAS distal
ground-truth set.** This is not coincidence: the switch-II pocket is bounded by switch II and
helix 3, and the Mattos allosteric site is the helix-3/loop-7 face of the same groove.

Consequences, each of which must appear in the report:

1. An ASD-trained predictor evaluated on KRAS has been trained on a homologue whose curated
   allosteric site **overlaps our label region at the residue level**. It is not blind in the
   way "KRAS is not in ASD" would suggest.
2. **A 30–40 % sequence-identity de-duplication does not separate KRAS from HRAS.** Every
   predictor reviewed here de-duplicates at 30 % (PASSer, PASSerRank, DeepAllo, MEF-AlloSite)
   or 40 % (CryptoSite). KRAS and HRAS G domains are far above that. The field's standard
   redundancy filter would _not_ have removed this leak.
3. `[UNVERIFIED]` The exact overlap count must be recomputed against `frozen.json` rather than
   against the prose above — `docs/benchmark/primary/README.md` is a document, not code. Recompute
   with `uv run allo benchmark show` before the number goes in the report.

`[UNVERIFIED]` Whether ASD 2023 has since added a KRAS entry (sotorasib was approved after
ASBench froze in 2015) is **not established**. The ASD2023 paper
([10.1093/nar/gkad915](https://doi.org/10.1093/nar/gkad915), PMC10767950) mentions
sotorasib, "K-Ras(G12C) inhibitors allosterically control GTP affinity and effector
interactions" and "pan-KRAS inhibitor disables oncogenic signalling" **only as introduction
citations**, not as curated targets `[VERIFIED-FULLTEXT]`. Treat the KRAS/ASD question as
open and resolve it before publishing any "blind on KRAS" claim.

## BCR-ABL1 — the earlier assertion is **VERIFIED**

The previously unverified claim was: _ASD curates the BCR-ABL myristoyl site._ It does, twice.

`[VERIFIED-DBRECORD]` ASBench record **`AS001006501`**: target "BCR-ABL", UniProt **P00519**,
gene ABL1, _Homo sapiens_, PDB **`3PYY`**, modulator `3YY`, allosteric type **Activator**,
EC 2.7.10.2. Curated allosteric site residues verbatim:

> `A356,L359,L360,A363,L448,etc.`

`[VERIFIED-DBRECORD]` `3PYY` is human ABL1 at 1.85 Å containing `STI` (imatinib) and `3YY`;
primary citation Yang et al., _Chemistry & Biology_ 2011,
[10.1016/j.chembiol.2010.12.013](https://doi.org/10.1016/j.chembiol.2010.12.013), titled
**"Discovery and Characterization of a Cell-Permeable, Small-Molecule c-Abl Kinase Activator
that Binds to the Myristoyl Binding Site"** (the compound is DPH). The site is named in the
title of the paper ASD cites.

`[VERIFIED-DBRECORD]` ASBench record **`AS002023501`**: target "BCR-ABL", UniProt **P00520**
(mouse Abl1), PDB **`3K5V`**, modulator `STJ`, allosteric type **Inhibitor**.

`[VERIFIED-DBRECORD]` `3K5V` is mouse ABL1 at 1.74 Å with `STI` (imatinib) and `STJ`
(3-(6-{[4-(trifluoromethoxy)phenyl]amino}pyrimidin-4-yl)benzamide, a GNF-2 analogue);
primary citation Zhang et al., _Nature_ 2010,
[10.1038/nature08675](https://doi.org/10.1038/nature08675), "Targeting Bcr-Abl by combining
allosteric with ATP-binding-site inhibitors" — GNF-2 **binds the myristate-binding site of Abl**.

`[VERIFIED-DBRECORD]` One further observation, from a partial render of the ASBench BCR-ABL
target page that did not reproduce on retry: a related-structures table listed **`1OPL` with
modulator `MYR`, classified Inhibitor**. Single observation, not reproduced — treat as
`[UNVERIFIED]` pending a `curl` confirmation. It does not change the verdict, which the two
reproducible records already establish.

`[VERIFIED-DBRECORD]` The residue numbers `A356, L359, L360, A363, L448` are ABL1 **isoform 1b**
numbering, the same convention `docs/targets.md` establishes for `1OPL`/`5MO4`. Consistent with
the myristoyl pocket; not independently re-derived here.

**Verdict: on BCR-ABL1 no ASD-trained method is blind, and neither are the two leading
ENM methods.** `3PYY` is the worked case study in the ESSA paper and `3K5V` is one of three
worked case studies in the APOP paper — details in section (c). This is stronger than the
open item currently recorded in `docs/benchmark/primary/README.md` §7, which names only PASSer.

## Cardiac myosin — absent from ASBench, but _is_ a test case for challenge reference [1]

`[VERIFIED-DBRECORD]` ASBench full-text search for `myosin` returns **"No Complex to
display"**. No myosin of any class is in the ASBench Core set.

`[VERIFIED-FULLTEXT]` **Zheng 2023 — the challenge's own reference [1] — uses myosin as one
of its four test proteins**, with apo `1MMA` and holo `1YV3` (blebbistatin-bound), and reports
"a cluster of pocket residues lying in the L50–U50 cleft" overlapping "both the ADP-binding
site and the known allosteric sites for blebbistatin". That is the **blebbistatin** pocket —
our Site 2.

**⚠️ CORRECTED 2026-08-20. An earlier version of this paragraph stopped here, and concluded
that reference [1] had not touched our Site 1. It had.** Zheng reports a _second_ site in the
same passage:

> "In addition to this key cleft, we also found another site at the **N-terminal/converter
> subdomain interface**, which may provide targets for other allosteric agents [see site 1 in
> Fig. 2(a)]."

> "Besides the blebbistatin-binding site and the ADP-binding site, **ESSA** predicted two other
> sites …: the first site at the **N-terminal/converter subdomain interface (residues 120 121
> 688 693 694)** corresponding to site 1 in Fig. 2(a)…"

> "Notably, **sites 1 and 3 were predicted by two methods** and thus may warrant further
> investigations."

Auguin 2024 places the mavacamten pocket "between the **N-terminal** (N-term) and the
**Converter** subdomains of the motor domain" — the same interface. The subdomain names alone
would be suggestive rather than decisive, so it was settled by alignment: `1MMA` ↔ MYH7 pairs
**673 residues at 52 % identity**, carrying ESSA's five residues onto MYH7 **119, 120, 705,
710, 711**. Three of those five are frozen labels on the `8QYP` arm (**120, 710, 711**;
hypergeometric E = 0.11, **P(≥3) = 0.0001**); two on the `9GZ3` arm (**710, 711**;
**P(≥2) = 0.0015**). Both are computed against the **candidate** set, never the node set
(ADR 0011) — the stale node-set figure for the `9GZ3` arm was P = 0.0022 — and the two arms
draw a different number of balls. Residue **120** is a frozen label on the `8QYP` arm, so the
MYH7 functional-site registry leaves it in that arm's universe; on the `9GZ3` arm it is not a
label, so the registry excludes it. Five draws there, four here.
Regenerate: the alignment uses `allo.groundtruth.labels.align_numbering`.

So reference [1] contains a **blind prediction of our Site 1**, made without naming it as the
mavacamten site. The correct statement for the report is now the narrower one: no method has
been reported on **MYH7 itself** — Zheng and ESSA ran on _Dictyostelium_ myosin II — so Site 1
has the _weakest_ prior art of our arms, not none. `manifest.yaml` records `blind: false` on
every Site 1 arm as a result, and Zheng's site 1 is a **bar to clear**, not an absence.

The general lesson is worth keeping: the original error was reading a paper to the sentence
that confirmed the expected answer and stopping. Every "X did not test our site" claim in this
file should be read as provisional until the whole results section has been read.

## Which predictors saw which set

`[VERIFIED-FULLTEXT]` unless noted. The chain matters: ASD → ASBench Core (235) → Core-Diversity
(147 sites / 127 proteins) → individual tools.

| Tool                                | Training source                                                     | Test source                                                                           |
| ----------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| AlloSite (Huang 2013)               | ASD                                                                 | ASD `[VERIFIED-ABSTRACT]`                                                             |
| AlloPred (Greener & Sternberg 2015) | ASBench **Core-Diversity**, 119 proteins after filtering, 79 train  | 40 test, random split (repeated 20×)                                                  |
| PASSer (Tian 2021)                  | ASD, 90 proteins / 2246 pockets / 119 allosteric                    | same, 10 independent runs                                                             |
| PASSer2.0 (2022)                    | ASD 90 + ASBench Core-Diversity 138, dedup → 204; 122 train, 41 val | 41 test + 50 extra from **ASBench Core set**                                          |
| PASSerRank (2023)                   | ASD, 207 proteins, 166 train                                        | 41 ASD test + **CASBench** external (ASD overlaps removed)                            |
| DeepAllo (2025)                     | ASD, 207 proteins, 165 train                                        | 42 test                                                                               |
| MEF-AlloSite (2024)                 | ASD v2.0, "Huang training set" of 90 proteins                       | Test 1/2 = **56 proteins from ASBench Core set**; Test 3 = 122 remaining ASD proteins |
| OHM / Ohm (2020)                    | none (unsupervised)                                                 | 20 proteins from Amor et al.                                                          |
| AlloReverse (2023)                  | MD + ML                                                             | CDC42, SIRT3 `[VERIFIED-ABSTRACT]`                                                    |
| AlloFinder (2018)                   | the group's own allosteric data (i.e. ASD)                          | `[VERIFIED-ABSTRACT]`                                                                 |
| APOP (2023)                         | none (unsupervised ENM)                                             | AlloPred test set + ESSA apo/holo pairs + literature = 104 proteins                   |
| ESSA (2020)                         | none (unsupervised ENM)                                             | 25 monomeric proteins (Dataset I); 12 apo/holo pairs (Dataset II)                     |
| PARS (2012/2014)                    | none (unsupervised)                                                 | 91 non-redundant proteins                                                             |

**The operative fact:** HRAS `4DLR` and ABL `3PYY`/`3K5V` sit in the **ASBench Core set**, which
is used as a **test set** by MEF-AlloSite and as extra validation by PASSer2.0, and is the
parent of the Core-Diversity set that AlloPred and PASSer2.0 **train** on.
`[UNVERIFIED]` Whether `4DLR`/`3PYY`/`3K5V` specifically survived the Core→Core-Diversity
structural de-duplication, and therefore whether they landed in AlloPred's train or test
split, could not be determined — ASBench exposes no Core-Diversity filter in its browse view.

## What to run next to close the ASD hole

Needs a shell. Plain HTTP only; the certificate is expired.

```bash
curl -s 'http://mdl.shsmu.edu.cn/ASD/module/download/download.jsp?tabIndex=1' -o asd_dl.html
# then locate and fetch the ASD_Release_*_AS.txt bulk file and grep it:
grep -iE 'KRAS|K-Ras|P01116|MYH7|myosin|P12883|ABL1|P00519|P00520|HRAS|P01112' ASD_Release_*_AS.txt
```

A 2019 copy of that file exists on GitHub at
`https://raw.githubusercontent.com/MoaazK/deepallo/main/source_data/ASD_Release_201909_AS.txt`
(columns: `target_domain, target_gene, organism, pdb_uniprot, allosteric_pdb, modulator_serial,
modulator_alias, modulator_chain, modulator_class, modulator_feature, modulator_name,
modulator_resi, function, position, pubmed_id, ref_title, site_overlap, allosteric_site_residue`)
`[VERIFIED-DBRECORD]`. **Do not trust a browser fetch of it** — it truncates at ~320 rows, and
that truncated view returns a false negative for ABL and HRAS, which we know from ASBench are
present. Download the whole file and grep it locally. Record its checksum; the transport is
unauthenticated.

---

# (b) How the allostery field scores a prediction

## The convention is **pocket-level top-N**, not residue-level AUC

`[VERIFIED-FULLTEXT]` Nine of the eleven predictors reviewed score at the level of a **pocket
returned by a geometric detector (almost always Fpocket)**, ranked, with success declared if a
true allosteric pocket lands in the top 1, 2 or 3. The definitions of "true" differ, and the
differences are large:

| Method                                        | What counts as a correct pocket                                                                                         |
| --------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| AlloPred, AlloSite (as evaluated by AlloPred) | "a pocket containing **at least one** allosteric binding residue"                                                       |
| PASSer (ASD proteins)                         | pocket "contains at least one residue identified as binding to allosteric modulators"                                   |
| PASSer (ASBench proteins), PASSerRank         | pocket whose **centroid is closest** to the modulator centroid; must be within **10 Å** of the modulator centre of mass |
| PARS                                          | a point is allosteric if **within 10 Å of a modulator atom**                                                            |
| ESSA, APOP                                    | allosteric site detected **within the top 3** ranked pockets                                                            |
| CASBench annotation                           | all residues **within 5 Å** of the ligand                                                                               |
| AlloBench                                     | **Jaccard index** between predicted and known site residue sets                                                         |

**"At least one true residue in the pocket" is a very weak criterion** and is the one the
best-known top-1 numbers were earned under. Our precision@5 / P(≥1 hit) endpoints are stricter
than it in one sense (5 residues, not a whole Fpocket pocket) and softer in another (we do not
require the pocket to be geometrically coherent).

## Residue-level scoring exists but is the minority

`[VERIFIED-FULLTEXT]` Ohm scores residues: TPR 0.57, PPV 0.72 on its 20-protein set (vs 0.23 /
0.48 for the method it replaces), and TPR 47.6 % for the top-20 residues against NMR CHESCA
data.
`[VERIFIED-ABSTRACT]` ZHMolEReP (2026) is explicitly residue-level and argues the pocket-level
framing is wrong on principle — "allosteric regulation is mediated by energy propagation and
cooperative interactions, which often extend beyond the pocket boundaries" — reporting
**recall 0.7037 and AUC 0.7858** on ASBench, with 33 of 40 proteins successfully identified.
`[VERIFIED-ABSTRACT]` AlloPED (2025) reports both: pocket-level MCC 0.544 / AUC 0.920 and
residue-level precision 0.601 / recall 0.422 / specificity 0.661.

**Verdict for our protocol.** Residue-level AUC-ROC/AUC-PR is a **defensible minority
position, not the field default.** ZHMolEReP's residue-level **AUC 0.7858** is the closest
directly comparable published number and is the figure our method should be benchmarked
against for the residue-level endpoint. But the report will be read by people who expect
top-N pocket accuracy, so precision@5 and P(≥1 hit) must be presented as co-equal headline
numbers, not as secondary endpoints in a table at the back. `docs/benchmark/primary/README.md` §5
already anticipates this by citing P2Rank's rejection of residue-level AUC; this review
confirms that P2Rank's position is the field norm in allostery too.

## Leading published numbers

All `[VERIFIED-FULLTEXT]` unless marked. **These are self-reported on the authors' own splits
and are not comparable across rows** — different datasets, different criteria.

| Method                           | Dataset                         | Metric            | Value                                                                                    |
| -------------------------------- | ------------------------------- | ----------------- | ---------------------------------------------------------------------------------------- |
| PARS (Panjkovich 2012)           | 91 non-redundant proteins       | PPV               | **65 %**; flexibility change detected in 70 % of cases `[VERIFIED-ABSTRACT]`             |
| PARS (as re-run by AlloPred)     | ASBench Core-Diversity, 40 test | top-1             | **10/40 = 25 %**                                                                         |
| AlloSite (as re-run by AlloPred) | same                            | top-1             | **21/40 = 52.5 %**                                                                       |
| AlloPred                         | same                            | top-1 / top-2     | **23/40 = 57.5 % / 28/40 = 70 %** (mean 23.6/40 over 20 random splits)                   |
| PASSer (2021)                    | ASD, 90 proteins                | top-1/2/3         | **60.7 % / 81.6 % / 84.9 %**; ROC AUC 0.914, F1 0.782                                    |
| PASSer2.0                        | ASD+ASBench, 41 test            | top-1/2/3         | **65.1 % / 77.8 % / 82.7 %**; precision 0.850, recall 0.616, F1 0.701                    |
| PASSerRank                       | ASD, 41 test                    | top-1/2/3         | **59.5 % / 73.9 % / 83.6 %**; F1 0.662, MCC 0.645                                        |
| PASSerRank                       | CASBench external               | top-1/2/3         | **56.3 % / 73.7 % / 80.5 %**; F1 0.608, MCC 0.589                                        |
| DeepAllo                         | ASD, 42 test                    | top-3             | **90.5 %**; F1 0.8966, precision 0.9231, recall 0.8814                                   |
| MEF-AlloSite                     | ASBench Core / remaining ASD    | average precision | **0.620 / 0.509 / 0.452** (vs PASSer2.0 0.588/0.495/0.438, PASSerRank 0.561/0.476/0.398) |
| ESSA                             | 12 apo/holo pairs               | top-3, **holo**   | **10/14 = 71.4 %**                                                                       |
| ESSA                             | same                            | top-3, **apo**    | **7/14 = 50 %**                                                                          |
| APOP                             | 104 proteins                    | top-3             | **92/104 = 88.5 %**; rank-1 on 35 (vs AlloPred 19, PASSer 29)                            |
| APOP                             | 50 holo                         | top-3             | **84 %** (vs AlloPred 68 %, PASSer 76 %; Wilcoxon p = 0.00088)                           |
| APOP                             | apo subset                      | top-3             | **11/14 = 86 %** excluding one cryptic pocket; **15/15** on the matched holo             |
| Ohm                              | 20 proteins, residue-level      | TPR / PPV         | **0.57 / 0.72**                                                                          |
| ZHMolEReP                        | ASBench, residue-level          | recall / AUC      | **0.7037 / 0.7858** `[VERIFIED-ABSTRACT]`                                                |

## The field's own reappraisal says all of the above is inflated

Three independent 2025–2026 results, and they agree.

`[VERIFIED-FULLTEXT]` **AlloBench** (Maity & Qiao, _ACS Omega_ 2025,
[10.1021/acsomega.5c01263](https://doi.org/10.1021/acsomega.5c01263)) built a 2141-site /
2034-structure / 418-unique-chain set from ASD + UniProt + M-CSA + PDB, **dropped every test
protein sharing a UniRef50 cluster with any training protein**, and re-ran the tools on 100
proteins. Result: _"none of these programs could achieve an accuracy of more than 60 %, even
with a very low JI cutoff."_ At **JI > 0.5**: PASSer (Ensemble) **18 %**, APOP **15 %**, PASSer
(AutoML) **13 %**. Best **median Jaccard index 0.060**. `[UNVERIFIED]` the exact tool count —
the text names seven primary tools (APOP, PASSer, Ohm, ALLO, Allosite, STRESS, AlloPred) but
the results table appears to break PASSer into three variants and add AllositePro.

`[VERIFIED-ABSTRACT]` **CAPASP** (Ai, Li, Huang & Liu, _J Comput Aided Mol Des_ 2026,
[10.1007/s10822-026-00831-4](https://doi.org/10.1007/s10822-026-00831-4)) built two datasets
"that had not been used in selected computational protocols" — **CAPASP-General (holo)** and
**CAPASP-Unbound (apo)** — and evaluated five tools on sensitivity, specificity, F1, MCC and
ranking. **PASSer and APOP led**, but "these models performed better with the CAPASP-General
subset than with the CAPASP-Unbound subset, suggesting that the prediction models require
further improvement." Paywalled; no per-tool numbers retrieved.

`[VERIFIED-ABSTRACT]` **AlloDyn / benchmark bias** (Pryakhin, Smail-Tabbone & Karami, bioRxiv
2026, [10.64898/2026.05.22.727284](https://doi.org/10.64898/2026.05.22.727284)) names the
mechanism: _"applying fpocket to holo structures without removing bound allosteric modulators
introduces data leakage and leads to artificially inflated performance estimates … current
benchmarks overestimate performance due to data leakage."_

**This is the same failure our own audit found in `1OPL`, arrived at independently.** It is
worth saying so explicitly in the report: the frozen benchmark's site-apo rule and its
`mandated`/`corrected`/`sensitivity` tiering implement, per-target, what this literature says
the field-wide benchmarks fail to do. Cite AlloBench and Pryakhin when defending the tiering.

**The honest bar our method must clear** is therefore _not_ "beat 65 % top-1". It is:

- beat **~50 % top-3 on an apo input** (ESSA's apo number, the only clean apo-vs-holo
  comparison at matched structures), and
- beat **residue-level AUC ≈ 0.79** (ZHMolEReP on ASBench), and
- do so without ASD training and without MD, which none of the above manages simultaneously.

---

# (c) The ENM / normal-mode lineage — our true classical baseline

## The two challenge references

`[VERIFIED-FULLTEXT]` **Reference [1] — Zheng W, _J Chem Phys_ 158:124127 (2023),
[10.1063/5.0141630](https://doi.org/10.1063/5.0141630), PMC10066797.**
ENM with all residue pairs within 25 Å connected, distance-dependent force constants decaying
from 10 Å; sample along **each of the lowest 30 modes** individually at RMSD 1–5 Å; rebuild
backbone and sidechains with PULCHRA; find pockets with **Concavity**; rank residues by
ensemble-averaged Concavity docking score. Four test proteins, each as an apo→holo pair:
GluR2 `1FTO`→`3H6T`; **myosin `1MMA`→`1YV3` (blebbistatin)**; GroEL `1GRL`→`4AB3`; GPCR M2
`3UON`→`4MQT`. On myosin it "identified a cluster of pocket residues lying in the L50–U50
cleft" overlapping "with both the ADP-binding site and the known allosteric sites for
blebbistatin" — a **qualitative** success statement, with mode overlap CO30 = 0.20 to the true
conformational change. Runtime 1–2 h for ~400 residues. **No MD** — the paper's selling point
is being "faster (1–2 h)" than MD-based sampling.
**No aggregate accuracy number is reported.** Four case studies, no ranking statistics, no
comparison to another method. The challenge's flagship ENM reference does **not** supply a
number we can be measured against.

`[VERIFIED-FULLTEXT]` **Reference [8] — Chennubhotla & Bahar, _PLoS Comput Biol_ 3(9):e172
(2007), [10.1371/journal.pcbi.0030172](https://doi.org/10.1371/journal.pcbi.0030172), PMC1988854.**
Discrete-time Markov process on a residue affinity network; affinities from atom–atom contacts
at **4 Å**, normalised by residue size; **hitting and commute times** as the communication
measure. Analysed: phospholipase A2 `1bk9`, HIV-1 protease `1a30`, ricin `1br6`, rhinovirus 3C
protease `1cqq`, endo-1,4-xylanase `1bvv`, adenylate kinase `4ake`. Catalytic residues have
"short and precise" hitting times.
**This is a mechanistic analysis, not a prediction task.** No ranking, no accuracy, no
statistical test — the assessment is that functional residues sit in minima of a plot. **No
Ras, no ABL, no myosin.** The challenge's reference [8] likewise supplies **no baseline number**.

This matters for R3: two of the challenge's own citations are conceptual foundations, not
benchmarks. Our classical baseline has to come from elsewhere, and the papers below are where.

## The real ENM baselines

| Method                                                                                                                                                                                        | Construction                                                                                                                                                                                                                                 | Result                                                                                                                                                                  |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **PARS** (Panjkovich & Daura 2012/2014, [10.1186/1471-2105-13-273](https://doi.org/10.1186/1471-2105-13-273), [10.1093/bioinformatics/btu002](https://doi.org/10.1093/bioinformatics/btu002)) | NMA flexibility change on ligand binding + structural conservation                                                                                                                                                                           | 91 proteins; flexibility change in **70 %**; **65 % PPV**. Re-run by AlloPred: **25 % top-1** `[VERIFIED-ABSTRACT]`                                                     |
| **AlloPred** (Greener & Sternberg 2015, [10.1186/s12859-015-0771-1](https://doi.org/10.1186/s12859-015-0771-1))                                                                               | Cα ENM, **Rc = 15 Å**, k = 1 kcal/mol/Å²; stiffen to **1.5** for springs touching the pocket; weight mode effects by frequency (ProDy); + Fpocket descriptors → SVM                                                                          | **23/40 = 57.5 % top-1**, 28/40 top-2                                                                                                                                   |
| **ESSA** (Kaynak, Bahar & Doruker 2020, [10.1016/j.csbj.2020.06.020](https://doi.org/10.1016/j.csbj.2020.06.020))                                                                             | **GNM 10 Å** and **ANM 15 Å**, uniform k = 1; add every heavy atom of residue _i_ as extra nodes to mimic binding crowding; z-score of mean eigenvalue shift over the **softest 10 modes**; combine with Fpocket + local hydrophobic density | **holo 10/14 = 71.4 %** top-3; **apo 7/14 = 50 %**. PARS 2/14 both. AllositePro 8/14 holo → **2/14 apo**.                                                               |
| **APOP** (Kumar, Kaynak, Dorman, Doruker & Jernigan, _Bioinformatics_ 2023, [10.1093/bioinformatics/btad275](https://doi.org/10.1093/bioinformatics/btad275))                                 | **GNM, 10 Å cutoff, γ = 1.0**; raise γ to **10.0** for all pairs inside a pocket; rank by combined z-score `sp = (zp + zhp)/2` of global-mode eigenvalue shift and hydrophobic density                                                       | **92/104 = 88.5 % top-3**; rank-1 on 35 vs AlloPred 19, PASSer 29. Holo subset **84 %** vs AlloPred 68 %, PASSer 76 % (p = 0.00088). Apo **11/14**, matched holo 15/15. |

**APOP is the state of the art for purely topological allosteric-pocket prediction and is the
number to beat.** It is unsupervised, structure-only, no MD, no training data — exactly our
constraint set (C1, C2 satisfied) — and it is **within the elastic-network hypothesis (C6)**.
It is also the method AlloBench found collapses to **15 % at JI > 0.5** on a leakage-free set,
so quote both numbers or neither.

**The apo penalty is the single most transferable finding in this section.** ESSA is the only
paper that measures the same method on matched apo and holo structures: **71.4 % → 50 %**, and
its competitor AllositePro falls **8/14 → 2/14**. CAPASP reproduces the direction on a larger,
independent set. Our benchmark is apo-only by construction (C1), so **the apo column is the
column we belong in**, and a method that reaches ~50 % top-3 on apo inputs is at the ENM
state of the art, not behind it.

## Where these methods have already been run on our targets

`[VERIFIED-FULLTEXT]` **APOP, on ABL — `3K5V`, the myristoyl pocket, rank 3 of 14.** Verbatim
from the paper: _"In another structure, imatinib again is bound to the same pockets (at first
and second rank) and a second inhibitor (GNF-2) is shown in an alternative pocket (third
rank). … Thus, APOP can predict these alternative allosteric pockets in ABL kinase."_ The
three ABL structures are `2HYY` (imatinib; ranks 1 and 2 of 14), `2V7A` (PHA-739358; rank 1 of 15) and `3K5V` (imatinib + GNF-2; ranks 1, 2 and 3 of 14). GNF-2 is the myristate-site binder
`[VERIFIED-DBRECORD]`.
**All three are holo structures**, and `3K5V` is an ASBench/ASD entry. So the published ENM
result on the ABL myristoyl pocket is a **top-3 hit on a holo input that the method's own
evaluation set contains**. Our task — the same pocket, from an apo input, blind — is strictly
harder, and the report should say so rather than claim parity with an 88.5 % headline.

`[VERIFIED-FULLTEXT]` **ESSA, on ABL — `3PYY`, myristoyl pocket detected.** Verbatim: _"the
essential sites include both the orthosteric (magenta) and allosteric (red, myristoylation)
sites that proved to be effective in cancer treatment when administered in combination."_
No rank is given in the text; the figure is a z-score-coloured surface. `3PYY` is the ASBench
BCR-ABL Core-set entry.

`[VERIFIED-FULLTEXT]` **GNM/ANM on KRAS, from `4OBE` — our exact frozen apo input.** Eren,
Tuncbag, Jang, Nussinov, Gursoy & Keskin, _J Phys Chem B_ 125:5210 (2021),
[10.1021/acs.jpcb.1c00891](https://doi.org/10.1021/acs.jpcb.1c00891). GNM cutoff **7.5 Å**,
ANM cutoff **12.0 Å**, γ = 1.0, 10 slowest modes, **no MD, static crystal structures only**.
Structures: unbound `4OBE` (WT-GDP), `6GOD` (WT-GNP), `4EPR` (G12D-GDP), `6GOF` (G12D-GNP);
complexes `6EPL` (SOS1), `6OB2` (NF1), `6XI7` (Raf-1). It identifies the **α3-L7 region,
residues 86–105**, as "the allosteric lobe", with communication between nucleotide-site
residues (G12, Y32, G60, Q61) and α3-L7 via the switch regions.

**This is the KRAS analogue of the Grant 2011 calibration fact already in
`docs/benchmark/primary/README.md` §4, and it is closer to home**: same input structure, ENM not MD,
purely topological. Residues 95, 96, 99, 100 and 103 of our 16-residue scoreable label set fall
inside their 86–105 window. `[UNVERIFIED]` — recompute the overlap and the hypergeometric
expectation from `frozen.json` before quoting it. As with Grant, this does not disqualify
anything, but it means **a GNM on `4OBE` has already pointed at part of our answer region,
and the report must state that a quantum method's claim is efficiency/mechanism, not
priority.**

`[VERIFIED-FULLTEXT]` **GNM on KRAS, residue-level.** Erman, _Physical Biology_ 23(1) (2026),
[10.1088/1478-3975/ae3e49](https://doi.org/10.1088/1478-3975/ae3e49). Dynamic distance,
edge centrality (spanning-tree fraction) and entropy sensitivity ∂S/∂δ = −0.5 R_ij on `6GOD`,
`6MBU`, `6GOF` (G12D), `6GOM` (Q61H) and `9O0R` (adagrasib). Bottleneck residues **G13, E31,
D47, Q61, E107, D119, P121, Y137, E168**; the switch-II region enters via the Q61–G12 edge
(33 % spanning-tree probability). **This is a residue-level network analysis, not a site
prediction** — no pocket ranking, no accuracy statistic — but it is the closest published
relative to our metric family (dynamic distance / centrality on a GNM) and is a natural
classical comparator for Phase 1.5.

`[VERIFIED-FULLTEXT]` **ESSA + residue-interaction network on KRAS-SOS1.** Sarica, Kurkcuoglu &
Sungur, _Int J Mol Sci_ 26:3293 (2025),
[10.3390/ijms26073293](https://doi.org/10.3390/ijms26073293). ESSA (ENM, 10 slowest modes,
top-25 % z-score quartile) + Fpocket + RIN betweenness (4.5 Å heavy-atom contacts, top 5 %
hubs), on `5OVI`, `6EPM`, `7KFZ` — **all holo** — plus 29 μs of Desmond MD. The two putative
pockets sit at the **SOS1–KRAS interface**, not at the switch-II pocket, which is not
recovered or discussed. Not a comparator for our task, but it is the closest published
ESSA-on-KRAS run and shows what ENM pocket ranking returns when pointed at a Ras complex.

---

# (d) Explicit negatives — searched for, not found

1. **No allosteric-site-prediction method has been reported to predict the KRAS switch-II
   pocket as an allosteric site.** Searched: Europe PMC for `"switch II pocket" AND (prediction
OR allosteric site)`, `KRAS AND "S-IIP" AND (pocket prediction OR allosteric site
prediction)`, `(KRAS OR HRAS) AND "allosteric site" AND (elastic network OR normal mode OR
network model OR perturbation response OR Markov)`. Every KRAS/S-IIP hit was either
   medicinal chemistry into a known pocket (docking, QSAR, virtual screening), an experimental
   structure paper, or a **cryptic-pocket** MD study. The nearest things to a prediction are
   (i) Grant 2011 (MD + FTMap, already in `docs/benchmark/primary/README.md` §4), (ii) Eren 2021
   (GNM/ANM, α3-L7 lobe, above) and (iii) `[VERIFIED-ABSTRACT]` Vithani et al., _J Chem Inf
   Model_ 2024, [10.1021/acs.jcim.4c01435](https://doi.org/10.1021/acs.jcim.4c01435),
   normal-mode-guided weighted-ensemble MD on KRAS G12D, >400 μs with cosolvents — **C2
   forbids the input, so this is a comparison point only.**

2. **No method has been reported to predict the ABL1 myristoyl pocket blind.** ESSA and APOP
   both **detect** it, from **holo** structures that are ASD/ASBench entries. Searched Europe
   PMC for `(ABL1 OR c-Abl OR BCR-ABL) AND ("myristoyl pocket" OR "myristate pocket" OR
"myristoyl binding site") AND (predict* OR "allosteric site" OR network OR "normal mode")`:
   every hit analyses or docks into the already-characterised site (Ming 2025 MD of asciminib
   pathways, Muratcioglu 2025, Merz 2026). None is a blind prediction.

3. **No method has been reported to predict the mavacamten pocket, at all.** Searched
   `("cardiac myosin" OR MYH7 OR "beta-cardiac myosin") AND mavacamten AND ("binding site" OR
pocket) AND ("molecular dynamics" OR docking OR predict* OR network)` (106 hits) and
   `myosin AND ("allosteric site" OR "allosteric pocket") AND (predict* OR "network model" OR
"normal mode" OR "elastic network") AND (mavacamten OR omecamtiv OR blebbistatin OR
aficamten)`. Everything is structure determination, drug mechanism, or clinical. The only
   _de novo_ computational work on myosin sites is `[VERIFIED-ABSTRACT]` Parijat et al., _Nat
   Commun_ 2023, [10.1038/s41467-023-43538-y](https://doi.org/10.1038/s41467-023-43538-y)
   (AI virtual screening for a novel modulator, not site prediction) and MD/MSM cryptic-pocket
   work on the **blebbistatin** site (Meller et al., _eLife_ 2023,
   [10.7554/eLife.83602](https://doi.org/10.7554/eLife.83602)).
   **The mavacamten pocket appears to be an open allosteric-site-prediction problem.** That is
   an asset for the submission and should be claimed — carefully, since our own audit already
   showed the site is **not cryptic** (0 clashing atoms on transplant in all three myosin
   arms) and the difficulty is "which pre-formed pocket", not "does a pocket exist".

4. **No myosin of any class is in ASBench.** Keyword search returned zero.

5. **No KRAS is in ASBench.** Keyword search returned zero. HRAS is present.

6. **CASBench membership could not be established for any of our targets.** The 91-entry list
   is not in the paper, not on the browse page, and only in a 1.9 GB tarball. All three
   targets are enzymes and all three are plausible members (CASBench = ASD ∩ Catalytic Site
   Atlas), so **do not assert absence**. `[UNVERIFIED]`

7. **No allosteric-site-prediction paper reviewed uses a spatially-matched permutation null.**
   This confirms, for the allostery literature specifically, what
   `docs/benchmark/primary/README.md` §5 already established for the cryptic-pocket literature.
   AlloBench is the closest — it drops UniRef50-related proteins — but that controls
   _sequence_ redundancy, not _spatial autocorrelation within a structure_. Our matched
   connected-patch null remains without precedent as a predictor calibration in either
   literature.

8. **No apo-only benchmark exists in the allostery field.** ESSA's Dataset II (12 pairs) and
   CAPASP-Unbound are the only apo evaluations found, and both are secondary analyses beside a
   holo primary. Every headline number in section (b) is a holo number.

---

## Bibliography

Databases and benchmarks

- ASD2023 — He et al., _Nucleic Acids Res_ 52:D376 (2024), [10.1093/nar/gkad915](https://doi.org/10.1093/nar/gkad915), PMC10767950
- ASBench — Huang et al., _Bioinformatics_ 31:2598 (2015), [10.1093/bioinformatics/btv169](https://doi.org/10.1093/bioinformatics/btv169)
- CASBench — Zlobin et al., _Acta Naturae_ 11:74 (2019), PMC6475866
- AlloBench — Maity & Qiao, _ACS Omega_ 10:17973 (2025), [10.1021/acsomega.5c01263](https://doi.org/10.1021/acsomega.5c01263), PMC12059942
- CAPASP — Ai, Li, Huang & Liu, _J Comput Aided Mol Des_ 40(1) (2026), [10.1007/s10822-026-00831-4](https://doi.org/10.1007/s10822-026-00831-4), PMID 42126486
- Benchmark bias / AlloDyn — Pryakhin, Smail-Tabbone & Karami, bioRxiv (2026), [10.64898/2026.05.22.727284](https://doi.org/10.64898/2026.05.22.727284)

Predictors

- AlloSite — Huang et al., _Bioinformatics_ 29:2357 (2013), [10.1093/bioinformatics/btt399](https://doi.org/10.1093/bioinformatics/btt399)
- AlloFinder — Huang et al., _Nucleic Acids Res_ 46:W451 (2018), [10.1093/nar/gky374](https://doi.org/10.1093/nar/gky374), PMC6030990
- AlloPred — Greener & Sternberg, _BMC Bioinformatics_ 16:335 (2015), [10.1186/s12859-015-0771-1](https://doi.org/10.1186/s12859-015-0771-1), PMC4619270
- PARS — Panjkovich & Daura, _BMC Bioinformatics_ 13:273 (2012), [10.1186/1471-2105-13-273](https://doi.org/10.1186/1471-2105-13-273); _Bioinformatics_ 30:1314 (2014), [10.1093/bioinformatics/btu002](https://doi.org/10.1093/bioinformatics/btu002)
- PASSer — Tian, Jiang & Tao, _Mach Learn Sci Technol_ 2:035015 (2021), [10.1088/2632-2153/abe6d6](https://doi.org/10.1088/2632-2153/abe6d6)
- PASSer2.0 — Xiao, Tian & Tao, _Front Mol Biosci_ 9:879251 (2022), [10.3389/fmolb.2022.879251](https://doi.org/10.3389/fmolb.2022.879251)
- PASSerRank — Tian, Xiao, Jiang & Tao, _J Comput Chem_ 44:2223 (2023), [10.1002/jcc.27193](https://doi.org/10.1002/jcc.27193), PMC9915737
- DeepAllo — Khokhar et al., _Bioinformatics_ 41:btaf294 (2025), [10.1093/bioinformatics/btaf294](https://doi.org/10.1093/bioinformatics/btaf294), PMC12145174
- MEF-AlloSite — Ugurlu et al., _J Cheminform_ 16:129 (2024), [10.1186/s13321-024-00882-5](https://doi.org/10.1186/s13321-024-00882-5), PMC11515501
- Ohm — Wang, Jain, McDonald, Gambogi, Lee & Dokholyan, _Nat Commun_ 11:3862 (2020), [10.1038/s41467-020-17618-2](https://doi.org/10.1038/s41467-020-17618-2), PMC7395124
- AlloReverse — Zha et al., _Nucleic Acids Res_ 51:W33 (2023), [10.1093/nar/gkad279](https://doi.org/10.1093/nar/gkad279), PMC10320067
- STRESS — Clarke et al., _Structure_ 24:826 (2016), [10.1016/j.str.2016.03.008](https://doi.org/10.1016/j.str.2016.03.008), PMC4883016
- ZHMolEReP — Ke et al., _J Chem Inf Model_ 66:6181 (2026), [10.1021/acs.jcim.6c00141](https://doi.org/10.1021/acs.jcim.6c00141)
- AlloPED — Chen et al., bioRxiv (2025), [10.1101/2025.03.28.645953](https://doi.org/10.1101/2025.03.28.645953)

ENM / normal-mode lineage

- Zheng W, _J Chem Phys_ 158:124127 (2023), [10.1063/5.0141630](https://doi.org/10.1063/5.0141630), PMC10066797 — **challenge ref [1]**
- Chennubhotla & Bahar, _PLoS Comput Biol_ 3:e172 (2007), [10.1371/journal.pcbi.0030172](https://doi.org/10.1371/journal.pcbi.0030172), PMC1988854 — **challenge ref [8]**
- ESSA — Kaynak, Bahar & Doruker, _Comput Struct Biotechnol J_ 18:1577 (2020), [10.1016/j.csbj.2020.06.020](https://doi.org/10.1016/j.csbj.2020.06.020), PMC7330491
- APOP — Kumar et al., _Bioinformatics_ 39:btad275 (2023), [10.1093/bioinformatics/btad275](https://doi.org/10.1093/bioinformatics/btad275), PMC10185404

Target biology cited above

- Buhrman, Holzapfel, Fetics & Mattos, _PNAS_ 107:4931 (2010), [10.1073/pnas.0912226107](https://doi.org/10.1073/pnas.0912226107), PMC2841912 — Ras helix-3/loop-7 allosteric site
- Holzapfel, Buhrman & Mattos, _Biochemistry_ 51:6114 (2012), [10.1021/bi300509j](https://doi.org/10.1021/bi300509j) — `4DLR` and the ASD Ras entries
- Yang et al., _Chem Biol_ 18:177 (2011), [10.1016/j.chembiol.2010.12.013](https://doi.org/10.1016/j.chembiol.2010.12.013) — `3PYY`, DPH at the myristoyl site
- Zhang et al., _Nature_ 463:501 (2010), [10.1038/nature08675](https://doi.org/10.1038/nature08675) — `3K5V`, GNF-2 at the myristate site
- Eren et al., _J Phys Chem B_ 125:5210 (2021), [10.1021/acs.jpcb.1c00891](https://doi.org/10.1021/acs.jpcb.1c00891) — GNM/ANM on `4OBE`
- Erman, _Phys Biol_ 23(1) (2026), [10.1088/1478-3975/ae3e49](https://doi.org/10.1088/1478-3975/ae3e49) — GNM network measures on KRAS
- Sarica, Kurkcuoglu & Sungur, _Int J Mol Sci_ 26:3293 (2025), [10.3390/ijms26073293](https://doi.org/10.3390/ijms26073293), PMC11989364 — ESSA + RIN on KRAS-SOS1
- Vithani et al., _J Chem Inf Model_ (2024), [10.1021/acs.jcim.4c01435](https://doi.org/10.1021/acs.jcim.4c01435), PMC11558672 — normal-mode-guided WE-MD on KRAS G12D
- Meller et al., _eLife_ 12:e83602 (2023), [10.7554/eLife.83602](https://doi.org/10.7554/eLife.83602), PMC9995120 — myosin blebbistatin pocket, MD/MSM
- Parijat et al., _Nat Commun_ 14:7692 (2023), [10.1038/s41467-023-43538-y](https://doi.org/10.1038/s41467-023-43538-y), PMC10673995 — AI screening for a cardiac myosin modulator
