# Validation targets

Source: `CHALLENGE.md` §6, Table 1. Four targets are the **minimum submission set**.

| Target | Disease area | Class | Apo (input) | Holo (ground truth) | Pocket to find |
|---|---|---|---|---|---|
| KRAS G12C | Oncology | GTPase | `4OBE` | `6OIM` | cryptic Switch-II pocket, locked by sotorasib (AMG 510) [18,19] |
| BCR-ABL1 | Oncology | tyrosine kinase | `1OPL` | `5MO4` | distal myristoyl pocket, used by asciminib [20,21] |
| Cardiac myosin | Cardiology | motor protein | `5TBY` | `6C1H` | mechanical site where mavacamten stabilises the super-relaxed state [22,23] |
| c-Myc (stretch) | Oncology | transcription factor | `1NKP` | — | none characterised; judged by consensus + docking viability [24] |

Bracketed numbers are reference indices in `CHALLENGE.md` §10.

---

## Ground-truth policy (non-negotiable)

**Ground-truth allosteric residues are derived programmatically from the holo
structure. They are never hand-typed from memory or from a paper's figure.**

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
Regenerate with `uv run allo benchmark show`. Full dossiers: `docs/benchmark/audit/`.
The audit found that **all three challenge-assigned pairs are defective**, one fatally;
the frozen benchmark and the corrected pairs are in `docs/benchmark/`.

| Pair | Verdict | The finding |
|---|---|---|
| KRAS `4OBE` → `6OIM` | usable with caveats | `4OBE` is **wild-type** KRAS (Gly12), not G12C |
| BCR-ABL1 `1OPL` → `5MO4` | not blind | `1OPL` carries myristate **in the target pocket**; apo and holo are the same conformation (1.00 Å) |
| Cardiac myosin `5TBY` → `6C1H` | **unscoreable** | `6C1H` is rat myosin-Ib + actin, no mavacamten; `5TBY` is a 20 Å homology model |

### KRAS G12C (`4OBE` → `6OIM`)

- `4OBE`: X-ray 1.24 Å, chains A and B, GDP + Mg only, `_struct_ref_seq_dif` lists **no
  mutation** — residue 12 is GLY in both chains. `6OIM`: G12C **plus** C51S/C80L/C118S,
  sotorasib as comp `MOV`, covalently linked `CYS12.SG–MOV303.C25`. 166/170 identical.
- Numbering: both auth 1–169 ↔ UniProt P01116 1–169, **offset 0**.
- Nucleotide state: GDP·Mg in apo and holo. Kept as a simple node or dropped — see the ADR.
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
  residues and **0.50 Å** across the pocket lining — there is no conformational change to predict.
- ⚠️ resolved: the numbering offset between the two entries is **zero**. Both use ABL1
  **isoform 1b** numbering (gatekeeper 334, DFG 400–402). The hazard is real but sits
  elsewhere: `1OPL`'s deposited `_struct_ref_seq` wrongly claims auth = UniProt, so
  normalising through that record shifts it by 19. SIFTS corrects it. The ABL corpus is
  split between 1a and 1b conventions (`2G1T`, `2HYY`, `4WA9`, `1M52` are 1a), so the
  convention is resolved **per entry**, never assumed.
- `5MO4` is a **ternary** complex: asciminib (`AY7`) in the myristoyl pocket **and** nilotinib
  (`NIL`) in the ATP site, on a T334I/D382N background. The holo is not singly liganded.
- ⚠️ corrected: `5MO4` is **not** kinase-domain-only. It models auth 83–531 continuously —
  SH3, SH2 and kinase, the same architecture as `1OPL`. The alignment step does not break.
- `1OPL` quality: 3.42 Å, R-free 0.315, 22.2 % RSRZ outliers (0.4th percentile). Chains A
  and B differ by 23 Å globally; chain B lacks the myristate and the αI helix.
- The myristoyl pocket is **not cryptic**, and the literature says so: Paladini et al.
  (*eLife* 2024) describe `1M52` as having an "empty myristoyl binding pocket" with a
  straight αI helix; Wylie 2017 calls it "vacant". Asciminib transplants into every myristate-free
  apo candidate with ≤ 4 of 31 atoms clashing (`1M52`, `2G1T`, `2G2H`, `4WA9`). It is an
  allosteric site — 12–30 Å from the ATP site — but a pre-formed cavity.

### Cardiac myosin (`5TBY` → `6C1H`) — fatal

- `6C1H` is **rat unconventional myosin-Ib** (Q05096) with rabbit skeletal actin (P68135)
  and calmodulin, cryo-EM 3.9 Å, ligands ADP and Mg only, all five in the **actin**
  nucleotide clefts (Mentes 2018, doi 10.1073/pnas.1718316115). It contains no mavacamten
  and no cardiac myosin. MYH7 vs MYO1B is 39.6 % identical — different gene, class and
  species. No label set can be derived.
- `5TBY` is a SWISS-MODEL homology model of the human sequence on a **tarantula** template
  (`3JBH`), rigid-body fitted; the entry records 20 Å and its source map `EMD-2240` is 28 Å
  (Alamo 2017). It is cited by challenge reference [23] (Anderson 2018), which explains the
  apo choice; `6C1H` has no such provenance anywhere in the challenge's bibliography. Clashscore 49.95
  (2.2nd percentile). It is a model of a model, not an experimental structure.
- Mavacamten's chemical component ID is **`XB2`**. It appears in exactly six PDB entries:
  `8QYQ`, `8QYR` (bovine, X-ray, Auguin 2024 doi 10.1038/s41467-024-47587-9), `9GZ1`,
  `9GZ2` (human, cryo-EM), `9YP9`, `9YR7` (human, cryo-EM).
- The site is reproducible across all six copies: **Tyr164, Thr167, Asp168, His666, Pro710,
  Asn711, Arg712, Ile713, Glu774** in every one, plus Arg721, Tyr722, Leu770 in most.
  Minimum Cα distance from a label to the active site is 13.3 Å (`8QYP`), 16.5 Å (`9GZ3`)
  and 18.3 Å (`9YRG`), maxima 31.0–35.6 Å — genuinely distal in every arm.
- Corrected pair: **`9GZ3` → `9GZ2`** (human MYH7, identical construct and primed state,
  764 modelled residues each, differing only by the drug). Sensitivity arms: `8QYP` → `8QYR`
  (bovine; the holo is 1.80 Å, the apo 2.76 Å) and `9YRG` → `9YR7` (experimental human
  folded-back off state — the interacting-heads motif `5TBY` was trying to model; single
  study, construct-identical, 0.88 Å core RMSD at 100 % identity).

### c-Myc (`1NKP`)

- Myc/Max heterodimer on DNA: 4 DNA chains, two copies of the dimer. Not addressed in this
  phase; the target is the final stage.
- Numbering hazard recorded now: the two Myc copies carry **different arbitrary offsets** —
  chain A auth 897–984 and chain D auth 499–581 both map to UniProt P01106 353–434. Any hit
  list must be reported in canonical MYC numbering, not author numbering.

---

## Extra targets (generalisability)

The challenge encourages additional targets from the **Allosteric Database (ASD)**
[25]. Candidates get added here with the same apo/holo table structure once Phase 1
tooling makes adding a target cheap.
