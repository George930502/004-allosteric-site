# Forensic structural audit — KRAS G12C (apo `4OBE` → holo `6OIM`)

> **Status: superseded in part, retained as the forensic record.** This dossier is the
> 2026-08-20 audit that produced ADR 0003 and the tiered benchmark. It is preserved because
> the *evidence* it gathered is what the tiers rest on, and every fact in it carries its
> provenance. But it predates **ADR 0007** (ground truth is the allosteric site; crypticity is
> a difficulty axis, never a validity test) and **ADR 0008** (one target per site), so its
> framing and some of its recommendations are no longer current.
> **For anything you intend to rely on, `docs/benchmark/frozen.json` is the authority and
> `docs/benchmark/README.md` is the current account.** Points where this file has been
> overtaken are marked `⚠️ SUPERSEDED` inline.

**Audit date:** 2026-08-20
**Pair source:** `CHALLENGE.md` §6 Table 1; mirrored in `docs/targets.md`.
**Target pocket:** cryptic Switch-II pocket (S-IIP), bound by sotorasib / AMG 510.

Every number below was derived programmatically. Nothing is stated from recall.


**Endpoints used**

| Endpoint | Used for |
|---|---|
| `https://data.rcsb.org/rest/v1/core/entry/{id}` | method, resolution, R-factors, dates, citation, entity ids |
| `https://data.rcsb.org/rest/v1/core/chemcomp/MOV` | ligand identity, synonyms, PubChem CID |
| `https://data.rcsb.org/graphql` | batch metadata for all 490 X-ray KRAS entries |
| `https://search.rcsb.org/rcsbsearch/v2/query` | entry search on UniProt `P01116` |
| `https://files.rcsb.org/download/{id}.cif` | all coordinate and metadata categories |
| `https://files.rcsb.org/download/{id}.pdb` | `REMARK 290 SMTRY` symmetry operators only |
| `https://files.rcsb.org/pub/pdb/validation_reports/{mid}/{id}/{id}_validation.xml.gz` | wwPDB percentile ranks |
| `https://www.ebi.ac.uk/pdbe/api/mappings/{id}` | SIFTS UniProt residue-level mapping |
| `https://rest.uniprot.org/uniprotkb/P01116.json` | canonical sequence, feature annotations |
| `https://api.crossref.org/works/{doi}` | DOI verification |

Local mmCIF copies: `data/raw/{4OBE,6OIM,4LDJ,4L8G,4LRW,8TVK,7A1X}.cif` (gitignored).
Contact definition throughout: **protein heavy atom within 4.5 Å of any ligand heavy atom**,
computed from `_atom_site.Cartn_x/y/z`, hydrogens excluded via `_atom_site.type_symbol`.

**Could not reach:** `ebi.ac.uk/europepmc` returned HTTP 503 for the whole audit, so literature
residue ranges for the switch regions are *not* asserted anywhere in this document.

---

## 1. Entry

| Field | `4OBE` (apo) | `6OIM` (holo) | Source field |
|---|---|---|---|
| Title | Crystal Structure of **GDP-bound Human KRas** | Crystal Structure of human **KRAS G12C covalently bound to AMG 510** | `_struct.title` |
| Method | X-RAY DIFFRACTION | X-RAY DIFFRACTION | `_exptl.method` |
| Resolution | **1.24 Å** | **1.65 Å** | `_refine.ls_d_res_high` |
| R-work | 0.1566 | 0.18092 | `_refine.ls_R_factor_R_work` |
| R-free | 0.1686 | 0.21519 | `_refine.ls_R_factor_R_free` |
| Deposited | 2014-01-07 | 2019-04-09 | `rcsb_accession_info.deposit_date` |
| Released | 2014-06-04 | 2019-11-06 | `rcsb_accession_info.initial_release_date` |
| Last revised | 2023-09-20 | 2024-11-13 | `rcsb_accession_info.revision_date` |
| Space group | C 1 2 1 | P 21 21 21 | `_symmetry.space_group_name_H-M` |
| Cell (a,b,c / α,β,γ) | 66.147, 42.096, 114.393 / 90, 105.32, 90 | 40.868, 58.417, 65.884 / 90, 90, 90 | `_cell.*` |

**Primary citations** (`_citation`, DOIs re-verified against `api.crossref.org`):

- `4OBE` — Hunter *et al.*, *PNAS* 111:8895–8900 (2014). "In situ selectivity profiling and crystal
  structure of SML-8-73-1, an active site inhibitor of oncogenic K-Ras G12C."
  DOI `10.1073/pnas.1404639111`, PMID 24889603.
- `6OIM` — Canon *et al.*, *Nature* 575:217–223 (2019). "The clinical KRAS(G12C) inhibitor AMG 510
  drives anti-tumour immunity." DOI `10.1038/s41586-019-1694-1`, PMID 31666701.

**wwPDB validation percentile ranks** (from `{id}_validation.xml`, `<Entry>` attributes; absolute /
relative-to-resolution):

| Metric | `4OBE` value | `4OBE` abs / rel | `6OIM` value | `6OIM` abs / rel |
|---|---|---|---|---|
| Clashscore | 1.11 | 95.7 / 86.1 | 1.46 | 92.6 / 89.4 |
| Ramachandran outliers | 0.00 % | 100.0 / 100.0 | 0.00 % | 100.0 / 100.0 |
| Sidechain (rotamer) outliers | 0.00 % | 100.0 / 100.0 | 0.00 % | 100.0 / 100.0 |
| RSRZ outliers | 2.95 % | 53.5 / 54.7 | 2.40 % | 59.5 / 64.7 |
| R-free (DCC) | 0.1560 | 97.6 / 82.0 | 0.2201 | 68.5 / 43.5 |

Both entries are structurally sound. One flag: `4OBE` xtriage reports **pseudo-translational
symmetry** — an off-origin Patterson peak at 39.81 % of the origin peak (`TransNCS` attribute);
data completeness 94.02 %.

---

## 2. Composition

### `4OBE`

| Entity | Type | Copies | Description | Chains |
|---|---|---|---|---|
| 1 | polymer | 2 | GTPase KRas | auth `A`,`B` = label `A`,`B` |
| 2 | non-polymer | 2 | GDP, `C10 H15 N5 O11 P2` | label `C`(auth A 201), `E`(auth B 201) |
| 3 | non-polymer | 2 | MG, `Mg 2` | label `D`(auth A 202), `F`(auth B 202) |
| 4 | water | 355 | HOH | label `G`,`H` |

Source organism *Homo sapiens* (taxid 9606), gene `KRAS, KRAS2, RASK2`, expressed in
*Escherichia coli* (`_entity_src_gen`). UniProt **`P01116`** (`RASK_HUMAN`), `_struct_ref`.
Sample sequence length **170**.

### `6OIM`

| Entity | Type | Copies | Description | Chain |
|---|---|---|---|---|
| 1 | polymer | 1 | GTPase KRas | auth `A` = label `A` |
| 2 | non-polymer | 1 | MG, `Mg 2` | label `B`, auth A 301 |
| 3 | non-polymer | 1 | GDP, `C10 H15 N5 O11 P2` | label `C`, auth A 302 |
| 4 | non-polymer | 1 | **MOV**, "AMG 510 (bound form)", `C30 H32 F2 N6 O3`, 562.61 Da | label `D`, auth A 303 |
| 5 | water | 207 | HOH | label `E` |

Same organism, gene, host and UniProt accession. Sample sequence length **183** (includes tag).

**Ligand identity was read from the file, not assumed.** `_chem_comp.name` for `MOV` is
"AMG 510 (bound form)"; `core/chemcomp/MOV` gives the systematic name
*6-fluoro-7-(2-fluoro-6-hydroxyphenyl)-4-[(2S)-2-methyl-4-propanoylpiperazin-1-yl]-1-[4-methyl-2-(propan-2-yl)pyridin-3-yl]pyrido[2,3-d]pyrimidin-2(1H)-one*
and PubChem CID 145946085. Note "**bound form**": the acrylamide warhead has already reacted, so
`C30 H32 F2 N6 O3` is the post-Michael-addition adduct, not free sotorasib.

---

## 3. Construct and mutations

### `4OBE` — `_struct_ref_seq_dif`, **2 rows**

| Chain | auth | label_seq | PDB res | UniProt res | Details |
|---|---|---|---|---|---|
| A | 0 | 1 | GLY | — | expression tag |
| B | 0 | 1 | GLY | — | expression tag |

**There is no mutation row.** Cross-checked at the coordinate level:
`_atom_site.label_comp_id` where `auth_seq_id == 12` is **GLY** in both chains A and B.
RCSB's own `entity_poly.rcsb_mutation_count` for this entity is **0**.
Residues 51, 80 and 118 are **CYS / CYS / CYS** — the native cysteines are all retained.
UniProt `P01116` canonical residue 12 is `G` (`rest.uniprot.org/uniprotkb/P01116.json`,
`sequence.value[11]`).

> ### `4OBE` is **wild-type KRAS**. It is not the G12C mutant.

### `6OIM` — `_struct_ref_seq_dif`, **18 rows**

14 rows are the N-terminal tag: auth `-13`..`0`, sequence `MKHHHHHHHDEVDG`
(row 1 `details` = "initiating methionine", rows 2–14 = "expression tag").

The 4 substantive rows:

| Chain | auth | label_seq | PDB res | UniProt res | Details |
|---|---|---|---|---|---|
| A | **12** | 26 | **CYS** | GLY | variant |
| A | 51 | 65 | SER | CYS | engineered mutation |
| A | 80 | 94 | LEU | CYS | engineered mutation |
| A | 118 | 132 | SER | CYS | engineered mutation |

Coordinate cross-check: auth 12 = `CYS`, 51 = `SER`, 80 = `LEU`, 118 = `SER`.

> ### `6OIM` **is** G12C — on a **cysteine-light** background (C51S / C80L / C118S).

**Differences between the two entries:** four positions — **12, 51, 80, 118** — plus a
14-residue N-terminal His tag present only in `6OIM`.

---

## 4. Numbering

| | `4OBE` | `6OIM` |
|---|---|---|
| `auth_seq_id` range, polymer | A: **1–169**; B: **0–169** | A: **0–104, 108–169** |
| `label_seq_id` → `auth_seq_id` | `auth = label − 1` (single offset, both chains) | `auth = label − 14` |
| Insertion codes | none (`_atom_site.pdbx_PDB_ins_code` all `?`) | none |
| `_struct_ref_seq` | seq_align 2–170 → auth 1–169 → UNP 1–169 | seq_align 15–183 → auth 1–169 → UNP 1–169 |
| SIFTS (`ebi.ac.uk/pdbe/api/mappings`) | chains A,B: PDB auth 1..169 → UniProt `P01116` 1..169 | chain A: PDB auth 1..169 → UniProt `P01116` 1..169 |

> ### Apo and holo residue numbering are **directly comparable. Offset = 0.**
> Both use UniProt `P01116` canonical numbering for auth residues 1–169. No insertion codes in
> either. The only numbering subtlety is the `label_seq_id` offset, which differs (−1 vs −14)
> because of the different tag lengths — never join on `label_seq_id`.

---

## 5. Completeness

Switch regions are **not** taken from memory:

- **Switch I** ≡ UniProt `P01116` feature `Motif` / "Effector region", residues **32–40**
  (`rest.uniprot.org/uniprotkb/P01116.json` → `features[]`).
- **Switch II** — operational, derived from the deposited secondary structure of the two files:
  the first residue after the end of β3 through the end of α2.
  `_struct_sheet_range` strand 2 = **49–57** (identical in both files).
  `_struct_conf` `HELX_P2` = **TYR64–GLY75** in `4OBE`, **SER65–THR74** in `6OIM`.
  Analysis window used: **57–76**.
  The switch concept is attributable to Milburn *et al.*, *Science* 1990,
  DOI `10.1126/science.2406906`, and the switch-II pocket to Ostrem *et al.*, *Nature* 2013,
  DOI `10.1038/nature12796` (both DOIs verified via CrossRef) — **their exact residue ranges are
  not asserted here**, because Europe PMC was unreachable during the audit.

### `4OBE` (`_pdbx_unobs_or_zero_occ_residues`, 1 row)

| Chain | Missing | Note |
|---|---|---|
| A | `GLY 0` | N-terminal expression-tag Gly |
| B | — | complete, 0–169 |

Missing side-chain atoms (`_pdbx_unobs_or_zero_occ_atoms`, 24 atoms): `GLN43` (CG,CD,OE1,NE2),
`GLU107` (CG,CD,OE1,OE2), `LYS169` (CG,CD,CE,NZ) — the same three in each chain.

Alternate conformations: **0 residues** (`_atom_site.label_alt_id` is `.` throughout).
Partial-occupancy polymer residues: **0**.

**Switch I and Switch II are fully modelled in both chains.**

### `6OIM` (`_pdbx_unobs_or_zero_occ_residues`, 16 rows)

| Chain | Missing | Note |
|---|---|---|
| A | auth `-13`..`-1` (13 res, `MKHHHHHHHDEVD`) | N-terminal His tag |
| A | auth `105–107` (`ASP105`, `SER106`, `GLU107`) | loop C-terminal to α3 |

No missing side-chain atoms, 0 altloc residues, 0 partial occupancies.

**Switch I and Switch II are fully modelled.** The 105–107 break lies outside both switches and
outside the 21-residue pocket set, so the label set is unaffected.

---

## 6. Ligands and the blindness question

### Every non-polymer component of `4OBE`, contacts at 4.5 Å

| Ligand | Contacts | Residues (auth) |
|---|---|---|
| `GDP` A201 | 19 | 11, 12, 13, 14, 15, 16, 17, 18, 28, 29, 30, 32, 116, 117, 119, 120, 145, 146, 147 |
| `MG` A202 | 6 | 17, 32, 33, 34, 36, 57 |
| `GDP` B201 | 19 | identical to chain A |
| `MG` B202 | 6 | identical to chain A |

Nearest approaches for `GDP` A201: `GLY13` 2.82 Å, `LYS16` 2.78 Å, `ALA18` 2.85 Å, `ASP119` 2.86 Å,
`ALA146` 2.78 Å — the canonical P-loop / NKxD / SAK nucleotide site.

**Nucleotide state:** `4OBE` carries **GDP + Mg²⁺**, two copies of each. It is *not*
nucleotide-free. `_struct_conn` has **12 `metalc` rows and 0 `covale` rows**: Mg²⁺ is coordinated
by `SER17.OG` (2.085 Å), `GDP.O1B` (2.053 Å) and four waters, per chain.

> ### Is `4OBE` genuinely free of ligand in the Switch-II pocket? **Yes.**
>
> The intersection of the GDP + Mg²⁺ contact sets with the 21-residue holo pocket set is
> `{11, 12, 13, 16, 34}` — all P-loop residues that the nucleotide site and the S-IIP rim share.
> The pocket proper — **58–63, 68, 69, 72, 95, 96, 99, 100, 103** — contacts **no ligand at all**.

**And the pocket is genuinely closed.** Superposing each `4OBE` chain onto `6OIM` chain A on the
166 common Cα atoms (Kabsch), then applying the inverse transform to the 41 `MOV` heavy atoms:

| | clashes < 1.0 Å | < 2.0 Å | < 2.5 Å | < 3.0 Å | closest contacts |
|---|---|---|---|---|---|
| `4OBE` A | 2 | 5 | 13 | 20 | `MET72.CE` 0.74, `HIS95.CD2` 0.91, `ARG68.CD` 1.55 |
| `4OBE` B | 2 | 6 | 12 | 20 | `MET72.CE` 0.65, `HIS95.CD2` 0.82, `ARG68.CD` 1.54 |

Met72, His95 and Arg68 occupy the volume the drug takes. Only 6 (chain A) / 4 (chain B) ordered
waters fall within 1.5 Å of the transplanted ligand. **This is the correct behaviour for a
cryptic-site benchmark** — no geometric cavity detector can find the site in the apo input, so the
prediction is genuinely blind, and a classical pocket-finding baseline should score near zero.

### `6OIM`

| Ligand | Contacts | Residues (auth) |
|---|---|---|
| `MG` A301 | 5 | 17, 33, 34, 57, 58 |
| `GDP` A302 | 18 | 11, 12, 13, 14, 15, 16, 17, 18, 28, 30, 32, 116, 117, 119, 120, 145, 146, 147 |
| **`MOV` A303** | **21** | **9, 10, 11, 12, 13, 16, 34, 58, 59, 60, 61, 62, 63, 68, 69, 72, 95, 96, 99, 100, 103** |

**Ground-truth S-IIP label set at 4.5 Å**, with minimum distances:

`VAL9` 3.45 · `GLY10` 3.50 · `ALA11` 4.28 · **`CYS12` 1.81** · `GLY13` 4.32 · `LYS16` 2.77 ·
`PRO34` 3.48 · `THR58` 3.94 · `ALA59` 3.15 · `GLY60` 3.16 · `GLN61` 3.52 · `GLU62` 3.63 ·
`GLU63` 3.22 · `ARG68` 3.16 · `ASP69` 4.28 · `MET72` 3.28 · `HIS95` 3.55 · `TYR96` 3.27 ·
`GLN99` 3.51 · `ILE100` 4.14 · `VAL103` 3.36

Independent cross-check: the depositors' own `_struct_site` `AC3` ("binding site for residue MOV A
303") declares `pdbx_num_residues = 21`. Our count matches exactly.

**Covalent link — confirmed, not assumed.** `_struct_conn` contains exactly one `covale` row:

```
covale1   covale   A/CYS12.SG  --  A/MOV303.C25   pdbx_dist_value = 1.805
```

`CYS12` Sγ to `MOV` C25 at **1.805 Å**. Plus 6 `metalc` rows for the Mg²⁺ site.

---

## 7. Assembly

| | `4OBE` | `6OIM` |
|---|---|---|
| Protein copies in ASU | **2** (chains A, B) | **1** (chain A) |
| Deposited assemblies | **2**, both `monomeric`, count 1 | **1**, `monomeric`, count 1 |
| Assembly composition | `1` = A,C,D,G · `2` = B,E,F,H | `1` = A,B,C,D,E |
| Method | PISA | PISA |

The biological unit is a **monomer** in both. The two `4OBE` chains are crystallographic copies,
**not** a biological dimer.

**Do the copies differ?** Barely. Chain A vs chain B, Kabsch on 169 common Cα: **RMSD 0.346 Å**.
Mean Cα deviation over Switch I (30–40) = 0.26 Å; over Switch II (57–76) = **0.10 Å**. Largest
single deviation is residue 121 at 2.28 Å. **The pocket is closed in both copies** — there is no
"one copy open, one closed" heterogeneity to exploit.

---

## 8. Modifications

Neither entry has any. `_pdbx_struct_mod_residue`: **absent from both files**.
`_entity_poly.nstd_monomer` = `no` in both. `_chem_comp` lists no modified amino acids — the only
non-standard components are `GDP`, `MG`, `HOH` (both) and `MOV` (`6OIM` only), all HETATM in
separate `label_asym_id`s outside the polymer chain. No selenomethionine, no PTMs, no HETATM inside
a polymer chain.

---

## 9. Apo ↔ holo comparability

**Sequence identity** — `Bio.Align.PairwiseAligner`, global, BLOSUM62, gap open −11 / extend −1,
on `_entity_poly.pdbx_seq_one_letter_code_can`:

- `4OBE` length 170, `6OIM` length 183
- 170 ungapped aligned columns, **166 identities → 97.65 %**
- 13-column gap = the `6OIM` His tag
- **4 mismatches**, all accounted for: `G12C`, `C51S`, `C80L`, `C118S`

| Question | Answer |
|---|---|
| Same species? | Yes — *Homo sapiens*, taxid 9606, both |
| Same UniProt accession? | Yes — `P01116` |
| Same isoform region? | Yes — both cover UniProt 1–169, identical between KRAS4A and KRAS4B |
| Same construct? | **No** — 4 substitutions + a His tag |
| Numbering comparable? | Yes, offset 0 |
| Residue-range overlap | 166 common auth residues in 1–169 |

**Pocket-residue mapping — all 21 holo pocket residues have a counterpart in the apo model:**

| | Count |
|---|---|
| Present in apo (`4OBE` chain A) | **21 / 21** |
| Identical residue type | **20 / 21** |
| Different residue type | **1** — auth 12: holo `CYS`, apo `GLY` |
| Absent | 0 |

**Superposition** (Kabsch, 166 common Cα, auth 1–169):

| | `4OBE` A → `6OIM` A | `4OBE` B → `6OIM` A |
|---|---|---|
| Overall Cα RMSD | **1.362 Å** | **1.267 Å** |
| Mean dev, Switch I (30–40) | 0.73 Å | 0.51 Å |
| Mean dev, **Switch II (57–76)** | **2.48 Å** (max 8.79) | **2.48 Å** (max 8.64) |
| Mean dev, α2 (60–74) | 3.10 Å | 3.11 Å |
| Mean dev, α3 (87–104) | 0.78 Å | 0.75 Å |
| Mean dev, core (excl. 25–45, 55–80) | 0.70 Å | 0.58 Å |

The conformational change on drug binding is **local and confined to Switch II**: the core moves
0.6–0.7 Å while residue 63 moves **8.79 Å**. Switch I is essentially unchanged. This is precisely
the signal a propagation method is supposed to recover.

---

## 10. Pipeline-breakers, most severe first

### 1 — `4OBE` is wild-type KRAS, not G12C. **(high)**

*Evidence.* `_struct_ref_seq_dif` in `data/raw/4OBE.cif` has exactly 2 rows, both "expression tag"
`GLY` at auth 0; no mutation row exists. `_atom_site.label_comp_id` at `auth_seq_id == 12` is `GLY`
in chains A and B. `_struct.title` is "Crystal Structure of GDP-bound Human KRas". RCSB reports
mutation count 0. UniProt `P01116` residue 12 is `G`.

*Mechanism of failure.* The ground-truth label set derived from `6OIM` contains `CYS12`, the
covalent anchor (Sγ–C25 at 1.805 Å) and the closest contact in the whole pocket. That residue does
not exist in the prediction input. Scoring residue 12 as a hit target scores a residue the model
never saw in its oncogenic form. More fundamentally, the G12C mutation is *the* biological reason
this pocket is druggable, so the apo input is not the apo form of the protein whose pocket we are
predicting.

### 2 — Four construct differences, three of them engineered cysteine removals. **(high)**

*Evidence.* Global alignment: 166/170 identities; mismatches at auth 12 (G/C), 51 (C/S), 80 (C/L),
118 (C/S). `6OIM` `_struct_ref_seq_dif` labels 51, 80 and 118 "engineered mutation".

*Mechanism of failure.* A contact network is built from side-chain and backbone geometry. C51S,
C80L and C118S change side-chain volume at three buried or semi-buried positions, so the apo
network and the holo network are not networks of the same molecule. C80L sits on the α3 face
beneath the S-IIP floor. Effect size is probably small, but it is currently **unquantified**, and
"probably small" is not evidence (R3).

### 3 — Switch II in `4OBE` is lattice-contacted and anomalously rigid. **(medium)**

*Evidence.* Symmetry expansion using the `REMARK 290 SMTRY` operators over unit-cell translations
−1..+1: **10 of the 21** pocket residues (34, 59, 60, 61, 62, 63, 68, 69, 99, 103) lie within
4.5 Å of a symmetry mate. Closest partners: `TYR137` 2.58 Å, `HIS94` 2.59 Å, `ARG102` 2.69 Å,
`ASP33` 2.86 Å, `LYS101` 2.93 Å. Mean B over auth 57–76 is **13.1** against a chain mean of 18.5
(**ratio 0.71**; chain B 0.68). For comparison, `6OIM` has **0 of 21** in crystal contact and a B
ratio of **1.18**; `4LDJ` has 2 of 21 and 0.92.

*Mechanism of failure.* The prediction path derives dynamics from topology (C6). If the apo
switch-II conformation is held by the lattice, the contact network encodes lattice-stabilised
geometry rather than solution-state flexibility, and any method ranking residues by predicted
mobility or dynamic connectivity will systematically **under-rank the very region it must find**.
Residue 63 — the largest apo/holo Cα deviation at 8.79 Å — is itself in crystal contact.

*Caveat.* `8TVK` has the same 10 contacts but a normal B ratio (0.95), so the crystal contacts do
not by themselves explain the depressed B-factors. The two observations co-occur in `4OBE`;
causation is not established.

### 4 — Two ASU copies but a monomeric biological assembly; plus pseudo-translational symmetry. **(medium-low)**

*Evidence.* `_entity.pdbx_number_of_molecules` = 2 for entity 1; two `_pdbx_struct_assembly` rows,
both `monomeric`. Chain A vs B Cα RMSD 0.346 Å, Switch II deviation 0.10 Å. Validation xtriage:
off-origin Patterson peak at 39.81 % of origin.

*Mechanism of failure.* Naive loading of the whole ASU builds a 338-node two-molecule network
instead of a 169-node monomer, doubling the graph and adding spurious inter-copy edges. The copies
are effectively identical, so nothing is gained. Silently wrong if unhandled; trivially fixed by
selecting a chain explicitly and recording the choice.

### 5 — Neither structure is nucleotide-free. **(low)**

*Evidence.* `4OBE` entities 2–3: GDP ×2, MG ×2. `6OIM` entities 2–3: MG ×1, GDP ×1. Mg²⁺
coordinated by `SER17.OG`, the GDP β-phosphate and four waters in both.

*Mechanism.* Not a defect — the nucleotide is physiological and the S-IIP is a separate site. But
"apo" here means **drug-free, not ligand-free**. Under C5 the nucleotide and Mg²⁺ must be either
dropped or modelled as simple nodes, and the choice recorded, because GDP contacts 19 residues
including S-IIP rim residues 11, 12, 13 and 16.

### 6 — `6OIM` has a 3-residue chain break at 105–107 that `4OBE` does not. **(low)**

*Evidence.* `_pdbx_unobs_or_zero_occ_residues` rows 14–16: `ASP105`, `SER106`, `GLU107`.

*Mechanism.* Relevant only if a network is also built on the holo structure. The break is outside
both switch regions and outside the 21-residue pocket set, so the label set is unaffected.

### 7 — The apo pocket is genuinely closed. **(informational — a property to preserve)**

Transplanted `MOV` clashes at 0.74 Å with `MET72.CE` and 0.91 Å with `HIS95.CD2`; 20 protein atoms
within 3.0 Å. This confirms a true cryptic-site problem and justifies a dynamics-based method over
a geometric one. Record it as the reason the classical baseline is expected to fail.

---

## Better-suited alternative entries

**Search method.** RCSB search API on UniProt `P01116` + `exptl.method = X-RAY DIFFRACTION` → **490
entries**. Batch GraphQL for sequence, `rcsb_polymer_entity_align.aligned_regions` (to read residue
12 through the true alignment rather than by assuming an offset) and non-polymer chem comps.
"Drug-like" = a non-polymer component that is neither a guanine nucleotide nor a common ion/buffer
and has formula weight > 200 Da. Residue-12 distribution across the 490 entries:
`G` 147, `D` 127, **`C` 122**, `V` 63, `R` 11, `A` 7, `S` 5, `N` 1. **16** apo G12C candidates.

### Recommended apo replacement: **`4LDJ`**

"Crystal Structure of a GDP-bound G12C Oncogenic Mutant of Human GTPase KRas"

| Property | `4LDJ` | `4OBE` (current) |
|---|---|---|
| Residue 12 | **CYS** | GLY |
| Mutations | `GLY12CYS` (engineered mutation) — only | none |
| Resolution | **1.15 Å** | 1.24 Å |
| R-work / R-free | **0.1318 / 0.1622** | 0.1566 / 0.1686 |
| Chains in ASU | **1** | 2 |
| Observed range | **0–169, no gaps** | A 1–169, B 0–169 |
| Altloc residues | 0 | 0 |
| Ligands | GDP + Mg²⁺ | GDP + Mg²⁺ |
| S-IIP residues missing | **0 / 21** | 0 / 21 |
| S-IIP residues in crystal contact | **2 / 21** (63, 69) | 10 / 21 |
| Switch II B / mean B | **0.92** | 0.71 |
| Pocket cryptic? | **Yes** — transplanted MOV: 8 atoms < 2.0 Å, 25 < 3.0 Å; `HIS95.CD2` 0.76, `MET72.CE` 0.80, `CYS12.SG` 1.40 | Yes |
| Cα RMSD to `6OIM` A | 1.220 Å | 1.362 Å |

**Why it is the right choice.** Same group, **same paper** (DOI `10.1073/pnas.1404639111`),
**released the same day** as `4OBE` (2014-06-04). Decisively: `4OBE`'s own
`_pdbx_database_related` record names `4LDJ` with `details = "G12C Kras"` — the depositors
themselves flag `4LDJ` as the G12C structure and `4OBE` as its wild-type companion. It is the
structure the challenge almost certainly meant.

**Tradeoff.** Only one of the four construct differences is removed: `4LDJ` still retains native
C51/C80/C118 whereas `6OIM` is cysteine-light. And it departs from the literal challenge text,
which names `4OBE`.

### Other candidates examined

| PDB | Res. | Verdict | Reason |
|---|---|---|---|
| `8TVK` | 1.04 Å | usable | Highest-resolution apo G12C found (R-free 0.2048, 1 chain, 1–169 no gaps, pocket cryptic). But **10 / 21** pocket residues in crystal contact — does not fix breaker 3. B ratio 0.95. Part of a multi-temperature series (`8TXK` 240 K, `8TXJ` 277 K, `8TY2` 293 K, `8TY8` 310 K, `8TY9` 313 K) that would make an interesting robustness set; each member needs its own check. |
| `4LRW` | 2.15 Å | **reject** | The *only* apo entry whose construct exactly matches `6OIM` (G12C + C51S + C80L + C118S) — it would fix breaker 2. But switch II residues 60–70 are unobserved, so **6 of the 21 pocket residues (60, 61, 62, 63, 68, 69) have no coordinates** and cannot enter a contact network. |
| `4L8G` | 1.52 Å | **reject** | Same defect: switch II 60–69 disordered, 6 of 21 pocket residues absent. |
| `7A1X` | 1.32 Å | **reject** | Carries fragment `QWB` (3-(imidazol-1-ylmethyl)-1H-indole). Its 4.5 Å contact set is {5, 6, 7, 37, 39, 54, 55, 56, 71, 74, 75} — **zero overlap** with the S-IIP set, so it is not an S-IIP occupancy problem, but it is still a bound small molecule in the prediction input. |

### Holo side: **no replacement needed**

`6OIM` is 1.65 Å, R-free 0.2152, all validation percentiles at or above median, single chain,
monomeric assembly, **zero** crystal contacts at the pocket, both switches fully modelled, the
covalent Cys12 link explicit in `_struct_conn`, and an unambiguous ligand chem comp. Our 21-residue
4.5 Å contact set matches the depositors' own `_struct_site AC3` count exactly.

---

## Verdict

> ## Usable with documented caveats — but a substitution is strongly recommended.

⚠️ **SUPERSEDED — read "blindness" here as clause (iii) _site-apo_, not as the benchmark's
`blind` field.** Under the settled vocabulary (`CONTEXT.md`) KRAS is **not blind**: ASBench
curates the HRAS helix-3/loop-7 site whose residues are 4 of 5 in our label set, and Eren 2021
ran GNM+ANM on `4OBE` itself. What this paragraph correctly establishes is the narrower,
still-true point that follows.

The site-apo requirement is **satisfied**: the Switch-II pocket in `4OBE` is genuinely closed and
genuinely ligand-free, and the numbering is directly comparable to `6OIM` with zero offset. No holo
information leaks into the apo input (C1 is safe).

The problem is not leakage — it is **target identity**. `4OBE` is wild-type KRAS. The challenge's
own apo/holo pair is not two forms of the same protein, and the single most important residue in
the ground-truth pocket (`CYS12`, the covalent anchor at 1.81 Å) does not exist in the prediction
input.

**If `4OBE` is kept as-is** (the challenge text fixes it, so it must be reported):

1. State plainly in the report that `4OBE` is wild-type KRAS. Evidence: `_struct_ref_seq_dif` has
   no mutation row; auth residue 12 is `GLY`.
2. ⚠️ **SUPERSEDED by the scoreable-label rule (ADR 0007).** Residue 12 leaves the scored set,
   but by *set membership* — it is an active-site residue under the frozen rule, along with 11,
   13, 16 and 34 — not by this ad-hoc exclusion. Original wording: exclude residue 12, or score it separately — its holo identity does
   not exist in the apo input.
3. Use **chain A only**; record the choice. Do not load both ASU copies.
4. Record the treatment of GDP and Mg²⁺ under C5 (dropped, or simple nodes).
5. Report the switch-II crystal-contact exposure (10 of 21 residues, B ratio 0.71) as a stated
   limitation of the apo input.

**Recommended action.** Run **`4LDJ`** as the primary apo input and keep `4OBE` as a documented
control. Report both. `4LDJ` is the same paper, the same deposition day, higher resolution, lower
R-free, one chain, no gaps, far less lattice contact at the pocket — and it is actually G12C.
Because the challenge text fixes `4OBE`, the `4OBE` result must still be reported; the `4LDJ`
result is the scientifically defensible one, and **the delta between them is itself a result worth
writing up** (it is a direct measurement of how much the oncogenic mutation and the lattice
environment perturb the predicted ranking).

**Constraint impact**

| Constraint | Status |
|---|---|
| C1 (apo only) | **Satisfied.** No holo-derived information in `4OBE`; S-IIP closed and unoccupied. |
| C5 (scope) | ✅ **Resolved in ADR 0006**: cofactors are not network nodes; the apo entry's own cofactor may locate the propagation source (ADR 0005). |
| C6 (elastic network) | **Weakened for `4OBE`** by the lattice contacts on switch II. Note as a limitation. |

---

## Could not determine

- Whether the organisers intended `4LDJ` and mistyped `4OBE`, or deliberately chose a wild-type
  apo input. Not derivable from any primary source.
- The quantitative effect of the C51S / C80L / C118S construct difference on a contact network.
  Requires an experiment (build both networks, compare rankings) — not answerable from metadata.
- Verbatim literature residue ranges for Switch I and Switch II: `ebi.ac.uk/europepmc` returned
  HTTP 503 throughout the audit. The ranges used here come from UniProt `P01116` annotations and
  from the `_struct_conf` / `_struct_sheet_range` records of the two files themselves.
- Whether the depressed switch-II B-factors in `4OBE` are *caused* by the crystal contacts. The two
  co-occur, but `8TVK` has the same 10 contacts with a normal B ratio (0.95), so the correlation is
  not established.
