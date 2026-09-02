# Graph construction: what a node is, what an edge is, and whether the choice matters

**Scope:** the substrate, not the algorithm. What the literature measures about node resolution,
edge definition, node features and hierarchy in protein structure graphs, and which of those
choices has a measured effect on a downstream task. It deliberately excludes the choice of
propagation observable (`../exploration/lit/22-transport-formalisms.md`), the quantum resource account
(`../exploration/results/43-quantum-resources.md`) and the coarse-graining _theorems_, which are
already surveyed in depth in `07-coarse-graining-scalability.md` — §Q6 here cites that file rather
than restating it.
**Sibling files:** `07-coarse-graining-scalability.md` (compression guarantees),
`../exploration/lit/24-residue-descriptors.md` (per-residue descriptors and the packing axis),
`../exploration/lit/25-md-free-fluctuation.md` (B-factor and the C2 verdicts),
`01-classical-baselines.md` (the methods themselves), `00-conventions.md` (evidence rules).
**Retrieved:** 2026-08-26.
**Archived paths:** every `../exploration/` path in this file, `lit/` included, is on the branch
`method-layer-archive` under `docs/method/exploration/`, because the method layer left `main` on
2026-09-02 (ADR 0037).

**Why this file exists.** We measured eight graph variants — cutoff ∈ {4.5, 6, 8, 10} Å, atom set
∈ {heavy, CB, CA}, weighting ∈ {unit, contact count, inverse-square, exponential, five-class
chemical} — and mean AUC over four arms moved by 0.031. The principal investigator's objection is
accepted: that family is one family. Every member is a residue-level distance-threshold graph, so
the experiment establishes that _the parameters of a distance-threshold graph_ do not matter. It
establishes nothing about scale, about non-metric edge definitions, or about node features. This
file asks the literature what lies outside that family and what is measured about it.

**Search.** Conducted 2026-08-26 across PubMed/NCBI E-utilities (`esummary.fcgi`), Europe PMC and
PMC article pages, arXiv (`abs`, `html`, `ar5iv`), bioRxiv, Crossref REST (`api.crossref.org/works`)
and general web search. Query strings, in the order run: `Delaunay tessellation protein structure
contact definition Voronoi four-body statistical potential`; `RING 3.0 residue interaction network
generator Arpeggio GetContacts typed interaction edges protein`; `PARS allosteric site prediction
server normal modes pocket conservation Panjkovich Daura`; `PASSer allosteric site prediction
machine learning ensemble AUC benchmark ASBench`; `protein graph neural network ablation atom-level
versus residue-level graph representation binding site prediction accuracy`; `Graphein python
library protein graph construction edge construction functions residue atom`; `CryptoSite cryptic
pocket prediction machine learning AUC Cimermancic 2016 PocketMiner Meller 2023 comparison`; `Ohm
allosteric communication perturbation propagation ... STRESS binding leverage Mitternacht
Berezovsky`; `perturbation response scanning protein allostery Atilgan ... anisotropic thermal
diffusion Ota Agard`; `Allosite AlloSitePro allosteric site prediction SVM pocket Huang Zhang 2013`;
`AlloReverse reverse allosteric communication server`; `Evaluating Representation Learning on the
Protein Structure Universe ProteinWorkshop graph construction ablation k-NN epsilon`; `GearNet
protein structure representation learning sequential edge radius edge KNN edge ablation`; `Voronoi
contact definition versus distance cutoff protein residue network comparison degree residue size
artefact`; `Effective inter-residue contact definitions for accurate protein fold recognition`;
`optimal distance cutoff protein structure networks side-chain centers of mass`; `parameter-free
anisotropic network model pfANM inverse power distance spring constant Yang Song Jernigan 2009`;
`Miyazawa Jernigan contact energy weighted protein residue network`; `ESM-2 protein language model
embeddings ligand binding site prediction feature ablation conservation PSSM RSA`; `hierarchical
multiscale protein graph neural network atom residue level hierarchy binding site prediction`;
`fpocket pyKVFinder CASTp cavity detection apo structure allosteric pocket descriptor`; `directed
asymmetric edges residue network allosteric signal directionality transfer entropy causality`;
`random geometric graph graph distance proportional Euclidean distance asymptotic geodesic scaling`;
`Voronota Laguerre tessellation protein contact areas Olechnovic Venclovas`; `Comparative Analysis
of Threshold and Tessellation Methods for Determining Protein Contacts`; `Entropy-based distance
cutoff protein internal contact networks`; `GrASP graph attention site prediction atom-level graph`;
`Allo-PED protein language model allosteric site prediction`; `Decoding protein structures with
residue interaction networks Trends in Biochemical Sciences 2025`. Bibliographic records were
independently confirmed through Crossref or PubMed for every reference in §References.

---

## Q1 — Scale and resolution: what is a node?

### Synthesis

The field has converged on one node per residue for network analysis and on Cα-only graphs for
geometric deep learning, and in both cases the convergence is defended by measurement rather than
by convenience — but the measurements are weaker than the convergence suggests.

The strongest general result is that **the low-frequency dynamics of a protein is nearly
resolution-independent, and this is a mechanism rather than a coincidence.** Yang and Chng's review
records that 5–6 lowest Tirion elastic-network modes suffice to describe the slow modes of the
all-atom CHARMM potential, and attributes the insensitivity to the collective nature of the modes:
a collective oscillation is "a joint effect of many interacting pairs, summed up to approach a
universal form that is governed by the central limit theorem, regardless of the details of pair
positions or potentials" [VERIFIED-FULLTEXT via `07-coarse-graining-scalability.md` §9,
doi:10.4137/bbi.s460]. Atilgan, Inanc and Atilgan reach the same conclusion from the construction
side: across a large protein dataset, different residue-network construction strategies give
consistent elastic-network predictions because the "residual" long-range interactions contribute
negligibly to the force balance, leaving eigenvectors conserved and shifting only the slower modes
marginally [VERIFIED-ABSTRACT, arXiv:0809.3715]. **If our observable is slow-mode dominated, Q1
predicts that resolution will not buy us accuracy.** That is a falsifiable prediction about our own
pipeline, and it is the same prediction our eight-variant sweep already confirmed within its family.

The one place resolution is measured to matter is where the task needs _local geometry_ rather than
collective motion. ProteinWorkshop is the cleanest instance: five progressively detailed
featurisations from Cα-only up to Cα plus backbone plus side-chain torsions, evaluated across a
matrix of encoders and tasks. On GO-BP the GearNet-Edge score moves 0.393 → 0.397 as backbone
torsions are added — 0.004, indistinguishable from our own 0.031. On fold classification the same
change moves 30.90 → 33.75, a 2.85-point gain [both VERIFIED-FULLTEXT, arXiv:2406.13864]. Same
models, same graphs, same change of resolution; one task barely notices and the other gains
materially. The authors' own summary is that Cα plus virtual angles plus backbone torsions "provides
the best performance overall on 22 out of 60 combinations" — i.e. the best single scheme wins about
a third of the time [VERIFIED-FULLTEXT, ibid.]. Notably they add a caution that runs _against_
higher resolution: letting models learn side-chain orientation implicitly "may prevent overfitting
on crystallisation artifacts" [VERIFIED-FULLTEXT, ibid.]. For an apo-only method that is a real
argument, because apo side-chain rotamers are precisely the coordinates least likely to be right.

Atom-level graphs are used in production for pocket detection. GrASP performs semantic segmentation
over protein surface _atoms_, aggregates atomic scores into sites by average-linkage clustering, and
reports that over 70 % of its output sites correspond to real binding sites against under 30 % for
P2Rank on P2Rank's own test sets [VERIFIED-ABSTRACT, doi:10.1021/acs.jcim.3c01698]. That is a large
precision gap — but it confounds resolution with architecture, training set (a rebuilt sc-PDB of
26 196 sites) and post-processing, so it is not an isolated measurement of resolution.

Multi-node-per-residue sits between the two and is the least-measured option. Martini-style bead
mappings coarse-grain _below_ the residue and therefore offer us nothing on the axis we need — our
node set is already one node per modelled residue under ADR 0010 [recorded in
`07-coarse-graining-scalability.md` §7, doi:10.1021/jp071097f, doi:10.1021/ct9002114]. A
backbone-bead-plus-side-chain-bead graph is different: it is the smallest representation in which
"the signal entered through this residue's side chain" and "the signal entered through this
residue's backbone" are distinguishable states. **No paper measuring a two-bead-per-residue graph
against a one-bead graph on a site-prediction or dynamics task was retrieved by the recorded
search.** The claim that such representations are "relatively concise ... while maintaining chemical
accuracy" was retrieved only as an assertion in a search summary, not as a measured comparison
[UNVERIFIED].

Community and domain-level coarse graphs are covered in `07-coarse-graining-scalability.md` §5, and
that file carries a load-bearing negative result: one-step community methods (modularity, Infomap)
over-partition geometric graphs by a published mechanism, giving 69 and 421 communities on a
214-residue protein where the right answers are ≈ 8 (secondary structure) and 3 (domains)
[VERIFIED-FULLTEXT there, doi:10.1371/journal.pone.0032210]. Do not build a community-level coarse
graph with Louvain or Leiden.

### The size and qubit trade-off, quantified on our own graphs

Our frozen graphs are profiled in `../exploration/data/30-frozen-graph-profile.md`. The
300-residue-scale arm is PTP1B (`1SUG`), N = 298, **1481 edges, mean contact number 9.9**, at the
input layer's own 4.5 Å heavy-atom rule [VERIFIED-FULLTEXT, that file's §2 table]. Scaling from
there:

| Representation              | Nodes at N_res ≈ 300 | Multiplier | What is gained                                                                                | What is lost                           |
| --------------------------- | -------------------- | ---------- | --------------------------------------------------------------------------------------------- | -------------------------------------- |
| Domain                      | 2–5                  | ÷ 75       | fits any device                                                                               | no residue-level answer at all         |
| Secondary-structure element | ≈ 20–35              | ÷ 10–15    | SSEs are the measured efficient mediators of communication (doi:10.1371/journal.pcbi.0030172) | cannot rank residues inside an element |
| Residue (**ours**)          | 298 (measured)       | 1×         | author numbering, medicinal-chemist-readable                                                  | side-chain orientation, chemistry      |
| Two beads per residue       | ≈ 580                | 1.9×       | backbone-vs-side-chain entry, side-chain direction                                            | apo rotamer error enters               |
| Martini-style beads         | ≈ 690                | 2.3×       | chemical bead types                                                                           | below the residue; wrong axis for us   |
| Heavy atom                  | ≈ 2 300–2 400        | ≈ 7.8×     | true covalent topology, H-bond geometry                                                       | 7.8× nodes, and more in edges          |

The qubit consequence depends entirely on the encoding, and the two encodings differ by an
exponential. Under **one qubit per node** (hard-core-boson / one-hot), heavy-atom resolution takes a
300-residue protein from 298 qubits to ≈ 2 400 — both already far past the N ≈ 20 coherence ceiling
recorded in `08-hardware-viability.md`, so the comparison is academic and coarse-graining is
mandatory either way. Under **binary amplitude encoding** of a single-particle walk, the cost is
⌈log₂ N⌉: 9 qubits at residue level, 12 at heavy-atom level. Three extra qubits is nothing. **The
real cost of atom resolution is depth, not width**, because a Trotterised `e^{−iHt}` costs O(|E|)
two-qubit rotations per step, and |E| grows faster than N when packing density is held fixed. Our
measured residue graph has 1481 edges; an atom graph at the same 4.5 Å with ≈ 7.8× the nodes and a
higher mean degree is a one-to-two-order-of-magnitude depth multiplier. That arithmetic is derived
here, not retrieved, and the atom-level edge count must be measured before it is quoted
[UNVERIFIED — derived in this file]. The authoritative resource account is
`../exploration/results/43-quantum-resources.md`.

| Citation                                     | Year | Graph choice studied                                         | Task                                                   | Measured effect                                                                          | Relevance to us                                                             |
| -------------------------------------------- | ---- | ------------------------------------------------------------ | ------------------------------------------------------ | ---------------------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| Jamasb et al., arXiv:2406.13864              | 2024 | 5 featurisation levels, Cα → Cα+backbone+side-chain torsions | GO-BP, fold classification, 60 model×task combinations | GO-BP 0.393 → 0.397 (+0.004); fold 30.90 → 33.75 (+2.85)                                 | Resolution is task-dependent. Our task resembles GO-BP more than fold       |
| Atilgan, Inanc & Atilgan, arXiv:0809.3715    | 2008 | Multiple residue-network construction strategies             | Elastic-network mode prediction                        | Eigenvectors conserved; only marginal shifts in slow modes                               | Mechanism for why our 8 variants moved 0.031                                |
| Yang & Chng, doi:10.4137/bbi.s460            | 2008 | All-atom CHARMM vs Cα elastic network                        | Slow-mode subspace                                     | 5–6 lowest ENM modes suffice for the all-atom slow modes                                 | Predicts resolution-independence _if_ our observable is slow-mode dominated |
| Smith et al., doi:10.1021/acs.jcim.3c01698   | 2024 | Atom-level surface graph + attention                         | Druggable site prediction, P2Rank test sets            | > 70 % of output sites real vs < 30 % for P2Rank                                         | Atom resolution works in production, but confounded with 4 other changes    |
| Chennubhotla & Bahar, doi:10.1038/msb4100075 | 2006 | 8015 → 21 nodes, 5 hierarchy levels                          | GroEL–GroES global modes, B-factors                    | Global-mode correlation 0.99 at every level; B-factor correlation _improved_ 0.68 → 0.89 | Coarser can be **better**. Degradation is not monotone                      |

---

## Q2 — Edge definition beyond a distance cutoff

### Synthesis

**Distance thresholding and its artefacts.** The known failure modes are three. (i) _Cutoff
sensitivity outside a sensible band._ Yuan, Chen and Kihara swept 15 cutoffs from 4.5 Å to 100 Å
across three contact bases and found fold-recognition AUC decays to random retrieval at 20 Å and
above [VERIFIED-FULLTEXT, doi:10.1186/1471-2105-13-292]. (ii) _Degree tracking residue size._ An
all-heavy-atom minimum-distance test gives a tryptophan more chances to make a contact than a
glycine; Esque, Oguey and de Brevern examined exactly this dependence of contact distributions on
residue volume, accessibility and hydrophobicity, and found that "the different methods gave
concordant results, although the method based on Cα distances showed significant discrepancies with
the all-atom tessellation method", with discrepancies "occasionally large enough to substantially
change the relative preferences of some contacts" [VERIFIED-ABSTRACT, doi:10.1021/ci100195t].
(iii) _Occlusion blindness._ Two residues 6 Å apart with a third between them are connected by a
cutoff and are not neighbours in any physical sense.

Two independent papers converge on a small optimal cutoff for side-chain-based nodes. Salamanca
Viloria et al. report an optimal 5 Å between side-chain centres of mass, "robust to changes in the
force field and the proteins" [VERIFIED-ABSTRACT, doi:10.1038/s41598-017-01498-6]. Sobieraj and
Setny minimise mutual information (least redundancy) across cutoff and contact-probability
threshold and find the minimum "universally achieved at the cutoff length of 5 Å ... in all
considered, distinct proteins" [VERIFIED-ABSTRACT, doi:10.1002/prot.26154]. Both use side-chain
centres, not heavy-atom minimum distance, so neither transfers to our rule directly — but 5 Å
side-chain-centre is a construction we have not tried.

**Delaunay / Voronoi.** Singh, Tropsha and Vaisman introduced Delaunay tessellation for proteins:
the tessellation of Cα coordinates yields simplices whose vertices "define objectively four nearest
neighbor Cα atoms, i.e. four nearest neighbor residues" [VERIFIED-ABSTRACT,
doi:10.1089/cmb.1996.3.213]. The construction is parameter-free and is the only edge definition in
this survey that is _occlusion-aware by construction_: a Voronoi facet exists only where two atoms
share a boundary with nothing between them. Esque et al. conclude the tessellation method "is more
accurate because of its fine adaptation to local protein topology, with far-reaching implications
for most contact-based prediction methods" [VERIFIED-ABSTRACT, doi:10.1021/ci100195t]. The
production implementation is Voronota (`voronota`, C++ with a scriptable interface), which
Olechnovič and Venclovas describe as computing the Voronoi diagram of atomic balls and which is
"the only publicly available software tool that outputs solvent-constrained tessellation-based
interatomic contact areas"; Voronota-LT uses the radical/Laguerre (power-diagram) variant for speed
[VERIFIED-ABSTRACT, doi:10.1002/jcc.23538; doi:10.1101/2024.02.05.577169]. Voronota-derived contacts
underpinned the best-performing method in the CASP15-CAPRI scoring challenge [VERIFIED-ABSTRACT,
ibid.], and VoroMQA uses the same contact areas for model quality assessment
[VERIFIED-ABSTRACT, doi:10.1002/prot.25278]. **The crucial point for us is the weight, not the edge
set: a Voronoi contact _area_ in Å² is not a function of inter-residue distance.** One documented
caveat: tessellation "tends to be unstable with respect to infinitesimal perturbations of the
structure" [VERIFIED-ABSTRACT, doi:10.1021/ci100195t] — relevant because an apo crystal structure is
exactly a perturbed structure. A minimum-area filter is the standard mitigation.

**Interaction-type edges.** Four tools compute typed interactions from a single static structure and
all are usable under C1/C2. **RING 4.0** (`ring`, web server and downloadable) generates residue
interaction networks with typed physico-chemical edges and now covers "over 35 000 different
chemical structures" and mmCIF input [VERIFIED-ABSTRACT, doi:10.1093/nar/gkae337]; RING 3.0 added
probabilistic edges over conformational ensembles [VERIFIED-ABSTRACT, doi:10.1093/nar/gkac365 —
NAR 50:W651, record confirmed by search, DOI not independently re-derived, see §Method].
**Arpeggio** computes "van der Waals', ionic, carbonyl, metal, hydrophobic, and halogen bond
contacts, and hydrogen bonds and specific atom–aromatic ring (cation–π, donor–π, halogen–π, and
carbon–π) and aromatic ring–aromatic ring (π–π) interactions", is implemented in Python and is
downloadable [VERIFIED-ABSTRACT, doi:10.1016/j.jmb.2016.12.004]. **Graphein** (`graphein.protein`)
is the Python library that composes these into multi-relational graphs; its edge constructors are
"organised into distance-based, intramolecular interaction-based, and atomic structure-based
submodules" and are "composable to produce multirelational graphs", with GetContacts available as
an optional dependency [VERIFIED-ABSTRACT, doi:10.1101/2020.07.15.204701; NeurIPS 35:27153–27167,
doi:10.52202/068431-1969].

**Is there evidence that typed edges beat plain contacts?** The honest answer is that we have
already measured this ourselves and the answer was no: `network.build(weighting="edge_class")`
placed 7th of 8 graphs, best mean AUC 0.772 (`../exploration/README.md`). **No published paper
isolating typed edges against plain contacts on a site-prediction task was retrieved by the recorded
search.** The 2025 TIBS review of residue interaction networks surveys construction approaches
across thermostability, allosterism, PTMs, homology and evolution but was retrieved at abstract
level only and no head-to-head number was extracted [VERIFIED-ABSTRACT,
doi:10.1016/j.tibs.2025.08.006 — see §Method for the DOI caveat].

**Energy-weighted edges.** Miyazawa–Jernigan contact energies are a 20 × 20 table derived from
observed residue-contact frequencies in the PDB by an inverted-Boltzmann argument
[VERIFIED-ABSTRACT, doi:10.1006/jmbi.1996.0114]. Using them to weight an existing contact set is a
handful of lines of Python and adds amino-acid identity to the edge. **On C2, the constraint is
about trajectories, not about energies.** C2 forbids MD trajectories and MD-derived covariance
matrices as _input_; a knowledge-based potential is a table indexed by residue-type pairs, and
evaluating it on one static structure produces no trajectory. The literature does treat these as
distinct classes — MJ energies are derived from a structural database, not from simulation. We could
retrieve **no paper that measures an MJ-weighted residue network against an unweighted one on an
allosteric-site task**; the applications retrieved are folding, threading and scoring.

**Elastic-network edge weighting.** GNM (uniform springs within a cutoff,
doi:10.1016/s1359-0278(97)00024-2) and ANM (the same with 3N degrees of freedom and direction-
dependent 3 × 3 blocks, doi:10.1016/s0006-3495(01)76033-x) are the C6 tradition. The one measured
improvement on this axis is **parameter-free ANM/GNM**: replacing the cutoff with springs falling
off as the inverse square of distance, tested on 1 220 X-ray structures plus 341 with anisotropic
B-factors, gives "better predictions of crystallographic B-factors (both isotropic and anisotropic)
and of the directions of conformational transitions", with roughly **73 % of proteins agreeing
better with pfGNM than with GNM** [VERIFIED-ABSTRACT, doi:10.1073/pnas.0902159106]. Note carefully
what this is and is not for us: we tried inverse-square weighting _inside a cutoff_; pfANM removes
the cutoff entirely, giving a dense graph. It is a different object with a different spectrum — and
it is, by construction, a pure function of distance.

**Directed / asymmetric edges.** The only construction retrieved that produces a genuinely asymmetric
residue graph from a static structure is **transfer entropy in the harmonic (GNM) approximation**.
Hacısüleyman and Erman derive a closed form for entropy transfer between residue pairs and note it
is "an asymmetric measure enabling measurement of the direction of information flow in a directed
graph" [VERIFIED-ABSTRACT, doi:10.1371/journal.pcbi.1005319; companion preprint
doi:10.1101/084764, published as a Proteins article]. Because the input is the GNM covariance —
itself the pseudo-inverse of a contact-graph Laplacian — this is computable from a single apo
structure with no MD and satisfies C1, C2 and C6. It is the strongest candidate in this file for
breaking the distance inheritance, for a reason developed in §The distance-correlation angle.

**Sequence edges as a separate relation.** GearNet's construction is the canonical example and its
justification is explicitly about degree distributions rather than accuracy: with only k-NN edges
"the node degrees in protein graphs are close to a constant", and with only radius edges "there will
be about 45 000 proteins with average degrees lower than two", so both are kept alongside sequential
edges at d_seq = 3, d_radius = 10.0 Å, k = 10 [all VERIFIED-FULLTEXT, arXiv:2203.06125 Appendix
C.1]. **GearNet does not ablate the individual edge types** — its Table 3 ablates relational
convolution, edge message passing and augmentation, not edge construction [VERIFIED-FULLTEXT,
ibid.]. So the field's most-cited multi-relational protein graph offers a _design argument_ for
separate relation types and no measurement of their value. That is worth saying plainly.

| Citation                                                 | Year | Graph choice studied                                           | Task                                                               | Measured effect                                                                     | Relevance to us                                                                          |
| -------------------------------------------------------- | ---- | -------------------------------------------------------------- | ------------------------------------------------------------------ | ----------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| Yuan, Chen & Kihara, doi:10.1186/1471-2105-13-292        | 2012 | 45 definitions: 3 bases (Cα, Cβ, heavy) × 15 cutoffs 4.5–100 Å | Fold recognition, AUC                                              | Best Cβ 7.0 Å 0.909; Cα 7.5 Å 0.908; heavy 4.5 Å 0.905; → 0.5 at ≥ 20 Å             | Within sensible definitions the spread is **0.004**. Across the whole sweep it is ≈ 0.41 |
| Esque, Oguey & de Brevern, doi:10.1021/ci100195t         | 2011 | Distance threshold vs Laguerre (weighted Voronoi) tessellation | Contact statistics, volume/accessibility/hydrophobicity dependence | Broadly concordant; Cα-based shows significant discrepancy vs all-atom tessellation | The tessellation is the occlusion-aware alternative; Cα is the one to avoid              |
| Salamanca Viloria et al., doi:10.1038/s41598-017-01498-6 | 2017 | Cutoff sweep, side-chain centre-of-mass nodes                  | Network-property stability                                         | Optimum 5 Å, robust to force field and protein                                      | A node/cutoff pair we have not tried                                                     |
| Sobieraj & Setny, doi:10.1002/prot.26154                 | 2021 | Cutoff × contact-probability threshold                         | Mutual-information redundancy of the PSN                           | MI minimum universally at 5 Å                                                       | Independent replication of the 5 Å side-chain optimum                                    |
| Yang, Song & Jernigan, doi:10.1073/pnas.0902159106       | 2009 | Cutoff springs vs parameter-free 1/d² springs                  | B-factors (1 220 structures), conformational-change directions     | ≈ 73 % of proteins better with pfGNM than GNM                                       | Removing the cutoff helps ENM — but it is pure distance                                  |
| Zhang et al., arXiv:2203.06125                           | 2023 | Sequential + radius (10 Å) + k-NN (k = 10) relations           | EC, GO                                                             | **No edge-type ablation reported**                                                  | The design argument for multi-relational graphs is unmeasured                            |
| Hacısüleyman & Erman, doi:10.1371/journal.pcbi.1005319   | 2017 | Directed graph from harmonic transfer entropy                  | Allosteric communication in ubiquitin                              | Asymmetric, direction-resolved couplings                                            | The only static-structure directed construction retrieved. C1/C2/C6 clean                |
| Olechnovič & Venclovas, doi:10.1002/jcc.23538            | 2014 | Voronoi diagram of atomic balls; contact areas                 | Software / contact-area computation                                | (Tool paper) contacts basis of best CASP15-CAPRI scorer                             | The implementable route to area-weighted, cutoff-free edges                              |

---

## Q3 — Node features: how do you enrich the graph?

### Synthesis

Every feature below is computable from an apo structure or its sequence alone, with one exception
noted. The question is which have _measured_ value for site prediction, and the honest summary is
that the measurements come overwhelmingly from orthosteric/general ligand-site prediction, and that
performance on allosteric sites is far worse in the same proteins.

**The largest measured feature effect retrieved is sequence-vs-structure, not any single
descriptor.** Chen, Lupo Pasini and Hauck compare an ESM-2-featurised GNN against one featurised
only with backbone dihedral angles for binding-site residue prediction: the structure-only model
reaches AUPRC 0.03 with AUROC 0.65, against 0.70 AUPRC for the sequence-featurised model on human
data — a collapse in precision-recall with "marked overprediction bias" while AUROC stays
respectable [VERIFIED-FULLTEXT, doi:10.1101/2025.08.25.672254]. Two lessons. First, a
language-model embedding is worth far more than local geometry for this class of task. Second, and
more important for us, **AUROC and AUPRC disagree violently on the same models** — a point developed
in Q5.

**Protein language models on allosteric sites specifically.** Allo-PED reports MCC 0.544 and AUC
0.920 for its pocket-level model, outperforming AllositePro and PARS, and finds ProtT5-3B beats
ESM-2 and ESM-C for this task, with ESM-2 and ESM-C giving recalls of 0.360 and 0.378
[VERIFIED-ABSTRACT, doi:10.1101/2025.03.28.645953]. Set against that, `00-conventions.md` §5 records
that protein language models collapse on allosteric sites: AUPR 0.64–0.76 on orthosteric against
**0.06** on allosteric in the same proteins, with AUROC still 0.70. The two are not contradictory —
they are the same AUROC/AUPRC divergence again, measured on the same class of feature. Any node
feature we adopt must be judged on the frozen benchmark's own estimator, never on a published AUC.

**Deposited B-factor** is the one feature whose status in this repo is already settled and it is
settled sharply: `../exploration/lit/25-md-free-fluctuation.md` establishes it as "the fluctuation route's
oracle, so one line of code closes or opens it", and it is implemented as
`allo.classical.baselines.mean_bfactor`. It is available from any apo PDB, it is free, and it is
already in the battery. Note the caution recorded there: Yang and Bahar place catalytic sites at
global-hinge _minima_ in over 70 % of 98 enzymes, so a naive high-flexibility ranking returns the
negative class.

**Packing and burial descriptors are closed.** `../exploration/lit/24-residue-descriptors.md` measured six
candidate columns — Voronoi volume, weighted contact number, occluded surface, residue depth, DPX
and CX — and found them to be one axis that the frozen null already controls. **Do not re-add
them.** RSA and burial depth belong to that axis. RSA remains worth carrying as a _filter_ (an
allosteric site must be at least partly solvent-exposed to be druggable) rather than as a score.

**Conservation** is available from sequence alone and is used by PARS, whose structural-conservation
term is half its method. But the direction of the signal is against us: allosteric sites are
measurably _less_ conserved than orthosteric sites — the GPCR literature reports orthosteric
residues showing "a strikingly high degree of conservation" while the muscarinic allosteric site
shows "a striking divergence of residues" by comparison [VERIFIED-ABSTRACT,
doi:10.3390/ijms24021170 — record retrieved by search; see §Method]. Conservation is therefore a
negative-going or at best weak feature for our positive class, not the free win it is for catalytic
sites.

**Cavity descriptors** are the strongest apo-available geometric feature and the bar we already have
to clear. fpocket reports that in a reference test set "94 and 92 % of known binding pockets were
correctly identified within the best three ranked pockets from the holo and apo proteins"
[VERIFIED-ABSTRACT, doi:10.1093/nar/gkq383; base method doi:10.1186/1471-2105-10-168]. The apo
number barely trails the holo number, which is unusual in this field and is why `00-conventions.md`
§6 lists `cavity_volume` as one of the four bars. fpocket is itself Voronoi-based — it uses α-spheres
derived from Voronoi tessellation — which links Q3 back to Q2.

**Secondary structure** is free from DSSP and has a physical justification specific to our problem:
Chennubhotla and Bahar measured hitting-time distributions over ~194 000 residue pairs across five
enzymes and found helical and strand residues communicate faster than coil residues
[VERIFIED-FULLTEXT via `07-coarse-graining-scalability.md` §3.5, doi:10.1371/journal.pcbi.0030172].
That makes SSE a _propagation-rate_ feature, not merely a label — it belongs on the edge, not only
on the node.

| Citation                                                 | Year | Feature studied                                          | Task                                          | Measured effect                                                    | Apo-available?                              |
| -------------------------------------------------------- | ---- | -------------------------------------------------------- | --------------------------------------------- | ------------------------------------------------------------------ | ------------------------------------------- |
| Chen, Lupo Pasini & Hauck, doi:10.1101/2025.08.25.672254 | 2025 | ESM-2 embeddings vs backbone dihedrals                   | Binding-site residue prediction               | AUPRC 0.70 vs 0.03; AUROC 0.82+ vs 0.65                            | Yes (sequence + backbone)                   |
| Allo-PED, doi:10.1101/2025.03.28.645953                  | 2025 | ProtT5-3B vs ESM-2 vs ESM-C embeddings + pocket features | Allosteric site prediction                    | Pocket model MCC 0.544, AUC 0.920; ESM-2 recall 0.360, ESM-C 0.378 | Yes                                         |
| Schmidtke et al., doi:10.1093/nar/gkq383                 | 2010 | Voronoi α-sphere cavity descriptors                      | Pocket detection, top-3                       | 94 % holo / **92 % apo**                                           | Yes — and the apo gap is small              |
| Chennubhotla & Bahar, doi:10.1371/journal.pcbi.0030172   | 2007 | Secondary structure as a communication mediator          | Hitting times, ~194k residue pairs, 5 enzymes | Helix/strand residues communicate faster than coil                 | Yes (DSSP)                                  |
| Jamasb et al., arXiv:2406.13864                          | 2024 | Virtual angles, backbone torsions, side-chain torsions   | 60 model × task combinations                  | Best scheme wins 22/60; GO-BP +0.004                               | Yes; side-chain torsions are apo-unreliable |
| Panjkovich & Daura, doi:10.1186/1471-2105-13-273         | 2012 | Flexibility (NMA) + structural conservation of pockets   | Allosteric site prediction                    | 65 % positive predictive value                                     | Yes                                         |

---

## Q4 — What the allosteric-site prediction field actually uses

### Synthesis

Read the table below beside two facts already established in this repo, because without them the
published numbers mislead. First, `00-conventions.md` §6: AlloBench dropped every test protein
sharing a UniRef50 cluster with a training protein and **no tool of eight exceeded 60 % accuracy
even at a very low Jaccard cutoff**, retesting APOP at 15 % at Jaccard > 0.5
(doi:10.1021/acsomega.5c01263). Second, CAPASP finds APOP and PASSer degrade specifically on apo
input against holo input (doi:10.1007/s10822-026-00831-4) — which is the exact axis the challenge
scores on. **Every number in the table below is a same-distribution number and none of them is a
target we should try to match.**

The structural observation that matters most for this file: **the field's graphs are almost all
distance-threshold contact graphs, and the two most interesting exceptions are in the weighting, not
the edge set.** Ohm's edge weight is a saturating nonlinearity on a normalised atom-contact count,
`P_ij = 1 − exp(−α·N_ij)` with α = 3.0 by default, where a contact is any atom pair within **3.4 Å**
and N_ij is normalised by the number of atoms in each residue [all VERIFIED-FULLTEXT,
doi:10.1038/s41467-020-17618-2]. That normalisation is the one construction in the published field
that explicitly cancels the residue-size degree artefact of Q2(ii). It is not a weighting we tried.

| Method                                                                                                                                 | Node                                                 | Edge                                         | Weight                                                                                     | What propagates                                                                                            | Reported performance                                                                                                                                                                                      | Tag                                                        |
| -------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------- | -------------------------------------------- | ------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| **PARS** (doi:10.1093/bioinformatics/btu002; method doi:10.1186/1471-2105-13-273)                                                      | Pocket (fpocket), plus ENM residue network for NMA   | ENM contact springs                          | Uniform                                                                                    | Not a propagation method: NMA flexibility change on ligand binding + structural conservation of the pocket | 65 % positive predictive value                                                                                                                                                                            | [VERIFIED-ABSTRACT]                                        |
| **Allosite** (doi:10.1093/bioinformatics/btt399)                                                                                       | Pocket                                               | — (pocket descriptors, SVM)                  | —                                                                                          | Nothing; classification                                                                                    | "~95 % accuracy on the test set"                                                                                                                                                                          | [VERIFIED-ABSTRACT]                                        |
| **AllositePro** (doi:10.1021/acs.jcim.7b00014)                                                                                         | Pocket + perturbation analysis                       | ENM                                          | —                                                                                          | Perturbation response                                                                                      | F1 89.66 %; 90.5 % of allosteric pockets in top 3                                                                                                                                                         | [VERIFIED-ABSTRACT]                                        |
| **AlloPred** (doi:10.1186/s12859-015-0771-1)                                                                                           | Pocket                                               | ENM (normal-mode perturbation)               | Spring perturbation on pocket residues                                                     | Change in normal modes when pocket residues are stiffened                                                  | SVM over perturbation + pocket features                                                                                                                                                                   | [VERIFIED-ABSTRACT]                                        |
| **PASSer** (doi:10.1088/2632-2153/abe6d6; 2.0 doi:10.3389/fmolb.2022.879251; server doi:10.1093/nar/gkad303; ranking arXiv:2302.01117) | Pocket (fpocket) + atomic graph for the GCNN branch  | Atomic graph                                 | Learned                                                                                    | XGBoost on physical properties ensembled with a GCNN on the atomic graph                                   | PASSer2.0: **82.7 %** of allosteric pockets in top 3. Ensembling gave +6.00 % recall, −0.82 % precision, +2.89 % F1, +1.89 % AUROC. Trained on ASBench core-diversity (138) → 204 proteins                | [VERIFIED-ABSTRACT]                                        |
| **Ohm** (doi:10.1038/s41467-020-17618-2)                                                                                               | Residue                                              | Any atom pair within **3.4 Å**               | `P_ij = 1 − exp(−α·N_ij)`, N_ij = contact count normalised by residue atom counts, α = 3.0 | Stochastic perturbation from the active site, 10⁴ repeats → allosteric coupling intensity                  | 20 proteins (147–3311 aa, monomer to dodecamer). TPR **0.57** vs 0.23 for Amor's method; PPV **0.72** vs 0.48. For residue-pair correlations, "TPR of Ohm and the hitting time are both 47.6 %" at top-20 | [VERIFIED-FULLTEXT]                                        |
| **AlloReverse** (doi:10.1093/nar/gkad279)                                                                                              | Residue / pocket / pathway, three scales             | Dynamics + ML pipeline                       | —                                                                                          | Reversed allosteric communication from the orthosteric site                                                | Known allosteric sites discovered on **77.6 %** of benchmark proteins                                                                                                                                     | [VERIFIED-ABSTRACT]                                        |
| **Binding leverage** (doi:10.1371/journal.pcbi.1002148)                                                                                | Surface site sampled by MC ligand probes             | ENM low-frequency modes                      | —                                                                                          | Coupling of site deformation to intrinsic motions                                                          | Introduced the leverage score; benchmark numbers not retrieved this session                                                                                                                               | [VERIFIED-ABSTRACT]                                        |
| **STRESS** (doi:10.1016/j.str.2016.03.008)                                                                                             | Surface-critical + interior-critical residues        | ENM + information-flow bottlenecks           | Binding leverage                                                                           | MC flexible-ligand probing for surface sites; betweenness-style bottlenecks for interior                   | Modified binding-leverage framework; benchmark numbers not retrieved this session                                                                                                                         | [VERIFIED-ABSTRACT]                                        |
| **SPACER** (doi:10.1093/nar/gkt460)                                                                                                    | Residue / site                                       | ENM                                          | —                                                                                          | Binding leverage and "leverage coupling" between allosteric and catalytic sites                            | Server paper; no benchmark accuracy retrieved                                                                                                                                                             | [VERIFIED-ABSTRACT]                                        |
| **PRS** (doi:10.1371/journal.pcbi.1000544)                                                                                             | Residue                                              | ENM contact springs                          | Uniform                                                                                    | Directed random forces on single residues, response via linear response theory                             | Reproduces bound-vs-unbound residue displacements                                                                                                                                                         | [VERIFIED-ABSTRACT]                                        |
| **Anisotropic thermal diffusion** (doi:10.1016/j.jmb.2005.05.043)                                                                      | Atom                                                 | MD force field                               | —                                                                                          | Heat injected at one residue, diffusion monitored                                                          | PSD-95 PDZ3: pathway His-372 → Ile-327/Phe-325 → Ile-341, Ala-347, Leu-353. "Greatly enhanced signal-to-noise" vs conventional MD                                                                         | [VERIFIED-ABSTRACT] — **violates C2** (non-equilibrium MD) |
| **Markov transients / commute time** (doi:10.1039/c4mb00088a; doi:10.1371/journal.pcbi.0030172)                                        | Atom (Amor et al.) or residue (Chennubhotla & Bahar) | Atomistic bond + interaction graph; ENM      | Chemistry-weighted                                                                         | Random-walk transients from the active site; hit and commute times                                         | Caspase-1: transient analysis from the active site "predict[s] the location of a known allosteric site". Satisfies C1, C2, C6 exactly                                                                     | [VERIFIED-ABSTRACT]                                        |
| **CryptoSite** (doi:10.1016/j.jmb.2016.01.029)                                                                                         | Residue                                              | — (feature vector incl. MD-derived features) | —                                                                                          | Classifier over structural, dynamic and sequence features                                                  | ROC-AUC **0.85**; requires on-the-fly simulation, ≈ 1 day per structure                                                                                                                                   | [VERIFIED-ABSTRACT] — **violates C2**                      |
| **PocketMiner** (doi:10.1038/s41467-023-36699-3)                                                                                       | Residue graph                                        | Learned GNN over structure                   | Learned                                                                                    | Predicts cryptic pocket _opening_ from a single structure                                                  | ROC-AUC **0.87** vs 0.85 for CryptoSite; > 1000× faster (< 1 s vs hours)                                                                                                                                  | [VERIFIED-ABSTRACT] — **trained on MD, violates C2**       |

**Two entries to read carefully.** ATD and CryptoSite are C2 violations at the input; PocketMiner is
a C2 violation at the weights (`00-conventions.md` §4 names it explicitly). None of the three is
usable, but Ohm's construction _is_ usable and is the single most transferable idea in this table.

---

## Q5 — Does graph construction measurably change results? The ablation evidence

### Synthesis

The literature's answer is consistent and has two halves, and reporting only one half would
misrepresent it.

**Half one: inside a sensible band, graph construction barely matters, and this is replicated.**
Yuan et al.'s three best of 45 contact definitions span **0.909, 0.908, 0.905** in fold-recognition
AUC — a spread of 0.004 across three different atom bases at three different cutoffs
[VERIFIED-FULLTEXT, doi:10.1186/1471-2105-13-292]. ProteinWorkshop's featurisation ladder moves
GO-BP by 0.004 [VERIFIED-FULLTEXT, arXiv:2406.13864]. Atilgan et al. give the mechanism for the
elastic-network case: residual long-range interactions barely change the force balance, so
eigenvectors are conserved [VERIFIED-ABSTRACT, arXiv:0809.3715]. Our own 0.031 sits in exactly this
regime, and `../exploration/data/30-frozen-graph-profile.md` §3.3 supplies the local proof: across a
7.2× range in protein size, mean contact number spans only 8.9–10.3, clustering 0.460–0.515 and λ₁
10.40–11.80. **A residue contact graph at a fixed cutoff is a near-universal object.** That is why
its parameters do not matter — and it is also a warning, because it means raw topology cannot be
what separates one target from another.

**Half two: outside that band, or on a different metric, graph construction matters enormously.**
Yuan et al.'s full sweep runs from 0.909 down to chance at cutoffs ≥ 20 Å — a range of about 0.41
[VERIFIED-FULLTEXT, ibid.]. ProteinWorkshop's fold task moves 2.85 points on the same change that
moves GO-BP by 0.004 [VERIFIED-FULLTEXT, arXiv:2406.13864]. And the sharpest result of all is Chen
et al.: sweeping the graph cutoff over 8, 12, 16, 20 and 24 Å leaves **AUROC essentially flat**
(≥ 0.82 throughout, standard deviation < 0.03) while **AUPRC collapses from 0.70 to 0.36 on human
data and from 0.50 to 0.25 on yeast** [VERIFIED-FULLTEXT, doi:10.1101/2025.08.25.672254]. The same
paper reports a hybrid rule — 24 Å between binding-residue pairs and 8 Å elsewhere — raising AUPRC
above 0.86; the extraction of that particular figure was internally inconsistent about which species
it applies to, so treat the hybrid number as **directionally reported, magnitude unconfirmed**
[UNVERIFIED] and re-read the paper before quoting it.

**This is the single most important finding in this file for us.** We measured AUC and concluded the
graph does not matter. Chen et al. show a construction sweep that a rank-based metric declares
irrelevant (ΔAUROC < 0.03) while a precision-based metric declares decisive (ΔAUPRC ≈ 0.34, roughly
a factor of two). Our positive class is small and our candidate pool is large, which is precisely
the regime where AUROC and AUPRC diverge. **Our 0.031 may be a property of our estimator rather
than of our graphs.** This does not license changing the frozen protocol — nothing in
`docs/benchmark/evaluation/` may move once a method has been scored — but it does mean the
conclusion "graph construction does not matter" is not supported by the experiment we ran, and it
identifies exactly which additional readout would settle it.

| Citation                                                 | Year | Graph choice ablated                                | Task                                       | Measured effect                                                                                                                                           | Direction                                    |
| -------------------------------------------------------- | ---- | --------------------------------------------------- | ------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------- |
| Chen, Lupo Pasini & Hauck, doi:10.1101/2025.08.25.672254 | 2025 | Cutoff 8/12/16/20/24 Å; hybrid cutoff; feature sets | Binding-site residue prediction, 4 species | AUROC flat (≥ 0.82, SD < 0.03). **AUPRC 0.70 → 0.36** (human), 0.50 → 0.25 (yeast) across the same sweep. Hybrid cutoff > 0.86 [UNVERIFIED, see §Q5 text] | **Large** — on AUPRC only                    |
| Yuan, Chen & Kihara, doi:10.1186/1471-2105-13-292        | 2012 | 45 contact definitions                              | Fold recognition, AUC                      | Top three span 0.004. Full sweep spans ≈ 0.41                                                                                                             | **Both**: tiny inside the band, huge outside |
| Jamasb et al., arXiv:2406.13864                          | 2024 | 5 featurisation levels × 12 encoder/task pairs      | GO-BP, fold, others                        | GO-BP +0.004; fold +2.85. Best scheme wins 22/60                                                                                                          | **Task-dependent**                           |
| Atilgan, Inanc & Atilgan, arXiv:0809.3715                | 2008 | Multiple network-construction strategies            | ENM modes                                  | Eigenvectors conserved; marginal slow-mode shifts                                                                                                         | **Small**, with a mechanism                  |
| Zhang et al., arXiv:2203.06125                           | 2023 | (design argument only) sequential + radius + k-NN   | EC, GO                                     | **No edge-construction ablation reported**                                                                                                                | Unmeasured                                   |
| Esque, Oguey & de Brevern, doi:10.1021/ci100195t         | 2011 | Threshold vs Laguerre tessellation                  | Contact preference statistics              | Generally concordant; Cα-based significantly discrepant; some contact preferences substantially changed                                                   | **Small on average, large in the tail**      |
| Sobieraj & Setny, doi:10.1002/prot.26154                 | 2021 | Cutoff × contact-probability threshold              | Mutual-information redundancy              | MI minimum universally at 5 Å across distinct proteins                                                                                                    | **A single optimum exists**                  |
| Chennubhotla & Bahar, doi:10.1038/msb4100075             | 2006 | 5 levels of coarse-graining, 8015 → 21 nodes        | B-factor correlation                       | 0.68 at full residue resolution, **0.89** at level 3 (133 nodes)                                                                                          | **Large, and non-monotone**                  |

---

## Q6 — Multi-scale and hierarchical graphs

**This question is already answered in depth by `07-coarse-graining-scalability.md`, which carries
49 full-text-verified claims on exactly this topic.** Restating it here would create two sources of
truth for a deliverable the challenge scores. What follows is only what that file does not cover,
plus a pointer to the three results that answer the challenge's "prove that this compression retains
the essential topological signal" clause.

**The theorem to cite is Loukas's restricted spectral approximation, not eigenvalue interlacing.**
Interlacing (`γ₁λ_k ≤ λ̃_k ≤ γ₂λ_{k+N−n}`) holds for every coarsening and is vacuous at useful
compression, because at 70 % compression `N − n` is most of the spectrum. Restricted spectral
approximation bounds the action of `L` on the span of the k lowest eigenvectors and gives bounds in
terms of `λ_k` rather than `λ_{k+N−n}`, with the guarantee _tighter for slower modes_ — which is the
subspace allostery uses [all VERIFIED-FULLTEXT in `07` §1.1–1.2, arXiv:1808.10650]. The guarantee is
a posteriori: you measure ε for the coarsening you produced.

**Does a coarse graph provably retain the low-frequency signal?** Three answers of different strength,
all in `07`: (a) Kron reduction preserves effective resistance between retained nodes **exactly** —
an equality, not a bound [arXiv:1102.2950 Thm 8] — at the cost of densifying the graph to a clique,
which is a direct C3 hit; (b) the Markov-state-model Galerkin bound `E(δ) ≤ λ₁(m−1)δ²` is
**quadratic** in the projection error of the dominant eigenvectors onto the coarse space
[doi:10.1137/100798910 family, Djurdjevac, Sarich & Schütte Thm 4.2]; (c) empirically, Chennubhotla
and Bahar retain global modes at correlation 0.99 across a 380× node reduction and _improve_ the
B-factor correlation from 0.68 to 0.89 [doi:10.1038/msb4100075].

**Does hierarchy beat a single scale, for us?** The retrieved protein-specific evidence is thin and
what exists is not on our task. Markov Stability recovers residue (206), secondary-structure (8) and
domain (3) levels from a single sweep on adenylate kinase [doi:10.1073/pnas.0903215107;
doi:10.1371/journal.pone.0032210] and is the best-validated multiscale method on proteins — but it
is a _partitioning_ result, not a demonstration that a hierarchical graph outperforms a single-scale
graph on site prediction. Hierarchical protein GNNs exist (GraphRBF is described as an interpretable
hierarchical geometric framework, doi:10.1093/gigascience/giae080; ScanNet builds spatiochemical
atom neighbourhoods then predicts hierarchical amino-acid representations) but **no ablation
isolating the hierarchy against a matched single-scale graph on a site-prediction task was retrieved
by the recorded search.** Graph pooling methods (DiffPool, MinCutPool) carry no retention theorem
and learn their assignments from labelled data, so they cannot satisfy the challenge's "prove"
clause and risk C2 — recorded as surveyed and rejected in `07` §4.

**One construction from `07` deserves promotion here because it is simultaneously the coarse-graining
answer and a candidate method.** Chennubhotla and Bahar's soft ownership matrix gives fractional
membership of fine residues in coarse nodes, so a coarse score expands to _different_ fine-scale
scores within one cluster — the resolution comes from ownership weights derived from the fine graph,
not invented. And the residues with _intermediate_ ownership are exactly their high-communication-
entropy "messengers", nominated as sites of high allosteric potential [VERIFIED-FULLTEXT in `07`
§10, doi:10.1038/msb4100075]. The reverse map and the allosteric readout are the same object. That
is an unusually clean fit and it is not in our code.

---

## Recommended graph variants to test

Ranked by expected information gain per unit of implementation cost. Node counts are for a
300-residue protein; our measured reference is PTP1B, N = 298, |E| = 1481, ⟨k⟩ = 9.9. The final
column is the property that matters most to us and is argued in the next section.

**1. Laguerre / Voronoi contact graph, weighted by contact area.**
(a) Run Voronota (or Voronota-LT) on the apo PDB's heavy atoms with radii; sum atom–atom contact
areas into a residue × residue matrix; drop pairs below a minimum area (e.g. 1 Å²) to absorb the
tessellation's perturbation instability. (b) `voronota` / `voronota-lt` CLI; parse the
`--contacts` output in pure Python. (c) Adds occlusion awareness (no facet through an intervening
residue), a physically meaningful weight in Å², and removes the residue-size degree artefact — none
of which a 4.5 Å heavy-atom cutoff has. (d) 300 nodes. (e) **Less** correlated: contact area is a
packing quantity, not a distance.

**2. Directed graph from GNM transfer entropy; rank on the antisymmetric part.**
(a) Build the GNM Kirchhoff matrix from the existing contact graph, take `Γ⁺`, evaluate
Hacısüleyman and Erman's closed form for `T(i→j)` at a chosen lag, and score each residue by
`Σ_j [T(source→j) − T(j→source)]` or the source column of the antisymmetric part. (b) NumPy only;
`allo.network` already supplies the graph. (c) Adds **direction**, which no symmetric construction
we have can express. (d) 300 nodes, 300 × 300 directed matrix. (e) **Least** correlated of the list:
the symmetric, distance-like part cancels in the antisymmetrisation. See next section.

**3. Hydrogen-bond and salt-bridge network only — no van der Waals edges.**
(a) Run RING 4.0 or Arpeggio on the apo structure; keep only HBOND, IONIC and SSBOND edges; discard
VDW and hydrophobic. (b) `ring` (downloadable) or the Arpeggio Python package; `graphein.protein`
composes the result. (c) Adds **angular** chemistry — an H-bond requires donor–acceptor geometry, so
many close pairs get no edge and some distant pairs do. Our `edge_class` experiment kept every
contact and only re-weighted it; this changes the edge _set_. (d) 300 nodes, roughly 1.5–2.5
edges per residue, i.e. a graph 4–6× sparser than ours — which also cuts circuit depth. (e)
**Less** correlated: the edge set is no longer a function of distance alone.

**4. Multi-relational graph with per-relation hopping rates.**
(a) Five relations from RING/Arpeggio — sequence (i, i+1), H-bond, ionic, hydrophobic, vdW — carried
as five separate adjacency matrices; the Hamiltonian is `H = Σ_r J_r A_r` with the five `J_r`
chosen on the `development` tier only. (b) `graphein.protein` edge constructors, which are explicitly
composable into multirelational graphs. (c) Adds relation-type structure that a single weighted
adjacency collapses by construction. GearNet argues for this design and never measures it, so the
measurement is genuinely open. (d) 300 nodes, 5 edge types. (e) **Less** correlated if the fitted
rates differ materially; identical to a re-weighting if they do not — which is itself the result.

**5. Ohm's normalised saturating contact weight.**
(a) Count atom pairs within 3.4 Å for each residue pair, divide by the atom counts of both residues,
set `w_ij = 1 − exp(−3.0 · N_ij)`. (b) Twenty lines over the existing structure parser. (c) The 3.4 Å
threshold is far tighter than our 4.5 Å; the normalisation cancels residue size; the exponential
saturates so a 12-atom-pair contact and a 20-atom-pair contact are nearly equal. This is the only
published construction that explicitly de-biases residue size, and it is the graph behind the best
head-to-head allosteric number in Q4 (TPR 0.57 vs 0.23). (d) 300 nodes. (e) **Slightly less**
correlated: still a contact graph, but the weight saturates rather than tracking distance.

**6. Backbone-stripped tertiary-contact graph.**
(a) Delete every edge with |i − j| ≤ k for k ∈ {2, 4}, keeping only tertiary contacts. (b) One line
of NumPy on the existing adjacency. (c) Removes the polymer chain, which is a trivially
distance-consistent path present in every one of our eight variants and which dominates short
geodesics. Forces propagation through packing. (d) 300 nodes, roughly 20–35 % fewer edges. (e)
**Less** correlated: the chain path is the most distance-faithful part of the graph, and this
deletes it.

**7. Two nodes per residue: backbone centroid plus side-chain centroid.**
(a) For each residue emit a node at the N/CA/C/O centroid and, for non-glycine, a node at the
side-chain heavy-atom centroid; connect intra-residue pairs with a strong edge and inter-node pairs
by a distance rule. (b) Biotite or Biopython for the parse; NumPy for the centroids. (c) Adds
side-chain orientation and makes "entered via the side chain" a distinct state — the minimum
representation in which a pocket-lining side chain is not the same object as its backbone. (d) ≈ 580
nodes (300 backbone + ≈ 280 side-chain). (e) **About the same** correlation, but the source is
sharper because the active site is defined by side chains.

**8. Delaunay tessellation on side-chain centroids, α-filtered.**
(a) `scipy.spatial.Delaunay` on the side-chain centroid coordinates; take simplex edges; drop edges
longer than 8–10 Å to remove the surface artefacts of an unbounded tessellation. (b) SciPy, stdlib
otherwise. (c) Parameter-free neighbourhood (up to the α filter), occlusion-aware, and the
four-body simplex structure is available for free as a hypergraph if we ever want three-body terms.
(d) 300 nodes. (e) **Marginally less** correlated: it removes occluded pairs but still connects
near neighbours.

**9. Miyazawa–Jernigan energy-weighted contact graph.**
(a) `w_ij = |e(a_i, a_j)|` on the existing 4.5 Å contact set, from the published 20 × 20 table.
(b) A hard-coded table plus NumPy. (c) Adds amino-acid identity to the edge — the first weight in
our repertoire that is not a function of geometry at all. Legal under C2: a knowledge-based table
evaluated on one static structure is not a trajectory. (d) 300 nodes. (e) **Less** correlated in
principle — but MJ energies track hydrophobicity, hydrophobicity tracks burial, and
`../exploration/lit/24-residue-descriptors.md` has already closed the burial axis. Test it, and expect the
matched-patch null to absorb much of it.

**10. Side-chain-centre-of-mass graph at 5 Å.**
(a) Nodes at side-chain centres of mass (CA for glycine); edge if the centres are within 5 Å.
(b) Biotite/Biopython + NumPy. (c) Two independent papers converge on 5 Å as optimal for this node
definition — one on network-property stability, one on mutual-information redundancy. It is a
node/cutoff pair our eight variants do not contain, and it produces a markedly sparser graph than
4.5 Å heavy-atom minimum distance. (d) 300 nodes. (e) **About the same** — it is still a threshold
graph, and it belongs on the list as the field's own recommended default rather than as a
distance-breaking construction.

**11. Secondary-structure-element coarse graph.**
(a) DSSP the apo structure; make each helix, strand and long loop a node; edge weight = number of
residue contacts between elements, or the summed Voronoi contact area. (b) `mkdssp` or
`biotite.structure.annotate_sse`; NumPy for the aggregation. (c) This is the challenge's
coarse-graining deliverable and the only construction here that gets a 300-residue protein onto a
near-term device under one-qubit-per-node. Physically justified: SSEs are the measured efficient
mediators of communication. (d) ≈ 20–35 nodes. (e) **Less** correlated, for a structural reason: an
element is an extended object, so "distance to the source" is no longer well defined for it.

**12. Chennubhotla–Bahar soft-ownership hierarchy, one level.**
(a) Build the Markov chain on the residue graph, extract the reduction operator `R` and expansion
kernel `K` as in their §Methods, propagate coarse, expand back by `p = K q`. (b) NumPy;
eigendecomposition at N ≈ 1000 is free. (c) It is simultaneously the coarse-graining method, the
reverse map to author-numbered residues, and a candidate readout — the intermediate-ownership
residues are their "messengers" and are nominated as high allosteric potential. It answers
`CHALLENGE.md` §4.2's two-part demand with one object. (d) Tunable; their GroEL hierarchy ran 8015 →
1316 → 483 → 133 → 35 → 21. (e) **Less** correlated: ownership is a stochastic-profile similarity,
not a metric.

**Not recommended, and why.** _pfANM_ (springs ∝ 1/d² with no cutoff) is the field's own measured
improvement — ≈ 73 % of proteins fit B-factors better — but it is by definition a pure function of
inter-residue distance on a complete graph, so it maximises exactly the confound we are trying to
escape, and its all-to-all Hamiltonian is a C3 disaster. _Full heavy-atom graphs_ at ≈ 2 400 nodes
buy 3 qubits under binary encoding and cost one to two orders of magnitude in depth, for a task
whose slow-mode character predicts resolution-independence. _Louvain/Leiden community coarse graphs_
are predicted to over-partition by a published mechanism.

---

## The distance-correlation angle

**The problem stated precisely.** Our scores correlate 0.65–0.85 with negated Euclidean distance to
the source, and the six constructions ADR 0026 opened measured |ρ| from 0.74 to 0.81
(`../exploration/README.md`). The matched-patch null absorbs exactly that. So the question is not
"which construction scores highest" but "which construction carries information that is not a
function of `‖r_i − r_j‖`".

**Why a contact graph cannot escape distance, as a theorem rather than an observation.** A graph
built by thresholding `‖r_i − r_j‖ < d` on points embedded in ℝ³ is a random geometric graph. Díaz,
Mitsche, Perarnau and Pérez-Giménez study exactly the relation between graph distance and Euclidean
distance in this model and establish the asymptotic proportionality, with the elementary lower
bound `‖u − v‖ ≤ r · d_G(u, v)` [VERIFIED-ABSTRACT, doi:10.1017/apr.2016.31; preprint
arXiv:1404.4757]. Geodesics in a geometric graph converge to geodesics of the underlying manifold as
density grows. **A residue contact graph is dense (⟨k⟩ ≈ 9.9 on our own arms) and low-dimensional,
so its shortest paths are Euclidean distance in different units.** Everything downstream inherits
it: a diffusion kernel `exp(−tL)` is dominated at short `t` by short paths and at long `t` by the
stationary (degree) distribution, and degree in a geometric graph is local packing density — burial.
Distance at one end, burial at the other. This is not a defect of our implementation; it is what a
distance-threshold graph _is_. `../exploration/data/30-frozen-graph-profile.md` §3.3 is the same
statement measured: at fixed cutoff, ⟨k⟩, clustering and λ₁ barely move across a 7.2× size range,
so the topology carries almost no target-specific information beyond the geometry.

**The test for whether a construction breaks the inheritance.** Ask one question of the edge
definition: _can two residue pairs at the same inter-residue distance receive different edges?_ If
no, the construction is a reparameterisation of distance and cannot escape. Applying it:

| Construction                               | Two pairs at equal distance get different edges?                      | Verdict                                                                                |
| ------------------------------------------ | --------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| Distance threshold, any cutoff             | No                                                                    | Cannot escape. This is our whole current family                                        |
| Inverse-square / exponential decay weights | No — a monotone function of `d`                                       | Cannot escape. Explains why 4 of our 5 weightings moved nothing                        |
| pfANM (1/d², no cutoff)                    | No                                                                    | Cannot escape; maximises the confound                                                  |
| Delaunay / Voronoi edge set                | **Yes** — occlusion by a third residue removes an edge                | Partial escape                                                                         |
| Voronoi contact **area** weight            | **Yes** — area depends on local packing and atomic radii              | Partial escape, and the weight is the stronger half                                    |
| Ohm's normalised contact count             | **Yes** — a Trp–Trp and a Gly–Gly pair at 4 Å differ                  | Partial escape, via atom counts and normalisation                                      |
| H-bond / salt-bridge edge set              | **Yes** — donor–acceptor angle and residue chemistry decide           | Substantial escape                                                                     |
| Miyazawa–Jernigan weights                  | **Yes** — depends only on the two residue types                       | Substantial in principle; confounded with burial in practice                           |
| Sequence relation as a separate type       | Partly — `\|i−j\|` is not a function of `‖r_i − r_j‖`                 | Partial escape; cheap                                                                  |
| Backbone-stripped graph                    | **Yes** — the same distance is kept or dropped by sequence separation | Partial escape; one line                                                               |
| ANM 3 × 3 blocks                           | **Yes** — the unit vector `r̂_ij` is orientation, not distance         | Partial escape; our scalar readout of it failed at 0.358, the graph itself is untested |
| GNM transfer entropy, antisymmetric part   | **Yes, and structurally** — see below                                 | Strongest escape available                                                             |
| Rigid-cluster / pebble-game decomposition  | **Yes** — cluster membership is combinatorial, not metric             | Strongest in principle; no maintained Python implementation retrieved                  |

**Why the antisymmetric transfer entropy is the strongest candidate.** Every symmetric function of a
symmetric graph operator — `L⁺`, `exp(−tL)`, resistance, commute time, the CTQW transfer amplitude —
is a symmetric function of a distance-like object, and therefore inherits distance. Transfer entropy
in the harmonic approximation is asymmetric: `T(i→j) ≠ T(j→i)`, and the asymmetry is driven by the
_ratio_ of the two residues' fluctuation amplitudes rather than by their separation. Forming
`T(i→j) − T(j→i)` cancels the symmetric, distance-carrying part by construction and leaves a
mobility-ratio signal. That is a different measurement, not a transform of one we already have —
which is exactly the criterion `../exploration/lit/23-quantum-node-ranking.md` applies to separate genuinely new
observables from restatements. **The honest caveat: GNM fluctuation amplitude is itself strongly
burial-correlated, and burial is a closed axis (`../exploration/lit/24-residue-descriptors.md`). So the
prediction is that the antisymmetric TE will have low |ρ| against distance and may still be absorbed
by the matched-patch null through burial.** It must be run through `allo.scoring.score_arm` with the
`against` correlation printed, like everything else. Low distance correlation is a necessary
condition for a new signal, not a sufficient one.

**One prediction this section makes that is cheap to falsify.** If distance inheritance is the
mechanism, then the constructions in the "cannot escape" rows must show |ρ| against negated distance
clustered tightly around the 0.74–0.81 band we already measured, and the "substantial escape" rows
must show materially lower |ρ| — regardless of their AUC. That is a label-free test. It can be run
on every arm, including the `generalisation` tier, without opening a single label, because ρ against
distance needs no ground truth.

---

## What the literature does NOT support

- **"Graph construction does not matter."** Not supported, and the counter-evidence is specific:
  the same cutoff sweep that leaves AUROC flat (SD < 0.03) halves AUPRC, 0.70 → 0.36
  [doi:10.1101/2025.08.25.672254]. What _is_ supported is the narrower claim that the parameters of
  a distance-threshold graph, inside a sensible band, do not matter — replicated by
  doi:10.1186/1471-2105-13-292 (spread 0.004 across the top three of 45) and arXiv:0809.3715.
- **"Typed interaction edges beat plain contacts for site prediction."** No paper isolating this was
  retrieved. Our own measurement of `edge_class` weighting placed it 7th of 8. The tools (RING,
  Arpeggio, Graphein) are excellent and the claim behind them is unmeasured on this task.
- **"Higher resolution is better."** Contradicted in both directions. ProteinWorkshop's own caution
  is that backbone-only featurisation "may prevent overfitting on crystallisation artifacts"
  [arXiv:2406.13864], and Chennubhotla and Bahar's B-factor correlation _improved_ from 0.68 to 0.89
  under a 60× node reduction [doi:10.1038/msb4100075].
- **"Multi-relational graphs improve accuracy."** GearNet's justification is a degree-distribution
  argument, and its ablation table covers architecture, not edge construction [arXiv:2203.06125].
- **"Hierarchical graphs beat single-scale graphs on site prediction."** No ablation isolating the
  hierarchy against a matched single-scale graph was retrieved by the recorded search.
- **"A two-bead-per-residue graph is measurably better than one bead."** No measured comparison on a
  site-prediction or dynamics task was retrieved.
- **"Published allosteric-site accuracies are achievable targets."** AlloBench's leakage-controlled
  reappraisal puts every one of eight tools under 60 % even at a very low Jaccard cutoff
  (doi:10.1021/acsomega.5c01263), and CAPASP shows APOP and PASSer degrade specifically on apo input
  (doi:10.1007/s10822-026-00831-4).
- **"MJ-weighted networks help allosteric prediction."** No paper measuring this was retrieved. The
  retrieved applications are folding, threading and scoring.
- **Absence claims.** Every "not retrieved" above is scoped to the searches in §Method, per ADR 0019.
  None of them is a claim that the work does not exist.

---

## What this changes for our pipeline

- **S1 (graph construction).** The claim "graph construction does not matter" must be withdrawn and
  replaced with "the parameters of a distance-threshold graph do not matter, and we have not tested
  anything else". The twelve variants above are the untested space; items 1, 2, 3 and 6 are the four
  worth running first because each is cheap and each fails the distance-inheritance test in a
  different way.
- **S1.** Add `network.build(contact="voronoi", weighting="contact_area")` via Voronota. It is the
  only cutoff-free, occlusion-aware, size-unbiased construction with a maintained implementation, and
  its weight is the only edge weight in this survey that is not a function of distance and not a
  function of residue type.
- **S1.** Add a `min_seq_sep` knob to `network.build`. Deleting `|i − j| ≤ 2` is one line and removes
  the most distance-faithful substructure in every graph we own.
- **S5 (propagation).** Implement the antisymmetric GNM transfer entropy in `allo.classical.coupling`.
  It is the only construction retrieved that produces a directed residue graph from a static
  structure under C1, C2 and C6, and antisymmetrisation cancels the distance-carrying part by
  construction.
- **Evaluation, without touching the frozen protocol.** Chen et al. show a graph sweep that AUROC
  calls irrelevant and AUPRC calls decisive on the same models. Our 0.031 was measured on a rank
  metric in a small-positive-class regime. Nothing in `docs/benchmark/evaluation/` may change once a
  method has been scored — but the graph-choice _conclusion_ should be re-derived with a
  precision-sensitive readout reported alongside, and an ADR should record that the earlier
  conclusion was estimator-limited.
- **A label-free diagnostic to add to every run.** |ρ| against negated source distance is computable
  with no ground truth on any arm at any tier. Make it the first screen for a new construction: a
  construction that cannot beat 0.74 on |ρ| is a distance ranker whatever its AUC.
- **Coarse-graining (`CHALLENGE.md` §4.2).** Item 11 (SSE nodes) and item 12 (soft ownership) are the
  two constructions that answer the "demonstrate and prove" clause. Item 12 additionally supplies the
  reverse map to author numbering and a candidate readout in the same object.
- **Nothing here reopens C2.** A knowledge-based potential table, a Voronoi tessellation, a DSSP
  annotation and a GNM covariance are all functions of one static structure. ATD, CryptoSite and
  PocketMiner remain excluded.

---

## Method

**Databases.** PubMed E-utilities (`esummary.fcgi`, batched by PMID), PMC article pages, Europe PMC,
arXiv (`/abs`, `/html`, `ar5iv`), bioRxiv (`.full` HTML), Crossref REST
(`api.crossref.org/works?query.bibliographic=`), and general web search. Thirty query strings, listed
verbatim in the scope paragraph. Approximately 240 result records screened, 44 screened in, 38 cited.

**Retrieval notes and failures, recorded per convention §2.**

- **Crossref was the reliable identifier route.** Every DOI in §References was confirmed either by a
  Crossref `query.bibliographic` lookup or by a PubMed `esummary` call in this session, except the
  three flagged below.
- **What the DOI confirmation covers, and what it does not.** Those lookups return DOI, title,
  **first author**, journal, year, volume and pages, and all seven fields are confirmed for every
  reference not flagged. They do **not** return full author lists. Where §References prints
  co-authors beyond the first, those names are recalled and were not re-derived this session — they
  are the least reliable text in this file. **Cite by DOI, and re-derive the author list from the DOI
  before any entry reaches `docs/report/`.** Six entries whose first author could not be confirmed
  either are printed as `[Author list not retrieved this session.]` rather than guessed; that is
  deliberate, and those brackets must not be filled in from memory.
- **Publisher redirects blocked several full texts.** `nature.com` and `link.springer.com` both
  redirect to identity providers and returned no content; `pubs.acs.org` was not reachable. Ohm was
  recovered through PMC7395124, and the BMC contact-definition paper through PMC3534397.
- **Raw PDF fetches failed** for arXiv:2203.06125, arXiv:0809.3715 and the Chen bioRxiv preprint
  (binary content not decoded). Two were recovered: Chen et al. through the bioRxiv `.full` HTML,
  GearNet through `ar5iv.labs.arxiv.org`. **arXiv:0809.3715 was retrieved at abstract level only**,
  so its "eigenvectors conserved" claim is [VERIFIED-ABSTRACT] and its per-construction numbers were
  not obtained.
- **Three DOIs are recorded with a caveat and must be re-derived before they reach `docs/report/`:**
  RING 3.0 (`10.1093/nar/gkac365`), the 2025 TIBS residue-interaction-network review
  (`10.1016/j.tibs.2025.08.006`), and the GPCR allosteric-conservation record
  (`10.3390/ijms24021170`). Each was matched from a search result rather than confirmed through
  Crossref or PubMed in this session. RING 4.0 (`10.1093/nar/gkae337`) _was_ Crossref-confirmed and
  should be preferred as the citable RING reference.
- **Semantic Scholar** was not queried directly; `00-conventions.md` §3 records it as rate-limited
  (HTTP 429), and its indexed records surfaced through general web search instead.
- **Searched and not retrieved** (ADR 0019 scoping applies — these are search outcomes, not
  non-existence claims): a measured comparison of two-bead-per-residue against one-bead graphs; an
  ablation isolating typed interaction edges against plain contacts on site prediction; an ablation
  isolating a hierarchical graph against a matched single-scale graph; a measurement of an
  MJ-weighted network on an allosteric task; benchmark accuracy figures for STRESS, SPACER and
  binding leverage; a maintained Python implementation of the 3D body-bar pebble game.
- **Stopping rule.** Searching stopped for a question when two further queries returned only records
  already screened, or only records behind unreachable publishers. Q2 and Q5 reached saturation;
  Q1's multi-node sub-question and Q6's hierarchy sub-question did not — both are recorded above as
  "not retrieved" rather than as settled.
- **Leakage.** Nothing under `docs/benchmark/` was opened. No real label residue appears in this
  file. Repo numbers quoted here come from `../exploration/data/30-frozen-graph-profile.md` and
  `../exploration/README.md`, both of which are label-free by their own scope statements.

---

## References

1. Yuan C, Chen H, Kihara D. Effective inter-residue contact definitions for accurate protein fold recognition. BMC Bioinformatics. 2012;13:292. doi:10.1186/1471-2105-13-292. PMID 23140471; PMC3534397.
2. Chen SH, Lupo Pasini M, Hauck CD. Enhancing protein binding site residue prediction with graph neural networks: impacts of cutoff distance and feature selection. bioRxiv. 2025. doi:10.1101/2025.08.25.672254.
3. Jamasb AR, Morehead A, Joshi CK, Zhang Z, Didi K, Mathis SV, et al. Evaluating representation learning on the protein structure universe. ICLR 2024. arXiv:2406.13864.
4. Zhang Z, Xu M, Jamasb AR, Chenthamarakshan V, Lozano A, Das P, Tang J. Protein representation learning by geometric structure pretraining. ICLR 2023. arXiv:2203.06125.
5. Atilgan C, Inanc I, Atilgan AR. Residue network construction and predictions of elastic network models. arXiv:0809.3715. doi:10.48550/arXiv.0809.3715.
6. Esque J, Oguey C, de Brevern AG. Comparative analysis of threshold and tessellation methods for determining protein contacts. J Chem Inf Model. 2011;51(2):493-507. doi:10.1021/ci100195t. PMID 21226523.
7. Singh RK, Tropsha A, Vaisman II. Delaunay tessellation of proteins: four body nearest-neighbor propensities of amino acid residues. J Comput Biol. 1996;3(2):213-21. doi:10.1089/cmb.1996.3.213. PMID 8811483.
8. Olechnovič K, Venclovas Č. Voronota: a fast and reliable tool for computing the vertices of the Voronoi diagram of atomic balls. J Comput Chem. 2014;35(8):672-81. doi:10.1002/jcc.23538.
9. Olechnovič K, Venclovas Č. Voronota-LT: efficient, flexible and solvent-aware tessellation-based analysis of atomic interactions. bioRxiv. 2024. doi:10.1101/2024.02.05.577169.
10. Olechnovič K, Venclovas Č. VoroMQA: assessment of protein structure quality using interatomic contact areas. Proteins. 2017;85(6):1131-45. doi:10.1002/prot.25278.
11. Salamanca Viloria J, Allega MF, Lambrughi M, Papaleo E. An optimal distance cutoff for contact-based protein structure networks using side-chain centers of mass. Sci Rep. 2017;7:2838. doi:10.1038/s41598-017-01498-6. PMID 28588190; PMC5460117.
12. Sobieraj M, Setny P. Entropy-based distance cutoff for protein internal contact networks. Proteins. 2021;89(10):1333-9. doi:10.1002/prot.26154. PMID 34053102.
13. Del Conte A, Camagni GF, Clementel D, Minervini G, Monzon AM, Ferrari C, et al. RING 4.0: faster residue interaction networks with novel interaction types across over 35,000 different chemical structures. Nucleic Acids Res. 2024;52(W1):W306-12. doi:10.1093/nar/gkae337.
14. Clementel D, Del Conte A, Monzon AM, Camagni GF, Minervini G, Piovesan D, Tosatto SCE. RING 3.0: fast generation of probabilistic residue interaction networks from structural ensembles. Nucleic Acids Res. 2022;50(W1):W651-6. doi:10.1093/nar/gkac365. _(DOI matched from a search record, not Crossref-confirmed this session.)_
15. Jubb HC, Higueruelo AP, Ochoa-Montaño B, Pitt WR, Ascher DB, Blundell TL. Arpeggio: a web server for calculating and visualising interatomic interactions in protein structures. J Mol Biol. 2017;429(3):365-71. doi:10.1016/j.jmb.2016.12.004. PMID 27964945; PMC5282402.
16. Jamasb AR, Viñas Torné R, Ma EJ, Harris C, Huang K, Hall D, et al. Graphein — a Python library for geometric deep learning and network analysis on protein structures and interaction networks. bioRxiv. 2020. doi:10.1101/2020.07.15.204701. Also Adv Neural Inf Process Syst. 2022;35:27153-67. doi:10.52202/068431-1969.
17. Miyazawa S, Jernigan RL. Residue-residue potentials with a favorable contact pair term and an unfavorable high packing density term, for simulation and threading. J Mol Biol. 1996;256(3):623-44. doi:10.1006/jmbi.1996.0114.
18. Bahar I, Atilgan AR, Erman B. Direct evaluation of thermal fluctuations in proteins using a single-parameter harmonic potential. Fold Des. 1997;2(3):173-81. doi:10.1016/s1359-0278(97)00024-2.
19. Atilgan AR, Durell SR, Jernigan RL, Demirel MC, Keskin O, Bahar I. Anisotropy of fluctuation dynamics of proteins with an elastic network model. Biophys J. 2001;80(1):505-15. doi:10.1016/s0006-3495(01)76033-x.
20. Yang L, Song G, Jernigan RL. Protein elastic network models and the ranges of cooperativity. Proc Natl Acad Sci USA. 2009;106(30):12347-52. doi:10.1073/pnas.0902159106. PMID 19617554.
21. Hacısüleyman A, Erman B. Entropy transfer between residue pairs and allostery in proteins: quantifying allosteric communication in ubiquitin. PLoS Comput Biol. 2017;13(1):e1005319. doi:10.1371/journal.pcbi.1005319.
22. Hacısüleyman A, Erman B. Causality, transfer entropy and allosteric communication landscapes in proteins with harmonic interactions. bioRxiv. 2016. doi:10.1101/084764.
23. Wang J, Jain A, McDonald LR, Gambogi C, Lee AL, Dokholyan NV. Mapping allosteric communications within individual proteins. Nat Commun. 2020;11:3862. doi:10.1038/s41467-020-17618-2. PMID 32737291; PMC7395124.
24. Panjkovich A, Daura X. PARS: a web server for the prediction of protein allosteric and regulatory sites. Bioinformatics. 2014;30(9):1314-5. doi:10.1093/bioinformatics/btu002.
25. Panjkovich A, Daura X. Exploiting protein flexibility to predict the location of allosteric sites. BMC Bioinformatics. 2012;13:273. doi:10.1186/1471-2105-13-273. PMC3562710.
26. Huang W, Lu S, Huang Z, Liu X, Mou L, Luo Y, et al. Allosite: a method for predicting allosteric sites. Bioinformatics. 2013;29(18):2357-9. doi:10.1093/bioinformatics/btt399. PMID 23842804.
27. Song K, Liu X, Huang W, Lu S, Shen Q, Zhang L, Zhang J. Improved method for the identification and validation of allosteric sites. J Chem Inf Model. 2017;57(9):2358-63. doi:10.1021/acs.jcim.7b00014.
28. Greener JG, Sternberg MJE. AlloPred: prediction of allosteric pockets on proteins using normal mode perturbation analysis. BMC Bioinformatics. 2015;16:335. doi:10.1186/s12859-015-0771-1.
29. Tian H, Jiang X, Tao P. PASSer: prediction of allosteric sites server. Mach Learn Sci Technol. 2021;2(3):035015. doi:10.1088/2632-2153/abe6d6.
30. Xiao S, Tian H, Tao P. PASSer2.0: accurate prediction of protein allosteric sites through automated machine learning. Front Mol Biosci. 2022;9:879251. doi:10.3389/fmolb.2022.879251. PMID 35898310; PMC9309527.
31. Tian H, Xiao S, Jiang X, Tao P. PASSer: fast and accurate prediction of protein allosteric sites. Nucleic Acids Res. 2023;51(W1):W427-31. doi:10.1093/nar/gkad303.
32. Xiao S, Tian H, Tao P. PASSerRank: prediction of allosteric sites with learning to rank. arXiv:2302.01117.
33. Zha J, Li M, Kong R, Lu S, Zhang J. AlloReverse: multiscale understanding among hierarchical allosteric regulations. Nucleic Acids Res. 2023;51(W1):W33-8. doi:10.1093/nar/gkad279. PMID 37070199; PMC10320067.
34. Mitternacht S, Berezovsky IN. Binding leverage as a molecular basis for allosteric regulation. PLoS Comput Biol. 2011;7(9):e1002148. doi:10.1371/journal.pcbi.1002148.
35. Goncearenco A, Mitternacht S, Yong T, Eisenhaber B, Eisenhaber F, Berezovsky IN. SPACER: server for predicting allosteric communication and effects of regulation. Nucleic Acids Res. 2013;41(W1):W266-72. doi:10.1093/nar/gkt460. PMID 23737445; PMC3692057.
36. Clarke D, Sethi A, Li S, Kumar S, Chang RWF, Chen J, Gerstein M. Identifying allosteric hotspots with dynamics: application to inter- and intra-species conservation. Structure. 2016;24(5):826-37. doi:10.1016/j.str.2016.03.008. PMID 27066750; PMC4883016.
37. Atilgan C, Atilgan AR. Perturbation-response scanning reveals ligand entry-exit mechanisms of ferric binding protein. PLoS Comput Biol. 2009;5(10):e1000544. doi:10.1371/journal.pcbi.1000544.
38. Ota N, Agard DA. Intramolecular signaling pathways revealed by modeling anisotropic thermal diffusion. J Mol Biol. 2005;351(2):345-54. doi:10.1016/j.jmb.2005.05.043. PMID 16005893.
39. Cimermancic P, Weinkam P, Rettenmaier TJ, Bichmann L, Keedy DA, Woldeyes RA, et al. CryptoSite: expanding the druggable proteome by characterization and prediction of cryptic binding sites. J Mol Biol. 2016;428(4):709-19. doi:10.1016/j.jmb.2016.01.029.
40. Meller A, Ward M, Borowsky J, Kshirsagar M, Lotthammer JM, Oviedo F, et al. Predicting locations of cryptic pockets from single protein structures using the PocketMiner graph neural network. Nat Commun. 2023;14:1177. doi:10.1038/s41467-023-36699-3.
41. Smith Z, Strobel M, Vani BP, Tiwary P. Graph attention site prediction (GrASP): identifying druggable binding sites using graph neural networks with attention. J Chem Inf Model. 2024;64(7):2637-44. doi:10.1021/acs.jcim.3c01698. Preprint doi:10.1101/2023.07.25.550565.
42. Le Guilloux V, Schmidtke P, Tuffery P. Fpocket: an open source platform for ligand pocket detection. BMC Bioinformatics. 2009;10:168. doi:10.1186/1471-2105-10-168. PMID 19486540.
43. Schmidtke P, Le Guilloux V, Maupetit J, Tuffery P. fpocket: online tools for protein ensemble pocket detection and tracking. Nucleic Acids Res. 2010;38(Web Server issue):W582-9. doi:10.1093/nar/gkq383.
44. Chennubhotla C, Bahar I. Markov propagation of allosteric effects in biomolecular systems: application to GroEL-GroES. Mol Syst Biol. 2006;2:36. doi:10.1038/msb4100075. PMC1681507.
45. Chennubhotla C, Bahar I. Signal propagation in proteins and relation to equilibrium fluctuations. PLoS Comput Biol. 2007;3(9):1716-26. doi:10.1371/journal.pcbi.0030172. PMC1988854.
46. Amor B, Yaliraki SN, Woscholski R, Barahona M. Uncovering allosteric pathways in caspase-1 using Markov transient analysis and multiscale community detection. Mol Biosyst. 2014;10(8):2247-58. doi:10.1039/c4mb00088a.
47. Delvenne JC, Yaliraki SN, Barahona M. Stability of graph communities across time scales. Proc Natl Acad Sci USA. 2010;107(29):12755-60. doi:10.1073/pnas.0903215107.
48. Schaub MT, Delvenne JC, Yaliraki SN, Barahona M. Markov dynamics as a zooming lens for multiscale community detection: non clique-like communities and the field-of-view limit. PLoS ONE. 2012;7(2):e32210. doi:10.1371/journal.pone.0032210. PMC3288079.
49. Loukas A. Graph reduction with spectral and cut guarantees. J Mach Learn Res. 2019;20(116):1-42. arXiv:1808.10650.
50. Dörfler F, Bullo F. Kron reduction of graphs with applications to electrical networks. arXiv:1102.2950.
51. Díaz J, Mitsche D, Perarnau G, Pérez-Giménez X. On the relation between graph distance and Euclidean distance in random geometric graphs. Adv Appl Probab. 2016;48(3):848-64. doi:10.1017/apr.2016.31. Preprint arXiv:1404.4757.
52. Yang LW, Chng CP. Coarse-grained models reveal functional dynamics — I. Elastic network models, theories, comparisons and perspectives. Bioinform Biol Insights. 2008;2:25-45. doi:10.4137/bbi.s460. PMC2735964.
53. [Author list not retrieved this session.] Allo-PED: leveraging protein language models and structure features for allosteric site prediction. bioRxiv. 2025. doi:10.1101/2025.03.28.645953. Conference version: AlloPED, in _Bioinformatics Research and Applications_, doi:10.1007/978-981-95-0695-8_31.
54. [AlloBench. Author list and exact title not retrieved this session.] ACS Omega. 2025. doi:10.1021/acsomega.5c01263. _(Quoted via `00-conventions.md` §6, which is the authority for this claim; not re-retrieved here.)_
55. [CAPASP. Author list not retrieved this session.] A systematic evaluation of protein allosteric site prediction tools with independent datasets. J Comput Aided Mol Des. 2026. doi:10.1007/s10822-026-00831-4. _(Quoted via `00-conventions.md` §6; not re-retrieved here.)_
56. [Author list not retrieved this session.] Decoding protein structures with residue interaction networks. Trends Biochem Sci. 2025. Publisher article ID S0968-0004(25)00195-1. doi:10.1016/j.tibs.2025.08.006. _(DOI **inferred**, not Crossref- or PubMed-confirmed. Re-derive before use.)_
57. [Author list not retrieved this session.] Conservation of allosteric ligand binding sites in G-protein coupled receptors. Int J Mol Sci. 2023. PMC9847135. doi:10.3390/ijms24021170. _(DOI and volume/pages **inferred** from a search record, not Crossref- or PubMed-confirmed. Re-derive before use.)_
58. [Author list not retrieved this session.] Protein–protein and protein–nucleic acid binding site prediction via interpretable hierarchical geometric deep learning (GraphRBF). GigaScience. 2024;13:giae080. doi:10.1093/gigascience/giae080. PMC11528319.
59. Marrink SJ, Risselada HJ, Yefimov S, Tieleman DP, de Vries AH. The MARTINI force field: coarse grained model for biomolecular simulations. J Phys Chem B. 2007;111(27):7812-24. doi:10.1021/jp071097f.
60. Periole X, Cavalli M, Marrink SJ, Ceruso MA. Combining an elastic network with a coarse-grained molecular force field: structure, dynamics, and intermolecular recognition. J Chem Theory Comput. 2009;5(9):2531-43. doi:10.1021/ct9002114.
