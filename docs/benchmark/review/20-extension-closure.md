# Extension closure — the sixteen unread rows, and every database beyond ASD

**Status: a literature and reachability record. It changes no freeze and admits no arm.**

Two jobs, both attempted on 2026-09-02. **Part 1** tries to close the sixteen rows
[`14-clause-ii-literature-pass.md`](14-clause-ii-literature-pass.md) left UNREAD behind publisher
paywalls. **Part 2** asks whether any resource other than ASD can supply admissible allosteric
apo/holo pairs.

**Read [`09-extension-sweep.md`](09-extension-sweep.md) §4 and
[`14-clause-ii-literature-pass.md`](14-clause-ii-literature-pass.md) §0 first.** This document
does not repeat their measurements. It inherits their bar, their abstract-only rule and their
redaction convention.

**This file names no allosteric-site residue.** Pocket-lining residues are redacted as
`[residue]` and catalytic residues are described by role rather than by number, exactly as
`14-clause-ii-literature-pass.md` does. The tree is protected by `PROTECTED_PATHS` (ADR 0034),
so redaction is defence in depth rather than the guard.

---

## Headline

1. **Four of the sixteen are now closed: one PASS, three FAIL. Twelve remain UNREAD.** The pass
   is `USP7`, decided on the full accepted manuscript of ASD's own curation reference. The three
   fails are `Enpp2`, `Ptgs2` and `birA`, each decided on evidence that a fail may rest on.
2. **The route that worked was not a new library. It was OpenAlex.** Querying every DOI for a
   legally-deposited copy found green or bronze open access for **six** of the sixteen papers
   that `14`'s session recorded as 403. One of those six — `USP7` — was retrievable end to end
   and decided the row. **`14-clause-ii-literature-pass.md` §0.3's list of routes is missing an
   OA-location lookup, and that omission cost it at least one pass.**
3. **A negative finding worth as much as the passes: every one of the sixteen holo entries'
   own primary citation is byte-identical to ASD's curation reference.** Checked in one RCSB
   GraphQL call for all sixteen. The "read the PDB entry's own paper instead" route does not
   exist for this candidate set. It is closed, not untried.
4. **Two rows were decided by chemistry rather than by prose.** `7CR` and `BTX` were resolved
   against `data.rcsb.org` chemical components, and in both cases the formula shows the
   annotated "effector" is not what the row assumes. `Enpp2`'s is an **orthosteric** chemotype;
   `birA`'s is the enzyme's own **reaction intermediate**. Neither needed the paywalled paper.
5. **Part 2 finds exactly one genuinely new resource, and it is paywalled.** **CAPASP**
   (doi:10.1007/s10822-026-00831-4, J. Comput. Aided Mol. Des. 2026) publishes a
   **`CAPASP-Unbound`** subset of _apo-state_ allosteric proteins — the only dataset shape in
   the whole survey that matches what this benchmark needs. Every other resource either
   certifies crypticity rather than allostery, or makes no allostery claim at all.
6. **New admissible arms delivered: zero.** From both parts. The `generalisation` tier stays at
   5 and its minimum attainable one-sided p stays 0.031. §5 does that arithmetic honestly.

---

## 0. Method, and the tooling limit that shapes every number below

### 0.1 What was used

`WebFetch` (fetch a URL, render to markdown, answer a prompt over it), `WebSearch`, and the
`Read` tool against PDFs that `WebFetch` saved to disk. Endpoints exercised:
`api.openalex.org`, `www.ebi.ac.uk/europepmc/webservices/rest`, `eutils.ncbi.nlm.nih.gov`,
`data.rcsb.org/graphql`, `rest.uniprot.org`, `www.ebi.ac.uk/pdbe/graph-api`, plus publisher and
institutional-repository hosts named per row.

### 0.2 Three limits, stated because they bound what "unreachable" means here

**This is the most important section in the document. A reachability claim below is weaker
than the one `database-reachability.json` records, and the difference is the tool.**

1. **No shell, so no raw HTTP status codes.** `09-extension-sweep.md` §1 used `curl` and
   recorded a status and a byte count per probe. `WebFetch` reports a status only when it
   fails. Where a status appears below it is one the tool surfaced verbatim; where it does not,
   the row says "loads" or "unknown" and means exactly that. **Do not merge these rows into
   `database-reachability.json`**, whose rows carry a status, a byte count and a content type.
2. **`WebFetch` upgrades HTTP to HTTPS, so the whole `*.shsmu.edu.cn` estate is unprobeable by
   this agent.** ASD, ASBench, AlloReverse, AlloPharm and AlloScore serve _only_ over plain
   HTTP, because the certificate expired 2025-12-28. My probe of `https://mdl.shsmu.edu.cn/ASD/`
   returned the error **`certificate has expired`** on 2026-09-02, which independently
   corroborates the repository's TLS finding and independently confirms nothing about the plain
   HTTP route. **§1.3 of `09-extension-sweep.md` remains the only verified ASD retrieval
   recipe.**
3. **Publisher and aggregator hosts block this user agent at a high rate.** Wiley, PNAS, JBC,
   MDPI and PMC's article HTML all returned **403** to fetches that a browser would serve. That
   is a property of the client, not of the licence. Six rows below are marked
   `OA-COPY-EXISTS-UNFETCHED` for exactly this reason, and **that verdict is materially
   different from "paywalled"** — those six are one browser session from being closed.

### 0.3 What was NOT done

Unpaywall was **not** queried. Its API requires an email parameter, and the operating rules
forbid sending the user's address to an unrelated service. OpenAlex returns the same
OA-location data with no identifier, and was used instead.

No apo entry was opened, no coordinate was measured, and no clause other than (ii) was
re-measured. Every structural statement below is quoted from a retrieved source or from an RCSB
metadata field.

### 0.4 The bar is unchanged

Clause (ii) as `../primary/README.md` §1 states it, and `14`'s asymmetric rule: **no PASS from
an abstract**; a **FAIL** may rest on an abstract, on a deposited structure title, or on a
chemical-component identity, because a fail cannot inflate the pass list.

---

## 1. Part 1 — per-candidate verdicts

|   # | Target  | Effector | Verdict 2026-09-02                            | Basis                                                                                                                            | Route that decided it                                                                         |
| --: | ------- | -------- | --------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
|   1 | `USP7`  | `8QQ`    | **PASS**                                      | Non-competitive inhibition, Ki 5.5 nM, confirmed three ways; site is an exo-site, not the catalytic triad                        | QUB Research Portal accepted manuscript of doi:10.1038/nchembio.2528, **read in full**        |
|   2 | `Enpp2` | `7CR`    | **FAIL**                                      | `7CR` is the orthosteric PF-8380 chemotype in the lipid-binding pocket, not the allosteric tunnel binder                         | RCSB chemcomp formula + Strathclyde green-OA full text of doi:10.1021/acs.jmedchem.6b01743    |
|   3 | `Ptgs2` | `PLM`    | **FAIL**                                      | The annotated site is the **cyclooxygenase catalytic channel**; in a one-chain node set clause (vii) removes the whole label set | `data.rcsb.org` entry title for `3QH0`                                                        |
|   4 | `birA`  | `BTX`    | **FAIL**                                      | `BTX` is biotinol-5'-AMP, the analogue of BirA's own reaction intermediate, bound at the ligase active site                      | RCSB chemcomp formula + UniProt `P06709` catalytic-activity and function annotation           |
|   5 | `NT5C2` | `ADN`    | **STILL UNREAD** (`OA-COPY-EXISTS-UNFETCHED`) | —                                                                                                                                | JBC hybrid CC-BY PDF exists; **403** to this agent                                            |
|   6 | `gyrB`  | `94H`    | **STILL UNREAD** (`OA-COPY-EXISTS-UNFETCHED`) | —                                                                                                                                | PNAS bronze-OA PDF exists; **403**. Row separately dead on the node set                       |
|   7 | `CTSK`  | `6HM`    | **STILL UNREAD** (`OA-COPY-EXISTS-UNFETCHED`) | —                                                                                                                                | Wiley bronze-OA PDF **403**; open-access substitute (MDPI 2023) **403**                       |
|   8 | `murI`  | `003`    | **STILL UNREAD**                              | —                                                                                                                                | OpenAlex "green" OA is a **false positive** — it resolves to a BindingDB record               |
|   9 | `Pck1`  | `1WD`    | **STILL UNREAD**                              | —                                                                                                                                | Same `10.7270/` OA pattern as `murI`; presumed the same false positive, **not verified**      |
|  10 | `opd`   | `EBP`    | **STILL UNREAD**                              | —                                                                                                                                | OpenAlex `is_oa: false`; Europe PMC substitute search returned no primary paper on this site  |
|  11 | `kmo`   | `7ZR`    | **STILL UNREAD**                              | —                                                                                                                                | OpenAlex `is_oa: false`; the OA KMO structure paper is a **different organism and inhibitor** |
|  12 | `kgd`   | `ACO`    | **STILL UNREAD**                              | —                                                                                                                                | OpenAlex `is_oa: false`; no substitute found                                                  |
|  13 | `AMY2A` | `0XR`    | **STILL UNREAD**                              | —                                                                                                                                | OpenAlex `is_oa: false`; no substitute found                                                  |
|  14 | `pyrH`  | `GTP`    | **STILL UNREAD**                              | —                                                                                                                                | OpenAlex `is_oa: false`; no substitute found                                                  |
|  15 | `pfkA`  | `ADP`    | **STILL UNREAD**                              | —                                                                                                                                | OpenAlex `is_oa: false`. `4PFK` re-confirmed to carry **no citation DOI** in RCSB             |
|  16 | `PYGM`  | `AMP`    | **STILL UNREAD**                              | —                                                                                                                                | OpenAlex `is_oa: false`; no substitute found                                                  |

**Running total across both passes: 14 PASS, 8 FAIL, 12 UNREAD, of 34.**

---

## 2. The four rows that closed

### 2.1 `USP7` — PASS

**Source.** doi:10.1038/nchembio.2528 (Gavory _et al._, _Nat. Chem. Biol._ **14**, 118–125,
2018), peer-reviewed accepted manuscript, 40 pp, deposited in the Queen's University Belfast
Research Portal at `pureadmin.qub.ac.uk/ws/files/138886374/DisCombined.pdf`. Located through
OpenAlex (`oa_status: green`, `license: other-oa`) and read in full on 2026-09-02. This is
**ASD's own curation reference**, not a substitute.

**Deciding sentence, Results, "Determination of a non-competitive mode of inhibition":**

> Lineweaver-Burk analysis revealed that **3** acts as a non-competitive inhibitor. The apparent
> *K*ₘ value for Ub-AMC was calculated as 1.9 μM and the inhibitory constant for **3** derived
> from this analysis (*K*ᵢ = 5.5 nM) was in excellent agreement with the IC₅₀ value obtained
> previously (IC₅₀ = 6.0 nM; Table 1).

**Where the site is, Results, "Co-crystal structure of USP7 bound with an inhibitor":**

> The ligand therefore sits in an exo-site _ca._ 5.5 Å away from the catalytic cysteine
> [residue] (as measured from the carbonyl group) and partially protrudes into the channel
> normally occupied by the C-terminal tail of ubiquitin.

**Independent lines — four.**

| Line | What it is                                                                                                                                                                                                        |
| ---- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1    | Lineweaver-Burk: non-competitive, *K*ᵢ = 5.5 nM against Ub-AMC                                                                                                                                                    |
| 2    | Eadie-Hofstee analysis of the same dataset, "which confirmed the non-competitive mode of inhibition"                                                                                                              |
| 3    | IC₅₀ independent of substrate concentration (average IC₅₀ = 1.0 nM)                                                                                                                                               |
| 4    | Enantiomer discrimination: **3** is "400-fold more active than its enantiomer _ent_-**3** (IC₅₀ = 2.4 μM)", and SPR gives K_d 2.0 nM vs 5.0 μM — the effect tracks a specific binding mode, not a nonspecific one |

**Four caveats, and the first is serious.**

1. **The site is 5.5 Å from the catalytic cysteine and protrudes into the ubiquitin C-terminal
   tail channel.** Clause (vii) removes any label that is itself an active-site residue, and the
   exposure here is high. The repo has a precedent both ways: `hiv_rt` is admitted with a nearest
   label 4.4 Å from the source and clean non-competitive kinetics, while
   `../secondary/README.md` §7.10 records `usp7` **already rejected once** on the argument that
   "GNE-6640 competes with ubiquitin, a natural binding partner. Partner competition is not
   allostery." That rejection was about a **different compound at a different site** (the
   Thumb-Palm cleft), so this pass sits beside it rather than overturning it — but the
   ubiquitin-channel overlap means the same objection is available against this series too.
2. **The crystallised compound is not the compound whose kinetics were measured.** `5N9T` holds
   `8QQ` (C₂₉H₃₁F₃N₆O₃, 568.59, `data.rcsb.org`), which matches compound **4** — the 1.7 Å
   structure, IC₅₀ 22.0 nM. The kinetics are on compound **3**. The paper ties them together
   explicitly: the two co-crystal structures show "a high degree of similarity … The Cα RMSD is
   0.35 Å and the same side chain movements which create the hydrophobic pocket and the same
   pattern of hydrogen bonds are observed in both structures." Compound **4** is itself a
   22 nM inhibitor. This is sufficient but it should be disclosed.
3. **The catalytic triad is disrupted in the complex** ("a disrupted catalytic triad";
   "The catalytic triad is also misaligned"), which is mechanistically consistent with allosteric
   inhibition and is also what a reviewer will ask about when clause (vii) is applied.
4. **A pass on (ii) is not an admission.** Clauses (iii)/(x), (ix) and (iv) are all unmeasured
   for this row, exactly as `14` §5.2 says.

### 2.2 `Enpp2` — FAIL

Decided by ligand identity, then confirmed by the full text (University of Strathclyde green OA
copy of doi:10.1021/acs.jmedchem.6b01743, read in full 2026-09-02).

**The chemistry.** `data.rcsb.org` chemical component `7CR` is
"[3,5-bis(chloranyl)phenyl]methyl 4-[(3R)-3-oxidanyl-3-(2-oxidanylidene-3H-1,3-benzoxazol-6-yl)propyl]piperazine-1-carboxylate",
**C₂₂H₂₃Cl₂N₃O₅, formula weight 480.341**. The paper's allosteric-tunnel steroid hybrids weigh
638–708 (Table 1) and all carry a bile-acid skeleton. `7CR` carries none. It is the
3,5-dichlorobenzyl-piperazine-carbamate/benzoxazolone scaffold of **compound 3**, the alcohol
analogue of **compound 2 = PF-8380**.

**What the paper says that chemotype does, Introduction:**

> …the structure of a compound from the represented by compound **2** (PF-8380), which we had
> determined in complex with ATX, showing the binding of this chemotype in the **orthosteric
> site**.

**Results and Discussion:**

> We determined the crystal structure of **3** bound to ATX … showing that the 3,5-dichlorobenzyl
> moiety of **3** binds in the **lipid binding pocket** …

> The piperazine linker unit, however, adopts a significantly different conformation in **11**
> compared to **3**, projecting towards the tunnel, **instead of the catalytic site** …

The lipid-binding pocket is a substrate subsite — the Introduction defines it as "a relatively
deep hydrophobic pocket which is responsible for binding of the lysophospholipid acyl chain".
And the series' kinetics follow the site:

> As anticipated, **17** was shown to be a **competitive inhibitor** of LPC hydrolysis … with a
> *K*ᵢ of 0.006 μM. This contrasts with the progenitor steroid **1** which is a weak
> non-competitive inhibitor of LPC hydrolysis. Accordingly, **by targeting the hydrophobic
> pocket, we have switched the mechanism of action** in this emerging lead series compared to
> the endogenous modulator **1**.

**Verdict.** Class 2, "right protein, wrong site". The genuinely allosteric ligand in this
system is the bile salt TUDCA bound in the tunnel alone — a different compound in a different
entry. The row annotates the orthosteric one. This is **not** the "competitive kinetics do not
refute allostery" case `../secondary/README.md` §7.10 protects: the objection here is
topographic, and the authors state it themselves.

**One loose end.** `09-extension-sweep.md` §4 records `5M0E` at 1.95 Å; the paper gives
compound **3** at 2.1 Å and compound **17** at 1.95 Å. The ligand formula is the decisive
evidence and it excludes every steroid hybrid, so the verdict stands, but the entry-to-compound
mapping deserves one check by anyone who reverses this call.

### 2.3 `Ptgs2` — FAIL

`14` §2.3 left this UNREAD and §3 item 8 already argued the defect. The deposited title closes
it, and a fail may rest on one:

> **`3QH0`**: "X-ray crystal structure of palmitic acid bound to the **cyclooxygenase channel**
> of cyclooxygenase-2" — `data.rcsb.org/graphql`, retrieved 2026-09-02.

The cyclooxygenase channel **is** the catalytic site. The allostery the paper reports is between
the two monomers of a conformational heterodimer, so it is only visible in a two-chain node set.
ADR 0010 fixes the node set to one protein chain; within that chain the annotated site is the
catalytic site and clause (vii) removes the entire label set. Class 2, "right protein, wrong
site", and simultaneously an argument that the row can never be admissible under ADR 0010.

**The full text remains unavailable and this verdict does not need it.** Europe PMC
`/PMC3099718/fullTextXML` returned **404** and NCBI `efetch db=pmc` returned front matter with
"The publisher of this article does not allow downloading of the full text in XML form", both on
2026-09-02.

### 2.4 `birA` — FAIL

`14` §2.3 stated the conditional: "If that site is the ligase active site, the arm is degenerate
under clause (vii)." The condition is now established, from two sources and no paywall.

**The chemistry.** `data.rcsb.org` chemical component `BTX` is
"((2R,3S,4R,5R)-5-(6-amino-9H-purin-9-yl)-3,4-dihydroxy-tetrahydrofuran-2-yl)methyl
5-((3aS,4S,6aR)-2-oxo-hexahydro-1H-thieno[3,4-d]imidazol-4-yl)pentyl hydrogen phosphate",
**C₂₀H₃₀N₇O₈PS, 559.533** — a biotin moiety joined through a pentyl phosphate to adenosine, i.e.
**biotinol-5'-AMP**, the non-hydrolysable reduced analogue of bio-5'-AMP. `4WF2` is titled
"Structure of E. coli BirA G142A bound to biotinol-5'-AMP".

**The biology.** UniProt `P06709`, fetched 2026-09-02:

- Function: "Acts both as a biotin--[acetyl-CoA-carboxylase] ligase and a biotin-operon
  repressor." BirA "activates biotin to form the BirA-biotinyl-5'-adenylate complex (holoBirA)".
- Catalytic activity, EC 6.3.4.15: "biotin + L-lysyl-[protein] + ATP = N(6)-biotinyl-L-lysyl-[protein]
  - AMP + diphosphate + H(+)".
- Activity regulation: "The switch between the enzymatic activity and the repressor activity is
  regulated by cellular demand for biotin."

bio-5'-AMP is therefore BirA's **own reaction intermediate, synthesised at its own catalytic
site from biotin and ATP**. The allosteric coupling the curation paper reports runs from that
site to **dimerisation** and DNA binding — a real and well-measured effect, and not one from a
topographically distinct effector site to the active site. Same class as `rocF`, where the
"effector" is the substrate.

**Recorded as a judgement call, like `nirK`.** A reviewer who reads clause (ii) as "binding at
site X changes a property measured elsewhere" could pass this row on the −4.0 ± 0.3 kcal/mol
coupling free energy in the abstract. The reason it fails here is clause (ii)'s own
"nonoverlapping, topographically distinct site" and clause (vii)'s consequence: the label set
would be emptied. The evidence is shown so the call can be reversed.

---

## 3. The twelve still unread, and every route tried

### 3.1 Routes run against all sixteen

| Route                                                               | Result                                                                                                                                                                |
| ------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Europe PMC `search?query=DOI:…&resultType=lite`, four batched calls | **14 of 16 are in neither PMC nor Europe PMC.** Only `Ptgs2` (PMC3099718) and `gyrB` (PMC5465892) are deposited                                                       |
| Europe PMC `/PMC*/fullTextXML` for those two                        | **404 for both** — deposited but outside the OA subset                                                                                                                |
| NCBI `efetch db=pmc` for those two                                  | Front matter only; "The publisher of this article does not allow downloading of the full text in XML form"                                                            |
| **`api.openalex.org/works?filter=doi:…`, two batched calls**        | **The new route.** 6 of 16 have a green/bronze/hybrid OA location: `USP7`, `Enpp2`, `CTSK`, `NT5C2`, `gyrB`, plus the two `10.7270/` false positives (`murI`, `Pck1`) |
| **`data.rcsb.org/graphql`, all 16 holo entries in one call**        | **Every entry's own primary citation is identical to ASD's curation reference.** The "read the depositors' paper instead" route does not exist here                   |
| `data.rcsb.org` chemical components for the ambiguous effectors     | Decided `Enpp2` and `birA` outright                                                                                                                                   |
| `rest.uniprot.org` functional annotation                            | Decided `birA`                                                                                                                                                        |
| Europe PMC open-access substitute searches (`opd`, `kmo`, `CTSK`)   | No usable substitute found for any                                                                                                                                    |
| Publisher / repository PDFs (Wiley, PNAS, JBC, MDPI, PMC HTML)      | **403 in every case** to this agent                                                                                                                                   |

### 3.2 The three that are one browser session from closing

Marked `OA-COPY-EXISTS-UNFETCHED`. **These are not paywalled.** A legally-deposited or
publisher-hosted free copy exists at a URL recorded here; only this agent's client was refused.

| Target  | Free copy located by OpenAlex                                                                                                                                   | Outcome         |
| ------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------- |
| `NT5C2` | `oa_status: hybrid`, `license: cc-by`, `http://www.jbc.org/article/S0021925820690883/pdf`                                                                       | **403**         |
| `gyrB`  | `oa_status: bronze`, `https://www.pnas.org/content/pnas/114/22/E4492.full.pdf`                                                                                  | **403**         |
| `CTSK`  | `oa_status: bronze`, `https://febs.onlinelibrary.wiley.com/doi/pdfdirect/10.1002/1873-3468.12495`; substitute doi:10.3390/molecules28104197 (MDPI, open access) | **403** on both |

**This is the single highest-value hour of work left in the extension programme.** Three rows,
three URLs, no subscription required.

### 3.3 A trap in OpenAlex, found the hard way

`murI` and `Pck1` are both reported by OpenAlex as `oa_status: green` with an `oa_url` under the
`10.7270/` prefix and a host labelled "UC San Diego repository". Resolving `murI`'s
(`https://doi.org/10.7270/q2hx1dj3`) returns **302 → `https://www.bindingdb.org/entry/50038411`**
— a **BindingDB affinity record**, not a copy of the Nature paper.

**OpenAlex's `best_oa_location` can point at a data record that merely cites the work.** Anyone
automating this route must resolve the URL and confirm it is a full text. `Pck1`'s
`10.7270/q2m61j1q` shares the prefix and host label and is presumed the same class; that was
**not** verified and is recorded as unknown.

### 3.4 The seven that are genuinely closed

`opd`, `kmo`, `kgd`, `AMY2A`, `pyrH`, `pfkA`, `PYGM` — OpenAlex reports `is_oa: false` and
`best_oa_location: null` for every one. No repository copy, no preprint, no publisher free
access. Substitute searches were run for `opd` (Europe PMC, 79 hits, none a primary paper on
this site) and `kmo` (three _P. fluorescens_ KMO papers, all closed; the one open-access KMO
structure paper, doi:10.1038/nature12039, is a **different organism and a different inhibitor**
and cannot establish this row). These need a library.

Two notes that reduce the value of chasing them:

- **`pfkA` is dead on a second ground, re-confirmed today.** `data.rcsb.org` returns
  `DOI: None` for `4PFK` — the entry's primary citation is the 1981 _Phil. Trans. R. Soc. B_
  **review**, which is not a primary paper and cannot satisfy clause (ii) as written.
- **`gyrB` is dead on the node set.** `5NPK` is titled "1.98A STRUCTURE OF THIOPHENE1 WITH
  S.AUREUS DNA GYRASE AND DNA". ADR 0010 gives the DNA nowhere to go.

---

## 4. Part 2 — every resource that could supply an allosteric apo/holo pair

All probes 2026-09-02, by `WebFetch`. **Read §0.2 before quoting a cell in the "Reachable"
column.** "Loads" means the tool returned rendered content and did not report an error; it is
not an HTTP 200 measurement.

| Resource                                                                | Reachable 2026-09-02                                                                                                                                                                                                | Licence                                                            | What a record certifies                                                                                                                              |                                                                                            New admissible pairs it could supply |
| ----------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------: |
| **ASD v5.1 (2023-09-20)**                                               | HTTPS **`certificate has expired`** (my probe). Plain HTTP unprobeable by this agent; `09-extension-sweep.md` §1.3 verified it with `curl`                                                                          | Research use only, **no redistribution** (verbatim, `download.js`) | the **protein**, not the site; 3102 curated sites mixed with 66,589 machine-predicted                                                                |                                                **0** — already swept exhaustively; 34 leads, 14 clause-(ii)-clean, 0 admissible |
| **ASD apo/holo module (v3.0 claim, 1688 pairs)**                        | Not probed by me (needs plain HTTP). Repo records **404** on the directory                                                                                                                                          | as ASD                                                             | **UNVERIFIED** — the path exists in `localcomponent.js`, the directory does not serve                                                                |                                                                       **unknown**. Still the largest unopened box in the survey |
| **ASBench v1.06 (2014)**                                                | Not probed (same expired certificate)                                                                                                                                                                               | Research use only, **no redistribution**                           | site; selection rules in a paywalled supplement                                                                                                      |                                                                                 **0** — holo-only, cannot support an apo member |
| **AlloBench (2025)**                                                    | Paper **open access**, doi:10.1021/acsomega.5c01263, PMC12059942, ACS Omega, **CC BY**. GitHub raw README loads                                                                                                     | MIT (repo) / CC BY (paper)                                         | 2141 allosteric sites, 2034 structures, **418 unique protein chains**; site per biological assembly                                                  | **0 by construction** — no apo step anywhere in the pipeline, and its inputs are ASD ∪ UniProt ∪ M-CSA ∪ PDB, all already swept |
| **CASBench**                                                            | Browse listing loads: "There are 91 protein(s) in the database."                                                                                                                                                    | none stated                                                        | protein with catalytic **and** allosteric sites annotated; site unioned over every deposited structure; inherits ASD's protein-level bar             |                                                                                              **0** — already swept; no apo step |
| **CAPASP (2026)** — _new to this survey_                                | Abstract retrieved via Europe PMC; **Springer paywall, `isOpenAccess: N`**                                                                                                                                          | unknown                                                            | **`CAPASP-General`** (holo allosteric proteins) and **`CAPASP-Unbound`** (**apo** allosteric proteins)                                               |                                                       **unknown, and the only resource whose shape matches the need.** See §4.1 |
| **AHoJ-DB v2c (2025-04-03, 515,463 entries)**                           | REST API **live**; `?ligands=FBP` returned 43 records                                                                                                                                                               | none stated anywhere                                               | the **pair** (PDB chain, ligand). Records carry `target_apoholo_assignment` and — new to this survey — a field named **`allostery_lig`**             |                                    **unknown.** Its apo call is not clause (iii) — the `1OPL`/`AY7` regression stands. See §4.2 |
| **CryptoBench (OSF)**                                                   | Page returned a shell only; details **not confirmed**                                                                                                                                                               | "Copyright holder – Vit Skrhak (2024)" per the repo survey         | cryptic site at 4.5 Å                                                                                                                                |                                                                                     **0** — cryptic ≠ allosteric (`CONTEXT.md`) |
| **CryptoBank**                                                          | Loads (title only); counts/licence not extractable — **unknown**                                                                                                                                                    | CC BY 4.0 per the repo survey                                      | apo/holo/ligand labelled for **crypticity**                                                                                                          |                                                                                                             **0** — same reason |
| **CryptoSite / PocketMiner**                                            | Not re-probed this session                                                                                                                                                                                          | not stated / not checked                                           | cryptic pocket                                                                                                                                       |                                                                                                             **0** — same reason |
| **PDBbind+**                                                            | Loads (JS shell); version, counts and licence **not extractable — unknown**                                                                                                                                         | restrictive (forced BioLiP to purge 24,809 records, Jan 2025)      | affinity for a protein-ligand complex. No allostery record                                                                                           |                                                                                                                           **0** |
| **BindingDB**                                                           | **Loads.** "3.2M data for 1.4M Compounds and 11.5K Targets", 1.6M curated                                                                                                                                           | not stated on the page                                             | measured affinity. **No record labels a site allosteric; no apo/holo pairs**                                                                         |                                                                                                                           **0** |
| **Binding MOAD**                                                        | **Gone, and now citable.** doi:10.1038/s41598-023-29996-w, _Sci. Rep._ **13**, 3008 (2023), PMC9944886 — the sunset announcement. Server EOL June 2024. Final release 41,409 structures, affinity for 15,223 (37 %) | n/a                                                                | n/a                                                                                                                                                  |                                                                                                   **0**. See §4.3 on the domain |
| **sc-PDB**                                                              | **`connect ECONNREFUSED 130.79.85.37:443`** — the host actively refused the connection                                                                                                                              | unknown                                                            | druggable site. No allostery record                                                                                                                  |                                                                                                                           **0** |
| **Kincore**                                                             | **Loads.** Bulk download available                                                                                                                                                                                  | none stated                                                        | kinase **conformational state** (DFG-in/out, αC, activation loop). "Allosteric" appears only as an inhibitor-type label, not as a site certification |                                           **0** — and `../secondary/README.md` §7.1 says the fix is "to stop proposing kinases" |
| **PDBe-KB graph API**                                                   | **Live.** `uniprot/ligand_sites/P00489` returned ~40 ligand sites                                                                                                                                                   | wwPDB / EMBL-EBI terms                                             | ligand-binding site aggregated across structures. **No allosteric or regulatory field**                                                              |                                                                                                      **0** — recall device only |
| **UniProt REST**                                                        | **Live.** `P06709` returned catalytic activity, activity regulation and binding features                                                                                                                            | CC BY 4.0                                                          | free-text activity-regulation annotation with evidence codes                                                                                         |               **0 new** — already the richest recall route in the 2026-08-24 sweep (431 accessions), and it decided `birA` here |
| **MetalPDB**                                                            | **Loads.** Bulk download (coordination spheres, metal sites, flat XML)                                                                                                                                              | not stated                                                         | metal site geometry from the PDB. **No allostery claim, no apo/holo pairs**                                                                          |                                                                                                                           **0** |
| **GtoPdb v2026.2, LIGYSIS, ProteinLens, PASSer, BioLiP2, PDBj, GPCRdb** | Unchanged from `database-reachability.json`; not re-probed                                                                                                                                                          | as recorded there                                                  | as recorded there                                                                                                                                    |                **0** — and PASSer is a **predictor trained on ASD/ASBench**, so using it as ground truth is circular (ADR 0017) |

### 4.1 CAPASP is the one lead worth acting on

**doi:10.1007/s10822-026-00831-4** — Ai Y, Li H, Huang X, Liu S, "A systematic evaluation of
protein allosteric site prediction tools with independent datasets", _J. Comput. Aided Mol.
Des._, 2026. Abstract retrieved from Europe PMC on 2026-09-02; `isOpenAccess: N`.

From the abstract, verbatim:

> …we created two independent datasets that had not been used in selected computational
> protocols: a CAPASP-General subset comprising holo state allosteric proteins and a
> **CAPASP-Unbound subset comprising apo state allosteric proteins**.

Two reasons this matters more than anything else in the table:

1. **It is the only resource in the whole survey built around an apo state.** ASD, ASBench,
   AlloBench and CASBench are holo-centric; AHoJ-DB, CryptoBench and CryptoBank make an apo call
   but certify crypticity or occupancy rather than allostery. `CAPASP-Unbound` is, by its own
   description, apo allosteric proteins.
2. **It reports the same failure mode this benchmark is built to expose.** "these models
   performed better with the CAPASP-General subset than with the CAPASP-Unbound subset,
   suggesting that the prediction models require further improvement" — an independent
   measurement that apo-state allosteric-site prediction is the hard case, which is exactly
   `CHALLENGE.md`'s premise.

**What is unknown and must not be guessed:** the dataset's size, its per-record evidence bar, its
licence, whether it publishes apo/holo _pairs_ or apo structures alone, whether it overlaps the
27 blocked Pfam families, and whether the data are downloadable at all. **None of that was
established.** The paper is paywalled and the datasets were not located. Treat CAPASP as a lead
with a DOI, not as a supply.

**And the standing warning applies to it in full.** `../secondary/README.md` §3 and ADR 0021
Decision 2: no database certifies allostery per record, per site, per structure, and clause (ii)
is re-established per target from primary literature whatever the frame. CAPASP would be a
**recall device**, like ASD. It would not pay clause (ii) for a single arm.

### 4.2 One correction candidate: AHoJ-DB may carry an allostery field

`database-reachability.json` records AHoJ-DB as certifying "the PAIR (target PDB chain, bound
ligand). **Makes NO allostery claim.**" My probe of `https://apoholo.cz/api/db/search?ligands=FBP`
on 2026-09-02 returned 43 records, and the response carries a field named **`allostery_lig`**
alongside `target_apoholo_assignment`.

**This is flagged, not concluded.** The field name was read out of a summarised API response.
Whether it encodes a curated allostery claim, a pass-through of an ASD annotation, or a
heuristic is **unknown** and was not established. It needs one direct look at the API schema
before `database-reachability.json` is edited. If it is a curated claim, the "makes no allostery
claim" row is wrong; if it is an ASD pass-through, the row is right and AHoJ-DB adds no
independent recall. **Do not edit the freeze record on the strength of this paragraph.**

### 4.3 Binding MOAD: the repository's warning is correct, and now has a DOI

`09-extension-sweep.md` §1.1 warns that `bindingmoad.org` returns 200 for a repurposed
commercial site and that "a 200 on this host must not be read as 'Binding MOAD is back.'"

**I could not reproduce the 200.** `bindingmoad.org` returned **403** to `WebFetch` on
2026-09-02, so the "BioStruct Explorer" content was **not independently confirmed by me**. What
_was_ confirmed is the underlying fact, from the primary source: the sunset was announced in
**doi:10.1038/s41598-023-29996-w** (_Sci. Rep._ **13**, 3008, 2023; PMC9944886; PMID 36810894),
which records the last data update at 41,409 structures with affinity for 15,223 (37 %) and
server end-of-life at June 2024.

**Both probes support the same operational rule and neither supports "Binding MOAD is back."**
The repository's warning stands and should now cite the sunset paper rather than only the
observed HTML.

---

## 5. What the extension buys, in the benchmark's own terms

**Nothing. The honest count of new admissible arms from both parts is zero.**

The arithmetic the task asks for, unchanged:

| `generalisation` tier N | Minimum attainable one-sided p (2⁻ᴺ) | Tolerates one failure at α = 0.05? |
| ----------------------: | -----------------------------------: | ---------------------------------- |
|           **5 — today** |                            **0.031** | No. One failure leaves p = 0.19    |
|                       7 |                               0.0078 | Yes                                |
|                       8 |                               0.0039 | Yes — one failure leaves p = 0.035 |

To move from 5 to 7 the `generalisation` tier needs **two** more admitted arms; at the observed
roughly-even seeded split that means roughly **four** more admitted targets overall. This
document delivers **one new clause-(ii) PASS** and **zero** admitted arms.

**Why one PASS is not one arm.** `USP7` has, today:

- clause (iii)/(x) **unmeasured** — historical kill rate 40 % (`../secondary/README.md` §7.1);
- clause (ix) **not re-measured** on `5N9T`'s biological assembly;
- clause (iv) checked as UniProt identity only, never as sequence identity;
- clause (vii) at **acute** risk — the site is 5.5 Å from the catalytic cysteine and protrudes
  into the ubiquitin C-terminal tail channel;
- a **prior rejection on clause (ii)** recorded in `../secondary/README.md` §7.10 for a
  different compound at a different site, which a reviewer will raise.

And even if it survived all of that, `../secondary/README.md` §7.10 and
`09-extension-sweep.md` §6.9 both hold: **adding one arm re-runs the seeded size-stratified
split and reassigns every existing tier.** That is a re-freeze, not a repair, and one arm does
not buy enough power to justify one.

**The direction of travel across the three sweeps is worth stating plainly.** 2026-08-24: 5
further admissible targets, none added. 2026-09-02 morning: 34 structural survivors, 0
admissible. 2026-09-02 afternoon (`14`): 13 PASS, 5 FAIL, 16 UNREAD, 0 admissible. This
document: 14 PASS, 8 FAIL, 12 UNREAD, **0 admissible**. Every pass has moved the _lead_ count and
none has moved the _arm_ count. **The binding constraint has never been supply of candidates or
reachability of databases. It is that clause (ii) plus clauses (iii), (vii), (ix) and (x)
applied jointly to one structure pair is a very narrow gate**, and no database in §4 pays any
of them.

---

## 6. What this cannot settle

1. **Twelve rows are still undecided, and three of those are decidable today by anyone with a
   browser.** `NT5C2`, `gyrB` and `CTSK` each have a free, legally-hosted copy whose URL is in
   §3.2. Only the client was refused. Quote the Part 1 result as "**14 established, 12 unknown,
   8 refuted**", never as "12 failed".
2. **Every reachability claim in §4 is weaker than the ones in `database-reachability.json`.**
   No shell, no status codes, no byte counts, and the entire `*.shsmu.edu.cn` estate
   unprobeable because `WebFetch` forces HTTPS onto a host whose certificate expired
   2025-12-28. **Do not merge §4 into that JSON.**
3. **The `Enpp2` entry-to-compound mapping has one unresolved discrepancy.** The sweep records
   `5M0E` at 1.95 Å; the paper puts compound **3** at 2.1 Å. The `7CR` formula excludes every
   steroid hybrid, which is why the FAIL stands, but the mapping deserves a check.
4. **`birA` was decided on a definition, not on a measurement** — like `nirK` and `lacS` in `14`
   §5.6. Its coupling free energy is real and well measured. It fails because the effector site
   is the enzyme's own active site. If the repository wants that settled by rule rather than by
   judgement a third time, **it should be written as a clause**: _the effector must not be the
   enzyme's own substrate, product or reaction intermediate_. Three rows now turn on it —
   `rocF`, `NT5C2` and `birA` — and a fourth, `PDC1`, passes only because substrate activation
   at a genuinely separate regulatory site is the mechanism under study.
5. **CAPASP was not obtained.** Its size, licence, evidence bar and availability are all
   **unknown**. §4.1 records a DOI and an abstract, nothing more.
6. **The `allostery_lig` observation is a lead, not a correction.** §4.2 says what would have to
   be checked before `database-reachability.json` moves.
7. **Nothing here re-opens a freeze.** No manifest, no `frozen.json`, no tier assignment, no
   selection ledger is touched. This document supplies evidence for a decision that has not been
   taken, and the recommendation is unchanged: **do not re-freeze the secondary set for this
   submission.**
8. **The quotations are faithful, not certified.** Each was read from a retrieved PDF or API
   response in this session and is given with its section so the check is one lookup. They have
   not been re-rendered and diffed character by character.

---

## Provenance

Every DOI, PMCID, OA status, chemical formula, structure title, UniProt annotation, record count
and quotation came from a live retrieval on **2026-09-02** through `api.openalex.org`,
`www.ebi.ac.uk/europepmc/webservices/rest`, `eutils.ncbi.nlm.nih.gov`,
`data.rcsb.org/graphql`, `rest.uniprot.org`, `www.ebi.ac.uk/pdbe/graph-api`, and the
institutional repositories named per row. The two full texts read end to end were retrieved as
PDFs from `pureadmin.qub.ac.uk` (USP7) and `strathprints.strath.ac.uk` (autotaxin) and read with
the local PDF reader. Nothing is recalled.

The candidate list, its tiers, its accessions and its curation DOIs were read from
[`09-extension-sweep.md`](09-extension-sweep.md) §4 and §4.2 and from
[`14-clause-ii-literature-pass.md`](14-clause-ii-literature-pass.md) §2.3. The clause (ii) text
and its authority were read from [`../primary/README.md`](../primary/README.md) §1; clauses
(ix)–(xii) and the power arithmetic from [`../secondary/README.md`](../secondary/README.md) §4,
§6 and §7. Prior reachability facts attributed to the repository were read from
[`data/database-reachability.json`](data/database-reachability.json), not re-measured, and are
marked as such wherever they appear.
