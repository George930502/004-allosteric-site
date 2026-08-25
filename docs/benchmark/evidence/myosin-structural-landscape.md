# Cardiac myosin — exhaustive RCSB sweep for allosteric apo/holo pairs

Status: evidence document. Compiled **2026-08-20** from live RCSB queries.
Scope: does cardiac myosin have usable apo/holo pairs for an **allosteric-site prediction**
benchmark beyond the mavacamten pair already frozen in `docs/benchmark/`?

**Verdict up front: the belief that mavacamten is the only route is WRONG, but only just.**
Cardiac myosin carries **three** distinct co-crystallised modulators (mavacamten `XB2`,
omecamtiv mecarbil `2OW`, aficamten `6I6`) sitting in **two** distinct pockets — because
omecamtiv mecarbil and mavacamten **share one pocket** (centroids 2.0–2.4 Å apart, measured
here, and asserted in the title of the depositing paper). The omecamtiv pair the parent asked
about (`5N6A` → `5N69`) is **real and verified**, but it is superseded by the same authors'
re-refinement (`8QYP` → `8QYU`) at markedly better resolution. Aficamten gives a genuinely
**second** pocket 34 Å away — but that pocket **abuts the ATPase site** (3 of its 21 residues
*are* active-site residues), so it is a weak allosteric target and a strong negative control.

Evidence markers follow `target-prior-art.md`: **[derived]** = read out of a machine-readable
RCSB record or computed from deposited coordinates this session; **[asserted]** = the cited
paper states it. Nothing here is recalled.

Reproduce: scripts in the session scratchpad; every geometric number below comes from
`src/allo/structure/pdb.py` (`parse_mmcif`, `contacts`) and
`src/allo/groundtruth/labels.py` (`align_numbering`, `transfer_labels`) run over mmCIF files
fetched from `files.rcsb.org`.

---

## 1. The structural landscape

### 1.1 Entry counts per accession **[derived]**

`search.rcsb.org/rcsbsearch/v2/query`, attribute
`rcsb_polymer_entity_container_identifiers.reference_sequence_identifiers.database_accession`,
`exact_match`, `return_all_hits`.

| Accession | Protein | Entries |
|---|---|---|
| **P12883** | human β-cardiac myosin heavy chain, MYH7 | **46** |
| **Q9BE39** | bovine MYH7 | **9** |
| **P13533** | human α-cardiac myosin heavy chain, MYH6 | **0** |
| P79293 | pig MYH7 (found via gene-name search, not requested) | 6 |

**MYH6 has no structure in the PDB at all.** Two independent queries return zero: the
accession query above, and a gene-name query (`rcsb_entity_source_organism.rcsb_gene_name.value`
= `MYH6`) → 0 entries. The bovine MYH6 accession `Q9BE40` also returns 0. **α-cardiac myosin
is not a candidate target.** This is a finding, not a gap in the search.

Backstop sweep, to catch anything the accession queries miss: Pfam **PF00063** (myosin head,
motor domain) → **247 entries** covering every myosin in the PDB of any class or species.
44 of those carry MYH7 (human, bovine or pig). Every modulator reported below was recovered
by this sweep as well as by the targeted queries.

### 1.2 MYH7 entries — the honest shape of the corpus **[derived]**

Of the 46 P12883 entries, **15 are coiled-coil / rod fragments fused to crystallisation
chaperones** (`4XA1`, `4XA3`, `4XA4`, `4XA6`, `5CHX`, `5CJ0`, `5CJ1`, `5CJ4`, `5WJ7`, `5WJB`,
`5WLQ`, `5WLZ`, `5WME`, `6PF2`, `6PFP` — Gp7/EB1/XRCC4 chimeras of residues 1173–1855) and
carry no motor domain. `2FXM`/`2FXO` are the S2 fragment. `5TBY` is the 20 Å homology model
already condemned in `docs/benchmark/primary/audit/cardiac-myosin.md`. The usable motor-domain corpus
is far smaller than the raw count suggests.

Full per-entry table (method, resolution, chains, all non-polymer components) for all 55
P12883 + Q9BE39 entries: regenerate with the GraphQL query in §7. The motor-domain entries
that matter:

| PDB | Method | Res (Å) | Species | Construct | Ligands (non-buffer) | Study |
|---|---|---|---|---|---|---|
| `4P7H` | X-ray | 3.2 | human | MYH7 motor::GFP chimera, 1023 aa | SO4 only — **nucleotide-free** | Mol. Biol. Cell 2011 (no DOI in record) |
| `4PA0` | X-ray | 2.25 | human | MYH7 motor::GFP chimera, 1024 aa | **2OW** | 10.1038/ncomms8974 |
| `4DB1` | X-ray | 2.6 | human | MYH7 S1dC, 783 aa | ANP, Mn | no DOI in record |
| `5N6A` | X-ray | 3.10 | bovine | MYH7 motor, 828 aa | ADP, Mg, PO4 | 10.1038/s41467-017-00176-5 |
| `5N69` | X-ray | 2.45 | bovine | MYH7 S1 + ELC, 828 aa | ADP, VO4, Mg, **2OW** | same |
| `6FSA` | X-ray | 2.33 | bovine | MYH7 S1 post-rigor | ADP, Mg | 10.1038/s41467-018-06191-4 |
| `8QYP` | X-ray | 2.759 | bovine | MYH7 motor, 780 aa | ADP, VO4, Mg | 10.1101/2023.11.15.567213 |
| `8QYQ` | X-ray | 2.61 | bovine | MYH7 S1 + ELC, 807 aa | ADP, Mg, BeF3, **XB2** | same |
| `8QYR` | X-ray | **1.80** | bovine | MYH7 motor, 781 aa | ADP, Mg, BeF3, **XB2** | same |
| `8QYU` | X-ray | 1.96 | bovine | MYH7 S1 + ELC, 810 aa | ADP, VO4, Mg, **2OW** | same |
| `9F6C` | X-ray | 2.33 | bovine | MYH7 motor, 782 aa | ADP, VO4, Mg, **6I6** | 10.1038/s44161-024-00505-0 |
| `9GZ1` | cryo-EM | 3.7 | human | HMM, IHM, 1145 aa | ADP, PO4, Mg, **XB2** | 10.1101/2025.02.12.637875 |
| `9GZ2` | cryo-EM | 2.9 | human | HMM motor, primed, 1145 aa | ADP, PO4, Mg, **XB2** | same |
| `9GZ3` | cryo-EM | 3.4 | human | HMM motor, primed, 1145 aa | ADP, PO4, Mg | same |
| `9YOP` | cryo-EM | 3.5 | human | IHM, S2-FH docked | ADP, PO4 | 10.1126/sciadv.aed6472 |
| `9YRG` | cryo-EM | 3.2 | human | IHM, S2-FH undocked | ADP, PO4 | same |
| `9YP4` | cryo-EM | 4.5 | human | IHM, docked | ADP, PO4, **2OW** | same |
| `9YRH` | cryo-EM | 3.8 | human | IHM, undocked | ADP, PO4, **2OW** | same |
| `9YP9` | cryo-EM | 3.0 | human | IHM, docked | ADP, PO4, **XB2** | same |
| `9YR7` | cryo-EM | 3.0 | human | IHM, undocked | ADP, PO4, **XB2** | same |
| `8ACT` | cryo-EM | 3.6 | human | HMM folded-back off state | ADP, PO4, Mg | 10.1038/s41467-023-38698-w |
| `9HTF`/`9HTG`/`9I8P` | X-ray | 2.48/2.60/2.60 | human | motor, Y115H / E497D / WT | ADP, VO4, Mg | 10.1038/s41467-025-63816-1 |
| `9TPJ`/`9TPK`/`9TPL` | cryo-EM | 3.0–3.8 | human | IHM, E525K and 2 conformations | ADP, PO4, Mg | 10.1038/s41467-026-73572-5 |
| `9YA8`/`9YAQ` | cryo-EM | 4.32/4.63 | **pig** | native cardiac cross-bridge, rigor | ADP, Mg (+Ca in `9YAQ`) | to be published |

Everything else in the P12883/Q9BE39/P79293 set is actomyosin, thick filament, or rod
fragment, with only ADP/Mg present.

---

## 2. Every small-molecule modulator, confirmed or denied

### 2.1 Present on cardiac myosin **[derived]**

Query: `rcsb_nonpolymer_entity_container_identifiers.nonpolymer_comp_id` `exact_match`.

| Comp | Name in the chem-comp record | MW | Entries |
|---|---|---|---|
| **`XB2`** | Mavacamten (synonyms include **MYK-461**) | 273.33 | `8QYQ`, `8QYR`, `9GZ1`, `9GZ2`, `9YP9`, `9YR7` |
| **`2OW`** | methyl 4-(2-fluoro-3-{[(6-methylpyridin-3-yl)carbamoyl]amino}benzyl)piperazine-1-carboxylate; synonym **Omecamtiv Mecarbil** | 401.44 | `4PA0`, `5N69`, `8QYU`, `9YP4`, `9YRH` |
| **`6I6`** | **aficamten** | 337.38 | `9F6C` |

`2OW` is confirmed as omecamtiv mecarbil from the component's own synonym list, not from
memory. Aficamten is deposited under its INN, **not** under CK-274/CK-3773274 — those
strings return zero chem-comp hits, which is why searching by code name looks like absence.

### 2.2 Explicitly searched for and ABSENT **[derived]**

Searched by `chem_comp.name` and `rcsb_chem_comp_synonyms.name` (`contains_phrase`) **and**
by entry-level full-text.

| Compound | Result |
|---|---|
| **danicamtiv / MYK-491** | **0** chem comps, **0** entries. No deposited structure. |
| **MYK-581** | **0** chem comps, **0** entries. |
| **CK-274 / CK-3773274** | 0 under those strings — the molecule is present as `6I6` "aficamten". |
| **reldesemtiv** | 0. |
| **blebbistatin on cardiac myosin** | `BIT` exists in 5 entries and `BL4`/`BL6`/`BL7` in 3 more, but **every one is *Dictyostelium* myosin-2 (P08799)**. No cardiac, skeletal or smooth vertebrate blebbistatin co-structure. |
| **EMD 57033** | `EMD` exists in exactly **one** entry, `1IH0` — and that is **human cardiac troponin C** (P63316), solution NMR, not myosin. EMD 57033 is a troponin-C calcium sensitiser, not a myosin modulator. |
| **tirasemtiv** | `W97` in `7KAA` only — fast skeletal **troponin C–troponin I**, NMR. Not myosin. |
| **para-nitroblebbistatin** | no chem comp with that name; the deposited blebbistatin analogues are `BL4`/`BL6`/`BL7` (methyl and des-methyl variants). |
| **chemical analogues** | Fingerprint-similarity search on the SMILES of `XB2`, `2OW` and `6I6` each returns **only the query compound**. There are no near-neighbour myotropes in the PDB under other codes. |

### 2.3 Modulators on other myosins — found by sweep, not by name **[derived]**

Of the 247 PF00063 entries, **56** carry a drug-like non-polymer component (≥140 Da,
excluding buffers and nucleotides); **33 distinct** such components. The ones that are
genuine motor modulators rather than nucleotide analogues:

| Comp | Compound | Entries | Protein |
|---|---|---|---|
| `BIT` | (S)-(−)-blebbistatin | `1YV3`, `3MJX`, `3MYH`, `3MYK`, `6Z7U` | *Dictyostelium* myosin-2 |
| `BL4`/`BL6`/`BL7` | blebbistatin analogues | `3BZ7`/`3BZ8`/`3BZ9` | *Dictyostelium* myosin-2 |
| `PJT` | **MPH-220** | `6YSY` | rabbit **skeletal** myosin (Q28641) |
| `A1IGE` | **MT-228** | `9FU2` | human **smooth-muscle** myosin II (P35749) |
| `52E` | **CK-571 / CK-2018571** | `5M05`, `5T45` | chicken **smooth-muscle** myosin (P10587) |
| `PBQ` | pentabromopseudilin | `2JHR` | *Dictyostelium* myosin-2 |
| `IA2` | pentachloropseudilin | `2XEL` | *Dictyostelium* myosin-2 |
| `H70` | tribromodichloropseudilin | `2XO8` | *Dictyostelium* myosin-2 |
| `KI9` | pentachlorocarbazol-1-ol | `2X9H` | *Dictyostelium* myosin-2 |
| `27X` | ammosamide 272 | `4AE3` | *Dictyostelium* myosin-2 |
| `Q5Q` | adhibin analogue (dibromo-carbazole) | `6Z2S` | *Dictyostelium* myosin-2 |
| `STL` | resveratrol | `3MNQ` | *Dictyostelium* myosin-2 |
| `Q8V` | phenamacril | `6UI4` | *Fusarium* myosin I |
| `KQ0`, `A1JT8` | pyrazole-amide antimalarials | `8CDM`/`8CDQ`, `9T7I` | *Plasmodium* MyoA |

None of these is on a cardiac myosin. Their value is that three of them (`PJT`, `A1IGE`,
`BIT`) occupy the **same pocket as aficamten**, which is what makes that pocket's definition
transferable (§3.2).

---

## 3. Where each site is — measured, not recalled

All distances below were computed in **one common frame**: bovine cardiac MYH7
pre-powerstroke `8QYR` chain B. Cross-entry and cross-species correspondence came from
`align_numbering` (BLOSUM62 global alignment of the *modelled* sequences), then Kabsch
superposition on the mapped Cα pairs with the worst 20 % trimmed and refitted. Core RMSDs are
reported so the reader can judge each superposition.

### 3.1 Pairwise ligand-centroid distance matrix (Å) **[derived]**

```
                   8QYR   5N69   8QYU   9YRH   9F6C   1YV3   6YSY   9FU2   4PA0   5M05   2JHR   4AE3   6Z2S    ADP
8QYR:XB2   (mava)   0.0    2.0    2.3    2.1   34.2   32.9   34.8   33.3   17.6   17.7   43.0   37.8   42.0   30.8
5N69:2OW   (OM)     2.0    0.0    0.3    0.3   33.5   32.3   34.1   32.6   16.3   16.4   42.6   37.6   41.3   29.2
8QYU:2OW   (OM)     2.3    0.3    0.0    0.4   33.6   32.4   34.2   32.7   16.1   16.3   42.8   37.8   41.4   29.1
9YRH:2OW   (OM)     2.1    0.3    0.4    0.0   33.6   32.4   34.3   32.8   16.5   16.6   42.7   37.8   41.4   29.2
9F6C:6I6   (afica) 34.2   33.5   33.6   33.6    0.0    1.4    1.2    0.9   34.2   30.2   13.1   11.1    7.9   19.8
1YV3:BIT   (bleb)  32.9   32.3   32.4   32.4    1.4    0.0    2.0    0.6   33.4   29.4   13.5   11.1    9.2   19.8
6YSY:PJT   (MPH)   34.8   34.1   34.2   34.3    1.2    2.0    0.0    1.7   34.8   30.8   12.7   10.0    7.3   21.0
9FU2:A1IGE (MT228) 33.3   32.6   32.7   32.8    0.9    0.6    1.7    0.0   33.6   29.6   13.5   11.2    8.7   19.7
4PA0:2OW   (OM!)   17.6   16.3   16.1   16.5   34.2   33.4   34.8   33.6    0.0    4.1   46.4   37.9   40.9   28.0
5M05:52E   (CK571) 17.7   16.4   16.3   16.6   30.2   29.4   30.8   29.6    4.1    0.0   42.5   33.8   36.8   25.3
2JHR:PBQ   (PBP)   43.0   42.6   42.8   42.7   13.1   13.5   12.7   13.5   46.4   42.5    0.0   15.6   11.6   29.5
```
Superposition quality (core RMSD onto `8QYR`/B): `5N69` 0.73 Å, `8QYU` 0.87 Å, `9YRH` 1.84 Å,
`9F6C` 0.52 Å, `1YV3` 0.91 Å, `6YSY` 0.97 Å, `9FU2` 0.75 Å, `2JHR` 1.01 Å, **`5M05` 1.85 Å**,
**`4PA0` 2.70 Å** (the two high ones are the two entries in a different structural state).

### 3.2 The four pockets

**Site 1 — the omecamtiv/mavacamten pocket. ALLOSTERIC.**
Mavacamten and omecamtiv mecarbil centroids are **2.0–2.4 Å apart** in every pre-powerstroke
or primed structure — the same pocket, with partly different footprints. Contact residues
(4.5 Å, bovine/human MYH7 auth numbering, identical in both species) **[derived]**:

- `XB2` (12–15 residues, reproducible across all six entries): **Tyr164, Thr167, Asp168,
  His666, Pro710, Asn711, Arg712, Ile713, Arg721, Tyr722, Leu770, Glu774**, plus Leu120,
  Gln163, Glu170 in the higher-resolution copies, plus Glu497/Glu500 in `9GZ1`.
- `2OW` (18–20 residues) adds a lobe toward the N-terminal subdomain: **Lys146, Arg147,
  Asn160, His492, Phe765, Gly771, Arg777** on top of the mavacamten set.

Location: the cleft between the **N-terminal subdomain**, the **transducer/HW helix** and
the **relay/converter** — the residue 710–722 stretch is the SH1-helix/relay region and 164–170
is the N-terminal subdomain. Distance to the nucleotide: **centroid 29–31 Å**, minimum
heavy-atom ligand→nucleotide **21.7 Å** (`8QYU`, omecamtiv) to **27.3 Å** (`9GZ1`, mavacamten), minimum Cα label→active-site **11.7–18.3 Å**,
and **zero** overlap between the label set and the active-site set. Genuinely distal.

**[asserted]** Planelles-Herrero *et al.* 2017 (doi:10.1038/s41467-017-00176-5): "omecamtiv
mecarbil binds to an **allosteric site** that stabilizes the lever arm in a primed position."
**[asserted]** Auguin *et al.* 2024 (doi:10.1038/s41467-024-47587-9), whose title is
"**Omecamtiv mecarbil and Mavacamten target the same myosin pocket** despite opposite effects
in heart contraction": "both drugs target the same pocket and stabilize a pre-stroke
structural state, with only few local differences." Our 2.0–2.4 Å measurement is an
independent confirmation.

**Site 2 — the blebbistatin pocket. Aficamten's site. Distinct from Site 1, but PROXIMAL.**
Aficamten (`6I6`, `9F6C`) sits **34.2 Å** from Site 1 and within **0.9–2.0 Å** of blebbistatin
(`1YV3`), MPH-220 (`6YSY`, skeletal) and MT-228 (`9FU2`, smooth) — one conserved pocket at
the apex of the **50 kDa cleft**, at the mouth of the γ-phosphate tunnel. Contacts in cardiac
numbering **[derived]**: **Ser242, Arg243, Phe244, Gly245, Tyr266, Leu267, Leu268, Glu269,
Lys270, Ile462, Ala463, Phe473, Glu474, Cys477, Ile478, Thr481, Val647, His651, Asn654,
Leu655, Leu658**.

⚠️ **This pocket abuts the active site.** Minimum heavy-atom ligand→ADP **10.4 Å**;
ligand→Mg **9.0 Å**; minimum Cα label→P-loop **7.0 Å**; and **3 of the 21 pocket residues
(242, 243, 463) are themselves active-site residues** under ADR 0005 rule 1. Label→active-site
Cα distances run **0.0 – 15.7 Å, median 8.4 Å**. Compare mavacamten on the same apo frame:
**17.5 – 38.5 Å, zero overlap.** Aficamten is pharmacologically allosteric (it is not
nucleotide-competitive) but geometrically it is *adjacent*, and a "connectivity to the active
site" score will rank it top for trivial reasons — the KRAS Switch-II confound of ADR 0005,
worse.

**[asserted]** Hartman *et al.* 2024 (doi:10.1038/s44161-024-00505-0; Chuang is 4th of 20 authors, and an earlier draft cited this as "Chuang 2024"): aficamten binds "an
**allosteric site** on the myosin catalytic domain **distinct from mavacamten**". Confirmed
here at 34.2 Å.

**Site 3 — the recovery-stroke / CK-571 pocket. ALLOSTERIC, but contested on cardiac myosin.**
The omecamtiv molecule in `4PA0` is **not** in Site 1. It is **17.6 Å** away, and **4.1 Å**
from where CK-571 (`52E`) binds chicken smooth-muscle myosin in `5M05`/`5T45` — i.e. `4PA0`
places OM in the CK-571 pocket. Contacts in `4PA0` **[derived]**: **Ala91, Met92, Leu93,
Thr94, Leu96, Ser118, Gly119, Phe121, Phe489, Met493, Glu497, Val698, Gly701, Ile702, Cys705,
Pro710, Asn711, Arg712, Ile713, Leu770** — sharing only 710–713 and 770 with Site 1. Minimum
Cα to the `4P7H` P-loop (located by sequence motif `GESGAGKT` at auth 178–185): **11.4 Å**,
median 21.6 Å.

**[asserted]** Winkelmann *et al.* 2015 (doi:10.1038/ncomms8974): "a single OM-binding site
nestled in a **narrow cleft separating two domains** of the human cMD." **[asserted]** Sirigu
*et al.* 2016 (doi:10.1073/pnas.1609342113) on CK-571: "a **novel allosteric pocket that opens
up during the 'recovery stroke' transition**."

The literature has not reconciled these. Four later omecamtiv structures — two bovine X-ray
(`5N69`, `8QYU`) and two human cryo-EM (`9YP4`, `9YRH`), from three independent groups — all
place OM in Site 1. `4PA0` is a **GFP chimera, nucleotide-free**, and superposes onto `8QYR`
at 2.70 Å core RMSD (8.4 Å without alignment-based correspondence), i.e. a different
structural state. **Do not use `4P7H` → `4PA0` as ground truth without resolving this.**

**Site 4 — the pentabromopseudilin pocket. ALLOSTERIC. No cardiac structure exists.**
`PBQ`/`IA2`/`H70`/`KI9`/`27X`/`Q5Q`, all on *Dictyostelium* myosin-2, 43 Å from Site 1 and
13 Å from Site 2, at the tip of the 50 kDa domain near the actin interface.
**[asserted]** Fedorov *et al.* 2009 (doi:10.1038/nsmb.1542): "a previously unknown allosteric
site near the tip of the 50-kDa domain, at a distance of **16 Å from the nucleotide binding
site** and 7.5 Å away from the blebbistatin binding pocket." Our minimum heavy-atom
PBQ→nucleotide distance in `2JHR` is **16.1 Å** — the paper's own number, reproduced.
**No cardiac (or any vertebrate) myosin co-structure at this site has been deposited**, so it
cannot enter a cardiac benchmark; it is available only as a *Dictyostelium* target
(`2JJ9` → `2JHR`, 2.3 / 2.8 Å, same paper, 4/17 transplant clashes).

---

## 4. Apo/holo pairability — measured **[derived]**

Method per pair: pocket = holo residues with a heavy atom within 4.5 Å of the named ligand in
the named chain; `align_numbering` maps holo→apo author numbering; Kabsch on mapped Cα with
20 % trim; **transplant test** = move the holo ligand into the apo frame with that transform
and count ligand atoms whose nearest apo protein heavy atom is < 2.5 Å (the crypticity probe
used on KRAS in `docs/benchmark/primary/audit/kras-g12c.md`).

| Apo → Holo | Ligand | Same study | Res apo/holo (Å) | Cα pairs | RMSD all / core | Pocket n / mapped / identical | Pocket RMSD | Transplant clashes | Min dist |
|---|---|---|---|---|---|---|---|---|---|
| `9GZ3` → `9GZ2` | XB2 | ✅ | 3.4 / 2.9 | 764 | 1.24 / **0.44** | 12 / 12 / 12 | 1.23 | **0 / 20** | 2.75 |
| `8QYP` → `8QYR` | XB2 | ✅ | 2.76 / **1.80** | 700 | 1.31 / 0.46 | 15 / 15 / 15 | 2.09 | **0 / 20** | 2.84 |
| `8QYP` → `8QYQ` | XB2 | ✅ | 2.76 / 2.61 | 706 | 2.55 / 0.35 | 12 / 12 / 12 | 2.73 | **0 / 20** | 2.55 |
| `9YRG` → `9YR7` | XB2 | ✅ | 3.2 / 3.0 | 912 | 0.89 / 0.33 | 12 / 12 / 12 | 0.46 | **0 / 20** | 2.75 |
| `9YOP` → `9YP9` | XB2 | ✅ | 3.5 / 3.0 | 912 | 0.74 / 0.41 | 12 / 12 / 12 | 0.44 | **0 / 20** | 3.04 |
| `8QYP` → `8QYU` | **2OW** | ✅ | 2.76 / **1.96** | 699 | 1.24 / 0.47 | 18 / 18 / 18 | 2.12 | **0 / 29** | 2.84 |
| `5N6A` → `5N69` | **2OW** | ✅ | 3.10 / 2.45 | 698 | 2.75 / 1.09 | 19 / **17** / 17 | 2.19 | 4 / 29 | 2.20 |
| `9YRG` → `9YRH` | **2OW** | ✅ | 3.2 / 3.8 | 912 | 3.34 / 1.32 | 19 / 19 / 19 | 1.61 | 2 / 29 | 2.05 |
| `9YOP` → `9YP4` | **2OW** | ✅ | 3.5 / 4.5 | 912 | 2.96 / 1.32 | 19 / 19 / 19 | 1.48 | 3 / 29 | 1.76 |
| `8QYP` → `9F6C` | **6I6** | ❌ | 2.76 / 2.33 | 705 | 1.02 / 0.33 | 21 / 21 / 21 | 0.43 | 1 / 25 | 2.25 |
| `5N6A` → `9F6C` | 6I6 | ❌ | 3.10 / 2.33 | 683 | 2.08 / 0.88 | 21 / 21 / 21 | 0.81 | 7 / 25 | 1.64 |
| `9GZ3` → `9F6C` | 6I6 | ❌ (cross-species) | 3.4 / 2.33 | 715 | 1.20 / 0.51 | 21 / 21 / 21 | 0.78 | 5 / 25 | 1.77 |
| `4P7H` → `4PA0` | 2OW | related entries | 3.2 / 2.25 | 960 | 1.25 / 0.68 | 20 / 20 / 20 | 0.50 | **0 / 29** | 2.62 |
| `6Z7T` → `6Z7U` | BIT (*Dicty*) | ✅ | 1.88 / 2.58 | 720 | 1.97 / 0.63 | 18 / 18 / 18 | 0.85 | 13 / 22 | 0.57 |
| `2JJ9` → `2JHR` | PBQ (*Dicty*) | ✅ | 2.3 / 2.8 | 692 | 0.49 / 0.25 | 14 / 14 / 14 | 0.30 | 4 / 17 | 1.22 |
| `2JJ9` → `1YV3` | BIT (*Dicty*) | ❌ | 2.3 / 2.0 | 684 | 0.42 / 0.26 | 19 / 19 / 19 | 0.58 | **16 / 22** | 0.98 |

**Which studies deposited their own apo** (entries sharing a primary-citation DOI) **[derived]**:

| DOI | Entries |
|---|---|
| 10.1038/s41467-017-00176-5 (Planelles-Herrero 2017, OM) | `5N69` (holo), **`5N6A` (apo)** |
| 10.1101/2023.11.15.567213 → 10.1038/s41467-024-47587-9 (Auguin 2024) | **`8QYP` (apo)**, `8QYQ`, `8QYR` (XB2), `8QYU` (2OW) |
| 10.1101/2025.02.12.637875 (2025, human HMM) | **`9GZ3` (apo)**, `9GZ2`, `9GZ1` (XB2) |
| 10.1126/sciadv.aed6472 (Sci Adv 2026, human IHM) | **`9YOP`, `9YRG` (apo)**, `9YP9`, `9YR7` (XB2), `9YP4`, `9YRH` (2OW) |
| 10.1038/s44161-024-00505-0 (aficamten) | `9F6C` **only — no apo deposited** |
| 10.1038/ncomms8974 (Winkelmann 2015) | `4PA0` only; `4P7H` is a separate entry (released 2014-05-21; primary citation *Mol. Biol. Cell* 2011, no DOI in the record) named in `4PA0`'s own `_pdbx_database_related` |

### 4.1 The omecamtiv pair the parent asked about — VERIFIED, then SUPERSEDED

`5N6A` and `5N69` are **both real, both from doi:10.1038/s41467-017-00176-5, and they are a
genuine matched pair** **[derived]**:

- `5N6A`: X-ray **3.10 Å**, one chain (A), bovine MYH7 828 aa, ligands **ADP, Mg, PO4, glycerol** —
  drug-free, pre-powerstroke. Released 2017-08-09.
- `5N69`: X-ray **2.45 Å**, chains A/B (heavy chain) + G/H (bovine ELC, P85100), same 828 aa
  construct, ligands **ADP, vanadate, Mg, 2OW**, plus glycerol and TCEP. Released 2017-08-16.
- The apo is the **motor domain alone**; the holo is the **S1 fragment with the essential light
  chain**. Same heavy-chain construct, same state, but the holo has an extra polymer entity.
- Caveats: the apo's nucleotide is **ADP + free phosphate**, the holo's is **ADP·vanadate** —
  chemically different transition-state mimics, though both pre-powerstroke. **2 of the 19
  pocket residues (Arg721, Tyr722) are not modelled in `5N6A`** and are therefore lost from the
  transferred label set. Core RMSD 1.09 Å, transplant 4/29 clashes.

**Both entries were re-refined by the same laboratory** and deposited as `8QYP` (from `5N6A`,
`_pdbx_database_related` content type "re-refinement") and `8QYU` (from `5N69`, likewise), at
**2.759 Å and 1.96 Å** — a full 0.34 Å and 0.49 Å better, with all 18 pocket residues modelled,
core RMSD 0.47 Å and **0 / 29 transplant clashes**. There is no reason to use `5N6A` → `5N69`
when `8QYP` → `8QYU` is the same experiment, better.

---

## 5. Verdict — ranked list of viable pairs

### 5.1 Ranking

| # | Apo → Holo | Ligand | Site | Species / method | Why here |
|---|---|---|---|---|---|
| **1** | **`8QYP` → `8QYR`** | XB2 mavacamten | 1 | bovine, X-ray 2.76 / **1.80 Å** | Highest-resolution myosin drug complex in the PDB. Same study, same construct, same ADP·transition-state, 15/15 pocket residues modelled and identical, 0/20 transplant clashes. |
| **2** | **`8QYP` → `8QYU`** | **2OW omecamtiv** | 1 | bovine, X-ray 2.76 / **1.96 Å** | **New arm.** Same apo as #1, second drug, larger 18-residue footprint in the same pocket. Lets the benchmark score two overlapping label sets against one input. Supersedes `5N6A` → `5N69`. |
| **3** | **`9GZ3` → `9GZ2`** | XB2 | 1 | human, cryo-EM 3.4 / 2.9 Å | Already frozen. Human sequence, construct-identical, 0/20 clashes. Keep as the human primary. |
| **4** | **`9YRG` → `9YR7`** and **`9YOP` → `9YP9`** | XB2 | 1 | human, cryo-EM 3.2 / 3.0 and 3.5 / 3.0 Å | Experimental human IHM. Best core RMSDs of any arm (0.33 / 0.41 Å), pocket RMSD 0.44–0.46 Å, 0 clashes. Two independent conformations from one study. |
| **5** | **`9YRG` → `9YRH`** and **`9YOP` → `9YP4`** | **2OW** | 1 | human, cryo-EM 3.2 / 3.8 and 3.5 / 4.5 Å | **New.** Omecamtiv in the human IHM, same-study apo. Holo resolution is the weak point (3.8 and 4.5 Å). |
| **6** | `5N6A` → `5N69` | 2OW | 1 | bovine, X-ray 3.10 / 2.45 Å | Verified genuine, but superseded by #2 (same crystals, better refinement, no unmodelled pocket residues). Keep only as a provenance note. |
| **7** | `8QYP` → `9F6C` | **6I6 aficamten** | **2** | bovine, X-ray 2.76 / 2.33 Å | The **only** route to a second pocket. Excellent geometry (core RMSD 0.33 Å, 21/21 residues, 1/25 clashes) but **cross-study** and the pocket **abuts the active site** — see the warning below. |
| **8** | `4P7H` → `4PA0` | 2OW | **3** | human, X-ray 3.2 / 2.25 Å | Geometrically the cleanest pair in the whole set (0/29 clashes, pocket RMSD 0.50 Å, 20/20 residues) but the **ligand placement contradicts four later structures**. Unusable as ground truth until the contradiction is adjudicated. |
| — | `2JJ9` → `2JHR` (PBQ) and `6Z7T` → `6Z7U` (BIT) | — | 4, 2 | *Dictyostelium* | Not cardiac. Listed only as out-of-family options if the benchmark ever wants a third pocket. |

### 5.2 Which sites are genuinely DISTINCT

Two, on cardiac myosin, with deposited co-structures:

1. **Site 1 — the omecamtiv/mavacamten pocket.** N-terminal subdomain / transducer /
   relay-converter cleft. 29–31 Å from the nucleotide, **no overlap** with the active site.
   The correct primary allosteric target. Two chemically unrelated drugs with **opposite
   pharmacology** (activator vs inhibitor) bind it, which is itself a strong benchmark
   property: the same pocket must be found regardless of which ligand defined the labels.
2. **Site 2 — the blebbistatin/aficamten pocket.** 50 kDa cleft apex. 34 Å from Site 1.
   Conserved across cardiac, skeletal, smooth and *Dictyostelium* myosin II, so the pocket
   definition is transferable. **But** it is 7.0 Å (Cα) from the P-loop and shares three
   residues with the active site.

Two more exist but are not usable on cardiac myosin: **Site 3** (recovery-stroke / CK-571) has
one contested cardiac structure and two solid smooth-muscle ones; **Site 4** (pentabromopseudilin)
has no vertebrate structure at all.

### 5.3 Recommendation

**Was the belief "mavacamten is the only route" correct?** No — but the correction is smaller
than it looks. Omecamtiv mecarbil doubles the number of usable holo entries and provides an
opposite-pharmacology control, **but it lands in the same pocket**, so it does not give the
benchmark a second ground-truth site. Aficamten does give a second site, but that site is
active-site-adjacent and has no same-study apo.

Concretely:

- **Add `8QYP` → `8QYU` (omecamtiv, 1.96 Å) as a same-pocket, different-ligand arm.** It costs
  nothing — the apo is already in the frozen set — and it tests label-set robustness directly.
- **Add `9YRG` → `9YRH` / `9YOP` → `9YP4`** if a human omecamtiv arm is wanted; note the 3.8 /
  4.5 Å holo resolution.
- **Consider `8QYP` → `9F6C` (aficamten) as a second scored pocket, but report its
  active-site adjacency prominently** and evaluate it on a distal-only label subset as
  ADR 0005 already prescribes for KRAS. On the full set it will look easy for the wrong reason.
- **Do not** promote `5N6A` → `5N69` over `8QYP` → `8QYU`, and **do not** use `4P7H` → `4PA0`.
- **α-cardiac myosin (MYH6) is structurally unavailable.** Do not plan around it.

---

## 6. Explicit negative findings

Stated because they were actually searched, not assumed:

- **MYH6 / P13533: zero PDB entries.** Confirmed by accession query and by gene-name query.
- **Danicamtiv (MYK-491): no chem comp, no entry.** Both name and full-text searches return 0.
- **MYK-581: no chem comp, no entry.**
- **Reldesemtiv: no chem comp, no entry.**
- **No blebbistatin or blebbistatin-analogue structure on any vertebrate myosin.** All 8
  blebbistatin-family entries are *Dictyostelium*.
- **EMD 57033 is not a myosin ligand.** Its single PDB entry `1IH0` is cardiac troponin C.
- **No chemical analogue of mavacamten, omecamtiv or aficamten exists in the PDB** under any
  other component code (fingerprint-similarity search returns only the query compound).
- **The aficamten study deposited no apo structure**; every apo pairing for `9F6C` is
  cross-study.
- **No cardiac myosin structure exists with a ligand at the pentabromopseudilin site.**

---

## 7. Provenance

Endpoints used, all 2026-08-20:

- `POST https://search.rcsb.org/rcsbsearch/v2/query` — text service on
  `…reference_sequence_identifiers.database_accession`,
  `rcsb_nonpolymer_entity_container_identifiers.nonpolymer_comp_id`,
  `rcsb_polymer_entity_annotation.annotation_id` (PF00063),
  `rcsb_primary_citation.pdbx_database_id_DOI`,
  `rcsb_entity_source_organism.rcsb_gene_name.value`; `text_chem` service on `chem_comp.name`
  and `rcsb_chem_comp_synonyms.name`; `full_text` service; `chemical` service with
  `fingerprint-similarity` on SMILES.
- `POST https://data.rcsb.org/graphql` — batched `entries(entry_ids:…)` for `struct.title`,
  `exptl.method`, `rcsb_entry_info.resolution_combined`, `rcsb_accession_info`,
  `rcsb_primary_citation`, `pdbx_database_related`, `polymer_entities` (description, chains,
  UniProt refs, source organism, length) and `nonpolymer_entities` (chem-comp id/name/weight).
- `GET https://data.rcsb.org/rest/v1/core/chemcomp/{id}` — names, synonyms, formula, SMILES.
- `GET https://files.rcsb.org/download/{id}.cif` — all coordinate geometry, via
  evaluation-side `allo.groundtruth.structures.fetch_mmcif`.
- `GET https://www.ebi.ac.uk/europepmc/webservices/rest/search` — depositing-paper abstracts
  (NCBI eutils is robots-blocked; see the memory note on literature fetch routes).

Geometry code paths: `allo.groundtruth.structures.parse_mmcif` / `allo.structure.pdb.contacts`;
`allo.groundtruth.labels.align_numbering` / `.transfer_labels`; Kabsch superposition with 20 %
trim written for this sweep. Cutoff 4.5 Å throughout, matching `docs/targets.md`.
