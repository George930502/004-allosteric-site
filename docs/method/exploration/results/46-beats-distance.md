# 46 — Does anything beat the distance baseline?

**Experiment:** `experiments/2026-08-26-beats-distance` · 276 records · 69 scorers · 4
`development` arms · evaluation-default graph · the frozen paired test `compare_methods`.

Every earlier result in this directory carries the same caveat: the score correlates 0.65 to
0.85 with plain Euclidean distance to the active site, and detrending distance out collapses
performance. That makes "beat distance" the question, and the evaluation layer already froze a
test for it. `allo.scoring.harness.compare_methods` pairs the two scores on the residue, takes
the difference of their midrank vectors, and reads that difference against the same
matched-patch pool the confirmatory test uses. It was frozen before any method existed
(ADR 0025), so this experiment invents no statistic. It runs the frozen one over the whole
battery.

Two baselines, because "beats distance" and "beats a cheap classical score" are different bars:
`distance_from_source_negated`, and `eigenvector_centrality`, which was the strongest single
classical scorer in the method sweep.

---

## 1. The result

| Comparison | Paired tests | Scorer leads | Wins at uncorrected p ≤ 0.05 | Expected by chance |
| --- | --- | --- | --- | --- |
| vs `distance_from_source_negated` | 272 | 125 | **7** | 6.8 |
| vs `eigenvector_centrality` | 272 | 100 | **0** | 6.8 |

**Nothing in the battery beats distance more often than chance, and nothing beats eigenvector
centrality at all.** Seven wins out of 272 two-sided tests is 6.8 expected under the null. Zero
wins against eigenvector centrality is not a near miss; it is the whole battery losing to one
line of NumPy.

The seven, for the record, because a negative result still has to name its members:

| Arm | Scorer | Family | p calibrated | ΔAUC |
| --- | --- | --- | --- | --- |
| `ns5b` | `local_contact_order` | classical | 0.00926 | +0.528 |
| `ptp1b` | `source_conditioned_betweenness` | classical | 0.00939 | +0.316 |
| `ptp1b` | `connectivity_entropy` | quantum | 0.01429 | +0.289 |
| `ns5b` | `connectivity_strength` | quantum | 0.01734 | +0.438 |
| `ptp1b` | `betweenness_centrality` | classical | 0.01987 | +0.354 |
| `ptp1b` | `connectivity_participation` | quantum | 0.02129 | +0.278 |
| `ns5b` | `gnm_fluctuation` | classical | 0.04885 | +0.503 |

Three of the seven come from the N × N connectivity family added on 2026-08-26. That is the
only encouraging line in this document, and at seven-against-6.8 it is not yet evidence.

---

## 2. The correction cannot run, on two of four arms

Holm over the battery rejects nothing on any arm: 0 of 12 on `mkp5`, 0 of 55 on `ptp1b`, 0 of 2
on `hiv_rt`, 0 of 56 on `ns5b`. **Do not read that as four negative results.** Two of them are
not results at all.

`compare_methods` computes its p from a permutation pool, so its finest resolution is bounded
below. The smallest calibrated p anywhere in these 272 tests is **0.001080**. Holm's first step
demands `p ≤ 0.05 / m`:

| Arm | Family size m | Holm step 1 needs | Permutation floor | Can the test reject? |
| --- | --- | --- | --- | --- |
| `hiv_rt` | 2 | 0.025000 | 0.001080 | yes |
| `mkp5` | 12 | 0.004167 | 0.001080 | yes |
| `ptp1b` | 55 | 0.000909 | 0.001080 | **no, at any data** |
| `ns5b` | 56 | 0.000893 | 0.001080 | **no, at any data** |

**On `ptp1b` and `ns5b` the procedure cannot reject however good a method is.** The pool is too
coarse for the family size. Reporting "zero survivors" on those two arms without this table
would have been a false negative dressed as evidence.

The two arms where the test had resolution are `mkp5` and `hiv_rt`, and there it could have
rejected and did not.

**Two ways to fix this, and they are different decisions.** Enlarge the permutation pool, which
buys resolution at a linear cost in compute and changes nothing about the protocol. Or shrink
the family by pre-registering a small candidate set before scoring, which is what the
`development` tier exists to make possible. The second is the better answer, because a battery
of 69 is a screen and a screen was never meant to carry a corrected claim.

---

## 3. Where the distance-orthogonal signal actually is

The useful quadrant is high accuracy **and** low distance correlation. Taking |ρ to negated
distance| below 0.35 and mean AUC above 0.55:

| Scorer | Family | Mean AUC | Worst arm | mean abs ρ to distance |
| --- | --- | --- | --- | --- |
| `gnm_entropy_response` | classical | 0.704 | 0.541 | 0.257 |
| `stiff_corridor_to_source` | classical | 0.684 | **0.650** | **0.057** |
| `gnm_transfer_entropy` | classical | 0.584 | 0.436 | 0.207 |
| `core_number` | classical | 0.575 | 0.556 | 0.279 |

**Four scorers make the quadrant and all four are classical.** `stiff_corridor_to_source` is the
standout: a mean AUC of 0.684 with a rank correlation of 0.057 against distance, and a worst arm
of 0.650, which is the highest floor in the entire battery.

**No quantum observable makes the quadrant.** The best quantum scorer by AUC is
`connectivity_strength` at 0.625, and its ρ to distance is 0.427, so it fails the orthogonality
bar. The quantum observables that *are* orthogonal — `ctqw_coherent_source_contrast` at 0.241,
`coherent_source_ratio` at 0.284, `ctqw_temporal_variance` at 0.345, `energy_contrast` at 0.213
— all sit between 0.36 and 0.53 AUC, which is chance.

This is the sharpest statement the repository can currently make about the quantum layer, and it
is not the one we wanted: **on this benchmark the quantum observables are either accurate because
they are distance, or orthogonal to distance and uninformative. None is both.**

---

## 4. What this does and does not refute

**Refuted.** That the existing battery contains a method which adds signal over the distance
baseline. It does not, at a rate distinguishable from chance, on four arms.

**Refuted.** That detrending is the missing piece. `40-method-sweep.md` already showed detrended
variants ranking below raw. This adds the paired version of the same finding: the problem is not
that distance is poorly removed, it is that little remains once it is.

**Not refuted, and not tested here.** That a *different kind of input* carries the signal. Every
scorer in this battery is a function of one contact graph and its geometry, and
`docs/method/review/13-graph-construction.md` proves that class inherits distance by
construction: a distance-threshold graph on 3D points is a random geometric graph, in which
graph distance is asymptotically proportional to Euclidean distance
(doi:10.1017/apr.2016.31). Escaping the confound from inside that class may not be possible.

The descriptors that `docs/method/review/14-distance-confound.md` finds survive the confound —
local energetic frustration, cavity geometry, contact area rather than contact distance — are
**not in this battery** because they are not functions of the contact graph. That is the next
experiment, not a gap in this one.

---

## 5. Threats to this reading

- **The paired test is two-sided and the battery is a screen.** Seven wins against 6.8 expected
  is the comparison that matters, and both numbers are small. This experiment has the power to
  say "no large effect", not "no effect".
- **`eigenvector_centrality` may be a strong baseline for a boring reason.** It ranks residues by
  their position in the packed core, and the matched-patch null matches on geometry rather than
  on packing. `45-source-choice.md` finds the same scorer wins as a *source*. Whether the null
  fully absorbs packing is an open question about the evaluation layer, not about the methods.
- **Four arms.** The quadrant table's worst-arm column is a minimum over four numbers.
- **69 scorers on 4 arms is the multiplicity `41-selection-and-power.md` prices.** The four
  quadrant members were selected after seeing the result and are hypotheses, not findings.

---

## 6. Reproducing this

```bash
uv run python experiments/2026-08-26-beats-distance/run.py
```

Resumable, keyed by `arm|scorer`. Both baselines and the Holm table are computed by `summarise`
in the same file. The permutation floor quoted in §2 is the minimum `p_calibrated` over the
272 paired tests in `records.jsonl` and is recomputed by reading that file.
