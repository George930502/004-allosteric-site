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

**Nothing outside `docs/benchmark/evidence/` was modified.** This is evidence, not a
change to the freeze.

---

## 0. Headline

> **Scope and naming, added 2026-08-20.** This audit ran on the **eight** arms frozen at the
> time and uses their then-current ids: `cardiac_myosin_corrected`,
> `cardiac_myosin_sensitivity_xray` and `cardiac_myosin_sensitivity_srx` are today's
> `cardiac_myosin_site1_*` arms (renamed by **ADR 0008**, which made a target a *site* rather
> than a protein). The two arms ADR 0008 added — `cardiac_myosin_site1_omecamtiv` and
> `cardiac_myosin_site2_corrected` — are **not** covered here. "Eight arms" below means those
> eight, not the current ten.

**No arm audited here shows an active-site conformational response that can be
attributed to the allosteric ligand.**

In six of eight arms the active site is the *most rigid* part of the chain: its median
apo→holo Cα deviation is **lower** than the rest of the protein (one-sided Mann-Whitney
p = 1.0 in every case). The two arms where the active site does move — `bcr_abl1_mandated`
and `bcr_abl1_corrected` — have a **different orthosteric inhibitor** in apo and holo, and
a three-structure internal control (§4.3) attributes that motion to the inhibitor swap, not
to asciminib.

The consequence for the project is stated in §6.2, and it is not "the pairs are bad". It is
that **the benchmark's ground truth is a binding-site label set, not a coupling label set**,
and no arm can be used as evidence that a propagation method recovered *coupling* rather
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
| `bcr_abl1_corrected` | Src-like inactive KD, **αC-out**, myristoyl pocket empty | **αC-in**, DFG borderline-out | **Yes**, αC-out → αC-in. But see §2: the ATP-site ligand also changes, and §4.3 attributes the αC/DFG motion to that change. |
| `bcr_abl1_sensitivity` | Src-like inactive KD, **αC-out**, **DFG-in** | αC-in, DFG borderline-out | **Yes**, largest of the three (chain RMSD 3.30 Å core-frame). Same confound, worse. |
| `cardiac_myosin_corrected` | Primed (pre-powerstroke), ADP·Mg·Pi, single motor domain | Primed, ADP·Mg·Pi, + mavacamten | **No.** Same state by title, same nucleotide, same construct. The pair isolates the drug — and shows the drug does not move the active site (§4). |
| `cardiac_myosin_sensitivity_xray` | Pre-powerstroke, **ADP·VO₄** | Pre-powerstroke, **ADP·BeF₃** | **No** state transition claimed; but the **nucleotide analogue differs**, so the pair is not drug-only (§2). |
| `cardiac_myosin_sensitivity_srx` | IHM + S2-FH undocked, ADP·Pi, 6 chains | **Same** IHM + S2-FH undocked, ADP·Pi, + mavacamten | **No** — and this is the strongest case of "apo already in the drug's target state". The apo *is* the interacting-heads motif that mavacamten stabilises. Chain RMSD 0.90 Å; largest label-residue deviation 0.87 Å (§4). |

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

| Region | 9GZ3→9GZ2 | 8QYP→8QYR | 9YRG→9YR7 |
|---|---|---|---|
| N-term 4–215 | 0.39 | 0.56 | 0.25 |
| P-loop 179–186 | 0.26 | 0.28 | 0.14 |
| switch I 233–247 | 0.29 | 0.21 | 0.31 |
| switch II 454–466 | 0.40 | 0.36 | 0.23 |
| relay 466–498 | 0.30 | 0.22 | 0.21 |
| SH1 690–710 | 0.30 | 0.30 | 0.19 |
| **converter 711–781** | **2.02** (max 4.34) | **3.51** (max 11.04) | **0.58** (max 3.55) |
| **lever 782–843** | **6.10** (max 7.34) | not modelled | **1.23** (max 3.84) |
| mavacamten site 164–177 | 0.32 | 0.38 | 0.25 |

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
residues — **entry-wide, not chain-scoped**, which is what catches 2G1T. `[DERIVED]`

| Arm | Apo orthosteric occupancy | Holo orthosteric occupancy | Matched? |
|---|---|---|---|
| `kras_g12c_mandated` | GDP (2.78 Å), MG (2.09 Å) | GDP (2.72), MG (2.16), **MOV (1.81)** | **Nucleotide matched.** But the allosteric ligand itself reaches the active site — see below. |
| `kras_g12c_corrected` | GDP (2.70), MG (2.11) | GDP (2.72), MG (2.16), **MOV (1.81)** | same |
| `bcr_abl1_mandated` | **P16** (PD166326, 3.49 Å) | **NIL** (nilotinib, 3.01 Å) | **NO — different ATP-site inhibitor** |
| `bcr_abl1_corrected` | **P16** (3.27 Å) | **NIL** (3.01 Å) | **NO — different ATP-site inhibitor** |
| `bcr_abl1_sensitivity` | **112** (ATP-peptide bisubstrate conjugate on chains E–H, 2.74 Å), MG (2.03 Å) | **NIL** (3.01 Å) | **NO — worst mismatch in the set.** The apo's occupant spans the ATP site *and* the peptide-substrate groove; the holo's is a type-II inhibitor. |
| `cardiac_myosin_corrected` | ADP (2.29), MG (2.09), PO4 (2.43) | ADP (2.34), MG (2.07), PO4 (2.61) | **YES — exact.** The only difference between the two entries is XB2. |
| `cardiac_myosin_sensitivity_xray` | ADP (2.73), MG (2.02), **VO4** (2.43) | ADP (2.74), MG (1.95), **BEF** (2.60), SO4 (3.63) | **NO — γ-phosphate analogue differs** (vanadate vs beryllium fluoride), plus a crystallisation sulfate in the site and EDO elsewhere. |
| `cardiac_myosin_sensitivity_srx` | ADP (2.35), PO4 (2.18) | ADP (2.38), PO4 (2.51) | **YES — exact** (no Mg modelled in either). |

**Three arms cannot attribute any structural difference to the allosteric ligand**
(`bcr_abl1_mandated`, `bcr_abl1_corrected`, `bcr_abl1_sensitivity`) and one more is
compromised (`cardiac_myosin_sensitivity_xray`). §4.3 rescues part of the BCR-ABL1 case with
an internal control.

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
| `kras_g12c_mandated` | **3.37** | 16.92 | 8.71 | **1** | 2.0 | **{11, 12, 13, 16, 34}** |
| `kras_g12c_corrected` | **3.43** | 16.77 | 8.74 | **1** | 2.0 | **{11, 12, 13, 16, 34}** |
| `bcr_abl1_mandated` | 7.66 | 24.29 | 15.45 | 2 | 3.0 | ∅ |
| `bcr_abl1_corrected` | 7.85 | 23.64 | 14.87 | 2 | 3.0 | ∅ |
| `bcr_abl1_sensitivity` | 7.78 | 22.98 | 14.91 | 2 | 3.0 | ∅ |
| `cardiac_myosin_corrected` | **13.70** | 30.08 | 23.81 | **4** | **6.0** | ∅ |
| `cardiac_myosin_sensitivity_xray` | 11.81 | 28.10 | 19.28 | 3 | 4.0 | ∅ |
| `cardiac_myosin_sensitivity_srx` | **14.65** | 28.81 | 20.37 | **4** | 4.5 | ∅ |

The same heavy-atom minima computed on the **holo** agree with the apo values to within
0.25 Å in every arm (largest gap: 11.56 vs 11.81 Å, `cardiac_myosin_sensitivity_xray`), so
the two sites neither approach nor separate on ligand binding. Hop counts were computed on
the apo only.

**The KRAS arms are not a distal-allostery task.** Five of the 21 label residues *are*
active-site residues. Even after the frozen 5 Å Cα distal filter removes them, the
remaining 14 "distal" labels are one contact-graph hop from the source (Y96 ··· A11) and
3.4 Å apart in heavy-atom terms. Any method that propagates from the active site will rank
these residues highly because they are the source's immediate neighbours — the KRAS arms
measure locality, not coupling. `bcr_abl1_*` at 2 hops / 7.7 Å and
`cardiac_myosin_*` at 3–4 hops / 11.8–14.7 Å are the arms that pose the actual problem.

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

| Arm | frame | n paired | chain RMSD | **distal labels** | p | **active site** | p | rest (null) |
|---|---|---|---|---|---|---|---|---|
| `kras_g12c_mandated` | global | 166 | 1.36 | 1.45 | 0.0013 | 0.43 | 1.0 | 0.66 |
| | core | | 1.53 | **1.88** | **0.0032** | **0.23** | **1.0** | 0.48 |
| `kras_g12c_corrected` | global | 167 | 1.34 | 1.33 | 2.4e-05 | 0.29 | 1.0 | 0.48 |
| | core | | 1.38 | **1.63** | **3.3e-05** | **0.26** | **1.0** | 0.43 |
| `bcr_abl1_mandated` | global | 429 | 0.98 | 0.37 | 1.0 | 0.71 | 0.031 | 0.56 |
| | core | | 1.10 | **0.37** | **0.78** | **1.35** | **0.017** | 0.41 |
| `bcr_abl1_corrected` | global | 252 | 1.78 | 0.64 | 0.86 | 0.93 | 0.11 | 0.87 |
| | core | | 2.01 | **0.48** | **0.61** | **0.90** | **0.025** | 0.50 |
| `bcr_abl1_sensitivity` | global | 251 | 2.54 | 0.64 | 1.0 | 1.65 | 0.35 | 1.60 |
| | core | | 3.30 | **0.47** | **0.46** | **1.58** | **0.34** | 0.50 |
| `cardiac_myosin_corrected` | global | 764 | 1.18 | 0.79 | 0.0019 | 0.29 | 1.0 | 0.59 |
| | core | | 1.26 | **0.74** | **0.036** | **0.29** | **1.0** | 0.43 |
| `cardiac_myosin_sensitivity_xray` | global | 700 | 1.23 | 1.03 | 0.00013 | 0.45 | 1.0 | 0.59 |
| | core | | 1.34 | **0.98** | **0.00046** | **0.26** | **1.0** | 0.43 |
| `cardiac_myosin_sensitivity_srx` | global | 912 | 0.88 | 0.40 | 0.23 | 0.28 | 1.0 | 0.36 |
| | core | | 0.90 | **0.39** | **0.076** | **0.18** | **1.0** | 0.31 |

Applying the rule:

| Arm | allosteric site responds? | **active site responds?** |
|---|---|---|
| `kras_g12c_mandated` | **yes** (1.88 Å, p = 0.003) | **no** (0.23 Å, p = 1.0 — *less* than the null) |
| `kras_g12c_corrected` | **yes** (1.63 Å, p = 3e-05) | **no** (0.26 Å, p = 1.0) |
| `bcr_abl1_mandated` | **no** (0.37 Å, p = 0.78) | yes by the rule (1.35 Å, p = 0.017) — **but see §4.3** |
| `bcr_abl1_corrected` | **one residue only** (median 0.48 Å; I521 = 10.25 Å) | yes by the rule (0.90 Å, p = 0.025) — **but see §4.3** |
| `bcr_abl1_sensitivity` | **one residue only** (median 0.47 Å; I502 = 9.44 Å) | **no** (1.58 Å but p = 0.34: the whole chain moves by that much) |
| `cardiac_myosin_corrected` | **yes** (0.74 Å, p = 0.036) | **no** (0.29 Å, p = 1.0) |
| `cardiac_myosin_sensitivity_xray` | **yes** (0.98 Å, p = 0.0005) | **no** (0.26 Å, p = 1.0) |
| `cardiac_myosin_sensitivity_srx` | **no** (0.39 Å, p = 0.08) | **no** (0.18 Å, p = 1.0) |

### 4.3 The BCR-ABL1 internal control: which ligand causes what `[DERIVED]`

The three ABL1 arms share one holo (5MO4) and differ in the apo's occupancy of the two
sites, which makes a clean 2×2 control possible:

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

**Reading.** A hinge opens at M515 and the helix beyond it swings 5–10 Å — *only when the
myristoyl pocket's occupancy differs between the members*. 1OPL, whose pocket is already
occupied (by myristate) and whose ATP-site ligand still differs from 5MO4's, shows
0.3–1.3 Å across the identical stretch. The helix position therefore **tracks the allosteric
pocket, not the ATP site**. This is a real, drug-attributable allosteric-site response, and
it is the only one in the benchmark that is both large and mechanistically coherent
(AY7 contacts F512, I521, V525, L529 in 5MO4 at 3.6–3.8 Å — one helix face, i/i+4/i+8).

The same control runs the other way on the active site:

| Region | 1OPL→5MO4 | 2G2H→5MO4 | 2G1T→5MO4 |
|---|---|---|---|
| P-loop | 3.22 | 2.37 | 4.47 |
| αC helix | 1.11 | 1.27 | 4.37 |
| catalytic loop HRD | 0.29 | 0.48 | 0.28 |
| DFG-Asp | 4.20 | 4.12 | 1.08 |
| **DFG-Phe** | **5.70** | **5.48** | **7.91** |

The DFG-Phe moves 5–8 Å in **all three** arms, including the one where the myristoyl pocket
is occupied in both members. **The active-site motion in the BCR-ABL1 arms is caused by the
ATP-site ligand swap (P16 / bisubstrate → nilotinib), not by asciminib.** Its appearance in
the §4.2 table is a confound, and the two arms that pass the decision rule fail this control.

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

## 5. Axis 5 — verdict and ranking

Five gates, each independently derived above:

- **A. Blind-input validity** — the allosteric site is genuinely empty in the apo.
- **B. Orthosteric match** — the same species occupies the catalytic site in both members,
  so a difference can be attributed to the allosteric ligand.
- **C. Genuine distality** — the two sites are separated enough that finding one from the
  other is a coupling problem rather than a neighbourhood problem.
- **D. Something to predict** — a measurable apo→holo change at the allosteric site.
- **E. Coupling demonstrated** — measurable, drug-attributable change at the **active site**.

| Rank | Arm | A | B | C | D | E | Net |
|---|---|---|---|---|---|---|---|
| **1** | `cardiac_myosin_corrected` 9GZ3→9GZ2 | ✅ | ✅ exact ADP·Mg·Pi | ✅ 13.7 Å / 4 hops | ✅ 0.74 Å, p = 0.036 | ❌ 0.29 Å, p = 1.0 | **Best available pair.** Drug is the only variable; site is genuinely distal. Cannot evidence coupling. |
| **2** | `cardiac_myosin_sensitivity_srx` 9YRG→9YR7 | ✅ | ✅ exact ADP·Pi | ✅ **14.7 Å / 4 hops** (largest separation in the set) | ❌ 0.39 Å, p = 0.08 | ❌ 0.18 Å, p = 1.0 | Only arm capturing the physiological IHM state the drug acts on — and precisely therefore, **the apo already sits in the drug-stabilised state**. Nothing changes anywhere (chain RMSD 0.90 Å). A valid label set with no transition to predict. |
| **3** | `cardiac_myosin_sensitivity_xray` 8QYP→8QYR | ✅ | ❌ **VO₄ vs BeF₃** + SO₄ in the site | ✅ 11.8 Å / 3 hops | ✅ 0.98 Å, p = 0.0005 | ❌ 0.26 Å, p = 1.0 | Strongest allosteric-site signal of the myosin arms and the highest-resolution holo, but the γ-phosphate analogue differs, so that signal is not attributable to mavacamten alone. |
| **4** | `bcr_abl1_corrected` 2G2H→5MO4 | ✅ | ❌ P16 vs nilotinib | ✅ 7.9 Å / 2 hops | ⚠️ one residue: I521 at 10.25 Å, hinge at M515 | ❌ active-site motion attributed to the ATP-ligand swap by the §4.3 control | The **only arm with a large, drug-attributable allosteric-site response** (§4.3). Its active-site motion is a confound, not coupling. |
| **5** | `bcr_abl1_sensitivity` 2G1T→5MO4 | ✅ | ❌ **worst**: bisubstrate `112` spanning ATP + peptide sites, vs nilotinib | ✅ 7.8 Å / 2 hops | ⚠️ one residue: I502 at 9.44 Å | ❌ 1.58 Å but p = 0.34 — indistinguishable from chain-wide noise (RMSD 3.30 Å) | Same αI signal as rank 4, but the whole chain moves, so nothing is separable. |
| **6** | `kras_g12c_corrected` 4LDJ→6OIM | ✅ | ✅ GDP·Mg | ❌ **1 hop, 3.4 Å, 5 shared residues; drug covalently bonded to active-site Cys12** | ✅ 1.63 Å, p = 3e-05 | ❌ 0.26 Å, p = 1.0 | A clean **cryptic-pocket** pair (frozen transplant: 18/41 clashes, 0.69 Å) and a poor **allosteric** pair: the site is contact-adjacent to the source. |
| **7** | `kras_g12c_mandated` 4OBE→6OIM | ✅ | ✅ GDP·Mg | ❌ same as rank 6 | ✅ 1.88 Å, p = 0.003 | ❌ 0.23 Å, p = 1.0 | Rank 6 plus the frozen genotype defect — and under this lens that defect is sharper: the apo lacks the very residue the drug is covalently attached to. |
| **8** | `bcr_abl1_mandated` 1OPL→5MO4 | ❌ **myristate occupies the target pocket** (15 atoms ≤ 4.5 Å, min 3.29 Å) | ❌ P16 vs nilotinib | ✅ 7.7 Å / 2 hops | ❌ 0.37 Å, p = 0.78 — pocket pre-formed *and* already ligand-adapted (§4.3) | ❌ attributed to the ATP-ligand swap | **Invalid on the allosteric lens as it was on the cryptic one.** Reported only because CHALLENGE.md Table 1 mandates it. |

Ranks 2 and 3 are a judgement call: `srx` trades "nothing to predict" for "nothing
confounded", `xray` the reverse. The ordering above weights attribution (gate B) above
signal magnitude (gate D), because a signal you cannot attribute cannot be scored against.

**Explicitly, as asked:**

- **Arms showing active-site response to allosteric-ligand binding: none.**
- Arms showing active-site response to *something*: `bcr_abl1_mandated` (p = 0.017) and
  `bcr_abl1_corrected` (p = 0.025) — both attributed to the orthosteric inhibitor swap by
  the §4.3 control, not to asciminib.
- Arms showing **no** active-site response at all: all six others; in every one the active
  site is *more* rigid than the rest of the chain (p_vs_rest = 1.0).

---

## 6. What follows

### 6.1 For the freeze

Nothing here requires the manifest to change, and this document changes nothing. Two facts
are new relative to the cryptic-lens audit and belong in the record if the freeze is ever
revisited:

1. **The KRAS arms fail a distality criterion that the cryptic lens never asked about.**
   Five label residues are active-site residues; the distal remainder is one contact hop
   from the source; the ligand is covalently bonded to an active-site residue. If the
   deliverable is "distal allosteric residues", the KRAS arms mostly test whether a method
   can rank the source's own neighbours.
2. **`cardiac_myosin_sensitivity_srx` is a matched pair with no transition.** Its virtue
   (identical construct, state, nucleotide) and its defect (apo and holo are the same
   structure to 0.90 Å) are the same fact. It is the allosteric analogue of a non-cryptic
   pocket, and its numbers should be read as a **negative control on transition**, not as an
   independent replication of the corrected arm.

### 6.2 For the method — the decision-relevant point

The frozen ground truth is **where the drug binds**, derived from holo-ligand contacts. It
is not **which residues are dynamically coupled to the active site**. This audit shows the
two are not the same thing in any frozen arm: the allosteric sites move (five arms) while
the active sites do not (all eight).

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
- The three myosin arms and the two ABL1 corrected/sensitivity arms are the ones that pose a
  real distal-search problem (3–4 and 2 hops). Reporting the KRAS arms alongside them without
  the hop-count context will overstate performance.

---

## 7. Reproduction

Every `[DERIVED]` number in §2, §3 and §4.2 regenerates from the script below; the §1.2,
§1.4, §1.5 and §4.3 tables come from the same primitives with different residue ranges.
Inputs are the frozen manifest, `frozen.json` and the deposited mmCIFs — no holo information
enters any apo-side quantity, and this file is evidence, never imported by prediction code
(C1).

Save as a scratch file and run `uv run python <file>` from the repo root. It imports one
private helper (`allo.benchmark._chain_ca`); if that moves, inline it.

> **Repaired 2026-08-20 after a second adversarial review.** The script had rotted twice and
> nobody had re-run it: it imported `allo.inputs.load`, which since the C1 boundary move
> returns the manifest **redacted** — so `sp["holo"]` raised `KeyError` — and its arm list
> still used the pre-ADR-0008 myosin IDs, missing the two arms that split added. The numbers
> below were computed when **eight** arms existed; §2's tables are unchanged and still hold
> for those eight, and the two added arms (`cardiac_myosin_site1_omecamtiv`,
> `cardiac_myosin_site2_corrected`) are **not** covered by them. Any claim that this document
> audits *every* frozen arm is true of the script as it now stands and not of the tables as
> written.

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
from allo.structure.pdb import fetch_mmcif, parse_mmcif

ARMS = [
    "kras_g12c_mandated",
    "kras_g12c_corrected",
    "bcr_abl1_mandated",
    "bcr_abl1_corrected",
    "bcr_abl1_sensitivity",
    "cardiac_myosin_site1_corrected",
    "cardiac_myosin_site1_sensitivity_xray",
    "cardiac_myosin_site1_sensitivity_srx",
    "cardiac_myosin_site1_omecamtiv",
    "cardiac_myosin_site2_corrected",
]
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


def contact_graph(st, chain, cutoff=CUT):
    """Residue graph: edge when any heavy-atom pair is within `cutoff`."""
    ri = res_atoms(st, chain)
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


def deviation(apo_id, apo_ch, holo_id, holo_ch):
    """Per-residue CA deviation, apo numbering, in a global and an outlier-rejected frame."""
    apo, holo = S(apo_id), S(holo_id)
    aca, hca = _chain_ca(apo, apo_ch), _chain_ca(holo, holo_ch)
    h2a = align_numbering(holo, apo, holo_ch, apo_ch)
    pairs = [(h, h2a[h]) for h in sorted(hca) if h in h2a and h2a[h] in aca]
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
    specs = {s["id"]: s for s in load()["targets"]}
    for arm in ARMS:
        sp, fz = specs[arm], frozen[arm]
        ac, hc = sp["apo"]["chain"], sp["holo"]["chain"]
        apo, holo = S(sp["apo"]["pdb"]), S(sp["holo"]["pdb"])
        labels, distal, active = (
            fz["label_residues"],
            fz["scoreable_label_residues"],
            fz["active_site"],
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
        g = site_distance(apo, ac, distal, active)
        adj = contact_graph(apo, ac)
        per = [hops(adj, [r], active) for r in distal if r in adj]
        print(
            f"  coupling: min {g['min']} A | mean-over-pairs {g['mean_over_pairs']} A | "
            f"mean-nearest {g['mean_nearest']} A | shortest path {hops(adj, distal, active)} hops | "
            f"median {float(np.median(per))} hops | shared residues {sorted(set(labels) & set(active))}"
        )

        # --- axis 4: local vs global response
        nums, dev_g, dev_c, ncore = deviation(sp["apo"]["pdb"], ac, sp["holo"]["pdb"], hc)
        rest = sorted(set(nums.tolist()) - set(labels) - set(active))
        for frame, dev in (("global", dev_g), ("core  ", dev_c)):
            r = dev[np.isin(nums, rest)]
            line = [
                f"  {frame} (n={len(nums)}, core-fit={ncore}, RMSD {np.sqrt((dev**2).mean()):.2f} A)"
            ]
            for name, s in (("distal-labels", distal), ("active-site", active)):
                x = dev[np.isin(nums, s)]
                p = mannwhitneyu(x, r, alternative="greater").pvalue
                line.append(f"{name} median {np.median(x):.2f} (p_vs_rest {p:.2g})")
            line.append(f"rest median {np.median(r):.2f}")
            print(" | ".join(line))


if __name__ == "__main__":
    main()
```

`9YRG.cif` was not in `data/raw/` at the start of this session; the script fetches it via
`allo.structure.pdb.fetch_mmcif`.
