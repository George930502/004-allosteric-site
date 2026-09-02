# Adjacent-Task Transfer: Frameworks Built for Other Problems

**Scope:** Methods whose stated purpose is _not_ allosteric-site prediction, screened for whether
their mathematics transfers to "rank residues by dynamic connectivity to a named source on a
contact graph, from one static apo structure." Excludes every method whose title or stated goal is
allosteric-site or allosteric-communication prediction itself.
**Sibling files:** 01 and 02 cover the direct allosteric-site-prediction literature (ENM/GNM
allostery tools, bond-to-bond propensity, coevolution-for-allostery, MD-network methods) — several
items below are cross-referenced there rather than re-argued here. File 00 is the conventions this
file obeys.
**Retrieved:** 2026-08-25.

---

## Why borrow

`docs/evidence/method-landscape/00-conventions.md` §5 records that a teammate repository has already measured
eleven quantum insertion points built _for_ this problem, and all eleven lost to a one-line
classical geometric baseline (`-distance`, AUC 0.617). The diagnosed mechanism — a single-particle
Hermitian walk on a graph carries no information beyond its transfer amplitude — rules out most of
the observable space a method designed from scratch for allostery would reach for. R4 says work as
an expert in _this field_ would, but also to search for what a neighbouring field already solved.
This file is that search: frameworks built to rank, localize, or control nodes on a graph for a
different reason, screened for whether the reason is close enough that the mathematics ports.

---

## 1. Protein–protein interaction hot-spot prediction

A PPI hot spot and an allosteric site are both "a residue whose local perturbation changes a
distant or global functional outcome," but PPI hot-spot methods are trained to find residues _at
an interface with a second protein_, not residues coupled through the _same_ protein's own
contact network to an internal active site. What they give us is a validated, orthogonal
per-residue feature — energetic or geometric interface propensity — computed with tools that never
see a trajectory.

- **ScanNet** — geometric deep learning directly on atomic coordinates and their spatio-chemical
  neighbourhood, trained on PDB protein/antibody complexes to output a per-residue binding-site
  probability. Tubiana, Schneidman-Duhovny & Wolfson, _Nat Methods_ 19:730–739 (2022),
  doi:10.1038/s41592-022-01490-7 [VERIFIED-ABSTRACT].
- **MaSIF** — geometric deep learning on the molecular surface mesh; three heads (ligand-pocket,
  PPI-site, ultrafast complementarity search) trained on PDB structures. Gainza et al., _Nat
  Methods_ (2020), doi:10.1038/s41592-019-0666-6 [VERIFIED-ABSTRACT].
- **PeSTo** — a parameter-free geometric transformer on raw atom coordinates and element identity
  (no physicochemical parameters at all), trained on PDB complexes, extended to nucleic
  acid/lipid/ion/small-molecule interfaces. Krapp, Abriata, Cortés Rodriguez & Dal Peraro, _Nat
  Commun_ 14:2175 (2023), doi:10.1038/s41467-023-37701-8 [VERIFIED-ABSTRACT].
- **Hot-spot energetics / alanine-scanning surrogates** — Bogan & Thorn's O-ring theory: binding
  free energy at an interface concentrates in a small subset of residues surrounded by an
  occluding ring. Bogan & Thorn, _J Mol Biol_ 280:1–9 (1998), doi:10.1006/jmbi.1998.1843
  [VERIFIED-ABSTRACT]. Physics-based computational alanine scanning (e.g. Rosetta ΔΔG) reproduces
  this from a single static structure with no trajectory and no ML training on dynamics data.
- **FTMap** — exhaustive rigid-body docking of ~16 small organic probes against a static structure,
  scored by a physics-based energy function; consensus probe clusters mark druggable hot spots.
  Brenke et al./Kozakov & Vajda, _Nat Protoc_ (2015), doi:10.1038/nprot.2015.043
  [VERIFIED-ABSTRACT]. No MD, no ML.

**C1/C2 verdict:** all five are legal as inputs to our pipeline — trained or parameterised on
static PDB structures, never on the target's own holo complex, never on an MD trajectory. What
they give us that a connectivity ranker does not: an _independent, structure-only_ prior on which
surface residues are energetically or geometrically "hot," usable as a feature to correlate
against — not replace — the propagation score, or as a decoy-pocket generator distinct from
`cavity_volume`.

---

## 2. Cryptic and transient pocket detection

CHALLENGE.md §3 names cryptic-pocket detection as the paradigm shift this project targets
("static pocket detection → dynamic signal mapping"), and CrypToth is cited directly in
`CHALLENGE.md` reference 2. Every leading tool in this category is MD-based; the C2 verdict is the
single most important thing this section can report.

- **CryptoSite** — supervised classifier (structure, sequence, evolutionary conservation, and
  "dynamic attributes") trained on 93 curated apo–holo cryptic-pocket pairs; test AUC 0.83.
  Cimermancic et al., _J Mol Biol_ (2016), PubMed 26854760 [VERIFIED-ABSTRACT]. The original
  feature set is reported to include short-simulation-derived dynamics attributes; the extent
  could not be pinned down from abstract-level retrieval this session — **[UNVERIFIED]** whether a
  structure/sequence/conservation-only subset was ever benchmarked in isolation. Treat as **likely
  C2-violating** until the feature list is confirmed clean.
- **PocketMiner** — graph neural network trained to predict where pockets open _in MD
  simulations_; ROC-AUC 0.87 vs >1000x faster than the simulations it was trained to imitate.
  Meller et al., _Nat Commun_ 14:1177 (2023), doi:10.1038/s41467-023-36699-3
  [VERIFIED-ABSTRACT]. **C2 violation, explicit** (already flagged in conventions §4).
- **CrypToth** — mixed-solvent MD + topological data analysis. doi:10.1021/acs.jcim.4c02111
  (`CHALLENGE.md` ref 2) [VERIFIED-FULLTEXT, per conventions §4]. **C2 violation, explicit.**
- **SWISH** ("Sampling Water Interfaces through Scaled Hamiltonians") and mixed-solvent MD
  generally — Hamiltonian replica-exchange cosolvent MD used directly to find cryptic sites.
  Oleinikovas, Saladino, Cossins & Gervasio, _J Am Chem Soc_ 138:14257–14263 (2016),
  doi:10.1021/jacs.6b05425 [VERIFIED-ABSTRACT]. **C2 violation, explicit** — the method _is_ an MD
  protocol, not a downstream analysis of one.
- **FTMap** (repeated from §1) is the one member of this category that is not MD at all: a static
  multi-probe docking scan. It cannot detect a pocket that is fully closed in the apo structure,
  but it can be run on any conformer an MD-free ensemble generator produces (§3), which is the
  legal route to the same biological question.

**What this gives us that an allosteric predictor does not:** a mature, quantitative definition of
"cryptic" (pocket volume/druggability score before vs. after some perturbation) that our own
`cavity_volume` baseline (conventions §6) is a zero-parameter instance of. Every ML tool that beat
a geometric baseline in this literature did so by training on MD; none of that lift is legally
available to us. FTMap plus an MD-free ensemble generator (§3) is the only path in this category
that survives C2 intact.

---

## 3. Conformational-ensemble generation without MD

This is the direct route around C2: the challenge's own primary objective (`CHALLENGE.md` §4.1)
offers "based on structural fluctuations" as an alternative phrasing to "dynamic connectivity,"
and every tool below produces per-residue fluctuation information from a single apo structure
without ever running a trajectory. This is the category most worth the pipeline's attention, and
it gets the most space here per the task brief.

- **Str2Str** — score-based diffusion, zero-shot, trained _only_ on PDB crystal structures with
  "no dependency on any simulation data during training or inference." Lu, Li et al., ICLR 2024,
  arXiv:2306.03117 [VERIFIED-ABSTRACT]. **Cleanest C2 verdict in this section.**
- **AlphaFlow / ESMFlow** — flow-matching fine-tune of AlphaFold2/ESMFold. Two training regimes
  exist: a **PDB-only** variant ("When trained and evaluated on the PDB, our method provides a
  superior combination of precision and diversity compared to AlphaFold with MSA subsampling")
  and an **MD-finetuned** variant ("When further trained on ensembles from all-atom MD, our method
  accurately captures conformational flexibility..."). Jing et al., ICML 2024, arXiv:2402.04845
  [VERIFIED-ABSTRACT, confirmed via WebFetch of the abstract]. **The PDB-only checkpoint is
  C2-legal; the publicly emphasised MD-finetuned checkpoint (trained on ATLAS MD ensembles) is
  not** — and it is the one most tutorials default to. A prediction-path use of either tool must
  name and verify which checkpoint it loads.
- **BioEmu** — diffusion model over AlphaFold2's Evoformer representations, "integrates more than
  200 milliseconds of molecular dynamics (MD) simulations, static structures, and experimental
  protein stabilities" directly into training. Lewis, Hempel et al., _Science_ 389 (2025),
  doi:10.1126/science.adv9817 [VERIFIED-ABSTRACT]. **C2 violation, explicit and unconditional** —
  every public BioEmu checkpoint has MD-trained weights, so even a zero-new-MD inference call
  still puts MD-trained weights in the prediction path.
- **AlphaFold MSA-subsampling tricks** — no fine-tuning at all; perturb the _input_ to an
  off-the-shelf AlphaFold2 (itself trained on PDB structures, not MD) by shrinking or clustering
  the MSA, and different conformational basins fall out. del Alamo, Sala, Mchaourab & Meiler,
  _eLife_ 11:e75751 (2022), doi:10.7554/eLife.75751 [VERIFIED-ABSTRACT]; Wayment-Steele et al.
  (AF-Cluster), _Nature_ 625:832–839 (2024), doi:10.1038/s41586-023-06832-9 [VERIFIED-ABSTRACT].
  **C2-legal**, provided the MSA is built from sequence databases only, with no structural
  template drawn from the target's own holo form (a build-time guard our `inputs.py` would need
  to enforce, not a property of the method itself).
- **Normal-mode / elastic-network-guided conformational search** — perturb a structure along the
  lowest-frequency modes of an ANM/GNM Hessian (a purely topological, C6-native object), then
  reconstruct atomistic detail. This is the mechanism inside Zheng (2023) (`CHALLENGE.md` ref 1,
  doi:10.1063/5.0141630) [VERIFIED-ABSTRACT] and its ICONGENI/NGENI-family relatives for
  transition-pathway interpolation. **Cross-reference:** Zheng (2023)'s site-ranking result (top-30
  modes exposing cryptic pockets detectable by Concavity, tested on GluR2/GroEL/GPCR/myosin) is
  allosteric-site prediction and belongs to files 01/02. What is genuinely transferable here,
  independent of that wrapper, is the _sampling mechanism itself_: for any protein, restructure
  along the lowest-k ENM modes to get a small conformational ensemble, entirely from one apo
  Hessian, with **zero MD and zero learned weights**. That makes it the single cheapest, most
  clearly C1/C2-legal ensemble generator in this file.

**What this gives us that an allosteric predictor does not:** every tool above turns "one static
structure" into "a small, MD-free ensemble," from which per-residue positional variance (an
ab-initio RMSF/B-factor proxy) or contact-frequency edge weights can be computed directly. That
converts the input graph from a single binary contact map into a fluctuation-aware weighted graph
— a strictly larger input for the same C1/C2 budget, and a literal implementation of the
challenge's "based on structural fluctuations" clause.

---

## 4. Protein dynamics predicted from a static structure

A narrower, single-shot version of §3: predict a _scalar_ flexibility value per residue, not an
ensemble.

- **B-factor prediction GNNs** — graph neural networks on the atom graph, trained on
  crystallographic B-factors (experimental, not MD-derived); best model reaches Pearson r ≈ 0.71
  on >4,000 proteins. arXiv:2408.12519 [VERIFIED-ABSTRACT]. **C2-legal** (labels are experimental
  B-factors, not simulation output).
- **RMSF-net** — GNN combining atomic structure with cryo-EM density, residue-level correlation
  0.765 ± 0.109 against a "large-scale protein dynamics dataset." Nat Commun 15:5538 (2024),
  doi:10.1038/s41467-024-49858-x [VERIFIED-ABSTRACT]. **[UNVERIFIED]** whether the RMSF training
  labels are MD-derived — the retrieved abstract does not state the label source explicitly;
  flag before use.
- **NMR order-parameter prediction** — random forest on protein NMR structure _ensembles_
  (independent experimental conformer sets, not a trajectory) predicting backbone ¹H-¹⁵N S²;
  Pearson r = 0.817 on a 10-protein test set. Wang et al., _J Biomol NMR_ (2024),
  doi:10.1007/s10858-024-00435-w [VERIFIED-ABSTRACT]. **C2-legal.**
- **DynaMine** — linear regression from **sequence alone** (no structure needed) predicting
  backbone S² order parameters, trained on curated NMR relaxation data. Cilia et al., _Nat Commun_
  4:2741 (2013) [VERIFIED-ABSTRACT]. **C2-legal**, and notably C1-agnostic — it needs no structure
  at all, so it cannot leak holo geometry even in principle.

**What this gives us that an allosteric predictor does not:** a second, independent MD-free route
to per-residue flexibility that does not go through an ENM Hessian at all — useful as a
cross-check that a propagation-based ranking is not simply rediscovering "flexible residues are
close to the active site" (the same confound the `-distance` baseline already exposes).

---

## 5. Mutation-effect and epistasis prediction

Epistasis between distant residues is allosteric coupling measured through sequence variation
instead of through structural dynamics — the same physical claim, a different measurement channel.

- **EVcouplings / DCA / GREMLIN** — pairwise Potts/MRF models fit to a target's own sequence
  family MSA, producing an evolutionary-coupling (EC) strength per residue pair. Marks/Sander lab,
  _Bioinformatics_ 35:1582–1584 (2019) [VERIFIED-ABSTRACT]; Kamisetty, Ovchinnikov & Baker, _PNAS_
  110 (2013), doi:10.1073/pnas.1314045110 [VERIFIED-ABSTRACT]. **C2-legal** — needs only a
  sequence database, never a trajectory, never the target's holo structure.
- **Statistical Coupling Analysis / protein sectors** (Ranganathan) — spectral decomposition of
  the SCA coevolution matrix into physically contiguous "sectors" that link the active site to
  distal surface residues. This is a coevolution method _explicitly framed as allosteric-pathway
  detection_, so it is cross-referenced to files 01/02 rather than re-argued here.
- **Direct coupling analysis of epistasis in allosteric _materials_** — DCA applied to _in silico_
  evolved spring networks with a known mechanical ground truth (the source-target strain response
  of §8). Result: "DCA predicts well the cost of point mutations but... fails to capture long-range
  epistasis." Bravi, Ravasio, Brito & Wyart, _PLOS Comput Biol_ 16:e1007630 (2020),
  doi:10.1371/journal.pcbi.1007630 [VERIFIED-ABSTRACT]. This is a **negative result with a known
  ground truth**, and it is the most relevant piece of evidence in this section: the one time DCA
  was checked against a mechanical allosteric coupling it was supposed to detect, it failed
  precisely at the long range that defines allostery. It is a warning against a coevolution-based
  classical baseline, not a proposal for one.
- **ESM-1v / protein-language-model zero-shot DMS surrogates** — per-mutation log-odds from a
  masked language model, aggregable to a per-residue mutational-sensitivity score. Meier et al.,
  arXiv:2107.09598 / bioRxiv:2021.07.09.450648 [VERIFIED-ABSTRACT]. **C2-legal** (sequence-only).
  **Already tried and already failed here**: conventions §5 records that protein language models
  collapse on allosteric sites specifically (AUPR 0.64–0.76 on orthosteric vs. **0.06** on
  allosteric in the same proteins). This transfer is closed, not new.
- **ThermoMPNN** — ProteinMPNN backbone (trained on PDB structures) plus a lightweight ΔΔG(folding)
  head, trained via transfer learning on the Megascale experimental stability dataset. Dieckhaus,
  Brocidiacono, Randolph & Kuhlman, _PNAS_ 121:e2314853121 (2024), doi:10.1073/pnas.2314853121
  [VERIFIED-ABSTRACT]. **C2-legal** (no MD anywhere in the training chain). Gives a per-residue
  "how load-bearing is this position for folding stability" score, distinguishable in principle
  from "how load-bearing is this position for signal transmission."

---

## 6. Communication-pathway and information-flow analysis

Nearly every method in this category was built _for_ allosteric communication and is closer to
files 01/02's territory than to a genuine adjacent-task import; it is included because the task
brief asks for it, and because the mathematics originates outside biology even where the
application does not.

- **Transfer entropy** — Schreiber-formulated directional information flow between residue pairs.
  As practiced on MD fluctuation time series (van der Vaart and successors; e.g. _PLOS Comput
  Biol_ 13:e1005319 (2017) [VERIFIED-ABSTRACT]), it requires a trajectory: **C2 violation**. A
  second, closed-form variant computes the same directional quantity analytically from a Gaussian
  Network Model's harmonic covariance, "allowing calculation times to be performed in seconds"
  with no trajectory (bioRxiv:084764 [VERIFIED-ABSTRACT]). **This GNM-analytic variant is
  C2-legal**, and it is the one member of this family that produces something a plain contact
  graph cannot: a **directed, asymmetric** edge weight. Conventions §5 states a real symmetric
  contact graph supplies "neither non-reciprocal hopping nor gain and loss" — a directed
  transfer-entropy edge set is a legal, MD-free way to add exactly that structure, worth testing
  before concluding non-Hermitian methods are foreclosed for lack of an edge-direction source.
- **Mutual-information pathway analysis** (McClendon 2009), **current-flow betweenness on an
  MD-covariance-weighted graph** (Botello-Smith & Luo, bioRxiv:259572 [VERIFIED-ABSTRACT]), **force
  distribution analysis** (Stacklies, Seifert & Gräter, _BMC Bioinformatics_ 12:101 (2011)
  [VERIFIED-ABSTRACT], "uses frames from MD simulation"), and **suboptimal-path / Markov
  propagation analysis** (Chennubhotla & Bahar, `CHALLENGE.md` ref 8 — already a C6 citation) are
  all, as published, **MD-trajectory-dependent: C2 violation.**
- The one legal reading in this group: **current-flow betweenness computed on a purely topological
  weighted contact graph**, with no MD-derived covariance in the edge weights at all. The
  observable itself is from network science (Newman, _Soc Netw_ 27:39–54 (2005)), not biology; its
  only published protein application weights edges from MD. A topology-only version has not been
  retrieved as tried for protein allostery — see the transfer table and §7.

---

## 7. Graph and network science outside biology

This is where the least-explored territory is. None of the items below were built with proteins in
mind, and — with the two exceptions noted — none were retrieved as having been applied to a
single-protein residue contact network at all.

- **Structural controllability** (minimum driver-node set via maximum matching) and its
  **observability dual** (minimum sensor-node set). Liu, Slotine & Barabási, _Nature_ 473:167–173
  (2011), doi:10.1038/nature10011 [VERIFIED-ABSTRACT]. **Has** been applied to a protein network
  before — but at proteome scale, treating whole proteins as nodes and PPIs as edges, to find
  disease genes and drug targets (Vinayagam et al., _PNAS_ 113:4976–4981 (2016),
  doi:10.1073/pnas.1603992113 [VERIFIED-ABSTRACT]; "indispensable" driver proteins ≈ 21% of the
  network). **Not retrieved at residue resolution, on a single structure's contact graph, for
  allosteric-site prediction.**
- **Target control** — the minimum driver-node set needed to control a _specified target subset_,
  not the whole network (Gao, Liu, D'Souza & Barabási, _Nat Commun_ 5:5415 (2014),
  doi:10.1038/ncomms6415 [VERIFIED-ABSTRACT]) and **control centrality** — the number of nodes a
  single node can control alone (Liu, Slotine & Barabási, _PLoS ONE_ 7:e44459 (2012),
  doi:10.1371/journal.pone.0044459 [VERIFIED-ABSTRACT]). Target = the active site; output = which
  residues are structurally necessary or individually sufficient to actuate it. **Not retrieved as
  applied to protein allostery** — see STEP 3(c) below.
- **Source localization** — maximum-likelihood estimate of a diffusion source from sparse observer
  arrival times. Pinto, Thiran & Vetterli, "Locating the Source of Diffusion in Large-Scale
  Networks" (2012) [VERIFIED-ABSTRACT via retrieved abstract/EPFL record]. Inverting the direction
  again: treat each candidate distal residue as a hypothetical source, score it by how well it
  predicts an observed (or assumed) arrival pattern at the active site. **Not retrieved as applied
  to protein allostery.**
- **Influence maximization** — greedy submodular seed-set selection maximizing expected cascade
  size under the independent-cascade/linear-threshold models. Kempe, Kleinberg & Tardos, KDD 2003
  [VERIFIED-ABSTRACT]. Directly reframes the challenge's "top-5 hit list" deliverable: instead of
  five independently top-scoring residues (which can be five neighbours all reporting the same
  channel), select the five whose _joint_ expected influence on the active site is maximal, which
  accounts for redundancy between candidates. **Not retrieved as applied to protein allostery, and
  not retrieved as a reframing of any top-k allosteric hit list.**
- **Graph signal processing / spectral graph wavelets** — a signal localized at a source vertex,
  filtered by a spectral kernel g(L) of the graph Laplacian, read out at every other vertex, at a
  chosen scale. Hammond, Vandergheynst & Gribonval, _Appl Comput Harmon Anal_ (2011)
  [VERIFIED-ABSTRACT via retrieved title/venue]; Shuman et al. survey, _IEEE Signal Process Mag_
  30:83–98 (2013) [VERIFIED-ABSTRACT]. GSP **has** been applied to protein residue networks before,
  but for global biophysical property prediction (alpha/beta content, globularity, folding rate)
  via Lasso regression on Fourier-decomposed node signals, not for a source-anchored per-residue
  ranking (bioRxiv:2021.01.02.425090, published Physica A (2023) [VERIFIED-ABSTRACT]). **A
  source-localized wavelet coefficient, active site as the delta signal, has not been retrieved as
  tried for allosteric ranking** — though see the caution below in STEP 3(a).
- **Effective resistance / commute time / Kirchhoff index** — Klein & Randić's resistance distance,
  built from the Moore–Penrose pseudo-inverse of the (weighted) graph Laplacian; equal to random-walk
  commute time up to a normalization by total graph volume [VERIFIED-ABSTRACT, general graph-theory
  literature]. **Current-flow betweenness** (Newman 2005) is the same object aggregated over all
  source-target pairs rather than anchored at one named source. See STEP 3(a) — this is the
  strongest candidate in the whole file.
- **Katz/Bonacich centrality and communicability** — $(I-\alpha A)^{-1}$ or $\exp(\beta A)$ applied
  to a source indicator vector; eigenvector centrality is the $\alpha \to \alpha_{\max}$ limit of
  Katz. Estrada & Hatano, "Communicability in complex networks," _Phys Rev E_ 77:036111 (2008),
  doi:10.1103/PhysRevE.77.036111 [VERIFIED-ABSTRACT]. Standard in general network science; a
  source-anchored (not global) reading is not retrieved as applied to protein allostery, but its
  large-α behaviour reduces toward eigenvector centrality, already on the "must clear" bar
  (conventions §6 item 3) — limited expected headroom.

---

## 8. Physical analogies with directly transferable mathematics

- **Allosteric mechanical metamaterials** — Rocks, Pashine, Bischofberger, Goodrich, Liu & Nagel,
  "Designing allostery-inspired response in mechanical networks," _PNAS_ 114:2520–2525 (2017),
  doi:10.1073/pnas.1612139114, arXiv:1607.08562 [VERIFIED-ABSTRACT]. See STEP 3(b).
- **Rigidity theory / pebble game / FIRST / Constraint Network Analysis** — combinatorial
  constraint counting (Jacobs & Thorpe, 1995) that decomposes a bond network into rigid clusters
  and flexible hinges with no energy minimization and no dynamics. Extended into a maintained tool
  (FIRST) and a Python front end, Constraint Network Analysis, doi:10.1021/ci400044m
  [VERIFIED-ABSTRACT]. See STEP 3(e) — **this one has already been used for allosteric-site
  prediction.**
- **Tensegrity** (Ingber) — a qualitative structural-engineering analogy (balanced
  tension/compression elements) for cytoskeletal mechanics. No computational allostery method
  built on it was retrieved at residue resolution; it is narrative/conceptual, useful for the
  methodological report's required "clear logic linking metric to biology" (`CHALLENGE.md` §4.2)
  but not a ranking algorithm.
- **Anderson localization of vibrational modes** — disorder localizes normal modes in an elastic
  network to within a few wavelengths, "an example of Anderson localization" explicitly noted for
  globular proteins [VERIFIED-ABSTRACT]. Overlaps conventions §5 item 5 (eigenvector content / IPR
  on the _quantum Hamiltonian's_ eigenvectors, found weak at 63.6%/36.4%). Whether a _classical_
  ANM-mode participation-ratio / localization-length reading was tried under that name specifically
  is unclear from the retrieved record — flagged as likely-overlapping, not confidently new.
- **Phonon transport in disordered solids** — the propagon/diffuson/locon classification of
  vibrational modes by transport character (ballistic, diffusive, or trapped) in amorphous
  lattices, and the unified Peierls/Allen-Feldman transport theory bridging crystalline and glassy
  limits [VERIFIED-ABSTRACT, general materials-physics literature]. Classifying a protein's own
  ANM normal modes this way — which modes are "propagon-like" (signal-carrying end to end) versus
  localized — has not been retrieved as applied to protein allostery. It needs only the Hessian
  already required by C6.
- **Rigidity/generic percolation** — the critical bond-dilution fraction at which a giant rigid or
  connected cluster fragments (Jacobs & Thorpe). A _targeted_, source-anchored percolation
  (remove contacts adjacent to a candidate residue, measure the resulting loss of rigid/connected
  coupling to the active site) has not been retrieved as applied to protein allostery, though
  untargeted rigidity percolation on proteins is well studied.

---

## The five questions

**(a) Best mathematical fit to "rank residues by dynamic connectivity to a named source, from one
static structure."**

**Effective resistance to a named source** — $\Omega(\text{source}, i) = L^+_{ss} + L^+_{ii} -
2L^+_{si}$ on the (weighted) graph Laplacian $L$ of the contact network — is the strongest fit,
for four reasons. First, it is a ranking _by construction_: it is defined as a source-to-every-node
quantity, unlike centralities that need an ad hoc readout convention. Second, it has a genuine
dynamical interpretation, not just a static-geometric one: it equals (up to a graph-volume
normalization) the expected commute time of a random walk started at the source — "dynamic
connectivity" is its literal definition, not a metaphor bolted onto a distance measure. Third, it
needs nothing beyond the contact topology plus edge (spring) weights — one static structure, C6
verbatim, no trajectory, no learned weights. Fourth, and most importantly, it is not a foreign
transplant: $L^+$ (or the closely related Kirchhoff matrix inverse $\Gamma^{-1}$) is _already_ the
mathematical core of the Gaussian Network Model's cross-correlation matrix that the ENM-allostery
literature has used for two decades — Perturbation-Response Scanning (Atilgan & Atilgan)
perturbs a source residue and reads a response elsewhere using exactly this pseudo-inverse. Reading
it out as an explicit, named, source-anchored resistance distance rather than mining it out of a
full $N\times N$ covariance matrix has not been retrieved as a stated baseline anywhere in this
search. The honest caveat: whether a _quantum_ estimator of this quantity (e.g. via a quantum
linear-solver primitive, or a dissipative/non-unitary walk whose steady state encodes $L^+$) is
distinguishable from the already-refuted single-particle CTQW transfer amplitude is unresolved —
some quantum-walk literature ties CTQW hitting times to resistance distance directly, which would
collapse it back into item 1 of conventions §5. That question belongs to a later file, not this
one; what this file can settle is that the _classical_ framework is the best-fitting target for
whatever quantum observable is chosen next.

**(b) What does the allosteric-mechanical-metamaterials literature use, and does it transfer?**

Rocks et al. (2017) apply a strain between a source pair of nodes in a central-force spring network
and measure the resulting strain at a target pair elsewhere, under linear response; they then prune
~1% of bonds to make that source→target coupling large and specific, reporting success rates near
100% for designed responses. The retrieved abstract states the result in these behavioural terms
("produce a strain between any pair of target nodes... in response to an applied source strain")
without giving the exact response-matrix formula in the text this session — full text was
unreachable (PNAS returned HTTP 403) — so the precise equation is **[UNVERIFIED]** here, flagged
rather than guessed, per R3. What is verifiable is the _structure_ of the calculation: a linear
response (compliance) of a central-force network's Hessian to a point-pair perturbation. That
structure is mathematically the same calculation as Perturbation-Response Scanning already applied
to protein ANMs — so the transfer has, in effect, already happened, historically in parallel rather
than as an import from materials science into biology. What Rocks et al. add that protein-ENM
practice typically does not is the **inverse-design step**: rank _bonds_, not residues, by how much
removing them changes a chosen source-target coupling, then act on the highest-ranked ones. Applied
to our graph, that becomes a contact-sensitivity analysis — which spatial contacts, if perturbed,
most change the active site's coupling to a candidate distal residue — a natural, C1/C2-legal
addition to a PRS-style baseline that was not retrieved as already standard practice in the
allostery literature.

**(c) A controllability or observability metric never tried on protein allostery?**

Yes. **Target control** (Gao, Liu, D'Souza & Barabási, _Nat Commun_ 2014) computes the minimum
driver-node set required to control a _specified_ target subset rather than the whole network —
set the target to the active-site residue(s) and the output is exactly "which residues are
structurally necessary to actuate the active site," the formal inverse of a connectivity-to-source
ranking. Its single-node analogue, **control centrality** (Liu, Slotine & Barabási, _PLoS ONE_
2012), scores each residue by how many other nodes it alone could drive. Structural controllability
and its observability dual have been applied to protein networks before, but only at the
proteome/interactome scale (Vinayagam et al., _PNAS_ 2016) — whole proteins as nodes, not residues
within one structure. No result in this search applies target control, control centrality, or
network observability to a single protein's residue contact graph for allosteric-site prediction.

**(d) Which transferable methods are legal under C1/C2 as literally written?**

Legal, no MD anywhere, no MD-trained weights: Str2Str; the PDB-only AlphaFlow/ESMFlow checkpoint;
AlphaFold MSA-subsampling (del Alamo, AF-Cluster/SPEACH_AF); ENM/NMA-guided sampling (Zheng-style
mechanism); ScanNet/MaSIF/PeSTo; FTMap; Bogan-Thorn-style static alanine scanning; B-factor GNNs;
NMR order-parameter ML and DynaMine; EVcouplings/GREMLIN/DCA/SCA; ESM zero-shot DMS; ThermoMPNN;
GNM-analytic (not MD) transfer entropy; every item in §7 (controllability, observability, target
control, source localization, influence maximization, GSP, effective resistance, Katz/
communicability — all pure graph topology); Rocks-et-al-style linear response of the ENM Hessian;
rigidity theory/FIRST/CNA; topology-only phonon-mode classification; targeted percolation.
Illegal, MD-trained weights or MD-trajectory input as published: PocketMiner; CrypToth; SWISH and
mixed-solvent MD generally; BioEmu (unconditionally — MD is baked into every released checkpoint);
the MD-finetuned AlphaFlow/ESMFlow checkpoint; MD-trajectory transfer entropy, mutual-information
pathway analysis, current-flow betweenness _as published_ (MD-covariance-weighted), force
distribution analysis, and suboptimal-path/Markov propagation analysis as published. Ambiguous,
flagged rather than resolved: CryptoSite's dynamics-feature subset; RMSF-net's label source.

**(e) Has rigidity/constraint-counting been used for allosteric-site prediction, and what did it
get?**

Yes, twice over, both already inside the field rather than a fresh import — reported here to close
the question, not to claim it as new. First, a rigidity-perturbation approach: rigidify contacts
near a candidate site (simulating ligand binding with no energy function beyond constraint
counting) and look for large changes in a quantified stability–flexibility relationship elsewhere
in the structure as the signature of an allosteric site [VERIFIED-ABSTRACT, retrieved chapter
title "Ensemble Properties of Network Rigidity Reveal Allosteric Mechanisms"]. Second, Gohlke's
Constraint Network Analysis, built on FIRST's pebble game, reports that allosteric interactions
"may be mediated by modules of structurally stable residues with high betweenness in the global
interaction network" [VERIFIED-ABSTRACT]. Neither retrieved source reports a benchmark statistic
comparable to the four bars in conventions §6 (AUC, a stated positive/negative class, a stated
null) — the record for this method is qualitative (recovers known allosteric residues; correlates
with cooperativity), not a number this file can compare against `-distance` at AUC 0.617. **Write
"unknown" for the quantitative comparison** rather than inferring one.

---

## Transfer table

| Source field          | Method                                                               | Observable it computes                                                  | What it would compute on our graph                                        | C1/C2 verdict                            | Published transfer / would be new                                                                                                                   |
| --------------------- | -------------------------------------------------------------------- | ----------------------------------------------------------------------- | ------------------------------------------------------------------------- | ---------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| PPI hot spots         | ScanNet / MaSIF / PeSTo                                              | Per-residue interface probability                                       | Independent "PPI-hotspot-like" feature per node                           | Legal                                    | Published (interface ID); as an allostery feature, new                                                                                              |
| PPI hot spots         | Alanine-scanning ΔΔG (static)                                        | Per-residue energetic criticality                                       | Energetic prior orthogonal to topology                                    | Legal                                    | Published (hot spots); as allostery feature, new                                                                                                    |
| Cryptic pockets       | FTMap                                                                | Consensus probe-cluster druggability                                    | Orthogonal decoy/candidate pocket generator                               | Legal                                    | Published (druggability); combined with propagation ranking, new                                                                                    |
| Cryptic pockets       | PocketMiner / CrypToth / SWISH                                       | Cryptic-pocket probability / occupancy                                  | Same                                                                      | **Illegal** (MD-trained or MD-run)       | Published; unusable as-is                                                                                                                           |
| Ensembles w/o MD      | Str2Str                                                              | Sampled backbone conformers                                             | Fluctuation-aware edge weights from one apo structure                     | Legal                                    | Published (generator); as allostery graph input, new                                                                                                |
| Ensembles w/o MD      | AlphaFlow/ESMFlow (PDB-only)                                         | Sampled conformers                                                      | Same                                                                      | Legal (PDB checkpoint only)              | Published; PDB-only use for allostery, new                                                                                                          |
| Ensembles w/o MD      | AlphaFlow/ESMFlow (MD) / BioEmu                                      | Sampled conformers, near-experimental                                   | Same                                                                      | **Illegal** (MD-trained weights)         | Published; unusable as-is                                                                                                                           |
| Ensembles w/o MD      | AF2 MSA subsampling (del Alamo, AF-Cluster)                          | Alternate folded states                                                 | Multi-conformer graph / per-residue variability score                     | Legal (guard MSA build)                  | Published (structural biology); as allostery signal, new                                                                                            |
| Ensembles w/o MD      | ENM/NMA-guided sampling (Zheng mechanism)                            | Restructured conformers along soft modes                                | Same, zero MD                                                             | Legal                                    | Site-ranking wrapper = files 01/02; sampling mechanism alone, transferable                                                                          |
| Dynamics from statics | B-factor GNN / RMSF-net / DynaMine / NMR-S² RF                       | Per-residue flexibility scalar                                          | MD-free flexibility prior, cross-check feature                            | Legal (RMSF-net label source unverified) | Published; unused as allostery covariate                                                                                                            |
| Epistasis             | EVcouplings / GREMLIN / DCA                                          | Evolutionary coupling strength per pair                                 | Alternative edge-weight source; EC(source,i) baseline column              | Legal                                    | Published (contacts); as a direct allostery baseline, new                                                                                           |
| Epistasis             | DCA-on-allosteric-materials (Bravi et al.)                           | DCA accuracy vs. known mechanical ground truth                          | Warning: DCA misses long-range coupling in the one checked case           | Legal                                    | Published negative result — not a proposal                                                                                                          |
| Epistasis             | ESM zero-shot DMS                                                    | Per-residue mutational sensitivity                                      | Same                                                                      | Legal                                    | Published and **already tried here** — AUPR 0.06 on allosteric sites                                                                                |
| Epistasis             | ThermoMPNN                                                           | Per-mutation ΔΔG(folding)                                               | Load-bearing-for-stability score, distinct from signal-transmission score | Legal                                    | Published; unused as allostery covariate                                                                                                            |
| Info-flow             | GNM-analytic transfer entropy                                        | Directed information flow, closed-form                                  | Directed edge weights (non-reciprocal structure)                          | Legal                                    | Published (allostery, files 01/02); as a non-Hermitian Hamiltonian input, new                                                                       |
| Info-flow             | MD transfer entropy / MI pathways / FDA / current-flow (MD-weighted) | Directed flow / pathway residues                                        | N/A (needs trajectory)                                                    | **Illegal**                              | Published; unusable as-is                                                                                                                           |
| Network science       | Structural controllability / observability                           | Driver-node / sensor-node membership                                    | Topology-only importance score                                            | Legal                                    | Published at proteome scale only; at residue scale, new                                                                                             |
| Network science       | Target control                                                       | Min. driver set to control a target subset                              | Which residues are necessary to actuate the active site                   | Legal                                    | New — not retrieved on any protein network                                                                                                          |
| Network science       | Control centrality                                                   | # nodes a single node can drive                                         | Per-residue control power                                                 | Legal                                    | New                                                                                                                                                 |
| Network science       | Source localization (MLE)                                            | Most likely diffusion source                                            | Likelihood that a candidate residue explains active-site arrival pattern  | Legal                                    | New                                                                                                                                                 |
| Network science       | Influence maximization                                               | Submodular top-k seed set                                               | Non-redundant top-5 hit list (reframes the deliverable itself)            | Legal                                    | New                                                                                                                                                 |
| Network science       | Spectral graph wavelets                                              | Source-localized multi-scale wavelet coefficient                        | Active site as delta signal, swept over scales                            | Legal                                    | GSP tried on protein networks for other tasks; source-anchored ranking, new (caution: may collapse to tested diffusion family at heat-kernel limit) |
| Network science       | Effective resistance / current-flow closeness                        | Pseudo-inverse-Laplacian distance to source                             | $\Omega(\text{source}, i)$ read out directly                              | Legal                                    | Underlying math already latent in GNM; explicit named baseline, new                                                                                 |
| Network science       | Katz / communicability                                               | Attenuated all-walk count from source                                   | Source-row of $(I-\alpha A)^{-1}$ or $\exp(\beta A)$                      | Legal                                    | New, but converges to already-tested eigenvector centrality at large α                                                                              |
| Physical analogy      | Rocks et al. mechanical metamaterials                                | Source→target strain response, bond sensitivity                         | Same math as PRS; bond-sensitivity ranking is the new piece               | Legal                                    | Observable = convergent with PRS; inverse-design sensitivity analysis, new                                                                          |
| Physical analogy      | Rigidity theory / FIRST / CNA                                        | Rigid/flexible decomposition, flexibility-index shift on rigidification | Directly: rigidify near candidate, measure active-site flexibility shift  | Legal                                    | **Already published for allosteric-site prediction** — see STEP 3(e); no comparable AUC retrieved                                                   |
| Physical analogy      | Anderson-localization mode analysis                                  | Localization length / participation ratio                               | Which ANM modes are extended vs. localized between source and candidate   | Legal                                    | Overlaps tested quantum-IPR result; classical version, unclear if tried                                                                             |
| Physical analogy      | Phonon transport classification (propagon/diffuson/locon)            | Transport character of vibrational modes                                | Classify protein's own ANM modes this way                                 | Legal                                    | New                                                                                                                                                 |
| Physical analogy      | Targeted rigidity percolation                                        | Critical bond-dilution fraction                                         | Source-anchored connectivity-loss sensitivity                             | Legal                                    | New                                                                                                                                                 |

---

## What this changes for our pipeline

- **`network/` (contact graph construction, Phase 1.2/4):** the ENM/NMA-guided sampling mechanism
  (§3) and AF2 MSA-subsampling (§3) are both C1/C2-legal ways to replace a single binary contact
  map with a fluctuation-aware weighted graph, directly implementing the challenge's "structural
  fluctuations" alternative objective. This should be evaluated before committing to a single
  static contact map as the only input the quantum stage ever sees.
- **`classical/` (baseline suite, Phase 1.4):** add **effective resistance to the active site**
  and **target control / control centrality** as named classical baselines alongside `-distance`,
  `cavity_volume`, eigenvector centrality, and ESSA/APOP. All four are C1/C2-legal, cheap, and —
  per this search — not previously reported as tried on a protein residue network. Effective
  resistance in particular should be run _before_ any new quantum observable is designed, because
  §STEP-3(a) argues it is the best classical target for a quantum method to either reproduce
  cheaply or beat with new information.
- **`quantum/` (Hamiltonian and circuit design, Phase 2/3):** the GNM-analytic transfer-entropy
  route (§6) is a legal source of **directed** edge weights, which conventions §5 identifies as the
  one structural ingredient (non-reciprocal hopping) a plain contact graph cannot supply for a
  non-Hermitian quantum method. Worth testing as an input before concluding non-Hermitian methods
  are foreclosed by the graph alone. Separately, any CTQW-based estimator of effective resistance
  or Kirchhoff index must be checked against the already-closed single-particle-transfer-amplitude
  finding before being reported as a new quantum observable.
- **Deliverable framing (methodological report):** influence maximization (§7) reframes the
  required top-5 hit list itself, from five independently top-scoring residues to a
  jointly-non-redundant seed set. Worth deciding explicitly whether the hit list should be a
  top-k-by-score cut or a submodular-optimal set before the report is written.
- **Do not spend time on:** mixed-solvent MD, PocketMiner/CrypToth/BioEmu, or the MD-finetuned
  AlphaFlow/ESMFlow checkpoint — all explicitly C2-illegal in this search, however good their
  published numbers. Also do not re-benchmark protein-language-model mutational sensitivity as an
  allostery baseline; conventions §5 already closed it (AUPR 0.06).

---

## Method

Searches run via WebSearch (arXiv, Europe PMC, PubMed, and general web indices returning
Nature/Science/PLOS/PNAS/ACS/eLife/bioRxiv/arXiv records) and WebFetch, grouped by category:
PPI hot spots and cryptic pockets (8 queries); MD-free conformational ensembles (7 queries plus 1
WebFetch on the AlphaFlow abstract to resolve its PDB-only vs. MD-finetuned training split);
static-structure dynamics prediction (4 queries); mutation-effect/epistasis/coevolution (6
queries); communication-pathway/information-flow (6 queries); network science outside biology —
controllability, observability, source localization, influence maximization, graph signal
processing, effective resistance, communicability (8 queries, plus 3 follow-up queries narrowing
controllability/dominating-set/GSP specifically to protein networks); physical analogies —
mechanical metamaterials, rigidity/FIRST, tensegrity, Anderson localization, phonon transport (6
queries, plus 1 WebFetch attempt on the Rocks et al. PNAS full text, which returned HTTP 403 and
was not recovered by any other route this session); rigidity-for-allostery and quantum-walk/
resistance-distance verification (4 queries, plus 1 WebFetch on the CTQW-protein arXiv full text
to confirm identity with the already-known Mohtashim/Sajjan/Kais result in conventions §5); DOI/
venue verification for citations lacking a confirmed identifier (13 queries). Roughly 65 WebSearch
calls and 4 WebFetch calls total. Stopping rule: stop screening a category once the same
method/observable pair recurred across three independent queries with no new candidate surfacing,
and once every explicit sub-bullet in the task brief had at least one sourced citation with a
stated C1/C2 verdict.

**Not reached this session:** the exact response-matrix formula in Rocks et al. (2017) — PNAS
returned HTTP 403 and no arXiv full-text mirror with the equation was located; the paper's
behavioural claims are sourced from its abstract only, flagged `[UNVERIFIED]` where the formula
would have been quoted. Semantic Scholar is rate-limited (HTTP 429, noted in conventions §3) and
was not used. RMSF-net's and CryptoSite's exact training-label provenance (MD-derived or not) were
not resolved past the abstract level; both are flagged rather than assigned a confident C2 verdict.
