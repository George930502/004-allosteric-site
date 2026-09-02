# 08 — Structure evidence for every benchmark accession, from live RCSB

**Fetched:** 2026-09-02, from `data.rcsb.org/rest/v1/core` and the
wwPDB validation reports served at `files.rcsb.org/pub/pdb/validation_reports/`.
**Raw responses:** `data/rcsb-raw/<PDB_ID>/`, one directory per entry.
**Machine-readable table:** `data/structure-evidence.json`.
**Re-run:** `python3 docs/benchmark/review/data/fetch_structure_evidence.py` — it reuses
anything already cached, so the JSON is re-derivable offline once `rcsb-raw/` exists.

Every number below is read from an API field or a validation-report attribute, named in
place. Where RCSB carries no value the cell is `—` and the JSON holds `null`. Nothing here
is filled in from a paper or from memory.

**Scope.** 33 distinct accessions, in five groups: 6 primary apo, 4 primary holo, 5 named by
the organisers as myosin alternatives, 9 secondary apo, 9 secondary holo. Two more —
`8QYP` and `9YRG` — are fetched and tabulated as *supporting* rows, because question (b)
asks whether each mavacamten holo has a matched apo in its own deposition series and those
two are the only candidates. They are excluded from every count over "the 33".

---

## 0. Headline

Nine findings that change what the repository can claim.

1. **`1OPL` chain B lacks myristate and keeps the ATP-site inhibitor — the organisers are right, and the cost is 86 residues.**
   Chain A models 451 of 537 residues with `MYR` 538 and `P16` 539; chain B models 365 with `P16` 538 and no `MYR`. Chain B additionally loses the 59 residues chain A models at auth 81–139, the 14 at 238–251, and 13 more at the C-terminus. Its `P16` copy is an RSCC outlier at 0.582 against 0.842 in chain A.

2. **`5TBY` is a 20 Å rigid-body fit with 41 impossible covalent bonds and no refinement statistics.**
   `resolution_combined` 20.0 Å at `FSC 0.5 CUT-OFF`; the `refine` category exists in the mmCIF but every value except `entry_id`, `pdbx_refine_id` and `ls_d_res_high` is `?`; 41 `struct_conn` rows of type `covale` span 1.083–1.644 Å, mean 1.422 Å; clashscore 51.3 at the 1.7th absolute percentile.

3. **`6C1H` is rabbit actin plus rat myosin-Ib plus calmodulin, with ADP and Mg and nothing else.**
   Five chains of `P68135` (*Oryctolagus cuniculus*), one chain `P` of `Q05096` (*Rattus norvegicus*), one chain `R` of `P0DP23`. No `P12883`. No `XB2`.

4. **`9GZ2` is the right mavacamten holo, and `9GZ3` is a residue-for-residue matched apo.**
   Both are one chain of `P12883`, both model 764 of 1145 residues, both carry the identical gap set (2, 203–213, 625–643, 797–1146), both were deposited 2024-10-03, both hold Mg·ADP·PO4. They differ by `XB2` and nothing else. No other mavacamten entry has a counterpart this close.

5. **Three of the 33 entries fail a rule of X-ray ≤ 2.5 Å or cryo-EM ≤ 4.0 Å: `1OPL`, `5TBY`, `8QYQ`.**
   3.42 Å X-ray, 20.0 Å EM and 2.61 Å X-ray respectively. Everything else passes, `1QUV` exactly at 2.50 Å.

6. **Four X-ray entries have no released structure factors, so they carry no RSRZ and no ligand density score.**
   `1IA8`, `1RTJ`, `1A9X`, `1VRT` all report `rcsb_accession_info.has_released_experimental_data = "N"`. That removes electron-density validation from both halves of the `hiv_rt` arm and from the apo of `chk1` and `ecoli_cps`.

7. **The repository's `1OPL` RSRZ number disagrees with the validation report RCSB serves today.**
   `docs/targets.md` records 22.18 % RSRZ outliers at the 0.4th absolute percentile and calls a prior correction to 6.50 % "itself the error". The wwPDB report at RCSB, created 2026-03-20 against revision 5, gives `percent-RSRZ-outliers="6.50"` and `absolute-percentile-percent-RSRZ-outliers="24.6"`. The PDBe percentile endpoint the repo cited still returns 22.18/0.4 — the two wwPDB partners are serving different runs.

8. **`5TBY`'s clashscore in the repository is stale.**
   `docs/targets.md` says 49.95 at the 2.2nd percentile. The report created 2026-03-09 says `clashscore="51.3"`, absolute percentile 1.7, relative 1.7.

9. **The secondary set's space-group claim does not hold.**
   `docs/benchmark/primary/README.md` line 307 says the six arms under 0.3 Å "share a space group in five of six". Live: `chk1`, `ptp1b` and `hiv_rt` share one, `mkp5` (`P 1` → `P 64`) and `ns5b` (`P 43 21 2` → `P 21 21 2`) do not, and `p97_vcp` is cryo-EM with no space group at all.

---

## 1. Table A — experiment, resolution, refinement, cell

`rcsb_entry_info.experimental_method`, `rcsb_entry_info.resolution_combined[0]`,
`refine[0].ls_R_factor_R_work` / `.ls_R_factor_R_free`, `symmetry.space_group_name_H_M`,
`cell.length_*` and `cell.angle_*`, `rcsb_accession_info.has_released_experimental_data`.
Angles are shown only when they are not 90/90/90.

| PDB | set | method | res (Å) | R-work | R-free | space group | unit cell a × b × c (Å) | exp. data released |
| --- | --- | --- | ---: | ---: | ---: | --- | --- | :-: |
| `4OBE` | primary apo | X-ray | 1.24 | 0.1566 | 0.1686 | C 1 2 1 | 66.147 × 42.096 × 114.393 (90, 105.32, 90) | Y |
| `4LDJ` | primary apo | X-ray | 1.15 | 0.1318 | 0.1622 | P 21 21 21 | 39.071 × 40.724 × 91.431 | Y |
| `1OPL` | primary apo | X-ray | 3.42 | 0.306 | 0.315 | C 2 2 21 | 77.017 × 273.384 × 124.384 | Y |
| `2G2H` | primary apo | X-ray | 2.0 | 0.193 | 0.213 | P 21 21 2 | 104.386 × 131.487 × 56.499 | Y |
| `5TBY` | primary apo | EM | 20.0 | — | — | — | — | Y |
| `9GZ3` | primary apo | EM | 3.4 | — | — | — | — | Y |
| `6OIM` | primary holo | X-ray | 1.65 | 0.18092 | 0.21519 | P 21 21 21 | 40.868 × 58.417 × 65.884 | Y |
| `5MO4` | primary holo | X-ray | 2.17 | 0.1818 | 0.217 | C 2 2 21 | 118.28 × 124.13 × 74.66 | Y |
| `6C1H` | primary holo | EM | 3.9 | — | — | — | — | Y |
| `9GZ2` | primary holo | EM | 2.9 | — | — | — | — | Y |
| `8QYR` | myosin alt. | X-ray | 1.8 | 0.187 | 0.227 | P 21 21 21 | 68.58 × 95.68 × 127.14 | Y |
| `9GZ1` | myosin alt. | EM | 3.7 | — | — | — | — | Y |
| `8QYQ` | myosin alt. | X-ray | 2.61 | 0.178 | 0.217 | P 1 21 1 | 102.801 × 147.977 × 116.751 (90, 91.62, 90) | Y |
| `9YP9` | myosin alt. | EM | 3.0 | — | — | — | — | Y |
| `9YR7` | myosin alt. | EM | 3.0 | — | — | — | — | Y |
| `1ZZW` | secondary apo | X-ray | 1.6 | 0.193 | 0.217 | P 1 | 39.533 × 41.073 × 55.569 (95.35, 99.81, 117.35) | Y |
| `1IA8` | secondary apo | X-ray | 1.7 | 0.216 | 0.235 | P 1 21 1 | 45.2 × 65.7 × 58.1 (90, 93.9, 90) | N |
| `1SUG` | secondary apo | X-ray | 1.95 | 0.188 | 0.203 | P 31 2 1 | 88.118 × 88.118 × 103.9 (90, 90, 120) | Y |
| `6P7Z` | secondary apo | X-ray | 1.19 | 0.1809 | 0.1981 | P 21 21 21 | 61.14 × 66.179 × 107.33 | Y |
| `3IDH` | secondary apo | X-ray | 2.14 | 0.18886 | 0.2201 | P 21 21 21 | 65.51 × 81.97 × 86.95 | Y |
| `1RTJ` | secondary apo | X-ray | 2.35 | 0.219 | — | P 21 21 21 | 137.5 × 109.4 × 72.3 | N |
| `1QUV` | secondary apo | X-ray | 2.5 | 0.223 | 0.316 | P 43 21 2 | 63.65 × 63.65 × 262.9 | Y |
| `5FTK` | secondary apo | EM | 2.4 | — | — | — | — | Y |
| `1A9X` | secondary apo | X-ray | 1.8 | — | — | P 21 21 21 | 152.1 × 164.4 × 332.3 | N |
| `7UMV` | secondary holo | X-ray | 1.8 | 0.1543 | 0.172 | P 64 | 76.962 × 76.962 × 89.238 (90, 90, 120) | Y |
| `3JVR` | secondary holo | X-ray | 1.76 | 0.202 | 0.225 | P 1 21 1 | 44.763 × 65.362 × 57.916 (90, 93.67, 90) | Y |
| `1T48` | secondary holo | X-ray | 2.2 | 0.21109 | 0.25451 | P 31 2 1 | 88.941 × 88.941 × 104.837 (90, 90, 120) | Y |
| `7BJ1` | secondary holo | X-ray | 1.61 | 0.1715 | 0.21 | P 21 21 21 | 60.909 × 66.05 × 107.277 | Y |
| `3F9M` | secondary holo | X-ray | 1.5 | 0.18969 | 0.22213 | P 21 21 21 | 65.7 × 81.2 × 85.6 | Y |
| `1VRT` | secondary holo | X-ray | 2.2 | 0.186 | — | P 21 21 21 | 141.8 × 116.7 × 66.4 | N |
| `2BRK` | secondary holo | X-ray | 2.3 | 0.184 | 0.245 | P 21 21 2 | 68.002 × 94.488 × 95.73 | Y |
| `5FTJ` | secondary holo | EM | 2.3 | — | — | — | — | Y |
| `1T36` | secondary holo | X-ray | 2.1 | 0.176 | 0.209 | P 21 21 21 | 152.5 × 164.9 × 333.1 | Y |
| `8QYP` | supporting | X-ray | 2.759 | 0.1897 | 0.2478 | P 43 2 2 | 94.397 × 94.397 × 219.693 | Y |
| `9YRG` | supporting | EM | 3.2 | — | — | — | — | Y |

`has_released_experimental_data` means structure factors for an X-ray entry and a map for a
cryo-EM one; it is `Y` on every cryo-EM entry here and `N` on four X-ray entries.

`1A9X`, `1RTJ` and `1VRT` carry an R-work in `refine` but no R-free. `5TBY`, `9GZ3`, `6C1H`,
`9GZ2`, `9GZ1`, `9YP9`, `9YR7`, `5FTK`, `5FTJ` and `9YRG` are cryo-EM and have no `refine`
R-factors at all. For `5TBY` the `refine` category is present in the deposited mmCIF but every
value except `entry_id`, `pdbx_refine_id` and `ls_d_res_high` is `?`.

## 2. Table B — dates and wwPDB version

`rcsb_accession_info.deposit_date`, `.initial_release_date`, `.revision_date`,
`.major_revision`-`.minor_revision`, and the length of `pdbx_audit_revision_history`.

| PDB | deposited | released | latest revision | version | revisions |
| --- | --- | --- | --- | :-: | ---: |
| `4OBE` | 2014-01-07 | 2014-06-04 | 2023-09-20 | 1-2 | 3 |
| `4LDJ` | 2013-06-24 | 2014-06-04 | 2023-09-20 | 1-3 | 4 |
| `1OPL` | 2003-03-06 | 2003-04-08 | 2023-08-16 | 1-4 | 5 |
| `2G2H` | 2006-02-16 | 2006-05-23 | 2023-08-30 | 1-4 | 5 |
| `5TBY` | 2016-09-13 | 2017-06-07 | 2024-10-23 | 1-9 | 10 |
| `9GZ3` | 2024-10-03 | 2025-03-12 | 2025-03-12 | 1-0 | 1 |
| `6OIM` | 2019-04-09 | 2019-11-06 | 2024-11-13 | 1-4 | 5 |
| `5MO4` | 2016-12-13 | 2017-04-05 | 2024-05-08 | 1-2 | 3 |
| `6C1H` | 2018-01-04 | 2018-01-31 | 2025-05-28 | 1-5 | 6 |
| `9GZ2` | 2024-10-03 | 2025-03-12 | 2025-11-12 | 1-1 | 2 |
| `8QYR` | 2023-10-26 | 2023-12-13 | 2025-11-12 | 1-1 | 2 |
| `9GZ1` | 2024-10-03 | 2025-03-12 | 2025-11-12 | 1-1 | 2 |
| `8QYQ` | 2023-10-26 | 2023-12-13 | 2025-11-12 | 1-1 | 2 |
| `9YP9` | 2025-10-13 | 2026-04-08 | 2026-05-20 | 1-1 | 2 |
| `9YR7` | 2025-10-16 | 2026-04-08 | 2026-05-20 | 1-1 | 2 |
| `1ZZW` | 2005-06-14 | 2006-07-04 | 2024-03-13 | 1-3 | 4 |
| `1IA8` | 2001-03-22 | 2001-04-18 | 2024-04-03 | 1-5 | 6 |
| `1SUG` | 2004-03-26 | 2004-09-07 | 2023-08-23 | 1-3 | 4 |
| `6P7Z` | 2019-06-06 | 2020-01-15 | 2024-03-13 | 1-2 | 3 |
| `3IDH` | 2009-07-21 | 2010-07-28 | 2023-11-01 | 1-5 | 6 |
| `1RTJ` | 1995-05-03 | 1996-04-03 | 2024-10-23 | 1-4 | 5 |
| `1QUV` | 1999-07-04 | 1999-11-05 | 2024-02-14 | 1-4 | 5 |
| `5FTK` | 2016-01-14 | 2016-01-27 | 2024-05-08 | 1-4 | 5 |
| `1A9X` | 1998-04-14 | 1998-10-21 | 2023-08-09 | 1-5 | 6 |
| `7UMV` | 2022-04-07 | 2022-10-05 | 2023-10-18 | 1-1 | 2 |
| `3JVR` | 2009-09-17 | 2009-10-06 | 2024-02-21 | 1-3 | 4 |
| `1T48` | 2004-04-28 | 2004-07-20 | 2023-08-23 | 1-3 | 4 |
| `7BJ1` | 2021-01-13 | 2021-03-03 | 2024-01-31 | 1-4 | 5 |
| `3F9M` | 2008-11-14 | 2008-12-02 | 2023-11-01 | 1-5 | 6 |
| `1VRT` | 1995-04-19 | 1996-04-03 | 2024-10-16 | 1-4 | 5 |
| `2BRK` | 2005-05-06 | 2005-06-14 | 2023-12-13 | 1-3 | 4 |
| `5FTJ` | 2016-01-14 | 2016-01-27 | 2024-05-08 | 1-6 | 7 |
| `1T36` | 2004-04-24 | 2004-09-21 | 2024-10-16 | 2-0 | 6 |
| `8QYP` | 2023-10-26 | 2023-12-13 | 2023-12-13 | 1-0 | 1 |
| `9YRG` | 2025-10-16 | 2026-04-08 | 2026-05-20 | 1-1 | 2 |

`1T36` is the only entry in the set at major version 2.

## 3. Table C — entities, chains, organisms, UniProt, mutations, assembly 1

`rcsb_entry_info.polymer_entity_count` / `.nonpolymer_entity_count` /
`.branched_entity_count` / `.deposited_polymer_entity_instance_count`,
`rcsb_entity_source_organism[].scientific_name`,
`rcsb_polymer_entity_container_identifiers.uniprot_ids`,
`entity_poly.rcsb_mutation_count`, `rcsb_polymer_entity.pdbx_mutation`, and
`assembly/1` → `pdbx_struct_assembly.oligomeric_details` with `rcsb_struct_symmetry`.

| PDB | poly / non-poly / branched entities | chains | assembly 1 | entity → organism, UniProt, mutations |
| --- | :-: | ---: | --- | --- |
| `4OBE` | 1 / 2 / 0 | 2 | monomeric (1 polymer, 2 non-polymer) A1 | **1** GTPase KRas (A,B) — Homo sapiens, `P01116`, mut: 0 |
| `4LDJ` | 1 / 2 / 0 | 1 | monomeric (1 polymer, 2 non-polymer) A1 | **1** GTPase KRas (A) — Homo sapiens, `P01116`, mut: 1 at auth 12 |
| `1OPL` | 1 / 2 / 0 | 2 | monomeric (1 polymer, 2 non-polymer) A1 | **1** proto-oncogene tyrosine-protein kinase (A,B) — Homo sapiens, `P00519`, mut: D382N, K29R, E29D (count 3) |
| `2G2H` | 1 / 1 / 0 | 2 | monomeric (1 polymer, 1 non-polymer) A1 | **1** Abl Tyrosine (A,B) — Homo sapiens, `P00519`, mut: H396P (count 1) |
| `5TBY` | 3 / 0 / 0 | 6 | hexameric (6 polymer) A2, B2, C2 | **1** Myosin-7 (A,B) — Homo sapiens, `P12883`, mut: 0<br>**2** Myosin light chain 3 (C,D) — Homo sapiens, `P08590`, mut: 0<br>**3** Myosin regulatory light chain 2, ventricular/cardiac muscle isoform (E,F) — Homo sapiens, `P10916`, mut: 0 |
| `9GZ3` | 1 / 3 / 0 | 1 | monomeric (1 polymer, 3 non-polymer) A1 | **1** Myosin-7 (A) — Homo sapiens, `P12883`, mut: 1 at auth 1124 |
| `6OIM` | 1 / 3 / 0 | 1 | monomeric (1 polymer, 3 non-polymer) A1 | **1** GTPase KRas (A) — Homo sapiens, `P01116`, mut: C51S,C80L,C118S (count 4) |
| `5MO4` | 1 / 2 / 0 | 1 | monomeric (1 polymer, 2 non-polymer) A1 | **1** Tyrosine-protein kinase ABL1 (A) — Homo sapiens, `P00519`, mut: T334I D382N (count 0) |
| `6C1H` | 3 / 2 / 0 | 7 | heptameric (7 polymer, 10 non-polymer) A5, B1, C1 | **1** Actin, alpha skeletal muscle (A,B,C,D,E) — Oryctolagus cuniculus, `P68135`, mut: 0<br>**2** Unconventional myosin-Ib (P) — Rattus norvegicus, `Q05096`, mut: 0<br>**3** Calmodulin (R) — unidentified, `P0DP23`, mut: 0 |
| `9GZ2` | 1 / 4 / 0 | 1 | monomeric (1 polymer, 4 non-polymer) A1 | **1** Myosin-7 (A) — Homo sapiens, `P12883`, mut: 1 at auth 1124 |
| `8QYR` | 1 / 6 / 0 | 1 | monomeric (1 polymer, 8 non-polymer) A1 | **1** Myosin-7 (B) — Bos taurus, `Q9BE39`, mut: 0 |
| `9GZ1` | 3 / 4 / 0 | 6 | hexameric (6 polymer, 10 non-polymer) A2, B2, C2 | **1** Myosin-7 (A,B) — Homo sapiens, `P12883`, mut: 1 at auth 1124<br>**2** Myosin light chain 1/3, skeletal muscle isoform (C,E) — Mus musculus, `P05977`, mut: 0<br>**3** Myosin regulatory light chain 11 (D,F) — Mus musculus, `P97457`, mut: 0 |
| `8QYQ` | 3 / 6 / 0 | 4 | dimeric (2 polymer, 8 non-polymer) A1, B1 | **1** Myosin-7 (A,B) — Bos taurus, `Q9BE39`, mut: 0<br>**2** Myosin light chain 3 (C) — Bos taurus, `P85100`, mut: 0<br>**3** Myosin light chain 3 (D) — Bos taurus, `P85100`, mut: 0 |
| `9YP9` | 3 / 3 / 0 | 6 | hexameric (6 polymer, 6 non-polymer) A2, B2, C2 | **1** Myosin-7,General control transcription factor GCN4,Enhanced Green fluorescent protein (A,B) — Homo sapiens/Saccharomyces cerevisiae/Aequorea victoria, `P03069,P12883,P42212`, mut: 4 at auth 1055,1118,1119,1285<br>**2** Myosin light chain 1/3, skeletal muscle isoform (C,D) — Mus musculus, `P05977`, mut: 0<br>**3** Myosin regulatory light chain 11 (E,F) — Mus musculus, `P97457`, mut: 0 |
| `9YR7` | 3 / 3 / 0 | 6 | hexameric (6 polymer, 6 non-polymer) A2, B2, C2 | **1** Myosin-7,General control transcription factor GCN4,Enhanced Green fluorescent protein (A,B) — Homo sapiens/Saccharomyces cerevisiae/Aequorea victoria, `P03069,P12883,P42212`, mut: 4 at auth 1055,1118,1119,1285<br>**2** Myosin light chain 1/3, skeletal muscle isoform (C,D) — Mus musculus, `P05977`, mut: 0<br>**3** Myosin regulatory light chain 11 (E,F) — Mus musculus, `P97457`, mut: 0 |
| `1ZZW` | 1 / 2 / 0 | 2 | monomeric (1 polymer, 1 non-polymer) A1 | **1** Dual specificity protein phosphatase 10 (A,B) — Homo sapiens, `Q9Y6W6`, mut: 0 |
| `1IA8` | 1 / 1 / 0 | 1 | monomeric (1 polymer, 1 non-polymer) A1 | **1** CHK1 CHECKPOINT KINASE (A) — Homo sapiens, `O14757`, mut: 0 |
| `1SUG` | 1 / 2 / 0 | 1 | monomeric (1 polymer, 5 non-polymer) A1 | **1** Protein-tyrosine phosphatase, non-receptor type 1 (A) — Homo sapiens, `P18031`, mut: 0 |
| `6P7Z` | 1 / 4 / 0 | 1 | monomeric (1 polymer, 7 non-polymer) A1 | **1** Histone-lysine N-methyltransferase SMYD3 (A) — Homo sapiens, `Q9H7B4`, mut: 0 |
| `3IDH` | 1 / 2 / 0 | 1 | monomeric (1 polymer, 2 non-polymer) A1 | **1** Glucokinase (A) — Homo sapiens, `P35557`, mut: 0 |
| `1RTJ` | 2 / 0 / 0 | 2 | dimeric (2 polymer) A2 | **1** HIV-1 REVERSE TRANSCRIPTASE (A) — Human immunodeficiency virus 1, `P04585`, mut: 0<br>**2** HIV-1 REVERSE TRANSCRIPTASE (B) — Human immunodeficiency virus 1, `P04585`, mut: 0 |
| `1QUV` | 1 / 0 / 0 | 1 | monomeric (1 polymer) A1 | **1** PROTEIN (RNA-DIRECTED RNA POLYMERASE) (A) — Hepatitis C virus, `P26663`, mut: R2963Q (count 1) |
| `5FTK` | 1 / 1 / 0 | 6 | hexameric (6 polymer, 12 non-polymer) A6 | **1** TRANSITIONAL ENDOPLASMIC RETICULUM ATPASE (A,B,C,D,E,F) — HOMO SAPIENS, `P55072`, mut: 0 |
| `1A9X` | 2 / 7 / 0 | 8 | octameric (8 polymer, 103 non-polymer) A4, B4 | **1** CARBAMOYL PHOSPHATE SYNTHETASE (LARGE CHAIN) (A,C,E,G) — Escherichia coli, `P00968`, mut: 0<br>**2** CARBAMOYL PHOSPHATE SYNTHETASE (SMALL CHAIN) (B,D,F,H) — Escherichia coli, `P0A6F1`, mut: H353N (count 2) |
| `7UMV` | 1 / 2 / 0 | 1 | monomeric (1 polymer, 2 non-polymer) A1 | **1** Dual specificity protein phosphatase 10 (A) — Homo sapiens, `Q9Y6W6`, mut: 0 |
| `3JVR` | 1 / 1 / 0 | 1 | monomeric (1 polymer, 1 non-polymer) A1 | **1** Serine/threonine-protein kinase Chk1 (A) — Homo sapiens, `O14757`, mut: 0 |
| `1T48` | 1 / 1 / 0 | 1 | monomeric (1 polymer, 1 non-polymer) A1 | **1** Protein-tyrosine phosphatase, non-receptor type 1 (A) — Homo sapiens, `P18031`, mut: 0 |
| `7BJ1` | 1 / 5 / 0 | 1 | monomeric (1 polymer, 9 non-polymer) A1 | **1** Histone-lysine N-methyltransferase SMYD3 (A) — Homo sapiens, `Q9H7B4`, mut: K13N, K140R (count 2) |
| `3F9M` | 1 / 2 / 0 | 1 | monomeric (1 polymer, 2 non-polymer) A1 | **1** Glucokinase (A) — Homo sapiens, `P35557`, mut: 0 |
| `1VRT` | 2 / 2 / 0 | 2 | dimeric (2 polymer, 2 non-polymer) A2 | **1** HIV-1 REVERSE TRANSCRIPTASE (A) — Human immunodeficiency virus 1, `P04585`, mut: 0<br>**2** HIV-1 REVERSE TRANSCRIPTASE (B) — Human immunodeficiency virus 1, `P04585`, mut: 0 |
| `2BRK` | 1 / 2 / 0 | 1 | monomeric (1 polymer, 3 non-polymer) A1 | **1** RNA-DIRECTED RNA POLYMERASE (A) — HEPATITIS C VIRUS, `P26663`, mut: 0 |
| `5FTJ` | 1 / 2 / 0 | 6 | hexameric (6 polymer, 18 non-polymer) A6 | **1** TRANSITIONAL ENDOPLASMIC RETICULUM ATPASE (A,B,C,D,E,F) — HOMO SAPIENS, `P55072`, mut: 0 |
| `1T36` | 2 / 8 / 0 | 8 | octameric (8 polymer, 86 non-polymer) A4, B4 | **1** Carbamoyl-phosphate synthase large chain (A,C,E,G) — Escherichia coli, `P00968`, mut: 0<br>**2** Carbamoyl-phosphate synthase small chain (B,D,F,H) — Escherichia coli, `P0A6F1`, mut: C248D (count 1) |
| `8QYP` | 1 / 3 / 0 | 1 | monomeric (1 polymer, 3 non-polymer) A1 | **1** Myosin-7 (A) — Bos taurus, `Q9BE39`, mut: 0 |
| `9YRG` | 3 / 2 / 0 | 6 | hexameric (6 polymer, 4 non-polymer) A2, B2, C2 | **1** Myosin-7,General control transcription factor GCN4,Enhanced Green fluorescent protein (A,B) — Homo sapiens/Saccharomyces cerevisiae/Aequorea victoria, `P03069,P12883,P42212`, mut: 4 at auth 1055,1118,1119,1285<br>**2** Myosin light chain 1/3, skeletal muscle isoform (C,D) — Mus musculus, `P05977`, mut: 0<br>**3** Myosin regulatory light chain 11 (E,F) — Mus musculus, `P97457`, mut: 0 |

`pdbx_mutation` is a depositor free-text field and is empty on seven entities that RCSB still
counts mutations for — `4LDJ`, `9GZ3`, `9GZ2`, `9GZ1`, `9YP9`, `9YR7` and `9YRG`. Where it is
empty the table gives the count and the author-numbered positions from
`rcsb_polymer_entity_feature` of type `mutation`, mapped through
`auth_to_entity_poly_seq_mapping`.

**RCSB's two mutation fields disagree on one entry.** `5MO4` carries
`rcsb_polymer_entity.pdbx_mutation = "T334I D382N"` and `entity_poly.rcsb_mutation_count = 0`,
with no `mutation` feature and therefore no positions. The repository's `docs/targets.md`
describes `5MO4` as being on a "T334I/D382N background", which the depositor field supports
and the derived count does not. Both values are printed above; neither is corrected here.

## 4. Table D — validation percentiles

From the wwPDB validation report `<Entry>` element: `clashscore`, `percent-rama-outliers`,
`percent-rota-outliers`, `percent-RSRZ-outliers`, each with its
`absolute-percentile-*` and `relative-percentile-*`. Percentiles run 0 (worst) to 100 (best).
Absolute is against the whole PDB, relative against entries in the same resolution band
(`percentilebins`).

| PDB | clash | abs | rel | Rama % | abs | rel | sidechain % | abs | rel | RSRZ % | abs | rel | bins | report |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| `4OBE` | 1.11 | 95.7 | 86.1 | 0 | 100 | 100 | 0 | 100 | 100 | 2.95 | 53.5 | 54.7 | all,1.24,xray | 2026-04-25 |
| `4LDJ` | 1.1 | 95.7 | 87.7 | 0 | 100 | 100 | 0 | 100 | 100 | 0 | 100 | 100 | all,1.15,xray | 2026-03-07 |
| `1OPL` | 11.29 | 20.1 | 50.2 | 0.62 | 21 | 49.3 | 2.95 | 36 | 58.6 | 6.5 | 24.6 | 19.3 | all,3.42,xray | 2026-03-20 |
| `2G2H` | 12.9 | 16.4 | 13.3 | 0.74 | 18.3 | 14.1 | 2.1 | 46.7 | 52 | 13.42 | 6.8 | 5.9 | all,2.0,xray | 2026-03-09 |
| `5TBY` | 51.3 | 1.7 | 1.7 | 5.96 | 2 | 1 | 1.96 | 47.7 | 19.6 | — | — | — | all,em | 2026-03-09 |
| `9GZ3` | 1.54 | 91.8 | 93.2 | 0.26 | 37.2 | 22.2 | 0.15 | 85.5 | 63.7 | — | — | — | all,em | 2026-03-06 |
| `6OIM` | 1.46 | 92.6 | 89.4 | 0 | 100 | 100 | 0 | 100 | 100 | 2.4 | 59.5 | 64.7 | all,1.65,xray | 2026-03-06 |
| `5MO4` | 1.19 | 95 | 96.6 | 0 | 100 | 100 | 0.85 | 73 | 83.4 | 5.13 | 33.2 | 32.5 | all,2.17,xray | 2026-03-09 |
| `6C1H` | 6.37 | 44.2 | 56.2 | 0.04 | 100 | 100 | 0.05 | 100 | 100 | — | — | — | all,em | 2026-03-15 |
| `9GZ2` | 1.78 | 89.2 | 91.9 | 0 | 100 | 100 | 0.15 | 85.5 | 63.7 | — | — | — | all,em | 2026-03-20 |
| `8QYR` | 3.28 | 71.6 | 66 | 0.14 | 47.5 | 34.3 | 3.9 | 28.5 | 16 | 5.36 | 31.1 | 29.8 | all,1.8,xray | 2026-03-07 |
| `9GZ1` | 14.4 | 15.9 | 15.7 | 0.13 | 49.1 | 42.8 | 0 | 100 | 100 | — | — | — | all,em | 2026-03-14 |
| `8QYQ` | 3.06 | 74.1 | 87.2 | 0.57 | 21 | 39.3 | 4.98 | 21.6 | 43.6 | 9.45 | 13.8 | 10.7 | all,2.61,xray | 2026-03-09 |
| `9YP9` | 9.21 | 29.4 | 34.7 | 0.04 | 100 | 100 | 0.47 | 78.3 | 47 | — | — | — | all,em | 2026-05-12 |
| `9YR7` | 10.18 | 25.8 | 29.2 | 0.04 | 100 | 100 | 1.04 | 65.5 | 31.2 | — | — | — | all,em | 2026-05-12 |
| `1ZZW` | 7.98 | 32 | 15.5 | 0 | 100 | 100 | 0.77 | 73 | 59.1 | 6.12 | 26.8 | 27.3 | all,1.6,xray | 2026-04-18 |
| `1IA8` | 19.79 | 7.7 | 1.7 | 1.12 | 11.3 | 2.5 | 3.85 | 29.2 | 12.7 | — | — | — | all,1.7,xray | 2026-03-09 |
| `1SUG` | 9.78 | 24.7 | 15.1 | 0.34 | 36.3 | 28.4 | 0.74 | 75.6 | 76.5 | 4.36 | 38.7 | 44.9 | all,1.95,xray | 2026-03-09 |
| `6P7Z` | 2.17 | 85.3 | 71.4 | 0 | 100 | 100 | 0 | 100 | 100 | 11.29 | 9.7 | 10.9 | all,1.19,xray | 2026-03-05 |
| `3IDH` | 5.27 | 50 | 43.2 | 1.11 | 11.3 | 5.6 | 7.97 | 11 | 6.6 | 3.8 | 44 | 49 | all,2.14,xray | 2026-03-09 |
| `1RTJ` | 32.13 | 2.8 | 1.3 | 3.12 | 3 | 1.6 | 18.37 | 1.5 | 1.2 | — | — | — | all,2.35,xray | 2026-03-07 |
| `1QUV` | 27.95 | 3.8 | 6.6 | 2.37 | 4.4 | 7.7 | 24.84 | 0.5 | 0.9 | 1.08 | 77.7 | 74.6 | all,2.5,xray | 2026-03-14 |
| `5FTK` | 25.17 | 6.4 | 5.8 | 0.42 | 31 | 17.5 | 0.65 | 73 | 39.5 | — | — | — | all,em | 2026-03-06 |
| `1A9X` | 17.36 | 9.8 | 2.9 | 0.35 | 29.6 | 18.9 | 9.58 | 7.7 | 2 | — | — | — | all,1.8,xray | 2026-03-05 |
| `7UMV` | 1.62 | 91.6 | 90.6 | 0 | 100 | 100 | 1.53 | 56.8 | 49.4 | 2.67 | 55.8 | 55.8 | all,1.8,xray | 2026-03-09 |
| `3JVR` | 7.31 | 35.8 | 18 | 0 | 100 | 100 | 3.04 | 36 | 15.9 | 15.5 | 4.9 | 5.3 | all,1.76,xray | 2026-03-05 |
| `1T48` | 17.95 | 9.3 | 8.9 | 1.04 | 12.5 | 11.4 | 1.89 | 49.8 | 65.8 | 7.53 | 20.1 | 17.4 | all,2.2,xray | 2026-03-06 |
| `7BJ1` | 4.12 | 62 | 46.3 | 0 | 100 | 100 | 0 | 100 | 100 | 4.93 | 34.7 | 37.3 | all,1.61,xray | 2026-03-07 |
| `3F9M` | 7.28 | 35.8 | 18 | 0.89 | 14 | 2.9 | 4.11 | 27 | 4.7 | 8.89 | 15.1 | 16.1 | all,1.5,xray | 2026-03-08 |
| `1VRT` | 16.02 | 11.4 | 12.2 | 1.2 | 10.2 | 8.4 | 11.81 | 4.9 | 4.6 | — | — | — | all,2.2,xray | 2026-03-09 |
| `2BRK` | 5.86 | 45.1 | 56.3 | 0.62 | 21 | 26.7 | 4.62 | 23.9 | 36.1 | 4.69 | 36.2 | 37.9 | all,2.3,xray | 2026-03-09 |
| `5FTJ` | 40.89 | 2.6 | 2.6 | 0.97 | 15 | 8 | 0.81 | 70.5 | 36.2 | — | — | — | all,em | 2026-03-24 |
| `1T36` | 19.36 | 8 | 5.1 | 0.35 | 36.3 | 36.5 | 8.93 | 9 | 6.4 | 2.77 | 54.6 | 57.5 | all,2.1,xray | 2026-03-05 |
| `8QYP` | 6.58 | 40.1 | 57 | 0.29 | 36.3 | 56.1 | 5.88 | 17.5 | 32.8 | 2.41 | 59.5 | 57.2 | all,2.759,xray | 2026-03-06 |
| `9YRG` | 8.81 | 31 | 37.3 | 0.04 | 100 | 100 | 0.48 | 78.3 | 47 | — | — | — | all,em | 2026-05-12 |

Cryo-EM entries have no RSRZ line: the report bin is `all,em` and no electron-density fit is
computed. The four X-ray entries with no released structure factors — `1IA8`, `1RTJ`, `1A9X`,
`1VRT` — have no RSRZ either, for the same reason on the other side.

## 5. Table E — non-polymer components

`nonpolymer_entity` → `pdbx_entity_nonpoly.name`; formula weight from `chemcomp` →
`chem_comp.formula_weight` (daltons). Per-instance density fit from
`nonpolymer_entity_instance` → `rcsb_nonpolymer_instance_validation_score[0].RSCC` / `.RSR`,
cross-checked against the `rscc`/`rsr` attributes of the validation report's
`ModelledSubgroup` rows. `SOI` is RCSB's own `is_subject_of_investigation` — its "ligand of
interest" call. `buffer?` is **our** criterion, not RCSB's: membership of a fixed list of
common cryoprotectants, salts, buffers and precipitants held in
`fetch_structure_evidence.py` as `CRYO_BUFFER`. Read it as a hint, never as a verdict:
`PO4` and `MG` are on that list and are catalytic in the myosin entries.

| PDB | comp | name | FW (Da) | copies | chains | SOI | buffer? | RSCC | RSR | flags |
| --- | --- | --- | ---: | ---: | --- | :-: | :-: | ---: | ---: | --- |
| `4OBE` | `GDP` | GUANOSINE-5'-DIPHOSPHATE | 443.201 | 2 | A,B | Y | — | 0.982–0.986 | 0.051–0.056 | `HAS_METAL_COORDINATION_LINKAGE` |
| `4OBE` | `MG` | MAGNESIUM ION | 24.305 | 2 | A,B | — | Y | 0.996 | 0.015–0.046 | `HAS_METAL_COORDINATION_LINKAGE` |
| `4LDJ` | `GDP` | GUANOSINE-5'-DIPHOSPHATE | 443.201 | 1 | A | Y | — | 0.988 | 0.042 | `HAS_METAL_COORDINATION_LINKAGE` |
| `4LDJ` | `MG` | MAGNESIUM ION | 24.305 | 1 | A | — | Y | 0.996 | 0.066 | `HAS_METAL_COORDINATION_LINKAGE` |
| `1OPL` | `MYR` | MYRISTIC ACID | 228.371 | 1 | A | Y | — | 0.902 | 0.246 | — |
| `1OPL` | `P16` | 6-(2,6-DICHLOROPHENYL)-2-{[3-(HYDROXYMETHYL) | 427.283 | 2 | A,B | Y | — | 0.582–0.842 | 0.182–0.197 | `IS_RSCC_OUTLIER` |
| `2G2H` | `P16` | 6-(2,6-DICHLOROPHENYL)-2-{[3-(HYDROXYMETHYL) | 427.283 | 2 | A,B | Y | — | 0.809–0.839 | 0.128–0.15 | — |
| `5TBY` | *(none)* |  |  |  |  |  |  |  |  |  |
| `9GZ3` | `MG` | MAGNESIUM ION | 24.305 | 1 | A | — | Y | — | — | `HAS_METAL_COORDINATION_LINKAGE` |
| `9GZ3` | `ADP` | ADENOSINE-5'-DIPHOSPHATE | 427.201 | 1 | A | Y | — | — | — | `HAS_METAL_COORDINATION_LINKAGE` |
| `9GZ3` | `PO4` | PHOSPHATE ION | 94.971 | 1 | A | — | Y | — | — | `HAS_METAL_COORDINATION_LINKAGE` |
| `6OIM` | `MG` | MAGNESIUM ION | 24.305 | 1 | A | — | Y | 0.981 | 0.034 | `HAS_METAL_COORDINATION_LINKAGE` |
| `6OIM` | `GDP` | GUANOSINE-5'-DIPHOSPHATE | 443.201 | 1 | A | Y | — | 0.971 | 0.053 | `HAS_METAL_COORDINATION_LINKAGE` |
| `6OIM` | `MOV` | AMG 510 (bound form) | 562.61 | 1 | A | Y | — | 0.908 | 0.084 | `HAS_COVALENT_LINKAGE` |
| `5MO4` | `NIL` | Nilotinib | 529.516 | 1 | A | Y | — | 0.967 | 0.061 | — |
| `5MO4` | `AY7` | asciminib | 449.838 | 1 | A | Y | — | 0.946 | 0.095 | — |
| `6C1H` | `ADP` | ADENOSINE-5'-DIPHOSPHATE | 427.201 | 5 | A,B,C,D,E | Y | — | — | — | `HAS_METAL_COORDINATION_LINKAGE` |
| `6C1H` | `MG` | MAGNESIUM ION | 24.305 | 5 | A,B,C,D,E | — | Y | — | — | `HAS_METAL_COORDINATION_LINKAGE` |
| `9GZ2` | `MG` | MAGNESIUM ION | 24.305 | 1 | A | — | Y | — | — | `HAS_METAL_COORDINATION_LINKAGE` |
| `9GZ2` | `ADP` | ADENOSINE-5'-DIPHOSPHATE | 427.201 | 1 | A | — | — | — | — | `HAS_METAL_COORDINATION_LINKAGE` |
| `9GZ2` | `PO4` | PHOSPHATE ION | 94.971 | 1 | A | — | Y | — | — | `HAS_METAL_COORDINATION_LINKAGE` |
| `9GZ2` | `XB2` | Mavacamten | 273.33 | 1 | A | Y | — | — | — | — |
| `8QYR` | `XB2` | Mavacamten | 273.33 | 1 | B | Y | — | 0.915 | 0.084 | — |
| `8QYR` | `SO4` | SULFATE ION | 96.063 | 3 | B | — | Y | 0.718–0.899 | 0.112–0.15 | — |
| `8QYR` | `EDO` | 1,2-ETHANEDIOL | 62.068 | 1 | B | — | Y | 0.876 | 0.144 | — |
| `8QYR` | `MG` | MAGNESIUM ION | 24.305 | 1 | B | Y | Y | 0.986 | 0.04 | `HAS_METAL_COORDINATION_LINKAGE` |
| `8QYR` | `ADP` | ADENOSINE-5'-DIPHOSPHATE | 427.201 | 1 | B | Y | — | 0.972 | 0.057 | `HAS_METAL_COORDINATION_LINKAGE` |
| `8QYR` | `BEF` | BERYLLIUM TRIFLUORIDE ION | 66.007 | 1 | B | Y | — | 0.975 | 0.035 | `HAS_METAL_COORDINATION_LINKAGE` |
| `9GZ1` | `MG` | MAGNESIUM ION | 24.305 | 4 | A,B,D,F | — | Y | — | — | `HAS_METAL_COORDINATION_LINKAGE` |
| `9GZ1` | `ADP` | ADENOSINE-5'-DIPHOSPHATE | 427.201 | 2 | A,B | — | — | — | — | `HAS_METAL_COORDINATION_LINKAGE` |
| `9GZ1` | `PO4` | PHOSPHATE ION | 94.971 | 2 | A,B | — | Y | — | — | `HAS_METAL_COORDINATION_LINKAGE` |
| `9GZ1` | `XB2` | Mavacamten | 273.33 | 2 | A,B | Y | — | — | — | — |
| `8QYQ` | `ADP` | ADENOSINE-5'-DIPHOSPHATE | 427.201 | 2 | A,B | Y | — | 0.983–0.984 | 0.053 | `HAS_METAL_COORDINATION_LINKAGE` |
| `8QYQ` | `BEF` | BERYLLIUM TRIFLUORIDE ION | 66.007 | 2 | A,B | Y | — | 0.974–0.988 | 0.067–0.073 | `HAS_METAL_COORDINATION_LINKAGE` |
| `8QYQ` | `MG` | MAGNESIUM ION | 24.305 | 2 | A,B | Y | Y | 0.998 | 0.026–0.037 | `HAS_METAL_COORDINATION_LINKAGE` |
| `8QYQ` | `XB2` | Mavacamten | 273.33 | 2 | A,B | Y | — | 0.98–0.983 | 0.054–0.058 | — |
| `8QYQ` | `FMT` | FORMIC ACID | 46.025 | 5 | A,B | — | Y | 0.892–0.96 | 0.091–0.238 | — |
| `8QYQ` | `GOL` | GLYCEROL | 92.094 | 1 | C | — | Y | 0.89 | 0.116 | — |
| `9YP9` | `PO4` | PHOSPHATE ION | 94.971 | 2 | A,B | Y | Y | — | — | — |
| `9YP9` | `XB2` | Mavacamten | 273.33 | 2 | A,B | Y | — | — | — | — |
| `9YP9` | `ADP` | ADENOSINE-5'-DIPHOSPHATE | 427.201 | 2 | A,B | Y | — | — | — | — |
| `9YR7` | `XB2` | Mavacamten | 273.33 | 2 | A,B | Y | — | — | — | — |
| `9YR7` | `ADP` | ADENOSINE-5'-DIPHOSPHATE | 427.201 | 2 | A,B | Y | — | — | — | — |
| `9YR7` | `PO4` | PHOSPHATE ION | 94.971 | 2 | A,B | Y | Y | — | — | — |
| `1ZZW` | `SO4` | SULFATE ION | 96.063 | 2 | A,B | — | Y | 0.675–0.974 | 0.075–0.239 | — |
| `1ZZW` | `EDO` | 1,2-ETHANEDIOL | 62.068 | 1 | B | — | Y | 0.84 | 0.155 | — |
| `1IA8` | `SO4` | SULFATE ION | 96.063 | 1 | A | — | Y | — | — | — |
| `1SUG` | `TRS` | 2-AMINO-2-HYDROXYMETHYL-PROPANE-1,3-DIOL | 122.143 | 1 | A | — | Y | 0.685 | 0.201 | — |
| `1SUG` | `GOL` | GLYCEROL | 92.094 | 4 | A | — | Y | 0.817–0.918 | 0.104–0.192 | — |
| `6P7Z` | `ZN` | ZINC ION | 65.409 | 3 | A | — | Y | 0.709–0.983 | 0.05–0.536 | `HAS_METAL_COORDINATION_LINKAGE` |
| `6P7Z` | `MG` | MAGNESIUM ION | 24.305 | 2 | A | — | Y | 0.992–0.993 | 0.08–0.144 | `HAS_METAL_COORDINATION_LINKAGE` |
| `6P7Z` | `SAM` | S-ADENOSYLMETHIONINE | 398.437 | 1 | A | — | — | 0.988 | 0.04 | — |
| `6P7Z` | `O41` | 5-cyclopropyl-N-[1-(methylsulfonyl)piperidin | 313.373 | 1 | A | Y | — | 0.771 | 0.177 | — |
| `3IDH` | `GLC` | alpha-D-glucopyranose | 180.156 | 1 | A | Y | Y | 0.951 | 0.054 | — |
| `3IDH` | `K` | POTASSIUM ION | 39.098 | 1 | A | — | Y | 0.975 | 0.072 | `HAS_METAL_COORDINATION_LINKAGE` |
| `1RTJ` | *(none)* |  |  |  |  |  |  |  |  |  |
| `1QUV` | *(none)* |  |  |  |  |  |  |  |  |  |
| `5FTK` | `ADP` | ADENOSINE-5'-DIPHOSPHATE | 427.201 | 12 | A,B,C,D,E,F | Y | — | — | — | — |
| `1A9X` | `PO4` | PHOSPHATE ION | 94.971 | 15 | C,E,G,A | — | Y | — | — | `HAS_METAL_COORDINATION_LINKAGE` |
| `1A9X` | `MN` | MANGANESE (II) ION | 54.938 | 12 | G,C,E,A | — | Y | — | — | `HAS_METAL_COORDINATION_LINKAGE` |
| `1A9X` | `K` | POTASSIUM ION | 39.098 | 32 | A,F,H,B,D,G,C,E | — | Y | — | — | `HAS_METAL_COORDINATION_LINKAGE` |
| `1A9X` | `CL` | CHLORIDE ION | 35.453 | 28 | F,H,B,D,G,C,E,A | — | Y | — | — | — |
| `1A9X` | `ADP` | ADENOSINE-5'-DIPHOSPHATE | 427.201 | 8 | E,G,A,C | Y | — | — | — | `HAS_METAL_COORDINATION_LINKAGE` |
| `1A9X` | `ORN` | L-ornithine | 132.161 | 4 | E,G,A,C | — | — | — | — | — |
| `1A9X` | `NET` | TETRAETHYLAMMONIUM ION | 130.251 | 4 | E,G,A,C | — | — | — | — | — |
| `7UMV` | `NUU` | 1-{[(10aP)-5,6-dihydropyrido[2,3-h]quinazoli | 313.417 | 1 | A | Y | — | 0.98 | 0.056 | — |
| `7UMV` | `ACT` | ACETATE ION | 59.044 | 1 | A | — | Y | 0.904 | 0.156 | — |
| `3JVR` | `AGX` | (1S)-1-(1H-benzimidazol-2-yl)ethyl (3,4-dich | 350.199 | 1 | A | Y | — | 0.962 | 0.088 | — |
| `1T48` | `BB3` | 3-(3,5-DIBROMO-4-HYDROXY-BENZOYL)-2-ETHYL-BE | 531.215 | 1 | A | Y | — | 0.969 | 0.112 | — |
| `7BJ1` | `SAM` | S-ADENOSYLMETHIONINE | 398.437 | 1 | A | — | — | 0.97 | 0.056 | — |
| `7BJ1` | `QKT` | Diperodon (S-enantiomer) | 397.467 | 1 | A | Y | — | 0.817 | 0.14 | — |
| `7BJ1` | `ZN` | ZINC ION | 65.409 | 3 | A | — | Y | 0.988–0.993 | 0.023–0.029 | `HAS_METAL_COORDINATION_LINKAGE` |
| `7BJ1` | `ACT` | ACETATE ION | 59.044 | 2 | A | — | Y | 0.833–0.837 | 0.118–0.128 | — |
| `7BJ1` | `GOL` | GLYCEROL | 92.094 | 2 | A | — | Y | 0.867–0.892 | 0.106–0.11 | — |
| `3F9M` | `GLC` | alpha-D-glucopyranose | 180.156 | 1 | A | Y | Y | 0.949 | 0.073 | — |
| `3F9M` | `MRK` | 2-AMINO-4-FLUORO-5-[(1-METHYL-1H-IMIDAZOL-2- | 349.406 | 1 | A | Y | — | 0.942 | 0.093 | — |
| `1VRT` | `MG` | MAGNESIUM ION | 24.305 | 1 | A | — | Y | — | — | `HAS_METAL_COORDINATION_LINKAGE` |
| `1VRT` | `NVP` | 11-CYCLOPROPYL-5,11-DIHYDRO-4-METHYL-6H-DIPY | 266.298 | 1 | A | Y | — | — | — | — |
| `2BRK` | `MN` | MANGANESE (II) ION | 54.938 | 2 | A | — | Y | 0.953–0.984 | 0.039–0.064 | `HAS_METAL_COORDINATION_LINKAGE` |
| `2BRK` | `CMF` | 3-CYCLOHEXYL-1-(2-MORPHOLIN-4-YL-2-OXOETHYL) | 446.538 | 1 | A | Y | — | 0.916 | 0.09 | — |
| `5FTJ` | `ADP` | ADENOSINE-5'-DIPHOSPHATE | 427.201 | 12 | A,B,C,D,E,F | Y | — | — | — | — |
| `5FTJ` | `OJA` | 1-(3-(5-FLUORO-1H-INDOL-2-YL)PHENYL)PIPERIDI | 463.633 | 6 | A,B,C,D,E,F | Y | — | — | — | — |
| `1T36` | `U5P` | URIDINE-5'-MONOPHOSPHATE | 324.181 | 4 | G,E,C,A | Y | — | 0.948–0.964 | 0.086–0.099 | — |
| `1T36` | `MN` | MANGANESE (II) ION | 54.938 | 12 | C,E,A,G | — | Y | 0.992–0.999 | 0.025–0.038 | `HAS_METAL_COORDINATION_LINKAGE` |
| `1T36` | `K` | POTASSIUM ION | 39.098 | 22 | B,E,G,C,A,H,F,D | — | Y | 0.949–0.997 | 0.014–0.087 | `HAS_METAL_COORDINATION_LINKAGE` |
| `1T36` | `PO4` | PHOSPHATE ION | 94.971 | 5 | E,C,A,G | — | Y | 0.771–0.997 | 0.026–0.124 | `HAS_METAL_COORDINATION_LINKAGE` |
| `1T36` | `CL` | CHLORIDE ION | 35.453 | 27 | G,E,C,H,A,F,D | — | Y | 0.839–0.996 | 0.022–0.198 | — |
| `1T36` | `ADP` | ADENOSINE-5'-DIPHOSPHATE | 427.201 | 8 | G,E,C,A | Y | — | 0.971–0.991 | 0.036–0.069 | `HAS_METAL_COORDINATION_LINKAGE` |
| `1T36` | `ORN` | L-ornithine | 132.161 | 4 | G,E,C,A | — | — | 0.942–0.957 | 0.063–0.08 | — |
| `1T36` | `NET` | TETRAETHYLAMMONIUM ION | 130.251 | 4 | G,E,C,A | — | — | 0.969–0.981 | 0.054–0.06 | — |
| `8QYP` | `ADP` | ADENOSINE-5'-DIPHOSPHATE | 427.201 | 1 | A | Y | — | 0.966 | 0.077 | `HAS_METAL_COORDINATION_LINKAGE` |
| `8QYP` | `VO4` | VANADATE ION | 114.939 | 1 | A | Y | — | 0.986 | 0.059 | `HAS_METAL_COORDINATION_LINKAGE` |
| `8QYP` | `MG` | MAGNESIUM ION | 24.305 | 1 | A | — | Y | 0.998 | 0.053 | `HAS_METAL_COORDINATION_LINKAGE` |
| `9YRG` | `ADP` | ADENOSINE-5'-DIPHOSPHATE | 427.201 | 2 | A,B | Y | — | — | — | — |
| `9YRG` | `PO4` | PHOSPHATE ION | 94.971 | 2 | A,B | Y | Y | — | — | — |

## 6. Table F — modelled polymer residues and unmodelled ranges, per chain

Modelled count = length of `auth_to_entity_poly_seq_mapping` minus the residues covered by
`rcsb_polymer_instance_feature` of type `UNOBSERVED_RESIDUE_XYZ`. Ranges are printed in
**author numbering**, mapped through the same array.

| PDB | chain | entity | modelled / deposited seq | unmodelled | unmodelled ranges (auth) |
| --- | :-: | :-: | ---: | ---: | --- |
| `4OBE` | A | 1 | 169 / 170 | 1 | 0–0 |
| `4OBE` | B | 1 | 170 / 170 | 0 | none |
| `4LDJ` | A | 1 | 170 / 170 | 0 | none |
| `1OPL` | A | 1 | 451 / 537 | 86 | 1–80, 532–537 |
| `1OPL` | B | 1 | 365 / 537 | 172 | 1–139, 238–251, 519–537 |
| `2G2H` | A | 1 | 272 / 287 | 15 | 245–251, 524–531 |
| `2G2H` | B | 1 | 272 / 287 | 15 | 245–251, 524–531 |
| `5TBY` | A | 1 | 954 / 1935 | 981 | 1–5, 960–1935 |
| `5TBY` | B | 1 | 950 / 1935 | 985 | 1–9, 960–1935 |
| `5TBY` | C | 2 | 152 / 195 | 43 | 1–43 |
| `5TBY` | D | 2 | 152 / 195 | 43 | 1–43 |
| `5TBY` | E | 3 | 160 / 166 | 6 | 1–6 |
| `5TBY` | F | 3 | 160 / 166 | 6 | 1–6 |
| `9GZ3` | A | 1 | 764 / 1145 | 381 | 2–2, 203–213, 625–643, 797–1146 |
| `6OIM` | A | 1 | 167 / 183 | 16 | -13–-1, 105–107 |
| `5MO4` | A | 1 | 429 / 495 | 66 | 40–82, 296–297, 402–419, 532–534 |
| `6C1H` | A | 1 | 375 / 375 | 0 | none |
| `6C1H` | B | 1 | 375 / 375 | 0 | none |
| `6C1H` | C | 1 | 375 / 375 | 0 | none |
| `6C1H` | D | 1 | 375 / 375 | 0 | none |
| `6C1H` | E | 1 | 375 / 375 | 0 | none |
| `6C1H` | P | 2 | 729 / 729 | 0 | none |
| `6C1H` | R | 3 | 148 / 148 | 0 | none |
| `9GZ2` | A | 1 | 764 / 1145 | 381 | 2–2, 203–213, 625–643, 797–1146 |
| `8QYR` | B | 1 | 711 / 781 | 70 | 1–33, 203–211, 368–370, 568–571, 626–643, 732–734 |
| `9GZ1` | A | 1 | 900 / 1145 | 245 | 2–2, 203–213, 625–643, 933–1146 |
| `9GZ1` | B | 1 | 900 / 1145 | 245 | 2–2, 203–213, 625–643, 933–1146 |
| `9GZ1` | C | 2 | 145 / 187 | 42 | 1–42 |
| `9GZ1` | E | 2 | 148 / 187 | 39 | 1–39 |
| `9GZ1` | D | 3 | 144 / 168 | 24 | 1–17, 162–168 |
| `9GZ1` | F | 3 | 146 / 168 | 22 | 1–14, 161–168 |
| `8QYQ` | A | 1 | 781 / 807 | 26 | 1–2, 203–211, 370–370, 629–642 |
| `8QYQ` | B | 1 | 770 / 807 | 37 | 1–2, 203–211, 627–643, 799–807 |
| `8QYQ` | C | 2 | 157 / 199 | 42 | 1–42 |
| `8QYQ` | D | 3 | 85 / 199 | 114 | 1–79, 103–128, 168–168, 174–180, 199–199 |
| `9YP9` | A | 1 | 940 / 1315 | 375 | 1–3, 944–1315 |
| `9YP9` | B | 1 | 940 / 1315 | 375 | 1–3, 944–1315 |
| `9YP9` | C | 2 | 152 / 188 | 36 | 1–35, 188–188 |
| `9YP9` | D | 2 | 152 / 188 | 36 | 1–35, 188–188 |
| `9YP9` | E | 3 | 142 / 169 | 27 | 1–21, 164–169 |
| `9YP9` | F | 3 | 142 / 169 | 27 | 1–21, 164–169 |
| `9YR7` | A | 1 | 940 / 1315 | 375 | 1–3, 944–1315 |
| `9YR7` | B | 1 | 926 / 1315 | 389 | 1–3, 627–640, 944–1315 |
| `9YR7` | C | 2 | 152 / 188 | 36 | 1–35, 188–188 |
| `9YR7` | D | 2 | 152 / 188 | 36 | 1–35, 188–188 |
| `9YR7` | E | 3 | 142 / 169 | 27 | 1–21, 164–169 |
| `9YR7` | F | 3 | 142 / 169 | 27 | 1–21, 164–169 |
| `1ZZW` | A | 1 | 147 / 149 | 2 | 466–467 |
| `1ZZW` | B | 1 | 147 / 149 | 2 | 319–320 |
| `1IA8` | A | 1 | 272 / 289 | 17 | 1–1, 45–47, 277–289 |
| `1SUG` | A | 1 | 298 / 321 | 23 | 1–1, 300–321 |
| `6P7Z` | A | 1 | 425 / 432 | 7 | -3–2, 94–94 |
| `3IDH` | A | 1 | 453 / 470 | 17 | -4–4, 458–465 |
| `1RTJ` | A | 1 | 543 / 560 | 17 | 544–560 |
| `1RTJ` | B | 2 | 426 / 440 | 14 | 1–1, 218–230 |
| `1QUV` | A | 1 | 553 / 578 | 25 | 544–546, 557–578 |
| `5FTK` | A | 1 | 723 / 806 | 83 | 1–20, 708–727, 764–806 |
| `5FTK` | B | 1 | 723 / 806 | 83 | 1–20, 708–727, 764–806 |
| `5FTK` | C | 1 | 723 / 806 | 83 | 1–20, 708–727, 764–806 |
| `5FTK` | D | 1 | 723 / 806 | 83 | 1–20, 708–727, 764–806 |
| `5FTK` | E | 1 | 723 / 806 | 83 | 1–20, 708–727, 764–806 |
| `5FTK` | F | 1 | 723 / 806 | 83 | 1–20, 708–727, 764–806 |
| `1A9X` | A | 1 | 1058 / 1073 | 15 | 717–723, 742–749 |
| `1A9X` | C | 1 | 1058 / 1073 | 15 | 2717–2723, 2742–2749 |
| `1A9X` | E | 1 | 1058 / 1073 | 15 | 4717–4723, 4742–4749 |
| `1A9X` | G | 1 | 1058 / 1073 | 15 | 6717–6723, 6742–6749 |
| `1A9X` | B | 2 | 379 / 379 | 0 | none |
| `1A9X` | D | 2 | 379 / 379 | 0 | none |
| `1A9X` | F | 2 | 379 / 379 | 0 | none |
| `1A9X` | H | 2 | 379 / 379 | 0 | none |
| `7UMV` | A | 1 | 150 / 152 | 2 | 316–317 |
| `3JVR` | A | 1 | 258 / 271 | 13 | 18–21, 43–49, 77–78 |
| `1T48` | A | 1 | 292 / 298 | 6 | 284–289 |
| `7BJ1` | A | 1 | 426 / 431 | 5 | -2–2 |
| `3F9M` | A | 1 | 451 / 470 | 19 | -4–3, 94–97, 459–465 |
| `1VRT` | A | 1 | 525 / 560 | 35 | 1–3, 444–454, 540–560 |
| `1VRT` | B | 2 | 401 / 440 | 39 | 1–4, 89–91, 216–230, 357–361, 429–440 |
| `2BRK` | A | 1 | 512 / 536 | 24 | 22–35, 148–152, 532–536 |
| `5FTJ` | A | 1 | 723 / 806 | 83 | 1–20, 708–727, 764–806 |
| `5FTJ` | B | 1 | 723 / 806 | 83 | 1–20, 708–727, 764–806 |
| `5FTJ` | C | 1 | 723 / 806 | 83 | 1–20, 708–727, 764–806 |
| `5FTJ` | D | 1 | 723 / 806 | 83 | 1–20, 708–727, 764–806 |
| `5FTJ` | E | 1 | 723 / 806 | 83 | 1–20, 708–727, 764–806 |
| `5FTJ` | F | 1 | 723 / 806 | 83 | 1–20, 708–727, 764–806 |
| `1T36` | A | 1 | 1058 / 1073 | 15 | 717–723, 742–749 |
| `1T36` | C | 1 | 1058 / 1073 | 15 | 717–723, 742–749 |
| `1T36` | E | 1 | 1058 / 1073 | 15 | 717–723, 742–749 |
| `1T36` | G | 1 | 1058 / 1073 | 15 | 717–723, 742–749 |
| `1T36` | B | 2 | 379 / 382 | 3 | 1–1, 381–382 |
| `1T36` | D | 2 | 379 / 382 | 3 | 1–1, 381–382 |
| `1T36` | F | 2 | 379 / 382 | 3 | 1–1, 381–382 |
| `1T36` | H | 2 | 379 / 382 | 3 | 1–1, 381–382 |
| `8QYP` | A | 1 | 706 / 780 | 74 | 1–31, 53–58, 203–211, 368–370, 626–644, 731–736 |
| `9YRG` | A | 1 | 912 / 1315 | 403 | 1–3, 203–214, 627–642, 944–1315 |
| `9YRG` | B | 1 | 908 / 1315 | 407 | 1–3, 202–214, 626–644, 944–1315 |
| `9YRG` | C | 2 | 152 / 188 | 36 | 1–35, 188–188 |
| `9YRG` | D | 2 | 152 / 188 | 36 | 1–35, 188–188 |
| `9YRG` | E | 3 | 142 / 169 | 27 | 1–21, 164–169 |
| `9YRG` | F | 3 | 142 / 169 | 27 | 1–21, 164–169 |

## 7. Table G — cryo-EM entries

`rcsb_entry_container_identifiers.emdb_ids`, `em_experiment.reconstruction_method`,
`em_3d_reconstruction[0].resolution` / `.resolution_method` / `.symmetry_type` /
`.num_particles`, `em_software[]` filtered to `category = MODEL FITTING` and
`MODEL REFINEMENT`, and `em_3d_fitting[0].ref_protocol` / `.target_criteria`.

| PDB | EMDB | reconstruction | map res (Å) | resolution method | symmetry | particles | model-fitting software | fit protocol |
| --- | --- | --- | ---: | --- | --- | ---: | --- | --- |
| `5TBY` | EMD-2240 | SINGLE PARTICLE | 20.0 | FSC 0.5 CUT-OFF | POINT | 10700 | UCSF Chimera 10 | RIGID BODY FIT / CORRELATION COEFFICIENT |
| `9GZ3` | EMD-51721 | SINGLE PARTICLE | 3.4 | FSC 0.143 CUT-OFF | POINT | 88809 | ISOLDE, Coot, PHENIX | FLEXIBLE FIT |
| `6C1H` | EMD-7331 | HELICAL | 3.9 | FSC 0.143 CUT-OFF | HELICAL | 62000 | PHENIX | FLEXIBLE FIT |
| `9GZ2` | EMD-51720 | SINGLE PARTICLE | 2.9 | FSC 0.143 CUT-OFF | POINT | 200487 | ISOLDE, Coot, PHENIX | FLEXIBLE FIT |
| `9GZ1` | EMD-51719 | SINGLE PARTICLE | 3.7 | FSC 0.143 CUT-OFF | POINT | 197869 | ISOLDE, Coot, PHENIX | FLEXIBLE FIT |
| `9YP9` | EMD-73288 | SINGLE PARTICLE | 3.0 | FSC 0.143 CUT-OFF | POINT | 216820 | UCSF ChimeraX, MDFF, Coot, PHENIX 1.20.1_4487:, PHENIX 1.20.1_4487: | FLEXIBLE FIT |
| `9YR7` | EMD-73362 | SINGLE PARTICLE | 3.0 | FSC 0.143 CUT-OFF | POINT | 187695 | UCSF ChimeraX, MDFF, Coot, PHENIX 1.20.1_4487:, PHENIX 1.20.1_4487: | FLEXIBLE FIT |
| `5FTK` | EMD-3296 | SINGLE PARTICLE | 2.4 | — | POINT | 30616 | — | — |
| `5FTJ` | EMD-3295 | SINGLE PARTICLE | 2.3 | — | POINT | 40913 | — | — |
| `9YRG` | EMD-73367 | SINGLE PARTICLE | 3.2 | FSC 0.143 CUT-OFF | POINT | 69575 | UCSF ChimeraX, MDFF, Coot, PHENIX 1.20.1_4487, PHENIX 1.20.1_4487 | FLEXIBLE FIT |

**`5TBY` is the outlier on two columns.** It is the only entry whose recorded map resolution
is worse than 4 Å, the only one whose `resolution_method` is `FSC 0.5 CUT-OFF` rather than the
modern `FSC 0.143`, the only one whose `ref_protocol` is `RIGID BODY FIT` rather than
`FLEXIBLE FIT`, and the only one whose sole model-fitting program is a visualisation tool.
`5FTK` and `5FTJ` record no `resolution_method`, no `em_3d_fitting` and no model-building
software at all — their only `em_software` row is `RECONSTRUCTION: FREALIGN`. Those are
nulls in RCSB, not omissions here.

---

## 8. The six questions

### (a) `1OPL` — per-chain contents, coverage, and the myristate claim

**The organisers' claim is confirmed.** Chain B carries the ATP-site inhibitor and no myristate.

| | chain A | chain B |
| --- | --- | --- |
| non-polymer components | `MYR` 538, `P16` 539 | `P16` 538 |
| modelled polymer residues | 451 of 537 | 365 of 537 |
| unmodelled (auth) | 1–80, 532–537 | 1–139, 238–251, 519–537 |
| modelled span (auth) | 81–531 | 140–518, broken at 238–251 |
| `P16` RSCC / RSR | 0.842 / 0.182 | 0.582 / 0.197 |
| `P16` intermolecular clashes | 2 | 5 |
| `P16` validation flags | `HAS_NO_COVALENT_LINKAGE` | `HAS_NO_COVALENT_LINKAGE`, `IS_RSCC_OUTLIER` |

**Deciding evidence.** Three independent reads agree.

1. `nonpolymer_entity/1OPL/2` → `rcsb_nonpolymer_entity_container_identifiers.auth_asym_ids`
   is `["A"]` for `MYR`. `nonpolymer_entity/1OPL/3` gives `["A", "B"]` for `P16`.
2. The wwPDB validation report has one `ModelledSubgroup` with `resname="MYR"`, on
   `chain="A" resnum="538"`, and two with `resname="P16"`, on `A/539` and `B/538`.
3. The deposited PDB file: chain A `HETATM` residues are `MYR 538` and `P16 539`; chain B's
   is `P16 538` alone. Counting distinct `ATOM` residue numbers gives 451 in chain A
   (81–531, no internal break) and 365 in chain B (140–518, one break at 238–251).

**The cost the reply does not mention.** Chain B models 86 fewer residues than chain A. The extra loss is at the N-terminus — chain B's first modelled residue is 140 against chain A's
81, so the 59 residues chain A models at 81–139 are absent — plus an internal 14-residue
break at 238–251 and 13 more at the C-terminus, 86 in total. Chain B is also the worse-resolved copy: its
`P16` sits at RSCC 0.582 and is flagged `IS_RSCC_OUTLIER`, against 0.842 in chain A.
A contact network built on chain B is a smaller and a noisier graph. That is a real trade
against the ligand-freeness the organisers are buying, and it should be stated in the
submission rather than absorbed silently.

### (b) The mavacamten candidates

`XB2` is mavacamten: `chemcomp/XB2` gives `chem_comp.name = "Mavacamten"`,
`formula = "C15 H19 N3 O2"`, `formula_weight = 273.33`, with `rcsb_chem_comp_related`
pointing at DrugBank `DB14921` and CAS `1642288-47-8`.

| PDB | `XB2` | heavy chain UniProt | organism | method, res | chains | construct | matched apo in the same series |
| --- | :-: | --- | --- | --- | ---: | --- | --- |
| `9GZ2` | Y | `P12883` | Homo sapiens | EM 2.9 Å | 1 | motor domain, no fusion, 1 mutation | **`9GZ3`** — same day, same construct, residue-identical |
| `9GZ1` | Y | `P12883` | Homo sapiens heavy chain, *Mus musculus* light chains | EM 3.7 Å | 6 | interacting-heads motif, no fusion | none — `9GZ3` is the motor domain, not the IHM |
| `9YP9` | Y | `P12883 + P03069 + P42212` | Homo sapiens / S. cerevisiae / A. victoria | EM 3.0 Å | 6 | **chimera**: Myosin-7–GCN4–EGFP, mouse light chains, 4 mutations | `9YRG` (3.2 Å) is the series apo but pairs with `9YR7` |
| `9YR7` | Y | `P12883 + P03069 + P42212` | Homo sapiens / S. cerevisiae / A. victoria | EM 3.0 Å | 6 | **chimera**: Myosin-7–GCN4–EGFP, mouse light chains, 4 mutations | **`9YRG`** — same day, same chimera, ADP·PO4, no `XB2` |
| `8QYR` | Y | `Q9BE39` | **Bos taurus** | X-ray 1.8 Å | 1 | motor domain, ADP·`BEF`·Mg | `8QYP` 2.759 Å — but ADP·**VO4**·Mg, and `P 43 2 2` not `P 21 21 21` |
| `8QYQ` | Y | `Q9BE39` | **Bos taurus** | X-ray 2.61 Å | 4 | S1 fragment, two light chains, ADP·`BEF`·Mg | `8QYP` — same mismatch, 1 chain against 4 |

All six contain `XB2`. Only `9GZ2`, `9GZ1`, `9YP9` and `9YR7` have a human heavy chain
(`P12883`); `8QYR` and `8QYQ` are `Q9BE39`, *Bos taurus*. Only `9YP9` and `9YR7` are chimeric
— their entity 1 aligns to three UniProt accessions, `P12883` plus GCN4 `P03069` plus EGFP
`P42212`, with `rcsb_mutation_count = 4` at author positions 1055, 1118, 1119 and 1285.
`9GZ1`, `9YP9` and `9YR7` are six-chain assemblies whose light chains are *Mus musculus*
(`P05977`, `P97457`), so "human" is true of the heavy chain and not of the particle.

**Ligand density.** Only the two X-ray entries carry one. `8QYQ` `XB2` RSCC 0.983 and 0.98,
`8QYR` 0.915. Every cryo-EM `XB2` returns `null` for RSCC and RSR — the report bin is
`all,em` and no density fit is computed. `9GZ1` chain B's `XB2` records 9 intermolecular
clashes; every other copy records 0.

**Ranked recommendation.**

1. **`9GZ2` — take this one.** It is the only candidate that is human `P12883`, non-chimeric,
   single-chain, and paired with an apo that matches it residue for residue. `9GZ3` and `9GZ2`
   both model 764 of 1145 residues, both carry the identical unmodelled set
   (2–2, 203–213, 625–643, 797–1146), both were deposited 2024-10-03 and released 2025-03-12, and both hold
   Mg·ADP·PO4. The only difference in the non-polymer list is `XB2`. For an apo/holo benchmark
   that is the whole requirement, and no other candidate meets it. Δres is 0.5 Å (3.4 → 2.9),
   which exceeds the 0.3 Å guidance and must be disclosed. It is also the organisers' own
   sanctioned substitution.
2. **`9YR7` with `9YRG`.** The second-best *pair*: same deposition day, same chimera, 3.0 vs
   3.2 Å (Δ 0.2 Å, inside the guidance), ADP·PO4 on both sides, differing by `XB2`. It loses
   to `9GZ2` on construct purity — a GCN4 coiled-coil and an EGFP are fused into the heavy
   chain, and the light chains are mouse — which puts non-human, non-myosin residues into the
   node set. Worth keeping as a robustness arm because it is the folded-back interacting-heads
   state, which is what `5TBY` was reaching for.
3. **`8QYR`.** The best-resolved mavacamten structure at 1.80 Å with the best-validated pose
   outside `8QYQ`, and single-chain. Rejected as primary because the heavy chain is bovine
   `Q9BE39`, and because its series apo `8QYP` is not state-matched: `8QYP` holds
   ADP·`VO4`·Mg (vanadate) against `8QYR`'s ADP·`BEF`·Mg (beryllium trifluoride), sits in
   `P 43 2 2` against `P 21 21 21`, and is 2.759 Å
   against 1.80 Å — a 0.96 Å gap.
4. **`9GZ1`.** Human heavy chain in the IHM at 3.7 Å, but no apo of the same assembly exists in
   the series and one `XB2` copy clashes 9 times.
5. **`8QYQ`.** Best `XB2` density in the set (RSCC 0.983) and worst fit to a resolution rule:
   2.61 Å X-ray fails a 2.5 Å ceiling. Bovine, four chains, one of which (`D`) models only 85
   of 199 residues.
6. **`9YP9`.** Same chimera as `9YR7` in the S2-FH *docked* state. Its natural apo partner is
   still `9YRG`, which is the *undocked* state, so the pair is not conformation-matched.

This confirms the freeze already in the repository: `cardiac_myosin_corrected` = `9GZ3` → `9GZ2`.

### (c) `5TBY` — everything measurable

| field | value | source |
| --- | --- | --- |
| title | HUMAN BETA CARDIAC HEAVY MEROMYOSIN INTERACTING-HEADS MOTIF OBTAINED BY HOMOLOGY MODELING (USING SWISS-MODEL) OF HUMAN SEQUENCE FROM APHONOPELMA HOMOLOGY MODEL (PDB-3JBH), RIGIDLY FITTED TO HUMAN BETA-CARDIAC NEGATIVELY STAINED THICK FILAMENT 3D-RECONSTRUCTION (EMD-2240) | `struct.title` |
| method | EM / ELECTRON MICROSCOPY | `rcsb_entry_info.experimental_method` |
| `structure_determination_methodology` | **experimental** | `rcsb_entry_info` |
| resolution | 20.0 Å | `rcsb_entry_info.resolution_combined[0]` |
| map resolution / criterion | 20.0 Å, FSC 0.5 CUT-OFF | `em_3d_reconstruction[0]` |
| EMDB | EMD-2240 | `rcsb_entry_container_identifiers.emdb_ids` |
| reconstruction / aggregation | SINGLE PARTICLE / FILAMENT | `em_experiment` |
| particles | 10700 | `em_3d_reconstruction[0].num_particles` |
| refinement statistics | **none** | `refine` absent from the API; present in the mmCIF with all values `?` except `entry_id`, `pdbx_refine_id`, `ls_d_res_high = 20.00` |
| entities | 3 polymer, 0 non-polymer, 0 branched | `rcsb_entry_info` |
| chains | 6 (A,B Myosin-7 `P12883`; C,D MYL3 `P08590`; E,F MYL2 `P10916`) | `polymer_entity/*` |
| assembly 1 | hexameric, A2 B2 C2 | `assembly/5TBY/1` |
| clashscore | **51.3**, absolute percentile 1.7, relative 1.7 | validation report `<Entry clashscore>` |
| Ramachandran outliers | 5.96 %, absolute percentile 2.0 | `percent-rama-outliers` |
| sidechain outliers | 1.96 %, absolute percentile 47.7 | `percent-rota-outliers` |
| RSRZ | — (cryo-EM, no EDS) | `percentilebins = "all,em"` |
| `covale` records | **41**, 1.083–1.644 Å, mean 1.422 Å | `_struct_conn` in `5TBY.cif` |
| HETATM records | 0 | deposited coordinate file |

**`em_software`, in full.** Thirteen rows, of which three name a program:
- `PARTICLE SELECTION` → EMAN 2
- `MODEL FITTING` → UCSF Chimera 10
- `RECONSTRUCTION` → ITERATIVE HELICAL REAL SPACE RECONSTRUCTION (EGELMAN, 2000) SPIDER 14

The remaining ten rows — `IMAGE ACQUISITION`, `MASKING`, `CTF CORRECTION`, `LAYERLINE
INDEXING`, `DIFFRACTION INDEXING`, `OTHER`, `MODEL REFINEMENT`, `INITIAL EULER ASSIGNMENT`,
`FINAL EULER ASSIGNMENT`, `CLASSIFICATION` — carry a category and a null name. **There is no
`MODEL REFINEMENT` program.** The model was placed by UCSF Chimera 10 and never refined:
`em_3d_fitting[0].ref_protocol = "RIGID BODY FIT"`, `target_criteria = "CORRELATION
COEFFICIENT"`, and `em_3d_fitting_list` names `3JBH` chains A–F as the fitted source, itself
recorded in `pdbx_initial_refinement_model` as `accession_code 3JBH`.

**The `covale` records.** All 41 are between side-chain or main-chain atoms of two *protein*
chains — there are no heteroatoms to bond to. Every distance is between 1.083 and 1.644 Å,
where a C–C single bond is 1.54 Å and a C–N is 1.47 Å. Examples:

| record | partners | distance (Å) |
| --- | --- | ---: |
| `covale1` | A/GLN454.CG – B/TYR410.CE2 | 1.083 |
| `covale13` | A/LYS803.CD – E/PRO108.CA | 1.093 |
| `covale3` | A/ARG723.NH2 – C/ARG138.NH2 | 1.188 |
| `covale4` | A/HIS760.CE1 – B/ASP376.CG | 1.200 |
| `covale10` | A/ILE788.CD1 – C/PHE133.CD1 | 1.643 |

These are not chemistry. They are the annotation pipeline's reading of atoms that overlap
because two rigid bodies were docked into a 20 Å envelope without refinement. The count and
the distance range are the cleanest single measurement of what `5TBY` is.

**One more thing the entry says about itself.** `em_specimen[0].details` reads *"A 6 ul
aliquot of native purified tarantula thick filaments suspension (Hidalgo et al. 2001)."* and
records `staining_applied = "NO"`, `vitrification_applied = "YES"`. The title says the model
was fitted to a *human* beta-cardiac *negatively stained* reconstruction. The entry's own
specimen record and its own title describe different experiments. Both are deposited fields;
neither is inferred here.

**`structure_determination_methodology` is `experimental`.**
The repository already warns against calling `5TBY` "not experimental" on that basis, and
that warning holds. Argue from 20 Å, no refinement statistics, no model-refinement program,
a rigid-body fit, 41 impossible bonds and a 1.7th-percentile clashscore.

### (d) `6C1H` — organism, accessions, ligands

**Confirmed.** It is rabbit actin plus rat myosin-Ib plus calmodulin, with no mavacamten.

| entity | description | chains | organism (taxid) | UniProt |
| :-: | --- | --- | --- | --- |
| 1 | Actin, alpha skeletal muscle | A,B,C,D,E | Oryctolagus cuniculus (9986) | `P68135` |
| 2 | Unconventional myosin-Ib | P | Rattus norvegicus (10116) | `Q05096` |
| 3 | Calmodulin | R | unidentified (32644) | `P0DP23` |

Non-polymer contents, complete: `ADP` (ADENOSINE-5'-DIPHOSPHATE) × 5 on chains A,B,C,D,E; `MG` (MAGNESIUM ION) × 5 on chains A,B,C,D,E.

`rcsb_entry_info.nonpolymer_bound_components` is `ADP, MG`. There is no `XB2`, no `P12883`, and no MYH7 sequence of
any species. Both ADP and Mg sit on the five actin chains A–E, not on the myosin chain P.
The shorthand "rat/rabbit myosin-Ib" is half right: the **myosin** is rat
(`Q05096`, taxid 10116); the **actin** is rabbit (`P68135`, taxid 9986). Calmodulin `P0DP23`
is deposited with `scientific_name = "unidentified"`, taxid 32644 — RCSB carries no organism
for it, and that is a `null`-equivalent, not an omission on our side.

Every chain is modelled complete: 375/375 on each of A–E, 729/729 on P, 148/148 on R, with no
unmodelled range anywhere. `6C1H` is a clean structure of the wrong protein.

### (e) Which entries fail "X-ray ≤ 2.5 Å or cryo-EM ≤ 4.0 Å"

| PDB | set | method | res (Å) | ceiling | margin |
| --- | --- | --- | ---: | ---: | ---: |
| `1OPL` | primary apo | X-ray | 3.42 | 2.5 | +0.92 |
| `5TBY` | primary apo | EM | 20.0 | 4.0 | +16.00 |
| `8QYQ` | myosin alternative | X-ray | 2.61 | 2.5 | +0.11 |

**3 of the 33 fail.** Of the two supporting entries outside the 33, `8QYP`
(2.759 Å X-ray) would also fail and `9YRG` (3.2 Å EM) would pass. Nothing else is close: the next
worst X-ray entry is `1QUV` at exactly 2.50 Å, which passes, and the next worst cryo-EM is
`6C1H` at 3.9 Å.

Two of the three failures are load-bearing. `1OPL` is the mandated BCR-ABL1 apo and `5TBY` is
the mandated cardiac-myosin apo. `8QYQ` is only a myosin alternative and is not used.

### (f) Resolution difference and space group, per apo/holo pair

| arm | apo | holo | Δres (Å) | > 0.3 Å | apo space group | holo space group | same? |
| --- | --- | --- | ---: | :-: | --- | --- | :-: |
| `kras_g12c_mandated` | `4OBE` X-ray 1.24 | `6OIM` X-ray 1.65 | 0.41 | **yes** | C 1 2 1 | P 21 21 21 | **no** |
| `kras_g12c_corrected` | `4LDJ` X-ray 1.15 | `6OIM` X-ray 1.65 | 0.5 | **yes** | P 21 21 21 | P 21 21 21 | yes |
| `bcr_abl1_mandated` | `1OPL` X-ray 3.42 | `5MO4` X-ray 2.17 | 1.25 | **yes** | C 2 2 21 | C 2 2 21 | yes |
| `bcr_abl1_corrected` | `2G2H` X-ray 2.0 | `5MO4` X-ray 2.17 | 0.17 | no | P 21 21 2 | C 2 2 21 | **no** |
| cardiac myosin, as written | `5TBY` EM 20.0 | `6C1H` EM 3.9 | 16.1 | **yes** | — | — | n/a |
| `cardiac_myosin_corrected` | `9GZ3` EM 3.4 | `9GZ2` EM 2.9 | 0.5 | **yes** | — | — | n/a |
| `mkp5` | `1ZZW` X-ray 1.6 | `7UMV` X-ray 1.8 | 0.2 | no | P 1 | P 64 | **no** |
| `chk1` | `1IA8` X-ray 1.7 | `3JVR` X-ray 1.76 | 0.06 | no | P 1 21 1 | P 1 21 1 | yes |
| `ptp1b` | `1SUG` X-ray 1.95 | `1T48` X-ray 2.2 | 0.25 | no | P 31 2 1 | P 31 2 1 | yes |
| `smyd3` | `6P7Z` X-ray 1.19 | `7BJ1` X-ray 1.61 | 0.42 | **yes** | P 21 21 21 | P 21 21 21 | yes |
| `glucokinase` | `3IDH` X-ray 2.14 | `3F9M` X-ray 1.5 | 0.64 | **yes** | P 21 21 21 | P 21 21 21 | yes |
| `hiv_rt` | `1RTJ` X-ray 2.35 | `1VRT` X-ray 2.2 | 0.15 | no | P 21 21 21 | P 21 21 21 | yes |
| `ns5b` | `1QUV` X-ray 2.5 | `2BRK` X-ray 2.3 | 0.2 | no | P 43 21 2 | P 21 21 2 | **no** |
| `p97_vcp` | `5FTK` EM 2.4 | `5FTJ` EM 2.3 | 0.1 | no | — | — | n/a |
| `ecoli_cps` | `1A9X` X-ray 1.8 | `1T36` X-ray 2.1 | 0.3 | no | P 21 21 21 | P 21 21 21 | yes |

**Over 0.3 Å: 7 of 15 pairs** — cardiac myosin, as written (16.1), `bcr_abl1_mandated` (1.25), `glucokinase` (0.64), `kras_g12c_corrected` (0.5), `cardiac_myosin_corrected` (0.5), `smyd3` (0.42), `kras_g12c_mandated` (0.41).
`ecoli_cps` lands on exactly 0.30 and is counted as *at* the limit, not over it.

**Different space groups: 4 of the 11 pairs that have one** — `kras_g12c_mandated`, `bcr_abl1_corrected`, `mkp5`, `ns5b`. The four cryo-EM pairs have no space group.

**A caution on "same space group".** `bcr_abl1_mandated` shares `C 2 2 21` across `1OPL` and
`5MO4`, but the cells are 77.0 × 273.4 × 124.4 Å against 118.3 × 124.1 × 74.7 Å. Same symmetry,
entirely different lattice. Matching the Hermann–Mauguin symbol is necessary and nowhere near
sufficient; the cells are in Table A and should be read with it. The pairs that genuinely share
a lattice are `chk1`, `ptp1b`, `smyd3`, `glucokinase` and `ecoli_cps`, whose cell edges agree to
under 1 %.

---

## 9. Discrepancies against what the repository currently records

Five. Two are stale numbers, one is a wrong word, one is a count that does not hold, and one
is a live conflict between two wwPDB partner APIs that the repository resolved the wrong way.
Everything else the repository states about these accessions is reproduced exactly by today's
RCSB — including the §4a resolution and space-group table, `6OIM` `MOV` RSCC 0.908, `5MO4`
`AY7` RSCC 0.946, `4OBE` residue 12 being glycine with `rcsb_mutation_count = 0`, `5TBY`'s 954
modelled residues in chain A and its 41 `covale` records, the `9GZ3`/`9GZ2` construct match,
and mavacamten appearing in exactly six PDB entries.

### D1 — `1OPL` RSRZ outliers: 6.50 %, not 22.18 %

**Repository:** `docs/targets.md` line 100. "`1OPL` quality: 3.42 Å, R-free 0.315, **22.18 %
RSRZ outliers**, which is the **0.4th absolute percentile** of the PDB", sourced to
`ebi.ac.uk/pdbe/api/validation/global-percentiles/entry/1opl`, and adding: "**A 2026-08-21
correction to 6.50 % was itself the error**". Repeated at
`docs/benchmark/secondary/README.md` line 212.

**Live wwPDB validation report served by RCSB**, `1opl_validation.xml.gz`,
`XMLcreationDate="Mar 20, 2026"`, `PDB-revision-number="5"`:

| attribute | value |
| --- | ---: |
| `percent-RSRZ-outliers` | **6.50** |
| `absolute-percentile-percent-RSRZ-outliers` | 24.6 |
| `relative-percentile-percent-RSRZ-outliers` | 19.3 |
| `clashscore` | 11.29 (abs 20.1) |
| `percent-rota-outliers` | 2.95 (abs 36.0) |
| `DCC_Rfree` | 0.2905 (abs 8.4) |

The same numbers appear in the Data API at `pdbx_vrpt_summary_diffraction[0].percent_RSRZ_outliers = 6.5`.

**The PDBe endpoint still returns the old run.** Fetched today and saved to
`data/rcsb-raw/1OPL/pdbe-global-percentiles.json`: `percent-RSRZ-outliers` `rawvalue 22.18`,
`absolute 0.4`, `relative 0.6`. But it also returns `clashscore 9.91` and
`percent-rota-outliers 2.39`, against 11.29 and 2.95 in the RCSB-served report. Those differ
too, so this is not a single stale field — the two partners are serving **different validation
runs of the same entry**. It is not one number being right and the other wrong.

**What to change.** `docs/targets.md` asserts that the 6.50 % figure was an error and gives a
mechanism ("a percentile read as a percentage"). That assertion cannot stand: 6.50 is what the
wwPDB report for revision 5 says, and its percentile is a separate attribute reading 24.6. The
honest record is that two wwPDB sources disagree, that RCSB's report is the newer of the two,
and that `1OPL` is a poor structure either way — 3.42 Å, R-free 0.315, `DCC_Rfree` at the 8.4th
absolute percentile. The argument for demoting `1OPL` never rested on the RSRZ number and does
not need it.

### D2 — `5TBY` clashscore: 51.3 at the 1.7th percentile, not 49.95 at the 2.2nd

**Repository:** `docs/targets.md` line 129, "Clashscore 49.95 (2.2nd percentile)".

**Live:** the validation report created 2026-03-09 gives `clashscore="51.3"`,
`absolute-percentile-clashscore="1.7"`,
`relative-percentile-clashscore="1.7"`. The Data API agrees:
`pdbx_vrpt_summary_geometry[0].clashscore = 51.3`.

A re-run moved the number. The direction is against `5TBY`, so no conclusion changes, but the
quoted value is stale. `percent-rama-outliers` is now
5.96 % at the 2.0th absolute percentile,
which the repository does not quote and which is the worse of the two.

### D3 — `5MO4` does **not** model auth 83–531 continuously

**Repository:** `docs/targets.md` line 97, "`5MO4` is **not** kinase-domain-only. It models
auth 83–531 continuously — SH3, SH2 and kinase, the same architecture as `1OPL`."

**Live:** the span is right, the word "continuously" is wrong.

| source | result |
| --- | --- |
| `polymer_entity_instance/5MO4/A` → `rcsb_polymer_instance_feature[UNOBSERVED_RESIDUE_XYZ]` | 429 of 495 modelled; unmodelled auth 40–82, **296–297**, **402–419**, 532–534 |
| deposited `5MO4.pdb`, distinct `ATOM` residue numbers | 429 residues, span 83–531, internal breaks at (296, 297) and (402, 419) |

Twenty residues inside the span are unmodelled, including an eighteen-residue block at
402–419. The architecture claim survives — SH3, SH2 and kinase are all present — but a holo
with an 18-residue hole is a holo that cannot contribute those residues to a pocket lining.
`5MO4` is the holo for **both** BCR-ABL1 arms, so this belongs in the label-accounting record
rather than in a parenthesis.

### D4 — the secondary set's space-group count

**Repository:** `docs/benchmark/primary/README.md` line 307,
"the other six are 0.06–0.25 Å and share a space group in five of six".

**Live:** of the six secondary arms under the 0.3 Å line, **three** share a space group.

| arm | Δres (Å) | apo SG | holo SG | same? |
| --- | ---: | --- | --- | :-: |
| `mkp5` | 0.2 | P 1 | P 64 | **no** |
| `chk1` | 0.06 | P 1 21 1 | P 1 21 1 | yes |
| `ptp1b` | 0.25 | P 31 2 1 | P 31 2 1 | yes |
| `hiv_rt` | 0.15 | P 21 21 21 | P 21 21 21 | yes |
| `ns5b` | 0.2 | P 43 21 2 | P 21 21 2 | **no** |
| `p97_vcp` | 0.1 | — (cryo-EM) | — (cryo-EM) | n/a |

`mkp5` moves from triclinic `P 1` to hexagonal `P 64`; `ns5b` from `P 43 21 2` to `P 21 21 2`.
`p97_vcp` is a cryo-EM pair and has no space group on either side, so "six" only ever had five
candidates. The corrected sentence is: three of the five crystallographic pairs share a space
group, and the sixth pair is cryo-EM.

### D5 — `5TBY`'s source map resolution is recorded by RCSB as 20 Å, not 28 Å

**Repository:** `docs/targets.md` line 127, "the entry records 20 Å and its source map
`EMD-2240` is 28 Å (Alamo 2017)".

**Live:** RCSB carries one resolution for this entry and it is 20.0 Å —
`rcsb_entry_info.resolution_combined[0] = 20.0`, `em_3d_reconstruction[0].resolution = 20.0`
with `resolution_method = "FSC 0.5 CUT-OFF"`, and the validation report's
`percentilebins="all,em"` with `PDB-resolution` 20.0. **RCSB records no 28 Å value anywhere**,
for this entry or for `EMD-2240` through `pdbx_database_related`. The 28 Å figure is a
literature value and is not refuted here; it is flagged because the sentence reads as though
both numbers come from the deposition, and only one does.

---

## 10. Things this table makes newly checkable

Not discrepancies. Facts nobody in the repository had written down.

1. **Four X-ray entries have no released structure factors.** `1IA8`, `1RTJ`, `1A9X` and
   `1VRT` all carry `has_released_experimental_data = "N"`, so they have no RSRZ, no EDS
   R-factor and no per-ligand RSCC. That covers **both halves** of the `hiv_rt` arm and the
   apo of `chk1` and `ecoli_cps`. Any statement of the form "the ligand is well ordered" is
   unverifiable on those four.
2. **`1RTJ` and `1QUV` are the geometrically worst crystal structures in either benchmark.**
   `1RTJ`: clashscore 32.13 (2.8th percentile), 3.12 % Ramachandran outliers (3.0th),
   18.37 % sidechain outliers (1.5th). `1QUV`: clashscore 27.95 (3.8th), 24.84 % sidechain
   outliers (**0.5th**). Both are secondary apo inputs. Resolution passed them; geometry
   would not have.
3. **The cryo-EM entries are geometrically split.** `9GZ3` (clashscore 1.54, 91.8th) and
   `9GZ2` (1.78, 89.2nd) are excellent. `5FTJ` (40.89, 2.6th), `5FTK` (25.17, 6.4th) and
   `5TBY` (51.3, 1.7th) are not. The `p97_vcp` arm's 2.3–2.4 Å map resolution says nothing
   about its model geometry.
4. **`8QYQ` chain D models 85 of 199 residues.** The bovine S1 fragment's second light chain
   is unmodelled across auth 1–79 and 103–128. If that entry is ever used, chain D is not a
   usable graph.
5. **`6C1H` has no unmodelled residue anywhere** — 375/375 on each of five actin chains,
   729/729 on myosin-Ib, 148/148 on calmodulin. It is a well-built structure of a protein
   this project does not study.
6. **`1T36` is the only entry at major version 2**; every other accession is still at major
   version 1, with minor revisions from 1-0 (`9GZ3`) to 1-9 (`5TBY`).

