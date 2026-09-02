# 47 — Three new quantum families, and what each one measured

**Code:** `src/allo/quantum/interference.py`, `connectivity.py`, `quantumness.py` ·
**Measured in:** `experiments/2026-08-26-beats-distance` (69 scorers, 4 `development` arms).

Phase 2 closed with eleven quantum observables that all behaved like distance rankings, and
with no account of *why*. Three literature results changed that on 2026-08-26, and each named a
construction the repository did not have. This document is what those constructions compute and
what they measured. The battery-wide verdict is `46-beats-distance.md`; the stability behaviour
is `44-stability-and-noise.md`. Neither is repeated here.

---

## 1. The diagnosis that came first

Faccin, Johnson, Biamonte, Kais and Migdał prove three things about a continuous-time walk on a
graph (Phys Rev X 3, 041007, 2013, arXiv:1305.6078):

1. The long-time occupation of a **classical** walk is exactly the degree distribution.
2. The long-time average of a **quantum** walk equals it **exactly when the initial state has
   zero energy**.
3. The deviation between them is bounded by `E / Δ`: the initial state's energy over the
   spectral gap.

**Our source state sat exactly on the classical point.** `walk._amplitudes` injects the
excitation at one active-site residue at a time and sums incoherently. A site-basis state
`|i⟩` has energy `⟨i|A|i⟩ = A_ii = 0`, because the adjacency has a zero diagonal. So every
time-averaged transfer probability in the Phase-2 battery was computed from a zero-energy state,
which is the one case in which the theorem says the answer is the classical one.

That is not a tuning mistake. It is a structural one, and it explains the measured behaviour
without appealing to anything about proteins.

**The bound also varies enormously between our arms**, which the theorem predicts and the method
sweep measured without being able to name:

| Arm | N | Spectral gap Δ | Energy E of the best source state | `E / Δ` |
| --- | --- | --- | --- | --- |
| `mkp5` | 147 | 1.6244 | 5.597 | 3.45 |
| `ptp1b` | 298 | 0.9819 | 5.928 | 6.04 |
| `ns5b` | 553 | 0.0748 | 2.000 | 26.72 |
| `hiv_rt` | 543 | 0.0860 | 5.307 | **61.69** |

**The gap varies by a factor of 21.7 across four proteins while the spectral range varies by
1.09.** The available "quantumness" therefore varies by roughly the same factor, at fixed
source. Any observable built on the difference between a quantum walk and a classical one is
measuring a quantity whose ceiling is eighteen times larger on `hiv_rt` than on `mkp5`.
`quantumness.quantumness_bound` computes this per target and it belongs in the report next to
any claim that a walk observable is not a classical one.

---

## 2. `interference.py` — isolate the term classical diffusion cannot produce

The finite-window transfer average separates exactly:

```
P_T(i) = Σ_k |⟨i|k⟩|² |⟨k|s⟩|²          the overlap term, phases already cancelled
       + cross terms in exp(-i(E_k - E_l)t)   the interference term
```

The first line is `walk.ctqw_infinite_time_average`. Subtracting it leaves the interference and
nothing else. Dividing by it cancels the magnitude, and the magnitude is where the radial
dependence lives — a residue far from the source has small overlap with every mode the source
excites, whatever the mechanism.

| Scorer | Mean AUC | Worst arm | mean abs ρ to distance |
| --- | --- | --- | --- |
| `coherent_source_ratio` | 0.533 | 0.282 | **0.284** |
| `interference_excess` | 0.517 | 0.197 | 0.671 |
| `interference_ratio` | 0.511 | 0.193 | 0.691 |
| `oscillation_ratio` | 0.507 | 0.272 | 0.377 |
| `spectral_participation_ratio` | 0.489 | 0.190 | 0.345 |

**The ratio construction works for the oscillation forms and fails for the magnitude forms.**
`oscillation_ratio` and `coherent_source_ratio` reach ρ of 0.28 to 0.38 against distance, where
the parent observables sit at 0.79 and 0.24. `interference_ratio` does not decorrelate at all,
at 0.691, because the interference excess is itself proportional to the overlap it is divided
by, so the ratio keeps what it was meant to cancel.

**And none of them is accurate.** Every AUC in the table is between 0.489 and 0.533, which is
chance. The family succeeds at its stated construction goal and fails at prediction.

---

## 3. `connectivity.py` — the required artifact, and what it makes possible

`CHALLENGE.md` §5 requires an **N × N matrix whose entry (i, j) is the quantum connectivity
between residue i and residue j**. No scorer in the repository produced one; every observable
returns an N-vector of connectivity *to the source*, which is one column of that matrix summed
over source residues. `connectivity_matrix` makes the object explicit, so the required artifact
and the ranked hit list come from the same construction rather than from two that happen to
agree. It is symmetric, verified on every arm, and costs `steps` N × N products.

Four scorers read the matrix without choosing a source, which matters because §4.1's "in most
cases, to an active site" exists for targets like c-Myc that have no catalytic site.

| Scorer | Mean AUC | Worst arm | mean abs ρ to distance | Beats distance |
| --- | --- | --- | --- | --- |
| `connectivity_strength` | **0.625** | 0.458 | 0.427 | 1 arm |
| `connectivity_participation` | 0.608 | 0.435 | 0.602 | 1 arm |
| `connectivity_entropy` | 0.596 | 0.345 | 0.623 | 1 arm |
| `connectivity_eigencentrality` | 0.578 | 0.472 | 0.452 | — |

**This is the strongest of the three new families and the only one that clears the previous
quantum ceiling.** The best Phase-2 quantum observable reached mean AUC 0.536; three of these
four exceed it. Three of the seven scorers that beat distance at uncorrected p ≤ 0.05 anywhere
in the 272 paired tests come from this family. Seven is chance across the whole battery
(`46-beats-distance.md` §1), so this is a lead and not a result — but it is the only family that
produced one.

---

## 4. `quantumness.py` — the energy lever and the symmetry route

**The energy lever.** Among states supported on the active site, the extremal energies are the
extremal eigenvectors of the Hamiltonian restricted to the source block. Same operator, same
graph, same averaging, same circuit: only the state preparation changes.

| Scorer | Mean AUC | Worst arm | mean abs ρ to distance |
| --- | --- | --- | --- |
| `low_energy_transfer` | 0.619 | 0.314 | 0.724 |
| `high_energy_transfer` | 0.553 | 0.207 | 0.655 |
| `energy_contrast` | 0.360 | 0.102 | **0.213** |

**The lever moves the ranking and does not escape the confound.** Both extremal states beat the
zero-energy `ctqw_average_transfer` on AUC — 0.619 and 0.553 against 0.524 — so the theorem's
prediction that the zero-energy state is the worst case holds. But their distance correlations
are 0.72 and 0.66, no better than the parent's 0.79.

**That distinction is worth stating carefully, because it corrects the obvious reading.**
Faccin's theorem is about the **degree** distribution, not about distance. Escaping the classical
degree limit is not the same as escaping the distance confound, and this experiment separates
them: raising `E` moved the score away from degree and left it on distance.

`energy_contrast` is the one construction that decorrelates, at 0.213 on all four arms, because
both states share the same radial envelope and it cancels in the difference. Its AUC of 0.360 is
below chance on every arm. A score consistently below 0.5 carries information in its sign, and
negating it would read 0.640 — **but that negation would be a sign chosen after seeing labels,
which is the selection ADR 0012 exists to forbid.** It is recorded as an observation and is not
available as a method.

**The symmetry route is empty, and this is measured rather than argued.** The survey's second
candidate builds on graph automorphisms: they give a quantum walk infinite hitting times where a
classical walk on a finite connected graph always has finite ones, and they show up as exact
degeneracy in the spectrum. Counting degenerate eigenvalue groups on the four arms:

| Arm | N | tol 1e-8 | 1e-6 | 1e-4 | 1e-3 | 1e-2 |
| --- | --- | --- | --- | --- | --- | --- |
| `mkp5` | 147 | 0 | 0 | 0 | 4 | 40 |
| `ptp1b` | 298 | 0 | 0 | 0 | 42 | 66 |
| `hiv_rt` | 543 | 1 | 1 | 4 | 130 | 88 |
| `ns5b` | 553 | 0 | 0 | 2 | 148 | 87 |

**Protein residue contact graphs have no exact symmetry.** `symmetry_dark_overlap` and
`degenerate_mixing_weight` return identically zero on three of four arms, and their AUC of 0.500
and 0.481 is the arithmetic consequence of a constant score. Anything below 1e-4 is numerical
noise in the eigensolver, not structure.

This closes a whole branch of the quantum-walk advantage literature for this problem, with a
measurement. A folded, asymmetric single chain has a generic spectrum, and every advantage that
requires degeneracy is unavailable on it.

---

## 5. What is worth keeping

1. **`connectivity_matrix` is required and is now the best-performing quantum construction we
   have.** It should be the reported metric, because it satisfies deliverable 1 and produces the
   hit list from the same object.
2. **`quantumness_bound` belongs in the report**, per target, next to any quantum claim. A
   `E/Δ` of 3.45 and one of 61.69 do not support the same sentence.
3. **The zero-energy source state is a defect and should not be restored.** Its replacement is a
   few lines and the ranking changes measurably.
4. **The symmetry family should be deleted or kept only as the recorded negative.** It is
   retained here because a measured "this branch is empty" is worth more than silence, and it
   costs nothing to run.
5. **The interference family stays as evidence, not as a method.** It succeeds at isolating the
   quantum term and shows that term carries no accuracy on this benchmark. That is a load-bearing
   negative for the report's honesty and it must not be quietly dropped.

## 6. Reproducing

```bash
uv run python experiments/2026-08-26-beats-distance/run.py
uv run python -c "
from allo.inputs import apo_input
from allo import network
from allo.quantum import quantumness
for arm in ('mkp5','ptp1b','hiv_rt','ns5b'):
    print(arm, quantumness.quantumness_bound(network.build(apo_input(arm))))
"
```
