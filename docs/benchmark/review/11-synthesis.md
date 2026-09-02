# What must change, ranked

> **SUPERSEDED — 2026-09-02.** [`25-second-pass-synthesis.md`](25-second-pass-synthesis.md) audited this pass, and [`27-fourth-pass-synthesis.md`](27-fourth-pass-synthesis.md) is the current ranked list. This document stays unedited as the record of the first pass.

**Audit closed 2026-09-02.** Scope: the frozen primary benchmark, the frozen secondary
benchmark and the frozen evaluation protocol, re-examined against the organisers' four
answers and against the literature and databases as they stand today.

**Headline.** The three frozen layers hold. Nothing found here requires rebuilding one.
Twenty-one items need action, of which **five block scoring on the primary arms** and the rest
are corrections and additions. One finding is not a defect at all — it is a property of the
biology that changes what this benchmark can claim, and it belongs in the report before any
number.

---

## Disposition, as of the end of 2026-09-02

This section was added after the audit, and it is the only part of this file that is not the
audit. Every other section records what was found, unedited. **Read this section for what has
since been done, and the sections below for the evidence behind each decision.**

| Item | Disposition |
| --- | --- |
| 1.1 BCR-ABL1 chain | **done** — ADR 0029. `1OPL:B` is the frozen arm, non-confirmatory, four defects printed. The 22.89 Å is decomposed: the kinase domain alone fits at 1.08 Å |
| 1.2 Negative class (b) | **done** — ADR 0030, protocol v3. Pocket-rank test stays descriptive; `decoy_pockets_combined` adds a Fisher combination across the confirmatory family; the detector is re-frozen selecting on `n_decoys` alone |
| 1.3 Supersede ADR 0016 | **done** — ADR 0031. `cardiac_myosin_mandated` is frozen for the first time, `5TBY`:A → `9GZ2`:A, non-confirmatory, both defects measured |
| 1.4 Claim threshold | **done** — ADR 0032. A second confirmatory family: paired `compare_methods` against `cavity_volume`, same three arms, Holm over three, two-sided |
| 1.5 "Uniformly stripped" | **done** — ADR 0033, narrow reading. **A measurement changed the design**: residue 10 is a scoreable KRAS label, so a motif source would move it out of the positive class. No new frozen arm; a descriptive matched comparison on the 15-residue intersection instead |
| 2.x Corrections | **done**, except where verification refuted the audit. See `13-correction-verification.md`: item **2.13 is refuted** (Table 1 has 19 rows and the existing text is right), item **2.17(a) is refuted** (the DOI is 2026 in print), item 2.12's stated cause was wrong, and item 2.16 mixed two scopes |
| 3.1 Conservation column | **decided, not built** — ADR 0035. Jensen-Shannon in the Capra & Singh form, BLOSUM62 background, Henikoff weights, λ = 1/2, window heuristic **off**, Pfam 38.2 full alignments. Blocked on artifact size: PF07714 alone is 191 MB gzipped, so the pinned artifact must be the derived column plus the alignment hash. Coevolution rejected as a category error |
| 3.2 Substitution record | **done** — `../../report/substitutions.md` |
| 3.3 Rule-level redundancy | **done** — `../secondary/README.md` §7 limitation 14 |
| 3.4 Synthetic-effector gap | **done** — promoted to `../README.md` |
| 3.5 Negative-class false negatives | **done** — `../README.md` and `../secondary/README.md` §7 limitation 16 |
| 3.6 Clauses (ix)–(xii) on the primary set | **done** — `../primary/README.md` §1. **One correction to this audit**: (xi) now fails on **two** entries, `1OPL` at 3.42 Å and `5TBY` at 20.00 Å, not on `1OPL` alone. `5TBY` was not a frozen arm when the audit measured it |
| 3.7 Top-5 fragmentation | **done** — `top_5_components` in `score_arm`, reported never tested |
| 3.8 Literature-last-searched date | **done** — `../evidence/README.md` |
| 3.9 Missing structure factors | **done and verified** — `../secondary/README.md` §7 limitation 13. Re-measured: `-sf.cif.gz` returns 404 for `1IA8`, `1RTJ`, `1A9X`, `1VRT`, and 200 for entries that have them. Both halves of `hiv_rt` are in that list |
| 3.10 Degree and distance columns | **done** — declared in `../evaluation/manifest.yaml`, computed beside every per-arm score at v3 |
| 3.11 Protect `review/` | **done** — ADR 0034. The tree is protected; its own tools are exempt by an import-based **rule**, not a name list. Two new tests pin it. Seventh guarded route |
| 4. Extension | **partly done.** Clause (ii) was read for all 34 survivors (`14-clause-ii-literature-pass.md`): **13 pass, 5 fail, 16 unread** behind publisher paywalls. Seven passes carry a separate structural blocker. Honest count of new admissible arms: **zero**. Honest count of leads: **13**. The set is **not** re-frozen |

**Two things were also settled that this audit did not name.** c-Myc became a reported
deliverable (ADR 0036, superseding ADR 0020), which closes the last of the four minimum
targets. And the c-Myc numbering was re-derived from the deposited `_struct_ref_seq` rather
than from a retrieved value: chain A auth **900–981** ↔ P01106 **353–434**, offset **+547**.

**Both layers are frozen again, and both verify.** `uv run allo benchmark verify --set all`
exits 0 over six primary arms and nine secondary; `uv run allo evaluate verify --detect` exits
0 at protocol version 3 over fifteen arms and 777 decoy pockets. The recalibration reproduced
**thirteen of fifteen** arms' `size_ratio` and `alpha_star` to six decimal places and moved
only the two the input re-freeze changed. That was the pre-registered check, and it passing is
what says the two moved for a reason rather than by drift.

**Three measurements from the re-run are worth carrying into the report.**

- **The organisers' chain B is a harder arm to calibrate than chain A was.** Its matched-patch
  type-I rate is 0.054 / 0.071 / 0.069 / 0.079 across λ = 4–20 Å against chain A's
  0.059 / 0.066 / 0.069 / 0.075, so its `size_ratio` rose from 1.0960 to 1.2073.
- **The 20 Å homology model is the best-calibrated arm in the set**, inside the binomial band
  at every correlation length, while the *measured* myosin structure is below it at two. Read
  it correctly: a calibrated null says the matched-patch construction works on that graph. It
  cannot see that the graph is largely invented.
- **The same twelve myosin labels form (8, 4) components on `9GZ3` and (7, 4, 1) on `5TBY`.**
  The label sets are identical, so the difference is entirely the contact graph. It is the
  long-range Jaccard of 0.471 seen from the label set's own side.

**One cost of the detector re-freeze, stated because it is a cost.** A decoy lining is smaller
than the label set on 15 of 15 arms at a median ratio of **0.412**, against 0.55 at the
version-2 settings. The null gained replicates and lost comparability at the same time. That
was accepted because the per-arm test is descriptive at version 3 and the decision runs on the
combination (ADR 0030).

**What is not done.** The conservation column (3.1) is decided and unbuilt, blocked on artifact
size. The descriptive 15-residue matched comparison ADR 0033 calls for belongs to Phase 2 and
has not run.

---

## 0. The finding that is not a defect

**For an allosteric site that works by a conformational switch, no apo structure carries the
coupled conformation, because carrying it is what binding causes.**

Measured on BCR-ABL1, exhaustively. Six PDB entries model more than the ABL kinase domain.
Every one with the SH3-SH2 clamp docked on the C-lobe has the myristoyl pocket filled — five
for five. Every one with the pocket empty has the SH2 domain on the N-lobe instead — two for
two. The clamp docks only when the pocket is filled.

The state this benchmark wants is the state the switch exists to prevent. That is not a
curation failure and no better structure will appear. It caps what the BCR-ABL1 disease area
can demonstrate, and any apo-input benchmark on a switch-type allosteric site inherits it.

**Put it in `docs/report/` as a scope statement, not as a caveat on one arm.**
`01-bcr-abl1-chain.md` §8.

---

## 1. Blocks scoring on the primary arms

### 1.1 The BCR-ABL1 chain choice needs an ADR — **ADR required**

The organisers direct teams to `1OPL` chain B. The frozen arm uses chain A. Measured, neither
is clean and the trade is not close to symmetric.

| | `1OPL:A` (frozen) | `1OPL:B` (organisers) | `2G2H:A` (comparison arm) |
| --- | --- | --- | --- |
| myristoyl pocket empty | **no**, 16 of 20 labels contacted at 3.29 A | yes, nearest 16.0 A | yes |
| SH3-SH2 clamp | present, and 2 of its 7 kinase contacts are pocket labels | **absent** — no SH3, SH2 on the N-lobe | absent |
| RMSD to the holo `5MO4:A` | 0.98 A | **22.89 A** | 1.78 A |
| coordinates | individual B-factors, 3041 distinct values | **rigid-body placed, 3 group B-factors**, mean B 170.7 | individual, 2.00 A |
| labels modelled | 20 of 20 | 17 of 20 | 18 of 20 |

The coordinate-quality row is the strongest and it is the depositors' own statement, in
`_refine.details` of the deposited file: "only overall domain B-factors were applied to
molecule B, whereas individual B-factors were refined for molecule A". Under C6, which makes
contact topology the object the method rests on, chain B's residue contacts are properties of
`1OPK`'s geometry plus a domain placement.

**Recommended:** report `1OPL:B` because the organisers designated it, non-confirmatory, with
all four defects printed beside it. Keep `2G2H:A` as the arm where methods are compared. Do
not substitute `4XEY:B`, which is better coordinates for a state that is wrong either way.
The ADR must state which arm is which and why, because an organiser instruction and a
measurement point different ways. `01-bcr-abl1-chain.md`.

### 1.2 Negative class (b) has no valid per-arm test — **ADR required, protocol version 3**

`CHALLENGE.md` §4.1 names non-functional surface pockets as half the success criterion. Three
constructions were measured against the ADR 0018 calibration gate. All three fail on the
confirmatory family.

| construction | measured type-I rate | verdict |
| --- | --- | --- |
| pocket permutation (frozen) | 0.000-0.032 | conservative; needs `delta >= 2.49` for 80 % power **at any decoy count** |
| residue-level rank test | **0.132-0.384** | anti-conservative by 3x to 8x. Worse than the unmatched null the protocol already rejects |
| size-matched patch inside the decoy union | not computable | on both KRAS arms **no decoy pocket is as large as the label set** |

**Recommended:** declare a Fisher or Stouffer combination across the confirmatory arms as the
tested form of negative class (b). Its minimum attainable p is **0.021** on the frozen
detector and 0.0014 on the loosest setting measured. Label it an intersection-null test.
Separately, re-freeze the detector settings selecting on `n_decoys` alone — that also repairs
the `bcr_abl1_corrected` site pocket, which currently covers two thirds of its label set.
`04-decoys-and-power.md`.

**This supersedes item 1 of `07-metrics-audit.md`**, which recommended the residue-level test
before the calibration ran.

### 1.3 ADR 0016 must be superseded — **ADR required**

Its blocking condition, "the organisers answer question (a)", has occurred. The answer clears
the label blocker completely: all twelve mavacamten labels transfer from `9GZ2` onto `5TBY`
with none unmapped. Both input blockers stand, and both are now measured:

- **No unique fold-general source rule.** PROSITE PS00016 matches twice in MYH7 and once in
  KRAS, so `active_site` raises. A myosin family motif triple is available and validated at
  Jaccard 0.48-0.52 against the ligand-derived source, with a 5.9 A centroid offset.
- **The contact topology is largely invented.** Against the 3.4 A cryo-EM `9GZ3`, `5TBY`'s
  long-range contact graph (`|i-j| >= 5`) agrees at **Jaccard 0.471**, recovering 57 % of
  measured edges. The fold is right — pairwise distances agree at Spearman 0.972 — and the
  graph is not.

**Recommended:** keep `9GZ3`→`9GZ2` as the scored arm; decide in the ADR whether to expose
`5TBY:A`→`9GZ2:A` as a reported, non-confirmatory arm with both numbers printed.
`02-cardiac-myosin.md`.

**Also record:** ADR 0016 forbids "a myosin-only motif", but every entry already in
`CATALYTIC_MOTIFS` is a family motif — `PTP` is PROSITE PS00383, `GDD` is an RdRp motif. The
prohibition is stricter than the repository's own precedent.

### 1.4 The claim threshold and the confirmatory family disagree — **ADR required**

ADR 0025 and `evaluation/README.md` §13 make "beat `cavity_volume`" the claim.
`evaluation/README.md` §8 makes everything except the three matched-patch tests descriptive
and not FWER-protected. So the load-bearing comparison has no multiplicity control, across
nine required baselines.

**Recommended:** declare a second confirmatory family — the paired `compare_methods` test
against `cavity_volume`, three `corrected` arms, Holm over three — and label every other
baseline comparison descriptive. `07-metrics-audit.md` item 2.

### 1.5 The ligand-derived source question is unsettled — **decide before scoring**

The organisers wrote that "all non-protein residues and ligands must be uniformly stripped".
**Seven of the fourteen arms derive the propagation source from a ligand in the apo entry**,
seven from a sequence motif. The split cuts across both sets and both tiers, so no partial fix
exists.

Under the narrow reading — "stripped" scopes the node set — nothing changes, and the
repository already complies. Under the wide reading, half the benchmark needs a new source
rule.

**Recommended:** report the source rule per arm in the submission and run a motif-only
sensitivity arm on KRAS, whose P-loop is a single unique PS00016 match at residues 10-17. That
converts an ambiguity into a measurement. `01-bcr-abl1-chain.md` §5,
`10-cross-set-consistency.md` §4.

---

## 2. Corrections — a stated fact is wrong

Each is a documentation change. None moves a frozen number.

**Ten of these were re-verified against primary sources on 2026-09-02, after this list was
written. [`13-correction-verification.md`](13-correction-verification.md) is the record. Five
stand exactly, four need a narrower statement, and one is refuted — the correction it proposed
would have put a wrong number into a freeze.** The rows below carry the verified wording.

| # | Where | What is wrong | What is right |
| --- | --- | --- | --- |
| 2.1 | `secondary/README.md` §3, `secondary/evidence/databases.md` | "ASD is not reachable as a data source" | **ASD is reachable.** Twelve release archives, 143 687 774 bytes = 143.7 MB, on disk and re-measured. The expired deployed certificate is real. **Two narrowings from `13`:** `<a href>` elements *do* exist in `download.js`, but only in a logged-in branch an anonymous client never reaches, and the anonymous path is the `dataRecord2023` JavaScript array; and CT logs hold two current `*.shsmu.edu.cn` certificates, so the certificate was renewed at the CA and not deployed on this host — do not write "has not been renewed". ASD states a licence, verbatim "ASD contains data for research use only. Users will not be allowed to distribute the data to a third party", so the archives stay untracked |
| 2.2 | `docs/targets.md` | `5MO4` "models auth 83-531 continuously" | 429 residues with **two gaps, 296-297 and 402-419**. No label falls in either, so no frozen number moves. `5MO4` is the holo for both BCR-ABL1 arms |
| 2.3 | `primary/README.md` §4a | "three of the five sit in different space groups" | **Two.** `kras_g12c_mandated` and `bcr_abl1_corrected`. Cardiac myosin is cryo-EM and has no crystal form |
| 2.4 | `primary/README.md` §4a | the six secondary arms below 0.3 A "share a space group in five of six" | One of the six is a cryo-EM pair. Of the **five crystallographic** pairs, **three** share one |
| 2.5 | `primary/README.md` §1 | clause (ii) tagged `[IN-DOMAIN]` | The evidence document tags it `[IN-DOMAIN + REPOSITORY POLICY]`. Adopt that in both places |
| 2.6 | `primary/README.md` §1 | "No formal definition ... contains a minimum separation" | **Partly false.** Kincore defines a Type IV allosteric kinase ligand by minimum distances >6.5 A from the hinge and C-helix-Glu(+4) (doi:10.1093/nar/gkab920). Kinase-specific and ligand-to-landmark. Record it; do not adopt it |
| 2.7 | `primary/README.md` §1 | site-apo "is the majority one in the field" | CryptoBank (doi:10.1126/sciadv.ady6364) applies a global entry-level apo filter over 6 M alignments. Narrow the claim to "the majority among resources that annotate apo/holo per binding site" |
| 2.8 | `evaluation/manifest.yaml` | three omission rationales its own `AUDIT.md` withdrew | MCC/F1 still quotes Utgés & Barton as the argument; Jaccard still states a ceiling of 0.31 against a measured 0.4545; DVO carries the clause the audit called false. `README.md` was fixed and the manifest was not |
| 2.9 | `evaluation/README.md` §12.4 | variogram-matched surrogates named "the right design" | A 2026 head-to-head puts them at 29.2-36.3 % false-positive rate, worse than the spin test, with eigenmode-rotation surrogates at 5.2-5.3 % (doi:10.1162/IMAG.a.71). **Confirmed in `07a`: all five digits exact, and the reversal is safe** |
| 2.10 | `primary/audit/bcr-abl1.md` §4 | calls K29R/E30D "phantom" while its own table lists them | The substitutions are real. The diff rows are written in isoform IB numbering while `_struct_ref` declares IA. Fix the frame, keep the rows |
| 2.11 | `secondary/README.md` §7.2 | "No new admissible target is below 272 residues" | Add "from that frame". The ASD frame returns candidates at 158 residues |
| 2.12 | `docs/targets.md` | `1OPL` RSRZ 22.18 %, 0.4th percentile | All four numbers are right and **the stated cause is wrong**. `13` retrieved PDBe's own validation XML: it reads **6.50 % / 24.6th percentile**, with an `XMLcreationDate` identical to RCSB's `report_creation_date` to the minute. The partners serve the **same** validation run; only PDBe's `validation/global-percentiles` REST endpoint is stale at 22.18 %. Do not write "different validation runs" — one fetch disproves it |
| ~~2.13~~ | `evaluation/README.md` §3.3 | ~~Vajda "8 of 19" is a wrong denominator~~ | **REFUTED by `13`. Change nothing.** Table 1 has **19** data rows, verified over three independent retrievals, and exactly 8 carry `Type = Allo`. The existing "8 of 19" is correct, and the proposed correction would have put 20 into a frozen document. Worth adding beside it: 19 sites over **18** distinct proteins, because HCV polymerase appears twice |
| 2.14 | `07-metrics-audit.md` §4.1, census row 35 | "Allo-Allo applies Bonferroni" to its AlphaMissense validation | **Misattributed.** The Bonferroni is real but it adjusts the attention-head **selection** t-tests. The AlphaMissense Welch test carries none. The repository's "0 apply any multiplicity correction" line still has to change; the reason given for it must not |
| 2.15 | `07-metrics-audit.md` census row 35 | Allo-Allo scores AUROC 0.95 | **Refuted in `07a`.** 0.95 is the Appendix-A baseline's AUROC, not Allo-Allo's |
| 2.16 | `07-metrics-audit.md` §3.2 | max MCC ≈ √(5/m) | The exact closed form is right and `13` re-derived it independently: `max MCC = sqrt(k(n−p)/(p(n−k)))`, maximal at `t = k` because the numerator collapses to `tn − kp` and the marginals are `t`-free. The shorthand **overstates**, by exactly `sqrt((n−5)/(n−p)) − 1`. **Narrowed:** say "up to 4.1 %". The audit's "0.491-0.642, not 0.50-0.67" mixes scopes — 0.67 needs an 11-residue label set, which is a *secondary* arm. On the five primary arms the shorthand runs 0.500-0.645 |
| 2.17 | `07-metrics-audit.md` §4.1 | "nine papers" above a ten-row table | The table has ten rows. **The other half of this item is refuted by `13`:** doi:10.1002/advs.202513641 has Crossref `issued` 2025-11-28 online but `published-print` February 2026, and Europe PMC gives `pubYear` 2026. Cite it as *Adv Sci* 2026;13(12):e13641, first published online 2025-11-28. The existing "2026" is right and flipping it to 2025 would make the citation worse |
| 2.18 | `evaluation/README.md` §4.3 | the distance baseline is "below chance on three of five arms" | True for the primary set, misleading for the benchmark. Across all fourteen arms **nine favour the "far" direction**, in which the plain baseline is above chance. Measured in `12-dataset-eda.md` §5 |

---

## 3. Additions — a real gap with no wrong statement behind it

| # | Add | Why |
| --- | --- | --- |
| 3.1 | **Conservation and coevolution as an apo-only confounder column** | `evaluation/README.md` §11 already names conservation as the fourth confounder and it reads `null`. It is sequence-only, so it clears C1 and C2. "Your hits are just the conserved residues" is the first objection a reviewer raises, and the repository currently cannot answer it. **The single highest-value addition in this audit** |
| 3.2 | **A one-page substitution record for the submission** | The organisers require documenting every substitution and its reason. Four exist — `6C1H`→`9GZ2`, `5TBY`→`9GZ3`, `4OBE`→`4LDJ`, `1OPL`→`2G2H` — each documented in a different file. A judge will look for one page |
| 3.3 | **Rule-level redundancy, as a thirteenth secondary limitation** | `chk1` sits in the `generalisation` tier and uses `{from_motifs: [VAIK, HRD, DFG]}`, the identical rule that locates BCR-ABL1's active site. Family-level disjointness is achieved; rule-level disjointness is not. Recorded nowhere |
| 3.4 | **The synthetic-effector gap, moved up to `benchmark/README.md`** | All fourteen arms use a synthetic small molecule. Classical allosteric enzymology — cooperativity and metabolite feedback — is untested across the whole benchmark. `secondary/README.md` §5.2 records it for its own set only |
| 3.5 | **The negative class's unknown false-negative rate** | Beltran 2026 (doi:10.1126/sciadv.aea2726) reports dozens of functionally allosteric surfaces in Src and that computational methods fail on them. A one-site-per-arm benchmark therefore has an unknown false-negative rate in its negatives. Disclose it; it argues for precision over recall |
| 3.6 | **Clauses (ix)-(xii) applied to the primary set as a reported diagnostic** | Measured here: (ix) passes on all fourteen arms, (xi) fails on `1OPL` alone. Cheap, and it closes the "different rules for different sets" objection |
| 3.7 | **A top-5 fragmentation statistic** | Nothing measures whether the top five residues are one place or five. `CHALLENGE.md` §4.2 asks for actionable output. Seq2Pocket's Pocket Fragmentation Index is a real published precedent, **confirmed in `07a`** (doi:10.64898/2026.01.28.702257). Do not carry `07`'s sentence about it as a verbatim quote — the paper does not use those words |
| 3.8 | **A "literature last searched" date in `evidence/README.md`** | The evidence base is dated 2026-08-20 to 2026-08-25. This audit re-searched on 2026-09-02 and found four materially new sources. Without a date the next reader cannot tell a real gap from a stale one |
| 3.9 | **Four X-ray entries have no released structure factors** | `1IA8`, `1RTJ`, `1A9X`, `1VRT`. Density validation is unavailable for both halves of `hiv_rt`. Record it as a difficulty axis |
| 3.10 | **`degree` and `distance_to_source` as reported confounder columns** | ADR 0025 prints three apo-only confounders beside every score. Two more separate label from background as strongly: degree reaches AUC 0.770 on `ns5b` and 0.751 on `mkp5`, distance reaches 0.932 on `hiv_rt` in its better direction. Both are free — the graph already holds them (`12-dataset-eda.md`) |
| 3.11 | **`docs/benchmark/review/` belongs in `PROTECTED_PATHS`** | The directory carries per-arm positive counts and, in `03-kras-mask.md`, five real label residues. C1 names the residue count directly. `extension-candidates.md` is a protected Markdown answer key on the identical argument. **The obvious fix was tried and fails**: `data/fetch_structure_evidence.py` writes into the same directory, so protecting the tree makes the runner gate flag the script's own output. Three options in `12-dataset-eda.md` §7. Needs a decision |

---

## 4. The extension question, answered

**Reachable today:** ASD, ASBench bulk files, RCSB, AHoJ-DB, CryptoBench, UniProt, Pfam. One
warning: `bindingmoad.org` now returns 200 and is **not** Binding MOAD — the domain was
repurposed.

**What ASD adds:** 3147 site records, 68 measured, **34 survive every clause the sweep could
measure** — 9 with an apo holding nothing but water. They close the gaps the current set
names: **13 carry physiological effectors** (AMP, GTP, His, Arg, acetyl-CoA and more) against
zero in the frozen set; three are under 272 residues, the smallest at 158; 61 Pfam families
appear, none a protein kinase; the size span rises from 0.86 to 1.06 dex and the organism
count from 4 to 20.

**What none of them has:** clause (ii). Every DOI is ASD's own curation reference and no paper
was read. At the measured 29 % kill rate that removes about ten. **The honest count of new
admissible arms today is zero. The honest count of new leads is 34.**

**Recommended:** do not re-freeze the secondary set for this submission. Adding arms re-runs
the seeded tier split and changes every existing assignment, which is a re-freeze rather than
a repair, and the clause (ii) reading work is not done. Record the 34 leads, correct the ASD
reachability claim, and leave the decision where the roadmap already puts it — Phase 5.
`09-extension-sweep.md`.

---

## 5. What this audit did not settle

- **Whether `5TBY`→`9GZ2` should be exposed.** Measured on both sides; the decision is an ADR.
- **Which reading of "uniformly stripped" the organisers meant.** Item 1.5. It can be asked.
- **Whether the detector settings should be re-frozen.** The measurement is in
  `04-decoys-and-power.md`; the decision is an ADR.
- **The converse crypticity fraction.** Still unreported in the literature, now shown to be
  computable from public inputs.
- **c-Myc.** ADR 0020's contract is untouched by anything here. `1NKP` still has no arm, and
  it is one of the four minimum deliverables.
- **`cardiac_myosin_mandated` and c-Myc are two of the four minimum targets, and neither has
  an arm in any freeze.** That is a conformance gap, not a statistical one, and it is the
  largest one open.

---

## 6. Method

Six agents ran in parallel against the frozen artifacts, and every quantitative claim above
was re-derived in this repository rather than taken from a summary. Delegation was not
trusted. Two delegated claims were **overturned by measurement**: the metrics audit's
per-residue permutation test failed its own type-I calibration (§1.2), and
`07a-metrics-fact-check.md` refuted one of that audit's census entries and corrected four
more of its statements (items 2.14 to 2.17).

Skills applied: `pdb-database` for every structural fact, `literature-review` and
`scientific-critical-thinking` for the two literature audits, `statistical-power` for the
decoy analysis, `exploratory-data-analysis` for the label-set descriptor sweep in
`12-dataset-eda.md`.

**What is measured and what is read.** Every number in `01`, `02`, `03`, `04`, `10` and `12`
came from a script run in this session. Every number in `05` to `09` came from a delegated
agent, and `05` and `07a` are the passes that checked them. Where the two disagree, the
measurement wins and the disagreement is recorded rather than resolved silently.
