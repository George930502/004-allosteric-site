# Independent fact-check of the organisers' reply and of the repository's own claims

**Checked on 2026-09-02.** Every fact below was re-derived from a primary source on the day of
writing. Nothing here is recalled. The claim list is the one given to the checker; claims 1–6
are the organisers' (`00-official-reply.md`), claims 7–13 are the repository's
(`docs/benchmark/primary/README.md`, `manifest.yaml`, `frozen.json`, `audit/*.md`).

**Sources used, all fetched live.** RCSB Data API (`https://data.rcsb.org/rest/v1/core/...`)
and GraphQL (`https://data.rcsb.org/graphql`); RCSB Search API
(`https://search.rcsb.org/rcsbsearch/v2/query`); wwPDB mmCIF headers
(`https://files.rcsb.org/header/{id}.cif`); PDBe REST
(`https://www.ebi.ac.uk/pdbe/api/...`); PDBe Graph API
(`https://www.ebi.ac.uk/pdbe/graph-api/...`, Arpeggio-derived contacts); PDBj Mine2 SQL over
the mmCIF categories (`https://pdbj.org/rest/mine2_sql`); UniProt
(`https://rest.uniprot.org/...`); PubChem PUG REST; Europe PMC.

**One limitation, stated up front.** The checker had no local compute. Distances at a chosen
cutoff could not be recomputed from coordinates. Where a claim is a 4.5 Å heavy-atom
measurement, it is checked against two independent _annotations_ — the deposited
`_struct_site_gen` records and PDBe's Arpeggio contact analysis — and the verdict says which
of the three criteria a residue passes. Both annotations are demonstrably **stricter** than a
4.5 Å heavy-atom shell (proof in §9), so a residue absent from them is not thereby refuted.

---

## Verdict table

| #   | Claim (abridged)                                                                                                     | Verdict               | One-line note                                                                                                                   |
| --- | -------------------------------------------------------------------------------------------------------------------- | --------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| 1   | `6C1H` is rabbit/rat actin–myosin-Ib, no MYH7, no mavacamten                                                         | CONFIRMED             | Every element holds. One precision note: the calmodulin chain's organism is deposited as "unidentified"                         |
| 2   | `9GZ2` is a 2.9 Å human MYH7–mavacamten complex                                                                      | CONFIRMED             | 2.9 Å cryo-EM, P12883, `XB2` present, one chain, no chimera, no GCN4/EGFP, no light chain modelled                              |
| 3   | `8QYR` and `9GZ1` are possible alternatives                                                                          | PARTIALLY CONFIRMED   | Both are genuine mavacamten complexes, but **`8QYR` is bovine** (Q9BE39) and `9GZ1` carries **mouse** light chains              |
| 4   | `1OPL` A has myristate + the ATP-site inhibitor **PD180970**; B has the inhibitor only                               | PARTIALLY CONFIRMED   | Ligand placement is exactly right; the inhibitor is **PD166326** (`P16`), not PD180970. The repo is correct                     |
| 5   | Switch-II label overlaps the source set at A11, C12, G13, K16, P34                                                   | PARTIALLY CONFIRMED   | Identities and the overlap are exact; but only **G13 and K16** are annotated nucleotide-binding residues                        |
| 6   | Those residues are "at graph distance zero from the source"                                                          | PARTIALLY CONFIRMED   | True only as self-distance. The operative fact is **set membership**; the distance reading does not generalise                  |
| 7   | `6OIM` `covale` A/CYS12.SG → A/MOV303.C25 at 1.805 Å                                                                 | CONFIRMED             | `_struct_conn` row `covale1`, `pdbx_dist_value` 1.805; MOV is chain A auth 303                                                  |
| 8   | `4OBE` residue 12 is GLY in both chains, no mutation, `rcsb_mutation_count = 0`                                      | CONFIRMED             | Precision note: `_struct_ref_seq_dif` is **not empty** — 7 rows per chain, none a mutation, none at 12                          |
| 9   | `MYR` contacts 16 of 20 labels, 3.29 Å, strict subset of asciminib's 20                                              | CONFIRMED (substance) | Independent Arpeggio: 13 vs 17 residues, 12 shared. Exact counts are cutoff-specific and were not recomputed                    |
| 10  | `5TBY` SWISS-MODEL on `3JBH`, rigid fit, 20 Å, 954 residues, 0 het, 41 covale at 1.083 Å, methodology "experimental" | CONFIRMED             | Every element verified, including `41` `covale` rows with minimum `pdbx_dist_value` **1.083**                                   |
| 11  | Mavacamten is `XB2`, in exactly six entries                                                                          | CONFIRMED             | Re-run today: still exactly **6** — `8QYQ`, `8QYR`, `9GZ1`, `9GZ2`, `9YP9`, `9YR7`                                              |
| 12  | `5MO4` is ternary: asciminib (`AY7`) **and** nilotinib (`NIL`)                                                       | CONFIRMED             | Entities 2 and 3, both chain A                                                                                                  |
| 13  | `1OPL` carries K29R, E30D, D382N; `2G2H` carries H396P = H415P                                                       | PARTIALLY CONFIRMED   | `2G2H` exact. `1OPL`: the record does say all three, but the repo's own audit calls two of them "phantom" — that gloss is wrong |

**Where the organisers and the repository disagree, the repository is right** — claim 4, the
identity of the `1OPL` ATP-site inhibitor. There is no other disagreement between them.

---

## 1. `6C1H` is an actin-bound myosin-Ib complex, not MYH7, and contains no mavacamten

**Verdict: CONFIRMED.**

Entity composition and organisms, from `https://www.ebi.ac.uk/pdbe/api/pdb/entry/molecules/6c1h`:

| entity | name                         | chem_comp | chains | organism (tax_id)              |
| ------ | ---------------------------- | --------- | ------ | ------------------------------ |
| 1      | Actin, alpha skeletal muscle | —         | A–E    | _Oryctolagus cuniculus_ (9986) |
| 2      | Unconventional myosin-Ib     | —         | P      | _Rattus norvegicus_ (10116)    |
| 3      | Calmodulin-1                 | —         | R      | **unidentified (32644)**       |
| 4      | ADENOSINE-5'-DIPHOSPHATE     | `ADP`     | A–E    | —                              |
| 5      | MAGNESIUM ION                | `MG`      | A–E    | —                              |

UniProt accessions, from `https://www.ebi.ac.uk/pdbe/api/mappings/uniprot/6c1h`:
**P68135** (`ACTS_RABIT`) → A–E; **Q05096** (`MYO1B_RAT`) → P; **P0DP23** (`CALM1_HUMAN`) → R.

Entry-level, from the RCSB GraphQL `entries` query: title "High-Resolution Cryo-EM Structures
of Actin-bound Myosin States Reveal the Mechanism of Myosin Force Sensing";
`exptl.method` ELECTRON MICROSCOPY; `resolution_combined` **3.9**; `polymer_entity_count` 3;
`nonpolymer_entity_count` **2**; `deposited_nonpolymer_entity_instance_count` 10;
released 2018-01-31.

No MYH7: no entity references P12883. No mavacamten: the only non-polymer components are `ADP`
and `MG`, and the `XB2` entry list (§11) does not contain `6C1H`.

**Precision note.** "from rabbit/rat" covers the two chains whose organism the deposition
states. The calmodulin chain is deposited with organism _unidentified_ (tax_id 32644); the
human assignment P0DP23 comes from SIFTS, not from the depositors. This does not change the
conclusion.

---

## 2. `9GZ2` is a 2.9 Å human MYH7–mavacamten complex

**Verdict: CONFIRMED on every element checked.**

| Element                | Finding                                                                                                                                                      | Source                                                                              |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------- |
| Method                 | ELECTRON MICROSCOPY                                                                                                                                          | RCSB GraphQL `exptl.method`                                                         |
| Resolution             | **2.9 Å**                                                                                                                                                    | `rcsb_entry_info.resolution_combined`                                               |
| Title                  | "Beta-cardiac heavy meromyosin motor domain in the primed state complexed to mavacamten"                                                                     | `struct.title`                                                                      |
| UniProt                | **P12883**, _Homo sapiens_, expression host _Mus musculus_                                                                                                   | `polymer_entity/9GZ2/1`; PDBe `molecules`                                           |
| Mavacamten present     | entity 5, `chem_comp_ids: XB2`, chain A                                                                                                                      | PDBe `molecules/9gz2`                                                               |
| Other ligands          | `MG`, `ADP`, `PO4`                                                                                                                                           | same                                                                                |
| Chain count            | **1 polymer entity, 1 instance, chain A**                                                                                                                    | `polymer_entity_count` 1, `deposited_polymer_entity_instance_count` 1               |
| Modelled residues      | **764** — observed auth 3–202, 214–624, 644–796                                                                                                              | `deposited_modeled_polymer_monomer_count`; PDBe `polymer_coverage/9gz2`             |
| Chimera?               | **No.** One source organism for the polymer; no GCN4, no GFP                                                                                                 | `rcsb_entity_source_organism`; PDBe `molecules`                                     |
| Non-human light chain? | **None modelled.** No light-chain entity exists in this entry                                                                                                | PDBe `molecules/9gz2` (5 entities, 1 polymer)                                       |
| Construct              | 1145 aa; entity 1–1137 aligns to P12883 2–1138; one annotated variant at entity position 1123 (= UniProt 1124); 8-residue expression tag at entity 1138–1145 | `polymer_entity/9GZ2/1`, `rcsb_polymer_entity_align`, `rcsb_polymer_entity_feature` |

The repository records the variant as **S1124A** and the tag at auth 1139–1146. The _position_
maps exactly (entity 1123 ↔ UniProt/auth 1124; tag entity 1138–1145 ↔ auth 1139–1146). The
residue identities S→A were not independently confirmed and are not load-bearing: both lie
outside the modelled range 3–796.

Two things worth stating plainly, because the entry title invites a wrong reading. The sample
is heavy meromyosin, but the **deposited model is one heavy-chain motor domain and nothing
else** — no second head, no ELC, no RLC. And the observed gaps 203–213 and 625–643 are exactly
the two gaps `docs/benchmark/primary/README.md` §2 reports for this arm, an independent
cross-check of that row.

---

## 3. `8QYR` and `9GZ1` as alternatives, plus `8QYQ`, `9YP9`, `9YR7`

**Verdict: PARTIALLY CONFIRMED.** Both named entries are genuine β-cardiac myosin–mavacamten
complexes, so "possible alternatives" is factually sound. The correction is on species and
construct: **`8QYR` is bovine, not human**, and `9GZ1`'s light chains are mouse. Read after
the preceding sentence ("`9GZ2`, a 2.9 Å human MYH7–mavacamten complex"), the reply reads as
if all three were the same kind of object. They are not.

All rows below: RCSB GraphQL `entries` + `polymer_entities`, and PDBe `molecules/{id}`.

| PDB    | Method |   Res. Å | Heavy chain UniProt / organism                              | Light chains                                | Ligands                                 | Modelled monomers | Released   |
| ------ | ------ | -------: | ----------------------------------------------------------- | ------------------------------------------- | --------------------------------------- | ----------------: | ---------- |
| `8QYR` | X-ray  | **1.80** | **Q9BE39, _Bos taurus_**                                    | none                                        | `XB2`, `ADP`, `BEF`, `MG`, `SO4`, `EDO` |               711 | 2023-12-13 |
| `8QYQ` | X-ray  |     2.61 | **Q9BE39, _Bos taurus_**                                    | Myosin light chain 3, _**Bos taurus**_      | `XB2`, `ADP`, `BEF`, `MG`, `FMT`, `GOL` |              1793 | 2023-12-13 |
| `9GZ2` | EM     |     2.90 | **P12883, _Homo sapiens_**                                  | none modelled                               | `XB2`, `ADP`, `MG`, `PO4`               |               764 | 2025-03-12 |
| `9GZ1` | EM     |     3.70 | **P12883, _Homo sapiens_** (chains A, B)                    | **P05977 ELC / P97457 RLC, _Mus musculus_** | `XB2`, `ADP`, `MG`, `PO4`               |              2383 | 2025-03-12 |
| `9YP9` | EM     |     3.00 | **chimera**: P12883 + **P03069 (GCN4)** + **P42212 (eGFP)** | **mouse** P05977 / P97457                   | `XB2`, `ADP`, `PO4`                     |              2468 | 2026-04-08 |
| `9YR7` | EM     |     3.00 | **chimera**: P12883 + P03069 + P42212                       | **mouse** P05977 / P97457                   | `XB2`, `ADP`, `PO4`                     |              2454 | 2026-04-08 |

Every accession, organism and resolution in `audit/cardiac-myosin.md` §10.1 reproduces here.
`8QYR`'s entity description is "Myosin-7" from _Bos taurus_, accession Q9BE39 — so the
1.80 Å resolution that makes it attractive comes with a species substitution, which the
organisers' one-line mention does not flag. `9GZ1`'s 3.7 Å and mouse light chains are the
corresponding cost on the other named alternative.

---

## 4. `1OPL` ligands, and PD180970 versus PD166326

**Verdict: PARTIALLY CONFIRMED. The ligand placement is exactly right; the compound name is
wrong. The repository's `PD166326` is correct and the organisers' `PD180970` is not.**

Placement, from `https://www.ebi.ac.uk/pdbe/api/pdb/entry/molecules/1opl`:

| entity | chem_comp | name                                                                                               | chains      |
| ------ | --------- | -------------------------------------------------------------------------------------------------- | ----------- |
| 1      | —         | Tyrosine-protein kinase ABL1 (537 aa)                                                              | A, B        |
| 2      | **`MYR`** | MYRISTIC ACID                                                                                      | **A only**  |
| 3      | **`P16`** | 6-(2,6-dichlorophenyl)-2-{[3-(hydroxymethyl)phenyl]amino}-8-methylpyrido[2,3-d]pyrimidin-7(8H)-one | **A and B** |

So: chain A carries both, chain B carries the ATP-site inhibitor and no myristate. Exactly as
the reply states. That `MYR` sits in the myristoyl pocket is confirmed independently in §9.

Compound identity. `https://data.rcsb.org/rest/v1/core/chemcomp/P16`:

- `chem_comp.formula` = **C21 H16 Cl2 N4 O2**, `formula_weight` 427.283
- `rcsb_chem_comp_synonyms`: **"PD166326"** (provenance _PDB Reference Data_) and
  **"PD-166326"** (provenance _DrugBank_)
- `rcsb_chem_comp_related`: DrugBank **DB08339**, PubChem **447700**, ChEMBL **CHEMBL327127**

PubChem CID 447700 (`/rest/pug/compound/cid/447700/property/...`): formula **C21H16Cl2N4O2**,
IUPAC name "6-(2,6-dichlorophenyl)-2-[3-(hydroxymethyl)anilino]-8-methylpyrido[2,3-d]pyrimidin-7-one".

PD180970 is a **different molecule**. PubChem `/compound/name/PD180970/property/...` returns
CID **5311104**, formula **C21H15Cl2FN4O**, IUPAC name
"6-(2,6-dichlorophenyl)-2-(4-fluoro-3-methylanilino)-8-methylpyrido[2,3-d]pyrimidin-7-one".
It differs from `P16` at the aniline substituent — 4-fluoro-3-methyl instead of
3-hydroxymethyl — and therefore in formula: one fluorine and one fewer oxygen. PD180970 has its
own ABL1 structure, **`2HZI`**, titled "Abl kinase domain in complex with PD180970" (RCSB
entry title). It is not in `1OPL`.

Corroboration from the deposition side: chem comp `P16` appears in exactly four entries —
`1opk`, `1opl`, `2fo0`, `2g2h` (`https://www.ebi.ac.uk/pdbe/api/pdb/compound/in_pdb/P16`).
`1OPK` and `1OPL` are both Nagar _et al._, _Cell_ 112:859 (2003),
doi:10.1016/s0092-8674(03)00194-6 (title and DOI verified at Europe PMC, EXT_ID:12654251). The
published abstract names only STI-571 and does not name the pyridopyrimidine; the full text
sits behind a 403 for automated fetches, so the compound identity here rests on the wwPDB
Chemical Component Dictionary and its DrugBank/PubChem cross-references, which is the stronger
source for "what molecule is in this file" in any case.

**Correction for the organisers:** the ATP-site inhibitor in `1OPL`, in both chains, is
**PD166326** (`P16`). The rest of the sentence — chain A has myristate in the myristoyl
pocket, chain B does not, both chains hold the ATP-site inhibitor — is confirmed.

The reply's substantive instruction is unaffected: stripping all non-protein components and
using chain B is a well-posed instruction whatever the inhibitor is called.

---

## 5. The five overlapping KRAS residues

**Verdict: PARTIALLY CONFIRMED.**

**Residue identities: correct.** From the UniProt P01116 sequence
(`https://rest.uniprot.org/uniprotkb/P01116.json`), residues 1–38 read
`MTEYKLVVVGAGGVGKSALTIQLIQNHFVDEYDPTIED`, giving **A11, G12, G13, K16, P34**.

Numbering is offset 0 in the deposited entries, so those positions are the auth numbers:
`4OBE` entity sequence begins `GMTEYKLVVVGAGGVGKSALTIQLIQNHFVDEYDPTIEDSY` with entity
positions 2–170 aligned to P01116 1–169 (`polymer_entity/4OBE/1`), and chain A is observed at
auth 1–169, chain B at auth 0–169 (PDBe `polymer_coverage/4obe`). In `6OIM`,
`_struct_ref_seq_dif` records auth **12 CYS** against db **GLY**, `details = variant` — so
"C12" is right for the holo and "G12" for the apo.

**The overlap with the frozen source set: exact.** From
`docs/benchmark/primary/frozen.json`, arm `kras_g12c_mandated`:

```
label_residues (21) : 9 10 11 12 13 16 34 58 59 60 61 62 63 68 69 72 95 96 99 100 103
active_site    (23) : 11 12 13 14 15 16 17 18 28 29 30 32 33 34 36 57 116 117 119 120 145 146 147
intersection   ( 5) : 11 12 13 16 34
scoreable      (16) : 21 - 5
n_candidates        : 169 - 23 = 146
```

The five the organisers name are exactly the five the freeze removes. Point 2 of the reply's
"what it forces" is correct.

**"Genuinely a GDP/Mg contact": true for two of the five, not for the other three.** Three
independent annotations agree, and none of them places residue 11, 12 or 34 at the nucleotide.

_UniProt P01116 `BINDING` features_ (`?fields=ft_binding`): GTP at **13, 14, 15, 16, 17, 18**;
**28, 29, 30**; **116, 117, 119**; **145, 146, 147**. Mg²⁺ at **17** and **57**. No 11, no 12,
no 34.

_Deposited `_struct_site_gen` records_ (PDBj Mine2, `struct_site` details verified as
"BINDING SITE FOR RESIDUE GDP/MG ..."), protein residues only:

| entry  | GDP site                                            | Mg site |
| ------ | --------------------------------------------------- | ------- |
| `4OBE` | 13 14 15 16 17 18 28 30 116 117 119 120 145 146     | 17      |
| `4LDJ` | 13 14 15 16 17 18 30 32 116 117 119 120 145 146 147 | 17      |
| `6OIM` | 13 14 15 16 17 18 28 30 116 117 119 120 145 146 147 | 17      |

_PDBe Graph API contact analysis_ for `4OBE` bound molecule `bm1` (GDP A 201) returns the same
14 protein residues as the `4OBE` row above, with interaction types (hbond, polar, vdw_clash,
weak_hbond). Residues 11, 12 and 34 appear in none of them.

For completeness, the same `6OIM` query returns the **`MOV` site** as
`V9 G10 C12 K16 P34 A59 G60 Q61 E62 E63 R68 M72 H95 Y96 Q99 V103` plus `GDP 302` — so
sotorasib genuinely contacts C12, K16 and P34, and genuinely touches the GDP. The switch-II
pocket does border the nucleotide. That is not in dispute.

**What this changes.** All five residues are in the repository's frozen source set, because
that set is defined as _every protein residue with a heavy atom within 4.5 Å of any GDP or MG
heavy atom_ (`allo.inputs.active_site` → `allo.structure.pdb.contacts`, a plain minimum
heavy-atom distance). A 4.5 Å shell is broader than a binding site. Under the curated and the
computed annotations alike, **only Gly13 and Lys16 are nucleotide-binding residues**;
Ala11, Gly12/Cys12 and Pro34 are second-shell. The checker could not recompute the 4.5 Å shell
without local compute, so this does **not** refute the freeze — the freeze is internally
consistent and re-derivable by `allo benchmark verify`. It refutes the _description_.

Practical consequence: the exclusion the organisers mandate stands, because it is justified by
source-set membership (§6), which is a property of the repository's own rule and is verified.
But a sentence calling all five "nucleotide-site residues" overstates three of them, and
`manifest.yaml`'s `_kras_evidence` line "5 of the 21 labels are active-site residues at 0.0 Å"
inherits the same overstatement — the 0.0 Å there is a _self_-distance to the source set, not a
distance to GDP.

---

## 6. "Graph distance zero from the source"

**Verdict: PARTIALLY CONFIRMED. It is true, but only as a restatement of membership, and the
distance reading does not generalise.**

What is literally true:

1. The five residues are **members** of the source set (§5).
2. If distance to a set is defined as the minimum over its members, then a member's distance to
   the set is 0 by the definition of a metric, on any graph and under any edge rule. No path is
   involved.
3. The frozen `distance_to_active_site.min` for `kras_g12c_mandated` is **0.0**, and that is
   the Euclidean Cα version of the same self-distance, not a separate finding.

What is not true, or not established:

4. "Graph distance zero" is not a property those residues have _in addition to_ being source
   residues. It is the same fact restated.
5. The inference does not extend. A residue at graph distance **1** — a direct contact of a
   source residue, on the frozen 4.5 Å graph — is not a source residue and is not excluded by
   the repository's rule. If the organisers' criterion were read as a distance criterion, it
   would have no principled stopping point, and the repository's own reasoning gives the reason
   not to adopt one: CASBench reports that "in **30%** of cases, the catalytic and allosteric
   sites either overlap or share a common border"
   (doi:10.32607/20758251-2019-11-1-74-80, quoted in `primary/README.md` §1), so a distance
   filter on a label set discards roughly a third of curated allosteric sites.

`src/allo/benchmark.py` states the same thing in a comment at the point of enforcement: "A
label that is itself a source residue scores maximally by construction, so it measures nothing.
That is set membership, not distance."

So: the organisers' conclusion is right and their stated reason is a coincidence on this label
set. `03-kras-mask.md` is correct to record the two as agreeing here and not in general.

---

## 7. `6OIM` covalent link CYS12.SG → MOV303.C25 at 1.805 Å

**Verdict: CONFIRMED.**

`https://files.rcsb.org/header/6OIM.cif`, `_struct_conn` category, row `covale1`:
partner 1 chain A, `CYS`, `SG`; partner 2 `MOV`, `C25`; **`pdbx_dist_value` 1.805**. The
remaining six rows are `metalc` (Mg²⁺ coordination) at 2.157–2.166 Å.

Two numbering details, both check out:

- The row names `CYS 26`, which is `label_seq_id`. The entity carries a 14-residue N-terminal
  tag at auth −13…0 (`_struct_ref_seq_dif` rows `initiating methionine` and `expression tag`),
  so `label_seq 26` ↔ **auth 12**. `_struct_ref_seq_dif` independently records auth 12 as `CYS`
  against db `GLY`.
- `MOV` is at chain A, **auth residue 303**
  (`https://www.ebi.ac.uk/pdbe/api/pdb/entry/ligand_monomers/6oim`: MG 301, GDP 302, MOV 303).

`_struct_ref_seq_dif` also confirms the rest of the genotype the repository reports for `6OIM`:
51 SER←CYS, 80 LEU←CYS, 118 SER←CYS, all `engineered mutation`.

---

## 8. `4OBE` residue 12 is GLY in both chains, no mutation, `rcsb_mutation_count = 0`

**Verdict: CONFIRMED, with one precision note.**

- `https://data.rcsb.org/rest/v1/core/polymer_entity/4OBE/1`: `entity_poly.rcsb_mutation_count`
  = **0**; `pdbx_description` "GTPase KRas"; `auth_asym_ids` **A, B** (one entity, two chains,
  so residue 12 is the same residue type in both); reference **P01116**, entity 2–170 ↔
  reference 1–169.
- The entity sequence begins `GMTEYKLVVVGAGGVGKSALTIQLIQNHFVDEYDPTIEDSY`. With entity position
  2 = UniProt 1, entity position 13 = **UniProt 12 = G**. Auth numbering is offset 0 (chain A
  observed 1–169, chain B 0–169), so **auth 12 is GLY**.

**Precision note.** `_struct_ref_seq_dif` is **not empty**. PDBe
`mutated_AA_or_NA/4obe` returns 7 rows per chain: one `Expression tag` GLY (auth 0 in chain B,
unnumbered in chain A) and six `Conflict` rows at auth **151, 153, 165, 166, 167, 168**, in the
C-terminal region. **None is typed `Engineered mutation`, and none is at residue 12.** The
repository's sentence "`_struct_ref_seq_dif` lists no mutation" is true as written and would be
sharper as "lists no engineered mutation, and nothing at residue 12".

---

## 9. `MYR` contacts 16 of 20 labels, nearest 3.29 Å, a strict subset of asciminib's 20

**Verdict: CONFIRMED in substance. The exact counts are cutoff-specific and were not
independently recomputed.**

Independent contact analysis, PDBe Graph API (`bound_molecule_interactions`):

| bound molecule           | interacting protein residues (auth)                                 |   n |
| ------------------------ | ------------------------------------------------------------------- | --: |
| `1OPL` bm1 = `MYR` A 538 | 356 359 360 363 448 451 452 481 487 **512** 521 525 529             |  13 |
| `5MO4` bm2 = `AY7` A 602 | 356 359 360 363 448 451 452 453 454 456 481 482 483 487 521 525 529 |  17 |

Intersection **12**; `MYR \ AY7` = {512} only; Jaccard 12/18 = 0.67. Compare the repository's
4.5 Å heavy-atom sets: `MYR` 16 residues, `AY7` 20, intersection 16, Jaccard 0.80. The two
criteria differ, and the difference is entirely accounted for by strictness: Arpeggio drops
482/483/484 from the `MYR` set (repo distances 3.93/4.15/3.99 Å) and drops 512 from the `AY7`
set (repo distance 3.63 Å).

**That the annotations are strictly tighter than 4.5 Å is demonstrated, not assumed.** The
deposited `_struct_site_gen` record for the same ligand — `1OPL` site `AC1`, details "BINDING
SITE FOR RESIDUE MYR A 538" — lists only **four** residues: LEU 360, GLU 481, ILE 521,
LEU 529. Three criteria on one ligand give 4, 13 and 16 residues. This is why the absence of
KRAS 11/12/34 from the annotations in §5 is reported as "not annotated as nucleotide-binding"
rather than as a refutation of a 4.5 Å measurement.

The claim's substance is confirmed by every criterion: the myristate occupies the asciminib
pocket in the mandated apo input, and its contact set is essentially contained in asciminib's.
The specific figures 16/20, 3.29 Å and Jaccard 0.80 are repository measurements at 4.5 Å that a
reader can re-derive with `allo benchmark verify`; they were not reproduced here.

One supporting fact does check out exactly: `1OPL` has **no `_struct_conn` category at all**
(`files.rcsb.org/header/1OPL.cif`), so there are zero `covale` rows and the myristate is a
free, non-covalent ligand — which is the basis of the audit's finding that deleting it is
coordinate-neutral.

---

## 10. `5TBY` is a SWISS-MODEL homology model on a tarantula template

**Verdict: CONFIRMED. Every element.**

| Element                                           | Finding                                                                                                                                                                                                                                         | Source                                                                       |
| ------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| SWISS-MODEL, tarantula template `3JBH`, rigid fit | `struct.title` verbatim: "…OBTAINED BY HOMOLOGY MODELING (USING SWISS-MODEL) OF HUMAN SEQUENCE FROM APHONOPELMA HOMOLOGY MODEL (PDB-3JBH), RIGIDLY FITTED TO HUMAN BETA-CARDIAC NEGATIVELY STAINED THICK FILAMENT 3D-RECONSTRUCTION (EMD-2240)" | RCSB GraphQL `struct.title`                                                  |
| Rigid-body fit, again from the data               | `_em_3d_fitting`: `ref_protocol` = **RIGID BODY FIT**, `ref_space` = REAL, `target_criteria` = CORRELATION COEFFICIENT                                                                                                                          | PDBj Mine2, `em_3d_fitting`                                                  |
| Deposited at 20 Å                                 | `resolution_combined` **20.0**; `REMARK 2 RESOLUTION. 20.00 ANGSTROMS.`                                                                                                                                                                         | RCSB GraphQL; `files.rcsb.org/header/5TBY.pdb`                               |
| Method                                            | `EXPDTA ELECTRON MICROSCOPY`                                                                                                                                                                                                                    | same                                                                         |
| 954 modelled residues in chain A                  | chain A observed **6–959** = 954 residues (total 2528 across six chains)                                                                                                                                                                        | PDBe `polymer_coverage/5tby`; `deposited_modeled_polymer_monomer_count` 2528 |
| Zero heteroatoms                                  | `nonpolymer_entity_count` **0**, `deposited_nonpolymer_entity_instance_count` **0**                                                                                                                                                             | RCSB GraphQL                                                                 |
| **41 `covale` records**                           | `select conn_type_id, count(*), min(pdbx_dist_value), max(pdbx_dist_value) from struct_conn where pdbid='5tby' group by conn_type_id` → one row: **`covale`, 41, 1.083, 1.644**                                                                 | PDBj Mine2 SQL                                                               |
| "distances such as 1.083 Å"                       | **1.083 is the exact minimum** of `pdbx_dist_value` across those 41 rows                                                                                                                                                                        | same query                                                                   |
| `structure_determination_methodology`             | **experimental**                                                                                                                                                                                                                                | RCSB GraphQL `rcsb_entry_info`                                               |

The single SQL row is worth restating: **all 41 `_struct_conn` records are `covale`, none is
`metalc` or `disulf`, and every one of them is between 1.083 and 1.644 Å.** The repository's
caution — report the measurables, do not call the entry "not experimental" — is the correct
framing, and RCSB does classify it as `experimental`.

---

## 11. Mavacamten is `XB2` and appears in exactly six entries — re-run today

**Verdict: CONFIRMED. The list is unchanged as of 2026-09-02.**

Two independent searches, both run today:

- RCSB Search API, `rcsb_nonpolymer_entity_container_identifiers.nonpolymer_comp_id`
  `exact_match` `"XB2"`, `return_type: entry`, `return_all_hits: true` →
  **`total_count`: 6**; result set **8QYQ, 8QYR, 9GZ1, 9GZ2, 9YP9, 9YR7**.
- PDBe `https://www.ebi.ac.uk/pdbe/api/pdb/compound/in_pdb/XB2` → **6** entries:
  `8qyr`, `9gz1`, `8qyq`, `9gz2`, `9yr7`, `9yp9`.

The two agree exactly and match the set frozen in `audit/cardiac-myosin.md` §10.1. **No new
mavacamten entry has appeared.** `6C1H` is not among them (§1).

---

## 12. `5MO4` is a ternary complex containing asciminib and nilotinib

**Verdict: CONFIRMED.**

`https://www.ebi.ac.uk/pdbe/api/pdb/entry/molecules/5mo4`:

| entity | type           | name                                  | chem_comp | chains |
| ------ | -------------- | ------------------------------------- | --------- | ------ |
| 1      | polypeptide(L) | Tyrosine-protein kinase ABL1 (495 aa) | —         | A      |
| 2      | bound          | Nilotinib                             | **`NIL`** | A      |
| 3      | bound          | asciminib                             | **`AY7`** | A      |
| 4      | water          | water                                 | `HOH`     | A      |

The deposited `_struct_site_gen` records list two ligand sites in chain A — one of 19 residues
running from TYR 272 to PHE 401 (the ATP cleft, nilotinib) and one of 13 residues from ALA 356
to VAL 525 (the myristoyl pocket, asciminib) — so the two occupy separate, non-overlapping
sites, as the repository states.

---

## 13. `1OPL` K29R / E30D / D382N, and `2G2H` H396P = H415P

**Verdict: PARTIALLY CONFIRMED.** The `2G2H` half is exact. The `1OPL` half is exactly what the
deposited record says, but the repository contradicts itself about it elsewhere, and that
contradiction should be resolved in favour of the manifest.

### `2G2H` — CONFIRMED exactly

`https://files.rcsb.org/header/2G2H.cif`:

- `_struct_ref`: `db_name` UNP, `pdbx_db_accession` **P00519**, `pdbx_align_begin` 229.
- `_struct_ref_seq`: auth **248–531** ↔ db **229–512**, chains A and B. Offset **+19**.
- `_struct_ref_seq_dif`: auth **415 PRO** ← db **HIS 396**, `details = engineered mutation`,
  on both chains; plus three cloning-artifact rows at auth 245–247 (GLY, HIS, MET).
- `_struct.title` "A Src-like Inactive Conformation in the Abl Tyrosine Kinase Domain";
  X-RAY DIFFRACTION; `_refine.ls_d_res_high` **2.0**.

PDBe `mutated_AA_or_NA/2g2h` returns the same: author residue **415**, PRO, `H→P`,
`Engineered mutation`, chains A and B.

The +19 offset is confirmed from primary sequence, not assumed. UniProt canonical **P00519**
(isoform IA, 1130 aa) begins `MLEICLKLVGCKSKKGLSSSSSCYLEEALQRPVASDFEPQGLSEAARWNSKENLLAGPSE`;
isoform **P00519-2** (IB) begins `MGQQPGKVLGDQRRPSLPALHFIKGAGKKESSRHGGPHCNVFVEHEALQRPVASDFEPQG`.
Aligning the shared region, IA 28 (`A`) ↔ IB 47 (`A`) and the two run in register from there:
**IB numbering = IA numbering + 19**. So auth 415 = canonical 396, and "H396P in 1a numbering =
H415P" is exactly right.

### `1OPL` — the record says all three, but the repository's audit calls two of them phantom

`https://files.rcsb.org/header/1OPL.cif`, `_struct_ref_seq_dif`:

| auth | mon_id | db_mon_id | db seq | details             |
| ---- | ------ | --------- | -----: | ------------------- |
| 29   | ARG    | LYS       |     29 | engineered mutation |
| 30   | ASP    | GLU       |     30 | engineered mutation |
| 382  | ASN    | ASP       |    382 | engineered mutation |

`_struct_ref`: UNP, `ABL1_HUMAN`, **P00519**, `pdbx_align_begin` **1**. PDBe
`mutated_AA_or_NA/1opl` returns the same three as `Engineered mutation`, plus a block of
`Conflict` rows at auth 23–45 and six `Cloning artifact` rows at 532–537, identically on chains
A and B.

So `manifest.yaml`'s sentence — "1OPL carries engineered K29R, E30D, D382N" — is a faithful
reading of the deposited record. **D382N** is additionally real in the coordinates: it knocks
out the HRD catalytic aspartate and is modelled.

**The correction is to `docs/benchmark/primary/audit/bcr-abl1.md` §4, which says:**

> The bogus alignment is also what produced the phantom "engineered mutations" K29R/E30D —
> those positions are inside the IB-specific cap, which has no IA counterpart at all.

That gloss is not supported, and the same file's own table contradicts it. Three findings:

1. The db residues those two rows name are **Lys29** and **Glu30**. Canonical P00519 (isoform
   IA) has **Leu29** and **Gln30**. Isoform IB (P00519-2) has **Lys29** and **Glu30**. So the
   diff rows are written against **isoform IB**, while `_struct_ref` declares the IA canonical
   with a 1:1 alignment from position 1. The entry is internally inconsistent about its own
   reference frame — which is the real defect, and the audit is right about that much.
2. Because the rows are IB-framed, they assert that the construct has **Arg29** and **Asp30**
   where IB has Lys and Glu. That is a genuine sequence difference from IB, not an artefact of
   the IA alignment. The audit's own §4 table records exactly this: "SEQRES vs isoform IB —
   differs at **3** positions (29, 30, 382)". Prose and table disagree; the table is right.
3. Both residues are **unmodelled** — `1OPL` chain A begins at auth 81 — so neither can affect
   the contact graph, the node set or any score. The dispute is about how to describe the
   construct, not about the input.

Recommended repair: in `audit/bcr-abl1.md` §4, replace "phantom engineered mutations" with a
statement of what is actually wrong — the entry's `_struct_ref` declares the isoform-IA
canonical while its `_struct_ref_seq_dif` rows are written against isoform IB, and SIFTS
silently re-aligns to +19. Keep `manifest.yaml` as it stands.

---

## Incidental findings, checked but not on the list

1. **`9GZ2`'s primary citation is still the preprint at RCSB, but the paper is out.**
   `rcsb_primary_citation` for `9GZ2` and `9GZ3` gives McMillan, S.N.; Pitts, J.R.T.; Barua, B.
   _et al._, _bioRxiv_ 2025, doi:10.1101/2025.02.12.637875, PMID 39990378. The peer-reviewed
   version is _Science Advances_, **doi:10.1126/sciadv.aea9335**. `primary/README.md` §5 already
   cites it as "McMillan et al., _Sci Adv_ 2026"; adding the DOI would close the gap, and would
   also make clear that this is a **different paper** from doi:10.1126/sciadv.aed6472
   (Somavarapu, Ge, Yengo _et al._), which is the citation for `9YP9`/`9YR7`.
2. **`4OBE`'s six `Conflict` rows** at auth 151, 153, 165–168 sit in the C-terminal region and
   are not mutations. Worth one line in the audit so a future reader does not rediscover them
   and mistake them for construct engineering.
3. **`8QYR` is the highest-resolution mavacamten complex in existence (1.80 Å X-ray)** and it
   is bovine. If the cardiac-myosin arm is ever revisited, the species/resolution trade is the
   decision, and Q9BE39 vs P12883 is the fact to record.

## What could not be determined with the available tooling

- Any distance measured at a chosen cutoff from coordinates. `1OPL` `MYR` nearest approach
  3.29 Å, the `MYR`/`AY7` 16-of-20 count, the 23-residue 4.5 Å GDP·Mg shell in `4OBE`, and the
  20.5 Å nucleotide-to-label separation in `9GZ3` were all checked against annotations rather
  than recomputed. PDBj Mine2 exposes the mmCIF annotation categories but not `atom_site`
  (`ERROR: relation "atom_site" does not exist`), and no local compute was available.
- Whether Nagar _et al._ 2003 names PD166326 in its body text. The Cell and ScienceDirect full
  texts return HTTP 403 to automated fetches and the paper predates PMC deposition; Europe PMC
  serves the abstract only, which names STI-571 and no pyridopyrimidine. The compound identity
  in §4 rests on the wwPDB Chemical Component Dictionary and its DrugBank/PubChem
  cross-references, which is the more direct evidence for what is in the file.
- The residue identities behind `9GZ2`'s annotated variant at UniProt position 1124. The
  position is confirmed; "S1124A" is not. It lies outside the modelled range and affects
  nothing.
