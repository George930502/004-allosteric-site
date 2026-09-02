# ABL1 apo survey — is there a myristate-free, assembled c-Abl?

**Question.** The myristoyl pocket is allosteric because myristate binding bends helix
alpha-I and creates the C-lobe surface that the SH3–SH2 clamp docks onto. To predict that
pocket from an apo structure we want a chain that (b) contains SH3 **and** SH2 **and** the
kinase domain in the assembled autoinhibited arrangement, and (c) has the myristoyl pocket
empty. This page asks whether any deposited structure satisfies both.

**Answer, up front: no. Not one structure in the PDB satisfies (b) and (c) together.**
Six entries in the entire PDB model more than the ABL kinase domain. Four have the pocket
occupied. The two with an empty pocket are both in the *extended* (active-like) arrangement,
in which the clamp is off the C-lobe — and neither models the SH3 domain.

**Retrieved** 2026-09-02 from live RCSB Search API, RCSB Data API (REST + GraphQL), the
deposited coordinate files, UniProt REST and Europe PMC / PMC. Raw responses are in
`rcsb-abl1/`. Every number below is either quoted from one of those responses or measured
from a downloaded coordinate file by the scripts whose output is saved beside them.

> **Handle this file like an answer key.** Section 2 lists the myristoyl-pocket lining
> residues, which are derived from the holo entry `5MO4`. Nothing on the prediction path
> may read this file. It is not yet named in `tests/test_no_leakage.py` `PROTECTED_PATHS`;
> it should be, on the same argument as
> `docs/benchmark/secondary/evidence/extension-candidates.md`.

---

## 1. Method — what was searched, and how completeness was established

| Step | Query | Result | Raw file |
| --- | --- | --- | --- |
| 1 | Search API, `reference_sequence_identifiers.database_accession = P00519` + `database_name = UniProt`, return `polymer_entity` | 85 entities | `search-P00519-human-ABL1-polymer-entities.json` |
| 2 | Same for `P42684` (human ABL2) | 9 entities | `search-P42684-human-ABL2-polymer-entities.json` |
| 3 | Same for `P00520` (mouse Abl1) | 24 entities | `search-P00520-mouse-Abl1-polymer-entities.json` |
| 4 | Data API GraphQL over all 118 entities: entry method/resolution/citation, entity description, mutation, auth chains, `rcsb_polymer_entity_align.aligned_regions`, source organism, every nonpolymer component and its chains | 118 records | `entities-*.json` |
| 5 | Domain classification from `aligned_regions` against UniProt P00519 domain boundaries | 6 entities model more than the kinase domain | `classified-entities.json` |
| 6 | Sequence-similarity search, ABL1 SH3–SH2 (1a 61–217) and SH3–SH2–kinase (1a 61–512) as query, identity cutoff 0.70 | Two entities not already covered: `4XLI` (mouse Abl2 kinase domain only) and `9F01` (a designed synthetic SH2). Neither adds a candidate | `seqsearch-id70-summary.txt` |
| 7 | Coordinate download + measurement of modelled ranges, numbering, ligand contacts, pocket occupancy, SH2–kinase interface, superposition | see §2–§5 | `measured-structures.txt`, `pocket-and-interface.txt` |
| 8 | Entity sequence vs UniProt, region by region, to derive mutations independently of the depositor's `pdbx_mutation` string | see §6 | `sequence-diffs.txt` |

Step 6 is the completeness argument. A 70%-identity sequence search over the ABL1 SH3–SH2
unit returns 50 entities and over SH3–SH2–kinase returns 116; every one of them is already
in the three UniProt result sets except `4XLI` and `9F01`. There is no ABL structure hiding
behind a missing UniProt cross-reference.

**Domain boundaries** are from UniProt P00519 (`uniprot-P00519.json`, canonical isoform IA,
1130 aa): SH3 61–121, SH2 127–217, protein-kinase 242–493. Those are **1a numbering**.
Almost every ABL structure file uses **1b numbering = 1a + 19**, so in file numbering:
SH3 80–140, SH2 146–236, kinase 261–512.

**Numbering was determined per file, not assumed.** For each chain the script locates the
catalytic-loop motif `HRDLAARN` or the `DFGLSRLM` DFG motif in the modelled sequence and
subtracts its UniProt index. Every ABL1 file measured here returned offset **+19** (1b)
except `9KS5`, which returned **0** (1a). Do not assume 1b. Verified positions in P00519:
`HRDLAARN` at 1a 361–368 (1b 380–387), so the catalytic aspartate is 1a D363 = **1b D382**;
`DFGLSRLM` at 1a 381–388 (1b 400–407); gatekeeper 1a T315 = **1b T334**.

**Modified residues were included** in the per-structure ligand measurement, not only
non-polymer entities. Across the six multi-domain entries the only modified residue found is
`SEP69` in 2FO0 (phosphoserine; measured 27.34 Å from the myristoyl pocket, contacting residues 67, 68, 70–73 and 143–146).
None of the six hides a pocket occupant as a modified residue.

---

## 2. The myristoyl pocket, defined by measurement

Derived, not recalled: the residues of `5MO4` chain A within 4.5 Å of **AY7 (asciminib)**,
measured from the deposited coordinates.

**20 residues, 1b numbering:** 351, 356, 359, 360, 363, 448, 451, 452, 453, 454, 456, 481,
482, 483, 484, 487, 512, 521, 525, 529.

Cross-check on the same definition: **MYR (myristate)** in `1OPL` chain A contacts 16 of
these 20 at 4.5 Å (nearest approach 3.29 Å), and those 16 are a strict subset — Jaccard 0.80.
The four asciminib-only contacts are 351, 453, 456 and the second half of 454. Myristate and
asciminib occupy the same site. (`pocket-and-interface.json`.)

Residues 521, 525 and 529 sit in helix alpha-I (roughly 1b 513–531). That matters below:
alpha-I is the part of the pocket that is remodelled by myristate binding, and it is the
first part to go disordered when myristate is absent.

---

## 3. Census — every ABL entry that models more than the kinase domain

Six. That is the whole population, across human ABL1, mouse Abl1 and human ABL2.

| PDB | Organism / UniProt | Method | Res (Å) | Chains | Modelled range per chain (1b, file numbering) | SH3 / SH2 / kinase residues modelled | Non-polymer components and which pocket | Mutations (derived) | Numbering |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **1OPL** | *H. sapiens*, P00519 | X-ray | 3.42 | A, B | A 81–531 (no gap); B 140–237 + 252–518 | A 60/91/252; **B 1/91/252** | **MYR** chain A only — myristoyl pocket, 3.29 Å; **P16** (PD166326) chains A and B — ATP site, 16.4 Å from the pocket | D382N (HRD catalytic Asp) | 1b |
| **2FO0** | *H. sapiens*, P00519 | X-ray | 2.27 | A | 65–68 + 70–530 | 61/91/252 | **MYR** — myristoyl pocket, 3.31 Å; **P16** — ATP site, 16.35 Å; GOL; SEP69 (phosphoserine) | D382N | 1b |
| **1OPK** | *M. musculus*, P00520 | X-ray | 1.80 | A | 83–531 (no gap) | 58/91/252 | **MYR** — myristoyl pocket, 3.47 Å; **P16** — ATP site, 16.41 Å; GOL | D382N | 1b |
| **4XEY** | *H. sapiens*, P00519 | X-ray | 2.891 | A, B | A 250–269 + 274–522; **B 141–205 + 209–238 + 251–267 + 274–292 + 296–523** | A 0/0/248; **B 0/88/243** | **1N1** (dasatinib) chains A and B — ATP site only. **Myristoyl pocket EMPTY**, nearest het 15.78 Å | **none — wild type** over 1a 119–515 | 1b |
| **5MO4** | *H. sapiens*, P00519 | X-ray | 2.17 | A | 83–295 + 298–401 + 420–531 | 58/91/232 | **AY7** (asciminib) — myristoyl pocket, 2.82 Å; **NIL** (nilotinib) — ATP site, 14.14 Å | T334I (gatekeeper), D382N | 1b |
| **8SSN** | *H. sapiens*, P00519 | X-ray | 2.86 | A, B | A 82–250 + 260–270 + 274–409 + 421–460 + 462–474 + 476–526; B nine segments, 82–525 | A 59/91/236; B 59/91/201 | **AY7** (asciminib) — myristoyl pocket, 2.98 Å (A) / 3.14 Å (B); **SKI** — ATP site, ~16 Å; CL, DMS, SO4 | **none — wild type** over 1a 64–510 | 1b |

Refinement statistics for the same six (`refine-stats.txt`, from `data.rcsb.org` `refine`):

| PDB | Space group | R<sub>work</sub> / R<sub>free</sub> | Mean B (Å²) | Released | Primary citation |
| --- | --- | --- | --- | --- | --- |
| 1OPL | C 2 2 2₁ | 0.306 / 0.315 | 123.3 | 2003-04-08 | Nagar et al., *Cell* 112:859–871, DOI `10.1016/S0092-8674(03)00194-6` |
| 2FO0 | P 2₁ 2₁ 2 | 0.210 / 0.246 | 38.8 | 2006-03-21 | Nagar et al., *Mol. Cell* 21:787–798, DOI `10.1016/j.molcel.2006.01.035` |
| 1OPK | C 2 2 2₁ | 0.196 / 0.221 | 30.9 | 2003-04-08 | Nagar et al., *Cell* 2003, same DOI |
| 4XEY | P 2₁ 2₁ 2 | 0.2308 / 0.2593 | 51.1 (paper Table 1) | 2015-04-01 | Lorenz, Deng, Hantschel, Superti-Furga, Kuriyan, *Biochem. J.* 468:283–291, DOI `10.1042/BJ20141492`, PMID 25779001 |
| 5MO4 | C 2 2 2₁ | 0.1818 / 0.2170 | 36.73 | 2017-04-05 | Wylie et al., *Nature* 543:733–737, DOI `10.1038/nature21702` |
| 8SSN | P 2₁ 2₁ 2₁ | 0.2977 / 0.3480 | [NOT RETRIEVED] (`B_iso_mean` absent) | 2023-09-06 | *PNAS* 120, DOI `10.1073/pnas.2304611120` |

### Entries that model SH3 and/or SH2 but no kinase domain (not candidates, listed for completeness)

| PDB | Content | Method | Res (Å) | Range | Note |
| --- | --- | --- | --- | --- | --- |
| 2ABL | ABL1 SH3–SH2 fragment | X-ray | 2.5 | 75–237 (file), 1a 57–218 | Insertion INS(M76). No kinase domain, so no pocket |
| 6AMV | Abl 1b "regulatory module", inhibiting state | Solution NMR | — | file 1–255, 1a 6–236 | No kinase domain |
| 6AMW | Abl 1b "regulatory module", activating state | Solution NMR | — | file 1–255, 1a 6–236 | No kinase domain |
| 1AB2, 3K2M, 3T04, 3UYO, 5DC0, 5DC4, 5DC9 | isolated SH2 (mostly monobody complexes) | — | — | 1a ~112–232 | |
| 1ABO, 1ABQ, 1AWO, 1BBZ, 2O88, 3EG0–3EGU, 4J9B–4J9I, 4JJB–4JJD, 5NP2, 5OAZ, 7PVQ–7PW2 | isolated SH3 | — | — | 1a ~60–121 | |

### Every ABL entry carrying a myristate or a known myristoyl-pocket ligand

Scan over all 118 entities (`ligand-scan.txt`):

| PDB | Pocket ligand | All ligands |
| --- | --- | --- |
| 1OPJ | MYR | CL, MYR, STI |
| 1OPK | MYR | GOL, MYR, P16 |
| 1OPL | MYR (chain A only) | MYR, P16 |
| 2FO0 | MYR | GOL, MYR, P16 |
| 3K5V | STJ (GNF-2) | CL, STI, STJ |
| 5MO4 | AY7 (asciminib) | AY7, NIL |
| 8SSN | AY7 (asciminib) | AY7, CL, DMS, SKI, SO4 |

Twenty-one entries carry no non-polymer component at all: 1AB2, 1ABQ, 1AWO, 1JU5, 1ZZP,
2ABL, 2ECD, 2KK1, 3ULR, 5DC0, 5NP2, 5NP3, 6AMV, 6AMW, **6XR6, 6XR7, 6XRG**, 7PVQ, 7PVR,
7PW2, **9KS5**. Four of these contain a kinase domain: the three NMR entries 6XR6/6XR7/6XRG,
and 9KS5.

**A non-polymer scan is not a ligand scan.** `9KS5` is titled "in complex with K-CNBA-1" and
its `nonpolymer_entity_count` is 0, because its covalent inhibitor is deposited as the
**modified residue `A1EG1`**, linked into the polymer, not as a separate entity. It also
carries `PTR393`, phosphotyrosine at the activation-loop tyrosine. Both are invisible to a
`nonpolymer_entities` query. Measured directly from the coordinates, neither is in the
myristoyl pocket: nearest approach 15.87 Å (A1EG1) and 21.36 Å (PTR). A ligand census that
only reads non-polymer entities will call such an entry apo when it is not.

---

## 4. The named entries — one row each

Full detail in `named-entries-summary.txt`. Ranges are UniProt-1a alignment ranges reported
by RCSB; file numbering is 1b for every ABL1 file measured.

| PDB | What it is | Method / Res | Chains | 1a align range | Domains | Ligands | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **1OPL** | Human c-Abl 1b SH3-SH2-kinase, autoinhibited | X-ray 3.42 | A, B | 6–512 | SH3+SH2+KD | MYR (A), P16 (A,B) | Chain A: pocket occupied. Chain B: pocket empty but extended/active, no SH3. See §5 |
| **2FO0** | Same construct, better crystal | X-ray 2.27 | A | 38–512 | SH3+SH2+KD | MYR, P16, GOL | Pocket occupied by MYR. Fails (c) |
| **1IEP** | Mouse Abl kinase domain + imatinib | X-ray 2.10 | A, B | P00520 229–515 | KD only | CL, STI | Fails (b) |
| **2G2H** | Human ABL1 KD, Src-like inactive | X-ray 2.00 | A, B | 229–512 | KD only | P16 (ATP site, 16.27 Å from pocket) | Fails (b). Pocket empty but 2/20 lining residues (525, 529) unmodelled. H396P (1a) = H415P (1b) |
| **2G2I** | Same, + ADP | X-ray 3.12 | A, B | 229–512 | KD only | ADP | Fails (b) |
| **2G1T** | Human ABL1 KD | X-ray 1.80 | A–D | 229–512 | KD only | MG, 112 (ATP-γ-S analogue) | Fails (b) |
| **2HYY** | Human ABL1 KD + imatinib | X-ray 2.40 | A–D | 228–500 | KD only | STI | Fails (b) |
| **3K5V** | Mouse Abl KD + imatinib + **GNF-2** | X-ray 1.74 | A, B | P00520 229–515 | KD only | STI, **STJ = GNF-2** | Fails (b) and (c) — allosteric ligand in the pocket |
| **3K2M** | ABL1 SH2 + monobody HA4 | X-ray 1.75 | A, B | 121–232 | SH2 only | PO4 | Fails (b) — no kinase domain |
| **6XR6** | Abl 1b KD, active state | Solution NMR | A | 229–515 | KD only | **none** | Fails (b). Both pockets empty, all 20 lining residues modelled |
| **6XR7** | Abl 1b KD, inactive1 | Solution NMR | A | 229–515 | KD only | **none** | Fails (b). Both pockets empty, 20/20 lining modelled, range 248–534 |
| **6XRG** | Abl 1b KD, inactive2 | Solution NMR | A | 229–515 | KD only | none | Fails (b). Mutations G269E, M309L, T408Y |
| **6NPE** | ABL1 KD + imatinib + activator cmpd6 | X-ray 2.15 | A, B | 229–512 | KD only | SO4, STI, KWD, 2PE | Fails (b) |
| **6NPU** | as above, cmpd29 | X-ray 2.33 | A, B | 229–512 | KD only | STI, KWV, SO4, GOL, 2PE | Fails (b) |
| **6NPV** | as above, cmpd51 | X-ray 1.86 | A, B | 229–512 | KD only | SO4, STI, KWP, GOL, 2PE | Fails (b) |
| **5MO4** | ABL1 SH3-SH2-KD + asciminib + nilotinib | X-ray 2.17 | A | 27–515 | SH3+SH2+KD | AY7, NIL | This is the repository's **holo**. Fails (c) by construction |
| **5HU9** | ABL1 KD + CHMFL-074 | X-ray 1.529 | A | 229–500 | KD only | 66K, EDO, CL | Fails (b) |
| **7DT2** | ABL1 KD + covalent inhibitor | X-ray 2.30 | A, B | 229–510 | KD only | HJ9 | Fails (b) |
| **8SSP** | **Not ABL1.** Aurora kinase A (UniProt O14965 122–403) + danusertib + monobody Mb1 | X-ray 2.60 | A, B | — | — | 627, EDO, MES, PDO, PO4, SO4 | Not applicable. The intended ID is almost certainly **8SSN** |
| **8SSN** | Abl kinase + SKI + asciminib | X-ray 2.86 | A, B | 64–510 | SH3+SH2+KD | AY7, SKI, CL, DMS, SO4 | Wild type, assembled — but asciminib fills the pocket. Fails (c) |
| **4XEY** | c-Abl SH2-kinase construct + dasatinib | X-ray 2.891 | A, B | 119–515 | SH2+KD, **no SH3** | 1N1 (ATP site) | **Pocket empty.** Fails (b) — no SH3, and SH2 is on the N-lobe. See §5 |
| **1OPK** | Mouse c-Abl SH3-SH2-KD, autoinhibited | X-ray 1.80 | A | P00520 27–515 | SH3+SH2+KD | MYR, P16, GOL | The best-resolved assembled c-Abl in the PDB — but MYR fills the pocket. Fails (c) |
| **1OPJ** | Mouse Abl KD + imatinib + MYR | X-ray 1.75 | A, B | P00520 229–515 | KD only | CL, MYR, STI | Fails (b) and (c) |

---

## 5. Verdict on 1OPL chain B

### What the file itself says

Deposited `REMARK 3` (also in `data.rcsb.org` `refine[0].details`, `entry-1OPL.json`) —
verbatim:

> "THE STRUCTURE WAS REFINED BY SUPERIMPOSING THE REFINED HIGH RESOLUTION STRUCTURE OF C-ABL
> (PDB ENTRY 1OPK) ON THE MOLECULAR REPLACEMENT SOLUTION AND OPTIMIZING POSITIONS OF
> INDIVIDUAL DOMAINS BY RIGID-BODY REFINEMENT. FOLLOWING THIS, ONLY OVERALL DOMAIN B-FACTORS
> WERE APPLIED TO MOLECULE B, WHEREAS INDIVIDUAL B-FACTORS WERE REFINED FOR MOLECULE A."

So molecule B is a rigid-body domain placement carrying one B-factor per domain. Measured
from the coordinates (`pocket-and-interface.txt`):

| | chain A | chain B |
| --- | --- | --- |
| Residues modelled | 451 (81–531, no gap) | 365 (140–237, 252–518) |
| Unmodelled (REMARK 465) | 1–80, 532–537 | **1–139**, 238–251, **519–537** |
| SH3 residues modelled (1b 80–140) | 60 | **1** |
| SH2 residues modelled (1b 146–236) | 91 | 91 |
| Kinase residues modelled (1b 261–512) | 252 | 252 |
| helix alpha-I 513–531 modelled | 19 | **6** (513–518 only) |
| Mean B, whole chain | 85.0 | **170.7** |
| Mean B, SH2 | 72.0 | **198.1** (one flat value) |
| Mean B, kinase | 88.1 | 160.9 |
| Myristoyl-pocket lining residues modelled (of 20) | 20 | **17** — 521, 525, 529 missing |
| Nearest non-solvent het to the pocket | MYR 3.29 Å | P16 16.00 Å — **pocket empty** |
| SH2 → kinase contacts ≤4.5 Å (kinase side) | 357, 358, 360, 361, 393, 394, 512 | 261, 262, 263, 291, 294, 328, 329, 331 |
| Of those, myristoyl-pocket lining | **360, 512** | **none** |

Biological assembly (`assembly-1OPL-*.json`, `REMARK 350`): assembly 1 is
`AUTHOR DETERMINED BIOLOGICAL UNIT: MONOMERIC` on chain A; assembly 2 is monomeric on chain
B; assembly 3 is a PISA-generated dimer. The authors declare a monomer. The two chains are
two copies, not a biological dimer.

`REMARK 999` of 1OPL, verbatim:

> "The bound myristoyl group is from the naturally occurring N-terminal myristoyl
> modification that is connected to the SH3 domain of the protein chain A by 79 residues
> that could not be modeled."

That is, the myristate in chain A is the protein's own N-terminal modification bound back
into its own pocket — the *cis*, autoinhibited assembly.

### What the literature says

The primary citation, Nagar et al., *Cell* 112:859–871 (2003), DOI
`10.1016/S0092-8674(03)00194-6`, PMID 12654251, **is paywalled to this session**. Unpaywall
and OpenAlex both report it as bronze open access at
`http://www.cell.com/article/S0092867403001946/pdf`, but cell.com and sciencedirect.com both
return HTTP 403 to every fetch attempted here, and the paper has no PMC record. **The
verbatim text of Nagar et al. 2003 is [NOT RETRIEVED].** Only the abstract was obtained, via
Europe PMC (`epmc-nagar2003.json`); it does not mention the two molecules.

The deciding quote instead comes from **Lorenz, Deng, Hantschel, Superti-Furga & Kuriyan,
*Biochem. J.* 468:283–291 (2015)**, DOI `10.1042/BJ20141492`, PMID 25779001, PMC5936049 —
the 4XEY paper, written by three of the nine authors of Nagar 2003 including the same senior
author. Retrieved in full from PMC and saved verbatim as
`rcsb-abl1/lit-lorenz2015-BJ20141492-PMC5936049.txt`.

On what the two molecules of 1OPL are:

> "The structure shows the SH2 and kinase domain in an extended conformation (Figure 4A), as
> was observed previously for the SH3-SH2-kinase domain construct bound to PD166326
> (PDB ID: 1OPL) [2]. **The previous crystal form, however, contained two different
> conformational states of the SH3-SH2-KD construct, (i) the compact autoinhibited
> conformation, in which the SH2 domain docks onto the C-lobe of the kinase domain and
> (ii) the extended conformation, for which only the SH2 and kinase domains could be modeled
> and which was characterized by very high temperature factors.**"

On how it was regarded at the time and how it was later validated:

> "In the case of Abl, the helix alphaC patch can interact with the flanking SH2 domain to
> give rise to an extended conformation, as opposed to the assembled, autoinhibited state in
> which the SH2 domain docks onto the backside of the C-lobe (Figure 1A). The extended
> conformation was originally observed in a crystal structure of a c-Abl three-domain
> construct containing the SH3, SH2 and kinase domains in complex with myristic acid and a
> small-molecule inhibitor, PD166326 [2]. **In this crystal the extended, myristoyl-free
> conformation occurred fortuitously alongside the assembled, myristoyl-bound state, and its
> significance initially remained unclear.** Small-angle X-ray scattering studies later
> revealed that an activated three-domain Abl construct, in which autoinhibitory constraints
> have been released through mutations in regulatory interfaces, has indeed an extended shape
> in solution that is in good agreement with the extended conformation found in the crystal
> [9]."

> "Contacts in the SH2-N-lobe interface of the extended conformation have been shown to be
> important for kinase activation [10] and for the deleterious effects of the overactive
> forms of Abl, such as Bcr-Abl, in vivo [11, 12]. Remarkably, perturbation of the interface
> by a single point mutation (I164E) inhibits downstream signaling events that are important
> for CML maintenance, in particular STAT5 phoshorylation, and abolishes leukemogenesis in a
> CML mouse model [11]."

Reference [9] is Nagar et al., *Mol. Cell* 21:787–798 (2006), DOI
`10.1016/j.molcel.2006.01.035`, PMID 16543148 — not in PMC, **full text [NOT RETRIEVED]**.
Reference [11] is Grebien/Filippakopoulos-line work; [10] is Filippakopoulos et al.,
*Cell* 134:793–803 (2008), DOI `10.1016/j.cell.2008.07.047`, PMC2572732.

I164 and T231 are 1b numbering. Verified from the coordinates: residue 164 is ILE and
residue 231 is THR in 1OPL chain A, 1OPL chain B and 4XEY chain B.

### Independent structural confirmation

`4XEY` chain B reproduces the 1OPL chain B arrangement in a different crystal form, from a
different construct, eleven years later, at better resolution and with individual B-factors.
Measured here (`pocket-and-interface.txt`), superposing on kinase residues 273–512 and then
measuring the SH2 (146–236) deviation:

| Pair | Kinase-fit RMSD | SH2 deviation after that fit (RMSD / max) | Global all-common-CA RMSD |
| --- | --- | --- | --- |
| 1OPL:A vs 1OPL:B | 0.53 Å / 240 CA | **70.06 / 101.31 Å** over 91 CA | 23.12 Å / 365 CA |
| 1OPL:A vs 5MO4:A (holo) | 0.92 Å / 220 CA | 1.49 / 2.46 Å over 91 CA | 0.98 Å / 429 CA |
| 1OPL:B vs 5MO4:A | 1.03 Å / 220 CA | 69.38 / 100.88 Å over 91 CA | 22.89 Å / 345 CA |
| **1OPL:B vs 4XEY:B** | **1.21 Å / 236 CA** | **2.28 / 8.07 Å** over 88 CA | **1.44 Å / 352 CA** |
| 1OPL:A vs 4XEY:B | 1.34 Å / 236 CA | 69.17 / 100.78 Å over 88 CA | 23.22 Å / 359 CA |

The SH2–kinase interfaces agree residue by residue. 1OPL:B contacts kinase 261, 262, 263,
291, 294, 328, 329, 331; 4XEY:B contacts 261, 262, 263, 276, 291, 292, 328, 329, 331 —
seven residues in common, all on the N-lobe, none of them in the myristoyl pocket. For
comparison, 1OPL:A, 2FO0:A, 1OPK:A, 5MO4:A all give the identical C-lobe interface
357, 358, 360, 361, 393, 394, 512, and **360 and 512 are themselves myristoyl-pocket lining
residues**.

The kinase domains of 1OPL chain A and chain B are the same conformation (0.53 Å over 240
CA), and both bind PD166326, which selects the Src-like inactive state. What differs between
the chains is only the position of the regulatory module.

### Verdict

**1OPL chain B is a described, biologically meaningful arrangement — but it is the extended,
active-like state, not an apo version of the autoinhibited state.** All three of the
candidate readings in the question are partly right, in this order of importance:

1. **It is a real, named conformational state.** Lorenz et al. call it "the extended
   conformation"; it was validated by SAXS in solution (Nagar 2006), and mutating its
   interface (I164E) abolishes leukemogenesis in a mouse model. It is not a packing accident,
   and 4XEY reproduces it independently to 1.44 Å global RMSD.
2. **It is nevertheless the low-quality copy of a 3.42 Å crystal.** Rigid-body placement, one
   B-factor per domain, chain mean B 170.7 Å² against 85.0 for chain A, "characterized by
   very high temperature factors" in the authors' own later words. 172 of 537 residues are
   unmodelled.
3. **It is partially disordered in exactly the place that matters.** The whole SH3 domain is
   gone (1–139 unmodelled). Helix alpha-I is truncated at 518, so 3 of the 20 myristoyl-pocket
   lining residues — 521, 525, 529 — are not in the file at all.

**Consequence for the challenge.** The myristoyl pocket is allosteric *because* filling it
bends alpha-I and builds the C-lobe surface that the clamp docks onto. In chain B the clamp is
not on the C-lobe, the SH3 domain does not exist in the model, and alpha-I is disordered from 519.
Predicting the myristoyl pocket from chain B means predicting it in the one state where its
allosteric mechanism is switched off, using a model that omits the helix the mechanism acts
through. Chain B is myristate-free in the trivial sense that nothing is bound there — but it
is not the assembled apo state; it is the disassembled active state.

---

## 6. Construct facts derived independently of the depositor

`sequence-diffs.txt` compares each entity's `pdbx_seq_one_letter_code_can` to UniProt P00519
region by region, using RCSB's own alignment. This is stricter than trusting the depositor's
`pdbx_mutation` string, whose numbering is not consistent between entries.

| Entity | RCSB `pdbx_mutation` (verbatim) | Differences from UniProt inside the aligned region | Note |
| --- | --- | --- | --- |
| 1OPL_1 | `D382N, K29R, E29D` | 1a 363 D→N only, in the 13–512 block; a further 12 differences at 1a 6–26 | **1a 363 = 1b 382 = the HRD catalytic aspartate.** The 1a 6–26 differences are all in 1b 25–45, which is unmodelled in both chains — they never appear in the coordinates. The repository manifest's "K29R, E30D" belong to that unmodelled stretch |
| 2FO0_1 | `D382N` | 1a 363 D→N | Same catalytic-dead mutation |
| 1OPK_1 | `D382N` | (mouse P00520) | Same |
| **4XEY_1** | `None` | **none over 1a 119–515** | **Wild type** |
| 5MO4_1 | `T334I D382N` | 1a 315 T→I, 1a 363 D→N | Gatekeeper T315I (1a) = T334I (1b), plus catalytic-dead |
| **8SSN_1** | `None` | **none over 1a 64–510** | **Wild type** |
| 2G2H_1 | `H396P` | 1a 396 H→P | Here the depositor's number is **1a**; in the file it is residue 415. RCSB's `pdbx_mutation` uses 1b for 1OPL/2FO0/5MO4 and 1a for 2G2H. Do not read that field without checking |
| 6XR7_1 | `None` | none over 1a 229–515 | Wild type |

`4XEY` and `8SSN` are the only wild-type structures in the PDB that model more than the ABL1
kinase domain.

---

## 7. Ranking as an apo input for predicting the myristoyl pocket

Criteria from the question: (b) SH3 **and** SH2 **and** kinase in the assembled autoinhibited
arrangement; (c) myristoyl pocket empty.

**No structure satisfies (b) and (c). That is the finding, not a failure to search.**

| Rank | Candidate | (b) assembled SH3+SH2+KD? | (c) pocket empty? | What it costs |
| --- | --- | --- | --- | --- |
| 1 | **1OPL chain B** | **No.** SH2 present but docked on the N-lobe (extended/active); SH3 modelled at 1 of 61 residues | **Yes** — nearest het 16.00 Å | Wrong conformational state for the mechanism being predicted. 3.42 Å, rigid-body refinement, chain mean B 170.7 Å², 172 residues unmodelled. Helix alpha-I truncated at 518, so 3 of 20 pocket-lining residues absent. Carries D382N. Endorsed by the organisers' reply, and it is the only myristate-free chain that carries any regulatory domain |
| 2 | **4XEY chain B** | **No.** SH2 on the N-lobe, same as 1OPL:B; **no SH3 in the construct at all** (c-Abl 1b 138–534) | **Yes** — nearest het 15.78 Å | Same wrong state as 1OPL:B, and by construction rather than by disorder. But better in every crystallographic respect: 2.891 Å, R<sub>free</sub> 0.259, mean protein B 51.1 Å², **wild-type sequence**, 359 modelled residues, 18 of 20 pocket residues present (525, 529 absent). If the SH2-on-N-lobe state is going to be used at all, this is the better representative of it |
| 3 | **6XR7 (or 6XR6 / 6XRG)** | **No** — kinase domain only, 248–534 | **Yes** — no ligand anywhere in the entry | Solution NMR, so no resolution figure and an ensemble rather than one model. But it is the **only ABL1 entry with 20 of 20 pocket-lining residues modelled and nothing bound in either pocket**, wild type, in a conformation the authors assign (`inactive1`). All regulatory domains absent |
| 4 | **2G2H chain A** | **No** — kinase domain only, 252–523 | **Yes** — P16 is in the ATP site, 16.27 Å from the pocket | The repository's current `bcr_abl1_corrected` apo. X-ray 2.00 Å, R<sub>free</sub> 0.213, mean B 18.2 Å², same 1b numbering as the holo. Costs: 2 of 20 pocket residues unmodelled (525, 529); carries the engineered activating H415P (1b) |
| 5 | **9KS5 chain A** | **No** — kinase domain only, 1a 233–500 = 1b 252–519 | **Yes** — nearest modelled ligand atom 17.03 Å | X-ray 2.20 Å, R<sub>free</sub> 0.212, mean B 39.1 Å², **wild type**. Two traps: it is the only ABL1 file measured here that uses **1a numbering** (offset 0, not +19), and its inhibitor is a modified residue (`A1EG1`), so a non-polymer ligand scan reports it as apo. It is also the **phosphorylated, active** kinase domain (`PTR393`), and it stops at 1a 500, so 3 of 20 pocket residues (1b 521, 525, 529) are unmodelled |
| — | 1OPL chain A | **Yes** — the reference assembled state | **No** — MYR at 3.29 Å, contacting 16 of the 20 lining residues | Holo at the site it is asked to predict. Disqualified by (c) |
| — | 2FO0 chain A | **Yes**, and better than 1OPL:A (2.27 Å, mean B 38.8, 465 residues, 61/61 SH3) | **No** — MYR at 3.31 Å | If the pocket did not have to be empty, this is the best assembled human c-Abl in the PDB. Disqualified by (c) |
| — | 1OPK chain A | **Yes** — best-resolved assembled c-Abl anywhere, 1.80 Å, mean B 30.9 | **No** — MYR at 3.47 Å | Mouse. Disqualified by (c) |
| — | 8SSN | **Yes**, wild type | **No** — asciminib at 2.98 Å | Disqualified by (c) |
| — | 5MO4 | **Yes** | **No** — asciminib at 2.82 Å | This is the holo |
| — | 3K5V | No — kinase domain only | **No** — GNF-2 in the pocket | Disqualified twice |

### Each candidate against the frozen holo, measured

All-common-CA superposition onto `5MO4` chain A, and the same pair fitted on kinase 273–512
with the SH2 deviation then measured (`pocket-and-interface.txt`, appended block):

| Apo candidate | Global RMSD vs 5MO4:A | Kinase-fit RMSD | SH2 deviation after the kinase fit | State-matched to the holo? |
| --- | --- | --- | --- | --- |
| 1OPL:A | **0.98 Å / 429 CA** | 0.92 Å / 220 CA | 1.49 Å (max 2.46) / 91 CA | **Yes** — but MYR fills the pocket |
| 2G2H:A | **1.78 Å / 252 CA** | 1.18 Å / 220 CA | no SH2 modelled | Yes, on the kinase domain |
| 6XR7:A (model 1) | 3.92 Å / 264 CA | 2.14 Å / 220 CA | no SH2 modelled | Approximately, on the kinase domain |
| 1OPL:B | **22.89 Å / 345 CA** | 1.03 Å / 220 CA | 69.38 Å (max 100.88) / 91 CA | **No** |
| 4XEY:B | **23.03 Å / 339 CA** | 1.18 Å / 216 CA | 68.46 Å (max 100.41) / 88 CA | **No** |

The kinase domain is the same in all five, to 1–2 Å. The 23 Å is entirely the regulatory
module. Any apo/holo pair built on chain B is matched at the catalytic domain and unmatched
at the domain arrangement that the myristoyl pocket controls.

### Reading of the ranking

The population splits cleanly and there is no middle:

* Every structure in which the SH3–SH2 clamp is **docked on the C-lobe** has something in the
  myristoyl pocket — MYR in 1OPL:A, 2FO0, 1OPK; asciminib in 5MO4, 8SSN. Five for five.
* Every structure with an **empty myristoyl pocket** that carries any regulatory domain has
  the SH2 on the **N-lobe** instead — 1OPL:B and 4XEY:B. Two for two.

That is not a gap in the PDB; it is the mechanism showing up in the deposited record. The
clamp only docks when the pocket is filled. A myristate-free assembled c-Abl is the state
that the myristoyl switch exists to prevent, so a crystal of it would be a surprise.

Consequences worth stating plainly:

1. **The best (b)-satisfying candidate and the best (c)-satisfying candidate are different
   structures, and no experiment will merge them.** Any choice concedes one criterion.
2. If the organisers' instruction to use chain B is followed, **4XEY chain B is the better
   structure for the same conformational state** — wild type, 2.891 Å against 3.42 Å,
   individual B-factors against per-domain, 18 of 20 pocket residues against 17. Its cost is
   that it drops SH3 by construction rather than by disorder, which is arguably more honest.
   Its blocker for this repository is that its holo pair `5MO4` is in the *other*
   conformation. Measured, all-common-CA superposition: 4XEY:B vs 5MO4:A is **23.03 Å over
   339 CA**, and 1OPL:B vs 5MO4:A is **22.89 Å over 345 CA**. Apo and holo would not be
   state-matched.
3. If state-matching to the holo is what matters, **only chain A of 1OPL/2FO0/1OPK matches
   5MO4** (0.98 Å global for 1OPL:A) — and all three have myristate in the pocket.
4. **2G2H remains defensible** as the corrected apo. It gives up all regulatory domains,
   which the extended-state candidates give up too, and in exchange it is a 2.00 Å structure
   with an empty pocket, the holo's numbering, and no conformational-state mismatch on the
   kinase domain (1OPL:A vs 2G2H:A, kinase-fit 0.78 Å over 240 CA).

---

## 8. Homologues — mouse Abl1 and human ABL2

Identities are BLAST identities returned by the RCSB sequence-similarity service against the
human ABL1 query, saved in `seqsearch-id70-summary.txt`. Threshold in the question: ≥90%.

| Source | Entries with SH3+SH2+kinase | Identity to human ABL1 | ≥90%? | Myristoyl pocket |
| --- | --- | --- | --- | --- |
| **Mouse Abl1 (P00520)** | **1OPK** only (1.80 Å, chain A, 83–531, SH3 58 / SH2 91 / kinase 252) | **0.993 over a 452-residue alignment** to human 1a 61–512; mouse kinase-domain entries score 0.989–0.996 | **Yes** | **Occupied** — MYR at 3.47 Å, contacting 17 residues including 512, 521, 525, 529 |
| Mouse Abl1, other entries | none — 1OPJ, 1IEP, 1M52, 2HZN, 2QOH, 3K5V, 3KF4, 3KFA, 3MS9, 3MSS, 3DK3/6/7, 3IK3, 3OXZ, 3OY3, 2Z60, 6HD4, 6HD6, 1FPU are all kinase-domain only (P00520 229–515) | 0.989–0.996 | Yes | 1OPJ has MYR; 3K5V has GNF-2; the rest are empty at the pocket but have no regulatory domains |
| **Human ABL2 / Arg (P42684)** | **none.** 2XYN, 3GVU, 3HMI are all kinase-domain only, P42684 279–546 | **0.847 over 301 residues** for the kinase domain; isolated ABL2 SH2 (2ECD) 0.890–0.896; isolated ABL2 SH3 (5NP3, 5NP5) 0.912 | **No** for the kinase domain and the SH2; marginal for the isolated SH3 | Not applicable — no assembled ABL2 structure exists |
| Mouse Abl2 (Q4JIM5) | none — 4XLI is kinase domain only, 279–546 | 0.925 over 268 residues | Yes, but no regulatory domains | Not applicable |

**So the homologues do not supply the missing state.** Mouse Abl1 clears 90% comfortably
(99.3% over the whole SH3-SH2-kinase span) and has exactly one assembled structure, 1OPK —
and 1OPK has myristate in the pocket, which is the same blocker as the human entries. ABL2
has no assembled structure at all, and at 84.7% over the kinase domain it would fail a 90%
identity requirement even if one existed.

---

## 9. What could not be retrieved

| Item | Status | Why |
| --- | --- | --- |
| Nagar et al., *Cell* 2003, full text — the authors' own words about the two molecules in the 1OPL asymmetric unit | **[NOT RETRIEVED]** | Listed as bronze OA by Unpaywall and OpenAlex at `cell.com`, but cell.com and sciencedirect.com return HTTP 403; no PMC record (`elink` returns no `pubmed_pmc` link for PMID 12654251); the EPFL repository copy returns HTTP 405. Only the abstract was obtained. The deposited `REMARK 3` / `REMARK 999` and the Lorenz 2015 quotes in §5 stand in its place |
| Nagar et al., *Mol. Cell* 2006 (the SAXS validation of the extended state, and 2FO0's primary citation), full text | **[NOT RETRIEVED]** | No PMC record for PMID 16543148. Cited here only through Lorenz et al. 2015 reference [9] |
| `8SSN` mean B-factor | **[NOT RETRIEVED]** | `refine[0].B_iso_mean` is absent from the RCSB entry record |
| `4XEY` mean B-factor from RCSB | **[NOT RETRIEVED]** from the API; the value 51.1 Å² in §3 is quoted from Table 1 of the paper, and 51.9 Å² for chain B was measured from the coordinates |
| Whether the myristoyl pocket cavity is *open* (alpha-I bent, alpha-I' formed) or *collapsed* in 1OPL:B, 4XEY:B, 2G2H and 6XR7 | **Not measured** | Requires cavity detection, which is out of scope here. What was measured is which lining residues are modelled and how far the nearest ligand is. In 1OPL:B and 4XEY:B the alpha-I residues that would answer this (521/525/529) are the ones that are missing |

---

## 10. Files

Everything under `rcsb-abl1/`:

* `search-*-polymer-entities.json` — the three UniProt searches (steps 1–3)
* `entities-*.json` — full GraphQL records for all 118 entities plus the extra hits
* `classified-entities.json` — per-entity domain coverage
* `seqsearch-*.json`, `seqsearch-id70-summary.txt` — completeness searches
* `uniprot-P00519.json`, `uniprot-P42684.json`, `uniprot-P00520.json` — domain boundaries and sequences
* `entry-*.json`, `assembly-1OPL-*.json`, `refine-stats.txt` — entry-level records
* `measured-structures.json`, `measured-structures.txt` — modelled ranges, numbering, all ligand contacts
* `pocket-and-interface.json`, `pocket-and-interface.txt` — pocket definition, occupancy, SH2–kinase interfaces, superpositions
* `ligand-scan.txt` — myristate / allosteric-ligand census over all entries
* `sequence-diffs.txt` — mutations derived from sequence, not from the depositor's string
* `named-entries-summary.txt` — per-entry detail for every PDB ID named in the request
* `lit-lorenz2015-BJ20141492-PMC5936049.txt` — the verbatim article text quoted in §5
* `epmc-nagar2003.json` — the Europe PMC record showing Nagar 2003 has no PMC full text
