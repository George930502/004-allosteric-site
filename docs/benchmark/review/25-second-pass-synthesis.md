# Second-pass audit: what must change, ranked

**Closed 2026-09-02, after the first pass.** `11-synthesis.md` audited the three frozen layers
against the organisers' answers and produced ADRs 0029 to 0036, a six-arm primary re-freeze and
evaluation protocol version 3. **Nobody had audited that work.** This pass does, and it audits
the layers again from outside, with an adversarial model reading the whole repository in
parallel.

**Scope.** Nine delegated reviews (`16` to `24`), one constraint audit against C1-C6, and two
independent `gpt-5.6-sol` passes: an adversarial review of the working tree and a whole-repository
audit from the first commit. Every finding below was re-checked by me against the code or the
deposited data before it was written down. Where a delegated agent and the adversarial model
disagreed, I ran the measurement that settles it and say who was right.

**Nothing here is frozen and nothing here moves a freeze.** Each item names the ADR that would
have to accept it.

---

## 0. Headline

**Both freezes verify.** `make check` and `make verify` exit 0: `allo benchmark verify --set all`
over six primary and nine secondary arms, and `allo evaluate verify --detect` at protocol
version 3 over fifteen arms and 777 decoy pockets, with the network tests re-downloading every
pinned artifact. The layers are internally consistent and reproduce from the deposited files.

**Five things block scoring, and none of them was known this morning.**

1. **A complete label set sits in an unprotected file.** `docs/targets.md` prints all twelve
   cardiac myosin label residues. C1 forbids the residue count; this is the residues.
2. **A second C1 leak in `experiments/`.** The sealed `generalisation` tier's exact positive
   count is in a tracked, unprotected file.
3. **The claim threshold moved and nothing recorded it.** Under version 3, `cavity_volume` no
   longer rejects on three of three confirmatory arms. It rejects on **one**.
4. **The decoy-pocket p-value does not test the statistic its ADR specifies.**
5. **A `src.`-prefixed import walks past every C1 import guard.**

**One finding is not a defect but a result.** Sequence conservation does not separate the
allosteric labels from the background on this benchmark: median AUC-ROC **0.491**, Wilcoxon
p = 0.76. That is the fourth confounder column, built and measured (`24-conservation-measured.md`).

---

## 1. Blockers

### 1.0 `docs/targets.md` holds a complete label set, unprotected — **repair, urgent**

**This is the most severe finding of the pass, and it is the answer key itself rather than a
count.** `docs/targets.md` is tracked, is named nowhere in `PROTECTED_PATHS` or
`FROZEN_TOKENS`, and prints the cardiac myosin site in apo author numbering:

> The site is reproducible across all six copies: **Tyr164, Thr167, Asp168, His666, Pro710,
> Asn711, Arg712, Ile713, Glu774** in every one, plus Arg721, Tyr722, Leu770 in most.

Checked against the freeze, that list is **12 of 12** — the complete `label_residues` set of
both `cardiac_myosin_mandated` and `cardiac_myosin_corrected`:

```
frozen label_residues : [164, 167, 168, 666, 710, 711, 712, 713, 721, 722, 770, 774]
named in targets.md   : [164, 167, 168, 666, 710, 711, 712, 713, 721, 722, 770, 774]
```

The same file also prints minimum label-to-active-site distances per arm. Any prediction
module can read it with one line and the leakage gate returns nothing, because the file is
neither a protected path nor a scanned runner.

`extension-candidates.md` became protected route four on exactly this argument — a tracked
Markdown answer key — and `docs/benchmark/review/` became route seven on it. **`docs/targets.md`
is older than both and was never checked.**

**Recommended:** protect it, or move the residue lists behind the `groundtruth` boundary and
leave the file describing the entries. Protecting it is the smaller change, but note that
`AGENTS.md` sends every agent to `docs/targets.md` when "touching a specific protein", so
protecting it changes a documented routine. Sweep the rest of `docs/` on the same argument
before assuming this is the only one.

### 1.1 `experiments/` is the eighth C1 data route — **ADR required**

`tests/test_no_leakage.py:24` lists seven protected paths. `experiments/` is not one, and
`experiments/2026-08-25-null-calibration/metrics.json` is tracked, committed and readable by any
prediction module.

Its `nulls.matched_patch.diagnostics` blocks carry `observed_components` per arm. Summing them
recovers the positive count exactly — **including for all five arms of the sealed
`generalisation` tier**, which is not opened until Phase 5:

| sealed arm    | `observed_components` | `secondary/frozen.json` positives |
| ------------- | --------------------- | --------------------------------- |
| `chk1`        | 12                    | 12                                |
| `smyd3`       | 12                    | 12                                |
| `glucokinase` | 19                    | 19                                |
| `p97_vcp`     | 17                    | 17                                |
| `ecoli_cps`   | 19                    | 19                                |

The same blocks carry `observed_radius_of_gyration` and `observed_median_distance_to_source` —
the true site's own geometry. `AGENTS.md` gives _those exact field names_ as the reason
`data/patches/` became protected route six on 2026-08-27. **The identical payload was already
sitting in an unprotected tree and the audit that closed route six did not look there.**

I verified the gate is blind to it: a prediction module reading that path produces zero
violations, because `is_runner()` skips `.json`, so the file is neither protected as data nor
scanned as a runner.

**Recommended:** strip `diagnostics.observed_*` and `n_positive` at write time in
`allo.scoring.harness`. Nothing reads them. Protecting the tree instead would break every
experiment runner. Verified by me, not delegated.

### 1.2 The `src.` prefix walks past every import guard — **repair, no ADR**

`tests/test_no_leakage.py:142` ends `imports_from_source` with
`{name for name in found if name.startswith("allo")}`. `src/` is an implicit namespace package
from the repository root, so `import src.allo.groundtruth.labels` works and is silently dropped
by that filter. I confirmed both halves: the import succeeds, and the filter discards the name.

A planted probe importing holo label code into `allo.network` passed all 32 tests. No module
uses the prefix today, so this is a latent hole, not an active breach. It is the same failure
mode as the parent-package route closed on 2026-08-27: the guard reads the text correctly and
the interpreter does something the text does not show.

**Recommended:** strip a leading `src.` before the filter, and add the form to
`test_the_detector_sees_every_import_form`.

### 1.3 The pre-declared claim threshold is stale — **ADR required**

ADR 0025 makes "beat `cavity_volume`" the claim, and ADR 0032 makes it a confirmatory family.
The founding measurement was `cavity_volume` rejecting on **all three** confirmatory arms at
`p_calibrated` 0.0073 / 0.0003 / 0.0001.

Re-scored under version 3, it gives **0.0715 / 0.3236 / 0.0046**. Holm rejects **one of three**.
AUC-ROC moved 0.795 to 0.563 on BCR-ABL1 and 0.977 to 0.806 on myosin.

The cause is mechanical and nobody traced it: ADR 0030 re-froze the detector, and
`cavity_volume` is computed _from_ the detector's cavities. Re-freezing the decoy detector
silently redefined the baseline the claim is measured against.

Three documents now quote three different, all-stale triples: `evaluation/manifest.yaml`, ADR
0025 and ADR 0032. Measured in `21-protocol-v3-statistics.md`.

### 1.4 The decoy-pocket p-value tests a different statistic from its ADR — **repair or ADR**

ADR 0030 line 11 defines the test as the site pocket lining ranked against the decoy pocket
linings, and its power argument is explicitly about "the site pocket's separation from the
decoys".

`harness.py` computes `site_score` from the site lining at line 258 and uses it only for the
reported `site_pocket_rank`. Line 365 computes the p-value as
`permutation_p(observed, decoy_ranks)`, where `observed` is the mean midrank of the **whole
scoreable label set**. The Fisher combination — the tested form of the challenge's negative
class (b) — therefore combines p-values for a statistic the ADR does not describe.

Both readings are defensible on their own terms; the label-set version is arguably closer to
`CHALLENGE.md` §4.1. **The defect is that the specification, the power calculation and the code
name three different things.** One of them has to move.

---

## 2. Adjudicating the adversarial model

`gpt-5.6-sol` returned eight findings from the working tree and seventeen from the whole
repository. Judged one at a time, against the code.

| #   | Claim                                                                 | Verdict                                                           |
| --- | --------------------------------------------------------------------- | ----------------------------------------------------------------- |
| C-1 | Protocol v3 is post-hoc; "no method scored under v2" is false         | **Confirmed as written, overstated as risk.** §2.1                |
| C-2 | The detector was tuned on the answer key                              | **Fact right, consequence refuted.** §2.2                         |
| C-3 | The decoy p-value tests the wrong statistic                           | **Confirmed.** §1.4                                               |
| C-4 | Family 2 is not size-calibrated and may be anti-conservative          | **Gap confirmed, anti-conservatism refuted by measurement.** §2.3 |
| C-5 | The myosin source rule was ratified against a holo structure          | **Confirmed as a disclosure defect.** §2.4                        |
| C-6 | c-Myc is declared complete and does not exist                         | **Confirmed.**                                                    |
| C-7 | The Faccin theorem is applied to the wrong operator                   | **Open.** §2.5                                                    |
| C-8 | Fourteen quantum scorers have no C3 resource account                  | **Confirmed.**                                                    |
| #11 | The infinite-time connectivity matrix is wrong for degenerate spectra | **Confirmed, severity reduced by measurement.** §2.6              |
| #16 | The reported top-5 depends on the answer key                          | **Confirmed, direction is conservative.** §2.7                    |
| #10 | `score_arm` returns `n_positive` and prevalence                       | **Confirmed as fact.** §2.8                                       |
| #6  | The "frozen" v3 state is not committed                                | **Confirmed.** §2.9                                               |

### 2.1 C-1, protocol v3 and prior scoring

`evaluation/README.md:6` states "**No method had been scored under version 2**, which is the only
condition under which this layer may move at all." The same document at line 1005 reports "All
five passed on 2026-08-25 under protocol version 2" and prints `cavity_volume` p-values from
that run, and `experiments/REGISTRY.md` records a 6 480-record method sweep on 2026-08-26.

**The sentence is false as written and must be narrowed.** The defensible statement is that no
_candidate_ method was scored on the primary confirmatory arms under v2 — the sweep ran on the
secondary `development` tier and the two v2 primary scores were the protocol's own required
controls.

**The risk is lower than the model claims.** Its recommendation to "quarantine protocol-v3
results" and to require "a genuinely unopened benchmark" does not follow: the
`generalisation` tier is still sealed and is the set that carries the generalisation claim.
But §1.3 shows the concern is not empty — one v3 change did move a load-bearing baseline
after it had been measured, which is exactly the chronology the manifest forbids.

### 2.2 C-2, the detector and the answer key — **I ran the measurement that settles it**

`evaluation/manifest.yaml:225` says "`n_decoys` is label-free and is a sample-size criterion, so
selecting on it cannot shape the negative class with the answer key."

**That sentence is false.** `decoys.classify()` picks the site pocket by maximum label coverage
and then admits a pocket as a decoy only if its lining holds no label and lies beyond the halo
of every label. `n_decoys` is a function of the labels by construction. The adversarial model is
right and my own constraint audit was wrong to call the criterion label-free.

**The consequence is nil, and this is measurable.** The genuinely label-free quantity
`n_detected` selects the identical setting on every arm in the committed sweep:

| arm                        | argmax on `n_decoys`   | argmax on `n_detected` | same |
| -------------------------- | ---------------------- | ---------------------- | ---- |
| `kras_g12c_mandated`       | `po 8 rd1.2 vol1` (13) | `po 8 rd1.2 vol1` (16) | yes  |
| `kras_g12c_corrected`      | `po 8 rd1.2 vol1` (18) | `po 8 rd1.2 vol1` (21) | yes  |
| `bcr_abl1_mandated`        | `po 8 rd1.2 vol1` (41) | `po 8 rd1.2 vol1` (44) | yes  |
| `bcr_abl1_corrected`       | `po 8 rd1.2 vol1` (31) | `po 8 rd1.2 vol1` (35) | yes  |
| `cardiac_myosin_corrected` | `po 8 rd1.2 vol1` (84) | `po 8 rd1.2 vol1` (85) | yes  |

**Recommended:** restate the criterion as `n_detected`, record that `n_decoys` agrees, and
delete the false sentence. The chosen setting does not move, so no re-freeze is needed. One
caveat stands: the manifest says the sweep ran over all fifteen arms while the committed record
holds five, so the same check cannot be run for the sealed tier without opening it. Selecting on
`n_detected` removes the need to.

### 2.3 C-4, the second confirmatory family

`compare_methods` produces a two-sided p — `extreme` counts `|null - centre| >= |observed - centre|`
— and passes it to `calibrated_p`, whose probit transform `max(p, sf(isf(p)/ratio))` is the
one-sided form. The two-sided analogue under the same Gaussian model is `2*sf(isf(p/2)/ratio)`.
The applied correction is smaller at every ratio in the freeze:

| `size_ratio` | raw p | applied | two-sided analogue |
| ------------ | ----- | ------- | ------------------ |
| 1.0509       | 0.05  | 0.0588  | 0.0622             |
| 1.0960       | 0.05  | 0.0667  | 0.0737             |
| 1.2073       | 0.05  | 0.0865  | 0.1045             |

The docstring's defence — "it only ever tightens, so the direction is the safe one" — is true of
the transform's monotonicity and does **not** establish that the resulting test holds its size.
Those are different claims, and until today only the first had evidence.

**The measurement now exists and it favours the repository.** `21-protocol-v3-statistics.md`
gated family 2 for the first time and found its size holds. So: the adversarial model correctly
identified an unevidenced assertion in a load-bearing decision rule, and the evidence, once
gathered, supports the rule. **ADR 0032 declared a confirmatory family without running the
ADR 0018 calibration gate on it.** The gate has now been run; the ADR should cite it.

### 2.4 C-5, the myosin source rule

`src/allo/inputs.py:97` records the three `MYO_*` motifs as validated at "Jaccard 0.483 on
`9GZ3`:A and 0.516 on `9GZ2`:A, centroid offset 5.96 and 5.92 Å". `9GZ2` is the **holo** entry.
The motifs define the propagation source for `cardiac_myosin_mandated`, which is squarely on the
prediction path.

**Severity is disclosure, not corruption.** The apo row is within 0.03 Jaccard and 0.04 Å of the
holo row, so the decision stands on apo evidence alone and the holo number is redundant. But
ADR 0031 orders the 0.48-0.52 range printed with the arm, which propagates a holo-derived
endpoint into the submission. No file-read guard can see this route; a human read it.

**Recommended:** cite the motifs to primary literature, print only the apo-derived validation,
and record the redundancy rather than the holo number.

### 2.5 C-7, the Faccin theorem — **the reviewer is right on substance and wrong on detail**

I read the paper (arXiv:1305.6078v2, full text) rather than accepting either side.

**Where the repository is right, and the reviewer is wrong.** The bound really is `E / Δ`, energy
over the gap. Equation 7 gives
`E = tr{H_Q ρ} = Σ_{j≠0} λ_j tr{Π_j ρ} ≥ Δ Σ_{j≠0} tr{Π_j ρ} = Δ ε`, and Table I's caption reads
"The quantumness ε and its upper bound E/Δ, the ratio of energy and gap". The abstract's
gap-free phrasing is the loose one. The classical long-time occupation being `d_i / Σ_j d_j`,
and the quantum average matching it exactly at zero energy, are both supported.

**Where the repository is wrong, on three counts.** The theorem is about a different operator
than the one `allo.quantum` uses.

| | the paper | `quantumness.py` |
| --- | --- | --- |
| Hamiltonian | `H_Q = D^(-1/2) L D^(-1/2)` (p.2, Fig. 1 caption). `A` is only the input from which `D` and `L` are built | the adjacency `A` |
| initial state at the classical point | the degree-weighted ground state `\|φ₀⟩ = D^(1/2)\|1⟩`, unique at `λ₀ = 0` | a site-basis state `\|i⟩` |
| `Δ` | `min_{i≠0} λ_i`, the gap **above the ground state** | `abs(values[-1] - values[-2])`, the **top** adjacency gap |

**Measured on `kras_g12c_mandated`, so this is not an argument about notation:**

```
(H_Q)_ii              = 1.000000 at every node        the repo's premise is <i|H|i> = 0
paper's Delta         = 0.056004                      quantumness.py uses 1.4383  (26x apart)
site-state quantumness eps = 1 - d_i/sum(d) = 0.994   the repo calls this "the classical point"
```

`⟨i|A|i⟩ = 0` is a true statement about the adjacency. It is not the theorem's zero-energy
condition, and under the paper's own operator a site-basis source sits at `ε ≈ 0.994` — the
**maximally quantum** end, the exact opposite of what `quantumness.py` lines 12 to 16 assert.

**What survives and what does not.** The empirical observation stands: the walk observables did
behave classically, and `2026-08-26-method-sweep` measured `eigenvector_centrality` as the best
scorer at mean AUC 0.810. **The explanation does not.** And the repository already contains the
simpler one it needs: `walk.py:64` records that the adjacency walk's ground state is the Perron
vector, "so a walk on it is the construction that reproduces eigenvector centrality". That is
what the sweep found. Faccin's degree result is not needed and does not apply.

**Consequence.** `docs/ROADMAP.md` carries the `E/Δ` diagnosis under "One diagnosis that changes
what Phase 2 means", and the 21.7x cross-arm spread it quotes is a spread in the **top adjacency
gap**, not in the paper's `Δ`. The paragraph must be rewritten or withdrawn, and
`quantumness.py`'s two levers must be re-derived or re-motivated without the theorem. This is a
method-layer item and belongs to Phase 2, not to the benchmark layers.

### 2.6 #11, the infinite-time connectivity matrix — **confirmed, then measured**

`connectivity.py:54` returns `squared @ squared.T` as the `T → ∞` limit. That equals
`Σ_k |⟨i|k⟩|²|⟨k|j⟩|²`, which is the correct time average **only for a non-degenerate spectrum**.
With degeneracy the limit needs squared spectral projectors, `Σ_λ |⟨i|P_λ|j⟩|²`.

On `K3`, which has a doubly-degenerate eigenvalue, the error is worse than the model reported —
0.191, not 1/6 — and the failure is qualitative: the naive form returns diagonal entries
0.365 / 0.551 / 0.417 on a graph whose three nodes are interchangeable, because it depends on
the arbitrary basis LAPACK happens to pick inside the degenerate eigenspace. The projector form
correctly returns 0.556 on all three.

**On the real arms the consequence is small, and I measured it rather than assuming either way.**

| arm                        | nodes | minimum eigenvalue gap | affected |
| -------------------------- | ----- | ---------------------- | -------- |
| `kras_g12c_mandated`       | 169   | 5.11e-03               | no       |
| `bcr_abl1_corrected`       | 272   | 1.40e-03               | no       |
| `cardiac_myosin_corrected` | 764   | **2.22e-15**           | yes      |

The myosin arm has a genuine doubly-degenerate eigenvalue at exactly −1 inside a single
connected component. The resulting error is **1.4e-4 at most, on 16 of 583 696 entries**.

**Verdict: a real correctness bug with a negligible present effect and a four-line fix.** It
should be fixed because the N × N connectivity matrix is a mandated deliverable
(`CHALLENGE.md` §5) and because a matrix that depends on the LAPACK build is not reproducible.

### 2.7 #16, the reported top-5 depends on the labels

`metrics.top_k_indices` is `np.lexsort((positive, -scores))[:k]`. The label mask is the
tie-breaker. Under tied scores the selected list changes when only the answer key changes.

The direction is conservative — non-positives are taken first, which is the pessimistic rule the
docstring claims — so no method is flattered. But `dcc_angstrom` and `top_5_components` are
computed from this list, and the top-5 hit list is the challenge's mandated artifact. **A
deliverable handed to a chemist must not be a function of the answer key**, whichever way the
tie falls.

**Recommended:** keep the pessimistic rule for scoring, and break ties by residue number for the
reported artifact. Say which is which.

### 2.8 #10, `score_arm` returns the positive count

Confirmed at `harness.py:306`: the record carries `n_positive` and `prevalence`. `AGENTS.md`
states C1 as "not even the residue count". The tension is real, though the path is the
evaluation side rather than the prediction side, and the mitigation is procedural: the primary
set is scored once, with the method already fixed. **Record it as a disclosed property of the
harness, or strip both fields.** The adaptive-query attack the model describes is the standard
hazard of any visible scoring oracle and is not specific to this repository.

### 2.9 #6, the frozen state is uncommitted

Correct, and it is the plainest finding of the pass. HEAD `a472c48` still holds protocol version
2 and five primary arms. ADRs 0029-0036, the September calibration experiment, the substitutions
report and this whole review directory are untracked or unstaged. **A clean clone cannot
reproduce the state the documents describe as frozen.** This is a housekeeping failure, not a
scientific one, but it makes every "frozen" claim unverifiable by a third party.

---

## 3. New findings from the delegated reviews

Each is written up in its own file. Ranked by what it costs.

| #    | Finding                                                                                                                                                                                                                             | Where |
| ---- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----- |
| 3.1  | **A label-blind cavity ruler clears negative class (b)**: `cavity_volume` reaches Fisher p = 0.01537. No "beat the baseline" threshold exists for that endpoint                                                                     | `21`  |
| 3.2  | **The combined (b) test was never gated.** Measured size 0.0014-0.0066 against nominal 0.05: 7.6x to 36x conservative                                                                                                               | `21`  |
| 3.3  | **`cardiac_myosin_mandated` has no declared reporting role.** Fully scored, 932 candidates, 139 decoys, and unassigned in `decision.supportive_only` — a free parameter                                                             | `19`  |
| 3.4  | **Complete label transfer is required of the secondary set only.** No primary equivalent of `test_every_transferred_label_survives_into_the_node_set`; `bcr_abl1_corrected` loses 2 of 20 and is a claim-family arm                 | `19`  |
| 3.5  | **Clause (xii) ships family-level while ADR 0012 specifies clan-level.** 17 cross-target InterPro collisions, including ABL1 x `chk1`                                                                                               | `19`  |
| 3.6  | **ADR 0024 is orphaned.** ADR 0030 re-froze the detector off pyKVFinder's defaults; ADR 0024 is titled "at its defaults", still `accepted`, superseded by nothing                                                                   | `16`  |
| 3.7  | **`cavity_volume` is the descriptor to beat, not distance.** Median AUC 0.795, Wilcoxon p = 0.0003 — the only apo-only column that rejects chance. Its own bar moves with the detector: 0.795 at defaults, 0.696 at the v3 settings | `22`  |
| 3.8  | **The "0.001080 permutation floor" is not a floor.** True floors 0.000276 / 0.000104 sit _below_ Holm step 1, so "cannot reject at any data" is false                                                                               | `21`  |
| 3.9  | **`5TBY`'s B-factor column runs 0.00-7.30 with no `refine` block**, and **`9GZ2`'s mavacamten carries B = 0.00 on all 20 atoms** — the ligand defining both myosin label sets                                                       | `18`  |
| 3.10 | **34 documentation contradictions**, including three different ADR counts, a guarded-route count of five in three files, and "sixteen arms" three times inside the frozen v3 document                                               | `23`  |
| 3.11 | **Conservation measured: median AUC 0.491, p = 0.76.** ADR 0035's artifact-size blocker dissolves — 1.11 GB of alignments reduce to a 172 KB pinned artifact                                                                        | `24`  |
| 3.12 | **Clause (ii) extension: one new pass, three refutations, twelve still unread.** New admissible arms: **zero**. `generalisation` stays at 5                                                                                         | `20`  |
| 3.13 | **The field has no single formal definition of an allosteric apo/holo pair.** Published contact shells span 3.5-8 Å; three instruments disagree on what breaks apo-ness; the repository states no occupant rule at all              | `17`  |

---

## 4. What held

Reported because a clean check is a result.

- **Both freezes re-derive.** `make verify` exits 0 end to end, including the 777 decoy pockets
  and the byte identity of every pinned wwPDB artifact.
- **No ADR in the 0029-0036 batch rests on a number that fails to reproduce** (`16`). ADR 0029
  explicitly excludes the four disputed SH2 centroid distances that `15` could not reproduce, and
  pins its argument to interface residue counts that reproduce 11 of 11.
- **C1 by import is clean.** All 17 prediction modules imported in fresh interpreters gain no
  `allo.groundtruth` and no `allo.scoring`, parent-package edges included.
- **The node sets are exact** on all six primary arms, recomputed from the mmCIF against
  `frozen.json`.
- **The `size_ratio` calibration is genuinely one-sided** — 0 violations in 30 600 draws — and
  FWER is controlled out of sample at 0.0376-0.0452.
- **The mean midrank is exactly AUC-ROC**, verified as an affine identity, and `17` found the
  repository an in-domain precedent it was not claiming: Amor et al. 2016 runs the same rank-sum
  on residue scores, allosteric against non-allosteric.
- **Live RCSB agrees with the first pass on 175 of 175 paired values.** Nothing drifted between
  2026-09-02 morning and evening (`18`).
- **No MD anywhere.** Every `covariance` in the tree is analytic and says so.

---

## 5. Disposition

**Actioned on 2026-09-02.** `make check` and `uv run allo evaluate verify --detect` both exit
0 after the repairs, and no value in any freeze moved.

| item | what was done | evidence |
| ---- | -------------- | -------- |
| §1.0 | **Refuted as written, and replaced by a wider finding.** `docs/targets.md` holds none of the twelve cardiac myosin label residues; the claim that it does was wrong. A sweep of every tracked `.md`, `.yaml`, `.json` and `.txt` outside the seven protected trees, for a run of label residues inside one 400-character window, found three files that do clear the floor: `primary/audit/kras-g12c.md` at 21 of 21 and `primary/audit/bcr-abl1.md` at 18 of 18, and `evidence/allosteric-prediction-prior-art.md`, which prints the KRAS distal label set as prose. `primary/audit/` and `evidence/` are now protected whole | `test_the_three_new_answer_keys_are_protected` |
| §1.1 | **Closed, and not by protecting the tree.** Protecting `experiments/` outright flags all ten runners, because each names its own output. The rule is narrower: **no file may name a record it did not write.** A run script may name the `metrics.json` and `records.jsonl` beside it; a `config.yaml` is not a record, which is why one runner legitimately reads another run's config | `test_no_file_may_name_a_record_it_did_not_write` |
| §1.2 | **Closed.** `imports_from_source` strips a leading `src.` before filtering, and two probes were added to the import-form test | `test_the_detector_sees_every_import_form` |
| §1.3 | **Closed as a documentation repair; no ADR needed.** The claim threshold is "beat `cavity_volume`", and that rule is unchanged — only the numbers behind it were stale. Re-measured independently here: `p_calibrated` **0.0046 / 0.0715 / 0.3236**, Holm rejects **1 of 3**. `evaluation/README.md` §8, `evaluation/manifest.yaml` and ADR 0025 now carry the v3 values, and ADR 0025's version-2 table is kept as dated history | reproduced review `21`'s script exactly |
| §1.4 | **Closed in favour of ADR 0030, against the code.** The ADR writes `p = (1 + #{decoy_rank >= site_rank}) / (1 + n_decoys)` and `decoy_power_sim.py` draws the site's number from the same unit-variance law as the decoys'. That exchangeability holds only while both halves are a pocket lining. The code passed the label set's own mean midrank, whose sampling variance goes as `1/\|labels\|` against a decoy's `1/\|lining\|` — a statistic no measured type-I rate covers. The code now matches the ADR | `test_the_decoy_p_value_is_built_from_the_site_pocket_and_not_the_label_set` |
| §2 C-4 | **Closed as a false sentence, not a moved freeze.** `n_decoys` is label-dependent: `decoys.classify` picks the site pocket by maximum label coverage and admits a decoy only when its lining holds no label. The label-free criterion is `n_detected`, and it selects `po 8 rd1.2 vol1` on all five arms with no tie — the same setting. The manifest now says so | `data/decoy-power-sweep.json` |
| §2 C-7 | **Corrected in the module, method left alone.** `quantum/quantumness.py` withdraws the paragraph that read Faccin onto the adjacency. Verified here: `(H_Q)_ii = 1.0` at every node, `<phi_0\|H_Q\|phi_0> = 0`, `Delta = 0.056004` against the code's 1.4383, site-basis quantumness 0.994. The two levers stay as measured heuristics with no derivation | numbers re-derived from `1305.6078` |
| §3 | **Two code defects fixed.** The infinite-time connectivity matrix now sums over spectral projectors, so it no longer depends on the arbitrary LAPACK basis of a degenerate eigenspace; `interference._overlap` calls it instead of writing the formula a second time. `top_k_indices` breaks ties by candidate order, so the reported top-5 list is no longer a function of the answer key | two new tests in `test_method.py`, one in `test_scoring.py` |
| §4 | **One first-pass finding does not reproduce.** Review `19` reports `cardiac_myosin_mandated` as scored with no declared reporting role. Its manifest block states "reported and NEVER confirmatory", and the confirmatory family is declared centrally as the three `_corrected` arms. Nothing changed | `evaluation/manifest.yaml: decision.confirmatory_family` |
| §2.9 | **Open, and the user's call.** The whole frozen state is uncommitted. A clean clone cannot reproduce what these documents call frozen | — |

Two ADRs were **not** written, deliberately. §1.3 turned out to change no decision, only stale
numbers behind an unchanged rule. §1.4 turned out to have one defensible answer rather than
three, because the ADR and its own type-I simulation already agreed with each other and only
the code disagreed with both.
