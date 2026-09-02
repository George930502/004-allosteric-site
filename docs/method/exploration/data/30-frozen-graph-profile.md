# What the frozen apo graphs actually look like

**Scope:** an exploratory data analysis of all fourteen frozen apo residue contact graphs —
their topology, their spectra, and the geometry of the propagation source. Label-free and
apo-only throughout: nothing here opens a holo structure or a label set, so it is safe to
read before a method is designed. It deliberately excludes any statement about which method
scores well; that is `../results/40-method-sweep.md`.
**Sibling files:** `../results/41-selection-and-power.md` for what these graphs can resolve,
`../lit/22-transport-formalisms.md` for the observables the spectra decide between.
**Produced:** 2026-08-26 by `profile_graphs.py`, output in `frozen-graph-profile.json`.
**Graph:** the input layer's own rule — heavy-atom minimum distance at 4.5 Å, every modelled
residue of the frozen chain. This is the same object `allo.scoring.nulls.evaluation_graph`
builds, checked by `tests/test_method.py`.

---

## 1. Why this file exists

`docs/method/review/09-data-analysis.md` profiled 501 contact graphs and drew two
conclusions that shaped the whole Phase-2 plan: the adjacency spectrum is
Gaussian-orthogonal-ensemble-like with no near-degenerate pairs, and the leading eigenvalue
is isolated by 25.6 mean spacings. A continuous-time quantum walk on a spectrum shaped like
that must collapse onto eigenvector centrality, which is why the review expects every
walk-based observable to fail.

Those 501 graphs are not ours. They were built at Cβ with a 10 Å cutoff, on a different
protein set, in a repository that ADR 0026 has now established is not disjoint from our
primary targets. This file re-derives the same quantities on the fourteen graphs a method in
this repository will actually receive.

**The headline: one of the two conclusions holds on our graphs and the other does not.**

---

## 2. The table

| Arm                      | PDB  | N    | Edges | ⟨k⟩  | Diam. | Clust. | λ₁    | Gap/⟨s⟩ | ⟨r⟩   | Degen. | λ₂(L) | d̃(source) |
| ------------------------ | ---- | ---- | ----- | ---- | ----- | ------ | ----- | ------- | ----- | ------ | ----- | --------- |
| kras_g12c_mandated       | 4OBE | 169  | 795   | 9.4  | 8     | 0.511  | 11.04 | 16.0    | 0.569 | 0      | 0.480 | 9.7       |
| kras_g12c_corrected      | 4LDJ | 170  | 803   | 9.4  | 8     | 0.507  | 11.10 | 15.7    | 0.534 | 0      | 0.497 | 9.6       |
| bcr_abl1_mandated        | 1OPL | 451  | 2093  | 9.3  | 13    | 0.493  | 11.34 | 29.9    | 0.521 | 1      | 0.117 | 14.5      |
| bcr_abl1_corrected       | 2G2H | 272  | 1273  | 9.4  | 10    | 0.502  | 11.25 | 22.8    | 0.535 | 0      | 0.194 | 9.2       |
| cardiac_myosin_corrected | 9GZ3 | 764  | 3641  | 9.5  | 22    | 0.481  | 11.45 | 22.6    | 0.538 | 2      | 0.053 | 18.3      |
| mkp5                     | 1ZZW | 147  | 718   | 9.8  | 7     | 0.515  | 11.29 | 15.7    | 0.531 | 0      | 0.548 | 7.6       |
| ptp1b                    | 1SUG | 298  | 1481  | 9.9  | 10    | 0.487  | 11.80 | 18.1    | 0.516 | 0      | 0.318 | 11.7      |
| hiv_rt                   | 1RTJ | 543  | 2403  | 8.9  | 22    | 0.499  | 10.40 | **3.2** | 0.519 | 2      | 0.025 | 23.9      |
| ns5b                     | 1QUV | 553  | 2720  | 9.8  | 12    | 0.477  | 11.26 | **2.7** | 0.495 | 0      | 0.120 | 19.0      |
| chk1                     | 1IA8 | 272  | 1255  | 9.2  | 13    | 0.502  | 11.29 | 19.1    | 0.520 | 3      | 0.139 | 9.4       |
| smyd3                    | 6P7Z | 425  | 2089  | 9.8  | 12    | 0.496  | 11.18 | **3.7** | 0.502 | 0      | 0.151 | 16.0      |
| glucokinase              | 3IDH | 453  | 2270  | 10.0 | 14    | 0.480  | 11.64 | 18.7    | 0.527 | 1      | 0.127 | 12.3      |
| p97_vcp                  | 5FTK | 723  | 3241  | 9.0  | 18    | 0.482  | 10.62 | **1.7** | 0.500 | 0      | 0.020 | 12.8      |
| ecoli_cps                | 1A9X | 1058 | 5433  | 10.3 | 15    | 0.460  | 11.62 | 19.5    | 0.526 | 1      | 0.095 | 10.1      |

`⟨k⟩` mean contact number. `Gap/⟨s⟩` the λ₁–λ₂ gap in units of the mean adjacency level
spacing. `⟨r⟩` the mean of the level-spacing ratio `min(sₙ, sₙ₊₁)/max(sₙ, sₙ₊₁)`. `Degen.`
the count of spacings below 1 % of the mean. `λ₂(L)` the algebraic connectivity. `d̃(source)`
the median minimum heavy-atom distance from a candidate residue to the active site, in Å.

---

## 3. Four findings

### 3.1 The spectra are chaotic on every arm. That part of the prior holds.

The level-spacing ratio has two reference values: **0.386** for a Poisson spectrum, which
means no level repulsion and localised eigenvectors, and **0.536** for the Gaussian
orthogonal ensemble, which means strong level repulsion and delocalised eigenvectors. Our
fourteen graphs run **0.495 to 0.569, mean 0.524**. Every one sits at the GOE end.

Near-degeneracy is correspondingly rare: **10 near-degenerate pairs across all fourteen
graphs**, and eight of the fourteen have none at all.

**What this closes.** Any observable whose signal is carried by degenerate or near-degenerate
subspaces has nothing to work with here. That covers level-spacing degeneracy readouts, and
it covers any construction that needs an avoided crossing. The prior was right and it is now
right about _our_ graphs.

### 3.2 The leading eigenvalue is **not** uniformly isolated. That part does not hold.

The review's 25.6 mean spacings is inside our range but is not typical of it. The gap runs
from **1.67 to 29.9**, median 17.1, and **four of fourteen arms sit below 4**: hiv_rt (3.2),
ns5b (2.7), smyd3 (3.7), p97_vcp (1.7).

This matters because the argument that a continuous-time quantum walk must collapse onto
eigenvector centrality runs through that gap. A large gap means the Perron mode dominates
the propagator at any time long enough to matter, so the walk reproduces the Perron vector.
At a gap of 1.7 mean spacings, several modes contribute comparably, and the collapse
argument does not apply.

**Two of the four low-gap arms are `development` arms** — hiv_rt and ns5b — so the
prediction is testable immediately, on the tier where testing is allowed. The prediction is
sharp and directional: **if the collapse mechanism is the real one, the rank correlation
between a walk observable and eigenvector centrality must be markedly lower on hiv_rt, ns5b,
smyd3 and p97_vcp than on the other ten.** `score_arm`'s `against` parameter prints that
correlation on every run, so the test costs nothing extra.

This is not a claim that a walk will _work_ on those arms. It is a claim that the reason
given for expecting it to fail does not apply there, which is a different and smaller claim.

### 3.3 The graphs are almost interchangeable as graphs. The geometry is not.

Across a 7.2× range in size, from 147 to 1058 residues:

- mean contact number spans **8.9 to 10.3**,
- mean clustering spans **0.460 to 0.515**,
- λ₁ spans **10.40 to 11.80**.

Three numbers that barely move. A residue contact graph at a fixed cutoff is a
near-universal object, which is why every purely topological centrality gives similar-looking
distributions on every protein and why a method that separates targets must be using
something other than the raw topology.

The geometry of the _source_ is where the arms differ, and they differ a great deal:

- source size spans **3 residues (ns5b) to 61 (ecoli_cps)**, a 20× range;
- the median candidate-to-source distance spans **7.6 Å (mkp5) to 23.9 Å (hiv_rt)**;
- the fraction of candidates within 10 Å of the source spans **0.12 (ns5b) to 0.69 (mkp5)**;
- the source's own mean relative solvent accessibility spans **0.017 (ptp1b, deeply buried)
  to 0.268 (kras, exposed)**.

**Consequence for the method.** Any observable with an absolute length scale — a diffusion
time, a decay length, a dephasing rate, a neighbourhood radius — is being asked to work
across a 3× range in the distance it has to cross and a 20× range in the size of the object
it starts from. Either the scale is set per target from the graph's own spectrum, or it is
a hyperparameter with a 3× mismatch built in. Every time and length scale in
`allo.quantum.walk` is set from the operator's spectral range for exactly this reason.

### 3.4 Eigenvector centrality is a proximity ranker on some arms and an anti-proximity

ranker on others.

The Spearman correlation between eigenvector centrality and negated distance-to-source runs
from **−0.227 (smyd3)** to **+0.802 (ptp1b)**. Weighted degree behaves similarly, +0.107 to
+0.535.

So "centrality is distance in disguise" is not a property of protein graphs. It is a
property of where the active site happens to sit: when the active site is buried in the
core, the residues near it are also the high-centrality ones, and the two scores agree; when
the active site is peripheral, they diverge and can anticorrelate.

**Consequence.** The confound has to be measured per arm, not assumed. Reporting one pooled
correlation would average +0.802 against −0.227 and produce a number that describes no arm.

---

## 4. Data-quality notes

- **Every graph is connected.** One component on all fourteen, so no Laplacian pseudoinverse
  and no resistance-like quantity is undefined anywhere, and no arm needs a special case.
- **No isolated residue exists at the frozen cutoff**, and `allo.network.build` refuses to
  return a graph containing one rather than letting a scorer divide by a zero degree.
- **B-factors are present and non-degenerate on all fourteen arms**, so the normalised
  B-factor confounder column is real everywhere rather than silently constant.
- **The spectral ratio λ_max/λ₂ of the Laplacian spans 33 to 920.** The largest values are
  p97_vcp (920) and hiv_rt (727), both elongated multi-domain chains. Any iterative solver
  on the Laplacian is that many times slower to converge on those two, which is a practical
  ceiling worth knowing before a sweep, not after.
- **`ns5b` has a three-residue active site.** It is the GDD motif, and it is the smallest
  source in the benchmark by a factor of three. Any score that averages over source residues
  has the least averaging available there.

---

## 5. What this changes for our pipeline

- **S5, the propagation observable.** The collapse-onto-eigenvector-centrality argument is
  arm-dependent, not universal. It is retained as the expected behaviour on the ten
  high-gap arms and **suspended on hiv_rt, ns5b, smyd3 and p97_vcp**. Print the
  eigenvector-centrality rank correlation on every arm and read it against the gap column
  above.
- **S1, the graph.** Raw topology is near-constant across arms, so a graph variant can only
  help by changing the _weights_, not by changing which pairs are in contact. That is a
  direct argument for the weighted variants and against tuning the cutoff.
- **S3, the operator.** Every time and length scale must be derived from the operator's own
  spectrum. A fixed constant is a 3× mismatch on this set.
- **S6, confound removal.** The distance-to-source distribution differs by 3× across arms, so
  the decay fit is per-target by necessity and not only by the C1 argument. A `k` carried
  between targets would be wrong on arithmetic before it was wrong on leakage.
- **S10, reporting.** The per-arm confound correlation belongs in the report as a column,
  because its sign is not constant.

## Method

No retrieval. `profile_graphs.py` in this directory builds each arm's graph through
`allo.network.build` at the input layer's frozen cutoff, and computes every quantity from
that graph, the Cα coordinates, the deposited B-factors and the frozen active site. The
level-spacing ratio needs no unfolding, which is why it is used in place of a
nearest-neighbour spacing distribution. Reference values 0.386 (Poisson) and 0.536 (GOE) are
the standard ones for the ratio statistic. Output: `frozen-graph-profile.json`.

**Limitation.** Fourteen graphs is a small sample for a distributional claim. The four
low-gap arms are four arms, and the statement in §3.2 is a hypothesis with a named test, not
a finding. The 501-graph profile in `review/09-data-analysis.md` has far more power for the
_distributional_ question and is not superseded by this file — it is complemented by it,
because the question here is what happens on these fourteen specifically.
