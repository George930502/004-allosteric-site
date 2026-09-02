# What physically carries an allosteric signal, and which observable therefore measures it

**Scope:** the phenomenon, not the algorithms. What moves between an effector site and an
active site, on what timescale, through which chemical structures, how strongly it decays
with distance, and which mathematical observable is a defensible proxy for that mechanism.
It deliberately excludes every method, propagator, circuit and predictor — those are the
sibling files' subject.
**Sibling files:** `00-conventions.md` (rules, and the eleven quantum insertion points already
closed by measurement). The algorithm reviews cover elastic-network baselines, quantum
propagators, pocket detection, machine learning, coarse-graining, hardware and evaluation.
**Retrieved:** 2026-08-25.

---

## 0. Why this file exists

Rule R1 says a method must state what it computes and what assumption makes that meaningful
*here*. That check is impossible without a description of the phenomenon that is independent
of any method. This file supplies it, so that a proposed observable can be judged against
the physics rather than against another algorithm's leaderboard position.

Two positions in `docs/FIELD.md` §4 are load-bearing and are defended below with sources
rather than asserted: trap 2, that residue-scale coherence is not the mechanism and a quantum
walk is used as a **mathematical propagator**, and trap 3, that the photosynthesis coherence
literature was substantially revised.

---

## 1. The three model families, and where each one now stands

**MWC (concerted).** A symmetric oligomer pre-exists in two states; effector binds the state
it prefers and shifts the equilibrium. **KNF (sequential).** Binding induces a local change
that propagates subunit to subunit. Both are conformational and both are stated in
`CHALLENGE.md` §10's reading of the field. Cui & Karplus reviewed the atomistic evidence and
concluded that the "new view" of allostery built on population shifts "is, in fact, an 'old
view'", and that mechanisms go beyond the classical MWC/Pauling-KNF descriptions
[VERIFIED-ABSTRACT] (doi:10.1110/ps.03259908).

**Ensemble / population shift.** A protein is a thermodynamic ensemble of microstates; an
effector reweights the ensemble. Gunasekaran, Ma & Nussinov argued that all non-fibrous
proteins are potentially allosteric, because allostery "is a consequence of re-distributions
of protein conformational ensembles", and that "practically any potential drug binding to
the protein surface can alter the conformational redistribution" [VERIFIED-ABSTRACT]
(doi:10.1002/prot.20232). Tsai & Nussinov reconciled thermodynamics, free-energy landscape
and structure under one set of descriptors, and made the sharp point that "allosteric
coupling (or communication) does not determine the allosteric efficacy; however, a
communication channel is what makes potential binding sites allosteric"
[VERIFIED-ABSTRACT] (doi:10.1371/journal.pcbi.1003394). Motlagh, Wrabl, Li & Hilser stated
the modern paradigm: allostery is facilitated by dynamic and intrinsically disordered
proteins, and understanding it "focuses on the conformational ensemble and the statistical
nature of the interactions responsible for the transmission of information"
[VERIFIED-ABSTRACT] (doi:10.1038/nature13001).

**Cooper & Dryden 1984** is the origin of the entropic branch. They showed by statistical
thermodynamics that "cooperative interaction free energies amounting to several kJ·mol⁻¹ may
be generated" by ligand-induced changes in the *frequencies and amplitudes* of thermal
fluctuations, "even in the absence of a macromolecular conformational change", and that the
effect "can involve all forms of dynamic behaviour, ranging from highly correlated,
low-frequency normal mode vibrations to random local anharmonic motions"
[VERIFIED-ABSTRACT] (doi:10.1007/BF00276625, PMID 6544679). Motlagh restates the magnitude
as "cooperative energies on the order of a few kcal per mol without perturbing the average
structure" [VERIFIED-FULLTEXT] (PMC4224315).

**Hilser's COREX and the ensemble allosteric model (EAM).** COREX/BEST enumerates
partially-unfolded microstates from a single structure and returns residue-resolved
stability in kcal/mol, with no MD trajectory required [VERIFIED-ABSTRACT]
(doi:10.1093/bioinformatics/bti520; doi:10.1007/978-1-62703-658-0_14). The EAM formulates
allostery as conformational free energies of cooperative elements plus coupling interactions
between them, and reports "allosteric ground rules" relating structurally different proteins
[VERIFIED-ABSTRACT] (doi:10.1146/annurev-biophys-050511-102319). Its most transferable
prediction is that "energetic coupling ... is maximized when one or more domains are
disordered", because a disorder-to-order transition contributes extra coupling
[VERIFIED-ABSTRACT] (doi:10.1098/rstb.2017.0175).

**Where this leaves us.** None of the three families is dead. The ensemble view subsumes MWC
and KNF as limits. The operational consequence is that our observable must be able to score
a residue that never moves, because the carrier can be a change in the *width* of a
distribution rather than in its mean.

---

## 2. Entropic versus enthalpic allostery, and what NMR order parameters actually measure

The canonical demonstration is CAP (catabolite activator protein). Popovych et al. showed
that binding the first cAMP "has no effect on the conformation of the other subunit", while
the dynamics are modulated: the first cAMP partially enhances and the second completely
quenches protein motions, so that "the second cAMP binding incurs a pronounced conformational
entropic penalty that is entirely responsible for the observed cooperativity"
[VERIFIED-ABSTRACT] (doi:10.1038/nsmb1132, PMC2757644). This is negative cooperativity with
essentially zero mean structural change — Cooper & Dryden realised experimentally.

**What the order parameter is.** NMR relaxation yields a generalised order parameter, most
usefully O²_axis for the symmetry axis of a methyl-bearing side chain. It "ranges between 0,
which represents complete isotropic disorder, and 1, which corresponds to no internal motion
within the molecular frame", and models indicate entropy change is linearly related to change
in O² over roughly 0.1–0.9 [VERIFIED-FULLTEXT] (PMC5488930, doi:10.1073/pnas.1621154114).
It reports **picosecond-to-nanosecond amplitude of local disorder**, not a displacement and
not a pathway.

**How much allostery is entropic.** Wand and colleagues calibrated the "entropy meter" across
28 protein–ligand complexes and found the conformational-entropy term ranges from strongly
favourable to strongly unfavourable, and that "for about one-quarter of these complexes, the
absence of conformational entropy would render the resulting affinity biologically
meaningless" [VERIFIED-FULLTEXT] (PMC5488930). A survey of side-chain dynamics found methyl
groups in two membrane proteins "more dynamic in the ps-ns timescale than any soluble protein
characterized to date", retaining "extraordinary residual conformational entropy"
[VERIFIED-ABSTRACT] (doi:10.1002/anie.202003527). For PKA, "globally coordinated changes of
conformational entropy activated by ligand binding, together with synchronous and asynchronous
breathing motions" underlie cooperativity across the catalytic cycle [VERIFIED-ABSTRACT]
(doi:10.1038/s41467-019-08655-7). Solvent entropy is a separate and often-neglected channel:
in yeast chorismate mutase the two effectors differ in the number of associated waters and
in the sign of the solvent entropy change [VERIFIED-ABSTRACT] (doi:10.1021/acs.biochem.0c00277).

**A caution, not a refutation.** Nussinov & Tsai argue that a failure to *see* a conformational
change is not proof of its absence, listing crystallisation artefacts, disordered states,
neglect of quaternary structure and too-short simulations as reasons the change escapes
detection [VERIFIED-ABSTRACT] (doi:10.1016/j.sbi.2014.11.005). The honest summary: a
substantial minority of measured allosteric couplings is carried by fluctuation entropy, the
fraction is system-dependent and not established globally, and "unknown" is the correct answer
to "what fraction of allostery in general is entropic".

**Implication for a propagation metric.** A metric that ranks residues by *displacement* under
a perturbation cannot see CAP-type coupling at all. A metric sensitive to a change in the
*fluctuation spectrum* — a mode-amplitude or entropy readout of the network — can.

---

## 3. Propagation as a physical process: timescales, damping, temperature

Stock & Hamm drove a photoswitchable PDZ2 domain and measured the response with transient IR,
alongside non-equilibrium MD [VERIFIED-FULLTEXT] (PMC5941181, doi:10.1098/rstb.2017.0187).
Their findings are the most direct experimental description of an allosteric transition in
progress:

- The time traces "do not exhibit one or a few well-defined decay times. Rather they show a
  whole spectrum of timescales, covering six decades in time from 10 ps to 10 μs."
- Three physically distinct phases: **elastic response ≲0.1 ns**, **inelastic reorganisation
  ≈100 ns**, **structural relaxation ≳1 μs**.
- There is no gap in the dynamical content that would indicate a dominant barrier; the process
  resembles downhill folding on a flat, rugged landscape with "a large ensemble of different
  transition paths".
- "Allosteric communication is a genuinely inelastic and nonlinear process," and "the common
  assumption of linear response becomes questionable".

**Vibrational energy transfer sets the elementary rates.** A master-equation model
parameterised from non-equilibrium MD gives "typical transfer times of 0.5–1 ps" between
adjacent residues along the backbone, described by a diffusive scaling rule requiring only a
backbone diffusion coefficient and interatom distances; **contact transport, e.g. via hydrogen
bonds, is considerably slower (6–30 ps) at room temperature**, and follows "a new scaling rule
depending on the inverse square contact distance", validated on the allosteric protein PDZ3
[VERIFIED-ABSTRACT] (doi:10.1063/1.5140070). The earlier scaling-rule paper separated the two
channels explicitly: backbone transport "relies on a diffusion model", tertiary-contact
transport "is based on a harmonic model" [VERIFIED-ABSTRACT] (doi:10.1021/acs.jpclett.5b02514).

**Thermal transport, and the fact that it is anharmonic.** A Green–Kubo calculation on villin
headpiece gives a thermal conductivity of 0.3 ± 0.01 W m⁻¹ K⁻¹, in agreement with measurement
on other proteins [VERIFIED-ABSTRACT] (doi:10.1021/acs.jpcb.2c00958). Thermoreflectance on
solid protein films from 77 to 296 K found temperature trends indicating "that anharmonic
coupling of vibrations in the protein is contributing to thermal conductivity", in a
"fractal-like" vibrational network [VERIFIED-ABSTRACT] (doi:10.1021/jz500174x).

**Damping is the default condition at 310 K.** The relevant control experiment is temperature.
Below ~270 K a helical peptide is rigid and heat moves ballistically through collective
backbone motion; above that temperature the backbone becomes flexible and transport switches to
intramolecular vibrational relaxation, "a diffusive process that occurs through localized
vibrational modes" [VERIFIED-FULLTEXT] (PMC3949117, reporting the Hamm group's earlier result).
Body temperature is firmly in the second regime.

---

## 4. Non-linear and non-diffusive propagation — the challenge's "too linear" claim, tested

`CHALLENGE.md` §2 asserts that current approximations are "often too linear to capture the
complex, non-linear dynamics of biological signal propagation". The literature supports the
premise and refutes the implied remedy.

**The premise holds.** Stock & Hamm call the transition "genuinely inelastic and nonlinear"
and question linear response [VERIFIED-FULLTEXT] (PMC5941181). A local-in-time-and-space
analysis of thermal transport in a peptide found that "finite-size effects, pronounced
nonlinearities, and ballistic processes produce behavior that diverges from the macroscale",
and — the key sentence — "**Unlike transport through small-molecule systems, such as alkanes,
nonlinearity dominates over coherent processes at even quite short time- and length-scales**"
[VERIFIED-FULLTEXT] (PMC6789131, doi:10.1038/s41467-019-12700-w). The same work reports a
weak ballistic front at v = 1.7 nm ps⁻¹ along the backbone and an effective diffusivity
D_eff = 2.3 × 10⁻² nm² ps⁻¹, and notes that ballistic channels "will inevitably be obscured by
more prominent diffusive features".

**Ballistic transport is real but is the minority channel — and it is effector-dependent.**
In bovine serum albumin, ultrafast IR resolves two decay phases: a 10 ps ballistic, anisotropic
phase and a 29 ps diffusive phase. Without the allosteric effector the two are "of nearly equal
amplitude", but with sodium myristate bound to the distal site the decay is "dominated (75%) by
the ballistic (10 ps) component", i.e. **binding an allosteric effector increases the ballistic
fraction of energy transport** [VERIFIED-FULLTEXT] (PMC3949117, doi:10.1038/ncomms4100). Heat
crosses the connecting rigid helix bundles "without local heating of the helix bundles",
implying transport by collective motion rather than local mode excitation.

**But the transport class of protein VET overall is diffusive.** The controlled
injector/sensor experiment on a β-hairpin states it directly: "The overall VET efficiency of
interresidue contacts is a consequence of the **diffusive** nature of biomolecular VET, whose
mean square deviation ⟨x²(t)⟩ scales with time t, instead of t² as in the case of ballistic
transport" [VERIFIED-FULLTEXT] (PMC8172543, doi:10.1038/s41467-021-23591-1). That single
sentence is the sharpest available constraint on propagator choice, because a unitary walk is
the t² case.

**Solitons and discrete breathers: not retrieved as a supported mechanism.** Non-linear IR
spectroscopy confirmed self-trapped amide-I states in acetanilide and in model α-helices, but
concluded that "given the short lifetime, any biological relevance in the sense of Davydov's
initial proposal can probably be ruled out" [VERIFIED-ABSTRACT] (doi:10.1007/s10867-009-9126-3,
PMC2660395). A 2026 re-derivation with an open-system treatment found that "under normal
assumptions the quantum excitation energy remains orders of magnitude below the threshold
needed to drive a stable soliton", and that the mechanism "alone is not sufficient"
[VERIFIED-ABSTRACT] (doi:10.1007/s10867-026-09707-y). Supersonic discrete solitons survive
only under weak hydrogen-bond anharmonicity in a 1D chain model [VERIFIED-ABSTRACT]
(doi:10.1103/PhysRevE.85.021925). We should not build on solitons.

**The correct reading of "too linear".** The non-linearity the literature documents is
**anharmonic and dissipative** — mode-mode coupling, frustration in the free-energy landscape,
contact breaking before dihedral rotation. It is not interference. A unitary propagator is a
*linear* map on the state; adding quantum interference does not add the kind of non-linearity
the challenge text is pointing at. This is a claim we must make explicitly in the report,
because a judge in this field will make it for us.

---

## 5. The structural carriers

**Hydrogen bonds beat the backbone over short spans.** The decisive measurement placed a VET
injector and a VET sensor at defined positions on a tryptophan-zipper β-hairpin. Backbone
transfer between adjacent residues takes 0.2–0.3 ps and contact transfer 2–10 ps — about an
order of magnitude slower per step — yet "transfer over a hydrogen bond shortcut is about as
efficient as transport over a stretch of 3–4 amino acids in the backbone", and the conclusion
is that "even if cutting short backbone stretches of only 3 to 4 amino acids in a protein,
**hydrogen bonds are the dominant VET pathway**" [VERIFIED-FULLTEXT] (PMC8172543).

**The independent genetic confirmation is the β-sheet result.** In the complete allosteric map
of a small GTPase, allosteric mutational effects are largest in the sheet strand that contacts
the effector and decrease progressively in each subsequent strand; "propagation appears more
efficient across the sheet than along the backbone within a strand", with first-strand residues
that do not contact the partner *depleted* for allosteric mutations (OR = 0.16, P = 10⁻³)
[VERIFIED-FULLTEXT] (PMC10866706, doi:10.1038/s41586-023-06954-0). Inter-strand backbone
hydrogen bonds carry more signal than the covalent chain. Two orthogonal techniques agree.

**Side-chain contacts, and specifically the ones that change state.** In the Src map, residues
are classified by their contacts in active and inactive structures. Mutations in "active-only"
and "swapping" residues affect activity more than "inactive-only" residues, and "the differences
in |∆∆G_a| are strongest when considering contacts between **side chains**, including salt
bridges, pi-cation interactions, and side-chain to side-chain hydrogen bonds"
[VERIFIED-FULLTEXT] (PMC12893324, doi:10.1126/sciadv.aea2726). Salt bridges that rearrange
during activation are among the most damaging positions.

**Hydrophobic core and packing.** Comparative maps of five homologous domains find that buried
core positions are the strongest single predictor of a conserved allosteric hotspot (relative
SASA < 0.25, OR = 8.91, P < 2.2 × 10⁻¹⁶), that hotspots are enriched in β-strands (OR = 2.90)
and depleted in loops (OR = 0.49) [VERIFIED-FULLTEXT via publisher page]
(doi:10.1101/2025.06.20.660748; published as doi:10.1038/s41467-026-71005-x). In kinases the
"R-spine" — a non-contiguous hydrophobic column — carries strongly inactivating mutations at
every position [VERIFIED-FULLTEXT] (PMC12893324). Xenon-trapping plus coupling analysis showed
internal hydrophobic cavities ~20 Å from the active centres are essential for function
[VERIFIED-ABSTRACT] (doi:10.1371/journal.pone.0077781).

**Water.** Structured water is a genuine carrier and a genuine C5 problem. A cellular-context
study concluded "entropy contributes favorably to the allosteric effect", highlighting the role
of solvation water [VERIFIED-ABSTRACT] (doi:10.1021/acs.jpcb.6c01283). In GPCRs a continuous
internal water column is part of the activation-competent state and sodium binding "disrupts"
it [VERIFIED-ABSTRACT] (doi:10.64898/2026.03.27.714850). C5 permits waters "modelled as simple
nodes"; nothing in this review requires that we do so, and doing so on apo structures would be
unreliable because ordered waters are resolution-dependent.

**Disulfides, loops and cofactors.** In albumin, disulfide-pinned rigid helix bundles are the
conduit and the *flexible* ligand-binding sites are where energy is deposited
[VERIFIED-FULLTEXT] (PMC3949117). Stock & Hamm found the PDZ2 reorganisation "mediated by a
change of atomic contacts and dihedral angles in the **flexible loop regions**"
[VERIFIED-FULLTEXT] (PMC5941181). These two are not in conflict: rigid elements conduct,
flexible elements convert. Cofactor-mediated coupling (nucleotide, heme, metal) is real and in
all our targets the nucleotide or the effector is a node; C5 allows simple-node treatment.

---

## 6. Evolution as an independent signal

**The original claim.** Lockless & Ranganathan's statistical coupling analysis (SCA) found, for
the PDZ family, "a set of energetically coupled positions ... that includes unexpected
long-range interactions", confirmed by mutation, forming "connected pathways through the protein
fold" [VERIFIED-ABSTRACT] (doi:10.1126/science.286.5438.295). Süel et al. extended this to
three unrelated families and reported "a surprisingly simple architecture ... a small subset of
residues forms physically connected networks that link distant functional sites"
[VERIFIED-ABSTRACT] (doi:10.1038/nsb881). Halabi et al. decomposed a protease family into three
quasi-independent "sectors", each physically contiguous with a distinct functional role
[VERIFIED-ABSTRACT] (doi:10.1016/j.cell.2009.07.038, PMC3210731). This is the strongest
pathway-flavoured evidence in the field and it is sequence-only, so it satisfies C1 and C2.

**The strongest counter.** A reanalysis showed that the experimental support for sectors
"involves almost exclusively proteins with a single sector", and that in that case "sequence
conservation is the dominating factor in SCA, and can alone be used to make statistically
equivalent functional predictions" [VERIFIED-ABSTRACT] (doi:10.1371/journal.pcbi.1004091,
PMC4344308). SCA's advantage over plain conservation is unproven on the published evidence base.

**Conservation of allostery itself is weaker than assumed.** A 2025 review of two pyruvate
kinase homologues sharing 66.5% sequence identity found that "the available functional
comparisons do not provide strong evidence for conserved allosteric mechanisms"
[VERIFIED-ABSTRACT] (doi:10.1016/j.jmb.2025.169176). Ancestral reconstruction of Aurora A /
TPX2 activation found, surprisingly, that "evolution of this regulation is encoded in the
kinase and did not arise by a dominating mechanism of coevolution" [VERIFIED-ABSTRACT]
(doi:10.1126/science.aay9959, PMC9617290). Comparative allosteric maps do find a conserved
core with protein-specific surface extensions: 16 positions are hotspots in ≥3 of five
homologous domains, 9 in exactly two, 18 in only one [VERIFIED-FULLTEXT via publisher page]
(doi:10.1101/2025.06.20.660748). Partial conservation, not general conservation.

---

## 7. Experimental ground truth beyond crystallography

| Technique | What it reports | Timescale | Key source |
| --- | --- | --- | --- |
| NMR CHESCA | Covariance of chemical-shift responses across a library of effector analogues; clusters of coupled residues | equilibrium | doi:10.1073/pnas.1017311108 (PMC3076865) |
| CPMG relaxation dispersion | Exchange between a ground and a sparsely-populated excited state; populations, rates, Δω | µs–ms | doi:10.1007/s12551-015-0166-6 (PMC5425744) |
| ps–ns relaxation (S², O²_axis) | Amplitude of fast local disorder → conformational entropy | ps–ns | doi:10.1073/pnas.1621154114 (PMC5488930) |
| HDX-MS | Amide solvent accessibility and H-bonding, peptide-resolved | s–h | doi:10.1021/acs.biochem.1c00277 (PMC9659328) |
| Double-mutant cycles | Pairwise coupling free energy ΔΔG_int between two positions | equilibrium | doi:10.3390/ijms22020828 (PMC7830974) |
| Deep mutational scanning + thermodynamic modelling | Causal ΔΔG of folding and of binding/activity for every substitution | equilibrium | doi:10.1038/s41586-023-06954-0; doi:10.1126/sciadv.aea2726 |
| smFRET / optical tweezers | Distance distributions and folding-landscape changes on single molecules | ms | PMC8884448; PMC9745801 |

CHESCA reaches residues that structure comparison misses: the covariance networks "reach not
only sites subject to effector-dependent structural variations, but also regions that are
controlled by dynamics" [VERIFIED-ABSTRACT] (doi:10.1073/pnas.1017311108). HDX-MS and NMR on
thrombin/thrombomodulin measure different things — chemical environment of backbone N–H versus
amide solvent accessibility and H-bonding — and both are needed [VERIFIED-ABSTRACT]
(doi:10.1021/acs.biochem.1c00277).

**DMS is the new gold standard and it is where the quantitative laws in §8 come from.** It is
also the technique that shows how *extensive* allostery is: for a GTPase probed in its native
cellular network, "28% of the 4,315 assayed mutations show pronounced gain-of-function
responses", and 20 of the 60 positions enriched for gain-of-function lie outside the canonical
switch regions, with kinetics confirming allosteric coupling to the active site
[VERIFIED-ABSTRACT] (doi:10.1016/j.cels.2023.01.003).

**Do these agree with contact-network predictions?** Partly, and the disagreements are large.
See §9.

---

## 8. The distance-decay law — question (b), answered

**The claim traces to the deep-mutational-scanning allosteric-map literature and it is real.**
The general statement, verbatim: "the experimental allosteric maps generated to date all share
a characteristic distance-dependent decay of allosteric mutational effects away from the active
site" [VERIFIED-FULLTEXT via publisher page] (doi:10.1101/2025.10.20.683418).

**Functional form.** Exponential. The comparative-maps paper fits y = a·e^(bx), where a is the
estimated |ΔΔG_b| at distance 0, b is the decay rate, and **x is the minimum heavy-atom
side-chain distance to the ligand** — not Cα–Cα [VERIFIED-FULLTEXT via publisher page]
(doi:10.1101/2025.06.20.660748). The Src map uses the same form with minimum heavy-atom
distance to the active site [VERIFIED-FULLTEXT] (PMC12893324).

**Length scale (half-distance d½, the distance over which the effect halves):**

| System | d½ | Source |
| --- | --- | --- |
| GB1 | 5.6 Å | doi:10.1101/2025.06.20.660748 |
| PDZ domains, median of 7 interactions | 6.9 Å | doi:10.1101/2025.06.20.660748 |
| Src kinase domain, all 252 sites | 7.45 Å (k = −0.063 ± 0.008 Å⁻¹) | PMC12893324 |
| Src kinase domain (re-fit in comparative study) | 8.3 Å | doi:10.1101/2025.06.20.660748 |
| KRAS, median over six binding partners | 9.50 Å | doi:10.1101/2025.06.20.660748 |
| GRB2-SH3 | 13.6 Å | doi:10.1101/2025.06.20.660748 |

**The single most useful number in this file.** In Src, when the fit is restricted to *major
allosteric sites only*, the decay is much weaker: k = −0.038 ± 0.005 Å⁻¹, **d½ = 18.24 Å**,
against 7.45 Å for all sites [VERIFIED-FULLTEXT] (PMC12893324). Real allosteric sites decay
roughly half as fast as the background. That gap is the entire predictable signal above a
distance control.

**Sign matters.** Inhibitory mutations decay (k = −0.078 ± 0.004 Å⁻¹); **activating mutations
do not decay at all** (k = +0.011 ± 0.003 Å⁻¹). This is not an effect-size artefact:
inactivating mutations subsampled to matched effect sizes still show median k = −0.028 Å⁻¹,
simulation P = 1 × 10⁻⁴ over 10,000 subsamples [VERIFIED-FULLTEXT] (PMC12893324). Positive and
negative allostery are different physics.

**Two caveats.** (i) Transcription-factor maps report decay rates of 0.246 (FOXG1) and 0.171
(FOXP1) — three to four times steeper than the kinase and GTPase values — but the units are not
stated explicitly in the retrieved text, and the distance metric there is minimal 3D distance to
DNA rather than to a small-molecule active site, so these are not directly comparable
[VERIFIED-FULLTEXT via publisher page, units UNVERIFIED] (doi:10.1101/2025.10.20.683418).
(ii) Every d½ above is measured against a *bound partner or ligand*, i.e. on holo geometry. On
an apo structure the metric is defined against the apo active site, which is not identical.

**Consequence for us.** `00-conventions.md` §6 records that `ctrl_closeness = −distance` reaches
AUC 0.617 and that the best tested method leads it by 0.001. That is now explained rather than
merely observed: the ground truth *is* distance-decaying, with a half-distance of order 6–14 Å.
The correct response is not to beat distance with a better proximity ranker. It is to model the
decay explicitly as the null and score the **residual**.

---

## 9. Pathway or ensemble — question (a), answered

This is the decision-relevant question, because an interference-sensitive path-summing
propagator is the right instrument only if a small number of specific routes carries the signal.

**Evidence for PATHWAY-like:**

1. SCA sectors: "a small subset of residues forms physically connected networks that link
   distant functional sites" across three unrelated families [VERIFIED-ABSTRACT]
   (doi:10.1038/nsb881); physically contiguous, functionally distinct sectors
   [VERIFIED-ABSTRACT] (doi:10.1016/j.cell.2009.07.038).
2. Src: **major allosteric sites "are not arranged uniformly throughout the KD. Instead, they
   are spatially clustered and have higher connectivity than expected by chance"**
   [VERIFIED-FULLTEXT] (PMC12893324). Of 252 residues, only 42 qualify as major allosteric
   sites. An 11-residue previously-predicted allosteric network is enriched for large |ΔΔG_a|
   at OR = 14.57, P = 2.1 × 10⁻⁷¹, and still OR = 7.54 after excluding active-site and
   second-shell residues [VERIFIED-FULLTEXT] (PMC12893324).
3. KRAS: propagation is concentrated in one structural element, the central β-sheet, and is
   *depleted* along the backbone within a strand [VERIFIED-FULLTEXT] (PMC10866706).
4. Albumin: energy travels through specific rigid helix bundles, and specifically **not** into
   them — the buried-helix IR band is "conspicuously absent" from the heating spectrum
   [VERIFIED-FULLTEXT] (PMC3949117).
5. Anisotropy of ≥6-fold in decay rate between directions (§10) means transmission is not a
   function of distance alone, i.e. there is route structure.

**Evidence for ENSEMBLE-like:**

1. Motlagh/Hilser, directly on this point: "The classic notion of an allosteric pathway, through
   a static picture of the protein, often conveys a deterministic (or at least homogeneous)
   picture of the signal propagation process ... The ensemble model states that, in the most
   general case, activity is an ensemble-weighted contribution" [VERIFIED-FULLTEXT] (PMC4224315).
2. Stock & Hamm, from real-time measurement: single non-equilibrium trajectories are "vastly
   different"; changes "do not necessarily correspond to a directed sequence along certain
   residues, but may also occur **non-locally**" — a rigid segment lets conformational stress
   "directly propagate to distant sites". Their conclusion: "the commonly used term 'allosteric
   pathway' should not be taken literally as in a falling row of dominoes"
   [VERIFIED-FULLTEXT] (PMC5941181).
3. Extent: Src has 861 allosteric mutations at 168 of 252 non-active-site positions — two-thirds
   of the domain has at least one [VERIFIED-FULLTEXT] (PMC12893324). Allosteric control is
   "pervasive". For a GTPase in cells, 28% of all assayed mutations are gain-of-function
   [VERIFIED-ABSTRACT] (doi:10.1016/j.cels.2023.01.003).
4. Mechanistic degeneracy: for TetR, allostery can be modulated "by perturbing both inter-domain
   coupling and intra-domain properties", and "this mechanistic degeneracy qualitatively explains
   the broad distribution of allostery hotspots across the protein structure observed in the DMS
   experiments" [VERIFIED-FULLTEXT] (PMC12339756, doi:10.1016/j.jmb.2025.168998).
5. Gunasekaran et al.: allostery is a property of ensembles, so in principle any surface binder
   can perturb it [VERIFIED-ABSTRACT] (doi:10.1002/prot.20232).

**The resolution, and it is not a fudge.** The two bodies of evidence describe different
percentiles of the same distribution. There is a broad, weak, ensemble-like background of
coupling almost everywhere — two-thirds of positions in Src — superposed on a sparse, spatially
clustered, higher-connectivity minority (42/252 ≈ 17% in Src) that carries the large effects and
that decays with distance far more slowly (d½ 18.24 Å versus 7.45 Å). The mechanism is
ensemble; the *strong* couplings are structured.

**What that means for an interference-sensitive path-summing propagator.** It is the wrong
instrument as the primary readout and a plausible one as a secondary. Three reasons:

- The thing we are asked to rank is the tail, and the tail is clustered — so path structure
  exists. Good for a path-summing propagator.
- But the physical process is one where individual realisations differ wildly and propagate
  non-locally, so any *single* dominant path is an artefact of averaging. A propagator whose
  output depends on constructive/destructive interference between specific routes is asserting
  a phase relationship between routes that the measured process does not have — trajectories are
  incoherent with respect to one another at 310 K.
- Empirically this has already been settled in our own corpus: absolute CTQW transfer amplitude
  correlates −0.60 to −0.71 with distance and is a proximity ranker (`00-conventions.md` §5).
  §8 now explains *why*: the ground truth itself decays exponentially with distance, so any
  monotone-in-distance propagator will land near the distance control and no further.

**The instrument the physics actually recommends** is one that measures *how the fluctuation
spectrum of the network changes when a site is clamped*, not one that measures how much
amplitude arrives along a route.

---

## 10. Directionality — question (e), answered

Allosteric coupling is thermodynamically reciprocal in equilibrium (the coupling free energy
ΔΔG_int between two sites is symmetric by construction in a double-mutant cycle). Everything
else about it is asymmetric.

**Measured asymmetries:**

1. **Spatial anisotropy of decay.** Fitting the Src decay separately along three orthogonal axes
   in both directions gives d½ = 19.80 Å in the direction of helix αC, 15.40 Å and 9.37 Å along
   the two vertical senses, and only **3.22 Å** toward the regulatory-domain interaction surface
   (k = −0.215 ± 0.026 Å⁻¹). The paper's summary: transmission is "anisotropic: Transmission
   efficiency is dependent on the direction of propagation, with at least a **sixfold difference
   in decay rates** between the most and least efficient directions" [VERIFIED-FULLTEXT]
   (PMC12893324).
2. **Structural-element anisotropy.** Propagation across a β-sheet outruns propagation along the
   strand backbone [VERIFIED-FULLTEXT] (PMC10866706). In Src, mutations in β strands "have
   smaller effects than expected given their distance to the active site" [VERIFIED-FULLTEXT]
   (PMC12893324) — note this is the opposite sign to the KRAS sheet result, so sheet-mediated
   transmission is not universal.
3. **Sign asymmetry.** Inhibitory mutations decay with distance; activating mutations do not
   (§8). "This suggests different mechanisms underlie inhibitory and activating mutations"
   [VERIFIED-FULLTEXT] (PMC12893324).
4. **Energy-flow anisotropy.** In albumin, the early transient IR spectrum is spectrally distinct
   from the equilibrated one, which is the direct signature of anisotropic flow; and the flow
   route bypasses the intervening helix interiors [VERIFIED-FULLTEXT] (PMC3949117).
5. **Mutation-effect anisotropy at matched distance.** "Allostery is, however, anisotropic, with
   mutations in particular sites having stronger allosteric effects than other mutations at the
   same distance from the active site" [VERIFIED-FULLTEXT via publisher page]
   (doi:10.1101/2025.10.20.683418).

**The observable that captures direction.** Transfer entropy is the standard choice: it is
explicitly non-symmetric and "provides an approach to understanding asymmetric information flow
in coupled systems" [VERIFIED-ABSTRACT] (doi:10.1021/acs.jctc.1c00004). It can be computed from
a variance–covariance matrix, and a GNM-based formulation exists that needs no trajectory
[VERIFIED-ABSTRACT] (doi:10.1021/acs.jpclett.3c00366; doi:10.1016/j.ijbiomac.2026.151961) — the
C2-compatible route. A caution from `00-conventions.md` §5: a real symmetric contact graph has
no non-reciprocal hopping, so a *unitary* observable on it cannot be directional. Direction has
to come from somewhere else — a time-lag, an entropy production, or an explicit source/sink —
and that is exactly what GNM transfer entropy supplies.

---

## 11. Is a unitary propagator at 310 K defensible? — question (c), answered

**The indefensible framing** (do not write this): "protein allosteric signalling is a quantum
coherent process, so a quantum walk models it." Every element is contradicted. Protein VET is
diffusive, ⟨x²(t)⟩ ∝ t, not ballistic ⟨x²⟩ ∝ t² [VERIFIED-FULLTEXT] (PMC8172543). Nonlinearity
dominates over coherent processes at short times and lengths [VERIFIED-FULLTEXT] (PMC6789131).
The transition is inelastic and nonlinear, spanning 10 ps to 10 μs with no timescale gap
[VERIFIED-FULLTEXT] (PMC5941181). Above ~270 K the transport mechanism switches from collective
ballistic to localised diffusive [VERIFIED-FULLTEXT] (PMC3949117). And the adjacent quantum-biology
precedent was corrected: the photosynthesis review concludes that "interexciton coherences are
too short lived to have any functional significance in photosynthetic energy transfer", with the
long-lived signals reassigned to "impulsively excited vibrations"; the useful lesson is that
"Nature, rather than trying to avoid dissipation, exploits it" [VERIFIED-FULLTEXT] (PMC7124948,
doi:10.1126/sciadv.aaz4888). This is trap 3 in `docs/FIELD.md`, and the citation above is the
accurate history to use.

**The defensible framing** (write this, in these terms):

> The residue network is not a quantum system. We use exp(−iHt) as a **mathematical propagator
> on the contact Laplacian**, chosen because it sums over walks with a different weighting than
> exp(−Lt) does. The claim under test is empirical — that this weighting ranks allosteric
> residues better on our frozen benchmark — not physical. Every quantum term in this submission
> refers to the algorithm, never to the protein.

Two further honest points strengthen it rather than weaken it:

- **There is one genuine physical foothold, and it is small.** The measured ballistic component
  of energy transport is real (10 ps phase in albumin, 1.7 nm ps⁻¹ front in peptide) and it
  *increases* when an allosteric effector binds — from ~50% to 75% of the decay amplitude
  [VERIFIED-FULLTEXT] (PMC3949117). A unitary propagator is the ballistic limit. So the
  defensible statement is that a unitary walk is a caricature of the minority channel whose
  weight correlates with allosteric activity, and that a **mixture** of unitary and diffusive
  propagation is closer to the physics than either alone. `00-conventions.md` §5 item 3 records
  that ENAQT/dephasing showed no optimum over γ ∈ [0, 3J_max] on our data, so the mixture has
  already been tested as a *tunable* and failed; what has not been tested is the ballistic
  **fraction** as an effector-response readout.
- **The classical-simulability admission belongs in the same paragraph.** exp(−iHt) on a
  200 × 200 matrix is classical arithmetic (`docs/FIELD.md` trap 1). Saying so alongside the
  propagator framing costs nothing and buys credibility.

---

## 12. Does allosteric coupling correlate with a topology-only quantity that is not degree, burial or distance? — question (d), answered

**Short answer: not strongly, and the honest reading is that edge weighting matters more than
propagator choice.**

**What distance and burial already explain.** The Src map fitted a linear model of ΔΔG_a for
non-active-site mutations from simple features: minimum heavy-atom distance to nucleotide and to
the catalytic residue, wild-type and mutant amino-acid identity, solvent accessibility, contact
type and contact dynamics, and secondary-structure type. "Distance to the catalytic site and to
the nucleotide are the most predictive features when tested individually." All predictors
together reach **R² = 0.40** on held-out data (10-fold CV), rising to **0.46** with specific
secondary-structure elements [VERIFIED-FULLTEXT] (PMC12893324). Burial is the strongest single
correlate of a *conserved* hotspot across homologues (rSASA < 0.25, OR = 8.91)
[VERIFIED-FULLTEXT via publisher page] (doi:10.1101/2025.06.20.660748). So distance + burial +
secondary structure + residue identity leaves more than half the variance unexplained, and none
of the residual is claimed for a topology invariant.

**Candidates that are topology-only and are *not* degree/burial/distance:**

| Quantity | Evidence | Verdict |
| --- | --- | --- |
| Hydrogen-bond adjacency as a distinct edge class | H-bond shortcut ≈ 3–4 backbone residues (PMC8172543); across-sheet > along-strand (PMC10866706); side-chain H-bonds/salt bridges/π-cation discriminate ΔΔG_a (PMC12893324) | **Strongest.** Three independent techniques. |
| Contact-transfer rate ∝ 1/(contact distance)² | Master-equation scaling rule, validated on PDZ3 (doi:10.1063/1.5140070) | **A concrete, parameter-free edge weight.** |
| Local packing density (weighted contact number) | Better predictor of site-specific evolutionary rate than relative solvent accessibility (doi:10.1093/molbev/mst178); sequence entropy correlates with inverse packing density (doi:10.1093/protein/gzi009) | Promising, but it is close kin to degree and burial — a null must separate them. |
| Contact *dynamics* (contacts that swap between functional states) | Swapping and active-only residues carry the largest ΔΔG_a (PMC12893324) | Physically the best signal, but it needs two structures — **holo-derived, so C1-forbidden for us.** |
| Community/modular structure with residue-potential edge weights | Community structure with Miyazawa–Jernigan edge weights is "a more fundamental feature" for low-frequency modes (doi:10.1089/cmb.2017.0171) | Untested against allosteric labels here. |
| H-bond fluctuation correlations in the apo state | HBAlloMap claims apo-state H-bond fluctuation correlations suffice to reveal allosteric networks (doi:10.1021/acs.jpcb.5c03281) | Interesting and apo-only, but it derives the fluctuations from MD — **C2 violation as published**; the H-bond graph itself is reusable. |

**Does a better graph break C6?** No. C6 states that "the topology of the contact network is the
primary driver of signal propagation". Assigning an edge weight to a contact — 1/d², or a class
weight for a side-chain hydrogen bond or salt bridge versus a generic 5 Å contact — is a
refinement *within* the elastic-network hypothesis, not a departure from it. It is also the one
change with two orthogonal experimental justifications (femtosecond VET and deep mutational
scanning) rather than one.

---

## Observables the physics supports

Ranked by strength of the physical warrant, best first. Each names the mechanism it measures and
the assumption that has to hold for it to mean anything here.

1. **Distance-residual coupling: any propagation score minus its fitted exp(−k·d) trend.**
   *Mechanism:* local energetic propagation with an exponential distance law, measured half-distance
   5.6–13.6 Å across five systems, and 18.24 Å versus 7.45 Å for true allosteric sites versus
   background in Src (§8).
   *Assumption:* the decay law is the null, not the discovery. Requires the same distance metric the
   maps use — **minimum heavy-atom distance**, not Cα–Cα.
   *Why first:* it is the only construction that can, in principle, beat `ctrl_closeness` for a
   reason rather than by luck.

2. **Change in the fluctuation spectrum of the network when a site is clamped** — a GNM/ANM
   mode-amplitude or configurational-entropy response, not a displacement.
   *Mechanism:* dynamic allostery (Cooper & Dryden; CAP), where cooperativity of a few kcal/mol is
   carried entirely by a conformational-entropy change with no mean structural change (§1, §2).
   *Assumption:* contact topology sets the mode spectrum — Tirion, and C6 itself. Also that the
   entropic channel is a material fraction of the coupling, which is true for at least a quarter of
   measured complexes and is unknown in general.

3. **Edge-weighted transfer using hydrogen-bond and side-chain-contact classes, with contact rates
   scaled as 1/d².**
   *Mechanism:* VET is carried preferentially by hydrogen bonds and side-chain contacts, and an
   H-bond shortcut is worth 3–4 backbone residues; across-sheet beats along-strand (§5, §12).
   *Assumption:* the ps-scale energy-transfer network and the equilibrium allosteric coupling network
   are the same network. That is an assumption, supported by two independent measurement classes
   agreeing on the β-sheet result, but it has not been proved.

4. **A directed, non-symmetric coupling readout — GNM-based transfer entropy or an equivalent
   time-lagged quantity.**
   *Mechanism:* transmission efficiency differs by ≥6-fold between directions in Src, and positive
   and negative allostery obey different distance laws (§10).
   *Assumption:* direction is injected by a lag, a source/sink or an entropy production. A unitary
   walk on a real symmetric contact graph cannot supply it (`00-conventions.md` §5, item 11).

5. **Ballistic fraction: the ratio of a unitary transfer to a diffusive transfer at matched time,
   compared apo versus site-clamped.**
   *Mechanism:* effector binding raises the ballistic component of energy transport from ~50% to 75%
   of the decay amplitude in albumin (§4).
   *Assumption:* the ballistic/diffusive split on a coarse residue graph is a meaningful analogue of
   the split measured on atomic vibrations. Weak assumption; this is a **hypothesis to test**, not a
   result to claim. It is also the one place where the eleven closed insertion points leave room —
   ENAQT was tested as a tunable γ and failed, but the ballistic fraction as an effector-response
   readout was not tested.

6. **Local packing density / weighted contact number as an edge or node weight.**
   *Mechanism:* packing density predicts site-specific evolutionary rate better than solvent
   accessibility, and buried core positions are the strongest single correlate of a conserved
   allosteric hotspot (§5, §12).
   *Assumption:* it adds information over degree and burial. This must be shown against a
   degree-preserving null before it is claimed — `docs/FIELD.md` §3 is explicit that "buried and
   central" is the thing most methods actually find.

7. **Sequence-only coupling (SCA) as an orthogonal, C1- and C2-clean prior.**
   *Mechanism:* sparse, physically contiguous coevolving networks linking distant functional sites (§6).
   *Assumption:* SCA adds information over plain conservation. The published support for that is
   contested — conservation alone gave statistically equivalent predictions on the single-sector
   proteins that make up almost all the experimental evidence. Use only with a conservation control.

**Explicitly not supported by the physics:**

- **Bare quantum-walk transfer amplitude as the hit score.** It is a proximity ranker (measured:
  r = −0.60 to −0.71 with distance), and §8 explains why any monotone-in-distance quantity lands on
  the distance control's number.
- **Anything justified by residue-scale electronic coherence, soliton transport, or "interference is
  like allostery".** Solitons: ruled out on lifetime grounds and on excitation-energy grounds.
  Coherence: reassigned to vibrational origin in the one system where it was ever measured.
- **Contact-dynamics features derived from comparing two structures.** Physically the strongest
  signal in the Src map, and forbidden by C1 for us.

---

## What this changes for our pipeline

1. **Evaluation / scoring — the decay law becomes the null.** `allo.scoring` should compare methods
   against an exponential-decay baseline with the half-distance treated as a fitted nuisance
   parameter, not against a bare `−distance` control. The frozen protocol already stratifies by
   distance; §8 says the correct family is exp(−k·d) with d = minimum heavy-atom distance, and that
   the discriminating quantity is the *ratio* of decay rates between hits and background (≈2× in Src),
   not the rank correlation. *Note:* `docs/benchmark/evaluation/` is frozen and this file changes
   nothing in it. This is a statement about what a method should report alongside the frozen score.
2. **Network construction (`network/`, Phase 1.2) — weight the edges.** Hydrogen bonds and
   side-chain contacts are a distinct, faster-than-expected channel; contact rates go as 1/d². This
   is the highest-value change identified in this review and it is a change to the *graph*, not to
   the propagator. It stays inside C6.
3. **Quantum metric design (`quantum/`, Phase 2) — the primary observable should be a perturbation
   response of the fluctuation spectrum, not an arrival amplitude.** §9 and §2 both point the same
   way. An arrival-amplitude readout has already lost eleven times.
4. **Directionality is a stated deliverable-level gap.** The N×N connectivity matrix required by
   `CHALLENGE.md` §5 is symmetric if built from a unitary walk on a symmetric graph. The biology is
   asymmetric by ≥6-fold. If we want a directional matrix, the asymmetry must be injected
   deliberately (lag, source/sink, entropy production) and the report must say so.
5. **Report framing (Phase 5).** §11 supplies the exact wording for trap 2 and the exact citation
   for trap 3. Use the propagator framing verbatim; do not claim protein coherence.
6. **Do not add waters or model cofactors beyond simple nodes.** §5 shows water-mediated coupling is
   real, but apo ordered-water assignment is resolution-dependent and C5 permits only simple nodes.
   Record this as a named limitation rather than a modelling choice.
7. **A negative expectation to record now.** §9 predicts that any method whose score is a monotone
   function of graph distance will reproduce the `ctrl_closeness` AUC of 0.617 to within noise. If a
   new method lands there, that is the diagnosis, not a coincidence.

---

## Method

**Databases.** Europe PMC REST search (`resultType=core`) and full-text; PMC article pages
(`pmc.ncbi.nlm.nih.gov/articles/{PMCID}/`) as the fallback when `fullTextXML` returned HTTP 404;
one general web search and three publisher-page fetches for preprints and paywalled journals.
arXiv was not queried: the scope of this file is experimental biophysics and biochemistry, which
arXiv does not index well. Semantic Scholar was not attempted (rate limited per conventions §3).

**Queries run** (Europe PMC unless noted; 9 batches, 38 distinct queries):
Cooper & Dryden title search; ensemble-allostery foundational titles (Motlagh, Tsai & Nussinov,
Gunasekaran); `"allosteric" AND "decay" AND ("complete allosteric map" OR "allosteric maps")`;
KRAS energetic/allosteric landscape title; Stock+Hamm author pair with allosteric; energy transport
in proteins (title); thermal transport / thermal conductivity in proteins (title); solitons,
discrete breathers, energy localisation; ballistic AND diffusive AND vibrational energy AND protein;
statistical coupling analysis / protein sectors; coevolution AND allosteric; conformational entropy
AND order parameters AND NMR AND allostery; dynamically driven protein allostery; entropy meter;
CHESCA / chemical shift covariance analysis; hydrogen-deuterium exchange AND allostery; double
mutant cycles; allosteric pathway critique terms; allostery AND asymmetry/directionality/causal;
water/hydration AND allostery; benchmark/assessment/evaluation AND allosteric; ensemble allosteric
model / COREX; population shift AND pathway; "allostery without a conformational change"; degenerate
/ redundant pathways; hydrogen bond AND allostery; network model AND edge weight AND allosteric;
deep mutational scanning AND allostery; TetR hotspots; "quantum biology revisited"; transfer entropy
AND allosteric; single-molecule / force spectroscopy AND allostery; rotamer AND allosteric; packing
density AND dynamics; relaxation dispersion AND allostery. Web search: the exact phrase
`"distance-dependent allosteric decay" "all complete allosteric maps"`.

**Counts.** Roughly 310 records returned across all queries; 62 screened in on title/abstract;
**14 full texts retrieved and read** in this session (PMC12893324 Src; PMC10866706 KRAS; PMC5941181
Stock & Hamm; PMC8172543 through-bonds-or-contacts; PMC6789131 topology/landscapes; PMC3949117
albumin; PMC4224315 Motlagh; PMC12339756 TetR; PMC5488930 Wand entropy; PMC7124948 Cao quantum
biology; PMC7585012 and PMC6688844 retrieved but not quoted; plus two publisher pages,
doi:10.1101/2025.06.20.660748 and doi:10.1101/2025.10.20.683418, read via WebFetch).

**Stopping rule.** Stop when each of the five STEP-3 questions has at least two independent primary
sources, and when a new query returns no record that changes an answer. Reached for (a), (b), (c),
(d) and (e). Question (b) was additionally cross-checked by locating the same decay law in four
separate protein systems.

**What could not be reached.**
- The published journal version of the comparative PDZ maps (doi:10.1038/s41467-026-71005-x) is
  behind an authentication redirect at nature.com; the numbers used here come from the bioRxiv
  version of the same work (doi:10.1101/2025.06.20.660748) read via publisher page. The two abstracts
  agree on the claims quoted.
- The transcription-factor decay rates (0.246 for FOXG1, 0.171 for FOXP1) are reported without
  explicit units in the retrieved text; treated as `[UNVERIFIED]` for units and excluded from the
  cross-system comparison.
- The original TetR deep-mutational-scanning paper (eLife 11:e79932, 2022) was not retrieved by the
  recorded searches; its results are quoted second-hand from PMC12339756, which reproduces its figure
  under CC BY.
- No source was retrieved that reports a topology-only invariant, independent of degree, burial and
  distance, correlating with allosteric coupling. Per ADR 0019 this is recorded as "not retrieved by
  the recorded search", not as an absence of prior art.
