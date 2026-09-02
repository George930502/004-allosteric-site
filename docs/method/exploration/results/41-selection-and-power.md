# What a screen of this size produces when the method knows nothing

**Experiment:** `experiments/2026-08-26-selection-power` · **Ran:** 2026-08-26 · **Seed:** 0
**Read this before quoting any number from [`40-method-sweep.md`](40-method-sweep.md).**

Three measurements, all on the four `development` arms, all through `allo.scoring.score_arm`.
None of them can change a frozen value. They measure the layer's behaviour, not a method's.

---

## 1. The headline

**A label-blind method screened at the raw size of our sweep reaches a mean AUC of 0.771.**

That is the _median_ of the best-of-3000 distribution, not its tail. The 95th percentile is
0.810 and the maximum over 20000 draws is 0.885. Every one of those variants knows nothing
about the label set. They differ from a real method in one respect only: they are smooth
fields on the protein's own coordinates, which is the property every real structural score
also has.

**The sweep's raw size is not its effective size.** Section 4 measures the effective number of
independent variants at **8.86 on `mkp5` and 10.58 on `ptp1b`**, not 1 620. At V ≈ 10 the same
distribution gives a median of 0.628 and a p95 of 0.707.

**So the ceiling is an interval, not a number: p95 between 0.707 and 0.810.** A screen result
below 0.71 is noise on any reading. A result above 0.81 clears the ceiling on any reading. The
sweep's best variant reaches **0.810**, which lands on the upper boundary. Section 5 says what
that does and does not license.

---

## 2. The null distribution of AUC, per arm

500 label-blind spatially autocorrelated fields per arm — 125 at each of four correlation
lengths, the same instrument and the same four lengths the frozen null calibration uses. A
uniform random score would be the wrong null here, because a uniform score has no spatial
autocorrelation and every real method does.

| Arm      | median | p95   | p99   |
| -------- | ------ | ----- | ----- |
| `mkp5`   | 0.528  | 0.780 | 0.845 |
| `ptp1b`  | 0.516  | 0.773 | 0.871 |
| `hiv_rt` | 0.516  | 0.794 | 0.852 |
| `ns5b`   | 0.495  | 0.731 | 0.798 |

**The median is at chance and the p95 is not.** One in twenty label-blind fields reaches AUC
0.78 on a single arm. A paper reporting AUC 0.78 on one protein has reported the 95th
percentile of noise.

The tail widens with the correlation length of the field, on every arm:

| Arm      | λ = 4 Å | λ = 8 Å | λ = 12 Å | λ = 20 Å |
| -------- | ------- | ------- | -------- | -------- |
| `mkp5`   | 0.688   | 0.768   | 0.790    | 0.820    |
| `ptp1b`  | 0.694   | 0.773   | 0.764    | 0.804    |
| `hiv_rt` | 0.669   | 0.766   | 0.810    | 0.819    |
| `ns5b`   | 0.707   | 0.681   | 0.713    | 0.754    |

_(p95 of the AUC, per correlation length.)_

A method whose score varies over a domain rather than over a residue draws from the right-hand
column. Most propagation scores do. This is why the correlation length of a method's own score
field belongs in its write-up.

---

## 3. The selection ceiling

Best-of-V, mean AUC across all four arms, 20000 draws. Variants are drawn independently across
arms, which is the conservative direction: real variants are correlated across arms, so a real
screen's maximum is if anything larger than this.

| V     | median | p95   | max   |
| ----- | ------ | ----- | ----- |
| 1     | 0.504  | 0.638 | 0.811 |
| 10    | 0.628  | 0.707 | 0.816 |
| 100   | 0.700  | 0.756 | 0.859 |
| 792   | 0.746  | 0.791 | 0.867 |
| 3000  | 0.771  | 0.810 | 0.885 |
| 10000 | 0.790  | 0.825 | 0.885 |

Read the row that matches the screen. Taken at face value the method sweep scores 1 620
complete variants, so its raw ceiling sits between the 792 and 3000 rows: **median 0.75 to
0.77, p95 0.79 to 0.81.** Section 4 shows that the face value is the wrong V.

---

## 4. But 1 620 variants are not 1 620 tests

**Measured on the finished screen, not extrapolated.** The participation ratio of the
eigenvalue spectrum of the variant-by-variant rank correlation matrix, over all 1 620 complete
variants, on two arms:

| Quantity                                    | `mkp5`    | `ptp1b`   |
| ------------------------------------------- | --------- | --------- |
| Variants measured                           | 1 620     | 1 620     |
| Effective independent variants              | **8.86**  | **10.58** |
| Fraction independent                        | 0.0055    | 0.0065    |
| Share of variance in the leading eigenvalue | 0.228     | 0.213     |
| Median absolute pairwise correlation        | 0.238     | 0.184     |

**The whole screen holds about ten independent measurements.** The two arms agree to within
two directions, which is the only replication available for this quantity.

An earlier pass measured 3.88 on a 150-variant subset and scaled it linearly to the full
sweep, giving ≈155. **That extrapolation was wrong by more than an order of magnitude.** The
participation ratio does not scale with the variant count, because the added variants are
mostly copies of directions already present. The number above replaces it.

### Which axis actually adds a direction

Same matrix on `mkp5`, sliced by axis. This is the most useful table in the file.

| Slice                                       | Variants | Effective independent | Median \|r\| |
| ------------------------------------------- | -------- | --------------------- | ------------ |
| 54 scorers, one graph, no detrending        | 54       | 3.45                  | 0.428        |
| + all 8 graphs                              | 432      | **4.08**              | 0.389        |
| + all 5 confound-removal forms, one graph   | 270      | **7.22**              | 0.262        |
| everything                                  | 1 620    | 8.86                  | 0.238        |
| one scorer across all 30 graph×detrend cells | 30      | 2.63                  | 0.562        |

**The graph axis buys 0.6 independent directions for eight times the compute. The
confound-removal axis buys 3.8.**

That is the same conclusion [`40-method-sweep.md`](40-method-sweep.md) §5 reaches from a
completely different statistic — the mean AUC spread across graphs is 0.031, and seven of
eight graphs sit inside 0.013. Two independent measurements agree: **the contact definition is
not a lever on this benchmark, and the confound-removal stage is.**

The 54-scorer battery holding only 3.45 directions is the algebraic finding of
`docs/method/exploration/lit/22-transport-formalisms.md` arriving as a measured number: most
propagation scores are one operator read at one source column.

### What this does to the ceiling, and it cuts both ways

**Against the screen:** a Bonferroni correction over 1 620 is far too conservative. The family
size for a multiplicity correction is closer to 10 than to 1 620.

**For the screen:** at V ≈ 10 the label-blind ceiling is **median 0.628, p95 0.707**. The
screen's best variant reaches 0.810, which is **above** that p95. At the raw V = 1620 the p95
is ≈0.80, and 0.810 sits on it.

**So the leader's position is ambiguous, and the ambiguity is the honest answer.** The
variance-based effective V is a **lower bound** on the number of independent chances at a
maximum: two variants correlated at 0.9 still give nearly two chances at an extreme value,
and the participation ratio counts them as one. The raw count is an **upper bound**. The true
ceiling for this screen lies between p95 = 0.707 and p95 = 0.810, and the observed 0.810 sits
at the top of that interval.

**Only the `generalisation` tier can resolve it.** That is what the tier is for.

**The honest ceiling to compare against is therefore an interval, AUC 0.71 to 0.81 at the
95th percentile** — the lower end from the measured effective count, the upper end from the
raw count. A screen result must clear the first to be interesting and the second to be safe.

---

## 5. What four arms can actually resolve

The frozen calibration module's own sensitivity pass, run on the `development` arms at
α = 0.0167 — the tightest Holm level of a three-member family — with 80 % power, 200 fields
and 9999 permutation replicates.

| Arm      | λ = 4 Å   | λ = 8 Å | λ = 12 Å | λ = 20 Å  |
| -------- | --------- | ------- | -------- | --------- |
| `mkp5`   | 0.847     | 0.892   | 0.906    | 0.919     |
| `ptp1b`  | 0.834     | 0.904   | 0.923    | 0.941     |
| `hiv_rt` | **0.794** | 0.885   | 0.924    | **0.955** |
| `ns5b`   | 0.800     | 0.881   | 0.918    | 0.942     |

_(Minimum detectable AUC-ROC at 80 % power.)_

**The band is 0.794 to 0.955.** Nothing below 0.79 is detectable on these arms at this α, at
any correlation length. The committed calibration reports the same quantity on the primary five
arms as 0.799 to 0.961 at α/3 (`experiments/REGISTRY.md`, 2026-08-25), so the `development`
tier is neither easier nor harder than the benchmark it selects for.

**The two bands nearly touch, and how nearly depends on §4.** The minimum detectable effect
starts at 0.794. The label-blind ceiling runs to 0.707 at the measured effective V and to 0.810
at the raw V.

- **At the raw count there is no window.** The ceiling and the resolution limit meet at 0.79 to
  0.81, so no screen result can be both above noise and below the resolution limit.
- **At the measured effective V a narrow window opens: 0.707 to 0.794.** A screen result inside
  it is above the noise ceiling and still below what four arms can resolve.

The screen's best variant reaches 0.810, which is above both ceilings and above the bottom of
the detectable band. **That is the most favourable reading available, and it is still not a
result**, for a reason that does not depend on either boundary: **0 of 1 923 variants reject
the matched-patch null on all four arms** ([`40-method-sweep.md`](40-method-sweep.md) §2).
An AUC above a ceiling is a description. The calibrated p is the test, and it says no.

**Only a pre-specified test on unseen arms can settle this.**

---

## 6. How to report a winner honestly

Five rules, and every file in this directory follows them.

1. **Quote the winner against the ceiling at the screen's effective V**, never against 0.5.
   The measured effective V is ≈10, giving 0.628 median and 0.707 at p95. Quote the raw-count
   ceiling of 0.810 beside it, because the effective V is a lower bound (§4).
2. **Quote the p-value from the matched-patch null, not the AUC.** The null is matched on
   size, components, mean degree and radius of gyration, so it already absorbs the spatial
   structure that produces the ceiling above. An AUC is a description; the calibrated p is the
   test.
3. **Correct the p-value for a family of about 4 within an arm, or about 10 across the
   sweep.** Say which, and why. Never correct over the raw variant count.
4. **Print `hits_at_5`, `recall_at_5` and `dcc_angstrom` against their chance lines beside
   every AUC.** The repository has a worked example of a score that rejects the confirmatory
   null on three arms with recall@5 of 0.00 on five.
5. **State the correlation length of the method's own score field.** It decides which column
   of §2 and §5 the method is being read against, and it varies by a factor of 1.2 in the
   detectable effect and 1.2 in the noise ceiling.

---

## 7. What this experiment does not establish

- **Nothing about the primary benchmark.** These are the four `development` arms.
- **Nothing about a specific method.** It measures the instrument, not a candidate.
- **The effective dimension is measured on two arms of four.** `mkp5` gives 8.86 and `ptp1b`
  gives 10.58 over the full 1 620-variant screen, so the quantity replicates within two
  directions. `hiv_rt` and `ns5b` were not measured, because the solve costs about 20 minutes
  per arm at 550 residues and the two measured arms already agree.
- **The participation ratio is a variance measure used on a tail statistic.** It counts two
  variants correlated at 0.9 as one direction, while a maximum draws nearly two chances from
  them. It is therefore a lower bound on the effective V for a best-of-V ceiling, and it is
  used as one throughout §4. The upper bound is the raw count. Nothing here narrows the
  interval between them, and narrowing it would need a direct best-of-V simulation over the
  screen's own correlation structure.
- **The ceiling simulation draws variants independently across arms.** Real variants correlate
  across arms, which makes the real ceiling higher than the table says, not lower. The
  direction is known; the size is not.
