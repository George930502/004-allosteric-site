# 0044 — The occupant annotation is two-class, cites a published roster, and decides nothing

**Status:** accepted · 2026-09-03 · closes review 27 §3.3 and §3.5 · input-layer re-freeze,
no evaluation protocol version change

## Context

Two clauses talk about what may sit in an apo entry's catalytic site, and neither defines its
own terms.

> **(iii)** The apo member contains **no ligand of any kind within the scoreable portion of
> that site**.
>
> **(x)** No apo component may contact a **scoreable** label.

"Ligand" and "component" are undefined. Water, glycerol, sulfate, chloride and polyethylene
glycol have no declared side. Meanwhile `orthosteric_vocabulary` carries an `additives` class
that is **empty in both frozen sets**, so every component that contacts an active site is
recorded as a catalytic-state component — as though it were the substrate or the cofactor.
Four occupants are recorded that way today:

| arm         | apo entry | occupant           | recorded as               |
| ----------- | --------- | ------------------ | ------------------------- |
| `ptp1b`     | `1SUG`    | `GOL`, four copies | catalytic-state component |
| `mkp5`      | `1ZZW`    | `SO4`              | catalytic-state component |
| `chk1`      | `1IA8`    | `SO4`              | catalytic-state component |
| `ecoli_cps` | `1A9X`    | `CL`, `K`          | catalytic-state component |

Review `27` raised this twice, as §3.3 "the occupant instrument is undefined" and §3.5 "the
orthosteric vocabulary is not shared across the sets". They are one question.

## What the evidence says

A scoped literature review ran on 2026-09-03 and two repository measurements were made against
it. Every claim below carries a DOI or a re-runnable command;
`../benchmark/review/data/occupant-instrument-2026-09-03.json` holds the record.

### 1. No published three-class scheme exists

§3.3 proposed `APO` / `APO_WITH_ADDITIVE_IN_POCKET` / `NOT_APO`. **The middle class has no
precedent.** The review searched for pseudo-apo, apo-like, quasi-apo and ligand-free-with-
additive. Every published instrument is binary and folds the third class into one of the other
two: Wankowicz's ten-heavy-atom floor and PocketMiner's five-species whitelist fold it into
apo; AHoJ folds it into holo, and says so deliberately, on the ground that a crystallographic
agent perturbs the local geometry whatever its biological relevance
(doi:10.1093/bioinformatics/btac701). Inventing a third class would be a hyperparameter chosen
after seeing the data, so it is not invented.

### 2. Every roster that names glycerol or sulfate puts them on the additive side

| source                                       | roster published   | `GOL`        | `SO4`        | `CL` / `K`    |
| -------------------------------------------- | ------------------ | ------------ | ------------ | ------------- |
| BioLiP2 (doi:10.1093/nar/gkad630)            | **yes, 463 IDs**   | artifact     | artifact     | artifact      |
| Binding MOAD (doi:10.1093/nar/gkm911)        | no, hand-curated   | additive     | additive     | additive      |
| PDBbind (doi:10.1093/bioinformatics/btu626)  | no                 | excluded     | excluded     | excluded      |
| sc-PDB (doi:10.1093/nar/gku928)              | no, 140 Da floor   | excluded     | excluded     | excluded      |
| RCSB Ligand of Interest                      | list not published | not an LOI   | not an LOI   | not an LOI    |
| PocketMiner (doi:10.1038/s41467-023-36699-3) | **yes, 5 species** | disqualifies | disqualifies | **tolerated** |
| ASD, CASBench, AlloBench                     | none               | silent       | silent       | silent        |

**No retrieved source classes `GOL` or `SO4` as a functional occupant.** The only instruments
that would keep them are the ones that filter nothing at all.

### 3. Per component, the mechanism

- **`GOL` in `1SUG`.** The depositors publish the entry as apo, in the title —
  "Water-molecule network and active-site flexibility of **apo** protein tyrosine phosphatase
  1B" (doi:10.1107/S0907444904015094) — and put four ordered **waters** in the catalytic
  pocket, three at the substrate phosphate oxygen positions. Measured here at the frozen 4.5
  angstrom heavy-atom cutoff against the eleven-residue PTP-motif site: two of the four
  glycerols do not reach it at all, at 11.93 and 16.44 angstrom, and the two that do graze
  **one** motif residue each, at 3.84 and 3.47 angstrom. Neither fills the phosphate cradle.
  Glycerol is **not** inert as a class — it is a competitive inhibitor of glycogen phosphorylase
  with an apparent K_i of 3.8 % v/v and binds that enzyme's catalytic site
  (doi:10.1110/ps.8.4.741) — which is why the rule below is per structure and not per component.
- **`SO4` in `1ZZW`.** The deposition paper attributes MKP5's active conformation to the
  protein itself, calling it constitutively active without substrate binding
  (doi:10.1016/j.jmb.2006.05.059). Nothing attributes the conformation to the sulfate. More
  generally, in a protein tyrosine phosphatase sulfate is a **positional** phosphate mimic and
  not a conformational one: phosphate closes the WPD loop and gives the substrate-bound
  conformation, sulfate leaves it open (doi:10.2174/09298665113209990041, full text).
- **`SO4` in `1IA8`, and it is the one case that points the other way.** Measured here: the
  sulfate contacts residues 54, 129, 153, 162, 164 and 166, which is Chen 2000's Lys54, Arg129,
  Thr153 and Arg162 plus Lys166 — and exactly **one** of the eleven VAIK/HRD/DFG motif
  residues. So it sits in the **activation-segment phosphothreonine cradle**, not in the ATP
  cleft. For a kinase the literature reports that such a sulfate can support the active
  conformation of an unphosphorylated activation segment, standing in for a modification the
  construct does not carry. That reading is `[UNVERIFIED]`: the deposition paper's full text
  returned 403 and the supporting claim is about kinases in general, not about CHK1. It is
  recorded rather than acted on, and §"Consequences" says what would settle it.
- **`CL` in `1A9X`.** Precipitant counter-ion. Crystals were grown from 0.65 to 1.35 M
  tetraethylammonium chloride plus 100 to 250 mM KCl and MnCl2 (doi:10.1021/bi982517h, full
  text), and the entry carries four tetraethylammonium ions from the same liquor. No retrieved
  source ascribes a function to any chloride site. This is an absence-of-evidence finding.
- **`K` in `1A9X`.** Functional, and named so by the structure's own laboratory: "Glu215 plays
  a key allosteric role by coordinating to the **physiologically important** potassium ion"
  (doi:10.1107/S0907444998006234). This is the one occupant of the four with direct published
  support for "catalytic-state component", and it keeps that class.

### 4. The annotation decides nothing, and that is the important part

The vocabulary looks like the instrument and is not. **Clause (iii) and clause (x) both decide
from `apo.ligand`**, defined at `src/allo/structure/pdb.py:87` as every non-polymer heavy atom
that is not water. That mask is **name-blind**: it counts glycerol, sulfate, chloride and
potassium alike, and consults no vocabulary. It is AHoJ's position, the most conservative of
the three in §1, and it is already what the code does.

Traced across the whole repository, `matches_apo` and `orthosteric_state` are written at
`src/allo/benchmark.py:281` and `:422` and read by **no score, no verdict and no gate** — only
by two test assertions and one review tool. Clause (vi) requires the occupancy to be
**recorded**, not to match. Clause (viii) reads the hand-declared `state.matched`, which
`secondary/README.md` already says is independent of the derived field.

So the benchmark's apo-ness was never resting on this judgement call. What was wrong is that
the annotation says something false and reads as though it were the gate.

## Decision

**1. The occupant annotation stays two-class, and the classes are named for what they are.**
`state_components` means "the substrate, product, cofactor or ion the enzyme needs to be in
this functional state". `additives` means "present because of how the crystal was grown".
There is no third class, because none exists to cite.

**2. The instrument is per structure with a cited roster, not a global component list.** Where
a component's own deposition literature settles it, that decides. Otherwise BioLiP2's
463-identifier artifact list (doi:10.1093/nar/gkad630) is the default, because it is the only
published, distributed roster in the field. This is Binding MOAD's own position, stated in
their paper: "some small molecules are valid ligands in some structures but additives in
others."

**3. Applied to the four occupants:**

| component | class                          | on what                                                                                                                             |
| --------- | ------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------- |
| `GOL`     | **additive**                   | every roster; the depositors' own "apo" title; two of four copies out of reach and two grazing one residue each                     |
| `SO4`     | **additive**                   | every roster; positional and not conformational mimic in a PTP; in `1IA8` it is in the phospho-cradle and touches one motif residue |
| `CL`      | **additive**                   | precipitant counter-ion at 0.65 to 1.35 M, no function in any source                                                                |
| `K`       | **state component**, unchanged | "physiologically important", named by the depositing laboratory                                                                     |

**4. `secondary/README.md` and the vocabulary's own comment state that the annotation is
descriptive.** A reader must not be able to mistake it for the apo-ness gate, which is
name-blind and stricter than any roster here.

**5. The `ptp1b` arm's recorded conformational state is corrected, and `matched` becomes
false.** The manifest records `apo: WPD-loop open` and `holo: WPD-loop open`, `matched: true`.
The deposition paper's headline result is that the apo WPD loop is **closed**
(doi:10.1107/S0907444904015094). Measured here, as the Asp181 carboxylate to Cys215 sulfur
distance, which is the field's own discriminator, with the arm's own holo as the control:

| entry  | role | Asp181(OD)–Cys215(SG) | reads  |
| ------ | ---- | --------------------: | ------ |
| `1SUG` | apo  |            **6.52 A** | closed |
| `1T48` | holo |           **12.62 A** | open   |

A 6.1 angstrom separation on the same arm. Both strings were wrong and the arm's two halves do
**not** match. Clause (viii) discloses state and never gates on it — three admitted arms
already carry `matched: false` — so nothing is admitted or rejected by this, and the arm stays.

## Consequences

- **The input layer is re-frozen.** `matches_apo` flips from false to true on `mkp5`, `chk1`
  and `ptp1b`, because each apo's only recorded occupant moves out of `state_components` and
  the holo has none. `smyd3` keeps its verdict and moves two bucket lists. `ecoli_cps` keeps
  its verdict, since both halves hold the same components. **No number moves.**

  **CORRECTED 2026-09-03 by the round-5 audit: this said the primary freeze is byte-identical
  and it is not.** `primary/frozen.json` moved one leaf, `orthosteric_vocabulary.additives`,
  from the empty list to the three components. The vocabulary is echoed into the freeze
  verbatim, so declaring an additive class necessarily moves it. What is true, and is what the
  sentence was reaching for, is that **no primary TARGET moved**: every per-arm value is
  identical, because no primary active site contacts any of the three components — which the
  existing freeze proves by existing, since the classifier raises on an unnamed contacting
  component. A wrong claim about a freeze is worse than a moved leaf, and this one stood for a
  day inside the ADR that made the change.
- **One sentence in `secondary/README.md` goes stale by this ADR and is corrected with it**:
  the derived and declared state fields no longer disagree on four arms.
- **The evaluation protocol does not move.** No endpoint, null, decoy or decision changes, and
  `docs/benchmark/evaluation/frozen.json` keeps `protocol_version: 4`.
- **What would reopen this.** Reading doi:10.1016/s0092-8674(00)80704-7 in full, or measuring
  whether removing the `1IA8` sulfate changes CHK1's activation-segment conformation, could
  move `SO4` back for that arm alone. The per-set vocabulary cannot express a per-arm class
  today, so that change would need a schema change and its own ADR. It is recorded here so
  that the next reader does not have to rediscover it.
- **A separate finding, recorded and not acted on.** The `ecoli_cps` active-site rule is
  `from_ligands: [ADP, MN, PO4]`, and the depositors describe that inorganic phosphate as a
  reagent contaminant: "the original crystallization conditions did not include inorganic
  phosphate… most likely resulted from either a contaminant in the ADP samples or the breakdown
  of ADP" (doi:10.1021/bi982517h, full text). The phosphate does mark the phosphate-binding
  subsite, so this is a provenance finding rather than a misplacement, but a propagation source
  partly anchored on a contaminant is worth its own decision and does not get one here.
