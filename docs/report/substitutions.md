# Every structure we use that differs from `CHALLENGE.md` Table 1, and why

**Who asked for this page.** The organisers, on 2026-09-02:

> "Please always document the substitution you make and explain rational of why you did it."

Their sentence was an answer about cardiac myosin, and its wording is general. This page is
the general answer. Read it before any per-target result.

**What counts as a substitution here.** One thing only: a structure a scored arm reads in
place of the one Table 1 names. An *extra* arm on a different structure is not a substitution,
because the mandated arm still runs and still reports. The two cases are separated below,
because conflating them would overstate how far we departed from the assignment.

**Authority.** Where the organisers' answers and `CHALLENGE.md` disagree, the answers win.
They are transcribed verbatim in
[`../benchmark/review/00-official-reply.md`](../benchmark/review/00-official-reply.md).

---

## 1. What Table 1 asks for, and what runs

| Target | Table 1 apo | Table 1 holo | What runs | Substituted? |
| --- | --- | --- | --- | --- |
| KRAS G12C | `4OBE` | `6OIM` | `4OBE`:A → `6OIM`:A | no |
| BCR-ABL1 | `1OPL` | `5MO4` | `1OPL`:**B** → `5MO4`:A | **chain only** |
| Cardiac myosin | `5TBY` | `6C1H` | `5TBY`:A → **`9GZ2`**:A | **yes, holo** |
| c-Myc | `1NKP` | — | `1NKP`:A, no holo member | no |

Two rows depart from the table. Both are documented below. No other scored arm reads a
structure Table 1 does not name.

---

## 2. Substitution 1 — cardiac myosin holo: `6C1H` → `9GZ2`

**What is wrong with `6C1H`.** It is not human cardiac myosin and it does not contain
mavacamten. The entry is rat unconventional **myosin-Ib** (UniProt Q05096) with rabbit actin
(P68135) and calmodulin (P0DP23), a 3.9 Å cryo-EM structure titled "…Actin-bound Myosin
States…". Its only heteroatoms are ADP and Mg. Mavacamten is PDB chemical component `XB2`,
and `XB2` appears in exactly six entries — `8QYQ`, `8QYR`, `9GZ1`, `9GZ2`, `9YP9`, `9YR7` —
none of them `6C1H`. **No label set for the human MYH7 mavacamten site can be derived from
it**, so the arm had no positive class at all.

**Why `9GZ2`.** The organisers named it:

> "To better represent the human MYH7-mavacamten complex for this challenge, you may
> substitute 9GZ2 for 6C1H."

It is human MYH7 with `XB2` bound, 2.9 Å cryo-EM. Transferring its ligand contacts onto
`5TBY` chain A returns **every** mavacamten-contact residue, none unmapped, all inside
the node set. Deciding record: [ADR 0031](../adr/0031-expose-5tby-as-a-reported-arm-with-both-defects-measured.md).

**What this does not repair.** The apo half of the assignment is unchanged and remains
defective. `5TBY` is a SWISS-MODEL homology model on a tarantula template (`3JBH`),
rigid-body fitted and deposited at 20 Å, with zero heteroatoms. Two consequences are measured
and printed beside every number the arm produces:

- **The contact graph is largely invented.** Against the 3.4 Å cryo-EM `9GZ3`, over 761
  shared residues at the frozen 4.5 Å cutoff, the long-range (sequence separation ≥ 5)
  contact **Jaccard is 0.471** and recall is 0.569. The fold is right — pairwise Cα distances
  agree at Spearman 0.972–0.974, median absolute difference 1.95–2.08 Å — and the graph is not.
- **There is no ligand-derived propagation source**, because the entry has no ligands. The
  source comes from a myosin family motif triple (`GESGAGKT`, `N..SSRFG`, `DI.GFE`), which
  agrees with the ligand-derived source at Jaccard 0.48–0.52 with a 5.9 Å centroid offset on
  the two entries where that truth exists.

The arm is therefore **reported and non-confirmatory**. It contributes no statistical decision.

**One further mismatch, declared not repaired.** `5TBY` deposits the hexameric
interacting-heads motif and `9GZ2` is monomeric, so the two members model different oligomeric
states. No repair exists inside this arm: the challenge fixes the apo and the organisers fixed
the holo, and every human MYH7-mavacamten complex in the PDB is a single head.

---

## 3. Substitution 2 — BCR-ABL1 input: `1OPL` chain A → `1OPL` chain B

**Not an accession change.** The same deposited file is read. The organisers designated the
chain:

> "To ensure equal starting conditions, all non-protein residues and ligands must be
> uniformly stripped. I would suggest teams use Chain B as the input, as its native lack of
> myristate best fulfills the requirement to use the unbound apo structure."

**Why the repository agrees, having measured both.** Chain A holds `MYR` **in the myristoyl
pocket**: myristate contacts 16 of the 20 label residues, nearest approach 3.29 Å. The
mandated apo is holo at the site it is asked to predict. Chain B's nearest ligand atom is
16.0 Å away. Under this repository's own pair definition, clause (iii), chain A fails and
chain B passes. Deciding record:
[ADR 0029](../adr/0029-bcr-abl1-uses-the-designated-chain-b-as-a-reported-arm.md).

**What it costs, stated because a reader will find it.** Four defects are printed beside every
number this arm produces:

1. **No SH3 domain is modelled**, and the SH2 domain sits on the N-lobe rather than clamped on
   the C-lobe. Eleven of eleven interface residue counts confirm the inversion.
2. **The coordinates are a rigid-body placement.** The depositors say so in `_refine.details`:
   "only overall domain B-factors were applied to molecule B, whereas individual B-factors
   were refined for molecule A". Chain B carries three group B-factors against chain A's 3041
   distinct values.
3. **22.89 Å Cα RMSD to the holo `5MO4`:A** over 345 common residues. **Read this with its
   decomposition:** over the 239 Cα of the kinase domain alone, chain B fits the holo at
   **1.08 Å**, against chain A's 1.00 Å. The 22.89 Å is the regulatory module and nothing else.
4. **Three of the twenty label residues are not modelled** in chain B (against zero in chain A)
   and are reported as unmapped.

The arm is **reported and non-confirmatory**.

**A scope statement follows, and it is not about this arm.** For an allosteric site that works
by a conformational switch, no apo structure carries the coupled conformation, because carrying
it is what binding causes. An exhaustive survey of every PDB entry modelling more than the ABL
kinase domain returns six: every entry with the SH3–SH2 clamp docked has the myristoyl pocket
filled (5 of 5), and every entry with the pocket empty has the SH2 domain on the N-lobe
(2 of 2). Any apo-input benchmark on a switch-type site inherits this.

---

## 4. Additional arms, which are not substitutions

For each of the three scored disease areas the benchmark carries a **second** arm on the same
protein and the same site, with the one defect of the mandated pair repaired. The mandated arm
still runs and still reports. The purpose is to separate "the method failed" from "the input
was wrong", which a single defective arm cannot do.

| Added arm | Reads | Replaces which defect |
| --- | --- | --- |
| `kras_g12c_corrected` | `4LDJ`:A → `6OIM`:A | `4OBE` residue 12 is **GLY**, not CYS: `_struct_ref_seq_dif` lists no mutation and RCSB reports `rcsb_mutation_count = 0`. The holo `6OIM` is G12C with a `covale` bond from `A/CYS12.SG` to the drug at 1.805 Å. The mandated apo lacks the cysteine the holo drug is bonded to. `4LDJ` is the same study, same release date (doi:10.1073/pnas.1404639111), 1.15 Å, and is actually G12C |
| `bcr_abl1_corrected` | `2G2H`:A → `5MO4`:A | Myristate-free, X-ray, and in the holo's own numbering. Its `P16` is 16.27 Å from the label set and contacts none of it |
| `cardiac_myosin_corrected` | `9GZ3`:A → `9GZ2`:A | The cleanest pair in the benchmark: same construct, same primed pre-powerstroke state, same Mg-ADP-Pi, differing by mavacamten and nothing else |

**The three `corrected` arms are the confirmatory family.** Every statistical decision in the
submission is made on them, under Holm correction at α = 0.05. The mandated arms are reported
beside them and carry no decision. That split was frozen before any method existed (ADR 0003),
so it cannot have been chosen to suit a result.

---

## 5. c-Myc, which needed no substitution and has no holo member

`1NKP` runs as named. It has no substitution because no replacement would help: **no deposited
structure anywhere shows a drug-like small molecule bound to human c-Myc.** Across all 25
human c-Myc PDB entries the complete non-polymer inventory is `K`, `CL`, `CA`, `SO4`, `GOL`,
`EDO`, `TRS` and `PTD` — salts, cryoprotectants, buffer and crosslinker.

The arm therefore has no holo-derived label set. It is scored against NMR chemical-shift
segments with a hypergeometric null, it is **declared non-blind**, and it enters no
confirmatory family. Deciding record:
[ADR 0036](../adr/0036-cmyc-is-a-reported-deliverable-scored-against-nmr-segments.md).

`6G6K` is recorded as the cleaner alternative — 1.35 Å, DNA-free, no artificial disulfide
tether — and is **not** substituted. Better coordinates do not make a scoreable arm when the
missing thing is a ligand.

---

## 6. Provenance

Every accession named here is pinned by version and by SHA-256 of its decompressed mmCIF, in
`docs/benchmark/primary/manifest.yaml` under `structure_provenance`. `6C1H` stays in the
tracked structure store although no arm reads it, because it is the evidence for §2.
`uv run allo benchmark verify --set all` re-derives every frozen value from those files.
