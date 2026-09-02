# Derived contact cutoffs: the pre-screen, and what it closes

**Question.** `docs/method/review/19-cross-protein-normalisation.md` §1.2 defines a two-number
pre-screen that any derived normalisation must pass before it is implemented. Number (a) is
the between-protein spread of the quantity the rule equalises. Number (b) is `R_within`, the
endpoint's sensitivity to that quantity inside one protein. **A rule needs both to be large.**

This experiment measures (a) for the three derived contact-cutoff rules §7 ranks at 7, 8 and
9. It scores nothing. Review 19 §7 states the falsifier in the form used here: if the derived
`r*` varies by less than 0.3 Angstrom across the arms, the rule is a global constant in
disguise and the experiment stops there.

**Scope.** Nine arms: the four `development` arms and the five primary arms. Apo side only.
The `generalisation` tier stays closed (ADR 0021). Protein size spans 147 to 764 residues, a
factor of 5.2.

---

## 1. The peptide bond had to be removed first, and that is itself a result

The first run returned a connectivity cutoff of 2.00 Angstrom and an RDF first minimum of
1.20 Angstrom. Neither is a contact distance. Both are artefacts of one fact:

**The closest residue-residue heavy-atom distance is the peptide bond, on every arm.** It
measures 1.281 to 1.323 Angstrom across the nine, and it is about 1.4 Angstrom below the
closest non-bonded contact. On `mkp5`, all 146 pairs below 2.0 Angstrom are sequence-adjacent
and there are exactly 146 of them for 147 residues, so the chain is unbroken.

Two consequences follow, and both are rulings on the rules rather than on the code.

- **The connectivity-threshold rule is degenerate for a single covalent chain.** The backbone
  is a path through every residue, so the graph is connected the moment the peptide bond is
  an edge. With the backbone left in, the rule reports the peptide bond length and reports
  chain breaks in the two arms that have them. It measures crystallographic completeness, not
  packing.
- **The RDF first minimum is degenerate for the same reason.** The peptide-bond spike sits
  alone at 1.3 Angstrom with an empty gap above it, so the first minimum is that gap.

Every rule is therefore solved twice. `backbone` keeps all pairs and is reported to show the
artefact. `tertiary` deletes pairs closer than 2 in author numbering, which removes exactly
the covalent bond, and it is the number that means something.

---

## 2. The result

Nine arms, tertiary contacts only.

| Rule | min | max | Spread | SD | Constant at 0.3 A? |
| --- | --- | --- | --- | --- | --- |
| Isostatic, `<k>(r*) = 2d = 6` | 3.85 | 4.15 | **0.30** | 0.092 | **Yes, at the threshold** |
| Connectivity threshold | 3.50 | 4.30 | 0.80 | 0.305 | No |
| RDF first minimum | 3.18 | 4.83 | **1.65** | 0.690 | No |

Per arm, ordered by size:

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

## 3. All three fail, and they fail in two different ways

**The isostatic rule is a global constant.** Maxwell counting is the one tier (i) rule in the
set: `z = 2d = 6` has no fitted constant anywhere. Solved on nine proteins spanning 5.2-fold
in size it returns 3.85 to 4.15 Angstrom, a standard deviation of 0.092 Angstrom. That is
review 19 §7's named failure mode for this rule, reached exactly: **a per-protein rule whose
value is the same on every protein is a constant, and there is nothing to normalise.**

**The other two vary, and what they vary with is protein size.**

| Rule | Spread | Spearman against N | p |
| --- | --- | --- | --- |
| Isostatic | 0.30 | +0.487 | 0.183 |
| Connectivity threshold | 0.80 | **+0.723** | **0.028** |
| RDF first minimum | 1.65 | **+0.845** | **0.004** |

A cutoff rule that tracks N is not reading protein-specific physics. It is reading the
residue count, and it would import the size confound into the graph that every downstream
scorer is built on. **This reproduces, on our own benchmark, the caveat review 19 quotes from
the percolation literature's own authors:** the critical threshold "is generally higher for
bigger proteins" (doi:10.1529/biophysj.105.064485, review 19 §Q1.1).

So the dichotomy is complete. The rule that is genuinely derived does not vary. The rules
that vary are varying with size.

---

## 4. What this closes and what it does not

**Closed.** The three derived contact-cutoff rules, on part (a) of the pre-screen alone. None
needs part (b) measured, and none needs scoring. This is the cheapest possible closure and it
is what review 19 §7 asked for: "measure the spread of `r*` across arms **before** scoring
anything."

**Not closed.** Every rule that acts on **source geometry** rather than on the graph. Those
are ranked 1, 2 and 5 in review 19 §7 and this experiment says nothing about them. It in fact
strengthens the case for them by elimination: the graph side has no spread to normalise, so
whatever between-protein structure exists is not reachable from the cutoff.

**One incidental finding worth carrying.** All three derived cutoffs land **below** the frozen
4.5 Angstrom input-layer cutoff, between 3.18 and 4.83 with a median near 4.0. The frozen
graph is therefore slightly denser than any of the three derived criteria would build. That is
a fact about the input layer, not a criticism of it: ADR 0012 fixes the evaluation graph so
that two methods' p-values stay comparable, and it is not a hyperparameter.

---

## 5. Reproducing this

```bash
uv run python experiments/2026-08-27-derived-cutoff-prescreen/run.py
```

Resumable. `records.jsonl` is keyed by `target` and an existing key is not recomputed. Every
number above is derived from `records.jsonl` by `summarise` in the same file.
