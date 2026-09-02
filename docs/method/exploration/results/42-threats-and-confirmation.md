# What would make the winner spurious, and what has to happen before it is a result

**Written 2026-08-26**, while the screen was still running, and deliberately so. Every threat
below is stated before the winner is known, because a threat named after the fact is not a
control — it is a rationalisation.

Read this before [`40-method-sweep.md`](40-method-sweep.md).

---

## 1. What the screen is, in one paragraph

Four experiments ran on the four `development` arms of the secondary benchmark — `mkp5`,
`ptp1b`, `hiv_rt`, `ns5b` — and on nothing else. `2026-08-26-method-sweep` scores every
combination of eight graphs, 54 scorers and three to five confound-removal forms.
`2026-08-26-mechanism-probe` scores four constructions taken from the cross-system mechanism
review. `2026-08-26-fusion-probe` scores label-blind combinations of them and the two
site-assembly rules. `2026-08-26-selection-power` measures what a screen of that size produces
when the method knows nothing. Every number in all four comes from one call,
`allo.scoring.score_arm`, so no result depends on the script that produced it.

**This is a screen. It selects; it does not confirm.** The distinction is the whole of this
document.

---

## 2. Ten ways the winner could be spurious

Ordered by how likely each is to be what actually happened.

### T1 — Selection. The screen has thousands of chances and one winner.

Of 7 692 scored records, 1 923 variants are complete on all four arms. Even with every variant label-blind, the _maximum_
mean AUC across that many draws sits well above 0.5, and the maximum is exactly the statistic
a screen reports. `2026-08-26-selection-power` measures the ceiling directly: it draws
label-blind spatially autocorrelated fields through the same harness and reports the best-of-V
distribution for V from 1 to 10000.

**Control.** Report the winner against the ceiling at the V the screen actually ran, never
against 0.5. **Status: measured.** See [`41-selection-and-power.md`](41-selection-and-power.md).

### T2 — The variants are not independent, so the correction is the wrong size.

Nearly two thousand variants are not two thousand tests. Most of the 54 scorers are functions of the
same operator read at the same source column, and
`docs/method/exploration/lit/22-transport-formalisms.md` says so explicitly. A Bonferroni
correction over 1 923 would be far too conservative. A correction over 1 would be far too
permissive.

**Control.** The participation ratio of the eigenvalue spectrum of the variant-by-variant rank
correlation matrix converts "we screened this many" into "we screened this many independent
things". **Status: measured on the finished screen** — 1 620 variants hold **8.86** independent
directions on `mkp5` and **10.58** on `ptp1b`. An earlier linear extrapolation from a
150-variant subset gave ≈155 and was wrong by more than an order of magnitude. The correction
widened the ceiling into an interval rather than closing the threat.

### T3 — Distance. The single confound that explains most published allosteric-site results.

An allosteric site is distal by definition, so _any_ score that decreases with distance from
the active site scores above chance, and a score that increases with it scores below chance.
The frozen calibration already shows the negated-distance baseline running from AUC 0.215 to
0.589 across the primary arms — informative in both directions, and never a method.

**Control, three layers.** The rank correlation against `distance_from_source_negated` is on
every record. Five confound-removal forms are swept as a first-class axis, so a variant that
only survives raw was measuring distance. And `distance_from_source_negated` is one of the
three controls each record is scored against.
**Status: measured, and it is doing work** — `strain_versus_diffusion` runs from ρ = −0.98 to
+0.18 against negated distance across its variants, which is the finding rather than a
footnote.

### T4 — Burial. The confound the null was built to absorb.

Buried residues are more contacted, more conserved, less mobile and closer to everything, so
almost every graph score is partly a burial score. `24-residue-descriptors.md` shows that six
separate published descriptor families — Voronoi volume, weighted contact number, occluded
surface, residue depth, DPX, CX — are one axis, and that axis is burial.

**Control.** The matched-patch null resamples patches matched on size, component count, mean
degree and radius of gyration. A high AUC with a high p-value is the expected signature of
that null working, not a bug. **Status: built into the frozen protocol.**

### T5 — The endpoint and the deliverable are different claims.

The confirmatory endpoint is the mean midrank of the label set. The challenge's deliverable is
a five-residue hit list. These come apart, and the repository has already measured how far:
`cavity_volume` rejects the confirmatory null on all three primary arms at p = 0.0073 /
0.0003 / 0.0001 **with recall@5 of 0.00 on all five**, and on `bcr_abl1_corrected` its
predicted centre is farther from the site than a random five-residue list.

**Control.** `hits_at_5`, `recall_at_5` and `dcc_angstrom` against its own chance line are
printed for every variant, and no file here reports an AUC without them.
**Status: enforced.** In the mechanism probe the leader has a mean AUC of 0.714 and a DCC worse
than chance on two of four arms, which is the same phenomenon appearing again.

### T6 — Four arms cannot resolve the differences the ranking is built on.

The frozen minimum detectable effect at 80 % power is AUC **0.762 to 0.936 at α**, rising to
**0.799 to 0.961 at α/3**. A ranking that separates 0.71 from 0.69 is ordering numbers the
benchmark cannot distinguish.

**Control.** No claim rests on a rank difference smaller than the resolvable band, and the
band is printed beside the ranking. **Status: enforced by the write-up, not by the code.**
This is the weakest control in the list and it is stated as such.

### T7 — The graph and the detrend axes may interact, and the design does not fully cross them.

The two additional confound-removal forms run on three of the eight graphs rather than all
eight, because full crossing costs 2688 further scored variants on an axis the first pass
showed to be flat.

**Control.** The three-graph subset holds the zero point plus the strongest weighted and
strongest single-point graph, so a strong interaction shows up as a rank change inside it.
**Status: a stated design limitation, disclosed in `config.yaml`.** No silent truncation.

### T8 — The prior work is not independent evidence.

Much of what the Phase-2 plan treated as settled came from `allosteric-benchmark/`, whose own
evaluation sets contain all three of our primary targets. **ADR 0026** records the finding.

**Control.** Its results are prior, not verdict. No hyperparameter here is set by reading it,
and its best method is reimplemented rather than cited, so it runs on our graph and our null.
**Status: closed by ADR 0026 and by `allo.classical.baselines.alps_spectral_response`.**

### T9 — Sign flips chosen after seeing the data.

An AUC of 0.31 and an AUC of 0.69 are the same measurement. Choosing the direction after
looking is selection with a sample size of two.

**Control.** Both directions stay in the table, the refuted one named as refuted, and the
choice is made on `development` and nowhere else (ADR 0021). **Status: one such flip has
happened** — `soft_corridor_to_source` to `stiff_corridor_to_source` — and it is written up as
a refuted prediction rather than as a discovery.

### T10 — A holo-tuned constant reached the prediction path by hand, not by import.

Found by the `constraint-auditor` pass on 2026-08-26, after the screen had already run.
`alps_spectral_response` is a reimplementation of the teammate benchmark's best method, and
its three constants — `radius = 12.0`, `stiffening = 2.0`, `modes = 3` — carry a comment in
that repository saying they were "re-tuned on curated labels". That curated set contains the
ABL1 myristoyl pocket (`3K5V`, `3PYY`), a PTP1B allosteric complex from the same series as our
`ptp1b` development arm's holo entry (`1T49`), and the myosin blebbistatin site (`2JHR`,
`3BZ7`). No module imports anything and no protected file is opened. A person read three
numbers and typed them in.

This is the exact route ADR 0026 predicted — "arrives here by a route no test watches" — and
clause 2 of that ADR forbids a stiffening constant as a default by name.

**Control, applied after the finding.** The function defaults are no longer theirs. The
published triple is one point in a sweep and never a default. And
**`alps_spectral_response` is not eligible to be selected as our method.** It is reported as a
bar, and it is an *optimistic* bar, because it was tuned with an advantage no candidate here
has. Beating it means something. Losing to it does not.

**Two smaller instances of the same class, fixed in the same pass.** `diversified_top_k`
defaulted to an 8.0 A exclusion radius, whose nearest documented source is that repository's
measured 8.2 A separation, and `spatial_smoothing` defaulted to a tuned 6.5 A. Both defaults
are now 0, which is the control in each case, so a non-zero value has to be passed in by a
caller that swept it.

**The general lesson, and it is the one worth keeping.** The leakage guard follows the import
graph and five file-read routes. It cannot see a number that a person carried across. The only
defence is that every constant on the prediction path names its provenance in its own
docstring, and that an audit reads them.

---

## 3. What is _not_ a threat here, and why

Worth stating, because a threat list that includes everything is not a threat list.

- **Leakage from the holo structure (C1) through code.** The audit computed the full
  transitive import closure of every new module: they reach `allo.inputs`,
  `allo.network.graph` and `allo.structure.pdb` and nothing else. The new `bfactor` field
  reads `apo.structure.bfactor`, whose file is SHA256-pinned to the apo record and whose cache
  partition is held by its own test. **Leakage by hand is a different matter — see T10.**
- **MD contamination (C2).** No trajectory, no MD-derived covariance, no MD-trained weights.
  `25-md-free-fluctuation.md` checked each candidate model against its own training corpus and
  ruled out eight by name, Boltz-2 included.
- **Tuning on the test set.** The `generalisation` tier stays closed and the primary benchmark
  is scored once, with every choice already fixed (ADR 0012, ADR 0021).
- **Reproducibility.** Every stochastic step takes an explicit seed, every runner is
  resumable on a key, and a rerun of a committed config reproduces its metrics.

**One gap in the guard itself, worth knowing.** `tests/test_no_leakage.py` discovers runner
scripts through `git ls-files`, so it inspects tracked files only. While the four experiment
directories were untracked, the gate passed without looking at them. The audit ran the same
`runner_violations` check over every file in all four by hand and they are clean, and the gate
covers them from the moment they are tracked. A guard that silently skips new work is a guard
worth naming.

---

## 4. The confirmatory design that follows

The screen cannot produce a result. This is what turns its output into one, and it is the next
unit of work rather than something this session did.

**Step 1 — Freeze one method.** One graph, one scorer, one confound-removal form, one
site-assembly rule, every parameter written into an ADR. Not a family, not "the best of these
three". The screen's job is to pick this, and picking it is the last decision the
`development` tier is allowed to make.

**Step 2 — Pre-register the prediction.** Write down the expected AUC and the expected
recall@5 on the `generalisation` tier _before_ opening it, together with the value at which
the method would be abandoned. The screen supplies the expected value; the prediction is what
makes the next step a test rather than a measurement.

**Step 3 — Score the `generalisation` tier once.** Five arms, never before opened, one call
each. This is the confirmatory test of generalisability, and its result stands whatever it is.

**Step 4 — Score the primary benchmark once.** Five arms, Holm-Bonferroni across the three
confirmatory ones, `cavity_volume` as the required comparator rather than chance. The claim
threshold is beating `cavity_volume`, not beating 0.5 (ADR 0025).

**Step 5 — Report both endpoints, always.** The confirmatory p-value and the five-residue hit
list are different claims, and a report that prints only the first misleads. The repository
already has the worked example of exactly that failure and it must be cited in the report.

**What would abandon the whole route.** If the frozen method's AUC on the `generalisation`
tier falls inside the label-blind ceiling from `41-selection-and-power.md` at the V the screen
ran, then the screen selected noise, and the correct write-up is a negative result with the
ceiling as its evidence. That outcome is planned for, not feared.
