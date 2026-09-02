# KRAS: the organisers' mask, and the frozen scoreable set

**Question.** The organisers require that the five switch-II label residues overlapping the
nucleotide source — A11, C12, G13, K16, P34 — be excluded from scoring. Does the frozen
benchmark already do that?

**Answer.** Yes, exactly, on both KRAS arms. No change is needed.

---

## 1. The measurement

`docs/benchmark/primary/frozen.json`, both KRAS arms:

```
label_residues            9 10 11 12 13 16 34 58 59 60 61 62 63 68 69 72 95 96 99 100 103   (21)
scoreable_label_residues  9 10          58 59 60 61 62 63 68 69 72 95 96 99 100 103          (16)
removed                        11 12 13 16 34                                                 (5)
```

The five removed residues are **11, 12, 13, 16 and 34**. The organisers name A11, C12, G13,
K16 and P34. The sets are identical.

The mechanism is clause (vii) of the pair definition, implemented in
`allo.benchmark.derive`: a label that is itself a propagation-source residue leaves the
positive class. On `kras_g12c_mandated` the derived source is 23 residues and on
`kras_g12c_corrected` it is 22; both contain all five.

`excluded_from_scoring` removes the same residues from the **negative** class too, so the
candidate set is 146 and 148 rather than 169 and 170 (ADR 0011). The organisers did not ask
for that half. It is the same argument applied consistently: a residue that scores maximally
by construction measures nothing, whichever class it sits in.

---

## 2. Two things the organisers' wording does not settle

### 2.1 Their reason is a distance argument; ours is a membership rule

The organisers write that the five residues "are not distal and would result in trivial
zero-distance credit". The repository's clause (vii) never mentions distance. It removes a
label because it is **inside the source set**, not because it is close to it.

The two agree on this label set and diverge in general. A residue 4 A from the source but
outside it is removed under a distance reading and kept under ours. `kras_g12c_corrected`'s
nearest **scoreable** label sits **3.8 A** from the source, so a distance rule with any
threshold above 3.8 A would remove more labels than the organisers named.

The repository keeps the membership rule, for a reason with evidence behind it: no formal
definition of an allosteric site in any source read for this project contains a minimum
separation from the active site, and CASBench measures that "in 30 % of cases, the catalytic
and allosteric sites either overlap or share a common border"
(doi:10.32607/20758251-2019-11-1-74-80). A distance filter would discard about a third of
curated allosteric sites.

**Consequence for the submission.** State the rule as membership, note that it reproduces the
organisers' five residues exactly, and print the scoreable set's minimum distance to the
source (3.8 A) so a reader can check that no trivial-credit residue survives.

### 2.2 "Report KRAS separately" was asked and not answered

The third sub-question — whether KRAS should be reported apart from the genuinely distal
targets — has no answer in the reply. The organisers said only that KRAS remains required and
the five residues are masked.

The repository already separates the arms on this axis without being asked.
`evaluation/README.md` §11 makes proximity to source one of four reporting factors, and
`primary/README.md` §4 Axis 2 gives the numbers:

| Arm | scoreable label distance to source: min / median / max |
| --- | --- |
| `kras_g12c_corrected` | 3.8 / 10.7 / 18.2 A — proximal |
| `bcr_abl1_corrected` | 10.8 / 17.5 / 30.1 A — distal |
| `cardiac_myosin_corrected` | 16.5 / 27.6 / 35.6 A — the most distal in the set |

Nothing is blocked. The report must show the per-arm numbers beside any pooled number, which
§11 already requires.

---

## 3. What this ratifies

Clause (vii) was a repository policy with a methodological analogy in AlloPred and no
benchmark-universe precedent. It now has the organisers' explicit endorsement on the one
target where it bites. That is worth recording in the report: the exclusion is not a choice
that flatters our numbers — it **removes five of twenty-one positives** from the easiest
arm, and it is what the organisers require.

## 4. One residual risk

Masking removes 5 of 21 labels and leaves 16. Prevalence falls from 12.4 % to 10.8 % on the
corrected arm. The exact hypergeometric chance line for "at least one hit in the top 5" on
that arm is **0.440** — the highest of the five primary arms. A top-5 list on KRAS clears
chance far less easily than the raw hit count suggests, and every top-5 number must be
printed against that line.
