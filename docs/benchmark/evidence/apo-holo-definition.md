# What "apo/holo pair" formally means — evidence review

**Question.** The benchmark input layer provisionally adopts a **site-apo** reading: a
structure is _apo_ with respect to the pocket of interest even if other ligands or
cofactors are bound elsewhere. Alternatives rejected: (a) globally ligand-free,
(b) merely drug-free.

**Scope.** Literature retrieved 2026-08-20 via Europe PMC. Every claim below carries a
DOI and a verification tag:

- `[VERIFIED-FULLTEXT]` — quoted from the open-access full text retrieved this session.
- `[VERIFIED-ABSTRACT]` — from the abstract record retrieved this session; full text not
  available (paywalled) or not read.
- `[UNVERIFIED]` — inferred, secondhand, or from a non-DOI source. Treat as a lead, not
  evidence.

Nothing here is recalled from memory. Where a source was silent, §6 says so by name.

---

## 1. The field does not have one definition. It has at least four.

### 1.1 Site-relative (supports our reading)

> "each one is listed as holo or apo respective to the presence or absence of ligands in
> the defined binding site(s)"

AHoJ, DOI [10.1093/bioinformatics/btac701](https://doi.org/10.1093/bioinformatics/btac701)
`[VERIFIED-FULLTEXT]`. This is the clearest statement in the retrieved corpus that apo
is a property of a _site_, not of a _structure_. AHoJ takes a query structure plus
user-specified ligands, maps that binding site onto every other structure sharing the
UniProt accession, and classifies each mapped site independently.

The same paper acknowledges the multi-site situation that makes the distinction
necessary:

> "proteins often bind several ligands, and even within the same protein, different
> structures can bind different ligands in the same or in different binding sites"

DOI [10.1093/bioinformatics/btac701](https://doi.org/10.1093/bioinformatics/btac701)
`[VERIFIED-FULLTEXT]`. Note the limit of this evidence: the paper states the multi-ligand
situation and classifies per site, but **gives no worked example of one structure labelled
apo for site A and holo for site B**. The inference is ours, not theirs.

AHoJ-DB scales the same logic PDB-wide: "the binding pocket is captured and mapped across
existing structures within the same UniProt, and the mapped pockets are annotated as apo
or holo, based on the presence or absence of ligands" — per pocket, not per structure.
DOI [10.1016/j.jmb.2024.168545](https://doi.org/10.1016/j.jmb.2024.168545)
`[VERIFIED-ABSTRACT]`. Input interactions come from the redundant set of BioLiP2,
excluding peptide and nucleic-acid ligands. Reported statistics: ~24% of binding sites
sit at an interface of two or more chains, and **fewer than 50% of processed binding
sites have any apo form in the PDB at all**.

### 1.2 Pocket-formation (CryptoSite)

> "a cryptic site can therefore be defined as a site that forms a pocket in a holo
> structure, but not in the apo structure"

Cimermancic et al. 2016, DOI [10.1016/j.jmb.2016.01.029](https://doi.org/10.1016/j.jmb.2016.01.029)
`[VERIFIED-ABSTRACT]`. This defines _cryptic_, and only presupposes apo/holo — it does not
define them. The apo/holo terms are used as if self-evident. Their operational rules are
in the paywalled body (see §6).

### 1.3 Global ligand-free, with a size threshold (contradicts our reading)

Wankowicz et al. 2022 define the two states over the whole structure:

> holo "contained at least one ligand, defined as any HETATM residue with 10 or more heavy
> atoms, excluding common crystallographic additives"; apo = "structures without a ligand
> bound"

DOI [10.7554/eLife.74114](https://doi.org/10.7554/eLife.74114) `[VERIFIED-FULLTEXT]`. There
is no site qualifier. A structure with NAD, FAD, heme or GDP bound anywhere is holo under
this rule, regardless of the pocket under study. Ions and small additives do not trigger
holo status because of the ≥10-heavy-atom floor — so this is not reading (a) in its pure
form either. It is a fourth position: _globally free of anything drug-sized_.

### 1.4 Classical enzymology (contradicts our reading, most sharply)

> "The inactive form of such enzymes is called an apoenzyme, while the active form is
> called a holoenzyme."

Biochemical Nomenclature Committee of IUPAC and NC-IUBMB, Newsletter 2023,
<https://iubmb.qmul.ac.uk/newsletter/2023.html> — **no DOI issued** `[VERIFIED-FULLTEXT,
NO DOI]`. Under the original sense of the prefixes, apo/holo refer to _cofactor_ occupancy,
full stop. A cofactor-bound structure is holo by construction. The nomenclature page did
not define apoprotein/holoprotein, only apoenzyme/holoenzyme.

This is the deepest disagreement in the set: the structural-bioinformatics site-relative
usage and the enzymological usage assign **opposite labels to the same structure** whenever
a cofactor is present away from the pocket of interest. Both are current. Neither is wrong.
A benchmark that says "apo" without saying which sense it means is ambiguous, and this
project's targets (nucleotide-bound KRAS, ATP-site kinases, nucleotide-bound myosin) sit
exactly on the fault line.

---

## 2. How the standard benchmarks operationalise it

### 2.1 CryptoBench (2024) — built on AHoJ-DB, therefore site-relative by inheritance

DOI [10.1093/bioinformatics/btae745](https://doi.org/10.1093/bioinformatics/btae745), all
`[VERIFIED-FULLTEXT]`.

| Clause                   | Value                                                                                                                            |
| ------------------------ | -------------------------------------------------------------------------------------------------------------------------------- |
| Source pool              | AHoJ-DB, 14 054 029 apo–holo pairs (August 2024)                                                                                 |
| Binding-site definition  | AHoJ default: protein residues within **4.5 Å** of the specified ligand's atoms                                                  |
| Resolution               | worse than **2.5 Å** filtered out                                                                                                |
| Pocket correspondence    | records where "pocket length in the apo state and holo state did not match were filtered out"                                    |
| Global fold match        | minimum **TM-score 0.5**, so that "the conformational changes are restricted to the binding site"                                |
| Site co-location         | "maximum distance threshold of **4 Å** between the centers of apo and holo binding sites, after the global structural alignment" |
| Compactness              | "up to a **20%** change in the radius of gyration from the holo state"                                                           |
| Sequence coverage        | "at least **50** observed residues from the protein must overlap with its UniProt sequence"                                      |
| Ligand size floor        | "excluded ligands where the number of atoms is less than **5**"                                                                  |
| Ligand blacklist         | HOH, DOD, WAT, UNK, ABA, MPD, GOL, SO4, PO4                                                                                      |
| Explicitly **kept**      | sugars (MAN, GLC, NAG) and covalently attached ligands                                                                           |
| Redundancy               | UniProt sequences clustered at **40%** identity                                                                                  |
| CV split leakage control | second clustering at **10%** identity                                                                                            |
| Crypticity threshold     | "pocket RMSD bigger than **2 Å** as a suitable threshold for differentiating between cryptic and regular binding sites"          |

Note the two design choices that cut against a naive apo definition: **sugars are kept as
ligands** (so a glycosylated structure is holo at that site) and **covalent ligands are
kept**.

Grouping is by UniProt ID. That means point mutants and different constructs of the same
gene product are pooled, since they share a UniProt accession — but the paper does not say
this explicitly (§6).

### 2.2 PocketMiner (2023) — site-local exclusion, near-exact sequence match

DOI [10.1038/s41467-023-36699-3](https://doi.org/10.1038/s41467-023-36699-3), all
`[VERIFIED-FULLTEXT]`.

The apo criterion is explicitly **scoped to the site**:

> "We removed apo candidate structures with ligands (excluding water, heavy water, sodium,
> chloride, and potassium) within **5 Å** of all MOAD-assigned biologically relevant
> residues in the holo candidate structure."

Nothing in the retrieved text requires the apo structure to be ligand-free elsewhere. This
is the second independent source supporting site-relative scope. But observe how narrow the
tolerated set is: **only water, heavy water, Na⁺, Cl⁻, K⁺**. Mg²⁺, Zn²⁺, Ca²⁺, GDP, NAD and
every cofactor count as ligands _at the site_.

Other clauses:

| Clause                   | Value                                                                                              |
| ------------------------ | -------------------------------------------------------------------------------------------------- |
| Candidate generation     | BLAST against Binding MOAD; hits below **90%** amino-acid identity removed                         |
| Resolution               | must be at least **2.5 Å**                                                                         |
| Excluded                 | multi-conformer X-ray structures; structures without a monomeric biological unit                   |
| Loops / gaps             | "We removed chains with gaps longer than **3** residues"                                           |
| Pocket-opening magnitude | apo LIGSITE pocket volume over the ligand-lining residues must be smaller than holo by **≥20 Å³**  |
| Label threshold          | **40 Å³** pocket-volume change for a residue to count as participating                             |
| LIGSITE settings         | min rank 7, grid 0.7 Å, probe 1.4 Å, cluster size 3; pocket points assigned to residues within 5 Å |
| Redundancy               | proteins removed when pairwise identity exceeds **40%** (lower cryptic-site RMSD dropped)          |

**Mutations and constructs — the strictest rule found anywhere:**

> "...less than **100%** sequence identity to their respective holo candidate structures,
> except for mismatches between selenocysteine and cysteine and selenomethionine and
> methionine."

with two admitted weaknesses, quoted because they matter for anyone reusing the set:

> "This step did not check for differences between unresolved terminal residues, which can
> result from variation in the placement of histidine tags."

> "As this step did not use a sequence alignment but instead relied on matching PDB residue
> numbers, it may have excluded some structures with mismatched PDB residue numbering."

So: **no mutations tolerated**; terminal-tag differences tolerated by accident; residue-number
mismatch causes silent false-negative exclusions.

**Their critique of CryptoSite** (relevant to any reuse of that set):

> "the CryptoSite set contains relatively few proteins in which large conformational changes
> are necessary for pocket formation"

> "The PDB has roughly doubled in size since the version used to generate the CryptoSite set
> was downloaded, and Sun et. al. observed that some proteins in the CryptoSite set had
> additional apo structures in which the pocket was open."

That second sentence is the most important line in this document for our purposes. It says
the apo/holo _label is not a property of the pair_ — it is a property of **which apo
structure you happened to pick**. See §3.3.

CryptoSite size, secondhand: "Cimermancic et. al. previously identified **93** apo-holo
protein structure pairs containing cryptic pockets" DOI
[10.1038/s41467-023-36699-3](https://doi.org/10.1038/s41467-023-36699-3)
`[VERIFIED-FULLTEXT]` (as a statement _about_ DOI 10.1016/j.jmb.2016.01.029, which we could
not read).

### 2.3 Clark, Benson, Smith & Carlson 2019 — hybrid, and the most instructive case

DOI [10.1371/journal.pcbi.1006705](https://doi.org/10.1371/journal.pcbi.1006705)
`[VERIFIED-FULLTEXT]`. Dataset: 305 protein sequences, 2369 holo and 1679 apo crystal
structures.

Two clauses, operating at **different scopes**:

1. Global: "HETs contained in the structure files were required to have a molecular weight
   **≤ 100 Daltons** or be present in appropriate filtering lists" — the lists cover
   "sugars, small organic molecules, membrane components, small metabolites, salts, buffers,
   solvents, crystal additives, cryoprotectants, detergents, and metal ions" (**620** HET
   groups, derived from Binding MOAD curation).
2. Site-local: "Any structures containing HET material apart from water (HOH) within
   **4.5 Å** of any unified binding site residue were removed."

Other criteria: resolution **2.5 Å or better**; clustering at **100%** identity in both
directions, then **95%**; families with fewer than two holo (resp. apo) structures dropped;
"structures with more than one valid ligand were excluded" (binary complexes only);
covalently attached ligands **excluded** — the opposite of CryptoBench's choice.

**Unresolved tension in this source.** Clause 1 as quoted is a restriction on _every_ HET in
the file, which would reject a structure with a large cofactor bound at a distal site — i.e.
it is a global-apo clause. The interpretation that "apo structures can contain small
molecules and cofactors anywhere, but nothing biologically relevant near the binding site"
is a _gloss produced during retrieval_, not a sentence in the paper. We could not settle
which reading is correct from the text retrieved. Flagged in §6. This matters: Clark et al.
is either a third vote for site-apo or a second vote for global-apo.

### 2.4 ASD — Allosteric Database

Consistent across five releases, `[VERIFIED-ABSTRACT]` in each case, is one definitional
commitment: an allosteric site is one **"topographically distinct from the orthosteric
site"**.

- ASD 2011, DOI [10.1093/nar/gkq1022](https://doi.org/10.1093/nar/gkq1022) — 336 allosteric
  proteins, 8095 modulators.
- ASD v2.0, DOI [10.1093/nar/gkt1247](https://doi.org/10.1093/nar/gkt1247) — 1286 proteins;
  907 allosteric site–modulator complexes; ">200 structural pairs of orthosteric/allosteric
  sites".
- ASD v3.0, DOI [10.1093/nar/gkv902](https://doi.org/10.1093/nar/gkv902) — "structural
  mechanisms of more than 1600 allosteric actions were elucidated by a **comparison of site
  structures before and after the binding of a modulator**". This is an apo/holo comparison
  in all but name, and it is **modulator-relative**, i.e. site-relative in spirit.
- ASD 2019, DOI [10.1093/nar/gkz958](https://doi.org/10.1093/nar/gkz958) — >10 000 potential
  allosteric sites; 1312 somatic missense mutations at allosteric sites.
- ASD2023, DOI [10.1093/nar/gkad915](https://doi.org/10.1093/nar/gkad915) — 66 589 potential
  allosteric sites computed with **AlloSitePro** over the human proteome ("Human Allosteric
  Pocketome"); ">70% of the proteins revealed allosteric sites with a high potential ...
  (allosite score > 0.6)". The Allosteric PPI dataset records "the PPI crystal structure
  (**apo or holo**), residues at the allosteric site and the PPI interface" — so ASD carries
  the apo/holo attribute per entry, `[VERIFIED-FULLTEXT]`.

**ASD does not publish, in the text we read, what evidence qualifies a site for entry** (see
§6), nor any required distance between allosteric and orthosteric site beyond the qualitative
"topographically distinct".

### 2.5 ASBench

235 unique allosteric sites ("Core set") and 147 structurally diverse sites
("Core-Diversity set"), assembled "through a complex process". DOI
[10.1093/bioinformatics/btv169](https://doi.org/10.1093/bioinformatics/btv169)
`[VERIFIED-ABSTRACT]`. Not open access; the actual inclusion criteria behind "a complex
process" are unknown to us.

### 2.6 A recent allosteric-site ML benchmark, for contrast

Riedlová et al. 2026, DOI [10.1021/acs.jctc.6c00427](https://doi.org/10.1021/acs.jctc.6c00427)
`[VERIFIED-FULLTEXT]`. Built on KinCoRe rather than ASD; uses **holo structures only**;
labels residues with heavy atoms within **4 Å** of any ligand heavy atom; resolution ≤3.0 Å;
ligand atoms with occupancy <0.5 excluded; >30% sequence identity removed for leakage
control. Type IV (allosteric) sites are scarce even in a kinase-scale set: 675 structures vs
7604 for Type I. Two things to take from this: (i) the 4–4.5 Å ligand-contact cutoff is
near-universal across the field; (ii) allosteric benchmarks routinely **skip the apo problem
entirely** by predicting from holo, which is precisely the shortcut CryptoBench was created
to close.

---

## 3. Evidence AGAINST the site-apo reading

Collected deliberately. This section is the point of the review.

### 3.1 A major, careful benchmark uses global-apo

Wankowicz et al. define apo as "structures without a ligand bound" with no site qualifier,
counting any HETATM of ≥10 heavy atoms other than common crystallographic additives, DOI
[10.7554/eLife.74114](https://doi.org/10.7554/eLife.74114) `[VERIFIED-FULLTEXT]`. If we adopt
site-apo, we are choosing against a peer-reviewed 743-pair benchmark that chose otherwise.
The reason matters: their scientific question was _what does ligand binding do to side-chain
heterogeneity_, and any second ligand anywhere is a confound for that question. **Our question
— how does a signal propagate through a residue network — has the same confound structure.**
A cofactor bound at a distal site perturbs the very network we are modelling. This is the
strongest argument against site-apo that we found, and it is an argument from purpose, not
from nomenclature.

### 3.2 Classical nomenclature inverts the label

Under IUPAC/NC-IUBMB usage, cofactor-bound = holo, unconditionally
(<https://iubmb.qmul.ac.uk/newsletter/2023.html>, no DOI) `[VERIFIED-FULLTEXT, NO DOI]`. A
reviewer trained as an enzymologist will read "apo cardiac myosin" as _nucleotide-free
myosin_ and will regard an ADP·Pi-bound structure described as apo as an error. Cost of
ignoring this is reputational, not technical, but it is real, and it is cheap to defuse with
one sentence of explicit definition in the report.

### 3.3 The apo label is not a property of the pair — it is a property of the chosen structure

> "Sun et. al. observed that some proteins in the CryptoSite set had additional apo
> structures in which the pocket was open."

DOI [10.1038/s41467-023-36699-3](https://doi.org/10.1038/s41467-023-36699-3)
`[VERIFIED-FULLTEXT]`. This undercuts _all_ readings, including ours. Being "apo at the site"
does not entail the pocket is closed, and the same protein can supply an apo structure with
the pocket open and another with it closed. Any benchmark that fixes one apo PDB per target
has silently fixed a conformational selection that the definition does not justify. Directly
relevant to a frozen benchmark: our choice of apo PDB is a free parameter that the apo/holo
definition does not pin down.

### 3.4 Site-apo is necessary but not sufficient — the tolerated-ligand whitelist is the real decision

AHoJ's own documentation makes a metal ion at the superimposed site sufficient for HOLO:
"If it finds protein chains with ZN, it will list them as HOLO, if the superimposed site is
empty of ligands, the chain will be listed as APO" (<https://apoholo.cz/>, no DOI)
`[VERIFIED-FULLTEXT, NO DOI]`. Water and non-standard residues are opt-in (defaults OFF),
each with an explicit residue list. PocketMiner tolerates exactly five species (HOH, DOD, Na,
Cl, K); CryptoBench blacklists nine HET codes and a <5-atom floor while explicitly **keeping**
sugars and covalent adducts. These whitelists disagree with one another. "Site-apo" therefore
does not by itself determine whether a structure is apo — it only sets the _scope_ of the
question. We must also publish the whitelist.

### 3.5 Fewer than half of all binding sites have any apo form

"less than 50% of the total binding sites processed have an apo form in the PDB", DOI
[10.1016/j.jmb.2024.168545](https://doi.org/10.1016/j.jmb.2024.168545)
`[VERIFIED-ABSTRACT]`. Not a contradiction of the definition, but a warning: the stricter the
reading, the emptier the benchmark. Global-apo would shrink an already sparse pool. This
argues _for_ site-apo on feasibility grounds, and it should be stated as feasibility, not
dressed up as correctness.

---

## 4. Pair-quality criteria the field applies

Synthesised from the tables above; every cell traceable to §2.

| Criterion                         | CryptoBench                                           | PocketMiner                      | Clark 2019                          | Wankowicz 2022                      |
| --------------------------------- | ----------------------------------------------------- | -------------------------------- | ----------------------------------- | ----------------------------------- |
| Resolution                        | ≤2.5 Å                                                | ≤2.5 Å                           | ≤2.5 Å                              | ≤2.0 Å                              |
| Resolution difference apo↔holo    | not stated                                            | not stated                       | not stated                          | **<0.1 Å**                          |
| Same space group                  | not stated                                            | not stated                       | not stated                          | **required**                        |
| Unit cell tolerance               | not stated                                            | not stated                       | not stated                          | **≤1 Å, ≤1°**                       |
| Sequence identity, apo↔holo       | UniProt group                                         | **100%** (Se-Cys/Se-Met exempt)  | 100% then 95% clustering            | exact (±5 terminal residues)        |
| Mutations tolerated               | unknown                                               | **no**                           | no                                  | no                                  |
| Redundancy clustering             | 40% (10% for CV)                                      | 40%                              | 95%                                 | not stated                          |
| Missing loops                     | pocket length must match                              | gaps >3 residues → reject        | not stated                          | not stated                          |
| Conformational-change requirement | pocket RMSD >2 Å; TM ≥0.5; Rg ≤20%; site centres ≤4 Å | apo pocket volume ≥20 Å³ smaller | n/a (studies flexibility)           | n/a                                 |
| Ligand definition                 | ≥5 atoms, 9-code blacklist, sugars+covalent kept      | anything but HOH/DOD/Na/Cl/K     | MW >100 Da and not on 620-code list | ≥10 heavy atoms, additives excluded |
| Covalent ligands                  | **kept**                                              | not stated                       | **excluded**                        | not stated                          |
| Scope of ligand-freedom           | site (via AHoJ)                                       | site (5 Å)                       | ambiguous (§2.3)                    | **global**                          |
| Same organism/construct           | via UniProt                                           | via 100% identity                | via 100%/95% clustering             | via exact sequence                  |

Two convergences worth adopting: the **4–4.5 Å ligand-contact cutoff** for defining site
residues (AHoJ, CryptoBench, Clark; 5 Å in PocketMiner; 4 Å in Riedlová) and the **2.5 Å
resolution ceiling** (three of four sources).

One divergence worth a decision record: **conformational-change magnitude** is measured four
incompatible ways — pocket RMSD (CryptoBench, 2 Å), pocket volume difference (PocketMiner,
20 Å³), no requirement at all (Clark, Wankowicz).

---

## 5. Implications for this repo

Not evidence; the reading of the evidence. Recorded so the reasoning is auditable.

1. Site-apo has **two independent peer-reviewed sources** with explicit site-scoped
   ligand-exclusion clauses (AHoJ 10.1093/bioinformatics/btac701; PocketMiner
   10.1038/s41467-023-36699-3) and one derived benchmark built on the first (CryptoBench
   10.1093/bioinformatics/btae745). It is a defensible published position, not an invention.
2. It has **one clear published counterexample** (Wankowicz 10.7554/eLife.74114) and **one
   nomenclatural counterexample** (IUPAC/NC-IUBMB). The report must state which sense it uses
   in the sentence where it first uses the word.
3. Adopting site-apo does not finish the job. Three further parameters are left free by the
   definition and must be pinned separately: the **tolerated-ligand whitelist** (§3.4), the
   **choice among multiple apo structures** (§3.3), and the **conformational-change
   requirement, if any** (§4).
4. §3.1 is the live risk for _this_ project specifically. A cofactor bound distally is not
   inert with respect to an elastic-network propagation model — it is a node, or a constraint
   on nodes, in the very network being simulated. C5 excludes cofactors from the model, which
   means a site-apo structure with a distal cofactor is modelled as if the cofactor were
   absent while its conformational imprint remains in the coordinates. That is a stated
   modelling approximation, and it should be written down as one rather than left implicit in
   the word "apo".

---

## 6. Not established

Questions we could not answer from a source read this session. Each is phrased so that a
later agent knows exactly what would close it.

1. **MOSTLY CLOSED.** ~~CryptoSite's own inclusion/exclusion criteria.~~ Full text retrieved
   via NCBI `efetch.fcgi?db=pmc&id=4794384&retmode=xml`, which serves the complete author
   manuscript even though Europe PMC reports `isOpenAccess: N`. Both that route and
   `pmc.ncbi.nlm.nih.gov/articles/PMC4794384/` re-served the body on 2026-08-21, and the three
   method clauses below were re-quoted verbatim from each; Europe PMC `fullTextXML` still 404s,
   so that route alone must not be read as the paper being unreachable. Now first-hand
   `[VERIFIED-FULLTEXT]`: binding residues are those with **any atom within 5 A of any ligand
   atom**; redundancy removed at a **40 % sequence-identity** threshold; cryptic sites
   separated from binding pockets by **Fpocket + ConCavity** pocket scores (bad unbound, good
   bound); dataset is **84 cryptic sites + 92 binding pockets + 705 concave surface patches**
   from the PDB and **Binding MOAD**. The abstract also gives the field's cleanest one-line
   definition: "a cryptic site can therefore be defined as a site that forms a pocket in a holo
   structure, but not in the apo structure."

   **The ligand policy follows from the MOAD dependency** (10.1093/nar/gkm911, full text):
   valid ligands are hand-curated as "biologically relevant small molecules ... agonists,
   antagonists, cofactors, inhibitors, allosteric regulators, enzymatic products"; the
   crystallisation matrix (solvents, buffers, detergents, salts) is excluded; glycosylation,
   catalytic metal and HEME are treated as **part of the protein**, not as ligands; and
   **"covalently attached molecules (covalent inhibitors or posttranslational modifications to
   the protein) are not considered valid ligands"**. That last clause excludes our KRAS pair
   from their benchmark -- `6OIM` records `covale CYS 12 SG - MOV C25, 1.805 A` in
   `_struct_conn`. The deviation is declared in `../README.md` section 1.

   _Still open:_ the numeric ligand size floor, the explicit ion policy, the resolution cutoff,
   and whether their apo had to be globally ligand-free -- all in the SI Text, which PMC now
   gates behind a JavaScript proof-of-work challenge that a plain HTTP client cannot satisfy.
   _Closes by: institutional access to the JMB PDF, or a browser session against
   `pmc.ncbi.nlm.nih.gov/articles/instance/4794384/bin/NIHMS758003-supplement-sup.pdf`._

2. **Whether CryptoBench excludes apo structures carrying ligands at other sites.** No
   sentence bearing on this was found in the retrieved full text. It inherits AHoJ's
   site-relative annotation, but inheritance is our inference. _Closes by: reading the
   AHoJ-DB pocket annotation schema at apoholo.cz/db, or the CryptoBench code at
   github.com/skrhakv/CryptoBench._
3. **The scope ambiguity in Clark et al. 2019** (§2.3): does the "MW ≤ 100 Da or on the filter
   list" rule apply to all HETs in the file (global) or only near the site? This decides
   whether the source supports or contradicts us. _Closes by: rereading the Methods of
   10.1371/journal.pcbi.1006705 at the paragraph containing "unified binding site"._
4. **Whether AHoJ / AHoJ-DB treat point mutants as the same protein.** UniProt-AC matching
   would pool them; not stated in what we read. Also unknown: whether AHoJ has an
   "exclude ions" toggle (the docs show ZN → HOLO but list toggles only for water,
   non-standard residues, D-amino acids).
5. **ASD's curation evidence requirement.** What qualifies a site for ASD — a modulator-bound
   crystal structure, mutagenesis, or literature assertion? The ASD2023 full text we read does
   not say. Also unstated: how the modulator-free reference is chosen for the ">1600 allosteric
   actions" structural comparisons, and any required orthosteric–allosteric separation distance.
6. **ASBench's inclusion criteria.** DOI 10.1093/bioinformatics/btv169, not open access. "A
   complex process" is all the abstract offers.
7. **Missing-loop policy** in CryptoBench and Wankowicz. Only PocketMiner states one (gaps >3
   residues rejected). CryptoBench requires apo and holo pocket lengths to match, which is a
   weaker, site-local proxy.
8. **Whether any benchmark besides Wankowicz requires matched crystal form.** No other source
   we read mentions space group or unit cell at all — silence, not rejection.
9. **The Sun et al. reference** cited by PocketMiner for open pockets in CryptoSite "apo"
   structures. We have the claim but not the primary citation's DOI. _Closes by: resolving
   reference list of 10.1038/s41467-023-36699-3._
10. **CLOSED by repo code, not literature.** ~~Whether KRAS has ever been crystallised
    nucleotide-free, and what the challenge's nominated apo PDBs actually contain.~~ The
    HETATM inventory was run over all eight frozen apo structures
    (`allo.structure.pdb`, heavy atoms, 4.5 A). Result: **none of the eight is globally
    ligand-free.** `4OBE` and `4LDJ` both carry GDP + Mg, so the literature question about
    nucleotide-free KRAS is moot for this benchmark -- the nominated structures are
    GDP-bound, measured rather than recalled. Under the global-apo reading of
    10.7554/eLife.74114 this benchmark would have no apo members at all, which is the
    strongest practical argument for the site-relative reading. Under site-apo, exactly one
    entry fails: `1OPL` myristate sits 3.29 A from, and contacts, **all 16** distal label
    residues. Full table in `../README.md` section 1. The two 2012 switch-II papers
    (10.1073/pnas.1116510109, 10.1002/anie.201201358) remain `[VERIFIED-ABSTRACT]` and are
    no longer needed for this question.

11. **Whether the field has an agreed name for the site-relative concept.** We found the
    concept in AHoJ and PocketMiner but no shared term ("site-apo" is our coinage; searches for
    explicit discussion of apo-definition ambiguity returned nothing on point).

---

## Sources retrieved this session

| Work                                            | DOI                                                                              | Access            | Tag used         |
| ----------------------------------------------- | -------------------------------------------------------------------------------- | ----------------- | ---------------- |
| Cimermancic et al. 2016, CryptoSite, J Mol Biol | [10.1016/j.jmb.2016.01.029](https://doi.org/10.1016/j.jmb.2016.01.029)           | paywalled; PMC AM | FULLTEXT         |
| Meller et al. 2023, PocketMiner, Nat Commun     | [10.1038/s41467-023-36699-3](https://doi.org/10.1038/s41467-023-36699-3)         | OA                | FULLTEXT         |
| Škrhák et al. 2024, CryptoBench, Bioinformatics | [10.1093/bioinformatics/btae745](https://doi.org/10.1093/bioinformatics/btae745) | OA                | FULLTEXT         |
| Feidakis et al. 2022, AHoJ, Bioinformatics      | [10.1093/bioinformatics/btac701](https://doi.org/10.1093/bioinformatics/btac701) | OA                | FULLTEXT         |
| Feidakis et al. 2024, AHoJ-DB, J Mol Biol       | [10.1016/j.jmb.2024.168545](https://doi.org/10.1016/j.jmb.2024.168545)           | paywalled         | ABSTRACT         |
| Wankowicz et al. 2022, eLife                    | [10.7554/eLife.74114](https://doi.org/10.7554/eLife.74114)                       | OA                | FULLTEXT         |
| Clark et al. 2019, PLoS Comput Biol             | [10.1371/journal.pcbi.1006705](https://doi.org/10.1371/journal.pcbi.1006705)     | OA                | FULLTEXT         |
| Huang et al. 2011, ASD, Nucleic Acids Res       | [10.1093/nar/gkq1022](https://doi.org/10.1093/nar/gkq1022)                       | OA                | ABSTRACT         |
| Huang et al. 2014, ASD v2.0, Nucleic Acids Res  | [10.1093/nar/gkt1247](https://doi.org/10.1093/nar/gkt1247)                       | OA                | ABSTRACT         |
| Shen et al. 2016, ASD v3.0, Nucleic Acids Res   | [10.1093/nar/gkv902](https://doi.org/10.1093/nar/gkv902)                         | OA                | ABSTRACT         |
| Liu et al. 2020, ASD 2019, Nucleic Acids Res    | [10.1093/nar/gkz958](https://doi.org/10.1093/nar/gkz958)                         | OA                | ABSTRACT         |
| ASD2023, Nucleic Acids Res                      | [10.1093/nar/gkad915](https://doi.org/10.1093/nar/gkad915)                       | OA                | FULLTEXT         |
| Huang et al. 2015, ASBench, Bioinformatics      | [10.1093/bioinformatics/btv169](https://doi.org/10.1093/bioinformatics/btv169)   | paywalled         | ABSTRACT         |
| Riedlová et al. 2026, J Chem Theory Comput      | [10.1021/acs.jctc.6c00427](https://doi.org/10.1021/acs.jctc.6c00427)             | OA                | FULLTEXT         |
| IUPAC/NC-IUBMB Nomenclature Newsletter 2023     | no DOI — <https://iubmb.qmul.ac.uk/newsletter/2023.html>                         | web               | FULLTEXT, NO DOI |
| AHoJ documentation                              | no DOI — <https://apoholo.cz/>                                                   | web               | FULLTEXT, NO DOI |

Author lists for the ASD series and CryptoBench are `[UNVERIFIED]` where not returned by the
search record; cite by DOI, not by name, until checked.
