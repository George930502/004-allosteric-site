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

## Per-target facts to establish in Phase 1

Everything below is an open item to resolve *from the actual files*, not an assertion.
Record answers here with the code path that produced them.

**All targets**
- Chain selection and catalytic-domain residue range (C5: catalytic domains only).
- Whether the deposited structure has gaps, alternate conformations, or multiple
  copies in the asymmetric unit — and which copy we use.
- **Active-site definition** — the propagation source. Needs a defensible, apo-only
  rule per target (e.g. nucleotide-binding residues from the apo structure's own
  ligand, or a conserved catalytic motif). This choice materially drives the ranking;
  it deserves an ADR.

**KRAS G12C (`4OBE` → `6OIM`)**
- Nucleotide state of the apo structure and whether the nucleotide is kept as a simple
  node or dropped (C5).
- Sotorasib chemical component ID in `6OIM`; it is covalently bound to Cys12 — confirm
  the covalent linkage is handled correctly by the contact selection.

**BCR-ABL1 (`1OPL` → `5MO4`)**
- ⚠️ `1OPL` is the autoinhibited c-Abl structure and is reported to carry an
  N-terminal myristoyl group occupying the myristoyl pocket. **Verify this against the
  file.** If the pocket is occupied in our "apo" input, decide and document the
  treatment (drop the myristoyl as an excluded modification per C5, and check whether
  the resulting network still hides the pocket — otherwise the prediction is not blind
  in spirit even if it is in letter). This is the most important correctness question
  in the target set.
- Domain content of `1OPL` (SH3, SH2, kinase) vs. `5MO4` (kinase domain only) — the
  alignment step in the ground-truth pipeline must handle the mismatch.

**Cardiac myosin (`5TBY` → `6C1H`)**
- Large structure; likely needs coarse-graining before any quantum treatment. Record
  the residue count early, since it sets the Phase 4 compression requirement.
- Light chains present? Included or excluded, and why.

**c-Myc (`1NKP`)**
- Myc/Max heterodimer bound to DNA. DNA is not protein: exclude, or model as simple
  nodes (C5) — decide and document.
- Largely helical/disordered coiled coil; the contact network will look nothing like a
  globular domain. Expect the method to behave differently and say so in the report
  rather than quietly reporting a number.

---

## Extra targets (generalisability)

The challenge encourages additional targets from the **Allosteric Database (ASD)**
[25]. Candidates get added here with the same apo/holo table structure once Phase 1
tooling makes adding a target cheap.
