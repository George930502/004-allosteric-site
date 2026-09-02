# 12 — What the fourteen label sets look like, before any method sees them

> **SUBJECT PARTLY DELETED — 2026-09-02.** This document cites files in the method layer:
> `src/allo/{network,classical,quantum}`, `docs/method/exploration/`, `tests/test_method.py`,
> or an experiment directory dated 2026-08-26 or 2026-08-27. All of those left `main` on
> 2026-09-02 (ADR 0037) and are preserved whole on the branch `method-layer-archive`.
> Findings whose subject is one of those files are **not re-runnable on `main`**. They stay
> here unedited, because a record of what an audit found is worth keeping even when the
> subject is gone. To re-run one, check out that branch. Two things moved rather than left:
> `allo.network.graph` is now `allo.structure.graph`, and the nine required baselines are now
> `allo.scoring.baselines`.

**Status.** Measured 2026-09-02. Apo-only descriptors, computed against the frozen label
sets. Nothing here changes a freeze. It is the confounder baseline the evaluation protocol
controls for but never prints.

`src/allo/structure/properties.py` states the gap in its own docstring: section 11 of
`docs/benchmark/evaluation/README.md` "controls burial _inside_ the null, which is the
stronger treatment, but it leaves the reader with no number." This page is that number, for
all five apo-only descriptors and all fourteen arms.

---

## 1. What was measured

For every arm, each candidate residue received five values. All five come from the apo
structure alone.

| Descriptor                       | Source                                                                     |
| -------------------------------- | -------------------------------------------------------------------------- |
| `relative_solvent_accessibility` | Shrake-Rupley SASA over Tien et al. maxima, doi:10.1371/journal.pone.0080635 |
| `normalised_b_factor`            | Deposited B-factor, z-scored within the chain                              |
| `hydrophobicity`                 | Kyte-Doolittle, doi:10.1016/0022-2836(82)90515-0                            |
| `degree`                         | Weighted degree in the frozen 4.5 Å contact graph                          |
| `distance_to_source`             | Minimum Cα distance to any active-site residue                             |

The statistic is the Mann-Whitney AUC of the descriptor as a **standalone predictor**: the
probability that a label residue outranks a background residue. A value of 0.5 is chance.
A value far from 0.5 in either direction means the descriptor alone separates the label set.

Positives are `scoreable_label_residues`. The background is `residue_ids` minus
`excluded_from_scoring`, which is the same candidate set `score_arm` uses.

**Validation.** The evaluation protocol §4.3 publishes the distance baseline on three
primary arms as AUC-ROC 0.589, 0.215 and 0.335. This sweep reproduces all three to the
digit, as 1 − 0.411, 1 − 0.785 and 1 − 0.665. The measurement pipeline agrees with the
frozen harness.

---

## 2. The result table

| arm                        | n+  | n−  |   RSA |  norm B | hydro | degree |  dist |
| -------------------------- | --- | --- | ----: | ------: | ----: | -----: | ----: |
| `kras_g12c_mandated`       | 16  | 130 | 0.485 |   0.260 | 0.504 |  0.419 | 0.411 |
| `kras_g12c_corrected`      | 16  | 132 | 0.487 |   0.491 | 0.500 |  0.425 | 0.412 |
| `bcr_abl1_mandated`        | 20  | 420 | 0.378 |   0.336 | 0.698 |  0.628 | 0.519 |
| `bcr_abl1_corrected`       | 18  | 243 | 0.500 |   0.388 | 0.667 |  0.542 | 0.785 |
| `cardiac_myosin_corrected` | 12  | 731 | 0.569 |   0.563 | 0.389 |  0.486 | 0.665 |
| `mkp5`                     | 11  | 125 | 0.264 |   0.242 | 0.644 |  0.751 | 0.201 |
| `chk1`                     | 12  | 249 | 0.511 |   0.451 | 0.491 |  0.494 | 0.550 |
| `ptp1b`                    | 11  | 276 | 0.407 |   0.606 | 0.549 |  0.664 | 0.667 |
| `smyd3`                    | 12  | 396 | 0.567 |   0.612 | 0.562 |  0.526 | 0.719 |
| `glucokinase`              | 19  | 419 | 0.575 |   0.674 | 0.607 |  0.531 | 0.365 |
| `hiv_rt`                   | 16  | 518 | 0.431 |   0.487 | 0.565 |  0.584 | 0.068 |
| `ns5b`                     | 16  | 534 | 0.232 |   0.404 | 0.645 |  0.770 | 0.739 |
| `p97_vcp`                  | 17  | 671 | 0.427 |   0.238 | 0.525 |  0.530 | 0.565 |
| `ecoli_cps`                | 19  | 978 | 0.571 |   0.759 | 0.422 |  0.426 | 0.804 |

Pooled test of each column against chance, by Wilcoxon signed-rank over the fourteen arms:

| descriptor  | mean AUC | Wilcoxon p |
| ----------- | -------: | ---------: |
| RSA         |    0.457 |      0.173 |
| norm B      |    0.465 |      0.451 |
| hydro       |    0.555 |      0.055 |
| degree      |    0.555 |      0.119 |
| dist        |    0.534 |      0.502 |

---

## 3. Finding 1 — no descriptor is a benchmark-wide shortcut

Every mean AUC sits between 0.457 and 0.555. No column rejects chance at α = 0.05, and
hydrophobicity comes closest at p = 0.055 without reaching it. A method cannot win the
pooled result by reading burial, flexibility, hydrophobicity, degree or distance.

This is a benchmark design strength, and no document states it. The eight admission clauses
were written to control apo/holo pair validity, not descriptor balance. Balance came out as
a by-product of demanding real allosteric sites across nine protein families.

---

## 4. Finding 2 — every descriptor is strong per arm, and the sign flips

The pooled null result hides large per-arm effects that cancel.

- `ns5b` labels are buried and high-degree: RSA 0.232, degree 0.770.
- `mkp5` labels are buried, high-degree and **close** to the source: 0.264, 0.751, 0.201.
- `ecoli_cps` labels are exposed, floppy and **far**: 0.571, 0.759, 0.804.
- `p97_vcp` labels are the most rigid in the set: norm B 0.238.

The direction is not a property of allosteric sites. It is a property of each protein's
architecture. A single-descriptor baseline therefore scores near chance overall while
scoring 0.75 or better on individual arms.

**What this forces.** A per-arm result that beats one confounder proves nothing on its own.
Report the confounder AUC beside every per-arm score, as ADR 0025 already requires for the
three that `residue_properties` returns. Extend that display to `degree` and
`distance_to_source`, which ADR 0025 does not cover.

---

## 5. Finding 3 — the two-directional distance baseline is much stronger than reported

The protocol requires both distance directions as baselines
(`manifest.yaml`, `secondary_objectives.classical_comparison`). Section 4.3 reports the
single direction and concludes it is "below chance on three of five arms". Taking the
better of the two required directions per arm gives a different picture.

| arm                        | dist AUC | better direction | best AUC |
| -------------------------- | -------: | ---------------- | -------: |
| `hiv_rt`                   |    0.068 | near             |    0.932 |
| `ecoli_cps`                |    0.804 | far              |    0.804 |
| `mkp5`                     |    0.201 | near             |    0.799 |
| `bcr_abl1_corrected`       |    0.785 | far              |    0.785 |
| `ns5b`                     |    0.739 | far              |    0.739 |
| `smyd3`                    |    0.719 | far              |    0.719 |
| `ptp1b`                    |    0.667 | far              |    0.667 |
| `cardiac_myosin_corrected` |    0.665 | far              |    0.665 |
| `glucokinase`              |    0.365 | near             |    0.635 |
| `kras_g12c_mandated`       |    0.411 | near             |    0.589 |
| `kras_g12c_corrected`      |    0.412 | near             |    0.588 |
| `p97_vcp`                  |    0.565 | far              |    0.565 |
| `chk1`                     |    0.550 | far              |    0.550 |
| `bcr_abl1_mandated`        |    0.519 | far              |    0.519 |

Median best-direction AUC is **0.666**. It reaches 0.72 or more on 5 of 14 arms and 0.80 or
more on 2. Nine arms favour "far" and five favour "near".

**The `hiv_rt` case is the sharp one.** Label residues sit at a median 10.4 Å from the
source. Background residues sit at a median 29.2 Å. The separation gives p = 3.9 × 10⁻⁹.
The NNRTI pocket is beside the polymerase active site, while the 543-residue p66 subunit
extends through the connection and RNase H domains, which are far from both.

`hiv_rt` still passes the distality clause. All 16 labels lie beyond 3 Å, and 9 lie beyond
10 Å. The clause tests **membership**, and the confound here is **proximity**. This is the
same distinction `03-kras-mask.md` records for the organisers' switch-II mask, appearing on
a second arm and in the opposite direction.

**What this forces.** Two things, and neither is a freeze change.

1. Picking the better direction per arm is selection on the answer. If the report quotes
   the best-of-two figure, it must say the direction was chosen post hoc, or spend a
   multiplicity level on it. Otherwise the geometry baseline is flattered and the
   propagation method is judged against a weakened control.
2. Section 4.3's sentence "below chance on three of five arms" is true for the primary set
   and misleading for the benchmark. Nine of fourteen arms favour the "far" direction, in
   which the plain baseline is above chance.

---

## 6. Finding 4 — amino-acid composition is not a route in

Pooled over all fourteen arms: 215 label residues against 5822 background residues.

| residue | label n | label % | background % | odds ratio | Fisher p |
| ------- | ------: | ------: | -----------: | ---------: | -------: |
| HIS     |       9 |     4.2 |          1.9 |       2.27 |    0.038 |
| TYR     |      14 |     6.5 |          3.4 |       1.97 |    0.023 |
| VAL     |      21 |     9.8 |          6.9 |       1.46 |    0.133 |
| SER     |       5 |     2.3 |          5.3 |       0.43 |    0.058 |
| ASP     |       5 |     2.3 |          5.5 |       0.41 |    0.044 |

Twenty tests were run and five are shown. The smallest p is 0.023 against a Holm threshold
of 0.05/20 = 0.0025. **Nothing survives correction.** A composition-only baseline cannot
score on this benchmark, which removes a whole class of trivial predictors.

The HIS and TYR trend is worth one line and no more. Neither reaches the corrected
threshold, and 215 pooled label residues cannot support a compositional claim. Recorded as
unknown.

---

## 7. Finding 5 — this review directory is an unprotected answer key

The measurement above cannot be committed. `tests/test_no_leakage.py` scans every tracked
`.py`, `.sh`, `.ipynb` and `Makefile` outside `src/`, `tests/`, `data/` and `structures/`,
and it fails any file naming `frozen.json`. The gate is correct. The consequence is that the
repository has **no sanctioned home for a committed evaluation-side analysis script**, so
this probe lives in the session scratchpad and its source is reproduced in section 9.

The same scan does not read Markdown. That is a gap, because
`docs/benchmark/secondary/evidence/extension-candidates.md` is a protected path and it is
Markdown. It was protected for naming real label residues in apo numbering.

`docs/benchmark/review/` now does the same thing. `03-kras-mask.md` names five real label
residues. `01`, `02`, `10` and this page carry per-arm positive counts, which C1 names
directly: "not even the residue count". The directory is not in `PROTECTED_PATHS`.

**The one-line fix does not work, and it was tried.** Adding `docs/benchmark/review/` to
`PROTECTED_PATHS` makes the suite fail. `data/fetch_structure_evidence.py` writes its output
into that same directory, so once the directory is protected the script names five protected
paths, all of them its own. A grep for the guarded tokens found nothing. Staging the
directory and running the suite found it at once.

The protection is still right. The obstacle is that `docs/benchmark/review/data/` holds two
kinds of file: prose evidence that must be protected, and the scripts that produce it, which
must be able to name their own output. Three ways out exist, and the choice is a design
decision rather than a guard tweak.

| Option                                          | Cost                                                                                                    |
| ----------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| Protect the directory, move both scripts out    | There is nowhere to move them to. The first paragraph of this section is that gap                       |
| Protect the directory, exempt the writer script | The precedent is `allo.inputs`, exempted for `data/raw/apo`. One named exemption and one comment        |
| Protect the prose files by name, not the tree   | Weakens the "protected by default" rule the evaluation directory was given for a stated reason          |

**Decided the same day: none of the three, and a fourth.** ADR 0034 protects the tree and
exempts its own tools by a **rule** instead of by a name list — a file is a review tool when it
is tracked inside the tree **and** imports nothing from `allo`. That is strictly narrower than
the second option, because a name list grows silently while the rule cannot be satisfied by
anything that touches the package. The leakage suite passes with the tree protected, and two
new tests pin the rule: every review tool imports no package module, and the exemption stops at
the tree boundary. The first option's gap — that there is nowhere to move the scripts to —
remains true and is now recorded rather than worked around.

---

## 8. Disposition

| # | Finding                                            | Action                                                                    |
| - | -------------------------------------------------- | ------------------------------------------------------------------------- |
| 1 | No descriptor separates labels benchmark-wide      | Record as a design strength in the report. No change                      |
| 2 | Per-arm descriptor AUC reaches 0.77                | Print `degree` and `distance_to_source` beside every per-arm score        |
| 3 | Best-direction distance AUC median 0.666           | Declare the direction choice, or spend a multiplicity level               |
| 4 | §4.3's "below chance on three of five" is primary-only | Correct the scope in the report, not in the freeze                     |
| 5 | Composition is not a route in                      | Record as closed. No baseline needed                                      |
| 6 | `docs/benchmark/review/` is an unprotected answer key | **Done 2026-09-02.** Protected, with an import-based exemption rule for its own tools (ADR 0034) |

Items 2 and 3 are the ones that change what the report must print. **Item 2 is done**: `degree`
and `distance_to_source` are declared in `evaluation/manifest.yaml` and are computed beside
every per-arm score at protocol v3. Item 3 is open. Item 6 is closed.

---

## 9. Reproduction

The probe is deliberately uncommitted, for the reason in section 7. Write it to a scratch
path and run it from the repository root.

```python
import json
from pathlib import Path

import numpy as np
from scipy import stats

from allo.inputs import apo_input
from allo.network import build
from allo.structure.properties import residue_properties

SETS = {
    "primary": Path("docs/benchmark/primary/frozen.json"),
    "secondary": Path("docs/benchmark/secondary/frozen.json"),
}

for path in SETS.values():
    frozen = json.loads(path.read_text())
    for arm, spec in frozen["targets"].items():
        apo = apo_input(arm)
        graph = build(apo)
        props = residue_properties(apo)

        candidates = [r for r in spec["residue_ids"] if r not in set(spec["excluded_from_scoring"])]
        labels = set(spec["scoreable_label_residues"])
        source = set(spec["active_site"])

        s = apo.structure
        ca = {
            int(r): np.asarray(x, dtype=float)
            for r, a, x in zip(s.seq_id, s.atom, s.coord, strict=True)
            if a == "CA"
        }
        source_xyz = np.array([ca[r] for r in sorted(source) if r in ca])
        degree = dict(zip(graph.order, graph.degree, strict=True))

        columns = dict(props)
        columns["degree"] = {r: float(degree.get(r, 0.0)) for r in candidates}
        columns["distance_to_source"] = {
            r: float(np.linalg.norm(source_xyz - ca[r], axis=1).min())
            for r in candidates
            if r in ca
        }

        for name, values in columns.items():
            pos = np.array([v for r, v in values.items() if r in candidates and r in labels])
            neg = np.array([v for r, v in values.items() if r in candidates and r not in labels])
            u, p = stats.mannwhitneyu(pos, neg, alternative="two-sided")
            print(arm, name, round(u / (len(pos) * len(neg)), 3), f"{p:.3g}")
```

`graph.order` and `graph.degree` are the correct field names. `ResidueGraph` has no
`residues` attribute, and `adjacency` is an alias for `weight`.
