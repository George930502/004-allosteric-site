# 0036 — c-Myc is a reported deliverable, scored against NMR segments and declared non-blind

**Status:** accepted · 2026-09-02 · **supersedes**
[ADR 0020](0020-cmyc-contract-must-precede-method-design.md) · clears the Phase 2 blocker on
`1NKP`

## Context

`1NKP` is one of the four minimum deliverables in `CHALLENGE.md` §6, and it has **no arm in
any freeze**. ADR 0020 blocked method design for it until its input and evaluation contract
was frozen. Nothing moved for nine days. The audit of 2026-09-02 named it, with
`cardiac_myosin_mandated`, as the largest open conformance gap.

The evidence base now exists:
[`../benchmark/evidence/cmyc-contract.md`](../benchmark/evidence/cmyc-contract.md). Four facts
decide the contract.

**1. The input is unambiguous once the chain collision is named.** `1NKP` is a 1.80 Å X-ray
ternary complex, space group `P 1`, with two independent copies of the c-Myc/Max heterodimer
on double-stranded DNA. In **author** numbering, chains `A` and `D` are c-Myc (P01106), `B`
and `E` are Max, and `F`, `G`, `H`, `J` are four 19-mer DNA strands. In `label_asym_id` space,
**`A` to `D` are the DNA strands.** The two identifier spaces overlap and denote different
molecules, so a parser that resolves "chain A" without declaring its space loads DNA or
protein depending on the library.

Chain A models auth 897–984 and chain D models auth 499–581. Both carry a `GHM` expression-tag
remnant and an engineered C-terminal `GGC`. **The native c-Myc content is exactly 82 residues
and is identical in both copies**: auth 900–981 in chain A, 500–581 in chain D.

**Corrected 2026-09-02, by reading the deposited file rather than a retrieved value.**
`_struct_ref_seq` of `1NKP` gives `A 900-981 <-> P01106 353-434` and `D 500-581 <-> P01106
353-434`. An earlier draft of this ADR wrote the UniProt span as 368–449. That is the same
82 residues expressed in the 454-residue **Myc-1** convention, 15 higher throughout, and it
was written without saying so. Use **353–434**, the canonical 439-residue convention, which is
also the convention the CSP literature uses.

**2. There is no positive class, and no structure will supply one.** Across all 25 human
c-Myc PDB entries the complete non-polymer inventory is `K`, `CL`, `CA`, `SO4`, `GOL`, `EDO`,
`TRS` and `PTD` — salts, cryoprotectants, buffer and crosslinker. **No deposited structure
anywhere shows a drug-like small molecule bound to human c-Myc.** All residue-level site
information comes from NMR chemical-shift perturbation and peptide truncation on the isolated,
disordered monomer.

**3. Nothing about c-Myc is allosteric in the sense this repository adopted.** The three
reported sites lie **inside** the Max dimerisation region, and Hammoudeh reports them as
"three discrete sites within the 85-residue bHLHZip domain" where binding is simultaneous and
independent. That is interface disruption, not a topographically distinct site conformationally
linked to a functional site. A Europe PMC search for MYC with allosteric and bHLHZip returned
no claim otherwise.

**4. The engineered tether is a property of this entry, not of the protein.** Sammak 2019
(doi:10.1021/acs.biochem.9b00296) names `1NKP` as "tethered by an artificial disulfide bridge
engineered by adding a cysteine residue at the C-terminus".

## Decision

**1. Produce the c-Myc deliverables, and produce them from `1NKP` chain A.** The challenge
names the accession and it is one of four minimum targets. Chain A carries the longer native
span and is the copy the contract pins. **Declare the identifier space in the manifest**, so
the collision cannot become a silent bug.

**2. Score the top-5 list against the CSP-derived segments, with a hypergeometric null over
the 82 native residues, and declare the arm non-blind.** Segments, in the 439-residue
literature convention with the derived chain A author numbering beside each:

| Site | literature (439-aa) | `1NKP` chain A author | compound |
| ---- | ------------------- | --------------------- | -------- |
| I    | 402–409             | 949–956               | 10058-F4 |
| II   | 366–375             | 913–922               | 10074-G5 |
| III  | 375–385             | 922–932               | 10074-A4 |

**The offset is now derived, not hand-computed.** `chain A auth = lit439 + 547` follows
directly from the deposited `_struct_ref_seq` row `A 900-981 <-> P01106 353-434`:
900 - 353 = 547, and 981 - 434 = 547 at the other end. Chain D's offset is 147 by the same
row. Pin both in the manifest and let a test re-derive them from the mmCIF. The Site I range is also inconsistent across secondary sources — 402–409 against the
widely repeated 402–412 — and both primary papers are paywalled. Freeze the narrower range and
record the discrepancy.

**3. The arm is descriptive and it is never confirmatory.** It enters no Holm family. It does
not pass through `score_arm`, because there is no label set derived from a holo structure and
no matched-patch null calibrated for it. Its statistic is an overlap count with an exact
hypergeometric p-value, and that is all it is.

**4. There is no propagation source, so the metric must be source-free.** c-Myc has no active
site. `CHALLENGE.md` §4.1 says connectivity "in most cases" to an active site, which is the
clause that admits this. The c-Myc deliverable uses a source-free scorer, declared before it
runs.

> **AMENDED 2026-09-02 by ADR 0037.** This decision named `allo.quantum.connectivity` as the
> source-free scorer. That module left `main` with the method layer and is on the branch
> `method-layer-archive`. **The requirement stands and its implementation does not exist on
> this branch.** Whatever source-free scorer Phase 2 builds must satisfy the rule above, and
> the rule is what this ADR froze, not the module.

**5. Do not use "consensus across winning teams" as a criterion of correctness.** It has no
precedent as a scientific evaluation standard, and its documented failure mode — correlated
errors between predictors that share inputs and machinery — is exactly the regime a challenge
with one shared input set and shared infrastructure creates. Report the consensus if the
organisers ask for it; never treat agreement as evidence of being right.

**6. Ask the organisers what "theoretical docking viability" means.** It is cheaper to ask
than to guess, and it is the one part of their stated c-Myc criterion that no reading here
makes concrete.

## Consequences

> **DECIDED, NOT BUILT.** `1NKP` is not in `primary/manifest.yaml` and the primary freeze
> holds six arms, none of them c-Myc. The bullets below describe the work this ADR
> authorises. Until it lands, the claim that all four minimum targets have an arm is a plan,
> not a fact, and no document may state it in the present tense.

- `1NKP` enters `primary/manifest.yaml` as a c-Myc arm with **no holo member**, an explicit
  `identifier_space: auth` field, and a `labels_from: literature_csp` rule rather than a ligand
  contact rule. It is excluded from every Holm family and from the evaluation freeze's
  matched-patch machinery.
- **All four minimum targets then have an arm.** The conformance gap the audit called largest
  is closed.
- **The arm is declared NON-BLIND, and that is now unavoidable.**
  `evidence/cmyc-contract.md` §2.2 transcribes the candidate site residues. Writing the
  evidence file is what removed blindness, and hiding that would be worse than losing it. It
  strengthens rather than weakens ADR 0020's requirement: the contract, evaluation included,
  is frozen here, before any c-Myc method is designed.
- **The number is not comparable to the three scored disease areas.** Different positive-class
  provenance, different null, different unit, no holo structure, and a target that is not
  allosteric in this repository's sense. The report says so beside the number, not in a
  footnote.
- `6G6K` is recorded as the cleaner alternative — 1.35 Å, DNA-free, no artificial disulfide
  tether — and **not** substituted. The organisers sanctioned documented substitution, but
  `1NKP` is the accession the challenge names and its defects do not prevent the deliverable.
- One correction to `docs/targets.md`: it gives the c-Myc range as 897–984 without saying that
  the span includes an expression-tag remnant and an engineered `GGC`, so modelled and native
  are conflated. The native content is 82 residues.

## Alternatives rejected

**Leave `1NKP` blocked.** Rejected: it is a minimum deliverable, the contract is now
writable, and "we could not decide" is not a result.

**Score by consensus across teams, as `CHALLENGE.md` suggests.** Rejected as a criterion of
correctness, for the reason in decision 5. It is reportable and it is not evidence.

**Treat c-Myc as a fifth confirmatory arm.** Rejected: no holo-derived label set, no
calibrated null, and a positive class read from a review article at ten-residue resolution. It
would import that uncertainty into a family that currently has none.

**Substitute `6G6K`.** Rejected: better coordinates do not make a scoreable arm, because the
missing thing is a ligand and no c-Myc entry has one. The gain would be cosmetic and the cost
would be departing from a named accession for no measured benefit.
