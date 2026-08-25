# What formally constitutes an apo/holo pair for allosteric-site identification

**Scope.** The allostery domain's own standards, read from its primary sources. This
review deliberately does **not** rest on the cryptic-pocket literature (CryptoSite,
PocketMiner, CryptoBench, AHoJ); where a point is only addressed by an adjacent field it
is marked **[BORROWED]** and named as such.

## Normative repository definition (verbatim from `docs/benchmark/README.md`)

> An **apo/holo pair for allosteric-site prediction** is an ordered pair of experimentally
> determined structures of the same gene product satisfying:
>
> **(i) Effector [IN-DOMAIN + REPOSITORY POLICY].** The _holo_ member contains the allosteric effector, identified by its PDB
> chemical component ID, at the site to be predicted; site residues are those within a
> **declared** radius of its heavy atoms.
> **(ii) Provenance of label [IN-DOMAIN + REPOSITORY POLICY].** The site is allosteric because _functional_ evidence says so.
> Distance from the active site is neither necessary nor sufficient. (ASD v1 pairs the
> functional requirement with a _topographic_ one — the site must be "topographically distinct
> from the orthosteric functional site" — so this clause narrows ASD rather than restating it,
> and it does so because ~30 % of CASBench's allosteric sites border the catalytic site.)
> **(iii) Site-apo [BORROWED + REPOSITORY POLICY].** The _apo_ member contains **no ligand of any kind within the
> _scoreable_ portion of that site** — the labels a method is actually asked to find. Contacts
> to the full label set are recorded beside it and do not disqualify: where the allosteric and
> orthosteric sites share a border, the catalytic cofactor touches labels that are *themselves*
> active-site residues, which is two sites adjoining, not a modulator in the pocket.
> **(iv) Identity [IN-DOMAIN].** Same protein at **≥ 90 % sequence identity**, differences enumerated.
> **(v) Assembly [IN-DOMAIN].** Same oligomeric state, and the modelled state should _be_ the biological
> assembly. (Both halves are the field's. An earlier version of this clause claimed the second
> half as **ours** — "no source states it" — while `docs/benchmark/evidence/curation-standard.md` already
> carried AlloBench stating it, `[VERIFIED-FULLTEXT]`. Corrected 2026-08-21.)
> **(vi) Second site [REPOSITORY POLICY].** Orthosteric occupancy recorded for **both** members, and the
> active-site rule stated.
> **(vii) Non-circularity [BORROWED + REPOSITORY POLICY] — a rule about the _procedure_, not about the biology.** No residue
> of the propagation source may be scored as a candidate for the site being predicted. The
> allosteric site is free to act _on_ the source; that is what allostery to a catalytic site
> **is**. Each arm declares which function the site is allosteric for, and whether that
> function is measured at the source (see below).
> **(viii) State disclosure [REPOSITORY POLICY].** The functional state of each member is **stated**, and the
> pocket-lining change reported. State difference is _disclosed, not required_.

Comparator blindness is deliberately outside this definition because it is a property of an
evaluation procedure. The remainder of this document supplies the clause-by-clause evidence;
it does not introduce a second definition (ADR 0017).

**Verification tags.** Every claim carries one:

- `[VERIFIED-FULLTEXT]` — read from the OA full text (Europe PMC `fullTextXML`).
- `[VERIFIED-FULLTEXT-PMC]` — read from the rendered PMC article page, because the entry is
  `inEPMC: Y` but `isOpenAccess: N`, so `fullTextXML` returns 404. Same body text, different
  route. The route is recorded per source, because it is not reproducible from the DOI alone.
- `[VERIFIED-ABSTRACT]` — abstract or indexed record only; the full text was not retrievable.
- `[VERIFIED-PARTIAL]` — publisher landing page gave part of the body but not the section needed.
- `[UNVERIFIED]` — stated by a secondary source, not confirmed at the primary source.
- `[NOT-RETRIEVABLE]` — attempted and failed; the reason is recorded.

**Retrieval failures, recorded rather than glossed.** These are the sources this question
needs that could not be opened from this environment. One was later resolved and is kept in
the table with its resolution, because a reader who finds the old claim needs the trail:

| Source                                           | Why                                                                                                                                                                                                                                                  |
| ------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ASD / ASBench web servers (`mdl.shsmu.edu.cn`)   | TLS certificate expired; the available fetch tool force-upgrades HTTP to HTTPS and has no plain-HTTP path. Confirmed: `certificate has expired`. A `curl http://…` from a shell would work (ADR 0003 open item).                                     |
| ASBench Supplementary Information (Huang 2015)   | The paper states its construction rules live in the SI; the SI is paywalled. OUP landing page gave partial body text only.                                                                                                                           |
| Fenton 2008 TIBS                                 | Not in the Europe PMC OA subset (`fullTextXML` → 404); publisher sites returned 403. **The Fenton four-complex framework is instead verified from Fenton's own 2024 OA restatement** (McCullagh et al., below), which is a stronger citation anyway. |
| ~~IUPHAR XC (Christopoulos 2014)~~ **RESOLVED 2026-08-24** | Was listed here for the same reason. It is `inEPMC: Y`, `isOpenAccess: N`, so `fullTextXML` 404s and `efetch` refuses — but the rendered page `pmc.ncbi.nlm.nih.gov/articles/PMC11060431/` serves the full body. Table 1 and Section III are now read and quoted in §1. |
| IUPAC Gold Book entry 14107                      | **Still unread.** `goldbook.iupac.org` returns 403 to every automated fetch (Anubis bot protection), `old.goldbook.iupac.org` fails the TLS handshake, three CORS proxies returned 522 or timed out, and `web.archive.org` is blocked for this tool although a snapshot `20260511182612` exists. Crossref gives the title and the parent recommendation and no definition text. |

**One correction to the brief.** ASD v2.0 is `doi:10.1093/nar/gkt1247`, not `gkt1092`
`[VERIFIED-FULLTEXT]`. ASBench is `doi:10.1093/bioinformatics/btv169` (PMID 25810427; no PMCID).

---

## 1. The allosteric site, formally defined

### 1.1 ASD, the field's reference database — definitions across five releases

Every ASD release opens with a definition, and they are **not identical**. The drift is
worth seeing, because the later ones drop the experimental-evidence clause the first one
carried.

**ASD v1** — Huang Z et al., _NAR_ 2011, `doi:10.1093/nar/gkq1022`, PMC3013650
`[VERIFIED-FULLTEXT]`:

> "Allostery, namely allosteric regulation, describes the regulation of protein function,
> structure and/or flexibility induced by the binding of a ligand at a site topographically
> distinct from the orthosteric site. Such site is then defined as an allosteric site."
> _(Introduction)_

**This is the only ASD release that states its inclusion criteria in the paper**:

> "With at least three cases of experimental evidence in crystal structure complex or
> biochemistry (inactive mutation of allosteric residue, cooperativity of kinetic effect
> from two ligands and uncompetitive-binding assay with chromatography, etc.), 336 proteins
> supporting their functional change elicited by modulator binding at a site that was
> topographically distinct from the orthosteric functional site, were verified as allosteric
> proteins for deposition into the ASD." _(Materials and Methods)_

Note what this criterion **is**: functional-change evidence, of which crystallography is
only one admissible kind, and mutagenesis and kinetics are the others. It is a
_functional_, not a _structural_, admission test. Radius rule: **ABSENT** in v1. Apo/holo:
**ABSENT** in v1.

**ASD v2.0** — Huang Z et al., _NAR_ 2014, `doi:10.1093/nar/gkt1247`, PMC3965017
`[VERIFIED-FULLTEXT]`:

> "Allostery is a fundamental process that regulates a protein's functional activity through
> the induction of changes in its conformation and dynamics in response to the perturbation
> of an effector at a site distinct from the active site, also termed the allosteric site."

**This is where the radius rule appears, and it is the only place in the ASD lineage that
states one:**

> "The residues constituting an allosteric site are automatically extracted from a complex
> structure by **6 Å** around allosteric modulator in the site using Pymol and manually
> inspected."

And for the orthosteric site:

> "all residues constituting the orthosteric site are detected by the fpocket algorithm
> around the annotated residues and manually checked."

The unit of deposition is a triple, not a pair:

> "For each allosteric protein-modulator complex, three structural files in pdb format were
> constructed from the original PDB structure: the allosteric site, the allosteric site bound
> to the modulator and the corresponding orthosteric site (if available) of the protein."

And a discriminating property between the two site classes:

> "allosteric sites evolved under lower sequence-conservation pressure compared with the
> evolutionarily conserved orthosteric sites."

**ASD v3.0** — Shen Q et al., _NAR_ 2016, `doi:10.1093/nar/gkv902`, PMC4702938
`[VERIFIED-FULLTEXT]`:

> "Allostery, an intrinsic property of a protein, is referred to as the regulation of activity
> at one site (also known as an orthosteric site) in a protein by a topographically and
> spatially distant site; the latter is designated as an allosteric site."

> "Allosteric regulation occurs through binding of a modulator (e.g., small molecule) at an
> allosteric site to engender a conformational change that affects function at the orthosteric
> site."

Curation criteria: **ABSENT** ("collected using previously described methods"). Radius rule:
**ABSENT**. See §2.1 for v3.0's apo/holo material, which is the single most relevant passage
in the whole ASD lineage.

**ASD 2019 release** — Liu X et al., _NAR_ 2020, `doi:10.1093/nar/gkz958`, PMC7145546
`[VERIFIED-FULLTEXT]`:

> "describes the existence of indirect coupling between two topographically and spatially
> distinct types of binding sites: allosteric and orthosteric sites"

> "The binding of effectors (e.g. small molecules, ions, and DNA/RNA) to an allosteric site
> enables a protein to propagate perturbations from an allosteric site to an orthosteric site"

> "10081 potential allosteric sites predicted from 4013 human proteins were constructed using
> our AllositePro method"

Curation criteria: **ABSENT**. Radius: **ABSENT**. Apo/holo: **ABSENT**.

**ASD2023** — He J et al., _NAR_ 2024, `doi:10.1093/nar/gkad915`, PMC10767950
`[VERIFIED-FULLTEXT]`:

> "Allosteric regulation, also known as allostery, is a prevalent phenomenon in which the
> functional site of a macromolecule is fine-tuned by distant allosteric sites in response to
> various perturbations" _(Introduction)_

> "Allosteric sites, which are topologically distinct from functional sites, are commonly
> found in most proteins" _(§3.1)_

> "In ASD2023, we conducted a comprehensive prediction of the entire human proteome,
> comprising 20,386 proteins, using AlloSitePro. This endeavor culminated in the construction
> of the 'Human Allosteric Pocketome,' a collection of 66,589 potential allosteric sites"

> "Notably, >70% of the proteins revealed allosteric sites with a high potential for molecular
> targeting and drug development (allosite score > 0.6)"

> "Dualsteric modulators represent an innovative class of chemical ligands that simultaneously
> bind to both the allosteric and orthosteric sites of a protein" _(§3.4)_

Curation criteria: **ABSENT**. Radius: **ABSENT**.

**Reading of the ASD lineage.** The definition is _relational and topographic_: a site is
allosteric **because binding there changes function at another site**, and the two sites are
"topographically distinct". No release states a distance threshold between the two sites.
The only geometric rule anywhere in the lineage is the **6 Å modulator shell** in v2.0, and
it defines _which residues belong to a site already known to be allosteric_ — it does not
decide _whether_ a site is allosteric. **How ASD decides a site is allosteric rather than
orthosteric is, in the published record, the v1 functional-evidence rule and expert
curation. There is no algorithm.**

A related 6 Å usage is confirmed in the ASD group's own methods paper — Lu S et al.,
_PLoS Comput Biol_ 2014, `doi:10.1371/journal.pcbi.1003831`, PMC4161293
`[VERIFIED-FULLTEXT]`:

> "The binding site residues for the allosteric and substrate ATP molecules were identified
> from those within **6 Å** of ATP using a fpocket-based pocket detection algorithm."

and it restates the v1 admission rule:

> "ASD v2.0 has manually curated allosteric proteins and allosteric modulators with at least
> three cases with experimental evidence, crystal structure of the complex or biochemical data."

### 1.2 ASBench

Huang W et al., _Bioinformatics_ 2015, `doi:10.1093/bioinformatics/btv169`, PMID 25810427.
No PMCID, not OA. `[VERIFIED-ABSTRACT]` + `[VERIFIED-PARTIAL]` from the OUP landing page.

Abstract `[VERIFIED-ABSTRACT]`:

> "Here, we report benchmarking data for experimentally determined allosteric sites through a
> complex process, including a 'Core set' with 235 unique allosteric sites and a
> 'Core-Diversity set' with 147 structurally diverse allosteric sites."

From the body text visible on the OUP page `[VERIFIED-PARTIAL]`:

> "A set of rules was applied to select the qualified allosteric sites and remove site
> redundancy, yielding the 'Core set' composed of 235 representative complexes"

> "the structural similarity of the allosteric sites in the 'Core set' was assessed, and 147
> structural complexes with diverse allosteric sites were further extracted to constitute the
> 'Core-Diversity set'"

The diversity filter uses a **Pocket Similarity score (PS-score)**; the reported effect is
that the maximum pairwise PS-score falls from 0.976 (Core set) to 0.491 (Core-Diversity set),
starting from 1,743 allosteric complexes in ASD v2.0 as of July 2014. And, decisively:

> "Detailed information about the process is provided in the 'Materials and Methods' of
> Supplementary Information"

**So ASBench's construction protocol is not in its paper.** The "set of rules" is never
enumerated in the retrievable record. This matters: ASBench is the training or evaluation
set for AlloPred, KeyAlloSite, ZHMolEReP and (via ASD) the PASSer family, and its selection
rules are effectively unauditable without the paywalled SI.

**ASBench's site-residue radius is 4 Å**, reported by a third party who worked with the
files — Wu, Strömich & Yaliraki, _Patterns_ 2022, PMC8767309 `[VERIFIED-FULLTEXT]`, quoting
their own reading of ASBench:

> "The allosteric sites are generally large in size based on the definition provided in the
> ASBench database (residues within **4 Å** from the allosteric ligand)."

This is `[UNVERIFIED]` at the primary source. It is corroborated independently by AlloBench
(§1.4), which regenerates ASD-derived allosteric sites at 4 Å.

### 1.3 CASBench

Zlobin A, Suplatov D, Kopylov K, Švedas V, _Acta Naturae_ 2019,
`doi:10.32607/20758251-2019-11-1-74-80`, PMC6475866 `[VERIFIED-FULLTEXT]`. 91 entries.

**Construction, verbatim:**

> "The protocol employed to collect the CASBench dataset contained four key steps: (1)
> numbering of allosteric site residues in the ASD was synchronized with the numbering of
> amino acid residues in the corresponding representative PDB structures; (2) for each protein
> in the ASD, all its structures in the PDB were retrieved; (3) the ASD entries were compared
> to the CSA entries to identify proteins deposited in both databases; and (4) annotations of
> catalytic and allosteric sites in the ASD and CSA databases were refined using information
> about the presence of ligands in all collected PDB structures of crystallographic complexes
> and taking into account the quaternary structure of each protein (when available)."

**Site-definition radius is 5 Å, applied twice:**

> "For each protein present in both the ASD and CSA databases, the collected information on all
> its structures in the PDB was used to select ligands bound to corresponding sites within
> **5 Å** of any amino acid residue included in the primary annotation."

> "In each structure, all residues located within **5 Å** of the selected ligand were considered
> and the resulting secondary annotations of each site were merged for all the PDB structures
> of the protein."

The merge across all PDB structures of the protein is a design choice worth noting: a CASBench
site is a **union over the whole structural ensemble deposited for that protein**, not a
property of one coordinate file.

**Catalytic/allosteric separation statistic — the field's only published number on this:**

> "In 30% of cases, the catalytic and allosteric sites either overlap or share a common border;
> in 70% of entries, both sites reside at a considerable distance from each other and do not
> overlap within the structure."

**Exclusions:**

> "Proteins that were present in the ASD but not in the CSA (i.e., none of the PDB structures
> retrieved at the previous stage was annotated in the CSA) were excluded from further
> consideration."

> "All entries in the ASD whose automatic synchronization had failed (i.e., it was not possible
> to conclusively identify the allosteric site in the PDB structure given the ASD numbering)
> were removed from analysis."

Redundancy: `"The amino acid sequences of all proteins presented in the PDB were clustered at a
95% sequence similarity level using the CD-HIT program."` Resolution limit: **ABSENT**.
Apo requirement: **ABSENT**.

### 1.4 AlloBench (the 2025 successor, and the most explicit protocol in the field)

Maity D, Qiao B, _ACS Omega_ 2025, `doi:10.1021/acsomega.5c01263`, PMC12059942
`[VERIFIED-FULLTEXT]`. 2,141 allosteric sites / 2,034 structures / 418 unique chains; 100-protein
test subset.

**Allosteric site rule:**

> "allosteric sites were obtained by locating the residues within **4 Å** of the allosteric
> modulator in the PDB structures."

**Active site**: taken from **UniProt and M-CSA annotations**, not from a radius —
`"The active site residue numbers are from the UniProt sequence."` No distance rule is given.

**Filters, verbatim:** resolution `"better than 4 Å"`; mmCIF-only entries dropped; multi-model
files merged; missing residues rebuilt with ProMod3 and kept only if `"lDDT < 0.8 were removed"`;
`"Only the entries with small-molecule allosteric modulators were selected"`; `">8000 residues"`
and nucleic-acid-containing structures dropped.

**Leakage control** — the strongest in the field:

> "The UniRef50 cluster IDs (UniProt reference clusters with at least 50% sequence identity) were
> obtained for the 268 unique UniProt IDs of these proteins. AlloBench proteins with these
> UniRef50 cluster IDs were dropped to remove any related proteins in addition to the proteins of
> the training sets."

**And the sentence that decides what AlloBench's "apo" actually is:**

> "Finally, the heteroatoms in the PDB files were removed, and only the protein chains were
> retained to create a test set of 100 protein structures."

**AlloBench's inputs are holo structures with the heteroatoms deleted.** It contains no
apo/holo pairing step at all; the words "apo", "holo", "unbound" do not appear in its
methodology.

### 1.5 What each predictor uses as its site definition

Compiled from full texts where OA. **The disagreement between rows is the finding.**

| Method                                                                         | Site definition used                                                                                                                                                                                                                               | Training / eval set                                                                                                                                                           | Structural state it runs on                                                                                                                                                                                                                  | Success criterion                                                                                                    |
| ------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| **Allosite** (2013) `doi:10.1093/bioinformatics/btt399` `[VERIFIED-PARTIAL]`   | not stated in accessible text                                                                                                                                                                                                                      | `"Ninety crystal structures of non-redundant allosteric proteins with a resolution better than 3 Å were carefully extracted from ASD"`                                        | not stated                                                                                                                                                                                                                                   | `"accuracies on test sets are all >95%"`, sens/spec >83%                                                             |
| **AllositePro** (2017) `doi:10.1021/acs.jcim.7b00014` `[VERIFIED-ABSTRACT]`    | not stated                                                                                                                                                                                                                                         | ASD                                                                                                                                                                           | not stated                                                                                                                                                                                                                                   | `"combining pocket features with perturbation analysis"`; allosite score, threshold 0.6 used in ASD2023              |
| **AlloPred** (2015) PMC4619270 `[VERIFIED-FULLTEXT]`                           | Fpocket pocket containing ≥1 ASBench allosteric-binding residue: `"389 (18 % of pockets, average 3.3 per protein) contained at least one residue identified as binding to an allosteric modulator and were hence labelled as allosteric pockets."` | ASBench Core-Diversity → 119 proteins, 79 train / 40 test                                                                                                                     | **Not stated. The strings "apo", "holo", "unbound" do not occur in the paper.**                                                                                                                                                              | top-1: 23/40; top-2: 28/40                                                                                           |
| **PARS** (2012/2014) PMC3562710 `[VERIFIED-FULLTEXT]`                          | `"its center less than 5 Å away from the allosteric ligand"` (pocket-centroid match)                                                                                                                                                               | 213 entries (146 ASD + 72 literature) → BLASTCLUST 30 % → 91 proteins                                                                                                         | Same coordinates, ligand present vs computationally absent: `"apo, the Cα only 'apo' protein crystallographic structure (allosteric ligand is not present); ligand, same protein structure as in 'apo' but including the allosteric ligand"` | positive predictive value; 65 % PPV at strict settings                                                               |
| **Amor et al.** (2016) PMC5007447 `[VERIFIED-FULLTEXT]`                        | `"Residues within 3.5 Å of the allosteric inhibitor"` (caspase-1 case)                                                                                                                                                                             | 20 proteins: `"Ten of these proteins were taken from a benchmark set collected by Daily et al. and a further seven were obtained through an extensive literature search."`    | explicit functional states, e.g. `"fully activated CheY (PDB ID: 1F4V) bound to Mg²⁺, BeF₃ and FliM"`, `"inactive conformation apo-CheY (PDB: 1CYE)"`                                                                                        | quantile score > 0.90; `"Nineteen out 20 allosteric sites are identified by at least one measure"`                   |
| **Ohm** (2020) PMC7395124 `[VERIFIED-FULLTEXT]`                                | site given as input                                                                                                                                                                                                                                | 20 proteins from Amor et al.                                                                                                                                                  | single static structure; `"We used the unphosphorylated state of CheY (PDB ID: 1JBE)"`                                                                                                                                                       | true-positive ratio of predicted hotspots; `"The average TPR of Ohm is 0.57, compared to 0.23 of Amor's method."`    |
| **PASSer** (2023) PMC10320119 `[VERIFIED-FULLTEXT]`                            | **nearest pocket, not a radius**: `"we define the pocket nearest to the modulator as the allosteric site and all other pockets as non-allosteric sites"`; `"Those proteins were removed if the closest pocket to the modulator is >10 Å."`         | ASD 1,949 → filters (`>3 Å` resolution out; missing residues in the allosteric site out; `"sequence identity threshold ≥ 30%"` out) → 207 proteins; CASBench as external test | **Not stated. "apo", "holo", "bound", "unbound" do not occur in the paper.**                                                                                                                                                                 | precision / recall / F1 + `"percentage of actual allosteric sites ranked in top 1 and 3 positions"`                  |
| **PASSer2.0** (2022) `doi:10.3389/fmolb.2022.879251` `[VERIFIED-ABSTRACT]`     | as PASSer                                                                                                                                                                                                                                          | as PASSer                                                                                                                                                                     | not stated                                                                                                                                                                                                                                   | `"82.7% of allosteric pockets appearing among the top three positions"`                                              |
| **PASSerRank** (2023) `doi:10.1002/jcc.27193` `[VERIFIED-ABSTRACT]`            | as PASSer                                                                                                                                                                                                                                          | ASD + CASBench                                                                                                                                                                | not stated                                                                                                                                                                                                                                   | top-3: `"83.6% and 80.5% of test proteins"`                                                                          |
| **DeepAllo** (2025) PMC12145174 `[VERIFIED-FULLTEXT]`                          | residue-level inherited from ASD pockets: `"Each residue in an allosteric pocket was labeled as allosteric."` No geometric overlap threshold is given for pocket-level positives.                                                                  | ASD → `"resolution below 3 Å"`, `"no missing residues"`, MMseqs2 `<30%` identity → 207 proteins, random 80/20                                                                 | **Not stated. No apo/holo discussion.**                                                                                                                                                                                                      | F1 89.66 %; `"90.5% confidence among the top 3 positions"`; threshold `"a pocket must have atleast 0.5 probability"` |
| **AlloReverse** (2023) PMC10320067 `[VERIFIED-FULLTEXT]`                       | AdaBoost over pocket-like regions                                                                                                                                                                                                                  | ASD-derived                                                                                                                                                                   | **input is `"a protein structure with orthosteric ligand bound"`**                                                                                                                                                                           | `"could recall 71.0% labeled allosteric sites and could re-emerge at least one allosteric site for 77.6% proteins"`  |
| **APOP** (2023) PMC10185404 `[VERIFIED-FULLTEXT]`                              | visual check that the known allosteric ligand sits in a top-3 pocket                                                                                                                                                                               | AlloPred test set + ESSA apo/holo set + literature; 61 monomers, 43 multimers                                                                                                 | **`"Our allosteric pocket predictions are based on holo-structures formed simply by removing any ligand(s)."`** plus a separate 14-case apo test                                                                                             | `"If this pocket is among the top-ranked three predicted pockets, we count it as a success."`                        |
| **ESSA** (2020) PMC7330491 `[VERIFIED-FULLTEXT]`                               | Fpocket pocket containing the allosteric ligand                                                                                                                                                                                                    | Dataset I: 25 monomers from two curated sets. Dataset II: see §2.3                                                                                                            | both; holo-with-ligand-stripped **and** true apo, scored separately                                                                                                                                                                          | `"only the allosteric sites detected in the top 3 predictions among all pockets are labelled as successful"`         |
| **KeyAlloSite** (2023) PMC9981151 `[VERIFIED-FULLTEXT]`                        | orthosteric pocket = `"residues within 6 Å around the ATP molecule"`; allosteric sites from ASBench                                                                                                                                                | ASBench Core Set, filtered to 23 proteins / 25 sites (see §2.3)                                                                                                               | `"For applications, we recommend to use the holo structure whenever possible."`                                                                                                                                                              | recall 0.92 at Z-score > 0.5                                                                                         |
| **MEF-AlloSite** (2024) PMC11515501 `[VERIFIED-ABSTRACT]`                      | pocket-level, 9,460 features                                                                                                                                                                                                                       | 90 proteins                                                                                                                                                                   | not stated                                                                                                                                                                                                                                   | average precision + ROC AUC; Student's t and Cohen's d                                                               |
| **STINGAllo** (2024/2025) PMC11570862, PMC12368853 `[VERIFIED-ABSTRACT]`       | **residue-level**, no pocket required                                                                                                                                                                                                              | ASD-derived                                                                                                                                                                   | not stated                                                                                                                                                                                                                                   | `"Distance Center Center (DCC) success rate"`, F1, MCC; 78 % / 60 % / 64 % / 64 %                                    |
| **ZHMolEReP** (2026) `doi:10.1021/acs.jcim.6c00141` `[VERIFIED-ABSTRACT]`      | residue-level, PRS-based                                                                                                                                                                                                                           | ASBench; AlloReverse as independent test                                                                                                                                      | not stated                                                                                                                                                                                                                                   | recall 0.7037, AUC 0.7858, 33/40 proteins                                                                            |
| **AlloScore** (2016) `doi:10.1093/bioinformatics/btw036` `[VERIFIED-ABSTRACT]` | — (scores affinity, not site location)                                                                                                                                                                                                             | —                                                                                                                                                                             | allosteric complex                                                                                                                                                                                                                           | binding-affinity correlation                                                                                         |
| **AlloFinder** (2018) `doi:10.1093/nar/gky374` `[VERIFIED-ABSTRACT]`           | AllositePro sites                                                                                                                                                                                                                                  | ASD                                                                                                                                                                           | not stated                                                                                                                                                                                                                                   | not extracted                                                                                                        |

**Three incompatible site definitions are in simultaneous use** — 3.5 Å (Amor), 4 Å (ASBench,
AlloBench, Riedlová), 5 Å (CASBench), 6 Å (ASD v2.0, KeyAlloSite orthosteric) — plus two
non-radius definitions (PASSer's _nearest pocket_, AlloPred's _any pocket containing ≥1 contact
residue_). A number reported against one is not comparable to a number reported against another.

### 1.6 Consensus / nomenclature-level definitions

**IUPAC, _Glossary of terms used in medicinal chemistry_ (1998), `doi:10.1351/pac199870051129`**
`[VERIFIED-FULLTEXT]` (entries A–H):

> "**Allosteric binding sites** … are contained in many enzymes and receptors. As a consequence
> of the binding to Allosteric binding sites, the interaction with the normal ligand may be
> either enhanced or reduced."

> "**Allosteric enzyme** is an enzyme that contains a region to which small, regulatory molecules
> ('effectors') may bind in addition to and separate from the substrate binding site and thereby
> affect the catalytic activity."

> "**Allosteric regulation** is the regulation of the activity of allosteric enzymes."

The glossary has **no entry** for "allosteric site" (singular), "allosterism", "allosteric
modulator" or "orthosteric" in A–H. Its definition is functional-and-relational: the site is
defined by its _effect on the normal ligand's interaction_, not by geometry.

**IUPHAR XC** — Christopoulos A et al., _Pharmacol Rev_ 2014, 66(4):918–947,
`doi:10.1124/pr.114.008862` `[VERIFIED-FULLTEXT-PMC]`, retrieved 2026-08-24.

**This entry read `[NOT-RETRIEVABLE]` until 2026-08-24 and the warning below stood. It was
superseded by a retrieval, not by a recollection.** Route, recorded so the next reader does
not repeat the dead ends: Europe PMC gives PMID 25026896 and **PMCID PMC11060431**, but
`isOpenAccess: N`, so `.../PMC11060431/fullTextXML` returns 404 and NCBI `efetch` returns
"The publisher of this article does not allow downloading of the full text in XML form."
The **working** route is the rendered page, `https://pmc.ncbi.nlm.nih.gov/articles/PMC11060431/`.

Two passages matter, and they have **different scopes**. Quoting the wrong one imports a scope
clause no target in this repo satisfies.

**Table 1**, captioned "Terms used to describe **receptor** allosterism and allosteric ligand
actions (see also Note 1)". Verified word for word, including that "nonoverlapping" is one word:

> **Allosteric site** — "A binding site on a receptor macromolecule that is nonoverlapping and
> spatially distinct from, but conformationally linked to, the orthosteric binding site."

This is **receptor-scoped**, in the receptor-theory sense: GPCR, ligand-gated ion channel,
nuclear receptor. KRAS, ABL1, cardiac myosin and c-Myc are none of those. Cite Table 1 and a
reviewer can reject the scope in one line.

**Section III, "Definitions"** — the same article, the same authority, and **protein-general**:

> "It is recommended that the term 'allosteric' _not_ be used to describe such phenomena but be
> reserved for instances where the properties of one ligand **(small molecule or protein)** are
> altered upon binding of a second ligand at a nonoverlapping, topographically distinct site and
> where, **ideally**, reciprocity in this interaction can be demonstrated."

The bolded parenthetical is the clause that makes the sentence protein-general, and the repo
dropped it once without an ellipsis. **This is the passage clause (ii) rests on**, not Table 1.

Three things the retrieval settles:

1. **Reciprocity is a preference, not a threshold.** The sentence carries two requirements —
   properties of one ligand altered by a second, at a nonoverlapping and topographically
   distinct site — and one preference, marked by "ideally". A benchmark that _excludes_ a site
   for want of demonstrated reciprocity is stricter than IUPHAR XC and may not cite XC for it.
2. **No minimum distance, anywhere in the article.** Every criterion is topological:
   "nonoverlapping", "spatially distinct", "topographically distinct". Not metric.
3. **Bitopic engagement is explicitly allowed**, and it is competitive: "A bitopic mode of
   engagement involves the (single) ligand occupying both sites at the same time and thus would
   still exhibit competitive behavior because one of the pharmacophores occupies the orthosteric
   site." So competitive kinetics alone do not refute an allosteric site.

**Unchecked.** Table 1's "Note 1" was not retrieved, so anything that note qualifies is unread.

**Fenton's energy-cycle definition — the one that actually answers question 2.**
McCullagh M, Zeczycki TN, Kariyawasam CS, Durie CL, Halkidis K, Fitzkee NC, Holt JM, Fenton AW,
_J Biol Chem_ 2024, `doi:10.1016/j.jbc.2024.105672`, PMC10897898 `[VERIFIED-FULLTEXT]`:

> "allosteric regulation is the through-protein energetic coupling between two protein–ligand
> interactions"

> "using a protein example, allosteric regulation is the modified function involving one ligand
> that interacts in the primary functional site that is caused when a second ligand is bound to
> a distinct site on the protein."

> "The primary functional site is an active site or an orthosteric site. The altered function is
> ligand binding or catalysis. The second ligand-binding site is often called an allosteric site
> and the second ligand, an allosteric effector."

> "**Allosteric site (effector site):** The binding site on the protein to which the allosteric
> effector binds."

> "**Orthosteric site:** This a term taken from the receptor field that is a general term for the
> site of function."

---

## 2. The apo/holo pair in allostery — the core question

### 2.1 Does the field even define one? Yes, once, and it is under-specified

**ASD v3.0 is the only database source that names the object** `[VERIFIED-FULLTEXT]`:

> "Identification of the origin of the conformational transitions in protein by the modulator is
> highly dependent on comparing the structure of the allosteric sites **before binding (apo
> structure)** with that **after binding (holo structure)**."

> "In ASD v3.0, 1688 allosteric _apo_/_holo_ paired structures for allosteric modulator action in
> 308 proteins from 107 organisms were constructed using the same protocol described in ATP action"

> "Of the 1688 allosteric _apo_/_holo_ paired structures, **92.6% and 5.9%** allosteric sites showed
> **local motions in backbone** and **in sidechain**, respectively upon the binding of modulators."

So ASD's sense of the pair is unambiguous on **one** axis: **apo = without the allosteric
modulator; holo = with it.** The pair is _modulator-relative_, not globally ligand-free.

**The protocol, however, is not published.** ASD v3.0 defers to `"see Supporting Information"`
and to the ATP-action paper. Lu et al. 2014 (PMC4161293) `[VERIFIED-FULLTEXT]` was read in full
for exactly this, and it contains only:

> "Ten out of thirteen allosteric ATP unbound structures were retrieved from the PDB"

> "3D structural alignment of the allosteric ATP-bound and unbound structures"

> "The resulting 500 structures were superimposed using all Cα atoms to remove overall rotation
> and transition"

It gives **no** sequence-identity threshold for pairing, **no** RMSD threshold, **no**
motion-classification cutoff distinguishing "backbone motion" from "sidechain motion" from
"none", and **no** named superposition tool for the pairing step. **The 92.6 % / 5.9 % figures
therefore rest on an unpublished threshold.** This is the field's canonical apo/holo statistic
and it is not reproducible from the literature.

### 2.2 Must the apo be free of the allosteric modulator, or of all ligands?

**Free of the allosteric modulator. No allostery source requires global ligand-freedom.** The
evidence, and note how far it goes in the _other_ direction:

- **ASD v3.0** `[VERIFIED-FULLTEXT]`: apo = `"before binding"` the modulator. Silent on other ligands.
- **PARS** (Panjkovich & Daura 2012) `[VERIFIED-FULLTEXT]` — apo is defined _only_ with respect to
  the allosteric ligand, and is literally the same coordinate file:
  > "apo, the Cα only 'apo' protein crystallographic structure (allosteric ligand is not present);
  > ligand, same protein structure as in 'apo' but including the allosteric ligand (or a simplified
  > molecular representation) in the allosteric site"
- **APOP** `[VERIFIED-FULLTEXT]`: `"Our allosteric pocket predictions are based on holo-structures
formed simply by removing any ligand(s)."`
- **AlloBench** `[VERIFIED-FULLTEXT]`: `"the heteroatoms in the PDB files were removed, and only the
protein chains were retained"`.
- **ESSA** `[VERIFIED-FULLTEXT]`: `"the latter being generated by removing the ligand(s) in silico"`.
- **KeyAlloSite** `[VERIFIED-FULLTEXT]` goes the opposite way and requires the _holo_ to be a
  **ternary** complex: `"(2) the corresponding three-dimensional protein structure data should
contain both allosteric ligand and orthosteric ligand"`.

**The dominant practice in the allostery field is not to use an apo structure at all.** Four of
the tools benchmarked in AlloBench (APOP, AlloPred, PASSer, Allosite) and AlloBench itself are
evaluated on **holo coordinates with the heteroatoms deleted**. Only ESSA and APOP separate the
two cases and report them separately, and only ESSA quantifies the difference (§2.5).

**[BORROWED — cryptic-pocket field]** The site-relative apo reading, and the argument that
deleting a ligand does not delete its conformational imprint, is stated explicitly in the
cryptic-site literature (AHoJ `doi:10.1093/bioinformatics/btac701`; PocketMiner
`doi:10.1038/s41467-023-36699-3`) and in `docs/benchmark/README.md` §1. **It is not stated
anywhere in the allostery sources reviewed here.** Our repo's clause (ii) is therefore an
import from an adjacent field, and must be labelled as such in the report.

### 2.3 What is required of the conformational / functional state of each member?

This is the question with the least published guidance and the largest consequences. What
exists:

**(a) A sequence-identity pairing rule — the only explicit one found.**
ESSA (Kaynak, Bahar & Doruker, _CSBJ_ 2020, PMC7330491) `[VERIFIED-FULLTEXT]`:

> "a second dataset, Dataset II, composed of 24 structures, mainly the bound and unbound forms of
> 12 proteins from the Dataset I, for which there was **an apo structure resolved for the same
> protein with at least 90% sequence identity**."

That is the field's only stated apo↔holo matching criterion. It constrains **identity**, not
**state**.

**(b) A functional-state exclusion rule — the only one found.**
Amor et al., _Nat Commun_ 2016, PMC5007447 `[VERIFIED-FULLTEXT]`:

> "(Five proteins in ref. 56 could not be used due to the presence of non-standard amino-acids, to
> the absence of an allosteric ligand, or to **a mismatch between the oligomeric state of the active
> and inactive structures**.)"

Amor et al. work explicitly with **active and inactive structures** and exclude a pair when the
two members disagree in oligomeric state. This is the closest the field comes to a
functional-state clause, and it is a one-line parenthesis. It also demonstrates that the working
unit in that dataset is an active/inactive pair — e.g. `"inactive conformation apo-CheY (PDB:
1CYE)"` against `"fully activated CheY bound to the phosphate mimic BeF₃ (PDB: 1DJM)"`.

**(c) A ternary-complex requirement.** KeyAlloSite (Xie et al., _eLife_ 2023, PMC9981151)
`[VERIFIED-FULLTEXT]` requires the structure to hold **both** ligands (quoted in §2.2). This is
the structural analogue of the EXA complex of the energy cycle.

**(d) The reversed sense — the pair defined on the _orthosteric_ ligand.**
AlloReverse (Zha et al., _NAR_ 2023, PMC10320067) `[VERIFIED-FULLTEXT]`:

> "RAE of a residue is then defined as its change of residue–residue interactions in the pocket
> between the **apo and orthosteric ligand-bound (holo)** states."

In AlloReverse, "holo" means **orthosteric-bound**, the opposite of ASD's usage. The word alone
does not identify which ligand is meant.

**(e) An explicit statement that state difference is a nuisance rather than a requirement.**
KeyAlloSite `[VERIFIED-FULLTEXT]`:

> "For Q152, its Z-score is slightly smaller than the threshold of 0.8, though with a high ranking.
> This indicates that conformational changes do have subtle influence on the predicted results."

> "When the conformational changes between apo and holo states are not large, the influence on the
> results is small."

> "For applications, we recommend to use the holo structure whenever possible."

Ohm `[VERIFIED-FULLTEXT]` says the same in the other direction:

> "Although Ohm uses only the static tertiary structure of a protein as input, under conditions
> where conformational change is induced the allosteric pathway calculated by Ohm is stable."

**Verdict on the state question.** _No source in the allostery domain requires the apo and holo
to represent different functional states, and none requires them to represent the same state._
The field's pairing rules constrain **identity** (≥90 % sequence, same protein) and **ligand
occupancy** (modulator absent/present). Functional state enters exactly once, as Amor's
oligomeric-state exclusion. **A benchmark whose apo is already in the modulator-stabilised state
violates no published criterion of the allostery field.** It is nonetheless a fatal defect for a
prediction task, and the argument for that has to be made from first principles plus:

- **the field's own measured penalty** (§2.5, ESSA 10/14 → 7/14), and
- **the borrowed cryptic-site threshold** `[BORROWED]` (CryptoBench 2 Å pocket-lining RMSD,
  `doi:10.1093/bioinformatics/btae745`), already applied in `docs/benchmark/README.md` §4.

There is one further reason the allostery field cannot impose a state-difference requirement,
and it is principled rather than an oversight: **allostery does not require conformational
change.** Lee & Sapienza, _Biochemistry_ 2026, PMC13001099 `[VERIFIED-ABSTRACT]` —
`"thermally activated, rapid-time scale dynamics can underlie allosteric ligand binding
cooperativity, even in the absence of conformational change"`; Sun et al., _J Phys Chem B_ 2025,
PMC12400411 `[VERIFIED-ABSTRACT]` — `"allostery without (measurable) conformational change"`;
Campitelli et al., _JMB_ 2025 `[VERIFIED-ABSTRACT]` — `"dynamic allostery—where protein function
is modulated through alterations in thermal fluctuations without major conformational shifts"`.
A benchmark that _required_ apo↔holo conformational change would exclude dynamic allostery by
construction. This is a real tension, not a loophole, and it should be stated rather than
resolved by fiat.

### 2.4 Must the orthosteric / active site be occupied, empty, or either?

**Either, in practice, and the choice is never justified.** But the _methods_ split on it:

- **Methods that need the active site as a perturbation source** must locate it, and differ on
  whether they need its ligand. Ohm `[VERIFIED-FULLTEXT]`: `"the algorithm perturbs residues in
the active site"`; and, for the ligand-free case, `"We recommend to use all residues on the
active site for the unbound structure."` Wu et al. `[VERIFIED-FULLTEXT]` had to fall back:
  `"as orthosteric ligands are not available in structures from the ASBench database, the
orthosteric site residues were selected as the perturbation source instead."`
- **The ligand matters measurably.** Wu et al. `[VERIFIED-FULLTEXT]`:
  `"The allosteric site is recovered for 127 of 146 proteins (407 of 432 structures) knowing only
the orthosteric sites or ligands."` and, on CASBench, `"Knowing the orthosteric ligands of the
protein, the allosteric site is identified for 32/33 proteins (308/314 structures)"` versus
  `"32/33 proteins (304/314 structures)"` from residues alone. Their conclusion:
  `"The specific ligand-site interactions are crucial for accurate allosteric site detection…the
method is sensitive to specific interactions between the ligand and the protein."`
- **AlloPred** `[VERIFIED-FULLTEXT]` excludes the active site from perturbation to avoid a
  circularity we should copy: `"Active site residues were not counted as being in any pocket for
this alteration of k, in order to avoid direct perturbation of the site at which the effect was
measured."`
- **AlloReverse** `[VERIFIED-FULLTEXT]` _requires_ orthosteric occupancy: input is
  `"a protein structure with orthosteric ligand bound"`.
- **KeyAlloSite** `[VERIFIED-FULLTEXT]` requires **both** ligands present.

**No source states a rule.** Whether the active site must be occupied is a free parameter of the
allostery field, and it interacts directly with ADR 0005 (our source term is derived from the apo
entry's own cofactor or from catalytic motifs — which is the Ohm/Wu fallback, and is therefore in
line with published practice).

### 2.5 The four-complex requirement (Fenton), and what it says about a two-structure benchmark

Verified from Fenton's 2024 OA restatement rather than the 2008 original (which is
`[NOT-RETRIEVABLE]`). McCullagh … Fenton, _JBC_ 2024, PMC10897898 `[VERIFIED-FULLTEXT]`:

> "an allosteric energy cycle provides a quantifiable allosteric coupling constant and focuses our
> attention on the unique properties of the **four equilibrated protein complexes** that constitute
> the energy cycle."

> "A, a simple allosteric energy cycle. … E will be used for protein. A is substrate and X is
> effector. Kia and Kix are equilibrium binding constants for A and X in the absence of the other
> ligand. Kia/x and Kix/a are binding constants for A and X with saturating X and A, respectively."

The four complexes are **E, EA, EX, EXA**. The coupling constant:

> "Qax = Kia/Kia/x = Kix/Kix/a"

> "Qax quantifies the extent of the allosteric response, that is, the magnitude of how much X
> binding influences the binding of A or how much A binding changes when X is absent versus is
> present."

**And the direct verdict on a two-structure comparison:**

> "any changes in the conformation or dynamics/ensemble that are identified by comparing only the
> E and XE complexes are not likely to provide the insights needed to define the allosteric
> mechanism fully."

> "Therefore, comparisons of only two complexes are not likely to identify all changes that are
> relevant to the allosteric mechanism"

> "rather than equating allosteric regulation with ligand binding (which is the comparison of only
> two enzyme complexes as exemplified in the E and EA comparison), the energy cycle approach
> defines allosteric regulation of a K-type system as a change in the binding of A caused by the
> presence of bound X."

**No structural database or benchmark implements the four-complex requirement.** The nearest
approach is KeyAlloSite's demand for a ternary (EXA) structure, which supplies one corner of the
cycle rather than all four. **This is the single largest gap between how allostery is _defined_
and how allosteric-site benchmarks are _built_, and stating it is a strength of our report, not a
weakness of our benchmark.** An apo/holo pair is, in Fenton's terms, an E↔EX comparison: it can
localise an effector site and its structural response, but it cannot by itself establish that the
site is allosteric. That establishment comes from the _curation_ evidence behind the label
(ASD v1's `"at least three cases of experimental evidence"`), not from the pair.

---

## 3. What allostery researchers actually measure on a pair

Every entry names the tool, the source, and what is computed. Restricted to the allostery
literature.

### 3.1 Structural comparison

| Measure                                                                                     | Source                                           | What exactly is computed                                                                                                                                                                               |
| ------------------------------------------------------------------------------------------- | ------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Cα superposition to remove rigid-body motion                                                | Lu et al. 2014, PMC4161293 `[VERIFIED-FULLTEXT]` | `"superimposed using all Cα atoms to remove overall rotation and transition"` — global fit, then local inspection at the site                                                                          |
| Local backbone vs. sidechain motion at the allosteric site                                  | ASD v3.0, PMC4702938 `[VERIFIED-FULLTEXT]`       | `"92.6% and 5.9% allosteric sites showed local motions in backbone and in sidechain"` across 1,688 pairs. **Threshold unpublished.**                                                                   |
| RMSD between an alternative complex and the original, when reconstructing a ternary complex | ESSA, PMC7330491 `[VERIFIED-FULLTEXT]`           | `"the corresponding PDB id and root-mean-square deviation (RMSD) from the original complex"` — reported, no threshold stated                                                                           |
| Sequence identity between pair members                                                      | ESSA `[VERIFIED-FULLTEXT]`                       | `"at least 90% sequence identity"`                                                                                                                                                                     |
| Oligomeric-state agreement between the two members                                          | Amor et al. `[VERIFIED-FULLTEXT]`                | pair excluded on `"a mismatch between the oligomeric state of the active and inactive structures"`                                                                                                     |
| Pocket similarity between allosteric sites (redundancy control)                             | ASBench `[VERIFIED-PARTIAL]`                     | **PS-score**; Core-Diversity built by lowering max PS-score 0.976 → 0.491                                                                                                                              |
| Residue-set overlap between predicted and known site                                        | AlloBench `[VERIFIED-FULLTEXT]`                  | **Jaccard index**: `"It is 0 if there are no residues in common between K and P and is 1 if K and P are identical."`                                                                                   |
| Centroid distance between predicted and known site                                          | AlloBench `[VERIFIED-FULLTEXT]`                  | `"the inverse of the distance between the centroids of the Cα atoms"`; used to validate JI, `"The strong correlation between the JI and inverse distance indicates that the JI is a robust estimator"` |
| Pocket-centre-to-ligand distance                                                            | PARS `[VERIFIED-FULLTEXT]`                       | `"its center less than 5 Å away from the allosteric ligand; if more than one pocket matched the ligand position within this cut-off, the closest was chosen"`                                          |
| Distance-centre-centre success rate                                                         | STINGAllo `[VERIFIED-ABSTRACT]`                  | **DCC**, reported at 78 % when all allosteric residues fall inside an Fpocket pocket                                                                                                                   |

**Not found anywhere in the allostery literature reviewed:** DynDom, FATCAT, explicit hinge
detection, or any domain-motion decomposition applied to an allosteric apo/holo pair as part of
a benchmark protocol. Domain-motion tooling exists in the general protein-motion literature
(e.g. D3PM, `doi:10.1186/s12859-022-04595-0`, `"7679 proteins with overall motions"` and
`"3513 proteins with pocket residue motions"` `[VERIFIED-ABSTRACT]`) but is **[BORROWED]** —
it is not part of any allosteric-site benchmark.

### 3.2 Network and dynamics methods applied to apo vs. holo

| Method                                                                | Source                                                     | What exactly is computed                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| --------------------------------------------------------------------- | ---------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **NMA + ligand perturbation** (PARS)                                  | Panjkovich & Daura 2012, PMC3562710 `[VERIFIED-FULLTEXT]`  | NMA via `"PDBMAT and DIAGRTB"`; `"calculated B-factors for the Cα protein atoms of the apo structure were compared to those obtained for the same atoms in the configurations including real or simulated ligands to test for significant changes in flexibility using the Wilcoxon-Mann-Whitney test. Differences with a p-value<0.05 were considered significant."` **This is the only explicit null hypothesis + significance test in the allosteric-site prediction literature reviewed.**         |
| **ENM spring stiffening** (AlloPred)                                  | PMC4619270 `[VERIFIED-FULLTEXT]`                           | `"harmonic springs of strength k between every pair of C-alpha atoms no further than distance Rc apart"`; `"1 kcal mol⁻¹ Å⁻² and 15 Å for k and Rc"`; perturbed pocket springs raised to `"1.5 kcal mol⁻¹ Å⁻²"`; effect = `"averaging across all identified active site residues the magnitude of the difference between the perturbed and the unperturbed displacements"` per normal mode                                                                                                             |
| **GNM eigenvalue shift** (APOP)                                       | PMC10185404 `[VERIFIED-FULLTEXT]`                          | springs `"within a cutoff distance of 10 Å"`, `"γ = 1.0 kcal mol⁻¹ Å⁻²"`, pocket residues raised to `"10.0 kcal mol⁻¹ Å⁻² regardless of the distances"`; `"pockets are scored and ranked according to the computed eigenvalue shifts in the global GNM modes together with their local hydrophobic densities"`                                                                                                                                                                                         |
| **Essential site scanning** (ESSA)                                    | PMC7330491 `[VERIFIED-FULLTEXT]`                           | GNM 10 Å / ANM 15 Å cutoffs; `"we populated the vicinity of residue i by adding extra nodes at the positions of all its heavy atoms"`; `"an effective shift in global mode frequencies is defined for each residue as the mean over the softest ten modes"`                                                                                                                                                                                                                                            |
| **Perturbation-response scanning + free-energy response** (ZHMolEReP) | `doi:10.1021/acs.jcim.6c00141` `[VERIFIED-ABSTRACT]`       | `"integrates perturbation response scanning (PRS) with free energy response approximation, establishing a concise and physically grounded seven-feature representation"`                                                                                                                                                                                                                                                                                                                               |
| **Bond-to-bond propensity** (Amor et al.)                             | PMC5007447 `[VERIFIED-FULLTEXT]`                           | atomistic energy-weighted graph; `"consider all the ligand–protein interactions formed at the active site and compute their combined effect on each bond b outside of the active site"`; significance via **quantile regression**: `"The quantile score of a bond p_b is a measure of how high the propensity Π_b is relative to other bonds in the sample which are at a similar distance from the active site."` — **explicitly distance-corrected, which is the confound `docs/FIELD.md` §3 names** |
| **Perturbation propagation / ACI** (Ohm)                              | PMC7395124 `[VERIFIED-FULLTEXT]`                           | `"P_ij = 1 − e^{−α·N_ij}"` probability matrix, propagation `"repeated 10,000 times"`; `"the frequency with which each residue is affected by a perturbation…We call this frequency the allosteric coupling intensity (ACI)"`; hotspots by clustering on ACI                                                                                                                                                                                                                                            |
| **Residue allosteric effect (RAE) + pathway** (AlloReverse)           | PMC10320067 `[VERIFIED-FULLTEXT]`                          | `"RAE of a residue is…its change of residue–residue interactions in the pocket between the apo and orthosteric ligand-bound (holo) states"`; `"regulation pathway of a predicted site is defined to be the shortest route from an orthosteric ligand to the residue in site with the highest RAE, where 'distances' between residues are calculated as the reciprocal of their mean motion correlation"`                                                                                               |
| **Evolutionary coupling strength** (KeyAlloSite)                      | PMC9981151 `[VERIFIED-FULLTEXT]`                           | `"The ECS between the orthosteric pocket and the mth pocket is defined as the sum of the coupling strength between the residues in the two pockets."`; `"the Frobenius norm FN(i,j) of J_ij is used to measure the ECS between the two sites i and j"`                                                                                                                                                                                                                                                 |
| **Dynamic community / correlation** (DCI)                             | `doi:10.1093/bioinformatics/btac159` `[VERIFIED-ABSTRACT]` | `"protein residue dynamic cross-correlations generated by Gaussian elastic network models"`                                                                                                                                                                                                                                                                                                                                                                                                            |
| **Nanoenvironment descriptors** (STINGAllo)                           | PMC11570862 `[VERIFIED-ABSTRACT]`                          | 54 descriptors incl. `"sponge effect, distance to the protein centre of geometry (cg), hydrophobic interactions, electrostatic potentials, eccentricity, and graph bottleneck features"`                                                                                                                                                                                                                                                                                                               |

### 3.3 Pocket / site characterisation tools used in the allostery field

- **Fpocket** — the field default. ASD v2.0 uses it for orthosteric sites; AlloPred, ESSA, APOP,
  PASSer, STINGAllo all build on it. Both APOP and ESSA record it as a failure mode
  (§4). `[VERIFIED-FULLTEXT]`
- **LIGSITEcs** — PARS. `[VERIFIED-FULLTEXT]`
- **CAVITY** — KeyAlloSite: `"we used CAVITY to find the potential ligand binding pockets"`.
  `[VERIFIED-FULLTEXT]`
- **PyMOL** — ASD v2.0's 6 Å site extraction. `[VERIFIED-FULLTEXT]`
- **AlloSite score / AllositePro** — the ASD ranking; ASD2023 uses `"allosite score > 0.6"` as its
  "high potential" threshold. `[VERIFIED-FULLTEXT]`
- **AlloScore** — scores allosteric _affinity_, not site location
  (`doi:10.1093/bioinformatics/btw036`). `[VERIFIED-ABSTRACT]`
- **PS-score** — ASBench's pocket-similarity redundancy metric. `[VERIFIED-PARTIAL]`

### 3.4 The field's standard success criterion for an allosteric-site predictor

There are effectively **four**, and papers rarely report more than one:

1. **Top-N pocket rank.** The most common. `"If this pocket is among the top-ranked three
predicted pockets, we count it as a success"` (APOP); `"only the allosteric sites detected in
the top 3 predictions among all pockets are labelled as successful"` (ESSA); top-1 and top-2
   (AlloPred); top-1 and top-3 (PASSer, PASSer2.0 82.7 %, PASSerRank 83.6 %/80.5 %, DeepAllo
   90.5 %). All `[VERIFIED-FULLTEXT]` or `[VERIFIED-ABSTRACT]` as tabulated in §1.5.
2. **Overlap fraction.** AlloBench's **Jaccard index**, with `"the percentage of proteins in
their top predictions with JI larger than a varying threshold"` — i.e. a _curve_, not a single
   threshold. `[VERIFIED-FULLTEXT]`
3. **Distance to the true site.** PARS' 5 Å pocket-centre rule; STINGAllo's DCC.
4. **Residue-level classification metrics.** F1 (DeepAllo, `"the performance was evaluated using
F1 score mainly"`), MCC (STINGAllo 64 %; Riedlová `"MCC offers a particularly informative
measure as it balances true and false predictions across all classes and remains reliable under
skewed label distributions"`), AUROC and AUPR, average precision (MEF-AlloSite).

**AUC alone is a minority practice in this field and is increasingly criticised within it.**
Riedlová et al. 2026 `[VERIFIED-FULLTEXT]` report both and show why: distal Type IV allosteric
sites give `"a near-random ranking regime (AUROC = 0.676)"` while `"Type III AUPR dropped to
0.363 and Type IV to 0.077"`, concluding `"although some allosteric residues may be ranked above
background on average, the top-scoring predictions are overwhelmingly false positives."` This is
the allostery-domain version of the argument our `README.md` §5 makes from Saito & Rehmsmeier and
from cryptic-site numbers — **it is now available from inside the allostery field.**

**Statistical testing is essentially absent.** Of the full texts read, only PARS states a null and
a test (Wilcoxon–Mann–Whitney, p<0.05, on Cα B-factors) and only Amor et al. correct for the
distance-to-active-site confound (quantile regression against bonds `"at a similar distance from
the active site"`). Wu et al.'s six statistical measures are compared against fixed expectation
values (0.05, 0.5) and 95 % CIs, not against a spatial null. **No allosteric-site predictor
reviewed uses a permutation or matched-patch null.** Our patch null therefore has no precedent in
this field; the closest precedents remain CryptoSite's concave-patch control **[BORROWED]** and
Amor's distance-matched quantile regression, which is the better in-domain citation.

### 3.5 How the field quantifies "allosteric coupling" between two sites

| Quantity                                     | Source                                      | Definition                                                                                                                                                                                          |
| -------------------------------------------- | ------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Allosteric coupling constant Qax**         | McCullagh…Fenton 2024 `[VERIFIED-FULLTEXT]` | `"Qax = Kia/Kia/x = Kix/Kix/a"`; `"it can be converted to ΔGax, constituted by both ΔHax and TΔSax terms"`. **The thermodynamic ground truth. Not obtainable from structures.**                     |
| **Allosteric coupling intensity (ACI)**      | Ohm `[VERIFIED-FULLTEXT]`                   | frequency a residue is reached by perturbation propagated from the active site over 10,000 trials                                                                                                   |
| **Site–site coupling degree**                | AlloReverse `[VERIFIED-FULLTEXT]`           | `"the degree of site A coupled by site B is defined as the proportion of shared residues in the pathway toward site A, i.e. the coupling is usually asymmetric"` — reported as a 0–1 heatmap        |
| **Evolutionary coupling strength (ECS)**     | KeyAlloSite `[VERIFIED-FULLTEXT]`           | Frobenius norm of the coupling block between the two pockets' residues, summed                                                                                                                      |
| **Bond-to-bond propensity + quantile score** | Amor et al. `[VERIFIED-FULLTEXT]`           | non-local effect of bond fluctuations propagating from the active site, distance-normalised                                                                                                         |
| **Silent coupling**                          | McCullagh…Fenton 2024 `[VERIFIED-FULLTEXT]` | `"we have used 'silent coupling' to describe an implicated change in binding coordination but without a change in substrate affinity"` — a coupling that exists thermodynamically but shows Qax ≈ 1 |

---

## 4. What the field considers a defective pair

Published pitfalls, exclusion criteria and failure modes, quoted.

**Wrong or unusable annotations in ASBench** — Wu, Strömich & Yaliraki 2022 `[VERIFIED-FULLTEXT]`:

> "From those 12 [structures where detection failed], the orthosteric residues of three structures
> (PDB: 1UXV, 2VD3, and 3QH0) reported in the ASD database are **incorrect (they do not form a
> binding site)**, and those of one further structure (PDB: 2ATS) do not match with the data in
> ASBench."

**A fragment of an assembly, standing in for the assembly** — same source:

> "Six structures (PDB: 1M8P, 3D2P, 3DC2, 3HQP, 3R1R, and 4HYW) obtained from the ASBench are only
> one part of a large and complex multimeric protein, where the effect of cooperativity might play
> a crucial role."

This is directly our `9YRG` hexamer question (README §7).

**Oligomeric-state mismatch between the two members** — Amor et al. `[VERIFIED-FULLTEXT]`:
five proteins excluded for non-standard amino acids, `"the absence of an allosteric ligand"`, or
`"a mismatch between the oligomeric state of the active and inactive structures"`.

**A site the pocket detector cannot see** — the field's most-reported failure mode.
PARS `[VERIFIED-FULLTEXT]` discarded 36 % of its dataset for it:

> "we discarded a total of 33 proteins for which no single LIGSITEcs predicted pocket matched the
> allosteric site, leaving a total of 58 cases to work with (63,7%)."

> "not all allosteric sites are predicted to be potential ligand-binding cavities by common
> algorithms. There can be different reasons for this, for example the allosteric site may be
> deeply buried in the protein, may display a planar shape or be located at the interface of
> subunits"

APOP `[VERIFIED-FULLTEXT]`:

> "Our method's dependence on the Fpocket algorithm may be a limitation in some cases, such as in
> the ATP phosphoribosyltransferase (PDB ID: 1NH8) and Hemoglobin (PDB ID: 1B86) structures, where
> Fpocket failed to predict a pocket in the allosteric ligand-binding region."

ESSA `[VERIFIED-FULLTEXT]`: `"No pocket is detected around the allosteric ligand of ribonucleotide
reductase R1…The ligand binds to a mobile loop."`
STINGAllo `[VERIFIED-ABSTRACT]`: `"Traditional pocket-based predictors miss approximately 18% of
experimentally confirmed sites that lie outside surface invaginations."`

**The apo penalty, measured.** ESSA `[VERIFIED-FULLTEXT]` — the single most useful number in this
review for our purposes:

> "Calculations performed using the holo structure (in which the ligand has been removed _in
> silico_) as input showed that **10 out of 14** allosteric sites present in Dataset II are
> successfully predicted by ESSA…in the more challenging test of using **apo** structures as
> input, ESSA shows **7/14** success rate."

> "Conformational rearrangements in apo structures may result in cryptic pockets, i.e. those
> unavailable in the apo form, but becoming accessible upon conformational changes…these sites
> could not be detected by Fpocket."

APOP `[VERIFIED-FULLTEXT]` reports the same direction: `"Although conformational rearrangements
seem to affect the success rate of our predictions for apo structures, we still achieve a
satisfactory prediction rate of 86% (11/14)."`

**So the allostery field has measured the leak our C1 forbids, and quantified it at roughly a
30 % relative drop in top-3 success.** Any comparison of our numbers against published
allosteric-site predictor numbers must state whether the published number was obtained on a
ligand-stripped holo. For AlloBench, APOP's headline, AlloPred, PASSer, DeepAllo and Allosite,
it was or is not stated.

**"The same protein has different sites in different structures."** ESSA `[VERIFIED-FULLTEXT]`:

> "An inherent problem in the assessment of prediction algorithms based on current benchmarks or
> datasets, including the one in this study…there may be different binding sites that are resolved
> in alternative structures for the same protein."

**Databases are stale, incomplete and mutually inconsistent.** AlloBench `[VERIFIED-FULLTEXT]`:

> "ASBench and CASBench have become outdated and are significantly smaller compared to the latest
> version of ASD 2023. Due to the lack of updated data sets, new programs (especially AI-based
> tools) being developed for studying allostery are still using the outdated ASBench data set
> released 10 years ago."

> "the tab-delimited file had missing values in the column for allosteric site residues for 1620
> out of 3102 entries"

> "only 46% of entries have annotations for orthosteric sites, and only 209 unique orthosteric
> sites are present."

> "Although ASBench lists the allosteric site residues on its web server, such information is
> missing in the downloadable data set… Furthermore, ASBench does not contain the active site
> residues of the target proteins."

> "While CASBench does list multiple active sites and allosteric sites, the corresponding ligands
> or allosteric modulators are absent, which must be inferred from the PDB structure."

> "The lack of structures solved with bound substrates and allosteric modulators adds to the
> challenge of accurately identifying the allosteric and active sites."

**Train/test leakage is the field's least-controlled hazard.** AlloBench is the only source that
removes it at the protein-family level (UniRef50). DeepAllo `[VERIFIED-FULLTEXT]` provides
`"no explicit discussion of leakage prevention or redundancy analysis between train/test splits
beyond the initial 80/20 random division"`, on a set already filtered to <30 % identity.
Riedlová et al. `[VERIFIED-FULLTEXT]` do it properly:
`"For each test sequence, any training sequence with >30% sequence identity was identified… all
such training sequences were removed from the training set."`
**This confirms README §7's open item: PASSer/PASSerRank/DeepAllo are ASD-trained, and ASD curates
the ABL1 myristoyl site.** Any comparison against them on BCR-ABL1 is a comparison against a model
that has seen the answer.

**Class imbalance is extreme and is the reason ranking metrics mislead.** DeepAllo
`[VERIFIED-FULLTEXT]`: `"positive samples (pockets) accounted to only 304 or 7.76% of the dataset
(4223 pockets). Moreover, at the residue level, there were 5.12% positive labels"`. Riedlová
`[VERIFIED-FULLTEXT]`: `"extreme sparsity for allosteric ones (<3% of residues)"`;
`"Type IV (ALLO) complexes constitute only 675 structures in the full data set compared to 7,604
for Type I inhibitors."`

**And the field's own summary of why allosteric prediction is not orthosteric prediction** —
Riedlová et al. 2026 `[VERIFIED-FULLTEXT]`:

> "Both predictors exhibit a sharp and reproducible dichotomy on protein kinases, in which
> orthosteric ATP-binding sites can be identified with high precision, whereas allosteric sites are
> detected with substantially lower confidence across kinase structures and distinct conformational
> states."

> "robust detection of functional allosteric and cryptic binding sites remains elusive as most
> methods are optimized for stable, evolutionarily conserved orthosteric pockets, whereas allosteric
> sites are often transient, weakly conserved and sparsely populated in structural databases."

> "allosteric pockets occupy predominantly neutrally frustrated zones associated with conformational
> plasticity and reduced evolutionary constraint."

And the overall state of the art, from AlloBench's head-to-head of seven tools on a common,
leakage-controlled set `[VERIFIED-FULLTEXT]`:

> "The results show a significant need for improvement, as the accuracy for all programs is well
> below 60%, with PASSer (Ensemble) outperforming the rest."

---

## 5. Proposed formal definition, with each clause traced

> **An _apo/holo pair for allosteric-site prediction_ is an ordered pair of experimentally
> determined structures of the same gene product, satisfying:**
>
> **(i) Effector clause.** The _holo_ member contains the **allosteric effector of interest**,
> identified by its PDB chemical component ID, bound at the site to be predicted. The site is the
> protein residues within a **declared radius** of the effector's heavy atoms.
> — _ASD v2.0: `"extracted from a complex structure by 6 Å around allosteric modulator"`; CASBench
> 5 Å; ASBench/AlloBench 4 Å. The radius is a free parameter and must be declared, not assumed._
>
> **(ii) Provenance-of-label clause.** The site is allosteric because **functional evidence** says
> so, not because it is far from the active site. — _ASD v1: `"at least three cases of experimental
evidence in crystal structure complex or biochemistry (inactive mutation of allosteric residue,
cooperativity of kinetic effect from two ligands and uncompetitive-binding assay…)"`. A pair
> cannot establish allostery; it can only localise a site whose allostery was established
> elsewhere — McCullagh…Fenton 2024: `"comparisons of only two complexes are not likely to identify
all changes that are relevant to the allosteric mechanism"`._
>
> **(iii) Site-apo clause.** The _apo_ member contains **no ligand within the site defined in (i)**.
> — _Modulator-relative apo is the ASD sense (`"before binding (apo structure)"`). Global
> ligand-freedom is required by no allostery source. The stricter reading — that a structure
> crystallised with something in the pocket carries that pocket's conformation even after the atoms
> are deleted — is `[BORROWED]` from AHoJ/PocketMiner and must be labelled as an import._
>
> **(iv) Identity clause.** Both members are the same protein at **≥90 % sequence identity** over
> the modelled region, with every difference enumerated. — _ESSA: `"an apo structure resolved for
the same protein with at least 90% sequence identity"`. This is the field's only published
> pairing threshold._
>
> **(v) Assembly clause.** Both members have the **same oligomeric state**, and that state is the
> biological assembly. — _Amor et al. exclude on `"a mismatch between the oligomeric state of the
active and inactive structures"`; Wu et al. flag six ASBench entries that are `"only one part of a
large and complex multimeric protein, where the effect of cooperativity might play a crucial
role"`; CASBench refines annotations `"taking into account the quaternary structure of each
protein"`._
>
> **(vi) Second-site clause.** The occupancy of the **orthosteric/active site is recorded for both
> members**, and the rule by which the active site is located is stated. Physiological cofactors at
> the active site may be present in either member. — _Ohm: `"We recommend to use all residues on the
active site for the unbound structure."` Wu et al.: `"as orthosteric ligands are not available in
structures from the ASBench database, the orthosteric site residues were selected as the
perturbation source instead."` KeyAlloSite requires both ligands present. AlloReverse requires the
> orthosteric ligand present. The field does not agree; therefore the choice must be declared._
>
> **(vii) Non-circularity clause.** The active site used as the propagation source must not be
> perturbed by, or derived from, the site being predicted. — _AlloPred: `"Active site residues were
not counted as being in any pocket for this alteration of k, in order to avoid direct perturbation
of the site at which the effect was measured."`_
>
> **(viii) State-disclosure clause.** The functional/conformational state of each member is
> **stated** (active/inactive, R/T, autoinhibited/activated, DFG-in/out, phosphorylated or not), and
> the pair's pocket-lining RMSD is reported. It is **not required** that the states differ — dynamic
> allostery exists — but a pair whose apo is already in the effector-stabilised conformation must be
> declared as such, because the field's own measurements show it inflates performance.
> — _State difference is required by no allostery source; Amor et al. work with `"active and
inactive structures"`; ESSA measures the penalty at 10/14 (ligand-stripped holo) vs 7/14 (true
> apo); the no-conformational-change case is real (Lee & Sapienza; Sun et al.; Campitelli et al.).
> The 2 Å pocket-lining floor we apply is `[BORROWED]` from CryptoBench._
>
> **(ix) Blindness clause.** If a predictor was trained on ASD, ASBench or CASBench, and the target
> protein is in them, the comparison is not blind and must be labelled. — _AlloBench's UniRef50
> exclusion; Riedlová's 30 %-identity removal; DeepAllo's absence of any such control._

---

## 6. Consolidated checklist for a candidate pair

Ordered so that the cheapest disqualifier fires first. Each line names the source that motivates it.

**Read from the files, never from a table:**

1. **Chemical component ID of the effector is present in the holo file**, at the site claimed.
   _(AlloBench had to resolve `"discrepancies between the allosteric sites listed in ASD and the
location of the allosteric modulator in the PDB structure"`.)_
2. **Every non-water component in the apo file is enumerated**, with its minimum distance to the
   label set. _(ASD is silent on other ligands; only enumeration makes the pair auditable.)_
3. **Label set derived at the declared radius**, with 4/5/6 Å frozen alongside it so the field's
   three conventions are all recoverable. _(ASD 6 Å / CASBench 5 Å / ASBench 4 Å.)_
4. **The allosteric label has functional provenance**, cited. _(ASD v1's three-cases rule.)_
5. **Sequence identity apo↔holo ≥ 90 %**, differences enumerated, mutations inside the label set
   listed. _(ESSA.)_
6. **Oligomeric state matches**, and matches the biological assembly. _(Amor; Wu et al.; CASBench.)_
7. **Residue numbering synchronised** between the annotation source and the coordinates.
   _(CASBench removed every entry `"whose automatic synchronization had failed"` — the ADR 0004
   hazard, published.)_
8. **Active-site occupancy recorded for both members**; active-site rule stated and applied
   identically to every arm. _(Ohm; Wu et al.; ADR 0005.)_
9. **Active site excluded from the perturbation** it is being measured at. _(AlloPred.)_
10. **Pocket-lining RMSD apo↔holo reported**, fitted off the label residues; functional state of
    each member named. _(ASD v3.0's local-motion classification; `[BORROWED]` 2 Å floor.)_
11. **A geometric pocket detector is run on the apo and its failure recorded** — if no pocket
    covers the site, that is a property of the benchmark instance, not of the method.
    _(PARS discarded 33/91; APOP and ESSA both name specific failures; STINGAllo puts it at 18 %.)_
12. **Resolution and ligand-fit quality recorded**; alternate conformers and occupancy handled
    explicitly. _(Riedlová: `"exclusion of ligand atoms with occupancy <0.5"`, `"use of only the
highest-occupancy conformer"` — README §7 records ours as latent.)_
13. **Chain breaks, missing residues and modelled regions near the site recorded.**
    _(AlloBench rebuilt 1,287 of 2,034 structures and gated on lDDT ≥ 0.8; PASSer simply drops
    proteins with `"missing residues in the allosteric site"`.)_
14. **Label prevalence and the chance baseline reported with every top-N number.**
    _(DeepAllo 7.76 % pockets / 5.12 % residues; Riedlová <3 %; AUPR collapses where AUROC does not.)_
15. **Every baseline labelled blind or not blind** on this target. _(ASD-trained predictors.)_
16. **State whether any published comparator number was obtained on a ligand-stripped holo.**
    _(APOP, AlloBench, ESSA-holo. ~30 % relative inflation, measured by ESSA.)_

---

## 7. What the allostery field does _not_ specify — our choices to declare

Each of these is a genuine gap in the published record, not a gap in this search. For each, the
choice we must make and declare.

| #      | Unspecified                                                                                                               | Evidence that it is unspecified                                                                                                                                         | Our declared choice                                                                                                                                                                                                                                   |
| ------ | ------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **1**  | **The contact radius defining site residues.** Four values in simultaneous use.                                           | ASD v2.0 **6 Å**; CASBench **5 Å**; CryptoSite and PocketMiner **5 Å**; AHoJ and CryptoBench **4.5 Å**; ASBench/AlloBench/Riedlová **4 Å**; Amor **3.5 Å**. No source justifies its choice.                                                 | **4.5 Å heavy-atom**, with 4.0 and 5.0 frozen alongside as `cutoff_sensitivity` (ADR 0004). Stricter than ASD; **matches AHoJ and CryptoBench**; must be stated at first use. (Corrected 2026-08-24: this row omitted AHoJ and CryptoBench from the survey and therefore concluded "matches nothing exactly", contradicting `../README.md` §1. It also listed a 6.0 Å sensitivity value the manifest does not freeze.)                                                                                                          |
| **2**  | **Whether apo means modulator-free or ligand-free.**                                                                      | ASD: modulator-free. PARS/APOP/ESSA/AlloBench: the _same_ coordinates with heteroatoms deleted. No source defines site-relative apo.                                    | Site-apo (README §1), imported from AHoJ/PocketMiner and **labelled `[BORROWED]`**.                                                                                                                                                                   |
| **3**  | **Whether apo and holo must be different functional states.**                                                             | **No allostery source states a requirement in either direction.** Amor's oligomeric-state exclusion is the only state-aware criterion found.                            | Do **not** require a state difference (dynamic allostery would be excluded). **Do** require the state to be named and the pocket-lining RMSD reported, and apply the `[BORROWED]` 2 Å floor as a _reported diagnostic_, never as an inclusion filter. |
| **4**  | **A conformational-change threshold.** ASD's own 92.6 %/5.9 % backbone-vs-sidechain split rests on an unpublished cutoff. | ASD v3.0 defers to SI; Lu et al. 2014 contains no threshold.                                                                                                            | Report the pocket-lining RMSD distribution; do not reproduce ASD's classification.                                                                                                                                                                    |
| **5**  | **Whether the orthosteric site must be occupied.**                                                                        | KeyAlloSite: both ligands. AlloReverse: orthosteric bound. Ohm/Wu: residues suffice. PASSer/AlloPred/DeepAllo: not stated.                                              | Either is acceptable; occupancy is **recorded per arm** and the active-site rule (ADR 0005) is applied identically across arms.                                                                                                                       |
| **6**  | **How to locate the active site when no ligand is present.**                                                              | ASD uses `"fpocket…around the annotated residues"`; AlloBench uses UniProt + M-CSA; Ohm says use all active-site residues; no radius is ever given for the active site. | ADR 0005: cofactor 4.5 Å shell, else conserved catalytic motif located by sequence. **Note: no allostery source gives an active-site radius at all, so ADR 0005's rule is ours.**                                                                     |
| **7**  | **A resolution ceiling.**                                                                                                 | CASBench and ASBench state none. PASSer/DeepAllo 3 Å; AlloBench 4 Å; Riedlová 3 Å. No cryo-EM-specific rule anywhere.                                                   | README §7's proposal: X-ray ≤2.5 Å or cryo-EM ≤4.0 Å, mandated tier exempt. Not yet an ADR.                                                                                                                                                           |
| **8**  | **Sequence-identity de-duplication threshold.**                                                                           | CASBench CD-HIT **95 %**; PARS BLASTCLUST **30 %**; PASSer/DeepAllo/Riedlová **30 %**; AlloBench **UniRef50**. Span of 65 points.                                       | 30 % for the ASD generalisability set; not applicable at three hand-specified targets. Declare which.                                                                                                                                                 |
| **9**  | **The statistical null.**                                                                                                 | Only PARS states one (Wilcoxon–Mann–Whitney, p<0.05). Only Amor corrects for distance-to-active-site. **No permutation or spatial null anywhere.**                      | Matched patch null (README §5). **In-domain precedent: Amor's distance-matched quantile regression.** Cite that rather than only the `[BORROWED]` CryptoSite patches.                                                                                 |
| **10** | **The primary metric.**                                                                                                   | Top-1/top-2/top-3, Jaccard-vs-threshold curve, DCC, F1, MCC, AUROC, AUPR, average precision — all in use, rarely more than one per paper.                               | AUC-ROC + AUC-PR primary, precision@5 and P(≥1 hit) secondary (README §5). Report top-3 as well, because it is the field's most common currency and is what makes us comparable.                                                                      |
| **11** | **How to handle a site the pocket detector misses.**                                                                      | PARS discards (36 % of its data); APOP and ESSA report the failure; STINGAllo builds a residue-level method to avoid it.                                                | Our method is residue-level, so this does not bind us — but the decoy-pocket negative set (README §7) inherits the problem and must record detector failures rather than silently producing fewer decoys.                                             |
| **12** | **Whether a benchmark must implement the four-complex requirement.**                                                      | **No structural benchmark does.** KeyAlloSite's ternary requirement is the closest.                                                                                     | We cannot. State it explicitly: an apo/holo pair is an E↔EX comparison, the allosteric label comes from functional evidence outside the pair, and Qax is not obtainable from our inputs.                                                              |
| **13** | **Whether covalent modulators count.** | **The allostery field does rule on this.** AlloBench: "Structures with covalently bound allosteric modulators were removed" (`10.1021/acsomega.5c01263`, `[VERIFIED-FULLTEXT]`, §curation-standard.md:368) — in-domain, not borrowed. LiveCoMS "would not recommend including covalent ligands"; Binding MOAD and Clark et al. exclude them too. | Retain KRAS/sotorasib per README §1 deviation 2, but as a **declared deviation from an in-domain rule**, not a gap in the field. An earlier version of this row read "no allostery source addresses covalency" and "the allostery field gives us no rule either way"; both are withdrawn, and they had understated the objection to keeping the arm. |
| **14** | **What "the same protein" means across numbering conventions.**                                                           | CASBench simply deletes entries where synchronisation failed. No positive rule is given.                                                                                | ADR 0004: identity-and-label transfer through alignment, never through pinned residue numbers.                                                                                                                                                        |

---

## 8. Source ledger

| Source                                                     | Identifier                                       | Access                                                               |
| ---------------------------------------------------------- | ------------------------------------------------ | -------------------------------------------------------------------- |
| ASD v1 — Huang Z et al., _NAR_ 2011                        | `10.1093/nar/gkq1022` · PMC3013650               | `[VERIFIED-FULLTEXT]`                                                |
| ASD v2.0 — Huang Z et al., _NAR_ 2014                      | `10.1093/nar/gkt1247` · PMC3965017               | `[VERIFIED-FULLTEXT]`                                                |
| ASD v3.0 — Shen Q et al., _NAR_ 2016                       | `10.1093/nar/gkv902` · PMC4702938                | `[VERIFIED-FULLTEXT]`                                                |
| ASD 2019 — Liu X et al., _NAR_ 2020                        | `10.1093/nar/gkz958` · PMC7145546                | `[VERIFIED-FULLTEXT]`                                                |
| ASD2023 — He J et al., _NAR_ 2024                          | `10.1093/nar/gkad915` · PMC10767950              | `[VERIFIED-FULLTEXT]`                                                |
| ATP action — Lu S et al., _PLoS Comput Biol_ 2014          | `10.1371/journal.pcbi.1003831` · PMC4161293      | `[VERIFIED-FULLTEXT]`                                                |
| ASBench — Huang W et al., _Bioinformatics_ 2015            | `10.1093/bioinformatics/btv169` · PMID 25810427  | `[VERIFIED-ABSTRACT]` + `[VERIFIED-PARTIAL]`; SI `[NOT-RETRIEVABLE]` |
| CASBench — Zlobin A et al., _Acta Naturae_ 2019            | `10.32607/20758251-2019-11-1-74-80` · PMC6475866 | `[VERIFIED-FULLTEXT]`                                                |
| AlloBench — Maity D, Qiao B, _ACS Omega_ 2025              | `10.1021/acsomega.5c01263` · PMC12059942         | `[VERIFIED-FULLTEXT]`                                                |
| Wu N, Strömich L, Yaliraki SN, _Patterns_ 2022             | `10.1016/j.patter.2021.100408` · PMC8767309      | `[VERIFIED-FULLTEXT]`                                                |
| Amor BR et al., _Nat Commun_ 2016                          | `10.1038/ncomms12477` · PMC5007447               | `[VERIFIED-FULLTEXT]`                                                |
| Ohm — Wang J et al., _Nat Commun_ 2020                     | `10.1038/s41467-020-17618-2` · PMC7395124        | `[VERIFIED-FULLTEXT]`                                                |
| AlloPred — Greener JG, Sternberg MJ, _BMC Bioinf_ 2015     | `10.1186/s12859-015-0771-1` · PMC4619270         | `[VERIFIED-FULLTEXT]`                                                |
| PARS — Panjkovich A, Daura X, _BMC Bioinf_ 2012            | `10.1186/1471-2105-13-273` · PMC3562710          | `[VERIFIED-FULLTEXT]`                                                |
| PARS server — Panjkovich A, Daura X, _Bioinformatics_ 2014 | `10.1093/bioinformatics/btu002`                  | `[VERIFIED-ABSTRACT]`                                                |
| ESSA — Kaynak BT, Bahar I, Doruker P, _CSBJ_ 2020          | `10.1016/j.csbj.2020.06.020` · PMC7330491        | `[VERIFIED-FULLTEXT]`                                                |
| APOP — Kumar A et al., _Bioinformatics_ 2023               | `10.1093/bioinformatics/btad275` · PMC10185404   | `[VERIFIED-FULLTEXT]`                                                |
| PASSer — Tian H et al., _NAR_ 2023                         | `10.1093/nar/gkad303` · PMC10320119              | `[VERIFIED-FULLTEXT]`                                                |
| PASSer2.0 — Xiao S et al., _Front Mol Biosci_ 2022         | `10.3389/fmolb.2022.879251` · PMC9309527         | `[VERIFIED-ABSTRACT]`                                                |
| PASSerRank — Tian H et al., _J Comput Chem_ 2023           | `10.1002/jcc.27193` · PMC11127606                | `[VERIFIED-ABSTRACT]`                                                |
| DeepAllo — Khokhar M et al., _Bioinformatics_ 2025         | `10.1093/bioinformatics/btaf294` · PMC12145174   | `[VERIFIED-FULLTEXT]`                                                |
| AlloReverse — Zha J et al., _NAR_ 2023                     | `10.1093/nar/gkad279` · PMC10320067              | `[VERIFIED-FULLTEXT]`                                                |
| KeyAlloSite — Xie J et al., _eLife_ 2023                   | `10.7554/eLife.81850` · PMC9981151               | `[VERIFIED-FULLTEXT]`                                                |
| Allosite — Huang W et al., _Bioinformatics_ 2013           | `10.1093/bioinformatics/btt399`                  | `[VERIFIED-PARTIAL]`                                                 |
| AllositePro — Song K et al., _JCIM_ 2017                   | `10.1021/acs.jcim.7b00014`                       | `[VERIFIED-ABSTRACT]`                                                |
| AlloFinder — Huang M et al., _NAR_ 2018                    | `10.1093/nar/gky374` · PMC6030990                | `[VERIFIED-ABSTRACT]`                                                |
| AlloScore — Li S et al., _Bioinformatics_ 2016             | `10.1093/bioinformatics/btw036`                  | `[VERIFIED-ABSTRACT]`                                                |
| MEF-AlloSite — Ugurlu SY et al., _J Cheminform_ 2024       | `10.1186/s13321-024-00882-5` · PMC11515501       | `[VERIFIED-ABSTRACT]`                                                |
| STINGAllo — Omage FB et al., _CSBJ_ 2024                   | `10.1016/j.csbj.2024.10.036` · PMC11570862       | `[VERIFIED-ABSTRACT]`                                                |
| STINGAllo server — Omage FB et al., _Brief Bioinform_ 2025 | `10.1093/bib/bbaf424` · PMC12368853              | `[VERIFIED-ABSTRACT]`                                                |
| ZHMolEReP — Ke X et al., _JCIM_ 2026                       | `10.1021/acs.jcim.6c00141`                       | `[VERIFIED-ABSTRACT]`                                                |
| Riedlová K et al., _JCTC_ 2026                             | `10.1021/acs.jctc.6c00427` · PMC13217555         | `[VERIFIED-FULLTEXT]`                                                |
| McCullagh M … Fenton AW, _JBC_ 2024                        | `10.1016/j.jbc.2024.105672` · PMC10897898        | `[VERIFIED-FULLTEXT]`                                                |
| Fenton AW, _TIBS_ 2008                                     | `10.1016/j.tibs.2008.05.009` · PMID 18706817     | `[VERIFIED-ABSTRACT]`; full text `[NOT-RETRIEVABLE]`                 |
| IUPHAR XC — Christopoulos A et al., _Pharmacol Rev_ 2014   | `10.1124/pr.114.008862` · PMC11060431            | `[VERIFIED-ABSTRACT]`; full text `[NOT-RETRIEVABLE]`                 |
| IUPAC medicinal chemistry glossary, 1998                   | `10.1351/pac199870051129`                        | `[VERIFIED-FULLTEXT]` (A–H entries)                                  |
| Lee AL, Sapienza PJ, _Biochemistry_ 2026                   | `10.1021/acs.biochem.5c00782` · PMC13001099      | `[VERIFIED-ABSTRACT]`                                                |
| Sun HM et al., _J Phys Chem B_ 2025                        | `10.1021/acs.jpcb.5c03261` · PMC12400411         | `[VERIFIED-ABSTRACT]`                                                |
| Campitelli P et al., _JMB_ 2025                            | `10.1016/j.jmb.2025.169175`                      | `[VERIFIED-ABSTRACT]`                                                |
| DCI — Kumar A et al., _Bioinformatics_ 2022                | `10.1093/bioinformatics/btac159` · PMC9113273    | `[VERIFIED-ABSTRACT]`                                                |
| D3PM — Peng C et al., _BMC Bioinf_ 2022 `[BORROWED]`       | `10.1186/s12859-022-04595-0` · PMC8845362        | `[VERIFIED-ABSTRACT]`                                                |
