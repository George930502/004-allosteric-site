# How allostery actually works in the best-characterised systems, and the graph observables that follow

**Scope:** system-specific mechanism. For seven well-mapped families — haemoglobin, PDZ
domains, protein kinases, small GTPases, class A GPCRs, myosin, and four enzymes with
mapped communication pathways — what the protein does, which structural elements carry the
coupling, and what that would look like in a residue contact graph. It deliberately excludes
the general physics of what carries a signal (timescales, damping, entropic versus enthalpic,
the distance-decay law) and every algorithm, propagator and predictor.
**Sibling files:** `00-conventions.md` (rules, and the eleven quantum insertion points already
closed by measurement); `../../review/06-signal-propagation-physics.md` (the phenomenon
independent of any system — read it first, this file does not repeat it). The algorithm
reviews cover elastic-network baselines, quantum propagators, pocket detection, machine
learning, coarse-graining, hardware and evaluation.
**Retrieved:** 2026-08-26.

---

## 0. How to read this file

**Two tags on every mechanistic claim.**

- **[apo]** — the feature can be computed from a single unbound structure. Legal as a
  prediction-path input.
- **[holo]** — the feature requires the effector-bound structure, the active-state structure,
  or a comparison of two states. **Forbidden as an input under C1.** Useful only as
  motivation, and as post-hoc explanation in the report.

Most of what the field knows about allosteric mechanism is **[holo]**. That is not an
accident of technique: mechanism is defined as a difference between states, and a difference
needs two states. The productive question for us is therefore never "what changes?" but
"what does the apo structure already say about _where_ a change is cheap?" Every "graph
signature" paragraph below is written to answer the second question.

**Leakage hygiene.** Three of the families below overlap the benchmark. For those families
this file names structural _elements_ (switch II, the myristoyl pocket, the relay helix) and
never residue numbers, so that no plausible label residue is written into a method-design
document. Residue numbers appear only for haemoglobin, ATCase, PDZ and IGPS, which are not
benchmark targets. Nothing under `docs/benchmark/` was opened.

**One number is borrowed rather than re-derived.** File 06 records that across five
homologous domains, burial is the strongest single correlate of a conserved allosteric
hotspot (relative SASA < 0.25, OR = 8.91, P < 2.2 × 10⁻¹⁶, doi:10.1101/2025.06.20.660748).
It is load-bearing in §8 and is cited, not re-measured.

---

## 1. Haemoglobin: quaternary versus tertiary coupling, and the salt-bridge network

**The classical picture.** Perutz's stereochemical mechanism is the origin of the field
[VERIFIED-ABSTRACT, metadata record only] (doi:10.1038/228726a0, PMID 5528785). Its content
is quoted here from a review that reproduces it, because the Europe PMC record for the 1970
paper carries no abstract.

**The salt bridges, named.** The T state of human HbA "is stabilized by salt bridges between
(i) the imidazole of the C-terminal βHis146 and βAsp or Glu94 or βGlu90 and (ii) the
C-terminal carboxyl of the same βHis146β and αLys40" [VERIFIED-FULLTEXT] (PMC10046315,
doi:10.3390/biom13030572). These are the constraints that break on T → R. **[holo]** for the
"break" part; **[apo]** for the identity of the bridges, since they are present and visible in
the unliganded T structure.

**The limitation the same review states, and it matters.** "In human HbA, the salt bridges
broken during the allosteric transition make an important contribution to the difference in
stability between the two allosteric states, **but do not seem to be sufficient enough to
account for the overall free energy change** calculated from the O₂ binding isotherm"
[VERIFIED-FULLTEXT] (PMC10046315). A named set of breakable contacts does not add up to the
measured cooperativity. Whatever carries the rest is distributed.

**MWC is not the whole story, and the correction is tertiary.** The tertiary two-state (TTS)
model holds that "binding without a quaternary conformational change is non-cooperative, but
... tertiary conformations of individual subunits play the primary role"
[VERIFIED-ABSTRACT] (doi:10.1016/s0301-4622(02)00091-1, PMID 12128196). The supporting
observation is that "a large fraction of liganded subunits in the T quaternary structure have
the same functional conformation as liganded subunits in the R quaternary structure"
[VERIFIED-ABSTRACT] (doi:10.1080/15216540701272380, PMID 17701554). Direct structural
evidence followed: trapping tertiary conformations in silica gels gives "direct evidence for
the coexistence of high- and low-affinity tertiary conformations with **broken and unbroken**
β-C-terminal salt bridges, respectively, **in the anion-free T quaternary structure**"
[VERIFIED-ABSTRACT] (doi:10.1002/pro.70193, PMC12168133). The same quaternary state contains
both bridge states. A review makes the general point that "cooperative events occurring within
each allosteric conformation, in the absence of quaternary structural change, have usually
been overlooked" [VERIFIED-ABSTRACT] (doi:10.2174/1389203718666171030103310, PMID 29086690).

**Reformulation is still live.** A 2026 treatment reformulates both the Pauling and the MWC
models for the canonical equilibrium and reassesses the role of cooperativity
[VERIFIED-ABSTRACT] (doi:10.1063/5.0310372, PMID 41562430). Crocodilian haemoglobin, where
bicarbonate rather than organic phosphate is the effector, shows the allosteric machinery is
re-wireable by a small number of substitutions [VERIFIED-ABSTRACT]
(doi:10.1038/s41467-024-49947-x, PMC11294572; doi:10.1016/j.cub.2022.11.049, PMC9839640).

**What an elastic-network reading of the transition gives.** A Gaussian network model computed
on each structure along the T → R2 path shows that "subunit correlation within the same dimer
becomes increasingly positive upon T → R2 transition, while interdomain correlation becomes
increasingly negative" [VERIFIED-ABSTRACT] (doi:10.1002/prot.70014, PMC12594184). The
transition is a re-partitioning of the correlation matrix into modules, not a displacement
along a route. A separate 2026 study reconstructs environment-dependent force constants from
equilibrium fluctuations and reports "mechanical softening at regulatory interfaces" that
correlates with cooperative binding [VERIFIED-ABSTRACT] (doi:10.1016/j.bpj.2026.01.006,
PMID 41536061) — but it derives the covariance from trajectories, so it is a **C2 violation as
published**; only the softening claim transfers.

### The graph signature this predicts

A two-state population shift does **not** appear in a single contact graph as a path. It
appears as a **sparse, low-capacity cut between two rigid modules**, decorated by a small
number of charged contacts that are the only thing holding the modules in the low-affinity
register. Three testable consequences, all **[apo]**:

1. The α1β2-type interface is a _narrow_ cut: few edges, high per-edge importance. Score a
   residue by its participation in minimum cuts separating the two largest GNM-correlated
   modules.
2. The residues that matter are **charged residues sitting on that cut**, not buried
   hydrophobics. This is the one system where a salt-bridge edge class should outweigh a
   generic contact edge — consistent with file 06 §5.
3. The correlation matrix, not the distance matrix, carries the state. A residue's score
   should be its contribution to the _sign structure_ of the slow modes, not its arrival
   amplitude.

**Scope limit, stated plainly.** All three are quaternary observables. Our node set is every
modelled residue of one frozen chain (ADR 0010, C5). A single-chain graph cannot see an
inter-subunit cut. Haemoglobin therefore motivates the _module-boundary_ family of observables
in §8 but supplies no feature we can compute on our own inputs.

---

## 2. PDZ domains and protein sectors: the strongest claim in the field, and the papers that failed to reproduce it

**The claim.** Lockless & Ranganathan reported for the PDZ family "a set of energetically
coupled positions ... that includes unexpected long-range interactions", forming "connected
pathways through the protein fold" (doi:10.1126/science.286.5438.295). Süel et al. extended
it to three unrelated families and Halabi et al. decomposed a protease family into three
quasi-independent, physically contiguous sectors. These three are quoted from file 06, which
retrieved them on 2026-08-25; they were not re-retrieved this session. **[apo]** — the method
is sequence-only, so it satisfies C1 and C2 exactly.

**The reproduction failures. Both are direct, both used double-mutant cycles.**

Fodor & Aldrich tested correlated-mutation predictions against proteins with measured
double-mutant-cycle couplings and concluded: "We find that correlated mutation algorithms can
find residue pairs that are physically close and that physically close residue pairs tend to
be thermodynamically coupled. **We find little evidence, however, for the hypothesis that
thermodynamic coupling is limited to the subset of evolutionarily constrained residue
positions**" [VERIFIED-ABSTRACT] (doi:10.1074/jbc.m402560200, PMID 15023994).

Chi et al. re-measured the PDZ network itself: "We have reassessed the energetic coupling of
these residues by double mutant cycles together with ligand binding and stability experiments
and found that **coupling is not a special property of the coevolved network of residues** in
PDZ domains. **The observed coupling for ligand binding is better explained by a distance
relationship**, where residues close in space are more likely to couple than distal residues.
Our study demonstrates that statistical coupling from sequence analysis is not necessarily a
reporter of energetic coupling and allostery" [VERIFIED-ABSTRACT] (doi:10.1073/pnas.0711732105,
PMC2290805, PMID 18339805).

That second sentence is the same null we already face. File 06 §8 records that the ground
truth decays exponentially with distance and that `−distance` reaches AUC 0.617 on 73 curated
targets. Chi et al. found the same thing by mutagenesis in 2008.

**Two further methodological critiques.** Teşileanu, Colwell & Leibler showed that the
experimental support for sectors "involves almost exclusively proteins with a single sector",
where "sequence conservation is the dominating factor in SCA, and can alone be used to make
statistically equivalent functional predictions" [VERIFIED-ABSTRACT]
(doi:10.1371/journal.pcbi.1004091, PMC4344308). Dietler et al. added the phylogenetic
confound: "correlations in amino-acid usage can also arise from the mere fact that homologous
sequences share common ancestry" [VERIFIED-ABSTRACT] (doi:10.1371/journal.pcbi.1012091,
PMC11449291).

**The defence.** Salinas & Ranganathan argued from a comprehensive experimental coupling
dataset that "the pattern of amino acid coupling is quantitatively captured in the coevolution
of amino acid positions, especially as indicated by the statistical coupling analysis (SCA)"
[VERIFIED-ABSTRACT] (doi:10.7554/elife.34300, PMC6117156). The debate is not settled by a
knockout on either side; it is settled by whether SCA beats a conservation control, and that
control is rarely reported.

**A context effect that undermines the transferability of any PDZ network.** Laursen et al.
found that "allosteric networks in a PDZ domain are highly dependent on the supertertiary
structure" [VERIFIED-ABSTRACT] (doi:10.1073/pnas.2007201117, PMC7533695). The same domain
sequence has different coupling depending on what it is attached to. A separate review notes
that "some of the most consistently identified allosteric residues within PTP-BL PDZ2 and
PSD-95 PDZ3 domains are evolutionarily conserved" [VERIFIED-ABSTRACT]
(doi:10.3390/ijms23031454, PMC8836106) — which is the Teşileanu point restated as agreement.

### The graph signature this predicts

Two signatures, and the evidence separates them.

**Supported:** a _sparse connected subgraph_ whose members are conserved and which contains
both functional sites. That is the sector claim minus the coupling claim, and it survives all
four critiques, because conservation is what the critiques say is doing the work. **[apo]**,
sequence-only.

**Not supported:** the same subgraph as an _energetic_ pathway with couplings above what
proximity predicts. Two independent double-mutant-cycle studies found the coupling is
explained by distance.

**Operational consequence.** Any sector-flavoured feature enters our pipeline with two
mandatory controls: a plain-conservation control and a distance control. Without both, a
positive result is uninterpretable. This is a stronger requirement than file 06 §6 states,
because §6 had only the Teşileanu critique; the Chi and Fodor results add a direct
experimental refutation of the energetic reading.

---

## 3. Protein kinases: the spines are literally a contact chain, so say exactly what detects them

**The regulatory spine, as originally defined.** Surface comparison across serine-threonine
and tyrosine kinases found "a set of 30 residues whose spatial positions are highly conserved"
and, among them, that "the most important feature of the activation is a 'spine' formation
that is dynamically assembled in all active kinases. The spine is comprised of **four
hydrophobic residues** that we detected in a set of **23 eukaryotic and prokaryotic kinases**.
It spans the molecule and plays a coordinating role in activated kinases. **The spine is
disordered in the inactive kinases**" [VERIFIED-ABSTRACT] (doi:10.1073/pnas.0607656103,
PMC1693824). The four are now conventionally named RS1–RS4 [VERIFIED-ABSTRACT]
(doi:10.1042/bst20210837, PMID 35226061).

**The second spine and the scaffold.** A follow-up found further "conserved motifs comprised
mostly of hydrophobic residues. These residues are **scattered throughout the protein sequence
and thus were not previously detected by traditional methods**. These motifs traverse the
conserved protein kinase core and play integrating and regulatory roles. They are anchored to
the F-helix, which acts as an organizing 'hub'" [VERIFIED-ABSTRACT]
(doi:10.1073/pnas.0807988105, PMC2533684). Two properties matter for us: hydrophobic, and
non-contiguous in sequence. A contact graph sees both; a sequence method sees neither.

**The catalytic spine is completed by the ligand.** Work on C-spine mutations leverages "the
structural role of ATP in assembling the catalytic spine" [VERIFIED-ABSTRACT]
(doi:10.1016/j.jbc.2025.110921, PMC12721161). C-spine completeness is therefore **[holo]** —
in an apo kinase the chain has a nucleotide-sized hole in it by construction. The R-spine does
not depend on the ligand and is **[apo]**, but see the twist below.

**αC-helix in/out.** RS3, one of the four spine residues, "is at the C-terminus of the
αC-Helix" [VERIFIED-ABSTRACT] (doi:10.1016/j.bbapap.2015.04.007, PMC4577442). The αC
in-to-out rotation therefore moves a spine element, which is why αC position and spine
assembly are two descriptions of the same event. The loop connecting αC to β4 is itself a
communication element: mutation there disrupts "communication between the N- and C-lobes"
[VERIFIED-ABSTRACT] (doi:10.7554/elife.91980, PMC11616992). αC-in versus αC-out is **[holo]**
as a classification; the residues forming the αC packing environment are **[apo]**.

**The dynamic reading, which is what a graph can express.** Kornev & Taylor: "Active kinases
reveal a dynamic pattern with residues clustering into **semirigid communities** that move in
μs-ms timescale. Dynamics is proposed to be the underlying mechanism for allosteric regulation
in protein kinases" [VERIFIED-ABSTRACT] (doi:10.1016/j.tibs.2015.09.002, PMC4630092). The
spine is the thing that couples the communities.

**The ABL myristoyl-pocket lineage, in order.** Autoinhibited c-Abl: "The N-terminal myristoyl
modification of c-Abl 1b binds to the kinase domain and induces conformational changes that
allow the SH2 and SH3 domains to dock onto it" [VERIFIED-ABSTRACT]
(doi:10.1016/s0092-8674(03)00194-6, PMID 12654251). A synthetic ligand for the same pocket:
GNF-2 "binds to the myristate-binding site of Abl, leading to **changes in the structural
dynamics of the ATP-binding site**", shown by NMR, crystallography, mutagenesis and HDX-MS
[VERIFIED-ABSTRACT] (doi:10.1038/nature08675, PMC2901986). The clinical endpoint: "ABL001
binds to the myristoyl pocket of ABL1 and **induces the formation of an inactive kinase
conformation**", with a resistance-mutation spectrum disjoint from that of catalytic-site
inhibitors [VERIFIED-ABSTRACT] (doi:10.1038/nature21702, PMID 28329763). A residue-level
transmission path from the pocket has since been proposed from simulation
[VERIFIED-ABSTRACT] (doi:10.7554/eLife.85216, PMC10619977) — MD-derived, so **C2-violating as
published**.

**The negative result that should temper expectations.** A dual protein-language-model plus
frustration study over **453 kinase structures** found that "orthosteric sites exhibit high
predictability while distal allosteric sites remain poorly resolved", with allosteric sites
sitting in "neutrally frustrated zones, producing diffuse and context-dependent predictions"
[VERIFIED-ABSTRACT] (doi:10.1002/pro.70714, PMID 42423121). This matches file 06's record that
protein language models collapse on allosteric sites (AUPR 0.06).

### The graph signature this predicts

The R-spine is the cleanest structural rule in this file, because it is a _literal path in a
contact graph_: four buried hydrophobic residues, non-contiguous in sequence, in mutual
contact, spanning the two lobes.

**The naive detector, and why it fails on our input.** "Find the longest buried hydrophobic
contact chain and score its members" would work on an _active_ kinase. Our input is apo, and
apo kinases are usually inactive, and Kornev's own sentence is "the spine is disordered in the
inactive kinases". Run the naive detector on an apo inactive kinase and it returns a **broken**
chain.

**The detector that follows from that.** Score the **gap**, not the chain. **[apo]**

```
H  = residues with hydrophobic side chain AND relative SASA < 0.25
G_H= graph on H, edge if min side-chain heavy-atom distance <= 5.0 A
C  = connected components of G_H with >= 3 members and sequence span >= 20
score(i) = 1 if i lies on a shortest path between the two most separated
           members of the largest component in C, PLUS
           1 if i is within 8 A of a second component in C   # gap / bridge residue
```

Three properties make this worth testing. It is zero-parameter apart from two cutoffs. It is
not a proximity ranker, so it is not pre-refuted by file 06 §8. And it predicts something
falsifiable: the residues that _would complete_ the broken chain should be enriched for
allosteric hits, because completing the chain is what activation does.

**A second, weaker signature.** The F-helix acts as an "organizing hub" for spine anchoring.
In graph terms: a secondary-structure element whose residues have unusually high degree
_to residues in other secondary-structure elements_. Cheap to compute, **[apo]**, and it must
be run against a degree-preserving null, because "high degree" is exactly the buried-and-central
trap named in `docs/FIELD.md` §3.

---

## 4. Small GTPases: switch ordering, and why a covalent ligand two switches away controls nucleotide preference

**The switches are order-disorder elements, not moving parts.** In a switch I point mutant of
Ras, "whereas the overall structure is very similar to wildtype, **residues from switch I are
completely invisible**, indicating that the effector loop region is highly mobile". ³¹P-NMR
resolves "an equilibrium between two rapidly interconverting conformations", state 1 and
state 2, with effector-competent state 2 the minority in the mutants [VERIFIED-ABSTRACT]
(doi:10.1073/pnas.081441398, PMC33143). The load-bearing sentence for us: "minor changes in the
switch region, such as removing the side chain methyl group of Thr-35, drastically affect
dynamic behavior". A single side-chain methyl controls a two-state equilibrium. **[apo]** in the
sense that the disorder is visible in an unbound structure as missing density and high
B-factors.

**Distal control of switch ordering is documented on apo-like structures.** A crystal of
wild-type Ras with calcium acetate bound at a site remote from the active site produced "a shift
in helix 3/loop 7 and **a network of H-bonding interactions that propagates across the
molecule**, culminating in the ordering of switch II" [VERIFIED-ABSTRACT]
(doi:10.1073/pnas.0912226107, PMC2841912). This is a real long-range coupling in a GTPase,
established structurally. **[holo]** with respect to the acetate; the propagating H-bond network
itself is a contact-graph object.

**The switch-II pocket is cryptic in the strict `CONTEXT.md` sense.** Ostrem et al., on their
own structures: "This fully formed pocket is **not apparent in other published structures of
Ras**, although a groove is visible in some cases" [VERIFIED-FULLTEXT] (PMC4274051,
doi:10.1038/nature12796). And the reason it is absent: "In the active state of Ras, residues
from switch-II **entirely fill** the S-IIP" [VERIFIED-FULLTEXT] (PMC4274051). The pocket and
the active conformation are mutually exclusive occupancies of the same volume. **[holo]** —
the pocket cannot be found by a geometric detector on an apo structure, because it is not
there.

**The mechanism of action at a distance, stated by the primary source.** Three linked
observations [VERIFIED-FULLTEXT] (PMC4274051):

1. The compounds occupy the position that a switch-II glycine requires in the active
   conformation, and displace it, "with larger distances correlating with disordering of
   switch-I".
2. "Many of our structures with carbon-based electrophiles show **disordering of switch-I and
   a lack of density for the metal ion**."
3. The thermodynamic readout: untreated K-Ras(G12C) has a "slight preference for GTP (relative
   affinity 0.6 ± 0.2)"; with the covalent compounds, "GTP affinity is significantly decreased
   relative to GDP (relative affinity 3.9 ± 0.6 (8) and 3.5 ± 0.8 (12))". That is a shift of
   roughly six-fold in nucleotide preference, driven from a pocket the ligand had to create.

**The chemical bookkeeping of that shift.** A later biophysical study makes the competition
explicit: a loss of affinity for the GTP analogue arises "due in part to rearrangements in
switch-II, where **the hydrogen bond between** a switch-II glycine **and the γ-phosphate needs
to break to form the switch-II pocket**" [VERIFIED-ABSTRACT] (doi:10.1016/j.jbc.2025.110331,
PMC12270674). The allosteric coupling is a single hydrogen bond that two states compete for.
Occupying the pocket costs that bond, and the bond is worth more to GTP than to GDP.

**The pocket is engageable reversibly and in cells**, so it is not a covalent artefact
[VERIFIED-ABSTRACT] (doi:10.1038/s41589-022-00985-w, PMC9135634), and a monobody has trapped it
"in the most widely open form reported to date" [VERIFIED-ABSTRACT]
(doi:10.1073/pnas.2302485120, PMC10334749). A 2026 review surveys the recent Ras allostery
literature [VERIFIED-ABSTRACT] (doi:10.1016/j.sbi.2025.103183, PMC12890071).

**Cryptic is not allosteric, and the base rates say so.** Cryptic pockets "exist in the
ligand-bound state of a protein but not in its apo form" [VERIFIED-ABSTRACT]
(doi:10.1093/bioadv/vbaf156, PMC12342141), and a 2026 survey puts them at "~18% of protein
clusters" [VERIFIED-ABSTRACT] (doi:10.1126/sciadv.ady6364, PMC13267282; the preprint version
reports 16.3%, doi:10.1101/2025.04.23.650184). `CONTEXT.md` already fixes the distinction. The
switch-II pocket happens to be both, which makes it a hard case, not a typical one.

### The graph signature this predicts

The switch-II pocket is the worst case for a geometry-first method and a fair case for a
topology-first one. Three **[apo]** signatures follow:

1. **Low-degree, high-variance loops adjacent to the active site.** Switch I and switch II are
   the regions with the fewest contacts per residue and the poorest density. Score a residue by
   `(expected contacts given burial) − (observed contacts)`, i.e. a coordination deficit. This
   is the "under-constrained corridor" observable that §8 finds independent support for.
2. **Edges incident on the active-site set whose removal opens a cavity.** The mechanism reduces
   to one hydrogen bond that the pocket and the nucleotide compete for. In graph terms: an edge
   `(u,v)` with `u` in the active-site set, whose deletion increases the size of the largest
   empty sphere in its neighbourhood. Computable on apo geometry without any holo input.
3. **Second-shell residues of a disordered loop.** The mechanism runs
   `pocket → switch II displacement → switch I disorder → metal loss`. The graph object is a
   short chain from the candidate to the metal-coordinating shell that passes through a
   low-coordination loop. Score = shortest-path length weighted by coordination deficit.

**What is forbidden.** Any feature computed on the pocket itself — its volume, its lining, its
druggability — is **[holo]** for this system, because the pocket does not exist in the apo
structure. Our `cavity_volume` baseline (conventions §6, item 2) will therefore _fail_ on
cases like this one by construction. That is a prediction, and it is worth recording before the
measurement rather than after.

---

## 5. Class A GPCRs: a conserved contact network, and an activation pathway defined as a contact _change_

**The fold has a conserved contact core.** A systematic analysis of high-resolution structures
"uncover[ed] a conserved network of non-covalent contacts that defines the GPCR fold"
[VERIFIED-ABSTRACT] (doi:10.1038/nature11896, PMID 23407534). The exact count of consensus
contacts is **[UNVERIFIED]** — the paper has no PMC record and the publisher page was not
reached this session. **[apo]**: the network is present in inactive structures.

**Activation is defined as a rearrangement of contacts, and it converges.** Across 27 GPCRs
with active, inactive, or both states: "Structural rearrangements of residue contacts in the
transmembrane domain serve as 'activation pathways' that connect the ligand-binding pocket to
the G-protein-coupling region... despite the diversity in activation pathways between
receptors, the pathways **converge near the G-protein-coupling region**. This convergence is
mediated by a highly conserved structural rearrangement of residue contacts between
transmembrane helices 3, 6 and 7" [VERIFIED-ABSTRACT] (doi:10.1038/nature19107, PMC5008462).
**[holo]** — it is a difference between two structures.

**The quantified version, and the numbers to use.** Analysing "the conformational changes in
**234 structures from 45 class A GPCRs**", Zhou et al. "discovered a common GPCR activation
pathway comprising of **34 residue pairs and 35 residues**. The pathway unifies previous
findings into a common activation mechanism and strings together the scattered key motifs such
as CWxP, DRY, Na⁺ pocket, NPxxY and PIF, thereby directly linking the bottom of ligand-binding
pocket with G-protein coupling region" [VERIFIED-ABSTRACT] (doi:10.7554/eLife.50279,
PMC6954041). Site-directed mutagenesis on that pathway produced constitutively active and
constitutively inactive receptors, so the set is causal, not merely correlated.

Thirty-five residues in a ~300-residue receptor is about 12%. File 06 records 42 major
allosteric sites out of 252 in the Src kinase domain, about 17%. Two unrelated folds, measured
by unrelated techniques, put the strongly-coupled minority at the same order of magnitude.

**The micro-switches are named consistently across the field**: the ionic lock, the Y–Y gate,
NPxxY, PIF and the Trp-Phe toggle [VERIFIED-ABSTRACT] (doi:10.1021/acsomega.5c12434,
PMC12947221); the CWxP toggle of TM6 "facilitates communication with NPxxY microswitch motif of
TM7" [VERIFIED-ABSTRACT] (doi:10.1016/j.jbc.2024.107948, PMC11625327). A 2026 study reports a
"hydration-mediated signal transduction network [that] bridges sodium-binding pocket, NPxxY and
DRY motifs" [VERIFIED-ABSTRACT] (doi:10.1371/journal.pbio.3003447, PMC13152116) — water again,
and C5 permits water only as simple nodes; file 06 §5 already rules against adding waters on
apo structures.

**Two orthogonal readouts on the same fold.** A rigidity-transmission analysis of the A₂A
receptor concluded that divalent cations "bridge specific extracellular acidic residues,
bringing TM5 and TM6 together at the extracellular surface and allosterically driving open the
G-protein-binding cleft" [VERIFIED-ABSTRACT] (doi:10.1038/s41467-018-03314-9, PMC5893540). A
frustration analysis of GPCR:G-protein complexes reports that interface residues "contain a
higher density of frustrated residues compared to other structural regions"
[VERIFIED-ABSTRACT] (doi:10.1021/acs.jcim.6c00203, PMID 42439392). A review frames the
mechanism as "allosteric communication pipelines" [VERIFIED-ABSTRACT]
(doi:10.1016/j.coph.2016.07.010, PMC5127785).

### The graph signature this predicts

**The trap first.** The GPCR literature's central object is a _set of residue pairs whose
contact status changes between two states_. That is the single most predictive feature class in
the field, and it is **[holo]** and therefore unusable. File 06 §12 reaches the same conclusion
independently from the Src mutational map, where "swapping" contacts carry the largest effects
and are C1-forbidden. Two independent literatures now say the best feature is the one we cannot
use. That should go in the report as a stated limitation, not be discovered by a judge.

**What survives, and it is not nothing.** Three **[apo]** signatures:

1. **Conserved-contact-motif membership.** The micro-switch positions are conserved and can be
   located on an apo structure by structural alignment to the fold, with no reference to an
   active-state structure. In graph terms: nodes belonging to a contact motif that recurs across
   the family. Cheap and family-specific — which means it does not generalise, and our benchmark
   spans unrelated folds.
2. **Inter-bundle boundary residues.** The activation pathway threads between helix bundles. A
   fold-agnostic version: partition the apo graph into modules (spectral clustering on the GNM
   correlation matrix), then score a residue by the number of distinct modules among its
   contacts. This is the §8 "module boundary" observable and it needs no family knowledge.
3. **Convergence toward a sink.** Diverse start points, one endpoint. That is exactly the
   structure a source-sink propagation observable expresses: seed at the active-site set and
   read the response everywhere else. It also predicts that the _score distribution_ should be
   funnel-shaped — many weakly-coupled distal residues, few strongly-coupled proximal ones —
   which is a diagnostic we can check without labels.

---

## 6. Myosin: a mechanical strain path, which is a different graph object from a diffusive path

**The coupling is an amplifying cascade along one helix.** Generating optimised intermediates
between the crystallographic end-states of the recovery stroke gave "a detailed structural model
for communication between the catalytic and the force-generating regions... The coupling is
achieved by an **amplifying cascade of conformational changes along the relay helix** lying
between the ATPase and the domain carrying the lever arm", with the lever arm rotating
"approximately 60 degrees" [VERIFIED-ABSTRACT] (doi:10.1073/pnas.0408784102, PMC1100758).
**[holo]** — it is a path computed between two crystal states.

**Normal-mode analysis of the same family names the graph object.** For the rigor to post-rigor
transition of myosin V: "**Rigid-body motions of the various subdomains and specific residues at
the subdomain interfaces** are key elements in the transition... The triggering event is the
change in the interaction of switch I and the P-loop... The motion of switch I, which is a
relatively rigid element of the U50 subdomain, leads directly to a partial opening of the
U50/L50 cleft", together with "partial untwisting of the central β-sheet" [VERIFIED-ABSTRACT]
(doi:10.1371/journal.pcbi.1000129, PMC2497441). The units of the mechanism are _rigid
subdomains_; the mechanism lives at their _interfaces_.

**The relay/SH1/converter chain is resolved as an ordered sequence.** An intermediate along the
myosin VI recovery stroke shows a "pretransition state where Relay/SH1 adopt postrecovery
conformation", with "lever arm repriming driven by thermal fluctuations" [VERIFIED-ABSTRACT]
(doi:10.1073/pnas.1711512115, PMC6004474). Simulation puts converter re-priming first, with
"weak coupling to ATP hydrolysis activation" [VERIFIED-ABSTRACT]
(doi:10.1371/journal.pcbi.1012005, PMC11086841). Mutation of a relay-region residue impairs an
"activation loop/relay helix communication pathway" affecting actin-activated phosphate release
[VERIFIED-ABSTRACT] (doi:10.1016/j.jbc.2026.113114, PMC13264367). Labelling the SH1 helix
"interferes with structural changes in the relay and SH1 helices required to generate the power
stroke" [VERIFIED-ABSTRACT] (doi:10.1007/s12551-026-01425-y, PMID 42620599).

**Strain, not diffusion, is the currency.** The force-generating ADP state shows a "9.5° rotation
of lever arm coupled to β-sheet rearrangement" underlying "strain-dependent ADP release"
[VERIFIED-ABSTRACT] (doi:10.1073/pnas.1516598113, PMC4822626). A comprehensive review frames
force generation around "strain-dependent mechanisms essential for processive myosins"
[VERIFIED-ABSTRACT] (doi:10.1021/acs.chemrev.9b00264, PMID 31689091). Time-resolved cryo-EM
resolves the power stroke as "rotation of the upper 50-kDa subdomain, closing the actin-binding
cleft" [VERIFIED-ABSTRACT] (doi:10.1038/s41586-025-08876-5, PMC12158783). A small-molecule
modulator "reduces conformational heterogeneity of the lever arm" in the pre-powerstroke state
[VERIFIED-ABSTRACT] (doi:10.3390/ijms251910425, PMC11477208) — a modulator that acts by
narrowing an ensemble, which is the Cooper-Dryden channel of file 06 §1.

**The general point, made independently.** Force distribution analysis on the methionine
repressor "directly monitored the propagation of internal forces through the MetJ structure"
rather than tracking conformational change, and recovered a strain network
[VERIFIED-ABSTRACT] (doi:10.1371/journal.pcbi.1000574, PMC2775130). MD-derived, so
**C2-violating as published**; the concept — that force takes different routes than
displacement or correlation — is what transfers.

### The graph signature this predicts

**A strain path and a diffusive path are different graph objects, and the difference is
concrete.**

- A **diffusive/information path** is a _high-conductance_ object. Many parallel routes, each
  contributing; the natural observable is effective resistance or a heat-kernel amplitude
  between two nodes. Adding an edge always helps. This is what a quantum or classical walk
  computes, and it is monotone in distance — which is why file 06 §8 predicts it will land on
  the `−distance` control.
- A **strain path** is a _series-constraint_ object. Force is transmitted through the stiffest
  connected chain, and a chain is only as stiff as its softest link. The natural observable is a
  **bottleneck** — the minimum stiffness along the best path — not a sum. Adding a _soft_ edge
  in parallel does nothing.

The implementable distinction, **[apo]**:

```
w[u,v] = stiffness of contact (u,v)          # e.g. 1/d^2, or a class weight
diffusive(i) = heat_kernel(L_w, t)[i, A]      # sums over walks; monotone in distance
strain(i)    = max over paths P from i to A of  min_{(u,v) in P} w[u,v]   # widest path
```

`strain` is computed by a Dijkstra variant with max-min relaxation, `O(E log V)`. It is _not_
monotone in distance: a distant residue linked by a stiff chain outranks a near residue behind
a soft one. That property is the reason to test it. It is also the graph statement of Fischer's
"cascade along the relay helix" and of Cecchini's "rigid subdomains coupled at their
interfaces".

**Second signature, and it is the same one haemoglobin and the GPCRs gave.** The mechanism is
carried by residues _at subdomain interfaces_. Rigid-module decomposition of the apo graph, then
score by module-boundary participation. Three unrelated systems now point at this observable.

**A caution specific to motors.** Myosin's coupling is a genuine mechanical lever with a
directional output. Most of our targets are not motors. A widest-path observable is being
proposed here as a general alternative to walk-summing, not on the claim that every allosteric
protein is a machine.

---

## 7. Four enzymes with well-mapped communication

### 7.1 Aspartate transcarbamoylase — the quaternary transition, quantified

The T → R transition is "an elongation of 11 Å along the molecular three-fold axis", "a rotation
of one catalytic trimer c3 relative to the other c3 by 12°", "a rotation of each of the three
regulatory dimers about the approximate two-fold axes by 15°", and domain closure within each
catalytic chain "by 6.8°" [VERIFIED-FULLTEXT] (PMC3276696, doi:10.1021/ar200166p). **[holo]**
for the transition; the domain and subunit boundaries themselves are **[apo]**.

The mechanical interlock is explicit and is the single most graph-like sentence in the ATCase
literature: "the 240's loops cannot attain their final domain-closed conformation without an
expansion of the enzyme along the three-fold axis, which allow the 240's loops from the upper
and lower catalytic subunits **to slide past each other**" [VERIFIED-FULLTEXT] (PMC3276696).
Two loops occupy overlapping volume in the T state. The coupling is steric exclusion between
two specific structural elements — the same logic as the Ras switch-II pocket in §4.

Two results complicate the two-state picture. The enzyme has "a preexisting equilibrium between
low-activity and high-activity quaternary structure states **in the absence of substrates**"
[VERIFIED-ABSTRACT] (doi:10.1073/pnas.0607641104, PMC1766413), and a mutant has been trapped
"in an intermediate quaternary structure between the canonical T and R structures"
[VERIFIED-ABSTRACT] (doi:10.1073/pnas.1119683109, PMC3356622). More importantly for the
regulatory pathway, "the effects of ATP or CTP binding **do not require** the quaternary
conformational transition" [VERIFIED-FULLTEXT] (PMC3276696) — heterotropic regulation over
~60 Å runs through a route that is not the T → R switch. A 2026 study proposes a global reading:
"ATCase behaves like a flexible balloon whose global 'breathing' motions directly regulate
activity" [VERIFIED-ABSTRACT] (doi:10.1038/s41467-026-70909-y, PMC13168310).

### 7.2 Glucokinase — a slow transition, and disorder as the carrier

Glucokinase is monomeric with one glucose site and still shows sigmoidal kinetics. The crystal
structures showed "global conformational change, including domain reorganization", supporting a
mnemonical rather than a concerted mechanism, and "revealed an allosteric site through which
small molecules may modulate kinetic properties" [VERIFIED-ABSTRACT]
(doi:10.1016/j.str.2004.02.005, PMID 15016359). **[holo]** for the reorganisation; the allosteric
site is a real cleft in the unliganded enzyme, so its geometry is **[apo]**.

The mechanism is order-disorder, not displacement: NMR showed "large-scale, glucose-mediated
disorder-order transitions", with the small domain of unliganded glucokinase "intrinsically
disordered, sampling broad conformational states", and cooperativity arising from millisecond
disorder-order cycling acting as a time-delay at low glucose [VERIFIED-ABSTRACT]
(doi:10.1371/journal.pbio.1001452, PMC3525530). **The disorder is a property of the apo state**,
which makes this the most directly apo-observable mechanism in the file. Two activation modes
follow: "α-type activation increases glucose affinity and suppresses loop proteolytic
susceptibility; β-type activation leaves glucose affinity largely unchanged while enhancing loop
susceptibility", localised to "a 30-residue active-site loop" [VERIFIED-ABSTRACT]
(doi:10.1073/pnas.1506664112, PMC4577146). A variant map found hypoactive variants concentrated
"at sites critical for conformational dynamics" [VERIFIED-ABSTRACT]
(doi:10.1186/s13059-023-02935-8, PMC10131484); a review states that the kinetic properties "are
intrinsically linked to the enzyme's conformational dynamics" [VERIFIED-ABSTRACT]
(doi:10.1016/j.tibs.2024.12.007, PMID 39753435).

### 7.3 Dihydrofolate reductase — a coupled network, contested in the same way as PDZ

The original claim: "a network of coupled promoting motions in dihydrofolate reductase spanning
femtosecond to millisecond timescales", with "broad implications for an expanded role of the
protein fold in catalysis" including "understanding distal drug action mechanisms"
[VERIFIED-ABSTRACT] (doi:10.1073/pnas.052005999, PMC122427). Simulation-derived, so
**C2-violating as an input**.

The structural-rule version: comprehensive mutagenesis of DHFR surfaces showed that
"sector-connected surface sites are preferred locations for allosteric control emergence",
with sectors as "sparse networks of physically contiguous and coevolving amino acids"
[VERIFIED-ABSTRACT] (doi:10.1016/j.cell.2011.10.049, PMC3414429). This is the most direct
experimental test of the sector hypothesis as a _predictor of where allostery can be installed_,
and it is positive — which must be weighed against the PDZ reproduction failures in §2.

An ENM-based reading gives the property we most want: "certain distal residues **control** the
dynamics of the M20 and FG loops while others are **controlled by** them" [VERIFIED-ABSTRACT]
(doi:10.1002/pro.4700, PMID 37313628). A directional, asymmetric readout derived from a
flexibility model rather than a trajectory. It is the C2-compatible cousin of the transfer-entropy
route in file 06 §10. Separately, SCA-identified coevolving residues in DHFR show "increased
correlated motions", with allosteric communication knocked down in mutants
[VERIFIED-ABSTRACT] (doi:10.1021/acs.jpcb.4c04195, PMC11514014).

### 7.4 Imidazole glycerol phosphate synthase — and the single most useful control experiment in this file

IGPS couples an effector site on HisF to a glutaminase active site on HisH across a domain
interface. Community analysis of dynamical networks identified "allosteric pathways [that]
involve conserved residues that correlate motion of the PRFAR binding loop to motion at the
protein-protein interface" [VERIFIED-ABSTRACT] (doi:10.1073/pnas.1120536109, PMC3365145). An
interdomain salt bridge "plays a key role in mediating communication between the two active
sites" [VERIFIED-ABSTRACT] (doi:10.1021/bi050706b, PMID 16142895), and signal transduction from
HisF to HisH "involves the closing of the cyclase:glutaminase subunit interface"
[VERIFIED-ABSTRACT] (doi:10.1021/acs.biochem.0c00332, PMID 32633500). NMR shows the apo enzyme is
the _more_ flexible state on the millisecond timescale as temperature rises
[VERIFIED-ABSTRACT] (doi:10.3389/fmolb.2018.00004, PMC5808140). The pathway is druggable:
"enzymatic activity can be impaired by small molecules that bind along the allosteric pathway
connecting orthosteric and allosteric sites" [VERIFIED-ABSTRACT]
(doi:10.1021/acs.biochem.6b00859, PMC5283573).

**The control experiment.** Maschietto et al. found that "a temperature increase triggers a
cascade of local amino acid-to-amino acid dynamics that **remarkably resembles the allosteric
activation upon effector binding**" [VERIFIED-ABSTRACT] (doi:10.1038/s41467-023-37956-1,
PMC10115891). A _non-specific, chemically featureless_ perturbation reproduces the effector's
pathway. That is the strongest single justification retrieved this session for the whole class
of "perturb the network and read the response" observables: the pathway is a property of the
structure, not of the ligand's chemistry. It is also the justification for using a generic
source term at the active site instead of modelling an effector.

### The graph signature these four predict

All four converge on the same two objects, and both are **[apo]**.

1. **A boundary between two rigid modules that separates the two sites.** ATCase: catalytic
   trimer against regulatory dimer, plus intra-chain domain closure. Glucokinase: large domain
   against a disordered small domain. IGPS: the HisF:HisH interface. DHFR: the M20 and FG loops
   against the core. Definition: partition the apo contact graph into modules; score a residue by
   how many distinct modules it contacts, weighted by module rigidity. This is now supported by
   six of the seven systems in this file.

2. **A coordination deficit — regions with fewer contacts than their burial predicts.** ATCase's
   240s loops must slide past each other, so the volume between them is under-packed in one
   state. Glucokinase's small domain is intrinsically disordered in the apo enzyme. IGPS's apo
   state is the flexible one. DHFR's control residues act on loops. Definition: weighted contact
   number `WCN_i = Σ_{j≠i} 1/d_ij²`, z-scored within a burial bin; negative z means under-packed.

One further, weaker signature from IGPS and DHFR: **a single salt bridge or hydrogen bond at a
module boundary can be the whole coupling**. That argues for a per-edge importance score
(betweenness on edges, or min-cut participation) rather than a per-node one, at least as a
secondary output.

---

## 8. Is there a structure-only signature that holds across systems?

Five candidates were named in the brief. Each is assessed on: how many independent systems
support it, whether anyone measured it across many proteins, the effect size, and whether it is
**[apo]**.

### 8.1 The residue is in a rigid cluster spanning both sites

**The method exists.** Rigidity transmission allostery (RTA) uses graph rigidity (pebble-game
style) to test whether rigidifying a candidate site propagates to a target site. "The RTA
algorithm is computationally very fast and can rapidly scan many unknown sites for allosteric
transmission" [VERIFIED-ABSTRACT] (doi:10.1007/978-1-0716-1154-8_5, PMID 33315218). It has been
applied to the A₂A receptor [VERIFIED-ABSTRACT] (doi:10.1038/s41467-018-03314-9, PMC5893540), to
a nickel-responsive transcription factor, where "nickel binding increases protein rigidity to
slow down the conformational exchange" [VERIFIED-ABSTRACT] (doi:10.1016/j.jbc.2022.102785,
PMC9860126), to a dehalogenase [VERIFIED-ABSTRACT] (doi:10.1039/d4cb00176a, PMC11465415), and to
remote loop evolution in chitinases [VERIFIED-ABSTRACT] (doi:10.1038/s41467-024-47588-8,
PMC11018821).

**Effect size across many proteins: not retrieved by the recorded search.** Every retrieved
application is a single-system case study. Per ADR 0019 this is recorded as "not retrieved",
not as absence of prior art.

**Verdict:** mechanistically the closest match to C6, **[apo]**, and the least quantified.
Worth building because it is cheap, but it cannot be justified by a published effect size.

### 8.2 The residue is a bottleneck on the shortest path

**Measured across families, but usually against the wrong positive class.** Residues "crucial for
maintaining short paths" were identified across **seven protein families** and argued to mediate
allosteric communication; "centrally conserved residues, whose removal increases the
characteristic path length in protein networks, may relate to the system fragility"
[VERIFIED-ABSTRACT] (doi:10.1038/msb4100063, PMC1681495). In the companion interface study,
"**83%** of these predicted highly central residues... correspond to or are in direct contact
with an experimentally annotated hot spot" [VERIFIED-ABSTRACT] (doi:10.1002/prot.20348,
PMID 15617065) — but the positive class there is a _protein-protein interface hot spot_, not an
allosteric site, so the number is not comparable to ours (conventions §2).

**The confound is explicit in the founding paper.** Converting structures to interaction graphs
showed that "active site, ligand-binding and evolutionary conserved residues typically have high
closeness values" [VERIFIED-ABSTRACT] (doi:10.1016/j.jmb.2004.10.055, PMID 15544817). Closeness
centrality finds the **active site**. That is the buried-and-central trap named in
`docs/FIELD.md` §3, and it is why file 06 §12 could not separate a topology invariant from degree
and burial. Betweenness remains in active use for mediator identification, for example in a CAP
case study [VERIFIED-ABSTRACT] (doi:10.1016/j.jmb.2023.168395, PMC10851786).

**Verdict:** **[apo]**, cheap, and largely already spent. It is a strong detector of the site we
are propagating _from_, and a weak detector of the site we are propagating _to_. Keep it as a
control, not as a candidate.

### 8.3 The residue is at a hinge between two rigid domains

**This is the best-measured apo-compatible candidate.** PARS started from **213 allosteric
proteins**, filtered to **91 non-redundant** entries, and observed "significant flexibility
changes in 70% of cases" on ligand binding. Predicting allosteric sites from normal-mode
flexibility change gave "**65% positive predictive value** in identifying allosteric sites" at
0.22 sensitivity under stricter parameters [VERIFIED-ABSTRACT] (doi:10.1186/1471-2105-13-273,
PMC3562710).

**Binding leverage is the companion measure and is single-structure.** "Both catalytic and
allosteric sites typically display high binding leverage", and the metric is calculable from one
structure [VERIFIED-ABSTRACT] (doi:10.1371/journal.pcbi.1002148, PMC3174156). The same paper
reports its own negative case: for CAP, regulation runs "through motions distinct from
high-leverage sites". The mechanism that file 06 §2 identifies as the purest entropic allostery
is the one binding leverage misses.

**Systems supporting a hinge/module-boundary reading in this file:** haemoglobin (§1), kinases
(§3, lobe boundary), GPCRs (§5, inter-bundle), myosin (§6, subdomain interfaces), ATCase,
glucokinase, IGPS, DHFR (§7). Eight of the seven sections, counting §7's four enzymes
separately — this is the single most widely supported signature in the file.

**Verdict:** **[apo]**, supported by the most systems and by the only allosteric-site-specific
effect size retrieved. Low sensitivity (0.22) is the honest ceiling.

### 8.4 The residue sits on a chain of hydrophobic contacts

**Two independent fold families, each with a named spine.** Protein kinases: four hydrophobic
residues spanning the molecule, detected across **23 kinases** [VERIFIED-ABSTRACT]
(doi:10.1073/pnas.0607656103, PMC1693824). TetR-like regulators: a bacterial acyl-CoA sensor
"senses long fatty acyl-CoA through a tunnel and **a hydrophobic transmission spine**", and "a
transmission spine is conserved in a **large number of TetR-like regulators**"
[VERIFIED-ABSTRACT] (doi:10.1038/s41467-020-17504-x, PMC7382501).

**Plus the burial statistic already in file 06:** buried core positions (rSASA < 0.25) are the
strongest single correlate of a conserved allosteric hotspot across five homologous domains,
OR = 8.91, P < 2.2 × 10⁻¹⁶ (doi:10.1101/2025.06.20.660748).

**What is missing.** No paper was retrieved that evaluates "hydrophobic contact chain membership"
as a _predictor_ on an allosteric-site benchmark. The evidence is that spines exist and that
burial is enriched; the composite feature has not been scored.

**Verdict:** **[apo]** and mechanistically the most specific rule in the file, with the
apo-specific twist from §3 that the informative residues are the ones bridging the _gap_ in a
broken chain. Untested as a predictor.

### 8.5 The residue has anomalous packing

**Two literatures, and they disagree about the sign.**

_Frustration is enriched at catalytic sites._ A survey of **907 nonredundant enzyme entries**
from the Catalytic Site Atlas found two shells of enriched frustration around catalytic
residues — one at ≈1 Å (the catalytic residues' own interactions) and "a second peak between
2 Å and 3.5 Å, which comprises interactions between residues that coordinate the catalytic
residues" — with "both neutral and highly frustrated interactions... enriched in these shells
compared with the overall contacts distribution", and local frustration "evolutionarily more
conserved than the primary structure itself" [VERIFIED-FULLTEXT] (PMC6410768,
doi:10.1073/pnas.1819859116). **No explicit odds ratio or p-value appears in the retrieved
text**, and the positive class is the _catalytic_ site.

_Allosteric sites are reported as neutrally frustrated._ Over **453 kinase structures**,
allosteric sites reside in "neutrally frustrated zones, producing diffuse and context-dependent
predictions" [VERIFIED-ABSTRACT] (doi:10.1002/pro.70714, PMID 42423121). A separate
machine-learning study reports that "allosteric pockets occupy predominantly neutrally
frustrated zones associated with conformational plasticity and reduced evolutionary constraint"
[VERIFIED-ABSTRACT] (doi:10.1021/acs.jctc.6c00427, PMC13217555).

_But one study reports the opposite for GPCR interfaces_: allosteric sites "show higher density
of frustrated residues compared to other structural regions" [VERIFIED-ABSTRACT]
(doi:10.1021/acs.jcim.6c00203, PMID 42439392).

**The contradiction is real and should be reported as such.** "Neutrally frustrated" and "high
frustration density" are different claims. The two are reconcilable only if the GPCR result is
measured against a different background. Not resolvable from abstracts.

**A cleaner and independent version of the same idea comes from physics, not biochemistry.** In
silico evolution of elastic networks for an allosteric task found that "functioning materials
evolve **a less-constrained trumpet-shaped region** connecting the stimulus and active sites",
that the response amplitude "varies nonmonotonically along the trumpet", and that the success of
the architecture "stems from the emergence of **soft edge modes**... near the surface of
marginally connected materials" [VERIFIED-ABSTRACT] (doi:10.1073/pnas.1615536114, PMC5347607).
Independently, an allosteric strain response can be tuned between arbitrary node pairs in a
disordered spring network "by removing only **∼1% of the bonds**", and long-range coupled
mechanical responses are "similarly easy to achieve in disordered networks"
[VERIFIED-ABSTRACT] (doi:10.1073/pnas.1612139114, PMC5347623).

These two are the most directly usable results in this file, because they are pure elastic
networks — exactly C6 — and they say two things at once. **The coupling corridor is
under-constrained, not over-constrained.** And **the signal is sparse**: 1% of bonds is enough.

**Verdict:** **[apo]**. Supported by mechanical-network theory (2 papers), by frustration
analyses on 453 kinases and on allosteric-pocket datasets (2 papers, with 1 dissenting), by the
disorder mechanisms in glucokinase and small GTPases, and by our own `cavity_volume` baseline
rejecting the null on all three confirmatory arms (conventions §6). It also _contradicts_ 8.2:
a bottleneck is a constraint, a soft corridor is the absence of one.

### 8.6 The one candidate with real cross-protein numbers: perturbation-response propagation

Not in the brief's list, but it is the only family with head-to-head benchmark numbers.

**Bond-to-bond propensity.** An energy-weighted atomistic graph, a propensity "quantifying the
non-local effect of instantaneous bond fluctuations propagating through the protein", and
significance by quantile regression against "a reference set of **100 protein structures from
the SCOP database**". Result on the test set: "The allosteric site is detected significantly by
at least one of the four measures in **19 out of 20** proteins in the test set, and is detected
by three or more of the four measures in **15 out of 20**." For caspase-1, "residues within
3.5 Å of the allosteric inhibitor have significantly higher propensities than non-allosteric
residues (Wilcoxon rank sum, **P < 0.0005**)" [VERIFIED-FULLTEXT] (PMC5007447,
doi:10.1038/ncomms12477).

**Ohm.** A structure-only perturbation-propagation method on the same 20-protein class of
benchmark: "**Ohm relies solely on the structure of the protein of interest**". "The average TPR
of Ohm is **0.57**, compared to **0.23** of Amor's method"; "The PPV of Ohm is **0.72**, compared
to **0.48** of Amor's method" [VERIFIED-FULLTEXT] (PMC7395124, doi:10.1038/s41467-020-17618-2).
The authors also address the unbound case directly: "we recommend to use all residues on the
active site for the unbound structure."

**AlloSigMA.** A harmonic model plus normal modes in a statistical-mechanical framework, where
"the entropic contribution to allosteric free energy of a residue is directly calculated",
"tested on a variety of allosteric proteins, heterogeneous in terms of size, topology and degree
of oligomerization" [VERIFIED-ABSTRACT] (doi:10.1371/journal.pcbi.1004678, PMC4777440).

**Four caveats, and they are large.** (i) The benchmarks are 20 proteins. (ii) They are not
leakage-controlled; conventions §6 records that AlloBench's leakage-controlled reappraisal put
every one of eight tools below 60% even at a very low Jaccard cutoff. (iii) A reimplementation
gap is visible inside the evidence itself — Amor's method scores 0.23 TPR when re-measured by
Ohm's authors. (iv) None of the three reports an apo-versus-holo split, which is the axis we are
scored on.

**Verdict:** **[apo]** in principle, best-quantified in practice, and the numbers should not be
believed at face value.

### 8.7 Summary table

| Signature                                   | Independent systems in this file                             | Cross-protein measurement retrieved                       | Effect size                                | Apo?                   |
| ------------------------------------------- | ------------------------------------------------------------ | --------------------------------------------------------- | ------------------------------------------ | ---------------------- |
| Module/hinge boundary between rigid domains | 8 (Hb, kinase, GTPase, GPCR, myosin, ATCase, GCK, IGPS/DHFR) | 91 non-redundant proteins (PARS)                          | PPV 0.65, sensitivity 0.22                 | **[apo]**              |
| Coordination deficit / soft corridor        | 6 (GTPase, GCK, IGPS, kinase, GPCR, ATCase)                  | elastic-network theory; 453 kinases; allosteric-pocket ML | qualitative; "∼1% of bonds"; sign disputed | **[apo]**              |
| Perturbation-response propagation           | all 7, as the underlying picture                             | 20 proteins (×2 methods), 100-protein null                | TPR 0.57 / PPV 0.72; 19/20                 | **[apo]**              |
| Buried non-contiguous hydrophobic chain     | 2 folds + burial statistic                                   | 23 kinases; TetR-like family; OR 8.91 for burial          | not scored as a predictor                  | **[apo]**              |
| Rigid cluster spanning both sites (RTA)     | 4 case studies                                               | none retrieved                                            | not retrieved                              | **[apo]**              |
| Shortest-path bottleneck / centrality       | 7 families (del Sol)                                         | 7 families; 83% on interface hot spots                    | wrong positive class                       | **[apo]**              |
| Contact-status change between two states    | 3 (GPCR, kinase spine, GTPase switch)                        | 234 structures / 45 GPCRs → 35 residues                   | causal by mutagenesis                      | **[holo] — forbidden** |

---

## What this changes for our pipeline

Observables ranked by the number of _independent systems_ in this file that support them, with an
implementable definition for each. All graphs are the apo residue contact graph `G`; `A` is the
named active-site set; `d_ij` is the minimum heavy-atom distance between residues.

**1. Module-boundary score — 8 systems. `network/` + `classical/`. [apo]**

Every system here decomposes into rigid units coupled at their interfaces: Hb's dimers, the
kinase lobes, myosin's subdomains, ATCase's trimers and closing domains, glucokinase's two
domains, the HisF:HisH interface, DHFR's loops.

```
C = correlation matrix of the GNM built on G           # apo only, no MD
M = spectral_clustering(C, k)                          # k from the slow-mode spectrum gap
score[i] = |{ M[j] : j in neighbours(i) }| - 1         # how many modules i touches
score[i] *= mode_amplitude_gap(M[a], M[b])             # weight by how rigid the modules are
```

Published anchor: PPV 0.65 at sensitivity 0.22 over 91 non-redundant proteins
(doi:10.1186/1471-2105-13-273). Must be run against a degree-preserving null: high module
contact and high degree are correlated.

**2. Coordination-deficit corridor — 6 systems. `network/`. [apo]**

Elastic-network evolution says the corridor is _less_ constrained
(doi:10.1073/pnas.1615536114); frustration analyses put allosteric sites in neutrally frustrated
zones (doi:10.1002/pro.70714, doi:10.1021/acs.jctc.6c00427); glucokinase's small domain and the
GTPase switches are disordered in the apo state.

```
WCN[i] = sum_j 1/d_ij^2                                # weighted contact number
z[i]   = zscore(WCN[i]) within a relative-SASA bin     # controls for burial
w[i]   = sigmoid(-z[i])                                # high = under-packed = soft
score[i] = widest_path(G, i, A, node_capacity=w)       # max over paths of min w
```

`widest_path` is Dijkstra with max-min relaxation, `O(E log V)`. This is the one observable in
this file that is _not_ monotone in graph distance, which is the property file 06 §8 says is
required to beat `ctrl_closeness` for a reason rather than by luck.

**3. Strain bottleneck versus diffusive amplitude — 5 systems, and it is the sharpest
methodological point. `quantum/` + `classical/`. [apo]**

A walk-summing propagator computes a _conductance_; a mechanical path computes a _bottleneck_.
Myosin's relay cascade, ATCase's sliding loops, Hb's interface bridges and the GTPase's single
gating hydrogen bond are all series constraints, not parallel sums.

```
w[u,v]       = 1/d_uv^2   (or a class weight for salt bridge / H-bond, per file 06 §5)
diffusive[i] = (expm(-L_w * t))[i, A].sum()            # what every walk, quantum or not, gives
strain[i]    = max_{paths i->A} min_{(u,v) in path} w[u,v]
report[i]    = strain[i] residualised on diffusive[i]  # the part a walk cannot see
```

The residual is the deliverable. File 06 §5 gives an edge-class weighting that is independently
justified; this uses it for a different aggregation.

**4. Broken-hydrophobic-chain bridge score — 2 folds + burial. `network/`. [apo]**

Pseudocode in §3. The apo-specific claim — that the informative residues are the ones spanning
the _gap_ in a chain that is broken in the inactive state — is a genuine prediction, not a
restatement, and it is falsifiable on our own benchmark.

**5. Perturbation-response propagation from the active site. `quantum/`. [apo]**

The IGPS temperature result (doi:10.1038/s41467-023-37956-1) is the physical warrant: a
non-specific perturbation reproduces the effector's pathway, so a generic source term at the
active site is defensible. The published bar is TPR 0.57 / PPV 0.72 on 20 proteins
(doi:10.1038/s41467-020-17618-2). Do not quote that bar as if it were leakage-controlled.

**6. Sector-like sparse coevolving subgraph, with two mandatory controls. `classical/`. [apo]**

Supported by DHFR surface mutagenesis (doi:10.1016/j.cell.2011.10.049). Refuted as an _energetic_
claim by two double-mutant-cycle studies (doi:10.1073/pnas.0711732105;
doi:10.1074/jbc.m402560200) and confounded by conservation and phylogeny
(doi:10.1371/journal.pcbi.1004091; doi:10.1371/journal.pcbi.1012091). Admissible only with a
plain-conservation control **and** a distance control reported alongside.

### Blocked, and why

- **Any contact-status-change feature.** The single most predictive class in the GPCR literature
  (34 residue pairs, causal by mutagenesis) and in the Src map. **[holo]**, C1-forbidden. State
  this in the report as a named limitation before a judge states it for us.
- **Cavity/pocket geometry as the primary detector.** For switch-II-pocket-type sites the pocket
  does not exist in the apo structure (doi:10.1038/nature12796). `cavity_volume` will fail on
  such cases by construction. Record the prediction now.
- **Quaternary observables.** Hb and ATCase both carry their mechanism across subunit interfaces.
  Our node set is one chain (ADR 0010, C5). Those systems motivate the module-boundary family and
  supply no computable feature.
- **MD-derived variants of any of the above.** Force distribution analysis
  (doi:10.1371/journal.pcbi.1000574), the Abl transmission path (doi:10.7554/eLife.85216), IGPS
  community analysis (doi:10.1073/pnas.1120536109) and the Hb Hessian reconstruction
  (doi:10.1016/j.bpj.2026.01.006) are all C2 violations as published. The _concepts_ transfer;
  the pipelines do not.

### One prediction to record before measuring

§8.2 and §8.5 point in opposite directions: centrality says the important residue is a
constraint, the elastic-network results say it is the absence of one. Both cannot dominate. A
single experiment separates them — rank by betweenness and by coordination deficit on the same
arms and compare against the same distance-stratified null. Whichever wins, the result is
informative, and it is cheap.

---

## Method

**Databases.** Europe PMC REST search (`resultType=core`, `pageSize` 10–40) for all bibliographic
retrieval; PMC article pages (`pmc.ncbi.nlm.nih.gov/articles/{PMCID}/`) for full text; PubMed
E-utilities `esearch` once, to resolve an author-pair query that Europe PMC title search missed;
two general web searches; two institutional/publisher page fetches. arXiv was not queried — the
scope is structural biology and biochemistry, which arXiv does not index well. Semantic Scholar
was not attempted (rate limited, conventions §3).

**Queries run** (26 batches, ~40 distinct Europe PMC queries). By section:
haemoglobin title search with allosteric/cooperativity/quaternary; exact titles for Perutz 1970,
Henry 2002 TTS, Eaton 2007; `salt bridge AND h(a)emoglobin AND (T state OR R state)`; haemoglobin
with elastic network / normal mode / contact network. Statistical coupling analysis OR protein
sectors with PDZ/reproduc/reappraisal/critique; exact titles for Chi 2008 and Fodor & Aldrich 2004. Regulatory spine OR catalytic spine OR R-spine AND kinase; exact titles for Kornev 2006 and
2008; `Dynamics-driven allostery in protein kinases` and αC-helix titles; myristoyl/myristate
pocket OR asciminib OR GNF-2 AND ABL; exact titles for Nagar 2003, Zhang 2010, Wylie 2017.
`switch-II pocket` OR KRAS G12C titles; Ostrem author search via both Europe PMC and PubMed;
exact titles for Buhrman 2010 and Spoerner 2001. Exact titles for Venkatakrishnan 2013 and 2016
and Zhou 2019; micro-switch/NPxxY/DRY/PIF AND receptor AND activation; `allosteric hub`. Relay
helix OR SH1 helix OR converter domain AND myosin; exact titles for Fischer 2005 and Cecchini
2008; Houdusse+Sweeney author pair. `aspartate transcarbamoylase` AND allosteric; Kantrowitz
author search; glucokinase title search with allosteric/cooperativity/conformational/disorder,
then exact titles for Larion 2012, Whittington 2015, Kamata 2004; dihydrofolate reductase title
search with network/allosteric/coupled/dynamics; `imidazole glycerol phosphate synthase` AND
allosteric/pathway/dynamic. Cross-cutting: exact titles for Amor 2016, Mitternacht 2011,
Panjkovich 2012, Reynolds 2011, Agarwal 2002, del Sol 2006, Amitai 2004, Wang 2020 (Ohm),
Guarnera 2016, Stacklies 2009, Yan 2017, Rocks 2017, Freiberger 2019, Gatlin 2026;
`rigidity transmission allostery`; betweenness/shortest path AND allosteric AND residue network;
frustration AND allosteric; allosteric AND orthosteric pocket comparison; hinge AND allosteric
AND (normal mode OR elastic network); force distribution analysis / internal strain / stress
propagation; cryptic site AND allosteric AND apo. Web searches: Yan & Wyart allosteric materials;
Venkatakrishnan 2013 consensus-contact count.

**Counts.** Roughly 340 title/abstract records inspected across all queries (individual query
hit counts ranged from 0 to 638; only the returned pages were read). **63 sources screened in**
and cited in this file. **Six full texts retrieved and read this session**: PMC5007447 (Amor,
bond-to-bond propensity), PMC7395124 (Wang, Ohm), PMC6410768 (Freiberger, frustration around
active sites), PMC10046315 (Brunori & Miele, haemoglobin), PMC3276696 (Lipscomb & Kantrowitz,
ATCase), PMC4274051 (Ostrem, K-Ras G12C). Everything else is `[VERIFIED-ABSTRACT]`.

**Stopping rule.** Stop when (a) each of the seven systems has at least one primary structural
source _and_ at least one source that quantifies or contests the mechanism, and (b) each of the
five cross-cutting candidates in §8 has either a multi-protein measurement with a stated effect
size or an explicit "not retrieved". Condition (a) was met for all seven. Condition (b) was met
for four of five; §8.1 (rigid cluster spanning both sites) has case studies only.

**What could not be reached.**

- **Venkatakrishnan 2013** (doi:10.1038/nature11896) has no PMC record; the Nature page was not
  fetched and the MRC LMB summary does not give numbers. The count of consensus non-covalent
  contacts is `[UNVERIFIED]` and no number is quoted from it.
- **Perutz 1970** (doi:10.1038/228726a0): the Europe PMC record carries no abstract. Every content
  claim attributed to the stereochemical mechanism is routed through PMC10046315.
- **Lockless & Ranganathan 1999, Süel 2003, Halabi 2009** were not re-retrieved this session; they
  are quoted from file 06, which retrieved them on 2026-08-25.
- **Freiberger 2019** states enrichment of frustrated contacts in the two shells but the retrieved
  text gives no odds ratio and no p-value. Reported qualitatively.
- **The frustration sign disagreement** (neutrally frustrated versus higher frustration density at
  allosteric sites) could not be resolved from abstracts; the full texts of doi:10.1002/pro.70714
  and doi:10.1021/acs.jcim.6c00203 were not landed.
- **No cross-protein benchmark of rigidity transmission allostery was retrieved.** Per ADR 0019
  this is "not retrieved by the recorded search", not an absence of prior art.
- **No source was retrieved that scores "buried non-contiguous hydrophobic chain membership" as a
  predictor on an allosteric-site benchmark.** Same wording applies.
- The Ostrem relative-affinity numbers (0.6 ± 0.2 → 3.9 ± 0.6 and 3.5 ± 0.8) are measured on the
  covalently modified protein and on holo structures. They motivate; they cannot be an input.
