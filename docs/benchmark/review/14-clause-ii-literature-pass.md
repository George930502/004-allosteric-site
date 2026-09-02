# Clause (ii) literature pass on the 34 extension survivors

> **CONTINUED, NOT REPLACED — 2026-09-02.** [`20-extension-closure.md`](20-extension-closure.md) is the second pass at the sixteen rows this pass left UNREAD. It closed four and left twelve, and it does not repeat the measurements here.

**Status: a literature record. It changes no freeze and admits no arm.** The candidates are the
34 survivors of [`09-extension-sweep.md`](09-extension-sweep.md) §4. That sweep measured every
structural clause it could and left clause (ii) — the load-bearing one — unpaid. This document
pays it, target by target, against papers that were retrieved rather than recalled.

**Read `09-extension-sweep.md` §4, §4.2 and §6 first.** This document does not repeat the
structural measurements; it only decides whether _functional_ evidence establishes that the
annotated modulator at the annotated site acts allosterically.

**This file names no allosteric-site residue.** Residue identities are redacted from
quotations as `[residue]`, and catalytic residues are described by role rather than by number.

**Updated 2026-09-02: the reason has changed and the practice has not.** When this file was
written, `docs/benchmark/review/` was **not** in `tests/test_no_leakage.py`'s
`PROTECTED_PATHS`, so keeping label residues out of the directory was the cheap alternative to
adding a guarded route. The route was added the same day (ADR 0034): the whole tree is now
protected, and its own tools are exempt by a rule rather than by a name list — a file is a
review tool when it is tracked inside the tree **and** imports nothing from `allo`. Redaction
is therefore no longer load-bearing. It is kept anyway, because defence in depth costs nothing
here and a protected path is one edit away from being unprotected.

---

## Headline

1. **13 of 34 pass clause (ii). 5 fail. 16 are UNREAD.** Every pass rests on a full text that
   was retrieved in this session and quoted. Every fail rests on a sentence from a retrieved
   source that contradicts the annotation. Every UNREAD names the reason.
2. **Among the 21 rows that could be decided, the kill rate is 24 % (5 of 21)** — close to the
   29 % the 2026-08-24 sweep measured and `09-extension-sweep.md` §6.1 predicted. The rate is
   not the interesting number, though: **the sixteen UNREAD rows are undecided, not passing**,
   and the honest count of clause-(ii)-clean leads is 13, not 34.
3. **A pass on clause (ii) is not an admission.** Seven of the thirteen passes carry a separate
   structural problem that the sweep's UniProt-level screening could not see — `AMD1`, `FDPS`,
   `LDHA`, `FBP1`, `PARP14`, `GAA` and `lacS`. §3 lists them. **Six passes carry no known
   structural blocker: `hisG`, `UBE2I`, `PDC1`, `LGMN`, `proRS`, `fbpC`** — and every one of
   those six still has unmeasured clauses, listed in §4.
4. **No curation DOI pointed at the wrong protein.** All twenty PubMed-resolvable references in
   §4.2 resolve to a title and journal that match their row. The defects found are of four other
   kinds — right protein but wrong question, right protein but wrong site, a deposited entry that
   cannot support the pair, and no journal citation at all. §3 lists thirteen, plus one
   correction to §4.2 itself.
5. **The best single new arm is `hisG`**, _M. tuberculosis_ ATP phosphoribosyltransferase under
   L-histidine feedback. It fills gap (a) with a metabolite, adds an organism, sits at 284
   residues, and its inhibition kinetics were measured three ways in an open-access primary
   paper. It is not the paper ASD cites.

---

## 0. How a verdict was reached

### 0.1 The bar

Clause (ii), from `../primary/README.md` §1:

> **(ii) Provenance of label.** The site is allosteric because _functional_ evidence says so.
> Distance from the active site is neither necessary nor sufficient. ASD v1 sets the evidence
> bar at "at least three cases of experimental evidence". A crystal structure alone is on
> nobody's list.

Operationally, a **PASS** required at least one retrieved primary paper reporting an experiment
in which binding at the annotated site changes a property measured elsewhere: enzyme kinetics
with a stated inhibition or activation type, mutagenesis at the site altering catalysis,
thermodynamic linkage, NMR or HDX coupling, or a cellular assay. A ligand seen in a crystal at
a distinct site was never sufficient on its own.

### 0.2 The abstract-only rule, stated because it decides sixteen rows

**No PASS was issued from an abstract.** Where the only retrievable text was an abstract, the
verdict is **UNREAD**, and what the abstract says is recorded so that a later reader knows
whether the row is worth a library visit. The rule is deliberately asymmetric: a **FAIL** may
rest on an abstract or on a deposited structure title, because a fail cannot inflate the pass
list. Two rows (`SIRT3`, `rocF`) fail on that basis and say so.

This asymmetry is the single largest driver of the UNREAD count. Eleven of the sixteen UNREAD
rows have an abstract that reads favourably. None of them is counted as a pass.

### 0.3 Retrieval routes, and which ones worked

| Route                                                                                 | Result                                                                  |
| ------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| `pmc.ncbi.nlm.nih.gov/tools/idconv` DOI → PMCID                                       | worked for all 34 DOIs; 14 of 34 curation references are in PMC         |
| `ebi.ac.uk/europepmc/…/PMC*/fullTextXML`                                              | full text for 8 of the 14                                               |
| `eutils…efetch.fcgi?db=pmc&id=<numeric>&retmode=xml`                                  | full text for 4 more, including three where Europe PMC returned 404     |
| `eutils…efetch/esearch/esummary` against PubMed                                       | abstracts and DOI↔PMID mapping for all 34                               |
| `data.rcsb.org/rest/v1/core/entry` and `…/chemcomp`                                   | entry titles, citations and effector chemical identities                |
| `pmc.ncbi.nlm.nih.gov/articles/PMC*/`                                                 | worked three times, then served a reCAPTCHA for the rest of the session |
| `jbc.org`, `pnas.org`, Wiley, Royal Society, ScienceDirect, `linkinghub.elsevier.com` | **403 Forbidden in every case**                                         |

The 403 wall is what produces the UNREAD count. It is not selective: JBC, PNAS, Nature, Nature
Chemical Biology, _Biochemistry_, _J. Med. Chem._, _Chemistry & Biology_, _Structure_, _JMB_,
_Arch. Biochem. Biophys._, _FEBS Letters_, _FASEB J._, _Acta Cryst. D_ and _Phil. Trans. R. Soc.
B_ were all unreachable. Two of those walls were got round by finding a **different**,
open-access primary paper on the same protein and the same site (`hisG`, `AMD1`), and one by
finding the functional companion of a structural paper (`GAA`).

### 0.4 A caveat on the quotations

Every quotation below was returned by a retrieval pass over the source document. They are
reproduced as returned. They have **not** been re-rendered a second time and diffed
character-by-character, so treat them as faithful rather than as certified verbatim. Where a
verdict turns on one sentence, that sentence is given in full and its section is named, so the
check is cheap for anyone with access.

---

## 1. Verdict summary

| Verdict    |      N | Targets                                                                                                                         |
| ---------- | -----: | ------------------------------------------------------------------------------------------------------------------------------- |
| **PASS**   | **13** | `hisG`, `UBE2I`, `AMD1`, `PDC1`, `FDPS`, `LDHA`, `FBP1`, `LGMN`, `proRS`, `fbpC`, `PARP14`, `GAA`, `lacS`                       |
| **FAIL**   |  **5** | `LTA4H`, `PDE10A`, `SIRT3`, `rocF`, `nirK`                                                                                      |
| **UNREAD** | **16** | `NT5C2`, `birA`, `USP7`, `pyrH`, `kgd`, `murI`, `CTSK`, `opd`, `kmo`, `AMY2A`, `Ptgs2`, `Pck1`, `gyrB`, `Enpp2`, `pfkA`, `PYGM` |

Eight of the thirteen physiological-effector rows are decided: **six pass** (`hisG`, `LDHA`,
`AMD1`, `FBP1`, `FDPS`, `PDC1`), **two fail** (`PDE10A`, `rocF`), and **five remain UNREAD**
(`NT5C2`, `pyrH`, `kgd`, `pfkA`, `PYGM`). Two of the three sub-272-residue rows are undecided
(`pyrH` at 240, `murI` at 255); the one that is decided, `UBE2I` at 158, passes.

---

## 2. The full per-candidate record

### 2.1 PASS — 13

| Target   | Effector | Evidence type                                                                                                   | Source retrieved                                                                                                      | Deciding sentence                                                                                                                                                                                               |
| -------- | -------- | --------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `hisG`   | `HIS`    | steady-state kinetics ×2 inhibition types, IC50 with cooperativity, structural distance                         | **doi:10.1021/bi300808b** (PMC3466779), full text. **Not ASD's reference**                                            | Results—Steady-State Kinetics: "Inhibition of l-histidine versus PRPP was linear and noncompetitive…with a Kii value of 23.5 ± 6.5 μM and a Kis value of 25.7 ± 12.8 μM."                                       |
| `UBE2I`  | `5VM`    | conjugation-assay IC50, site mutagenesis, NMR chemical-shift perturbation                                       | doi:10.1002/anie.201511351 (PMC4973392), full text                                                                    | Results: "Neither mutant was inhibited by **1** at any concentration. Thus, mutation of the binding site residues abolishes inhibitory activity"                                                                |
| `AMD1`   | `PUT`    | activation assays (two activities), site mutagenesis, structural distance                                       | **doi:10.1021/bi801732m** (PMC2646671), full text. **Not ASD's reference**                                            | Discussion 4.1: "Mutation of [residue] totally abolished binding, while mutations of [two residues] greatly reduced the affinity for putrescine"                                                                |
| `PDC1`   | `PYR`    | sigmoid steady-state kinetics and lag phases, slow isomerisation, site mutagenesis                              | doi:10.1074/jbc.M806228200 (PMC2673282), full text                                                                    | Results and Discussion: "Kinetic studies reveal a slow isomerization as triggered by substrate binding to a separate regulatory site."                                                                          |
| `FDPS`   | `FPP`    | ITC at a single site, product-inhibition kinetics, mechanism                                                    | doi:10.1038/ncomms14132 (PMC5253651), full text                                                                       | Results: "An additional reaction with an initial amount of FPP produced a depressed rate curve as well (black, Fig. 4a), thus establishing that the reduced catalytic efficiency is due to product inhibition." |
| `LDHA`   | `OAA`    | non-competitive inhibition kinetics with Ki                                                                     | doi:10.1038/ncomms16018 (PMC5508129), full text                                                                       | Results: "Moreover, we find that, similar to malonate, oxaloacetate is a non-competitive inhibitor of L-LDH with respect to pyruvate with moderate in vitro inhibition too (Ki=2.30±0.22 mM)"                   |
| `FBP1`   | `AMP`    | non-competitive inhibition kinetics, R→T quaternary transition                                                  | **doi:10.1021/bi400532n** (PMC4869526), full text. §4.2 records this reference as having no DOI; it has one           | Introduction: "AMP binds 28 Å away from the nearest active site, inhibiting catalysis noncompetitively with respect to Fru-1,6-P2."                                                                             |
| `LGMN`   | `5KN`    | binding to active-site-blocked enzyme, biphasic inhibition kinetics, conformational cross-talk                  | doi:10.1038/ncomms14740 (PMC5378956), full text                                                                       | Results: "all active site blocked δ-secretase forms exhibited significant binding, demonstrating that compound 11 does not only bind to δ-secretase's active site but rather targets a regulatory exosite."     |
| `proRS`  | `3O6`    | site is not the active site; IC50 varies with substrate concentration                                           | doi:10.1021/acsinfecdis.6b00078 (PMC5241706), full text                                                               | Summary of Findings: "For TCMDC-124506 an increase in IC₅₀ for *Pf*ProRS inhibition was observed as the ATP or proline concentration was increased"                                                             |
| `fbpC`   | `6Y1`    | inactivation kinetics (kinact/KI), covalent labelling of a non-catalytic residue 14 Å away                      | doi:10.1021/acsinfecdis.7b00003 (PMC6126352), full text                                                               | Introduction: "Ebselen was shown to covalently modify the only cysteine, [residue], in Ag85C, which is conserved, noncatalytic, and solvent-accessible"                                                         |
| `PARP14` | `9HH`    | ITC competition (linkage), BLI and ITC KD, crystallography                                                      | doi:10.1021/acschembio.7b00445 (PMC6089342), full text                                                                | Results: "In the presence of 80 µM GeA-69, binding of ADPR to the macrodomain was not detected while in absence of the inhibitor recognition of the ADPR with a KD of 7.8 µM was measured"                      |
| `GAA`    | `SC2`    | site 30 Å from the active site; stabilisation without catalytic disruption; cellular and animal activity rescue | doi:10.1038/s41467-017-01263-3 (PMC5653652) full text **plus** doi:10.1038/mt.2012.152 (PMC3519985) **abstract only** | Nat Commun, Introduction: "a NAC molecule, designated as NAC1, is located about 30 Å away from the active site, at the interface between the (β/α)₈ barrel and the distal β-sheet domain"                       |
| `lacS`   | `14O`    | 730-fold kcat/Km restoration, dose–response, partial agonism                                                    | doi:10.1021/acssynbio.6b00097 (PMC5161622), full text                                                                 | Introduction: "we found that introduction of the [residue]→Gly mutation led to a 730-fold decrease in kcat/Km relative to wild type; this was completely restored upon addition of 10 mM indole."               |

**Supporting lines, per pass.** The count below is of _independent_ experimental lines found in
the retrieved text, not of sentences.

| Target   |                         Lines | What they are                                                                                                                                                                                                                                                                                                                                                                                                         |
| -------- | ----------------------------: | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `hisG`   |                         **3** | noncompetitive inhibition versus PRPP (Kii 23.5 μM); uncompetitive versus ATP (Kii 27.9 μM); IC50 33.3 ± 3.5 μM with Hill number 1.5. The site is located "∼30 Å from the active site"                                                                                                                                                                                                                                |
| `UBE2I`  |                         **3** | sumoylation IC50 5.8 ± 0.1 mM; binding-site mutants not inhibited at any concentration; NMR chemical-shift perturbation. Also E2–SUMO thioester formation inhibited at concentrations tracking the IC50                                                                                                                                                                                                               |
| `AMD1`   |                         **3** | decarboxylase activation ~4-fold and proenzyme-processing activation 5–8-fold by putrescine; three site mutations that abolish or greatly reduce putrescine affinity; site "at a distance of 15 to 20 Å from the active site"                                                                                                                                                                                         |
| `PDC1`   |                         **3** | sigmoid steady-state kinetics and lag phases; time-dependent activation by substrate and by the analogue MAP; mutagenesis of the regulatory cysteine to Ala or Ser                                                                                                                                                                                                                                                    |
| `FDPS`   |                         **3** | ITC showing one FPP per monomer at a single site, Kd 5.3 μM; product-inhibition rate curves; the stated mechanism — "FPP binding at the new druggable site, purely by altering the enzyme's conformational ensemble, interferes with DMAPP binding at the distantly located allylic substrate site"                                                                                                                   |
| `LDHA`   |                         **2** | non-competitive inhibition versus pyruvate with Ki 2.30 ± 0.22 mM; crystallographic placement "adjacent to, but not within, the active site"                                                                                                                                                                                                                                                                          |
| `FBP1`   |                         **2** | noncompetitive inhibition versus Fru-1,6-P2 from 28 Å, and competitive versus divalent cations; the AMP-triggered 15° subunit-pair rotation from R to T. **Both deciding sentences are Introduction statements of established kinetics, not new measurements in this paper**                                                                                                                                          |
| `LGMN`   |                         **3** | surface-acoustic-wave binding to active-site-blocked enzyme; curvilinear, time- and concentration-dependent inhibition consistent with a two-step mechanism; retardation of association and dissociation by an active-site substrate analogue, described as "a conformational cross talk between inhibitor binding to the regulatory exosite and the active site"                                                     |
| `proRS`  |                         **2** | "Surprisingly, these compounds did not bind in the known active site, neither where the nucleotide nor where halofuginone binds"; IC50 rising with ATP or proline concentration                                                                                                                                                                                                                                       |
| `fbpC`   |                         **2** | kinact/KI for three ebselen derivatives (0.0065–0.3057 μM⁻¹ min⁻¹); covalent modification of the single conserved non-catalytic cysteine "approximately 14 Å from the [catalytic] nucleophile", relaxing a helix and displacing the catalytically relevant glutamate                                                                                                                                                  |
| `PARP14` |                         **2** | BLI and ITC KD of 1.4 μM and 860 nM; ITC competition abolishing ADPR binding, ADPR alone binding at KD 7.8 μM. The inhibitor "did not occupy the ADPR binding site but was deeply buried within the macrodomain"                                                                                                                                                                                                      |
| `GAA`    | **2** (one at abstract level) | thermal-stability scans and the statement "NAC is indeed an allosteric chaperone, as anticipated by functional studies", both from the retrieved full text; and, **at abstract level only**, "NAC improved the stability of rhGAA as a function of pH and temperature without disrupting its catalytic activity" with "GAA activities were 3.7–8.7-fold higher than those obtained in cells treated with rhGAA alone" |
| `lacS`   |                         **2** | 730-fold kcat/Km loss on mutation, fully restored by 10 mM indole; dose-dependent initial-velocity increases for three effectors with fitted KD and extent                                                                                                                                                                                                                                                            |

### 2.2 FAIL — 5

| Target   | Effector | Why                                                                                                                                                                           | Source retrieved                                                                                                                      | Deciding sentence                                                                                                                                                                                                                                                                                                                                                 |
| -------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `LTA4H`  | `692`    | The site is the substrate cleft. The paper's own crystallographic screen found exactly one fragment outside that cleft, and it was inactive                                   | doi:10.1021/jm900259h (PMC2722745), full text; ligand identity from `data.rcsb.org`                                                   | Results: "Of all the fragments identified by crystallographic screening, only compound 10 (FOL-Biaryl) did not bind in the substrate binding cavity." — and of that one compound: "Molecule 10 was not competitive with bestatin (1) an LTA4H competitive inhibitor (data not shown) and displayed little or no inhibitory activity against LTA4H (IC50 > 1 mM)." |
| `PDE10A` | `CMP`    | Structure only. The curation reference reports a cAMP-bound GAF-B domain and no functional measurement. Separately, the proposed apo and holo are **non-overlapping domains** | PubMed abstract (JBC full text 403); `data.rcsb.org` entries `2ZMF` and `2OUS`                                                        | Abstract: "In the PDE10A GAF-B domain, cAMP tightly binds to a cNMP-binding pocket." No sentence in the abstract reports an effect of that binding on catalysis                                                                                                                                                                                                   |
| `SIRT3`  | `BVB`    | The mechanism the authors establish biochemically is substrate competition at the internal site; the second site's role is offered as a possibility, not a result             | PubMed abstract (Chem Biol full text 403); `data.rcsb.org` entry `4C7B`                                                               | Abstract: "Crystal structures of Sirt3…reveal two compound binding sites. Biochemical studies identify the internal site and substrate competition as the mechanism for inhibition." and, of the other site, "the second, allosteric site might indicate the site for Sirt1 activation."                                                                          |
| `rocF`   | `ARG`    | Structure only, and the "effector" is the substrate. `3CEV` is "ARGINASE FROM BACILLUS CALDEVELOX, COMPLEXED WITH L-ARGININE" and holds six L-arginine copies                 | PubMed abstract (Structure full text 403); `data.rcsb.org` entry `3CEV`                                                               | Abstract: "a second arginine-binding site, remote from the active site". The abstract reports **no** kinetic or mutational measurement attributable to that site                                                                                                                                                                                                  |
| `nirK`   | `ACM`    | The pocket exists only in an engineered point mutant, and it is the position a copper ligand occupies in the wild type. That is not a topographically distinct site           | PubMed abstract (JMB full text 403); `data.rcsb.org` entry `1ZDS`, titled "Crystal Structure of Met150Gly AfNiR with Acetamide Bound" | Abstract: "ligands act as allosteric effectors by displacing [residue], which moves to bind to the Cu in the position emptied by the [engineered] mutation."                                                                                                                                                                                                      |

`nirK`'s fail is the one judgement call in this group and is flagged as such. The functional
evidence is real — the mutant's kcat falls from 416 ± 10 s⁻¹ to 133 ± 6 s⁻¹ and external ligand
binding restores it to 374 ± 28 s⁻¹ — but the ligand occupies a cavity created by removing a
copper ligand, and the effect is transmitted by pushing a second residue onto the catalytic
copper. Recorded as a fail on "topographically distinct", with the evidence shown so the call
can be reversed by someone who reads it differently.

### 2.3 UNREAD — 16

Every row here has a stated reason. "Abstract only" means the abstract was retrieved from
PubMed and the full text refused.

| Target  | Effector | Why UNREAD                                                                                                                                                       | What the retrieved text does say                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| ------- | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `NT5C2` | `ADN`    | JBC full text 403; abstract only (doi:10.1074/jbc.M700917200)                                                                                                    | "At effector site 1 located near a subunit interface we modeled diadenosine tetraphosphate with one adenosine moiety in each subunit." **No sentence places adenosine at an effector site**, and `2JC9` is titled "in complex with adenosine" — adenosine is this enzyme's reaction product. The row's annotation is unverified and the effector site the paper describes is an interface site                                                                                                                                                                                                                                                                                                                                                     |
| `birA`  | `BTX`    | JMB full text 403; abstract only (doi:10.1016/j.jmb.2015.02.021)                                                                                                 | "Small ligand, bio-5'-AMP, binding and dimerization of the Escherichia coli biotin repressor are allosterically coupled", with "the full coupling free energy of -4.0 ± 0.3 kcal/mol observed in the wild-type protein". The coupling is to dimerisation, and the effector is an analogue of the ligase reaction intermediate. If that site is the ligase active site, the arm is degenerate under clause (vii)                                                                                                                                                                                                                                                                                                                                    |
| `USP7`  | `8QQ`    | Nature Chemical Biology full text 403; abstract only (doi:10.1038/nchembio.2528)                                                                                 | "reveal a previously undisclosed allosteric binding site" and "highly potent (IC50 < 10 nM), selective USP7 inhibitors". The companion Nature paper (doi:10.1038/nature24451, PMC6029662) was retrieved in full but is about a **different** series that binds "in the Thumb-Palm cleft that guides the ubiquitin C-terminus into the active site", within 4.7 Å of the catalytic cysteine, so it does not establish this site. Note `../secondary/README.md` §7.10: `usp7` was already rejected once on clause (ii), on a different compound                                                                                                                                                                                                      |
| `pyrH`  | `GTP`    | Acta Cryst. D full text 403; abstract only (doi:10.1107/S0907444912011407)                                                                                       | "six GTP molecules at its centre". No functional measurement in the abstract, and "at its centre" in a hexamer is an interface hazard                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| `kgd`   | `ACO`    | Chemistry & Biology full text 403; abstract only (doi:10.1016/j.chembiol.2011.06.004)                                                                            | "acetyl-CoA, a powerful allosteric activator able to enhance the concerted protein motions observed during catalysis". A search of PMC for an open-access substitute on mycobacterial KGD returned nothing on this enzyme                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| `murI`  | `003`    | Nature full text 403; abstract only (doi:10.1038/nature05689)                                                                                                    | "inhibitors specifically targeting Helicobacter pylori glutamate racemase that bind to a cryptic allosteric site". The open-access follow-up found in PMC (doi:10.1128/AAC.00226-09) is metadata-only — "The publisher of this article does not allow downloading of the full text in XML form"                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `CTSK`  | `6HM`    | FEBS Letters full text 403; abstract only (doi:10.1002/1873-3468.12495)                                                                                          | Abstract: "compound NSC94914 binds this site and acts as a specific partial inhibitor of the collagenolytic activity of cathepsin K". `5JA7` is titled "Human cathepsin K mutant C25S in complex with the allosteric effector NSC94914", so the identity is confirmed. **But** an earlier open-access paper from the same group (doi:10.1371/journal.pone.0106642, PMC4153677) reports of the eight modifiers it tested — a set that includes NSC94914 — "only compounds 1 and 2 showed a concentration-dependent inhibitory effect…whereas no inhibitory, or activating, activity was observed for the remaining six compounds". The two are reconcilable (different substrates) but this row must not be admitted without reading the 2016 paper |
| `opd`   | `EBP`    | Arch. Biochem. Biophys. full text 403; abstract only (doi:10.1016/j.abb.2005.08.012)                                                                             | The strongest UNREAD abstract in the set: "bound exclusively into a well-defined surface pocket 12 A away from the active site", with a "4-fold increase in the hydrolysis of demetonS", a "183-fold decrease with DFP", and "non-competitive inhibition of paraoxon hydrolysis by EBP with [an active-site mutant], in contrast to the native enzyme, which showed competitive inhibition". **Chase this one first**                                                                                                                                                                                                                                                                                                                              |
| `kmo`   | `7ZR`    | FASEB J. full text 403; abstract only (doi:10.1096/fj.201700397RR)                                                                                               | "Ro 61-8048 inhibits the enzyme in an allosteric manner"; "tunnel binds the Ro 61-8048 molecule". Identity confirmed: `7ZR` is Ro 61-8048 and `5Y66` is "Crystal structure of Pseudomonas fluorescens Kynurenine 3-monooxygenase in complex with L-KYN and Ro61-8048"                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| `AMY2A` | `0XR`    | J. Med. Chem. full text 403; abstract only (doi:10.1021/jm301273u)                                                                                               | `0XR` is ethyl caffeate, confirmed by `data.rcsb.org`, and `4GQQ` is "Human pancreatic alpha-amylase with bound ethyl caffeate". The abstract says it "operates from binding sites far removed from the active site" and "acts by disordering precisely those polypeptide chain segments that make up the active site binding cleft", but reports no kinetic number. Note the plural "sites"                                                                                                                                                                                                                                                                                                                                                       |
| `Ptgs2` | `PLM`    | JBC full text not served ("only front matter and abstract"); abstract only (doi:10.1074/jbc.M111.231969)                                                         | "Palmitic acid, an efficacious stimulator of human PGHS-2, binds only E_allo in palmitic acid/murine PGHS-2 co-crystals" and "E_cat is regulated by E_allo in a manner dependent on what ligand is bound to E_allo". The allostery is between the two monomers of a conformational heterodimer, so within one chain the "allosteric site" is the COX catalytic site. See §3                                                                                                                                                                                                                                                                                                                                                                        |
| `Pck1`  | `1WD`    | _Biochemistry_ full text 403; abstract only (doi:10.1021/acs.biochem.5b00822)                                                                                    | "PEPCK is inhibited by the binding of MPA at two discrete binding sites: one acting in a competitive fashion with PEP/OAA (∼10 μM) and the other acting at a previously unidentified allosteric site (Ki ∼ 150 μM)." Identity confirmed: `1WD` is 3-sulfanylpyridine-2-carboxylic acid, i.e. 3-mercaptopicolinic acid. **But `4YW8` holds exactly one copy of `1WD`** and the paper describes two sites, so which site the row annotates cannot be determined without the paper                                                                                                                                                                                                                                                                    |
| `gyrB`  | `94H`    | PNAS full text not served ("The publisher of this article does not allow downloading of the full text in XML form"); abstract only (doi:10.1073/pnas.1700721114) | "compounds binding to a protein pocket between the winged helix domain and topoisomerase-primase domain, remote from the DNA", "consistent with allosteric inhibition of DNA gyrase". `09-extension-sweep.md` §6.6 already says this row should be treated as dead: the holo is a protein/DNA complex and ADR 0010 gives the DNA nowhere to go                                                                                                                                                                                                                                                                                                                                                                                                     |
| `Enpp2` | `7CR`    | J. Med. Chem. full text 403; abstract only (doi:10.1021/acs.jmedchem.6b01743)                                                                                    | "potent competitive Autotaxin inhibitors that do not interact with the catalytic site". `5M0E` is "Structure-based evolution of a hybrid steroid series of Autotaxin inhibitors". Competitive kinetics do not by themselves refute allostery (`../secondary/README.md` §7.10), but the pocket in question is the lipid-substrate channel, so this needs the paper                                                                                                                                                                                                                                                                                                                                                                                  |
| `pfkA`  | `ADP`    | Phil. Trans. R. Soc. B full text 403; abstract only (doi:10.1098/rstb.1981.0059), **and the reference is a review**                                              | "The third site binds both allosteric activator and inhibitor"; "cooperative kinetics with respect to the substrate fructose-6-phosphate"; "allosteric activation by ADP, and inhibition by phosphoenolpyruvate". See §3 for two further defects on this row                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| `PYGM`  | `AMP`    | JMB full text 403; abstract only (doi:10.1016/0022-2836(91)90887-c, PMID 1900534, confirmed)                                                                     | "AMP binds to R state GPb with at least 100-fold greater affinity". `../secondary/README.md` §7.3 has already measured this site drawing lining residues from two protomers on a different holo entry, so clause (ix) remains the live question regardless of clause (ii)                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |

---

## 3. Defects found — thirteen, in four classes, plus one correction

The failure mode `09-extension-sweep.md` §5 warns about — a curation DOI pointing at a paper
about a different protein — **did not recur**. All twenty PubMed-resolvable references matched
their row's protein. The defects are of four other kinds, and the last two classes are ones no
DOI check would catch.

### Class 1 — right protein, wrong question

1. **`AMD1`.** ASD's reference, doi:10.1021/bi0268854, is "Mechanism of human S-adenosylmethionine
   decarboxylase proenzyme processing as revealed by the structure of the S68A mutant". Its
   abstract is about processing chemistry and reports no functional evidence for the putrescine
   site. The functional paper is **doi:10.1021/bi801732m**, which is also the citation of the
   row's own proposed apo entry. The row passes on that paper, not on ASD's.
2. **`hisG`.** ASD's reference, doi:10.1074/jbc.M212124200, is a crystal-structure paper. The
   inhibition kinetics that decide the row are in **doi:10.1021/bi300808b**, an open-access paper
   ASD does not cite.
3. **`pfkA`.** ASD's reference, doi:10.1098/rstb.1981.0059, is a **review** ("Phosphofructokinase:
   structure and control"), not a report of new experiments.

### Class 2 — right protein, wrong site

4. **`LTA4H`.** The row annotates `692` as an allosteric effector. The curation paper's own
   screen placed all but one of its fragments in the substrate cleft, and the one exception was
   non-inhibitory. Either way the row is not an allosteric site. `692` is
   "N-methyl-1-(2-thiophen-2-ylphenyl)methanamine"; its compound number in the paper could not be
   resolved because the compound-to-PDB-code mapping lives in figure panels and Supporting
   Information the full text does not carry.
5. **`rocF`.** The row's effector is `ARG`, which is arginase's **substrate**, and `3CEV` holds
   six copies of it beside twelve manganese ions. The paper reports a second, remote arginine
   site from structure alone. Which copy ASD annotated is not determinable from the row.
6. **`NT5C2`.** The row annotates `ADN` in `2JC9`. Adenosine is this enzyme's reaction product,
   `2JC9` is titled "in complex with adenosine", and the curation paper's abstract places its
   modelled effectors — diadenosine tetraphosphate and 2,3-bisphosphoglycerate — at an effector
   site "located near a subunit interface", not at an adenosine site.
7. **`nirK`.** The pocket is created by an engineered point mutation and sits where a copper
   ligand sits in the wild type.
8. **`Ptgs2`.** The "allosteric site" is the cyclooxygenase site of the **partner monomer**. In a
   one-chain node set (ADR 0010) it is the catalytic site, and clause (vii) would remove the
   entire label set.

### Class 3 — the deposited entry cannot support the pair

9. **`PDE10A`.** The proposed apo `2OUS` is a 331-residue **catalytic**-domain construct
   ("crystal structure of PDE10A2 mutant D674A"); the holo `2ZMF` is a 189-residue **GAF-B**
   domain. They are non-overlapping regions of one UniProt entry. The sweep checked clause (iv)
   as UniProt identity, which cannot see this. **Any ASD-derived pipeline needs a residue-range
   overlap check, not an accession check.**
10. **`AMD1` again.** The holo `1MSV` is the unprocessed proenzyme (one polymer entity); the
    proposed apo `3EP3` is the processed enzyme (two polymer entities, α and β from one gene
    product). Clause (v) requires the same oligomeric state, and ADR 0010's one-chain node set
    would cut the processed form in half.
11. **`Pck1`.** `4YW8` holds **one** copy of `1WD` while the paper describes MPA at two discrete
    sites. The row does not say which.

### Class 4 — no citation at all

12. **`pfkA`.** `4PFK`'s primary citation in RCSB is the PDB's own DOI, `10.2210/pdb4pfk/pdb` —
    the entry has no journal citation. It also holds two ADP copies, one of which is at the
    catalytic site.
13. **`FDPS`'s proposed apo.** `4NUA` is "To be Published", citation DOI `10.2210/pdb4nua/pdb`,
    and it is a double point mutant carrying risedronate at the catalytic site. This is the same
    class of problem `../secondary/README.md` §7.1 names when it says "three of the five apo
    entries have no primary citation".

### One correction to `09-extension-sweep.md` §4.2

14. **`FBP1`.** §4.2 records the curation reference as "PMID Not in PubMed (no DOI in PubMed)".
    It is in PubMed: PMID 23844654, **doi:10.1021/bi400532n**, PMC4869526, _Biochemistry_ 2013.
    The row's title string matched the paper exactly; only the identifier lookup failed.

---

## 4. Ranked shortlist

Ranked by what each would add to a set that currently has **zero physiological effectors, no
protein under 272 residues, four organisms and 0.86 dex of size span**, then discounted by the
structural work still outstanding. Apo/holo usability is judged from `09-extension-sweep.md` §4
and from the entry metadata retrieved here.

|   # | Target      | Adds                                                                                                                                                                                  | Apo/holo, as named in §4                                                                                                                                        | Outstanding                                                                                                                                                                                                                                                                                                                                                                              |
| --: | ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|   1 | **`hisG`**  | **Physiological** metabolite (L-histidine feedback), **new organism** (_M. tuberculosis_), 284 aa, three independent kinetic lines                                                    | `5U99` 2.40 Å → `1NH8` 1.80 Å. Apo carries `ATP`, `MG` — the enzyme's own substrate at the **active** site, which clause (iii) permits, but it must be measured | clause (iii)/(x) distance measurement; clause (ix) re-check — the abstract of the curation paper places the site near the subunit boundary in some organisms; holo entity length is 304 against a 284-residue UniProt                                                                                                                                                                    |
|   2 | **`UBE2I`** | **158 aa** — the only pass below 272, and a monomer rather than an obligate oligomer. Human                                                                                           | `5F6E` 1.12 Å → `5F6Y` 1.14 Å. Apo carries nothing but water                                                                                                    | potency is millimolar (fragment-grade), which is weaker than the `smyd3` precedent in `../secondary/README.md` §7.5; the holo is a **triple mutant**, so clause (iv) must be measured; and `09-extension-sweep.md` §6.2 is right that the active-site rule is the exposed clause — Ubc9 has a catalytic cysteine and no cofactor                                                         |
|   3 | **`AMD1`**  | **Physiological** metabolite (putrescine), human, 334 aa, a polyamine chemistry nothing else in either set carries                                                                    | `3EP3` 1.84 Å → `1MSV` 1.75 Å. Apo carries `PYR`                                                                                                                | **the processed/unprocessed chain-architecture mismatch in §3 item 10 is probably fatal as assigned**; a different apo/holo choice may repair it. Site is 15–20 Å from the active site and described as near the dimer interface                                                                                                                                                         |
|   4 | **`PDC1`**  | **Physiological** (pyruvate substrate activation), **new organism** (_S. cerevisiae_), 563 aa, and a distinct allosteric class — hysteretic substrate activation rather than feedback | `1PVD` 2.30 Å → `2VK1` 1.71 Å. Apo carries `MG`, `TPP`, both cofactors at the **active** site                                                                   | the effector is **covalently** bound as a thiohemiketal, which AlloBench excludes by rule (`09-extension-sweep.md` §6.5); the regulatory loops are described as "in the neighborhood of the active site at the core region of the tetramer", so clause (ix) needs care                                                                                                                   |
|   5 | **`FDPS`**  | **Physiological** product feedback, human, 419 aa. The 2026-08-24 record already called this "the best clause (ii) evidence in the whole sweep" and this pass confirms it             | `4NUA` 1.43 Å → `5JA0` 1.90 Å                                                                                                                                   | **the proposed apo has no publication and two point mutations** (§3 item 13), and carries risedronate at the catalytic site — the same freeze-level decision the earlier record describes, not a new one. A different apo is worth looking for                                                                                                                                           |
|   6 | **`LDHA`**  | **Physiological** metabolite (oxaloacetate), **new organism** (_O. cuniculus_), 332 aa                                                                                                | `5KKC` 1.86 Å → `5NQQ` 1.87 Å. Apo carries `6V0`, an inhibitor — **this is the row most likely to fail clause (iii)/(x)**                                       | the authors themselves write that it is "unlikely that malonate (and perhaps oxaloacetate) play an important role in the regulation of rabbit L-LDH activity"; Ki is 2.3 mM; and the site is "adjacent to, but not within, the active site", so clause (vii) will bite                                                                                                                   |
|   7 | **`FBP1`**  | **Physiological** metabolite (AMP), **new organism** (_S. scrofa_), 338 aa, the textbook case                                                                                         | `1NUY` 1.30 Å → `2F3D` 1.83 Å. Apo carries `F6P`, `MG` at the **active** site                                                                                   | PF00316 admits one arm, and the human FBPase candidate from the 2026-08-24 sweep competes for it; the deciding kinetics are cited rather than measured in the retrieved paper; and FBPase is a classically cooperative oligomer, so it needs the clause (viii) disclosure `09-extension-sweep.md` §6.8 requires                                                                          |
|   8 | **`LGMN`**  | Human, 433 aa, a genuinely distal exosite at ~30 Å with three lines of evidence — the cleanest **distal** site among the passes                                                       | `4N6O` 1.80 Å → `5LU8` 1.95 Å. Apo carries nothing but water                                                                                                    | the same compound also binds the active site, so the pair is bitopic in effect; `5LU8` carries a covalent active-site block and glycans; and `../secondary/README.md` §7.1 records legumain failing an earlier sweep for a site that was not topographically distinct — **that earlier rejection was about a different structure and this pass does not overturn it, it sits beside it** |

**Not shortlisted, and why.** `proRS` (746 aa, _P. falciparum_, synthetic effector) and `fbpC`
(340 aa, _M. tuberculosis_, covalent synthetic effector) are sound passes that add organisms but
no physiological chemistry and no size headroom; `fbpC` also carries the covalent-modulator
question. `PARP14` passes cleanly but is a **non-catalytic reader domain**, which
`../secondary/README.md` §7.4 puts out of scope, and only its second macrodomain is modelled.
`GAA` is the weakest pass — its mechanism is chaperoning rather than modulation of a folded
enzyme's turnover, its KD is 11.57 mM, and its activity data were read at abstract level.
`lacS` should **not** be admitted: its functional evidence is unimpeachable but the site is a
cavity engineered into the protein by a tryptophan-to-glycine mutation, so predicting it from
an apo structure is not the task this benchmark poses.

**Effect on the stated gaps, if the top eight were admissible.** Physiological effectors would
go from 0 to 6 (histidine, putrescine, pyruvate, FPP, oxaloacetate, AMP), the sub-272 floor
would be filled once (158), and organisms would gain _M. tuberculosis_, _S. cerevisiae_,
_O. cuniculus_ and _S. scrofa_. **None of that is available today**, because every one of the
eight has at least one unmeasured or adverse structural clause in the right-hand column.

---

## 5. What this cannot settle

1. **Sixteen rows are undecided, and eleven of those have favourable abstracts.** The pass count
   is a floor, not an estimate. If the publisher wall were crossed, `opd`, `kmo`, `murI`, `CTSK`,
   `Pck1`, `Enpp2`, `USP7` and `kgd` would each plausibly pass, and `pyrH`, `pfkA`, `PYGM`,
   `Ptgs2`, `birA` and `NT5C2` would each plausibly fail on the second reading. **Do not quote 13
   as "the answer"; quote it as "13 established, 16 unknown, 5 refuted".**
2. **A clause (ii) pass is the cheapest of the remaining clauses, not the last one.** Seven of
   the thirteen passes carry a structural blocker found incidentally here (§3). Clause (iii)/(x)
   was not measured for any row, clause (ix) was not re-measured, and clause (iv) was checked as
   UniProt identity only. `09-extension-sweep.md` §6.3 puts the historical clause (iii)/(x) kill
   rate at 40 %. Applying that to thirteen leaves about eight, before clause (ix) is re-run.
3. **The `aa` column in `09-extension-sweep.md` §4 is the UniProt length, not the modelled chain,
   and the size claims rest on it.** Measured here from RCSB entity lengths: `PDE10A`'s holo
   models 189 residues against a 1055-residue UniProt; `PARP14`'s holo is one macrodomain of an
   1801-residue protein; `FDPS`'s holo models 375 of 419; `kgd`'s models 868 of 1227; `GAA`'s
   holo is a mature construct. **The "1.06 dex, 158 to 1801" span in §4.1 is therefore an
   overstatement of what a method would actually receive**, and the correction runs in the
   direction that makes the scalability gap harder to fill, not easier.
4. **Four passes rest on a paper ASD does not cite.** `hisG`, `AMD1` and `GAA` were decided on
   substitute or companion papers found by open-access search, and `FBP1` on a reference §4.2
   recorded as unresolvable. That is a good outcome for those rows and a bad one for the method:
   **ASD's curation reference is not reliably the paper that carries the functional evidence**,
   so a pipeline that reads only the cited DOI will under-count passes as well as over-count
   them.
5. **The quotations are faithful, not certified.** See §0.4. Each was returned by a retrieval
   pass over the source and is given with its section so that it can be checked in one lookup.
6. **`lacS` and `nirK` were both decided on a definition, not on a measurement.** Both have
   unambiguous functional data for a site that exists only because of a mutation. `lacS` is
   recorded as a pass with a recommendation not to admit; `nirK` as a fail. A reviewer could
   reasonably swap them, and if the repository wants a rule it should be written as a clause
   rather than settled twice by judgement.
7. **Nothing here re-opens a freeze.** `../secondary/README.md` §7.10 and `09-extension-sweep.md`
   §6.9 both hold: adding an arm re-runs the seeded size-stratified split and changes every
   existing tier assignment. This document supplies evidence for a decision that has not been
   taken.
8. **The `692` compound number was not resolved**, and the `LTA4H` fail therefore rests on a
   disjunction rather than on one identification. Both branches fail, which is why the verdict
   stands, but the row deserves one more look if anyone has the Supporting Information.
9. **No apo entry was opened.** The question "does the apo hold a ligand at the site" was
   answered from the component lists `09-extension-sweep.md` §4 already records, not from
   coordinates. The flag on `LDHA`'s `6V0` and `FDPS`'s `RIS` is a suspicion raised from a
   component name, not a measurement.

---

## Provenance

Every DOI, PubMed identifier, PMC identifier, structure title, chemical-component name and
quotation in this document came from a live retrieval on 2026-09-02, through
`pmc.ncbi.nlm.nih.gov/tools/idconv`, `eutils.ncbi.nlm.nih.gov`,
`www.ebi.ac.uk/europepmc/webservices/rest` and `data.rcsb.org/rest/v1`. Nothing is recalled.
The candidate list, its tiers, its accessions and its curation DOIs were read from
[`09-extension-sweep.md`](09-extension-sweep.md) §4 and §4.2 and from
[`data/extension-candidates-2026-09.json`](data/extension-candidates-2026-09.json). The clause
(ii) text and its authority were read from [`../primary/README.md`](../primary/README.md) §1;
the four selection clauses from [`../secondary/README.md`](../secondary/README.md) §4.
