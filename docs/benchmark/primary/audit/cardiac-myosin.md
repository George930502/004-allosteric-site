# Benchmark audit — Cardiac myosin (`5TBY` apo → `6C1H` holo)

> **Status: superseded in part, retained as the forensic record.** This dossier is the
> 2026-08-20 audit that produced ADR 0003 and the tiered benchmark. It is preserved because
> the *evidence* it gathered is what the tiers rest on, and every fact in it carries its
> provenance. But it predates **ADR 0007** (ground truth is the allosteric site; crypticity is
> a difficulty axis, never a validity test) and **ADR 0008** (one target per site), so its
> framing and some of its recommendations are no longer current.
> **For anything you intend to rely on, `docs/benchmark/primary/frozen.json` is the authority and
> `docs/benchmark/primary/README.md` is the current account.** Points where this file has been
> overtaken are marked `⚠️ SUPERSEDED` inline.

**Verdict up front: UNUSABLE.** `6C1H` does **not** contain mavacamten. It does not contain
cardiac myosin. It is a rat **unconventional myosin-Ib** motor bound to a rabbit skeletal
**actin** filament with **calmodulin**; its only ligands are five ADP and five Mg²⁺, all of
them in the actin nucleotide clefts. The challenge's designated ground truth for this target
does not exist in the file it names.

Audit date **2026-08-20**. Every number below carries the endpoint or the mmCIF field that
produced it. Nothing here is recalled. Reproduce with the scripts named in §Provenance.

Assignment under audit: `CHALLENGE.md` §6 Table 1, row "Cardiac Myosin (Cardiology)" —
apo `5TBY`, holo `6C1H`, objective *"Identify the mechanical site where Mavacamten
stabilizes the 'super-relaxed state'"*. Mirrored in `docs/targets.md`.

---

## 1. Entry

| | `5TBY` | `6C1H` |
|---|---|---|
| Title (`_struct.title`) | HUMAN BETA CARDIAC HEAVY MEROMYOSIN INTERACTING-HEADS MOTIF OBTAINED BY HOMOLOGY MODELING (USING SWISS-MODEL) OF HUMAN SEQUENCE FROM APHONOPELMA HOMOLOGY MODEL (PDB-3JBH), RIGIDLY FITTED TO HUMAN BETA-CARDIAC NEGATIVELY STAINED THICK FILAMENT 3D-RECONSTRUCTION (EMD-2240) | High-Resolution Cryo-EM Structures of Actin-bound Myosin States Reveal the Mechanism of Myosin Force Sensing |
| Method (`_exptl.method`) | ELECTRON MICROSCOPY | ELECTRON MICROSCOPY |
| Resolution (`_em_3d_reconstruction.resolution`) | **20.0 Å** (`resolution_method` = FSC 0.5 CUT-OFF) | **3.9 Å** (FSC 0.143 CUT-OFF) |
| `_refine.ls_d_res_high` | 20.00 | `.` |
| R-work / R-free | **not applicable** — cryo-EM, no `_refine.ls_R_factor_*` in file | **not applicable** |
| Particles / symmetry | 10 700 particles, POINT symmetry, aggregation FILAMENT, single particle | 62 000 particles, HELICAL symmetry, aggregation HELICAL ARRAY |
| Microscope | FEI/PHILIPS CM120T; `_em_ctf_correction.type = NONE` | FEI TITAN KRIOS; PHENIX model refinement |
| Deposited | 2016-09-13 | 2018-01-04 |
| Released | **2017-06-07** | **2018-01-31** |
| Last revised | 2024-10-23 | 2025-05-28 |
| Primary citation | Alamo *et al.*, *eLife* **6** (2017), "Effects of myosin variants on interacting-heads motif explain distinct hypertrophic and dilated cardiomyopathy phenotypes." DOI **10.7554/eLife.24634**, PMID 28606303 | Mentes A, Huehn A, Liu X, Zwolak A, Dominguez R, Shuman H, Ostap EM, Sindelar CV, *PNAS* **115**:1292–1297 (2018), "High-resolution cryo-EM structures of actin-bound myosin states reveal the mechanism of myosin force sensing." DOI **10.1073/pnas.1718316115**, PMID 29358376 |
| Related EM volumes (`_pdbx_database_related`) | EMD-2240 (associated), EMD-1950 (other), PDB 3JBH | EMD-7331 (associated), EMD-7329, EMD-7330 |

The `6C1H` primary citation title contains no mention of cardiac myosin, of mavacamten, or of
the super-relaxed state. It is a paper about **myosin-I force sensing on actin filaments**.

### wwPDB validation percentiles

Source `https://www.ebi.ac.uk/pdbe/api/validation/global-percentiles/entry/{id}` and
`https://data.rcsb.org/rest/v1/core/entry/{id}` → `pdbx_vrpt_summary_geometry`,
`pdbx_vrpt_summary_em`.

| metric | `5TBY` raw | `5TBY` absolute %ile | `6C1H` raw | `6C1H` absolute %ile |
|---|---|---|---|---|
| clashscore | **49.95** | **2.2** | 6.00 | 49.9 |
| % Ramachandran outliers | **5.96** | **2.8** | 0.04 | 100.0 |
| % rotamer outliers | 2.05 | 57.2 | 1.06 | 74.4 |
| bonds RMSZ / angles RMSZ | 0.85 / 1.35 | — | 0.23 / 0.57 | — |
| EM Q-score | **0.032** | — | 0.32 | — |
| atom inclusion (backbone) | 0.783 | — | 0.962 | — |
| PDBe overall quality percentile | **3.62** | — | 69.0 | — |

`5TBY` sits in the bottom ~3 % of the PDB on both clashes and backbone geometry.

---

## 2. Composition

### `5TBY` — three polymer entities, zero non-polymer entities

| entity | description | UniProt | organism | SEQRES len | auth chains |
|---|---|---|---|---|---|
| 1 | Myosin-7 (β-cardiac myosin heavy chain, MYH7) | P12883 | *Homo sapiens* | 1935 | A, B |
| 2 | Myosin light chain 3 (**ELC**, MYL3) | P08590 | *Homo sapiens* | 195 | C, D |
| 3 | Myosin regulatory light chain 2, ventricular (**RLC**, MYL2) | P10916 | *Homo sapiens* | 166 | E, F |

**ELC and RLC are both present, both human, two copies each.** The construct is a
**two-headed interacting-heads motif (IHM)** built on an S1-length heavy chain: `SEQRES`
declares full-length MYH7 (1935 aa) but only residues 6–959 / 10–959 are modelled, i.e. motor
domain plus lever arm. **No S2 coiled coil is modelled**, so despite "heavy meromyosin" in
the title the coordinates are 2 × S1 + 4 light chains, not an HMM.

**Non-polymer entities: none.** `rcsb_entry_info.nonpolymer_entity_count = 0`;
`grep -c '^HETATM' data/raw/5TBY.cif` → **0**. Waters: **0**
(`deposited_solvent_atom_count = 0`).

Modelled residues (distinct `auth_seq_id` with ≥1 `ATOM` record):

| chain | entity | n | auth range |
|---|---|---|---|
| A | 1 | 954 | 6–959 |
| B | 1 | 950 | 10–959 |
| C | 2 | 152 | 44–195 |
| D | 2 | 152 | 44–195 |
| E | 3 | 160 | 7–166 |
| F | 3 | 160 | 7–166 |
| **total** | | **2528** | |

Matches `rcsb_entry_info.deposited_modeled_polymer_monomer_count = 2528` exactly.
Deposited atoms 20 357. **Coarse-graining budget for this entry: 2528 nodes**, or 954 for a
single motor+lever-arm head, or 1266 for one head with its two light chains.

### `6C1H` — three polymer entities, two non-polymer entities

| entity | description | UniProt | organism | SEQRES len | auth chains |
|---|---|---|---|---|---|
| 1 | Actin, alpha skeletal muscle | P68135 | *Oryctolagus cuniculus* (rabbit) | 375 | A, B, C, D, E |
| 2 | **Unconventional myosin-Ib** | **Q05096** | ***Rattus norvegicus*** | 729 | P |
| 3 | Calmodulin | P0DP23 (via SIFTS; `_struct_ref` in file gives `PDB 6C1H`, no UniProt) | recorded as "unidentified", taxid 32644 | 148 | R |

**ELC and RLC are absent.** There is no MYL3 and no MYL2 in this entry. The light chain
present is **calmodulin**, the class-I myosin light chain. This is neither a myosin-II S1 nor
an HMM nor an IHM: it is a **class-I myosin motor + one IQ/CaM, decorating a five-subunit
F-actin segment**.

Non-polymer entities (`/core/nonpolymer_entity/6C1H/{4,5}` and `/core/chemcomp/{id}`):

| chem comp | resolved name | formula | MW | count | on auth chains |
|---|---|---|---|---|---|
| `ADP` | ADENOSINE-5'-DIPHOSPHATE | C10 H15 N5 O10 P2 | 427.201 | 5 | A, B, C, D, E |
| `MG` | MAGNESIUM ION | Mg | 24.305 | 5 | A, B, C, D, E |

Waters: **0**. `HETATM` atom census: 135 ADP atoms + 5 MG atoms, nothing else.
**Every ligand copy sits on an actin subunit. Chain P (the myosin) and chain R (calmodulin)
carry no ligand at all.**

Modelled residues:

| chain | entity | n | auth range |
|---|---|---|---|
| A–E | 1 (actin) | 375 each | 1–375 |
| P | 2 (Myo1b) | 729 | 6–734 |
| R | 3 (CaM) | 148 | 1–148 |
| **total** | | **2752** | |

Matches `deposited_modeled_polymer_monomer_count = 2752`. Deposited atoms 20 966.
`deposited_unmodeled_polymer_monomer_count = 0` — every SEQRES residue is modelled.

---

## 3. Construct and mutations

**`5TBY` — `_struct_ref_seq_dif`: no rows.** No engineered mutations, no expression tags, no
chimera, no fusion partner. The sequence is wild-type human MYH7 / MYL3 / MYL2 verbatim.

That is expected, and it is the problem: the coordinates were not produced by expressing this
sequence. From the file itself —

- `_em_3d_fitting.ref_protocol = 'RIGID BODY FIT'`, `ref_space = REAL`,
  `target_criteria = 'CORRELATION COEFFICIENT'`.
- `_em_3d_fitting_list`: all six chains have `initial_refinement_model` = PDB **`3JBH`**,
  `type = 'experimental model'`, `accession_code 3JBH` — a **tarantula** myosin filament model.
- `_em_specimen.details` = *"A 6 ul aliquot of native purified **tarantula** thick filaments
  suspension (Hidalgo et al. 2001)."*
- `_em_entity_assembly.name` = `MYOSIN THICK FILAMENTS TARANTULA STRIATED MUSCLE`;
  `_em_entity_assembly_naturalsource`: organism **Aphonopelma**, taxid 6896, organ LEG,
  organelle THICK FILAMENTS, cellular location SARCOPLASM.
- `_citation` ids 4, 5, 6 are the three **SWISS-MODEL** methods papers (PMIDs 9504803,
  12824332, 16301204).
- `_em_ctf_correction.type = NONE`.

So the human sequence enters this deposition **only through comparative modelling**. Every
side-chain rotamer in `5TBY` is a SWISS-MODEL prediction templated on *Aphonopelma*, placed by
rigid-body correlation into a 20 Å envelope. **No residue-level experimental information about
human β-cardiac myosin is present in these coordinates.**

Metadata inconsistency worth recording, unresolved from the file: the title says the model was
fitted to a *negatively stained human* reconstruction (EMD-2240), while
`_em_specimen.staining_applied = NO`, `vitrification_applied = YES`, and the whole `_em_*`
block describes the *tarantula cryo-EM* experiment. Both statements are in the same file; the
audit cannot decide which map the deposited coordinates were actually fitted to.

**`6C1H` — `_struct_ref_seq_dif`: 6 rows**, all chain P, all `details = 'expression tag'`,
`db_mon_id = ?` (no UniProt counterpart):

| auth_seq_id | mon_id |
|---|---|
| 729 | GLY |
| 730 | LEU |
| 731 | ASN |
| 732 | ASP |
| 733 | ILE |
| 734 | PHE |

Chain P residues **6–728 are native rat Myo1b; 729–734 are a non-native C-terminal tag
remnant** and must be excluded from any network. No engineered point mutations. Calmodulin
(entity 3) is deposited without a UniProt reference (`_struct_ref.db_name = PDB`), so its
provenance rests on the SIFTS assignment to P0DP23.

---

## 4. Numbering

| entry | chain | auth range | `auth − label_seq` offset | SIFTS UniProt mapping | auth == UniProt canonical? |
|---|---|---|---|---|---|
| `5TBY` | A, B | 6–959 / 10–959 | **0** | P12883, auth 1–1935 ↔ UNP 1–1935, identity 1.0 | **yes** |
| `5TBY` | C, D | 44–195 | 0 | P08590 1–195 ↔ UNP 1–195 | yes |
| `5TBY` | E, F | 7–166 | 0 | P10916 1–166 ↔ UNP 1–166 | yes |
| `6C1H` | A–E | 1–375 | 0 | P68135, auth 1–375 ↔ **UNP 3–377** | **no — auth = UniProt − 2** |
| `6C1H` | P | 6–734 | **+5** | Q05096, auth 6–728 ↔ UNP 6–728, identity 0.99 | yes for 6–728; 729–734 have no UniProt counterpart |
| `6C1H` | R | 1–148 | 0 | P0DP23, auth 1–148 ↔ **UNP 2–149** | **no — auth = UniProt − 1** |

Insertion codes: **none** in either entry (`_atom_site.pdbx_PDB_ins_code` is `?` throughout).
Alternate conformations: **none** in either entry (`label_alt_id` is `.` for every atom in
both). Single model each (`pdbx_PDB_model_num = 1`).

### Are apo and holo residue numbering directly comparable?

**No, and no offset exists that would make them so.** The question is not a numbering
question — it is a protein-identity question.

- `5TBY` heavy chain = human MYH7 (P12883), class **II** myosin, 1935 aa.
- `6C1H` myosin chain = rat MYO1B (Q05096), class **I** myosin, 1136 aa full-length.

`Bio.Align.PairwiseAligner`, BLOSUM62, open −11 / extend −1, on
`_entity_poly.pdbx_seq_one_letter_code_can`:

| comparison | mode | aligned columns | identities | % identity |
|---|---|---|---|---|
| P12883 (5TBY e1) vs Q05096 (6C1H e2) | local | 692 | 274 | **39.6 %** |
| P12883 vs Q05096 | global | 713 | 291 | 40.8 % |
| P08590 ELC (5TBY e2) vs CaM (6C1H e3) | local | 140 | 66 | 47.1 % |
| P10916 RLC (5TBY e3) vs CaM (6C1H e3) | local | 137 | 54 | 39.4 % |

**Different species and different myosin class**, ~40 % identical over the motor domain —
that is the divergence of two distinct protein families sharing a fold, not two structures of
one target. `6C1H` additionally contains 1875 residues of rabbit skeletal actin with **no
counterpart whatsoever** in `5TBY`.

---

## 5. Completeness

**`5TBY`** — `_pdbx_unobs_or_zero_occ_residues`, as ranges:

| chain | unmodelled n | ranges |
|---|---|---|
| A | 981 | 1–5, 960–1935 |
| B | 985 | 1–9, 960–1935 |
| C | 43 | 1–43 |
| D | 43 | 1–43 |
| E | 6 | 1–6 |
| F | 6 | 1–6 |
| **total** | **2064** | |

**2064 of 4592 SEQRES residues (45 %) are unmodelled**, matching
`deposited_unmodeled_polymer_monomer_count = 2064`. The whole of S2 and LMM (960–1935 in both
heavy chains) is absent, as is the ELC N-terminal extension (1–43). Within the modelled range
there are **no internal gaps at all** — chains A, B, C, D, E, F are each one unbroken run.
That is itself diagnostic of a homology model: real 3.5 Å cryo-EM structures of this molecule
(`8ACT`, `9GZ2`) break at loop 1 (~129), loop 2 (~203–213) and the ~625–644 loop.

Alternate conformations: 0. Disordered loops of note: none inside 6–959, by construction.

**`6C1H`** — no `_pdbx_unobs_or_zero_occ_residues` category, and
`deposited_unmodeled_polymer_monomer_count = 0`. **Every SEQRES residue of every chain is
modelled.** Alternate conformations: 0.

---

## 6. Ligands — the critical section

### 6.1 Does `6C1H` contain mavacamten?

# NO.

Evidence, four independent derivations:

1. **Chem-comp identity.** Mavacamten's PDB chemical component ID is **`XB2`**
   (`/core/chemcomp/XB2` → `chem_comp.name = "Mavacamten"`, formula **C15 H19 N3 O2**,
   MW 273.33; synonyms include **MYK-461**; cross-refs DrugBank **DB14921**, CAS
   **1642288-47-8**, ChEMBL CHEMBL4297517, PubChem 117761397).
2. **Entity list.** `6C1H` has exactly two non-polymer entities,
   `/core/nonpolymer_entity/6C1H/4` → `ADP` and `/5` → `MG`. `XB2` is not among them.
3. **Coordinates.** `awk '$1=="HETATM"{print $6}' data/raw/6C1H.cif | sort | uniq -c` →
   `135 ADP`, `5 MG`. Nothing else. No `XB2` atom exists in the file.
4. **Search complement.** The RCSB structured search
   `rcsb_nonpolymer_entity_container_identifiers.nonpolymer_comp_id == "XB2"` returns
   **exactly 6 entries: `8QYQ`, `8QYR`, `9GZ1`, `9GZ2`, `9YP9`, `9YR7`.** `6C1H` is not one
   of them. (An RCSB full-text search for "mavacamten" returns 9 entries — the 6 above plus
   `8QYP`, `9GZ3`, `8QYU`, which are the drug-free / omecamtiv controls from the same two
   papers. `6C1H` is not in that list either.)

**What `6C1H` actually is**, per its own primary citation: Mentes *et al.*, *PNAS*
115:1292–1297 (2018), DOI 10.1073/pnas.1718316115 — a cryo-EM study of **actin-bound
myosin-Ib** and the structural basis of **myosin force sensing**. The entry is one of three
actomyosin reconstructions in that paper (`6C1D`, `6C1G`, `6C1H`). It contains **no cardiac
myosin, no myosin II, no mavacamten, and no drug of any kind.**

### 6.2 Contact residues for every non-polymer component

Computed from coordinates: all ligand heavy atoms vs all protein heavy atoms, `cKDTree`,
**4.5 Å** cutoff, auth numbering (`scratchpad/contacts.py`).

**`6C1H`, ADP (5 copies, chains A–E):** 17–19 residues per copy. Union of distinct residue
numbers, all on **actin**:

```
12 13 14 15 16 18 137 156 157 182 210 213 214 301 302 303 305 306 336 339
```

e.g. chain A: ASN12 GLY13 SER14 GLY15 LEU16 LYS18 GLN137 GLY156 ASP157 GLY182 ARG210 LYS213
GLU214 GLY302 THR303 MET305 TYR306 LYS336. This is the canonical **actin nucleotide cleft**
(P-loops at 13–16 and 156–157, the 301–306 strand, K336).

**`6C1H`, MG (5 copies, chains A–E):** 3–4 residues each — GLN137, GLY156, plus VAL339 or
GLY302 depending on copy. Also actin.

**Residues of the myosin (chain P) within 4.5 Å of any ligand: zero.** Minimum heavy-atom
distance from any ADP/Mg to chain P is **6.7 Å** (to the actin-B ADP, across the actomyosin
interface). Minimum distance to calmodulin (chain R) is **83.3 Å**.

Consequence: a mechanical "select protein residues within 4.5 Å of the holo ligand" rule —
exactly the procedure `docs/targets.md` mandates — applied to `6C1H` yields **20 rabbit actin
residues and not one myosin residue**.

**`5TBY`: no ligands of any kind.** No nucleotide (no ADP, ATP, ADP·VO₄, ADP·BeF₃), no
sulfate, no phosphate, no small molecule, no omecamtiv mecarbil (`2OW`), no blebbistatin, no
waters, no metals. `HETATM` count is literally 0. **Nothing in `5TBY` can bias a blind
prediction by ligand occupancy** — but see §11, because the absence is a consequence of the
entry being a homology model, not of the protein being ligand-free, and it removes the
obvious apo-only way to define the active site (the nucleotide pocket) as a propagation source.

### 6.3 Covalent links

**`6C1H`:** `_struct_conn` contains **15 records, all `metalc`** (Mg²⁺ coordination).
**Zero `covale`.** Clean.

**`5TBY`:** `_struct_conn` contains **41 records, all `conn_type_id = covale`**, and **all 41
are inter-chain** (A–B, A–C, A–E, A–F, B–D, B–F). Their actual interatomic distances,
measured from the coordinates: **min 1.08 Å, max 1.64 Å, mean 1.42 Å**.

These are not chemistry. Examples: `A GLN454 CG — B TYR410 CE2`, `A LYS803 CD — E PRO108 CB`,
`A ARG845 CZ — B ARG845 NE`, `A MET877 CG — B MET877 CE`. Side chains of **different
polypeptide chains are interpenetrating at bond length**, and the annotation pipeline recorded
the resulting sub-bonding distances as covalent links. This is the coordinate-level
manifestation of the clashscore-50 / 2nd-percentile validation result. It is concentrated
precisely at the **head–head and head–light-chain interfaces** — the interfaces the
super-relaxed-state hypothesis is about.

---

## 7. Assembly

**`5TBY`:** one assembly, `_pdbx_struct_assembly.details = author_defined_assembly`,
`oligomeric_details = hexameric`, `oligomeric_count = 6`. Generated from asyms A,B,C,D,E,F
with `oper_expression = 1` (identity) — the asymmetric unit *is* the biological assembly.
Stoichiometry **2 × MYH7 : 2 × MYL3 (ELC) : 2 × MYL2 (RLC)**.

Conformational state: **interacting-heads motif (IHM)**, named in `_struct.title` and in
`_struct_keywords.text` (`"Myosin interacting-heads motif"`), and the subject of the primary
citation (DOI 10.7554/eLife.24634) and of the deposited reference
`10.1016/j.jmb.2016.01.027`, *"Conserved Intramolecular Interactions Maintain Myosin
Interacting-Heads Motifs Explaining Tarantula Muscle Super-Relaxed State Structural Basis."*
So the *intent* of `5TBY` is exactly the SRX biology the challenge asks about — it is the holo
side, not the apo side, that is broken in the target's premise.

**`6C1H`:** one assembly, `author_defined_assembly`, `oligomeric_details = heptameric`,
`oligomeric_count = 7`, generated from all 17 asyms with `oper_expression = 1`. Stoichiometry
**5 × actin : 1 × Myo1b : 1 × calmodulin** (+ 5 ADP, 5 Mg).

Conformational state: the entry names none in a machine-readable field. Derived from
coordinates: **the Myo1b active site is empty** — no nucleotide on chain P, nearest ADP heavy
atom 6.7 Å away — whereas the sibling entry **`6C1D`** from the same paper carries `ADP` + `MG`
on its chain P. `6C1H` therefore models the **nucleotide-free, actin-bound (rigor-like)**
state. Recorded as unresolved: the associated map **EMD-7331** is titled *"Complex of actin,
myosin-1b, and calmodulin with ADP"*, which conflicts with the deposited coordinates for the
myosin (the five ADP present are all on actin). The audit reports the coordinates; it cannot
resolve the map annotation.

---

## 8. Modifications

**`5TBY`:** `_pdbx_struct_mod_residue` absent. Non-standard residues: none — the `ATOM`
records contain only the 20 standard amino acids. HETATM inside the polymer: none (there are
no HETATM records).

**`6C1H`:** `_pdbx_struct_mod_residue` absent. Non-standard residues: none. HETATM inside the
polymer: none — the ADP/Mg are separate entities in their own `label_asym_id`s
(H,I,J,K,L,M,N,O,P,Q), each given `auth_seq_id` 401/402 on the actin chains.

(For contrast, the recommended replacement `8ACT` *does* carry `M3L` — N-trimethyllysine — at
auth 129 and 549 in both heavy chains, listed in `_pdbx_struct_mod_residue`. Any replacement
pipeline must map `M3L` → LYS rather than dropping it.)

---

## 9. Apo ↔ holo comparability

| criterion | result |
|---|---|
| Same protein? | **No.** MYH7 (myosin class II) vs MYO1B (myosin class I) |
| Same species? | **No.** *Homo sapiens* vs *Rattus norvegicus* (myosin), *Oryctolagus cuniculus* (actin) |
| Same isoform? | **No** — different gene, different myosin class |
| Heavy-chain sequence identity | **39.6 %** local / 40.8 % global over 692–713 aligned columns (`Bio.Align.PairwiseAligner`, BLOSUM62, −11/−1) |
| Light chains | MYL3 + MYL2 (human ELC/RLC) vs calmodulin — 47.1 % / 39.4 % identity |
| Extra chains in holo with no apo counterpart | 5 × rabbit skeletal actin, 1875 residues |
| Residue-range overlap | Meaningless — the two numbering systems index different proteins |
| **Holo ligand-contact residues with a modelled counterpart in the apo entry** | **0 of 20.** All 20 are actin residues; `5TBY` contains no actin. |

There is nothing to align, nothing to transfer, and no label set to build.

---

## 10. Where the mavacamten site actually is

### 10.1 Every PDB entry containing mavacamten

Query: `rcsb_nonpolymer_entity_container_identifiers.nonpolymer_comp_id == "XB2"` at
`https://search.rcsb.org/rcsbsearch/v2/query`, return_type `entry`. **Total count 6.**

| PDB | method | res. (Å) | released | heavy-chain UniProt | **species** | β-cardiac? | title | primary DOI |
|---|---|---|---|---|---|---|---|---|
| **`8QYR`** | X-ray | **1.80** (R 0.187 / R-free 0.227) | 2023-12-13 | Q9BE39 | *Bos taurus* | yes | Beta-cardiac myosin motor domain in the pre-powerstroke state complexed to Mavacamten | 10.1101/2023.11.15.567213 (PMID 38014327) |
| **`8QYQ`** | X-ray | 2.61 (R 0.178 / R-free 0.217) | 2023-12-13 | Q9BE39 (+ P85100 ELC) | *Bos taurus* | yes | Beta-cardiac myosin S1 fragment in the pre-powerstroke state complexed to Mavacamten | 10.1101/2023.11.15.567213 |
| **`9GZ2`** | cryo-EM | 2.90 | 2025-03-12 | **P12883** | ***Homo sapiens*** | yes | Beta-cardiac heavy meromyosin motor domain in the primed state complexed to mavacamten | 10.1101/2025.02.12.637875 (PMID 39990378) |
| **`9GZ1`** | cryo-EM | 3.70 | 2025-03-12 | **P12883** (+ mouse P05977 ELC, P97457 RLC) | ***Homo sapiens*** (heavy chain) | yes | Beta-cardiac myosin **interacting heads motif** complexed to mavacamten | 10.1101/2025.02.12.637875 |
| **`9YP9`** | cryo-EM | 3.00 | 2026-04-08 | **P12883** fused to P03069 (GCN4) + P42212 (eGFP); mouse light chains | ***Homo sapiens*** (heavy chain) | yes | Human β-cardiac myosin + mavacamten, **IHM**, S2-FH **docked** | 10.1126/sciadv.aed6472 (PMID 42054467) |
| **`9YR7`** | cryo-EM | 3.00 | 2026-04-08 | as `9YP9` | ***Homo sapiens*** (heavy chain) | yes | Human β-cardiac myosin + mavacamten, **IHM**, S2-FH **undocked** | 10.1126/sciadv.aed6472 |

All six are β-cardiac myosin. Four have a **human** heavy chain (`9GZ1`, `9GZ2`, `9YP9`,
`9YR7`); two are **bovine** (`8QYQ`, `8QYR`). None is `6C1H`.

For `9YP9`/`9YR7` the GCN4 and eGFP fusion partners occupy auth 1017–1048 and 1055–1292 with a
`linker` at 1049–1054 and four `engineered mutation` rows (V1055M-rev, L1118F-rev, T1119S-rev,
L1285H-rev, per `_struct_ref_seq_dif`) — but the **modelled** range of chains A/B is only
**4–943**, i.e. the entire fusion is unmodelled and every modelled residue is native human
MYH7. `9GZ1`/`9GZ2` carry a `variant` S1124A and an 8-residue C-terminal expression tag at
1139–1146, both outside their modelled range (3–932 / 3–796).

### 10.2 The pocket, computed from coordinates

4.5 Å heavy-atom contacts to `XB2`, auth numbering. Every one of these entries numbers its
MYH7 heavy chain with `auth == UniProt canonical` (offset 0, verified from
`_struct_ref_seq`), so the numbers below are directly **P12883 canonical numbering**.

| entry | chain | contact residues |
|---|---|---|
| `8QYR` (1.8 Å, bovine) | B | L120 Q163 **Y164 T167 D168** E170 **H666 P710 N711 R712 I713** R721 Y722 L770 **E774** |
| `8QYQ` (2.61 Å, bovine) | A, B | **Y164 T167 D168 H666 P710 N711 R712 I713** R721 Y722 L770 **E774** |
| `9GZ2` (2.9 Å, human) | A | **Y164 T167 D168 H666 P710 N711 R712 I713** R721 Y722 L770 **E774** |
| `9GZ1` (3.7 Å, human IHM) | A | Q163 **Y164 T167 D168** E497 E500 **H666 P710 N711 R712 I713 E774** |
| `9GZ1` | B | **Y164 T167 D168 H666 P710 N711 R712 I713** R721 Y722 L770 **E774** |
| `9YP9` (3.0 Å, human IHM) | A / B | as `9GZ2` / + L120, E170 |
| `9YR7` (3.0 Å, human IHM) | A / B | as `9GZ2` / + E170 |

**Core consensus — present in every one of the 9 mavacamten copies across all 6 entries (9
residues, P12883 numbering):**

```
Y164  T167  D168  H666  P710  N711  R712  I713  E774
```

**Union across all copies (17 residues):**

```
L120  Q163  Y164  T167  D168  E170  E497  E500  H666  P710  N711  R712  I713  R721  Y722  L770  E774
```

Cross-validation: the omecamtiv mecarbil entry `8QYU` (2OW, 1.96 Å, bovine) contacts
K146 R147 N160 Y164 T167 D168 E170 H492 E497 H666 P710 N711 R712 I713 R721 Y722 L770 G771
E774 — **the same pocket**, consistent with its paper's title claim that the two drugs share
a site.

**The site is genuinely allosteric.** Minimum heavy-atom distance from mavacamten to the ADP
in the myosin active site: **25.1 Å** (`8QYR`), **25.7 Å** (`9GZ2`), **27.3 Å** (`9GZ1`);
centroid separation 30.8–31.3 Å. That is a well-posed distal-site prediction problem — the
target objective is sound even though the assigned holo entry is not.

### 10.3 Species flag and transferability to `5TBY`'s numbering

Human P12883 vs bovine Q9BE39 over residues 1–781 (`PairwiseAligner`, global, BLOSUM62):
**95.9 % identity, 32 mismatches, and the only distinct `human_resnum − bovine_resnum` offset
across the whole alignment is 0** — i.e. **no indels; bovine auth numbering is 1:1 with human
canonical numbering** through the motor domain. **Zero of the 17 pocket positions differ
between human and bovine.** Bovine entries can therefore be used as ground truth against a
human apo structure with no renumbering step at all.

Transfer onto `5TBY` (checked residue-by-residue, `scratchpad/xfer.py`):

- **All 17 pocket residues are modelled in `5TBY` chains A and B**, with **identical residue
  types** at every position (L120, Q163, Y164, T167, D168, E170, E497, E500, H666, P710, N711,
  R712, I713, R721, Y722, L770, E774). All 9 core residues likewise.
- So the *labelling* step would work against `5TBY`. What fails is the *geometry*: Cα
  superposition of `9GZ2` chain A onto `5TBY` chain A over their 761 common Cα (auth 6–796)
  gives **global RMSD 5.02 Å**, **pocket-local RMSD 2.57 Å**, core-local 2.02 Å, with
  per-residue deviations reaching **5.05 Å at R721 and Y722** — two of the pocket-lining
  residues. Part of that is a genuine conformational-state difference (IHM blocked head vs
  primed head); the rest is the 20 Å homology model.

---

## 11. Pipeline-breakers, ranked

**P1 — `6C1H` is the wrong protein. Severity: fatal.**
Rat unconventional myosin-Ib (Q05096) + rabbit skeletal actin (P68135) + calmodulin. Not
cardiac myosin, not myosin II, not human. Mechanism: `src/allo/groundtruth/` loads the holo
entry, looks for a cardiac-myosin chain to align to the apo entry, and either (a) throws, (b)
aligns MYH7 to MYO1B at ~40 % identity and produces a residue mapping that is confidently
wrong across the whole motor domain, or (c) picks the largest chain — actin — and maps
nothing. Every downstream number for this target (top-5 hit list, enrichment vs. random,
noise-resilience curve) would be computed against a label set that does not describe cardiac
myosin. Because project-wide enrichment statistics pool across targets, one silently broken
target contaminates the headline result too.

**P2 — mavacamten is absent from `6C1H`; the ground truth does not exist. Severity: fatal.**
Chem comp `XB2` appears in exactly 6 PDB entries and `6C1H` is not one. `docs/targets.md`
step 1 is *"identify the ligand of interest by chemical component ID"* — that lookup returns
nothing. If the implementation falls back to "the only ligand present", it selects ADP and
emits the 20-residue **actin nucleotide cleft** as the "allosteric site of cardiac myosin".
That failure is silent: it produces a plausible-looking 20-residue label set with no exception
raised.

**P3 — apo↔holo alignment is undefined. Severity: fatal.**
39.6 % local identity between the two heavy chains, different species, different myosin class,
and 1875 residues of actin present only in the holo entry. `docs/targets.md` step 3 requires
mapping holo numbering onto apo numbering by sequence alignment; at 40 % identity that
alignment will place gaps through the loops and shift residue correspondences by several
positions in exactly the surface regions where allosteric pockets live. There is no offset
that fixes it.

**P4 — `5TBY` is not an experimental structure. Severity: fatal for a contact-network method.**
`_em_3d_fitting.ref_protocol = 'RIGID BODY FIT'`; every chain's starting model is PDB `3JBH`
(tarantula); the specimen was tarantula thick filaments; the human sequence was threaded on by
SWISS-MODEL; the envelope is **20 Å** (FSC 0.5); EM Q-score **0.032**; `_em_ctf_correction.type
= NONE`. Mechanism: constraint **C6** makes contact topology the entire physical content of
our model. In `5TBY` that topology is a SWISS-MODEL side-chain packing prediction templated on
an arachnid muscle protein, not a measurement of human cardiac myosin. A quantum walk on that
graph measures the modelling protocol. Every claim we make about "signal propagation in human
β-cardiac myosin" would be, at best, a claim about `3JBH` plus SWISS-MODEL.

**P5 — `5TBY` geometry poisons the contact graph. Severity: high.**
Clashscore 49.95 (**2.2nd percentile**), 5.96 % Ramachandran outliers (**2.8th percentile**),
PDBe overall quality percentile **3.62**, and **41 inter-chain atom pairs at 1.08–1.64 Å**
auto-annotated as `covale`. Mechanism: (a) any builder that reads `_struct_conn` gains 41
spurious covalent edges; (b) even ignoring `_struct_conn`, a distance-cutoff contact map
inherits dozens of unphysically short inter-chain contacts, and they are concentrated at the
head–head and head–RLC interfaces, i.e. **precisely the IHM interface that mediates the
super-relaxed state**. The method would find strong "connectivity" there for a reason that is
an artefact.

**P6 — no ligand anywhere in `5TBY`, so the active site has no apo-derived anchor. Severity: medium.**
`docs/targets.md` names "nucleotide-binding residues from the apo structure's own ligand" as
the preferred apo-only rule for defining the propagation source. `5TBY` has zero HETATM
records, so that rule is unavailable for this target and a different, target-specific rule
(conserved P-loop / switch-I / switch-II motif detection) is required — which needs its own
ADR and is a divergence from the other three targets.

**P7 — SEQRES/ATOM mismatch will mis-size the qubit budget. Severity: medium.**
`5TBY` declares 4592 SEQRES residues and models 2528 (45 % unmodelled; all of 960–1935 in both
heavy chains). Any Phase-4 sizing that reads `entity_poly` length rather than counting `ATOM`
records overstates the compression requirement by ~1.8×.

**P8 — `6C1H` chain P residues 729–734 are an expression tag. Severity: low** (moot given
P1–P3, but it would matter for any pipeline that *did* use this entry).

### Recommended replacements

Numbers below are from §10 and from `/core/entry/` + `/core/polymer_entity/` for each ID.
All auth numbering is P12883-canonical (or 1:1 with it, for the bovine entries).

**Holo (ground truth), pick by priority:**

| PDB | why | tradeoff |
|---|---|---|
| **`8QYR`** | **1.80 Å X-ray**, R-free 0.227 — by far the sharpest view of the pocket. 15 contact residues, the most complete pocket definition. | Bovine (Q9BE39), not human — but 95.9 % identical, **numbering 1:1 with P12883, all 17 pocket residues identical**. Motor domain only (auth 34–781, 709 residues), no light chains. |
| **`9GZ2`** | **2.90 Å cryo-EM, human MYH7 (P12883)**, primed state + mavacamten. PDBe quality percentile **92.76**, clashscore 1.78, 0.00 % Ramachandran outliers — the cleanest model in the set. 764 residues (auth 3–796). | Single head, no light chains; a preprint DOI (10.1101/2025.02.12.637875, PMID 39990378). |
| **`9GZ1`** | **Human β-cardiac IHM + mavacamten** — the drug bound to the exact assembly (two heads + ELC + RLC) whose stabilisation *is* the super-relaxed state. This is the structural statement the challenge objective is about. 2383 residues. | 3.70 Å; PDBe quality percentile 31.6; light chains are **mouse** (P05977, P97457), not human MYL3/MYL2. |
| **`9YP9` / `9YR7`** | **3.00 Å human IHM + mavacamten**, better resolved than `9GZ1`, peer-reviewed (*Sci Adv* 2026, DOI 10.1126/sciadv.aed6472). Modelled range 4–943 is pure native MYH7. | GCN4 + eGFP fusion in the construct (entirely unmodelled); mouse light chains; released 2026-04-08, i.e. after the challenge statement was drafted. |

**Apo (input), pick by priority:**

| PDB | why | tradeoff |
|---|---|---|
| **`8ACT`** | **The experimental structure `5TBY` was trying to be.** "Structure of the human beta-cardiac myosin folded-back off state", 3.6 Å cryo-EM, Grinzato *et al.*, *Nat Commun* 2023, DOI **10.1038/s41467-023-38698-w**, PMID 37258552. **Human MYH7 (P12883) + human MYL3 + human MYL2**, auth == UniProt canonical for all six chains, 2318 modelled residues, ADP·PO₄·Mg only — **no drug**. Same IHM/SRX biology, same light chains, same species as `5TBY`, but measured rather than modelled. All 17 pocket residues fall inside its modelled ranges. | 3.6 Å; `M3L` (trimethyl-Lys) at auth 129 and 549 in both heavy chains must be mapped to LYS; internal gaps at 129, 199–213, 549, 625–644. |
| **`9GZ3`** | **Matched control for `9GZ2`** — same lab, same construct, same map series, same 764 modelled residues (auth 3–796), 3.4 Å, ADP·PO₄·Mg, **no drug**. Pairing `9GZ3`→`9GZ2` removes construct, species and method as confounders entirely: the *only* difference between input and validation structure is the drug. | Single head, no light chains; 3.4 Å. |
| **`9I8P`** | Highest-resolution human WT apo motor domain: **2.601 Å X-ray**, "Human beta-cardiac myosin wild type motor domain in the pre-powerstroke state, MgADP.VO4 form", 704 residues (auth 30–780), released 2025-10-22. | Motor domain only; carries ADP·VO₄·Mg + EDO/GOL/SO₄ cryo-additives that must be filtered under C5. |
| **`8QYP`** | **Matched control for `8QYR`/`8QYQ`** — same paper, same bovine construct, **2.759 Å X-ray**, ADP·VO₄·Mg, no drug, 704 residues (auth 32–780). Pairing `8QYP`→`8QYR` gives the highest-resolution matched apo/holo pair available for this target. | Bovine, not human (numbering still 1:1 with P12883). |
| **`4P7H`** | 3.2 Å X-ray human β-cardiac motor domain, **nucleotide-free** (only 2 × SO₄) — the only genuinely ligand-free human option. | GFP chimera construct; 3.2 Å. |

**Recommended pairings, in order:**

1. **`8QYP` → `8QYR`** — 2.76 Å apo, 1.80 Å holo, same lab/construct/species, numbering
   identical to human. Best data quality by a wide margin. Cost: bovine sequence (95.9 % id,
   pocket 100 % conserved).
2. **`9GZ3` → `9GZ2`** — 3.4 Å apo, 2.9 Å holo, **human**, identical construct. Best
   confound-free human pair.
3. **`8ACT` → `9GZ1`** (or `9YP9`) — human IHM apo → human IHM + mavacamten. The only pairing
   that preserves the challenge's stated *super-relaxed-state* framing, with human ELC/RLC on
   the apo side. Cost: 3.6 / 3.7 Å, mouse light chains on the holo side.
4. **Keep `5TBY`, replace only the holo side** — mechanically viable (all 17 pocket residues
   are modelled in `5TBY` with correct residue types and P12883 numbering) but **not
   recommended**: P4 and P5 mean the resulting network is a property of SWISS-MODEL and
   `3JBH`, not of human cardiac myosin.

Any substitution is a deviation from `CHALLENGE.md` §6 Table 1 and needs an ADR under
`docs/adr/`, plus an update to `docs/targets.md`. The deviation is defensible: the challenge's
own rule is *"blind-predict the location of the allosteric pocket known to exist in the
drug-bound (holo) validation structure"*, and the named validation structure contains neither
the drug nor the protein.

---

## Verdict

**UNUSABLE as assigned.**

The holo side is not defective — it is unrelated. `6C1H` is a rat myosin-Ib / rabbit actin /
calmodulin complex whose only ligands are five ADP·Mg pairs in the **actin** nucleotide
clefts. It contains no mavacamten (chem comp `XB2` is absent from the file and `6C1H` is not
among the 6 PDB entries that contain it), no cardiac myosin, and no human protein. The
ground-truth procedure in `docs/targets.md` cannot be executed against it, and if executed
carelessly it returns 20 rabbit-actin residues with no error raised.

The apo side is separately unusable for our method. `5TBY` is a SWISS-MODEL homology model of
human MYH7, templated on a **tarantula** model (`3JBH`), rigid-body fitted into a **20 Å**
envelope, with a clashscore in the **2nd percentile** of the PDB and 41 inter-chain atom pairs
at bond-length distance clustered on the head–head interface. Under constraint **C6** — contact
topology *is* the physics — that makes any connectivity result an artefact of the modelling
protocol.

Two things survive the audit and should be carried forward:

1. **The target objective is sound.** The mavacamten site is real, well-determined, and
   genuinely distal: **25–27 Å** from the nucleotide pocket, lined by
   **Y164 T167 D168 H666 P710 N711 R712 I713 E774** (core consensus, P12883 numbering) with
   L120/Q163/E170/E497/E500/R721/Y722/L770 in the union. It is a legitimate blind
   allosteric-prediction problem.
2. **Replacement structures exist for both sides**, in matched apo/holo pairs from the same
   labs and constructs — `8QYP`→`8QYR` (best resolution), `9GZ3`→`9GZ2` (best human),
   `8ACT`→`9GZ1` (best match to the SRX framing).

**Recommendation:** replace both sides, write the ADR, and report the defect to the challenge
organisers — the `6C1H` assignment is a factual error in the challenge statement, not a
judgement call, and any team that scores against it is scoring against rabbit actin.

---

## Provenance

All facts derived on **2026-08-20** from the endpoints below. Scripts:
`scratchpad/parse.py` (mmCIF categories), `scratchpad/contacts.py` (KD-tree 4.5 Å contacts),
`scratchpad/align.py` (`Bio.Align.PairwiseAligner`, BLOSUM62, open −11 / extend −1),
`scratchpad/xfer.py` (pocket transfer + `Bio.PDB.Superimposer`), `scratchpad/gql*.py`
(GraphQL surveys). Coordinates in `data/raw/*.cif` (gitignored).

| endpoint | used for |
|---|---|
| `https://files.rcsb.org/download/{id}.cif` | all coordinate- and category-level facts, parsed with `Bio.PDB.MMCIF2Dict.MMCIF2Dict` |
| `https://data.rcsb.org/rest/v1/core/entry/{id}` | method, resolution, dates, entity id lists, `pdbx_vrpt_summary_geometry`, `pdbx_vrpt_summary_em`, residue counts |
| `https://data.rcsb.org/rest/v1/core/polymer_entity/{id}/{n}` | description, organism, UniProt, chains, sequence |
| `https://data.rcsb.org/rest/v1/core/nonpolymer_entity/{id}/{n}` | ligand comp id, count, chains |
| `https://data.rcsb.org/rest/v1/core/chemcomp/{comp_id}` | `XB2` → Mavacamten / MYK-461; `2OW` → omecamtiv mecarbil; `M3L`, `BEF`, `VO4` |
| `https://data.rcsb.org/graphql` | multi-entry surveys (mavacamten set, all 46 P12883 entries) |
| `https://search.rcsb.org/rcsbsearch/v2/query` | `nonpolymer_comp_id == XB2` (6 entries); `2OW` (5 entries); full-text "mavacamten" (9 entries); `P12883` UniProt (46 entries); `rcsb_primary_citation.pdbx_database_id_DOI == 10.1073/pnas.1718316115` (4 entries) |
| `https://www.ebi.ac.uk/pdbe/api/mappings/{id}` | SIFTS residue-level UniProt mapping and identity |
| `https://www.ebi.ac.uk/pdbe/api/validation/global-percentiles/entry/{id}` | wwPDB absolute/relative percentile ranks |
| `https://www.ebi.ac.uk/pdbe/api/validation/summary_quality_scores/entry/{id}` | PDBe overall quality percentile |
| `https://www.ebi.ac.uk/emdb/api/entry/EMD-{n}` | EMD-7329/7330/7331 titles and sample names |

### Could not be determined

- **R-work / R-free for either entry** — both are cryo-EM; the category is absent by
  construction, not missing. Reported as "not applicable", not as a gap.
- **Which map `5TBY`'s coordinates were actually fitted into.** `_struct.title` says the human
  negative-stain reconstruction EMD-2240; the `_em_*` block describes the tarantula cryo-EM
  experiment (`staining_applied = NO`, `vitrification_applied = YES`, specimen = tarantula
  thick filaments, natural source *Aphonopelma* taxid 6896). Both are in the deposited file
  and the audit cannot adjudicate between them.
- **`6C1H`'s conformational state as the depositors would name it.** No `struct` field names
  one. Nucleotide-free myosin is derived from coordinates (empty Myo1b site; sibling `6C1D`
  has ADP·Mg on chain P), but the associated map EMD-7331 is annotated *"…with ADP"*. Recorded
  as a conflict, not resolved.
- **Full text of the primary citations.** Only the deposited `_citation` / `_citation_author`
  records (title, journal, volume, pages, year, DOI, PMID, author list) were read. No claim
  here rests on the body of any paper.
- **Whether the challenge organisers intended a different PDB ID.** `6C1H` is what
  `CHALLENGE.md` §6 Table 1 says, verbatim. Any inference about the intended entry would be
  speculation.
