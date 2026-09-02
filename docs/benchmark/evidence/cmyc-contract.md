# c-Myc (`1NKP`): the evidence a contract needs

Review date **2026-09-02**. Compiled to clear the blocker recorded in
[ADR 0020](../../adr/0020-cmyc-contract-must-precede-method-design.md). It decides nothing.
It assembles what is retrievable, says what each source actually supports, and names what is
still unknown, so that the ADR that freezes the c-Myc contract can be written against
evidence rather than against plausibility.

## Headline

A c-Myc deliverable can be produced and cannot be scored. `1NKP` is a 1.80 Å ternary complex
of the c-Myc and Max bHLHZip regions on double-stranded DNA, carrying two independent copies
of the heterodimer with author numbering offset by 400 between them, an expression-tag
remnant on Myc and an engineered C-terminal Gly-Gly-Cys on both proteins; the c-Myc content
is exactly **82 native residues**, identical in both copies. No deposited structure anywhere
in the PDB shows a drug-like small molecule bound to human c-Myc — the twenty-five entries
that map to UniProt P01106 contain only potassium, chloride, calcium, sulfate, glycerol,
ethanediol, Tris and glutaraldehyde, all of them crystallisation or cryo additives. The only
residue-level binding-site information that exists for c-Myc comes from NMR chemical-shift
work and peptide truncation on the isolated, disordered bHLHZip monomer, it describes three
short sequence segments **inside** the Max dimerisation region, and no source retrieved here
calls any of it allosteric in the strict sense the repository has adopted. There is
consequently no positive class, no propagation source derived from the entry's own contents,
and no instrument: a c-Myc number would not pass through `allo.scoring.score_arm` and would
not be an AUC of anything. The one evaluation route that is both reproducible offline and
defensible is **overlap of the top-5 hit list with the CSP-derived segments of Follis 2008
and Hammoudeh 2009, reported with a hypergeometric null over the 82-residue candidate set,
declared non-blind**, supported by an apo-only pocket-and-hot-spot characterisation of the
predicted region. "Consensus across winning teams" has no precedent as a scientific
evaluation standard and its one documented failure mode — correlated errors between
predictors that share inputs and machinery — is exactly the regime this challenge creates.

**Tags.** `[VERIFIED-DBRECORD]` read live from RCSB, PDBe, UniProt, Europe PMC or Crossref in
this session. `[VERIFIED-FULLTEXT]` quoted from a paper's full text this session.
`[VERIFIED-ABSTRACT]` from the abstract or bibliographic record only. `[DERIVED]` computed
here from retrieved values, by hand, and **must be re-derived in code before use**.
`[UNVERIFIED]` not established from a primary source this session.

---

## 1. The structure

### 1.1 What `1NKP` is

`[VERIFIED-DBRECORD]` `https://data.rcsb.org/rest/v1/core/entry/1NKP`,
`https://www.rcsb.org/structure/1NKP`, `https://files.rcsb.org/header/1NKP.pdb`.

| Field                 | Value                                                       |
| --------------------- | ----------------------------------------------------------- |
| Title                 | `CRYSTAL STRUCTURE OF MYC-MAX RECOGNIZING DNA`              |
| Method                | X-ray diffraction                                           |
| Resolution            | **1.80 Å**                                                  |
| R-work / R-free       | 0.219 / 0.263                                               |
| Space group           | `P 1`                                                       |
| Unit cell             | a 39.244, b 45.128, c 86.484 Å; α 87.91°, β 84.61°, γ 71.5° |
| Deposited / released  | 2003-01-03 / 2003-02-04                                     |
| Clashscore            | 15.06                                                       |
| Ramachandran outliers | 0.0 %                                                       |
| Polymer entities      | 3 (2 protein, 1 DNA) + water                                |
| Assemblies            | 2                                                           |

Primary citation `[VERIFIED-DBRECORD]`: Nair SK, Burley SK. _X-ray structures of Myc-Max and
Mad-Max recognizing DNA: molecular bases of regulation by proto-oncogenic transcription
factors._ **Cell** 2003;112:193–205. doi:10.1016/S0092-8674(02)01284-9

### 1.2 Chains — and a naming collision that will cause a bug

`[VERIFIED-DBRECORD]` `data.rcsb.org/rest/v1/core/polymer_entity/1NKP/{1,2,3}` and
`www.ebi.ac.uk/pdbe/api/pdb/entry/molecules/1nkp`.

| Entity | What it is                                                                | UniProt    | `label_asym_id` | `auth_asym_id`         | Length |
| ------ | ------------------------------------------------------------------------- | ---------- | --------------- | ---------------------- | -----: |
| 1      | 19-mer DNA, `CGAGTAGCACGTGCTACTC`, synthetic, contains the E-box `CACGTG` | —          | A, B, C, D      | **F, G, H, J**         |  19 nt |
| 2      | **Myc proto-oncogene protein**, bHLHZ region, human, _E. coli_ BL21(DE3)  | **P01106** | E, G            | **A, D**               |  88 aa |
| 3      | **Max protein**, bHLHZ region, human, _E. coli_ BL21(DE3)                 | **P61244** | F, H            | **B, E**               |  83 aa |
| 4      | water, 581 copies                                                         | —          | I–P             | A, B, D, E, F, G, H, J |      — |

> **`label_asym_id` A–D are the four DNA strands. `auth_asym_id` A and D are the two c-Myc
> copies.** The two identifier spaces overlap and denote different molecules. The RCSB entry
> page reports the DNA as "chains A-D" (label space) while every residue number in the
> coordinate file is author-space, where A is Myc. Any code that resolves "chain A" without
> declaring which space it means will silently load a DNA strand or a protein depending on
> the parser. `allo.structure.parse_mmcif` must be checked against this entry specifically.

There are **two complete copies** of the Myc:Max:DNA complex in the asymmetric unit
(space group `P 1`).

### 1.3 What is modelled of c-Myc, and in which numbering

`[VERIFIED-DBRECORD]` PDBe polymer coverage (`/pdbe/api/pdb/entry/polymer_coverage/1nkp`),
SIFTS (`/pdbe/api/mappings/uniprot/1nkp`), and PDB `REMARK 465`.

| Chain (auth) | Observed author range | Entity positions   | Missing                                               | Native c-Myc mapped (SIFTS)       |
| ------------ | --------------------- | ------------------ | ----------------------------------------------------- | --------------------------------- |
| **A**        | 897–984 (88 residues) | 1–88, **complete** | none                                                  | auth 900–981 ↔ P01106 **368–449** |
| **D**        | 499–581 (83 residues) | 3–85               | `GLY 497`, `HIS 498`, `GLY 582`, `GLY 583`, `CYS 584` | auth 500–581 ↔ P01106 **368–449** |

The Myc entity sequence is
`GHMNVKRRTHNVLERQRRNELKRSFFALRDQIPELENNEKAPKVVILKKATAYILSVQAEEQKLISEEDLLRKRREQLKHKLEQLGGC`
(88 aa). SIFTS maps only entity positions 4–85 to UniProt. The flanks are construct, not
protein: `GHM` at the N-terminus is an expression-tag remnant — RCSB's own SCOP annotation
for instance `E` labels residues 1–3 `"N-terminal Tags"` — and `GGC` at the C-terminus is
engineered. The Max entity ends `...QVRALGGC` and carries the same addition.

**So the c-Myc content of `1NKP` is 82 native residues, and both copies model exactly the
same 82.** Chain A additionally models 6 non-native residues, chain D one.

`docs/targets.md` currently states that "chain A auth 897–984 and chain D auth 499–581 both
map to UniProt P01106 353–434". The mapped **native** ranges are auth 900–981 and 500–581;
897–899 / 982–984 and 499 are construct and map to nothing. The prose conflates the modelled
range with the mapped range. Correction belongs in the ADR, not edited into `targets.md`
here.

#### The numbering, which has three conventions and one silent trap

`[VERIFIED-DBRECORD]` `https://rest.uniprot.org/uniprotkb/P01106.txt`. UniProt's **displayed
canonical sequence for P01106 is 454 residues** (isoform 2, sequence version 2, updated
2023-02-22). Isoform **P01106-1 is 439 residues and lacks the first 15**; the two forms arise
from alternative initiation at an upstream in-frame CTG versus a downstream ATG.

The published c-Myc literature uses the **439-residue** convention. Two independent checks:

- `[VERIFIED-FULLTEXT]` Sammak et al. 2019 state their constructs as `"c-MYC = 352–437,
MAX = 22–102"`. A bHLHZip ending at 437 is only possible in the 439-residue frame.
- `[VERIFIED-FULLTEXT]` Michel & Cuchillo 2012 write `"c-Myc402–412 (sequence YILSVQAEEQK)"`.
  That 11-mer is present in the `1NKP` Myc entity sequence above.

`[DERIVED]` Combining SIFTS (entity 4–85 ↔ P01106-454 368–449), UniProt's +15 offset, and the
observed author ranges:

```
entity_index  = lit439 - 349          # lit439 = the 439-residue literature convention
P01106-454    = lit439 + 15
1NKP auth (chain A, Myc copy 1) = lit439 + 547
1NKP auth (chain D, Myc copy 2) = lit439 + 147
```

Check: Tyr402 (lit439) → entity 53 → chain A auth **949**, chain D auth **549**; the residue
at entity 53 is the `Y` that opens `YILSVQAEEQK`. The native span is lit439 **353–434**,
P01106-454 **368–449**, chain A auth **900–981**, chain D auth **500–581**.

**These offsets were computed by hand from retrieved strings and must be re-derived
programmatically before any of them is used.** The two Myc copies differ by 400 in author
numbering; the two Max copies by 500 (chain B `auth = entity + 201`, chain E
`auth = entity + 701`). Any hit list must be emitted in a declared canonical convention —
and because the field and UniProt now disagree by 15, the convention has to be named
explicitly, not implied.

### 1.4 Gaps, alternate conformations, and the engineered tether

`[VERIFIED-DBRECORD]` from `files.rcsb.org/header/1NKP.pdb`:

- `REMARK 465` missing residues: chain D `497, 498, 582, 583, 584`; chain E (Max) `702, 703`.
  **All of them are construct flanks.** No native residue is missing from either Myc copy.
- `REMARK 470` missing atoms: chain E `GLU 735` (CG, CD, OE1, OE2) and `LYS 736`
  (CG, CD, CE, NZ). Both in Max, neither in Myc.
- `SSBOND`: **zero lines.** `LINK`, `CISPEP`, `MODRES`, `HET`, `REMARK 400`, `REMARK 999`:
  zero lines. The entry contains no ligand, no metal, no modified residue.
- `HELIX`: chain A `897–926`, `927–932`, `938–982`; chain D `499–526`, `527–532`, `538–581`.
  Each Myc copy is two long helices joined by a short one and a five-residue break. The same
  pattern holds for both Max copies.

`[VERIFIED-FULLTEXT]` Sammak et al. 2019 describe this entry as artificial: _"The only
available structure of a MYC:MAX heterodimer is a c-MYC:MAX bHLHZip complex bound to DNA
containing an E-box motif, tethered by an artificial disulfide bridge engineered by adding a
cysteine residue at the C-terminus."_ That is the `GGC` seen in both entity sequences.

**Unresolved tension.** The deposited header carries no `SSBOND` record, so the disulfide
Sammak describes is not annotated as a bond in `1NKP`. Whether the two `CYS` side chains are
within bonding distance is a coordinate-level question that was not answered here.

**Alternate conformations: not established.** The PDB-format header carries no remark about
alternate conformers, but `altLoc` is an `ATOM`-record column and a `label_alt_id` field, not
a header record, so its absence from the header proves nothing. The check is one pass over
`_atom_site.label_alt_id` in the mmCIF. Recorded as unknown.

### 1.5 The biological assembly includes the DNA

`[VERIFIED-DBRECORD]` `REMARK 350`: **Biomolecule 1 = chains F, G, A, B**; **Biomolecule 2 =
chains H, J, D, E** (author space). RCSB's assembly record for assembly 1 reports
`polymer_entity_instance_count 4`, `polymer_composition "protein/NA"`,
`oligomeric_details "tetrameric"`, `modeled_polymer_monomer_count 209`, global symmetry `C1`
with stoichiometry `A1 B1` over the protein chains and a pseudo-`C2`.

209 = 88 (Myc chain A) + 83 (Max chain B) + 19 + 19 (two DNA strands).

**The biological assembly is the protein–DNA complex, not the heterodimer alone.** The
repository's clause (v) — "the modelled state should be the biological assembly" — therefore
points at a four-chain, two-polymer-type object. This matters because the organisers' answer
to Q2 (`../review/00-official-reply.md`) requires that "all non-protein residues and ligands
must be uniformly stripped": read literally that deletes the DNA, which is the assembly's
functional partner, and leaves open whether Max — a protein — stays.

### 1.6 Every other human c-Myc structure

`[VERIFIED-DBRECORD]` RCSB search API,
`rcsb_polymer_entity_container_identifiers.reference_sequence_identifiers.database_accession
= P01106`, `return_type: entry`: **`total_count` = 25**. PDBe SIFTS `best_structures/P01106`
returns the identical set of 25, independently. Ligand and description fields from the RCSB
GraphQL `entries` endpoint.

| PDB    | Method, Å      | What is modelled of c-Myc (P01106-454 range) | What it is                                               | Non-polymer content    |
| ------ | -------------- | -------------------------------------------- | -------------------------------------------------------- | ---------------------- |
| `1NKP` | X-ray 1.80     | 368–449                                      | Myc:Max bHLHZip **on DNA**, disulfide-tethered construct | none                   |
| `6G6K` | X-ray **1.35** | 366–452                                      | **Myc:Max bHLHZip, DNA-free, no artificial linker**      | `CL`                   |
| `6G6J` | X-ray 2.25     | 366–452                                      | same complex, second crystal form                        | `SO4`                  |
| `6G6L` | X-ray 2.20     | 366–452                                      | same complex, third crystal form, 4 copies               | `SO4`                  |
| `5I4Z` | X-ray 1.95     | 363–454                                      | **apo Omomyc** (Myc bHLHZip with 4 zipper mutations)     | `K`, `CL`, `GOL`       |
| `5I50` | X-ray 2.70     | 365–454                                      | Omomyc on double-stranded DNA                            | none                   |
| `8OTS` | cryo-EM 3.3    | 366–452                                      | OCT4 **and** MYC-MAX co-bound to a nucleosome            | `PTD` (glutaraldehyde) |
| `8OTT` | cryo-EM 3.3    | 368–420                                      | MYC-MAX bound to a nucleosome at SHL+5.8                 | `PTD`                  |
| `1A93` | NMR            | 420–449                                      | Myc:Max heterodimeric **leucine zipper**                 | none                   |
| `2A93` | NMR            | 420–449                                      | same, 40-structure ensemble                              | none                   |
| `6E16` | X-ray 2.40     | 111–140                                      | c-Myc peptide in a ternary c-Myc–TBP–TAF1 structure      | none                   |
| `6E24` | X-ray 3.00     | 111–140                                      | same system                                              | none                   |
| `7T1Y` | X-ray 2.55     | 250–280                                      | Myc **C-terminal degron** on Fbw7–Skp1                   | `SO4`                  |
| `7T1Z` | X-ray 2.77     | 62–81                                        | Myc **N-terminal degron** on Fbw7–Skp1                   | `SO4`                  |
| `1MV0` | NMR            | 70–83                                        | Myc peptide bound to BIN1                                | none                   |
| `4Y7R` | X-ray 1.90     | 275–282                                      | MYC **MbIIIb** peptide on WDR5                           | `EDO`, `TRS`           |
| `8Q1N` | X-ray 1.84     | 273–283                                      | cyclic peptide at the WDR5 WBM site (Myc-derived)        | none                   |
| `1EE4` | X-ray 2.10     | 335–343                                      | c-Myc **NLS** peptide on karyopherin-α                   | none                   |
| `6C4U` | X-ray 2.60     | 69–77                                        | Myc phospho-peptide on an engineered FHA domain          | `GOL`                  |
| `9QNH` | X-ray 1.30     | 290–298                                      | Myc pSer294 phosphopeptide on 14-3-3σ                    | `CA`, `CL`             |
| `2OR9` | X-ray 2.70     | 425–434                                      | 9E10 epitope peptide on the 9E10 Fab                     | none                   |
| `8J2Q` | X-ray 1.92     | 417–427                                      | c-Myc fragment **fused into** cypovirus polyhedrin       | none                   |
| `8X8V` | X-ray 2.00     | 417–427                                      | same                                                     | none                   |
| `8X8S` | X-ray 2.04     | 417–427                                      | same                                                     | none                   |
| `8WLG` | X-ray 2.55     | 417–426                                      | same                                                     | none                   |

Four conclusions follow directly from the table.

1. **No monomer.** Every entry containing more than about thirty residues of c-Myc contains
   it dimerised with Max or with itself (Omomyc). c-Myc alone has never been crystallised.
2. **No longer construct.** The largest c-Myc content anywhere is `5I4Z`'s Omomyc, and that is
   a mutant. Nothing models the transactivation domain, MB0–MBIV, or anything N-terminal of
   residue 363 except as an isolated peptide bound to a partner protein.
3. **No small molecule.** Across all 25 entries the complete non-polymer inventory is
   `K`, `CL`, `CA`, `SO4`, `GOL`, `EDO`, `TRS`, `PTD`. Every one is a salt, a cryoprotectant,
   a buffer component or a crosslinker. **There is no deposited structure of a drug-like
   small molecule bound to human c-Myc.**
4. **`6G6K` is a better structural object than `1NKP` on every axis the repository cares
   about**: 1.35 Å rather than 1.80 Å, no DNA, no artificial disulfide tether, and the same
   bHLHZip. Sammak et al. deposited it precisely because `1NKP` is artificially constrained.
   The organisers' Q1 answer sanctions documented substitution. This is evidence for the ADR,
   not a decision taken here: `CHALLENGE.md` §6 names `1NKP`, and `1NKP` is the only entry
   with the DNA that defines what the basic region is doing.

Citations for the entries used above `[VERIFIED-DBRECORD]`: `6G6J`/`6G6K`/`6G6L` — Sammak S,
Hamdani N, Gorrec F, Allen MD, Freund SMV, Bycroft M, Zinzalla G. _Biochemistry_
2019;58:3144–3154, doi:10.1021/acs.biochem.9b00296. `5I4Z`/`5I50` — Jung LA et al.
_Oncogene_ 2017, doi:10.1038/onc.2016.354. `8OTS`/`8OTT` — Michael AK et al. _Nature_ 2023,
doi:10.1038/s41586-023-06282-3.

---

## 2. What is known about druggable or allosteric sites on c-Myc

### 2.1 Is there a structurally characterised site? No.

Section 1.6 settles it from the database side: no PDB entry contains a small molecule bound
to c-Myc. `[VERIFIED-ABSTRACT]` Obisesan et al. 2025 — the most recent dedicated
medicinal-chemistry paper retrieved — state their own structural basis as docking into
`1NKP` and into the AlphaFold model `AF-P01106-F1-v4`, with **no experimental structure of
the complex solved**. Every residue-level site assignment for c-Myc in the literature comes
from solution biophysics on the isolated bHLHZip: NMR chemical-shift work, circular
dichroism, fluorescence polarisation and peptide truncation.

### 2.2 The compounds and where each is said to bind

All residue numbers below are in the **439-residue convention** (§1.3). The conversion to
`1NKP` author numbering is `chain A auth = lit439 + 547`, `chain D auth = lit439 + 147`
`[DERIVED]`.

| Compound                      | Site, lit439                                                                 | `1NKP` chain A auth `[DERIVED]` | Evidence                                                             | Source                                                                       |
| ----------------------------- | ---------------------------------------------------------------------------- | ------------------------------- | -------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| **10058-F4**                  | **402–409** ("Site I"); other secondary sources give 402–412                 | 949–956 (or 949–959)            | NMR + CD + FP on the isolated bHLHZip monomer                        | Yin 2003 (discovery); Follis 2008; Hammoudeh 2009; quoted from Beaulieu 2020 |
| **10074-G5**                  | **366–375** ("Site II")                                                      | 913–922                         | as above                                                             | Follis 2008; Hammoudeh 2009; quoted from Beaulieu 2020                       |
| **10074-A4**                  | **375–385** ("Site III")                                                     | 922–932                         | as above                                                             | Hammoudeh 2009; quoted from Beaulieu 2020                                    |
| **MYCi361 / MYCi975**         | **366–378**, "the same site as 10074-G5"                                     | 913–925                         | quoted from Beaulieu 2020                                            | Han 2019                                                                     |
| **4da** (α-helix mimetic)     | **363–381**, "targeting the helical conformation"                            | 910–928                         | quoted from Beaulieu 2020                                            | Beaulieu 2020                                                                |
| **MY05** (pyrazolopyridinone) | **402–409**, "π-stacking with Tyr402"                                        | 949–956                         | docking + CD + CETSA + co-IP; no structure                           | Obisesan 2025                                                                |
| **MYCMI-6**                   | not localised to residues in any source retrieved                            | —                               | binds the MYC bHLHZip, K_D 1.6 ± 0.5 µM by SPR                       | Castell 2018                                                                 |
| **KJ-Pyr-9**                  | **unknown**                                                                  | —                               | K_d 6.5 ± 1.0 nM by backscattering interferometry; site not reported | Hart 2014                                                                    |
| **EN4** (covalent)            | **Cys171** — _outside_ the bHLHZip                                           | **absent from `1NKP`**          | covalent cysteine-reactive screen                                    | Boike 2021                                                                   |
| **KI-MS2-008**                | binds **MAX**, not MYC — stabilises the Max homodimer                        | —                               | small-molecule microarray screen                                     | Struntz 2019                                                                 |
| **Omomyc / OMO-103**          | a 91-residue mini-protein occupying the dimerisation interface, not a pocket | whole zipper                    | phase 1 trial, 22 patients                                           | Jung 2017; Garralda 2024                                                     |

Two entries need care.

- **`Cys171` is not in `1NKP`.** `[VERIFIED-ABSTRACT]` Boike et al. name "cysteine 171 of MYC
  within a predicted intrinsically disordered region". The paper's numbering convention was
  not established here, but 171 lies far N-terminal of the bHLHZip in **either** convention
  (353–437 in lit439, 368–452 in P01106-454). The one covalent, cell-active, directly ligand-
  able site on MYC is in a region no c-Myc structure models.
- **The Site I range is not consistent across secondary sources.** Beaulieu 2020 says
  402–409; the widely repeated figure is 402–412, which is the peptide Michel & Cuchillo
  simulated (`YILSVQAEEQK`). Hammoudeh 2009 and Follis 2008 are paywalled and were not read.
  Recorded as an open discrepancy, not resolved.

`[VERIFIED-ABSTRACT]` The mechanism Hammoudeh et al. report is three _independent_ sites:
"three discrete sites within the 85-residue bHLHZip domain", where "binding can occur
simultaneously and independently on the three identified sites", each interaction inducing
only localised structural change "while preserving overall protein disorder and blocking Max
dimerization".

### 2.3 Is any of it allosteric in the strict sense? No source retrieved says so.

The repository's threshold (`../primary/README.md` §1, clause (ii)) is IUPHAR XC §III: a site
that is "nonoverlapping, topographically distinct" from the functional site and
"conformationally linked to" it, with allostery established by a _functional_ experiment.

- A Europe PMC search for `(c-Myc OR MYC) AND allosteric AND bHLHZip` returned 23 records.
  `[VERIFIED-ABSTRACT]` **None claims an allosteric site on c-Myc.** The single allosteric hit
  is Martínez-Cartró et al. 2025 (doi:10.1002/advs.202506068), which reports allosteric
  modulators of **FBW7**, the E3 ligase that degrades MYC — a different protein.
- A Europe PMC search for `MYC AND "cryptic pocket"` returned nothing describing a cryptic or
  transient pocket in MYC or MYC:MAX.
- Every site in §2.2 lies **inside** the bHLHZip segment that must fold to heterodimerise. The
  reported mechanism is local distortion of a segment required for the interface, preventing
  the coupled folding. That is PPI disruption at the interface, which is the opposite of
  clause (ii)'s "nonoverlapping".

`[UNVERIFIED]` Whether ASD or CASBench curates any MYC or MYC:MAX entry. Prior repository
sessions could not query ASD (expired `*.shsmu.edu.cn` certificate, JavaScript-only tables)
or enumerate CASBench; neither was retried here.

**One caveat against over-reading this.** "Topographically distinct" is a statement about a
folded tertiary structure. c-Myc has none in the free state. The concept the repository uses
to license the word "allosteric" may simply not have a referent on this target, which is a
different problem from the sites failing the test.

### 2.4 c-Myc is an intrinsically disordered protein, and what that does to a contact network

Four retrieved statements, in increasing order of consequence for this repository.

1. `[VERIFIED-ABSTRACT]` Follis et al. 2008: _"The basic-helix-loop-helix-leucine-zipper
   domains of the c-Myc oncoprotein and its obligate partner Max are intrinsically disordered
   (ID) monomers that undergo coupled folding and binding upon heterodimerization."_
2. `[VERIFIED-FULLTEXT]` Sammak et al. 2019 assigned the c-MYC bHLHZip NMR spectrum **in the
   absence of Max** and found "the basic region has an intrinsic helical propensity even in
   the absence of its dimerization partner", concluding that recognition proceeds by
   "conformational selection rather than an induced fit". So the free monomer is not
   featureless — but it is an ensemble, not the object in `1NKP`.
3. `[VERIFIED-ABSTRACT]` Yu et al. 2016: _"conventional structure-based approaches cannot be
   applied directly to IDPs, due to their lack of ordered structures."_ Their working method
   was to sample conformations, identify three pockets in representative conformations of
   c-Myc370–409, and screen against all of them; seven compounds bound in vitro.
4. `[VERIFIED-FULLTEXT]` Michel & Cuchillo 2012: _"a single average structure obtained from
   minimization of NMR derived restraints may not be representative of the multiple distinct
   conformations adopted by a disordered protein."_ Their sampling was bias-exchange
   metadynamics, 120 ns per replica.
5. `[VERIFIED-DBRECORD]` The one worked structural account of a small molecule bound to an IDP
   is on a different protein: Robustelli P et al., _J Am Chem Soc_ 2022;144:2501–2510,
   doi:10.1021/jacs.1c07591, on α-synuclein. It is cited here only to fix what "the site" means
   for a disordered chain — a distribution of contacts over an ensemble, not a cavity. That is
   not an object a single N × N contact matrix can represent.

**The implication for this repository is specific and uncomfortable.** The contact graph the
pipeline would build from `1NKP` is the graph of the _bound, DNA-engaged, disulfide-tethered,
fully helical_ state. The state that the published inhibitors bind — and the state a drug
would have to engage — is the free monomer ensemble, which has a different contact graph, or
arguably no persistent one. C6, the elastic-network hypothesis, assumes that contact topology
is the primary driver of signal propagation. That assumption is a statement about a folded
protein with a persistent topology. **On c-Myc the assumption is not merely unvalidated, its
premise is contested by the primary literature on the target.** The two routes that the field
uses to get round this — conformational ensembles (Yu 2016) and metadynamics (Michel &
Cuchillo 2012) — both generate the ensemble by simulation, which is exactly what C2 rules out
of the prediction path.

`[DERIVED, HYPOTHESIS]` One structural consequence is worth measuring rather than asserting.
Each Myc copy is two long helices (`HELIX` records: 897–926, 927–932, 938–982) packed against
Max in a parallel coiled coil. A residue contact graph of a coiled coil is close to
one-dimensional: dominated by `i, i±3, i±4` along each helix plus the heptad register across
the interface. If so, any source-conditioned propagation score on it will be close to a
monotone function of sequence separation from the source, and the distance-only baseline that
`../primary/README.md` §4 already requires will be unusually hard to beat. **This is a
hypothesis with an obvious test — run the distance baseline first — not a finding.**

---

## 3. Evaluating a binding-site prediction with no holo structure

### 3.1 Consensus and ensemble agreement

**What the field does with consensus.** Consensus is used as a _predictor_, and it is
validated against experiment.

- `[VERIFIED-DBRECORD]` MetaPocket 2.0 (Zhang Z et al., _Bioinformatics_ 2011;27:2083–2088,
  doi:10.1093/bioinformatics/btr331) merges eight pocket predictors and reports an improved
  success rate. Its answer key is the experimentally observed ligand position.
- `[VERIFIED-ABSTRACT]` CASP's binding-site category (Gallo Cassarino T, Bordoli L, Schwede T,
  _Proteins_ 2014;82(S2):154–163, doi:10.1002/prot.24495) evaluates predictions on "13
  prediction targets containing **biologically relevant ligands**". There is no consensus-based
  scoring anywhere in the assessment.

- `[VERIFIED-ABSTRACT]` The field's own survey of the area — Zhao J, Cao Y, Zhang L, _Comput
  Struct Biotechnol J_ 2020;18:417–426, doi:10.1016/j.csbj.2020.02.008 — classifies binding-site
  predictors into four families and discusses their evaluation throughout in terms of observed
  ligand positions. Consensus appears as a way to combine predictors, never as a criterion.

**No source retrieved uses agreement between predictors as the criterion of correctness.**
That is the whole of the precedent question, and the answer is negative.

**The documented failure mode is correlated error.**

- `[VERIFIED-ABSTRACT]` Charifson et al. 1999 (doi:10.1021/jm990352k) established consensus
  scoring on the premise that independent scoring functions make independent errors; the
  method's gain is a function of that independence.
- `[VERIFIED-ABSTRACT]` Gao X, Bu D, Xu J, Li M, _BMC Struct Biol_ 2009;9:28,
  doi:10.1186/1472-6807-9-28, state the problem directly: majority voting assumes "all the
  individual servers are equally important and **independent**", and they have to model server
  correlation explicitly (maximum likelihood plus PCA to extract "independent latent servers")
  before consensus becomes reliable. On new-fold targets, plain majority voting reached 13.0 %
  accuracy against their 37 %.
- `[VERIFIED-ABSTRACT]` Won J, Baek M, Monastyrskyy B, Kryshtafovych A, Seok C, _Proteins_
  2019;87:1351–1360, doi:10.1002/prot.25804, report that in CASP13 "higher consensus toward
  models of higher global accuracy appeared even for free modeling targets" because the server
  pool had adopted a common new technique, and that this "pose[s] a new challenge for EMA
  method developers". Consensus measures the composition of the pool, and the pool moves.

**Applied to "consensus across winning teams".** Every team receives the same input (`1NKP`),
under the same constraints (apo-only, no MD, elastic network), building the same class of
object (a residue contact graph), and scoring it with methods drawn from the same small
literature. The independence premise that makes consensus informative is violated by the
design of the challenge itself. Agreement between teams would measure shared method bias.
`[DERIVED]` — but it follows directly from Charifson's and Gao's stated premise, and nothing
retrieved contradicts it.

**What consensus can honestly be.** A _descriptive_ statement — "our top-5 overlaps team X's
by k residues" — with no accuracy claim attached. That is a reproducibility observation, and
it is worth reporting as one.

### 3.2 "Theoretical docking viability", made concrete

Four constructions, each reproducible, each with a stated input and a stated ceiling.

**(a) Pocket detection plus a druggability score on the apo input.**

| Tool                             | What it scores                                                              | Citation                                                                                                                                                                            |
| -------------------------------- | --------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| fpocket + its druggability score | α-sphere pockets; a logistic model over volume, hydrophobicity and polarity | Le Guilloux V, Schmidtke P, Tuffery P, _BMC Bioinformatics_ 2009;10:168, doi:10.1186/1471-2105-10-168; Schmidtke P, Barril X, _J Med Chem_ 2010;53:5858–5867, doi:10.1021/jm100574m |
| DoGSiteScorer                    | grid-based pockets plus a druggability score                                | Volkamer A, Kuhn D, Rippmann F, Rarey M, _Bioinformatics_ 2012;28:2074–2075, doi:10.1093/bioinformatics/bts310                                                                      |
| SiteMap `Dscore`                 | SiteScore/Dscore from site size, enclosure, hydrophilic/hydrophobic balance | Halgren TA, _J Chem Inf Model_ 2009;49:377–389, doi:10.1021/ci800324m                                                                                                               |

Input: one structure. No holo, no MD. What the published validation supports: **separation of
known druggable from known undruggable sites on folded proteins**, calibrated on curated
sets. What it does not support: a _ranking of residues_, which is what this challenge scores.
And the honest anticipation for c-Myc is that a flat, solvent-exposed, two-helix dimerisation
surface scores uniformly low by construction — that is the operational content of calling
c-Myc undruggable. A near-flat score vector carries no ranking information. **This should be
measured before it is relied on.**

**(b) FTMap hot spots.** `[VERIFIED-DBRECORD]` Kozakov D et al., _Nat Protoc_
2015;10:733–755, doi:10.1038/nprot.2015.043; druggability criteria in Kozakov D, Hall DR,
Napoleon RL, Yueh C, Whitty A, Vajda S, _J Med Chem_ 2015;58:9063–9088,
doi:10.1021/acs.jmedchem.5b00586. Computational solvent mapping docks small organic probes
over the whole surface and clusters them; a "hot spot" is a consensus site, and its strength
is the number of probe clusters it holds. Input: one structure. No holo, no MD. Validation:
`[VERIFIED-ABSTRACT]` Landon MR, Lancia DR Jr, Yu J, Thiel SC, Vajda S, _J Med Chem_
2007;50:1231–1240, doi:10.1021/jm061134b, verified computational-solvent-mapping hot spots
against experimentally characterised hot spots from the literature — i.e. **against
alanine-scanning data, not against a holo structure**. That makes FTMap the strongest of the
four routes here, because its own validation precedent is holo-free. Reproducibility caveat:
FTMap is a web server, so the version must be recorded and the run archived.

**(c) Docking a defined ligand set into a defined box, then rescoring.**
`[VERIFIED-DBRECORD]` Trott O, Olson AJ, _J Comput Chem_ 2010;31:455–461,
doi:10.1002/jcc.21334; Eberhardt J, Santos-Martins D, Tillack AF, Forli S, _J Chem Inf Model_
2021;61:3891–3898, doi:10.1021/acs.jcim.1c00203. Needs a box centre and size, a ligand set, an
exhaustiveness and a seed — all four are contract terms, and all four must be frozen before
any prediction exists, or the box is fitted to the answer. Ceilings, both retrieved:

- `[VERIFIED-DBRECORD]` Warren GL et al., _J Med Chem_ 49:5912–5931, doi:10.1021/jm050362n,
  "A Critical Assessment of Docking Programs and Scoring Functions" — docking programs
  reproduce poses far better than scoring functions rank affinities. Crossref's `issued` date
  is 2005 and the issue is conventionally cited as 2006;49(20); the DOI is the authority.
- `[VERIFIED-ABSTRACT]` Karelina M, Noh JJ, Dror RO, _eLife_ 2023;12:RP89386,
  doi:10.7554/eLife.89386 — docking to AlphaFold models, although the pockets are accurate,
  gives pose accuracy "not significantly higher than when docking to traditional homology
  models and ... much lower than when docking to structures determined experimentally without
  these ligands bound". This bears directly on Obisesan 2025's use of `AF-P01106-F1-v4` and on
  any plan to dock into a c-Myc conformation that was not experimentally determined.

A Vina score on a predicted c-Myc region supports one sentence: _a ligand-sized cavity exists
there that accepts a pose with score s_. It does not support "druggable", and it does not
support "allosteric".

**(d) Enrichment of known binders over decoys.** Possible in principle. The known-binder set
for c-Myc is 10058-F4, 10074-G5, 10074-A4, MYCi361/975, MYCMI-6, MY05 and KJ-Pyr-9 — fewer
than ten compounds, several chemically related, most with micromolar or unreproduced
affinities and a long history of promiscuity concerns. `[UNVERIFIED]` The strength of that
concern was not established from a primary source here. An enrichment statistic over such a
set is not interpretable.

### 3.3 Precedent for scoring against mutagenesis or NMR chemical-shift perturbation

This precedent exists, is well established, and is the strongest available route.

- **CSP as the method.** `[VERIFIED-DBRECORD]` Williamson MP, _Prog Nucl Magn Reson Spectrosc_
  2013;73:1–16, doi:10.1016/j.pnmrs.2013.02.001 — the standard reference for using chemical-
  shift perturbation to map a binding site to residues.
- **CSP and mutagenesis treated as experimental interface evidence.** `[VERIFIED-ABSTRACT]`
  Dominguez C, Boelens R, Bonvin AMJJ, _J Am Chem Soc_ 2003;125:1731–1737,
  doi:10.1021/ja026939x — HADDOCK encodes "chemical shift perturbation data resulting from NMR
  titration experiments **or mutagenesis data**" as ambiguous interaction restraints. The field
  accepts CSP and mutagenesis as defining an interface at residue resolution.
- **Hot spots from alanine scanning as the answer key for a computational prediction.**
  Landon 2007 (above) — the direct precedent for validating a _computed_ site against
  _mutational_ data rather than a holo structure.
- **Mutagenesis as an allosteric answer key.** `[VERIFIED-DBRECORD]` Faure AJ et al., _Nature_
  2022;604:175–183, doi:10.1038/s41586-022-04586-4, map energetic and allosteric landscapes of
  binding domains by deep mutational scanning. `[VERIFIED-DBRECORD]` Leander M, Liu Z, Cui Q,
  Raman S, _eLife_ 2022;11:e79932, doi:10.7554/eLife.79932, derive allosteric hotspots in
  homologous proteins from deep mutational scanning plus machine learning. Both produce
  residue-level allosteric labels **with no holo structure anywhere in the derivation**.
- **On c-Myc itself, this is the only evidence class that exists.** Follis 2008 and Hammoudeh
  2009 defined Sites I–III by NMR, CD, fluorescence polarisation and peptide truncation on the
  isolated bHLHZip. That is simultaneously the opportunity — there _is_ a residue-level answer
  key — and the ceiling: it is a set of three sequence segments, at roughly ten-residue
  resolution, on a molecule that is disordered in the state where it was measured.

`[UNVERIFIED]` No paper was found that evaluates a _contact-network or normal-mode_
allosteric-site prediction against CSP data. One Europe PMC search for MYC/Max plus elastic
network, normal mode analysis or residue interaction network returned nothing relevant; the
search was one query and is not exhaustive.

### 3.4 What runs with no holo structure and no molecular dynamics

| Route                                                     | Needs a holo structure? | Needs MD or an ensemble? | Reproducible offline?                        |
| --------------------------------------------------------- | ----------------------- | ------------------------ | -------------------------------------------- |
| fpocket / DoGSiteScorer druggability on the apo input     | no                      | no                       | yes, pinned version                          |
| SiteMap `Dscore`                                          | no                      | no                       | commercial licence required                  |
| FTMap hot spots                                           | no                      | no                       | web server — archive the run                 |
| Vina into a pre-declared box                              | no                      | no                       | yes, with a pinned seed and box              |
| Overlap with the CSP-derived segments of Follis/Hammoudeh | no                      | no                       | yes                                          |
| Consensus across teams                                    | no                      | no                       | **no** — depends on other teams' submissions |
| Yu 2016-style IDP ensemble virtual screening              | no                      | **yes**                  | yes, but the ensemble is simulated           |
| Enrichment of known binders over decoys                   | no                      | no                       | yes, but the binder set is too small         |

**The C2 question this raises, flagged and not answered.** C2 forbids classical MD as an input
to the _prediction_. An MD-derived c-Myc ensemble used only in _evaluation_ is not literally
covered. But it would break offline reproducibility, break parity with the other arms, and
sit awkwardly against ADR 0027's tiering. This belongs in the ADR.

---

## 4. What can honestly be claimed

### 4.1 What a c-Myc result could support

- **That the deliverable set is complete.** `CHALLENGE.md` §8 requires an N × N connectivity
  matrix and a top-5 hit list for four targets. Producing both for `1NKP` satisfies the
  submission requirement, and that is a statement about completeness, not about accuracy.
- **A stated overlap with prior literature.** "k of our top 5 fall inside Site I / II / III as
  reported by Follis 2008 and Hammoudeh 2009", with a hypergeometric probability under uniform
  sampling of the 82-residue candidate set. This has a null and is checkable.
- **An apo-only druggability characterisation of the predicted region**, with the tool, its
  version, its score and its published calibration all named — and with the anticipated
  near-flat score distribution reported whether or not it is flattering.
- **A structural description of what the method found**, in canonical numbering, that a
  medicinal chemist can act on (`docs/FIELD.md`).

### 4.2 What it could not support, and why each is non-comparable

Eight ways a c-Myc number differs in kind, not in degree, from a number on the three scored
disease areas.

1. **No positive class.** The five frozen arms derive `scoreable_label_residues` from an
   effector's 4.5 Å heavy-atom footprint in a holo structure, programmatically, with the
   cutoff and component ID recorded. c-Myc has no effector, no holo entry and therefore no
   derived label set. Anything used as a positive class would be a hand-transcribed sequence
   range from a review article — precisely the practice `docs/targets.md` forbids.
2. **No propagation source derived from the entry.** `kras_g12c_*` uses
   `{from_ligands: [GDP, MG]}`, `bcr_abl1_*` uses `{from_motifs: [VAIK, HRD, DFG]}`,
   `cardiac_myosin_corrected` uses `{from_ligands: [ADP, MG, PO4]}`. c-Myc has no catalytic
   site, no cofactor and no catalytic motif. Every candidate source — the E-box-contacting
   basic residues, the Max interface — is read off a _partner molecule_ that the organisers'
   Q2 answer instructs teams to strip. The source would be a modelling choice made by us, and
   the challenge's primary objective is defined as connectivity **to an active site**.
3. **Prevalence is undefined, so no prevalence-sensitive statistic transfers.** The scored arms
   run 146–743 candidates at 1.6–11.0 % prevalence. c-Myc offers 82 candidates and an
   undefined positive count. AUC-PR is prevalence-dependent; the evaluation layer already
   treats cross-arm comparison of it with care.
4. **The input is a different kind of object.** Every other apo input is a single-chain view of
   one gene product's own crystal. `1NKP` is a four-chain ternary complex of two different
   proteins and two DNA duplexes, in which the protein construct carries an expression tag and
   an engineered disulfide-forming C-terminal tripeptide. Making an input from it requires
   deleting a partner protein and a nucleic acid, which no other arm requires.
5. **The modelling assumption is contested on this target.** C6 assumes contact topology drives
   propagation. The primary literature on c-Myc says the bHLHZip is an intrinsically disordered
   monomer that folds only on binding (Follis 2008), and that a single static structure is not
   representative of it (Michel & Cuchillo 2012). The graph would be the graph of the bound
   state, and the drug-relevant state is not that.
6. **A different measuring instrument.** Protocol version 2 (`../evaluation/README.md`) is
   frozen, and every method calls `allo.scoring.score_arm` and no other path. A c-Myc number
   would not go through it. It is not a different value of the same quantity; it is a
   different quantity.
7. **Not blind, irreversibly.** The candidate sites are published and are transcribed in §2.2
   of this file. Anyone who designs the c-Myc method after reading this has seen the answer
   key. `manifest.yaml`'s `blind:` field would have to record this, and the contract has to be
   frozen — including the evaluation — before a method is designed, which is exactly what
   ADR 0020 requires.
8. **N = 1 with no null.** A single target contributes nothing to a target-level test. The
   floor argument in `../primary/README.md` §1 applies unchanged.

### 4.3 The one route judged most defensible

**Overlap of the top-5 hit list with the CSP-derived segments of Follis 2008 and Hammoudeh
2009, evaluated with a hypergeometric null over the 82 native residues, declared non-blind,
and accompanied by an apo-only pocket-and-hot-spot characterisation (fpocket druggability
plus FTMap) of the predicted region.**

Why this and not the others:

- It is the only route with an answer key that came from **experiment on this target**,
  however coarse. Everything else is a computation scoring a computation.
- Its evidence class has precedent: Landon 2007 validated computed hot spots against
  mutational data; HADDOCK treats CSP and mutagenesis as experimental interface evidence;
  Faure 2022 and Leander 2022 build allosteric answer keys from mutagenesis with no holo
  structure. Consensus-between-predictors has no such precedent, and its documented failure
  mode is the regime this challenge creates.
- It needs no holo structure, no MD, no licence and no other team's submission, so it can be
  frozen before a method exists — which is the property ADR 0020 actually demands.
- It states its own ceiling honestly: three segments at ten-residue resolution, measured on a
  disordered monomer, transcribed from an open-access review because the two primary papers
  are paywalled.

---

## What this cannot settle

- **Alternate conformations in `1NKP`.** The header carries no remark, but `altLoc` is not a
  header record. The check is one pass over `_atom_site.label_alt_id`. Not done.
- **Whether the engineered C-terminal cysteines form a modelled disulfide.** The header has
  zero `SSBOND` lines; Sammak 2019 describes the construct as disulfide-tethered. Needs an
  SG–SG distance from the coordinates.
- **The `[DERIVED]` numbering offsets.** `lit439 + 547` (chain A) and `lit439 + 147` (chain D)
  were computed by hand from retrieved strings. They must be re-derived in code, against the
  deposited bytes, before any hit list uses them.
- **Site I's extent.** 402–409 (Beaulieu 2020) versus 402–412 (widely repeated, and the peptide
  Michel & Cuchillo simulated). Hammoudeh 2009 and Follis 2008 are paywalled and were not read.
- **MYCMI-6's and KJ-Pyr-9's binding sites** at residue resolution. Not reported in either
  abstract; full texts not read.
- **Boike 2021's numbering convention for Cys171.** Not established. The conclusion that 171 is
  outside the bHLHZip holds in both candidate conventions, so nothing here depends on it.
- **Whether ASD or CASBench curates MYC.** Neither database was queried; both were unreachable
  in earlier repository sessions.
- **Whether any elastic-network or residue-network study of `1NKP` exists.** One Europe PMC
  query, noisy, nothing relevant. Not exhaustive; a citation-graph search from Nair & Burley
  2003 would be the proper method.
- **Whether "consensus across winning teams" has ever been used as a scientific evaluation
  standard.** Searched; no precedent found. Absence of evidence from two queries.
- **The promiscuity record of 10058-F4 and 10074-G5.** Widely discussed, not verified here.
- **What the organisers intend by "theoretical docking viability".** Not asked. Given that they
  answered four questions on 2026-09-02, this is the obvious fifth, and it is cheaper to ask
  than to guess.

---

## Bibliography

**Structural records** — all retrieved live 2026-09-02.

- RCSB entry `1NKP`: `https://data.rcsb.org/rest/v1/core/entry/1NKP`,
  `https://www.rcsb.org/structure/1NKP`, `https://files.rcsb.org/header/1NKP.pdb`
- RCSB polymer entities: `https://data.rcsb.org/rest/v1/core/polymer_entity/1NKP/{1,2,3}`
- RCSB polymer entity instance: `https://data.rcsb.org/rest/v1/core/polymer_entity_instance/1NKP/E`
- RCSB assembly: `https://data.rcsb.org/rest/v1/core/assembly/1NKP/1`
- RCSB search API, `database_accession = P01106`, `return_type: entry`,
  `https://search.rcsb.org/rcsbsearch/v2/query`
- RCSB GraphQL `entries` endpoint, `https://data.rcsb.org/graphql`
- PDBe: `/pdbe/api/pdb/entry/molecules/1nkp`, `/polymer_coverage/1nkp`, `/assembly/1nkp`,
  `/pdbe/api/mappings/uniprot/1nkp`, `/pdbe/api/mappings/best_structures/P01106`
- UniProt: `https://rest.uniprot.org/uniprotkb/P01106.txt`

**c-Myc structural biology**

1. Nair SK, Burley SK. X-ray structures of Myc-Max and Mad-Max recognizing DNA: molecular
   bases of regulation by proto-oncogenic transcription factors. _Cell_ 2003;112:193–205.
   doi:10.1016/S0092-8674(02)01284-9
2. Sammak S, Hamdani N, Gorrec F, Allen MD, Freund SMV, Bycroft M, Zinzalla G. Crystal
   structures and nuclear magnetic resonance studies of the apo form of the c-MYC:MAX bHLHZip
   complex reveal a helical basic region in the absence of DNA. _Biochemistry_
   2019;58:3144–3154. doi:10.1021/acs.biochem.9b00296 (PMC6791285, open access)
3. Jung LA, Gebhardt A, Koelmel W, et al. OmoMYC blunts promoter invasion by oncogenic MYC to
   inhibit gene expression characteristic of MYC-dependent tumors. _Oncogene_ 2017.
   doi:10.1038/onc.2016.354
4. Michael AK, Stoos L, Crosby P, et al. Cooperation between bHLH transcription factors and
   histones for DNA access. _Nature_ 2023. doi:10.1038/s41586-023-06282-3

**c-Myc chemical biology**

5. Yin X, Giap C, Lazo JS, Prochownik EV. Low molecular weight inhibitors of Myc-Max
   interaction and function. _Oncogene_ 2003;22:6151–6159. doi:10.1038/sj.onc.1206641
6. Follis AV, Hammoudeh DI, Wang H, Prochownik EV, Metallo SJ. Structural rationale for the
   coupled binding and unfolding of the c-Myc oncoprotein by small molecules. _Chem Biol_
   2008;15:1149–1155. doi:10.1016/j.chembiol.2008.09.011
7. Hammoudeh DI, Follis AV, Prochownik EV, Metallo SJ. Multiple independent binding sites for
   small-molecule inhibitors on the oncoprotein c-Myc. _J Am Chem Soc_ 2009;131:7390–7401.
   doi:10.1021/ja900616b
8. Michel J, Cuchillo R. The impact of small molecule binding on the energy landscape of the
   intrinsically disordered protein c-Myc. _PLoS One_ 2012;7:e41070.
   doi:10.1371/journal.pone.0041070 (PMC3397933, open access)
9. Hart JR, Garner AL, Yu J, et al. Inhibitor of MYC identified in a Kröhnke pyridine library.
   _PNAS_ 2014;111:12556–12561. doi:10.1073/pnas.1319488111
10. Yu C, Niu X, Jin F, Liu Z, Jin C, Lai L. Structure-based inhibitor design for the
    intrinsically disordered protein c-Myc. _Sci Rep_ 2016;6:22298. doi:10.1038/srep22298
    (PMC4773988, open access)
11. Castell A, Yan Q, Fawkner K, et al. A selective high affinity MYC-binding compound inhibits
    MYC:MAX interaction and MYC-dependent tumor cell proliferation. _Sci Rep_ 2018;8:10064.
    doi:10.1038/s41598-018-28107-4 (PMC6030159, open access)
12. Struntz NB, Chen A, Deutzmann A, et al. Stabilization of the Max homodimer with a small
    molecule attenuates Myc-driven transcription. _Cell Chem Biol_ 2019;26:711–723.e14.
    doi:10.1016/j.chembiol.2019.02.009
13. Han H, Jain AD, Truica MI, et al. Small-molecule MYC inhibitors suppress tumor growth and
    enhance immunotherapy. _Cancer Cell_ 2019;36:483–497.e15. doi:10.1016/j.ccell.2019.10.001
14. Beaulieu ME, Castillo F, Soucek L. Structural and biophysical insights into the function of
    the intrinsically disordered Myc oncoprotein. _Cells_ 2020;9:1038. doi:10.3390/cells9041038
    (PMC7226237, open access) — **the source of the Site I/II/III residue ranges quoted in
    §2.2, read in full text this session**
15. Boike L, Cioffi AG, Majewski FC, et al. Discovery of a functional covalent ligand targeting
    an intrinsically disordered cysteine within MYC. _Cell Chem Biol_ 2021;28:4–13.e17.
    doi:10.1016/j.chembiol.2020.09.001 (PMC7854864, open access)
16. Garralda E, Beaulieu ME, Moreno V, et al. MYC targeting by OMO-103 in solid tumors: a phase
    1 trial. _Nat Med_ 2024;30:762–771. doi:10.1038/s41591-024-02805-1 (PMC10957469, open
    access)
17. Obisesan OA, Ofori S, Orobator ON, Sharma H, Groetecke E, Awuah SG. Discovery of a
    pyrazolopyridinone-based MYC inhibitor that selectively engages intracellular c-MYC and
    disrupts MYC-MAX heterodimerization. _J Med Chem_ 2025;68:6233–6251.
    doi:10.1021/acs.jmedchem.4c02556 (PMC12344569)

**Evaluation methodology**

18. Zhang Z, Li Y, Lin B, Schroeder M, Huang B. Identification of cavities on protein surface
    using multiple computational approaches for drug binding site prediction (MetaPocket 2.0).
    _Bioinformatics_ 2011;27:2083–2088. doi:10.1093/bioinformatics/btr331
19. Gallo Cassarino T, Bordoli L, Schwede T. Assessment of ligand binding site predictions in
    CASP10. _Proteins_ 2014;82(Suppl 2):154–163. doi:10.1002/prot.24495
20. Charifson PS, Corkery JJ, Murcko MA, Walters WP. Consensus scoring: a method for obtaining
    improved hit rates from docking databases of three-dimensional structures into proteins.
    _J Med Chem_ 1999;42:5100–5109. doi:10.1021/jm990352k
21. Gao X, Bu D, Xu J, Li M. Improving consensus contact prediction via server correlation
    reduction. _BMC Struct Biol_ 2009;9:28. doi:10.1186/1472-6807-9-28 (PMC2689239, open access)
22. Won J, Baek M, Monastyrskyy B, Kryshtafovych A, Seok C. Assessment of protein model
    structure accuracy estimation in CASP13: challenges in the era of deep learning. _Proteins_
    2019;87:1351–1360. doi:10.1002/prot.25804
23. Le Guilloux V, Schmidtke P, Tuffery P. Fpocket: an open source platform for ligand pocket
    detection. _BMC Bioinformatics_ 2009;10:168. doi:10.1186/1471-2105-10-168
24. Schmidtke P, Barril X. Understanding and predicting druggability. A high-throughput method
    for detection of drug binding sites. _J Med Chem_ 2010;53:5858–5867. doi:10.1021/jm100574m
25. Halgren TA. Identifying and characterizing binding sites and assessing druggability.
    _J Chem Inf Model_ 2009;49:377–389. doi:10.1021/ci800324m
26. Volkamer A, Kuhn D, Rippmann F, Rarey M. DoGSiteScorer: a web server for automatic binding
    site prediction, analysis and druggability assessment. _Bioinformatics_ 2012;28:2074–2075.
    doi:10.1093/bioinformatics/bts310
27. Kozakov D, Grove LE, Hall DR, et al. The FTMap family of web servers for determining and
    characterizing ligand-binding hot spots of proteins. _Nat Protoc_ 2015;10:733–755.
    doi:10.1038/nprot.2015.043
28. Kozakov D, Hall DR, Napoleon RL, Yueh C, Whitty A, Vajda S. New frontiers in druggability.
    _J Med Chem_ 2015;58:9063–9088. doi:10.1021/acs.jmedchem.5b00586
29. Landon MR, Lancia DR Jr, Yu J, Thiel SC, Vajda S. Identification of hot spots within
    druggable binding regions by computational solvent mapping of proteins. _J Med Chem_
    2007;50:1231–1240. doi:10.1021/jm061134b
30. Trott O, Olson AJ. AutoDock Vina: improving the speed and accuracy of docking with a new
    scoring function, efficient optimization, and multithreading. _J Comput Chem_
    2010;31:455–461. doi:10.1002/jcc.21334
31. Eberhardt J, Santos-Martins D, Tillack AF, Forli S. AutoDock Vina 1.2.0: new docking
    methods, expanded force field, and Python bindings. _J Chem Inf Model_ 2021;61:3891–3898.
    doi:10.1021/acs.jcim.1c00203
32. Warren GL, Andrews CW, Capelli AM, et al. A critical assessment of docking programs and
    scoring functions. _J Med Chem_ 2005;49:5912–5931. doi:10.1021/jm050362n
33. Karelina M, Noh JJ, Dror RO. How accurately can one predict drug binding modes using
    AlphaFold models? _eLife_ 2023;12:RP89386. doi:10.7554/eLife.89386 (PMC10746139, open
    access)
34. Williamson MP. Using chemical shift perturbation to characterise ligand binding. _Prog Nucl
    Magn Reson Spectrosc_ 2013;73:1–16. doi:10.1016/j.pnmrs.2013.02.001
35. Dominguez C, Boelens R, Bonvin AMJJ. HADDOCK: a protein-protein docking approach based on
    biochemical or biophysical information. _J Am Chem Soc_ 2003;125:1731–1737.
    doi:10.1021/ja026939x
36. Faure AJ, Domingo J, Schmiedel JM, et al. Mapping the energetic and allosteric landscapes
    of protein binding domains. _Nature_ 2022;604:175–183. doi:10.1038/s41586-022-04586-4
37. Leander M, Liu Z, Cui Q, Raman S. Deep mutational scanning and machine learning reveal
    structural and molecular rules governing allosteric hotspots in homologous proteins.
    _eLife_ 2022;11:e79932. doi:10.7554/eLife.79932
38. Zhao J, Cao Y, Zhang L. Exploring the computational methods for protein-ligand binding site
    prediction. _Comput Struct Biotechnol J_ 2020;18:417–426. doi:10.1016/j.csbj.2020.02.008
    (PMC7049599, open access)
39. Robustelli P, Ibanez-de-Opakua A, Campbell-Bezat C, et al. Molecular basis of small-molecule
    binding to α-synuclein. _J Am Chem Soc_ 2022;144:2501–2510. doi:10.1021/jacs.1c07591
40. Martínez-Cartró M, et al. Discovering uncharted binding pockets on E3 ligases leads to the
    identification of FBW7 allosteric modulators. _Adv Sci_ 2025. doi:10.1002/advs.202506068
    (PMC12533291, open access) — cited only to record that the one "MYC allosteric" hit in the
    literature search targets the ligase, not MYC
