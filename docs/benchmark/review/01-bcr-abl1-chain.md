# BCR-ABL1: which `1OPL` chain, and what each one costs

**Question.** The organisers direct teams to `1OPL` chain **B**. The frozen
`bcr_abl1_mandated` arm uses chain **A**. Which is right?

**Answer in one line.** Chain B fixes the defect the repository found and breaks the
mechanism the challenge asks a method to find. Neither chain is a clean apo input, and the
reason is now measured rather than argued.

All numbers below come from `allo.benchmark.derive` and from direct measurement on the
deposited `1OPL` bytes. Reproduce with the probes named in section 7.

---

## 1. What each chain contains

| | chain A | chain B |
| --- | --- | --- |
| modelled residues | 451 | 365 |
| author range | 81-531, no gaps | 140-518, gap 238-251 |
| non-polymer components on the chain | `MYR`, `P16` | `P16` only |
| myristate in the myristoyl pocket | **yes** | **no** |
| SH3 domain modelled (84-138) | 55 residues | **0 residues** |
| SH2 domain modelled (146-236) | 91 residues | 91 residues |
| kinase domain modelled (254-512) | 259 residues | 259 residues |

The organisers' description of the ligand contents is correct. Chain A carries myristate and
the ATP-site inhibitor. Chain B carries the ATP-site inhibitor alone.

---

## 2. Clause (iii) — chain B passes, chain A fails

`derive` measures the apo occupancy of the site being predicted.

| Arm | labels contacted by an apo component | nearest label |
| --- | ---: | ---: |
| `1OPL:A` (frozen `bcr_abl1_mandated`) | **16 of 20** | 3.29 A |
| `1OPL:B` | **0 of 17** | 16.00 A |
| `2G2H:A` (frozen `bcr_abl1_corrected`) | 0 of 18 | 16.27 A |

On clause (iii) the organisers are right and the frozen arm is wrong. Chain B's myristoyl
pocket is empty.

---

## 3. What chain B costs — three measured losses

### 3.1 Three labels disappear

Chain B ends at residue 518. Labels 521, 525 and 529 are not modelled. The label set falls
from 20 to 17, and `derive` reports them as `unmapped`, not as absences.

| Arm | labels | scoreable | candidates | prevalence |
| --- | ---: | ---: | ---: | ---: |
| `1OPL:A` | 20 | 20 | 440 | 4.5 % |
| `1OPL:B` | 17 | 17 | 354 | 4.8 % |
| `2G2H:A` | 18 | 18 | 261 | 6.9 % |

### 3.2 The SH3-SH2 clamp is not assembled

Superpose the two chains on their kinase domains (254-512): the fit is **0.53 A over 259
Cα**. Then measure where the rest goes.

| After superposing the kinase domains | RMSD | max deviation |
| --- | ---: | ---: |
| SH2 domain, chain A against chain B | **70.07 A** | 101.3 A |
| kinase domain, chain A against chain B | 0.53 A | 3.8 A |

The kinase domains are the same. The SH2 domain is in a different place.

Measured directly, the SH2-kinase interface is a different interface in each chain:

| | SH2 packs against | kinase residues at the interface | of which are myristoyl-pocket labels |
| --- | --- | --- | ---: |
| `1OPL:A` | the **C-lobe** | 357, 358, 360, 361, 393, 394, 512 | **360 and 512** |
| `5MO4:A` (the holo) | the **C-lobe** | 357, 358, 360, 361, 393, 394, 512 | **360 and 512** |
| `1OPL:B` | the **N-lobe** | 258-263, 291, 294, 328, 329, 331 | **none** |

Centroid distances say the same thing. In chain A the SH2 centroid is 34.9 A from the C-lobe
centroid and 40.8 A from the N-lobe centroid. In chain B those numbers invert: 49.8 A and
28.2 A.

**Why this decides the question.** The myristoyl pocket is allosteric because myristate
binding remodels helix alpha-I, which creates the surface the SH3-SH2 unit docks onto, which
clamps the kinase off (Nagar 2003; Zhang 2010, doi:10.1038/nature08675). In chain A that
coupling is present in the coordinates, and two of its seven contacts are pocket-lining
residues. In chain B the coupling is absent: the SH3 domain is not modelled and the SH2
domain sits on the opposite lobe.

A method run on chain B is asked to find a site whose mechanism the input structure does not
contain. Its contact graph carries no edge from the myristoyl pocket to the regulatory
module.

**This is the same objection ADR 0010 raised against trimming `1OPL` to the kinase domain**,
reached by a different route. ADR 0010 declined the trim because it "deletes the SH3-SH2
clamp the myristoyl pocket acts through". Chain B deletes SH3 outright and moves SH2 off the
pocket face.

### 3.4 Chain B's coordinates were not independently refined, and the depositors say so

`_refine.details` in the deposited `1OPL` mmCIF, verbatim:

> "The structure was refined by superimposing the refined high resolution structure of c-Abl
> (pdb entry 1OPK) on the molecular replacement solution and optimizing positions of
> individual domains by rigid-body refinement. Following this, **only overall domain
> B-factors were applied to molecule B, whereas individual B-factors were refined for
> molecule A**."

Measured from the same bytes:

| | atoms | mean B | median B | range | **distinct B values** |
| --- | ---: | ---: | ---: | --- | ---: |
| `1OPL:A` | 3628 | 85.0 | 72.1 | 25.5-254.5 | **3041** |
| `1OPL:B` | 2954 | **170.7** | 161.2 | 160.8-198.1 | **3** |

Three distinct B-factors across 2954 atoms — one per rigid domain. The entry's overall
`_refine.B_iso_mean` is 123.3, and chain B sits well above it.

Chain B is therefore a **rigid-body placement of a higher-resolution model**, not coordinates
refined atom by atom against this 3.42 A density. Its residue-level contacts are properties
of `1OPK`'s geometry plus a domain placement. That is the same objection this repository
raises against `5TBY` (`02-cardiac-myosin.md` §3), reached here from the depositors' own
statement rather than from an inference.

Under C6, which makes contact topology the object the whole method rests on, this is the
single strongest argument against chain B.

### 3.3 State matching against the holo fails

| Pair | global Cα RMSD, all common residues |
| --- | ---: |
| `1OPL:A` against `5MO4:A` | **0.98 A** |
| `1OPL:B` against `5MO4:A` | **22.89 A** |
| `2G2H:A` against `5MO4:A` | 1.78 A |

Clause (v) requires the same oligomeric state and clause (viii) requires the functional state
to be stated. Chain A and the holo are the same assembled autoinhibited state. Chain B is not.

---

## 4. The graph is connected, so this is not a parsing failure

A displaced domain could leave the single-chain contact graph in pieces, which would break
propagation for a trivial reason. It does not.

| | nodes | components | mean degree | isolated nodes |
| --- | ---: | --- | ---: | ---: |
| `1OPL:A` | 451 | one, 451 | 9.28 | 0 |
| `1OPL:B` | 365 | one, 365 | 9.28 | 0 |

Chain B's SH2 domain reaches its own kinase N-lobe at 2.60 A with 76 heavy-atom contacts
below 4.5 A. The arrangement is intramolecular, not a lattice artefact: chain B's SH2 comes no
closer than 32.66 A to any atom of chain A.

---

## 5. The ligand-stripping instruction, and one thing it does not settle

> "all non-protein residues and ligands must be uniformly stripped"

The repository already complies. `allo.inputs.apo_input` returns a ligand-free, single-chain,
immutable view holding exactly the frozen node set. No method ever sees `MYR` or `P16`.

**The instruction does not say whether a stripped ligand may still locate the active site.**
Two frozen arms derive the propagation source from the apo entry's own cofactor —
`{from_ligands: [GDP, MG]}` on KRAS and `{from_ligands: [ADP, MG, PO4]}` on myosin. The
cofactor is not a node and not an edge. Its coordinates are used once, to say where the
catalytic site is.

Both readings are defensible:

- **Narrow.** "Stripped" scopes the node set. Locating the active site is a separate step, and
  `CHALLENGE.md` §4.1 requires connectivity "to an active site", so the site must be locatable
  somehow. Under this reading nothing changes.
- **Wide.** "Stripped" scopes every use of the coordinates. Under this reading KRAS and myosin
  need a sequence-motif source, as ABL1 already has.

BCR-ABL1 is unaffected either way: its source rule is `{from_motifs: [VAIK, HRD, DFG]}` and
uses no ligand.

**Recommendation.** Report the source rule for every arm in the submission, and report a
motif-only sensitivity arm for KRAS. The wide reading is then answered with a measurement
rather than an argument. It is cheap: KRAS's P-loop is a single unique PROSITE PS00016 match
at residues 10-17 (measured), which is inside the frozen ligand-derived source of 22-23
residues.

---

## 6. The trilemma, and what to do

No available ABL1 apo structure satisfies both requirements at once.

| Input | pocket empty (clause iii) | clamp present | state matches holo | labels | verdict |
| --- | --- | --- | --- | ---: | --- |
| `1OPL:A` | **no** — 16 of 20 labels contacted | yes | yes, 0.98 A | 20 | holo at the site it predicts |
| `1OPL:B` | yes | **no** — no SH3, SH2 on the wrong lobe | **no**, 22.89 A | 17 | mechanism absent |
| `2G2H:A` | yes | **no** — kinase domain only | yes, 1.78 A | 18 | mechanism absent, state right |

**Recommended disposition.**

1. **Add `1OPL:B` as a third arm and keep chain A.** The organisers designated chain B, so a
   submission that reports only chain A is not answering the instruction. Chain A is the
   literal Table 1 assignment and is what the challenge document names. Both are reported;
   neither is confirmatory.
2. **Keep `2G2H:A` as the confirmatory arm for this disease area.** It is the only ABL1 input
   that has an empty pocket and matches the holo state. Its cost — no clamp — is shared with
   chain B, so chain B buys nothing that `2G2H` does not already have, and loses the state
   match on top.
3. **Record the mechanism loss in the report.** On every ABL1 arm except chain A, the
   structural path from the myristoyl pocket to the SH3-SH2 clamp is absent from the input.
   That is a property of the available structures, not of any method, and it caps what this
   disease area can demonstrate.
4. **Open an ADR.** The chain choice is now a decision with an organiser instruction on one
   side and a measured mechanism loss on the other. It must be written down before any method
   is scored.

**Still open.** Whether any deposited ABL1 entry has SH3, SH2 and the kinase domain in the
assembled arrangement with the myristoyl pocket empty. An RCSB survey is running; if one
exists it supersedes all three rows above.

---

## 7. Reproduction

```
scratchpad/probe/abl_chainB.py    derive() for chain A, chain B and 2G2H
scratchpad/probe/abl_domains.py   domain-wise superposition
scratchpad/probe/abl_sh2.py       SH2-kinase interface residues per chain
scratchpad/probe/abl_graph.py     contact-graph components and degree
```

These are probes, not experiments. Nothing here is frozen. Promoting any of it to the freeze
needs a manifest change, an ADR and a re-run of `allo benchmark verify`.

---

## 8. Addendum: an exhaustive PDB survey, and the finding that outranks the rest

An RCSB survey of every entry modelling more than the ABL kinase domain (UniProt P00519,
P00520, P42684; 118 entities, plus a 70 % identity sequence search that added nothing)
returns **six** entries. The split is clean and it is mechanistic.

| Regulatory domains docked on the **C-lobe** | Myristoyl pocket |
| --- | --- |
| `1OPL:A`, `2FO0`, `1OPK` | filled with `MYR` |
| `5MO4`, `8SSN` | filled with asciminib |

| Regulatory domains present, SH2 on the **N-lobe** | Myristoyl pocket |
| --- | --- |
| `1OPL:B`, `4XEY:B` | **empty** |

Five for five, and two for two. **The clamp docks only when the pocket is filled.** The state
the benchmark wants — regulatory module assembled, pocket empty — is the state the switch
exists to prevent, so no deposited structure has it and none is likely to.

**This is not a defect in the benchmark or in the challenge. It is a property of the
biology**, and it generalises past this target: for an allosteric site that works by a
conformational switch, the apo structure does not carry the coupled conformation, because
carrying it is what binding causes. Any apo-input benchmark on a switch-type allosteric site
inherits this. It belongs in the report as a scope statement, not as a caveat on one arm.

**Independent confirmation of what chain B is.** Lorenz, Hantschel, Superti-Furga and Kuriyan
report that the `1OPL` crystal "contained two different conformational states ... (i) the
compact autoinhibited conformation ... and (ii) the extended conformation, for which only the
SH2 and kinase domains could be modeled and which was characterized by very high temperature
factors", and that the extended form "occurred fortuitously alongside the assembled,
myristoyl-bound state" (doi:10.1042/BJ20141492). Nagar 2003's own text could not be retrieved.

**A better structure for the same conformation exists.** If chain B's arrangement is to be
modelled at all, `4XEY:B` is strictly better coordinates for it:

| | resolution | B-factors | sequence | pocket residues modelled | RMSD to `5MO4:A` |
| --- | ---: | --- | --- | ---: | ---: |
| `1OPL:B` | 3.42 A | 3 group values | D382N (the HRD catalytic Asp) | 17 of 20 | 22.89 A |
| `4XEY:B` | **2.891 A** | **individual** | **wild type** | **18 of 20** | 23.03 A |

`1OPL:B` and `4XEY:B` are the same arrangement: 1.44 A global over 352 Ca, seven shared
N-lobe interface residues.

**Two corrections to the survey list used to reach this.** `8SSP` is Aurora kinase A, not
ABL1 — the ABL1 entry intended was `8SSN`. `9KS5` uses 1a numbering and deposits its covalent
ligand as a modified residue, so a non-polymer scan wrongly reports it as apo.

**Revised disposition, superseding section 6 item 1.**

Report `1OPL:B` because the organisers designated it, and mark it non-confirmatory with all
four defects printed beside it: no SH3, SH2 on the wrong lobe, 22.89 A from the holo, and
coordinates that were rigid-body placed with three group B-factors. Keep `2G2H:A` as the
comparison arm. Do **not** substitute `4XEY:B` for the organisers' choice — it is better
coordinates for a state that is wrong either way, and swapping an accession the organisers
named for one they did not is the move that needs the strongest reason, not the weakest.

Full survey: `data/abl1-apo-survey.md`.
