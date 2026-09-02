# Extension sweep — what is reachable on 2026-09-02, and how far the benchmark can go

**Status: a screening record and a reachability audit. It changes no freeze.** The secondary
benchmark is still the nine targets frozen on 2026-08-24. Nothing here is in `manifest.yaml`
or `frozen.json`.

**Read `../secondary/README.md` §3 and §7 first.** This document contradicts one of its
conclusions on evidence, and confirms another.

Data behind every number: [`data/database-reachability.json`](data/database-reachability.json)
and [`data/extension-candidates-2026-09.json`](data/extension-candidates-2026-09.json).

**This file names no allosteric-site residue.** Clause (ix) is reported as a chain count and a
list of chain IDs, never as residue identities. That is deliberate: `selection.json` and
`secondary/evidence/extension-candidates.md` are both in `tests/test_no_leakage.py`'s
`PROTECTED_PATHS` because they name real label residues, and at the time of writing
`docs/benchmark/review/` was **not** protected. Keeping residue identities out of this
directory was cheaper than adding a seventh guarded route.

> **Resolved 2026-09-02, later the same day.** The tree **is** protected now. ADR 0034 adds
> `docs/benchmark/review/` to `PROTECTED_PATHS` and exempts its own tools by a **rule** rather
> than by a name list: a file is a review tool when it is tracked inside the tree **and**
> imports nothing from `allo`. The leakage suite passes with the tree protected. Redaction is
> kept anyway, as defence in depth.


---

## Headline

1. **ASD is reachable, and it was reachable on 2026-08-24 too.** All twelve release archives
   downloaded with plain `curl`, no login, no browser. The 2026-08-24 conclusion — "A script
   cannot fetch ASD today. A human must first capture that URL from a rendered page"
   (`../secondary/evidence/databases.md` §1) — is **falsified**. The blocker was never the
   server. The file table is a literal JavaScript array in
   `/ASD/module/download/js/download.js`, and the URL prefix is one variable in
   `/ASD/js/util/localcomponent.js`. The 2026-08-24 sweep enumerated `<a href>` elements on the
   rendered page, which is exactly the one place the list is not.
2. **The TLS failure is real and unchanged.** The `*.shsmu.edu.cn` certificate expired
   2025-12-28 and has not been renewed. Everything on that host is plain HTTP only. That was
   right on 2026-08-24 and is right today.
3. **35 extension candidates survive every structural clause this sweep can measure**, from a
   frame of 3147 ASD site records. 13 carry a **physiological** effector. **4 are under 272
   residues**, including one at **158**. Both are gaps `../secondary/README.md` §5.2 and §7.2
   record as unfilled, and §7.2 states flatly that "No new admissible target is below 272
   residues."
4. **None of the 35 has clause (ii).** Not one paper has been read. The 2026-08-24 sweep
   measured clause (ii) killing 29 % of candidates that had already passed every structural
   clause. That bill has not been paid here and it is the whole remaining cost.

   **Partly paid on 2026-09-02** by [`14-clause-ii-literature-pass.md`](14-clause-ii-literature-pass.md),
   which read papers for the 34 survivors of §4. **13 PASS, 5 FAIL, 16 UNREAD.** The measured
   kill rate among the 21 rows that could be decided is **24 %**, close to the 29 % this sweep
   predicted. Two things follow, and neither is "the extension is ready":
   - **The sixteen UNREAD rows are undecided, not passing.** No PASS was issued from an
     abstract. Publisher paywalls returned 403 in every case at JBC, PNAS, Nature, Nature
     Chemical Biology, *Biochemistry*, *J. Med. Chem.* and nine more, so the UNREAD count is a
     retrieval limit and not a judgement. **The honest count of clause-(ii)-clean leads is 13,
     not 34.**
   - **A clause (ii) pass is not an admission.** Seven of the thirteen carry a separate
     structural problem the UniProt-level screening could not see. **Six carry no known
     structural blocker: `hisG`, `UBE2I`, `PDC1`, `LGMN`, `proRS`, `fbpC`**, and every one of
     those still has unmeasured clauses.
   - **The best single lead is `hisG`**, *M. tuberculosis* ATP phosphoribosyltransferase under
     L-histidine feedback: a metabolite effector, a new organism, 284 residues, and inhibition
     kinetics measured three ways in an open-access primary paper — which is **not** the paper
     ASD cites.
   - **Thirteen defects were found in the curation references, and one correction to §4.2's own
     table.** No curation DOI pointed at the wrong protein; the defects are of four other kinds.
     The `FBP1` DOI is corrected to `10.1021/bi400532n`.
5. **Clause (ix) is still the binding structural constraint, but it is cheaper to dodge than
   the 72 % figure suggests** — because ASD's site-residue field is chain-annotated, so a
   multi-chain site can be rejected before anything is downloaded. 487 of 3147 records were
   killed that way for free, and of the 65 that were then measured on the biological assembly,
   19 failed (29 %).

---

## 1. Reachability, 2026-09-02

Method: `curl` 8.x against the macOS system trust store, `-L`, 45 s timeout, browser user
agent. A TLS failure was retried with `-k`, so a dead certificate is separated from a dead
host. 40 probes, each carrying its own UTC timestamp in the JSON.

### 1.1 What changed since 2026-08-24

| Source | 2026-08-24 | 2026-09-02 | What moved |
| --- | --- | --- | --- |
| **ASD bulk data** | "no data file on the download page"; release filename known only out of band | **All 12 archives downloaded, 143.7 MB** | Nothing on the server. The 2026-08-24 method looked at rendered `href`s; the list is in `download.js` |
| **ASBench bulk data** | registration wall, "formats behind the form were never seen" | **`Core_Set.tar.gz`, `Core_Diversity_Set.tar.gz` and the statistics `.xls` all return HTTP 200** at `/asbench/datasource/file/`, by the same `download.js` route | Same. Not downloaded — the licence forbids redistribution and the set is holo-only |
| **BioLiP2** | 403 to direct fetch, needed a proxy | **200 direct** | The block is gone |
| **PDBj** | "probe returned 404, not verified" | **200, 6.1 MB of JSON** | Wrong endpoint on 2026-08-24. `/rest/newweb/search/` 404s; `/rest/newweb/search/pdb?query=…` works |
| **Binding MOAD** | 403 | **200 — and it is NOT Binding MOAD** | `bindingmoad.org` now serves "BioStruct Explorer", a commercial site whose inline `window.__ENV__` names `https://api.lyprobio.com` and a live API key. The domain was repurposed. **A 200 on this host must not be read as "Binding MOAD is back."** |
| **CryptoSite, PocketMiner** | "not fetched this session" | **Both 200** | Now checked. PocketMiner's licence is still unchecked |
| **sc-PDB** | not probed | **Timed out twice, no HTTP status** | Recorded as UNREACHABLE-TIMEOUT, not "dead" |
| **ASD apo/holo module** | claimed by v3.0, not found in the 2023 navigation | **Still not found.** The path exists — `localcomponent.js:92` defines `apo_holo_pse_gz_path` — but the directory 404s and no per-file naming convention was recovered | Unchanged: **UNVERIFIED** |
| GtoPdb, AHoJ-DB, AlloBench, CASBench, RCSB, UniProt, InterPro | reachable | reachable, same versions | GtoPdb v2026.2 (2026-06-15), AHoJ-DB v2c (2025-04-03, 515,463 entries), AlloBench 2257 rows — all unchanged |

### 1.2 New to this sweep

**LIGYSIS** (`compbio.dundee.ac.uk/ligysis`) serves and is not in the 2026-08-24 survey. Its
record is a ligand-binding site defined over superposed structures of a UniProt segment: no
allostery label, no apo/holo pair record. **LIGYSIS-bench 404s** at `bartongroup/LIGYSIS-bench`;
the organisation listing was retrieved and holds no repository of that name.

**ProteinLens** (`proteinlens.io`) serves. It is an analysis server, not a database — it computes
bond-to-bond propensity on a structure you supply. Nothing to enumerate.

**PASSer** (`passer.smu.edu`) serves. It is a **predictor trained on ASD/ASBench**. Using its
output as ground truth would be circular and would breach ADR 0017.

### 1.3 The ASD retrieval recipe, so nobody has to rediscover it

```
1. GET http://mdl.shsmu.edu.cn/ASD/module/download/js/download.js
   -> `dataRecord2023`, a literal array of 12 {fileName, fileDescrip, fileType,
      versionNum, dateCreate} objects. Release 5.1, newest file dated 2023-09-20.
2. GET http://mdl.shsmu.edu.cn/ASD/js/util/localcomponent.js
   -> asd2015_static_file_root = "https://mdl.shsmu.edu.cn/ASD2023Common/static_file/"
      (line 32; use the http:// form, the certificate is expired)
3. Each file is at <root>archive_2023/<fileName>.
```

`ASD_Release_202306_XF.tar.gz` (11.8 MB, 2419 XML entry files) is the one to take. The
tab-delimited `AS` file leaves **1620 of 3102** site-residue fields blank, exactly as
`../secondary/evidence/databases.md` §3.1 records; the XML does not.

**Licence, and it is now quoted rather than absent.** `../secondary/evidence/databases.md` says
ASD states no licence. It does, in `download.js`, verbatim:

> ASD contains data for research use only. Users will not be allowed to distribute the data to
> a third party.

That is the same clause the survey used to disqualify ASBench. It does **not** stop ASD being a
recall device — a candidate name is not the data — but **no verbatim ASD file may be committed
or redistributed**. The archives are under `data/external/asd/`, which `.gitignore` already
excludes. `../secondary/evidence/databases.md` §2 and §3.1 should be corrected on this row.

### 1.4 What an ASD record still does not certify

Nothing in §1 changes `../secondary/README.md` §3 or ADR 0021 Decision 2. Reachability was
never the argument. ASD's evidence bar sits on the **protein**, its 2023 release mixes 3102
curated sites with 66,589 machine-predicted ones, and its extraction radius is 6 Å against our
4.5 Å. The frame stays RCSB. What ASD adds is **recall**, and this sweep measures how much.

---

## 2. What ASD adds as a recall device

Parsed from `ASD_Release_202306_XF` and `ASD_Release_202309_AS`:

| | count |
| --- | ---: |
| XML entry files | 2419 |
| allosteric-site records | 3147 |
| distinct UniProt accessions | 700 |
| distinct holo PDB entries | 2968 |
| records with an effector component ID | 3135 |
| records with site residues recorded | 2525 |
| records with a PubMed reference | 2532 |
| **single-chain lining, as ASD records it** | **2040** |
| multi-chain lining, as ASD records it | 487 |
| records whose entry also lists a ligand-free PDB entry | 2990 (95 %) |
| …and that entry is ≤ 2.5 Å | 2868 (91 %) |

**ASD publishes no apo/holo pair record** — the v3.0 module is still unverified — but it does
publish, per entry, a `PDB_List` with `Has_Ligand` and `Resolution` per structure. That makes an
apo candidate derivable for 95 % of site records without leaving the file. This is the field
`AlloBench` does not have and `CASBench` does not label.

**The chain-annotated residue field is the useful part.** ASD writes site residues as
`Chain A:…; Chain B:…`. That is a free clause (ix) prescreen: a record already split across two
chains cannot pass, and 487 were killed for zero downloads. It is **necessary, not sufficient** —
ASD measures on the deposited entry, so a single-chain ASD record can still be an interface site
once the biological assembly is built. That is the exact trap `../secondary/README.md` §7.3
records for glycogen phosphorylase, so every survivor below was re-measured on `assembly1`.

---

## 3. The funnel

3147 site records in, 68 screened to a deciding clause, 35 survivors.

| Deciding clause (first to fire) | Killed |
| --- | ---: |
| no catalytic mechanism recorded (`../secondary/README.md` §7.4) | 669 |
| no site residues recorded | 620 |
| **(ix) multi-chain lining, from ASD's own chain annotation** | **487** |
| **(xii) blocked Pfam family** | **377** |
| (xi) holo resolution > 2.5 Å | 148 |
| effector is an ion, a cryoprotectant, or absent | 145 |
| ASD's own `Site_Overlap = Yes` | 121 |
| effector is not a small molecule | 71 |
| no Pfam annotation | 52 |
| no literature reference | 47 |
| no resolution | 6 |
| **alive** | **404** |

404 alive collapse to 111 distinct UniProt accessions, then to 68 after within-set Pfam
disjointness (clause (xii) applied to the *new* set as well as against the 27 blocked
families, which were read from the two manifests rather than recalled). Those 68 were measured.

| After measurement | Count |
| --- | ---: |
| **A — every measurable clause passes, apo carries nothing but water** | **9** |
| **B — passes, one measurement outstanding** (apo occupant, or (ix) on one effector copy only) | **25** |
| **survivors (A + B)** | **34** ¹ |
| C — dead on clause (ix), measured on `assembly1` | 19 |
| C — no ASD-listed ligand-free entry ≤ 2.5 Å | 7 |
| C — dead on clause (iv), apo UniProt differs | 4 |
| C — ASD curation defect | 1 |
| D — assembly or effector could not be retrieved | 3 |

¹ 35 before the ASD curation defect in §5 was removed.

**Clause (ix), measured properly.** Of the 65 holo entries whose `assembly1` was retrieved,
**19 failed (29 %)**. Compare the 2026-08-24 figure of **72 %** on 32 physiological-effector
entries. The two are not in conflict: this sweep spent ASD's chain annotation first and only
downloaded assemblies for records ASD already called single-chain. **The clause is as
expensive as `../secondary/README.md` §7.1 says; the search is much cheaper.** That is the
practical correction.

**Clause (xii) cost 377 records, and it is still not the binding constraint.** Every one of
those 377 is a duplicate of a family already spoken for. The 68 that were measured span **61
Pfam families**, none of them blocked and none shared.

---

## 4. The survivors

Tier **A** — every structural clause this sweep can measure passes and the apo carries no
non-cryoprotectant component. Tier **B** — the same, except one measurement is outstanding:
either the apo carries a component that must be measured against the site (usually the enzyme's
own cofactor at the **active** site, which the repo's site-apo clause (iii) permits), or clause
(ix) passes on some effector copies in the assembly and not all.

"Flags" counts entries in `curation_flags` in the JSON — engineered mutants, covalent
modulators, glycans, nucleic acid in the assembly. **Read them before quoting a row.**

| T | Target | UniProt | aa | Apo | Holo / effector | Phys | Pfam | Organism | Apo occupant | Flags |
| :-: | --- | --- | ---: | --- | --- | :-: | --- | --- | --- | --- |
| A | NT5C2 | `P49902` | 561 | `5L50` 1.64 | `2JC9`/`ADN` 1.50 | Y | PF05761 | Homo sapiens | - |  |
| A | UBE2I | `P63279` | 158 | `5F6E` 1.12 | `5F6Y`/`5VM` 1.14 |  | PF00179 | Homo sapiens | - | 1 |
| A | birA | `P06709` | 321 | `1BIA` 2.30 | `4WF2`/`BTX` 2.31 |  | PF02237, PF03099, PF08279 | Escherichia coli | - | 1 |
| A | fbpC | `P9WQN9` | 340 | `4MQM` 1.35 | `5KWI`/`6Y1` 1.30 |  | PF00756 | Mycobacterium tuberculosis | - | 1 |
| A | LGMN | `Q99538` | 433 | `4N6O` 1.80 | `5LU8`/`5KN` 1.95 |  | PF01650 | Homo sapiens | - | 2 |
| A | lacS | `P22498` | 489 | `4EAM` 1.70 | `5IXE`/`14O` 1.75 |  | PF00232 | Saccharolobus solfataricus | - | 1 |
| A | proRS | `Q8I5R7` | 746 | `4NCX` 1.85 | `4WI1`/`3O6` 1.65 |  | PF03129, PF09180, PF00587, PF04073 | Plasmodium falciparum | - |  |
| A | GAA | `P10253` | 952 | `5NN3` 1.90 | `5NN4`/`SC2` 1.83 |  | PF13802, PF01055, PF00088 | Homo sapiens | - | 1 |
| A | USP7 | `Q93009` | 1102 | `4YSI` 1.02 | `5N9T`/`8QQ` 1.73 |  | PF00917, PF00443, PF12436 | Homo sapiens | - |  |
| B | pyrH | `P56106` | 240 | `4A7X` 2.49 | `4A7W`/`GTP` 1.80 | Y | PF00696 | Helicobacter pylori | UDP |  |
| B | hisG | `P9WMN1` | 284 | `5U99` 2.40 | `1NH8`/`HIS` 1.80 | Y | PF01634, PF08029 | Mycobacterium tuberculosis | ATP, MG |  |
| B | LDHA | `P13491` | 332 | `5KKC` 1.86 | `5NQQ`/`OAA` 1.87 | Y | PF02866, PF00056 | Oryctolagus cuniculus | 6V0 |  |
| B | AMD1 | `P17707` | 334 | `3EP3` 1.84 | `1MSV`/`PUT` 1.75 | Y | PF01536 | Homo sapiens | PYR | 1 |
| B | FBP1 | `P00636` | 338 | `1NUY` 1.30 | `2F3D`/`AMP` 1.83 | Y | PF00316 | Sus scrofa | F6P, MG |  |
| B | FDPS | `P14324` | 419 | `4NUA` 1.43 | `5JA0`/`FPP` 1.90 | Y | PF00348 | Homo sapiens | MG, RIS |  |
| B | PDE10A | `Q9Y233` | 1055 | `2OUS` 1.45 | `2ZMF`/`CMP` 2.10 | Y | PF01590, PF00233 | Homo sapiens | MG |  |
| B | kgd | `A0R2B1` | 1227 | `6R29` 1.67 | `2XTA`/`ACO` 2.20 | Y | PF00198, PF00676, PF02779 | Mycobacterium smegmatis | MG, QSP |  |
| B | murI | `Q9ZLT0` | 255 | `2JFY` 1.90 | `2JFZ`/`003` 1.86 |  | PF01177 | Helicobacter pylori | DGL |  |
| B | CTSK | `P43235` | 329 | `5TDI` 1.40 | `5JA7`/`6HM` 1.61 |  | PF08246, PF00112 | Homo sapiens | 7AS | 1 |
| B | opd | `P0A434` | 365 | `2OB3` 1.04 | `1QW7`/`EBP` 1.90 |  | PF02126 | Brevundimonas diminuta | BTB, ZN | 1 |
| B | SIRT3 | `Q9NTG7` | 399 | `3GLR` 1.80 | `4C7B`/`BVB` 2.10 |  | PF02146 | Homo sapiens | ZN | 1 |
| B | kmo | `Q84HF5` | 461 | `5NAK` 1.50 | `5Y66`/`7ZR` 2.34 |  | PF01494 | Pseudomonas fluorescens | FAD, KYN |  |
| B | AMY2A | `P04746` | 511 | `4X9Y` 1.07 | `4GQQ`/`0XR` 1.35 |  | PF00128, PF02806 | Homo sapiens | CA |  |
| B | Ptgs2 | `Q05769` | 604 | `3NT1` 1.73 | `3QH0`/`PLM` 2.10 |  | PF03098 | Mus musculus | BOG, HEM, NAG, NPS | 1 |
| B | LTA4H | `P09960` | 611 | `3B7S` 1.47 | `3FUD`/`692` 2.20 |  | PF09127, PF01433 | Homo sapiens | YB, ZN |  |
| B | Pck1 | `P07379` | 622 | `4GMU` 1.20 | `4YW8`/`1WD` 1.55 |  | PF00821 | Rattus norvegicus | GTP, MN, OXL |  |
| B | gyrB | `P66937` | 644 | `2XCS` 2.10 | `5NPK`/`94H` 1.98 |  | PF00204, PF00986, PF02518, PF01751 | Staphylococcus aureus | MN, RXV | 1 |
| B | Enpp2 | `Q64610` | 887 | `5DLT` 1.60 | `5M0E`/`7CR` 1.95 |  | PF01223, PF01663, PF01033 | Rattus norvegicus | 5JK, CA, ZN | 1 |
| B | PARP14 | `Q460N5` | 1801 | `5QI7` 1.05 | `5O2D`/`9HH` 1.60 |  | PF01661, PF00644 | Homo sapiens | GVV |  |
| B | rocF | `P53608` | 299 | `1CEV` 2.40 | `3CEV`/`ARG` 2.40 | Y | PF00491 | Bacillus caldovelox | MN |  |
| B | pfkA | `P00512` | 319 | `4I36` 2.30 | `4PFK`/`ADP` 2.40 | Y | PF00365 | Geobacillus stearothermophilus | - |  |
| B | PDC1 | `P06169` | 563 | `1PVD` 2.30 | `2VK1`/`PYR` 1.71 | Y | PF02775, PF00205, PF02776 | Saccharomyces cerevisiae | MG, TPP | 1 |
| B | PYGM | `P00489` | 843 | `7P7D` 1.45 | `8GPB`/`AMP` 2.20 | Y | PF00343 | Oryctolagus cuniculus | - |  |
| B | nirK | `P38501` | 376 | `4YSE` 1.20 | `1ZDS`/`ACM` 1.55 |  | PF00394, PF07732 | Alcaligenes faecalis | CU | 1 |

### 4.1 What the survivors fix

**Gap (a) — physiological effectors.** `../secondary/README.md` §5.2: "Every admitted effector
is a synthetic compound … Classical allosteric enzymology — cooperativity and feedback
inhibition by a metabolite — is therefore untested here, and that is the oldest and best-attested
form of the phenomenon the method claims to predict."

**13 survivors carry a physiological effector.** They include:

- **`PYGM` / AMP on glycogen phosphorylase** — the exact arm the set lost. `../secondary/README.md`
  §5.2 records it rejected on clause (ix), and §7.3 records why: measured on the `1FA9` dimer,
  the AMP site drew 8 lining residues from one protomer and 3 from the other. Measured here on
  **`8GPB` assembly1** — a different holo entry — one AMP copy is lined by chain A alone, while
  another copy is not. Tier **B**, `B_one_effector_copy_only`. **This does not overturn the
  rejection**; it says the rejection was entry-specific and `8GPB` deserves its own measurement.
- **`FBP1` / AMP on pig liver fructose-1,6-bisphosphatase.** Same chemistry as the human FBPase
  arm the 2026-08-24 sweep found. Both cannot enter — PF00316 admits one.
- **`FDPS` / FPP** — the arm §5.1 of the earlier record calls "the best clause (ii) evidence in
  the whole sweep", blocked there by a crystallisation anion. A different apo, `4NUA` at 1.43 Å,
  is proposed here. Its components are `MG, RIS`; `RIS` is risedronate, a bisphosphonate at the
  **catalytic** site, which is the `4KQU` escape route the earlier record describes — so this is
  the same freeze-level decision, not a new one.
- **`hisG` / histidine feedback on ATP-PRT**, **`rocF` / arginine on arginase**,
  **`LDHA` / oxaloacetate**, **`pfkA` / ADP**, **`pyrH` / GTP**, **`AMD1` / putrescine**,
  **`PDC1` / pyruvate**, **`NT5C2` / adenosine**, **`PDE10A` / cGMP**, **`kgd` / acetyl-CoA**.

Ten distinct metabolite chemistries, against zero in the frozen set.

**Gap (b) — small proteins.** `../secondary/README.md` §7.2: "The size ladder is thin at the
bottom, and one arm carries it", and the 2026-08-24 record concludes "**I found no new
admissible target below 272 residues**", with the mechanism "small catalytic domains are
overwhelmingly obligate oligomers, so they lose on (ix) before size is ever the question."

**Three survivors are below 272 residues** after the T4-lysozyme defect in §5 is removed:

| Target | aa | Tier | Note |
| --- | ---: | :-: | --- |
| `UBE2I` (SUMO E2, Ubc9) | **158** | **A** | Second-smallest target either set has seen, after `mkp5` at 147, and a monomer rather than an obligate oligomer. Holo `5F6Y` is a **triple mutant**, so clause (iv) must be measured, and see §6.2 on its active site |
| `pyrH` (*H. pylori* uridylate kinase) | 240 | B | Apo `4A7X` carries `UDP` — needs the site-relative measurement. Note the 2026-08-24 sweep rejected *Pyrococcus* and *E. coli* UMP kinases; this is a third organism and it passed (ix) here |
| `murI` (*H. pylori* glutamate racemase) | 255 | B | Apo carries `DGL`, D-glutamate — the substrate, so probably active-site, but that is the measurement |

The earlier conclusion is **too strong as written**. The correct statement is: no new admissible
target below 272 residues was found *from that frame*. From the ASD frame there are three
structural survivors, and whether any becomes admissible depends on clause (ii).

**Gap (c) — non-kinase, non-phosphatase families.** The 68 measured candidates span 61 Pfam
families and none is a protein kinase or a classical phosphatase. The 2026-08-24 record's advice
— "The fix is not to relax (xii); it is to stop proposing kinases" — is followed by construction
here, because ASD's frame is enzyme-wide rather than a kinase pile.

**Span.** The survivors run 158 to 1801 residues, **1.06 dex** against the frozen set's 0.86,
across **20 organisms** against the frozen set's four.

### 4.2 The curation references

Every DOI below is **ASD's own curation reference**, resolved from its PubMed id through NCBI
esummary on 2026-09-02. **Nobody has read any of these papers.** Clause (ii) asks whether
functional evidence establishes that *this modulator* at *this site* in *this structure* acts
allosterically, and a title is not that. The 2026-08-24 sweep killed `pdhk2` and `p300` at
exactly this step, both of which "looked perfect until someone read the paper".

| Target | Effector | Curation reference (ASD's, NOT READ) |
| --- | --- | --- |
| AMD1 | `PUT` | doi:10.1021/bi0268854 — Mechanism of human S-adenosylmethionine decarboxylase proenzyme processing as  |
| AMY2A | `0XR` | doi:10.1021/jm301273u — Order and disorder: differential structural impacts of myricetin and ethyl caf |
| birA | `BTX` | doi:10.1016/j.jmb.2015.02.021 — Allosteric coupling via distant disorder-to-order transitions. |
| CTSK | `6HM` | doi:10.1002/1873-3468.12495 — An allosteric site enables fine-tuning of cathepsin K by diverse effectors. |
| Enpp2 | `7CR` | doi:10.1021/acs.jmedchem.6b01743 — Rational Design of Autotaxin Inhibitors by Structural Evolution of Endogenous  |
| FBP1 | `AMP` | PMID Not in PubMed (no DOI in PubMed) — Mechanism of displacement of a catalytically essential loop from the active si |
| fbpC | `6Y1` | doi:10.1021/acsinfecdis.7b00003 — Exploring Covalent Allosteric Inhibition of Antigen 85C from Mycobacterium tub |
| FDPS | `FPP` | doi:10.1038/ncomms14132 — Human farnesyl pyrophosphate synthase is allosterically inhibited by its own p |
| GAA | `SC2` | doi:10.1038/s41467-017-01263-3 — Structure of human lysosomal acid α-glucosidase-a guide for the treatment of P |
| gyrB | `94H` | doi:10.1073/pnas.1700721114 — Thiophene antibacterials that allosterically stabilize DNA-cleavage complexes  |
| hisG | `HIS` | doi:10.1074/jbc.M212124200 — Crystal structure of ATP phosphoribosyltransferase from Mycobacterium tubercul |
| kgd | `ACO` | doi:10.1016/j.chembiol.2011.06.004 — Functional plasticity and allosteric regulation of α-ketoglutarate decarboxyla |
| kmo | `7ZR` | doi:10.1096/fj.201700397RR — Biochemistry and structural studies of kynurenine 3-monooxygenase reveal allos |
| lacS | `14O` | doi:10.1021/acssynbio.6b00097 — Full and Partial Agonism of a Designed Enzyme Switch. |
| LDHA | `OAA` | doi:10.1038/ncomms16018 — The self-inhibitory nature of metabolic networks and its alleviation through c |
| LGMN | `5KN` | doi:10.1038/ncomms14740 — Inhibition of delta-secretase improves cognitive functions in mouse models of  |
| LTA4H | `692` | doi:10.1021/jm900259h — Discovery of leukotriene A4 hydrolase inhibitors using metabolomics biased fra |
| murI | `003` | doi:10.1038/nature05689 — Exploitation of structural and regulatory diversity in glutamate racemases. |
| nirK | `ACM` | doi:10.1016/j.jmb.2006.02.042 — A rearranging ligand enables allosteric control of catalytic activity in coppe |
| NT5C2 | `ADN` | doi:10.1074/jbc.M700917200 — Crystal structure of human cytosolic 5'-nucleotidase II: insights into alloste |
| opd | `EBP` | doi:10.1016/j.abb.2005.08.012 — Structural and mutational studies of organophosphorus hydrolase reveal a crypt |
| PARP14 | `9HH` | doi:10.1021/acschembio.7b00445 — Discovery of a Selective Allosteric Inhibitor Targeting Macrodomain 2 of Polya |
| Pck1 | `1WD` | doi:10.1021/acs.biochem.5b00822 — Inhibition and Allosteric Regulation of Monomeric Phosphoenolpyruvate Carboxyk |
| PDC1 | `PYR` | doi:10.1074/jbc.M806228200 — Covalently bound substrate at the regulatory site of yeast pyruvate decarboxyl |
| PDE10A | `CMP` | doi:10.1074/jbc.M800595200 — Crystal structure of the GAF-B domain from human phosphodiesterase 10A complex |
| pfkA | `ADP` | doi:10.1098/rstb.1981.0059 — Phosphofructokinase: structure and control. |
| proRS | `3O6` | doi:10.1021/acsinfecdis.6b00078 — Biochemical and Structural Characterization of Selective Allosteric Inhibitors |
| Ptgs2 | `PLM` | doi:10.1074/jbc.M111.231969 — Human cyclooxygenase-2 is a sequence homodimer that functions as a conformatio |
| PYGM | `AMP` | doi:10.1016/0022-2836(91)90887-c — Structural mechanism for glycogen phosphorylase control by phosphorylation and |
| pyrH | `GTP` | doi:10.1107/S0907444912011407 — Structures of Helicobacter pylori uridylate kinase: insight into release of th |
| rocF | `ARG` | doi:10.1016/s0969-2126(99)80056-2 — Crystal structures of Bacillus caldovelox arginase in complex with substrate a |
| SIRT3 | `BVB` | doi:10.1016/j.chembiol.2013.09.019 — Crystal structures of Sirt3 complexes with 4'-bromo-resveratrol reveal binding |
| UBE2I | `5VM` | doi:10.1002/anie.201511351 — Insights Into the Allosteric Inhibition of the SUMO E2 Enzyme Ubc9. |
| USP7 | `8QQ` | doi:10.1038/nchembio.2528 — Discovery and characterization of highly potent and selective allosteric USP7  |

---

## 5. What was rejected, and one ASD data defect

| Target | UniProt | Holo/effector | Deciding clause | Measured |
| --- | --- | --- | --- | --- |
| E (T4 lysozyme) | `P00720` | `4PHU`/`2YB` | C_asd_curation_defect | `4PHU` is a GPR40 structure; `P00720` is its fusion partner. See below |
| E8Y329 | `E8Y329` | `4KGV`/`ATP` | C_dead_clause_iv | apo 3CSU UniProt ['P0A786'] |
| Q9TZZ6 | `Q9TZZ6` | `1NJJ`/`GET` | C_dead_clause_iv | apo 2TOD UniProt ['P07805'] |
| Q99AU2 | `Q99AU2` | `2HAI`/`PFI` | C_dead_clause_iv | apo 2FP7 UniProt ['P06935'] |
| Q76353 | `Q76353` | `5KRT`/`6W6` | C_dead_clause_iv | apo 4LH4 UniProt ['P12497'] |
| coaD | `A0A0X1KGP2` | `4RUK`/`COA` | C_dead_clause_ix | assembly1: best copy lined by ['A(A)', 'F(F)'] |
| ARO7 | `P32178` | `5CSM`/`TRP` | C_dead_clause_ix | assembly1: best copy lined by ['A(A)', 'A-2(A-2)'] |
| nagB | `P0A759` | `1FS5`/`16G` | C_dead_clause_ix | assembly1: best copy lined by ['A(A)', 'A-3(A-3)'] |
| dapA | `P0A6L2` | `1YXD`/`LYS` | C_dead_clause_ix | assembly1: best copy lined by ['A(A)', 'B(B)'] |
| kynA | `Q8PDA8` | `2NW8`/`TRP` | C_dead_clause_ix | assembly1: best copy lined by ['A(A)', 'B(B)'] |
| aroG | `Q9K169` | `4UC5`/`PHE` | C_dead_clause_ix | assembly1: best copy lined by ['A(A)', 'B(B)'] |
| IDH3A | `P50213` | `5GRI`/`CIT` | C_dead_clause_ix | assembly1: best copy lined by ['A(A)', 'B(B)'] |
| glgC | `P39669` | `5W5R`/`PYR` | C_dead_clause_ix | assembly1: best copy lined by ['A(A)', 'P(M)'] |
| gltA | `P0ABH7` | `1OWB`/`NAD` | C_dead_clause_ix | assembly1: best copy lined by ['A(A)', 'A-2(A-2)'] |
| Q9I000 | `Q9I000` | `5UXM`/`TRP` | C_dead_clause_ix | assembly1: best copy lined by ['A(A)', 'A-3(A-3)'] |
| PAH | `P00439` | `5FII`/`PHE` | C_dead_clause_ix | assembly1: best copy lined by ['A(A)', 'C(C)'] |
| CBS | `P35520` | `4UUU`/`SAM` | C_dead_clause_ix | assembly1: best copy lined by ['A(A)', 'B(B)'] |
| ppa | `P9WI55` | `5KDF`/`6RU` | C_dead_clause_ix | assembly1: best copy lined by ['A(A)', 'A-6(A-6)'] |
| GMDS | `O60547` | `5IN4`/`6CK` | C_dead_clause_ix | assembly1: best copy lined by ['A(A)', 'B(B)'] |
| MAT2A | `P31153` | `5UGH`/`8AJ` | C_dead_clause_ix | assembly1: best copy lined by ['A(A)', 'C(C)'] |
| CASP8 | `Q14790` | `3KJN`/`B93` | C_dead_clause_ix | assembly1: best copy lined by ['A(A)', 'B(B)'] |
| GBA1 | `P04062` | `5LVX`/`79B` | C_dead_clause_ix | assembly1: best copy lined by ['A(A)', 'B(B)'] |
| GLS | `O94925` | `3VP1`/`04A` | C_dead_clause_ix | assembly1: best copy lined by ['A(A)', 'A-2(A-2)', 'A-4(A-4)'] |
| FASN | `P49327` | `4W9N`/`TCL` | C_dead_clause_ix | assembly1: best copy lined by ['A(A)', 'B(B)'] |
| folA | `P0ABQ4` | `5CC9`/`NAP` | C_no_apo_candidate | no ASD-listed ligand-free entry <=2.5 A |
| trpE | `P00898` | `1I1Q`/`TRP` | C_no_apo_candidate | no ASD-listed ligand-free entry <=2.5 A |
| PKM | `P14618` | `3GR4`/`FBP` | C_no_apo_candidate | no ASD-listed ligand-free entry <=2.5 A |
| GFA1 | `P53704` | `2POC`/`UD1` | C_no_apo_candidate | no ASD-listed ligand-free entry <=2.5 A |
| ppc | `P00864` | `1JQN`/`ASP` | C_no_apo_candidate | no ASD-listed ligand-free entry <=2.5 A |
| ORF17 | `O40922` | `5V5D`/`8OY` | C_no_apo_candidate | no ASD-listed ligand-free entry <=2.5 A |
| GRESAG 4.1 | `Q99279` | `1FX2`/`DTT` | C_no_apo_candidate | no ASD-listed ligand-free entry <=2.5 A |
| GLUD1 | `P00366` | `-`/`GTP` | D_unmeasured | download_failed:HTTPError |
| nrdE | `P50620` | `6CGN`/`DA` | D_unmeasured | effector_DA_absent_from_assembly1 |
| MMP9 | `P14780` | `5UE4`/`5XQ` | D_unmeasured | effector_5XQ_absent_from_assembly1 |

**The curation defect is worth stating on its own.** ASD row `P00720` / `4PHU` / `2YB` reached
the final table and is **not a candidate at all**. `P00720` is **T4 lysozyme**, the
crystallisation fusion partner. `4PHU` is "Crystal structure of Human GPR40 bound to allosteric
agonist TAK-875", and ASD's own curation DOI for the row, `10.1038/nature13494`, is the GPR40
paper. The site is on the receptor; ASD mapped the row to the chaperone's UniProt. It passed
clause (ix) cleanly, because T4 lysozyme genuinely is one chain.

Nothing caught this except reading the structure title. **Any pipeline that consumes ASD must
check that the effector actually contacts the accession the row names.** This is the same class
of error as the `1OPL`/`AY7` case in `../secondary/evidence/databases.md` §4: the database is
internally consistent and externally wrong.

---

## 6. What this cannot fix

Stated flatly, because everything above is a supply result and none of it is an admission.

1. **Clause (ii) is not established for a single row, and it is the whole remaining cost.**
   Every DOI in §4.2 is ASD's curation reference. ASD's own admission rule sits on the
   **protein**, not the site (`../secondary/evidence/databases.md` §3.1), so an ASD row is not
   evidence that this modulator at this site is allosteric. At the 2026-08-24 measured rate of
   29 %, roughly **10 of 34** survivors would die on a literature pass — and that rate was
   measured on candidates that had already been hand-picked. Expect worse here. **The honest
   number of new admissible arms today is zero, and the honest number of new *leads* is 34.**

2. **No active-site rule is established for any row.** Clause (vii) needs a propagation source,
   and `allo.inputs` derives it from `{from_ligands: …}` or `{from_motifs: …}`
   (`src/allo/inputs.py`). This sweep checked only that ASD records a catalytic mechanism. It did
   **not** check that a PROSITE `PA` line matches exactly once on the modelled apo chain, or that
   a cofactor is present in the apo. The 2026-08-24 record shows this failing twice on otherwise
   clean candidates (`pfk_tbrucei` needed a new motif; `p300`'s only clean apo held no CoA), and
   `../secondary/README.md` §7.4 records twelve rejections on it. **`UBE2I` is the row most
   exposed**: Ubc9 has a catalytic cysteine but no cofactor, and its "active site" is a
   thioester-transfer centre — the same curatorial judgement the 2026-08-24 record flags for
   `cblb`, and the same brush with §7.4's "non-catalytic targets are out of scope".

3. **Clause (iii)/(x) was not measured.** Apo entries holding the effector component itself were
   hard-excluded. Everything else is listed, not measured. Whether `1NUY`'s `F6P` or `4A7X`'s
   `UDP` reaches into the site being predicted needs the labels transferred to the apo by
   `allo.groundtruth.labels.align_numbering` and a distance measurement, which this sweep did not
   run. The 2026-08-24 rate on this clause was **40 %** of the candidates that survived (ix).

4. **Clause (iv) was checked as UniProt identity, not as sequence identity.** Nine survivors are
   flagged because the holo title names a mutant or an engineered variant. `UBE2I`'s holo is a
   **triple** mutant, `birA`'s is G142A, `PDC1`'s is D28A, `lacS`'s is W33G, `opd` is an
   engineered variant with "increased activity". The ≥ 90 % bar is almost certainly met; the
   point is that it was **not measured**, and the 2026-08-24 sweep found this clause costing
   nothing across 14 measured pairs, so this is a cheap gap to close rather than a likely killer.

5. **Two survivors carry a covalent modulator** (`fbpC`, `LGMN`). AlloBench removes these by rule
   — "Structures with covalently bound allosteric modulators were removed"
   (`../secondary/evidence/databases.md` §3.4) — and this repo has no clause either way. That is
   a decision, not a measurement.

6. **`gyrB`'s holo is a protein/DNA complex** and three more carry glycans. Clause (v) matches
   the oligomeric state between the members, and ADR 0010 fixes the node set to one protein
   chain, so the DNA has nowhere to go. `gyrB` should be treated as dead until someone argues
   otherwise.

7. **The apo pool is under-sampled, by construction.** Apo candidates came from each ASD entry's
   own `PDB_List`. Any apo entry ASD does not list is invisible to this sweep. The seven rows
   killed as `C_no_apo_candidate` are therefore "no apo **in ASD**", not "no apo". A per-UniProt
   RCSB query would find more. **`PKM` is the proof**: it survived every clause here, and then
   lost its apo because every ASD-listed ligand-free PKM entry either holds FBP or fails (xi) —
   yet the 2026-08-24 sweep found `1ZJH`, 2.20 Å with zero heteroatoms, independently.

8. **Interface sites are still excluded, and the class is still the one being lost.** Clause (ix)
   killed 487 records for free plus 19 on measurement. `../secondary/README.md` §7.3 and the
   2026-08-24 record both say what this costs: metabolite feedback and cooperativity are
   quaternary phenomena, so the class being excluded is the class gap (a) is trying to add.
   **Nothing in this sweep changes that.** Thirteen physiological effectors survived because
   their *pockets* are intra-chain, not because their *mechanisms* are — `PYGM`, `FBP1` and
   `rocF` are all classically cooperative oligomers. Every one of those arms needs the same
   clause (viii) disclosure the 2026-08-24 record writes for `fbpase` and `gdh`.

9. **Adding arms is a re-freeze, not a repair.** `../secondary/README.md` §7.1 and §7.10 both
   argue this, and it is unchanged: adding any target re-runs the seeded size-stratified split
   and changes every existing tier assignment. This document does not propose a re-freeze. It
   establishes that the supply exists, which §7.1 currently denies — "Two independent exhaustive
   frames produced 5 further admissible targets between them. That is the supply."

10. **ASD's licence forbids redistribution.** The archives are under `data/external/asd/`, which
    `.gitignore` excludes. **Do not commit them.** A derived candidate list — names, accessions,
    DOIs — is not the data and is fine; a verbatim ASD file is not.

11. **The 3147-record frame is not exhaustive either.** ASD's last release is 2023-09-20. Three
    years of depositions are missing from it, and the RCSB full-text frame the 2026-08-24 sweep
    used remains the complement. The two frames should be unioned, not swapped.

---

## 7. What should happen next, in cost order

1. **Correct `../secondary/evidence/databases.md`.** Three rows are now wrong: ASD's fetch
   route, ASD's licence ("none stated" → the verbatim research-use clause), and ASBench's
   ("formats never seen" → three files at HTTP 200). One paragraph, no re-freeze.
2. **Correct `../secondary/README.md` §7.2**, which states "No new admissible target is below
   272 residues" without the qualifier "from that frame".
3. **Run clause (iii)/(x) and the active-site derivation** on the 13 physiological survivors.
   That is one script against `allo.inputs` and `allo.groundtruth.labels`, and it converts
   "structural survivor" into "candidate a reviewer can argue about".
4. **Read the papers**, physiological rows first. This is the only step that produces an
   admissible arm, and it is the step no amount of database work replaces —
   `../secondary/README.md` §3 predicted exactly this and it is still true.
   **Started 2026-09-02** in [`14-clause-ii-literature-pass.md`](14-clause-ii-literature-pass.md):
   13 pass, 5 fail, 16 blocked by publisher paywalls. What remains is a library visit for the
   sixteen, and the six clause-(ii)-clean rows with no known structural blocker are where the
   next structural measurement should go: `hisG`, `UBE2I`, `PDC1`, `LGMN`, `proRS`, `fbpC`.

**None of this re-freezes the secondary set, and the recommendation is unchanged.** Adding an
arm re-runs the seeded tier split and reassigns every existing arm, which is a re-freeze rather
than a repair. The leads are recorded; the decision stays where `docs/ROADMAP.md` puts it.

---

## Provenance

Every status code, byte count, resolution, Pfam family and chain count in this document came
from a live fetch or a file read on 2026-09-01T20:56Z–21:10Z UTC (repository date 2026-09-02).
Nothing is recalled. Clause (ix) was measured on `files.rcsb.org/download/<PDB>-assembly1.cif.gz`,
model 1, effector heavy atoms against protein heavy atoms at 4.5 Å, grouped by `label_asym_id`
so that symmetry copies are distinguished — the same measurement `tests/test_secondary.py`
makes. The 27 blocked Pfam families were read from `../primary/manifest.yaml` and
`../secondary/manifest.yaml`, not recalled.
