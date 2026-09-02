# 52 — Derived contact cutoffs: the cheap half of the pre-screen, and what it closes

**Experiment:** `experiments/2026-08-27-derived-cutoff-prescreen` · 9 arms · 3 rules × 2
contact definitions · apo side only · **nothing is scored**.

`docs/method/review/19-cross-protein-normalisation.md` §1.2 defines a two-number pre-screen
that any derived normalisation must pass before it is implemented:

- **(a)** the between-protein spread of the quantity the rule equalises, and
- **(b)** `R_within`, the endpoint's sensitivity to that quantity inside one protein.

**A rule needs both to be large.** This document measures (a) for the three derived
contact-cutoff rules that review 19 §7 ranks at 7, 8 and 9. Part (a) is the cheap half, and a
small (a) closes a rule on its own: a per-protein rule whose value is the same on every
protein is a global constant in disguise.

Nine arms: the four `development` arms and the five primary arms, spanning 147 to 764
residues. The `generalisation` tier stays closed (ADR 0021).

---

## 1. The peptide bond had to be removed first

The first run returned a connectivity cutoff of 2.00 Angstrom and an RDF first minimum of
1.20 Angstrom. Neither is a contact distance, and the reason is one measurement:

**The closest residue-residue heavy-atom distance is the peptide bond, on every arm.** It
runs 1.281 to 1.323 Angstrom over the nine, about 1.4 Angstrom below the closest non-bonded
contact. On `mkp5` all 146 pairs below 2.0 Angstrom are sequence-adjacent, and 146 is exactly
the number of bonds in an unbroken 147-residue chain.

Two rules read the bottom of the distance distribution, so with the backbone left in they
read the peptide bond and nothing else.

- **The connectivity-threshold rule is degenerate for a covalent chain.** The backbone is a
  path through every residue, so the graph is connected the moment the bond is an edge. What
  the rule then measures is crystallographic chain breaks, not packing.
- **The RDF first minimum is degenerate for the same reason.** The bond spike sits alone at
  1.3 Angstrom above an empty gap, and the gap is the first minimum.

Every rule is therefore solved twice. `backbone` keeps all pairs and is reported to show the
artefact. `tertiary` deletes pairs closer than 2 in author numbering, removing exactly the
covalent bond, and it is the number that means something.

---

## 2. The result

Tertiary contacts, nine arms.

| Rule | Tier (review 19 §1.3) | min | max | Spread | SD |
| --- | --- | --- | --- | --- | --- |
| Isostatic, `<k>(r*) = 2d = 6` | **(i)** — no fitted constant at all | 3.85 | 4.15 | **0.30** | **0.092** |
| Connectivity threshold | (ii) — this graph's own percolation point | 3.50 | 4.30 | 0.80 | 0.305 |
| RDF first minimum | (ii) — this structure's own histogram | 3.18 | 4.83 | **1.65** | 0.690 |

Per arm, largest first:

| Arm | N | Isostatic | Connectivity | RDF first min |
| --- | --- | --- | --- | --- |
| `cardiac_myosin_corrected` | 764 | 4.00 | 4.30 | 4.68 |
| `ns5b` | 553 | 3.90 | 4.25 | 4.53 |
| `hiv_rt` | 543 | 4.15 | 4.25 | 4.47 |
| `bcr_abl1_mandated` | 451 | 4.00 | 3.70 | 4.83 |
| `ptp1b` | 298 | 3.85 | 3.85 | 4.43 |
| `bcr_abl1_corrected` | 272 | 3.95 | 3.60 | 3.68 |
| `kras_g12c_corrected` | 170 | 3.95 | 4.10 | 3.18 |
| `kras_g12c_mandated` | 169 | 3.95 | 4.10 | 3.18 |
| `mkp5` | 147 | 3.85 | 3.50 | 3.28 |

---

## 3. All three fail, in two different ways

**The one genuinely derived rule is a global constant.** Maxwell counting is the only tier (i)
entry in review 19's whole list: `z = 2d = 6` contains no fitted number anywhere. Solved on
nine proteins across a 5.2-fold size range it returns **3.85 to 4.15 Angstrom**, a standard
deviation of **0.092 Angstrom**. Review 19 §7 names this exact failure mode for this exact
rule, and the measurement reaches it: **a per-protein rule whose value is the same on every
protein is a constant, and there is nothing to normalise.**

**The two rules that do vary, vary with protein size.**

| Rule | Spread | Spearman against N | p |
| --- | --- | --- | --- |
| Isostatic | 0.30 | +0.487 | 0.183 |
| Connectivity threshold | 0.80 | **+0.723** | **0.028** |
| RDF first minimum | 1.65 | **+0.845** | **0.004** |

A cutoff that tracks the residue count is not reading protein-specific physics. It is reading
N, and adopting it would build the size confound into the graph that every downstream scorer
stands on — the same confound the matched-patch null exists to absorb.

**This reproduces the caveat the percolation literature's own authors state.** Review 19 §Q1.1
quotes them: the critical threshold "is generally higher for bigger proteins"
(doi:10.1529/biophysj.105.064485). That was a literature caveat about someone else's dataset.
It is now a measurement on ours.

So the dichotomy is complete and it needs no scoring to close:

> **The rule that is genuinely derived does not vary. The rules that vary, vary with size.**

---

## 4. What this closes, and what it hands forward

**Closed.** All three derived contact-cutoff rules, on part (a) alone. None needs part (b)
measured. This is what review 19 §7 asked for in the cheapest possible form: "measure the
spread of `r*` across arms **before** scoring anything."

**Not closed, and strengthened by elimination.** Every rule that acts on **source geometry**
rather than on the graph — ranks 1, 2 and 5 of review 19 §7. This experiment says nothing
about them directly. It says a great deal indirectly: the graph side has no between-protein
spread to normalise, so whatever between-protein structure exists is not reachable from the
cutoff. Combined with `30-frozen-graph-profile.md` §3.3 (mean contact number 8.9 to 10.3,
clustering 0.460 to 0.515 across a 7.2-fold size range) and `44-stability-and-noise.md` §6
(the spectral clock moves the spread by 2 %), the elimination now covers the graph, the
operator's time scale, and the cutoff. **What is left is where propagation starts.**

**One incidental fact worth carrying.** All three derived cutoffs land **below** the frozen
4.5 Angstrom input-layer cutoff, between 3.18 and 4.83 with a median near 4.0. That is a fact
about the input layer, not a criticism of it: ADR 0012 fixes the evaluation graph so two
methods' p-values stay comparable, and it is not a hyperparameter.

---

## 5. What this document supports and what it does not

**Supported.**

- The closest residue-residue heavy-atom distance is the peptide bond on all nine arms,
  1.281 to 1.323 Angstrom.
- The isostatic cutoff varies by 0.30 Angstrom (SD 0.092) across a 5.2-fold size range.
- The connectivity and RDF cutoffs correlate with N at Spearman +0.723 (p 0.028) and +0.845
  (p 0.004).

**Not supported.**

- No claim that a derived cutoff would score worse than the frozen 4.5 Angstrom graph. Nothing
  here is scored. The claim is that the rules are not **per-protein** rules, which is a
  different and cheaper thing to establish.
- No claim about part (b) of the pre-screen for these rules. It was not measured, because
  part (a) already closes them.
- No claim about source-geometry rules. Those are ranks 1, 2 and 5 and remain open.
- The size correlations rest on nine points. They order the rules; they do not measure the
  ordering precisely.

---

## 6. Reproducing this

```bash
uv run python experiments/2026-08-27-derived-cutoff-prescreen/run.py
```

Resumable, keyed by `target`. Every number above comes from `records.jsonl` via `summarise`
in the same file.
