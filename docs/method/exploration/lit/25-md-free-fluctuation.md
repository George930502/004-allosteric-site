# Predicting structural fluctuations from one static structure, without MD

**Scope:** the challenge's _other_ deliverable route — "identifies potential allosteric sites based on
**structural fluctuations**" (`CHALLENGE.md` §2) — covering what can be computed about a protein's
fluctuation from a single apo structure with no molecular-dynamics trajectory and no MD-trained
weights (C2). Covers elastic-network fluctuation prediction and its validation against experiment,
ENM-based transition and hinge prediction, deep-learning ensemble generators and their training
provenance, fluctuation-ranked site identification, and deposited experimental fluctuation data.
Deliberately excludes: quantum observables (files `review/03`, `review/04`), signal-propagation
physics (`review/06`), coarse-graining (`review/07`), and the graph-theoretic ranking family
(effective resistance, controllability — `review/05` §7).
**Sibling files:** `docs/method/review/05-adjacent-task-transfer.md` §3 opened this territory with
five sources at abstract level; this file goes past it and contradicts it in two places (Boltz-class
models, and the C1 status of AlphaFold). `review/01-classical-baselines.md` holds ESSA/APOP as
baselines; this file re-reads them as _fluctuation_ methods. `review/02-ai-methods.md` holds the
supervision ceiling. `review/00-conventions.md` is the contract this file obeys.
**Retrieved:** 2026-08-26.

---

## 0. Read the clause before spending on it

The "structural fluctuations" wording appears once, in the executive-summary deliverable sentence
(`CHALLENGE.md` §2): _"a quantum algorithm approach that takes a protein structure as input and
identifies potential allosteric sites based on structural fluctuations or via dynamic connectivity
to an active site."_ It reads like a fork. It is not one, because two later sections close it.

- §4.1, the primary objective: _"The circuit **must** output a ranking of residues based on their
  **dynamic connectivity** — in most cases, connectivity **to an active site**."_
- §5, required outputs: _"an **N × N matrix** where entry (i, j) represents the calculated quantum
  connectivity strength between residue i and residue j."_

A per-residue fluctuation scalar is neither of those. It is a length-N vector, not an N × N matrix,
and it is not conditioned on the active site. **The fluctuation route cannot be the submitted
ranking.** [VERIFIED-FULLTEXT, `CHALLENGE.md` §2, §4.1, §5.]

That leaves three legal uses, and they are the only ones this file evaluates as candidates:

1. **Fluctuation as graph input** — turn the binary contact map into a fluctuation-weighted or
   multi-conformer graph before the propagation stage runs on it.
2. **Fluctuation as a baseline** — a classical arm scored through `allo.scoring.score_arm` beside
   `−distance`, `cavity_volume` and eigenvector centrality (`review/00-conventions.md` §6).
3. **Fluctuation as a covariate** — a control column proving the propagation ranking is not
   rediscovering "flexible residues are near the active site."

Everything below is judged against those three, not against "can it find allosteric sites alone."

---

## 1. Elastic network models as fluctuation predictors

### 1.1 What they compute, and why they are C6-native

The Gaussian Network Model gives a per-residue mean-square fluctuation as the diagonal of the
pseudo-inverse Kirchhoff matrix, `MSF_i ∝ (Γ⁺)_ii`; the Anisotropic Network Model gives the same
from the 3N × 3N Hessian and additionally gives directions. Both need only a contact cut-off and
Cα coordinates. Both are **C1-clean** (apo coordinates only), **C2-clean** (no trajectory, no
learned weight), and **C6-native** — the elastic network hypothesis is literally their statement.
`CHALLENGE.md` cites Erman's GNM paper (ref 16, doi:10.1529/biophysj.106.090803) and Das et al.'s
two-state ANM (ref 15) as the assumed model class, so an ENM fluctuation column is inside the spec
rather than an import into it.

### 1.2 What the B-factor correlation actually is

The field's standard validation is Pearson correlation between predicted MSF and crystallographic
B-factors. The honest numbers:

| Study                                                                      | Set                                                | Reported correlation                                                                                                                                                                            |
| -------------------------------------------------------------------------- | -------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Kondrashov, Cui & Phillips 2006, doi:10.1529/biophysj.106.085894           | 98 ultra-high-resolution (≤1.0 Å) X-ray structures | GNM **0.64**; separating covalent from non-covalent interactions **0.74**; adding ligands and cofactors **0.75**; further chemical subdivision "no significant improvement" [VERIFIED-ABSTRACT] |
| Song & Jernigan 2007 (vGNM), doi:10.1016/j.jmb.2007.03.059                 | "a large protein set"                              | GNM **0.59**, vGNM **0.81** once rigid-body motion and crystal packing are allowed to vary [VERIFIED-ABSTRACT]                                                                                  |
| Kundu, Melton, Sorensen & Phillips 2002, doi:10.1016/S0006-3495(02)75203-X | 113 proteins                                       | GNM beat crystallographic TLS rigid-body libration; adding crystal-neighbour effects improved it further [VERIFIED-ABSTRACT]                                                                    |

So the defensible figure for plain GNM against B-factors is **r ≈ 0.59–0.64 on hundreds of
proteins**, and it does not move much with chemical detail. Kondrashov's own abstract calls 0.64
"consistent with a previous large-scale study" [VERIFIED-ABSTRACT].

Directionality is worse than magnitude. Kondrashov et al. 2007 (doi:10.1016/j.str.2006.12.006)
tested five potentials against anisotropic displacement parameters on 83 ultra-high-resolution
structures: "while all five potentials provide good predictions of the **magnitude** of flexibility,
all-atom potentials have a clear edge at prediction of **directionality**" [VERIFIED-ABSTRACT]. An
ENM gets the size of the wiggle roughly right and the direction of the wiggle less so.

### 1.3 Three failure modes, each independently sourced

**(a) B-factors are mostly rigid-body motion, not internal dynamics.** Song & Jernigan found rigid
body motions account for approximately 60 % of total fluctuations [VERIFIED-ABSTRACT]. Lezon 2012
(doi:10.1002/prot.24014) goes further: "X-ray B factors carry the signature of rigid-body motions,
to the extent that **B factors can be almost entirely accounted for by rigid motions alone**," and
when fitting to refined anisotropic temperature factors instead, "the contributions of rigid motions
are significantly reduced, indicating that the large contribution of rigid motions to B factors is
a result of **over-fitting**" [VERIFIED-ABSTRACT].

**(b) The crystal lattice is in the number.** Hinsen 2008 (doi:10.1093/bioinformatics/btm625) built
an ENM of the whole crystal and found "crystal packing modifies the atomic fluctuations
considerably" and that "thermal fluctuations are not the dominant contribution to crystallographic
Debye–Waller factors" [VERIFIED-ABSTRACT]. Riccardi, Cui & Phillips 2009
(doi:10.1016/j.bpj.2008.10.010): "treating the crystal environment leads to better agreement with
experimental anisotropic displacement parameters" [VERIFIED-ABSTRACT]. Zimmermann et al. 2011
(doi:10.4172/1745-7580.1000047) state the consequence for us directly: "effects of the protein
environment on crystallographic temperature factors may be **misleading for evaluating specific
functional motions**" [VERIFIED-ABSTRACT].

**(c) Optimising against B-factors makes the collective motions worse.** This is the sharpest
result in the section. Fuglebakk, Reuter & Hinsen 2013 (doi:10.1021/ct400399x) quantified how well
ENMs reproduce the covariance structure of MD, found "large and consistent differences between
proposed models," and **cautioned against benchmarking models using crystallographic B-factors,
because the models performing best against B-factors showed weaker collective-motion predictions**
[VERIFIED-ABSTRACT]. Every "we beat GNM on B-factors by 20–32 %" paper below is therefore
optimising a target that this study says is the wrong one for our purpose.

**(d), for completeness — the units are not what people assume.** Kuzmanic & Zagrovic 2010
(doi:10.1016/j.bpj.2009.11.011) derive the relation between mean B-factor, RMSF and ensemble-average
pairwise RMSD, and conclude "the ensemble-average pairwise backbone RMSD for a microscopic ensemble
underlying a typical protein x-ray structure is **approximately 1.1 Å**" [VERIFIED-ABSTRACT]. The
microscopic ensemble behind one crystal structure is narrow. Whatever opens a cryptic pocket is not
generically inside it.

### 1.4 "Essential dynamics from a single structure" — the claim and the critics

The claim, stated at its strongest by the Bahar group: "the intrinsic dynamics of allosteric
proteins defined by their 3-dimensional architecture ... favors cooperative motions that bear close
similarity to the structural changes they undergo during their allosteric actions. These
conformational motions are usually driven by energetically favorable or soft modes"
(Zhang et al. 2020, doi:10.1016/j.sbi.2019.11.002) [VERIFIED-ABSTRACT]. Reviewed at length in
Bahar, Lezon, Yang & Eyal 2010, doi:10.1146/annurev.biophys.093008.131258 [VERIFIED-ABSTRACT].

The critics, in order of severity:

- **Petrone & Pande 2006** (doi:10.1529/biophysj.105.070045) projected observed conformational
  changes onto normal-mode subspaces: "the first **20 modes only contribute 50 % or less** of the
  total conformational change in four test cases (myosin, calmodulin, NtrC, and hemoglobin)"
  [VERIFIED-ABSTRACT]. Two of those four are on our own target list's mechanism classes.
- **Yang, Song & Jernigan 2007** (doi:10.1529/biophysj.106.095927) on 170 open/closed pairs found
  applicability splits into three categories and depends on how **collective** the transition is,
  not on protein size [VERIFIED-ABSTRACT]. Where the transition is local, the modes miss it.
- **Tama & Sanejouand 2001** (doi:10.1093/protein/14.1.1), the founding positive result, is
  explicitly conditional: on 20 open/closed proteins, a single low-frequency mode matches the
  transition **for highly collective motions** [VERIFIED-ABSTRACT].
- **Fuglebakk, Reuter & Hinsen 2013** (above) — the validation target itself is misleading.

Net reading: the ENM soft modes are a real, cheap, C2-legal description of _global, collective_
motion. They are not a description of the local side-chain and short-loop rearrangement that
Beglov et al. (§5.2) identify as the commonest way a cryptic pocket is occluded.

### 1.5 The post-GNM fluctuation predictors (all optimise the compromised target)

Reported as improvements over GNM on B-factor correlation, and all C1/C2-clean since they train on
nothing or on experimental B-factors: flexibility-rigidity index, "about **20 %** more accurate than
GNM in B-factor prediction" (doi:10.1063/1.4922045) [VERIFIED-ABSTRACT]; multiscale weighted
colored graphs, "more than **11 %** improvement" (doi:10.1063/1.4936132) [VERIFIED-ABSTRACT];
persistent sheaf Laplacians, "an increase in accuracy of **32 %** compared to the classical Gaussian
network model" (doi:10.1021/acs.jpcb.5c01287) [VERIFIED-ABSTRACT]; multiscale differential geometry
learning, "**27 %**" (doi:10.1002/jcc.70073) [VERIFIED-ABSTRACT]; an extended GNM with local,
allosteric and structural terms "reducing RMSDs between predicted and experimental B-factors by
**26 %–46 %** across nine representative proteins" (doi:10.1088/1478-3975/ae1dc1)
[VERIFIED-ABSTRACT]. None of these reports a site-prediction number. Per §1.3(c), a gain here is
not evidence of a gain on collective motion, which is what a propagation method uses.

Also in this family and worth naming because it wins on the one comparison that used both data
types: **NOLB**, non-linear rigid-block NMA (Hoffmann & Grudinin 2017, doi:10.1021/acs.jctc.7b00197)
[VERIFIED-ABSTRACT], which Dziadek et al. 2024 (doi:10.1021/acs.jctc.4c00754) found gave "the best
agreement between the predicted and experimental fluctuation profiles" for X-ray structures on a
100-protein set, while for NMR-derived profiles the ranking inverted to
CABS-flex > UNRES-DSSP-flex > UNRES-flex > NOLB [VERIFIED-ABSTRACT]. Two experimental references
disagree about which predictor is best. That is itself a finding: the "ground truth" for fluctuation
is not one quantity.

---

## 2. ENM-based transition and hinge prediction

### 2.1 Overlap and two-state models

**ANMPathway / two-state ANM** (Das, Gur, Cheng, Jo, Bahar & Roux 2014,
doi:10.1371/journal.pcbi.1003521, `CHALLENGE.md` ref 15) builds a two-state potential by combining
two ENMs "representative of the experimental structures resolved for the endpoints," finds the
minimum-energy structure on the cusp hypersurface, and descends to both sides. Validated on adenylate
kinase, SERCA, LeuT and a glutamate transporter, "in good agreement with those from other similar
methods and with data obtained from all-atom molecular dynamics simulations" [VERIFIED-ABSTRACT].

**This is C1-illegal for us as written.** It takes _two_ endpoints. Our second endpoint is the holo
structure. Using it anywhere in the prediction path is exactly the leak C1 forbids. The challenge
citing it as ref 15 does not change that — it is cited as an instance of the elastic network
hypothesis, not as a licence to read the holo endpoint. **The single-state half (one ENM, soft-mode
sampling) is legal; the two-state cusp construction is not.** [UNVERIFIED — this is our reading of
C1 applied to a method the challenge cites, not a statement from the paper.]

### 2.2 Hinge detection from one structure

- **HingeProt** (Emekli, Schneidman-Duhovny, Wolfson, Nussinov & Haliloglu 2008,
  doi:10.1002/prot.21613): "Given a **single** protein structure, the method automatically divides
  it into the rigid parts and the hinge regions connecting them ... employs the Elastic Network
  Model ... validated against a large data set of proteins" [VERIFIED-ABSTRACT]. No accuracy figure
  in the abstract; the dataset size is not stated. **C1/C2/C6 all clean** (single apo structure, ENM,
  no trajectory).
- **PACKMAN** (Khade, Kumar & Jernigan 2020, doi:10.1016/j.jmb.2019.11.018): hinges from **alpha-shape
  packing geometry**, not from modes. "This characterization is sufficient to enable reliable hinge
  predictions from a single static structure, and notably, this can be from **either the open or the
  closed form**" ... "predicted hinges are validated by using permutation tests on B-factors" ...
  "A group of **167 protein pairs** with open and closed structures has been investigated"
  [VERIFIED-ABSTRACT]. No AUC or top-k number in the abstract. **C1/C2 clean; C6-orthogonal** — it
  uses packing geometry rather than the elastic network, so it is a second, independent structural
  route to the same object.

The "predicts equally well from open or closed" property is the one worth noting: it is the closest
published analogue to our own apo-versus-holo robustness requirement, which CAPASP found APOP and
PASSer fail (doi:10.1007/s10822-026-00831-4, via `review/00-conventions.md` §6).

### 2.3 Zheng's normal-mode-guided sampling — `CHALLENGE.md` reference 1, retrieved in full

Two papers, and the earlier one carries the benchmark the challenge's cited paper does not.

**Zheng 2021, _Proteins_ 89:416–426, doi:10.1002/prot.26027** [VERIFIED-ABSTRACT, complete abstract
retrieved]: "a fast and simple conformational sampling scheme guided by normal modes solved from the
coarse-grained elastic models followed by atomistic backbone refinement and side-chain repacking ...
simply sampling along each of the **lowest 30 modes** is near optimal for adequately restructuring
cryptic sites so they can be detected by existing pocket finding programs like **fpocket and
concavity**." Benchmark: "a **training set of 84 known cryptic sites and a test set of 14
proteins**," achieving "**area under the receiver operating characteristic curve > 0.8**"
— "comparable to the CryptoSite server." Cost: "**1–2 hours for an average-size protein**." Machine
learning was tried on top and "only slightly improved the performance."

**Zheng 2023, _J Chem Phys_ 158:124127, doi:10.1063/5.0141630** (`CHALLENGE.md` ref 1)
[VERIFIED-FULLTEXT via PMC10066797]: the same sampler applied to four allosteric systems — GluR2,
GroEL, a GPCR, and myosin. Protocol details from full text: sampling along the lowest 30 modes at
"**five discrete root mean square deviation (RMSD) values: 1, 2, 3, 4, and 5 Å**"; "every residue is
assigned a pocket score by fpocket and concavity. Each pocket score is then **averaged over the
conformational ensemble**"; "the performance of both fpocket and concavity scores **peaks near 30
modes**, although concavity seems to perform slightly better." Runtime "**1–2 h for an average-size
protein of ∼400 residues**." Atomistic rebuild via PULCHRA. **No MD anywhere in the pipeline.**
Critically: **the 2023 paper reports no benchmark statistic** — four case studies, assessed
qualitatively. The number the challenge's own reference stands on is the 2021 AUC > 0.8 on 14 test
proteins.

**Verdict: C1 clean, C2 clean, C6 native.** This is the single most defensible MD-free ensemble
generator available to us, it is the challenge's own citation, and its mechanism — perturb along
low-k ENM modes, rebuild, average a per-residue score over the ensemble — needs nothing we do not
already have except a backbone-rebuild step. `review/05` §3 reached the same conclusion from the
abstract; the full text confirms it and adds the exact amplitudes.

**Caution, and it is not small.** Zheng's readout is a **pocket score averaged over the ensemble**,
i.e. a geometric cavity detector run many times. Our `cavity_volume` baseline is a zero-parameter
instance of that same detector run once (`review/00-conventions.md` §6 item 2). Zheng's method is
therefore closer to "cavity_volume, ensemble-averaged" than to a fluctuation ranker, and the honest
comparison is against `cavity_volume`, not against `−distance`. [UNVERIFIED — our inference from
the two method descriptions; no head-to-head exists.]

---

## 3. Deep-learning ensembles that do not train on MD

### 3.1 What each was trained on, and what it recovered

| Method                                                                                                          | Input                           | Trained on                                                            | Published recovery                                                                                                                                                                                                                                                                                                                                    | Criterion / set                                                                                                                                                                                                                                                                                                                                                                                                      |
| --------------------------------------------------------------------------------------------------------------- | ------------------------------- | --------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| AF2 + MSA subsampling (del Alamo, Sala, Mchaourab & Meiler 2022, doi:10.7554/eLife.75751)                       | sequence + MSA                  | AF2 weights = PDB structures                                          | models spanning the range between two experimental structures; "models at the extremes of these conformational distributions observed to be among the most accurate (**average template modeling score of 0.94**)" [VERIFIED-ABSTRACT]                                                                                                                | transporters + GPCRs "absent from the AF2 training set"; TM-score against the two known endpoints                                                                                                                                                                                                                                                                                                                    |
| AF2 + MSA subsampling for cryptic pockets (Meller, Bhakat, Solieva & Bowman 2023, doi:10.1021/acs.jctc.2c01189) | sequence + MSA                  | AF2 weights = PDB                                                     | "**In 6 out of 10 cases AlphaFold samples the open state**" [VERIFIED-FULLTEXT]                                                                                                                                                                                                                                                                       | 10 known cryptic pockets, 5 pre- and 5 post-training-cutoff; criterion RMSD < **1.2 Å** to the ligand-bound structure over the cryptic-site region. Protocol: `max_msa_clusters` 32, `max_extra_msa` 64, dropout on, **32 or 160** structures per target. Failures: TEM β-lactamase not recovered; plasmepsin II only partially — and "32 μs of MD simulations do not reveal cryptic pocket opening in PM II" either |
| CFold / AF2 architecture, restricted training set (Schafer & Porter 2025, doi:10.1002/pro.70105)                | sequence                        | a deliberately **limited** subset of PDB                              | "Despite sampling **1300–4300 structures/protein** with various sequence sampling techniques, CFold predicted **only one alternative structure outside of its training set** accurately and with high confidence while also generating experimentally inconsistent structures with higher confidence" [VERIFIED-ABSTRACT]                             | 8 fold switchers from 6 families                                                                                                                                                                                                                                                                                                                                                                                     |
| AF3 for cryptic pockets (Lazou, Tuchscherer, Vajda & Joseph-McCarthy 2026, doi:10.1038/s42003-026-10596-z)      | sequence (+ optional ligand)    | AF3 weights = PDB                                                     | "AF3 is generally able to reproduce the scale of conformational change required for cryptic site formation. **When given a cryptic-site ligand**, AF3 predominantly predicts conformations competent to bind the ligand in the cryptic site; **without the ligand, conformations lacking the cryptic pocket generally dominate**" [VERIFIED-ABSTRACT] | case studies; no aggregate rate in the abstract                                                                                                                                                                                                                                                                                                                                                                      |
| ConforFold / ConforPSSP (Syrlybaeva & Strauch 2026, doi:10.1002/pro.70564)                                      | sequence                        | retrained OpenFold + a transformer over secondary-structure fragments | "correctly identified **both conformers in 84 % of cases at TM-scores ≥ 0.8**, outperforming AlphaFlow (**75.4 %**) ... It outperformed BioEmu ... in cases where secondary structures between conformers differ significantly (**83 % and 76 %**)" [VERIFIED-ABSTRACT]                                                                               | test set of proteins with two alternative conformations; size not stated in the abstract                                                                                                                                                                                                                                                                                                                             |
| AF2 + frustration analysis (Guan, Tang, Ren, Chen, Wang, Wolynes & Li 2024, doi:10.1073/pnas.2410662121)        | one static structure + sequence | AF2 = PDB; frustration = an energy function                           | "Starting from ground state static structures, this integrative method generates alternative structures as well as pathways of protein conformational motions"; "consistent with available experimental and molecular dynamics simulation data" [VERIFIED-ABSTRACT]                                                                                   | no aggregate rate retrieved                                                                                                                                                                                                                                                                                                                                                                                          |
| AF2 randomised sequence scanning + frustration on ABL1 (Raisinghani et al. 2024, doi:10.1021/acs.jctc.4c00222)  | sequence                        | AF2 = PDB                                                             | "detection of hidden allosteric states in the ABL1 protein kinase" [VERIFIED-ABSTRACT]                                                                                                                                                                                                                                                                | single-target case study — but the target is our BCR-ABL1 kinase domain                                                                                                                                                                                                                                                                                                                                              |
| AlphaConformers (Daniel, Vitoriano De Queiroz Lira & Zea 2026, doi:10.64898/2026.08.18.745512, bioRxiv)         | sequence + structural guidance  | AF2 = PDB                                                             | "expanded AlphaFold2 conformational sampling" on "a curated benchmark of **88 proteins** with known ligand-bound and unbound conformations" [VERIFIED-ABSTRACT]                                                                                                                                                                                       | no single headline rate retrieved                                                                                                                                                                                                                                                                                                                                                                                    |

### 3.2 The C2 verdict is easy. The C1 verdict is the problem.

AF2, AF3, OpenFold and Boltz-1 train on PDB structures, not trajectories. On the letter of C2 —
"no classical MD trajectories as inputs ... no MD-trained weights in the prediction path" — they
pass.

They do not obviously pass **C1**, for two separate reasons, and `review/05` §3 did not raise either.

**(a) Template retrieval.** AF2/AF3 template search hits the PDB. Left on, it can retrieve the
target's own holo entry — the exact structure our benchmark scores against. This is a direct,
mechanical C1 breach. It is switchable off, so it is a build-time guard, not a disqualification.
[UNVERIFIED — mechanism is documented behaviour of the pipelines; not re-retrieved from a paper this
session.]

**(b) Training-set memorisation, which is not switchable off.** Schafer & Porter's whole result is
that AF2's success on alternative conformations "stems largely from its training data"
[VERIFIED-ABSTRACT]. Meller et al. explicitly split their benchmark on this axis: "the bottom five
examples had their **holo** crystal structures deposited **after** AlphaFold was trained"
[VERIFIED-FULLTEXT], with the cutoff given in the full text as April 2018. Lazou et al. hedge the
same way for AF3: "the results may reflect a bias toward memorized structural priors, the level of
detrimental memorization appears to be limited" [VERIFIED-ABSTRACT].

The operational consequence for us: **for every apo/holo pair we are scored on, check the holo
entry's PDB deposition date against the checkpoint's training cutoff before any AF-family model
enters the prediction path.** Where the holo entry predates the cutoff, the model has seen the
answer, and a recovered pocket is a memory, not a prediction. Newer checkpoints are strictly worse
here: AF2's cutoff is April 2018 [VERIFIED-FULLTEXT via Meller full text]; AF3 is reported to train
on PDB entries released before 30 September 2021 [UNVERIFIED — from the recorded web search summary
of the AF3 weights terms, not confirmed against the AF3 paper this session]. Boltz-2 "adds every
protein-, RNA- and DNA-ligand complex deposited through **early 2025**" [UNVERIFIED — same search
summary]. Our holo validation structures are named publicly in `CHALLENGE.md` §6 Table 1; the check
is a lookup, and it is cheap.

**(c) AF3 needs the ligand to work, which is a third C1 breach.** Lazou et al.'s central finding is
that AF3 predicts the cryptic-competent conformation _when given the cryptic-site ligand_ and mostly
does not without it [VERIFIED-ABSTRACT]. The ligand is holo information. The unconditioned mode —
the only C1-legal one — is the mode they report as mostly failing.

### 3.3 What this costs us

Sizes in scope: 147–1058 residues, 4 mandatory targets, up to 13 with the secondary set.

AF2 inference attention cost grows with sequence length; a 1058-residue chain is roughly 50× the
pair-representation area of a 147-residue chain. Meller's protocol is 160 predictions per target.
160 × 13 = 2080 inferences, of which the large targets dominate. On one A100 that is plausibly
1–3 GPU-days plus MSA construction, which for 13 sequences against a clustered database is hours
[UNVERIFIED — our arithmetic from the published prediction counts and standard AF2 scaling; no
runtime figure was retrieved]. This is affordable but it is not cheap, and every hour of it buys a
result whose C1 status has to be argued rather than asserted.

---

## 4. Generative ensemble models: strict C2 verdicts

The rule from `review/00-conventions.md` §4: MD in the training chain puts MD-trained weights in the
prediction path, and inference without new MD does not cure it.

| Model                                                                                                                                                          | Trained on                                                                                                                                                                                                                                                                                                                                                                                                                                                      | C2 verdict                                                                                                                            | Evidence                                                           |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| **Str2Str** (Lu, Zhong, Zhang & Tang, arXiv:2306.03117)                                                                                                        | "an amortized denoising score matching objective **trained on general crystal structures**" with "**no reliance on simulation data during both training and inference**"                                                                                                                                                                                                                                                                                        | **LEGAL. Cleanest verdict in this file.**                                                                                             | [VERIFIED-ABSTRACT]                                                |
| **AlphaFlow / ESMFlow, PDB checkpoint** (Jing, Berger & Jaakkola, arXiv:2402.04845)                                                                            | "When trained and evaluated on the PDB, our method provides a superior combination of precision and diversity compared to AlphaFold with MSA subsampling"                                                                                                                                                                                                                                                                                                       | **LEGAL, checkpoint-conditional.** The loaded checkpoint must be named and verified.                                                  | [VERIFIED-ABSTRACT]                                                |
| **AlphaFlow / ESMFlow, MD checkpoint** (same paper)                                                                                                            | "When further trained on **ensembles from all-atom MD**..."                                                                                                                                                                                                                                                                                                                                                                                                     | **ILLEGAL.** And it is the default in most tutorials.                                                                                 | [VERIFIED-ABSTRACT]                                                |
| **AlphaFlow-Lit** (Li et al., arXiv:2407.12053)                                                                                                                | distils/fine-tunes AlphaFlow's structure module; 47× sampling speed-up                                                                                                                                                                                                                                                                                                                                                                                          | **INHERITS the parent checkpoint's verdict.** Abstract does not state training data. Do not load without checking.                    | [VERIFIED-ABSTRACT]                                                |
| **Boltz-2** (doi:10.1101/2025.06.14.659707)                                                                                                                    | "we supervise Boltz-2 using ensembles coming from both experimental techniques, such as NMR, as well as computational ones, such as **molecular dynamics**" ... "we collected poses from the trajectories released as part of three large-scale open efforts: **MISATO, ATLAS, and mdCATH**" ... "we supervise the model's single representation ... to predict **B-factors coming from both experimental methods as well as molecular dynamics trajectories**" | **ILLEGAL, unconditional.** Every released checkpoint has MD in it.                                                                   | [VERIFIED-FULLTEXT via PMC12262699]                                |
| **Boltz-1**                                                                                                                                                    | PDB structures, single structure per system ("Unlike Boltz-1, which trained on a single structure per system")                                                                                                                                                                                                                                                                                                                                                  | **LEGAL** on the letter of C2 — but carries the same C1 memorisation problem as AF3 (§3.2).                                           | [VERIFIED-FULLTEXT, same source]                                   |
| **BioEmu** (doi:10.1126/science.adv9817)                                                                                                                       | ">200 ms of MD" baked into training                                                                                                                                                                                                                                                                                                                                                                                                                             | **ILLEGAL, unconditional.**                                                                                                           | [VERIFIED-ABSTRACT, carried from `review/05` §3; not re-retrieved] |
| **idpGAN** (Janson, Valdes-Garcia, Heo & Feig 2023, doi:10.1038/s41467-023-36443-x)                                                                            | "machine learning can be trained **with simulation data** ... train a generative adversarial network ... on **coarse-grained simulations** of intrinsically disordered peptides ... also retrain idpGAN on **atomistic simulation data**"                                                                                                                                                                                                                       | **ILLEGAL.** Its stated purpose is to amortise simulation.                                                                            | [VERIFIED-ABSTRACT]                                                |
| **ConforFold / ConforPSSP** (doi:10.1002/pro.70564)                                                                                                            | retrained OpenFold + secondary-structure transformer; abstract does **not** name the training corpus                                                                                                                                                                                                                                                                                                                                                            | **UNRESOLVED — flag, do not assume.** Its comparator set (AlphaFlow, Cfold, BioEmu) is mixed-legality.                                | [VERIFIED-ABSTRACT]                                                |
| **EPO** (Sun et al., arXiv:2511.10165)                                                                                                                         | online energy-preference refinement of a **pretrained ensemble generator**; "without requiring MD trajectories"                                                                                                                                                                                                                                                                                                                                                 | **INHERITS the base model's verdict.** The claim is about the refinement stage only.                                                  | [VERIFIED-ABSTRACT]                                                |
| **Structure-token "synonym swap"** (Liu, Feng, Cao & Li, arXiv:2511.10056)                                                                                     | exploits redundancy in PDB-trained structure tokenizers; "accurately recapitulates protein flexibility, performing competitively with state-of-the-art models"                                                                                                                                                                                                                                                                                                  | **LIKELY LEGAL** if the tokenizer is PDB-trained; the tokenizer identity must be checked.                                             | [VERIFIED-ABSTRACT]                                                |
| **DynamicMPNN** (Abrudan et al., arXiv:2507.21938)                                                                                                             | "**46,033 conformational pairs** covering 75 % of CATH superfamilies" from PDB                                                                                                                                                                                                                                                                                                                                                                                  | **LEGAL** for C2. Multi-state inverse folding, not ensemble generation — wrong output type for us.                                    | [VERIFIED-ABSTRACT]                                                |
| **ProTDyn** (arXiv:2510.00013), **PHASE** (arXiv:2608.23490), **ENSEMBITS** (arXiv:2605.13789), **LD-FPG** (arXiv:2506.17064), **GeoGraph** (arXiv:2510.00774) | MD trajectories, explicitly                                                                                                                                                                                                                                                                                                                                                                                                                                     | **ILLEGAL**, all five.                                                                                                                | [VERIFIED-ABSTRACT]                                                |
| **PEGASUS** (doi:10.1002/pro.70221)                                                                                                                            | sequence-based predictor of **MD-derived** flexibility                                                                                                                                                                                                                                                                                                                                                                                                          | **ILLEGAL** — the labels are simulation output.                                                                                       | [VERIFIED-ABSTRACT]                                                |
| **Pražnikar 2026 GDV flexibility predictor** (doi:10.1093/bioinformatics/btag175)                                                                              | "achieves a Spearman correlation of **0.828** compared to **MD data**"                                                                                                                                                                                                                                                                                                                                                                                          | **PROBABLY ILLEGAL** — MD is at least the evaluation target and appears to be the label source; not resolved past the abstract. Flag. | [VERIFIED-ABSTRACT]                                                |

The pattern is worth stating plainly: **the 2025–2026 generative frontier has moved toward MD
training, not away from it.** Of the models retrieved with a datable training corpus, the MD-free
ones (Str2Str, the PDB AlphaFlow checkpoint, structure-token swapping) are the older or the smaller
ones. C2 does not just cost us accuracy; it costs us the direction the field is travelling in.

---

## 5. Ranking residues and pockets by predicted fluctuation

### 5.1 The methods that already do exactly this

| Method                                                                                       | Input                             | What it ranks by                                                                                                                    | Published number                                                                                                                                                                                                                                                      | C1/C2/C6                                   |
| -------------------------------------------------------------------------------------------- | --------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------ |
| **Panjkovich & Daura 2012**, doi:10.1186/1471-2105-13-273                                    | one structure + a pocket detector | change in NMA-predicted flexibility when a pocket is occupied, plus structural conservation                                         | on **91 non-redundant allosteric proteins**: "significant changes in protein flexibility upon allosteric-ligand binding in **70 %** of the cases"; predictive approach reaches "**65 % positive predictive value**" at **0.22 sensitivity** under stricter parameters | clean / clean / native [VERIFIED-ABSTRACT] |
| **PARS** server, doi:10.1093/bioinformatics/btu002                                           | one structure                     | same, packaged                                                                                                                      | "queries protein dynamics and structural conservation to identify pockets ... that may exert a regulatory effect"; no new statistic in the abstract                                                                                                                   | clean / clean / native [VERIFIED-ABSTRACT] |
| **Binding leverage**, Mitternacht & Berezovsky 2011, doi:10.1371/journal.pcbi.1002148        | one crystal structure             | "the ability of a binding site to **couple to the intrinsic motions** of a protein," via Monte Carlo probe placement + normal modes | "both catalytic and allosteric sites have high binding leverage"; can "predict latent allosteric sites from single crystal structures"; no aggregate rate in the abstract                                                                                             | clean / clean / native [VERIFIED-ABSTRACT] |
| **SPACER** server, doi:10.1093/nar/gkt460                                                    | one structure                     | binding leverage + leverage coupling                                                                                                | interactive framework; no benchmark statistic in the abstract                                                                                                                                                                                                         | clean / clean / native [VERIFIED-ABSTRACT] |
| **ESSA**, Kaynak, Bahar & Doruker 2020, doi:10.1016/j.csbj.2020.06.020                       | one structure                     | shift in **soft-mode frequencies** when each residue's heavy atoms are added as extra network nodes                                 | "enrichment of allosteric and orthosteric binding sites, **as well as global hinge regions**, among essential residues"; combined with pocket + hydrophobicity gives "successful predictions of allosteric pockets for both ligand-bound and -unbound structures"     | clean / clean / native [VERIFIED-ABSTRACT] |
| **APOP**, Kumar, Kaynak, Dorman, Doruker & Jernigan 2023, doi:10.1093/bioinformatics/btad275 | one structure (incl. assemblies)  | shift in **global-mode frequencies** on stiffening the network across a pocket, plus mean local hydrophobicity                      | "Out of the **104** test cases, APOP predicts known allosteric pockets for **92** within the top 3"                                                                                                                                                                   | clean / clean / native [VERIFIED-ABSTRACT] |

Two cautions inherited from `review/00-conventions.md` §6 and not re-derived here: APOP's
apo-matched figure is 11/15 (73 %) against ESSA's 7/14 (50 %); AlloBench's leakage-controlled
retest puts APOP at **15 %** at Jaccard > 0.5 (doi:10.1021/acsomega.5c01263); and CAPASP finds APOP
degrades specifically on apo versus holo input (doi:10.1007/s10822-026-00831-4) — the exact axis we
are scored on. [Not re-retrieved this session; cited as recorded in conventions §6.]

**The important structural fact about this whole column:** ESSA, APOP, PARS and binding leverage all
rank by a **perturbation of the fluctuation spectrum**, not by the fluctuation itself. None of them
is "rank residues by MSF." That plain reading — the literal "based on structural fluctuations" — is
not retrieved by the recorded search as a published, benchmarked allosteric-site method at all.
[Per ADR 0019, this is an absence in a scoped search, not a claim that none exists.]

### 5.2 "Cryptic sites open where fluctuation is high" — for and against

**For.** Beglov, Hall, Wakefield, Luo, Allen, Kozakov, Whitty & Vajda 2018,
doi:10.1073/pnas.1711490115: "As expected, regions around cryptic sites exhibit **above-average
flexibility**, and close to **50 %** of the proteins studied here have unbound structures that could
accommodate the ligand **without clashes**" [VERIFIED-ABSTRACT].

**Against, from the same abstract.** Flexibility is not what makes the site druggable: "the strong
hot spot neighboring each cryptic site is **almost always exploited** by the bound ligand" — the
discriminating feature is a binding-energy hot spot, not motion. And the motions that matter are
small and local: cryptic sites are occluded by "intrusion of loops (**22.5 %**), side chains
(**19.4 %**), or in some cases entire helices (**5.4 %**)," while "motions that create sites that
are **too open** can also eliminate pockets (**19.4 %**)" — high fluctuation destroys pockets as
often as it creates them, to within a fifth of the cases either way. Most damning for a flexibility
ranker: "cryptic sites formed **solely** by the movement of side chains, or of backbone segments with
fewer than five residues, result **only in low affinity binding sites** with limited use for drug
discovery" [VERIFIED-ABSTRACT]. The high-fluctuation regions a Cα ENM cannot even see are the ones
that would not be worth finding.

**Against, structurally.** Yang & Bahar 2005, doi:10.1016/j.str.2005.03.015, on 98 enzymes: "In more
than **70 %** of the examined enzymes, the **global hinge centers** predicted by the GNM are found to
be **colocalized with the catalytic sites**," and "low translational mobility (**< 7 %**) is observed
for the catalytic residues"; ligand binding sites "enjoy a **moderate** flexibility"
[VERIFIED-ABSTRACT]. So a global-mode fluctuation ranking puts the **active site at the bottom** and
the flexible termini and loops at the top. Since our scoring conditions on the active site, a naive
MSF ranking is close to an anti-correlated proxy for it, and the top of the list will be
solvent-exposed loop and terminus residues — which is exactly the "non-functional surface" negative
class the challenge asks us to beat (`CHALLENGE.md` §4.1).

**The one large-N experimental result that supports a fluctuation route.** Wankowicz, de Oliveira,
Hogan, van den Bedem & Fraser 2022, doi:10.7554/eLife.74114, multiconformer-modelled **743
stringently matched apo/holo crystallographic pairs** and found "when binding site residues become
**more rigid** upon ligand binding, **distant residues tend to become more flexible**, especially in
**non-solvent-exposed regions**" [VERIFIED-ABSTRACT]. That is allosteric entropy redistribution,
measured on experimental data at N = 743 with no simulation. It is evidence the fluctuation signal
is real. It is **not** a prediction method — it reads the holo state — but it says what a fluctuation
predictor should be looking for: a **buried** residue whose flexibility is coupled to the active
site's, not the most flexible residue.

**PocketMiner's baseline table, for calibration.** Full text retrieved: on the 39-protein cryptic
pocket set, the only baseline compared is CryptoSite — "PocketMiner providing a small advantage
(ROC-AUC: **0.87** for PocketMiner vs. **0.85** for CryptoSite)" — and **no flexibility-, B-factor-
or normal-mode-based baseline appears at all** [VERIFIED-FULLTEXT via PMC9977097]. Training data:
"This dataset included **37 proteins and 2400 independent MD simulations** at least 40 ns in length"
— C2-illegal, as already recorded. The field's flagship cryptic-pocket predictor never measured
itself against the cheap fluctuation baseline. That gap is ours to measure.

For scale on the target class: CryptoBank (Martinez, Fröhlking, Borsatto & Gervasio 2026,
doi:10.1126/sciadv.ady6364) applied ML to "more than **6 million** structural alignments of unbound
(apo) and bound (holo) protein pairs from the Protein Data Bank" and reports cryptic pockets
"occurring in ~**18 %** of protein clusters" [VERIFIED-ABSTRACT].

---

## 6. Deposited experimental fluctuation data — arguably C2-legal, mostly unavailable

C2 forbids MD trajectories and MD-trained weights. It says nothing about **measured** fluctuations.
A deposited B-factor is an experimental observable of the apo crystal, C1-clean by construction. The
question for each source is availability for an _arbitrary_ apo entry, not for a lucky few.

| Source                                                                                        | What it reports                                                                                                                                                                                                                                                                                                                       | Available for an arbitrary apo entry?                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | C1/C2                                                                                                                                                                                     |
| --------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Per-atom B-factors**                                                                        | isotropic ADP: thermal motion + static disorder + lattice + refinement model, inseparably (§1.3)                                                                                                                                                                                                                                      | **Yes, always.** Every X-ray entry has them. Already parsed by `allo.structure`.                                                                                                                                                                                                                                                                                                                                                                                                                                             | clean / clean                                                                                                                                                                             |
| **Anisotropic ADPs**                                                                          | directional displacement                                                                                                                                                                                                                                                                                                              | **Rarely.** Requires roughly sub-1.2 Å data; the Kondrashov 2007 study needed a curated set of 83 "ultrahigh-resolution" structures to get them [VERIFIED-ABSTRACT]                                                                                                                                                                                                                                                                                                                                                          | clean / clean                                                                                                                                                                             |
| **TLS groups**                                                                                | rigid-body translation/libration/screw per group (Winn, Isupov & Murshudov 2001, doi:10.1107/S0907444900014736) [VERIFIED-ABSTRACT]                                                                                                                                                                                                   | **Sometimes**, in the REMARK 3 records where used. No retrieved source states the PDB-wide fraction; the 2001 paper does not address deposition prevalence. Write "unknown"                                                                                                                                                                                                                                                                                                                                                  | clean / clean                                                                                                                                                                             |
| **Ensemble refinement models** (Burnley, Afonine, Adams & Gros 2012, doi:10.7554/eLife.00311) | an explicit ensemble fitting the diffraction data; "Modeling of **20** protein datasets at **1.1–3.1 Å** reduced cross-validated R_free by **0.3–4.9 %**" [VERIFIED-ABSTRACT]                                                                                                                                                         | **No — must be produced, not fetched.** And the method itself "sampled by **molecular-dynamics simulation**" internally, so producing one for our targets would run MD. **C2-illegal as a production route**; a _deposited_ ensemble would be a grey area we should not need to enter                                                                                                                                                                                                                                        | clean / **illegal to produce**                                                                                                                                                            |
| **qFit multiconformer models** (Riley et al. 2021, doi:10.1002/pro.4001) [VERIFIED-ABSTRACT]  | discrete alternate conformers from density                                                                                                                                                                                                                                                                                            | **No.** Must be run, and needs good density. Related: qFit-ligand found "up to **29 %** of protein crystal structures bound with drug-like molecules present evidence of unmodeled ... conformations" (doi:10.1021/acs.jmedchem.8b01292) [VERIFIED-ABSTRACT] — i.e. heterogeneity is systematically under-modelled in deposited files. No retrieved source gives a resolution cut-off or a count of re-refined PDB entries; write "unknown"                                                                                  | clean / clean (no MD)                                                                                                                                                                     |
| **Room-temperature vs cryo**                                                                  | Fraser et al. 2011, doi:10.1073/pnas.1111325108: "crystal cryocooling remodels the conformational distributions of **more than 35 %** of side chains" [VERIFIED-ABSTRACT]. Confirmed not to be a radiation artefact (doi:10.1107/S1600577516017343) and re-examined at 277 K (doi:10.1107/S2059798322005939) [both VERIFIED-ABSTRACT] | **No — a lucky few.** Requires a matched RT dataset to exist                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | clean / clean                                                                                                                                                                             |
| **NMR model ensembles**                                                                       | spread across deposited models                                                                                                                                                                                                                                                                                                        | **Only for NMR entries**, which our targets are not (all four are crystal or the c-Myc heterodimer). And the spread is protocol-dependent: Lezon 2012 found "no correlation ... between force constants fit to NMR data and those fit to X-ray data, possibly due to the **inability of NMR data to accurately capture protein dynamics**" [VERIFIED-ABSTRACT]; Dziadek et al. 2024 found the predictor ranking **inverts** between NMR-derived and X-ray-derived fluctuation profiles on 100 structures [VERIFIED-ABSTRACT] | clean / clean, but low trust                                                                                                                                                              |
| **PDBFlex** (Hrabe et al. 2016, doi:10.1093/nar/gkv1316)                                      | observed structural variation across all PDB depositions of the same protein at **95 % sequence identity**, with per-residue average local RMSD [VERIFIED-ABSTRACT]                                                                                                                                                                   | **Only where the protein has many depositions.** Kinases and KRAS do; a singleton does not                                                                                                                                                                                                                                                                                                                                                                                                                                   | **C1 HAZARD.** At 95 % identity the cluster for any of our targets will contain the **holo** entries. Reading PDBFlex for our targets reads the answer. Do not use on the prediction path |
| **HDX-MS**                                                                                    | amide exchange rate as a proxy for local flexibility; "**peptide-level**, and sometimes residue-level" (doi:10.64898/2026.07.14.738285); residue resolution needs ECD/ETD fragmentation (doi:10.1021/jasms.6c00020); reviewed doi:10.1042/BCJ20250131 [all VERIFIED-ABSTRACT]                                                         | **No.** Per-study, deposited to PRIDE when deposited at all; "data availability depends on individual studies" [VERIFIED-ABSTRACT]. No systematic per-entry resource retrieved                                                                                                                                                                                                                                                                                                                                               | clean / clean, but not obtainable                                                                                                                                                         |

**The one row that matters.** Only per-atom B-factors are available for every apo entry, cost
nothing, and are already in our parsed structures. Everything else in this table is either a
lucky-few dataset, a C1 hazard, or a thing we would have to compute — and one of those computations
runs MD.

Sequence/structure predictors of B-factors, if we ever want a B-factor for an entry that lacks a
trustworthy one: **OPUS-BFactor** (doi:10.3390/molecules30122570), transformer over structure
features plus ESM-2 embeddings, sequence-only or structure-only mode, "significantly outperformed
other B-factor prediction methods" on CAMEO and CASP15 test sets — no correlation figure in the
abstract [VERIFIED-ABSTRACT]. C2-legal (labels are experimental B-factors). Also, on the question of
whether AlphaFold's own confidence is a flexibility proxy: CASP16's cryo-EM assessment across 38
targets found "the correlation between the local resolution and pLDDT was **less clear**" than with
RMSF, "especially when mobile domains were present" (doi:10.1002/prot.70099) [VERIFIED-ABSTRACT].
pLDDT is not a fluctuation measurement.

---

## 7. Cost to run on our set (4 mandatory, up to 13 targets; 147–1058 residues)

All figures below marked [UNVERIFIED] are our own arithmetic from stated complexities, not retrieved
runtimes.

| Route                                           | Cost on 13 targets                                                                                                                                                                                                                                                              | Dependencies beyond what we have                                                                                   |
| ----------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| Per-residue mean B-factor                       | **Free.** Already parsed. One `groupby`                                                                                                                                                                                                                                         | none                                                                                                               |
| GNM MSF                                         | Symmetric eigendecomposition of an N × N Kirchhoff matrix. At N = 1058, ~1.2 × 10⁹ flops, sub-second in LAPACK; ~9 MB working memory. **Seconds for all 13** [UNVERIFIED — our arithmetic]                                                                                      | `numpy.linalg.eigh` only                                                                                           |
| ANM MSF + mode directions                       | 3N × 3N Hessian; at N = 1058 that is 3174², ~3 × 10¹⁰ flops and ~80 MB. **Under a minute for all 13** [UNVERIFIED — our arithmetic]                                                                                                                                             | `numpy` only                                                                                                       |
| ESSA-style soft-mode frequency shift            | N repeated ANM/GNM solves, one per residue. At N = 1058 that is ~1058 × the above ≈ tens of minutes per target, hours for all 13; trivially parallel, and the low-mode subset can be tracked with a sparse solver instead of a full decomposition [UNVERIFIED — our arithmetic] | `numpy`/`scipy.sparse.linalg`                                                                                      |
| Zheng-style mode-guided ensemble + pocket score | Published **1–2 h for ~400 residues** [VERIFIED-ABSTRACT/FULLTEXT]. Scaling superlinearly with N for the rebuild and pocket-detection steps, order **1–3 CPU-days** for 13 targets [UNVERIFIED — our extrapolation]                                                             | backbone/side-chain rebuild (PULCHRA-class) **and** a pocket detector (fpocket/Concavity) — two new external tools |
| AF2 MSA subsampling, Meller protocol            | 160 predictions × 13 targets, dominated by the 1058-residue chains; order **1–3 GPU-days** plus MSA construction [UNVERIFIED — our arithmetic]                                                                                                                                  | GPU, AF2 weights, an MSA database, a template-off guard, and a per-target training-cutoff audit (§3.2)             |
| Str2Str / PDB-AlphaFlow                         | GPU inference per conformer; comparable order to the above                                                                                                                                                                                                                      | GPU, checkpoint provenance verification                                                                            |

The ratio is the finding. The two cheapest rows cost **seconds** and need **nothing new**. The
routes that need a new dependency cost three to four orders of magnitude more and, in the AF family,
also cost a C1 argument.

---

## What this changes for our pipeline

Ranked. Each names the stage it touches.

1. **Do not open the fluctuation route as a second deliverable. It is not one.** `CHALLENGE.md` §4.1
   requires a ranking by dynamic connectivity and §5 requires an N × N connectivity matrix; a
   per-residue fluctuation vector is neither. _Stage: deliverable framing / `docs/report/`._ This
   corrects the natural reading of the §2 summary sentence that motivated this file.

2. **Add two fluctuation columns to `classical/` this week, and let them settle the route.**
   `mean_bfactor` (per-residue mean of the deposited apo B-factors, already parsed) and `gnm_msf`
   (diagonal of the pseudo-inverse Kirchhoff matrix on the contact graph we already build). Both are
   C1-clean, C2-clean, C6-native or C6-agnostic, and both are seconds of compute with no new
   dependency. Score them through `allo.scoring.score_arm` on the secondary set's `development` tier
   beside `−distance` and `cavity_volume`. _Stage: `classical/`, Phase 1.4._

3. **The single cheapest decisive experiment is `mean_bfactor`, and the reason is that it is the
   route's oracle.** GNM reaches only r ≈ 0.59–0.64 against B-factors on hundreds of proteins
   (§1.2). So the deposited B-factor is an upper bound on what any MD-free _predictor_ of
   fluctuation can deliver, up to the crystal artefacts in §1.3. **If `mean_bfactor` does not
   separate real allosteric residues from the distal background, no predicted-fluctuation method
   will, and the route closes for one line of code.** Run `gnm_msf` in the same experiment as the
   control for the artefact objection: if B-factor fails but GNM MSF succeeds, the failure was
   lattice contamination, not the hypothesis. Two columns, one run directory, one afternoon.
   _Stage: `classical/` + `experiments/`._

4. **Expect the naive fluctuation ranking to fail, and pre-register that expectation.** Yang & Bahar
   put catalytic sites at global-hinge minima in >70 % of 98 enzymes with <7 % translational mobility
   (§5.2). A high-MSF ranking is therefore close to an anti-proxy for the active site, and its top
   entries will be exposed loops and termini — the challenge's own negative class. Panjkovich &
   Daura's direct measurement of the flexibility route is 65 % PPV at **0.22 sensitivity** on 91
   proteins. Writing this down before the run is what makes the result evidence either way.
   _Stage: `experiments/REGISTRY.md`._

5. **The usable fluctuation signal is a spectral _perturbation_, not a fluctuation magnitude — and
   it is already on the must-clear bar.** ESSA, APOP, PARS and binding leverage all rank by how a
   pocket or residue _shifts the soft-mode spectrum_. If step 2 shows any life, the next arm is an
   ESSA-style per-residue soft-mode frequency shift, which is N repeated ENM solves and still needs
   no new dependency. Do not build it before step 2 reports. _Stage: `classical/`, then `network/`._

6. **Zheng's mode-guided sampler stays the recommended MD-free ensemble generator, but re-scope what
   it competes against.** Full text confirms: 30 lowest modes, RMSD amplitudes 1–5 Å, per-residue
   pocket score averaged over the ensemble, no MD, 1–2 h for ~400 residues; the benchmark behind it
   is the 2021 paper's AUC > 0.8 on 14 test proteins after training on 84 cryptic sites, not the 2023
   paper, which reports four qualitative case studies. Its readout is an ensemble-averaged **cavity
   detector**, so its honest comparator is our `cavity_volume` baseline, not `−distance`. It needs a
   backbone rebuild and a pocket finder — two new external tools — so it is a Phase-4 item, not a
   Phase-2 one. _Stage: `network/` (as a graph-input generator), Phase 4._

7. **`review/05` §3's treatment of AlphaFold-family generators needs a C1 amendment, not just a C2
   one.** Three separate C1 exposures: template search can retrieve the target's own holo entry;
   the weights have memorised holo structures deposited before the checkpoint cutoff (Schafer &
   Porter's central finding); and AF3's cryptic-pocket competence is reported to depend on being
   _given the cryptic-site ligand_, which is holo information. Before any AF-family model enters
   the prediction path, add a gate that (a) disables templates and (b) checks each holo validation
   entry's deposition date against the checkpoint cutoff. Newer checkpoints are strictly worse.
   _Stage: `allo.inputs` / `tests/test_no_leakage.py`._

8. **Two C2 verdicts to record now, because they are easy to get wrong.** **Boltz-2 is
   C2-illegal, unconditionally** — its own text says it is supervised on MD ensembles from MISATO,
   ATLAS and mdCATH and on B-factors derived from MD trajectories. **idpGAN is C2-illegal** — it is
   trained on coarse-grained and atomistic simulation. **Str2Str remains the only fully clean
   generative option** ("trained on general crystal structures ... no reliance on simulation data
   during both training and inference"). _Stage: `docs/adr/` or `review/02-ai-methods.md`._

9. **Do not touch PDBFlex for our targets.** It clusters depositions at 95 % sequence identity, so
   the cluster for any of our four contains the holo entries. It is an answer key wearing a database
   URL. _Stage: leakage guard — worth naming in `tests/test_no_leakage.py`'s prose._

10. **One measurement gap worth claiming in the report.** PocketMiner's full text shows the field's
    flagship cryptic-pocket predictor benchmarked itself only against CryptoSite (0.87 vs 0.85 on 39
    proteins) and against **no flexibility, B-factor or normal-mode baseline at all**. If step 2
    produces a number, it is a number the cryptic-pocket literature has not published.
    _Stage: `docs/report/`._

---

## Method

**Databases.** Europe PMC REST (`search` with `resultType=core` for complete abstracts;
`fullTextXML` and the PMC article page for full text), arXiv API (`export.arxiv.org/api/query`),
bioRxiv, and two WebSearch calls for items with no open record. Semantic Scholar was not used
(HTTP 429, per conventions §3). PubMed E-utilities was not needed — Europe PMC covered the same
records with abstracts attached.

**Queries, by section.**
§1: GNM/ANM × B-factor correlation (2); elastic network × crystal environment × B-factor (1); Kundu
/ vGNM / Hinsen by title (1); Kuzmanic & Zagrovic by author (1); Fuglebakk by author (1); DOI-batch
for Kondrashov 2006/2007 and Lezon 2012 (1); Dziadek/Guan DOI batch (1); pLDDT × flexibility (1).
§2: normal-mode overlap papers by title (1); HingeProt/PACKMAN/alpha-shape (1); Zheng by author ×
cryptic × normal mode (1); Zheng 2021 DOI (1); Zheng 2023 DOI, `fullTextXML` (404) then PMC article
page (2); ENM × cryptic × pocket detection (1); NOLB by title (1); ANMPathway/ESSA/APOP DOI batch (1).
§3: AlphaFold × cryptic pocket (1); AF2 MSA subsampling / SPEACH_AF / AFsample / alternative
conformations (1); Meller 2023 JCTC full text via PMC (1); DOI batch for Schafer & Porter, del Alamo,
Beglov, Janson (1); ConforFold DOI (1); frustration × AlphaFold2 (1); AF3 weights terms (1
WebSearch).
§4: arXiv AlphaFlow/Str2Str/idpGAN (1); arXiv conformational-ensemble × generative, date-sorted, 30
results (1); Boltz-1/Boltz-2 on arXiv (1); Boltz-2 training data — WebSearch (1), bioRxiv landing
page (1, no training section), PDF (1, unreadable binary), PMC full text (1, successful).
§5: PARS/SPACER/normal-mode allosteric-site (2); Mitternacht by author (1); ESSA by title (1);
Yang & Bahar catalytic-site/global-hinge (1); cryptic × flexibility × descriptor (1); PocketMiner
full text via PMC (1); PocketMiner/AF3/OPUS-BFactor DOI batch (1); Bahar × intrinsic dynamics (1).
§6: ensemble refinement / qFit / RT-vs-cryo (1); Burnley + PDBFlex + TLS DOI batch (1); HDX ×
allosteric (1, returned an unrelated record — repeated as HDX-MS × resolution/database, 1);
Wankowicz by author (1); qFit × alternate conformations × PDB (1).

**Counts.** 32 retrieval calls (29 WebFetch, 2 WebSearch, plus 1 failed `fullTextXML` and 1
unreadable PDF). Roughly 190 records surfaced across the result sets; **58 screened in** and cited
with a DOI or arXiv ID retrieved this session. Full text was landed for five: Zheng 2023
(PMC10066797), Meller 2023 JCTC (PMC10373493), PocketMiner (PMC9977097), Boltz-2 (PMC12262699), and
the AF3 weights terms via search summary (partial). Everything else is abstract-level, tagged
accordingly.

**Stopping rule.** Stop a section when (a) every explicit sub-bullet of the brief has at least one
sourced citation with a stated C1/C2/C6 verdict, and (b) two further independent queries return only
records already screened. §4 was extended past that rule because the C2 verdict on Boltz-class models
is load-bearing and the abstract-level record was ambiguous; it took four attempts to reach the
training-data section.

**Not reached this session.**

- The PDB-wide fraction of entries carrying TLS parameters, and the count of entries re-refined with
  qFit. Recorded as "unknown", not as zero.
- A resolution cut-off for multiconformer modelling. Not stated in any retrieved abstract.
- ConforFold's training corpus. The abstract names the architecture, not the data. C2 verdict left
  **UNRESOLVED**, not guessed.
- AF3's exact training cutoff and Boltz-2's PDB cutoff, from primary sources. Both are reported in a
  retrieved web-search summary only and are tagged [UNVERIFIED].
- A published head-to-head of a fluctuation-only baseline against a cryptic-pocket or allosteric-site
  predictor. Not retrieved by the recorded search — which is the gap item 10 above proposes to fill,
  stated per ADR 0019 as an absence in a scoped search rather than an absence in the literature.
- Runtimes for AF2/Str2Str at 1058 residues. Every cost figure in §7 marked [UNVERIFIED] is our own
  arithmetic from stated complexities and published prediction counts.
