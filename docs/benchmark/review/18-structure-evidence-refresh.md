# 18 — Structure evidence for the six frozen primary arms, refetched after the reply

**Fetched:** 2026-09-02 from `data.rcsb.org/rest/v1/core`, the wwPDB validation reports at
`files.rcsb.org/pub/pdb/validation_reports/`, and — new in this pass — the **deposited
mmCIF** of every entry from `files.rcsb.org/download/`.
**Raw bytes:** `data/rcsb-2026-09-refresh/<PDB_ID>/`, one directory per entry, plus
`_chemcomp/`. **Derived table:** `data/structure-evidence-refresh.json`.
**Re-run:**

```
python3   docs/benchmark/review/data/fetch_refresh_2026_09.py      # cache, reuses what exists
uv run python docs/benchmark/review/data/extract_refresh_2026_09.py # derive + print
```

**Why this exists.** `08-structure-evidence.md` was written before the organisers' reply
(`00-official-reply.md`) moved two arms. `bcr_abl1_mandated` changed from `1OPL:A` to
`1OPL:B`; `cardiac_myosin_mandated` was created for the first time as `5TBY:A` → `9GZ2:A`.
This pass is narrower — nine accessions instead of 33 — and deeper: it reads the deposited
coordinate file, so per-chain B-factors, occupancies, `_struct_ref_seq` ranges,
`_struct_conn` records and audit history come from the primary artifact rather than from a
REST summary.

**Scope, confirmed from `docs/benchmark/primary/frozen.json`.** The frozen set has **six**
arms over **nine** distinct accessions.

| arm                        | tier      | apo          | holo                 | nodes a method receives | scored candidates |
| -------------------------- | --------- | ------------ | -------------------- | ----------------------: | ----------------: |
| `kras_g12c_mandated`       | mandated  | `4OBE:A`     | `6OIM:A` (`MOV`)     |                     169 |               146 |
| `kras_g12c_corrected`      | corrected | `4LDJ:A`     | `6OIM:A` (`MOV`)     |                     170 |               148 |
| `bcr_abl1_mandated`        | mandated  | **`1OPL:B`** | `5MO4:A` (`AY7`)     |                     365 |               354 |
| `bcr_abl1_corrected`       | corrected | `2G2H:A`     | `5MO4:A` (`AY7`)     |                     272 |               261 |
| `cardiac_myosin_mandated`  | mandated  | **`5TBY:A`** | **`9GZ2:A`** (`XB2`) |                     954 |               932 |
| `cardiac_myosin_corrected` | corrected | `9GZ3:A`     | `9GZ2:A` (`XB2`)     |                     764 |               743 |

Every number below is read from a named API field, a validation-report attribute, or an
mmCIF category. Where the database carries no value the cell is `—` and the JSON holds
`null`. Nothing here is filled in from a paper or from memory.

---

## 0. Headline

**Nothing `08` recorded for these nine entries has drifted.** A field-by-field comparison of
`structure-evidence.json` against `structure-evidence-refresh.json` — resolution, R-work,
R-free, deposit/release/revision dates, wwPDB version, revision count, space group,
clashscore and its percentile, Ramachandran, sidechain and RSRZ percentages, per-chain
modelled-residue counts, and every ligand instance's RSCC, RSR and clash count —
compares **175 paired values and finds 0 differences**. The news is in the dimensions `08`
did not open.

1. **`5TBY`'s B-factor column is not a B-factor column.** `_atom_site.B_iso_or_equiv` runs
   **0.00–7.30 Å², mean 2.45** across all six chains. Every other entry in the set has a
   minimum of at least 3.60 and a mean between 12.9 and 123.3. A 20 Å model cannot have
   displacement parameters near zero, and the entry has no `refine` block that could have
   produced any. The column carries something that is not a thermal parameter. §9.

2. **Mavacamten in `9GZ2` carries B = 0.00 on all 20 atoms.** In the same file `ADP` is at
   41.76, `PO4` at 50.49, `MG` at 42.39, and the polymer averages 57.50. `XB2` is the only
   group in the entry at zero. This is the ligand whose contact footprint **defines the
   label set of both cardiac-myosin arms** (`9GZ2:A:XB2`, 12 residues in `frozen.json`), and
   it is also the only ligand in all nine entries whose "subject of investigation" flag is
   author-assigned rather than RCSB-assigned. §5.

3. **All four repository claims about `1OPL` chain B are confirmed from primary data**, and
   the fourth is now exact. Chain B has no `MYR` (`MYR` is `auth_asym_ids: ["A"]`); it keeps
   `P16` at auth 538; it carries **no SH3 domain in CATH, SCOP or ECOD** where chain A
   carries one in all three; and its polymer atoms hold exactly **three distinct B values —
   160.84 (1455 atoms), 198.13 (776), 161.17 (723)** — against 3041 in chain A, which is
   what `_refine.details` says was done. §8.

4. **`1OPL` has three deposited assemblies, not one.** Assembly 1 monomeric
   (author-defined), assembly 2 monomeric (PISA), assembly 3 **dimeric** (PISA,
   software-defined, A2). `08` reported only assembly 1. The frozen arm selects one chain,
   so nothing moves, but "the biological assembly" is not a single answer for this entry. §7.

5. **RCSB's `pdbx_mutation` free text for `1OPL` is wrong, and the manifest is right.**
   RCSB says `D382N, K29R, E29D`. The deposited `_struct_ref_seq_dif` says auth 29 ARG←LYS,
   auth **30** ASP←GLU, auth 382 ASN←ASP — that is **E30D**, not E29D. `manifest.yaml`
   records "K29R, E30D, D382N", which matches the file. §4a.

6. **The revision count depends on which artifact you read.** REST
   `pdbx_audit_revision_history` gives `9GZ2` two rows and `9GZ3` one; the deposited
   `_pdbx_audit_revision_history` gives **11** and **9**, and the validation report's
   `PDB-revision-number` agrees with the file (11, 9). Both counts are correct about
   different things — distinct versions versus audit rows — and `08`'s "revisions" column is
   the REST one. §2.

7. **ECOD domain names on RCSB are unstable and meaningless here.** `1OPL:A` domain
   `e1oplA3` was named `LRR_6,LRR_RI_capping` in the 2026-08 cache and is named
   `Hexapep,Acetyltransf_11` in today's. Both describe the ABL1 kinase domain. `5TBY` has
   **no CATH and no SCOP assignment at all** — only ECOD, which calls myosin `Med6` and
   `LpxC`. Do not quote an ECOD name as a domain identity. §6, §11 C4.

8. **`5TBY`'s template chain is a model of a model.** `_em_3d_fitting_list` has six rows,
   all `3JBH`, all typed `experimental model`, with `pdb_chain_residue_range` 1–962 (heavy
   chains), 1–156, 1–196. `_pdbx_database_related` names `EMD-1950` (tarantula cryo-EM),
   `3jBH`, and `EMD-2240` (human heart, negative stain). §9.

9. **Two X-ray facts nobody had written down.** `1OPL` has the worst data completeness in
   the set at **89.01 %** (validation `DataCompleteness`), against 94.0–99.6 % elsewhere;
   and `5MO4`'s single sub-unit-occupancy residue is **Met256 alone**, a two-conformer
   methionine, not a coverage defect. §1a and §5.

---

## 1. Dimension 1 — experimental provenance

### 1a. Method, resolution, refinement

`rcsb_entry_info.experimental_method` / `.resolution_combined[0]`,
`refine[0].ls_R_factor_R_work` / `.ls_R_factor_R_free`, `symmetry.space_group_name_H_M`,
`refine.pdbx_method_to_determine_struct` and `.pdbx_starting_model` from the mmCIF, plus the
validation report's independently recomputed `DCC_R` / `DCC_Rfree` and `DataCompleteness`.

| PDB    | role                   | method | res (Å) |  R-work |  R-free |  EDS R | DCC R-free | data compl. % | space group | phasing / starting model           |
| ------ | ---------------------- | ------ | ------: | ------: | ------: | -----: | ---------: | ------------: | ----------- | ---------------------------------- |
| `4OBE` | apo (kras mandated)    | X-ray  |    1.24 |  0.1566 |  0.1686 | 0.1580 |     0.1560 |         94.02 | C 1 2 1     | MR, `4EPV`                         |
| `4LDJ` | apo (kras corrected)   | X-ray  |    1.15 |  0.1318 |  0.1622 | 0.1294 |     0.1520 |         99.60 | P 21 21 21  | MR, `4EPV`                         |
| `1OPL` | apo (abl1 mandated)    | X-ray  |    3.42 |   0.306 |   0.315 | 0.2760 |     0.2905 |     **89.01** | C 2 2 21    | MR, `1M52` + `2ABL`                |
| `2G2H` | apo (abl1 corrected)   | X-ray  |    2.00 |   0.193 |   0.213 | 0.1912 |     0.2132 |         96.86 | P 21 21 2   | MR, `1M52`                         |
| `5TBY` | apo (myosin mandated)  | EM     |    20.0 |       — |       — |      — |          — |             — | —           | rigid-body fit of `3JBH`           |
| `9GZ3` | apo (myosin corrected) | EM     |     3.4 |       — |       — |      — |          — |             — | —           | flexible fit, initial model `6Z47` |
| `6OIM` | holo (both kras)       | X-ray  |    1.65 | 0.18092 | 0.21519 | 0.1874 |     0.2201 |         96.98 | P 21 21 21  | MR                                 |
| `5MO4` | holo (both abl1)       | X-ray  |    2.17 |  0.1818 |  0.2170 | 0.1833 |     0.2161 |         98.48 | C 2 2 21    | MR                                 |
| `9GZ2` | holo (both myosin)     | EM     |     2.9 |       — |       — |      — |          — |             — | —           | flexible fit, initial model `6Z47` |

`5TBY`, `9GZ2` and `9GZ3` are cryo-EM and carry no crystallographic R-factors. For `5TBY`
the `refine` category **exists** in the mmCIF with exactly three non-null values:
`entry_id = 5TBY`, `pdbx_refine_id = ELECTRON MICROSCOPY`, `ls_d_res_high = 20.00`.
`9GZ2` and `9GZ3` have no `refine` category at all — the honest state for a cryo-EM entry.
`5TBY`'s is the anomaly: a refinement block with nothing refined in it.

`1OPL`'s `_refine.details`, verbatim and load-bearing for §8 and §10:

> The structure was refined by superimposing the refined high resolution structure of c-Abl
> (pdb entry 1OPK) on the molecular replacement solution and optimizing positions of
> individual domains by rigid-body refinement. Following this, **only overall domain
> B-factors were applied to molecule B, whereas individual B-factors were refined for
> molecule A.**

`6OIM`'s is `HYDROGENS HAVE BEEN ADDED IN THE RIDING POSITIONS`. `2G2H`, `4LDJ`, `4OBE`,
`5MO4` and `5TBY` carry `?`; `9GZ2` and `9GZ3` have no `_refine` category to carry one.

### 1b. Cryo-EM specifics

`em_3d_reconstruction[0]`, `em_3d_fitting[0]`, `_em_3d_fitting_list`, `_em_software`.

| PDB    | EMDB      | map res (Å) | criterion           | particles | fit protocol       | target                  | model fitting | model refinement     |
| ------ | --------- | ----------: | ------------------- | --------: | ------------------ | ----------------------- | ------------- | -------------------- |
| `5TBY` | EMD-2240  |        20.0 | **FSC 0.5 CUT-OFF** |    10 700 | **RIGID BODY FIT** | CORRELATION COEFFICIENT | UCSF Chimera  | **`?` — none named** |
| `9GZ3` | EMD-51721 |         3.4 | FSC 0.143 CUT-OFF   |    88 809 | FLEXIBLE FIT       | —                       | ISOLDE, Coot  | PHENIX               |
| `9GZ2` | EMD-51720 |         2.9 | FSC 0.143 CUT-OFF   |   200 487 | FLEXIBLE FIT       | —                       | ISOLDE, Coot  | PHENIX               |

`5TBY` differs on every column: the only worse-than-4 Å map, the only `FSC 0.5` criterion,
the only rigid-body fit, the only entry whose sole model-fitting program is a visualisation
tool, and the only one with no model-refinement program.

---

## 2. Dimension 1 (cont.) — dates, versions, and released experimental data

`rcsb_accession_info.*`, the deposited `_pdbx_audit_revision_history`, and
`rcsb_entry_container_identifiers.emdb_ids`.

| PDB    | deposited  | released   | latest revision | version | audit rows (mmCIF) | audit rows (REST) | validation report created | report revision | structure factors / map released |
| ------ | ---------- | ---------- | --------------- | :-----: | -----------------: | ----------------: | ------------------------- | :-------------: | :------------------------------: |
| `4OBE` | 2014-01-07 | 2014-06-04 | 2023-09-20      |   1-2   |                  3 |                 3 | 2026-04-25                |        3        |              Y (SF)              |
| `4LDJ` | 2013-06-24 | 2014-06-04 | 2023-09-20      |   1-3   |                  4 |                 4 | 2026-03-07                |        4        |              Y (SF)              |
| `1OPL` | 2003-03-06 | 2003-04-08 | 2023-08-16      |   1-4   |                  5 |                 5 | 2026-03-20                |        5        |              Y (SF)              |
| `2G2H` | 2006-02-16 | 2006-05-23 | 2023-08-30      |   1-4   |                  5 |                 5 | 2026-03-09                |        5        |              Y (SF)              |
| `5TBY` | 2016-09-13 | 2017-06-07 | 2024-10-23      |   1-9   |                 10 |                10 | 2026-03-09                |       10        |         Y (map EMD-2240)         |
| `9GZ3` | 2024-10-03 | 2025-03-12 | 2025-03-12      |   1-0   |              **9** |             **1** | 2026-03-06                |        9        |        Y (map EMD-51721)         |
| `6OIM` | 2019-04-09 | 2019-11-06 | 2024-11-13      |   1-4   |                  5 |                 5 | 2026-03-06                |        5        |              Y (SF)              |
| `5MO4` | 2016-12-13 | 2017-04-05 | 2024-05-08      |   1-2   |                  3 |                 3 | 2026-03-09                |        3        |              Y (SF)              |
| `9GZ2` | 2024-10-03 | 2025-03-12 | 2025-11-12      |   1-1   |             **11** |             **2** | 2026-03-20                |       11        |        Y (map EMD-51720)         |

All nine report `rcsb_accession_info.has_released_experimental_data = "Y"`. For the six
X-ray entries that means released structure factors, which is why all six carry an RSRZ and
per-ligand RSCC below; for the three cryo-EM entries it means a released map, which carries
no electron-density fit at all.

`9GZ2` and `9GZ3` are the only entries where the two audit counts disagree. The deposited
file records nine rows all stamped `1-0 / 2025-03-12` for `9GZ3` and eleven rows (nine at
`1-0`, two at `1-1 / 2025-11-12`) for `9GZ2` — several mmCIF categories revised in the same
release. REST collapses them to distinct versions. Neither is wrong; the two count different
things, and `08`'s table used the REST number.

---

## 3. Dimension 1 (cont.) — wwPDB validation percentiles

From the report's `<Entry>` element. Percentiles run 0 (worst) to 100 (best); absolute is
against the whole PDB, relative against the entry's resolution band (`percentilebins`).

| PDB    |     clash |     abs |  rel |   Rama % |     abs |  rel | sidechain % |  abs |  rel | RSRZ % |  abs |  rel | bins          |
| ------ | --------: | ------: | ---: | -------: | ------: | ---: | ----------: | ---: | ---: | -----: | ---: | ---: | ------------- |
| `4OBE` |      1.11 |    95.7 | 86.1 |     0.00 |     100 |  100 |        0.00 |  100 |  100 |   2.95 | 53.5 | 54.7 | all,1.24,xray |
| `4LDJ` |      1.10 |    95.7 | 87.7 |     0.00 |     100 |  100 |        0.00 |  100 |  100 |   0.00 |  100 |  100 | all,1.15,xray |
| `1OPL` |     11.29 |    20.1 | 50.2 |     0.62 |    21.0 | 49.3 |        2.95 | 36.0 | 58.6 |   6.50 | 24.6 | 19.3 | all,3.42,xray |
| `2G2H` |     12.90 |    16.4 | 13.3 |     0.74 |    18.3 | 14.1 |        2.10 | 46.7 | 52.0 |  13.42 |  6.8 |  5.9 | all,2.0,xray  |
| `5TBY` | **51.30** | **1.7** |  1.7 | **5.96** | **2.0** |  1.0 |        1.96 | 47.7 | 19.6 |      — |    — |    — | all,em        |
| `9GZ3` |      1.54 |    91.8 | 93.2 |     0.26 |    37.2 | 22.2 |        0.15 | 85.5 | 63.7 |      — |    — |    — | all,em        |
| `6OIM` |      1.46 |    92.6 | 89.4 |     0.00 |     100 |  100 |        0.00 |  100 |  100 |   2.40 | 59.5 | 64.7 | all,1.65,xray |
| `5MO4` |      1.19 |    95.0 | 96.6 |     0.00 |     100 |  100 |        0.85 | 73.0 | 83.4 |   5.13 | 33.2 | 32.5 | all,2.17,xray |
| `9GZ2` |      1.78 |    89.2 | 91.9 |     0.00 |     100 |  100 |        0.15 | 85.5 | 63.7 |      — |    — |    — | all,em        |

Every value reproduces `08` exactly. `5TBY` is the worst entry on clashscore and on
Ramachandran outliers by a wide margin — 51.30 against a next-worst 12.90, and 5.96 %
against a next-worst 0.74 %. `2G2H` is the worst on RSRZ (13.42 %, 6.8th percentile), which
matters because it is the **corrected** BCR-ABL1 apo and therefore the confirmatory input.

---

## 4. Dimension 2 — polymer entities, source, and UniProt mapping

`rcsb_entity_source_organism`, `rcsb_polymer_entity_container_identifiers.uniprot_ids`, and
`_struct_ref` / `_struct_ref_seq` from the deposited file. The auth↔UniProt ranges are the
answer to "which numbering is this entry in".

| PDB    | ent | description                                  | chains | organism (taxid)    | UniProt  | `_struct_ref_seq` auth ↔ UniProt | sample len | RCSB mut. count |
| ------ | :-: | -------------------------------------------- | ------ | ------------------- | -------- | -------------------------------- | ---------: | :-------------: |
| `4OBE` |  1  | GTPase KRas                                  | A, B   | Homo sapiens (9606) | `P01116` | 1–169 ↔ 1–169                    |        170 |        0        |
| `4LDJ` |  1  | GTPase KRas                                  | A      | Homo sapiens (9606) | `P01116` | 1–169 ↔ 1–169                    |        170 |        1        |
| `1OPL` |  1  | proto-oncogene tyrosine-protein kinase       | A, B   | Homo sapiens (9606) | `P00519` | 1–531 ↔ 1–531                    |        537 |        3        |
| `2G2H` |  1  | Abl Tyrosine                                 | A, B   | Homo sapiens (9606) | `P00519` | **248–531 ↔ 229–512**            |        287 |        1        |
| `5TBY` |  1  | Myosin-7                                     | A, B   | Homo sapiens (9606) | `P12883` | 1–1935 ↔ 1–1935                  |       1935 |        0        |
| `5TBY` |  2  | Myosin light chain 3                         | C, D   | Homo sapiens (9606) | `P08590` | 1–195 ↔ 1–195                    |        195 |        0        |
| `5TBY` |  3  | Myosin regulatory light chain 2, ventricular | E, F   | Homo sapiens (9606) | `P10916` | 1–166 ↔ 1–166                    |        166 |        0        |
| `9GZ3` |  1  | Myosin-7                                     | A      | Homo sapiens (9606) | `P12883` | 2–1138 ↔ 2–1138                  |       1145 |        1        |
| `6OIM` |  1  | GTPase KRas                                  | A      | Homo sapiens (9606) | `P01116` | 1–169 ↔ 1–169                    |        183 |        4        |
| `5MO4` |  1  | Tyrosine-protein kinase ABL1                 | A      | Homo sapiens (9606) | `P00519` | **46–534 ↔ 27–515**              |        495 |        0        |
| `9GZ2` |  1  | Myosin-7                                     | A      | Homo sapiens (9606) | `P12883` | 2–1138 ↔ 2–1138                  |       1145 |        1        |

Every polymer in every entry is human. There is no cross-species contamination anywhere in
the six frozen arms — which is exactly what the `6C1H` substitution removed.

**The ABL1 numbering offset is now explicit.** `1OPL` is auth = UniProt (1b numbering,
offset 0). `2G2H` and `5MO4` both carry an auth↔UniProt offset of **+19** (248↔229, 46↔27).
So `2G2H` and `5MO4` share a numbering convention with each other, and `1OPL` uses a
different one — the manifest's `active_site: {from_motifs: [...]}` rule exists because of
exactly this, and the primary files confirm it.

### 4a. Sequence differences, from `_struct_ref_seq_dif`

Author numbering. `engineered mutation` / `variant` / `conflict` are the depositor's own words.

| PDB            | position                       | PDB → UniProt                                               | depositor category                                                    |
| -------------- | ------------------------------ | ----------------------------------------------------------- | --------------------------------------------------------------------- |
| `4OBE`         | 0                              | GLY → (none)                                                | expression tag (both chains)                                          |
| `4LDJ`         | 0 / **12**                     | GLY → (none) / **CYS ← GLY**                                | expression tag / **engineered mutation (G12C)**                       |
| `1OPL`         | 29 / **30** / 382              | ARG ← LYS / **ASP ← GLU** / ASN ← ASP                       | engineered mutation ×3 (both chains)                                  |
| `1OPL`         | 532–537                        | ENLYFQ                                                      | cloning artifact                                                      |
| `2G2H`         | 245–247 / **415**              | GHM / **PRO ← HIS**                                         | cloning artifact / engineered mutation (= H396P in UniProt numbering) |
| `5TBY`         | —                              | none                                                        | —                                                                     |
| `9GZ3`, `9GZ2` | **1124** / 1139–1146           | **SER ← ALA** / DYKDDDDK                                    | variant / expression tag (FLAG)                                       |
| `6OIM`         | −13…0 / **12** / 51 / 80 / 118 | His-tag / **CYS ← GLY** / SER ← CYS / LEU ← CYS / SER ← CYS | expression tag / variant / engineered mutation ×3                     |
| `5MO4`         | 40–45 / **334** / **382**      | GAMDPS / **ILE ← THR** / **ASN ← ASP**                      | expression tag / conflict ×2                                          |

`5MO4` is the entry where RCSB's two mutation fields disagree — `pdbx_mutation = "T334I
D382N"` against `entity_poly.rcsb_mutation_count = 0`. The deposited file settles it: the
differences exist and the depositor typed them as `conflict` rather than `engineered
mutation`, which is why the derived count is zero. Both substitutions are real.

`1OPL`'s RCSB `pdbx_mutation` string reads `D382N, K29R, **E29D**`. The file says the third
change is at auth **30**, GLU→ASP. `manifest.yaml` records `K29R, E30D, D382N` and is
correct; RCSB's free-text field is not.

**Modified residues: none.** `_pdbx_struct_mod_residue` is absent from all nine deposited
files. No phosphorylation, no glycosylation, no non-standard amino acid anywhere in the set.
`branched_entity_count` is 0 for all nine — no carbohydrates either.

---

## 5. Dimension 2 (cont.) — every non-polymer entity

`pdbx_entity_nonpoly` + `chemcomp` for identity, `_atom_site` for atom count, occupancy and
group B, and `nonpolymer_entity_instance.rcsb_nonpolymer_instance_validation_score[0]` for
the density fit. `SOI` is RCSB's `is_subject_of_investigation` with its provenance.

| PDB    | comp     | name                                          | formula             | FW (Da) | chain | auth seq | atoms | occ. |    group B |      SOI       |      RSCC |   RSR |     compl. | clashes | flags                    |
| ------ | -------- | --------------------------------------------- | ------------------- | ------: | :---: | -------: | ----: | ---: | ---------: | :------------: | --------: | ----: | ---------: | ------: | ------------------------ |
| `4OBE` | `GDP`    | guanosine-5'-diphosphate                      | C10 H15 N5 O11 P2   | 443.201 |   A   |      201 |    37 |  1.0 |      14.67 |    Y (RCSB)    |     0.982 | 0.056 |       1.00 |       0 | metal coord.             |
| `4OBE` | `MG`     | magnesium ion                                 | Mg                  |  24.305 |   A   |      202 |     1 |  1.0 |       9.28 |       N        |     0.996 | 0.046 |       1.00 |       0 | metal coord.             |
| `4OBE` | `GDP`    | "                                             | "                   | 443.201 |   B   |      201 |    37 |  1.0 |      13.80 |    Y (RCSB)    |     0.986 | 0.051 |       1.00 |       0 | metal coord.             |
| `4OBE` | `MG`     | "                                             | Mg                  |  24.305 |   B   |      202 |     1 |  1.0 |       8.82 |       N        |     0.996 | 0.015 |       1.00 |       0 | metal coord.             |
| `4LDJ` | `GDP`    | "                                             | "                   | 443.201 |   A   |      201 |    40 |  1.0 |      10.20 |    Y (RCSB)    |     0.988 | 0.042 |       1.00 |       0 | metal coord.             |
| `4LDJ` | `MG`     | "                                             | Mg                  |  24.305 |   A   |      202 |     1 |  1.0 |       6.57 |       N        |     0.996 | 0.066 |       1.00 |       0 | metal coord.             |
| `1OPL` | `MYR`    | myristic acid                                 | C14 H28 O2          | 228.371 | **A** |      538 |    15 |  1.0 |      84.35 |    Y (RCSB)    |     0.902 | 0.246 | **0.9375** |       3 | no covalent linkage      |
| `1OPL` | `P16`    | 6-(2,6-dichlorophenyl)-…-pyrido[2,3-d]pyrimidin-7(8H)-one | C21 H16 Cl2 N4 O2   | 427.283 |   A   |      539 |    29 |  1.0 |      85.49 |    Y (RCSB)    |     0.842 | 0.182 |       1.00 |       2 | no covalent linkage      |
| `1OPL` | `P16`    | "                                             | "                   | 427.283 | **B** |      538 |    29 |  1.0 | **152.41** |    Y (RCSB)    | **0.582** | 0.197 |       1.00 |   **5** | **IS_RSCC_OUTLIER**      |
| `2G2H` | `P16`    | "                                             | "                   | 427.283 |   A   |      532 |    29 |  1.0 |      19.52 |    Y (RCSB)    |     0.839 | 0.128 |       1.00 |       4 | no covalent linkage      |
| `2G2H` | `P16`    | "                                             | "                   | 427.283 |   B   |      532 |    29 |  1.0 |      29.97 |    Y (RCSB)    |     0.809 | 0.150 |       1.00 |       0 | no covalent linkage      |
| `5TBY` | _(none)_ | —                                             | —                   |       — |   —   |        — | **0** |    — |          — |       —        |         — |     — |          — |       — | zero heteroatoms         |
| `9GZ3` | `MG`     | magnesium ion                                 | Mg                  |  24.305 |   A   |     1201 |     1 |  1.0 |      20.75 |       N        |         — |     — |       1.00 |       0 | metal coord.             |
| `9GZ3` | `ADP`    | adenosine-5'-diphosphate                      | C10 H15 N5 O10 P2   | 427.201 |   A   |     1202 |    27 |  1.0 |      22.72 |    Y (RCSB)    |         — |     — |       1.00 |       1 | metal coord.             |
| `9GZ3` | `PO4`    | phosphate ion                                 | O4 P                |  94.971 |   A   |     1203 |     5 |  1.0 |      28.28 |       N        |         — |     — |       1.00 |       1 | metal coord.             |
| `6OIM` | `MG`     | magnesium ion                                 | Mg                  |  24.305 |   A   |      301 |     1 |  1.0 |      20.19 |       N        |     0.981 | 0.034 |       1.00 |       0 | metal coord.             |
| `6OIM` | `GDP`    | "                                             | "                   | 443.201 |   A   |      302 |    28 |  1.0 |      20.23 |    Y (RCSB)    |     0.971 | 0.053 |       1.00 |       0 | metal coord.             |
| `6OIM` | `MOV`    | AMG 510 / sotorasib (bound form)              | C30 H32 F2 N6 O3    | 562.610 |   A   |      303 |    41 |  1.0 |      26.83 |    Y (RCSB)    |     0.908 | 0.084 |       1.00 |       2 | **HAS_COVALENT_LINKAGE** |
| `5MO4` | `NIL`    | nilotinib                                     | C28 H22 F3 N7 O     | 529.516 |   A   |      601 |    39 |  1.0 |      32.75 |    Y (RCSB)    |     0.967 | 0.061 |       1.00 |       1 | no covalent linkage      |
| `5MO4` | `AY7`    | asciminib                                     | C20 H18 Cl F2 N5 O3 | 449.838 |   A   |      602 |    31 |  1.0 |      36.19 |    Y (RCSB)    |     0.946 | 0.095 |       1.00 |       0 | no covalent linkage      |
| `9GZ2` | `MG`     | magnesium ion                                 | Mg                  |  24.305 |   A   |     1201 |     1 |  1.0 |      42.39 |       N        |         — |     — |       1.00 |       0 | metal coord.             |
| `9GZ2` | `ADP`    | "                                             | "                   | 427.201 |   A   |     1202 |    27 |  1.0 |      41.76 |     **N**      |         — |     — |       1.00 |       0 | metal coord.             |
| `9GZ2` | `PO4`    | "                                             | O4 P                |  94.971 |   A   |     1203 |     5 |  1.0 |      50.49 |       N        |         — |     — |       1.00 |       0 | metal coord.             |
| `9GZ2` | `XB2`    | **mavacamten**                                | C15 H19 N3 O2       | 273.330 |   A   |     1204 |    20 |  1.0 |   **0.00** | Y (**Author**) |         — |     — |       1.00 |       0 | no covalent linkage      |

Waters: `1OPL` 0, `2G2H` 413, `4LDJ` 250, `4OBE` 355, `5MO4` 307, `5TBY` 0, `6OIM` 207,
`9GZ2` 0, `9GZ3` 0.

**Occupancy is 1.0 on every non-polymer atom in all nine entries.** The only sub-unit
occupancy anywhere in the set is on the _polymer_: `5MO4` chain A **Met256**, which has
alternate conformers A and B. That is one two-conformer side chain, not a coverage problem.

Three things the density scores say that the frozen files do not:

- **`1OPL:B`'s `P16` is the worst-fitted ligand in the set** — RSCC 0.582, the only
  `IS_RSCC_OUTLIER` flag, five intermolecular clashes, and a group B of 152.41 against
  85.49 for the same compound in chain A.
- **`1OPL:A`'s `MYR` is incompletely modelled** — `completeness` 0.9375, the only value
  below 1.0 in the table. `MYR` is C14 H28 O2, sixteen heavy atoms; fifteen are deposited,
  and 15/16 = 0.9375.
- **`6OIM`'s `MOV` is genuinely covalent**: `_struct_conn` carries one `covale` record,
  `A/CYS12.SG — A/MOV303.C25` at **1.805 Å**, which is a plausible C–S bond. That is the
  bond `kras_g12c_mandated`'s apo (`4OBE`, wild-type Gly12) has no cysteine to make.

---

## 6. Dimension 3 — what is actually modelled, per chain

`polymer_entity_instance.rcsb_polymer_instance_feature[UNOBSERVED_RESIDUE_XYZ]` mapped
through `auth_to_entity_poly_seq_mapping`, cross-checked against distinct `ATOM` residue
numbers in the deposited file. CATH ranges are the per-instance assignment in author
numbering; `—` means CATH has not classified that chain.

| PDB    | chain | ent | modelled / deposited | gaps (auth)                          | modelled span (auth)     | CATH domains (auth)                                             |
| ------ | :---: | :-: | -------------------: | ------------------------------------ | ------------------------ | --------------------------------------------------------------- |
| `4OBE` |   A   |  1  |            169 / 170 | 0 (the auth-0 tag Gly)               | 1–169                    | 3.40.50.300 P-loop 1–169                                        |
| `4OBE` |   B   |  1  |            170 / 170 | none                                 | 0–169                    | 3.40.50.300 P-loop 0–169                                        |
| `4LDJ` |   A   |  1  |            170 / 170 | none                                 | 0–169                    | 3.40.50.300 P-loop 0–169                                        |
| `1OPL` |   A   |  1  |            451 / 537 | 1–80, 532–537                        | **81–531**, unbroken     | **SH3 83–145**, SH2 146–247, kinase N 259–344, kinase C 345–519 |
| `1OPL` | **B** |  1  |        **365 / 537** | **1–139**, **238–251**, 519–537      | 140–237, 252–518         | **no SH3**, SH2 140–252, kinase N 253–336, kinase C 337–518     |
| `2G2H` |   A   |  1  |            272 / 287 | 245–251, 524–531                     | 252–523                  | kinase N 252–336, kinase C 337–518                              |
| `2G2H` |   B   |  1  |            272 / 287 | 245–251, 524–531                     | 252–523                  | kinase N 252–336, kinase C 337–518                              |
| `5TBY` |   A   |  1  |       **954 / 1935** | 1–5, 960–1935                        | 6–959                    | **— (no CATH, no SCOP)**                                        |
| `5TBY` |   B   |  1  |           950 / 1935 | 1–9, 960–1935                        | 10–959                   | —                                                               |
| `5TBY` | C, D  |  2  |            152 / 195 | 1–43                                 | 44–195                   | —                                                               |
| `5TBY` | E, F  |  3  |            160 / 166 | 1–6                                  | 7–166                    | —                                                               |
| `9GZ3` |   A   |  1  |           764 / 1145 | 2, 203–213, 625–643, 797–1146        | 3–202, 214–624, 644–796  | —                                                               |
| `6OIM` |   A   |  1  |            167 / 183 | −13…−1, 105–107                      | 0–104, 108–169           | 3.40.50.300 P-loop 0–169                                        |
| `5MO4` |   A   |  1  |            429 / 495 | 40–82, 296–297, **402–419**, 532–534 | 83–295, 298–401, 420–531 | — (SCOP: 83–139 SH3, 140–240 SH2, 241–531 kinase)               |
| `9GZ2` |   A   |  1  |           764 / 1145 | 2, 203–213, 625–643, 797–1146        | 3–202, 214–624, 644–796  | —                                                               |

`9GZ2` and `9GZ3` are residue-identical: same 764 modelled, same four gaps, same span. That
is what makes `cardiac_myosin_corrected` the cleanest pair in the benchmark.

`5MO4`'s 18-residue hole at 402–419 is confirmed again from both routes. It is the holo of
**both** BCR-ABL1 arms; the three label residues the mandated arm reports as `unmapped`
(`A:ILE521`, `A:VAL525`, `A:LEU529`) are lost on the _apo_ side, because `1OPL:B` stops at
518 — not on the holo side.

**No CATH or SCOP classification exists for `5TBY` or for `9GZ2`/`9GZ3`.** For the two 2024
myosin entries that is age. For `5TBY`, released 2017 and at version 1-9, it is not.

---

## 7. Dimension 3 (cont.) — asymmetric unit against biological assembly

`rcsb_entry_info.deposited_*` for the asymmetric unit; `assembly/<id>` →
`pdbx_struct_assembly` + `rcsb_struct_symmetry` for each assembly RCSB serves.

| PDB    | AU: polymer chains / non-polymer / atoms | assemblies | assembly definitions                                                                      | what the frozen arm takes              |
| ------ | ---------------------------------------- | :--------: | ----------------------------------------------------------------------------------------- | -------------------------------------- |
| `4OBE` | 2 / 4 / 3093                             |     2      | 1 monomeric A1 (PISA), 2 monomeric A1 (PISA)                                              | chain A, 1 copy — matches              |
| `4LDJ` | 1 / 2 / 1636                             |     1      | 1 monomeric A1 (PISA)                                                                     | chain A, 1 copy — matches              |
| `1OPL` | 2 / 3 / 6655                             |   **3**    | 1 monomeric = **chain A** + `MYR` + `P16` (author); 2 monomeric = **chain B** + `P16` (author+PISA); 3 **dimeric A2** = chain A doubled by crystal symmetry (software-defined, PISA) | chain B, 1 copy = **assembly 2**       |
| `2G2H` | 2 / 2 / 4889                             |     2      | 1 monomeric A1 (author), 2 monomeric A1 (author)                                          | chain A, 1 copy — matches              |
| `5TBY` | **6 / 0 / 20357**                        |     1      | 1 **hexameric**, author-defined, symmetry A2 B2 C2                                        | chain A, **2 entity copies deposited** |
| `9GZ3` | 1 / 3 / 6180                             |     1      | 1 monomeric A1                                                                            | chain A, 1 copy — matches              |
| `6OIM` | 1 / 3 / 1613                             |     1      | 1 monomeric A1 (PISA)                                                                     | chain A, 1 copy — matches              |
| `5MO4` | 1 / 2 / 3770                             |     1      | 1 monomeric A1 (PISA)                                                                     | chain A, 1 copy — matches              |
| `9GZ2` | 1 / 4 / 6200                             |     1      | 1 monomeric A1                                                                            | chain A, 1 copy — matches              |

Two entries where the asymmetric unit and the biological assembly are not the same object:

- **`1OPL`.** The AU holds two chains, and RCSB serves three assemblies built from them.
  Assembly 1 is chain A with both its ligands (451 modelled residues). Assembly 2 is chain B
  with `P16` alone (365 modelled residues, `polymer_atom_count` 2954) — that is exactly the
  frozen input. Assembly 3 is **chain A doubled by crystal symmetry**, `A2`, 902 modelled
  residues, generated from asym ids `A, C, D` twice; chain B is not in it. So the entry does
  not answer "what is the biological unit" with one number, and the arm's selection
  corresponds to assembly 2, not to assembly 1.
- **`5TBY`.** The AU is the whole interacting-heads motif — six chains, three entities, one
  hexameric assembly with two copies of the heavy chain. `frozen.json` records
  `assembly_agreement.selected_target_copies_match = false` and
  `polymer_composition_matches = false` against `9GZ2`'s monomer. That is 6 against 1, and
  the freeze already declares it rather than repairing it.

---

## 8. Dimension 4 — `1OPL` chain A against chain B, and the four claims

The repository asserts four things about chain B: it lacks myristate, it retains the
ATP-site inhibitor, it models no SH3 domain, and it carries only three group B-factors.
**All four are confirmed.**

|                                                  | chain A                                                  | chain B                                         |
| ------------------------------------------------ | -------------------------------------------------------- | ----------------------------------------------- |
| non-polymer contents                             | `MYR` 538, `P16` 539                                     | **`P16` 538 only**                              |
| modelled polymer residues                        | 451 / 537                                                | **365 / 537**                                   |
| modelled span (auth)                             | 81–531, unbroken                                         | 140–237 + 252–518                               |
| unmodelled (auth)                                | 1–80, 532–537                                            | 1–139, 238–251, 519–537                         |
| CATH domains                                     | **SH3** 83–145, SH2 146–247, kinase 259–344 + 345–519    | SH2 140–252, kinase 253–336 + 337–518           |
| SCOP domains                                     | d1opla1 **SH3 81–139**, d1opla2 140–240, d1opla3 241–531 | d1oplb1 140–237, d1oplb2 252–518                |
| ECOD domains                                     | 3 (83–139, 141–238, 247–520)                             | 2 (141–237, 252–518)                            |
| distinct `_atom_site.B_iso_or_equiv` over `ATOM` | **3041**                                                 | **3**                                           |
| the three values                                 | —                                                        | 160.84 (1455 atoms), 198.13 (776), 161.17 (723) |
| `P16` RSCC / RSR                                 | 0.842 / 0.182                                            | **0.582** / 0.197                               |
| `P16` intermolecular clashes                     | 2                                                        | 5                                               |
| `P16` group B                                    | 85.49                                                    | 152.41                                          |
| `P16` validation flags                           | no covalent linkage                                      | no covalent linkage, **IS_RSCC_OUTLIER**        |

**Claim 1 — chain B lacks myristate. CONFIRMED.** Three independent reads agree:
`nonpolymer_entity/1OPL/2` gives `MYR` an `auth_asym_ids` of `["A"]`; the deposited file has
exactly one `MYR` residue group, 15 atoms, on chain A at auth 538; and the validation report
has one `ModelledSubgroup` with `resname="MYR"`, on `chain="A" resnum="538"`.

**Claim 2 — chain B retains the ATP-site inhibitor. CONFIRMED.** `nonpolymer_entity/1OPL/3`
gives `P16` `auth_asym_ids` `["A","B"]`; the file has two `P16` groups of 29 atoms each, at
`A/539` and `B/538`. Ligand stripping is therefore load-bearing for this arm, and
`frozen.json` records the consequence: chain B's nearest ligand heavy atom is **16.0 Å**
from the label set and contacts none of it.

**Claim 3 — chain B models no SH3 domain. CONFIRMED, by three classifications
independently.** CATH assigns `2.30.30.40 SH3 Domains` to chain A at auth 83–145 and assigns
nothing of the kind to chain B. SCOP assigns `d1opla1 "Abl tyrosine kinase, SH3 domain"` at
81–139 to chain A and gives chain B only two domains, neither an SH3. ECOD gives chain A
three domains and chain B two. The geometric reason is in the coverage: chain B's first
modelled residue is **140**, and the SH3 domain ends at 139/145.

**Claim 4 — chain B carries only three group B-factors. CONFIRMED, exactly.** Counting
distinct `_atom_site.B_iso_or_equiv` strings over `ATOM` records: chain A 3041, chain B
**3**. The depositors say why, in `_refine.details`: _"only overall domain B-factors were
applied to molecule B, whereas individual B-factors were refined for molecule A."_ Three
values for three rigid-body domains. The values themselves — 160.84, 198.13, 161.17 — are
far above the entry's own mean of 123.3 and above every atom in chain A except the tail.

**What that means for C6.** Chain B is not an independently refined copy. Its coordinates
are `1OPK`'s refined high-resolution geometry, rigid-body-placed into a 3.42 Å molecular
replacement solution, with one B per domain. A residue contact graph over chain B is
therefore a property of `1OPK`'s internal geometry plus three rigid placements — and the
elastic network hypothesis (C6) makes that contact graph the object the whole method rests
on. The repository already states this in `manifest.yaml`; the primary data confirms every
element of it.

**One cost the organisers' reply does not mention.** Chain B models 86 fewer residues than
chain A: 59 at the N-terminus (81–139, the SH3 domain), 14 in an internal break at 238–251,
and 13 more at the C-terminus. It is also the noisier copy — its `P16` is the only
`IS_RSCC_OUTLIER` in the nine entries.

---

## 9. Dimension 5 — `5TBY`, everything measurable

| field                                 | value                                                                                                                                                                                                                                                                                       | source                                          |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------- |
| title                                 | HUMAN BETA CARDIAC HEAVY MEROMYOSIN INTERACTING-HEADS MOTIF OBTAINED BY HOMOLOGY MODELING (**USING SWISS-MODEL**) OF HUMAN SEQUENCE FROM APHONOPELMA HOMOLOGY MODEL (**PDB-3JBH**), RIGIDLY FITTED TO HUMAN BETA-CARDIAC NEGATIVELY STAINED THICK FILAMENT 3D-RECONSTRUCTION (**EMD-2240**) | `struct.title`                                  |
| method                                | EM / ELECTRON MICROSCOPY                                                                                                                                                                                                                                                                    | `rcsb_entry_info.experimental_method`           |
| `structure_determination_methodology` | **experimental**                                                                                                                                                                                                                                                                            | `rcsb_entry_info`                               |
| resolution field                      | **20.0 Å**                                                                                                                                                                                                                                                                                  | `rcsb_entry_info.resolution_combined[0]`        |
| map resolution / criterion            | 20.0 Å, **FSC 0.5 CUT-OFF**                                                                                                                                                                                                                                                                 | `em_3d_reconstruction[0]`                       |
| EMDB                                  | EMD-2240                                                                                                                                                                                                                                                                                    | `rcsb_entry_container_identifiers.emdb_ids`     |
| particles                             | 10 700                                                                                                                                                                                                                                                                                      | `em_3d_reconstruction[0].num_particles`         |
| fit protocol / criterion              | **RIGID BODY FIT** / CORRELATION COEFFICIENT                                                                                                                                                                                                                                                | `em_3d_fitting[0]`                              |
| template                              | **`3JBH`**, six rows, `type = "experimental model"`, ranges 1–962 (A,B), 1–156 (C,D), 1–196 (E,F)                                                                                                                                                                                           | `_em_3d_fitting_list`                           |
| initial refinement model              | `3JBH`                                                                                                                                                                                                                                                                                      | `_pdbx_initial_refinement_model.accession_code` |
| related entries                       | EMD-1950 (tarantula cryo-EM), `3jBH`, EMD-2240 (human heart, negative stain)                                                                                                                                                                                                                | `_pdbx_database_related`                        |
| model-fitting software                | UCSF Chimera                                                                                                                                                                                                                                                                                | `_em_software[MODEL FITTING]`                   |
| model-refinement software             | **`?` — the row exists and names no program**                                                                                                                                                                                                                                               | `_em_software[MODEL REFINEMENT]`                |
| `refine` category                     | present, three non-null values: `entry_id`, `pdbx_refine_id = ELECTRON MICROSCOPY`, `ls_d_res_high = 20.00`                                                                                                                                                                                 | `_refine`                                       |
| **heteroatom count**                  | **0** — no ligand, no ion, no water                                                                                                                                                                                                                                                         | `_atom_site` `HETATM` rows                      |
| entities / chains                     | 3 polymer, 0 non-polymer, 0 branched / 6 chains                                                                                                                                                                                                                                             | `rcsb_entry_info`                               |
| assembly 1                            | hexameric, A2 B2 C2, author-defined                                                                                                                                                                                                                                                         | `assembly/5TBY/1`                               |
| deposited atoms                       | 20 357                                                                                                                                                                                                                                                                                      | `rcsb_entry_info.deposited_atom_count`          |
| **B-factor range**                    | **0.00 – 7.30 Å², mean 2.45** (chain A 0.00–6.25, 359 distinct values over 954 residues)                                                                                                                                                                                                    | `_atom_site.B_iso_or_equiv`                     |
| clashscore                            | **51.30**, absolute percentile **1.7**                                                                                                                                                                                                                                                      | validation `<Entry clashscore>`                 |
| Ramachandran outliers                 | **5.96 %**, absolute percentile **2.0**                                                                                                                                                                                                                                                     | `percent-rama-outliers`                         |
| sidechain outliers                    | 1.96 %, absolute percentile 47.7                                                                                                                                                                                                                                                            | `percent-rota-outliers`                         |
| RSRZ                                  | — (`percentilebins = "all,em"`, no EDS)                                                                                                                                                                                                                                                     | validation report                               |
| CATH / SCOP classification            | **none**                                                                                                                                                                                                                                                                                    | `rcsb_polymer_instance_annotation`              |
| `_struct_conn`                        | **41 `covale`**, 1.083–1.644 Å, mean 1.422 Å, across six chain pairs: A–B ×9, A–E ×9, B–D ×9, B–F ×7, A–C ×5, A–F ×2                                                                                                                                                                        | `_struct_conn`                                  |
| specimen                              | _"A 6 ul aliquot of native purified **tarantula** thick filaments suspension (Hidalgo et al. 2001)."_, `staining_applied = NO`, `vitrification_applied = YES`                                                                                                                               | `_em_specimen`                                  |

**Is it a SWISS-MODEL homology model?** The entry says so, in its own title, and names its
template: `3JBH`. `_em_3d_fitting_list` and `_pdbx_initial_refinement_model` name `3JBH`
independently of the title, six times, once per chain. `3JBH` is itself a _tarantula_
(Aphonopelma) model, so the template chain is: tarantula model → human homology model →
rigid fit into a human negative-stain envelope. Every step of that chain is recorded in a
deposited field.

**What a 20 Å resolution field means for a deposited model.** It is the resolution of the
map the model was _placed into_, reported at `FSC 0.5` — an older and more permissive
criterion than the `FSC 0.143` the two 2024 myosin entries use. At 20 Å a density envelope
constrains the position and orientation of a rigid body; it does not constrain a side chain,
a backbone torsion, or an interatomic contact. The 41 `covale` records are the direct
consequence: they are the annotation pipeline reading pairs of atoms that overlap at
1.08–1.64 Å because two rigid bodies were docked into one envelope and never refined apart.
`A/GLN454.CG — B/TYR410.CE2` at **1.083 Å** is shorter than any real covalent bond.

**Is the entry experimental at all?** RCSB says `structure_determination_methodology =
experimental`, and `5TBY` is a released PDB entry at version 1-9 with ten audit revisions
and a released map. **Do not claim it is not experimental** — that claim is refutable from
one field. Argue instead from what is measurable and not in dispute: 20 Å, `FSC 0.5`, a
rigid-body fit, no model-refinement program, a `refine` block with nothing in it, 41
impossible covalent bonds, a clashscore at the 1.7th percentile of the entire PDB, no CATH
or SCOP classification, and — new here — **a B-factor column running 0.00–7.30 Å²**, which
cannot be a refined isotropic displacement parameter for a 20 Å model and which nothing in
the entry claims to have refined.

**Heteroatom count is zero**, which is why `cardiac_myosin_mandated`'s active site must be
found by sequence motif (`from_motifs: [MYO_PLOOP, MYO_SWITCH1, MYO_SWITCH2]`) rather than
by cofactor contact: there is no cofactor in the file to contact.

---

## 10. Verdict — is each frozen arm's physical evidence sufficient?

One row per arm. "Apo input" asks whether the apo entry can carry a residue contact graph
that means something under C6. "Holo validation" asks whether the holo entry can define a
label set. The deciding measurement is named; everything else is context.

| arm                        | apo input?                                       | deciding measurement                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | holo validation?                   | deciding measurement                                                                                                                                                                                                                                                                                                                                                                                  |
| -------------------------- | ------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `kras_g12c_mandated`       | **Yes**                                          | `4OBE` 1.24 Å X-ray, clashscore 1.11 (95.7th), 0 % Rama and 0 % sidechain outliers; the arm's chain A models 169 of 170 with **no internal gap** — the one absent residue is the auth-0 expression-tag glycine. Its own `GDP`·`MG` is 4.57 Å from the nearest **scoreable** label and contacts none of the 16, so the source-set cofactor does not sit on what is scored.                                                                                                                                                                                                                                               | **Yes, with one disclosed defect** | `6OIM` 1.65 Å, `MOV` RSCC 0.908 / RSR 0.084, and one `covale` `A/CYS12.SG — MOV.C25` at 1.805 Å. The defect is that the bond needs a Cys12 the wild-type apo does not have: `sequence_agreement.differences_in_label_set = ["GLY12→CYS"]`, 1 residue of 21.                                                                                                                                           |
| `kras_g12c_corrected`      | **Yes**                                          | `4LDJ` 1.15 Å, the best-validated entry in the set — clashscore 1.10 (95.7th), and **0 %** on Ramachandran, sidechain and RSRZ outliers, all three at the 100th absolute percentile. 170/170 modelled, no gap, and `seq_dif` confirms the G12C the mandated apo lacks.                                                                                                                                                                                                                                                                                            | **Yes**                            | Same `6OIM`, and now `differences_in_label_set` is empty.                                                                                                                                                                                                                                                                                                                                             |
| `bcr_abl1_mandated`        | **Reportable, never confirmatory**               | `1OPL:B` carries **three distinct B-factors over its 2 954 polymer atoms** (160.84 / 198.13 / 161.17), because `_refine.details` says only overall domain B-factors were applied to molecule B. Its coordinates are `1OPK` rigid-body-placed at 3.42 Å with 89.01 % data completeness — the lowest in the set. Under C6 the contact graph is the method's object, and this graph was never independently refined. Compounding: 365/537 modelled, no SH3 domain in CATH, SCOP or ECOD, and `apo_holo_rmsd.core = 22.79 Å` over 328 Cα. | **Yes**                            | `5MO4` 2.17 Å, `AY7` (asciminib) RSCC 0.946 / RSR 0.095, 0 clashes, occupancy 1.0, footprint of 20 residues frozen in `label_footprints`. The one caveat is coverage, not quality: an 18-residue unmodelled block at 402–419.                                                                                                                                                                         |
| `bcr_abl1_corrected`       | **Yes, with a stated caveat**                    | `2G2H:A` 2.00 Å, 272 of 287 modelled over an unbroken span 252–523, per-atom B-factors (1471 distinct values), and its `P16` measured 16.27 Å from the label set contacting none of it — the pocket is genuinely empty. The caveat is **RSRZ 13.42 % at the 6.8th absolute percentile**, the worst electron-density fit of the six X-ray entries; and the chain carries the engineered activating mutation at auth 415 (PRO←HIS).                                                                                                | **Yes**                            | Same `5MO4`.                                                                                                                                                                                                                                                                                                                                                                                          |
| `cardiac_myosin_mandated`  | **No — reportable only, and never confirmatory** | `5TBY` is a **rigid-body fit of a homology model into a 20 Å FSC-0.5 envelope with no model-refinement program, no refinement statistics, 41 `covale` records at 1.083–1.644 Å, a clashscore at the 1.7th percentile, and a B-factor column running 0.00–7.30 Å².** Zero heteroatoms, no CATH or SCOP classification. The single decisive number is the 41 impossible bonds: a contact graph is a statement about which residues touch, and this file records 41 pairs touching at distances no chemistry allows.                 | **Yes, with one new caveat**       | `9GZ2` 2.9 Å cryo-EM at FSC 0.143, clashscore 1.78 (89.2nd), 0 % Rama outliers, flexible fit with PHENIX refinement. New caveat: **`XB2` carries B = 0.00 on all 20 atoms** while `ADP`/`PO4`/`MG` in the same file sit at 41.76 / 50.49 / 42.39. Cryo-EM entries have no RSCC, so the B-factor column is the only per-ligand quality signal available and it is unset for the label-defining ligand. |
| `cardiac_myosin_corrected` | **Yes**                                          | `9GZ3` 3.4 Å cryo-EM at FSC 0.143, clashscore 1.54 (91.8th), 0.26 % Rama, flexible fit refined in PHENIX, and **residue-identical to its holo**: both model 764/1145 with the same four gaps (2, 203–213, 625–643, 797–1146). `sequence_agreement.identity = 1.0` over 764. Its `ADP`·`MG`·`PO4` is 20.52 Å from the nearest label and contacts none of the 12.                                                                                                                                                                   | **Yes, same caveat**               | Same `9GZ2`, and here the pair is state-matched: both hold Mg·ADP·Pi, `apo_holo_rmsd.pocket_lining = 1.10 Å`, `pocket_max = 1.9 Å`. The `XB2` B = 0.00 caveat applies to both myosin arms because both take their labels from `9GZ2:A:XB2`.                                                                                                                                                           |

**Summary of the six.** Four arms are supported end to end on physical evidence: both KRAS
arms, `bcr_abl1_corrected`, and `cardiac_myosin_corrected`. Two are not, for reasons on the
**input** side only, and both are already marked non-confirmatory in `manifest.yaml`:
`bcr_abl1_mandated`, whose apo chain was never independently refined, and
`cardiac_myosin_mandated`, whose apo is a rigid-body-fitted homology model. Every holo in
the set is usable; the only holo-side finding is `9GZ2`'s zero-B mavacamten, which is a
disclosure item rather than a disqualification, since the ligand's _position_ — which is
what the label footprint uses — is fixed by the flexible fit and the coordinates are
present.

---

## 11. Corrections and cautions this pass adds

Corrections live here, not edited into the freezes (`review/README.md`).

**C1 — `08-structure-evidence.md` reproduces exactly for these nine entries.** 175 paired
values, 0 differences. Nothing in `08`'s Tables A–F needs revising for `1OPL`, `2G2H`,
`4LDJ`, `4OBE`, `5MO4`, `5TBY`, `6OIM`, `9GZ2` or `9GZ3`. Its five discrepancies (D1–D5)
against `docs/targets.md` and `docs/benchmark/primary/README.md` are untouched by this pass
and still stand.

**C2 — `08` reported only assembly 1 for each entry.** `1OPL` has **three**, `4OBE` and
`2G2H` have two each, and `1OPL`'s assembly 3 is a **dimer** of chain A. Where the
repository writes "the biological assembly of `1OPL`", it should name which one: the frozen
input chain B is assembly **2**.

**C3 — RCSB's `pdbx_mutation` for `1OPL` says `E29D`; the deposited file says `E30D`.**
`manifest.yaml` is right and RCSB's free-text field is wrong. Do not import that string.

**C4 — do not quote an ECOD name.** `e1oplA3` was `LRR_6,LRR_RI_capping` in the 2026-08
cache and is `Hexapep,Acetyltransf_11` today, for the same ABL1 kinase domain. `5TBY`'s
myosin chains are called `Med6` and `LpxC`. The ranges are stable; the names are auto-derived
and are not domain identities.

**C5 — the revision count is ambiguous for `9GZ2` and `9GZ3`.** REST says 2 and 1; the
deposited file and the validation report say 11 and 9. State which artifact a count comes
from.

**C6 — one number to check, not a refutation.** `manifest.yaml`'s `bcr_abl1_mandated` defect
text says the Cα RMSD to `5MO4:A` is **22.89 Å** "over all common residues".
`frozen.json` records `apo_holo_rmsd.core = 22.79` over `n_core = 328`. The two may be over
different residue subsets — "all common" against "core" — but the prose does not say so, and
the numbers should be reconciled or the subsets named. Not checked here; this pass did no
superposition.

**C7 — the `9GZ2` `XB2` zero-B finding is new and belongs in the myosin defect text.** Both
cardiac-myosin arms take their 12 labels from `9GZ2:A:XB2`. The ligand's atoms carry
`B_iso_or_equiv = 0.00` while every other group in the file carries a refined value. Cryo-EM
entries have no RSCC or RSR, so no independent per-ligand quality number exists to set
against it.
