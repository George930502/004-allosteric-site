# Reachable extension candidates — screened 2026-08-24, NOT admitted

**Status: a screening record, not part of the freeze.** Nothing here is in
`manifest.yaml` or `frozen.json`. The secondary benchmark remains the nine targets frozen on
2026-08-24. This file exists so that a re-freeze decision, if it is ever taken, does not have
to redo the screening.

**This file is an answer key.** It names real label residues, holo accessions and effector
component IDs for candidate arms. `tests/test_no_leakage.py` names it in `PROTECTED_PATHS` and
in `FROZEN_TOKENS`, exactly as `selection.json` is named, so no prediction-path module and no
experiment runner may open it. It is the **fourth** data route that bypasses the import graph.

**Why it was not acted on.** Adding arms re-runs the seeded size-stratified split, so every
existing tier assignment changes. Under the reasoning `README.md` §7.10 used to decline
reopening `usp7`, that is a re-freeze and a re-freeze is a decision, not a repair. Two further
blockers stand on the evidence itself, and they are stated in §7 below: `gdh` needs one more
literature pass on clause (ii), and three of the five apo entries have no primary citation.

**What it changes even if nothing is added.** The measured clause costs in §6 correct
`README.md` §7.1. Clause (ix) is the binding constraint, not clause (xii). On the 32
physiological-effector holo entries measured, clause (ix) kills 72 % and end-to-end survival is
3 of 32.

---


Run 2026-08-24. Read-only on the repo. Every accession, resolution, Pfam family and lining
measurement below comes from a live fetch or a file read in this session; nothing is recalled.

**Answer up front.** The supply claim in `docs/benchmark/secondary/README.md` §7 limitation 1 is **true but
mis-attributed**. Supply is binding, and the clause doing the binding is **(ix) single-chain
lining**, not the scarcity of published allosteric sites. Clause (ix) kills **23 of 32**
physiological-effector holo entries I measured (72 %) and **5 of 12** drug-effector candidates
(42 %); of those 32, exactly **3 survive every clause** (9 %). Clause (xii) is the cheaper kill
on the *pending* list only because that list is mostly protein kinases — on an unrestricted
frame it costs 12 %.

I found **5 further admissible targets** (4 clean, 1 conditional), taking the set from 9 to 14
— still half the 28 the power analysis asked for. **Three carry physiological effectors**
(FBP, AMP, GTP), which closes the gap §5.2 names. Clause (ii) then did its job on the way out:
it killed the one candidate that had passed every structural clause cleanly (`pdhk2`) and
confirmed the rejection of another (`p300`), whose own authors call the compound series
artifactual.

---

## 0. The blocked-family set, derived not guessed

| Source | File read | Pfam families |
| --- | --- | --- |
| primary `kras_g12c_*` | `docs/benchmark/manifest.yaml:272,295` | PF00071 |
| primary `bcr_abl1_mandated` | `manifest.yaml:316` | PF00017, PF00018, PF07714 |
| primary `bcr_abl1_corrected` | `manifest.yaml:343` | PF07714 |
| primary `cardiac_myosin_mandated` | `manifest.yaml:373` | PF00063, PF01576, PF02736 |
| primary `cardiac_myosin_corrected` | `manifest.yaml:418` | PF00063, PF02736 |
| secondary (9 arms) | `docs/benchmark/secondary/manifest.yaml:263…595` | PF00782, PF00069, PF00102, PF00856, PF01753, PF00349, PF03727, PF00078, PF06815, PF06817, PF00075, PF00998, PF00004, PF02359, PF02933, PF17862, PF02786, PF02787, PF25596, PF02142 |

MYH7 was **derived, not guessed**: the primary manifest already records `pfam:` for every arm
(added so clause (xii) is a test rather than a promise), so PF00063/PF01576/PF02736 is a file
read, not a lookup. 27 families are blocked in total.

---

## 1. Step 1 — the cheap kill on clause (xii)

Pfam resolved twice per accession and cross-checked: UniProt `xref_pfam`
(`https://rest.uniprot.org/uniprotkb/<ACC>.json?fields=xref_pfam`) and InterPro
(`https://www.ebi.ac.uk/interpro/api/entry/pfam/protein/uniprot/<ACC>/`). **The two sources
agreed on all 24** except p300, where UniProt lists PF08214 and InterPro PF29847 — a
difference that changes nothing, since neither is blocked.

### Verdict: 11 DEAD-ON-XII, 13 ALIVE

| # | Candidate | UniProt | Pfam (both sources) | (xii) | Colliding arm |
| --- | --- | --- | --- | --- | --- |
| 1 | `acc_bc` | Q00955 | PF00289, PF00364, PF01039, PF02785, **PF02786**, PF08326, PF21385 | **DEAD** | `ecoli_cps` (PF02786) |
| 2 | `cblb` | Q13191 | PF00097, PF02262, PF02761, PF02762 | ALIVE | — |
| 3 | `cdk2` | P24941 | **PF00069** | **DEAD** | `chk1` |
| 4 | `cgas` | Q8N884 | PF03281, PF20266 | ALIVE | — |
| 5 | `ck2a` | P68400 | **PF00069** | **DEAD** | `chk1` |
| 6 | `dhdps_cb` | Q9PPB4 | PF00701 | ALIVE | — |
| 7 | `fak1` | Q05397 | PF00373, PF03623, **PF07714**, PF18038, PF21477 | **DEAD** | `bcr_abl1` |
| 8 | `fh_mtb` | P9WN93 | PF00206, PF10415 | ALIVE | — |
| 9 | `fpps` | P14324 | PF00348 | ALIVE | — |
| 10 | `idh1` | O75874 | PF00180 | ALIVE | — |
| 11 | `kit` | P10721 | PF00047, **PF07714** | **DEAD** | `bcr_abl1` |
| 12 | `legumain` | Q99538 | PF01650, PF20985 | ALIVE | — |
| 13 | `map2k7` | O14733 | **PF00069** | **DEAD** | `chk1` |
| 14 | `mat2a` | P31153 | PF00438, PF02772, PF02773 | ALIVE | — |
| 15 | `mek1` | Q02750 | **PF00069** | **DEAD** | `chk1` |
| 16 | `melk` | Q99640 | **PF00069** | **DEAD** | `chk1` |
| 17 | `p300` | Q09472 | PF00439, PF00569, PF02135, PF02172, PF06001, PF09030, PF23570, PF08214/PF29847 | ALIVE | — |
| 18 | `pak1` | Q13153 | **PF00069**, PF00786 | **DEAD** | `chk1` |
| 19 | `pdhk2` | Q15119 | PF02518, PF10436 | ALIVE | — |
| 20 | `pfk_tbrucei` | O15648 | PF00365 | ALIVE | — |
| 21 | `pkm2_fbp` | P14618 | PF00224, PF02887 | ALIVE | — |
| 22 | `ptpn7` | P17706 | **PF00102** | **DEAD** | `ptp1b` |
| 23 | `pycr1` | P32322 | PF03807, PF14748 | ALIVE | — |
| 24 | `ripk1` | Q13546 | PF00531, **PF07714** | **DEAD** | `bcr_abl1` |

**Your prior is confirmed, with two corrections.** Nine of the ten canonical protein kinases
on the pending list are dead: five on PF00069 (`chk1`) and four on PF07714 (`bcr_abl1`).

- **RIPK1 is a serine/threonine kinase but carries PF07714, not PF00069.** Both sources say
  so. It dies against ABL1, not against CHK1. Assuming the fold from the substrate would have
  got this one wrong.
- **`pdhk2` is the kinase that survives.** PDK2 is a GHKL-fold (Bergerat) kinase —
  PF10436 `BCDHK_Adom3` + PF02518 `HATPase_c` — with no Pkinase domain at all. "Pending
  kinases are all dead" is false by exactly one arm, and that arm turns out to be admissible.
- **Two non-kinases also die**, which the prior did not anticipate: `ptpn7` (HePTP) on PF00102
  against `ptp1b`, and `acc_bc` on **PF02786** against `ecoli_cps` — the yeast acetyl-CoA
  carboxylase biotin-carboxylase domain and carbamoyl-phosphate synthetase share the ATP-grasp
  `CPSase_L_D2` family. That collision is invisible from the protein names.

---

## 2. Step 2 — screening the 13 survivors

Clauses were worked cheapest-first, **except** that clause (ix) was pulled forward once the
first two candidates showed it was the dominant killer and it is measurable offline from one
downloaded assembly. Method, for reproducibility:

- **(ix)** `https://files.rcsb.org/download/<PDB>-assembly1.cif.gz`, model 1, effector heavy
  atoms (HETATM only) vs all protein heavy atoms, 4.5 Å, grouped by author chain. Measured on
  the **biological assembly**, per §4 of the secondary README.
- **(iii)/(x)** labels transferred to the apo by the repo's own scheme — global BLOSUM62
  alignment with `open_gap=-11, extend=-1`, mirroring
  `allo.groundtruth.labels.align_numbering` (`src/allo/groundtruth/labels.py:53-77`) — then
  every non-water apo component measured against the mapped label residues.
- **(iv)** identity over aligned pairs from the same alignment.
- **active site** a `from_ligands` rule needs the component present in the *apo*; a
  `from_motifs` rule needs a PROSITE `PA` line that matches **exactly once** on the modelled
  apo chain (`src/allo/inputs.py:60-72,173-179`).

### 2.1 Verdicts

| Candidate | Deciding clause | Evidence (measured this session) |
| --- | --- | --- |
| `idh1` | **clause_ix_interface** | `5DE1`/`59D` asm1: 22 lining residues, **A:19 + B:3**. Two alternative holos fail the same way: `6BKZ`/`DWM` = A:21 + B:4; `6BKY`/`K32` = C:8 + D:8. The whole GSK321/ivosidenib class sits on the IDH1 dimer axis. The ledger's "19-residue label set" is the asymmetric-unit count — the false pass §7 limitation 3 warns about |
| `dhdps_cb` | **clause_ix_interface** | `7KKD`/`3VN` asm1: 20 lining residues, A:11 + F:9. The bis-lysine sits on the DHDPS tight-dimer axis |
| `fh_mtb` | **clause_ix_interface** | `6S43`/`KUE` asm1: 16 lining residues, A:6 + C:10 |
| `mat2a` | **clause_ix_interface** | `7RWG`/`7UN` asm1: 23 lining residues, A:13 + A-2:10 |
| `pycr1` | **clause_ix_interface** | `9P0R`/`A1CFJ` asm1: 12-13 lining residues, split ~6/6 across the dimer on every one of 10 copies |
| `legumain` | **effector is orthosteric** (clause (i)/(ii)) | `7FQI`/`WSN` asm1: 14 lining residues, single chain — but the list is `TYR41, ARG44, HIS45, **HIS148**, GLY149, GLU187, ALA188, **CYS189**, SER215…`. H148 and C189 are legumain's catalytic dyad; `WSN` carries a nitrile warhead. This is an active-site covalent inhibitor. Separately, the ledger's recorded rule `lig:NAG` is not an active site at all — NAG is the N-glycan |
| `cgas` | **ledger defect — cannot be screened as written** | `https://data.rcsb.org/rest/v1/core/entry/8TSN` → **HTTP 404, "No data found for entryId: 8TSN"**. Searching RCSB for component `A1AB0` returns exactly one entry, **`8VIE`, "2-PPA bound human TMEM175"** — a lysosomal cation channel, not cGAS. Both the holo and the effector in this row belong to a different protein. cGAS itself has 107 entries and excellent apos (`4MKP` 1.95 Å, `7FTJ` 1.46 Å), but every ≤2.5 Å ligand-bound entry I listed is an **active-site** (nucleotide-pocket) inhibitor. Needs a fresh holo before it can be screened |
| `p300` | **clause_x_apo_occupant** | `6PF1`/`OJ7` asm1: 18 lining residues, **single chain — passes (ix)**. But every CoA-bearing apo has a cryoprotectant in the pocket: `4PZR` — DMS[A1703] at **2.86 Å** of PHE1596 and within 4.5 Å of 9 of 18 labels, PEG[A1701] at 3.13 Å of TRP1436; `4PZS` — DMS[A1702] at 2.81 Å; `5LKZ` — GOL[A1708] at **2.53 Å** of ASP1507. The one apo that clears the pocket, `6V90` (2.04 Å, PASS on (iii)/(x)), holds no CoA — so `{from_ligands: [COA]}` is underivable there. A genuine double bind, not a search failure |
| `fpps` | **clause_x_apo_occupant** | `6N7Y`/`KFA` and `5JA0`/`FPP` both **single-chain (12 and 20 residues)** — (ix) passes. But every FPPS apo at ≤2.5 Å has an anion parked in the allosteric pocket's diphosphate subsite: `4XQR` PO4[F401] 2.87 Å from LYS57; `2F7M` PO4 2.63 Å; `4XQT` SO4[F404] **2.59 Å** from ASN59; `4XQS` SO4 2.95 Å. The bisphosphonate+IPP entries are worse — `4KQU` IPE at 2.75 Å of ARG60. See §5 for the one escape route |
| `cblb` | **ADMISSIBLE, with a stated assumption** | see §4 |
| `pdhk2` | **clause_ii_evidence** | passes every structural clause (see §4.7) and then fails on mechanism: the "allosteric" lipoyl pocket is the docking site of the enzyme's own physiological activator, the E2 L2 lipoyl domain |
| `pfk_tbrucei` | **conditionally admissible** — every structural clause passes, one new motif needed | see §4 |
| `pkm2_fbp` | **ADMISSIBLE** | see §4 |

### 2.2 What (xi) cost: nothing

Every recorded holo on the pending list passes clause (xi). Measured resolutions: `8QTG` 1.42,
`7KKD` 1.60, `6S43` 1.42, `6N7Y` 2.00, `7FQI` 1.45, `7RWG` 0.97, `6PF1` 2.32, `6LIL` 1.93,
`6QU3` 2.35, `9P0R` 1.49, `5DE1` 2.25, `1ZJH` 2.20 — all X-ray, all ≤ 2.5 Å. `8TSN` does not
exist. Resolution is not what is limiting this set.

---

## 3. Step 3 — sweeping beyond the 24

### 3.1 Routes actually reached

| Route | What was run | Result |
| --- | --- | --- |
| **RCSB full-text** (`https://search.rcsb.org/rcsbsearch/v2/query`) | 12 phrases — the ledger's recorded 5, plus `feedback inhibition`, `allosteric effector`, `allosteric regulation`, `homotropic`, `heterotropic`, `effector site`, `regulatory site` — filtered `resolution_combined ≤ 2.5`, `results_content_type: [experimental]` | totals: 411 / 225 / 93 / 32 / 28 / 69 / 24 / 398 / 9 / 15 / 2 / 17. **Union 1061 entries** |
| **RCSB GraphQL** (`https://data.rcsb.org/graphql`) | metadata for all 1061 | **380 distinct UniProt accessions** |
| **UniProt REST batch** | `xref_pfam`, length, organism, catalytic-activity flag for all 380 | 380/380 resolved |
| **RCSB per-accession** | full entry lists for 13 pending survivors + 12 new leads | ~700 further entries |
| **Assembly geometry** | 40+ biological assemblies downloaded and measured | see below |
| **PROSITE** (`https://prosite.expasy.org/<AC>.txt`) | PS00110, PS00433, PS00518, PS00124, PS00074, PS00627 | 6/6 retrieved; PA lines converted mechanically |
| **Crossref + Europe PMC** | DOI and abstract for 9 primary citations | 9/9 resolved |

A parallel harvest closed the remaining routes:

| Route | Endpoint that worked | Raw | After Pfam/known exclusions |
| --- | --- | ---: | ---: |
| **AlloBench** | `raw.githubusercontent.com/djmaity/allobench/HEAD/AlloBench.csv` (3.0 MB, flat repo, one CSV) | 2257 rows / 430 UniProt | 340 |
| **CASBench** | no download table; the real listing is at the undocumented `biokinet.belozersky.msu.ru/casbenchbrowse/all.php`, found in inline JS | 91 entries | 84 |
| **GtoPdb** | `guidetopharmacology.org/DATA/interactions.csv` v2026.2 → 963 rows `Type = Allosteric modulator` | 161 targets / 179 UniProt | 133, of which **7 enzymes, 0 new** |
| **AHoJ-DB** | `apoholo.cz/api/db/search?ligands=<CCD>` × 10 CCDs | 20 124 holo → 3020 UniProt, 1371 with ≥1 apo | used for apo verification, not discovery |
| **UniProt `cc_activity_regulation`** | 16 `stream` queries, `reviewed:true`, `database:pdb`, `length:[80 TO 700]` | 503 unique | **431 — the richest single route** |
| **Local prior-art clone** | `allosteric-benchmark/data/allo_tableS2.csv`; columns `pdb, name, allo_ligand, allo_lig_res, allo_site_residues, active_site_residues` — no UniProt, no DOI, no organism | 118 rows / 108 PDB | 84 |

Merged: **1049 unique UniProt → 865 after exclusions → 461 with a structural anchor → 78
curated**. Exclusions fired 119 times on Pfam alone (PF00069 × 50, PF07714 × 16, SH2/SH3+kinase
× 15). **GtoPdb is a dead route for this project** — ~95 % GPCR and ion channel; its 7 surviving
enzymes are PKLR, Arf6, SIRT3, SIRT6, PRMT3, PDE4D, NLRP3, none new. `allo_tableS2.csv` and every
AlloBench row were treated as **unverified third-party claims** and none was used as evidence —
only as a name to go and measure.

### 3.2 What the frame costs

Of the 380 accessions the full-text frame returned:

| | count | share |
| --- | ---: | ---: |
| blocked on clause (xii) | **47** | 12 % |
| already in `selection.json` | 37 | 10 % |
| **alive** | **313** | 82 % |
| …of those, catalytic and ≤ 650 aa | 152 | 40 % |

Top blocking families in the frame: PF00069 (15 accessions), PF07714 (10), PF00017 (4),
PF00102 (4), PF00998 (3). **Clause (xii) costs only 12 % of an unrestricted frame.** It looks
expensive on the pending list (46 %) purely because that list is a kinase pile.

### 3.3 Deliberately targeting the two named gaps

Sixteen holo entries with **physiological / metabolite effectors** were measured on clause (ix).

| Target | UniProt | Holo / effector | Res Å | Lining split (asm1) | (ix) |
| --- | --- | --- | ---: | --- | --- |
| Human FBPase 1 | P09467 | `1FTA` / **AMP** | 2.30 | A:15 | **PASS** |
| Bovine glutamate dehydrogenase | P00366 | `6DHQ` / **GTP** | 2.30 | A:13 | **PASS** |
| *E. coli* FBPase class 1 | P0A993 | `2Q8M` / **AMP** | 2.05 | A:17 | **PASS** |
| Rat mevalonate kinase | P17256 | `2R42` / **FPP** | 2.40 | A:16 | **PASS** |
| *P. furiosus* UMP kinase | Q8U122 | `2JI5` / **UTP** | 2.45 | A:21 | **PASS** |
| *E. coli* FBPase, second site | P0A993 | `2Q8M` / **G6P** | 2.05 | A:5 + B-2:5 | fail |
| Human FBPase, GGPP site | P09467 | `7CVH` / **GGPP** | 2.09 | A:9 + B:4 + C:4 + D:9 | fail |
| Human PRPS1 | P60891 | `2HCR` / **AMP** | 2.20 | A:7 + B:1 + B-3:3 | fail |
| Human malic enzyme 2 | P23368 | `1PJ3` / **fumarate** | 2.10 | A:6 + B:2 | fail |
| Human UGDH | O60701 | `3PTZ` / **UDP-xylose** | 2.50 | A:23 + B:1 | fail |
| Arabidopsis ATCase | P49077 | `6YPO` / **UMP** | 1.67 | A:15 + A-2:4 | fail |
| *E. coli* NagB | P0A759 | `1HOT` / **GlcNAc6P** | 2.40 | A:3 + A-3:8 | fail |
| Yeast chorismate mutase | P32178 | `5CSM` / **Trp** | 2.00 | A:11 + A-2:3 | fail |
| *E. coli* DAHP synthase | P00888 | `6AGM` / **Tyr** | 2.00 | A:11 + C-2:5 | fail |
| *N. meningitidis* DAHPS | Q9K169 | `4HSO` / **Tyr** | 2.10 | A:12 + B:4 | fail |
| *C. jejuni* ATP-PRT | Q5HSJ4 | `4YB5` / **His** | 2.24 | A:10 + E:6 | fail |
| Human NT5C2 | P49902 | `2XJD` / **ATP** | 2.00 | A:11 + A-2:3 | fail |
| Human PANK3 | Q9H999 | `2I7P` / **AcCoA** | 2.05 | A:11 + C:12 | fail |

A second batch of 13, drawn from the AlloBench / CASBench / UniProt harvest and chosen for small
size, was measured the same way. Results: **PASS** — yeast NAGK `3ZZH`/`ARG` (C:16), *T. maritima*
NAGK `2BTY`/`ARG` (A:15), yeast pyruvate kinase `1A3W`/`FBP` (A:17). **FAIL (ix)** — dCMP
deaminase `2HVW`/`DCP` (A:12 + A-2:4 + B:1), uracil PRTase `1VST`/`GTP` (spread over **three**
chains), *E. coli* UMP kinase `2V4Y`/`GTP` (A:8 + E:6 + F:2), prephenate dehydratase `2QMX`/`PHE`,
*Bs* LDH `1LDN`/`FBP`, citramalate synthase `3F6G`/`ILE`, tryptophan dioxygenase `2NW8`/`TRP`,
aspartokinase III `2J0X`/`LYS`, PGDH `1PSD`/`SER`. Three could not be measured
(`4MHD` has no SPM, `3UC5` no COA, `5L6S` no AMP in assembly 1).

**Across both batches: 32 physiological-effector holo entries measured, 23 fail clause (ix) —
72 %.** Of the 9 that pass, 6 then die for other reasons (§3.4), so **3 of 32 survive every
clause: 9 %.** That is not fixable by searching harder: feedback inhibition by a metabolite is,
in the MWC picture, overwhelmingly a *quaternary* phenomenon. §7 limitation 3 says clause (ix)
removes "a class"; the measured rate says it removes **most of the class the set is trying to
add**.

### 3.4 What happened to the nine that passed clause (ix)

Three are the admissible arms in §4 (`1FTA`/AMP → `fbpase`, `6DHQ`/GTP → `gdh`, `3BJF`/FBP →
`pkm2`). The other six died on a second check, and the reasons are worth recording because four
of them are traps a database row would not reveal:

- **Rat MVK / FPP — the FPP site *is* the ATP site.** `2R42` FPS lining = L53, N55, V56, S108,
  V133, S135, P139-S146, Y149, H197. `1KVK` ATP lining = K13, **L53, N55**, N104, E105,
  **S108, V133, S135, P139-S146**, A147, **Y149**, I196, **H197**, D204. 15 of 16 FPP labels
  are ATP contacts. Clause (vii) would delete almost the entire label set. **Not a distinct site.**
- **Pfu UMP kinase / UTP — the UTP site *is* the UMP substrate site.** `2JI5` UTP lining vs
  `2BMU` U5P lining share 19 of 21 residues (G43-45, A48, I52, D66, G69, I70, T73, G113-T120,
  V123). UTP is bound as a UMP analogue. **Not a distinct site.**
- ***E. coli* FBPase** dies three times over: `2GQ1` SO4[A346] sits in the AMP pocket
  (3.03 Å of GLU21) → clause (x); PROSITE PS00124 has **0 matches** on `2GQ1:A`, so the active
  site is underivable; and it shares PF00316/PF18913 with human FBPase, so only one could enter.
- **Yeast pyruvate kinase** `1A3W`/`FBP` passes cleanly (A:17) and lands on the same intra-chain
  pocket as PKM2 — a useful confirmation that the PK FBP site is intra-chain across the family —
  but it shares PF00224/PF02887 with `pkm2`, so **clause (xii) admits one, not both**. `pkm2`
  wins on a globally ligand-free apo and human relevance.
- ***T. maritima* N-acetylglutamate kinase** `2BTY`/`ARG` passes (ix) at A:15 and is a genuine
  arginine-feedback site — but `2BTY` is **2.75 Å** and is the **only** entry for Q9X2A4, so it
  **fails clause (xi)**.
- **Yeast N-acetylglutamate kinase** (Q01217, ARG5,6 AAK domain) is the closest new miss.
  `3ZZF:C` 2.20 Å → `3ZZH:C` 2.10 Å / `ARG`: (ix) **single-chain, 16 residues**; (iv) **100.0 %**;
  16/16 labels map; the ARG site (Y87, F91, K265, S285, M286, E337-M347) is **completely disjoint**
  from the NLG substrate site (G135-A250); and `active_site: {from_ligands: [NLG]}` is derivable
  because the apo keeps its substrate. It fails clause (iii)/(x) **by 0.18 Å**: the apo is a
  **mercury derivative** and HG[C1356] sits **4.32 Å** from LEU338. Chain A is worse (EDO 2.87 Å
  from GLU337). The only other Q01217 entries are 2.95 Å, 3.25 Å and 3.8 Å — all fail (xi). One
  better apo would make this admissible; none exists today.

**Small proteins (< 272 aa).** The frame surfaced 25 catalytic accessions under 272 residues.
Every one I carried to a measurement failed: yeast chorismate mutase (256 aa) and NagB (266 aa)
on (ix); procaspase-6 (293 aa, `4N7J`/`2GQ` = A:4 + B:5) on (ix); Pfu UMP kinase (225 aa) on
site identity; *E. coli* DHFR `3K74` because its "allosteric effector" is an **antibody**, not a
small molecule. **I found no new admissible target below 272 residues.** §7 limitation 2 stands
unchanged, and its cause is now measured rather than inferred: small catalytic domains are
overwhelmingly obligate oligomers, so they lose on (ix) before size is ever the question.

---

## 4. The candidates that reached a final verdict, with manifest-row fields

Five admissible (§4.1-4.3, 4.5, 4.6) and one instructive rejection (§4.4). The five admissible
are mutually Pfam-disjoint and disjoint from all 27 blocked families, so all five could be added
together.

| | target | effector | physiological? | verdict |
| --- | --- | --- | --- | --- |
| 4.1 | `pkm2` | FBP | **yes** | admissible |
| 4.2 | `fbpase` | AMP | **yes** | admissible |
| 4.3 | `gdh` | GTP | **yes** | admissible, one literature pass short (§7) |
| 4.4 | `pdhk2` | compound 8c | no | **rejected, clause (ii)** |
| 4.5 | `cblb` | Z3N | no | admissible, one stated assumption |
| 4.6 | `pfk_tbrucei` | CTCB-360 | no | admissible after one new motif |

### 4.1 `pkm2` — pyruvate kinase M2, activated by fructose-1,6-bisphosphate  ★ best new arm

| Field | Value |
| --- | --- |
| `protein` | Pyruvate kinase PKM, M2 isoform (P14618), *Homo sapiens* |
| `site` | FBP allosteric activator pocket, C domain |
| `pfam` | `[PF00224, PF02887]` |
| `apo` | `1ZJH:A`, 2.20 Å X-ray, **507 modelled residues, zero heteroatoms of any kind** |
| `holo` | `3BJF:A`, 2.03 Å X-ray, ligand **`FBP`** |
| `active_site` | `{from_motifs: [PK]}` — new motif, PROSITE **PS00110** `PYRUVATE_KINASE`, PA `[LIVAC]-x-[LIVM](2)-[SAPCV]-K-[LIV]-E-[NKRST]-x-[DEQHS]-[GSTA]-[LIVM]`, `/SITE=5,active_site`. Verified: **exactly 1 match** on `1ZJH:A` at auth 264-276 (`IKIISKIENHEGV`) and 1 on `3BJF:A` at 265-277 |
| measured | (ix) 18 lining residues, **all chain A**; (iv) **99.8 %** (506/507); (iii)/(x) **no apo component within 4.5 Å of any label**; (v) `1ZJH` assembly 1 is a tetramer (A, A-2, A-3, A-4), matching `3BJF`'s A-D |
| label set in apo numbering | LEU430, THR431, LYS432, SER433, GLY434, ARG435, SER436, TRP481, ARG488, GLY513, TRP514, ARG515, PRO516, GLY517, SER518, GLY519, PHE520, THR521 — **18/18 map**, none overlaps the motif source (264-276), so **all 18 scoreable** |
| `allosteric_evidence` | doi:**10.7554/eLife.45068**, Macpherson *et al.*, *eLife* 2019 (open access, full text read). Steady-state kinetics with the varied substrate named and the mode stated: "**FBP decreased the KMPEP to (0.23 ± 0.04) mM, compared to the absence of any added ligands (PKM2apo*) [KMPEP = (1.22 ± 0.02) mM]**" and "These results are consistent with previous reports … that FBP, Phe and Ser change the KMPEP but not the kcat and therefore **act as K-type modulators (Reinhart, 2004) of PKM2**." Table 3: kcat 349.3 ± 40.9 apo vs 356.7 ± 25.7 + FBP — catalysis unchanged, affinity 5-fold improved. The deposition paper for `3BJF` is doi:10.1038/nature06667 (Christofk *et al.*, *Nature* 2008), which calls FBP "the allosteric activator" but does not itself measure it |
| reviewer's caveat | `3BJF` models 518 residues to `1ZJH`'s 548-residue construct; the FBP pocket is ~35 Å from the catalytic Lys, so this is a long-range arm, which is a strength for the method and a weakness for a geometry-first baseline. `1ZJH` has no primary citation ("To be published") |

### 4.2 `fbpase` — human liver fructose-1,6-bisphosphatase, inhibited by AMP  ★ the gap-(a) filler

| Field | Value |
| --- | --- |
| `protein` | Fructose-1,6-bisphosphatase 1 (P09467), *Homo sapiens* |
| `site` | AMP allosteric site, N-terminal domain |
| `pfam` | `[PF00316, PF18913]` |
| `apo` | `7WVB:F`… **`7WVB:A`**, 2.09 Å X-ray, zero heteroatoms, "APO **R-state**" |
| `holo` | `1FTA:A`, 2.30 Å X-ray, ligand **`AMP`** (T-state) |
| `active_site` | `{from_motifs: [FBPASE]}` — new motif, PROSITE **PS00124**, PA `[AG]-[RK]-[LI]-x(1,2)-[LIV]-[FY]-E-x(2)-P-[LIVM]-[GSA]`, `/SITE=2,active_site`. Verified: **exactly 1 match** on `7WVB:A` at auth 274-286 (`GKLRLLYECNPMA`) and 1 on `1FTA:A` at 273-285 |
| measured | (ix) 15 lining residues, **all chain A**; (iv) **98.3 %**; (iii)/(x) **PASS, nothing within 4.5 Å** |
| label set in apo numbering | VAL18, GLY29, GLU30, LEU31, THR32, LYS113, TYR114, ARG141, VAL161, MET178 — **only 10 of 15 map**, because the AMP-binding loop (holo E20-G28) is **disordered in the R-state apo**. Disjoint from the motif source (274-286) → 10 scoreable |
| `allosteric_evidence` | doi:**10.1016/s0021-9258(18)47047-0**, Lu, Gidh-Jain, Hasemann, Pilkis, *J Biol Chem* 1994, "The allosteric site of human liver fructose-1,6-bisphosphatase. Analysis of six AMP site mutants based on the crystal structure." **This is a clean binding-null site-mutant test**, abstract retrieved from Europe PMC: "**Kinetic analyses revealed that all forms had similar turnover numbers, Km values for fructose 2,6-bisphosphate, and inhibition constants for fructose 2,6-bisphosphate.** … the apparent Ki values for the Arg140 → Ala and Ala24 → Phe mutants were 7- to 20-fold higher, respectively. … mutation of Thr31 to Ala increased the apparent Ki 120-fold. **AMP inhibition of the Tyr113 → Phe mutant was undetectable even at millimolar AMP concentrations.**" Ala24, Thr31, Tyr113, Arg140 are all in the measured label set; the enzyme stays catalytically intact. Kind 2 evidence, unambiguously |
| reviewer's caveat | Two, and both must be disclosed. (a) `7WVB` is the **R50A mutant** and has **no primary citation** ("To be published"); the alternative apo `5LDZ` maps 13/15 labels but has SO4 in the AMP pocket at 2.68 Å, so it fails clause (x). (b) The pair is an R→T **quaternary** transition, so the transplant-clash count will be high and clause (viii) state disclosure is doing real work. A reviewer will also note the AMP effect is cooperative (Hill n≈2), i.e. the classical mechanism is quaternary even though the *pocket* is single-chain |

### 4.3 `gdh` — bovine glutamate dehydrogenase, inhibited by GTP  ★ second gap-(a) filler

| Field | Value |
| --- | --- |
| `protein` | Glutamate dehydrogenase 1, mitochondrial (P00366), *Bos taurus* |
| `site` | GTP inhibitory site, antenna/pivot-helix region |
| `pfam` | `[PF00208, PF02812]` |
| `apo` | `7VDA:A`, **2.26 Å cryo-EM**, 496 modelled residues, zero heteroatoms |
| `holo` | `6DHQ:A`, 2.30 Å X-ray, ligand **`GTP`** (also GLU + NADPH at the active site) |
| `active_site` | `{from_motifs: [GLFV]}` — new motif, PROSITE **PS00074** `GLFV_DEHYDROGENASE`, PA `[LIV]-x(2)-G-G-[SAG]-K-x-[GV]-x(3)-[DNST]-[PL]`, `/SITE=6,active_site`. Verified: **exactly 1 match** on `7VDA:A` at auth 120-133 (`VPFGGAKAGVKINP`) and 1 on `6DHQ:A` at the same numbers |
| measured | (ix) 13 lining residues, **all chain A**, identical on all six protomers; (iv) **99.2 %**; (iii)/(x) **PASS, nothing within 4.5 Å**; **13/13 labels map** |
| label set in apo numbering | HIS209, GLY210, SER213, ARG217, LEU257, HIS258, ARG261, TYR262, ARG265, LYS289, GLU292, LYS446, HIS450 — disjoint from the motif source (120-133) → **13 scoreable** |
| `allosteric_evidence` | doi:**10.1006/jmbi.2001.4499**, Smith, Peterson, Bell, *J Mol Biol* 2001. Abstract (Europe PMC): "only animal GDH … exhibits a complex pattern of **allosteric inhibition** by a wide variety of small molecules. **The major allosteric inhibitors are GTP and NADH** and the two main allosteric activators are ADP and NAD(+). … **Kinetic analysis of a hyperinsulinism/hyperammonemia mutant strongly suggests that ATP can inhibit the reaction by binding to the GTP site.**" The HI/HH disease mutations *are* the binding-null control — they sit in this GTP site and abolish GTP inhibition while leaving catalysis intact |
| reviewer's caveat | (a) the apo is **cryo-EM** and the holo **X-ray**; the secondary set has no cross-method pair yet, and a reviewer will ask whether contact topology at 2.26 Å cryo-EM is comparable to 2.30 Å X-ray. (b) GDH is a homohexamer and the *allosteric mechanism* is quaternary even though the *pocket* is not — the same disclosure FBPase needs. (c) bovine, not human — the set gains a fifth organism |

### 4.4 `pdhk2` — **REJECTED on clause (ii)**, after passing every structural clause

Recorded in full because it is the most instructive rejection in the sweep: it is the only
candidate that cleared **(ix), (x), (iii), (iv), (xi), (v) and active-site derivability** and
then failed on mechanism.

Structural facts, all measured: apo `2BU8:A` 2.50 Å (ADP + Mg at the catalytic site, TF4 at the
*pyruvate/DCA* second site), holo `6LIL:A` 1.93 Å ligand `EGX`; (ix) 8 lining residues **all on
chain A**; (iv) **100.0 %** (343/343); (iii)/(x) **PASS** — TF4 never comes within 4.5 Å of a
label; `active_site: {from_ligands: [ADP, MG]}` derivable from `2BU8`. Author numbering differs
by **+8** between the two entries (`6LIL` S29 = `2BU8` S21), so a hand-typed label list would
have been silently wrong.

**Why it fails.** The pocket is not an allosteric site; it is the docking site of the enzyme's
own **physiological activator**, the inner lipoyl (L2) domain of dihydrolipoyl transacetylase.
Ligands there are *competitive with L2*, and the repo already rejected `usp7` for exactly this
("partner competition is not allostery").

- Green, Grigorian, Klyuyeva, Tuganova, Luo, Popov, *Biochemistry* 2007, doi:**10.1021/bi700650k**
  — abstract: "Finally, evidence that the blood glucose-lowering compound **AZD7545 disrupts the
  interactions between PDHK2 and L2** and thereby inhibits PDHK2 activity is presented."
- Kato, Li, Chuang, Chuang, *Structure* 2007;15:992-1004, doi:**10.1016/j.str.2007.07.001** —
  abstract, and this is the decisive sentence: "**Paradoxically, AZD7545 at saturating
  concentrations robustly increases scaffold-free PDK3 activity, similar to the inner lipoyl
  domain.**"

A compound that *activates* the scaffold-free kinase exactly as the physiological activator does
is an L2 mimetic at L2's own site. Neither deposition paper reports inhibition-mode kinetics:
Knoechel *et al.*, *Biochemistry* 2006, doi:**10.1021/bi051402s** only "**propose** that the
different inhibitor classes act by discrete mechanisms", and Kang *et al.*, *BBRC* 2020,
doi:**10.1016/j.bbrc.2020.04.102** is purely structural ("The co-crystal structure confirmed the
specific binding location of compound 8c and revealed the remote conformational change in the
ATP-binding pocket"). Note that `2BU2` contains ATP **and** TF1 simultaneously, so the ligand is
demonstrably not ATP-competitive — but the relevant orthosteric partner here is L2, not ATP, and
the ligand sits in L2's pocket.

**This is clause (ii) doing its job.** It is also the second time in this sweep that an
apparently clean structural pass concealed an orthosteric site — `legumain` was the first.

### 4.5 `cblb` — CBL-B E3 ubiquitin ligase (admissible, with one stated assumption)

| Field | Value |
| --- | --- |
| `protein` | E3 ubiquitin-protein ligase CBL-B (Q13191), *Homo sapiens* |
| `site` | TKBD-LHR interface pocket that traps Tyr363 |
| `pfam` | `[PF00097, PF02262, PF02761, PF02762]` |
| `apo` | `26LM:A`, 1.95 Å X-ray, 396 modelled residues, **zero heteroatoms** |
| `holo` | **`8QNH:A`, 2.00 Å X-ray, ligand `Z3N`** — chosen over `8QTG`/`WUQ` (1.42 Å) deliberately: `Z3N` is the **same chemical component** as `8GCY`, the structure in the paper that carries the mechanism, so evidence and coordinates describe one molecule |
| `active_site` | `{from_motifs: [ZF_RING]}` — PROSITE **PS00518** `ZF_RING_1`, PA `C-x-H-x-[LIVMFY]-C-x(2)-C-[LIVMYA]`. Verified: **exactly 1 match** on `26LM:A` at auth 388-397 (`CGHLMCTSCL`) and 1 on the holo. `{from_ligands: [ZN]}` — the rule the ledger recorded — **does not work**: `26LM` models no zinc |
| measured | (ix) **18 lining residues, all chain A**; (iv) **99.7 %**; (iii)/(x) **PASS, nothing within 4.5 Å**; **18/18 labels map** |
| label set in apo numbering | PRO71, ARG141, THR144, LYS145, LEU148, SER218, THR219, LEU222, TYR260, ALA262, PHE263, LEU264, THR265, GLU268, LEU287, **TYR363**, MET366, GLY367 — disjoint from the RING (388-397) → **18 scoreable** |
| `allosteric_evidence` | doi:**10.1038/s42003-023-05655-8**, Kimani *et al.*, *Commun Biol* 2023;6:1272 (open access, full text read). Mechanism: "The compound binding at the interface between the TKBD and LHR, as well as its specific interaction with the **Y363 in the flexible LHR, locks the protein in an inactive conformation that prevents phosphorylation of Y363**, which is crucial for Cbl-b activation." Abstract: "a small-molecule inhibitor that **locks the protein in an inactive conformation by acting as an intramolecular glue**." The orthosteric alternative is excluded by a binding-site control: "…revealing the compound's interaction with both the TKBD and LHR, **but not the RING domain**" and "…consistent with our biophysical studies, which showed that the compound binding does not involve the RING domain" — the RING being, in the same paper's words, "an E2 binding module". Clause (ii) kind 3 |
| corroboration | doi:**10.1021/acs.jmedchem.3c02083**, *J Med Chem* 2024 (the `8QTG`/`8QTJ` deposition paper): "inhibition of Cbl-b autoubiquitination, inhibition of ubiquitin transfer to ZAP70". Functional, but on its own it does not exclude an orthosteric mechanism — a strict scan of the sibling ACS Med Chem Lett paper found **neither "competitive" nor "allosteric" present in the text** |
| reviewer's caveat | **The assumption to write down.** For a RING E3, thioester transfer happens on the **E2**, not on CBL-B; CBL-B has no catalytic site of its own. Calling the RING zinc finger "the active site" is a curatorial judgement. It is defensible — the RING is where CBL-B's measured output (ubiquitin transfer to ZAP-70) is generated, and the inhibitor's mechanism is precisely to stop the RING presenting E2~Ub — but it sits close to §7 limitation 4's "non-catalytic targets are out of scope", and it must be declared, not slipped in. Secondary caveat: `26LM` has no primary citation ("To be published") |

### 4.6 `pfk_tbrucei` — *T. brucei* phosphofructokinase (conditional: one motif away)

| Field | Value |
| --- | --- |
| `protein` | ATP-dependent 6-phosphofructokinase (O15648), *Trypanosoma brucei* |
| `site` | ctcb360 allosteric pocket |
| `pfam` | `[PF00365]` |
| `apo` | `2HIG:A`, 2.40 Å X-ray, 440 modelled residues, only Na⁺ |
| `holo` | `6QU3:A`, 2.35 Å X-ray, ligand **`JJ5`** |
| `active_site` | **BLOCKED.** PROSITE **PS00433** `PHOSPHOFRUCTOKINASE` (`[RK]-x(4)-[GAS]-H-x-[QL]-[QR]-[GS]-[GF]-x(5)-[DE]-[RL]`) gives **0 matches** on both `2HIG:A` and `6QU3:A` — trypanosomatid PFK is too divergent. `2HIG` holds no cofactor, and the only ligand-bound *T. brucei* PFK entries are `3F5M` (ATP, **2.70 Å**) and `6SY7` (AMP, **2.75 Å**), both failing clause (xi). **A literature-cited catalytic motif must be written**, which ADR 0021 §4 (amended) explicitly permits |
| measured | (ix) 16 lining residues, **all chain A**, on all four protomers; (iv) **100.0 %** (428/428); (iii)/(x) **PASS — nearest apo component is Na at 16.05 Å**; (v) `2HIG` assembly 1 is a tetramer (A, A-2, B, B-2), matching `6QU3`'s A-D |
| label set in apo numbering | GLY197, GLY198, ASP199, GLN202, ARG203, PRO225, LYS226, THR227, ASP231, LEU232, ARG274, ASP275, ALA430, THR431, VAL433, ARG434 — **16/16 map** |
| `allosteric_evidence` | doi:**10.1038/s41467-021-21273-6**, McNae *et al.*, *Nat Commun* 2021;12:1052, PMC7887271 (open access, full text read). **Best-case bar — both substrates varied independently**: "**Enzyme kinetic studies confirmed that the CTCB compounds are not competitive against either ATP or F6P.**" With the estimator named: "The Michaelis–Menten plots (Supplementary Fig. 2 and Supplementary Table 1) show inhibitory behaviour for the compound CTCB-405 … **The reduction of Vmax for both substrates (F6P and ATP) indicates that the inhibitor is not competitive with either ATP or F6P.**" |
| reviewer's caveat | **Three, and the first is the one that will be raised.** (a) **The kinetics and the coordinates are different molecules.** The paper's data-availability statement maps CTCB-12 → `6QU5`, CTCB-360 → `6QU3`, CTCB-405 → `6QU4`; the kinetics above are on **CTCB-405 = `6QU4`**, described as "typical for the compound series". Switching the holo to `6QU4` to match does **not** work — `6QU4` is **2.75 Å and fails clause (xi)** (checked). So this arm either accepts congener kinetics, as `smyd3` already accepts fragment-grade potency, or it does not enter. (b) The arm needs a **new active-site motif with a primary-literature citation**, because PS00433 gives 0 matches — real work and a real reviewable decision. (c) `6QU3` carries a phosphoserine (`SEP`) as a modified residue; check it does not enter the node set unhandled. Constructs differ (507 vs 487 residues) though aligned identity is 100 % |

---

## 5. The two rejections worth writing down

A third near-miss — yeast N-acetylglutamate kinase, which fails clause (iii)/(x) by 0.18 Å on a
mercury atom — is recorded in §3.4.

### 5.1 `fpps` — the best clause (ii) evidence in the whole sweep, blocked by a crystallisation anion

Human farnesyl pyrophosphate synthase has the strongest **physiological**-effector evidence I
found anywhere, and it is blocked by an ion.

doi:**10.1038/ncomms14132**, Park, Zielinski, Magder, Tsantrizos, Berghuis, *Nat Commun* 2017;8:14132
(open access, full text read): "the product of FPPS, farnesyl pyrophosphate (FPP), can bind to
this pocket and **lock the enzyme in an inactive state**. The Kd for this binding is 5-6 μM,
within a catalytically relevant range. … **Kinetic analysis shows that the enzyme is inhibited
through FPP accumulation. Having a specific physiological effector, FPPS is a bona fide
allosteric enzyme.**" Results: "**Indeed, reaction progress kinetic analyses demonstrate product
inhibition by FPP**", by the "same excess" protocol; and "Intriguingly, the product is bound not
to the active site, but to the speculated allosteric pocket of the enzyme." ITC puts allosteric
Kd(FPP) = 5.3 ± 0.4 µM against active-site Kd 2.2 µM (DMAPP) / 2.1 µM (GPP).

Two honest limits on that evidence: the inhibition is **not classified against a named varied
substrate**, and there is **no allosteric-site mutant**; attribution to the pocket rests on the
structure plus an energetic argument. Separately, **the widely-cited Jahnke 2010 kinetics could
not be verified** — doi:10.1038/nchembio.421 is paywalled (Nature returns HTTP 303 to
`idp.nature.com`) and its abstract makes **no kinetic claim** at all, only "These new inhibitors
bind to a previously unknown allosteric site on FPPS". Do not cite non-competitive FPPS kinetics
to that paper without reading it. The `6N7Y` paper (doi:10.1021/acs.jmedchem.9b01104, ACS
returns 403) is structure/SAR only and establishes nothing functional.

**The structural block, measured.** `6N7Y`/`KFA` and `5JA0`/`FPP` are both **single-chain**
(12 and 20 lining residues) — (ix) passes. Clause (x) fails on every apo at ≤ 2.5 Å, because a
crystallisation anion occupies the pocket's diphosphate subsite: `4XQR` PO4[F401] 2.87 Å from
LYS57; `2F7M` PO4 2.63 Å; `4XQT` SO4[F404] **2.59 Å** from ASN59; `4XQS` SO4 2.95 Å. The
substrate-loaded entries are worse — `4KQU` IPE 2.75 Å from ARG60.

**The escape route, if the freeze is being reopened anyway.** Admit `4KQU:A` or `4NKE:A`
(Mg + IPP + bisphosphonate at the catalytic site) with `active_site: {from_ligands: [MG, IPE]}`.
IPP is a *substrate*, so the labels it touches (LYS57, ARG60) become active-site residues and
clause (vii) removes them **before** clause (iii) is applied — the same pattern `mkp5` and both
KRAS arms already record. The catalytic site itself is cleanly marked: `4XQT`'s three Mg ions sit
on D103/D107/Q171/D174/K200 and Q240/D243/D247/D261, the two DDXXD motifs. I did not mark this
admissible because it means calling a bisphosphonate-loaded enzyme "apo", and that is a
freeze-level decision, not a measurement. **Note the ledger's recorded `lig:PO4` rule for this
row is wrong**: the phosphate is in the *allosteric* pocket, not the active site (measured).

### 5.2 `p300` — rejected twice over; its own authors call the series artifactual

I first rejected this on clause (x): every CoA-bearing apo has a cryoprotectant in the
CPI-090 pocket (`4PZR` DMS 2.86 Å, PEG 3.13 Å; `4PZS` DMS 2.81 Å; `5LKZ` GOL **2.53 Å**), and
the one apo that clears the pocket, `6V90`, holds no CoA so `{from_ligands: [COA]}` is
underivable. That rejection now stands on a much stronger ground.

doi:**10.1063/1.5119336**, Gardberg *et al.*, *Struct Dyn* 2019;6:054702 (open access, full text
read) — the paper that deposited `6PF1` and `6PGU` — **fails its own non-competitive test and
then withdraws the series**:

- "On further examination, **neither the 10× AcCoA nor the 30× histone peptide met the IC50
  shift threshold necessary to be considered truly competitive.**" and "In both situations,
  CPI-076 and CPI-090 are **AcCoA- and peptide-modulating compounds but not wholly competitive
  compounds**" — i.e. modulated by *both* substrates, the opposite of clean non-competitive
  behaviour.
- Abstract: "**the full-length enzymatic assay demonstrated that this allosteric HAT inhibitor
  series was artifactual, inhibiting only the HAT domain of p300 with no effect on the
  full-length enzyme.**" Conclusions: "**CPI-090 does not inhibit the FL enzyme in our
  experiments**"; "The related compound CPI-076 had no measurable FL activity."

**Drop this pair.** The site has no demonstrated function in the intact enzyme, which is a
harder failure than the apo-occupant problem that first caught it.

## 6. Verdict on the supply claim

**§7 limitation 1 is right that supply binds, and wrong about which clause does the binding.**

### 6.1 What each clause costs, measured

| Clause | Denominator | Killed | Rate |
| --- | --- | ---: | ---: |
| **(xii)** within-set redundancy | 24 pending candidates | 11 | **46 %** |
| **(xii)** | 380 accessions from an unrestricted RCSB frame | 47 | **12 %** |
| **(xii)** | 865 accessions from the merged 6-route harvest | 119 | **14 %** |
| **(ix)** single-chain lining | 12 pending candidates with a real holo | 5 | **42 %** |
| **(ix)** | **32 physiological-effector holo entries** | **23** | **72 %** |
| **(ix)** | all 44 holo entries measured this session | 28 | 64 % |
| **(x)/(iii)** apo occupant | 10 candidates that survived (ix) | 4 | 40 % |
| **(ii)** functional evidence | 7 candidates that survived every structural clause | **2** | **29 %** |
| site not topographically distinct | 9 (ix)-survivors | 2 | 22 % |
| active site underivable | 8 candidates past (ix)+(x) | 1 hard, 1 soft | 13-25 % |
| **(xi)** resolution | 13 pending holo entries | **0** | 0 % |
| **(xi)** | new physiological candidates | 1 (`2BTY`, 2.75 Å) | — |
| **(iv)** identity | 14 pairs measured | **0** (range 98.1-100 %) | 0 % |

Read down that column and the story is unambiguous.

- **Clause (xii) is not the binding constraint.** It costs 12-14 % on both independent frames —
  380 accessions from RCSB full text, 865 from the six-route harvest. It looks lethal on the
  pending list (46 %) only because that list is ten protein kinases deep, and the set already
  spent its two kinase families on `chk1` and ABL1. The fix is not to relax (xii); it is to stop
  proposing kinases. Note also that (xii) is what forces the choice between human and *E. coli*
  FBPase, and between PKM2 and yeast PK — in both cases the *better* member was still available,
  so the clause cost nothing real.
- **Clause (ix) is the binding constraint, and it is worse than §7 says.** The README reports
  11 of 97 rejected on (ix) and calls it "the largest single cause of rejection after an
  underivable active site". Measured prospectively on candidates chosen *for* the gap the set
  admits to having, the rate is **72 %**, and the end-to-end survival is **3 of 32 = 9 %**.
  The clause and the gap are the same fact: the class §5.2 says is missing — metabolite
  feedback, cooperativity — is precisely the class that is quaternary and therefore
  inadmissible. **You cannot fill gap (a) at scale without amending clause (ix) or ADR 0010's
  one-chain node set.** Three arms squeezed through; that is what a 9 % yield looks like.
- **Clause (ii) is the second most expensive, and it is expensive at the *end*.** It killed 2 of
  the 7 candidates that had already survived every structural clause — `pdhk2` (an L2-mimetic at
  the physiological activator's own site) and `p300` (a series its authors withdrew as
  artifactual on the full-length enzyme). Both look perfect until someone reads the paper. That
  is the cost §3 of the secondary README predicts — "the expensive part of building a set like
  this, and no choice of frame avoids it" — and it is confirmed at 29 %.
- **Clauses (xi) and (iv) cost essentially nothing** and should be dropped from the story about
  why N is small. Across 14 measured pairs identity ran 98.1-100 %; resolution killed one
  candidate in the entire sweep.
- **A fifth cost the ledger does not have a category for**: the effector turning out not to
  occupy a topographically distinct site. Rat MVK (FPP in the ATP site, 15 of 16 labels shared),
  Pfu UMP kinase (UTP in the UMP site, 19 of 21 shared) and legumain (nitrile warhead on the
  H148/C189 catalytic dyad). Three candidates, none detectable from a database row — all three
  are annotated as allosteric somewhere. **This is a clause the ledger should record explicitly.**

### 6.2 How many additional admissible targets exist

| | count | targets |
| --- | ---: | --- |
| Admissible now, no new decision | **3** | `pkm2`, `fbpase`, `gdh` |
| Admissible with one stated assumption | **1** | `cblb` (RING zinc finger = active site) |
| Admissible after writing one literature-cited motif | **1** | `pfk_tbrucei` |
| **Total reachable extension** | **5** | |
| Behind one freeze-level decision each | 2 | `fpps` (declare IPP part of the active site), `nagk_yeast` (accept Hg at 4.32 Å, or find a better apo) |
| Resulting set size | **9 → 14**, or 16 with both decisions | |
| Design target | **28** | |

**The design target is not reachable from this frame.** Two independent, exhaustive frames —
1061 RCSB full-text entries over 12 phrases, and a 1049-accession merge of AlloBench, CASBench,
GtoPdb, AHoJ-DB, UniProt activity-regulation text and the local prior-art clone — produced 5
further admissible targets between them. That is the supply.

**What the extension buys.** Three of the five (`pkm2`/FBP, `fbpase`/AMP, `gdh`/GTP) carry
**physiological effectors**. That closes the gap §5.2 names — "the one candidate with a
physiological effector, AMP on glycogen phosphorylase, was rejected by clause (ix)" — three
times over, and `fbpase`/AMP is the *same chemistry* as the glycogen-phosphorylase arm that was
lost. It also adds two organisms and a cryo-EM input.

**What it does not buy.** **No new admissible target is below 272 residues.** Every small
candidate that reached a measurement failed: yeast chorismate mutase (256 aa) and NagB (266 aa)
on (ix); dCMP deaminase (150 aa), uracil PRTase (216 aa), *E. coli* UMP kinase (241 aa) and
prephenate dehydratase (280 aa) on (ix); procaspase-6 (293 aa) on (ix); Pfu UMP kinase (225 aa)
on site identity; *T. maritima* NAGK (282 aa) on (xi); *E. coli* DHFR (159 aa) because its
"allosteric effector" is an **antibody**, not a small molecule. The cause is now measured rather
than inferred: **small catalytic domains are overwhelmingly obligate oligomers, so they lose on
clause (ix) before size is ever the question.** §7 limitation 2 should stand, with this as its
mechanism.

### 6.3 What a re-freeze would cost

Adding 5 arms takes N from 9 to 14 and re-runs the seeded size-stratified split, so **every
existing tier assignment changes**. Under the README's own reasoning that is a re-freeze, not a
repair — the same argument §7 limitation 10 used to decline reopening `usp7`. The pay-off is
real: `generalisation` would go from 5 to ~7-8, moving the minimum attainable one-sided p from
2⁻⁵ = 0.031 to 2⁻⁷ = 0.0078 or 2⁻⁸ = 0.0039. At N = 5 one failure leaves p = 0.19 and the tier
is dead; at N = 8 one failure leaves p = 0.035 and it still rejects. That is the difference
between a hypothesis test with no margin and one with a little.

It would also fix the §6 complaint that `development` spans only two biological classes: `pkm2`,
`fbpase` and `gdh` are three new classes (glycolytic kinase, gluconeogenic phosphatase, amino-acid
dehydrogenase), and the seeded split would distribute them without anyone choosing.

## 7. What I could not check, and why

- **Clause (ii) is established at the required bar for 4 of the 5 admissible targets.**
  `fbpase` (site mutants: Ki 7-120-fold up, Y113F undetectable, kcat and K_M unchanged),
  `pkm2` (K-type on K_M^PEP, kcat unchanged), `pfk_tbrucei` (V_max reduced with both ATP and F6P
  varied independently) and `cblb` (conformational lock, RING/E2 site excluded biophysically).
  **`gdh` is the exception**: I have the *J Mol Biol* 2001 abstract calling GTP a major allosteric
  inhibitor and reporting HI/HH mutant kinetics, but **I did not read the full text** and do not
  have a verbatim sentence naming the varied substrate or the inhibition mode. Treat `gdh` as
  needing one more literature pass before admission.
- **The `pfk_tbrucei` kinetics are on a congener.** CTCB-405 (`6QU4`) was the molecule assayed;
  `6QU3` holds CTCB-360. `6QU4` is 2.75 Å and fails clause (xi), so the mismatch cannot be
  repaired by swapping the holo. Whether "typical for the compound series" is good enough is a
  curatorial call, not a measurement.
- **Jahnke 2010 (doi:10.1038/nchembio.421) could not be read** — Nature returns HTTP 303 to
  `idp.nature.com`; the Novartis OAK archive (`oak.novartis.com/2500/`) is discontinued. Its
  abstract makes **no kinetic claim**. Any statement that the FPPS allosteric inhibitors are
  non-competitive **must not** be cited to that paper without someone reading it. Likewise
  `pubs.acs.org/doi/10.1021/bi051402s` returned **HTTP 403**, and
  doi:10.1021/acs.jmedchem.9b01104 (the `6N7Y` paper) was abstract-only.
- **Europe PMC `fullTextXML` returned HTTP 404** for PMC10726479, PMC2136408, PMC2871385,
  PMC2414299, PMC4703025 and PMC3894725 (Chaneton 2012); NCBI efetch returned "The publisher of
  this article does not allow downloading of the full text" for five of those. Several
  secondary corroborations for `pkm2` are therefore abstract-level.
- **Transplant clash fractions, prevalence, nearest-label distance and the seeded tier
  assignment are not computed** for any new candidate. Those come from `allo.benchmark.derive`,
  which needs a manifest edit, and I was read-only. For `fbpase` in particular the R→T
  transition means the clash count could be extreme; that is **unknown** until derived.
- **The `fbpase` label-mapping loss (10 of 15) is measured but not priced.** Five labels are
  unmodelled in the apo because the AMP loop is disordered in the R state. Whether a 10-label arm
  is worth having is a judgement `docs/benchmark/evaluation/README.md` has to make. Same question, harder,
  for a hypothetical 8-label arm.
- **Three of the admissible arms rest on an apo with no primary citation** — `7WVB` (fbpase,
  and it is the **R50A mutant**), `26LM` (cblb) and `1ZJH` (pkm2), all "To be published". I
  cannot check construct provenance, expression tags, or whether the coordinates were reviewed.
  The cathepsin-K failure recorded in §7 limitation 2 — a pocket partly built from an N-terminal
  expression tag — is exactly the trap an uncited deposition hides.
- **`7VDA` (the `gdh` apo) was deposited in a methods paper about a hydrophobin cryo-EM support
  film**, not a GDH paper. Whether that is a suitable benchmark input is a judgement I did not
  make. It would also be the set's **first cross-method pair** (cryo-EM apo, X-ray holo), and
  whether 4.5 Å contact topology is comparable across methods is **unknown**.
- **I did not verify that `3BJF` is wild-type PKM2**, only that it aligns to `1ZJH` at 99.8 %
  over 507 aligned pairs. One residue differs; which one is **unknown**.
- **Clause (ix) was measured on assembly 1 only.** Entries with several deposited assemblies
  could give a different answer; assembly 1 was taken as the biological assembly throughout,
  matching what `tests/test_secondary.py` does.
- **Three candidate measurements could not be completed**: `4MHD` (SpeG) contains no `SPM`,
  `3UC5` (PPAT) no `COA` and `5L6S` (ADP-glucose pyrophosphorylase) no `AMP` in assembly 1 — the
  effector CCDs the harvest sources record are not in the deposited assembly. Marked
  **needs-measurement**, not passed and not failed.
- **The 313 alive accessions from the RCSB frame and the 78 curated harvest rows were triaged,
  not screened.** I carried ~55 to a geometric measurement. The rest are **unscreened**, so the
  admissible count of 5 is a **floor, not a total** — the same caveat §7 limitation 2 puts on its
  own count of 11. That said, the two frames overlap heavily on their best candidates (FBPase,
  GDH, PK, NagB, chorismate mutase, DAHPS, ATP-PRT, UMP kinase all appear in both), which is
  weak evidence that the pool is close to exhausted rather than merely under-sampled.
- **23 rows in the harvest are non-catalytic** (ATCase regulatory chain, CRP/TetR/FadR
  transcription factors, AMPK-γ, PKA RIα, GroEL, BiP, P2X3). They have published allosteric sites
  and good holo structures, but no active site, so "distal from the active site" has no referent.
  Per §7 limitation 4 they cannot enter. I did not screen them.
- **The database-derived candidate lists were never used as evidence.** AlloBench rows,
  `allo_tableS2.csv` rows and CASBench names were used only as names to go and measure. Their
  published site-residue lists were **not** checked against structure, and nothing above depends
  on them being right.
- **CASBench's bulk data is 1.9 GB of coordinate archives** at `biokinet.belozersky.msu.ru`
  with no metadata table; not downloaded, out of scope. UniProt accession `L8A208` and PDB entry
  `3MW9` could not be resolved (deleted/obsoleted); 1 of 430 and 1 of 108 respectively.
