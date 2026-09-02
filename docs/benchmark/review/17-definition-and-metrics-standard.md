# The field's definition and the field's metrics — a second, independent pass

**Date of search: 2026-09-02.** Independent re-derivation of (Q1) what a published apo/holo
pair for an **allosteric** site is, and (Q2) what the field actually reports and against what
chance line — then a judgement of `../primary/README.md` §1 and `../evaluation/README.md`
against both.

**This is a second pass, not a second opinion on the first one.** It was run by fetching
primary sources rather than by re-reading `06-definition-audit.md` and `07-metrics-audit.md`.
Those two were read first and are assumed; where this document reaches the same conclusion the
citation here is one **I** retrieved, and where it reaches a different one it says so. Nine
findings below are not in either predecessor and are marked **[NEW]**.

## Provenance tags

| Tag         | Meaning                                                                              |
| ----------- | ------------------------------------------------------------------------------------ |
| `[FT]`      | I fetched the source this session and the quoted string came back from that fetch    |
| `[ABS]`     | abstract or indexed record only, fetched this session                                |
| `[SEARCH]`  | from a web-search summary this session; **not** a fetched primary source             |
| `[repo]`    | carried from this repository's evidence base or from `06`/`07`; not re-verified here |
| `[UNKNOWN]` | searched this session and no source found. Not "false" — unmeasured                  |

**The same limit that binds `06` binds this.** Every quoted string passed through a
fetch-and-summarise tool and is one step removed from the raw XML or PDF. Nothing here is
quotable into `docs/report/` until re-read at the raw source. One quote failed exactly this
way and is flagged in §B.5.

---

## Headline verdict

**Q1.** There is no single formal definition. There are **two** things the field agrees on and
**four** it does not.

Agreed: (a) an allosteric site is defined **topologically**, not metrically — "nonoverlapping
and spatially distinct from, but conformationally linked to, the orthosteric binding site"
(IUPHAR XC Table 1) `[FT]` and "a site topographically distinct from the orthosteric site"
(ASD v1) `[FT]`; (b) site residues are enumerated by a **contact shell around a deposited
effector**. Not agreed: the shell radius (**3.5 to 8 Å**, six incompatible values, wider than
the range this repo currently records) **[NEW]**; whether "apo" is entry-level or site-level;
what counts as an occupant that breaks apo-ness (three incompatible operationalisations)
**[NEW]**; and whether functional evidence is required at all.

Against that, the repository's eight clauses come out as **five standard, one stricter than the
field, one looser than every published rule, and one with no precedent at all**. The single
clause with no published counterpart anywhere is **(iii)'s "scoreable portion" restriction**,
which the repo already labels a relaxation — correctly. Two further items are looser than the
field and are **not** currently disclosed as such: the 90 % identity floor, and the complete
absence of any conformational-distance pair-admission rule (§A.6).

**Q2.** The confirmatory endpoint is fine and is under-defended. The mean midrank is an exact
affine re-parameterisation of AUC-ROC (§B.4, with the algebra), so it introduces no new
behaviour — but no reviewer will recognise the phrase, and the repo cites no in-domain
precedent for a rank test. **There is one, in a paper the repo already cites for something
else:** Amor et al. run a Wilcoxon rank-sum on residue propensities, allosteric against
non-allosteric, `P < 0.0005` `[FT]` **[NEW]**. That is the same test on the same unit and it
should be cited at §3.1 of the evaluation README.

The comparability problem is elsewhere and it is real: the field's success rate is a **pocket**
number, not a residue number, and the repo computes the pocket number (`site_pocket_rank`) but
never converts it into the success rate the field reads. And **"DCC" names two different
quantities in two widely cited papers** `[FT]` **[NEW]** — P2Rank calls centre-to-any-ligand-atom
"DCC"; STINGAllo and Utgés & Barton reserve DCC for centre-to-centre. A DCC number without a
naming statement is not comparable to anything.

**One finding that flatters the repo more than either predecessor does.** Of eleven papers I
read at source this session, **two** report any chance line at all, and **none** reports a chance
line for a top-N success rate. The repo's exact hypergeometric baseline for top-5 has no
precedent in the papers I read. It is not merely "ahead"; it is a number the field does not
compute.

---

# Part A — Q1: what an apo/holo pair for an allosteric site is

## A.1 What makes a site allosteric, in the sources that define the term

Three definitional statements exist. All three are **topological**, and two are verified
verbatim here.

**IUPHAR XC** (Christopoulos et al., _Pharmacol Rev_ 2014, `doi:10.1124/pr.114.008862`,
PMC11060431) `[FT]`. Table 1: an allosteric site is "A binding site on a receptor macromolecule
that is nonoverlapping and spatially distinct from, but conformationally linked to, the
orthosteric binding site." §III: "It is recommended that the term 'allosteric' be reserved for
instances where the properties of one ligand (small molecule or protein) are altered upon
binding of a second ligand at a nonoverlapping, topographically distinct site and where,
ideally, reciprocity in this interaction can be demonstrated." Table 1 note 7 admits a
**bitopic** ligand that "concomitantly engages an orthosteric and an allosteric site". The fetch
returned, explicitly, that the document **does not specify a minimum distance**, "only that they
be 'nonoverlapping and spatially distinct'". This independently reproduces the repo's reading of
IUPHAR, including the small-molecule-**or-protein** parenthetical it relies on.

**ASD v1** (Huang et al., _NAR_ 2011, `doi:10.1093/nar/gkq1022`, PMC3013650) `[FT]`. The
evidence bar, verbatim: "With at least three cases of experimental evidence in crystal structure
complex or biochemistry (inactive mutation of allosteric residue, cooperativity of kinetic
effect from two ligands and uncompetitive-binding assay with chromatography, etc.), 336 proteins
supporting their functional change elicited by modulator binding at a site that was
topographically distinct from the orthosteric functional site, were verified as allosteric
proteins". Site definition: "a site topographically distinct from the orthosteric site". **No
distance threshold appears.** This confirms, at the primary source, both halves of the repo's
clause (ii) authority and the "no minimum distance" claim — and it confirms that the bar sits on
the **protein**, not on the site, which is the limitation the repo's secondary README already
records.

**The one metric exception, and it is family-scoped.** Kincore (Modi & Dunbrack, _NAR_ 2022,
`doi:10.1093/nar/gkab920`, PMC8728253) `[FT]`: allosteric inhibitors are "Any small molecule in
the asymmetric unit whose minimum distances from the hinge region and C-helix-Glu(+4) residues
are both >6.5 Å" — 220 unique ligands; Type 3 is "back pocket only without displacing ATP"; all
pocket contacts at "distance between any two atoms is ≤4.0 Å (hydrogens not included)". This
independently reproduces `06` §3.2. Two things `06` does not add: the Kincore rule classifies a
**ligand**, so it presupposes a holo structure and cannot be applied to an apo input at all; and
it makes **no functional demand**, so adopting it would contradict clause (ii). It remains the
only published metric separation rule, and BCR-ABL1 is a kinase.

**The counterweight to any distance rule, verified.** CASBench (Zlobin et al., _Acta Naturae_
2019, `doi:10.32607/20758251-2019-11-1-74-80`, PMC6475866) `[FT]`: "In 30% of cases, the
catalytic and allosteric sites either overlap or share a common border; in 70% of entries, both
sites reside at a considerable distance from each other and do not overlap within the
structure." 91 enzymes. Both the fraction and the set size reproduce exactly against the repo.

## A.2 The shell radius — six values, and the range is wider than the repo records **[NEW]**

Every resource enumerates site residues as a contact shell around the deposited effector. Nobody
agrees on the radius.

|    Radius | Resource                          | Verbatim rule                                                                                                                                                   | Src        |
| --------: | --------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- |
|     3.5 Å | Amor et al. 2016                  | "residues within 3.5 Å of the allosteric ligand"                                                                                                                | `[FT]`     |
|     4.0 Å | AlloBench                         | "residues within 4 Å of the allosteric modulator in the PDB structures"                                                                                         | `[FT]`     |
|     4.0 Å | Kincore (contacts)                | "distance between any two atoms is ≤4.0 Å (hydrogens not included)"                                                                                             | `[FT]`     |
|     4.0 Å | ASBench                           | structures removed if "missing residues within 4 Å of the allosteric modulator"                                                                                 | `[SEARCH]` |
| **4.5 Å** | AHoJ, inherited by CryptoBench    | "AHoJ defines the binding site by considering protein residues within a user-defined distance threshold (default 4.5 Å) from the atoms of the specified ligand" | `[FT]`     |
|     5.0 Å | CASBench                          | "all residues located within 5 Å of the selected ligand were considered"                                                                                        | `[FT]`     |
|     5.0 Å | CryptoSite                        | "residues with at least one atom within 5 Å from any atom of a ligand in the bound conformation"                                                                | `[FT]`     |
|     5.0 Å | PocketMiner                       | ligands "within 5 Å of all MOAD-assigned biologically relevant residues"                                                                                        | `[FT]`     |
|     6.0 Å | ASD v2.0                          | "automatically extracted from a complex structure by 6 Å around allosteric modulator in the site using Pymol and manually inspected"                            | `[FT]`     |
|     6.0 Å | KeyAlloSite (orthosteric)         | "all residues within 6 Å around the orthosteric ligand"                                                                                                         | `[FT]`     |
| **8.0 Å** | KeyAlloSite (allosteric fallback) | when CAVITY failed, "within 8 Å around the allosteric ligand"                                                                                                   | `[FT]`     |

**The repo's table records 3.5–6 Å. The true published range is 3.5–8 Å**, because KeyAlloSite
falls back to 8 Å for the allosteric site specifically. That is a 2.3× spread in radius and
therefore a large spread in label-set size, and it is the single strongest reason a
cross-paper number comparison is invalid. The repo's 4.5 Å is mid-range and matches the two
resources with the largest PDB-wide coverage.

## A.3 What makes a structure "apo" — two families and three incompatible occupant rules

**Family 1 — entry-level.** The structure must carry no ligand anywhere.

- **CryptoBank** (Febrer Martinez et al., _Sci Adv_ 2026, `doi:10.1126/sciadv.ady6364`,
  PMC13267282) `[FT]`: "protein chains with a nonpolymer_entity_count of zero were classified as
  apo"; holo is "nonpolymer_entity_count ≥ 1". Resolution "higher or equal to 2.5 Å"; "chains
  that belong to the same 95% identity cluster in the PDB"; exclusion list of "ions, low
  molecular weight compounds (<60 Da), solvents"; "only alignments that resulted in a Cα RMSD
  lower than 2.5 Å were selected for scoring"; crypticity at "values of 0.5 or higher".
- **Wankowicz et al. 2022** (`doi:10.7554/eLife.74114`) `[FT]`: holo is "structures that
  contained at least one ligand, defined as any HETATM residue with 10 or more heavy atoms,
  excluding common crystallographic additives"; apo is "structures without a ligand bound".
  Pairing additionally requires "A resolution difference between the two structures less than
  0.1 Å", "Exact sequence or exact sequence after removing the first or last five base pairs",
  **matching space groups and unit cell parameters (dimensions within 1 Å, angles within 1°)**.

**Family 2 — site-level.** The structure must be ligand-free _at the site of interest_.

- **AHoJ** (`doi:10.1093/bioinformatics/btac701`, PMC9750100) `[FT]`: "each one is listed as
  holo or apo respective to the presence or absence of ligands in the defined binding site(s)".
  The main text states **no numeric threshold**; the 4.5 Å default is recoverable only through
  CryptoBench's description of it `[FT]`. The repo should cite CryptoBench, not AHoJ, for the
  number.
- **PocketMiner** (`doi:10.1038/s41467-023-36699-3`, PMC9977097) `[FT]`: "We removed apo
  candidate structures with ligands (excluding water, heavy water, sodium, chloride, and
  potassium) within 5 Å of all MOAD-assigned biologically relevant residues in the holo
  candidate structure"; "less than 100% sequence identity ... except for mismatches between
  selenocysteine and cysteine and selenomethionine and methionine"; "removed each candidate
  structure which did not have a monomeric biological unit assigned in remark 350".

**The finding the repo does not have. [NEW]** The three rules disagree not only on _where_ to
look but on _what counts as an occupant_, and they use three mutually inconsistent instruments:

| Instrument           | Rule                                                                       | Source                |
| -------------------- | -------------------------------------------------------------------------- | --------------------- |
| **Name list**        | water, heavy water, Na⁺, Cl⁻, K⁺ are not occupants                         | PocketMiner `[FT]`    |
| **Mass**             | ions, solvents, anything **< 60 Da** is not an occupant                    | CryptoBank `[FT]`     |
| **Heavy-atom count** | a ligand is a HETATM residue with **≥ 10 heavy atoms**, additives excluded | Wankowicz 2022 `[FT]` |

These do not agree on the cases that actually decide a benchmark. Glycerol (92 Da, 6 heavy
atoms) is an occupant under CryptoBank and not under Wankowicz. Sulfate (96 Da, 5 heavy atoms)
is an occupant under CryptoBank and PocketMiner and not under Wankowicz. Acetate, PEG fragments
and DMSO split the same way.

**The repo publishes no such instrument.** Clause (iii) says "no ligand of any kind within the
scoreable portion of that site"; secondary clause (x) says "No apo component may contact a
scoreable label". Neither defines _ligand_ or _component_, so neither answers what a
cryoprotectant, a buffer ion or an ordered water does to a pair. That is a genuine gap and it is
cheap to close — the answer is presumably "everything in the coordinate file that is not a
polymer residue or a water", which is nearest to CryptoBank, but it is not written down and the
question the brief asks cannot be answered from the frozen documents.

## A.4 What each published resource's inclusion rule actually is

| Resource                                           | Encodes a definition of            | Apo reading                                        | Site rule                                                                                                                                                                   | Redundancy rule                                                           | Src                               |
| -------------------------------------------------- | ---------------------------------- | -------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- | --------------------------------- |
| **ASD v1** (`10.1093/nar/gkq1022`)                 | allosteric **protein**             | n/a — no apo step                                  | "topographically distinct from the orthosteric site"; ≥ 3 cases of experimental evidence                                                                                    | —                                                                         | `[FT]`                            |
| **ASD v2.0** (`10.1093/nar/gkt1247`)               | allosteric **site**                | n/a                                                | 6 Å around modulator, Pymol, manually inspected                                                                                                                             | —                                                                         | `[FT]`                            |
| **ASBench** (`10.1093/bioinformatics/btv169`)      | benchmark subset of ASD            | n/a                                                | 4 Å; excludes peptide/ion modulators, overlapping sites, resolution > 3.0 Å                                                                                                 | Core set 235, Core-Diversity 147                                          | `[SEARCH]`                        |
| **CASBench** (`10.32607/20758251-2019-11-1-74-80`) | catalytic **and** allosteric sites | n/a                                                | 5 Å; unions over deposited structures                                                                                                                                       | CD-HIT 95 %                                                               | `[FT]`                            |
| **AlloBench** (`10.1021/acsomega.5c01263`)         | allosteric site, tool benchmark    | **no apo step**                                    | 4 Å; **biological assembly** structures downloaded; benchmark subset "only ... small-molecule allosteric modulators" (dataset is 90 % small molecule, 8 % ion, 2 % peptide) | —                                                                         | `[FT]`                            |
| **CryptoSite** (`10.1016/j.jmb.2016.01.029`)       | **cryptic** site                   | site-level, ligand-stripped holo                   | 5 Å                                                                                                                                                                         | 40 % identity                                                             | `[FT]`                            |
| **CryptoBench** (`10.1093/bioinformatics/btae745`) | **cryptic** site                   | site-level, inherited from AHoJ                    | 4.5 Å default                                                                                                                                                               | **10 %** identity, but as a train/test **split** rule, not a pairing rule | `[FT]`                            |
| **CryptoBank** (`10.1126/sciadv.ady6364`)          | **cryptic** site, PDB-scale        | **entry-level**, `nonpolymer_entity_count = 0`     | —                                                                                                                                                                           | 95 % clusters; pair admitted only at Cα RMSD < 2.5 Å                      | `[FT]`                            |
| **AHoJ** (`10.1093/bioinformatics/btac701`)        | apo/holo **relationship**          | **site-level**                                     | user-defined, default 4.5 Å                                                                                                                                                 | —                                                                         | `[FT]`                            |
| **AHoJ-DB** (`10.1016/j.jmb.2024.168545`)          | apo/holo, PDB-wide                 | site-level                                         | —                                                                                                                                                                           | —                                                                         | metadata `[FT]`, content `[repo]` |
| **PocketMiner** (`10.1038/s41467-023-36699-3`)     | cryptic pocket opening             | **site-level**, 5 Å, named exclusions              | 5 Å                                                                                                                                                                         | **100 %** identity; monomeric biological unit only                        | `[FT]`                            |
| **Wankowicz 2022** (`10.7554/eLife.74114`)         | apo/holo pair                      | **entry-level**, ≥ 10 heavy atoms                  | —                                                                                                                                                                           | exact sequence ± 5 termini; same space group; cell within 1 Å / 1°        | `[FT]`                            |
| **Kincore** (`10.1093/nar/gkab920`)                | allosteric **ligand** (Type IV)    | n/a — holo only                                    | ligand > 6.5 Å from hinge **and** αC-Glu(+4); contacts ≤ 4.0 Å                                                                                                              | 7,177 human kinase chains                                                 | `[FT]`                            |
| **PDBbind** (`10.1093/bioinformatics/btu626`)      | protein–ligand **affinity**        | **no apo member exists**; every entry is a complex | refined set: resolution ≤ 2.5 Å, non-covalent binary complex, measured Kd or Ki, ligand MW < 1000                                                                           | —                                                                         | `[SEARCH]`                        |

**PDBbind encodes no allosteric definition and no apo/holo pair.** It is an affinity set of
complexes; its "refined set" rules are quality rules for a bound structure. It is in the brief's
list and the honest answer is that it is not a source for this question at all. Its exclusion of
covalent complexes is worth one line, because it is the same convention AlloBench applies and
the same one the KRAS/sotorasib arm departs from.

**CAPASP** (`doi:10.1007/s10822-026-00831-4`) `[ABS]`, abstract retrieved verbatim this session,
is the field's only current independent assessment: "a CAPASP-General subset comprising holo
state allosteric proteins and a CAPASP-Unbound subset comprising apo state allosteric proteins",
evaluated "across five dimensions: sensitivity, specificity, F1-score, MCC value and ranking
capability", with "PASSer and APOP" leading and all five tools performing "better with the
CAPASP-General subset than with the CAPASP-Unbound subset". **What "apo" means in
CAPASP-Unbound remains `[UNKNOWN]`** — the construction is paywalled. `06` reached the same
place independently.

## A.5 The repository's eight clauses against field precedent

Verdicts: **STANDARD** = a majority of resources apply a rule of this kind and the repo's value
sits inside the published range. **STRICTER** = the repo demands more than any published rule.
**LOOSER** = at least one published rule would reject a pair the repo admits. **NO PRECEDENT** =
no published resource states a rule of this kind; the repo must defend it, not cite it.

| Clause                                                    | Repo rule, compressed                                                                                                   | Closest published rule, verified this session                                                                                                                                                                                                                                     | Verdict                                                                        | What follows                                                                                                                                                                                                                  |
| --------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **(i) Effector**                                          | holo contains the effector by PDB component ID; site = residues within a **declared** radius (4.5 Å) of its heavy atoms | Practice universal; radius spans **3.5–8 Å** across ASD/CASBench/CryptoSite/PocketMiner/AHoJ/CryptoBench/ASBench/AlloBench/Amor/KeyAlloSite `[FT]`                                                                                                                                | **STANDARD** in kind, mid-range in value                                       | Widen the repo's recorded range to 3.5–8 Å (KeyAlloSite's 8 Å fallback). Keep declaring the radius at first use                                                                                                               |
| **(i) sub-rule: small molecules only**                    | effector must have a PDB **chemical component ID**                                                                      | AlloBench's benchmark subset does the same ("only ... small-molecule allosteric modulators"), but its dataset is 8 % ions and 2 % peptides `[FT]`; IUPHAR XC §III admits a protein second ligand `[FT]`                                                                           | **STRICTER than the authority cited**                                          | One scope sentence in clause (i). `06` recommendation 9 says the same; this pass adds AlloBench's own 90/8/2 split as the size of what is excluded                                                                            |
| **(ii) Provenance of label**                              | the site is allosteric because **functional** evidence says so; distance neither necessary nor sufficient               | ASD v1: "at least three cases of experimental evidence" `[FT]`; IUPHAR XC §III `[FT]`. **Every later ASD release drops the bar**, and Kincore + Riedlová define allosteric purely geometrically `[FT]`/`[repo]`                                                                   | **STANDARD as principle, STRICTER than current practice**                      | This is the repo's strongest clause and its per-arm `allosteric_evidence` DOI exceeds every resource fetched here. Say so in the report; it is a differentiator, not overhead                                                 |
| **(iii) Site-apo, restricted to the _scoreable_ portion** | no ligand of any kind within the scoreable labels; contacts to the full label set recorded, not disqualifying           | Site-level apo is published (AHoJ, CryptoBench, PocketMiner `[FT]`). **Restricting the check to a sub-region of the site is published nowhere.** PocketMiner and Clark reject on contact to _any_ site residue `[FT]`/`[repo]`                                                    | **NO PRECEDENT**, and **LOOSER** than the two rules that exist                 | Already disclosed as a relaxation, correctly. The report must name it as the one clause the field would reject and name the arms that depend on it (both KRAS)                                                                |
| **(iii) sub-rule: what counts as an occupant**            | **not stated** in clause (iii) or secondary clause (x)                                                                  | Three incompatible instruments: name list (PocketMiner), < 60 Da (CryptoBank), ≥ 10 heavy atoms (Wankowicz) `[FT]`                                                                                                                                                                | **NO PRECEDENT — because nothing is stated**                                   | Publish the repo's instrument. Water, glycerol, sulfate and PEG decide pairs and the frozen documents do not say which side they fall on **[NEW]**                                                                            |
| **(iv) Identity ≥ 90 %**                                  | same protein at ≥ 90 % identity, differences enumerated                                                                 | PocketMiner **100 %** `[FT]`; Wankowicz **exact ± 5 termini + same space group + cell within 1 Å/1°** `[FT]`; CryptoBank **95 %** clusters `[FT]`; CryptoSite 40 % (a redundancy rule, not a pairing rule) `[FT]`; CryptoBench 10 % (a **split** rule, not a pairing rule) `[FT]` | **LOOSER than every published pairing rule**                                   | The floor is non-binding in fact (arms are 97.6–100 %). Either raise it to 95 % or state in one line that it never binds. **[NEW]** Two of the fetched rules are _not_ pairing rules and should not be quoted as if they were |
| **(v) Assembly**                                          | same oligomeric state; modelled state should be the biological assembly                                                 | AlloBench: "The biological assembly structures of the target proteins were downloaded" `[FT]`. **PocketMiner requires a monomeric biological unit and discards the rest** `[FT]`. Amor excludes on oligomeric mismatch `[repo]`                                                   | **STANDARD, field split**                                                      | Reproduces `06`. Record that the clause takes a side; the myosin arm's mechanism is an assembly property                                                                                                                      |
| **(vi) Second site**                                      | orthosteric occupancy recorded for **both** members; active-site rule stated                                            | No resource fetched states any rule. Nearest analogue is PDBbind's "binary complexes" quality rule, from a different task `[SEARCH]`                                                                                                                                              | **NO PRECEDENT** — but it is a _disclosure_, not a filter                      | Costs nothing, admits nothing. Defensible as written; do not upgrade it to a filter                                                                                                                                           |
| **(vii) Non-circularity**                                 | no residue of the propagation source may be scored as a candidate                                                       | AlloPred's rule about pocket membership inside its own procedure `[repo]`. **CASBench's 30 % overlap** `[FT]` is why a _distance_ version would be wrong                                                                                                                          | **NO PRECEDENT as an admission clause**; standard as a leakage control         | Keep. Add the corroboration in §B.6: P2Rank states in its own text that the negative class is contaminated                                                                                                                    |
| **(viii) State disclosure**                               | functional state of each member **stated**, pocket-lining change reported; difference disclosed, not required           | No resource requires a state difference. **CryptoBank admits a pair only at Cα RMSD < 2.5 Å** `[FT]` — a state _filter_ the repo has no analogue of                                                                                                                               | **NO PRECEDENT as written; LOOSER than CryptoBank on the pair-admission axis** | Report the pair Cα RMSD per arm beside the disclosure. It is one number, it is what CryptoBank filters on, and the repo currently has no conformational-distance admission rule at all **[NEW]**                              |

**Count: five clauses standard or standard-in-kind, one stricter, one looser, three with no
precedent** — of which (vi) and (vii) are cheap and defensible and (iii)'s sub-region rule is the
one that must be argued rather than cited.

## A.6 Two axes the repo does not use and the field does **[NEW]**

Neither is in `06`'s ranked list of missing axes.

1. **Crystal-form matching.** Wankowicz 2022 pairs only structures with the **same space group
   and unit cell within 1 Å / 1°** `[FT]`. The repo's pairs cross crystal forms freely. This is
   not a defect — the repo's question is different, and matching crystal forms would empty the
   set — but a reviewer who knows that paper will ask, and the answer is "we do not, and here is
   the pair RMSD instead", which requires §A.5 item (viii) to have been done.
2. **Global conformational distance as an admission rule.** CryptoBank's Cα RMSD < 2.5 Å `[FT]`.
   The repo's cardiac-myosin arm is precisely where this would bite, and the arm already
   discloses a long-range contact Jaccard of 0.471 — a different, and arguably better,
   instrument for the same concern. Say that it is the same concern.

---

# Part B — Q2: recognised metrics and the evaluation workflow

## B.1 What the field reports, with the paper that sets each convention

Every row was fetched this session unless tagged otherwise. "Chance line" answers the brief's
question directly: does the paper state what the metric would be under a null?

| Endpoint                                                  | Unit            | Standard N / threshold                                                                                                    | Chance line reported?                              | Negatives                                                                                                                                    | Convention-setting source                                                                                                                                                                                                                                                                                                 |
| --------------------------------------------------------- | --------------- | ------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Top-n / top-(n+2) identification success**              | pocket          | n = number of relevant ligands; "for proteins with only one ligand this corresponds to the usual Top-1 and Top-3 cutoffs" | **No**                                             | other detected pockets                                                                                                                       | P2Rank, `doi:10.1186/s13321-018-0285-8` `[FT]`                                                                                                                                                                                                                                                                            |
| **Top-N+2 recall, as the universal success rate**         | pocket          | N+2                                                                                                                       | **No**                                             | non-binding residues / pockets                                                                                                               | Utgés & Barton 2024, `doi:10.1186/s13321-024-00923-z` `[FT]`: "all authors of ligand site prediction tools should use top-_N_+2 recall as 'success rate' for consistency"                                                                                                                                                 |
| **Top-3 pocket rank success**                             | pocket          | 3                                                                                                                         | **No**                                             | other fpocket pockets                                                                                                                        | APOP, `doi:10.1093/bioinformatics/btad275` `[FT]`: "If this pocket is among the top-ranked three predicted pockets, we count it as a success"                                                                                                                                                                             |
| **Top-1/2/3 rank probability**                            | pocket          | 1, 2, 3 → 56.0 / 76.0 / 96.0 %                                                                                            | **Yes** — random size-matched surface patches      | "randomly selected two residues that are not part of the orthosteric and allosteric sites from the surface residues", 4 repeats, Student's t | KeyAlloSite, `doi:10.7554/eLife.81850` `[FT]`                                                                                                                                                                                                                                                                             |
| **DCA** (centre → nearest ligand atom)                    | pocket          | **4 Å**                                                                                                                   | No                                                 | —                                                                                                                                            | P2Rank `[FT]` — **but P2Rank calls this "DCC"**                                                                                                                                                                                                                                                                           |
| **DCC** (centre → centre)                                 | residue cluster | **4 Å** (STINGAllo) vs **10–12 Å** (Utgés & Barton)                                                                       | No                                                 | —                                                                                                                                            | STINGAllo, `doi:10.1093/bib/bbaf424` `[FT]`: "the geometric center of the predicted AFRs cluster is within 4 Å of the geometric center of the experimentally confirmed allosteric site". Utgés & Barton `[FT]`: "A DCC threshold of 4 Å is too conservative, and a more flexible DCC threshold of 10–12 Å should be used" |
| **AUC-ROC**                                               | residue         | —                                                                                                                         | Nominally 0.5; **never stated** in the papers read | non-site residues                                                                                                                            | CryptoSite, `doi:10.1016/j.jmb.2016.01.029` `[FT]`, AUC 0.83 (0.74 without MD features); PocketMiner, `doi:10.1038/s41467-023-36699-3` `[FT]`, "average test PR-AUC of 0.44 ± 0.12 (average ROC-AUC: 0.83 ± 0.04)", 0.87 on the experimental task; CryptoBench, `doi:10.1093/bioinformatics/btae745` `[FT]`               |
| **AUC-PR / average precision**                            | residue         | —                                                                                                                         | Prevalence; **not stated** in any paper read       | as above                                                                                                                                     | PocketMiner `[FT]`; CryptoBench `[FT]`                                                                                                                                                                                                                                                                                    |
| **MCC and F1**                                            | residue         | threshold-dependent                                                                                                       | No                                                 | non-binding residues                                                                                                                         | STINGAllo `[FT]`: "overall per-residue classification F1 score of 0.64 (Matthews correlation coefficient 0.64)"; CryptoBench reports "AUC, AUPRC, ACC, FPR, TPR, MCC, F1" `[FT]`; CAPASP names F1 and MCC among its five dimensions `[ABS]`                                                                               |
| **Jaccard index**                                         | residue set     | swept at 0, 0.1, 0.2, 0.3, 0.4, 0.5                                                                                       | No                                                 | **none defined**                                                                                                                             | AlloBench, `doi:10.1021/acsomega.5c01263` `[FT]`                                                                                                                                                                                                                                                                          |
| **AP at an IoU threshold**                                | residue mask    | IoU thresholds `[repo]`                                                                                                   | No                                                 | unmatched ground-truth sites                                                                                                                 | UniSite, `arXiv:2506.03237` `[ABS]`: "Average Precision based on Intersection over Union (IoU)"                                                                                                                                                                                                                           |
| **Wilcoxon rank-sum on residue scores**                   | **residue**     | —                                                                                                                         | non-allosteric residues                            | non-allosteric residues                                                                                                                      | **Amor et al. 2016**, `doi:10.1038/ncomms12477` `[FT]`: "residues within 3.5 Å of the allosteric inhibitor have significantly higher propensities than non-allosteric residues (Wilcoxon rank sum, P<0.0005)"                                                                                                             |
| **Surrogate-site null + bootstrap CI**                    | site            | 1,000 surrogates; 10,000 bootstrap resamples                                                                              | **Yes**                                            | size- and diameter-matched surrogate sites                                                                                                   | Amor et al. `[FT]`                                                                                                                                                                                                                                                                                                        |
| **Between-method Wilcoxon signed-rank**                   | pocket rank     | —                                                                                                                         | not a null                                         | —                                                                                                                                            | APOP `[FT]`, "P-value of 0.00088" against AlloPred                                                                                                                                                                                                                                                                        |
| **Sensitivity, specificity, F1, MCC, ranking capability** | pocket          | five dimensions                                                                                                           | No                                                 | two purpose-built independent sets                                                                                                           | CAPASP, `doi:10.1007/s10822-026-00831-4` `[ABS]`                                                                                                                                                                                                                                                                          |
| **KS test on feature distributions**                      | residue         | —                                                                                                                         | not on performance                                 | 705 concave surface patches                                                                                                                  | CryptoSite `[FT]`                                                                                                                                                                                                                                                                                                         |

## B.2 The chance-line finding, stated as a count **[NEW]**

Of the **eleven** papers I read at source this session (P2Rank, Utgés & Barton, APOP,
KeyAlloSite, STINGAllo, CryptoSite, PocketMiner, CryptoBench, AlloBench, Amor, CAPASP-abstract):

- **Two** report any chance line derived from a null construction: Amor's 1,000 surrogate sites
  with a 10,000-resample bootstrap CI, and KeyAlloSite's random size-matched surface patches at
  four repeats.
- **Zero** report a chance line for a top-N success rate. Not one paper states what top-3 would
  be if the ranking were random, even though every one of them knows the denominator.
- **Zero** report the prevalence beside AUC-PR. PocketMiner reports PR-AUC 0.44 without a
  prevalence in the same sentence.

This is a stronger and narrower statement than `07`'s "13 of 18 state no test", and it is
independent of it. **The repo's exact hypergeometric E[precision@5] and P(≥ 1 hit) are not
merely uncommon; in the sample I read they are unprecedented.** They should be presented that
way in the report, foregrounded rather than buried in a `chance` dict.

## B.3 "DCC" names two different quantities **[NEW]**

P2Rank `[FT]` defines its criterion as "DCC(distance between the center of the pocket and any
ligand atom) ... with 4 Å threshold" — that is centre-to-**atom**, which Utgés & Barton and
STINGAllo both call **DCA**. STINGAllo `[FT]` defines DCC as centre-to-**centre**. Utgés &
Barton `[FT]` use both and recommend "a threshold of DCC of 10–12 Å" specifically "to obtain
comparable results between DCA and DCC recall".

So a "DCC ≤ 4 Å" number from P2Rank and a "DCC ≤ 4 Å" number from STINGAllo measure different
things, and the second is much harder. The repo's evaluation README already notes P2Rank's usage
in passing; it must be promoted to a naming statement wherever DCC is printed, or the repo's DCC
column will be read against the wrong comparator.

**One correction to `07` from this pass.** `07`'s census row 39 records STINGAllo as "DCC
success 78 % / 60.2 %". The fetched text gives **60.2 % overall** and **77.8 % conditional on
the predicted residues falling inside an FPocket pocket**. The two numbers are not two datasets;
one is a subset condition. Quoting 78 % unqualified overstates the comparator.

## B.4 Is the mean midrank recognisable? The algebra, then the verdict

**It is AUC-ROC.** With `n₁` positives, `n₀` negatives, midranks over all `n₁ + n₀` candidates,
and `R̄₁` the mean midrank of the positives, the Mann-Whitney statistic is
`U = n₁R̄₁ − n₁(n₁+1)/2` and

```
AUC-ROC = U / (n₁ n₀) = (R̄₁ − (n₁ + 1)/2) / n₀
```

Under every null in the frozen protocol `n₁` and `n₀` are held fixed, so AUC-ROC is a strictly
increasing **affine** function of `R̄₁`, and a permutation test on one is the identical test on
the other. This is checkable in three lines and the evaluation README asserts it without
showing it. Show it.

**Verdict on recognisability, in three parts.**

1. **The name is not recognised.** "Mean midrank" appears in none of the eleven papers I read at
   source and in none of the 48 rows of `07`'s census. A reviewer meeting the phrase cold will
   not know what it is.
2. **The quantity is recognised instantly, once named correctly.** Call it the Mann-Whitney
   statistic, or state the identity above, and it becomes AUC-ROC — which is the residue-level
   convention in CryptoSite, PocketMiner and CryptoBench, all verified here `[FT]`.
3. **The _test_ has an in-domain precedent the repo does not claim. [NEW]** Amor et al. 2016
   run exactly this test: a **Wilcoxon rank-sum on residue-level scores, allosteric site
   residues against non-allosteric residues, `P < 0.0005`** `[FT]`. The repo cites Amor only for
   the surrogate-site null (`../evaluation/README.md` §4.2 and §12.3). The rank-sum is a
   separate, additional test in the same paper, on the same unit as the repo's confirmatory
   statistic. **Citing it converts "no precedent in allostery" into "the precedent is in the
   paper we already cite".** This is the cheapest high-value change in this document.

**What the field would expect instead of the repo's endpoint**, in the order a reviewer will ask
for them: (a) a **top-N pocket** success rate, N = 3, or Utgés & Barton's top-N+2 recall; (b)
DCC or DCA with a stated threshold and a stated definition; (c) residue AUC-ROC **and** AUPRC;
(d) F1 and MCC on a variable-size predicted residue set; (e) nothing else. The first is the
modal metric in the census and the one CAPASP calls "ranking capability".

## B.5 One quote that failed verification, recorded rather than used

I fetched Amor et al. twice with different prompts. The first fetch returned the surrogate rule
as matched on residue count with a diameter that "does not exceed the allosteric site's
diameter"; the second returned "matched by geometric distance from the active site". These are
different rules. The first agrees with the repository's independent reading and with `07`; the
second does not appear anywhere else. **Neither is quotable until read at the raw text.** The
repo's §4.2 statement ("matched on residue count and diameter ... one-sided") is therefore
carried as `[repo]` here, not confirmed. `PMC5007447` closes it.

Two count discrepancies are likewise unresolved and are recorded, not used. My APOP fetch
returned "84% success rate (42/50 proteins)" for holo where the repo records 92/104; and it
returned an apo figure of "86% (11/14-15)" against the repo's 11/14. The **success criterion**
sentence reproduced verbatim and is what §3.2 of the evaluation README actually relies on, so
nothing load-bearing moves. KeyAlloSite's 56.0 / 76.0 / 96.0 % reproduced exactly.

## B.6 One corroboration the repo should take, from the pocket side **[NEW]**

`06` §Headline caveat 4 argues, from Beltran 2026 on Src, that the negative class contains
unknown real positives. The same admission exists in **P2Rank's own text** `[FT]`: "It is naive
to assume that in our datasets all possible binding sites are demarked by bound ligands. That is
to say that many locations labeled as negatives (non-binding sites) in the datasets may be
binding sites yet to be discovered."

P2Rank is far more widely cited than Beltran and is not an allostery paper, so it makes the
point without depending on one deep-mutational-scanning result. Use both.

---

# Part C — what the repository must change or add, ranked

Ranked by how much a hostile reviewer's verdict moves per unit of work. Items 1–3 are single
paragraphs. Nothing here requires a freeze to move; items 4–7 are report-layer or
descriptive-endpoint additions.

1. **Cite Amor's Wilcoxon rank-sum as the in-domain precedent for the confirmatory statistic.**
   `doi:10.1038/ncomms12477` `[FT]`, "residues within 3.5 Å of the allosteric inhibitor have
   significantly higher propensities than non-allosteric residues (Wilcoxon rank sum,
   P<0.0005)". One sentence in `../evaluation/README.md` §3.1, and one edit to §12.3, which
   currently concedes the precedent is "adjacent and thin" when a residue-level rank test exists
   in a paper the section already cites. **[NEW]**

2. **Publish the occupant instrument for clauses (iii) and (x).** Neither clause defines
   _ligand_ or _component_, and the three published instruments — name list (PocketMiner
   `[FT]`), < 60 Da (CryptoBank `[FT]`), ≥ 10 heavy atoms (Wankowicz `[FT]`) — disagree on
   glycerol, sulfate, acetate and PEG. State which the repo uses. This is the one question in
   the brief that the frozen documents cannot currently answer. **[NEW]**

3. **Say, in the report, that clause (iii)'s scoreable-portion restriction is the repository's
   own invention and name the arms that depend on it.** Site-level apo is published; restricting
   the check to a sub-region of the site is published nowhere. `../primary/README.md` §1 already
   calls it a relaxation and that framing is correct; the report must carry it forward rather
   than leave it in the freeze.

4. **Print DCC with its definition attached, and print DCA separately.** P2Rank's "DCC" is
   centre-to-atom `[FT]`; STINGAllo's is centre-to-centre `[FT]`; Utgés & Barton recommend
   10–12 Å for the latter `[FT]`. Without a naming statement the repo's DCC column will be read
   against the wrong comparator. Also correct `07`'s STINGAllo row: 60.2 % overall, 77.8 %
   conditional. **[NEW]**

5. **Convert `site_pocket_rank` into the field's success rate.** The modal metric across the
   whole census is a top-3 pocket hit rate (APOP `[FT]`, KeyAlloSite `[FT]`, P2Rank `[FT]`), and
   CAPASP's fifth dimension is "ranking capability" `[ABS]`. The repo computes the rank and never
   reports "success at top-3: yes/no", which is the only form a reviewer can compare. Report it
   descriptively, with the detector and version named, exactly as the protocol already does for
   the rank. This does not test it and breaks no freeze.

6. **Report F1, MCC and residue-set IoU on the assembled site (stage S7), descriptive only.**
   The comparators are all verified here: STINGAllo F1 0.64 / MCC 0.64 `[FT]`, CryptoBench's
   seven-metric panel `[FT]`, AlloBench's Jaccard sweep `[FT]`, CAPASP's five dimensions
   `[ABS]`, UniSite's AP@IoU `[ABS]`. At fixed k = 5 the repo's reason for declining them is
   correct and should stay; on a variable-size assembled site it does not apply, and this is the
   only route to a number commensurable with published work. Independently reaches `07`
   recommendation 5, with the comparator values re-verified.

7. **Foreground the chance lines as a contribution, not a footnote.** Of eleven papers read at
   source, two report any chance line and none reports one for a top-N success rate (§B.2). The
   report should state that count and then print E[precision@5] and P(≥ 1 hit) beside every
   top-5 number. **[NEW]**

8. **Widen the shell-radius table to 3.5–8 Å** and add KeyAlloSite's 8 Å allosteric fallback
   `[FT]`. The repo currently records 3.5–6 Å, which understates the incomparability it is
   arguing for. **[NEW]**

9. **Report the pair Cα RMSD per arm.** CryptoBank admits a pair only below 2.5 Å `[FT]`; the
   repo has no conformational-distance admission rule at all. One number per arm, disclosed
   beside clause (viii), answers the objection without adding a clause. **[NEW]**

10. **Either raise clause (iv) to 95 % or state that it never binds.** 90 % is the loosest
    published pairing threshold — against PocketMiner's 100 % `[FT]`, Wankowicz's exact-sequence
    rule `[FT]` and CryptoBank's 95 % `[FT]` — and the arms sit at 97.6–100 %, so nothing
    depends on it. Also stop quoting CryptoSite's 40 % and CryptoBench's 10 % as pairing
    thresholds: the first is a redundancy filter and the second is a train/test split rule
    `[FT]`. **[NEW]**

11. **Add P2Rank's own negative-class admission** beside Beltran 2026 as corroboration that the
    negative class is contaminated `[FT]`. It makes the point from the pocket-prediction
    mainstream rather than from one DMS study. **[NEW]**

12. **Record that PDBbind is not a source for this question.** It has no apo member, no
    allosteric annotation, and its rules are quality rules for a bound complex `[SEARCH]`. The
    brief asks about it; the honest entry is one line, not silence.

**Not recommended.** Do not adopt Kincore's > 6.5 Å rule as a clause: it classifies a ligand in
a holo structure, is kinase-scoped, and makes no functional demand, so it contradicts clause
(ii) `[FT]`. Do not adopt an entry-level apo rule: it would reject all eight frozen apo
structures `[repo]` and the site-level reading is the one the task requires. Do not add a
minimum site-separation distance: ASD v1 `[FT]`, IUPHAR XC `[FT]` and CASBench's 30 % overlap
`[FT]` are three independent reasons against it.

---

## What this pass could not settle

1. **Amor's surrogate matching rule**, verbatim. Two fetches of the same paper returned
   different rules (§B.5). _Closes by: reading Methods at PMC5007447 raw._
2. **APOP's holo success counts** — 42/50 fetched here against 92/104 in the repo. _Closes by:
   reading the results tables at PMC10185404 raw._
3. **AHoJ's own numeric site threshold.** The main text states none; the 4.5 Å default is known
   only through CryptoBench's description `[FT]`. _Closes by: reading AHoJ's supplementary
   information._
4. **ASBench's rules** are `[SEARCH]` only. The repo already records that its criteria are
   paywalled and its licence forbids redistribution.
5. **PDBbind's refined-set rules** are `[SEARCH]` only; the primary methodology paper was not
   fetched. Nothing in Part C depends on the detail.
6. **CAPASP-Unbound's definition of "apo"** remains `[UNKNOWN]`, as `06` also found.
7. **UniSite's IoU thresholds** were not visible in the fetched abstract; `07a` records 0.3 and
   0.5 and that is carried `[repo]`.
8. **Whether any paper reports a chance line for top-N that I did not read.** Eleven papers is a
   sample, not a census. The claim in §B.2 is scoped to what was read and must stay scoped.

---

## Bibliography

Fetched this session, in the order they are first used.

- Christopoulos A, et al. International Union of Basic and Clinical Pharmacology XC.
  _Pharmacol Rev_ 2014;66(4):918–947. `doi:10.1124/pr.114.008862`. PMC11060431. `[FT]`
- Huang Z, Zhu L, Cao Y, et al. ASD: a comprehensive database of allosteric proteins and
  modulators. _Nucleic Acids Res_ 2011;39:D663–D669. `doi:10.1093/nar/gkq1022`. PMC3013650. `[FT]`
- Huang Z, et al. ASD v2.0. _Nucleic Acids Res_ 2014;42:D510–D516. `doi:10.1093/nar/gkt1247`. `[FT]`
- Huang W, et al. ASBench: benchmarking sets for allosteric discovery. _Bioinformatics_
  2015;31(15):2598–2600. `doi:10.1093/bioinformatics/btv169`. `[SEARCH]`
- Zlobin A, Suplatov D, Kopylov K, Švedas V. CASBench. _Acta Naturae_ 2019;11(1):74–80.
  `doi:10.32607/20758251-2019-11-1-74-80`. PMC6475866. `[FT]`
- AlloBench: A Data Set Pipeline for the Development and Benchmarking of Allosteric Site
  Prediction Tools. _ACS Omega_ 2025;10(17):17973–17982. `doi:10.1021/acsomega.5c01263`.
  PMC12059942. `[FT]`
- Cimermancic P, et al. CryptoSite. _J Mol Biol_ 2016;428(4):709–719.
  `doi:10.1016/j.jmb.2016.01.029`. PMC4794384. `[FT]`
- Vít Škrhák et al. CryptoBench. _Bioinformatics_ 2025;41(1):btae745.
  `doi:10.1093/bioinformatics/btae745`. PMC11725321. `[FT]`
- Febrer Martinez P, Fröhlking T, Borsatto A, Gervasio FL. CryptoBank. _Sci Adv_
  2026;12(17):eady6364. `doi:10.1126/sciadv.ady6364`. PMC13267282. `[FT]`
- Feidakis CP, et al. AHoJ. _Bioinformatics_ 2022;38(24):5452–5453.
  `doi:10.1093/bioinformatics/btac701`. PMC9750100. `[FT]`
- Feidakis CP, et al. AHoJ-DB. _J Mol Biol_ 2024;436:168545. `doi:10.1016/j.jmb.2024.168545`.
  metadata `[FT]`, content `[repo]`
- Meller A, et al. PocketMiner. _Nat Commun_ 2023;14:1177. `doi:10.1038/s41467-023-36699-3`.
  PMC9977097. `[FT]`
- Wankowicz SA, et al. _eLife_ 2022;11:e74114. `doi:10.7554/eLife.74114`. `[FT]`
- Modi V, Dunbrack RL. Kincore. _Nucleic Acids Res_ 2022;50(D1):D654–D664.
  `doi:10.1093/nar/gkab920`. PMC8728253. `[FT]`
- Liu Z, et al. PDBbind. _Bioinformatics_ 2015;31(3):405–412.
  `doi:10.1093/bioinformatics/btu626`. `[SEARCH]`
- Ai Y, Li H, Huang X, Liu S. CAPASP. _J Comput Aided Mol Des_ 2026;40(1):122.
  `doi:10.1007/s10822-026-00831-4`. PMID 42126486. `[ABS]`
- Krivák R, Hoksza D. P2Rank. _J Cheminform_ 2018;10:39. `doi:10.1186/s13321-018-0285-8`.
  PMC6091426. `[FT]`
- Utgés JS, Barton GJ. Comparative evaluation of methods for the prediction of protein–ligand
  binding sites. _J Cheminform_ 2024;16:126. `doi:10.1186/s13321-024-00923-z`. PMC11552181. `[FT]`
- Xu Y, Wang S, Hu Q, et al. APOP. _Bioinformatics_ 2023;39(5):btad275.
  `doi:10.1093/bioinformatics/btad275`. PMC10185404. `[FT]`
- Tan ZW, et al. KeyAlloSite. _eLife_ 2023;12:e81850. `doi:10.7554/eLife.81850`. `[FT]`
- Mariano DCB, et al. STINGAllo. _Brief Bioinform_ 2025;26(4):bbaf424.
  `doi:10.1093/bib/bbaf424`. PMC12368853. `[FT]`
- Amor BRC, Schaub MT, Yaliraki SN, Barahona M. Prediction of allosteric sites and mediating
  interactions through bond-to-bond propensities. _Nat Commun_ 2016;7:12477.
  `doi:10.1038/ncomms12477`. PMC5007447. `[FT]`
- UniSite. NeurIPS 2025. `arXiv:2506.03237`, `doi:10.48550/arXiv.2506.03237`. `[ABS]`

Cited from the repository's own evidence base without re-verification here: ESSA
`doi:10.1016/j.csbj.2020.06.020`; AlloPred `doi:10.1186/s12859-015-0771-1`; Clark 2019
`doi:10.1371/journal.pcbi.1006705`; Beltran et al. `doi:10.1126/sciadv.aea2726`; Riedlová et al.
`doi:10.1021/acs.jctc.6c00427`; Seq2Pocket `doi:10.64898/2026.01.28.702257`; Fenton
`doi:10.1016/j.tibs.2008.05.009`; Vajda et al. `doi:10.1016/j.cbpa.2018.05.003`.
