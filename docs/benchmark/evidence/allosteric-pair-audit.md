# Structural audit of the frozen pairs against the ALLOSTERIC criterion

**Question.** The frozen arms were validated against *cryptic-pocket* criteria — is the
pocket absent in the apo, does the ligand clash if transplanted. That lens is silent on
the two things allostery actually is: **coupling between two sites** and **transition
between functional states**. This document re-audits every frozen arm on the axes
crypticity does not measure.

**Date:** 2026-08-20. **Sources:** RCSB `data.rcsb.org/rest/v1/core/entry/{id}` (retrieved
this session) and the deposited mmCIF files in `data/raw/`. Frozen values read from
`docs/benchmark/manifest.yaml` and `docs/benchmark/frozen.json`; nothing restated from
memory.

**Tags.** `[DERIVED]` — computed from coordinates this session by the script in §7.
`[RETRIEVED]` — read from an RCSB entry record this session. Nothing else is asserted.

This is evaluation-side evidence and is never imported by prediction code.

---

## 0. Headline

The reproduction script now enumerates `sorted(frozen)` and this re-run covers all **11
scoreable arms**, including the trimmed ABL1 arm and both myosin sites.

**No arm supplies an isolated structural comparison from which an active-site response can
be attributed to the allosteric ligand.** In seven arms the active site is more rigid than
the rest of the chain (one-sided Mann–Whitney p = 1.0). Three ABL1 arms pass the predeclared
active-site-motion rule, but each also changes its ATP-site occupant; the remaining ABL1
sensitivity arm moves chain-wide. The available structures therefore do not identify which
ligand, construct difference or conformational selection produced an observed displacement.

The consequence for the project is stated in §6.2, and it is not "the pairs are bad". It is
that **the benchmark's ground truth is a binding-site label set, not a coupling label set**,
and no arm can by itself establish that a propagation method recovered *coupling* rather
than *a pocket*.

---

## 1. Axis 1 — functional / conformational state

### 1.1 What the depositors say `[RETRIEVED]`

| Entry | `_struct.title` | Keywords | Method / res. | Primary citation (RCSB record) |
|---|---|---|---|---|
| 4OBE | Crystal Structure of GDP-bound Human KRas | Small GTPase, GDP binding | X-ray 1.24 Å | *In situ selectivity profiling and crystal structure of SML-8-73-1…*, PNAS 2014 |
| 4LDJ | Crystal Structure of a GDP-bound G12C Oncogenic Mutant of Human GTPase KRas | GDP bound, oncogenic mutation | X-ray 1.15 Å | same study as 4OBE |
| 6OIM | Crystal Structure of human KRAS G12C covalently bound to AMG 510 | Inhibitor, GTPase | X-ray 1.65 Å | *The clinical KRAS(G12C) inhibitor AMG 510…*, Nature 2019 |
| 1OPL | Structural basis for the auto-inhibition of c-Abl tyrosine kinase | TRANSFERASE | X-ray 3.42 Å | Cell 2003 |
| 2G2H | A Src-like Inactive Conformation in the Abl Tyrosine Kinase Domain | Protein Kinase | X-ray 2.00 Å | PLoS Biol 2006 |
| 2G1T | A Src-like Inactive Conformation in the Abl Tyrosine Kinase Domain | Kinase | X-ray 1.80 Å | PLoS Biol 2006 |
| 5MO4 | ABL1 kinase (T334I_D382N) in complex with asciminib and nilotinib | Kinase, drug, inhibitor | X-ray 2.17 Å | *The allosteric inhibitor ABL001 enables dual targeting of BCR-ABL1*, Nature 2017 |
| 9GZ3 | Beta-cardiac heavy meromyosin motor domain **in the primed state** | Mavacamten, Primed myosin | cryo-EM 3.4 Å | *Mavacamten inhibits myosin activity by stabilising the myosin interacting-heads motif and stalling motor force generation* |
| 9GZ2 | …**primed state** complexed to mavacamten | Mavacamten, Primed myosin | cryo-EM 2.9 Å | same study |
| 8QYP | Beta-cardiac myosin motor domain **in the pre-powerstroke state** | cardiac myosin modulators | X-ray 2.76 Å | *Omecamtiv mecarbil and Mavacamten target the same myosin pocket…* |
| 8QYR | …**pre-powerstroke state** complexed to Mavacamten | mavacamten | X-ray 1.80 Å | same study |
| 8QYU | …**pre-powerstroke state** complexed to omecamtiv mecarbil | cardiac myosin modulators | X-ray 1.96 Å | same study |
| 9F6C | Cardiac myosin motor domain **in the pre-powerstroke state** co-crystallized with aficamten | cardiac myosin, modulator | X-ray 2.33 Å | Hartman et al., *Nat Cardiovasc Res* 2024, doi 10.1038/s44161-024-00505-0 |
| 9YRG | Cryo-EM structure of human beta-cardiac myosin **in the interacting-heads motif and S2-FH undocked state** | IHM, Actin Binding | cryo-EM 3.2 Å | *Cryo-EM reveals how cardiomyopathy therapeutic drugs modulate the myosin motors of the heart*, Sci Adv 2026 |
| 9YR7 | …**bound to mavacamten in the interacting-heads motif and S2-FH undocked state** | IHM, Mavacamten | cryo-EM 3.0 Å | same study |

RCSB's citation record for 9GZ3/9GZ2 still points at the bioRxiv preprint; the manifest
records the peer-reviewed version (Sci Adv 2026, doi 10.1126/sciadv.aea9335). Both refer to
the same study. The RCSB record is what was retrieved this session.

### 1.2 Kinase state, derived rather than read off the title `[DERIVED]`

Dunbrack's spatial DFG classification (Modi & Dunbrack, PNAS 2019,
doi [10.1073/pnas.1814279116](https://doi.org/10.1073/pnas.1814279116)): D1 = αC-Glu(+4) Cα
to DFG-Phe Cζ, D2 = β3-Lys Cα to DFG-Phe Cζ; DFG-in iff D1 ≤ 11 and D2 ≥ 11, DFG-out iff
D1 > 11 and D2 < 11. αC-in/out from the β3-Lys NZ ··· αC-Glu carboxylate salt bridge.
Motifs located by the repo's own `CATALYTIC_MOTIFS` regexes, so the numbering convention
comes out of the file rather than being assumed.

| Entry | β3-Lys | DFG | αC-Glu | K···E (Å) | αC | D1 | D2 | DFG class |
|---|---|---|---|---|---|---|---|---|
| 1OPL:A | K290 | D400-F401-G402 | E305 | 2.94 | **in** | 12.81 | 11.67 | inter |
| 2G2H:A | K290 | D400-F401-G402 | E305 | 8.47 | **out** | 10.34 | 7.76 | inter |
| 2G1T:A | K271 | D381-F382-G383 | E286 | 14.45 | **out** | 5.49 | 13.36 | **in** |
| 5MO4:A | K290 | D400-F401-(G402 unmodelled) | E305 | 2.80 | **in** | 13.95 | 11.32 | inter (borderline out) |

Two facts fall out that the titles do not give:

- **1OPL and 2G1T use different numbering conventions** (ABL1b vs ABL1a, +19), confirmed
  from the motif positions, not assumed.
- **5MO4's activation loop 402–419 is unmodelled**, so its DFG-Gly is absent and the regex
  finds no DFG; D400/F401 are present and were anchored on HRD+20. Any claim about
  A-loop response in the ABL arms is unmeasurable on this holo.
- 1OPL at 3.42 Å has side-chain positions of limited reliability; its D1/D2 are the least
  trustworthy row.

### 1.3 Does each pair span a transition?

| Arm | Apo state | Holo state | Spans a functional-state transition? |
|---|---|---|---|
| `kras_g12c_mandated` | GDP·Mg, **off** state | GDP·Mg, **off** state + sotorasib | **No.** Both members are GDP-bound. The drug traps the state the apo is already in. What the pair does span is a *local* switch-II remodelling (§1.4). |
| `kras_g12c_corrected` | GDP·Mg, off | GDP·Mg, off + sotorasib | **No**, same as above. |
| `bcr_abl1_mandated` | Autoinhibited **assembled** SH3-SH2-KD, myristate bound, αC-in | Kinase domain **alone**, αC-in | **No** — and not comparable: the apo carries SH3+SH2 (451 modelled residues) that the holo does not have (429, starting at 83 but kinase-domain-centred). The assembly axis the myristoyl pocket controls is present in only one member. |
| `bcr_abl1_corrected` | Src-like inactive KD, **αC-out**, myristoyl pocket empty | **αC-in**, DFG borderline-out | **Yes**, αC-out → αC-in. But the ATP-site ligand also changes, so the structures cannot identify the cause (§4.3). |
| `bcr_abl1_sensitivity` | Src-like inactive KD, **αC-out**, **DFG-in** | αC-in, DFG borderline-out | **Yes**, largest of the three (chain RMSD 3.30 Å core-frame). Same confound, worse. |
| `bcr_abl1_trimmed` | The 1OPL kinase-domain range, myristate bound, αC-in | Kinase domain, αC-in | **No.** This scope sensitivity preserves the same P16→NIL comparison as the mandated arm while removing SH3–SH2 nodes **and the C-terminal 513–531, which carries 3 of the 20 labels**. |
| `cardiac_myosin_site1_corrected` | Primed (pre-powerstroke), ADP·Mg·Pi, single motor domain | Primed, ADP·Mg·Pi, + mavacamten | **No.** Same state by title, same nucleotide, same construct. |
| `cardiac_myosin_site1_sensitivity_xray` | Pre-powerstroke, **ADP·VO₄** | Pre-powerstroke, **ADP·BeF₃** | **No** state transition claimed; but the **nucleotide analogue differs**, so the pair is not drug-only (§2). |
| `cardiac_myosin_site1_sensitivity_srx` | IHM + S2-FH undocked, ADP·Pi, 6 chains | **Same** IHM + S2-FH undocked, ADP·Pi, + mavacamten | **No.** The apo already occupies the assembly state mavacamten stabilises. |
| `cardiac_myosin_site1_omecamtiv` | Pre-powerstroke, ADP·Mg·VO₄ | Pre-powerstroke, ADP·Mg·VO₄, + omecamtiv | **No.** Catalytic state is matched; DMS is an additive (§2). |
| `cardiac_myosin_site2_corrected` | Pre-powerstroke, ADP·Mg·VO₄ | Pre-powerstroke, ADP·Mg·VO₄, + aficamten | **No.** Catalytic state is matched; the effector contact is classified separately (§2). |

### 1.4 Where the KRAS change actually is `[DERIVED]`

Per-region median Cα deviation, apo → 6OIM, outlier-rejected frame:

| Region | 4OBE → 6OIM | 4LDJ → 6OIM |
|---|---|---|
| P-loop 10–17 | 0.14 | 0.17 |
| **switch I 30–38** | **0.33** | **0.56** |
| **switch II 60–76** | **3.20** (max 8.51 at E63) | **2.79** (max 8.46 at E63) |
| α3 87–104 | 0.80 | 0.57 |
| NKxD 116–119 | 0.18 | 0.18 |
| SAK 145–147 | 0.25 | 0.18 |

Switch II opens; switch I, the P-loop and the guanine-recognition motifs do not move. The
KRAS pairs span a **pocket-opening event confined to switch II**, not a nucleotide-state or
switch-I transition.

### 1.5 Where the myosin change actually is `[DERIVED]`

Per-subdomain median Cα deviation, outlier-rejected frame:

| Region | 9GZ3→9GZ2 | 8QYP→8QYR | 9YRG→9YR7 | 8QYP→8QYU | 8QYP→9F6C |
|---|---|---|---|---|---|
| N-term 4–215 | 0.39 | 0.56 | 0.25 | 0.52 | 0.29 |
| P-loop 179–186 | 0.26 | 0.28 | 0.14 | 0.17 | 0.21 |
| switch I 233–247 | 0.29 | 0.21 | 0.31 | 0.21 | 0.21 |
| switch II 454–466 | 0.40 | 0.36 | 0.23 | 0.24 | 0.22 |
| relay 466–498 | 0.30 | 0.22 | 0.21 | 0.28 | 0.35 |
| SH1 690–710 | 0.30 | 0.30 | 0.19 | 0.54 | 0.21 |
| **converter 711–781** | **2.02** (max 4.34) | **3.51** (max 11.04) | **0.58** (max 3.55) | **3.76** (max 5.55) | **1.56** (max 8.69) |
| **lever 782–843** | **6.10** (max 7.34) | not modelled | **1.23** (max 3.84) | not modelled | not modelled |
| Site 1 N-term segment 164–177 | 0.32 | 0.38 | 0.25 | 0.27 | 0.38 |

The whole apo→holo signal in the myosin arms is a **converter/lever displacement**. The
ATPase machinery — P-loop, switch I, switch II, relay — is unchanged at 0.14–0.40 Å, at or
below cryo-EM/X-ray coordinate precision for these resolutions. Note the mavacamten site
itself splits across two regions: 164–177 (N-terminal subdomain, unmoved) and 710–774
(converter, moved), so "the drug site responds" in these arms is largely a statement about
the converter.

---

## 2. Axis 2 — orthosteric site state

Derived by mapping the frozen `active_site` (apo numbering) onto the holo through the
sequence alignment, then listing every non-water heteroatom component within 4.5 Å of those
residues — **entry-wide, not chain-scoped**, which is what catches 2G1T. Match status compares
only the manifest's catalytic `state_components`; crystallisation `additives` and the named
allosteric effector are recorded separately and cannot flip the classification. `[DERIVED]`

| Arm | Apo orthosteric occupancy | Holo orthosteric occupancy | Matched? |
|---|---|---|---|
| `kras_g12c_mandated` | GDP (2.78 Å), MG (2.09 Å) | GDP (2.72), MG (2.16), **MOV (1.81)** | **Nucleotide matched.** But the allosteric ligand itself reaches the active site — see below. |
| `kras_g12c_corrected` | GDP (2.70), MG (2.11) | GDP (2.72), MG (2.16), **MOV (1.81)** | same |
| `bcr_abl1_mandated` | **P16** (PD166326, 3.49 Å) | **NIL** (nilotinib, 3.01 Å) | **NO — different ATP-site inhibitor** |
| `bcr_abl1_corrected` | **P16** (3.27 Å) | **NIL** (3.01 Å) | **NO — different ATP-site inhibitor** |
| `bcr_abl1_sensitivity` | **112** (ATP-peptide bisubstrate conjugate on chains E–H, 2.74 Å), MG (2.03 Å) | **NIL** (3.01 Å) | **NO — worst mismatch in the set.** The apo's occupant spans the ATP site *and* the peptide-substrate groove; the holo's is a type-II inhibitor. |
| `bcr_abl1_trimmed` | **P16** (3.49 Å) | **NIL** (3.01 Å) | **NO — same mismatch as the mandated arm** |
| `cardiac_myosin_site1_corrected` | ADP (2.29), MG (2.09), PO4 (2.43) | ADP (2.34), MG (2.07), PO4 (2.61) | **YES — exact.** |
| `cardiac_myosin_site1_sensitivity_xray` | ADP (2.73), MG (2.02), **VO4** (2.43) | ADP (2.74), MG (1.95), **BEF** (2.60); additive SO4 (3.63) | **NO — γ-phosphate analogue differs.** Sulfate is recorded but does not decide the state. |
| `cardiac_myosin_site1_sensitivity_srx` | ADP (2.35), PO4 (2.18) | ADP (2.38), PO4 (2.51) | **YES — exact** (no Mg modelled in either). |
| `cardiac_myosin_site1_omecamtiv` | ADP (2.73), MG (2.02), VO4 (2.43) | ADP (2.79), MG (1.95), VO4 (2.73); additive DMS (3.25) | **YES.** DMS is not a catalytic ligand. |
| `cardiac_myosin_site2_corrected` | ADP (2.73), MG (2.02), VO4 (2.43) | ADP (2.75), MG (1.93), VO4 (2.71); effector 6I6 (3.27) | **YES.** Effector contact is recorded separately. |

The four ABL1 arms and the myosin x-ray sensitivity arm do not isolate the allosteric
ligand: their catalytic state components differ. The ABL1 cross-structure comparison in
§4.3 is descriptive and does not repair that identification problem.

**The KRAS finding that matters more than the nucleotide match.** `[DERIVED]` The closest
MOV–protein contact in 6OIM is **C25(MOV) ··· SG(CYS12) at 1.81 Å** — a covalent bond.
Cys12 is itself an active-site residue by the frozen `{from_ligands: [GDP, MG]}` rule
(its heavy atoms lie within 4.5 Å of GDP/Mg). Sotorasib is therefore covalently anchored
to a residue of the nucleotide site. In the mandated arm the anchor residue does not even
exist in the apo (4OBE is wild-type Gly12).

---

## 3. Axis 3 — coupling geometry

Computed on the **apo**, since that is the blind-prediction input. Distances are
heavy-atom minima between the frozen `scoreable_label_residues` (the allosteric positives; the
key was renamed from `distal_label_residues` by ADR 0007 and the script below follows the
current name) and
the frozen `active_site`. The contact graph is residue-level with an edge whenever any
heavy-atom pair is within the frozen 4.5 Å cutoff; "hops" is the BFS edge count. `[DERIVED]`

| Arm | min (Å) | mean over all site-pairs (Å) | mean nearest-per-label (Å) | shortest path (hops) | median hops per label | shared residues (labels ∩ active) |
|---|---|---|---|---|---|---|
| `kras_g12c_mandated` | **1.32** | 16.08 | 7.79 | **1** | 2.0 | **{11, 12, 13, 16, 34}** |
| `kras_g12c_corrected` | **1.31** | 15.93 | 7.81 | **1** | 2.0 | **{11, 12, 13, 16, 34}** |
| `bcr_abl1_mandated` | 7.66 | 24.29 | 15.45 | 2 | 3.0 | ∅ |
| `bcr_abl1_corrected` | 7.85 | 23.64 | 14.87 | 2 | 3.0 | ∅ |
| `bcr_abl1_sensitivity` | 7.78 | 22.98 | 14.91 | 2 | 3.0 | ∅ |
| `bcr_abl1_trimmed` | 7.66 | 23.16 | 14.27 | 2 | 3.0 | ∅ |
| `cardiac_myosin_site1_corrected` | **13.70** | 30.08 | 23.81 | **4** | **6.0** | ∅ |
| `cardiac_myosin_site1_omecamtiv` | 9.64 | 27.58 | 18.39 | 3 | 4.0 | ∅ |
| `cardiac_myosin_site1_sensitivity_srx` | **14.65** | 28.81 | 20.37 | **4** | 4.5 | ∅ |
| `cardiac_myosin_site1_sensitivity_xray` | 11.81 | 28.10 | 19.28 | 3 | 4.0 | ∅ |
| `cardiac_myosin_site2_corrected` | **1.33** | 16.30 | 5.98 | **1** | 2.0 | **{242, 243, 463}** |

The same heavy-atom minima computed on the **holo** agree with the apo values to within
0.25 Å in every arm (largest gap: 11.56 vs 11.81 Å,
`cardiac_myosin_site1_sensitivity_xray`), so
the two sites neither approach nor separate on ligand binding. Hop counts were computed on
the apo only.

**The KRAS arms and myosin Site 2 are proximal tasks.** Their full label sets overlap the
active site, and their scoreable labels remain one contact-graph hop from it, with 1.31–1.33
Å heavy-atom minima. A method propagating from the active site can rank these residues by
locality alone. The ABL1 arms and myosin Site 1 provide the separated cases.

---

## 4. Axis 4 — local vs global response (the decisive axis)

### 4.1 Method

Apo and holo Cα atoms paired **through the sequence alignment**, never by author number
(`allo.groundtruth.labels.align_numbering`), then superposed by Kabsch in two frames:

- **global** — fitted on all paired Cα. Neutral, but a large domain motion (a myosin lever)
  is spread over the whole chain.
- **core** — iterative 2σ outlier rejection (floor: 50 % of pairs retained), converging on
  the rigid core. This is the frame in which "did region X move relative to the body of the
  protein" is a meaningful question.

Both are reported; **every conclusion below is the same in both frames.**

The null is the rest of the chain: all paired residues that are neither a label nor an
active-site residue. `p_vs_rest` is a one-sided Mann-Whitney U (alternative: the set's
deviations are stochastically greater than the rest's). Decision rule stated in advance:
an arm shows an active-site response iff **median active-site deviation > 0.5 Å**
(a conservative coordinate-precision floor for 1.2–3.4 Å structures) **and p_vs_rest < 0.05**.

### 4.2 Results `[DERIVED]`

Median Cα deviation in Å; `p` is `p_vs_rest`.

| Arm | frame | n paired | chain RMSD | **scoreable labels** | p | **active site** | p | rest (null) |
|---|---|---|---|---|---|---|---|---|
| `kras_g12c_mandated` | global | 166 | 1.36 | 1.19 | 0.0046 | 0.43 | 1.0 | 0.66 |
| | core | | 1.53 | **1.53** | **0.010** | **0.23** | **1.0** | 0.48 |
| `kras_g12c_corrected` | global | 167 | 1.34 | 1.03 | 8.4e-05 | 0.29 | 1.0 | 0.48 |
| | core | | 1.38 | **1.21** | **0.00019** | **0.26** | **1.0** | 0.43 |
| `bcr_abl1_mandated` | global | 429 | 0.98 | 0.37 | 1.0 | 0.71 | 0.031 | 0.56 |
| | core | | 1.10 | **0.37** | **0.78** | **1.35** | **0.017** | 0.41 |
| `bcr_abl1_corrected` | global | 252 | 1.78 | 0.64 | 0.86 | 0.93 | 0.11 | 0.87 |
| | core | | 2.01 | **0.48** | **0.61** | **0.90** | **0.025** | 0.50 |
| `bcr_abl1_sensitivity` | global | 251 | 2.54 | 0.64 | 1.0 | 1.65 | 0.35 | 1.60 |
| | core | | 3.30 | **0.47** | **0.46** | **1.58** | **0.34** | 0.50 |
| `bcr_abl1_trimmed` | global | 232 | 1.01 | 0.23 | 1.0 | 0.61 | 0.10 | 0.48 |
| | core | | 1.12 | **0.24** | **0.96** | **0.72** | **0.012** | 0.29 |
| `cardiac_myosin_site1_corrected` | global | 764 | 1.18 | 0.79 | 0.0019 | 0.29 | 1.0 | 0.59 |
| | core | | 1.26 | **0.74** | **0.036** | **0.29** | **1.0** | 0.43 |
| `cardiac_myosin_site1_omecamtiv` | global | 699 | 1.15 | 1.71 | 2.7e-08 | 0.33 | 1.0 | 0.65 |
| | core | | 1.34 | **1.47** | **8.3e-05** | **0.21** | **1.0** | 0.42 |
| `cardiac_myosin_site1_sensitivity_srx` | global | 912 | 0.88 | 0.40 | 0.23 | 0.28 | 1.0 | 0.36 |
| | core | | 0.90 | **0.39** | **0.076** | **0.18** | **1.0** | 0.31 |
| `cardiac_myosin_site1_sensitivity_xray` | global | 700 | 1.23 | 1.03 | 0.00013 | 0.45 | 1.0 | 0.59 |
| | core | | 1.34 | **0.98** | **0.00046** | **0.26** | **1.0** | 0.43 |
| `cardiac_myosin_site2_corrected` | global | 705 | 1.00 | 0.44 | 0.23 | 0.19 | 1.0 | 0.41 |
| | core | | 1.04 | **0.42** | **0.037** | **0.21** | **1.0** | 0.33 |

Applying the rule:

| Arm | allosteric site responds? | **active site responds?** |
|---|---|---|
| `kras_g12c_mandated` | **yes** (1.53 Å, p = 0.010) | **no** (0.23 Å, p = 1.0 — *less* than the null) |
| `kras_g12c_corrected` | **yes** (1.21 Å, p = 0.00019) | **no** (0.26 Å, p = 1.0) |
| `bcr_abl1_mandated` | **no** (0.37 Å, p = 0.78) | yes by the rule (1.35 Å, p = 0.017) — **but see §4.3** |
| `bcr_abl1_corrected` | **one residue only** (median 0.48 Å; I521 = 10.25 Å) | yes by the rule (0.90 Å, p = 0.025) — **but see §4.3** |
| `bcr_abl1_sensitivity` | **one residue only** (median 0.47 Å; I502 = 9.44 Å) | **no** (1.58 Å but p = 0.34: the whole chain moves by that much) |
| `bcr_abl1_trimmed` | **no** (0.24 Å, p = 0.96) | yes by the rule (0.72 Å, p = 0.012) — **but see §4.3** |
| `cardiac_myosin_site1_corrected` | **yes** (0.74 Å, p = 0.036) | **no** (0.29 Å, p = 1.0) |
| `cardiac_myosin_site1_omecamtiv` | **yes** (1.47 Å, p = 8.3e-05) | **no** (0.21 Å, p = 1.0) |
| `cardiac_myosin_site1_sensitivity_srx` | **no** (0.39 Å, p = 0.076) | **no** (0.18 Å, p = 1.0) |
| `cardiac_myosin_site1_sensitivity_xray` | **yes** (0.98 Å, p = 0.00046) | **no** (0.26 Å, p = 1.0) |
| `cardiac_myosin_site2_corrected` | **no by magnitude** (0.42 Å, p = 0.037) | **no** (0.21 Å, p = 1.0) |

### 4.3 The BCR-ABL1 cross-structure comparison `[DERIVED]`

The ABL1 arms share one holo (`5MO4`) but their apo structures differ simultaneously in
construct extent, mutations, conformation and occupancy at both sites. This is **not a
controlled comparison**: no structure changes only the ATP-site ligand or only the
myristoyl-site ligand while holding the rest fixed. The comparison below records
co-variation and cannot identify which difference produced a displacement. The trimmed arm
uses the 1OPL coordinates over a smaller node range, so it adds scope sensitivity rather
than an independent structure.

| Apo | myristoyl pocket | ATP site | vs 5MO4 (asciminib + nilotinib) |
|---|---|---|---|
| 1OPL | **occupied** (MYR, 3.29 Å) | P16 | pocket occupancy *same*, ATP ligand *differs* |
| 2G2H | **empty** | P16 | pocket occupancy *differs*, ATP ligand *differs* |
| 2G1T | **empty** | bisubstrate `112` | pocket occupancy *differs*, ATP ligand *differs* |

Per-residue Cα deviation, core frame, along the C-terminal helix that lines the myristoyl
pocket (ABL1b numbering; 2G1T shown in its own ABL1a numbering, −19):

| Residue (1b) | 1OPL→5MO4 | 2G2H→5MO4 | 2G1T→5MO4 |
|---|---|---|---|
| I508 / I489 | 0.31 | 0.31 | 0.29 |
| F512 / F493 | 0.56 | 1.08 | 0.97 |
| E513 / E494 | 0.79 | 2.00 | 1.78 |
| M515 / M496 | 0.63 | 3.02 | 2.97 |
| F516 / F497 | 0.49 | **6.16** | **6.14** |
| S519 / S500 | 1.34 | **5.36** | **5.39** |
| **I521 / I502** | **0.39** | **10.25** | **9.44** |
| S522 / S501 (2G1T ends at 502) | 0.53 | 8.57 | — |
| D523 | 0.44 | 10.43 | — |

**Reading.** The M515 hinge and following helix differ most for the 2G2H and 2G1T
comparisons, while 1OPL differs less. That pattern is consistent with myristoyl-site
occupancy mattering, but the correlated construct and conformational differences prevent
attribution. AY7 contacts the same helix face in 5MO4, which establishes spatial relevance,
not identification of an effect.

The active-site regions show another descriptive pattern:

| Region | 1OPL→5MO4 | 2G2H→5MO4 | 2G1T→5MO4 |
|---|---|---|---|
| P-loop | 3.22 | 2.37 | 4.47 |
| αC helix | 1.11 | 1.27 | 4.37 |
| catalytic loop HRD | 0.29 | 0.48 | 0.28 |
| DFG-Asp | 4.20 | 4.12 | 1.08 |
| **DFG-Phe** | **5.70** | **5.48** | **7.91** |

The DFG-Phe differs by 5–8 Å in all three structure comparisons, including 1OPL where both
members occupy the myristoyl pocket. Because every comparison also changes the ATP-site
ligand and other structural factors, the §4.2 active-site motion is **confounded and
unattributable**. These coordinates cannot distinguish an ATP-ligand effect from asciminib,
construct or state selection.

### 4.4 Caveats on this axis

- A crystal or cryo-EM structure is one conformer. **Absence of a mean-structure change at
  the active site does not disprove allostery** — a purely entropic/dynamic allosteric
  effect, or a population shift between assemblies, moves no mean coordinate. The
  depositors' own titles say so: mavacamten's stated mechanism is *stabilising the
  interacting-heads motif*, i.e. a population shift, and asciminib's is stabilising the
  assembled autoinhibited state.
- What these numbers do establish is narrower and still decisive for us: **no arm can serve
  as structural evidence that the allosteric ligand perturbs the active site**, so no arm can
  validate a coupling claim by apo/holo comparison.
- 5MO4's activation loop (402–419) is unmodelled, so A-loop response in the ABL arms is
  unmeasurable, not absent.
- The 9YRG→9YR7 "rest" distribution has one 16.4 Å outlier at residue 202; medians are
  used throughout for this reason.

---

## 5. Axis 5 — arm-by-arm audit summary

This is a descriptor table, not a ranking. "Site response" and "active response" apply the
§4.1 magnitude-plus-Mann–Whitney rule; they do not assign a cause.

| Arm | Site-apo? | Catalytic state | separation | site response | active response | Main limitation |
|---|---|---|---|---|---|---|
| `kras_g12c_mandated` | yes | matched | 1.32 Å / 1 hop | yes, 1.53 Å (p=0.010) | no | wrong genotype; proximal and covalently anchored at Cys12 |
| `kras_g12c_corrected` | yes | matched | 1.31 Å / 1 hop | yes, 1.21 Å (p=0.00019) | no | proximal and covalently anchored at Cys12 |
| `bcr_abl1_mandated` | **no** | P16→NIL | 7.66 Å / 2 hops | no | yes, **confounded** | target pocket already contains myristate |
| `bcr_abl1_corrected` | yes | P16→NIL | 7.85 Å / 2 hops | no by magnitude | yes, **confounded** | catalytic occupant and conformation both change |
| `bcr_abl1_sensitivity` | yes | 112+MG→NIL | 7.78 Å / 2 hops | no by magnitude | no | chain-wide motion; catalytic occupant changes |
| `bcr_abl1_trimmed` | **no** | P16→NIL | 7.66 Å / 2 hops | no | yes, **confounded** | strict scope, but same occupied 1OPL pocket |
| `cardiac_myosin_site1_corrected` | yes | matched | 13.70 Å / 4 hops | yes, 0.74 Å (p=0.036) | no | no mean-coordinate active-site response |
| `cardiac_myosin_site1_omecamtiv` | yes | matched; DMS additive | 9.64 Å / 3 hops | yes, 1.47 Å (p=8.3e-05) | no | no mean-coordinate active-site response |
| `cardiac_myosin_site1_sensitivity_srx` | yes | matched | 14.65 Å / 4 hops | no | no | apo already occupies the IHM state |
| `cardiac_myosin_site1_sensitivity_xray` | yes | VO4→BEF; SO4 additive | 11.81 Å / 3 hops | yes, 0.98 Å (p=0.00046) | no | phosphate analogue changes |
| `cardiac_myosin_site2_corrected` | yes | matched; 6I6 separate | 1.33 Å / 1 hop | no by magnitude | no | proximal; labels overlap the active site |

No row provides an isolated structural estimate of an allosteric-ligand effect at the active
site. The three rows that pass the active-response rule are ABL1 comparisons with unmatched
catalytic occupants and other correlated differences.

---

## 6. What follows

### 6.1 For the freeze

Nothing here requires the manifest to change, and this document changes nothing. Two facts
are new relative to the cryptic-lens audit and belong in the record if the freeze is ever
revisited:

1. **The KRAS arms and myosin Site 2 are proximal.** Their full labels overlap the active
   site and their scoreable labels remain one contact hop away. This is a descriptor, not an
   exclusion criterion, but it means a locality score is a mandatory baseline.
2. **`cardiac_myosin_site1_sensitivity_srx` is a matched pair with no transition.** Its virtue
   (identical construct, state, nucleotide) and its defect (apo and holo are the same
   structure to 0.90 Å) are the same fact. It is the allosteric analogue of a non-cryptic
   pocket, and its numbers should be read as a **negative control on transition**, not as an
   independent replication of the corrected arm.

### 6.2 For the method — the decision-relevant point

The frozen ground truth is **where the drug binds**, derived from holo-ligand contacts. It
is not **which residues are dynamically coupled to the active site**. Scoreable-site labels
pass the structural-response rule in five arms. The active-site rule passes in three ABL1
arms, but all three comparisons are confounded; none isolates an allosteric-ligand effect.

That does not falsify the elastic-network hypothesis (C6) — a connectivity or quantum-walk
method measures *fluctuation coupling in the apo*, which can be large where the mean
structure does not shift, and every mechanism in §1 is a population shift rather than a
mean-coordinate shift. What it does mean is:

- A high score on this benchmark demonstrates **pocket identification**, not **coupling
  recovery**. The report must not claim the latter from the former.
- Any claim that the method "found the allosteric site because it is coupled to the active
  site" needs evidence the benchmark cannot supply. If that claim is to be made, it needs a
  separate endpoint — e.g. published mutational coupling data, or a stated prediction that
  fails on a decoy site equally distant from the source.
- The four myosin Site 1 arms and four ABL1 arms provide the separated cases (3–4 and 2
  hops). Reporting the KRAS and myosin Site 2 arms without hop-count context will overstate
  performance.

---

## 7. Reproduction

Every `[DERIVED]` number in §2, §3 and §4.2 regenerates from the script below; the §1.2,
§1.4, §1.5 and §4.3 tables come from the same primitives with different residue ranges.
Inputs are the frozen manifest, `frozen.json` and the deposited mmCIFs — no holo information
enters any apo-side quantity, and this file is evidence, never imported by prediction code
(C1).

The exact re-run command used from the repo root was:

```text
awk '/^```python/{flag=1;next}/^```$/{if(flag){exit}}flag' docs/benchmark/evidence/allosteric-pair-audit.md | UV_CACHE_DIR=/tmp/allo-uv-cache uv run python -
```

It imports one private helper (`allo.benchmark._chain_ca`). The arm list is derived as
`ARMS = sorted(frozen)`, so adding or removing a frozen arm changes both the run and the
coverage regression test. The tables in §2, §3 and §4.2 above are the output of the current
11-arm re-run, not retained results from the pre-ADR-0008 script.

```python
"""Regenerates the derived numbers in docs/benchmark/evidence/allosteric-pair-audit.md."""

from __future__ import annotations

import json
from collections import deque
from pathlib import Path

import numpy as np
from scipy.stats import mannwhitneyu

from allo.benchmark import FROZEN, _chain_ca
from allo.groundtruth.labels import align_numbering
from allo.groundtruth.manifest import read_manifest as load  # evaluation side: needs `holo`
from allo.inputs import RAW
from allo.groundtruth.structures import fetch_mmcif
from allo.structure.pdb import parse_mmcif

CUT = 4.5
_seen: dict[str, object] = {}


def S(pdb):
    if pdb not in _seen:
        _seen[pdb] = parse_mmcif(fetch_mmcif(pdb, RAW), pdb)
    return _seen[pdb]


def res_atoms(st, chain, keep=None):
    """{author seq id: heavy-atom row indices} for polymer residues of `chain`."""
    idx = np.where(st.protein & (st.chain == chain))[0]
    out: dict[int, list[int]] = {}
    for i in idx:
        out.setdefault(int(st.seq_id[i]), []).append(i)
    return {n: np.array(v) for n, v in out.items() if keep is None or n in keep}


def site_distance(st, chain, setA, setB):
    """Heavy-atom distances between two residue sets of one chain."""
    ai, bi = res_atoms(st, chain, set(setA)), res_atoms(st, chain, set(setB))
    per_res = {}
    for ka, ia in ai.items():
        per_res[ka] = min(
            float(
                np.linalg.norm(st.coord[ia][:, None, :] - st.coord[ib][None, :, :], axis=-1).min()
            )
            for ib in bi.values()
        )
    allpairs = [
        float(np.linalg.norm(st.coord[ia][:, None, :] - st.coord[ib][None, :, :], axis=-1).min())
        for ia in ai.values()
        for ib in bi.values()
    ]
    return {
        "min": round(min(allpairs), 2),
        "mean_over_pairs": round(float(np.mean(allpairs)), 2),
        "mean_nearest": round(float(np.mean(list(per_res.values()))), 2),
        "max_nearest": round(max(per_res.values()), 2),
    }


def contact_graph(st, chain, keep=None, cutoff=CUT):
    """Residue graph: edge when any heavy-atom pair is within `cutoff`."""
    ri = res_atoms(st, chain, keep)
    keys = sorted(ri)
    cen = np.array([st.coord[ri[k]].mean(0) for k in keys])
    rad = np.array(
        [np.linalg.norm(st.coord[ri[k]] - cen[i], axis=1).max() for i, k in enumerate(keys)]
    )
    D = np.linalg.norm(cen[:, None, :] - cen[None, :, :], axis=-1)
    adj = {k: set() for k in keys}
    for i in range(len(keys)):
        for j in np.where(D[i] <= rad[i] + rad + cutoff)[0]:
            if j <= i:
                continue
            a, b = ri[keys[i]], ri[keys[j]]
            if (
                np.linalg.norm(st.coord[a][:, None, :] - st.coord[b][None, :, :], axis=-1).min()
                <= cutoff
            ):
                adj[keys[i]].add(keys[j])
                adj[keys[j]].add(keys[i])
    return adj


def hops(adj, src, dst):
    """BFS hop count from any residue in `src` to the nearest residue in `dst`."""
    dst = set(dst) & set(adj)
    seen = {s: 0 for s in set(src) & set(adj)}
    q = deque(seen)
    while q:
        u = q.popleft()
        if u in dst:
            return seen[u]
        for v in adj[u]:
            if v not in seen:
                seen[v] = seen[u] + 1
                q.append(v)
    return None


def deviation(apo_id, apo_ch, holo_id, holo_ch, keep):
    """Per-residue CA deviation, apo numbering, in a global and an outlier-rejected frame."""
    apo, holo = S(apo_id), S(holo_id)
    aca, hca = _chain_ca(apo, apo_ch), _chain_ca(holo, holo_ch)
    h2a = align_numbering(holo, apo, holo_ch, apo_ch)
    pairs = [(h, h2a[h]) for h in sorted(hca) if h in h2a and h2a[h] in aca and h2a[h] in keep]
    P = np.array([hca[h] for h, _ in pairs])
    Q = np.array([aca[a] for _, a in pairs])
    nums = np.array([a for _, a in pairs])

    def kabsch(mask):
        p, q = P[mask], Q[mask]
        pb, qb = p.mean(0), q.mean(0)
        V, _, W = np.linalg.svd((p - pb).T @ (q - qb))
        R = V @ np.diag([1, 1, np.sign(np.linalg.det(V @ W))]) @ W
        return np.linalg.norm((P - pb) @ R + qb - Q, axis=1)

    mask = np.ones(len(P), bool)
    for _ in range(10):  # iterative 2-sigma rejection -> rigid core
        d = kabsch(mask)
        new = d <= max(d[mask].mean() + 2 * d[mask].std(), 0.5)
        if new.sum() < 0.5 * len(P):
            new = d <= np.quantile(d, 0.5)
        if (new == mask).all():
            break
        mask = new
    return nums, kabsch(np.ones(len(P), bool)), kabsch(mask), int(mask.sum())


def main():
    frozen = json.loads(Path(FROZEN).read_text())["targets"]
    ARMS = sorted(frozen)
    specs = {s["id"]: s for s in load()["targets"]}
    for arm in ARMS:
        sp, fz = specs[arm], frozen[arm]
        ac, hc = sp["apo"]["chain"], sp["holo"]["chain"]
        apo, holo = S(sp["apo"]["pdb"]), S(sp["holo"]["pdb"])
        labels, scoreable, active, nodes = (
            fz["label_residues"],
            fz["scoreable_label_residues"],
            fz["active_site"],
            set(fz["residue_ids"]),
        )
        print("=" * 78)
        print(
            f"{arm}  {sp['apo']['pdb']}:{ac} -> {sp['holo']['pdb']}:{hc}  ({sp['holo']['ligand']})"
        )

        # --- axis 2: what occupies each member's orthosteric site
        h2a = align_numbering(holo, apo, hc, ac)
        holo_active = [h for h, a in h2a.items() if a in set(active)]
        for tag, st, ch, site in (("apo ", apo, ac, active), ("holo", holo, hc, holo_active)):
            tgt = st.protein & (st.chain == ch) & np.isin(st.seq_id, site)
            lig = st.ligand
            d = np.linalg.norm(st.coord[lig][:, None, :] - st.coord[tgt][None, :, :], axis=-1).min(
                1
            )
            near = {}
            for i in np.where(d <= CUT)[0]:
                near.setdefault(str(st.resname[lig][i]), []).append(float(d[i]))
            print(
                f"  orthosteric {tag}: "
                + ", ".join(f"{k} (min {min(v):.2f} A)" for k, v in sorted(near.items()))
            )

        # --- axis 3: coupling geometry, on the apo (the blind input)
        g = site_distance(apo, ac, scoreable, active)
        adj = contact_graph(apo, ac, nodes)
        per = [hops(adj, [r], active) for r in scoreable if r in adj]
        print(
            f"  coupling: min {g['min']} A | mean-over-pairs {g['mean_over_pairs']} A | "
            f"mean-nearest {g['mean_nearest']} A | shortest path {hops(adj, scoreable, active)} hops | "
            f"median {float(np.median(per))} hops | shared residues {sorted(set(labels) & set(active))}"
        )

        # --- axis 4: local vs global response
        nums, dev_g, dev_c, ncore = deviation(sp["apo"]["pdb"], ac, sp["holo"]["pdb"], hc, nodes)
        rest = sorted(set(nums.tolist()) - set(labels) - set(active))
        for frame, dev in (("global", dev_g), ("core  ", dev_c)):
            r = dev[np.isin(nums, rest)]
            line = [
                f"  {frame} (n={len(nums)}, core-fit={ncore}, RMSD {np.sqrt((dev**2).mean()):.2f} A)"
            ]
            for name, s in (("scoreable-labels", scoreable), ("active-site", active)):
                x = dev[np.isin(nums, s)]
                p = mannwhitneyu(x, r, alternative="greater").pvalue
                line.append(f"{name} median {np.median(x):.2f} (p_vs_rest {p:.2g})")
            line.append(f"rest median {np.median(r):.2f}")
            print(" | ".join(line))


if __name__ == "__main__":
    main()
```

All required mmCIF files were present in `data/raw/` for this re-run.
