# Apo/holo pair curation — the field's checklist, and where it is silent

**Question.** When structural-biology / cryptic-pocket / allostery groups curate an apo–holo
pair _for a benchmark_, what is the published protocol? What dimensions do they check, with
which tools and thresholds — so that a new benchmark can be audited against field standard
rather than against intuition.

**Companion document.** [`apo-holo-definition.md`](apo-holo-definition.md) settles what the
word _apo_ means. This document assumes that answer and asks the next one: given a candidate
pair, what else does the field check. Overlap is deliberate where a source speaks to both.

**Scope.** Literature retrieved 2026-08-20 via Europe PMC REST, plus four sources outside
Europe PMC's OA subset (marked). Verification tags:

- `[VERIFIED-FULLTEXT]` — quoted from full text retrieved this session.
- `[VERIFIED-ABSTRACT]` — from the abstract record retrieved this session; body not read.
- `[UNVERIFIED]` — secondhand, inferred, or recorded in a sibling document but not
  re-derived here. A lead, not evidence.

Nothing is recalled from memory. §7 lists what no retrieved source establishes.

---

## 0. The headline

Three findings matter more than the individual thresholds.

1. **There is a stable core and a long tail.** Five dimensions are checked by nearly
   everyone (resolution, ligand-contact cutoff, ligand-validity list, pair sequence identity,
   redundancy clustering). Everything else is checked by one to four sources, often with
   _incompatible_ policies — covalent ligands are excluded by Binding MOAD and Clark et al.
   and kept by CryptoBench; oligomeric interfaces are excluded by PocketMiner and
   deliberately included by AHoJ-DB.
2. **No apo–holo or cryptic-pocket benchmark in the retrieved corpus validates the ligand's
   own electron density.** RSCC/RSR/OMIT-density checking is a well-developed standard
   (VHELIBS, Twilight, Iridium, the LiveCoMS best-practice guide), and it lives entirely in
   the docking / affinity-benchmark literature. CryptoSite, PocketMiner, CryptoBench, AHoJ,
   AHoJ-DB, ASD, ASBench, CASBench, AlloBench, PASSer and DeepAllo all take the deposited
   ligand at face value. Wankowicz et al. come closest, by re-refining every structure and
   rejecting any whose R-free degrades.
3. **The dimensions most likely to break a hand-built four-target benchmark are the ones the
   field checks least**, because a PDB-wide pipeline gets them for free and a human does not:
   ligand identity by chemical component ID, gene/species identity, residue-numbering
   convention, and obsolete or superseded entries. §6 is written for that failure mode.

---

## 1. Sources, and what each one actually is

| #   | Source                                                           | DOI                                                                                                                | What it is                                                             | Access                         |
| --- | ---------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------- | ------------------------------ |
| A   | Cimermancic et al. 2016, **CryptoSite**, J Mol Biol              | [10.1016/j.jmb.2016.01.029](https://doi.org/10.1016/j.jmb.2016.01.029)                                             | the founding cryptic-site apo/holo set                                 | body via PMC author manuscript |
| B   | Meller et al. 2023, **PocketMiner**, Nat Commun                  | [10.1038/s41467-023-36699-3](https://doi.org/10.1038/s41467-023-36699-3)                                           | 38 pairs / 39 cryptic pockets, the most explicit filter list published | OA                             |
| C   | Škrhák et al. 2024, **CryptoBench**, Bioinformatics              | [10.1093/bioinformatics/btae745](https://doi.org/10.1093/bioinformatics/btae745)                                   | 1107 apo structures, PDB-scale, built on AHoJ-DB                       | OA                             |
| D   | Feidakis et al. 2022, **AHoJ**, Bioinformatics                   | [10.1093/bioinformatics/btac701](https://doi.org/10.1093/bioinformatics/btac701)                                   | the search tool; defines apo/holo per site                             | OA                             |
| E   | Feidakis et al. 2024, **AHoJ-DB**, J Mol Biol                    | [10.1016/j.jmb.2024.168545](https://doi.org/10.1016/j.jmb.2024.168545)                                             | PDB-wide precomputed apo/holo relations                                | paywalled                      |
| F   | Wankowicz et al. 2022, **eLife**                                 | [10.7554/eLife.74114](https://doi.org/10.7554/eLife.74114)                                                         | 743 pairs; the strictest crystallographic matching found               | OA                             |
| G   | Clark et al. 2019, PLoS Comput Biol                              | [10.1371/journal.pcbi.1006705](https://doi.org/10.1371/journal.pcbi.1006705)                                       | 305 sequences, 2369 holo / 1679 apo                                    | recorded in sibling doc        |
| H   | Benson et al. 2008, **Binding MOAD**, NAR                        | [10.1093/nar/gkm911](https://doi.org/10.1093/nar/gkm911)                                                           | the ligand-validity authority the others depend on                     | OA                             |
| I   | **ASD** v3.0 / 2019, NAR                                         | [10.1093/nar/gkv902](https://doi.org/10.1093/nar/gkv902), [10.1093/nar/gkz958](https://doi.org/10.1093/nar/gkz958) | the allosteric database                                                | OA                             |
| J   | Kuzmin et al. 2019, **CASBench**, Acta Naturae                   | [10.32607/20758251-2019-11-1-74-80](https://doi.org/10.32607/20758251-2019-11-1-74-80)                             | 91 enzymes with catalytic + allosteric sites                           | OA                             |
| K   | 2025, **AlloBench**, ACS Omega                                   | [10.1021/acsomega.5c01263](https://doi.org/10.1021/acsomega.5c01263)                                               | a _pipeline_, and a critique of ASD/ASBench/CASBench curation          | OA                             |
| L   | 2023, **PASSer**, NAR                                            | [10.1093/nar/gkad303](https://doi.org/10.1093/nar/gkad303)                                                         | allosteric-site predictor; states the "Huang" cleaning workflow        | OA                             |
| M   | 2025, **DeepAllo**, Bioinformatics                               | [10.1093/bioinformatics/btaf294](https://doi.org/10.1093/bioinformatics/btaf294)                                   | pLM-based allosteric-site predictor                                    | OA                             |
| N   | 2024, **MEF-AlloSite**, J Cheminform                             | [10.1186/s13321-024-00882-5](https://doi.org/10.1186/s13321-024-00882-5)                                           | ASBench-based; explicit test-isolation rules                           | OA                             |
| O   | Monzon et al. 2016, **CoDNaS 2.0**, Database                     | [10.1093/database/baw038](https://doi.org/10.1093/database/baw038)                                                 | conformational-diversity database — the "matched conformer" tradition  | OA                             |
| P   | Brylinski & Skolnick 2008, Proteins                              | [10.1002/prot.21510](https://doi.org/10.1002/prot.21510)                                                           | 521 paired apo/holo structures, global conformational change           | abstract only                  |
| Q   | Adasme-Carreño / Gonzalez et al. 2013, **VHELIBS**, J Cheminform | [10.1186/1758-2946-5-36](https://doi.org/10.1186/1758-2946-5-36)                                                   | binding-site + ligand density validation thresholds                    | OA                             |
| R   | 2022, **LiveCoMS best practices** for protein–ligand benchmarks  | [10.33011/livecoms.4.1.1497](https://doi.org/10.33011/livecoms.4.1.1497)                                           | the most complete published curation checklist                         | OA body via PMC                |
| S   | Warren et al. 2012, **Iridium**, Drug Discov Today               | [10.1016/j.drudis.2012.06.011](https://doi.org/10.1016/j.drudis.2012.06.011)                                       | "only 17% were found to be acceptable"                                 | abstract only                  |
| T   | Weichenberger et al. 2017, **Twilight reloaded**, Acta Cryst D   | [10.1107/S205979831601620X](https://doi.org/10.1107/S205979831601620X)                                             | ligand density scepticism                                              | OA                             |

Also consulted and reported as thin: ASBench ([10.1093/bioinformatics/btv169](https://doi.org/10.1093/bioinformatics/btv169),
paywalled, abstract only), AlloSite ([10.1093/bioinformatics/btt399](https://doi.org/10.1093/bioinformatics/btt399),
paywalled), MolMovDB ([10.1093/nar/gkg104](https://doi.org/10.1093/nar/gkg104), full text
404 from the Europe PMC XML endpoint this session), and the apoholo.cz documentation (no DOI).

---

## 2. Source-by-source: the stated criteria

### 2.1 CryptoSite (A)

The founding set. Criteria are terse; the numeric detail lives in an SI Text that PMC now
gates behind a JavaScript challenge.

| Dimension             | Stated criterion                                                                                                                                                                                                                       |
| --------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Apo/holo              | "gathering structures of protein-ligand complexes as well as structures of proteins in ligand-free (unbound) conformations" `[VERIFIED-FULLTEXT]`                                                                                      |
| Ligand validity       | "We selected cryptic sites and binding pockets whose ligands are biologically relevant (MOAD database)" `[VERIFIED-FULLTEXT]` — i.e. the rule is **delegated to Binding MOAD (H)**                                                     |
| Site definition       | "residues with at least one atom within **5 Å** from any atom of a ligand" `[VERIFIED-FULLTEXT]` (note: _any_ atom, not heavy atom)                                                                                                    |
| Redundancy            | "applying sequence identity threshold of **40%**" `[VERIFIED-FULLTEXT]`                                                                                                                                                                |
| Crypticity            | "Binding sites with bad pocket scores in the unbound conformation and good pocket scores in the bound conformation were defined as cryptic sites"; tools are **Fpocket and ConCavity** `[VERIFIED-FULLTEXT]`                           |
| Non-cryptic positive  | "those with good pocket scores in both conformations were defined as binding pockets" `[VERIFIED-FULLTEXT]`                                                                                                                            |
| Negative class        | "705 concave surface patches from the Protein Data Bank and the MOAD database" `[VERIFIED-FULLTEXT]`                                                                                                                                   |
| Conformational change | reported, not filtered on: "all-atom RMSD of cryptic binding sites between apo and holo conformations ranges between **0.45 Å and 22.45 Å**" `[VERIFIED-FULLTEXT]`                                                                     |
| Counts                | "84 known examples of cryptic binding sites, 92 binding pockets, and 705 concave surface patches" `[VERIFIED-FULLTEXT]`                                                                                                                |
| Performance           | "AUC of 0.83, with respective true positive and false positive rates of 79% and 29%" `[VERIFIED-FULLTEXT]`                                                                                                                             |
| Resolution            | **not stated in the body.** The paper instead advertises tolerance: "CryptoSite can also be applied to low-resolution atomic structures and comparative models, in addition to high-resolution X-ray structures" `[VERIFIED-FULLTEXT]` |

Not mentioned anywhere in the retrieved body: mutations, species, construct differences,
altlocs, missing residues, crystal contacts, insertion codes, manual/literature validation of
individual sites. Targeted probes for each returned nothing `[VERIFIED-FULLTEXT]` (absence
established by search, not by reading every line).

**Consequence for anyone reusing this set:** its ligand policy is Binding MOAD's, so
covalent ligands are excluded by inheritance (§2.8), and its structure-quality policy is
essentially _none_.

### 2.2 PocketMiner (B)

The most explicit filter list published for apo–holo pairs. Quoted in full because the list
itself is the contribution.

Ligand and site:

> "Cryptic ligands are the holo ligands with ligand-free apo binding sites, plus any associated ions within 3.5 Å which are absent from apo" `[VERIFIED-FULLTEXT]`

> "Ligand-lining residues are residues with any heavy atom within **5 Å** of any heavy atom of a cryptic ligand." `[VERIFIED-FULLTEXT]`

> "We removed apo candidate structures with ligands (excluding water, heavy water, sodium, chloride, and potassium) within **5 Å** of all MOAD-assigned biologically relevant residues" `[VERIFIED-FULLTEXT]`

> "We removed holo candidate chains without biologically relevant ligands" / "We removed holo candidate chains in which the holo ligand was a polymer." `[VERIFIED-FULLTEXT]`

Structure quality and topology:

> "We removed each candidate structure which did not have at least **2.5 Å** resolution." — and they note the side effect: "This criterion removed NMR structures, which do not have resolutions reported in PDB files." `[VERIFIED-FULLTEXT]`

> "We also excluded multi-conformer X-ray structures (not to be confused with structures which have only a few residues modelled in multiple conformations)." `[VERIFIED-FULLTEXT]`

> "We removed each candidate structure which did not have a **monomeric biological unit** assigned in remark 350 of the PDB file." `[VERIFIED-FULLTEXT]`

> "We removed chains with **gaps longer than 3 residues**." `[VERIFIED-FULLTEXT]`

> "We removed chains with **alphabetic residue insertion codes** (e.g., 35 A)." `[VERIFIED-FULLTEXT]`

> "We removed **non-canonical residues**, except for those containing selenocysteine and selenomethionine, which were treated as cysteine and methionine respectively." `[VERIFIED-FULLTEXT]`

Pair identity:

> "We removed apo candidate structures with less than **100%** sequence identity to their respective holo candidate structures, except for mismatches between selenocysteine and cysteine and selenomethionine and methionine" `[VERIFIED-FULLTEXT]`

Crypticity, measured with LIGSITE:

> "we removed any apo-holo pairs in which the LIGSITE pocket volume assigned to the ligand-lining residues in apo was greater than the volume assigned to them in holo by at least **20 Å³**" `[VERIFIED-FULLTEXT]`

> "For the LIGSITE calculation implemented in enspara, we used a **min rank of 7, a grid spacing of 0.7 Å, a probe radius of 1.4 Å, and a minimum cluster size of 3 grid points**." `[VERIFIED-FULLTEXT]`

> "To assign pocket volumes to residues, we calculated how many LIGSITE pocket grid points were within **5 Å** of each residue." `[VERIFIED-FULLTEXT]`

> residue-level label: "a positive example if at any point in simulation the nearby pocket volume determined by the LIGSITE algorithm increased by more than **40 Å³**" — with an unusually candid justification: "volume alone does not indicate steric compatibility… The threshold was therefore assigned manually." `[VERIFIED-FULLTEXT]` (the fetched text renders the unit as "Ų"; the sibling doc records Å³, and volume is the quantity)

Leakage control:

> "We removed the protein with the lower cryptic site RMSD when the sequence identity of a pair of proteins exceeds **40%**." / "All of the proteins in the test set had less than **55%** sequence identity with proteins in the training set" `[VERIFIED-FULLTEXT]`

Evaluation: ROC-AUC 0.87 vs CryptoSite's 0.85; per-fold PR-AUC 0.44 ± 0.12 against ROC-AUC
0.83 ± 0.04 `[VERIFIED-FULLTEXT]`. No statistical null.

Candidate generation by BLAST against Binding MOAD with hits below 90% identity removed, and
their two admitted blind spots (histidine-tag terminal differences; reliance on PDB residue
numbers rather than alignment) are recorded in the sibling document `[UNVERIFIED here]`.

### 2.3 CryptoBench (C)

Built on AHoJ-DB, so its apo/holo semantics are inherited (site-relative). The filter cascade,
quoted:

> "All records with a resolution worse than **2.5 Å** were filtered out" `[VERIFIED-FULLTEXT]`

> "all records where **pocket length** in the apo state and holo state did not match were filtered out" `[VERIFIED-FULLTEXT]`

> "we establish a threshold for the minimum accepted global similarity between the two states of the protein chain that comprises the binding site, achieved by a minimum **TM-score of 0.5**" `[VERIFIED-FULLTEXT]`

> "we establish a maximum distance threshold of **4 Å** between the centers of apo and holo binding sites, after the global structural alignment" `[VERIFIED-FULLTEXT]`

> "we establish a threshold for the allowed change in the level of compactness of the binding site… by allowing up to a **20% change in the radius of gyration** from the holo state" `[VERIFIED-FULLTEXT]`

> "at least **50 observed residues** from the protein must overlap with its UniProt sequence" `[VERIFIED-FULLTEXT]`

> "records with **pocket RMSD below 2 Å** were filtered out" `[VERIFIED-FULLTEXT]`

> "we excluded ligands where the number of atoms is less than **5**… the name of the PDB group is not on the list of ignored groups: **HOH, DOD, WAT, UNK, ABA, MPD, GOL, SO4, PO4**" `[VERIFIED-FULLTEXT]`

> "The original P2Rank ignored group list also included sugars MAN, GLC, and NAG. However, these sugars are biologically relevant" — sugars **kept** `[VERIFIED-FULLTEXT]`

> "we have decided to keep even ligands that are **covalently attached** as they have proven to be relevant" `[VERIFIED-FULLTEXT]`

Definition and its calibration:

> "A CBS refers to a region in a protein that can bind a ligand and undergoes a significant structural change between its holo and apo forms." `[VERIFIED-FULLTEXT]`

> "By selecting the upper bound of the borderline interval **[1.5, 2] Å**, we aimed to minimize the risk of unintentionally including regular binding sites in the cryptic dataset" — set after they "manually inspected the remaining six pairs with RMSD between 1.35 and 1.93 Å" `[VERIFIED-FULLTEXT]`

Pair selection and leakage:

> "from each cluster from the previous step, we selected **one representative apo–holo pair based on maximal pocket RMSD**" `[VERIFIED-FULLTEXT]`

> "unique UniProt sequences were clustered based on **40%** similarity"; then "another round of clustering… utilized a threshold of **10%** sequence identity" for the CV split `[VERIFIED-FULLTEXT]`

Numbering: "Apo and holo structures are mapped residue-wise by linking the common binding
residues by their **UniProt sequence indices**" `[VERIFIED-FULLTEXT]`.

Evaluation: TPR, FPR, F1, ACC, MCC, AUC, AUPRC at residue level; baselines PocketMiner,
P2Rank, and a sequence-only pLM-NN. No null model `[VERIFIED-FULLTEXT]`. Stated limitation:
the 2 Å rule "may fail to detect CBSs with small changes, such as a minor side chain
rotation" `[VERIFIED-FULLTEXT]`.

Silent on: alternate locations, insertion codes, modified residues, crystal contacts,
experimental method.

### 2.4 AHoJ and AHoJ-DB (D, E)

The tool that made apo/holo a property of a _pocket_.

> "each one is listed as holo or apo respective to the presence or absence of ligands in the **defined binding site(s)**" — AHoJ `[VERIFIED-FULLTEXT]`

> "the binding pocket is captured and mapped across existing structures within the same UniProt, and **the mapped pockets are annotated as apo or holo**, based on the presence or absence of ligands" — AHoJ-DB `[VERIFIED-ABSTRACT]`

> "labeled as HOLO (bound) or APO (unbound) **with respect to the binding site** defined by the ligand" — apoholo.cz/db documentation, no DOI `[VERIFIED-FULLTEXT, NO DOI]`

Mechanics:

- Binding site: protein residues within a **user-defined 4.5 Å default** of the specified
  ligand's atoms `[VERIFIED-FULLTEXT via C, which restates AHoJ's default]`; the AHoJ paper
  itself defers numerics to its Supplementary Information.
- Candidate retrieval: "detecting the **UniProt** accession number (AC) of each query chain
  and retrieving all other chains that belong to the same UniProt AC", residue-level mapping
  from **SIFTS**, then structural alignment with **TM-align** `[VERIFIED-FULLTEXT]`.
- Admission threshold: "If a **minimum percentage of binding residues** is detected, the
  chain is considered a successful candidate" `[VERIFIED-FULLTEXT]`; the default (1% of
  mapped binding residues on the candidate SEQRES) is documented on apoholo.cz
  `[UNVERIFIED — from search-result text, not from a page I read directly]`.
- Ligand scope is configurable: "in AHoJ, the concept of ligand can be extended to include
  **water molecules and modified or non-standard residues**" `[VERIFIED-FULLTEXT]`, i.e.
  off by default.
- Metals count. From the AHoJ documentation: "If it finds protein chains with ZN, it will
  list them as HOLO, if the superimposed site is empty of ligands, the chain will be listed
  as APO" — and the _user's tolerance for a different ligand at the same site_ flips the
  label: "if the user wants APO with no other ligands there, it will be listed as HOLO, and
  if the user does not mind other ligands in this binding site, it will be listed as APO"
  `[VERIFIED-FULLTEXT, NO DOI]`.
- Per-pair metrics: "chain RMSD, pocket residue RMSD, SASA, etc." (apoholo.cz help)
  `[VERIFIED-FULLTEXT, NO DOI]`.

Two statistics from AHoJ-DB that constrain how ambitious any apo-based benchmark can be:

> "about **24% of the binding sites occur at the interface of two or more chains**"

> "**less than 50%** of the total binding sites processed have an apo form in the PDB" `[VERIFIED-ABSTRACT]`

No resolution, method or validation filter is stated at either level. AHoJ-DB is a _census_,
not a curated benchmark — the filtering is the downstream consumer's job, which is exactly
what CryptoBench does.

### 2.5 Wankowicz et al. (F)

Different scientific question (side-chain heterogeneity on ligand binding), and by far the
strictest crystallographic matching. Where the cryptic-pocket sets match _sequences_, this
matches _crystals_.

> apo: "Structures without ligands, excluding common crystallographic additives, were classified as apo"; holo: "if they had a ligand with **10 or more heavy atoms**, excluding common crystallographic additives" `[VERIFIED-FULLTEXT]` — global, not site-relative.

> "We identified high-quality, high-resolution (**2 Å resolution or better**) X-ray crystallography datasets"; non-X-ray structures removed `[VERIFIED-FULLTEXT]`

Pair-matching rules, quoted as a list:

> "Same space group." / "Exact sequence or exact sequence after removing the first or last five base pairs." / "A resolution difference between the two structures less than **0.1 Å**." / "Dimensions of unit cells do not differ by more than **1 Å**" / "Angles of the unit cells do not differ by more than **1°**." `[VERIFIED-FULLTEXT]`

> when several apo candidates qualify: "we then subsetted this list down to provide only one apo structure per holo structure, based on the **smallest resolution difference**" `[VERIFIED-FULLTEXT]`

Model quality, done by re-refinement rather than by trusting the deposition:

> "we re-refined all structures using the deposited structure factors and **phenix.refine**" and "removed **88 structures where the R-free increased by >2.5%** compared to the value reported in the PDB header" `[VERIFIED-FULLTEXT]`

Occupancy and alternate conformations are treated as data, not as noise: "There were **193
structures with ligands with alternative conformations or partially occupied ligands**… 125
ligands had less than full occupancy, whereas 68 had alternative conformations that amounted
to full occupancy", plus "We normalized the ligand B-factor by the mean C-alpha B-factor to
identify ligands with higher B-factors than expected" `[VERIFIED-FULLTEXT]`.

Site definition: "any residue with a heavy atom within **5 Å** of any ligand heavy atom",
with a documented sensitivity sweep — "We varied the cutoff values between **2 and 10 Å**,
observing that the tighter the binding site definition, the more drastic the difference"
`[VERIFIED-FULLTEXT]`. Distal control: "more than **10 Å** away from any heavy atom in the
ligand" `[VERIFIED-FULLTEXT]`. Burial filter: residues "less than 20% solvent exposed".

Counts: 15 214 candidate pairs → 1205 → 743 pairs (743 unique holo, 432 unique apo), 315
UniProt IDs, plus **a 293-pair apo–apo control dataset built by identical criteria**
`[VERIFIED-FULLTEXT]`. That control set is the single most transferable idea in this source:
it measures how much apparent change is crystallographic noise.

### 2.6 Clark et al. 2019 (G) — recorded, not re-derived

Two ligand clauses at different scopes: a global one (HETs must be **≤ 100 Da** or on a
620-code filter list covering "sugars, small organic molecules, membrane components, small
metabolites, salts, buffers, solvents, crystal additives, cryoprotectants, detergents, and
metal ions", derived from Binding MOAD curation) and a site-local one ("Any structures
containing HET material apart from water (HOH) within **4.5 Å** of any unified binding site
residue were removed"). Resolution ≤ 2.5 Å; clustering at 100% then 95%; binary complexes
only; **covalent ligands excluded**. Full quotes and the unresolved scope ambiguity:
[`apo-holo-definition.md`](apo-holo-definition.md) §2.3 `[UNVERIFIED here]`.

### 2.7 Binding MOAD (H) — the ligand-validity authority

Everything above that says "biologically relevant" ultimately points here.

> "Each entry in Binding MOAD must have **resolution better than 2.5 Å**, and each entry must contain a valid ligand." `[VERIFIED-FULLTEXT]`

> "**Valid ligands are biologically relevant small molecules** and can include agonists, antagonists, cofactors, inhibitors, allosteric regulators, enzymatic products, etc." `[VERIFIED-FULLTEXT]`

> "Many small molecules present in a crystal structure are not considered biologically relevant because they are part of the **crystallization matrix**… Such molecules include **solvents, buffers, detergents and salts**, but care must be taken because **some small molecules are valid ligands in some structures but additives in others**. Examples of such are sugars, membrane components, small organic molecules (e.g. toluene) and metabolites (e.g. citrate)." `[VERIFIED-FULLTEXT]`

> "**Covalently attached molecules** (covalent inhibitors or posttranslational modifications to the protein) **are not considered valid ligands**." `[VERIFIED-FULLTEXT]`

> "When a hetgroup is considered **part of the protein** (glycosylation, catalytic metal, HEME group, etc.), it is not listed on the data page." `[VERIFIED-FULLTEXT]`

> "proteins are grouped into families of **90% sequence identity**. By choosing one representative of each family (the ligand with the best affinity), we can create a non-redundant set" `[VERIFIED-FULLTEXT]`

> "Each crystallography paper is read to classify the ligands and extract affinity data for the ligand." `[VERIFIED-FULLTEXT]`

The last quote is the important one. **Binding MOAD's ligand-validity rule is not an
algorithm — it is hand curation against the primary paper.** Every downstream benchmark that
says "biologically relevant ligands (MOAD)" is importing a human judgement, not a filter it
could reproduce. A new benchmark that cannot afford that human step must say what it
substituted.

### 2.8 The allosteric branch (I, J, K, L, M, N)

This literature largely **skips the apo problem**: it predicts allosteric sites from the
modulator-bound structure and never constructs a pair. That is the single biggest structural
difference between the cryptic-pocket branch and the allostery branch, and it is why an
allosteric benchmark cannot be audited against CryptoBench's checklist without translation.

**ASD (I).** The definitional commitment is qualitative — an allosteric site is "topographically
and spatially distant" from the orthosteric site `[VERIFIED-FULLTEXT]`. Curation method is
delegated: "Allosteric molecules and features… were collected using previously described
methods" `[VERIFIED-FULLTEXT]`. ASD does hold pairs — "**1688 allosteric apo/holo paired
structures** for allosteric modulator action in 308 proteins from 107 organisms were
constructed using the same protocol" `[VERIFIED-FULLTEXT]` — but the protocol is a citation,
not a stated criterion. No resolution filter, no site distance cutoff, no redundancy rule
appears in the v3.0 or 2019 text retrieved.

**CASBench (J).** Annotation by intersection of ASD, the Catalytic Site Atlas and the PDB:
"Proteins that were present in the ASD but not in the CSA… were excluded" `[VERIFIED-FULLTEXT]`.
Site residues: "**All residues located within 5 Å** of the selected ligand were considered and
the resulting secondary annotations of each site were merged for all the PDB structures"
`[VERIFIED-FULLTEXT]`. Redundancy: CD-HIT at **95%** `[VERIFIED-FULLTEXT]`. No resolution
filter; no apo/holo pairing.

**AlloBench (K)** is the most useful member of this group because it is a _pipeline plus a
critique_. Its steps, quoted:

> "Obsolete PDB IDs of the target protein were updated, and ASD entries of structures no longer present in the PDB were dropped." `[VERIFIED-FULLTEXT]`

> "UniProt IDs were updated by fetching the data using PDB's GraphQL API, and the entries with **discrepancies between PDB and UniProt IDs were removed**." `[VERIFIED-FULLTEXT]`

> "The active site residue numbers are from the UniProt sequence… This was resolved by **aligning the UniProt sequence with the PDB sequence**." `[VERIFIED-FULLTEXT]`

> "further filtered to only include PDB structures with a **resolution better than 4 Å**" `[VERIFIED-FULLTEXT]`

> "The **biological assembly** structures of the target proteins were downloaded from the PDB website." `[VERIFIED-FULLTEXT]`

> "**1291 out of 2034 structures had missing residues**, and 1287 structures could be modeled using ProMod3." / "Modeled structures with **lDDT < 0.8** were removed" `[VERIFIED-FULLTEXT]`

> "The discrepancies between the allosteric sites listed in ASD and the location of the allosteric modulator in the PDB structure were resolved by obtaining the **chemical component alias**." `[VERIFIED-FULLTEXT]`

> "**Structures with covalently bound allosteric modulators were removed.**" `[VERIFIED-FULLTEXT]`

> "allosteric sites were obtained by locating the residues **within 4 Å** of the allosteric modulator" `[VERIFIED-FULLTEXT]`

> leakage: "**UniRef50** cluster IDs… AlloBench proteins with these UniRef50 cluster IDs were dropped" `[VERIFIED-FULLTEXT]`

> evaluation: "The agreement between the known and predicted allosteric sites was assessed using the **Jaccard index (JI)**"; "Suppose we consider correct predictions to be those with a **JI > 0.5**. The top three programs are PASSer (Ensemble), APOP, and PASSer (AutoML), with an accuracy of **18, 15, and 13%**" `[VERIFIED-FULLTEXT]`

And its critique of its predecessors, which is directly relevant to auditing:

> "ASBench and CASBench have become **outdated** and are significantly smaller compared to the latest version of ASD 2023." / "**CASBench contains 2870 PDB structures from 91 unique proteins and thus has significant redundancy.**" / "The tab-delimited file had **missing values in the column for allosteric site residues for 1620 out of 3102 entries**" / "only **46% of entries have annotations for orthosteric sites**" `[VERIFIED-FULLTEXT]`

**PASSer (L)** states the widely-reused "Huang" cleaning workflow verbatim:

> "those proteins were filtered out if they (i) have **low resolution (>3 Å)**; (ii) have **missing residues in the allosteric site**; or (iii) have **similar structures (sequence identity threshold ≥ 30%)**" `[VERIFIED-FULLTEXT]`

and one criterion nobody else states — a sanity check that the annotated site and the
modulator actually coincide:

> "The Euclidean distances between the center of masses in its modulator and all pockets are calculated. **Those proteins were removed if the closest pocket to the modulator is >10 Å.**" `[VERIFIED-FULLTEXT]`

**DeepAllo (M)** reuses the same workflow — "resolution below 3 Å, ensuring completeness
(i.e. **no missing residues**), and maintaining a **sequence identity of <30%**", with
MMseqs2 clustering `[VERIFIED-FULLTEXT]`.

**MEF-AlloSite (N)** adds a structural leakage control the others lack:

> "protein structures that either lacked allosteric site residues or were captured at a **higher resolution than 3 Å** should be removed" / "remove redundant proteins with greater than **30% sequence similarity**" / "**A protein having higher than 0.5 TM-Score** in test 3 has been discarded" `[VERIFIED-FULLTEXT]`

Positive-pocket labelling is coarse across this whole branch: "A pocket is classified as 1
(positive) if it contains **at least one residue** that is identified as binding to allosteric
modulators" `[VERIFIED-FULLTEXT]`.

### 2.9 The conformational-change branch (O, P)

**CoDNaS 2.0 (O)** curates _conformers of the same protein_, which is the apo/holo problem
with the ligand condition dropped.

> "**BLASTClust** was run against all protein chains deposited in PDB to obtain all available clusters at **95% of local sequence identity with a minimum coverage of 0.90**" `[VERIFIED-FULLTEXT]`

> "to avoid the inclusion of **homologous** sequences in a given CoDNaS entry, we used **UNIPROT ID** to check each cluster" `[VERIFIED-FULLTEXT]`

> "The only clusters considered were those with at least two structures and with an **X-ray resolution of <4.00 Å**" `[VERIFIED-FULLTEXT]`

> "we calculated the **C-alpha RMSD using MAMMOTH** for all possible pairs of conformers… The **maximum C-alpha RMSD** value for each protein entry was registered as a measure of the conformational diversity extension." Plus "**TM score, GDT-TS and GDT-HA**" and per-position RMSD with **ProFit** `[VERIFIED-FULLTEXT]`

> "Each conformer… is characterized by the experimental conditions… including **pH, temperature, presence of ligands, mutations, oligomeric state, post-translational modifications and presence of disorder**." Sources: ligands from HETATM + **BioLiP**; oligomeric state from author annotation + **PISA**; PTMs from **MODRES**; disorder from **MobiDB** `[VERIFIED-FULLTEXT]`

This is the most complete _annotation_ schema in the corpus — it records the confounders
rather than filtering them, which is arguably the better design for a benchmark that wants to
be re-sliced later.

**Brylinski & Skolnick (P)**, 521 paired structures, is the reference point for how much
change to expect: most proteins show RMSD < 1 Å on ligand binding, with roughly a third of
multi-domain proteins showing larger changes driven by domain reorientation
`[VERIFIED-ABSTRACT]`. Useful as a prior: a 1 Å apo↔holo Cα RMSD is _typical_, not evidence
of a conformational transition.

### 2.10 The structure/ligand-quality standard (Q, R, S, T)

This is where the checks the benchmark papers omit actually live.

**VHELIBS (Q)** publishes concrete defaults:

> "default **minimum RSCC of 0.9**, a **minimum average occupancy of 1.0**, a **maximum RSR of 0.4** and a maximum good RSR of **0.24 for PDB** and **0.165 for PDB_REDO**" `[VERIFIED-FULLTEXT]`

> binding site: "all the residues nearer than a specified distance (**4.5 Å by default**) are considered to be part of the binding site of that ligand" `[VERIFIED-FULLTEXT]`

> and the rationale for not trusting global metrics: "the model quality of the protein binding sites and of the ligands bound to them are of particular interest, while **the overall model quality or the quality of the model outside the binding site are not directly relevant**" `[VERIFIED-FULLTEXT]`

Values come from **EDS** or **PDB_REDO** `[VERIFIED-FULLTEXT]`.

**LiveCoMS best practices (R)** is the closest thing to a published curation checklist, and
its items map one-to-one onto the dimensions this document is enumerating:

> resolution: "Iridium… suggests a resolution threshold of **< 3.5 Å**… Stricter thresholds have been suggested (i.e. **< 2.0 Å** in a recent benchmark)." `[VERIFIED-FULLTEXT]`

> ligand density: "The electron density around the ligand should cover **at least 90% of the ligand atom centers**… **real space correlation coefficient (RSCC) value > 0.90**." `[VERIFIED-FULLTEXT]`

> occupancy: "All ligand and active site atoms with **occupancy < 1.0** should be identified. If there is only partial density for the ligand… these partial-density atoms should be identified." `[VERIFIED-FULLTEXT]`

> missing residues: "Identify all **unmodeled residues and side chain atoms within 6 to 8 Å** of any ligand atom. When multiple structures… the structure with **no missing residues**… should be used." `[VERIFIED-FULLTEXT]`

> crystal packing: "**Ligand atoms where there are crystal packing atoms within 6 Å should be identified**… such packing atoms may affect the observed binding mode." `[VERIFIED-FULLTEXT]`

> constructs: "Often structural studies use **shorter constructs**… **mutations** might have been introduced… Such deviations should be kept to a minimum." `[VERIFIED-FULLTEXT]`

> covalent and excipients: "we would **not recommend including covalent ligands** into the standardized benchmark sets. Generally, we recommend **excluding excipients** (often specific to crystallization media)." `[VERIFIED-FULLTEXT]`

**Iridium (S)**: applying quality criteria to 728 structures previously used to validate
docking software, "**only 17% were found to be acceptable**", and structures were re-refined
"to maintain internal consistency in the comparison" `[VERIFIED-ABSTRACT]`. The headline
number is the argument: a benchmark assembled without density checks is mostly not what it
claims to be. The specific Iridium thresholds are in the paywalled body `[NOT ESTABLISHED]`.

**Twilight (T)** supplies the operational instruction: what you want is "**distinct positive
OMIT electron density for the entire modelled ligand**" `[VERIFIED-FULLTEXT]`, and B-factor
comparison against neighbouring atoms as a secondary signal. It states no numeric cutoff in
the retrieved text.

---

## 3. The consolidated checklist

Ordered by how many independent retrieved sources state the check. "Sources" counts the
letters in §1. **Near-universal** = ≥ 6 sources; **common** = 3–5; **idiosyncratic** = 1–2.

| #   | Dimension                                                                                   | Sources               | Status                                                                                            | Tool / metric normally used                     | Values seen                                                                                                                                                                                                             |
| --- | ------------------------------------------------------------------------------------------- | --------------------- | ------------------------------------------------------------------------------------------------- | ----------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | **Resolution ceiling**                                                                      | B C F G H K L M N O R | near-universal                                                                                    | PDB header `_refine.ls_d_res_high`              | 2.0 (F), 2.5 (B C G H), 3.0 (L M N), 3.5 or 2.0 recommended (R), 4.0 (K O). A does not state one                                                                                                                        |
| 2   | **Ligand-contact cutoff defining the site**                                                 | A B C D F G J K Q     | near-universal                                                                                    | heavy-atom (or any-atom) distance from ligand   | **4.0 Å** (K), **4.5 Å** (C D G Q), **5.0 Å** (A B F J). F sweeps 2–10 Å                                                                                                                                                |
| 3   | **Ligand validity / exclusion list**                                                        | A B C F G H K R       | near-universal                                                                                    | Binding MOAD hand curation, or a HET blacklist  | MOAD "biologically relevant" (A B G); ≥5 atoms + 9-code blacklist (C); ≥10 heavy atoms (F); ≤100 Da or 620-code list (G); small molecules only (K)                                                                      |
| 4   | **Redundancy clustering (leakage control)**                                                 | A B C G J K L M N     | near-universal                                                                                    | BLASTClust / CD-HIT / MMseqs2 / UniRef          | 40% (A B C), 30% (L M N), 95% (G J O), 90% (H), UniRef50 (K); tighter for CV splits: 10% (C), 55% train↔test (B)                                                                                                        |
| 5   | **Sequence identity between the two pair members**                                          | B C D E F G           | near-universal                                                                                    | pairwise identity, or shared UniProt AC         | 100% (B G), exact ± 5 terminal residues (F), same UniProt AC (C D E)                                                                                                                                                    |
| 6   | **A required conformational-change magnitude**                                              | A B C O P             | common                                                                                            | _four incompatible metrics_                     | pocket score bad→good, Fpocket + ConCavity (A); LIGSITE volume ≥ 20 Å³ larger in holo (B); pocket RMSD > 2 Å (C); max Cα RMSD as diversity (O)                                                                          |
| 7   | **Missing / disordered residues near the site**                                             | B C K L M R           | common                                                                                            | gap length, observed-residue count, remodelling | gaps > 3 residues rejected (B); apo/holo pocket length must match, ≥ 50 observed residues vs UniProt (C); ProMod3 + lDDT ≥ 0.8 (K); no missing residues in the site (L M); identify unmodelled within 6–8 Å (R)         |
| 8   | **Global fold / superposition sanity**                                                      | C D E F O             | common                                                                                            | TM-align, MAMMOTH, or crystal-form matching     | TM-score ≥ 0.5, site centres ≤ 4 Å apart, Rg change ≤ 20% (C); TM-align (D E); same space group + cell ≤ 1 Å/1° (F); TM/GDT-TS/GDT-HA (O)                                                                               |
| 9   | **Occupancy and alternate conformations**                                                   | B F Q R               | common                                                                                            | altloc/occupancy fields; qFit                   | multi-conformer X-ray excluded (B); altloc/partial-occupancy ligands counted and B-factor-normalised (F); min average occupancy 1.0 (Q); flag occupancy < 1.0 (R)                                                       |
| 10  | **Covalent ligands**                                                                        | C G H K R             | common — and **contested**                                                                        | `_struct_conn` covale records                   | **excluded** by H G K R; **kept** by C                                                                                                                                                                                  |
| 11  | **Biological assembly / oligomeric state**                                                  | B C E K O             | common — and **contested**                                                                        | REMARK 350 / `pdbx_struct_assembly`, PISA       | monomeric assembly required (B); biological assemblies downloaded (K); interface pockets deliberately **included** (C E — 24% of sites); annotated not filtered (O)                                                     |
| 12  | **Experimental method restriction**                                                         | B F K O               | common                                                                                            | `_exptl.method`                                 | X-ray only (F); NMR removed as a side effect of the resolution filter (B); X-ray + NMR as conformers (O); PDB-format-only requirement drops mmCIF-only entries (K). **No source explicitly admits or excludes cryo-EM** |
| 13  | **Construct differences: mutations, tags, chimeras**                                        | B F G R               | common — but only _indirectly_                                                                    | pairwise sequence identity                      | 100% identity (B G), exact sequence ± 5 termini (F), "keep deviations to a minimum" (R). **No source reads `_struct_ref_seq_dif`**                                                                                      |
| 14  | **Numbering reconciliation (auth ↔ label ↔ UniProt)**                                       | B C D K               | common                                                                                            | SIFTS, or explicit alignment                    | SIFTS residue-level mapping (C D); align UniProt to PDB SEQRES (K); B _admits failing this_: "it may have excluded some structures with mismatched PDB residue numbering"                                               |
| 15  | **Ligand electron density (RSCC / RSR / OMIT)**                                             | Q R S T               | **idiosyncratic to the crystallography-quality literature; absent from every apo–holo benchmark** | EDS / PDB-REDO validation reports, OMIT maps    | RSCC ≥ 0.9 and RSR ≤ 0.4 (Q); RSCC > 0.90 and ≥ 90% of ligand atom centres covered (R); "distinct positive OMIT density for the entire modelled ligand" (T)                                                             |
| 16  | **Choice among multiple qualifying apo structures**                                         | B C F                 | common, rarely discussed                                                                          | an explicit tie-break rule                      | maximal pocket RMSD (C); smallest resolution difference (F); lower-RMSD member dropped (B)                                                                                                                              |
| 17  | **Modified / non-canonical residues**                                                       | B D H O               | common                                                                                            | MODRES / `pdbx_struct_mod_residue`              | removed except MSE/SEC → Cys/Met (B); optionally treated as ligands (D); glycosylation/catalytic metal/HEME are "part of the protein" (H); annotated (O)                                                                |
| 18  | **R-free / re-refinement of the deposited model**                                           | F Q S                 | idiosyncratic                                                                                     | phenix.refine, PDB-REDO                         | re-refine, reject if R-free rises > 2.5% (F); R-free as a scoring input (Q); re-refined for consistency (S)                                                                                                             |
| 19  | **Crystal-packing contacts at the site**                                                    | F R                   | idiosyncratic                                                                                     | symmetry-mate contact search                    | packing atoms within 6 Å of any ligand atom must be identified (R); matched space group + unit cell as an indirect control (F)                                                                                          |
| 20  | **Site/ligand correspondence check** (does the annotated site actually contain the ligand?) | K L                   | idiosyncratic — high value                                                                        | centroid distance; component alias              | modulator-to-nearest-pocket centre > 10 Å → drop (L); resolve chemical component alias when ASD and PDB disagree (K)                                                                                                    |
| 21  | **Obsolete / superseded entries; ID drift**                                                 | K                     | idiosyncratic                                                                                     | PDB GraphQL / status API                        | update obsolete PDB IDs, drop entries no longer in the PDB, drop PDB↔UniProt ID discrepancies (K)                                                                                                                       |
| 22  | **Insertion codes**                                                                         | B                     | idiosyncratic                                                                                     | `pdbx_PDB_ins_code`                             | "removed chains with alphabetic residue insertion codes" (B)                                                                                                                                                            |
| 23  | **A matched negative / control set built by identical criteria**                            | A F                   | idiosyncratic — and the most under-used idea in the corpus                                        | same pipeline, no ligand difference             | 705 concave surface patches (A); **293 apo–apo pairs** (F)                                                                                                                                                              |
| 24  | **Species / gene identity**                                                                 | —                     | **checked by nobody explicitly**                                                                  | implied by UniProt AC or 100% identity          | see §6.2                                                                                                                                                                                                                |
| 25  | **Statistical null or random baseline for evaluation**                                      | A (partial)           | **near-absent**                                                                                   | —                                               | A compares three site classes with p-values and states a random-residue baseline; B C K L M N report metrics only. See [`evaluation-protocol-lit.md`](evaluation-protocol-lit.md)                                       |

J (CASBench) is absent from row 1 deliberately: it states no resolution filter, substituting
membership of ASD **and** the Catalytic Site Atlas as its quality gate.

### 3.1 The minimal defensible set

If a benchmark can only justify a handful of checks, the corpus supports this ordering.
Rows 1–5 are what a reviewer will assume you did.

1. Resolution ceiling, stated per member, plus the resolution _difference_ if the pair is
   compared quantitatively (F is the only source that constrains the difference, and it is
   the only source whose comparison is quantitative at side-chain resolution).
2. Ligand-contact cutoff, stated with its atom selection, plus at least one neighbouring
   value so the reader can see the label set is not cutoff-tuned.
3. A published or explicitly enumerated ligand-validity list, including the _tolerated_ set
   at the site — the whitelists disagree (B tolerates only HOH/DOD/Na/Cl/K; C blacklists
   nine codes and keeps sugars).
4. Pair sequence identity, with the differences enumerated rather than merely thresholded.
5. Redundancy clustering, if there is more than one target family.
6. An explicit conformational-change measure, chosen and justified — not inherited.
7. A tie-break rule for which apo structure was used, because the apo label does not pin it
   down ([`apo-holo-definition.md`](apo-holo-definition.md) §3.3).

---

## 4. Metrics used to characterise a pair

Collected because "how the field measures the pair" is a separate question from "how the
field filters it".

**Contact cutoff for the pocket.** 4.0 Å (K), 4.5 Å heavy-atom (C D G Q), 5.0 Å (A B F J).
A uses _any_ atom, not heavy atom — a detail that changes label counts and is easy to miss.
F is the only source that publishes a sensitivity sweep (2–10 Å) `[VERIFIED-FULLTEXT]`.

**RMSD.** Four distinct quantities travel under the name:

- _Global Cα RMSD_ after global superposition — O (via MAMMOTH), P.
- _Pocket / binding-site RMSD_, all-atom, over the pocket residues — C (threshold 2 Å), A
  (reported range 0.45–22.45 Å).
- _Per-position RMSD_ — O (ProFit).
- _Cryptic-site RMSD_ used as a ranking key rather than a filter — B.

None of C, A or B states in the retrieved text whether the pocket RMSD is computed after a
_global_ or a _local_ superposition. C does state that a global structural alignment precedes
the binding-site-centre distance check, which implies global for that metric at least
`[VERIFIED-FULLTEXT]`. **This is a genuine ambiguity in the published protocols** — a global
fit inflates local RMSD when a distal domain moves, and a local fit hides it.

**Pocket volume / pocket score.**

- **Fpocket** — A (with ConCavity), and the whole allosteric branch (L M N) as the pocket
  generator.
- **ConCavity** — A only.
- **LIGSITE** — B, with published parameters (min rank 7, grid 0.7 Å, probe 1.4 Å, min
  cluster 3 points; grid points assigned to residues within 5 Å).
- **P2Rank** — C, as a baseline predictor and as the origin of its ignored-group list.
- **CASTp, POVME** — not used by any retrieved source. B mentions fpocket druggability
  scoring as a labelling alternative "since druggability scores consider not only the
  geometry of a pocket but also the chemical environment" `[VERIFIED-FULLTEXT]`.

**Crypticity.** Three published operationalisations, mutually incompatible:

- pocket-score transition, Fpocket + ConCavity, apo bad → holo good (A);
- pocket-volume gain, LIGSITE, ≥ 20 Å³ (B);
- pocket RMSD > 2 Å, calibrated by manual inspection of the [1.5, 2] Å borderline (C).

A fourth, used in this repo and not found in the corpus, is **ligand transplantation**: carry
the holo ligand into the apo frame and count steric clashes. It is a direct test of "does the
pocket exist in the apo input", where all three published measures are proxies. If we report
it we should say it is not a field-standard metric.

**Other pair descriptors.** TM-score (C D E N O), GDT-TS / GDT-HA (O), radius of gyration
change (C), binding-site-centre displacement after superposition (C), SASA (D), B-factor
Z-scores (O), ligand B-factor normalised by mean Cα B-factor (F), order parameters (F).

---

## 5. Is there a published term for the site-relative sense of "apo"?

**No. There is no coined, agreed term in the retrieved corpus.**

Searches this session: `"apo with respect to" AND "binding site"` (4 hits, none definitional),
`"pseudo-apo" OR "quasi-apo" OR "site-specific apo" OR "locally apo"` (20 hits, none on
point), `"apo with respect to the binding site" OR "apo with respect to this site" OR
"site-specific apo state" OR "apo form of the binding site"` (5 hits, none definitional),
`"apo state of the binding site"` (8 hits, all incidental usage), `"apo binding site"`
(24 hits), `"apo pocket" OR "holo pocket"` (43 hits, all informal). None of these introduces
or defines a term `[VERIFIED-ABSTRACT — search records, not full texts]`.

**The closest published phrasings**, in descending order of how load-bearing they are:

1. > "listed as holo or apo **respective to the presence or absence of ligands in the defined
   > binding site(s)**" — AHoJ, [10.1093/bioinformatics/btac701](https://doi.org/10.1093/bioinformatics/btac701) `[VERIFIED-FULLTEXT]`
2. > "labeled as HOLO (bound) or APO (unbound) **with respect to the binding site** defined by
   > the ligand" — apoholo.cz/db documentation, no DOI `[VERIFIED-FULLTEXT, NO DOI]`
3. > "the mapped **pockets are annotated as apo or holo**" — AHoJ-DB,
   > [10.1016/j.jmb.2024.168545](https://doi.org/10.1016/j.jmb.2024.168545) `[VERIFIED-ABSTRACT]`
4. > "the candidate pockets are annotated as holo or apo, **in reference to the particular
   > query pocket**" — apoholo.cz help page, no DOI `[VERIFIED-FULLTEXT, NO DOI]`
5. > "holo ligands with **ligand-free apo binding sites**" — PocketMiner,
   > [10.1038/s41467-023-36699-3](https://doi.org/10.1038/s41467-023-36699-3) `[VERIFIED-FULLTEXT]`
6. The AHoJ-DB title itself: _"a PDB-wide assignment of apo & holo relationships **based on
   individual protein–ligand interactions**"_ — the phrase "based on individual protein–ligand
   interactions" is the field's nearest thing to naming the concept `[VERIFIED-ABSTRACT]`.

**Recommended usage.** The construction the field actually uses is _adjectival with an
explicit referent_: "apo **with respect to** \<site\>", or "**apo pocket** / **holo pocket**"
when the referent is obvious. Both are attestable. The noun phrase "**apo–holo relationship
of a binding site**" (AHoJ-DB) is the most precise published form. This repo's term
"site-apo" remains a coinage — it should be introduced with a gloss and a citation to AHoJ on
first use, not presented as standard vocabulary.

Two further terminological hazards worth stating in any report:

- Classical enzymology (IUPAC/NC-IUBMB) uses apo/holo for **cofactor** occupancy, so a
  cofactor-bound structure is _holo_ unconditionally — the opposite label to the
  structural-bioinformatics site-relative sense. See [`apo-holo-definition.md`](apo-holo-definition.md) §1.4.
- "Unbound" is used interchangeably with "apo" by A ("proteins in ligand-free (unbound)
  conformations") and carries the same ambiguity.

---

## 6. What a benchmark builder gets wrong

Ranked by how likely the error is to survive review undetected. Items 1–4 are the ones the
PDB-wide pipelines never hit, because a pipeline reads the file and a human reads a table.

### 6.1 Trusting a table instead of the file

No published pipeline hand-enters a PDB ID / ligand / residue list; all of them read
identifiers programmatically. AlloBench is the only source that says out loud what happens
when the table and the file disagree — obsolete IDs, PDB↔UniProt discrepancies, and
"discrepancies between the allosteric sites listed in ASD and the location of the allosteric
modulator in the PDB structure… resolved by obtaining the chemical component alias"
`[VERIFIED-FULLTEXT]`. **A hand-curated four-target benchmark has no such step unless it
builds one.** The check that catches it: verify the ligand's chemical component ID is present
in the holo entry, and that the entry's polymer is the intended gene product, before anything
else.

### 6.2 Species and gene identity — checked by nobody, assumed by everybody

Every pipeline gets this free: AHoJ/AHoJ-DB/CryptoBench group by UniProt accession,
PocketMiner and Wankowicz require ~100% sequence identity. **No source in the corpus states
an explicit species or gene check**, because none needs one. A hand-assembled pair has no such
guarantee, and the failure is silent — two structures can be labelled "cardiac myosin" in a
table and be different genes from different organisms. The cheap substitute for the field's
implicit check: resolve both members to a UniProt accession via SIFTS and require equality,
then report the pairwise identity.

### 6.3 Residue numbering

Three conventions coexist per entry (`auth_seq_id`, `label_seq_id`, UniProt index) and the
deposited `_struct_ref_seq` can be wrong. C and D route everything through SIFTS; K aligns
UniProt to the PDB SEQRES explicitly; **B admits the bug** — "as this step did not use a
sequence alignment but instead relied on matching PDB residue numbers, it may have excluded
some structures with mismatched PDB residue numbering" `[VERIFIED-FULLTEXT]`. If a
peer-reviewed Nature Communications pipeline states this as a known defect, a hand-built
benchmark should assume it has the same defect until it proves otherwise.

### 6.4 Confusing "apo" with "pocket-closed"

> "Sun et. al. observed that some proteins in the CryptoSite set had additional apo structures
> in which the pocket was open." — B `[VERIFIED-FULLTEXT]`

Being ligand-free at the site does not entail the pocket is closed. C and F both encode
tie-break rules precisely because the apo choice is a free parameter (maximal pocket RMSD;
smallest resolution difference). **A benchmark that names one apo PDB per target has made a
conformational selection its definition does not justify, and must say so.**

### 6.5 Deleting the ligand and calling the structure apo

Not stated as a rule anywhere in the corpus — but it follows from every pocket-based
crypticity measure (A B C): the _conformation_ carries the information, not the coordinates
of the ligand. B enforces it operationally by requiring the apo structure to have no ligand
within 5 Å of the holo-defined site _in the deposited file_. Removing HETATM records during
cleaning does not satisfy that clause.

### 6.6 Never looking at the ligand's electron density

§0 finding 2. Iridium's number is the argument: of 728 structures used to validate docking
software, "only 17% were found to be acceptable" `[VERIFIED-ABSTRACT]`. For a four-target
benchmark this is a cheap check — the PDB validation report gives ligand RSCC/RSRZ per entry,
and R's threshold (RSCC > 0.90, density covering ≥ 90% of ligand atom centres) is a published
bar to state compliance or non-compliance against. It is also the single most defensible
place to _exceed_ field standard, since the cryptic-pocket benchmarks skip it entirely.

### 6.7 Reporting AUC-ROC alone under low prevalence

Both B and C publish the gap on their own predictors (ROC 0.83 ± 0.04 vs PR 0.44 ± 0.12;
AUC 0.86 vs AUPRC 0.36) `[VERIFIED-FULLTEXT]`, and neither draws the conclusion. See
[`evaluation-protocol-lit.md`](evaluation-protocol-lit.md) and `../README.md` §5.

### 6.8 Assuming a monomer

24% of biologically relevant binding sites sit at a chain interface (E)
`[VERIFIED-ABSTRACT]`. B handles this by _excluding_ non-monomeric assemblies; C and E by
_supporting_ multi-chain pockets. Both are defensible; silence is not. The related trap is
using the asymmetric unit where the biological assembly is meant — K downloads biological
assemblies explicitly `[VERIFIED-FULLTEXT]`.

### 6.9 Treating 1 Å as a conformational change

P's survey of 521 pairs finds most proteins change by < 1 Å on ligand binding
`[VERIFIED-ABSTRACT]`; C sets its crypticity floor at 2 Å pocket RMSD after manual inspection
of the 1.35–1.93 Å borderline `[VERIFIED-FULLTEXT]`. A pair with ~1 Å global RMSD is, on the
published priors, _unchanged_.

### 6.10 Having no control set built by the same pipeline

F's 293 apo–apo pairs and A's 705 concave surface patches are the only matched negatives in
the corpus. Without one, there is no measurement of how much apparent apo↔holo difference is
crystallographic noise rather than ligand response.

---

## 7. Not established

Phrased so a later agent knows what would close each.

1. **Whether the pocket RMSD in CryptoBench (and the cryptic-site RMSD in PocketMiner) is
   computed after global or local superposition.** Decisive for reproducing their crypticity
   thresholds. _Closes by:_ reading `github.com/skrhakv/CryptoBench` and the AHoJ-DB metric
   definitions, or the AHoJ-DB body (paywalled).
2. **CryptoSite's resolution cutoff, ligand size floor and ion policy.** In the SI Text, which
   PMC gates behind a JavaScript proof-of-work challenge. _Closes by:_ institutional access to
   the JMB PDF, or a browser session against the NIHMS supplement.
3. **AHoJ's default ignore list and minimum-mapped-binding-residue percentage from a primary
   source.** The 4.5 Å default and the 1% MBR default reached me through search-result text
   and through CryptoBench's restatement, not from a page or supplement I read directly.
   _Closes by:_ the AHoJ Supplementary Information, or `github.com/cusbg/AHoJ-project` source.
4. **Whether AHoJ-DB's input interactions come from BioLiP2** (recorded in
   [`apo-holo-definition.md`](apo-holo-definition.md) §1.1 but not re-derived this session;
   the abstract says only "biologically relevant protein-ligand interactions").
5. **Iridium's numeric criteria.** Abstract only. The LiveCoMS guide restates its resolution
   threshold (< 3.5 Å) and an RSCC bar (> 0.90) but attributes only the former to Iridium.
6. **ASD's evidence requirement for admitting an allosteric site**, and the protocol behind
   its "1688 allosteric apo/holo paired structures". Both are citations to earlier work in
   every ASD release text read (v3.0, 2019). _Closes by:_ the cited Lu et al. 2014 protocol.
7. **ASBench's inclusion criteria** — "a complex process" is all the abstract offers;
   [10.1093/bioinformatics/btv169](https://doi.org/10.1093/bioinformatics/btv169) is paywalled.
   This matters because ASBench is the training set for most of the allosteric branch.
8. **MolMovDB's pairing and change-quantification criteria.** The Europe PMC full-text XML
   endpoint returned 404 for PMC165551 this session. CoDNaS covers the same ground and was
   readable.
9. **Whether any apo–holo benchmark checks the ligand's electron density.** Established as
   _not found_ across A B C D E F H I J K L M N O, by targeted extraction — but absence
   established by targeted search is weaker than absence established by full reading.
10. **Whether any source besides F and R considers crystal packing at the site.** Same caveat.

---

## Retrieval record

All Europe PMC REST (`/search`, `/{PMCID}/fullTextXML`), 2026-08-20, except: CryptoSite body
via `pmc.ncbi.nlm.nih.gov/articles/PMC4794384/`; LiveCoMS body via
`pmc.ncbi.nlm.nih.gov/articles/PMC9662604/`; AHoJ documentation via `apoholo.cz` and
`raw.githubusercontent.com/ioChris/AHoJ`; Iridium and AHoJ-DB abstracts via the Europe PMC
`core` search record. Sources G (Clark 2019) and the AHoJ-DB BioLiP2 attribution are carried
from [`apo-holo-definition.md`](apo-holo-definition.md) and are `[UNVERIFIED]` in this
document.
