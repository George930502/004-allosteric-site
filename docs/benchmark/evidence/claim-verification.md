# Independent verification of benchmark claims — literature and database records

**Scope.** Seven claims (C1–C7) about the apo/holo pairs assigned in `CHALLENGE.md` §6 Table 1,
verified against published literature and public database records only. **No fact in this
document was derived from a PDB coordinate file**; a parallel effort covers the file-level
evidence. Where a claim can only be settled from coordinates, that is stated.

**Date of verification:** 2026-08-20. **Challenge document date:** 2026-04-17.

**Credibility key.** `PRIMARY` = peer-reviewed primary research article. `RECORD` = wwPDB /
UniProt / EMDB database record (authoritative for provenance metadata, author-deposited for
scientific content). `PREPRINT` = bioRxiv. `SECONDARY` = review, database aggregation, or
summary — evidence about what the field believes, not about what is true.

---

## Summary

| Claim                                                                     | Verdict                                                                                                                                | Confidence                 | Key deciding source                                                                                                              |
| ------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- | -------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| **C1** `6C1H` is not cardiac myosin / mavacamten                          | **CONFIRMED**                                                                                                                          | High                       | Mentes et al., _PNAS_ 2018, doi:10.1073/pnas.1718316115 (PMID 29358376) + RCSB record for `6C1H`                                 |
| **C2** Mavacamten = `XB2`; first co-structures 2023+                      | **CONFIRMED** (entry list needs correction)                                                                                            | High                       | RCSB chem-comp `XB2` (created 2023‑10‑26, released 2023‑12‑13); Auguin et al., _Nat Commun_ 2024, doi:10.1038/s41467-024-47587-9 |
| **C3** `5TBY` is a homology model, not experimental                       | **CONFIRMED** (one numeric correction: map is 28 Å, not ~20 Å)                                                                         | High                       | Alamo et al., _eLife_ 2017;6:e24634, doi:10.7554/eLife.24634; EMDB `EMD-2240` record                                             |
| **C4** Literature location of the mavacamten site                         | **PARTIALLY CONFIRMED** — 9/12 of our residues named; two literature residues missing from ours                                        | Medium                     | McMillan et al. (bioRxiv 2025.02.12.637875 → _Sci Adv_ 2026, doi:10.1126/sciadv.aea9335); Auguin et al. 2024                     |
| **C5** Innocent explanation for the pairing                               | **PARTIALLY CONFIRMED** — found for `5TBY`, **not found for `6C1H`**; cause of `6C1H` **UNVERIFIABLE** from public sources             | Medium (5TBY) / n/a (6C1H) | Anderson et al., _PNAS_ 2018 names `5TBY` explicitly; no source found linking `6C1H` to mavacamten                               |
| **C6a** `1OPL` = myristate-bound autoinhibited c‑Abl + ATP-site inhibitor | **CONFIRMED**                                                                                                                          | High                       | Nagar et al., _Cell_ 2003;112:859‑871, doi:10.1016/S0092‑8674(03)00194‑6; RCSB record (`MYR` + `P16`)                            |
| **C6b** `5MO4` = asciminib complex; construct/mutations                   | **CONFIRMED** — and it is a **ternary** asciminib+nilotinib complex in a T334I/D382N construct                                         | High                       | RCSB record + `pdbx_mutation` "T334I D382N"; Wylie et al., _Nature_ 2017, doi:10.1038/nature21702                                |
| **C6c** ABL1 1a vs 1b offset of 19 residues is documented                 | **CONFIRMED**                                                                                                                          | High                       | UniProt P00519 (VSP_004957: 26 aa → 45 aa); Paladini et al., _eLife_ 2024, doi:10.7554/eLife.92324                               |
| **C6d** Myristoyl pocket described as _cryptic_                           | **REFUTED** as stated — literature describes a constitutively present cavity gated by the αI‑helix; no source found calling it cryptic | Medium-High                | Paladini et al., _eLife_ 2024 (empty pocket in `1M52`); Wylie et al. 2017 ("vacant pocket")                                      |
| **C7a** `4OBE` WT + `4LDJ` G12C, same study                               | **CONFIRMED**                                                                                                                          | High                       | Hunter et al., _PNAS_ 2014;111:8895‑8900, doi:10.1073/pnas.1404639111 (PMID 24889603)                                            |
| **C7b** `6OIM` = sotorasib complex, construct                             | **CONFIRMED** — G12C on a C51S/C80L/C118S "cys-light" background                                                                       | High                       | Canon et al., _Nature_ 2019, doi:10.1038/s41586‑019‑1694‑1; RCSB `pdbx_mutation`                                                 |
| **C7c** Switch-II pocket is genuinely cryptic                             | **CONFIRMED**                                                                                                                          | High                       | Ostrem et al., _Nature_ 2013, doi:10.1038/nature12796; Vasta et al., _Nat Chem Biol_ 2022, doi:10.1038/s41589‑022‑00985‑w        |

---

## C1 — `6C1H` is not a cardiac-myosin / mavacamten structure

**Verdict: CONFIRMED (High confidence).**

### Deciding evidence

**RECORD** — RCSB entry `6C1H` (https://www.rcsb.org/structure/6C1H) and the wwPDB data API
(`data.rcsb.org/rest/v1/core/entry/6C1H`):

- Title: _"High-Resolution Cryo-EM Structures of Actin-bound Myosin States Reveal the Mechanism
  of Myosin Force Sensing"_
- Method: electron microscopy, helical reconstruction, **3.9 Å**
- Deposited 2018‑01‑04, released 2018‑01‑31
- Polymer entities: **Actin, alpha skeletal muscle** (UniProt **P68135**, _Oryctolagus
  cuniculus_, chains A–E); **Unconventional myosin-Ib** (UniProt **Q05096**, _Rattus
  norvegicus_, chain F); **Calmodulin** (UniProt P0DP23, _Homo sapiens_, chain G)
- Non-polymer entities: **2** — ADP and MG. No other ligand.
- `struct_keywords` include **"Myosin-I"**.

**PRIMARY** — Mentes A, Huehn A, Liu X, Zwolak A, Dominguez R, Shuman H, Ostap EM, Sindelar CV.
"High-resolution cryo-EM structures of actin-bound myosin states reveal the mechanism of myosin
force sensing." _PNAS_ 2018;115(6):1292–1297. **doi:10.1073/pnas.1718316115**, **PMID
29358376**. The paper reports "near-atomic resolution structures of one rigor and two ADP-bound
states of **myosin-IB (myo1b)** bound to actin." Sister depositions from the same work: `5V7X`,
`6C1D`, `6C1G` — all myosin-1b.

**Mavacamten does not appear in that work, and could not have.** The PDB chemical component
`XB2` (mavacamten) was **created 2023‑10‑26 and first released 2023‑12‑13**
(`data.rcsb.org/rest/v1/core/chemcomp/XB2`) — five years after `6C1H` was released. `6C1H` is
not among the six entries containing `XB2` (see C2).

### Credibility

RCSB/wwPDB record (authoritative for entity identity and citation linkage) corroborated by a
peer-reviewed PNAS article. Two independent evidence types agree. No conflicting source found.

### Caveats

- Our sub-claim that ADP and Mg are bound **"in the actin protomers"** is **not decided by these
  sources**. The records report two non-polymer entities without a chain assignment in the
  summary, and the paper's states are described as "ADP-bound" _myosin_ states, so ADP is
  expected in the myosin chain as well. Which chains carry ADP is a coordinate-level question —
  leave it to the file-level audit; do not assert it from literature.
- Myosin-1b (`MYO1B`, class I, _Rattus norvegicus_) and β-cardiac myosin (`MYH7`, class II,
  _Homo sapiens_) are different genes, different myosin classes, and different species. This is
  not a near-miss.

---

## C2 — Mavacamten is `XB2`; first co-structures deposited 2023 or later

**Verdict: CONFIRMED for the substantive claim. The specific entry list in the claim is wrong on
three of seven IDs.**

### Deciding evidence

**RECORD** — chemical component `XB2`: name **Mavacamten**, formula C₁₅H₁₉N₃O₂, MW 273.33,
synonym **MYK-461**. **Created 2023‑10‑26; initial release 2023‑12‑13.** This alone bounds the
earliest possible mavacamten co-structure in the PDB.

**RECORD** — RCSB search API, exact match on `rcsb_chem_comp_container_identifiers.comp_id =
XB2`, return type `entry`: **exactly six entries** contain mavacamten:

| Entry  | What it is                                                      | Species                                         | Method / res.     | Deposited  | Released       |
| ------ | --------------------------------------------------------------- | ----------------------------------------------- | ----------------- | ---------- | -------------- |
| `8QYQ` | β-cardiac myosin **S1** + mavacamten, pre-powerstroke           | _Bos taurus_ (Q9BE39 + P85100)                  | X-ray 2.61 Å      | 2023‑10‑26 | **2023‑12‑13** |
| `8QYR` | β-cardiac myosin **motor domain** + mavacamten, pre-powerstroke | _Bos taurus_                                    | X-ray             | 2023‑10‑26 | **2023‑12‑13** |
| `9GZ1` | β-cardiac myosin **IHM** + mavacamten                           | _H. sapiens_ MYH7 (P12883) + mouse light chains | cryo-EM 3.7 Å     | 2024‑10‑03 | **2025‑03‑12** |
| `9GZ2` | β-cardiac HMM **motor domain, primed** + mavacamten             | _H. sapiens_ MYH7                               | cryo-EM **2.9 Å** | 2024‑10‑03 | **2025‑03‑12** |
| `9YP9` | β-cardiac myosin + mavacamten, IHM / S2-FH docked               | chimeric _H. sapiens_ MYH7 + mouse LCs          | cryo-EM 3.0 Å     | 2025‑10‑13 | **2026‑04‑08** |
| `9YR7` | (same study as `9YP9`)                                          | —                                               | cryo-EM           | 2025‑10‑13 | 2026‑04‑08     |

**Correction to the claim as posed.** Three of the IDs listed in the claim are _not_ mavacamten
structures:

- `8QYP` = "Beta-cardiac myosin motor domain in the pre-powerstroke state" — **drug-free control**
- `8QYU` = "Beta-cardiac myosin S1 fragment … complexed to **Omecamtiv mecarbil**"
- `9GZ3` = "Beta-cardiac heavy meromyosin motor domain in the primed state" — **drug-free
  control**, ligands ADP/PO₄/Mg only

These are the apo/comparator members of their respective studies, which is useful (see
"What we should tell the challenge organisers"), but they do not contain `XB2`.

### Primary citations

- **PRIMARY** — Auguin D, Robert-Paganin J, Réty S, Kikuti C, David A, Theumer G, Schmidt AW,
  Knölker H-J, Houdusse A. "Omecamtiv mecarbil and Mavacamten target the same myosin pocket
  despite opposite effects in heart contraction." _Nat Commun_ 2024;15:4885.
  **doi:10.1038/s41467-024-47587-9**, **PMID 38849353**. Depositions `8QYP` (PPS‑MD‑Apo),
  `8QYQ` (PPS‑S1‑Mava), `8QYR` (PPS‑MD‑Mava), `8QYU` (PPS‑S1‑OM). Bovine β-cardiac myosin.
- **PREPRINT → PRIMARY** — McMillan SN, Pitts JRT, Barua B, Winkelmann DA, Scarff CA. bioRxiv
  2025.02.12.637875 (posted Feb 2025; the citation attached to `9GZ1`–`9GZ3`), published as
  "Mavacamten inhibits myosin activity by stabilizing the myosin interacting-heads motif and
  stalling motor force generation." _Science Advances_ 2026;12(18):eaea9335,
  **doi:10.1126/sciadv.aea9335**, published **29 Apr 2026**.
- **PREPRINT → PRIMARY** — Somavarapu AK, Ge J, Yengo CM, Craig R, Padrón R. "Cryo-EM reveals
  how cardiomyopathy therapeutic drugs modulate the myosin motors of the heart." bioRxiv
  2025.10.29.685122; _Science Advances_ 2026;12:eaed6472, **doi:10.1126/sciadv.aed6472**,
  published **29 Apr 2026**. Depositions `9YP9`, `9YR7`.

### Was a mavacamten co-structure publicly available on 2026‑04‑17?

**Yes — for 2 years and 4 months.** `8QYQ` and `8QYR` were publicly released **2023‑12‑13**;
human‑MYH7 entries `9GZ1`/`9GZ2` on **2025‑03‑12**; `9YP9`/`9YR7` on **2026‑04‑08**, nine days
before the challenge document date. The peer-reviewed Auguin et al. paper appeared in _Nature
Communications_ in June 2024.

### Credibility

wwPDB records plus one fully peer-reviewed primary paper (Auguin 2024) and two now-peer-reviewed
primary papers (both _Science Advances_, 2026‑04‑29 — note: **after** the challenge document
date, though their preprints and PDB depositions were public well before).

---

## C3 — `5TBY` is not an experimental structure of human β-cardiac myosin

**Verdict: CONFIRMED, with one numeric correction to the claim (the fitted map is 28 Å, not
~20 Å; and it is negative stain, not cryo-EM).**

### Deciding evidence

**RECORD** — RCSB/PDBe entry `5TBY`. The deposited title is itself the deciding evidence, and is
unusually explicit:

> "HUMAN BETA CARDIAC HEAVY MEROMYOSIN INTERACTING-HEADS MOTIF OBTAINED BY **HOMOLOGY MODELING
> (USING SWISS-MODEL)** OF HUMAN SEQUENCE FROM **APHONOPELMA HOMOLOGY MODEL (PDB-3JBH)**,
> **RIGIDLY FITTED** TO HUMAN BETA-CARDIAC **NEGATIVELY STAINED** THICK FILAMENT
> 3D-RECONSTRUCTION (**EMD-2240**)"

Deposited 2016‑09‑13, released 2017‑06‑07. Method field: electron microscopy. Reported
resolution field: **20.0 Å**. Entities: Myosin-7 (P12883) chains A,B; Myosin light chain 3
(P08590) chains C,D; MLC-2v (P10916) chains E,F. **No bound ligands.**

**PRIMARY** — Alamo L, Ware JS, Pinto A, Gillilan RE, Seidman JG, Seidman CE, Padrón R. "Effects
of myosin variants on interacting-heads motif explain distinct hypertrophic and dilated
cardiomyopathy phenotypes." _eLife_ 2017;6:e24634. **doi:10.7554/eLife.24634**, **PMID
28606303**. The model is a human β-cardiac IHM quasi-atomic model built on the tarantula
striated-muscle IHM (`3JBH`) template, exploiting "the high evolutionary conservation between
human MYH7 and tarantula striated myosin (**60% amino acid identity**)."

**RECORD** — EMDB `EMD-2240`: _"3D structure of myosin filaments isolated from human heart
muscles by negative stain electron microscopy and single particle image analysis"_, **28.0 Å**,
**negative stain**, deposited 2012‑12‑07, primary citation Al-Khayat HA, Kensler RW, Squire JM,
Marston SB, Morris EP, _PNAS_ 2013;110:318–323, doi:10.1073/pnas.1212708110.

### What the authors themselves say about the model's limits

From the eLife paper:

- _"There are neither atomic nor near-atomic structures of the human cardiac IHM."_
- The resolution of the IHM "does not define specific atomic contacts or individual side chain
  densities."
- Resolution "comparable (2.0 nm) to the tarantula structure employed here, perhaps because the
  intrinsic flexibility of swaying free heads limits higher resolution."
- "Future models will refine the resolution of interactions identified."
- The tarantula template "lacks MyBP-C and titin, molecules that may interact with IHMs."
- On mapping structural IHM states onto functional DRX/SRX states: "these cannot be proven to be
  synonymous."

The paper **does not mention mavacamten**; its only drug reference is to MYK-461 (mavacamten's
investigational name) as an ATPase inhibitor that "improved the pathophysiology in HCM mouse
models" — i.e. a functional citation, not a structural one.

### Conflict to report, not resolve

The **PDB entry reports 20.0 Å**; the **EMDB record for the map it was fitted to reports
28.0 Å**; the **eLife text says ~2.0 nm (20 Å)** for the IHM resolution while describing
EMD‑2240. These are inconsistent across records. We report the conflict. Either way the map is
an order of magnitude coarser than side-chain resolution.

### Bearing on our argument that residue-level contact networks cannot be built from `5TBY`

The evidence **supports** the argument, but state it precisely to keep it defensible:

- **Supported:** side-chain positions and specific residue–residue atomic contacts in `5TBY` are
  _not experimentally determined_. They are SWISS-MODEL outputs on a 60%-identity arthropod
  template. The authors say so themselves.
- **Supported:** inter-head and head–tail geometry (i.e. the IHM interface that defines the SRX
  state) is fixed by a **rigid-body fit into a 28 Å negative-stain envelope**, so relative domain
  placement carries an error far larger than any contact cutoff we would use.
- **Not supported by this evidence alone:** that a Cα-level contact network _within_ a single
  motor domain is meaningless. A 60%-identity homology model of a well-conserved fold will be
  broadly correct at the backbone level inside each domain. The failure is at the residue-contact
  level and at the inter-domain level — which is exactly where an elastic-network method lives,
  so the conclusion holds, but the argument should be made on those grounds rather than by
  calling the whole model wrong.

### Credibility

RCSB + PDBe + EMDB records, all consistent, plus a peer-reviewed _eLife_ article whose own
authors state the limitations. Highest available quality.

---

## C4 — Where the mavacamten binding site is, per the literature

**Verdict: PARTIALLY CONFIRMED.** The literature places the site exactly where our computation
does, and names 9 of our 12 residues explicitly. But **two residues named in the literature are
absent from our set**, and three of ours are not named in any text we found. Do not report our
set as "confirmed by the literature" without these two caveats.

### Pre-structural inferences (both cited by the challenge)

**PRIMARY** — Green EM, Wakimoto H, Anderson RL, et al. "A small-molecule inhibitor of sarcomere
contractility suppresses hypertrophic cardiomyopathy in mice." _Science_ 2016;351:617–621.
**doi:10.1126/science.aad3456** (challenge ref [22]). We read the full text via PMC4784435:
**it contains no binding-site information whatsoever.** The only mechanistic statement is that
"MYK-461 acts directly on myosin", reducing the duty ratio by slowing the rate-limiting step
(phosphate release). **No structure was determined.**

**PRIMARY** — Anderson RL, Trivedi DV, Sarkar SS, et al. "Deciphering the super relaxed state of
human β-cardiac myosin and the mode of action of mavacamten…" _PNAS_ 2018;115:E8143–E8152.
**doi:10.1073/pnas.1809540115** (challenge ref [23]). Methods: single-turnover MANT-nucleotide
kinetics, negative-stain EM, low-angle X-ray fibre diffraction, skinned-fibre tension. **No
structure with mavacamten bound.** On the site, the closest statement is indirect — mavacamten
"reduce[s] the basal release rates of ADP and Pi, possibly by holding the switch elements in a
closed state" — and the authors explicitly flag the structural basis as open: "the high-resolution
detailed structural basis of formation of this SRX folded-back state … is an intriguing open
question."

**Conclusion on the pre-structural period:** as of the two references the challenge cites for
this target, the mavacamten binding site was **unknown**. Auguin et al. 2024 state this directly:
before their work "the binding site for Mava was unknown."

### Structural determinations

**PRIMARY** — Auguin et al., _Nat Commun_ 2024 (bovine β-cardiac myosin, X-ray). Pocket location:
**"located between the N-terminal (N-term) and the Converter subdomains."** Named contacts:

- `N-term Asp168` — "direct interactions involve N-termAsp168"
- `Conv Asn711` side chain, `Conv Arg712` backbone amide nitrogen
- `HW His666` — "distinct interactions of HW-His666 with both drugs"
- **`N-term Leu120`** — "The isopropyl group of Mava **uniquely** interacts with N-termLeu120";
  "The end of the Transducer β2 strand (L120) **uniquely participates in Mava binding**"
- `Conv Ala767`
- `Tyr164` and `Asn711` named as the two positions that differ in fast skeletal myosin:
  "CardY164/SkF, CardN711/SkS"

Numbering is bovine β-cardiac (UniProt Q9BE39). **The paper does not state that its numbering is
identical to human MYH7.**

**PRIMARY** (preprint text read; now published in _Sci Adv_) — McMillan et al., human MYH7
numbering, cryo-EM `9GZ2`/`9GZ1`:

> "Mavacamten-protein interactions are predominantly hydrophobic formed by the sidechain
> backbones of residues **R721, L770, and I713 on the converter** with isopropyl pyrimidinedione,
> methylethyl ester and phenyl moieties of mavacamten"

> "These hydrophobic contacts are then further supported by an ionic interaction between **Y164
> on the U50** and the isopropyl pyrimidinedione moiety and hydrogen bonding between **N711**,
> the backbone of **R712** from the converter, and **D168** from the U50"

`T167` and `H666` are also named. On mutagenesis/genetic evidence: "HCM mutations **R712L** and
**E774V** would directly affect the mavacamten binding site, likely rendering mavacamten less
effective in patients with these mutations"; "HCM mutations **Arg719→Trp** and **Arg723→Gly**,
within immediate proximity of the binding site, do mildly affect mavacamten binding."

### Comparison with our computed 4.5 Å shell (human MYH7 numbering, from `9GZ2`)

Our set: Tyr164, Thr167, Asp168, His666, Pro710, Asn711, Arg712, Ile713, Arg721, Tyr722, Leu770,
Glu774.

| Residue    | Named in McMillan (human)                        | Named in Auguin (bovine)            |
| ---------- | ------------------------------------------------ | ----------------------------------- |
| Tyr164     | yes (ionic, U50)                                 | yes (Card Y164 vs skeletal F)       |
| Thr167     | yes                                              | —                                   |
| Asp168     | yes (H-bond, U50)                                | yes (N-term Asp168)                 |
| His666     | yes                                              | yes (HW His666)                     |
| Pro710     | —                                                | —                                   |
| Asn711     | yes (H-bond)                                     | yes                                 |
| Arg712     | yes (backbone H-bond); HCM R712L flagged         | yes                                 |
| Ile713     | yes (hydrophobic, converter)                     | —                                   |
| Arg721     | yes (hydrophobic, converter)                     | —                                   |
| Tyr722     | —                                                | —                                   |
| Leu770     | yes (hydrophobic, converter)                     | —                                   |
| Glu774     | flagged as HCM mutation E774V affecting the site | —                                   |
| **Leu120** | **not seen in our set**                          | **yes — "uniquely" a Mava contact** |
| **Ala767** | **not seen in our set**                          | **yes**                             |

**Where the literature disagrees with us.** `Leu120` is the sharpest case: Auguin et al. single it
out as a contact that is _unique to mavacamten_ (vs omecamtiv mecarbil), and it sits in the
Transducer β1–β2 region rather than the N-term/converter cluster our shell captured. `Ala767`
likewise. Candidate explanations — **none of which we can adjudicate from literature alone** —
are (i) different structures: bovine X-ray pre-powerstroke S1/MD vs human cryo-EM primed motor
domain, in which the pocket may not be identically packed; (ii) our 4.5 Å heavy-atom cutoff
excluding a contact the authors describe from a figure; (iii) an unstated bovine↔human numbering
difference. Report the discrepancy; do not paper over it.

**Where absence of evidence is weak.** Pro710, Tyr722 being unnamed in the text is not evidence
against them. Papers name _interactions_, not every residue inside a distance shell; Pro710 and
Tyr722 flank Asn711/Arg712 and Arg721 in sequence and are exactly the kind of shell members prose
omits.

### Credibility and conflicts

Two independent peer-reviewed structural determinations (different labs, different species,
different methods — X-ray vs cryo-EM) agree on the pocket's identity and on the core contacts
Y164/D168/H666/N711/R712. That is strong convergent evidence for the site. The residue-level
lists differ between the two papers themselves (Auguin names L120 and A767 that McMillan does
not; McMillan names T167, I713, R721, L770 that Auguin does not), which is itself a signal that
neither text is a complete distance-based enumeration.

### Open sub-point

Whether bovine (Q9BE39) and human (P12883) β-cardiac myosin share residue numbering over the
motor domain is **UNVERIFIED** here. Neither paper states it. It should be established by
alignment before comparing the two residue lists as if they were in one frame.

---

## C5 — Is there an innocent explanation for the `5TBY` / `6C1H` assignment?

**Verdict: PARTIALLY CONFIRMED. A clean innocent explanation exists for `5TBY`. None was found
for `6C1H`, and its true cause is UNVERIFIABLE from public sources.**

### `5TBY`: innocent explanation found, and it is a good one

**PRIMARY** — Anderson et al., _PNAS_ 2018 — **which is the challenge's own reference [23] for
this target** — cites `5TBY` by accession:

> "fits the MS03 homology-modeled structure from the J.A.S. laboratory (…) and the **5TBY**
> homology modeled structure from the Padrón laboratory"

So `5TBY` is reachable in a single hop from the challenge's own citation, and it is the canonical
published quasi-atomic model of the human β-cardiac **interacting-heads motif**, the structural
correlate of the **super-relaxed state** the challenge names in its objective. Choosing it as the
"cardiac myosin, SRX" structure is a defensible intent. The error is not in _what protein state_
it represents; it is that a homology model rigid-fitted to a 28 Å negative-stain envelope cannot
carry residue-level contacts (C3).

**Independent corroboration that `5TBY` is the field's default IHM model:** it was used as the
myosin II starting point for the recent native cardiac thick-filament model (Nature 2023,
`s41586-023-06690-5`) — **SECONDARY** for our purposes, but it establishes that a non-specialist
searching "human β-cardiac myosin super-relaxed state structure" would land on `5TBY`.

### `6C1H`: no explanation found

Searches performed, all negative:

1. **Web search for any page co-mentioning `5TBY` and `6C1H`** — no result pairs them, in any
   context.
2. **Web search for `6C1H` with mavacamten / super-relaxed / cardiac myosin / allosteric** — every
   hit for `6C1H` resolves to the Mentes 2018 myosin-1b work, RCSB, PDBe, or PDBsum. No source
   associates it with mavacamten or the SRX state.
3. **AlloBench** (Maity & Qiao, _ACS Omega_ 2025;10:17973–17982, PMC12059942) — the most recent
   published allosteric-site benchmark pipeline. **None** of `5TBY`, `6C1H`, `6OIM`, `4OBE`,
   `5MO4`, `1OPL` appears in it. It also does not construct apo/holo pairs at all: it defines
   sites as "residues within 4 Å of the allosteric modulator" in ligand-bound structures only.
4. **PDBbind / BindingDB** — no evidence found associating `6C1H` with any drug. Structurally it
   could not be in an affinity dataset: its only ligands are ADP and Mg.
5. **Allosteric Database (ASD)**, the challenge's own reference [25] and recommended resource at
   `https://mdl.shsmu.edu.cn/ASD/` — **could not be queried: the server's TLS certificate has
   expired** (checked 2026‑08‑20). This is the one avenue we could not close. If ASD contains a
   myosin/mavacamten record pairing these IDs, we would not have seen it.

### Transcription-error hypothesis: tested and not supported

- `6CIH` (capital I substituted for the digit 1) **exists** and is _"Crystal structure of a group
  II intron lariat in the post-catalytic state"_ (Chan et al., _Nat Commun_ 2018;9:4676) —
  a _Pylaiella littoralis_ RNA. Unrelated.
- `6C1G`, `6C1D`, `5V7X` — the sibling depositions from the same Mentes 2018 paper — are all
  myosin-1b. A one-character slip within the `6C1x` family lands on more myosin-1b.
- **No mavacamten structure has an accession within one character of `6C1H`.** The six `XB2`
  entries are `8QYQ`, `8QYR`, `9GZ1`, `9GZ2`, `9YP9`, `9YR7`; none shares a character in any
  matching position with `6C1H`. A typo cannot bridge that distance.

### The strongest circumstantial evidence, and its limit

The other two rows of Table 1 have holo IDs traceable to the challenge's own cited references:
`6OIM` is the deposition of Canon et al. 2019 (ref [19]); `5MO4` is the deposition of Wylie et al.
2017 (ref [20]). The myosin row cites Green 2016 (ref [22]) and Anderson 2018 (ref [23]) —
**neither of which deposited or cites any drug-bound myosin structure**, because none existed
when they were written (C2, C4). So the myosin row's holo entry has no provenance in the
document's own bibliography, whereas the apo entry does.

**What this does and does not establish.** It establishes that `6C1H` did not come from the
sources the document cites for that target. It does **not** establish _how_ it did arise. A stale
citation, a transposition from an unrelated note, an aggregation error in a resource we could not
reach (ASD), or generation without a source are all consistent with what we can see. **We have no
evidence for any of them and should not assert one.**

### What would settle it

Only the organisers: the provenance note or working document behind Table 1's cardiac-myosin row.
Absent that, restoring ASD access would close the one search avenue that remains open.

### Credibility

The negative searches are only as strong as the indexes behind them (web search + two database
APIs + one benchmark paper's full text). Absence of a pairing in these is meaningful but is not
proof that no such source exists anywhere.

---

## C6 — The BCR-ABL1 pair

### (a) `1OPL` — myristate-bound autoinhibited c-Abl that also contains an ATP-site inhibitor

**Verdict: CONFIRMED (High).**

**RECORD** — RCSB `1OPL` and `data.rcsb.org/rest/v1/core/polymer_entity/1OPL/1`:

- Title: "Structural basis for the auto-inhibition of c-Abl tyrosine kinase"
- X-ray, **3.42 Å**; deposited 2003‑03‑06, released 2003‑04‑08
- Entity: proto-oncogene tyrosine-protein kinase, _Homo sapiens_, UniProt **P00519**, 537
  residues, described as **"the N-terminal 531 residues including the MYR-SH3-SH2-Kinase domain
  regions"**; `pdbx_mutation` = **"D382N, K29R, E29D"**
- Ligands: **`MYR`** (myristic acid, chain C) and **`P16`** =
  6-(2,6-dichlorophenyl)-2-{[3-(hydroxymethyl)phenyl]amino}-8-methylpyrido[2,3-d]pyrimidin-7(8H)-one
  — a pyrido[2,3-d]pyrimidinone **ATP-site inhibitor** (PD166326 class), IC₅₀ 2.8–8 nM

**PRIMARY** — Nagar B, Hantschel O, Young MA, Scheffzek K, Veach D, Bornmann W, Clarkson B,
Superti-Furga G, Kuriyan J. "Structural basis for the autoinhibition of c-Abl tyrosine kinase."
_Cell_ 2003;112:859–871. **doi:10.1016/S0092-8674(03)00194-6**, **PMID 12654251**. Abstract:
_"the N-terminal myristoyl modification of c-Abl 1b binds to the kinase domain and induces
conformational changes that allow the SH2 and SH3 domains to dock onto it."_ Sibling depositions
`1OPJ`, `1OPK` (the latter _Mus musculus_, 1.80 Å, also `MYR` + `P16`).

**Consequence for the benchmark.** `1OPL` is being used as the **apo input** for a task whose
objective is to _blind-predict the myristoyl pocket_. On the record, that pocket is **occupied**
(`MYR`), and the ATP site is also occupied (`P16`). It is a doubly-liganded structure.

**Caveat.** `MYR` is deposited as a **separate non-polymer chain**, not as a modified residue.
Whether it is covalently linked to Gly2 in the deposited model is a connectivity question that
must be answered from the file, not from these records. Do not assert covalency from literature.

### (b) `5MO4` — asciminib complex, construct and mutations

**Verdict: CONFIRMED, with an important addition: it is a ternary complex.**

**RECORD** — RCSB `5MO4` and `data.rcsb.org/rest/v1/core/polymer_entity/5MO4/1`:

- Title: **"ABL1 kinase (T334I_D382N) in complex with asciminib and nilotinib"**
- X-ray **2.17 Å**; deposited 2016‑12‑13, released 2017‑04‑05
- Entity: Tyrosine-protein kinase ABL1, _Homo sapiens_, P00519, single chain, 495 residues,
  expressed in _Spodoptera frugiperda_ Sf9; `pdbx_mutation` = **"T334I D382N"**
- Ligands: **`AY7`** (asciminib / ABL001, C₂₀H₁₈ClF₂N₅O₃) and **`NIL`** (nilotinib)

**PRIMARY** — Wylie AA, Schoepfer J, Jahnke W, Cowan-Jacob SW, Loo A, Furet P, et al. "The
allosteric inhibitor ABL001 enables dual targeting of BCR-ABL1." _Nature_ 2017;543:733–737.
**doi:10.1038/nature21702**, **PMID 28329763**. The paper's thesis is dual targeting: "the
combination of ABL001 and nilotinib led to complete disease control", with `5MO4` the structural
demonstration that both sites can be occupied at once. It identifies **A337V** as a myristoyl-site
resistance mutation.

**Conflict to record (a numbering conflict, not a factual one).** The wwPDB record annotates the
mutations as **T334I / D382N** (ABL **1b** numbering). Secondary summaries of the same paper
describe the same construct as **T315I / D363N** (ABL **1a** numbering). Both describe the same
protein: the gatekeeper mutation and the catalytic-aspartate (kinase-dead) mutation. This is
precisely the trap C6(c) is about.

**Consequences for the benchmark.** (i) ~~The holo structure is a kinase domain only, against
an apo (`1OPL`) that carries SH3-SH2-kinase plus the myristoylated cap — the alignment step
must handle a large domain-content mismatch~~ — **withdrawn 2026-08-20.** `5MO4` models auth
**83–531** on chain A (429 residues), RCSB aligns its polymer entity to P00519 **27–515**, and
SIFTS Pfam places SH3 at 86–132: it is N-cap + SH3 + SH2 + kinase, the **same architecture as
`1OPL`**, not a kinase domain. There is no large domain-content mismatch for the alignment to
handle, which is good news rather than bad. Corrected in `docs/targets.md` and
`evidence/target-prior-art.md` (Discrepancy 2) at the time; this paragraph was missed and a
second adversarial review found it still asserting the withdrawn claim. (ii) carries **two
point mutations** including one
that alters the ATP site; (iii) contains a **second drug** (nilotinib) at the ATP site, so a
naive "residues within 4.5 Å of any ligand" rule would label the ATP site as allosteric ground
truth. The ligand must be selected as `AY7` specifically.

### (c) The ABL1 1a vs 1b numbering offset of 19 residues

**Verdict: CONFIRMED (High). Multiple citable sources state it explicitly, and a primary database
record allows it to be derived rather than recalled.**

**RECORD (derivable, not recalled)** — UniProt **P00519** (`rest.uniprot.org/uniprotkb/P00519.txt`):
canonical **isoform IA = 1130 aa**; **isoform IB** = P00519‑2, differing by a single splice
variant **VSP_004957** replacing residues **1–26** (26 aa) with a **45-aa** N-terminal segment
(`MLEICLKLVGCKSKKGLSSSSSCYLE` → `MGQQPGKVLGDQRRPSLPALHFIKGAGKKESSRHGGPHCNVFVEH`).
**45 − 26 = 19.** Isoform IB carries the Gly-2 myristoylation site.

**PRIMARY** — Paladini L, et al. "The molecular basis of Abelson kinase regulation by its
αI-helix." _eLife_ 2024, **doi:10.7554/eLife.92324**. States its convention explicitly:
**"Abl 1b numbering used throughout"**, and notes "Abl 1b being **19 residues longer** and
N-terminally myristoylated."

**SECONDARY (peer-reviewed review)** — Liu Y, Zhang M, Tsai C-J, Jang H, Nussinov R. "Allosteric
regulation of autoinhibition and activation of c-Abl." _Comput Struct Biotechnol J_ 2022,
**doi:10.1016/j.csbj.2022.08.014**: **"The 1b isoform is 19-residue longer than 1a in the
N-terminal region."**

**Practical note for us.** `1OPL` and `5MO4` both carry `D382N` in their `pdbx_mutation` fields,
i.e. **both are annotated in 1b numbering** — so the apo/holo pair is internally consistent. The
+19 offset matters only when mapping to the clinical/TKI literature (T315I, D363N, A337V ↔ A356V).

### (d) Is the myristoyl pocket described as _cryptic_?

**Verdict: REFUTED as posed.** The literature describes a **constitutively present cavity whose
accessibility is gated by the C-terminal αI-helix conformation** — not a cryptic pocket that is
absent or closed in ligand-free structures. **No source was found that calls it cryptic.**

**PRIMARY** — Paladini et al., _eLife_ 2024, is the deciding source:

> The C-terminal αI-helix (residues 504–522, 1b numbering) "adopts a **straight conformation** in
> crystal structures of the **isolated Abl kinase domain with an empty myristoyl binding pocket**
> (PDB **1M52**; Nagar et al., 2002)."

and in the assembled autoinhibited core (PDB `2FO0`) "the helix breaks into two parts" with "the
αI′ part **bending towards the myristoyl bound in the myristoyl pocket**." The paper **does not
use the word "cryptic."**

**PRIMARY** — Wylie et al., _Nature_ 2017: asciminib "engages a **vacant** pocket at a site
normally occupied by the myristoylated N-terminal of ABL1." _Vacant_, not cryptic — the pocket is
there and empty.

**The nuance that must not be lost.** There are also ABL/ABL2 structures in which the **bent αI′
helix occupies part of the pocket volume** (e.g. ABL1 residues 516, 521, 525 overlap the space
imatinib occupies in the corresponding ABL2 structure). So pocket volume is genuinely
conformation-dependent, and a naive geometric pocket-finder may or may not see it depending on
which structure is used. But that is helix-gating, not cryptic-pocket formation, and it is the
opposite sense from the claim: in the ligand-free isolated kinase domain the helix is _straight_
and the pocket is _open_.

**Consequence for the benchmark.** The BCR-ABL1 target is categorically unlike KRAS. The KRAS
switch-II pocket is genuinely absent without ligand (C7c); the ABL myristoyl pocket is a
pre-existing cavity that in our designated apo input (`1OPL`) is **already filled with its native
ligand**. Any claim that our method "discovered a cryptic pocket" in ABL1 would be unsupported.

---

## C7 — The KRAS pair

### (a) `4OBE` = wild-type GDP-bound KRAS; `4LDJ` = G12C GDP-bound, same study

**Verdict: CONFIRMED (High).**

**RECORD** — RCSB `4OBE`: _"Crystal Structure of GDP-bound Human KRas"_, X-ray **1.24 Å**,
deposited 2014‑01‑07, released 2014‑06‑04; GTPase KRas, UniProt **P01116**, chains A and B, 170
residues, **no mutations listed (wild type)**; ligands **GDP** and **MG**.

**RECORD** — RCSB `4LDJ`: _"Crystal Structure of a GDP-bound **G12C** Oncogenic Mutant of Human
GTPase KRas"_, X-ray **1.15 Å**, deposited 2013‑06‑24, released 2014‑06‑04; P01116, chain A,
residues 1–170, **mutation G12C**; ligands **GDP** and **MG**.

**PRIMARY** — Both entries carry the **same** primary citation: Hunter JC, Gurbani D, Ficarro SB,
Carrasco MA, Lim SM, Choi HG, Xie T, Marto JA, Chen Z, Gray NS, Westover KD. "In situ selectivity
profiling and crystal structure of SML-8-73-1, an active site inhibitor of oncogenic K-Ras G12C."
_PNAS_ 2014;111:8895–8900. **doi:10.1073/pnas.1404639111**, **PMID 24889603**.

**Consequence for the benchmark — this is a finding in its own right.** The row is labelled
"KRAS **G12C**", but the assigned apo input `4OBE` is **wild-type**: residue 12 is glycine.
Sotorasib is a **covalent** binder to Cys12 in `6OIM`. So the input structure lacks the residue
that anchors the ground-truth ligand. `4LDJ` — same paper, same nucleotide state, same
crystallisation context, higher resolution — is the matched G12C apo and is the obvious
substitute. Note also that neither `4OBE` nor `4LDJ` carries the C51S/C80L/C118S cys-light
background present in `6OIM`.

### (b) `6OIM` = sotorasib/AMG 510 complex; construct

**Verdict: CONFIRMED (High).**

**RECORD** — RCSB `6OIM` and `data.rcsb.org/rest/v1/core/polymer_entity/6OIM/1`:

- Title: _"Crystal Structure of human KRAS G12C covalently bound to AMG 510"_
- X-ray **1.65 Å**; deposited 2019‑04‑09, released 2019‑11‑06
- Entity: GTPase KRas, P01116, residues **1–183** (167 modelled); `pdbx_mutation` = **"C51S,
  C80L, C118S"** — i.e. the **cys-light** background — in addition to G12C
- Ligands: **`MOV`** = AMG 510 (C₃₀H₃₂F₂N₆O₃), plus **GDP** and **MG**

**PRIMARY** — Canon J, Rex K, Saiki AY, Mohr C, Cooke K, Bagal D, et al. "The clinical KRAS(G12C)
inhibitor AMG 510 drives anti-tumour immunity." _Nature_ 2019;575:217–223.
**doi:10.1038/s41586-019-1694-1**, **PMID 31666701** (challenge ref [19]).

The same cys-light background was introduced by Ostrem et al. 2013, which used
"K-Ras (**G12C/C51S/C80L/C118S**)", the "Cys-light mutant", to enable selective labelling at
position 12. So `6OIM` inherits an established convention — but it means the holo differs from
`4OBE`/`4LDJ` at four positions, three of them engineered.

### (c) Is the Switch-II pocket genuinely cryptic?

**Verdict: CONFIRMED (High).**

**PRIMARY** — Ostrem JM, Peters U, Sos ML, Wells JA, Shokat KM. "K-Ras(G12C) inhibitors
allosterically control GTP affinity and effector interactions." _Nature_ 2013;503:548–551.
**doi:10.1038/nature12796** (challenge ref [18]). Abstract:

> "Crystallographic studies reveal the formation of a **new pocket that is not apparent in
> previous structures of Ras**, beneath the effector binding switch-II region."

Main text, the more careful statement:

> "This **fully formed pocket is not apparent in other published structures of Ras**, although a
> **groove is visible in some cases**."

**PRIMARY (later usage of the term)** — Vasta JD, Peacock DM, Zheng Q, Walker JA, Zhang Z,
Zimprich CA, Thomas MR, Beck MT, Binkowski BF, Corona CR, Robers MB, Shokat KM. "KRAS is
vulnerable to reversible switch-II pocket engagement in cells." _Nat Chem Biol_ 2022;18:596–604.
**doi:10.1038/s41589-022-00985-w**. Describes sotorasib as having "weak reversible affinity to a
**cryptic pocket** on the protein, termed the switch II-pocket (SIIP)", and reports that SII-Ps
of many KRAS hotspot mutants are accessible to non-covalent ligands and that accessibility "is
not necessarily coupled to the GDP state."

### Caveats

- Ostrem's own qualifier — a **groove is visible** in some prior Ras structures — matters for us.
  The SII-P is not a pocket that appears from nothing; it is a shallow groove that opens into a
  pocket. A method that scores the groove region highly in `4OBE` is doing the right thing, and a
  strict "the pocket does not exist in the apo" framing overstates the case.
- Vasta et al. 2022 report that SII-P accessibility is **not** tied to the GDP state, which
  complicates any narrative that the pocket only opens in the GDP-bound, G12C-mutant context.
- The `4OBE` wild-type problem in (a) is the more consequential issue for the benchmark and is
  independent of the cryptic-pocket question.

---

## What we should tell the challenge organisers

Only what the evidence above supports. Stated as findings with sources, not as accusations.

1. **`6C1H` cannot serve as the mavacamten holo ground truth.** It is an actin/**myosin-1b**
   (rat, UniProt Q05096) / calmodulin cryo-EM structure at 3.9 Å from Mentes et al., _PNAS_
   2018 (doi:10.1073/pnas.1718316115). Its only ligands are ADP and Mg — it contains no drug.
   Mavacamten's PDB chemical component `XB2` did not exist until 2023‑10‑26, five years after
   `6C1H` was released. Sources: RCSB entry record; PNAS primary citation; RCSB chem-comp record.

2. **Mavacamten co-structures have been publicly available since 2023‑12‑13, and human ones since
   2025‑03‑12.** Exactly six PDB entries contain mavacamten: `8QYQ`, `8QYR` (bovine, X-ray,
   Auguin et al., _Nat Commun_ 2024, doi:10.1038/s41467-024-47587-9); `9GZ1`, `9GZ2` (human MYH7,
   cryo-EM, McMillan et al., _Sci Adv_ 2026, doi:10.1126/sciadv.aea9335); `9YP9`, `9YR7`
   (Somavarapu et al., _Sci Adv_ 2026, doi:10.1126/sciadv.aed6472, released 2026‑04‑08). For a
   residue-level ground truth in human numbering, **`9GZ2`** (human MYH7, 2.9 Å, XB2 + ADP +
   PO₄ + Mg) is the best-resolved single-domain option, and **`9GZ3`** — the drug-free primed
   motor domain from the same study, same construct, 3.4 Å — is its matched apo. Note that
   `8QYP`, `8QYU` and `9GZ3` are **not** mavacamten structures and should not be described as
   such.

3. **`5TBY` is not an experimental structure and cannot support residue-level contact analysis.**
   Its own deposited title states it is a SWISS-MODEL homology model of the human sequence built
   on a **tarantula** template (`3JBH`, 60% identity) and **rigid-body fitted** to a
   **negative-stain** thick-filament reconstruction (`EMD-2240`, **28 Å** per EMDB; the PDB entry
   reports 20 Å — the records conflict). Its authors state: "There are neither atomic nor
   near-atomic structures of the human cardiac IHM," and that the reconstruction "does not define
   specific atomic contacts or individual side chain densities" (Alamo et al., _eLife_ 2017,
   doi:10.7554/eLife.24634). Its selection is understandable — the challenge's own reference [23],
   Anderson et al. _PNAS_ 2018, cites `5TBY` by name — but a contact-network method cannot use it.

4. **The KRAS apo input is wild-type, not G12C.** `4OBE` is "Crystal Structure of GDP-bound Human
   KRas" with **no mutations** (Hunter et al., _PNAS_ 2014, doi:10.1073/pnas.1404639111).
   Sotorasib in `6OIM` is **covalently bound to Cys12**, a residue absent from the input.
   `4LDJ` — the G12C GDP-bound structure from the **same paper**, 1.15 Å — is the matched apo and
   would fix this without changing anything else about the row.

5. **`1OPL` is not apo with respect to the pocket participants are asked to find.** Its record
   lists **`MYR`** (myristic acid, in the myristoyl pocket) **and `P16`** (a pyrido[2,3-d]-
   pyrimidinone ATP-site inhibitor). It is a doubly-liganded structure. Separately, the myristoyl
   pocket is **not** a cryptic pocket: the literature describes a constitutively present cavity
   gated by the C-terminal αI-helix, open and empty in ligand-free isolated kinase-domain
   structures such as `1M52` (Paladini et al., _eLife_ 2024, doi:10.7554/eLife.92324); Wylie et
   al. 2017 call it a "vacant pocket." This makes the BCR-ABL1 task structurally different from
   the KRAS one, which the scoring design may want to reflect.

6. **Two mechanical notes on the ABL1 pair.** (i) `5MO4` is a **ternary** complex containing
   **both** asciminib (`AY7`) and **nilotinib** (`NIL`); a distance-based ground-truth rule must
   select `AY7` specifically or it will label the ATP site as the allosteric site. (ii) Both
   `1OPL` and `5MO4` are annotated in **ABL 1b numbering** (both carry `D382N`), so the pair is
   self-consistent — but any cross-reference to the clinical literature (T315I, D363N, A337V)
   needs the **+19** isoform offset, derivable from UniProt P00519 (splice variant VSP_004957
   replaces 26 N-terminal residues with 45).

7. **The Allosteric Database (challenge reference [25], recommended for additional targets) is
   currently unreachable.** `https://mdl.shsmu.edu.cn/ASD/` presents an **expired TLS
   certificate** (checked 2026‑08‑20 from one network). Participants directed there for extra
   targets will hit this.

**What we should not tell them.** We have **no evidence** about how the `6C1H` assignment arose.
It is not a one-character typo for any mavacamten entry (`6CIH` is a group II intron lariat; the
sibling `6C1G`/`6C1D` entries are more myosin-1b), and we found no review, database record,
benchmark table, or web resource that pairs `6C1H` with `5TBY`, with mavacamten, or with the
super-relaxed state. The one search avenue we could not close is ASD, which was unreachable.
Report the facts about what `6C1H` is and leave the cause to the organisers.
