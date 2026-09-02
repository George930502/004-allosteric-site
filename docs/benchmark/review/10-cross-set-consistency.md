# Cross-set consistency: are the primary and secondary sets built by the same rules?

**Question.** The two frozen input sets must be aligned on both axes — horizontally, so every
arm inside a set is treated alike, and vertically, so a number from one set is comparable with
a number from the other.

**Answer.** The machinery is genuinely shared and the parameters are identical. Four
divergences remain. Two are known and disclosed, and two are not recorded anywhere.

Everything below is re-derived from the frozen artifacts. Reproduce with
`scratchpad/probe/clause_matrix.py` and `scratchpad/probe/clause_ix.py`.

---

## 1. What is genuinely identical

| | primary | secondary |
| --- | --- | --- |
| contact cutoff | 4.5 A | 4.5 A |
| cutoff sensitivity | 4.0, 5.0 | 4.0, 5.0 |
| atom selection | heavy | heavy |
| model | 1 | 1 |
| derivation code | `allo.benchmark.derive` | the same function |
| evaluation layer | protocol version 2 | the same protocol, same 14 arms |

One `derive`, one cutoff, one evaluation protocol over all fourteen arms. This is the part
that makes a cross-set comparison possible at all, and it holds.

---

## 2. Clauses (i)-(viii) — measured on all fourteen arms

| Arm | (iii) site-apo | (iv) identity | (v) assembly | (vii) labels removed |
| --- | --- | ---: | --- | ---: |
| `kras_g12c_mandated` | pass | 0.9759 | pass | 5 |
| `kras_g12c_corrected` | pass | 0.9820 | pass | 5 |
| `bcr_abl1_mandated` | **FAIL** — 20 of 20 labels contacted, nearest 3.29 A | 0.9977 | pass | 0 |
| `bcr_abl1_corrected` | pass | 0.9921 | pass | 0 |
| `cardiac_myosin_corrected` | pass | 1.0000 | pass | 0 |
| `mkp5` | pass | 1.0000 | pass | 1 |
| `chk1` | pass | 1.0000 | pass | 0 |
| `ptp1b` | pass | 1.0000 | pass | 0 |
| `smyd3` | pass | 0.9976 | pass | 0 |
| `glucokinase` | pass | 1.0000 | pass | 0 |
| `hiv_rt` | pass | 1.0000 | pass | 0 |
| `ns5b` | pass | 1.0000 | pass | 0 |
| `p97_vcp` | pass | 1.0000 | pass | 0 |
| `ecoli_cps` | pass | 0.9981 | pass | 0 |

Exactly one arm fails a clause that binds both sets, and it is the challenge's own mandated
BCR-ABL1 pair. Identity runs 97.6-100 %, so clause (iv)'s 90 % floor never binds.

---

## 3. Clauses (ix)-(xii) applied to the primary set as well

The repository applies these four only to the secondary set, because a selection rule needs a
pool. Applying them anyway is the horizontal-consistency check.

### Clause (ix), single-chain lining — **passes on all fourteen arms**

Measured at 4.5 A from the effector heavy atoms to every protein chain present.

| Arm | holo | assembly composition | lining chains | lining residues |
| --- | --- | --- | --- | ---: |
| both KRAS arms | `6OIM:A` | monomer | A only | 21 |
| both ABL1 arms | `5MO4:A` | monomer | A only | 20 |
| `cardiac_myosin_corrected` | `9GZ2:A` | monomer | A only | 12 |
| `hiv_rt` | `1VRT:A` | heterodimer, both chains deposited | **A only** | 16 |
| `p97_vcp` | `5FTJ:A` | hexamer, six chains deposited | **A only** | 17 |
| `ecoli_cps` | `1T36:A` | 4+4, eight chains deposited | **A only** | 19 |
| all other secondary arms | — | monomer | A only | 11-19 |

The three oligomeric arms deposit their full assembly in the asymmetric unit, so this
measurement is not the false pass the repository warns about. No interface site is hiding in
any arm of either set.

### Clause (xi), structure admission — **one failure, and it is a primary arm**

X-ray <= 2.5 A or cryo-EM <= 4.0 A, applied to both members of every arm.

| Entry | method | resolution | admits |
| --- | --- | ---: | --- |
| `1OPL` | X-ray | **3.42 A** | **no** |
| every other entry in either set | X-ray or cryo-EM | 1.15-3.40 A | yes |

`1QUV` passes at exactly 2.50 A. `9GZ3` at 3.4 A passes on the cryo-EM ceiling. This confirms
what `secondary/README.md` §5.2 Axis B already records, now measured across both sets in one
pass.

### Clause (xii), redundancy — **passes at family level, fails at rule level**

No two arms share a Pfam family. But the *propagation-source rule* is shared across the two
sets:

| Source rule | Arms using it | Sets |
| --- | --- | --- |
| `{from_motifs: [VAIK, HRD, DFG]}` | `bcr_abl1_mandated`, `bcr_abl1_corrected`, **`chk1`** | primary **and** generalisation |
| `{from_motifs: [PTP]}` | `mkp5`, `ptp1b` | development, twice |

`chk1` sits in the `generalisation` tier, which carries the across-target claim. Its active
site is located by the identical rule that locates BCR-ABL1's. Family-level disjointness is
achieved and rule-level disjointness is not. **This is recorded nowhere in the repository.**

It is a bounded problem — the rule is a sequence-motif regex, not a fitted parameter, so no
information flows from one arm to another — but a reviewer asking "is the generalisation set
really independent?" will find it, and the answer should be written before they do.

### Clause (x), apo occupant — passes on all fourteen

`scoreable_labels_contacted` is 0 on every arm except `bcr_abl1_mandated`, which is the
clause (iii) failure above.

---

## 4. The divergence the organisers' reply makes urgent

**Seven of fourteen arms locate the active site from a ligand in the apo entry.**

| `{from_ligands: ...}` — 7 arms | `{from_motifs: ...}` — 7 arms |
| --- | --- |
| `kras_g12c_mandated` (GDP, MG) | `bcr_abl1_mandated` (VAIK, HRD, DFG) |
| `kras_g12c_corrected` (GDP, MG) | `bcr_abl1_corrected` (VAIK, HRD, DFG) |
| `cardiac_myosin_corrected` (ADP, MG, PO4) | `mkp5` (PTP) |
| `smyd3` (SAM) | `chk1` (VAIK, HRD, DFG) |
| `glucokinase` (GLC) | `ptp1b` (PTP) |
| `p97_vcp` (ADP) | `hiv_rt` (POLA, YXDD) |
| `ecoli_cps` (ADP, MN, PO4) | `ns5b` (GDD) |

The organisers wrote that "all non-protein residues and ligands must be uniformly stripped".
The repository strips them from the node set on every arm. It still uses the stripped
ligand's **coordinates**, once, to say where the catalytic site is.

Under the narrow reading of that sentence nothing changes. Under the wide reading, **half the
benchmark needs a new source rule**. The split is exactly 7 and 7, and it cuts across both
sets and both tiers, so no partial fix is available.

**Recommendation.** Report the source rule per arm in the submission, and run a motif-only
sensitivity arm on KRAS, where the P-loop is a single unique PROSITE PS00016 match at
residues 10-17. That converts the ambiguity into a measurement.

---

## 5. Two documentation errors found by re-deriving

The repository's rule is that numbers come from code. These two do not.

**`primary/README.md` §4a says "three of the five sit in different space groups".** Its own
table shows two differing and one not applicable. Read from the deposited bytes:

| Arm | apo space group | holo space group | differ |
| --- | --- | --- | --- |
| `kras_g12c_mandated` | `C 1 2 1` | `P 21 21 21` | **yes** |
| `kras_g12c_corrected` | `P 21 21 21` | `P 21 21 21` | no |
| `bcr_abl1_mandated` | `C 2 2 21` | `C 2 2 21` | no |
| `bcr_abl1_corrected` | `P 21 21 2` | `C 2 2 21` | **yes** |
| `cardiac_myosin_corrected` | `P 1` (cryo-EM placeholder) | none deposited | not applicable |

Two, not three. A cryo-EM entry's `P 1` is a placeholder, not a crystal form.

**`primary/README.md` §4a also says the six secondary arms below 0.3 A "share a space group
in five of six".** Measured, one of those six — `p97_vcp` — is a cryo-EM pair, so it has no
crystal form and cannot share one. Of the **five crystallographic** pairs, **three** share a
space group (`chk1`, `ptp1b`, `hiv_rt`) and two do not: `mkp5` (`P 1` against `P 64`) and
`ns5b` (`P 43 21 2` against `P 21 21 2`).

Neither error changes a decision. Both are the kind a reader checks.

**A third, and this one is substantive.** `docs/targets.md` states that `5MO4` "models auth
83-531 continuously". It does not. Read from the deposited bytes, chain A holds **429
residues over 83-531 with two gaps: 296-297 and 402-419**, the second of them 18 residues
long. `5MO4` is the holo for **both** BCR-ABL1 arms. No label falls inside either gap — the
labels run 351-529 and the gap sits between 363 and 448 — so the label set is unaffected and
no frozen number moves. What moves is every statement about coverage, and the paired-residue
counts behind the superposition and RMSD figures.

---

## 6. What the two sets do not share, by design, and why it is right

| Property | primary | secondary | is the difference sound? |
| --- | --- | --- | --- |
| `tier` field meaning | `mandated` / `corrected` | `development` / `generalisation` | yes, and both READMEs warn about it |
| arm selection | mandated by `CHALLENGE.md` | twelve admission clauses over an RCSB frame | yes — a selection needs a pool |
| clauses (ix)-(xii) | not applied | applied | **partly.** Section 3 shows they can be applied, and one primary arm fails (xi) |
| effector class | 3 synthetic, 0 physiological | 9 synthetic, 0 physiological | consistent, and both sets share the gap |
| blindness | none blind, per-arm reason recorded | none blind, per-arm reason recorded | yes |

**The shared gap is worth stating once, loudly.** All fourteen arms use a synthetic
small-molecule effector. Classical allosteric enzymology — cooperativity and feedback
inhibition by a metabolite — is untested across the whole benchmark, and it is the oldest and
best-attested form of the phenomenon. `secondary/README.md` §5.2 records this for its own set.
It is true of the primary set as well and is recorded there nowhere.

---

## 7. Disposition

1. **Record clause-rule sharing.** `chk1` and both ABL1 arms use one source rule, across the
   primary set and the generalisation tier. Add it to `secondary/README.md` §7 as a
   thirteenth limitation.
2. **Apply clauses (ix)-(xii) to the primary set as a reported diagnostic**, not as an
   admission rule. Section 3 is the table; put it in `primary/README.md` §2.
3. **Correct the two space-group counts.**
4. **Move the synthetic-effector gap** from `secondary/README.md` §5.2 to
   `benchmark/README.md`, where it covers both sets.
5. **Decide the ligand-derived-source question** (section 4) before scoring. It is a
   conformance question, not a statistical one.
