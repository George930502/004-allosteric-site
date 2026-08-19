# The field: what expertise looks like here

Rule 4 of this project's research principles (R4 in `AGENTS.md`, in full in
`docs/PRINCIPLES.md`) says to work like a
frontier researcher who is expert in this field. This file defines the field so that
instruction is executable rather than aspirational.

---

## 1. What field is this, exactly

This challenge sits at the intersection of three mature disciplines. It is not "AI for
biology"; it is a specific, older question being attacked with a new instrument.

**(a) Protein allostery / dynamic structural biology.** The study of how binding at one
site on a protein changes function at a distant site. The classical models are
Monod–Wyman–Changeux (concerted) and Koshland–Némethy–Filmer (sequential), both
conformational. The modern view is *ensemble* allostery: a protein is a thermodynamic
ensemble of conformations, and an effector reshapes the population rather than pushing
a lever — allostery can occur with **no** mean conformational change at all, purely
through changes in fluctuation entropy (Cooper & Dryden 1984; Hilser and Nussinov,
refs [3,4,6] in `CHALLENGE.md`). This matters directly for us: if allostery is carried
by fluctuations and correlations rather than by displacement, then a *propagation*
metric on the contact network is the right kind of observable, and a purely geometric
pocket-finder is the wrong kind.

**(b) Network biophysics / elastic network models.** The tradition that represents a
protein as a network of nodes (usually one per residue, at the Cα) connected by
harmonic springs within a cutoff. Tirion's 1996 result — that a single-parameter
potential reproduces the low-frequency modes of a full force field — is the license for
the whole approach, and is precisely the elastic network hypothesis the challenge tells
us to assume (C6). From it descend the Gaussian Network Model (GNM), the Anisotropic
Network Model (ANM), perturbation-response scanning, Markov/diffusive information
propagation on the residue network (ref [8]), and community/betweenness analyses of
allosteric pathways. **These are our classical baselines, and they are strong.** An
expert does not treat GNM as a strawman: it predicts B-factors well, it is cheap, and
for many proteins its slow modes already implicate functional sites.

**(c) Quantum simulation and quantum transport on graphs.** Continuous-time quantum
walks (Farhi & Gutmann 1998), single-excitation dynamics of XY/Heisenberg spin
networks, quantum state transfer in spin chains, and Hamiltonian simulation
(Trotterisation, LCU, qubitisation). The adjacent biological precedent is excitonic
energy transfer in light-harvesting complexes and the environment-assisted quantum
transport (ENAQT) literature — where the finding was that *neither* pure coherence
*nor* pure dissipation is optimal, but a specific interplay of the two. That result is
the most transferable idea in quantum biology and is directly relevant to our metric
design.

**Where the value chain sits (the applied field):** early-stage target identification
and validation in pharmaceutical R&D — upstream of docking, virtual screening and HTS.
The user of our output is a medicinal chemist deciding where on a surface to aim a
library. This is why interpretability is a stated objective, not decoration.

## 2. The specific open problem we are attacking

Given a single static, unbound structure, predict which surface residues form a pocket
whose occupancy will allosterically modulate the active site — **including cryptic
pockets that are not open in the input structure.**

State of the art, classically: pocket-geometry methods (fpocket, FTMap-family),
allostery-specific predictors (PARS, AlloPred, Ohm, STRESS/SPACER), ML cryptic-pocket
predictors trained on simulation data (e.g. PocketMiner), and the expensive gold
standard — long MD, mixed-solvent MD, or Markov state models to observe the pocket
open. Reported accuracies on blind apo-only prediction are modest; this is an unsolved
problem, not a solved one being re-solved. The challenge's framing (§2 of
`CHALLENGE.md`) is fair: months of MD, and approximations that are often too linear.

Our constraint set removes the MD route entirely (C2), which is the point: we must get
dynamics *ab initio* from topology.

## 3. What an expert in this field actually does

- **Treats the null model as the real opponent.** Any residue score correlates with
  burial, degree and closeness to the protein centre. Functional sites are usually
  well-connected. A method that "finds" allosteric sites without a degree-preserving
  or geometry-matched null has probably found "buried and central". Expert practice is
  to build the null before the method.
- **Distinguishes the three things that get conflated:** the *pocket* (a geometric
  cavity), the *allosteric site* (a pocket whose occupancy modulates function), and the
  *communication pathway* (residues that carry the signal between the two). Pathway
  residues are frequently buried and are not druggable; scoring them as hits is a
  category error the ground-truth definition must exclude.
- **Reports on the units chemists use.** Author residue numbering, chain IDs, pocket
  names from the literature — not zero-indexed matrix rows.
- **Knows that apo→holo is a moving target.** Cryptic pockets are, by definition,
  absent or occluded in the apo structure. Side chains move; loops reorder. Any method
  reading only apo geometry is predicting something the input does not show, which is
  why *dynamics* (even harmonic, topology-derived dynamics) is the right instrument.
- **Is honest about crystallographic artefacts:** crystal contacts, missing loops,
  alternate conformations, non-physiological constructs and bound ligands in
  "apo" files. Structures are experiments, not ground truth.
- **Quotes effect sizes with nulls, never bare rankings.** AUC/enrichment against both
  random background *and* decoy surface pockets, with a permutation test — exactly what
  `CHALLENGE.md` §4.1 asks for.

## 4. Known intellectual traps in this specific challenge

Recording these because they are the failure modes that produce a confident, wrong, or
hollow submission. Each is a claim to defend explicitly in the report.

1. **The classical-simulability trap.** A continuous-time quantum walk on an N≈200-node
   graph is `exp(-iHt)` on a 200×200 matrix — trivially computable classically. Our
   submission cannot claim advantage from *computing the walk*. The defensible claims
   are: (i) the walk is a **better metric** for this biology than diffusion, which is a
   physics argument tested empirically; (ii) hardware becomes relevant in regimes where
   the object genuinely is hard — many-excitation sectors, open-system/thermal
   dynamics, disorder or ensemble averaging, or full-atom node counts; (iii) a
   hardware-native implementation with a credible near-term resource budget (C3/C4).
   Say this out loud in the report. Judges in this field will know it; pretending
   otherwise costs more credibility than admitting it.
2. **The metaphor trap.** "Interference is like allosteric signalling" is an analogy,
   not a mechanism. Protein signal propagation at 310 K is a classical, strongly damped,
   thermally driven process; nobody credible claims residue-scale electronic coherence
   carries allostery. Our defensible position: the quantum walk is used as a
   **mathematical propagator with different path-summation properties**, not as a claim
   about protein physics. That distinction is the difference between a serious entry
   and a poster.
3. **The coherence-in-biology overclaim.** The photosynthesis coherence literature was
   substantially revised — much of the observed long-lived signal was reassigned to
   vibrational rather than electronic coherence. Cite that history accurately if we
   invoke quantum biology at all.
4. **Ground-truth leakage.** Tuning a cutoff, a top-k, or a Hamiltonian variant until
   the known pocket appears is test-set fitting even with no holo import. Constraint C1
   in `AGENTS.md` and the audit playbook exist for this.
5. **N = 3 targets.** The scored validation set is three proteins. Almost nothing is
   statistically significant *across targets* at that N; significance lives *within* a
   target (residues vs. null) and the cross-target claim is qualitative. Do not report a
   cross-target p-value as if it were powered.

## 5. Reading list

Entries marked **[C]** are cited in `CHALLENGE.md` §10 with DOIs — use those DOIs.
Unmarked entries are from domain knowledge: **verify the citation before it appears in
the report** (project rule 3).

*Allostery, concepts*
- **[C]** Nussinov & Tsai 2013, *Cell* — allostery in disease and drug discovery [3]
- **[C]** Motlagh, Wrabl, Li & Hilser 2014, *Nature* — the ensemble nature of allostery [4]
- **[C]** Tsai & Nussinov 2014, *PLoS Comput Biol* — a unified view of how allostery works [6]
- **[C]** Gunasekaran, Ma & Nussinov 2004, *Proteins* — is allostery intrinsic to all dynamic proteins? [9]
- Cooper & Dryden 1984, *Eur Biophys J* — allostery without conformational change
- Monod, Wyman & Changeux 1965; Koshland, Némethy & Filmer 1966 — the classical models

*Elastic networks and classical propagation (our baselines)*
- **[C]** Chennubhotla & Bahar 2007, *PLoS Comput Biol* — signal propagation and equilibrium fluctuations [8]
- **[C]** Erman 2006, *Biophys J* — GNM and residue fluctuations [16]
- **[C]** Das, Gur, Cheng, Jo, Bahar & Roux 2014, *PLoS Comput Biol* — two-state ANM [15]
- **[C]** Zheng 2023, *J Chem Phys* — allosteric site prediction from coarse-grained normal modes [1]
- Tirion 1996, *PRL* — single-parameter elastic potential (the licence for ENM)
- Bahar, Atilgan & Erman 1997 (GNM); Atilgan et al. 2001 (ANM)
- Atilgan & Atilgan 2009 — perturbation response scanning
- Sethi, Eargle, Black & Luthey-Schulten 2009, *PNAS* — dynamical network analysis

*Cryptic pockets and allosteric-site prediction*
- **[C]** Koseki et al. 2025, *JCIM* — CrypToth, mixed-solvent MD + topological data analysis [2]
- **[C]** Lu, Li & Zhang 2014, *Med Res Rev* — harnessing allostery for drug discovery [14]
- **[C]** Shen et al. 2016, *NAR* — Allosteric Database ASD v3.0 [25]
- Cimermancic et al. 2016, *JMB* — CryptoSite; Meller et al. 2023 — PocketMiner
- Panjkovich & Daura 2014 — PARS; Greener & Sternberg 2015 — AlloPred; Wang et al. 2020 — Ohm

*Quantum side*
- **[C]** Oh, Krogmeier, Schlimgen & Head-Marsden 2024, *ACS Phys Chem Au* — SVD quantum algorithm for quantum biology [11]
- **[C]** Mitarai & Fujii 2021, *Quantum* — simulating non-local channels with local ones [10]
- **[C]** Javadi-Abhari et al. 2024 — Qiskit [17]
- Farhi & Gutmann 1998 — continuous-time quantum walks; Childs 2009 — universality
- Bose 2003; Christandl et al. 2004 — state transfer in spin chains
- Plenio & Huelga 2008; Rebentrost et al. 2009; Mohseni et al. 2008 — ENAQT
- Cao et al. 2020, *Sci Adv* — quantum biology revisited (the corrective on coherence claims)
- Lloyd 1996 (Trotter); Low & Chuang 2017 (qubitisation) — simulation cost

*Targets*
- **[C]** Ostrem et al. 2013 [18] and Canon et al. 2019 [19] — KRAS G12C switch-II pocket, AMG 510
- **[C]** Wylie et al. 2017 [20] and Schoepfer et al. 2018 [21] — asciminib, myristoyl pocket
- **[C]** Green et al. 2016 [22] and Anderson et al. 2018 [23] — mavacamten, super-relaxed state
- **[C]** Dang, Reddy, Shokat & Soucek 2017 [24] — drugging undruggable targets (c-Myc)
