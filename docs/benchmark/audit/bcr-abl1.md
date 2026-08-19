# Benchmark audit — BCR-ABL1: apo `1OPL` → holo `5MO4`

Target pocket: the distal **myristoyl pocket** bound by **asciminib (ABL001)**
(`CHALLENGE.md` §6, Table 1, row 2).

**Every number below was derived programmatically.** The endpoint or file/field that
produced each fact is given inline. Machine-readable twin: `bcr-abl1.json`
(`provenance` object lists every endpoint and the generation date). Method: `Bio.PDB.MMCIF2Dict` +
`scipy.spatial.cKDTree` over `data/raw/*.cif` (re-downloadable from the endpoints listed
in the JSON), 4.5 Å heavy-atom contact cutoff, hydrogens excluded via
`_atom_site.type_symbol`. The generating script was a session scratchpad throwaway; the
JSON `provenance` block is the durable record.

**Verdict up front: UNUSABLE AS AN APO→HOLO BLIND-PREDICTION PAIR.** `1OPL` is not apo
— it carries a myristic-acid molecule sitting in the target pocket whose 16 contact
residues are a strict subset of asciminib's 20 contact residues in `5MO4`, in identical
auth numbering. See §10.

---

## 1. Entry-level facts

| | `1OPL` (apo input) | `5MO4` (holo ground truth) |
|---|---|---|
| Title (`_struct.title`) | Structural basis for the auto-inhibition of c-Abl tyrosine kinase | ABL1 kinase (T334I_D382N) in complex with asciminib and nilotinib |
| Method (`exptl.method`) | X-RAY DIFFRACTION | X-RAY DIFFRACTION |
| Resolution (`_refine.ls_d_res_high`) | **3.42 Å** | **2.17 Å** |
| R-work / R-free (`_refine.ls_R_factor_R_work` / `_R_free`) | **0.306 / 0.315** | 0.1818 / 0.2170 |
| Mean B (`_refine.B_iso_mean`) | **123.3 Å²** | 36.73 Å² |
| Reflections obs. / completeness | 16 203 / 89.1 % | 29 028 / 98.49 % |
| Deposited → released (`rcsb_accession_info`) | 2003-03-06 → 2003-04-08 | 2016-12-13 → 2017-04-05 |
| Primary citation | Cell 112:859 (2003), DOI `10.1016/S0092-8674(03)00194-6`, PMID 12654251 | Nature 543:733 (2017), DOI `10.1038/nature21702`, PMID 28329763 |

Source: `https://data.rcsb.org/rest/v1/core/entry/{1OPL,5MO4}` plus `_refine.*` and the
`_citation` loop of `data/raw/{1OPL,5MO4}.cif`. RCSB's `citation.pdbx_database_id_doi`
returns `null` for both; the DOIs above come from `_citation.pdbx_database_id_DOI` in
the mmCIF.

### wwPDB validation percentiles
`https://www.ebi.ac.uk/pdbe/api/validation/global-percentiles/entry/{1opl,5mo4}`
(`rawvalue` / `absolute` = percentile against the whole PDB / `relative` = against
entries of similar resolution).

| Metric | `1OPL` raw | `1OPL` abs %ile | `5MO4` raw | `5MO4` abs %ile |
|---|---|---|---|---|
| Clashscore | 9.91 | 27.8 | 1.34 | 94.1 |
| Ramachandran outliers | 0.62 % | 24.9 | 0.00 % | 100.0 |
| Sidechain (rotamer) outliers | 2.39 % | 48.5 | 0.56 % | 85.9 |
| **RSRZ outliers** | **22.18 %** | **0.4** | 4.43 % | 33.9 |
| DCC R-free | 0.2848 | 13.0 | 0.22 | 68.2 |

`1OPL` sits in the **bottom 0.4 %** of the PDB for real-space fit. This is the
structure the challenge nominates as the *input* to an elastic-network model.

---

## 2. Composition and domain content

### Polymer entities (`_entity`, `_entity_poly`, `_entity_src_gen`, `_struct_ref`)

| | `1OPL` | `5MO4` |
|---|---|---|
| Description | proto-oncogene tyrosine-protein kinase | Tyrosine-protein kinase ABL1 |
| Organism / host | *Homo sapiens* (9606) / *Spodoptera frugiperda* | same |
| UniProt | P00519 (`ABL1_HUMAN`) | P00519 |
| SEQRES length | 537 | 495 |
| Copies / auth chains | **2** — A, B | 1 — A |

### Non-polymer entities (`_entity`, `_chem_comp`, `_atom_site`)

| Entry | Comp ID | Name (`_chem_comp.name`) | Formula | Copies | Auth position | Occ. | Mean B |
|---|---|---|---|---|---|---|---|
| `1OPL` | **`MYR`** | MYRISTIC ACID | C14 H28 O2 | 1 | A/538 | 1.0 | 84.4 |
| `1OPL` | **`P16`** | 6-(2,6-dichlorophenyl)-2-{[3-(hydroxymethyl)phenyl]amino}-8-methylpyrido[2,3-d]pyrimidin-7(8H)-one | C21 H16 Cl2 N4 O2 | 2 | A/539, B/538 | 1.0 | 118.9 |
| `5MO4` | **`NIL`** | Nilotinib | C28 H22 F3 N7 O | 1 | A/601 | 1.0 | 32.7 |
| `5MO4` | **`AY7`** | asciminib | C20 H18 Cl F2 N5 O3 | 1 | A/602 | 1.0 | 36.2 |

Waters (`rcsb_entry_info.deposited_solvent_atom_count`): `1OPL` = **0**, `5MO4` = 307.

The asciminib chem-comp ID was **read from the file**, not assumed:
`_entity.pdbx_description` = "asciminib" for entity 3 → `_chem_comp.id` = `AY7`.

### Domains present — from modelled `auth_seq_id` mapped onto UniProt features

UniProt P00519 features (`https://rest.uniprot.org/uniprotkb/P00519.json`, canonical =
isoform IA numbering): CAP 1–60, SH3 61–121, SH2 127–217, protein kinase 242–493,
active site (proton acceptor) 363. Adding the +19 isoform-IB offset established in §4
gives auth-numbering equivalents; SIFTS Pfam/CATH mappings
(`https://www.ebi.ac.uk/pdbe/api/mappings/{1opl,5mo4}`) agree and are quoted directly:

| Region | SIFTS Pfam/CATH auth range | Modelled in `1OPL` A | `1OPL` B | `5MO4` A |
|---|---|---|---|---|
| 1b CAP / N-terminus | ≤ 80 | no | no | no |
| SH3 (`PF00018`) | 86–132 | **yes** | **no** | **yes** |
| SH2 (`PF00017`) | 146–221 | yes | yes | yes |
| SH2–kinase linker | ~222–260 | yes | partial (gap 238–251) | yes |
| Kinase / SH1 (`PF07714`) | 261–512 | yes | yes | yes (act. loop 402–419 absent) |
| αI helix (`_struct_conf` HELX_P20 / HELX_P19) | **520–531** | **yes (12/12)** | **no (0/12)** | **yes (12/12)** |

> **The project's working assumption that `5MO4` is "kinase domain only" is false.**
> SIFTS Pfam places SH3 at auth 86–132 and SH2 at 146–221 in `5MO4`, and the
> coordinates model 83–531 continuously through both. `5MO4` is the same
> SH3–SH2–kinase autoinhibited assembly as `1OPL` chain A. `docs/targets.md` must be
> corrected.

The αI helix range 520–531 is **not** recalled — it is `_struct_conf` record
`HELX_P20` (`1OPL`, chain A, `beg_auth_seq_id` 520 → `end_auth_seq_id` 531, class 1,
length 12) and `HELX_P19` (`5MO4`, identical range). In `1OPL` chain B the last helix
is `HELX_P38`, 504–518: **no αI**.

---

## 3. Construct and mutations

`_struct_ref_seq_dif` verbatim, reconciled against the isoform sequences (§4). Reported
`pdbx_seq_db_seq_num` values for `1OPL` are unreliable because the deposited alignment
is wrong; the "vs isoform IB" column is derived by direct string comparison of
`_entity_poly.pdbx_seq_one_letter_code_can` against `P00519-2.fasta`.

**`1OPL`** (identical rows for chains A and B):

| auth | deposited | vs isoform IB | `details` | modelled? |
|---|---|---|---|---|
| 29 | ARG (db LYS 29) | K29R | engineered mutation | no (1–80 unobserved) |
| 30 | ASP (db GLU 30) | E30D | engineered mutation | no |
| **382** | ASN (db ASP 382) | **D382N** = D363N in IA | engineered mutation | **yes** |
| 532–537 | E,N,L,Y,F,Q | `ENLYFQ` TEV site | cloning artifact | no |

**`5MO4`** (chain A):

| auth | deposited | vs isoform IB | `details` | modelled? |
|---|---|---|---|---|
| 40–45 | G,A,M,D,P,S | `GAMDPS` | expression tag | no |
| **334** | ILE (db THR 315) | **T334I** = T315I in IA | conflict | **yes** |
| **382** | ASN (db ASP 363) | **D382N** = D363N in IA | conflict | **yes** |

**The two entries carry different mutations.** Both are D382N — verified in the
coordinates, where `1OPL`/A residues 380–382 read HIS-ARG-**ASN**, i.e. the catalytic
HRD aspartate is knocked out in both. But `1OPL` auth 334 is **THR** (wild-type
gatekeeper) while `5MO4` auth 334 is **ILE**: the holo structure is the **T315I
imatinib-resistance mutant**, the apo structure is not.

---

## 4. Numbering — CRITICAL, and the flagged hypothesis is **refuted**

### Auth ranges and label↔auth offsets (`_atom_site`)

| Entry / chain | auth range in ATOM records | `label_seq_id`→`auth_seq_id` offset | insertion codes | alt-loc IDs |
|---|---|---|---|---|
| `1OPL` A | 81–531 (451 residues, **no internal gaps**) | **0** (auth == label) | none (`?`) | none (`.`) |
| `1OPL` B | 140–237, 252–518 (365 residues) | 0 | none | none |
| `5MO4` A | 83–295, 298–401, 420–531 (429 residues) | **+39** | none | `.`, A, B |

### Isoform relation, derived not recalled

- `https://rest.uniprot.org/uniprotkb/P00519.json` → `primaryAccession` P00519,
  `uniProtkbId` ABL1_HUMAN, canonical length **1130**, isoform list: `P00519-1` = **IA**
  (Displayed), `P00519-2` = **IB**. Feature `Alternative sequence 1-26 in isoform IB`;
  feature `Lipidation 2-2 N-myristoyl glycine`.
- `P00519-1.fasta` (1130 aa) vs `P00519-2.fasta` (1149 aa): **`IA[27:] == IB[46:]`
  evaluates `True`**. Length difference **19**. So *isoform IB numbering = canonical
  (IA) numbering + 19* for every residue from IA 27 / IB 46 onward.

### Which convention does each entry use?

| Test | `1OPL` | `5MO4` |
|---|---|---|
| SEQRES vs isoform IB | differs at **3** positions (29, 30, 382) | differs at **2** positions (334, 382) |
| SEQRES vs isoform IA | differs at **497** positions | — |
| SIFTS `/mappings/` | label 32–531 ↔ UNP 13–512 → offset **+19** | auth 46 ↔ UNP 27 → offset **+19** |
| Deposited `_struct_ref_seq` | claims db 1–531 ↔ auth 1–531, offset **0** | db 27–515 ↔ auth 46–534, offset +19 |

> **The `1OPL` mmCIF `_struct_ref_seq` block is wrong.** It force-aligns an isoform-IB
> construct onto the isoform-IA canonical sequence 1:1. SIFTS has silently corrected
> this, and the coordinates confirm SIFTS. The bogus alignment is also what produced the
> phantom "engineered mutations" K29R/E30D — those positions are inside the IB-specific
> cap, which has no IA counterpart at all.

### **Apo↔holo offset: ZERO**

Both entries use ABL1 **isoform IB numbering** (auth = UniProt canonical + 19). The
suspicion that the pair mixes 1a and 1b numbering is **refuted by the data**.

**Worked example — three residues that are unambiguously the same physical residue,
read out of `_atom_site.auth_comp_id`:**

| Physical residue | `1OPL` auth (comp) | `5MO4` auth (comp) | UniProt IA |
|---|---|---|---|
| gatekeeper | **334 (THR)** | **334 (ILE)** — T315I mutant | 315 |
| HRD catalytic Asp (mutated to Asn in both) | **382 (ASN)** | **382 (ASN)** | 363 |
| β3 catalytic lysine | **290 (LYS)** | **290 (LYS)** | 271 |
| DFG aspartate | 400 (ASP) | 400 (ASP) | 381 |

*A caution that survives this result:* the wider ABL1 corpus **is** split. SIFTS gives
auth−UNP = **0** for `2E2B` (and `9KS5` carries `PTR393`, an IA-numbered activation-loop
phosphotyrosine) but **+19** for `1OPL`, `5MO4`, `3PYY`, `4XEY`, `8SSN`, `6XR7`. Any
future ABL1 entry must be re-checked; do not generalise the "+19" from this pair.

---

## 5. Completeness

`_pdbx_unobs_or_zero_occ_residues`:

| Entry / chain | unobserved auth ranges | count |
|---|---|---|
| `1OPL` A | 1–80, 532–537 | 86 |
| `1OPL` B | 1–139, **238–251**, **519–537** | 172 |
| `5MO4` A | 40–82, 296–297, **402–419** (activation loop), 532–534 | 66 |

Alternate conformations (`_atom_site.label_alt_id`): `1OPL` = **0** in either chain (all
`.`); `5MO4` = 1 residue, auth 256.

**Pocket and αI coverage** (pocket lining defined in §6 from computed contacts, αI from
`_struct_conf`):

| | myristoyl-pocket residues modelled | αI 520–531 modelled |
|---|---|---|
| `1OPL` A | **16/16** | 12/12 |
| `1OPL` B | 13/16 (missing 521, 525, 529) | **0/12** |
| `5MO4` A | 16/16 | 12/12 |

Residue-level validation inside the pocket
(`https://www.ebi.ac.uk/pdbe/api/validation/residuewise_outlier_summary/entry/{1opl,5mo4}`):
`1OPL` chain A flags 360 (clashes), 448 (sidechain outlier), 529 (clashes); `1OPL`
chain B flags 356, 363, 448, 451, 452 (RSRZ), 360, 512 (clashes); `5MO4` chain A flags
**none** of its 20 pocket residues.

---

## 6. Ligands and the blindness question — **the critical section**

Contacts computed from coordinates: any ligand heavy atom within **4.5 Å** of any
protein heavy atom, `scipy.spatial.cKDTree` over `_atom_site`, hydrogens excluded.

### `1OPL` — every non-polymer component

**`MYR` (myristic acid), chain A, auth 538, 15 heavy atoms → 16 protein residues**

```
A/356 ALA 3.92   A/359 LEU 3.89   A/360 LEU 3.47   A/363 ALA 3.92
A/448 LEU 4.07   A/451 ILE 4.39   A/452 ALA 4.22   A/481 GLU 3.62
A/482 GLY 3.93   A/483 CYS 4.15   A/484 PRO 3.99   A/487 VAL 4.10
A/512 PHE 4.24   A/521 ILE 3.56   A/525 VAL 3.79   A/529 LEU 3.29
```

**`P16`, chain A, auth 539, 29 heavy atoms → 21 residues**: 267, 268, 272, 275, 288,
289, 290, 305, 309, 318, 332, **334**, 335, 336, **337**, 338, 340, 389, 399, **400**,
**401**. That contact set is the ATP cleft — β3 Lys290, αC Glu305, gatekeeper Thr334,
hinge Met337, DFG Asp400/Phe401 (all identities read from `auth_comp_id`).
`P16` in chain B, auth 538, gives the equivalent 23-residue set.

### Direct answers

**Does `1OPL` contain a myristoyl group occupying the myristoyl pocket?**
**YES.** `MYR`, occupancy 1.0, mean B 84.4 Å². Its 16 contact residues are exactly the
pocket lined by helices αE/αH/αI at the C-lobe base, and they are a **strict subset** of
asciminib's contact residues in `5MO4` (proved below).

**Is it covalently linked to the protein?**
**NO.** Neither file contains a `_struct_conn` category at all
(`[k for k in MMCIF2Dict(...) if "conn" in k]` returns `[]` for both; `grep -c
_struct_conn` returns 0 for both). There are therefore **zero `covale` rows**, and no
`_pdbx_struct_mod_residue` entries in either file. `MYR` is a free, non-covalently
modelled fatty acid, deposited as its own non-polymer entity at auth 538, with the
would-be attachment point (the isoform-IB N-terminal Gly2 of the cap) unmodelled
(`1OPL` chain A begins at auth 81).

> **Consequence for constraint C5.** The myristate is *not* a PTM in this file. It is an
> independent ligand. "Exclude PTMs unless modelled as simple nodes" does not
> automatically remove it; a deliberate rule is needed (see §10a).

**Does `1OPL` contain an ATP-site kinase inhibitor?**
**YES — two copies of `P16`**, one per chain, binding the ATP cleft as shown above.

### `5MO4`

**`AY7` (asciminib), chain A, auth 602, 31 heavy atoms → 20 protein residues**

```
A/351 ARG 3.79   A/356 ALA 3.68   A/359 LEU 3.22   A/360 LEU 3.38
A/363 ALA 3.57   A/448 LEU 3.27   A/451 ILE 3.61   A/452 ALA 3.52
A/453 THR 3.47   A/454 TYR 3.87   A/456 MET 4.20   A/481 GLU 2.82
A/482 GLY 4.39   A/483 CYS 3.84   A/484 PRO 3.73   A/487 VAL 3.68
A/512 PHE 3.63   A/521 ILE 3.62   A/525 VAL 3.68   A/529 LEU 3.76
```

**`NIL` (nilotinib), chain A, auth 601, 39 heavy atoms → 26 residues** in the ATP cleft
(267, 272, 275, 288, 289, 290, 304, 305, 308, 309, 312, 317, 318, 332, **334**, 336,
**337**, 340, 373, 378, 380, 389, 398, 399, **400**, 401).

### Set algebra (identical auth numbering, offset 0 — §4)

| Comparison | Result |
|---|---|
| `MYR`(`1OPL`/A) ⊆ `AY7`(`5MO4`/A) | **True** |
| Intersection | **16 residues** |
| Jaccard | **0.800** |
| `AY7` \ `MYR` | 351, 453, 454, 456 |
| `MYR` ∩ `P16`(`1OPL`/A) | ∅ (the two sites are disjoint) |
| `AY7` ∩ `NIL`(`5MO4`/A) | ∅ |
| `P16`(`1OPL`/A) vs `NIL`(`5MO4`/A) | 18 shared, Jaccard 0.621 |

**Every single ground-truth pocket residue (20/20) is modelled in `1OPL` chain A, and
16 of the 20 are already in direct van-der-Waals contact with a ligand in the "apo"
input file.**

---

## 7. Assembly

**`1OPL`** — 2 polymer copies in the asymmetric unit. `_pdbx_struct_assembly`: assembly
1 = author-defined, **monomeric**, asyms A,C,D (= chain A + `MYR` + `P16`); assembly 2 =
PISA, monomeric, asyms B,E (= chain B + `P16`); assembly 3 = PISA, **dimeric**, A,C,D
under operators 1,2.

**The two copies are not the same molecule in the same state.**

| Comparison | n CA | CA-RMSD |
|---|---|---|
| chain A vs chain B, all common residues | 365 | **23.12 Å** |
| chain A vs chain B, kinase domain 261–512 only | 252 | **0.52 Å** |

After superposing on the kinase domain, the SH2 domain (146–221) of chain B sits a mean
of **68.4 Å** (max 101.3 Å) from where it sits in chain A, while the pocket lining moves
only 0.21 Å. Chain A is the **assembled autoinhibited state**; chain B has SH3
completely unmodelled (starts at 140), a 238–251 gap, a disengaged SH2, and **no αI
helix** (stops at 518).

**Is the pocket occupied in all copies? No.** `MYR` appears once, in chain A only.
Chain B has no ligand within 4.5 Å of any pocket-lining residue — but it also cannot
form the pocket, because the αI wall (521, 525, 529) is unmodelled.

**`5MO4`** — 1 polymer copy; single deposited assembly, PISA, **monomeric**, asyms
A,B,C,D (protein + `NIL` + `AY7` + water).

---

## 8. Modifications

`_pdbx_struct_mod_residue`: **absent from both files**. No modified residues.
`_entity_poly.nstd_monomer` = `no` for both. No non-standard residues appear inside
either polymer; every `HETATM` record belongs to `MYR`, `P16`, `NIL`, `AY7`, or `HOH`
(enumerated from `_atom_site.group_PDB` × `auth_comp_id`).

---

## 9. Apo↔holo comparability

Global alignment of `_entity_poly.pdbx_seq_one_letter_code_can`
(`Bio.Align.PairwiseAligner`, BLOSUM62, gap open −11 / extend −1, global):

- lengths 537 (`1OPL`) vs 495 (`5MO4`); 495 aligned columns; **486 identities =
  98.18 %**.
- All 9 mismatches are accounted for: alignment columns 0–5 = the two different
  N-terminal tags (`MGQQ.G` vs `GAMDPS`), column 333 = **T→I** (the T334I gatekeeper),
  columns 531–533 = `1OPL`'s `ENLYFQ` TEV artifact.

| Question | Answer |
|---|---|
| Same species / UniProt? | Yes — *H. sapiens*, P00519, Sf9-expressed, both |
| Same isoform? | Yes — both isoform **IB** constructs |
| Same numbering? | Yes — offset **0** (§4) |
| Same domain content? | Yes — both SH3–SH2–kinase (§2) |
| Residue-range overlap | `1OPL`/A 81–531 vs `5MO4`/A 83–531 → 429 common modelled residues |
| Holo pocket residues with a modelled apo counterpart | **20/20** in `1OPL` chain A; 17/20 in chain B |
| Structural similarity, all common CA | **0.98 Å** |
| Kinase domain 261–512 | 1.01 Å |
| Pocket lining after kinase superposition | mean CA deviation **0.41 Å** |

The apo and holo structures are, to within 1 Å, **the same conformation of the same
construct** — differing only in which ligands fill two already-open pockets.

---

## 10. Pipeline-breakers, ranked

### 1. The "apo" input has the target pocket occupied by a ligand — the prediction is not blind (SEVERITY: fatal)

`MYR` is present at occupancy 1.0 in `1OPL` chain A, and `MYR`-contact ⊆ `AY7`-contact
with Jaccard 0.800 in identical numbering (§6). **Mechanism:** the pocket in the input
file is not cryptic — it is a fully formed, ligand-shaped cavity whose walls have been
splinted open by a C14 fatty acid. An elastic network built from `1OPL` chain A inherits
that geometry. Any method that scores "distal cavities with unusual local packing" will
find it, and will do so for a reason that has nothing to do with quantum signal
propagation. It is measurement of the answer, not prediction of it.

The apo/holo gap that the benchmark is supposed to test *does not exist here*: 0.98 Å
global CA-RMSD, 0.41 Å over the pocket lining (§9). A benchmark whose input and ground
truth are the same structure cannot discriminate a good method from a bad one.

**(a) What happens if we delete the myristate, per C5?**
The removal is *coordinate-neutral*: `MYR` is a separate non-polymer entity with no
`covale` link (§6), so deleting it changes zero protein atoms. The residue-level contact
network in the pocket is **completely unchanged** by the deletion — the pocket walls
stay exactly where the myristate propped them. Deleting `MYR` therefore satisfies C1/C5
*in letter* while leaving the leak fully intact. The measurable evidence that this
matters: the pocket-lining CA geometry in `1OPL`/A (359–529 = 16.83 Å; radius of
gyration of the 16 pocket CAs = 7.66 Å) is indistinguishable from asciminib-bound
`5MO4`/A (16.02 Å; 7.59 Å), and both are far tighter and more ordered than any genuinely
ligand-free ABL1 kinase domain — `6XR6`/`6XR7`/`6XRG` model 1 give 31.24 / 13.35 /
17.81 Å and Rg 11.30 / 8.96 / 8.08 Å. **Removing the ligand does not remove the leak;
only changing the input structure does.**

### 2. `1OPL` also contains an ATP-site inhibitor, so nothing about it is apo (SEVERITY: fatal for the active-site definition)

`P16` occupies the ATP cleft in **both** chains (§6). Two consequences. (i) The
"active site" that the challenge asks us to propagate *from* is itself drug-occupied
and drug-shaped in the input. (ii) `P16`'s contact set shares 18 residues with
nilotinib's set in `5MO4` (Jaccard 0.621) — so the ATP-site geometry is also
pre-conditioned toward the holo answer. A defensible apo-only active-site rule
(conserved VAIK/HRD/DFG motifs: Lys290, Asn382 of the mutated HRD, Asp400-Phe401-Gly402
— all verified from `auth_comp_id`) exists, but it must not be derived from `P16`.

### 3. `1OPL` is a 3.42 Å, R-free 0.315, mean-B 123 Å² model in the bottom 0.4 % of the PDB for RSRZ (SEVERITY: high)

An elastic network model is a function of interatomic distances. At 3.42 Å with 22.18 %
RSRZ outliers, side-chain positions — which set contact-network edges at any cutoff
below ~8 Å — carry error comparable to the contact threshold itself. Three of the 16
pocket residues in chain A are already flagged (clashes at 360 and 529, sidechain
outlier at 448). Noise-resilience results computed on this input will be measuring the
crystallography, not the method.

### 4. Which of the two copies is used silently changes the answer (SEVERITY: high, and it is a reproducibility trap)

Chain A and chain B are 23.12 Å apart globally (§7). Chain B has no SH3, no αI helix,
and 3 of 16 pocket residues unmodelled. A pipeline that defaults to "the first chain" or
"the longest chain" picks A; one that picks B produces a network in which the target
pocket **does not exist**. This must be an explicit, recorded choice.

### 5. Construct mismatch: WT gatekeeper (apo) vs T315I (holo) (SEVERITY: moderate)

`1OPL` auth 334 = THR, `5MO4` auth 334 = ILE (§3). The ground truth is derived from a
resistance-mutant structure. Thr334 is not in the asciminib contact set, so the *label
set* is unaffected; but any claim that the two entries are "the same protein" is wrong,
and the mutation does sit in the ATP cleft that `NIL` and `P16` occupy.

### 6. Domain-content mismatch — **the premise is false, so this one is a non-issue** (SEVERITY: none)

**(b)** `docs/targets.md` records "Domain content of `1OPL` (SH3, SH2, kinase) vs.
`5MO4` (kinase domain only)". This is **refuted**: SIFTS Pfam places SH3 at auth 86–132
and SH2 at 146–221 in `5MO4`, and `5MO4` chain A is modelled continuously from 83 to 531
(§2). Both entries are SH3–SH2–kinase. The ground-truth transfer alignment step is
therefore trivial (98.18 % identity, offset 0) and **does not break**. The doc must be
corrected so nobody builds a residue-remapping workaround for a problem that does not
exist.

### Alternatives, with evidence

Searched all **85** experimental PDB entries carrying UniProt P00519
(`https://search.rcsb.org/rcsbsearch/v2/query`, attribute
`rcsb_polymer_entity_container_identifiers.reference_sequence_identifiers.database_accession`),
then screened candidates by downloading the mmCIF and asking two coordinate questions:
is any non-water `HETATM` within 4.5 Å of the 16 pocket-lining residues, and is
αI 520–531 modelled.

**Holo side — keep `5MO4`.** Only **two** PDB entries contain chem comp `AY7`
(asciminib): `5MO4` and `8SSN`. `8SSN` is 2.86 Å, R-free 0.348, also carries a second
ligand (`SKI`), and models αI only 7/12. `5MO4` is strictly better on every axis. There
is no asciminib-only ABL1 structure to move to. *Tradeoff:* we keep the co-bound
nilotinib, which is harmless for the label set (`AY7` ∩ `NIL` = ∅).

**Apo side — replace `1OPL`.** Best candidates, all verified pocket-empty from
coordinates and all in the same isoform-IB numbering (SIFTS auth−UNP = +19), so labels
transfer with offset 0:

| Candidate | Method | auth range | αI modelled | Pocket residues | Pocket ligand | kinase RMSD to `5MO4`/A |
|---|---|---|---|---|---|---|
| **`6XR7`** "Abl isoform 1b inactive1 state" | SOLUTION NMR, 20 models | 248–534 | **12/12** | **16/16** | **none** | 2.15 Å |
| `6XRG` "inactive2 state" | SOLUTION NMR, 20 models | 248–534 | 12/12 | 16/16 | none | 2.37 Å |
| `6XR6` "active state" | SOLUTION NMR, 20 models | 248–534 | 12/12 | 16/16 | none | 1.93 Å |
| `4XEY` | X-ray 2.891 Å, R-free 0.2593 | 250–522 / 141–523 | 3/12, 4/12 | 14/16 | none | 1.23 Å |

*Tradeoffs.* `6XR7`/`6XRG`/`6XR6` are the only ABL1 entries found with **no ligand
anywhere near the pocket and the complete αI wall modelled** — they are genuinely apo,
and their pocket geometry is visibly different from the bound state (Rg of the 16 pocket
CAs: 8.96 / 8.08 / 11.30 Å vs 7.59 Å in `5MO4`), which is exactly the cryptic-pocket
signal a blind prediction should have to overcome. Cost: they are NMR ensembles (no
resolution or R-free; a model-selection or ensemble-averaging rule is needed, and it
must be recorded), and they cover the kinase domain only — dropping SH3/SH2 changes the
network size from ~450 to ~287 nodes and removes the autoinhibitory clamp whose
allosteric coupling to the pocket is arguably the biology of interest. `4XEY` is
crystallographic and pocket-empty but models only 3–4 of the 12 αI residues, so a third
of the pocket wall is simply absent from the network, and it carries a second ligand
(`1N1`, `_chem_comp.formula` C22 H26 Cl N7 O2 S) elsewhere in the structure — outside
the myristoyl pocket by the 4.5 Å screen, but it is not ligand-free either.

**Recommendation.** Report the `1OPL` finding as a documented defect of the *challenge's
own* target table (it is not our error to fix silently), keep `1OPL`→`5MO4` as the
"as-specified" run so the submission answers the stated task, and add `6XR7`→`5MO4` as
the honest blind-prediction run. Score and report both. If only one number is reported,
it must be the `6XR7` one, with the `1OPL` result presented as the positive control that
demonstrates why.

---

## Verdict

**UNUSABLE as an apo→holo blind-prediction pair, as specified.**

1. `1OPL` is not apo. It contains myristic acid (`MYR`) at occupancy 1.0 in the target
   pocket, plus an ATP-site inhibitor (`P16`) in both chains. Sixteen of the twenty
   ground-truth pocket residues are in van-der-Waals contact with a ligand **in the
   input file**, in identical numbering.
2. The apo and holo structures superimpose at 0.98 Å over 429 residues — there is no
   conformational change for the method to predict.
3. Deleting the myristate satisfies the letter of C1/C5 and does nothing about the leak,
   because the ligand is non-covalent and the pocket geometry it holds open is what the
   network sees.
4. `1OPL` is additionally a poor model: 3.42 Å, R-free 0.315, mean B 123 Å², bottom
   0.4 % of the PDB for RSRZ.

**Usable with documented caveats** if the apo input is replaced by `6XR7` (or `6XR6` /
`6XRG`), which is ligand-free, models the full αI wall, and uses the same numbering — at
the cost of an NMR ensemble and the loss of SH3/SH2.

Two of the pair's flagged suspicions are **refuted, and `docs/targets.md` should be
corrected on both**: there is **no** apo↔holo numbering offset (both are isoform IB,
offset 0), and `5MO4` is **not** kinase-domain-only (it is the same SH3–SH2–kinase
assembly as `1OPL`). What is *not* refuted, and is worse than suspected, is the
myristoyl occupancy — compounded by a second, unreported ATP-site ligand.

### Not determined

- Whether the challenge organisers intend `1OPL` chain A or chain B, or intend the
  myristate to be stripped. `CHALLENGE.md` §6 names only PDB IDs.
- Whether the `MYR` density in a 3.42 Å map with 22.18 % RSRZ outliers actually supports
  a fatty acid; PDBe's residue-level API returns no ligand-specific RSCC for `MYR`, and
  no map coefficients were fetched. The occupancy-1.0/B-84 modelling is what the
  depositors asserted, not an independent confirmation.
- Pocket-volume comparisons are reported only as CA-distance and radius-of-gyration
  proxies. No cavity-detection algorithm (fpocket/CASTp) was run, so "the pocket is
  more open in `1OPL` than in apo ABL1" is supported by a proxy, not by a volume.
