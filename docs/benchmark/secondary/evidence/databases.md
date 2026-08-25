# Database landscape — what the allostery databases certify

**Status: survey, checked 2026-08-24. Evidence note, not a proposal.**

This note holds the evidence for two statements in
[`../../../adr/0021-secondary-benchmark-is-two-disjoint-sets.md`](../../../adr/0021-secondary-benchmark-is-two-disjoint-sets.md):

- **Fact 1** — no database certifies allostery per record, per site, per structure.
- **Decision 2** — the candidate frame is RCSB and not the Allosteric Database, although
  `CHALLENGE.md` §6 points at ASD.

**The question a reviewer asks first.** "Why not just use ASD, the database the challenge
named?" The short answer is below and the evidence is in §3 and §4. ASD is the only source
in this landscape whose admission rule is functional, and that is why it stays in the
document as a cross-check. It is not the frame, because its evidence bar sits on the
**protein** and not on the site, because three of its five releases publish no inclusion
criteria at all, because its 2023 release mixes curated records with 66,589 machine-predicted
sites, because it states no licence, and because it has no fetch route that a script can
reproduce today.

**Tags.** Claims from the source reviews keep their original confidence.
`[VERIFIED-FULLTEXT]` means the quote came back from the paper full text.
`[VERIFIED-ABSTRACT]` means abstract or indexed record only. `[UNVERIFIED]` means
secondhand. Nothing here is promoted one level up.

---

## 1. What was checked, and how

Every availability fact below comes from a fetch made on **2026-08-24**. Two fetch routes
were in use, and the difference between them is operational, not cosmetic.

| Route            | What it does                                                                    | What it fails on                       |
| ---------------- | --------------------------------------------------------------------------------- | -------------------------------------- |
| **Direct fetch** | The agent fetcher force-upgrades HTTP to HTTPS and sends a bot-like user agent  | a dead certificate, and a bot block    |
| **Proxy fetch**  | A plain-text extraction proxy (`r.jina.ai`) reaches plain HTTP. No bot block hits it | nothing that was tried in this session |

Where the two routes disagree, both results appear. The disagreement is itself a fact about
how reproducible a fetch is.

### Reachable on 2026-08-24

| Source          | URL as checked                                    | Route and result                                                 |
| --------------- | ------------------------------------------------- | ---------------------------------------------------------------- |
| ASD             | `http://mdl.shsmu.edu.cn/ASD/`                    | plain HTTP only. Rendered pages returned                         |
| ASBench         | `http://mdl.shsmu.edu.cn/asbench/`                | plain HTTP only. A registration form blocks the data             |
| CASBench        | `https://biokinet.belozersky.msu.ru/casbench`     | direct. Bulk `tgz` and per-entry `tgz` present                   |
| AlloBench       | `https://github.com/djmaity/allobench`            | direct, and `raw.githubusercontent`                              |
| AHoJ-DB         | `https://apoholo.cz/db`                           | direct. REST API verified with live queries                      |
| CryptoBank      | `https://cryptobankdb.com/` and Zenodo            | direct. Zenodo DOI `10.5281/zenodo.19099155`                     |
| CryptoBench     | `https://osf.io/pz4a9/`                           | direct, through the OSF API                                      |
| PDBbind+        | `https://www.pdbbind-plus.org.cn/`                | direct. Front page only, the data is behind a paywall            |
| BioLiP2         | `https://zhanggroup.org/BioLiP/`                  | **direct fails with 403**, proxy renders it                      |
| RCSB PDB        | `https://data.rcsb.org/rest/v1/core/entry/…`      | direct. JSON returned for `6OIM`                                 |
| PDBe            | `https://www.ebi.ac.uk/pdbe/api/…`                | direct. JSON returned for `6oim`                                 |
| GtoPdb          | `https://www.guidetopharmacology.org/DATA/*.csv`  | direct. CSVs downloaded with no authentication                   |
| GPCRdb          | `https://gpcrdb.org/`                             | direct. REST at `/services/`                                     |
| UniProt         | `https://rest.uniprot.org/uniprotkb/…`            | direct. `P01116` returned `cc_activity_regulation` and PDB xrefs |
| InterPro / Pfam | `https://www.ebi.ac.uk/interpro/api/…`            | direct. Release **InterPro 109.0**                               |

### Not reachable, with the exact failure

| Source                    | URL as checked                                          | Exact failure on 2026-08-24                                                                     |
| ------------------------- | ------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| ASD over HTTPS            | `https://mdl.shsmu.edu.cn/ASD/`                         | `certificate has expired`. The wildcard for `*.shsmu.edu.cn` expired on 2025-12-28               |
| ASD download page, HTTPS  | `https://mdl.shsmu.edu.cn/ASD/module/download/download.jsp` | the same expired certificate                                                                     |
| ASD release archive       | three guessed direct paths                              | **HTTP 404** on all three                                                                        |
| ASD, any bad path         | four distinct paths over plain HTTP                     | genuine **404** with a `JBoss Web/3.0.0-beta-2` server banner                                     |
| ASBench data              | `http://mdl.shsmu.edu.cn/asbench/`                      | registration wall. The formats behind the form were never seen. The survey also records broken TLS |
| ASBench supplement        | OUP supplementary information                           | **paywalled**. The selection rules are not in the retrievable record                             |
| Binding MOAD              | `bindingmoad.org`                                       | **HTTP 403** to direct fetch on both hosts                                                       |
| PDBbind+ data             | `https://www.pdbbind-plus.org.cn/`                      | **paywalled**. The free tier is a "demo user" account, v2020 data, 10 trials                     |
| PDBj                      | `https://pdbj.org/rest/newweb/search/`                  | the probe returned **404**. No endpoint answered. **Not verified**                    |
| PocketMiner               | GitHub `Mickdub/gvp@pocket_pred`                        | **not fetched** this session. Repository licence **not checked**                                 |
| CryptoSite                | Cimermancic 2016 supplement                             | **not fetched** this session                                                                     |

**The ASD server is alive and its TLS is dead.** Plain HTTP serves rendered pages and
genuine 404s. Only the certificate fails. The software age is the durability tell: JBoss Web
3.0.0-beta-2 dates to roughly 2008.

**The download page has no download links, and that is the stronger objection.** Every
`href` on `download.jsp` and on `site.jsp` was enumerated. Each page carries 32 links, all of
them navigation, and none of them a data file. The site builds the file list under the DOWNLOAD tab client-side. The
release filename is known only out of band as `ASD_Release_202306_XF.tar.gz`, named in the
AlloBench README as a manual prerequisite. A script cannot fetch ASD today. A human must
first capture that URL from a rendered page.

---

## 2. The comparison table

Columns: **Unit** is what one record certifies. **Criteria** is whether the source publishes
its inclusion rule. **Curated vs predicted** is whether the source separates hand-curated
records from machine-predicted ones. **Pairs** is apo/holo pair support and the rule behind
it. **Live** is the 2026-08-24 result.

| Database          | Unit certified                                                        | Criteria published                                       | Curated vs predicted separated                                            | Licence and redistribution                                                          | Apo/holo pairs                                                       | Live 2026-08-24                     |
| ----------------- | --------------------------------------------------------------------- | -------------------------------------------------------- | ------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- | --------------------------------------------------------------------- | ----------------------------------- |
| **ASD v1**        | **protein** — "336 **proteins** … verified as **allosteric proteins**" | **Yes** — three cases of experimental evidence           | n/a in v1                                                                 | none stated                                                                         | not in v1                                                            | see ASD row                         |
| **ASD v2.0**      | site geometry only                                                    | **No admission test** — a 6 Å extraction rule only       | n/a in v2.0                                                               | none stated                                                                         | not in v2.0                                                          | see ASD row                         |
| **ASD v3.0**      | protein, inherited                                                    | **No** — "collected using previously described methods"  | n/a in v3.0                                                               | none stated                                                                         | **Yes, claimed** — 1688 paired structures, 308 proteins              | **module not found in 2023 nav**    |
| **ASD 2019**      | protein, inherited                                                    | **No**                                                   | **No** — adds 10,081 AllositePro-**predicted** sites                      | none stated                                                                         | not restated                                                         | see ASD row                         |
| **ASD 2023**      | protein, inherited                                                    | **No**                                                   | **No** — 3102 curated sites beside 66,589 **potential** sites             | **none stated**                                                                     | not exposed as a module                                              | **HTTP yes, HTTPS no** (cert)       |
| **ASBench**       | site — a 235-complex "Core set"                                       | **No** — "a set of rules", detail in a paywalled SI      | unknown, the rules are not retrievable                                    | **"not allowed to distribute the data to a third party"**                           | **No** — holo only                                                   | HTTP yes, behind a registration wall |
| **CASBench**      | protein — the site is a union over every deposited structure          | **Yes** — a four-step ASD-to-CSA synchronisation         | not stated                                                                | **none stated**                                                                     | **No** — apo is derivable from the enumeration, never labelled       | **Yes**                             |
| **AlloBench**     | site, per biological assembly, at 4 Å                                 | **Yes** — the most explicit protocol in the field        | not stated                                                                | **MIT** for the repo, CC BY 4.0 for the paper                                       | **No** — "apo", "holo" and "unbound" do not occur in its methodology | **Yes**                             |
| **Binding MOAD**  | structure — 41,409 at sunset. No allostery record                     | not checked                                              | not checked                                                               | not checked                                                                         | **No**                                                               | **No — 403, sunset 2023, EOL 2024** |
| **PDBbind+**      | entry — 35,924 in v2025. No allostery record                          | not checked                                              | not checked                                                               | **restrictive** — BioLiP purged 24,809 records in Jan 2025 "due to licensing issue" | **No**                                                               | Front page yes, data paywalled      |
| **AHoJ-DB**       | **pair** — `(target PDB chain, bound ligand)`. **No allostery claim** | **Yes** — per-chain occupancy of the superimposed site   | n/a — no prediction                                                       | **none stated anywhere** — site, About page and GitHub all silent                   | **Yes — the record is the pair**. See §4                             | **Yes**, API verified               |
| **CryptoBank**    | apo/holo/ligand combination. Label is crypticity, not allostery       | not checked                                              | n/a                                                                       | **CC BY 4.0**                                                                       | **Yes** — explicit `Structure ID (Holo)` and `Structure ID (Apo)`    | **Yes**, MD5 per file               |
| **CryptoBench**   | cryptic site at 4.5 Å. Not allostery                                  | not checked                                              | n/a                                                                       | **"Copyright holder — Vít Škrhák (2024)"**, that is all rights reserved             | **Yes** — apo/holo splits                                            | **Yes**, OSF API                    |
| **PocketMiner**   | cryptic pocket. Not allostery                                         | not checked                                              | n/a                                                                       | **not checked**                                                                     | **Yes** — 38 apo/holo pairs                                          | **not fetched**                     |
| **CryptoSite**    | cryptic site. Not allostery                                           | not checked                                              | n/a                                                                       | not checked                                                                         | **Yes** — 84 of 93 pairs                                             | **not fetched**                     |
| **BioLiP2**       | ligand-protein interaction. No allostery record                       | not checked                                              | n/a                                                                       | **none stated**                                                                     | **No**                                                               | 403 direct, renders via proxy       |
| **GtoPdb**        | ligand-target interaction with an `Action` column                     | curated, with PubMed references                          | n/a                                                                       | **CC BY-SA 4.0** — share-alike can pass to a derived label file                     | **No** — there is no PDB ID column, the join runs through UniProt    | **Yes**, v2026.2, 2026-06-15        |
| **GPCRdb**        | GPCR structure with `Apo (no ligand)` and PAM/NAM tags               | not checked                                              | n/a                                                                       | **none found**                                                                      | **Partial** — apo is explicit, the pair is not a record              | **Yes**, release 2025-03-20         |
| **RCSB PDB**      | **structure** — the deposition itself. No allostery record            | wwPDB deposition and validation                          | n/a                                                                       | **public domain / CC0**                                                             | **No** — a frame, not a pair set                                     | **Yes**, versioned URLs             |
| **PDBe**          | structure. No allostery record                                        | wwPDB                                                    | n/a                                                                       | EMBL-EBI terms                                                                      | **No**                                                               | **Yes**                             |
| **PDBj**          | structure                                                             | wwPDB                                                    | n/a                                                                       | not checked                                                                         | **No**                                                               | **not verified** — probe 404        |
| **UniProt**       | protein sequence and annotation                                       | UniProt evidence codes                                   | reviewed and unreviewed are separate                                      | **CC BY 4.0**                                                                       | **No**                                                               | **Yes**                             |
| **InterPro/Pfam** | protein family                                                        | InterPro member-database rules                           | n/a                                                                       | **CC0**                                                                             | **No**                                                               | **Yes**, release 109.0              |

---

## 3. Per-database findings

### 3.1 ASD — the Allosteric Database

**The evidence bar sits on the protein, not on the site and not on the modulator.** ASD v1,
doi:10.1093/nar/gkq1022 `[VERIFIED-FULLTEXT]`:

> "With at least three cases of experimental evidence in crystal structure complex or
> biochemistry (inactive mutation of allosteric residue, cooperativity of kinetic effect from
> two ligands and uncompetitive-binding assay with chromatography, etc.), 336 **proteins**
> supporting their functional change elicited by modulator binding at a site that was
> topographically distinct from the orthosteric functional site, were verified as
> **allosteric proteins** for deposition into the ASD"

A protein that enters on three pieces of evidence for site A carries every later structure of
any modulator at any pocket. Our clause (ii) is per-site. ASD's rule is not, so nothing is
inherited.

**v2.0 restates no admission test.** doi:10.1093/nar/gkt1247 `[VERIFIED-FULLTEXT]` gives a
geometric extraction rule only:

> "The residues constituting an allosteric site are automatically extracted from a complex
> structure by 6 Å around allosteric modulator in the site using Pymol and manually inspected"

Additions are "collected using the same methods described in our previous publication". The
6 Å radius is wider than our declared 4.5 Å, so an ASD residue list is not a label set for
this repo without a re-derivation from coordinates.

**v3.0, 2019 and 2023 publish no inclusion criteria at all.** Checked across gkv902, gkz958
and gkad915 `[VERIFIED-FULLTEXT]`. v3.0 says only "collected using previously described
methods".

**The 2023 release mixes curated and machine-predicted records.** The 2019 paper adds
"10081 potential allosteric sites **predicted** … using our AllositePro method". The 2023
paper adds "66,589 **potential** allosteric sites" over 20,386 human proteins, beside 2422
allosteric proteins and 3102 curated allosteric sites (doi:10.1093/nar/gkad915, NAR 2024
52:D376). The R1 audit states the consequence plainly: a set that pulls "allosteric sites"
from ASD2023 without a separation of the curated records will use another model's output as
ground truth, and that "leaves no trace in the files".

**Scope of an effector is wider than a small molecule.** doi:10.1093/nar/gkz958: "The
binding of effectors (e.g. small molecules, ions, and DNA/RNA) to an allosteric site…".

**The apo/holo module is claimed and not found.** ASD v3.0 states 1688 allosteric apo/holo
paired structures over 308 proteins from 107 organisms, downloadable as PyMOL PSE alignments.
This is the only apo/holo pair set in existence that is allosteric by construction. All 32
navigation links on two ASD2023 pages were enumerated on 2026-08-24 and **no apo/holo module
appears in the current site**. Status: **unverified**. A static fetch cannot settle it, and
one manual browser session can.

**Two data defects to price in.** 1620 of 3102 ASD entries have absent allosteric-site
residues in the tab-delimited file, so the XML must be parsed. No 2025 or 2026 release was
found. **No licence is stated.**

### 3.2 ASBench

**The selection rules are not in the retrievable record.** doi:10.1093/bioinformatics/btv169,
`[VERIFIED-ABSTRACT]` plus publisher page:

> "A set of rules was applied to select the qualified allosteric sites and remove site
> redundancy, yielding the 'Core set' composed of 235 representative complexes"

Diversity runs on a PS-score, from a maximum of 0.976 down to 0.491. The paper then says
"Detailed information about the process is provided in the 'Materials and Methods' of
Supplementary Information". That supplement is paywalled. Re-checked in this session: the
OUP body text still gives only "a set of rules". Treat every ASBench-derived pair as if it
carried no criteria.

**A common misattribution.** The 3 Å resolution, no-absent-residues and 30 %-identity triple
that is often attributed to ASBench is in fact **Allosite's**. PASSer2.0 attributes it to
Huang 2013, doi:10.1093/bioinformatics/btt399 `[VERIFIED-FULLTEXT]`. ASBench's 4 Å radius is
known only through Wu 2022's report of ASBench, doi:10.1016/j.patter.2021.100408, and stays
tagged `[UNVERIFIED]`.

**The licence ends the discussion before the rules do.** The site states research use only
and:

> "Users will not be allowed to distribute the data to a third party."

That clause is incompatible with a frozen, reproducible, publishable benchmark. Core set 235
sites, Core-Diversity 147.

### 3.3 CASBench

**It adds no independent allostery test.** CASBench, doi:10.32607/20758251-2019-11-1-74-80
`[VERIFIED-FULLTEXT]`, runs a four-step synchronisation of ASD against the Catalytic Site
Atlas. Ligand selection takes ligands "within 5 Å of any amino acid residue included in the
primary annotation", then "all residues located within 5 Å of the selected ligand". It
inherits ASD's protein-level evidence bar entirely.

**Its site is a union over the whole deposited ensemble.** Residues are merged across all PDB
structures of the protein, so a CASBench residue list is not a label set for one apo/holo
pair. Entries annotate "all sites, as well as associated ligands in all available
crystallographic structures from the PDB". Apo members are derivable from that enumeration.
They are not labelled.

**It publishes a set-level rule and two measurements this repo already uses.** "The CD-HIT
algorithm was then used to cluster proteins at a sequence similarity threshold of 95%"
`[VERIFIED-FULLTEXT]`, and "The quaternary structure of each protein (if any) was restored
according to the corresponding BIOMT records" `[VERIFIED-FULLTEXT]`. The two load-bearing
numbers:

> "In 30% of cases, the catalytic and allosteric sites either overlap or share a common
> border" `[VERIFIED-FULLTEXT]`

> "In 5% of entries, both sites are formed within the intersubunit contact; in 22% of the
> cases, only one site is located between the subunits and 73% of entries correspond to both
> sites being formed within the subunits." `[VERIFIED-FULLTEXT]`

91 entries. No resolution limit, no apo requirement, no ligand-quality rule. No licence is
stated. No update was seen since 2019. Bulk file:
`https://biokinet.belozersky.msu.ru/sites/default/data/casbench.tgz`, 1.9 GB.

### 3.4 AlloBench

**It is the most explicit protocol in the field and it still has no apo step.**
doi:10.1021/acsomega.5c01263, 2025-04-23, `[VERIFIED-FULLTEXT]`. Its published rules:

> "allosteric sites were obtained by locating the residues within 4 Å of the allosteric
> modulator"; "resolution better than 4 Å"; "Only the entries with small-molecule allosteric
> modulators were selected"; "Structures with covalently bound allosteric modulators were
> removed"; "Modeled structures with lDDT < 0.8 were removed"; "The biological assembly
> structures of the target proteins were downloaded from the PDB website"

And the step that closes the door on pairs:

> "Finally, the heteroatoms in the PDB files were removed, and only the protein chains were
> retained"

The words "apo", "holo" and "unbound" do not occur in its methodology. It also inherits ASD's
protein-level evidence bar, and it does not carry the ASD citations forward.

**It measures the effector modality distribution.** "90% of the allosteric sites bind to
small molecule ligands, 8% bind to ions, and only 2% have peptides" `[VERIFIED-FULLTEXT]`.

2141 sites, 2034 structures, 418 unique chains. The repository is **MIT** and holds
`AlloBench.csv`, `ASD_Updated.csv` and `ASD_Enriched.csv`, with 6 commits and no release tag.
It is the one redistributable snapshot of ASD's site annotations in this survey.

### 3.5 Binding MOAD

**Dead.** `bindingmoad.org` returned **HTTP 403** to a direct fetch on both hosts on
2026-08-24. The sunset was announced in 2023 and the server EOL was scheduled for June 2024.
41,409 structures at sunset. It carries no allostery record and no apo/holo pairs. Its
inclusion criteria and licence terms were **not checked**, because the site did not answer.

### 3.6 PDBbind+

**Licence-hostile, and the current data is paywalled.** `https://www.pdbbind-plus.org.cn/`
answered on 2026-08-24, and the free tier is a "demo user" account with v2020 data and 10
trials. v2025 holds 35,924 entries and was released in 2026-02. The legacy free site is
frozen at v2020. Its licence terms already forced BioLiP to purge 24,809 PDBbind-CN records in
January 2025 "due to licensing issue". It carries no allostery record and no apo/holo pairs.

### 3.7 AHoJ and AHoJ-DB

**Its record is the pair, and it makes no allostery claim.** `https://apoholo.cz/db` answered
live queries on 2026-08-24. The unit of record is `(target PDB chain, bound ligand)`, for
example `5mo4-A-AY7-602`. A record carries `target_pdb_id`, `target_chains`,
`target_ligand`, `target_ligand_group`, `query_ligs`, `nonquery_ligs`, `allostery_lig`,
`target_apoholo_assignment` (`H` or `A`), `target_experimental_method`, `target_resolution`,
`target_uniprot_ids`, residue counts, SASA, pocket volume, and the payload:
**`found_apo_pdbids` and `found_holo_pdbids`**.

**Its published rule is per-chain occupancy of the superimposed site.** Its radius is 4.5 Å
(doi:10.1093/bioinformatics/btac701), which matches ours. It reports binding sites at an
interface of two or more chains at about **24 %** (doi:10.1016/j.jmb.2024.168545)
`[VERIFIED-ABSTRACT]`.

515,463 entries in v2c, dated 2025-04-03. v2b is 2024-09-15 and v1 is 2023-07-22. The paper
reports 522,153 interactions across the PDB. A 38 GB bulk archive exists at
`https://apoholo.cz/api/db/archive/download/ahojdb_v2c.tar.gz`. **AHoJ publishes no
checksums.**

**No licence is stated anywhere** — not on the site, not on the About page, not in the GitHub
repository. The contact recorded in the survey is `christos.feidakis@natur.cuni.cz`.

---

## 4. The AHoJ-DB check on `AY7`

**This is the single item that decides Decision 2, so it stands alone.**

The query was run live on 2026-08-24:

```bash
curl -sSf 'https://apoholo.cz/api/db/search?ligands=AY7'
```

`AY7` is asciminib, the BCR-ABL1 allosteric effector. The query returns 3 entries: `5mo4 A
AY7 602`, `8ssn A AY7 601` and `8ssn B AY7 601`. Each lists **66 candidate apo structures,
34 of them unique** — the list repeats entries and carries no per-chain resolution. Among
them are `2g2f`, `2g2h` and `2g1t`, siblings of this repo's chosen `2G2H`. Among them is
also **`1opl`**, in all three entries. Re-checked independently on 2026-08-24 with the same
command.

**`1OPL` is the pair this repo's own audit rejected.** `docs/benchmark/primary/README.md` §2 records
the measurement: `1OPL` chain A holds `MYR` in the myristoyl pocket, `MYR` contacts **16 of
the 20** asciminib label residues, the nearest approach is **3.29 Å**, and those 16 are a
strict subset of asciminib's 20 at Jaccard 0.80. The mandated apo already is holo at the site
to be predicted. `1OPL` fails clause (iii).

**Why AHoJ still calls it apo.** AHoJ's published rule is per-chain occupancy of the
superimposed site. The likely explanation is that `1OPL` chain B is site-free while chain A is
not. That explanation is **unverified**, because `found_apo_pdbids` is a flat PDB-ID list. It
carries no per-apo metadata, no chain resolution, and no field that records what else sits in
the candidate's pocket.

**The plain statement.** AHoJ-DB's apo call is not our clause (iii). A recipe that takes that
call at face value gets the pair our own audit rejected. Any recipe that consumes AHoJ must
re-derive site occupancy from the coordinates, per chain. The `1OPL`/`AY7` case is
the regression test for that step.

---

## 5. What this means for us

**Conclusion 1 — the frame is RCSB, and the databases are cross-checks.** ADR 0021 Decision 2
records this. The evidence is §1 and §2: ASD needs a manual browser step before any fetch,
states no licence and serves over plain HTTP only. ASBench forbids redistribution. Binding
MOAD is dead. PDBbind+ is paywalled. AHoJ-DB states no licence and its apo call is not ours.
CASBench and AlloBench are reachable, redistributable and useful, and neither one certifies
allostery independently of ASD.

**Conclusion 2 — clause (ii) must be re-established from primary literature under any frame.**
This is not a cost of the RCSB frame. It is a cost of the field. None of the four allostery
databases certifies, per record, that _this modulator_ at _this site_ in _this structure_ has
functional evidence of allostery. ASD certifies proteins. ASBench's rules are unpublished.
CASBench inherits ASD. AlloBench inherits ASD. The functional-evidence DOI comes from the
primary literature per target, exactly as the three primary arms already do through
`allosteric_evidence`. That is the expensive part of a secondary set, and the fetch is not.

**Conclusion 3 — the databases keep a real role, and it is corroboration.** ASD holds the
only functional admission rule in the landscape, so an ASD record beside a target corroborates
an allostery claim. CASBench's 91 curated enzymes are a scriptable
check on any distance assumption, and its 30 % overlap figure is already load-bearing in
`docs/benchmark/primary/README.md`. AlloBench's MIT-licensed CSVs are a pinnable snapshot of ASD's
site annotations. AHoJ-DB is a candidate generator for apo partners, after a per-chain
re-filter. GtoPdb curates `Action = "Allosteric modulator"` independently of ASD, so agreement
there is real corroboration. None of them is the claim itself.

---

## 6. Limitations

**What was not checked, and stays not checked.**

- **PocketMiner** was not fetched this session. Its repository licence was **not checked**.
- **CryptoSite** was not fetched this session.
- **PDBj**: the probe returned 404 and no endpoint answered. Marked **not verified**, not
  "down".
- **Binding MOAD**: inclusion criteria and licence terms are unknown, because the host
  returned 403.
- **PDBbind+**: inclusion criteria are unknown. Only the front page was reached.
- **ASBench**: the formats behind the registration form were never seen. The selection rules
  are paywalled and remain unauditable.
- **CASBench and AlloBench**: whether either separates ASD's curated records from ASD's
  machine-predicted records is **not stated** in the source reviews.

**What is unverified and stays unverified.**

- **The ASD apo/holo module.** v3.0 claims 1688 allosteric apo/holo paired structures. A
  static fetch of 32 navigation links on two ASD2023 pages found no such module. Presence in
  the 2023 release is **unverified**. Only a manual browser session can settle it.
- **The `1OPL` chain explanation.** The per-chain account of AHoJ's apo call for `1opl` is
  likely and not verified. AHoJ exposes no per-apo chain metadata.
- **ASBench's 4 Å radius** rests on Wu 2022's report of ASBench,
  doi:10.1016/j.patter.2021.100408, and stays `[UNVERIFIED]`.
- **AHoJ-DB's interface fraction** of about 24 % is `[VERIFIED-ABSTRACT]` only
  (doi:10.1016/j.jmb.2024.168545).

**One licence question stays open.** AHoJ-DB states no terms anywhere. Do not redistribute
any file derived from it until an answer arrives.

**Source reviews.** This note condenses two session reports from 2026-08-24: an audit of the
normative apo/holo pair definition, and a survey of the database landscape. Where one of them
disagrees with the freeze, the freeze wins.
