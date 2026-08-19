# Target prior art — what the literature actually says about the three pockets

Status: evidence document, Phase 0/1. Compiled 2026-08-20.
Scope: the three scored targets in `CHALLENGE.md` §6 Table 1 — KRAS G12C, BCR-ABL1,
cardiac myosin. c-Myc (`1NKP`) is out of scope here; it has no characterised pocket.

**Purpose.** `CHALLENGE.md` assigns fixed apo/holo PDB pairs. This document establishes,
independently of the challenge, what the primary literature says each pocket is and which
structures characterise it, so that the challenge's assignments can be judged rather than
assumed. It is a _literature_ audit. A parallel _structural_ audit of the deposited files
should confirm or contradict every "expected file content" note flagged below.

---

## How to read this document (evidence conventions)

Per `AGENTS.md` R3 and the working agreement:

| Marker           | Meaning                                                                                                                                                           |
| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **[asserted]**   | The cited source states this. Quotation or close paraphrase.                                                                                                      |
| **[derived]**    | Read directly out of a machine-readable RCSB record (entry page, `data.rcsb.org` REST, `search.rcsb.org` REST, or the PDB header file). The record is the source. |
| **[inferred]**   | My reasoning over cited facts. Not stated by any source. Treat as a hypothesis.                                                                                   |
| **[unverified]** | I could not retrieve the primary source. States what would resolve it.                                                                                            |

No PDB ID, residue number or numeric value in this document comes from recall. Every one
was retrieved during this review from the source named beside it. Where a residue list
appears, it is reproduced _as the paper states it_ and is **not** to be used as ground
truth — ground truth comes from `src/allo/groundtruth/` operating on the holo file
(`docs/targets.md`, "Ground-truth policy").

### Search strings used (for reproducibility)

RCSB REST/search API:

- `https://data.rcsb.org/rest/v1/core/entry/{ID}` and `/core/polymer_entity/{ID}/1` for
  4OBE, 6OIM, 1OPL, 1OPJ, 5MO4, 8QYR, 9GZ2
- `https://files.rcsb.org/header/1OPL.pdb` (HET / SEQADV / COMPND records)
- Search service, `rcsb_primary_citation.pdbx_database_id_DOI exact_match` on:
  `10.1038/nature21702`, `10.1021/acs.jmedchem.8b01040`, `10.1038/s41586-019-1694-1`,
  `10.1073/pnas.1404639111`
- Search service, `rcsb_chem_comp_container_identifiers.comp_id exact_match` on `XB2`,
  `MOV`; `in ["AY7","FYW"]`
- Ligand pages `https://www.rcsb.org/ligand/{XB2,MOV,AY7,FYW}`

NCBI E-utilities:

- `esearch db=pubmed term=KRAS AND "switch-II pocket" AND (cryptic OR prediction OR "molecular dynamics")` → 17 PMIDs
- `esearch db=pubmed term=Skora AND Jahnke AND Grzesiek AND Abelson` → 24191057
- `esearch db=pubmed term=mavacamten AND ("super relaxed" OR "super-relaxed") AND Anderson` → 30104387
- `esearch db=pubmed term="aad3456" OR (Green AND Wakimoto AND mavacamten)` → 26912705
- `esearch db=pubmed term=Zheng[Author] AND "Predicting allosteric sites" AND "normal modes"` → 37003737
- `esummary`/`efetch db=pubmed rettype=abstract` on the PMID sets above
- PMC ID converter for 24191057, 30104387, 24256730, 12654251, 12654250, 28329763, 31666701

Web search (Semantic-Scholar-style discovery, then primary retrieval):

- `mavacamten crystal structure myosin PDB co-structure bound cryo-EM`
- `ABL1 isoform 1a 1b numbering offset 19 residues myristoyl pocket T315I T334I`
- `"myristoyl pocket" ABL1 lined residues "αE" "αF" "αH" "αI'" ...`
- `cryptic pocket prediction KRAS switch II pocket apo 4OBE molecular dynamics PocketMiner cryptosite`
- `Abl myristoyl pocket computational prediction allosteric site normal mode elastic network apo 1OPL`
- `myosin allosteric communication network analysis normal mode elastic network predict mavacamten omecamtiv pocket computational`
- `allosteric site prediction benchmark "myristoyl pocket" ABL kinase apo structure identify computational blind`

---

## A. KRAS G12C — the cryptic switch-II pocket (S-IIP)

### A.1 Discovery and definition

The S-IIP was discovered by **disulfide (tethering) fragment screening against
K-Ras(G12C)**, not by cavity detection on an apo structure. Ostrem JM, Peters U, Sos ML,
Wells JA, Shokat KM. _K-Ras(G12C) inhibitors allosterically control GTP affinity and
effector interactions._ Nature 2013;503:548–551. doi:10.1038/nature12796. PMID 24256730.
PMC4274051.

Location, **[asserted]** verbatim from that paper:

> "The S-IIP is located between the central β-sheet of Ras, and the α2-(switch-II) and
> α3-helices" (Extended Data Fig. 2a)

and the compounds extend "from Cys 12 into an adjacent pocket composed largely of
switch-II". In the active (GTP) state, "residues from switch-II entirely fill the S-IIP"
(Fig. 2d) — i.e. the pocket is _occupied by protein_ in the active conformation, and only
exists when switch-II is displaced.

### A.2 Is it genuinely cryptic?

Yes, on the paper's own evidence. **[asserted]**, Ostrem 2013, verbatim:

> "This fully formed pocket is not apparent in other published structures of Ras, although
> a groove is visible in some cases" (main text, cf. Extended Data Fig. 1b)

> "The S-IIP is not visible in other structures of Ras, and thus it is probably highly
> dynamic when GDP is bound" (Discussion)

So the literature's own position is: **a groove exists in some GDP structures; the fully
formed pocket does not.** This is the single most important sentence in the KRAS section
for our purposes — it means a topology-only method is being asked to score a region that
is a shallow surface groove in the input, and it also means the _degree_ of pocket opening
in the specific apo file we use is an empirical question for the structural audit, not a
literature fact.

Quantification of pocket opening by simulation: Vithani N, Zhang S, Thompson JP, et al.
_Exploration of Cryptic Pockets Using Enhanced Sampling Along Normal Modes: A Case Study of
KRAS(G12D)._ J Chem Inf Model 2024;64:8258–8273. doi:10.1021/acs.jcim.4c01435. PMID 39419500. **[asserted]** They ran >400 μs of weighted-ensemble MD using inherent normal
modes as progress coordinates on wild-type KRAS and G12D, with cosolvents, and report
recovery of known cryptic sites plus analysis of conformational-selection vs induced-fit.
**[unverified]** Their exact starting apo PDB ID: a figure caption retrieved via search
states "The crystal structure of the KRAS wild-type (WT):GDP complex (PDB ID: 4OBE)", but I
could not open the article body (ACS returned 403) or the ChemRxiv preprint (403). Opening
either would resolve it. If it holds, the field does use `4OBE` as _the_ WT KRAS:GDP
reference — which is a point in the challenge's favour for choice of file, though not for
choice of _genotype_ (see A.5).

### A.3 Nucleotide state — and why it matters to us

**[asserted]** Ostrem 2013:

- "Binding of these inhibitors to K-Ras(G12C) disrupts both switch-I and switch-II,
  subverting the native nucleotide preference to favour GDP over GTP" (abstract);
  quantitatively, relative GTP/GDP affinity shifts of 3.9 ± 0.6 (cmpd 8) and 3.5 ± 0.8
  (cmpd 12), Fig. 3b,c.
- "Pre-loading of K-Ras with GTP significantly impairs modification by both compounds,
  indicating incompatibility between compound binding and the active conformation of Ras."

**The pocket is targetable only in the GDP (inactive) state.** In the GTP state switch-II
fills the volume.

Consequence for us **[inferred]**: any apo input we use must be the **GDP-bound** form, and
the nucleotide is not incidental — it selects the conformational state that makes the
pocket exist at all. Under C5 the nucleotide may be modelled as a simple node or dropped;
dropping it entirely removes the only structural marker of the state the pocket depends on.
This deserves an ADR, not a default.

### A.4 Residues the literature names

Reproduced **as the papers state them**. We re-derive our labels computationally.

| Residues                                                                                                | What the source says they are                                                                                                                                 | Source                                                                                                                                                                                                                            |
| ------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Glu 99, Gly 60                                                                                          | "Glu 99 and Gly 60 form direct hydrogen bonds to 6" (Fig. 1f); compounds "occupy the required position for Gly 60 in the active conformation" and displace it | Ostrem 2013, doi:10.1038/nature12796 **[asserted]**                                                                                                                                                                               |
| switch-II (α2) as a block                                                                               | "In the active state of Ras, residues from switch-II entirely fill the S-IIP" (Fig. 2d)                                                                       | Ostrem 2013 **[asserted]**                                                                                                                                                                                                        |
| His95 / Tyr96 / Gln99                                                                                   | "a cryptic pocket (H95/Y96/Q99)" exploited to reach clinical potency — the "H95 groove" that AMG 510 occupies in addition to the S-IIP proper                 | Lanman BA, et al. _Discovery of a Covalent Inhibitor of KRAS(G12C) (AMG 510) for the Treatment of Solid Tumors._ J Med Chem 2020;63:52–65. doi:10.1021/acs.jmedchem.9b01180 **[asserted, abstract-level — full text not opened]** |
| p2 pocket: residues 61–65 and 90–99, "between helices α2 and α3 at the interface between the two lobes" | a _predicted_ pocket, published two years before Ostrem                                                                                                       | Grant BJ, et al. PLoS One 2011;6:e25711. doi:10.1371/journal.pone.0025711. PMID 22046245 **[asserted]** — see §D                                                                                                                  |

Note the convergence: Grant's predicted p2 (61–65, 90–99) brackets both Ostrem's Gly60/
Glu99 and Lanman's H95/Y96/Q99. That is a strong signal that this region is reachable by
topology/dynamics-based methods.

Canon J, Rex K, Saiki AY, et al. _The clinical KRAS(G12C) inhibitor AMG 510 drives
anti-tumour immunity._ Nature 2019;575:217–223. doi:10.1038/s41586-019-1694-1. PMID 31666701. **[asserted]** The abstract (retrieved in full) describes "novel binding
interactions to markedly enhance their potency and selectivity" but **names no residues**.
The residue-level account of the AMG 510 site is in the companion med-chem paper (Lanman
2020), not in the Nature paper the challenge cites.

### A.5 Covalent warhead chemistry, and what it implies

**[asserted]** Ostrem 2013: compound 6 forms a **disulfide** to Cys 12 ("Well-defined
electron density … confirms the disulphide linkage between 6 and Cys 12", Fig. 1e); later
compounds use **acrylamides and vinyl sulfonamides** for irreversible C–S bond formation.
AMG 510 is likewise covalently bound in `6OIM` **[derived]** — RCSB reports MOV as the
"bound form" of AMG 510, and the MOV ligand page lists 7 entries with "covalent linkages to
polymer".

Implication for pocket definition **[inferred]**: the ligand is _anchored_ at Cys12, which
sits at the **P-loop / nucleotide site**, and reaches from there into the S-IIP. A naive
4.5 Å contact shell around the ligand therefore returns a residue set that **spans the
active site and the allosteric pocket**. If our active-site source residues are defined
from the nucleotide pocket, we will be scoring a label set that partially overlaps the
propagation source — inflating apparent performance. The ground-truth builder must handle
the covalent link explicitly (already flagged in `docs/targets.md`), and we should consider
reporting metrics both with and without the Cys12-proximal residues.

### A.6 The canonical structures

**Reference apo, per the literature.** Two entries from the same paper, same lab, same
crystallisation programme — Hunter JC, Gurbani D, Ficarro SB, et al. _In situ selectivity
profiling and crystal structure of SML-8-73-1, an active site inhibitor of oncogenic K-Ras
G12C._ Proc Natl Acad Sci USA 2014;111:8895–8900. doi:10.1073/pnas.1404639111. PMID 24889603. The DOI search on RCSB returns exactly three entries: `4LDJ`, `4NMM`, `4OBE`
**[derived]**.

|                                                    | `4OBE`                                           | `4LDJ`                                                                        |
| -------------------------------------------------- | ------------------------------------------------ | ----------------------------------------------------------------------------- |
| Title **[derived]**                                | "Crystal Structure of GDP-bound Human KRas"      | "Crystal Structure of a GDP-bound G12C Oncogenic Mutant of Human GTPase KRas" |
| Mutations **[derived]**                            | none (`rcsb_mutation_count` = 0; UniProt P01116) | 1 — G12C                                                                      |
| Resolution **[derived]**                           | 1.24 Å                                           | 1.15 Å                                                                        |
| Ligands **[derived]**                              | GDP, MG                                          | GDP, MG                                                                       |
| Residue 12 in the deposited sequence **[derived]** | **Gly** (`GMTEYKLVVVGAGGVGKS…`)                  | Cys (per the mutation record)                                                 |

**Discrepancy 1 (KRAS).** The challenge's apo input `4OBE` is **wild-type KRAS**, not
KRAS G12C. `4LDJ` — same paper, same nucleotide state, _better_ resolution — is the
G12C apo structure. Since the entire pocket concept is defined by the G12C cysteine
(the tethering anchor, the covalent warhead target, and the reason the pocket was ever
found), predicting "the KRAS G12C S-IIP" from a structure that has a glycine at position
12 is at minimum a documentation error in the challenge. **[inferred]** For a pure
topology/elastic-network method the Gly→Cys substitution changes one side chain and is
unlikely to move the ranking much; the correctness argument is about provenance and about
what we can claim, not about a large expected numeric effect. Recommended action: run
`4OBE` as the challenge specifies (it is the scored input), and run `4LDJ` as a documented
sensitivity check. Both, reported.

**Reference holo.** `6OIM` **[derived]**: "Crystal Structure of human KRAS G12C covalently
bound to AMG 510", X-ray 1.65 Å, ligands **MOV** (AMG 510/sotorasib, bound form) + GDP +
MG; primary citation Canon 2019. It is the _only_ entry RCSB returns for that DOI
**[derived]**. Mutations recorded: **C51S, C80L, C118S** plus G12C — the deposited sequence
is `MKHHHHHHHDEVDGMTEYKLVVVGACGVGKSALTIQL…`, i.e. an **N-terminally His-tagged, cysteine-
light construct** **[derived]**.

Other sotorasib-containing entries (chem comp MOV), 7 total **[derived]**: `6OIM`, `8G47`,
`8TLR`, `8UDR`, `8VR9`, `8VRA`, `8VRB`.

Ostrem 2013 deposited 11 structures **[asserted]**, from PMC4274051: `4LV6`, `4LUC`,
`4M1O`, `4LYF`, `4LYH`, `4LYJ`, `4M21`, `4M1S`, `4M1T`, `4M1Y`, `4M22`. Spot-check
**[derived]**: `4LUC` = "Crystal Structure of small molecule disulfide 6 bound to K-Ras
G12C", 1.29 Å, ligands GDP + 20G + CA, 4 mutations.

### A.7 Expected file-level disagreements (for the structural audit)

1. **`4OBE` sequence at position 12 must be GLY.** If the audit finds CYS, one of us is
   wrong and this document is the one to fix.
2. **Residue numbering offset in `6OIM`.** The entity carries a 14-residue N-terminal tag
   (`MKHHHHHHHDEVDG`) ahead of the KRAS Met1. Whether `auth_seq_id` restarts KRAS at 1 is
   not determinable from the records I pulled. `docs/targets.md` already mandates
   sequence-alignment-based mapping rather than assuming numbering matches; this is the
   concrete case that justifies it. **[unverified]**
3. **`6OIM` has 3 engineered Cys→X substitutions** absent from `4OBE`. Sequence alignment
   must not silently treat those as unmapped.
4. **Covalent MOV–Cys12 linkage.** Contact selection must not double-count or drop the
   linked atoms.

### A.8 What this implies for our benchmark

The KRAS assignment is the _soundest_ of the three, and the pocket is a genuine cryptic
site with a clean cited definition (between the central β-sheet and the α2/α3 helices) that
an elastic-network method can plausibly reach — Grant et al. reached it in 2011 by MD +
ensemble docking. Two caveats govern how we report: (i) the apo file is wild-type, so every
claim must say "wild-type KRAS:GDP (`4OBE`)" and not "KRAS G12C apo"; (ii) the holo ligand
is covalently anchored at the active site, so the raw contact-shell label set is
contaminated by active-site residues and we must report the enrichment statistic both with
and without them.

---

## B. BCR-ABL1 — the myristoyl pocket

### B.1 The pocket and the autoinhibition mechanism

Two back-to-back 2003 _Cell_ papers define it:

- Nagar B, Hantschel O, Young MA, Scheffzek K, Veach D, Bornmann W, Clarkson B,
  Superti-Furga G, Kuriyan J. _Structural basis for the autoinhibition of c-Abl tyrosine
  kinase._ Cell 2003;112:859–871. doi:10.1016/S0092-8674(03)00194-6. PMID 12654251.
- Hantschel O, Nagar B, Guettler S, Kretzschmar J, Dorey K, Kuriyan J, Superti-Furga G.
  _A myristoyl/phosphotyrosine switch regulates c-Abl._ Cell 2003;112:845–857.
  doi:10.1016/S0092-8674(03)00191-0. PMID 12654250.

**[asserted]** Nagar 2003: "the N-terminal myristoyl modification of c-Abl 1b binds to the
kinase domain and induces conformational changes that allow the SH2 and SH3 domains to dock
onto it. Autoinhibited c-Abl forms an assembly strikingly similar to that of inactive Src
kinases." **[asserted]** Hantschel 2003: the myristoyl engages "a hydrophobic pocket in the
kinase domain, which induces a kink in the kinase C-terminal αI helix, and this kinked
conformation of the helix enables docking of the SH2 domain to the kinase C-lobe and
consequently kinase inhibition."

So the mechanism is: **myristate in → αI kinks (αI/αI′) → SH2 docks on the C-lobe → kinase
off.** BCR-ABL1 loses the myristoylated N-cap in the fusion, hence constitutive activity;
asciminib restores the "off" assembly by occupying the vacated pocket.

Wylie AA, Schoepfer J, Jahnke W, Cowan-Jacob SW, Loo A, Furet P, et al. _The allosteric
inhibitor ABL001 enables dual targeting of BCR–ABL1._ Nature 2017;543:733–737.
doi:10.1038/nature21702. PMID 28329763. **[asserted]**, abstract verbatim: "ABL001 binds to
the myristoyl pocket of ABL1 and induces the formation of an inactive kinase conformation."

### B.2 **Does `1OPL` contain a myristoyl group? Yes — in chain A only.**

**[derived]**, from `https://files.rcsb.org/header/1OPL.pdb`:

```
COMPND  MOLECULE: PROTO-ONCOGENE TYROSINE-PROTEIN KINASE; CHAIN: A, B;
        FRAGMENT: N-TERMINAL 531 RESIDUES (MYR-SH3-SH2-KINASE DOMAIN);
        ENGINEERED: YES; MUTATION: YES
HET     MYR  A 538      15
HET     P16  A 539      29
HET     P16  B 538      29
HETNAM  MYR MYRISTIC ACID
HETNAM  P16 6-(2,6-DICHLOROPHENYL)-2-{[3-(HYDROXYMETHYL)PHENYL]AMINO}-
            8-METHYLPYRIDO[2,3-D]PYRIMIDIN-7(8H)-ONE
SEQADV  ARG A 29 (LYS→ARG); ASP A 30 (GLU→ASP); ASN A 382 (ASP→ASN)   [same for chain B]
```

Entry facts **[derived]**: X-ray, **3.42 Å**, 2 chains, 816 deposited polymer residues,
UniProt P00519, primary citation Nagar 2003.

Three consequences, all material:

1. **The challenge's "apo" BCR-ABL1 input is not apo with respect to the pocket we are
   asked to predict.** Chain A's myristoyl pocket is occupied by myristate. This is the
   single largest constraint-C1-adjacent problem in the target set — not a holo-leakage
   violation in the letter of C1 (myristate is not the drug), but a violation in spirit:
   the input tells the algorithm where the pocket is, because the pocket is open and full.
2. **`1OPL` also contains an ATP-site inhibitor (P16 = PD166326) in both chains.** The
   "apo" structure carries two ligands, not zero. Under C5 both are excluded (or modelled
   as simple nodes) — but the _conformation_ they stabilise remains in the coordinates.
3. **Chain B has no myristate.** `HET MYR A 538` appears once. Chain B therefore is a
   copy of the same assembly with an unoccupied (or differently occupied) myristoyl pocket
   in the same crystal. **[inferred]** This is potentially a gift: chain B may be a
   defensible "myristate-free but autoinhibited" input, letting us keep `1OPL` as the file
   while removing the occupancy problem. Whether chain B's αI is kinked or straight, and
   whether the pocket is open there, is a **structural-audit question** — I found no
   literature statement about `1OPL` chain B specifically. **[unverified]** Resolving it:
   compute the cavity volume of the myristoyl pocket in chains A and B of `1OPL` and
   compare with `1OPK` (myristate-bound) and `1M52` (myristate-free).

Also from Nagar 2003 **[asserted]** (via the paper's data-availability statement, retrieved
through search): the three deposited entries are `1OPJ`, `1OPL`, `1OPK`.

| Entry  | Content **[derived from RCSB]**                                                                                                                        |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `1OPJ` | Mouse Abl (UniProt **P00520**), kinase domain, entity residues 7–293 aligned to reference **229–515**; 1.75 Å; ligands **MYR**, **STI** (imatinib), CL |
| `1OPK` | Mouse Abl, 495 residues (SH3-SH2-kinase); 1.80 Å; ligands **P16**, **MYR**, GOL                                                                        |
| `1OPL` | UniProt **P00519** (human), 2 chains, MYR-SH3-SH2-kinase; 3.42 Å; ligands **MYR** (chain A only), **P16** (both chains)                                |

**[derived]** `1OPJ` shows the myristoyl pocket occupied in an **isolated kinase domain**,
without SH3/SH2 — useful as a "pocket open, minimal construct" reference.

### B.3 The 1a / 1b numbering trap

**[asserted]** Paladini J, Maier A, Habazettl JM, Hertel I, Sonti R, Grzesiek S. _The
molecular basis of Abelson kinase regulation by its αI-helix._ eLife 2024;13:e92324.
doi:10.7554/eLife.92324: "Abl 1b being 19 residues longer and N-terminally myristoylated"
compared with variant 1a; "Abl 1b numbering used throughout".

**[asserted]** Blakes AJM, et al. _Pathogenic variants causing ABL1 malformation syndrome
cluster in a myristoyl-binding pocket and increase tyrosine kinase activity._ Eur J Hum
Genet 2021;29:593–603. doi:10.1038/s41431-020-00766-w. PMID 33223528: the longer isoform
"encodes 19 additional N-terminal residues involved in auto-inhibition"; their pocket
residues are numbered per **isoform 1b (NM_007313.2)**.

**[asserted]** de Buhr S, Gräter F. _Myristoyl's dual role in allosterically regulating and
localizing Abl kinase._ eLife 2023;12:e85216. doi:10.7554/eLife.85216: "1b isoform
numbering throughout this work".

**[asserted]** Skora L, Mestan J, Fabbro D, Jahnke W, Grzesiek S. PNAS 2013;110:E4437–E4445.
doi:10.1073/pnas.1314712110. PMID 24191057: construct "c-Abl83–534 (Abl 1b numbering)".

**Offset = +19 going from 1a to 1b.** The canonical worked example, **[asserted]** via
search of the CML literature: the gatekeeper mutation **T315I (1a) = T334I (1b)**.

Confirmation from the deposited files **[derived]**:

- `5MO4` mutations are recorded as **T334I** and **D382N** → 1b numbering.
- `1OPL` SEQADV records **ASN A 382 (ASP→ASN)** → same convention, 1b numbering.
  (D382 in 1b = D363 in 1a = the catalytic-loop HRD aspartate; the mutation is the standard
  kinase-dead substitution. **[inferred]** from the offset, not stated by a source.)
- `5MO4` polymer entity aligns entity residues 7–495 to **UniProt P00519 residues 27–515**
  **[derived]**. P00519 canonical is the 1b sequence.

**Where the trap bites.** The clinical/resistance literature is largely in **1a**; the
structures and the biophysics are in **1b**. Asciminib resistance mutations are usually
written **A337V, P465S, V468F** (1a) — which are **A356V, P484S, V487F** in 1b, i.e. the
same residues Blakes and the pocket-lining lists name **[inferred, arithmetic on the stated
+19 offset]**. Any list of "myristoyl pocket residues" copied from a review without checking
its convention will be wrong by 19.

### B.4 Residues the literature names as lining the pocket

All in **1b numbering** unless stated. Again — reproduced as stated, not to be used as
labels.

| Residues                                                                                                                                                                                                                                  | Source                                                                                                                                                                                                                                                                                                                    | Marker                                                                                                                                                                                                                                         |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Ala356, Ala452, Val525, Glu528** — "form important hydrophobic interactions with the myristoyl group and to other amino acids that complete the binding pocket"; the four residues at which ABL1-malformation-syndrome variants cluster | Blakes 2021, doi:10.1038/s41431-020-00766-w (used PDB `1OPL`, Fig. 3)                                                                                                                                                                                                                                                     | **[asserted]**                                                                                                                                                                                                                                 |
| **I521, V525, L529** — hydrophobic residues contacting myristoyl in the kinked αI conformation; "solvent exposed in the straight conformation"                                                                                            | de Buhr & Gräter 2023, doi:10.7554/eLife.85216                                                                                                                                                                                                                                                                            | **[asserted]**                                                                                                                                                                                                                                 |
| **F516, Q517, S520, D523** — stabilise the bound myristoyl; αI = residues 504–515, αI′ = 520–531, joined by the αI–αI′ loop                                                                                                               | Paladini 2024, doi:10.7554/eLife.92324                                                                                                                                                                                                                                                                                    | **[asserted]**                                                                                                                                                                                                                                 |
| αE **A356, L359, L360**; αF **L448, A452, Y454**; αH **C483, P484, V487**; induced αI′ **I521, V525, L529** — full pocket lining; asciminib additionally contacts R351, A363, F512                                                        | Retrieved as an aggregated passage; the underlying source is most likely Roskoski R Jr. _Targeting BCR-Abl in the treatment of Philadelphia-chromosome positive chronic myelogenous leukemia._ Pharmacol Res 2022;178:106156. doi:10.1016/j.phrs.2022.106156. PMID 35257901 — **I could not open it** (ScienceDirect 403) | **[unverified attribution]** — the residue list is internally consistent with the three verified sources above and with the +19 offset; the citation is not confirmed. Resolving it: open Roskoski 2022 §"asciminib" or Schoepfer 2018 Fig. 3. |

Also **[asserted]**, Roskoski 2022 (via abstract-level search): asciminib "interact[s] with
the myristate-binding site located **23 Å from the ATP-binding site**" and "is the prototype
of a type IV inhibitor". That 23 Å figure is a useful sanity check on any distance-based
"distal site" definition we adopt.

### B.5 Is the myristoyl pocket cryptic, or a permanent cavity?

**Conformationally gated, not permanent.** The evidence:

**[asserted]** Skora 2013 (PNAS, doi:10.1073/pnas.1314712110): "In the absence of myristoyl
pocket ligands, the C-terminal helix αI of the isolated kinase is straight in crystals and
partially flexible in solution," and that "straight helix αI … would clash with the SH2
domain in the closed SH3-SH2–kinase conformation."

**[asserted]** de Buhr & Gräter 2023: crystal structures without myristoyl "show the helix
in a straight conformation", and the pocket-lining hydrophobics I521/V525/L529 "are solvent
exposed in the straight conformation".

**[asserted]** Paladini 2024: the pocket requires conformational change rather than being
pre-formed; myristoyl-induced αI bending is what stabilises the autoinhibited assembly.

The reference **myristate-free** structure the field uses for the straight-αI state is
`1M52` **[asserted]** (Paladini 2024 cites it as "isolated kinase domain, straight αI-helix").
`1M52` **[derived]**: "Crystal Structure of the c-Abl Kinase domain in complex with
PD173955", mouse, 2.60 Å, ligands **P17**, MES — **no MYR**; Nagar B, et al. Cancer Res
2002;62:4236–4243, PMID 12154025.

**[inferred]** So the honest characterisation is: the myristoyl pocket is a **hydrophobic
cleft at the base of the kinase C-lobe whose _floor_ exists in all structures but whose
_enclosure_ requires the αI→αI′ transition**. It is "cryptic" in the same operational sense
as the S-IIP — closed in the ligand-free crystal form — but the closing mechanism is a
helix rearrangement rather than a loop displacement.

### B.6 The canonical structures

| Role                                               | Entry  | Content **[derived]**                                                                                  | Citation                                                                                                                                                                                |
| -------------------------------------------------- | ------ | ------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Myristoyl-**bound**, autoinhibited assembly, human | `1OPL` | MYR (chain A) + P16, 3.42 Å, MYR-SH3-SH2-kinase, 2 chains                                              | Nagar 2003, doi:10.1016/S0092-8674(03)00194-6                                                                                                                                           |
| Myristoyl-bound, assembly, mouse, high res         | `1OPK` | P16 + MYR + GOL, 1.80 Å, 495 res                                                                       | Nagar 2003                                                                                                                                                                              |
| Myristoyl-bound, **isolated kinase domain**        | `1OPJ` | MYR + STI + CL, 1.75 Å, P00520 res 229–515                                                             | Nagar 2003                                                                                                                                                                              |
| Myristoyl-bound, human 1b core, best res           | `2FO0` | P16 + MYR + GOL + SEP, 2.27 Å, human, "1B isoform"                                                     | Nagar B, et al. _Organization of the SH3-SH2 unit in active and inactive forms of the c-Abl tyrosine kinase._ Mol Cell 2006;21:787–798. doi:10.1016/j.molcel.2006.01.035. PMID 16543148 |
| Myristoyl-**free**, straight αI                    | `1M52` | P17 + MES, 2.60 Å, **no MYR**                                                                          | Nagar 2002, PMID 12154025                                                                                                                                                               |
| **Asciminib-bound** (the holo the challenge names) | `5MO4` | **AY7** (asciminib) + **NIL** (nilotinib), 2.17 Å, human, P00519 res 27–515, T334I + D382N, **no MYR** | Wylie 2017, doi:10.1038/nature21702                                                                                                                                                     |
| Asciminib-bound, second independent entry          | `8SSN` | **AY7** + **SKI**, 2.86 Å, human ABL1, 448 res                                                         | Kim C, Ludewig H, Hadzipasic A, et al. _A biophysical framework for double-drugging kinases._ PNAS 2023;120:e2304611120. doi:10.1073/pnas.2304611120. PMID 37590418                     |
| Earlier allosteric myristate-site ligand (GNF-2)   | `3K5V` | STI + **STJ** (GNF-2) + CL, 1.74 Å, mouse                                                              | Zhang J, et al. _Targeting Bcr-Abl by combining allosteric with ATP-binding-site inhibitors._ Nature 2010;463:501–506. doi:10.1038/nature08675. PMID 20072125                           |

**Discrepancy 2 (BCR-ABL1), and a correction to our own notes.** `5MO4` is **not** a
kinase-domain-only construct. `docs/targets.md` currently states "`5MO4` (kinase domain
only)". The RCSB polymer entity aligns it to **P00519 residues 27–515** — N-cap remnant +
SH3 + SH2 + kinase — the same architecture as `1OPL` **[derived]**. That is good news for
the alignment step (domain content largely matches) and `docs/targets.md` should be
corrected.

**Discrepancy 3 (BCR-ABL1) — asciminib is not in the Schoepfer structures.** The challenge
cites Schoepfer 2018 (doi:10.1021/acs.jmedchem.8b01040, PMID 30137981) as a reference for
asciminib. The two entries deposited with that paper are `6HD4` and `6HD6` **[derived, DOI
search]**, both mouse ABL1, 293 residues, with imatinib (**STI**) plus, respectively,
**FYW** and **FYH**. Neither ligand is asciminib: the asciminib chem-comp is **AY7**
(`N-[4-[chloro-difluoromethoxy]phenyl]-6-[(3R)-3-hydroxypyrrolidin-1-yl]-5-(1H-pyrazol-5-yl)
pyridine-3-carboxamide`, C20H18ClF2N5O3, RCSB→DrugBank mapped to asciminib/Scemblix),
whereas **FYW** is `6-[(3R)-3-hydroxypyrrolidin-1-yl]-5-pyrimidin-5-yl-N-[4-(trifluoro-
methoxy)phenyl]pyridine-3-carboxamide`, C21H18F3N5O3 — a different compound in the same
series **[derived from the ligand pages]**. A comp-ID search for `AY7` returns exactly
**two** entries: `5MO4` and `8SSN` **[derived]**. Anyone extracting "the asciminib pocket"
from `6HD4` would be extracting a close analogue's pocket. `5MO4` is the right file.

### B.7 Expected file-level disagreements (for the structural audit)

1. **`1OPL` chain A has MYR at residue 538; chain B does not.** Confirm, and decide the
   chain policy. This is the highest-value audit item in the whole target set.
2. **`1OPL` also contains P16 in both chains.** Our "apo" input is a two-ligand structure.
3. **`1OPL` is 3.42 Å** — low resolution for a contact-network build. 816 polymer residues
   deposited across two chains for a construct described as "N-terminal 531 residues", so
   expect substantial disorder/gaps. `1OPK` (1.80 Å) and `2FO0` (2.27 Å) are the
   high-resolution alternatives, at the cost of species (mouse) and of `2FO0` carrying a
   phosphoserine.
4. **Numbering.** Both `1OPL` and `5MO4` should be 1b. Verify `auth_seq_id` ranges; do not
   assume.
5. **Domain-content mismatch is smaller than we assumed** — verify `5MO4`'s _modelled_
   (not merely deposited) residue range; 429 of 495 entity residues are modelled
   **[derived]**, so some of SH3/SH2 may be missing.

### B.8 What this implies for our benchmark

This target is where the challenge's design is weakest and our documentation burden is
highest. The prediction is only blind if the myristate is removed _and_ we can show the
resulting network does not still encode an open pocket. Three defensible options, in
increasing order of cost:

- (a) Use `1OPL` chain A with MYR and P16 stripped per C5, and **report the pocket volume
  before and after stripping** so the reader can judge how much was given away.
- (b) Use `1OPL` **chain B**, if the audit shows it is myristate-free — same file, same
  citation, no occupancy problem.
- (c) Add `1M52` (straight αI, no myristate) as a genuinely closed-pocket control input and
  report whether the method still ranks the myristoyl-pocket residues highly. This is the
  strongest scientific result available on this target: succeeding on `1M52` would be a
  real cryptic-pocket prediction, not a cavity-detection exercise.

Whatever we choose, the report must state that `1OPL` as deposited contains myristate.
Silence on that point would be the kind of thing a referee finds.

---

## C. Cardiac myosin — the mavacamten site

### C.1 **Does any PDB structure contain mavacamten? Yes — exactly six.**

Mavacamten's chemical component ID is **XB2** **[derived]**. A comp-ID search returns
`total_count: 6` **[derived]**:

| Entry  | Content                                                                                                                       | Method / res.       | Species                                              | Citation           |
| ------ | ----------------------------------------------------------------------------------------------------------------------------- | ------------------- | ---------------------------------------------------- | ------------------ |
| `8QYQ` | "Beta-cardiac myosin S1 fragment in the pre-powerstroke state complexed to Mavacamten"; XB2, ADP, **BEF**, MG, GOL, FMT       | X-ray, **2.61 Å**   | _Bos taurus_ (MYH7 Q9BE39 + MYL3)                    | Auguin 2024        |
| `8QYR` | "Beta-cardiac myosin motor domain in the pre-powerstroke state complexed to Mavacamten"; XB2, ADP, SO4, **BEF**, EDO, MG, M3L | X-ray, **1.80 Å**   | _Bos taurus_                                         | Auguin 2024        |
| `9GZ1` | "Beta-cardiac myosin interacting heads motif complexed to mavacamten"; XB2, ADP, PO4, MG                                      | cryo-EM, **3.70 Å** | _H. sapiens_ MYH7 + mouse light chains               | McMillan 2025/2026 |
| `9GZ2` | "Beta-cardiac heavy meromyosin motor domain in the primed state complexed to mavacamten"; XB2, ADP, PO4, MG                   | cryo-EM, **2.90 Å** | _H. sapiens_ MYH7 (P12883)                           | McMillan 2025/2026 |
| `9YP9` | "…human beta-cardiac myosin bound to mavacamten in the interacting-heads motif and **S2-FH docked** state"; XB2, ADP, PO4     | cryo-EM, **3.00 Å** | _H. sapiens_ (GCN4/eGFP-tagged) + mouse light chains | Somavarapu 2026    |
| `9YR7` | "…in the interacting-heads motif and **S2-FH undocked** state"; XB2, ADP, PO4                                                 | cryo-EM, **3.00 Å** | _H. sapiens_ + mouse light chains                    | Somavarapu 2026    |

Citations **[derived from RCSB primary-citation records, cross-checked against PubMed]**:

- Auguin D, Robert-Paganin J, Réty S, Kikuti C, David A, Theumer G, Schmidt AW, Knölker HJ,
  Houdusse A. _Omecamtiv mecarbil and Mavacamten target the same myosin pocket despite
  opposite effects in heart contraction._ Nat Commun 2024;15:4885.
  doi:10.1038/s41467-024-47587-9. PMID 38849353. (Preprint: bioRxiv
  doi:10.1101/2023.11.15.567213, PMID 38014327.)
- McMillan SN, Pitts JRT, Barua B, Winkelmann DA, Scarff CA. _Mavacamten inhibits myosin
  activity by stabilising the myosin interacting-heads motif and stalling motor force
  generation._ bioRxiv doi:10.1101/2025.02.12.637875, PMID 39990378 — RCSB's primary
  citation for `9GZ1`/`9GZ2`. **[asserted, search-level]** Published version: Science
  Advances, doi:10.1126/sciadv.aea9335 (listed on science.org; I could not open it, 403).
- Somavarapu AK, et al. _Cryo-EM reveals how cardiomyopathy therapeutic drugs modulate the
  myosin motors of the heart._ Science Advances 2026;12:eaed6472. doi:10.1126/sciadv.aed6472.
  PMID 42054467.

**The first mavacamten co-structures are the Auguin bovine X-ray structures, deposited
2023-10-26 and released 2023-12-13 [derived].** Everything published before that — including
both papers the challenge cites — predates any mavacamten co-structure.

### C.2 **Does `6C1H` contain mavacamten? No. It is not even cardiac myosin.**

**[derived]**, RCSB entry `6C1H`:

- Title: "High-Resolution Cryo-EM Structures of Actin-bound Myosin States Reveal the
  Mechanism of Myosin Force Sensing"
- Method: cryo-EM, **3.90 Å**; deposited 2018-01-04
- Macromolecules: **Actin, alpha skeletal muscle (_Oryctolagus cuniculus_)** +
  **Unconventional myosin-Ib (_Rattus norvegicus_)** + **Calmodulin**
- Ligands: **ADP, MG** — no XB2, no drug
- Primary citation: Mentes A, et al. _High-resolution cryo-EM structures of actin-bound
  myosin states reveal the mechanism of myosin force sensing._ Proc Natl Acad Sci USA
  2018;115:1292–1297. doi:10.1073/pnas.1718316115. PMID 29358376

**Discrepancy 4 (myosin) — and it is fatal to the challenge's myosin ground truth.**
`6C1H` is a **rat myosin-1b** (an unconventional class-I myosin) bound to **rabbit skeletal
actin** and calmodulin. It is not β-cardiac myosin (MYH7), not human, contains no
mavacamten, and contains no drug of any kind. It cannot serve as the holo validation
structure for "the mechanical site where mavacamten stabilizes the super-relaxed state".
There is no plausible reading of `6C1H` under which it does.

**[inferred]** The most likely origin of the error: `6C1H` was released 2018-01-31, in the
same window as the Anderson 2018 PNAS mavacamten paper, and both are PNAS myosin cryo-EM
work. Whatever the cause, the assignment is wrong on the file's own record.

### C.3 What is `5TBY`?

**[derived]**, RCSB: "HUMAN BETA CARDIAC HEAVY MEROMYOSIN INTERACTING-HEADS MOTIF OBTAINED
BY HOMOLOGY MODELING". Method recorded as Electron Microscopy, **resolution 20.0 Å**.
Chains: Myosin-7 A,B (1,935 residues each); Myosin light chain 3 C,D (195); Myosin
regulatory light chain 2 ventricular/cardiac E,F (166). Organism _Homo sapiens_.
**No non-polymer ligands** — no nucleotide, no Mg.

Primary citation: Alamo L, Ware JS, Pinto A, Gillilan RE, Seidman JG, Seidman CE, Padrón R.
_Effects of myosin variants on interacting-heads motif explain distinct hypertrophic and
dilated cardiomyopathy phenotypes._ eLife 2017;6:e24634. doi:10.7554/eLife.24634.
PMID 28606303.

**[asserted]**, from that paper's methods: `5TBY` is a **homology model**, not an
experimentally determined structure. The template is the **tarantula striated-muscle IHM
quasi-atomic cryo-EM structure, PDB `3JBH`**; human β-cardiac ELC, RLC and MHC (MD and S2)
were modelled onto it by sequence alignment. The model was then **rigid-body fitted to a
2.8 nm (28 Å) negative-stain 3D reconstruction of the human cardiac thick filament,
EMD-2240**, and cross-checked against SAXS ("the predicted SAXS profile of PDB 5TBY is
consistent with X-ray solution scattering of squid HMM").

**Discrepancy 5 (myosin).** The challenge's apo input for cardiac myosin is a
**20 Å homology model built on an arachnid template**. Side-chain positions in it are
_modelled_, not observed; inter-residue contacts at the 4.5–8 Å scale that an elastic
network depends on are template-derived, not experimental. **[inferred]** For an
elastic-network / contact-graph method this is less catastrophic than it sounds — the fold
and the domain packing are the signal, and those are constrained by the fit — but every
number we produce from `5TBY` inherits the model's assumptions, and the report must say so.
It also means `5TBY` cannot be used to make any claim about pocket geometry.

### C.4 What was known about the binding site _before_ a co-structure existed?

**Green EM, Wakimoto H, Anderson RL, et al.** _A small-molecule inhibitor of sarcomere
contractility suppresses hypertrophic cardiomyopathy in mice._ Science 2016;351:617–621.
doi:10.1126/science.aad3456. PMID 26912705. **[asserted]** The full abstract (retrieved)
identifies MYK-461 as reducing "the adenosine triphosphatase activity of the cardiac myosin
heavy chain" and reports the mouse phenotype. **It says nothing about a binding site.**

**Anderson RL, Trivedi DV, Sarkar SS, et al.** _Deciphering the super relaxed state of human
β-cardiac myosin and the mode of action of mavacamten from myosin molecules to muscle
fibers._ Proc Natl Acad Sci USA 2018;115:E8143–E8152. doi:10.1073/pnas.1809540115. PMID 30104387. PMC6126717. **[asserted]** from the full text:

- **No crystal or cryo-EM co-structure.** The paper explicitly leaves the question open —
  "How does this molecule affect the detailed structure of the myosin active site?" — and
  states "It is crucial now to obtain a high-resolution crystallographic or cryo-EM
  structure of the SRX folded-back state."
- The evidence is **functional/biochemical**: nucleotide-release kinetics (mavacamten
  "reduce[s] the basal release rates of ADP and Pi" by "holding the switch elements in a
  closed state"), single-turnover assays showing SRX stabilisation, and EM imaging with a
  cross-linkable analogue (MYK-3046).
- **No docking model, no mutagenesis mapping, no HDX-MS** is presented.
- Homology models MS03 and HBCprestrokeS1 are used, and **PDB `5TBY` is cited** from the
  Padrón laboratory for comparison.

So: as of 2018 the site was **unlocalised**; mavacamten was known to stabilise the IHM/SRX
state and to slow phosphate release, and the structural hypothesis was "somewhere that
stabilises the folded-back state". The `5TBY`↔Anderson-2018 link is presumably why the
challenge picked `5TBY`.

### C.5 Residues the literature names for the mavacamten site

From Auguin 2024 (Nat Commun 2024;15:4885, doi:10.1038/s41467-024-47587-9), **bovine
β-cardiac myosin numbering** **[asserted]**:

- Location: the pocket is "located between the N-terminal (N-term) and the Converter
  subdomains of the motor domain", positioned "between the Lever arm and the motor domain".
- Named contacts, by subdomain: **N-terminal Leu120, Asp168**; **Transducer Arg169,
  Tyr455** (and β1/β2 strands); **Relay His492, Glu497**; **Converter Asn711, Arg712,
  Asp717, Ala767**. The Arg712–Asp717 pair is highlighted as an electrostatic interaction
  the drugs modulate.
- **Omecamtiv mecarbil binds the same pocket** — that is the paper's headline result.

Numbering across species **[inferred, not asserted by any source I retrieved]**: human MYH7
(UniProt **P12883**) and bovine MYH7 (UniProt **Q9BE39**) are **both 1,935 residues**
**[derived from UniProt]**. Equal length is consistent with, but does not prove, a 1:1
residue correspondence in the motor domain. **[unverified]** Resolving it: pairwise-align
P12883 and Q9BE39 and confirm zero indels before residue 800. Do not transfer Auguin's
bovine numbers to a human structure until that alignment is run — and note separately that
`auth_seq_id` in `9GZ2` maps entity residue 1 to P12883 residue 2 **[derived]**, so even
the human entries may carry a ±1 offset.

I did **not** find a residue list stated in human numbering from a source I could open.
The McMillan and Somavarapu full texts (which would give human numbering) returned 403 from
bioRxiv and science.org. **[unverified]**

### C.6 Is the mavacamten site allosteric in our strict sense?

Yes. **[asserted]** Auguin 2024: "No differences are found in the active site, including in
the Switch-2 position"; the drugs act by altering "allosteric communication" and "motor
allostery" rather than by contacting catalytic residues; both drugs "stabilize a pre-stroke
structural state".

**The active site in this system is the ATPase (nucleotide) site** — P-loop, switch-1,
switch-2 — which in the co-structures is occupied by Mg·ADP·VO4 (`8QYP`, `8QYR` uses BeFx)
or Mg·ADP·Pi (`9GZ1`, `9GZ2`) **[derived from the ligand lists]**. The mavacamten pocket is
a distinct site between the N-terminal and Converter subdomains whose occupancy modulates
the ATPase cycle (Pi release, lever-arm priming). That is a textbook allosteric
relationship and is a good fit for our "dynamic connectivity to an active site" formulation
**[inferred]**.

Is it cryptic? **[asserted]** Auguin 2024 describe "a binding site that only forms in
states of the motor in which the Lever arm is primed", and "Closure of the allosteric
pocket around the drug results in a similar priming." So the site is **state-gated**: it
exists in the pre-powerstroke/primed state and closes around the ligand. That makes the
conformational state of our apo input decisive.

### C.7 The canonical structures — what the literature actually uses

| Role                                             | Entry                             | Content **[derived]**                                                                                                  | Citation                                                                                                                                                          |
| ------------------------------------------------ | --------------------------------- | ---------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Matched apo for the mavacamten pocket**        | `8QYP`                            | "Beta-cardiac myosin motor domain in the pre-powerstroke state"; ADP, **VO4**, MG, M3L; **no drug**; 2.76 Å            | Auguin 2024, doi:10.1038/s41467-024-47587-9                                                                                                                       |
| Holo, best resolution                            | `8QYR`                            | motor domain + **XB2**; 1.80 Å, bovine                                                                                 | Auguin 2024                                                                                                                                                       |
| Holo, S1 fragment (motor + lever + ELC)          | `8QYQ`                            | S1 + **XB2**; 2.61 Å, bovine                                                                                           | Auguin 2024                                                                                                                                                       |
| Same-pocket comparator (activator)               | `8QYU` (S1+OM, 1.96 Å) and `5N69` | OM-bound cardiac myosin                                                                                                | Auguin 2024; Planelles-Herrero VJ, Hartman JJ, Robert-Paganin J, Malik FI, Houdusse A. Nat Commun 2017;8:190. doi:10.1038/s41467-017-00176-5. PMID 28775348       |
| Apo bovine cardiac motor domain, PPS             | `5N6A`                            | ADP, PO4, GOL, MG; 3.10 Å; _Bos taurus_                                                                                | Planelles-Herrero 2017                                                                                                                                            |
| **Experimental** human β-cardiac IHM (drug-free) | `8ACT`                            | "Structure of the human beta-cardiac myosin folded-back off state"; ADP, PO4, MG; cryo-EM **3.60 Å**; all-human chains | Grinzato A, et al. _Cryo-EM structure of the folded-back state of human β-cardiac myosin._ Nat Commun 2023;14:3166. doi:10.1038/s41467-023-38698-w. PMID 37258552 |
| Human IHM **+ mavacamten**                       | `9GZ1`, `9YP9`, `9YR7`            | see C.1                                                                                                                | McMillan; Somavarapu                                                                                                                                              |
| The challenge's apo                              | `5TBY`                            | 20 Å homology model, no ligands                                                                                        | Alamo 2017, doi:10.7554/eLife.24634                                                                                                                               |
| The challenge's "holo"                           | `6C1H`                            | rat myosin-1b + rabbit actin + calmodulin, ADP only                                                                    | Mentes 2018, doi:10.1073/pnas.1718316115                                                                                                                          |

### C.8 Expected file-level disagreements (for the structural audit)

1. **`6C1H` must contain no XB2 and no MYH7 chain.** If the audit finds cardiac myosin in
   `6C1H`, this document is wrong. I expect it will find rat MYO1B + rabbit ACTA1 + CALM.
2. **`5TBY` must contain zero HETATM records** (no ADP, no Mg) and two 1,935-residue
   myosin-7 chains plus four light chains — a very large graph. `docs/targets.md` already
   flags the residue-count/coarse-graining issue; the count is roughly
   2×1935 + 2×195 + 2×166 ≈ 4,592 modelled residues **[inferred arithmetic from the
   deposited chain lengths]**. Confirm against the file.
3. **`5TBY` is a model** — expect ideal geometry, no B-factors of the usual kind, no gaps.
   A structure with no gaps and no ligands is itself a fingerprint of a model.
4. **Chain/species heterogeneity in `9GZ1`, `9YP9`, `9YR7`**: human heavy chain, **mouse**
   light chains **[derived]**; `9YP9`/`9YR7` also carry GCN4 and eGFP fusion tags
   **[derived]**. Any ground-truth extraction must restrict to the MYH7 chains.

### C.9 What this implies for our benchmark

The myosin target as specified is **unscoreable**: the holo structure contains no
mavacamten and no cardiac myosin, so no label set can be derived from it, and the apo
structure is a 20 Å homology model. Proposed remediation, in order of preference:

1. **Replace the pair with `8QYP` (apo) → `8QYR` (mavacamten).** Same paper, same species,
   same construct, same conformational state, 2.76 Å and 1.80 Å. This is the cleanest
   apo/holo pair in the entire target set — better than the KRAS pair — and it is a matched
   pair by construction, which removes the sequence-alignment risk almost entirely. Cost:
   bovine, not human; motor domain only, so the IHM/SRX narrative is lost.
2. **Human variant: `8ACT` (apo, experimental human IHM, 3.60 Å) → `9GZ1` or `9YP9`
   (mavacamten-bound human IHM).** Keeps species and the SRX story; costs resolution and
   introduces mouse light chains on the holo side.
3. **Keep `5TBY` as the scored input (it is what the challenge specifies) but derive labels
   from `8QYR`/`9GZ1` and map them onto `5TBY` by alignment.** This satisfies the letter of
   the challenge while producing a defensible label set. Requires the human/bovine alignment
   in C.5 to be run first.

Report all three if cheap; report (1) as the scientific result and (3) as the
challenge-compliant result. Either way the report must state plainly that `6C1H` contains
no mavacamten — that is a finding, and a referee will check it in thirty seconds.

---

## D. Prior art — has anyone predicted these pockets computationally from apo structures?

This is our real comparison set. Searched via the strings in the header; what follows is
what I could verify.

### D.1 KRAS S-IIP — yes, and one attempt predates the discovery

**Grant BJ, Lukman S, Hocker HJ, Sayyah J, Brown JH, McCammon JA, Gorfe AA.** _Novel
Allosteric Sites on Ras for Lead Generation._ PLoS One 2011;6:e25711.
doi:10.1371/journal.pone.0025711. PMID 22046245. **[asserted]**

- Method: crystallographic ensemble (seven representative structures) + 3 × 20 ns MD on
  K-Ras GTP and GDP (120 ns total) + FTMAP / AutoLigand / blind docking for site detection
  - Glide ensemble docking and rescoring. Structures named: `2PMX` (K-Ras, MD), `3GFT`
    (K-Ras, blind docking), plus H-Ras WT and G12V.
- Result: four non-nucleotide pockets. **p2** is "between helices α2 and α3 at the interface
  between the two lobes", residues **61–65, 90–99**; its accessibility is "modulated by
  helix α2 displacement", and "the large relative displacement of α2 between GDP- and
  GTP-like conformers effectively modulates the accessibility of these two pockets".
  Also p1 (residues 5–7, 39, 54–56, 67, 70–75), p3 ("the most distal non active site
  pocket… approximately 25 Å from the nucleotide-binding site"; residues 97, 101, 107–111,
  136–140, 161–166) and p3b.
- **[inferred]** p2 is the switch-II pocket by any reasonable reading: same secondary
  structure elements as Ostrem's definition (α2/α3 vs the central β-sheet), residue span
  covering Gly60/Glu99 (Ostrem) and H95/Y96/Q99 (Lanman). Published **two years before**
  Ostrem 2013. **This is the strongest existing demonstration that the S-IIP is reachable
  from apo Ras by dynamics-based methods, and it is our headline comparison point.**

**Vithani N, et al.** J Chem Inf Model 2024;64:8258–8273. doi:10.1021/acs.jcim.4c01435.
PMID 39419500. **[asserted]** Weighted-ensemble MD with **inherent normal modes as progress
coordinates**, >400 μs, cosolvents, WT KRAS and G12D; probe-occupancy mapping, exposon
analysis; reports predictive capacity for known cryptic sites and analyses conformational
selection vs induced fit using MRTX1133. **[unverified]** starting apo PDB (probably
`4OBE`, see A.2). Methodologically this is the closest classical analogue to what we are
doing — normal modes driving the sampling — and it costs 400 μs of MD, which is exactly the
cost the challenge claims quantum methods should undercut. **Use it as the classical
cost-comparison anchor.**

**Meller A, Ward M, Borowsky J, Kshirsagar M, Lotthammer JM, Oviedo F, Ferres JL, Bowman
GR.** _Predicting locations of cryptic pockets from single protein structures using the
PocketMiner graph neural network._ Nat Commun 2023;14:1177. doi:10.1038/s41467-023-36699-3.
PMID 36859488. **[asserted]** Graph neural network trained to predict where pockets open in
MD; **ROC-AUC 0.87** on a curated set of **39 experimentally confirmed cryptic pockets**,
">1,000-fold faster than existing methods". **[unverified]** whether KRAS is in the 39-pocket
set — search results assert KRAS is among the validation examples but I could not open the
supplementary list. Resolving it: the dataset is on the paper's GitHub/Zenodo. **This is the
single most important baseline number in the document**: 0.87 ROC-AUC from a _single static
structure_ with no MD at inference time. Our quantum method must be compared against it or
against a re-implementation, and the challenge's "statistically significant enrichment"
criterion should be reported in a form comparable to an ROC-AUC.

**Zhang S, Bowman GR.** _Decrypting cryptic pockets with physics-based simulations and
artificial intelligence._ Curr Opin Struct Biol 2026;96:103215. doi:10.1016/j.sbi.2025.103215.
**[asserted]** Recent review; treats the KRAS G12C switch-II pocket as the canonical
success story ("the discovery of a hidden switch-II pocket in KRAS G12C led to the
development of two FDA-approved covalent inhibitors, AMG 510 and MRTX849"). **[asserted]**
Contains **no** discussion of the ABL myristoyl pocket or of myosin.

### D.2 BCR-ABL1 myristoyl pocket — no blind apo prediction found

I found **no published attempt to blind-predict the myristoyl pocket from a myristate-free
apo ABL structure**. What exists:

- **Kumar A, Kaynak BT, Dorman KS, Doruker P, Jernigan RL.** _Predicting allosteric pockets
  in protein biological assemblages._ Bioinformatics 2023;39:btad275.
  doi:10.1093/bioinformatics/btad275. PMID 37115636. **[asserted]** APOP: **Gaussian
  Network Model** (Cα-level elastic network) + Fpocket; pockets are perturbed by stiffening
  their springs to emulate ligand binding, then ranked by the resulting shift in **global
  mode frequencies** combined with local hydrophobic density. Benchmark: 104 proteins
  (61 monomers, 43 multimers) from the AlloPred and ESSA sets; **88.5% of known allosteric
  pockets in the top 3**; 84% on 50 holo structures; first-rank 35/50 vs AlloPred's 19/50;
  p = 0.00088. **[asserted]** KRAS, ABL1 and myosin are **not** named among the benchmark
  examples in the text I retrieved. **This is the closest classical analogue to our own
  method** — an elastic network, perturbed, scored by mode-frequency shift — and it is the
  baseline our quantum metric must beat or at least match. Get the 104-protein list.
- **[unverified]** Gatlin et al., Protein Science 2026, doi:10.1002/pro.70714 — a
  protein-language-model + energy-landscape-frustration framework which, per search
  snippets, reports that "the myristoyl allosteric pocket in ABL remains neutrally
  frustrated across complexes" and that allosteric sites in general are "enriched in
  neutrally frustrated zones, producing diffuse and context-dependent predictions". Wiley
  returned 402 (paywall). If accurate this is a _negative_ result for the myristoyl pocket
  and worth citing as such — negative results are results.
- **[unverified]** Verkhivker G, bioRxiv 2022 doi:10.1101/2022.11.29.518410, "Probing
  Conformational Landscapes and Mechanisms of Allosteric Communication in the Functional
  States of the ABL Kinase Domain…" — per search snippets, built its myristate-bound and
  DFG-out systems **starting from `1OPL` chain B** with the SH2 domain removed. Not a blind
  prediction (it is a mechanism study), but it confirms that `1OPL` chain B is treated by
  others as a usable single-chain starting point.

**[inferred]** The absence of a blind apo prediction on this pocket is an _opportunity_: if
our method ranks the myristoyl pocket highly from `1M52` (straight αI, no myristate), that
is a novel result, not a reproduction.

### D.3 Cardiac myosin — one relevant method paper, no mavacamten-site prediction found

**Zheng W.** _Predicting allosteric sites using fast conformational sampling as guided by
coarse-grained normal modes._ J Chem Phys 2023;158:124127. doi:10.1063/5.0141630. PMID 37003737. This is **reference [1] of `CHALLENGE.md` §10**. **[asserted]**, abstract
verbatim: conformational sampling "guided by coarse-grained normal modes solved from the
elastic network models followed by atomistic backbone and sidechain reconstruction";
"simply sampling along each of the lowest 30 modes can adequately restructure cryptic sites
so they are detectable by pocket finding programs like Concavity"; applied to "four
classical examples of allosteric regulation (**GluR2 receptor, GroEL chaperonin, GPCR, and
myosin**)"; runtime "1–2 h for an average-size protein of ∼400 residues".

**[unverified]** Which myosin, which structure, and which site Zheng targeted — the abstract
does not say and AIP is paywalled. This matters a great deal: if Zheng's myosin case is the
mavacamten/OM pocket, it is direct prior art on our exact target and the challenge cites it
as its own reference [1]. Resolving it: obtain the paper's §III myosin subsection.
**Flag this as a high-priority open item.**

I found **no** published attempt to predict the mavacamten binding site from an apo myosin
structure. General myosin allostery modelling exists (e.g. normal-mode and network studies
of myosin II and myosin V) but targets the lever-arm/converter communication pathway rather
than pocket prediction. **[inferred]** Combined with the fact that the co-structures only
appeared in December 2023, this makes the mavacamten pocket a genuinely open prediction
problem — and therefore the most _interesting_ of our three, provided we fix the structures
(C.9).

### D.4 Summary of baselines to beat

| Method                    | Class                                                | Reported performance                         | Applies to                                       |
| ------------------------- | ---------------------------------------------------- | -------------------------------------------- | ------------------------------------------------ |
| APOP (Kumar 2023)         | GNM elastic network + pocket perturbation, **no MD** | 88.5% top-3 over 104 proteins                | direct analogue of our method                    |
| PocketMiner (Meller 2023) | GNN on a single static structure                     | ROC-AUC 0.87 over 39 cryptic pockets         | direct analogue; sets the accuracy bar           |
| Zheng 2023                | CG-NMA-guided sampling + Concavity                   | qualitative; 1–2 h per ~400-residue protein  | sets the _runtime_ bar; includes myosin          |
| Grant 2011                | MD ensemble + FTMAP/docking                          | found the S-IIP region 2 years pre-discovery | KRAS specifically                                |
| Vithani 2024              | WE-MD along normal modes                             | >400 μs of MD                                | KRAS specifically; the cost we claim to undercut |

---

## E. Index of every PDB ID named in this document

Each row names the source that put the ID in front of me. "RCSB" means I pulled the entry's
own record; where a paper is also named, that paper is the entry's primary citation or the
publication that names the ID.

| PDB ID                                                                         | What it is                                                                                                               | Source that named it                                                                                                        |
| ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------- |
| `1M52`                                                                         | c-Abl kinase domain + PD173955, **no myristate**, straight αI, 2.60 Å, mouse                                             | Paladini 2024 (doi:10.7554/eLife.92324); RCSB; Nagar 2002 Cancer Res, PMID 12154025                                         |
| `1NKP`                                                                         | Myc–Max heterodimer + DNA, 1.80 Å                                                                                        | `CHALLENGE.md` §6; RCSB; Nair & Burley, Cell 2003;112:193–205, doi:10.1016/S0092-8674(02)01284-9, PMID 12553908             |
| `1OPJ`                                                                         | Mouse Abl kinase domain + **MYR** + imatinib, 1.75 Å, P00520 res 229–515                                                 | Nagar 2003 (doi:10.1016/S0092-8674(03)00194-6); RCSB                                                                        |
| `1OPK`                                                                         | Mouse Abl SH3-SH2-kinase + **MYR** + P16, 1.80 Å                                                                         | Nagar 2003; RCSB                                                                                                            |
| `1OPL`                                                                         | Human Abl MYR-SH3-SH2-kinase, 3.42 Å, **MYR in chain A only** + P16 in both                                              | `CHALLENGE.md` §6; RCSB header file; Nagar 2003                                                                             |
| `2FO0`                                                                         | Human Abl 1b core + **MYR** + P16 + SEP, 2.27 Å                                                                          | de Buhr & Gräter 2023 (doi:10.7554/eLife.85216); Paladini 2024; RCSB; Nagar 2006 Mol Cell, doi:10.1016/j.molcel.2006.01.035 |
| `2G2F`, `2G2I`                                                                 | Abl ATP-analog-bound / active kinase domain                                                                              | de Buhr & Gräter 2023 **[not independently verified]**                                                                      |
| `2HYY`                                                                         | Abl, type-II-inhibitor-bound, inactive A-loop                                                                            | Paladini 2024 **[not independently verified]**                                                                              |
| `2PMX`                                                                         | K-Ras, used for MD                                                                                                       | Grant 2011 (doi:10.1371/journal.pone.0025711)                                                                               |
| `3GFT`                                                                         | K-Ras, used for blind docking                                                                                            | Grant 2011                                                                                                                  |
| `3JBH`                                                                         | Tarantula striated-muscle IHM — **the template for `5TBY`**                                                              | Alamo 2017 (doi:10.7554/eLife.24634)                                                                                        |
| `3K5V`                                                                         | Mouse Abl kinase + imatinib + **GNF-2 (STJ)**, 1.74 Å                                                                    | RCSB; Zhang 2010 Nature, doi:10.1038/nature08675, PMID 20072125                                                             |
| `4DB1`, `4P7H`                                                                 | human β-cardiac myosin reference structures                                                                              | search result only — **[unverified]**, not used                                                                             |
| `4LDJ`                                                                         | **KRAS G12C**, GDP + Mg, 1.15 Å, no inhibitor                                                                            | RCSB DOI search on 10.1073/pnas.1404639111; Hunter 2014 PNAS, PMID 24889603                                                 |
| `4LUC`                                                                         | K-Ras G12C + disulfide compound 6 (20G) + GDP, 1.29 Å                                                                    | RCSB; Ostrem 2013                                                                                                           |
| `4LV6`, `4LYF`, `4LYH`, `4LYJ`, `4M1O`, `4M1S`, `4M1T`, `4M1Y`, `4M21`, `4M22` | the other Ostrem 2013 K-Ras G12C inhibitor complexes                                                                     | Ostrem 2013 data-availability statement, PMC4274051 **[not individually verified]**                                         |
| `4NMM`                                                                         | K-Ras G12C + GDP-competitive covalent inhibitor (Y9Z), 1.89 Å                                                            | RCSB DOI search; Hunter 2014                                                                                                |
| `4OBE`                                                                         | **Wild-type** human KRas + GDP + Mg, 1.24 Å                                                                              | `CHALLENGE.md` §6; RCSB; Hunter 2014                                                                                        |
| `5MO4`                                                                         | Human ABL1 res 27–515 (1b), T334I/D382N + **asciminib (AY7)** + nilotinib, 2.17 Å, **no MYR**                            | `CHALLENGE.md` §6; RCSB; Wylie 2017, doi:10.1038/nature21702                                                                |
| `5N69`                                                                         | Bovine cardiac myosin S1 + **omecamtiv mecarbil**                                                                        | RCSB; Planelles-Herrero 2017, doi:10.1038/s41467-017-00176-5                                                                |
| `5N6A`                                                                         | Bovine cardiac myosin motor domain, pre-powerstroke, **no drug**, 3.10 Å                                                 | RCSB; Planelles-Herrero 2017                                                                                                |
| `5TBY`                                                                         | Human β-cardiac HMM **interacting-heads motif homology model**, 20 Å, no ligands                                         | `CHALLENGE.md` §6; RCSB; Alamo 2017                                                                                         |
| `6C1H`                                                                         | **Rat myosin-1b + rabbit skeletal actin + calmodulin**, ADP only, cryo-EM 3.90 Å — **no mavacamten, not cardiac myosin** | `CHALLENGE.md` §6; RCSB; Mentes 2018 PNAS, doi:10.1073/pnas.1718316115, PMID 29358376                                       |
| `6HD4`                                                                         | Mouse ABL1 + imatinib + **FYW** (asciminib _analogue_, not asciminib), 2.03 Å                                            | RCSB DOI search on 10.1021/acs.jmedchem.8b01040; Schoepfer 2018                                                             |
| `6HD6`                                                                         | Mouse ABL1 + imatinib + **FYH**, 2.30 Å                                                                                  | RCSB DOI search; Schoepfer 2018                                                                                             |
| `6NPE`                                                                         | Abl structure with straight αI helix                                                                                     | de Buhr & Gräter 2023 **[not independently verified]**                                                                      |
| `6OIM`                                                                         | Human KRAS G12C (+C51S/C80L/C118S, His-tagged) covalently bound to **AMG 510 (MOV)** + GDP + Mg, 1.65 Å                  | `CHALLENGE.md` §6; RCSB DOI search on 10.1038/s41586-019-1694-1; Canon 2019                                                 |
| `8ACT`                                                                         | **Experimental** human β-cardiac myosin folded-back (IHM) off state, cryo-EM 3.60 Å, ADP + PO4 + MG, all-human           | RCSB; Grinzato 2023 Nat Commun, doi:10.1038/s41467-023-38698-w, PMID 37258552; also cited by Auguin 2024                    |
| `8G47`, `8TLR`, `8UDR`, `8VR9`, `8VRA`, `8VRB`                                 | other entries containing sotorasib (MOV)                                                                                 | RCSB comp-ID search on MOV                                                                                                  |
| `8QYP`                                                                         | Bovine β-cardiac myosin motor domain, pre-powerstroke, **apo (no drug)**, ADP·VO4·Mg, 2.76 Å                             | RCSB; Auguin 2024, doi:10.1038/s41467-024-47587-9                                                                           |
| `8QYQ`                                                                         | Bovine β-cardiac myosin **S1 + mavacamten (XB2)**, 2.61 Å                                                                | RCSB comp-ID search on XB2; Auguin 2024                                                                                     |
| `8QYR`                                                                         | Bovine β-cardiac myosin **motor domain + mavacamten (XB2)**, 1.80 Å                                                      | RCSB comp-ID search on XB2; Auguin 2024                                                                                     |
| `8QYU`                                                                         | Bovine β-cardiac myosin S1 + omecamtiv mecarbil, 1.96 Å                                                                  | Auguin 2024 (PMC11161628)                                                                                                   |
| `8SSN`                                                                         | Human ABL1 kinase + **asciminib (AY7)** + SKI, 2.86 Å                                                                    | RCSB comp-ID search on AY7; Kim 2023 PNAS, doi:10.1073/pnas.2304611120, PMID 37590418                                       |
| `9GZ1`                                                                         | **Human** β-cardiac myosin **IHM + mavacamten (XB2)**, cryo-EM 3.70 Å                                                    | RCSB comp-ID search on XB2; McMillan, doi:10.1101/2025.02.12.637875 / Sci Adv doi:10.1126/sciadv.aea9335                    |
| `9GZ2`                                                                         | **Human** β-cardiac HMM motor domain, primed, **+ mavacamten (XB2)**, cryo-EM 2.90 Å                                     | RCSB comp-ID search on XB2; McMillan                                                                                        |
| `9YP9`                                                                         | Human β-cardiac myosin **IHM + mavacamten**, S2-FH **docked**, cryo-EM 3.00 Å                                            | RCSB comp-ID search on XB2; Somavarapu 2026 Sci Adv, doi:10.1126/sciadv.aed6472, PMID 42054467                              |
| `9YR7`                                                                         | Human β-cardiac myosin **IHM + mavacamten**, S2-FH **undocked**, cryo-EM 3.00 Å                                          | RCSB comp-ID search on XB2; Somavarapu 2026                                                                                 |
| EMD-2240                                                                       | 2.8 nm negative-stain human cardiac thick-filament reconstruction — the map `5TBY` was fitted to                         | Alamo 2017                                                                                                                  |

### Chemical component IDs worth pinning

| Comp ID | Compound                                                | Entries containing it                                     | Source                                          |
| ------- | ------------------------------------------------------- | --------------------------------------------------------- | ----------------------------------------------- |
| `MOV`   | AMG 510 / sotorasib (bound form)                        | 7: `6OIM`, `8G47`, `8TLR`, `8UDR`, `8VR9`, `8VRA`, `8VRB` | RCSB comp-ID search **[derived]**               |
| `AY7`   | **asciminib** (C20H18ClF2N5O3; RCSB→DrugBank: Scemblix) | 2: `5MO4`, `8SSN`                                         | RCSB comp-ID search + ligand page **[derived]** |
| `FYW`   | asciminib analogue (C21H18F3N5O3) — **not** asciminib   | 1: `6HD4`                                                 | RCSB ligand page **[derived]**                  |
| `XB2`   | **mavacamten**                                          | **6**: `8QYQ`, `8QYR`, `9GZ1`, `9GZ2`, `9YP9`, `9YR7`     | RCSB comp-ID search **[derived]**               |
| `MYR`   | myristic acid                                           | present in `1OPJ`, `1OPK`, `1OPL` (chain A only), `2FO0`  | RCSB / PDB header **[derived]**                 |

---

## F. Open items that this review could not close

Ordered by impact on the submission.

1. **Zheng 2023 (`CHALLENGE.md` ref [1]) myosin case study** — which myosin, which
   structure, which site? If it is the mavacamten/OM pocket this is direct prior art on our
   target, cited by the challenge itself. Paywalled (AIP). **High priority.**
2. **`1OPL` chain B** — myristate-free? αI straight or kinked? Pocket open or collapsed? No
   literature statement found; answerable by our own structural audit in minutes.
3. **PocketMiner's 39-pocket dataset** — does it contain KRAS? If so, its per-pocket score
   on the S-IIP is a directly comparable number. Available from the paper's data repository.
4. **Vithani 2024 starting structure** — `4OBE` or not. Determines whether the field really
   treats `4OBE` as the standard WT KRAS:GDP reference.
5. **Human vs bovine MYH7 residue correspondence** — run the pairwise alignment before
   transferring Auguin's bovine residue numbers to any human structure.
6. **Attribution of the αE/αF/αH/αI′ myristoyl-pocket residue list** — probably Roskoski
   2022 Pharmacol Res 178:106156; the residues are corroborated by three open sources but
   the citation is not confirmed.
7. **A residue list for the mavacamten site in human numbering** — McMillan and Somavarapu
   have it; both full texts returned 403.
8. **Gatlin 2026 Protein Sci** — the claim that the ABL myristoyl pocket is "neutrally
   frustrated" and hard to predict is a citable negative result if it holds. Paywalled.

---

## G. One-line verdict per target

- **KRAS G12C** — pocket well defined, apo/holo pair usable; the apo file is **wild-type**,
  not G12C. Add `4LDJ` as a sensitivity check, and state the genotype honestly everywhere.
- **BCR-ABL1** — pocket well defined and the holo (`5MO4`) is correct; the apo (`1OPL`)
  **contains myristate in the pocket we are asked to find**, plus an ATP-site inhibitor.
  Fix by chain choice, by stripping-with-disclosure, or by adding `1M52` as a genuinely
  closed control.
- **Cardiac myosin** — the holo (`6C1H`) is **the wrong protein, the wrong species, and
  contains no drug**; the apo (`5TBY`) is a 20 Å homology model. Replace with
  `8QYP` → `8QYR` (or `8ACT` → `9GZ1`) and say why.
