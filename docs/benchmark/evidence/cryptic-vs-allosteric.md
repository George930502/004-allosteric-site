# Are "cryptic site" and "allosteric site" the same concept?

Definitional literature review, 2026-08-20. Retrieval route: Europe PMC REST
(`/search?query=...&resultType=core&format=json`, `/{PMCID}/fullTextXML`).

Every claim is tagged:

- `[VERIFIED-FULLTEXT]` — sentence pulled from the article's open-access full text.
- `[VERIFIED-ABSTRACT]` — sentence pulled from the Europe PMC `core` abstract record.
- `[UNVERIFIED]` — could not reach primary text; recorded as a lead, not as evidence.

---

## 0. Bottom line

**No. They are orthogonal axes that overlap heavily in practice.**

- **"Allosteric" is a claim about _function_:** binding at site B changes what happens at
  site A. It is established by a functional experiment, not by looking at a structure.
- **"Cryptic" is a claim about _structure_:** the pocket is absent in apo and present in
  holo. It is established by comparing two structures, and says nothing about function.

A site can be either, both, or neither. Both classes are populated by named,
well-characterised examples, and the one paper that classifies a curated cryptic-site
set by function finds that **fewer than half of validated cryptic sites are allosteric**
(8/19; Vajda 2018, §3.3).

The decisive sentence in the whole review is from Cruz et al. 2022, who state the
conditional relationship explicitly [VERIFIED-FULLTEXT]:

> "These cryptic sites can serve as valuable drug targets **if** they coincide with key
> functional sites, **or if** they are allosterically coupled to distant functional sites"

Crypticity is a property of the pocket; allostery is a property that must be
_demonstrated separately_.

**Consequence for this benchmark:** a ground truth built from apo→holo pocket contacts
is a **cryptic-site** ground truth, not an **allosteric-site** ground truth. They are
not interchangeable and the report must not use the words as synonyms. See §7.

---

## 1. The formal definition of "allosteric site"

### 1.1 Historical

| Source                                                                                                   | Status                                                                                                                |
| -------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| Monod, Wyman & Changeux, _J Mol Biol_ 12:88–118 (1965), PMID 14343300, doi 10.1016/S0022-2836(65)80285-6 | `[UNVERIFIED]` — Europe PMC holds no abstract for this record; full text not reachable. Cited at metadata level only. |
| Koshland, Némethy & Filmer, _Biochemistry_ 5:365–385 (1966), PMID 5938952, doi 10.1021/bi00865a047       | `[UNVERIFIED]` — same.                                                                                                |
| Monod, Changeux & Jacob, _J Mol Biol_ 6:306–329 (1963), PMID 13936070, doi 10.1016/S0022-2836(63)80091-1 | `[UNVERIFIED]` — same.                                                                                                |

Do **not** quote MWC or KNF verbatim in the report without obtaining the PDFs. The
secondary quotation below is what is actually verified.

**Etymology, quoted secondarily** by Liu & Nussinov, _PLoS Comput Biol_ 12:e1004966
(2016), PMCID PMC4890769 `[VERIFIED-FULLTEXT]`:

> "The term 'allosteric' first appeared in 1961, when Jacques Monod and Francois Jacob
> used 'allosteric inhibition'" to describe a mechanism in which "the inhibitor is not a
> steric analogue of the substrate."

Note what the original coinage is about: the inhibitor is _chemically_ unlike the
substrate. Not "the inhibitor binds far away."

**Changeux & Edelstein**, _Science_ 308:1424–1428 (2005), PMID 15933191,
doi 10.1126/science.1108595 `[VERIFIED-ABSTRACT]`:

> "Forty years ago, a simple model of allosteric mechanisms (**indirect interactions
> between distinct sites**), used initially to explain feedback-inhibited enzymes, was
> presented by Monod, Wyman, and Changeux."

Criterion in the parenthesis: _indirect interaction_ + _distinct sites_. Not distance.

### 1.2 Modern conceptual definitions

**Motlagh, Wrabl, Li & Hilser**, _Nature_ 508:331–339 (2014), PMID 24740064,
doi 10.1038/nature13001 `[VERIFIED-ABSTRACT]` (full text is not open access):

> "Allostery is the process by which biological macromolecules (mostly proteins)
> transmit the effect of binding at one site to another, **often distal**, functional
> site, allowing for regulation of activity."

"**often** distal" — distance is a frequent correlate, explicitly not a requirement.
Same abstract, on the ensemble reframing:

> "Recent experimental observations demonstrating that allostery can be facilitated by
> dynamic and intrinsically disordered proteins have resulted in a new paradigm for
> understanding allosteric mechanisms, which focuses on the conformational ensemble and
> the statistical nature of the interactions responsible for the transmission of
> information."

**Nussinov & Tsai**, _Cell_ 153:293–305 (2013), PMID 23582321,
doi 10.1016/j.cell.2013.03.034 `[VERIFIED-ABSTRACT]` (paywalled, no PMCID; full text
unreachable):

> "Allostery is largely associated with conformational and functional transitions in
> individual proteins. This concept can be extended to consider the impact of
> conformational perturbations on cellular function and disease states. Here, we clarify
> the concept of allostery and how it controls physiological activities."

The abstract does not contain a one-sentence definition. **Do not cite this paper for a
verbatim definition of "allosteric site" — I could not obtain one.** Use Hilser or ASD
instead.

**Gunasekaran, Ma & Nussinov**, _Proteins_ 57:433–443 (2004), PMID 15382234,
doi 10.1002/prot.20232 `[VERIFIED-ABSTRACT]` — the maximal position:

> "Allostery involves coupling of conformational changes between two widely separated
> binding sites. […] Here we argue that **all (nonfibrous) proteins are potentially
> allosteric.** Allostery is a consequence of re-distributions of protein conformational
> ensembles. […] In principle, practically any potential drug binding to the protein
> surface can alter the conformational redistribution."

If every protein is potentially allosteric, "allosteric site" cannot be a structural
category. It has to be earned by a functional measurement — which is exactly Fenton's
point below.

**Fenton**, _Trends Biochem Sci_ 33:420–425 (2008), PMID 18706817,
doi 10.1016/j.tibs.2008.05.009 `[VERIFIED-ABSTRACT]` — the strict functional definition,
and the single most useful sentence for a benchmark designer:

> "In my opinion, experimental progress is hampered by a commonly used but misleading
> definition of allostery as protein structural changes that are elicited by the binding
> of a single ligand. **Allostery is more strictly defined in functional terms as a
> comparison of how one ligand binds in the absence, versus the presence, of a second
> ligand.** Therefore, as each of the two binding events involves two protein complexes,
> a study of allostery must consider **four complexes and not just two**. Such a
> comparison can distinguish allosteric from non-allosteric protein changes, the
> importance of which is frequently overlooked."

An apo→holo structure pair is **two** complexes. By Fenton's criterion it is
_constitutively insufficient_ to establish allostery. This is the formal reason our
label-generation procedure produces cryptic-site labels rather than allosteric-site
labels.

### 1.3 The operational definition — the Allosteric Database (ASD)

ASD is the field's reference curation, and the challenge statement names it (§10 ref
[25]). Its wording is stable across four releases:

**ASD v1** — Huang et al., _NAR_ 39:D663–D669 (2011), PMCID PMC3013650
`[VERIFIED-FULLTEXT]`:

> "regulation of protein function, structure and/or flexibility induced by the binding of
> a ligand at a site **topographically distinct** from the orthosteric site"

**ASD v2.0** — Huang et al., _NAR_ 42:D510–D516 (2014), PMCID PMC3965017
`[VERIFIED-FULLTEXT]`: "an allosteric site topographically distinct from the orthosteric
site".

**ASD v3.0** — Shen et al., _NAR_ 44:D527–D535 (2016), PMCID PMC4702938,
doi 10.1093/nar/gkv902 `[VERIFIED-ABSTRACT]`:

> "Allosteric regulation, the most direct and efficient way of regulating protein
> function, is induced by the binding of a ligand at one site that is **topographically
> distinct from an orthosteric site**."

and `[VERIFIED-FULLTEXT]`:

> "Allostery, an intrinsic property of a protein, is referred to as the regulation of
> activity at one site (also known as an orthosteric site) in a protein by a
> topographically and spatially distant site; the latter is designated as an allosteric
> site."

**ASD 2019** — Liu et al., _NAR_ 48:D394–D401 (2020), PMCID PMC7145546
`[VERIFIED-FULLTEXT]`: "Two topographically and spatially distinct types of binding
sites: allosteric and orthosteric sites".

### 1.4 ASD's inclusion criteria — what evidence is actually required

This is the answer to "what would it take to call a site experimentally validated."
ASD v1, Materials and Methods, PMCID PMC3013650 `[VERIFIED-FULLTEXT]`:

> "With **at least three cases of experimental evidence** in crystal structure complex or
> biochemistry (**inactive mutation of allosteric residue, cooperativity of kinetic
> effect from two ligands and uncompetitive-binding assay with chromatography**, etc.),
> 336 proteins supporting their functional change elicited by modulator binding at a site
> that was topographically distinct from the orthosteric functional site, were verified
> as allosteric proteins"

Three named accepted experiment classes: **site mutagenesis**, **two-ligand kinetic
cooperativity**, **uncompetitive/non-competitive binding**. A crystal structure alone is
not on the list as sufficient.

ASD v2.0, "Allosteric Sites" subsection `[VERIFIED-FULLTEXT]` — the geometric rule, which
is a _site-residue extraction_ rule, not a separation threshold:

> "The residues constituting an allosteric site are automatically extracted from a
> complex structure by **6 Å** around allosteric modulator […] and manually inspected"

ASD v2.0, "Allosteric Pathways" `[VERIFIED-FULLTEXT]`: pathways were collected where
identified "by experimental (e.g. **site-directed mutagenesis, X-ray crystallography and
NMR**) and theoretical […] approaches".

### 1.5 Is there a minimum distance convention? — **No.**

Searched ASD v1/v2/v3/2019 and CASBench full texts and found no minimum separation
threshold anywhere. What exists:

| Quantity                       | Value                | Source                            | What it actually is                    |
| ------------------------------ | -------------------- | --------------------------------- | -------------------------------------- |
| Site-residue extraction radius | 6 Å around modulator | ASD v2.0 `[VERIFIED-FULLTEXT]`    | defines _which residues_ are in a site |
| Site-residue extraction radius | 5 Å around ligand    | CASBench `[VERIFIED-FULLTEXT]`    | same                                   |
| Accepted allosteric separation | ~9 Å                 | Meller 2023 `[VERIFIED-FULLTEXT]` | a _precedent_, not a rule              |

**Meller et al.**, _eLife_ 12:e83602 (2023), PMCID PMC9995120 `[VERIFIED-FULLTEXT]`:

> "Blebbistatin inhibits myosin ATPase by preventing the release of phosphate from the
> active site and interfering with actin binding. However, experimental structures of
> blebbistatin bound to myosin reveal that it binds in a cleft **approximately 9 Å from
> the active site, consistent with its designation as an allosteric effector**."

So 9 Å is enough for the field. There is no published lower bound. **The honest
statement for the report: distance is a correlate, not a criterion; no minimum Å
convention exists in the primary literature or in ASD.**

### 1.6 The decisive counter-case to a distance criterion

**Weng, Faure, Escobedo & Lehner**, _Nature_ 626:643–652 (2024), PMCID PMC10866706,
doi 10.1038/s41586-023-06954-0 — a 26,000-mutation deep mutational scan of KRAS,
i.e. the largest purely functional allosteric map that exists. `[VERIFIED-FULLTEXT]`:

> "Allosteric mutations defined in this manner are highly enriched in **the physiological
> allosteric site of KRAS, the nucleotide-binding pocket**"

They call the **nucleotide-binding pocket itself** an allosteric site. It is allosteric
_with respect to RAF1 binding_, because that is the functional output being measured. The
same pocket is orthosteric with respect to GTP hydrolysis.

**"Allosteric" is a two-place relation — site B is allosteric _for function A_.** A
benchmark that asks "is this residue allosteric?" without naming the coupled function is
asking an ill-posed question. Their operational definition `[VERIFIED-FULLTEXT]`:

> "Defining major allosteric sites as residues where the mean absolute change in binding
> free energy upon mutation is equal to or greater than that in binding interface
> residues identifies a total of 18 sites."

Purely energetic. No distance term.

---

## 2. The formal definition of "cryptic site"

Unlike allostery, this one is stable, structural, and near-unanimous.

**CryptoSite** — Cimermancic et al., _J Mol Biol_ 428:709–719 (2016), PMID 26854760,
doi 10.1016/j.jmb.2016.01.029 `[VERIFIED-ABSTRACT]` (full text is _not_ open access;
`fullTextXML` returns 404):

> "Many proteins have small-molecule binding pockets that are not easily detectable in
> the ligand-free structures. These cryptic sites require a conformational change to
> become apparent; **a cryptic site can therefore be defined as a site that forms a
> pocket in a holo structure, but not in the apo structure.**"

**Vajda, Beglov, Wakefield, Egbert & Whitty**, _Curr Opin Chem Biol_ 44:1–8 (2018),
PMCID PMC6088748, doi 10.1016/j.cbpa.2018.05.003, section "When is a binding site
cryptic?" `[VERIFIED-FULLTEXT]`:

> "A cryptic site can therefore be defined as a site that forms a pocket in a
> ligand-bound structure, but not in the unbound protein structure."

> "Cryptic sites were defined as sites with an average pocket score of **less than 0.1 in
> the unbound form** of the protein and **greater than 0.4 in the bound form**."

> "An alternative, more stringent definition is for a pocket to be considered cryptic only
> if it is **absent in all, or nearly all, unbound structures** of the protein, such that
> it cannot be reliably identified in the absence of a bound ligand."

> "To assure that the analysis captured only sites that are genuinely cryptic even when
> all their unbound structures are considered, the proteins were subjected to a further
> test to ensure that **all available unbound structures would clash with the ligand**,
> and thus the pocket is fully formed only upon ligand binding."

That last one is the strictest published operational test and is exactly what this
repo's KRAS audit already performs (ligand transplant + clash count).

**Kuzmanic, Bowman, Juarez-Jimenez, Michel & Gervasio**, _Acc Chem Res_ 53:654–661
(2020), PMID 32134250, doi 10.1021/acs.accounts.9b00613 `[VERIFIED-ABSTRACT]`:

> "Cryptic binding sites are **not visible in protein targets crystallized without a
> ligand and only become visible crystallographically upon binding events.**"

**PocketMiner** — Meller et al., _Nat Commun_ 14:1177 (2023), PMCID PMC9977097,
doi 10.1038/s41467-023-36699-3 `[VERIFIED-FULLTEXT]`:

> "Cryptic pockets are cavities that open and close as a protein fluctuates in solution
> but are typically closed and therefore hidden in experimental structures."

Their MD label rule `[VERIFIED-FULLTEXT]`:

> "A residue was considered a positive example if at any point in simulation the nearby
> pocket volume determined by the LIGSITE algorithm increased by **more than 40 Å³**
> relative to its assigned pocket volume in the starting structure."

> "Pockets were considered open if the pocket volume of a simulated structure reached or
> exceeded the holo crystal structure pocket volume."

**CryptoBench** — Škrhák, Novotný, Feidakis, Krivák & Hoksza, _Bioinformatics_ 41:btae745
(2024), PMCID PMC11725321, doi 10.1093/bioinformatics/btae745 `[VERIFIED-FULLTEXT]`:

> "The CBS refers to a region in a protein that can bind a ligand and undergoes a
> significant structural change between its holo (ligand-bound) and apo (unbound) forms."

> "A significant change is defined as a difference of **at least 2 Å RMSD** between the
> binding residues in the apo and holo forms."

Their full filter stack `[VERIFIED-FULLTEXT]`: pocket RMSD ≥ 2 Å; resolution ≤ 2.5 Å;
global TM-score ≥ 0.5; binding-site-centre distance ≤ 4 Å post-alignment; radius of
gyration change ≤ 20 %; ≥ 50 residues observed overlap; ligand ≥ 5 atoms; 40 % sequence
clustering, 10 % for the train/test split.

**The word "allosteric" does not appear anywhere in the CryptoBench paper**
`[VERIFIED-FULLTEXT]`. The most recent, most explicitly benchmark-focused cryptic-site
resource in the field never invokes allostery. That is itself strong evidence the
concepts are separable.

**CrypToth** — Koseki et al., _J Chem Inf Model_ 65:5153–5166 (2025), PMCID PMC12152933,
doi 10.1021/acs.jcim.4c02111 `[VERIFIED-ABSTRACT]`:

> "Some functional proteins undergo conformational changes to expose hidden binding sites
> when a binding molecule approaches their surface. Such binding sites are called cryptic
> sites and are important targets for drug discovery."

**Beglov et al.**, _PNAS_ 115:E3416–E3425 (2018), PMID 29581267,
doi 10.1073/pnas.1711490115 `[VERIFIED-ABSTRACT]` — a structural-origins caveat that
matters for scoring:

> "close to **50% of the proteins studied here have unbound structures that could
> accommodate the ligand without clashes**"

> "An interesting observation is that cryptic sites formed solely by the movement of side
> chains, or of backbone segments with fewer than five residues, result only in **low
> affinity binding sites** with limited use for drug discovery."

**Summary: crypticity is defined structurally, always. Every definition surveyed is a
statement about apo vs holo geometry. None mentions function.**

---

## 3. The relationship

### 3.1 The explicit conditional

**Cruz et al.**, _Nat Commun_ 13:2269 (2022), PMCID PMC9046395,
doi 10.1038/s41467-022-29927-9, Introduction `[VERIFIED-FULLTEXT]` (retrieved twice
independently; the fetcher's per-quote length cap prevented a single contiguous pull, the
two fragments are reproduced as returned):

> "Cryptic pockets are absent in available experimental structures but form in a subset of
> excited states…"

> "…can serve as valuable drug targets **if** they coincide with key functional sites,
> **or if** they are allosterically coupled to distant functional sites"

Two disjoint success modes. Coinciding with a functional site is the _orthosteric_ mode.
Allosteric coupling is the other. The paper's own structure — find pocket, _then_ test
coupling by thiol labelling, mutation, and binding assay — treats allostery as something
demonstrated after the fact.

### 3.2 Quantified overlap — the one hard number in the literature

**Vajda et al. 2018**, Table 1 `[VERIFIED-FULLTEXT]`. This is the CryptoSite validated
set, classified by site type. Legend: "Allo – allosteric, ortho – orthosteric (primary
binding), PPI – protein–protein interaction inhibitor."

| Protein                             | Apo    | Holo   | Ligand | Affinity     | Type     |
| ----------------------------------- | ------ | ------ | ------ | ------------ | -------- |
| mRNA-decapping enzyme DcpS          | 3BL9 B | 3BL7 A | DD1    | IC₅₀ 7.6 nM  | **Allo** |
| Hepatitis C virus polymerase        | 3CJ0 A | 2BRL A | POO    | IC₅₀ 18 nM   | **Allo** |
| Hepatitis C virus polymerase        | 3CJ0 A | 3FQK B | 79Z    | IC₅₀ 81 nM   | **Allo** |
| c-MET tyrosine kinase domain        | 1R1W A | 3F82 A | 353    | IC₅₀ 4.6 nM  | **Allo** |
| TetR-like transcriptional regulator | 2WGB A | 2V57 A | PRL    | K_D 79 nM    | **Allo** |
| Angiopoietin-1 receptor (TIE2)      | 1FVR A | 2OO8 X | RAJ    | IC₅₀ 1 nM    | **Allo** |
| Nicotinic acetylcholine receptor    | 3PEO G | 2BYS J | LOB    | K_D 0.3 nM   | **Allo** |
| Biotin carboxylase                  | 1BNC B | 2V5A A | LZL    | IC₅₀ 150 nM  | **Allo** |
| Staphylococcal nuclease             | 1TQO A | 1TR5 A | THP    | K_i ~100 nM  | ortho    |
| DXP reductoisomerase                | 1K5H C | 2EGH B | FOM    | K_i 38 nM    | ortho    |
| Glutamate racemase                  | 2OHG A | 2OHV A | NHL    | K_i 16 nM    | ortho    |
| SARS-CoV main protease              | 1UK2 A | 2GZ7 A | D3F    | IC₅₀ 300 nM  | ortho    |
| Serotonin N-acetyltransferase       | 1B6B A | 1KUV A | CA5    | K_i 22 nM    | ortho    |
| Coagulation factor VII zymogen      | 1JBU H | 1WUN H | 5B     | IC₅₀ 62 nM   | ortho    |
| NPC2 lysosomal protein              | 1NEP A | 2HKA C | C3S    | K_D 30–50 nM | ortho    |
| Hsp90                               | 2QFO B | 2WI7 A | 2KL    | IC₅₀ 58 nM   | ortho    |
| Integrin alpha-L                    | 3F74 C | 3BQM C | BQM    | IC₅₀ 2 nM    | ortho    |
| Interleukin-2                       | 1Z92 A | 1PY2 A | FRH    | IC₅₀ 60 nM   | PPI      |
| Bcl-xL                              | 3FDL A | 2YXJ A | N3C    | K_i 0.5 nM   | PPI      |

Accompanying text `[VERIFIED-FULLTEXT]`:

> "**Eight of the sites shown in Table 1 are allosteric.** Since molecular mechanisms of
> allosteric communication are rooted in the dynamic nature of proteins, allosteric
> modulators frequently bind at flexible regions without pre-formed pockets."

> "**Table 1 also shows nine orthosteric (primary binding) sites. Five of these are enzyme
> active sites.**"

> "Cryptic sites located away from the main functional site of a protein, but which can
> modulate the activity of the protein allosterically, are also potentially useful."

**8 / 19 = 42 % of validated high-affinity cryptic sites are allosteric.
9 / 19 = 47 % are orthosteric. 2 / 19 = 11 % are PPI sites.**

This is the number to cite. Fewer than half.

### 3.3 The complementary statistic — allosteric sites that sit next to the active site

**CASBench** — Zlobin, Suplatov, Kopylov & Švedas, _Acta Naturae_ 11:74–80 (2019),
PMCID PMC6475866, doi 10.32607/20758251-2019-11-1-74-80. 91 enzymes with both catalytic
(from Catalytic Site Atlas) and allosteric (from ASD) sites annotated
`[VERIFIED-FULLTEXT]`:

> "In all the CASBench annotations, different sites are topologically independent from
> each other (i.e., they are represented by separate cavities in the enzyme structure).
> **In 30% of cases, the catalytic and allosteric sites either overlap or share a common
> border; in 70% of entries, both sites reside at a considerable distance from each other
> and do not overlap within the structure.**"

**In the field's own curated allosteric-site benchmark, 30 % of allosteric sites overlap
or border the catalytic site.** Any "min distance to active site" filter applied to a
ground-truth label set would silently discard roughly a third of real allosteric sites.

### 3.4 Cryptic but NOT allosteric — named examples

All from Vajda Table 1, §3.2, with apo/holo PDB pairs `[VERIFIED-FULLTEXT]`. Nine
orthosteric cryptic sites, five of them enzyme active sites:

1. **Staphylococcal nuclease** 1TQO → 1TR5 (thymidine-3′,5′-diphosphate) — active site
2. **DXP reductoisomerase** 1K5H → 2EGH (fosmidomycin) — active site
3. **Glutamate racemase** 2OHG → 2OHV — active site
4. **SARS-CoV main protease** 1UK2 → 2GZ7 — active site
5. **Serotonin N-acetyltransferase** 1B6B → 1KUV — active site
6. **Hsp90** 2QFO → 2WI7 — ATP site
7. **Coagulation factor VIIa** 1JBU → 1WUN
8. **NPC2** 1NEP → 2HKA
9. **Integrin alpha-L** 3F74 → 3BQM

Also relevant to KRAS specifically: **Lanman et al.**, _J Med Chem_ 63:52–65 (2020),
PMID 31820981, doi 10.1021/acs.jmedchem.9b01180 `[VERIFIED-ABSTRACT]` report exploiting
"a **cryptic pocket (H95/Y96/Q99)** we identified in KRAS^G12C" — a _second_, distinct
cryptic sub-pocket adjacent to the S-IIP, exploited by AMG 510 for potency. This is a
cryptic surface feature whose function is drug-binding, with no independent allosteric
claim attached to it.

### 3.5 Allosteric but NOT cryptic — named examples

**(a) The ABL1 myristoyl pocket** — the strongest and most directly relevant example,
because it is one of our three targets.

Paladini, Maier, Habazettl, Hertel, Sonti & Grzesiek, _eLife_ 13:e92324 (2024),
PMCID PMC11001296, doi 10.7554/eLife.92324 `[VERIFIED-FULLTEXT]`:

> "The C-terminal αI-helix (residues 504–522, 1b numbering used throughout) adopts a
> straight conformation […] in crystal structures of the isolated Abl kinase domain with
> an **empty myristoyl binding pocket (PDB 1M52)**"

The pocket is observable, unoccupied, in a deposited apo-for-this-site structure. It is
not cryptic. It is unambiguously allosteric (§4.2). Independently corroborated by this
repo's own ligand-transplant audit: asciminib transplants into 1M52, 2G1T, 2G2H and 4WA9
with ≤ 4 of 31 atoms clashing (`docs/targets.md`).

**(b) The M2 muscarinic receptor extracellular vestibule.** Kruse et al., _Nature_
504:101–106 (2013), PMID 24256733, PMCID PMC4020789, doi 10.1038/nature12735
`[UNVERIFIED — abstract-level gloss only, obtain the PDF before quoting]`: the positive
allosteric modulator LY2119620 is reported to recognise "a largely **pre-formed** binding
site in the extracellular vestibule of the iperoxo-bound receptor, inducing a slight
contraction of this outer binding pocket."

**(c) All eight ASD-derived allosteric sites in CASBench that overlap or border the
catalytic site (§3.3)** are by construction not cryptic in the strict sense — they are
part of an already-open catalytic cavity.

### 3.6 Does any source treat the terms as synonyms?

Not as a formal equivalence. What exists is a **compound term**, "cryptic allosteric
site," which by its construction presupposes the two are separate modifiers:

- **Bowman & Geissler**, _PNAS_ 109:11681–11686 (2012), PMID 22753506, PMCID PMC3406870,
  doi 10.1073/pnas.1209309109 `[VERIFIED-ABSTRACT]`: "Cryptic allosteric sites—transient
  pockets in a folded protein that are invisible to conventional experiments but **can**
  alter enzymatic activity via allosteric communication with the active site". The "can"
  is doing real work.
- **Ni et al.**, _Chem Sci_ 12:464–476 (2021), PMCID PMC8178949, doi 10.1039/D0SC05131D
  `[VERIFIED-FULLTEXT]`: "The cryptic allosteric sites are exclusively detected in
  specific intermediate states within protein conformational ensemble", and separately,
  "Allostery involves fine-tuning the functions of conserved orthosteric sites by
  topologically distinct allosteric sites."
- **Chen et al.**, _Cancer Cell_ 39:225–239 (2021), PMID 33357454,
  doi 10.1016/j.ccell.2020.11.013 `[VERIFIED-ABSTRACT]`: arsenic trioxide binds "a cryptic
  allosteric site" in the p53 DNA-binding domain.

**Loose usage does exist** in review-level prose that slides between "cryptic pocket" and
"allosteric pocket" — e.g. PocketMiner's only allostery-adjacent sentence
`[VERIFIED-FULLTEXT]`: "while molecules that target an orthosteric site are obligate
inhibitors, molecules that target a cryptic pocket can modulate protein function via
inhibition or activation." Note this too says _can_, and it is a claim about modulation
mode, not a classification of the pocket. **No primary source asserts the terms are
equivalent.**

### 3.7 The 2×2, populated

|                                  | **Cryptic** (absent in apo)                                                                                                                                            | **Not cryptic** (pre-formed)                                                                                                                      |
| -------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Allosteric**                   | HCV polymerase thumb sites, c-MET, DcpS, biotin carboxylase, nAChR, TIE2 (Vajda Table 1); Ebola VP35 (Cruz 2022); myosin blebbistatin site (Meller 2023)               | **ABL1 myristoyl pocket** (Paladini 2024); M2 receptor vestibule (Kruse 2013); the 30 % of CASBench allosteric sites bordering the catalytic site |
| **Not allosteric** (orthosteric) | SARS-CoV Mpro, staphylococcal nuclease, DXP reductoisomerase, glutamate racemase, serotonin N-acetyltransferase, Hsp90, factor VIIa, NPC2, integrin αL (Vajda Table 1) | ordinary enzyme active sites                                                                                                                      |

Every cell is populated by named, cited examples. **That is the proof they are orthogonal
axes.**

---

## 4. The three targets

### 4.1 KRAS G12C switch-II pocket (S-IIP) — **CRYPTIC = yes. ALLOSTERIC = yes, with a

caveat about the frame of reference.**

**Cryptic.** Ostrem, Peters, Sos, Wells & Shokat, _Nature_ 503:548–551 (2013),
PMID 24256730, doi 10.1038/nature12796 `[VERIFIED-ABSTRACT]` (full text not open access;
`fullTextXML` on PMC4274051 returns 404):

> "Crystallographic studies reveal **the formation of a new pocket that is not apparent in
> previous structures of Ras**, beneath the effector binding switch-II region."

That is the CryptoSite definition restated in the primary paper. Corroborated by this
repo's own transplant test: `MOV` into the 4OBE apo frame leaves 14 of 41 ligand atoms
below 2.5 Å from protein (`docs/targets.md`) — passing Vajda's strictest crypticity test
(§2). Also `[VERIFIED-ABSTRACT]` Janes et al., _Cell_ 172:578–589 (2018), PMID 29373830,
doi 10.1016/j.cell.2018.01.006: "an **inducible** allosteric switch II pocket (S-IIP)" —
"accessibility of the S-IIP is restricted only to the GDP-bound state."

**Allosteric.** Same Ostrem abstract `[VERIFIED-ABSTRACT]`:

> "Efforts to target this oncogene directly have faced difficulties owing to its picomolar
> affinity for GTP/GDP and **the absence of known allosteric regulatory sites**."

> "Binding of these inhibitors to K-Ras(G12C) disrupts both switch-I and switch-II,
> subverting the native nucleotide preference to favour GDP over GTP and impairing binding
> to Raf. Our data provide **structure-based validation of a new allosteric regulatory
> site on Ras** that is targetable in a mutant-specific manner."

Reinforced by Janes 2018's phrase "**allosteric** switch II pocket" and by Weng 2024
`[VERIFIED-FULLTEXT]`:

> "Pocket 2 (also called the switch-II pocket) is located between switch-II and α-helix 3
> and is the binding site of sotorasib and other clinically approved **allosteric
> inhibitors** of KRAS(G12C)."

> "Seventy-one mutations in nine residues that contact sotorasib **allosterically inhibit
> RAF1 binding**."

**The caveat, stated honestly.** The S-IIP abuts the nucleotide site and the covalent
anchor Cys12 is a P-loop residue that contacts the nucleotide phosphates. So the ligand
contact set will contain residues that are, with respect to GTP hydrolysis, orthosteric.
"Allosteric" here means _allosteric with respect to effector (RAF1) binding and to
nucleotide preference_ — which is precisely what Ostrem measured and what Weng validated
genetically. Weng makes the frame-of-reference point unavoidable by calling the
nucleotide pocket itself "the physiological allosteric site of KRAS" (§1.6).

I found **no primary source disputing the allosteric designation**. (A search-tool
summary offered editorial commentary to that effect; it cited no paper and is recorded
here as `[UNVERIFIED — not a source, tool-generated commentary]`. Do not cite it.)

**Verdict: cryptic ✓, allosteric ✓ — the only one of the three that is both.**

### 4.2 ABL1 myristoyl pocket — **CRYPTIC = no. ALLOSTERIC = yes, strongly.**

**Allosteric — the label.** Wylie et al., _Nature_ 543:733–737 (2017), PMID 28329763,
doi 10.1038/nature21702, title and abstract `[VERIFIED-ABSTRACT]`: "**The allosteric
inhibitor ABL001** enables dual targeting of BCR-ABL1"; "In contrast to catalytic-site
ABL1 kinase inhibitors, ABL001 **binds to the myristoyl pocket** of ABL1 and **induces
the formation of an inactive kinase conformation.**"

Schoepfer et al., _J Med Chem_ 61:8120–8135 (2018), PMID 30137981,
doi 10.1021/acs.jmedchem.8b01040, title `[VERIFIED-ABSTRACT]`: "Discovery of Asciminib
(ABL001), **an Allosteric Inhibitor** of the Tyrosine Kinase Activity of BCR-ABL1."

**STAMP** = **S**pecifically **T**argeting the **A**BL **M**yristoyl **P**ocket. Cleanest
verified definitional use: Hughes, White & Yeung, _Haematologica_ (2025), PMID 40568725,
PMCID PMC12485309, doi 10.3324/haematol.2024.286798 `[VERIFIED-ABSTRACT]`: "Asciminib, the
first STAMP (specifically targeting the ABL myristoyl pocket) inhibitor, binds to the
myristoyl pocket of BCR::ABL1."

**Not cryptic.** Paladini 2024 `[VERIFIED-FULLTEXT]`, quoted in §3.5: PDB 1M52 is a
crystal structure of the isolated Abl kinase domain "with an empty myristoyl binding
pocket." The pocket is a _physiological_ ligand site — it is the docking site for c-Abl's
own N-terminal myristoyl group (Nagar et al., _Cell_ 112:859–871 (2003), PMID 12654251,
doi 10.1016/S0092-8674(03)00194-6 `[VERIFIED-ABSTRACT]`: "the N-terminal myristoyl
modification of c-Abl 1b **binds to the kinase domain** and induces conformational changes
that allow the SH2 and SH3 domains to dock onto it"). A site that a native ligand occupies
in the ground state is by definition not "absent in the apo structure."

**Verdict: cryptic ✗, allosteric ✓.** This target therefore tests _nothing_ about
cryptic-pocket prediction. It is a pure allosteric-communication test. That is a feature,
not a bug — but it means the KRAS and ABL1 arms of this benchmark are measuring
**different things**, and the report must say so.

### 4.3 Cardiac myosin mavacamten site — **CRYPTIC = not established (no source calls it

cryptic). ALLOSTERIC = yes.**

**Allosteric.** Rohde, Roopnarine, Thomas & Muretta, _PNAS_ 115:E7486–E7494 (2018),
PMID 30018063, PMCID PMC6094135, doi 10.1073/pnas.1720342115 `[VERIFIED-ABSTRACT]`:
"mavacamten, **an allosteric cardiac myosin inhibitor** and a prospective treatment for
hypertrophic cardiomyopathy."

Somavarapu, Ge, Yengo, Craig & Padrón, _Sci Adv_ (2026), PMID 42054467,
PMCID PMC13127576, doi 10.1126/sciadv.aed6472 `[VERIFIED-FULLTEXT]`:

> "both target the same **allosteric binding pocket**"

and, cross-validating this repo's programmatically derived label set exactly
`[VERIFIED-FULLTEXT]`:

> "Within 4 Å of each ligand, key interacting residues included **N711, R712, I713, L770,
> E774, R721, Y722, T167, D168, Y164, and H666.**"

(Compare `docs/targets.md`, derived independently from the six `XB2` entries: Tyr164,
Thr167, Asp168, His666, Pro710, Asn711, Arg712, Ile713, Glu774, plus Arg721, Tyr722,
Leu770. Identical up to Pro710. This is a genuine independent confirmation.)

Auguin et al., _Nat Commun_ 15:4885 (2024), PMID 38849353,
doi 10.1038/s41467-024-47587-9 `[VERIFIED-ABSTRACT]`: "we reveal by X-ray crystallography
that **both drugs target the same pocket** and stabilize a pre-stroke structural state
[…] All-atom molecular dynamics simulations reveal how these molecules produce distinct
effects **in motor allostery** thus impacting force production in opposite way."

**Cryptic — unresolved, and the literature does not claim it.** A dedicated
`"mavacamten" AND "cryptic"` search returned **no** paper describing the mavacamten site
as a cryptic pocket. Somavarapu 2026 full text contains no "cryptic" and no
pre-existing-vs-induced statement `[VERIFIED-FULLTEXT]`.

Two adjacent facts that make the answer state-dependent rather than simply "no":

- Sirigu et al., _PNAS_ 113:E7448–E7455 (2016), PMID 27815532,
  doi 10.1073/pnas.1609342113 `[VERIFIED-ABSTRACT]`: the smooth-muscle myosin inhibitor
  CK-2018571 "binds to **a novel allosteric pocket that opens up during the 'recovery
  stroke' transition** necessary to reprime the motor." An allosteric myosin pocket that
  exists only in a transition intermediate — i.e. conditionally cryptic.
- Meller 2023 `[VERIFIED-FULLTEXT]` establishes that a _different_ myosin pocket (the
  blebbistatin site, ~9 Å from the active site) is genuinely cryptic: "In blebbistatin-free
  myosin experimental structures, a leucine residue in the U50 linker […] always points
  into the blebbistatin pocket, creating a steric impediment to binding", and all 124
  blebbistatin-free myosin structures in the PDB have a closed pocket.

**Verdict: allosteric ✓ (well cited); cryptic = unknown, must be measured, not asserted.**
Do the transplant test on `9GZ3 → 9GZ2` (the corrected pair in `docs/benchmark/`) and
report the clash count. If it transplants cleanly, this target is the second
"allosteric but not cryptic" arm alongside ABL1, and the benchmark contains exactly one
genuinely cryptic target.

---

## 5. What counts as "experimentally validated allosteric"

### 5.1 The field's accepted evidence classes

From ASD v1's stated verification rule (§1.4) `[VERIFIED-FULLTEXT]` — three cases of
experimental evidence, drawn from:

1. **Inactive mutation of an allosteric residue** (site-directed mutagenesis)
2. **Cooperativity of kinetic effect from two ligands**
3. **Uncompetitive-binding assay**

plus, from ASD v2.0's pathway curation `[VERIFIED-FULLTEXT]`: site-directed mutagenesis,
X-ray crystallography, NMR.

Fenton's stricter formulation (§1.2) `[VERIFIED-ABSTRACT]` — the four-complex
requirement: measure how ligand 1 binds _in the absence_ and _in the presence_ of ligand 2. Anything less "cannot distinguish allosteric from non-allosteric protein changes."

Weng 2024's modern high-throughput equivalent (§1.6) `[VERIFIED-FULLTEXT]`: deep
mutational scanning with inferred free-energy changes, defining allosteric sites as
residues whose mutation shifts binding free energy at a distal interface by at least as
much as interface residues do.

### 5.2 The single most important caveat: binding ≠ modulating

**Paladini et al. 2024** `[VERIFIED-FULLTEXT]`:

> "Importantly, **not all myristoyl pocket binders act as allosteric inhibitors**, but
> only those that also bend the αI-helix"

**Schoepfer et al. 2018** `[VERIFIED-ABSTRACT]`, describing the asciminib campaign:

> "Fragment-based screening using NMR and X-ray yielded ligands for the myristate pocket.
> An NMR-based conformational assay guided the transformation of these **inactive
> ligands** into ABL1 inhibitors."

Novartis found fragments that bound the allosteric pocket and did nothing. Occupancy of an
allosteric site is not allosteric modulation. A structure-derived label set cannot
distinguish the two.

### 5.3 Per target, the specific validating experiment

| Target                             | Experiment establishing allosteric function                                                                                                                                                                                                                                           | Citation                                                                                  | Tag                                           |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | --------------------------------------------- |
| **KRAS G12C S-IIP**                | Inhibitor binding subverts native nucleotide preference (GTP→GDP) and impairs Raf binding — a functional change at sites distal to the drug                                                                                                                                           | Ostrem 2013, _Nature_ 503:548, doi 10.1038/nature12796                                    | `[VERIFIED-ABSTRACT]`                         |
|                                    | Deep mutational scanning: 71 mutations in 9 sotorasib-contacting residues allosterically inhibit RAF1 binding; genetic validation of the pocket as allosterically active                                                                                                              | Weng 2024, _Nature_ 626:643, doi 10.1038/s41586-023-06954-0                               | `[VERIFIED-FULLTEXT]`                         |
|                                    | Trapping mechanism: inhibition requires intact GTPase cycling; drug-bound KRAS^G12C is insusceptible to exchange factors — a functional coupling, not steric occlusion of GTP                                                                                                         | Lito 2016, _Science_ 351:604, doi 10.1126/science.aad6204                                 | `[VERIFIED-ABSTRACT]`                         |
| **ABL1 myristoyl pocket**          | **The cleanest case in the whole review.** "using solution NMR, X-ray crystallography, mutagenesis and hydrogen exchange mass spectrometry, we show that GNF-2 binds to the myristate-binding site of Abl, **leading to changes in the structural dynamics of the ATP-binding site**" | Zhang 2010, _Nature_ 463:501, PMCID PMC2901986, doi 10.1038/nature08675                   | `[VERIFIED-ABSTRACT]`                         |
|                                    | Non-ATP-competitive kinetics: GNF-2 kills Bcr-Abl-transformed cells "while showing **no inhibition of the kinase activity** of full-length or catalytic domain of c-abl… through an allosteric non-ATP competitive mechanism"                                                         | Adrián 2006, _Nat Chem Biol_ 2:95, doi 10.1038/nchembio760                                | `[VERIFIED-ABSTRACT]`                         |
|                                    | Resistance mutations map to the myristate site and are orthogonal to ATP-site mutations — genetic proof the two sites are distinct and both functional                                                                                                                                | Wylie 2017, _Nature_ 543:733; Schoepfer 2018, _J Med Chem_ 61:8120                        | `[VERIFIED-ABSTRACT]`                         |
|                                    | NMR force model: asciminib "strongly reduces Abl's activity by fixating the αI-helix and reducing the force onto the SH2 domain" — a measured mechanical coupling path from pocket to active site                                                                                     | Paladini 2024, _eLife_ 13:e92324                                                          | `[VERIFIED-FULLTEXT]`                         |
| **Cardiac myosin mavacamten site** | Transient biochemical + structural kinetics: mavacamten stabilises an autoinhibited two-headed state, enhances autoinhibition of ATP turnover and of ADP release, slows actin-induced lever-arm rotation — modulation of the ATPase cycle from a non-catalytic site                   | Rohde 2018, _PNAS_ 115:E7486, doi 10.1073/pnas.1720342115                                 | `[VERIFIED-ABSTRACT]`                         |
|                                    | Single-molecule to fibre: mavacamten promotes the super-relaxed state; HCM mutations destabilise it                                                                                                                                                                                   | Anderson 2018, _PNAS_ 115:E8143, doi 10.1073/pnas.1809540115                              | `[VERIFIED-ABSTRACT]`                         |
|                                    | Same-pocket opposite-effect pair (mavacamten vs omecamtiv mecarbil) — the strongest possible demonstration that the effect is transmitted, not steric                                                                                                                                 | Auguin 2024, _Nat Commun_ 15:4885; Somavarapu 2026, _Sci Adv_, doi 10.1126/sciadv.aed6472 | `[VERIFIED-ABSTRACT]` / `[VERIFIED-FULLTEXT]` |

---

## 6. What I could not verify

Recorded so nobody re-runs these dead ends, and so no one quotes them from memory.

| Item                                                                  | Why                                                                                                                                                                                                            |
| --------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| MWC 1965, KNF 1966, Monod-Changeux-Jacob 1963 verbatim definitions    | Europe PMC holds no abstract text for these records; no PMCID; full text not reachable. Metadata only.                                                                                                         |
| Nussinov & Tsai 2013 _Cell_ full text                                 | Paywalled, no PMCID. Abstract does not contain a one-line definition of "allosteric site".                                                                                                                     |
| Motlagh/Hilser 2014 _Nature_ full text                                | `PMC4224315/fullTextXML` → 404 (`isOpenAccess: N`). Abstract only.                                                                                                                                             |
| CryptoSite (Cimermancic 2016) full text                               | **RETRIEVED 2026-08-20.** Europe PMC `PMC4794384/fullTextXML` → 404, but `https://pmc.ncbi.nlm.nih.gov/articles/PMC4794384/` serves the full text. All five criteria in README §1 were read from it.        |
| Ostrem 2013 _Nature_ full text                                        | **RETRIEVED 2026-08-20** via `pmc.ncbi.nlm.nih.gov/articles/PMC4274051/`. Assay detail (mant-dGDP competition, co-IP, SOS exchange) read from it.                                                            |
| Fenton 2008 _TiBS_ full text                                          | `PMC2574622/fullTextXML` → 404. Abstract carries the definition in full.                                                                                                                                       |
| Auguin 2024 _Nat Commun_ full text                                    | **RETRIEVED 2026-08-20** via `PMC11161628/fullTextXML`. This is the source that resolved `Ala767` (an omecamtiv residue, not a mavacamten one) — README §7.                                                  |
| Kruse 2013 "largely pre-formed" quote                                 | Retrieved via a search-result gloss, not from full text. Marked `[UNVERIFIED]`. Get the PDF before citing.                                                                                                     |
| A paper quantifying "what fraction of _allosteric_ sites are cryptic" | Searched four ways; **does not appear to exist**. Vajda Table 1 gives the converse (cryptic → allosteric, 8/19) and CASBench gives the spatial-overlap statistic (30 %). Record as a genuine gap in the field. |

---

## 7. Consequences for this benchmark

Stated plainly, because the ground-truth definition depends on it.

1. **Our label-generation procedure produces cryptic-site labels.** `docs/targets.md`
   §"Ground-truth policy" selects protein residues within 4.5 Å of the holo ligand. That
   is exactly ASD's site-extraction rule (6 Å) and CASBench's (5 Å) — a _site-membership_
   rule. It is not, and cannot be, an allostery test: allostery needs four complexes
   (Fenton 2008), we have two.

2. **Do not write "allosteric site" where the evidence supports "ligand-contact pocket."**
   The defensible framing: _"the ground truth is the residue set lining a
   literature-validated allosteric pocket, identified from the holo complex."_ The
   allostery is inherited from the cited functional experiments in §5.3, not from our
   geometry.

3. **Do not add a minimum-distance-from-active-site filter to the labels.** No such
   convention exists in the literature (§1.5), and CASBench shows it would discard ~30 %
   of real allosteric sites (§3.3). If distance is reported at all, report it as a
   descriptive statistic — which `docs/targets.md` already does for myosin (13.3–35.6 Å).

4. **The three targets are not measuring the same thing.** KRAS is cryptic + allosteric;
   ABL1 is allosteric but pre-formed; myosin is allosteric with crypticity unmeasured.
   A method that scores well on ABL1 has demonstrated allosteric-coupling prediction, not
   pocket-opening prediction, and vice versa for KRAS. Report per-target, and say which
   axis each target probes. This is a strength if stated, and a hidden confound if not.

5. **Measure myosin's crypticity before writing the report.** Transplant `XB2` from
   `9GZ2` into the `9GZ3` frame and count clashes below 2.5 Å, exactly as was done for
   KRAS/`MOV` and ABL1/`AY7`. That one number decides whether this benchmark has one
   cryptic target or two.

---

## 8. Bibliography

Definitions — allostery

- Monod J, Wyman J, Changeux JP. _J Mol Biol_ 12:88–118 (1965). PMID 14343300. doi 10.1016/S0022-2836(65)80285-6
- Koshland DE Jr, Némethy G, Filmer D. _Biochemistry_ 5:365–385 (1966). PMID 5938952. doi 10.1021/bi00865a047
- Changeux JP, Edelstein SJ. _Science_ 308:1424–1428 (2005). PMID 15933191. doi 10.1126/science.1108595
- Gunasekaran K, Ma B, Nussinov R. _Proteins_ 57:433–443 (2004). PMID 15382234. doi 10.1002/prot.20232
- Fenton AW. _Trends Biochem Sci_ 33:420–425 (2008). PMID 18706817. PMCID PMC2574622. doi 10.1016/j.tibs.2008.05.009
- Nussinov R, Tsai CJ. _Cell_ 153:293–305 (2013). PMID 23582321. doi 10.1016/j.cell.2013.03.034
- Motlagh HN, Wrabl JO, Li J, Hilser VJ. _Nature_ 508:331–339 (2014). PMID 24740064. PMCID PMC4224315. doi 10.1038/nature13001
- Liu J, Nussinov R. _PLoS Comput Biol_ 12:e1004966 (2016). PMID 27253437. PMCID PMC4890769. doi 10.1371/journal.pcbi.1004966

Databases and benchmarks — allosteric

- Huang Z et al. ASD v1. _NAR_ 39:D663–D669 (2011). PMID 21051350. PMCID PMC3013650. doi 10.1093/nar/gkq1022
- Huang Z et al. ASD v2.0. _NAR_ 42:D510–D516 (2014). PMID 24293647. PMCID PMC3965017. doi 10.1093/nar/gkt1247
- Shen Q et al. ASD v3.0. _NAR_ 44:D527–D535 (2016). PMID 26365237. PMCID PMC4702938. doi 10.1093/nar/gkv902
- Liu X et al. ASD 2019. _NAR_ 48:D394–D401 (2020). PMID 31665428. PMCID PMC7145546. doi 10.1093/nar/gkz958
- Zlobin A, Suplatov D, Kopylov K, Švedas V. CASBench. _Acta Naturae_ 11:74–80 (2019). PMID 31024751. PMCID PMC6475866. doi 10.32607/20758251-2019-11-1-74-80

Definitions and benchmarks — cryptic

- Cimermancic P et al. CryptoSite. _J Mol Biol_ 428:709–719 (2016). PMID 26854760. PMCID PMC4794384. doi 10.1016/j.jmb.2016.01.029
- Vajda S, Beglov D, Wakefield AE, Egbert M, Whitty A. _Curr Opin Chem Biol_ 44:1–8 (2018). PMID 29800865. PMCID PMC6088748. doi 10.1016/j.cbpa.2018.05.003
- Beglov D et al. _PNAS_ 115:E3416–E3425 (2018). PMID 29581267. PMCID PMC5899430. doi 10.1073/pnas.1711490115
- Kuzmanic A, Bowman GR, Juarez-Jimenez J, Michel J, Gervasio FL. _Acc Chem Res_ 53:654–661 (2020). PMID 32134250. PMCID PMC7263906. doi 10.1021/acs.accounts.9b00613
- Meller A et al. PocketMiner. _Nat Commun_ 14:1177 (2023). PMID 36859488. PMCID PMC9977097. doi 10.1038/s41467-023-36699-3
- Škrhák V, Novotný M, Feidakis CP, Krivák R, Hoksza D. CryptoBench. _Bioinformatics_ 41:btae745 (2024). PMID 39693053. PMCID PMC11725321. doi 10.1093/bioinformatics/btae745
- Koseki J et al. CrypToth. _J Chem Inf Model_ (2025). PMID 40404166. PMCID PMC12152933. doi 10.1021/acs.jcim.4c02111

The relationship

- Bowman GR, Geissler PL. _PNAS_ 109:11681–11686 (2012). PMID 22753506. PMCID PMC3406870. doi 10.1073/pnas.1209309109
- Hart KM et al. _PLoS ONE_ 12:e0178678 (2017). PMID 28570708. PMCID PMC5453556. doi 10.1371/journal.pone.0178678
- Porter JR et al. _Biophys J_ 116:818–830 (2019). PMID 30744991. PMCID PMC6400826. doi 10.1016/j.bpj.2018.11.3144
- Ni D et al. _Chem Sci_ 12:464–476 (2021). PMID 34163609. PMCID PMC8178949. doi 10.1039/D0SC05131D
- Chen S et al. _Cancer Cell_ 39:225–239 (2021). PMID 33357454. doi 10.1016/j.ccell.2020.11.013
- Cruz MA et al. _Nat Commun_ 13:2269 (2022). PMID 35477718. PMCID PMC9046395. doi 10.1038/s41467-022-29927-9
- Colombo G. _Curr Opin Struct Biol_ 83:102702 (2023). PMID 37716095. doi 10.1016/j.sbi.2023.102702

KRAS

- Ostrem JM, Peters U, Sos ML, Wells JA, Shokat KM. _Nature_ 503:548–551 (2013). PMID 24256730. PMCID PMC4274051. doi 10.1038/nature12796
- Lito P, Solomon M, Li LS, Hansen R, Rosen N. _Science_ 351:604–608 (2016). PMID 26841430. PMCID PMC4955282. doi 10.1126/science.aad6204
- Gentile DR et al. _Cell Chem Biol_ 24:1455–1466 (2017). PMID 29033317. PMCID PMC5915340. doi 10.1016/j.chembiol.2017.08.025
- Janes MR et al. _Cell_ 172:578–589 (2018). PMID 29373830. doi 10.1016/j.cell.2018.01.006
- Canon J et al. _Nature_ 575:217–223 (2019). PMID 31666701. doi 10.1038/s41586-019-1694-1
- Lanman BA et al. _J Med Chem_ 63:52–65 (2020). PMID 31820981. doi 10.1021/acs.jmedchem.9b01180
- Weng C, Faure AJ, Escobedo A, Lehner B. _Nature_ 626:643–652 (2024). PMID 38109937. PMCID PMC10866706. doi 10.1038/s41586-023-06954-0

ABL1

- Nagar B et al. _Cancer Res_ 62:4236–4243 (2002). PMID 12154025. [PDB 1M52]
- Hantschel O et al. _Cell_ 112:845–857 (2003). PMID 12654250. doi 10.1016/S0092-8674(03)00191-0
- Nagar B et al. _Cell_ 112:859–871 (2003). PMID 12654251. doi 10.1016/S0092-8674(03)00194-6
- Adrián FJ et al. _Nat Chem Biol_ 2:95–102 (2006). PMID 16415863. doi 10.1038/nchembio760
- Zhang J et al. _Nature_ 463:501–506 (2010). PMID 20072125. PMCID PMC2901986. doi 10.1038/nature08675
- Wylie AA et al. _Nature_ 543:733–737 (2017). PMID 28329763. doi 10.1038/nature21702
- Schoepfer J et al. _J Med Chem_ 61:8120–8135 (2018). PMID 30137981. doi 10.1021/acs.jmedchem.8b01040
- Paladini J, Maier A, Habazettl JM, Hertel I, Sonti R, Grzesiek S. _eLife_ 13:e92324 (2024). PMID 38588001. PMCID PMC11001296. doi 10.7554/eLife.92324
- Hughes TP, White DL, Yeung DT. _Haematologica_ (2025). PMID 40568725. PMCID PMC12485309. doi 10.3324/haematol.2024.286798

Cardiac myosin

- Green EM et al. _Science_ 351:617–621 (2016). PMID 26912705. PMCID PMC4784435. doi 10.1126/science.aad3456
- Sirigu S et al. _PNAS_ 113:E7448–E7455 (2016). PMID 27815532. PMCID PMC5127359. doi 10.1073/pnas.1609342113
- Rohde JA, Roopnarine O, Thomas DD, Muretta JM. _PNAS_ 115:E7486–E7494 (2018). PMID 30018063. PMCID PMC6094135. doi 10.1073/pnas.1720342115
- Anderson RL et al. _PNAS_ 115:E8143–E8152 (2018). PMID 30104387. PMCID PMC6126717. doi 10.1073/pnas.1809540115
- Meller A et al. _eLife_ 12:e83602 (2023). PMID 36705568. PMCID PMC9995120. doi 10.7554/eLife.83602
- Auguin D et al. _Nat Commun_ 15:4885 (2024). PMID 38849353. doi 10.1038/s41467-024-47587-9
- Somavarapu AK, Ge J, Yengo CM, Craig R, Padrón R. _Sci Adv_ (2026). PMID 42054467. PMCID PMC13127576. doi 10.1126/sciadv.aed6472
- McMillan SN, Pitts JRT, Barua B, Winkelmann DA, Scarff CA. _Sci Adv_ (2026). PMID 42054462. PMCID PMC13127578. doi 10.1126/sciadv.aea9335
