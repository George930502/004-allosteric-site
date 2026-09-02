# Validation targets

Source: `CHALLENGE.md` §6, Table 1. Four targets are the **minimum submission set**.

> **This file is narrative. `docs/benchmark/primary/frozen.json` is the authority for every residue
> count, label set, distance and active site, and `docs/benchmark/primary/manifest.yaml` for every
> choice.** Where the two disagree, the freeze wins and this file is the bug — it is prose and
> nothing re-derives it. Read `docs/benchmark/primary/README.md` for the frozen benchmark itself.

| Target | Disease area | Class | Apo (input) | Holo (ground truth) | Pocket to find |
|---|---|---|---|---|---|
| KRAS G12C | Oncology | GTPase | `4OBE` | `6OIM` | cryptic Switch-II pocket, locked by sotorasib (AMG 510) [18,19] |
| BCR-ABL1 | Oncology | tyrosine kinase | `1OPL` | `5MO4` | distal myristoyl pocket, used by asciminib [20,21] |
| Cardiac myosin | Cardiology | motor protein | `5TBY` | `6C1H` | mechanical site where mavacamten stabilises the super-relaxed state [22,23] |
| c-Myc (stretch) | Oncology | transcription factor | `1NKP` | — | none characterised; judged by consensus + docking viability [24] |

Bracketed numbers are reference indices in `CHALLENGE.md` §10.

---

## Ground-truth policy (non-negotiable)

**The ground-truth label set is derived programmatically from the holo structure. It is
never hand-typed from memory or from a paper's figure.**

It is the residue shell lining a literature-validated allosteric pocket, identified from
the holo complex — a drug footprint, whose allosteric status comes from the functional
experiment cited in `manifest.yaml` under `allosteric_evidence`, not from the geometry
(ADR 0007).

Procedure (implemented in `src/allo/groundtruth/`, Phase 1):

1. Load the holo structure, identify the ligand of interest by chemical component ID.
2. Select protein residues with any heavy atom within a cutoff (default 4.5 Å) of any
   ligand heavy atom — this residue set is the pocket.
3. Map holo residue numbering onto the apo numbering by sequence alignment, not by
   assuming the numbering matches. Record unmapped residues explicitly.
4. Emit the label set with the cutoff, ligand ID, chain and alignment recorded
   alongside it, so a label set is always traceable to how it was made.

Rationale: hand-entered residue lists are the single most likely source of a silent,
result-invalidating error in this project, and an LLM recalling "the Switch-II pocket
residues" is exactly the failure mode to design out. The cutoff is a knob; report
sensitivity to it.

**Holo data must never reach the prediction path (constraint C1 in `AGENTS.md`).**
Enforced by `tests/test_no_leakage.py`.

---

## Per-target facts — established 2026-08-20

Derived programmatically from the deposited mmCIF files and RCSB/SIFTS, never recalled.
Regenerate with `uv run allo benchmark show`. Full dossiers: `docs/benchmark/primary/audit/`.
The audit found that **all three challenge-assigned pairs are defective**, one fatally;
the frozen benchmark and the corrected pairs are in `docs/benchmark/`.

| Pair | Verdict | The finding |
|---|---|---|
| KRAS `4OBE` → `6OIM` | usable with caveats | `4OBE` is **wild-type** KRAS (Gly12), not G12C |
| BCR-ABL1 `1OPL` → `5MO4` | not blind **on chain A** | chain A carries myristate **in the target pocket**; apo and holo are the same conformation (1.00 Å) |
| Cardiac myosin `5TBY` → `6C1H` | **unscoreable as assigned** | `6C1H` is rat myosin-Ib + actin, no mavacamten; `5TBY` is a 20 Å homology model |

**Two verdicts were reopened on 2026-09-02, when the organisers answered four questions.**
Their answers outrank `CHALLENGE.md`. Both mandated arms now run, both are non-confirmatory,
and both print their measured defects. One page states every departure from Table 1:
[`report/substitutions.md`](report/substitutions.md).

| Pair | What changed | Record |
|---|---|---|
| BCR-ABL1 | the input is **`1OPL` chain B**, which the organisers designated. Chain B's myristoyl pocket is genuinely empty — nearest ligand atom 16.0 Å. The cost is that chain B was rigid-body placed with three group B-factors | [ADR 0029](adr/0029-bcr-abl1-uses-the-designated-chain-b-as-a-reported-arm.md) |
| Cardiac myosin | the holo is **`9GZ2`**, which the organisers sanctioned in place of `6C1H`. All twelve mavacamten-contact residues transfer onto `5TBY`:A with none unmapped, so a label set exists. Both input defects stand and are measured | [ADR 0031](adr/0031-expose-5tby-as-a-reported-arm-with-both-defects-measured.md) |
| c-Myc | `1NKP` becomes a reported deliverable, scored against NMR chemical-shift segments with a hypergeometric null, and **declared non-blind** | [ADR 0036](adr/0036-cmyc-is-a-reported-deliverable-scored-against-nmr-segments.md) |

### KRAS G12C (`4OBE` → `6OIM`)

- `4OBE`: X-ray 1.24 Å, chains A and B, GDP + Mg only, `_struct_ref_seq_dif` lists **no
  mutation** — residue 12 is GLY in both chains. `6OIM`: G12C **plus** C51S/C80L/C118S,
  sotorasib as comp `MOV`, covalently linked `CYS12.SG–MOV303.C25`. 166/170 identical.
- Numbering: both auth 1–169 ↔ UniProt P01116 1–169, **offset 0**.
- Nucleotide state: GDP·Mg in apo and holo. **Settled in ADR 0006**: cofactors are not network
  nodes, but the apo entry's own cofactor may *locate* the propagation source (ADR 0005).
- The pocket is **genuinely cryptic**: transplanting `MOV` into the apo frame leaves its
  closest atom 0.75 Å from protein and 14 of 41 ligand atoms clashing below 2.5 Å.
- Corrected apo: **`4LDJ`** — same study (doi 10.1073/pnas.1404639111), same release day,
  1.15 Å, one chain, and actually G12C. `4OBE`'s own `_pdbx_database_related` names it.

### BCR-ABL1 (`1OPL` → `5MO4`)

- ⚠️ resolved: `1OPL` **does** contain myristate (`MYR`, chain A only) occupying the
  myristoyl pocket, plus an ATP-site inhibitor (`P16`) in both chains. The 16 `MYR`
  contact residues are a strict subset of asciminib's 20 in `5MO4`.
- Deleting `MYR` as an excluded modification (C5) does not restore blindness: the pocket
  walls stay in the ligand-bound conformation. Apo↔holo Cα RMSD is **1.00 Å** over 409 paired
  residues and **0.50 Å** across the pocket lining.
  ⚠️ **The clause "there is no conformational change to predict" stood here and is withdrawn**
  (ADR 0003 amendment, ADR 0007). A pre-formed pocket is not a defect: the myristoyl pocket is
  the field's canonical *allosteric but not cryptic* site, and what remains to predict is which
  of the many pre-formed pockets is the coupled one. The ligand-occupancy reason above is
  sufficient on its own and is the one that bears on C1.
- ⚠️ resolved: the numbering offset between the two entries is **zero**. Both use ABL1
  **isoform 1b** numbering (gatekeeper 334, DFG 400–402). The hazard is real but sits
  elsewhere: `1OPL`'s deposited `_struct_ref_seq` wrongly claims auth = UniProt, so
  normalising through that record shifts it by 19. SIFTS corrects it. The ABL corpus is
  split between 1a and 1b conventions (`2G1T`, `2HYY`, `4WA9`, `1M52` are 1a), so the
  convention is resolved **per entry**, never assumed.
- `5MO4` is a **ternary** complex: asciminib (`AY7`) in the myristoyl pocket **and** nilotinib
  (`NIL`) in the ATP site, on a T334I/D382N background. The holo is not singly liganded.
- ⚠️ corrected: `5MO4` is **not** kinase-domain-only. It spans auth 83–531 — SH3, SH2 and
  kinase, the same architecture as `1OPL`. The alignment step does not break.
- ⚠️ corrected again, 2026-09-02: that span is **not continuous**. `5MO4`:A models **429**
  residues over 83–531 with two gaps, **296–297** and **402–419**. The second gap is the
  activation loop and it swallows the DFG motif at 400–402. An earlier version of the line
  above said "continuously", which is wrong. It moves no label — all twenty are modelled — and
  it does not move the propagation source, because the `{from_motifs: [VAIK, HRD, DFG]}` rule
  runs on the apo member. Measured with `gemmi` from the tracked mmCIF.
- `1OPL` quality: 3.42 Å, R-free 0.315, **22.18 % RSRZ outliers**, which is the **0.4th
  absolute percentile** of the PDB (wwPDB `percent-RSRZ-outliers`; re-fetched 2026-08-24 from
  `ebi.ac.uk/pdbe/api/validation/global-percentiles/entry/1opl`, which returns
  `rawvalue: 22.18, absolute: 0.4`). **A 2026-08-21 correction to 6.50 % was itself the error**
  and said the 22.2 % was "a percentile read as a percentage". It is the other way round: 22.18
  is the value and 0.4 is the percentile. Chains A and B differ by 23 Å globally; chain B lacks
  the myristate and the αI helix.
- **`1OPL` chain B is the frozen input since 2026-09-02**, on the organisers' designation
  (ADR 0029). Its dossier, all measured from the tracked mmCIF:
  - Models **365** residues over auth **140–518**, with one gap at **238–251**. Chain A models
    451 over 81–531 with no gap. **Chain B models no SH3 domain at all** — the SH3 domain
    starts at 81 — and its SH2 domain sits on the N-lobe rather than clamped on the C-lobe.
  - **Three of the twenty label residues are unmodelled** (Ile521, Val525, Leu529) and are
    reported as `unmapped`. Chain A loses none.
  - The myristoyl pocket is genuinely empty: nearest ligand heavy atom **16.0 Å**. Chain A's
    myristate contacts 16 of the 20 labels at 3.29 Å.
  - The coordinates are a rigid-body placement, and the depositors say so in `_refine.details`:
    "only overall domain B-factors were applied to molecule B, whereas individual B-factors
    were refined for molecule A". Chain B carries **three** group B-factors; chain A carries
    3041 distinct values.
  - **22.89 Å** Cα RMSD to `5MO4`:A over 345 common residues. Read it with its decomposition:
    over the 239 Cα of the **kinase domain alone**, chain B fits the holo at **1.08 Å** against
    chain A's 1.00 Å. The 22.89 Å is the regulatory module and nothing else.
- Strict-C5 scope was measured and does not repair the mandated pair. Admitting only
  UniProt-derived kinase residues 261–512 of the same `1OPL`:A bytes gives 252 nodes and 17
  labels, and myristate still contacts 13 of them. The arm was removed on 2026-08-24 as a
  method-phase robustness question; the measurement stands (ADR 0010).
- The myristoyl pocket is **not cryptic**, and the literature says so: Paladini et al.
  (*eLife* 2024) describe `1M52` as having an "empty myristoyl binding pocket" with a
  straight αI helix; Wylie 2017 calls it "vacant". Asciminib transplants into every myristate-free
  apo candidate with ≤ 4 of 31 atoms clashing (`1M52`, `2G1T`, `2G2H`, `4WA9`). It is an
  allosteric site — label→active-site Cα distances of **10.6–29.3 Å** (mandated) and
  **10.8–30.1 Å** (corrected), per `frozen.json` — but a pre-formed cavity.

### Cardiac myosin (`5TBY` → `6C1H`) — fatal

- `6C1H` is **rat unconventional myosin-Ib** (Q05096) with rabbit skeletal actin (P68135)
  and calmodulin, cryo-EM 3.9 Å, ligands ADP and Mg only, all five in the **actin**
  nucleotide clefts (Mentes 2018, doi 10.1073/pnas.1718316115). It contains no mavacamten
  and no cardiac myosin. MYH7 vs MYO1B is 39.6 % identical — different gene, class and
  species. No label set can be derived. **Superseded as the holo on 2026-09-02**: the
  organisers sanctioned `9GZ2` in its place, and `9GZ2` does supply a label set.
- `5TBY` is a SWISS-MODEL homology model of the human sequence on a **tarantula** template
  (`3JBH`), rigid-body fitted; the entry records 20 Å and its source map `EMD-2240` is 28 Å
  (Alamo 2017). It is cited by challenge reference [23] (Anderson 2018), which explains the
  apo choice; `6C1H` has no such provenance anywhere in the challenge's bibliography.
  Clashscore 49.95 (2.2nd percentile), zero heteroatoms, no `refine` block, and 41 `covale`
  records at physically impossible distances down to 1.083 Å. Note that RCSB does classify it
  `structure_determination_methodology: experimental`, so argue from those measurements and
  not from the label. It is a model built on a model (`3JBH` is itself a 20 Å EM-docked model).
- Mavacamten's chemical component ID is **`XB2`**. It appears in exactly six PDB entries:
  `8QYQ`, `8QYR` (bovine, X-ray, Auguin 2024 doi 10.1038/s41467-024-47587-9), `9GZ1`,
  `9GZ2` (human, cryo-EM), `9YP9`, `9YR7` (human, cryo-EM).
- The site is reproducible across all six copies: **Tyr164, Thr167, Asp168, His666, Pro710,
  Asn711, Arg712, Ile713, Glu774** in every one, plus Arg721, Tyr722, Leu770 in most.
  Minimum Cα distance from a label to the active site is 13.3 Å (`8QYP`), 16.5 Å (`9GZ3`)
  and 18.3 Å (`9YRG`), maxima 31.0–35.6 Å — genuinely distal in every arm.
- Corrected pair: **`9GZ3` → `9GZ2`** (human MYH7, identical construct and primed state,
  764 modelled residues each, identical modelled range 3–796, identical gaps, identical
  Mg·ADP·Pi state, differing by mavacamten and nothing else). Two alternatives were surveyed
  and are re-addable in the method phase: `8QYP` → `8QYR` (bovine Q9BE39; the holo is 1.80 Å,
  the highest-resolution mavacamten structure) and `9YRG` → `9YR7` (the human folded-back
  interacting-heads motif `5TBY` was trying to model, but a Myosin-7/GCN4/EGFP chimera in a
  six-chain assembly).

### c-Myc (`1NKP`)

- Myc/Max heterodimer on DNA: 4 DNA chains, two copies of the dimer. The chain/copy, canonical
  mapping, node set, source semantics, output contract and evaluation were unresolved and
  blocked Phase 2 under ADR 0020. **They were settled on 2026-09-02 by
  [ADR 0036](adr/0036-cmyc-is-a-reported-deliverable-scored-against-nmr-segments.md)**, which
  supersedes 0020.
- **Identifier-space collision, and it is a real bug source.** In **author** numbering chains
  `A` and `D` are c-Myc, `B` and `E` are Max, and `F`, `G`, `H`, `J` are the four DNA strands.
  In `label_asym_id` space, **`A` to `D` are the DNA strands.** A parser that resolves "chain A"
  without declaring its space loads DNA or protein depending on the library. The manifest
  declares `identifier_space: auth`.
- Numbering hazard recorded now: the two Myc copies carry **different arbitrary offsets**.
  Measured from the deposited `_struct_ref_seq` on 2026-09-02: chain A **900–981** and chain D
  **500–581** both map to UniProt P01106 **353–434**, so the offsets are **+547** and **+147**.
  Any hit list must be reported in canonical MYC numbering, not author numbering.
- ⚠️ corrected: the *modelled* ranges are 897–984 (chain A) and 499–581 (chain D), and they are
  **not** the native content. Chain A carries a `GHM` expression-tag remnant at 897–899 and an
  engineered C-terminal `GGC` at 982–984. **The native c-Myc content is exactly 82 residues.**
  An earlier version of this line gave the modelled range and the UniProt range as if they
  matched; 88 author positions cannot map onto 82 UniProt positions.

---

## Extra targets (generalisability)

The challenge encourages additional targets from the **Allosteric Database (ASD)**
[25]. Candidates get added here with the same apo/holo table structure once Phase 1
tooling makes adding a target cheap.
