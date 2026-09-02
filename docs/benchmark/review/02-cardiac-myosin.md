# Cardiac myosin: what the organisers' answer fixes, and what it leaves broken

**Question.** The organisers permit `9GZ2` in place of `6C1H`. Does that make the mandated
cardiac-myosin arm scoreable, and does it clear ADR 0016?

**Answer in one line.** It clears the label-side blocker completely and leaves both
input-side blockers standing. Both are now measured rather than argued.

---

## 1. The label side is fixed, and completely

`transfer_labels(9GZ2:A, 5TBY:A, XB2, 4.5 A)` returns all twelve mavacamten-contact
residues, none unmapped, all inside the `5TBY` chain A node set:

```
164, 167, 168, 666, 710, 711, 712, 713, 721, 722, 770, 774
```

That is the same twelve residues as the frozen `cardiac_myosin_corrected` label set.
`5TBY` and `9GZ3` use the same author numbering, so no offset is involved.

ADR 0016 anticipated this: "An organiser-supplied correct holo structure would make labels
scoreable but would not, by itself, cure the two input-side blockers." That sentence is now
the operative one.

---

## 2. Input blocker 1 — no unique fold-general source rule

ADR 0016 forbids "a myosin-only motif added for this arm" and permits a rule that is
"fold-general" and "independently validated".

**The fold-general candidate fails on uniqueness.** PROSITE PS00016, the ATP/GTP-binding
site motif A, is `[AG]-x(4)-G-K-[ST]`. `allo.inputs.active_site` requires exactly one match.

| Entry | PS00016 matches |
| --- | --- |
| `4OBE:A`, `4LDJ:A` (KRAS) | 1 — `GAGGVGKS`, residues 10-17 |
| `9GZ3:A`, `9GZ2:A`, `5TBY:A` (MYH7) | **2** — `AETEYGKT` at 61-68 and `GESGAGKT` at 178-185 |

The rule raises on myosin. Forced through by taking both matches, the source centroid lands
**13.50 A** from the ligand-derived centroid on `9GZ3`, because 61-68 is not near the
nucleotide site.

**A family-level rule does work, and is validated.** `GESGAGKT` (P-loop), `N..SSRFG`
(switch I) and `DI.GFE` (switch II) each match exactly once in MYH7 and zero times in KRAS,
ABL1 or the two ABL1 apo entries. Validated against the ligand-derived source on the two
entries where that truth exists:

| Entry | ligand source | motif source | overlap | Jaccard | centroid offset |
| --- | ---: | ---: | ---: | ---: | ---: |
| `9GZ3:A` | 21 | 22 | 14 | 0.483 | **5.96 A** |
| `9GZ2:A` | 25 | 22 | 16 | 0.516 | **5.92 A** |

Read this honestly. A family motif triple **is** available, and it is the same kind of object
as the five rules already in `CATALYTIC_MOTIFS` — `PTP` is PROSITE PS00383, `POLA` and
`YXDD` are Poch 1989 polymerase motifs, `GDD` is motif C in an RdRp. None of those is
fold-general either. **ADR 0016's prohibition is stricter than the repository's own
precedent**, and that inconsistency should be recorded.

What the motif triple is not is a substitute for the ligand-derived source. It agrees with it
at Jaccard 0.5 and puts the source centroid 6 A away. It misses the purine-binding region
126-134 entirely.

---

## 3. Input blocker 2 — the contact topology is largely invented, and here is the number

C6 makes contact topology the object the whole method rests on. `5TBY` is a SWISS-MODEL
homology model on a tarantula template, rigid-body fitted into a 20 A envelope. `9GZ3` is a
cryo-EM structure of the same protein at 3.4 A.

Aligned by sequence, 761 residues are present in both. Contact graphs at the frozen 4.5 A
heavy-atom cutoff:

| minimum sequence separation | `5TBY` edges | `9GZ3` edges | shared | Jaccard | recall of measured edges |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1 (all contacts) | 3226 | 3626 | 2862 | 0.717 | 0.789 |
| 3 | 1783 | 2166 | 1447 | 0.578 | 0.668 |
| **5 (long-range only)** | 1103 | 1419 | 807 | **0.471** | **0.569** |

Degree agreement is Spearman **0.741**. Mean degree is 8.48 against 9.53.

**The fold is right and the graph is not.** Pairwise Cα-Cα distances agree at Spearman
**0.9724**, with a median absolute difference of **2.08 A** over all residue pairs. So `5TBY`
places the domains correctly and the residues wrongly.

That distinction is the whole finding. A method that reads only global shape would be fine on
`5TBY`. A method that reads the contact graph — which is what C6 mandates — receives a graph
in which **43 % of the measured long-range contacts are missing and 27 % of the contacts
present were not measured**. Those are the edges that carry allosteric signal.

---

## 4. What the organisers' final sentence licenses

> "Please always document the substitution you make and explain rational of why you did it."

That sentence is general. It converts every substitution in this repository from a unilateral
repair into sanctioned procedure conditional on documentation. It covers:

| Substitution | Frozen as | Documented in |
| --- | --- | --- |
| `6C1H` → `9GZ2` (holo) | `cardiac_myosin_corrected` | `primary/README.md` §2, `audit/cardiac-myosin.md` |
| `5TBY` → `9GZ3` (apo) | `cardiac_myosin_corrected` | same |
| `4OBE` → `4LDJ` (apo) | `kras_g12c_corrected` | `primary/README.md` §2, `audit/kras-g12c.md` |
| `1OPL` → `2G2H` (apo) | `bcr_abl1_corrected` | `primary/README.md` §2, `audit/bcr-abl1.md` |

The documentation exists. What is missing is a single submission-facing page that states each
substitution and its reason in one place, which is what a judge will look for. That page does
not exist yet.

**Note what the organisers did not do.** They declined to designate one replacement for all
teams. Scoring parity across teams is therefore not guaranteed on this target, and a
cross-team comparison on cardiac myosin is not like-for-like. Say so in the report.

---

## 5. Disposition

1. **Supersede ADR 0016.** Its blocking condition — "the organisers answer question (a)" —
   has occurred. A new ADR must record the answer, the cleared label blocker, and the two
   measured input blockers.
2. **Keep `cardiac_myosin_corrected` (`9GZ3`→`9GZ2`) as the scored arm.** It is the only
   cardiac-myosin pair with measured contact topology and a ligand-derived source, and it is
   the cleanest pair in the benchmark: same construct, same state, differing by mavacamten
   alone.
3. **Decide, in that ADR, whether to expose `5TBY:A`→`9GZ2:A` as a reported arm.** The
   argument for: it is the challenge's literal apo input, a valid label set now exists, and
   "unscoreable" was the honest answer only while no label set could be derived. The argument
   against: the arm needs a motif source that agrees with the ligand-derived source at Jaccard
   0.5, on a graph whose long-range topology agrees at Jaccard 0.47, so any number it produces
   measures the homology model as much as the method.
   **Recommendation: expose it, non-confirmatory, with both numbers printed beside every
   result.** A disclosed defective number beats a missing one, because a judge reading Table 1
   will look for the accession.
4. **Add the myosin motif triple to `CATALYTIC_MOTIFS` only if item 3 is decided yes**, with
   its PROSITE or primary-literature citation and the validation table in section 2 committed
   as a test.
5. **Write the substitution page** named in section 4.

---

## 6. Reproduction

```
scratchpad/probe/myosin_topology.py   5TBY vs 9GZ3 contact-graph agreement
scratchpad/probe/myosin_source.py     motif candidates, and label transfer onto 5TBY
scratchpad/probe/myosin_source2.py    PS00016 failure mode
scratchpad/probe/myosin_source3.py    family-triple validation against ligand truth
```
