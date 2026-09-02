# Per-residue descriptors from an apo structure: what marks an allosteric site, and what only marks burial

**Scope:** physicochemical, evolutionary and biological descriptors computable per residue from apo
heavy-atom coordinates, the one-letter sequence and the deposited B-factors — packing, flexibility,
electrostatics, evolutionary rate, language-model entropy and amino-acid composition — and the
published evidence on which of them separate **allosteric** sites specifically. It deliberately
excludes pocket-level detectors (fpocket, ConCavity, cavity volume), network centrality measures,
elastic network models, and any method that consumes an MD trajectory.
**Sibling files:** `docs/method/review/01-classical-baselines.md` (pocket and ENM baselines),
`docs/method/review/02-ai-methods.md` (supervised predictors and their C2 verdicts),
`docs/method/review/06-signal-propagation-physics.md` (what physically carries the signal),
`docs/method/review/09-data-analysis.md` (what our own measured numbers already say).
**Retrieved:** 2026-08-26.

---

## 0. The one-paragraph answer

Almost every packing descriptor in the literature is the **same descriptor**. Halle showed in 2002
that the crystallographic mean-square displacement is essentially the inverse of local contact
density, and concluded that B-factors "provide little independent information beyond that contained
in the mean atomic coordinates" (doi:10.1073/pnas.032522499) [VERIFIED-ABSTRACT]. Voronoi volume,
weighted contact number, occluded surface, residue depth, DPX and the protrusion index are all
monotone functions of how much protein sits within a few Å of a residue. Our benchmark's null
already controls burial, and `allo.scoring.properties` already reports RSA and normalised B-factor.
Adding five more descriptors on that axis buys correlated tests and a worse multiplicity correction,
not new information.

The axes that are genuinely **not** burial are: evolutionary rate, local electrostatic anomaly,
crystallographic conformational heterogeneity (altloc), sequence separation of contacts, and
rigid-cluster membership. Of those, only evolutionary rate has been measured against allosteric
sites — and the measurement says conservation works for **catalytic** sites and largely fails for
allosteric ones. That is the single most decision-relevant finding in this file.

---

## 1. Packing and burial beyond plain SASA

### 1.1 What each descriptor is

| Descriptor                            | Definition, as published                                                                                                                                        | Source                                                                                                                                    |
| ------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| Residue depth                         | "the distance of any atom/residue to the closest bulk water"                                                                                                    | Tan 2013, doi:10.1093/nar/gkt503 [VERIFIED-ABSTRACT]                                                                                      |
| DPX (depth index)                     | "its distance (A) from the closest solvent accessible atom"                                                                                                     | Pintar 2003, doi:10.1093/bioinformatics/19.2.313 [VERIFIED-ABSTRACT]                                                                      |
| CX (protrusion index)                 | sphere of "predetermined radius" per heavy atom; cx = ratio of external to internal volume                                                                      | Pintar 2002, doi:10.1093/bioinformatics/18.7.980 [VERIFIED-ABSTRACT]                                                                      |
| Occluded surface / OSP                | dots on each atom's vdW surface; a normal is _occluded_ if it meets a neighbour's vdW surface before exceeding a water diameter; OSP is the per-residue average | FIBOS, doi:10.1093/bioinformatics/btaf434 [VERIFIED-FULLTEXT], method of Pattabiraman 1995, doi:10.1002/jmr.300080603 [VERIFIED-ABSTRACT] |
| Voronoi cell volume / packing density | "the free space between neighbouring atoms to estimate van der Waals interactions"                                                                              | Voronoia 4-ever, doi:10.1093/nar/gkab466 [VERIFIED-ABSTRACT]                                                                              |
| Weighted contact number               | contact count weighted by "the square of the reciprocal distance between the contacting pair", i.e. `WCN_i = Σ_{j≠i} r_ij^-2`                                   | Lin 2008, doi:10.1002/prot.21983 [VERIFIED-ABSTRACT]                                                                                      |
| Contact order                         | "the average sequence separation between contacting residues in the native state"                                                                               | Plaxco 1998, doi:10.1006/jmbi.1998.1645 [VERIFIED-ABSTRACT]                                                                               |

Note the CX and DPX programs both write their output into the PDB B-factor field
(doi:10.1093/bioinformatics/18.7.980, doi:10.1093/bioinformatics/19.2.313) [VERIFIED-ABSTRACT]. If
we ever parse their output we must not then read that field as a temperature factor.

### 1.2 Per-descriptor verdict

All seven are computable from heavy-atom coordinates alone. None needs an external resource, an
alignment, a force field or a trajectory. All pass C1, C2 and C6 without argument.

| Descriptor              | (a) coords+seq+B alone? | (b) external resource | (c) C1/C2/C6   | (d) allosteric effect size |
| ----------------------- | ----------------------- | --------------------- | -------------- | -------------------------- |
| Residue depth           | yes                     | none                  | pass/pass/pass | **not measured**           |
| DPX                     | yes                     | none                  | pass/pass/pass | **not measured**           |
| CX protrusion           | yes                     | none                  | pass/pass/pass | **not measured**           |
| Occluded surface / OSP  | yes                     | none                  | pass/pass/pass | **not measured**           |
| Voronoi volume          | yes                     | none                  | pass/pass/pass | **not measured**           |
| Weighted contact number | yes                     | none                  | pass/pass/pass | **not measured**           |
| Local contact order     | yes                     | none                  | pass/pass/pass | **not measured**           |

"Not measured" throughout means **not retrieved by the search recorded in §8**, per ADR 0019. It is
not a claim that no such measurement exists. What the searches did return, repeatedly, was
validation against a _different_ endpoint:

- Residue depth "correlates significantly better than accessibility with effects of mutations on
  protein stability and on protein-protein interactions" (Chakravarty & Varadarajan 1999,
  doi:10.1016/s0969-2126(99)80097-5) [VERIFIED-ABSTRACT]. The endpoint is ΔΔG, not allostery.
- SDM adopts "packing density and residue depth" as stability-prediction parameters
  (doi:10.1093/nar/gkx439) [VERIFIED-ABSTRACT]; Packpred uses "amino acid depth" for missense effect
  (doi:10.3389/fmolb.2021.646288) [VERIFIED-ABSTRACT]. Again mutation effect, not site class.
- CX was demonstrated on "two protein-protein complexes and in the prediction of limited proteolysis
  sites" (doi:10.1093/bioinformatics/18.7.980) [VERIFIED-ABSTRACT]. Proteolysis susceptibility is a
  surface-exposure endpoint.
- Voronoi packing is applied "in determining thermostability, in protein design, ligand binding and
  to identify flexible regions" (Voronoia 2009, doi:10.1093/nar/gkn769) [VERIFIED-ABSTRACT].
- Treado 2019 found "the distributions of surface Voronoi cell volumes and local porosities obey
  similar statistics" in jammed packings and protein cores (doi:10.1103/physreve.99.022416)
  [VERIFIED-ABSTRACT] — i.e. protein packing statistics are generic, which is an argument _against_
  packing carrying site-specific information.

So the honest summary for section 1: **every one of these descriptors has published evidence that it
separates buried from exposed, and none has published evidence that it separates allosteric from
background.** They are refinements of the burial axis. Chakravarty & Varadarajan's own motivation
says so explicitly: accessible surface area "does not distinguish between atoms just below the
protein surface and those in the core" [VERIFIED-ABSTRACT]. Depth is a better burial ruler. It is
still a burial ruler.

### 1.3 The one exception: contact order is not a burial descriptor

Contact order measures _sequence_ separation of spatial contacts, not amount of neighbouring
protein. Plaxco's result — proteins with primarily sequence-local contacts fold faster
(doi:10.1006/jmbi.1998.1645) [VERIFIED-ABSTRACT] — is a chain-level statistic. A per-residue variant
(mean `|i − j|` over residue _i_'s contacts, optionally normalised by chain length) is a
straightforward construction, but it is **our** construction: no published per-residue local contact
order with an allosteric effect size was retrieved [UNVERIFIED]. It is worth computing precisely
because it is the only cheap descriptor in this section that is not collinear with burial by
construction.

### 1.4 A caution about single structures

Gáspári 2010 recomputed CX and DPX across an RDC-restrained ubiquitin ensemble and found "the
environment of protruding atoms is highly variable across conformers, on the other hand, only a part
of buried atoms tends to fluctuate", concluding that "the variability of the ensemble cautions
against the use of single conformers when explaining functional phenomena"
(doi:10.2174/138920310794109201) [VERIFIED-ABSTRACT]. Our input is one apo structure. Surface-side
descriptors (CX, RSA) are therefore noisier across the ensemble than core-side ones (DPX, depth) —
which is the wrong way round for finding a surface allosteric pocket.

---

## 2. Flexibility and rigidity from a static structure, without MD

### 2.1 B-factor: the descriptor we already compute, and what it is worth

Two findings bound it from opposite sides.

**It is not independent information.** Halle's local density model predicts "a direct inverse
proportionality between the AMSD and the contact density, i.e., the number of noncovalent neighbor
atoms within a local region of approximately 1.5 nm³ volume", tested on 38 non-homologous
high-quality structures, and concludes "AMSDs provide little independent information beyond that
contained in the mean atomic coordinates" (doi:10.1073/pnas.032522499) [VERIFIED-ABSTRACT]. Lin 2008
quantified the same relation the other way: over 972 X-ray structures (resolution < 2.0 Å, sequence
identity < 25 %) the mean correlation between X-ray and computed B-factors is **0.61** for the
weighted contact-number model and **0.51** for plain contact number (doi:10.1002/prot.21983)
[VERIFIED-ABSTRACT].

Read those together and the consequence for us is direct: **`normalised_b_factor` and any
contact-number descriptor are, to r ≈ 0.6–0.8, the same column.** We should not add WCN as a fourth
confounder and then treat it as an independent test.

**It is noisy in absolute terms.** Carugo compared the same atoms across numerous independent
crystal structures of _Gallus gallus_ lysozyme and found "the estimated B-factor errors are quite
large, close to 9 Å² in ambient-temperature structures and to 6 Å² in low-temperature structures",
adding that "it therefore remains essential to normalize B factors when comparing different crystal
structures" (doi:10.1107/S2059798321011736) [VERIFIED-ABSTRACT]. His review of ADPs states the
"crucial aspect is the standardization of the ADPs when comparisons between two or more protein
crystal structures are made, since ADPs are differently affected by several factors, from
crystallographic resolution to refinement protocols", and warns of "the modern tendency to let ADPs
to inflate up to extremely large values that have little physico-chemical meaning"
(doi:10.1007/s00726-018-2574-y) [VERIFIED-ABSTRACT]. A further review is titled, without hedging,
"Uses and Abuses of the Atomic Displacement Parameters in Structural Biology"
(doi:10.1007/978-1-0716-2095-3_12) [VERIFIED-ABSTRACT].

Our implementation already takes the chain's own z-score, which is exactly the normalisation Carugo
demands. That is the right choice and it is now cited. What it does **not** fix is that the z-score
is within-chain: two arms refined at different resolutions have differently-shaped B distributions,
so a z-score is comparable in rank but not in scale.

**Does B-factor discriminate allosteric sites?** No paper reporting a B-factor-alone effect size for
allosteric-site discrimination was retrieved, in either direction. Two searches aimed squarely at it
("B-factor allosteric site prediction flexibility discriminate"; "allosteric hotspot residues buried
versus exposed solvent accessibility statistics") returned nothing on point. Record this as
**unknown**, not as absent. The nearest evidence is indirect and points at flexibility _change_
rather than flexibility _level_: Panjkovich & Daura observed "significant changes in protein
flexibility upon allosteric-ligand binding in 70% of the cases" and reported "65% positive
predictive value in identifying allosteric sites" (doi:10.1186/1471-2105-13-273)
[VERIFIED-ABSTRACT]. The 70 % figure is measured by comparing apo and holo, so it characterises the
phenomenon and cannot be an input under C1.

### 2.2 Anisotropic displacement parameters

Anisotropic refinement gives six ADPs per atom instead of one B, and hence a direction of preferred
motion. Carugo predicts "future applications will involve anisotropically refined B-factors"
(doi:10.1007/978-1-0716-2095-3_12) [VERIFIED-ABSTRACT]. No paper stating the resolution threshold
for anisotropic refinement, nor the fraction of PDB entries carrying `ANISOU` records, was retrieved
by the recorded search. **Practical verdict:** available only for a minority of entries, and its
availability correlates with resolution, which correlates with everything. (a) yes when `ANISOU` is
present, no otherwise; (b) none; (c) pass/pass/pass; (d) not measured. Do not build on it until the
coverage on our own frozen arms is counted — that is a two-line check, not a literature question.

### 2.3 Ensemble-of-NMR-models RMSF

Per-residue spread across deposited NMR models is free when models exist. Its interpretation is
contested in the literature we retrieved: Fowler, Sljoka & Williamson built an NMR _validation_
method by comparing "random coil index [RCI] against local rigidity predicted by mathematical
rigidity theory, calculated from NMR structures [FIRST]" (doi:10.1038/s41467-020-20177-1)
[VERIFIED-ABSTRACT] — i.e. the model spread is treated as something to be validated, not as a
measurement of dynamics. Gáspári's ubiquitin result above is the same warning.

(a) Yes, if the deposited entry is an NMR ensemble; (b) none; (c) pass/pass/pass; (d) not measured
for allosteric discrimination. **Irrelevant for us in practice**: our apo inputs are crystal
structures. Skip.

### 2.4 Alternate-conformation (altloc) occupancy

This is the most interesting item in section 2, because it is real experimental heterogeneity that
is already sitting in the input file and costs nothing to read.

The supporting literature is strong on the concept. van den Bedem's CONTACT performs "automated
identification of functional dynamic contact networks from X-ray crystallography" and found that in
ecDHFR "mutations that alter optimized contact networks of coordinated motions can impair catalytic
function" (doi:10.1038/nmeth.2592) [VERIFIED-ABSTRACT]. Wankowicz 2022 reports the coupling
directly: "When binding site residues become more rigid upon ligand binding, distant residues tend
to become more flexible, especially in non-solvent-exposed regions" (doi:10.7554/eLife.74114)
[VERIFIED-ABSTRACT] — note that this is an apo-vs-holo comparison and so is a description of the
phenomenon, not an admissible input. Tooling to _increase_ altloc coverage exists: qFit
(doi:10.7554/elife.90606) [VERIFIED-ABSTRACT] and FLEXR, which states that "protein conformational
dynamics that may inform biology often lie dormant in high-resolution electron-density maps"
(doi:10.1107/s2059798323002498) [VERIFIED-ABSTRACT].

(a) Yes — the altloc indicator and occupancy are columns in the PDB file. (b) None for reading them;
re-refining with qFit or FLEXR needs the structure factors from the PDB, which is an extra fetch and
a real dependency. (c) C1 pass (apo file's own altlocs), C2 pass (crystallographic measurement, not
simulation), C6 pass (no force field involved in reading the column; qFit re-refinement would
introduce one and needs its own verdict). (d) Not measured as a per-residue allosteric ranking score
by any paper retrieved.

**Limitation that decides it:** altloc records are sparse and their density tracks resolution.
Before spending effort here, count what fraction of residues in our frozen apo arms carry any
altloc. If it is a few percent, the descriptor is mostly zeros and cannot rank.

### 2.5 Rigidity theory and rigid-cluster size

FIRST counts degrees of freedom in a constraint network of "covalent and hydrogen bonds and salt
bridges", identifies "all the rigid and flexible substructures", assigns "a flexibility index for
each bond", is "approximately a million times faster than molecular dynamics simulations" and works
"from analysis of a single, static three-dimensional structure" (Jacobs 2001, doi:10.1002/prot.1081)
[VERIFIED-ABSTRACT]. Thorpe 2001 adds that "a negative flexibility index provides a measure of the
density of redundant bonds in rigid regions" (doi:10.1016/s1093-3263(00)00122-4) [VERIFIED-ABSTRACT].

Applied to allostery: Pfleger used "a rigidity-theory-based approach" on HCN2 channels to "identify
two intersubunit and one intrasubunit pathways that differ in allosteric coupling strength"
(doi:10.1016/j.bpj.2021.01.017) [VERIFIED-ABSTRACT]. Schulze, Sljoka & Whiteley analysed how
oligomer point-group symmetry adds flexibility in body-bar frameworks, motivated by dimers that
"often have allosteric function that requires motions to link distant sites on the two protein
chains" (doi:10.1098/rsta.2012.0041) [VERIFIED-ABSTRACT]. Sljoka's NikR work concluded
computationally "that nickel binding increases protein rigidity to slow down the conformational
exchange" (doi:10.1016/j.jbc.2022.102785) [VERIFIED-ABSTRACT].

(a) **No.** The pebble game needs hydrogen bonds with geometry and an energy cut-off, which needs
hydrogens placed and a donor-acceptor energy function. That is more than heavy atoms plus sequence.
(b) A hydrogen-placement step and an H-bond energy function; both are local, no database. (c) C1
pass; C2 pass (combinatorial, single structure, explicitly not MD); **C6 is a judgement call** — the
H-bond energy function is a force-field fragment, and C6 says atomic force fields are abstracted
away. Reading C6 as scoping the _propagation model_ rather than every auxiliary readout makes it
admissible; the opposite reading blocks it. This needs an ADR before anyone implements it.
(d) Case studies only; no dataset-level allosteric effect size retrieved.

**Verdict:** highest conceptual fit of anything in section 2, highest implementation cost, no
published effect size on a benchmark. Defer, and record why.

---

## 3. Electrostatics without a force field

### 3.1 THEMATICS, retrieved in full

The original result: analysis of theoretical microscopic titration curves for all ionizable residues
of TIM, aldose reductase and phosphomannose isomerase "shows that a small fraction (3-7%) of the
curves possess a flat region where the residue is partially protonated over a wide pH range. The
preponderance of residues with such perturbed curves occur in the active site" (Ondrechen, Clifton &
Ringe 2001, doi:10.1073/pnas.211436698) [VERIFIED-ABSTRACT].

The numbers on a real benchmark, 169 enzymes, positive class = CatRes/CSA-annotated catalytic
residues (Wei 2007, doi:10.1186/1471-2105-8-119) [VERIFIED-ABSTRACT]:

| Z-score cut-off | Recall | Precision | False-positive rate |
| --------------- | ------ | --------- | ------------------- |
| 1.00            | 41.1 % | 19.4 %    | 1.95 %              |
| 0.99            | 50.4 % | 17.9 %    | 2.60 %              |
| 0.98            | 54.2 % | 16.4 %    | 3.12 %              |

With an SVM on top: "average recall rate for annotated catalytic residues is 61%; good precision is
maintained selecting only 4% of all residues. The average false positive rate ... is only 3.2%, far
lower than other 3D-structure-based methods" (Tong 2008, doi:10.1110/ps.073213608)
[VERIFIED-ABSTRACT].

**Input requirement, which is the decisive fact.** THEMATICS computes its curves using "Finite
Difference Poisson-Boltzmann techniques" (Shehadi 2005, doi:10.1142/s0219720005000916)
[VERIFIED-ABSTRACT]. FDPB requires per-atom partial charges and per-atom radii — a parameter set
such as PARSE, CHARMM or AMBER. That is a force field in everything but name.

In POOL, "THEMATICS features represent the single most important component" of the classifier, and
structure-only POOL reaches "nearly the same level of performance as methods that use both 3D
structure and sequence alignment data" (Tong 2009, doi:10.1371/journal.pcbi.1000266)
[VERIFIED-ABSTRACT]. The POOL server takes "THEMATICS electrostatics data and pocket information
from ConCavity" plus optional evolutionary data from INTREPID (doi:10.1093/bioinformatics/bts321)
[VERIFIED-ABSTRACT].

**Two hard caveats for us.** First, every THEMATICS/POOL number above is for **catalytic** sites.
The Ondrechen group's extension toward distal residues is a separate paper about "distal residue
participation in enzyme catalysis" (doi:10.1002/pro.2648) [VERIFIED-ABSTRACT], which is catalysis at
a distance, not allosteric-modulator sites. No allosteric-site effect size for THEMATICS was
retrieved. Second, our benchmark **gives the method the active site as input**. A descriptor whose
demonstrated skill is finding the active site is not scoreable on our endpoint — it would rediscover
what it was told.

### 3.2 Is there an admissible electrostatics route?

| Route                                 | (a) coords+seq+B alone?          | (b) external resource                | (c) C1/C2/C6                       | (d) allosteric effect size                             |
| ------------------------------------- | -------------------------------- | ------------------------------------ | ---------------------------------- | ------------------------------------------------------ |
| Poisson-Boltzmann (THEMATICS)         | **no** — needs charges and radii | a parameter set (PARSE/CHARMM/AMBER) | C1 pass, C2 pass, **C6 contested** | not measured for allosteric; catalytic numbers in §3.1 |
| Net formal charge in a sphere         | yes                              | none                                 | pass/pass/pass                     | not measured                                           |
| Count of titratable groups within _r_ | yes                              | none                                 | pass/pass/pass                     | not measured                                           |
| Depth-based pKa prediction (DEPTH)    | yes                              | none                                 | pass/pass/pass                     | not measured for allosteric                            |

The C6 verdict on PB is the substantive call. C6 says the elastic network hypothesis holds and
"atomic force fields are abstracted away". Loading a partial-charge set to solve PB reintroduces
exactly the atomistic parameterisation C6 abstracts away. It is arguable that C6 scopes the
_propagation Hamiltonian_ only and a confounder readout is outside it. It is equally arguable that a
reviewer reading "we abstracted away force fields" next to "we ran finite-difference
Poisson-Boltzmann with PARSE charges" will not accept the distinction. **Do not implement PB without
an ADR.**

The escape hatch is real and it is cheap. The DEPTH server predicts pKa from geometry: "we use depth
(and other features) to predict pKas of GLU, ASP, LYS and HIS residues. Our results produce an
average error of just <1 pH unit over 60 predictions", and the authors report the method
"statistically on par with two and superior to three other methods while inferior to only one"
(doi:10.1093/nar/gkt503) [VERIFIED-ABSTRACT]. Sixty predictions is a small benchmark and the error
is ~1 pH unit, so this is a coarse signal — but it needs no charges, no radii and no network. A
buried titratable residue with a large predicted shift is the geometric shadow of what THEMATICS
detects electrostatically.

No paper measuring net-charge-in-a-sphere or titratable-group-count as an allosteric-site descriptor
was retrieved. Both are one-liners; if they are worth anything, we will find out faster by running
them than by searching further.

---

## 4. Evolutionary signal

### 4.1 What each method needs, and whether it is reachable

| Method                        | External data                               | Alignment depth needed                                                  | Reachable programmatically                                | C1   | C2   |
| ----------------------------- | ------------------------------------------- | ----------------------------------------------------------------------- | --------------------------------------------------------- | ---- | ---- |
| ConSurf / Rate4Site           | homologue search over UniProt/UniRef by HMM | not stated numerically in the retrieved abstracts                       | yes, but it is a **network dependency at run time**       | pass | pass |
| SCA / sectors                 | a curated protein-family MSA                | "tens of thousands of effective sequences" for L ≥ 100                  | family-dependent; curation is manual in the source papers | pass | pass |
| DCA                           | a deep family MSA (Pfam-scale)              | "contingent on the existence of a large number of homologous sequences" | yes for well-populated families                           | pass | pass |
| Evolutionary Trace / INTREPID | MSA plus a phylogenetic tree                | not stated numerically                                                  | yes                                                       | pass | pass |

**C1 and C2 both pass, cleanly, for all four.** An MSA of homologous _sequences_ carries no holo
structural information — apo and holo are the same sequence — so nothing about the ligand-bound
state enters. And none of these is an MD trajectory or an MD-trained weight. The one C1 trap is
operational rather than conceptual: **query by sequence, never by PDB accession.** ConSurf-DB is
keyed by PDB entry; resolving our target through an accession lookup could silently pull a holo
entry's annotation into the prediction path.

**The real blocker is our offline gate, not a constraint.** `properties.py` already records
conservation as `null` because "it needs a multiple-sequence alignment against an external
database. That is a network dependency the offline gate cannot carry." That reasoning survives this
review intact. §5 is the way around it.

### 4.2 What the methods established

ConSurf "automatically collects homologues, infers their multiple sequence alignment and
reconstructs a phylogenetic tree" and uses "a probabilistic framework, to estimate the evolutionary
rates of each sequence position" (doi:10.1093/nar/gkw408) [VERIFIED-ABSTRACT]; the 2023 update
gathers homologues "using hidden Markov model-based search tools" (doi:10.1002/pro.4582)
[VERIFIED-ABSTRACT].

SCA's founding claim is that statistical coupling "predicted a set of energetically coupled
positions for a binding site residue that includes unexpected long-range interactions", confirmed by
mutation, and that "sets of interacting residues form connected pathways through the protein fold
that may be the basis for efficient energy conduction within proteins" (Lockless & Ranganathan 1999,
doi:10.1126/science.286.5438.295) [VERIFIED-ABSTRACT]. Süel 2003 generalised it: "a small subset of
residues forms physically connected networks that link distant functional sites in the tertiary
structure", across GPCRs, serine proteases and haemoglobins (doi:10.1038/nsb881)
[VERIFIED-ABSTRACT]. Hatley 2003 mutated one-third of the 38 SCA-identified residues in Gsα and
found results "consistent with this prediction" of a two-state allosteric model
(doi:10.1073/pnas.1835919100) [VERIFIED-ABSTRACT]. Halabi 2009 decomposed the S1A serine proteases
into "three quasi-independent groups of correlated amino acids that we term 'protein sectors'"
(doi:10.1016/j.cell.2009.07.038) [VERIFIED-ABSTRACT].

The single most relevant SCA result for us is Reynolds 2011 on DHFR: "sector-connected surface sites
are statistically preferred locations for the emergence of allosteric control in vivo"
(doi:10.1016/j.cell.2011.10.049) [VERIFIED-ABSTRACT]. That is a direct claim that a
sequence-derived, structure-independent quantity marks allosteric surface sites. Its limitation is
equally direct: the abstract gives no count of surface sites tested and no fraction that showed an
allosteric effect, so **no effect size is extractable** from what was retrieved. One model system,
one enzyme.

DCA: "DCA is shown to yield a large number of correctly predicted contacts, recapitulating the
global structure of the contact map for the majority of the protein domains examined", explicitly
"contingent on the existence of a large number of homologous sequences" (Morcos 2011,
doi:10.1073/pnas.1111471108) [VERIFIED-ABSTRACT]. A later application reports "accuracy exceeding
82% for a large number of top pairs (>4L)" (doi:10.1063/5.0232831) [VERIFIED-ABSTRACT]. DCA's
success is at _contact prediction_, which for us is a structure-recovery task we do not need — we
have the structure.

Evolutionary Trace and its descendants: INTREPID reports "improved sensitivity at high values of
specificity" and "significant improvements over Evolutionary Trace, ConSurf"
(doi:10.1093/bioinformatics/btn474) [VERIFIED-ABSTRACT]; DISCERN cites the prior state of the art at
"precision of 18.5% at a corresponding recall of 57%" and improves it "by 12% and 20%"
(doi:10.1093/bioinformatics/btq008) [VERIFIED-ABSTRACT]. All of these numbers are for **catalytic**
residues.

### 4.3 The alignment-depth problem is severe

Kleeorin, Russ, Rivoire & Ranganathan quantified it: "For real proteins with a sequence length of
100 or greater, tens of thousands of effective sequences are required just to overcome the lowest
possible scale (pure noise associated with non-interacting positions), and many more sequences may
be required to fully sample various scales of true interactions." Practical alignments hold "on the
order of N = 10³ — 10⁵ sequences", so "nearly all cases of model inference operate in the
undersampled regime" (doi:10.1016/j.cels.2022.12.013) [VERIFIED-FULLTEXT]. Avila-Herrera & Pollard
concur that "all coevolutionary methods clearly benefit from alignments with many sequences"
(doi:10.1186/s12859-015-0677-y) [VERIFIED-ABSTRACT].

Our four primary targets are human proteins with large families, so depth is probably attainable —
but this is a per-target check, not an assumption, and it is one more reason a coupling-based
descriptor is not a free lunch.

### 4.4 Are allosteric sites more or less conserved than background? Both sides.

This is contested and the file must show both. The retrieved evidence is asymmetric in kind: the
"more conserved" side is mechanistic and case-based; the "less conserved" side is statistical and
dataset-based.

**More conserved / on a conserved network.**

- Süel 2003: "evolutionarily conserved sparse networks of amino acid interactions represent
  structural motifs for allosteric communication in proteins" (doi:10.1038/nsb881)
  [VERIFIED-ABSTRACT].
- Reynolds 2011: sectors are "an evolutionarily conserved 'wiring' mechanism", and sector-connected
  surface sites are the preferred locations for new allosteric control
  (doi:10.1016/j.cell.2011.10.049) [VERIFIED-ABSTRACT].
- Rivoire 2016 frames SCA as identifying "functionally relevant, collectively evolving residues"
  (doi:10.1371/journal.pcbi.1004817) [VERIFIED-ABSTRACT].

Note precisely what this side claims. It says allosteric sites sit on a **coevolving** network. That
is a _coupling_ statement, not a _rate_ statement. A residue can be strongly coupled to others and
still be individually variable. Conflating the two is the commonest way this debate is
mis-summarised.

**Less conserved.**

- AR-Pred, which explicitly trained on both site classes with a conservation feature: "residue
  conservation score is the most important feature" overall, but it was "significantly more
  important for active site than for allosteric site detection, as indicated by the remarkably large
  difference"; allosteric residues "are subject to lower evolutionary pressure compared to
  orthosteric residues" and are "often not conserved across all phyla" (Mishra, Kandoi & Jernigan
  2019, doi:10.1002/prot.25749) [VERIFIED-FULLTEXT]. AR-Pred's own allosteric performance is "median
  AUC of 80% and MCC of 0.48" on its validation set [VERIFIED-FULLTEXT].
- Riedlová 2026, on 453 human kinases: "Orthosteric pockets are located in minimally frustrated
  basins that generate strong evolutionary and structural signatures, whereas allosteric pockets
  occupy predominantly neutrally frustrated zones associated with conformational plasticity and
  reduced evolutionary constraint", and allosteric sites are "often transient, weakly conserved and
  sparsely populated in structural databases" (doi:10.1021/acs.jctc.6c00427) [VERIFIED-FULLTEXT].
- Martí-Aranda & Lehner 2026, mapping allosteric mutations across seven homologues: "The divergence
  in the location of allosteric mutations in each protein suggests that each protein in a family
  might have distinct sites to target with allosteric drugs" (doi:10.1038/s41467-026-71005-x)
  [VERIFIED-ABSTRACT]. If allosteric sites diverge within a family, a family MSA cannot mark them.

**Where this lands.** The two sides are not symmetric in what they would license us to build. The
"more conserved" side supports a _coupling_ descriptor (SCA sector membership), which needs tens of
thousands of sequences (§4.3) and has no dataset-level effect size. The "less conserved" side is a
direct measurement, on large datasets, of the descriptor we would actually implement — per-residue
conservation rate — and it says that descriptor is much weaker for allosteric than for catalytic
sites. For our purpose (a confounder column reported beside every score), the second side is the
operative one. **Expect conservation to be a weak allosteric discriminator and a strong catalytic
one.** That asymmetry is itself worth reporting, because our benchmark hands the method the active
site: a conservation column that lights up on the active site and not on the label set is evidence
the column is working correctly, not evidence it is useful.

---

## 5. Protein language models as an alignment-free conservation substitute

This is the route that resolves the offline-gate problem in `properties.py`.

**The substitution works, at MSA-level accuracy, for the conservation endpoint.** Marquet 2022:
"Embeddings alone predicted residue conservation almost as accurately from single sequences as
ConSeq using MSAs (two-state Matthews Correlation Coefficient-MCC-for ProtT5 embeddings of 0.596 ±
0.006 vs. 0.608 ± 0.006 for ConSeq)" (doi:10.1007/s00439-021-02411-y) [VERIFIED-ABSTRACT]. The test
set is ConSurf10k-derived, 519 sequences with experimental structures [VERIFIED-FULLTEXT].

_Verification note._ The full-text retrieval labelled 0.596 as a nine-state Q9 and separately gave
two-state Q2 = 0.688 ± 0.005 for a ProtT5 CNN against 0.698 ± 0.005 for ConSeq. The abstract labels
0.596 as a two-state MCC. The two readings conflict on what 0.596 measures. **Use the abstract
wording and treat the metric label as unsettled**; the conclusion — embeddings match MSA-based
conservation to within ~0.01 on the same metric — is the same either way, and that conclusion is
what we rely on.

**Raw entropy is a much weaker proxy than a trained head.** From the same paper's full text: the
Spearman correlation between pLM substitution-probability entropy and ConSurf-DB conservation scores
is **−0.374** [VERIFIED-FULLTEXT]. That is the number that matters if we take the cheap route — a
bare per-residue entropy from a masked-LM forward pass, with no trained regressor on top. It
explains roughly 14 % of the variance in ConSurf conservation. It is a proxy, not a substitute.

**Family-specific evotuning lifts it a long way, and shows how brittle the general case is.** Lytras
2026 correlated pLM entropy against alignment entropy on influenza haemagglutinin: off-the-shelf
ESM-2 (650M) reached Spearman 0.74 (H1), 0.67 (H5), 0.43 (H3), 0.45 (H7); evotuned models on all HA
sequences reached "between 0.83 and 0.89"; and off-the-shelf protT5MLM showed "virtually no
correlation in any comparison" (doi:10.1093/nargab/lqag018) [VERIFIED-FULLTEXT]. Read the spread:
0.43 to 0.74 across four subtypes of _one_ protein, from _one_ model. Whatever number we get on our
arms, it will not be predictable in advance.

**And PLMs fail specifically on the class we care about.** Riedlová 2026 fine-tuned a PLM on kinase
binding sites and reported AUROC by site type: Type I 0.968, Type I.5 0.975, Type II 0.941, Type III
0.910, and **Type IV (distal allosteric) 0.676**, described as a "near-random ranking regime"
(doi:10.1021/acs.jctc.6c00427) [VERIFIED-FULLTEXT]. Datasets: KinCoRe, 10,301 complexes across 453
human kinases; training on LIGYSIS_SI30, 2,949 sequences, leakage-filtered [VERIFIED-FULLTEXT]. The
method needs "Protein sequences only", no MSA and no MD [VERIFIED-FULLTEXT].

This converges with the finding already recorded in `00-conventions.md` §5 ("AUPR 0.64–0.76 on
orthosteric against 0.06 on allosteric in the same proteins, with AUROC still 0.70"). The numbers
are not identical and I did not establish whether the two trace to the same underlying work, so
treat them as one line of evidence unless someone checks [UNVERIFIED]. Either way, the direction is
unambiguous: **PLM signal is an orthosteric-site detector that degrades to near-random on distal
allosteric sites.**

|                                   | (a) coords+seq+B alone?       | (b) external resource                                                   | (c) C1/C2/C6                                                     | (d) allosteric effect size                                                                                                           |
| --------------------------------- | ----------------------------- | ----------------------------------------------------------------------- | ---------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| ESM-2 / ESM-C per-residue entropy | sequence only, no coordinates | model weights (~2.5 GB for 650M), one-time download, then fully offline | C1 pass, C2 pass (trained on sequence, not trajectories), C6 n/a | ρ = −0.374 vs ConSurf-DB (doi:10.1007/s00439-021-02411-y); as a _site_ predictor, Type IV AUROC 0.676 (doi:10.1021/acs.jctc.6c00427) |

C2 deserves one sentence of care. C2 forbids "MD-trained ML weights in the prediction path". ESM-2's
training corpus is UniRef sequences. No trajectory, no MD-derived label. It passes. This is the
distinction that kills PocketMiner and spares ESM.

---

## 6. Amino-acid composition signatures of allosteric pockets

The searches for this were the least productive of the file, and the negative result is itself
informative.

**What was found.**

- Malik & Li surveyed the intracellular candidate allosteric region across "more than 100
  representative human GPCR structures" and reported that "the physico-chemical properties and amino
  acid composition of this site vary among and within GPCR classes"; the site is "druggable for 89%
  of the GPCRs" and "not 100% identical between a GPCR and its most similar homolog for 94% of the
  GPCRs" (doi:10.1007/s10822-022-00454-5) [VERIFIED-ABSTRACT]. That is an explicit finding of
  compositional **variability**, i.e. the absence of a signature.
- Peter 2024, on GPCR allosteric sites: "extrahelical allosteric ligands and binding sites represent
  a distinct chemical space characterized by shallow pockets with low volume, and the corresponding
  allosteric ligands showed an enrichment of halogens" (doi:10.1021/acs.jcim.4c00819)
  [VERIFIED-ABSTRACT]. The enrichment is in the _ligand_, not the pocket residues.
- Smith, Lu & Carlson assembled 70,219 allosteric and 9,511 competitive unique ligands from ASD v3.0
  and ChEMBL v20, and found allosteric ligands "tend to be more aromatic and rigid"; a previously
  reported hydrophobicity difference "was not confirmed" once newer data were added
  (doi:10.1371/journal.pcbi.1005813) [VERIFIED-ABSTRACT]. Again: ligand properties, not site-residue
  composition. And the one property closest to what we compute — hydrophobicity — is the one that
  failed to replicate.
- STINGAllo's per-residue models are trained **per residue type**, and the paper notes the "donor
  energy" descriptor was pronounced for the high-performing TRP and MET models
  (doi:10.1016/j.csbj.2024.10.036) [VERIFIED-FULLTEXT]. That per-type performance spread is indirect
  evidence that residue identity carries some signal, but the paper reports no enrichment ratio.

**What was not found.** No paper reporting a residue-type enrichment or depletion at allosteric
sites versus orthosteric sites versus random surface, with an odds ratio or a p-value, was retrieved
by four separate searches (§8). Recorded as **not retrieved by the recorded search**, not as absent.

**Consequence for the descriptor we already have.** `hydrophobicity` in `properties.py` is a pure
Kyte-Doolittle lookup keyed on residue name. It contains **zero structural information** — two
residues of the same type anywhere in the chain get the same value. It can therefore only ever
detect a composition bias. The single retrieved test of a hydrophobicity difference in the
allosteric context failed to replicate (Smith 2017). Keep it as a confounder — it is free, and
reporting it costs nothing — but the prior that it moves is low, and it is partly collinear with
burial through the hydrophobic effect.

---

## 7. What this changes for our pipeline

Ranked by expected value per unit of effort. Every item names its pipeline stage. Stage names follow
`CLAUDE.md`: `scoring/properties.py` is the confounder layer, `network/` is Phase 1.2/4.

**1. Do not add any further packing descriptor. [`scoring/properties.py`]**
Formula: none needed — this is a decision not to write code. Inputs: n/a. Evidence: Halle
(doi:10.1073/pnas.032522499) shows AMSD ∝ 1/contact density and states AMSDs carry "little
independent information beyond that contained in the mean atomic coordinates"; Lin
(doi:10.1002/prot.21983) puts the B-factor/WCN correlation at 0.61 over 972 structures. **Voronoi
volume, WCN, occluded surface, residue depth, DPX and CX are all burial proxies**, and burial is
already controlled inside the null _and_ already reported as `relative_solvent_accessibility`.
Adding six correlated columns worsens multiplicity for zero new information. This is the highest-value
item in the list because it prevents work.

**2. Replace the `null` conservation column with an ESM-2 per-residue entropy. [`scoring/properties.py`]**
Formula: `H_i = −Σ_a p(a | seq \ i) log p(a | seq \ i)` from one masked forward pass per residue, or
the cheaper single-pass wild-type-marginal variant. Inputs: one-letter sequence only; model weights
vendored once so the offline gate still holds. Expected discriminative value: **weak, and that is
the point.** ρ = −0.374 against ConSurf-DB (doi:10.1007/s00439-021-02411-y); as a _site_ signal,
Type IV distal-allosteric AUROC 0.676 against Type I 0.968 (doi:10.1021/acs.jctc.6c00427); AR-Pred
finds conservation "significantly more important for active site than for allosteric site detection"
(doi:10.1002/prot.25749). It closes the fourth confounder the audit named, which is its job. Do not
promote it to a predictor.

**3. Report distance to the chain centroid alongside every score. [`scoring/properties.py`]**
Formula: `d_i = ‖x_i − mean(x)‖` over Cα, or over all heavy atoms. Inputs: coordinates. Evidence:
STINGAllo's SHAP analysis names "distance to the chain's centre of gravity" the single most
influential of its 54 descriptors, "with a mean SHAP value exceeding 0.4"
(doi:10.1016/j.csbj.2024.10.036) [VERIFIED-FULLTEXT]. Read this next to `00-conventions.md` §5,
where `ctrl_closeness = −distance` to the active site reaches AUC 0.617 and beats every quantum
observable tested. **Two independent lines now say a distance-to-a-reference-point descriptor
dominates.** Any propagation score we build must be reported net of both distances or it will be
indistinguishable from geometry. Flag: this is not a burial proxy in the RSA sense, but it is a
_globularity_ proxy and will correlate with depth. Report its Spearman against RSA the first time it
runs.

**4. Count altloc coverage on the frozen apo arms before deciding anything about it. [`structure/`]**
Algorithm: fraction of residues with more than one altloc, and mean minor-conformer occupancy.
Inputs: the apo PDB file we already parse. This is a coverage measurement, not a descriptor
proposal. Evidence for the concept is good (van den Bedem, doi:10.1038/nmeth.2592; Wankowicz,
doi:10.7554/eLife.74114), but no per-residue allosteric effect size was retrieved and the descriptor
is worthless if it is 97 % zeros. Twenty minutes of work decides whether to proceed.

**5. Compute per-residue local contact order as the one non-burial cheap descriptor. [`network/`]**
Formula: `LCO_i = mean(|i − j|)` over contacts _j_ of residue _i_, from the contact graph
`network/` already builds. Inputs: coordinates plus residue indexing. Expected value: **unknown** —
Plaxco established contact order as a chain-level folding-rate correlate
(doi:10.1006/jmbi.1998.1645) and no per-residue allosteric measurement was retrieved [UNVERIFIED for
the per-residue form]. It is worth running exactly because it is the only descriptor in this file
that is orthogonal to burial by construction and costs one line given the graph.

**6. Titratable-group count and net formal charge in a sphere, as the admissible electrostatics.
[`scoring/properties.py`]**
Formula: over a sphere of radius _r_ around the residue centroid, `q_i = Σ (+1 for Arg/Lys, −1 for
Asp/Glu, +0.1 for His)` and `n_i = ` count of those residues. Inputs: coordinates plus residue names.
No charges, no radii, no parameter set — so no C6 argument. Evidence: THEMATICS found "a small
fraction (3-7%)" of ionizable residues have anomalous titration and "the preponderance ... occur in
the active site" (doi:10.1073/pnas.211436698), with 41–54 % recall at 1.95–3.12 % FPR on 169 enzymes
(doi:10.1186/1471-2105-8-119). **But every one of those numbers is for catalytic sites, which our
benchmark hands the method as input.** No allosteric effect size retrieved. Low prior; near-zero
cost. Run it, expect nothing, report it.

**7. Blocked: Poisson-Boltzmann electrostatics, pending an ADR. [`scoring/`]**
THEMATICS needs "Finite Difference Poisson-Boltzmann techniques"
(doi:10.1142/s0219720005000916) [VERIFIED-ABSTRACT], hence per-atom partial charges and radii from a
force-field parameter set. C1 and C2 pass. **C6 is genuinely contested** and the contest is about
whether C6 scopes the propagation model or the whole prediction path. Do not implement until that is
written down and accepted.

**8. Deferred: rigid-cluster size from a FIRST-style pebble game. [`network/`]**
Best conceptual fit in the file — it is a single-static-structure, non-MD, topology-driven
flexibility decomposition, "approximately a million times faster than molecular dynamics"
(doi:10.1002/prot.1081), with a published allosteric application (doi:10.1016/j.bpj.2021.01.017).
Blocked on two things: it needs hydrogens placed and an H-bond energy cut-off, which raises the same
C6 question as item 7; and no dataset-level allosteric effect size was retrieved, only case studies.
Revisit if items 2–6 all come back flat.

**9. Not applicable: NMR-ensemble RMSF and anisotropic displacement parameters.**
Our apo inputs are crystal structures, so ensemble RMSF is unavailable. ADPs exist only for a
resolution-selected minority of entries, which makes their availability itself a confounder. Neither
has a retrieved allosteric effect size.

**Explicit burial-proxy flags**, since the null already controls burial:

| Descriptor                                          | Burial proxy?                                                                               | Basis                                                       |
| --------------------------------------------------- | ------------------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| Residue depth, DPX                                  | **Yes**, by definition — distance to solvent                                                | doi:10.1093/nar/gkt503                                      |
| CX protrusion                                       | **Yes**, inverted burial                                                                    | doi:10.1093/bioinformatics/18.7.980                         |
| Voronoi volume, OSP, packing density                | **Yes**                                                                                     | doi:10.1093/nar/gkab466, doi:10.1093/bioinformatics/btaf434 |
| Weighted contact number                             | **Yes**, and additionally collinear with B-factor at r ≈ 0.61                               | doi:10.1002/prot.21983                                      |
| Normalised B-factor (already implemented)           | **Yes** — Halle's inverse-contact-density result makes it one                               | doi:10.1073/pnas.032522499                                  |
| Kyte-Doolittle hydrophobicity (already implemented) | **Partly** — collinear via the hydrophobic effect; carries no structural information at all | doi:10.1016/0022-2836(82)90515-0                            |
| Distance to centroid                                | No, but a globularity proxy; measure its correlation with RSA                               | doi:10.1016/j.csbj.2024.10.036                              |
| Local contact order                                 | **No** — sequence separation, orthogonal by construction                                    | doi:10.1006/jmbi.1998.1645                                  |
| Conservation / PLM entropy                          | **No** — but conservation itself correlates with burial, so report both                     | doi:10.1007/s00439-021-02411-y                              |
| Altloc fraction                                     | **No** — but correlates with resolution                                                     | doi:10.1038/nmeth.2592                                      |
| Titratable count, net charge                        | **No** — composition and geometry                                                           | doi:10.1073/pnas.211436698                                  |

One more consequence, for whoever writes the report. **B-factor is not an independent flexibility
measurement.** Halle's conclusion means that when we print `normalised_b_factor` beside a score, we
are printing a smoothed inverse contact number. If a propagation score correlates with it, the
correct interpretation is "correlates with local packing", not "correlates with dynamics". Saying
otherwise in `docs/report/` would be a claim the source does not support.

---

## 8. Method

**Databases.** Europe PMC REST search (`resultType=core`) and full text (`fullTextXML`); PubMed
E-utilities `esearch` and `efetch`; PMC article pages; the arXiv API. All routes from
`00-conventions.md` §3. Semantic Scholar was not attempted (rate-limited per conventions).

**Query-syntax finding, worth recording for the next file.** Europe PMC returns
`{"version":"6.9"}` with an empty result list when the query string is percent-encoded with `%20`
between terms. Use `+` separators. Two searches were lost to this before it was diagnosed, and both
were re-run.

**Queries run (24 Europe PMC / PubMed searches, 2 arXiv searches).**
Packing: `residue depth allosteric site prediction`; `Chakravarty Varadarajan residue depth
protein`; `"residue depth" AND "solvent accessibility" AND cavity`; `occluded surface packing
protein Pattabiraman`; `FIBOS occluded surface packing osp protein Fleming R Python`; `Voronoi
volume packing density protein residue cavity`; `Voronoia packing density atomic volume protein
cavities Preissner Hildebrand`; `weighted contact number protein flexibility B-factor`; `"weighted
contact number"`; `"contact order" AND folding rate Plaxco`; `protrusion index CX protein surface
Pintar`; `Pintar A[Author] AND (CX OR protrusion OR DPX)`; `packing density cavity functional site
enzyme catalytic residues buried prediction Voronoi`.
Flexibility: `B-factor allosteric site prediction flexibility discriminate`; `Halle flexibility
packing proteins contact density B-factors`; `Halle B[Author] AND flexibility AND packing`;
`B-factor normalization resolution dependence pitfalls crystallographic comparison proteins`;
`temperature factor normalization protein structures comparison Z-score flexibility prediction`;
`Carugo O[Author] AND B-factor`; `anisotropic displacement parameters protein crystal structures
anisotropy dynamics`; `NMR ensemble RMSF per-residue flexibility model variability prediction`;
`alternate conformations altloc electron density Ringer qFit protein dynamics allostery`; `van den
Bedem CONTACT dynamic contact networks X-ray crystallography alternate conformations`; `rigidity
theory FIRST rigid cluster decomposition protein allostery`; `(Jacobs DJ[Author] OR Rader
AJ[Author]) AND (rigidity OR FIRST OR flexibility) AND protein`; `Sljoka A[Author] AND allosteric`.
Electrostatics: `THEMATICS titration curves active site`; `THEMATICS[Title]`; `THEMATICS Ondrechen
active site prediction titration`; `POOL Ondrechen machine learning functional site prediction
electrostatics geometry recall`; `Depth web server predict pKa ionizable residues cavity
Madhusudhan`; `PROPKA empirical pKa prediction protein accuracy RMSD`; `electrostatic potential
functional site prediction protein without force field charge density catalytic`.
Evolution: `ConSurf 2016 evolutionary conservation web server Rate4Site`; `statistical coupling
analysis protein sectors Halabi Ranganathan`; `(Lockless SW[Author] OR Suel GM[Author]) AND
(allosteric OR coupling)`; `Suel evolutionarily conserved networks residues mediate allosteric
communication`; `Reynolds McLaughlin Ranganathan hot spots allosteric regulation protein surfaces`;
`direct coupling analysis residue contacts protein structure prediction Morcos`; `Morcos F[Author]
AND direct-coupling analysis AND 2011`; `number of effective sequences Neff required coevolution
contact prediction alignment depth threshold`; `evolutionary trace Lichtarge functional site
prediction ranking`; `INTREPID evolutionary conservation catalytic residue prediction phylogenetic
accuracy`; `allosteric site conservation compared orthosteric less conserved`; `allosteric sites
evolutionarily conserved than surface residues analysis`; `allosteric site sequence conservation
ConSurf score significantly higher lower random`; `coevolution allosteric site prediction conserved
coupling sector enrichment statistics`.
Language models: arXiv `all:"protein language model" AND all:"conservation" AND all:"entropy"` (0
results); arXiv `abs:"protein language model" AND abs:conservation` (12 results, 0 on point);
`ESM-2 protein language model entropy correlates conservation ConSurf`; `protein language model
embeddings capture conservation without alignment per-residue`; `ESM language model attention
conservation ConSurf comparison per-residue Spearman`; `"pseudo-perplexity" OR "masked language
model" protein conservation correlation Shannon entropy`.
Composition and site properties: `allosteric pocket amino acid composition hydrophobic enrichment
orthosteric`; `allosteric AND "amino acid composition" AND (site OR pocket)`; `allosteric site
residue composition enriched depleted comparison random surface patches`; `allosteric residues amino
acid propensity enrichment glycine proline aromatic statistical analysis`; `allosteric pocket
enriched aromatic residues tryptophan phenylalanine propensity analysis kinases`; `allosteric
binding site more hydrophobic smaller shallower than orthosteric analysis dataset`; `Allosteric
Database ASD statistics allosteric sites properties survey modulators`; `allosteric site prediction
physicochemical features machine learning feature importance pocket`; `Allosite Huang 2013
allosteric site prediction pocket features SVM accuracy`; `Panjkovich Daura allosteric site
prediction flexibility normal mode`; `CASBench ASBench allosteric benchmark dataset curated sites`;
`allosteric hotspot residues buried versus exposed solvent accessibility statistics analysis
dataset`; `cryptic pocket residues hydrophobic enrichment apo structure descriptors comparison`;
`long-range contacts sequence separation allosteric communication network residue betweenness`;
`allosteric residues hinge regions Gaussian network model slow modes enrichment`.

**Counts.** Approximately 78 distinct records were returned across the searches with usable
bibliographic metadata. **45 were screened in** and are cited above with a DOI. Screening criterion:
the record either (i) defines a descriptor in this file's scope, (ii) reports a numeric effect size
for a descriptor against a functional-site or allosteric-site endpoint, or (iii) states an input
requirement or a limitation that changes a C1/C2/C6 verdict. Records about a single protein's
mechanism with no transferable descriptor were screened out.

**Verification depth.** 8 claims [VERIFIED-FULLTEXT] (STINGAllo 2025 and Omage 2024 full texts,
Riedlová 2026 full text, Marquet 2022 full text, Lytras 2026 full text, Kleeorin 2023 via the PMC
article page, AR-Pred via the PMC article page, FIBOS full text). The remainder are
[VERIFIED-ABSTRACT] from an abstract or metadata record retrieved this session. Three claims are
marked [UNVERIFIED] and each says why.

**Stopping rule.** Stop when a new query returns only records already screened, or returns records
whose abstracts contain no numeric effect size for the descriptor in question. Applied per section.
Sections 1 and 6 hit the rule after the fourth query each; section 4 after the fifth.

**What could not be reached.**

- **Amino-acid enrichment at allosteric sites.** Five queries, no paper with an enrichment ratio or
  a p-value. This is the largest gap in the file. Recorded as not retrieved, per ADR 0019.
- **A B-factor-alone allosteric effect size, in either direction.** Two queries aimed at it, nothing
  on point. This is a real gap given that we already compute the descriptor.
- **`AR-Pred` full text via `fullTextXML`** returned HTTP 404 for PMC6718341; the PMC article page
  worked. Same for Kleeorin (PMC10911952). Confirming `00-conventions.md` §3: when `fullTextXML`
  404s, the article page is the working fallback.
- **The Allosite 2013 paper.** Not returned by two targeted queries; only its successors (PASSer,
  PASSerRank) came back. Its feature list therefore is not quoted here.
- **Anisotropic-refinement resolution thresholds and PDB-wide ADP coverage.** Not retrieved. This is
  better answered by counting `ANISOU` records in our own frozen arms than by further searching.
- **arXiv contributed nothing.** Two queries, 12 records, none reporting a pLM-entropy /
  conservation correlation. The useful language-model numbers all came from journal venues via
  Europe PMC.

**Leakage guard.** No file under `docs/benchmark/` was opened. No real label residue appears in this
document. The only repository files read were `docs/method/review/00-conventions.md`,
`docs/method/README.md` and `src/allo/scoring/properties.py`.
