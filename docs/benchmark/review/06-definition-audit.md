# Independent re-audit of the eight-clause pair definition

**Date of search: 2026-09-02.** Adversarial re-audit of the normative definition in
[`../primary/README.md`](../primary/README.md) §1, against literature published or revised
since mid-2025, and against what a pharma structure-based drug discovery (SBDD) group would
say. It does not restate
[`../evidence/allosteric-pair-definition.md`](../evidence/allosteric-pair-definition.md),
[`../evidence/apo-holo-definition.md`](../evidence/apo-holo-definition.md) or
[`../evidence/curation-standard.md`](../evidence/curation-standard.md); all three were read
first and are assumed.

**Retrieval method and its limit.** Sources were retrieved through the Europe PMC REST API
(`search`, `fullTextXML`) and publisher pages, via a fetch-and-summarise tool. Quoted strings
are therefore **one step removed from the raw XML** — they are as returned by that tool, not
as read from the file. Anything load-bearing must be re-quoted from the raw source before it
enters `docs/report/`. Tags follow the repo convention
(`[VERIFIED-FULLTEXT]`, `[VERIFIED-ABSTRACT]`, `[UNVERIFIED]`, `[NOT-RETRIEVABLE]`,
`[NOT ESTABLISHED]`), with that caveat applied uniformly.

---

## Headline verdict

**The definition holds up, with four caveats — two of which require an edit to a factual
claim, not merely a hedge.**

It holds because nothing published since mid-2025 contradicts any of the eight clauses, and
two new sources strengthen them. No new definition of "allosteric site" has appeared. No
successor to Wankowicz 2022 changes the apo/holo curation standard. ASD has not been
re-released since ASD2023. No CASP-style blind community assessment of allosteric-site
prediction exists.

The four caveats:

1. **One factual claim is now false as stated.** `../primary/README.md` §1 says "No formal
   definition of an allosteric site in any source we have **read** contains a minimum
   separation from the active site." Kincore defines an allosteric (Type IV) kinase ligand as
   one whose "minimum distances from the hinge region and C-helix-Glu(+4) residues are both
   **>6.5 Å**" (`doi:10.1093/nar/gkab920`) `[VERIFIED-FULLTEXT]`. That is a published,
   metric, minimum-separation convention. It is family-specific and ligand-to-landmark rather
   than site-to-site, and the repo's sentence survives literally because Kincore was not among
   the sources read — but the implied claim that none exists is wrong, and **BCR-ABL1 is a
   kinase**, so the convention is directly applicable to one of the four targets.

2. **The "site-apo is the majority reading" claim has weakened.** CryptoBank (Sci Adv 2026,
   6 million apo/holo alignments) applies an **entry-level** apo filter — "apo structure filter
   selecting entries with **no nonpolymer entities**" (`doi:10.1126/sciadv.ady6364`)
   `[VERIFIED-FULLTEXT]`. That is a second global-apo source, at a scale that dwarfs the
   site-relative ones, published after the repo froze. Site-apo remains defensible; "majority"
   now needs qualifying to "majority among resources that annotate apo/holo per binding site".

3. **Two clause tags are wrong by the repo's own glossary.** Clause (ii) is tagged
   `[IN-DOMAIN]` in `../primary/README.md` §1 but `[IN-DOMAIN + REPOSITORY POLICY]` in the
   evidence document — an internal inconsistency. Clause (vii) is tagged `[BORROWED]`, but its
   only cited authority (AlloPred) is squarely in the allostery domain, and the repo defines
   `[BORROWED]` as "addressed only by an adjacent field".

4. **The negative class is less safe than the benchmark assumes.** Beltran et al. identify
   "42 major allosteric sites (OR > 2, FDR < 0.1): 7 in the N lobe and 35 in the C lobe" in a
   single kinase by deep mutational scanning, and report that "computational methods do not
   successfully predict the allosteric pockets in Src" (`doi:10.1126/sciadv.aea2726`)
   `[VERIFIED-FULLTEXT]`. If one kinase carries dozens of functionally allosteric surfaces,
   residues scored as negatives in a one-site-per-arm benchmark include an unknown number of
   real positives. This does not invalidate the definition; it is a limitation the evaluation
   layer must disclose.

Nothing found requires a clause to be deleted, added, or reversed.

---

## 1. Currency check — what is new since mid-2025

### 1.1 The single most relevant new source: CAPASP

Ai Y, Li H, Huang X, Liu S. _A systematic evaluation of protein allosteric site prediction
tools with independent datasets._ J Comput Aided Mol Des 2026. `doi:10.1007/s10822-026-00831-4`,
PMID 42126486. Not open access; **not in Europe PMC**, so `[VERIFIED-ABSTRACT]` only.

> "we created two independent datasets that had not been used in selected computational
> protocols: a **CAPASP-General subset comprising holo state allosteric proteins** and a
> **CAPASP-Unbound subset comprising apo state allosteric proteins**. We then systematically
> evaluated the accuracy of five allosteric site prediction tools across five dimensions:
> sensitivity, specificity, F1-score, MCC value and ranking capability… these models performed
> **better with the CAPASP-General subset than with the CAPASP-Unbound subset**, suggesting
> that the prediction models require further improvement."

Three things follow.

- **This is the first purpose-built apo-vs-holo split in allosteric-site evaluation.** Until
  now the apo penalty was in-domain only via ESSA's 10/14 → 7/14. CAPASP makes the split the
  organising principle of an evaluation set. The repo's C1 (apo input only) now has direct
  in-domain empirical backing that did not exist when clause (viii) was written.
- **CAPASP is not a community assessment.** It is a dataset name inside one retrospective
  paper by one group. It is not CASP-like: no blind rounds, no registration, no independent
  hub. Anyone reading "CAPASP" as a CASP analogue is mistaken.
- **The construction protocol is unretrievable.** The paper is paywalled and outside Europe
  PMC. What defines CAPASP-Unbound's "apo" — global, site-relative or ligand-stripped — is
  `[NOT ESTABLISHED]`. _Closes by: institutional access to the Springer PDF._

### 1.2 CryptoBank — the new PDB-scale apo/holo resource

Febrer Martinez P, Fröhlking T, Borsatto A, Gervasio FL. _CryptoBank._ Sci Adv 2026;
12(17):eady6364. `doi:10.1126/sciadv.ady6364`, PMC13267282, OA `[VERIFIED-FULLTEXT]`.
(Note: the repo refers to "CryptoBank 2025"; the preprint is 2025
`doi:10.1101/2025.04.23.650184`, the journal article is 2026, and the headline crypticity
figure moved from 16.3% to 18.4% between them.)

Its curation clauses, for direct comparison against `curation-standard.md` §3:

| Clause           | CryptoBank value                                                                                                                                                                                                                                   |
| ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Apo definition   | "Apo structure filter selecting entries with **no nonpolymer entities**" — entry-level, not site-relative                                                                                                                                          |
| Holo definition  | "preliminary holo structure filter selecting entries with **at least one nonpolymer entity**"                                                                                                                                                      |
| Resolution       | "structures with resolution higher or equal to **2.5 Å**"                                                                                                                                                                                          |
| Redundancy       | "**95%** sequence identity cluster"                                                                                                                                                                                                                |
| Ligand exclusion | "ions, low molecular weight compounds (**<60 Da**), solvents"                                                                                                                                                                                      |
| Superposition    | PyMOL global alignment, five refinement cycles                                                                                                                                                                                                     |
| Pair admission   | "only alignments that resulted in a **Cα RMSD lower than 2.5 Å** were selected for scoring"                                                                                                                                                        |
| Crypticity       | ML crypticity score; "a binding site is flagged as cryptic if its **mean site score is ≥ 0.5**"                                                                                                                                                    |
| Scale            | "**6 million** unique apo-holo-ligand combinations"; "~574,000 apo-holo-ligand combinations associated with crypticity, distributed across **3643** distinct clusters of 95% sequence identity… accounting for **18.4%** of all identity clusters" |

Two consequences for this repo. First, it is a **fourth** operationalisation of crypticity
(after Fpocket+ConCavity score transition, LIGSITE ≥20 Å³, and pocket RMSD >2 Å) — a learned
classifier rather than a threshold. Second, the apo clause is global, which is the point in
caveat 2 above.

### 1.3 Community standards

Wankowicz SA. _Ten rules for a structural bioinformatic analysis._ PLoS Comput Biol 2025;
21(10):e1013094. `doi:10.1371/journal.pcbi.1013094`, PMC12578330, OA `[VERIFIED-FULLTEXT]`.

**Correction to the brief that commissioned this audit: this paper is single-authored by
Wankowicz. Fraser is not a co-author.** The repo does not currently cite it; it should. Its
ten rule headings are: define your biological selection criteria; determine how you will
quality control your data; re-processing structural model data; the PDB and structural models
are weird and biased; consider your analysis's sample size, statistics, overfitting, and
uncertainty; determine and apply the correct controls; understand how metrics are compared
across your structures; appropriately connect and compare structures; connect your analysis
to other databases or prospective experiments; visualize everything.

Three lines bear directly on frozen clauses:

> "**Controls must directly address the null hypothesis you wish to reject.**"

> "**High B-factors do not necessarily guarantee high flexibility in solution. To use them
> reliably, it's best to normalize B-factors.**"

> "High resolution, **better than 2.5 Å**, is essential for accurate side chain positioning,
> whereas lower resolution models can yield insights."

The B-factor line is the actionable one: the repo characterises pairs by deposited B-factor
and, on this guidance, should report a normalised B-factor.

**No successor to it, and no wwPDB or IUPAC/IUPHAR nomenclature revision, was found.** A
targeted search for IUPHAR allosteric-nomenclature updates after Christopoulos 2014 (XC,
`doi:10.1124/pr.114.008862`) returned nothing later than the Concise Guide series, which is a
target catalogue rather than a nomenclature recommendation. Recorded as a negative search
result, not as proof of absence. IUPAC Gold Book 14107 remains `[NOT-RETRIEVABLE]` — no new
route was attempted, and the repo's existing account of the failure stands.

### 1.4 Databases and benchmarks

| Resource       | Status as of 2026-09-02                                                                                                |
| -------------- | ---------------------------------------------------------------------------------------------------------------------- |
| ASD            | **No release after ASD2023** (`doi:10.1093/nar/gkad915`) found `[VERIFIED-ABSTRACT]`                                   |
| ASBench        | No update. AlloBench's 2025 verdict that it is "outdated" stands                                                       |
| CASBench       | No update                                                                                                              |
| AlloBench      | Current (2025, `doi:10.1021/acsomega.5c01263`). Still the most explicit protocol in-domain                             |
| CryptoBench    | No v2 found. Remains `doi:10.1093/bioinformatics/btae745`                                                              |
| AHoJ / AHoJ-DB | No new release found                                                                                                   |
| CryptoBank     | **New** (§1.2)                                                                                                         |
| CAPASP         | **New** (§1.1)                                                                                                         |
| AlloFusion D24 | **New** independent test set of 24 sites, inside a method paper (`doi:10.1021/acs.jcim.5c01033`) `[VERIFIED-ABSTRACT]` |

### 1.5 New methods, and what they say about the definition

None introduces a new definition; all reuse ASD-derived labels. Two are worth reading anyway.

- **AlloEF** — Zhang J, Sun X, Wu Z, Su J, Zhang X, Li C. J Phys Chem B 2026;130(19):4970-4981.
  `doi:10.1021/acs.jpcb.6c00242` `[VERIFIED-ABSTRACT]`. Combines **transfer entropy** and
  **energetic frustration** with sequence/structure/network features; F1 0.630, MCC 0.609.
  The sentence that matters for clause (i): "AlloEF can detect not only the allosteric sites in
  the canonical allosteric pockets but also the ones **distributed beyond the pocket regions**."
- **AlloFusion** — Huang J, Guo D, Liu Y, Wang Y, Lv M. J Chem Inf Model 2025;65(16):8858-8870.
  `doi:10.1021/acs.jcim.5c01033` `[VERIFIED-ABSTRACT]`. "current computational methods often
  rely on static structures or single-modality features, limiting their ability to identify
  allosteric sites that are **transient, cryptic, or located outside conventional pockets**."

Also new and in scope, recorded without further analysis: DeepAlloWeb
(`doi:10.1016/j.jmb.2026.169863`), ZHMolEReP (`doi:10.1021/acs.jcim.6c00141`, already in the
repo), Gatlin W et al. Protein Sci 2026;35(8):e70714 (`doi:10.1002/pro.70714`, frustration +
pLM on kinases), Yuce & Kurkcuoglu Proteins 2026 (`doi:10.1002/prot.70122`, network models for
allosteric sites), Chen EA & Zhang Y J Chem Inf Model 2025 (`doi:10.1021/acs.jcim.5c00331`,
blind docking fails on allosteric compounds).

### 1.6 Is there a CASP for allosteric-site prediction?

**No.** `[VERIFIED-FULLTEXT]` for the nearest analogue. The closest existing community
experiment is **CACHE** — Ackloo S et al. Nat Rev Chem 2022;6(4):287-295,
`doi:10.1038/s41570-022-00363-z`, PMC9246350:

> "Critical Assessment of Computational Hit-finding Experiments (CACHE), a public benchmarking
> project to compare and improve small molecule hit-finding algorithms through cycles of
> **prediction and experimental testing**… CACHE will launch 3 new benchmarking exercises every
> year."

CACHE assesses **hit finding**, not site prediction, and its author list is heavily industrial
(Bayer, Boehringer, Novartis, AstraZeneca, Sanofi, Takeda, Merck KGaA). Results papers exist:
CACHE Challenge #3 targeting the SARS-CoV-2 Nsp3 macrodomain
(`doi:10.1021/acs.jcim.5c02441`, PMC12892310) and Challenge #2 targeting the NSP13
RNA-binding site (`doi:10.1021/acs.jcim.6c00560`) `[VERIFIED-ABSTRACT]`. The design point the
repo should note: **CACHE's ground truth is prospective experiment, not a curated label set.**
That is the standard the field's industrial half actually respects.

---

## 2. Clause-by-clause adversarial challenge

For each clause: (a) does a majority of the field apply it; (b) is there a published
contradiction; (c) what a pharma SBDD reviewer would say; (d) is the tag correct.

### (i) Effector — tagged `[IN-DOMAIN + REPOSITORY POLICY]`

**(a) Majority: yes for the practice, no for the value.** Every curated set defines site
residues by a contact shell around the modulator: ASD v2.0 6 Å, CASBench 5 Å, CryptoSite and
PocketMiner 5 Å, AHoJ and CryptoBench 4.5 Å, ASBench/AlloBench/Riedlová 4 Å, Amor 3.5 Å. The
repo's 4.5 Å matches AHoJ and CryptoBench. All already established in the evidence documents.

**(b) Contradiction: yes, two kinds.** First, non-radius label conventions are in current use
— PASSer's "nearest pocket to the modulator", AlloPred's "any pocket containing ≥1 contact
residue", AlloBench's Jaccard over pocket residues. A top-3 pocket number is not commensurable
with a residue-level AUC, and the repo already says so. Second, and new: **two 2025-26 in-domain
methods state that allosteric residues fall outside pockets** — AlloEF
(`doi:10.1021/acs.jpcb.6c00242`) and AlloFusion (`doi:10.1021/acs.jcim.5c01033`), with STINGAllo
putting it at "approximately 18% of experimentally confirmed sites that lie outside surface
invaginations" (`doi:10.1016/j.csbj.2024.10.036`) `[VERIFIED-ABSTRACT]`. A shell around a
deposited effector is a _lower bound_ on the allosteric surface, not the surface.

**(c) Pharma reviewer.** Four questions, in order. Which atom set — heavy atoms only, and were
symmetry mates included? Does the deposited ligand actually have density supporting the pose
(the repo answers this: `6OIM` MOV RSCC 0.908, `5MO4` AY7 0.946 — good, and better than the
field standard, which skips density entirely). Is a 4.5 Å shell of a large effector the
pharmacophorically relevant subset, or is half of it solvent-exposed rim? And: **you have
given me residues; I design to a pocket.** They will ask for the pocket volume and shape, not
a residue list.

**(d) Tag: correct.** The practice is in-domain, the specific 4.5 Å is repository policy.
**One scope gap:** the clause says "identified by its PDB chemical component ID", which
silently restricts effectors to small molecules with a component ID. AlloBench does the same
("Only the entries with small-molecule allosteric modulators were selected"), but IUPHAR XC §III
explicitly admits a protein second ligand ("small molecule **or protein**"). The repo narrows
the authority it cites, and should say so in one clause.

### (ii) Provenance of label — tagged `[IN-DOMAIN]` in README, `[IN-DOMAIN + REPOSITORY POLICY]` in the evidence doc

**(a) Majority: no. This is the clause the field most conspicuously fails to apply.** ASD v1 is
the only release that stated an evidence bar ("at least three cases of experimental evidence")
and every later release dropped it. Every downstream predictor inherits ASD labels without
re-deriving the functional evidence. AlloBench documents the consequence: "the tab-delimited
file had missing values in the column for allosteric site residues for **1620 out of 3102**
entries"; "only **46%** of entries have annotations for orthosteric sites". So clause (ii) is
in-domain **as a stated principle** (ASD v1, IUPHAR XC §III, Fenton's energy cycle) and
**repository policy as an enforced practice**. The README tag is therefore incomplete and the
two documents disagree with each other.

**(b) Contradiction: not to the principle, but to its consequences.** Beltran A, Naqvi MM,
Faure AJ, Lehner B. _The allosteric landscape of the Src kinase._ Sci Adv 2026;12(7):eaea2726.
`doi:10.1126/sciadv.aea2726`, PMC12893324 `[VERIFIED-FULLTEXT]`. They define allosteric sites
functionally, exactly as clause (ii) demands — "residues outside the active site that are
enriched in mutations modulating kinase activity" (OR > 2, FDR < 0.1) — and find **42 major
allosteric sites: 7 in the N lobe and 35 in the C lobe**, with "28 predicted small-molecule
fragment-binding hotspots" of which "16 Src pockets [are] enriched for inhibitory mutations".
Whether "site" here denotes a residue position, a cluster or a pocket was not resolvable from
the retrieved text; that ambiguity is recorded rather than resolved. Either way, applied
consistently, the functional criterion **expands** the positive class far beyond one
modulator-defined pocket per protein. The same paper reports that "computational methods do not
successfully predict the allosteric pockets in Src".

**(c) Pharma reviewer.** They will endorse this clause more strongly than any other — pharma
does not call a pocket allosteric because it is far from the active site; it calls it
allosteric when a compound bound there changes function with a measured potency and a
structure–activity relationship. But they will raise the bar: one inactivating mutation is not
evidence of allostery, it is evidence of importance. They want non-competitive or cooperative
pharmacology, ideally with the reciprocity IUPHAR XC calls the ideal case.

**(d) Tag: wrong in the README.** Should read `[IN-DOMAIN + REPOSITORY POLICY]`, matching the
evidence document.

### (iii) Site-apo — tagged `[BORROWED + REPOSITORY POLICY]`

**(a) Majority: contested, and the balance has shifted.** Site-relative: AHoJ, AHoJ-DB,
CryptoBench (by inheritance), PocketMiner, Clark's site clause. Global: Wankowicz 2022
(`doi:10.7554/eLife.74114`) and now **CryptoBank 2026** at 6 million alignments
(`doi:10.1126/sciadv.ady6364`). Absent entirely from most of the allostery branch, which
predicts from ligand-stripped holo. The README's "That reading is the majority one in the
field" was defensible at freeze and is now too strong without qualification.

**(b) Contradiction: yes, and it is the sharpest one in this audit.** Under CryptoBank's apo
filter ("entries with no nonpolymer entities") **none of the repo's eight frozen apo
structures is apo** — the repo has already measured this: all eight carry heteroatoms, `4OBE`
and `4LDJ` both carry GDP·Mg. Under PocketMiner's and Clark's site rules, both KRAS arms fail
because GDP·Mg contacts 5 of the 21 KRAS labels; the repo's "scoreable portion" qualifier is
what rescues them, and the repo already flags this as a **relaxation**, not a narrowing.
That disclosure is correct and should be kept exactly as it is.

**(c) Pharma reviewer.** They will not care about the nomenclature and will care about two
things the nomenclature does not answer. Was the pocket open in the coordinates you started
from — because "ligand-free at the site" does not imply "pocket present at the site", which
PocketMiner states outright ("some proteins in the CryptoSite set had additional apo structures
in which the pocket was open"). And: why one crystal structure at all? An SBDD group would
start from an ensemble. AstraZeneca's own published method does exactly that (§4).

**(d) Tag: correct.** `[BORROWED]` for the site-relative reading (AHoJ/PocketMiner),
`[REPOSITORY POLICY]` for the scoreable-portion relaxation. This is the best-tagged clause in
the set.

### (iv) Identity ≥90% — tagged `[IN-DOMAIN]`

**(a) Majority: yes for the practice; the repo's threshold is the loosest published.** ESSA 90%,
PocketMiner 100%, Clark 100% then 95%, Wankowicz exact ±5 terminal residues, CryptoBank 95%
clusters, CryptoBench a shared UniProt accession. The repo's arms are 97.6-100% in fact, which
the README already states — so the floor is not the operative number and no arm depends on it.

**(b) Contradiction: none.** No source argues for a looser bar. CryptoBench's UniProt grouping
is looser in a different direction (it pools point mutants), which is a scope difference, not a
contradiction.

**(c) Pharma reviewer.** They will say percent identity is the wrong instrument. What breaks a
pair is a **construct** difference: a truncation boundary near the site, a surface-entropy or
thermostabilising mutation, a fusion partner, a tag. LiveCoMS says this explicitly ("Often
structural studies use shorter constructs… mutations might have been introduced… Such
deviations should be kept to a minimum", `doi:10.33011/livecoms.4.1.1497`). The repo enumerates
differences and pins `sequence_agreement.identity`, which is the right shape; what it should
add is the **modelled construct boundary** per member, since a 100%-identical pair can still
differ by 40 residues of ordered N-terminus that change an elastic network.

**(d) Tag: correct**, but it rests on a single source (ESSA). Label it as the field's only
published pairing threshold — which the evidence doc already does and the README compresses.

### (v) Assembly — tagged `[IN-DOMAIN]`

**(a) Majority: the field is split, not agreed.** For: Amor et al. exclude on "a mismatch
between the oligomeric state of the active and inactive structures"; AlloBench downloads "the
biological assembly structures"; CASBench refines "taking into account the quaternary structure".
Against: **PocketMiner requires a monomeric biological unit** and discards everything else;
AHoJ-DB reports that "about 24% of the binding sites occur at the interface of two or more
chains" and treats those as first-class; CryptoBench supports multi-chain pockets.

**(b) Contradiction: yes — PocketMiner's monomer requirement is the direct opposite policy.**
It excludes precisely the assemblies clause (v) requires.

**(c) Pharma reviewer.** Two questions. Is the deposited assembly the physiologically relevant
one, checked against solution behaviour (SEC-MALS, AUC, native MS), or is it the crystallographic
one? And for this repo specifically: **the cardiac myosin arm's mechanism is an assembly
property.** The SRX/DRX equilibrium involves an interacting-heads motif; a single head cannot
carry it. A reviewer will ask whether the modelled assembly can express the mechanism the arm's
`allosteric_evidence` cites. This is not a defect in the clause — it is the clause doing its job
and pointing at an arm.

**(d) Tag: correct.** Both halves are the field's, as the 2026-08-21 correction established.
The clause should nevertheless record that it takes a side in a live disagreement.

### (vi) Second site — tagged `[REPOSITORY POLICY]`

**(a) Majority: no rule exists, so the tag is right.** The field splits four ways: KeyAlloSite
requires both ligands; AlloReverse requires the orthosteric ligand bound; Ohm and Wu fall back
to residues; PASSer, AlloPred and DeepAllo are silent.

**(b) Contradiction: none, but there is a new data point.** AstraZeneca's method operates on
"ensembles of protein structures **with orthosteric ligands**" (`doi:10.1039/d2sc06272k`)
`[VERIFIED-FULLTEXT]`. Industry's default is orthosteric-occupied. The repo's arms vary, which
the clause permits and records — that is the correct call, but the report should note that the
occupied case is the industrial default and the unoccupied case is the harder one.

**(c) Pharma reviewer.** Orthosteric occupancy is not bookkeeping; it selects the conformational
state (DFG-in/out, αC-in/out, R/T, nucleotide state), and a prediction from an empty active site
is a different question from a prediction from an occupied one. They will also raise
**dualsteric and bitopic ligands**, where the two sites are not separable: ASD2023 curates 456
dualsteric modulators, and IUPHAR XC explicitly allows bitopic engagement with competitive
kinetics. A benchmark whose second-site rule assumes separability should say so.

**(d) Tag: correct.**

### (vii) Non-circularity — tagged `[BORROWED + REPOSITORY POLICY]`

**(a) Majority: no.** Only AlloPred states the rule, and it states it about pocket membership
inside its own perturbation procedure: "Active site residues were not counted as being in any
pocket for this alteration of k, in order to avoid direct perturbation of the site at which the
effect was measured." The repo already notes this scope difference and handles it honestly.

**(b) Contradiction: none directly, but the clause is insufficient.** Beltran et al. measure
"an exponential decay of mutational effects on activity away from the active site" with decay
rate **k = −0.063 ± 0.008 Å⁻¹**, i.e. a 50% reduction over **7.45 Å**
(`doi:10.1126/sciadv.aea2726`) `[VERIFIED-FULLTEXT]`. Functional coupling to the active site is
a smooth, steep function of distance. Removing the source residues from candidacy removes the
degenerate case; it does not remove the confound. The control that does is the matched-patch
null, and clause (vii) should point at it.

**(c) Pharma reviewer.** They will say the clause is obviously right and obviously not enough,
and will ask what the distance-matched baseline scored. This is the single question most likely
to sink a top-5 hit list.

**(d) Tag: wrong.** `[BORROWED]` is defined in the evidence document as marking a point
"addressed by an adjacent field". AlloPred is an allosteric-site predictor — in-domain. What is
borrowed is not the field but the **scope**: a procedural rule inside one method, repurposed as
an admission clause. Recommend `[IN-DOMAIN (procedural, rescoped) + REPOSITORY POLICY]` with the
existing footnote retained.

### (viii) State disclosure — tagged `[REPOSITORY POLICY]`

**(a) Majority: no source requires a state difference in either direction, and that is still
true.** No 2025-26 source changes it. The principled reason the repo gives — dynamic allostery
exists — stands and is reinforced: Nussinov R, Regev C, Jang H, Trends Pharmacol Sci 2026,
`doi:10.1016/j.tips.2026.01.006`, PMC13006995 `[VERIFIED-FULLTEXT]`, states flatly "Allosteric
drugs are based on ensembles. Without ensembles, there would be no allosteric drugs."

**(b) Contradiction: none. New support: two sources.** CAPASP's General-vs-Unbound gap (§1.1),
and Riedlová et al. J Chem Theory Comput 2026, `doi:10.1021/acs.jctc.6c00427`, PMC13217555
`[VERIFIED-FULLTEXT]`: "structure-based methods including P2Rank showed a noticeable decline in
prediction performance on apo structures, underscoring the reliance of current structure-based
ML tools on conformational patterns that may be altered by ligand-induced conformational
changes." Disclosure has moved from courtesy to comparability requirement.

**(c) Pharma reviewer.** They will want the state named in their vocabulary, which the repo
does. They will additionally ask what **fraction of the solution ensemble** that state
represents, and whether the crystal form traps a non-physiological one — a question a single
deposited structure cannot answer, and which the repo should concede rather than model.

**(d) Tag: correct** for the disclosure requirement. The **evidence that state matters** is now
in-domain and should be cited as such (ESSA 10/14 → 7/14; CAPASP; Riedlová), rather than resting
on the borrowed CryptoBench 2 Å floor alone.

---

## 3. The two gaps the repo names

### 3.1 What fraction of allosteric sites are cryptic — still `[NOT ESTABLISHED]`

Searched this session: Europe PMC phrase and boolean searches over `"allosteric sites are
cryptic"`, `"crypticity" AND "allosteric site"`, `"cryptic" AND "allosteric" AND "ASBench"`,
`"cryptic" AND "allosteric" AND "CryptoSite" AND "ASD"`; full texts of CryptoBank, the
Zhang & Bowman 2026 review, Vajda 2018, Riedlová 2026 and the Acta Pharm Sin B 2026 druggable-site
review. **No source reports the converse fraction.** The repo's claim survives the re-audit.

What the search did establish, as bounds and proxies:

| Quantity                                                 | Value                                                                                                   | Source                                                                                                                                                   |
| -------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Cryptic sites that are allosteric (forward direction)    | "**Eight** of the sites shown in Table 1 are allosteric"                                                | Vajda S, Beglov D, Wakefield AE, Egbert M, Whitty A. Curr Opin Chem Biol 2018;44:1-8. `doi:10.1016/j.cbpa.2018.05.003`, PMC6088748 `[VERIFIED-FULLTEXT]` |
| Base rate of crypticity across proteins                  | "cryptic sites… accounting for **18.4%** of all identity clusters" (95% identity)                       | CryptoBank `doi:10.1126/sciadv.ady6364` `[VERIFIED-FULLTEXT]`                                                                                            |
| Allosteric sites invisible to a pocket detector in apo   | PARS discarded **33 of 91** (36%); STINGAllo "approximately **18%**… lie outside surface invaginations" | `doi:10.1186/1471-2105-13-273`; `doi:10.1016/j.csbj.2024.10.036`                                                                                         |
| Apo penalty, measured in-domain                          | ESSA **10/14** holo-stripped vs **7/14** apo; APOP **11/14** apo                                        | `doi:10.1016/j.csbj.2020.06.020`; `doi:10.1093/bioinformatics/btad275`                                                                                   |
| Local motion at the allosteric site on modulator binding | **92.6%** backbone, **5.9%** sidechain over 1688 pairs (threshold unpublished)                          | ASD v3.0 `doi:10.1093/nar/gkv902`                                                                                                                        |
| Apo-vs-holo evaluation gap                               | CAPASP-General > CAPASP-Unbound for all five tools                                                      | `doi:10.1007/s10822-026-00831-4` `[VERIFIED-ABSTRACT]`                                                                                                   |

**Discrepancy to resolve.** The repo states "**8 of 19** cryptic sites are allosteric". The
retrieved full text gives "Eight of the sites shown in Table 1 are allosteric", and the
extraction reported Table 1 as containing **20** proteins. The row count could not be verified
independently in this session. The denominator must be re-checked against Table 1 before the
number is used in `docs/report/`.

**The important finding is that this is not a literature question any more.** Both inputs are
public: ASD/AlloBench give allosteric sites with apo/holo pairs, AHoJ-DB gives PDB-wide apo
mappings, and CryptoBench's 2 Å pocket-lining RMSD rule and CryptoBank's crypticity classifier
are both published operationalisations. The fraction is **computable in this repo**, under
`groundtruth/`, in a bounded amount of work. Continuing to cite its absence is weaker than
computing it — and computing it would be a genuine contribution, because the number is one the
field wants and has not produced.

### 3.2 A minimum-distance convention — `PARTIALLY CLOSED`. The repo's claim needs correcting

**Kincore states one.** Modi V, Dunbrack RL. _Kincore: a web resource for structural
classification of protein kinases and their inhibitors._ Nucleic Acids Res 2022;50(D1):D654-D664.
`doi:10.1093/nar/gkab920`, PMC8728253, OA `[VERIFIED-FULLTEXT]`:

> **Allosteric (Type IV):** "Any small molecule in the asymmetric unit whose **minimum distances
> from the hinge region and C-helix-Glu(+4) residues are both >6.5 Å**." — 220 unique ligands.

> **Type 3:** "**minimum distance from the hinge >6 Å** and at least three contacts in the back
> pocket." — 109 unique ligands.

Back pocket residues are enumerated (166-193, 196-204, 205-207, 273-275, in the paper's common
numbering); contact threshold ≤4.0 Å; 7,177 human kinase chains surveyed.

Riedlová et al. 2026 adopt exactly this as their allosteric label definition
(`doi:10.1021/acs.jctc.6c00427`) `[VERIFIED-FULLTEXT]`, which makes it the operative convention
in the most recent kinase allosteric-site benchmark.

Four qualifications, so the correction is not overstated:

1. It is **kinase-specific**, not a general definition of an allosteric site.
2. It measures **ligand to named landmark** (hinge, αC-Glu+4), not **site to site**. It is a
   classification rule for inhibitors, not an admission rule for pairs.
3. It is **geometric only** — it makes no functional-evidence demand, so it is precisely the
   kind of rule clause (ii) is written to refuse. Adopting it wholesale would contradict
   clause (ii).
4. The repo's literal sentence ("in any source we have **read**") is not falsified, because
   Kincore was not read. The **implication** that no such convention exists is falsified.

**Related, and not a site-separation rule:** PASSer's sanity check "Those proteins were removed
if the closest pocket to the modulator is **>10 Å**" (`doi:10.1093/nar/gkad303`) is a
label-integrity filter, not a definition. And the only quantitative statement about the
allosteric–orthosteric distance relationship remains CASBench's "in **30%** of cases, the
catalytic and allosteric sites either overlap or share a common border"
(`doi:10.32607/20758251-2019-11-1-74-80`), now joined by Beltran's decay constant
(k = −0.063 Å⁻¹, 50% per 7.45 Å).

---

## 4. The industry frame

**What a pharma SBDD group means, operationally, when it calls a pocket allosteric.** Four
conditions, applied together. None is a distance.

1. **A ligandable, non-orthosteric pocket** — scored, not merely detected. The scoring
   instruments are named and quantitative: FTMap hot-spot strength, where "a binding site is
   potentially druggable if it harbors a binding energy hot spot that is strong enough to
   comprise **at least 16 FTMap probe clusters**" (Vajda et al. 2018,
   `doi:10.1016/j.cbpa.2018.05.003`) `[VERIFIED-FULLTEXT]`; SiteMap's Dscore (Halgren TA,
   J Chem Inf Model 2009;49(2):377-389, `doi:10.1021/ci800324m`); fpocket druggability
   (Schmidtke P, Barril X, J Med Chem 2010;53(15):5858-5867, `doi:10.1021/jm100574m`);
   FTMap itself (Kozakov D et al., Nat Protoc 2015;10(5):733-755, `doi:10.1038/nprot.2015.043`).
   The kinase-specific census is Kinase Atlas — Yueh C, Rettenmaier J, Xia B, Hall DR,
   Alekseenko A, Porter KA, Barkovich K, Keseru G, Whitty A, Wells JA, Vajda S, Kozakov D.
   J Med Chem 2019;62(14):6512-6524, `doi:10.1021/acs.jmedchem.9b00089`, PMC7019049
   `[VERIFIED-ABSTRACT]`: "a systematic collection of binding hot spots located at [ten] sites
   in **4910 structures of 376 distinct kinases**".
2. **Pharmacology that is not orthosteric-competitive** — or, where it is (bitopic), an
   explained reason. This is the working content of "allosteric" in a project team.
3. **A co-structure with the compound in the site**, confirming the site is where the
   pharmacology comes from.
4. **A tractable SAR** — the pocket must support chemistry. A site with validated allostery
   and no ligandable volume is a publication, not a program.

**Evidence that this is what industry does, from industry.**

- **AstraZeneca.** La Sala G, Pfleger C, Käck H, Wissler L, Nevin P, Böhm K, Janet JP, Schimpl M,
  Stubbs CJ, De Vivo M, Tyrchan C, Hogner A, Gohlke H, Frolov AI. _Combining structural and
  coevolution information to unveil allosteric sites._ Chem Sci 2023;14(25):7057-7067.
  `doi:10.1039/d2sc06272k`, PMC10306073, OA `[VERIFIED-FULLTEXT]`. Three parameters, all
  computed, none of them distance: a **druggability score** ("pockets being likely druggable if
  the DS is between 0.5 and 1"), a **coevolution coverage score** from statistical coupling
  analysis ("the percentage of coevolving amino acids within pockets identified during the MD
  simulations"), and a **rigidity-theory free-energy measure of dynamic allostery** ("an
  ensemble- and rigidity theory-based free-energy perturbation approach… ΔG_{i,CNA}"). Input is
  "MD simulations… performed using the **apo state** of the protein to detect new pockets", run
  on ensembles that carry the orthosteric ligand. Success criterion: "the model successfully
  ranked all known allosteric pockets in the **top three** positions", on five proteins
  (LFA-1, p38-α, GR, MAT2A, BCKDK), with two novel sites confirmed by X-ray and SPR.
- **Novartis.** Wylie AA, Schoepfer J, Jahnke W, et al. _The allosteric inhibitor ABL001 enables
  dual targeting of BCR-ABL1._ Nature 2017;543(7647):733-737, `doi:10.1038/nature21702`
  `[VERIFIED-ABSTRACT]`. This is the source of the repo's own BCR-ABL1 label. "Allosteric" there
  is established by myristoyl-pocket occupancy plus non-competition with ATP-site drugs — clause
  (ii)'s standard, met by pharmacology.
- **Relay Therapeutics.** Varkaris A, Pazolli E, Gunaydin H, et al. Cancer Discov
  2024;14(2):240-257, `doi:10.1158/2159-8290.CD-23-0944`, PMC10850943 `[VERIFIED-ABSTRACT]`.
  RLY-2608's allosteric site was found by a **DNA-encoded library screen using an
  orthosteric-blocking compound** — that is, industry finds allosteric sites by
  competition-blocked experimental screening, not by structure-based site prediction.
- **Roche / Nested Therapeutics / Mount Sinai.** Rudolph J, Hoeflich KP, Dar AC. _Contemporary
  design of small-molecule kinase modulators: orthosteric, allosteric and induced-proximity
  strategies._ Nat Rev Drug Discov 2026;25:595-618, `doi:10.1038/s41573-026-01411-9`,
  PMID 42049946 `[VERIFIED-ABSTRACT]`. The framing is by **modality** — ATP-site inhibitor,
  allosteric modulator, molecular glue, heterobivalent degrader — and by what each solves
  ("selectivity, modulation of scaffolding functions and overcoming drug resistance"), never by
  a geometric criterion.
- **Covalent-allosteric is a recognised class, not an anomaly.** Tao H, Yang B, Farhangian A,
  Xu K, Li T, Zhang ZY, Li J. _Covalent-Allosteric Inhibitors: Do We Get the Best of Both
  Worlds?_ J Med Chem 2025;68(4):4040-4052, `doi:10.1021/acs.jmedchem.4c02760`, PMC12207613
  `[VERIFIED-ABSTRACT]`: CAIs "may achieve the best of both worlds", surveyed across
  phosphatases, kinases and GTPases. **This materially strengthens the repo's decision to keep
  the covalent KRAS/sotorasib arm** against AlloBench's exclusion rule. The exclusion is a
  dataset-hygiene convention, not a statement that covalent modulators are not allosteric.
- **The industry benchmarking norm is prospective.** CACHE (§1.6) is a public-private
  partnership whose ground truth is experimental testing, co-authored by Bayer, Boehringer,
  Novartis, AstraZeneca, Sanofi, Takeda and Merck KGaA.

**Is the repo's definition recognisable to them? Mostly yes; three parts are not.**

Recognisable and welcome: (ii) functional provenance, (vi) recording second-site occupancy,
(viii) naming the conformational state, and the ligand-density check, which exceeds field
standard.

Not recognisable:

- **Apo-only input.** No SBDD group predicts an allosteric site from one apo crystal structure.
  They use ensembles (AstraZeneca: MD; Nussinov 2026: "Allosteric drugs are based on ensembles").
  The repo's apo-only rule is a **challenge constraint (C1) and a scientific-integrity rule**,
  not industry practice, and the report must present it that way rather than as best practice.
- **A residue list as the deliverable.** Industry wants a pocket with a volume, a shape and a
  druggability score. The repo's top-5 residue hit list is what `CHALLENGE.md` mandates, so this
  is a limitation to state in `docs/report/`, not a benchmark defect — but a reviewer from that
  world will say it in the first five minutes.
- **No ligandability filter anywhere in the definition.** All eight clauses concern whether the
  pair is valid; none concerns whether the site is druggable. In pharma the two questions are
  never separated.

---

## 5. Axes the repo is not using, ranked by how much a reviewer would expect them

The repo characterises pairs by crypticity, proximity, resolution, packing, B-factor and
alternate conformations. Ranked below by expectation, with feasibility under C1 (apo only) and
C2 (no MD trajectories) noted, because an axis the constraints forbid is not a gap.

**1. Evolutionary conservation and coevolution — highest expectation, and the most serious
omission.** ASD v2.0 itself reports that "allosteric sites evolved under **lower
sequence-conservation** pressure compared with the evolutionarily conserved orthosteric sites"
(`doi:10.1093/nar/gkt1247`). Riedlová 2026 restates it: allosteric sites are "conformationally
plastic, **evolutionarily permissive**, and often lineage-specific". AstraZeneca uses statistical
coupling analysis as one of three parameters (`doi:10.1039/d2sc06272k`). KeyAlloSite uses
evolutionary coupling strength (`doi:10.7554/eLife.81850`). AlloFusion uses PSSM profiles
(`doi:10.1021/acs.jcim.5c01033`). **Any reviewer will ask whether the repo's high-ranking
residues are simply conserved residues.** Conservation is computable from sequence alone, needs
no holo structure and no MD, and is therefore admissible under C1 and C2. It belongs beside the
three existing apo-only confounders in `structure/properties`.

**2. Pocket detectability and druggability score.** The field's single most-reported failure
mode is that the detector cannot see the site (PARS 36% discarded; APOP and ESSA name specific
failures; STINGAllo 18%). The repo runs a pocket detector for decoys, so the machinery exists;
what is missing is a **per-candidate druggability number** — fpocket druggability
(`doi:10.1021/jm100574m`), or an FTMap-style hot-spot count (`doi:10.1038/nprot.2015.043`,
threshold ≥16 probe clusters). Cheap, apo-only, and it is the axis the industry reviewer
weights most.

**3. Local energetic frustration.** New, in-domain, and physics-based:
"allosteric pockets occupy predominantly **neutrally frustrated zones** associated with
conformational plasticity and reduced evolutionary constraint" (Riedlová 2026,
`doi:10.1021/acs.jctc.6c00427`); the same claim is the organising idea of Gatlin W et al.
Protein Sci 2026;35(8):e70714 (`doi:10.1002/pro.70714`) and one of the two novel features in
AlloEF (`doi:10.1021/acs.jpcb.6c00242`). Computable from a single structure with a
frustratometer — no MD, no holo. This is the strongest **new** axis available to the repo.

**4. Deep mutational scanning / measured allosteric coupling maps.** Beltran 2026
(`doi:10.1126/sciadv.aea2726`) and Faure AJ, Domingo J, Schmiedel JM, Hidalgo-Carcedo C, Diss G,
Lehner B. Nature 2022;604(7904):175-183 (`doi:10.1038/s41586-022-04586-4`) `[VERIFIED-ABSTRACT]`
are the emerging gold standard for allosteric labels — dense, functional, per-residue, and
independent of any structure pair. The repo cannot generate such data, but it should (a) cite
it as the reason its negative class is uncertain and (b) check whether any arm has a published
DMS map that could serve as an external validation set.

**5. Thermodynamic coupling magnitude (Qax).** The repo knows Fenton's energy cycle and states
correctly that Qax is not obtainable from its inputs. What is missing is smaller and doable:
where the literature reports a **measured coupling magnitude or fold-shift** for an arm's
modulator, record it, so arms can be ordered by how strong the allostery actually is. A weak
coupling and a strong one are not equally scoreable.

**6. Solution-dynamics readouts: HDX-MS and NMR chemical-shift covariance.** These are the
experimental analogues of exactly what the repo computes — per-residue propagation from a
perturbation. CHESCA: Selvaratnam R, Chowdhury S, VanSchouwen B, Melacini G. PNAS
2011;108(15):6133-6138, `doi:10.1073/pnas.1017311108`, PMC3076865 `[VERIFIED-ABSTRACT]`. HDX on
an energy cycle: Beckett D. Methods Mol Biol 2012, `doi:10.1007/978-1-61779-334-9_14`
`[VERIFIED-ABSTRACT]`; with the Fenton-lab control on D₂O itself, Prasannan CB, Artigues A,
Fenton AW. Anal Bioanal Chem 2011, `doi:10.1007/s00216-011-5133-x`, PMC3142283
`[VERIFIED-ABSTRACT]`. A reviewer will ask whether the predicted propagation path agrees with
any measured one. Even a single arm with published HDX or CHESCA data would be a strong
qualitative validation.

**7. Conformational entropy / dynamic allostery.** Frederick KK, Marlow MS, Valentine KG,
Wand AJ. Nature 2007;448(7151):325-329, `doi:10.1038/nature05959`, PMC4156320
`[VERIFIED-ABSTRACT]`. The repo already argues correctly that requiring a conformational change
would exclude dynamic allostery. What it does not do is record any entropy-adjacent descriptor,
so the argument is asserted rather than instrumented.

**8. Burial and hydrophobicity.** APOP ranks on "local hydrophobic densities"; STINGAllo uses 54
nanoenvironment descriptors including "sponge effect… hydrophobic interactions, electrostatic
potentials, eccentricity". If relative SASA or burial is not already one of the repo's three
apo-only confounders, it should be — it is the cheapest possible confound and correlates with
both degree and score in any contact-network method.

**9. Normalised B-factors and ensemble re-refinement.** Wankowicz 2025: "High B-factors do not
necessarily guarantee high flexibility in solution. To use them reliably, it's best to
**normalize** B-factors" (`doi:10.1371/journal.pcbi.1013094`). The repo carries deposited
B-factors. Normalising them (against the mean Cα B, as Wankowicz 2022 does for ligands) is a
one-line change that converts a biased quantity into a usable one. qFit/PDB-REDO re-refinement
is the fuller version and is optional.

**10. Interface and oligomerisation status of the site.** 24% of biologically relevant binding
sites are at chain interfaces (AHoJ-DB, `doi:10.1016/j.jmb.2024.168545`), and ASD2023 curates
allosteric PPI modulators as a category of their own. Relevant to the myosin and c-Myc arms.

**Below the line, and deliberately so:** MD-derived flexibility, cosolvent/mixed-solvent hot
spots, Markov-state pocket-opening probabilities. All are standard in the cryptic-pocket field
(Zhang S, Bowman GR, Curr Opin Struct Biol 2026;96:103215, `doi:10.1016/j.sbi.2025.103215`;
Zhang S, Miller JJ, Bowman GR, J Chem Theory Comput 2026;22(8):3839-3850,
`doi:10.1021/acs.jctc.6c00135`), and all are forbidden by C2 as inputs. The report should name
them as the axes it is constitutionally unable to use, and say why — otherwise a reviewer will
read the omission as an oversight rather than a constraint.

---

## What must change in the repo

Ordered by severity. Each is a bounded edit, not a research programme.

1. **Fix the clause (ii) tag mismatch.** `../primary/README.md` §1 tags it `[IN-DOMAIN]`;
   `../evidence/allosteric-pair-definition.md` tags it `[IN-DOMAIN + REPOSITORY POLICY]`. Adopt
   the evidence document's tag in both places. The reason is in §2(ii): the principle is the
   field's, the enforcement is entirely ours.

2. **Re-tag clause (vii).** `[BORROWED]` contradicts the repo's own glossary, since AlloPred is
   an allosteric-site predictor and therefore in-domain. Replace with
   `[IN-DOMAIN (procedural, rescoped) + REPOSITORY POLICY]` and keep the existing footnote about
   AlloPred's rule being about pocket membership inside its own procedure.

3. **Correct the "no minimum distance" section in `../primary/README.md` §1.** Add Kincore's
   Type IV rule verbatim — "minimum distances from the hinge region and C-helix-Glu(+4) residues
   are both >6.5 Å" (`doi:10.1093/nar/gkab920`) — with the four qualifications in §3.2, and
   state whether the BCR-ABL1 arms' effector satisfies it. Do **not** adopt it as a clause: it is
   geometric-only and would contradict clause (ii).

4. **Qualify the site-apo "majority" claim.** `../primary/README.md` §1 currently says site-apo
   "is the majority one in the field". Add CryptoBank (`doi:10.1126/sciadv.ady6364`) as a second
   global-apo source at 6-million-alignment scale, and narrow the claim to "the majority among
   resources that annotate apo/holo per binding site". The scoreable-portion relaxation
   disclosure needs no change — it is already correctly framed as a weakening.

5. **Replace "not reported anywhere in the literature" with a computation.** The converse
   crypticity fraction is confirmed absent (§3.1), but it is now computable from public inputs
   (ASD/AlloBench sites × AHoJ-DB apo mappings × CryptoBench's 2 Å rule or CryptoBank's
   classifier). Either compute it under `groundtruth/` or state explicitly that it is computable
   and out of scope. Also **re-check the Vajda denominator** — the repo says 8 of 19; the
   retrieved text says "Eight of the sites shown in Table 1", with Table 1 reported as 20 rows.

6. **Add CAPASP to `../evidence/`** as the first purpose-built apo-vs-holo split in
   allosteric-site evaluation (`doi:10.1007/s10822-026-00831-4`), tagged `[VERIFIED-ABSTRACT]`
   with the unretrievable-methods caveat, and cite it under clause (viii) so the apo insistence
   rests on in-domain evidence rather than the borrowed CryptoBench floor alone.

7. **Add Wankowicz 2025 to `../evidence/curation-standard.md`** (`doi:10.1371/journal.pcbi.1013094`),
   noting it is **single-authored** — any repo or report text saying "Wankowicz & Fraser 2025" is
   wrong. Act on its B-factor rule: report normalised B-factors alongside deposited ones.

8. **Add conservation/coevolution as a fourth apo-only confounder** in `structure/properties`,
   and local frustration as a fifth diagnostic. Both are apo-only and MD-free, so both clear C1
   and C2. §5 items 1 and 3 give the citations. This is the single change most likely to survive
   a hostile review, because "your hits are just the conserved residues" is the first objection
   a reviewer will raise and the repo currently cannot answer it.

9. **Add a scope sentence to clause (i):** effectors are small molecules identified by a PDB
   chemical component ID; protein and peptide effectors are out of scope. IUPHAR XC §III — the
   authority clause (ii) rests on — explicitly admits a protein second ligand, so the repo
   narrows its own authority and should say so.

10. **Record the negative-class limitation in `../evaluation/README.md`.** Beltran 2026
    (`doi:10.1126/sciadv.aea2726`) reports dozens of functionally allosteric surfaces in one
    kinase and that "computational methods do not successfully predict the allosteric pockets in
    Src". A one-site-per-arm benchmark therefore has an unknown false-negative rate in its
    negatives. This does not require a protocol change — the protocol is frozen — but it must be
    disclosed as a limitation, and it is an argument for reporting precision-oriented metrics
    over recall-oriented ones.

11. **In `docs/report/`, state the industry gap explicitly** (§4): apo-only single-structure
    input is a challenge constraint and an integrity rule, not SBDD best practice; the deliverable
    is residues where industry wants a scored pocket; and no clause of the definition tests
    ligandability. Say it before a reviewer does.

12. **Add a "literature last searched" date** to `../evidence/README.md`. The evidence base is
    dated 2026-08-20 to 2026-08-25; this audit re-searched on 2026-09-02 and found four
    materially new sources. Without a date, the next reader cannot tell whether a gap is real or
    merely stale.

---

## Bibliography

Every entry was retrieved this session unless marked otherwise. `[VERIFIED-FULLTEXT]` means the
body was returned through Europe PMC `fullTextXML` or the publisher page; `[VERIFIED-ABSTRACT]`
means abstract or indexed record only. All quoted strings passed through a fetch-and-summarise
tool and are one step removed from the raw source.

**New since mid-2025**

- Ai Y, Li H, Huang X, Liu S. A systematic evaluation of protein allosteric site prediction tools with independent datasets. _J Comput Aided Mol Des_ 2026. `doi:10.1007/s10822-026-00831-4`. PMID 42126486. `[VERIFIED-ABSTRACT]`
- Febrer Martinez P, Fröhlking T, Borsatto A, Gervasio FL. CryptoBank: A resource for the identification and prediction of cryptic sites in proteins. _Sci Adv_ 2026;12(17):eady6364. `doi:10.1126/sciadv.ady6364`. PMC13267282. `[VERIFIED-FULLTEXT]`
- Beltran A, Naqvi MM, Faure AJ, Lehner B. The allosteric landscape of the Src kinase. _Sci Adv_ 2026;12(7):eaea2726. `doi:10.1126/sciadv.aea2726`. PMC12893324. `[VERIFIED-FULLTEXT]`
- Wankowicz SA. Ten rules for a structural bioinformatic analysis. _PLoS Comput Biol_ 2025;21(10):e1013094. `doi:10.1371/journal.pcbi.1013094`. PMC12578330. `[VERIFIED-FULLTEXT]`
- Nussinov R, Regev C, Jang H. Leveraging conformational ensembles in allosteric drug discovery. _Trends Pharmacol Sci_ 2026. `doi:10.1016/j.tips.2026.01.006`. PMC13006995. `[VERIFIED-FULLTEXT]`
- Zhang S, Bowman GR. Decrypting cryptic pockets with physics-based simulations and artificial intelligence. _Curr Opin Struct Biol_ 2026;96:103215. `doi:10.1016/j.sbi.2025.103215`. PMC12959236. `[VERIFIED-FULLTEXT]`
- Zhang S, Miller JJ, Bowman GR. How Well Can AI and Physics-Based Simulations Predict the Probability a Cryptic Pocket Is Open? _J Chem Theory Comput_ 2026;22(8):3839-3850. `doi:10.1021/acs.jctc.6c00135`. `[VERIFIED-ABSTRACT]`
- Zhang J, Sun X, Wu Z, Su J, Zhang X, Li C. AlloEF: An Ensemble Model for Protein Allosteric Site Identification Based on Transfer Entropy and Energetic Frustration. _J Phys Chem B_ 2026;130(19):4970-4981. `doi:10.1021/acs.jpcb.6c00242`. `[VERIFIED-ABSTRACT]`
- Huang J, Guo D, Liu Y, Wang Y, Lv M. Allofusion: Allosteric Site Prediction Based on Language Models and Multi-Feature Fusion. _J Chem Inf Model_ 2025;65(16):8858-8870. `doi:10.1021/acs.jcim.5c01033`. `[VERIFIED-ABSTRACT]`
- Gatlin W, Ludwick M, Turano L, Foley B, Riedlová K, Škrhák V, Novotný M, Hoksza D, Verkhivker GM. Decoding the allosteric grammar of protein kinases. _Protein Sci_ 2026;35(8):e70714. `doi:10.1002/pro.70714`. `[VERIFIED-ABSTRACT]`
- Khokhar M, Keskin O, Gursoy A. DeepAlloWeb. _J Mol Biol_ 2026. `doi:10.1016/j.jmb.2026.169863`. `[VERIFIED-ABSTRACT]`
- Yuce M, Kurkcuoglu O. Computationally Efficient Network Models Successfully Predict Allosteric Sites of SARS-CoV-2 Main Protease. _Proteins_ 2026. `doi:10.1002/prot.70122`. `[VERIFIED-ABSTRACT]`
- Chen EA, Zhang Y. Can Deep Learning Blind Docking Methods be Used to Predict Allosteric Compounds? _J Chem Inf Model_ 2025. `doi:10.1021/acs.jcim.5c00331`. PMC12004537. `[VERIFIED-ABSTRACT]`
- Lin A, Zhang Z, Jiang A, et al. Computational approaches to druggable site identification. _Acta Pharm Sin B_ 2026. `doi:10.1016/j.apsb.2025.10.032`. PMC12827903. `[VERIFIED-FULLTEXT]` — searched and found to contain **no** allosteric-site definition, no distance criterion and no crypticity statistic.

**Conventions and definitions**

- Modi V, Dunbrack RL. Kincore: a web resource for structural classification of protein kinases and their inhibitors. _Nucleic Acids Res_ 2022;50(D1):D654-D664. `doi:10.1093/nar/gkab920`. PMC8728253. `[VERIFIED-FULLTEXT]`
- Modi V, Dunbrack RL. Defining a new nomenclature for the structures of active and inactive kinases. _PNAS_ 2019;116(14):6818-6827. `doi:10.1073/pnas.1814279116`. PMC6452665. `[VERIFIED-ABSTRACT]`
- Riedlová K, Škrhák V, Gatlin WG, et al. Predicting and Decoding Allosteric Binding Sites Using Protein Language Models and Structure-Based Machine Learning. _J Chem Theory Comput_ 2026. `doi:10.1021/acs.jctc.6c00427`. PMC13217555. `[VERIFIED-FULLTEXT]`
- Vajda S, Beglov D, Wakefield AE, Egbert M, Whitty A. Cryptic binding sites on proteins: definition, detection, and druggability. _Curr Opin Chem Biol_ 2018;44:1-8. `doi:10.1016/j.cbpa.2018.05.003`. PMC6088748. `[VERIFIED-FULLTEXT]`
- Christopoulos A, et al. IUPHAR XC. _Pharmacol Rev_ 2014;66(4):918-947. `doi:10.1124/pr.114.008862`. PMC11060431. `[UNVERIFIED here — quoted from the repo's own prior retrieval]`
- IUPAC Gold Book entry 14107. `[NOT-RETRIEVABLE]` — no new route attempted this session.

**Industry**

- La Sala G, Pfleger C, Käck H, Wissler L, Nevin P, Böhm K, Janet JP, Schimpl M, Stubbs CJ, De Vivo M, Tyrchan C, Hogner A, Gohlke H, Frolov AI. Combining structural and coevolution information to unveil allosteric sites. _Chem Sci_ 2023;14(25):7057-7067. `doi:10.1039/d2sc06272k`. PMC10306073. `[VERIFIED-FULLTEXT]`
- Rudolph J, Hoeflich KP, Dar AC. Contemporary design of small-molecule kinase modulators. _Nat Rev Drug Discov_ 2026;25:595-618. `doi:10.1038/s41573-026-01411-9`. PMID 42049946. `[VERIFIED-ABSTRACT]`
- Varkaris A, Pazolli E, Gunaydin H, et al. Discovery and Clinical Proof-of-Concept of RLY-2608. _Cancer Discov_ 2024;14(2):240-257. `doi:10.1158/2159-8290.CD-23-0944`. PMC10850943. `[VERIFIED-ABSTRACT]`
- Wylie AA, Schoepfer J, Jahnke W, et al. The allosteric inhibitor ABL001 enables dual targeting of BCR-ABL1. _Nature_ 2017;543(7647):733-737. `doi:10.1038/nature21702`. `[VERIFIED-ABSTRACT]`
- Green EM, Wakimoto H, Anderson RL, et al. A small-molecule inhibitor of sarcomere contractility suppresses hypertrophic cardiomyopathy in mice. _Science_ 2016;351(6273):617-621. `doi:10.1126/science.aad3456`. PMC4784435. `[VERIFIED-ABSTRACT]`
- Tao H, Yang B, Farhangian A, Xu K, Li T, Zhang ZY, Li J. Covalent-Allosteric Inhibitors: Do We Get the Best of Both Worlds? _J Med Chem_ 2025;68(4):4040-4052. `doi:10.1021/acs.jmedchem.4c02760`. PMC12207613. `[VERIFIED-ABSTRACT]`
- Yueh C, Rettenmaier J, Xia B, Hall DR, Alekseenko A, Porter KA, Barkovich K, Keseru G, Whitty A, Wells JA, Vajda S, Kozakov D. Kinase Atlas: Druggability Analysis of Potential Allosteric Sites in Kinases. _J Med Chem_ 2019;62(14):6512-6524. `doi:10.1021/acs.jmedchem.9b00089`. PMC7019049. `[VERIFIED-ABSTRACT]`
- Ackloo S, Al-Awar R, Amaro RE, et al. CACHE: a public-private partnership benchmarking initiative. _Nat Rev Chem_ 2022;6(4):287-295. `doi:10.1038/s41570-022-00363-z`. PMC9246350. `[VERIFIED-FULLTEXT]`
- Herasymenko O, Silva M, Correy GJ, et al. CACHE Challenge #3: Targeting the Nsp3 Macrodomain of SARS-CoV-2. _J Chem Inf Model_ 2026. `doi:10.1021/acs.jcim.5c02441`. PMC12892310. `[VERIFIED-ABSTRACT]`
- Wang X, Mettu A, Herasymenko O, et al. Targeting the RNA-Binding Site of SARS-CoV-2 NSP13 by FRASE-bot in CACHE Challenge #2. _J Chem Inf Model_ 2026. `doi:10.1021/acs.jcim.6c00560`. `[VERIFIED-ABSTRACT]`

**Axes**

- Faure AJ, Domingo J, Schmiedel JM, Hidalgo-Carcedo C, Diss G, Lehner B. Mapping the energetic and allosteric landscapes of protein binding domains. _Nature_ 2022;604(7904):175-183. `doi:10.1038/s41586-022-04586-4`. `[VERIFIED-ABSTRACT]`
- Selvaratnam R, Chowdhury S, VanSchouwen B, Melacini G. Mapping allostery through the covariance analysis of NMR chemical shifts. _PNAS_ 2011;108(15):6133-6138. `doi:10.1073/pnas.1017311108`. PMC3076865. `[VERIFIED-ABSTRACT]`
- Beckett D. Hydrogen-deuterium exchange study of an allosteric energy cycle. _Methods Mol Biol_ 2012. `doi:10.1007/978-1-61779-334-9_14`. `[VERIFIED-ABSTRACT]`
- Prasannan CB, Artigues A, Fenton AW. Monitoring allostery in D2O. _Anal Bioanal Chem_ 2011. `doi:10.1007/s00216-011-5133-x`. PMC3142283. `[VERIFIED-ABSTRACT]`
- Frederick KK, Marlow MS, Valentine KG, Wand AJ. Conformational entropy in molecular recognition by proteins. _Nature_ 2007;448(7151):325-329. `doi:10.1038/nature05959`. PMC4156320. `[VERIFIED-ABSTRACT]`
- Schmidtke P, Barril X. Understanding and predicting druggability. _J Med Chem_ 2010;53(15):5858-5867. `doi:10.1021/jm100574m`. `[VERIFIED-ABSTRACT]`
- Halgren TA. Identifying and characterizing binding sites and assessing druggability. _J Chem Inf Model_ 2009;49(2):377-389. `doi:10.1021/ci800324m`. `[VERIFIED-ABSTRACT]`
- Kozakov D, Grove LE, Hall DR, Bohnuud T, Mottarella SE, Luo L, Xia B, Beglov D, Vajda S. The FTMap family of web servers. _Nat Protoc_ 2015;10(5):733-755. `doi:10.1038/nprot.2015.043`. PMC4762777. `[VERIFIED-ABSTRACT]`

**Already in the repo's evidence base, cited here without re-verification**

ASD v1 `doi:10.1093/nar/gkq1022` · ASD v2.0 `doi:10.1093/nar/gkt1247` · ASD v3.0
`doi:10.1093/nar/gkv902` · ASD2023 `doi:10.1093/nar/gkad915` · ASBench
`doi:10.1093/bioinformatics/btv169` · CASBench `doi:10.32607/20758251-2019-11-1-74-80` ·
AlloBench `doi:10.1021/acsomega.5c01263` · CryptoBench `doi:10.1093/bioinformatics/btae745` ·
CryptoSite `doi:10.1016/j.jmb.2016.01.029` · PocketMiner `doi:10.1038/s41467-023-36699-3` ·
AHoJ `doi:10.1093/bioinformatics/btac701` · AHoJ-DB `doi:10.1016/j.jmb.2024.168545` ·
Wankowicz 2022 `doi:10.7554/eLife.74114` · Clark 2019 `doi:10.1371/journal.pcbi.1006705` ·
Binding MOAD `doi:10.1093/nar/gkm911` · LiveCoMS `doi:10.33011/livecoms.4.1.1497` ·
ESSA `doi:10.1016/j.csbj.2020.06.020` · APOP `doi:10.1093/bioinformatics/btad275` ·
PARS `doi:10.1186/1471-2105-13-273` · AlloPred `doi:10.1186/s12859-015-0771-1` ·
PASSer `doi:10.1093/nar/gkad303` · KeyAlloSite `doi:10.7554/eLife.81850` ·
STINGAllo `doi:10.1016/j.csbj.2024.10.036` · Amor 2016 `doi:10.1038/ncomms12477` ·
McCullagh … Fenton 2024 `doi:10.1016/j.jbc.2024.105672`.

---

## What this audit could not settle

1. **CAPASP's construction protocol.** Paywalled, outside Europe PMC. What "apo" means in
   CAPASP-Unbound is `[NOT ESTABLISHED]`. _Closes by: institutional access to the Springer PDF._
2. **CryptoBank's apo filter, precisely.** The retrieved Methods give both an entry-level filter
   ("no nonpolymer entities") and a ligand exclusion list (ions, <60 Da, solvents). Which is
   applied first, and therefore whether an ion-bearing entry can be apo, is `[NOT ESTABLISHED]`.
   _Closes by: reading the raw Methods XML at PMC13267282._
3. **The Vajda 2018 denominator** — 19 or 20 rows in Table 1. _Closes by: reading Table 1 at
   PMC6088748 directly._
4. **Whether "42 major allosteric sites" in Beltran 2026 counts residue positions, clusters or
   pockets.** _Closes by: reading the Results and Fig. 4 of PMC12893324._
5. **Kinase Atlas full text.** PMC returned a CAPTCHA and Europe PMC `fullTextXML` 404s;
   only the indexed record was read. _Closes by: institutional access to J Med Chem._
6. **Whether any IUPHAR/NC-IUPHAR nomenclature revision after XC 2014 exists.** Searched, none
   found. Recorded as a negative search result, not as proof of absence.
