# Independent re-measurement of the five blocking numbers

**Measured 2026-09-02**, from the deposited coordinate files only. Every number in the
2026-09-02 audit that a pending architecture decision rests on was re-derived here by a
second reader who did not run the audit's code and did not copy a value out of its prose.
The audit's probes were never committed, so nothing was reused: the reader is a fresh mmCIF
parser built on Biopython's `MMCIF2Dict` and NumPy, reproduced verbatim in section 7.

**Scope.** Items A to E below correspond to the five pending decisions. Nothing here is frozen
and nothing here moves a freeze. Where this recheck disagrees with the audit, the disagreement
is stated first and its cause after it.

**Provenance.** Every file was read from `data/raw/eval/`, and every one is byte-identical to
the decompressed tracked copy under `structures/`. Every one also matches the SHA-256 pinned in
`docs/benchmark/primary/manifest.yaml`. `5TBY` was not pinned there when this recheck began; it
was pinned during the run, and the hash measured here is the hash that was pinned.

| Entry | decompressed SHA-256 | matches the manifest pin |
| --- | --- | --- |
| `1OPL` | `af3a6348cbf0748243503f3aeec85f8cf0fa37a4989696cbfb4afa7424a97f6a` | yes |
| `5MO4`, `4OBE`, `4LDJ`, `6OIM`, `9GZ2`, `9GZ3`, `2G2H` | pinned values reproduced | yes |
| `5TBY` | `3d9a579847a11335ecf3b1dc858088ca2c046d7ddfa6fea0943ff17b6b319911` | yes, pinned mid-run |

**One thing moved while this ran.** Partway through the recheck, `docs/benchmark/primary/`
was rewritten in the working tree by the work implementing these very decisions:
`bcr_abl1_mandated` was re-pointed from `1OPL:A` to `1OPL:B`, so its `label_residues` fell
from 20 to 17, its `n_residues` from 451 to 365 and its `apo_site_occupancy` to an empty
pocket at 16.0 A; `cardiac_myosin_mandated` was added; `5TBY` was pinned in
`structure_provenance`. The KRAS and cardiac-myosin label sets, the source sets and the
`label_footprints` block are untouched, so items B, C and D are unaffected.

Item A is affected in one way that matters for reproduction and in no way that changes a
number. The audit's chain A claims are about the **20**-residue asciminib footprint, and
`frozen.json` no longer holds it. The probes therefore do not read the label set from
`frozen.json` at all: they derive it from `5MO4:A` plus `AY7` at 4.5 A, carry it onto
`1OPL:A` by alignment, and check it against `manifest.yaml`'s pinned `5MO4:A:AY7`
footprint, which the rewrite did not touch. All 20 are recovered, none unmapped, and every
item A number below is identical to the one obtained before the rewrite. Anyone re-running
these probes after the ADR lands will get the same values, which would not be true of a
probe that read `label_residues`.

---

## 0. Every number, side by side

`R` is this recheck. A dash in the audit column means the audit did not state the quantity.

| # | Quantity | Audit | R | Verdict |
| --- | --- | ---: | ---: | --- |
| A1 | `1OPL:A` labels contacted by `MYR`, 4.5 A heavy atom | 16 of 20 | 16 of 20 | AGREES |
| A2 | `1OPL:A` nearest `MYR` heavy atom to a label | 3.29 A | 3.29 A | AGREES |
| A3 | `1OPL:A` labels modelled | 20 of 20 | 20 of 20 | AGREES |
| A4 | `1OPL:A` distinct polymer B-factor values | 3041 | 3041 | AGREES |
| A5 | `1OPL:A` Ca RMSD to `5MO4:A`, all common residues | 0.98 A | 0.98 A | AGREES |
| A6 | `1OPL:B` myristoyl pocket | empty | empty, no `MYR` on the chain | AGREES |
| A7 | `1OPL:B` nearest ligand heavy atom to the label set | 16.0 A | 16.00 A | AGREES |
| A8 | `1OPL:B` labels modelled | 17 of 20 | 17 of 20, missing 521/525/529 | AGREES |
| A9 | `1OPL:B` distinct polymer B-factor values | 3 | 3 | AGREES |
| A10 | `1OPL:B` Ca RMSD to `5MO4:A`, all common residues | 22.89 A | 22.89 A | AGREES |
| A11 | `_refine.details` names group B-factors for molecule B | yes | yes, quoted in 1.6 | AGREES |
| A12 | Ca RMSD to `5MO4:A` over the kinase core, A / B | — | 1.00 / 1.08 A | new |
| B1 | `5TBY` vs `9GZ3` long-range Jaccard, separation >= 5 | 0.471 | 0.4706 | AGREES |
| B2 | recall of `9GZ3`'s long-range edges | 0.569 | 0.5687 | AGREES |
| B3 | edges at separation >= 5: `5TBY` / `9GZ3` / shared | 1103 / 1419 / 807 | 1103 / 1419 / 807 | AGREES |
| B4 | mean degree, separation >= 1 | 8.48 / 9.53 | 8.48 / 9.53 | AGREES |
| B5 | degree Spearman | 0.741 | 0.741 | AGREES |
| B6 | pairwise Ca-Ca distance Spearman | 0.9724 | 0.9742 | DISAGREES, third decimal |
| B7 | median absolute pairwise distance difference | 2.08 A | 1.95 A | DISAGREES, 0.13 A |
| C1 | mavacamten component ID in `9GZ2` | `XB2` | `XB2`, `_chem_comp.name` "Mavacamten" | AGREES |
| C2 | `XB2` contacts in `9GZ2:A` at 4.5 A | 12 | 12 | AGREES |
| C3 | transferred onto `5TBY:A`, unmapped | 12, none | 12, none | AGREES |
| D1 | KRAS residues masked | 11, 12, 13, 16, 34 | 11, 12, 13, 16, 34, both arms | AGREES |
| D2 | scoreable of label | 16 of 21 | 16 of 21, both arms | AGREES |
| D3 | the mask is labels intersected with the derived source | claimed | confirmed from `GDP`/`MG` contacts | AGREES |
| E1 | `1OPL:B` SH3 modelled | none | 0 residues under both window sets | AGREES |
| E2 | `1OPL:B` SH2 packs against the N-lobe | yes | yes, 11 of 11 interface residues | AGREES |
| E3 | SH2 to C-lobe centroid, chain A | 34.9 A | 34.3-34.6 A | DISAGREES, 0.3-0.6 A |
| E4 | SH2 to N-lobe centroid, chain A | 40.8 A | 42.4-43.1 A | DISAGREES, 1.6-2.3 A |
| E5 | SH2 to C-lobe centroid, chain B | 49.8 A | 48.8-49.2 A | DISAGREES, 0.6-1.0 A |
| E6 | SH2 to N-lobe centroid, chain B | 28.2 A | 26.5-27.1 A | DISAGREES, 1.1-1.7 A |
| E7 | chain B SH2 to nearest chain A atom | 32.66 A | 32.51 A | DISAGREES, 0.15 A |
| E8 | kinase-domain Ca RMSD, chain A on chain B | 0.53 A | 0.53 A | AGREES |
| E9 | SH2 Ca RMSD after that superposition | 70.07 A | 70.07 A | AGREES |
| E10 | SH2-kinase interface residues, chain A | 7, listed | identical list | AGREES |
| E11 | SH2-kinase interface residues, chain B | 11, listed | identical list | AGREES |

**Three disagreements. None of them changes a conclusion.**

1. **B6 and B7.** The pairwise Ca-Ca agreement between `5TBY` and `9GZ3` is Spearman 0.9742
   here against 0.9724 in the audit, and the median absolute distance difference is 1.95 A
   against 2.08 A. Both readings support the audit's finding at the same strength. The cause
   was not isolated: the residue-pair set is the same 289 180 pairs and neither entry has
   alternate conformations.
2. **E3 to E6.** The four SH2 centroid distances do not reproduce. The audit did not state
   where it put the boundary between the kinase N-lobe and the C-lobe, and its four numbers are
   reproducible only with that boundary near residue 350, which is not the canonical hinge
   (334-338 in this entry's numbering). Under every boundary from 320 to 355 the inversion the
   audit reports is intact and large. The claim survives; the four printed values need the
   boundary stated beside them.
3. **E7.** 32.51 A here against 32.66 A, on a claim neither value threatens.

Everything else reproduces to the last digit the audit printed.

---

## 1. A — `1OPL` chain A against chain B

**Method.** Model 1, hydrogens dropped, alternate conformations reduced to `.` or `A` (`1OPL`
has none). Chain membership is `_atom_site.auth_asym_id`; residue identity is `auth_seq_id`. A
residue is contacted when the minimum distance from any of its heavy atoms to any heavy atom of
the named component is at most 4.5 A, which is the frozen benchmark's own definition
(`manifest.yaml`, `defaults.contact_cutoff_angstrom`). The label set is derived rather than read: the `AY7`
footprint in `5MO4:A` at the same 4.5 A, carried onto `1OPL:A` by global alignment, which
recovers 20 residues with none unmapped and equals `manifest.yaml`'s pinned `5MO4:A:AY7`
footprint exactly. The same 20 author numbers are used for chain B, because `_struct_ref_seq`
gives both chains the same UniProt-to-author correspondence. B-factor statistics are over polymer atoms only. RMSD is computed by Kabsch
superposition on Ca atoms with no outlier rejection, and the residue correspondence between
entries comes from a global BLOSUM62 alignment of the two modelled chains (open -11,
extend -1), the convention `allo.groundtruth.labels` uses. Probe: `a_abl_chain.py`.

### 1.1 What each chain holds

```
A: 451 residues, 81-531, no gaps          non-polymer on the chain: MYR, P16
B: 365 residues, 140-518, gap 238-251     non-polymer on the chain: P16
```

Audit: chain A 451 residues, 81-531, no gaps, `MYR` and `P16`; chain B 365 residues, 140-518,
gap 238-251, `P16` only. **AGREES.**

### 1.2 Ligand contacts to the label set

| Chain | component | heavy atoms | labels within 4.5 A | nearest |
| --- | --- | ---: | ---: | ---: |
| A | `MYR` | 15 | **16 of 20** | **3.29 A** |
| A | `P16` | 29 | 0 | 16.37 A |
| A | both, and every component in the entry | 44 / 73 | 16 | 3.29 A |
| B | `P16` | 29 | **0 of 17** | **16.00 A** |
| B | every component in the entry | 73 | 0 | 16.00 A |

The 16 contacted labels are 356, 359, 360, 363, 448, 451, 452, 481, 482, 483, 484, 487, 512,
521, 525 and 529.

Audit: chain A 16 of 20 at 3.29 A; chain B 0 of 17, nearest ligand heavy atom 16.0 A.
**AGREES.** One clarification the audit's table leaves implicit: on chain A the 16 contacts and
the 3.29 A minimum come from `MYR` alone. `P16` contributes nothing to the label set at any
cutoff below 16 A, so the frozen `apo_site_occupancy` figure is a myristate figure.

### 1.3 Labels modelled

Chain A models all 20. Chain B models 17; 521, 525 and 529 lie past its C-terminus at 518.
Audit: 20 of 20 and 17 of 20. **AGREES.**

### 1.4 B-factors

| Chain | polymer atoms | mean | median | range | distinct values |
| --- | ---: | ---: | ---: | --- | ---: |
| A | 3628 | 85.0 | 72.1 | 25.5-254.5 | **3041** |
| B | 2954 | 170.7 | 161.2 | 160.8-198.1 | **3** |

`_refine.B_iso_mean` is 123.3. Including each chain's non-polymer atoms raises the distinct
counts to 3066 and 4. Audit: 3628 and 2954 atoms, means 85.0 and 170.7, 3041 and 3 distinct
values, entry mean 123.3. **AGREES.**

### 1.5 Ca RMSD against `5MO4:A`

`5MO4:A` models 429 residues over 83-531. The alignment finds 429 residues common with
`1OPL:A` and 345 common with `1OPL:B`.

| Superposed on | `1OPL:A` | `1OPL:B` |
| --- | ---: | ---: |
| all common Ca | **0.98 A** over 429 | **22.89 A** over 345 |
| the kinase core 254-512, RMSD over that core | 1.00 A over 239 | 1.08 A over 239 |
| the kinase core, RMSD then taken over all common Ca | 1.23 A over 429 | 36.56 A over 345 |

Audit: 0.98 A and 22.89 A, "global Ca RMSD, all common residues". **AGREES.**

The middle row is what the headline hides, and it belongs in the ADR. Chain B's kinase domain
fits the holo kinase domain as well as chain A's does, 1.08 A against 1.00 A over the same 239
Ca. The 22.89 A is entirely the regulatory module. Superposing on the kinase core and then
measuring everything gives 36.56 A, larger than the 22.89 A obtained when the fit is free to
compromise between the two arrangements. Chain B is not a poor model of the kinase; it is a
correct kinase carrying a different regulatory arrangement.

The 239-residue core is smaller than the 259 residues chain B models in 254-512, because
`5MO4:A` does not model all of that window.

### 1.6 `_refine.details`, verbatim

The value of `_refine.details` in the deposited `1OPL` mmCIF, character for character:

> The structure was refined by superimposing the refined high resolution structure of c-Abl (pdb entry 1OPK) on the molecular replacement solution and optimizing positions of individual domains by rigid-body refinement.  Following this, only overall domain B-factors were applied to molecule B, whereas individual B-factors were refined for molecule A.

The audit quotes this correctly. Its rendering has one space after "rigid-body refinement."
and the file has two. **AGREES.**

---

## 2. B — `5TBY` against `9GZ3`

**Method.** `5TBY` chain A models 954 residues over 6-959 with no gaps; `9GZ3` chain A models
764 over 3-796 with gaps at 203-213 and 625-643. A global BLOSUM62 alignment of the two
modelled chains gives 761 residues present in both. 760 of those 761 pairs carry the same
author number and all 761 carry the same residue name, so the two entries share a numbering
convention. The one exception is a terminal artefact of the aligner, which pairs `5TBY` 959
with `9GZ3` 796. Matching by identical author number instead gives the same 761 residues with
no name mismatch and the same edge counts, so the mapping is not load-bearing.

The contact definition is the frozen benchmark's, and it is not a Ca one: an edge exists when
two residues have heavy atoms within 4.5 A of each other. That is what the audit used and what
`manifest.yaml` freezes. A Ca-only family is reported beside it for the sensitivity question,
at 7, 8, 9 and 10 A. Sequence separation is the difference of author numbers. Jaccard is
shared over union; recall is shared over the `9GZ3` edge count. Probe:
`b_myosin_topology.py`.

### 2.1 The headline three

| Quantity | Audit | R |
| --- | ---: | ---: |
| Jaccard, separation >= 5, 4.5 A heavy atom | 0.471 | **0.4706** |
| recall of `9GZ3`'s long-range edges | 0.569 | **0.5687** |
| pairwise Ca-Ca Spearman | 0.9724 | **0.9742** |

Two of the three **AGREE** to the digits printed. The Spearman **DISAGREES** in the third
decimal. Both values round to 0.97 and both say the same thing.

### 2.2 The full edge accounting, 4.5 A heavy atom

| separation | `5TBY` | `9GZ3` | shared | Jaccard | recall | precision |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| >= 1 | 3226 | 3626 | 2862 | 0.7173 | 0.7893 | 0.8871 |
| >= 3 | 1783 | 2166 | 1447 | 0.5783 | 0.6681 | 0.8115 |
| >= 5 | 1103 | 1419 | 807 | 0.4706 | 0.5687 | 0.7316 |

Mean degree at separation >= 1 is 8.48 against 9.53; degree Spearman is 0.741. The audit
reports 3226/3626/2862, 1783/2166/1447 and 1103/1419/807, mean degree 8.48 against 9.53 and
degree Spearman 0.741. **AGREES on every cell.**

### 2.3 One convention the audit did not state, and what it is worth

`9GZ3` has two internal gaps and `5TBY` has none, so "sequence separation" is not the same
filter under the two entries' own numbering. Three readings:

| Separation keyed on | `9GZ3` edges, sep >= 3 | `9GZ3` edges, sep >= 5 | Jaccard, sep >= 5 | recall |
| --- | ---: | ---: | ---: | ---: |
| each entry's own author numbering | 2164 | 1415 | 0.4717 | 0.5703 |
| `5TBY` author numbering for both | **2166** | **1419** | **0.4706** | **0.5687** |
| position in the common set | 2164 | 1415 | 0.4717 | 0.5703 |

The audit used the middle row. It is the reading that treats the two graphs as one indexed
object, which is the right choice when the question is whether the same edge is present in
both. The three readings differ by 0.001 in Jaccard. This is recorded so the number is
reproducible, not because the choice matters.

### 2.4 Cutoff sensitivity

Jaccard at separation >= 5, with recall in brackets.

| Definition | 4.0 A | 4.5 A | 5.0 A | 5.5 A | 6.0 A |
| --- | ---: | ---: | ---: | ---: | ---: |
| heavy atom | 0.402 (0.515) | 0.472 (0.570) | 0.498 (0.610) | 0.565 (0.668) | 0.563 (0.673) |

| Definition | 7 A | 8 A | 9 A | 10 A |
| --- | ---: | ---: | ---: | ---: |
| Ca-Ca | 0.519 (0.620) | 0.549 (0.655) | 0.572 (0.678) | 0.589 (0.689) |

The finding is not an artefact of the cutoff. Long-range agreement is between 0.40 and 0.59
across every definition tried, heavy-atom and Ca alike, and recall of the measured edges never
exceeds 0.69. A looser cutoff improves the agreement by counting more pairs as contacts on both
sides, which is the expected direction and does not rescue the graph: at 6.0 A heavy atom, one
third of the measured long-range edges is still missing.

### 2.5 Pairwise distances

Over all 289 180 residue pairs of the common 761: Spearman 0.9742, Pearson 0.9690, median
absolute difference 1.95 A, mean absolute difference 2.98 A. The global Ca RMSD after
superposition is 6.87 A. Under the number-identity mapping the Spearman is 0.9754 and the
median difference 1.94 A.

The audit reports Spearman 0.9724 and a median absolute difference of 2.08 A. **DISAGREES** on
both, by 0.002 and 0.13 A. The audit's conclusion — the domains are placed correctly and the
residues are not — is unaffected. The rank agreement is 0.97 either way and the long-range
contact recall is 0.57 either way.

---

## 3. C — cardiac myosin label transfer

**Method.** The effector component was identified from `9GZ2`'s own `_chem_comp` block rather
than assumed. The four non-polymer components are `ADP`, `MG`, `PO4` and `XB2`, and
`_chem_comp.name` for `XB2` is **"Mavacamten"**, formula `C15 H19 N3 O2`. Contacts are heavy
atom to heavy atom within 4.5 A, with the ligand scoped to chain A. Transfer onto `5TBY` chain
A is by global BLOSUM62 alignment of the two modelled chains. Probe: `c_myosin_labels.py`.

### 3.1 The contact set

`XB2` has 20 heavy atoms in `9GZ2:A`. Twelve protein residues lie within 4.5 A.

| Residue | nearest heavy-atom distance |
| --- | ---: |
| TYR164 | 3.64 A |
| THR167 | 3.49 A |
| ASP168 | 2.80 A |
| HIS666 | 3.60 A |
| PRO710 | 3.82 A |
| ASN711 | 2.92 A |
| ARG712 | 2.91 A |
| ILE713 | 4.01 A |
| ARG721 | 3.73 A |
| TYR722 | 4.05 A |
| LEU770 | 3.94 A |
| GLU774 | 3.49 A |

At 4.0 A the set is 10 residues, because 713 and 722 drop out. At 5.0 A it is 14, because 163
and 717 enter.

### 3.2 Transfer

All twelve map onto modelled residues of `5TBY` chain A, at the same author number and with the
same residue name in every case. Nothing is unmapped and nothing falls outside the node set.
The resulting apo-numbered label set is

```
164, 167, 168, 666, 710, 711, 712, 713, 721, 722, 770, 774
```

which equals `frozen.json`'s `cardiac_myosin_corrected.label_residues` exactly, and the holo
footprint equals `manifest.yaml`'s pinned `9GZ2:A:XB2`.

Audit: all twelve transfer, none unmapped, the same twelve residues. **AGREES.**

---

## 4. D — the KRAS mask

**Method.** Two independent checks, plus a third on the labels. First, read `label_residues`
and `scoreable_label_residues` from `frozen.json` for both KRAS arms and take the difference.
Second, re-derive the propagation source from coordinates rather than trusting the frozen list:
apply the manifest rule `active_site: {from_ligands: [GDP, MG]}` to the apo entry, taking
protein residues with a heavy atom within 4.5 A of any `GDP` or `MG` heavy atom in chain A, and
intersect that with the label set. Third, re-derive the label set itself from the holo. Probe:
`d_kras_mask.py`.

### 4.1 The frozen sets

| Arm | labels | scoreable | removed | source | `n_residues` | `n_candidates` |
| --- | ---: | ---: | --- | ---: | ---: | ---: |
| `kras_g12c_mandated` | 21 | 16 | 11, 12, 13, 16, 34 | 23 | 169 | 146 |
| `kras_g12c_corrected` | 21 | 16 | 11, 12, 13, 16, 34 | 22 | 170 | 148 |

`n_candidates` equals `n_residues` minus the source on both arms, so the exclusion is applied
to the negative class as well.

### 4.2 The source, re-derived from coordinates

`4OBE:A` carries `GDP`, `MG` and water; 29 heavy atoms of `GDP` and `MG` are used. The derived
source is

```
11 12 13 14 15 16 17 18 28 29 30 32 33 34 36 57 116 117 119 120 145 146 147      (23)
```

`4LDJ:A` carries the same components and gives

```
11 12 13 14 15 16 17 18 28 30 32 33 34 36 57 116 117 119 120 145 146 147         (22)
```

Both equal the arm's frozen `active_site` exactly. No residue is derived that is not frozen and
none is frozen that is not derived. The two arms differ only at residue 29, which is within
4.5 A of the nucleotide in `4OBE` and not in `4LDJ`.

### 4.3 The overlap

Intersecting each derived source with the 21 labels gives, on both arms,

```
11, 12, 13, 16, 34
```

This is exactly the set the organisers name (A11, C12, G13, K16, P34) and exactly the set
`frozen.json` removes. **The five are a computed overlap, not a hand-typed list.**

### 4.4 The label set is also derived, not typed

`6OIM`'s effector component is `MOV`, whose `_chem_comp.name` is "AMG 510 (bound form)". Its
pocket in chain A at 4.5 A is 21 residues, and carried onto `4OBE:A` and onto `4LDJ:A` by
alignment it gives, in both cases,

```
9 10 11 12 13 16 34 58 59 60 61 62 63 68 69 72 95 96 99 100 103                  (21)
```

equal to the frozen `label_residues` on both arms.

The audit and the organisers say the overlap is exactly 11, 12, 13, 16 and 34, leaving 16
scoreable of 21, on both arms. **AGREES**, on both arms, with the source and the labels both
re-derived from coordinates.

---

## 5. E — what `1OPL` chain B actually models

**Method.** The entry's own records first. `_struct_ref` names UniProt `P00519`
(`ABL1_HUMAN`), with an isoform field of `?`. `_struct_ref_seq` states, for both chains, that
UniProt residues 1-531 correspond to author residues 1-531. The reference sequence in
`_struct_ref.pdbx_seq_one_letter_code` begins `MGQQPGKVLGDQ`, which is the isoform IB
N-terminus, and its residue 334 is a threonine — the ABL1 gatekeeper, numbered T315 in isoform
IA. **The author numbering of `1OPL` is UniProt P00519, and the offset to isoform IA numbering
is +19.** That is derived from the file, not recalled. `_pdbx_poly_seq_scheme` gives the
modelled residues. Probe: `e_abl_domains.py`.

### 5.1 Modelled content

`_pdbx_poly_seq_scheme` reports 537 residues per chain in the construct, of which chain A
models 451 (81-531) and chain B models 365 (140-518).

The isoform IA windows in the task map to author numbering by +19: SH3 **80-139**, SH2
**140-236**, kinase **261-512**. The audit used SH3 84-138, SH2 146-236 and kinase 254-512,
which are structure-based rather than UniProt-based windows; 146 is the first residue of the
SH2 `WYHG` motif in this sequence, so they are defensible. Both are reported.

| Window set | Domain | author range | chain A | chain B |
| --- | --- | --- | ---: | ---: |
| isoform IA + 19 | SH3 | 80-139 | 59 of 60 | **0 of 60** |
| | SH2 | 140-236 | 97 of 97 | 97 of 97 |
| | kinase | 261-512 | 252 of 252 | 252 of 252 |
| audit | SH3 | 84-138 | 55 of 55 | **0 of 55** |
| | SH2 | 146-236 | 91 of 91 | 91 of 91 |
| | kinase | 254-512 | 259 of 259 | 259 of 259 |

**"No SH3 modelled" is CONFIRMED**, under both window sets, because chain B begins at residue
140 and every SH3 window considered ends at 138 or 139. The margin is one residue under the
UniProt-derived window, so the claim is correct but not comfortable. Chain B additionally omits
238-251, the SH2-kinase linker.

Audit: chain A SH3 55, SH2 91, kinase 259; chain B SH3 0, SH2 91, kinase 259. **AGREES** on
every cell under the audit's own windows.

### 5.2 Where the SH2 domain sits — the interface

Kinase-domain residues (254-512) within 4.5 A of any SH2 atom (146-236):

| Chain | interface residues | N-lobe | C-lobe | of which are labels |
| --- | --- | ---: | ---: | --- |
| A | 357, 358, 360, 361, 393, 394, 512 | 0 | 7 | **360, 512** |
| B | 258, 259, 260, 261, 262, 263, 291, 294, 328, 329, 331 | 11 | 0 | none |

The audit prints chain A as "357, 358, 360, 361, 393, 394, 512" with labels 360 and 512, and
chain B as "258-263, 291, 294, 328, 329, 331" with none. **AGREES exactly.** The interface is
the strongest form of the claim, because it needs no lobe-boundary convention: every one of
chain A's seven contacts is past the hinge and every one of chain B's eleven is before it.

### 5.3 Where the SH2 domain sits — the centroids, and the disagreement

The lobe boundary has to be chosen, and the audit did not say what it chose. Taking the kinase
domain as 254-512 and the SH2 domain as 146-236, with centroids over Ca atoms:

| Boundary | chain A: SH2 to N-lobe | to C-lobe | chain B: SH2 to N-lobe | to C-lobe |
| ---: | ---: | ---: | ---: | ---: |
| 335, the gatekeeper T334 plus one | 43.1 A | 34.3 A | 26.5 A | 48.8 A |
| 338, the end of the hinge | 42.7 A | 34.4 A | 26.7 A | 49.1 A |
| 338, over heavy atoms rather than Ca | 43.0 A | 34.6 A | 26.6 A | 49.0 A |
| **audit** | **40.8 A** | **34.9 A** | **28.2 A** | **49.8 A** |

**DISAGREES**, on all four numbers, by 0.3 to 2.3 A. Sweeping the boundary from 320 to 355
shows why, and shows that it does not matter:

| Boundary | A: N-lobe | A: C-lobe | B: N-lobe | B: C-lobe |
| ---: | ---: | ---: | ---: | ---: |
| 320 | 42.4 | 34.5 | 26.9 | 46.7 |
| 330 | 43.0 | 34.3 | 26.5 | 48.1 |
| 340 | 42.4 | 34.5 | 26.8 | 49.2 |
| 350 | 41.0 | 34.8 | 28.1 | 49.8 |
| 355 | 39.9 | 35.3 | 29.0 | 49.9 |

The audit's four values are matched to within 0.6 A only at a boundary near 349, which puts
helix alpha-C in the C-lobe and is not a kinase lobe boundary anyone uses. The likeliest
explanation is a different, unstated split. A different SH2 or kinase window is a second
candidate. Neither can be checked, because the audit's probes were not committed.

**The claim the numbers were quoted to support is unaffected.** Across the whole sweep, chain
A's SH2 centroid is nearer the C-lobe by 5 to 9 A, and chain B's is nearer the N-lobe by 20 to
23 A. The inversion is real, it is large, and it agrees with the interface evidence in 5.2,
which needs no convention at all.

**Recommendation.** Reprint the four centroid values in `01-bcr-abl1-chain.md` §3.2 with the
lobe boundary stated beside them, or replace them with the interface counts in 5.2, which are
convention-free and reproduce exactly.

### 5.4 Two supporting numbers

Superposing chain A on chain B over the kinase domain gives **0.53 A** over 259 common Ca, and
the SH2 domain is then **70.07 A** away over 91 Ca. Both match the audit to the digit. Chain
B's SH2 domain comes no closer than **32.51 A** to any atom of chain A, against the audit's
32.66 A — a 0.15 A difference on a claim (the arrangement is intramolecular, not a lattice
contact) that neither value threatens.

---

## 6. What this changes

Nothing in items A, C and D. All three re-derive exactly, from coordinates, including the two
claims that most needed independent confirmation: that the `1OPL:A` myristoyl pocket is filled
at 3.29 A against the very residues the arm is scored on, and that the KRAS mask is a computed
label-source overlap rather than a list transcribed from the organisers' reply.

Item B re-derives to the digit on every count that carries the finding, and differs in the
third decimal on the Spearman and by 0.13 A on the median distance difference. The finding —
`5TBY` gets the fold right and the contact graph wrong — holds at every heavy-atom cutoff from
4.0 to 6.0 A and at every Ca cutoff from 7 to 10 A.

Item E confirms the two qualitative claims and does not reproduce the four centroid distances.
Those four numbers should be restated with their definition, or dropped in favour of the
interface counts.

One number is new and belongs in the ADR on the `1OPL` chain choice. **Chain B's kinase domain
fits the holo kinase domain as well as chain A's does, 1.08 A against 1.00 A over the same 239
Ca.** The 22.89 A global figure is entirely the regulatory module, and quoting it without that
decomposition overstates the case against chain B's coordinates. The case against chain B rests
on the three group B-factors, the absent SH3 domain and the N-lobe SH2 placement, all of which
reproduce exactly. It does not rest on the kinase domain being wrong, because it is not.

---

## 7. Reproduction

`d_kras_mask.py` reads `docs/benchmark/primary/frozen.json`, because item D is a question
about that file. Under `tests/test_no_leakage.py` that makes it uncommittable anywhere in the
repository, and the rest are kept beside it. They ran in the session scratchpad and
their source is reproduced here in full, which is the convention `README.md` clause 3 sets and
`12-dataset-eda.md` §9 established. Place the six files in one directory and run each with
`uv run python <file>` from inside it. Only `numpy`, `scipy` and `biopython` are needed, and
all three are declared in `pyproject.toml`.

### `common.py`

```python
"""Shared mmCIF reader for the blocking-measurement recheck.

Deliberately independent of `src/allo`: the point of the exercise is to re-derive the
audit's numbers without reusing the code that produced them. Only Biopython's
MMCIF2Dict (a plain text-to-dict reader, no coordinate model) and NumPy are used.
"""

from __future__ import annotations

import gzip
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from Bio.PDB.MMCIF2Dict import MMCIF2Dict

ROOT = Path("/Users/george0502/dev/004-allosteric-site")
CIF = ROOT / "data" / "raw" / "eval"  # uncompressed mirror
GZ = {"apo": ROOT / "structures" / "apo", "holo": ROOT / "structures" / "holo"}

THREE_TO_ONE = {
    "ALA": "A",
    "ARG": "R",
    "ASN": "N",
    "ASP": "D",
    "CYS": "C",
    "GLN": "Q",
    "GLU": "E",
    "GLY": "G",
    "HIS": "H",
    "ILE": "I",
    "LEU": "L",
    "LYS": "K",
    "MET": "M",
    "PHE": "F",
    "PRO": "P",
    "SER": "S",
    "THR": "T",
    "TRP": "W",
    "TYR": "Y",
    "VAL": "V",
    "MSE": "M",
    "SEC": "U",
    "PYL": "O",
}


@dataclass
class Atoms:
    """Flat, column-oriented atom table for one entry, model 1, hydrogens dropped."""

    pdb_id: str
    chain: np.ndarray  # auth_asym_id
    resnum: np.ndarray  # auth_seq_id (int)
    icode: np.ndarray  # pdbx_PDB_ins_code, '' when absent
    resname: np.ndarray  # auth_comp_id
    atom: np.ndarray  # auth_atom_id
    altloc: np.ndarray
    bfac: np.ndarray
    xyz: np.ndarray  # (n, 3)
    polymer: np.ndarray  # bool: label_seq_id is not '.'/'?'

    def sel(self, mask: np.ndarray) -> Atoms:
        return Atoms(
            self.pdb_id,
            *[
                getattr(self, f)[mask]
                for f in (
                    "chain",
                    "resnum",
                    "icode",
                    "resname",
                    "atom",
                    "altloc",
                    "bfac",
                    "xyz",
                    "polymer",
                )
            ],
        )

    def residues(self, chain: str) -> list[tuple[int, str]]:
        """Modelled polymer residues of one chain, in file order, (auth_seq_id, resname)."""
        m = (self.chain == chain) & self.polymer
        out, seen = [], set()
        for n, r in zip(self.resnum[m], self.resname[m], strict=True):
            if (n, r) not in seen:
                seen.add((n, r))
                out.append((int(n), str(r)))
        return out

    def res_atoms(self, chain: str, number: int) -> np.ndarray:
        m = (self.chain == chain) & (self.resnum == number) & self.polymer
        return self.xyz[m]

    def ca(self, chain: str) -> dict[int, np.ndarray]:
        m = (self.chain == chain) & self.polymer & (self.atom == "CA")
        return {int(n): x for n, x in zip(self.resnum[m], self.xyz[m], strict=True)}


def _col(d, key, n):
    v = d.get(key)
    if v is None:
        return [""] * n
    return v if isinstance(v, list) else [v]


def load(pdb_id: str, first_altloc: bool = True) -> Atoms:
    """Model 1, no hydrogens. `first_altloc` keeps altloc '.' or the lexically first."""
    d = MMCIF2Dict(str(CIF / f"{pdb_id}.cif"))
    n = len(d["_atom_site.id"])
    model = np.array(_col(d, "_atom_site.pdbx_PDB_model_num", n))
    elem = np.array(_col(d, "_atom_site.type_symbol", n))
    alt = np.array(_col(d, "_atom_site.label_alt_id", n))
    keep = (model == model[0]) & ~np.isin(elem, ["H", "D"])
    if first_altloc:
        keep &= np.isin(alt, [".", "?", "", "A"])
    lab_seq = np.array(_col(d, "_atom_site.label_seq_id", n))
    ins = np.array(_col(d, "_atom_site.pdbx_PDB_ins_code", n))
    return Atoms(
        pdb_id=pdb_id,
        chain=np.array(_col(d, "_atom_site.auth_asym_id", n))[keep],
        resnum=np.array([int(v) for v in _col(d, "_atom_site.auth_seq_id", n)])[keep],
        icode=np.where(np.isin(ins, [".", "?"]), "", ins)[keep],
        resname=np.array(_col(d, "_atom_site.auth_comp_id", n))[keep],
        atom=np.array(_col(d, "_atom_site.auth_atom_id", n))[keep],
        altloc=alt[keep],
        bfac=np.array([float(v) for v in _col(d, "_atom_site.B_iso_or_equiv", n)])[keep],
        xyz=np.stack(
            [
                np.array([float(v) for v in _col(d, f"_atom_site.Cartn_{a}", n)])[keep]
                for a in "xyz"
            ],
            axis=1,
        ),
        polymer=~np.isin(lab_seq, [".", "?"])[keep],
    )


def cif_dict(pdb_id: str) -> dict:
    return MMCIF2Dict(str(CIF / f"{pdb_id}.cif"))


def sha256_of_pinned(pdb_id: str) -> str | None:
    """SHA-256 over the decompressed bytes of the tracked structures/ copy."""
    for d in GZ.values():
        p = d / f"{pdb_id}.cif.gz"
        if p.exists():
            return hashlib.sha256(gzip.decompress(p.read_bytes())).hexdigest()
    return None


def frozen() -> dict:
    return json.loads((ROOT / "docs/benchmark/primary/frozen.json").read_text())


def manifest_footprint(key: str) -> list[str]:
    """The manifest's pinned holo-coordinate authority for one label set."""
    import yaml

    text = (ROOT / "docs/benchmark/primary/manifest.yaml").read_text()
    return yaml.safe_load(text)["label_footprints"][key]


def holo_labels(holo_id, holo_chain, comp, apo_id, apo_chain, cutoff=4.5):
    """The effector footprint in the holo, carried onto the apo by sequence alignment.

    Used instead of `frozen()["targets"][...]["label_residues"]` wherever the label set
    must not move: the frozen arm can be re-pointed at another chain, which changes that
    field, while the holo footprint is a property of the deposited holo entry alone.
    """
    holo, apo = load(holo_id), load(apo_id)
    lig = holo.xyz[(holo.chain == holo_chain) & ~holo.polymer & (holo.resname == comp)]
    pocket = [
        (n, r)
        for n, r in holo.residues(holo_chain)
        if min_dist(lig, holo.res_atoms(holo_chain, n)) <= cutoff
    ]
    mapping = align(holo.residues(holo_chain), apo.residues(apo_chain))
    modelled = dict(apo.residues(apo_chain))
    kept = sorted(mapping[n] for n, _ in pocket if mapping.get(n) in modelled)
    unmapped = [n for n, _ in pocket if mapping.get(n) not in modelled]
    return kept, unmapped, [f"{holo_chain}:{r}{n}" for n, r in pocket]


def min_dist(a: np.ndarray, b: np.ndarray) -> float:
    """Minimum pairwise Euclidean distance between two coordinate blocks."""
    if len(a) == 0 or len(b) == 0:
        return float("inf")
    return float(np.sqrt(((a[:, None, :] - b[None, :, :]) ** 2).sum(-1)).min())


def kabsch(mob: np.ndarray, ref: np.ndarray) -> tuple[np.ndarray, np.ndarray, float]:
    """Least-squares superposition of `mob` onto `ref`. Returns (R, t, rmsd)."""
    cm, cr = mob.mean(0), ref.mean(0)
    h = (mob - cm).T @ (ref - cr)
    u, _, vt = np.linalg.svd(h)
    dsign = np.sign(np.linalg.det(vt.T @ u.T))
    r = vt.T @ np.diag([1.0, 1.0, dsign]) @ u.T
    t = cr - r @ cm
    fitted = (r @ mob.T).T + t
    rmsd = float(np.sqrt(((fitted - ref) ** 2).sum(1).mean()))
    return r, t, rmsd


def rmsd_after(r, t, mob: np.ndarray, ref: np.ndarray) -> float:
    fitted = (r @ mob.T).T + t
    return float(np.sqrt(((fitted - ref) ** 2).sum(1).mean()))


def align(seq_a: list[tuple[int, str]], seq_b: list[tuple[int, str]]) -> dict[int, int]:
    """Global BLOSUM62 alignment of two modelled chains; auth number -> auth number."""
    from Bio.Align import PairwiseAligner, substitution_matrices

    al = PairwiseAligner(mode="global")
    al.substitution_matrix = substitution_matrices.load("BLOSUM62")
    al.open_gap_score, al.extend_gap_score = -11, -1
    sa = "".join(THREE_TO_ONE.get(r, "X") for _, r in seq_a)
    sb = "".join(THREE_TO_ONE.get(r, "X") for _, r in seq_b)
    best = al.align(sa, sb)[0]
    out = {}
    for (a0, a1), (b0, _) in zip(*best.aligned, strict=True):
        for k in range(a1 - a0):
            out[seq_a[a0 + k][0]] = seq_b[b0 + k][0]
    return out
```

### `a_abl_chain.py`

```python
"""A. 1OPL chain A versus chain B: ligand occupancy, B-factors, RMSD to 5MO4:A."""

from __future__ import annotations

import gzip
import hashlib
import sys

import numpy as np

sys.path.insert(0, str(__file__.rsplit("/", 1)[0]))
import common as C

# The label set is derived from the holo entry, not read from `frozen.json`: the frozen
# `bcr_abl1_mandated` arm can be re-pointed at another chain, which changes that field.
LAB, LAB_UNMAPPED, LAB_FOOTPRINT = C.holo_labels("5MO4", "A", "AY7", "1OPL", "A")
KINASE = (254, 512)  # the audit's kinase-domain window, author numbering


def labels():
    print("\n-- label set, derived from 5MO4:A + AY7 at 4.5 A --")
    print(f"  holo footprint ({len(LAB_FOOTPRINT)}): {LAB_FOOTPRINT}")
    print(
        f"  matches the manifest's pinned 5MO4:A:AY7: "
        f"{C.manifest_footprint('5MO4:A:AY7') == LAB_FOOTPRINT}"
    )
    print(f"  carried onto 1OPL:A ({len(LAB)}): {LAB}   unmapped: {LAB_UNMAPPED}")


def provenance():
    raw = (C.CIF / "1OPL.cif").read_bytes()
    gz = gzip.decompress((C.GZ["apo"] / "1OPL.cif.gz").read_bytes())
    print("1OPL raw mirror == pinned gz bytes:", raw == gz)
    print("1OPL sha256:", hashlib.sha256(gz).hexdigest())
    import yaml

    pinned = yaml.safe_load((C.ROOT / "docs/benchmark/primary/manifest.yaml").read_text())
    print("manifest pin:", pinned["structure_provenance"]["1OPL"]["sha256"])


def occupancy(a, chain):
    print(f"\n-- {chain}: ligand contacts to the 20 holo-derived labels --")
    modelled = {n for n, _ in a.residues(chain)}
    present = [r for r in LAB if r in modelled]
    print(
        f"labels modelled in chain {chain}: {len(present)} of {len(LAB)}  "
        f"missing={sorted(set(LAB) - modelled)}"
    )
    het = a.chain == chain
    comps = sorted(set(a.resname[het & ~a.polymer]))
    lab_xyz = {r: a.res_atoms(chain, r) for r in present}
    for scope, mask in [
        *[(c, (a.chain == chain) & ~a.polymer & (a.resname == c)) for c in comps],
        ("ALL chain components", (a.chain == chain) & ~a.polymer),
        ("ALL entry components", ~a.polymer),
    ]:
        lig = a.xyz[mask]
        d = {r: C.min_dist(lig, x) for r, x in lab_xyz.items()}
        within = sorted(r for r, v in d.items() if v <= 4.5)
        nearest = min(d.values()) if d else float("nan")
        print(
            f"  {scope:<22} atoms={len(lig):4d}  labels<=4.5A={len(within):2d}  "
            f"nearest={nearest:.2f} A  {within}"
        )


def bfactors(a):
    print("\n-- B-factors, polymer atoms only, model 1, first altloc --")
    for chain in ("A", "B"):
        m = (a.chain == chain) & a.polymer
        b = a.bfac[m]
        print(
            f"  {chain}: atoms={len(b)}  mean={b.mean():.1f}  median={np.median(b):.1f}  "
            f"range={b.min():.1f}-{b.max():.1f}  distinct={len(set(b.tolist()))}"
        )
        m2 = a.chain == chain
        print(f"     (incl. het atoms: n={m2.sum()}, distinct={len(set(a.bfac[m2].tolist()))})")
    d = C.cif_dict("1OPL")
    print("  _refine.B_iso_mean:", d.get("_refine.B_iso_mean"))


def refine_details():
    d = C.cif_dict("1OPL")
    v = d["_refine.details"]
    print("\n-- _refine.details, verbatim --")
    print(v[0] if isinstance(v, list) else v)


def rmsd_to_holo(a):
    holo = C.load("5MO4")
    href = holo.residues("A")
    hca = holo.ca("A")
    print("\n-- Ca RMSD against 5MO4:A --")
    print(f"  5MO4:A modelled residues: {len(href)}  range {href[0][0]}-{href[-1][0]}")
    for chain in ("A", "B"):
        aref = a.residues(chain)
        mapping = C.align(aref, href)  # 1OPL auth -> 5MO4 auth
        aca = a.ca(chain)
        pairs = [(n, m) for n, m in mapping.items() if n in aca and m in hca]
        mob = np.array([aca[n] for n, _ in pairs])
        ref = np.array([hca[m] for _, m in pairs])
        _, _, r_all = C.kabsch(mob, ref)
        core = [i for i, (n, _) in enumerate(pairs) if KINASE[0] <= n <= KINASE[1]]
        rot, tr, r_core = C.kabsch(mob[core], ref[core])
        r_all_on_core = C.rmsd_after(rot, tr, mob, ref)
        print(
            f"  1OPL:{chain}  modelled={len(aref)} range {aref[0][0]}-{aref[-1][0]}  "
            f"common with 5MO4:A = {len(pairs)}"
        )
        print(f"     superposed on all common Ca   -> RMSD {r_all:.2f} A over {len(pairs)}")
        print(
            f"     superposed on kinase {KINASE} -> RMSD {r_core:.2f} A over {len(core)} core, "
            f"{r_all_on_core:.2f} A over all {len(pairs)}"
        )


def gaps(a):
    print("\n-- modelled ranges and internal gaps --")
    for chain in ("A", "B"):
        nums = [n for n, _ in a.residues(chain)]
        g = [
            (nums[i] + 1, nums[i + 1] - 1)
            for i in range(len(nums) - 1)
            if nums[i + 1] != nums[i] + 1
        ]
        print(f"  {chain}: n={len(nums)} range {nums[0]}-{nums[-1]} gaps={g}")


if __name__ == "__main__":
    provenance()
    labels()
    a = C.load("1OPL")
    gaps(a)
    for ch in ("A", "B"):
        occupancy(a, ch)
    bfactors(a)
    refine_details()
    rmsd_to_holo(a)
```

### `b_myosin_topology.py`

```python
"""B. 5TBY:A against 9GZ3:A -- contact-graph agreement and pairwise-distance agreement."""

from __future__ import annotations

import sys

import numpy as np
from scipy.spatial import cKDTree
from scipy.stats import spearmanr

sys.path.insert(0, str(__file__.rsplit("/", 1)[0]))
import common as C


def common_residues():
    m5, m9 = C.load("5TBY"), C.load("9GZ3")
    r5, r9 = m5.residues("A"), m9.residues("A")
    mapping = C.align(r5, r9)  # 5TBY auth -> 9GZ3 auth
    have9 = {n for n, _ in r9}
    pairs = [(a, b) for a, b in sorted(mapping.items()) if b in have9]
    seq5 = {n: r for n, r in r5}
    seq9 = {n: r for n, r in r9}
    same_number = sum(1 for a, b in pairs if a == b)
    same_name = sum(1 for a, b in pairs if seq5[a] == seq9[b])
    print(
        f"5TBY:A modelled {len(r5)} ({r5[0][0]}-{r5[-1][0]}), "
        f"9GZ3:A modelled {len(r9)} ({r9[0][0]}-{r9[-1][0]})"
    )
    print(
        f"aligned and modelled in both: {len(pairs)}; "
        f"identical author number: {same_number}; identical residue name: {same_name}"
    )
    return m5, m9, pairs


def edges(atoms, chain, numbers, cutoff, mode):
    """Undirected contact set over `numbers`. mode='heavy' or 'ca'."""
    idx = {n: i for i, n in enumerate(numbers)}
    if mode == "ca":
        ca = atoms.ca(chain)
        pts = np.array([ca[n] for n in numbers])
        tree = cKDTree(pts)
        return {(min(i, j), max(i, j)) for i, j in tree.query_pairs(cutoff)}
    coords, owner = [], []
    for n in numbers:
        x = atoms.res_atoms(chain, n)
        coords.append(x)
        owner.append(np.full(len(x), idx[n]))
    pts, own = np.vstack(coords), np.concatenate(owner)
    tree = cKDTree(pts)
    out = set()
    for i, j in tree.query_pairs(cutoff):
        a, b = own[i], own[j]
        if a != b:
            out.add((min(a, b), max(a, b)))
    return out


def filt(es, numbers, sep):
    """Keep edges whose author-numbering separation is at least `sep`."""
    return {e for e in es if abs(numbers[e[0]] - numbers[e[1]]) >= sep}


def convention_sweep(m5, m9, pairs, cutoff=4.5):
    """The three ways of keying |i-j| once the two entries are matched up."""
    n5 = [a for a, _ in pairs]
    n9 = [b for _, b in pairs]
    e5 = edges(m5, "A", n5, cutoff, "heavy")
    e9 = edges(m9, "A", n9, cutoff, "heavy")
    keys = {
        "each entry's own author numbering": (n5, n9),
        "5TBY author numbering for both": (n5, n5),
        "position in the common set": (list(range(len(n5))), list(range(len(n5)))),
    }
    print(f"\n== separation convention, heavy {cutoff} A ==")
    for name, (k5, k9) in keys.items():
        print(f"  {name}")
        for sep in (1, 3, 5):
            a, b = filt(e5, k5, sep), filt(e9, k9, sep)
            s = a & b
            print(
                f"    sep>={sep}: 5TBY={len(a):5d} 9GZ3={len(b):5d} shared={len(s):5d} "
                f"Jaccard={len(s) / len(a | b):.4f} recall={len(s) / len(b):.4f}"
            )


def number_identity(cutoff=4.5):
    """Cross-check: match residues by identical author number instead of by alignment."""
    m5, m9 = C.load("5TBY"), C.load("9GZ3")
    r5 = dict(m5.residues("A"))
    r9 = dict(m9.residues("A"))
    shared_n = sorted(set(r5) & set(r9))
    bad = [(n, r5[n], r9[n]) for n in shared_n if r5[n] != r9[n]]
    n = [x for x in shared_n if r5[x] == r9[x]]
    print(f"\n== number-identity mapping: {len(n)} residues, name mismatches {bad} ==")
    e5, e9 = edges(m5, "A", n, cutoff, "heavy"), edges(m9, "A", n, cutoff, "heavy")
    for sep in (1, 3, 5):
        a, b = filt(e5, n, sep), filt(e9, n, sep)
        s = a & b
        print(
            f"  sep>={sep}: 5TBY={len(a):5d} 9GZ3={len(b):5d} shared={len(s):5d} "
            f"Jaccard={len(s) / len(a | b):.4f} recall={len(s) / len(b):.4f}"
        )
    ca5, ca9 = m5.ca("A"), m9.ca("A")
    x5 = np.array([ca5[i] for i in n])
    x9 = np.array([ca9[i] for i in n])
    iu = np.triu_indices(len(n), 1)
    d5 = np.linalg.norm(x5[iu[0]] - x5[iu[1]], axis=1)
    d9 = np.linalg.norm(x9[iu[0]] - x9[iu[1]], axis=1)
    print(
        f"  pairwise Ca Spearman = {spearmanr(d5, d9).statistic:.4f}  "
        f"median |diff| = {np.median(np.abs(d5 - d9)):.2f} A"
    )


def report(m5, m9, pairs, cutoff, mode):
    n5 = [a for a, _ in pairs]
    n9 = [b for _, b in pairs]
    e5 = edges(m5, "A", n5, cutoff, mode)
    e9 = edges(m9, "A", n9, cutoff, mode)
    print(f"\n== {mode} cutoff {cutoff} A ==")
    for sep in (1, 3, 5):
        a, b = filt(e5, n5, sep), filt(e9, n9, sep)
        shared = a & b
        jac = len(shared) / len(a | b)
        print(
            f"  sep>={sep}: 5TBY={len(a):5d} 9GZ3={len(b):5d} shared={len(shared):5d} "
            f"Jaccard={jac:.3f} recall={len(shared) / len(b):.3f} "
            f"precision={len(shared) / len(a):.3f} "
            f"mean_deg={2 * len(a) / len(n5):.2f}/{2 * len(b) / len(n9):.2f}"
        )
    d5 = np.bincount([i for e in filt(e5, n5, 1) for i in e], minlength=len(n5))
    d9 = np.bincount([i for e in filt(e9, n9, 1) for i in e], minlength=len(n9))
    print(f"  degree Spearman (sep>=1): {spearmanr(d5, d9).statistic:.3f}")


def pairwise_distances(m5, m9, pairs):
    ca5, ca9 = m5.ca("A"), m9.ca("A")
    x5 = np.array([ca5[a] for a, _ in pairs])
    x9 = np.array([ca9[b] for _, b in pairs])
    iu = np.triu_indices(len(pairs), 1)
    d5 = np.linalg.norm(x5[iu[0]] - x5[iu[1]], axis=1)
    d9 = np.linalg.norm(x9[iu[0]] - x9[iu[1]], axis=1)
    print(f"\n== pairwise Ca-Ca distances over {len(d5)} residue pairs ==")
    print(
        f"  Spearman = {spearmanr(d5, d9).statistic:.4f}   "
        f"Pearson = {np.corrcoef(d5, d9)[0, 1]:.4f}"
    )
    print(
        f"  median |difference| = {np.median(np.abs(d5 - d9)):.2f} A   "
        f"mean = {np.abs(d5 - d9).mean():.2f} A"
    )
    _, _, rms = C.kabsch(x5, x9)
    print(f"  global Ca RMSD after superposition = {rms:.2f} A")


if __name__ == "__main__":
    m5, m9, pairs = common_residues()
    for cut in (4.0, 4.5, 5.0, 5.5, 6.0):
        report(m5, m9, pairs, cut, "heavy")
    for cut in (7.0, 8.0, 9.0, 10.0):
        report(m5, m9, pairs, cut, "ca")
    pairwise_distances(m5, m9, pairs)
    convention_sweep(m5, m9, pairs)
    number_identity()
```

### `c_myosin_labels.py`

```python
"""C. Mavacamten contacts in 9GZ2, and their transfer onto 5TBY chain A."""

from __future__ import annotations

import sys

sys.path.insert(0, str(__file__.rsplit("/", 1)[0]))
import common as C


def identify_ligand():
    d = C.cif_dict("9GZ2")
    ids = d["_chem_comp.id"]
    names = d["_chem_comp.name"]
    formulas = d.get("_chem_comp.formula", [""] * len(ids))
    types = d.get("_chem_comp.type", [""] * len(ids))
    print("-- 9GZ2 chemical components that are not standard amino acids --")
    for i, n, f, t in zip(ids, names, formulas, types, strict=True):
        if "PEPTIDE" in str(t).upper():
            continue
        print(f"  {i:4s}  {n}   [{f}]  ({t})")
    return d


def pocket(cutoff=4.5, comp="XB2", chain="A"):
    a = C.load("9GZ2")
    lig = a.xyz[(a.chain == chain) & ~a.polymer & (a.resname == comp)]
    print(f"\n-- {comp} in 9GZ2 chain {chain}: {len(lig)} heavy atoms --")
    out = []
    for n, name in a.residues(chain):
        d = C.min_dist(lig, a.res_atoms(chain, n))
        if d <= cutoff:
            out.append((n, name, round(d, 2)))
    print(f"protein residues within {cutoff} A: {len(out)}")
    for n, name, d in out:
        print(f"   {name}{n:<5d} {d:5.2f} A")
    return [n for n, _, _ in out], a


def transfer(holo_numbers, holo_atoms):
    m5 = C.load("5TBY")
    r5, r9 = m5.residues("A"), holo_atoms.residues("A")
    mapping = C.align(r9, r5)  # 9GZ2 auth -> 5TBY auth
    modelled = dict(r5)
    print("\n-- transfer onto 5TBY chain A (global BLOSUM62 alignment of modelled chains) --")
    kept, unmapped = [], []
    for n in holo_numbers:
        t = mapping.get(n)
        if t is None or t not in modelled:
            unmapped.append(n)
        else:
            kept.append((n, t, modelled[t], dict(r9)[n]))
    for h, t, name5, name9 in kept:
        flag = "" if name5 == name9 else "   <-- residue name differs"
        print(f"   9GZ2 {name9}{h:<5d} -> 5TBY {name5}{t:<5d}{flag}")
    print(f"mapped {len(kept)}, unmapped {unmapped}")
    print("apo-numbered label set:", sorted(t for _, t, _, _ in kept))
    frozen = C.frozen()["targets"]["cardiac_myosin_corrected"]
    print("frozen cardiac_myosin_corrected label_residues:", frozen["label_residues"])
    print("frozen holo_label_footprint:", frozen["holo_label_footprint"])


if __name__ == "__main__":
    identify_ligand()
    for cut in (4.0, 4.5, 5.0):
        nums, atoms = pocket(cut)
        if cut == 4.5:
            keep = (nums, atoms)
    transfer(*keep)
```

### `d_kras_mask.py`

```python
"""D. KRAS: is the five-residue mask the label/source overlap, re-derived from coordinates?"""

from __future__ import annotations

import sys

import numpy as np

sys.path.insert(0, str(__file__.rsplit("/", 1)[0]))
import common as C

ARMS = {"kras_g12c_mandated": ("4OBE", "A"), "kras_g12c_corrected": ("4LDJ", "A")}
SOURCE_LIGANDS = ["GDP", "MG"]  # manifest rule: active_site {from_ligands: [GDP, MG]}


def frozen_view():
    print("-- frozen.json, both KRAS arms --")
    t = C.frozen()["targets"]
    for arm in ARMS:
        a = t[arm]
        lab, sc = set(a["label_residues"]), set(a["scoreable_label_residues"])
        print(f"  {arm}")
        print(f"    label_residues     ({len(lab)}): {sorted(lab)}")
        print(f"    scoreable          ({len(sc)}): {sorted(sc)}")
        print(f"    removed            ({len(lab - sc)}): {sorted(lab - sc)}")
        print(f"    active_site        ({len(a['active_site'])}): {a['active_site']}")
        print(
            f"    n_residues={a['n_residues']}  n_candidates={a['n_candidates']}  "
            f"n_residues - |excluded| = {a['n_residues'] - len(a['excluded_from_scoring'])}"
        )


def derive_source(pdb_id, chain, cutoff=4.5):
    a = C.load(pdb_id)
    comps = sorted(set(a.resname[(a.chain == chain) & ~a.polymer].tolist()))
    lig = a.xyz[(a.chain == chain) & ~a.polymer & np.isin(a.resname, SOURCE_LIGANDS)]
    hits = []
    for n, _ in a.residues(chain):
        if C.min_dist(lig, a.res_atoms(chain, n)) <= cutoff:
            hits.append(n)
    print(f"\n-- {pdb_id}:{chain} source from {SOURCE_LIGANDS} at {cutoff} A --")
    print(f"   chain components: {comps}   ligand heavy atoms used: {len(lig)}")
    print(f"   derived source ({len(hits)}): {hits}")
    return hits


def check():
    t = C.frozen()["targets"]
    for arm, (pdb_id, chain) in ARMS.items():
        derived = set(derive_source(pdb_id, chain))
        a = t[arm]
        frozen_src = set(a["active_site"])
        lab, sc = set(a["label_residues"]), set(a["scoreable_label_residues"])
        print(
            f"   frozen active_site matches derived: {derived == frozen_src}"
            f"   (derived-only {sorted(derived - frozen_src)}, "
            f"frozen-only {sorted(frozen_src - derived)})"
        )
        overlap = lab & derived
        print(f"   labels inside the derived source ({len(overlap)}): {sorted(overlap)}")
        print(
            f"   organisers' mask {{11, 12, 13, 16, 34}} == that overlap: "
            f"{overlap == {11, 12, 13, 16, 34}}"
        )
        print(f"   frozen removed set == that overlap: {(lab - sc) == overlap}")
        print(f"   scoreable count: {len(sc)} of {len(lab)}")


def labels_from_holo(cutoff=4.5):
    """Cross-check the 21 labels themselves: 6OIM:A + MOV, carried onto each apo."""
    holo = C.load("6OIM")
    d = C.cif_dict("6OIM")
    ids, names = d["_chem_comp.id"], d["_chem_comp.name"]
    print("\n-- 6OIM effector component --")
    for i, n in zip(ids, names, strict=True):
        if i == "MOV":
            print(f"   MOV = {n}")
    lig = holo.xyz[(holo.chain == "A") & ~holo.polymer & (holo.resname == "MOV")]
    pocket = [n for n, _ in holo.residues("A") if C.min_dist(lig, holo.res_atoms("A", n)) <= cutoff]
    print(f"   6OIM:A MOV pocket at {cutoff} A ({len(pocket)}): {pocket}")
    for arm, (pdb_id, chain) in ARMS.items():
        apo = C.load(pdb_id)
        mapping = C.align(holo.residues("A"), apo.residues(chain))
        moved = sorted({mapping[n] for n in pocket if n in mapping})
        print(f"   -> {arm} ({pdb_id}:{chain}): {len(moved)} labels {moved}")
        print(
            f"      equals frozen label_residues: "
            f"{moved == C.frozen()['targets'][arm]['label_residues']}"
        )


if __name__ == "__main__":
    frozen_view()
    check()
    labels_from_holo()
```

### `e_abl_domains.py`

```python
"""E. 1OPL chain B: which domains are modelled, and where the SH2 domain sits."""

from __future__ import annotations

import sys

import numpy as np

sys.path.insert(0, str(__file__.rsplit("/", 1)[0]))
import common as C

# Domain windows in ABL1 isoform IA numbering, as given in the task.
IA = {"SH3": (61, 120), "SH2": (121, 217), "kinase": (242, 493)}
# The audit's windows, in the file's own author numbering.
AUDIT = {"SH3": (84, 138), "SH2": (146, 236), "kinase": (254, 512)}


def numbering():
    """Establish the author <-> UniProt offset from the file, not from memory."""
    d = C.cif_dict("1OPL")
    seq = "".join(d["_struct_ref.pdbx_seq_one_letter_code"][0].split())
    print("-- _struct_ref / _struct_ref_seq --")
    print(
        "  db:",
        d["_struct_ref.db_name"],
        d["_struct_ref.db_code"],
        d["_struct_ref.pdbx_db_accession"],
        "isoform:",
        d["_struct_ref.pdbx_db_isoform"],
    )
    for row in zip(
        d["_struct_ref_seq.pdbx_strand_id"],
        d["_struct_ref_seq.db_align_beg"],
        d["_struct_ref_seq.db_align_end"],
        d["_struct_ref_seq.pdbx_auth_seq_align_beg"],
        d["_struct_ref_seq.pdbx_auth_seq_align_end"],
        strict=True,
    ):
        print(f"  chain {row[0]}: UNP {row[1]}-{row[2]}  ==  author {row[3]}-{row[4]}")
    print(f"  reference sequence length {len(seq)}, starts {seq[:12]!r}")
    print("  isoform IB N-terminus (MGQQPGKV...):", seq.startswith("MGQQPGKV"))
    print(
        f"  residue 334 of the reference sequence = {seq[333]!r} "
        f"(ABL1 gatekeeper T315 in isoform IA numbering => offset "
        f"{334 - 315 if seq[333] == 'T' else 'undetermined'})"
    )
    return seq


def poly_seq_scheme():
    """Modelled / not modelled per chain, from the entry's own residue scheme."""
    d = C.cif_dict("1OPL")
    ch = d["_pdbx_poly_seq_scheme.pdb_strand_id"]
    auth = d["_pdbx_poly_seq_scheme.auth_seq_num"]
    seqn = d["_pdbx_poly_seq_scheme.seq_id"]
    out = {}
    for c, a, s in zip(ch, auth, seqn, strict=True):
        out.setdefault(c, {})[int(s)] = None if a in {".", "?"} else int(a)
    print("\n-- _pdbx_poly_seq_scheme: modelled residues per chain --")
    for c, m in out.items():
        obs = sorted(v for v in m.values() if v is not None)
        print(f"  chain {c}: {len(obs)} of {len(m)} modelled, {obs[0]}-{obs[-1]}")
    return out


def domain_content(a, windows, tag):
    print(f"\n-- domain content, {tag} windows (author numbering) --")
    for chain in ("A", "B"):
        nums = {n for n, _ in a.residues(chain)}
        row = []
        for name, (lo, hi) in windows.items():
            got = sorted(n for n in nums if lo <= n <= hi)
            row.append(f"{name} {lo}-{hi}: {len(got)}/{hi - lo + 1}")
        print(f"  chain {chain}: " + " | ".join(row))


def centroids(a, windows, hinge, atoms="CA"):
    """SH2 centroid to N-lobe and C-lobe centroids, per chain."""
    k0, k1 = windows["kinase"]
    s0, s1 = windows["SH2"]
    print(f"\n-- SH2 centroid distances, kinase {k0}-{k1} split at {hinge}, {atoms} atoms --")

    def cen(chain, nums, lo, hi):
        sel = [n for n in nums if lo <= n <= hi]
        if atoms == "CA":
            ca = a.ca(chain)
            pts = np.array([ca[n] for n in sel if n in ca])
        else:
            pts = np.vstack([a.res_atoms(chain, n) for n in sel])
        return pts.mean(0), len(sel)

    for chain in ("A", "B"):
        nums = [n for n, _ in a.residues(chain)]
        sh2, n_sh2 = cen(chain, nums, s0, s1)
        nlobe, n_n = cen(chain, nums, k0, hinge - 1)
        clobe, n_c = cen(chain, nums, hinge, k1)
        dn = float(np.linalg.norm(sh2 - nlobe))
        dc = float(np.linalg.norm(sh2 - clobe))
        print(
            f"  chain {chain}: SH2({n_sh2}) -> N-lobe({n_n}) {dn:5.1f} A   "
            f"-> C-lobe({n_c}) {dc:5.1f} A   closer to "
            f"{'N-lobe' if dn < dc else 'C-lobe'}"
        )


def sh2_interface(a, windows, hinge, cutoff=4.5):
    k0, k1 = windows["kinase"]
    s0, s1 = windows["SH2"]
    labels = set(C.holo_labels("5MO4", "A", "AY7", "1OPL", "A")[0])
    print(f"\n-- kinase residues within {cutoff} A of the SH2 domain --")
    for chain in ("A", "B"):
        nums = [n for n, _ in a.residues(chain)]
        sh2 = np.vstack([a.res_atoms(chain, n) for n in nums if s0 <= n <= s1])
        hits = [
            n for n in nums if k0 <= n <= k1 and C.min_dist(sh2, a.res_atoms(chain, n)) <= cutoff
        ]
        nl = [n for n in hits if n < hinge]
        cl = [n for n in hits if n >= hinge]
        print(f"  chain {chain}: {hits}")
        print(
            f"     N-lobe {len(nl)} {nl} | C-lobe {len(cl)} {cl} | "
            f"of which labels: {sorted(set(hits) & labels)}"
        )


def domain_superposition(a, windows):
    k0, k1 = windows["kinase"]
    s0, s1 = windows["SH2"]
    ca_a, ca_b = a.ca("A"), a.ca("B")
    core = [n for n in sorted(set(ca_a) & set(ca_b)) if k0 <= n <= k1]
    rot, tr, rms = C.kabsch(np.array([ca_a[n] for n in core]), np.array([ca_b[n] for n in core]))
    sh2 = [n for n in sorted(set(ca_a) & set(ca_b)) if s0 <= n <= s1]
    r_sh2 = C.rmsd_after(
        rot, tr, np.array([ca_a[n] for n in sh2]), np.array([ca_b[n] for n in sh2])
    )
    print("\n-- chain A superposed on chain B, kinase domain only --")
    print(f"  kinase {k0}-{k1}: {len(core)} common Ca, RMSD {rms:.2f} A")
    print(f"  SH2 {s0}-{s1} after that superposition: {len(sh2)} Ca, RMSD {r_sh2:.2f} A")
    # closest approach of chain B's SH2 to any atom of chain A -- lattice check
    b_sh2 = np.vstack([a.res_atoms("B", n) for n, _ in a.residues("B") if s0 <= n <= s1])
    a_all = a.xyz[a.chain == "A"]
    print(f"  chain B SH2 to nearest chain A atom: {C.min_dist(b_sh2, a_all):.2f} A")


def hinge_sweep(a, windows=AUDIT):
    """How much of the centroid numbers is the lobe boundary, and how much is geometry."""
    k0, k1 = windows["kinase"]
    s0, s1 = windows["SH2"]
    print(f"\n-- centroid sensitivity to the lobe boundary, kinase {k0}-{k1} --")
    print("  hinge |  A: N-lobe  C-lobe  |  B: N-lobe  C-lobe")
    for hinge in range(320, 356, 5):
        row = []
        for chain in ("A", "B"):
            ca = a.ca(chain)
            nums = sorted(ca)
            sh2 = np.mean([ca[n] for n in nums if s0 <= n <= s1], axis=0)
            nl = np.mean([ca[n] for n in nums if k0 <= n < hinge], axis=0)
            cl = np.mean([ca[n] for n in nums if hinge <= n <= k1], axis=0)
            row += [np.linalg.norm(sh2 - nl), np.linalg.norm(sh2 - cl)]
        print(
            f"   {hinge}  |     {row[0]:5.1f}   {row[1]:5.1f}  |     {row[2]:5.1f}   {row[3]:5.1f}"
        )


if __name__ == "__main__":
    seq = numbering()
    poly_seq_scheme()
    a = C.load("1OPL")
    mapped_ia = {k: (lo + 19, hi + 19) for k, (lo, hi) in IA.items()}
    print("\ntask's isoform IA windows mapped to author numbering (+19):", mapped_ia)
    domain_content(a, mapped_ia, "isoform IA + 19")
    domain_content(a, AUDIT, "audit")
    for hinge in (335, 338):
        centroids(a, AUDIT, hinge)
        centroids(a, mapped_ia, hinge)
    centroids(a, AUDIT, 338, atoms="heavy")
    sh2_interface(a, AUDIT, 338)
    domain_superposition(a, AUDIT)
    hinge_sweep(a)
```
